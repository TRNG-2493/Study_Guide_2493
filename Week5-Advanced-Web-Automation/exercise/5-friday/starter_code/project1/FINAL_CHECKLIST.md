# Project 1 - QE Foundations: UI deliverable, final checklist

Copy into your Project 1 repo and tick every line. Anything you cannot tick goes in README section 8 (honest limitations).
ASSUMPTION: Project 1's application and exact scope come from your instructor's brief; adapt the wording, keep the structure.

## A. README
- [ ] Follows README.template.md: purpose, prerequisites with exact versions, install/run, test inventory, visual policy, artifacts, latest result, limitations
- [ ] A classmate could run it with no questions (give it to one and note their feedback)

## B. Run instructions
- [ ] Verified from a FRESH clone in a new folder: `npm install` then the documented commands work
- [ ] AUT start command and port are documented; no manual steps hidden in your head
- [ ] Secrets are not in the repo (`cypress.env.json` ignored, only an `.example` file committed)

## C. Passing suite
- [ ] `npm run cy:run` exits with code 0 twice in a row (same result both times)
- [ ] `npm run visual:compare` is green against committed baselines
- [ ] No `it.skip`, `it.only`, `describe.only`, `cy.pause()`, `.debug()` or `cy.wait(<number>)` left in any spec
- [ ] Every test has a behaviour name and at least one outcome assertion (not only "it did not crash")
- [ ] The raw recorded test is kept only as a labelled "before" example, or removed

## D. Artifacts
- [ ] Baseline PNGs committed under cypress/snapshots/base/ and each one reviewed by eye
- [ ] One failure screenshot + video from an intentional failure (saved under `evidence/`) plus the diff image from Task 6
- [ ] `docs/DIAGNOSIS.md` completed
- [ ] Final `cypress run` summary pasted into README section 7
- [ ] Run log (`cypress/logs/cypress-run.log`) from one full run saved under `evidence/`

## E. Repo hygiene
- [ ] .gitignore covers node_modules, actual/diff/screenshots/videos/logs, cypress.env.json
- [ ] No node_modules, no large videos, no secrets in git history of the final commit
- [ ] Clear commit history; final commit tagged or noted `project1-ui-final`

## F. Submission
- [ ] Link to the repo/branch (or zip) + the one-paragraph reflection below pasted in the submission form

### Reflection (5-8 sentences)
What did Friday's techniques change in how you debug, document and protect the UI? What would you automate next?
