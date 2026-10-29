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

**[Open the public demo](https://surgcore-mcq-validator-demo.hossamalkadasi.workers.dev/)**. It is deployed to a dedicated Cloudflare Worker called `surgcore-mcq-validator-demo`, separate from the production SurgCore Pro application. Cloudflare API independently reports a successful script upload, an active 100% deployment, and an enabled `workers.dev` subdomain. Our environment could not perform an independent external HTTP load of the URL; testers should report any accessibility issues.

The static host may receive the visitor's IP when requesting the page and assets. The demo never uploads selected question files, sends analytics, or calls external APIs. If `workers.dev` cannot be reached, download the repository ZIP and open `demo/index.html` locally.

## Reporting and privacy

Use [Issue #1](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1) for reproducible reports based only on artificial examples. Never publish proprietary MCQs, patient information, clinical reports, login credentials, or copyrighted books.

JSON reports can contain question IDs and quality metadata; treat them as confidential when using private banks.
