# Pipeline Stages and Jobs

## Learning Objectives

By the end of this lesson you will be able to:

- Explain how **stages** and **jobs** relate, and how GitLab schedules them (stages in order, jobs in a stage in parallel).
- Define default and custom stages and name jobs so pipeline graphs are readable.
- Use `needs` to build a **DAG** so jobs start as soon as their real prerequisites finish, and know how it differs from `dependencies`.
- Fan out work with `parallel: N` and `parallel:matrix` (for example Python versions x browsers).
- Decide when a job runs using `rules` (`if`, `changes`, `exists`, `when`, `allow_failure`) and `workflow:rules`, and recognise legacy `only`/`except`.
- Control failure behaviour with `when`, `allow_failure`, `retry`, `timeout`, `interruptible`, and `resource_group`.
- Reuse configuration with hidden jobs, `extends`, `!reference`, `include`, and YAML anchors.
- Model deployments with `environment:` and introduce trigger/child pipelines.
- Design a complete `lint -> unit -> api -> a11y -> build -> deploy` pipeline and avoid the common mistakes.

---

## Why This Matters

This is the Week 7 epic: you are building a test automation suite for an API and an accessibility check, and wiring it into CI/CD so every change is verified automatically. Earlier today you learned what CI/CD is, how the pipeline lifecycle works, and the basics of `.gitlab-ci.yml`. This lesson is where that file stops being a toy and becomes a real design.

Picture a team with one giant job called `run-everything`. It takes 25 minutes, and when it goes red nobody knows whether the linter, the API tests, or the accessibility scan broke. Now picture the same checks split into well-named jobs inside well-ordered stages: lint finishes in 20 seconds, API and accessibility checks run side by side, and the red box says `a11y-scan`. Developers get faster feedback, the failure points at the cause, and your team can decide per job whether a failure blocks a release or merely warns.

As a QEA, choosing what runs, in what order, under what conditions, and with what consequences on failure is exactly your craft. Stages and jobs are how you express that judgment in code.

---

## The Concept

### 1. Jobs and Stages: The Execution Model

**What.** A **job** is the smallest unit of work: a named block with a `script` that runs on a runner in a clean environment. A **stage** is a named group of jobs. The `stages:` list sets the order of groups.

**Why.** Grouping gives you two things at once: ordering (do cheap checks before expensive ones) and parallelism (run independent checks at the same time).

**How GitLab schedules them** (the rules to memorise):

1. Stages run in the order listed.
2. Jobs in the same stage run in parallel, if enough runners are free.
3. A stage starts only when every job in the previous stage succeeded (unless you use `needs`, section 3).
4. If a job fails, later stages do not start by default.
5. Every job belongs to exactly one stage.

```
 stage 1: lint     stage 2: unit        stage 3: api            stage 4: deploy
 ┌──────┐          ┌────────────┐       ┌─────────────┐         ┌─────────┐
 │ ruff │  ──────► │ unit-tests │ ────► │ api-smoke   │ ─────►  │ staging │
 └──────┘          └────────────┘       │ api-regress │         └─────────┘
                                        └─────────────┘
                              (jobs in one stage run side by side)
```

#### Default stages

If you never write `stages:`, GitLab uses this built-in list: `.pre`, `build`, `test`, `deploy`, `.post`. A job with no `stage:` lands in `test`. That is why your very first pipeline with a bare `script` job showed up in a stage called "test".

#### Custom stages

Write your own list when the defaults do not describe your workflow:

```yaml
stages:
  - lint
  - unit
  - api
  - a11y
  - build
  - deploy

lint-code:
  stage: lint
  script:
    - echo "linting"
```

Line by line:

- `stages:` declares the ordered list. Order in this list is the run order. Jobs are listed in any order in the file; the list decides.
- `- lint` ... `- deploy` are the stage names. They are just labels you choose. A stage with no jobs is simply skipped.
- `lint-code:` is a job name (a top-level key that is not a reserved keyword).
- `stage: lint` attaches the job to the first stage. If you typo it as `stage: lnit`, GitLab rejects the file with "chosen stage does not exist".
- `script:` is the only required key; it lists shell commands. A non-zero exit code fails the job.

`.pre` and `.post` are special: they always run first and last regardless of the `stages:` list. Use them for setup or cleanup, but sparingly, because they make the order less obvious.

#### Job naming

Job names show up in the graph, notifications, and failure emails, so they matter.

- Use lowercase kebab-case that says what the job does: `api-smoke`, `a11y-scan`.
- Do not use reserved words as job names (`image`, `services`, `stages`, `variables`, `cache`, `include`, `default`, `workflow`, `before_script`, `after_script`).
- A name starting with a dot (`.setup`) is a hidden job and never runs (section 8).
- GitLab groups jobs in the graph by the text before `:`, `/`, or a space, so `test:api` and `test:mcp` collapse into a tidy group `test`.
- Job names must be unique in the whole pipeline, including included files; a duplicate silently overrides another.

#### Real-world scenario

A developer opens a merge request and fails lint after 15 seconds. Because lint is in an earlier stage, the 8-minute API suite never even starts. That is "fail fast" and it saves runner minutes and developer attention.

### 2. `needs` and the DAG, versus Stage Ordering and `dependencies`

**What.** `needs` lets a job declare exactly which jobs it waits for. GitLab then runs it the moment those jobs finish, even if other jobs in earlier stages are still running. The result is a **Directed Acyclic Graph (DAG)**: arrows have a direction and no loops.

**Why.** Stage ordering is simple but wasteful. If `a11y-scan` only needs the linted code, why should it wait for a slow unit job that has nothing to do with it?

```yaml
stages: [lint, unit, api]

lint-code:
  stage: lint
  script: [ruff check .]

slow-unit-tests:
  stage: unit
  script: [pytest -m unit]

api-smoke:
  stage: api
  needs: [lint-code]
  script: [pytest -m smoke]

api-contract:
  stage: api
  needs: []
  script: [pytest -m contract]
```

Line by line:

- `stages: [lint, unit, api]` is the same list in flow style (one line).
- `lint-code` and `slow-unit-tests` have no `needs`, so they follow normal stage rules.
- `api-smoke` has `needs: [lint-code]`. It starts as soon as `lint-code` succeeds, without waiting for `slow-unit-tests`.
- `api-contract` has `needs: []`, an empty list meaning "I depend on nothing". It starts immediately when the pipeline starts, even though its stage is third.
- A job's `stage:` still matters for display and for jobs that do not use `needs`.

Key facts:

- A job with `needs` downloads artifacts only from the jobs it needs (artifacts are covered in a later Friday lesson).
- `needs` can reference jobs in the same or an earlier stage, never a later one, and cycles (`a` needs `b`, `b` needs `a`) are errors.
- If a needed job might not exist (because of `rules`), write `needs: [{job: lint-code, optional: true}]`.
- Do not mix styles carelessly. A pipeline where half the jobs use `needs` and half rely on stages is hard to read. Pick one dominant approach.

**`needs` versus `dependencies`.** They are often confused:

| Keyword | Controls timing? | Controls artifact download? |
|---------|------------------|-----------------------------|
| `needs` | Yes: job starts when needed jobs finish | Yes: fetches artifacts from needed jobs |
| `dependencies` | No: stage order still applies | Yes: restricts which earlier jobs' artifacts to fetch |

`dependencies: []` means "download no artifacts", which speeds up jobs that do not need any.

### 3. Fan-out: `parallel` and `parallel:matrix`

#### `parallel: N`

**What.** Runs N identical copies of a job. GitLab sets `CI_NODE_INDEX` (1..N) and `CI_NODE_TOTAL` (N) in each copy.

**Why.** To split a long test run across several runners.

```yaml
api-regression:
  stage: api
  parallel: 4
  script:
    - pip install pytest-split
    - pytest -m regression --splits $CI_NODE_TOTAL --group $CI_NODE_INDEX
```

- `parallel: 4` creates `api-regression 1/4` through `4/4`.
- `pip install pytest-split` installs a plugin that can divide a test suite.
- `--splits $CI_NODE_TOTAL` says "divide the suite into 4 pieces"; `--group $CI_NODE_INDEX` says "this copy runs piece number N". Together every test runs exactly once.

Your 20-minute job becomes roughly 5 minutes plus startup overhead. Splitting only helps when tests are independent (isolation, from Wednesday's lessons).

#### `parallel:matrix`

**What.** Runs the same job once per combination of variable values.

**Why.** To cover a grid, such as every supported Python version against every browser.

```yaml
a11y-scan:
  stage: a11y
  image: python:$PY_VERSION
  parallel:
    matrix:
      - PY_VERSION: ["3.11", "3.12"]
        BROWSER: [chromium, firefox]
  script:
    - pip install -r requirements.txt
    - pytest -m accessibility --browser $BROWSER
```

Line by line:

- `image: python:$PY_VERSION` uses a matrix variable inside the image name; each job gets its own value.
- `parallel:` then `matrix:` opens the matrix, a list of "blocks".
- Inside the block, `PY_VERSION` has two values and `BROWSER` has two, so GitLab generates 2 x 2 = 4 jobs: `a11y-scan: [3.11, chromium]`, `a11y-scan: [3.11, firefox]`, and so on.
- The versions are quoted. Unquoted `3.10` would be parsed by YAML as the number 3.1, a classic bug.
- Each job gets `PY_VERSION` and `BROWSER` as environment variables for its script.
- `--browser` is an option provided by `pytest-playwright`.

Limits: a matrix can produce at most 200 jobs. Include the variable values in report filenames (for example `junit-$BROWSER.xml`) or the copies will overwrite each other's output.

Use `parallel: N` to split one workload; use `matrix` to repeat a workload under different conditions. They cannot be combined in the same job.

### 4. Controlling When a Job Runs: `rules`, `workflow:rules`, `only/except`

#### `rules`

**What.** `rules` is a list of conditions evaluated top to bottom. The first match wins and decides whether the job is added to the pipeline, and with what `when` and `allow_failure`. If nothing matches, the job is not created.

**Why.** Not every job belongs in every pipeline. Heavy suites might run only on the default branch; a docs check only when docs change.

```yaml
api-regression:
  stage: api
  script: [pytest -m regression]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - src/**/*
        - tests/**/*
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: always
    - if: $CI_COMMIT_BRANCH =~ /^experiment\//
      allow_failure: true
    - exists:
        - pytest.ini
      when: manual
    - when: never
```

Line by line:

- `rules:` starts the ordered list. Each `-` item is one rule.
- Rule 1: `if:` tests a CI variable. `$CI_PIPELINE_SOURCE == "merge_request_event"` is true for merge request pipelines. `changes:` adds a second condition: some file under `src/` or `tests/` was modified. Both must be true. With no `when`, the default is `on_success`.
- Rule 2: on the default branch, always run. `when: always` here means "run regardless of earlier-stage failures".
- Rule 3: `=~` is a regex match. Branches starting with `experiment/` run the job but `allow_failure: true` means a failure will not turn the pipeline red.
- Rule 4: `exists:` is true if the listed file exists in the repository. Here it makes the job manual if a `pytest.ini` exists.
- Rule 5: `when: never` with no condition is a catch-all: otherwise, do not run. Be explicit; a job with no matching rule is already excluded, but a final `when: never` documents intent.

The keywords:

| Clause | Meaning |
|--------|---------|
| `if` | Boolean expression on variables |
| `changes` | True if listed files changed (in merge requests, compared to the target branch) |
| `exists` | True if the listed files exist |
| `when` | What to do on match: `on_success`, `manual`, `always`, `never`, `delayed` |
| `allow_failure` | Whether this failure should block the pipeline |

#### `workflow:rules` (pipeline level)

`rules` decides per job; `workflow:rules` decides whether the **whole pipeline** is created at all.

```yaml
workflow:
  rules:
    - if: $CI_COMMIT_TITLE =~ /^WIP/
      when: never
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
```

- Rule 1 skips any pipeline whose commit title starts with "WIP".
- Rule 2 allows merge request pipelines (no `when` means the pipeline is created).
- Rule 3 blocks the branch pipeline if the branch already has an open merge request. This prevents the notorious **duplicate pipeline** (one for the branch push, one for the merge request).
- Rule 4 allows ordinary branch pipelines (branches with no open MR).

#### Legacy `only` / `except`

Older projects use `only: [main]` and `except: [schedules]`. These still work but are no longer developed and cannot express many conditions. If you see them in an existing file, understand them; in new files use `rules`. Never mix `rules` and `only/except` in the same job; GitLab rejects it.

### 5. Controlling Failure and Resources: `when`, `allow_failure`, `retry`, `timeout`, `interruptible`, `resource_group`

#### `when` values for a job

| Value | Behaviour | Typical use |
|-------|-----------|-------------|
| `on_success` (default) | Run if all earlier needed jobs succeeded | Normal jobs |
| `on_failure` | Run only if an earlier job failed | Collect diagnostics, notify |
| `always` | Run no matter what | Cleanup, publishing results |
| `manual` | Wait for a human to press Run | Production deploys |
| `delayed` | Run after `start_in` | Soak or canary checks |

```yaml
notify-failure:
  stage: deploy
  script: [./notify.sh "Pipeline failed"]
  when: on_failure

soak-check:
  stage: deploy
  script: [pytest -m smoke]
  when: delayed
  start_in: 10 minutes
```

- `notify-failure` appears and runs only when something earlier failed. If all is green it is skipped.
- `soak-check` waits ten minutes after becoming ready (`start_in` is required with `delayed`), useful for checking a deployment is still healthy after a short while.

Note: `manual` jobs are `allow_failure: true` by default, so a pipeline can pass without anyone pressing the button. Set `allow_failure: false` when the pipeline must wait for the click.

#### `allow_failure`

```yaml
a11y-best-practices:
  stage: a11y
  script: [pytest -m "accessibility and best_practice"]
  allow_failure: true

lint-code:
  stage: lint
  script: [ruff check .]
  allow_failure:
    exit_codes: [2]
```

- The first job can fail, shows an orange warning, and the pipeline continues. Use for experimental or advisory checks, and agree this with your team.
- The second ignores only exit code 2 (a tool's "warnings only" code) and fails on anything else.

#### `retry`, `timeout`, `interruptible`

```yaml
api-regression:
  stage: api
  script: [pytest -m regression]
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  timeout: 20 minutes
  interruptible: true
```

- `retry.max: 2` allows up to two automatic re-runs (three attempts total). Maximum allowed is 2.
- `retry.when` limits retries to infrastructure problems. Without it, GitLab retries any failure, which would hide flaky tests. **Retrying is not a cure for flakiness**; fix the cause.
- `timeout: 20 minutes` kills a hung job instead of waiting for the project default (often 60 minutes).
- `interruptible: true` says "if a newer pipeline starts on the same branch, you may cancel me". Great for tests, dangerous for deploys, so never set it on them. (The project setting "auto-cancel redundant pipelines" must be on.)

#### `resource_group`

```yaml
deploy-production:
  stage: deploy
  script: [./deploy.sh production]
  resource_group: production
```

- Jobs sharing the same `resource_group` name run one at a time. If two pipelines reach production simultaneously, the second waits. This prevents two deployments colliding.

### 6. Reuse: Hidden Jobs, `extends`, `!reference`, `include`, Anchors

Copy-pasted YAML drifts: you fix `image` in four places and forget the fifth. GitLab gives you several tools.

#### Hidden jobs and `extends`

```yaml
.python-test:
  image: python:3.12
  interruptible: true
  before_script:
    - pip install -r requirements.txt

api-smoke:
  extends: .python-test
  stage: api
  script: [pytest -m smoke]

unit-tests:
  extends: .python-test
  stage: unit
  script: [pytest -m unit]
  interruptible: false
```

- `.python-test` starts with a dot, so it is a **hidden job** (a template): never runs, only inherited.
- `extends: .python-test` copies its keys into the job. Keys in the child override the parent: `unit-tests` sets `interruptible: false`, replacing `true`.
- Hashes (maps) are merged deeply; lists such as `script` are replaced, not appended. That is a common surprise.
- A job can extend several templates: `extends: [.python-test, .on-main]`; later ones win.

#### `!reference`

When you want a single fragment (not the whole job), use `!reference [job, key]`:

```yaml
.setup:
  script:
    - pip install -r requirements.txt
    - playwright install chromium

a11y-scan:
  stage: a11y
  script:
    - !reference [.setup, script]
    - pytest -m accessibility
```

- `!reference [.setup, script]` pastes the two setup lines into this job's script, then `pytest` runs. Because it is spliced into a list, it solves the "lists are replaced" problem of `extends`.

#### `include`

Split a large pipeline into files, or share config across projects:

```yaml
include:
  - local: ci/templates.yml
  - project: qea/shared-ci
    ref: main
    file: /security.yml
  - template: Jobs/SAST.gitlab-ci.yml
```

- `local:` reads a file from the same repository (path from the repo root).
- `project:` pulls a file from another project; `ref` pins the branch or tag, and pinning a tag is safer than a moving branch.
- `template:` uses a GitLab-maintained template shipped with the product.
- Included content is merged with your file; your own keys win on conflict.

#### YAML anchors

```yaml
.defaults: &py_defaults
  image: python:3.12
  tags: [docker]

lint-code:
  <<: *py_defaults
  stage: lint
  script: [ruff check .]
```

- `&py_defaults` names a block; `<<: *py_defaults` merges it. Anchors are plain YAML and work only inside one file, not across `include`. Prefer `extends`; know anchors because you will see them.

### 7. Environments and Deployment Jobs

**What.** `environment:` tells GitLab a job deploys to a named place, such as `staging` or `production`.

**Why.** GitLab then tracks deployment history, shows a link to the live URL, and enables rollback.

```yaml
deploy-staging:
  stage: deploy
  script: [./deploy.sh staging]
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  needs: [deploy-staging]
  script: [./deploy.sh production]
  environment:
    name: production
    url: https://www.example.com
  resource_group: production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: false
```

- `environment.name` registers the deployment under Operate > Environments; `url` adds a clickable link.
- `deploy-production` needs staging, so a failed staging deploy blocks it.
- `resource_group` serialises production deploys.
- `when: manual` adds a Run button, the difference between Continuous Delivery (human approves) and Continuous Deployment (fully automatic). `allow_failure: false` makes the pipeline wait at that step instead of showing passed.
- `deploy.sh` is a placeholder; the point is the structure of the gates. Credentials for deploys come from CI/CD variables, covered in a later Friday lesson.

### 8. Trigger and Child Pipelines (Briefly)

A `trigger` job starts another pipeline instead of running a script.

```yaml
a11y-suite:
  stage: a11y
  trigger:
    include: ci/a11y-pipeline.yml
    strategy: depend
```

- `trigger:include` launches a **child pipeline** defined in another file in the same project; the parent keeps its overview and the child has its own stages. Useful for monorepos or very large pipelines.
- `strategy: depend` makes the trigger job wait and take on the child's status; without it, the trigger job succeeds as soon as the child starts.
- Use `trigger:project: group/other-project` to start a **multi-project pipeline** in a different repository.

For Week 7 a single pipeline is enough; know child pipelines exist for when yours outgrows one file.

### 9. Designing a Good Stage Layout

Principles:

| Principle | Why |
|-----------|-----|
| Cheapest and fastest first | Failing in 20 seconds beats failing in 10 minutes |
| One purpose per job | The red box tells you what broke |
| Independent suites share a stage | API and a11y do not depend on each other |
| Gates before deploy | Nothing ships unless required checks passed |
| Advisory checks are `allow_failure` | Warnings should not block merges |

The layout this week: `lint -> unit -> api -> a11y -> build -> deploy`.

| Stage | Purpose | Example job |
|-------|---------|-------------|
| `lint` | Style and syntax, seconds | `lint-code` |
| `unit` | Mocked tests, no network | `unit-tests` |
| `api` | API suites against a test environment | `api-smoke`, `api-regression` |
| `a11y` | Accessibility scans | `a11y-scan` |
| `build` | Package the app or image | `build-package` |
| `deploy` | Staging then gated production | `deploy-staging`, `deploy-production` |

#### Complete example

```yaml
stages: [lint, unit, api, a11y, build, deploy]

workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH

default:
  image: python:3.12
  interruptible: true
  before_script:
    - pip install -r requirements.txt

.test-job:
  timeout: 15 minutes
  retry:
    max: 1
    when: [runner_system_failure]

lint-code:
  stage: lint
  script:
    - ruff check .

unit-tests:
  extends: .test-job
  stage: unit
  script:
    - pytest -m unit -v

api-smoke:
  extends: .test-job
  stage: api
  needs: [lint-code]
  script:
    - pytest -m smoke -v

api-regression:
  extends: .test-job
  stage: api
  needs: [lint-code, unit-tests]
  parallel: 3
  script:
    - pip install pytest-split
    - pytest -m regression --splits $CI_NODE_TOTAL --group $CI_NODE_INDEX

a11y-scan:
  extends: .test-job
  stage: a11y
  needs: [lint-code]
  parallel:
    matrix:
      - BROWSER: [chromium, firefox]
  script:
    - playwright install $BROWSER
    - pytest -m accessibility --browser $BROWSER

a11y-best-practices:
  extends: .test-job
  stage: a11y
  needs: [lint-code]
  allow_failure: true
  script:
    - pytest -m "accessibility and best_practice"

build-package:
  stage: build
  needs: [api-smoke, api-regression, a11y-scan]
  script:
    - python -m build

deploy-staging:
  stage: deploy
  needs: [build-package]
  interruptible: false
  script: [./deploy.sh staging]
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  needs: [deploy-staging]
  interruptible: false
  script: [./deploy.sh production]
  environment:
    name: production
  resource_group: production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: false
```

Walkthrough:

- **`workflow:rules`**: pipelines exist for merge requests and for branches without an open MR, preventing duplicates.
- **`default:`** applies `image`, `interruptible`, and `before_script` to every job so you do not repeat them.
- **`.test-job`** is a hidden template: 15-minute timeout and one retry limited to runner crashes. Test jobs extend it.
- **`lint-code`** has no `needs`, so it starts at once.
- **`unit-tests`** is in stage `unit`; without `needs` it waits for lint to pass.
- **`api-smoke`** needs only lint, so it starts the moment lint is green, not after the unit stage.
- **`api-regression`** needs lint and unit, and is split three ways with `parallel: 3`.
- **`a11y-scan`** uses a matrix to run in two browsers; **`a11y-best-practices`** is advisory (`allow_failure: true`), so it never blocks.
- **`build-package`** needs the required test jobs (not the advisory one), forming the quality gate before packaging.
- **`deploy-staging`** runs only on the default branch and sets `interruptible: false` to override the `default`, since cancelling a deploy halfway is dangerous.
- **`deploy-production`** is manual, serialised, and waits for staging.

Merge request pipelines stop at `build-package` because both deploy jobs have rules that match only the default branch. That is intended.

### 10. Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Stage name typo in `stage:` | "chosen stage does not exist" | Match the `stages:` list exactly |
| Unquoted `3.10` in a matrix | Python 3.1 image not found | Quote versions: `"3.10"` |
| `needs` pointing to a job removed by `rules` | "job does not exist" error | Use `optional: true` or align rules |
| Using `retry` to hide flaky tests | Green pipelines, unstable suite | Retry only infrastructure failures; fix tests |
| Both branch and MR pipelines | Every push builds twice | Add `workflow:rules` |
| Mixing `rules` and `only/except` | Config validation error | Use `rules` only |
| Forgetting `allow_failure: false` on manual job | Pipeline "passes" with deploy never run | Set it explicitly |
| `interruptible: true` on deploys | A deploy cancelled midway | Set `false` for deploy jobs |
| Same report filename in matrix jobs | Reports overwrite each other | Put `$BROWSER` or `$CI_NODE_INDEX` in the name |
| Expecting `extends` to append lists | Parent `script` lines vanish | Use `!reference` |
| Duplicate job names across includes | One job silently replaces another | Keep names unique |
| Whole suite in one job | "It failed" with no clue why | One purpose per job |

If a job is missing from the pipeline, open **Build > Pipeline editor** and use the **Validate** tab to simulate the pipeline; check which `rules` matched.

### 11. Practice Exercises

**Exercise 1: Faster with `needs`.** This pipeline takes 8 minutes because `ui-check` waits for the slow `unit-tests`. Use `needs` so `ui-check` starts right after `lint-code`.

```yaml
stages: [lint, unit, ui]
lint-code:
  stage: lint
  script: [ruff check .]
unit-tests:
  stage: unit
  script: [pytest -m unit]
ui-check:
  stage: ui
  script: [pytest -m ui]
```

*Solution.* Add `needs: [lint-code]` to `ui-check`. It now starts when lint finishes (seconds) and runs alongside `unit-tests`. The pipeline duration drops from lint + unit + ui to lint + max(unit, ui). If `unit-tests` takes 5 minutes and `ui-check` takes 3, you save about 3 minutes. Keep `unit-tests` as is.

**Exercise 2: A matrix.** Run `pytest -m smoke` on Python 3.11 and 3.12, against `TEST_ENV` values `test` and `staging`.

*Solution.*

```yaml
api-smoke:
  stage: api
  image: python:$PY_VERSION
  parallel:
    matrix:
      - PY_VERSION: ["3.11", "3.12"]
        TEST_ENV: [test, staging]
  script:
    - pip install -r requirements.txt
    - pytest -m smoke --junitxml=junit-$PY_VERSION-$TEST_ENV.xml
```

This creates 2 x 2 = 4 jobs. Versions are quoted, and the report name includes both variables so the files do not clash.

**Exercise 3: Rules.** The job `docs-check` should run in merge requests only when files under `docs/` change; on the default branch always run; otherwise never. Write the rules.

*Solution.*

```yaml
docs-check:
  stage: lint
  script: [./check_docs.sh]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - docs/**/*
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - when: never
```

Rule 1 needs both an MR pipeline and a docs change. Rule 2 covers the default branch. Rule 3 is the explicit catch-all.

**Exercise 4: Reuse and a gate.** Three jobs repeat `image: python:3.12` and the same `before_script`. Refactor with a hidden job. Then add a manual production deploy that cannot be skipped.

*Solution.*

```yaml
.python-job:
  image: python:3.12
  before_script:
    - pip install -r requirements.txt

api-smoke:
  extends: .python-job
  stage: api
  script: [pytest -m smoke]

deploy-production:
  stage: deploy
  needs: [api-smoke]
  script: [./deploy.sh production]
  environment:
    name: production
  resource_group: production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: false
```

The hidden job holds shared settings. `needs: [api-smoke]` makes smoke failure block the deploy (a quality gate). `allow_failure: false` means the pipeline waits for a human decision.

### 12. Check Your Understanding (Quiz)

1. A job has `needs: []` and sits in the third stage. When does it start?
2. What is the difference between `needs` and `dependencies`?
3. How many jobs does `matrix: [{A: [1, 2, 3], B: [x, y]}]` create?
4. In a `rules` list, two rules would match. Which applies?
5. Which of these should have `interruptible: true`: a unit-test job or a production deploy?

**Answers.**

1. Immediately when the pipeline starts, because an empty `needs` list means no prerequisites and ignores stage order.
2. `needs` changes timing (start when the named jobs finish) and fetches their artifacts; `dependencies` only limits which earlier jobs' artifacts are downloaded and does not change timing.
3. Six (3 x 2).
4. The first matching rule; evaluation stops at the first match.
5. The unit-test job. Cancelling redundant test runs saves resources; cancelling a deploy halfway can leave a broken environment.

### 13. Glossary

### Stage
A named group of jobs; stages run in listed order.

### Job
A named unit of work with a `script`, run by a runner.

### DAG
Directed Acyclic Graph: jobs linked by `needs`, with no cycles.

### Hidden job
A job whose name starts with `.`; never runs, used as a template.

### Matrix
A `parallel:matrix` grid creating one job per variable combination.

### Rule
A condition in `rules` deciding if and how a job runs.

### Workflow rules
Conditions deciding whether the entire pipeline is created.

### Environment
A named deployment target tracked by GitLab, such as `staging`.

### Child pipeline
A separate pipeline started by a `trigger` job.

---

## Summary

- Stages run in order and jobs in a stage run in parallel; default stages are `.pre`, `build`, `test`, `deploy`, `.post`, and you can define your own.
- Name jobs clearly and uniquely; one purpose per job makes failures obvious.
- `needs` builds a DAG so jobs start as soon as prerequisites finish; `dependencies` only filters artifact downloads.
- `parallel: N` splits one workload; `parallel:matrix` repeats a job over combinations such as Python versions x browsers.
- `rules` (`if`, `changes`, `exists`, `when`, `allow_failure`) control jobs; `workflow:rules` control the whole pipeline; `only/except` is legacy.
- Use `when`, `allow_failure`, `retry` (infrastructure only), `timeout`, `interruptible`, and `resource_group` to control failure and safety.
- Reuse with hidden jobs, `extends`, `!reference`, `include`, and anchors.
- `environment:` plus manual gating models safe deployments; `trigger` starts child pipelines for large setups.
- A good layout is `lint -> unit -> api -> a11y -> build -> deploy`: fast and cheap first, gates before deploy.
- Artifacts and reports, and secrets and variables, are covered in later Friday lessons.

## Additional Resources

- GitLab Docs, *CI/CD YAML syntax reference*: https://docs.gitlab.com/ci/yaml/
- GitLab Docs, *CI/CD jobs*: https://docs.gitlab.com/ci/jobs/
- GitLab Docs, *Pipelines*: https://docs.gitlab.com/ci/pipelines/
- GitLab Docs, *Make jobs start earlier with needs*: https://docs.gitlab.com/ci/yaml/needs/
- GitLab Docs, *Environments*: https://docs.gitlab.com/ci/environments/
- `pytest-split` plugin: https://github.com/jerry-git/pytest-split
