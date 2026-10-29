"""Unit tests run with python -m unittest discover -s tests -v."""

import json
import tempfile
import unittest
from pathlib import Path

from surgcore_mcq_validator import InputError, Question, load_questions, normalize_text, validate_questions


def question(index=1, **changes):
    row = dict(
        record_index=index,
        question_id=f"Q{index}",
        stem="Which field stores the correct answer label for this MCQ?",
        options=("id", "answer", "source", "explanation"),
        answer="B",
        explanation="The answer field contains an option label.",
        source="Synthetic example, not clinical content",
    )
    row.update(changes)
    return Question(**row)


class ValidatorTests(unittest.TestCase):
    def codes(self, *questions, **kwargs):
        return [issue.code for issue in validate_questions(list(questions), **kwargs).issues]

    def test_valid_question(self):
        self.assertEqual(self.codes(question()), [])

    def test_missing_question_id(self):
        self.assertIn("missing_id", self.codes(question(question_id="")))

    def test_duplicate_ids(self):
        results = validate_questions([question(1), question(2, question_id="Q1", stem="What is the second synthetic question in this example?")])
        duplicate = next(issue for issue in results.issues if issue.code == "duplicate_id")
        self.assertEqual(duplicate.related_record_index, 1)

    def test_empty_stem(self):
        self.assertIn("missing_stem", self.codes(question(stem="")))

    def test_short_stem_warning(self):
        report = validate_questions([question(stem="Why?")])
        self.assertTrue(any(issue.code == "short_stem" and issue.severity == "warning" for issue in report.issues))

    def test_empty_option(self):
        self.assertIn("missing_option", self.codes(question(options=("one", "two", "", "four"))))

    def test_duplicate_option(self):
        self.assertIn("duplicate_option", self.codes(question(options=("same value", " same VALUE! ", "three", "four"))))

    def test_missing_answer(self):
        self.assertIn("missing_answer", self.codes(question(answer="")))

    def test_invalid_answer(self):
        self.assertIn("invalid_answer", self.codes(question(answer="E")))

    def test_multiletter_answer_is_invalid(self):
        self.assertIn("invalid_answer", self.codes(question(answer="AB")))

    def test_lowercase_answer_allowed(self):
        self.assertEqual(self.codes(question(answer="b")), [])

    def test_missing_provenance_warnings(self):
        report = validate_questions([question(explanation="", source="")])
        self.assertEqual({issue.code for issue in report.issues}, {"missing_explanation", "missing_source"})
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 2)

    def test_exact_duplicate_normalizes_punctuation(self):
        first = question(1)
        second = question(2, stem="which field stores the correct ANSWER label for this MCQ!!!")
        self.assertIn("duplicate_stem", self.codes(first, second))

    def test_near_duplicates(self):
        first = question(1)
        second = question(2, stem="Which field stores the correct answer label for this MCQ record?")
        report = validate_questions([first, second], near_duplicate_threshold=0.80)
        issues = [issue for issue in report.issues if issue.code == "near_duplicate_stem"]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].related_record_index, 1)

    def test_near_duplicates_disabled(self):
        first = question(1)
        second = question(2, stem="Which field stores the correct answer label for this MCQ record?")
        self.assertNotIn("near_duplicate_stem", self.codes(first, second, check_near_duplicates=False))

    def test_no_false_positive_unrelated(self):
        first = question(1)
        second = question(2, stem="Where should release history be recorded before publishing changes?")
        self.assertNotIn("near_duplicate_stem", self.codes(first, second))

    def test_threshold_validation(self):
        with self.assertRaises(ValueError):
            validate_questions([question()], near_duplicate_threshold=0.50)

    def test_report_summary(self):
        report = validate_questions([question(), question(2, answer="E", stem="Why does the data validator produce a report?")])
        summary = report.to_dict()["summary"]
        self.assertEqual(summary["record_count"], 2)
        self.assertEqual(summary["schema_valid_record_count"], 1)
        self.assertEqual(summary["error_count"], 1)
        self.assertFalse(summary["passed_structural_checks"])

    def test_arabic_normalization(self):
        self.assertEqual(normalize_text("  سؤال،   طبي! "), "سؤال طبي")


class LoaderTests(unittest.TestCase):
    def test_json_object_with_mapping_options(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.json"
            path.write_text(json.dumps({"questions": [{
                "id": "Q1", "stem": "Choose the correct label from options",
                "options": {"A": "one", "B": "two", "C": "three", "D": "four"},
                "answer": "b", "source": "synthetic", "explanation": "test",
            }]}), encoding="utf-8")
            data = load_questions(path)
            self.assertEqual(data[0].options, ("one", "two", "three", "four"))
            self.assertEqual(data[0].answer, "b")

    def test_json_list_options(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.json"
            path.write_text(json.dumps([{"id": 42, "question": "Synthetic question long enough?", "options": ["A1", "B1", "C1", "D1"], "correct_answer": "A"}]), encoding="utf-8")
            data = load_questions(path)
            self.assertEqual(data[0].question_id, "42")
            self.assertEqual(data[0].options[2], "C1")

    def test_csv_alias_headers(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.csv"
            path.write_text("id,question,option_a,option_b,option_c,option_d,correct_answer\nQ1,Which field is used here?,one,two,three,four,A\n", encoding="utf-8")
            data = load_questions(path)
            self.assertEqual(data[0].stem, "Which field is used here?")
            self.assertEqual(data[0].answer, "A")

    def test_reject_empty_bank(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaises(InputError):
                load_questions(path)

    def test_reject_bad_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("{bad", encoding="utf-8")
            with self.assertRaises(InputError):
                load_questions(path)

    def test_reject_non_object(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("[1]", encoding="utf-8")
            with self.assertRaises(InputError):
                load_questions(path)

    def test_reject_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.txt"
            path.write_text("hello", encoding="utf-8")
            with self.assertRaises(InputError):
                load_questions(path)


if __name__ == "__main__":
    unittest.main()
