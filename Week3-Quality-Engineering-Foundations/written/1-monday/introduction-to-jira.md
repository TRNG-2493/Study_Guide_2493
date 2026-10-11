# Introduction to Jira

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain what Jira is, why software teams use it, and how it fits into the Atlassian ecosystem.
- Distinguish between Jira Software, Jira Work Management, and Jira Service Management at a high level, and between cloud and data center deployments.
- Define the core Jira vocabulary: project, issue, issue key, issue type, status, priority, assignee, reporter, label, component, version, epic, sprint, backlog, and board.
- Create a Jira account and site, and navigate the main areas of the interface with confidence.
- Create a Scrum project, explain the difference between Scrum and Kanban templates, and explain the difference between team-managed and company-managed projects.
- Create issues in the backlog, plan a sprint, start it, work it with daily updates, complete it, and relate each step to the Scrum ceremonies you studied earlier today.
- Write simple JQL (Jira Query Language) searches and save them as filters.
- Describe what dashboards, burndown charts, and velocity charts show.
- Explain how a Quality Engineer uses Jira day to day.
- Invite teammates and describe basic roles and permissions.
- Apply good habits when writing issues, and recognise common beginner mistakes.
- Set up "Project 1 - QE Foundations" in Jira.

---

## Why This Matters

Earlier today you learned about the Software Development Life Cycle (SDLC), the Software Testing Life Cycle (STLC), Agile roles, and the Scrum ceremonies. Those ideas describe how a team *thinks* and *behaves*. But a team of ten people, working in two-week sprints on dozens of features, cannot keep all of that work in their heads. Somebody has to answer questions like these every single day:

- What are we building this sprint?
- Who is working on which task?
- Has the login feature been tested yet?
- Which bugs are still open, and which are the most serious?
- Are we on track to finish by the end of the sprint?

Jira is where most Agile teams answer those questions. As a Quality Engineer (QE), you will spend a large part of your working day inside Jira: reading user stories before you design tests, creating test tasks, reporting defects, linking those defects to the stories they affect, and giving the team visibility into the quality of the product. Many job descriptions for test automation engineers list Jira as a required tool, and interviewers regularly ask candidates to describe how they have used it.

Think of Jira as the **shared to-do whiteboard for the whole team**. Imagine a large whiteboard in a team room with sticky notes on it. Each note describes a piece of work. The notes are arranged in columns such as "To Do", "In Progress", and "Done". Anyone can walk up, see what is happening, pick up a note, or move one along. Now imagine that whiteboard is available on every team member's laptop, keeps a permanent history of every change, can be searched in a second, can produce charts, and can be shared with colleagues in other countries. That is Jira.

Learning Jira well in your first weeks also pays off for the rest of this programme. Everything you plan, design, and report in Project 1 this week will be tracked in Jira, so the habits you build today will carry forward.

> Note on the user interface: Jira is a cloud product that Atlassian updates frequently. Menu names, icon positions, and screen layouts may differ slightly from the descriptions in this lesson. The concepts stay the same even when the labels change. If you cannot find an option exactly where this lesson says it should be, look for a similarly named option nearby, use the search box at the top of the screen, or check the current Atlassian documentation (links at the end of the lesson).

---

## The Concept

### 1. What Jira Is

**Jira** is a work-tracking tool made by a company called **Atlassian**. Originally it was created to track software bugs (the name comes from "Gojira", the Japanese name for Godzilla), but today it is used to plan, track, and report on almost any kind of work.

In Jira, every piece of work is recorded as an **issue**. An issue is a single item of work: a feature to build, a task to complete, a bug to fix, a test to write. Issues are collected inside a **project**, and projects are displayed on **boards**, **backlogs**, **lists**, and **reports** so that the team can see what is going on.

Why do teams use it? The main reasons are:

| Reason | What it means in practice |
|---|---|
| Single source of truth | Everyone looks at the same list of work, so there is no confusion over which spreadsheet or email thread is correct. |
| Visibility | Managers, developers, testers, and product owners can see the current status of any piece of work at any time. |
| Accountability | Every issue has an assignee (who is doing it) and a reporter (who raised it). |
| History and traceability | Jira records who changed what and when. You can trace a bug back to the story it affects and forward to the fix. |
| Support for Agile | Backlogs, sprints, Scrum boards, Kanban boards, burndown charts, and velocity charts are built in. |
| Searching and reporting | You can find any group of issues with a query and turn the results into dashboards and reports. |
| Integration | Jira connects with source code tools, build tools, chat tools, and test management tools. |

### 2. The Atlassian Ecosystem

Atlassian makes a family of products that are designed to work together. You do not need to learn them all today, but you should recognise the names, because you will meet them on real projects:

| Product | Purpose (high level) |
|---|---|
| Jira | Planning and tracking work (issues, sprints, bugs). |
| Confluence | Team documentation and knowledge sharing (requirements pages, test plans, meeting notes). |
| Bitbucket | Source code hosting and code review (similar in purpose to GitHub). |
| Trello | A simpler, card-based board tool for lightweight task tracking. |
| Loom | Short video messages for explaining work. |
| Rovo and Atlassian Intelligence | AI features that assist with search, writing, and summarising (discussed later in this lesson). |

A very common real-world pattern: requirements are written in Confluence, work items are tracked in Jira, code lives in Bitbucket or GitHub, and everything is linked together.

### 3. Jira Product Families

The word "Jira" is used for several related products. At a high level:

| Product | Who it is mainly for | Typical use |
|---|---|---|
| **Jira Software** | Software and engineering teams | Agile planning with backlogs, sprints, Scrum and Kanban boards, bug tracking, release tracking. This is the product we use in this course. |
| **Jira Work Management** | Business teams such as marketing, HR, finance, and operations | Simple task and project tracking with list, calendar, and timeline views, without software-specific features. Atlassian has been merging these capabilities into the wider Jira product over time, so naming may vary. |
| **Jira Service Management** | IT support, customer support, and service desks | A "request" portal where customers or employees raise tickets, with service-level agreement (SLA) tracking and an incident process. |

Whenever this course says "Jira", it means Jira Software unless stated otherwise.

### 4. Cloud Versus Data Center

Jira can be delivered in two main ways:

- **Cloud**: Atlassian hosts Jira for you. You sign up, get a web address such as `yourname.atlassian.net`, and start working. Updates happen automatically. This is what you will use in this course and is the most common choice today.
- **Data Center**: A company installs and runs Jira on its own servers (or on its own cloud account). The company controls upgrades, security configuration, and data location. Large organisations with strict compliance rules sometimes choose this. Atlassian has announced changes to its self-managed offerings over the years, so check current announcements if this matters to you.

For learning, cloud is the right choice because there is nothing to install.

**Free plan note:** Atlassian has historically offered a free plan of Jira Cloud for small teams, with a limit on the number of users and fewer advanced features. The limits, features, and plan names can change, so check the current pricing page when you sign up. A free plan is normally sufficient for learning and for Project 1.

### 5. Core Vocabulary

Before we click anything, let us define the words you will see on every Jira screen. Read this section slowly. Everything later in the lesson builds on it.

**Project.** A container for a related set of work, such as everything about one product or one team. Our sample project is "QE Foundations". Each project has its own board, backlog, issues, and settings.

**Issue.** One item of work inside a project. Despite the name, an issue is not always a problem. It could be a new feature, a task, a bug, or a test activity. Think of an issue as one sticky note on the whiteboard.

**Issue key.** The unique identifier of an issue, made of the project key, a hyphen, and a number. For example, in a project whose key is QEA, the twelfth issue created is **QEA-12**. The project key is chosen when the project is created (usually two to five capital letters). Issue keys are how teams refer to work in conversation: "Can you review QEA-12?"

**Issue type.** The category of an issue. Common types are Epic, Story, Task, Bug, and Subtask. In brief:

| Issue type | Plain-language meaning |
|---|---|
| Epic | A large body of work that is broken into smaller issues, for example "User Login". |
| Story | A feature described from the user's point of view, for example "As a customer, I want to log in so that I can see my orders". |
| Task | A piece of work that is not a user-facing feature, for example "Prepare test data". |
| Bug | A defect: something that does not work as expected. |
| Subtask | A smaller piece of work that belongs to a parent issue. |

> Depth boundary: this is only an overview. Tomorrow (Tuesday) you will study issue types in detail: how to write good stories, tasks, and bugs, how to write a bug report, and the defect lifecycle.

**Status.** Where an issue currently is in its workflow. Typical statuses are To Do, In Progress, and Done. On a board, each status is a column.

**Workflow.** The set of statuses an issue can pass through and the allowed moves between them. (Workflows and board customisation are taught in depth on Tuesday; today we use the defaults.)

**Priority.** How urgent or important an issue is. Jira's default scale is usually Highest, High, Medium, Low, and Lowest. Priority answers the question "How soon should we deal with this?"

**Assignee.** The person currently responsible for doing the work on the issue.

**Reporter.** The person who created the issue. The reporter and the assignee are often different people, for example a tester reports a bug and a developer is assigned to fix it.

**Labels.** Free-text tags you attach to issues to group them informally, for example `regression`, `smoke`, or `login`. You can type any label, so agree on naming conventions with your team to avoid `Regression`, `regression`, and `regresion` all existing separately.

**Components.** Named parts of a product within a project, such as "Checkout", "Search", or "Admin Portal". Components are usually set up by a project administrator and chosen from a list, which makes them more controlled than labels.

**Versions (releases).** A named release of the product, for example "1.0" or "2025.03". An issue can record which version it was found in (affects version) and which version it will be fixed in (fix version). This helps teams answer "What is in the next release?"

**Epic.** A large piece of work that is broken down into several smaller issues. For example, the epic "User Authentication" might contain stories for registration, login, and password reset.

**Sprint.** A fixed time-box, commonly one to four weeks, in which the team commits to completing a chosen set of issues. You studied sprints in the Scrum lesson earlier today. In Jira, a sprint is a container that holds the issues selected for that period.

**Backlog.** The ordered list of work that has been identified but not yet scheduled into a sprint. The product owner orders it by importance. In Jira, the Backlog view shows the backlog beneath any current and future sprints.

**Board.** A visual display of issues arranged in columns by status. A Scrum board shows the issues of the active sprint. A Kanban board shows a continuous flow of work.

Here is a quick picture of how these pieces relate:

```
Project: QE Foundations (key: QEA)
 |
 +-- Epic: User Login
 |     +-- Story QEA-3: Log in with email and password
 |     +-- Story QEA-4: Reset a forgotten password
 |     +-- Task  QEA-5: Prepare test accounts
 |     +-- Bug   QEA-9: Login accepts an empty password
 |
 +-- Backlog (work not yet in a sprint)
 |
 +-- Sprint 1 (work the team has committed to now)
 |
 +-- Board (visual view of Sprint 1 work by status)
```

### 6. Creating an Account and a Site

To use Jira Cloud you need an Atlassian account and a **site**. The site is your team's private Jira space, with its own address.

Step by step (screen names may vary):

1. Open a web browser and go to the Atlassian website. Find the Jira product page and choose the option to get Jira free or to try it.
2. Sign up with your work or personal email address, or with a Google or Microsoft account. Use an address you will still have access to later, and one that you are comfortable using for professional learning.
3. Verify your email address if you are asked to. Atlassian typically sends a confirmation message.
4. When asked to choose a product, select **Jira** (Jira Software). If you are asked what kind of work you do, choose the software development option.
5. Choose a **site name**. This becomes your web address, for example `qea-yourname.atlassian.net`. Site names must be unique, so you may need to try a few variations. Pick something professional.
6. If you are prompted to pick a plan, choose the free option for learning (check what is currently offered).
7. Answer any short setup questions (team size, kind of work) and continue. Atlassian may offer to create a sample project or a first project for you. You will create your own project in a later section.
8. Bookmark your site address. You will return to it every day.

### 7. Navigating the Interface

When you first sign in, you land on a home page that may show recent work and shortcuts. Jira's layout has three main regions: the **top navigation bar** across the top, a **sidebar** down the left, and the **main content area**.

```
+--------------------------------------------------------------------------+
| [Apps grid] Jira | Your work | Projects | Filters | Dashboards | [Create] |
|                                     [Search...]   [?] [Bell] [Settings] [You]|
+----------------+---------------------------------------------------------+
| Project name   |                                                         |
|  Planning      |                  MAIN CONTENT AREA                      |
|   Summary      |        (backlog, board, issue list, reports)            |
|   Backlog      |                                                         |
|   Board        |                                                         |
|   List         |                                                         |
|   Timeline     |                                                         |
|  Development   |                                                         |
|   Reports      |                                                         |
|   Issues       |                                                         |
|   Project      |                                                         |
|    settings    |                                                         |
+----------------+---------------------------------------------------------+
```

This sketch is a simplification. Your screen may place or label items differently.

Here is a table of where things are and what they are for:

| Area | Where to find it | What it is for |
|---|---|---|
| App switcher (grid icon) | Top left | Jump between Atlassian products on your site (Jira, Confluence, and others). |
| Your work | Top navigation bar | A personal home for issues assigned to you, issues you worked on recently, and items you viewed. Use it at the start of each day. |
| Projects | Top navigation bar | Lists your recent and starred projects and lets you browse all projects or create a new one. |
| Filters | Top navigation bar | Your saved searches. You can open, create, or manage filters here. |
| Dashboards | Top navigation bar | Pages of gadgets (charts and lists) that summarise project information. |
| Create button | Top navigation bar (often a blue button) | Opens the form to create a new issue in any project. A keyboard shortcut, the letter C, may also work when you are not typing in a text box. |
| Search | Top navigation bar | Quick search for issues, projects, boards, and people. Also the entry point to advanced searching with JQL. |
| Notifications (bell) | Top right | Shows updates about issues you watch, own, or are mentioned in. |
| Settings (gear) | Top right | Personal settings and, if you are an administrator, project and site settings. |
| Profile (your avatar) | Top right | Account settings, personal preferences, and sign out. |
| Project sidebar | Left side, when inside a project | Switches between the project's views: Summary, Backlog, Board, List, Timeline, Reports, and Project settings. |

Take two minutes now to click through each top-level menu. Nothing you click while exploring will break anything.

### 8. Creating a Project

A project is where your team's work lives. Before creating one you should understand two choices: the **template** and the **project type**.

#### Scrum template versus Kanban template

| Feature | Scrum template | Kanban template |
|---|---|---|
| Working style | Work is done in fixed-length sprints. | Work flows continuously with no fixed iterations. |
| Planning | Sprint planning selects issues from the backlog into a sprint. | Issues are pulled onto the board as capacity allows. |
| Key views | Backlog, Active Sprint board, reports such as burndown and velocity. | Board with columns, and often a backlog that is optional. |
| Main control | Sprint scope (the team commits to a set amount of work). | Work in progress (WIP) limits, which cap how many items can be in a column at once. |
| Best for | Teams building products in planned increments, like the one in our Scrum ceremonies lesson. | Support teams, maintenance work, or teams with a steady stream of unpredictable requests. |

This course uses the **Scrum template**, because it matches the Scrum ceremonies you learned today.

#### Team-managed versus company-managed

Jira offers two project "styles". In simple terms:

| Aspect | Team-managed | Company-managed |
|---|---|---|
| Who controls the settings | The team itself. Anyone with the project administrator role can change the project. | Jira administrators for the whole site. |
| Setup effort | Quick and simple. | More configuration options, more complexity. |
| Customisation | Each project has its own issue types, workflows, and fields, and changes do not affect other projects. | Settings (workflows, fields, screens) can be shared across many projects for consistency. |
| Best for | Small teams, new teams, and learning. | Larger organisations needing standard processes and reporting across many teams. |
| Some terminology | You may see "classic" and "next-gen" in older material. Team-managed was formerly called "next-gen". | Formerly called "classic". |

Names and the availability of some features differ between the two, so you may see slight variations in what menus offer. For Project 1 we use a **team-managed Scrum project** because it is quick to set up and you will be the administrator.

#### Step by step: create the project

1. From the top navigation bar, open **Projects** and select **Create project**. (If you are brand new to the site, you may be guided to this screen automatically.)
2. Choose **Scrum** from the list of templates. A description appears explaining that it is for teams that work in sprints.
3. Select **Use template**.
4. Choose the project type, **Team-managed** (or the option labelled as simple or team-controlled in your version).
5. Give the project a **Name**: type `QE Foundations`.
6. Check the **Key**. Jira suggests one based on the name. Change it to `QEA` so your issue keys look like QEA-1, QEA-2, and so on. Keys are usually hard or impossible to change later in some project types, so choose carefully.
7. Review the access setting. For learning, the default (members of the project only, or similar) is fine.
8. Select **Create** or **Next** until Jira finishes. You land on the project, usually on the Backlog or Board view.

### 9. The Backlog View and Creating Your First Issues

Open the project and choose **Backlog** in the sidebar. The Backlog view has two main sections:

- At the top, one or more **sprint panels** (for example "QEA Sprint 1"), which hold issues the team plans to do in that sprint.
- Below, the **Backlog** panel, which holds issues not yet assigned to a sprint.

```
+--------------------------------------------------------------+
| QEA Sprint 1                  0 issues   [Start sprint]      |
|   (empty: drag issues here during sprint planning)           |
+--------------------------------------------------------------+
| Backlog                       4 issues   [Create sprint]     |
|   [S] QEA-1  Register a new account            TO DO   (SJ)  |
|   [S] QEA-2  Log in with email and password    TO DO   (SJ)  |
|   [T] QEA-3  Prepare test accounts             TO DO   ( )   |
|   [S] QEA-4  Reset a forgotten password        TO DO   ( )   |
|   + Create issue                                             |
+--------------------------------------------------------------+
   [S] = Story, [T] = Task, (SJ) = assignee avatar
```

#### Creating issues quickly in the backlog

1. In the Backlog panel, select **+ Create issue** at the bottom.
2. Choose the issue type from the small drop-down (for example Story or Task).
3. Type a short **summary**, which is the issue title, such as `Register a new account`.
4. Press Enter. The issue is created and receives the next key (for example QEA-1). Keep typing to add more.

#### Creating an issue with the full form

Use the **Create** button in the top navigation bar when you want to fill in more details. The form usually offers:

- **Project** and **Issue type**.
- **Summary** (required): the title.
- **Description**: the detail, using a rich-text editor.
- **Assignee** and **Reporter**.
- **Priority**.
- **Labels** and **Components**.
- **Attachments**, for screenshots or documents.
- **Parent** (for example, an epic).
- **Sprint**.

Fill in what you know and select **Create**. A small confirmation appears with the new issue key, and you can click it to open the issue.

#### The issue detail view

Opening an issue shows a detail screen. On the left you see the summary, description, child issues, links, and a comments and history area. On the right you see status, assignee, reporter, priority, labels, sprint, and other fields. You can change most fields by clicking them. The **status** drop-down at the top moves the issue through the workflow, for example from To Do to In Progress.

#### Ranking the backlog

The backlog is an ordered list. The issues at the top are the most important and will be picked first. You can drag an issue up or down to change its order. Usually the Product Owner is responsible for this order, but QEs and developers often help by explaining risks and effort.

### 10. A First Look at the Boards

#### Scrum board

When a sprint is active, the **Board** view shows the sprint's issues as cards arranged in columns by status.

```
 QEA board - QEA Sprint 1                      (5 days remaining)
+-----------------+-------------------+-----------------+
| TO DO           | IN PROGRESS       | DONE            |
+-----------------+-------------------+-----------------+
| +-------------+ | +---------------+ | +-------------+ |
| | QEA-2       | | | QEA-1         | | | QEA-3       | |
| | Log in with | | | Register a    | | | Prepare     | |
| | email and   | | | new account   | | | test        | |
| | password    | | |         (SJ)  | | | accounts    | |
| |        (AK) | | +---------------+ | |        (SJ) | |
| +-------------+ |                   | +-------------+ |
|                 |                   |                 |
+-----------------+-------------------+-----------------+
```

Each card shows the issue key, summary, assignee avatar, and often priority and type icons. To change an issue's status, **drag the card** to another column or open the issue and use the status drop-down.

Team members update the board during the day, so at the Daily Scrum anyone can look at it and see the real situation.

#### Kanban board

A Kanban board looks similar but has no sprint. Work flows continuously from left to right. Columns may have **WIP limits**, shown as a number in the column header, so that the team does not start too many things at once.

```
+----------------+----------------------+---------------+
| BACKLOG        | IN PROGRESS (max 3)  | DONE          |
+----------------+----------------------+---------------+
| QEA-8          | QEA-5                | QEA-1         |
| QEA-9          | QEA-6                | QEA-2         |
| QEA-10         | QEA-7                |               |
+----------------+----------------------+---------------+
```

> Depth boundary: board customisation (adding columns, changing swimlanes, quick filters) and workflows are taught in depth on Tuesday. Today you only need to read a board and move cards.

### 11. Running a Sprint in Jira

Earlier today you learned the sprint lifecycle and the Scrum ceremonies. Jira supports each one. The table links the ceremonies to what you do in Jira:

| Scrum ceremony or event | What happens in Jira |
|---|---|
| Backlog refinement | Add detail, estimates, and acceptance criteria to backlog issues, and rank them. |
| Sprint planning | Create the sprint, drag selected issues into it, set the sprint goal and dates, then start the sprint. |
| Daily Scrum | The team looks at the board, updates the status of cards, assigns work, and adds comments about blockers. |
| Sprint review | The team demonstrates completed work and checks the Done column and sprint report. |
| Sprint retrospective | The team reflects on the sprint, often using sprint report data to see what was finished or not. |

#### Step by step: plan and start a sprint

1. Open the **Backlog** view.
2. Make sure the backlog is in priority order, and that issues have summaries, descriptions, and, ideally, estimates (this is **sprint planning** preparation).
3. If no sprint exists, select **Create sprint** to make an empty one. A project often starts with "QEA Sprint 1" already present.
4. **Drag issues** from the Backlog panel into the sprint panel. Choose only as much work as the team believes it can finish in the sprint.
5. Select **Start sprint** in the sprint panel.
6. In the dialog, check the **Sprint name** (for example, "Sprint 1"), the **Duration** (commonly two weeks) or custom start and end dates, and the **Sprint goal**, a short sentence describing what the sprint should achieve. An example is "Users can register and log in".
7. Select **Start**. Jira opens the **Board**, which now shows the sprint's issues in the To Do column.

#### Daily updates during the sprint

Each day, usually around the Daily Scrum:

1. Open the **Board**.
2. Move a card to **In Progress** when you start working on it.
3. Add **comments** to issues when you have progress, questions, or blockers. Use the @ symbol followed by a name to mention a teammate and notify them.
4. Move a card to **Done** only when it meets the team's Definition of Done. For a QE this means the testing for that item has been completed as agreed.
5. Look for cards that have been stuck in one column for several days. They need a conversation.

If new work appears mid-sprint, the team discusses it. New urgent bugs may be added; but adding too much work mid-sprint is a habit to avoid, since it breaks the commitment made at sprint planning.

#### Step by step: complete a sprint

1. At the end of the sprint, open the **Board** and select **Complete sprint** (usually in the top right).
2. Jira shows how many issues are **Done** and how many are **open**.
3. Choose where unfinished issues go. They can move to the **Backlog** or to the **next sprint**. Do not delete or pretend they are done.
4. Select **Complete**. The sprint is closed and a **sprint report** becomes available under Reports.
5. Use the report and the board in the **Sprint review**, then move on to the **Sprint retrospective**.

### 12. Searching with JQL

As projects grow, scrolling through lists stops being practical. **JQL** (Jira Query Language) is Jira's way of asking for exactly the issues you want. It looks like a mix of plain English and simple logic.

A JQL query is built from:

- A **field** (such as `project`, `status`, `assignee`, `priority`, `issuetype`, `labels`).
- An **operator** (such as `=`, `!=`, `IN`, `~`, `>`).
- A **value** (such as `QEA`, `"To Do"`, `currentUser()`).
- Optional keywords `AND`, `OR`, `NOT`, and `ORDER BY` to combine and sort.

Values with spaces go in double quotes.

**How to run a query:** open **Filters** (or **Search**), choose **View all issues** or **Advanced issue search**, switch to **JQL** mode if you see a Basic/JQL toggle, type the query, and press Enter or select **Search**. (Navigation names can vary.)

Seven gentle examples:

```jql
project = QEA
```
Finds every issue in the project with key QEA. This is the simplest possible query and a good first test.

```jql
project = QEA AND status = "To Do"
```
Finds issues in project QEA that have not been started. Because "To Do" has a space, it is in quotes.

```jql
project = QEA AND assignee = currentUser()
```
Finds issues in QEA that are assigned to you. `currentUser()` is a built-in function that means "whoever is logged in".

```jql
project = QEA AND issuetype = Bug AND status != Done
```
Finds bugs that are not yet finished. The `!=` operator means "is not equal to". This is one of the most useful searches for a QE.

```jql
project = QEA AND priority IN (Highest, High) ORDER BY created DESC
```
Finds high-priority and highest-priority issues, with the newest first. `IN` accepts a list of values, and `ORDER BY` sorts the results.

```jql
project = QEA AND labels = regression
```
Finds issues tagged with the label `regression`. Labels are matched by their exact text.

```jql
project = QEA AND summary ~ "login" AND created >= -14d
```
Finds issues in QEA whose title contains the word "login" and that were created in the last 14 days. The `~` operator means "contains (text search)", and `-14d` means "14 days ago".

```jql
project = QEA AND sprint in openSprints() AND issuetype = Bug ORDER BY priority DESC
```
Finds bugs in the sprint that is currently running, with the most urgent first. `openSprints()` is a function representing active sprints.

Tips for learning JQL:

- Start with a simple query and add one condition at a time.
- Jira's search box suggests field names and values as you type, which helps avoid typing mistakes.
- Status and priority names depend on your project's setup, so if a query returns nothing, check the exact spelling.
- Advanced JQL (functions, history searches, and more) can be learned later. These queries will cover most of your first month.

### 13. Filters, Dashboards, and Reports

#### Filters

A **filter** is a saved search. After you run a query that you will need again, select **Save as** and give it a name such as "QEA - Open Bugs". Saved filters appear under **Filters** in the top navigation bar. Filters can be shared with colleagues, used as the basis of dashboard gadgets, and used to drive some board features.

#### Dashboards

A **dashboard** is a customisable page of **gadgets**, small panels that each show one piece of information. Examples of gadgets include a list of issues from a filter, a pie chart of issues by status, or a count of bugs by priority. A QE might build a dashboard called "Quality Overview" with:

- Open bugs by priority.
- Bugs created over the last 30 days.
- Test tasks still in progress.
- Issues assigned to me.

To create one: open **Dashboards**, select **Create dashboard**, give it a name, add gadgets, and configure each gadget (usually by choosing a filter). Dashboards can be shared with the team so that stakeholders can check quality without asking anyone.

#### Basic reports

Under **Reports** in the project sidebar, Scrum projects offer built-in charts. Two you should know:

| Report | What it shows | How to read it |
|---|---|---|
| **Burndown chart** | The amount of work remaining in a sprint over time, compared with an ideal straight line from the start to zero. | If the actual line stays above the ideal line, the team may be behind. If it drops sharply at the end, work may have been left until the last day, which is a warning sign. |
| **Velocity chart** | The amount of work (often story points) the team committed to and completed in each of the last several sprints. | Over a few sprints, the team learns how much it typically completes. This helps with future sprint planning. |

Other reports exist (such as sprint report, cumulative flow diagram, and created versus resolved issues). Their names and availability depend on your project type and plan. Reports are only as good as the data in them: if people forget to update statuses, the charts will mislead everyone.

### 14. How a Quality Engineer Uses Jira

Quality work is visible in Jira only if you put it there. Typical QE activities:

| QE activity | How it appears in Jira |
|---|---|
| Reviewing requirements | You read user stories and acceptance criteria, and comment with questions or concerns before development starts. |
| Planning testing | You create Task issues such as "Design test cases for QEA-2" or "Prepare test data" and add them to the sprint, so testing effort is visible and counted in planning. |
| Tracking test progress | You move your test tasks across the board, and you update the status of stories when testing is done. |
| Reporting defects | You create Bug issues with clear steps to reproduce, and link them to the story they relate to. (Bug writing is covered tomorrow.) |
| Linking | You use the **Link issue** option to connect, for example, a bug to a story with a "relates to" or "is caused by" style link (link names vary). This gives **traceability**: the ability to follow a requirement to its tests and defects. |
| Verifying fixes | You retest bugs that developers marked as fixed, and then close them or reopen them with a comment. |
| Giving visibility | You build filters and dashboards that show open bugs, bugs by severity, and testing status for the team and managers. |
| Supporting release decisions | You search for open high-priority bugs in a version to help the team decide whether a release is ready. |

Because Jira is shared by the whole team, a QE who keeps tickets accurate gives the team early warning about risk. That is what "visibility" means in practice.

### 15. Inviting Users and Basic Permissions

A Jira project is only useful when your team is in it.

#### Inviting people

1. In the project sidebar, open **Project settings**, then **Access** (or **People**), depending on your project type.
2. Select **Add people**.
3. Enter the person's email address or name.
4. Choose a **role** for them.
5. Select **Add** or **Send invite**. They receive an email and can join.

(For site-wide invitations you may instead use the administration area of your site, where users and groups are managed. Your plan may limit how many users you can invite.)

#### Roles and permissions overview

A **role** is a set of permissions for a person within a project. The names vary by project type, but the idea is similar:

| Role (typical name) | What the person can usually do |
|---|---|
| Administrator | Change project settings, manage people, configure the board and workflow. |
| Member | Create issues, edit issues, comment, and move work across the board. |
| Viewer | See issues and comments, but not change them. |

Companies often use a more detailed permission setup (called permission schemes) in company-managed projects, which is managed by Jira administrators. As a learner, you only need to understand that not everyone can do everything, and that if you cannot see a button, you may lack permission and should ask the project administrator.

### 16. A Note on Jira's AI Features

Atlassian has been adding artificial intelligence features to its products, marketed under names such as **Atlassian Intelligence** and **Rovo**. Depending on your plan, region, and the date you read this, these features may help with tasks such as:

- Summarising a long issue and its comments.
- Suggesting a rewrite or improving the wording of an issue description.
- Searching across Jira, Confluence, and connected tools using natural language.
- Helping to draft a query, sometimes turning plain-English questions into JQL.
- Suggesting how to break a large issue into smaller pieces.

Please treat this list as a general picture, not a promise. Availability, naming, limits, and pricing may vary by plan and can change, so **check the current Atlassian documentation** for what is available on your site. When you do use AI suggestions, remember that you remain responsible for the result: read what the AI produces, check it against your actual requirements, and never paste confidential company data into any tool unless your organisation allows it. This theme returns throughout the course: AI is a helpful assistant for a Quality Engineer, not a substitute for judgement.

### 17. Good Habits

A tracker is only as useful as the information inside it. Build these habits from your first day.

**Write clear titles (summaries).** A title should let a teammate understand the issue without opening it.

| Weak title | Stronger title |
|---|---|
| Login broken | Login fails with "Invalid request" error when password contains a plus sign |
| Test stuff | Design test cases for user registration (QEA-1) |
| Fix bug | Correct validation message for empty email field on registration page |
| Search | As a shopper, I can search products by name |

**Write useful descriptions.** Explain the context: what is needed, why, and any constraints. For a bug, include steps to reproduce, expected result, and actual result (details tomorrow).

**Include acceptance criteria.** Acceptance criteria are the specific conditions that must be true for the work to be considered complete. They remove guesswork for developers and give testers something concrete to verify. A simple, readable format is a checklist or a Given/When/Then pattern. For example, for QEA-2, "Log in with email and password":

```
Acceptance criteria
- Given a registered user, when they enter a correct email and password,
  then they are taken to the home page.
- Given a registered user, when they enter an incorrect password,
  then an error message is shown and they stay on the login page.
- Given an empty email field, when the user selects Log in,
  then a message asks them to enter an email address.
```

**Keep statuses honest.** Update the card as soon as the real situation changes. A board that is out of date is worse than no board.

**Use comments, not side channels.** Record decisions and questions on the issue so that everyone, including future team members, can see them.

**Link related work.** Connect bugs to stories, tasks to epics, and duplicates to each other.

**Search before you create.** Run a quick search to check that a similar issue does not already exist.

**Be consistent with labels and components.** Agree on naming and stick to it.

### 18. Common Beginner Mistakes

| Mistake | Why it is a problem | What to do instead |
|---|---|---|
| Vague titles such as "Bug" or "Issue with page" | Others cannot tell what it is about, and searching becomes hard. | Write a specific summary that names the feature and the symptom. |
| Leaving the description empty | Developers must ask for details, which wastes time. | Provide context, steps, and expected results. |
| Forgetting to update the status | The board and reports show a false picture. | Move cards when work starts and finishes. |
| Putting a whole feature in one giant issue | It cannot be finished in a sprint and progress is invisible. | Break it into smaller stories and tasks. |
| Creating duplicates without searching | Effort is split and confusion grows. | Search first, and link duplicates if they occur. |
| Assigning everything to yourself, or to nobody | Ownership is unclear. | Assign each issue to the person actually doing it. |
| Setting every priority to Highest | When everything is urgent, nothing is. | Use priority honestly and agree on definitions with the team. |
| Moving a card to Done before testing is complete | Quality gaps reach the customer. | Check the Definition of Done first. |
| Adding lots of work to a running sprint | The sprint commitment is broken. | Discuss with the team, and only add truly urgent work. |
| Using many inconsistent labels | Searches miss issues. | Agree on a small set of label names. |
| Closing a sprint without moving unfinished work deliberately | Work is lost or hidden. | Decide on each unfinished item and move it with a reason. |
| Being afraid to explore | Learning stalls. | Use a practice project; you cannot break anything important. |

---

## Examples

### Example 1: A day in Jira for a QE

Aisha is the QE on a team building an online shop. Here is her morning:

1. She opens **Your work** and sees two issues assigned to her: QEA-6 (Design test cases for checkout) and QEA-9 (a bug awaiting retest).
2. At the Daily Scrum, she looks at the board. QEA-5, the checkout story, has just moved to In Review. She tells the team she will test it today.
3. She opens QEA-9. The developer has commented that the bug is fixed. She retests it using the steps in the description. It passes, so she adds a comment "Verified on build 1.2.4, fixed" and moves it to Done.
4. While testing QEA-5, she finds that the discount code field accepts negative numbers. She selects **Create**, picks the issue type **Bug**, writes a clear summary, "Discount code field accepts negative values at checkout", adds steps and a screenshot, sets priority to High, and links the bug to QEA-5 using **Link issue**.
5. She runs this JQL to see the whole picture and saves it as a filter named "Sprint 1 open bugs":

```jql
project = QEA AND issuetype = Bug AND sprint in openSprints() AND status != Done
```

6. She adds this filter to the team's dashboard so the product owner can follow quality without needing to ask.

### Example 2: From story to test task to bug

Consider the story **QEA-2: Log in with email and password**.

```
QEA-2  Story: Log in with email and password           (Sprint 1)
  |-- QEA-6  Task: Design test cases for QEA-2         (assignee: QE)
  |-- QEA-7  Task: Automate smoke test for login       (assignee: QE)
  '-- QEA-9  Bug:  Login accepts an empty password     (linked to QEA-2)
```

Anyone opening QEA-2 can see the testing tasks and the related bug. This traceability means the team can answer "Is login ready?" by looking at one screen.

### Example 3: Reading the burndown chart

Imagine a two-week sprint with 20 story points. By day 5, the burndown shows 18 points remaining, but the ideal line says there should be about 13. Two things might be going on: the work is being completed more slowly than planned, or cards are being finished but not moved to Done. Either way, the chart gives the team a reason to talk early rather than discover a problem on the last day. The right response is a conversation, not blame.

---

## Knowledge Check

Try to answer each question in your own words before reading the answer.

**1. In one sentence, what is Jira?**
Answer: Jira is Atlassian's tool for planning, tracking, and reporting on work, where each item of work is recorded as an issue in a project.

**2. What is the difference between an issue and an issue key?**
Answer: An issue is one item of work. The issue key is its unique identifier, made of the project key and a number, such as QEA-12.

**3. Which Jira product would a company's IT help desk most likely use, and which would a software team use?**
Answer: The help desk would likely use Jira Service Management. A software team would use Jira Software.

**4. What is the difference between cloud and data center?**
Answer: Cloud is hosted and maintained by Atlassian. Data center is installed and managed by the customer's own organisation on its own infrastructure.

**5. What is the difference between a label and a component?**
Answer: A label is a free-text tag anyone can type, used for informal grouping. A component is a named part of the product, normally set up by an administrator and selected from a list.

**6. How do the backlog and the sprint relate?**
Answer: The backlog is the ordered list of work not yet scheduled. At sprint planning, the team selects issues from the backlog and moves them into a sprint, which is a time-boxed set of work.

**7. Which Scrum ceremony corresponds to dragging issues into a sprint and selecting Start sprint?**
Answer: Sprint planning.

**8. What should you decide when you complete a sprint that still has unfinished issues?**
Answer: Where each unfinished issue should go: back to the backlog or into the next sprint. They should be moved deliberately, not hidden or marked Done.

**9. What does this query return?**
`project = QEA AND issuetype = Bug AND status != Done`
Answer: All bugs in project QEA that are not yet in the Done status.

**10. What does the burndown chart show, and what does the velocity chart show?**
Answer: The burndown chart shows work remaining in a sprint over time. The velocity chart shows how much work the team completed in each past sprint, which helps future planning.

**11. Give two ways a QE uses Jira beyond reporting bugs.**
Answer: Examples include creating test tasks so testing effort is visible, reviewing and commenting on stories before development, linking bugs to stories for traceability, building filters and dashboards for visibility, and verifying fixes.

**12. Why should you check current documentation when you read about Jira's AI features?**
Answer: Because the features, names, availability, and limits can differ by plan and change over time. You should also review any AI output before relying on it.

**13. Rewrite this weak title so it is useful: "Search is broken".**
Answer: A stronger version names the feature and the symptom, for example "Product search returns no results when the query contains an apostrophe".

---

## Try It: Set Up Project 1 in Jira

In this activity you will create and configure the Jira project for "Project 1 - QE Foundations", the sample web app you will plan quality for this week. Work through the checklist in order and tick off each step. Remember that menu labels may differ slightly from those described here.

**Checklist**

1. [ ] **Create or sign in to your Atlassian account.** Go to the Atlassian website, sign up for Jira (the free option is fine for learning), and verify your email address.
2. [ ] **Create your site.** Choose a professional site name such as `qea-yourname`. Write the address down.
3. [ ] **Explore the top navigation bar.** Open **Your work**, **Projects**, **Filters**, and **Dashboards** once each. Find the **Create** button and the **Search** box.
4. [ ] **Create a project.** Select **Projects**, then **Create project**. Choose the **Scrum** template, then the **Team-managed** project type.
5. [ ] **Name and key.** Name the project `QE Foundations` (or your own variation such as "Project 1 - QE Foundations") and set the key to `QEA`.
6. [ ] **Open the Backlog.** From the sidebar, select **Backlog** and identify the sprint panel and the backlog panel.
7. [ ] **Create an epic.** Create an epic named `User Authentication`. (If you do not see an Epic panel, use the **Create** button and choose Epic as the issue type.)
8. [ ] **Create at least five issues** using **+ Create issue** in the backlog. Use meaningful titles, such as:
   - `Register a new account` (Story)
   - `Log in with email and password` (Story)
   - `Reset a forgotten password` (Story)
   - `Prepare test accounts and test data` (Task)
   - `Design test cases for user registration` (Task)
9. [ ] **Add detail to two issues.** Open two of them and add a description and a short list of acceptance criteria (use the Given/When/Then example from this lesson as a guide). Set a priority on each.
10. [ ] **Attach issues to the epic.** Open each authentication issue and set its **Parent** to the `User Authentication` epic.
11. [ ] **Add a label.** Give at least one issue the label `smoke` and another the label `registration`, practising consistent naming.
12. [ ] **Rank the backlog.** Drag the issues into the order you think is most important, and be ready to explain why.
13. [ ] **Plan Sprint 1.** Drag three or four issues into the sprint panel. Include at least one test-related Task.
14. [ ] **Start the sprint.** Select **Start sprint**, set a duration of one week (or as your instructor says), and enter a sprint goal such as "Users can register and log in with verified test coverage".
15. [ ] **Open the board.** Confirm the cards appear in To Do. Assign yourself as the assignee on each card you are working on.
16. [ ] **Simulate daily updates.** Move one card to In Progress, add a comment with a status update, and then move it to Done. Repeat for another card if time allows.
17. [ ] **Run three JQL searches** in advanced search and note the results:
    ```jql
    project = QEA
    ```
    ```jql
    project = QEA AND status = "To Do"
    ```
    ```jql
    project = QEA AND assignee = currentUser()
    ```
18. [ ] **Save a filter.** Save one of your queries as a filter named `QEA - My Open Work`.
19. [ ] **Look at a report.** Open **Reports** in the sidebar and find the burndown chart. Note that it may be nearly flat on day one, which is normal.
20. [ ] **Invite a teammate.** Go to **Project settings**, then **Access** (or **People**), and invite a classmate or your instructor with the Member role, if your instructor asks you to.
21. [ ] **Complete the sprint.** When directed (or at the end of the simulation), select **Complete sprint**. Move unfinished issues to the backlog, then view the sprint report.
22. [ ] **Reflect.** Write three sentences in your own notes: what felt easy, what felt confusing, and one thing you will do differently in the next sprint.

**Stretch goal.** Create a dashboard named "QEA Overview" and add one gadget that displays a list of issues from your saved filter.

**Success check.** You are done when you can show that (a) your project key is QEA, (b) you have at least five well-titled issues with an epic, (c) a sprint has been started with a goal, (d) at least one card has moved across the board, and (e) you have one saved filter. Keep this project, because you will keep using it for the rest of the week.

> Pointer: tomorrow (Tuesday) you will go deeper into issue types, writing excellent bug reports, the defect lifecycle, workflows, and board customisation. Your project today is the foundation for those lessons.

---

## Key Takeaways

- Jira is a shared, searchable, always-current to-do whiteboard for the whole team. It is the central place where Agile work is planned and tracked.
- Everything is an **issue** inside a **project**, identified by an **issue key** such as QEA-12.
- Know the vocabulary: status, priority, assignee, reporter, label, component, version, epic, sprint, backlog, and board.
- Jira Software is for software teams. Work Management and Service Management serve other needs. Cloud is hosted by Atlassian, while Data Center is self-managed.
- For this course, use a team-managed Scrum project with the key QEA.
- The Jira sprint flow mirrors the Scrum ceremonies: refine and plan the backlog, start the sprint, update the board daily, complete the sprint, and use the results in review and retrospective.
- JQL lets you find exactly the issues you want. Start with simple queries and save the useful ones as filters.
- Dashboards and reports such as burndown and velocity turn Jira data into visibility, but only if the data is kept honest.
- A Quality Engineer uses Jira to track test tasks, report and link bugs, verify fixes, and keep quality visible.
- Good habits matter: clear titles, helpful descriptions, acceptance criteria, honest statuses, and linked work.
- AI features such as Atlassian Intelligence and Rovo may help, but features vary by plan, so check current documentation and always review the output.
- Menu names and layouts change over time. Focus on the concepts and use search and documentation when the screen looks different.
- Issue types, bug reports, defect lifecycle, workflows, and board customisation continue in depth on Tuesday.

---

## Additional Resources

- Atlassian Jira Software documentation (official guides for projects, boards, sprints, and JQL): https://support.atlassian.com/jira-software-cloud/
- Atlassian Agile Coach (articles on Scrum, Kanban, sprints, and how Jira supports them): https://www.atlassian.com/agile
- Atlassian University / Atlassian Learning (free introductory courses and tutorials; availability of specific courses may change): https://university.atlassian.com/

Since these sites are updated regularly, use their search boxes for the latest articles on topics such as "create a Scrum project", "JQL basics", and "Jira dashboards".
