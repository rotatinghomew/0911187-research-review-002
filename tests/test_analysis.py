import unittest

from research_review.analysis import summarize
from research_review.reports import build_report


class ResearchReviewTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "e1", "week": "2026-W40", "student": "s1", "question": "窗口影响", "claim": "两次测量不同", "evidence": "run-1", "status": "observed", "value": 5},
            {"id": "e2", "week": "2026-W40", "student": "s1", "question": "窗口影响", "claim": "可能与预热有关", "evidence": "note-1", "status": "interpreted"},
            {"id": "e3", "week": "2026-W41", "student": "s1", "question": "窗口影响", "claim": "换批次复测", "evidence": "", "status": "to_verify"},
        ]

    def test_timeline_keeps_claims_separate_by_evidence_status(self):
        thread = summarize(self.records)["s1:窗口影响"]
        self.assertEqual(len(thread["observations"]), 1)
        self.assertEqual(len(thread["interpretations"]), 1)
        self.assertEqual(len(thread["to_verify"]), 1)
        self.assertTrue(thread["has_new_observation"])

    def test_report_flags_unlinked_plan_without_counting_it_as_observation(self):
        report = build_report(self.records, source_revision="r3")
        self.assertEqual(report["source_revision"], "r3")
        self.assertEqual(report["unlinked_records"], ["e3"])
        self.assertEqual(len(report["questions"]["s1:窗口影响"]["observations"]), 1)

    def test_repeated_record_identity_is_rejected(self):
        from research_review.facts import load_records
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile("w", encoding="utf-8") as handle:
            import json
            json.dump([self.records[0], self.records[0]], handle)
            handle.flush()
            with self.assertRaisesRegex(ValueError, "重复记录"):
                load_records(handle.name)


if __name__ == "__main__":
    unittest.main()
