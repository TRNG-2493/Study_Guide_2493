"""Project 1 - QE Foundations: UI milestone TEMPLATE (Week 5 Monday).

ASSUMPTION: the application under test for Project 1 is chosen by you/your instructor. This
template is therefore app-neutral: copy it into your Project 1 repository (e.g. tests/ui/),
rename it, set P1_BASE_URL, and replace every `# TODO` with locators for YOUR app's main form flow.
Until P1_BASE_URL is set the tests skip, so this file never breaks your repo's test run.

    set P1_BASE_URL=https://your-app.example      (Windows)   |   export P1_BASE_URL=...   (macOS/Linux)
    pytest tests/ui/test_p1_form_flow.py --headed --slowmo 400
"""
import os

import pytest
from playwright.sync_api import Page, expect

BASE = os.environ.get("P1_BASE_URL")
pytestmark = pytest.mark.skipif(not BASE, reason="Set P1_BASE_URL to your Project 1 app to run these tests")


def open_flow(page: Page) -> None:
    page.goto(BASE)          # TODO: go to the page that holds the main form flow (login? registration? checkout?)


def test_p1_form_flow_happy_path(page: Page):
    open_flow(page)
    # TODO: fill text inputs; check()/select the radio + checkbox controls the form really has.
    # TODO: use select_option for native <select>; open-then-click for a custom dropdown (if any).
    # TODO: use press_sequentially + expect(...to_have_text) for any autosuggest/typeahead (if any).
    # TODO: if the app uses a native alert/confirm/prompt, register a dialog handler BEFORE the click and assert its message.
    # TODO: submit and assert the final outcome (success message / data shown / URL change).


def test_p1_form_flow_negative_path(page: Page):
    open_flow(page)
    # TODO: submit with a required field empty or a rule broken; assert the specific validation message.


def test_p1_conditional_rule(page: Page):
    open_flow(page)
    # TODO: assert one "control X is disabled/hidden until Y" rule BEFORE and AFTER satisfying it.
