"""Verify the product-page rows of the catalog: count AND (where given) the text."""
import pytest

from locator_catalog.assertions import assert_locator_count, assert_locator_text
from tests.params import catalog_params

pytestmark = [pytest.mark.catalog, pytest.mark.inventory]


# TODO (Task 4): write test_inventory_css and test_inventory_xpath, parametrized over
# catalog_params("inventory"), using the inventory_page fixture and your two assertion helpers.
# Copy the shape of test_login_css in test_catalog_login.py.
@pytest.mark.css
@pytest.mark.parametrize("row", catalog_params("inventory"))
def test_inventory_css(inventory_page, row):
    pytest.fail("TODO Task 4: verify row.css (count + text)")


@pytest.mark.xpath
@pytest.mark.parametrize("row", catalog_params("inventory"))
def test_inventory_xpath(inventory_page, row):
    pytest.fail("TODO Task 4: verify row.xpath (count + text)")
