"""Playwright architecture: one Browser, many isolated BrowserContexts. (Thursday written lesson, Ex. 4)"""
import pytest

from locator_catalog import config, pages

pytestmark = pytest.mark.smoke


def test_contexts_do_not_share_a_session(site_browser):
    # TODO (Task 7): prove that sessions are isolated BETWEEN contexts but shared INSIDE one.
    #   1. context_a = site_browser.new_context(); context_b = site_browser.new_context()
    #   2. log in on a page of context A (pages.open_login, pages.login)
    #   3. open config.INVENTORY_URL in a SECOND page of context A and in a page of context B
    #   4. assert: A's second tab sees 6 products; B sees 0 products and 1 login button
    #   5. close both contexts, even if an assert fails (try/finally)
    pytest.fail("TODO Task 7: context isolation")
