# Manual vs. Automated Testing

**Week 3 - Quality Engineering Foundations | Wednesday: Testing Fundamentals**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define manual testing and automated testing in your own words, and name the strengths and weaknesses of each.
2. Compare manual and automated testing across ten dimensions (speed, cost over time, accuracy, reusability, and more).
3. Apply a decision checklist to decide whether a given test should be automated or kept manual.
4. Calculate a simple, illustrative break-even point (return on investment, or ROI) for an automation effort.
5. Describe the test automation pyramid and explain why too many user-interface (UI) tests is an anti-pattern.
6. Explain what test automation is NOT, and correct common myths about it.
7. Name the main types of test automation and the common tools in each area (names only; the tools themselves are covered in later weeks).
8. Describe the test automation lifecycle and where automation fits into a CI/CD pipeline.
9. Describe, realistically, how AI helps and where it falls short in testing.
10. Read a manual login test case and its automated equivalent in Python, and explain each line.
11. Propose which login and registration checks in Project 1 to automate first, and justify the choice.

---

## Why This Matters

Earlier this week you learned the quality mindset, the difference between QA and QC, and the difference between verification and validation. On Monday and Tuesday you learned how software is built and how testing is planned and executed. Today we look at a question every test team faces on every project:

> **Who (or what) should run this test: a person, or a program?**

The answer shapes your project's schedule, budget, and quality. If a team tests everything by hand, releases become slow and exhausting. If a team tries to automate everything, it spends months building scripts that break constantly, and it still misses problems that only a human eye would catch. Good quality engineers know how to choose.

This lesson is also your first conceptual meeting with **test automation**. You will not install any tools today. Hands-on automation arrives in later weeks. Today's goal is to build the judgment that makes those later weeks make sense: what automation is, what it is good for, what it is bad at, and how to decide.

For your career, this matters even more. Job postings for "Test Automation Engineer," "SDET," and "Quality Engineer" all assume you can reason about this trade-off. Interviewers love the question "What would you automate, and what would you leave manual?" By the end of today, you will have a confident, structured answer.

---

## The Concept

### 1. A simple analogy: dishes by hand vs. the dishwasher

Imagine you run a restaurant kitchen.

- **Washing dishes by hand** is flexible. You can handle a delicate wine glass, a burnt pot, or a one-off oddly shaped item. You notice if a plate is chipped. But it is slow, tiring, and the quality varies depending on how tired you are. Washing 500 plates a night by hand is painful.
- **A dishwasher** handles 500 plates identically every night, runs while you sleep, and never gets bored. But buying one costs money, it needs maintenance, it cannot wash a fragile antique, and it will happily wash a dirty plate badly if you load it wrong. Also, it will never notice that a plate is chipped.

Testing works the same way. Manual testing is the flexible human. Automated testing is the tireless machine. A smart kitchen uses both: the dishwasher for the daily volume, and human hands for the special items.

Keep this analogy in mind. We will return to it.

---

### 2. What is manual testing?

**Manual testing** is testing in which a human tester executes test cases by hand, without using automation scripts. The tester reads the steps, interacts with the application (clicking, typing, tapping), observes what happens, and compares what actually happened (the **actual result**) with what should have happened (the **expected result**).

Recall from Tuesday that a **test case** is a documented set of steps, input data, and expected results used to check one specific behavior. In manual testing, a person follows that document.

**A typical manual testing session looks like this:**

1. Open the application in a browser.
2. Follow the steps of a test case, one at a time.
3. Observe the result.
4. Record pass or fail (and log a defect in Jira if it fails, as you learned yesterday).
5. Move to the next test case.

**Skills a good manual tester needs:**

- **Curiosity and observation:** noticing small oddities such as a misaligned button or a confusing message.
- **Domain knowledge:** understanding how real users and the business work.
- **Clear communication:** writing precise defect reports.
- **Critical thinking:** asking "what if?" and trying unexpected things.
- **Attention to detail and patience.**

Notice that none of these require programming. That is one reason manual testing is a common entry point into the field.

#### Strengths of manual testing

| Strength | What it means | Example |
|---|---|---|
| **Exploratory testing** | Learning, designing, and executing tests at the same time, following your curiosity rather than a script. | A tester notices an odd delay after clicking "Register" and starts probing: what if I click twice? What if I go back? |
| **Usability testing** | Judging whether the product is easy and pleasant to use. | "This form is confusing; I could not find the Submit button." |
| **Ad-hoc testing** | Informal, unplanned testing without documentation, often based on experience and intuition. | Quickly trying random inputs on a new screen to see if anything breaks. |
| **Visual checking** | Spotting visual problems like overlapping text, wrong colors, or broken layout. | A logo that appears squashed on a phone screen. |
| **Human judgment** | Deciding whether something "feels right," is appropriate, or makes sense to a real person. | An error message that is technically correct but rude or unclear. |
| **Low startup cost** | You can begin testing immediately; no scripts to build. | Testing a brand-new feature the day it is delivered. |

#### Weaknesses of manual testing

| Weakness | Why it hurts |
|---|---|
| **Slow** | A human clicks and types at human speed. A suite of 500 test cases may take days. |
| **Repetitive** | Running the same 200 checks every release is boring work. |
| **Error-prone** | Bored or tired people skip steps, mistype data, or overlook a failure. This is **human error**. |
| **Hard to scale** | To test twice as much, you need roughly twice as many people or twice as much time. |
| **Not repeatable at speed** | You cannot easily re-run everything every hour, or at 3 a.m., or on 10 browsers at once. |
| **Costs grow over time** | Each run costs the same human effort again, forever. |

---

### 3. What is automated testing?

**Automated testing** (also called **test automation**) is the practice of using software to execute tests, automatically compare the actual results with the expected results, and report the outcome, with little or no human involvement during the run.

In plain terms: instead of a person following the steps, a program follows the steps.

#### The building blocks of automation

Let us define the vocabulary you will hear constantly. Do not worry about memorizing tool details; just learn what each word means.

| Term | Definition | Dishwasher-style analogy |
|---|---|---|
| **Test script** | A piece of code that performs the steps of a test case and checks the result. | The programmed wash cycle. |
| **Test data** | The inputs the tests use (usernames, passwords, product IDs, and so on). | The dishes you load in. |
| **Assertion** | A statement in the script that says "this must be true." If it is false, the test fails. Example: assert that the welcome message equals "Welcome, alice". | The sensor that checks "are the dishes clean?" |
| **Test framework** | A set of libraries, rules, and structure that helps you organize and write tests consistently (for example, how to name tests, set up data, and share code). | The dishwasher's overall design. |
| **Test runner** | The program that finds your tests, executes them, and collects pass/fail results. | The button that starts the cycle. |
| **Test report** | The output summarizing which tests passed, failed, or were skipped, often with screenshots and logs. | The display saying "cycle complete; 2 problems". |
| **Expected result** | What the system should do according to the requirement. | The definition of "clean." |
| **Actual result** | What the system really did during the run. | What actually came out. |

**The core loop of every automated test is:**

```
  Arrange        Act            Assert
  (set up data)  (do the thing) (check the result)
       |             |               |
   username =    call login()    result must equal
   "alice"                       "Welcome, alice"
```

This **Arrange - Act - Assert** pattern is a popular way to think about any automated test. We will use it in the Python example below.

#### Strengths of automated testing

| Strength | What it means |
|---|---|
| **Speed** | A machine can run hundreds of checks in minutes. |
| **Repeatability** | The same script does exactly the same thing every time. No skipped steps. |
| **Coverage** | Because runs are cheap, you can run many more tests, on many more data sets and browsers. |
| **CI/CD integration** | Automated tests can run automatically whenever a developer saves new code (explained later in this lesson). |
| **Off-hours execution** | Tests can run overnight or on weekends without anyone present. |
| **Fast feedback** | Developers learn within minutes that a change broke something. |
| **Reduced human error** | Machines do not get bored or distracted. |

#### Weaknesses of automated testing

| Weakness | What it means |
|---|---|
| **Upfront cost** | Writing scripts and building a framework takes time, skill, and money before any benefit appears. |
| **Maintenance** | When the application changes, scripts must be updated. Scripts that are not maintained become useless. |
| **Flaky tests** | A **flaky test** is a test that sometimes passes and sometimes fails even though nothing in the product changed (often because of timing, slow networks, or unstable test data). Flaky tests destroy trust. |
| **Cannot judge usability** | A script can check that a button exists; it cannot tell you the button is confusing or ugly. |
| **Only checks what you told it to check** | Scripts do not notice the unexpected problem you did not write an assertion for. |
| **False sense of security** | "All 800 tests passed" feels great, but if those tests are shallow or wrong, serious defects can still be hiding. |
| **Needs technical skill** | Someone must be able to code, debug, and design tests. |

> **Key idea:** A passing automated test only tells you that the thing it checks still works. It does not tell you the product is good.

---

### 4. Detailed comparison: manual vs. automated

| Dimension | Manual testing | Automated testing |
|---|---|---|
| **Speed of execution** | Slow; limited by human speed. | Fast; limited by computer speed. |
| **Cost over time** | Low startup cost, but cost repeats on every run and grows with the number of runs. | High startup cost, but each additional run costs very little. |
| **Accuracy / human error** | Prone to oversight, fatigue, and typos on repetitive work. | Highly consistent; does exactly what the script says (including exactly the wrong thing if the script is wrong). |
| **Reusability** | Test cases are reusable as documents, but each execution needs fresh human effort. | Scripts are reused again and again at almost no extra effort. |
| **Exploratory ability** | Excellent; humans adapt, improvise, and notice the unexpected. | Very limited; follows only pre-written steps. |
| **Initial investment** | Low: a tester, a test case document, and the application. | High: tools, framework, skilled engineers, test environments, and time to build. |
| **Skills required** | Domain knowledge, observation, communication, test design. | All of the above plus programming, debugging, and framework design. |
| **Best fit** | New features, usability, exploratory, one-time, and rapidly changing areas. | Stable, repetitive, high-volume, data-heavy, and cross-browser checks. |
| **Feedback speed** | Slow; results arrive hours or days after a change. | Fast; results can arrive in minutes after a change. |
| **Maintenance** | Light: update the test case document when a requirement changes. | Heavy and continuous: update scripts whenever the application changes. |

Read this table carefully. Notice that neither column "wins" in every row. That is the entire point: the two approaches complement each other.

---

### 5. When to automate and when to keep manual: a decision checklist

Not every test deserves automation. A good quality engineer asks structured questions before deciding. Use this checklist.

#### Signs a test is a good candidate for automation

| Criterion | Question to ask | Why it points to automation |
|---|---|---|
| **Repetitive** | Will this test be run many times? | The more runs, the more the upfront cost is repaid. |
| **Stable** | Is the feature mature and unlikely to change soon? | Stable features mean less script maintenance. |
| **High risk / business critical** | Would a failure here be very costly (money, safety, reputation)? | You want these checked on every change, quickly and reliably. |
| **Data-heavy** | Does the test need many combinations of input data? | Machines are tireless at running the same steps with many inputs (data-driven testing is covered Friday). |
| **Cross-browser / cross-device** | Must this run on several browsers, operating systems, or devices? | Running the same script across many environments is easy for machines and exhausting for humans. |
| **Regression** | Does it re-check that existing features still work after a change? | Regression suites are the classic automation target (regression testing is covered in depth Friday). |
| **Smoke** | Is it a quick "is the build basically alive?" check? | Smoke tests run after every build; automating them gives instant feedback. |
| **Performance / load** | Does it need hundreds or thousands of simulated users? | Humans cannot generate that load at all (performance testing is covered Friday). |

#### Signs a test should stay manual (at least for now)

| Criterion | Question to ask | Why it points to manual |
|---|---|---|
| **One-time** | Will this test be run only once or twice? | The scripting cost will never be repaid. |
| **Rapidly changing UI** | Is the screen being redesigned every sprint? | Scripts would break constantly. |
| **Usability** | Are we judging ease of use or look and feel? | Needs human perception and opinion. |
| **Exploratory** | Are we investigating and learning, not confirming? | Needs human creativity. |
| **New feature** | Is the feature brand-new and not yet understood or stable? | Test it by hand first; automate once it settles. |
| **Hard to automate** | Does it involve physical devices, CAPTCHAs, or complex human interaction? | The technical cost may outweigh the benefit. |

#### A quick scoring approach

Count how many "automate" signs apply to a test and how many "manual" signs. If the automate signs clearly outnumber the manual signs, it is a candidate. If the answer is mixed, start manual and revisit later. This is a thinking aid, not a formula; always apply judgment.

```
 Is it repeated often?  ----- no -----> keep manual
        | yes
 Is the feature stable? ----- no -----> keep manual (revisit later)
        | yes
 Is a human judgment needed? -- yes --> keep manual
        | no
 Is it technically feasible and
 is the payback reasonable? -- no ----> keep manual
        | yes
     AUTOMATE
```

---

### 6. Return on investment (ROI) and break-even: a worked example

Automation costs money upfront. The question is: when does it pay for itself? The point at which total savings equal total investment is the **break-even point**. **ROI (return on investment)** measures how much you gain compared to what you spent.

> **Important:** All numbers below are **illustrative**, chosen to make the arithmetic easy. They are not industry benchmarks. Real teams must measure their own costs.

**Scenario:** A team has a set of 40 regression checks for the Project 1 web app. They run these twice a week.

**Assumptions (illustrative):**

| Item | Value |
|---|---|
| Time for a human to run the 40 checks once | 4 hours |
| Cost of a tester's time | $40 per hour |
| So, manual cost per run | 4 x $40 = **$160** |
| Runs per month (twice a week, about 8 times) | 8 |
| Time to build the automated scripts (one time) | 60 hours |
| Cost of an automation engineer's time | $50 per hour |
| So, one-time build cost | 60 x $50 = **$3,000** |
| Monthly maintenance of scripts | 4 hours x $50 = **$200** |
| Time to review automated results per run | 15 minutes at $40/hour = **$10** per run |

**Monthly cost:**

- Manual: 8 runs x $160 = **$1,280 per month**
- Automated (after build): $200 maintenance + (8 x $10 review) = $200 + $80 = **$280 per month**

**Monthly saving:** $1,280 - $280 = **$1,000 per month**

**Break-even point:** Build cost divided by monthly saving = $3,000 / $1,000 = **3 months**

**Cumulative cost, month by month:**

| Month | Manual (cumulative) | Automated (cumulative, including $3,000 build) | Who is cheaper? |
|---|---|---|---|
| 1 | $1,280 | $3,280 | Manual |
| 2 | $2,560 | $3,560 | Manual |
| 3 | $3,840 | $3,840 | Break-even |
| 4 | $5,120 | $4,120 | Automation |
| 6 | $7,680 | $4,680 | Automation |
| 12 | $15,360 | $6,360 | Automation |

**ROI after 12 months:**

- Total savings over 12 months = 12 x $1,000 = $12,000
- Net gain = $12,000 - $3,000 investment = $9,000
- ROI = $9,000 / $3,000 = **300%**

**Now the counter-example.** Suppose a different check will be run exactly once, for a one-time data migration. Manual cost is $160. Scripting it costs thousands. Automation never breaks even. Keep it manual.

Two lessons from this calculation:

1. **The number of times a test will run is the biggest driver of ROI.** Many runs favor automation; few runs favor manual.
2. **The calculation is only as good as its assumptions.** If the UI changes every sprint and maintenance triples, the break-even point moves far out. Real ROI also includes hard-to-measure benefits (faster feedback, fewer escaped defects) and hard-to-measure costs (flaky test investigation, tool licenses, training).

---

### 7. The test automation pyramid (introductory view)

Not all automated tests are equal. Some are fast, cheap, and stable. Others are slow, costly, and fragile. The **test automation pyramid**, popularized by Mike Cohn and discussed by Martin Fowler, is a simple model for deciding how many tests to write at each level.

```
                    /\
                   /  \        UI / End-to-End tests
                  / UI \       FEW: slow, costly, fragile,
                 /------\      but test the whole system
                /        \
               / Service  \    Service / API tests
              /   / API    \   SOME: faster, more stable,
             /--------------\  test business logic directly
            /                \
           /       Unit       \  Unit tests
          /                    \ MANY: very fast, cheap,
         /----------------------\ pinpoint problems exactly

   Speed:     slowest  <---------------------->  fastest
   Cost:      highest  <---------------------->  lowest
   Quantity:  fewest   <---------------------->  most
```

**Definitions:**

- **Unit test:** checks one small piece of code (a single function or class) in isolation. Example: does the `login()` function return the right message for a wrong password? Usually written by developers; runs in milliseconds.
- **Service / API test:** checks how parts of the system talk to each other, often through an **API** (application programming interface: a way for programs to send requests and receive responses without using a screen). Example: send a login request directly to the server and check the response. Faster and more stable than clicking through a browser.
- **UI (user interface) / end-to-end test:** drives the real application through the screen, like a user: open the browser, type, click, read the result. It checks the whole chain but is the slowest and most fragile.

#### Why too many UI tests is an anti-pattern

An **anti-pattern** is a common approach that looks sensible but causes problems. When a team builds mostly UI tests, the pyramid turns upside down into an "ice cream cone."

```
     Anti-pattern: "ice cream cone"

        ______________________
        \                    /
         \   MANY UI tests  /    slow, flaky, expensive
          \________________/
           \  some API    /
            \____________/
             \ few unit /
              \________/
```

Problems with the ice-cream cone:

- **Slow feedback:** the full suite takes hours.
- **Flakiness:** browsers, timing, and networks introduce random failures.
- **Expensive maintenance:** a small screen change breaks dozens of tests.
- **Hard to diagnose:** when a UI test fails, the cause could be anywhere in the system.

**The guideline:** test as much as you can at the lowest practical level, and keep a small number of UI tests for the critical user journeys. Later weeks cover the pyramid in detail; for now, remember the shape: wide and cheap at the bottom, narrow and expensive at the top.

---

### 8. What test automation is NOT

Many beginners hold wrong ideas about automation. Let us correct them directly.

1. **It is NOT a replacement for testers.** Automation replaces repetitive execution, not thinking. Someone still has to decide what to test, design good checks, investigate failures, and explore the product. Automation changes what testers spend their time on; it does not eliminate the need for them.
2. **It is NOT 100% automation.** Trying to automate every test is neither achievable nor economical. Usability, exploratory work, and one-off checks stay with people. Healthy teams target the right tests, not all tests.
3. **It is NOT a silver bullet.** It does not fix a poor process, unclear requirements, or bad test design. Automating a bad test just gives you a bad test that runs fast.
4. **It is NOT "free after the first build."** Scripts need ongoing care.
5. **It is NOT the same as quality.** Quality comes from the whole process (the QA mindset you studied today), not from a tool.

---

### 9. Myths and misconceptions

| Myth | Reality |
|---|---|
| "Automation will make manual testers obsolete." | Teams still need human judgment; roles evolve, and many testers grow into automation roles. |
| "Automated tests find more bugs than manual testing." | Automation is mainly good at re-checking known behavior (catching regressions). Humans, especially through exploration, usually find more new defects. |
| "Automation saves money immediately." | It costs more at first and pays back over time, as the ROI example showed. |
| "If all automated tests pass, the product is bug-free." | Tests only check what they were written to check. Passing tests prove only that those checks passed. |
| "We should automate everything." | Some tests are cheaper, safer, or only possible by hand. |
| "Once automated, always automated." | Scripts must be maintained, and sometimes retired. |
| "Anyone can record a test and be done." | Record-and-playback tools exist, but the resulting scripts are often fragile and need engineering skill to keep reliable. |
| "Automation is only for testers who can code like developers." | You need to learn programming basics, but you do not need to be a software architect to start. This course builds the skills step by step. |
| "Flaky tests are normal; just re-run them." | Ignoring flakiness teaches the team to ignore failures, including real ones. Flaky tests should be fixed or removed. |

---

### 10. Types of test automation (names only)

"Test automation" is an umbrella term. Here are the main types, defined briefly. Later weeks go deeper.

| Type | What it checks | Level of the pyramid |
|---|---|---|
| **Unit testing** | Individual functions or classes in isolation. | Base |
| **API testing** | Whether the server's interfaces accept requests and return correct responses. | Middle |
| **UI / end-to-end (E2E) testing** | Complete user journeys through the real screen (for example register, log in, and view a profile). | Top |
| **Performance testing** | How the system behaves under load: speed, stability, and capacity. (Covered Friday.) | Separate dimension |
| **Visual testing** | Whether the screen looks right by comparing screenshots against an approved baseline. | Top |
| **Contract testing** | Whether two services (a consumer and a provider) still agree on the format of the messages they exchange. | Middle |

### 11. Common tools (names only)

You will meet these names in job descriptions and in later weeks. **They are covered later in the course; today you only need to recognize them. We are not installing or configuring anything now.**

| Tool | Typically associated with |
|---|---|
| **Selenium** | Automating web browsers (UI testing); long established. |
| **Playwright** | Modern browser automation (UI/E2E and some API testing). |
| **Cypress** | Browser-based UI testing aimed at web developers. |
| **Postman** | Exploring and testing APIs. |
| **JUnit** | Unit testing framework for Java. |
| **pytest** | Testing framework for Python. |
| **JMeter** | Performance and load testing. |
| **Appium** | Automating mobile apps. |
| **Jenkins / GitHub Actions** | CI/CD tools that run your tests automatically (see below). |

Tools come and go; the concepts in this lesson stay valuable for your entire career. When someone asks which tool is "best," the honest answer is: it depends on the application, the team's language, and the goal.

---

### 12. The test automation lifecycle

Just as software has a lifecycle (SDLC) and testing has a lifecycle (STLC), automation has its own cycle. A common overview has six stages:

```
   +---------+    +--------+    +-------+
   | 1.Select| -> |2.Design| -> |3.Build|
   +---------+    +--------+    +-------+
        ^                           |
        |                           v
   +---------+    +--------+    +-------+
   |6.Report | <- |5.Maint.| <- | 4.Run |
   +---------+    +--------+    +-------+
```

| Stage | What happens | Example in Project 1 |
|---|---|---|
| **1. Select** | Decide what to automate using the checklist and ROI thinking. | Choose the valid-login check because it is critical and stable. |
| **2. Design** | Plan the test: steps, data, expected results, and how it fits the framework. | Define the data (username, password) and the expected "Welcome" message. |
| **3. Build** | Write the scripts, prepare data, and set up the framework and environment. | Code the test function with its assertion. |
| **4. Run** | Execute the tests, locally or on a schedule or in the CI/CD pipeline. | Run the suite after each code change. |
| **5. Maintain** | Update scripts when the application changes; fix flaky tests; remove obsolete ones. | The login button's label changed, so the script is updated. |
| **6. Report** | Share results with the team: pass/fail counts, trends, failures with evidence. | A dashboard shows 48 of 50 tests passed, with two defects logged. |

It is a loop: reports lead to new decisions about what to select, and maintenance is never "done." Many beginners underestimate stage 5.

---

### 13. Test automation in CI/CD (overview)

Two terms first:

- **Continuous Integration (CI):** developers frequently merge their code changes into a shared codebase, and each merge automatically triggers a build and a set of tests.
- **Continuous Delivery / Deployment (CD):** the tested software is automatically prepared (delivery) or released (deployment) to an environment.

Together, **CI/CD** is an automated pipeline that moves code from a developer's computer toward users. Automated tests are the safety gates in that pipeline.

```
 Developer      Source         Build         Automated tests        Deploy
 commits  -->   control  -->   server  -->  +----------------+ --> (if all
 code           (merge)        (compile)     | unit  (fast)   |     gates
                                             | API   (medium) |     pass)
                                             | UI    (few)    |
                                             +----------------+
                                                    |
                                                  fail
                                                    v
                                         Team is notified at once
```

Why this matters:

- A developer who breaks something learns within minutes, while the change is still fresh in their mind. Fixing it is cheap.
- No one has to remember to run the tests; the pipeline does it every time.
- Tests can run on a schedule (for example nightly) as well.

Without automation, CI/CD cannot work at speed, because a human cannot run hundreds of checks on every commit. This is one of the main reasons the industry values automation skills. Tools like Jenkins and GitHub Actions, which orchestrate these pipelines, are covered in later weeks.

---

### 14. The role of AI in testing (a realistic view)

Artificial intelligence is changing testing. It is useful to know both what it can do and where it must be handled carefully.

#### Where AI helps today

| Capability | What it means | Benefit |
|---|---|---|
| **AI-assisted test generation** | An AI model reads a requirement, user story, or code and suggests test cases or draft scripts. | Faster first drafts; helps you think of cases you missed. |
| **Self-healing locators** | A **locator** is how a script finds an element on a page (for example by its ID or label). If the page changes and the locator breaks, some tools use AI to find the most likely matching element and repair the script. | Less maintenance when small UI changes occur. |
| **Log and failure analysis** | AI summarizes large logs, groups similar failures, and suggests likely causes. | Faster diagnosis of failed runs. |
| **Test data generation** | AI can produce realistic, varied sample data (names, addresses, edge-case inputs). | Faster data preparation; broader variety. |
| **Prioritization** | AI can suggest which tests to run first based on what code changed. | Shorter feedback time. |

#### Honest limitations

- **AI can be confidently wrong.** Generated tests may contain incorrect expected results, or assert nothing meaningful.
- **It does not understand your business the way you do.** It may miss domain rules that were never written down.
- **Self-healing can hide real bugs.** If a button was removed on purpose and the tool "heals" to a different button, a real defect may pass silently.
- **Generated tests can be shallow,** covering the obvious path and missing the risky ones.
- **Data privacy matters.** Do not paste confidential requirements, customer data, or secrets into tools your organization has not approved.
- **Accountability stays with you.** If an AI-written test misses a defect, the team is still responsible.

#### The rule: human review is required

Treat AI as a fast, enthusiastic junior assistant: useful for drafts, but its work must be reviewed. A reviewer should ask: Does this test check the right requirement? Is the expected result correct? Would this test fail if the feature were broken? A tester who can judge AI output is more valuable, not less. The mindset you learned today (curiosity, skepticism, critical thinking) is exactly what makes AI usable safely.

---

### 15. Hybrid strategy: using both

The best teams do not pick a side. A **hybrid strategy** deliberately combines manual and automated testing so that each handles what it does best.

```
 +-------------------------+-----------------------------------+
 |      AUTOMATE           |        KEEP MANUAL                |
 +-------------------------+-----------------------------------+
 | Smoke checks per build  | Exploratory sessions on new work  |
 | Stable regression suite | Usability and look-and-feel       |
 | Data-heavy validations  | One-off and ad-hoc checks         |
 | Cross-browser repeats   | Features still being defined      |
 | API and unit checks     | Investigating odd failures        |
 +-------------------------+-----------------------------------+
            \                          /
             \    Shared goal: quality  /
              \  Shared results: Jira  /
```

A common workflow in an Agile sprint:

1. A new feature arrives. Testers **explore it manually** to learn it and find early defects.
2. Once the feature stabilizes, the most valuable, repeatable checks are **automated** and added to the regression suite.
3. Each sprint, automation protects old features while manual effort focuses on the new ones.
4. Findings from exploration feed back into new automated checks.

This way, human time moves from repeated work to creative, high-value work.

---

### 16. A small illustrative example in Python

Now let us see the same check done manually and then automatically. We will use a simple login scenario, which connects directly to Project 1.

> Python is the language used in this course. You do not need to master it today; focus on understanding the idea of the test, not the syntax. Every line is explained.

#### Part A: The manual test cases

| ID | Title | Preconditions | Steps | Test data | Expected result | Actual result | Status |
|---|---|---|---|---|---|---|---|
| TC-01 | Valid login | User "alice" exists | 1. Open login page. 2. Enter username. 3. Enter password. 4. Click Login. | alice / Secret#123 | Message "Welcome, alice" is shown | (tester fills in) | (Pass/Fail) |
| TC-02 | Wrong password | User "alice" exists | Same steps | alice / wrong | Message "Error: invalid credentials" | | |
| TC-03 | Unknown user | User "bob" does not exist | Same steps | bob / Secret#123 | Message "Error: invalid credentials" | | |
| TC-04 | Empty password | None | Same steps, leave password blank | alice / (empty) | Message "Error: username and password are required" | | |
| TC-05 | Empty username | None | Same steps, leave username blank | (empty) / Secret#123 | Message "Error: username and password are required" | | |

A human would perform these five cases, write down the actual results, and mark each Pass or Fail. Each time the login code changes, the human would repeat all five. At five cases that is easy. At 500 cases it is a heavy burden.

#### Part B: The same checks, automated

Below is a complete program. It contains a very simple `login` function (the "application") and five test functions that check it. Save it as `login_demo.py`.

```python
# login_demo.py - a tiny login function plus automated checks

VALID_USERS = {"alice": "Secret#123"}


def login(username, password):
    """Return a message describing the result of a login attempt."""
    if not username or not password:
        return "Error: username and password are required"
    if VALID_USERS.get(username) == password:
        return "Welcome, " + username
    return "Error: invalid credentials"


def test_valid_login():
    assert login("alice", "Secret#123") == "Welcome, alice"


def test_wrong_password():
    assert login("alice", "wrong") == "Error: invalid credentials"


def test_unknown_user():
    assert login("bob", "Secret#123") == "Error: invalid credentials"


def test_empty_password():
    assert login("alice", "") == "Error: username and password are required"


def test_empty_username():
    assert login("", "Secret#123") == "Error: username and password are required"


if __name__ == "__main__":
    tests = [test_valid_login, test_wrong_password, test_unknown_user,
             test_empty_password, test_empty_username]
    passed = 0
    for test in tests:
        try:
            test()
            print("PASS", test.__name__)
            passed += 1
        except AssertionError:
            print("FAIL", test.__name__)
    print(f"{passed} of {len(tests)} tests passed")
```

**How to run it:** in a terminal, in the folder containing the file, type `python login_demo.py`.

**Expected output:**

```
PASS test_valid_login
PASS test_wrong_password
PASS test_unknown_user
PASS test_empty_password
PASS test_empty_username
5 of 5 tests passed
```

(This output was produced by running the code exactly as shown.)

#### Part C: Line-by-line explanation

**The application code**

- `# login_demo.py - ...` A **comment**. Python ignores any line starting with `#`. Comments are notes for humans.
- `VALID_USERS = {"alice": "Secret#123"}` Creates a **dictionary**, a collection of key-value pairs. Here the key is the username `"alice"` and the value is her password. This is our stand-in for a user database. (In real software, passwords are never stored as plain text; this is a teaching simplification.)
- `def login(username, password):` Defines a **function** named `login` that accepts two inputs, called **parameters**.
- `"""Return a message ..."""` A **docstring**: a description of what the function does.
- `if not username or not password:` Checks whether either input is empty. In Python an empty string counts as "false," so `not username` is true when the username is blank.
- `return "Error: username and password are required"` Sends back this message and ends the function. This handles the empty-input cases (TC-04 and TC-05).
- `if VALID_USERS.get(username) == password:` Looks up the username in the dictionary. `.get()` returns the stored password, or `None` if the user does not exist. If it equals the typed password, the login is valid. The double equals `==` means "is equal to" (a single `=` assigns a value).
- `return "Welcome, " + username` Joins the text "Welcome, " with the username to build the success message.
- `return "Error: invalid credentials"` If neither earlier rule applied, the login failed. This covers wrong password and unknown user (TC-02 and TC-03).

**The test code**

- `def test_valid_login():` Defines a test. Naming test functions with the prefix `test_` is a convention that frameworks such as pytest use to discover tests automatically.
- `assert login("alice", "Secret#123") == "Welcome, alice"` This is the **Arrange-Act-Assert** pattern compressed into one line. It calls the login function with the test data (act), and asserts that the result equals the expected message. If the statement is true, nothing happens and the test passes. If false, Python raises an `AssertionError` and the test fails.
- The next four test functions do exactly the same for the other four manual test cases. Compare them with the table in Part A: each row of the table became one function. The "Expected result" column became the right side of the `==`.

**The mini test runner (the part under `if __name__ == "__main__":`)**

- `if __name__ == "__main__":` Means "run the following only when this file is executed directly." It keeps the runner from running if the file is imported elsewhere.
- `tests = [ ... ]` A **list** holding the five test functions (note: no parentheses, so we are storing the functions themselves, not calling them yet).
- `passed = 0` A counter starting at zero.
- `for test in tests:` A **loop** that takes each test from the list in turn.
- `try:` / `test()` Calls the test. `try` means "attempt this, and be ready for a problem."
- `print("PASS", test.__name__)` If the test finished without an error, print PASS and the function's name. `passed += 1` adds one to the counter.
- `except AssertionError:` If an assertion failed, jump here instead of crashing.
- `print("FAIL", test.__name__)` Print the failure.
- `print(f"{passed} of {len(tests)} tests passed")` A summary. The `f` before the quotes makes it an **f-string**, in which values inside braces are inserted into the text. `len(tests)` gives the number of tests.

In real projects you would not write this runner yourself. A **test runner** such as **pytest** discovers all functions starting with `test_`, runs them, and produces a detailed report. You would simply type `pytest` in the terminal. We write the small runner here only so you can see what a runner actually does. pytest is covered in later weeks.

#### Part D: What to notice

- The automated version runs in a fraction of a second. A human takes minutes.
- It will give identical results every time (repeatability).
- If someone breaks the login code tomorrow, one command tells us immediately.
- But the script cannot tell us whether the login page looks good or the error message is friendly. For that, we still need a person.
- Try it: change `"Secret#123"` in `VALID_USERS` to something else and re-run. Watch tests fail. That is a regression being caught.

---

## Examples

### Example 1: Choosing for a checkout page

**Situation:** An online shop has a checkout flow that has been stable for a year. Each release, a tester spends three hours checking it by hand. The business loses money if it breaks.

**Decision:** Automate. It is repetitive, stable, high-risk, and run often. The ROI is strongly positive.

### Example 2: Choosing for a new feature

**Situation:** The team just built a brand-new "Recommended for you" widget. The design is changing every few days.

**Decision:** Keep manual (exploratory) for now. Automating would produce scripts that break with each design change. Revisit when the feature stabilizes.

### Example 3: A hybrid release cycle

**Situation:** A team releases every two weeks. Automated smoke and API tests run on every build. Before release, testers spend a day on exploratory and usability testing of the new features. Defects found are logged in Jira, and the most important new checks are added to automation next sprint.

**Result:** Fast, reliable coverage of old features, plus human insight on new ones.

### Example 4: A flaky test

**Situation:** A UI test fails about one run in ten, with no code change. Investigation shows it clicks a button before the page has finished loading.

**Lesson:** The product is fine; the test is badly designed (a timing problem). This is why maintenance and quality of test code matter. Fix it properly rather than ignoring it.

---

## Try It: Classification Exercise

For each of the 15 scenarios below, decide: **Automate** or **Keep manual** (or **Start manual, automate later**). Write one sentence of reasoning, then compare with the answer key.

1. Verifying that the login page accepts valid credentials; this check must run on every build.
2. Checking whether a newly redesigned registration page feels intuitive to first-time users.
3. A one-time check that data was migrated correctly from an old system to a new one.
4. Running the same 30 checkout checks on Chrome, Firefox, and Edge every release.
5. Exploring a brand-new, half-finished "wishlist" feature to find unexpected problems.
6. Validating a tax-calculation function with 200 different input combinations.
7. Checking that the website's pages look right on a new phone model (colors, spacing, readability).
8. Confirming that the application homepage loads and the main menu is visible after each deployment (a smoke check).
9. Simulating 5,000 users logging in at the same time to see how the system responds.
10. Testing a screen whose layout and labels are being redesigned every sprint.
11. Verifying that every field on the registration form rejects invalid input (for example, an email without "@") using many sample values.
12. Evaluating whether the error messages in the app sound polite and helpful.
13. Checking that a payment API returns the correct status code and response format for valid and invalid requests.
14. A quick ad-hoc check, by an experienced tester, of a bug fix someone just committed, to see if "anything else looks off."
15. Re-checking the 150 existing features of a mature product after every code change.

### Answer key

| # | Decision | Reasoning |
|---|---|---|
| 1 | **Automate** | Critical, stable, and run on every build; ideal smoke/regression check. |
| 2 | **Keep manual** | "Intuitive" is a human judgment; this is usability testing. |
| 3 | **Keep manual** | One-time; scripting cost will never be repaid. (A quick script for comparing record counts may be reasonable, but a full automation suite is not.) |
| 4 | **Automate** | Cross-browser repetition is tiresome for humans and easy for machines. |
| 5 | **Keep manual** | New, unstable, and exploratory; needs curiosity and adaptability. |
| 6 | **Automate** | Data-heavy with many combinations; best handled at the unit or API level. |
| 7 | **Keep manual** | Visual and device-feel judgment; human eyes are best (visual automation tools can help later, but human review remains). |
| 8 | **Automate** | Classic smoke test: quick, repeated, and gives instant feedback. |
| 9 | **Automate** | Humans cannot generate that load; needs performance tooling (covered Friday). |
| 10 | **Keep manual** | Rapidly changing UI would cause constant script breakage. |
| 11 | **Automate** | Many input values and a stable rule; ideal for automated, data-driven checks (data-driven testing is covered Friday). |
| 12 | **Keep manual** | Tone and helpfulness need human judgment. |
| 13 | **Automate** | Stable, precise, and repeatable; API tests are fast and reliable. |
| 14 | **Keep manual** | Ad-hoc and exploratory by nature; relies on experience and intuition. |
| 15 | **Automate** | A large regression set run after every change; the textbook case (regression testing is covered Friday). |

**Scoring:** 13-15 correct, excellent judgment. 10-12, solid; review the criteria tables. Under 10, re-read sections 5 and 6. Remember that some items have defensible alternatives; the reasoning matters more than the label.

---

## Project 1: What Should We Automate First?

Wednesday's exercise has you write positive and negative test cases for the login and registration features of the Project 1 web app. Now, consider which of those checks to automate first. Do not automate all of them. Use the checklist.

**Candidate checks and a proposed priority:**

| Priority | Check | Type | Decision | Justification |
|---|---|---|---|---|
| 1 | Valid login with correct credentials succeeds | Positive, smoke | **Automate first** | Business critical (if login fails, nothing else works), stable, and runs on every build. |
| 2 | Login with wrong password is rejected with the correct message | Negative, regression | **Automate** | High risk (security), stable, and simple to script. |
| 3 | Login with empty username or password shows the required-field message | Negative | **Automate** | Quick, stable, and repeated often. |
| 4 | Registration with valid details creates an account | Positive, smoke | **Automate** | Critical path; if registration breaks, no new users can join. |
| 5 | Registration rejects duplicate email | Negative, regression | **Automate** | Important business rule; stable. |
| 6 | Registration field validation with many invalid values (bad email formats, short passwords) | Negative, data-heavy | **Automate (later, with data-driven approach)** | Many combinations suit automation (data-driven testing is covered Friday). |
| 7 | Login works across Chrome, Firefox, Edge | Cross-browser | **Automate (once core scripts are stable)** | Easy extension of existing scripts. |
| 8 | Is the registration form easy and clear to complete? | Usability | **Keep manual** | Needs human judgment. |
| 9 | Do error messages look right and sound helpful? | Visual/usability | **Keep manual** | Human perception needed. |
| 10 | Exploratory session: try unusual inputs (very long names, special characters, double-clicking Submit) | Exploratory | **Keep manual** | Finding the unexpected is a human strength. |
| 11 | Any element of the registration page still under redesign | Changing UI | **Keep manual for now** | Scripts would break constantly. |

**Why this order?** We start with the checks that are critical, stable, and quick to script, because they deliver the most protection for the least effort and give fast feedback. We lean toward API- or function-level checks where possible (the base of the pyramid) and keep UI-level automation to the critical journeys. Anything unstable, subjective, or exploratory stays with human testers, who will also use their findings to suggest the next automation candidates.

**Your task:** Take the positive and negative test cases you write in today's exercise. Mark each with "Automate," "Keep manual," or "Later," and write one sentence of justification, using the decision checklist.

---

## Career Paths and Skills Roadmap

Quality engineering offers a ladder you can climb at your own pace. Titles vary between companies, but a typical progression looks like this:

```
 Manual QA Tester
      |   (learn programming, automation basics)
      v
 Junior Automation Engineer / QA Automation Engineer
      |   (learn frameworks, APIs, CI/CD, design patterns)
      v
 SDET (Software Development Engineer in Test)
      |   (learn architecture, strategy, mentoring, quality metrics)
      v
 Senior SDET / Lead Quality Engineer
      |
      v
 Quality Engineering Manager / Quality Architect
```

An **SDET** is a person who combines development skills and testing skills, building test tools and frameworks as well as tests. A **Quality Engineer (QE)** looks beyond testing to improve quality across the whole lifecycle: prevention, process, automation, and monitoring.

**Skills roadmap (what you will build over time):**

| Stage | Skills |
|---|---|
| **Foundation (Weeks 1-3)** | SDLC/STLC, test design basics, defect reporting, Jira, quality mindset, manual vs. automation judgment. |
| **Programming basics** | Python fundamentals, reading and writing simple functions, using assertions. |
| **Test automation basics** | A test framework (such as pytest), browser automation, locators, waits, reports. |
| **API and data skills** | API testing, JSON, SQL basics, test data management. |
| **Pipeline skills** | Git, CI/CD tools, running tests automatically. |
| **Advanced** | Framework design, performance testing, visual and contract testing, using AI tools responsibly, test strategy. |
| **Soft skills (always)** | Communication, curiosity, collaboration with developers, risk-based thinking. |

Notice that manual testing skills never stop being useful. The best automation engineers are strong testers first: they know what is worth checking.

---

## Knowledge Check

Try to answer these before looking at the answers.

1. In one sentence, what is the difference between manual and automated testing?
2. Name three strengths of manual testing and three weaknesses of automated testing.
3. What is an assertion? Give an example in plain English.
4. What is a flaky test, and why is it harmful?
5. A test will be run only once. Should you automate it? Why or why not?
6. In the worked ROI example, how was the break-even point calculated, and what was it?
7. Draw or describe the test automation pyramid. Which level should have the most tests?
8. Why is having mostly UI tests considered an anti-pattern?
9. True or false: "If all automated tests pass, the product has no defects." Explain.
10. Name two things AI can help with in testing, and two limitations.
11. List the six stages of the test automation lifecycle in order.
12. Why do automated tests fit naturally into a CI/CD pipeline?
13. Give two reasons usability testing is usually kept manual.
14. In Project 1, which login check would you automate first, and why?
15. What does SDET stand for, and how does it differ from a manual tester?

### Answers

1. Manual testing is performed by a human following test steps by hand; automated testing uses software to execute tests and compare actual with expected results.
2. Manual strengths (any three): exploratory ability, usability judgment, ad-hoc testing, visual checking, human judgment, low startup cost. Automated weaknesses (any three): upfront cost, maintenance, flaky tests, cannot judge usability, false sense of security, requires technical skill.
3. An assertion is a statement in a test that must be true for the test to pass. Example: "The message after a valid login must be 'Welcome, alice'."
4. A flaky test sometimes passes and sometimes fails without any change to the product. It is harmful because it wastes investigation time and teaches the team to ignore failures, including real ones.
5. No. The scripting cost will not be repaid by a single run, so it is cheaper to run it manually.
6. Break-even = one-time build cost / monthly saving = $3,000 / $1,000 = 3 months (illustrative numbers).
7. Wide base of unit tests (most), a middle layer of service/API tests (some), and a narrow top of UI/end-to-end tests (fewest). Unit tests should be the most numerous.
8. UI tests are slow, fragile, expensive to maintain, and hard to diagnose; too many give slow feedback and constant breakage. It is better to test at lower levels where possible.
9. False. Tests check only what they were written to check; defects can exist in areas not covered, and the tests themselves could be flawed.
10. Helps (any two): drafting test cases, self-healing locators, log analysis, test data generation, test prioritization. Limitations (any two): can be confidently wrong, may miss business rules, self-healing may hide real defects, shallow tests, data privacy risk, human review still required.
11. Select, design, build, run, maintain, report.
12. They run automatically and quickly on every code change, giving fast feedback and acting as gates before release, without needing a person to start them.
13. Usability depends on human perception and opinion (is it easy, pleasant, clear?), which a script cannot judge; real users' reactions and context matter.
14. Valid login with correct credentials: it is business critical, stable, a smoke check, and run on every build.
15. Software Development Engineer in Test. An SDET combines programming and testing skills to build automated tests and test tooling, while a manual tester focuses on executing tests by hand and applying human judgment (though the best SDETs also retain strong testing instincts).

---

## Key Takeaways

- **Manual testing** is human-executed; its strengths are exploration, usability, visual checks, and judgment. Its weaknesses are speed, repetition, and scalability.
- **Automated testing** uses scripts, data, frameworks, runners, assertions, and reports to execute tests and compare actual with expected results. Its strengths are speed, repeatability, and CI/CD integration. Its weaknesses are upfront cost, maintenance, flakiness, and blindness to usability.
- Neither approach is better overall. Use a **hybrid strategy**: automate the repetitive, stable, and high-risk; keep manual the new, changing, subjective, and exploratory.
- Decide using a **checklist** and an **ROI/break-even** estimate. The number of times a test will run is the biggest factor.
- The **test pyramid** says: many unit tests, some API tests, few UI tests. Too many UI tests is an anti-pattern.
- Automation is **not** a replacement for testers, **not** 100%, and **not** a silver bullet. A green test run is not proof of quality.
- The automation lifecycle (**select, design, build, run, maintain, report**) is a loop; maintenance is never finished.
- In **CI/CD**, automated tests act as fast, automatic gates.
- **AI** speeds up drafting tests, data, and analysis, but it needs human review and does not remove accountability.
- Careers progress from manual QA toward automation engineer, SDET, and quality engineer. Strong manual testing foundations remain valuable at every stage.

---

## Additional Resources

- **Martin Fowler: The Test Pyramid** - a short, widely cited explanation of the pyramid concept: https://martinfowler.com/bliki/TestPyramid.html
- **Selenium Documentation** - official documentation for the Selenium browser automation project (for reference; used in later weeks): https://www.selenium.dev/documentation/
- **Playwright Documentation** - official documentation for Playwright (for reference; used in later weeks): https://playwright.dev/docs/intro
