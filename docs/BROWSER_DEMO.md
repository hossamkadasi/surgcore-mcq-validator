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

## Public demo hosting

These are static files that can be hosted on GitHub Pages, Cloudflare Pages, or any static host. **The existence of a repository does not mean a public demo URL has been activated.** An owner must configure hosting; a hosted page can reveal a visitor's IP to the static host when loading HTML, JS and CSS, but selected question files are not uploaded.

## Reporting and privacy

Use [Issue #1](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1) for reproducible reports based only on artificial examples. Never publish proprietary MCQs, patient information, clinical reports, login credentials, or copyrighted books.

JSON reports can contain question IDs and quality metadata; treat them as confidential when using private banks.
