# Contributing

Thank you for contributing to SurgCore MCQ Validator. The goal is a small, safe, dependable validator for educational question datasets.

1. Open an issue describing a reproducible defect or scoped enhancement. Check existing issues first.
2. Use synthetic question data only; never publish private exams, copyrighted question banks, patient information, tokens, or confidential code.
3. Create a branch and add tests for any behavior change.
4. Run `PYTHONPATH=src python -m unittest discover -s tests -v` and include the result in your pull request.
5. In your PR, explain impact on input formats, exit codes, and security/privacy considerations.

Code should remain understandable and dependency-light. Do not add an external AI or network service as an implicit dependency. If you propose medical-content verification, supply evidence and implement a clear human-review gate rather than describing a model's answer as medically verified.

The MIT license covers contributions to this repository. By contributing, you agree that your contributions may be distributed under that license. Be respectful in discussions and provide reproducible cases.
