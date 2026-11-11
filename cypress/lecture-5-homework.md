# Lecture 5 Homework: Recording and Visual Testing

**Task:** Record a login with Cypress Studio, edit the generated code, and add visual snapshot tests for the login page.

## Instructions

1. Start the practice app first with `npm start` (see 00-setup-and-practice-app.md).
2. Save the starter code below as `cypress/e2e/exercises/lecture5-exercise.cy.js`.
3. Replace every `TODO` comment with Cypress code.
4. Run it: `npx cypress open`, or `npx cypress run --spec cypress/e2e/exercises/lecture5-exercise.cy.js`.
5. All tests should pass. (In Lecture 4, they pass once you fix the bugs.)

## Starter code

### `cypress/e2e/exercises/lecture5-exercise.cy.js`

```js
// Lecture 5 exercise
//
// Part A: Record and edit
//   1. Run `npx cypress open`, open this file and hover the "records a login" test.
//   2. Click "Add commands to test" (the magic wand icon) to start Cypress Studio.
//   3. In the app: type "admin" / "admin123", click "Log in", then click "Log out".
//   4. Click "Save Commands".
//   5. Edit the generated code: use cy.login(), add assertions for the dashboard URL,
//      the welcome text and the return to the login page.
//
// Part B: Visual tests
//   6. Snapshot the login page.
//   7. Snapshot the login form showing the "Invalid username or password" error.
//   8. Change a colour in app/styles.css, run again and look at the diff image
//      in cypress/snapshots/__diff_output__. Then undo the change.

describe('Lecture 5 exercise', () => {
  it('records a login', () => {
    cy.visit('/login.html');
    // Studio will add commands here
  });

  it('matches the login page', () => {
    // TODO: visit /login.html and take a snapshot called "login-page"
  });

  it('matches the login error state', () => {
    // TODO: submit a wrong password, then snapshot only the form (data-cy="login-form")
  });
});
```
