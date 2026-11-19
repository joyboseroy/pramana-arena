import os
import unittest

from pramana.engines import ENGINES, WHEEL
from pramana.model import Case, load_cases

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = {c.id: c for c in load_cases(os.path.join(HERE, "data", "cases.json"))}


def verdict(engine, case_id, native=False):
    c = CASES[case_id]
    if native:
        c = c.as_seen_by(ENGINES[engine].ontology)
    return ENGINES[engine].fn(c).valid


class TestWheel(unittest.TestCase):
    def test_nine_cells_and_two_valid(self):
        self.assertEqual(len(WHEEL), 9)
        valid = [n for n, kind in WHEEL.values() if kind == "valid"]
        self.assertEqual(sorted(valid), [2, 8])
        contradictory = [n for n, kind in WHEEL.values() if kind == "contradictory"]
        self.assertEqual(sorted(contradictory), [4, 6])


class TestCanonicalCases(unittest.TestCase):
    def test_smoke_fire_valid_everywhere_except_carvaka(self):
        for k in ("dignaga", "dharmakirti", "nyaya", "navya_nyaya", "jain"):
            self.assertTrue(verdict(k, "smoke-fire"), k)
        self.assertFalse(verdict("carvaka", "smoke-fire"))

    def test_fallacies_rejected_by_all_inferential_schools(self):
        for cid in ("audible-eternal", "knowable-impermanent", "produced-eternal", "fire-cold"):
            for k in ("dignaga", "dharmakirti", "nyaya", "navya_nyaya", "jain"):
                self.assertFalse(verdict(k, cid), f"{cid}/{k}")

    def test_tatputratva_splits_the_schools(self):
        self.assertTrue(verdict("dignaga", "tatputratva"))
        self.assertTrue(verdict("nyaya", "tatputratva"))
        self.assertFalse(verdict("dharmakirti", "tatputratva"))
        self.assertFalse(verdict("navya_nyaya", "tatputratva"))
        self.assertFalse(verdict("jain", "tatputratva"))

    def test_pakshadharmata_not_needed_in_jain(self):
        self.assertFalse(verdict("dignaga", "krttika-rohini"))
        self.assertFalse(verdict("nyaya", "krttika-rohini"))
        self.assertTrue(verdict("jain", "krttika-rohini"))

    def test_kevalanvayi_and_kevalavyatireki(self):
        self.assertTrue(verdict("nyaya", "knowable-nameable"))
        self.assertIsNone(verdict("dignaga", "knowable-nameable"))
        self.assertTrue(verdict("nyaya", "earth-smell"))
        self.assertIsNone(verdict("dignaga", "earth-smell"))

    def test_anupalabdhi(self):
        self.assertTrue(verdict("dharmakirti", "no-pot"))
        self.assertIsNone(verdict("nyaya", "no-pot"))


class TestOntology(unittest.TestCase):
    def test_existence_momentary_flips_with_ontology(self):
        self.assertTrue(verdict("dharmakirti", "existence-momentary"))
        self.assertTrue(verdict("nyaya", "existence-momentary", native=False))
        self.assertFalse(verdict("nyaya", "existence-momentary", native=True))
        self.assertFalse(verdict("jain", "existence-momentary", native=True))


class TestSatpratipaksa(unittest.TestCase):
    def test_counter_reason_blocks_nyaya_and_buddhist(self):
        base = CASES["produced-impermanent"]
        c = Case(**{**base.__dict__, "counter_reason": True})
        self.assertFalse(ENGINES["nyaya"].fn(c).valid)
        self.assertFalse(ENGINES["dignaga"].fn(c).valid)
        self.assertFalse(ENGINES["dharmakirti"].fn(c).valid)


if __name__ == "__main__":
    unittest.main()
