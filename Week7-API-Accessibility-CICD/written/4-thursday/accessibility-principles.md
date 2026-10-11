# Accessibility Principles

## Learning Objectives

By the end of this lesson you will be able to:

- Define **accessibility (a11y)** and explain who benefits, including people with permanent, temporary, and situational limits.
- Describe visual, auditory, motor, and cognitive disabilities and the assistive technologies (AT) people use.
- Explain the legal and business drivers: ADA, Section 508, the European Accessibility Act (EAA), and WCAG.
- Explain the four **POUR** principles with a concrete example of each.
- Read the structure of **WCAG** (principles, guidelines, success criteria) and the A/AA/AAA conformance levels.
- Recognise key WCAG 2.2 criteria: 1.1.1, 1.4.3, 1.4.4, 2.1.1, 2.4.7, 2.5.8, 3.3.x, 4.1.2.
- Contrast semantic HTML with "div soup" and apply alt text, labels, headings, landmarks, contrast, and focus visibility.
- Use ARIA correctly: roles, states, properties, the first rule of ARIA, `aria-label`, `aria-labelledby`, `aria-describedby`, and live regions.
- Apply the principles as a tester by knowing what to check on any page.

---

## Why This Matters

Week 7 is about three disciplines that all answer one question: "Is this software really ready to ship?" On Monday through Wednesday you tested APIs (requests, status codes, schemas, automation of those checks). Today you turn to the user-facing side: can *everyone* actually use the product? On Friday the work moves into CI/CD pipelines so these checks run automatically on every change. Accessibility sits in the middle as a quality dimension that is easy to forget and expensive to ignore.

Consider three realistic situations:

- **The blocked checkout.** A retailer redesigns its checkout. The "Pay now" button is a styled `<div>`. Mouse users are fine. A keyboard-only user cannot reach it, and a screen reader user hears nothing. Every one of those customers abandons the purchase. Functionally "it works", yet for those users it does not.
- **The lawsuit letter.** A company receives a demand letter because its site cannot be used with a screen reader. Fixing it under legal pressure costs many times more than building it right.
- **The lost contract.** A public-sector tender requires a conformance report against WCAG 2.2 AA. The vendor cannot produce one, and a competitor wins.

As a Test Automation Engineer you will be expected to know the standards, spot defects by inspecting markup, automate what can be automated, and write precise defect reports. This lesson gives you the vocabulary and mental model. Hands-on techniques are **covered later today** in the keyboard and screen-reader testing, automated scanning, defect analysis, and MCP lessons, and Friday's CI/CD lesson covers running scans in a pipeline.

---

## The Concept

### 1. What Is Accessibility (a11y)?

**Accessibility** means designing and building products so people with disabilities can perceive, understand, navigate, and interact with them. The shorthand **a11y** is the letter "a", then 11 letters, then "y".

*What:* a quality attribute, like performance or security. An inaccessible page has defects.

*Why:* roughly 1 in 6 people worldwide lives with a significant disability (World Health Organization estimate). Many more have temporary or situational limits (next section).

*How:* by following a shared standard (WCAG), using standard HTML correctly, and testing with real assistive technology and real interaction patterns.

*When:* from the start. Retrofitting is possible but costly. Testers should check on every release, not once a year.

A useful reframe: accessibility is not a feature for a small group. It is *usability under varied conditions*. Most accessibility improvements help everyone (captions in a noisy train, keyboard shortcuts for power users, clear labels for a first-time visitor).

### 2. Types of Disability and Limits

Disability is not only permanent. The **permanent / temporary / situational** spectrum (popularised by Microsoft's Inclusive Design toolkit) shows how broad the audience is.

| Limit | Permanent | Temporary | Situational |
|-------|-----------|-----------|-------------|
| Seeing | Blind | Eye infection, dilated pupils | Glare from sunlight on a phone |
| Hearing | Deaf | Ear infection | Noisy cafe, sleeping baby nearby |
| Moving | One arm, paralysis | Broken wrist | Holding a baby, carrying shopping |
| Thinking | Dyslexia, memory conditions | Concussion, medication fog | Stress, distraction, tiredness |

#### 2.1 Visual
Blindness, low vision, colour-vision deficiency (about 1 in 12 men), light sensitivity.
*Barriers:* missing alt text, low contrast, information by colour only, content that breaks when zoomed.
*Real-world case:* a user with low vision zooms the browser to 300%. If the layout forces horizontal scrolling for every line, reading becomes impractical.

#### 2.2 Auditory
Deafness and hard of hearing.
*Barriers:* video without captions, audio-only instructions, alerts signalled only by sound.
*Real-world case:* a training video with no captions is unusable for a deaf employee, and also for anyone watching on mute in an open office.

#### 2.3 Motor (physical)
Tremors, paralysis, arthritis, missing limbs, repetitive strain injury.
*Barriers:* tiny click targets, drag-only interactions, hover-only menus, timed actions, anything requiring a mouse.
*Real-world case:* a user with a tremor cannot reliably hit a 12px "x" icon. A user who cannot use a mouse relies on keyboard, voice, or a switch device.

#### 2.4 Cognitive and neurological
Dyslexia, ADHD, autism, memory and learning difficulties, and also seizure conditions such as photosensitive epilepsy.
*Barriers:* dense jargon, inconsistent navigation, vague errors, short time limits, flashing content, forms that lose data on error.
*Real-world case:* a session timeout that logs you out after 60 seconds without warning can make a long form impossible for someone who needs more time.

Speech differences matter too: voice-only inputs need alternatives.

### 3. Assistive Technologies (Overview)

**Assistive technology (AT)** is hardware or software that helps people use a computer in ways that suit them.

| AT | Used by | What it does |
|----|---------|--------------|
| **Screen reader** (NVDA, JAWS, VoiceOver, TalkBack) | Blind, low vision | Speaks or brailles the content; navigates by headings, links, landmarks, form fields |
| **Screen magnifier / browser zoom** | Low vision | Enlarges content; relies on reflow and good contrast |
| **High-contrast / forced-colors mode, dark mode** | Low vision, light sensitivity | Overrides colours; custom drawn controls often vanish |
| **Captions, transcripts** | Deaf, hard of hearing | Text version of audio |
| **Keyboard only** | Motor, blind, power users | Tab, Shift+Tab, Enter, Space, arrows, Esc |
| **Voice control** (Dragon, Voice Control) | Motor | Says visible link or button names: "click Save" |
| **Switch device / eye tracking** | Severe motor | One or two inputs drive focus movement |
| **Reading aids, text-to-speech** | Dyslexia | Highlight or read text aloud |

Key insight for testers: a screen reader does not "look at" the screen. The browser builds an **accessibility tree** from your HTML (each node has a **name**, **role**, **state**, and **value**), and AT reads that tree. If the tree is wrong, the experience is wrong, however good the page looks.

### 4. Legal and Business Drivers

| Driver | Where | Short summary |
|--------|-------|---------------|
| **ADA** (Americans with Disabilities Act) | USA | Civil-rights law. Courts increasingly treat websites and apps as places of public accommodation; lawsuits are common. The law does not name a technical standard, but WCAG 2.x AA is what settlements and the Department of Justice rules reference. |
| **Section 508** (Rehabilitation Act) | USA | US federal agencies and their vendors must buy and provide accessible ICT. It incorporates WCAG 2.0 AA. |
| **EAA** (European Accessibility Act) | EU | Applies from June 2025 to many consumer products and services (e-commerce, banking, e-books, transport ticketing). Referenced via the standard EN 301 549, which maps to WCAG 2.1 AA. |
| **Equality Act, AODA, others** | UK, Ontario, etc. | Similar duties in other jurisdictions. |
| **WCAG** | International (W3C) | The technical yardstick that nearly every law and contract points to. |

*Note:* this is an overview for testers, not legal advice. Your organisation's compliance team decides the exact target.

Business drivers beyond law:

- **Market reach:** disability communities and ageing populations are large customer segments.
- **SEO and quality:** semantic HTML, text alternatives, and good structure help search engines and maintainability.
- **Brand and risk:** accessibility failures become public, and lost tenders are costly.
- **Better engineering:** teams that test accessibility tend to ship cleaner markup and more robust UIs.

### 5. WCAG: Structure and Versions

**WCAG** (Web Content Accessibility Guidelines) is published by the W3C Web Accessibility Initiative (WAI). It has a three-level hierarchy:

1. **Principles (4):** Perceivable, Operable, Understandable, Robust (POUR).
2. **Guidelines (13 in WCAG 2.x):** broad goals, for example 1.1 "Text Alternatives" or 2.4 "Navigable".
3. **Success criteria:** testable statements, for example **1.1.1 Non-text Content**. They are numbered *principle.guideline.criterion*, so "1.4.3" means principle 1, guideline 4 (Distinguishable), criterion 3.

Beneath these sit non-normative **Techniques** and **Failures** (documents explaining how to meet or how people commonly fail a criterion) and **Understanding** pages. These are what you cite and read when writing defects.

| Version | Year | Notes |
|---------|------|-------|
| 2.0 | 2008 | Foundation; Section 508 refresh uses it |
| 2.1 | 2018 | Added mobile, low-vision, and cognitive criteria |
| **2.2** | 2023 | Added focus visibility improvements, **target size**, accessible authentication, consistent help, dragging alternatives. Backward compatible with 2.1 |
| 3.0 | In development | Not yet a standard; do not cite |

Versions are **additive**: meeting 2.2 AA implies meeting 2.1 AA (except one obsolete criterion, 4.1.1 Parsing, removed in 2.2).

#### 5.1 Conformance levels

| Level | Meaning | Examples | Typical use |
|-------|---------|----------|-------------|
| **A** | Minimum. Failing it blocks some users completely | 1.1.1 alt text, 2.1.1 keyboard, 4.1.2 name/role/value | Mandatory baseline |
| **AA** | Removes major barriers for most users | 1.4.3 contrast 4.5:1, 1.4.4 resize text, 2.4.7 focus visible, 2.5.8 target size | **The legal and contractual target** |
| **AAA** | Highest; not achievable for all content | 1.4.6 enhanced contrast 7:1, sign-language video | Aspirational, applied selectively |

To claim AA conformance a page must meet **all** Level A **and** Level AA criteria. Partial conformance is not AA.

### 6. The POUR Principles in Depth

#### 6.1 Perceivable: information must be presentable in ways users can perceive

*What:* nothing important is available only through a single sense. *Why:* a blind user cannot see an image; a deaf user cannot hear a video. *How:* provide alternatives and flexible presentation. *When:* every time you add non-text content or style information.

Main criteria areas:

- **Text alternatives** (1.1.1)
- **Captions and transcripts** for audio and video (1.2.x)
- **Adaptable structure**: meaning is in the code, not just the look (1.3.x)
- **Distinguishable**: contrast, resize, no colour-only meaning, reflow (1.4.x)

*Scenario:* a dashboard shows status as red and green dots. A colour-blind user cannot tell failed from passed. Adding text ("Failed") or an icon with a name fixes it.

#### 6.2 Operable: the interface must be usable by many input methods

*What:* every function works without a mouse, with enough time, and without harm. *Why:* many users never use a mouse. *How:* keyboard support, visible focus, no traps, skip links, adequate target size.

*Scenario:* a mega-menu opens on hover only. Keyboard users cannot open it, and touch users have no hover. Make it open on focus or click.

#### 6.3 Understandable: content and behaviour must be predictable and clear

*What:* readable text, predictable behaviour, help with mistakes. *Why:* people with cognitive disabilities, or anyone in a hurry, need clear interactions. *How:* declare the language, label inputs, keep navigation consistent, explain errors.

*Scenario:* submitting a form returns "Error 4012". The user has no idea what to fix. "Enter a date in the format DD/MM/YYYY" is understandable.

#### 6.4 Robust: content must work with current and future user agents

*What:* markup that browsers and AT can reliably interpret. *Why:* AT depends on the accessibility tree. *How:* valid semantic HTML, correct name/role/state for custom widgets, announce status messages.

*Scenario:* a custom dropdown built from `<div>`s looks right but exposes nothing. A screen reader announces "group" and nothing else. Using `<select>` or correct ARIA makes it robust.

### 7. Key WCAG 2.2 Success Criteria

| Criterion | Level | Plain-English requirement | Quick tester check |
|-----------|-------|---------------------------|--------------------|
| **1.1.1** Non-text Content | A | Non-text content has a text alternative serving the same purpose | Inspect each `<img>`, icon button, chart |
| **1.4.3** Contrast (Minimum) | AA | Text contrast at least **4.5:1**; large text (18pt, or 14pt bold) at least **3:1** | Colour picker or contrast checker |
| **1.4.4** Resize Text | AA | Text can be resized to 200% without loss of content or function | Zoom to 200% and look for clipping |
| **2.1.1** Keyboard | A | All functionality operable via keyboard | Unplug the mouse and complete the task |
| **2.4.7** Focus Visible | AA | Keyboard focus indicator is visible | Tab through; can you always see where you are? |
| **2.5.8** Target Size (Minimum) | AA (new in 2.2) | Pointer targets at least **24 by 24 CSS pixels**, with exceptions (inline links, enough spacing) | Measure buttons and icons |
| **3.3.1** Error Identification | A | Errors are identified and described in text | Submit invalid data |
| **3.3.2** Labels or Instructions | A | Inputs have labels or instructions | Check every field |
| **3.3.3** Error Suggestion | AA | If a fix is known, suggest it | Read the messages |
| **4.1.2** Name, Role, Value | A | Every UI component exposes name, role, and state | Inspect accessibility tree |

Other criteria you will meet often: 1.3.1 Info and Relationships, 1.4.1 Use of Color, 1.4.10 Reflow, 1.4.11 Non-text Contrast (3:1 for UI parts), 2.4.1 Bypass Blocks, 2.4.2 Page Titled, 2.4.4 Link Purpose, 3.1.1 Language of Page, 4.1.3 Status Messages.

### 8. Semantic HTML versus "Div Soup"

**Semantic HTML** means choosing elements for what they *mean*. **Div soup** is markup made of generic `<div>` and `<span>` elements styled to look like real controls.

*Why it matters:* native elements ship with role, name, keyboard behaviour, and focus handling for free. A `<div>` ships with none of it, so you must rebuild everything, usually imperfectly.

#### 8.1 Bad versus good: a button

```html
<!-- BAD: div soup -->
<div class="btn" onclick="save()">Save</div>

<!-- GOOD: native element -->
<button type="button" onclick="save()">Save</button>
```

Line by line:

- `<div class="btn" ...>`: a generic container. The accessibility tree role is "generic"; the screen reader announces just "Save", with no hint it is clickable.
- `onclick="save()"`: only fires on mouse click or touch. The div is not in the Tab order, so keyboard users cannot reach it. Enter and Space do nothing.
- `<button type="button">`: role "button", focusable, activates with Enter and Space, and appears in voice-control lists. `type="button"` stops it submitting a surrounding form by accident.

The same logic applies to links (`<a href>`), headings (`<h1>`-`<h6>`), lists (`<ul>`, `<ol>`), and tables (`<table>`, `<th>`).

#### 8.2 Alt text

```html
<!-- BAD: missing alt; some screen readers read the file name -->
<img src="chart-q3.png">

<!-- BAD: useless alt -->
<img src="chart-q3.png" alt="image">

<!-- GOOD: informative -->
<img src="chart-q3.png" alt="Bar chart: Q3 sales rose 12% over Q2, led by EMEA">

<!-- GOOD: decorative -->
<img src="divider.png" alt="">

<!-- GOOD: image inside a link describes the destination -->
<a href="/cart"><img src="cart.svg" alt="View cart (3 items)"></a>
```

Line by line:

- First line: no `alt` attribute at all. This is a failure of 1.1.1.
- Second: an `alt` exists but says nothing useful ("image" is already announced by the role).
- Third: the text conveys what a sighted user learns from the chart. Ask: "What would I say if reading this aloud on the phone?"
- Fourth: `alt=""` (empty, not missing) tells AT to skip a purely decorative image.
- Fifth: when an image is the only content of a link, the alt text acts as the link text and should describe the action.

Rule of thumb: informative image, describe its meaning; decorative, empty alt; complex chart, short alt plus a longer description or data table nearby.

#### 8.3 Labels

```html
<!-- BAD: placeholder as the only label -->
<input type="email" placeholder="Email">

<!-- GOOD: explicit label -->
<label for="email">Email address</label>
<input id="email" name="email" type="email" autocomplete="email" required>
```

Line by line:

- The placeholder vanishes as soon as the user types, is often low contrast, and is not reliably used as the accessible name.
- `<label for="email">` and `id="email"` must match: this programmatic link means clicking the label focuses the input and a screen reader announces "Email address, edit text".
- `type="email"` gives the right mobile keyboard and basic validation.
- `autocomplete="email"` lets browsers and assistive tools fill in the value (criterion 1.3.5 Identify Input Purpose).
- `required` exposes the required state to AT.

#### 8.4 Headings and landmarks

```html
<!-- BAD: visual headings only, no structure -->
<div class="big-bold">Order history</div>
<div class="nav"><a href="/">Home</a></div>

<!-- GOOD: structure users can navigate by -->
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header><p>ShopDemo</p></header>
  <nav aria-label="Main"><ul><li><a href="/">Home</a></li></ul></nav>
  <main id="main">
    <h1>Order history</h1>
    <h2>Recent orders</h2>
  </main>
  <footer>&copy; 2026 ShopDemo</footer>
</body>
```

Line by line:

- `skip-link`: first focusable item; jumps over repeated navigation (2.4.1 Bypass Blocks). It is usually hidden visually until focused.
- `<header>`, `<nav>`, `<main>`, `<footer>`: **landmarks**. Screen reader users jump between them with shortcut keys. Use one `<main>` per page.
- `aria-label="Main"` on `<nav>`: when there are several navs (main, footer, breadcrumb), labels tell them apart.
- `<h1>` then `<h2>`: a logical outline. Do not skip levels for visual size; use CSS for size.
- The bad version is invisible to heading and landmark navigation.

Also set the page language and title: `<html lang="en">` and a unique `<title>`.

#### 8.5 Colour contrast

```css
/* BAD: ratio about 2.85:1 on white, fails 1.4.3 */
.hint { color: #999999; background: #ffffff; }

/* GOOD: ratio about 4.54:1, passes AA for normal text */
.hint { color: #767676; background: #ffffff; }
```

Line by line:

- `color` and `background` together determine the ratio. Contrast is always a *pair*.
- `#999999` on white is roughly 2.85:1: below the 4.5:1 minimum.
- `#767676` on white is roughly 4.54:1: the lightest grey that passes for normal text.
- Large text needs only 3:1, and meaningful UI parts (input borders, icons) need 3:1 under 1.4.11.

#### 8.6 Focus visibility

```css
/* BAD: removes the only cue keyboard users have */
button:focus { outline: none; }

/* GOOD: strong, visible indicator for keyboard focus */
button:focus-visible {
  outline: 3px solid #1a56db;
  outline-offset: 2px;
}
```

Line by line:

- `outline: none` with no replacement fails 2.4.7. Developers often add it because the default ring "looks ugly".
- `:focus-visible` applies the style when the browser decides focus should be shown (keyboard use), avoiding rings on mouse clicks.
- `3px solid #1a56db` is a thick, high-contrast ring. `outline-offset: 2px` separates it from the element so it is not lost against borders.

#### 8.7 Target size (WCAG 2.2)

```css
/* BAD: 16px icon button, hard to hit, fails 2.5.8 */
.icon-btn { width: 16px; height: 16px; padding: 0; }

/* GOOD: at least 24x24 CSS pixels (44x44 is a comfortable aim) */
.icon-btn { min-width: 44px; min-height: 44px; padding: 10px; }
```

The graphic may stay small; the *clickable area* grows through padding.

### 9. ARIA: Filling the Gaps

**WAI-ARIA** (Accessible Rich Internet Applications) is a set of HTML attributes that tell AT things native HTML cannot express, such as "this `<div>` is a tab panel" or "this section updates live". ARIA changes only what AT is told, **not** behaviour: it adds no keyboard support and no focus.

| Kind | Meaning | Examples |
|------|---------|----------|
| **Roles** | What something *is* | `role="dialog"`, `role="tablist"`, `role="alert"`, `role="status"` |
| **Properties** | Relationships and fixed traits | `aria-label`, `aria-labelledby`, `aria-describedby`, `aria-controls` |
| **States** | What something is *doing now* | `aria-expanded`, `aria-checked`, `aria-selected`, `aria-hidden`, `aria-invalid` |

#### 9.1 The first rule of ARIA

> If you can use a native HTML element that already has the semantics and behaviour you need, use it instead of adding ARIA. **No ARIA is better than bad ARIA.**

Supporting rules: do not change native semantics unnecessarily; every interactive ARIA control must be keyboard operable; do not put `aria-hidden="true"` on focusable elements; every interactive element needs an accessible name.

#### 9.2 When NOT to use ARIA

```html
<!-- BAD: ARIA bolted onto the wrong element, and still incomplete -->
<div role="button" onclick="save()">Save</div>

<!-- BAD: contradicts native semantics -->
<h2 role="button">Details</h2>

<!-- GOOD: native element, no ARIA needed -->
<button type="button" onclick="save()">Save</button>
```

Line by line:

- `role="button"` makes AT announce "button", but the `<div>` is still not focusable and ignores Enter and Space. You have created a *promise you do not keep*, which is worse than saying nothing.
- `<h2 role="button">` removes the heading semantics, so heading navigation loses that item.
- The native `<button>` needs zero ARIA.

Use ARIA when no native element fits: tabs, comboboxes, tree views, modal dialogs (though `<dialog>` helps), live announcements.

#### 9.3 Accessible name: aria-label and aria-labelledby

The **accessible name** is what AT announces for an element. The browser computes it in priority order: `aria-labelledby`, then `aria-label`, then native sources (`<label>`, `alt`, text content), then `title`.

```html
<!-- BAD: icon-only button, no name: announced just as "button" -->
<button type="button"><svg><!-- x icon --></svg></button>

<!-- GOOD: aria-label gives the name -->
<button type="button" aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false"><!-- x icon --></svg>
</button>

<!-- GOOD: aria-labelledby points to visible text -->
<section aria-labelledby="bill-title">
  <h2 id="bill-title">Billing address</h2>
  ...
</section>
```

Line by line:

- First: an unnamed button fails 4.1.2. Users hear "button" and cannot know what it does.
- `aria-label="Close dialog"`: a string used as the name. Use it when there is no visible text. Remember to translate it for localised sites.
- `aria-hidden="true"` on the `<svg>`: hides the decorative icon so it is not read twice; `focusable="false"` stops old browsers tabbing into the SVG.
- `aria-labelledby="bill-title"`: takes the name from another element's text via its `id`. Preferred when visible text already exists, because the visible and announced names stay in sync (supports voice control, 2.5.3 Label in Name).

#### 9.4 aria-describedby

```html
<label for="pw">Password</label>
<input id="pw" type="password" aria-describedby="pw-help pw-error" aria-invalid="true">
<p id="pw-help">At least 12 characters.</p>
<p id="pw-error">Password is too short.</p>
```

- `aria-describedby="pw-help pw-error"`: space-separated ids; the screen reader reads them *after* the name and role, as extra description ("Password, edit text, invalid, At least 12 characters. Password is too short.").
- `aria-invalid="true"`: exposes the error state (set it only after validation fails).
- Name versus description: the **name** says *what it is*; the **description** gives supporting detail.

#### 9.5 States and properties on custom widgets

```html
<button type="button" aria-expanded="false" aria-controls="faq1">Return policy</button>
<div id="faq1" hidden>Returns are accepted within 30 days.</div>
```

```javascript
button.addEventListener("click", () => {
  const open = button.getAttribute("aria-expanded") === "true";
  button.setAttribute("aria-expanded", String(!open)); // tell AT the new state
  panel.hidden = open;                                  // show or hide the panel
});
```

Line by line:

- `aria-expanded="false"`: AT announces "collapsed". It must flip to `"true"` when opened, or users get stale information.
- `aria-controls="faq1"`: links the button to the panel it controls (support varies, so do not depend on it alone).
- `hidden` attribute: hides the panel visually and from AT.
- The script reads the current state, writes the opposite, and syncs the panel. State attributes that never change are one of the most common ARIA bugs.

#### 9.6 Live regions

```html
<!-- Polite: announced when the user is idle -->
<div id="cart-status" role="status" aria-live="polite"></div>

<!-- Assertive: interrupts; use for errors -->
<div role="alert"></div>
```

```javascript
document.getElementById("cart-status").textContent = "3 items in your cart";
```

Line by line:

- A **live region** tells AT to announce changes inside it without moving focus (criterion 4.1.3 Status Messages).
- `role="status"` implies `aria-live="polite"`; `role="alert"` implies `assertive`. `polite` waits for a pause, `assertive` interrupts, so use it sparingly.
- The region must exist in the DOM *before* the text is inserted. Updating `textContent` triggers the announcement.
- Representative announcement: "3 items in your cart".

### 10. How Testers Apply the Principles

Start with a repeatable checklist for any page or feature.

| Principle | Ask yourself | Look for |
|-----------|--------------|----------|
| **Perceivable** | Can I get the information without sight or sound? | Alt text, captions, contrast, no colour-only cues, 200% zoom and 320px reflow |
| **Operable** | Can I do everything with the keyboard alone? | Tab order, no traps, visible focus, skip link, target size, no timeouts |
| **Understandable** | Is it clear what to do and what went wrong? | `lang`, labels, instructions, specific errors, consistent navigation |
| **Robust** | Does the accessibility tree tell the truth? | Native elements, name/role/state, valid ARIA, live status messages |

A practical first five minutes:

1. Read the page title and zoom to 200%.
2. Tab through the whole page. Can you see focus every time and reach every control?
3. Inspect two or three controls in DevTools (Accessibility panel) and read their name and role.
4. Check headings and landmarks.
5. Submit a form with errors and read the messages.

Automation finds only a fraction of issues (commonly estimated at a third to a half): missing alt, missing labels, contrast, invalid ARIA. Humans must judge whether alt text is *meaningful*, focus order is *logical*, and errors are *understandable*. How to do each is **covered later today** (keyboard and screen-reader testing, automated scanning, defect analysis), and running scans in pipelines is **covered Friday**.

When you report a defect, always include: the page and element, the WCAG criterion number and level, steps to reproduce, actual versus expected result, and the user impact.

### 11. Common Mistakes

1. **Placeholder instead of a label.** Fix with a real `<label>`.
2. **`outline: none` with no replacement.** Fails 2.4.7. Provide a strong `:focus-visible` style.
3. **Clickable `<div>`/`<span>`.** Use `<button>` or `<a href>`.
4. **Empty or vague link text** ("click here", icon links with no name). Link text should make sense out of context.
5. **Skipping heading levels or using headings for size.** Use CSS for size.
6. **Colour as the only signal** (red border for an error with no text).
7. **ARIA used instead of HTML**, or ARIA states that never update.
8. **`aria-hidden="true"` on focusable elements**, creating silent focus targets.
9. **Using alt text on everything**, or filename alts such as `alt="IMG_2044.jpg"`.
10. **Believing a clean automated scan means "accessible".** It means "no machine-detectable failures".
11. **Ignoring reduced-motion and zoom**: layouts that break at 200% or flashing animations.

### 12. Glossary

### 12.1 Core terms

- **a11y:** abbreviation of "accessibility".
- **AT (assistive technology):** tools such as screen readers, magnifiers, switches.
- **Accessibility tree:** the browser's structured view (name, role, state, value) that AT reads.
- **Accessible name:** the text AT announces for an element.
- **Landmark:** page region (`header`, `nav`, `main`, `footer`) users can jump between.
- **Focus:** the element currently receiving keyboard input.
- **Focus trap:** keyboard focus that cannot leave a component (a defect, except in modal dialogs that manage it properly).
- **Live region:** area whose changes are announced automatically.
- **Screen reader:** software that outputs content as speech or braille.

### 12.2 Standards and law

- **WCAG:** W3C Web Content Accessibility Guidelines (current 2.2).
- **POUR:** Perceivable, Operable, Understandable, Robust.
- **Success criterion (SC):** one testable WCAG requirement, e.g. 1.4.3.
- **Conformance level:** A, AA, AAA.
- **ADA / Section 508 / EAA / EN 301 549:** US civil-rights law / US federal procurement rules / EU directive / European standard referencing WCAG.
- **VPAT / ACR:** report documenting how a product meets accessibility criteria.

### 12.3 Technical terms

- **Semantic HTML:** elements chosen for meaning.
- **Div soup:** generic elements used where semantic ones belong.
- **ARIA role / state / property:** what it is / what it is doing / fixed relationship or trait.
- **Contrast ratio:** luminance comparison of two colours, from 1:1 to 21:1.
- **Reflow:** content adapting to narrow width (320 CSS px) without two-direction scrolling.

### 13. Practice Exercises

**Exercise 1: Spot the barrier.** List one barrier for each of the four disability categories in a typical online store and name the WCAG criterion each would violate.

*Solution (representative):*
- Visual: product photos with no alt text, 1.1.1.
- Auditory: product demo video with no captions, 1.2.2.
- Motor: "Add to cart" built from a `<div>` that is not keyboard reachable, 2.1.1.
- Cognitive: error message "Invalid input" with no explanation, 3.3.1 and 3.3.3.

**Exercise 2: Contrast check.** Does `#777777` text on `#FFFFFF` pass AA for normal text? What about `#595959`?

*Solution:* `#777777` on white is about 4.48:1 (just *below* 4.5:1), so it fails for normal text but passes for large text (3:1). `#595959` is about 7:1, so it passes AA and even AAA (7:1). The takeaway: tiny differences matter, so always measure with a checker rather than judging by eye. (Exact values vary slightly by tool; treat them as representative.)

**Exercise 3: Fix the markup.** Make this accessible, naming each fix:

```html
<div class="form">
  <div>Sign up</div>
  <input type="text" placeholder="Email">
  <div class="btn" onclick="go()">Create account</div>
  <img src="logo.png">
</div>
```

*Solution:*

```html
<main>
  <h1>Sign up</h1>
  <form onsubmit="return go(event)">
    <label for="email">Email address</label>
    <input id="email" name="email" type="email" autocomplete="email" required>
    <button type="submit">Create account</button>
  </form>
  <img src="logo.png" alt="ShopDemo logo">
</main>
```

Fixes: `<main>` landmark; `<h1>` real heading (1.3.1); `<label for>` replaces placeholder (3.3.2, 4.1.2); `type="email"` and `autocomplete` (1.3.5); real `<button type="submit">` (2.1.1, 4.1.2); `alt` on the image (1.1.1). Notice that no ARIA was needed.

**Exercise 4: Name the icon button and make it announce state.** Fix `<a href="#" onclick="openMenu()"><img src="menu.png"></a>` so it opens a navigation menu `#site-menu`.

*Solution:*

```html
<button type="button" aria-expanded="false" aria-controls="site-menu" id="menu-btn">
  <img src="menu.png" alt="Menu">
</button>
<nav id="site-menu" aria-label="Main" hidden>...</nav>
```

Explanation: the action opens something, so it is a `<button>`, not a link (a link navigates). The image `alt="Menu"` provides the accessible name. `aria-expanded` and `aria-controls` expose state and relationship, and the script must flip `aria-expanded` as in section 9.5. Representative screen-reader announcement: "Menu, button, collapsed".

### 14. Knowledge Check (5 Questions)

1. What do the letters in POUR stand for, and which principle does "all functionality available by keyboard" belong to?
2. What is the minimum contrast ratio for normal text under WCAG 1.4.3?
3. Which conformance level is usually the legal and contractual target?
4. State the first rule of ARIA.
5. Which is better for a "Save" action and why: `<div role="button" onclick>` or `<button>`?

**Answers:**

1. Perceivable, Operable, Understandable, Robust. Keyboard access (2.1.1) belongs to **Operable**.
2. **4.5:1** (3:1 for large text).
3. **Level AA** (all A plus AA criteria).
4. If a native HTML element provides the semantics and behaviour you need, use it instead of ARIA. No ARIA is better than bad ARIA.
5. `<button>`. It is focusable, activated with Enter and Space, announced with the right role, and needs no extra code. The `div` with a role only *claims* to be a button and still lacks keyboard behaviour.

---

## Summary

- **Accessibility (a11y)** lets people with permanent, temporary, and situational limits use your product. It is a quality attribute backed by law (ADA, Section 508, EAA) and by business sense.
- Disabilities fall into visual, auditory, motor, and cognitive groups, each with its own assistive technologies. AT reads the browser's **accessibility tree**, so correct markup is what matters.
- **WCAG** has 4 principles (POUR), guidelines, and testable success criteria at levels A, AA, AAA. **WCAG 2.2 AA** is the usual target.
- Key criteria to remember: 1.1.1 alt, 1.4.3 contrast 4.5:1, 1.4.4 resize, 2.1.1 keyboard, 2.4.7 focus visible, 2.5.8 target size 24px, 3.3.x errors and labels, 4.1.2 name/role/value.
- **Semantic HTML first**: native buttons, links, labels, headings, and landmarks give accessibility for free; div soup removes it.
- **ARIA** supplements HTML: use roles, states, and properties (`aria-label`, `aria-labelledby`, `aria-describedby`, live regions) only when native HTML cannot do the job, and keep states up to date.
- Testers apply POUR as a checklist, combine automated and manual checks, and cite WCAG criteria in defect reports. Techniques are covered in the next lessons today, and pipelines on Friday.

## Additional Resources

- W3C WAI, *WCAG 2 Overview*: https://www.w3.org/WAI/standards-guidelines/wcag/
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2* (the specification): https://www.w3.org/TR/WCAG22/
- W3C WAI, *Understanding WCAG 2.2* and *How to Meet WCAG (Quick Reference)*: https://www.w3.org/WAI/WCAG22/quickref/
- W3C WAI, *WAI-ARIA Authoring Practices Guide*: https://www.w3.org/WAI/ARIA/apg/
- W3C WAI, *Web Accessibility Tutorials*: https://www.w3.org/WAI/tutorials/
- MDN Web Docs, *Accessibility*: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- MDN Web Docs, *ARIA*: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA
- WebAIM, *Contrast Checker*: https://webaim.org/resources/contrastchecker/
