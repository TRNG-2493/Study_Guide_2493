// PORT OF: test_add_to_cart_updates_badge (Playwright, shape 2: shared login + conditional element)
// Lessons: writing-cypress-tests s.5 + s.7, element-location s.8, assertions-and-annotations s.7 (absence)
//
// TODO 1: log in (first with a plain beforeEach that types into the form; refactor to cy.login in Task 4).
// TODO 2: assert the badge is ABSENT first: cy.getByTest('cart-badge').should('not.exist')
// TODO 3: click the add-to-cart button for 'sauce-backpack'; assert the badge has text '1'.
// TODO 4: assert the remove button for that product is visible.
// Think: Playwright used to_have_count(0). Which Cypress assertion is the equivalent, and why is
//        .should('not.be.visible') the WRONG one here? (assertions s.7)

describe('Cart badge', () => {
  it.skip('TODO: write the test', () => {});
});
