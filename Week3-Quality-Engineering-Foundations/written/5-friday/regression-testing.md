# Regression Testing: Protecting What Already Works

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define regression testing and explain, in plain language, why changes to software break things that used to work.
2. List the common causes of regressions: shared code, side effects, configuration changes, dependency upgrades, data migrations, merge conflicts, and environment changes.
3. Distinguish regression testing from retesting (confirmation testing), smoke testing, and sanity testing, and state the correct order of work after a bug fix.
4. Identify the moments when regression testing should run, from a single pull request to a pre-release gate.
5. Describe the main types of regression testing: corrective, progressive, selective, complete, partial, unit-level, and release regression.
6. Build a regression suite by deciding what to include and what to leave out, and apply suite design principles (independent, deterministic, fast, maintainable, tagged).
7. Recognize the maintenance problems that make suites rot (bloat, flaky tests, obsolete tests) and explain how review cadence and ownership prevent them.
8. Select and prioritize regression tests using risk-based scoring, impact analysis, coverage-based selection, history-based selection, and requirement priority.
9. Organize tests into tiers (smoke, core regression, full regression) with realistic timing.
10. Explain where automation fits in regression, how a CI pipeline runs it, and where manual regression still belongs.
11. Calculate regression metrics such as defect leakage, pass rate, flakiness rate, and automation coverage, and use them with pass/fail thresholds for a release go/no-go decision.
12. Perform an impact analysis for a change request on Project 1 and turn it into a prioritized regression suite.
13. Use pytest markers (`smoke`, `regression`, `bugfix`) to run chosen subsets of a test suite.

---

## Why This Matters

Imagine that you hire a plumber to fix a dripping kitchen tap. The plumber replaces a washer, the drip stops, and you are delighted. The next morning you turn on the shower and no hot water comes out. The plumber's repair touched a shared pipe, and now something that worked yesterday is broken today.

Software behaves the same way. Every time a team changes a product, whether adding a feature, fixing a bug, or upgrading a library, there is a chance that something that previously worked will stop working. That kind of damage has a name: a **regression**. The activity of looking for it is called **regression testing**.

Here is why this topic deserves a full lesson:

- **Regressions are among the most common and most embarrassing defects.** Users forgive a new feature that is missing. They do not forgive a feature that worked last week and is broken this week, especially login, payment, or saving their data.
- **Every release adds risk.** In a mature product, most of the code was written before the current sprint started. If you only test the new work, you are ignoring most of the system.
- **Regression testing is where automation earns its keep.** Wednesday's lesson on manual versus automated testing pointed out that automation shines on repetitive, stable checks. Regression testing is the textbook example.
- **Regression testing is a skill of choosing, not just running.** A team that re-runs every test after every change soon runs out of time. A team that runs too little ships regressions. The craft is deciding what to run, when to run it, and what the results mean for the release decision.
- **It ties together this entire week.** Traceability (Tuesday), risk thinking and the pesticide paradox (Wednesday), test design techniques (Thursday), coverage, data-driven tests, and non-functional testing (earlier today) all feed into regression suite design. In this lesson you will use them together on Project 1.

You are not expected to build a full automation framework today. Selenium, Playwright, and CI/CD tooling come in later weeks. What you will do today is learn the thinking, which is the part that does not go out of date.

---

## The Concept

### 1. The Problem: Changes Break Working Behavior

Consider a few realistic scenarios, described generally.

- **The shared helper.** A developer improves a function that formats dates so that it supports a new language. The registration page uses that function to show the "member since" date, and so does the invoice page. The change works on the registration page, but invoices now show dates in the wrong order for some users. Nobody touched the invoice code, and nobody thought to test it.
- **The "harmless" validation tweak.** A team tightens the rules for passwords during sign-up. Existing users who created their accounts under the old rule now cannot log in, because the login screen runs the new rule against their old, shorter password.
- **The library upgrade.** A security warning forces the team to upgrade a third-party library. The upgrade passes all the new feature tests, but a date picker that depended on an older behavior stops working in one browser.
- **The bug fix that returns.** A bug is fixed in version 2.1. In version 2.3, another developer rewrites the surrounding code and accidentally reintroduces the very same bug. The users notice immediately: "This was fixed already!"
- **The configuration slip.** Someone changes a timeout setting in the staging environment to speed up a test. The setting is accidentally copied to production, and slow requests begin failing for real users.

All of these share a pattern. The change was made in one place, but the damage appeared somewhere else, and often in an area that had been working for a long time. The people who made the change usually do not predict the damage, which is exactly why they need a safety net.

**Analogy: renovating one room.** If you renovate the bathroom, you test that the new shower works. But a careful owner also checks that the lights in the hall still turn on, that the kitchen tap still has pressure, and that the walls of the neighboring bedroom have no new cracks. The renovation touched shared wiring and plumbing. Checking the rest of the house is regression testing.

### 2. Definition

A **regression** is a defect where behavior that previously worked correctly no longer works correctly, because of a change somewhere in the system or its environment.

**Regression testing** is the practice of re-running previously executed tests (or a carefully chosen subset of them) after a change, to confirm that existing functionality still works and that the change has not introduced new defects in unchanged areas.

The ISTQB glossary describes regression testing as testing of a previously tested component or system following modification, to ensure that defects have not been introduced or uncovered in unchanged areas as a result of the changes made. Notice the two key ideas in that wording:

- **Previously tested.** The tests already exist. We are reusing them.
- **Unchanged areas.** We are looking for damage where nobody expected it.

Regression testing is not a different "technique" like boundary value analysis. It is a **purpose**. You can use black-box tests, white-box tests, manual tests, or automated tests. What makes them regression tests is that you run them to detect unintended side effects of change.

### 3. Why Regressions Happen

Understanding causes helps you predict where to look. Here are the usual suspects.

| Cause | What it means | Simple example |
|---|---|---|
| **Shared code** | Many features use the same function, class, or component, so a change to it affects every user of it. | A shared "validate email" function is changed; registration, login, and "forgot password" all use it. |
| **Side effects** | A function does more than its name suggests, such as changing a global value or a database record. | A "calculate total" function also quietly rounds the stored price. |
| **Configuration changes** | Settings, feature flags, or environment variables change behavior without code changing. | A "session timeout" value is reduced from 30 minutes to 3. |
| **Dependency upgrades** | A library, framework, runtime, database driver, or operating system is updated, and its behavior shifts subtly. | A new browser version changes how a date input renders. |
| **Data migrations** | The structure or content of stored data changes, such as a new column, a renamed field, or reformatted values. | Old user records lack a new "country" field, so the profile page crashes. |
| **Merge conflicts** | Two developers change the same file; the merge resolves badly and silently drops or duplicates logic. | A bug fix from branch A is lost when branch B is merged on top. |
| **Environment changes** | A different server, database version, time zone, or network setup behaves differently from the one the tests assumed. | Code that works on the developer's laptop fails on a server in another time zone. |

Notice that **only some** of these are about the application code itself. A great deal of regression risk lives in configuration, dependencies, data, and environments, which is why regression testing is triggered by more than "the developer changed some code" (we will list the triggers soon).

### 4. Regression Testing vs. Retesting vs. Smoke vs. Sanity

These four terms are confused constantly, even by working testers. Learn the differences now and you will stand out.

- **Retesting** (also called **confirmation testing**) means re-running the *exact test that failed* after a fix, to confirm the specific defect is really gone. You covered the retest and reopen loop in Tuesday's defect lifecycle.
- **Regression testing** means running *other* tests (plus the bug-fix test itself) to make sure the fix, or any other change, did not break something else.
- **Smoke testing** is a very quick, shallow check of the most critical functions to decide whether a new build is stable enough to test at all. The name comes from hardware: switch the device on and see whether smoke comes out.
- **Sanity testing** is a narrow, focused check, usually after a small change or fix, to confirm that the specific changed area behaves reasonably before investing in deeper testing. It is often unscripted and fast.

| Aspect | Retesting (confirmation) | Regression testing | Smoke testing | Sanity testing |
|---|---|---|---|---|
| **Question it answers** | "Is this specific bug really fixed?" | "Did the change break anything that used to work?" | "Is this build stable enough to test at all?" | "Does the changed area basically make sense?" |
| **When it runs** | After a defect is marked Fixed | After any change: fixes, features, upgrades, config | At the start, on every new build or deployment | After a small fix or minor change, before deeper testing |
| **Why it runs** | Verify the fix; close or reopen the defect | Detect unintended side effects | Reject a broken build cheaply | Quick confidence on a narrow area |
| **Scope** | Only the failed test(s), same steps and data | Wide: many areas, existing tests | Wide but very shallow: critical paths only | Narrow: only the changed area |
| **Depth** | Deep on one defect | Moderate to deep | Shallow | Shallow to moderate |
| **Test cases** | The original failing test cases | Previously passed tests, selected subset or full | A small fixed list of critical checks | Few tests, often chosen on the spot |
| **Automation** | Usually manual first, may become automated | Strongly suited to automation | Strongly suited to automation (runs in CI) | Often manual or ad hoc; can be automated |
| **Typical size** | 1 to a handful of tests | Dozens to thousands of tests | 5 to 30 tests | A handful of tests |
| **Typical duration** | Minutes | Minutes to hours | Minutes | Minutes |

#### The correct order after a bug fix

When a developer marks a defect as fixed, the tester should work in this order:

1. **Smoke check the new build.** If the build will not even start, stop and report it. Do not waste time.
2. **Retest (confirm) the fix.** Run the exact steps from the original defect report. If it still fails, reopen the defect (Tuesday's lifecycle).
3. **Run sanity checks around the fixed area**, if the fix was small, to make sure the area is behaving reasonably.
4. **Run regression tests** for the areas the fix could have affected, plus the permanent bug-fix test for this defect.

Why this order? Retesting before regression is efficient. If the fix did not even work, running a large regression suite on a build that will be rejected anyway wastes hours. First prove the fix; then prove it did no harm.

**Analogy: the leaking tap.** Retesting is turning on the tap you fixed and checking that it no longer drips. Regression testing is turning on all the other taps, flushing the toilet, and running the shower to ensure the repair did not disturb the pipes. Smoke testing is checking that the water is on at the mains before you begin. Sanity testing is glancing at the fixed tap and the pipe directly under it.

### 5. When to Run Regression Testing

Run regression testing whenever something that could change behavior has changed. Here are the common triggers.

| Trigger | Why it needs regression testing |
|---|---|
| **After bug fixes** | Fixes change code and can introduce new faults ("fix one, break two"). |
| **After new features** | New code often shares components with old code. |
| **After refactoring** | Refactoring changes structure without intending to change behavior, so regression tests are precisely the proof that behavior stayed the same. |
| **After configuration or environment changes** | Settings, servers, certificates, and infrastructure alter behavior without code changes. |
| **After dependency, library, OS, or browser updates** | External software changes underneath your product. |
| **Before a release** | Final confirmation that the whole product is releasable. |
| **Nightly** | A larger suite runs overnight on the latest combined code, when nobody is waiting. |
| **On every commit or pull request (in CI)** | A small, fast subset gives developers feedback within minutes, before problems spread. |

A useful mental model: the more **expensive** the check, the less often it runs. Cheap checks run on every change; expensive checks run nightly or before release. We will formalize this as **test suite tiers** shortly.

### 6. Types of Regression Testing

Different books use slightly different names, so treat the following as a working vocabulary. The exact labels matter less than understanding the idea behind each.

**Corrective regression testing.** Used when the software has *not* changed in terms of requirements, so the existing test cases can be reused as they are. You simply run them again, perhaps after a small fix.
*Example:* The team fixes a spelling error in an error message on Project 1's login page. The login test cases remain valid, so you re-run them unchanged.

**Progressive regression testing.** Used when requirements or functionality *have* changed, so you must write new or updated test cases along with re-running the old ones that remain valid.
*Example:* The password rule changes from 8 to 12 characters. The test "password of 8 characters is accepted" is now wrong; you update it, add new tests for 12 characters and the special-character rule, and re-run the rest.

**Selective regression testing.** You choose a **subset** of the existing tests, based on what was changed and what could be affected (impact analysis).
*Example:* A fix touches only the email template code. You run tests for registration emails, password reset emails, and anything else that sends email, and skip the profile page tests.

**Complete (full) regression testing.** You run the **entire** regression suite. This is slow and expensive but gives the highest confidence.
*Example:* Before the major 3.0 release, the team runs all 1,200 regression tests across every supported browser.

**Partial regression testing.** You test the changed area plus the areas **directly connected** to it, with a smaller set than selective regression often implies; it is the "change plus its neighbors" check. Some teams use "partial" and "selective" almost interchangeably; the point is that you are not running everything.
*Example:* After changing the registration form, you run registration tests plus login (since a new account must be able to log in).

**Unit-level regression testing.** You re-run the **unit tests** of one component or module in isolation after changing it. It is the cheapest and fastest level, and it runs constantly on developers' machines.
*Example:* After editing the `validate_password` function, the developer re-runs all unit tests for the `validators` module in two seconds.

**Release regression ("release regression").** A broad regression cycle run when a release candidate is prepared, usually combining the full suite, key non-functional checks, and some manual exploratory testing, before the go/no-go decision.
*Example:* On the Thursday before a Friday release, the team executes the full automated suite, a manual pass for areas that cannot be automated, and a final smoke test on the production-like staging environment.

You can think of these types as answers to two questions: *Did the requirements change?* (corrective vs. progressive) and *How much do we run?* (unit-level, partial, selective, complete, release).

### 7. Building a Regression Test Suite

A **regression test suite** is a maintained collection of tests designed to be re-run repeatedly to detect regressions. The suite is a living asset, not a dumping ground.

#### What to include

1. **Critical business flows.** Anything that makes or loses money, or that the product exists to do. For Project 1: registration, login, and password reset.
2. **High-risk and historically defect-prone areas.** Defect clustering (Wednesday) says defects concentrate in a few modules. Include extra tests there.
3. **Recently changed areas.** Code that changed recently is statistically more likely to contain defects.
4. **Integration points.** Places where components, services, databases, or third-party systems meet, such as the email service or a payment gateway.
5. **Tests for previously fixed bugs ("bug-fix tests").** Every serious defect that is fixed should leave behind a test that guards it **forever**. If someone reintroduces the bug, that test fails immediately. These are the cheapest insurance in testing.
6. **Core smoke checks.** A tiny set of "is the product alive?" tests that form the first tier of the suite.

#### What to exclude (or remove)

- **Tests for features that no longer exist.** They are dead weight.
- **Duplicates.** Two tests that check the same thing in the same way.
- **Low-value, low-risk checks** that have never found a defect and cover cosmetic or rarely used areas (these may live in a lower tier rather than being deleted).
- **Unstable tests** that fail randomly, until they are fixed (see "flaky tests" below).
- **Tests that cannot run unattended** if you plan to automate them, such as tests requiring a person to read a code from a physical device.
- **One-off exploratory checks** that were useful once but are not repeatable.

#### Suite design principles

Whether manual or automated, good regression tests share these qualities.

| Principle | Meaning | Why it matters |
|---|---|---|
| **Independent** | Each test sets up what it needs and does not rely on another test running first. | Tests can run in any order or in parallel; one failure does not cause a chain of false failures. |
| **Deterministic** | The same test on the same code gives the same result every time. | Random passes and failures destroy trust. |
| **Fast** | Each test finishes quickly; slow checks live in later tiers. | Fast suites get run often; slow ones get skipped. |
| **Maintainable** | Clear names, no copy-pasted steps, test data kept tidy, one reason to fail. | Cheap to update when the product changes. |
| **Tagged and prioritized** | Each test carries labels (for example `smoke`, `regression`, `bugfix`, `high`) so you can select subsets. | Enables selective regression, the heart of this lesson. |
| **Traceable** | Each test links to a requirement or a defect ID. | You can answer "what does this test protect?" and perform impact analysis. |

### 8. The Maintenance Problem

A regression suite is like a garden. If you only plant and never prune, it becomes a jungle. Four problems appear again and again.

**Suite bloat.** Every new feature adds tests, but nobody removes any. The suite grows from 200 tests to 2,000. Run time grows from 10 minutes to 6 hours, people stop running it, and regressions escape.

**Flaky tests.** A **flaky test** is a test that sometimes passes and sometimes fails on the *same* code, with no change in between. Causes include timing problems (waiting too briefly for a page to load), shared test data, dependence on test order, and unstable external services. Flaky tests are poisonous because people learn to ignore red results ("oh, that one fails sometimes"), and eventually they ignore a *real* failure.

**Obsolete tests.** The product changed, but the tests still describe the old behavior. They either fail for the wrong reason, or worse, pass while checking nothing useful. This is the **pesticide paradox** from Wednesday: running the same tests repeatedly stops finding new defects, because the product has moved on and the tests have not. A regression suite that never evolves slowly stops protecting you.

**No owner.** When "everybody" owns the suite, nobody does. Failures sit unexamined, and flaky tests are left alone.

**The cure is routine, not heroics:**

| Practice | What it looks like |
|---|---|
| **Review cadence** | Once per sprint (or at least once per release), review which tests failed often, never failed, duplicated each other, or no longer match requirements. Remove, fix, or move them. |
| **Ownership** | Each area of the suite has a named owner (a person or a small team) responsible for fixing failures, removing flakiness, and updating tests when requirements change. |
| **Add-with-delete discipline** | When a new test is added, ask whether an older test is now redundant. |
| **Flaky policy** | A flaky test is quarantined (moved out of the blocking suite), logged as a defect in the test code, and fixed within an agreed time or deleted. |
| **Tie to change** | When a requirement changes (progressive regression), updating its tests is part of the work, not an afterthought. |

### 9. Regression Test Selection and Prioritization

You rarely have time to run everything on every change. **Test selection** decides *which* tests to run. **Test prioritization** decides *in what order*, so the most valuable tests run first and failures appear early. Several techniques exist, and good teams combine them.

#### 9.1 Risk-based selection

Recall from earlier weeks that **risk** is the combination of how likely something is to go wrong and how bad it would be if it did. A simple scoring method:

- **Likelihood (L):** How likely is a failure here? Scale 1 (unlikely) to 5 (very likely).
- **Impact (I):** How bad would a failure be (money, safety, reputation, legal, user harm)? Scale 1 (trivial) to 5 (severe).
- **Risk score = L x I** (range 1 to 25).

Typical bands: **20 to 25 critical**, **12 to 19 high**, **6 to 11 medium**, **1 to 5 low**.

A likelihood-by-impact matrix looks like this (cell values are the scores):

| | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|---|---|---|---|---|---|
| **Likelihood 5** | 5 | 10 | 15 | 20 | 25 |
| **Likelihood 4** | 4 | 8 | 12 | 16 | 20 |
| **Likelihood 3** | 3 | 6 | 9 | 12 | 15 |
| **Likelihood 2** | 2 | 4 | 6 | 8 | 10 |
| **Likelihood 1** | 1 | 2 | 3 | 4 | 5 |

**Worked scoring example (Project 1, after a change to password validation code).**

| Area | Likelihood of regression (why) | L | Impact if broken (why) | I | Score | Band |
|---|---|---|---|---|---|---|
| Registration | Changed code is used directly | 5 | New users cannot join | 5 | 25 | Critical |
| Login | Shares the validation function | 4 | Nobody can use the product | 5 | 20 | Critical |
| Password reset | Shares the validation function | 4 | Locked-out users cannot recover | 4 | 16 | High |
| Change password | Shares the validation function | 4 | Users cannot update credentials | 3 | 12 | High |
| Profile display | Not connected to the change | 1 | Cosmetic issues only | 2 | 2 | Low |

Decision: run all critical and high tests now, run medium tests in the nightly suite, and leave low tests to the weekly full run. Notice how a *numeric* score turns an argument ("I feel login is important") into something a team can discuss and agree.

#### 9.2 Impact analysis (what did the change touch?)

**Impact analysis** asks: *Given what changed, which parts of the system could be affected?* It is the most practical selection technique because it starts from the facts of the change. Tools and artifacts that help:

- **The change description.** A change request, user story, or defect report states the intent.
- **Pull request and diff.** A **diff** is the list of lines added and removed; a **pull request (PR)** is a request to merge a developer's changes, which shows exactly which files changed. Ask the developer which modules those files belong to.
- **Change logs and release notes.** Summaries of what changed between versions. For third-party upgrades, the library's own release notes list behavior changes.
- **Traceability matrix (from Tuesday).** It maps requirements to test cases. If requirement R-12 changed, the matrix tells you which tests protect R-12, and by extension related requirements.
- **Dependency mapping.** A simple diagram or table showing "feature A uses component X; component X is used by features B and C". If X changed, A, B, and C are all in scope.
- **Developer conversation.** The cheapest tool of all. Ask: "What else uses this?" The answer is often very revealing.

A good habit: always analyze impact in **three rings**. Ring 1 is the **changed item** itself. Ring 2 is whatever **directly uses or is used by** it. Ring 3 is **indirect or business-critical flows** that pass through it, even if the connection is remote. Tests from Ring 1 and Ring 2 almost always run; Ring 3 is chosen by risk.

#### 9.3 Coverage-based selection

Earlier today you learned **code coverage**: the percentage of statements, branches, or paths that tests execute. Coverage can guide selection in two ways:

- **Map tests to code.** If you know which tests execute which functions (a coverage report can show this), then when a function changes you select exactly the tests that touch it.
- **Choose tests that add coverage.** If two tests execute the same lines and branches, running both adds little; prefer the one that covers more of the changed code.

Caution: coverage tells you code was *executed*, not that behavior was *verified*. A test with no assertions can reach 100% coverage while checking nothing. Use coverage to guide selection, not to prove quality.

#### 9.4 History-based selection

The past predicts the future. Use records to prioritize:

- **Defect-prone modules.** Modules with many past defects (defect clustering) deserve more regression tests and earlier execution.
- **Failure history of tests.** Tests that have failed recently, or frequently, are likely to detect something again. Run them first.
- **Tests that have never failed in a long time** may be candidates for a lower tier (but not automatic deletion, since a protective test that never fails is doing its job).
- **Recent change frequency.** Files changed many times recently tend to be riskier.

#### 9.5 Requirement-priority-based selection

If the team already ranks requirements (for example MoSCoW: Must have, Should have, Could have, Won't have this time), use it. Tests tied to **Must have** requirements go in the first tiers; tests tied to **Could have** features can wait. This works well with traceability: every test already links to a requirement, so the priority comes along for free.

#### 9.6 Test impact analysis tools (name level)

Some tools automate part of this reasoning. **Test impact analysis** tools examine a code change and use coverage data to select only the tests that exercise the changed code. Some build systems and CI platforms offer this, and some products (for example, those in the Microsoft Azure DevOps and Launchable families) provide such features. You do not need to learn them now. What is important is the principle: *change in, relevant tests out.* Also remember the caution: such tools are only as good as the data they are given, and they can miss indirect effects such as configuration or data changes.

#### 9.7 "Retest all" vs. selective regression

| Dimension | Retest all (run everything) | Selective (run chosen subset) |
|---|---|---|
| **Confidence** | Highest, in principle | Good if selection is sound; blind spots if not |
| **Time and cost** | High and grows with the suite | Lower, scales better |
| **Feedback speed** | Slow | Fast |
| **Risk of missed regression** | Lowest | Higher; depends on analysis quality |
| **Effort to decide** | None | Needs impact analysis and maintained tags/traceability |
| **Best used** | Before major releases, after big refactors or platform upgrades, nightly or weekend | On commits, small fixes, minor features, mid-sprint changes |
| **Danger** | Gets skipped because it is slow | Gets trusted too much, with outdated impact analysis |

The practical answer is **both**: selective regression for fast feedback during the day, and a full run on a schedule as a safety net.

### 10. Test Suite Tiers

Instead of a single giant suite, organize tests into **tiers** by cost and purpose. This lets you run the right amount at the right time.

| Tier | Purpose | Typical contents | Typical duration | When it runs |
|---|---|---|---|---|
| **Tier 1: Smoke** | Is the build alive and are the vital functions working? | 5 to 30 checks: app starts, user can register, user can log in, main page loads | Under 5 to 10 minutes | Every commit or PR; every deployment |
| **Tier 2: Core / sanity regression** | Do the important and risky flows still work? | Critical flows, bug-fix tests, high-risk areas, integrations | About 30 to 60 minutes | Per merge to main, per build, after a change in a related area |
| **Tier 3: Full regression** | Does everything still work? | All regression tests, wider data and browser combinations, deeper negative cases | Several hours | Nightly, weekend, and before release |

A **tag** such as `smoke`, `core`, or `full` on each test makes running a tier as simple as one command (you will see this in the pytest demo). Tiers also tell you what to do with a failing result: a Tier 1 failure means "stop everything, the build is broken"; a Tier 3 failure on a low-risk edge case might be triaged calmly the next morning.

### 11. The Role of Automation in Regression

Regression testing is the single best candidate for automation, for a very simple reason: you run the same checks again and again. A manual tester running 300 tests by hand might take two full days per release. A machine can do the same in 20 minutes, at 3 a.m., every night, without getting bored or skipping step 7.

#### What to automate

Automate tests that are:

- **Stable.** The feature is not changing weekly; otherwise you will spend all your time repairing scripts.
- **Repetitive.** The test will run many times.
- **High-value.** It protects something important.
- **Deterministic.** It has a clear expected result a machine can verify.
- **Data-heavy.** Many input combinations (data-driven tests you studied today) are tedious by hand and easy for machines.

#### The test pyramid applied to regression

Wednesday's **test pyramid** says to have many fast, cheap unit tests at the base, fewer integration (service/API) tests in the middle, and few slow end-to-end UI tests at the top. The same shape applies to regression suites:

```
            /\
           /UI\          few, slow, expensive; protect critical user journeys
          /----\
         / API  \        moderate number; fast; check business rules and integrations
        /--------\
       /   Unit   \      many, very fast; run on every change by developers
      /------------\
```

A suite shaped like an upside-down pyramid (mostly UI tests) is slow, flaky, and costly to maintain. Push checks *down* to the lowest level that can reliably detect the problem. For example, "password shorter than 12 characters is rejected" can be checked as a unit test of the validation function in milliseconds; you do not need to open a browser for every length variation.

#### Where regression runs in a CI pipeline

**Continuous Integration (CI)** means that every time a developer submits a change, an automated system builds the software and runs tests. The tool details come in later weeks; for now, understand the flow. Here is a typical pipeline, from the developer's keyboard to production:

```
 Developer
    |  commit / open pull request
    v
+------------+   +-------------+   +------------------+   +---------------------+
|   BUILD    |-->| UNIT TESTS  |-->|   SMOKE TESTS    |-->| API / INTEGRATION   |
| compile &  |   | (seconds to |   | (Tier 1, under   |   | REGRESSION (Tier 2) |
| package    |   |  minutes)   |   |  10 minutes)     |   | (about 30 minutes)  |
+------------+   +-------------+   +------------------+   +---------------------+
      | fail           | fail             | fail                    | fail
      v                v                  v                         v
   STOP, notify author: fix before merging (fast feedback)          |
                                                                    v
                                              +--------------------------------+
                                              |  MERGE to main + deploy to     |
                                              |  TEST / STAGING environment    |
                                              +---------------+----------------+
                                                              v
                                              +--------------------------------+
                                              |  NIGHTLY FULL REGRESSION       |
                                              |  (Tier 3: UI, browsers, data;  |
                                              |   parallel, several hours)     |
                                              +---------------+----------------+
                                                              v
                                              +--------------------------------+
                                              |  QUALITY GATE: thresholds met? |
                                              |  yes -> release candidate      |
                                              |  no  -> stop, investigate      |
                                              +---------------+----------------+
                                                              v
                                              +--------------------------------+
                                              |  PRODUCTION: canary rollout,   |
                                              |  post-release smoke + monitor  |
                                              +--------------------------------+
```

Reading the diagram: the cheapest, fastest checks come first, so most broken changes are rejected within minutes. Expensive checks run later and less often. This ordering is called **shift-left** thinking: find problems as early (as far left) as possible, because the cost of fixing grows over time.

#### Running automation on every commit

Running a small, fast subset on every commit or pull request catches a regression within minutes of its creation, when the developer still remembers what they changed and the change is small enough to find quickly. A regression discovered three weeks later, among 200 other changes, can take days to trace.

#### Flaky tests and quarantine

When a test is flaky, do not simply re-run until it goes green. Follow a policy:

1. **Detect.** Track tests whose results change without code changes (many tools can report this).
2. **Quarantine.** Move the test out of the blocking suite (a tag such as `quarantine`) so it no longer stops releases or trains people to ignore red builds, but continue running it in a non-blocking job so you still collect data.
3. **Diagnose and fix.** Typical fixes: replace fixed "sleep" waits with waiting for a condition, isolate test data, remove order dependence, and stub unreliable external services.
4. **Return or delete.** After the fix, restore it to the main suite. If nobody will fix it within an agreed period, delete it. A test you do not trust gives no protection.

#### Parallel execution (name level)

Instead of running 1,000 tests one after another, split them across several machines or processes and run them simultaneously. If the suite takes 120 minutes serially, running on 6 parallel workers could bring it to roughly 20 to 25 minutes (not exactly 20, because setup overhead and uneven test lengths add time). Parallel execution requires **independent** tests, which is one more reason for that design principle. Tools exist for this (pytest has a plugin named `pytest-xdist`, and test platforms such as Selenium Grid offer parallel browsers), but you only need the idea today.

#### Where manual regression still fits

Automation does not replace people entirely. Manual regression still has a place when:

- **The feature is new or changing rapidly.** Scripts would be rewritten constantly.
- **The check requires human judgment**, such as "does this layout look right and feel usable?"
- **The test runs rarely** (once a year), so automation never pays back.
- **Exploratory testing** (earlier today) is needed to look beyond scripted checks. Automated regression only finds what you told it to look for; exploratory sessions hunt for the surprises.
- **Physical or external factors** are involved: a real phone, a hardware device, a third-party service that cannot be simulated.

A healthy balance: automate the stable core, and reserve human time for exploration and judgment.

### 12. Regression in Agile Sprints

Agile teams change the product every two weeks or less, so regression risk never sleeps. Several concepts matter.

**Regression debt.** Like technical debt, regression debt builds up when a team adds features without adding or maintaining regression tests. The cost is paid later, with interest: slow manual regression, escaped defects, and fear of changing anything.

**Hardening sprint.** Some teams dedicate a sprint (or part of one) near a release to stabilization: running full regression, fixing escaped defects, and polishing. A hardening sprint is often a symptom of regression debt. Mature teams try to avoid it by testing continuously.

**Continuous regression.** Instead of one big regression phase at the end, the suite runs automatically all the time: on each commit, nightly, and on each release candidate. New tests are added in the same sprint as the feature.

**Definition of Done includes regression.** Recall Scrum's **Definition of Done (DoD)** from Monday: the team's shared checklist for when work counts as complete. A strong DoD includes items such as "regression tests for the story are written or updated", "the relevant regression tier passes", and "bug-fix tests exist for any defect fixed". If a story passes its own acceptance criteria but breaks login, it is not Done.

**Practical sprint rhythm:**

- *Sprint planning:* Estimate regression work (new tests and updates) as part of each story.
- *During the sprint:* Run smoke and core regression on each merge; run full regression nightly.
- *Sprint review/end:* Check that all tiers are green and the suite is up to date.
- *Retrospective:* Ask whether any regression slipped through and why.

### 13. Regression in DevOps and Continuous Delivery

**DevOps** joins development and operations to deliver software quickly and reliably. **Continuous Delivery (CD)** means the software is always kept in a releasable state and can be released at any moment through an automated pipeline. In such pipelines regression testing becomes the evidence that "releasable" is true.

**Quality gates.** A **quality gate** is an automated checkpoint that a change must pass to move on. Examples: "all smoke tests pass", "at least 95 percent of core regression passes with zero critical failures", "no new critical security warnings", "code coverage on changed lines at least 80 percent". If the gate fails, the pipeline stops. Gates turn quality rules into automatic decisions rather than opinions at 5 p.m. on release day.

**Canary releases (name level).** A **canary release** deploys the new version to a small percentage of real users first (say 5 percent) while the old version serves everybody else. The team monitors errors and performance. If all is well, the rollout widens; if not, it rolls back. The name is borrowed from canaries once used in mines to warn of danger. A canary is a form of regression detection in production, a last safety net, and it complements rather than replaces pre-release regression testing.

Related ideas include **feature flags** (switching a new feature on for some users only) and **monitoring/alerting** (noticing errors in production quickly). Together they shrink the damage of any regression that escapes.

### 14. Visual Regression and API Regression (Name Level)

Two specialized flavors deserve a mention. You will not build them today.

**Visual regression testing.** A tool takes a screenshot of a page, compares it to an approved "baseline" screenshot, and flags pixel differences. It catches layout shifts, overlapping text, missing images, and wrong colors that functional tests miss, because a functional test may report "button exists" even when it is hidden behind a banner. Tools in this area include Percy, Applitools, and the screenshot comparison features in Playwright. The challenge: small harmless differences (fonts, animations, dynamic content) cause false alarms, so teams must tune the comparison and review differences by hand.

**API regression testing.** Most systems expose **APIs** (Application Programming Interfaces), which are the doors through which one program talks to another. API regression tests send requests (for example, "register a user") and verify the responses (status codes, data returned, error messages). They are faster and more stable than UI tests, so they form the middle of the pyramid. A key idea here is **contract testing**: making sure an API still honors the format it promised to other systems, so a change to field names does not break the mobile app. Tools such as Postman and REST Assured are commonly used; you will meet API testing properly in later weeks.

### 15. Measuring Regression Effectiveness

What gets measured gets improved, but only if you measure the right things and understand what they mean. Here are the core metrics, with formulas.

| Metric | Formula | What it tells you |
|---|---|---|
| **Defect leakage (escape rate)** | (Defects found in production / (Defects found before release + Defects found in production)) x 100 | How many defects slipped past testing. Lower is better. |
| **Defects found by regression** | Number of defects first detected by regression runs, optionally as a share of all pre-release defects | Whether regression is doing its job of finding side effects. |
| **Regression pass rate** | (Tests passed / Tests executed) x 100 | Current health of the product (and suite). |
| **Execution time** | Wall-clock time of each tier | Whether feedback is fast enough. |
| **Flakiness rate** | (Number of flaky tests / Total tests in suite) x 100, or (flaky failures / total runs) x 100 | Trustworthiness of the suite. |
| **Automation coverage** | (Automated regression tests / Total regression tests) x 100 | How much of regression is machine-run. |

#### Worked numeric example

Release 4.2 of a sample product has these results.

- Defects found before release (all testing activities): 45
- Of those, found by regression tests: 9
- Defects found in production within 30 days: 5
- Regression suite size: 500 tests
- Tests executed in the final regression run: 500
- Tests passed: 480 (20 failed)
- Automated tests: 380
- Flaky tests identified (over several runs): 12
- Full suite run time: 38 minutes (after parallelization)

Calculations:

- **Defect leakage** = 5 / (45 + 5) x 100 = 5 / 50 x 100 = **10 percent**.
- **Defects found by regression** = 9 of 45 = 9 / 45 x 100 = **20 percent** of pre-release defects.
- **Regression pass rate** = 480 / 500 x 100 = **96 percent**.
- **Flakiness rate** = 12 / 500 x 100 = **2.4 percent**.
- **Automation coverage** = 380 / 500 x 100 = **76 percent**.
- **Execution time** = **38 minutes** for the full suite.

How to read them *together*: A pass rate of 96 percent sounds good, but 20 failed tests might contain a critical failure, so pass rate alone must not decide a release. A leakage of 10 percent says one in ten defects reached users, so the team should study those 5 production defects: which tests would have caught them? Each answer becomes a new bug-fix test. A flakiness rate of 2.4 percent is above the common target of under 1 to 2 percent, so quarantine work is due. Notice also what these numbers cannot tell you: a high pass rate on a weak suite is a false comfort. That is why leakage (an outcome measure) must accompany pass rate (an activity measure).

**Caution about metrics.** Metrics are signals, not goals. If you reward people for pass rate, they may delete failing tests. If you reward execution time only, they may drop valuable slow tests. Always interpret numbers with context.

### 16. Reporting Regression Results

A regression report must let a busy reader make a decision in one minute. Here is a sample template.

```
REGRESSION TEST REPORT
------------------------------------------------------------
Project / Release : Project 1 - QE Foundations, Build 1.4.0-rc2
Change summary    : Password policy changed to 12 chars + special char
Environment       : Staging (Chrome 126, Firefox 127), DB v15
Run date / Tier   : 2026-10-08, Tier 2 core + bug-fix tests
Executed by       : CI pipeline run #212 / Tester: <name>

RESULTS
  Planned : 60     Executed : 60     Not run : 0
  Passed  : 57     Failed   : 3      Blocked : 0
  Pass rate: 95.0 percent     Duration: 24 min

FAILURES
  ID          Test                                   Severity  Defect
  TC-REG-014  Login with legacy 8-char password     High      BUG-231 (new)
  TC-REG-022  Reset email shows old rule text        Medium    BUG-232 (new)
  TC-REG-031  Change password rejects 11 chars       Low       Known issue BUG-198

FLAKY / QUARANTINED : TC-REG-040 (timeout, 2 of 5 runs), ticket TST-77
COVERAGE OF CHANGE  : Requirements R-12, R-13 covered; R-14 not run (reason)
RISKS / NOTES       : Legacy-user login behavior needs product decision
RECOMMENDATION      : NO-GO until BUG-231 is fixed and retested
------------------------------------------------------------
```

Good reports share these habits: state **what was run and why**, report failures with severity and defect links, mention **what was not run** (silence about gaps is misleading), track flaky tests honestly, and end with a clear recommendation tied to agreed criteria.

### 17. Decision Criteria: Pass/Fail Thresholds and Go/No-Go

A release decision should follow criteria agreed **before** the test run, not feelings after it. Typical criteria:

| Criterion | Example threshold |
|---|---|
| Smoke tests | 100 percent pass |
| Critical (Priority 1) regression tests | 100 percent pass |
| High (Priority 2) regression tests | At least 98 percent pass; no open High/Critical defects |
| Overall regression pass rate | At least 95 percent |
| Open defects | Zero Critical, zero High; Medium only with documented acceptance |
| Flaky tests in blocking suite | Zero (quarantined tests documented) |
| Bug-fix tests | 100 percent pass |
| Environment | Release candidate tested in a production-like environment |

A single failing critical test can mean **No-Go** even when the overall pass rate looks excellent. The decision belongs to the accountable stakeholders (for example product owner and QA lead), but the data and thresholds come from you.

#### Sample release checklist

- [ ] Release candidate build is identified and frozen (no more changes).
- [ ] Smoke tests pass (100 percent) on the release candidate.
- [ ] Retests for all defects fixed in this release are complete and recorded.
- [ ] Bug-fix tests for those defects exist in the regression suite.
- [ ] Core regression passes against thresholds; failures triaged and linked to defects.
- [ ] Full regression run completed within the last 24 hours on this build.
- [ ] No open Critical or High defects; any Medium defects have documented acceptance.
- [ ] Flaky tests identified, quarantined, and documented.
- [ ] Non-functional checks (performance baseline, security basics) reviewed.
- [ ] Configuration and data migration steps verified on a production-like environment.
- [ ] Exploratory session on changed areas completed.
- [ ] Regression report published; traceability matrix updated.
- [ ] Rollback plan and monitoring in place.
- [ ] Go/No-Go decision recorded with names and date.

---

## Examples

### Working Example 1: Project 1 Password Policy Change

**The change request (CR-07):** "The password policy changes from a minimum of 8 characters to a minimum of 12 characters, and passwords must now contain at least one special character."

Your job: decide what to regression test.

#### Step 1: Impact analysis

Ask: where does the password rule appear or interact? Using the three rings from earlier:

| # | Affected feature | How it is affected | Ring | Risk reasoning |
|---|---|---|---|---|
| 1 | **User Registration** | Primary change: new rule enforced on sign-up; form hints and error messages change | 1 (changed) | Business critical: new users cannot join if broken, or weak passwords slip in |
| 2 | **Password reset** | A user choosing a new password must obey the new rule; the reset page may have its own copy of the rule | 2 (shares logic) | Locked-out users depend on it |
| 3 | **Change password** (logged-in) | Same rule applies to the new password field; old password must still be accepted as "current" | 2 (shares logic) | Moderate; users can still log in, but changing credentials breaks |
| 4 | **Login** | Existing users have old 8-character passwords. Login must NOT reject them by applying the new length rule; error messages for bad credentials must not change meaning | 2 (shares validation / messaging) | Critical: if login breaks, everything breaks |
| 5 | **Login messaging** | Error text may refer to the old rule ("at least 8 characters") | 2 | Medium: wrong guidance confuses users |
| 6 | **Email templates** | Registration confirmation and reset emails may state password requirements | 3 (indirect) | Low to medium: text mismatch only |
| 7 | **API validation** | The server must enforce the same rule as the UI; otherwise API calls bypass it | 2 (integration) | High: security rule enforced in one place only is not enforced |
| 8 | **Existing data / migration** | Existing accounts keep old passwords unless a forced-reset policy is added | 3 (data) | Needs a product decision; tests for legacy users |
| 9 | Profile page, logout | Not connected | none | Low; leave to full regression |

#### Step 2: Select regression tests with justification

| Selected test | Justification |
|---|---|
| Register with valid 12+ char password containing a special character | Progressive: confirms the new happy path works |
| Register with 11-character password (with special) is rejected | Boundary just below the new minimum (boundary value analysis from Thursday) |
| Register with exactly 12 characters accepted | Boundary at the minimum |
| Register with 12+ characters, no special character, rejected | New rule, negative case |
| Old tests "8-character password accepted" | **Obsolete:** update or retire these (progressive regression) |
| Login with an existing account created under the old 8-character rule | Guards against rejecting legacy users: the most dangerous regression here |
| Login with wrong password shows the standard error | Unchanged behavior; messaging must not leak or change meaning |
| Reset password with new valid password; with too short; with no special char | Shares the rule; new behavior expected |
| Change password: valid, invalid, and current-password-wrong | Shares the rule |
| API: POST to registration with short password returns a validation error | UI/API consistency check |
| Email content check: registration email and reset email show updated requirement text | Indirect effect |
| Bug-fix tests: duplicate email with different case (BUG-101); any past password defects | These stay forever |
| Smoke: register then login with a valid new user | Core flow after any build |

Not selected now (left for nightly full regression): profile editing, logout, help pages.

#### Step 3: The resulting regression suite

| ID | Test | Priority | Tier | Automation status |
|---|---|---|---|---|
| REG-01 | Register new user, valid 12+ char password with special char | P1 | Smoke | Automated |
| REG-02 | Login with newly registered user | P1 | Smoke | Automated |
| REG-03 | Login with legacy account (8-char password) succeeds | P1 | Core | Automated |
| REG-04 | Register with 11 chars rejected, message shown | P1 | Core | Automated |
| REG-05 | Register with exactly 12 chars accepted | P1 | Core | Automated |
| REG-06 | Register with no special char rejected | P1 | Core | Automated |
| REG-07 | Registration API rejects short password | P1 | Core | Automated (API level) |
| REG-08 | Password reset accepts valid new password | P2 | Core | Automated |
| REG-09 | Password reset rejects non-compliant password | P2 | Core | Automated |
| REG-10 | Change password: valid and invalid cases (data-driven) | P2 | Core | Automated |
| REG-11 | Login wrong password shows standard error | P2 | Core | Automated |
| REG-12 | BUG-101: email with capitals and spaces normalized, no duplicate | P2 | Core (bug-fix) | Automated |
| REG-13 | Login error messages show updated wording | P3 | Full | Manual for now |
| REG-14 | Registration and reset email text shows new rule | P3 | Full | Manual (email check) |
| REG-15 | Registration form hint text matches the rule, across browsers | P3 | Full | Manual, visual regression later |
| REG-16 | Exploratory session: password edge cases (unicode, spaces, very long) | P3 | Full | Manual, 45 min |
| REG-17 | Profile edit and logout still work | P4 | Full | Automated |

Reading the table: P1 tests (critical) are in the smoke and core tiers and are automated first. The manual items are checks of wording and appearance, or exploration, where human judgment is valuable.

### Working Example 2: E-commerce Discount Change

**The change:** An online shop changes its discount rule. Previously, the code "SAVE10" gave 10 percent off the whole order. Now, discounts apply only to items that are not already on sale, and the discount is applied before tax rather than after.

**Impact analysis**

| Area | Why it is affected |
|---|---|
| Cart total calculation | Direct: changed discount logic |
| Tax calculation | Direct: the order of operations changed |
| Order confirmation page and email | Shows totals and discount lines |
| Invoices and receipts | Totals must match what the customer saw |
| Refunds and returns | A refund of a discounted item must return the correct amount |
| Reports (revenue) | Finance reports aggregate totals |
| Other promotions (free shipping over 50, buy-one-get-one) | May interact with the new discount rule (promotion stacking) |
| Payment gateway | Amount sent for charging must match the total |
| Inventory | Not affected |
| Product browsing | Not affected |

**Risk scoring**

| Area | L | I | Score | Decision |
|---|---|---|---|---|
| Cart total and tax | 5 | 5 | 25 | Run now, P1 |
| Payment amount sent to gateway | 3 | 5 | 15 | Run now, P1 |
| Refund amount for discounted item | 4 | 4 | 16 | Run now, P1 |
| Promotion stacking | 4 | 4 | 16 | Run now, P1 |
| Invoice/receipt totals | 3 | 4 | 12 | Run now, P2 |
| Confirmation email totals | 3 | 3 | 9 | Nightly |
| Revenue report | 2 | 4 | 8 | Nightly |
| Product browsing | 1 | 2 | 2 | Weekly full |

**Selected tests (examples):**

- Cart with one full-price item and SAVE10: 10 percent off, tax applied after discount.
- Cart with a sale item plus a full-price item: discount applies only to the full-price item.
- Cart containing only sale items: SAVE10 rejected or no discount, with clear message.
- Boundary: order exactly at a free-shipping threshold, before and after discount (does the discounted total drop below it?).
- Refund of an item bought with SAVE10 returns the discounted price, not the list price.
- Payment request amount equals the displayed total to the cent (rounding check).
- Bug-fix test: previously fixed defect where a 100 percent discount code produced a negative total.

**What this example teaches:** The most dangerous regressions were not in the "discount" screen. They were in refunds, payments, and promotion stacking: places that consume the changed result. Impact analysis follows the data **downstream**, asking "who uses the number this code produces?"

### Hands-On Demonstration: A Tagged Suite with pytest

**pytest** is the most popular testing tool for Python. A pytest **marker** is a label you attach to a test function. Markers let you run subsets by label. You are not expected to master Python here; focus on the idea of tags and selection. This demonstration was run for this lesson; the output below is genuine.

#### Files

**pytest.ini** (configuration; registers the marker names so typos are caught and `pytest --markers` documents them)

```ini
[pytest]
markers =
    smoke: fastest critical checks, run on every commit
    regression: broader checks that guard existing behavior
    bugfix: tests that guard a previously fixed defect
```

**validators.py** (a tiny stand-in for Project 1's validation code)

```python
SPECIALS = "!@#$%^&*"

def is_valid_password(password, min_length=12):
    if len(password) < min_length:
        return False
    return any(ch in SPECIALS for ch in password)

def normalize_email(email):
    return email.strip().lower()
```

**test_registration.py** (the suite)

```python
import pytest
from validators import is_valid_password, normalize_email

@pytest.mark.smoke
@pytest.mark.regression
def test_strong_password_is_accepted():
    assert is_valid_password("Abcdefgh1234!") is True

@pytest.mark.regression
def test_short_password_is_rejected():
    assert is_valid_password("Ab1!") is False

@pytest.mark.regression
def test_password_without_special_char_is_rejected():
    assert is_valid_password("Abcdefgh12345") is False

@pytest.mark.regression
def test_exactly_12_characters_is_accepted():
    assert is_valid_password("Abcdefghij1!") is True

@pytest.mark.regression
@pytest.mark.bugfix
def test_bug_101_email_with_uppercase_and_spaces_is_normalized():
    # BUG-101: " User@Example.COM " created a duplicate account
    assert normalize_email("  User@Example.COM ") == "user@example.com"

@pytest.mark.smoke
def test_normalize_email_basic():
    assert normalize_email("a@b.com") == "a@b.com"
```

#### Line-by-line explanation

**pytest.ini**

- `[pytest]` starts the pytest configuration section.
- `markers =` begins the list of allowed marker names.
- Each indented line has the form `name: description`. Registering a marker means a misspelling such as `@pytest.mark.smok` is flagged (it can be made an error with `--strict-markers`) instead of silently creating a tag that matches nothing. The descriptions appear in `pytest --markers`.

**validators.py**

- `SPECIALS = "!@#$%^&*"` defines the characters that count as special.
- `def is_valid_password(password, min_length=12):` defines the rule; the default minimum is now 12 (the changed requirement).
- `if len(password) < min_length: return False` rejects passwords that are too short.
- `return any(ch in SPECIALS for ch in password)` returns True only if at least one character is special (`any` checks whether at least one item matches).
- `normalize_email` removes surrounding spaces (`strip`) and converts to lowercase (`lower`), the fix for BUG-101.

**test_registration.py**

- `import pytest` makes the markers available; the next line imports the functions to be tested.
- `@pytest.mark.smoke` is a **decorator**: a line placed above a function that attaches something to it. Here it attaches the `smoke` label.
- A test can carry **several** labels, as the first test does (smoke and regression).
- `def test_...` pytest automatically treats functions whose names start with `test_` as tests.
- `assert ... is True` is the check. If the statement is false the test fails.
- Test 4 sits exactly at the boundary (12 characters). Test with 11 characters comes later.
- The bug-fix test has an explicit bug ID in its name and in a comment. A name like `test_bug_101_...` means that anyone who sees it fail knows the history. That is the "stays forever" bug-fix test.

#### Running subsets

Everything (the full suite):

```
$ python3 -m pytest -v
collected 6 items

test_registration.py::test_strong_password_is_accepted PASSED            [ 16%]
test_registration.py::test_short_password_is_rejected PASSED             [ 33%]
test_registration.py::test_password_without_special_char_is_rejected PASSED [ 50%]
test_registration.py::test_exactly_12_characters_is_accepted PASSED      [ 66%]
test_registration.py::test_bug_101_email_with_uppercase_and_spaces_is_normalized PASSED [ 83%]
test_registration.py::test_normalize_email_basic PASSED                  [100%]

============================== 6 passed in 0.02s ===============================
```

Only the smoke tier (`-m smoke`; the `-m` option means "select by marker expression"):

```
$ python3 -m pytest -m smoke -v
collected 6 items / 4 deselected / 2 selected

test_registration.py::test_strong_password_is_accepted PASSED            [ 50%]
test_registration.py::test_normalize_email_basic PASSED                  [100%]

======================= 2 passed, 4 deselected in 0.02s ========================
```

Only bug-fix tests:

```
$ python3 -m pytest -m bugfix -v
collected 6 items / 5 deselected / 1 selected

test_registration.py::test_bug_101_email_with_uppercase_and_spaces_is_normalized PASSED [100%]

======================= 1 passed, 5 deselected in 0.01s ========================
```

Regression tests that are *not* bug-fix tests (marker expressions combine with `and`, `or`, `not`):

```
$ python3 -m pytest -m "regression and not bugfix" -v
collected 6 items / 2 deselected / 4 selected

test_registration.py::test_strong_password_is_accepted PASSED            [ 25%]
test_registration.py::test_short_password_is_rejected PASSED             [ 50%]
test_registration.py::test_password_without_special_char_is_rejected PASSED [ 75%]
test_registration.py::test_exactly_12_characters_is_accepted PASSED      [100%]

======================= 4 passed, 2 deselected in 0.03s ========================
```

**How to read this output**

- `collected 6 items / 4 deselected / 2 selected`: pytest found 6 tests, set aside 4 that do not match your marker, and will run 2. "Deselected" tests are skipped, not failed.
- `PASSED`: the assertion held. `[ 50%]` is progress through the selected tests.
- The last line summarizes the count and the time. Selecting by marker is exactly how a pipeline runs "Tier 1 on every commit" and "everything nightly".
- The registered markers are listed by `pytest --markers`:

```
@pytest.mark.smoke: fastest critical checks, run on every commit
@pytest.mark.regression: broader checks that guard existing behavior
@pytest.mark.bugfix: tests that guard a previously fixed defect
```

#### A regression caught, and a gap exposed

Now suppose a developer accidentally changes the default `min_length=12` back to `8` (a configuration-style slip). Run the regression subset:

```
$ python3 -m pytest -m regression -q
.....                                                                    [100%]
5 passed, 1 deselected in 0.01s
```

All green, yet the product is wrong! Why? None of the tests checks a password with a length from 8 to 11 that contains a special character. Our "short" test uses a 4-character password, which is rejected under *both* rules. This is the **pesticide paradox** and a coverage gap in action: the suite protected what it was told to protect. We close the gap by adding a boundary test (11 characters), which Thursday's boundary value analysis would have suggested:

```python
@pytest.mark.regression
def test_11_characters_is_rejected():
    assert is_valid_password("Abcdefghi1!") is False
```

With the broken default still in place, the suite now fails:

```
$ python3 -m pytest -m regression -q
.....F                                                                   [100%]
=================================== FAILURES ===================================
________________________ test_11_characters_is_rejected ________________________

    @pytest.mark.regression
    def test_11_characters_is_rejected():
>       assert is_valid_password("Abcdefghi1!") is False
E       AssertionError: assert True is False
E        +  where True = is_valid_password('Abcdefghi1!')

test_registration.py:33: AssertionError
=========================== short test summary info ============================
FAILED test_registration.py::test_11_characters_is_rejected - AssertionError:...
1 failed, 5 passed, 1 deselected in 0.03s
```

Reading it: `F` marks the failing test; the `>` arrow points at the failed line; `E` lines explain: the function returned True where False was expected, so an 11-character password is wrongly accepted. After restoring `min_length=12`, the run is green again:

```
......                                                                   [100%]
6 passed, 1 deselected in 0.01s
```

The lesson: a regression suite is only as good as its boundary cases. This new test is also now a permanent guard for the 12-character rule.

---

## AI-Assisted Regression Test Selection

AI tools can help with regression work, and you will see more of them each year. Realistic uses today:

- **Suggesting impact:** Given a pull request diff or change description, an AI assistant can propose which features might be affected and draft a first impact analysis table. This is a useful starting point for review.
- **Predictive test selection:** Some tools learn from historical data (which code changes caused which test failures) and rank tests by their likelihood of failing for a given change, so the likeliest failures run first.
- **Drafting test cases:** AI can draft regression test cases from requirements or defect reports, including bug-fix tests.
- **Clustering and triage:** AI can group similar failures, spot likely flaky tests from result history, and summarize large reports.
- **Maintenance help:** AI can suggest updates to scripts after a UI change.

**Cautions you must keep in mind:**

1. **AI does not know your system's hidden coupling.** Configuration, data, and environment effects are easy for it to miss. Treat its list as a prompt for your thinking, not as the answer.
2. **Confident does not mean correct.** AI can invent features, miss rings 2 and 3, or recommend skipping the one test that matters. A human reviewer must approve the selection.
3. **Data quality limits predictive tools.** With poor or thin history, predictions are poor.
4. **Never skip tiers solely on AI advice.** Keep the scheduled full run as the safety net, and compare the AI's skipped tests with your risk scores.
5. **Protect confidential information.** Do not paste proprietary code or customer data into tools your organization has not approved.
6. **Accountability stays with you.** If a regression escapes, "the AI said it was fine" is not an answer a team can accept.

A sound workflow: let AI draft, let your analysis (and the traceability matrix) verify, and record the final selection and reasons in the test plan.

---

## Common Mistakes

| Mistake | Why it hurts | Better approach |
|---|---|---|
| **Running everything, always** | Slow feedback; the suite is skipped or ignored; costs balloon | Use tiers and selective regression; run full regression on a schedule |
| **Never pruning the suite** | Bloat, obsolete tests, long runtimes, pesticide paradox | Review every sprint or release; delete, merge, and update |
| **Ignoring flaky tests** | People stop believing red results, and real failures hide | Quarantine, diagnose, fix, or delete |
| **No ownership** | Failures sit unexamined; nobody updates tests when requirements change | Name an owner for each area and the suite as a whole |
| **Retesting only the fix** | Misses side effects, the very definition of regression | Retest, then regress |
| **Skipping the bug-fix test** | The same bug returns later | Every important fix adds a permanent test |
| **Automating everything immediately** | Scripts for unstable features rot quickly | Automate stable, high-value tests first |
| **Judging by pass rate alone** | One critical failure matters more than 95 percent passing | Use thresholds on priority, plus leakage |
| **Forgetting non-code changes** | Config, data, dependency, and environment changes cause regressions too | Treat them as regression triggers |
| **Selection without evidence** | "Gut feel" misses indirect effects | Use impact analysis, traceability, and risk scores |
| **Testing only through the UI** | Slow, fragile suite | Follow the pyramid; push checks down to unit and API |

---

## Practice Exercises

Try each exercise yourself before reading the answer key.

### Exercise 1: Impact analysis for three changes

For each change, list at least five affected areas of Project 1 (User Registration and Login) and say which ring each belongs to.

- **Change A:** The email validation rule is updated to also reject disposable-email domains.
- **Change B:** The login page adds a "Remember me" checkbox that keeps users logged in for 30 days.
- **Change C:** The web framework used by the sample app is upgraded to a new major version.

**Answer key (sample answers; yours may differ if justified)**

*Change A: disposable-email domains rejected*

| Area | Ring | Reason |
|---|---|---|
| Registration email field validation | 1 | Directly changed |
| Password reset (email entry) | 2 | Often uses the same email validator; legitimate users with such addresses may be blocked |
| Login (email as username) | 2 | If the validator is reused, existing users with disposable addresses might be locked out |
| Change email / profile email update | 2 | Same validator |
| API registration endpoint | 2 | Must enforce the same rule |
| Existing accounts with now-disallowed domains | 3 | Data/migration question |
| Email normalization and bug-fix test BUG-101 | 2 | Shares normalization code |
| Confirmation email sending | 3 | Rejected addresses must not trigger emails |

*Change B: Remember me*

| Area | Ring | Reason |
|---|---|---|
| Login with checkbox ticked and unticked | 1 | Direct |
| Session creation and timeout | 2 | The 30-day session changes expiry logic |
| Logout | 2 | Must clear the persistent session |
| Password change/reset | 2 | Should invalidate persistent sessions |
| Security: cookie flags, shared computer risk | 3 | Non-functional/security regression |
| Registration followed by automatic login | 2 | Shares session code |
| Browser compatibility for cookies | 3 | Environment variation |

*Change C: framework major-version upgrade*

Nearly everything is potentially affected, so this is a **complete (full) regression** case: all registration and login tests, form rendering, validation messages, session handling, API endpoints, email sending, performance baseline, and browser compatibility. Ring labels matter less because the dependency touches every feature (a ring 1 change everywhere). The key insight is that dependency upgrades are risk multipliers; do not attempt a small selective suite here.

### Exercise 2: Prioritize a 15-test list using risk scores

Score each test as L x I, rank them, and assign tiers (Smoke, Core, Full). Context: the change is the password policy update from Example 1.

| ID | Test | L | I |
|---|---|---|---|
| T1 | Register with valid password | | |
| T2 | Login with existing legacy user | | |
| T3 | Reset password with valid new password | | |
| T4 | Profile photo upload | | |
| T5 | Registration rejects 11-char password | | |
| T6 | Change password with wrong current password | | |
| T7 | Footer links open correct pages | | |
| T8 | Login shows error for wrong password | | |
| T9 | Registration API rejects no-special-char password | | |
| T10 | Email template text shows new rule | | |
| T11 | Dark mode toggle | | |
| T12 | Duplicate email registration blocked (BUG-101) | | |
| T13 | Logout clears session | | |
| T14 | Registration form hint text | | |
| T15 | Help page search | | |

**Answer key (one defensible scoring)**

| ID | Test | L | I | Score | Tier |
|---|---|---|---|---|---|
| T1 | Register with valid password | 5 | 5 | 25 | Smoke |
| T2 | Login with existing legacy user | 4 | 5 | 20 | Smoke |
| T5 | Registration rejects 11-char password | 5 | 4 | 20 | Core |
| T9 | Registration API rejects no-special-char password | 4 | 5 | 20 | Core |
| T3 | Reset password with valid new password | 4 | 4 | 16 | Core |
| T12 | Duplicate email registration blocked (BUG-101) | 3 | 5 | 15 | Core (bug-fix) |
| T8 | Login shows error for wrong password | 3 | 4 | 12 | Core |
| T6 | Change password with wrong current password | 3 | 4 | 12 | Core |
| T10 | Email template text shows new rule | 4 | 2 | 8 | Full |
| T14 | Registration form hint text | 4 | 2 | 8 | Full |
| T13 | Logout clears session | 2 | 4 | 8 | Full |
| T4 | Profile photo upload | 1 | 3 | 3 | Full |
| T7 | Footer links open correct pages | 1 | 2 | 2 | Full |
| T15 | Help page search | 1 | 2 | 2 | Full |
| T11 | Dark mode toggle | 1 | 1 | 1 | Full |

Notes: Ties (such as 20 and 20 and 20) are broken by judgment, here "business flow first". The smoke tier gets only the two tests proving the product is alive for new and existing users. If your scores differ by a point or two, that is fine; what matters is that your **reasoning** about likelihood (is this connected to the change?) and impact (what is lost if it breaks?) is explicit.

### Exercise 3: Tier a suite and estimate timing

A suite has 400 automated tests. Test durations: 25 smoke-eligible tests average 12 seconds each; 120 core tests average 20 seconds each; the other 255 average 45 seconds each. Tests run one at a time.

1. Compute the time for each tier.
2. Which tiers fit the targets (smoke under 10 minutes, core under 60 minutes)?
3. If full regression runs on 5 parallel workers, estimate the time.

**Answer key**

1. Smoke: 25 x 12 s = 300 s = **5 minutes**. Core: 120 x 20 s = 2,400 s = **40 minutes**. The remaining 255 x 45 s = 11,475 s, which is about **191 minutes (3 hours 11 minutes)**. Full regression (if it includes all tiers) = 300 + 2,400 + 11,475 = 14,175 s = **about 236 minutes (about 3 hours 56 minutes)**.
2. Smoke (5 minutes) is under 10 minutes: fits. Core (40 minutes) is under 60 minutes: fits. If Core is defined to include Smoke, 45 minutes total, still fits.
3. Ideal parallel time is 236 / 5 = about **47 minutes**. In practice, add overhead and uneven distribution, so expect roughly **55 to 65 minutes**. This shows why parallel execution depends on independent tests.

### Exercise 4: Compute defect leakage and other metrics

Release A: 72 defects found before release, 8 found in production. Release B: 90 defects found before release, 5 found in production.

1. Compute the leakage for each release and compare.
2. Release B's regression run: 600 tests executed, 570 passed, 18 flaky tests identified, 450 automated tests in the suite of 600. Compute pass rate, flakiness rate, and automation coverage.
3. A manager says "Release B had a 95 percent pass rate, so we are great." Respond.

**Answer key**

1. Release A: 8 / (72 + 8) = 8 / 80 = **10.0 percent**. Release B: 5 / (90 + 5) = 5 / 95 = **5.26 percent (about 5.3 percent)**. Release B's leakage is about half of A's, a clear improvement. A caution: different releases differ in size and complexity, so compare trends over several releases.
2. Pass rate = 570 / 600 = **95.0 percent**. Flakiness = 18 / 600 = **3.0 percent** (above a 1 to 2 percent target). Automation coverage = 450 / 600 = **75 percent**.
3. Pass rate is an activity metric. The better question is *which* 30 tests failed (any Critical?), whether the 3 percent flakiness hides real failures, and what the leakage was (5.3 percent: good, but 5 defects still escaped). Look at each escaped defect and add a bug-fix test for it. Pass rate alone does not demonstrate release readiness.

---

## Knowledge Check

1. **Define a regression in one sentence.**
   *Answer:* A defect in which behavior that previously worked no longer works correctly because of a change in the system or its environment.

2. **A developer fixes BUG-55 and you re-run exactly the original failing steps. What is this called?**
   *Answer:* Retesting (confirmation testing).

3. **After the retest passes, you run login, registration, and reset tests to see whether the fix broke anything. What is this called?**
   *Answer:* Regression testing.

4. **What is the right order after a bug fix is delivered?**
   *Answer:* Smoke check the build, retest the fix, sanity check the area if needed, then run regression (including the bug-fix test).

5. **Name four causes of regressions that have nothing to do with the feature code a developer was editing.**
   *Answer:* Any four of: configuration changes, dependency or library upgrades, data migrations, environment changes, merge conflicts, browser/OS updates.

6. **What is the difference between corrective and progressive regression testing?**
   *Answer:* Corrective reuses existing tests unchanged because requirements did not change. Progressive is needed when requirements changed, so tests must be added or updated along with re-running the unchanged ones.

7. **Why should every important bug fix leave behind a test?**
   *Answer:* To guard permanently against the same defect being reintroduced; it is cheap insurance and its name documents the history.

8. **A test passes on Monday, fails on Tuesday, and passes on Wednesday with no code change. What is it and what should you do?**
   *Answer:* A flaky test. Quarantine it, diagnose (timing, shared data, order dependence, external services), fix it or delete it.

9. **A change has likelihood 4 and impact 5. What is the risk score and band?**
   *Answer:* 20, Critical.

10. **State the three rings of impact analysis.**
    *Answer:* Ring 1: the changed item; Ring 2: things that directly use or are used by it; Ring 3: indirect or business-critical flows that pass through it.

11. **Why is "retest all" not always the best choice?**
    *Answer:* It is slow and costly, so feedback is delayed and the suite may be skipped; selective regression gives faster feedback when impact analysis is sound. The best practice combines selective runs with a scheduled full run.

12. **What belongs in the smoke tier, and how long should it take?**
    *Answer:* A small set of the most critical checks (app starts, register, login), typically under 5 to 10 minutes.

13. **How does the test pyramid shape regression automation?**
    *Answer:* Many fast unit tests, a moderate number of API tests, and a few UI tests; push checks to the lowest reliable level.

14. **Compute defect leakage: 36 defects found before release, 4 in production.**
    *Answer:* 4 / (36 + 4) = 4 / 40 = 10 percent.

15. **A suite has a 98 percent pass rate, but one failing test covers payment. Go or no-go?**
    *Answer:* Probably No-Go, since critical-priority tests must pass at 100 percent under typical thresholds; one failing payment test outweighs the overall percentage.

16. **What is a quality gate?**
    *Answer:* An automated checkpoint in the pipeline with pass/fail criteria that a change must meet to proceed.

17. **Why can a green regression suite still be misleading?**
    *Answer:* The suite only checks what it was written to check. Obsolete tests, missing boundary cases, or weak assertions (pesticide paradox, coverage gaps) can leave regressions undetected. Leakage data and periodic review reveal this.

18. **When does manual regression still make sense?**
    *Answer:* For new or rapidly changing features, judgment-based checks (look and feel), rarely run tests, exploratory sessions, and checks involving physical devices or unsimulatable external systems.

---

## Try It: Project 1 Regression Plan

This activity completes the regression and risk part of your Project 1 test-design document.

**Scenario:** Product management raises change request **CR-09**: "After 5 failed login attempts, the account is locked for 15 minutes. The login page should show a message explaining this. A locked user may unlock the account early by using Password Reset."

**Your tasks**

1. **Impact analysis (30 minutes).** Create a table of at least 8 affected areas of Project 1. For each, record the area, how it is affected, the ring (1, 2, or 3), and a one-line reason. Think about registration (does a new user start with zero failed attempts?), login, password reset, error messaging, email templates (lock notification?), API behavior, session handling, and stored data (a new "failed attempts" field for existing users).
2. **Risk scoring (20 minutes).** Give each area a likelihood and impact (1 to 5), compute the score, and assign a band.
3. **Select regression tests (30 minutes).** List at least 12 tests (existing tests you would re-run, updated tests, and new tests). Mark each as retest, regression, or progressive/new. Include **at least one bug-fix test** (for example, a past defect from your Tuesday Jira practice) and at least one test on **boundaries** (4 vs 5 failed attempts; 14:59 vs 15:00 minutes).
4. **Tier and automate (20 minutes).** Build a suite table like Example 1 with columns ID, test, priority, tier, automation status. Put no more than 5 tests in smoke. State which you would automate first and why.
5. **Exit criteria (15 minutes).** Write pass/fail thresholds for go/no-go on CR-09.
6. **Optional pytest extension.** In a new folder (not in your submission folder), write a tiny `is_locked(failed_attempts)` function and three tests tagged `smoke`, `regression`, and `bugfix`. Run each subset with `-m` and paste your output.

**Deliverable:** Add the impact table, risk scores, suite table, and exit criteria to your Project 1 test-design document under the heading "Regression and Risk Plan".

**Self-check questions:** Did you include the unchanged but nearby feature (password reset)? Did you check that existing users with no failed-attempts data still log in? Did you give a reason for every excluded area? Can a reader tell which tests run on every commit and which run nightly?

---

## Key Takeaways

- A **regression** is something that used to work and no longer does, caused by a change. **Regression testing** re-runs existing tests to catch such damage.
- Regressions come from shared code, side effects, configuration, dependency upgrades, data migrations, merge conflicts, and environment changes, not just edited code.
- **Retesting** confirms a specific fix; **regression** checks everything else; **smoke** checks that a build is alive; **sanity** is a quick focused check. After a fix: smoke, retest, sanity, then regression.
- Run regression after fixes, features, refactoring, config and dependency changes, before release, nightly, and on commits or pull requests.
- Build the suite from critical flows, high-risk and defect-prone areas, recent changes, integrations, bug-fix tests, and smoke checks. Keep tests independent, deterministic, fast, maintainable, tagged, and traceable.
- Suites rot through bloat, flakiness, and obsolescence (the pesticide paradox). Review regularly and give the suite owners.
- Select tests using risk (L x I), impact analysis (three rings, traceability, diffs), coverage, history, and requirement priority. Combine selective and scheduled full runs.
- Organize tiers: smoke (minutes), core (about an hour), full (nightly, weekend, pre-release).
- Automate stable, repetitive, high-value checks following the test pyramid; quarantine flaky tests; parallelize; keep manual and exploratory testing for judgment.
- Agile and DevOps need continuous regression, regression in the Definition of Done, and quality gates; canary releases are a final safety net.
- Measure leakage, pass rate, flakiness, automation coverage, execution time, and defects found by regression; read them together, and decide go/no-go on thresholds agreed in advance.
- Use AI as an assistant for drafting and ranking; people verify and own the decision.

---

## Additional Resources

- **ISTQB Glossary** (regression testing, confirmation testing, smoke test definitions): https://glossary.istqb.org
- **Atlassian: Regression testing** (a practical overview of types, strategy, and automation): https://www.atlassian.com/continuous-delivery/software-testing/regression-testing
- **pytest documentation: Working with custom markers** (registering and selecting by marker): https://docs.pytest.org/en/stable/how-to/mark.html
