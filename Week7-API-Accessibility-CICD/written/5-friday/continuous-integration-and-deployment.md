# Continuous Integration and Deployment

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the integration problem that existed before CI ("integration hell") and why long-lived branches cause it.
- Describe the core **Continuous Integration (CI)** practices and why each one exists.
- Define **Continuous Delivery** and **Continuous Deployment** and state precisely how they differ.
- Name the four **DORA metrics** and explain what they tell a team.
- Describe a pipeline in tool-neutral terms: trigger, stages, jobs, gates, and artifacts.
- Recognise the main CI tools (GitLab CI, GitHub Actions, Jenkins, CircleCI, Azure DevOps).
- Explain how automated tests act as **quality gates**, using the test pyramid and the idea of **shift-left**.
- Describe branching strategies and merge requests with required checks.
- Diagnose typical pipeline failures, including flaky tests.
- Say where this week's API tests and accessibility scans fit in a pipeline, and what a QA engineer does in CI/CD.

---

## Why This Matters

This week's epic is about three connected skills: **API testing** (Monday to Wednesday), **accessibility testing** (Thursday), and **CI/CD** (today). Each skill alone is useful. Together they form a safety net. Your API tests check that the service behind the screen behaves correctly. Your accessibility scans check that the screen can be used by everyone. CI/CD is the machinery that runs both of them automatically, on every change, on a machine that is not your laptop.

Without CI, tests depend on someone remembering to run them. A suite that runs "when there is time" is soon forgotten, and then it rots: tests fail for reasons nobody investigates, and the team stops trusting them. With CI, the question "does the latest code still work?" is answered in minutes, every time anyone changes anything. Test automation delivers most of its value **inside a pipeline**. Today you learn the ideas; the remaining Friday lessons teach the practical details.

Employers also expect it. Almost every QA automation job description mentions pipelines. Being able to say "I wrote API tests and accessibility checks and wired them into the pipeline as merge gates" is a strong, concrete statement.

---

## The Concept

### 1. The Problem Before CI: Integration Hell

#### What it was

Picture a team of five developers working on one product. In the old style of working, each developer took a copy of the code and worked on a long-lived **branch** (a separate line of development) for weeks. At the end of the project, or the end of the month, everyone tried to **integrate**: combine all branches into one working product.

That moment was painful enough to earn a nickname: **integration hell**. What typically happened:

- Two developers changed the same file in different ways, producing **merge conflicts**.
- Developer A renamed a function that developer B was calling in new code. Each branch worked alone; together they broke.
- Nobody remembered why a change was made three weeks ago, so resolving conflicts meant guessing.
- Testing started only after integration, so defects were found late, when many changes were mixed together and the cause was hard to locate.
- Releases were rare, huge, risky, and stressful. Teams scheduled "integration weeks" and "code freezes".

#### Why long-lived branches cause it

The cost of a merge grows faster than the size of the change. If two branches drift apart for one day, the difference is small and everyone still remembers it. If they drift apart for a month, the differences interact: change X depends on change Y, which conflicts with change Z. The problem is not linear; it compounds.

**Analogy:** Five co-authors write a book. If each writes alone for a month and then merges chapters, they discover contradictory plots, a character who dies twice, and duplicated chapters. If they share their draft every day and a proofreader checks continuity each time, any contradiction is tiny and cheap to fix.

#### Real-world scenario

A retail team keeps a "payments" branch for six weeks while another team changes the shopping basket on `main`. When the branches meet, the basket total is calculated in two different ways, and checkout fails in 14 places. Three developers spend a week fixing it, and the release slips. With daily integration, the first disagreement would have shown up on day two, as a one-file fix.

#### The principle that fixes it

If something is painful, do it more often, in smaller pieces, until it stops being painful. That is the heart of CI: **integrate often, and check every integration automatically.**

### 2. Continuous Integration (CI)

**Continuous Integration** is the practice of developers **merging their changes into a shared mainline frequently (at least daily)**, where every merge triggers an **automated build and automated tests**. The word "continuous" does not mean "literally nonstop"; it means "so often that integration is never a big event".

#### The practices, step by step

| Practice | What it means | Why it exists |
|----------|---------------|---------------|
| **One shared repository** | All code, tests, and the pipeline definition live in version control (Git) | Everyone works from the same truth; the build can be reproduced |
| **Frequent merges** | Merge to the shared branch at least daily | Keeps differences small, conflicts rare |
| **Trunk-based or short-lived branches** | Work on `main` ("trunk") directly, or on branches that live hours to a couple of days | Prevents long-lived branch drift |
| **Automated build** | One command or one pipeline builds the system from scratch | Removes "it only builds on Sam's laptop" |
| **Self-testing build** | Tests run on every build | A change that breaks behaviour is caught at once |
| **Fast feedback** | Results arrive in minutes (a common target is under 10) | Developers still remember the change and fix it cheaply |
| **Fix a broken build first** | When the build is red, fixing it is the team's top priority | A red mainline blocks everyone and hides new failures |
| **Production-like test environment** | Use containers and consistent configuration | "Works on my machine" stops being an excuse |
| **Visible results** | Status is visible to everyone | Quality is a team property, not a secret |
| **Pipeline as code** | The pipeline is a file in the repository, reviewed like any code | Changes to the process are tracked and reviewable |

#### What "fix the broken build first" looks like

Suppose the build turns red at 10:15. Good teams react immediately: the person whose commit caused it either fixes it within minutes or **reverts** the commit. Nobody merges new work on top of red. Bad teams say "someone will look at it later"; by afternoon three more commits are stacked on the failure and nobody knows which one broke what. The rule exists because a red mainline destroys the entire point of fast feedback.

#### Real-world scenario

At 11:00 a developer pushes a small change to how an order total is rounded. Within six minutes the pipeline reports that an API test expecting `19.99` now receives `20.00`. The developer, still in the middle of the same task, sees it, fixes the rounding rule, and pushes again. Total cost: ten minutes. Without CI, the same bug might surface in testing next week, mixed up with forty other changes.

### 3. Continuous Delivery vs Continuous Deployment

These two terms are often confused, and both abbreviate to "CD". Learn the difference carefully.

**Continuous Delivery** extends CI. After the tests pass, the software is automatically built, packaged, and prepared so that it **could be released to production at any moment**. The final step, releasing to real users, is a **human decision** (a button, an approval).

**Continuous Deployment** removes that human decision. **Every change that passes all automated checks is released to production automatically.**

| | Continuous Integration | Continuous Delivery | Continuous Deployment |
|---|---|---|---|
| Frequent merges, automated build and tests | Yes | Yes | Yes |
| Always-releasable, packaged artifact | Not necessarily | Yes | Yes |
| Release to production | Not included | **Manual** approval | **Automatic** |
| Who decides to release | Humans, separately | A person (business or team) | The pipeline, based on checks |
| Dependence on test quality | High | Very high | **Extreme** |

The last row matters most for you. In Continuous Deployment, **nothing stands between a commit and your customers except the automated checks**. If your tests are weak, bad code ships automatically. This is why test automation engineers are so valuable in mature CD setups.

#### How to choose

- Regulated or high-risk domains (banking, medical, some government systems) often use Continuous Delivery: automation up to the release, then a documented human approval.
- Web products with good monitoring and fast rollback often use Continuous Deployment, sometimes dozens of releases per day.
- Many teams start with delivery and move to deployment as trust in their tests grows.

**Quick mnemonic:** *Delivery = "deliverable at any time, you choose when". Deployment = "deployed automatically, no choosing".*

#### Real-world scenario

A bank's mobile app team uses Continuous Delivery. Each merged change produces a tested release candidate, and the product owner approves releases every Thursday after reviewing the change list. A marketing website team at the same bank uses Continuous Deployment: a copy fix merged at 14:05 is live at 14:12.

### 4. Why It Pays Off: Benefits and the DORA Metrics

#### Benefits

- **Faster feedback:** defects are found minutes after introduction.
- **Smaller, safer releases:** a release with three changes is easy to diagnose; one with three hundred is not.
- **Less stress:** releases become routine rather than events.
- **Fewer integration surprises:** the mainline always builds and passes tests.
- **Better use of people:** machines run repetitive checks so humans do exploratory work.

#### Measuring it: the four DORA metrics

The DevOps Research and Assessment (DORA) programme studied thousands of teams and identified four metrics that distinguish high-performing delivery teams. Two measure **speed** and two measure **stability**.

| Metric | Plain meaning | Example | Better is |
|--------|---------------|---------|-----------|
| **Deployment frequency** | How often the team releases to production | 12 deployments per week | Higher |
| **Lead time for changes** | Time from a commit to that change running in production | 2 hours | Shorter |
| **Change failure rate** | Percentage of deployments that cause a problem needing a fix, rollback, or hotfix | 4 of 100 deployments = 4% | Lower |
| **Mean time to restore (MTTR)** | How long it takes to recover when a failure happens | 25 minutes | Shorter |

A key finding is that speed and stability are **not a trade-off**. Teams that deploy often with small changes tend to also have lower failure rates and faster recovery, because small changes are easier to test, understand, and undo.

#### Where QA affects the metrics

- Reliable, fast automated tests shorten **lead time** (no waiting for manual regression).
- Good gates lower the **change failure rate**.
- Clear failure reports and good smoke tests after deployment shorten **MTTR**.
- Flaky or slow suites hurt both **deployment frequency** and **lead time**.

Treat metrics as a conversation starter, not a weapon. If people are punished for a high failure rate, they will hide failures instead of fixing the process.

### 5. The Pipeline Concept (Tool-Neutral)

A **pipeline** is an automated workflow that takes a change from source code to a verified (and possibly deployed) result. Every CI tool has this idea, with different names. The vocabulary:

- **Trigger:** the event that starts the pipeline. Examples: a push to a branch, opening a merge request, a schedule (nightly), a manual click, or another pipeline finishing.
- **Stage:** a phase of the pipeline, such as build, test, or deploy. Stages run in order; a later stage starts only when the earlier stage succeeds.
- **Job:** a single unit of work inside a stage, such as "run API tests". Jobs in the same stage can run in parallel.
- **Runner / agent:** the machine or container that actually executes a job.
- **Gate:** a condition that must be true for the change to move on, for example "all required jobs passed" or "a person approved".
- **Artifact:** a file produced by a job and stored for later use: a build package, a test report, a screenshot, a log.

#### A simple pipeline diagram

```
 TRIGGER            STAGE 1        STAGE 2            STAGE 3         STAGE 4
 (push / MR)         BUILD           TEST              PACKAGE         DEPLOY
┌────────────┐    ┌─────────┐   ┌─────────────┐    ┌───────────┐   ┌────────────┐
│ developer  │    │ compile │   │ unit tests  │    │ create    │   │ staging    │
│ pushes     │──► │ install │──►│ API tests   │──► │ artifact  │──►│ (auto)     │
│ a change   │    │ lint    │   │ a11y scan   │    │ (image/   │   │     │      │
└────────────┘    └─────────┘   └─────────────┘    │  zip)     │   │     ▼      │
                                     │             └───────────┘   │ production │
                                     ▼                             │ (manual or │
                            test reports (artifacts)               │  auto)     │
                                                                   └────────────┘
   GATE: if any job in a stage fails, later stages do not run
```

#### Reading the diagram

1. A **trigger** starts the pipeline. The developer did nothing special beyond pushing.
2. In the **build** stage the code is prepared: dependencies installed, code compiled or linted.
3. The **test** stage runs several jobs in parallel (unit, API, accessibility). They are the quality gate. If any required job fails, the arrow to the next stage is cut.
4. Reports are saved as **artifacts** so humans can read them after the runner disappears.
5. The package stage produces the thing that will be deployed. Good practice is **build once, deploy the same artifact everywhere**, so what you tested is what you ship.
6. The deploy stage pushes to staging, and then to production either automatically (Continuous Deployment) or after a click (Continuous Delivery).

#### A minimal generic example

Most tools describe a pipeline in a text file stored in the repository. This is deliberately generic pseudo-configuration, not a real tool's syntax:

```yaml
stages: [build, test]

run-api-tests:
  stage: test
  run:
    - install dependencies
    - run the API test suite
```

Line by line:

- `stages: [build, test]` declares the ordered phases. Test comes after build.
- `run-api-tests:` names one job. The name appears in the pipeline view.
- `stage: test` places that job in the test stage.
- `run:` lists commands the runner executes, top to bottom. If any command fails, the job fails, which turns the pipeline red.

The real syntax, stages and jobs in depth, artifacts, and secrets each have their own lesson later today; here you only need to know that a pipeline is a repository file that a tool turns into automated work.

### 6. The CI Tool Landscape

| Tool | Notes |
|------|-------|
| **GitLab CI/CD** | Built into GitLab; the pipeline lives in a file in the repository; the tool used in this course |
| **GitHub Actions** | Built into GitHub; workflows are files in the repository; large marketplace of reusable actions |
| **Jenkins** | Long-established, self-hosted, extremely extensible through plugins; needs more maintenance |
| **CircleCI** | Hosted service with a strong focus on speed and caching |
| **Azure DevOps Pipelines** | Microsoft's offering; popular in organisations that use Azure and Microsoft tooling |

Others exist (Bitbucket Pipelines, TeamCity, and deployment-focused tools), but the five above are what you will meet most often.

The **ideas are the same everywhere**: triggers, stages, jobs, runners, artifacts, variables, secrets. Only the syntax and menus differ. Learning one tool well makes the rest quick to learn. This course uses GitLab CI/CD because the repository, merge requests, pipelines, and artifact storage are in one product, which keeps the learning path short.

**Choosing a tool in real life:** teams rarely pick on features alone. They choose what fits where their code is hosted, what they already pay for, security rules, and the skills they have. Expect to inherit a tool, not choose one.

### 7. Automated Tests as Quality Gates

A **quality gate** is a condition a change must satisfy to move forward. Automated tests are the most common gates. The pipeline asks a yes-or-no question ("did the checks pass?") and acts on the answer without negotiation, which is what makes it trustworthy.

#### The test pyramid

Not all tests are equal. Some are fast and precise; others are slow and broad. The **test pyramid** is a guide to how many of each to have.

```
            /\
           /UI\          few, slow, broad, brittle
          /----\
         /  a11y \       targeted scans on key pages
        /--------\
       /   API    \      many, fast, stable, business logic
      /------------\
     /     Unit     \    most, fastest, cheapest, precise
    /----------------\
```

| Layer | What it checks | Speed | Typical failure message quality |
|-------|----------------|-------|---------------------------------|
| **Unit** | One function or class in isolation | Milliseconds | Points to the exact line |
| **API** | Services through their HTTP interface: status codes, bodies, schemas, auth | Fast (tens to hundreds of ms per test) | Points to an endpoint and field |
| **Accessibility** | Pages or components against accessibility rules (this week's Thursday scans) | Seconds per page | Points to an element and a rule |
| **UI end-to-end** | Complete user journeys in a browser | Slow (seconds to minutes) | Often vague: "element not found" |

The reasoning: the lower you test, the faster, cheaper, and more precise the feedback. Put most checks low in the pyramid and keep UI tests for a small number of critical journeys. A team that does the opposite (the "ice-cream cone": mostly slow UI tests) gets slow, flaky pipelines.

#### Mapping tests to gates

| Gate | Example criterion |
|------|-------------------|
| Merge request opened | Build passes; unit tests pass; API smoke tests pass; no new serious accessibility violations |
| Merge into `main` | Full API regression passes |
| Deploy to staging | Package exists; smoke tests on staging pass |
| Promote to production | Full regression on staging passes; approval (delivery) |
| After deployment | Smoke tests on production pass, otherwise roll back |

#### Shift-left

**Shift-left** means moving testing earlier on the timeline (toward the left of a diagram that runs from idea to production). The reason is cost: the later a defect is found, the more it costs to fix.

| Found at | Relative cost (rule of thumb) | Found by |
|----------|-------------------------------|----------|
| Developer's laptop | 1x | Developer |
| CI pipeline minutes after commit | About 2 to 5x | Your automated tests |
| Manual QA phase days later | About 10x | Tester |
| In production | About 50 to 100x | The customer |

These multipliers are illustrative rules of thumb, not exact figures, but the direction is well established. Shift-left is not only about running tests earlier. It includes reviewing requirements for testability, writing acceptance criteria that tests can check, and, for accessibility, catching missing labels or poor contrast before a page is ever built.

### 8. Branching Strategies and Merge Requests

How the team uses branches determines how well CI works.

| Strategy | How it works | Fit with CI |
|----------|--------------|-------------|
| **Trunk-based development** | Everyone commits to `main` (or very short-lived branches lasting hours) with small changes; unfinished features hidden behind feature flags | Best fit; the purest form of CI |
| **Feature branches (short-lived)** | A branch per task, merged within a day or two via a merge request | Very common and works well if branches stay short |
| **GitFlow** | Long-lived `develop`, release, and hotfix branches alongside `main` | Heavier; long-lived branches bring back some integration pain; used where formal release cycles exist |

For beginners and most teams the practical rule is: **keep branches small and short-lived, and merge often.**

#### The merge request (MR)

A **merge request** (GitLab's name; GitHub calls it a pull request) is a proposal to merge a branch into another, with a place for discussion and review. Combined with CI it becomes the main quality control point.

Typical flow:

1. Create a branch from the latest `main`.
2. Make a small change, commit, and push.
3. The push triggers a pipeline on the branch.
4. Open the merge request. The pipeline result is shown on it.
5. A colleague reviews the code and the tests.
6. Merging is allowed only when **required checks** pass and the needed approvals exist.
7. The merge triggers the pipeline on `main`, which may deploy.

#### Required checks (protected main)

Teams configure the repository so that `main` is **protected**: nobody can push to it directly, and a merge request cannot be merged unless the pipeline is green and (usually) at least one reviewer approves. This turns your test suite from advice into enforcement. A failing API test literally disables the merge button.

#### Real-world scenario

Priya changes the response of `GET /orders/{id}` by renaming `total` to `grandTotal`. She opens a merge request. The API contract test she wrote on Tuesday fails because the schema still expects `total`. The merge button is disabled. She either updates the contract deliberately (with the consumer teams informed) or reverts the rename. A breaking change that would have reached customers was stopped by a test and a required check.

### 9. Typical Failures and Flaky Tests

When a pipeline goes red, the first skill is **triage**: find which kind of failure it is.

| Failure type | Example | Right action |
|--------------|---------|--------------|
| **Product defect** | API returns 500 for valid input | Report to developers; fix the code |
| **Test defect** | Test expects an outdated field name | Fix the test |
| **Environment problem** | Test server down; wrong base URL | Fix configuration or environment |
| **Infrastructure problem** | Runner out of disk space; network blip while installing packages | Retry; fix the infrastructure |
| **Flaky test** | Passes and fails on the same code | Quarantine, investigate, fix root cause |

#### What is a flaky test?

A **flaky test** gives different results for the same code and the same inputs. Common causes:

- **Shared data:** tests depend on each other's records or on the order they run.
- **Timing:** fixed waits (`sleep 2`) instead of waiting for a condition; slow responses.
- **External dependencies:** a real third-party service that is sometimes slow or down.
- **Time and randomness:** tests that depend on the current date, a random value, or a timezone.
- **Unstable environment:** shared test servers modified by others.

Flakiness is poisonous. After a few unexplained red runs, the team starts clicking "retry" and then ignoring red altogether. At that moment the pipeline stops protecting anything.

**How to handle flakiness:**

1. Do not simply rerun and move on. Record it.
2. **Quarantine** the test (take it out of the blocking gate but keep it visible) so it does not block everyone.
3. Find the root cause: isolate the data, replace fixed waits with condition waits, mock unstable external services.
4. Return the test to the gate only when it is reliably stable.

Automatic retries can hide flakiness. Use them sparingly and track how often they happen.

#### Other common mistakes

- **Giant pipelines:** a 45-minute pipeline kills fast feedback. Run quick checks on every commit and slower suites on merge or nightly.
- **Tests that pass locally and fail in CI:** usually hard-coded paths, missing environment variables, or different versions of tools.
- **Ignoring red:** "it is always red, never mind."
- **Weak gates:** a green pipeline that checks little gives false confidence.
- **Secrets in the repository:** never commit passwords or tokens (a later lesson covers the right approach).

### 10. Where This Week's Work Fits

Here is how Monday to Thursday plugs into the pipeline.

| This week's work | Pipeline placement | Why there |
|------------------|--------------------|-----------|
| API smoke tests (a few critical endpoints) | Every push and merge request | Fast and valuable; catches broken endpoints quickly |
| Full API regression suite (CRUD, auth, schema, negative cases) | On merge to `main` and before deploying | Broader and slower; strong release gate |
| API contract / schema checks | Merge requests | A breaking change is caught before it merges |
| Accessibility scans on key pages | Merge requests for the affected pages, plus a wider scan on `main` or nightly | Prevents new violations; full-site scans are slower |
| Tests against a deployed staging environment | After deploy to staging | Verifies the real deployed system |
| Reports from all of the above | Saved as artifacts | Humans need to read details after the run |

A sensible policy for a beginner team might be: **block** merges on failing API smoke tests and on *new serious* accessibility violations; **report but do not block** on minor accessibility warnings, then work them down over time. Gates should be strict where the signal is reliable and lenient where it is noisy.

Remember that automated accessibility scanners find only a portion of real accessibility issues. A green scan means "no automatically detectable problems", not "fully accessible". Keep manual keyboard and screen-reader checks in your plan.

### 11. The QA Engineer's Role in CI/CD

A QA or test automation engineer in a CI/CD team does much more than "write tests that someone runs".

1. **Design the test strategy per stage:** decide which tests are fast enough for every commit and which belong in nightly runs.
2. **Write pipeline-friendly tests:** deterministic, isolated, order-independent, configurable by environment variables, producing clear reports.
3. **Define quality gates:** agree with developers and product owners what must pass to merge and to release.
4. **Maintain the test jobs in the pipeline:** configure jobs, reports, and credentials.
5. **Triage failures:** product defect, test defect, environment issue, or flake.
6. **Fight flakiness and slowness:** a slow or unreliable pipeline gets ignored.
7. **Provide visibility:** reports, trends, and metrics the team can act on.
8. **Collaborate early (shift-left):** review requirements and designs for testability, and pair with developers on unit and API tests.
9. **Keep exploratory testing alive:** automation checks what we already know; humans find what we have not thought of.

### 12. Glossary

#### Core terms

- **CI (Continuous Integration):** merging frequently into a shared branch, with an automated build and tests on each change.
- **Continuous Delivery:** always having a tested, releasable build, with a manual release step.
- **Continuous Deployment:** releasing every passing change to production automatically.
- **Pipeline:** the automated workflow from change to verified result.
- **Stage / Job:** a phase of the pipeline / one unit of work inside a stage.
- **Runner (agent):** the machine or container that runs jobs.
- **Artifact:** a file saved from a job, such as a report or a build package.
- **Gate / Quality gate:** a condition a change must meet to proceed.

#### Practices and metrics

- **Trunk-based development:** all work merges quickly into one main branch.
- **Merge request (pull request):** a reviewed proposal to merge a branch.
- **Protected branch:** a branch that cannot be changed directly and requires checks.
- **Shift-left:** testing earlier in the lifecycle.
- **Flaky test:** a test with inconsistent results on unchanged code.
- **Rollback:** restoring the previous working version.
- **DORA metrics:** deployment frequency, lead time for changes, change failure rate, mean time to restore.
- **Integration hell:** the painful merging that results from long-lived branches.

### 13. Practice Exercises

**Exercise 1: Explain it simply.** In four sentences, explain to a non-technical friend why integrating code often is better than integrating once a month.

**Solution 1 (example).** "Imagine five people writing one book separately for a month and then gluing it together: the stories contradict each other and fixing it takes ages. If they combine their work every day, any mismatch is tiny and easy to fix while everyone still remembers it. Software teams do the same with code, and a robot checks each combination automatically. The result is fewer nasty surprises and faster, calmer releases."

**Exercise 2: Classify.** For each, decide whether it is Continuous Integration, Continuous Delivery, or Continuous Deployment: (a) every merged change goes live with no human approval; (b) every merge runs tests, and a product owner clicks "Deploy" to release; (c) developers merge daily and tests run automatically, but releases are manual packaging events.

**Solution 2.** (a) Continuous Deployment. (b) Continuous Delivery. (c) Continuous Integration only, because there is no automatic always-releasable output; releases are manual.

**Exercise 3: Place your tests.** Using this week's work, assign each of the following to "every push/merge request", "merge to main", or "nightly", and justify with speed and reliability: (1) five API smoke tests, about 20 seconds; (2) 200-test API regression, about 8 minutes; (3) accessibility scan of the home and login pages, about 40 seconds; (4) accessibility crawl of the whole site, about 35 minutes.

**Solution 3.** (1) Every push/merge request: very fast, reliable, catches broken basics. (2) Merge to `main` (and before deploy): too slow for every push, but a strong release gate. (3) Merge request: quick and targeted, so new violations on key pages are blocked early. (4) Nightly: far too slow for developer feedback, but valuable for trend tracking and for catching issues on pages no one touched. Acceptable alternatives exist if justified, for example running (2) on merge requests when it can be parallelised under about 5 minutes.

**Exercise 4: Triage.** A pipeline fails twice in a row on the same commit with "Connection timed out" in an API test, then passes on a third retry. Another test fails every time with "expected `total`, got `grandTotal`". Classify each failure and say what you would do.

**Solution 4.** The timeout that passes on retry is an intermittent environment or infrastructure issue (possibly a flaky test depending on a slow service). Do not just retry and forget: record it, check whether the test server or an external dependency is unstable, add proper waits or mocks, and quarantine if it keeps recurring. The `total` versus `grandTotal` failure is consistent, so it is either a product defect (an unintended breaking rename) or an outdated test. Ask the developer whether the rename was intended; if yes, update the test and notify consumers, if no, fix the code.

### 14. Quiz

**Question 1.** Why does integrating once a month cause more pain than integrating daily?

**Question 2.** What is the single difference between Continuous Delivery and Continuous Deployment?

**Question 3.** Name the four DORA metrics and say which two measure stability.

**Question 4.** In the test pyramid, which layer should have the most tests and why?

**Question 5.** A test passes, then fails, then passes again on the same code. What is it called, and what is a good first step for the team?

**Answers**

1. Differences between branches compound: changes interact and conflict, and developers forget why changes were made. Daily integration keeps differences tiny and cheap to resolve.
2. Delivery keeps software always releasable but requires a manual approval to release to production; Deployment releases automatically with no human step.
3. Deployment frequency, lead time for changes, change failure rate, and mean time to restore. The stability metrics are change failure rate and mean time to restore.
4. The unit layer, because unit tests are the fastest, cheapest, and most precise; the higher layers are slower and more fragile, so they should be fewer.
5. A flaky test. First step: do not ignore it or just retry; record it, quarantine it if it blocks others, and investigate the root cause (shared data, timing, external dependencies).

---

## Summary

- Before CI, long-lived branches caused **integration hell**: late, painful, risky merges. CI fixes it by integrating small changes often, with an automated build and tests on every change, fast feedback, and a rule to fix a broken build first.
- **Continuous Delivery** keeps software always releasable with a manual release step; **Continuous Deployment** releases every passing change automatically. The more automation you trust, the more your tests matter.
- The four **DORA metrics** (deployment frequency, lead time, change failure rate, MTTR) measure speed and stability, and good test automation improves all of them.
- A **pipeline** is a trigger, ordered stages, parallel jobs, gates, and artifacts, described in a file in the repository. GitLab CI, GitHub Actions, Jenkins, CircleCI, and Azure DevOps share these ideas.
- Automated tests are **quality gates**. Follow the test pyramid (unit, API, accessibility, UI) and **shift left** so defects are found when they are cheapest.
- Short-lived branches and merge requests with **required checks** turn your tests into enforcement. Triage red pipelines carefully and treat flaky tests as a priority.
- This week's API tests and accessibility scans become pipeline jobs, and the QA engineer designs, maintains, and trusts those gates.
- Later Friday lessons cover the build-test-deploy lifecycle, GitLab CI/CD syntax, stages and jobs, running tests in pipelines, artifacts and reporting, and secrets.

## Additional Resources

- Atlassian, *Continuous integration vs. delivery vs. deployment*: https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment
- Martin Fowler, *Continuous Integration*: https://martinfowler.com/articles/continuousIntegration.html
- GitLab Docs, *Get started with GitLab CI/CD*: https://docs.gitlab.com/ci/
- DORA, *DORA's software delivery metrics (the four keys)*: https://dora.dev/guides/dora-metrics-four-keys/
- GitHub Docs, *Understanding GitHub Actions*: https://docs.github.com/en/actions/get-started/understand-github-actions
- Martin Fowler, *The Practical Test Pyramid*: https://martinfowler.com/articles/practical-test-pyramid.html
