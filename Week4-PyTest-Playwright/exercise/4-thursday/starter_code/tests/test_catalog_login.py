"""Verify the login-page rows (and the 'after a bad login' rows) of the catalog."""
import pytest

from locator_catalog.assertions import assert_locator_count, assert_locator_text
from tests.params import catalog_params

pytestmark = [pytest.mark.catalog, pytest.mark.login]


# Worked example (provided): one parametrized test per language, so a CSS failure and an
# XPath failure show up as separate lines in the report.
@pytest.mark.css
@pytest.mark.parametrize("row", catalog_params("login"))
def test_login_css(login_page, row):
    assert_locator_count(login_page, row.css, row.expected, f"{row.name} CSS")
    if row.expected_text:
        assert_locator_text(login_page, row.css, row.expected_text, f"{row.name} CSS")


# TODO (Task 4): test_login_xpath  - same idea for row.xpath (remember the "xpath=" prefix!)
@pytest.mark.xpath
@pytest.mark.parametrize("row", catalog_params("login"))
def test_login_xpath(login_page, row):
    pytest.fail("TODO Task 4: verify row.xpath (count, and text when expected_text is set)")


# TODO (Task 4): test_error_css and test_error_xpath for the "login_error" rows (use the error_page fixture)
@pytest.mark.css
@pytest.mark.parametrize("row", catalog_params("login_error"))
def test_error_css(error_page, row):
    pytest.fail("TODO Task 4: verify row.css on the error page")


@pytest.mark.xpath
@pytest.mark.parametrize("row", catalog_params("login_error"))
def test_error_xpath(error_page, row):
    pytest.fail("TODO Task 4: verify row.xpath on the error page")
