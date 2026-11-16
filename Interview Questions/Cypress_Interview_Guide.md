# Cypress Interview Guide

## Beginner to Intermediate: Questions, Answers, Scenarios, Coding Exercises

This guide is intended for candidates who know basic JavaScript and are
beginning browser automation. Examples use Cypress with JavaScript and
the current `cy.*` command style.

> **Version note:** Cypress features and configuration can change
> between releases. Check the installed Cypress version and its
> documentation before relying on a particular Studio, browser, or
> reporting feature. Cypress Studio availability and behavior can depend
> on version and project configuration.

## Difficulty labels

-   **Beginner:** Explain the concept or write a straightforward test.
-   **Intermediate:** Apply the concept to a realistic test, understand
    framework behavior, or troubleshoot an issue.
-   **Advanced basics:** A stretch question for a beginner interview;
    not usually a pass/fail requirement for an entry-level candidate.

------------------------------------------------------------------------



## Quick navigation

- [Conceptual Cypress questions](#part-1----conceptual-interview-questions-and-suggested-answers)
- [Scenario-based questions (5 scenarios)](#scenario-based-questions)
- [Practical coding exercises](#part-3----practical-coding-exercises)
- [Difficulty classification](#question-by-question-difficulty-classification)


# Part 1 -- Conceptual interview questions and suggested answers

## 1. Introduction to Cypress and architecture

### Q1. What is Cypress, and why is it used in automation testing?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress is a JavaScript-based testing framework primarily used for
automating and testing web applications. It runs tests in a real browser
and provides commands for interacting with the page, making assertions,
stubbing network requests, and debugging test behavior.

It is commonly used for end-to-end and component testing. Its
retryability, automatic waiting behavior, interactive Test Runner, and
network stubbing features help create reliable browser tests.

</details>

### Q2. What are the key features and advantages of Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

-   Interactive Test Runner with a Command Log.
-   Automatic retrying of queries and assertions.
-   Network request interception and stubbing through `cy.intercept()`.
-   Screenshots and video recording options.
-   Time-travel debugging in the Test Runner.
-   Fixtures, custom commands, hooks, and configuration.
-   CI integration and support for multiple browsers.

A candidate should also know that Cypress has its own execution model
and is not simply a wrapper around Selenium WebDriver.

</details>

### Q3. Can you explain the architecture of Cypress? How does Cypress interact with the browser?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Cypress runs in the same run loop as the application under test in the
browser, allowing it to directly interact with the DOM and observe
application behavior. The Cypress Test Runner coordinates test execution
and displays command history, snapshots, and errors.

A simplified view:

``` text
Cypress Test Runner
        |
        | coordinates test commands
        v
Browser
  ├── Application under test
  └── Cypress automation code
        |
        v
Cypress proxy / network layer
        |
        v
Application server and APIs
```

The proxy/network layer enables Cypress to observe and modify HTTP
traffic. Cypress's architecture differs from WebDriver-based tools,
which typically control the browser through a separate driver protocol.

</details>

### Q4. How is Cypress different from Selenium and Playwright?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

-   **Cypress:** JavaScript/TypeScript-oriented, runs closely with the
    browser application, has a command queue, retryability, and built-in
    network interception.
-   **Selenium:** Supports many languages and browsers, uses the
    WebDriver standard, and is suitable for broad browser automation.
-   **Playwright:** Supports several languages, controls browsers
    through browser automation protocols, and provides browser contexts,
    auto-waiting, and multi-page support.

The best choice depends on the team's language, application, browser
requirements, ecosystem, and testing needs.

</details>

### Q5. What is the role of the Cypress Test Runner?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

The Test Runner is the interactive interface used to select and execute
Cypress spec files. It displays test results, command history,
snapshots, errors, and browser activity. It is particularly useful when
developing and debugging tests.

</details>

### Q6. What programming languages can be used with Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress tests are written in JavaScript or TypeScript. A project may
also use HTML, CSS, JSON, and configuration files, but test code itself
uses JavaScript or TypeScript. Cypress is not a Python automation
framework.

</details>

------------------------------------------------------------------------

## 2. Locators and element identification

### Q7. How do you locate web elements in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use Cypress queries such as `cy.get()` for CSS selectors and
`cy.contains()` for text. Prefer stable attributes such as `data-cy` or
`data-testid` rather than fragile styling classes.

``` javascript
cy.get('[data-cy="username"]').type('demo');
cy.contains('button', 'Sign in').click();
```

</details>

### Q8. What is the purpose of the `cy.get()` command?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

`cy.get()` queries the DOM using a selector and yields the matching
element or elements. Cypress retries the query until it finds a match or
the command times out.

``` javascript
cy.get('#email').type('demo@example.com');
```

</details>

### Q9. What is the difference between `cy.get()` and `cy.contains()`?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

-   `cy.get()` finds elements using a selector.
-   `cy.contains()` finds an element containing specified text,
    optionally scoped by a selector.

``` javascript
cy.get('[data-cy="submit"]');
cy.contains('button', 'Submit');
```

Use `cy.contains()` when the visible text is meaningful and stable.

</details>

### Q10. How do you locate elements using CSS selectors and attributes in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress uses CSS selectors with `cy.get()`.

``` javascript
cy.get('#username');                    // ID
cy.get('.login-button');                // class
cy.get('input[name="email"]');          // attribute
cy.get('[data-cy="save"]');             // test attribute
cy.get('button[type="submit"]');        // combined selector
```

A dedicated testing attribute is usually more resilient than a CSS class
used only for styling.

</details>

### Q11. How do you handle multiple elements matching the same selector?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

First scope the query to a meaningful container or make the selector
more specific. If the requirement is genuinely positional, use
`.first()`, `.last()`, or `.eq(index)`.

``` javascript
cy.get('[data-cy="result"]').eq(1).click();
```

Avoid relying on position if the order can change.

</details>

### Q12. What is the purpose of `.first()`, `.last()`, and `.eq()` in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

They select an element from a collection: - `.first()` selects the first
element. - `.last()` selects the last element. - `.eq(index)` selects an
element using a zero-based index.

``` javascript
cy.get('.product').first().click();
cy.get('.product').eq(2).click();
cy.get('.product').last().click();
```

</details>

### Q13. How would you handle dynamic web elements in Cypress?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Use stable attributes, accessible text, or a stable parent container.
Avoid generated IDs and brittle positional selectors. Cypress
automatically retries queries and assertions, so assert the expected
state instead of adding arbitrary delays.

``` javascript
cy.get('[data-cy^="user-row-"]')
  .contains('Asha')
  .should('be.visible');
```

The selector should match the actual DOM and uniquely identify the
intended element.

</details>

### Q14. What is the difference between `cy.get()` and `cy.find()`?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

`cy.get()` starts a new query from the document (or a configured root).
`.find()` searches for descendants of the element yielded by the
previous command.

``` javascript
cy.get('[data-cy="profile-card"]')
  .find('button')
  .contains('Edit')
  .click();
```

Use `.find()` when you want to scope a search inside a previously
selected container.

</details>

------------------------------------------------------------------------

## 3. Handling web elements and user interactions

### Q15. How do you interact with textboxes, buttons, and links in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use commands such as `.type()`, `.clear()`, `.click()`, and assertions
such as `.should()`.

``` javascript
cy.get('#username').type('demo');
cy.get('#password').type('secret');
cy.get('button[type="submit"]').click();
cy.contains('a', 'Forgot password').click();
```

</details>

### Q16. How do you enter text into a textbox and clear its existing value?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `.type()` to enter text and `.clear()` to remove the current value.

``` javascript
cy.get('#search').clear().type('Cypress');
```

</details>

### Q17. How do you handle dropdowns in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

For a native HTML `<select>`, use `.select()`. For a custom dropdown,
click the control and select an option from the rendered list.

``` javascript
cy.get('#country').select('India');
cy.get('#country').should('have.value', 'IN');
```

The selected option's visible label and underlying value may be
different.

</details>

### Q18. How do you select an option from a standard HTML dropdown?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `.select()` with the option's value or visible text.

``` javascript
cy.get('select[name="country"]').select('IN');
cy.get('select[name="country"]').should('have.value', 'IN');
```

You can also use `{ force: true }` in unusual cases, but first
investigate why the control is not actionable normally.

</details>

### Q19. How would you handle a custom dropdown that is not implemented using a `<select>` element?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Treat it as ordinary DOM elements: click the dropdown trigger, wait for
the options to appear, and click the desired option.

``` javascript
cy.get('[data-cy="country-dropdown"]').click();
cy.contains('[role="option"]', 'India').click();
cy.get('[data-cy="country-dropdown"]')
  .should('contain', 'India');
```

Do not use `.select()` for a custom dropdown built from `div`, `li`, or
buttons.

</details>

### Q20. How do you interact with checkboxes and radio buttons in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `.check()` and `.uncheck()` for checkboxes and radio buttons. Verify
the state with `.should('be.checked')` or `.should('not.be.checked')`.

``` javascript
cy.get('#terms').check().should('be.checked');
cy.get('#newsletter').uncheck().should('not.be.checked');
cy.get('input[value="monthly"]').check();
```

</details>

### Q21. How do you perform mouse actions such as hover, click, double-click, and right-click?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress supports `.click()`, `.dblclick()`, and `.rightclick()`. Hover
is not a native high-level Cypress command in the same way as click;
common approaches include triggering relevant events or using a plugin,
depending on how the application implements hover behavior.

``` javascript
cy.get('[data-cy="menu"]').trigger('mouseover');
cy.get('[data-cy="item"]').click();
cy.get('[data-cy="open"]').dblclick();
cy.get('[data-cy="context-target"]').rightclick();
```

For CSS-only hover behavior, a real browser hover may require a suitable
plugin or another supported approach. `.trigger('mouseover')` dispatches
an event but does not always reproduce a real pointer movement.

</details>

### Q22. How do you perform keyboard actions in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `.type()` with key sequences such as `{enter}`, `{esc}`,
`{selectall}`, or modifier combinations.

``` javascript
cy.get('#search').type('Cypress{enter}');
cy.get('#name').type('{selectall}New name');
cy.get('body').type('{esc}');
```

</details>

### Q23. How do you handle alerts and confirmation dialogs in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress automatically accepts browser alerts. To verify alert text,
listen for the `window:alert` event. For confirmation dialogs, Cypress
automatically accepts by default; listen for `window:confirm` and return
`false` to dismiss.

``` javascript
cy.on('window:alert', (text) => {
  expect(text).to.equal('Saved successfully');
});

cy.on('window:confirm', (text) => {
  expect(text).to.include('Are you sure');
  return false; // dismiss the confirmation
});
```

Register the event listener before the action that triggers the dialog.

</details>

### Q24. How do you handle multiple tabs or windows in Cypress?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Cypress generally operates within one browser tab and does not provide
Selenium-style switching between tabs. For links with `target="_blank"`,
a common approach is to remove or change the target and continue in the
same tab. For cross-origin navigation, use `cy.origin()` where supported
and appropriate.

``` javascript
cy.get('a[data-cy="open-report"]')
  .invoke('removeAttr', 'target')
  .click();

cy.url().should('include', '/report');
```

This tests navigation to the destination, but it does not test the
browser's actual new-tab behavior. If that behavior itself is a
requirement, consider whether Cypress is the best tool for that
particular check.

</details>

------------------------------------------------------------------------

## 4. Debugging and test execution

### Q25. How do you debug a failing Cypress test?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use the Cypress Test Runner and Command Log to inspect each command,
snapshots, and failure messages. Use `.debug()`, `.pause()`, browser
DevTools, `cy.log()`, and screenshots as needed.

``` javascript
cy.get('[data-cy="submit"]').debug().click();
```

Also check whether the locator is correct, whether the application state
is ready, and whether an assertion is waiting for the right condition.

</details>

### Q26. What is time-travel debugging in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Time-travel debugging lets a tester select commands in the Command Log
and inspect a snapshot of the application DOM at the point that command
ran. It helps understand what the page looked like before or after an
interaction without manually reproducing every step.

</details>

### Q27. How does the Cypress Command Log help with debugging?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

It displays the commands executed by the test, their status, and details
about the selected command. Selecting a command can show a DOM snapshot
and related information. This makes it easier to identify which step
failed and what the application looked like at that time.

</details>

### Q28. How can you capture screenshots in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `cy.screenshot()` to capture the current application state.

``` javascript
cy.screenshot('checkout-page');
cy.get('[data-cy="submit"]').screenshot('submit-button');
```

Cypress can also capture screenshots automatically on test failures in
supported run configurations. The screenshot folder can be configured in
`cypress.config.js`.

</details>

### Q29. How do you record videos of test execution?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress can record videos during headless `cypress run` execution when
video recording is enabled in configuration.

``` javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  video: true,
});
```

Run:

``` bash
npx cypress run
```

Video behavior and defaults can vary by Cypress version and
configuration. Interactive `cypress open` runs are not generally
recorded in the same way as headless runs.

</details>

### Q30. How do you use `cy.log()` to display messages during test execution?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use `cy.log()` to add readable messages to the Cypress Command Log.

``` javascript
it('logs the login steps', () => {
  cy.log('Open login page');
  cy.visit('/login');

  cy.log('Enter credentials');
  cy.get('#username').type('demo');
  cy.get('#password').type('secret');

  cy.log('Submit login form');
  cy.get('button[type="submit"]').click();
});
```

</details>

### Q31. What is the difference between `console.log()` and `cy.log()`?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

-   `console.log()` writes to the browser's DevTools console (or the
    relevant JavaScript runtime console).
-   `cy.log()` adds a command entry to the Cypress Command Log in the
    Test Runner.

`cy.log()` is useful for readable test steps; `console.log()` is useful
for inspecting JavaScript values.

</details>

### Q32. How do you view browser console errors and network requests during test execution?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Use browser DevTools for console messages and the Network panel for
requests. Cypress can also listen to browser console events with
`cy.window()` and observe or stub network calls using `cy.intercept()`.

``` javascript
cy.visit('/dashboard');

cy.window().then((win) => {
  cy.stub(win.console, 'error').as('consoleErrors');
});
```

For network requests:

``` javascript
cy.intercept('GET', '/api/profile').as('profile');
cy.visit('/dashboard');
cy.wait('@profile');
```

The console stub example must be registered early enough to observe the
messages of interest; for errors emitted during initial page load, use
an appropriate pre-load hook such as `onBeforeLoad` in `cy.visit()`.

</details>

------------------------------------------------------------------------

## 5. Recording and generating automation scripts

### Q33. What is Cypress Studio, and how does it help record user interactions?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Cypress Studio is a feature that can record interactions with an
application and add corresponding Cypress commands to a test. It can
help create an initial test flow, especially for common interactions.
Availability and exact workflow depend on Cypress version and
configuration.

</details>

### Q34. How can you record user actions and convert them into Cypress automation commands?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Use Cypress Studio, when available in the installed version, to open a
test and record actions such as clicking, typing, and selecting. Review
the generated commands, add assertions, and refactor repeated behavior
into helpers or custom commands.

Do not assume that every action or complex workflow can be recorded
accurately.

</details>

### Q35. How do you edit and customize the automation code generated by Cypress Studio?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Treat recorded code as a starting point. Replace brittle selectors with
stable `data-*` attributes, add meaningful assertions, remove
unnecessary steps, use fixtures or parameterized test data, and extract
reusable logic.

</details>

### Q36. What are the advantages and limitations of recording automation scripts instead of writing them manually?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Advantages: - Quick way to create an initial test flow. - Helpful for
beginners learning Cypress syntax. - Captures common user interactions.

Limitations: - Generated selectors may be brittle. - It may not add
meaningful assertions. - Complex logic, test data, API setup, and
reusable architecture still need manual coding. - Recorded tests may
need refactoring for readability and maintainability.

</details>

------------------------------------------------------------------------

## 6. Visual testing

### Q37. What is visual testing, and why is it important in automation testing?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Visual testing checks whether the user interface looks as expected. It
can detect problems such as overlapping elements, incorrect spacing,
missing images, font changes, and unexpected layout shifts that
functional assertions may not detect.

</details>

### Q38. What is visual regression testing?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Visual regression testing compares a current screenshot with an approved
baseline image and highlights visual differences. It helps detect
unintended UI changes after code or styling updates.

</details>

### Q39. How can you identify unintended UI changes using visual testing?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Capture screenshots under consistent conditions and compare them with
approved baselines. Review the difference image and decide whether the
change is a defect or an intentional update. Control viewport size,
browser, fonts, test data, animations, and dynamic content to reduce
false positives.

</details>

### Q40. How can you integrate visual testing into a Cypress automation framework?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Use a visual testing plugin or service that integrates with Cypress.
Capture screenshots of important pages or components and compare them
with stored baselines. Review and approve baseline updates through a
controlled process.

Cypress itself provides screenshot capture, but screenshot capture alone
is not visual regression comparison.

</details>

------------------------------------------------------------------------

## 7. Additional recommended Cypress topics

### Q41. What are the different types of assertions in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress commonly uses Chai assertions through `.should()` and `.and()`,
as well as assertions inside `.then()` callbacks. Common checks include
visibility, text, value, class, attribute, and checked state.

``` javascript
cy.get('#status').should('be.visible');
cy.get('#status').should('have.text', 'Active');
cy.get('#email').should('have.value', 'demo@example.com');
cy.get('#terms').should('be.checked');
```

</details>

### Q42. How does Cypress retry commands and assertions?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Cypress retries linked queries and assertions until they pass or time
out. For example, `cy.get()` can retry while looking for an element, and
`.should()` can retry its assertion. Action commands such as `.click()`
are not blindly replayed after an action has occurred; Cypress waits for
the element to become actionable before performing the action.

This is why tests should generally assert a meaningful condition rather
than use arbitrary `cy.wait(5000)` delays.

</details>

### Q43. What are fixtures in Cypress, and how do you use JSON test data?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Fixtures are files containing reusable test data, commonly JSON. Use
`cy.fixture()` to load them.

``` javascript
cy.fixture('users.json').then((users) => {
  cy.get('#username').type(users.valid.username);
});
```

Fixture files are usually stored in `cypress/fixtures`.

</details>

### Q44. What is the difference between `before`, `beforeEach`, `after`, and `afterEach` hooks?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

-   `before()`: runs once before all tests in the suite.
-   `beforeEach()`: runs before each test.
-   `afterEach()`: runs after each test.
-   `after()`: runs once after all tests in the suite.

``` javascript
describe('Login tests', () => {
  before(() => {
    // One-time suite setup
  });

  beforeEach(() => {
    cy.visit('/login');
  });

  afterEach(() => {
    // Per-test cleanup if needed
  });

  after(() => {
    // One-time suite cleanup
  });

  it('shows the login form', () => {
    cy.get('#username').should('be.visible');
  });
});
```

</details>

### Q45. How do you create and use custom Cypress commands?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Custom commands encapsulate reusable Cypress workflows. They are
commonly defined in `cypress/support/commands.js` or the TypeScript
equivalent and loaded by the support file.

``` javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (username, password) => {
  cy.get('#username').type(username);
  cy.get('#password').type(password, { log: false });
  cy.get('button[type="submit"]').click();
});
```

Use it in a test:

``` javascript
cy.visit('/login');
cy.login('demo', 'secret');
```

Use custom commands for reusable application actions, but avoid turning
every small operation into a command.

</details>

### Q46. What is `cy.intercept()`, and how do you use it?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

`cy.intercept()` spies on, modifies, or stubs network requests and
responses. It is useful for waiting on an API call, controlling test
data, and testing error states.

``` javascript
cy.intercept('GET', '/api/users', {
  statusCode: 200,
  body: [{ id: 1, name: 'Asha' }],
}).as('getUsers');

cy.visit('/users');
cy.wait('@getUsers');
cy.contains('Asha').should('be.visible');
```

</details>

### Q47. What are aliases in Cypress, and how do you use `.as()`?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Aliases give a reusable name to a route, element, fixture, or other
yielded value. Access an alias with `@alias`.

``` javascript
cy.intercept('GET', '/api/orders').as('orders');
cy.visit('/orders');
cy.wait('@orders');

cy.get('[data-cy="order-row"]').as('orderRows');
cy.get('@orderRows').should('have.length.greaterThan', 0);
```

Aliases declared in a test or hook have a lifecycle associated with the
test; do not assume they persist across unrelated tests.

</details>

### Q48. What is `cy.session()`, and how does it help with login optimization?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

`cy.session()` caches and restores browser session data such as cookies,
local storage, and session storage for a given session identifier. It
can reduce repeated login setup.

``` javascript
Cypress.Commands.add('loginSession', (username, password) => {
  cy.session([username], () => {
    cy.visit('/login');
    cy.get('#username').type(username);
    cy.get('#password').type(password, { log: false });
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  }, {
    validate() {
      cy.visit('/dashboard');
      cy.get('[data-cy="user-menu"]').should('be.visible');
    },
  });
});
```

Session caching should be configured carefully. Include all
identity-relevant inputs in the session ID and validate that the
restored session is still usable.

</details>

### Q49. How do you manage environment-specific test data and configuration?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Use Cypress configuration and environment variables rather than
hard-coding environment-specific values in tests. Use `baseUrl` for the
application address and `Cypress.env()` for suitable test configuration
values.

``` javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://test.example.com',
  },
});
```

Run with environment values:

``` bash
npx cypress run --env user=demo
```

Access the value:

``` javascript
const username = Cypress.env('user');
```

Do not commit secrets. Supply credentials through a secure CI secret
store or environment variables.

</details>

### Q50. How do you organize smoke and regression tests in Cypress?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

Organize specs and/or use tags with a tagging plugin or a project
convention. For example, keep critical smoke specs in a dedicated folder
and run them separately in CI. The built-in `--spec` option can select
files.

``` bash
npx cypress run --spec "cypress/e2e/smoke/**/*.cy.js"
npx cypress run --spec "cypress/e2e/regression/**/*.cy.js"
```

If using tags, confirm the selected plugin and its syntax; tags are not
automatically a built-in Cypress marker system like Pytest markers.

</details>

### Q51. How do you configure test retries in Cypress?

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Configure retries in `cypress.config.js`, optionally with different
values for open and run modes.

``` javascript
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  retries: {
    runMode: 2,
    openMode: 0,
  },
});
```

Retries can help identify intermittent failures, but they should not
conceal flaky tests or application defects.

</details>

### Q52. What is `cypress.config.js`, and what configurations can be defined in it?

**Level: Beginner**

<details>
<summary>Answer (click to reveal)</summary>

It is the main Cypress configuration file. It can define E2E and
component testing settings, `baseUrl`, viewport dimensions, retries,
screenshots, videos, timeouts, spec patterns, support files, and event
handlers through `setupNodeEvents`.

``` javascript
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://test.example.com',
    specPattern: 'cypress/e2e/**/*.cy.js',
    setupNodeEvents(on, config) {
      // Register Node-side event handlers or tasks here.
      return config;
    },
  },
  viewportWidth: 1280,
  viewportHeight: 800,
  retries: 1,
});
```

</details>

------------------------------------------------------------------------

<a id="scenario-based-questions"></a>

# Part 2 -- Scenario-based interview questions with answers and solutions

## Scenario 1 -- Two users update the same record simultaneously

**Q53. Two users are updating the same record simultaneously. How will
you test this scenario?**

**Level: Advanced basics**

<details>
<summary>Answer (click to reveal)</summary>

First clarify the expected business rule: should the application use
last-write-wins, optimistic locking, record locking, or conflict
detection? Then create two independent browser sessions or users, load
the same record in both, change it, and submit both updates. Verify that
the final state and user-facing conflict behavior match the requirement.

Cypress example using two isolated browser contexts is not directly
available as a simple built-in test abstraction. A practical Cypress
approach is to use separate browser sessions or independent API requests
to simulate the two users. For example, test the concurrency rule at the
API level and verify the UI conflict message separately.

Illustrative API-level test:

``` javascript
it('rejects a stale update when another user has changed the record', () => {
  cy.request('GET', '/api/records/42').then((response) => {
    const version = response.body.version;

    cy.request('PUT', '/api/records/42', {
      title: 'Updated by user A',
      version,
    }).its('status').should('eq', 200);

    cy.request({
      method: 'PUT',
      url: '/api/records/42',
      failOnStatusCode: false,
      body: {
        title: 'Updated by user B',
        version,
      },
    }).then((secondResponse) => {
      expect(secondResponse.status).to.be.oneOf([409, 412]);
    });
  });
});
```

This illustrates optimistic concurrency using a version field. Adapt the
endpoint, authentication, and expected status to the application's
actual contract. It simulates stale updates sequentially; a true
simultaneous race test may require coordinated requests or a dedicated
concurrency test harness.

</details>

## Scenario 2 -- Slow-loading API causes failures

**Q54. An application has a slow-loading API, causing test failures.
What will you do?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

-   Identify the specific API request using `cy.intercept()`.
-   Wait for that request with `cy.wait('@alias')` rather than using a
    fixed sleep.
-   Set an appropriate request timeout only when justified.
-   Assert the expected UI state after the response.
-   Stub the API when the test is focused on UI behavior and does not
    need to validate the real service.
-   Investigate whether the API itself is genuinely slow or returning
    errors.

``` javascript
it('waits for the product API', () => {
  cy.intercept('GET', '/api/products').as('products');

  cy.visit('/products');

  cy.wait('@products', { timeout: 15000 })
    .its('response.statusCode')
    .should('eq', 200);

  cy.get('[data-cy="product-list"]').should('be.visible');
});
```

Avoid adding long fixed `cy.wait(10000)` calls as the default solution.

</details>

## Scenario 3 -- Automation passes but layout is broken

**Q55. Your automation passes, but the application has a broken layout.
How will you identify it?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Functional tests verify behavior, but they may not detect visual
defects. Add visual regression checks using screenshot comparison, or
assert important layout properties when appropriate.

A screenshot can be captured with:

``` javascript
cy.visit('/dashboard');
cy.screenshot('dashboard-layout');
```

For actual visual comparison, integrate a visual testing tool/plugin
that stores and compares approved baselines. Review differences for
unintended layout changes. Keep viewport, browser, fonts, data, and
animations consistent to reduce false positives.

</details>

## Scenario 4 -- Test passes in Chromium but fails in Firefox

**Q56. A test passes in Chromium but fails in Firefox. How would you
investigate?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

-   Confirm the failure is reproducible in Firefox.
-   Check Cypress/browser compatibility and supported versions.
-   Review browser console errors and network requests.
-   Check timing assumptions, CSS behavior, selectors, and
    browser-specific APIs.
-   Remove brittle fixed waits and use state-based assertions.
-   Compare screenshots and test data.
-   Isolate whether the issue is in the application, Cypress
    configuration, or test code.

Cypress supports multiple browsers, but browser support and feature
availability depend on the Cypress release. Verify the browser is
supported by the installed version.

</details>

## Scenario 5 -- Run tests whenever code is committed

**Q57. Your test suite must run automatically whenever new code is
committed. How would you implement this?**

**Level: Intermediate**

<details>
<summary>Answer (click to reveal)</summary>

Set up a CI pipeline such as GitHub Actions, GitLab CI, Jenkins, or
Azure DevOps. Configure it to install dependencies, start the
application or connect to a test environment, run Cypress headlessly,
and publish screenshots/videos/reports when failures occur.

Example GitHub Actions workflow:

``` yaml
name: Cypress E2E

on:
  push:
    branches: [main]
  pull_request:

jobs:
  cypress:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run Cypress
        uses: cypress-io/github-action@v6
        with:
          install: true
          start: npm run start
          wait-on: 'http://localhost:3000'
          wait-on-timeout: 120
```

The example assumes the project has a valid `package.json`, Cypress
dependency, and `npm run start` script. Pin action versions according to
the organization's security and maintenance policy.

</details>

------------------------------------------------------------------------

# Part 3 -- Practical coding exercises with solutions

Use a practice application or adapt the sample selectors and URLs to the
candidate's test environment.

## Exercise 1 -- Open a website and verify its title

**Level: Beginner**

**Ask:** Write a test that opens the application and verifies its page
title.

``` javascript
describe('Homepage', () => {
  it('shows the expected title', () => {
    cy.visit('/');
    cy.title().should('eq', 'My Application');
  });
});
```

**Evaluate:** `cy.visit()`, `cy.title()`, and assertions.

## Exercise 2 -- Automate a login form

**Level: Beginner**

**Ask:** Enter a username and password, submit the form, and verify
successful login.

``` javascript
it('logs in with valid credentials', () => {
  cy.visit('/login');

  cy.get('[data-cy="username"]').type('standard_user');
  cy.get('[data-cy="password"]').type('secret123', { log: false });
  cy.get('[data-cy="login-button"]').click();

  cy.url().should('include', '/dashboard');
  cy.get('[data-cy="welcome-message"]').should('be.visible');
});
```

**Evaluate:** selectors, interactions, and meaningful assertions.

## Exercise 3 -- Select a value from a dropdown

**Level: Beginner**

**Ask:** Select India from a native dropdown and verify the selected
value.

``` javascript
it('selects India', () => {
  cy.visit('/profile');

  cy.get('#country').select('IN');
  cy.get('#country').should('have.value', 'IN');
});
```

This assumes `IN` is the option's value attribute.

## Exercise 4 -- Select and verify checkboxes

**Level: Beginner**

**Ask:** Check the terms checkbox and verify it is selected.

``` javascript
it('accepts terms', () => {
  cy.visit('/register');

  cy.get('#terms').check();
  cy.get('#terms').should('be.checked');

  cy.get('#newsletter').uncheck();
  cy.get('#newsletter').should('not.be.checked');
});
```

## Exercise 5 -- Verify text on a page

**Level: Beginner**

**Ask:** Verify that a success message is displayed.

``` javascript
it('shows a success message', () => {
  cy.visit('/profile');
  cy.contains('Profile updated successfully').should('be.visible');
});
```

## Exercise 6 -- Intercept an API request and validate its response

**Level: Intermediate**

**Ask:** Intercept a users API request, wait for it, and verify the
response.

``` javascript
it('loads users from the API', () => {
  cy.intercept('GET', '/api/users').as('users');

  cy.visit('/users');

  cy.wait('@users').then(({ response }) => {
    expect(response.statusCode).to.eq(200);
    expect(response.body).to.be.an('array');
  });
});
```

## Exercise 7 -- Create a reusable login command

**Level: Intermediate**

**Ask:** Create a custom command for logging in.

``` javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (username, password) => {
  cy.get('[data-cy="username"]').type(username);
  cy.get('[data-cy="password"]').type(password, { log: false });
  cy.get('[data-cy="login-button"]').click();
});
```

Use it:

``` javascript
it('logs in using a custom command', () => {
  cy.visit('/login');
  cy.login('standard_user', 'secret123');
  cy.url().should('include', '/dashboard');
});
```

## Exercise 8 -- Read test data from a JSON fixture

**Level: Beginner**

**Ask:** Load user credentials from a JSON fixture and use them in a
login test.

Example `cypress/fixtures/users.json`:

``` json
{
  "validUser": {
    "username": "standard_user",
    "password": "secret123"
  }
}
```

Test:

``` javascript
it('logs in using fixture data', () => {
  cy.fixture('users').then((users) => {
    cy.visit('/login');
    cy.get('[data-cy="username"]').type(users.validUser.username);
    cy.get('[data-cy="password"]').type(
      users.validUser.password,
      { log: false }
    );
    cy.get('[data-cy="login-button"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

## Exercise 9 -- Execute only smoke tests

**Level: Beginner**

**Ask:** Organize smoke tests separately and execute only those tests.

Example structure:

``` text
cypress/
└── e2e/
    ├── smoke/
    │   └── login.cy.js
    └── regression/
        └── orders.cy.js
```

Run smoke specs:

``` bash
npx cypress run --spec "cypress/e2e/smoke/**/*.cy.js"
```

This uses file organization rather than assuming Cypress has built-in
Pytest-style markers.

## Exercise 10 -- Capture a screenshot on failure

**Level: Intermediate**

**Ask:** Configure Cypress to capture screenshots when tests fail.

``` javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  screenshotsFolder: 'cypress/screenshots',
  screenshotOnRunFailure: true,
});
```

Run tests:

``` bash
npx cypress run
```

Cypress captures screenshots on failures in supported run-mode
configurations. Verify behavior for the installed version and
configuration.

## Exercise 11 -- Record browser interactions using Cypress Studio

**Level: Intermediate**

**Ask:** Demonstrate how you would record a simple login flow using
Cypress Studio and then improve the generated test.

**Expected approach**

1.  Open the Cypress Test Runner.
2.  Open a spec that can be extended using Studio.
3.  Start the Studio recording workflow supported by the installed
    Cypress version/configuration.
4.  Interact with the application: enter credentials and click Sign in.
5.  Review the generated commands.
6.  Replace unstable selectors with stable `data-cy` attributes.
7.  Add assertions for the expected login outcome.
8.  Remove unnecessary actions and refactor repeated steps.

**Evaluate:** understanding of the recording workflow and ability to
improve generated code. Do not award full credit just for recording
clicks without assertions.

## Exercise 12 -- Add a visual regression check

**Level: Intermediate**

**Ask:** Explain how you would detect unintended visual changes in a
dashboard.

**Expected approach**

1.  Choose a visual testing plugin or service compatible with the
    Cypress version.
2.  Capture a baseline screenshot of the dashboard.
3.  Run the same test in a consistent environment.
4.  Compare the new screenshot with the baseline.
5.  Review the difference image.
6.  Update the baseline only when the visual change is intentional and
    approved.

Cypress screenshot capture by itself is not visual comparison. The
candidate should identify the need for a visual regression tool or
service.

------------------------------------------------------------------------

# Part 4 -- Quick-reference Cypress commands

  ----------------------------------------------------------------------------------------
  Goal                                Command
  ----------------------------------- ----------------------------------------------------
  Open Cypress Test Runner            `npx cypress open`

  Run tests headlessly                `npx cypress run`

  Run a specific spec                 `npx cypress run --spec "cypress/e2e/login.cy.js"`

  Set a base URL                      Configure `baseUrl` in `cypress.config.js`

  Visit a page                        `cy.visit('/login')`

  Find an element                     `cy.get('[data-cy="login"]')`

  Find text                           `cy.contains('Welcome')`

  Type text                           `cy.get('#name').type('Asha')`

  Clear a field                       `cy.get('#name').clear()`

  Click an element                    `cy.get('button').click()`

  Select a native dropdown option     `cy.get('select').select('IN')`

  Check a checkbox                    `cy.get('#terms').check()`

  Uncheck a checkbox                  `cy.get('#terms').uncheck()`

  Assert visible                      `.should('be.visible')`

  Assert text                         `.should('contain', 'Welcome')`

  Wait for an aliased request         `cy.wait('@users')`

  Intercept a request                 `cy.intercept('GET', '/api/users').as('users')`

  Load a fixture                      `cy.fixture('users')`

  Capture screenshot                  `cy.screenshot('page')`

  Add Command Log message             `cy.log('Step 1')`

  Debug a yielded element             `.debug()`

  Pause execution                     `cy.pause()`
  ----------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Part 5 -- Question-by-question difficulty classification

    Question Topic (short form)                    Level
  ---------- ------------------------------------- -----------------
           1 What is Cypress?                      Beginner
           2 Features and advantages               Beginner
           3 Cypress architecture                  Intermediate
           4 Cypress vs Selenium vs Playwright     Intermediate
           5 Test Runner                           Beginner
           6 Supported test languages              Beginner
           7 Locating elements                     Beginner
           8 `cy.get()`                            Beginner
           9 `cy.get()` vs `cy.contains()`         Beginner
          10 CSS and attribute selectors           Beginner
          11 Multiple matching elements            Beginner
          12 `.first()`, `.last()`, `.eq()`        Beginner
          13 Dynamic elements                      Intermediate
          14 `cy.get()` vs `.find()`               Beginner
          15 Basic web element interactions        Beginner
          16 Typing and clearing text              Beginner
          17 Dropdown handling                     Beginner
          18 Native dropdown selection             Beginner
          19 Custom dropdowns                      Intermediate
          20 Checkboxes and radio buttons          Beginner
          21 Mouse actions and hover               Beginner
          22 Keyboard actions                      Beginner
          23 Alerts and confirmation dialogs       Beginner
          24 Multiple tabs/windows                 Intermediate
          25 Debugging failing tests               Beginner
          26 Time-travel debugging                 Beginner
          27 Command Log                           Beginner
          28 Screenshots                           Beginner
          29 Video recording                       Beginner
          30 `cy.log()`                            Beginner
          31 `console.log()` vs `cy.log()`         Beginner
          32 Console errors and network requests   Intermediate
          33 Cypress Studio                        Intermediate
          34 Recording user actions                Intermediate
          35 Editing generated code                Intermediate
          36 Recording vs manual automation        Beginner
          37 Visual testing                        Beginner
          38 Visual regression testing             Beginner
          39 Detecting visual changes              Intermediate
          40 Visual testing integration            Intermediate
          41 Cypress assertions                    Beginner
          42 Automatic retries                     Beginner
          43 Fixtures and JSON data                Beginner
          44 Hooks                                 Beginner
          45 Custom commands                       Intermediate
          46 `cy.intercept()`                      Intermediate
          47 Aliases and `.as()`                   Intermediate
          48 `cy.session()`                        Intermediate
          49 Environment configuration             Beginner
          50 Smoke and regression organization     Beginner
          51 Test retries                          Intermediate
          52 `cypress.config.js`                   Beginner
          53 Concurrent updates to one record      Advanced basics
          54 Slow API                              Intermediate
          55 Broken layout despite passing tests   Intermediate
          56 Chromium pass, Firefox fail           Intermediate
          57 CI execution on code commit           Intermediate

## Practical exercise difficulty

    Exercise Topic                         Level
  ---------- ----------------------------- --------------
           1 Verify page title             Beginner
           2 Automate login                Beginner
           3 Select dropdown option        Beginner
           4 Check/uncheck controls        Beginner
           5 Verify page text              Beginner
           6 Intercept and validate API    Intermediate
           7 Create custom login command   Intermediate
           8 Read JSON fixture             Beginner
           9 Run smoke tests               Beginner
          10 Screenshot on failure         Intermediate
          11 Record with Cypress Studio    Intermediate
          12 Visual regression workflow    Intermediate

------------------------------------------------------------------------

# Part 6 -- Suggested beginner interview plan

For a 45--60 minute interview, select a representative set rather than
asking every question.

  -----------------------------------------------------------------------------
  Section                                  Suggested time What to assess
  -------------------------- ---------------------------- ---------------------
  Cypress basics and                             5--7 min Framework purpose and
  architecture                                            execution model

  Locators and interactions                        10 min Selectors, forms,
                                                          dropdowns, assertions

  Debugging and                                 8--10 min Retryability, Command
  synchronization                                         Log, screenshots

  Fixtures and reusable code                    8--10 min JSON, hooks, custom
                                                          commands

  Practical coding                             10--15 min Candidate can write
                                                          and explain a test

  Scenario/troubleshooting                       5--8 min Network, visual
                                                          defects, CI, browser
                                                          issues
  -----------------------------------------------------------------------------

## Suggested evaluation weighting

-   **Beginner fundamentals -- 50%:** Cypress basics, locators,
    interactions, assertions, fixtures, and hooks.
-   **Intermediate application -- 35%:** Intercepts, custom commands,
    aliases, sessions, debugging, and CI.
-   **Advanced basics -- 15%:** Concurrency, visual regression,
    cross-browser troubleshooting, and pipeline design.

## Interviewer tips

-   Ask candidates to explain why they chose a selector.
-   Look for stable selectors such as `data-cy` rather than fragile
    styling classes.
-   Check that candidates understand Cypress's command queue and
    retryability.
-   Ask them to distinguish a native `<select>` dropdown from a custom
    dropdown.
-   For API scenarios, look for `cy.intercept()` and alias-based waiting
    rather than arbitrary fixed waits.
-   For visual testing, ensure candidates understand that screenshot
    capture and screenshot comparison are different capabilities.
-   For concurrency, expect candidates to clarify the application's
    conflict-handling rule before proposing a test.
-   For CI/CD, look for a repeatable headless run and preserved
    artifacts on failure.

## Environment and version note

Examples use Cypress with JavaScript and the E2E testing configuration.
Install Cypress through the project's package manager and use the
version locked by the project. Commands, browser support, Studio
availability, and video behavior can vary by release. Keep secrets out
of source control and use CI secret management for credentials.
