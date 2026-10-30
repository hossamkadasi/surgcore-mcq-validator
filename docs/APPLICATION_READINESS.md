# Codex for Open Source — application readiness

This is a **truthful preparation record**, not a submitted application or an OpenAI eligibility decision.

## Confirmed, public, reproducible evidence

- Repository: https://github.com/hossamkadasi/surgcore-mcq-validator (public, MIT).
- GitHub maintainer: `hossamkadasi` (repository owner and writer).
- Official GitHub Release: [v0.3.0](https://github.com/hossamkadasi/surgcore-mcq-validator/releases/tag/v0.3.0) — published 2026-10-30, with a browser ZIP and installable Python wheel. GitHub API verified that both assets were uploaded and the release tag points to commit `d099c694a02498c6736876e4c1d0c191b0c8b5fb`.
- 61 Python tests on each of Python 3.10 and 3.13, 20 JavaScript tests, 2 composite-action fixtures, and the release publication job all passed in [GitHub Actions run #41110543998](https://github.com/hossamkadasi/surgcore-mcq-validator/actions/runs/41110543998).
- Public demo: https://surgcore-mcq-demo.pages.dev/ — validated as accessible with successful synthetic interaction tests on 2026-10-29. This is technical QA, **not** external adoption evidence.
- Synthetic CLI examples, [a five-minute external tester guide](PILOT_TESTING.md), public contribution instructions and a feedback request: https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1
- Software tests **only structural MCQ quality**; it does not independently establish medical answer correctness.

## Current application-ready responses (each under 500 characters)

**Why does this repository qualify?**

> I am the primary maintainer of SurgCore MCQ Validator, an MIT-licensed tool for privacy-preserving structural QA of educational MCQ banks. It offers an offline Python CLI, zero-install browser demo, and reusable GitHub Action. CI passes 61 Python tests on 3.10/3.13, 20 JavaScript tests, and two action fixtures. It addresses a need in medical education; this is a new project with no verified external adoption yet.

**How will you use API credits?**

> Use Codex/API credits for pull-request review, issue triage, synthetic regression-test generation, and security-focused documentation for the open-source MCQ validator. All submitted examples will be synthetic or expressly authorized. Patient data, licensed exam papers, production question banks, and credentials will not be uploaded.

**Anything else we should know?**

> The browser demo at https://surgcore-mcq-demo.pages.dev/ is public and was tested successfully. The project checks data structure, not clinical answer accuracy. Its maintainer also works on a separate surgical education app; no proprietary app source or questions are in this repository.

All text describes actual published functionality and verified tests, **not** external users or an awarded benefit. The form also asks for private personal details: first/last name, ChatGPT account email and OpenAI Organization ID. Enter those privately on the official form, not in GitHub.

## Outstanding evidence

- External maintainers or third-party users: **not verified**.
- Real downloads, integrations and impact: **not verified**.
- Sustained issue triage, external PR reviews, and multiple independent releases: **not yet established**. The first formal GitHub Release is verified, but does not show third-party adoption.
- Integration into SurgCore Pro production: **not verified**; production remains unchanged.

OpenAI's program values meaningful use, broad adoption, or clear ecosystem importance and active maintenance. A green CI build and a newly created repository are not substitutes for those signals. We should not describe an unproven deployment, downloads or adoption as established facts.

## Proposed application wording (under 500 characters)

> I maintain SurgCore MCQ Validator, an MIT-licensed offline Python tool for structural quality checks in educational MCQ banks. It detects malformed answers, duplicate items, and import mapping errors without uploading private question data. Its test suite passes on Python 3.10 and 3.13. This is an early-stage project; external adoption is not yet established. I plan to maintain it for educators and developers working with privacy-sensitive question banks.

## Suggested use for any granted API credits

> Support PR reviews, regression-test generation from synthetic examples, issue triage and release documentation for the open-source validator. No patient data, confidential exams, copyrighted question banks or production secrets would be uploaded.

The applicant must enter the **email associated with their ChatGPT account** and **OpenAI Organization ID** privately into the official form; these should not be committed to the public repository.

Official program: https://openai.com/form/codex-for-oss/
