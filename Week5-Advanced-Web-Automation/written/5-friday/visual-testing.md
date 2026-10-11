# Visual Testing in Cypress: Baselines, Diffs, Thresholds and Plugins

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **visual testing** (visual regression testing) is, what kinds of bugs it catches that functional assertions miss, and what it does *not* replace.
- Define and use the core vocabulary: **baseline** (reference/base image), **actual** (current screenshot), **diff** (difference image), **threshold**, **tolerance**, **mask**, **approval** (accepting a new baseline).
- Describe, with simple arithmetic, how **pixel-by-pixel comparison** works, and distinguish the two common kinds of threshold: per-pixel *colour sensitivity* and overall *percentage of mismatched pixels*.
- Compare the main tool families: open-source plugins (`cypress-visual-regression`, `cypress-image-snapshot` and its forks, Cypress Image Diff, FRSOURCE's visual-regression-diff plugin) and commercial services (Percy, Applitools Eyes), and choose between them.
- Install and configure **`cypress-visual-regression`**, generate baselines, run comparisons, read diff images, and update baselines deliberately.
- Make visual tests **stable**: fixed viewport and environment, waiting for fonts and images, disabling animation, freezing time, stubbing data, element-level snapshots and thresholds.
- **Mask** dynamic content (timestamps, ads, random avatars, counters) with `blackout`, CSS injection, data stubbing and scoped snapshots.
- Integrate visual checks into a CI workflow and a team review process, and avoid the classic visual-testing anti-patterns.

---

## Why This Matters

This week's epic ends where users actually experience software: on the screen. For four days you have automated *behaviour*: click this, type that, assert the text. Those assertions can all pass while the page looks broken. Think about:

- A CSS change that makes the "Buy" button white text on a white background. The button still exists, is "visible" to Cypress, is clickable and has the right text. Every functional test passes. Customers cannot see it.
- A font file that fails to load, so the whole site renders in a default serif font.
- A layout that overlaps on a narrow viewport so the price covers the product name.
- A logo image that vanished because of a wrong path (the `<img>` element exists, so `should('exist')` passes).

**Visual testing** catches this class of bug by comparing *what the page looks like* now with an approved picture of how it *should* look. For **Project 1: QE Foundations**, adding a few well-chosen visual checks to your Cypress tests is a high-value finishing touch for your UI deliverable: it demonstrates that your automation covers the presentation layer, and it shows you understand when and how to use it responsibly.

"Responsibly" is the key word. Visual tests are notorious for being **flaky** and **noisy** when done carelessly: a one-pixel font shift on a different machine, a blinking cursor, a live clock, an animated banner, and your test fails for no good reason. A team that experiences too many false alarms stops trusting the suite. The second half of this lesson is therefore about *stability*: making visual tests boring and reliable.

Yesterday and earlier today you built the foundations: `cy.screenshot()` (the previous lesson on screenshots and video is the mechanical basis for everything here), custom commands, fixtures, `cy.intercept`, and Cypress's configuration options. Now we combine them.

---

## The Concept

### 1. Functional versus visual testing

| | Functional assertion | Visual comparison |
|---|---|---|
| Question | "Does the element exist, with this text, and does it work?" | "Does the page *look* the way it looked when we approved it?" |
| Evidence | DOM state and values | Pixels (an image) |
| Precision | Exact, targeted | Broad, catches unexpected side effects |
| Typical failures | Missing element, wrong text | Overlap, wrong colour, missing image, misalignment, broken font |
| Maintenance | Low if selectors are stable | Higher: legitimate design changes require baseline updates |
| Speed | Fast | Slower (image capture and comparison) |

They are **complementary**. Functional assertions say *what is true*; visual tests say *nothing visibly changed unexpectedly*. A visual test should never be your only check of a business rule.

### 2. The vocabulary

- **Baseline (base, reference, golden image):** the approved screenshot that represents the correct appearance. It is stored (usually in version control) and compared against in every later run.
- **Actual (current, candidate):** the screenshot taken in the current test run.
- **Diff:** an image (and numbers) showing where actual differs from baseline. Many tools highlight differing pixels (often in red or magenta) so you can see at a glance what changed.
- **Threshold / tolerance:** how much difference is acceptable before the test fails. We will see that there are usually *two* thresholds.
- **Mask / blackout / ignore region:** an area that is deliberately excluded or painted over so its changing content does not matter.
- **Approval / baseline update:** accepting the actual image as the new baseline after a *deliberate* design change. This is a human decision, never an automatic one.
- **Flakiness (false positive):** a failure when nothing meaningful changed, caused by environment noise.
- **False negative:** a real visual bug that slips through because thresholds or masks are too generous.

### 3. The basic workflow

1. **Create the baseline.** Run the tests in "base" mode, review the images and commit them.
2. **Compare on every run.** Run in "regression" mode: each test captures an actual image and compares it to its baseline.
3. **Pass or fail.** If the difference is within the threshold, the test passes. If not, it fails and a diff image is saved.
4. **Triage.** A human looks at the diff. Is it a **bug** (fix the application) or an **intended change** (update the baseline)?
5. **Update baselines deliberately** and review them in a pull request like code.

### 4. How the comparison works: pixels, arithmetic and thresholds

Most open-source Cypress plugins compare images **pixel by pixel**. Under the hood, many use a library such as **pixelmatch** (small and fast) or Jimp/ImageMagick-style tools. The idea:

1. Both images must have the **same dimensions** (width and height). If they differ (for example because the page became taller), the comparison either fails immediately or resizes/pads, depending on the tool.
2. For every pixel position, compare the colour of the baseline pixel with the colour of the actual pixel. Colours are made of Red, Green, Blue (and sometimes alpha) values, 0-255 each.
3. If the *distance* between the two colours is bigger than a **per-pixel threshold**, count that pixel as **mismatched**.
4. After checking all pixels, compute the **mismatch percentage**:

   `percentage = mismatchedPixels / totalPixels * 100`

5. If the percentage is above your **error threshold**, the test fails.

**A worked example.** Suppose you screenshot an element that is 800 pixels wide and 600 pixels tall. Total pixels = 800 x 600 = **480,000**. Suppose your error threshold is **0.1 percent**. Then you allow at most 0.001 x 480,000 = **480 mismatched pixels**. A single changed icon of 20 x 20 = 400 pixels would pass (0.083 percent), while a changed 30 x 30 icon = 900 pixels would fail (0.1875 percent). Notice the lesson: *a threshold that seems tiny can hide a real defect on a large image*, and one that is zero will fail on invisible noise. That is why we prefer **smaller, element-level screenshots**: the same defect is a larger percentage of the image, so you can use a tighter threshold.

**Two kinds of threshold** (in `cypress-visual-regression` they are separate settings):

| Threshold | Meaning | Typical default | Analogy |
|---|---|---|---|
| Per-pixel colour **sensitivity** (in pixelmatch: `threshold`, from 0 to 1, default 0.1) | How different two colours must be before that pixel counts as different. Lower means more sensitive. | ~0.1 | How good your eyes are at telling two shades apart. |
| **Error threshold** (`errorThreshold`, percentage in this plugin) | How many mismatched pixels are tolerated overall. | 0 | How many mistakes on the whole page you will forgive. |

**Anti-aliasing** is the smoothing of the edges of text and shapes, which can differ slightly between operating systems, browsers and GPUs. Pixelmatch can detect and ignore anti-aliased pixels by default (the option `includeAA` controls whether they count). Even so, differences in text rendering across machines are the number one cause of false failures, which is why **baselines must be generated in the same environment where comparisons run** (see stability section).

### 5. Beyond pixels: other comparison approaches

| Approach | How it works | Pros | Cons |
|---|---|---|---|
| **Pixel diff** (pixelmatch, image-snapshot) | Compares colours of each pixel. | Simple, free, deterministic. | Sensitive to rendering noise; cannot "understand" the page. |
| **DOM/CSS snapshot comparison** | Compares serialised DOM and styles. | Stable across machines. | Cannot see rendering issues (overlap, missing fonts). |
| **Perceptual / structural similarity** | Uses algorithms that approximate human perception (for example SSIM). | Fewer false alarms. | More complex, tool-specific. |
| **AI/"Visual AI"** (for example Applitools) | A trained model identifies meaningful differences, ignoring noise such as anti-aliasing and small shifts; supports layout-level matching. | Few false positives; cross-browser grids. | Commercial; vendor dependency. |
| **Cloud rendering services** (Percy) | Capture DOM + assets in your test, render in the vendor's own browsers, and diff there. | Consistent environment across your team and CI; cross-browser and responsive rendering; review UI. | Commercial; data leaves your network. |

### 6. The tool landscape for Cypress

Cypress itself provides `cy.screenshot()` (capture) but **not comparison**. The official Cypress guide on visual testing explains this and lists plugins you can add. The categories are:

**Open-source plugins (free; you manage baselines and environment):**

- **`cypress-visual-regression`** (maintained under the `cypress-visual-regression` GitHub organisation): adds `cy.compareSnapshot()`, uses pixelmatch, supports full-page, viewport and element snapshots, stores baselines in a folder you control. We use it for the hands-on example below.
- **`cypress-image-snapshot`**: originally by Jared Palmer, built on `jest-image-snapshot`, adding `cy.matchImageSnapshot()`. The original package has seen little maintenance for a long time, so many teams use maintained **forks** (for example `@simonsmith/cypress-image-snapshot`, which adds support for newer Cypress versions). Always check the repository activity and the Cypress versions supported before adopting.
- **Cypress Image Diff** and **FRSOURCE `cypress-plugin-visual-regression-diff`**: other community plugins with their own comparison commands and report UI. The official visual-testing page also names "Visual Regression Diff" and **Pixeleye** (a self-hostable review platform with a Cypress integration).

**Commercial services (paid, with trials; they handle storage, rendering and review):**

- **Percy** (from BrowserStack): you install `@percy/cypress`, call `cy.percySnapshot('name')` in tests, and run Cypress under `percy exec`. Percy captures the DOM and assets, renders them in its own browsers and shows diffs in a web dashboard with approval workflows.
- **Applitools Eyes**: uses `@applitools/eyes-cypress`; commands such as `cy.eyesOpen()`, `cy.eyesCheckWindow()` and `cy.eyesClose()`; "Visual AI" comparisons and an "Ultrafast Grid" for cross-browser rendering.
- Others: Argos, Chromatic and similar services also integrate with Cypress.

**How to choose:**

| Situation | Suggested direction |
|---|---|
| Learning, small project, no budget | Open-source plugin (our choice today). |
| Single browser, controlled CI environment, small team | Open-source plugin with baselines in Git, generated in CI. |
| Many browsers/devices, many reviewers, frequent design changes | Commercial service (Percy, Applitools) to avoid environment management and gain a review UI. |
| Strict data restrictions | Self-hosted/open-source options; check vendor data policies. |

### 7. Where to take snapshots: scope matters

- **Full page** is easy but fragile: any change anywhere (a banner, an ad, a changed footer) fails the test, and long pages mean many pixels to compare.
- **Viewport** screenshots are more predictable: a fixed rectangle.
- **Element/component** screenshots are the most stable and the most useful: the failure tells you *which component* changed, and the tolerance is easier to tune. Prefer them for headers, product cards, forms and tables.
- **Key pages only.** Do not screenshot every page at every step. Choose representative screens (home, product list, cart, checkout) and states (empty, filled, error).

### 8. Making visual tests deterministic (flakiness handling)

Visual flakiness has a small number of root causes. Fix each at its source.

**1. The environment differs.**
Different OS, browser version, GPU, screen scaling or font rendering produce different pixels. Solutions:

- Generate and compare baselines **in the same environment**, ideally the **same Docker image** in CI (for example the official `cypress/included` or `cypress/browsers` images pinned to a version). Developers should *not* commit baselines generated on their laptops if CI compares on Linux.
- Use the same browser (and version) for baseline and comparison. Keep separate baselines per browser if you test several.
- Fix `device pixel ratio`/scaling issues by running headless in CI with a defined viewport.

**2. The viewport differs.**
Set `cy.viewport(width, height)` explicitly in every visual test (or `viewportWidth`/`viewportHeight` in config). Responsive layouts depend on it.

**3. The page was not ready.**
Capturing during loading gives different images each time. Wait for:

- the key element(s) to be visible (`should('be.visible')`),
- network responses (`cy.wait('@alias')`),
- **fonts** (`document.fonts.ready` / `document.fonts.status`),
- **images** (each `<img>` has `naturalWidth > 0`),
- spinners to disappear (`should('not.exist')`).

**4. Animations and transitions.**
`cy.screenshot()` defaults to `disableTimersAndAnimations: true`, which pauses JavaScript timers and CSS animations while capturing. For extra safety, inject CSS that disables `animation`, `transition` and `caret-color`.

**5. Dynamic data.**
Dates, times, counters, random content, "recently viewed" widgets, ads, user avatars, live prices. Options, from best to last resort:

- **Stub the data:** `cy.intercept` returns fixed JSON so the page always shows the same text.
- **Freeze time:** `cy.clock(fixedTimestamp)` makes the application's notion of "now" constant (for code that uses `Date`/timers).
- **Hide or replace** the element: inject CSS (`visibility: hidden`) or set fixed text.
- **Mask** it: `blackout` paints it black in the screenshot.
- **Exclude** it by snapshotting a more specific element.

**6. Scrollbars, caret and focus.**
A blinking text caret in a focused input, a hover effect under the mouse, or a visible scrollbar create differences. Blur the active element, move focus, hide the caret with `caret-color: transparent`.

**7. Sub-pixel and rounding noise.**
Use a small `errorThreshold` (for example 0.1 to 0.5 percent on large areas, tighter on small elements) and sensible pixel sensitivity, *after* fixing the other causes. Thresholds are the **last** tool, not the first.

**8. Retries.**
Cypress test retries (`retries: { runMode: 1 }`) can hide an unstable visual test. Use them carefully, and investigate every visual test that needs one.

### 9. Masking dynamic content, in detail

**Blackout (via `cy.screenshot` options).** `cypress-visual-regression` accepts Cypress screenshot options in the options argument of `compareSnapshot`, so you can pass `blackout: ['.selector']`. The element is painted black in the *actual* image *and* the baseline (as the baseline was created with the same option), so changes inside it are invisible to the comparison. Remember: the mask must also be used when you create the baseline.

**CSS injection.** Add a style block to the page before capturing:

```js
cy.document().then((doc) => {
  const style = doc.createElement('style');
  style.innerHTML = '[data-test="clock"] { visibility: hidden !important; }';
  doc.head.appendChild(style);
});
```

`visibility: hidden` keeps the element's *space* in the layout (so nothing shifts), whereas `display: none` removes it and may shift other elements.

**Stubbing data with `cy.intercept`.** If the product list comes from `/api/products`, intercept it and return a fixture. Then there is no dynamic content to mask.

**Narrower snapshots.** Instead of the full page, capture `cy.get('[data-test="product-card"]')`.

**Rule:** mask the *minimum* area needed. Large masks are blind spots where real bugs can hide.

### 10. Baseline management in a team

- **Where to store:** commit baselines to Git (small PNGs are fine; for many large images consider Git LFS). Keep `actual` and `diff` folders in `.gitignore` because they are outputs.
- **Where *not* to store:** inside `cypress/screenshots` if `trashAssetsBeforeRuns` is `true`, because Cypress deletes that folder before each `cypress run` (see the screenshots lesson). The plugin we use keeps baselines in `cypress/snapshots/base`, separate from the `actual` output folder.
- **Review changes like code:** a baseline update appears in a pull request as an image diff. The reviewer asks "is this change intended?".
- **Naming:** use descriptive, stable names (`inventory-page`, `cart-empty`), including viewport/browser if you keep several (`inventory-page-desktop`, `inventory-page-mobile`).
- **Never auto-approve in CI.** Updating baselines should be an explicit action (for example, a manual pipeline job or a local command), not a side effect of a failing build.
- **Separate base generation from regression runs:** a base run overwrites images; a regression run compares.

### 11. When *not* to use visual testing

- On pages dominated by constantly changing data you cannot control.
- To verify business logic (use assertions).
- As a replacement for accessibility testing or exploratory testing by humans.
- When the design is still changing daily (you will spend all your time re-approving).
- On every page of a huge application; choose critical, stable, high-value screens.

---

## Code Examples

We now build a **working** visual-regression setup with `cypress-visual-regression` on the public Sauce Demo site. Everything below is plain JavaScript. (Version note: this plugin changes between major versions, including how options are configured. The instructions below follow the `env`-based configuration shown in the plugin's current npm page for Cypress 10 and later configs. Always read the README for the version you install, and run `npm ls cypress-visual-regression` to see which version you have.)

### Step 0: Project layout we are aiming for

```
project/
├─ cypress.config.js
├─ cypress.env.json                (git-ignored; holds credentials)
├─ cypress/
│  ├─ e2e/
│  │  └─ visual.cy.js
│  ├─ fixtures/
│  ├─ snapshots/
│  │  ├─ base/                     (committed: approved baselines)
│  │  ├─ actual/                   (generated; git-ignored)
│  │  └─ diff/                     (generated; git-ignored)
│  └─ support/
│     ├─ commands.js
│     └─ e2e.js
└─ .gitignore
```

### Step 1: Install

```bash
npm install --save-dev cypress cypress-visual-regression
```

**Explanation:** `--save-dev` records both packages as development dependencies in `package.json`. `cypress-visual-regression` provides the Node-side plugin (which compares images) and the browser-side command (`cy.compareSnapshot`).

### Step 2: Configure `cypress.config.js`

```js
const { defineConfig } = require('cypress');
const { configureVisualRegression } = require('cypress-visual-regression');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    viewportWidth: 1280,
    viewportHeight: 800,

    env: {
      visualRegressionType: 'regression',
      visualRegressionBaseDirectory: 'cypress/snapshots/base',
      visualRegressionDiffDirectory: 'cypress/snapshots/diff',
      visualRegressionGenerateDiff: 'fail',
      visualRegressionFailSilently: false,
    },

    screenshotsFolder: 'cypress/snapshots/actual',
    trashAssetsBeforeRuns: true,
    video: false,

    setupNodeEvents(on, config) {
      configureVisualRegression(on);
      return config;
    },
  },
});
```

**Line-by-line explanation**

1. `require('cypress')` gives `defineConfig`; `require('cypress-visual-regression')` gives `configureVisualRegression`, the function that registers the plugin's Node-side tasks.
2. `baseUrl` lets us visit relative URLs.
3. `viewportWidth` and `viewportHeight` fix the browser window size at 1280 by 800 for *every* test. Visual tests must not depend on whatever default size the machine gives.
4. `env: {...}` holds plugin settings. The plugin reads them with the prefix `visualRegression`:
   - `visualRegressionType: 'regression'` means "compare against the baseline". The other value, `'base'`, means "generate baseline images and overwrite existing ones". We keep `'regression'` as the safe default and override it from the command line when we want to generate baselines.
   - `visualRegressionBaseDirectory` is where approved baselines live (this is also the plugin's documented default).
   - `visualRegressionDiffDirectory` is where diff images are written.
   - `visualRegressionGenerateDiff: 'fail'` generates a diff image only when a comparison fails (the other values are `'never'` and `'always'`).
   - `visualRegressionFailSilently: false` means a failed comparison throws an error and fails the test. If `true`, the failure is returned in the command's result so you can handle it yourself.
5. `screenshotsFolder: 'cypress/snapshots/actual'` tells Cypress to put screenshots (the "actual" images) in a folder that is *different* from the baselines. That is crucial because of the next line.
6. `trashAssetsBeforeRuns: true` empties `screenshotsFolder` (the `actual` folder) before every `cypress run`, so old actual images never confuse a new run. Because baselines are in a *different* folder, they are safe.
7. `video: false` is the default in Cypress 13+, shown explicitly because video is useless here.
8. `setupNodeEvents(on, config)` runs in Node. `configureVisualRegression(on)` registers the plugin's tasks, which do the image reading, pixelmatch comparison and file writing.
9. `return config;` hands the configuration back.

### Step 3: Register the browser command in `cypress/support/e2e.js`

```js
const { addCompareSnapshotCommand } = require('cypress-visual-regression/dist/command');

addCompareSnapshotCommand({
  capture: 'viewport',
  errorThreshold: 0.1,
});

require('./commands');
```

**Line-by-line explanation**

1. `require('cypress-visual-regression/dist/command')` loads the browser-side code.
2. `addCompareSnapshotCommand({...})` registers the custom command `cy.compareSnapshot()`. The object contains **global defaults** for every call: `capture: 'viewport'` (take viewport screenshots unless told otherwise) and `errorThreshold: 0.1`. In this plugin the threshold is a **percentage**: 0.1 means up to 0.1 percent of pixels may differ. (Other options documented by the plugin include `pixelmatchOptions`, where you can pass pixelmatch's own settings such as `{ threshold: 0.1 }` for colour sensitivity.)
3. `require('./commands')` loads our own custom commands (like `cy.login`, from the previous lesson).

### Step 4: The login command (from the previous lesson)

`cypress/support/commands.js`:

```js
Cypress.Commands.add('login', () => {
  cy.session('standard_user', () => {
    cy.visit('/');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce', { log: false });
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  });
});
```

**Explanation:** This is a trimmed version of the command from "Editing generated code": it logs in once and caches the session so each visual test can start on the inventory page quickly. (Sauce Demo's password is public, so it is shown inline for the demo; real secrets belong in `cypress.env.json` or CI secrets.)

### Step 5: Write the visual spec

`cypress/e2e/visual.cy.js`:

```js
describe('Visual regression', () => {
  const stabilise = () => {
    // 1. Wait until web fonts are loaded
    cy.document().its('fonts.status').should('eq', 'loaded');

    // 2. Wait until every image has really loaded
    cy.get('img').should(($imgs) => {
      $imgs.each((_, img) => {
        expect(img.naturalWidth, `image ${img.src} loaded`).to.be.greaterThan(0);
      });
    });

    // 3. Remove animation, transitions and the blinking caret
    cy.document().then((doc) => {
      const style = doc.createElement('style');
      style.innerHTML = `
        *, *::before, *::after {
          animation: none !important;
          transition: none !important;
          caret-color: transparent !important;
        }
      `;
      doc.head.appendChild(style);
    });
  };

  context('Login page (logged out)', () => {
    it('matches the baseline', () => {
      cy.visit('/');
      cy.get('[data-test="login-button"]').should('be.visible');
      stabilise();

      cy.compareSnapshot('login-page');
    });
  });

  context('Inventory page (logged in)', () => {
    beforeEach(() => {
      cy.login();
      cy.visit('/inventory.html');
      cy.get('[data-test="inventory-item"]').should('have.length', 6);
      stabilise();
    });

    it('whole viewport matches the baseline', () => {
      cy.compareSnapshot('inventory-viewport', 0.1);
    });

    it('product list (element) matches the baseline', () => {
      cy.get('[data-test="inventory-list"]').compareSnapshot('inventory-list', 0.05);
    });

    it('first product card (element) matches the baseline', () => {
      cy.get('[data-test="inventory-item"]').first().compareSnapshot('inventory-card-first', 0.05);
    });

    it('masks the shopping cart badge when it changes', () => {
      cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
      cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');

      cy.compareSnapshot('inventory-with-item', {
        errorThreshold: 0.1,
        blackout: ['[data-test="shopping-cart-badge"]'],
      });
    });
  });

  if (Cypress.env('simulateRegression')) {
    it('DEMO ONLY: detects a deliberate visual change', () => {
      cy.login();
      cy.visit('/inventory.html');
      cy.get('[data-test="inventory-item"]').should('have.length', 6);
      cy.document().then((doc) => {
        const s = doc.createElement('style');
        s.innerHTML = '[data-test="inventory-list"] { filter: invert(1); }';
        doc.head.appendChild(s);
      });
      cy.get('[data-test="inventory-list"]').compareSnapshot('inventory-list', 0.05);
    });
  }
});
```

**Line-by-line explanation**

1. `describe('Visual regression', ...)` groups the visual tests.
2. `const stabilise = () => { ... }` is a **helper function** that queues several Cypress commands. It is not a Cypress custom command; it is plain JavaScript that, when called inside a test or hook, adds its commands to the queue in order. Calling it before each snapshot removes duplicated code.
3. `cy.document().its('fonts.status').should('eq', 'loaded')`: `cy.document()` yields the application's `document`. `.its('fonts.status')` reads the nested property `document.fonts.status`, which the browser sets to `'loading'` while web fonts are downloading and `'loaded'` when finished. `.should('eq', 'loaded')` retries until it equals `'loaded'`. This guards against screenshots taken before fonts are ready.
4. `cy.get('img').should(($imgs) => { ... })` uses a **callback assertion**: Cypress retries the callback until it stops throwing. Inside, `$imgs.each((_, img) => {...})` loops over each image (the first parameter, the index, is unused so it is named `_`). `expect(img.naturalWidth, 'message').to.be.greaterThan(0)` is a Chai assertion: a fully loaded image has a natural width greater than zero; a broken or still-loading one has zero. The second argument to `expect` is a custom failure message.
5. `cy.document().then((doc) => { ... })` runs a function with the document. We create a `<style>` element, set its CSS and append it to `<head>`. The CSS selector `*, *::before, *::after` targets every element and pseudo-element; the rules `animation: none`, `transition: none` and `caret-color: transparent` (all with `!important` to override the site's styles) stop motion and hide the blinking text caret.
6. `context('Login page (logged out)', ...)` is an alias for `describe`, used here for readability.
7. `cy.visit('/')` opens the login page; `should('be.visible')` waits for the login button, a *readiness signal*.
8. `stabilise();` prepares the page.
9. `cy.compareSnapshot('login-page')` takes a screenshot (viewport capture, from our global default) and, depending on `visualRegressionType`, either stores it as a baseline (`base`) or compares it with the baseline named `login-page` (`regression`). The `errorThreshold` is the global 0.1.
10. `beforeEach` in the inventory context logs in (via the cached session), visits the inventory page, waits for six product cards (a readiness signal and a functional guard) and stabilises.
11. `cy.compareSnapshot('inventory-viewport', 0.1)`: the second argument is a number, interpreted as the `errorThreshold` for this call (0.1 percent).
12. `cy.get('[data-test="inventory-list"]').compareSnapshot('inventory-list', 0.05)`: when `compareSnapshot` is chained from an element, only that element is captured (an **element snapshot**). We use a tighter threshold (0.05 percent) since the image is smaller.
13. `.first().compareSnapshot('inventory-card-first', 0.05)` snapshots just the first product card, the most stable and informative kind of check.
14. In the last test we add a product to the cart; the badge number changes the page, so to avoid depending on it we use `blackout: ['[data-test="shopping-cart-badge"]']`. Here the second argument is an **options object** (the plugin accepts either a number or an object): `errorThreshold` plus Cypress screenshot options. `blackout` paints the badge black in the screenshot. The *same mask is applied when the baseline is generated* because the same test runs in base mode.
15. The final test is only defined when you run with `--env simulateRegression=true`. It injects CSS `filter: invert(1)` on the product list, which inverts all colours. Comparing against the baseline named `inventory-list` must now **fail**, proving that our setup detects visual changes. `Cypress.env('simulateRegression')` reads the environment value; without it, the block is skipped, so our normal suite stays green.

### Step 6: Generate the baselines

```bash
npx cypress run --env visualRegressionType=base
```

**Explanation:** `--env visualRegressionType=base` overrides the value from the config for this run only. In `base` mode, `compareSnapshot` saves the screenshot into `cypress/snapshots/base` (overwriting any existing file) instead of comparing. Tests pass because there is nothing to compare. **Open the generated PNGs and look at them.** A baseline is only as good as the review you give it: if the baseline is wrong (a half-loaded page, an error banner), every later comparison "protects" a bug.

Commit the `cypress/snapshots/base` folder.

### Step 7: Run comparisons

```bash
npx cypress run
```

**Explanation:** The default `visualRegressionType` is `regression`. Each `compareSnapshot` takes a screenshot into `cypress/snapshots/actual`, compares it with the corresponding baseline and fails the test when the mismatch percentage exceeds the threshold. When it fails, because `visualRegressionGenerateDiff` is `'fail'`, a diff image appears in `cypress/snapshots/diff`. The error message reports numbers such as the mismatch percentage so you can judge how big the difference is.

### Step 8: Prove it detects changes

```bash
npx cypress run --env simulateRegression=true
```

**Explanation:** The DEMO test inverts the product list colours, so the comparison with the `inventory-list` baseline fails. Open `cypress/snapshots/diff` and look at the diff: the differing pixels are highlighted (in this plugin's output, differences are marked in a contrasting colour). Then remove the flag and confirm the suite is green again. This "make it fail on purpose" step is an essential habit: **a visual test that cannot fail is worthless**.

### Step 9: Update a baseline deliberately

When a design change is intentional (say the product card got a new border):

```bash
# 1. Regenerate only the affected spec's baselines
npx cypress run --spec cypress/e2e/visual.cy.js --env visualRegressionType=base

# 2. Review the changed PNGs in your Git diff tool or editor
git status
git diff --stat

# 3. Commit them with an explanatory message
git add cypress/snapshots/base
git commit -m "Update baselines: new product card border (design ticket DES-123)"
```

**Explanation:** Notice there is no automation that updates baselines by itself. A human reviews the images and the commit message links them to the design decision. (A real project would put this in a pull request.) Also note: running `base` mode regenerates *every* snapshot in the specs you run, so run it only for the affected spec, then check in Git that only the intended images changed. If unrelated images changed, you have environment noise to fix first.

### Step 10: `.gitignore`

```
cypress/snapshots/actual/
cypress/snapshots/diff/
cypress.env.json
```

**Explanation:** Actual and diff images are outputs. In CI you *upload* them as artifacts (see the screenshots lesson) when the job fails, so reviewers can see them.

### Step 11: CI sketch (GitHub Actions)

```yaml
name: visual-tests
on: [pull_request]

jobs:
  visual:
    runs-on: ubuntu-latest
    container:
      image: cypress/browsers:<pinned-tag>   # use the SAME image whenever baselines are regenerated
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx cypress run --browser chrome
      - name: Upload visual diffs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diffs
          path: |
            cypress/snapshots/actual
            cypress/snapshots/diff
```

**Explanation:** `container.image` pins the operating system and browser fonts, which is the single most effective flake-prevention measure for pixel comparison. Replace `<pinned-tag>` with a real, specific tag from Cypress's published images (the documentation lists them). `npm ci` installs exact versions from the lock file. `if: failure()` ensures the artifact upload step runs only after a failure, giving reviewers the actual and diff images.

### Example: A closer look at a dynamic-data stub

```js
it('product list is stable when the API data is stubbed', () => {
  cy.intercept('GET', '**/api/products*', { fixture: 'products.json' }).as('products');
  cy.visit('/products');
  cy.wait('@products');
  cy.get('[data-test="product-grid"]').should('be.visible');
  cy.get('[data-test="product-grid"]').compareSnapshot('product-grid', 0.05);
});
```

**Line-by-line explanation**

1. `cy.intercept(method, urlPattern, response)` stubs the network call. `{ fixture: 'products.json' }` replies with `cypress/fixtures/products.json` instead of hitting the real API. (The endpoint is hypothetical: adapt it to your Project 1 application. Sauce Demo's data is bundled in the page and does not need stubbing.)
2. `.as('products')` aliases it so we can wait for it.
3. `cy.visit('/products')` loads the page.
4. `cy.wait('@products')` waits for the stubbed request to happen. Because the response is fixed, the content is identical on every run.
5. `should('be.visible')` ensures the grid has rendered.
6. `compareSnapshot` compares just the grid.

### Example: Freezing time

```js
it('shows a stable "Last updated" label', () => {
  cy.clock(new Date('2026-01-15T10:00:00Z').getTime(), ['Date']);
  cy.visit('/dashboard');
  cy.get('[data-test="last-updated"]').should('contain.text', '15 Jan 2026');
  cy.get('[data-test="dashboard"]').compareSnapshot('dashboard', 0.1);
});
```

**Line-by-line explanation**

1. `new Date('2026-01-15T10:00:00Z').getTime()` converts a fixed date to milliseconds since 1970.
2. `cy.clock(now, ['Date'])` overrides only the `Date` function in the application (the second argument lists which functions to fake; leaving out `setTimeout` etc. keeps timers working so the app still loads). It must be called **before** `cy.visit`, so the app starts with the fake clock.
3. The assertion guards that the label shows the frozen date (a functional check with the visual check).
4. The snapshot is now independent of the real day and time. (The dashboard URL and the label text are illustrative.)

### Example: Commercial service snippets (illustrative, confirm in vendor docs)

These are outlines to show how different the *workflow* is; you will not run them today.

**Percy:**

```js
// cypress/support/e2e.js
import '@percy/cypress';

// in a test
cy.visit('/');
cy.percySnapshot('Login page');
```

```bash
# Percy needs a project token, supplied as PERCY_TOKEN
npx percy exec -- cypress run
```

**Explanation:** `cy.percySnapshot` does not save a PNG locally; it sends the DOM and assets to Percy, which renders and compares in its own browsers. `percy exec` starts a local Percy agent around the Cypress run.

**Applitools Eyes (outline):**

```js
cy.eyesOpen({ appName: 'Sauce Demo', testName: 'Inventory page' });
cy.visit('/inventory.html');
cy.eyesCheckWindow('Inventory');
cy.eyesClose();
```

**Explanation:** `eyesOpen` begins a visual test, `eyesCheckWindow` captures a checkpoint and sends it to Applitools for AI-based comparison, and `eyesClose` completes the test and reports results. An API key is required, and the plugin must be registered per its documentation.

---

## Real-World Scenarios

### Scenario 1: A brand refresh

The design team updates the primary colour from blue to teal. Functional tests pass. The 40 visual tests fail, as they should, because every page changed. The QA engineer regenerates the baselines in CI's Docker image, a designer reviews the images in the pull request, and the commit merges together with the CSS change. The visual suite did its job: it made an application-wide change *visible and reviewable*.

### Scenario 2: The silent CSS regression

A developer fixes a button's margin on the checkout page. A shared CSS file also controls the cart summary. The next pipeline fails `cart-summary` with 3.2 percent mismatch; the diff shows the "Total" label now overlaps the price. Nobody noticed in code review because the CSS diff was two lines. Without the visual test, the bug would have reached production.

### Scenario 3: Flaky because of a clock

A dashboard visual test fails at midnight every day: it shows "Today, 23:59" instead of "Today, 00:01". The fix is `cy.clock` plus a masked element, not a bigger threshold.

### Scenario 4: Different laptops, different pixels

Two engineers commit baselines created on macOS and Windows. CI (Linux) fails every test with 0.3 percent mismatch caused by font anti-aliasing. The team switches to generating baselines in the CI Docker image only (a manually triggered "update baselines" job) and never again commits baselines from laptops.

### Scenario 5: Choosing between plugin and service

A start-up with one browser target and a Docker-based CI uses `cypress-visual-regression`. A larger company that must verify Chrome, Firefox, Safari and three device sizes uses Percy, because maintaining nine baselines sets locally would take more engineering time than the subscription costs.

---

## Common Pitfalls and Best Practices

1. **Baselines generated in a different environment than comparisons.** Generate and compare in the same image/OS/browser.
2. **Not reviewing the baseline.** If the baseline shows a loading spinner or an error, you are protecting the wrong thing.
3. **Using thresholds to hide flakiness.** Fix the root cause first (environment, readiness, animation, data), then tune thresholds.
4. **Full-page snapshots everywhere.** Prefer element-level snapshots on stable components, and a few key full-page ones.
5. **Letting `trashAssetsBeforeRuns` erase baselines.** Keep baselines in a folder different from `screenshotsFolder` (as in our config).
6. **Masking too much.** A large black box hides real defects. Mask only what changes.
7. **Applying a mask in regression mode only.** The mask must be present when the baseline is created as well.
8. **Auto-updating baselines in CI.** Approval must be a conscious human decision.
9. **Visual tests that cannot fail.** Always demonstrate a failure once (our `simulateRegression` demo).
10. **Missing viewport control.** Always set the viewport; test mobile/desktop separately with named snapshots.
11. **Snapshotting before the page is ready.** Wait for fonts, images, network and spinners.
12. **Third-party content.** Ads, chat widgets, cookie banners, maps. Block or stub them (`cy.intercept` with a static response, or hide via CSS).
13. **Ignoring accessibility of the process.** Diff images are only one signal; they say nothing about screen-reader behaviour or keyboard access.
14. **Version drift.** The plugin's configuration style changed across major versions; pin the version in `package-lock.json` and read its README before upgrading Cypress or the plugin. Check also that the plugin supports your Cypress version.
15. **Too many snapshots.** Hundreds of tiny baselines are costly to review. Choose the screens that matter.
16. **Large repositories.** Many big PNGs bloat Git; use Git LFS or limit scope.

---

## Mini Practice Exercises

### Exercise 1: The arithmetic of thresholds

An element screenshot is 400 x 250 pixels. (a) How many pixels in total? (b) With `errorThreshold: 0.5` (percent), how many mismatched pixels are tolerated? (c) A 15 x 15 pixel icon turns from blue to red. Does the test pass?

*Solution:* (a) 400 x 250 = 100,000. (b) 0.5 percent of 100,000 = 500. (c) 15 x 15 = 225 pixels, which is below 500, so the test **passes**, even though a visible icon changed colour. Lesson: tolerate less on small images (try 0.1 percent = 100 pixels, which would fail).

### Exercise 2: Set it up

Follow Steps 1 to 8 in a fresh Cypress project. Report: where baselines are stored, what the console prints when the simulated regression runs, and what the diff image looks like.

*Hint:* if `cy.compareSnapshot is not a function`, the support-file import is missing; if you get "baseline not found", you have not run the base mode yet.

### Exercise 3: Mask it

Add a product to the cart, then snapshot the inventory page *without* blackout and with a different number of items on the second run. Show that the comparison fails, then add the blackout and show it passes. Why must the baseline be regenerated after adding the blackout option?

*Solution:* the badge pixels differ without a mask. With a mask, both images contain a black rectangle in the same place. The baseline must be regenerated because the old baseline has no black rectangle, so comparing it with a masked actual would show a difference.

### Exercise 4: Make it flaky, then fix it

Temporarily remove the `stabilise()` call and the fixed viewport, and run the suite ten times, noting any failures. Then restore them and run ten times again. What changed?

*Hint:* use `Cypress._.times(10, ...)` or a shell loop. Failures often show up as slightly different text rendering or a visible caret/animation.

### Exercise 5: Choose a tool

For each project, pick open-source plugin or commercial service and justify in two sentences: (a) an internal HR tool used only in Chrome on Windows; (b) a public e-commerce site with Chrome, Safari and Firefox on three screen sizes with a large design team; (c) a regulated bank that forbids sending page content to third parties.

*Solution (typical reasoning):* (a) open-source plugin, one environment, low cost. (b) commercial service (Percy/Applitools) for cross-browser rendering and review workflow. (c) open-source or self-hosted solution (for example a plugin with images in the bank's own repo or a self-hostable platform), because data must stay inside.

### Exercise 6: Write a policy

Write five bullet points for a "visual testing policy" for your team: what to snapshot, who approves baselines, where they are stored, how thresholds are chosen, and what to do on a failure.

*Hint:* use the baseline-management section as a checklist.

---

## Summary / Key Takeaways

- **Visual testing** compares screenshots of the application with approved **baselines**, catching presentation bugs that functional assertions cannot see. It complements, never replaces, functional tests.
- Cypress's `cy.screenshot()` only *captures*. Comparison comes from **plugins** (`cypress-visual-regression`, `cypress-image-snapshot` and forks, Cypress Image Diff, FRSOURCE's plugin) or **services** (Percy, Applitools, and others).
- Pixel comparison counts mismatched pixels (per-pixel colour sensitivity) and compares the **percentage** with an **error threshold**; small thresholds on big images can hide real defects, so prefer **element-level snapshots**.
- With `cypress-visual-regression`: configure `env` options, set `screenshotsFolder` to an `actual` folder, keep baselines elsewhere, register the plugin in `setupNodeEvents`, add the command in the support file, generate baselines with `visualRegressionType=base`, compare in `regression` mode, and review diffs.
- **Flakiness is an engineering problem**: pin the environment (same Docker image), set the viewport, wait for fonts, images and network, disable animations, freeze time, stub data, and use thresholds last.
- **Mask** only what must be masked (`blackout`, CSS injection, stubbing) and apply the same mask when creating the baseline.
- Baselines are **reviewed and approved by humans**, committed to Git, and never auto-updated in CI.
- Always prove a visual test can fail. Plugin details change between versions, so pin versions and read the README.

---

## External Resources

- Cypress documentation, Visual Testing guide (concepts, plugin list, reliability practices): https://docs.cypress.io/app/tooling/visual-testing
- `cypress-visual-regression` package documentation (installation, options, usage): https://www.npmjs.com/package/cypress-visual-regression
- pixelmatch (the pixel comparison library used by many plugins; explains the `threshold` and anti-aliasing options): https://github.com/mapbox/pixelmatch
