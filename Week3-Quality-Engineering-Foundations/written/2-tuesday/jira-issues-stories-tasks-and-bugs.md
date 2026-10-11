# Jira Issues, Stories, Tasks and Bugs

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain what a Jira **issue** is and why it is the basic unit of work in Jira.
- Describe the default issue type hierarchy (Epic, Story/Task/Bug, Sub-task) and explain how team-managed and company-managed projects differ.
- Decide when to use an Epic, a Story, a Task, a Bug or a Sub-task, and write each one well.
- Identify and use the key issue fields: summary, description, issue type, priority, assignee, reporter, labels, components, versions, environment, sprint, estimates, attachments, links, due date and custom fields.
- Create issues in several ways: the Create button, quick create on the backlog or board, templates, and a first look at bulk creation by CSV import.
- Write a user story with acceptance criteria in both Given/When/Then and checklist form, and tell a good story from a poor one.
- Write a high-quality bug in Jira by mapping each field of the defect report (from earlier today) onto Jira fields, using Jira description formatting.
- Link issues with blocks / is blocked by, relates to, duplicates and tests / is tested by, and connect bugs to the stories they affect.
- Use comments, mentions, watchers, attachments and issue history to collaborate.
- Distinguish priority from severity, labels from components, and estimate work with story points; split large stories into thin vertical slices.
- Describe how a Quality Engineer (QE) tracks testing work in Jira, even without a test management plugin.
- Write and explain 10-12 beginner JQL queries for issues, stories and bugs.
- Bulk edit, clone and move issues, follow good hygiene and naming conventions, and avoid common mistakes.
- Describe, cautiously, the AI features that Jira may offer.
- Complete a hands-on exercise: create an epic, four stories, two tasks and three bugs for Project 1 - QE Foundations.

---

## Why This Matters

Yesterday you met Jira as a tool: its screens, its backlog, its boards and a little JQL. Earlier today you learned how to analyse requirements, plan and execute tests, and move a defect through its lifecycle. This lesson is where those two worlds meet. Everything you learned about requirements, test cases and defect reports now has to live somewhere that a whole team can see, search, discuss and track. In most software teams, that place is Jira, and the thing you put into Jira is called an **issue**.

Consider what a Quality Engineer actually does all day:

- You read a **story** to check that it is testable before development starts.
- You write or review **acceptance criteria** so everyone agrees on what "done" means.
- You log **bugs** that developers can reproduce in minutes instead of hours.
- You link a bug back to the story it breaks, so the product owner sees the real risk.
- You search with JQL to answer questions such as "Which critical bugs are still open in this sprint?"

If your issues are vague, duplicated, badly linked or missing key fields, the team loses time, trust and visibility. If your issues are clear and well structured, the team moves faster, and your testing work becomes visible and valued. A well-written Jira issue is one of the cheapest quality improvements any team can make.

As an AI-enabled Test Automation Engineer, you will also use these same issues later as the input for automated tests and AI-assisted test design. An AI tool can only generate useful tests from a story with clear acceptance criteria; it cannot rescue a story that says "make login better." Good issue writing is a foundation skill for everything that follows.

---

## The Concept

### 1. The Issue: The Unit of Work

Imagine a wall covered in **index cards**. Each card describes one thing that someone needs to do or fix: "Build the registration form," "The login button does nothing on Safari," "Set up the test environment." The cards are colour coded, they have names written on them, and they are pinned in columns that show progress. If you want to know what is happening on the project, you look at the wall.

Jira is that wall, and the index cards are **issues**.

An **issue** is a single trackable item of work in Jira. It might be a feature to build, a defect to fix, a chore to complete, or a large goal that groups many smaller items. Every issue has:

- A unique **issue key** made of the project key, a dash and a number, for example `QEF-12`. The project key (here `QEF`, short for "QE Foundations") is set when the project is created. The key never changes and is how people refer to the work: "Have you looked at QEF-12?"
- An **issue type** that tells you what kind of work it is.
- A set of **fields** that hold details such as summary, description, priority and assignee.
- A **status** that shows where it is in the workflow (for example To Do, In Progress, Done). Workflows and statuses are covered in the next lesson, so for now simply notice that every issue has one.
- A **history** that records every change and a **comment** area for conversation.

> Note on terminology: In everyday speech people say "ticket," "card," "story" or "bug" for any issue. Strictly, "issue" is the umbrella word, and "story" or "bug" is a specific **issue type**.

Why do we put everything into issues rather than a spreadsheet or email? Because an issue is **searchable** (JQL), **linkable** (to other issues), **traceable** (history shows who changed what and when), **assignable** (one clear owner), and **reportable** (boards, charts and dashboards read from issues). Those four properties are what make Jira useful.

### 2. The Issue Type Hierarchy

Issue types are arranged in levels, like a family tree, so that big goals break down into smaller pieces of work.

**The default hierarchy**

```
Epic                      (a large body of work, a theme or a feature area)
  |- Story                (a user-facing piece of value)
  |- Task                 (a piece of work that is not a user-facing feature)
  |- Bug                  (a defect to fix)
        |- Sub-task       (a small step within a story, task or bug)
```

In words: an **Epic** contains **Stories, Tasks and Bugs**, and each of those can contain **Sub-tasks**. Sub-tasks are the lowest level and cannot have children of their own.

You can picture this as a filing system:

| Level | Think of it as | Typical size |
|---|---|---|
| Epic | A folder or a chapter of a book | Weeks to months |
| Story / Task / Bug | A document inside the folder | Hours to a few days (fits in one sprint) |
| Sub-task | A checklist line on the document | Minutes to hours |

**Newer hierarchy variations.** Atlassian has been evolving the hierarchy, and you may see differences depending on your site and plan:

- **Levels above Epic.** Higher plans offer extra levels (often named things like Initiative, Theme or Portfolio-level items) so that several Epics can roll up under a larger business goal. Jira Premium and related planning tools are where this commonly appears.
- **Renamed levels.** Some Jira versions and plans label the levels by number: Level 1 is Epic, Level 0 is Story/Task/Bug, and Level -1 is Sub-task. Newer interfaces may show "parent" and "child" work items instead of "epic link" and "sub-task."
- **Work item wording.** Atlassian has been moving toward calling issues **work items** in the interface and documentation. They are the same thing. If your screen says "Create work item" rather than "Create issue," do not worry; the concept is identical.
- **Parent field.** Older projects used a special "Epic Link" field to connect a story to an Epic. Newer projects use the general **Parent** field. The result is the same: the story belongs to the Epic.

Because Atlassian updates its interface often, **menu names and layouts in this lesson may differ slightly from what you see.** Focus on the ideas; the buttons will be easy to find once you understand what they are for.

**Team-managed vs company-managed projects.** When you create a Jira Software project you choose one of two styles:

| Aspect | Team-managed (formerly "next-gen") | Company-managed (formerly "classic") |
|---|---|---|
| Who controls the setup | The team that owns the project | Jira administrators for the whole site |
| Issue types and fields | Configured inside this one project only | Shared schemes across many projects |
| Setup complexity | Simple and quick | More powerful, more to configure |
| Best for | Small teams that want to move fast | Larger organisations needing consistency |
| Effect on you | Your project may have custom issue types the team added | Issue types and fields are standard across the company |

For this course, assume the default types (Epic, Story, Task, Bug, Sub-task). Your practice project may be either style. In a team-managed project you can add or rename issue types yourself; in a company-managed project an administrator does it. Check with your instructor if a type you expect is missing.

### 3. Each Issue Type in Depth

#### 3.1 Epic

**What it is.** An Epic is a large body of work that is too big to finish in one sprint and that you break into smaller issues. It represents a feature area, a theme or a business goal.

**When to use it.** Use an Epic when you can describe a coherent goal that will need several stories to achieve, such as "User Account Management" or "Checkout and Payments." A good test: can you picture 4 to 15 child issues underneath it?

**How to write it.**

- **Summary:** a short noun phrase naming the goal, for example "User Account Management".
- **Description:** explain the goal, the business reason, who benefits, what is in scope and what is out of scope.
- **Do not** put a single small piece of work in an Epic of its own. An Epic with one child is just a story wearing a hat.
- **Do not** use an Epic as a bucket for unrelated leftovers (for example "Misc" or "Sprint 4 stuff"). Such Epics become useless for tracking.

**Example (Project 1):**

> **Summary:** User Account Management
> **Description:** Allow visitors to create an account, sign in securely and recover access if they forget their password. This reduces support requests and is a prerequisite for personalised features. **In scope:** registration, login, password reset. **Out of scope:** social login, two-factor authentication (future epic).

#### 3.2 Story (User Story)

**What it is.** A **user story** is a short description of a feature written from the point of view of the person who wants it. It captures *who* needs something, *what* they need and *why*. It is deliberately small and conversational: the story is a promise to have a conversation, not a full specification.

**When to use it.** Use a Story for a piece of work that delivers visible value to a user and can be completed within one sprint.

**The user story format.**

```
As a <type of user>,
I want <some goal or capability>,
so that <benefit or reason>.
```

Each part matters:

- **As a** identifies the user (a "registered customer," an "administrator," not just "a user" if you can be more specific).
- **I want** describes the capability, not the technical solution.
- **So that** explains the value. If you cannot write the "so that," you may not understand why the work matters.

**Acceptance criteria.** **Acceptance criteria (AC)** are the specific, testable conditions a story must meet to be accepted. They define the boundaries of the story and are the main source of test cases for a QE. Good acceptance criteria are:

- **Specific:** exact values, messages and behaviours.
- **Testable:** a tester could say clearly "pass" or "fail."
- **Independent of implementation:** they describe what, not how.
- **Cover the unhappy paths too:** invalid input, errors, edge cases.

We will practise writing them in two forms (Given/When/Then and checklist) in section 7.

**Story points.** A **story point** is a unit used to estimate the relative size or effort of a story. It is not hours or days. A story of 5 points is roughly "bigger than a 3 and smaller than an 8." Points combine effort, complexity and uncertainty. See section 12.

**Definition of Done (DoD).** The **Definition of Done** is a shared checklist that applies to *every* story, agreed by the whole team. It is different from acceptance criteria, which belong to one story. A sample DoD:

- Code is reviewed and merged.
- Acceptance criteria are met and verified by QE.
- Unit and relevant automated tests pass.
- No open critical or high bugs are linked to the story.
- Documentation or help text is updated where needed.

You can remember it this way: **acceptance criteria answer "Did we build the right thing?" for this story; the Definition of Done answers "Did we finish it properly?" for all stories.**

The Definition of Done is often stored in the team's working agreement (a wiki page) rather than inside each issue, though some teams paste a link to it in the story template.

#### 3.3 Task

**What it is.** A **Task** is a piece of work that needs doing but is not a user-facing feature and is not a defect. Tasks are the "chores" and technical to-dos of a project.

**When to use it.** Use a Task for things like "Set up the test environment," "Prepare test data for registration," "Update the README," or "Configure the CI job." A good question to ask: *would a user notice this work directly as a new capability?* If no, it is probably a Task.

**How to write it.** State the action clearly with a verb: "Create...," "Configure...," "Document...". Add a short description of the outcome and a "how will we know it is finished" line. Tasks should still have an owner and ideally an estimate.

**Example:**

> **Summary:** Prepare test data set for registration testing
> **Description:** Create 10 valid and 10 invalid email/password combinations in the shared test data sheet, including boundary lengths and special characters. **Done when:** the sheet is saved in the team folder and linked here.

#### 3.4 Bug

**What it is.** A **Bug** is a defect: a place where the software behaves differently from what was expected or required. You learned the full defect lifecycle earlier today; a Bug issue is how a defect is recorded and tracked in Jira.

**When to use it.** Use a Bug when something that was supposed to work does not work as specified. If the behaviour is working as designed but the design is wrong or missing, that is usually a new Story or a requirement question, not a Bug. Agree on this boundary with your team early.

**How to write it.** The summary names the problem; the description gives environment, steps to reproduce, expected result and actual result, with evidence attached. Section 8 shows this in detail with a complete worked example.

#### 3.5 Sub-task

**What it is.** A **Sub-task** is a smaller piece of work that belongs to a parent issue (a Story, Task or Bug). It breaks the parent down into steps that can be assigned separately.

**When to use it.** Use sub-tasks when different people or different skills handle parts of the same story, or when you want visible, small, trackable steps. For example, a story may have sub-tasks "Implement registration form," "Write API tests," and "Perform exploratory testing." Sub-tasks cannot exist on their own; they always need a parent.

**Caution.** Too many sub-tasks create clutter. If a sub-task is a whole day or more of work with its own acceptance criteria, it probably should be a story.

#### 3.6 Spike and Improvement (brief mention)

You may see two other issue types in some projects, either built in or added by a team:

- **Spike:** a short, time-boxed investigation to answer a question or reduce uncertainty, such as "Spike: evaluate options for email verification service (max 1 day)." The output is knowledge or a recommendation, not shipped functionality.
- **Improvement:** an enhancement to existing functionality. Some older templates include it; many teams simply use Story or Task for this.

If your project does not have these types, you can use a Task with a label such as `spike`.

#### Summary Table of Issue Types

| Issue type | Purpose | Typical size | Has parent? | Example (Project 1) |
|---|---|---|---|---|
| Epic | Big goal or feature area | Many sprints | No (or a higher level on some plans) | User Account Management |
| Story | User-facing value | Fits in a sprint | Epic | User can register with email |
| Task | Non-feature work | Hours to days | Epic (optional) | Prepare test data for registration |
| Bug | A defect | Hours to days | Epic (optional) | Registration accepts invalid email |
| Sub-task | Step within an issue | Minutes to hours | Story, Task or Bug (required) | Write API tests for registration |
| Spike | Time-boxed investigation | 1-2 days | Epic (optional) | Evaluate email verification options |

### 4. The Key Issue Fields Explained

When you create an issue, you fill in **fields**. Think of fields as the printed boxes on the index card. Here are the most important ones.

| Field | What it is | How to use it well |
|---|---|---|
| **Summary** | The one-line title of the issue. Required. | Short, specific, and searchable. Say what and where. |
| **Description** | The full details, with formatting. | Follow a template (story format or bug template). Include context and acceptance criteria. |
| **Issue type** | Epic, Story, Task, Bug, Sub-task. | Pick the right one; you can change it later, but fix it early. |
| **Priority** | How urgently the work should be done (Highest to Lowest by default). | Set by the product owner or triage group, based on business impact. |
| **Assignee** | The person responsible for doing the work right now. | One person at a time; "Unassigned" is okay in a backlog. |
| **Reporter** | The person who created or raised the issue. | Set automatically to you; useful when someone has questions. |
| **Labels** | Free-form tags for flexible grouping. | Keep a short, agreed vocabulary (for example `regression`, `ui`, `api`). |
| **Components** | Formal parts of the product (for example Login, Payments). | Defined by a project admin; used for routing and reports. |
| **Affects version(s)** | The version of the product where a bug was found. | Fill for bugs: it helps trace regressions. |
| **Fix version(s)** | The release in which the work is planned or delivered. | Set by the team when work is scheduled for a release. |
| **Environment** | Where the problem occurred (OS, browser, device, build, URL). | Essential for bugs; copy exact versions. |
| **Sprint** | The sprint the issue is planned in. | Set when you pull the issue into a sprint. |
| **Story points / Original estimate** | Size (points) or time (hours/days). | Points for Scrum teams; time for those who track time. |
| **Attachments** | Files such as screenshots, logs, videos. | Always attach evidence to bugs. |
| **Linked issues** | Relationships to other issues. | Connect bugs to stories, blockers, duplicates. |
| **Due date** | A calendar date by which work should be complete. | Use sparingly; mostly for hard deadlines. |
| **Custom fields** | Extra fields added by admins, such as Severity or Test Type. | Use consistently, and fill in what your team has agreed is mandatory. |

Some further details worth knowing:

- **Priority vs Fix version vs Sprint.** *Priority* says how important; *Sprint* says when we plan to do it in the short term; *Fix version* says which release it will ship in.
- **Original estimate vs Story points.** Teams usually pick one primary method. Many Scrum teams use story points only; some teams use "original estimate" for time and "time tracking" fields to log work. Mixing them without agreement causes confusion.
- **Components vs Labels.** Covered in section 11.
- **Fields shown on screen depend on your project configuration.** You may not see every field in this table on the Create screen. In company-managed projects, an administrator controls which fields appear for which issue type. In team-managed projects, you can adjust fields in the project settings.

### 5. Creating Issues Step by Step

There are several ways to create an issue. Which you use depends on the situation.

**Method A: The Create button (full form)**

1. Click the **Create** button in the top navigation bar (a blue button on most layouts).
2. In the dialog, choose the **Project** (for example "QE Foundations").
3. Choose the **Issue type** (Story, Bug, Task, Epic...). The form changes depending on what you pick.
4. Type a **Summary**.
5. Complete the **Description** using the formatting toolbar.
6. Set other fields: Priority, Assignee, Labels, Components, Affects version, Parent (Epic) and so on.
7. Optionally tick **Create another** if you plan to add several issues in a row.
8. Click **Create**. A confirmation message appears with the new issue key, which you can click to open.

**Method B: Quick create on the backlog or board**

On the **Backlog** (and on boards, depending on setup) there is a **+ Create issue** link at the bottom of a sprint or the backlog list. You can:

1. Click **+ Create issue**.
2. Select the issue type from the small dropdown.
3. Type just a summary, and press Enter.

The issue is created instantly with only the minimum fields. Open it later to add detail. This is great for capturing ideas fast or building a first list of stories, but it is a **trap** if you never come back to fill in the description. Quick create is for speed, not completeness.

On an Epic, you can also use **Add child issue** (or "Create child work item") to create items already attached to the Epic.

**Method C: From a template or by cloning**

Many teams create new issues from a **template** so that every story or bug starts with the same headings. In Jira, you can:

- Save a standard description (as text in a Confluence page or a pinned note) and paste it into the Description field.
- Some project types provide a **description template** feature or default description; availability depends on plan and project type.
- **Clone** an existing, well-written issue (see section 16) and edit it.
- Use Jira **automation rules** to pre-fill fields; this is an admin topic.

For this course, a simple copy-and-paste template works well. Later in this lesson you will see both a Story template and a Bug template.

**Method D: Bulk create and CSV import (introduction)**

When you have many issues to create at once, such as importing an existing spreadsheet of requirements, you can use **CSV import**:

1. Prepare a CSV file with a header row. Typical columns: `Summary`, `Issue Type`, `Description`, `Priority`, `Labels`, `Epic Name` or `Parent`.
2. In Jira, look for **Import issues from CSV** (often under the **Settings** area, **System**, **External System Import**, or the **Apps/Import** menu, depending on your version and permissions).
3. Upload the file, choose the project, then **map** each CSV column to a Jira field.
4. Run the import and review the result.

Things to know: you need adequate permission; importing is hard to undo, so test with two or three rows first; and the exact path to the import screen differs by Jira version. For this lesson, knowing the *idea* is enough: **a CSV with a header row, a column per field, and a mapping step.**

There is also **Create multiple issues** from a pasted list in some versions, and on the backlog you can create several in a row by pressing Enter after each summary.

### 6. Working in an Issue: The Issue View

When you open an issue, you see the **issue view**. It typically has these areas:

- **Header:** the key, the summary (editable by clicking), and action buttons (such as Attach, Add a child issue, Link issue).
- **Left or main area:** the Description, Attachments, Child issues or Sub-tasks, Linked issues, and the Activity section (Comments, History, Work log).
- **Right panel (Details):** Status, Assignee, Reporter, Labels, Priority, Sprint, Story points, Components, Versions, and other fields.

Most fields can be edited **in place**: click the value and change it. This is handy but also risky: a careless click can change a field. Remember that every change is recorded in History.

### 7. Writing a Great Story with Acceptance Criteria

#### 7.1 Principles: INVEST

A well-known checklist for a good story is **INVEST**:

| Letter | Means | In plain language |
|---|---|---|
| **I** | Independent | Can be built and tested without waiting for other stories (as far as possible). |
| **N** | Negotiable | Details are open for discussion; it is not a rigid contract. |
| **V** | Valuable | Delivers something a user or the business cares about. |
| **E** | Estimable | The team understands enough to estimate it. |
| **S** | Small | Fits within one sprint. |
| **T** | Testable | You can tell clearly when it is done. |

As a QE, the **T** is your special responsibility. If you cannot imagine how to test a story, it is not ready.

#### 7.2 Acceptance Criteria in Given/When/Then

The **Given/When/Then** format (from Behaviour-Driven Development, or BDD) describes a scenario in three parts:

- **Given** the starting situation (preconditions).
- **When** the user takes an action.
- **Then** the observable result.

You can chain extra steps with **And** and **But**. Each scenario covers one behaviour.

Example for registration:

```gherkin
Scenario: Successful registration with a valid email and password
  Given I am on the registration page
  And no account exists for "new.user@example.com"
  When I enter "new.user@example.com" as my email
  And I enter "Passw0rd!23" as my password
  And I click "Create account"
  Then I see the message "Registration successful. Please check your email to verify your account."
  And a verification email is sent to "new.user@example.com"

Scenario: Registration with an email that is already registered
  Given an account already exists for "existing.user@example.com"
  When I try to register with "existing.user@example.com"
  Then I see the error "An account with this email already exists."
  And no new account is created

Scenario: Registration with an invalid email format
  Given I am on the registration page
  When I enter "not-an-email" as my email and a valid password
  And I click "Create account"
  Then I see the error "Please enter a valid email address."
```

Notice that each scenario is concrete: exact messages, exact values. These can become manual test cases today and automated tests later.

#### 7.3 Acceptance Criteria as a Checklist

Not every team likes Given/When/Then; many prefer a simple **checklist** (also called rule-based acceptance criteria). It is shorter and quick to scan:

- [ ] Email field accepts only valid email format (contains `@` and a domain).
- [ ] Password must be at least 8 characters with one number and one special character.
- [ ] Duplicate emails are rejected with the message "An account with this email already exists."
- [ ] On success, the user sees a confirmation message and receives a verification email.
- [ ] Required fields show an inline error when left empty.
- [ ] The Create account button is disabled while the request is in progress (prevents double submit).

**Which to use?** Use Given/When/Then for behaviour with multiple steps and states (login flows, workflows). Use a checklist for simple rules and validations. Many good stories combine both: a checklist of rules plus two or three key scenarios.

In Jira, you can put acceptance criteria in the Description under a heading "Acceptance Criteria." Some projects have a dedicated **Acceptance Criteria** custom field. Either works; consistency matters more.

#### 7.4 Good vs Bad Stories for Project 1

Seeing contrast is the fastest way to learn. Here are three stories, each in a weak and a strong version.

**Example 1: User can register with email**

*Bad:*

> **Summary:** Registration
> **Description:** Users should be able to register. Make it work well and be secure.

Problems: the summary is a label, not a statement; no user, no value, no rules; "work well" and "secure" cannot be tested.

*Good:*

> **Summary:** User can register with email and password
> **Description:**
> **As a** new visitor,
> **I want** to create an account using my email address and a password,
> **so that** I can access features available only to registered users.
>
> **Acceptance Criteria**
> - [ ] Email must be in valid format; invalid format shows "Please enter a valid email address."
> - [ ] Password must be 8-64 characters with at least one number and one special character.
> - [ ] A duplicate email is rejected with "An account with this email already exists."
> - [ ] On success the user sees a confirmation and receives a verification email.
>
> **Out of scope:** social login, phone number registration.
> **Story points:** 5

**Example 2: User can log in**

*Bad:*

> **Summary:** Login page
> **Description:** Build login page. Should be fast. Handle errors.

Problems: describes an artefact, not value; "fast" and "handle errors" are vague; no scenarios.

*Good:*

> **Summary:** Registered user can log in with email and password
> **Description:**
> **As a** registered user,
> **I want** to log in with my email and password,
> **so that** I can access my account and personal information.
>
> **Acceptance Criteria**
> ```gherkin
> Scenario: Successful login
>   Given I have a verified account
>   When I enter my correct email and password and click "Log in"
>   Then I am taken to my dashboard
>   And my name appears in the page header
>
> Scenario: Wrong password
>   Given I have a verified account
>   When I enter my correct email and an incorrect password
>   Then I see "Incorrect email or password."
>   And I remain on the login page
>
> Scenario: Account locked after repeated failures
>   Given I have entered a wrong password 5 times in a row
>   When I try to log in again, even with the correct password
>   Then I see "Your account is temporarily locked. Try again in 15 minutes."
> ```
> **Story points:** 3

**Example 3: User can reset password**

*Bad:*

> **Summary:** Forgot password
> **Description:** Add forgot password feature like other sites.

Problems: "like other sites" is not a requirement; unknown behaviour; the team and tester will guess differently.

*Good:*

> **Summary:** User can reset a forgotten password through an emailed link
> **Description:**
> **As a** registered user who forgot my password,
> **I want** to receive a reset link by email,
> **so that** I can regain access without contacting support.
>
> **Acceptance Criteria**
> - [ ] A "Forgot password?" link is visible on the login page.
> - [ ] Entering a registered email sends a reset link valid for 30 minutes.
> - [ ] Entering an unregistered email shows the same generic confirmation message (to avoid revealing which emails have accounts).
> - [ ] The reset link can be used only once.
> - [ ] The new password must follow the same rules as registration.
> - [ ] After a successful reset the user is able to log in with the new password and not the old one.
> **Story points:** 5

Notice how the good versions give testers concrete behaviours, include negative cases, and show security thinking (the generic message for unknown emails).

#### 7.5 A Story Template You Can Reuse

```
*As a* <user>,
*I want* <goal>,
*so that* <benefit>.

h3. Acceptance Criteria
* <criterion 1>
* <criterion 2>

h3. Out of scope
* <what we are not doing>

h3. Notes / Links
* Design: <link>
* Related: <issue keys>
```

(The `h3.` heading syntax is Jira's older wiki markup; the newer editor uses a toolbar or Markdown-style shortcuts. See section 8.3.)

### 8. Writing a Great Bug in Jira

#### 8.1 From Defect Report to Jira Fields

In the defect lifecycle lesson earlier today, you learned that a good defect report contains certain information. Now we map that information onto Jira fields. This table is your cheat sheet:

| Defect report element | Jira field | Notes |
|---|---|---|
| Defect ID | **Issue key** (automatic, e.g. `QEF-31`) | You do not type this; Jira generates it. |
| Title / summary | **Summary** | Specific and searchable: what fails, where, under what condition. |
| Description of the problem | **Description** (opening sentence) | One or two lines of overview. |
| Steps to reproduce | **Description** (numbered list) | Exact, in order, starting from a known state. |
| Expected result | **Description** | What should happen, per the requirement. |
| Actual result | **Description** | What did happen, with exact messages. |
| Test environment (OS, browser, build, URL) | **Environment** field (or Description) | Include versions. |
| Version / build where found | **Affects version(s)** | Helps trace regressions. |
| Severity | **Custom field "Severity"** | Technical impact. Not a default field. |
| Priority | **Priority** | Business urgency. Agreed in triage. |
| Module / area | **Components** | For example Registration. |
| Evidence (screenshots, logs, video) | **Attachments** | Always attach. |
| Reporter | **Reporter** | Set automatically. |
| Owner / developer | **Assignee** | Often set after triage. |
| Related requirement or story | **Linked issues** (relates to / is caused by) | Traceability. |
| Status (New, Open, Fixed, Closed...) | **Status** | Workflow states; covered by the defect lifecycle and next lesson. |
| Date reported | **Created** (automatic) | System field. |
| Tags | **Labels** | For example `regression`, `smoke`. |

#### 8.2 Principles of a Great Bug

1. **One bug per issue.** If you find three problems, raise three bugs and link them. A mixed bug cannot be closed cleanly.
2. **Reproducible.** The steps should allow a stranger to see the problem in a few minutes. If it happens intermittently, say how often ("3 out of 10 attempts").
3. **Specific summary.** Use the pattern: *[Area] Symptom when condition.* For example: "[Registration] Invalid email format accepted when domain has no dot."
4. **Facts, not blame or opinion.** Write "The page shows a blank screen," not "The developer broke the page."
5. **Evidence.** Screenshot, video, console log, network trace. A picture saves a thousand words of comments.
6. **Search first.** Before raising a bug, search for duplicates using JQL or the search box.
7. **Separate expected from actual.** Always link expected behaviour to a requirement or story if possible.

#### 8.3 Description Formatting in Jira

Jira's editor lets you format text so that a bug is easy to read. The exact toolbar varies, but these capabilities exist in most versions:

| Feature | How to use it | When to use it in a bug |
|---|---|---|
| **Headings** | Toolbar "Normal text" dropdown, or type `#` then space (Markdown-style shortcuts) in the newer editor; `h3.` in older wiki markup | Separate sections: Steps, Expected, Actual |
| **Bulleted and numbered lists** | Toolbar buttons, or type `*` / `1.` followed by a space | Numbered list for steps; bullets for environment details |
| **Code block** | Toolbar "Insert" menu, or type three backticks then Enter | Error messages, stack traces, JSON responses, console logs |
| **Inline code** | Wrap text in single backticks | Field names, URLs, button labels |
| **Panel** | Insert menu, "Panel" (info, note, success, warning, error) | Highlight a workaround or a warning |
| **Mentions** | Type `@` and begin typing a name | Ask a specific person a question or notify them |
| **Bold / italic** | Toolbar, or `**bold**` / `*italic*` shortcuts in the newer editor | Emphasise exact messages |
| **Tables** | Insert menu, Table | Compare test data or results |
| **Links** | Paste a URL, or type an issue key such as `QEF-12` | Reference stories and pages |
| **Images / attachments inline** | Drag and drop into the description | Show the screenshot where it is relevant |

> **Tip:** Smart-link behaviour: if you paste an issue key such as `QEF-12` or a URL, Jira often turns it into a clickable link with the title. Try it.

#### 8.4 A Bug Template

```
h3. Overview
<One or two sentences describing the problem>

h3. Environment
* Build/Version: <e.g. v0.3.1>
* URL: <page>
* Browser/OS: <e.g. Chrome 126 on Windows 11>

h3. Steps to Reproduce
# <Step 1>
# <Step 2>
# <Step 3>

h3. Expected Result
<What should happen, per QEF-xx>

h3. Actual Result
<What actually happens, exact messages>

h3. Frequency
<Always / Intermittent (x of y attempts)>

h3. Evidence
<Screenshot, video, log attached>

h3. Notes / Workaround
<Anything else useful>
```

#### 8.5 Complete Worked Example

Here is a bug as it should appear in Jira for Project 1.

**Issue type:** Bug
**Summary:** [Registration] Email "user@domain" without a dot is accepted as valid
**Priority:** Medium
**Severity (custom field):** Minor
**Components:** Registration
**Affects version:** 0.3.1
**Labels:** `validation`, `negative-test`
**Environment:** Chrome 126, Windows 11, Project 1 test site (QA environment), build 0.3.1
**Assignee:** Unassigned (to be set in triage)
**Reporter:** (you)
**Linked issues:** *relates to* QEF-14 (User can register with email and password)
**Attachments:** `registration-invalid-email.png`, `console-log.txt`

**Description:**

> ### Overview
> The registration form accepts an email address with no top-level domain (for example `user@domain`) and creates an account, although acceptance criteria in QEF-14 state that only valid email formats are allowed.
>
> ### Environment
> - Build: 0.3.1 (QA environment)
> - URL: `/register`
> - Browser/OS: Chrome 126 on Windows 11
>
> ### Steps to Reproduce
> 1. Open the registration page at `/register`.
> 2. Enter `user@domain` in the Email field.
> 3. Enter `Passw0rd!23` in the Password field.
> 4. Click **Create account**.
>
> ### Expected Result
> The form shows the error "Please enter a valid email address." and no account is created (per QEF-14, acceptance criterion 1).
>
> ### Actual Result
> The form shows "Registration successful." and an account for `user@domain` is created. The API response is:
>
> ```json
> { "status": 201, "message": "User created", "email": "user@domain" }
> ```
>
> ### Frequency
> Reproducible 5 out of 5 attempts.
>
> ### Notes
> Info panel: Email addresses with a dot in the domain (for example `user@domain.com`) are validated correctly. Suggest checking the email validation pattern. @Dana (developer) can you take a look?

Note how this bug uses a heading structure, a numbered list for steps, a code block for the API response, an info panel for the note, and an @mention to draw attention. A developer can reproduce it in under two minutes.

**Bad version for contrast:**

> **Summary:** Registration broken
> **Description:** Registration doesn't work properly with emails. Please fix ASAP!!!

Why bad: no steps, no expected/actual, no environment, no evidence, vague summary, shouting priority in the description instead of using the Priority field.

### 9. Linking Issues

A **link** is a labelled relationship between two issues. Links make dependencies and relationships visible without copying information around.

**Common link types (default names; admins can customise):**

| Link type | Wording from each side | Meaning | Example |
|---|---|---|---|
| **Blocks** | "blocks" / "is blocked by" | One issue must be finished before the other can proceed | "Set up test environment" blocks "Test registration" |
| **Relates to** | "relates to" | A general association without a dependency | A bug relates to a story |
| **Duplicates** | "duplicates" / "is duplicated by" | Two issues describe the same problem; one is the original | A new bug duplicates an earlier bug |
| **Tests** | "tests" / "is tested by" | A test issue verifies a story (appears when test tools or the link type is configured) | A test sub-task or test case tests a story |
| **Clones** | "clones" / "is cloned by" | One issue was created as a copy of another | Added automatically when you clone |
| **Causes** (in some setups) | "causes" / "is caused by" | Root cause relationships | A change causes a regression bug |

The exact list varies by configuration. Not every site has "tests / is tested by" by default; it often appears when a test management app is installed, or it can be added by an administrator.

**How to link an issue:**

1. Open the issue.
2. Click **Link issue** (or the link icon, or use the **...** menu).
3. Select the **link type** from the dropdown.
4. Start typing the key or summary of the other issue and select it.
5. Click **Link** (or **Save**).

**Linking bugs to stories.** This is one of the most valuable habits for a QE. When you find a bug while testing a story, link it so that:

- The story shows an obvious list of its open defects.
- The product owner and Scrum Master can see that the story cannot be considered Done.
- Later, someone can trace which requirement was affected, which helps regression planning.
- Reports can count defects per story or per Epic.

A common choice is to use **relates to** for a bug found while testing a story, or **is caused by / causes** if your team has configured it. Some teams create the bug as a **child of the story's Epic** and link it to the story. Agree on one convention and stay with it.

**Duplicates.** If you find that your new bug is already reported, do not delete it. Link it as **duplicates** the original and close it with a resolution such as "Duplicate." The history remains, and people who watched the duplicate can follow the original.

### 10. Collaborating: Comments, Mentions, Watchers, Attachments and History

**Comments.** Use the comment box in the **Activity** section for questions, decisions and progress notes. Good comment habits:

- Keep decisions in comments, not only in chat or email, so the issue holds the full story.
- Write complete thoughts: "Retested on build 0.3.2: still fails with `user@domain`."
- Use **internal** comments (where available, for example in service projects) only when appropriate.

**Mentions.** Type `@` followed by a name to notify a person. Use mentions to ask a direct question or request an action. Avoid mentioning everyone for every comment, because too many notifications are ignored.

**Watchers.** A **watcher** is a person who receives notifications when an issue changes. You can click the eye icon to watch an issue yourself, or add other watchers. As a QE, watch the stories you are testing and the bugs you reported. The reporter and assignee are often notified automatically depending on notification settings.

**Attachments.** Attach screenshots, screen recordings, log files, and test data. Tips:

- Name files meaningfully (`login-error-chrome126.png`, not `Screenshot1.png`).
- Do not attach sensitive data such as real customer information or passwords.
- Respect file size limits (set by your site).
- Pasting an image straight into the description or a comment (Ctrl+V) is usually the fastest approach.

**Issue history.** The **History** tab (in the Activity section) lists every change: who changed which field, from what to what, and when. For QEs this is gold. If a story's acceptance criteria were changed after testing began, History shows it. If a bug's priority moved from High to Low, History shows who did it. Use it to answer "when and why did this change?" Because history is automatic, you cannot hide an edit, which supports honest and traceable work.

### 11. Priority, Severity, Labels and Components

#### 11.1 Priority vs Severity

You learned these two terms in the defect lifecycle lesson. Recap:

- **Severity** is the *technical impact* of a defect on the system. It is usually judged by QE. (Examples: Critical, Major, Minor, Trivial.)
- **Priority** is the *business urgency* of fixing it. It is typically decided with the product owner. (Examples: Highest, High, Medium, Low, Lowest.)

They are related but not the same. A spelling mistake in the company name on the home page may have low severity (nothing breaks) but high priority (embarrassing and highly visible). A crash in a rarely used admin report may have high severity but low priority.

In Jira:

- **Priority** is a **default field** with levels commonly named Highest, High, Medium, Low, Lowest. Administrators can rename or reorder them.
- **Severity** is **not a default field**. Teams that want it add a **custom field**, often a dropdown with Critical / Major / Minor / Trivial. If your project does not have one, you can mention severity in the description or use a label, but a real field is better because you can search and report on it.

| Combination | Example in Project 1 | Typical decision |
|---|---|---|
| High severity, high priority | Login crashes for all users | Fix immediately |
| High severity, low priority | Crash in an obscure setting page used by one admin | Schedule, document a workaround |
| Low severity, high priority | Company name misspelled on login page | Quick fix soon |
| Low severity, low priority | Slight misalignment on a rarely visited help page | Backlog |

#### 11.2 Labels vs Components

| Aspect | Labels | Components |
|---|---|---|
| Definition | Free-text tags you can add on the fly | Formal, predefined parts of the product |
| Who creates them | Anyone with permission, by typing | Project administrators (in most setups) |
| Consistency | Easy to misspell: `login` vs `Login` vs `log-in` | Chosen from a list, so consistent |
| Extra features | Searchable and filterable | Can have a component lead and a default assignee; used in reports and routing |
| Best use | Cross-cutting tags: `regression`, `smoke`, `usability`, `needs-ux` | Product areas: Registration, Login, Dashboard |

A simple rule: **if it is *where* in the product, use a component; if it is *a flag or theme* that cuts across areas, use a label.** Keep your label list small and agreed. A project with 200 inconsistent labels is as unhelpful as no labels at all.

### 12. Estimation and Story Points

**Why estimate?** Estimates help the team decide how much work fits into a sprint and give the product owner a rough idea of the time to finish a goal. Estimates are **forecasts**, not promises.

**Story points** are a relative scale. Teams commonly use the **Fibonacci-like sequence**: 1, 2, 3, 5, 8, 13. The growing gaps reflect growing uncertainty: you can tell a 2 from a 3, but not a 12 from a 13.

How points work:

- Choose a small, well-understood **reference story** and call it a 2 or 3. Compare others against it.
- Points reflect **effort, complexity and uncertainty together**, not just hours.
- Different teams have different scales. "5 points" on one team is not equal to "5 points" on another, so never compare teams by points.
- **Velocity** is the number of points a team completes per sprint on average; it is used for forecasting.

**Planning Poker.** A common technique: each team member privately picks a card with their estimate and everyone reveals at once. If estimates differ widely (a 2 and a 13), the highest and lowest explain their reasoning and the team re-votes. The discussion is more valuable than the number. As a QE, **speak up on testing effort**. Developers sometimes forget that thorough testing of a "simple" form can take as long as building it.

**Time-based estimates.** Jira also offers **Original estimate**, **Remaining estimate** and **Time spent** (time tracking), in hours or days. Some organisations require this. If your team uses points, avoid also demanding hour estimates on every story; it duplicates work.

**Where to set them.** Story points appear as a field on the issue (and often directly on the backlog next to each issue). Click the small number badge to edit it.

| Points | Rough meaning | Project 1 example |
|---|---|---|
| 1 | Trivial, very clear | Change the text of an error message |
| 2 | Small | Add an inline validation message |
| 3 | Moderate | Login with success and wrong-password scenarios |
| 5 | Larger, some unknowns | Registration with validation and verification email |
| 8 | Big, many unknowns; consider splitting | Full password reset including email and expiry |
| 13+ | Too big; split before taking into a sprint | "Complete account management" |

### 13. Splitting Large Stories

A story that is too big (often 8 points or more) is hard to estimate, hard to test and risky. **Splitting** means breaking it into smaller stories, each still delivering some value.

**Vertical slices vs horizontal slices.**

- A **horizontal slice** splits by technical layer: "Build the database," "Build the API," "Build the UI." Each piece alone delivers nothing a user can try.
- A **vertical slice** cuts through all layers to deliver a thin but complete piece of functionality: a user can do something, however small, from the screen to the database and back.

Think of a layered cake. Slicing horizontally gives you a plate of only icing. Slicing vertically gives you every layer in every piece. Always prefer **vertical slices**, because they can be tested end to end and shown to stakeholders.

**SPIDR.** A helpful technique by Mike Cohn gives five ways to split a story. **SPIDR** stands for:

| Letter | Split by | Example with "User can reset password" |
|---|---|---|
| **S** | **Spike** | Spike: investigate email service options and token expiry approach |
| **P** | **Paths** | Reset via emailed link (path 1) first; reset via security questions later (path 2) |
| **I** | **Interfaces** | Web interface first; mobile web layout second |
| **D** | **Data** | Handle standard email addresses first; internationalised addresses later |
| **R** | **Rules** | Basic password rules first; strength meter and breached-password check later |

Other useful splits: by **workflow steps** (request reset, then set new password), by **happy path vs error handling** (but make sure the happy path is still valuable), and by **user role**.

**Example split.** Original: "As a user I can manage my account" (13+). Split into:

1. User can register with email and password (5)
2. User can log in (3)
3. User can reset a forgotten password via emailed link (5)
4. User can log out (1)
5. User can view their profile details (2)

Now each story is testable on its own. The original becomes the Epic.

### 14. How QE Tracks Testing Work in Jira

Jira is not a test management tool by default, but it can do a good job of making testing visible. Here is how QEs commonly work.

**Testing a story.**

- Add **sub-tasks** to the story: "Review acceptance criteria for testability," "Design test cases," "Execute functional tests," "Exploratory testing," "Regression check," "Write automation (if applicable)." Each can be assigned, estimated and moved across the board. This makes QE work visible in sprint planning and prevents testing from being squeezed into the last day.
- Keep a **testing sub-task** open until testing is done, so the story does not appear complete too early. Tie this to the Definition of Done.

**Test cases.**

- Specialised **test management apps** (for example **Xray** and **Zephyr**) add issue types such as Test, Test Plan, Test Execution, with steps, results and traceability. They are paid add-ons from the Atlassian Marketplace and are mentioned here only so you recognise the names; this course does not require them.
- **Manual workaround without a plugin:**
  - Put test scenarios in the story as Given/When/Then or a checklist, and tick them as you pass them.
  - Use **sub-tasks** for test activities, or one **Task** per test charter (an exploratory testing session).
  - Store detailed test cases in a spreadsheet or Confluence page and **link** them in the issue.
  - Record test results in a **comment**: "Tested on build 0.3.2 (Chrome 126): AC1 pass, AC2 pass, AC3 FAIL see QEF-31."
  - Use a **label** such as `qe-verified` once testing is complete.

**Bugs.** Raise bugs with the template in section 8; link each to the story; keep the **Affects version** and **Fix version** up to date so you can retest the correct build.

**Visibility.** Use filters and boards (see JQL below) to answer: "What is waiting for QE?", "Which stories have open bugs?", "What failed in the last build?"

### 15. JQL Queries for Issues, Stories and Bugs

**JQL (Jira Query Language)** lets you search issues precisely. You met the basics yesterday. A query has the shape **field operator value**, combined with `AND`, `OR` and `NOT`, and optionally ended with `ORDER BY`. You can type JQL in **Filters > Advanced issue search** (the menu name may vary). In the examples below, `QEF` is the Project 1 key; replace it with yours.

**Query 1: All open bugs in the project**

```jql
project = QEF AND issuetype = Bug AND statusCategory != Done ORDER BY created DESC
```

`statusCategory != Done` excludes anything in a finished state regardless of the exact status names, which is safer than listing statuses by hand.

**Query 2: Critical and high priority bugs not yet resolved**

```jql
project = QEF AND issuetype = Bug AND priority in (Highest, High) AND resolution = Unresolved ORDER BY priority DESC, created ASC
```

`resolution = Unresolved` finds issues that have not been given a resolution. `in (...)` matches any value in the list.

**Query 3: Bugs reported by me**

```jql
project = QEF AND issuetype = Bug AND reporter = currentUser() ORDER BY created DESC
```

`currentUser()` is a function that means "whoever is logged in," so the same filter works for everyone.

**Query 4: Unassigned bugs needing triage**

```jql
project = QEF AND issuetype = Bug AND assignee IS EMPTY AND statusCategory != Done
```

`IS EMPTY` finds issues where a field has no value.

**Query 5: Bugs raised in the last 7 days**

```jql
project = QEF AND issuetype = Bug AND created >= -7d ORDER BY created DESC
```

`-7d` means seven days ago. You can also use `-2w` for two weeks, or `startOfWeek()`.

**Query 6: All stories in the current sprint**

```jql
project = QEF AND issuetype = Story AND sprint in openSprints()
```

`openSprints()` returns the active sprints. Use `sprint in futureSprints()` to see planned ones.

**Query 7: All issues in an epic**

```jql
project = QEF AND parent = QEF-1
```

Replace `QEF-1` with your Epic's key. In older company-managed projects, you might see `"Epic Link" = QEF-1` instead; both express the same idea. Which one works depends on your project configuration.

**Query 8: Stories without story points (not estimated)**

```jql
project = QEF AND issuetype = Story AND "Story point estimate" IS EMPTY AND statusCategory != Done
```

The field name in quotes may be "Story Points" or "Story point estimate" depending on your site.

**Query 9: Bugs in a specific component with a label**

```jql
project = QEF AND issuetype = Bug AND component = Registration AND labels = regression
```

Combines a component and a label. Remember that text values containing spaces should be wrapped in quotes.

**Query 10: Stories that have open bugs linked (requires the issueFunction or similar app)**

Without an app, you can look for issues that have any link:

```jql
project = QEF AND issueLinkType is not EMPTY AND statusCategory != Done
```

The `issueLinkType` clause is available only in some Jira versions or with specific apps. If it is rejected, use the **Linked issues** panel on the issue or a dashboard gadget instead. This is a good reminder that **some JQL features depend on your Jira version or installed apps.**

**Query 11: Overdue work**

```jql
project = QEF AND duedate < now() AND statusCategory != Done ORDER BY duedate ASC
```

Finds issues with a due date in the past that are still open.

**Query 12: Recently updated issues that mention "email" in the summary or description**

```jql
project = QEF AND text ~ "email" AND updated >= -14d ORDER BY updated DESC
```

`~` is the "contains" operator for text searches, and `text` searches several text fields at once.

**Bonus: Possible duplicates before you log a bug**

```jql
project = QEF AND issuetype = Bug AND summary ~ "registration" AND summary ~ "email" ORDER BY created DESC
```

Run something like this before creating a new bug.

**Saving a query.** After running a search, click **Save as** to store it as a **filter**. Filters can be shared and used as the source for boards and dashboard gadgets, which you will do in the next lesson.

> Tip: Jira usually offers autocomplete suggestions when you type JQL. Use them, and switch between the "Basic" and "JQL" search modes if you are unsure.

### 16. Bulk Edit, Cloning and Moving Issues

**Bulk change.** When you need to update many issues at once (for example, add the label `sprint-3-regression` to 12 bugs), use bulk change:

1. Run a search (basic or JQL) that returns the issues.
2. Click the **...** menu (or **Tools**) at the top right of the results and choose **Bulk change** (sometimes **Bulk edit**).
3. Select the issues using the checkboxes, then click **Next**.
4. Choose the operation: **Edit Issues**, **Transition Issues**, **Move Issues**, **Delete Issues**, **Watch/Stop watching**.
5. Select the field(s) to change and the new values.
6. Review the summary and confirm.

> **Warning:** Bulk operations affect many issues quickly and can be hard to reverse. Double check the filter results first, and avoid bulk deleting unless you are sure. You may need special permissions.

**Cloning.** To **clone** an issue means to create a copy with the same summary (prefixed "CLONE -") and fields. Use cloning to reuse a well-written template, or to repeat a test task each sprint. Steps: open the issue, click **...** (More), choose **Clone**, edit the summary, choose whether to clone attachments, links or sub-tasks (options vary), and click **Create**. Cloning automatically links the copy back to the original with "clones."

**Moving.** **Move** changes the project or the issue type of an existing issue, for example a Task that should have been a Story, or an issue created in the wrong project. Steps: open the issue, click **...**, choose **Move**, select the new project and issue type, map fields and statuses if prompted, and confirm. Notes: the issue gets a **new key** in a new project (the old key continues to redirect); some fields may not carry over; moving between projects with different workflows needs status mapping. Changing only the issue type within the same project is also done through **Move**, in many versions.

### 17. Hygiene and Naming Conventions

Good hygiene keeps Jira usable as it grows. Suggested conventions for your team:

| Area | Convention | Example |
|---|---|---|
| Story summary | Written as the user capability, starting with the user or a verb | "User can register with email and password" |
| Task summary | Starts with a verb | "Prepare test data for registration" |
| Bug summary | `[Area] Symptom when condition` | "[Login] Error message missing when password empty" |
| Epic name | Short noun phrase | "User Account Management" |
| Sub-task | Verb + object | "Execute functional tests for QEF-14" |
| Labels | Lowercase, hyphenated, from an agreed list | `regression`, `smoke`, `needs-ux` |
| Descriptions | Use the team template | Story template, Bug template |
| Links | Always link bugs to the related story | "relates to QEF-14" |
| Cleanup | Review stale issues regularly | Close or archive old items |

Additional habits:

- **Keep one issue = one thing.** Avoid "and" in summaries.
- **Update status honestly and promptly.** Boards that lie are worse than no boards.
- **Write for a stranger.** Someone reading in six months should understand.
- **Do not put secrets in issues.** No real passwords, personal data or tokens.
- **Groom the backlog.** Remove duplicates, close the obsolete, and keep the top of the backlog refined.
- **Agree on definitions.** What is a Bug vs a Story? What does each priority mean? Write them down.

### 18. Common Mistakes

| Mistake | Why it hurts | Better approach |
|---|---|---|
| Vague summary ("It doesn't work") | Cannot be searched or understood from a list | Specific, with area and symptom |
| Missing steps to reproduce | Developer cannot see the problem; cycle of "cannot reproduce" | Numbered steps from a known starting state |
| Multiple bugs in one issue | Cannot close partially; confusing | One bug per issue, linked together |
| No acceptance criteria | Everyone guesses what "done" means | Add testable criteria before sprint planning |
| Using Epic as a dumping ground | Meaningless reports | Epics represent clear goals |
| Overusing priority "Highest" | Everything is urgent, so nothing is | Agree on definitions; use sparingly |
| Confusing severity and priority | Wrong triage order | Severity = impact; priority = urgency |
| Not linking bugs to stories | Lost traceability; stories look Done while defects exist | Link every bug |
| Skipping duplicate search | Wasted effort and fragmented conversation | Search before creating |
| Too many sub-tasks | Board clutter; admin overhead | Use only where valuable |
| Quick-create and never filling in details | Empty cards that no one understands | Return and complete the description |
| Inconsistent labels | Searches miss items | Use an agreed list; prefer components for areas |
| Editing the description silently after estimating | Surprise scope change | Comment on changes and tell the team |
| Putting sensitive data in attachments | Security and privacy risk | Use dummy data |
| Estimating with hours and points both without a reason | Double the effort, little benefit | Pick one primary method |

### 19. AI Features in Jira (A Cautious Overview)

Atlassian has been adding AI-powered assistance to its products (often branded with names such as **Atlassian Intelligence** or **Rovo**, though names and packaging change). Whether you see these features, and exactly how they behave, **depends on your plan, your administrator's settings and the current release. Check the current Atlassian documentation for what is available to you.**

Features you may encounter, described in general terms:

- **Summarising an issue.** Condensing a long comment thread or description into a short summary. Useful for catching up on a bug with 40 comments.
- **Drafting or improving text.** Suggesting a description, rewording a summary or turning rough notes into a structured story or bug report.
- **Suggesting child issues or breaking down work.** Proposing sub-tasks or smaller stories from an Epic or story description.
- **Natural-language search to JQL.** Typing a question such as "open high priority bugs assigned to me" and getting a JQL query produced for you.
- **Automation help.** Describing an automation rule in words and having a draft rule created.
- **Search and chat assistants.** Finding information across Jira and connected tools.

How to use such tools responsibly as a QE:

1. **Treat output as a draft, not a fact.** AI can invent details, such as error messages or steps you did not observe. You are the author of record; verify everything.
2. **Never let it fabricate evidence.** The "actual result" in a bug must come from what you saw.
3. **Review generated acceptance criteria critically.** Do they cover negative and edge cases? Are they testable? Are they consistent with what the product owner agreed?
4. **Check generated JQL.** Read it, understand it, and verify the result count looks plausible. You now know enough JQL to review it.
5. **Respect privacy and policy.** Know your organisation's rules about what content may be processed by AI features, and avoid pasting sensitive data.
6. **Do not rely on it to replace the conversation.** A story is "a promise to have a conversation." AI can help you start it, not finish it.

You will build deeper AI skills later in the programme; for now, the key point is that **good fundamentals make AI assistance far more useful, and poor fundamentals make it confidently wrong.**

---

## Examples

### Example A: From Epic to Sub-tasks (Project 1 hierarchy)

```
QEF-1   Epic     User Account Management
 |- QEF-2   Story  User can register with email and password        (5 pts)
 |   |- QEF-6   Sub-task  Review acceptance criteria for testability
 |   |- QEF-7   Sub-task  Design and execute functional test cases
 |   |- QEF-8   Sub-task  Exploratory test: registration edge cases
 |- QEF-3   Story  Registered user can log in                        (3 pts)
 |- QEF-4   Story  User can reset a forgotten password               (5 pts)
 |- QEF-5   Task   Prepare test data for registration and login
 |- QEF-9   Bug    [Registration] Email "user@domain" accepted
```

### Example B: A bug linked to a story

QEF-9 (Bug) *relates to* QEF-2 (Story). On QEF-2, the **Linked issues** panel now shows "is related to QEF-9 - [Registration] Email "user@domain" accepted - Open". The product owner can see at a glance that QEF-2 has an unresolved defect.

### Example C: A short comment that helps

> Retested on build 0.3.2 (Chrome 126, Windows 11). `user@domain` is now rejected with "Please enter a valid email address." `user@domain.com` still works. No regression seen on login. Moving to Verified. @Dana thanks for the quick fix.

This comment states the build, environment, what was checked, the result, and who is thanked.

### Example D: Reading a JQL query step by step

```jql
project = QEF AND issuetype = Bug AND priority in (Highest, High) AND resolution = Unresolved ORDER BY created ASC
```

Read it aloud: "In project QEF, show me issues that are Bugs, whose priority is Highest or High, and that have not been resolved, with the oldest first." If you can read a query in plain English, you can write one.

---

## Try It: Hands-On Activity

**Goal:** Populate your practice Jira project for Project 1 - QE Foundations with one epic, four stories, two tasks and three bugs, then link them and run searches.

**Time:** About 60-90 minutes.

**Before you start:** Make sure you have a Jira Software project (your instructor will provide it or you may use the one you created yesterday). The examples use key `QEF`; use your own key. Use the **Create** button for the first issue of each type, and quick create for the others if you wish; then complete each description.

### Part 1: Create the Epic

1. Click **Create**. Issue type: **Epic**.
2. **Summary:** `User Account Management`
3. **Description:**

```
Allow visitors to create an account, sign in securely and recover access if they forget their password.

h3. In scope
* Registration with email and password
* Login
* Password reset by emailed link

h3. Out of scope
* Social login
* Two-factor authentication
```

4. Priority: **High**. Click **Create**. Note the key (for example `QEF-1`).

### Part 2: Create the Four Stories

For each, set the **Parent** (or Epic Link) to your Epic and fill in story points.

**Story 1: User can register with email and password** (5 points)

```
As a new visitor,
I want to create an account using my email address and a password,
so that I can access features available only to registered users.

Acceptance Criteria
- Email must be in a valid format; otherwise show "Please enter a valid email address."
- Password must be 8-64 characters with at least one number and one special character.
- A duplicate email is rejected with "An account with this email already exists."
- On success the user sees a confirmation and receives a verification email.
- Required fields show an inline error when left empty.
```

**Story 2: Registered user can log in** (3 points)

```
As a registered user,
I want to log in with my email and password,
so that I can access my account.

Acceptance Criteria
Scenario: Successful login
  Given I have a verified account
  When I enter the correct email and password and click "Log in"
  Then I am taken to my dashboard

Scenario: Wrong password
  Given I have a verified account
  When I enter a wrong password
  Then I see "Incorrect email or password." and stay on the login page

Scenario: Lockout
  Given I entered a wrong password 5 times
  When I try again
  Then I see "Your account is temporarily locked. Try again in 15 minutes."
```

**Story 3: User can reset a forgotten password through an emailed link** (5 points)

```
As a registered user who forgot my password,
I want to receive a reset link by email,
so that I can regain access without contacting support.

Acceptance Criteria
- "Forgot password?" link is visible on the login page.
- A registered email receives a reset link valid for 30 minutes.
- An unregistered email shows the same generic confirmation message.
- A reset link can be used only once.
- The new password must follow the same rules as registration.
```

**Story 4: User can log out** (1 point)

```
As a logged-in user,
I want to log out,
so that my account stays safe on shared computers.

Acceptance Criteria
- A "Log out" option is visible in the page header when logged in.
- After logging out, the user is returned to the login page.
- Using the browser Back button after logout does not show private pages.
```

### Part 3: Create the Two Tasks

**Task 1: Prepare test data for registration and login**

```
Create a test data sheet with 10 valid and 10 invalid email/password combinations,
including boundary lengths (7, 8, 64, 65 characters) and special characters.
Done when: the sheet is saved in the shared folder and the link is added to this issue.
```
Labels: `test-data`. Assignee: yourself.

**Task 2: Set up the QA test environment checklist**

```
Document the URL, test accounts, browsers and versions to be used for Project 1 testing.
Done when: a short list is added to this issue as a comment or attachment.
```
Labels: `environment`.

### Part 4: Create the Three Bugs

Use the Bug template from section 8.4. Give each bug the **Affects version** `0.3.1` (create it if needed or put it in Environment), a **Component** if available, a **Severity** (custom field if you have it, otherwise in the description), and an attached screenshot (a sample image is fine for practice).

**Bug 1: [Registration] Email "user@domain" without a dot is accepted as valid**

- Priority: Medium. Severity: Minor.
- Steps: open `/register`; enter `user@domain` and `Passw0rd!23`; click **Create account**.
- Expected: error "Please enter a valid email address."
- Actual: "Registration successful." and the account is created.
- Link: *relates to* Story 1.

**Bug 2: [Login] No error message shown when password field is empty**

- Priority: Medium. Severity: Minor.
- Steps: open `/login`; enter a valid email; leave Password empty; click **Log in**.
- Expected: inline error "Password is required."
- Actual: page reloads with no message; user is unsure what happened.
- Link: *relates to* Story 2.

**Bug 3: [Password reset] Reset link still works after it has been used once**

- Priority: High. Severity: Major.
- Steps: request a reset link; open the link and set a new password; open the same link again.
- Expected: message "This link has already been used or has expired."
- Actual: the reset form opens again and accepts another password.
- Link: *relates to* Story 3. Add a comment that mentions a teammate and asks them to confirm security impact.

### Part 5: Link and Review

1. Add a **blocks** link from Task 2 ("Set up the QA test environment checklist") to Story 1, with the explanation that testing cannot begin until the environment is documented. Check that Story 1 now shows "is blocked by."
2. Add a **Story 4 relates to Story 2** link.
3. Open the Epic. Confirm that all four stories and any child items are listed.
4. Add **sub-tasks** to Story 1: "Review acceptance criteria for testability" and "Execute functional test cases."
5. Click the **eye** icon to watch Story 1 and Bug 3.

### Part 6: Run Searches

In advanced issue search, run and save at least three of these (replace `QEF`):

```jql
project = QEF AND issuetype = Bug AND statusCategory != Done ORDER BY priority DESC
```

```jql
project = QEF AND parent = QEF-1 AND issuetype = Story
```

```jql
project = QEF AND issuetype = Bug AND priority in (Highest, High) AND resolution = Unresolved
```

Write down how many results each returns and whether it matches what you created (1 epic, 4 stories, 2 tasks, 3 bugs).

### Part 7: Practise a Clean-up

1. Create a deliberately sloppy issue called "stuff" with no description.
2. Use **Move** (or edit the issue type) to turn it into a Task.
3. Improve the summary and description using the conventions in section 17.
4. Use **Clone** on Bug 1 and rename the clone to a different validation problem, then compare the **clones** link.
5. Delete the clone if it is not needed (only if you have permission).

### Self-Check Checklist

- [ ] The Epic has four child stories.
- [ ] Each story has a clear "As a / I want / so that" and acceptance criteria.
- [ ] Each bug has steps, expected, actual, environment and attachment.
- [ ] Each bug is linked to a story.
- [ ] At least one blocks link exists.
- [ ] You ran and saved at least three JQL filters.

---

## Knowledge Check

**Question 1.** What is a Jira issue, and what does the issue key `QEF-12` tell you?

**Answer:** An issue is a single trackable item of work in Jira (a story, task, bug, epic or sub-task). The key `QEF-12` shows it is issue number 12 in the project with key `QEF`. The key is unique and does not change.

**Question 2.** Put these in hierarchy order, from highest to lowest: Sub-task, Epic, Story.

**Answer:** Epic, Story, Sub-task. (Tasks and Bugs sit at the same level as Stories.)

**Question 3.** Name one difference between team-managed and company-managed projects.

**Answer:** In a team-managed project, the team configures issue types, fields and workflow for that project alone; in a company-managed project, administrators control shared schemes across many projects. Team-managed is simpler; company-managed is more standardised.

**Question 4.** Which issue type fits "Configure the CI job to run smoke tests nightly": Story, Task or Bug? Why?

**Answer:** Task. It is necessary work but not a user-facing feature and not a defect.

**Question 5.** What are the three parts of a user story?

**Answer:** As a (user), I want (goal), so that (benefit).

**Question 6.** What is the difference between acceptance criteria and the Definition of Done?

**Answer:** Acceptance criteria are specific conditions for one story. The Definition of Done is a shared checklist that applies to all stories (for example code reviewed, tests pass, no open critical bugs).

**Question 7.** Rewrite this as Given/When/Then: "User with wrong password should see an error."

**Answer:** Given I have a verified account, When I enter my correct email and a wrong password and click "Log in", Then I see "Incorrect email or password." and remain on the login page.

**Question 8.** Which Jira field holds the defect report's "steps to reproduce," and how should they be formatted?

**Answer:** The Description field, as a numbered list under a heading, starting from a known state, with one action per step.

**Question 9.** Is Severity a default Jira field? What about Priority?

**Answer:** Priority is a default field. Severity is usually a custom field added by an administrator (or not available at all unless added).

**Question 10.** Give an example of a defect with high severity but low priority.

**Answer:** A crash in a rarely used admin report that only one person uses, with a workaround available. The impact is severe but business urgency is low.

**Question 11.** When should you use a component instead of a label?

**Answer:** Use a component for a formal part of the product (for example Registration or Login), since components are predefined and consistent. Use labels for flexible, cross-cutting tags such as `regression` or `smoke`.

**Question 12.** What does "is blocked by" mean, and give an example.

**Answer:** The issue cannot proceed until another issue is finished. Example: "Test registration" is blocked by "Set up test environment."

**Question 13.** You find a bug that already exists. What should you do?

**Answer:** Do not create a new one (or if you did, link it with "duplicates" to the original and close it with a Duplicate resolution). Add any new information as a comment on the original.

**Question 14.** Why prefer vertical slices over horizontal slices when splitting a story?

**Answer:** A vertical slice delivers a thin but complete piece of working functionality through all layers, so it can be tested and demonstrated. A horizontal slice (for example just the database) delivers nothing a user can use or a tester can verify end to end.

**Question 15.** What does SPIDR stand for?

**Answer:** Spike, Paths, Interfaces, Data, Rules.

**Question 16.** How can a QE track test cases in Jira without Xray or Zephyr?

**Answer:** Use acceptance criteria scenarios in the story, sub-tasks for test activities, links to a spreadsheet or Confluence page of detailed test cases, comments recording results per build, and labels such as `qe-verified`.

**Question 17.** Explain this JQL in plain English: `project = QEF AND issuetype = Bug AND assignee IS EMPTY AND statusCategory != Done`.

**Answer:** Show all open (not done) bugs in project QEF that have nobody assigned, which is useful for triage.

**Question 18.** Write a JQL query for bugs reported by you in the last 14 days.

**Answer:** `project = QEF AND issuetype = Bug AND reporter = currentUser() AND created >= -14d`

**Question 19.** What risks come with bulk change?

**Answer:** It modifies many issues at once and may be hard to undo, so wrong filter results or wrong field values can cause widespread damage. Verify the list and the change before confirming and check permissions.

**Question 20.** Name two cautions when using AI features in Jira.

**Answer:** Treat AI output as a draft that you must verify (it may invent details), and follow your organisation's policy on sensitive data. Also, feature availability depends on plan and settings, so check current documentation.

---

## Key Takeaways

- An **issue** is the unit of work in Jira, identified by a unique key and made of fields, a status, comments and history. Newer screens may call issues "work items."
- The default hierarchy is **Epic > Story / Task / Bug > Sub-task**, with possible extra levels above Epic on some plans. Team-managed projects are configured by the team; company-managed by administrators.
- Use **Epics** for big goals, **Stories** for user-facing value, **Tasks** for non-feature work, **Bugs** for defects and **Sub-tasks** for small steps. Spikes are time-boxed investigations.
- A good **story** follows "As a / I want / so that" and includes testable **acceptance criteria**, written as Given/When/Then, a checklist, or both. The **Definition of Done** applies to all stories.
- A good **bug** has a specific summary, environment, numbered steps, expected and actual results, evidence, severity, priority, component and a link to the affected story. Map every defect report element to a Jira field.
- Use Jira's formatting: headings, lists, code blocks, panels and mentions, to make descriptions readable.
- **Link** issues (blocks, relates to, duplicates, tests) to make dependencies and traceability visible; always connect bugs to stories.
- **Priority** is business urgency (default field); **severity** is technical impact (usually a custom field). **Components** are formal product areas; **labels** are flexible tags.
- Estimate with **story points** (relative size) and split big stories into **vertical slices**, using SPIDR as a guide.
- QEs make testing visible through sub-tasks, scenarios in stories, linked test case documents, comments and labels; Xray and Zephyr are optional plugins.
- JQL turns Jira into a question-answering tool: master the field, operator, value pattern and the common functions `currentUser()`, `openSprints()` and relative dates.
- Keep **hygiene**: clear naming, one issue one thing, no duplicates, no sensitive data. Be careful with bulk change, clone and move.
- AI features can help draft and summarise, but you must verify everything; availability varies by plan.
- **Next lesson:** Boards, workflows and customisation, where you will see how issue statuses and boards are configured.

---

## Additional Resources

- **Atlassian Support: Jira Software issues documentation.** Explains issues (work items), issue types, fields and how to create and edit them. Search "Jira Software Cloud issues" at `https://support.atlassian.com/jira-software-cloud/`.
- **Atlassian Agile Coach: User stories.** A clear explanation of what user stories are, how to write them, and examples. `https://www.atlassian.com/agile/project-management/user-stories`
- **Atlassian Support: Use advanced search with Jira Query Language (JQL).** Reference for fields, operators and functions used in the queries in this lesson. Start from `https://support.atlassian.com/jira-software-cloud/` and search for "JQL".

> Reminder: Atlassian updates its documentation and interface regularly. If a link has moved, use the site search with the terms above. Menu names and layouts may differ slightly from the descriptions in this lesson.
