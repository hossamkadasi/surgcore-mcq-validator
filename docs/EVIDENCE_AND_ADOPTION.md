# Evidence and adoption record

**Important:** This document reports what is independently reproducible from public code and GitHub CI, not claims of third-party adoption.

## Verified implementation evidence

- Open-source repository uses an MIT license; source and tests are publicly inspectable.
- A fixed synthetic example is validated on each automated CI run.
- Regression tests cover JSON/CSV parsing, invalid answer labels, duplicate stems/options/IDs, field mapping, and malformed input.
- Official review and CI checks are structural only; **they do not certify medical correctness**.

## Verified GitHub CI results (2026-10-29)

- [v0.2.0 commit](https://github.com/hossamkadasi/surgcore-mcq-validator/commit/6969545e7a5405b269225fdf455ba0705ef9ff9c).
- [GitHub Actions run #40910419913](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40910419913): **success** on Python 3.10 and 3.13.
- GitHub job logs independently confirmed **50 passing unit tests per Python version**, plus validation of both the ordinary and custom-mapped synthetic examples.
- [Community feedback request](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1) is an invitation, **not** proof of external engagement.

## Adoption status at initial publication (2026-10-29)

- Public GitHub repository was newly created on 2026-10-29.
- No independent third-party contributors or adoption have yet been confirmed. Check public GitHub metrics at application time; do not present unverified counts.
- No independent third-party downloads or integrations have been verified.
- Use in the production SurgCore Pro application has **not** been established.

## What can become verifiable evidence

1. User-submitted bug reports from authorized, *synthetic* fixtures.
2. Reviewed external pull requests and maintainer triage.
3. Explicitly permissioned integration descriptions from independent projects.
4. Public releases and CI runs, with links and date-stamped evidence.
5. Private usage counts only with permitted aggregation and clear methodology; never publish private question content.

OpenAI's Codex for Open Source program evaluates actual usage, broader importance and maintainer activity. This project may be useful but passing CI or opening Issues is **not** evidence of adoption or approval.
