# Lecture 2 Homework: Locate, Interact, Assert

**Task:** Test the login form: empty fields, a wrong password, a valid login and the checkbox.

## Instructions

1. Start the practice app first with `npm start` (see 00-setup-and-practice-app.md).
2. Save the starter code below as `cypress/e2e/exercises/lecture2-exercise.cy.js`.
3. Replace every `TODO` comment with Cypress code.
4. Run it: `npx cypress open`, or `npx cypress run --spec cypress/e2e/exercises/lecture2-exercise.cy.js`.
5. All tests should pass. (In Lecture 4, they pass once you fix the bugs.)

## Starter code

### `cypress/e2e/exercises/lecture2-exercise.cy.js`

```js
// Lecture 2 exercise: test the login page (login.html).
// Accounts: student / cypress123 and admin / admin123

describe('Lecture 2 exercise: login form', () => {
  beforeEach(() => {
    // TODO 1: visit /login.html
  });

  it('shows an error when both fields are empty', () => {
    // TODO 2: click the submit button (data-cy="login-submit")
    // TODO 3: check the error (data-cy="login-error") is visible and says
    //         "Username and password are required"
  });

  it('shows an error for a wrong password', () => {
    // TODO 4: type "student" into the username field and "nope" into the password field
    // TODO 5: submit the form
    // TODO 6: check the error says "Invalid username or password"
  });

  it('logs in with valid credentials', () => {
    // TODO 7: log in as student / cypress123
    // TODO 8: check the URL includes "/dashboard.html"
    // TODO 9: check the welcome message (data-cy="welcome") contains "student"
  });

  it('ticks the "Remember me" checkbox', () => {
    // TODO 10: check the checkbox (data-cy="remember") and assert it is checked
  });
});
```
