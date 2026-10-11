r"""Command line entry point (PROVIDED; do not edit).

    Windows PowerShell :  python -m qe_foundations.ingestion data\ingestion\test_cases_messy.csv
    macOS / Linux      :  python3 -m qe_foundations.ingestion data/ingestion

Accepts one or more files and/or folders. Exit code 0 = every source was readable
(rejected RECORDS are reported but are not a failure); 1 = at least one source failed.
"""

import sys
from pathlib import Path

from .exceptions import SourceError
from .loader import load_directory, load_test_cases


def print_report(report):
    print(report.summary())
    for error in report.rejected:
        print(f"    rejected - {error}")


def main(argv):
    if not argv:
        print("usage: python -m qe_foundations.ingestion <file-or-folder> [...]")
        return 2

    exit_code = 0
    for argument in argv:
        path = Path(argument)
        try:
            if path.is_dir():
                batch = load_directory(path)
                for report in batch.reports:
                    print_report(report)
                for error in batch.failed_sources:
                    print(f"SOURCE FAILED - {error}")
                    exit_code = 1
                totals = batch.totals()
                print(f"TOTAL for {path.name}: {totals}")
            else:
                print_report(load_test_cases(path))
        except SourceError as error:
            print(f"SOURCE FAILED - {error}")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
