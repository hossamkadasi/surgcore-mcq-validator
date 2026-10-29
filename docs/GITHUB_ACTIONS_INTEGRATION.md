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
