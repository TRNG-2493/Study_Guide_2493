# Recording User Actions: Cypress Studio, Chrome DevTools Recorder and Cypress Cloud

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what "record and playback" (also called "record and generate") means, what it is good for, and why recorded tests are a **starting point**, not a finished product.
- Describe the history and **current status of Cypress Studio**, including the version-dependent `experimentalStudio` flag (needed in Cypress 10.7 through at least 14, no longer present in recent 15.x releases), its Beta label, its requirements and its limitations.
- Launch Cypress Studio, record a login-and-add-to-cart flow, add assertions by right-clicking, and save the generated commands into a spec file.
- Configure the **Selector Playground priority** so that recorded selectors prefer stable attributes such as `data-test`.
- Record a flow with the **Chrome DevTools Recorder**, export it as JSON, and convert it to a Cypress test using the **`@cypress/chrome-recorder`** CLI or the Cypress Chrome Recorder extension.
- Explain what **Cypress Cloud** does and does not do in relation to recording (it records *test runs*, not user actions, and is connected to the AI-assisted Studio features in recent versions).
- Compare the three approaches (Studio, Chrome Recorder export, hand-writing) and choose the right one for a situation.
- Identify the typical weaknesses of generated code, preparing for the next lesson, "Editing generated code".

---

## Why This Matters

This week's epic is about growing from a tester who can click through a form in a script into a Test Automation Engineer who builds reliable, maintainable suites across tools. You have already learned how to write Cypress tests by hand. But in the real world, **speed of creation** matters too. Imagine you must automate fifteen user journeys for **Project 1: QE Foundations** before a deadline. Recording the *skeleton* of each journey by clicking through the application, and then refining the generated code, can save a lot of typing, and it is also a wonderful way to **discover what selectors and commands a flow needs**.

Recording is also a bridge between roles. A manual tester who does not yet write code can record a flow; an automation engineer then reviews and hardens it. Product owners can record a scenario to show a bug. Many teams use recorders to produce a first draft in minutes.

Yet recording has a bad reputation among experienced engineers, and rightly so, if used carelessly. A recorded test is typically a straight line of clicks and typing with no assertions, brittle selectors and no structure. A suite made of raw recordings becomes a maintenance nightmare. Today you will learn *both sides*: how to record, and what to be careful about. The next lesson, "Editing generated code", is where we turn raw recordings into professional tests.

You may remember Playwright's code generator (`codegen`), which does the same job in that tool. The idea is identical; the tools and their quirks differ.

---

## The Concept

### 1. What is record and playback?

**Record and playback** means: you perform actions in a real browser (click, type, select), and a tool writes the corresponding test commands for you. When you "play back" the generated test, it repeats those actions automatically.

Under the hood, a recorder attaches event listeners to the page. When you click, it notes *which element* you clicked (it computes a **selector** that identifies the element) and *what you did* (click, type, select, check). It then writes a line such as `cy.get('[data-test="login-button"]').click();`.

Strengths:

- Very fast to produce a first draft.
- Helps beginners see the mapping between user actions and test commands.
- Helps discover selectors and navigation paths.
- Handy for reproducing a bug as a test quickly.

Weaknesses:

- The recorder knows **what you did**, but not **what you expected**. So there are usually no assertions, and a test with no assertions verifies nothing (apart from "did not crash").
- Selectors are auto-generated and may be fragile (long CSS paths, `nth-child`, auto-generated classes).
- No structure: no reuse, no page objects, no test data separation.
- Timing/wait issues may be hidden, and conditional behaviour (pop-ups) is not captured.
- Cannot capture everything: iframes, shadow DOM, multiple origins, drag-and-drop and complex gestures are often unsupported.

### 2. The three recording options in the Cypress world

| Option | What it is | Cost | Typical use |
|---|---|---|---|
| **Cypress Studio** | Built into the Cypress Test Runner; records actions directly into your spec file. | Free for the core recording; AI suggestions need a Cypress Cloud account (recent 15.x). | Quick additions and drafts inside the Cypress workflow. |
| **Chrome DevTools Recorder + export to Cypress** | Chrome's built-in Recorder panel records a flow; you export it to Cypress code via an extension or a CLI. | Free. | Recording independently of Cypress, sharing recordings as JSON, flows that Studio cannot handle. |
| **Cypress Cloud AI/recording-related features** | Cypress Cloud is primarily a service for recording and analysing *test runs*. In recent versions it also powers AI-assisted features connected to Studio. | Paid plans, with free tier/trial limits. | Team dashboards, Test Replay (previous lesson), and optional AI help. |

Let us go through each carefully, including version caveats.

### 3. Cypress Studio

#### 3.1 A short history (so you can read old tutorials correctly)

- **Cypress 6.3 (January 2021):** Cypress Studio was introduced as an *experimental* feature, enabled with a configuration flag.
- **Cypress 10.0:** Studio was removed in the big Cypress 10 redesign (the team said refactoring it was too costly at that point), and the Cypress team pointed people to the Chrome DevTools Recorder as an alternative.
- **Cypress 10.7 (August 2022):** Studio came back as an *experimental* feature. To use it, you had to set `experimentalStudio: true` in your configuration.
- **Cypress 10.7 through 14.x:** the `experimentalStudio` flag is the way to enable it. Many articles and videos you will find online describe this era, including the instruction "add `experimentalStudio: true` to cypress.config.js".
- **Cypress 15.4.0:** the official experiments reference states that the `experimentalStudio` option was **removed** in 15.4.0 and Studio is now the default behaviour (no flag required). The current Studio documentation still describes Studio as **Beta**.
- **Cypress 15.11.0 and later:** the Studio documentation describes an AI-assisted mode ("Studio AI") that suggests assertions; it requires Cypress 15.11.0 or later and a Cypress Cloud account (a free account is enough, and an anonymous trial allows a limited number of accepted suggestions).

> Version rule of thumb for this course: **if you are on Cypress 13 or 14, set `experimentalStudio: true`. If you are on a recent 15.x or 16.x release, Studio is available without a flag. Always check which version you have with `npx cypress --version` and read the docs that match.** The Studio page on docs.cypress.io is the authority for the current behaviour; this lesson is a teaching summary and details may evolve.

#### 3.2 Enabling Studio (Cypress 13 / 14 era)

In `cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    experimentalStudio: true,
  },
});
```

On recent versions where the option was removed, you simply omit it. If you leave it in a very recent version, Cypress may warn you that the option is no longer needed or is unknown; delete it.

#### 3.3 Requirements and limitations (current docs)

- **Studio needs sourcemaps and internet access** to function.
- **E2E only:** component testing and Cucumber-style tests are not supported.
- **No recording across multiple origins** (for example, a login that redirects to another domain).
- **iframes and Shadow DOM are not supported** in recording.
- It records only a limited set of commands: `.click()`, `.type()`, `.check()`, `.uncheck()` and `.select()`. Other actions (hover, drag and drop, file upload, keyboard shortcuts) are not recorded; you add them by hand.
- Recorded commands are **appended to the end of an existing test** (or into a new test); Studio does not reorganise your code.
- AI suggestions can be noisy with animations, and very large pages may exceed context limits.

#### 3.4 How to launch Studio (current UI)

The docs list three entry points:

1. In the Cypress app, on a spec or suite, click **New Test** to create a new test and record into it.
2. In the Test Runner, hover over an existing test in the Command Log and click **Edit in Studio**.
3. Click **Studio Beta** in the header of the runner (the label says "Beta" in the current documentation, so the interface text you see may differ slightly in your version).

In older versions (10.7 to 14), the typical entry was: hover over a test in the Command Log, click the small **magic wand** icon (**Add Commands to Test**), or, for a spec with no tests, click **Add New Test** (also shown as a wand icon). The interface has changed, so rely on what you see on screen and the docs for your version.

#### 3.5 Step-by-step: your first recording

We will record a login and add-to-cart flow on https://www.saucedemo.com.

1. **Create a spec.** In `cypress/e2e/`, create `studio-demo.cy.js` containing a test with the first step already written:

```js
describe('Studio demo', () => {
  it('logs in and adds a product', () => {
    cy.visit('https://www.saucedemo.com');
  });
});
```

2. **Run it in `cypress open`.** Start `npx cypress open`, choose E2E, choose a browser, click `studio-demo.cy.js`.
3. **Open Studio** on that test using one of the entry points above. The runner enters recording mode: the preview is *live*, and Studio watches your actions. A small panel lists the commands as they are recorded.
4. **Interact like a user:** click the username field and type `standard_user`; click the password field and type `secret_sauce`; click **Login**; click **Add to cart** for the first product.
5. **Add an assertion:** *right-click* the cart badge (the small number next to the cart icon). A context menu appears offering assertion options (for example "should have text", "should be visible", "should contain"). Choose "have text" and the value shown. Studio records `cy.get(...).should('have.text', '1')`.
6. **Save.** Click **Save Commands** (the wording may differ). Studio writes the commands into your spec file in place.

You will now find new code in your spec, wrapped in comment markers such as:

```js
describe('Studio demo', () => {
  it('logs in and adds a product', () => {
    cy.visit('https://www.saucedemo.com');
    /* ==== Generated with Cypress Studio ==== */
    cy.get('[data-test="username"]').clear();
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').clear();
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');
    /* ==== End Cypress Studio ==== */
  });
});
```

The exact comment text, and whether `.clear()` calls are inserted before `.type()`, depends on the version. The important points are the structure and that the code is **plain Cypress** that you can edit freely. The marker comments help you see which lines were generated; you can delete them once you have reviewed the code.

**Line-by-line explanation of the generated code**

1. `cy.visit('https://www.saucedemo.com');` was written by *you*; Studio appended after it.
2. `/* ==== Generated with Cypress Studio ==== */` is a comment marking the start of the generated block.
3. `cy.get('[data-test="username"]').clear();` finds the username field and clears its existing content. Studio often inserts `clear()` before typing so that replaying the test does not append text to a pre-filled field.
4. `cy.get('[data-test="username"]').type('standard_user');` types the username. It re-queries the same element (Studio writes one `cy.get` per action instead of chaining).
5. The password lines are the same pattern.
6. `.click()` on the login button navigates to the inventory page.
7. `cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();` adds the product.
8. `cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');` is the assertion you added with the right-click menu: the badge must read "1".
9. `/* ==== End Cypress Studio ==== */` closes the block.

#### 3.6 Selector quality: `Cypress.SelectorPlayground.defaults`

Studio and the Selector Playground generate selectors using a **priority list**. By default Cypress prefers (in order): `data-cy`, `data-test`, `data-testid`, `id`, `class`, `tag`, `attributes`, `nth-child`. If your application uses `data-qa` or `data-automation-id` instead, tell Cypress. In `cypress/support/e2e.js`:

```js
Cypress.SelectorPlayground.defaults({
  selectorPriority: ['data-test', 'data-testid', 'data-cy', 'id', 'name', 'class', 'tag'],
});
```

**Explanation:** `Cypress.SelectorPlayground.defaults` sets global defaults for the playground. `selectorPriority` is an ordered array of strategies. When Cypress inspects an element, it uses the *first* strategy in the list for which the element has a value. For the login button on Sauce Demo, `data-test="login-button"` wins, producing `[data-test="login-button"]` instead of something like `#login-button` or `.submit-button.btn_action`. Because the test attribute is a deliberate contract between developers and testers, it breaks far less often than class names.

Also remember what you learned on Thursday in "Element location": good selectors describe *intent*, not layout.

#### 3.7 Studio AI (recent versions)

Recent 15.x documentation describes **Studio AI**: while you interact with the application, it proposes assertions based on visible changes (visibility, text, form values, attributes, URL and title). It:

- requires **Cypress 15.11.0 or later**,
- requires a **Cypress Cloud** account linked to the project,
- only observes what *you* interact with (it does not crawl your app),
- needs your review: AI suggestions are drafts, not truth.

This is a fast-moving area. Treat anything AI-generated like a pull request from a new teammate: read it, question it, edit it. There is also a newer AI-based command in the 15.x line (`cy.prompt`) for writing steps in natural language; its behaviour and availability depend on version and plan, so check the official documentation before relying on it.

### 4. Chrome DevTools Recorder, exported to Cypress

#### 4.1 What it is

The **Recorder** is a panel in Google Chrome's DevTools (available in Chrome 101+). It records your interactions in any web page (including pages that Cypress cannot easily record, because Recorder works outside the Cypress runner) and stores them as a **user flow**. A user flow is a JSON document listing *steps*: `setViewport`, `navigate`, `click`, `change`, `keyDown`, `keyUp`, `scroll`, `waitForElement`, and more.

#### 4.2 How to record

1. Open DevTools (F12), click the **three dots menu** > **More tools** > **Recorder**. (Alternatively press `Ctrl+Shift+P` / `Cmd+Shift+P` inside DevTools and type "Recorder".)
2. Click **Create a new recording**. Give it a name (such as `saucedemo-login`). In the **Selector attribute** field, enter the test attribute your app uses (for example `data-test`). The Recorder will prefer it, which gives you much better selectors. If the field is left empty, Recorder uses its own heuristics (ARIA role/name, text, CSS and XPath fallbacks).
3. Click **Start recording**. Perform the flow in the page.
4. Click **End recording**.
5. Use **Replay** to check that it works inside Chrome.
6. Click the **export** (download) icon to export as **JSON**, which is the native format for Recorder, or choose another export format if available in your Chrome version.

Recorder in Chrome can export directly to some formats (for example Puppeteer, and, via extensions, other tools). For Cypress, you have two paths.

#### 4.3 Exporting to Cypress

**Path A: the Cypress Chrome Recorder extension.** Install the *Cypress Chrome Recorder* extension from the Chrome Web Store. It adds an **Export as a Cypress Test** option to the Recorder's export menu, producing a `.cy.js`-style test directly.

**Path B: the `@cypress/chrome-recorder` CLI.** It converts exported JSON recordings into Cypress tests from the command line. From the official repository:

```bash
# Interactive mode: prompts you for input and output paths
npx @cypress/chrome-recorder

# Convert one file
npx @cypress/chrome-recorder ./recordings/saucedemo-login.json

# Convert every JSON file in a folder
npx @cypress/chrome-recorder ./recordings/*.json
```

Useful options: `-o, --output` to set the output folder, `-d, --dry` for a dry run that changes no files, `-p, --print` to print the result, and `-f, --force` to bypass Git safety checks. By default the output goes to your `cypress/e2e` folder (older Cypress versions used `cypress/integration`); make sure the folder exists.

Requirements from the project's documentation: Chrome 101 or newer to export JSON, and Chrome 103 or newer for double-click and right-click steps.

**How steps are translated** (from the official README):

| Recorder step | Generated Cypress code |
|---|---|
| `navigate` | `cy.visit(url)` |
| `setViewport` | `cy.viewport(width, height)` |
| `click` | `cy.get(selector).click()` |
| right click | `cy.get(selector).rightclick()` |
| `doubleClick` | `cy.get(selector).dblclick()` |
| `change` (typing) | `cy.get(selector).type(text)` |
| `keyDown` | `cy.type("{key}")` |
| `keyUp` | not exported |
| `hover` | `cy.get(selector).trigger()` |
| `scroll` | `cy.scrollTo(x, y)` |

Unsupported step types produce a warning in the CLI. The README does not describe how selectors are chosen, so inspect them carefully after generation.

An example of exported code might look like:

```js
describe('saucedemo-login', () => {
  it('tests saucedemo-login', () => {
    cy.viewport(1280, 720);
    cy.visit('https://www.saucedemo.com/');
    cy.get('[data-test="username"]').click();
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
  });
});
```

(Exact output varies by version of the tool and the selectors Recorder chose.)

**Line-by-line explanation**

1. `describe('saucedemo-login', ...)` and `it('tests saucedemo-login', ...)` are named after your recording. You should rename them to meaningful business names (next lesson).
2. `cy.viewport(1280, 720)` sets the window size recorded at the start. Keep it if layout matters; otherwise centralise it in config.
3. `cy.visit(...)` is the recorded `navigate` step.
4. `cy.get('[data-test="username"]').click()` is the click that focused the field. It is harmless but redundant, because `.type()` focuses the element itself.
5. `.type('standard_user')` types into the field. The Recorder emitted a `change` step with the final value, so the code types the whole text.
6. The last lines fill the password and click the button.
7. Notice: **no assertions at all.** A recording cannot know what the page should show after login.

#### 4.4 Studio vs Chrome Recorder

| Aspect | Cypress Studio | Chrome DevTools Recorder + export |
|---|---|---|
| Runs where | Inside the Cypress runner | Chrome DevTools, independent of Cypress |
| Output | Appended directly to your spec | JSON then converted to a spec file |
| Assertions | Right-click menu, or AI suggestions (recent versions) | None automatically; add by hand |
| Selector control | `Cypress.SelectorPlayground.defaults` | "Selector attribute" field in Recorder |
| Cross-origin flows | Not recorded | Recorded (Recorder is not limited by Cypress's origin rules), but Cypress may have its own cross-origin handling (`cy.origin`) when you run the result |
| iframes / Shadow DOM | Not supported | Partial support in Recorder; the generated Cypress code may need manual changes |
| Non-Cypress browsers | Cypress-supported browsers | Chrome only |
| Sharing | The spec file | A JSON file that can be shared and exported to other tools (for example Playwright, Puppeteer) |
| Maturity | Beta (current docs) | Chrome feature; the exporter is a separate open-source tool |

A good habit: **use Studio** when you are already inside a Cypress spec and want to add a few steps or assertions; **use Chrome Recorder** when you need to capture an awkward flow or want the same recording for multiple tools.

### 5. Cypress Cloud and "recording": clearing up a naming confusion

Cypress documentation uses the word **record** in a different sense: `cypress run --record` *records a test run* to **Cypress Cloud**. That means it uploads results, screenshots, videos and (on supported plans and browsers) Test Replay data so that your team can view them in a dashboard. It does **not** record user actions or write test code.

The connections between Cypress Cloud and "recording user actions" are:

1. **Studio AI** (recent versions) needs a Cloud account to generate assertion suggestions.
2. Debugging recorded CI runs with Test Replay (previous lesson).
3. Cloud project settings and keys used with `--record --key`.

So: *Cloud is not a recorder of your clicks*. If someone says "we record our tests in Cypress Cloud", they mean they upload their run results.

### 6. The pattern: record, review, refine

A healthy workflow looks like this:

1. **Decide the scenario first** ("A standard user can log in, add a product and see it in the cart"), including what must be *verified*.
2. **Record** the happy path in Studio or Recorder.
3. **Review** the generated code for selectors, redundant steps, missing waits and missing assertions.
4. **Refine:** rename, add assertions, extract helpers and custom commands, and move data out of the test (next lesson).
5. **Run it repeatedly** (at least 5-10 times) to check stability.
6. **Commit** only the refined test.

---

## Code Examples

### Example 1: Minimal config that works on both older and newer Cypress

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    // Needed in Cypress 10.7 - 14.x. Remove on Cypress 15.4.0 or later,
    // where Studio no longer needs a flag.
    experimentalStudio: true,
    setupNodeEvents(on, config) {
      return config;
    },
  },
});
```

**Explanation**

- `defineConfig` wraps the config for editor help.
- `baseUrl` lets tests use `cy.visit('/')`.
- `experimentalStudio: true` is a *boolean flag* that turned on Studio during the experimental era. We keep the comment so the next engineer knows when to delete it.
- `setupNodeEvents` is empty here but is where plugins and tasks (like the `log` task from the logging lesson) are registered.

### Example 2: Making recorded selectors prefer test attributes

`cypress/support/e2e.js`:

```js
Cypress.SelectorPlayground.defaults({
  selectorPriority: ['data-test', 'data-testid', 'data-cy', 'id', 'class', 'tag'],
  onElement: ($el) => {
    const qa = $el.attr('data-qa');
    if (qa) {
      return `[data-qa="${qa}"]`;
    }
  },
});
```

**Line-by-line explanation**

1. `Cypress.SelectorPlayground.defaults({...})` configures the Selector Playground (and therefore the selectors Studio suggests).
2. `selectorPriority` is the ordered list of attribute strategies.
3. `onElement` is an optional callback that runs for every element you hover or select. It receives the jQuery element (`$el`).
4. `$el.attr('data-qa')` reads the `data-qa` attribute, if any.
5. If it exists, we return a custom selector string. Returning a value overrides the default logic; returning nothing (`undefined`) lets Cypress continue with the priority list.

### Example 3: A raw recording vs the intention (a taste of the next lesson)

Raw recorded steps (assertions missing, duplicated queries):

```js
it('recorded', () => {
  cy.visit('/');
  cy.get('[data-test="username"]').click();
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').click();
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();
  cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
});
```

Intent captured as a test you could be proud of:

```js
it('adds the backpack to the cart after login', () => {
  cy.visit('/');
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();
  cy.url().should('include', '/inventory.html');

  cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
  cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');
});
```

**Explanation**

- The refined test removes redundant `click()` calls before `type()`, adds a URL assertion to verify login success *before* continuing, and finishes with an assertion about the outcome. The test name now states the behaviour being verified.
- The full cleanup process (custom commands, `cy.session`, data from fixtures) is in the next lesson.

### Example 4: Converting a Recorder export with the CLI, then running it

```bash
# 1. Create a folder for recordings
mkdir recordings

# 2. Move your exported JSON into it (exported from DevTools > Recorder > Export > JSON)
#    recordings/saucedemo-login.json

# 3. Preview the result without writing files
npx @cypress/chrome-recorder --dry ./recordings/saucedemo-login.json

# 4. Generate the spec into cypress/e2e
npx @cypress/chrome-recorder ./recordings/saucedemo-login.json

# 5. Open Cypress and run it
npx cypress open
```

**Explanation**

1. The folder keeps your raw recordings organised; committing them is optional.
2. `--dry` shows what would be generated without changing the repository, useful on a shared project.
3. The second command writes the `.cy.js` file (by default into `cypress/e2e`).
4. `npx cypress open` lets you run it with time travel, and then refine it.

### Example 5: Handling a step that recorders cannot capture

Some flows include hovering to open a menu, drag-and-drop or file upload. Studio does not record them, and the Chrome export may produce a limited `trigger()`. You add them by hand:

```js
cy.get('[data-test="menu"]').trigger('mouseover');
cy.get('[data-test="menu-item-reports"]').should('be.visible').click();

cy.get('input[type="file"]').selectFile('cypress/fixtures/report.pdf');
```

**Explanation**

- `trigger('mouseover')` fires a DOM event to simulate hovering (Cypress cannot truly move a mouse cursor, which is a known difference from Playwright's `hover()`).
- `.should('be.visible').click()` waits until the submenu appears before clicking. The assertion doubles as a wait.
- `selectFile` (built into Cypress since 9.3) attaches a fixture file to an `<input type="file">`.

---

## Real-World Scenarios

### Scenario 1: Reproducing a bug report in 10 minutes

A tester reports: "When I apply a discount code and then change the quantity, the total is wrong." Rather than write code from scratch, a developer records the flow with Studio, saves it, adds an assertion for the expected total (right-click on the total), and commits the failing test with the bug ticket. When the fix is merged, the same test protects against regression.

### Scenario 2: Onboarding a manual tester

A manual tester with no coding background records ten regression journeys with the Chrome Recorder, exports JSON, and the automation engineer converts them with the CLI. The engineer reviews each one, adds assertions, extracts a `cy.login()` command and merges them. The manual tester learns by reading the diff between "raw" and "refined".

### Scenario 3: Cross-tool sharing

A team evaluating Cypress and Playwright records one checkout flow in Chrome Recorder, exports JSON, and generates a Cypress test via the CLI and a Playwright test via another exporter, so they can compare the code and run time of each tool on identical behaviour. This supports the cross-tool perspective that is the epic of this week.

### Scenario 4: Why a recorded suite became a burden

A project recorded 200 tests and never refactored them. Every test repeated the login steps, selectors used `nth-child`, and none had assertions. After a minor redesign, 150 of them broke. The team spent two weeks fixing selectors one by one. The lesson: **recording is for drafts; maintainability requires refactoring**.

---

## Common Pitfalls and Best Practices

1. **Treating a recording as a finished test.** Always add assertions and review selectors.
2. **Following outdated tutorials.** Many guides show `experimentalStudio: true`, the old Studio UI and `cypress/integration`. Check your version and the current docs.
3. **Ignoring Studio's limitations.** No iframes, Shadow DOM or cross-origin recording; only five commands are recorded. Plan to add the rest by hand.
4. **Fragile selectors.** If the generated selector contains `nth-child`, generated class names or very long chains, replace it. Prefer `data-test` style attributes and ask developers to add them.
5. **Recording on a slow or unstable environment.** Mis-clicks and half-loaded pages produce junk steps. Record on a stable environment, slowly.
6. **Recording with real credentials or personal data.** Recorded values are written into the file. Use test accounts and move secrets to environment variables (`Cypress.env`) afterwards.
7. **Leaving redundant steps.** Clicking a field before typing, repeated scrolls, repeated viewport settings: delete them.
8. **Keeping auto-generated test names.** `tests saucedemo-login` says nothing; name tests after behaviour.
9. **Forgetting that Cypress Cloud "record" is something else.** `--record` uploads runs; it does not capture your actions.
10. **Trusting AI suggestions blindly.** Review each generated assertion: does it check something that *matters*, or just something that happened to change?
11. **Committing without re-running.** Run the refined test several times (and in headless mode) before committing.
12. **Overusing recording for complex logic.** Conditional flows, loops and data-driven tests are better written by hand.

---

## Mini Practice Exercises

### Exercise 1: Identify your version and path

Run `npx cypress --version`. Write down: (a) your version, (b) whether you need `experimentalStudio: true`, (c) which Studio entry point you see in the runner.

*Hint:* versions 10.7 to 14 need the flag; the docs for 15.4.0 and later state it was removed.

### Exercise 2: Record with Studio

Record the flow: log in, add two products, open the cart. Add at least two assertions by right-click (badge text equals `2`, cart page contains both product names). Save and read the generated code. Which lines would you change, and why?

*Hint:* look for redundant `clear()` or `click()` calls and missing URL assertions.

### Exercise 3: Record with Chrome Recorder

Record the same flow in Chrome Recorder with the *Selector attribute* set to `data-test`. Export JSON and convert it with `npx @cypress/chrome-recorder`. Compare the selectors with those produced by Studio.

*Solution (typical outcome):* both prefer `[data-test="..."]` selectors on this site. The Recorder output may include an initial `cy.viewport` and extra `click` steps before `type`; Studio output may include `clear()`.

### Exercise 4: Selector priority

Pretend your app uses `data-qa` attributes. Modify `Cypress.SelectorPlayground.defaults` so that `data-qa` is the first priority. Test it with the Selector Playground on a page that has `data-qa` attributes (or temporarily add one in DevTools).

*Solution:*

```js
Cypress.SelectorPlayground.defaults({
  selectorPriority: ['data-qa', 'data-test', 'id', 'class', 'tag'],
});
```

### Exercise 5: Spot the weaknesses

Given this recorded code, list at least five weaknesses:

```js
it('tests flow', () => {
  cy.viewport(1500, 800);
  cy.visit('https://www.saucedemo.com/');
  cy.get('div:nth-child(1) > .form_group > input').click();
  cy.get('div:nth-child(1) > .form_group > input').type('standard_user');
  cy.get('#password').type('secret_sauce');
  cy.get('#login-button').click();
  cy.get('.inventory_item:nth-child(1) button').click();
});
```

*Solution:* (1) vague test name; (2) hard-coded URL instead of `baseUrl`; (3) hard-coded credentials; (4) fragile `nth-child` selectors; (5) no assertions anywhere; (6) redundant clicks before typing; (7) hard-coded viewport; (8) no check that login succeeded before adding a product; (9) mixing different selector styles (`#id`, classes, structure).

---

## Summary / Key Takeaways

- **Recording** generates test code from your actions. It is excellent for drafts and discovery, poor as a finished product.
- **Cypress Studio** was experimental from Cypress 6.3, removed in 10.0, reintroduced in 10.7 behind `experimentalStudio: true`, and per the official experiments reference the flag was removed in **15.4.0**. The current docs call it **Beta**. It is E2E only, needs sourcemaps and internet, records `click`, `type`, `check`, `uncheck` and `select`, and does not support multiple origins, iframes or Shadow DOM.
- **Studio AI** (Cypress 15.11.0 or later) suggests assertions and needs a Cypress Cloud account; review everything it proposes.
- **Chrome DevTools Recorder** records flows in Chrome (101+), exports JSON, and can be converted to Cypress with the **`@cypress/chrome-recorder`** CLI or the Cypress Chrome Recorder extension.
- **Cypress Cloud** records *test runs* (`--record`), not user actions; its link to recording is the AI-assisted Studio feature and Test Replay for debugging.
- Use `Cypress.SelectorPlayground.defaults` and the Recorder's *Selector attribute* to get stable selectors.
- Always follow **record, review, refine**, which is the subject of the next lesson.

---

## External Resources

- Cypress documentation, Cypress Studio (the version history of `experimentalStudio` is in the Experiments reference at https://docs.cypress.io/app/references/experiments): https://docs.cypress.io/app/guides/cypress-studio
- Google Chrome DevTools documentation, Recorder: https://developer.chrome.com/docs/devtools/recorder
- Cypress Chrome Recorder (open-source exporter, README with CLI usage): https://github.com/cypress-io/cypress-chrome-recorder
