"""Tests for qe_utils.usernames (CSV data source). Read the SPECIFICATION in src/qe_utils/usernames.py first."""
import pytest
from helpers.assertions import assert_valid_username
from helpers.data_loader import load_csv_cases
from qe_utils.usernames import is_valid_username, normalize_username


@pytest.mark.smoke
@pytest.mark.parametrize("username, expected", load_csv_cases("username_cases.csv"))
def test_is_valid_username_from_csv(username, expected):
    """CSV-driven validity check. (SKIPPED until you finish load_csv_cases in Task 3b.)"""
    assert is_valid_username(username) is expected


def test_normalize_username_strips_and_lowercases():
    """TODO Task 5b: assert normalize_username('  Ana_QA ') == 'ana_qa'; add a TypeError test for 123 and None."""
    pytest.fail("TODO Task 5b")


def test_known_good_username_passes_custom_assertion():
    """TODO Task 4a: use assert_valid_username('ana_qa') once you have implemented it."""
    pytest.fail("TODO Task 4a")


def test_custom_assertion_message_explains_why():
    """TODO Task 4c: prove your helper's MESSAGE is useful.
    Call assert_valid_username('9lives') inside `with pytest.raises(AssertionError, match=...)`
    and match a word from your 'starts with a letter' message."""
    pytest.fail("TODO Task 4c")
