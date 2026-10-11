# Weekly Knowledge Check: [Week 5 - Friday: Cypress Advanced & Visual Testing]

**Covers:** Trace/time-travel debugging, screenshots and video, logging, recording user actions, editing generated code, visual testing.

**How to use this quiz:** Try each question before opening the solution. Questions marked **(version-dependent)** have answers that change between Cypress or plugin versions; the explanation says which version the answer is based on. Always check `npx cypress --version` and `npm ls cypress-visual-regression` against the docs for your own project.

---

## Part 1: Multiple Choice

### 1. What is a Cypress **snapshot**?
- [ ] A) A short video clip of the command running
- [ ] B) A HAR file listing the network traffic of the test
- [ ] C) A PNG image produced by `cy.screenshot()`
- [ ] D) A saved copy of the page's DOM and styles captured around a command

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A saved copy of the page's DOM and styles captured around a command

**Explanation:** Snapshots are DOM and CSS copies kept in memory so the Test Runner can rebuild the page "as it was" when you hover over or pin a command.
- **Why others are wrong:**
  - A) Video is a separate artifact, recorded per spec and only in `cypress run`.
  - B) Snapshots do not store network traffic; aliased requests show up as Command Log rows instead.
  - C) A screenshot is a real image file; a snapshot is a reconstructed DOM, not pixels.
</details>

---

### 2. Which commands get both a **Before** and an **After** snapshot?
- [ ] A) Only assertions such as `.should()`
- [ ] B) Only `cy.visit()`
- [ ] C) Action commands such as `click`, `type`, `check` and `select`
- [ ] D) Every Cypress command gets exactly two snapshots

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Action commands such as `click`, `type`, `check` and `select`

**Explanation:** Actions change the page, so Cypress captures the state just before and just after. Query and assertion commands (`get`, `contains`, `should`) typically get a single snapshot.
- **Why others are wrong:**
  - A) Assertions usually get one snapshot, not two.
  - B) `visit` is not the only (or defining) case; the rule is about action commands.
  - D) Queries and assertions typically have only one snapshot, so "every command" is false.
</details>

---

### 3. What happens when you **click a row** in the Command Log?
- [ ] A) The command is pinned: the preview stays frozen on its snapshot and details print to the DevTools console
- [ ] B) The test restarts from that command
- [ ] C) That command is deleted from the spec file
- [ ] D) Only that command is re-run against the live page

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The command is pinned: the preview stays frozen on its snapshot and details print to the DevTools console

**Explanation:** Hovering is temporary; clicking pins the snapshot, enables the Before/After switch for actions, and logs the element(s), selector and yielded value to the console.
- **Why others are wrong:**
  - B) Cypress cannot resume a test mid-way by clicking a row; use `cy.pause()` and **Next** for stepping.
  - C) The runner never edits your spec when you pin a row.
  - D) Pinning only displays stored data; it does not run anything.
</details>

---

### 4. Which statement about a Cypress "trace" is **accurate**?
- [ ] A) `cypress run --trace` writes a `trace.zip` just like Playwright
- [ ] B) Open-source Cypress has no `trace.zip` equivalent; the nearest thing for CI failures is Cypress Cloud **Test Replay**
- [ ] C) Test Replay produces a local `trace.zip` that you open with `npx cypress show-trace`
- [ ] D) `screenshotOnRunFailure` produces an interactive trace file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Open-source Cypress has no `trace.zip` equivalent; the nearest thing for CI failures is Cypress Cloud **Test Replay**

**Explanation:** Open-source time travel is a live, in-memory feature of `cypress open`. For CI, Test Replay (Cypress 13+, Chromium browsers, recorded to Cloud) gives an interactive replay.
- **Why others are wrong:**
  - A) There is no `--trace` flag or `trace.zip` in Cypress; that is Playwright's Trace Viewer.
  - C) Test Replay is hosted in Cypress Cloud, not a local zip, and there is no `show-trace` command.
  - D) A failure screenshot is a static image, not an interactive trace.
</details>

---

### 5. Automatic failure screenshots taken in `cypress run` use which `capture` mode?
- [ ] A) `viewport`
- [ ] B) `fullPage`
- [ ] C) Only the failing element
- [ ] D) `runner` (the Command Log plus the app preview)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `runner` (the Command Log plus the app preview)

**Explanation:** Failure screenshots always capture the whole runner, so one picture shows the red failed command beside the app state.
- **Why others are wrong:**
  - A) `viewport` is an option for manual screenshots, but failure screenshots ignore it.
  - B) `fullPage` is the default for manual page screenshots, not for failures.
  - C) Element capture only happens when you chain `.screenshot()` off an element yourself.
</details>

---

### 6. How does Cypress organise **video** recording?
- [ ] A) One video per test, in both `cypress open` and `cypress run`
- [ ] B) One video for the whole project, however many specs run
- [ ] C) One MP4 per spec file, recorded only in `cypress run`
- [ ] D) One video per browser tab, only in `cypress open`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) One MP4 per spec file, recorded only in `cypress run`

**Explanation:** All tests in a spec appear in one MP4 in `videosFolder`. Video is never recorded in interactive `cypress open`.
- **Why others are wrong:**
  - A) The unit is the spec file, not the test, and open mode records no video.
  - B) Each spec gets its own file.
  - D) There is no per-tab recording, and open mode does not record video.
</details>

---

### 7. Why is it risky to commit visual baselines inside `cypress/screenshots` with default settings?
- [ ] A) Cypress compresses images in that folder and ruins them
- [ ] B) `trashAssetsBeforeRuns` defaults to `true`, so Cypress deletes that folder's contents before each `cypress run`
- [ ] C) The folder is read-only
- [ ] D) Git always ignores PNG files

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `trashAssetsBeforeRuns` defaults to `true`, so Cypress deletes that folder's contents before each `cypress run`

**Explanation:** Cypress empties the screenshots and videos folders (including sub-folders) at the start of each run, so baselines kept there can vanish. Keep baselines in a different folder.
- **Why others are wrong:**
  - A) Cypress does not compress screenshots.
  - C) The folder is writable; that is where screenshots are saved.
  - D) Git tracks PNGs unless you add an ignore rule.
</details>

---

### 8. Which `cy.screenshot()` option paints chosen elements solid black **in the image only**, leaving the live app untouched?
- [ ] A) `blackout`
- [ ] B) `clip`
- [ ] C) `padding`
- [ ] D) `scale`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `blackout`

**Explanation:** `blackout` takes an array of CSS selectors. It hides changing or sensitive content (not available for `runner` captures).
- **Why others are wrong:**
  - B) `clip` crops the image to a rectangle `{ x, y, width, height }`.
  - C) `padding` adds space around an element screenshot.
  - D) `scale` controls whether the app is scaled down to fit the viewport.
</details>

---

### 9. A spec contains `console.log('user:', user)`. Where does that output go when the suite runs with `cypress run` in CI?
- [ ] A) The CI terminal
- [ ] B) The Command Log, then the terminal
- [ ] C) The browser's DevTools console, which nobody sees in headless CI; it is not forwarded to the terminal
- [ ] D) A file under `cypress/logs/`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The browser's DevTools console, which nobody sees in headless CI; it is not forwarded to the terminal

**Explanation:** Spec code runs in the browser, so `console.log` writes to the browser console. Use `cy.task` (Node) to reach the terminal.
- **Why others are wrong:**
  - A) The terminal is the Node process, not the browser.
  - B) Only `cy.log` and `Cypress.log` write to the Command Log.
  - D) Files are written only by `cy.task` handlers using `fs` or by `cy.writeFile`.
</details>

---

### 10. Which technique prints a line into the **CI terminal** from a spec?
- [ ] A) `cy.log('text')`
- [ ] B) `console.log('text')`
- [ ] C) `Cypress.log({ message: 'text' })`
- [ ] D) `cy.task('log', ...)` with a Node handler that calls `console.log`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `cy.task('log', ...)` with a Node handler that calls `console.log`

**Explanation:** `cy.task` bridges the browser to the Node process, where `console.log` writes to the terminal and CI logs.
- **Why others are wrong:**
  - A) `cy.log` only adds a Command Log row (UI, screenshots, videos).
  - B) `console.log` in a spec goes to the browser console.
  - C) `Cypress.log` also creates a Command Log row only.
</details>

---

### 11. Why does `console.log('A'); cy.log('B'); console.log('C');` show `A`, `C` in the console and only **afterwards** `B` in the Command Log?
- [ ] A) The test function runs synchronously and `cy.*` calls only add commands to a queue that runs after the function finishes
- [ ] B) `cy.log` is deliberately delayed by one second
- [ ] C) `console.log` has higher priority than every other function
- [ ] D) `cy.log` only runs if the test fails

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The test function runs synchronously and `cy.*` calls only add commands to a queue that runs after the function finishes

**Explanation:** This is the "command queue trap". Plain JavaScript runs immediately while the queue is built; queued commands execute afterwards. Put dependent code inside `.then()`.
- **Why others are wrong:**
  - B) There is no timed delay; it is about queueing.
  - C) Priority is not the mechanism; plain JS simply runs while the queue is built.
  - D) `cy.log` always runs as a queued command.
</details>

---

### 12. What does `autoEnd: false` in `Cypress.log({...})` mean?
- [ ] A) The row is hidden from the Command Log
- [ ] B) Cypress will not finish the row automatically; you must call `log.end()` yourself
- [ ] C) The message is sent to the terminal as well
- [ ] D) Snapshots are disabled for the row

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Cypress will not finish the row automatically; you must call `log.end()` yourself

**Explanation:** Use `autoEnd: false` for asynchronous custom commands. If you set it and forget `end()`, the row spins forever; if you leave the default for async work, the row ends too early.
- **Why others are wrong:**
  - A) Rows are hidden with `{ log: false }` on the command, not with `autoEnd`.
  - C) Terminal output requires `cy.task`.
  - D) Snapshots are controlled by calling `log.snapshot()`.
</details>

---

### 13. **(version-dependent)** On **Cypress 13 or 14**, which config option enables Cypress Studio?
- [ ] A) `studio: true`
- [ ] B) `experimentalRecorder: true`
- [ ] C) `experimentalStudio: true`
- [ ] D) `record: true`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `experimentalStudio: true`

**Explanation:** From Cypress 10.7 through 14.x the flag is `experimentalStudio`. Per the lesson (citing the Cypress experiments reference), it was removed in 15.4.0, where Studio needs no flag. Always check your installed version.
- **Why others are wrong:**
  - A) and B) are not real Cypress options.
  - D) `record` is a `cypress run` flag for uploading runs to Cypress Cloud, unrelated to Studio.
</details>

---

### 14. What does `npx cypress run --record --key <key>` do?
- [ ] A) Records your clicks and generates a spec file
- [ ] B) Records a screen video of your desktop locally
- [ ] C) Creates a Chrome Recorder JSON file
- [ ] D) Uploads the test run (results, screenshots, videos, Test Replay data) to Cypress Cloud

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Uploads the test run (results, screenshots, videos, Test Replay data) to Cypress Cloud

**Explanation:** In Cypress terminology "record" means recording a *test run* to Cloud. It never records user actions or writes test code.
- **Why others are wrong:**
  - A) Generating specs from clicks is what Studio or Chrome Recorder do.
  - B) Nothing is recorded from your desktop.
  - C) Recorder JSON comes from Chrome DevTools, not from this command.
</details>

---

### 15. Per the lesson, which set of commands does **Cypress Studio** record?
- [ ] A) `hover`, `drag`, `selectFile`
- [ ] B) `visit`, `intercept`, `request`
- [ ] C) `click`, `type`, `check`, `uncheck`, `select`
- [ ] D) Every Cypress command

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `click`, `type`, `check`, `uncheck`, `select`

**Explanation:** Studio records only this limited set (plus assertions added via right-click). Hover, drag and drop, file upload and keyboard shortcuts must be added by hand.
- **Why others are wrong:**
  - A) These are exactly the kind of actions Studio does not record.
  - B) These are not user actions recorded from the page.
  - D) Studio is far from recording every command.
</details>

---

### 16. A manual tester recorded a flow with the Chrome DevTools **Recorder**. How do you turn it into a Cypress spec?
- [ ] A) Paste the JSON into `cypress.config.js`
- [ ] B) Upload the JSON to Cypress Cloud
- [ ] C) Run `cypress run --record`
- [ ] D) Export it as JSON and convert it with the `@cypress/chrome-recorder` CLI (or use the Cypress Chrome Recorder extension)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Export it as JSON and convert it with the `@cypress/chrome-recorder` CLI (or use the Cypress Chrome Recorder extension)

**Explanation:** The CLI converts exported user-flow JSON into a `.cy.js` spec (default output `cypress/e2e`). The result is a draft that still needs assertions and cleanup.
- **Why others are wrong:**
  - A) The config file does not accept recordings.
  - B) Cypress Cloud does not convert Recorder files.
  - C) `--record` uploads test runs; it does not generate tests.
</details>

---

### 17. Which selector is the **most stable** choice for the username field?
- [ ] A) `div:nth-child(1) > .form_group > input`
- [ ] B) `[data-test="username"]`
- [ ] C) `.btn_inventory`
- [ ] D) `#root > div:nth-child(2)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[data-test="username"]`

**Explanation:** A dedicated test attribute is a deliberate contract between developers and testers and survives restyling and layout changes.
- **Why others are wrong:**
  - A) and D) are structural/positional selectors that break when the layout changes.
  - C) A styling class that changes with redesigns (and here it is also the wrong element).
</details>

---

### 18. After `cy.session()` sets up or restores a session, what state is the page in?
- [ ] A) Blank, so you must still call `cy.visit()` for the page you want
- [ ] B) It stays on the page you were on
- [ ] C) It automatically visits `baseUrl`
- [ ] D) It lands on the dashboard of the logged-in user

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Blank, so you must still call `cy.visit()` for the page you want

**Explanation:** With test isolation on (default since Cypress 12), the page is cleared; `cy.session` restores cookies and storage, not the page.
- **Why others are wrong:**
  - B) The page is cleared before the session is set up or restored.
  - C) No automatic visit happens.
  - D) Where the user lands is never implied; you navigate explicitly.
</details>

---

### 19. A recorded test is flaky after submitting a form, and a colleague added `cy.wait(3000)`. What is the better fix?
- [ ] A) Increase it to `cy.wait(6000)`
- [ ] B) Raise `defaultCommandTimeout` to 60 seconds for the whole project
- [ ] C) Wait for an event or state, such as `cy.url().should('include', '/success')` or `cy.wait('@submit')` on an aliased request
- [ ] D) Delete the assertions that fail

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Wait for an event or state, such as `cy.url().should('include', '/success')` or `cy.wait('@submit')` on an aliased request

**Explanation:** The lesson's rule is "wait for an event or a state, never for time". Assertions retry until true, so they double as synchronisation.
- **Why others are wrong:**
  - A) A longer fixed wait is still a guess: slower when the app is fast, still flaky when slow.
  - B) A huge global timeout hides problems and slows failures.
  - D) Deleting assertions makes a "green but useless" test.
</details>

---

### 20. Why is `.should()` preferred over a manual check inside `.then()` when the value may not be ready yet?
- [ ] A) `.should()` is faster to type
- [ ] B) `.then()` cannot access the DOM
- [ ] C) `.should()` only works on URLs
- [ ] D) `.should()` retries until it passes or times out, while `.then()` runs its callback once

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `.should()` retries until it passes or times out, while `.then()` runs its callback once

**Explanation:** Retry-ability is what makes Cypress assertions robust. A check in `.then()` that runs too early simply fails.
- **Why others are wrong:**
  - A) Typing speed is not the reason.
  - B) `.then()` receives the subject and can read the DOM; it just does not retry.
  - C) `.should()` works on any subject.
</details>

---

### 21. What does `cy.screenshot()` do with respect to **comparing** the page against an expected look?
- [ ] A) It compares automatically with the last run
- [ ] B) It fails the test when the page looks different
- [ ] C) It only captures an image; comparison needs a plugin or service
- [ ] D) It ships with pixelmatch built in

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It only captures an image; comparison needs a plugin or service

**Explanation:** Visual comparison comes from plugins (`cypress-visual-regression`, image-snapshot forks, and others) or services (Percy, Applitools) built on top of screenshots.
- **Why others are wrong:**
  - A) Nothing is compared automatically.
  - B) `cy.screenshot()` never fails because the page "looks wrong".
  - D) Pixelmatch is a library used by some plugins, not part of Cypress itself.
</details>

---

### 22. Why are **element-level** snapshots usually more reliable than full-page snapshots?
- [ ] A) Cypress cannot take full-page screenshots
- [ ] B) Element images are never compared pixel by pixel
- [ ] C) Elements cannot contain text
- [ ] D) A defect is a larger share of a smaller image, failures point to a component, and unrelated page changes do not break the test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A defect is a larger share of a smaller image, failures point to a component, and unrelated page changes do not break the test

**Explanation:** Smaller images allow tighter tolerances, and the failure tells you which component changed.
- **Why others are wrong:**
  - A) Full-page capture is the default for page screenshots.
  - B) Element images are compared the same way.
  - C) Elements can contain text; text rendering is a common source of noise.
</details>

---

### 23. Which baseline layout matches the lesson's `cypress-visual-regression` setup? **(version-dependent)**
- [ ] A) Baselines in a separate folder (default `cypress/snapshots/base`) while actual screenshots go to `screenshotsFolder` (for example `cypress/snapshots/actual`)
- [ ] B) Baselines and actual images share `cypress/screenshots`
- [ ] C) Baselines inside `node_modules`
- [ ] D) Baselines inside `cypress/videos`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Baselines in a separate folder (default `cypress/snapshots/base`) while actual screenshots go to `screenshotsFolder` (for example `cypress/snapshots/actual`)

**Explanation:** Keeping baselines apart means `trashAssetsBeforeRuns` empties only the `actual` folder. Version note: in `cypress-visual-regression` 5.3.0 the baselines are saved in a per-spec sub-folder, `cypress/snapshots/base/<spec file>/<name>.png` (the lesson's layout diagram omits the spec sub-folder).
- **Why others are wrong:**
  - B) Sharing the screenshots folder risks Cypress deleting baselines.
  - C) `node_modules` is installed code, not project assets.
  - D) The videos folder is also trashed before runs.
</details>

---

### 24. A dashboard visual test fails every night around midnight because it shows the current time. What is the best **first** fix?
- [ ] A) Raise `errorThreshold` to 1
- [ ] B) Freeze time with `cy.clock(...)` (and/or stub data or mask the element)
- [ ] C) Add more test retries
- [ ] D) Add `cy.wait(5000)` before the snapshot

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Freeze time with `cy.clock(...)` (and/or stub data or mask the element)

**Explanation:** Fix the root cause (dynamic data) at its source. Thresholds are the *last* tool, not the first.
- **Why others are wrong:**
  - A) A bigger threshold hides real defects without removing the changing data.
  - C) Retries can hide an unstable visual test.
  - D) A fixed wait does not stop the clock from changing.
</details>

---

## Part 2: True / False (Common Misconceptions)

### 25. True or False: A Cypress snapshot is a static copy of the page, so JavaScript is not running inside it and a dropdown will not open when you click it there.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** A snapshot is like a photograph rebuilt from saved DOM and CSS. It is for looking (inspect classes, sizes, highlighted matches), not for interacting. To work with the live page use `cy.pause()`.
</details>

---

### 26. True or False: `cy.screenshot()` fails the test when the page looks wrong.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `cy.screenshot()` only saves an image. It verifies nothing. Verification needs assertions or a visual-comparison plugin or service.
</details>

---

### 27. True or False: A `console.log()` placed in a spec appears in the terminal output of `cypress run` in CI.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Spec code runs in the browser, so `console.log` goes to the browser DevTools console, which is not forwarded to the terminal. Use `cy.task('log', ...)` (Node) or a plugin such as `cypress-terminal-report`.
</details>

---

### 28. True or False: In the Chrome DevTools Recorder you can set a **Selector attribute** (for example `data-test`) so recorded selectors prefer it.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Entering `data-test` in the *Selector attribute* field when creating a recording gives much more stable selectors. If it is left empty, Recorder falls back to its own heuristics (ARIA, text, CSS, XPath).
</details>

---

### 29. True or False: A manual check inside `.then(($el) => { expect(...) })` retries automatically just like `.should()`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `.should()` retries until it passes or times out; the `.then()` callback runs once. Use `.should()` for anything that may need time to become true.
</details>

---

### 30. True or False: Visual baselines should be generated in the same environment (OS, browser, ideally the same Docker image) where the comparisons run.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Fonts, anti-aliasing and scaling differ between macOS, Windows and Linux, so baselines from a laptop often fail on a Linux CI runner. Generate them in the CI image.
</details>

---

### 31. True or False: Chaining `.debug()` changes the subject of the command chain.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `.debug()` logs the subject to the console (and triggers `debugger` if DevTools is open) but the chain continues with the same elements.
</details>

---

### 32. True or False: Cypress records video only during `cypress run`, never during `cypress open`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Videos are a run-mode artifact (one MP4 per spec). In open mode you can watch the test live.
</details>

---

### 33. True or False: Calling `log.error(err)` on a `Cypress.log` object makes the test fail.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `log.error()` only marks the Command Log row as failed. You must also throw the error if you want the test to fail.
</details>

---

### 34. True or False: `cypress run --record` captures your clicks and generates test code for you.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `--record` uploads a *test run* to Cypress Cloud. Recording user actions into code is what Cypress Studio and the Chrome DevTools Recorder do.
</details>

---

### 35. True or False: In a recorded test, a `.click()` on an input immediately followed by `.type()` on the same input is redundant noise.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `.type()` already focuses (clicks) the element. Remove the extra click unless focus behaviour is what you are testing.
</details>

---

### 36. True or False: A good CI practice is to automatically accept the new screenshots as baselines whenever the visual job fails.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Approving a baseline is a deliberate human decision reviewed like code. Auto-approving would turn real visual bugs into the new "expected" look.
</details>

---

### 37. True or False: In `cypress run`, `numTestsKeptInMemory` defaults to `0`, so snapshots of finished tests are not retained.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** In `cypress open` the default is 50; in `cypress run` it is 0 because nobody is hovering over the Command Log. This is why interactive time travel is for open mode.
</details>

---

### 38. True or False: Automatic failure screenshots are taken in `cypress run`, but not in interactive `cypress open`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** In open mode you can look at the failed state. If you want an image while developing, call `cy.screenshot()` explicitly.
</details>

---

## Part 3: Code Prediction

### 39. A spec contains the test below. In what order do `1`, `3` and `4` appear in the **browser console**?
```js
it('order', () => {
  console.log('1');
  cy.log('2');
  cy.then(() => console.log('3'));
  console.log('4');
});
```
- [ ] A) 1, 3, 4
- [ ] B) 3, 1, 4
- [ ] C) 1, 4, 3
- [ ] D) 4, 1, 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 1, 4, 3

**Explanation:** The function body runs top to bottom synchronously. Plain `console.log` calls print immediately (`1`, `4`); `cy.log('2')` and `cy.then(...)` are queued and run afterwards, so `3` prints last. (`2` appears as a Command Log row, not in the console.) Verified with a small Node queue simulation.
- **Why others are wrong:**
  - A) Treats `cy.then` as if it ran in source order.
  - B) and D) Reverse the synchronous order of the two plain `console.log` calls or put queued code first.
</details>

---

### 40. What does this helper return?
```js
const SENSITIVE_KEYS = ['password', 'token', 'authorization', 'cardNumber'];

function sanitize(value) {
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) =>
        SENSITIVE_KEYS.includes(k) ? [k, '***'] : [k, sanitize(v)]
      )
    );
  }
  return value;
}

console.log(JSON.stringify(sanitize({ user: 'a', password: 'b', nested: { token: 'c' } })));
```
- [ ] A) `{"user":"a","password":"b","nested":{"token":"c"}}`
- [ ] B) `{"user":"a","password":"***","nested":{"token":"c"}}`
- [ ] C) `{"user":"***","password":"***","nested":"***"}`
- [ ] D) `{"user":"a","password":"***","nested":{"token":"***"}}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `{"user":"a","password":"***","nested":{"token":"***"}}`

**Explanation:** The function is recursive: sensitive keys are replaced by `'***'` and other values are sanitised again, so the nested `token` is masked too. Verified by running it in Node.
- **Why others are wrong:**
  - A) Nothing would be masked.
  - B) Would be the result of a non-recursive version; this one recurses.
  - C) Only keys in `SENSITIVE_KEYS` are masked, not `user` or the `nested` object itself.
</details>

---

### 41. With this config, what happens when a spec runs `cy.task('log', 'hi')`?
```js
setupNodeEvents(on, config) {
  on('task', {
    log(message) {
      console.log(message);
    },
  });
  return config;
}
```
- [ ] A) `hi` is printed in the terminal, but the `cy.task` command fails because the handler returned `undefined`
- [ ] B) It passes silently; `hi` is printed in the terminal
- [ ] C) `hi` is printed in the browser console
- [ ] D) The command fails before the handler is called

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `hi` is printed in the terminal, but the `cy.task` command fails because the handler returned `undefined`

**Explanation:** Task handlers run in Node, so `console.log` prints in the terminal, but a handler must return something other than `undefined` (use `return null`). Cypress fails the command when `undefined` is returned.
- **Why others are wrong:**
  - B) Missing `return null` is the most frequent task error and fails the command.
  - C) Tasks run in Node, not in the browser.
  - D) The handler is called; the failure comes from its return value.
</details>

---

### 42. What text does the Command Log row show?
```js
cy.log('User details', 'standard_user', 42);
```
- [ ] A) `User details`
- [ ] B) `User details standard_user 42`
- [ ] C) `User details, standard_user, 42`
- [ ] D) `["User details","standard_user",42]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `User details, standard_user, 42`

**Explanation:** `cy.log` joins the message and extra arguments into one line separated by a comma and a space.
- **Why others are wrong:**
  - A) Extra arguments are shown, not dropped.
  - B) The separator is a comma plus a space, not just a space.
  - D) Arguments are not rendered as a JSON array (use `JSON.stringify(obj)` for objects).
</details>

---

### 43. Given this `after:spec` hook, which videos are **kept**?
```js
on('after:spec', (spec, results) => {
  if (results && results.video) {
    const failed = results.tests.some((t) =>
      t.attempts.some((a) => a.state === 'failed')
    );
    if (!failed) fs.unlinkSync(results.video);
  }
});
```
Spec A: two tests, all attempts `passed`. Spec B: one test with attempts `failed`, then `passed` (a retry). Spec C: one test with attempts `failed`, `failed`.
- [ ] A) Only C
- [ ] B) Only B
- [ ] C) None
- [ ] D) B and C

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) B and C

**Explanation:** The hook checks whether **any attempt** failed. Spec B had a failed attempt (it passed only on retry), so its video is kept, which is useful for investigating flakiness. Spec C failed outright. Spec A has no failed attempt, so its video is deleted. Verified with a Node mock.
- **Why others are wrong:**
  - A) Ignores that a retried-then-passed test still had a failed attempt.
  - B) Forgets the fully failing spec C.
  - C) Would only be true if every spec passed on its first attempt.
</details>

---

### 44. Which folders are emptied before the next `cypress run`?
```js
module.exports = defineConfig({
  e2e: {
    screenshotsFolder: 'cypress/snapshots/actual',
    trashAssetsBeforeRuns: true,
  },
});
// Baselines are stored in cypress/snapshots/base
```
- [ ] A) Only `cypress/snapshots/base`
- [ ] B) `cypress/snapshots/actual` (and the videos folder), but not `cypress/snapshots/base`
- [ ] C) Both `actual` and `base`
- [ ] D) None, because trashing only happens after a failure

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `cypress/snapshots/actual` (and the videos folder), but not `cypress/snapshots/base`

**Explanation:** `trashAssetsBeforeRuns` deletes the contents of the configured screenshots and videos folders at the start of each `cypress run`. Baselines in a different folder are safe, which is the point of this layout.
- **Why others are wrong:**
  - A) Cypress only trashes the screenshots and videos folders; `base` is neither.
  - C) `base` is not a Cypress-managed assets folder, so it is not deleted.
  - D) Trashing happens before every run when the option is `true`.
</details>

---

### 45. Where is this screenshot saved, for the spec `cypress/e2e/login.cy.js` with default folders?
```js
cy.screenshot('login/after-submit');
```
- [ ] A) `cypress/screenshots/login/after-submit.png`
- [ ] B) `cypress/screenshots/login.cy.js-login-after-submit.png`
- [ ] C) `cypress/screenshots/login.cy.js/login/after-submit.png`
- [ ] D) `cypress/screenshots/after-submit.png`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `cypress/screenshots/login.cy.js/login/after-submit.png`

**Explanation:** Screenshots go in a folder named after the spec file, and slashes in the name create sub-folders. Checked with `path.join`.
- **Why others are wrong:**
  - A) Omits the spec-file folder.
  - B) Slashes make folders; they are not turned into dashes.
  - D) Drops both the spec folder and the `login` sub-folder.
</details>

---

### 46. **(version-dependent)** On Cypress 14 with this config, what does `npx cypress run` do about video?
```js
module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    screenshotOnRunFailure: true,
  },
});
```
- [ ] A) Records one MP4 per spec, compressed at CRF 32
- [ ] B) Records one MP4 per spec, uncompressed
- [ ] C) Records one MP4 per test
- [ ] D) Records no video, because `video` defaults to `false` since Cypress 13

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Records no video, because `video` defaults to `false` since Cypress 13

**Explanation:** In Cypress 12 and earlier the default was `true`; since 13.0 videos are off unless you set `video: true`. (Separately, the default for `videoCompression` has been described differently across versions, so set it explicitly when you enable video.)
- **Why others are wrong:**
  - A) and B) assume video is on; it is off by default now.
  - C) Even when enabled, video is per spec, not per test.
</details>

---

### 47. What is the **maximum number of attempts** of an always-failing test in `cypress run` versus `cypress open`?
```js
retries: { runMode: 1, openMode: 0 }
```
- [ ] A) 2 attempts in run mode, 1 in open mode
- [ ] B) 1 attempt in run mode, 0 in open mode
- [ ] C) 1 in both modes
- [ ] D) 2 in both modes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 2 attempts in run mode, 1 in open mode

**Explanation:** `retries` counts *extra* attempts: attempts = 1 + retries. Open mode shows the failure immediately; run mode retries once, so you may see two failure screenshots.
- **Why others are wrong:**
  - B) Confuses the number of retries with the number of attempts (0 attempts would mean the test never runs).
  - C) Run mode has one retry configured.
  - D) Open mode has zero retries.
</details>

---

### 48. The Selector Playground uses its **default** priority. Which selector does it suggest for this element?
```html
<button id="login-button" class="btn_action" data-test="login-button">Login</button>
```
- [ ] A) `#login-button`
- [ ] B) `.btn_action`
- [ ] C) `[data-test="login-button"]`
- [ ] D) `button`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `[data-test="login-button"]`

**Explanation:** The default priority is `data-cy`, `data-test`, `data-testid`, `id`, `class`, `tag`, `attributes`, `nth-child`. The element has no `data-cy`, so `data-test` wins over `id`, `class` and `tag`. A small Node simulation of "first strategy that has a value" confirms it.
- **Why others are wrong:**
  - A) `id` ranks below the `data-*` test attributes.
  - B) `class` ranks even lower.
  - D) `tag` is the weakest of these.
</details>

---

### 49. The `@cypress/chrome-recorder` CLI converts a Recorder `doubleClick` step into which Cypress code?
- [ ] A) `cy.get(selector).click({ multiple: true })`
- [ ] B) `cy.get(selector).click().click()`
- [ ] C) `cy.get(selector).rightclick()`
- [ ] D) `cy.get(selector).dblclick()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `cy.get(selector).dblclick()`

**Explanation:** Per the exporter README (quoted in the lesson): `navigate` becomes `cy.visit`, `click` becomes `.click()`, right-click becomes `.rightclick()`, `doubleClick` becomes `.dblclick()`, `change` becomes `.type()`. Requires Chrome 103+ for double-click and right-click steps.
- **Why others are wrong:**
  - A) `multiple: true` clicks several matched elements, not a double-click.
  - B) Two separate clicks are not the same event as a double-click.
  - C) `rightclick()` is the mapping for a right-click step.
</details>

---

### 50. With this config in `cypress/support/e2e.js`, which selector is suggested for `<input id="go" data-test="go">`?
```js
Cypress.SelectorPlayground.defaults({
  selectorPriority: ['data-qa', 'data-test', 'id'],
});
```
- [ ] A) `#go`
- [ ] B) `[data-test="go"]`
- [ ] C) `[data-qa="go"]`
- [ ] D) None, it throws an error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[data-test="go"]`

**Explanation:** Cypress uses the first strategy in the list for which the element has a value. There is no `data-qa`, so the next one, `data-test`, is used.
- **Why others are wrong:**
  - A) `id` is third in the list.
  - C) The element has no `data-qa` attribute to build a selector from.
  - D) A missing attribute just means that strategy is skipped.
</details>

---

### 51. How many tests does this loop define, and what are their names?
```js
Cypress._.times(3, (i) => {
  it(`run ${i + 1}`, () => { /* body */ });
});
```
- [ ] A) One test named `run 1`
- [ ] B) Three tests named `run 0`, `run 1`, `run 2`
- [ ] C) Three tests named `run 1`, `run 2`, `run 3`
- [ ] D) Ten tests named `run 1` to `run 10`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Three tests named `run 1`, `run 2`, `run 3`

**Explanation:** `_.times(3, fn)` calls `fn` with index 0, 1, 2, and the template adds 1. This is the temporary stability-check technique (do not commit it). Index-to-name mapping verified in Node.
- **Why others are wrong:**
  - A) The loop defines one `it` per iteration.
  - B) The name uses `i + 1`, so it starts at 1.
  - D) The loop count is 3 here (the lesson example uses 10).
</details>

---

### 52. What happens when this custom command is called as `cy.fillAddress({ firstName: 'Ada' })` with **no** previous command?
```js
Cypress.Commands.add('fillAddress', { prevSubject: 'element' }, ($form, address) => {
  cy.wrap($form).within(() => { /* type into fields */ });
});
```
- [ ] A) It works and `$form` is the `window`
- [ ] B) It works and `$form` is the `document`
- [ ] C) It runs with `$form` as `undefined`
- [ ] D) It fails, because a child command needs an existing element subject (for example `cy.get('form').fillAddress(...)`)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It fails, because a child command needs an existing element subject (for example `cy.get('form').fillAddress(...)`)

**Explanation:** `prevSubject: 'element'` declares a child command that must be chained off a command yielding a DOM element. Use `prevSubject: 'optional'` for a dual command.
- **Why others are wrong:**
  - A) and B) Cypress does not substitute `window` or `document` for an element requirement.
  - C) Cypress validates the subject and errors instead of passing `undefined`.
</details>

---

### 53. **(version-dependent)** Using `cypress-visual-regression` **5.3.0**, where `errorThreshold` is a **fraction** (not a percentage), what happens here?
```js
// image: 1000 x 500 px = 500,000 px
// 30,000 pixels differ from the baseline
cy.compareSnapshot('inventory-viewport', 0.1);
```
- [ ] A) It passes, because 0.1 means 10% of pixels may differ (up to 50,000 px) and 30,000 px is 6%
- [ ] B) It fails, because 0.1 means 0.1%, which is only 500 pixels
- [ ] C) It fails, because `errorThreshold` counts pixels, so 0.1 allows 0.1 pixels
- [ ] D) It passes, because `errorThreshold` is ignored in regression mode

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It passes, because 0.1 means 10% of pixels may differ (up to 50,000 px) and 30,000 px is 6%

**Explanation:** In 5.3.0 the threshold is compared with the fraction `mismatchedPixels / totalPixels` (30,000 / 500,000 = 0.06 which is below 0.1). **Lesson discrepancy:** `visual-testing.md` describes `errorThreshold` as a percentage (0.1 = 0.1%). That reading is version-dependent and is not what 5.3.0 does. Always check the README of the version you install, and use `npm ls cypress-visual-regression`. Arithmetic checked in Node.
- **Why others are wrong:**
  - B) This is the lesson's percent reading, which does not match 5.3.0.
  - C) The threshold is a ratio of mismatched pixels, not an absolute pixel count.
  - D) The threshold applies exactly in `regression` mode; `base` mode is what skips comparison.
</details>

---

### 54. The baseline was generated **without** `blackout` (cart badge showing `1`). The regression run adds the mask below, with a strict threshold of 0. What happens?
```js
cy.compareSnapshot('inventory-with-item', {
  errorThreshold: 0,
  blackout: ['[data-test="shopping-cart-badge"]'],
});
```
- [ ] A) It passes, because masks are applied only to the actual image
- [ ] B) It fails, because the actual image has a black rectangle where the baseline has the badge
- [ ] C) Cypress silently updates the baseline
- [ ] D) The comparison is skipped

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It fails, because the actual image has a black rectangle where the baseline has the badge

**Explanation:** The mask must also be present when the baseline is created, otherwise the two images differ. After adding a mask, regenerate the baseline with `visualRegressionType=base`.
- **Why others are wrong:**
  - A) A one-sided mask creates a difference, which is exactly why baselines must use the same mask.
  - C) Baselines are never updated automatically; that is a deliberate human action.
  - D) In `regression` mode the comparison runs.
</details>

---

## Part 4: Fill-in-the-Blank

### 55. To keep the app preview frozen on a command's snapshot, you _____ it by clicking its row in the Command Log.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** pin (pinning)

**Explanation:** Hover to time-travel temporarily; click to pin. A pinned action command also offers Before/After snapshots and prints details to the DevTools console.
</details>

---

### 56. In `cypress open`, the `numTestsKeptInMemory` option keeps snapshots for this many tests by default: _____ (in `cypress run` the default is `0`).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 50

**Explanation:** Lowering it reduces memory use for very large specs. In run mode it is `0` because nobody inspects finished tests interactively.
</details>

---

### 57. `cy.screenshot()` accepts three `capture` values: `'fullPage'` (default for page screenshots), `'viewport'` and `'_____'`, which includes the Command Log.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** runner

**Explanation:** `'runner'` captures the entire Test Runner window. It is what automatic failure screenshots use, and it is a poor choice for visual baselines because the Command Log changes constantly.
</details>

---

### 58. **(version-dependent)** The default value of `video` changed to `false` in Cypress _____ (it was `true` in Cypress 12 and earlier).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 13 (Cypress 13.0)

**Explanation:** If a pipeline "lost its videos" after an upgrade, this is why. Set `video: true` explicitly and set `videoCompression` explicitly too, because its documented default has varied across versions.
</details>

---

### 59. A `cy.task` handler must return a value other than _____ (return `null` if there is nothing to return), otherwise Cypress fails the command.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** undefined

**Explanation:** This check catches typos in event names and forgotten returns. A handler may also return a promise.
</details>

---

### 60. In an asynchronous custom command, create the log with `Cypress.log({ ..., _____: false })` and call `log.end()` yourself when the work finishes.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** autoEnd

**Explanation:** `autoEnd` defaults to `true`. For async work, turn it off, otherwise the row ends before the work is done.
</details>

---

### 61. The command `npx cypress run --_____ --key <your-record-key>` uploads a test run to Cypress Cloud.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** record

**Explanation:** `--record` records the *run* (results, screenshots, video, Test Replay data). It does not record user actions. Keep the key in a CI secret or the `CYPRESS_RECORD_KEY` environment variable.
</details>

---

### 62. To make Studio and the Selector Playground prefer `data-qa` attributes, call `Cypress.SelectorPlayground.defaults({ _____: ['data-qa', 'id'] })`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** selectorPriority

**Explanation:** `selectorPriority` is an ordered array; Cypress uses the first strategy for which the element has a value. Put the call in `cypress/support/e2e.js`.
</details>

---

### 63. `cy._____(id, setupFn, { validate })` runs a login once, caches cookies and storage, and restores them in later tests.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** session

**Explanation:** `cy.session` shows `created`, `restored` or `recreated` in the Command Log. The page is blank afterwards, so call `cy.visit()` for the page you want.
</details>

---

### 64. A custom child command that must be chained off a DOM element is declared with `Cypress.Commands.add('name', { _____: 'element' }, fn)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** prevSubject

**Explanation:** `prevSubject: 'element'` makes a child command; `prevSubject: 'optional'` makes a dual command that works with or without a previous subject.
</details>

---

### 65. The approved reference screenshot that every later screenshot is compared against is called the _____ (also "base" or "golden" image).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** baseline

**Explanation:** Baselines are committed to Git, reviewed like code, and updated only by a deliberate human decision.
</details>

---

### 66. The browser-side command that `cypress-visual-regression` adds to compare a screenshot with its baseline is `cy._____('name')`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** compareSnapshot

**Explanation:** `addCompareSnapshotCommand()` in the support file registers `cy.compareSnapshot()`. Without that import you get "cy.compareSnapshot is not a function". Version note: the `errorThreshold` argument is a fraction in 5.3.0 (0.1 allows 10% of pixels to differ), unlike the percent wording in the lesson.
</details>
