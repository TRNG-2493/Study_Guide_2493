"""Fast checks on the catalog itself: no browser, runs in milliseconds.
(Wednesday: data-driven test design, exception testing.)"""
import pytest

from locator_catalog.catalog import CATALOG, PAGES, TECHNIQUES, CatalogRow, get_row, rows_for

pytestmark = pytest.mark.data


# ---- provided example ----
def test_names_are_unique():
    names = [r.name for r in CATALOG]
    duplicates = sorted({n for n in names if names.count(n) > 1})
    assert not duplicates, f"duplicate row names: {duplicates}"


# ---- TODO (Task 3): replace each pytest.fail with a real check and a helpful message ----
def test_catalog_has_at_least_16_rows():
    pytest.fail("TODO: at least 16 rows")


def test_every_page_is_covered():
    pytest.fail("TODO: all of PAGES used; at least 4 'login' rows and 8 'inventory' rows")


def test_css_and_xpath_are_never_empty_or_identical():
    pytest.fail("TODO: both present, and different from each other, for every row")


def test_xpath_looks_like_xpath():
    pytest.fail("TODO: every xpath starts with // or (//  (list the offending row names in the message)")


def test_at_least_7_different_techniques_are_used():
    pytest.fail("TODO: len({r.technique for r in CATALOG}) >= 7; message says which techniques are still unused")


def test_at_least_3_rows_check_text():
    pytest.fail("TODO: at least 3 rows have expected_text")


def test_stability_ranking_is_consistent_with_technique():
    pytest.fail("TODO: pseudo-position rows must be rank 7; rows whose technique is data-test must be rank 1")


def test_fragile_rows_explain_themselves():
    pytest.fail("TODO: every row with stability >= 6 has a `why` of at least 20 characters")


# ---- TODO (Task 5): exception testing ----
def test_get_row_returns_the_row():
    pytest.fail("TODO: get_row('login_logo').page == 'login'")


def test_get_row_unknown_name_raises_keyerror_with_known_names():
    pytest.fail("TODO: use pytest.raises(KeyError, match=...)")


@pytest.mark.parametrize(
    "overrides, message",
    [
        # TODO: five cases: a bad page, a bad technique, expected=0, stability=9,
        # expected=3 together with an expected_text.  Give each case an id.
    ],
)
def test_bad_rows_are_rejected(overrides, message):
    fields = dict(name="x", page="login", css=".a", xpath="//a", expected=1,
                  technique="tag-class", stability=5, why="valid example row for testing")
    fields.update(overrides)
    with pytest.raises(ValueError, match=message):
        CatalogRow(**fields)
