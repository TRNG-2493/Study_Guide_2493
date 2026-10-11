"""Driver: build a Suite from sample rows and print every report format."""
from report_system import Suite, TextReporter, CsvReporter, TestResult

SAMPLE_ROWS = [
    {"test_id": "TC-001", "status": "PASS", "duration": 1.2},
    {"test_id": "TC-002", "status": "FAIL", "duration": 3.4, "message": "Timeout, retry failed"},
    {"test_id": "TC-003", "status": "pass", "duration": 0.8},
    {"test_id": "TC-004", "status": "SKIPPED"},
]
# Rows that SHOULD be rejected (bad id, bad status, negative duration).
BAD_ROWS = [
    {"test_id": "XX-9", "status": "PASS"},
    {"test_id": "TC-005", "status": "PSAS"},
    {"test_id": "TC-006", "status": "PASS", "duration": -1},
]


def main():
    # TODO 4.1: create Suite("Login") and add a TestResult.from_dict(row) for every
    #           row in SAMPLE_ROWS.
    # TODO 4.2: for every row in BAD_ROWS, try to add it. Catch (ValueError, TypeError)
    #           and print "Rejected <test_id>: <error message>".
    # TODO 4.3: put TextReporter(suite) and CsvReporter(suite) in ONE list, loop over
    #           it and print reporter.render() (same call, different output).
    # TODO 4.4: print "Results created:" and TestResult.how_many().
    print("run_report.py: TODO, nothing implemented yet")


if __name__ == "__main__":
    main()
