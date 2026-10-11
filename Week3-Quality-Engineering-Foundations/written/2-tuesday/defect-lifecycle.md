# Defect Lifecycle: From "Found It" to "Fixed and Verified"

**Week 3 - Quality Engineering Foundations | Tuesday: Test Management and Defect Lifecycle**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain in practical terms what a defect (bug) is, and why disciplined defect management matters to a team and a product.
2. Describe every state in a typical defect lifecycle (New, Assigned, Open, In Progress, Fixed, Ready for Retest, Verified/Closed, Reopened, Rejected, Deferred, Duplicate, Not a Bug / Cannot Reproduce, Won't Fix), including who moves a defect into and out of each state.
3. Read and draw a defect state diagram and use a transition table to decide which moves are legal.
4. Compare a simple 5-state workflow with a detailed 12-state workflow and explain why organizations differ.
5. Name the roles that touch a defect (tester/reporter, dev lead/triager, developer, product owner, release manager) and describe what happens in a defect triage meeting.
6. Write a clear, complete, reproducible defect report using a standard template, and tell a good report from a bad one.
7. Explain severity versus priority, place defects on a severity/priority matrix, and give examples of each combination.
8. Classify defects by type and by root cause category.
9. Calculate and interpret simple defect metrics: defect age, defect leakage, defect density (and the related defect removal efficiency).
10. Handle disagreements with developers professionally and with evidence.
11. Describe the prevention mindset, and run a simple root cause analysis using 5 Whys and a fishbone diagram.
12. Retest a fix, run a quick regression check, and trace a defect back to its test case and requirement.
13. Use AI tools to help draft bug reports, while knowing their limits and the cautions that apply.

---

## Why This Matters

Earlier today you looked at requirements analysis, test planning, and test execution. Execution is where the test plan meets reality, and reality usually answers back with a surprise: something did not behave the way the requirement said it should. What happens next is just as important as the finding itself.

Imagine two testers who each find the same problem on the checkout page of your Project 1 application.

Tester A writes in the team chat: "checkout broken." The developer asks which browser, which account, what steps. Tester A is in a meeting. Two days pass. The developer cannot reproduce the problem, marks it "works on my machine," and the problem ships.

Tester B writes a short, structured report: exact steps, the build number, the browser, what was expected, what actually happened, a screenshot, and a link to the requirement. The developer reproduces it in five minutes, fixes it before lunch, and Tester B verifies the fix that afternoon.

The product, the code, and the bug are identical in both stories. The only difference is how the defect was handled. That is what this lesson is about.

Defect management matters because:

- **Defects are the main output of testing.** Test cases are inputs; defects and the confidence that there are no serious ones are the outputs the business actually pays for.
- **Communication is the real job.** A defect report is a message from a tester to a developer, a manager, and sometimes a customer. Poor messages cost time and money.
- **Decisions depend on it.** Whether a release goes out on Friday depends on which defects are open, how serious they are, and how fast they are being closed.
- **History becomes knowledge.** A well-kept defect log tells the team where the product is weak and where the process leaks, so the same mistakes are not repeated.
- **It is a core QE skill.** Quality Engineers are hired largely on the strength of how they find, describe, track, and help prevent defects. AI tools can help, but only if you understand what a good defect looks like.

---

## The Concept

### 1. What is a defect (bug)?

In everyday work, people say "defect" and "bug" to mean the same thing, and this lesson does the same. In practical terms:

> A **defect** (or **bug**) is a flaw in a work product, such as software, a requirement, a design, or a test, that makes it behave differently from what it should.

"What it should" comes from somewhere: the requirements, the design, the user stories and acceptance criteria, an industry standard, or reasonable user expectations. If there is no expectation, there is no defect, only an observation. That is why testers who know the requirements well find better bugs.

Some practical examples in a web application:

- A "Place Order" button does nothing when clicked.
- A total shows 45.00 when two items of 20.00 each are in the cart and no discount applies.
- The page layout overlaps text on a phone screen.
- A password reset email takes 15 minutes to arrive when the requirement says 1 minute.
- A user can view another user's order by changing a number in the URL.

Notice the range: a defect can be about function, appearance, speed, security, or data. We will classify them later in this lesson.

**A note on vocabulary.** Textbooks distinguish carefully between an *error* (a human mistake), a *defect* (the flaw that mistake leaves in a work product), and a *failure* (the visible wrong behavior when the flaw is triggered). We will teach that distinction formally on Wednesday. For today, whenever you read "defect" or "bug," think "something is wrong and someone needs to track it until it is dealt with."

### 2. Why we manage defects: the package-tracking analogy

When you order something online, you receive a tracking number. You can see "Order placed," "Packed," "Shipped," "Out for delivery," "Delivered." Every status has an owner (the warehouse, the courier, you), and every status tells you what happens next. If a package is lost, there is a separate path ("Investigation," "Refund issued").

A defect lifecycle is the same idea for bugs. Without it:

- Nobody knows who is responsible for a bug right now.
- Bugs get lost in chat messages and emails.
- The same bug is reported three times.
- Fixed bugs are never rechecked, so "fixed" means "someone said so."
- Management has no reliable picture of product health.

With it, every defect has a visible status, a named owner, and a defined next step.

A second analogy is a **hospital patient journey**. A patient arrives (defect found), is registered (logged), is examined by a triage nurse who decides how urgent the case is (triage), is assigned to a doctor (assigned), is treated (fixed), is checked after treatment to confirm recovery (retested), and is discharged (closed). Sometimes the patient is sent home because nothing is wrong (not a bug), is told to come back later because the condition is not urgent (deferred), or comes back because the treatment did not work (reopened). If you keep the hospital picture in mind, most of the states below will feel familiar.

### 3. The complete defect lifecycle

The **defect lifecycle** (also called the **bug lifecycle**) is the series of states a defect passes through from the moment it is found until it is finally resolved, together with the rules for who may move it from one state to another.

Different organizations name and count the states differently (we compare variations later), but the following is a thorough, widely recognized set. For each state we give a definition, who normally moves the defect into it, the entry condition, and where it can go next.

#### New

- **Definition:** The defect has just been logged and nobody has yet reviewed it.
- **Moved by:** The tester (reporter). Anyone can raise a defect: testers, developers, product owners, even support staff.
- **Entry condition:** A tester has observed behavior that differs from expectations and has recorded it in the defect tracker with enough information to be understood.
- **Next states:** Assigned (accepted and given to a developer), Rejected (not valid), Duplicate (already reported), Not a Bug / Cannot Reproduce, Deferred (valid but not now).

#### Assigned

- **Definition:** The defect has been reviewed, accepted as valid, and given to a specific developer (or team) to fix.
- **Moved by:** The dev lead or triager, often after a triage meeting. In small teams, the developer may self-assign.
- **Entry condition:** The defect is confirmed as valid, has a severity and priority, and has an owner.
- **Next states:** Open (the developer has accepted it), In Progress, Deferred, Rejected, Duplicate, Not a Bug / Cannot Reproduce.

#### Open

- **Definition:** The developer has accepted the defect and it is on their active list.
- **Moved by:** The developer (or the lead as part of assignment).
- **Entry condition:** The assignee has acknowledged the defect. Some organizations use "Open" as the first state after "New" and skip a separate "Assigned" state.
- **Next states:** In Progress, Rejected, Duplicate, Not a Bug / Cannot Reproduce, Deferred, Won't Fix.

#### In Progress

- **Definition:** The developer is actively working on analysis and the fix.
- **Moved by:** The developer.
- **Entry condition:** The developer has started work, investigating the cause or changing code.
- **Next states:** Fixed, Cannot Reproduce (if the developer cannot recreate it), Deferred, Won't Fix, back to Assigned (if reassigned).

#### Fixed

- **Definition:** The developer has made a code or configuration change that they believe resolves the defect.
- **Moved by:** The developer.
- **Entry condition:** The change is made, reviewed (for example through a code review or pull request), and merged into the code line. Note the word "believe": a defect that is "Fixed" is not yet "Verified."
- **Next states:** Ready for Retest (once the fix is in a build the tester can use). In many tools, Fixed and Ready for Retest are combined.

#### Ready for Retest (also called Retest or Pending Retest)

- **Definition:** The fix is available in a test environment and waiting for a tester to confirm it.
- **Moved by:** The developer, or automatically by the build and deployment process once the fix is included in a build.
- **Entry condition:** The fix is deployed to a test environment, and the build or version number that contains the fix is recorded on the defect.
- **Next states:** Verified/Closed (fix works), Reopened (fix does not work).

#### Verified / Closed

- **Definition:** The tester has retested the fix and confirmed that the defect is gone and nothing new broke. The defect's story is over.
- **Moved by:** The tester (usually the original reporter or another tester).
- **Entry condition:** The original steps now produce the expected result, and a quick regression check around the fix is clean. Some organizations use two separate states: **Verified** (the tester confirms) and **Closed** (a lead or release manager formally closes after release). Others merge them into one.
- **Next states:** Reopened, if the problem comes back later. Otherwise this is the end of the line.

#### Reopened

- **Definition:** A defect that was thought to be fixed or closed is shown to still exist, or to have returned.
- **Moved by:** The tester (or any person who sees it recur).
- **Entry condition:** Retest fails, or a closed defect is seen again in a later build. The tester should add a comment with evidence, including the build number where it fails.
- **Next states:** Assigned or Open (back to a developer), then the cycle continues. A defect that is reopened several times is a warning sign worth discussing in triage.

#### Rejected

- **Definition:** The defect is judged not valid and no fix will be made.
- **Moved by:** The dev lead, developer, or triage group, with a recorded reason. In some teams the product owner decides.
- **Entry condition:** The report describes behavior that is actually correct, a misunderstanding, or something outside the product's scope.
- **Next states:** Reopened (if the reporter provides evidence the rejection was wrong) or Closed.

#### Duplicate

- **Definition:** The defect describes the same problem as another defect that is already logged.
- **Moved by:** The triager or developer, who links to the original defect.
- **Entry condition:** A matching defect already exists. The duplicate is linked to the original, which becomes the single "master" defect.
- **Next states:** Closed (linked to the original). When the original is fixed, duplicates are rechecked and closed.

#### Not a Bug / Cannot Reproduce

These two are related and often shown together, though they mean different things.

- **Not a Bug (also "Works as Designed")**
  - **Definition:** The behavior is intended according to the requirements or design.
  - **Moved by:** Developer or triager, with explanation and a pointer to the requirement. The product owner confirms if the requirement is unclear.
  - **Next states:** Closed. If the tester believes the design itself is wrong, a change request or new requirement may be raised.
- **Cannot Reproduce**
  - **Definition:** The developer followed the steps but could not make the problem appear.
  - **Moved by:** The developer, after honest attempts in the stated environment.
  - **Entry condition:** Steps were followed exactly on the stated build and environment and the problem did not occur.
  - **Next states:** Reopened (the reporter supplies more details, such as a video, logs, or an exact data set) or Closed if the problem cannot be reproduced after reasonable effort.

Note that "Cannot Reproduce" is a signal about the *report* as much as the product. Intermittent problems are real, and a good reporter notes the frequency and conditions so that the developer has a fair chance.

#### Deferred

- **Definition:** The defect is valid but will be fixed in a later release, not the current one.
- **Moved by:** The triage group, the product owner, or the release manager. A developer alone should not defer a defect.
- **Entry condition:** The fix is not needed for the current release, for example because the impact is small, there is an acceptable workaround, or the risk of changing code now outweighs the benefit.
- **Next states:** Assigned or Open when scheduled into a future release. Deferred defects must be reviewed regularly, or they become a graveyard.

#### Won't Fix

- **Definition:** The defect is valid but the organization has decided it will never be fixed.
- **Moved by:** The product owner (or triage group) with a recorded business reason.
- **Entry condition:** The cost or risk of the fix is higher than the benefit, the affected feature is being retired, or the defect affects an unsupported environment.
- **Next states:** Closed. It can be reopened if business conditions change, for example if complaints surge.

### 4. The state diagram

Below is the full lifecycle drawn as an ASCII state diagram. Read the arrows as "may move to." Do not worry if this looks busy; most defects travel along the main path in the middle.

```
                               +-----------+
                               |    NEW    |  <-- tester logs the defect
                               +-----+-----+
                                     |
                 triage / review     |
     +-----------+-----------+-------+---------+-----------------+
     |           |           |                 |                 |
     v           v           v                 v                 v
+---------+ +-----------+ +-------------+ +-----------+   +-----------+
| REJECTED| | DUPLICATE | | NOT A BUG / | | DEFERRED  |   | ASSIGNED  |
|         | | (linked)  | | CANNOT REPRO| | (later)   |   | (to dev)  |
+----+----+ +-----+-----+ +------+------+ +-----+-----+   +-----+-----+
     |            |              |              |               |
     |            |              |   scheduled  |               v
     |            |              |   in future  |         +-----------+
     |            |              |   release    +-------->|   OPEN    |
     |            |              |                        +-----+-----+
     |            |              |                              |
     |            |              |  (won't fix decision)        v
     |            |              |      +-----------+     +-------------+
     |            |              |      | WON'T FIX |<----| IN PROGRESS |
     |            |              |      +-----+-----+     +------+------+
     |            |              |            |                  |
     |            |              |            |                  v
     |            |              |            |            +-----------+
     |            |              |            |            |   FIXED   |
     |            |              |            |            +-----+-----+
     |            |              |            |                  |
     |            |              |            |                  v
     |            |              |            |         +-----------------+
     |            |              |            |         | READY FOR RETEST|
     |            |              |            |         +--------+--------+
     |            |              |            |           pass /  \  fail
     |            |              |            |               /    \
     |            |              |            |              v      v
     v            v              v            v     +--------------+  +-----------+
 +---------------------------------------------+    |VERIFIED /    |  | REOPENED  |
 |                   CLOSED                    |<---|CLOSED        |  +-----+-----+
 +---------------------------------------------+    +--------------+        |
                                                                             |
                           back to ASSIGNED / OPEN  <------------------------+

 Also: a CLOSED / REJECTED defect can move to REOPENED if new evidence
 shows it was wrong or it comes back later.
```

The "happy path" (the route most defects take) is:

**New -> Assigned -> Open -> In Progress -> Fixed -> Ready for Retest -> Verified/Closed**

### 5. Transition table: from, to, who, when

This table is the rulebook. If a move is not in the table, it should not happen. Most tools let administrators enforce these rules so that, for instance, a defect cannot jump from "New" straight to "Closed."

| From | To | Who moves it | When (condition) |
|---|---|---|---|
| (none) | New | Tester / any reporter | A deviation is observed and logged with full details |
| New | Assigned | Dev lead / triager | Defect is valid, severity and priority set, owner chosen |
| New | Rejected | Dev lead / triager | Behavior is correct or out of scope; reason recorded |
| New | Duplicate | Triager / developer | Same problem already logged; link added |
| New | Not a Bug / Cannot Reproduce | Triager / developer | Matches design, or steps do not reproduce it |
| New | Deferred | Triage group / product owner | Valid, but fix is not for this release |
| Assigned | Open | Developer | Developer accepts the defect |
| Assigned | Rejected / Duplicate / Not a Bug | Developer (with lead's agreement) | Further analysis shows it is invalid or repeated |
| Open | In Progress | Developer | Work on the fix starts |
| Open | Won't Fix | Product owner / triage group | Business decides never to fix; reason recorded |
| Open | Deferred | Triage group / product owner | Postponed to a later release |
| In Progress | Fixed | Developer | Change is coded, reviewed, and merged |
| In Progress | Cannot Reproduce | Developer | Honest attempts fail to recreate the problem |
| Fixed | Ready for Retest | Developer / build process | Fix is deployed to a test environment; build number recorded |
| Ready for Retest | Verified / Closed | Tester | Original steps pass and a regression check is clean |
| Ready for Retest | Reopened | Tester | Original steps still fail, or the fix broke something else |
| Verified / Closed | Reopened | Tester / anyone | Defect reappears in a later build |
| Rejected / Not a Bug / Cannot Reproduce | Reopened | Tester (with new evidence) | Reporter provides information that changes the verdict |
| Rejected / Duplicate / Won't Fix | Closed | Lead / triager | Decision is final and documented |
| Deferred | Assigned / Open | Product owner / triage group | Scheduled into a future release |
| Reopened | Assigned / Open | Dev lead / developer | Returned to a developer for another attempt |

Two golden rules hide in this table:

1. **Only a tester (or the reporter) closes a fixed defect.** Developers fix; testers verify. A separate pair of eyes is the whole point.
2. **Every "not going to fix" decision needs a recorded reason.** "Rejected," "Won't Fix," "Deferred," and "Cannot Reproduce" must always include a comment saying why, so the reporter and future readers understand.

### 6. Variations across organizations and tools

No two companies use exactly the same workflow. Some use a handful of states; others use a dozen or more. The differences usually reflect team size, how regulated the industry is, and how much control the organization wants.

**A simple 5-state workflow** is popular in small teams and in agile teams that value speed:

```
 To Do  -->  In Progress  -->  Fixed / In Review  -->  Done (Verified)
   ^                                  |
   +----------- Reopened -------------+
```

| State | Meaning |
|---|---|
| Open (To Do) | Logged and waiting |
| In Progress | A developer is working on it |
| Fixed (Ready for Retest) | Fix is done and awaiting verification |
| Closed (Done) | Verified or otherwise resolved (with a "resolution" such as Fixed, Duplicate, Won't Fix, Cannot Reproduce) |
| Reopened | Fix failed or defect returned |

Here, reasons like Duplicate or Won't Fix are not separate states but a **resolution** field added when the defect is closed. This is how many modern tools, including Jira, commonly work. You will see the mechanics of this in the Jira lessons later today.

**A detailed 12-state workflow** is more common in larger or regulated organizations (finance, healthcare, aviation), where each step must be auditable:

New, Assigned, Open, In Progress, Fixed, Ready for Retest, Retesting, Verified, Closed, Reopened, Deferred, and Rejected (with Duplicate, Not a Bug, Cannot Reproduce, and Won't Fix as resolutions or additional states).

| Feature | Simple 5-state | Detailed 12-state |
|---|---|---|
| Best for | Small or agile teams, fast feedback | Large, regulated, or distributed teams |
| Control and audit trail | Light | Strong |
| Speed | Faster; fewer clicks | Slower; more handoffs |
| Risk | Decisions hidden in comments; states can be skipped | Bureaucracy; defects waiting in queues between states |
| Where "why" is stored | Resolution field plus comments | Distinct states plus comments |

Neither approach is "right." The skill to build is to read any workflow and map its names to the core ideas: *reported, accepted, being fixed, fixed, verified, closed, or set aside with a reason.* For example, one company's "Resolved" is another's "Fixed," and one tool's "Done" is another's "Closed."

### 7. Roles in the defect lifecycle

A defect passes through several hands. Knowing who does what keeps handoffs clean and avoids blame.

| Role | What they do with defects |
|---|---|
| **Tester / reporter** | Finds the defect, confirms it, writes the report, supplies evidence, answers developer questions, retests the fix, and closes or reopens. |
| **Dev lead / triager** | Reviews new defects, checks validity and completeness, confirms severity, proposes priority, assigns an owner, detects duplicates, and chairs or attends triage. |
| **Developer** | Investigates the cause, reproduces, fixes, adds a unit test where sensible, comments on what was changed and in which build, and marks it ready for retest. |
| **Product owner (PO)** | Decides business priority and the final call on "Won't Fix," "Deferred," and "Works as Designed" when requirements are unclear. Represents the customer's interests. |
| **Release manager** | Decides, based on open defects, whether a build is fit to release; tracks which fixes are in which build; may approve urgent fixes ("hotfixes"). |

In a small team one person may wear several hats. What matters is that the *responsibilities* are covered and the *decisions are recorded.*

### 8. Defect triage meeting (defect review board)

**Triage** is a word borrowed from medicine: sorting patients by urgency so scarce resources help the most critical first. A **defect triage meeting** (also called a **defect review board**, **bug scrub**, or **bug review**) is a regular, short meeting in which the team reviews new, reopened, and disputed defects and makes decisions about them.

**Purpose:**

- Make sure every new defect is understood and valid.
- Agree on severity and priority consistently.
- Assign owners and target releases.
- Remove duplicates and invalid reports.
- Decide what is fixed now, deferred, or declined.
- Keep the backlog healthy and visible.

**Typical attendees:**

- QE lead or the testers who raised the defects (explain and demonstrate).
- Dev lead (technical feasibility and effort).
- Product owner or business analyst (business impact and priority).
- Release manager or project manager (schedule impact).
- Others as needed, such as a security or UX specialist.

**How it runs (example, 30 minutes, daily during a test cycle or twice weekly otherwise):**

1. Go through new and reopened defects, highest severity first.
2. For each: confirm it is reproducible, agree severity and priority, decide the action.
3. Record decisions in the tracker immediately so the meeting does not need minutes.
4. Review defects that are overdue or stuck.

**Possible outcomes for each defect:**

| Outcome | Result |
|---|---|
| Accept and assign | Goes to a developer with a target build or sprint |
| Request more information | Returns to the reporter with specific questions |
| Reject or Not a Bug | Closed with a reason |
| Duplicate | Linked to the master defect |
| Defer | Scheduled for a future release with a review date |
| Won't Fix | Closed with a documented business decision |
| Escalate | Raised to management when it threatens the release |

Triage is about decisions, not debates. If a discussion about one defect takes more than a few minutes, take it offline and move on.

### 9. How to write an excellent defect report

A defect report is a small piece of technical writing with a very practical goal: *a stranger should be able to understand, reproduce, and judge the defect without asking you anything.* If the developer has to come back with questions, the report was not finished.

Here are the fields of a strong defect report and what each should contain.

| Field | What to write | Tip |
|---|---|---|
| **Title (summary line)** | A short, specific one-line description: what is wrong, where | Follow "[Area] - What happens when what", e.g. "Checkout - Total shows 40.00 instead of 36.00 after applying 10% coupon" |
| **Description / summary** | One or two sentences expanding on the title and the impact | Plain language; no blame; no guessing at the cause |
| **Environment** | Where you saw it: operating system, browser and version, device, test environment name (QA, staging), user role | Same bug on one browser but not another is a valuable clue |
| **Build / version** | Exact application build or version number or commit | Without this, nobody knows whether the defect still exists |
| **Steps to reproduce** | Numbered, exact, minimal steps, starting from a known state, including test data | Each step is one action. Include precise inputs. |
| **Expected result** | What should happen, according to the requirement or reasonable expectation | Cite the requirement if possible |
| **Actual result** | What really happened, including exact error text | Copy messages exactly |
| **Severity** | How serious the technical impact is (explained below) | Set by tester, confirmed in triage |
| **Priority** | How urgently it should be fixed (explained below) | Usually set by product owner or triage |
| **Attachments / evidence** | Screenshots, screen recording, logs, network trace, console errors | Highlight the problem area; hide personal data |
| **Reproducibility** | Can you make it happen every time? (Always, Sometimes, Once) | Honest reporting builds trust |
| **Frequency** | How often it occurs (for example 3 out of 10 attempts) | Helpful for intermittent issues |
| **Workaround** | Any way a user can still reach their goal | May lower the priority; helps support teams |
| **Linked requirement / test case** | IDs of the requirement and the test case that found it | Gives traceability |
| **Other** | Reporter, date, assignee, component, labels, related defects | Often filled by the tool automatically |

**Rules of thumb for writing:**

- **One defect per report.** If you found three problems, write three reports (and link them).
- **Be objective.** Describe facts. Avoid words like "terrible" or "stupid." Never write "the developer broke this."
- **Be reproducible.** Re-run your own steps before you submit them. If they do not reproduce the problem for you, they will not for anyone.
- **Be minimal.** Remove steps that are not needed to trigger the problem.
- **Do not diagnose.** Say what you saw, not what you think the code is doing wrong. You may add a hint ("might be related to the discount code") in a clearly marked comment.
- **Search first.** Check whether the defect is already logged.

#### BAD report example

> **Title:** Checkout not working
> **Description:** I tried to buy something and it did not work. Please fix ASAP. This is very bad.
> **Severity:** High
> **Attachment:** (none)

What is wrong with it? No steps, no data, no environment, no build, no expected or actual result, no evidence, vague title, emotional tone, and no way to know what "not working" means. The developer must start by asking five questions.

#### GOOD report example

> **Title:** Checkout - "Place Order" returns "Error 500" when shipping address contains an apostrophe
>
> **Description:** An order cannot be placed if the street name contains an apostrophe (e.g. "O'Connor Street"). Customers with such addresses are completely blocked from buying. Other addresses work.
>
> **Environment:** QA environment; Windows 11; Chrome 126; logged in as test user `qa.buyer01` (role: Customer)
>
> **Build:** 2.4.1-build.318
>
> **Steps to reproduce:**
> 1. Log in as `qa.buyer01`.
> 2. Add "Blue Notebook" (SKU NB-102) to the cart.
> 3. Click "Checkout".
> 4. In Shipping Address, enter Street = `12 O'Connor Street`, City = `Dublin`, Postcode = `D02 XY45`.
> 5. Choose "Standard delivery" and click "Place Order".
>
> **Expected result:** Order is placed; confirmation page "Thank you for your order" is shown with an order number (Requirement REQ-CHK-014).
>
> **Actual result:** Page displays "Something went wrong. Error 500" and no order is created. No order appears in My Orders.
>
> **Severity:** High (customers cannot complete a purchase for affected addresses)
> **Priority:** High (revenue impact; common in some regions)
>
> **Reproducibility:** Always (5 out of 5 attempts). Does not occur with `12 OConnor Street`.
>
> **Workaround:** Enter the street without the apostrophe.
>
> **Attachments:** `checkout-error-500.png`, `checkout-error.mp4`, browser console log `console.txt` (shows POST /api/orders returned 500).
>
> **Linked to:** Requirement REQ-CHK-014; Test case TC-CHK-031

The good report is longer, but it saves everyone time. The developer reproduces the problem in minutes, knows the impact, knows the workaround, and can easily trace it. Even the hint about the apostrophe was found by the tester by changing one variable at a time, which is a skill we practise below.

#### Full defect report template

Copy this into your notes or your tracker's description field.

```
DEFECT REPORT TEMPLATE
----------------------------------------------------------
Defect ID:            [assigned by the tool]
Title:                [Area] - [What goes wrong] when [condition]
Reported by / Date:   [name] / [YYYY-MM-DD]
Project / Component:  [e.g. Project 1 - Checkout]

DESCRIPTION
[1-3 sentences: what is wrong and who is affected]

ENVIRONMENT
  Test environment:   [QA / Staging / etc.]
  OS and version:     [e.g. Windows 11]
  Browser / device:   [e.g. Chrome 126 / iPhone 14, iOS 17]
  User account/role:  [e.g. qa.buyer01 / Customer]
  Build / version:    [e.g. 2.4.1-build.318]

PRECONDITIONS / TEST DATA
  [Anything that must be true before step 1]

STEPS TO REPRODUCE
  1.
  2.
  3.

EXPECTED RESULT
  [What should happen] (Requirement: [ID])

ACTUAL RESULT
  [What did happen, including exact messages]

SEVERITY:             [Critical / High / Medium / Low]
PRIORITY:             [Urgent / High / Medium / Low]
REPRODUCIBILITY:      [Always / Sometimes / Once]
FREQUENCY:            [e.g. 3 of 10 attempts]
WORKAROUND:           [Yes - describe / None]
DEFECT TYPE:          [Functional / UI / Performance / Security / ...]

EVIDENCE
  [Screenshots, video, logs, network trace file names]

TRACEABILITY
  Requirement ID:     [ ]
  Test case ID:       [ ]
  Related defects:    [ ]

ADDITIONAL NOTES
  [Observations, variations tried, suspected area (clearly marked as guess)]
----------------------------------------------------------
```

### 10. Severity versus priority

These two words are often mixed up, and a good tester separates them clearly.

- **Severity** describes **how serious the defect's impact is on the system or user**: how much it breaks. It is mainly a *technical and functional* measure. It is usually set by the tester and confirmed in triage.
- **Priority** describes **how soon the defect should be fixed**: the order of repair. It is a *business and scheduling* decision, usually set by the product owner or triage group, taking into account customer impact, deadlines, risk, and effort.

A simple way to remember: **severity is about damage; priority is about order.** In the hospital analogy, severity is how serious the injury is; priority is who gets treated first, which also depends on the queue, resources, and circumstances.

Typical severity levels (names differ between organizations):

| Severity | Meaning |
|---|---|
| Critical (Blocker) | System crashes, data is lost or corrupted, a security breach, or a core function is completely unusable with no workaround. Testing may be blocked. |
| High (Major) | A major function is broken or wrong, but the system as a whole still runs. A workaround may be hard. |
| Medium (Moderate) | A function misbehaves in a limited way, or has a reasonable workaround. |
| Low (Minor / Trivial) | Cosmetic issues, small typos, minor visual problems, with no effect on function. |

Typical priority levels:

| Priority | Meaning |
|---|---|
| Urgent / P1 | Fix immediately; drop other work; may require a hotfix. |
| High / P2 | Fix in the current release or sprint, before release. |
| Medium / P3 | Fix when capacity allows, likely this release or the next. |
| Low / P4 | Fix if time permits; can wait. |

#### The severity/priority 2x2 matrix

```
                          PRIORITY
                 Low (fix later)       High (fix soon)
              +---------------------+----------------------+
              |                     |                      |
    High      |  HIGH SEVERITY      |  HIGH SEVERITY       |
              |  LOW PRIORITY       |  HIGH PRIORITY       |
  S           |  Serious, but rare  |  Fix NOW             |
  E           |  or off the main    |  Core function       |
  V           |  path               |  broken for many     |
  E           |                     |                      |
  R           +---------------------+----------------------+
  I           |                     |                      |
  T   Low     |  LOW SEVERITY       |  LOW SEVERITY        |
  Y           |  LOW PRIORITY       |  HIGH PRIORITY       |
              |  Tiny and           |  Small flaw, but     |
              |  harmless           |  highly visible or   |
              |                     |  embarrassing        |
              +---------------------+----------------------+
```

#### Examples for each quadrant

**High severity, high priority (fix now)**

- Customers cannot log in at all after the latest release.
- Payment is taken twice for one order.
- The application crashes on start-up on the most popular browser.
- User passwords are stored or displayed in plain text.

**High severity, low priority**

- The application crashes when a user uploads a 2 GB profile photo, but the upload is limited to 5 MB by the UI and the case is nearly impossible to reach.
- A report export fails for the year 2099 date range, a date no user would ever select.
- A rarely used admin function crashes on a legacy browser that is no longer supported and is used by about 0.1 percent of users.
- A feature is broken in a module that will be retired next month.

**Low severity, high priority**

- The company name is misspelled on the home page, or the logo shows the wrong version, on the day of a major marketing launch.
- A legal disclaimer or required copyright text is missing from the footer before a regulatory audit.
- A typo in the "Pay Now" button label ("Pay Nwo") on the main checkout page: harmless to function, embarrassing, and trivially fast to fix.
- The brand color on the landing page is wrong in the week of a customer demo.

**Low severity, low priority**

- A button is 2 pixels out of alignment on a settings page that few people visit.
- A tooltip has a minor grammatical error on an admin-only screen.
- A rarely used field label is slightly inconsistent in capitalization.

Remember: severity is typically stable (the technical impact does not change), while priority can change with context (the same typo is low priority in March and high priority on launch day).

### 11. Defect categories and root cause categories

Classifying defects helps you spot patterns. There are two common ways to classify.

#### By type (what kind of problem is it?)

| Type | Description | Example in the Project 1 app |
|---|---|---|
| **Functional** | A feature does not behave as specified | Discount code is accepted but not applied |
| **UI / Visual** | Layout, alignment, colors, text, images | Text overlaps the "Add to Cart" button on mobile |
| **Performance** | Slow, unresponsive, or fails under load | Search takes 12 seconds to return results |
| **Security** | Weakness that could expose data or allow misuse | Changing an order number in the URL shows someone else's order |
| **Compatibility** | Works in one browser, device, or OS but not another | Checkout form does not submit in Safari |
| **Data** | Wrong, lost, duplicated, or corrupted data | Order total saved in the database differs from the one displayed |
| **Usability** | Hard or confusing to use | Error message "Invalid input" gives no hint which field is wrong |
| **Accessibility** | Hard to use for people with disabilities | Form fields have no labels for screen readers |

#### By root cause (why did it happen?)

Root cause categories are filled in by the developer or team after the fix, and they tell the team where the process leaks.

| Root cause category | Meaning |
|---|---|
| Requirements | Missing, ambiguous, or wrong requirement |
| Design | The solution design was flawed or incomplete |
| Coding | Logic error, wrong condition, typo in code |
| Data / Database | Incorrect data, migration, or schema issue |
| Configuration / Environment | Wrong settings, missing setup, infrastructure |
| Integration | Two components or systems do not work together properly |
| Third-party | A library or external service behaves unexpectedly |
| Test / Process | Wrong test, missed review, or poor process; or the defect was invalid |

If, say, 40 percent of defects in a release come from "Requirements," the best investment is not more testing at the end, but better requirements review at the start. This is exactly why Monday's early involvement of QE matters.

**A note on clusters.** You may notice that defects tend to bunch up in a few modules. That observation is a named testing principle, **defect clustering**, which we will study on Wednesday. For now, just notice it when you look at your defect lists.

### 12. Defect metrics: what the numbers tell us

Teams measure defects not to blame people but to learn about product quality and process health. Here are the beginner-level measures. Always remember that a number alone never tells the whole story; it tells you where to ask questions.

#### Defect age

**Defect age** is how long a defect has been open: the time between when it was logged and now (or when it was closed).

> Defect age = Closed date (or today) - Reported date

Old defects may mean they are hard, ignored, stuck waiting for a decision, or low priority. A dashboard of "defects older than 30 days" is a classic triage input.

#### Defect density

**Defect density** is the number of defects relative to the size of the product, so that large and small modules can be compared fairly.

> Defect density = Number of defects / Size of the software (for example thousand lines of code, called KLOC, or function points, or number of modules or pages)

#### Defect leakage

**Defect leakage** shows how many defects "leaked" past testing and were found after release (by customers or in production).

> Defect leakage % = (Defects found after release / (Defects found in testing + Defects found after release)) x 100

A closely related and widely used measure is **Defect Removal Efficiency (DRE)**, which is the other side of the same coin:

> DRE % = (Defects found before release / Total defects found before and after release) x 100
> DRE % = 100 - Defect leakage %

#### Other helpful measures

- **Open vs closed trend:** Are we closing defects faster than we find them? Rising "open" counts near release are a risk sign.
- **Defects by severity and by module:** Where is the pain?
- **Reopen rate:** Percentage of fixed defects that were reopened. A high rate suggests poor fixes or poor reports.
- **Rejected/duplicate rate:** A high rate may suggest weak reports or unclear requirements.

#### Worked example

The Project 1 team finishes a release. Facts gathered:

- The checkout module has 6,000 lines of code (6 KLOC); the search module has 2,000 lines (2 KLOC).
- Testing found 18 defects in checkout and 2 in search.
- After release, customers found 5 more defects (all counted as "found after release").
- One specific defect was reported on Monday 3 March and closed on Friday 7 March.

Calculations:

1. **Defect density, checkout:** 18 / 6 KLOC = **3.0 defects per KLOC.**
2. **Defect density, search:** 2 / 2 KLOC = **1.0 defect per KLOC.**
   Checkout has three times the density of search, a hint to examine the checkout code and tests more closely.
3. **Total found during testing:** 18 + 2 = 20.
4. **Defect leakage:** 5 / (20 + 5) x 100 = 5 / 25 x 100 = **20 percent.** One in five defects reached customers.
5. **DRE:** 20 / 25 x 100 = **80 percent** (which equals 100 - 20).
6. **Defect age of the one defect:** reported Monday 3 March, closed Friday 7 March, so **4 days** (or 5 working days if you count both end days; teams should agree on one convention).

**Interpretation:** An 80 percent DRE is a conversation starter. Was it a rushed release? Were the five leaked defects in untested areas? Did requirements miss something? The numbers prompt the question; the team investigates the answer.

**Cautions:** Never use defect counts to rank or punish individual testers or developers. Doing so leads to hidden bugs, argued severities, and fights over who "owns" a defect. Treat metrics as a mirror for the process, not a weapon.

### 13. Handling disagreements with developers professionally

Disagreements about defects are normal. A developer may say, "That's not a bug," or "That's low priority," or "I can't reproduce it." These conversations can be productive or poisonous, depending on how they are handled.

**Principles:**

1. **Attack the problem, not the person.** The defect is the shared enemy, not the developer.
2. **Lead with evidence.** Offer steps, a recording, logs, the requirement ID. Evidence turns opinion into fact.
3. **Check your own work first.** Re-run it on the latest build. Perhaps the developer is right.
4. **Check the source of truth.** Is the behavior in the requirement, acceptance criteria, or design? If it is ambiguous, ask the product owner. The product owner, not the tester or developer, settles what the business wants.
5. **Ask questions, do not accuse.** "Can we look at this together?" is better than "You broke it."
6. **Offer help.** Provide the data, the account, or a quick screen share so the developer can reproduce it.
7. **Separate severity from priority in the discussion.** Often the argument is really about "when," not "whether."
8. **Escalate calmly and last.** Use triage or the product owner for deadlocks. Do not go over someone's head without telling them.
9. **Accept decisions.** If triage decides to defer or reject, record your concern in the defect, and move on. Your job is to provide information; the decision belongs to the business.
10. **Say thank you.** A quick fix deserves recognition.

**Example conversation:**

> Developer: "Cannot reproduce. Works fine."
>
> Tester (poor reply): "You're wrong. It fails every time."
>
> Tester (better reply): "Thanks for trying. I just re-ran it on build 318 and recorded a short video, attached now. One thing that might differ: my test user has a saved address with an apostrophe. Could you try with `qa.buyer01`? Happy to hop on a call for five minutes if easier."

Notice the better reply is polite, specific, supplies evidence, and removes obstacles.

### 14. The prevention mindset and root cause analysis (intro)

Finding and fixing defects is necessary, but the best quality teams ask a deeper question: **"How did this get here, and how do we stop it happening again?"** This is the difference between **detection** (finding bugs) and **prevention** (stopping them from being created). The cost of fixing a defect generally rises the later it is found: a typo in a requirement costs minutes to correct on paper, but days if it is discovered in production after code, tests, and documentation have been built on it.

**Root cause analysis (RCA)** is a structured way of looking past the symptom to find the underlying reason. Two simple tools:

#### The 5 Whys

Keep asking "why?" (about five times, though the number is not magic) until you reach a cause you can act on.

Example: a customer received a wrong discount.

1. **Why** did the customer get a wrong discount? Because the discount was calculated on the price before tax instead of after.
2. **Why** was it calculated that way? Because the developer coded it from the old requirement document.
3. **Why** was the old document used? Because the updated requirement was posted in a chat message, not in the requirements tool.
4. **Why** was it only in chat? Because there is no rule that requirement changes must be updated in one place.
5. **Why** is there no rule? Because the team never agreed on a change-control step.

**Action:** Agree that all requirement changes are recorded in the requirements tool, and add a review step. The fix is a process change, not "tell the developer to be careful."

#### The fishbone (Ishikawa) diagram

A **fishbone diagram** helps a group brainstorm many possible causes, grouped by category. The problem is the "head" of the fish; the main bones are categories; smaller bones are specific causes.

```
  People                 Process                 Tools / Environment
    \                       \                          \
     \  new joiner,          \  no code review,         \  test data differs
      \ not trained           \ requirement change       \ from production
       \                       \ not communicated         \
        +----------------------+---------------------------+----------> PROBLEM:
       /                       /                           /           Wrong discount
      /  unclear acceptance   /  no test for tax           /            in production
     /   criteria            /   + discount mix            /
    /                       /                             /
  Requirements           Testing                        Code / Design
```

Use categories that fit your product. Common ones are People, Process, Tools, Environment, Requirements, Code, Data, and Testing. The diagram will not give the answer by itself, but it helps the team see where to look and prevents tunnel vision. Pair it with 5 Whys on the most likely branch.

**Typical prevention actions:** better requirement reviews, checklists, pair testing, code reviews, unit tests and automated checks, clearer acceptance criteria, shared test data, and training. We will return to prevention through the week.

### 15. Retesting and regression checks after a fix

When a defect reaches "Ready for Retest," the tester's job begins again with two distinct activities.

1. **Retesting (confirmation testing):** Repeat the *exact* steps that originally exposed the defect on the new build. The question is: **Is this specific defect gone?**
2. **Regression check:** Quickly test nearby features that the fix might have accidentally broken. The question is: **Did the fix break anything else?**

Practical checklist:

- Confirm you are testing the **build that contains the fix** (check the build number on the defect).
- Use the original environment and data where possible.
- Follow the original steps exactly. Then try a few variations (for example other addresses with apostrophes, a different browser).
- Check the area around the fix. If the checkout code was changed, quickly run the key checkout test cases, such as adding items, applying a coupon, paying with each method.
- Record the result in the defect: build number, what you tested, and the verdict.
- **Pass:** move to Verified/Closed. **Fail:** move to Reopened with evidence.

Regression testing is a large subject (selecting, automating, and prioritizing regression suites) and we will study it in depth on Friday. For today, remember the pairing: *retest the bug, regress around the fix.*

### 16. Tracing defects to test cases and requirements

**Traceability** means each defect can be linked back to the test case that found it and the requirement it violates, and forward to the fix and retest. We saw earlier today how requirements are linked to test cases; defects extend that chain.

```
 Requirement  <-->  Test Case  <-->  Test Execution  <-->  Defect  <-->  Fix (code change)  <-->  Retest
 REQ-CHK-014       TC-CHK-031        Run 12, Fail         BUG-207        PR #88, build 319        Run 14, Pass
```

Why it helps:

- **Impact analysis:** If a requirement changes, we see all linked tests and defects.
- **Coverage insight:** A requirement with many defects is a risk area; a requirement with no tests is a gap.
- **Better retesting:** The linked test case tells you exactly what to rerun.
- **Release decisions:** The release manager can see "all defects linked to critical requirements are closed."
- **Defects found outside test cases:** If you find a bug by exploring (not following a written test), create or update a test case afterwards so the bug is guarded against in future. This gives the defect a home in the test suite.

### 17. AI-assisted bug reporting (high level) and cautions

AI assistants can speed up defect reporting. At a high level, they can help you:

- **Turn rough notes into a structured report** using your template: fixing grammar, ordering the steps, separating expected from actual.
- **Suggest a clear title** from a long description.
- **Check completeness**: "What fields are missing from this report?"
- **Summarize** a long log or a thread of comments for a triage meeting.
- **Suggest possible duplicates** or related defects (some trackers have this built in).
- **Draft a polite reply** to a developer or a clarification question.
- **Propose possible categories or severity** as a starting point.

**Cautions (these matter):**

1. **You are still accountable.** The report carries your name. Read every word; AI can add steps you never did, invent error messages, or smooth over the details that matter.
2. **Never let AI invent facts.** Steps, data, build numbers, and results must come from what you actually observed. If you did not see it, it does not go in.
3. **Protect confidential data.** Do not paste real customer data, credentials, secrets, or proprietary code into tools that your organization has not approved. Follow company policy and remove personal information from screenshots and logs.
4. **Verify severity and priority yourself.** AI does not know your business context, deadlines, or customers. Treat its suggestions as drafts for discussion.
5. **Reproduce before you submit.** An AI-polished report with steps that do not actually reproduce the problem is worse than a rough one that does.
6. **Do not skip the thinking.** Understanding what a good defect looks like is exactly what lets you judge AI output. Learn the skill first; then use AI as an assistant, not a replacement.

A simple prompt pattern might be: "Here are my raw notes and the template below. Turn the notes into a report using the template. Do not add any information that is not in my notes. List any fields you could not fill so I can complete them." The last two sentences protect against invention.

---

## Examples

### Worked story: one bug through its whole lifecycle

Follow a single defect, **BUG-207**, through the Project 1 application. The team uses a detailed workflow. Dates are in one working week.

**The find (Monday).** While executing test case TC-CHK-031 ("Place order with a valid shipping address"), the tester, Priya, finds that an address containing an apostrophe causes "Error 500." She repeats it five times, tries a different address without an apostrophe (works), writes the report (like the good example above), attaches evidence, and submits.

| Day | State change | Who | What happened and comments |
|---|---|---|---|
| **Mon 09:30** | (none) -> **New** | Priya (tester) | Logged BUG-207: "Checkout - Place Order returns Error 500 when street contains an apostrophe." Severity High, suggested Priority High. Linked to REQ-CHK-014 and TC-CHK-031. Attached screenshot, video, console log. Comment: "Reproduced 5/5 on build 318. Works without the apostrophe." |
| **Mon 14:00** | New -> **Assigned** | Marcus (dev lead) in triage | Triage confirmed High severity. Product owner Dana set Priority High because customers in several target regions have apostrophes in street names. Assigned to developer Sam. Triage comment: "Fix in this sprint; target build 319." |
| **Mon 14:30** | Assigned -> **Open** | Sam (developer) | Sam accepted it. Comment: "Reproduced locally. Looks like input handling in the order service." |
| **Mon 15:00** | Open -> **In Progress** | Sam | Started investigating. |
| **Tue 11:00** | In Progress -> **Fixed** | Sam | Found that the apostrophe was breaking a database query because the value was not safely passed as a parameter. Changed the code to use parameterized queries. Added a unit test. Code reviewed and merged. Comment: "Root cause: coding (unsafe query construction). Fix in PR #88." |
| **Tue 16:00** | Fixed -> **Ready for Retest** | Build pipeline / Sam | Build 319 deployed to QA. Sam updated "Fixed in build: 2.4.1-build.319." |
| **Wed 09:15** | Ready for Retest -> **Reopened** | Priya | Retest of the original steps passed with `12 O'Connor Street`, but the same error appears for an address containing a double quote (`The "Old" Mill`). Comment: "Original case fixed in 319, but the same error for double quotes. Evidence attached. Also quick regression of checkout is otherwise clean." Because it is the same underlying problem, she reopened the defect with a clear comment rather than raising a new one. |
| **Wed 09:45** | Reopened -> **Assigned** | Marcus | Returned to Sam with the new evidence. Note on the reopen rate: one reopen is normal and healthy; the retest caught an incomplete fix. |
| **Wed 13:00** | Assigned -> Open -> In Progress -> **Fixed** | Sam | Fixed the remaining input path, expanded the unit tests to cover quotes, ampersands, and non-English characters. Comment: "Fix in PR #91." |
| **Wed 15:30** | Fixed -> **Ready for Retest** | Build pipeline | Build 320 deployed to QA. |
| **Thu 10:00** | Ready for Retest -> **Verified** | Priya | Retested original steps, the double quote case, ampersand, and an address with an accent. All pass. Ran 12 key checkout regression test cases: all pass. Comment: "Verified on build 320." |
| **Fri 11:00** | Verified -> **Closed** | Marcus (release manager sign-off at release) | Included in release 2.4.1. Closed with resolution "Fixed." Defect age: 5 calendar days from Mon to Fri. |

**What the story shows:**

- Every move had an owner and a reason.
- Triage turned a tester's suggestion into an agreed priority.
- The developer recorded the **root cause category** (coding), which later feeds metrics and prevention (for example, a code review checklist item about parameterized queries).
- The retest found an **incomplete fix**, and the Reopened state worked exactly as intended.
- The final closure was by the tester's verification, not the developer's claim.

### Example: a defect that is not accepted

Another report, BUG-212, says "Search is case sensitive: searching 'notebook' returns nothing but 'Notebook' works." The developer finds that the requirement REQ-SRC-003 states that search must be case insensitive and cannot reproduce it. After comparing environments, the team discovers the tester was on an older build. The defect moves **New -> Not a Bug / Cannot Reproduce** with the comment "Not reproducible on build 318 or later; was present in build 301. Please recheck on the latest build." Priya retests on the latest build, confirms, and the defect is closed. This is a healthy "no" with a recorded reason, and it shows why build number is a mandatory field.

### Example: a deferred defect

BUG-220: on the "My Account" page, a rarely used "Download invoices as ZIP" button is slightly slow when a user has more than 200 invoices. Severity Low-Medium, workaround exists (download invoices one by one), only a few users affected. Triage defers it: **New -> Deferred**, with a note "Review in next release planning; PO Dana to decide on inclusion." Deferred does not mean forgotten: it has a review date.

---

## Practice Section A: Write the Bug Report (five scenarios)

For each scenario, write a defect report using the template in this lesson. Fill in every field you can from the information given, mark anything you would have to find out as "to confirm," and set sensible severity and priority. Sample answers are at the end of this lesson. Try each one yourself first.

**Scenario 1: Login lockout.**
Requirement REQ-LOG-005: "After 5 consecutive failed login attempts, the account is locked for 15 minutes and the user sees the message 'Your account is locked. Try again in 15 minutes.'" You enter the wrong password 5 times on build 2.4.1-build.320 (Chrome 126, Windows 11, QA environment). Nothing happens; you can keep trying wrong passwords, 12 times in a row. The same happened the second time you tried with a different test account.

**Scenario 2: Cart total.**
Requirement REQ-CRT-009: "Cart total equals the sum of item prices times quantities, with no discount unless a coupon is applied." You add two units of "Blue Notebook" at 12.50 each and one "Pen Set" at 8.00. You calculate 2 x 12.50 + 8.00 = 33.00, but the cart shows 45.50. When you remove the "Pen Set," the total correctly shows 25.00; when you add it back, the total again shows 45.50. Build 320, Firefox 127, macOS, QA environment, logged in as `qa.buyer02`.

**Scenario 3: Mobile layout.**
On an iPhone 14 (iOS 17, Safari), in portrait orientation, the product detail page of "Blue Notebook" shows the "Add to Cart" button partially hidden behind the footer, so only the top half can be tapped. In landscape orientation, it displays normally. Desktop browsers are fine. Build 320, QA environment. No requirement states mobile layout in detail, but REQ-GEN-002 says "The site must be usable on current mobile devices."

**Scenario 4: Slow search.**
Requirement REQ-SRC-006: "Search results appear within 3 seconds for catalogs of up to 10,000 products." On the QA environment with the 10,000-product test catalog, searching for "pen" takes between 9 and 14 seconds in 6 of 10 attempts; the other 4 attempts return within 2 seconds. Build 320, Chrome 126, wired network. Searching for "zebra" (few matches) is consistently fast.

**Scenario 5: Order of another user.**
You are logged in as `qa.buyer01` and view your order at `/orders/10045`. You change the number in the address bar to `/orders/10046`, an order belonging to `qa.buyer02`. The page displays the other user's name, address, and items. Build 320, QA environment, Chrome 126.

---

## Practice Section B: Classify Severity and Priority

For each item below, assign a severity (Critical, High, Medium, Low) and a priority (Urgent, High, Medium, Low), and write one sentence of justification. Answers follow at the end.

1. The home page shows "Welcome to Project 1 Shopp" (the final letters are cut off) the day before a press demo.
2. Customers' saved credit card numbers are visible in the page source of the account page.
3. A "Print receipt" button prints with the wrong font on one older browser version used by 0.2 percent of visitors.
4. The site crashes every time the user clicks "Apply Coupon," and no discount can be used. A marketing campaign with coupons starts tomorrow.
5. The "Contact us" page has a spelling mistake in the third paragraph.
6. The admin report for "Orders by year" fails if the user chooses the year 1900.
7. After a new release, search returns results from the previous catalog (stale data) for about 5 minutes after products are updated.
8. The password reset email is sent correctly, but its link expires after 1 minute instead of the required 60 minutes.

---

## Try It: Project 1 Activity

**Goal:** Practise raising, classifying, and tracing defects for the Project 1 application, and prepare for the Jira work later today.

**Part 1: Find and log three defects (30 minutes).**
Using your Project 1 application (or the test cases you have drafted today), pick three areas, for example login, search, and checkout. For each, either execute a test and find a real discrepancy, or, if the application has none that you can find, choose one deliberate check from your test plan and write the report for a plausible defect clearly labelled "practice example." Write all three reports using the full template.

**Part 2: Classify (10 minutes).**
For each of your three defects, record the defect type (functional, UI, performance, security, compatibility, data, usability), severity, priority, and a likely root cause category. Write one sentence about why the severity and priority differ (if they do).

**Part 3: Trace (10 minutes).**
For each defect, add the test case ID and requirement ID it relates to. If no test case exists, write a short new test case to cover it.

**Part 4: Draw the journey (10 minutes).**
Choose one defect and sketch the path it would follow in a 5-state workflow and in the detailed workflow from this lesson. Mark who moves it at each step.

**Part 5: Peer review and triage (20 minutes).**
Swap reports with a partner. Each of you acts as developer for the other: try to reproduce by reading only the written steps. List every question you had to ask. Then hold a two-minute mock triage for each defect: accept, reject, defer, or request more information. Revise your reports based on the feedback.

**Part 6: Metrics (10 minutes).**
Suppose your team logged 24 defects in the product catalog module (4 KLOC), and 6 more were found by customers after release. Calculate defect density, defect leakage, and DRE. (Answers: density 6 per KLOC counting testing defects; leakage 6/30 = 20 percent; DRE 80 percent.)

**Optional AI step:** Take one rough note about a defect and ask an AI assistant to format it into the template without adding any new facts. Compare the result with your own report. What did it get right? What did it invent or leave out?

**Deliverable:** Save your three reports, classification table, traceability links, and workflow sketch in your Project 1 folder. You will reuse them when you create issues and workflows in Jira later today.

---

## Knowledge Check

Try to answer each question before reading the answers.

1. In your own words, what is a defect?
2. Which role normally moves a defect from "Ready for Retest" to "Verified/Closed"?
3. A developer moves a defect from "In Progress" to "Fixed." Is the defect now resolved? Explain.
4. What is the difference between "Rejected" and "Deferred"?
5. What is the difference between "Cannot Reproduce" and "Not a Bug"?
6. Who normally has the final say on priority, and why?
7. Give one example of a high severity, low priority defect and one of a low severity, high priority defect.
8. Name five fields that every good defect report should contain.
9. Why is the build or version number a mandatory field?
10. A defect was found in testing 20 times and in production 5 times. What is the defect leakage?
11. A module has 12 defects and 3 KLOC. What is its defect density?
12. Name two purposes of a defect triage meeting.
13. What is the difference between retesting and a regression check?
14. In a 5 Whys analysis, what kind of answer are you aiming for at the end?
15. Give two cautions when using AI to write bug reports.
16. A defect has been reopened three times. What might that suggest, and what should the team do?
17. What does a "Won't Fix" decision require?
18. A tester finds a bug while exploring with no written test. What should they do afterwards to maintain traceability?

### Knowledge Check Answers

1. A defect (bug) is a flaw in a work product, such as software, requirements, or design, that makes it behave differently from what it should, based on requirements, design, or reasonable expectations.
2. The tester (usually the original reporter or another tester) after confirming the fix works and a regression check is clean. Developers fix; testers verify.
3. No. "Fixed" means the developer believes it is resolved. It is only truly resolved once it has been retested and verified on a build containing the fix.
4. Rejected means the report is judged invalid (correct behavior, misunderstanding, out of scope). Deferred means the defect is valid but its fix is postponed to a later release.
5. Not a Bug means the behavior is intended by the requirements or design. Cannot Reproduce means the problem could not be recreated by following the steps, so its validity is undetermined. The reporter can supply more information to try again.
6. The product owner (or the triage group acting for the business), because priority is a business and scheduling decision that depends on customers, deadlines, and risk. Testers give input; severity is the technical measure.
7. High severity, low priority: a crash that can only be triggered by an unrealistic action, such as an extreme date, or in a module that is about to be retired. Low severity, high priority: a misspelled company name on the home page just before a launch demo.
8. Any five of: title, description, environment, build/version, steps to reproduce, expected result, actual result, severity, priority, evidence, reproducibility, frequency, workaround, linked requirement or test case.
9. Because behavior changes from build to build. The version tells developers where to reproduce the problem and tells testers where to retest, and it prevents "works on my machine" misunderstandings.
10. 5 / (20 + 5) x 100 = 20 percent.
11. 12 / 3 = 4 defects per KLOC.
12. Any two of: confirm validity, agree severity and priority, assign owners, remove duplicates, decide fix now or defer or decline, keep the backlog healthy.
13. Retesting repeats the original failing steps to confirm that specific defect is fixed. A regression check tests surrounding functionality to confirm the fix did not break anything else.
14. A root cause you can act on, usually a process or system weakness, rather than blaming a person. The result should lead to a preventive action.
15. Any two of: you remain accountable for the report; do not let AI invent facts or steps; do not paste confidential or personal data into unapproved tools; verify severity and priority yourself; reproduce before submitting.
16. It suggests poor fixes, unclear reports, an unclear requirement, or unstable code. The team should discuss it in triage, perform root cause analysis, and possibly pair the developer and tester to agree on the exact expected behavior and add stronger tests.
17. A documented business decision with a recorded reason, usually made by the product owner or triage group, not by a developer alone.
18. Write a test case (or update an existing one) that covers the scenario, and link the defect and the requirement to it.

---

## Sample Answers

### Sample answers for Practice Section A (bug reports)

**Scenario 1 sample report**

- **Title:** Login - Account is not locked after 5 consecutive failed login attempts
- **Description:** Entering a wrong password repeatedly never locks the account and no lockout message appears, which weakens protection against password guessing.
- **Environment:** QA; Windows 11; Chrome 126; two test accounts (names to be recorded)
- **Build:** 2.4.1-build.320
- **Steps:** 1. Open the login page. 2. Enter a valid username and an incorrect password. 3. Click "Log in." 4. Repeat steps 2 and 3 at least 12 times.
- **Expected:** After the 5th failed attempt, the account is locked for 15 minutes and the message "Your account is locked. Try again in 15 minutes." is shown (REQ-LOG-005).
- **Actual:** No lock; the standard "Invalid username or password" message appears on all 12 attempts, and login with the correct password would still work (to confirm and add).
- **Severity:** High (security control missing). **Priority:** High (should be fixed before release).
- **Reproducibility:** Always (2 of 2 accounts). **Workaround:** None for the user; the control is missing.
- **Type:** Security / Functional. **Evidence:** Screenshot of the 12th attempt, test log. **Linked:** REQ-LOG-005; test case ID to be confirmed.

**Scenario 2 sample report**

- **Title:** Cart - Total shows 45.50 instead of 33.00 when cart contains 2 Blue Notebooks and 1 Pen Set
- **Description:** The cart total is overstated by 12.50 when both products are present; the total is right with only the notebooks.
- **Environment:** QA; macOS; Firefox 127; user `qa.buyer02`
- **Build:** 320
- **Steps:** 1. Log in as `qa.buyer02` with an empty cart. 2. Add "Blue Notebook" (12.50) and set quantity to 2. 3. Add "Pen Set" (8.00), quantity 1. 4. Open the cart and read the total. 5. Remove the Pen Set and read the total again; add it back and read again.
- **Expected:** 33.00 (2 x 12.50 + 8.00), no coupon applied (REQ-CRT-009).
- **Actual:** 45.50 with both items; 25.00 with only notebooks (correct).
- **Observation:** The difference, 12.50, equals the price of one notebook, suggesting one extra notebook is counted when the Pen Set is present (marked as a guess, not a diagnosis).
- **Severity:** High (incorrect money amounts). **Priority:** High (customers would be overcharged).
- **Reproducibility:** Always (to be confirmed with count). **Workaround:** None known.
- **Type:** Functional / Data. **Evidence:** Screenshots of the cart in both states. **Linked:** REQ-CRT-009.

Notice that the arithmetic is shown in the report (25.00 + 8.00 = 33.00), so the developer can see the expected value is not an opinion.

**Scenario 3 sample report**

- **Title:** Product detail (mobile portrait) - "Add to Cart" button partly hidden behind footer on iPhone 14 Safari
- **Description:** In portrait orientation, only the top half of the button is tappable because the footer overlaps it. Landscape and desktop are fine.
- **Environment:** QA; iPhone 14, iOS 17, Safari; portrait
- **Build:** 320
- **Steps:** 1. Open the site on iPhone 14 in portrait. 2. Open "Blue Notebook" product detail. 3. Scroll to the Add to Cart button.
- **Expected:** The full button is visible and tappable (REQ-GEN-002, usable on current mobile devices).
- **Actual:** Lower half of the button is covered by the footer; tapping the covered part does nothing (to confirm).
- **Severity:** Medium (purchase is still possible by tapping the visible part, or rotating the phone). **Priority:** High if mobile traffic is substantial; to be confirmed in triage with the product owner.
- **Reproducibility:** Always in portrait. **Workaround:** Tap the upper half or rotate the device.
- **Type:** UI / Compatibility. **Evidence:** Screenshot in portrait and landscape. **Other devices:** To be checked (other iPhones, Android).

**Scenario 4 sample report**

- **Title:** Search - Query "pen" takes 9-14 seconds in 6 of 10 attempts (requirement is 3 seconds)
- **Description:** Search response time is intermittently far above the requirement with the 10,000-product catalog; searching for "zebra" is consistently fast.
- **Environment:** QA; 10,000-product test catalog; Chrome 126; wired network
- **Build:** 320
- **Steps:** 1. Open the search box. 2. Enter "pen" and press Enter. 3. Record the time until results appear (stopwatch or developer tools network timing). 4. Repeat 10 times.
- **Expected:** Results within 3 seconds (REQ-SRC-006).
- **Actual:** 6 of 10 attempts took 9-14 seconds; 4 of 10 under 2 seconds.
- **Severity:** Medium-High (feature works but misses a performance requirement). **Priority:** Medium (agree in triage).
- **Reproducibility:** Sometimes (60 percent). **Frequency:** 6 of 10.
- **Type:** Performance. **Evidence:** Table of 10 timings and network trace. **Note:** Broad query (many matches) is slow; narrow query is fast.

**Scenario 5 sample report**

- **Title:** Orders - Logged-in user can view another user's order by changing the order number in the URL
- **Description:** Visiting `/orders/10046` while logged in as `qa.buyer01` shows `qa.buyer02`'s name, address, and items, exposing personal data.
- **Environment:** QA; Chrome 126; logged in as `qa.buyer01`
- **Build:** 320
- **Steps:** 1. Log in as `qa.buyer01`. 2. Open My Orders and click order 10045 (URL `/orders/10045`). 3. Change the URL to `/orders/10046` and press Enter.
- **Expected:** Access denied or "Order not found," because the order belongs to another user.
- **Actual:** Full details of qa.buyer02's order are displayed.
- **Severity:** Critical (data exposure; security). **Priority:** Urgent (must be fixed before any release; report privately if your organization requires restricted visibility for security defects).
- **Reproducibility:** Always. **Workaround:** None.
- **Type:** Security. **Evidence:** Two screenshots, with personal data masked if real. **Linked:** Requirement for order access control (ID to confirm).

### Sample answers for Practice Section B (classify)

| # | Severity | Priority | Justification |
|---|---|---|---|
| 1 | Low | High | Cosmetic, but highly visible the day before a press demo, and trivial to fix. |
| 2 | Critical | Urgent | Exposure of sensitive payment data is a serious security and legal risk. |
| 3 | Low | Low | Minor visual issue on a rarely used browser; negligible impact. |
| 4 | High (or Critical, since a core feature fails completely) | Urgent | Feature crashes completely, and the marketing campaign starts tomorrow. |
| 5 | Low | Low | A spelling mistake with no functional impact; fix with the next content update. |
| 6 | Low-Medium | Low | Fails only for an unrealistic input; an input validation message would be nice, but few will ever see it. |
| 7 | Medium | Medium | Stale data for 5 minutes is misleading but temporary; priority depends on how often products change. |
| 8 | High | High | Users cannot realistically use the reset link; this breaks the account recovery requirement, though a retry is possible. |

Your answers may differ slightly. What matters is the reasoning: severity explains the damage; priority explains the order and urgency in the business context.

---

## Key Takeaways

- A **defect (bug)** is a flaw that makes something behave differently from what it should. The formal difference between error, defect, and failure comes on Wednesday.
- A **defect lifecycle** gives every defect a visible state, a named owner, and a defined next step. It is like package tracking or a hospital patient journey.
- The main path is **New -> Assigned -> Open -> In Progress -> Fixed -> Ready for Retest -> Verified/Closed**, with side exits for **Rejected, Duplicate, Not a Bug / Cannot Reproduce, Deferred, Won't Fix,** and a loop back via **Reopened**.
- Developers fix; **testers verify**. "Fixed" is not "done" until it is retested.
- Every "not going to fix" outcome needs a **recorded reason**.
- Workflows vary: a simple 5-state flow suits small agile teams; a detailed 12-state flow suits large or regulated ones. Learn to map names to core ideas.
- **Triage meetings** turn defect lists into decisions: accept, assign, defer, reject, or ask for more information.
- A great report is **specific, reproducible, objective, minimal, and evidence-backed**. One defect per report, with build number, environment, steps, expected versus actual, and links to requirement and test case.
- **Severity is about damage; priority is about order.** They often differ, and priority can change with context.
- Classify defects by **type** and **root cause** to see patterns. Clusters of defects are a topic for Wednesday.
- **Metrics** (defect age, density, leakage, DRE, reopen rate) help us ask better questions. They are for improving the process, not for blaming people.
- Handle disagreements with **evidence, respect, and the product owner** as the source of truth on business intent.
- Aim for **prevention**: ask why, use 5 Whys and fishbone diagrams, and fix the process, not only the product.
- After a fix, **retest the bug and regress around it**; full regression comes on Friday.
- **Traceability** connects requirement, test case, defect, fix, and retest.
- **AI can help draft** reports, but you remain accountable: never invent facts, protect confidential data, and verify severity and priority yourself.

---

## Additional Resources

- **ISTQB Glossary** (official definitions of testing terms, including defect, severity, priority, and defect report): https://glossary.istqb.org/
- **Guru99: Defect / Bug Life Cycle in Software Testing** (a beginner-friendly walkthrough of the states and flow): https://www.guru99.com/defect-life-cycle.html
- **Atlassian: Bug Tracking with Jira** (an overview of tracking bugs in a tool, a helpful preview for the Jira lessons later today): https://www.atlassian.com/software/jira/bug-tracking

Take a few minutes after class to compare how these sources name the states and notice how the vocabulary differs while the ideas stay the same.
