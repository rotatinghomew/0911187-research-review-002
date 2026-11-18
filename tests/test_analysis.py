import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from research_review.analysis import summarize
from research_review.metric_summary import summarize_cohort_metrics
from research_review.reports import build_report


class ResearchReviewTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "e1", "week": "2026-W40", "student": "s1", "question": "窗口影响", "claim": "两次测量不同", "evidence": "run-1", "status": "observed", "value": 5},
            {"id": "e2", "week": "2026-W40", "student": "s1", "question": "窗口影响", "claim": "可能与预热有关", "evidence": "note-1", "status": "interpreted"},
            {"id": "e3", "week": "2026-W41", "student": "s1", "question": "窗口影响", "claim": "换批次复测", "evidence": "", "status": "to_verify"},
            {"id": "e4", "week": "2026-W40", "student": "s2", "question": "窗口影响", "claim": "重复测量", "evidence": "run-2", "status": "observed", "value": 9, "cohort": "2026"},
            {"id": "e5", "week": "2026-W40", "student": "s2", "question": "窗口影响", "claim": "重复测量", "evidence": "run-3", "status": "observed", "value": 11, "cohort": "2026"},
            {"id": "e6", "week": "2026-W40", "student": "s3", "question": "窗口影响", "claim": "尚未测量", "evidence": "", "status": "to_verify", "value": None, "cohort": "2026"},
        ]

    def test_timeline_keeps_claims_separate_by_evidence_status(self):
        thread = summarize(self.records)["s1:窗口影响"]
        self.assertEqual(len(thread["observations"]), 1)
        self.assertEqual(len(thread["interpretations"]), 1)
        self.assertEqual(len(thread["to_verify"]), 1)
        self.assertTrue(thread["has_new_observation"])
        self.assertEqual(thread["evidence_progress"]["observed_weeks"], 1)
        self.assertEqual(thread["evidence_progress"]["weeks_without_linked_evidence"], ["2026-W41"])

    def test_report_flags_unlinked_plan_without_counting_it_as_observation(self):
        report = build_report(self.records, source_revision="r3")
        self.assertEqual(report["source_revision"], "r3")
        self.assertEqual(report["unlinked_records"], ["e3", "e6"])
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

    def test_cohort_summary_averages_within_student_and_reports_coverage(self):
        metrics = summarize_cohort_metrics(self.records)
        row = metrics["2026:窗口影响"][0]
        self.assertEqual(row["eligible_students"], 2)
        self.assertEqual(row["measured_students"], 1)
        self.assertEqual(row["coverage"], 0.5)
        self.assertEqual(row["mean"], 10)

    def test_unverified_or_unlinked_values_do_not_enter_metric_summary(self):
        metrics = summarize_cohort_metrics(self.records)
        row = metrics["未分组:窗口影响"][1]
        self.assertIsNone(row["mean"])
        self.assertEqual(row["measured_students"], 0)

    def test_non_finite_measurements_are_rejected(self):
        from research_review.facts import load_records
        from tempfile import NamedTemporaryFile
        import json

        invalid = dict(self.records[0], value=float("nan"))
        with NamedTemporaryFile("w", encoding="utf-8") as handle:
            json.dump([invalid], handle)
            handle.flush()
            with self.assertRaisesRegex(ValueError, "有限数值"):
                load_records(handle.name)


if __name__ == "__main__":
    unittest.main()
