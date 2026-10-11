"""Integration script: uses the whole library. Run with: python3 demo_report.py"""
from test_utils.generators import generate_test_cases
from test_utils.helpers import sort_cases, slowest, count_by
from test_utils.decorators import timer


@timer
def build_demo_report(count=6, seed=7):
    """Return a multi-line report string (assume count >= 1).

    Line 1: 'TEST DATA REPORT'
    Line 2: 'Total: <count>'
    Line 3: 'Slowest: <id> (<duration:.2f> s)'
    Line 4: 'By priority: High=2, Low=1, Medium=3'   (priority names in alphabetical order)
    Then one line per case, slowest first: '<id> | <priority> | <status> | <duration:.2f> s'
    """
    # TODO (Milestone 5): cases = generate_test_cases(count, seed=seed); use slowest(), count_by(),
    #   sorted(counts) for the alphabetical priority names, and sort_cases(..., reverse=True).
    #   Build a list `lines`, then return "\n".join(lines).
    pass


if __name__ == "__main__":
    print(build_demo_report())
