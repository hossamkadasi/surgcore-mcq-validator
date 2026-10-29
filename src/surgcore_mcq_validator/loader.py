"""Load CSV and JSON question banks without network requests or dependencies."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import Question

MAX_BYTES = 25 * 1024 * 1024
OPTION_LETTERS = "ABCD"


class InputError(ValueError):
    """Invalid input file or unsupported input schema."""


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalized_keys(raw: dict[str, Any]) -> dict[str, Any]:
    return {str(key).strip().lower(): value for key, value in raw.items()}


def _field(record: dict[str, Any], *keys: str) -> str:
    for key in keys:
        if key in record:
            return _text(record[key])
    return ""


def _parse_question(raw: dict[str, Any], index: int) -> Question:
    record = _normalized_keys(raw)
    nested_options = record.get("options")
    if isinstance(nested_options, dict):
        options_by_letter = _normalized_keys(nested_options)
        options = tuple(_text(options_by_letter.get(letter.lower())) for letter in OPTION_LETTERS)
    elif isinstance(nested_options, list):
        options = tuple(_text(nested_options[i]) if i < len(nested_options) else "" for i in range(4))
    else:
        options = tuple(_field(record, f"option_{letter.lower()}", letter.lower()) for letter in OPTION_LETTERS)

    return Question(
        record_index=index,
        question_id=_field(record, "id", "question_id"),
        stem=_field(record, "stem", "question", "question_text"),
        options=options,  # type: ignore[arg-type]
        answer=_field(record, "answer", "correct_answer", "correct_option"),
        explanation=_field(record, "explanation", "rationale"),
        source=_field(record, "source", "reference"),
    )


def load_questions(filename: str | Path) -> list[Question]:
    """Parse a local JSON or CSV file; raise InputError for file-level failures."""
    path = Path(filename)
    if not path.is_file():
        raise InputError(f"File not found: {path}")
    if path.stat().st_size > MAX_BYTES:
        raise InputError(f"Input exceeds {MAX_BYTES // (1024 * 1024)} MiB limit")
    ext = path.suffix.lower()
    if ext not in {".json", ".csv"}:
        raise InputError("Supported extensions: .json or .csv")

    try:
        if ext == ".json":
            with path.open("r", encoding="utf-8-sig") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                data = data.get("questions")
            if not isinstance(data, list):
                raise InputError("JSON must be a list of question objects or {\"questions\": [...]}.")
            rows = data
        else:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    raise InputError("CSV must contain a header row")
                rows = list(reader)
    except (UnicodeError, OSError, json.JSONDecodeError, csv.Error) as exc:
        raise InputError(f"Unable to parse input: {exc}") from exc

    if not rows:
        raise InputError("Input contains no question records")

    questions: list[Question] = []
    for index, raw in enumerate(rows, start=1):
        if not isinstance(raw, dict):
            raise InputError(f"Record {index} must be an object")
        questions.append(_parse_question(raw, index))
    return questions
