# QA Review & Interview Questions: Week 7 Friday - CI/CD for Quality Engineering

## Part A: Artifact Review
Day: **5-friday - CI/CD for Quality Engineering**

### Written content
| Lesson | Words | Required sections | Fences balanced | Resource links | Later-day mentions |
|---|---|---|---|---|---|
| continuous-integration-and-deployment.md | 5,549 | yes | yes | 6 | 0 |
| build-test-deploy-lifecycle.md | 5,489 | yes | yes | 5 | 0 |
| gitlab-ci-cd-fundamentals.md | 4,992 | yes | yes | 6 | 0 |
| pipeline-stages-and-jobs.md | 4,862 | yes | yes | 6 | 0 |
| test-automation-within-pipelines.md | 5,342 | yes | yes | 7 | 0 |
| artifacts-and-reporting.md | 4,671 | yes | yes | 7 | 0 |
| secrets-and-configuration-management.md | 5,489 | yes | yes | 7 | 0 |

### Demo
| Item | Status |
|---|---|
| demos/5-friday/code/demo_ci_cd_for_quality_engineering.yaml | present |
| demos/5-friday/demo-script.md | present |
| demos/5-friday/diagrams/*.mermaid | 2 file(s) |

### Exercise
| Item | Status |
|---|---|
| exercise/5-friday/exercise-ci-cd-for-quality-engineering.md | present |
| starter_code/ | present |
| solution/ | present |
| 'Project 2 milestone' section | yes |

### Quiz
| Item | Status |
|---|---|
| quiz/5-friday/quiz-ci-cd-for-quality-engineering.md | present |
| Questions | 59 |
| Hidden-solution blocks | 59 |

### Issues found by the audit
- None

### Reviewer notes and open items for human sign-off

1. **Completeness.** All 7 written lessons, the demo (script, fully commented `.gitlab-ci.yml` as `demo_ci_cd_for_quality_engineering.yaml`, notes, helper scripts, a YAML consistency checker, 2 diagrams), the exercise (brief, merged Project 2 starter repo, solution pipeline) and the quiz (59 questions) are present.
2. **Lesson length.** The lessons are 4.7-5.5k words, slightly over the log's 10-20 minute guide, because of the depth standard. Use the Summary and Practice sections for a short read.
3. **No pipeline was run on a real GitLab.** The demo and solution YAML parse with PyYAML and pass stage/`needs` consistency checks, and the jobs' commands were run locally (merged repo: 77 tests passing; JUnit, HTML and coverage reports generated). Runner behaviour, the Playwright image tag (`v1.56.0-noble`, pinned to match the Playwright version installed during the build), `needs:parallel:matrix`, hidden variables and GitLab Pages are unverified. Rehearse on a real GitLab project before class.
4. **Internet needed.** The Tuesday smoke job needs internet access from the runner.
5. **QA fix applied.** Monday lessons said Newman would be "covered Friday", but Friday does not teach it. The wording now says it is outside this week's lessons.
6. **Lesson correction made during the build.** The old secrets draft ranked `.gitlab-ci.yml` variables above project variables. The final lesson ranks project, group and instance (Settings) variables above YAML-defined ones. Confirm against the current GitLab docs for the instance version used.
7. **Starter repo content.** The exercise's starter repo includes `storefront_fixed/` (Thursday's solution) because Friday's tests need it.
8. **Project 2 milestone.** The week closes with the milestone: a green pipeline with published reports and no secrets in the repo.

**Verdict:** Complete against the log; pending a real-GitLab rehearsal and the human sign-off items above.

### Week 7 cross-day summary

- **Totals:** 33 written lessons, 5 demos, 5 exercises (including Thursday's pair project) and 5 quizzes of 57-62 questions, 296 questions in total (57 + 59 + 62 + 59 + 59).
- **Stand-in Project 2 API:** the real Project 2 API spec was not provided, so exercises use a stand-in server; swap in the real API and re-check the contract before class.
- **Representative outputs:** curl, Postman and similar outputs in the lessons are representative, not captured live, because the build environment could not reach external hosts (for example JSONPlaceholder and httpbin).
- **Unrun items across the week:** the Postman collection and `pm.test` scripts were never run in Postman; Mermaid diagrams were not render-checked; no GitLab pipeline was run; the Playwright image tag, `needs:parallel:matrix`, hidden variables and GitLab Pages are unverified; the Tuesday smoke job needs internet.
- **Cross-day wording fix:** Monday's "Newman covered Friday" claim was corrected to "outside this week's lessons".
- **Pending sign-off:** the CMA verification checkbox remains for human sign-off.

---

## Part B: Interview Question Bank

## Beginner (Foundational)

### Q1: What is the difference between Continuous Integration, Continuous Delivery and Continuous Deployment?
**Keywords:** CI, continuous delivery, continuous deployment, manual release, automation
<details>
<summary>Click to Reveal Answer</summary>

Continuous Integration means developers merge small changes often and every change triggers an automated build and tests, with the rule that a broken build is fixed first. Continuous Delivery keeps the software always in a releasable state, but a person still presses the button to release. Continuous Deployment removes that button and releases every change that passes the pipeline automatically. The more automation you trust, the more your tests matter, because they become the only safety check.
</details>

---

### Q2: What problem does CI solve, and what is 'integration hell'?
**Keywords:** integration hell, long-lived branches, small changes, fast feedback
<details>
<summary>Click to Reveal Answer</summary>

Before CI, developers worked on long-lived branches and merged late, which produced painful, risky merges and surprises close to release. That is integration hell. CI fixes it by integrating small changes often, building and testing every change automatically, giving fast feedback and treating a broken build as the top priority.
</details>

---

### Q3: What are the four DORA metrics, and how does test automation affect them?
**Keywords:** DORA, deployment frequency, lead time, change failure rate, MTTR
<details>
<summary>Click to Reveal Answer</summary>

The four DORA metrics are deployment frequency, lead time for changes, change failure rate and mean time to restore (MTTR). The first two measure speed and the last two measure stability. Good test automation improves all of them: reliable automated checks let teams ship more often and faster, catch defects before release so fewer changes fail, and speed up finding and fixing problems when they do occur.
</details>

---

### Q4: Describe the build-test-deploy lifecycle and where QA validates at each step.
**Keywords:** source, build, test, package, deploy, monitor
<details>
<summary>Click to Reveal Answer</summary>

The lifecycle runs source, build, test, package, release, deploy and operate/monitor, with feedback to the team and a gate between phases. QA validates throughout: reviewing and checking changes at source, confirming the build is reproducible, running layered tests (unit, API, accessibility, smoke), checking the packaged artifact, and verifying health and smoke checks after deployment. Failures are triaged by cause and the right people are notified.
</details>

---

### Q5: What does 'build once, deploy many' mean and why does it matter?
**Keywords:** immutable artifact, versioning, semver, promotion, configuration
<details>
<summary>Click to Reveal Answer</summary>

The software is built and packaged once into an immutable, versioned artifact (semantic version plus commit SHA), and that same artifact is promoted from dev to staging to production. Environments differ only by configuration, not by code. This means what you tested is exactly what you ship, and rollback is simple because older versioned artifacts still exist.
</details>

---

### Q6: What is `.gitlab-ci.yml` and how do pipelines, stages and jobs relate?
**Keywords:** gitlab-ci.yml, pipeline, stage, job, script
<details>
<summary>Click to Reveal Answer</summary>

GitLab reads `.gitlab-ci.yml` from the repository root and creates a pipeline when an event such as a push, merge request, schedule or manual run occurs. A pipeline is made of stages that run in order, and jobs inside a stage that run in parallel. A job is a `script`, and it fails on any non-zero exit code, which is how tests pass or fail a pipeline.
</details>

---

### Q7: What is a GitLab Runner and what do shared versus project runners mean?
**Keywords:** runner, executor, docker, shared runner, image
<details>
<summary>Click to Reveal Answer</summary>

Runners are the agents that execute pipeline jobs. They may be shared across many projects or specific to one project. With the docker executor, each job gets a fresh container started from the `image` named in the configuration, so jobs are isolated and reproducible.
</details>

---

### Q8: How does `needs` differ from normal stage ordering and from `dependencies`?
**Keywords:** needs, DAG, stages, dependencies, artifacts
<details>
<summary>Click to Reveal Answer</summary>

By default a job waits for every job in earlier stages to finish. `needs` builds a directed acyclic graph (DAG), so a job starts as soon as the jobs it names have finished, regardless of stage. `dependencies` does not change timing at all; it only filters which jobs' artifacts are downloaded.
</details>

---

### Q9: What is the difference between artifacts and cache in GitLab CI?
**Keywords:** artifacts, cache, expire_in, results, speed
<details>
<summary>Click to Reveal Answer</summary>

Artifacts are job results uploaded to GitLab so people and later jobs can use them, such as test reports, with retention set by `expire_in`. Cache is a best-effort speed-up, for example pip downloads, that is restored on the runner and must not be relied on for results. Use artifacts for outputs and cache only for dependencies you could re-download.
</details>

---

### Q10: How do JUnit XML, coverage and GitLab Pages make test results visible?
**Keywords:** JUnit, Tests tab, coverage, Cobertura, Pages
<details>
<summary>Click to Reveal Answer</summary>

`reports: junit` uploads JUnit XML so GitLab shows the Tests tab and a merge request summary. Coverage is measured with pytest-cov, shown using the `coverage:` regex, and `coverage_report` with Cobertura XML shows line coverage in the merge request diff. HTML reports such as pytest-html can be published with a `pages` job so anyone can read them in a browser.
</details>

---

### Q11: What is the difference between configuration and secrets, and why must secrets never be committed?
**Keywords:** configuration, secrets, environment variables, twelve-factor, git history
<details>
<summary>Click to Reveal Answer</summary>

Configuration is non-sensitive and varies by environment, while secrets are credentials such as passwords, keys and tokens. Both reach the code as environment variables, following the twelve-factor rule, and the code never contains the values. Git remembers everything, so a committed secret is compromised even after you delete it.
</details>

---

### Q12: What do masked and protected CI/CD variables do?
**Keywords:** masked, protected, variable, branch, job log
<details>
<summary>Click to Reveal Answer</summary>

A masked variable has its value hidden in job logs, although it can still leak if printed in a transformed way. A protected variable is only provided to pipelines on protected branches and tags. Secrets belong in GitLab Settings variables rather than in the YAML, with these flags chosen to limit where they are exposed.
</details>

---

### Q13: What is a quality gate, and why do the test pyramid and 'shift left' matter?
**Keywords:** quality gate, test pyramid, shift left, required checks, merge request
<details>
<summary>Click to Reveal Answer</summary>

A quality gate turns a test result into a decision, such as an exit code, a coverage threshold, zero critical accessibility violations, or the merge request setting 'Pipelines must succeed'. The test pyramid says to have many fast unit tests, fewer API tests, and few slow UI tests. Shifting left means finding defects earlier, when they are cheapest to fix.
</details>

---

## Intermediate (Application)

### Q14: You want smoke tests on merge requests, the full regression on main and everything on a nightly schedule. How do you configure that, and how would you make one non-critical job non-blocking?
**Keywords:** rules, workflow:rules, schedule, allow_failure, smoke
**Hint:** Think about job-level versus pipeline-level control.
<details>
<summary>Click to Reveal Answer</summary>

Use `rules` with conditions such as `if` on the pipeline source and branch to include each job only where it should run, for example smoke on merge requests, regression on main and all suites on scheduled pipelines. `workflow:rules` control whether the whole pipeline is created, and `only/except` is the legacy approach. Setting `allow_failure` makes a job's failure show a warning without blocking the pipeline, which suits an advisory check.
</details>

---

### Q15: Your pipeline fails intermittently on a test that passes when re-run. How do you handle it?
**Keywords:** flaky test, retry, quarantine, root cause, ticket
**Hint:** Consider what a blanket retry hides.
<details>
<summary>Click to Reveal Answer</summary>

Treat flakiness as a defect: find and fix the cause first, because it erodes trust in the pipeline. Retry only for known transient errors such as infrastructure problems, never blanket re-run assertions, which hides real bugs. If it cannot be fixed immediately, quarantine the test with a ticket so it is tracked rather than ignored.
</details>

---

### Q16: A developer accidentally commits an API token to the repository. What do you do, and in what order?
**Keywords:** rotate, revoke, history, investigate, secret scanning
**Hint:** Which action stops the harm fastest?
<details>
<summary>Click to Reveal Answer</summary>

Rotate the credential first, because it must be treated as compromised even after deletion. Then clean up the repository history, investigate whether it was used, and report the incident. Afterwards add secret scanning (for example GitLab Secret Detection or gitleaks) and move the value into masked, protected variables in Settings.
</details>

---

### Q17: A test job fails, but when you open the pipeline there are no screenshots or reports to download. What is likely wrong and how do you fix it?
**Keywords:** artifacts, when: always, expire_in, reports, evidence
**Hint:** Think about what happens to artifacts when a job exits non-zero.
<details>
<summary>Click to Reveal Answer</summary>

By default, artifacts are only uploaded when a job succeeds, so a failing job keeps no evidence. Add `when: always` to the `artifacts` block, together with sensible `paths`, `name` and `expire_in`, so reports, screenshots, traces and logs are kept from failed runs. Keep retention short and artifacts small, and make sure they contain no secrets.
</details>

---

## Advanced (Deep Dive)

### Q18: Design how a pipeline should handle credentials for a deployment job: where they live, who can use them, which value wins when names clash, and how to avoid long-lived secrets.
**Keywords:** precedence, protected variables, environment scope, least privilege, OIDC
**Hint:** Combine variable flags, branch protection and short-lived credentials.
<details>
<summary>Click to Reveal Answer</summary>

Store secrets in project, group or instance Settings variables, never in the YAML, using the Masked (or masked and hidden), Protected and environment-scoped options. Precedence is pipeline-run values over project, group and instance variables, over YAML-defined ones, over predefined ones. Because protected variables only reach protected branches and tags, a two-tier design gives feature branches low-privilege test credentials and protected branches the production ones. Apply least privilege and rotation, add secret scanning, and where possible use a secret manager such as Vault or OIDC, where the job presents a signed short-lived ID token and receives temporary credentials, so nothing long-lived is stored. In code, read required values with `os.environ[...]`, fail fast with messages that name but never reveal the variable, and never `echo`, run `env` or `set -x` on secrets.
</details>

---
