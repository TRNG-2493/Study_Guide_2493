"""Performance diagnostics (lesson: performance-profiling.md)."""
import time

import pytest
from qe_utils.shipping import shipping_cost


def test_pretend_slow_dependency():
    """Sleeps 0.4 s so something shows up at the top of --durations (WORKED EXAMPLE; no change needed
    except registering the `slow` marker and adding @pytest.mark.slow in Task 1/7)."""
    time.sleep(0.4)


def test_shipping_cost_stays_within_budget():
    """TODO Task 7: time 10,000 calls of shipping_cost(2, 'local') with time.perf_counter().
    Assert the total is under 1.0 second and make the failure message print the measured time."""
    pytest.fail("TODO Task 7")
