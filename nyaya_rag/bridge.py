"""Turn a RAG argument into a pramana-arena Case and judge it under a chosen regime.

The regimes are the engines from pramana/engines.py. Swapping the regime changes
how strict the checker is, which is the experimental handle of the project:
  nyaya         five characteristics and five fallacies
  navya_nyaya   plus the upadhi test (a hidden condition on the rule)
  dharmakirti   requires a connection by identity or causation
  dignaga       trairupya via the nine-fold wheel
  jain          necessary connection only
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from pramana.engines import ENGINES
from pramana.model import Case, Verdict

from .schema import Argument, Claim, Corpus, Instance


def _presence(instances: List[Instance], pred: str, val: str) -> str:
    if not instances:
        return "no_instances"
    n = sum(1 for i in instances if i.attrs.get(pred) == val)
    return "all" if n == len(instances) else ("none" if n == 0 else "some")


def build_case(arg: Argument, corpus: Corpus, context: Dict[str, str]) -> Case:
    ev = {e.id: e for e in corpus.evidence}
    cited = list(arg.hetu_evidence_ids) + [arg.rule_evidence_id]
    missing = [i for i in cited if i not in ev]

    hetu_supported = (not missing) and any(
        arg.hetu in ev[i].claims for i in arg.hetu_evidence_ids
    )
    rule_ev = ev.get(arg.rule_evidence_id)
    rule = None
    if rule_ev:
        rule = next(
            (r for r in rule_ev.rules
             if r.if_claim == (arg.hetu.predicate, arg.hetu.value)
             and r.then_claim == (arg.pratijna.predicate, arg.pratijna.value)),
            None,
        )

    support_rank = max((ev[i].rank for i in cited if i in ev), default=0)
    contradicted = counter = False
    for e in corpus.evidence:
        for c in e.claims:
            if (c.subject == arg.pratijna.subject and c.predicate == arg.pratijna.predicate
                    and c.value != arg.pratijna.value):
                if e.rank > support_rank:
                    contradicted = True
                elif e.rank == support_rank:
                    counter = True

    upadhi = bool(rule) and any(context.get(k) != v for k, v in rule.conditions.items())

    sadhya_p, sadhya_v = arg.pratijna.predicate, arg.pratijna.value
    sap = [i for i in corpus.instances if i.attrs.get(sadhya_p) == sadhya_v]
    vip = [i for i in corpus.instances if sadhya_p in i.attrs and i.attrs[sadhya_p] != sadhya_v]
    sap_pres = _presence(sap, arg.hetu.predicate, arg.hetu.value)
    vip_pres = _presence(vip, arg.hetu.predicate, arg.hetu.value)

    relation = rule.relation if rule else "none"
    kind = {"tadutpatti": "karya", "tadatmya": "svabhava"}.get(relation, "other")
    # A conflicting equal-rank source also undermines any claim that the connection is necessary.
    necessary = bool(rule) and vip_pres in ("none", "no_instances") and not upadhi and not counter

    return Case(
        id="rag-argument",
        title=f"{arg.pratijna.subject}: {arg.pratijna.predicate}={arg.pratijna.value}",
        thesis=f"{arg.pratijna.subject} {arg.pratijna.predicate} = {arg.pratijna.value}",
        reason=f"because {arg.hetu.predicate} = {arg.hetu.value}",
        pakshadharmata=hetu_supported and arg.hetu.subject == arg.pratijna.subject,
        hetu_established=hetu_supported,
        sapaksa=sap_pres,
        vipaksa=vip_pres,
        hetu_kind=kind,
        relation=relation,
        contradicted=contradicted,
        counter_reason=counter,
        upadhi=upadhi,
        necessary_connection=necessary,
        notes="; ".join(f"missing evidence {m}" for m in missing),
    )


@dataclass
class CheckResult:
    regime: str
    verdict: Verdict
    case: Case


def check(arg: Argument, corpus: Corpus, context: Optional[Dict[str, str]] = None,
          regime: str = "nyaya") -> CheckResult:
    case = build_case(arg, corpus, context or {})
    return CheckResult(regime, ENGINES[regime].fn(case), case)
