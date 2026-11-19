import json
import unittest

from nyaya_rag.extract import ExtractionError, Passage, parse_json
from nyaya_rag.llm import ScriptedLLM
from nyaya_rag.pipeline import render, run

P1 = Passage("P1", "Device registry entry: device_7 is classified as category cat_9.", "device registry", 2, "pratyaksa")
P2 = Passage("P2", "Release 17 specification: every category cat_9 device supports carrier aggregation.", "spec Rel-17", 2)
P3 = Passage("P3", "Test log: d1 cat_9 supports CA; d2 cat_9 supports CA; d3 cat_4 does not.", "lab test log", 1, "pratyaksa")
PASSAGES = [P1, P2, P3]
Q = "Does device_7 support carrier aggregation?"

EX1 = json.dumps({"claims": [{"subject": "device_7", "predicate": "category", "value": "cat_9"}]})
EX2 = json.dumps({"rules": [{"if": {"predicate": "category", "value": "cat_9"},
                             "then": {"predicate": "carrier_aggregation", "value": "yes"},
                             "conditions": {"release": "Rel-17"}, "relation": "none"}]})
EX3 = "Here you go:\n```json\n" + json.dumps({"instances": [
    {"id": "d1", "attrs": {"category": "cat_9", "carrier_aggregation": "yes"}},
    {"id": "d2", "attrs": {"category": "cat_9", "carrier_aggregation": "yes"}},
    {"id": "d3", "attrs": {"category": "cat_4", "carrier_aggregation": "no"}}]}) + "\n```"
GOOD_ARG = json.dumps({
    "pratijna": {"subject": "device_7", "predicate": "carrier_aggregation", "value": "yes"},
    "hetu": {"subject": "device_7", "predicate": "category", "value": "cat_9"},
    "rule_evidence_id": "P2", "hetu_evidence_ids": ["P1"],
    "answer_text": "Yes, device_7 supports carrier aggregation."})


def script(arg=GOOD_ARG, repair='{"abstain": true}'):
    return ScriptedLLM([
        ("TASK: REPAIR", repair),
        ("TASK: ARGUE", arg),
        ("classified as category cat_9", EX1),
        ("every category cat_9 device", EX2),
        ("Test log", EX3),
    ])


class TestParse(unittest.TestCase):
    def test_fenced_json_with_chatter(self):
        self.assertIn("instances", parse_json(EX3))

    def test_no_json_raises(self):
        with self.assertRaises(ExtractionError):
            parse_json("sorry, I cannot")

    def test_bad_json_raises(self):
        with self.assertRaises(ExtractionError):
            parse_json("{not json}")


class TestPipeline(unittest.TestCase):
    def test_accepts_grounded_answer(self):
        r = run(Q, PASSAGES, {"release": "Rel-17"}, script(), "navya_nyaya")
        self.assertEqual(r.status, "accept")
        self.assertIn("Application (upanaya)", render(r))
        self.assertIn("pratyaksa", render(r))

    def test_hidden_condition_splits_regimes(self):
        ctx = {"release": "Rel-15"}
        self.assertEqual(run(Q, PASSAGES, ctx, script(), "nyaya").status, "accept")
        r = run(Q, PASSAGES, ctx, script(), "navya_nyaya")
        self.assertEqual(r.status, "abstain")          # repair step returns abstain
        self.assertTrue(r.label.startswith("sopadhika"))

    def test_hallucinated_evidence_id_rejected(self):
        bad = json.dumps(json.loads(GOOD_ARG) | {"hetu_evidence_ids": ["P9"]})
        r = run(Q, PASSAGES, {"release": "Rel-17"}, script(arg=bad, repair=bad), "nyaya")
        self.assertEqual(r.status, "reject")
        self.assertEqual(r.label, "asiddha")

    def test_repair_can_recover(self):
        bad = json.dumps(json.loads(GOOD_ARG) | {"hetu_evidence_ids": ["P9"]})
        r = run(Q, PASSAGES, {"release": "Rel-17"}, script(arg=bad, repair=GOOD_ARG), "nyaya")
        self.assertEqual(r.status, "accept")
        self.assertEqual(r.attempts, 2)

    def test_malformed_extraction_skips_passage(self):
        llm = ScriptedLLM([
            ("TASK: ARGUE", '{"abstain": true}'),
            ("classified as category cat_9", "not json at all"),
            ("every category cat_9 device", EX2),
            ("Test log", EX3),
        ])
        r = run(Q, PASSAGES, {"release": "Rel-17"}, llm, "nyaya")
        self.assertEqual(r.skipped, ["P1"])
        self.assertEqual(r.status, "abstain")

    def test_malformed_argument_abstains(self):
        r = run(Q, PASSAGES, {"release": "Rel-17"}, script(arg='{"pratijna": 3}'), "nyaya")
        self.assertEqual(r.status, "abstain")
        self.assertEqual(r.label, "malformed argument")


if __name__ == "__main__":
    unittest.main()
