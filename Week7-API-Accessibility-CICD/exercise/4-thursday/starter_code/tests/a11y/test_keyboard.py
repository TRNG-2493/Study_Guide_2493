"""Stretch: automate the keyboard findings from task 1 (marker: a11y).

Axe cannot see keyboard traps, div-buttons or missing focus styles. Playwright can.
"""
import pytest

from a11y_helpers import open_state, page  # noqa: F401  (page is a fixture)


@pytest.mark.a11y
def test_promo_field_is_a_keyboard_trap(page):
    pytest.skip("STRETCH: Tab into #promo, press Tab 3 more times, assert document.activeElement.id is still 'promo'.")


@pytest.mark.a11y
def test_add_to_cart_is_keyboard_operable(page):
    pytest.skip("STRETCH: Tab through the page; assert at least one .add-btn ever receives focus.")


@pytest.mark.a11y
def test_focus_is_visible(page):
    pytest.skip("STRETCH: focus #search; assert computed outline-style is not 'none'.")


@pytest.mark.a11y
def test_form_error_is_announced(page):
    pytest.skip("STRETCH: trigger the error; assert #email-error (or an ancestor) has role=alert or aria-live.")
