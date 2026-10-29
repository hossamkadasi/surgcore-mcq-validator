"""Command line interface for the SurgCore MCQ Validator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .loader import InputError, load_questions, read_mapping
from .models import ValidationReport
from .validator import validate_questions


def format_text(report: ValidationReport) -> str:
    summary = report.to_dict()["summary"]
    lines = [
        f"Records: {summary['record_count']} | Schema-valid records: {summary['schema_valid_record_count']}",
        f"Errors: {report.error_count} | Warnings: {report.warning_count}",
    ]
    for issue in report.issues:
        location = f"record {issue.record_index}"
        if issue.question_id:
            location += f" (id={issue.question_id})"
        lines.append(f"[{issue.severity.upper()}] {location} {issue.code}: {issue.message}")
    lines.append("NOTE: Structural checks only; not a medical accuracy review.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="surgcore-mcq-validator", description="Offline quality checks for educational MCQ banks")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="Validate local CSV/JSON questions")
    validate_parser.add_argument("file", type=Path, help="Local .csv or .json input")
    validate_parser.add_argument("--format", choices=("text", "json"), default="text", help="Report format")
    validate_parser.add_argument("--mapping", type=Path, help="JSON mapping of canonical fields to CSV/JSON source keys")
    validate_parser.add_argument("--output", type=Path, help="Write report to a local file")
    validate_parser.add_argument("--fail-on", choices=("error", "warning"), default="error", help="What triggers exit status 1")
    validate_parser.add_argument("--similarity", type=float, default=0.92, help="Near-duplicate threshold (0.80-1.00)")
    validate_parser.add_argument("--no-near-duplicates", action="store_true", help="Disable fuzzy duplicate scan")
    args = parser.parse_args(argv)

    try:
        mapping = read_mapping(args.mapping) if args.mapping else None
        questions = load_questions(args.file, field_mapping=mapping)
        report = validate_questions(
            questions, near_duplicate_threshold=args.similarity,
            check_near_duplicates=not args.no_near_duplicates,
        )
        output_text = json.dumps(report.to_dict(), ensure_ascii=False, indent=2) if args.format == "json" else format_text(report)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output_text + "\n", encoding="utf-8")
            print(f"Report written to {args.output}")
        else:
            print(output_text)
        has_failure = bool(report.error_count or (args.fail_on == "warning" and report.warning_count))
        return 1 if has_failure else 0
    except (InputError, ValueError, OSError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
