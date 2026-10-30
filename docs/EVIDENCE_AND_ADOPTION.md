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

- [v0.2.1 safe-report and threshold fix](https://github.com/hossamkadasi/surgcore-mcq-validator/pull/2) was merged into `main` after passing GitHub Actions tests.
- [GitHub Actions main-branch run #40930922609](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40930922609): **success** on Python 3.10 and Python 3.13 with 61 unit tests in the reviewed change.
- [Pilot tester instructions](PILOT_TESTING.md) are published; publishing instructions does **not** demonstrate that anyone has used them.

## Browser trial distribution (2026-10-30)

- [Public demo address](https://surgcore-mcq-validator-demo.hossamalkadasi.workers.dev/) backed by a dedicated Cloudflare Worker; Cloudflare API shows 100% deployment and enabled subdomain. The live URL was **not independently HTTP-loaded** from the current execution environment.
- Node.js CI [run #40957177430](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40957177430) passed 20 synthetic tests; Python 3.10 and 3.13 jobs also succeeded.
- This is **distribution readiness**, not evidence of independent users. Obtain genuine tester feedback at [Issue #1](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1).

## Verified public browser demo (2026-10-29)

- Dedicated project: [surgcore-mcq-demo.pages.dev](https://surgcore-mcq-demo.pages.dev/) running a GitHub-linked Cloudflare Pages deployment of `demo/`.
- Cloudflare deployment ID `f0d1c5c9-b5c0-4a6b-9678-be4c256ddbfd` reports **success**.
- External live page retrieval returned HTTP **200** and the expected title and interface.
- Interactive synthetic sample QA in an independent browser: **valid sample 2/2, zero errors/warnings**; intentionally flagged sample **3 records, 2 errors, 1 warning** with `duplicate_stem` and `invalid_answer`.
- These interactions were performed during maintenance QA. They **do not represent independent external adoption**.

## Reusable GitHub Action verification (2026-10-29)

- [PR #6](https://github.com/hossamkadasi/surgcore-mcq-validator/pull/6) added the composite `action.yml` and was merged after all checks passed.
- [Main-branch CI run #40963511292](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/40963511292): **success** on Python 3.10 and 3.13, JavaScript browser tests, and the reusable Action smoke job.
- Action smoke job validated **two synthetic CSV fixtures**: standard headers (2 records, no errors/warnings) and custom mapping (1 record, no errors/warnings).
- The reusable Action is published and can be consumed by other repositories through its pinned SHA. **No independent downstream adoption is claimed.**

## Dedicated custom hostname and external availability (2026-10-30)

- The public preview was additionally mapped to [validator.surgcorepro.com](https://validator.surgcorepro.com/) on the existing dedicated `surgcore-mcq-validator-demo` Cloudflare Worker.
- Cloudflare Worker Domain API returned `enabled=true`, `service=surgcore-mcq-validator-demo`, and an automatically generated proxied AAAA record for `validator.surgcorepro.com`. No pre-existing conflicting DNS record or Worker domain was found.
- Cloudflare Browser Rendering successfully loaded the homepage and the three essential assets (`validator.js`, `app.js`, and `styles.css`) over HTTPS from the new hostname on 2026-10-30.
- This is **not proof of availability on every network**. A separate GitHub Actions smoke workflow now checks the custom hostname from a GitHub runner; any local ISP/DNS issue must still be confirmed by an actual affected user.
- The host is a separate subdomain; existing Cloudflare routes for `surgcorepro.com` production were left unchanged.

## Formal GitHub Release (2026-10-30)

- [Official v0.3.0 release](https://github.com/hossamkadasi/surgcore-mcq-validator/releases/tag/v0.3.0) published 2026-10-30; public, non-draft, and non-prerelease.
- [Gated main-branch CI run #41110543998](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/41110543998) succeeded, including Python 3.10/3.13, browser JavaScript, two synthetic composite Action fixtures, and the release packaging and publication job.
- GitHub REST evidence confirmed two downloadable assets: `surgcore-mcq-browser-demo-v0.3.0.zip` (10,068 bytes) and `surgcore_mcq_validator-0.3.0-py3-none-any.whl` (15,716 bytes). Release tag points to main commit `d099c694a02498c6736876e4c1d0c191b0c8b5fb`.
- The first snapshot of public asset download counters was **zero** immediately after publication. Do not infer external adoption from those counts or from internal QA downloads.

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
