// Custom commands = the Cypress stand-in for Playwright fixtures (partly).
// Lesson: fixtures-and-custom-fixtures, Part B

// PROVIDED so Task 1 is quick to start. Playwright twin: set_test_id_attribute("data-test") + get_by_test_id.
Cypress.Commands.add('getByTest', (value, options) => cy.get(`[data-test="${value}"]`, options));

// TODO (Task 4 - Navigator researches, Driver types):
// Create cy.login(username, password) using cy.session() so tests 2 and 3 share one cached login.
// Remember: after cy.session the page is blank -> the test must cy.visit('/inventory.html') next.
// Validate the session with cy.getCookie('session-username').should('exist').
// Hint: lesson writing-cypress-tests s.7; fixtures-and-custom-fixtures s.8.2
