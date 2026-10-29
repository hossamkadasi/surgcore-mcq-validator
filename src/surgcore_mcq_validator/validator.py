"""Deterministic structural validation of educational MCQ banks.

Not an answer-key verifier, plagiarism detector, or medical review system.
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from difflib import SequenceMatcher
from typing import Sequence

from .models import Issue, Question, ValidationReport

OPTION_LETTERS = "ABCD"
MAX_POSTING_LIST = 60  # Ignore overly common shingles when finding fuzzy candidates.


def normalize_text(value: str) -> str:
    """Normalize case, spaces and punctuation for *heuristic* deduplication."""
    unicode_normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", unicode_normalized, flags=re.UNICODE))


def _shingles(stem: str) -> set[str]:
    tokens = stem.split()
    if len(tokens) < 4:
        return set()
    return {" ".join(tokens[i : i + 3]) for i in range(len(tokens) - 2)}


def validate_questions(
    questions: Sequence[Question], *, near_duplicate_threshold: float = 0.92,
    check_near_duplicates: bool = True,
) -> ValidationReport:
    """Check structural quality and heuristically flag similar stems.

    check_near_duplicates uses informative token trigrams as candidate blocks. This
    bounds ordinary use but is not a comprehensive semantic similarity search.
    """
    if not 0.80 <= near_duplicate_threshold <= 1.0:
        raise ValueError("near_duplicate_threshold must be within [0.80, 1.00]")

    issues: list[Issue] = []
    seen_ids: dict[str, int] = {}
    seen_stems: dict[str, int] = {}
    prior_stems: dict[int, str] = {}
    inverted: dict[str, list[int]] = defaultdict(list)

    def flag(question: Question, severity: str, code: str, message: str, *,
             related: int | None = None, similarity: float | None = None) -> None:
        issues.append(Issue(
            severity=severity,  # type: ignore[arg-type]
            code=code,
            record_index=question.record_index,
            question_id=question.question_id,
            message=message,
            related_record_index=related,
            similarity=similarity,
        ))

    for question in questions:
        qid = question.question_id
        if not qid:
            flag(question, "error", "missing_id", "Question ID is missing")
        elif qid in seen_ids:
            flag(question, "error", "duplicate_id", f"ID duplicates record {seen_ids[qid]}", related=seen_ids[qid])
        else:
            seen_ids[qid] = question.record_index

        stem = normalize_text(question.stem)
        if not stem:
            flag(question, "error", "missing_stem", "Question stem is empty")
        elif len(stem) < 12:
            flag(question, "warning", "short_stem", "Question stem is unusually short")

        present_options: dict[str, str] = {}
        for letter, option_text in zip(OPTION_LETTERS, question.options):
            normalized_option = normalize_text(option_text)
            if not normalized_option:
                flag(question, "error", "missing_option", f"Option {letter} is empty")
            elif normalized_option in present_options:
                flag(question, "error", "duplicate_option", f"Option {letter} duplicates option {present_options[normalized_option]}")
            else:
                present_options[normalized_option] = letter

        if not question.answer:
            flag(question, "error", "missing_answer", "Correct answer label is missing")
        elif question.answer.upper() not in set(OPTION_LETTERS):
            flag(question, "error", "invalid_answer", "Correct answer must be A, B, C or D")

        if not question.explanation:
            flag(question, "warning", "missing_explanation", "Explanation is missing")
        if not question.source:
            flag(question, "warning", "missing_source", "Source/reference is missing")

        if stem:
            if stem in seen_stems:
                flag(question, "error", "duplicate_stem", f"Question stem duplicates record {seen_stems[stem]}", related=seen_stems[stem])
            else:
                # Fuzzy matching is deliberately conservative and may miss some paraphrases.
                shingles = _shingles(stem)
                if check_near_duplicates and shingles:
                    candidates: set[int] = set()
                    for shingle in shingles:
                        posting = inverted.get(shingle, [])
                        if len(posting) <= MAX_POSTING_LIST:
                            candidates.update(posting)
                    best_index: int | None = None
                    best_score = near_duplicate_threshold
                    for previous_index in sorted(candidates):
                        previous_stem = prior_stems[previous_index]
                        if abs(len(stem) - len(previous_stem)) > max(len(stem), len(previous_stem)) * (1 - near_duplicate_threshold):
                            continue
                        score = SequenceMatcher(None, stem, previous_stem, autojunk=False).ratio()
                        if score >= best_score:
                            best_index = previous_index
                            best_score = score
                    if best_index is not None:
                        flag(question, "warning", "near_duplicate_stem", f"Stem resembles record {best_index}", related=best_index, similarity=round(best_score, 3))

                for shingle in shingles:
                    inverted[shingle].append(question.record_index)
                prior_stems[question.record_index] = stem
                seen_stems[stem] = question.record_index

    return ValidationReport(record_count=len(questions), issues=tuple(issues))
