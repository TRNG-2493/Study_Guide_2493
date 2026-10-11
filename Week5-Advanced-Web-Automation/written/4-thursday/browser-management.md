# Browser Management in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- List the browsers Cypress supports (Chrome, Chromium, Edge, Firefox, Electron, and experimental WebKit) and explain how Cypress finds them on your machine.
- Choose a browser with the `--browser` flag in `cypress run` and with the browser selector in `cypress open`.
- Explain the difference between **headed** and **headless** execution and use `--headed`, `--headless`, and `--no-exit` appropriately.
- Explain the difference between `cypress open` (interactive Test Runner) and `cypress run` (command-line runner), and when to use each.
- Control viewport size globally (configuration), per spec or per test (`cy.viewport`), and for device presets (for example `'iphone-x'`).
- Pass launch options to browsers using the `before:browser:launch` event.
- Run the same tests across several browsers, and compare this with how Playwright handled browsers on Monday through Wednesday.

---

## Why This Matters

Users do not all use the same browser. Your company's customers might use Chrome on Windows, Safari on iPhone, and Edge at work. A rendering bug that appears only in Firefox is still a bug, and the cheapest place to find it is your automated suite.

This week's epic is to master UI automation in Playwright and then learn Cypress for a cross-tool perspective. Browser handling is a place where the two tools differ noticeably, and your Project 1 comparison note should address it:

| Topic | Playwright | Cypress |
|---|---|---|
| Browsers installed by | `playwright install` downloads its own patched Chromium, Firefox, WebKit | Cypress uses browsers **already installed on your machine** (plus its bundled Electron) |
| Choose browser | `--browser chromium/firefox/webkit` or `projects` in config | `--browser chrome/edge/firefox/electron` |
| WebKit / Safari engine | First-class | Experimental |
| Default mode | Headless | `cypress run` is headless; `cypress open` is headed |
| Multiple browsers in one run | Multiple `projects` run in one command | One browser per command; loop in a CI matrix or npm script |
| Viewport | `viewport` in context / config | `viewportWidth/Height` in config and `cy.viewport()` |
| Mobile emulation | Device descriptors (`playwright.devices`) | Viewport presets plus (optionally) a user agent setting |

Understanding browser management also helps with CI: a pipeline typically has Chrome pre-installed, uses headless mode, and needs the correct `--browser` flag. Mistakes here show up as the "I cannot find the browser" error that wastes teams' hours.

---

## The Concept

### 1. Browsers that Cypress supports

Cypress can run your tests in the following browsers:

| Browser | Notes |
|---|---|
| **Chrome** | Google Chrome (stable, beta, dev, canary channels). Most commonly used in CI and by developers. |
| **Chromium** | The open-source base of Chrome. Often found on Linux servers. |
| **Edge** | Microsoft Edge (Chromium-based). Supported on Windows, macOS, Linux. |
| **Firefox** | Mozilla Firefox, supported on all platforms. |
| **Electron** | The browser **bundled inside Cypress itself**. No installation needed. It is Chromium-based and is the default for `cypress run`. |
| **WebKit (experimental)** | Cypress offers an experimental WebKit option (enabled with `experimentalWebKitSupport: true` in the configuration and installing the `playwright-webkit` npm package). Not suitable as your only cross-browser strategy, and you should check the current docs before relying on it. |

**Important concept: Cypress does not download the browsers for you** (except Electron, which ships inside the Cypress binary). When you run `npx cypress open`, Cypress scans your machine for installed browsers and lists the ones it detects. If Chrome is not installed, Chrome will not appear in the list.

Contrast with Playwright: when you ran `playwright install` earlier this week, it downloaded special builds of Chromium, Firefox, and WebKit that the library controls. That is why Playwright tests behave identically on every machine. In Cypress, the version of Chrome on your laptop might differ from the version on the CI server; this can cause "works on my machine" differences, so pin or document your browser versions in CI.

#### 1.1 Seeing which browsers Cypress detects

```bash
npx cypress info
```

This prints a report including: Cypress version, binary path, detected browsers with versions and paths, and OS/proxy information. It is the first command to run when "Cypress cannot find my browser."

### 2. `cypress open` versus `cypress run`

Cypress has two primary modes. Understanding them is fundamental.

#### 2.1 `cypress open` - the interactive Test Runner

```bash
npx cypress open
```

- Opens the **Launchpad**, then the **Test Runner**, with a graphical interface.
- You choose **E2E Testing** or **Component Testing**, then a **browser**, then a **spec**.
- Tests run in a **visible (headed)** browser window. The Command Log, time-travel snapshots, selector playground, and DevTools are available.
- Watches your files: saving a spec re-runs it automatically (a "watch mode" feature).
- Retries default to **0** in open mode (`retries.openMode`), so failures are shown immediately.
- Use it **while developing and debugging tests**.

You can also skip the Launchpad choices using flags:

```bash
npx cypress open --e2e --browser chrome
```

- `--e2e` jumps directly into E2E mode.
- `--browser chrome` pre-selects Chrome.

#### 2.2 `cypress run` - the command-line runner

```bash
npx cypress run
```

- Runs all specs without a graphical interface (by default, headless Electron).
- Prints results to the terminal and exits with a **status code**: `0` if all tests passed, otherwise the number of failed tests (up to 254, with other special codes). CI systems rely on that exit code to mark a build pass or fail.
- Supports **retries** (`runMode`), screenshots on failure, and optional video.
- Use it **for CI, scheduled runs, and smoke checks**.

| Feature | `cypress open` | `cypress run` |
|---|---|---|
| Interface | GUI | Terminal |
| Default browser | You choose in UI | Electron (headless) |
| Visible browser | Yes | No (unless `--headed`) |
| File watching and re-run | Yes | No |
| Retries default | `openMode: 0` | `runMode` as configured |
| Ideal for | Writing and debugging | CI and batch runs |

A common beginner mistake is to use `cypress open` in a CI pipeline (there is no screen, so it fails) or to debug using only `cypress run` (you lose the visual feedback that makes Cypress valuable).

### 3. Choosing a browser with `--browser`

#### 3.1 In `cypress run`

```bash
npx cypress run --browser chrome
npx cypress run --browser firefox
npx cypress run --browser edge
npx cypress run --browser electron
```

You can also provide a *path* to a browser executable, or a channel:

```bash
npx cypress run --browser chrome:canary
npx cypress run --browser /usr/bin/chromium
```

- `chrome:canary` selects a specific release channel of Chrome (`stable`, `beta`, `dev`, `canary`).
- A path is useful on Linux CI where Chromium sits in a custom location.

If the requested browser is not found, Cypress aborts with an error listing the browsers it *did* find. That list is exactly what `cypress info` would show.

#### 3.2 Using environment-aware npm scripts

```json
{
  "scripts": {
    "cy:open": "cypress open",
    "cy:run": "cypress run",
    "cy:run:chrome": "cypress run --browser chrome",
    "cy:run:firefox": "cypress run --browser firefox",
    "cy:run:edge": "cypress run --browser edge",
    "cy:run:all": "npm run cy:run:chrome && npm run cy:run:firefox"
  }
}
```

**Explanation:**

- Each key under `scripts` is a name you invoke with `npm run <name>`.
- `cy:run:all` uses `&&` to run the Chrome command and *only if it succeeds* the Firefox command. If Chrome fails, Firefox does not run; use `;` or a CI matrix if you want both to run regardless.

This is the equivalent of Playwright's `projects` array, but spread across commands, because **Cypress runs one browser per invocation**. A CI matrix (for example a GitHub Actions job strategy with `browser: [chrome, firefox, edge]`) is the usual way to run browsers in parallel.

### 4. Headed versus headless

A **headless** browser runs without a visible window. It still renders the page and runs JavaScript, but the output is not drawn to a screen. A **headed** browser opens a real window.

| | Headed | Headless |
|---|---|---|
| Speed | Slightly slower (rendering to screen) | Faster, less memory |
| Debugging | Watch it run | Not visible |
| CI use | Needs a virtual display (Xvfb) on Linux | Works without display |
| Reliability of results | Same as headless in nearly all cases | Same |

#### 4.1 Defaults

- `cypress open` is always headed.
- `cypress run` is headless by default **for Electron**. For Chrome, Edge, and Firefox, `cypress run` also runs headless by default; you can force a visible window with `--headed`.

```bash
npx cypress run --headed                    # watch tests run in Electron (visible)
npx cypress run --browser chrome --headed   # visible Chrome window
npx cypress run --browser chrome --headless # explicitly headless (the default)
```

#### 4.2 `--no-exit`

```bash
npx cypress run --headed --no-exit
```

Normally the browser closes after the run. `--no-exit` keeps it open so you can inspect the final state of the application and use DevTools. Useful for investigating "why did this one test fail on `run` but pass on `open`?"

#### 4.3 Choosing between them

- Developing: `cypress open`.
- Quick local check of the full suite: `cypress run` (headless).
- Debugging a CI-only failure: `cypress run --headed --no-exit --browser <same browser>`.
- CI: headless; always specify `--browser` so the browser is predictable.

### 5. Viewport

The **viewport** is the size of the browser's visible page area, in CSS pixels. It determines which layout your application renders: a desktop navigation bar at 1280 wide may collapse into a "hamburger" menu at 375 wide. If your tests rely on an element that is hidden at small widths, they might fail in CI for a reason you do not see locally.

The default Cypress viewport is **1000 x 660** pixels.

#### 5.1 Set globally in config

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    viewportWidth: 1280,
    viewportHeight: 720,
  },
});
```

Every test in the project begins with this viewport.

#### 5.2 Change inside a test with `cy.viewport()`

```js
cy.viewport(375, 667);          // width, height in pixels
cy.viewport('iphone-x');        // a named preset
cy.viewport('ipad-2', 'landscape'); // preset with orientation
```

**Presets available** include: `macbook-16`, `macbook-15`, `macbook-13`, `macbook-11`, `ipad-2`, `ipad-mini`, `iphone-xr`, `iphone-x`, `iphone-6+`, `iphone-se2`, `iphone-8`, `iphone-7`, `iphone-6`, `iphone-5`, `iphone-3`, `samsung-s10`, `samsung-note9`. Check the `cy.viewport` documentation for the current list.

Important: `cy.viewport` **resets for each test** (the next test starts again with the configured default), so you will typically call it in a `beforeEach` or at the top of a test.

#### 5.3 Viewports and `cypress run`

Headless runs often default to different window sizes from what you see in `cypress open`, which is why explicit `viewportWidth`/`viewportHeight` in the config is a best practice. It removes one variable from "works on my machine."

#### 5.4 Responsive testing loops

```js
const sizes = [
  ['iphone-6', 'portrait'],
  ['ipad-2', 'portrait'],
  [1280, 720],
];

sizes.forEach((size) => {
  describe(`Header at ${size}`, () => {
    beforeEach(() => {
      if (Array.isArray(size)) {
        cy.viewport(...size);
      } else {
        cy.viewport(size);
      }
      cy.visit('/');
    });

    it('shows the logo', () => {
      cy.get('[data-test="logo"]').should('be.visible');
    });
  });
});
```

(Do not worry about the fine details of the `[data-test="logo"]` selector; it is a placeholder.) The loop generates a separate `describe` for each viewport so each result appears separately in the report. Note that normal JavaScript loops *can* generate tests, because describe/it registration happens synchronously at load time, unlike `cy` commands, which are queued.

Playwright comparison: Playwright allows you to supply `viewport` or a complete **device descriptor** (including user agent, `isMobile`, `hasTouch`, device pixel ratio) in the context or project configuration. Cypress's presets change only the **size**. If you also need a mobile user agent, set `userAgent` in the config (`userAgent: 'Mozilla/5.0 (iPhone; ...)'`) or via an intercept header.

### 6. Browser launch options (advanced)

Cypress lets you adjust how the browser starts through the `before:browser:launch` event, registered in `setupNodeEvents`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      on('before:browser:launch', (browser = {}, launchOptions) => {
        if (browser.family === 'chromium' && browser.name !== 'electron') {
          launchOptions.args.push('--window-size=1400,900');
          launchOptions.args.push('--disable-dev-shm-usage');
        }
        if (browser.family === 'firefox') {
          launchOptions.args.push('-width', '1400', '-height', '900');
        }
        return launchOptions;
      });
      return config;
    },
  },
});
```

**Line-by-line explanation:**

1. `on('before:browser:launch', ...)` registers a handler that runs in Node, just before Cypress starts the browser.
2. `(browser = {}, launchOptions)` - `browser` describes which browser is about to start (`name`, `family`, `version`, `isHeadless`...). `launchOptions` is an object with `args` (command-line switches), `preferences`, and `extensions`.
3. `browser.family === 'chromium' && browser.name !== 'electron'` - Chrome, Chromium and Edge are in the `chromium` family; Electron is also chromium-family but uses different options, so we exclude it with the second condition.
4. `launchOptions.args.push('--window-size=1400,900')` - Adds a Chrome switch to set the window size (relevant to headed mode).
5. `'--disable-dev-shm-usage'` - A common Chrome switch for Docker containers with limited shared memory; prevents crashes in CI.
6. For Firefox, we use its own switches for width and height.
7. `return launchOptions;` - You *must* return the object for your changes to apply.

Use launch options sparingly; they make your test environment differ from user reality. Common legitimate uses: Docker shared memory flag, enabling a browser extension, disabling a first-run popup, setting a download directory.

### 7. Cross-browser strategy in practice

A practical approach many teams use:

1. **Develop in Chrome** (`cypress open`). Fast, familiar DevTools.
2. **Run the full suite on Chrome in CI** for every pull request.
3. **Run a smaller smoke subset on Firefox and Edge** on a nightly schedule or before release. (How to select a subset is covered in the "Test selection" lesson.)
4. **Use Electron** as a quick default; remember it is Chromium-based, so it does not give extra cross-browser coverage compared with Chrome.
5. **Treat WebKit as experimental** and verify Safari behaviour manually or with Playwright (which has stable WebKit support). This is a real argument for using both tools in a larger organization.

### 8. Other browser-related settings you will meet

| Setting | Where | Purpose |
|---|---|---|
| `chromeWebSecurity` | config | Set `false` to disable same-origin enforcement in Chromium-family browsers (use `cy.origin` instead when possible). |
| `userAgent` | config | Override the browser's user agent string. |
| `pageLoadTimeout` | config | Max time for `cy.visit`/page load (default 60000 ms). |
| `downloadsFolder` | config | Where downloaded files are saved. |
| `video` | config | Record a video during `cypress run` (default is `false` as of Cypress 13); details on Friday. |
| `screenshotOnRunFailure` | config | Take screenshots when a test fails during `run`; details on Friday. |
| `testIsolation` | config | Default true; clears browser state between tests. |

Videos, screenshots and debugging with the runner are **covered in depth on Friday**; for now just know they exist.

### 9. Verifying which browser you are running

Sometimes you want a test to behave differently by browser or to log the browser in use. Cypress exposes it:

```js
it('reports the browser', () => {
  cy.log(`Browser: ${Cypress.browser.name} ${Cypress.browser.version}`);
  cy.log(`Headless: ${Cypress.browser.isHeadless}`);
});
```

`Cypress.browser` contains `name`, `family`, `channel`, `displayName`, `version`, `path`, `isHeadless`, `isHeaded`. Combined with Mocha's ability to skip tests, you can write conditional tests:

```js
it('uses a Chrome-only feature', function () {
  if (Cypress.browser.family !== 'chromium') {
    this.skip();
  }
  // Chrome-specific steps here
});
```

Here `this.skip()` is a Mocha method that marks the test as pending. Because it uses `this`, the callback must be a regular `function`, not an arrow function. (Cypress also has a built-in `Cypress.isBrowser('chrome')` helper and an `{ browser: 'chrome' }` test configuration option; examples below.)

```js
it('runs only on Firefox', { browser: 'firefox' }, () => {
  // runs only in Firefox, skipped elsewhere
});

it('runs on everything except Firefox', { browser: '!firefox' }, () => {
  // negation with !
});
```

The `{ browser: ... }` object between title and function is **test configuration**; it overrides configuration or filters per test. We expand on this in "Assertions and annotations" and "Test selection".

---

## Code Examples

### Example 1: A responsive layout check

```js
describe('Responsive navigation (Sauce Demo)', () => {
  const login = () => {
    cy.visit('/');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
  };

  it('desktop shows the product list', () => {
    cy.viewport(1280, 720);
    login();
    cy.get('.inventory_item').should('have.length.greaterThan', 0);
  });

  it('iPhone shows the product list in a narrower layout', () => {
    cy.viewport('iphone-x');
    login();
    cy.get('.inventory_item').should('have.length.greaterThan', 0);
    cy.get('.inventory_item').first().should('be.visible');
  });
});
```

**Explanation:**

- `const login = () => {...}` defines a plain JavaScript helper that *queues* four Cypress commands whenever it is called. (Custom commands, taught in the Fixtures lesson, are a more Cypress-idiomatic way to share this.)
- `cy.viewport(1280, 720)` must be called **before** `cy.visit` so the page renders at that size from the start.
- `should('have.length.greaterThan', 0)` is a Chai-jQuery assertion on how many elements `cy.get` found.
- `.first().should('be.visible')` asserts that the first product card is visible in the narrower viewport.

### Example 2: A per-browser smoke script

```bash
#!/usr/bin/env bash
# run-matrix.sh - run the smoke tests in each installed browser
for b in chrome firefox edge; do
  echo "=== Running in $b ==="
  npx cypress run --browser "$b" --spec "cypress/e2e/smoke/**/*.cy.js" || echo "FAILED in $b"
done
```

**Explanation:** a shell loop runs the same command with a different `--browser` each time; `|| echo` prevents the loop from stopping after a failure; `--spec` limits to smoke tests (covered in the Test Selection lesson). On a CI system you would replace the loop with a matrix.

### Example 3: Logging environment details

```js
beforeEach(() => {
  cy.log(`Running in ${Cypress.browser.displayName} v${Cypress.browser.version}`);
  cy.log(`Viewport: ${Cypress.config('viewportWidth')} x ${Cypress.config('viewportHeight')}`);
});
```

**Explanation:** `Cypress.config('key')` reads a configuration value at runtime. This is useful for diagnosing why a test passes locally but fails in CI.

### Example 4: The same intent in Playwright (Python) for comparison

```python
# pytest-playwright
# pytest --browser chromium --browser firefox --headed
def test_title(page):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("https://www.saucedemo.com")
    assert "Swag Labs" in page.title()
```

Contrast: Playwright can run two browsers in a single command (`--browser` repeated), uses its own bundled browsers, and sets viewport on `page`. Cypress runs one browser per command, uses the machine's installed browsers, and sets viewport using `cy.viewport`.

---

## Real-World Scenarios

1. **"It passes in Chrome but fails in Firefox."** A date input behaves differently between browsers. Because you can run `cypress run --browser firefox` locally or in CI, you reproduce the failure and file a precise bug.
2. **Mobile menu regression.** After a CSS refactor, the hamburger menu disappears on phone widths. A test that sets `cy.viewport('iphone-x')` and clicks the menu button catches it before customers do.
3. **Docker CI crashes.** A pipeline running Chrome in Docker intermittently crashes with "Aw, Snap!". Adding `--disable-dev-shm-usage` via `before:browser:launch` stabilises it.
4. **Release gate.** The team runs the entire suite on Chrome for each pull request (5 minutes) but only 15 smoke tests on Firefox and Edge before a release candidate.
5. **Safari bug reports from customers.** Because Cypress WebKit is experimental, the QA lead keeps a handful of critical flows in Playwright where WebKit is stable. Knowing both tools lets you design this hybrid.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Assuming Cypress installs browsers.**
It does not. If CI says "Can't run because you've entered an invalid browser name," install Chrome in the pipeline image or use Cypress's official Docker images (for example `cypress/browsers` and `cypress/included`) that include them.

**Pitfall 2: Setting the viewport after `cy.visit`.**
Layout is determined at load time for responsive sites; call `cy.viewport` first. (Many apps re-layout on resize, so it sometimes works, but being consistent avoids flaky behaviour.)

**Pitfall 3: Relying on the default viewport.**
Different runs may use different default sizes. Always set `viewportWidth`/`viewportHeight` in config.

**Pitfall 4: Using `cypress open` in CI.**
It needs a display and a human. Use `cypress run`.

**Pitfall 5: Confusing Electron with "a different browser."**
Electron is Chromium-based; a pass in Electron says little about Firefox or Safari.

**Pitfall 6: Over-customising launch args.**
Each flag makes the test environment less like a real user's. Document each flag with a comment explaining why it exists.

**Pitfall 7: Forgetting that `cy.viewport` resets per test.**
If a later test has the wrong layout, check you called `cy.viewport` in `beforeEach`.

**Best practices**

- Pass `--browser` explicitly in CI commands.
- Keep a `cy:run:<browser>` script for each supported browser.
- Run the full suite in one browser and a smoke subset in the others.
- Log `Cypress.browser` details at the start of failing builds.
- Always set a viewport in config.

---

## Mini Practice Exercises

**Exercise 1 - Discover.**
Run `npx cypress info`. List the browsers detected, their versions, and paths. Which one will `cypress run` use if you pass no flag?

*Answer:* Electron.

**Exercise 2 - Run in two browsers.**
Write a spec `cypress/e2e/title.cy.js` that visits `https://example.cypress.io` and asserts the title contains "Kitchen Sink". Run it with `--browser electron` and `--browser chrome` (and Firefox if installed). Then run with `--headed`.

*Hint:* the code is the same as the lesson-1 smoke test.

**Exercise 3 - Viewport.**
Write a test that visits `https://example.cypress.io`, sets the viewport to `iphone-x`, and asserts that the element `.navbar-toggle` (the collapsed menu button on that site; confirm it in DevTools) is visible. Then set the viewport to `macbook-15` and assert that it is *not* visible.

*Solution outline:*

```js
it('toggles nav by viewport', () => {
  cy.viewport('iphone-x');
  cy.visit('https://example.cypress.io');
  cy.get('.navbar-toggle').should('be.visible');

  cy.viewport('macbook-15');
  cy.get('.navbar-toggle').should('not.be.visible');
});
```

(If the selector differs, inspect the page and adjust. Resizing mid-test is allowed.)

**Exercise 4 - Browser-specific test.**
Write a test that only runs in Chrome-family browsers using the `{ browser: ... }` option. What would you pass for "everything except Electron"?

*Answer:* `{ browser: '!electron' }`.

**Exercise 5 - Launch option.**
Add a `before:browser:launch` handler that logs `browser.name` and `browser.isHeadless` using `console.log` and then returns `launchOptions` unchanged. Run `cypress run` and `cypress run --headed`. Observe how `isHeadless` changes.

**Exercise 6 - Compare.**
In your Project 1 comparison note, add a paragraph answering: "If our product must work in Safari, which tool would I choose for those tests and why?" Use evidence from this lesson.

---

## Summary / Key Takeaways

- Cypress supports Chrome, Chromium, Edge, Firefox, Electron (bundled), and experimental WebKit. It uses **browsers installed on your machine**, unlike Playwright, which downloads its own.
- `cypress open` is the interactive, headed, watch-mode runner for **development**; `cypress run` is the command-line, headless, exit-code-driven runner for **CI**.
- Use `--browser <name|path>`, `--headed`, `--headless`, and `--no-exit` to control execution. `npx cypress info` shows detected browsers.
- Viewport defaults to 1000 x 660. Set `viewportWidth`/`viewportHeight` in config, and use `cy.viewport(width, height)` or a preset such as `'iphone-x'` inside tests; it resets for each test.
- `before:browser:launch` lets you add browser switches; use sparingly.
- `Cypress.browser` and the `{ browser: ... }` test option let you tailor tests by browser.
- Strategy: develop in Chrome, run full suite on one browser, smoke on others; use Playwright for stable WebKit coverage.
- Time-travel debugging, screenshots, and video options mentioned here are **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - Launching Browsers: https://docs.cypress.io/app/guides/launching-browsers
- Cypress Documentation - Command Line (`cypress open`, `cypress run`, flags): https://docs.cypress.io/app/references/command-line
- Cypress Documentation - `cy.viewport()`: https://docs.cypress.io/api/commands/viewport
