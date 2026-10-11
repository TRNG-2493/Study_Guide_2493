# Playwright vs Cypress - Comparison Note

**Pair:** <Name A> + <Name B> | **Branch:** `pair/<a>-<b>` | **Date:** <date>
**App under test:** ShopLite starter app (or your Project 1 app: <name>) - <state which>

> Rules: every claim needs EVIDENCE (a line of code, a file, a run result, an error message you actually saw).
> "Cypress is better/faster" with no evidence earns no credit. Keep the whole note to about 1-2 pages.

## 1. What we ported (3 tests)

| # | Playwright test | Cypress spec | Shape | Ported OK? (pass in `run`? in `open`?) |
|---|---|---|---|---|
| 1 | `test_login_rejected` | `cypress/e2e/01-login-rejected.cy.js` | form + data-driven | |
| 2 | `test_add_to_cart_updates_badge` | | | |
| 3 | `test_sort_price_low_to_high` | | | |

## 2. Side-by-side comparison

Fill every row. "Evidence" = file + line, command output, or a message you saw. Add your own rows at the bottom.

| Dimension | Playwright (Python) | Cypress (JS) | Evidence (file/line/output) |
|---|---|---|---|
| Locators (how you found elements; any you had to change) | | | |
| Waiting (how the delayed product list was handled) | | | |
| Assertions (retrying vs non-retrying; the sort check) | | | |
| Reading values (`all_inner_texts()` vs `.then()/.should(cb)`) | | | |
| Reusable login (fixture vs command + `cy.session`) | | | |
| Data-driven tests (parametrize vs loop over a JSON file) | | | |
| Debugging (the first time a test failed: what did you use, how long to find the cause?) | | | |
| Speed (measured: command + wall time, N runs; say how you measured) | | | |
| Setup friction (install, binary, config, first green test: minutes and blockers) | | | |
| Lines of code per test (count them) | | | |
| Error messages (paste one from each tool and rate how helpful it was) | | | |
| Browser/language coverage (what each tool could not do for our project) | | | |
| _(your own row)_ | | | |

## 3. What got shorter, longer, or different (with line examples)

- Shorter: <example with file/line>
- Longer: <example>
- Different (a concept that does not map 1:1): <example, e.g. `await`-free chaining, no native `to_have_count(0)`>

## 4. Surprises and mistakes we made

(At least two. For example: a thing that failed because we assumed Playwright behaviour in Cypress, and how we found it.)

1.
2.

## 5. Which tool for which situation (the recommendation)

State a recommendation for **our** Project 1 and one situation where you would choose the **other** tool.
Cite at least three rows or pieces of evidence from the table above.

- For Project 1 we would use: ___ because (evidence): ___
- We would choose the other tool when: ___ because (evidence): ___

## 6. Open questions

What could we not verify (e.g. cross-browser runs, CI behaviour)? What would we test next?
