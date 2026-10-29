# Private, local-only browser demo

This folder contains an independent, dependency-free **browser preview** for nontechnical educators and MCQ authors. It provides a subset of the structural checks offered by the Python CLI.

## Run without installation

Open [demo/index.html](../demo/index.html) in any modern browser after downloading and extracting this repository. No local server, web API, Python, account, or internet connection is required to run the downloaded demo.

The browser preview:

- Processes selected **CSV or JSON files in browser memory only**.
- Supports custom column mappings and downloads a JSON report to the user's device.
- Checks IDs, stems, four choices, answer labels, missing explanations/sources, and exact duplicates.
- Ships with synthetic success and failure examples for a 30-second test.
- Uses local JavaScript and CSS, with no third-party scripts, analytics, remote fonts, or API calls.
- Enforces a restrictive Content-Security-Policy that disallows outgoing connections.

**Important:** The preview does **not** perform the Python CLI's **heuristic near-duplicate detection**, which is computationally heavier. Numeric comparison and threshold symbols are preserved during exact-match checks. It does **not** verify medical answer correctness.

Browser limits: 5 MiB and 5,000 question records. The Python CLI remains the recommended integration for large files and CI pipelines.

## Run automated browser-engine tests

With Node.js 20+:

```bash
node --test demo/tests/browser-validator.test.cjs
```

## Hosted demo

**[Open the live browser demo](https://surgcore-mcq-demo.pages.dev/)**. A dedicated Cloudflare Pages project `surgcore-mcq-demo` is connected to this repository, with `main` as its production branch and `demo` as its static output directory. Cloudflare reported deployment success (deployment ID `f0d1c5c9-b5c0-4a6b-9678-be4c256ddbfd`) on 2026-10-29 UTC.

An independent browser load returned HTTP 200, and interactive testing confirmed:

- Valid synthetic sample: 2 checked, 2 structurally valid, 0 errors, 0 warnings.
- Intentionally flagged sample: 3 checked, 2 structurally valid, 2 errors and 1 warning.
- Both `duplicate_stem` and `invalid_answer` appeared in the flagged sample.

These are **maintainer-run verification tests**, not user adoption metrics. If the Pages URL is inaccessible on your network, an [alternative Cloudflare Worker host](https://surgcore-mcq-validator-demo.hossamalkadasi.workers.dev/) or local ZIP download can be used. The Workers mirror was not part of the independent browser verification described above.

Cloudflare sees HTTP requests for static HTML/JS/CSS and may log client IP addresses; **selected question files are handled entirely in browser memory**, with no remote upload endpoints.

## Reporting and privacy

Use [Issue #1](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1) for reproducible reports based only on artificial examples. Never publish proprietary MCQs, patient information, clinical reports, login credentials, or copyrighted books.

JSON reports can contain question IDs and quality metadata; treat them as confidential when using private banks.
