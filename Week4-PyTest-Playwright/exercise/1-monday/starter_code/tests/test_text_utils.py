"""Tests for is_valid_username, count_words, truncate  (function-style tests)."""
import pytest

from qe_utils import count_words, is_valid_username, truncate


# ---- WORKED EXAMPLE (already done for you; read it, then copy the pattern) ----
@pytest.mark.smoke
def test_username_valid_simple_name():
    # Arrange
    name = "qe_trainee"
    # Act
    result = is_valid_username(name)
    # Assert
    assert result is True


# ---- TODO tests: replace each `pytest.fail(...)` line with real test code ----

def test_username_too_short_is_rejected():
    # TODO (Task 3): 2 characters must be rejected. Add markers: boundary, regression
    pytest.fail("TODO: implement")


def test_username_exactly_3_chars_is_accepted():
    # TODO (Task 3): lower boundary. Markers: boundary, regression
    pytest.fail("TODO: implement")


def test_username_16_chars_is_rejected():
    # TODO (Task 3): upper boundary + 1. Markers: boundary, regression
    pytest.fail("TODO: implement")


def test_username_starting_with_digit_is_rejected():
    # TODO (Task 3): "1abc" -> False. Marker: regression
    pytest.fail("TODO: implement")


def test_username_with_space_or_symbol_is_rejected():
    # TODO (Task 3): "bad name" and "bad-name" -> False (two asserts are fine). Marker: regression
    pytest.fail("TODO: implement")


def test_username_non_string_raises_type_error():
    # TODO (Task 4): use pytest.raises(TypeError, match=...) with the input 12345
    pytest.fail("TODO: implement")


def test_count_words_simple_sentence():
    # TODO (Task 3): "quality is everyone's job" -> 4. Marker: smoke
    pytest.fail("TODO: implement")


def test_count_words_empty_string_is_zero():
    # TODO (Task 3): "" -> 0. Markers: boundary, regression
    pytest.fail("TODO: implement")


def test_count_words_non_string_raises_type_error():
    # TODO (Task 4): None must raise TypeError
    pytest.fail("TODO: implement")


def test_truncate_short_text_is_unchanged():
    # TODO (Task 3): truncate("hello", 10) == "hello". Marker: smoke
    pytest.fail("TODO: implement")


def test_truncate_long_text_ends_with_ellipsis_and_has_max_len():
    # TODO (Task 3): truncate("abcdefghij", 8) == "abcde..."  (len 8). Marker: regression
    pytest.fail("TODO: implement")


def test_truncate_text_exactly_max_len_is_unchanged():
    # TODO (Task 6): by the docstring, text that fits exactly must NOT be cut.
    # Write the test according to the docstring. It will FAIL - why?
    # Then mark it as a known bug:  @pytest.mark.xfail(reason="...", strict=True)
    # Markers: boundary, regression
    pytest.fail("TODO: implement")


def test_truncate_max_len_below_3_raises_value_error():
    # TODO (Task 4): max_len=2 -> ValueError, check the message with match=
    pytest.fail("TODO: implement")
