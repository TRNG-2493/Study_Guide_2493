// TASK 5: visual regression for QE Shop. (STARTER: remove .skip as you implement each test.)
// Baselines are written to cypress/snapshots/base/cypress/e2e/visual.cy.js/<name>.png  (one folder per spec path!).
// Read: visual-testing.md s.7 (scope), s.8 (determinism), s.9 (masking), Steps 5-8.
//
// Two elements on the inventory page change by design on every load (look in app/app.js, marked DYNAMIC):
//   [data-test="last-updated"]   - a clock that ticks every second
//   [data-test="visitors-online"] - a random number
// They must NOT make the tests flaky, and the SAME masking must be present when baselines are generated.
//
// Threshold policy to implement (write it as a comment above your tests, VIS Exercise 6):
//   whole-page snapshots   0.1 percent       element snapshots   0.05 percent
//   remember: the plugin wants a FRACTION. Use Cypress.pct(...) from support/e2e.js.
describe('Visual regression: QE Shop', () => {
  beforeEach(() => {
    cy.viewport(1280, 800);
  });

  it.skip('login page matches the baseline', () => {
    // TODO: cy.openApp('/'); wait for [data-test="login-button"] to be visible; cy.stabilise();
    //       cy.compareSnapshot('login-page');   (global default threshold)
  });

  context('Inventory page (logged in)', () => {
    beforeEach(() => {
      // TODO: cy.login(); cy.openApp('/inventory.html'); assert 4 items; cy.stabilise();
    });

    it.skip('whole viewport matches the baseline (dynamic content masked)', () => {
      // TODO: cy.compareSnapshot('inventory-viewport', { errorThreshold: Cypress.pct(0.1), blackout: [ ...two dynamic selectors ] });
    });

    it.skip('product list (element) matches the baseline', () => {
      // TODO: cy.get('[data-test="inventory-list"]').compareSnapshot('inventory-list', Cypress.pct(0.05));
    });

    it.skip('first product card (element) matches the baseline', () => {
      // TODO: element snapshot of the first [data-test="inventory-item"], threshold 0.05 percent
    });
  });

  it.skip('order confirmation page matches the baseline (order number masked)', () => {
    // TODO: log in, add a product, finish checkout with the fixture customer (reuse your commands),
    //       stabilise, compareSnapshot('order-complete', { blackout: ['[data-test="order-number"]'], ... })
  });
});
