# Changelog

## 0.3.1 — 2026-10-30

- Allow users to **open previously downloaded JSON reports** in the browser and review earlier issues without revalidating them.
- Add bilingual report-vs-question-bank guidance and an explicit saved-report status; prevent accidental revalidation of a report.
- Validate saved-report structure, cap visible findings at 200 for mobile responsiveness, and preserve safe text-only rendering.
- Improve the Python CLI's error message when a report is mistakenly supplied as input.
- Add browser, Python and CLI regression tests. No changes to clinical correctness claims.


## 0.3.0 — 2026-10-30

- Added the independent local-only browser preview, hosted on Cloudflare Pages, with CSV/JSON processing, sample questions, issue review, and local JSON report downloads.
- Added 20 Node.js regression tests for the browser data-validation engine and a reusable composite GitHub Action for other projects.
- Added 2 GitHub Action synthetic smoke fixtures, pilot onboarding, strict browser security headers, and automated public-demo checks.
- Preserved prior v0.2.1 safeguards against unsafe output-file overwrite and losing clinical threshold operators during duplicate screening.
- Added formal, CI-gated GitHub release artifacts and documentation. A release is only considered published after its GitHub Release page is verified.


## 0.2.1 — 2026-10-29

- Prevent clinical inequalities, numeric thresholds, dose and percent symbols from being erased during question-stem duplicate detection.
- Suppress heuristic near-duplicate flags where the ordered clinical numeric/operator tokens differ.
- Prevent `--output` from overwriting the input file or mapping file, even when `--overwrite` is requested.
- Require an explicit `--overwrite` flag to replace an existing report; write reports atomically.
- Add focused regression tests for both safety issues.


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
