"""Data model: an inference case and a verdict.

A Case records only the structural facts about an inference that the
different schools disagree about how to weigh. It does not contain any
school's verdict. Verdicts are computed by the engines in engines.py.

Presence values for sapaksa / vipaksa:
  all           hetu is present in every instance
  some          hetu is present in some but not all instances
  none          instances exist, hetu is present in none of them
  no_instances  there are no instances of that kind at all
                (vipaksa no_instances = kevalanvayi inference,
                 sapaksa no_instances = kevalavyatireki inference)

sapaksa = instances where the probandum (sadhya) is present.
vipaksa = instances where the probandum is absent.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

PRESENCE = ("all", "some", "none", "no_instances")
HETU_KINDS = ("svabhava", "karya", "anupalabdhi", "other")
RELATIONS = ("tadatmya", "tadutpatti", "none")


@dataclass
class Case:
    id: str
    title: str
    thesis: str
    reason: str
    pakshadharmata: bool            # reason is present in the subject
    hetu_established: bool          # reason is itself accepted as real/established
    sapaksa: str
    vipaksa: str
    hetu_kind: str = "other"        # Dharmakirti's three: svabhava, karya, anupalabdhi
    relation: str = "none"          # tadatmya (identity) or tadutpatti (causation)
    perceptible_if_present: bool = False   # for anupalabdhi reasons
    contradicted: bool = False      # thesis contradicted by another pramana (badhita)
    counter_reason: bool = False    # an equally strong opposing reason (satpratipaksa)
    upadhi: bool = False            # a hidden conditioning factor (Navya-Nyaya)
    necessary_connection: Optional[bool] = None  # Jain anyathanupapannatva; None = unannotated
    ontology: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    confidence: str = "illustrative"
    notes: str = ""

    def __post_init__(self) -> None:
        assert self.sapaksa in PRESENCE, f"{self.id}: bad sapaksa {self.sapaksa}"
        assert self.vipaksa in PRESENCE, f"{self.id}: bad vipaksa {self.vipaksa}"
        assert self.hetu_kind in HETU_KINDS, f"{self.id}: bad hetu_kind"
        assert self.relation in RELATIONS, f"{self.id}: bad relation"

    def as_seen_by(self, ontology: Optional[str]) -> "Case":
        """Return a copy with that school's ontology-specific facts applied.

        The same inference can have different sapaksa/vipaksa facts depending
        on what each school thinks exists (for example, enduring substances).
        Separating ontology from logic is the point of the two comparison modes.
        """
        overrides = self.ontology.get(ontology or "", {})
        if not overrides:
            return self
        view = copy.deepcopy(self)
        for key, value in overrides.items():
            setattr(view, key, value)
        view.__post_init__()
        return view


@dataclass
class Verdict:
    valid: Optional[bool]           # True / False / None (engine abstains)
    label: str
    why: List[str] = field(default_factory=list)


def load_cases(path: str) -> List[Case]:
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)
    return [Case(**item) for item in raw]
