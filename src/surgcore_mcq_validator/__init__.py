"""Offline, open-source structural quality validation for educational MCQs."""

__version__ = "0.2.0"

from .loader import InputError, load_questions, read_mapping
from .models import Issue, Question, ValidationReport
from .validator import normalize_text, validate_questions

__all__ = ["InputError", "Issue", "Question", "ValidationReport", "load_questions", "read_mapping", "normalize_text", "validate_questions"]
