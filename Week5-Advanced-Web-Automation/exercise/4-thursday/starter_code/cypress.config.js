// Lesson: cypress-architecture-and-setup s.6 (config), browser-management s.5 (viewport)
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3100', // start the app first: npm run app
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: 'cypress/support/e2e.js',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    retries: { runMode: 1, openMode: 0 },
  },
});
