// PORT OF: test_sort_price_low_to_high (Playwright, shape 3: list + sort)
// Lessons: element-interaction s.5 (.select), assertions-and-annotations s.4 + s.6, writing-cypress-tests s.4 + s.5
//
// TODO 1: log in, then choose 'lohi' in the sort dropdown (.select).
// TODO 2: collect the prices and assert they are ascending.
//         The Playwright version used a plain `assert` AFTER all_inner_texts() - no retrying.
//         In Cypress, do it with .should(($els) => { ... }) so the check RETRIES while the list re-sorts.
// TODO 3: also assert there are 6 items (.should('have.length', 6)).
// WATCH OUT: the product list loads ~300 ms after the page does. Do not use cy.wait(300)!

describe('Sort by price', () => {
  it.skip('TODO: write the test', () => {});
});
