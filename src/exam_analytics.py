"""Batch analytics using the same per-question grades as the results window."""
from dataclasses import dataclass
import math
import statistics
import typing as tp

from data_exporting import OutputSheet
from examinee_list import MATCH_COLUMN, NO_SCAN_STATUS


RESPONSE_LABELS = ("A", "B", "C", "D", "E", "Blank", "Multiple", "Other")


def response_category(answer: str) -> str:
    if answer in ("", "G"):
        return "Blank"
    if answer == "F" or (answer.startswith("[") and "|" in answer):
        return "Multiple"
    return answer if answer in RESPONSE_LABELS[:5] else "Other"


@dataclass
class QuestionStats:
    name: str
    key: str
    responses: tp.Dict[str, int]
    correct: int = 0
    incorrect: int = 0

    @property
    def graded(self):
        return self.correct + self.incorrect

    @property
    def incorrect_percent(self):
        return 100 * self.incorrect / self.graded if self.graded else None


@dataclass
class BatchAnalytics:
    scan_count: int
    missing_count: int
    questions: tp.List[QuestionStats]
    percentages: tp.List[float]

    @property
    def mean_score(self):
        return statistics.mean(self.percentages) if self.percentages else None

    @property
    def median_score(self):
        return statistics.median(self.percentages) if self.percentages else None

    @property
    def hardest_questions(self):
        # Stable ties preserve numeric question order.
        return sorted((q for q in self.questions if q.graded),
                      key=lambda q: q.incorrect, reverse=True)

    @property
    def response_totals(self):
        return {label: sum(q.responses[label] for q in self.questions)
                for label in RESPONSE_LABELS}

    @property
    def score_distribution(self):
        counts = [0] * 10
        for score in self.percentages:
            counts[min(int(score // 10), 9)] += 1
        return [(f"{i * 10}\u2013{'<' if i < 9 else ''}{(i + 1) * 10}%", count)
                for i, count in enumerate(counts)]


def build_analytics(results: OutputSheet, scores: tp.Optional[OutputSheet],
                    answer_key: tp.Optional[OutputSheet] = None) -> BatchAnalytics:
    """Count each processed scan once; no-scan roster rows never enter denominators.

    A shorter key restricts analysis to that exam's questions. Missing grades
    stay unscored rather than becoming incorrect answers. Scores are joined by
    ID and source file so repeated IDs retain their separate scan results.
    """
    headings = results.data[0]
    start = results.first_question_column_index
    question_names = headings[start:]
    key_answers = {}
    if answer_key is not None and answer_key.row_count == 1:
        key_start = answer_key.first_question_column_index
        key_answers = dict(zip(answer_key.data[0][key_start:],
                               answer_key.data[1][key_start:]))
        question_names = [name for name in question_names if name in key_answers]
    questions = [QuestionStats(name, key_answers.get(name, ""),
                               dict.fromkeys(RESPONSE_LABELS, 0))
                 for name in question_names]
    columns = {name: headings.index(name, start) for name in question_names}
    id_index = headings.index("Examinee ID")
    source_index = headings.index("Source File")
    match_index = headings.index(MATCH_COLUMN) if MATCH_COLUMN in headings else None
    score_rows = {}
    score_columns = {}
    percent_index = None
    if scores is not None:
        score_headings = scores.data[0]
        score_id = score_headings.index("Examinee ID")
        score_source = score_headings.index("Source File")
        percent_index = score_headings.index("Total Score (%)")
        score_columns = {name: index for index, name in enumerate(score_headings)
                         if index >= scores.first_question_column_index}
        score_rows = {(row[score_id], row[score_source]): row for row in scores.data[1:]}

    percentages = []
    scan_count = missing_count = 0
    for row in results.data[1:]:
        if match_index is not None and row[match_index] == NO_SCAN_STATUS:
            missing_count += 1
            continue
        scan_count += 1
        scored = score_rows.get((row[id_index], row[source_index]), [])
        if scored and percent_index is not None:
            try:
                percent = float(scored[percent_index])
            except (ValueError, TypeError):
                pass
            else:
                if math.isfinite(percent) and 0 <= percent <= 100:
                    percentages.append(percent)
        for question in questions:
            column = columns[question.name]
            answer = row[column] if column < len(row) else ""
            question.responses[response_category(answer)] += 1
            grade_column = score_columns.get(question.name)
            grade = (scored[grade_column] if grade_column is not None
                     and grade_column < len(scored) else "")
            question.correct += int(grade == "1")
            question.incorrect += int(grade == "0")
    return BatchAnalytics(scan_count, missing_count, questions, percentages)
