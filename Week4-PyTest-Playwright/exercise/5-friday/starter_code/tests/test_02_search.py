"""Task 4: search (Project 1 milestone: scenario 3). The site's search is SLOW (600 ms) on purpose."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.offline
@pytest.mark.project1
def test_search_finds_matching_products(logged_in_page: Page):
    """P1 scenario 3 (manual case TC-UI-03): searching for 'usb' shows only the 2 USB-C products."""
    # TODO Act: fill the search box (get_by_role("searchbox", name=...) or get_by_placeholder).
    # TODO Assert (NO time.sleep, NO .count() snapshot right after typing!):
    #      - the card headings have count 2 (retrying assertion)
    #      - the headings' texts are exactly ["USB-C Hub", "USB-C Charger"] (to_have_text with a list)
    pytest.skip("TODO: implement test_search_finds_matching_products")


@pytest.mark.offline
def test_search_with_no_match_shows_message(logged_in_page: Page):
    """Negative search: 'zzz' -> message 'No gadgets match your search.' and zero cards."""
    # TODO: implement. Also assert the 'Searching...' status goes away (to_be_hidden).
    pytest.skip("TODO: implement test_search_with_no_match_shows_message")


@pytest.mark.offline
@pytest.mark.parametrize("term, expected_names", [])  # TODO (stretch-light): 3 search terms + expected cards
def test_search_terms_parametrized(logged_in_page: Page, term, expected_names):
    pytest.skip("TODO: implement test_search_terms_parametrized")
