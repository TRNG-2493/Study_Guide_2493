// cypress/support/e2e.js  -  loaded before every spec. STARTER: finish the TODOs.

// TODO 5.3: register cy.compareSnapshot with a global default threshold.
//   const { addCompareSnapshotCommand } = require('cypress-visual-regression/dist/command');
//   VERSION TRAP (the instructor demo's finding): in cypress-visual-regression 5.3.0 errorThreshold is a FRACTION
//   from 0 to 1 (0.001 = 0.1 percent), NOT a percentage as visual-testing.md Step 3 says. Run `npm run check:threshold`
//   (Task 5.1) to see it, then define a tiny helper so your specs read in percent:
//       Cypress.pct = (percent) => percent / 100;     // Cypress.pct(0.1) === 0.001
//   Global default: 0.1 percent of pixels, viewport capture.   Hint: visual-testing.md Step 3, Exercise 1.

// TODO 4.1: make the Selector Playground (and Studio) prefer our contract attribute.
//   Cypress.SelectorPlayground.defaults({ selectorPriority: ['data-test', 'data-testid', 'data-cy', 'id', 'class', 'tag'] });
//   Hint: recording-user-actions.md Example 2.

// Defaults for manual evidence screenshots (screenshots-and-video.md Example 3)
Cypress.Screenshot.defaults({
  overwrite: true,
  disableTimersAndAnimations: true,
});

require('./commands');
