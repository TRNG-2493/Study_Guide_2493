"""Task 2 (SOLUTION): automated axe scan as pytest tests (marker: a11y)."""
import json
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe

from a11y_helpers import STATES, open_state, page  # noqa: F401  (page is a fixture)

REPORTS = Path(__file__).resolve().parents[2] / "reports" / "a11y"
BASELINE = Path(__file__).with_name("baseline.json")

# Rules we expect on the BAD page; contrast/alt need product cards so they vary by state.
ALWAYS = {"html-has-lang", "document-title", "landmark-one-main", "page-has-heading-one",
          "region", "label", "image-alt"}   # image-alt: the hero banner is always present
WITH_PRODUCTS = ALWAYS | {"color-contrast"}


def scan(page):
    return Axe().run(page).response["violations"]


def save_report(name, violations):
    REPORTS.mkdir(parents=True, exist_ok=True)
    slim = [{"id": v["id"], "impact": v["impact"], "help": v["help"], "helpUrl": v["helpUrl"],
             "nodes": [{"target": n["target"], "html": n["html"][:120]} for n in v["nodes"]]} for v in violations]
    (REPORTS / f"{name}.json").write_text(json.dumps(slim, indent=2))


def counts(violations):
    return {v["id"]: len(v["nodes"]) for v in violations}


def new_vs_baseline(violations, baseline):
    """Return {rule: (found, allowed)} for rules that are new or have MORE nodes than the baseline."""
    return {rid: (n, baseline.get(rid, 0)) for rid, n in counts(violations).items() if n > baseline.get(rid, 0)}


@pytest.mark.a11y
@pytest.mark.parametrize("state", STATES)
def test_bad_page_has_known_violations(page, state):
    open_state(page, "bad", state)
    violations = scan(page)
    save_report(f"bad-{state}", violations)
    ids = {v["id"] for v in violations}
    expected = WITH_PRODUCTS if state != "api-down" else ALWAYS
    assert ids == expected
    if state == "api-down":
        assert "color-contrast" not in ids          # no price cells rendered
    # What axe can NOT see (manual-only defects), asserted so the claim stays honest:
    assert "button-name" not in ids and "keyboard" not in " ".join(ids)
    assert all(v["impact"] and v["nodes"] for v in violations)


@pytest.mark.a11y
def test_no_new_violations_vs_baseline(page):
    """Baseline = known issues the team accepts for now. Anything new or worse fails the build."""
    open_state(page, "bad", "loaded")
    baseline = json.loads(BASELINE.read_text())
    assert new_vs_baseline(scan(page), baseline) == {}


@pytest.mark.a11y
def test_baseline_catches_a_regression(page):
    open_state(page, "bad", "loaded")
    page.evaluate("document.body.insertAdjacentHTML('beforeend', '<img src=\"img/placeholder.svg\">')")
    baseline = json.loads(BASELINE.read_text())
    assert new_vs_baseline(scan(page), baseline) == {"image-alt": (7, 6), "region": (11, 10)}


@pytest.mark.a11y
@pytest.mark.parametrize("state", STATES)
def test_fixed_page_has_zero_violations(page, state):
    open_state(page, "fixed", state)
    violations = scan(page)
    save_report(f"fixed-{state}", violations)
    assert violations == []


@pytest.mark.a11y
def test_before_after_counts(page):
    summary = {}
    for variant in ("bad", "fixed"):
        open_state(page, variant, "loaded")
        v = scan(page)
        summary[variant] = {"rules": len(v), "nodes": sum(len(x["nodes"]) for x in v)}
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "summary.json").write_text(json.dumps(summary, indent=2))
    assert summary["bad"] == {"rules": 8, "nodes": 26}
    assert summary["fixed"] == {"rules": 0, "nodes": 0}
