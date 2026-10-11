# Friday Exercise: CI/CD for Quality Engineering

Individual exercise. Time box: 2 to 3 hours.

## Scenario

Your Project 2 framework runs on your laptop: API tests (Monday to Wednesday), accessibility and MCP tests (Thursday). A framework nobody runs automatically is not a safety net. Your team lead wants every merge request checked within minutes, a full run on main, and reports anyone can open without asking you. Today you build that pipeline in GitLab, publish the reports, and break it on purpose to prove you can read a failure.

## Objectives

By the end you can:
- translate the local commands of a test framework into pipeline jobs and stages;
- run an API under test inside a job and wait for it to be ready;
- publish JUnit, HTML, coverage and accessibility evidence with `artifacts` and `when: always`;
- keep credentials in masked (and protected where relevant) CI/CD variables, never in the repo or logs;
- choose which tests run on merge requests versus main and schedules;
- publish reports with GitLab Pages and debug a red pipeline from the log and the Tests tab.

## Prerequisites

- A GitLab project you can push to (GitLab.com or the class instance), and Maintainer rights to create CI/CD variables and protect branches.
- At least one runner available (shared runners enabled under Settings > CI/CD > Runners). Ask your instructor which tag to use, if any. If jobs stay "pending/stuck", this is the first place to look.
- Git and Python 3.12+ locally. Chromium for the accessibility tests is preinstalled in the lab image; do not run `playwright install` there. Inside the pipeline you will use a Playwright image instead.
- Mon to Fri material only: pytest markers and reports (Mon/Tue), layered framework and mocking (Wed), accessibility and MCP tests (Thu), GitLab CI/CD (Fri lesson and demo).

### Get the starter repo into GitLab

```
cd starter_code/project2-repo
git init -b main
git add . && git commit -m "Project 2 framework before CI"
git remote add origin <your-project-url>.git
git push -u origin main
```
Then create a branch for your work (`git switch -c add-ci`) and open a merge request when you have a first pipeline. The starter has no `.gitlab-ci.yml` yet. Its README lists the run commands. Also fill in `templates/ci-variables-checklist.md` as you go.

## Core tasks

Commit after each stage. Read every pipeline result before moving on. Do not copy the demo file blindly: understand each line you keep.

### Task 1: Run locally and list the pipeline commands (15 min)
1. Install requirements, start the API (`python project2_api_server.py 8000`), run the whole suite once.
2. Find out what each marker selects: `pytest -m smoke`, `mock`, `live`, `a11y`, `mcp` (use `-q`). Note counts and timing.
3. Write down in your README (CI section, draft) a table: command, needs API?, needs browser?, needs credentials?, duration. This table drives your stage design.

### Task 2: First pipeline, lint plus API tests (20 min)
Create `.gitlab-ci.yml` with stages `lint` and `test-api`.
- `lint`: install `ruff`, run a minimal rule set (`--select E9,F63,F7,F82`, syntax and undefined names).
- `test-api`: pinned `python:3.12` image, install `requirements.txt`, run pytest. At this stage use `API_MODE=mock` so no server is needed.
- Cache pip downloads (`PIP_CACHE_DIR` inside the project directory, `cache:` keyed on `requirements.txt`).
- The pipeline must run on every push.

Check: pipeline green; second run shows "Successfully extracted cache".

### Task 3: Run the API under test inside the job (20 min)
Add a job that starts the stand-in API in the background and runs live tests.
- Start `project2_api_server.py` on port 8000 with `&`, log to a file.
- Wait until `/health` answers before running tests (a retry loop, not a fixed `sleep`).
- `BASE_URL` must come from a variable, not from test code. Set `REQUIRE_API=1` so a missing API is a failure, not a quiet skip.
- Optional discussion: when would a `services:` container be better than starting the process yourself?

Check: live tests pass; if you remove the wait, explain what you see.

### Task 4: Separate stages (25 min)
Restructure into: `lint` -> `test-api` (mocked, the MR gate) -> `test-a11y` -> `test-mcp` -> `report`.
- The accessibility job needs a real browser: use `mcr.microsoft.com/playwright/python:v<version>-noble` and install the same `playwright==<version>` with pip. The two versions must match. Choose the version from the pip package your install resolves, or pin both.
- MCP tests are in-memory: plain Python image.
- Use `needs:` so independent jobs start right after `lint` instead of waiting for a whole stage.

Check: pipeline graph shows the stages; the a11y job runs without `playwright install`.

### Task 5: Artifacts and reports (25 min)
For every test job publish:
- JUnit XML with `artifacts:reports:junit` (it fills the Tests tab);
- a self-contained pytest-html report;
- for a11y: the JSON files in `reports/a11y/` plus an HTML report;
- coverage: a `coverage:` regex that matches the pytest-cov `TOTAL` line, and a Cobertura XML via `coverage_report`.

Use `when: always` and a sensible `expire_in`. Do not put `.cache/` or `__pycache__` in artifacts.

Check: break a test and confirm the reports are still downloadable. A failed job without artifacts is the most common mistake.

### Task 6: Secrets and configuration (20 min)
1. In Settings > CI/CD > Variables create `API_USER`, `API_PASSWORD`, `API_ADMIN_USER`, `API_ADMIN_PASSWORD`. Mask the passwords; protect the admin password (or justify why not). Fill in the checklist.
2. The framework already reads these names from the environment. Keep the values out of the repo and the YAML.
3. Add a fail-fast check that stops the job with a clear message when a required variable is missing (shell `: "${NAME:?message}"` is enough). Demonstrate it: delete one variable, run, capture the failure, restore it.
4. Prove that nothing leaks: `git grep` for the password, read the job log, check that you never print the value (print its length at most).

Think: why does a protected variable disappear on a merge request from an unprotected branch, and which of your jobs does that affect?

### Task 7: Rules, parallelism (20 min)
- Smoke only (`-m smoke`, with the API started) on merge requests; full live suite on the default branch and on scheduled pipelines.
- Add `workflow:rules` so a push to a branch with an open MR does not create two pipelines.
- Run one job in parallel: either `parallel:matrix` over two Python versions for the mocked tests, or `pytest -n 2` (pytest-xdist) for the live suite. Say in your notes which you chose and why.
- Create a pipeline schedule (Build > Pipeline schedules) and run it once manually.

### Task 8: Publish with GitLab Pages (15 min)
- A `report`-stage job collects all reports into `public/` with a simple `index.html` linking them.
- A job named exactly `pages`, on the default branch only, publishes `public/` as an artifact.
- Open the Pages URL (Deploy > Pages) and click through to a report and an a11y JSON file.

### Task 9: Break and fix drill (15 min)
On a branch, make a test fail deliberately (for example change an expected status code). Open an MR.
1. Locate the failure in the job log, then in the pipeline's Tests tab. Note the assertion message and the test name.
2. Download the HTML report from the artifacts.
3. Fix it and see the MR go green.
4. Repeat with a second, different kind of failure (a YAML mistake, a wrong image tag, a missing variable, a wrong artifact path). Record both in your notes.

## Stretch goals

- Make the DAG explicit: `needs` on every job so the `report` job waits only for what it uses (use `optional: true` for jobs excluded by rules).
- Add an `allow_failure: true` experimental job (for example a higher-parallelism run). Show the orange warning with a green pipeline.
- Add a manual `deploy-sim` job with an `environment:` (name and URL) that only simulates a deploy and needs a secret.
- Add a badge for coverage to the README.

## Deliverables

1. Screenshot of the pipeline page (graph visible) of a green main pipeline, and the project/pipeline URL.
2. `.gitlab-ci.yml` committed to the repo.
3. README "CI" section: stages table, variables you need (names only), how to run jobs locally, link to the Pages site.
4. Completed `templates/ci-variables-checklist.md` (no values).
5. Notes (half a page): two failures you debugged, with symptom, cause, fix.

## Definition of Done

- [ ] Green pipeline on `main` with lint, API, a11y, MCP, report stages.
- [ ] A merge request ran the faster gate (mocked + smoke) and passed.
- [ ] Tests tab shows results; coverage percentage is visible.
- [ ] Artifacts exist for failing runs too (`when: always`).
- [ ] No secret in the repo, the YAML or any job log; passwords masked.
- [ ] A missing variable fails the job with a clear message.
- [ ] Reports are published on GitLab Pages.
- [ ] Two failures documented.
- [ ] README CI section written.

## Grading rubric (100 points)

| Area | Points | Full marks means |
|---|---|---|
| Pipeline structure | 20 | Correct stage order, pinned images, cache, `needs`, no duplicate pipelines |
| API under test in the job | 15 | Server started in background, real health-wait, `BASE_URL` from a variable, no silent skips |
| Artifacts and reports | 20 | JUnit in Tests tab, HTML, a11y JSON, coverage, all with `when: always` |
| Secrets and configuration | 15 | Masked variables, protected where sensible, fail-fast demonstrated, nothing leaked |
| Rules and parallelism | 10 | Smoke on MR, full on main/schedule, matrix or xdist with a justification |
| GitLab Pages | 10 | `pages` job publishes an index with working links |
| Debugging notes, README, checklist | 10 | Two real failures analysed, clear README section |

## Hints (no full solution)

- Local first: every pipeline `script:` line should work in your terminal. Run it there before pushing.
- Which Python am I using? In the job log the first lines show the image and Python version; the framework needs Python 3.12 or newer.
- `pytest-html` and `pytest-cov` are not in `requirements.txt`: install them in the job.
- A multi-line command with `>` folds into one line, convenient for long pytest options.
- Use `python -m pytest` so the interpreter that installed the packages is the one that runs them.
- Missing playwright browsers in the a11y job means wrong image or mismatched version, not a missing `playwright install`.
- The a11y tests check that KNOWN violations are present on the bad storefront. A green job is the expected result.
- Reusable snippets: a hidden job `.name:` with `extends:`, or a YAML anchor `&x` used as `- *x` inside a script list.
- Masking fails if the value has spaces or is shorter than 8 characters.
- `needs:` pointing at a job that did not run in this pipeline fails the pipeline unless `optional: true`.
- The pages job must be named `pages` and produce `public/`.
- A job that stays pending: check runner tags and whether shared runners are enabled.

## Project 2 milestone

Project 2 framework is pipeline-ready when: the repository has a green pipeline on `main`, test reports (JUnit, HTML, a11y JSON, coverage) are published and reachable, the README explains how to run the framework locally and in CI, and no secret exists in the repository or logs. Bring the pipeline URL and the Pages URL to the Project 2 review.

## Week-closing self-assessment

Tick honestly; leave a note for anything unticked.

- [ ] Postman: I can build requests, collections, environments and assertions, and explain what they do not give me.
- [ ] API automation: I can write pytest tests with a client layer, schemas, data-driven cases and fixtures that clean up.
- [ ] Mocking: I can isolate a dependency with `responses`/mocks and decide between mock and live tests.
- [ ] Accessibility: I can run an axe scan, read violations, and name what needs manual keyboard/screen-reader checks.
- [ ] MCP: I can describe what an MCP server exposes and test tools/resources in-memory.
- [ ] CI: I can build a pipeline from scratch, publish reports, manage secrets and read a failure.
- [ ] Biggest gap this week, and my plan for it:
