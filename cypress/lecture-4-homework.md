# Lecture 4 Homework: Debugging and Evidence

**Task:** Every test fails on purpose. Use the Command Log, time-travel, .debug() and cy.pause() to find out why, then fix the test (not the app).

## Instructions

1. Start the practice app first with `npm start` (see 00-setup-and-practice-app.md).
2. Save the starter code below as `cypress/e2e/exercises/lecture4-exercise.cy.js`.
3. Replace every `TODO` comment with Cypress code.
4. Run it: `npx cypress open`, or `npx cypress run --spec cypress/e2e/exercises/lecture4-exercise.cy.js`.
5. All tests should pass. (In Lecture 4, they pass once you fix the bugs.)

## Starter code

### `cypress/e2e/exercises/lecture4-exercise.cy.js`

```js
// Lecture 4 exercise: each test below fails.
// Run this file in open mode, use the Command Log, time-travel, .debug() and
// cy.pause() to find out WHY, then fix the test (not the app).

describe('Lecture 4 exercise: find the bugs', () => {
  it('Bug 1: adds a todo', () => {
    cy.visit('/todo.html');
    cy.get('[data-cy=new-todo]').type('Buy milk');
    cy.get('[data-cy=todo-item]').should('have.length', 3);
  });

  it('Bug 2: filters completed todos', () => {
    cy.visit('/todo.html');
    cy.get('[data-cy=filter]').select('Done');
    cy.get('[data-cy=todo-item]').should('have.length', 1);
  });

  it('Bug 3: shows the welcome message', () => {
    cy.login('student', 'cypress123');
    cy.get('[data-cy=welcome]').should('have.text', 'Welcome, student');
  });

  it('Bug 4: counts the products', () => {
    cy.visit('/products.html');
    cy.get('[data-cy=product-name]').should('have.length', 4);
    cy.get('[data-cy=product-price]').first().should('have.text', '24.99');
  });

  it('Extra: save evidence', () => {
    // TODO: visit /products.html, log the number of products with cy.log and cy.task,
    // and save a screenshot of the product list called "products-list".
  });
});
```
