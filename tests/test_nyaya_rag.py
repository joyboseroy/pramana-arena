import unittest

from nyaya_rag.bridge import check
from nyaya_rag.demo import ARG, scenarios, toy_corpus


def verdicts(index, regime):
    name, corpus, arg, ctx = scenarios()[index]
    return check(arg, corpus, ctx, regime).verdict


class TestNyayaRag(unittest.TestCase):
    def test_grounded_answer_accepted_by_nyaya_and_jain(self):
        self.assertTrue(verdicts(0, "nyaya").valid)
        self.assertTrue(verdicts(0, "navya_nyaya").valid)
        self.assertTrue(verdicts(0, "jain").valid)

    def test_dharmakirti_rejects_without_stated_relation(self):
        self.assertFalse(verdicts(0, "dharmakirti").valid)

    def test_dharmakirti_accepts_when_source_states_causal_relation(self):
        c = toy_corpus(relation="tadutpatti")
        # hetu_kind becomes karya, so Dharmakirti's engine can accept it
        self.assertTrue(check(ARG, c, {"release": "Rel-17"}, "dharmakirti").verdict.valid)

    def test_upadhi_split(self):
        self.assertTrue(verdicts(1, "nyaya").valid)
        self.assertFalse(verdicts(1, "navya_nyaya").valid)
        self.assertFalse(verdicts(1, "jain").valid)

    def test_counterexample_rejected_everywhere(self):
        for r in ("nyaya", "navya_nyaya", "dignaga", "dharmakirti", "jain"):
            self.assertFalse(verdicts(2, r).valid, r)

    def test_higher_rank_contradiction_is_badhita(self):
        self.assertEqual(verdicts(3, "nyaya").label, "badhita")

    def test_equal_rank_conflict_is_satpratipaksa(self):
        self.assertEqual(verdicts(4, "nyaya").label, "satpratipaksa")
        for r in ("nyaya", "navya_nyaya", "dignaga", "dharmakirti", "jain"):
            self.assertFalse(verdicts(4, r).valid, r)

    def test_missing_evidence_is_asiddha(self):
        self.assertEqual(verdicts(5, "nyaya").label, "asiddha")


if __name__ == "__main__":
    unittest.main()
