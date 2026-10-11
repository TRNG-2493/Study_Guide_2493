"""STRETCH tasks (optional). Each test is skipped until you delete its `pytest.skip(...)` line."""
import pytest
from playwright.sync_api import Page, expect


def open_form(page: Page) -> None:
    page.goto("/")
    expect(page.get_by_role("heading", name="QE Summit 2026 - Registration")).to_be_visible()


def test_s1_validation_errors_show_no_dialog(page: Page):
    pytest.skip("STRETCH S1 - remove this line to attempt")
    # TODO: with a page.on("dialog") listener that records types, tick the terms and click Register on an EMPTY form.
    # TODO: assert the three error messages in #errors li (one assertion, a list) and #status.
    # TODO: assert NO dialog was raised (validation happens before any confirm).


def test_s2_donation_slider_with_keyboard(page: Page):
    pytest.skip("STRETCH S2 - remove this line to attempt")
    # TODO: focus the slider; press ArrowRight 3 times -> aria-valuenow "15"; End -> "100"; Home -> "0".  [KBM s3]


def test_s3_promo_is_case_insensitive_and_escape_removes_it(page: Page):
    pytest.skip("STRETCH S3 - remove this line to attempt")
    # TODO: VIP ticket, promo "qe2026" + Enter -> total "$400.00"; press Escape in the promo field -> empty, total "$500.00".


def test_s4_city_autosuggest_edge_cases(page: Page):
    pytest.skip("STRETCH S4 - remove this line to attempt")
    # TODO: one char shows no list; "zz" shows "No results" which is NOT an option (count 0); "TO" matches
    #       Toronto + Tokyo (case-insensitive); Escape closes the list but keeps the typed text.   [SUG s9]


def test_s5_price_matrix_with_a_loop(page: Page):
    pytest.skip("STRETCH S5 - remove this line to attempt")
    # TODO: loop over (ticket, expected total) pairs with a plain for-loop; then add Gala + Parking on VIP and assert the sum.


def test_s6_two_dialogs_in_a_row_with_one_handler(page: Page):
    pytest.skip("STRETCH S6 - remove this line to attempt")
    # TODO: ONE page.on handler that answers a prompt with text and a confirm with accept (branch on dialog.type);
    #       trigger the dietary prompt then Reset; assert both outcomes and the order of the recorded dialog types.
