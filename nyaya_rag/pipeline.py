"""End-to-end flow: passages -> typed evidence -> five-member argument -> fallacy check -> repair or abstain."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from pramana.model import Verdict

from .bridge import check
from .extract import ExtractionError, Passage, extract, parse_json
from .llm import LLM
from .schema import Argument, Claim, Corpus, Evidence, Instance

ARGUE_PROMPT = """TASK: ARGUE
Answer the question as a five-member argument built ONLY from the evidence listed below.
If no argument can be built from this evidence, return {"abstain": true}.

Question: <<QUESTION>>

Evidence (id, source, type, claims, rules):
<<EVIDENCE>>

Return one JSON object and nothing else:
  "pratijna": {"subject": str, "predicate": str, "value": str}     the claim that answers the question
  "hetu":     {"subject": str, "predicate": str, "value": str}     the reason, about the same subject
  "rule_evidence_id": str                                          id of the evidence holding the general rule that links hetu to pratijna
  "hetu_evidence_ids": [str]                                       ids of the evidence showing the reason holds for this subject
  "answer_text": str                                               one or two sentences for the user
Use only ids, predicates and values that appear in the evidence.
"""

REPAIR_PROMPT = """TASK: REPAIR
Your argument was rejected by a checker.
Question: <<QUESTION>>
Rejected argument: <<ARGUMENT>>
Fallacy found: <<LABEL>>
Reason: <<WHY>>

Evidence (id, source, type, claims, rules):
<<EVIDENCE>>

If a different argument from this evidence avoids the fallacy, return it in the same JSON format as before.
If not, return {"abstain": true}. Do not repeat the rejected argument.
"""


@dataclass
class RunResult:
    status: str                       # accept | reject | abstain
    label: str = ""
    why: List[str] = field(default_factory=list)
    argument: Optional[Argument] = None
    answer_text: str = ""
    evidence: List[Evidence] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)   # passage ids whose extraction failed
    attempts: int = 0


def _describe(evidence: List[Evidence]) -> str:
    lines = []
    for e in evidence:
        claims = "; ".join(f"{c.subject} {c.predicate}={c.value}" for c in e.claims) or "-"
        rules = "; ".join(
            f"if {r.if_claim[0]}={r.if_claim[1]} then {r.then_claim[0]}={r.then_claim[1]}"
            + (f" (only when {r.conditions})" if r.conditions else "")
            for r in e.rules) or "-"
        lines.append(f"[{e.id}] source={e.source} type={e.pramana} claims: {claims} | rules: {rules}")
    return "\n".join(lines)


def _argument_from(obj: dict) -> Argument:
    try:
        return Argument(
            pratijna=Claim(**{k: str(obj["pratijna"][k]) for k in ("subject", "predicate", "value")}),
            hetu=Claim(**{k: str(obj["hetu"][k]) for k in ("subject", "predicate", "value")}),
            rule_evidence_id=str(obj["rule_evidence_id"]),
            hetu_evidence_ids=[str(x) for x in obj["hetu_evidence_ids"]],
        )
    except (KeyError, TypeError) as exc:
        raise ExtractionError(f"malformed argument: {exc}") from exc


def _draft(prompt: str, llm: LLM):
    obj = parse_json(llm(prompt))
    if obj.get("abstain"):
        return None, ""
    return _argument_from(obj), str(obj.get("answer_text", ""))


def run(question: str, passages: List[Passage], context: Dict[str, str], llm: LLM,
        regime: str = "navya_nyaya", max_repairs: int = 1) -> RunResult:
    vocab: Set[str] = set()
    evidence: List[Evidence] = []
    instances: List[Instance] = []
    skipped: List[str] = []
    for p in passages:
        try:
            ev, inst = extract(p, question, vocab, llm)
        except ExtractionError:
            skipped.append(p.id)
            continue
        evidence.append(ev)
        instances.extend(inst)
    corpus = Corpus(evidence, instances)
    described = _describe(evidence)

    base = ARGUE_PROMPT.replace("<<QUESTION>>", question).replace("<<EVIDENCE>>", described)
    try:
        arg, text = _draft(base, llm)
    except ExtractionError as exc:
        return RunResult("abstain", "malformed argument", [str(exc)], evidence=evidence, skipped=skipped)
    if arg is None:
        return RunResult("abstain", "no argument from evidence", evidence=evidence, skipped=skipped)

    attempts = 0
    while True:
        attempts += 1
        verdict: Verdict = check(arg, corpus, context, regime).verdict
        if verdict.valid is True:
            return RunResult("accept", verdict.label, verdict.why, arg, text, evidence, skipped, attempts)
        if verdict.valid is None:
            return RunResult("abstain", verdict.label, verdict.why, arg, text, evidence, skipped, attempts)
        if attempts > max_repairs:
            return RunResult("reject", verdict.label, verdict.why, arg, text, evidence, skipped, attempts)
        prompt = (REPAIR_PROMPT.replace("<<QUESTION>>", question)
                  .replace("<<ARGUMENT>>", f"{arg.pratijna} because {arg.hetu}, rule in {arg.rule_evidence_id}")
                  .replace("<<LABEL>>", verdict.label)
                  .replace("<<WHY>>", "; ".join(verdict.why))
                  .replace("<<EVIDENCE>>", described))
        try:
            new_arg, new_text = _draft(prompt, llm)
        except ExtractionError:
            new_arg = None
        if new_arg is None:
            return RunResult("abstain", verdict.label, verdict.why, arg, text, evidence, skipped, attempts)
        arg, text = new_arg, new_text


def render(result: RunResult) -> str:
    """Human-readable five-member rendering with evidence types, or the reason for no answer."""
    if result.argument is None or result.status != "accept":
        return f"No answer given ({result.status}: {result.label}). " + " ".join(result.why)
    a = result.argument
    ev = {e.id: e for e in result.evidence}
    rule_ev = ev[a.rule_evidence_id]
    hetu_src = ", ".join(f"{i} ({ev[i].pramana}, {ev[i].source})" for i in a.hetu_evidence_ids)
    return "\n".join([
        f"Claim (pratijna): {a.pratijna.subject} {a.pratijna.predicate} = {a.pratijna.value}",
        f"Reason (hetu): {a.hetu.subject} {a.hetu.predicate} = {a.hetu.value}",
        f"Rule (udaharana): {a.rule_evidence_id} ({rule_ev.pramana}, {rule_ev.source})",
        f"Application (upanaya): the reason holds here, shown by {hetu_src}",
        f"Conclusion (nigamana): {a.pratijna.subject} {a.pratijna.predicate} = {a.pratijna.value}",
        f"Checked under: {result.label}",
    ])
