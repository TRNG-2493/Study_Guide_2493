# Automated Accessibility Scanning

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what automated accessibility scanning can and cannot catch, and why it is a supplement to manual testing rather than a replacement.
- Describe how **axe-core** works: rules, impact levels, and the four result buckets (`violations`, `passes`, `incomplete`, `inapplicable`).
- Read the result JSON and interpret one violation: `id`, `impact`, `help`, `helpUrl`, `nodes`, `target`, `failureSummary`.
- Run a quick scan with the axe browser extension and with the Lighthouse accessibility audit, and explain what the Lighthouse score means.
- Run axe from Python with `axe-playwright-python` (`Axe().run(page)`, `violations_count`, `generate_report`), choosing WCAG tags and include/exclude contexts.
- Build a PyTest fixture and a parametrized multi-page scan test.
- Choose between "zero violations", baselines, and known-issue allowlists.
- Scan dynamic states (an open modal, a logged-in page) and triage `incomplete` items and false positives.
- Report results and combine scanning with manual testing.

---

## Why This Matters

This is the Week 7 accessibility epic coming together. Earlier this week you learned the principles behind accessible design, then practised the manual techniques: keyboard-only navigation and screen-reader checks. Those techniques are essential, but they are slow. Nobody can tab through every page of a 200-page application on every commit.

Automated scanning fills that gap. A scan runs in a few seconds, checks hundreds of machine-checkable rules, and does it identically every time. Think of it as a **smoke alarm**: it cannot tell you the building is safe, but it reliably shouts when one well-known kind of danger appears. A missing form label, a low-contrast button, or an invalid ARIA attribute is exactly the kind of defect a developer introduces by accident on a Tuesday afternoon, and a scan catches it before a user with a screen reader ever meets it.

For a QEA, scanning gives three things: **speed** (instant feedback), **coverage** (every page in a list), and **regression protection** (a fixed defect stays fixed). In your Python and Playwright framework it is just another test, so everything you already know about fixtures and parametrization applies. Tomorrow's lesson covers running these scans inside a CI pipeline; today you build the tests themselves.

---

## The Concept

### 1. What Automation Can and Cannot Catch

An automated scanner loads the **rendered page** (after JavaScript has run), walks the DOM and the accessibility tree, and applies a library of rules. Each rule asks a question that a computer can answer definitively.

**What automation catches well (objective, mechanical checks):**

| Defect | Example rule |
|--------|-------------|
| Missing text alternative | `image-alt`: an `<img>` has no `alt` |
| Missing form label | `label`: an `<input>` has no associated label or accessible name |
| Buttons and links with no name | `button-name`, `link-name` |
| Low colour contrast (plain backgrounds) | `color-contrast` |
| Invalid or misused ARIA | `aria-valid-attr`, `aria-roles` |
| Missing page language | `html-has-lang` |
| Duplicate IDs referenced by ARIA | `duplicate-id-aria` |
| Missing or empty page title | `document-title` |

**What automation cannot catch (needs human judgement):**

- Whether alt text is **meaningful**. `alt="image1"` passes `image-alt` and is completely useless.
- Whether the **reading and focus order** makes sense.
- Whether error messages are **understandable** and tell people how to recover.
- Whether a custom widget is actually **usable** with a keyboard or screen reader.
- Whether captions are accurate, or whether content is written in plain language.

A commonly quoted industry figure is that automated tools find somewhere around **a third to a half** of WCAG issues, depending on how you count. Do not memorise a precise number; remember the shape of the claim: *a clean scan means "no machine-detectable failures", not "accessible".*

**Real-world scenario.** A team ships a checkout page with a perfect scan. A blind customer cannot complete the purchase because the "Pay now" button is an unlabelled `<div>` with a click handler, and, once it was fixed to be a button, the focus jumped to the top of the page after payment. The first problem a scan would have caught (`button-name`, or a missing role); the second is a focus-management problem only keyboard and screen-reader testing, from earlier this week, will reveal. Both kinds of testing are needed.

### 2. axe-core: The Engine

**axe-core** is an open-source JavaScript library from Deque. It is the engine behind the axe browser extension, behind Lighthouse's accessibility audits, and behind many test-framework integrations, including the Python one we use today. Learning axe's vocabulary therefore pays off across the whole tool landscape.

#### Rules

axe is a collection of **rules**. Each rule has an `id` (like `color-contrast`), a description, tags that map it to a standard, and an impact level. A rule examines specific elements ("every `<img>`") and returns a verdict per element.

#### Rule tags

Tags say which standard a rule belongs to. The ones you will use most:

| Tag | Meaning |
|-----|---------|
| `wcag2a` | WCAG 2.0 level A |
| `wcag2aa` | WCAG 2.0 level AA |
| `wcag21a`, `wcag21aa` | WCAG 2.1 additions at A and AA |
| `wcag22aa` | WCAG 2.2 additions at AA |
| `best-practice` | Not a WCAG failure, but recommended (for example `region`, `landmark-one-main`) |
| `cat.*` | Category tags such as `cat.color` or `cat.forms` |

Criterion tags such as `wcag143` mean success criterion 1.4.3 (Contrast Minimum).

#### Impact levels

Every violation has an **impact**, an estimate of how badly it hurts users:

| Impact | Meaning (roughly) |
|--------|-------------------|
| `critical` | Blocks some users completely (for example a button with no accessible name) |
| `serious` | Causes major difficulty (for example insufficient contrast on body text) |
| `moderate` | Causes some difficulty |
| `minor` | Annoying but low impact |

Impact is axe's general estimate of a rule's effect, not a measurement of your specific page. Use it for **prioritising**, not as the last word.

#### The four result buckets

Every axe run sorts its findings into four lists:

| Bucket | Meaning | What you do |
|--------|---------|-------------|
| `violations` | A rule **definitely failed** on one or more elements | These are your defects |
| `passes` | A rule ran and the elements passed | Proof of what was checked |
| `incomplete` | axe **could not decide** (for example text over a background image) | A human must review |
| `inapplicable` | The rule had nothing to check (no `<video>`, so no video rules) | Ignore; it is just coverage information |

The `incomplete` bucket is the heart of axe's philosophy: it would rather say "I don't know" than raise a false alarm. This is why teams trust axe's violations.

#### Result JSON shape (simplified)

```json
{
  "url": "https://example.com/login",
  "timestamp": "2026-10-11T10:15:00.000Z",
  "testEngine": { "name": "axe-core", "version": "4.10.0" },
  "violations": [ { "id": "...", "impact": "...", "nodes": [ ] } ],
  "passes": [ ],
  "incomplete": [ ],
  "inapplicable": [ ]
}
```

Line by line: `url` and `timestamp` record what was scanned and when (useful in saved reports); `testEngine` records the axe version, which matters because newer versions add rules and a baseline from an old version may not match; the four arrays are the buckets above. Each array contains **rule objects**, and each rule object contains a `nodes` list, one entry per offending element.

### 3. Interpreting a Single Violation

Here is a violation object, shortened. This is **representative output** from a scan of a login page with a pale grey hint text:

```json
{
  "id": "color-contrast",
  "impact": "serious",
  "tags": ["cat.color", "wcag2aa", "wcag143"],
  "description": "Ensure the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds",
  "help": "Elements must meet minimum color contrast ratio thresholds",
  "helpUrl": "https://dequeuniversity.com/rules/axe/4.10/color-contrast",
  "nodes": [
    {
      "html": "<p class=\"hint\">Optional</p>",
      "target": [".hint"],
      "failureSummary": "Fix any of the following:\n  Element has insufficient color contrast of 2.85 (foreground color: #999999, background color: #ffffff, font size: 12.0pt, font weight: normal). Expected contrast ratio of 4.5:1"
    }
  ]
}
```

Reading it field by field:

- `id`: the rule name. This is what you search for, put in a bug title, and use in a baseline.
- `impact`: `serious`, so this should be fixed soon and is a sensible reason to fail a build.
- `tags`: it is a WCAG 2.x AA rule (`wcag2aa`), criterion 1.4.3 (`wcag143`). This tells you which conformance level it affects.
- `description`: what the rule checks, in standards language.
- `help`: a one-line, human-friendly statement of the problem. Good for a bug title.
- `helpUrl`: a Deque University page explaining the rule, why it matters, and how to fix it. Paste it into the bug report.
- `nodes`: the list of elements that failed. One rule can fail on many elements, so **the number of violations is the number of rules failed, not the number of broken elements**.
- `nodes[].html`: the element's markup, so a developer sees what was found.
- `nodes[].target`: a CSS selector that locates the element. Usually a list with one string; for elements inside an iframe or shadow DOM it is a list of selectors, one per level.
- `nodes[].failureSummary`: the precise reason, including measured values (2.85 found, 4.5 required). This is the most useful sentence in the whole object.

**Common mistake:** counting `len(violations)` and calling it "the number of bugs". A single `color-contrast` violation might hide forty failing elements. Always report both rule count and element count.

### 4. Using the axe Browser Extension

The axe DevTools extension (Chrome, Edge, Firefox) is the fastest way to explore a page by hand.

1. Install **axe DevTools** from your browser's extension store.
2. Open the page you want to test, press `F12`, and open the **axe DevTools** tab.
3. Click the scan button (often labelled "Scan ALL of my page").
4. Read the results panel: issues grouped by rule, each with impact, a description, a highlight button that flashes the element on the page, and fix guidance.
5. Use the **Needs review** (incomplete) section to inspect items axe could not decide.

**When to use it:** exploratory testing, reproducing a failure a script reported, and checking a page *state* you have manually set up (a half-completed form, a tooltip). **When not to use it:** repeated regression checks. A person clicking a button is not a regression suite; that is what the Python scan below is for.

**Common mistake:** scanning only the first state of the page. Open the menu, trigger the error message, then scan again.

### 5. Lighthouse Accessibility Audit

**Lighthouse** is Google's open-source auditing tool, built into Chrome DevTools. Its accessibility category runs a subset of axe-core rules and turns the result into a score.

**In Chrome DevTools:**

1. Open DevTools (`F12`) and choose the **Lighthouse** tab.
2. Tick only **Accessibility**; choose Desktop or Mobile.
3. Click **Analyze page load**.
4. Read the score (0-100), the list of failed audits with the offending elements, a list of **"Additional items to manually check"**, and passed/not-applicable audits.

**From the command line** (requires Node.js):

```bash
npx lighthouse https://example.com --only-categories=accessibility --output=json --output-path=reports/lighthouse.json --chrome-flags="--headless"
```

Line by line: `npx lighthouse <url>` downloads and runs Lighthouse against the URL; `--only-categories=accessibility` skips performance, SEO and the rest, making the run faster; `--output=json` and `--output-path=...` write machine-readable results to a file; `--chrome-flags="--headless"` runs Chrome without a visible window, which is what you need on a server.

#### What the score means

The score is a **weighted average** of the audits that passed: each audit carries a weight reflecting its impact, and an audit is pass/fail, with no partial credit. So a score of 92 means "most weighted audits passed", not "92% accessible".

- A score of **100 does not mean the page is accessible.** It means no automated audit failed.
- A drop from 98 to 84 is a useful *signal* that something regressed.
- The score hides detail; always open the failed audits.

**Lighthouse versus axe in your framework:** Lighthouse is great for a quick look and a headline number. For tests with pass/fail assertions, a configurable scope, and structured results per element, axe in code is the better tool, and that is where the rest of this lesson lives.

### 6. Other Tools: pa11y and WAVE

You may meet these on real projects, so recognise them:

- **pa11y** is a command-line scanner (and `pa11y-ci` for lists of URLs). It can use the HTML CodeSniffer engine or axe. Handy for quick URL-list scanning from a shell script.
- **WAVE** (from WebAIM) is a browser extension that overlays icons directly on the page: red for errors, yellow for alerts, green for features. It is excellent for *seeing* structure and for explaining issues to non-technical stakeholders, but it is not designed for code-based regression tests.

Different engines have different rules and different opinions. A second tool occasionally catches something axe misses, and the overlap between tools is large but not total. We standardise on axe because it has the best Python integration and a conservative false-positive policy.

### 7. axe-playwright-python

`axe-playwright-python` bundles axe-core and gives you a small Python API around a Playwright page.

#### Setup

```bash
pip install pytest-playwright axe-playwright-python
playwright install chromium
```

`pytest-playwright` provides the `page` fixture (a fresh browser tab per test), `axe-playwright-python` provides the `Axe` class, and `playwright install chromium` downloads the browser binary once.

#### A first scan

```python
# tests/accessibility/test_login_a11y.py
from playwright.sync_api import Page
from axe_playwright_python.sync_playwright import Axe


def test_login_page_has_no_axe_violations(page: Page):
    page.goto("https://example.com/login")

    results = Axe().run(page)

    assert results.violations_count == 0, results.generate_report()
```

Line by line:

- `from playwright.sync_api import Page` imports the type only so your editor offers autocomplete; it does not change behaviour.
- `from axe_playwright_python.sync_playwright import Axe` imports the sync version of the helper (there is an async version for async Playwright).
- `def test_...(page: Page)` is a normal PyTest test; `page` is injected by `pytest-playwright`.
- `page.goto(...)` loads the URL in a real browser, so JavaScript runs and the DOM is fully built.
- `Axe().run(page)` injects axe-core into the page, runs it, and returns an `AxeResults` object.
- `results.violations_count` is the number of **failed rules** (not elements).
- `results.generate_report()` returns a readable text report of the violations. Using it as the assertion message means a failure explains itself in the test output.

The raw dictionary (the JSON shape from section 2) is available as `results.response`, which is what you use for custom logic and for saving JSON.

On failure, the message lists each rule, its impact, help URL, and the affected element snippet (representative output; layout varies by library version).

#### Options: choosing tags

By default axe runs most rules, including best-practice ones. To match your project's target (for example WCAG 2.2 AA), pass options:

```python
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]

results = Axe().run(
    page,
    options={"runOnly": {"type": "tag", "values": WCAG_TAGS}},
)
```

Explanation: `options` is passed straight through to axe-core's `run`. `runOnly` with `type: "tag"` means "run only the rules that carry one of these tags". Listing `wcag2a` and `wcag2aa` alongside `wcag21*` and `wcag22aa` matters, because the tags are **not cumulative**: `wcag22aa` contains only the rules *added* in 2.2, so asking for it alone would skip the 2.0 rules.

**Common mistake:** requesting only `["wcag22aa"]` and getting an almost empty result, then believing the page is nearly perfect.

#### Context: include and exclude

A **context** tells axe *where* to look:

```python
results = Axe().run(
    page,
    context={
        "include": [["#checkout-form"]],
        "exclude": [["#third-party-chat"], [".ad-banner"]],
    },
    options={"runOnly": {"type": "tag", "values": WCAG_TAGS}},
)
```

Explanation: `include` limits the scan to the checkout form; `exclude` removes the chat widget and ads from that area. Each selector is wrapped in its own list because axe uses a nested list to express a path through iframes (an outer list item per frame boundary). For ordinary elements in the main document, you write `[["#selector"]]`.

**When to scope:** testing a single component (a modal), or excluding third-party widgets you cannot fix. **Rule of thumb:** every exclusion gets a comment naming the reason and a ticket, because exclusions silently hide real problems over time.

To save evidence, write `json.dumps(results.response, indent=2)` to a file; `results.response` is a plain dictionary. The fixture below does exactly this.

### 8. A PyTest Fixture for Scanning

Copy-pasting the same five lines into every test violates the habit you built on Monday: put shared setup into fixtures. Here is a fixture that wraps scanning, applies your standard tags, and saves a report.

```python
# tests/accessibility/conftest.py
import json
from pathlib import Path

import pytest
from axe_playwright_python.sync_playwright import Axe

REPORT_DIR = Path("reports/accessibility")
WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]


@pytest.fixture
def scan(page):
    """Return a function that scans the current page and saves the result."""

    def _scan(name, include=None, exclude=None):
        context = {}
        if include:
            context["include"] = include
        if exclude:
            context["exclude"] = exclude

        results = Axe().run(
            page,
            context=context or None,
            options={"runOnly": {"type": "tag", "values": WCAG_TAGS}},
        )

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        (REPORT_DIR / f"{name}.json").write_text(
            json.dumps(results.response, indent=2), encoding="utf-8"
        )
        return results

    return _scan
```

Line by line:

- Constants at the top (`REPORT_DIR`, `WCAG_TAGS`) mean the standard lives in one place. Change the target level once, and every test follows.
- `@pytest.fixture def scan(page)`: the fixture depends on `page`, so PyTest gives it the same tab the test is using.
- `def _scan(...)` is an inner function. The fixture **returns a function** rather than a result, because the test needs to choose *when* to scan (after navigating, after clicking) and what to call the report.
- The `context` dictionary is built only from what the caller passed; `context or None` sends `None` when it is empty, meaning "scan the whole document".
- `Axe().run(...)` is the call from section 7, with the standard options applied.
- The `write_text` lines save evidence for every scan automatically.
- `return results` hands the `AxeResults` object back so the test can assert on it.

#### A parametrized multi-page test

```python
# tests/accessibility/test_pages_a11y.py
import pytest

PAGES = [
    pytest.param("/", id="home"),
    pytest.param("/login", id="login"),
    pytest.param("/products", id="products"),
    pytest.param("/cart", id="cart"),
]


@pytest.mark.accessibility
@pytest.mark.parametrize("path", PAGES)
def test_page_has_no_axe_violations(page, scan, base_url, path):
    page.goto(f"{base_url}{path}")
    page.wait_for_load_state("networkidle")

    results = scan(name=path.strip("/") or "home")

    assert results.violations_count == 0, results.generate_report()
```

Line by line:

- `PAGES` is a list of `pytest.param` entries. The `id=` values make the test names readable: `test_page_has_no_axe_violations[login]` rather than `[/login]`.
- `@pytest.mark.accessibility` is a custom marker so you can run just these tests with `pytest -m accessibility`. Register it in `pytest.ini` to avoid warnings.
- `@pytest.mark.parametrize("path", PAGES)` creates one independent test per page. If `/cart` fails, `/home` still reports its own result.
- `base_url` is the fixture or option (`--base-url`) your framework already provides.
- `page.wait_for_load_state("networkidle")` waits until network activity settles, so content loaded by JavaScript is present when axe scans. Never use `time.sleep`; fixed pauses are either too short (flaky) or too long (slow).
- `path.strip("/") or "home"` turns `/login` into `login` and `/` into `home` for the report filename.
- The assertion uses `generate_report()` so a failure names the rule and element.

Adding a page to the scan is now one line. That is the payoff of building the fixture.

**Common mistakes:** scanning before the page is ready (random results); forgetting to give each report a unique name (files overwrite each other); testing only the home page.

### 9. Zero Violations, Baselines and Known-Issue Allowlists

"Assert zero violations" is the ideal. It is also unrealistic on day one with a legacy application that has 200 existing problems: the test would be permanently red, the team would ignore it, and you would have wasted your effort. You have three strategies.

| Strategy | Use when | Trade-off |
|----------|----------|-----------|
| **Zero violations** | New pages, new features, or after clean-up | Strictest; brand-new pages should always start here |
| **Impact threshold** | Legacy app; fail only on `critical` and `serious` | Simple, but still red if old serious issues exist |
| **Baseline / allowlist** | Legacy app with existing known issues | Fails only on *new* problems; needs maintenance |

#### Baseline test

A **baseline** is a saved list of known violations. The test fails only if the current scan contains something *not in the list*.

```python
import json
from pathlib import Path

BASELINE = Path("testdata/a11y_baseline.json")


def fingerprints(violations):
    return {f"{v['id']}|{n['target'][-1]}" for v in violations for n in v["nodes"]}


def test_products_page_has_no_new_violations(page, scan, base_url):
    page.goto(f"{base_url}/products")
    results = scan("products")

    known = set(json.loads(BASELINE.read_text())) if BASELINE.exists() else set()
    current = fingerprints(results.response["violations"])
    new_issues = current - known

    assert not new_issues, "NEW accessibility violations:\n  " + "\n  ".join(sorted(new_issues))
```

Line by line:

- `BASELINE` points to a JSON file of strings that is committed to the repository.
- `fingerprints(violations)` builds a **set** of identifiers, one per failing element. A fingerprint is `rule-id|selector`, such as `color-contrast|.hint`. The nested comprehension loops violations, then their nodes. `n['target'][-1]` takes the last selector in the target list (the element itself, even when it is inside a frame).
- `known` loads the saved list, or an empty set if no baseline exists yet.
- `current - known` is a set difference: everything present now that was not known before.
- `assert not new_issues` passes only when nothing new appeared, and the message lists exactly what is new.

The same idea can be an **allowlist** of deliberate exceptions, each with a reason:

```json
{
  "color-contrast|.promo-banner": "TICKET-481: brand colours under review, due Q4",
  "region|body": "TICKET-502: legacy template, scheduled for replacement"
}
```

A dictionary is better than a plain list because the **reason travels with the exception**.

**Common mistakes:** fingerprints built from fragile selectors (auto-generated class names change every build and make the baseline "fail" without a real regression); baselines that only ever grow; adding to the baseline without a ticket. A baseline should *shrink* over time. Review it regularly and delete fixed entries.

### 10. Scanning Dynamic States

A page's initial load is only one of its states. Many defects appear only after interaction, and a scan only sees what is in the DOM at that moment. A modal that is not open is not scanned.

#### An open modal

```python
def test_delete_dialog_is_accessible(page, scan, base_url):
    page.goto(f"{base_url}/account")
    page.get_by_role("button", name="Delete account").click()
    page.get_by_role("dialog").wait_for()

    results = scan("delete-dialog", include=[["[role=dialog]"]])

    assert results.violations_count == 0, results.generate_report()
```

Line by line: navigate to the page; click the button using a role-based locator (which also doubles as a quick check that the button has an accessible name); `wait_for()` pauses until the dialog is actually visible, so the scan never runs against an empty page; `include=[["[role=dialog]"]]` scans only the dialog, keeping the result focused and fast.

#### A logged-in page

Pages behind a login need an authenticated session. The efficient approach is a fixture that logs in once and reuses the session:

```python
@pytest.fixture
def logged_in_page(page, base_url):
    page.goto(f"{base_url}/login")
    page.get_by_label("Email").fill("qa.user@example.com")
    page.get_by_label("Password").fill("a-test-only-password")
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url("**/dashboard")
    return page


def test_dashboard_is_accessible(logged_in_page, scan):
    results = scan("dashboard")
    assert results.violations_count == 0, results.generate_report()
```

Explanation: the fixture performs the login steps using label-based locators, then waits for the URL to change before handing the page to the test. The test requests `logged_in_page` instead of `page`, but because the fixture returns the same `page` object, the `scan` fixture scans that very tab. Use test accounts and never real credentials; keep passwords in environment variables in a real framework.

**Other states worth scanning:** a validation-error state (submit an empty form), an open menu, a selected tab, an expanded accordion, an empty cart, a mobile viewport (`page.set_viewport_size({"width": 375, "height": 800})`), and any dark theme.

### 11. Triage: False Positives and "Incomplete"

A scan result is not a bug list until a human has looked at it. Triage in this order:

1. **Violations.** Verify each manually (use the highlighted element, the extension, or a keyboard check). Most will be real; log them.
2. **Incomplete.** These are the "axe is not sure" items. Typical causes: text over a gradient or background image (`color-contrast`), elements hidden or overlapped so axe could not measure them. Inspect each one manually. Do **not** fail the build on `incomplete`; print them in the report instead.
3. **Suspected false positives.** Rare with axe but possible with custom widgets or unusual CSS. Confirm manually that it really is acceptable, then suppress *that rule on that element*, with a comment and ticket. Never disable a rule globally to make a test pass.

A quick way to see incomplete items from Python:

```python
for item in results.response["incomplete"]:
    print(f"[review] {item['id']}: {len(item['nodes'])} element(s)  {item['helpUrl']}")
```

Explanation: `results.response["incomplete"]` is the list of rule objects needing review; the loop prints the rule id, the number of affected elements, and the help link for each.

**Flakiness.** Inconsistent results usually mean scanning before the page settled. Wait for a real condition (`wait_for_load_state`, `locator.wait_for()`), never for a fixed sleep.

### 12. Reporting Results

| Output | How | Used for |
|--------|-----|----------|
| Text summary | `results.generate_report()` | Assertion messages and console output |
| JSON per page | `json.dumps(results.response)` | Archive, comparison over time, dashboards |
| Test-runner reports | `pytest --junitxml=reports/junit.xml`, `pytest --html=reports/report.html` (with `pytest-html`) | Sharing with the team |
| Lighthouse report | `--output=html` or `json` on the CLI | A headline score for stakeholders |

A good report names the page, state, rule, impact, selector, and the help link, and distinguishes violations from `incomplete` items. Keep the JSON: it is the evidence you attach to a defect. Turning that evidence into well-written, prioritised defect reports is the subject of a later lesson; running these tests automatically on every pull request and keeping the reports as pipeline artifacts is covered Friday.

### 13. Limits and Combining With Manual Testing

Scans are fast and consistent, but have firm limits:

- They find only the machine-checkable minority of problems.
- They test only the state present in the DOM when they run.
- They cannot judge meaning, order, clarity, or real usability.
- They can be gamed by superficial fixes (adding `alt="image"` to quiet a rule).

A practical mix: an axe scan on key pages and states every commit; keyboard and screen-reader checks each feature; a fuller audit, ideally with assistive-technology users, before major releases.

### 14. Glossary

### axe-core
Open-source JavaScript accessibility rules engine from Deque, used by many tools.

### Rule
One automated check, identified by an `id` such as `image-alt`.

### Violation
A rule that definitely failed on at least one element.

### Incomplete
A result axe could not decide; needs manual review. Also called "needs review".

### Inapplicable
A rule with nothing to check on the page.

### Impact
Estimated severity: `minor`, `moderate`, `serious`, or `critical`.

### Node
One failing element within a violation, with `html`, `target`, and `failureSummary`.

### Target
A CSS selector locating the failing element.

### Context
The part of the page to scan (`include` and `exclude`).

### Baseline
A saved list of known violations so tests fail only on new ones.

### Allowlist
A list of deliberately accepted violations, each with a reason.

### Lighthouse score
A weighted pass/fail average of automated audits, 0-100; not a measure of overall accessibility.

### 15. Practice Exercises

#### Exercise 1: Read a violation

Given this node, answer: which rule failed, what is the impact, which WCAG criterion, and what exactly must change?

```json
{
  "id": "label",
  "impact": "critical",
  "tags": ["cat.forms", "wcag2a", "wcag412"],
  "help": "Form elements must have labels",
  "nodes": [
    {
      "html": "<input id=\"email\" type=\"text\">",
      "target": ["#email"],
      "failureSummary": "Fix any of the following:\n  Form element does not have an implicit (wrapped) <label>\n  Form element does not have an explicit <label>\n  aria-label attribute does not exist or is empty"
    }
  ]
}
```

**Solution.** The `label` rule failed with `critical` impact. The tag `wcag412` is criterion 4.1.2 (Name, Role, Value), level A. The input `#email` has no accessible name. Fix it by adding a visible label, for example `<label for="email">Email</label>` placed with the input, or (less ideal) an `aria-label`. A visible `<label>` is preferred because it also helps sighted users and enlarges the click target. Because the summary says "fix **any** of the following", one option is enough.

#### Exercise 2: Write a first scan

Write a test that opens `https://www.w3.org/WAI/demos/bad/before/home.html` and fails if axe finds any WCAG 2.0 A or AA violations.

**Solution.**

```python
from axe_playwright_python.sync_playwright import Axe


def test_before_demo_page_wcag2(page):
    page.goto("https://www.w3.org/WAI/demos/bad/before/home.html")
    results = Axe().run(
        page,
        options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}},
    )
    assert results.violations_count == 0, results.generate_report()
```

This test is *expected to fail*, because the "before" page is deliberately inaccessible; the failure message lists the problems. Change the URL to the `after` page and compare what remains. Remember the lesson's point: even the "after" page needs manual testing.

#### Exercise 3: A baseline that catches a regression

You have a baseline file `testdata/a11y_baseline.json` containing `["color-contrast|.hint"]`. A developer removes the `<label>` from `#email` in the signup page. Describe what the baseline test reports, and why it is better than "zero violations" for this app.

**Solution.** The current scan produces the fingerprints `color-contrast|.hint` (existing, in the baseline) and `label|#email` (new). The set difference `current - known` contains only `label|#email`, so the test fails with the message "NEW accessibility violations: label|#email". The existing contrast issue does not fail the build, so the team is not blocked by old debt, but the *new* problem is caught immediately, on the pull request that introduced it. With "zero violations" the test would already be red before the developer's change and would not distinguish old from new. As the old contrast issue is fixed, delete its line from the baseline so it cannot return unnoticed.

### 16. Quiz

**Q1. A page scores 100 in Lighthouse's accessibility audit. What can you conclude?**
A. The page meets WCAG AA
B. No automated audit failed, but manual testing is still needed
C. Screen reader users can use it
D. It has no `incomplete` items

**Q2. In axe results, what does the `incomplete` bucket contain?**
A. Rules that failed definitively
B. Rules that passed
C. Checks axe could not decide, needing human review
D. Rules not relevant to the page

**Q3. `results.violations_count` returns 3. What does that number represent?**
A. Three failing elements
B. Three failed rules (each may affect many elements)
C. Three pages with problems
D. Three critical issues

**Q4. You ask axe to run only `["wcag22aa"]`. Why is this a mistake?**
A. The tag does not exist
B. It only includes rules added in 2.2, skipping the 2.0 and 2.1 rules
C. It forces best-practice rules to run
D. It disables `color-contrast` only

**Q5. Why use a baseline on a legacy application?**
A. To hide accessibility issues permanently
B. To make the test fail on every violation
C. To fail the build only on new violations while old ones are fixed gradually
D. To skip scanning dynamic states

**Answers**

1. **B.** A perfect score means no automated check failed; it says nothing about meaning, order, or real usability.
2. **C.** `incomplete` means axe was not confident either way (for example text over an image), so a person reviews it.
3. **B.** The count is of rules that failed. One rule can have many `nodes`, so also report the element count.
4. **B.** Tags are not cumulative: `wcag22aa` holds only the criteria introduced at AA in WCAG 2.2, so you would miss most checks.
5. **C.** A baseline separates old known debt from new regressions, so the scan stays useful and the baseline shrinks as defects are fixed.

---

## Summary

- Automated scanners catch the objective, machine-checkable defects (missing labels, alt text, contrast, invalid ARIA) quickly and consistently, but not meaning, order, or real usability. A clean scan is not proof of accessibility.
- axe-core organises findings into `violations`, `passes`, `incomplete`, and `inapplicable`; each violation carries `id`, `impact`, `help`, `helpUrl`, and `nodes` with `target` and `failureSummary`.
- The axe extension and Lighthouse are for fast manual exploration; the Lighthouse score is a weighted average of automated audits, not a certificate. pa11y and WAVE are alternatives worth recognising.
- With `axe-playwright-python`, `Axe().run(page)` plus `violations_count` and `generate_report()` give a one-line scan; use `runOnly` tags (remembering they are not cumulative) and `include`/`exclude` contexts to focus it.
- Wrap scanning in a PyTest fixture and a parametrized test to cover many pages with one line each; save JSON evidence.
- Choose zero violations for new work, and baselines or allowlists with reasons for legacy apps; keep the baseline shrinking.
- Scan dynamic states (open dialogs, logged-in pages, error states), triage `incomplete` items by hand, and never fix a false positive by disabling a rule globally.
- Combine scans with the keyboard and screen-reader testing you learned earlier this week. Defect analysis of results comes later in the week, and running scans in CI is covered Friday.

## Additional Resources

- Deque, *axe-core documentation and rule descriptions*: https://www.deque.com/axe/core-documentation/
- axe-core repository and API reference (options, context, result object): https://github.com/dequelabs/axe-core
- *axe-playwright-python* on PyPI and GitHub: https://pypi.org/project/axe-playwright-python/
- Google Chrome for Developers, *Lighthouse accessibility scoring*: https://developer.chrome.com/docs/lighthouse/accessibility/scoring
- Playwright for Python, *Accessibility testing*: https://playwright.dev/python/docs/accessibility-testing
- W3C WAI, *Web Accessibility Evaluation Tools List*: https://www.w3.org/WAI/test-evaluate/tools/list/
