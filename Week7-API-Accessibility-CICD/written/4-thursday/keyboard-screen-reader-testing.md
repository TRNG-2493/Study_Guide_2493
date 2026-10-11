# Keyboard and Screen-Reader Testing

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why manual keyboard and screen-reader testing is necessary even when an automated scan passes.
- Run a structured keyboard-only test using Tab, Shift+Tab, Enter, Space, arrow keys, Esc, and skip links.
- Judge focus order, focus visibility, and spot keyboard traps.
- Use `tabindex="0"` and `tabindex="-1"` correctly and explain why positive values are a defect.
- Check custom widgets (menus, modals, tabs, dropdowns) against the keyboard patterns in the ARIA Authoring Practices Guide (APG).
- Check focus management in modals and single-page applications (SPAs).
- Set up NVDA and VoiceOver, and name the alternatives (JAWS, TalkBack).
- Navigate with a screen reader by headings, landmarks, links, and form fields, and explain browse mode versus focus mode.
- Listen for names, roles, states, headings, landmarks, form errors, live regions, and alt text.
- Write a repeatable manual test script and record findings with steps, expected result, actual result, and the WCAG success criterion.
- Choose sensible browser and screen-reader pairings, and run quick zoom, reflow, and high-contrast checks.

---

## Why This Matters

This is the Week 7 accessibility epic: you are building the skills to make a web product usable by everyone, and to prove it. Earlier in today's lesson you learned the principles (POUR, WCAG, ARIA). This lesson is about the human side of verification.

Imagine you join a QA team on Monday. The team's automated accessibility scan is green, yet a customer who uses a screen reader emails support: "I tapped Checkout and nothing happened. I could not find the payment form." The scan was not wrong about what it checked. It simply could not check that.

Research from accessibility vendors and the W3C consistently suggests that automated tools detect only about **a third to a half** of accessibility problems. Tools are excellent at finding objective, rule-based faults (a missing `alt` attribute, a form field with no label, low colour contrast). They cannot answer questions that need judgement or interaction:

- Can I reach the "Checkout" button with only a keyboard?
- When the payment dialog opens, does focus move into it?
- When I press Esc, does focus come back to where I was?
- Does the screen reader say "Payment, dialog" or just silence?
- Is the alt text *meaningful*, or merely present ("image1")?
- Is the reading order sensible?

A person can answer these in minutes. That is manual testing, and keyboard plus screen reader are the two most valuable manual checks. Keyboard operability matters beyond keyboard users: switch devices, voice control, and screen readers all rely on the same keyboard interface. If the page works with a keyboard, many other technologies work too. If it does not, they all fail together.

Scanning tools, interpreting and writing up defects, MCP-assisted testing, and wiring checks into CI/CD are covered in later sessions. Here, you learn to test by hand and to write results others can act on.

---

## The Concept

### 1. Why Manual Testing Is Necessary

#### 1.1 What automation can and cannot see

Think of automated scanning like a spell-checker. It finds misspelled words, but it cannot tell you whether the essay makes sense. A scanner reads the HTML and applies rules. It does not press keys, listen to speech, or understand intent.

| Automation is good at | Automation cannot judge |
|-----------------------|-------------------------|
| Missing `alt`, missing form labels | Whether alt text is accurate and useful |
| Invalid ARIA attribute names | Whether the ARIA *pattern* behaves correctly when used |
| Colour-contrast ratios for plain text | Contrast on images, gradients, hover/focus states |
| Duplicate IDs, missing page language | Whether focus order is logical |
| Heading element presence | Whether headings describe the content |
| Empty buttons and links | Whether the name is clear and unique in context |

#### 1.2 When to test manually

- After any new component (menu, modal, tabs, carousel) is built.
- Before a release, on the most important user journeys (sign up, log in, search, checkout).
- After a significant redesign or framework change.
- Whenever an automated scan passes but a user reports a problem.

You do not have to test everything with a screen reader every time. A sensible split: keyboard-test every page quickly, screen-reader-test critical journeys and every custom widget.

---

### 2. Keyboard-Only Testing

#### 2.1 The keys you need

Put the mouse aside. Many testers literally move it out of reach so they are not tempted.

| Key | What it should do |
|-----|-------------------|
| **Tab** | Move focus to the next focusable element |
| **Shift + Tab** | Move focus to the previous focusable element |
| **Enter** | Activate links and buttons; submit forms |
| **Space** | Activate buttons; toggle checkboxes; scroll the page if nothing is focused |
| **Arrow keys** | Move *within* a composite widget (radio group, menu, tabs, listbox, slider) |
| **Esc** | Close a dialog, menu, or popup |
| **Home / End** | Jump to first / last item in lists, menus, sliders |
| **Page Up / Page Down** | Scroll, or move by larger steps in a widget |

Rule of thumb: **Tab moves between controls; arrows move inside a control.** A radio group is a single Tab stop. Tab lands on the selected radio, the arrow keys change the choice, and Tab leaves the group.

#### 2.2 What focus is

**Focus** is the element currently receiving keyboard input. The browser shows it with a **focus indicator**, usually an outline ring. Natively focusable elements include links with `href`, `<button>`, form fields, and `<summary>`. A plain `<div>` or `<span>` is not focusable unless you add `tabindex`.

#### 2.3 tabindex: 0, -1, and never positive

```html
<div tabindex="0">Reachable by Tab, in natural DOM order</div>
<div tabindex="-1" id="error-summary">Focusable by script only</div>
<div tabindex="3">Do not do this</div>
```

Line by line:

- `tabindex="0"` puts the element into the normal Tab sequence, in the position where it appears in the HTML. Use it sparingly, for custom widgets that truly need to be focusable and have a proper role.
- `tabindex="-1"` removes the element from the Tab sequence but allows `element.focus()` from JavaScript. This is the tool for *focus management*, such as moving focus to an error summary or a heading after navigation.
- `tabindex="3"` forces this element to be visited before all `tabindex="0"` content, in numeric order. It creates a confusing path that no longer matches the page and is almost impossible to maintain. A positive `tabindex` is a classic defect. The fix is to remove it and fix the DOM order instead.

The best rule: use native elements (`<button>`, `<a href>`, `<input>`) and you rarely need `tabindex` at all.

#### 2.4 Step-by-step keyboard test procedure

Start at the top of the page after a fresh reload.

1. **Press Tab once.** The first stop should be a **skip link** ("Skip to main content") that becomes visible on focus. Press Enter on it. Does focus (and the view) move to the main content? (WCAG 2.4.1 Bypass Blocks.)
2. **Press Tab repeatedly** through the entire page, noting every stop in order.
3. At each stop, ask four questions:
   - *Can I see where focus is?* (2.4.7 Focus Visible)
   - *Does this order follow the visual and reading order?* (2.4.3 Focus Order)
   - *Is every interactive thing reachable?* Links, buttons, form fields, menu triggers, tabs, video controls, cookie banners.
   - *Does the control have a sensible name?* (Confirm later with a screen reader.)
4. **Activate each control** with Enter or Space. It should do the same thing a mouse click does. (2.1.1 Keyboard)
5. **Go backwards** with Shift+Tab to confirm the reverse order is consistent.
6. **Open each widget** (menu, modal, accordion, date picker) and test the keys from section 2.6.
7. **Test forms**: fill in, trigger an error, and correct it using only the keyboard. Is the error reachable? Does focus go to the first error or an error summary?
8. **Look for traps.** Can you always leave a component with Tab, Shift+Tab, or Esc? (2.1.2 No Keyboard Trap)
9. **Look for hidden stops.** Focus should never vanish onto an invisible element such as an off-screen menu or closed dialog.
10. **Repeat the pass at 200 percent zoom** and in a narrow window to catch responsive-menu problems.

#### 2.5 Focus order, visible focus, and traps in depth

**Focus order.** Order follows the DOM, not the screen. If CSS (`order`, `float`, absolute positioning, grid placement) rearranges items visually, keyboard users may bounce around the page. Real-world example: a two-column layout where the sidebar is first in the HTML but appears on the right. Tab visits the sidebar before the main article, which feels random.

**Visible focus.** The most common cause of invisible focus is this CSS:

```css
/* BAD: removes the ring for everyone, no replacement */
button:focus { outline: none; }

/* GOOD: styled ring only for keyboard focus */
button:focus-visible {
  outline: 3px solid #1a5fb4;
  outline-offset: 2px;
}
```

Line by line: the bad rule deletes the browser's default ring, so keyboard users cannot see where they are. The good rule uses `:focus-visible`, which the browser applies when focus came from the keyboard, and draws a thick outline with a small gap. Also check the ring is not hidden by `overflow: hidden` on a parent, and has enough contrast against its background (WCAG 1.4.11 non-text contrast).

**Keyboard traps.** A trap is any place where focus enters but cannot leave. Typical sources: an embedded map or video, a rich-text editor, a third-party chat widget, and a modal with broken focus code. If you ever have to use the mouse to escape, record a failure against 2.1.2.

#### 2.6 Expected keys for custom widgets (APG patterns)

The WAI-ARIA Authoring Practices Guide documents what keys users expect. If a developer builds a custom widget, it must behave like these.

| Widget | Expected keyboard behaviour |
|--------|-----------------------------|
| **Button** | Enter and Space activate |
| **Link** | Enter activates |
| **Checkbox** | Space toggles |
| **Radio group** | Tab enters group; arrows move and select; Tab leaves |
| **Native select / dropdown listbox** | Arrows change option; typing a letter jumps to a matching option; Enter/Esc commits or cancels |
| **Custom dropdown (combobox)** | Down opens list; arrows move; Enter selects; Esc closes; focus stays on the combobox |
| **Tabs** | Tab moves into the tab list (one stop); Left/Right arrows switch tabs; Home/End jump to first/last; Tab moves on into the panel |
| **Menu button + menu** | Enter/Space/Down opens; arrows move; Esc closes and returns focus to the button |
| **Accordion** | Tab moves between headers; Enter/Space expands or collapses |
| **Modal dialog** | Focus moves in on open; Tab cycles inside; Esc closes; focus returns to the trigger |
| **Slider** | Arrows change value; Home/End go to min/max |

A key idea behind tabs, menus, and radio groups is the **roving tabindex**. Only the active item has `tabindex="0"`; the others have `tabindex="-1"`. Arrow keys move the `0` from item to item. This keeps the widget to a single Tab stop so a keyboard user is not forced to press Tab through ten tabs.

```html
<div role="tablist" aria-label="Account sections">
  <button role="tab" aria-selected="true"  tabindex="0"  id="t1" aria-controls="p1">Profile</button>
  <button role="tab" aria-selected="false" tabindex="-1" id="t2" aria-controls="p2">Billing</button>
  <button role="tab" aria-selected="false" tabindex="-1" id="t3" aria-controls="p3">Security</button>
</div>
```

Line by line: `role="tablist"` groups the tabs and `aria-label` names the group. Each button has `role="tab"`. Only "Profile" is `aria-selected="true"` and `tabindex="0"`, so it is the single Tab stop. "Billing" and "Security" are `tabindex="-1"` and are reached with the arrow keys. `aria-controls` links each tab to its panel. When you press Right Arrow, script must move `tabindex="0"` and `aria-selected="true"` to the next tab and call `.focus()` on it. Your test: press Right, then verify both the visual change and (with a screen reader) the announcement "Billing, tab, 2 of 3".

#### 2.7 Focus management in modals and SPAs

**Modal dialogs.** A well-behaved modal does four things:

1. On open, moves focus inside (to the dialog, its heading, or its first control).
2. Keeps Tab and Shift+Tab cycling *within* the dialog (the background is inert).
3. Closes on Esc.
4. On close, returns focus to the element that opened it.

Test script: Tab to "Delete account", press Enter. Where is focus? Press Tab ten times: does focus ever reach the page behind? Press Esc. Where is focus now? If focus lands at the top of the page or on `<body>`, record a failure (2.4.3). Developers often fix this by saving `document.activeElement` before opening and calling `.focus()` on it after closing, and by using the native `<dialog>` element with `showModal()` or the `inert` attribute on the background.

**Single-page applications.** In a classic website, clicking a link loads a new page, resets focus to the top, and the screen reader announces the new title. In an SPA, the framework swaps content without a reload, so none of this happens automatically. Check:

- After a route change, does focus move somewhere sensible (the new `<h1>` with `tabindex="-1"`, or the main region)?
- Is the new page title announced or updated (`document.title`)?
- Is the change announced (for example through a polite live region)?
- Does the browser Back button restore focus sensibly?

Symptom of failure: a screen-reader user clicks "Pricing", hears nothing, and has no idea the content changed.

---

### 3. Screen-Reader Testing

#### 3.1 What a screen reader does

A screen reader converts what is on screen into synthesised speech (and often braille). It does not read pixels. It reads the **accessibility tree**, which the browser builds from your HTML and ARIA. That is why your markup quality directly changes what is said. Users do not read the page top to bottom; they jump around by headings, landmarks, links, and form fields, so those must exist and be meaningful.

#### 3.2 Which screen reader?

| Screen reader | Platform | Cost | Typical browser pairing |
|---------------|----------|------|-------------------------|
| **NVDA** | Windows | Free, open source | Firefox or Chrome |
| **JAWS** | Windows | Commercial (paid) | Chrome or Edge |
| **Narrator** | Windows | Built in | Edge |
| **VoiceOver** | macOS and iOS | Built in | Safari |
| **TalkBack** | Android | Built in | Chrome |

In practice, WebAIM's regular screen-reader user surveys have found JAWS and NVDA the most-used desktop options, with VoiceOver dominant on Apple devices. For this course, use **NVDA with Firefox or Chrome** on Windows, or **VoiceOver with Safari** on macOS. Always record which pair you used, because the same page can be announced differently by different combinations.

**Recommended pairings (a lean test matrix):**

- Windows: NVDA + Firefox (primary), NVDA + Chrome, JAWS + Chrome if licensed.
- macOS: VoiceOver + Safari (primary).
- iOS: VoiceOver + Safari.
- Android: TalkBack + Chrome.

Avoid odd pairs such as VoiceOver with Chrome or NVDA with Safari as your main evidence; they are uncommon and may mislead.

#### 3.3 Setup

**NVDA (Windows)**

1. Download from nvaccess.org and install.
2. Start it (`Ctrl + Alt + N` if you enabled the shortcut). Quit with `Insert + Q`.
3. The **NVDA key** is `Insert` (or `Caps Lock` if you chose the laptop layout).
4. Open **Tools > Speech Viewer** to see a live text log of what is spoken. It is excellent for learning and for attaching evidence to defects.
5. Press `Ctrl` to stop speech instantly.

**VoiceOver (macOS)**

1. Toggle with `Cmd + F5`.
2. The **VO key** is `Control + Option`.
3. Run the built-in VoiceOver tutorial the first time.
4. Turn on the **Caption Panel** in VoiceOver Utility to see spoken text.

**TalkBack (Android):** Settings > Accessibility > TalkBack. Swipe right/left to move between items, double-tap to activate. **JAWS:** commercial; the 40-minute demo mode is enough for practice, and its commands are similar to NVDA's quick-navigation keys.

#### 3.4 Browse mode versus focus mode

This is the concept beginners find most confusing.

- **Browse mode** (NVDA/JAWS): the screen reader owns the keyboard. Letter keys are *navigation shortcuts*: `H` jumps to the next heading, `D` to the next landmark, `K` to the next link. You are moving a virtual cursor through a copy of the page, not typing.
- **Focus mode** (also called forms mode): the keys go straight to the page, so typing works. NVDA switches automatically when you land on a text field, and plays a short sound when the mode changes.

Why it matters to testers: if you press `H` in a text field and it types the letter "h", you are in focus mode, which is correct. If custom widgets do not set proper roles (`role="textbox"`, `role="combobox"`, `role="application"` misused), the screen reader may stay in browse mode and swallow the arrow keys the widget expected. That is a real class of bugs you can only find by listening.

VoiceOver has no browse/focus modes; instead you navigate with VO commands and the **rotor**.

#### 3.5 Essential commands

| Task | NVDA (browse mode) | VoiceOver (macOS) |
|------|--------------------|-------------------|
| Read all from here | `Insert + Down arrow` | `VO + A` |
| Next / previous item | Down / Up arrow | `VO + Right / Left` |
| Next heading | `H` (`Shift + H` previous) | `VO + Cmd + H` |
| Headings by level | `1` to `6` | Rotor > Headings |
| Next landmark | `D` | Rotor > Landmarks |
| Next link | `K` | Rotor > Links |
| Next form field | `F` | Rotor > Form Controls |
| Next button | `B` | `VO + Cmd + J` |
| Next table / cell navigation | `T`; `Ctrl + Alt + arrows` | `VO + Cmd + T`; `VO + arrows` |
| Elements list | `Insert + F7` | Rotor `VO + U` |
| Activate | `Enter` / `Space` | `VO + Space` |
| Stop speech | `Ctrl` | `Control` |
| Switch off/on virtual cursor | `Insert + Space` | not applicable |

Learn five well: Tab, Shift+Tab, `H`, `D`, `F` (or the rotor equivalents).

#### 3.6 What to listen for

For each interactive element a screen reader should announce **name, role, and state or value**.

| Part | Meaning | Example |
|------|---------|---------|
| **Name** | What is it called? | "Search" |
| **Role** | What type of thing? | "button", "link", "edit text", "checkbox" |
| **State / value** | Current condition | "checked", "expanded", "required", "invalid entry", "42" |

Good: "Subscribe to newsletter, checkbox, not checked."
Bad: "Checkbox, not checked." (no name, so the user cannot tell what they are agreeing to).
Bad: "Click here, link." (meaningless out of context).
Bad: "Button." (icon button with no name).

Beyond individual controls, listen for these categories:

- **Names, roles, states:** as above. A toggle that never says "expanded" or "collapsed" is a defect (4.1.2).
- **Headings:** one `h1`, levels that do not skip, and text that describes the section (1.3.1, 2.4.6).
- **Landmarks:** banner, navigation, main, complementary, contentinfo. Multiple regions of the same type need distinct labels ("Primary navigation", "Footer navigation").
- **Form errors:** when you submit with mistakes, is the error spoken? Does it say *which* field and *what to do*? Is the invalid state announced when you return to the field (`aria-invalid`)? (3.3.1, 3.3.3)
- **Live regions:** dynamic updates (cart count, "Saved", search result count) should be announced without moving focus, using `role="status"` or `aria-live="polite"` (4.1.3).
- **Alt text:** informative images are described meaningfully; decorative images (`alt=""`) are skipped; image links say where they go (1.1.1).
- **Page title and language:** announced on load; wrong language produces garbled pronunciation.

#### 3.7 Step-by-step screen-reader test

1. **Page load:** is the title meaningful ("Order history - ShopDemo")?
2. **Read all** from the top. Does the order make sense? Is decorative or duplicate content read? Is visible content missed?
3. **Headings list:** one `h1`, logical nesting.
4. **Landmarks:** present, labelled, and containing all content.
5. **Links list:** each link understandable out of context; repeated "Read more" links distinguishable.
6. **Images:** informative ones described, decorative ones silent.
7. **Forms:** Tab through each field and listen for label, type, required, and instructions. Submit with errors and check the announcement.
8. **Tables:** are row and column headers announced as you move cell to cell?
9. **Dynamic updates:** add to cart, trigger validation, load more results. Is each change announced?
10. **Widgets:** open menus, tabs, dialogs. Is the role announced ("dialog", "tab 2 of 3, selected")? Is the dialog's name spoken on open?
11. **Media:** captions available, controls labelled, no unexpected autoplay audio.

#### 3.8 Common failures with bad and good code

**Failure 1: Div pretending to be a button**

```html
<!-- BAD -->
<div class="btn" onclick="save()">Save</div>

<!-- GOOD -->
<button type="button" onclick="save()">Save</button>
```

The bad version is not focusable, ignores Enter and Space, and a screen reader announces plain text, not "button". The good version fixes all three for free.

**Failure 2: Icon button with no name**

```html
<!-- BAD -->
<button><svg>...</svg></button>

<!-- GOOD -->
<button type="button" aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>
```

`aria-label` supplies the name. `aria-hidden="true"` on the SVG stops the icon itself being announced.

**Failure 3: Unlabelled input and error not announced**

```html
<!-- BAD -->
<input type="email" placeholder="Email">
<span class="error">Invalid</span>

<!-- GOOD -->
<label for="email">Email address</label>
<input id="email" type="email" required aria-describedby="email-err" aria-invalid="true">
<span id="email-err" role="alert">Enter an email like name@example.com</span>
```

Line by line: `<label for="email">` ties the visible text to the input so the name is "Email address". `required` announces "required". `aria-invalid="true"` announces "invalid entry". `aria-describedby` makes the error text read after the field. `role="alert"` makes the message spoken immediately when it appears. A placeholder alone is not a label, since it disappears and is not reliably announced.

**Failure 4: Expandable menu with no state**

```html
<!-- BAD -->
<button onclick="toggle()">Products</button>

<!-- GOOD -->
<button type="button" aria-expanded="false" aria-controls="menu1">Products</button>
<ul id="menu1" hidden>...</ul>
```

Script must flip `aria-expanded` to `"true"` and remove `hidden` when opened. The screen reader then says "Products, button, collapsed" and "expanded".

#### 3.9 Testing with zoom, reflow, and high contrast (brief)

- **Zoom and reflow (1.4.4, 1.4.10):** zoom the browser to 200 percent, then 400 percent (equivalent to a 320 CSS pixel wide window). Content should reflow into one column with no horizontal scrolling, no clipped text, and no overlapping controls. Check that menus still open and focus is still visible.
- **High contrast / forced colours:** on Windows turn on a Contrast theme (Settings > Accessibility > Contrast themes) and reload. Icons, borders, and focus rings must still be visible. Backgrounds used as the only indicator of state often disappear.
- **Colour only:** confirm errors and status are not shown by colour alone (1.4.1).

---

### 4. Recording Findings and a Repeatable Checklist

#### 4.1 The repeatable checklist

Run the same list on every page so results are comparable.

Keyboard:
- [ ] Skip link present, visible on focus, works
- [ ] Every interactive element reachable by Tab
- [ ] Focus always visible and has good contrast
- [ ] Focus order matches visual order
- [ ] No keyboard traps
- [ ] Widgets follow APG key patterns
- [ ] Modals: focus in, contained, Esc closes, focus returns
- [ ] Forms completable and errors reachable
- [ ] No hover-only content

Screen reader:
- [ ] Title meaningful, language correct
- [ ] One `h1`, logical headings
- [ ] Landmarks present and labelled
- [ ] Links meaningful out of context
- [ ] Images: alt correct or empty when decorative
- [ ] Controls announce name, role, state
- [ ] Form labels, required, and errors announced
- [ ] Dynamic updates announced
- [ ] Tables have headers announced

Display:
- [ ] 200 percent zoom and 320 px reflow work
- [ ] High contrast mode usable

#### 4.2 Test script template

| # | Page / component | Test step | Expected | Actual | Pass / Fail | WCAG SC | Environment |
|---|------------------|-----------|----------|--------|-------------|---------|-------------|
| 1 | Home | Press Tab once after load | Skip link appears | First stop is logo | Fail | 2.4.1 | Chrome 130, Windows 11 |
| 2 | Login | Tab to Email field with NVDA | "Email address, edit, required" | "Edit, blank" | Fail | 1.3.1, 4.1.2 | NVDA 2025.x + Firefox |
| 3 | Cart | Add item | "Item added" spoken | Silence | Fail | 4.1.3 | NVDA + Firefox |
| 4 | Delete dialog | Press Esc | Closes, focus on trigger | Focus on body | Fail | 2.4.3 | Chrome |

#### 4.3 Writing a finding

A good finding lets a developer reproduce the problem without asking you anything. Include:

- **Title:** specific ("Delete dialog does not return focus to trigger on Esc").
- **Steps to reproduce:** numbered, starting from a URL.
- **Expected result:** what should happen, ideally citing the APG pattern.
- **Actual result:** what you saw or heard, quoting the screen-reader output exactly.
- **WCAG success criterion and level:** for example 2.4.3 Focus Order (A).
- **Environment:** OS, browser, screen reader, versions.
- **Evidence:** screenshot, short recording, or Speech Viewer text.
- **Severity:** does it block a task (high) or merely annoy (low)?

Example:

> **Title:** Newsletter checkbox has no accessible name
> **Steps:** 1. Open /signup. 2. Start NVDA. 3. Press F until the checkbox is reached.
> **Expected:** "Subscribe to newsletter, checkbox, not checked."
> **Actual:** "Checkbox, not checked."
> **WCAG:** 4.1.2 Name, Role, Value (A); 1.3.1 Info and Relationships (A)
> **Environment:** Windows 11, NVDA + Firefox.

Detailed defect analysis and prioritisation are covered in a later session; for now, aim for clear, reproducible notes.

Automated keyboard checks (for example with Playwright) are possible and are covered with the automation material later in the week; they supplement but never replace the manual passes above.

---

### 5. Practice Exercises

Use any NVDA or VoiceOver setup. The W3C "Before and After Demonstration" site is a deliberately inaccessible page (before) with a fixed version (after).

#### Exercise 1: Keyboard-only walkthrough

Open `https://www.w3.org/WAI/demos/bad/before/home.html`. Without the mouse, Tab through the page and complete a script table of at least six steps.

**Solution (model script):**

| # | Step | Expected | Likely actual | Result | WCAG |
|---|------|----------|---------------|--------|------|
| 1 | Reload, press Tab once | Skip link appears | No skip link; focus goes to first nav item | Fail | 2.4.1 |
| 2 | Tab through navigation | Ring visible at each stop | Ring weak or missing on some items | Fail | 2.4.7 |
| 3 | Continue Tab to main content | Order matches visual | Order may differ from layout | Note | 2.4.3 |
| 4 | Press Enter on a nav link | Page loads | Works | Pass | 2.1.1 |
| 5 | Tab to a form field | Reachable and labelled | Field reachable, label weak | Note | 3.3.2 |
| 6 | Shift+Tab backwards | Reverse order consistent | Consistent | Pass | 2.4.3 |

#### Exercise 2: Modal dialog test script

Write a test script for a "Delete account" modal on any site you have access to (or a sample from the APG dialog example at `https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/`).

**Solution:**

| # | Step | Expected | Pass criteria | WCAG |
|---|------|----------|---------------|------|
| 1 | Tab to "Delete account" trigger | Visible focus on trigger | Ring visible | 2.4.7 |
| 2 | Press Enter | Dialog opens; focus moves inside | Focus on dialog or first control | 2.4.3 |
| 3 | Press Tab 10 times | Focus cycles inside dialog only | Never reaches background | 2.1.2, 2.4.3 |
| 4 | Press Shift+Tab from first control | Wraps to last control | Stays inside | 2.4.3 |
| 5 | Screen reader: on open | Hears dialog name and role | "Delete account, dialog" | 4.1.2 |
| 6 | Press Esc | Dialog closes | Closed | 2.1.1 |
| 7 | Check focus | Returned to trigger | Focus on "Delete account" button | 2.4.3 |

Record Pass or Fail per step with browser and screen reader.

#### Exercise 3: Screen-reader structure audit

Start NVDA (or VoiceOver) on `https://www.w3.org/WAI/demos/bad/before/home.html` and then `https://www.w3.org/WAI/demos/bad/after/home.html`. Open the headings list, landmarks, and links list on each. Describe three differences.

**Solution (typical findings):**

1. Headings: the "before" page has poor or missing heading structure, so the headings list is short or illogical; the "after" page has a clear `h1` and nested headings (1.3.1, 2.4.6).
2. Landmarks: "before" has few or none, so `D` jumps nowhere; "after" exposes banner, navigation, main, and footer (1.3.1, 2.4.1).
3. Images and links: "before" images may be read as file names and links as "click here"; "after" has descriptive alt text and meaningful link text (1.1.1, 2.4.4).

Write each as: element, what you heard (before), what you heard (after), and the SC.

---

### 6. Quiz

**Q1.** Roughly what share of accessibility issues can automated tools detect, and why does that justify manual testing?

**Q2.** A modal opens, but pressing Tab moves focus through the page behind it. Name two defects and one WCAG success criterion.

**Q3.** What is the difference between `tabindex="0"`, `tabindex="-1"`, and `tabindex="3"`?

**Q4.** In NVDA, you press `H` in a text input and the letter "h" appears. Is that a bug? Explain browse mode and focus mode.

**Q5.** A screen reader says only "Button" for a magnifier icon. What is wrong, and how do you fix it?

**Answers**

1. About a third to a half. Tools check markup rules, not usability, order, or what is actually announced, so interaction and judgement need a human.
2. Focus is not contained in the dialog (and was probably not moved into it on open); the background is not inert. Relevant criteria include 2.4.3 Focus Order and 2.1.1 Keyboard (and 4.1.2 for the dialog role).
3. `0` adds the element to the natural Tab order; `-1` allows script focus only and is not a Tab stop; `3` forces an artificial order and should be avoided.
4. Not a bug. In a text field NVDA is in focus mode so keys type text. In browse mode, letter keys are navigation shortcuts. NVDA switches automatically.
5. The icon button has no accessible name (4.1.2). Add `aria-label="Search"` (or visually hidden text) and hide the decorative SVG with `aria-hidden="true"`.

---

### 7. Glossary

#### Accessibility tree
The browser's accessibility view of the page, built from the DOM and ARIA. Screen readers read this, not the pixels.

#### APG
WAI-ARIA Authoring Practices Guide: W3C documentation of expected roles, states, and keyboard patterns for widgets.

#### Browse mode / focus mode
NVDA/JAWS modes: browse mode uses letter keys for navigation; focus mode sends keys to the page for typing.

#### Focus indicator
The visible outline showing which element has keyboard focus.

#### Keyboard trap
A place where keyboard focus can enter but not leave (WCAG 2.1.2).

#### Landmark
A page region (banner, navigation, main, contentinfo) that screen-reader users jump between.

#### Live region
An element (`aria-live`, `role="status"`, `role="alert"`) whose changes are announced automatically.

#### Roving tabindex
A technique where only the active item in a widget has `tabindex="0"`, and arrows move it.

#### Rotor
VoiceOver's list-based navigator for headings, links, landmarks, and form controls.

#### Skip link
A first-in-order link that lets users bypass repeated navigation and jump to main content.

#### Speech Viewer
NVDA tool that displays spoken output as text, useful for evidence.

---

## Summary

- Automation finds roughly a third to a half of issues, so keyboard and screen-reader testing are essential for anything involving interaction, order, and announcement.
- Keyboard testing: Tab and Shift+Tab through everything, check visible focus, logical order, skip links, no traps, Enter/Space activation, and APG key patterns for menus, tabs, dropdowns, and modals.
- Use `tabindex="0"` sparingly, `-1` for script-managed focus, and never positive values. Prefer native elements.
- Modals and SPAs need deliberate focus management: move in, contain, return, and announce route changes.
- Screen readers (NVDA, JAWS, VoiceOver, TalkBack) read the accessibility tree. Learn browse versus focus mode, headings, landmarks, and the rotor or elements list.
- Listen for name, role, state, headings, landmarks, form errors, live regions, and alt text.
- Use a repeatable checklist, record findings with steps, expected, actual, WCAG criterion, and environment, and use sensible browser and screen-reader pairings.
- Check zoom, reflow, and high-contrast modes briefly on every page.

## Additional Resources

- WebAIM, *Keyboard Accessibility*: https://webaim.org/techniques/keyboard/
- WebAIM, *Using NVDA to Evaluate Web Accessibility*: https://webaim.org/articles/nvda/
- WebAIM, *Screen Reader User Survey*: https://webaim.org/projects/screenreadersurvey/
- W3C, *WAI-ARIA Authoring Practices Guide*: https://www.w3.org/WAI/ARIA/apg/
- W3C WAI, *Before and After Demonstration*: https://www.w3.org/WAI/demos/bad/
- NV Access, *NVDA User Guide*: https://www.nvaccess.org/files/nvda/documentation/userGuide.html
- Apple, *VoiceOver User Guide for Mac*: https://support.apple.com/guide/voiceover/welcome/mac
