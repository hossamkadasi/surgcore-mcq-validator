# Maintainer plan

This is a planning document, not evidence of adoption or eligibility for any external program.

## Verified milestones

- 2026-10-29: Published an MIT-licensed repository with a runnable CLI and artificial samples.
- 2026-10-29: GitHub Actions tests succeeded on Python 3.10 and 3.13 ([first successful run](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40899999185)).
- 2026-10-29: Published v0.2.0 data-mapping and malformed-input safeguards; [GitHub CI passed](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40910419913) on Python 3.10 and 3.13 with 50 tests each.

- 2026-10-29: Merged [PR #2](https://github.com/hossamkadasi/surgcore-mcq-validator/pull/2) fixing clinical-threshold duplicate matching and report-output safety. [GitHub Actions main run](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40930922609) passed, with 61 unit tests on Python 3.10 and 3.13.

## Near-term maintenance goals

- Invite genuine feedback and bug reports based on synthetic or permissioned datasets.
- Document actual external adoption and reviewed pull requests with public URLs.
- Publish formal GitHub releases after CI passes; a version string alone is not a release.
- Independently test private/question-bank integration without uploading any proprietary data.

## Evidence to collect before applying to a maintainer program

- Public repository URL and maintainer write permissions.
- Verified release history and reproducible tests.
- Real-world usage examples, with explicit permission and without publishing private content.
- Actual stars/forks/contributor/download metrics (never fabricated).
- Public issue triage, PR reviews and sustained maintenance activity.

Creating a repository and passing tests does **not** automatically establish significance, adoption, or qualification for the Codex for Open Source program. Applications are reviewed by OpenAI, and grant selection is discretionary.
