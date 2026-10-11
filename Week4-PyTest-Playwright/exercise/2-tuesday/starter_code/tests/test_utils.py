"""TASK 1 - Refactor target.

These are the kind of tests you wrote on Monday: they work, but every case is a copy-paste.
Your job: replace them with a SMALL number of @pytest.mark.parametrize tests (readable ids,
keep the markers) WITHOUT losing any case. See README Task 1 for the exact Definition of Done.

Do not delete a case unless you can explain why it was redundant.
"""
import pytest

from project1_utils import add, apply_discount, average, divide, is_even, is_palindrome, reverse_string


@pytest.mark.smoke
def test_add_positives():
    assert add(2, 3) == 5


@pytest.mark.smoke
def test_add_negatives():
    assert add(-2, -3) == -5


@pytest.mark.smoke
def test_add_zeros():
    assert add(0, 0) == 0


def test_add_cancel_out():
    assert add(-5, 5) == 0


def test_add_floats():
    assert add(1.5, 2.5) == 4.0


def test_is_even_zero():
    assert is_even(0) is True


def test_is_even_one():
    assert is_even(1) is False


def test_is_even_two():
    assert is_even(2) is True


def test_is_even_negative_odd():
    assert is_even(-3) is False


def test_is_even_negative_even():
    assert is_even(-4) is True


def test_palindrome_simple():
    assert is_palindrome("level") is True


def test_palindrome_mixed_case_and_space():
    assert is_palindrome("Race Car") is True


def test_palindrome_false():
    assert is_palindrome("hello") is False


def test_palindrome_empty():
    assert is_palindrome("") is True


def test_reverse_simple():
    assert reverse_string("abc") == "cba"


def test_reverse_empty():
    assert reverse_string("") == ""


def test_reverse_with_space():
    assert reverse_string("ab cd") == "dc ba"


@pytest.mark.boundary
def test_discount_zero_percent():
    assert apply_discount(100, 0) == 100


@pytest.mark.boundary
def test_discount_hundred_percent():
    assert apply_discount(100, 100) == 0


@pytest.mark.boundary
def test_discount_ten_percent():
    assert apply_discount(100, 10) == 90


@pytest.mark.boundary
def test_discount_rounding():
    assert apply_discount(19.99, 15) == 16.99


@pytest.mark.boundary
def test_discount_negative_price():
    with pytest.raises(ValueError, match="price"):
        apply_discount(-1, 10)


@pytest.mark.boundary
def test_discount_percent_below_zero():
    with pytest.raises(ValueError, match="percent"):
        apply_discount(100, -1)


@pytest.mark.boundary
def test_discount_percent_above_hundred():
    with pytest.raises(ValueError, match="percent"):
        apply_discount(100, 101)


def test_average_three_numbers():
    assert average([1, 2, 3]) == 2


def test_average_single_number():
    assert average([5]) == 5


def test_average_two_numbers():
    assert average([1, 2]) == 1.5


def test_average_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        average([])


def test_divide_even_result():
    assert divide(10, 2) == 5


def test_divide_negative():
    assert divide(-9, 3) == -3


def test_divide_fraction():
    assert divide(1, 4) == 0.25


def test_divide_by_zero():
    with pytest.raises(ValueError, match="zero"):
        divide(1, 0)


# TODO (Task 1): after refactoring, this placeholder must be deleted.
def test_task1_not_done_yet():
    pytest.fail("TODO Task 1: refactor the copy-pasted tests above into parametrize tables, then delete this test")
