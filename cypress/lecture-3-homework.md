# Lecture 3 Homework: Organizing Tests

**Task:** Use the users.json fixture, the cy.login() custom command and cy.intercept to stub and search products.

## Instructions

1. Start the practice app first with `npm start` (see 00-setup-and-practice-app.md).
2. Save the starter code below as `cypress/e2e/exercises/lecture3-exercise.cy.js`.
3. Replace every `TODO` comment with Cypress code.
4. Run it: `npx cypress open`, or `npx cypress run --spec cypress/e2e/exercises/lecture3-exercise.cy.js`.
5. All tests should pass. (In Lecture 4, they pass once you fix the bugs.)

## Starter code

### `cypress/e2e/exercises/lecture3-exercise.cy.js`

```js
// Lecture 3 exercise: fixtures, custom commands and cy.intercept

describe('Lecture 3 exercise', () => {
  it('logs in as the admin user from the fixture file', () => {
    // TODO 1: load users.json with cy.fixture()
    // TODO 2: use cy.login() with users.valid[1]
    // TODO 3: check the welcome message says "Welcome, admin!"
  });

  it('logs out after logging in', () => {
    // TODO 4: log in as student with cy.login()
    // TODO 5: click the logout button (data-cy="logout")
    // TODO 6: check you are back on /login.html
  });

  it('searches the stubbed product list', () => {
    // TODO 7: stub GET **/api/products.json with the products.json fixture and alias it
    // TODO 8: visit /products.html and wait for the alias
    // TODO 9: type "B" into the search box (data-cy="search")
    // TODO 10: check exactly one product is shown and its name is "Test Product B"
  });

  it('shows "No products found" for a search with no matches', () => {
    // TODO 11: stub the API again, visit the page, search for "zzz"
    // TODO 12: check the empty message (data-cy="empty") is visible
  });
});
```
