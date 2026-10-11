// Type declarations for custom commands (gives editor autocomplete). Add yours as you create them.
declare namespace Cypress {
  interface Chainable {
    /** cy.getByTest('username') -> cy.get('[data-test="username"]') */
    getByTest(value: string, options?: Partial<Loggable & Timeoutable & Withinable & Shadow>): Chainable<JQuery<HTMLElement>>;
    // TODO (Task 4): declare cy.login() here if you create it
  }
}
