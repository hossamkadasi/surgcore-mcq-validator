# Five-minute open-source pilot for educators and developers

**Goal:** Validate that SurgCore MCQ Validator works for your use case, and share *genuine* feedback. This is not a clinical content certification or a request for real medical exam papers.

## 1. Run it locally

Prerequisites: Python 3.10 or newer and Git.

On macOS or Linux:

```bash
git clone https://github.com/hossamkadasi/surgcore-mcq-validator.git
cd surgcore-mcq-validator
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.csv
```

On Windows PowerShell:

```powershell
git clone https://github.com/hossamkadasi/surgcore-mcq-validator.git
cd surgcore-mcq-validator
$env:PYTHONPATH="src"
python -m surgcore_mcq_validator validate examples/synthetic_questions.csv
```

Expected output for the *synthetic* CSV is **Records: 2, Errors: 0, Warnings: 0** with exit code 0. If the tool produces anything else, please report it.

No Git installed? On GitHub, select **Code > Download ZIP**, extract it, navigate to the extracted directory in a local terminal and run the Python command above.

## 2. Try the error-detection example

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/synthetic_questions.json
```

This synthetic JSON intentionally contains an invalid answer and a duplicate stem, so the tool exits with code 1. This is *expected* and is not a failed installation.

## 3. Optional custom-schema demo

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate examples/custom_schema.csv --mapping examples/column_mapping.json
```

Expected: one structurally valid record and no errors. The mapping file is a public synthetic demonstration, not a private question bank.

## 4. Optional authorized-bank validation

Only use data that you are legally allowed to process, and **keep it on your own machine**. This tool does not upload the contents. Example:

```bash
PYTHONPATH=src python -m surgcore_mcq_validator validate local-authorized-file.csv --format json --output local-report.json
```

Do not commit the input or output report to this repository; both may contain sensitive metadata. A report filename already in use will not be overwritten unless you explicitly use `--overwrite`. Input and mapping files cannot be overwritten even with that flag.

## 5. Give real feedback

Please add a comment to [Issue #1: Community validation](https://github.com/hossamkadasi/surgcore-mcq-validator/issues/1), using this structure:

- Operating system and Python version:
- CSV or JSON / optional mapping used:
- Expected behavior:
- Actual behavior:
- Was this reproducible using **artificial** example data?
- What change would make you use this in a real educational software workflow?

**Never** upload confidential exams, copyrighted books, real patient data, personal information, proprietary question banks, private screenshots, credentials, or production exports. Create an artificial *minimal reproduction* instead.

This project's maintainer will use genuine reproducible reports to prioritize fixes. Creating this pilot guide does not mean third-party users have run it. Contributions and external usage will be reported only after independently verifiable evidence exists.

**Limitations:** All checks are structural. No answer is medically fact-checked, no clinical guideline is consulted, and no medical content should be published without professional review.
