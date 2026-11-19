"""Compare schools by which pramanas they accept and how many debate-loss grounds they list.

Usage: python -m pramana.inventory
"""
from __future__ import annotations

import itertools
import json
import os


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 1.0


def main() -> None:
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(here, "data", "pramana_inventory.json"), encoding="utf-8") as fh:
        inv = {k: set(v) for k, v in json.load(fh).items() if not k.startswith("_")}
    names = list(inv)
    print("## Pramanas accepted\n")
    for n in names:
        print(f"- {n} ({len(inv[n])}): {', '.join(sorted(inv[n]))}")
    print("\n## Jaccard similarity of pramana sets\n")
    print("| | " + " | ".join(names) + " |")
    print("|" + "---|" * (len(names) + 1))
    for a in names:
        print(f"| {a} | " + " | ".join(f"{jaccard(inv[a], inv[b]):.2f}" for b in names) + " |")
    with open(os.path.join(here, "data", "debate_rules.json"), encoding="utf-8") as fh:
        rules = json.load(fh)
    print("\n## Debate-loss grounds\n")
    print(f"- Nyaya nigrahasthana: {len(rules['nyaya_nigrahasthana'])}")
    print(f"- Dharmakirti, Vadanyaya: {len(rules['dharmakirti_vadanyaya'])}")


if __name__ == "__main__":
    main()
