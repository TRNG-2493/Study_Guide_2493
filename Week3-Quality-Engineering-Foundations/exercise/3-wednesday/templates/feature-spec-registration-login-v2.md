# Feature specification v2: Registration and Login (Project 1 - QE Foundations)

Build under test: 0.3.0. Owner: Product Owner. Status: approved for testing. This is your only source of truth: if something is not written here, note it as a question instead of guessing.

## Registration form fields

| Field | Notes |
|---|---|
| Email | Text |
| Username | Text |
| Password | Hidden by default, with a show/hide toggle |
| Confirm password | Hidden |
| Terms and Conditions | Checkbox |

## Business rules

| Rule ID | Area | Rule | Message / outcome |
|---|---|---|---|
| R-01 | Registration | Email is required and must be valid: exactly one "@", something before it, a domain containing a "." that does not start or end the domain, no spaces. | "Enter a valid email address." |
| R-02 | Registration | Email must be unique. "ALICE@x.com" and "alice@x.com" are the same email. | "This email is already registered." |
| R-03 | Registration | Username: leading and trailing spaces are removed first; the remaining text must be 3-20 characters, letters, digits or underscore only. | "Username must be 3-20 characters (letters, digits, underscore)." |
| R-04 | Registration | Password length is 8-64 characters. | "Password must be 8-64 characters." |
| R-05 | Registration | Password must contain at least one uppercase letter, one lowercase letter, one digit and one special character from ! @ # $ % ^ & * | "Password must include an uppercase letter, a lowercase letter, a digit and a special character (!@#$%^&*)." |
| R-06 | Registration | Confirm password must match the password exactly (case-sensitive). | "Passwords do not match." |
| R-07 | Registration | The Terms and Conditions checkbox must be ticked. | "You must accept the Terms and Conditions." |
| R-08 | Registration | When all rules pass: the account is created, the message is shown, and the password is never shown back in the result. | "Registration successful." |
| R-09 | Login | A registered user can log in with email or username plus the correct password. Email and username are not case-sensitive; the password is. | "Login successful." |
| R-10 | Login | Unknown user and wrong password give the same single message (nothing reveals whether the account exists). | "Invalid email/username or password." |
| R-11 | Login | Lockout: N = 5. The 5th consecutive failed attempt locks the account and shows the lock message. While locked, even the correct password is rejected. A successful login resets the failed-attempt counter. (How the lock is released is out of scope.) | "Account locked. Try again later." |
| R-12 | Login | Both the email/username and the password are required. | "Email/username and password are required." |
| R-13 | Login | Remember me: only when the box is ticked and login succeeds, a remember token is returned. A failed login never returns a token. | token present / absent |
| R-14 | Login | Show/hide password: the password box is masked by default (one "*" per character). Showing it displays the exact text; toggling never changes the value. | masked / exact text |

## Notes

* When several registration rules are broken at once, only the first message is shown, in this order: R-01, R-03, R-04, R-05, R-06, R-07, R-02. Design your cases so that each one breaks one rule only.
* Unknown accounts have no failed-attempt counter.
* Out of scope: password reset, email verification, session expiry, the visual layout.

## Questions you may raise

If a rule seems ambiguous, write it in the "Assumptions and questions" part of your suite and state the assumption you used.
