# Screenshots and Video in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why screenshots and videos are the main "evidence" artifacts of a Cypress test run in CI, and how they differ from interactive time-travel debugging.
- Take manual screenshots with `cy.screenshot()` for the whole page, the viewport, a single element and the Cypress runner, and control their names, folders and options (`capture`, `blackout`, `clip`, `padding`, `overwrite`, `disableTimersAndAnimations`, `onBeforeScreenshot`, `onAfterScreenshot`).
- Understand and configure **automatic failure screenshots** with `screenshotOnRunFailure`, and know exactly when they are (and are not) taken.
- Configure video recording in `cypress.config.js` (`video`, `videoCompression`, `videosFolder`, `trashAssetsBeforeRuns`), and state the **current defaults** and which Cypress version changed them.
- Use the `after:spec` and `after:screenshot` Node events to delete videos of passing specs, rename screenshots, or post-process files.
- Publish screenshots and videos from a CI pipeline as downloadable artifacts.
- Avoid leaking secrets into screenshots, and handle storage and flakiness concerns.

---

## Why This Matters

This week's epic ends with visual testing and a finished Project 1 UI deliverable. Before you can reason about *visual* verification, you need to be fluent in how Cypress produces images and recordings, because every visual-testing plugin you will meet later today is built on top of `cy.screenshot()`.

But there is a more immediate, practical reason. In your day-to-day work as a Test Automation Engineer, most test failures that matter happen **where you are not looking**: on a CI server, overnight, in a headless browser. In the previous lesson you learned that Cypress's interactive time travel works in `cypress open`, but in `cypress run` there is nobody to hover over the Command Log. What survives a headless CI run is:

1. The **terminal output** (error message, stack, which spec failed).
2. A **screenshot** of the failure moment.
3. Optionally a **video** of the whole spec.

For **Project 1: QE Foundations**, these artifacts are what you attach to bug reports, what your reviewers will look at when a pipeline fails, and what lets you prove that a test genuinely exercised the UI. Learning to configure them correctly (and to keep storage costs and secrets under control) is part of professional-grade test automation.

You may remember that Playwright has its own screenshot and video options (`screenshot: 'only-on-failure'`, `video: 'retain-on-failure'`, and so on, in `playwright.config`). The ideas are the same; the knobs are named differently. We will point out the contrasts as we go.

---

## The Concept

### 1. Two kinds of screenshots

Cypress produces screenshots in two ways:

1. **Manual screenshots** that *you* request in the test code with `cy.screenshot()`. These are taken in both `cypress open` and `cypress run`.
2. **Automatic failure screenshots**, taken by Cypress itself when a test fails. These are only taken during `cypress run` (headless or headed), not during interactive `cypress open`, because in open mode you can just look at the failed state.

Both kinds are saved as PNG files in the **screenshots folder**, which defaults to `cypress/screenshots`.

### 2. `cy.screenshot()`: the basics

The simplest use:

```js
cy.screenshot();
```

This takes a screenshot of the application under test and saves it in:

```
cypress/screenshots/<spec file path>/<suite name -- test name>.png
```

For example, for `cypress/e2e/login.cy.js` containing `describe('Login')` and `it('shows inventory')`, the file would be something like:

```
cypress/screenshots/login.cy.js/Login -- shows inventory.png
```

Cypress joins the suite and test titles with ` -- ` and removes characters that are not safe in file names. If you take several screenshots in one test without naming them, Cypress adds a numeric suffix such as `(1)`, `(2)` so nothing is overwritten (unless you pass `overwrite: true`).

You can give a screenshot a **name**:

```js
cy.screenshot('inventory-page');
```

which saves to `cypress/screenshots/login.cy.js/inventory-page.png`. A name with slashes creates sub-folders: `cy.screenshot('login/after-submit')` creates `login/after-submit.png` inside the spec's folder. This is useful for organising visual baselines, which we use later today.

### 3. What exactly is captured? The `capture` option

`cy.screenshot()` accepts a `capture` option with three values:

| `capture` | What you get |
|---|---|
| `'fullPage'` (default for page screenshots) | The whole scrollable page. Cypress scrolls and stitches it together. |
| `'viewport'` | Only what is visible in the application's viewport (for example 1000x660 by default in `cypress run`). |
| `'runner'` | The entire Cypress Test Runner window, including the **Command Log**, the app preview and the header. |

Notes:

- When you screenshot a **specific element** (`cy.get('.card').screenshot()`), the `capture` option is ignored: you get just that element, cropped.
- **Failure screenshots always use `capture: 'runner'`**, so the image shows the Command Log with the red failed command next to the app. This is extremely helpful: one picture shows both what the page looked like and which step failed.

### 4. Element screenshots

Chain `.screenshot()` off a command that yields an element:

```js
cy.get('[data-test="inventory-item"]').first().screenshot('first-product');
```

Cypress scrolls the element into view, captures just its bounding box and saves it. Element screenshots are the foundation of *stable* visual testing, because a screenshot of one component has far fewer reasons to change than a screenshot of a whole page.

You can add `padding` to include some space around the element (a number, or up to four numbers following CSS shorthand rules, like `padding: [10, 20]`).

### 5. Options in detail

| Option | Default | What it does |
|---|---|---|
| `capture` | `'fullPage'` | `'fullPage'`, `'viewport'` or `'runner'` (see above). |
| `blackout` | `[]` | An array of CSS selectors; matching elements are painted solid black in the image. Used to hide changing or sensitive content (not available for `runner` captures). |
| `clip` | `null` | `{ x, y, width, height }` in pixels; crops the image to that rectangle. |
| `disableTimersAndAnimations` | `true` | While the screenshot is taken, JavaScript timers (`setTimeout` etc.) and CSS animations are paused so the image is deterministic. |
| `padding` | `null` | Extra pixels around an element screenshot. |
| `scale` | `false` | Whether to scale the app down to fit the viewport; always effectively `true` for `runner` captures. |
| `overwrite` | `false` | If `true`, replace a file with the same name; otherwise a numeric suffix is added. |
| `onBeforeScreenshot` | `null` | A callback that runs right before the image is taken (for manual screenshots). It receives the element (or the document). Use it to hide things temporarily. |
| `onAfterScreenshot` | `null` | A callback after the image has been saved. It receives the element/document and an object with details such as the file `path` and `dimensions`. |
| `log` | `true` | Show or hide the command in the Command Log. |
| `timeout` | `responseTimeout` | How long Cypress waits for the screenshot to complete. |

You can set defaults for *all* screenshots with `Cypress.Screenshot.defaults({...})`, usually in `cypress/support/e2e.js`:

```js
Cypress.Screenshot.defaults({
  blackout: ['[data-test="secret-banner"]'],
  capture: 'viewport',
  overwrite: false,
  disableTimersAndAnimations: true,
  screenshotOnRunFailure: true,
});
```

### 6. Automatic failure screenshots: `screenshotOnRunFailure`

During `cypress run`, if a test fails, Cypress takes a screenshot automatically. It is controlled by the `screenshotOnRunFailure` option, which is **on** by default. Details:

- File name: `<suite -- test> (failed).png`. If you use test retries and a later attempt fails, Cypress adds an attempt marker to the file name (for example `(attempt 2)`), so the screenshots of each failed attempt are preserved.
- The picture is of the **runner**: you will see the Command Log with the error on the left and the app state on the right.
- It is taken at the moment of failure, so if a test fails in a `before`/`beforeEach` hook, the screenshot names include the hook name (such as `-- before each hook (failed)`).
- It is *not* taken in `cypress open`.
- You can turn it off globally:

```js
// cypress.config.js
module.exports = defineConfig({
  e2e: { screenshotOnRunFailure: false },
});
```

or in the support file with `Cypress.Screenshot.defaults({ screenshotOnRunFailure: false })`.

> Contrast with Playwright: Playwright's `screenshot: 'only-on-failure'` is *opt-in* and captures the page only, while Cypress's failure screenshot is *on by default* and captures the runner (page plus Command Log).

### 7. The folders and `trashAssetsBeforeRuns`

| Option | Default | Purpose |
|---|---|---|
| `screenshotsFolder` | `cypress/screenshots` | Where screenshots go. |
| `videosFolder` | `cypress/videos` | Where videos go. |
| `trashAssetsBeforeRuns` | `true` | Before each `cypress run`, Cypress **deletes everything** in the screenshots and videos folders (including sub-folders). |

That last one surprises people. If you commit baseline images into `cypress/screenshots` (some visual plugins suggest that), they could be erased at the start of a run! Always keep **baselines in a different folder**, or set `trashAssetsBeforeRuns: false` consciously. We will configure this carefully in the Visual Testing lesson.

### 8. Video recording: the current defaults

Cypress can record a video of each **spec file** during `cypress run`. Important facts:

- Videos are **only recorded in `cypress run`**, never in `cypress open`.
- One video per **spec file** (not per test). All tests in the spec appear in one video, in sequence.
- Format: MP4, saved in `videosFolder` (default `cypress/videos`) with the spec's name.

**Version-dependent defaults (please read carefully):**

- In **Cypress 12 and earlier**, `video` defaulted to `true`.
- Since **Cypress 13.0**, `video` defaults to **`false`**. Videos are off unless you set `video: true`. The current official documentation states that video recording is disabled by default.
- `videoCompression`: the current documentation says compression is **disabled by default**, which means Cypress skips the encoding (compression) step, files are bigger, but runs finish sooner. Setting it to `true` applies a Constant Rate Factor (CRF) of 32, or you can pass a number (lower numbers mean better quality and bigger files; `0` or `false` disables). Older documentation and some type definitions stated a default of `32`, and this was corrected in a later 15.x release. **Moral: do not rely on the default.** Set `videoCompression` explicitly if you care.
- Some features, such as **video chapters** (which mark where each test attempt begins), need both video and compression enabled in newer versions. Check the current documentation for the exact requirements of your installed version.
- The older option `videoUploadOnPasses` was removed in Cypress 13. If you see it in an old tutorial, ignore it and use the `after:spec` approach below.

To enable video in `cypress.config.js`:

```js
module.exports = defineConfig({
  e2e: {
    video: true,
    videoCompression: 32,
  },
});
```

You can also toggle from the command line without editing files:

```bash
npx cypress run --config video=true,videoCompression=32
```

or with an environment variable: `CYPRESS_VIDEO=true npx cypress run`.

### 9. When should you record video?

Video is a tool, not a default. Weigh:

| Pros | Cons |
|---|---|
| Shows the *whole* sequence, including animations and timing. | Large files (tens of MB for long specs when not compressed). |
| Great for flaky tests: you see what happened between steps. | Slows runs slightly (encoding). |
| Easy to share with developers and product owners. | Can capture sensitive data (emails, tokens in URL bars, personal data). |
| Works in CI with no extra tooling. | If you use Cypress Cloud Test Replay, the docs suggest disabling video to reduce overhead. |

Common strategy: **keep video off by default; enable it on CI for nightly or retry runs; and delete the videos of passing specs** so you only store evidence for failures.

### 10. Node events: `after:spec` and `after:screenshot`

Cypress lets you hook into the Node process (not the browser) through `setupNodeEvents` in the config. Two events are especially useful here.

**`after:spec`** fires after each spec file finishes. It gives you the spec details and the results, including the `video` path and per-test attempt states. A classic recipe deletes videos for specs where nothing failed:

```js
const fs = require('fs');

module.exports = defineConfig({
  e2e: {
    video: true,
    setupNodeEvents(on, config) {
      on('after:spec', (spec, results) => {
        if (results && results.video) {
          const hadFailure = results.tests.some((test) =>
            test.attempts.some((attempt) => attempt.state === 'failed')
          );
          if (!hadFailure) {
            fs.unlinkSync(results.video);
          }
        }
      });
    },
  },
});
```

**`after:screenshot`** fires after each screenshot is saved. You can rename, move or post-process it, and return the new details:

```js
const fs = require('fs');
const path = require('path');

on('after:screenshot', (details) => {
  const newPath = path.join(
    path.dirname(details.path),
    `${Date.now()}-${path.basename(details.path)}`
  );
  return new Promise((resolve, reject) => {
    fs.rename(details.path, newPath, (err) => {
      if (err) return reject(err);
      resolve({ path: newPath });
    });
  });
});
```

### 11. Getting artifacts out of CI

Screenshots and videos live on the CI machine's disk. When the job ends, the machine is destroyed, so you must **upload them as artifacts**. In GitHub Actions, that looks like:

```yaml
- name: Run Cypress
  run: npx cypress run --browser chrome

- name: Upload screenshots on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: cypress-screenshots
    path: cypress/screenshots
    if-no-files-found: ignore

- name: Upload videos
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: cypress-videos
    path: cypress/videos
    if-no-files-found: ignore
```

If you record to Cypress Cloud (`--record`), Cypress uploads screenshots and videos to the Cloud for you after each spec, and you view them in the run's page. Deleting a video file in `after:spec` before upload prevents it from being uploaded.

### 12. Screenshots, security and privacy

An image can leak what the code does not. Think about:

- Passwords typed into visible fields (Cypress masks password-type inputs as dots, but not "show password" toggles).
- Personal data in test environments that are copies of production data.
- API keys or tokens visible in the URL.
- Banners or toolbars with a developer's email.

Mitigations: use synthetic data, use `blackout` for sensitive regions, keep artifacts private (restricted CI artifact access, short retention such as 7-14 days), and delete videos of passing runs.

---

## Code Examples

### Example 1: A manual screenshot of a page and an element

`cypress/e2e/screenshots-demo.cy.js`:

```js
describe('Screenshots demo', () => {
  beforeEach(() => {
    cy.visit('https://www.saucedemo.com');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  });

  it('captures the full page, the viewport and one product', () => {
    cy.screenshot('inventory/full-page');
    cy.screenshot('inventory/viewport-only', { capture: 'viewport' });
    cy.get('[data-test="inventory-item"]')
      .first()
      .screenshot('inventory/first-product', { padding: 8 });
  });
});
```

**Line-by-line explanation**

1. `describe(...)` defines the suite named "Screenshots demo".
2. `beforeEach(() => { ... })` logs the user in before each test. Putting it in a hook means every `it` in the file starts on the inventory page.
3. `cy.visit(...)` loads the site. The next three commands type credentials and click the login button, exactly as in the previous lesson.
4. `cy.url().should('include', '/inventory.html')` makes sure the login actually worked before we take screenshots. This is a good habit: **never take a screenshot before the page is in the state you want**, otherwise you capture a half-loaded page and the image is useless (or flaky, for visual tests).
5. `cy.screenshot('inventory/full-page')` takes a full-page capture and saves it as `cypress/screenshots/screenshots-demo.cy.js/inventory/full-page.png`. The slash creates the sub-folder `inventory`.
6. `cy.screenshot('inventory/viewport-only', { capture: 'viewport' })` passes an options object. `capture: 'viewport'` restricts it to the visible area.
7. `cy.get('[data-test="inventory-item"]')` finds all product cards; `.first()` reduces to the first; `.screenshot('inventory/first-product', { padding: 8 })` captures just that card with 8 pixels of space around it.

### Example 2: Hiding dynamic content with `blackout` and `onBeforeScreenshot`

```js
it('blacks out the cart badge and hides the footer for the screenshot', () => {
  cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();

  cy.screenshot('inventory/masked', {
    blackout: ['[data-test="shopping-cart-badge"]'],
    onBeforeScreenshot($el) {
      $el.find('.footer').css('visibility', 'hidden');
    },
    onAfterScreenshot($el, props) {
      Cypress.log({
        name: 'screenshot saved',
        message: props.path,
      });
    },
  });
});
```

**Line-by-line explanation**

1. The first line adds an item so the cart badge shows a number.
2. `blackout: [...]` takes selectors. Cypress paints those elements black *only in the image*; the live app is untouched. If the cart count changes between runs, the black box means it does not matter.
3. `onBeforeScreenshot($el)` is a function that Cypress calls right before the capture. `$el` is a jQuery-wrapped element or document (for page screenshots, it wraps the document). `$el.find('.footer').css('visibility', 'hidden')` finds the footer within it and hides it temporarily. Careful: your change is visible to the app, so undo it if later steps need it.
4. `onAfterScreenshot($el, props)` runs after the file is written. `props` includes `path` (the file location on disk), `dimensions` and other details. We call `Cypress.log` to add a row to the Command Log showing where the file was saved. (We study `Cypress.log` in the Logging lesson.)

### Example 3: Global defaults in the support file

`cypress/support/e2e.js`:

```js
Cypress.Screenshot.defaults({
  capture: 'viewport',
  overwrite: true,
  disableTimersAndAnimations: true,
  blackout: ['[data-test="timestamp"]'],
});
```

**Explanation**

- `Cypress.Screenshot.defaults(obj)` sets the default options for *every* `cy.screenshot()` call afterwards. Individual calls can still override them.
- `overwrite: true` is handy for visual baselines where you want a fixed name, not `name (1).png`.
- The support file `cypress/support/e2e.js` runs before every spec, so these defaults apply everywhere.

### Example 4: Full configuration for screenshots and video

`cypress.config.js`:

```js
const { defineConfig } = require('cypress');
const fs = require('fs');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    screenshotsFolder: 'cypress/screenshots',
    videosFolder: 'cypress/videos',
    trashAssetsBeforeRuns: true,
    screenshotOnRunFailure: true,
    video: true,
    videoCompression: 32,
    retries: { runMode: 1, openMode: 0 },
    setupNodeEvents(on, config) {
      on('after:spec', (spec, results) => {
        if (results && results.video) {
          const failed = results.tests.some((t) =>
            t.attempts.some((a) => a.state === 'failed')
          );
          if (!failed) {
            fs.unlinkSync(results.video);
          }
        }
      });
      return config;
    },
  },
});
```

**Line-by-line explanation**

1. `require('cypress')` and `defineConfig` give typed config; `fs` is Node's file-system module used to delete files.
2. `baseUrl` lets tests use relative URLs: `cy.visit('/')`.
3. `screenshotsFolder` and `videosFolder` are shown with their default values to make them explicit (good for teaching and for teams that want to move them to, say, `artifacts/`).
4. `trashAssetsBeforeRuns: true` clears old artifacts before each `cypress run` so you never confuse old and new evidence.
5. `screenshotOnRunFailure: true` keeps failure screenshots on (default).
6. `video: true` turns on recording (the default is `false` since Cypress 13).
7. `videoCompression: 32` explicitly enables compression at CRF 32, a decent balance of size and quality. Setting it explicitly avoids depending on a default that changed in documentation between versions.
8. `retries: { runMode: 1, openMode: 0 }` retries failing tests once in `cypress run`. This is why you might see two failure screenshots, one per failed attempt.
9. `setupNodeEvents(on, config)` is where Node-side events and plugins are registered. `on('after:spec', (spec, results) => {...})` registers our listener.
10. `if (results && results.video)` guards against runs where no video was recorded (for example, if video is disabled).
11. `results.tests.some(...)` loops over tests; `t.attempts.some(...)` loops over each attempt; `a.state === 'failed'` is true if any attempt of any test failed. If no attempt failed, we delete the video with `fs.unlinkSync`. Note the subtlety: a test that failed once and then passed on retry *did* have a failed attempt, so its video is kept, which is exactly what you want when investigating flakiness.
12. `return config;` returns the (possibly modified) configuration.

### Example 5: Trigger a failure to see the failure screenshot

```js
it('fails on purpose so we get a failure screenshot', () => {
  cy.visit('https://www.saucedemo.com');
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="does-not-exist"]', { timeout: 2000 });
});
```

**Explanation**

- The last line looks for an element that is not there, with a short `timeout` of 2 seconds so you do not wait the default 4 seconds.
- Run `npx cypress run --spec cypress/e2e/screenshots-demo.cy.js`. Cypress fails the test, takes a screenshot, and (if video is on) records the video.
- Look in `cypress/screenshots/screenshots-demo.cy.js/` for a file ending in `(failed).png`. Open it: you should see the Command Log with the red error on the left and the login page on the right.

---

## Real-World Scenarios

### Scenario 1: The nightly regression run

Your team runs 150 Cypress specs every night. Keeping every video would cost gigabytes per week. You enable `video: true`, `videoCompression: 32`, and the `after:spec` clean-up so only specs that had failures keep their videos. Artifacts are retained for 14 days. In the morning, the QA lead opens the failing spec's video, sees a modal that was not dismissed, and files a precise bug with the video attached.

### Scenario 2: Evidence for acceptance testing

A product owner wants proof that the checkout page showed the correct total for a discounted order. You add `cy.screenshot('evidence/checkout-total')` after asserting the text. The assertion is the *real* verification; the screenshot is human-readable evidence you can attach to the user story.

### Scenario 3: A flaky failure only on CI

Locally the test passes; on CI it fails 1 in 5 times. You enable video on CI only for that spec (`--config video=true --spec cypress/e2e/checkout.cy.js`). The video reveals a promotional pop-up that appears after a random delay and covers the "Pay" button. You fix the test by closing or blocking the pop-up in a `beforeEach`, and by stubbing the promotion API with `cy.intercept`.

### Scenario 4: Compliance and privacy

A healthcare client cannot let patient names appear in test artifacts. You switch the test environment to synthetic data, use `blackout` for the patient banner, restrict artifact access to the QA group, and set retention to 7 days.

---

## Common Pitfalls and Best Practices

1. **Screenshot before the page is ready.** Always wait on a meaningful condition (an assertion on a visible element, a URL change, an aliased network response) before capturing. Never use a fixed `cy.wait` for this.
2. **Assuming video is on.** Since Cypress 13 it is off by default. If your pipeline "lost its videos" after upgrading, this is why.
3. **Forgetting `trashAssetsBeforeRuns`.** Baselines saved in the screenshots folder can be deleted at the start of the next run. Keep baselines elsewhere or disable trashing deliberately.
4. **Storing everything forever.** Delete passing-spec videos, compress, and set retention on CI artifacts.
5. **Assuming `cy.screenshot` verifies anything.** It only saves an image. It will never fail because the page "looks wrong". For verification, use assertions or a visual-comparison plugin (the last lesson of today).
6. **Environment differences.** Fonts, anti-aliasing, scrollbar widths and viewport size differ between your laptop, a Docker image and a CI runner. Screenshots taken in different environments are **not comparable pixel for pixel**. This matters hugely for visual testing.
7. **Capturing secrets.** Use synthetic data, blackout selectors, restricted access.
8. **Using the runner capture for visual baselines.** `capture: 'runner'` includes the Command Log, which changes constantly. Use `viewport` or `fullPage` (or element screenshots) for anything you plan to compare.
9. **Relying on screenshots in `cypress open` for the failure.** Failure screenshots are not taken there. If you want an image while developing, call `cy.screenshot()` explicitly.
10. **Not naming screenshots.** Unnamed screenshots in the same test get `(1)`, `(2)` suffixes; stable, meaningful names make artifacts discoverable and make visual baselines possible.
11. **Slashes in names.** They create folders, which is a feature; but on Windows avoid characters like `:`, `?`, `*`.
12. **Heavy full-page screenshots on infinite-scroll pages.** Cypress may stitch a very tall image. Prefer element screenshots or `clip`.

---

## Mini Practice Exercises

### Exercise 1: Name and organise

Write a test that logs in and takes three named screenshots: `login/before-submit` (taken before clicking the login button), `login/after-submit` and `inventory/cart-empty`. Run it and verify the folder structure on disk.

*Hint:* take the first screenshot after typing the credentials but before `.click()`.

*Solution sketch:*

```js
it('captures login flow', () => {
  cy.visit('/');
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.screenshot('login/before-submit');
  cy.get('[data-test="login-button"]').click();
  cy.url().should('include', '/inventory.html');
  cy.screenshot('login/after-submit');
  cy.get('[data-test="shopping-cart-link"]').screenshot('inventory/cart-empty');
});
```

(This assumes `baseUrl` is set to `https://www.saucedemo.com`.)

### Exercise 2: Prove the folders are cleaned

1. Run a spec that takes a screenshot. Note the file's timestamp.
2. Run it again with `trashAssetsBeforeRuns: true`, then with `false`.
3. Describe what happened to the old files in each case.

*Hint:* with `true`, old files vanish before the run starts; with `false`, files with identical names get `(1)` suffixes unless `overwrite: true`.

### Exercise 3: Video only for failures

Configure `video: true` and the `after:spec` hook so that only failing specs keep their video. Create one passing spec and one failing spec. After `npx cypress run`, confirm that `cypress/videos` contains only the failing spec's MP4.

*Solution:* use Example 4's `setupNodeEvents`. If both videos remain, check that `results.tests[].attempts[].state` matches `'failed'` for the failing spec, and that your hook is returning `config`.

### Exercise 4: Mask a changing value

Add a `blackout` for the cart badge, add an item to the cart, and take a screenshot. Open the image and confirm the badge area is black. Explain in two sentences why this helps visual testing.

*Hint:* think about what happens to a pixel comparison when a number changes from 1 to 2.

### Exercise 5: CI artifacts (thought exercise)

Write the YAML steps that upload `cypress/screenshots` only when the job fails and `cypress/videos` always. Which of the two would you give a shorter retention, and why?

*Solution:* see the YAML in section 11. Videos are larger and often contain more incidental data, so they usually get shorter retention.

---

## Summary / Key Takeaways

- `cy.screenshot()` takes **manual** screenshots (page, viewport, runner or a single element) in both `open` and `run` modes; **failure screenshots** are automatic in `cypress run` and capture the whole runner.
- Control images with `capture`, `blackout`, `clip`, `padding`, `overwrite`, `disableTimersAndAnimations` and the `onBefore`/`onAfter` callbacks; set global defaults with `Cypress.Screenshot.defaults()`.
- `screenshotOnRunFailure` is on by default; `screenshotsFolder` defaults to `cypress/screenshots`.
- **Video is off by default since Cypress 13**; it records **one MP4 per spec** and only in `cypress run`. Set `video` and `videoCompression` explicitly, and be aware that documented compression defaults have varied across versions.
- `trashAssetsBeforeRuns` (default `true`) deletes old screenshots and videos before each run, so do not keep baselines there.
- Use `after:spec` to delete videos for passing specs and `after:screenshot` to rename or move images.
- Upload artifacts in CI, keep retention short, and never capture secrets.
- `cy.screenshot()` captures; it does not compare. Comparison arrives with **visual testing** (last lesson of today).

---

## External Resources

- Cypress documentation, Screenshots and Videos guide: https://docs.cypress.io/app/guides/screenshots-and-videos
- Cypress documentation, `cy.screenshot()` API reference: https://docs.cypress.io/api/commands/screenshot
- Cypress documentation, Configuration reference (video, screenshot and folder options): https://docs.cypress.io/app/references/configuration
