"""Load local CSV and JSON MCQ banks; reject ambiguous or lossy input."""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .models import Question

MAX_BYTES = 25 * 1024 * 1024
MAX_MAPPING_BYTES = 32 * 1024
OPTION_LETTERS = "ABCD"
FIELD_ALIASES = {
    "id": ("id", "question_id"),
    "stem": ("stem", "question", "question_text"),
    "option_a": ("option_a", "a"),
    "option_b": ("option_b", "b"),
    "option_c": ("option_c", "c"),
    "option_d": ("option_d", "d"),
    "answer": ("answer", "correct_answer", "correct_option"),
    "explanation": ("explanation", "rationale"),
    "source": ("source", "reference"),
}


class InputError(ValueError):
    """Invalid input file, mapping, or unsupported schema."""


def _text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def _normalize_keys(raw: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in raw.items():
        if not isinstance(key, str) or not key.strip():
            raise InputError("Record contains a missing or invalid field name")
        name = key.strip().casefold()
        if name in normalized:
            raise InputError(f"Duplicate field name (case-insensitive): {name}")
        normalized[name] = value
    return normalized


def read_mapping(filename: str | Path) -> dict[str, str]:
    """Read a small JSON object mapping canonical field names to source names."""
    path = Path(filename)
    if not path.is_file():
        raise InputError(f"Mapping file not found: {path}")
    if path.stat().st_size > MAX_MAPPING_BYTES:
        raise InputError("Mapping exceeds 32 KiB")
    try:
        with path.open("r", encoding="utf-8-sig") as file:
            mapping = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"Cannot read field mapping: {exc}") from exc
    if not isinstance(mapping, dict) or not mapping:
        raise InputError("Mapping must be a nonempty JSON object")
    result: dict[str, str] = {}
    for canonical, source in mapping.items():
        if canonical not in FIELD_ALIASES:
            raise InputError(f"Unknown canonical mapping key: {canonical}")
        if not isinstance(source, str) or not source.strip():
            raise InputError(f"Mapping for {canonical} must be a nonempty string")
        result[canonical] = source.strip().casefold()
    if len(set(result.values())) < len(result):
        raise InputError("Mapping source columns must be unique")
    return result


def _field(record: Mapping[str, Any], canonical: str, mapping: Mapping[str, str]) -> str:
    if canonical in mapping:
        return _text(record.get(mapping[canonical]))
    for alias in FIELD_ALIASES[canonical]:
        if alias in record:
            return _text(record[alias])
    return ""


def _parse_question(raw: Mapping[str, Any], index: int, mapping: Mapping[str, str]) -> Question:
    record = _normalize_keys(raw)
    nested_options = record.get("options")
    option_map_set = any(f"option_{letter.lower()}" in mapping for letter in OPTION_LETTERS)
    if option_map_set:
        options = tuple(_field(record, f"option_{letter.lower()}", mapping) for letter in OPTION_LETTERS)
    elif isinstance(nested_options, dict):
        nested = _normalize_keys(nested_options)
        if set(nested) != set(OPTION_LETTERS.lower()):
            raise InputError(f"Record {index}: nested options must have exactly A, B, C and D")
        options = tuple(_text(nested[letter.lower()]) for letter in OPTION_LETTERS)
    elif isinstance(nested_options, list):
        if len(nested_options) != 4:
            raise InputError(f"Record {index}: nested options must contain exactly 4 choices")
        options = tuple(_text(option) for option in nested_options)
    elif nested_options is not None:
        raise InputError(f"Record {index}: options must be a 4-item list or A-D object")
    else:
        options = tuple(_field(record, f"option_{letter.lower()}", mapping) for letter in OPTION_LETTERS)

    return Question(
        record_index=index,
        question_id=_field(record, "id", mapping),
        stem=_field(record, "stem", mapping),
        options=options,  # type: ignore[arg-type]
        answer=_field(record, "answer", mapping),
        explanation=_field(record, "explanation", mapping),
        source=_field(record, "source", mapping),
    )


def load_questions(filename: str | Path, *, field_mapping: Mapping[str, str] | None = None) -> list[Question]:
    """Read local MCQs. Never uploads, rewrites, or transmits source content."""
    path = Path(filename)
    if not path.is_file():
        raise InputError(f"File not found: {path}")
    if path.stat().st_size > MAX_BYTES:
        raise InputError("Input exceeds 25 MiB")
    if path.suffix.casefold() not in {".json", ".csv"}:
        raise InputError("Supported extensions: .json or .csv")
    mapping = field_mapping or {}
    for field, column in mapping.items():
        if field not in FIELD_ALIASES or not isinstance(column, str) or not column.strip():
            raise InputError("Invalid field mapping")
    try:
        if path.suffix.casefold() == ".json":
            with path.open("r", encoding="utf-8-sig") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                data = data.get("questions")
            if not isinstance(data, list):
                raise InputError('JSON must be a list or {"questions": [...]}')
            rows = data
        else:
            with path.open("r", encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if not reader.fieldnames:
                    raise InputError("CSV must have a header row")
                headers = [key.strip().casefold() for key in reader.fieldnames if key is not None]
                if len(headers) != len(reader.fieldnames) or not all(headers) or len(set(headers)) != len(headers):
                    raise InputError("CSV column names must be unique and nonempty")
                rows = list(reader)
    except (OSError, UnicodeError, json.JSONDecodeError, csv.Error) as exc:
        raise InputError(f"Unable to parse input: {exc}") from exc

    if not rows:
        raise InputError("Input contains no question records")
    result: list[Question] = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise InputError(f"Record {index} must be an object")
        if None in row:
            raise InputError(f"Record {index}: CSV contains more fields than its header")
        result.append(_parse_question(row, index, mapping))
    return result
