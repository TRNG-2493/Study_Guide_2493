// TASK 4: the CLEANED version of cypress/recorded/raw-checkout.cy.js. (STARTER: replace the TODOs.)
// Follow the 10 steps of editing-generated-code.md s.3-12. Keep the journey identical:
//   login -> add the first two products -> cart -> checkout -> enter details -> finish.
//
// Checklist for this file:
//   [ ] a behaviour-style name (describe + it), no "template" / "tests checkout"
//   [ ] no cy.viewport / full URLs / cy.wait(number): they live in config or become retry-able assertions
//   [ ] data-test selectors only; products found by NAME via cy.addProductToCart
//   [ ] customer data from cypress/fixtures/users.json; password only from Cypress.env
//   [ ] FOUR assertion layers: guard (URL), state (badge count, cart rows), outcome (confirmation text), negative (badge gone)
//   [ ] cy.step('...') headings (Task 3) so the Command Log and the terminal read like a story
//   [ ] hooks: cy.login() + cy.openApp('/inventory.html') in beforeEach
describe('TODO: name the feature', () => {
  beforeEach(() => {
    // TODO
  });

  it.skip('TODO: name the behaviour a user can observe', () => {
    // TODO: remove .skip once cy.login / cy.addProductToCart exist
  });

  // TODO (extra, 5 min): a NEGATIVE test, e.g. checkout with an empty first name shows
  //   'Error: First Name is required' and stays on /checkout.html.
});
