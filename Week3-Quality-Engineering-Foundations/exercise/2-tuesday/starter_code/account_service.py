"""Account Profile and Password Reset: a small in-memory service for Project 1 - QE Foundations.

Training code. Standard library only. It stands in for the real web application so you
can run your test cases from a console. Every method returns (ok, message).
Two builds exist: "0.5.0" (the QA build you test) and "0.5.1" (the developer's fix drop,
used for the retest in Part 4).
"""
import hashlib
import re
import secrets

TOKEN_MINUTES = 30
NAME_MIN, NAME_MAX = 1, 50
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PASSWORD_RULE_MSG = "Password must be at least 8 characters and contain a letter and a digit"
GENERIC_RESET_MSG = "If an account exists for this email, a reset link has been sent."


def _hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _password_ok(password):
    return (8 <= len(password) <= 64
            and any(c.isalpha() for c in password)
            and any(c.isdigit() for c in password))


class AccountService:
    def __init__(self, data=None, build="0.5.0"):
        self.build = build
        data = data or self.seed()
        self.accounts = data["accounts"]      # id -> {"email", "name", "pw"}
        self.current = data.get("current")    # id of the logged-in user, or None
        self.tokens = data["tokens"]          # token -> {"account", "expires_at", "status"}
        self.mailbox = data["mailbox"]        # simulated emails sent
        self.now = data["now"]                # simulated clock, in minutes
        self.next_id = data["next_id"]

    @staticmethod
    def seed():
        return {
            "accounts": {
                "u1": {"email": "anna@example.com", "name": "Anna Lee", "pw": _hash("Pass@1234")},
                "u2": {"email": "ben@example.com", "name": "Ben Carter", "pw": _hash("Pass@1234")},
            },
            "current": None, "tokens": {}, "mailbox": [], "now": 0, "next_id": 3,
        }

    def to_data(self):
        return {"accounts": self.accounts, "current": self.current, "tokens": self.tokens,
                "mailbox": self.mailbox, "now": self.now, "next_id": self.next_id}

    # ---- helpers ----
    def _find(self, email):
        """Find an account id by email, ignoring letter case."""
        for acc_id, acc in self.accounts.items():
            if acc["email"].lower() == email.strip().lower():
                return acc_id
        return None

    def _fixed(self):
        return self.build != "0.5.0"

    # ---- registration and login (support functions, not under test today) ----
    def register(self, email, name, password):
        if not email.strip():
            return False, "Email is required"
        if not name.strip():
            return False, "Name is required"
        if not EMAIL_RE.match(email):
            return False, "Enter a valid email address"
        if self._find(email):
            return False, "An account with this email already exists."
        if not _password_ok(password):
            return False, PASSWORD_RULE_MSG
        acc_id = "u%d" % self.next_id
        self.next_id += 1
        self.accounts[acc_id] = {"email": email, "name": name.strip()[:NAME_MAX], "pw": _hash(password)}
        return True, "Account created. Please log in."

    def login(self, email, password):
        acc_id = self._find(email)
        if acc_id and self.accounts[acc_id]["pw"] == _hash(password):
            self.current = acc_id
            return True, "Welcome, %s" % self.accounts[acc_id]["name"]
        return False, "Invalid email or password"

    def logout(self):
        self.current = None
        return True, "You have been logged out"

    # ---- profile ----
    def profile(self):
        if not self.current:
            return False, "Please log in"
        acc = self.accounts[self.current]
        return True, "Profile: name=%s | email=%s" % (acc["name"], acc["email"])

    def set_name(self, name):
        if not self.current:
            return False, "Please log in"
        name = name.strip()
        if not (NAME_MIN <= len(name) <= NAME_MAX):
            return False, "Name must be 1 to 50 characters"
        if not self._fixed():
            name = name[:20]
        self.accounts[self.current]["name"] = name
        return True, "Profile updated."

    def set_email(self, email):
        if not self.current:
            return False, "Please log in"
        email = email.strip()
        if not EMAIL_RE.match(email):
            return False, "Enter a valid email address"
        if self._fixed():
            owner = self._find(email)
            taken = owner is not None and owner != self.current
        else:
            taken = any(a["email"] == email for i, a in self.accounts.items() if i != self.current)
        if taken:
            return False, "An account with this email already exists."
        self.accounts[self.current]["email"] = email
        return True, "Profile updated."

    # ---- password reset ----
    def advance_clock(self, minutes):
        self.now += minutes
        return True, "Clock advanced by %d minutes (simulated time is now +%d minutes)" % (minutes, self.now)

    def request_reset(self, email):
        if not email.strip():
            return False, "Email is required"
        acc_id = self._find(email)
        if acc_id:
            for tok in self.tokens.values():
                if tok["account"] == acc_id and tok["status"] == "active":
                    tok["status"] = "replaced"
            token = secrets.token_urlsafe(9)
            self.tokens[token] = {"account": acc_id, "expires_at": self.now + TOKEN_MINUTES, "status": "active"}
            self.mailbox.append({"to": self.accounts[acc_id]["email"], "token": token, "sent_at": self.now})
        return True, GENERIC_RESET_MSG

    def complete_reset(self, token, new_password, confirm):
        tok = self.tokens.get(token)
        if not tok or tok["status"] == "replaced":
            return False, "This reset link is not valid."
        if tok["status"] == "used":
            return False, "This reset link has already been used."
        if self._fixed() and self.now > tok["expires_at"]:
            return False, "This reset link has expired. Please request a new one."
        if self._fixed() and new_password != confirm:
            return False, "Passwords do not match"
        if not _password_ok(new_password):
          
            return False, PASSWORD_RULE_MSG if self._fixed() else "Password is too weak"
        self.accounts[tok["account"]]["pw"] = _hash(new_password)
        tok["status"] = "used"
        return True, "Your password has been reset. Please log in."

    def read_mailbox(self, email):
        mails = [m for m in self.mailbox if m["to"].lower() == email.strip().lower()]
        if not mails:
            return True, "Mailbox for %s is empty" % email
        return True, "\n".join("Email to %s (sent at +%d min): reset link token=%s (valid %d minutes)"
                               % (m["to"], m["sent_at"], m["token"], TOKEN_MINUTES) for m in mails)
