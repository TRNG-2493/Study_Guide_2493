# Daily Knowledge Check: Week 7 Thursday - Accessibility & MCP Testing

Test yourself on today's four lessons: accessibility principles (POUR, WCAG, ARIA), keyboard and screen-reader testing, automated scanning with axe, accessibility defect analysis, and the introduction to MCP testing. Try each question before opening the solution. Part 3 uses real contrast calculations and a FastMCP server that was run to confirm the output.

---

## Part 1: Multiple Choice

### 1. What do the letters of POUR stand for in WCAG?

- [ ] A) Perceivable, Optional, Usable, Reliable
- [ ] B) Perceivable, Operable, Understandable, Robust
- [ ] C) Programmable, Operable, Universal, Responsive
- [ ] D) Predictable, Open, Understandable, Readable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Perceivable, Operable, Understandable, Robust

**Explanation:** WCAG has four principles: Perceivable, Operable, Understandable and Robust. Every success criterion belongs to exactly one of them.

**Why the others are wrong:**

- **A)** Optional, Usable and Reliable are not WCAG principle names.
- **C)** Programmable, Universal and Responsive are not WCAG principle names.
- **D)** Predictable, Open and Readable are not WCAG principle names; the P is Perceivable and the R is Robust.
</details>

### 2. A tester reads the criterion number 1.4.3 (Contrast Minimum). What do the three numbers mean?

- [ ] A) Level 1, version 4, rule 3
- [ ] B) WCAG version 1.4, revision 3
- [ ] C) Priority 1, severity 4, rule 3
- [ ] D) Principle 1 (Perceivable), guideline 4 (Distinguishable), criterion 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Principle 1 (Perceivable), guideline 4 (Distinguishable), criterion 3

**Explanation:** Success criteria are numbered principle.guideline.criterion, so 1.4.3 sits under Perceivable, in the Distinguishable guideline.

**Why the others are wrong:**

- **A)** Conformance levels are A, AA and AAA, not numbers, and the number is not a rule count.
- **B)** WCAG versions are 2.0, 2.1 and 2.2; the number is not a version.
- **C)** Priority and severity are defect-tracking fields, not part of a criterion number.
</details>

### 3. A client contract demands 'WCAG 2.2 AA conformance'. What must a page meet to claim it?

- [ ] A) All Level A criteria and all Level AA criteria
- [ ] B) Only the Level AA criteria
- [ ] C) All Level A, AA and AAA criteria
- [ ] D) Most Level AA criteria, with Level A optional

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) All Level A criteria and all Level AA criteria

**Explanation:** AA conformance is cumulative: every Level A and every Level AA criterion must be met. Partial conformance is not AA.

**Why the others are wrong:**

- **B)** Level A is the mandatory baseline, so it cannot be skipped.
- **C)** AAA is aspirational and is not achievable for all content, so it is not required for an AA claim.
- **D)** There is no 'most criteria' option; partial conformance is not AA.
</details>

### 4. What is the minimum contrast ratio for normal-size text under WCAG 1.4.3 (Level AA)?

- [ ] A) 3:1
- [ ] B) 7:1
- [ ] C) 4.5:1
- [ ] D) 2.85:1

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 4.5:1

**Explanation:** Normal text needs at least 4.5:1. Large text (18pt, or 14pt bold) needs only 3:1.

**Why the others are wrong:**

- **A)** 3:1 applies to large text (and, under 1.4.11, to meaningful UI parts such as input borders).
- **B)** 7:1 is the Level AAA enhanced contrast of 1.4.6.
- **D)** 2.85:1 is the ratio of #999999 on white in the lesson and is an example of a failure.
</details>

### 5. WCAG 2.2 added SC 2.5.8 Target Size (Minimum). What does it require at Level AA?

- [ ] A) Pointer targets of at least 44 by 44 CSS pixels with no exceptions
- [ ] B) Pointer targets of at least 16 by 16 CSS pixels
- [ ] C) Pointer targets of at least 24 by 24 CSS pixels, with exceptions such as inline links
- [ ] D) Pointer targets of at least 24 by 24 CSS pixels, but only at Level AAA

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Pointer targets of at least 24 by 24 CSS pixels, with exceptions such as inline links

**Explanation:** 2.5.8 is a Level AA criterion new in 2.2 requiring 24 by 24 CSS pixels (exceptions include inline links and enough spacing). 44 by 44 is only a comfortable aim.

**Why the others are wrong:**

- **A)** 44 by 44 is described as a comfortable aim, not the AA minimum, and the criterion has exceptions.
- **B)** A 16px icon button is the lesson's example of a failure of 2.5.8.
- **D)** The criterion is Level AA, not AAA.
</details>

### 6. A developer wants a clickable `<div role="button">` instead of a `<button>` because it is easier to style. Which statement matches the first rule of ARIA?

- [ ] A) Use the native `<button>`; no ARIA is better than bad ARIA
- [ ] B) Keep the div, because ARIA roles always make a control accessible
- [ ] C) Keep the div and add `aria-hidden="true"` so only the role is exposed
- [ ] D) Keep the div, because ARIA is always better than native HTML

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Use the native `<button>`; no ARIA is better than bad ARIA

**Explanation:** If a native element already has the needed semantics and behaviour, use it. `role="button"` on a div announces 'button' but the div is still not focusable and ignores Enter and Space.

**Why the others are wrong:**

- **B)** A role only changes what is announced; it adds no keyboard behaviour or focusability.
- **C)** `aria-hidden="true"` would hide the control from assistive technology, and must never be put on focusable elements.
- **D)** ARIA only supplements HTML; it is not better when a native element fits.
</details>

### 7. A form field has `tabindex="3"`. How should a tester log this?

- [ ] A) Correct practice: it moves the field to the front of the Tab order, which helps users
- [ ] B) Not a defect: tabindex is ignored on form fields
- [ ] C) A defect only if the field is a div
- [ ] D) A defect: positive tabindex creates a confusing focus order; remove it and fix the DOM order

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A defect: positive tabindex creates a confusing focus order; remove it and fix the DOM order

**Explanation:** A positive tabindex forces numeric visiting order before all `tabindex="0"` content, so the path no longer matches the page. The fix is to remove it and fix the DOM order.

**Why the others are wrong:**

- **A)** The jump ahead of other content is exactly what makes the path confusing and unmaintainable.
- **B)** tabindex is honoured on any focusable element, and a positive value changes the order.
- **C)** The problem is the positive value itself, not the element type.
</details>

### 8. What does `tabindex="-1"` do?

- [ ] A) Puts the element first in the Tab sequence
- [ ] B) Removes the element from the Tab sequence but allows `element.focus()` from script
- [ ] C) Makes the element unfocusable even by script
- [ ] D) Adds the element to the Tab sequence in DOM order

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Removes the element from the Tab sequence but allows `element.focus()` from script

**Explanation:** `-1` is the tool for focus management, such as moving focus to an error summary or a heading after navigation.

**Why the others are wrong:**

- **A)** Putting an element first is what a positive tabindex does.
- **C)** Script focus still works; that is the whole point of -1.
- **D)** Adding it in DOM order is the behaviour of `tabindex="0"`.
</details>

### 9. A keyboard tester reaches a radio group with three options. What is the expected behaviour?

- [ ] A) Tab lands on the selected radio, arrow keys change the choice, and Tab leaves the group
- [ ] B) Tab moves through each radio button in turn
- [ ] C) Only the Space key can move between the radios
- [ ] D) Arrow keys leave the group and move to the next control

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Tab lands on the selected radio, arrow keys change the choice, and Tab leaves the group

**Explanation:** Tab moves between controls and arrows move inside a control; a radio group is a single Tab stop.

**Why the others are wrong:**

- **B)** That would make the group three Tab stops instead of one.
- **C)** Space toggles a checkbox or activates a button; arrows move inside a radio group.
- **D)** Arrows move within the group; Tab is what leaves it.
</details>

### 10. In NVDA browse mode, a tester presses H on a page. What happens?

- [ ] A) The letter h is typed into the page
- [ ] B) NVDA switches off and the page takes over the keyboard
- [ ] C) The virtual cursor jumps to the next heading
- [ ] D) Help opens in the browser

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The virtual cursor jumps to the next heading

**Explanation:** In browse mode the screen reader owns the keyboard and letter keys are navigation shortcuts: H for headings, D for landmarks, K for links.

**Why the others are wrong:**

- **A)** Typing happens in focus mode, for example in a text field.
- **B)** Insert+Space toggles the virtual cursor; H does not.
- **D)** H is a quick-navigation key, not a help key.
</details>

### 11. What does a screen reader actually read when it speaks a page?

- [ ] A) The pixels on the screen
- [ ] B) The accessibility tree the browser builds from HTML and ARIA
- [ ] C) The CSS file only
- [ ] D) The page's JavaScript source

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The accessibility tree the browser builds from HTML and ARIA

**Explanation:** A screen reader does not read pixels; it reads the accessibility tree, so markup quality directly changes what is said.

**Why the others are wrong:**

- **A)** It does not do image recognition of the screen.
- **C)** CSS styling is not what is spoken; the tree comes from HTML and ARIA.
- **D)** The tree is built from the rendered DOM and ARIA, not from script source.
</details>

### 12. A screen reader says only 'Checkbox, not checked.' What is missing, and why is it a defect?

- [ ] A) The role: a checkbox is announced without any type
- [ ] B) The state: the user cannot tell whether it is checked
- [ ] C) The value: a number must always be spoken
- [ ] D) The name: the user cannot tell what they are agreeing to

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The name: the user cannot tell what they are agreeing to

**Explanation:** A control should announce name, role and state or value. Here role and state are spoken, but the name is missing.

**Why the others are wrong:**

- **A)** 'Checkbox' is the role and is already spoken.
- **B)** 'Not checked' is the state and is already spoken.
- **C)** A value applies to controls such as sliders; a checkbox needs a name instead.
</details>

### 13. In an axe result, what does an entry in `incomplete` mean?

- [ ] A) A rule definitely failed and must be fixed
- [ ] B) axe could not decide, so a human must review it
- [ ] C) The rule passed on every element
- [ ] D) The rule had nothing to check on this page

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) axe could not decide, so a human must review it

**Explanation:** `incomplete` holds items axe could not decide (for example text over a background image). They are reviewed manually, and the build should not be failed on them.

**Why the others are wrong:**

- **A)** Definite failures are in `violations`.
- **C)** Those are in `passes`.
- **D)** Those are in `inapplicable`.
</details>

### 14. `results.violations_count` is 5 in a Python axe scan. What does that number count?

- [ ] A) Failing elements (nodes)
- [ ] B) Items in `incomplete`
- [ ] C) Pages scanned
- [ ] D) Failed rules, not failing elements

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Failed rules, not failing elements

**Explanation:** The number of violations is the number of rules failed. One rule can hide many nodes, so report both rule count and element count.

**Why the others are wrong:**

- **A)** Elements are counted in each rule's `nodes` list.
- **B)** `incomplete` is a separate bucket.
- **C)** A single run scans one page.
</details>

### 15. A team runs axe with `runOnly` tags set to just `["wcag22aa"]` and sees almost no violations. What went wrong?

- [ ] A) The tags are not cumulative: `wcag22aa` holds only rules added in 2.2, so the 2.0 and 2.1 rules were skipped
- [ ] B) `wcag22aa` is an invalid tag and axe ignored the option
- [ ] C) `wcag22aa` includes every rule from 2.0, 2.1 and 2.2, so the page really is nearly perfect
- [ ] D) `runOnly` only works with `best-practice` tags

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The tags are not cumulative: `wcag22aa` holds only rules added in 2.2, so the 2.0 and 2.1 rules were skipped

**Explanation:** List `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa` and `wcag22aa` together. Requesting only the 2.2 tag gives a misleadingly empty result.

**Why the others are wrong:**

- **B)** It is a valid tag; it simply covers only the 2.2 additions.
- **C)** That is the misconception: the tags are not cumulative.
- **D)** `runOnly` with `type: "tag"` accepts any tag, including WCAG tags.
</details>

### 16. A page scores 92 in the Lighthouse accessibility audit. What can you conclude?

- [ ] A) The page is 92% accessible to real users
- [ ] B) The page meets WCAG AA
- [ ] C) Most weighted automated audits passed; it does not mean the page is 92% accessible
- [ ] D) Only 8% of users face barriers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Most weighted automated audits passed; it does not mean the page is 92% accessible

**Explanation:** The score is a weighted average of passed automated audits, with no partial credit. A 100 would still only mean no automated audit failed.

**Why the others are wrong:**

- **A)** The score is not a measure of user accessibility.
- **B)** A score is not a conformance claim; manual checks are still needed.
- **D)** The score says nothing about the share of users affected.
</details>

### 17. Which defect meets the definition of a Blocker severity?

- [ ] A) Heading levels skip from h2 to h4 on one article
- [ ] B) Body text has a contrast ratio of 3.5:1 but is still readable
- [ ] C) Checkout 'Pay now' is a div, so keyboard and screen-reader users cannot buy and have no workaround
- [ ] D) A decorative image has a long alt text

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Checkout 'Pay now' is a div, so keyboard and screen-reader users cannot buy and have no workaround

**Explanation:** A Blocker means a user group cannot complete a core task and there is no workaround, so release should not go ahead.

**Why the others are wrong:**

- **A)** A skipped heading level is Minor in the lesson's ShopDemo rating, because the page is still navigable.
- **B)** Contrast of 3.5:1 on body text is listed as Major, because a workaround exists.
- **D)** A decorative image with a long alt is Minor.
</details>

### 18. A one-line CSS fix would restore a missing focus ring (SC 2.4.7), and the team asks to rate it as Minor because it is cheap. What is the correct approach?

- [ ] A) Keep the severity based on user impact, and use the low effort to raise its priority as a quick win
- [ ] B) Lower the severity because effort reduces severity
- [ ] C) Merge severity and priority into one field
- [ ] D) Close it as won't fix because it is cheap

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Keep the severity based on user impact, and use the low effort to raise its priority as a quick win

**Explanation:** Severity describes harm to users; priority is the business order of fixing. Effort matters for priority but never for severity.

**Why the others are wrong:**

- **B)** Effort never changes severity.
- **C)** The lesson says to keep both fields because they are different.
- **D)** A cheap fix is a reason to schedule it sooner, not to drop it.
</details>

### 19. An axe scan shows two `color-contrast` failures: one from a global grey `.hint` style and one from a white-on-yellow banner in another stylesheet. How many tickets?

- [ ] A) One ticket, because the rule id is the same
- [ ] B) One ticket per node
- [ ] C) No tickets until axe impact is critical
- [ ] D) Two tickets, because the same rule has different causes and different fixes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Two tickets, because the same rule has different causes and different fixes

**Explanation:** Same rule, same cause, same fix is one ticket; same rule with different causes is separate tickets.

**Why the others are wrong:**

- **A)** Rule id alone does not decide; the cause and the fix do.
- **B)** Per-node tickets flood the tracker and are listed as a common mistake.
- **C)** Impact is only a starting point and is not a precondition for logging a defect.
</details>

### 20. During a modal test, after pressing Esc, focus lands on the `<body>` instead of the button that opened the modal. How is this classified?

- [ ] A) Root-cause category: contrast / design; SC 1.4.3
- [ ] B) Root-cause category: focus management; recorded against SC 2.4.3
- [ ] C) Root-cause category: content / authoring; SC 1.1.1
- [ ] D) Root-cause category: naming; SC 2.5.3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Root-cause category: focus management; recorded against SC 2.4.3

**Explanation:** A modal should return focus to its trigger on close. Focus landing on the body is recorded as a failure of 2.4.3, in the focus-management category.

**Why the others are wrong:**

- **A)** Contrast concerns colour ratios, not focus movement.
- **C)** Content / authoring covers vague links, skipped headings and missing alt text.
- **D)** Naming covers missing or mismatched accessible names.
</details>

### 21. In MCP, which role holds exactly one connection to one server?

- [ ] A) The client, a component inside the host
- [ ] B) The host, which holds one connection to every server
- [ ] C) The server, which holds one connection per host
- [ ] D) The Inspector, which connects every client

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The client, a component inside the host

**Explanation:** The host is the AI application; it contains one client per server. In your tests you play the client.

**Why the others are wrong:**

- **B)** The host owns several clients, one per server.
- **C)** A server exposes capabilities; it is not the connection holder in this model.
- **D)** The Inspector is a testing tool, not an MCP role.
</details>

### 22. What is the correct order of an MCP connection lifecycle?

- [ ] A) notifications/initialized, initialize, tools/list, shutdown
- [ ] B) tools/list, initialize, operation, notifications/initialized
- [ ] C) initialize request, initialize response with capabilities, notifications/initialized, operation, shutdown
- [ ] D) initialize request, operation, notifications/initialized, shutdown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) initialize request, initialize response with capabilities, notifications/initialized, operation, shutdown

**Explanation:** The client sends `initialize`, the server answers with its capabilities (capability negotiation), the client sends `notifications/initialized`, and only then does normal traffic flow.

**Why the others are wrong:**

- **A)** The handshake must start with `initialize`.
- **B)** `tools/list` is normal traffic and must wait for the handshake.
- **D)** Normal operation is only allowed after `notifications/initialized`.
</details>

### 23. Which MCP method reads a resource such as `greeting://Ann`?

- [ ] A) `tools/call`
- [ ] B) `resources/read`
- [ ] C) `prompts/get`
- [ ] D) `resources/call`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `resources/read`

**Explanation:** Resources are application-controlled readable data identified by URI; `resources/list` lists them and `resources/read` returns their contents.

**Why the others are wrong:**

- **A)** `tools/call` runs a tool.
- **C)** `prompts/get` returns a prompt's messages.
- **D)** `resources/call` is not an MCP method named in the lesson.
</details>

### 24. Why must a stdio MCP server never `print()` to stdout?

- [ ] A) stdout is reserved for the Inspector UI
- [ ] B) Python buffers stdout, so the text would appear late
- [ ] C) print() raises an exception inside FastMCP
- [ ] D) stdout carries the JSON-RPC messages, so extra text corrupts the stream; log to stderr instead

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) stdout carries the JSON-RPC messages, so extra text corrupts the stream; log to stderr instead

**Explanation:** With stdio, messages travel over stdin/stdout, one JSON message per line. Any other text lands in the protocol stream.

**Why the others are wrong:**

- **A)** stdout is the protocol channel, not a UI channel.
- **B)** Buffering is not the issue; the corruption is.
- **C)** print() does not raise; it silently breaks the message stream.
</details>

### 25. A bug: the `add` function returns `a - b`. Which test layer catches it cheapest?

- [ ] A) Layer 5: a real stdio end-to-end test
- [ ] B) Layer 1: a plain unit test that calls the Python function directly, with no MCP client
- [ ] C) Layer 4: a resource and prompt test
- [ ] D) The Inspector only, never automated

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Layer 1: a plain unit test that calls the Python function directly, with no MCP client

**Explanation:** Match each bug to the cheapest layer. `@mcp.tool()` returns your original function, so it can be unit tested without MCP at all.

**Why the others are wrong:**

- **A)** Layer 5 is slower and is kept for proving the real startup path.
- **C)** Resource and prompt tests check `resources/read` and `prompts/get` output.
- **D)** Anything checked by hand twice in the Inspector should become a pytest test.
</details>

---

## Part 2: True/False

### 26. True or False: Automated accessibility scanners catch all accessibility issues.

- [ ] A) False
- [ ] B) True

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) False

**Explanation:** Scanners catch only objective, machine-checkable problems. They cannot judge whether alt text is meaningful, whether focus order makes sense or whether a widget is usable.
- **Why B) is wrong:** The claim is the misconception: a clean scan means no machine-detectable failures, not 'accessible'.
</details>

### 27. True or False: ARIA is always better than native HTML for accessibility.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The first rule of ARIA says to use a native element when one fits, because no ARIA is better than bad ARIA.
- **Why A) is wrong:** Native elements bring semantics, focus and keyboard behaviour for free; ARIA only supplements them.
</details>

### 28. True or False: A page with zero axe violations is therefore accessible to screen-reader users.

- [ ] A) False
- [ ] B) True

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) False

**Explanation:** Zero violations only means no automated rule failed. `alt="image1"` passes `image-alt` and is useless, and focus order and announcements need manual testing.
- **Why B) is wrong:** A clean scan is not proof of accessibility.
</details>

### 29. True or False: An informative image needs a meaningful `alt`, while a purely decorative image should use `alt=""` so screen readers skip it.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Informative images need meaningful alt text; decorative images use an empty alt and are skipped.
- **Why B) is wrong:** Both halves of the statement match the lesson's guidance on 1.1.1.
</details>

### 30. True or False: A Lighthouse accessibility score of 100 proves the page is accessible.

- [ ] A) False
- [ ] B) True

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) False

**Explanation:** A 100 only means no automated audit failed; manual checks still apply and the score is not a certificate.
- **Why B) is wrong:** The score is a weighted average of automated audits.
</details>

### 31. True or False: `button:focus { outline: none; }` with no replacement style fails SC 2.4.7 Focus Visible.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Removing the only visual cue leaves keyboard users unable to see where they are. Use `:focus-visible` with a clear outline instead.
- **Why B) is wrong:** The rule removes the focus indicator entirely, which is exactly the failure.
</details>

### 32. True or False: In JSON-RPC, a notification has no `id`, and the receiver must not reply to it.

- [ ] A) False
- [ ] B) True

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) True

**Explanation:** `notifications/initialized` is an example. Waiting for a reply to a notification is a common mistake.
- **Why A) is wrong:** Only requests carry an `id` and expect a response.
</details>

### 33. True or False: If a FastMCP tool raises an exception, the server crashes and the connection must be restarted.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** FastMCP catches the exception and returns a result with `isError: true` and the message in `content`; the server stays alive and a good call can follow.
- **Why A) is wrong:** The tool-error design is specifically to keep the server usable after a failure.
</details>

### 34. True or False: In the v2 Python SDK, a raising tool returns exactly the same error text as in SDK 1.x, so error-message assertions are safe to keep.

- [ ] A) False
- [ ] B) True

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) False

**Explanation:** In the lesson's check, v2 returned a generic 'Error executing tool divide' message instead of the original text. Assert on `isError` first and re-check text on upgrade.
- **Why B) is wrong:** Error text can differ between SDK versions.
</details>

### 35. True or False: Because a fix takes only one hour, a Blocker defect can be downgraded to Minor.

- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Severity reflects impact on users; effort influences priority only.
- **Why A) is wrong:** The fix cost is irrelevant to how badly users are blocked.
</details>

### 36. True or False: A scenario you check twice by hand in the MCP Inspector should become an automated pytest test.

- [ ] A) False
- [ ] B) True

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) True

**Explanation:** The Inspector is for exploring a new server and reproducing bugs; repeated manual checks should be automated.
- **Why A) is wrong:** The lesson advises automating anything you check by hand twice.
</details>

---

## Part 3: Code and Markup Prediction

### 37. axe scans this markup. Which rule fires, and which fix gives a meaningful result?

```html
<img src="sales-chart.png">
```

- [ ] A) `image-alt`; add `alt="image1"`, which satisfies the rule and helps users
- [ ] B) `image-alt`; add `alt="Bar chart of monthly sales"`
- [ ] C) `label`; wrap the image in a `<label>`
- [ ] D) `image-alt`; add `alt=""`, because the chart is informative

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `image-alt`; add `alt="Bar chart of monthly sales"`

**Explanation:** A missing text alternative on an image is the `image-alt` rule (SC 1.1.1, Level A). The alt must describe the content; an empty alt is for decorative images.

**Why the others are wrong:**

- **A)** `alt="image1"` passes the rule but is completely useless, so automation cannot tell meaning.
- **C)** `label` is about form inputs, not images.
- **D)** An empty alt makes screen readers skip an informative chart.
</details>

### 38. A sign-up form uses this input. axe reports rule `label` (tags `wcag2a`, `wcag412`, `wcag131`). Which fix is correct?

```html
<form>
  <input id="name" type="text">
</form>
```

- [ ] A) Add `tabindex="0"` to the input
- [ ] B) Add `aria-hidden="true"` to the input
- [ ] C) Add `role="textbox"` to the input
- [ ] D) Add `<label for="name">Full name</label>` so the input gets an accessible name

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Add `<label for="name">Full name</label>` so the input gets an accessible name

**Explanation:** A native label gives the input a name. NVDA would otherwise read something like 'edit, blank'.

**Why the others are wrong:**

- **A)** The input is already focusable; tabindex does not name it.
- **B)** `aria-hidden="true"` on a focusable element is forbidden and hides the field.
- **C)** The input already has a textbox role; the missing piece is the name.
</details>

### 39. What happens for a keyboard and a screen-reader user with this control?

```html
<div class="btn" onclick="pay()">Pay now</div>
```

- [ ] A) It is not focusable and has no button role; it fails 2.1.1 and 4.1.2 (both Level A); use `<button type="button">`
- [ ] B) It passes: the visible text 'Pay now' is enough for both users
- [ ] C) It fails only 1.4.3 contrast, and the fix is a darker colour
- [ ] D) It is fine once `tabindex="5"` is added, because that makes it focusable and correct

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It is not focusable and has no button role; it fails 2.1.1 and 4.1.2 (both Level A); use `<button type="button">`

**Explanation:** A div with a click handler has no role, is not in the Tab order and ignores Enter and Space. The lesson's checkout scenario is exactly this Blocker.

**Why the others are wrong:**

- **B)** Text alone does not give a role, focusability or keyboard activation.
- **C)** Contrast is unrelated to the keyboard and role failure.
- **D)** A positive tabindex is itself a defect and still gives no role or key handling.
</details>

### 40. A user tabs into this tab list from the preceding content. What is the correct behaviour?

```html
<div role="tablist" aria-label="Account sections">
  <button role="tab" aria-selected="true"  tabindex="0"  id="t1" aria-controls="p1">Profile</button>
  <button role="tab" aria-selected="false" tabindex="-1" id="t2" aria-controls="p2">Billing</button>
  <button role="tab" aria-selected="false" tabindex="-1" id="t3" aria-controls="p3">Security</button>
</div>
```

- [ ] A) Tab moves through Profile, then Billing, then Security
- [ ] B) Billing gets focus first, because it has tabindex="-1"
- [ ] C) Profile gets focus as the only Tab stop; Right Arrow moves to Billing; Tab leaves into the panel
- [ ] D) No tab receives focus, because buttons with role="tab" are not focusable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Profile gets focus as the only Tab stop; Right Arrow moves to Billing; Tab leaves into the panel

**Explanation:** This is the roving tabindex pattern: only the active tab has `tabindex="0"`, the others have `-1`, and arrows move the 0 between tabs.

**Why the others are wrong:**

- **A)** That would make three Tab stops; the pattern keeps the widget to one.
- **B)** -1 removes an element from the Tab sequence, so Billing is not reached by Tab.
- **D)** They are native buttons, and the active one has tabindex="0".
</details>

### 41. A visible-label button has a different accessible name. Which criterion is at risk, and who is mainly affected?

```html
<button aria-label="Find products">Search</button>
```

- [ ] A) 1.1.1 Non-text Content; sighted mouse users
- [ ] B) 1.4.3 Contrast (Minimum); only keyboard users
- [ ] C) 2.5.3 Label in Name (Level A); voice-control users who say the visible label 'Search'
- [ ] D) 3.1.1 Language of Page; only screen-magnifier users

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 2.5.3 Label in Name (Level A); voice-control users who say the visible label 'Search'

**Explanation:** The visible label 'Search' does not match the accessible name 'Find products', so a voice-control user saying 'Search' may not activate it. The lesson's Q4 gives 2.5.3 (A).

**Why the others are wrong:**

- **A)** There is no image or alt text involved here.
- **B)** Contrast is a colour issue and is not related to name mismatches.
- **D)** Page language is unrelated to this button.
</details>

### 42. Two navigation blocks on one page are both announced only as 'navigation landmark'. What is the best fix?

```html
<nav>...main site links...</nav>
<main>...</main>
<nav>...legal and contact links...</nav>
```

- [ ] A) Give each a distinct label, such as `aria-label="Primary navigation"` and `aria-label="Footer navigation"`
- [ ] B) Change both to `<div>` elements so they are not landmarks
- [ ] C) Add `tabindex="1"` and `tabindex="2"` to order them
- [ ] D) Remove all landmarks, since landmarks only help sighted users

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Give each a distinct label, such as `aria-label="Primary navigation"` and `aria-label="Footer navigation"`

**Explanation:** Multiple regions of the same type need distinct labels so screen-reader users can tell them apart.

**Why the others are wrong:**

- **B)** Removing landmarks takes away a main way screen-reader users jump around the page.
- **C)** Positive tabindex values are a defect and do not label anything.
- **D)** Landmarks exist chiefly for screen-reader navigation, not for sighted users.
</details>

### 43. Four hint styles are on a white (#ffffff) background; their contrast ratios were computed with the WCAG relative-luminance formula. Which colour is the first that passes SC 1.4.3 AA for normal-size text?

```css
.a { color: #999999; background: #ffffff; }  /* ratio 2.85 */
.b { color: #808080; background: #ffffff; }  /* ratio 3.95 */
.c { color: #777777; background: #ffffff; }  /* ratio 4.48 */
.d { color: #767676; background: #ffffff; }  /* ratio 4.54 */
```

- [ ] A) `#999999` (2.85:1)
- [ ] B) `#808080` (3.95:1)
- [ ] C) `#777777` (4.48:1)
- [ ] D) `#767676` (4.54:1)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `#767676` (4.54:1)

**Explanation:** Normal text needs at least 4.5:1. #767676 gives 4.54:1, which is why the lesson calls it the lightest grey that passes; #777777 is 4.48:1, just below the line.

**Why the others are wrong:**

- **A)** 2.85:1 is well below 4.5:1 and even below 3:1.
- **B)** 3.95:1 would pass only for large text (3:1).
- **C)** 4.48:1 rounds close to 4.5 but is still below it, so it fails.
</details>

### 44. Grey `#808080` on white has a contrast ratio of 3.95:1. How does it fare under SC 1.4.3 AA?

- [ ] A) Passes for all text sizes, because it is above 3:1
- [ ] B) Passes as 18pt text (needs 3:1) but fails as 12pt normal text (needs 4.5:1)
- [ ] C) Fails for all text sizes, because it is below 4.5:1
- [ ] D) Passes as 12pt text but fails as 18pt text

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Passes as 18pt text (needs 3:1) but fails as 12pt normal text (needs 4.5:1)

**Explanation:** Large text (18pt, or 14pt bold) needs 3:1; normal text needs 4.5:1. 3.95 sits between the two thresholds.

**Why the others are wrong:**

- **A)** Normal-size text still needs 4.5:1.
- **C)** Large text only needs 3:1, which 3.95 exceeds.
- **D)** The thresholds are reversed in this option; large text has the lower requirement.
</details>

### 45. An axe-playwright-python scan returned the dictionary below. What does the scan report?

```python
results = {
    "violations": [
        {"id": "label", "impact": "critical",
         "nodes": [{"target": ["#name"]}, {"target": ["#email"]}, {"target": ["#city"]}]},
        {"id": "color-contrast", "impact": "serious",
         "nodes": [{"target": [".hint"]}]},
    ],
    "incomplete": [
        {"id": "color-contrast", "nodes": [{"target": [".hero p"]}]},
    ],
}
```

- [ ] A) `violations_count` is 2 rules and 4 failing elements; the highest impact is critical; the `incomplete` item needs manual review
- [ ] B) `violations_count` is 4, because there are four failing elements
- [ ] C) `violations_count` is 3, because `incomplete` counts as a violation
- [ ] D) `violations_count` is 2 rules and 3 failing elements, with the highest impact serious

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `violations_count` is 2 rules and 4 failing elements; the highest impact is critical; the `incomplete` item needs manual review

**Explanation:** Violations counts failed rules (`label` and `color-contrast`): 2. Nodes are 3 + 1 = 4 elements. `label` is critical, `color-contrast` serious. `incomplete` is a separate bucket for human review.

**Why the others are wrong:**

- **B)** Four is the node count, not the rule count.
- **C)** `incomplete` is not part of `violations`.
- **D)** The elements total 4 (3 + 1), and the highest impact is critical, not serious.
</details>

### 46. This message goes from client to server. Which statement is correct?

```json
{"jsonrpc": "2.0", "id": 7, "method": "tools/call",
 "params": {"name": "shout", "arguments": {"text": "hi"}}}
```

- [ ] A) It is a notification, so no reply is sent
- [ ] B) It is a response to an earlier `initialize`
- [ ] C) It is a request for `tools/call`; the reply must echo `"id": 7` and carry either a `result` or an `error`
- [ ] D) It is a request for `tools/list`; the reply carries `params`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is a request for `tools/call`; the reply must echo `"id": 7` and carry either a `result` or an `error`

**Explanation:** It has an `id`, a `method` and `params`, so it is a request and expects a response with the same id. Notifications have no id.

**Why the others are wrong:**

- **A)** A notification has no `id`; this message has `"id": 7`.
- **B)** A response has `result` or `error`, not `method`.
- **D)** The method named is `tools/call`, and responses carry `result` or `error`, not `params`.
</details>

### 47. A server sends the message below in reply to a `tools/call` request. What kind of failure is it?

```json
{"jsonrpc": "2.0", "id": 4,
 "result": {"content": [{"type": "text", "text": "b must not be zero"}],
            "isError": true}}
```

- [ ] A) A protocol error, because the message contains an error text
- [ ] B) A tool execution error: the request was valid and the tool ran but its work failed (`isError: true`)
- [ ] C) A parse error with code -32700
- [ ] D) A notification, because it has no `error` field

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A tool execution error: the request was valid and the tool ran but its work failed (`isError: true`)

**Explanation:** Protocol errors use the JSON-RPC `error` object (for example -32601 method not found). A `result` with `isError: true` means the request was fine and the tool's work failed.

**Why the others are wrong:**

- **A)** The error is inside `result`, not in a JSON-RPC `error` object.
- **C)** This message has no `error` object or code at all.
- **D)** It has an `id` (4), so it is a response, not a notification.
</details>

### 48. This FastMCP server and pytest-asyncio test were run with `mcp<2`. What lines does it print, in order?

```python
# s.py
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("notes")

@mcp.tool()
def shout(text: str, times: int = 2) -> str:
    """Repeat text in upper case."""
    if times < 1:
        raise ValueError("times must be positive")
    return " ".join([text.upper()] * times)

@mcp.resource("note://{id}")
def note(id: str) -> str:
    """Read a note."""
    return f"Note {id}"

# test_s.py
import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connect
from s import mcp

@pytest.fixture
def server():
    return mcp._mcp_server

@pytest.mark.asyncio
async def test_demo(server):
    async with connect(server) as s:
        tools = await s.list_tools()
        print([t.name for t in tools.tools])
        print(tools.tools[0].inputSchema["required"])
        print((await s.call_tool("shout", {"text": "hi"})).content[0].text)
        print((await s.call_tool("shout", {"text": "hi", "times": 0})).isError)
        print((await s.call_tool("shout", {"times": 3})).isError)
```

- [ ] A) `['shout']`, `['text', 'times']`, `HI HI`, `False`, `False`
- [ ] B) `['shout', 'note']`, `['text']`, `HI`, `True`, `True`
- [ ] C) `['shout']`, `['text']`, `HI HI`, `False`, `True`
- [ ] D) `['shout']`, `['text']`, `HI HI`, `True`, `True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `['shout']`, `['text']`, `HI HI`, `True`, `True`

**Explanation:** Only `shout` is a tool (`note` is a resource). Because `times` has a default, only `text` is in `required`. The default makes the output 'HI HI'. `times=0` raises, so `isError` is True, and a missing `text` is rejected, so `isError` is True.

**Why the others are wrong:**

- **A)** `times` has a default value, so it is not required.
- **B)** Resources do not appear in `tools/list`, and the default `times=2` repeats twice.
- **C)** A raised ValueError produces `isError` True, so the fourth line cannot be False.
</details>

---

## Part 4: Fill in the Blank

### 49. Complete the rule of thumb: 'Tab moves between controls; ______ keys move inside a control.'

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** arrow

**Explanation:** Arrow keys move within composite widgets such as radio groups, menus, tabs and sliders.
</details>

### 50. To remove an element from the Tab sequence but still allow `element.focus()` from script, set `tabindex="______"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** -1

**Explanation:** `tabindex="-1"` is used for focus management, such as moving focus to an error summary after navigation.
</details>

### 51. In axe results, findings the engine could not decide on are placed in the ______ bucket and must be reviewed by a human.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** incomplete

**Explanation:** The other buckets are `violations`, `passes` and `inapplicable`.
</details>

### 52. The four defect severity levels used in the lesson are Blocker, Critical, Major and ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Minor

**Explanation:** Severity is separate from priority (P1 to P4).
</details>

### 53. NVDA and JAWS have two modes: in ______ mode, letter keys such as H and D act as navigation shortcuts.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** browse

**Explanation:** In focus (forms) mode keys go straight to the page so typing works; NVDA switches automatically on text fields.
</details>

### 54. A JSON-RPC notification has no ______ field, so the receiver must not reply.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** id

**Explanation:** Requests carry an `id`, and the response echoes it.
</details>

### 55. pytest-asyncio runs `async def` tests that are marked with `@pytest.mark.______`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** asyncio

**Explanation:** The SDK client is asynchronous, so tests must be too.
</details>

### 56. When debugging a stdio MCP server, never `______()` to stdout; log to stderr instead.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** print

**Explanation:** stdout carries the JSON-RPC protocol messages, so extra text corrupts the stream.
</details>

---

## Part 5: Matching

### 57. Match each POUR principle (left) with the example failure (right).

| Item | Match with |
|---|---|
| 1. Perceivable | A. A form returns 'Error 4012' with no hint of what to fix |
| 2. Operable | B. A custom dropdown built from divs exposes no name or role |
| 3. Understandable | C. A keyboard trap in a chat widget |
| 4. Robust | D. An image with no text alternative |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-D, 2-C, 3-A, 4-B

**Explanation:** Missing alt is Perceivable, a keyboard trap is Operable, an unclear error is Understandable, and missing name/role/value is Robust. The first digit of the SC number maps to the principle.
</details>

### 58. Match each axe result bucket (left) with what it means (right).

| Item | Match with |
|---|---|
| 1. violations | A. The rule had nothing to check, for example no video on the page |
| 2. passes | B. A rule ran and the elements passed |
| 3. incomplete | C. axe could not decide, so a human reviews it |
| 4. inapplicable | D. A rule definitely failed on one or more elements |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-D, 2-B, 3-C, 4-A

**Explanation:** Violations are your defects; passes prove what was checked; incomplete needs manual review; inapplicable is coverage information only.
</details>

### 59. Match each MCP purpose (left) with its method (right).

| Item | Match with |
|---|---|
| 1. Run a tool with arguments | A. `notifications/initialized` |
| 2. Read data identified by a URI | B. `tools/call` |
| 3. Fetch a reusable message template | C. `prompts/get` |
| 4. Tell the server the client is ready after the handshake | D. `resources/read` |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-B, 2-D, 3-C, 4-A

**Explanation:** Tools use `tools/call`, resources use `resources/read`, prompts use `prompts/get`, and the client sends the `notifications/initialized` notification to end the handshake.
</details>
