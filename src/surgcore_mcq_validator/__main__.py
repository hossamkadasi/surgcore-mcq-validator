"""Allow `python -m surgcore_mcq_validator ...`."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
