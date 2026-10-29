# SurgCore MCQ Validator

**An offline, open-source quality checker for multiple-choice question (MCQ) datasets.**

Before importing educational questions into a quiz application, check for missing or duplicated IDs, malformed choices, unsupported answer labels, absent explanations/references, and identical or *potentially* similar question stems. The CLI also emits machine-readable JSON for review workflows.

The validator was designed for the needs of medical education question banks, but works with any four-option educational MCQ bank. **It does not verify the medical accuracy of questions or answers.**

- Runs locally; **no uploads, accounts, analytics, API keys, or network requests**.
- Works with JSON and CSV; Python 3.10+; no runtime dependencies.
- Supports English and other Unicode text (including Arabic) for normalization.
- Separates blocking `error`s from non-blocking `warning`s.
- Supports human-readable output and JSON reports for downstream review.
- MIT licensed, with synthetic examples only.

## Quick start

From this repository root, without installing anything:

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.json
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="src"; python -m surgcore_mcq_validator validate examples/synthetic_questions.json
```

Or install as a CLI into your chosen Python environment:

```bash
python -m pip install .
surgcore-mcq-validator validate examples/synthetic_questions.csv
```

The JSON example intentionally includes one duplicated stem and an invalid `E` answer. The program should exit with code **1**, showing both issues. The CSV example contains valid synthetic rows and exits with **0**.

To export a JSON report:

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.json --format json --output reports/qa.json
```

Warnings can block CI or import gates if desired:

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.csv --fail-on warning
```

Use `--no-near-duplicates` to disable the optional fuzzy-stem check or `--similarity 0.95` to adjust its sensitivity (allowed range: 0.80-1.00).

## Supported schema

### JSON

Accept a list or a wrapper object with a `questions` list:

```json
{
  "questions": [
    {
      "id": "EXAMPLE-1",
      "stem": "Which field identifies the correct answer option?",
      "options": {"A": "source", "B": "answer", "C": "stem", "D": "id"},
      "answer": "B",
      "explanation": "Answer holds an option label.",
      "source": "Synthetic example"
    }
  ]
}
```

Alternatively, `options` may be a four-item list in A/B/C/D order. Flat JSON fields `option_a` through `option_d` also work.

### CSV

Columns: `id,stem,option_a,option_b,option_c,option_d,answer,explanation,source`.

Aliases: `question`/`question_text` for `stem`, `question_id` for `id`, `correct_answer`/`correct_option` for `answer`, `rationale` for `explanation`, `reference` for `source`.

Extra columns are ignored; `explanation` and `source` may be omitted but trigger warnings. See [`examples/synthetic_questions.csv`](examples/synthetic_questions.csv).

## What the checker reports

| Severity | Code | Meaning |
| --- | --- | --- |
| Error | `missing_id`, `duplicate_id` | Missing or repeated question identifiers |
| Error | `missing_stem`, `missing_option` | Empty question or A-D choice |
| Error | `duplicate_option` | Two options normalize to the same text |
| Error | `missing_answer`, `invalid_answer` | No answer or label outside A-D |
| Error | `duplicate_stem` | Stems match after case/punctuation/space normalization |
| Warning | `short_stem` | Stem is unusually short |
| Warning | `missing_explanation`, `missing_source` | Missing educational rationale or provenance |
| Warning | `near_duplicate_stem` | A *heuristic*, not semantic, near-match was found |

Near-duplicate scanning uses overlapping three-word shingles to select candidates, then character-sequence similarity. It may **miss paraphrases** and may flag false positives, especially for templated questions. Always review flags manually.

JSON reports include issue location, stable code, severity, related record (when present), and summary counts. `schema_valid_record_count` counts rows with no **structural errors**; it is **not** a medically reviewed or publication-ready count.

### Exit codes

- `0`: no issues meeting the failure policy (`--fail-on error` by default).
- `1`: one or more issues meet the failure policy.
- `2`: invalid input, unsupported format, file error, or invalid threshold.

## Testing

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Tests run offline. A green test suite is not a substitute for evaluating the validator on representative, **authorized** data.

## Privacy, safety, and licensing

- Local file processing only. **Do not commit patient data, private questions, licensed books, exam papers, API keys, or production exports** to a public repository.
- The sample questions are artificial. No protected medical content is included.
- Correct-answer labels are checked only for structure, **not factual correctness**. A medical educator must independently review clinical content and reference quality prior to publication.
- This repository and the SurgCore Pro commercial/production application are separate. **Nothing here grants access to SurgCore Pro source code or its private question banks.**
- See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Roadmap (not yet implemented)

- Configurable import mapping for diverse MCQ schemas.
- Human-in-the-loop review bundles for near duplicates.
- Optional CI integration after verifying workflow billing availability.
- User-supplied clinical evidence metadata checks (without claiming factual verification).

We welcome reports of reproducible bugs, test cases based on synthetic data, and contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT, see [LICENSE](LICENSE). Maintained by the SurgCore open-source community.
