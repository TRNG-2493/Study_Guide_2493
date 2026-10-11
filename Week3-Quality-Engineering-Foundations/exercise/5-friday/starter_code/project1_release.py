"""Project 1 - release 1.1 logic (small teaching module, standard library only).

Contains: password login with lockout, partner (social) login, session timeout,
and promo-code validation. Times are plain numbers of minutes so tests need no clock.
"""
import re

SESSION_TIMEOUT_MIN = 15      # release 1.1 (was 30)
MAX_FAILED_ATTEMPTS = 3       # account locks on the 3rd failed attempt
PROMO_MIN_LEN = 8             # release 1.1 (was 6)
PROMO_MAX_LEN = 12            # release 1.1 (was 10)

OK, DENIED, LOCKED = "OK", "DENIED", "LOCKED"


class AuthService:
    def __init__(self):
        self._users = {}

    def add_user(self, username, password):
        self._users[username] = {"password": password, "failed": 0, "locked": False}

    def add_partner_user(self, username):
        """Account created through the partner sign-in: it has no password."""
        self._users[username] = {"password": None, "failed": 0, "locked": False}

    def login(self, username, password):
        user = self._users.get(username)
        if user is None:
            return DENIED
        if user["locked"]:
            return LOCKED
        if user["password"] is None or user["password"] == password:
            user["failed"] = 0
            return OK
        user["failed"] += 1
        if user["failed"] >= MAX_FAILED_ATTEMPTS:
            user["locked"] = True
            return LOCKED
        return DENIED

    def partner_login(self, partner_token):
        """Token format 'partner:<id>' where <id> is 1 to 20 letters or digits."""
        match = re.fullmatch(r"partner:([A-Za-z0-9]{1,20})", partner_token or "")
        if not match:
            return DENIED
        username = "p_" + match.group(1)
        if username not in self._users:
            self.add_partner_user(username)
        return OK

    def is_locked(self, username):
        return self._users[username]["locked"]


class Session:
    def __init__(self, now):
        self.expires_at = now + SESSION_TIMEOUT_MIN

    def is_active(self, now):
        return now < self.expires_at

    def touch(self, now):
        """User activity extends an active session; an expired session stays expired."""
        if self.is_active(now):
            self.expires_at = now + 30


def validate_promo(code):
    """True if the promo code is acceptable (case-insensitive, surrounding spaces ignored)."""
    if not isinstance(code, str):
        return False
    if not re.fullmatch(r"[A-Z0-9]+", code):
        return False
    return PROMO_MIN_LEN <= len(code) <= PROMO_MAX_LEN
