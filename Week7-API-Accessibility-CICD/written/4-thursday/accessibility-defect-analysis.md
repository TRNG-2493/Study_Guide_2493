# Accessibility Defect Analysis

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why a raw accessibility finding is not yet a defect, and turn findings into actionable tickets.
- Classify each defect by **WCAG success criterion**, **conformance level (A/AA/AAA)**, **POUR principle**, and **user group impacted**.
- Rate **severity** (blocker, critical, major, minor) using impact, frequency, workaround, and legal exposure, and separate it from **priority**.
- Assign a **root-cause category** (missing semantics, naming, contrast/design, focus management, ARIA misuse, dynamic content, content/authoring).
- Run a repeatable **triage workflow** and de-duplicate axe findings (one root cause, many nodes).
- Write a high-quality accessibility bug report, including environment, assistive technology (AT) version, evidence, and a before/after code fix.
- Verify fixes, write regression tests, and track metrics (violations over time, issue density).
- Explain an **accessibility conformance report (ACR/VPAT)** and build a remediation roadmap by user journey.

---

## Why This Matters

This is the Week 7 epic: your team is shipping a product with a tested API, an accessibility test strategy, and a CI/CD pipeline. By Thursday you have already learned the principles of accessibility, how to test with a keyboard and a screen reader, and how to run automated scans with axe. Those skills produce **findings**. This lesson is about what happens next.

A scan that returns 212 violations, or a note saying "the form isn't accessible", helps nobody. A developer cannot fix a vague note. A product owner cannot decide what to do first with a pile of 212 items. A lawyer cannot judge exposure from "some contrast issues". The skill that separates a strong QE from someone who just runs tools is **analysis**: turning observations into small, prioritised, well-evidenced, fixable defects, and then proving the fix works and stays fixed.

You will use this today in your pair exercise, where you audit a page and write defect reports. The same habits apply to the functional and API bugs you reported earlier this week. (Later this week, automation will help you keep these defects from returning. For now, focus on the human analysis.)

---

## The Concept

### 1. From Finding to Defect: What Is the Difference?

A **finding** is something you observed: "axe flagged `#email` for `label`", or "I pressed Tab and focus vanished." A **defect** is a finding that has been:

1. **Verified** (it is real, not a false positive; you can reproduce it).
2. **Scoped** (which pages and components are affected).
3. **Explained** (which standard it breaks and who it hurts).
4. **Rated** (how bad, and how soon).
5. **Made actionable** (a developer knows where to look and what "fixed" means).

Think of a doctor. A symptom ("my arm hurts") is a finding. A diagnosis with cause, severity, and treatment plan is the defect. Developers can only treat diagnoses.

---

### 2. The Triage Workflow

Use this workflow every time. It works for one page or a whole product.

```
Collect -> Verify -> De-duplicate -> Classify -> Rate -> Report -> Fix -> Retest -> Prevent
```

In short: verify each finding (reject false positives), merge duplicates, tag each with SC, level, POUR, users and root cause, rate severity then priority, write the ticket, retest with the original method, and add prevention.

---

### 3. Classifying a Defect

Classification gives every defect four labels. Do not skip them; they make your report credible ("this is a standards failure, not my opinion") and they drive severity.

#### 3.1 WCAG success criterion (SC)

The Web Content Accessibility Guidelines (WCAG) are organised into numbered **success criteria**, such as 1.4.3 Contrast (Minimum). The first digit tells you the principle, the second the guideline, the third the criterion. Always cite the number and name. If one defect breaks several criteria, list the one that fits best first, then others.

#### 3.2 POUR principle

Every SC belongs to one of four principles:

| Principle | Question | Example failures |
|-----------|----------|------------------|
| **Perceivable** | Can users sense the content? | Missing alt text, low contrast, no captions |
| **Operable** | Can users operate the interface? | Keyboard trap, no focus indicator, tiny targets |
| **Understandable** | Can users understand content and operation? | Unclear errors, unexpected context change |
| **Robust** | Does it work with current and future AT? | Missing name/role/value, invalid ARIA |

The first digit of the SC number maps directly: 1.x Perceivable, 2.x Operable, 3.x Understandable, 4.x Robust.

#### 3.3 Conformance level

Each SC is Level **A** (most basic), **AA** (the usual legal and contractual target), or **AAA** (aspirational, not required in full). Most organisations and laws target **WCAG 2.2 Level AA**, which means you must meet all A and AA criteria. A Level A failure is more fundamental than an AA failure, so it usually raises severity.

#### 3.4 User group impacted

Name the people affected. This keeps the team focused on real users, not rules.

Typical groups: blind and screen-reader users (names, roles, announcements); low-vision and colour-deficient users (contrast, resize); keyboard-only and switch users (focus, no traps); voice-control users (label matches name); deaf users (captions); cognitive-disability users (clear errors); vestibular users (reduced motion); and anyone in temporary or situational limits.

#### 3.5 Root-cause category

Also tag the technical origin. This tells you who should fix it and which prevention will work.

| Root-cause category | What it means | Typical SCs | Typical owner |
|---------------------|---------------|-------------|---------------|
| **Missing semantics** | Wrong or no HTML element (a `div` instead of `button`, no headings or landmarks) | 1.3.1, 2.1.1, 4.1.2 | Developer |
| **Naming** | Control has no or wrong accessible name (no label, no alt, "Click here") | 1.1.1, 2.4.4, 2.5.3, 4.1.2 | Developer and content |
| **Contrast / design** | Colours, focus style, target size, layout decisions | 1.4.3, 1.4.11, 2.4.7, 2.5.8 | Designer |
| **Focus management** | Focus lost, trapped, or not moved to new content | 2.1.2, 2.4.3, 3.2.2 | Developer |
| **ARIA misuse** | Wrong roles, redundant or conflicting ARIA, hidden-but-focusable | 4.1.2, 1.3.1 | Developer |
| **Dynamic content** | Updates not announced: toasts, errors, loading states, single-page route changes | 4.1.3, 3.3.1 | Developer |
| **Content / authoring** | Editors write vague links, skip heading levels, upload images without alt | 2.4.4, 2.4.6, 1.1.1 | Content team |

A rule of thumb from experience: *the first rule of ARIA is to not use ARIA if a native element does it.* A large share of ARIA misuse defects disappear when the right native element is used.

---

### 4. Severity and Priority

**Severity** describes how badly the defect hurts users. It is a property of the defect.
**Priority** is the order in which the business chooses to fix it. It uses severity plus cost, risk, traffic, and deadlines.

These are different. A severe defect on a page nobody visits may be lower priority than a moderate defect on checkout. A cosmetic bug for the CEO's demo may be a priority without being severe. Keep both fields.

#### 4.1 The four severity levels

| Severity | Criteria | Example |
|----------|----------|---------|
| **Blocker** | A user group cannot complete a core task at all, and there is no workaround. Release should not go ahead. | Checkout "Pay now" is a `div`: keyboard and screen-reader users cannot buy. Keyboard trap on login. |
| **Critical** | Task is possible only with great effort or outside help, or the defect affects a core task for a group. Workaround is hard to find. | Form errors are silent: users must guess what failed. No visible focus on the main nav. |
| **Major** | Significant difficulty or frustration, but a reasonable workaround exists or the task is secondary. | Heading levels skipped; contrast of 3.5:1 on body text; unclear link purpose in a long article. |
| **Minor** | Slight inconvenience, or a best-practice issue with little real impact. | Redundant `title` attributes; decorative image has a long alt; ARIA role that duplicates native role. |

Note: axe uses its own labels (critical, serious, moderate, minor). Treat axe's impact as a **starting point**, not the final rating, because axe cannot know your user journeys.

#### 4.2 The impact x frequency x workaround model

Score three factors, each Low (1), Medium (2), High (3):

- **Impact**: how much it harms the affected user (annoys = 1, hinders = 2, blocks = 3).
- **Frequency / reach**: how many users and pages (one rare page = 1, a section = 2, a global component or key journey = 3).
- **Workaround**: how hard it is to get around (easy = 1, hard to find = 2, none = 3).

Add the scores. A simple mapping: 8-9 Blocker, 6-7 Critical, 4-5 Major, 3 Minor. Then adjust using judgement and the legal factor below. Use the numbers to start a conversation, not to end it.

#### 4.3 Legal and contractual exposure

A Level A or AA failure on a public service (ADA claims in the US, the European Accessibility Act, UK Equality Act) or a contract that demands "WCAG 2.2 AA" raises urgency regardless of score. You are not a lawyer: write "Legal exposure: High (public checkout, SC 2.1.1 Level A)" and let legal and product decide.

#### 4.4 Priority

A simple priority scheme:

| Priority | Meaning | Typical rule |
|----------|---------|--------------|
| P1 | Fix this sprint | Blocker, or Critical on a key journey, or high legal risk |
| P2 | Next sprint | Critical elsewhere; Major on a key journey |
| P3 | Planned | Major elsewhere; Minor on a key journey |
| P4 | Backlog | Minor, low traffic |

Quick wins (cheap, global fixes such as restoring the focus outline) can be pulled forward even if their severity is only Major. Effort matters for priority but never for severity.

---

### 5. Running Example: ShopDemo Sign-up

We will analyse these raw findings from the ShopDemo sign-up page, gathered from earlier-lesson techniques (axe scan, keyboard test, NVDA + Firefox test).

Raw findings: axe `label` on 10 inputs across 3 pages; axe `color-contrast` on 14 hint nodes (#999 on #fff, 2.85:1); axe `button-name` on the icon search button; keyboard: "Create account" is a `div` and Tab skips it; keyboard: no visible focus ring; NVDA: errors not announced after submit; NVDA: heading jumps h1 to h4; NVDA: "Click here" appears 6 times.

Before reading on, notice that these 8 lines hide about 5 root causes in 4 categories. Section 6 shows how to see that.

---

### 6. De-duplicating axe Findings: One Root Cause, Many Nodes

An axe result has a **rule** (for example `label`), and under each rule a list of **nodes** (the individual elements that failed). One rule can have 50 nodes. This is where many beginners flood the tracker.

```json
{
  "id": "label",
  "impact": "critical",
  "tags": ["wcag2a", "wcag412", "wcag131"],
  "nodes": [
    { "target": ["#name"],  "html": "<input id=\"name\" type=\"text\">" },
    { "target": ["#email"], "html": "<input id=\"email\" type=\"email\">" },
    { "target": ["#city"],  "html": "<input id=\"city\" type=\"text\">" }
  ]
}
```

Line by line:

- `"id": "label"`: the axe rule that failed. This is the rule name you cite in the ticket.
- `"impact": "critical"`: axe's generic guess about severity; use it as a hint only.
- `"tags"`: includes `wcag2a` (Level A) and `wcag412`, `wcag131` (SC 4.1.2 and 1.3.1). These give you the WCAG mapping for free.
- `"nodes"`: each entry is one failing element. `target` is a CSS selector to find it; `html` is the markup.

All three inputs share the same shape: `<input id=... type=...>` with no `<label>`. That suggests a shared `Input` component that omits labels. One component fix repairs all three.

**De-duplication rules of thumb:**

1. **Same rule, same cause, same fix = one ticket.** List all selectors and pages in the ticket.
2. **Same rule, different causes = separate tickets.** Two `color-contrast` failures, one from the global grey hint style and one from a white-on-yellow banner in a different stylesheet, need different fixes.
3. **Same cause found by different methods = one ticket.** The unlabelled field found by axe and by NVDA ("edit, blank") is one defect; record both as "Detected by".
4. **Different rules, same element, same fix = one ticket** (`button-name` plus NVDA reading "button").

**Beware of false positives and "incomplete" results.** axe puts items it cannot decide into an `incomplete` list (for example, contrast over a background image). Check those by hand and record what you decided. Never silently ignore them.

**ShopDemo result after de-duplication:**

| Defect | Root cause | Category | Instances |
|--------|-----------|----------|-----------|
| D1 Inputs unlabelled | Shared `Input` component lacks `<label>` | Naming | 10 across 3 pages |
| D2 Hint text contrast | `.hint { color:#999 }` | Contrast / design | 14 nodes, 1 CSS rule |
| D3 Icon button no name | `.search-btn` has only an SVG | Naming | 1 (in global header, so every page) |
| D4 Submit is a `div` | Wrong element | Missing semantics | 1 |
| D5 No focus ring | `*:focus { outline:none }` | Contrast / design | Global |
| D6 Errors silent | No live region or focus move | Dynamic content | 1 form (pattern reused) |
| D7 Heading skip | Editors pick h4 for size | Content / authoring | 1 page |
| D8 "Click here" | Vague link text | Content / authoring | 6 links |

Eight lines of raw findings (and the hundreds of nodes behind them) are now eight actionable defects.

---

### 7. Classification and Rating of the ShopDemo Defects

| Defect | WCAG SC (level) | POUR | Users impacted | Severity | Priority | Reasoning |
|--------|-----------------|------|----------------|----------|----------|-----------|
| D4 Submit is a `div` | 2.1.1 Keyboard (A); 4.1.2 (A) | Operable / Robust | Keyboard, switch, screen reader | **Blocker** | P1 | Impact 3, reach 3 (core sign-up), no workaround 3 = 9; Level A; legal exposure |
| D1 Inputs unlabelled | 1.3.1 (A); 3.3.2 (A); 4.1.2 (A) | Perceivable / Understandable / Robust | Screen reader, voice control, cognitive | **Critical** | P1 | Form nearly unusable by ear; placeholder disappears when typing |
| D6 Errors silent | 3.3.1 (A); 4.1.3 (AA) | Understandable / Robust | Screen reader | **Critical** | P1 | User cannot recover from a mistake |
| D5 No focus ring | 2.4.7 Focus Visible (AA) | Operable | Keyboard, low vision | **Critical** | P1 | Global; one-line CSS quick win |
| D3 Icon button no name | 4.1.2 (A) | Robust | Screen reader, voice control | **Major** | P2 | Search is secondary to sign-up; user can browse instead |
| D2 Hint contrast 2.85:1 | 1.4.3 (AA) | Perceivable | Low vision, colour deficiency | **Major** | P2 | Helpful text is hard to read; fails AA |
| D7 Heading skip | 1.3.1 (A); 2.4.6 (AA) | Perceivable / Operable | Screen reader | **Minor** | P3 | Page still navigable |
| D8 "Click here" | 2.4.4 Link Purpose (A) | Operable | Screen reader, cognitive | **Minor** | P3 | Context nearby; fix in content |

---

### 8. Writing a High-Quality Accessibility Bug Report

A good ticket lets a developer fix the problem without asking you a single question. Each field below has a purpose.

| Field | Why it matters | Good example |
|-------|----------------|--------------|
| **Title** | Searchable, specific, names the component and the symptom | "Sign-up inputs have no accessible name (NVDA reads 'edit, blank')" |
| **Environment** | AT and browsers behave differently; the developer must reproduce | "Staging 2.4.1, Windows 11, Firefox 130, NVDA 2025.1" |
| **Steps** | Exact path, keys pressed | "1. Open /signup. 2. Press Tab twice." |
| **Expected** | What should happen, in user terms | "NVDA says 'Full name, edit, required'." |
| **Actual** | What really happens | "NVDA says 'edit, blank'." |
| **WCAG SC and level** | Turns opinion into standard | "1.3.1 (A), 4.1.2 (A)" |
| **Evidence** | Proof and a pointer to the code | Screenshot with axe node highlighted, selector, speech transcript |
| **Suggested fix** | Saves time; shows before/after | Code snippet |
| **Impact** | Who is blocked doing what | "Screen-reader users cannot register" |

The template below is a complete report. Read the annotations after it.

```markdown
## [A11Y] Sign-up: inputs have no accessible name (NVDA reads "edit, blank")

**ID:** A11Y-123
**Severity:** Critical   **Suggested priority:** P1   **Legal exposure:** High
**WCAG:** 1.3.1 Info and Relationships (A); 3.3.2 Labels or Instructions (A); 4.1.2 Name, Role, Value (A)
**Principle:** Perceivable / Understandable / Robust
**Root cause category:** Naming (shared Input component)
**Environment:** ShopDemo staging 2.4.1 | Windows 11 | Firefox 130 | NVDA 2025.1
**Detected by:** axe 4.10 rule `label` (10 nodes) + NVDA manual test
**Affected users:** Screen-reader, voice-control, cognitive disability users

### Steps to reproduce
1. Start NVDA. Open https://staging.shopdemo.test/signup in Firefox.
2. Press Tab until focus reaches the first text field.
3. Listen to the announcement. Repeat for the second field.

### Expected result
Each field is announced with its purpose, for example "Full name, edit, required".

### Actual result
NVDA announces "edit, blank" for every field. Placeholder text is the only hint and it
vanishes when typing. Same pattern on /login and /contact (10 inputs total).

### Evidence
- signup-axe.png (axe DevTools, node `#name` highlighted)
- NVDA speech viewer transcript: "edit blank / edit blank"
- Selector list: #name, #email, #city, #login-user, ...

### Suggested fix
Before:
    <input id="name" type="text" placeholder="Full name">
After:
    <label for="name">Full name</label>
    <input id="name" type="text" autocomplete="name" required>
Make `label` a required prop of the shared Input component.

### Acceptance criteria
- NVDA+Firefox and VoiceOver+Safari announce each label, role, and required state.
- axe `label` reports 0 violations on /signup, /login, /contact.
- Clicking the label focuses its input.
```

Walkthrough: the title names component, symptom, and observed behaviour so it is searchable. Severity, priority, and legal exposure are separate fields so triage can change one without the other. The WCAG line lists several criteria because one missing label breaks several. Environment gives version numbers for every layer, otherwise "works on my machine" closes the ticket. Evidence includes selectors that point at the code. The suggested fix shows a "before" the developer recognises and an "after" that works, and the last line fixes the cause. Acceptance criteria make "done" testable.

**Writing tips:** describe the product, not people; one defect per ticket; prefer facts ("2.85:1; 4.5:1 required") over adjectives.

---

### 9. Worked Examples: Five Realistic Defects

Each example shows the finding, analysis, and fix.

#### Example 1: Custom dropdown cannot be used by keyboard

**Finding:** The "Country" selector is a styled `div` that opens on click. Tab skips it; Enter and arrow keys do nothing.

**Analysis**
- WCAG: 2.1.1 Keyboard (A); 4.1.2 Name, Role, Value (A). Principle: Operable / Robust.
- Category: Missing semantics.
- Users: keyboard, switch, screen reader.
- Severity: Blocker (required field on sign-up, no workaround). Priority P1.

**Fix**

```html
<!-- Before -->
<div class="select" onclick="openList()">Country</div>

<!-- After: use the native element -->
<label for="country">Country</label>
<select id="country" name="country" autocomplete="country-name">
  <option value="">Choose a country</option>
  <option value="gb">United Kingdom</option>
  <option value="us">United States</option>
</select>
```

Explanation: the native `<select>` gives keyboard support, role, state, and mobile pickers for free. If design insists on a custom widget, it must implement the full ARIA combobox pattern with arrow-key and Escape handling; that costs far more and is easy to get wrong.

#### Example 2: Modal dialog loses focus

**Finding:** Opening "Delete account" shows a modal. Focus stays on the page behind it, and Tab moves through background links. After closing, focus jumps to the top of the page.

**Analysis**
- WCAG: 2.4.3 Focus Order (A); 1.3.2 Meaningful Sequence (A); 4.1.2 (A). Principle: Operable.
- Category: Focus management.
- Users: keyboard and screen-reader users (they may not realise a modal opened).
- Severity: Critical (a destructive action cannot be reliably completed or cancelled). Priority P1.

**Fix**

```javascript
let trigger;
function openModal(btn) {
  trigger = btn;                       // remember what opened it
  dialog.showModal();                  // native dialog traps focus and sets inert background
  dialog.querySelector("h2").focus();  // move focus into the dialog
}
dialog.addEventListener("close", () => trigger.focus()); // return focus on close
```

Explanation: `showModal()` on a `<dialog>` keeps focus inside and makes the page inert; focus moves to the heading (give it `tabindex="-1"`), and the `close` listener returns focus to the opener.

#### Example 3: Toast message never announced

**Finding:** After "Add to basket" a green toast reads "Item added". NVDA says nothing.

**Analysis**
- WCAG: 4.1.3 Status Messages (AA). Principle: Robust.
- Category: Dynamic content.
- Users: screen-reader users get no confirmation and may click again, adding duplicates.
- Severity: Major (they can check the basket icon as a workaround). Priority P2.

**Fix**

```html
<!-- Before: injected element, not in a live region -->
<div class="toast">Item added</div>

<!-- After: a live region that exists in the page from load -->
<div id="status" role="status" aria-live="polite"></div>
<script>
  document.getElementById("status").textContent = "Item added to basket";
</script>
```

Explanation: screen readers announce *changes* in a live region that already exists; a freshly injected element is often silent. Use `role="alert"` only for urgent errors.

#### Example 4: ARIA misuse on a "button" link

**Finding:** `<a href="#" role="button" aria-label="Buy" onclick="buy()">Add to basket</a>`. Voice users saying "click Add to basket" fail; NVDA announces "Buy, button" but Space does not work.

**Analysis**
- WCAG: 2.5.3 Label in Name (A); 4.1.2 (A); 2.1.1 (A). Principle: Operable / Robust.
- Category: ARIA misuse.
- Users: voice control, keyboard, screen reader.
- Severity: Critical (main action on product pages). Priority P1.

**Fix**

```html
<!-- Before -->
<a href="#" role="button" aria-label="Buy" onclick="buy()">Add to basket</a>

<!-- After -->
<button type="button" onclick="buy()">Add to basket</button>
```

Explanation: a link that acts as a button needs extra keyboard code for Space; the `aria-label` overrides the visible text and breaks Label in Name. A native `<button>` has the correct role, both Enter and Space, and the name equals the visible text. This illustrates "no ARIA is better than bad ARIA".

---

### 10. Verifying Fixes and Regression Testing

A fix is not done until the **same method that found it** confirms it, on the build that contains it.

| Found by | Retest by |
|----------|-----------|
| axe | Re-run the scan; all listed nodes are gone and no new violations appeared |
| Keyboard | Repeat the exact key sequence; check focus order, visibility, no trap |
| Screen reader | Same AT, same browser, same steps; compare announcement to "Expected" |

Also check three things:

1. **Neighbours**: did the fix break layout, another page, or another AT? (Test in a second browser/AT pair.)
2. **Every listed instance**: a grouped defect has many nodes; check each page, not only one.
3. **Acceptance criteria**: tick each one.

Record the result: "Verified in build 2.4.2, NVDA 2025.1 + Firefox 130, 3 pages, 2026-10-15: Pass." If it fails, reopen with new evidence.

**Regression tests** stop the defect returning. Pick the cheapest test that catches it:

```javascript
// Playwright: label regression + keyboard check
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("sign-up has no label violations", async ({ page }) => {
  await page.goto("/signup");
  const results = await new AxeBuilder({ page }).withRules(["label"]).analyze();
  expect(results.violations).toEqual([]);
});

test("Create account is keyboard reachable", async ({ page }) => {
  await page.goto("/signup");
  await page.getByLabel("Full name").focus();
  await page.keyboard.press("Tab");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: "Create account" })).toBeFocused();
});
```

Line by line: the imports bring in Playwright and the axe adapter. In the first test, we open /signup, run axe with only the `label` rule, and expect an empty violations array; if the shared component loses its label again, this fails. In the second, we focus the first field, press Tab twice, and assert the button is focused. `getByRole("button", {name})` also proves the element has the right role and name, so a `div` would fail.

Screen-reader announcements need a manual regression checklist run before releases.

---

### 11. Tracking Metrics

Metrics show progress and justify investment. Keep them simple.

Useful metrics: **violations over time** (open distinct defects and raw axe violations per release); **issue density** (defects per page or component, showing the worst areas); counts by severity and by level A/AA; **automation coverage** (defects found by axe divided by all defects, often 30-40%, which is why manual testing stays); mean time to fix; journey pass rate; and escape rate (found in production versus before release).

Warning: zero scanner violations does not mean usable; pair numbers with journey tests.

---

### 12. Accessibility Conformance Report (ACR) and VPAT

A **VPAT** (Voluntary Product Accessibility Template) is a standard form vendors use to describe how a product meets accessibility standards. The completed document is an **Accessibility Conformance Report (ACR)**. Buyers, especially governments and universities, ask for one during procurement.

For each WCAG criterion the report states a **conformance level**:

The standard terms are **Supports**, **Partially Supports**, **Does Not Support**, and **Not Applicable**, given per WCAG criterion.

Each row also has a remarks column. Your analysed defect list is the raw material: every open defect maps to an SC row, and the count and severity decide whether a row is "Partially Supports" or "Does Not Support". Be honest; an inflated ACR is a legal and reputational risk. QE usually provides the evidence, and a specialist or legal reviews the final document.

---

### 13. Remediation Roadmap: Prioritise by User Journey

With a ranked defect list, build a roadmap. Organise by **user journey**, not by WCAG number, because users experience journeys.

1. **List key journeys**: for ShopDemo, sign-up, login, search, checkout, account recovery.
2. **Map defects to journeys**: D4, D1, D6 all lie on sign-up.
3. **Find the broken journeys**: any journey with a Blocker cannot be completed by some users; those come first.
4. **Group by fix**: fix shared components and global CSS first; one change clears many defects.
5. **Slot into sprints**:
   - Sprint 1: unblock sign-up and login (D4, D1, D6, D5).
   - Sprint 2: search and checkout (D3, D2).
   - Sprint 3: content clean-up (D7, D8), plus training for editors.
6. **Retest each journey** end to end with keyboard and screen reader.
7. **Prevent**: regression tests, linters such as eslint-plugin-jsx-a11y, design-system fixes, and accessibility in the Definition of Done.

---

### 14. Common Mistakes

- Raising one ticket per axe node instead of grouping by root cause.
- Rating everything "Critical", or mixing severity with priority.
- Omitting browser, AT, and version numbers, or citing no WCAG criterion.
- Trusting axe impact blindly, or ignoring "incomplete" results.
- Closing a defect without retesting using the original method.
- Adding more ARIA instead of using native HTML, or blaming individuals.

### 15. Practice Exercises (with Solutions)

#### Exercise 1: Consolidate and classify

Raw notes: (a) axe `link-name` on 12 links, all icon links in the footer; (b) axe `region` on every page; (c) keyboard: no skip link; (d) NVDA: promo video has no captions; (e) NVDA: product-grid buttons read only "button".

Task: group into root causes, map SC, and rate.

**Solution**

| Defect | Root cause | SC (level) | POUR | Category | Severity | Priority |
|--------|-----------|-----------|------|----------|----------|----------|
| Footer icon links no name (a) | Social icons have only SVGs, one footer component | 2.4.4 (A), 4.1.2 (A) | Operable / Robust | Naming | Major | P2 |
| No landmarks (b) and no skip link (c) | Page template lacks `<main>`/`<nav>` and bypass block | 1.3.1 (A), 2.4.1 Bypass Blocks (A) | Perceivable / Operable | Missing semantics | Major | P2 |
| Video lacks captions (d) | Content upload process | 1.2.2 Captions (A) | Perceivable | Content | Critical if the video has key information, otherwise Major | P1/P2 |
| Grid buttons unnamed (e) | Button component renders icon only, repeated in each card | 4.1.2 (A) | Robust | Naming | Critical (product selection is core) | P1 |

Notes: (a) and (e) are different components, so separate tickets. (b) and (c) share a template fix, so one ticket.

#### Exercise 2: Rate with the model

The checkout "Apply coupon" input has no label. It is optional and checkout can complete without it. Rate it.

**Solution**

Impact 2 (hinders coupon users), reach 3 (key journey, shared component), workaround 2 (skip it, or guess from the placeholder). Total 7 suggests Critical, but the field is optional and the task can complete, so judgement lowers it to **Major, P2**. The shared component fix itself (defect D1) stays P1. The score starts the conversation; it does not end it.

#### Exercise 3: Write a report summary

Finding: pressing Tab on the carousel cycles between the Previous and Next arrows forever.

Task: fill in title, SC, severity, fix, acceptance criteria.

**Solution**

- Title: "Home carousel traps keyboard focus between Previous/Next arrows".
- SC: 2.1.2 No Keyboard Trap (A); Operable. Category: Focus management.
- Users: keyboard, switch, screen reader.
- Severity: Blocker (cannot reach checkout link or footer; home is high traffic). Priority: P1. Legal exposure: High (Level A).
- Cause: script intercepts Tab and wraps focus.
- Fix: remove the Tab key handler; let Tab move normally; offer arrow keys within slides if desired, and a pause control for auto-rotation.
- Acceptance criteria: Tab from the first heading passes through the carousel and reaches the footer; Shift+Tab goes back; no focus lost; Playwright test tabs up to 30 times and asserts the footer link is eventually focused.

---

### 15b. Glossary

#### Finding vs defect
A finding is an observation; a defect is a verified, scoped, rated, actionable finding.

#### Success criterion (SC)
A testable statement in WCAG, such as 2.4.7 Focus Visible.

#### POUR
Perceivable, Operable, Understandable, Robust: the four WCAG principles.

#### Conformance level
A, AA, or AAA; AA is the usual target.

#### Severity and priority
Severity is the impact on users; priority is the order of fixing.

#### Root cause
The single underlying code, design, or content problem behind one or many symptoms.

#### Assistive technology (AT)
Software or hardware that helps people use a computer, such as NVDA, JAWS, VoiceOver, Dragon.

#### Live region
A page area whose changes screen readers announce (`role="status"`, `aria-live`).

#### Regression test
A test that fails if a fixed defect returns.

#### ACR / VPAT
The report and template describing how a product conforms to accessibility standards.

---

### 17. Quiz

**Q1.** A scan reports 60 `label` violations, all from the shared `Input` component. How many tickets should you raise?
**Q2.** A defect blocks keyboard users from paying on checkout, but a fix is estimated at one day. Which fields differ: severity or priority?
**Q3.** Which POUR principle covers 4.1.2 Name, Role, Value?
**Q4.** A button shows "Search" but has `aria-label="Find products"`. Which SC fails and who is affected?
**Q5.** Why should you retest a screen-reader defect with the same AT and browser that found it?

**Answers**

1. One ticket, listing all affected pages and selectors, because one component fix repairs all 60 nodes.
2. Severity is Blocker regardless of effort. Priority is P1; the low effort only makes it easier to schedule. Effort never changes severity.
3. Robust (4.x).
4. 2.5.3 Label in Name (A); voice-control users (and some screen-magnifier and cognitive-support users) who say the visible label.
5. AT and browsers announce things differently; the same combination proves your original observation is resolved and avoids a false pass.

---

## Summary

- A finding becomes a **defect** only when verified, scoped, classified, rated, and made actionable.
- Use a repeatable triage workflow: collect, verify, de-duplicate, classify, rate, report, fix, retest, prevent.
- Classify each defect by WCAG SC, conformance level, POUR principle, user group, and root-cause category (missing semantics, naming, contrast/design, focus management, ARIA misuse, dynamic content, content/authoring).
- Rate severity (blocker, critical, major, minor) with impact x frequency x workaround and legal exposure; keep priority as a separate business decision.
- De-duplicate axe results: many nodes often share one root cause and one fix.
- A strong bug report has a specific title, environment with AT versions, steps, expected and actual results, WCAG reference, evidence, before/after fix, impact, and acceptance criteria.
- Verify with the original method, add regression tests, and track metrics such as violations over time, issue density, and automation coverage.
- Use ACR/VPAT concepts and a journey-based remediation roadmap to communicate and plan work.
- Later this week, MCP-based testing and the Friday CI/CD pipeline build on this: they help you run and enforce these checks automatically.

## Additional Resources

- W3C WAI, *Understanding WCAG 2.2*: https://www.w3.org/WAI/WCAG22/Understanding/
- W3C WAI, *Evaluating Web Accessibility Overview*: https://www.w3.org/WAI/test-evaluate/
- W3C WAI, *WCAG-EM Report Tool and Methodology*: https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/
- Deque University, *axe rule descriptions*: https://dequeuniversity.com/rules/axe/
- ITI, *VPAT and Accessibility Conformance Reports*: https://www.itic.org/policy/accessibility/vpat
- GOV.UK, *Making your service accessible*: https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
