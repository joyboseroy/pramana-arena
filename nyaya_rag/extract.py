"""Turn a retrieved passage into typed Evidence by asking an LLM for structured claims.

The prompt asks for what the passage states and nothing more. Everything the model
returns is validated before it is used, and a malformed response raises
ExtractionError so the pipeline can skip that passage instead of crashing.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from .llm import LLM
from .schema import Claim, Evidence, Instance, Rule

RELATIONS = ("none", "tadatmya", "tadutpatti")


class ExtractionError(ValueError):
    pass


@dataclass
class Passage:
    id: str
    text: str
    source: str
    rank: int                    # authority of this source; higher overrides lower
    pramana: str = "sabda"       # sabda for documents; pratyaksa for tool or database output


EXTRACT_PROMPT = """TASK: EXTRACT
You convert one passage into structured records. Use only what the passage explicitly states.
Do not infer, generalise, or add outside knowledge.

Question being investigated: <<QUESTION>>

Vocabulary already in use (reuse these predicate names when they mean the same thing):
<<VOCAB>>

Return one JSON object and nothing else, with these keys:
  "claims":    list of {"subject": str, "predicate": str, "value": str}
              a fact the passage asserts about one named thing
  "rules":     list of {"if": {"predicate": str, "value": str},
                        "then": {"predicate": str, "value": str},
                        "conditions": {str: str},
                        "relation": "none" | "tadatmya" | "tadutpatti"}
              a general statement that applies to any subject.
              "conditions" holds scope the passage states (a release, a jurisdiction, a date); use {} if none.
              "relation" is "none" unless the passage itself says the link is by identity (tadatmya) or by cause (tadutpatti).
  "instances": list of {"id": str, "attrs": {str: str}}
              individual cases the passage describes, with their attributes

Use lowercase snake_case for subjects and predicates. Use empty lists when nothing applies.

PASSAGE (source: <<SOURCE>>):
<<TEXT>>
"""


def parse_json(text: str) -> dict:
    """Parse the first JSON object in a model response, tolerating code fences and chatter."""
    cleaned = re.sub(r"```(?:json)?", "", text)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end <= start:
        raise ExtractionError("no JSON object found in response")
    try:
        obj = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"invalid JSON: {exc}") from exc
    if not isinstance(obj, dict):
        raise ExtractionError("top-level JSON value is not an object")
    return obj


def _s(x) -> str:
    return str(x).strip()


def _pair(d, where: str) -> Tuple[str, str]:
    if not isinstance(d, dict) or "predicate" not in d or "value" not in d:
        raise ExtractionError(f"{where}: needs predicate and value")
    return _s(d["predicate"]), _s(d["value"])


def validate(obj: dict, passage: Passage) -> Tuple[Evidence, List[Instance]]:
    claims = []
    for c in obj.get("claims", []):
        if not isinstance(c, dict) or not {"subject", "predicate", "value"} <= set(c):
            raise ExtractionError("claim needs subject, predicate and value")
        claims.append(Claim(_s(c["subject"]), _s(c["predicate"]), _s(c["value"])))
    rules = []
    for r in obj.get("rules", []):
        if not isinstance(r, dict):
            raise ExtractionError("rule is not an object")
        cond = r.get("conditions", {}) or {}
        if not isinstance(cond, dict):
            raise ExtractionError("rule conditions must be an object")
        rel = _s(r.get("relation", "none"))
        rules.append(Rule(
            if_claim=_pair(r.get("if"), "rule.if"),
            then_claim=_pair(r.get("then"), "rule.then"),
            conditions={_s(k): _s(v) for k, v in cond.items()},
            relation=rel if rel in RELATIONS else "none",
        ))
    instances = []
    for i, inst in enumerate(obj.get("instances", [])):
        if not isinstance(inst, dict) or not isinstance(inst.get("attrs"), dict):
            raise ExtractionError("instance needs attrs")
        iid = _s(inst.get("id", i))
        instances.append(Instance(f"{passage.id}:{iid}", {_s(k): _s(v) for k, v in inst["attrs"].items()}))
    ev = Evidence(passage.id, passage.text, passage.pramana, passage.source, passage.rank,
                  claims=claims, rules=rules)
    return ev, instances


def extract(passage: Passage, question: str, vocab: Set[str], llm: LLM) -> Tuple[Evidence, List[Instance]]:
    prompt = (EXTRACT_PROMPT
              .replace("<<QUESTION>>", question)
              .replace("<<VOCAB>>", ", ".join(sorted(vocab)) or "(none yet)")
              .replace("<<SOURCE>>", passage.source)
              .replace("<<TEXT>>", passage.text))
    ev, instances = validate(parse_json(llm(prompt)), passage)
    for c in ev.claims:
        vocab.add(c.predicate)
    for r in ev.rules:
        vocab.update([r.if_claim[0], r.then_claim[0]])
    for inst in instances:
        vocab.update(inst.attrs)
    return ev, instances
