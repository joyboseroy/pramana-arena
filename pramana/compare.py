"""Run every engine over every case and report where the schools diverge.

Two modes separate logic from ontology:
  stipulated  every engine sees the case exactly as written
  native      each engine sees the case through its own school's ontology
              (the case's `ontology` overrides), so a disagreement may come
              from different logic or from different views of what exists

Usage:
  python -m pramana.compare [--cases data/cases.json] [--out results]
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import os
from dataclasses import asdict
from typing import Dict, List

from .engines import ENGINES
from .model import Case, load_cases

SYMBOL = {True: "valid", False: "invalid", None: "n/a"}


def evaluate(cases: List[Case], mode: str) -> Dict[str, Dict[str, dict]]:
    results: Dict[str, Dict[str, dict]] = {}
    for case in cases:
        row = {}
        for key, eng in ENGINES.items():
            view = case.as_seen_by(eng.ontology) if mode == "native" else case
            row[key] = asdict(eng.fn(view))
        results[case.id] = row
    return results


def diverges(row: Dict[str, dict]) -> bool:
    seen = {v["valid"] for k, v in row.items() if v["valid"] is not None and not ENGINES[k].baseline}
    return len(seen) > 1


def matrix_md(cases: List[Case], res: Dict[str, Dict[str, dict]]) -> str:
    keys = list(ENGINES)
    head = "| Case | " + " | ".join(ENGINES[k].label for k in keys) + " |"
    sep = "|" + "---|" * (len(keys) + 1)
    lines = [head, sep]
    for c in cases:
        cells = [SYMBOL[res[c.id][k]["valid"]] for k in keys]
        mark = " *" if diverges(res[c.id]) else ""
        lines.append(f"| {c.id}{mark} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def agreement_md(res: Dict[str, Dict[str, dict]]) -> str:
    keys = list(ENGINES)
    lines = ["| | " + " | ".join(ENGINES[k].label for k in keys) + " |", "|" + "---|" * (len(keys) + 1)]
    for a in keys:
        cells = []
        for b in keys:
            both = [r for r in res.values() if r[a]["valid"] is not None and r[b]["valid"] is not None]
            agree = sum(1 for r in both if r[a]["valid"] == r[b]["valid"])
            cells.append(f"{agree}/{len(both)}")
        lines.append(f"| {ENGINES[a].label} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def divergence_md(cases: List[Case], res: Dict[str, Dict[str, dict]]) -> str:
    out = []
    for c in cases:
        row = res[c.id]
        if not diverges(row):
            continue
        out.append(f"### {c.id}: {c.title}")
        out.append(f"*{c.thesis}, {c.reason}.* Confidence of the case annotation: **{c.confidence}**.")
        for k, v in row.items():
            out.append(f"- {ENGINES[k].label}: **{SYMBOL[v['valid']]}**, {v['label']}")
        if c.notes:
            out.append(f"\nNote: {c.notes}")
        out.append("")
    return "\n".join(out)


def ontology_effect(cases: List[Case], stip, native) -> List[str]:
    lines = []
    for c in cases:
        for k in ENGINES:
            a, b = stip[c.id][k]["valid"], native[c.id][k]["valid"]
            if a != b:
                lines.append(f"- {c.id}, {ENGINES[k].label}: {SYMBOL[a]} (stipulated) to {SYMBOL[b]} (native)")
    return lines


def report(cases: List[Case]) -> str:
    stip = evaluate(cases, "stipulated")
    native = evaluate(cases, "native")
    n_stip = sum(diverges(r) for r in stip.values())
    n_native = sum(diverges(r) for r in native.values())
    parts = [
        "# Divergence report",
        f"{len(cases)} cases, {len(ENGINES)} engines. A star marks a case where engines disagree.",
        "",
        f"## Stipulated mode (pure logic): {n_stip} of {len(cases)} cases diverge",
        matrix_md(cases, stip),
        "",
        f"## Native mode (logic plus each school's ontology): {n_native} of {len(cases)} cases diverge",
        matrix_md(cases, native),
        "",
        "## Where ontology changes a verdict",
        *(ontology_effect(cases, stip, native) or ["- none"]),
        "",
        "## Pairwise agreement, stipulated mode (agree / comparable cases)",
        agreement_md(stip),
        "",
        "## Divergent cases in detail (stipulated mode)",
        divergence_md(cases, stip),
    ]
    return "\n".join(parts)


def write_outputs(cases: List[Case], out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    for mode in ("stipulated", "native"):
        res = evaluate(cases, mode)
        with open(os.path.join(out_dir, f"verdicts_{mode}.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
        with open(os.path.join(out_dir, f"matrix_{mode}.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["case"] + list(ENGINES))
            for c in cases:
                w.writerow([c.id] + [SYMBOL[res[c.id][k]["valid"]] for k in ENGINES])
    with open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8") as fh:
        fh.write(report(cases))


def main() -> None:
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(here, "data", "cases.json"))
    ap.add_argument("--out", default=os.path.join(here, "results"))
    args = ap.parse_args()
    cases = load_cases(args.cases)
    write_outputs(cases, args.out)
    print(report(cases))


if __name__ == "__main__":
    main()
