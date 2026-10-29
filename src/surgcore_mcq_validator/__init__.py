"""Offline, open-source structural quality validation for educational MCQs."""

__version__ = "0.1.0"

from .loader import InputError, load_questions
from .models import Issue, Question, ValidationReport
from .validator import normalize_text, validate_questions

__all__ = ["InputError", "Issue", "Question", "ValidationReport", "load_questions", "normalize_text", "validate_questions"]
