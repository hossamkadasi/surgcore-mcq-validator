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
