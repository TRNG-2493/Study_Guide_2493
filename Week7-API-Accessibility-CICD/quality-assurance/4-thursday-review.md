# QA Review & Interview Questions: Week 7 Thursday - Accessibility & MCP Testing

## Part A: Artifact Review

Day: **4-thursday - Accessibility & MCP Testing**

### Written content
| Lesson | Words | Required sections | Fences balanced | Resource links | Later-day mentions |
|---|---|---|---|---|---|
| accessibility-principles.md | 5,391 | yes | yes | 8 | 4 |
| keyboard-screen-reader-testing.md | 5,503 | yes | yes | 7 | 0 |
| automated-accessibility-scanning.md | 5,431 | yes | yes | 6 | 2 |
| accessibility-defect-analysis.md | 5,473 | yes | yes | 6 | 1 |
| introduction-to-mcp-testing.md | 5,473 | yes | yes | 5 | 2 |

### Demo
| Item | Status |
|---|---|
| demos/4-thursday/code/demo_accessibility_mcp_testing.py | present |
| demos/4-thursday/demo-script.md | present |
| demos/4-thursday/diagrams/*.mermaid | 2 file(s) |

### Exercise
| Item | Status |
|---|---|
| exercise/4-thursday/exercise-accessibility-mcp-testing.md | present |
| starter_code/ | present |
| solution/ | present |
| 'Project 2 milestone' section | yes |
| Pair-programming (driver/navigator, 30-min swap, retrospective) | yes |

### Quiz
| Item | Status |
|---|---|
| quiz/4-thursday/quiz-accessibility-mcp-testing.md | present |
| Questions | 59 |
| Hidden-solution blocks | 59 |

### Issues found by the audit
- None

### Reviewer notes and open items for human sign-off

1. **Completeness.** All 5 written lessons, the demo (script, runnable axe/Playwright and MCP tests, two local HTML pages, MCP server, 2 diagrams), the exercise (pair-programming brief with driver/navigator roles, 30-minute swap table and retrospective template; `starter_code` ShopFront page with 10 planted defects; solution with fixed page, tests and 5 sample defect reports) and the quiz (59 questions) are present. The Thursday protocol (a collaborative pair project that synthesises the week) is met.
2. **Lesson length.** The lessons are about 5.4k words each (roughly 25+ minutes of reading), slightly over the log's 10-20 minute guide, because of the depth standard. Suggest using the Summary and Practice sections for the timed read.
3. **Verified by running.** The demo suite passed 9 tests offline in Chromium, the exercise solution passed 21, and the overlay on Wednesday's framework passed 39. Scanning confirmed that axe catches 6 of the 10 planted defects; 4 are manual-only (div-as-button, keyboard trap, missing focus style, unannounced form error).
4. **Open item: lesson snippets unchecked.** The `axe-playwright-python` calls in `automated-accessibility-scanning.md` were written from memory and were not checked against the library during the lesson build. The demo and exercise code use the installed library's real API. Cross-check the lesson's snippets against `demos/4-thursday/code` before class and fix any drift.
5. **Open item: inconsistent automation figure.** The lessons disagree on how much of accessibility testing automation can cover ("30 to 40 percent" versus "a third to a half"). The quiz avoids any figure. Harmonise the lessons.
6. **Contrast ratios.** The lessons' ratios were first written from memory, but the quiz's script-computed values agree (#999999 2.85, #767676 4.54, #777777 4.48).
7. **MCP version pin.** The MCP lessons and demo pin `mcp<2` because mcp 2.x renames FastMCP to MCPServer. A yield-style async fixture holding an open session errors at teardown, so the tests open a session per test.
8. **Not executed or rendered.** Screen-reader steps (NVDA/VoiceOver) are manual and were not run. The Mermaid diagrams were not rendered; render-check them.
9. **No spoilers.** Friday mentions in the lessons are one-line pointers.

**Verdict:** Complete against the log and the Thursday protocol; pending the human items above (notes 4, 5 and 8).

---


## Part B: Interview Question Bank

## Beginner (Foundational)

### Q1: What does accessibility (a11y) mean, and why does it matter to a tester?
**Keywords:** accessibility, a11y, permanent, temporary, situational
<details>
<summary>Click to Reveal Answer</summary>

Accessibility means people with permanent, temporary and situational limits can use your product. It is a quality attribute, backed by law (ADA, Section 508, the European Accessibility Act) and by business sense, so a tester treats it as a requirement to verify rather than a nice-to-have.
</details>

---

### Q2: What are the main disability groups, and how does assistive technology work with a web page?
**Keywords:** visual, auditory, motor, cognitive, accessibility tree
<details>
<summary>Click to Reveal Answer</summary>

Disabilities fall into visual, auditory, motor and cognitive groups, and each has its own assistive technologies. Assistive technology reads the browser's accessibility tree rather than the pixels on screen. That is why correct markup, not visual appearance, determines whether a page is usable.
</details>

---

### Q3: What are the four POUR principles of WCAG?
**Keywords:** Perceivable, Operable, Understandable, Robust, WCAG
<details>
<summary>Click to Reveal Answer</summary>

POUR stands for Perceivable (information can be perceived), Operable (the interface works with many input methods), Understandable (content and behaviour are predictable and clear) and Robust (content works with current and future user agents). Testers use POUR as a checklist and cite the matching WCAG success criterion in defect reports.
</details>

---

### Q4: What are WCAG conformance levels A, AA and AAA, and which is the usual target?
**Keywords:** Level A, Level AA, AAA, success criteria, WCAG 2.2
<details>
<summary>Click to Reveal Answer</summary>

Level A is the minimum, where failure blocks some users completely. Level AA removes major barriers for most users and is the usual legal and contractual target, with WCAG 2.2 AA the common choice. Level AAA is aspirational and not achievable for all content. To claim AA, a page must meet all Level A and all Level AA criteria; partial conformance is not AA.
</details>

---

### Q5: Why is semantic HTML preferred over a div-based button?
**Keywords:** semantic HTML, native button, div soup, name/role/value
<details>
<summary>Click to Reveal Answer</summary>

Native elements such as buttons, links, labels, headings and landmarks give accessibility for free: role, keyboard behaviour and an accessible name. A clickable div removes all of that, which is why a div-as-button is a classic defect, often a blocker. Semantic HTML comes first, with ARIA only filling gaps.
</details>

---

### Q6: What is the first rule of ARIA?
**Keywords:** ARIA, first rule, native HTML, role, aria-label
<details>
<summary>Click to Reveal Answer</summary>

If a native HTML element already has the semantics and behaviour you need, use it instead of adding ARIA. The lesson summarises this as 'No ARIA is better than bad ARIA'. Related rules: do not change native semantics unnecessarily, every interactive ARIA control must be keyboard operable, never put aria-hidden on focusable elements, and every interactive element needs an accessible name.
</details>

---

### Q7: How do you run a basic keyboard-only accessibility test?
**Keywords:** Tab, Shift+Tab, visible focus, focus order, keyboard trap
<details>
<summary>Click to Reveal Answer</summary>

Tab and Shift+Tab through everything and check that focus is visible, the order is logical, skip links work and there are no keyboard traps. Confirm that Enter and Space activate controls, and that custom widgets follow the expected APG key patterns for menus, tabs, dropdowns and modals. Modals and single-page apps also need deliberate focus management.
</details>

---

### Q8: How should tabindex be used when testing and building focusable elements?
**Keywords:** tabindex 0, tabindex -1, positive tabindex, native elements
<details>
<summary>Click to Reveal Answer</summary>

Use `tabindex=0` sparingly to add an element to the tab order, and `tabindex=-1` for focus that is managed by script. Never use positive values, because they override the natural order. The better approach is to prefer native elements, which are focusable by default.
</details>

---

### Q9: What is the difference between browse mode and focus mode in a screen reader?
**Keywords:** screen reader, NVDA, browse mode, focus mode, VoiceOver rotor
<details>
<summary>Click to Reveal Answer</summary>

In browse mode (NVDA/JAWS) the screen reader owns the keyboard, so letter keys are navigation shortcuts such as H for the next heading. In focus mode, keys go straight to the page so typing works; NVDA switches automatically on a text field. VoiceOver has no such modes and uses VO commands and the rotor instead. Custom widgets with wrong roles can leave the screen reader in browse mode and swallow the keys they expect.
</details>

---

### Q10: What are the four result buckets in an axe-core scan?
**Keywords:** violations, passes, incomplete, inapplicable, axe-core
<details>
<summary>Click to Reveal Answer</summary>

Violations are rules that definitely failed and are your defects. Passes show what was checked and passed. Incomplete means axe could not decide, for example text over a background image, so a human must review it. Inapplicable means the rule had nothing to check, so it is only coverage information.
</details>

---

### Q11: What can automated accessibility scanners not catch, and what does a clean scan prove?
**Keywords:** automation limits, manual testing, meaning, order, clean scan
<details>
<summary>Click to Reveal Answer</summary>

Scanners catch objective, machine-checkable defects such as missing labels, missing alt text, contrast failures and invalid ARIA. They cannot judge meaning, order or real usability, so a clean scan is not proof of accessibility. Automation must be combined with keyboard and screen-reader testing.
</details>

---

### Q12: What is MCP (Model Context Protocol)?
**Keywords:** MCP, host, client, server, tools resources prompts
<details>
<summary>Click to Reveal Answer</summary>

MCP connects AI applications (hosts, through clients) to servers that offer tools, resources and prompts. From a tester's point of view a server is an API, so API testing skills transfer directly.
</details>

---

### Q13: What message format does MCP use?
**Keywords:** JSON-RPC 2.0, request, response, error, notification
<details>
<summary>Click to Reveal Answer</summary>

MCP messages are JSON-RPC 2.0, in four shapes: request, successful response, error response and notification. Testers must also distinguish protocol errors from tool errors, where a tool reports failure through the isError flag in an otherwise valid result.
</details>

---

## Intermediate (Application)

### Q14: How do you turn an automated accessibility finding into a good defect report, and how do you rate its severity?
**Keywords:** finding vs defect, severity, WCAG criterion, reproduction steps, acceptance criteria
**Hint:** Think about triage, classification, and the difference between severity and priority.
<details>
<summary>Click to Reveal Answer</summary>

A finding becomes a defect only when it is verified, scoped, classified, rated and actionable. Classify it by WCAG success criterion, level, POUR principle, user group and root cause, then rate severity as blocker, critical, major or minor using impact, frequency, workaround and legal exposure. A strong report has a specific title, environment with AT versions, steps, expected and actual results, WCAG reference, evidence, suggested fix and acceptance criteria. Priority stays a separate business decision, and axe's impact label is only a starting point.
</details>

---

### Q15: axe reports 40 nodes with the same violation. How should you handle it in triage?
**Keywords:** de-duplicate, root cause, nodes, regression test, metrics
**Hint:** Consider how many fixes are really needed.
<details>
<summary>Click to Reveal Answer</summary>

De-duplicate axe results, because many nodes often share one root cause and one fix, such as a shared component. Report the root cause once, listing the affected nodes. After the fix, verify with the original method, add regression tests, and track metrics such as violations over time, issue density and automation coverage.
</details>

---

### Q16: What are the three MCP primitives, and who controls each?
**Keywords:** tools, resources, prompts, tools/list, resources/read
**Hint:** Think about model, application and user.
<details>
<summary>Click to Reveal Answer</summary>

Tools are controlled by the model and perform actions with inputs, using tools/list and tools/call. Resources are controlled by the application and are readable data identified by a URI, using resources/list and resources/read. Prompts are controlled by the user and are reusable message templates, using prompts/list and prompts/get. FastMCP derives each tool's inputSchema from type hints and its description from the docstring, so both are part of the contract.
</details>

---

### Q17: Describe the layers of MCP testing and where most tests should sit.
**Keywords:** test layers, unit tests, contract tests, in-memory client, stdio end-to-end
**Hint:** Compare it with the test pyramid in API testing.
<details>
<summary>Click to Reveal Answer</summary>

Layer 1 is tool logic unit tests with no MCP client. Layer 2 is contract tests on tools/list names, descriptions and inputSchema. Layer 3 covers protocol conformance and errors, layer 4 covers resources and prompts, and layer 5 is a real stdio or HTTP end-to-end test. Most tests should be layers 1 to 4, which are fast, with a few layer-5 tests to prove the real startup path works.
</details>

---

## Advanced (Deep Dive)

### Q18: How would you approach testing a new MCP server end to end, from exploration to automation?
**Keywords:** Inspector, pytest-asyncio, protocol vs tool errors, lifecycle, security
**Hint:** Start manual, then automate by layer, and include lifecycle and security.
<details>
<summary>Click to Reveal Answer</summary>

Explore first with the MCP Inspector, then automate with pytest-asyncio: logic tests, tools/list contract tests, error tests, resource and prompt tests, plus one real stdio test. Cover the lifecycle (initialize, capability negotiation, notifications/initialized, operation, shutdown) and assert both protocol errors and tool errors via isError. For stdio servers, never print to stdout, since that corrupts the message stream. Validate inputs, apply least privilege, stay aware of prompt injection, and pin SDK versions.
</details>

---
