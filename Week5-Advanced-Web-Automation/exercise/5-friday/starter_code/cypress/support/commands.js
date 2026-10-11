// cypress/support/commands.js  -  STARTER. Custom commands you build during the exercise.

// ---------------------------------------------------------------------------------------------
// TODO 3.2: logging helpers (logging.md Example 4, Exercise 3 and Exercise 4)
//   const SENSITIVE_KEYS = ['password', 'token', 'authorization', 'cardNumber'];
//   function sanitize(value) { ... recursive: replace values of sensitive keys with '***' ... }
//   Cypress.sanitize = sanitize;                              // exposed so a spec can unit-test it
//   Cypress.Commands.add('step', (title) => { ... cy.log + cy.task('log') ... });
//   Cypress.Commands.add('logInfo', (message, data) => { ... Cypress.log + cy.task('log') ... });
// ---------------------------------------------------------------------------------------------

// ---------------------------------------------------------------------------------------------
// TODO 4.5: reusable commands for the cleaned test (editing-generated-code.md Example 2)
//   cy.login(username)            UI login once per user, cached with cy.session, validate the cookie
//                                 'session-username'. Read the password from Cypress.env('APP_PASSWORD')
//                                 and type it with { log: false }.
//   cy.addProductToCart(name)     by product NAME, not by position:
//                                 cy.contains('[data-test="inventory-item"]', name).find('button')...
//   cy.openApp(path)              cy.visit(path) that appends ?diff=on when Cypress.env('appDiff') is set
//                                 (used by Task 6 to trigger the deliberate visual difference).
// ---------------------------------------------------------------------------------------------

// GIVEN (read it and explain each of the three parts in your notes, Task 5.4):
// cy.stabilise(): make the page deterministic before any screenshot (visual-testing.md Step 5, s.8)
Cypress.Commands.add('stabilise', () => {
  cy.document({ log: false }).its('fonts.status').should('eq', 'loaded');           // part 1: fonts
  cy.get('img', { log: false }).should(($imgs) => {                                  // part 2: images
    $imgs.each((_, img) => {
      expect(img.naturalWidth, `image ${img.src} loaded`).to.be.greaterThan(0);
    });
  });
  cy.document({ log: false }).then((doc) => {                                        // part 3: motion and caret
    const style = doc.createElement('style');
    style.innerHTML = '*, *::before, *::after { animation: none !important; transition: none !important; caret-color: transparent !important; }';
    doc.head.appendChild(style);
  });
});
