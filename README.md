# SurgCore MCQ Validator

[![Python tests](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/workflows/tests.yml/badge.svg)](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/workflows/tests.yml)

**An offline, open-source quality checker for multiple-choice question (MCQ) datasets.**

**Previous stable release:** [v0.3.0](https://github.com/hossamkadasi/surgcore-mcq-validator/releases/tag/v0.3.0) — [Download the offline browser ZIP](https://github.com/hossamkadasi/surgcore-mcq-validator/releases/download/v0.3.0/surgcore-mcq-browser-demo-v0.3.0.zip) or [Python wheel](https://github.com/hossamkadasi/surgcore-mcq-validator/releases/download/v0.3.0/surgcore_mcq_validator-0.3.0-py3-none-any.whl). Artifacts are published only after CI passes.

Before importing educational questions into a quiz application, check for missing or duplicated IDs, malformed choices, unsupported answer labels, absent explanations/references, and identical or *potentially* similar question stems. The CLI also emits machine-readable JSON for review workflows.

The validator was designed for the needs of medical education question banks, but works with any four-option educational MCQ bank. **It does not verify the medical accuracy of questions or answers.**

- Runs locally; **no uploads, accounts, analytics, API keys, or network requests**.
- Works with JSON and CSV; Python 3.10+; no runtime dependencies.
- Supports explicit field mapping for differently named CSV/JSON columns (v0.2.0).
- Compares question stems and option strings without discarding clinically significant symbols such as `<`, `>`, `+`, `-`, and decimal points.
- Rejects ambiguous CSV headers or nested A-E/5-choice input instead of silently dropping answers.
- Supports English and other Unicode text (including Arabic) for normalization.
- Separates blocking `error`s from non-blocking `warning`s.
- Supports human-readable output and JSON reports for downstream review.
- MIT licensed, with synthetic examples only.

**Latest source version: v0.3.1.** Its [release will be available here](https://github.com/hossamkadasi/surgcore-mcq-validator/releases/tag/v0.3.1) after GitHub CI verifies the patch and publishes the wheel and offline ZIP.

## Browser preview (no Python installation)

**[Open the live browser demo](https://validator.surgcorepro.com/)** — the standalone Cloudflare Pages deployment is online and was independently loaded and exercised in a browser on 2026-10-29. Valid synthetic sample: 2 records, 0 errors. Intentionally invalid sample: 3 records, 2 errors, 1 warning. Files are processed inside the browser; selected MCQ files are not sent to an application server. Alternative [Pages](https://surgcore-mcq-demo.pages.dev/) and [workers.dev](https://surgcore-mcq-validator-demo.hossamalkadasi.workers.dev/) mirrors and a [downloadable offline ZIP](https://github.com/hossamkadasi/surgcore-mcq-validator/archive/refs/heads/main.zip) are also available.

A local-only, dependency-free **browser demo** is included in [demo/index.html](demo/index.html). Download the repository ZIP, extract it and open that HTML file in a modern browser. Try the built-in synthetic samples, check CSV/JSON files with optional column mapping, and download a JSON report without uploading questions to a server. [Preview instructions and limitations](docs/BROWSER_DEMO.md).

**Saved reports:** You may reselect a downloaded `surgcore-validation-report.json` in the browser. The page will display its **previous findings** (without rerunning MCQ checks); select the original MCQ file to run a new validation. The file picker has English and Arabic guidance.

The preview does not run the Python CLI's heuristic near-duplicate scan and does not verify medical answers. The demo is hosted independently from SurgCore Pro production.

## Quick start

**New here?** Follow the [5-minute pilot guide](docs/PILOT_TESTING.md) using artificial data; no account, API key, or sensitive question bank is required. [Report feedback](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1) using a synthetic reproduction.


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

To export a JSON report (the output file must not exist yet):

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.json --format json --output reports/qa.json
```

Existing reports are never overwritten unless you add `--overwrite`. Even with that flag, the input file and optional mapping file can **never** be used as output targets. Reports are saved atomically to reduce partial writes.

Warnings can block CI or import gates if desired:

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.csv --fail-on warning
```

### Custom input column names (v0.2.0)

If your file uses different headers, use an explicit mapping. The source column names below are **synthetic**, not private exam material:

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/custom_schema.csv --mapping examples/column_mapping.json
```

The mapping JSON maps canonical names (`id`, `stem`, `option_a`, `option_b`, `option_c`, `option_d`, `answer`, `explanation`, `source`) to the corresponding source keys. Unmapped fields retain standard aliases. All four options remain mandatory and the validator rejects five-option JSON objects/lists rather than truncating them.

Use `--no-near-duplicates` to disable the optional fuzzy-stem check or `--similarity 0.95` to adjust its sensitivity (allowed range: 0.80-1.00).

## Drop-in GitHub Action

Other repositories can run the same structural checks on each pull request with a [reusable composite GitHub Action](action.yml), without writing validation scripts.

```yaml
name: MCQ QA
on: [pull_request]
permissions:
  contents: read
jobs:
  questions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          persist-credentials: false
      - uses: hossamkadasi/surgcore-mcq-validator@dc5df8bd19a18c88dc19e78a98f8fc4cbe8f39c7
        with:
          file: path/to/your-authorized-bank.csv
          fail-on: warning
```

This example is pinned to a **reviewed full Git commit SHA** for reproducible usage; update it only after reviewing a newer revision. Use the [mapping input](docs/GITHUB_ACTIONS_INTEGRATION.md) for custom schemas. CI execution occurs on the runner chosen by the downstream repository; do not run private question data on public CI runners or expose identifiers in public logs.

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
| Error | `duplicate_option` | Two options match after case/whitespace and superficial punctuation normalization (clinical operators and decimals are preserved) |
| Error | `missing_answer`, `invalid_answer` | No answer or label outside A-D |
| Error | `duplicate_stem` | Stems match after case/punctuation/space normalization |
| Warning | `short_stem` | Stem is unusually short |
| Warning | `missing_explanation`, `missing_source` | Missing educational rationale or provenance |
| Warning | `near_duplicate_stem` | A *heuristic*, not semantic, near-match was found |

Near-duplicate scanning preserves ordered numeric/operator tokens; changes to clinical thresholds or comparison operators are not flagged as near duplicates. This can miss real duplicates with altered numbers, by design. It uses overlapping three-word shingles to select candidates, then character-sequence similarity. It may **miss paraphrases** and may flag false positives, especially for templated questions. Always review flags manually.

JSON reports include issue location, stable code, severity, related record (when present), and summary counts. `schema_valid_record_count` counts rows with no **structural errors**; it is **not** a medically reviewed or publication-ready count.

### Exit codes

- `0`: no issues meeting the failure policy (`--fail-on error` by default).
- `1`: one or more issues meet the failure policy.
- `2`: invalid input, unsupported format, ambiguous columns, file error, or invalid threshold.

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

- Optional multi-file batch reports for heterogeneous banks.
- Human-in-the-loop review bundles for near duplicates.
- Verified opt-in CI integration for external question banks; [example workflow](docs/GITHUB_ACTIONS_INTEGRATION.md) (this repository's own test workflow already runs).
- User-supplied clinical evidence metadata checks (without claiming factual verification).

We welcome reports of reproducible bugs, test cases based on synthetic data, and contributions. The [pilot guide](docs/PILOT_TESTING.md) explains how to give actionable feedback without exposing private data. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [community-validation feedback issue](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1).

## License

MIT, see [LICENSE](LICENSE). Maintained by the SurgCore open-source community.
