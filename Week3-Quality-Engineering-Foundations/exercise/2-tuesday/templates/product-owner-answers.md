# Product Owner answers (read ONLY after you finish your question log in Part 1)

The Product Owner answered the questions most teams would ask. Use these answers to rewrite requirements (Part 1), write expected results (Part 2) and run the program (Part 3). If you asked a question that is not answered here, write your own sensible assumption in your log and label it "Assumption".

| Area | Answer |
|---|---|
| Not logged in | Opening the profile without being logged in shows "Please log in". |
| Display name | 1 to 50 characters after leading and trailing spaces are removed. Anything else is rejected with "Name must be 1 to 50 characters". Success message: "Profile updated." |
| Email change | Same format rule as registration (text, "@", a domain with a dot, no spaces), otherwise "Enter a valid email address". An address already used by another account is rejected with "An account with this email already exists." No re-verification in this release. Success message: "Profile updated." |
| Case | Email is not case-sensitive anywhere (profile, uniqueness check, reset lookup, login). |
| Speed | Saving a profile change (no noticeable delay) shows the confirmation within 2 seconds under normal load. (The console program cannot measure this.) |
| Reset request | Always show "If an account exists for this email, a reset link has been sent." whether or not the email is registered. No limit on the number of requests in this release (rate limiting is on the backlog). Requesting a new link makes the older link stop working. |
| Reset link | Valid for 30 minutes from the moment it was sent, single use. Messages: after 30 minutes "This reset link has expired. Please request a new one."; already used "This reset link has already been used."; unknown or replaced link "This reset link is not valid." |
| New password | Typed twice. If the two entries differ: "Passwords do not match" and the password stays unchanged. The new password follows the registration rule (8 to 64 characters, at least one letter and one digit); otherwise "Password must be at least 8 characters and contain a letter and a digit". Checks run in this order: link, match, rule. |
| After reset | Message "Your password has been reset. Please log in." The old password stops working; the user is not logged in automatically. |
| Security and usability | The token must be unguessable. Quality targets for "user-friendly" and "safe" are not defined yet; they will be agreed in a later release. |
