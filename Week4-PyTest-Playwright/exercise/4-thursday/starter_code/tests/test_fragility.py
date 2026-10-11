"""STRETCH S1: prove that position-based selectors are fragile.

Create site/practice_page_reordered.html yourself: copy site/practice_page.html and move ONE
whole product card (the Backpack) to a different position inside the <template>.
Then show: a name-anchored row still works, a position-based row breaks.
"""
import pytest

from locator_catalog import config

pytestmark = [pytest.mark.stretch, pytest.mark.skipif(config.SITE == "live", reason="uses the offline reordered copy")]


def test_identity_based_row_survives_reordering():
    pytest.skip("STRETCH S1: not started")


def test_position_based_row_breaks_after_reordering():
    pytest.skip("STRETCH S1: not started")
