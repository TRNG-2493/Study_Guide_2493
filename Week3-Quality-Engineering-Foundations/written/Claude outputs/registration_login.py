"""Small Registration and Login service used as the test target for the
Week 3 Wednesday exercise (build 0.3.0).

Treat this file as a black box: test it through the public methods and the
run_cases.py command line, using the specification in
templates/feature-spec-registration-login-v2.md.
Standard library only.
"""
import json
import os
import re

MAX_FAILED_ATTEMPTS = 5          # N in the specification
SPECIAL_CHARS = "!@#$%^&*"

MSG = {
    "reg_ok": "Registration successful.",
    "email": "Enter a valid email address.",
    "email_taken": "This email is already registered.",
    "username": "Username must be 3-20 characters (letters, digits, underscore).",
    "pw_len": "Password must be 8-64 characters.",
    "pw_rule": ("Password must include an uppercase letter, a lowercase letter, "
                "a digit and a special character (!@#$%^&*)."),
    "confirm": "Passwords do not match.",
    "terms": "You must accept the Terms and Conditions.",
    "login_ok": "Login successful.",
    "login_bad": "Invalid email/username or password.",
    "login_required": "Email/username and password are required.",
    "locked": "Account locked. Try again later.",
}


def _fail(key):
    return {"ok": False, "message": MSG[key]}


def _valid_email(email):
    if not isinstance(email, str) or not email or " " in email:
        return False
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or "." not in domain:
        return False
    return not (domain.startswith(".") or domain.endswith("."))


def mask_password(password, visible=False):
    """Return what the password box displays (show/hide toggle)."""
    return password if visible else "*" * len(password)


class AuthService:
    def __init__(self, state_path=None):
        self.state_path = state_path
        self.users = {}      # email as stored -> {"username", "password"}
        self.fails = {}      # lower-case email -> consecutive failed logins
        self._token_counter = 0
        if state_path and os.path.exists(state_path):
            with open(state_path) as f:
                data = json.load(f)
            self.users = data["users"]
            self.fails = data["fails"]
            self._token_counter = data.get("tokens", 0)

    def _save(self):
        if self.state_path:
            with open(self.state_path, "w") as f:
                json.dump({"users": self.users, "fails": self.fails,
                           "tokens": self._token_counter}, f)

    def user_count(self):
        return len(self.users)

    def register(self, email, username, password, confirm, terms_accepted):
        if not _valid_email(email):
            return _fail("email")

        raw = username if isinstance(username, str) else ""
        if not (3 <= len(raw) <= 20):
            return _fail("username")
        name = raw.strip()
        if not re.fullmatch(r"[A-Za-z0-9_]+", name):
            return _fail("username")

        if not (8 <= len(password) <= 64):
            return _fail("pw_len")
        if not (any(c.isupper() for c in password)
                and any(c.islower() for c in password)
                and any(c.isdigit() for c in password)):
            return _fail("pw_rule")

        if password.lower() != confirm.lower():
            return _fail("confirm")

        if email in self.users:
            return _fail("email_taken")

        self.users[email] = {"username": name, "password": password}
        self._save()
        return {"ok": True, "message": MSG["reg_ok"],
                "user": {"email": email, "username": name}}

    def _find(self, identifier):
        ident = identifier.strip().lower()
        for email, u in self.users.items():
            if email.lower() == ident or u["username"].lower() == ident:
                return email, u
        return None, None

    def login(self, identifier, password, remember_me=False):
        if not identifier or not identifier.strip() or not password:
            return _fail("login_required")
        email, user = self._find(identifier)
        if user is None:
            return _fail("login_bad")
        key = email.lower()
        if self.fails.get(key, 0) >= MAX_FAILED_ATTEMPTS - 1:
            return _fail("locked")
        if user["password"] != password:
            self.fails[key] = self.fails.get(key, 0) + 1
            self._save()
            if self.fails[key] >= MAX_FAILED_ATTEMPTS - 1:
                return _fail("locked")
            return _fail("login_bad")
        self.fails[key] = 0
        result = {"ok": True, "message": MSG["login_ok"], "username": user["username"]}
        if remember_me:
            self._token_counter += 1
            result["remember_token"] = "tok-%04d" % self._token_counter
        self._save()
        return result
