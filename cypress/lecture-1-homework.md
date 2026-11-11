# Lecture 1 Homework: Foundations

**Task:** Use the navigation bar, aliases and the counter on the home page.

## Instructions

1. Start the practice app first with `npm start` (see 00-setup-and-practice-app.md).
2. Save the starter code below as `cypress/e2e/exercises/lecture1-exercise.cy.js`.
3. Replace every `TODO` comment with Cypress code.
4. Run it: `npx cypress open`, or `npx cypress run --spec cypress/e2e/exercises/lecture1-exercise.cy.js`.
5. All tests should pass. (In Lecture 4, they pass once you fix the bugs.)

## Starter code

### `cypress/e2e/exercises/lecture1-exercise.cy.js`

```js
// Lecture 1 exercise: fill in each TODO.

describe('Lecture 1 exercise', () => {
  beforeEach(() => {
    // TODO 1: visit the home page
  });

  it('opens the Todos page from the navigation bar', () => {
    // TODO 2: click the "Todos" link (data-cy="nav-todo")
    // TODO 3: check the URL includes "/todo.html"
    // TODO 4: check the page title (data-cy="page-title") has the text "Todos"
  });

  it('decrements the counter twice', () => {
    // TODO 5: save the decrement button (data-cy="decrement") as an alias called "minus"
    // TODO 6: click the alias twice
    // TODO 7: check the counter (data-cy="count") shows "-2"
  });
});
```
