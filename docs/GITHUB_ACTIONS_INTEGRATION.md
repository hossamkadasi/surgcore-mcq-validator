# GitHub Actions integration for other repositories

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
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install pinned open-source validator
        run: python -m pip install 'git+https://github.com/hossamkadasi/surgcore-mcq-validator.git@ec3daac393a9d6ddc2cb389c8080343db665a4b7'
      - name: Block structurally invalid questions
        run: surgcore-mcq-validator validate path/to/your/authorized-bank.csv --fail-on warning
```

The commit pin above installs the known 0.1.0 version. After reviewing a newer version, replace it with that release's verified commit SHA. In private repositories, make sure logs and artifacts do not expose private content. The validator does not use any network APIs at runtime.
