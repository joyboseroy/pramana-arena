"""Synthetic demo. Every name and fact below is invented for illustration.

Run: python -m nyaya_rag.demo
"""
from __future__ import annotations

import copy

from .bridge import check
from .schema import Argument, Claim, Corpus, Evidence, Instance, Rule

REGIMES = ["nyaya", "navya_nyaya", "dignaga", "dharmakirti", "jain"]


def toy_corpus(relation: str = "none") -> Corpus:
    rule = Rule(("category", "cat_9"), ("carrier_aggregation", "yes"),
                conditions={"release": "Rel-17"}, relation=relation)
    return Corpus(
        evidence=[
            Evidence("E1", "Registry: device_7 is category cat_9.", "pratyaksa", "device registry", 2,
                     claims=[Claim("device_7", "category", "cat_9")]),
            Evidence("E3", "Rel-17 spec: cat_9 devices support carrier aggregation.", "sabda", "spec Rel-17", 2,
                     rules=[rule]),
        ],
        instances=[
            Instance("d1", {"category": "cat_9", "carrier_aggregation": "yes"}),
            Instance("d2", {"category": "cat_9", "carrier_aggregation": "yes"}),
            Instance("d3", {"category": "cat_4", "carrier_aggregation": "no"}),
        ],
    )


ARG = Argument(
    pratijna=Claim("device_7", "carrier_aggregation", "yes"),
    hetu=Claim("device_7", "category", "cat_9"),
    rule_evidence_id="E3",
    hetu_evidence_ids=["E1"],
)


def scenarios():
    """Return (name, corpus, argument, context) tuples, one per failure mode."""
    ctx = {"release": "Rel-17"}
    out = [("grounded answer", toy_corpus(), ARG, ctx)]
    out.append(("upadhi: rule needs Rel-17, query is Rel-15", toy_corpus(), ARG, {"release": "Rel-15"}))

    c = toy_corpus()
    c.instances.append(Instance("d4", {"category": "cat_9", "carrier_aggregation": "no"}))
    out.append(("counterexample in the corpus", c, ARG, ctx))

    c = toy_corpus()
    c.evidence.append(Evidence("E5", "Operator override: device_7 has no CA.", "sabda", "operator note", 3,
                               claims=[Claim("device_7", "carrier_aggregation", "no")]))
    out.append(("higher-ranked source contradicts", c, ARG, ctx))

    c = toy_corpus()
    c.evidence.append(Evidence("E6", "Forum post: device_7 has no CA.", "sabda", "forum", 2,
                               claims=[Claim("device_7", "carrier_aggregation", "no")]))
    out.append(("equal-rank source conflicts", c, ARG, ctx))

    bad = copy.deepcopy(ARG)
    bad.hetu_evidence_ids = ["E9"]
    out.append(("cited evidence does not exist", toy_corpus(), bad, ctx))
    return out


def main() -> None:
    print("| Scenario | " + " | ".join(REGIMES) + " |")
    print("|" + "---|" * (len(REGIMES) + 1))
    for name, corpus, arg, ctx in scenarios():
        cells = []
        for r in REGIMES:
            v = check(arg, corpus, ctx, r).verdict
            cells.append({True: "accept", False: "reject", None: "abstain"}[v.valid])
        print(f"| {name} | " + " | ".join(cells) + " |")
    print("\nDetail for the upadhi scenario under navya_nyaya:")
    _, corpus, arg, ctx = scenarios()[1]
    v = check(arg, corpus, ctx, "navya_nyaya").verdict
    print(f"  {v.label}: {'; '.join(v.why)}")


if __name__ == "__main__":
    main()
