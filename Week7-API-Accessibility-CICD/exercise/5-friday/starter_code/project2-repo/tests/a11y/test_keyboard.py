"""Stretch (SOLUTION): automate what axe cannot see. Bad page proves the defect; fixed page proves the fix."""
import pytest

from a11y_helpers import open_state, page  # noqa: F401  (page is a fixture)


def tab_ids(page, n):
    seen = []
    for _ in range(n):
        page.keyboard.press("Tab")
        seen.append(page.evaluate("document.activeElement.id || document.activeElement.className"))
    return seen


@pytest.mark.a11y
@pytest.mark.parametrize("variant,trapped", [("bad", True), ("fixed", False)])
def test_promo_field_keyboard_trap(page, variant, trapped):          # WCAG 2.1.2
    open_state(page, variant, "loaded")
    page.focus("#promo")
    for _ in range(3):
        page.keyboard.press("Tab")
    still = page.evaluate("document.activeElement.id") == "promo"
    assert still is trapped


@pytest.mark.a11y
@pytest.mark.parametrize("variant,operable", [("bad", False), ("fixed", True)])
def test_add_to_cart_keyboard_operable(page, variant, operable):    # WCAG 2.1.1 / 4.1.2
    open_state(page, variant, "loaded")
    page.focus("#search")
    reached = False
    for _ in range(12):
        page.keyboard.press("Tab")
        if page.evaluate("document.activeElement.classList.contains('add-btn')"):
            reached = True
            break
    assert reached is operable
    if operable:
        page.keyboard.press("Enter")
        assert page.inner_text("#cart-count") == "1"


@pytest.mark.a11y
@pytest.mark.parametrize("variant,visible", [("bad", False), ("fixed", True)])
def test_focus_is_visible(page, variant, visible):                   # WCAG 2.4.7
    open_state(page, variant, "loaded")
    page.focus("#search")
    style = page.evaluate("(()=>{const s=getComputedStyle(document.activeElement);return [s.outlineStyle,parseFloat(s.outlineWidth)]})()")
    assert (style[0] != "none" and style[1] >= 2) is visible


@pytest.mark.a11y
@pytest.mark.parametrize("variant,announced", [("bad", False), ("fixed", True)])
def test_form_error_is_announced(page, variant, announced):         # WCAG 3.3.1 / 4.1.3
    open_state(page, variant, "form-error")
    live = page.evaluate("""(()=>{const e=document.getElementById('email-error');
        return !!e.closest('[role=alert],[role=status],[aria-live]')})()""")
    assert live is announced
    invalid = page.evaluate("document.getElementById('email').getAttribute('aria-invalid')") == "true"
    assert invalid is announced
