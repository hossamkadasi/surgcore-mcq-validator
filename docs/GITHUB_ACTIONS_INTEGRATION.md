# GitHub Actions integration for other repositories

## Simplest option: composite GitHub Action

SurgCore MCQ Validator includes a reusable [root-level `action.yml`](../action.yml) that installs the package from the source of the action and runs it on files checked out by the calling repository.

```yaml
name: MCQ structure checks
on: [pull_request]
permissions:
  contents: read
jobs:
  mcq_quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          persist-credentials: false
      - uses: hossamkadasi/surgcore-mcq-validator@main
        with:
          file: data/authorized-questions.csv
          fail-on: warning
```

This unpinned example demonstrates syntax. **Pin a reviewed full commit SHA instead of `@main` for production workloads.** The action also accepts `mapping`, `similarity` and `no-near-duplicates` inputs.

Example custom mapping:

```yaml
      - uses: hossamkadasi/surgcore-mcq-validator@main
        with:
          file: data/authorized-questions.csv
          mapping: data/column-mapping.json
          fail-on: error
          no-near-duplicates: 'true'
```

**Privacy:** The validator itself does not upload data, but the calling CI runner already has access to the checked-out repository's files. Never put licensed exam papers or patient records in a public repository, and remember GitHub Actions logs may expose question identifiers in diagnostics.

## Alternative: install the pinned CLI directly


Check an **authorized** CSV file in a separate project without uploading the source data to SurgCore or a third-party API:

```yaml
name: MCQ checks
on: [pull_request]
permissions:
  contents: read
jobs:
  validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          persist-credentials: false
      - uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Install pinned open-source validator
        run: python -m pip install 'git+https://github.com/hossamkadasi/surgcore-mcq-validator.git@b42e4d50e763d96f1b390ce1a96c2045496d5e6c'
      - name: Block structurally invalid questions
        run: surgcore-mcq-validator validate path/to/your/authorized-bank.csv --fail-on warning
```

The commit pin above installs the verified 0.2.1 version. After reviewing a newer version, replace it with that release's verified commit SHA. In private repositories, make sure logs and artifacts do not expose private content. The validator does not use any network APIs at runtime.
