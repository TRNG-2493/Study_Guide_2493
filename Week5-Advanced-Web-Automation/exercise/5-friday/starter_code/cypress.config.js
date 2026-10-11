// cypress.config.js  -  STARTER. Work through the TODO markers (search for "TODO").
// Lessons: screenshots-and-video.md (s.6-8, 10, Example 4) | logging.md (s.7 cy.task) | visual-testing.md (Step 2)
const { defineConfig } = require('cypress');
// TODO 2.1 / 5.2: you will need these once you use them (remove the comment marks)
// const { configureVisualRegression } = require('cypress-visual-regression');
// const fs = require('fs');
// const path = require('path');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:4173', // start the app first: npm start
    specPattern: ['cypress/e2e/**/*.cy.js', 'cypress/recorded/**/*.cy.js'],

    // Fixed viewport: a visual test must never depend on the machine default (visual-testing.md s.8.2)
    viewportWidth: 1280,
    viewportHeight: 800,
    retries: { runMode: 0, openMode: 0 }, // retries can hide a flaky visual test (visual-testing.md s.8.8)

    // TODO 2.1: screenshots and video.
    //   - screenshotsFolder  -> 'cypress/snapshots/actual'   (so baselines in snapshots/base are never trashed)
    //   - screenshotOnRunFailure -> true
    //   - trashAssetsBeforeRuns  -> true
    //   - videosFolder -> 'cypress/videos'; video -> true (off by default since Cypress 13); videoCompression -> 32
    //   Hint: screenshots-and-video.md s.7 and Example 4.

    // TODO 5.2: visual-regression settings, env-based style of cypress-visual-regression 5.x
    //   visualRegressionType ('regression'), visualRegressionBaseDirectory ('cypress/snapshots/base'),
    //   visualRegressionDiffDirectory ('cypress/snapshots/diff'), visualRegressionGenerateDiff ('fail'),
    //   visualRegressionFailSilently (false).   Hint: visual-testing.md Step 2.
    env: {
      APP_USER: 'standard_user',
      APP_PASSWORD: 'secret_sauce', // practice data for the local app; real secrets go in cypress.env.json / CI secrets
    },

    setupNodeEvents(on, config) {
      // TODO 5.2: register the plugin tasks:  configureVisualRegression(on);

      // TODO 3.1: on('task', { log, logToFile })  - terminal and file logging.
      //   Both handlers MUST return null (never undefined). Hint: logging.md s.7 and Example 3.

      // TODO 2.2: on('after:spec', ...) - delete the video of a spec whose attempts all passed.
      //   Hint: screenshots-and-video.md s.10 and Example 4.

      return config;
    },
  },
});
