# Reference System Brief: ShopFront and its Test Automation Framework

This brief is the **only** system you may target in today's exercise. It describes a synthetic web shop and the test automation framework a QE team maintains for it. It is modelled on the kind of framework you built in Weeks 4 to 7, so every part should feel familiar. All names, data and logs here are invented and safe to paste into Claude.

## 1. The product: ShopFront

| Area | What it does | Where it shows up in testing |
|---|---|---|
| Registration and login | Sign-up form (rules in `materials/user-stories.md`), login, password reset by email | UI tests, data-driven tests, API tests |
| Product search | Keyword search, category filter, "no results" message | UI tests |
| Cart | Add, remove, change quantity | UI and API tests |
| Checkout | Promo codes (US-101), guest checkout (US-102), saved addresses (US-103), shipping rules (`materials/shipping.py`) | Unit, API and UI tests |
| Order history | Registered users only | UI and API tests |
| Items API | `GET/POST/PUT/PATCH/DELETE /items`, token auth, pagination | API tests (`requests` + pytest, as in Week 7) |

## 2. The framework

| Layer | Contents |
|---|---|
| Unit tests | pytest tests for pure business rules such as `shipping_cost` |
| API tests | `requests` + pytest, JSON Schema checks on responses |
| UI tests | Playwright for Python with page objects (`LoginPage`, `SearchPage`, `CartPage`, `CheckoutPage`) |
| BDD layer | A few Gherkin feature files for checkout, owned with the product owner |
| Test data | CSV and JSON files under `data/` for data-driven tests |
| Accessibility | axe scan tests on three page states |
| CI | Pipeline runs smoke tests on every merge request and the full suite nightly; about 150 tests; JUnit XML and HTML reports |

## 3. How the team works today (the pain points)

These are the problems the team lead wants GenAI ideas for. You do not have to use all of them, and you may find others in the brief.

1. New user stories arrive vague (see US-101 to US-103). Ambiguities are found late, during automation.
2. Test design for new rules (such as shipping) is done under time pressure; boundaries are sometimes missed.
3. Data files for data-driven tests are hand-written and repetitive (`user1`, `user2`, ...).
4. New page objects take a long time to write and copy-paste mistakes creep in.
5. The nightly run produces about 3 to 10 failures. Someone spends the first hour of every morning reading logs (see `materials/ci-failure-sample.txt`).
6. Bug reports from exploratory sessions are inconsistent (see `materials/bug-notes.txt`).
7. The product owner wants a short, plain-language quality summary every Friday.
8. About 2,000 historical failure messages sit in the CI archive and nobody has grouped them.
9. Some UI tests are flaky; the team has 6 months of labelled pass/fail history per test.
10. A checklist rule says every username field must reject more than 16 characters.

## 4. Constraints

- Only Claude (the organisation-approved assistant) may be used. Nothing from a real system, real customer, real credential or internal URL may go into a prompt.
- Every AI output used by the team must have a named human reviewer and a way to check it.
- The team will not let any AI output approve, merge or release anything on its own.
