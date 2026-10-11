# <Project 1 name>: UI test suite

> TEMPLATE for the Project 1 - QE Foundations UI deliverable. Replace every <angle bracket>.
> ASSUMPTION: the exact Project 1 application and test scope are set by your instructor's Project 1 brief;
> this template is deliberately generic. Where the brief says something different, the brief wins.

## 1. What this is
<2-3 sentences: the application under test (AUT), what the UI suite covers, which tools (Playwright and/or Cypress).>

## 2. Prerequisites
- Node.js <version>, npm <version>
- Cypress <exact version>, cypress-visual-regression <exact version>
- Browser used for baselines: <name + version>; OS used for baselines: <OS>
- The AUT must be reachable at <URL / how to start it locally>

## 3. Install and run (verified from a clean clone on <date>)
```bash
git clone <repo url> && cd <repo>
npm install
<command to start the AUT, if local>
npm run cy:run                # whole suite, headless
npm run cy:open               # interactive, time-travel debugging
npm run visual:compare        # visual checks only
npm run visual:base           # ONLY to (re)create baselines; review every PNG before committing
```
Environment values (names only, never real secrets): <APP_USER, APP_PASSWORD ... and where they are set>.

## 4. Test inventory
| Spec | Type (functional / visual) | What it proves |
|---|---|---|
| <file> | <type> | <behaviour> |

## 5. Visual testing policy
- Snapshot scope and thresholds (and the unit: fraction vs percent for your plugin version): <...>
- Dynamic content and how it is handled (mask / stub / freeze): <...>
- How to update a baseline deliberately (steps + who reviews): <...>

## 6. Artifacts produced by a run
| Artifact | Location | Committed? |
|---|---|---|
| Baselines | cypress/snapshots/base/ | yes |
| Actual screenshots, diffs | cypress/snapshots/actual, cypress/snapshots/diff | no |
| Videos (failing specs only) | cypress/videos/ | no |
| Run log | cypress/logs/ | no |

## 7. Latest result
<paste the final `cypress run` summary table: specs, tests, passing, failing, duration>

## 8. Known limitations and next steps
- <honest list: flaky areas, browsers not covered, pages without visual checks, ...>
