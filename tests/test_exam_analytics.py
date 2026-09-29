"""Synthetic batch checks for chart counts and scoring denominators."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_exporting import OutputSheet
from exam_analytics import build_analytics
from examinee_list import ExamineeTable
from grid_info import Field, VirtualField
from scoring import score_results


class AnalyticsTests(unittest.TestCase):
    def make_batch(self):
        scans = OutputSheet([Field.STUDENT_ID, Field.IMAGE_FILE], 4)
        for identity, source, answers in (
                ("01", "one.png", ["A", "B", "", "D"]),
                ("01", "repeat.png", ["B", "F", "G", "D"]),
                ("02", "two.png", ["A", "[A|B]", "C", "A"])):
            scans.add({Field.STUDENT_ID: identity, Field.IMAGE_FILE: source}, answers)
        key = OutputSheet([Field.IMAGE_FILE], 4)
        key.add({}, ["A", "B", "C", "D"])
        return scans, key

    def test_counts_grades_and_ranking_exclude_roster_without_scans(self):
        scans, key = self.make_batch()
        roster = ExamineeTable(["Examinee ID"], [["01"], ["02"], ["03"]]).bind()
        review, _, _ = roster.merge(scans, include_unscanned=True)
        scores = score_results(scans, key, 4)
        scores.data[1:] = list(reversed(scores.data[1:]))
        batch = build_analytics(review, scores, key)
        self.assertEqual((batch.scan_count, batch.missing_count), (3, 1))
        self.assertEqual(batch.percentages, [75, 25, 50])
        self.assertEqual(batch.mean_score, 50)
        self.assertEqual(batch.median_score, 50)
        self.assertEqual([q.name for q in batch.hardest_questions], ["Q2", "Q3", "Q1", "Q4"])
        self.assertEqual(batch.questions[1].responses["Multiple"], 2)
        self.assertEqual(batch.questions[2].responses["Blank"], 2)
        self.assertAlmostEqual(batch.questions[1].incorrect_percent, 200 / 3)
        self.assertEqual(sum(batch.response_totals.values()), 12)
        for q in batch.questions:
            self.assertEqual(sum(q.responses.values()), 3)
            self.assertEqual(q.graded, 3)

    def test_no_key_preserves_responses_without_inventing_grades(self):
        scans, _ = self.make_batch()
        batch = build_analytics(scans, None)
        self.assertEqual(batch.percentages, [])
        self.assertIsNone(batch.mean_score)
        self.assertEqual(batch.hardest_questions, [])
        self.assertTrue(all(q.incorrect_percent is None for q in batch.questions))
        self.assertEqual(batch.response_totals["Multiple"], 2)

    def test_short_key_ignores_unused_questions_and_padded_score_headers(self):
        scans, _ = self.make_batch()
        key = OutputSheet([Field.IMAGE_FILE], 4)
        key.add({}, ["A", "B"])
        batch = build_analytics(scans, score_results(scans, key, 4), key)
        self.assertEqual([q.name for q in batch.questions], ["Q1", "Q2"])
        self.assertEqual(batch.percentages, [100, 0, 50])
        self.assertEqual(sum(batch.response_totals.values()), 6)
        self.assertEqual([count for _, count in batch.score_distribution],
                         [1, 0, 0, 0, 0, 1, 0, 0, 0, 1])

    def test_empty_batch_and_no_scan_only(self):
        scans = OutputSheet([Field.STUDENT_ID, Field.IMAGE_FILE], 3)
        batch = build_analytics(scans, None)
        self.assertEqual(batch.scan_count, 0)
        self.assertEqual(sum(batch.response_totals.values()), 0)
        self.assertIsNone(batch.median_score)
        roster = ExamineeTable(["Examinee ID"], [["01"]]).bind()
        review, _, _ = roster.merge(scans, include_unscanned=True)
        batch = build_analytics(review, None)
        self.assertEqual((batch.scan_count, batch.missing_count), (0, 1))
        self.assertEqual(sum(batch.response_totals.values()), 0)

    def test_missing_grades_do_not_become_incorrect_and_other_response_is_counted(self):
        scans, key = self.make_batch()
        scans.data[1][-1] = "?"
        scores = score_results(scans, key, 4)
        scores.data[1] = scores.data[1][:-1]
        scores.data[2][scores.data[0].index("Total Score (%)")] = "NO KEY FOUND"
        scores.data[2] = scores.data[2][:scores.first_question_column_index]
        batch = build_analytics(scans, scores, key)
        self.assertEqual(batch.questions[3].responses["Other"], 1)
        self.assertEqual(batch.questions[3].graded, 1)
        self.assertEqual(batch.questions[3].incorrect, 1)
        self.assertEqual(len(batch.percentages), 2)

    def test_score_bin_boundaries_and_invalid_scores(self):
        scans = OutputSheet([Field.STUDENT_ID, Field.IMAGE_FILE], 1)
        scores = OutputSheet([Field.STUDENT_ID, Field.IMAGE_FILE, VirtualField.SCORE], 1)
        for index, score in enumerate(("0", "9.99", "10", "89.99", "90", "100", "nan", "inf", "-1", "101")):
            fields = {Field.STUDENT_ID: str(index), Field.IMAGE_FILE: f"{index}.png"}
            scans.add(fields, ["A"])
            scores.add({**fields, VirtualField.SCORE: score}, ["1"])
        batch = build_analytics(scans, scores)
        self.assertEqual([count for _, count in batch.score_distribution],
                         [2, 1, 0, 0, 0, 0, 0, 0, 1, 2])


if __name__ == "__main__":
    unittest.main()
