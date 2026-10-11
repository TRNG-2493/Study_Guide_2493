"""Instructor solution: the 5 automated cases (3 positive + 2 negative).
Copy next to registration_login.py and run: python -m pytest -v sample-automated-tests-solution.py
(or rename to test_*.py). On build 0.3.0 exactly two tests fail, on purpose:
  test_tc_014 -> SD-03 (lockout threshold)   test_tc_028 -> SD-02 (confirm password case)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "starter_code"))
from registration_login import AuthService

BAD = "Invalid email/username or password."


def registered_service():
    svc = AuthService()
    svc.register("alice@example.com", "alice_01", "Abcdef1!", "Abcdef1!", True)
    return svc


def test_tc_009_login_with_email_and_correct_password():           # positive, R-09
    svc = registered_service()
    result = svc.login("alice@example.com", "Abcdef1!")
    assert result["ok"] is True
    assert result["message"] == "Login successful."


def test_tc_012_remember_me_gives_token():                          # positive, R-13
    svc = registered_service()
    result = svc.login("alice@example.com", "Abcdef1!", remember_me=True)
    assert result["ok"] is True
    assert result.get("remember_token")


def test_tc_014_four_failed_logins_do_not_lock():                   # positive, R-11 (fails on 0.3.0: SD-03)
    svc = registered_service()
    for _ in range(4):
        assert svc.login("alice@example.com", "Wrong1!x")["message"] == BAD
    assert svc.login("alice@example.com", "Abcdef1!")["ok"] is True


def test_tc_024_password_too_short_is_rejected():                   # negative, R-04
    svc = AuthService()
    result = svc.register("alice@example.com", "alice_01", "Ab1!xyz", "Ab1!xyz", True)
    assert result["ok"] is False
    assert result["message"] == "Password must be 8-64 characters."
    assert svc.user_count() == 0


def test_tc_028_confirm_password_case_difference_is_rejected():     # negative, R-06 (fails on 0.3.0: SD-02)
    svc = AuthService()
    result = svc.register("alice@example.com", "alice_01", "Abcdef1!", "abcdef1!", True)
    assert result["ok"] is False
    assert result["message"] == "Passwords do not match."
    assert svc.user_count() == 0
