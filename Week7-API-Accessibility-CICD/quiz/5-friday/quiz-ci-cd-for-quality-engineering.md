# Daily Knowledge Check: Week 7 Friday - CI/CD for Quality Engineering

This quiz checks your understanding of today's CI/CD lessons: continuous integration and deployment, the build-test-deploy lifecycle, GitLab CI/CD fundamentals, pipeline stages and jobs, test automation in pipelines, artifacts and reporting, and secrets and configuration management. Try each question first, then open the solution to check your reasoning.

**Format:** Part 1 Multiple Choice, Part 2 True/False, Part 3 YAML/Config Prediction, Part 4 Fill-in-the-Blank, Part 5 Matching.


## Part 1: Multiple Choice

### 1. Which description best matches "integration hell"?

- [ ] A) Merging many tiny changes into the shared branch several times a day
- [ ] B) Running too many jobs in parallel on a small number of runners
- [ ] C) Late, painful, risky merges that happen after long-lived branches have drifted apart
- [ ] D) A pipeline that has more stages than jobs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Late, painful, risky merges that happen after long-lived branches have drifted apart

**Explanation:** Long-lived branches accumulate differences, so the eventual merge is large, late and risky. CI avoids this by integrating small changes often with an automated build and tests.
- **Why others are wrong:**
  - A) That is the Continuous Integration practice that fixes integration hell, not the problem itself.
  - B) Runner capacity can cause queueing, but it is not what the lesson calls integration hell.
  - D) Stage and job counts have nothing to do with the merge pain that CI was created to solve.
</details>

### 2. A team makes every passing change releasable and packaged, but the product owner approves the final release to production with a button. Which practice is this?

- [ ] A) Continuous Delivery
- [ ] B) Continuous Deployment
- [ ] C) Continuous Integration only
- [ ] D) Integration hell

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Continuous Delivery

**Explanation:** Continuous Delivery keeps software always releasable with a manual release step. The human decision to release is what separates it from Continuous Deployment.
- **Why others are wrong:**
  - B) Continuous Deployment removes the human decision; every passing change goes to production automatically.
  - C) CI covers frequent merges with automated build and tests; it does not by itself guarantee an always-releasable packaged artifact.
  - D) That is the painful merge problem from long-lived branches, not a release practice.
</details>

### 3. Which DORA metric is the percentage of deployments that cause a problem needing a fix, rollback or hotfix?

- [ ] A) Deployment frequency
- [ ] B) Lead time for changes
- [ ] C) Mean time to restore (MTTR)
- [ ] D) Change failure rate

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Change failure rate

**Explanation:** Change failure rate is, for example, 4 failed deployments out of 100 = 4%, and lower is better. It is one of the two stability metrics.
- **Why others are wrong:**
  - A) This measures how often the team releases to production, not how many releases fail.
  - B) This is the time from a commit to that change running in production.
  - C) This is how long recovery takes after a failure, not the percentage of failing deployments.
</details>

### 4. Why does the lifecycle lesson insist on "build once, deploy many"?

- [ ] A) It saves disk space on the runner
- [ ] B) The exact artifact that passed the tests is the one that ships; a rebuild could pull fresh dependencies and change what you ship
- [ ] C) GitLab refuses to deploy an artifact more than once
- [ ] D) It lets each environment contain slightly different code

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The exact artifact that passed the tests is the one that ships; a rebuild could pull fresh dependencies and change what you ship

**Explanation:** A rebuild can pull in fresh dependencies, a different compiler state or a different base image. Promoting the same immutable artifact means a pass in dev or staging is evidence about what reaches production.
- **Why others are wrong:**
  - A) Storage is not the reason; the reason is that you would test one thing and ship another.
  - C) This is not a GitLab restriction; it is a good-practice rule about reproducibility.
  - D) Environments should differ only by configuration, never by code or build output.
</details>

### 5. An image is released as `myapi:2.4.1` after `myapi:2.4.0`, and the change only fixes a bug without breaking clients. Which part of semantic versioning changed?

- [ ] A) MAJOR, because every release must increase the major number
- [ ] B) MINOR, because any new tag increases the minor number
- [ ] C) PATCH, because it is a backwards-compatible bug fix
- [ ] D) None, because semver only applies to commit SHAs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) PATCH, because it is a backwards-compatible bug fix

**Explanation:** In MAJOR.MINOR.PATCH, a backwards-compatible bug fix bumps the PATCH number, here 2.4.0 to 2.4.1.
- **Why others are wrong:**
  - A) MAJOR changes (for example 1.x to 2.0.0) signal breaking changes that force clients to change.
  - B) MINOR signals new backwards-compatible features, for example 2.3.0 to 2.4.0.
  - D) Semver (MAJOR.MINOR.PATCH) and the commit SHA tag are two complementary labels; teams often use both.
</details>

### 6. Which deployment strategy keeps two complete environments, tests the new version on the idle one, then switches traffic in one step, giving instant rollback by switching back?

- [ ] A) Blue-green
- [ ] B) Canary
- [ ] C) Rolling
- [ ] D) Recreate

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Blue-green

**Explanation:** Blue-green deploys to the idle environment, validates it, then flips traffic. The cost is double the infrastructure during the release.
- **Why others are wrong:**
  - B) Canary sends a small share of real traffic (for example 5%) to the new version and increases it gradually.
  - C) Rolling replaces instances one at a time, so old and new versions run side by side for a while.
  - D) Recreate stops the old version completely before starting the new one, which causes a gap of downtime.
</details>

### 7. What is the main benefit of a feature flag?

- [ ] A) It removes the need for any automated tests
- [ ] B) It guarantees zero cost because old flags clean themselves up
- [ ] C) It rebuilds the artifact for each environment
- [ ] D) It separates "deployed" from "released": code can be deployed switched off and a bad feature turned off in seconds without redeploying

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It separates "deployed" from "released": code can be deployed switched off and a bad feature turned off in seconds without redeploying

**Explanation:** A feature flag is a configuration switch controlling exposure independent of deployment, giving an instant rollback by flipping the flag.
- **Why others are wrong:**
  - A) Tests are still needed, and they must cover both flag states.
  - B) Old flags must be cleaned up manually; flag management is the cost of this strategy.
  - C) Rebuilding per environment contradicts build once, deploy many; a flag is just a configuration switch.
</details>

### 8. Following fail-fast ordering, which check should run first in a typical pipeline?

- [ ] A) The full regression suite
- [ ] B) Lint and static checks
- [ ] C) Smoke tests on the shared staging environment
- [ ] D) Accessibility scans of every page

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Lint and static checks

**Explanation:** Cheapest, fastest and most informative checks go first. If lint fails in 10 seconds there is no reason to start a 20-minute regression.
- **Why others are wrong:**
  - A) This is slow and expensive; it should run after cheap checks have passed.
  - C) Smoke tests run after the deploy, near the end of the order.
  - D) Scans take minutes and need a running app, so they run after lint and unit tests.
</details>

### 9. A job in `.gitlab-ci.yml` has no `stage:` key and the file has no `stages:` list. In which stage does it run?

- [ ] A) build
- [ ] B) deploy
- [ ] C) test
- [ ] D) .pre

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) test

**Explanation:** The default stages are `.pre`, `build`, `test`, `deploy`, `.post`, and a job with no `stage:` lands in `test`.
- **Why others are wrong:**
  - A) `build` is a default stage, but jobs without `stage:` do not land there.
  - B) `deploy` is a default stage, but it is not the fallback for jobs without `stage:`.
  - D) `.pre` is a special stage that always runs first, but a job only goes there if you assign it.
</details>

### 10. Two jobs, `api-smoke` and `a11y-scan`, are in the same stage and enough runners are free. What happens?

- [ ] A) They run in parallel
- [ ] B) They run one after the other in alphabetical order
- [ ] C) Only the first one listed in the file runs
- [ ] D) The second waits until the first passes, because stages are sequential

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) They run in parallel

**Explanation:** Stages run in order, and jobs within the same stage run in parallel if enough runners are free.
- **Why others are wrong:**
  - B) Jobs in one stage run side by side, not sequentially.
  - C) Every job in a stage is created and run.
  - D) Stages are sequential; jobs inside a stage are not.
</details>

### 11. What does `needs: []` on a job mean?

- [ ] A) The job is skipped because it has no dependencies
- [ ] B) The job depends on nothing and starts immediately when the pipeline starts, even if its stage is late
- [ ] C) The job downloads artifacts from every earlier job
- [ ] D) The configuration is invalid because the list is empty

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The job depends on nothing and starts immediately when the pipeline starts, even if its stage is late

**Explanation:** `needs` builds a DAG; an empty list tells GitLab the job has no prerequisites, so it can start at once.
- **Why others are wrong:**
  - A) An empty `needs` list does not skip the job; it removes the wait on earlier stages.
  - C) `needs: []` means no dependencies, so it does not fetch artifacts from earlier jobs.
  - D) An empty list is valid and documented as "I depend on nothing".
</details>

### 12. Which statement correctly contrasts `needs` and `dependencies`?

- [ ] A) `dependencies` makes a job start early, while `needs` only filters downloads
- [ ] B) Both only control timing and neither affects artifacts
- [ ] C) They are aliases for the same keyword
- [ ] D) `needs` changes when a job starts, while `dependencies` only restricts which earlier jobs' artifacts are downloaded

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `needs` changes when a job starts, while `dependencies` only restricts which earlier jobs' artifacts are downloaded

**Explanation:** `needs` controls timing (and fetches artifacts from the needed jobs); `dependencies` leaves stage order alone and only limits downloads. `dependencies: []` downloads nothing.
- **Why others are wrong:**
  - A) This reverses the two keywords.
  - B) Both relate to artifacts: `needs` downloads from needed jobs and `dependencies` filters downloads.
  - C) They are different: only `needs` affects timing and builds the DAG.
</details>

### 13. Why should Python versions in a `parallel:matrix` be quoted, such as `"3.10"`?

- [ ] A) Unquoted `3.10` is parsed by YAML as the number 3.1, so the wrong image would be requested
- [ ] B) Quoted values run faster
- [ ] C) GitLab only accepts strings in the `stages:` list
- [ ] D) Unquoted versions are skipped by the matrix

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Unquoted `3.10` is parsed by YAML as the number 3.1, so the wrong image would be requested

**Explanation:** YAML reads an unquoted `3.10` as a float equal to 3.1, a classic bug that leads to a "Python 3.1 image not found" error.
- **Why others are wrong:**
  - B) Quoting has no effect on speed; it affects how YAML parses the value.
  - C) This is unrelated to the matrix problem and not a stated rule.
  - D) They are not skipped; they are silently converted to a number, creating a wrong image name.
</details>

### 14. In a job's `rules:` list, several conditions are written. How does GitLab evaluate them?

- [ ] A) All rules are evaluated and the last match wins
- [ ] B) Top to bottom; the first match decides, and if none match the job is not created
- [ ] C) Every rule must be true for the job to be created
- [ ] D) If nothing matches, the job runs with default settings

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Top to bottom; the first match decides, and if none match the job is not created

**Explanation:** `rules` is an ordered list: the first matching rule decides whether the job exists and with what `when` and `allow_failure`.
- **Why others are wrong:**
  - A) The first match wins, not the last.
  - C) Rules are alternatives evaluated in order, not a combined AND.
  - D) If nothing matches, the job is not added to the pipeline.
</details>

### 15. What is the purpose of `workflow:rules`?

- [ ] A) To decide which runner executes each job
- [ ] B) To replace `stages:` with an automatic order
- [ ] C) To set a different `expire_in` for artifacts
- [ ] D) To decide whether the whole pipeline is created at all, for example to prevent duplicate branch and merge request pipelines

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) To decide whether the whole pipeline is created at all, for example to prevent duplicate branch and merge request pipelines

**Explanation:** `rules` works per job; `workflow:rules` works at pipeline level. A rule that blocks branch pipelines when an open MR exists prevents the notorious duplicate pipeline.
- **Why others are wrong:**
  - A) Runner choice depends on tags, not on `workflow:rules`.
  - B) Stage ordering is defined by `stages:` and `needs`.
  - C) Artifact retention is configured under `artifacts:`.
</details>

### 16. A QE wants pytest's `junit.xml` kept so teammates can open it tomorrow and so the merge request shows a test summary. What should be used?

- [ ] A) A cache entry keyed by branch
- [ ] B) A predefined CI variable
- [ ] C) Artifacts, with `reports: junit` pointing at the file
- [ ] D) A `services:` container

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Artifacts, with `reports: junit` pointing at the file

**Explanation:** If a person or a later job needs a file, it is an artifact. `reports: junit` also makes GitLab parse the file to produce the Tests tab and MR widget.
- **Why others are wrong:**
  - A) Cache is a best-effort speed-up with no UI and no guarantee of availability.
  - B) Variables hold configuration values, not result files.
  - D) Services provide dependencies such as databases or mocks; they do not store results.
</details>

### 17. Why do test jobs usually add `artifacts: when: always`?

- [ ] A) Without it the job cannot run at all
- [ ] B) Artifacts upload only on success by default, but test reports are needed most when pytest fails and fails the job
- [ ] C) It makes artifacts never expire
- [ ] D) It forces the job to pass even when tests fail

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Artifacts upload only on success by default, but test reports are needed most when pytest fails and fails the job

**Explanation:** The default `when` is `on_success`. A failing test run fails the job, so without `when: always` you lose the evidence exactly when you need it.
- **Why others are wrong:**
  - A) The job runs fine; only the upload is skipped on failure.
  - C) Retention is controlled by `expire_in`, not by `when`.
  - D) `when` controls only the upload; `allow_failure` affects whether failure blocks the pipeline.
</details>

### 18. What does `reports: junit: reports/junit.xml` accomplish?

- [ ] A) It runs the tests in JUnit format automatically
- [ ] B) It converts the file into a cache entry
- [ ] C) It publishes the file on GitLab Pages
- [ ] D) The file is uploaded and GitLab parses it, showing the Tests tab and a merge request test summary

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The file is uploaded and GitLab parses it, showing the Tests tab and a merge request test summary

**Explanation:** `reports: junit` does two things: it uploads the XML like an artifact and GitLab parses it into the Tests tab with failure messages and MR summary.
- **Why others are wrong:**
  - A) pytest must still be told to write the file, for example with `--junitxml`.
  - B) Reports are artifacts, not cache.
  - C) Pages publishing needs a job named `pages` and a `public/` folder.
</details>

### 19. What does it mean when a CI/CD variable is flagged as Masked?

- [ ] A) The value is encrypted inside any artifact you upload
- [ ] B) The variable is only available on protected branches
- [ ] C) GitLab replaces an exact match of the value with `[MASKED]` in job logs
- [ ] D) The value can never appear in any output even if Base64-encoded

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) GitLab replaces an exact match of the value with `[MASKED]` in job logs

**Explanation:** Masking is a safety net on log output through exact string matching. Printing the secret in a changed form defeats it.
- **Why others are wrong:**
  - A) Masking applies to the job log, not to files you write.
  - B) That describes the Protected flag, not Masked.
  - D) Masking is exact string matching, so an encoded or split value can still leak.
</details>

### 20. What does a Protected variable do?

- [ ] A) It is only given to pipelines running on protected branches or protected tags
- [ ] B) It is hidden from every job log forever
- [ ] C) It is automatically rotated every 90 days
- [ ] D) It is stored inside the Git repository

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It is only given to pipelines running on protected branches or protected tags

**Explanation:** A feature-branch pipeline does not receive protected variables, creating a trust boundary for strong credentials.
- **Why others are wrong:**
  - B) Hiding in logs is the job of Masked.
  - C) Rotation is a practice you must schedule; the flag does not rotate anything.
  - D) Secrets must never live in the repository; variables live in Settings.
</details>

### 21. A developer realises a password was committed to the repository two days ago and quickly deletes it in a new commit. What is the correct FIRST step?

- [ ] A) Nothing more is needed because the file is deleted from the current tree
- [ ] B) Revoke or rotate the secret immediately and assume it was copied
- [ ] C) Rewrite history with `git filter-repo` and stop there
- [ ] D) Mask the value in the CI/CD variable settings

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Revoke or rotate the secret immediately and assume it was copied

**Explanation:** Rotating is the only step that actually ends the exposure. "I deleted the commit" is not "I fixed the leak."
- **Why others are wrong:**
  - A) Git history still contains it, so anyone with a clone can read it.
  - C) History cleanup is a later step and cannot remove copies in clones, forks and caches.
  - D) Masking only affects job logs and does not end the exposure of a leaked secret.
</details>

### 22. A project variable `API_TIMEOUT` is set in Settings, and the same name is defined in `.gitlab-ci.yml`. A normal push pipeline runs. Which value does the job use?

- [ ] A) The `.gitlab-ci.yml` value, because the file is committed
- [ ] B) Whichever was defined most recently in time
- [ ] C) Neither, because duplicates cause an error
- [ ] D) The project Settings value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The project Settings value

**Explanation:** Variables entered when running a pipeline manually beat project, group and instance variables, which beat job-level YAML, then global YAML, then predefined variables.
- **Why others are wrong:**
  - A) Settings variables outrank those defined in the YAML.
  - B) Precedence is a fixed order, not based on time.
  - C) Duplicate names are allowed; GitLab applies a fixed precedence.
</details>

### 23. A suite runs `pytest -m smoek` (a typo in the marker) and selects zero tests. What does the job do?

- [ ] A) It passes, because zero failures means success
- [ ] B) It fails with exit code 1, meaning some tests failed
- [ ] C) It fails with pytest exit code 5, because no tests were collected
- [ ] D) It is skipped automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It fails with pytest exit code 5, because no tests were collected

**Explanation:** pytest exit code 5 means no tests collected. GitLab treats any non-zero exit code as a failed job, which is the safe behaviour.
- **Why others are wrong:**
  - A) Zero tests collected returns code 5, which fails the job; a green run with no tests would be a lie.
  - B) Code 1 means some tests failed, but none ran here.
  - D) The job runs; the non-zero exit code makes it fail rather than skip.
</details>

### 24. How can a pipeline enforce "zero critical accessibility violations" using the Thursday axe tests?

- [ ] A) Assert in the test that the critical list is empty, so a violation makes pytest exit non-zero and the job fails
- [ ] B) Add `allow_failure: true` to the accessibility job
- [ ] C) Print the violations to the log and rely on a human to notice
- [ ] D) Mark the scan results file as a cache

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Assert in the test that the critical list is empty, so a violation makes pytest exit non-zero and the job fails

**Explanation:** All quality gates boil down to exiting non-zero when a condition is violated. Combine with **Pipelines must succeed** so a red pipeline blocks the merge button.
- **Why others are wrong:**
  - B) That would turn failures into warnings and weaken the gate.
  - C) A gate must exit non-zero when violated; reading logs is not enforcement.
  - D) Cache does not evaluate results or fail jobs.
</details>

### 25. A test job uses `services:` with `name: postgres:16` and `alias: db`. How should the tests reach the database?

- [ ] A) Using `localhost`, since services share the job's network namespace
- [ ] B) Using the hostname `db`, not `localhost`, and waiting until it accepts connections
- [ ] C) Using the runner's public IP address
- [ ] D) It needs no waiting because services start before the job finishes booting

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Using the hostname `db`, not `localhost`, and waiting until it accepts connections

**Explanation:** Services are reachable by alias, and because they boot in parallel with the job, poll for health (for example `pg_isready`) before running tests.
- **Why others are wrong:**
  - A) Services are separate containers, so `localhost` is a common mistake.
  - C) Services are reached by hostname or alias.
  - D) Services start in parallel with your job, so a health-wait loop is needed.
</details>


## Part 2: True/False

### 26. True or False: Variables flagged as Masked can never leak into job logs.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Masking is exact string matching on log output. A Base64-encoded, URL-encoded or split value is not matched and appears in plain text. Masking is a safety net, not permission to print secrets.
</details>

### 27. True or False: Artifacts and cache are the same feature, because both save files between jobs.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Artifacts keep and share results (reports, builds) and are uploaded to GitLab; cache is a best-effort speed-up (such as pip downloads) that can be missing at any time.
</details>

### 28. True or False: Continuous delivery means every passing change is automatically deployed to production.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** That describes Continuous Deployment. Continuous Delivery keeps a releasable build, with a human decision for the production release.
</details>

### 29. True or False: Jobs in the same stage run in parallel when enough runners are available.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Stages run in order, and jobs inside a stage run side by side if enough runners are free.
</details>

### 30. True or False: A `when: manual` job is allowed to fail by default, so a pipeline can pass without anyone pressing the button.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Manual jobs are `allow_failure: true` by default. Set `allow_failure: false` when the pipeline must wait for the click, for example before a production deploy.
</details>

### 31. True or False: Deleting the commit that contained a password in a later commit fixes the leak.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Git history still holds the value and clones, forks and caches may have it. You must rotate or revoke the secret first.
</details>

### 32. True or False: Adding GitLab `retry` to every test job is the recommended cure for flaky tests.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Retry should be limited to infrastructure failures (for example `runner_system_failure`) and can hide real flakiness or race conditions. Fix the cause, or quarantine with a ticket.
</details>

### 33. True or False: A variable defined in project Settings overrides a variable with the same name defined in `.gitlab-ci.yml`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Settings variables beat the YAML. If a YAML default is not taking effect, check Settings.
</details>

### 34. True or False: Variables you `export` in a job's `script` are still visible in its `after_script`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `after_script` runs in a separate shell, so exported variables are not visible there. It still runs even when the script failed.
</details>

### 35. True or False: A Playwright accessibility job and a PyTest API job placed in the same stage will run one after the other because they use different tools.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The tool is irrelevant: jobs in the same stage run in parallel if enough runners are free. This is why API tests and axe scans can share a stage for faster feedback.
</details>


## Part 3: YAML/Config Prediction

### 36. In this pipeline, `unit-tests` exits with code 1. What happens?

```yaml
stages: [lint, unit, api]

lint-code:
  stage: lint
  script: [ruff check .]

unit-tests:
  stage: unit
  script: [exit 1]

unit-docs:
  stage: unit
  script: [pytest -m docs]

api-smoke:
  stage: api
  script: [pytest -m smoke]
```

- [ ] A) `unit-docs` still runs in parallel, `api-smoke` does not start, and the pipeline fails
- [ ] B) Only `unit-tests` fails and `api-smoke` still runs
- [ ] C) Everything stops immediately, including `unit-docs`
- [ ] D) The pipeline passes because `api-smoke` never started

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `unit-docs` still runs in parallel, `api-smoke` does not start, and the pipeline fails

**Explanation:** Jobs in one stage run in parallel. A failure prevents later stages (`api`) from starting by default, so `api-smoke` is skipped.
- **Why others are wrong:**
  - B) Later stages do not start by default when a job fails.
  - C) `unit-docs` is in the same stage and runs in parallel, so it is not cancelled by this rule.
  - D) A failed job makes the pipeline fail; skipped later jobs do not turn it green.
</details>

### 37. Given this file, which statement about when jobs start is correct?

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

- [ ] A) Both api jobs wait until the whole `unit` stage finishes
- [ ] B) `api-contract` starts immediately at pipeline start; `api-smoke` starts as soon as `lint-code` succeeds, without waiting for `slow-unit-tests`
- [ ] C) `api-contract` waits for `lint-code`, and `api-smoke` starts immediately
- [ ] D) The file is invalid because `needs` cannot be an empty list

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `api-contract` starts immediately at pipeline start; `api-smoke` starts as soon as `lint-code` succeeds, without waiting for `slow-unit-tests`

**Explanation:** `needs` builds a DAG. `api-smoke` waits only for `lint-code`; `api-contract` with `needs: []` has no prerequisites at all.
- **Why others are wrong:**
  - A) `needs` lets them skip waiting for the whole previous stage.
  - C) The two are reversed: `needs: []` means no prerequisites; `needs: [lint-code]` waits for that job.
  - D) An empty list is valid and means the job depends on nothing.
</details>

### 38. A developer opens a merge request. What happens to the `regression` job in the MR pipeline?

```yaml
regression:
  stage: regression
  script: [pytest -q -m "regression and not live"]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      allow_failure: true
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

- [ ] A) It runs automatically as soon as the pipeline starts
- [ ] B) It is not created, because no rule matches merge requests
- [ ] C) It is created as a manual job with a Play button, and because `allow_failure: true` the pipeline can pass without it being run
- [ ] D) It blocks the pipeline until someone presses Play

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is created as a manual job with a Play button, and because `allow_failure: true` the pipeline can pass without it being run

**Explanation:** Rules are checked top to bottom and the first match wins. The first rule matches MR pipelines and makes the job manual and non-blocking.
- **Why others are wrong:**
  - A) The first matching rule sets `when: manual`, so it waits for a click.
  - B) The first rule matches `merge_request_event`.
  - D) With `allow_failure: true` an unrun manual job does not block the pipeline.
</details>

### 39. `unit` exits with code 1. Which of the later jobs run?

```yaml
stages: [test, notify]

unit:
  stage: test
  script: [exit 1]

notify-failure:
  stage: notify
  script: [./notify.sh "Pipeline failed"]
  when: on_failure

cleanup:
  stage: notify
  script: [./cleanup.sh]
  when: always

report:
  stage: notify
  script: [./report.sh]
```

- [ ] A) `notify-failure` and `cleanup` run; `report` is skipped
- [ ] B) Only `report`, because it has no `when`
- [ ] C) Only `notify-failure`, because `always` jobs run only when everything passes
- [ ] D) All three run, because they are in the same stage

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `notify-failure` and `cleanup` run; `report` is skipped

**Explanation:** `on_failure` runs only if an earlier job failed, `always` runs regardless, and the default `on_success` runs only if earlier jobs succeeded.
- **Why others are wrong:**
  - B) With the default `when: on_success`, `report` is skipped after a failure.
  - C) `when: always` runs no matter what, so `cleanup` runs too.
  - D) Stage placement does not override `when`; `report` uses the default `on_success`.
</details>

### 40. `a11y-best-practices` exits with code 1 while the other jobs pass. What is the outcome?

```yaml
stages: [test, deploy]

a11y-best-practices:
  stage: test
  script: [exit 1]
  allow_failure: true

smoke:
  stage: test
  script: [pytest -m smoke]

deploy:
  stage: deploy
  script: [./deploy.sh]
```

- [ ] A) The pipeline is red and `deploy` is skipped
- [ ] B) The job is retried automatically up to twice
- [ ] C) The job is skipped, not failed
- [ ] D) The job shows an orange warning and the pipeline continues, so `deploy` still runs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The job shows an orange warning and the pipeline continues, so `deploy` still runs

**Explanation:** `allow_failure: true` turns a job failure into a warning. Use it only for experimental or advisory checks agreed with the team.
- **Why others are wrong:**
  - A) `allow_failure: true` lets the pipeline continue past this failure.
  - B) No `retry` is configured, and `allow_failure` does not retry.
  - C) The job ran and failed, but the failure is allowed and shown as a warning.
</details>

### 41. What does this `allow_failure` setting do if `ruff check .` exits with code 2, and what if it exits with code 1?

```yaml
lint-code:
  stage: lint
  script: [ruff check .]
  allow_failure:
    exit_codes: [2]
```

- [ ] A) Both codes are tolerated
- [ ] B) Exit code 2 is tolerated as a warning; exit code 1 fails the job
- [ ] C) Exit code 1 is tolerated; exit code 2 fails the job
- [ ] D) Neither is tolerated, because `exit_codes` is not valid under `allow_failure`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Exit code 2 is tolerated as a warning; exit code 1 fails the job

**Explanation:** The job ignores only exit code 2 (a tool's "warnings only" code) and fails on anything else.
- **Why others are wrong:**
  - A) Only the listed exit codes are ignored.
  - C) The list contains 2, so 2 is the tolerated one.
  - D) `allow_failure: exit_codes` is valid and ignores only the listed codes.
</details>

### 42. How many `a11y-scan` jobs does this matrix generate, and what is wrong with the version values?

```yaml
a11y-scan:
  stage: a11y
  image: python:$PY_VERSION
  parallel:
    matrix:
      - PY_VERSION: [3.9, 3.10]
        BROWSER: [chromium, firefox]
  script:
    - pytest -m accessibility --browser $BROWSER
```

- [ ] A) 4 jobs; the unquoted `3.10` is parsed by YAML as the number 3.1, so versions should be quoted
- [ ] B) 2 jobs, because only the Python versions create jobs
- [ ] C) 4 jobs, and nothing is wrong
- [ ] D) 3 jobs, because `3.9` and `3.10` collapse into one value

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 4 jobs; the unquoted `3.10` is parsed by YAML as the number 3.1, so versions should be quoted

**Explanation:** `parallel:matrix` creates one job per combination, here 2 Python versions x 2 browsers = 4. Always quote versions such as `"3.10"`.
- **Why others are wrong:**
  - B) The matrix creates one job per combination: 2 x 2 = 4.
  - C) Unquoted `3.10` becomes 3.1, a classic bug.
  - D) They stay separate values, but 3.10 is read as 3.1; the job count is still 4.
</details>

### 43. `pytest` finds one failing test. What is uploaded as an artifact?

```yaml
api-regression:
  stage: test
  script:
    - mkdir -p reports
    - pytest -m regression --junitxml=reports/junit.xml
  artifacts:
    paths:
      - reports/
    expire_in: 7 days
```

- [ ] A) The whole `reports/` folder, because `paths` is set
- [ ] B) Nothing, because `when` defaults to `on_success` and the job failed
- [ ] C) Only `junit.xml`, for 7 days
- [ ] D) Only the files that Git tracks

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Nothing, because `when` defaults to `on_success` and the job failed

**Explanation:** The failing pytest run fails the job, so the default upload condition is not met. The fix is to add `when: always` so the evidence is kept.
- **Why others are wrong:**
  - A) Without `when: always`, artifacts upload only if the job succeeds.
  - C) `expire_in` affects retention, not whether the upload happens.
  - D) `untracked` is not set and tracking is not the criterion here.
</details>

### 44. What happens with `artifacts: false` in the `needs` of `api-regression`?

```yaml
generate-data:
  stage: build
  script:
    - python tools/make_testdata.py
  artifacts:
    paths:
      - testdata/generated/
    expire_in: 1 day

api-regression:
  stage: test
  needs:
    - job: generate-data
      artifacts: false
  script:
    - pytest -m regression
```

- [ ] A) It waits for the whole `build` stage and downloads everything
- [ ] B) It downloads the artifacts but ignores the job order
- [ ] C) `api-regression` starts as soon as `generate-data` finishes but does not download its artifacts, so the generated test data may be missing
- [ ] D) The configuration is rejected because `artifacts` is not allowed in `needs`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `api-regression` starts as soon as `generate-data` finishes but does not download its artifacts, so the generated test data may be missing

**Explanation:** `artifacts: false` orders the jobs but skips the download; use `artifacts: true` when the job needs the files.
- **Why others are wrong:**
  - A) `needs` already lets it start right after `generate-data`, and downloads are disabled.
  - B) `artifacts: false` keeps the ordering and skips the download.
  - D) `needs` can take `job:` with `artifacts: true` or `false`.
</details>

### 45. Settings contain a project variable `LOG_LEVEL=ERROR` and a group variable `LOG_LEVEL=CRITICAL`. The YAML below also defines it. Nobody runs a pipeline manually; it is an ordinary push. What does the `echo` print?

```yaml
variables:
  LOG_LEVEL: "INFO"

show-log-level:
  stage: test
  variables:
    LOG_LEVEL: "WARNING"
  script:
    - echo "Log level is $LOG_LEVEL"
```

- [ ] A) WARNING
- [ ] B) INFO
- [ ] C) CRITICAL
- [ ] D) ERROR

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) ERROR

**Explanation:** Precedence: manual or trigger or schedule values, then project, group, instance, inherited, job-level YAML, global YAML, deployment, predefined. Project beats group.
- **Why others are wrong:**
  - A) Job-level YAML has lower priority than project Settings variables.
  - B) Global YAML is the lowest of the user-defined sources here.
  - C) Within Settings the closest level wins, so project beats group.
</details>

### 46. What is wrong with this snippet from a secrets point of view?

```yaml
variables:
  API_BASE_URL: "https://staging.example.com/api"
  API_PASSWORD: "Passw0rd!"

api-tests:
  stage: test
  script:
    - pytest -m regression
    - env
```

- [ ] A) The password is committed in `variables:` and stays in Git history, and `env` dumps every variable into the job log
- [ ] B) Nothing is wrong, because pytest reads variables internally
- [ ] C) Only the URL is a problem because it is not masked
- [ ] D) `variables:` cannot hold strings with exclamation marks

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The password is committed in `variables:` and stays in Git history, and `env` dumps every variable into the job log

**Explanation:** Secrets belong in Settings (masked, protected) or a secret manager, never in the committed YAML. Never run `env`, `echo` a secret or use `set -x`.
- **Why others are wrong:**
  - B) Reading variables inside Python is safe, but the plain password in the YAML and the `env` command are not.
  - C) A staging URL is ordinary configuration; the password is the secret.
  - D) The syntax is valid; the problem is committing a secret.
</details>

### 47. What is the status of this job and why?

```yaml
smoke:
  stage: smoke
  script:
    - pytest -q -m smoek
```

- [ ] A) Passed: no tests failed
- [ ] B) Skipped: a job with no matching tests is skipped
- [ ] C) Failed: pytest exits with code 5 because the marker selects no tests, and any non-zero exit code fails the job
- [ ] D) Warning: pytest exit code 5 is treated as allowed failure

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Failed: pytest exits with code 5 because the marker selects no tests, and any non-zero exit code fails the job

**Explanation:** A wrong `-m` expression selects zero tests, giving exit code 5 and a red job, which is better than a green run with no tests.
- **Why others are wrong:**
  - A) Zero collected tests returns code 5, not 0.
  - B) GitLab marks jobs skipped when not run, but this job runs and exits non-zero.
  - D) No `allow_failure` is configured, so the failure is not softened.
</details>

### 48. All tests pass but total coverage is 72%. What is the result?

```yaml
check:
  stage: test
  script:
    - echo "start"
    - pytest -q -m "regression and not live" --cov=api --cov-fail-under=80
    - echo "finished"
```

- [ ] A) The job passes, because all tests passed
- [ ] B) `pytest` exits non-zero because of `--cov-fail-under=80`, the job fails, and `echo "finished"` never runs
- [ ] C) The job passes with an orange warning
- [ ] D) The job fails but `echo "finished"` still runs

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `pytest` exits non-zero because of `--cov-fail-under=80`, the job fails, and `echo "finished"` never runs

**Explanation:** Quality gates are "exit non-zero when violated". GitLab runs each script line in order, and the first non-zero exit code stops the script.
- **Why others are wrong:**
  - A) The coverage threshold makes pytest exit non-zero when coverage is below 80%.
  - C) A warning needs `allow_failure`, which is not set.
  - D) The first non-zero exit code fails the job and stops the script.
</details>


## Part 4: Fill-in-the-Blank

### 49. If you never declare `stages:`, GitLab uses the default order `.pre`, `build`, ______, `deploy`, `.post`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** test

**Explanation:** The default stage list is `.pre`, `build`, `test`, `deploy`, `.post`, and a job with no `stage:` lands in `test`.
</details>

### 50. The keyword ______ restricts which earlier jobs' artifacts a job downloads without changing the order in which jobs run.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `dependencies`

**Explanation:** `dependencies: []` downloads no artifacts. By contrast, `needs` controls both order and downloads.
</details>

### 51. The DORA metric "______" is the time from a commit to that change running in production.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Lead time for changes

**Explanation:** The four DORA metrics are deployment frequency, lead time for changes, change failure rate and mean time to restore.
</details>

### 52. The `coverage:` keyword holds a ______ that GitLab applies to the job log to extract the coverage percentage.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** regular expression (regex)

**Explanation:** The part in parentheses is captured as the percentage, for example 90 from a `TOTAL 480 48 90%` line.
</details>

### 53. A job named ______ publishes the contents of the `public/` folder as a static website with GitLab Pages.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `pages`

**Explanation:** The job must also list `public` under `artifacts: paths`.
</details>

### 54. A CI/CD variable of type ______ is written to a temporary file on the runner, and the variable contains the path to that file.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** File

**Explanation:** Use File type for multi-line or file-shaped secrets such as a service-account JSON key or a certificate.
</details>

### 55. A job whose `tags:` match no available runner waits forever in the ______ status.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** pending (created/pending)

**Explanation:** A tag mismatch is the most common reason for jobs that never start; the job exists but waits for a runner.
</details>

### 56. `retry: when:` should list only ______ failures such as `runner_system_failure`, so that flaky tests are not hidden.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** infrastructure (runner/system)

**Explanation:** Retrying infrastructure problems is acceptable; retrying product or test failures hides real problems.
</details>


## Part 5: Matching

### 57. Match each GitLab keyword (1-5) to its purpose (A-E).

| # | Item | | Letter | Description |
|---|------|---|--------|-------------|
| 1 | `needs: []` | | A | Kills a hung job instead of waiting for the project default |
| 2 | `resource_group` | | B | Allows a running job to be cancelled when a newer pipeline starts on the same branch |
| 3 | `interruptible: true` | | C | Decides whether the whole pipeline is created |
| 4 | `timeout` | | D | Makes jobs that share a name run one at a time, such as production deploys |
| 5 | `workflow:rules` | | E | Declares that a job depends on nothing and starts immediately |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-D, 3-B, 4-A, 5-C

**Explanation:** `needs: []` means no prerequisites; `resource_group` serialises jobs; `interruptible` allows auto-cancel (never on deploys); `timeout` caps a job; `workflow:rules` works at pipeline level.
</details>

### 58. Match each deployment strategy (1-5) to its description (A-E).

| # | Item | | Letter | Description |
|---|------|---|--------|-------------|
| 1 | Recreate | | A | Sends a small share of real traffic to the new version and increases it if monitoring looks healthy |
| 2 | Rolling | | B | Deploys code switched off and turns it on with a configuration setting, independent of deployment |
| 3 | Blue-green | | C | Stops the old version fully, then starts the new one, causing a gap of downtime |
| 4 | Canary | | D | Keeps two complete environments and switches traffic in one step |
| 5 | Feature flag | | E | Replaces instances gradually so old and new versions run side by side |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-D, 4-A, 5-B

**Explanation:** Recreate has downtime; rolling updates gradually; blue-green switches in one step with instant rollback; canary exposes a small share first; feature flags separate deployed from released.
</details>

### 59. Match each variable term (1-5) to its meaning (A-E).

| # | Item | | Letter | Description |
|---|------|---|--------|-------------|
| 1 | Masked | | A | Value is used exactly as typed, with no `$REFERENCE` substitution |
| 2 | Masked and hidden | | B | Only given to pipelines on protected branches or tags |
| 3 | Protected | | C | Applies only to jobs whose environment matches, such as `staging` |
| 4 | Raw (expand off) | | D | Replaced with `[MASKED]` in job logs on exact match |
| 5 | Environment scope | | E | Masked in logs and never shown again in Settings after saving |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-D, 2-E, 3-B, 4-A, 5-C

**Explanation:** Masked affects logs; masked and hidden also hides the value in Settings; protected limits which refs receive it; raw disables expansion; environment scope matches the job's `environment:`.
</details>
