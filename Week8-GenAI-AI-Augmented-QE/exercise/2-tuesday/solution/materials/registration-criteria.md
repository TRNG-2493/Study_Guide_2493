# ShopFront registration: acceptance criteria (synthetic, safe to paste into Claude)

Used in Stage 4 (few-shot Gherkin). Same rules as Monday's registration table, now with
the exact messages the page shows.

- A username must be 4 to 16 characters long. A shorter or longer username shows
  "Username must be 4-16 characters".
- A username may contain only lower-case letters, digits and hyphens, and must start with a
  letter. Otherwise the page shows "Username may use a-z, 0-9 and - and must start with a letter".
- The email domain must be example.com or example.org. Any other domain shows
  "Use an example.com or example.org address".
- Age must be a whole number from 16 to 99. Otherwise the page shows "Age must be between 16 and 99".
- When every field is valid, submitting the form shows "Welcome to ShopFront, <username>!".
