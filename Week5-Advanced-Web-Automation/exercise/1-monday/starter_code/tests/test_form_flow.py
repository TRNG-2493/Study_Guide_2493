"""Week 5 / Monday - Complex form flow (STARTER).

How to work:
  1. Open the app yourself first:  python serve.py   ->  http://127.0.0.1:8765/   (explore every control)
  2. Pick the next failing test below, read its TODO steps, implement them, then delete the
     `pytest.fail(...)` line. Run just that test:   pytest -k test_01 --headed --slowmo 400
  3. Work top to bottom (stages 1 -> 6). Every action is followed by an assertion; no time.sleep().

Lesson tags in hints:  [DLG] alerts-dialogs-and-pop-ups   [CHK] radio-buttons-and-checkboxes
                       [DDN] dropdowns-and-multi-selects  [KBM] keyboard-and-mouse-actions
                       [SUG] auto-suggestions            ("s6" = section 6 of "The Concept")
"""
import pytest
from playwright.sync_api import Page, expect


def open_form(page: Page) -> None:
    """Open the registration form served by the local helper (base_url is provided by conftest.py)."""
    page.goto("/")
    expect(page.get_by_role("heading", name="QE Summit 2026 - Registration")).to_be_visible()


# ---------------------------------------------------------------------------
# Stage 0 - Worked example (passes already: read it, it shows the style we want)
# ---------------------------------------------------------------------------
def test_00_worked_example_form_loads_in_a_clean_state(page: Page):
    open_form(page)
    expect(page).to_have_title("QE Summit Registration")
    expect(page.locator("#total")).to_have_text("$0.00")
    expect(page.get_by_role("button", name="Register")).to_be_disabled()


# ---------------------------------------------------------------------------
# Stage 1 - Dialogs  [DLG]   (3 dialog types: alert, prompt, confirm)
# ---------------------------------------------------------------------------
def test_01_help_button_shows_alert(page: Page):
    open_form(page)
    # TODO 1: create a list `seen_dialogs` and a function `dialog_handler(dialog)` that records
    #         (dialog.type, dialog.message) and then ANSWERS the dialog.   Hint: [DLG s8], Example 4
    # TODO 2: register the handler with page.once("dialog", ...) BEFORE the click.   Hint: [DLG s5, s6]
    # TODO 3: click the "Need help?" button.
    # TODO 4: assert seen_dialogs == [("alert", "<the exact message>")]. Read the real text in the browser first.
    pytest.fail("TODO: implement test_01_help_button_shows_alert")


def test_02_dietary_prompt_accept_with_text(page: Page):
    open_form(page)
    # TODO: "Add dietary request" opens a prompt. Accept it with the text "Vegetarian, no nuts".   Hint: [DLG s7]
    # TODO: assert #dietary-status shows "Dietary request: Vegetarian, no nuts".
    # TODO: assert the dialog type is "prompt" and capture its message too.
    pytest.fail("TODO: implement test_02_dietary_prompt_accept_with_text")


def test_03_dietary_prompt_cancel_is_not_empty_text(page: Page):
    open_form(page)
    # TODO: click "Add dietary request" and DISMISS the prompt -> #dietary-status must say "Dietary request cancelled".
    # TODO: click again, ACCEPT with an empty string -> status must say "No dietary request".
    #       Two different outcomes for Cancel vs OK-with-nothing.   Hint: [DLG s7] last paragraph
    pytest.fail("TODO: implement test_03_dietary_prompt_cancel_is_not_empty_text")


def test_04_reset_dismiss_keeps_the_data(page: Page):
    open_form(page)
    # TODO: fill "Full name" and check the "Workshop" ticket radio.
    # TODO: register a handler that records the dialog and DISMISSES it; click "Reset form".
    # TODO: assert #status == "Reset cancelled", the name and radio are unchanged,
    #       and the recorded dialog is a ("confirm", "<exact text>").
    pytest.fail("TODO: implement test_04_reset_dismiss_keeps_the_data")


def test_05_reset_accept_clears_the_form(page: Page):
    open_form(page)
    # TODO: fill the name, check Workshop, check Lunch. Assert the total shown in #total (see the price tooltip for prices).
    # TODO: ACCEPT the reset confirm.
    # TODO: assert #status == "Form cleared", name empty, radio and checkbox unchecked, total back to "$0.00".
    pytest.fail("TODO: implement test_05_reset_accept_clears_the_form")


# ---------------------------------------------------------------------------
# Stage 2 - Radios and checkboxes with conditional enabling  [CHK]
# ---------------------------------------------------------------------------
def test_06_initial_state_rules(page: Page):
    open_form(page)
    # TODO: assert NO ticket radio is checked (hint: a `:checked` locator + to_have_count(0), [CHK s5]).
    # TODO: assert "I accept the terms" is NOT pre-ticked.
    # TODO: assert Lunch is enabled, "Workshop kit" and "Gala dinner" are disabled.   Hint: [CHK s7]
    pytest.fail("TODO: implement test_06_initial_state_rules")


def test_07_ticket_type_controls_the_add_ons(page: Page):
    open_form(page)
    # Rules (explore the form to confirm): kit needs Workshop or VIP; gala needs VIP; changing the ticket
    # to something that no longer allows an add-on UNTICKS it.
    # TODO: Standard  -> kit and gala disabled.
    # TODO: Workshop  -> kit enabled, gala disabled; check kit; assert #total.
    # TODO: VIP       -> gala enabled; check gala; assert #total.
    # TODO: back to Standard -> assert VIP radio is no longer checked (radio group!), kit and gala are
    #       disabled AND unchecked, total is "$100.00".
    # Use check() (state), never click().   Hint: [CHK s2, s3, s6]
    pytest.fail("TODO: implement test_07_ticket_type_controls_the_add_ons")


def test_08_terms_enable_the_register_button(page: Page):
    open_form(page)
    # TODO: Register is disabled. check() the terms box TWICE (idempotent) -> still checked, Register enabled.
    # TODO: uncheck() it -> Register disabled again.   Hint: [CHK s2, s3, s7]
    pytest.fail("TODO: implement test_08_terms_enable_the_register_button")


# ---------------------------------------------------------------------------
# Stage 3 - Dropdowns  [DDN]
# ---------------------------------------------------------------------------
def test_09_tshirt_native_select_three_ways(page: Page):
    open_form(page)
    # TODO: assert the list of option texts of "T-shirt size" in ONE assertion (placeholder included).   Hint: [DDN s6]
    # TODO: assert the default value is "" (placeholder).
    # TODO: select "M" by value=, "Extra Large" by label=, and the 3rd option after the placeholder by index=.
    #       After each, assert with expect(...).to_have_value(...).   Hint: [DDN s2, s5]
    pytest.fail("TODO: implement test_09_tshirt_native_select_three_ways")


def test_10_sessions_multi_select_replaces_and_clears(page: Page):
    open_form(page)
    # TODO: select "basics" and "api" together; assert with to_have_values([...]).   Hint: [DDN s3]
    # TODO: select only "ai" -> assert the selection was REPLACED, not added to.
    # TODO: clear the selection with an empty list; assert nothing is selected.
    pytest.fail("TODO: implement test_10_sessions_multi_select_replaces_and_clears")


def test_11_country_custom_dropdown_open_then_click(page: Page):
    open_form(page)
    # The Country control is NOT a <select>, so select_option() will not work.   Hint: [DDN s8]
    # TODO: locate the combobox named "Country". Click it to open; assert aria-expanded == "true".
    # TODO: assert the four options (India, Canada, Germany, United States). SCOPE your locator to
    #       "#country-list": there are other role=option elements on this page (native <option>s).
    # TODO: click "Canada"; assert the combobox now shows "Canada" and aria-expanded == "false".
    pytest.fail("TODO: implement test_11_country_custom_dropdown_open_then_click")


# ---------------------------------------------------------------------------
# Stage 4 - Keyboard and mouse  [KBM]
# ---------------------------------------------------------------------------
def test_12_promo_code_applied_with_enter_key(page: Page):
    open_form(page)
    # TODO: check the Workshop ticket (total "$250.00").
    # TODO: fill "Promo code" with WRONG and press the Enter KEY (key names are case-sensitive, [KBM s3]).
    #       Assert #promo-msg == "Invalid promo code" and the total is unchanged.
    # TODO: fill QE2026 - assert nothing was applied yet (typing alone does not apply it) - then press Enter.
    #       Assert the success message and the discounted total (20% off).
    pytest.fail("TODO: implement test_12_promo_code_applied_with_enter_key")


def test_13_price_tooltip_appears_on_hover(page: Page):
    open_form(page)
    # TODO: assert #price-tooltip is hidden BEFORE you hover (before-state).   Hint: [KBM s6]
    # TODO: hover the "Ticket price info" badge; assert the tooltip is visible and its text lists the three prices.
    pytest.fail("TODO: implement test_13_price_tooltip_appears_on_hover")


def test_14_donation_slider_drag_with_low_level_mouse(page: Page):
    open_form(page)
    # The slider only moves while the mouse button is held AND the pointer moves.
    # TODO: get the slider handle (role "slider") and the "#donation-track" element.
    # TODO: read the track's bounding_box(); assert it is not None; compute the x/y of 50 % of the track.   Hint: [KBM s7]
    # TODO: handle.hover(); page.mouse.down(); page.mouse.move(x, y, steps=15); page.mouse.up()   Hint: [KBM s8]
    # TODO: assert #donation-value is "50", the handle's aria-valuenow is "50", and #total is "$50.00".
    pytest.fail("TODO: implement test_14_donation_slider_drag_with_low_level_mouse")


# ---------------------------------------------------------------------------
# Stage 5 - Autosuggest  [SUG]
# ---------------------------------------------------------------------------
def test_15_city_fill_does_not_trigger_suggestions(page: Page):
    open_form(page)
    # TODO: fill() "Ha" into the City combobox. Assert the value is "Ha" and that "#city-list" stays hidden
    #       (use a short timeout: we expect NOTHING to happen).   Hint: [SUG s3], [KBM s2]
    pytest.fail("TODO: implement test_15_city_fill_does_not_trigger_suggestions")


def test_16_city_type_wait_for_content_and_click(page: Page):
    open_form(page)
    # TODO: type "Ha" with press_sequentially(..., delay=80).
    # TODO: define `suggestions` = the options INSIDE "#city-list" only (a native <option> also has role=option!).
    # TODO: synchronise on CONTENT: expect(suggestions).to_have_text([...two cities...]). No sleeps.   Hint: [SUG s4]
    # TODO: click the second city by its text; assert the field value and aria-expanded == "false".   Hint: [SUG s6]
    pytest.fail("TODO: implement test_16_city_type_wait_for_content_and_click")


def test_17_city_keyboard_selection(page: Page):
    open_form(page)
    # TODO: type "De", wait for the suggestions, press ArrowDown twice.
    # TODO: assert the highlighted option (get_by_role("option", selected=True), scoped to the list) is the 2nd city.
    # TODO: press Enter; assert the field value is that city.   Hint: [SUG s7, s8]
    pytest.fail("TODO: implement test_17_city_keyboard_selection")


# ---------------------------------------------------------------------------
# Stage 6 - End-to-end flow (everything together)
# ---------------------------------------------------------------------------
def test_18_full_registration_flow(page: Page):
    open_form(page)
    # Fill the form in this order, asserting as you go:
    # TODO 1  Full name "Asha Rao", Email "asha.rao@example.com".
    # TODO 2  Ticket Workshop; add-ons Lunch + Workshop kit.
    # TODO 3  T-shirt "Medium"; Sessions basics + api; Country Canada (custom dropdown); City "Hy" -> Hyderabad (autosuggest).
    # TODO 4  Promo qe2026 + Enter; drag donation to 50; dietary prompt "Vegan".
    # TODO 5  Assert #total == "$290.00"   (hint: promo applies to ticket + add-ons only, not to the donation).
    # TODO 6  Register is disabled until the terms are accepted; accept them.
    # TODO 7  NEGATIVE path first: click Register, DISMISS the confirm. Assert #status "Registration cancelled",
    #         #receipt hidden, and the name still filled in.
    # TODO 8  HAPPY path: click Register again. This flow shows TWO dialogs in a row (a confirm, then an alert),
    #         so one page.once will NOT be enough. Use ONE page.on handler that records and accepts both,
    #         and remove it in a finally block.   Hint: [DLG s5] "a flow may open several dialogs in a row"
    # TODO 9  Assert the status, the recorded dialogs (types + exact messages), and every #r-* field of the receipt.
    pytest.fail("TODO: implement test_18_full_registration_flow")
