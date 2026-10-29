"""CLI tests exercise output, errors, and exit status."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from surgcore_mcq_validator.cli import main


GOOD = [{
    "id": "Q1",
    "stem": "Which file extension represents a JavaScript Object Notation document?",
    "options": [".csv", ".json", ".html", ".png"],
    "answer": "B",
    "explanation": "JSON files usually use the .json extension.",
    "source": "Synthetic technical example",
}]


class CliTests(unittest.TestCase):
    def run_cli(self, args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(args)
        return code, out.getvalue(), err.getvalue()

    def test_success_text(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "good.json"
            path.write_text(json.dumps(GOOD), encoding="utf-8")
            code, out, err = self.run_cli(["validate", str(path)])
            self.assertEqual((code, err), (0, ""))
            self.assertIn("Errors: 0", out)

    def test_error_exit_one_and_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps([{**GOOD[0], "answer": "E"}]), encoding="utf-8")
            code, out, err = self.run_cli(["validate", str(path), "--format", "json"])
            self.assertEqual((code, err), (1, ""))
            self.assertEqual(json.loads(out)["issues"][0]["code"], "invalid_answer")

    def test_warning_exit_with_strict_policy(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "warn.json"
            path.write_text(json.dumps([{**GOOD[0], "source": ""}]), encoding="utf-8")
            code, _, _ = self.run_cli(["validate", str(path)])
            self.assertEqual(code, 0)
            code, _, _ = self.run_cli(["validate", str(path), "--fail-on", "warning"])
            self.assertEqual(code, 1)

    def test_output_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "good.json"
            path.write_text(json.dumps(GOOD), encoding="utf-8")
            report_path = Path(folder) / "reports" / "result.json"
            code, _, _ = self.run_cli(["validate", str(path), "--output", str(report_path), "--format", "json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(report_path.read_text(encoding="utf-8"))["summary"]["record_count"], 1)

    def test_cli_mapping_works(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bank.csv"
            path.write_text("qid,prompt,one,two,three,four,key\nX1,What is the correct label in the mapping example?,alpha,beta,gamma,delta,C\n", encoding="utf-8")
            config = Path(folder) / "mapping.json"
            config.write_text(json.dumps({"id": "qid", "stem": "prompt", "option_a": "one", "option_b": "two", "option_c": "three", "option_d": "four", "answer": "key"}), encoding="utf-8")
            code, out, _ = self.run_cli(["validate", str(path), "--mapping", str(config), "--format", "json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["summary"]["schema_valid_record_count"], 1)

    def test_missing_mapping_file_returns_2(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "good.json"
            path.write_text(json.dumps(GOOD), encoding="utf-8")
            code, _, err = self.run_cli(["validate", str(path), "--mapping", str(Path(folder) / "missing.json")])
            self.assertEqual(code, 2)
            self.assertIn("Mapping file not found", err)

    def test_report_cannot_overwrite_input_even_with_force(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "bank.json"
            original = json.dumps(GOOD)
            file.write_text(original, encoding="utf-8")
            for force in ([], ["--overwrite"]):
                code, _, err = self.run_cli(["validate", str(file), "--output", str(file), *force])
                self.assertEqual(code, 2)
                self.assertIn("Refusing", err)
                self.assertEqual(file.read_text(encoding="utf-8"), original)

    def test_report_cannot_overwrite_mapping(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "bank.json"
            file.write_text(json.dumps(GOOD), encoding="utf-8")
            mapping = Path(folder) / "mapping.json"
            original = '{"id": "id"}'
            mapping.write_text(original, encoding="utf-8")
            code, _, err = self.run_cli(["validate", str(file), "--mapping", str(mapping),
                                         "--output", str(mapping), "--overwrite"])
            self.assertEqual(code, 2)
            self.assertIn("Refusing", err)
            self.assertEqual(mapping.read_text(encoding="utf-8"), original)

    def test_report_overwrite_requires_explicit_flag(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "bank.json"
            file.write_text(json.dumps(GOOD), encoding="utf-8")
            report = Path(folder) / "report.json"
            report.write_text("Existing report must be preserved", encoding="utf-8")
            code, _, err = self.run_cli(["validate", str(file), "--format", "json", "--output", str(report)])
            self.assertEqual(code, 2)
            self.assertIn("--overwrite", err)
            self.assertEqual(report.read_text(encoding="utf-8"), "Existing report must be preserved")
            code, _, _ = self.run_cli(["validate", str(file), "--format", "json", "--output", str(report), "--overwrite"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["summary"]["record_count"], 1)

    def test_output_source_symlink_is_protected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "bank.json"
            source.write_text(json.dumps(GOOD), encoding="utf-8")
            link = Path(folder) / "fake-report.json"
            try:
                link.symlink_to(source)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable")
            before = source.read_text(encoding="utf-8")
            code, _, _ = self.run_cli(["validate", str(source), "--output", str(link), "--overwrite"])
            self.assertEqual(code, 2)
            self.assertEqual(source.read_text(encoding="utf-8"), before)

    def test_report_write_cleans_up_temp_files(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "bank.json"
            file.write_text(json.dumps(GOOD), encoding="utf-8")
            report = Path(folder) / "report.txt"
            code, _, _ = self.run_cli(["validate", str(file), "--output", str(report)])
            self.assertEqual(code, 0)
            self.assertEqual(list(Path(folder).glob(".surgcore-report-*.tmp")), [])

    def test_missing_file(self):
        code, _, err = self.run_cli(["validate", "/missing/example.csv"])
        self.assertEqual(code, 2)
        self.assertIn("Input error", err)

    def test_bad_similarity(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "good.json"
            path.write_text(json.dumps(GOOD), encoding="utf-8")
            code, _, err = self.run_cli(["validate", str(path), "--similarity", "0.5"])
            self.assertEqual(code, 2)
            self.assertIn("threshold", err)


if __name__ == "__main__":
    unittest.main()
