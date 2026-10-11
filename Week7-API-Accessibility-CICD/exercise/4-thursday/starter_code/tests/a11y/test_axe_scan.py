"""Task 2: automated axe scan as pytest tests (marker: a11y).

Fixture `page` and helpers `open_state`, `STATES` (all in a11y_helpers.py) are provided.
"""
import pytest

from a11y_helpers import STATES, open_state, page  # noqa: F401  (page is a fixture)

# from axe_playwright_python.sync_playwright import Axe   # TODO: used by scan()


def scan(page):
    """TODO 1: run axe on the CURRENT page and return the list of violations
    (hint: Axe().run(page).response["violations"]). Every violation has
    id, impact, help, helpUrl, nodes[]."""
    raise NotImplementedError


def save_report(name, violations):
    """TODO 2: write violations as JSON to reports/a11y/<name>.json (create the folder if needed)."""
    raise NotImplementedError


@pytest.mark.a11y
@pytest.mark.parametrize("state", ["loaded", "form-error", "api-down"])
def test_bad_page_has_known_violations(page, state):
    pytest.skip("TODO 3: open_state(page, 'bad', state); scan; save_report; assert the rule ids you expect "
                "for THIS state (e.g. image-alt, label, color-contrast ...). Which rules differ per state?")


@pytest.mark.a11y
def test_no_new_violations_vs_baseline(page):
    pytest.skip("TODO 4: load tests/a11y/baseline.json ({rule_id: max_node_count}); scan the 'bad' page in "
                "state 'loaded'; fail if a rule is missing from the baseline or has MORE nodes than allowed.")


@pytest.mark.a11y
def test_baseline_catches_a_regression(page):
    pytest.skip("TODO 5: open the bad page, inject a NEW violation with page.evaluate (e.g. append an <img> "
                "without alt), and prove the baseline comparison from TODO 4 reports it.")


@pytest.mark.a11y
@pytest.mark.parametrize("state", ["loaded", "form-error", "api-down"])
def test_fixed_page_has_zero_violations(page, state):
    pytest.skip("TODO 6 (task 4): after you create storefront_fixed/, scan it in every state; assert [].")


@pytest.mark.a11y
def test_before_after_counts(page):
    pytest.skip("TODO 7 (task 4): count nodes before (bad) and after (fixed), write reports/a11y/summary.json, "
                "assert after < before.")
