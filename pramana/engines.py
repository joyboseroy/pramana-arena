"""Executable models of inference validity in several Indian traditions.

Each engine takes a Case and returns a Verdict. These are deliberately small,
auditable formalisations of the schools' *criteria*, not of everything they say.
Where a school's treatment is disputed among scholars, the engine says so in
Verdict.why. Treat every rule here as a hypothesis to be checked against the
primary texts and the secondary literature (see SOURCES.md).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from .model import Case, Verdict

# Dignaga's nine-fold wheel of reasons (hetu-cakra), keyed by
# (presence of hetu in sapaksa, presence of hetu in vipaksa).
# Numbering follows the usual presentation; verify against Hattori and Katsura.
WHEEL: Dict[tuple, tuple] = {
    ("all", "all"): (1, "uncertain"),
    ("all", "none"): (2, "valid"),
    ("all", "some"): (3, "uncertain"),
    ("none", "all"): (4, "contradictory"),
    ("none", "none"): (5, "uncertain"),   # asadharana: too specific, e.g. audibility
    ("none", "some"): (6, "contradictory"),
    ("some", "all"): (7, "uncertain"),
    ("some", "none"): (8, "valid"),
    ("some", "some"): (9, "uncertain"),
}


def _basic_failures(c: Case, name: str):
    """Fallacies shared by the Buddhist engines."""
    if not c.hetu_established or not c.pakshadharmata:
        return Verdict(False, "asiddha", ["reason not established in the subject (fails pakshadharmata)"])
    if c.contradicted:
        return Verdict(False, "pakshabhasa", ["thesis contradicted by another pramana"])
    return None


def dignaga(c: Case) -> Verdict:
    """Dignaga: trairupya (three characteristics) read through the nine-fold wheel."""
    early = _basic_failures(c, "dignaga")
    if early:
        return early
    if c.sapaksa == "no_instances" or c.vipaksa == "no_instances":
        return Verdict(None, "outside the wheel",
                       ["the wheel presupposes instances in both sapaksa and vipaksa"])
    n, kind = WHEEL[(c.sapaksa, c.vipaksa)]
    if kind != "valid":
        return Verdict(False, f"hetu-cakra case {n}: {kind}", [f"sapaksa={c.sapaksa}, vipaksa={c.vipaksa}"])
    if c.counter_reason:
        return Verdict(False, "viruddhavyabhicarin (uncertain)", ["an equally strong opposing reason exists"])
    return Verdict(True, f"hetu-cakra case {n}: valid",
                   ["pakshadharmata, sapaksa-sattva and vipaksa-asattva all satisfied"])


def dharmakirti(c: Case) -> Verdict:
    """Dharmakirti: the reason must be tied to the probandum by identity or causation.

    Grounding: the need for an invariable connection is verified in Nagatomi 1957 (verse 300);
    the identity/causation split and the three reason types are not yet traced to PV 1.
    See docs/CITATIONS.md rows 3, 6, 7.
    """
    early = _basic_failures(c, "dharmakirti")
    if early:
        return early
    if c.counter_reason:
        return Verdict(False, "inconsistent case data",
                       ["Dharmakirti is generally read as denying that two valid reasons can conflict, so one must fail (unverified, see docs/CITATIONS.md row 9)"])
    if c.hetu_kind == "anupalabdhi":
        if c.perceptible_if_present:
            return Verdict(True, "anupalabdhi hetu", ["the object would be perceived if present, and is not"])
        return Verdict(False, "anupalabdhi hetu fails", ["the object would not be perceivable even if present"])
    if c.vipaksa in ("all", "some"):
        return Verdict(False, "vipaksa-asattva fails", [f"vipaksa={c.vipaksa}"])
    if c.hetu_kind == "svabhava" and c.relation == "tadatmya":
        return Verdict(True, "svabhava hetu", ["connection by identity (tadatmya)"])
    if c.hetu_kind == "karya" and c.relation == "tadutpatti":
        return Verdict(True, "karya hetu", ["connection by causation (tadutpatti)"])
    return Verdict(False, "no pratibandha",
                   ["no necessary connection by identity or causation, so the trairupya is only a coincidence"])


def nyaya(c: Case) -> Verdict:
    """Classical Nyaya: five characteristics (pancarupya) and five hetvabhasa."""
    if c.hetu_kind == "anupalabdhi":
        return Verdict(None, "outside anumana",
                       ["Nyaya treats absence as cognised by perception (abhava), not by inference"])
    if not c.hetu_established or not c.pakshadharmata:
        return Verdict(False, "asiddha", ["reason not established in the subject"])
    if c.contradicted:
        return Verdict(False, "badhita", ["thesis contradicted by another pramana"])
    if c.counter_reason:
        return Verdict(False, "satpratipaksa", ["an equally strong opposing reason neutralises it"])
    sap, vip = c.sapaksa, c.vipaksa
    if vip in ("all", "some"):
        if sap == "none" and vip == "all":
            return Verdict(False, "viruddha", ["the reason pervades the absence of the probandum"])
        return Verdict(False, "anaikantika (savyabhicara)", [f"reason occurs in vipaksa ({vip})"])
    # vipaksa is none or has no instances: no counterexample
    if sap in ("all", "some"):
        kind = "anvaya-vyatireki" if vip == "none" else "kevalanvayi"
        return Verdict(True, f"valid ({kind})", ["all five characteristics satisfied"])
    if sap == "none":
        return Verdict(False, "anaikantika (asadharana)", ["reason is absent from every sapaksa"])
    if sap == "no_instances" and vip == "none":
        return Verdict(True, "valid (kevalavyatireki)", ["negative concomitance only, accepted by Nyaya"])
    return Verdict(False, "ungrounded", ["no instances of either kind"])


def navya_nyaya(c: Case) -> Verdict:
    """Navya-Nyaya: classical Nyaya plus the upadhi test on vyapti."""
    base = nyaya(c)
    if base.valid is None:
        return base
    if base.valid and c.upadhi:
        return Verdict(False, "sopadhika (vyapti fails)",
                       ["a hidden conditioning factor (upadhi) separates the reason from the probandum"])
    if (not base.valid) and c.upadhi:
        base.why.append("diagnosis: the failure is due to an upadhi")
    return base


def jain(c: Case) -> Verdict:
    """Jain: a single characteristic, anyathanupapannatva, ascertained by tarka."""
    if not c.hetu_established:
        return Verdict(False, "asiddha", ["reason not established"])
    if c.contradicted:
        return Verdict(False, "akincitkara", ["thesis contradicted by another pramana"])
    if c.necessary_connection is None:
        return Verdict(None, "unannotated", ["necessary_connection not annotated for this case"])
    if c.necessary_connection:
        why = ["the reason cannot be otherwise than with the probandum"]
        if not c.pakshadharmata:
            why.append("valid despite lacking pakshadharmata: the three characteristics are not required")
        return Verdict(True, "anyathanupapanna", why)
    return Verdict(False, "no anyathanupapatti", ["no necessary connection, whatever the three characteristics show"])


def carvaka(c: Case) -> Verdict:
    """Carvaka: perception only; inference is not a pramana."""
    return Verdict(False, "anumana not a pramana",
                   ["vyapti cannot be established, since not all instances can be perceived"])


@dataclass
class Engine:
    key: str
    label: str
    ontology: str      # which school's ontology overrides apply in native mode
    fn: Callable[[Case], Verdict]
    baseline: bool = False   # baselines are reported but ignored when flagging divergence


ENGINES: Dict[str, Engine] = {
    e.key: e for e in [
        Engine("dignaga", "Dignaga", "buddhist", dignaga),
        Engine("dharmakirti", "Dharmakirti", "buddhist", dharmakirti),
        Engine("nyaya", "Nyaya", "nyaya", nyaya),
        Engine("navya_nyaya", "Navya-Nyaya", "nyaya", navya_nyaya),
        Engine("jain", "Jain", "jain", jain),
        Engine("carvaka", "Carvaka (baseline)", "carvaka", carvaka, baseline=True),
    ]
}
