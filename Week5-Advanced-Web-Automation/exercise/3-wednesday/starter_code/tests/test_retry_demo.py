"""Task 6 helper (PROVIDED): a simulated flaky test.  Skipped by default (marker retry_demo).

Attempt 1 raises TimeoutError (an "infrastructure" style failure), attempt 2 passes.
execution_count is supplied by pytest-rerunfailures.  Run it with:
    pytest -m retry_demo -v -rR
"""
import pytest


@pytest.mark.retry_demo
@pytest.mark.flaky(reruns=2, reruns_delay=0, only_rerun="TimeoutError")
def test_flaky_passes_on_second_attempt(request):
    if request.node.execution_count < 2:
        raise TimeoutError("simulated slow environment (attempt 1)")
