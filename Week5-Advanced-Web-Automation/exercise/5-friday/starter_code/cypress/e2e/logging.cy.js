// TASK 3.3: two small specs that PROVE the logging behaviour instead of just printing it. (STARTER)
// Hint: logging.md s.2 + Exercise 1 (queue order), Exercise 4 (sanitiser).
describe('Logging helpers', () => {
  it.skip('plain JavaScript runs first, queued commands run later (order A, C, B)', () => {
    // TODO: push 'A' (plain JS), queue cy.log + cy.then(push 'B'), push 'C' (plain JS),
    //       then in a final cy.then assert the order is ['A', 'C', 'B'].
  });

  it.skip('sanitize() masks secrets recursively', () => {
    // TODO: expect(Cypress.sanitize({ user: 'a', password: 'b', nested: { token: 'c' } }))
    //       to deep-equal { user: 'a', password: '***', nested: { token: '***' } }
  });
});
