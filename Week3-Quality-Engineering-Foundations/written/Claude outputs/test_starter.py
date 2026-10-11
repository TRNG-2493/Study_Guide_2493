"""Starter tests (pytest style). Run:  python -m pytest -v   (or: pytest -v)

Two worked examples are provided. Add your own 5 automated cases below
(3 positive + 2 negative) in the same pattern: Arrange, Act, Assert.
Each test builds a fresh AuthService, so tests never affect each other.
"""
from registration_login import AuthService


def make_service():
    return AuthService()           # fresh, empty, in-memory


def test_tc_example_p_register_with_valid_data():
    # Arrange
    svc = make_service()
    # Act
    result = svc.register("alice@example.com", "alice_01", "Abcdef1!", "Abcdef1!", True)
    # Assert: success message, account created, password not echoed back
    assert result["ok"] is True
    assert result["message"] == "Registration successful."
    assert svc.user_count() == 1
    assert "password" not in str(result["user"]).lower()


def test_tc_example_n_register_with_too_short_password():
    svc = make_service()
    result = svc.register("alice@example.com", "alice_01", "Ab1!xyz", "Ab1!xyz", True)  # 7 chars
    # Assert: rejected, exact message, nothing was created
    assert result["ok"] is False
    assert result["message"] == "Password must be 8-64 characters."
    assert svc.user_count() == 0


# ---- YOUR TESTS GO BELOW (name them after your case IDs, e.g. test_tc_008_...) ----
