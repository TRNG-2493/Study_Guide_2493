"""
Tuesday lab - STARTER. Every test below fails with "TODO" until you implement it.

Run:   pytest -v                 (all tests)
       pytest -v -k test_1a      (one test)
       pytest -x -v              (stop at the first failure)

Rules of the lab
  * Only Monday + Tuesday material. Plain functions only: no fixtures, no conftest.py, no Page Objects, no JSON data files.
  * No time.sleep() / page.wait_for_timeout(). Wait for conditions with expect(...), wait_for_url, expect_popup, etc.
  * Prefer role / label / text locators. Never use positional selectors like tr[3]/td[2].
  * `open_page()` (from support.py) gives you a fresh headless Page; relative URLs such as "/orders" work.
  * Stretch tests are marked skip. Remove the @pytest.mark.skip line when you start one.
"""

import csv
import re
import tempfile
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import expect

from support import open_page


def todo(msg: str):
    raise NotImplementedError(f"TODO: {msg}")


# ----------------------------------------------------------------------------------------------
# Helper functions (plain functions - NOT Page Objects). Implement them as you meet them in the tasks.
# ----------------------------------------------------------------------------------------------

def read_visible_rows(page) -> list[dict]:
    """Task 1a. Rows on the CURRENT page of #orders as dicts keyed by header text, WITHOUT the 'Actions' column.
    Example: {'Order': '1001', 'Customer': 'Maria Lopez', 'Total': '10.50', 'Status': 'Paid'}"""
    todo("read_visible_rows (Web tables, Concept 4: turn a table into data)")


def collect_all_rows(page, max_pages=10) -> list[dict]:
    """Task 1a. Click Next until it is disabled and return the rows of every page, in order.
    Wait for the page to CHANGE after each click (Web tables, Concept 8 and demo Appendix A, item 2)."""
    todo("collect_all_rows (Web tables, Concept 8: pagination)")


def download_orders_csv(page, folder: Path) -> list[dict]:
    """Task 1a / 6. Click 'Export CSV', save the download into `folder`, return the parsed rows (list of dicts).
    Also assert the suggested filename is 'orders.csv'."""
    todo("download_orders_csv (File upload and download, Concepts 7-8)")


def accept_terms(page) -> None:
    """Task 3 / 7. Open the Terms tab from /checkout, click 'I agree' (the tab closes itself),
    then assert the opener shows 'Terms: accepted'."""
    todo("accept_terms (Multiple tabs and windows, Concepts 3 and 9)")


def pay_in_frames(page, card="4242 4242 4242 4242", otp="123456") -> None:
    """Task 2 / 7. In the 'Secure card payment' iframe enter the card and click Continue; then in the
    'Bank verification' iframe (nested INSIDE the first one, added ~0.5 s later) enter the code and approve."""
    todo("pay_in_frames (Frames and nested frames, Concept 5)")


# ----------------------------------------------------------------------------------------------
# Task 1 - Web tables  (page: /orders)
# ----------------------------------------------------------------------------------------------

def test_1a_table_matches_export():
    with open_page() as page, tempfile.TemporaryDirectory() as tmp:
        page.goto("/orders")
        # TODO 1: gate on the table having rendered: assert exactly 5 body rows (no sleeping).
        # TODO 2: use collect_all_rows(page) -> assert 12 rows and 12 DISTINCT order numbers.
        # TODO 3: reload /orders (fresh state), use download_orders_csv(page, Path(tmp)).
        # TODO 4: assert the UI rows == the CSV rows (the file is your independent oracle).
        # TODO 5: compute in PYTHON the number of Pending orders and their total with Decimal (not float),
        #         then assert #summary shows exactly "<n> pending orders, total <amount>".
        todo("Task 1a")


def test_1b_sorting():
    with open_page() as page:
        page.goto("/orders")
        # TODO 1: click the 'Customer' column header (found by ROLE columnheader). Assert aria-sort == ascending.
        # TODO 2: collect all 12 customers across pages; assert they equal sorted(..., key=str.lower).
        # TODO 3: click the 'Total' header twice -> descending. Assert aria-sort, then that the totals (as floats!)
        #         equal sorted(..., reverse=True) and that the largest is 40.0.
        todo("Task 1b")


def test_1c_search_and_row_action():
    with open_page() as page:
        page.goto("/orders")
        # TODO 1: search "ann". Assert 2 rows are shown AND every row text contains "ann" (non-empty AND all-match).
        # TODO 2: show that filter(has_text="Ann") matches 2 rows, but a row filtered by an EXACT cell "Ann Lee" matches 1.
        # TODO 3: with a guard (count == 1) click Refund in Ann Lee's row only. Assert that row now shows "Refunded"
        #         and no longer has a Refund button.
        # TODO 4: search "zzz" and assert the 'No orders found' message.
        todo("Task 1c")


# ----------------------------------------------------------------------------------------------
# Task 2 - Frames and nested frames  (page: /checkout)
# ----------------------------------------------------------------------------------------------

def test_2_nested_frames_payment():
    with open_page() as page:
        page.goto("/checkout")
        # TODO 1: prove a page-level locator cannot see 'Card number' (count == 0).
        # TODO 2: negative path: card "1234" + Continue -> the alert 'Invalid card number' appears INSIDE the iframe.
        # TODO 3: use pay_in_frames(page, otp="000000") -> the bank iframe shows 'Wrong code'
        #         and the main page still says 'Payment: not started'.
        # TODO 4: enter the right code (123456) and approve -> the card iframe says 'Verified card ending 4242'
        #         and the MAIN page says 'Payment: approved' (no "switch back" call is needed).
        todo("Task 2")


# ----------------------------------------------------------------------------------------------
# Task 3 - Multi-tab / popup flow  (page: /checkout)
# ----------------------------------------------------------------------------------------------

def test_3_terms_tab_and_popups():
    with open_page() as page:
        page.goto("/checkout")
        # TODO 1: assert the Terms link has target="_blank" and the context has exactly 1 page.
        # TODO 2: click 'Help' (a window.open popup), capture it, assert its heading 'Help centre',
        #         assert the opener's 'Checkout' heading is still visible and the context has 2 pages. Close the popup.
        # TODO 3: use accept_terms(page). Assert 'Place order' is STILL disabled and only 1 page remains open.
        # TODO 4: click the same-tab link 'View orders' WITHOUT expect_popup; wait for the /orders URL.
        todo("Task 3")


# ----------------------------------------------------------------------------------------------
# Task 4 - Date picker  (page: /delivery)
# ----------------------------------------------------------------------------------------------

def pick_delivery_date(page, target: date) -> None:
    """Task 4. Open the 'Delivery date' calendar, move forward/backward by month arithmetic, click the day by its
    accessible name (e.g. 'June 20, 2025'; use exact=True), and assert the calendar closes."""
    todo("pick_delivery_date (Date pickers, Concept 4 and Example 3)")


def test_4_date_pickers():
    with open_page() as page:
        # TODO 1: freeze the browser clock at 2025-03-14 10:00 BEFORE page.goto("/delivery"); assert '#today'.
        page.goto("/delivery")
        # TODO 2: native input 'Invoice date': fill with the ISO value 2025-02-28, assert value and the confirmation text.
        #         Negative: filling "2025-02-30" must raise an error containing "Malformed value".
        # TODO 3: pick_delivery_date(page, date(2025, 6, 20)) then date(2025, 4, 2) (backwards); assert value and '#chosen'.
        # TODO 4: reopen the calendar, go to March 2025, assert March 13 is DISABLED and March 14 is ENABLED.
        todo("Task 4")


# ----------------------------------------------------------------------------------------------
# Task 5 - Shadow DOM  (page: /components)
# ----------------------------------------------------------------------------------------------

def test_5_shadow_dom_cards():
    with open_page() as page:
        page.goto("/components")
        # TODO 1: show the boundary: document.querySelector('button.ship') evaluated in the browser is None,
        #         page.locator('button.ship') counts 3, and an XPath '//button' counts 0.
        # TODO 2: scope by the HOST: click 'Mark shipped' on Ann Lee's card only. Assert her status is 'Shipped'
        #         and Chen Wei's card still says 'Processing'.
        todo("Task 5")


# ----------------------------------------------------------------------------------------------
# Task 6 - File download + upload round trip  (pages: /orders then /import)
# ----------------------------------------------------------------------------------------------

def test_6_export_then_import_round_trip():
    with open_page() as page, tempfile.TemporaryDirectory() as tmp:
        page.goto("/orders")
        # TODO 1: download the CSV with download_orders_csv; assert it has 12 rows. Remember the saved file path.
        page.goto("/import")
        # TODO 2: upload that saved file via set_input_files on the 'Orders CSV' input. Register the response wait FIRST,
        #         assert HTTP 200 and the UI message 'Imported 12 orders from orders.csv'.
        # TODO 3: negative: upload an IN-MEMORY file (name malware.exe, any bytes). The input says accept=".csv" but the
        #         SERVER must reject it: assert HTTP 415 and the message 'Rejected: only .csv files are accepted'.
        todo("Task 6")


# ----------------------------------------------------------------------------------------------
# Task 7 - Project 1 milestone: one end-to-end flow  (page: /checkout)
# ----------------------------------------------------------------------------------------------

def test_7_milestone_checkout_end_to_end():
    with open_page() as page:
        page.goto("/checkout")
        # TODO 1: 'Place order' starts disabled.
        # TODO 2: accept_terms(page) -> still disabled (payment missing).
        # TODO 3: pay_in_frames(page) -> 'Payment: approved' and the button becomes enabled.
        # TODO 4: click it with the network response registered first: assert HTTP 201, read the order id from the JSON,
        #         and assert the UI shows 'Order confirmed: <that id>'.
        todo("Task 7")


# ----------------------------------------------------------------------------------------------
# Stretch tasks (optional; remove the skip marker when you start one)
# ----------------------------------------------------------------------------------------------

@pytest.mark.skip(reason="stretch S1")
def test_s1_closed_shadow_root():
    """The <audit-badge> on /components has a CLOSED shadow root.
    (a) Show host.shadowRoot is None and a locator inside finds 0 elements; click the HOST to run the audit
        and assert '#audit-out' == 'Audited'.
    (b) New page: use add_init_script to force attachShadow to mode 'open' BEFORE goto, then click the real button by role."""
    todo("S1")


@pytest.mark.skip(reason="stretch S2")
def test_s2_file_chooser():
    """On /import the 'Pick file...' button creates a file input on demand. Use expect_file_chooser (register first),
    assert chooser.is_multiple() is False, set an in-memory two-row CSV and assert 'Imported 2 orders from two.csv'."""
    todo("S2")


@pytest.mark.skip(reason="stretch S3")
def test_s3_ctrl_click_background_tab():
    """Ctrl/Cmd+Click the Terms link on /checkout. Capture the background tab with context.expect_page().
    New pages start at about:blank, so assert its URL with expect(...).to_have_url, do not read .url immediately."""
    todo("S3")


@pytest.mark.skip(reason="stretch S4")
def test_s4_bad_header_rejected():
    """Upload an in-memory 'wrong.csv' whose first line is 'id,name'. Assert HTTP 422 and 'Rejected: unexpected header'."""
    todo("S4")
