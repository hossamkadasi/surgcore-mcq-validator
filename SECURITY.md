# Security and privacy

This tool reads local CSV/JSON files and writes an optional local report. It is intentionally offline and does not require an API key, browser session, external model, or remote account.

## Supported security boundary

- Input files are processed locally. Do not use a shared/public runner with confidential question banks.
- Avoid placing patient data, copyrighted exam text, credentials, or secret data into public issues or test fixtures.
- A JSON output report may contain portions of question identifiers and issue messages; treat reports as sensitive when inputs are sensitive.
- Maximum input size: 25 MiB. No claim is made that every possible malicious file or resource-exhaustion scenario is mitigated.
- The tool does not execute embedded content from input rows.

## Reporting vulnerabilities

Please open a GitHub issue for non-sensitive reproducible bugs using synthetic data. For sensitive findings, contact the repository maintainer through GitHub profile channels; do not post exploit payloads, private data or secrets publicly.

## Medical limitation

This tool does not detect incorrect answers, unsafe medical advice, out-of-date recommendations, plagiarism, licensing conflicts, or improperly sourced questions. Human medical and editorial verification is required before publishing educational/clinical material.
