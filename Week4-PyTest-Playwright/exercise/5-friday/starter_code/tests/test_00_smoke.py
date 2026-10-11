"""PROVIDED and already passing. Run it first: if it fails, fix your setup before anything else."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.offline
def test_setup_works_and_site_opens(login_page: Page):
    expect(login_page).to_have_title("GadgetHub - Sign in")
    expect(login_page.get_by_role("button", name="Sign in")).to_be_visible()
