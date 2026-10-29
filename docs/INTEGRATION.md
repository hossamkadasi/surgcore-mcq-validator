# Integration notes for educational applications

The validator can be run as an offline pre-import check. It is not coupled to SurgCore Pro; other open-source or private quiz applications may reuse it under the MIT license.

1. Prepare a **local, authorized** CSV or JSON export with synthetic or approved educational data. Do not copy private production data into a public repository.
2. Run `surgcore-mcq-validator validate bank.csv --format json --output reports/check.json`.
3. If the exit status is `2`, fix input format or file access; for exit `1`, review issues with severity `error`.
4. Optionally run with `--fail-on warning` to require manual handling of missing explanations, references and suspected duplicates.
5. Human reviewers verify answer accuracy, clinical evidence, licensing, figures and provenance before any import/publishing decision.
6. Keep a separate acceptance log for human-approved content; this tool does not create medical approval records.

## Example machine-readable fields

`summary.record_count`, `summary.schema_valid_record_count`, `summary.error_count`, `summary.warning_count`, `summary.passed_structural_checks`, and `issues[]` (each with `code`, `severity`, `record_index`, `question_id`, `message`, possibly `related_record_index` or `similarity`).

## Limitations

Exact duplicate checks are punctuation/case insensitive, which may occasionally coalesce questions that need distinct contexts. Fuzzy duplicates are heuristic and may miss reworded or translated questions. Large banks with repetitive phrasing may have lower fuzzy recall due to candidate-blocking limits. The result is **quality triage**, not an import approval or a medical certification.
