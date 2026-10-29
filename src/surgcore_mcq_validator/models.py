"""Data contracts for offline MCQ structure checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Question:
    record_index: int  # 1-based position in the input; not an external ID
    question_id: str
    stem: str
    options: tuple[str, str, str, str]
    answer: str
    explanation: str
    source: str


@dataclass(frozen=True)
class Issue:
    severity: Severity
    code: str
    record_index: int
    question_id: str
    message: str
    related_record_index: int | None = None
    similarity: float | None = None

    def to_dict(self) -> dict[str, object]:
        # Drop irrelevant null fields; stable schema across CLI and Python API.
        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True)
class ValidationReport:
    record_count: int
    issues: tuple[Issue, ...]

    @property
    def error_count(self) -> int:
        return sum(issue.severity == "error" for issue in self.issues)

    @property
    def warning_count(self) -> int:
        return sum(issue.severity == "warning" for issue in self.issues)

    @property
    def schema_valid_record_count(self) -> int:
        error_rows = {issue.record_index for issue in self.issues if issue.severity == "error"}
        return self.record_count - len(error_rows)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0",
            "summary": {
                "record_count": self.record_count,
                "schema_valid_record_count": self.schema_valid_record_count,
                "error_count": self.error_count,
                "warning_count": self.warning_count,
                "passed_structural_checks": self.error_count == 0,
            },
            "issues": [issue.to_dict() for issue in self.issues],
            "disclaimer": "Structural checks only. No medical fact-checking or clinical certification.",
        }
