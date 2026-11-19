"""Typed evidence and five-member arguments.

This scaffold works on *structured* claims. In a full system an LLM or an
extraction model would turn retrieved text into Claim, Rule and Instance
records. That extraction step is not implemented here; the point of this
module is the checking layer that sits after it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

PRAMANA = ("pratyaksa", "sabda", "anumana", "upamana")
# pratyaksa: observed directly (tool output, database value, executed query)
# sabda:     testimony (a retrieved document, statute, specification)
# anumana:   derived from other evidence by a rule
# upamana:   by analogy to a similar retrieved case


@dataclass(frozen=True)
class Claim:
    subject: str
    predicate: str
    value: str


@dataclass
class Rule:
    """A general statement: whenever if_claim holds of a subject, then_claim holds of it."""
    if_claim: Tuple[str, str]       # (predicate, value)
    then_claim: Tuple[str, str]
    conditions: Dict[str, str] = field(default_factory=dict)  # context needed, e.g. {"release": "Rel-17"}
    relation: str = "none"          # tadatmya | tadutpatti | none (only if the source says so)


@dataclass
class Evidence:
    id: str
    text: str
    pramana: str
    source: str
    rank: int                       # authority: a higher rank overrides a lower one
    claims: List[Claim] = field(default_factory=list)
    rules: List[Rule] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert self.pramana in PRAMANA, f"{self.id}: bad pramana {self.pramana}"


@dataclass
class Instance:
    """An observed individual, used to look for supporting and opposing examples."""
    id: str
    attrs: Dict[str, str]


@dataclass
class Corpus:
    evidence: List[Evidence]
    instances: List[Instance] = field(default_factory=list)


@dataclass
class Argument:
    """Five-member argument in compact form.

    pratijna   the claim to be established
    hetu       the reason, a claim about the same subject
    udaharana  rule_evidence_id points to the general rule with its example base
    upanaya    hetu_evidence_ids point to the evidence that the reason holds here
    nigamana   the conclusion, which restates the pratijna
    """
    pratijna: Claim
    hetu: Claim
    rule_evidence_id: str
    hetu_evidence_ids: List[str]
