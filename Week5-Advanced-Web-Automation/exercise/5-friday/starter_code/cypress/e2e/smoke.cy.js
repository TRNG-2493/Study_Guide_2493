// GIVEN, works as-is. Run it first (Task 1) to prove your setup: app running, Cypress opens, spec is green.
// The last test is switched on with --env demoFailure=true and produces the failure screenshot + video (Task 2.3).
describe('Smoke: QE Shop is reachable', () => {
  it('logs in through the UI and lists four products', () => {
    cy.visit('/');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce', { log: false });
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
    cy.get('[data-test="inventory-item"]').should('have.length', 4);
  });

  if (Cypress.env('demoFailure')) {
    it('DEMO ONLY: fails on purpose to create evidence', () => {
      cy.visit('/');
      cy.get('[data-test="does-not-exist"]', { timeout: 2000 });
    });
  }
});
