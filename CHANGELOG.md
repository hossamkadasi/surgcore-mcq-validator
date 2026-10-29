# Changelog

## 0.2.0 — 2026-10-29

- Added optional column mapping for CSV and JSON input (`--mapping`) and an example mapping file.
- Preserves clinically relevant comparison, sign and decimal symbols in answer-option duplicate checks.
- Rejects ambiguous duplicate/empty CSV headers, excess CSV fields and lossy JSON option shapes.
- Adds unit/CLI regression tests; no medical fact-checking claims.
- Offline-only operation; no changes to SurgCore Pro production infrastructure.

## 0.1.0 (initial development snapshot)

- Local CSV and JSON loader with flexible option representations.
- Structural MCQ validation and duplicate detection.
- JSON and human-readable reports with standard exit codes.
- Unit tests and synthetic data samples.

Note: this is a development snapshot and not a claim of a published GitHub release or adoption.
