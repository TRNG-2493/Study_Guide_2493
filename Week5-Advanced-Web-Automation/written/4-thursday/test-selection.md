# Test Selection in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why teams need to run *subsets* of their test suite (smoke, regression, a single feature, a single failing test) and the cost of always running everything.
- Select tests inside a file with `it.only`, `describe.only`, `it.skip`, `describe.skip`, and conditional skipping with `this.skip()`.
- Select spec files from the command line with `--spec`, including globs, folders, and comma-separated lists.
- Configure which files Cypress treats as specs using `specPattern` and `excludeSpecPattern`, and organise folders so selection is natural.
- Use the Cypress Test Runner UI to run one spec or one test.
- Install and configure the official **`@cypress/grep`** package to select tests by **title** and by **tag** (for example `@smoke`, `@regression`).
- Combine tags with AND/OR/NOT logic, run only untagged tests, and "burn" a flaky test many times to prove it is stable.
- Design a tagging strategy and CI commands for pull-request, nightly, and release runs.
- Compare Cypress's approach with pytest markers and `-k` expressions used with Playwright (Python) earlier in the week.

---

## Why This Matters

A new project with ten tests can be run in seconds. A mature product might have 1,500 end-to-end tests that take 90 minutes. Nobody wants to wait 90 minutes to find out whether a one-line fix worked. Professional teams therefore *select* tests to match the situation:

| Situation | What to run | Why |
|---|---|---|
| You are writing a new test | Just that test | Fast feedback |
| You are debugging a failure | The one failing test, repeatedly | Isolate cause |
| A developer opens a pull request | Smoke tests plus tests for the changed area | Fast gate, 5-10 min |
| Nightly build | The full regression suite | Thorough |
| Pre-release | Full suite on several browsers | Confidence |
| Hunting flakiness | One test, 50 times | Statistical evidence |

This is the same idea you used in Playwright with pytest, where you chose tests with file paths, `-k "login"` expressions, and markers (`@pytest.mark.smoke`, then `pytest -m smoke`). Cypress does not include marker-style tags in its core, so it uses a combination of Mocha's `.only`/`.skip`, command-line `--spec`, and an official plugin, `@cypress/grep`.

Tie this to the Week 5 epic and Project 1: your Thursday exercise asks you to port three Project 1 tests into Cypress. In a real CI pipeline those three tests would be tagged (`@smoke`) so they can run on every commit. Being able to design a selection strategy is part of building a test *framework*, not just a pile of tests.

---

## The Concept

### 1. The selection toolbox at a glance

| Level | Tool | Example |
|---|---|---|
| Inside a file | `.only`, `.skip`, `this.skip()`, per-test `browser` option | `it.only('...', ...)` |
| File level (CLI) | `--spec` | `cypress run --spec "cypress/e2e/cart/*.cy.js"` |
| File level (config) | `specPattern`, `excludeSpecPattern` | `specPattern: 'cypress/e2e/**/*.cy.js'` |
| Interactive | Spec list and "Run" in the Test Runner; filter box | `cypress open` |
| Test level by name/tag | `@cypress/grep` | `--env grepTags=@smoke` |
| Environment | `Cypress.env()`, `Cypress.browser` conditions | `it('...', { browser: 'chrome' }, ...)` |

### 2. Selecting inside a spec file: `.only` and `.skip`

#### 2.1 `.only`

```js
describe('Cart', () => {
  it('adds an item', () => { /* ... */ });

  it.only('removes an item', () => { /* ... */ });   // only this runs in the file

  it('clears the cart', () => { /* ... */ });
});
```

- Mocha sees `.only` and runs just that test in the spec file.
- Other tests in the same file are **not run and not listed as skipped**; they simply do not execute. In `cypress run`, the summary may show them as pending/skipped depending on the version.
- You can apply `.only` to a `describe`, which runs every test inside that suite: `describe.only('Cart', () => {...})`.
- If multiple `.only` appear in a file, *all of them* run (and nothing else).
- `.only` affects only the file where it appears, not other specs.

This is a **development convenience**. It is the quickest way to focus on one test while writing it. The danger is that `.only` stays in the code when committed, silently disabling the other tests in the file. Safeguards: ESLint rule `mocha/no-exclusive-tests`; code review; a CI grep for `.only(`.

#### 2.2 `.skip`

```js
it.skip('applies a gift card (feature in progress)', () => { /* ... */ });

describe.skip('Legacy checkout', () => {
  it('works with the old payment form', () => { /* ... */ });
});
```

- A skipped test is reported as **pending**: it appears in output as skipped, not as passing or failing. This is honest reporting: the team can see what is not being verified.
- Always add a comment or ticket number explaining *why* a test is skipped, and when it should be revived: `// TODO QE-142: unskip after payment API fix`.
- A skipped test is a debt. Review them regularly.

#### 2.3 Conditional skipping

Skip based on runtime conditions (browser, environment variable, feature flag):

```js
it('uses the clipboard API', function () {
  if (Cypress.browser.name === 'firefox') {
    this.skip();            // Mocha marks this test as pending and stops
  }
  // test body
});
```

- You must use a `function () {}` callback because `this` refers to the Mocha context.
- Declarative alternative with test configuration (no `this`):

```js
it('uses the clipboard API', { browser: '!firefox' }, () => { /* ... */ });
```

- Environment-based:

```js
const isProd = Cypress.env('ENV') === 'prod';
(isProd ? it.skip : it)('creates test data via the admin API', () => { /* ... */ });
```

Line by line: `Cypress.env('ENV')` reads an environment value passed with `--env ENV=prod`. The ternary expression `(cond ? it.skip : it)` chooses which function to call to register the test; because describe/it registration is plain synchronous JavaScript, this works.

### 3. Selecting spec files from the command line: `--spec`

```bash
npx cypress run --spec "cypress/e2e/login.cy.js"
npx cypress run --spec "cypress/e2e/cart/**/*.cy.js"
npx cypress run --spec "cypress/e2e/login.cy.js,cypress/e2e/checkout.cy.js"
npx cypress run --spec "cypress/e2e/**/smoke*.cy.js"
```

Rules:

1. The value is a **glob pattern** (wildcards): `*` matches within a folder name segment; `**` matches any number of nested folders.
2. Always wrap globs in **quotes**, otherwise your shell expands `*` before Cypress sees it (and on Windows PowerShell/CMD the behaviour differs).
3. Multiple specs are separated by a **comma** inside one quoted string.
4. `--spec` works with `cypress run`. With `cypress open` you pick a spec in the UI, or open directly with `cypress open --e2e --browser chrome` and click.

#### 3.1 Using folders as selection groups

A folder structure that makes `--spec` meaningful:

```
cypress/e2e/
  smoke/
    login.cy.js
    checkout.cy.js
  regression/
    cart/
      cart-add.cy.js
      cart-remove.cy.js
    search/
      search-filters.cy.js
  api/
    posts.cy.js
```

Commands:

```bash
npx cypress run --spec "cypress/e2e/smoke/**"
npx cypress run --spec "cypress/e2e/regression/cart/**"
npx cypress run --spec "cypress/e2e/api/**"
```

This approach is simple, transparent, and requires no plugin. Its weakness: a test can live in only one folder, so "all smoke tests" that span features need duplicates or cross-cutting folders. That is the problem tags solve.

#### 3.2 Specs in `package.json` scripts

```json
{
  "scripts": {
    "cy:smoke": "cypress run --spec \"cypress/e2e/smoke/**\"",
    "cy:cart": "cypress run --spec \"cypress/e2e/regression/cart/**\"",
    "cy:all": "cypress run"
  }
}
```

The backslash-escaped quotes `\"` are needed because JSON strings use double quotes themselves.

### 4. Configuring which files are specs

In `cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    excludeSpecPattern: ['**/__snapshots__/*', '**/helpers/*', '**/*.skip.cy.js'],
  },
});
```

- `specPattern` - glob(s) selecting spec files (default `cypress/e2e/**/*.cy.{js,jsx,ts,tsx}`).
- `excludeSpecPattern` - glob(s) that are **never** treated as specs. Useful for helper files you want to keep next to specs.

You can also override on the command line without editing the file:

```bash
npx cypress run --config specPattern="cypress/e2e/smoke/**/*.cy.js"
```

`--config` accepts `key=value` pairs for most configuration options.

Multiple config files per environment:

```bash
npx cypress run --config-file cypress.staging.config.js
```

### 5. Selecting in the interactive runner

In `cypress open`:

1. After choosing E2E and a browser, you see the **Specs** list.
2. Click a spec file to run it. Use the **search box** to filter by file name.
3. Within a running spec, the Command Log lists tests by suite; each test header has a **play button** ("Run this test only", available in recent versions) and a re-run button for the whole spec.
4. `.only` is also honoured here.

This is the day-to-day development workflow: open a spec, edit, save, watch it re-run.

### 6. Selecting by title and tag with `@cypress/grep`

#### 6.1 What it is

`@cypress/grep` is an **official plugin from the Cypress team** (formerly the community package `cypress-grep`). It lets you:

- Run only tests whose **title** contains a string or matches a pattern.
- Run only tests whose **tags** match an expression.
- Run only untagged tests.
- **Burn** a test: repeat it N times to expose flakiness.
- Skip *spec files* entirely when none of their tests match (a big speedup).

This is the Cypress parallel of pytest `-m` (markers) and `-k` (name expression).

#### 6.2 Installation

```bash
npm install --save-dev @cypress/grep
```

Register it in two places.

**1. Support file** (browser side), `cypress/support/e2e.js`:

```js
const { registerCypressGrep } = require('@cypress/grep');
registerCypressGrep();
```

(If you use ES modules: `import registerCypressGrep from '@cypress/grep'; registerCypressGrep();` per the plugin's README for your version.)

**2. Config file** (Node side), `cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    env: {
      grepFilterSpecs: true,
      grepOmitFiltered: true,
    },
    setupNodeEvents(on, config) {
      require('@cypress/grep/src/plugin')(config);
      return config;
    },
  },
});
```

**Line by line:**

1. `registerCypressGrep()` hooks into Mocha in the browser and filters tests at load time based on the configured values.
2. `env: { grepFilterSpecs: true }` makes Cypress **filter out spec files** that contain no matching tests, so they never even open. Without it, every spec is loaded and individual tests are skipped.
3. `grepOmitFiltered: true` removes unmatched tests from the report instead of showing them as pending.
4. `require('@cypress/grep/src/plugin')(config)` is the Node-side plugin that implements the spec filtering. It **must** return `config` afterwards (the last line of `setupNodeEvents`).

Check the package README for the exact import path of your installed version, as the maintainers occasionally adjust it.

#### 6.3 Adding tags to tests

Tags are provided in the **test configuration object**, as the second argument of `it` or `describe`:

```js
describe('Login', { tags: '@auth' }, () => {
  it('logs in with valid credentials', { tags: ['@smoke', '@critical'] }, () => {
    /* ... */
  });

  it('rejects a wrong password', { tags: '@regression' }, () => {
    /* ... */
  });

  it('remembers the user', () => {
    /* untagged */
  });
});
```

- `tags: '@smoke'` - a single tag as a string.
- `tags: ['@smoke', '@critical']` - an array for multiple tags.
- Tags on a `describe` are **inherited** by every test inside it. So every test in 'Login' also has `@auth`.
- The `@` prefix is a convention, not a requirement; you can write `smoke`. Be consistent.

A second style, for people who like putting tags in the title (no config object needed):

```js
it('logs in successfully @smoke', () => { /* ... */ });
```

With `grep=@smoke` the title match picks it up. Tags in the config object are cleaner and survive title rewording.

#### 6.4 Running by tag

Pass values through Cypress env variables with `--env`:

```bash
# one tag
npx cypress run --env grepTags=@smoke

# OR: tests tagged @smoke or @critical (space = OR)
npx cypress run --env grepTags="@smoke @critical"

# AND: tests tagged both @smoke and @fast (plus = AND)
npx cypress run --env grepTags=@smoke+@fast

# NOT: smoke tests that are not slow (dash = NOT)
npx cypress run --env grepTags=@smoke+-@slow

# Everything except @slow
npx cypress run --env grepTags=-@slow
```

Symbols to memorise:

| Symbol | Meaning | Example |
|---|---|---|
| space | OR | `"@smoke @critical"` |
| `+` | AND | `@smoke+@fast` |
| `-` | NOT | `-@slow` |

When you pass several env values, separate by commas:

```bash
npx cypress run --env grepTags=@smoke,grep=login
```

(Quote the whole `--env` value on your shell if it contains spaces.) You can also set them as OS environment variables: `CYPRESS_grepTags=@smoke npx cypress run` (Linux/macOS) or `$env:CYPRESS_grepTags="@smoke"; npx cypress run` (PowerShell).

#### 6.5 Running by title

```bash
npx cypress run --env grep="login"             # tests whose title contains "login"
npx cypress run --env grep="login success"     # contains that phrase
npx cypress run --env grep="-slow"             # titles NOT containing "slow"
npx cypress run --env grep="login; checkout"   # OR with semicolon-separated phrases (check README)
```

Title grepping is handy for a quick one-off run: "run everything about coupons."

#### 6.6 Combine title and tags

```bash
npx cypress run --env grep="checkout",grepTags=@smoke
```

Both conditions must match (the plugin ANDs the two filters).

#### 6.7 Run only untagged tests

```bash
npx cypress run --env grepUntagged=true
```

Helps you find tests that nobody has categorised.

#### 6.8 Burn: repeat to detect flakiness

```bash
npx cypress run --env grep="adds an item",burn=20
```

`burn=20` repeats each matching test 20 times. If one repetition fails, you have evidence of flakiness and the failure report shows which run failed. This is the Cypress counterpart to Playwright's `--repeat-each` flag.

#### 6.9 In the interactive runner

You can also set grep values in the browser's console or via the config `env` while using `cypress open`:

```bash
npx cypress open --env grepTags=@smoke
```

#### 6.10 Where grep applies

The plugin filters at test registration time. When `grepFilterSpecs` is on, a spec file that contains no matching test is not run at all. Without `grepFilterSpecs`, Cypress still loads each spec file and visits `about:blank`, adding overhead.

### 7. Designing a tagging strategy

A good tag set is **small, documented, and meaningful**. Typical tags:

| Tag | Meaning | Where it runs |
|---|---|---|
| `@smoke` | Few critical-path tests (login, checkout, search) | Every pull request, every deployment |
| `@regression` | Full functional coverage | Nightly |
| `@critical` | Business-critical flows | Pre-release gate |
| `@slow` | Tests over ~1 minute | Nightly only (`-@slow` on PRs) |
| `@wip` | Work in progress | Never in CI (`-@wip`) |
| `@flaky` | Known unstable, quarantined | Separate non-blocking job |
| `@api`, `@ui` | Layer | Separate pipelines |
| `@mobile` | Mobile viewport tests | Specific job |

Guidelines:

1. Keep to 5-8 tags. Tag sprawl makes selection confusing.
2. Document them in the README (one table).
3. Review `@flaky` regularly; quarantine is not a solution.
4. A test can have several tags; avoid tag-based logic so complex that it is hard to explain.
5. Combine folders for *ownership* (`cypress/e2e/cart`) and tags for *purpose* (`@smoke`).

### 8. Example CI strategy

```json
{
  "scripts": {
    "test:pr": "cypress run --browser chrome --env grepTags=@smoke+-@wip",
    "test:nightly": "cypress run --browser chrome --env grepTags=-@wip",
    "test:release": "cypress run --env grepTags=\"@regression @critical\"",
    "test:burn": "cypress run --env grep=\"$GREP\",burn=25"
  }
}
```

Explanation: on every PR run the smoke tests that are not work in progress. Nightly runs everything except WIP. A release run executes regression and critical tests (you would add each browser via a CI matrix). The burn script reads the title from an environment variable `GREP` so engineers can type `GREP="adds an item" npm run test:burn`. (Windows shells differ in variable syntax; in a cross-platform repo use the `cross-env` package or pass arguments with `-- --env ...`.)

Pass extra arguments through npm with `--`: `npm run cy:run -- --env grepTags=@smoke`.

### 9. Related selection mechanisms you will hear about

- **Parallelisation and spec balancing** across machines: offered by Cypress Cloud (`cypress run --record --parallel`) or open-source alternatives. This is about *distributing* tests, not selecting them.
- **Retries** (test retries via `retries` config) cover flaky failures but are not selection; you configured them in the first lesson.
- **Spec ordering**: Cypress runs spec files in alphabetical order unless parallelised; tests inside a file run in the order written. Never depend on order.
- **Playwright comparison:** `pytest -m smoke` / `-k "login and not slow"` / `pytest tests/cart/` correspond to `grepTags`, `grep`, and `--spec`. Playwright's native TypeScript test runner also has `--grep` and `@tag` support, as well as `--repeat-each`.

---

## Code Examples

### Example 1: Smoke and regression tags

```js
describe('Sauce Demo - authentication', { tags: '@auth' }, () => {
  beforeEach(() => cy.visit('/'));

  it('logs in with a valid user', { tags: '@smoke' }, () => {
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  });

  it('blocks a locked-out user', { tags: '@regression' }, () => {
    cy.get('[data-test="username"]').type('locked_out_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.get('[data-test="error"]').should('contain.text', 'locked out');
  });

  it('shows required-field error', { tags: ['@regression', '@validation'] }, () => {
    cy.get('[data-test="login-button"]').click();
    cy.get('[data-test="error"]').should('contain.text', 'Username is required');
  });
});
```

**Explanation:**

- The `describe`'s `{ tags: '@auth' }` is inherited by all three tests.
- Test 1 has `@smoke`; running `--env grepTags=@smoke` runs only it.
- Test 3 has an array of two tags; `--env grepTags=@validation` selects it.
- `--env grepTags=@auth+-@smoke` runs tests 2 and 3 (authentication tests that are not smoke).

### Example 2: Commands cheat sheet

```bash
# One file
npx cypress run --spec "cypress/e2e/auth/login.cy.js"

# A folder
npx cypress run --spec "cypress/e2e/smoke/**"

# Two files
npx cypress run --spec "cypress/e2e/auth/login.cy.js,cypress/e2e/cart/cart.cy.js"

# Smoke in Firefox, headed
npx cypress run --browser firefox --headed --env grepTags=@smoke

# Everything but slow tests
npx cypress run --env grepTags=-@slow

# Burn one test 30 times
npx cypress run --spec "cypress/e2e/cart/cart.cy.js" --env grep="adds two items",burn=30
```

### Example 3: Quarantining flaky tests

```js
it('applies a discount code', { tags: '@flaky' }, () => {
  // known intermittent failure, tracked in ticket QE-311
});
```

PR pipeline: `--env grepTags=-@flaky`. A separate non-blocking nightly job: `--env grepTags=@flaky,burn=10` to gather statistics until fixed.

### Example 4: Guarding against `.only`

ESLint configuration fragment:

```json
{
  "plugins": ["mocha"],
  "rules": {
    "mocha/no-exclusive-tests": "error",
    "mocha/no-skipped-tests": "warn"
  }
}
```

**Explanation:** `eslint-plugin-mocha` understands `describe/it`. `no-exclusive-tests` errors on `.only` so linting fails before merge; `no-skipped-tests` warns on `.skip` so debt is visible.

### Example 5: The same selection in pytest for comparison

```bash
pytest -m smoke                       # run tests marked @pytest.mark.smoke
pytest -k "login and not locked"      # name expression
pytest tests/cart/                    # a folder
pytest tests/test_login.py::test_valid_login  # one test
pytest --count 20 -k "test_add"       # repeat with pytest-repeat plugin
```

Mapping: `-m smoke` -> `grepTags=@smoke`; `-k` -> `grep=`; folder -> `--spec`; repeated runs -> `burn`.

---

## Real-World Scenarios

1. **Fast PR gates.** A team's 400-test suite takes 45 minutes. They tag 30 critical tests `@smoke` and run them on every PR in 4 minutes with `grepTags=@smoke`; the full suite runs nightly. Developers get feedback quickly and still have broad coverage.
2. **Release regression across browsers.** Before a release, a matrix job runs `@regression` tests on Chrome, Firefox, and Edge in parallel, with the `--browser` flag from the first two lessons.
3. **Proving a fix for a flaky test.** A test failed in about 1 in 20 runs. After a fix, the engineer runs `--env grep="applies a discount code",burn=50`; 50 passes give confidence, 1 failure shows more work is needed.
4. **Feature-flagged functionality.** A new payment method is behind a feature flag that is on in staging only. Tests are tagged `@new-payments` and the staging pipeline includes them; production smoke excludes them.
5. **Onboarding trainees.** The training repository has `cypress/e2e/exercises/` and `cypress/e2e/solutions/`. Trainees run only `--spec "cypress/e2e/exercises/**"`. Folder-based selection avoids a plugin for a simple need.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Committing `.only`.** Add ESLint and CI checks.

**Pitfall 2: Unquoted globs.** `--spec cypress/e2e/**/*.cy.js` may be expanded by your shell into a list that Cypress does not expect. Always quote.

**Pitfall 3: Forgetting to return `config` from `setupNodeEvents`.** The grep plugin needs it; tests then run unfiltered.

**Pitfall 4: Registering the plugin only on one side.** Both `registerCypressGrep()` (support file) and the plugin in `setupNodeEvents` are needed for `grepFilterSpecs`.

**Pitfall 5: Tag typos.** `@smok` selects nothing and the run "passes" with zero tests. Add a CI step that fails when the total test count is zero, or define tag constants in a shared file:

```js
// cypress/support/tags.js
module.exports = { SMOKE: '@smoke', REGRESSION: '@regression', SLOW: '@slow' };
```

```js
const { SMOKE } = require('../support/tags');
it('logs in', { tags: SMOKE }, () => {});
```

**Pitfall 6: Skipped tests forgotten forever.** Track with a ticket number in the comment and review monthly.

**Pitfall 7: Using test order dependencies with selection.** If test B depends on test A having run, selecting only B will fail. Tests must be independent.

**Pitfall 8: Overusing retries instead of fixing flakiness.** Retries and tags like `@flaky` are temporary measures, not strategy.

**Best practices**

- Use folders for feature ownership and tags for cross-cutting purpose.
- Keep a small, documented tag vocabulary.
- Prefer `--spec` for quick local runs, tags for CI strategy.
- Fail CI if zero tests ran.
- Lint for `.only`.
- Keep selection commands as named npm scripts.

---

## Mini Practice Exercises

**Exercise 1 - `.only` and `.skip`.**
Create a spec with four tests. Use `.only` on one, run it, then switch to `.skip` on another and run again. Observe how the runner reports each.

**Exercise 2 - `--spec`.**
Create two folders, `cypress/e2e/smoke` and `cypress/e2e/regression`, each with one spec. Write the two commands to run (a) just smoke and (b) both specs by listing them.

*Solution:*

```bash
npx cypress run --spec "cypress/e2e/smoke/**"
npx cypress run --spec "cypress/e2e/smoke/**,cypress/e2e/regression/**"
```

**Exercise 3 - Tags.**
Install `@cypress/grep` and register it. Tag three tests: one `@smoke`, one `@regression`, one both. Predict how many tests each command runs, then verify:

a) `--env grepTags=@smoke`
b) `--env grepTags=@smoke+@regression`
c) `--env grepTags=-@smoke`
d) `--env grepTags="@smoke @regression"`

*Answer:* a) 2; b) 1; c) 1 (the only test without smoke); d) 3.

**Exercise 4 - Burn.**
Pick any passing test, run it with `burn=10`, and note the result. Deliberately introduce randomness (for example `expect(Math.random()).to.be.greaterThan(0.1)`) and burn again to see a failure caught.

**Exercise 5 - Plan.**
Write a table (tag, purpose, when it runs) for your Project 1 test suite. Choose 4-6 tags and write the exact `npm` scripts for PR, nightly, and release.

**Exercise 6 - Conditional.**
Write a test that is skipped when `Cypress.env('ENV') === 'prod'`. Run it twice, with and without `--env ENV=prod`.

**Exercise 7 - Compare.**
For each of the three pytest commands in Example 5, write the nearest Cypress command. Add a sentence in your comparison note about which approach you find easier to maintain.

---

## Summary / Key Takeaways

- Teams need to run subsets of tests for speed, focus, and strategy: smoke on PRs, regression nightly, burn to find flakiness.
- Inside a file: `.only` focuses; `.skip` disables (and reports pending); `this.skip()` and `{ browser: ... }` skip conditionally. Never commit `.only`; lint for it.
- From the command line: `--spec` selects files by glob (quote it; comma-separate multiple); `specPattern` and `excludeSpecPattern` define what counts as a spec; `--config` and `--config-file` change configuration per run.
- Organise folders for ownership; use tags for purpose.
- `@cypress/grep` provides `grep` (title), `grepTags` (tags with space = OR, `+` = AND, `-` = NOT), `grepUntagged`, and `burn` repeats; enable `grepFilterSpecs` for speed.
- Tests must be independent for selection to work.
- Selection maps to pytest's `-k`, `-m`, paths, and repeat plugins from your Playwright (Python) work.
- Debugging and evidence for failed selected tests (time travel, screenshots, video) is **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - Command Line (`--spec`, `--env`, `--config`): https://docs.cypress.io/app/references/command-line
- Cypress Documentation - Writing and Organizing Tests (`.only`, `.skip`, spec patterns): https://docs.cypress.io/app/core-concepts/writing-and-organizing-tests
- `@cypress/grep` (official package README): https://github.com/cypress-io/cypress/tree/develop/npm/grep
