// PORT OF: test_login_rejected (Playwright, shape 1: form + data-driven)
// Lessons: writing-cypress-tests s.1-2, element-location s.1, element-interaction s.3,
//          assertions-and-annotations s.3.2, fixtures-and-custom-fixtures Part A
//
// TODO 1: load cypress/fixtures/login-cases.json (hint: require() at top-level is fine for generating tests,
//         cy.fixture() is async and cannot create tests dynamically).
// TODO 2: loop over the cases and create one it() per case, titled with case.title.
// TODO 3: visit '/', type username/password ONLY if non-empty (Cypress throws on .type('')! see element-interaction s.3).
// TODO 4: click Login, then assert the error text with .should('contain.text', ...) and that url does not include 'inventory'.

describe('Login - rejected credentials', () => {
  it.skip('TODO: replace this placeholder with the data-driven loop', () => {});
});
