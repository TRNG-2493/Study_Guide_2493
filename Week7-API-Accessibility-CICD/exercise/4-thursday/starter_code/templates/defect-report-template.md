# DR-<nnn>: <short, specific title - include the control and the user impact>

| Field | Value |
|---|---|
| **ID** | DR-<nnn> |
| **Page / state** | ShopFront `loaded` / `form-error` / `api-down` |
| **WCAG success criterion** | e.g. 1.1.1 Non-text Content (Level A) |
| **POUR principle** | Perceivable / Operable / Understandable / Robust |
| **Severity** | Blocker / Critical / Major / Minor (justify below with impact x frequency x workaround) |
| **Priority** | P1 / P2 / P3 |
| **Found by** | axe rule `<id>` / keyboard pass / screen-reader pass (say which) |
| **Users affected** | e.g. screen-reader users, keyboard-only users, low-vision users |
| **Environment** | Browser + version, OS, AT (NVDA / VoiceOver) + version, page commit/branch |
| **Reporter / date** | |

## Steps to reproduce
1.
2.

## Expected result

## Actual result

## Evidence
axe rule id, impact, number of nodes and 1-2 selectors (e.g. `.card img`); screenshot / transcript of the screen-reader announcement.

## Root cause and de-duplication
One root cause may produce many axe nodes. List the nodes this single report covers.

## Severity justification
Impact: __  Frequency: __  Workaround: __

## Suggested fix
Concrete HTML/CSS/JS change (a short snippet is ideal).

## Acceptance criteria (re-test)
- [ ] axe rule `<id>` reports 0 nodes in state `<state>`
- [ ] Manual re-check: <what a human verifies>
