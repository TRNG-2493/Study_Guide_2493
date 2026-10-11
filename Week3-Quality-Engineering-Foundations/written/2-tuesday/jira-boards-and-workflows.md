# Jira Boards and Workflows

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain what a Jira board is and distinguish a Scrum board from a Kanban board.
- Identify and describe every part of a board: columns, swimlanes, quick filters, cards, backlog, active sprint, epics panel and versions.
- Configure a board: map statuses to columns, create swimlanes, write quick filters with JQL, adjust card layout and colors, set estimation and working days, and apply WIP limits on a Kanban board.
- Manage a backlog by ranking issues, and run a full sprint: create, start, add or remove issues, move incomplete work, complete the sprint and read the sprint report.
- Explain Kanban flow metrics in plain language: cumulative flow diagram, control chart, cycle time and lead time.
- Read the main Jira reports (burndown, burnup, velocity, sprint report, created vs resolved) and build a simple QE dashboard of bugs by priority and status.
- Define a workflow (statuses, transitions, resolutions, status categories) and compare Jira's default workflow with a custom workflow.
- Design a Bug workflow that maps every state from the defect lifecycle lesson, and a Story workflow that includes a QA stage.
- Describe transition features (conditions, validators, post functions, screens), permissions, workflow schemes and issue type schemes at an overview level.
- Describe the difference between team-managed and company-managed projects and which tasks need administrator rights.
- Write a simple Jira Automation rule (trigger, condition, action) and describe how notifications work.
- Enforce a Definition of Done through workflow design, recognize workflow best practices and anti-patterns, and plan a migration from a Waterfall-style process to an Agile board.
- Complete a hands-on lab that builds the Project 1 board and bug workflow.

---

## Why This Matters

Earlier today you learned the defect lifecycle: a defect is found, reported, fixed, retested and closed (or reopened, rejected, deferred or marked duplicate). You also created Jira issues, stories, tasks and bugs. That raises a practical question: where does the lifecycle actually live, and how does the whole team see it?

The answer is **boards and workflows**.

- A **workflow** is the rulebook. It defines which states an issue can be in and which moves between states are allowed.
- A **board** is the picture. It shows every issue in its current state so the whole team can see progress at a glance.

Think of an **airport check-in flow**. A passenger moves through check-in, security, boarding gate and the plane. There is a defined order, you cannot board without passing security, and a departures screen shows where everyone is. The workflow is the set of rules for moving through the airport; the board is the departures screen.

For a Quality Engineer this matters because:

1. **Defects are only useful if they move.** A bug that sits in "Open" for three weeks is a risk nobody sees. A board makes stalled work visible.
2. **QA is a stage, not an afterthought.** If the workflow has no "In Testing" state, testing is invisible and gets squeezed at the end of the sprint.
3. **Workflows enforce quality rules.** A bug cannot be closed without a resolution, or a story cannot reach Done without passing testing. The tool helps the team keep its own promises.
4. **Reports give evidence.** Burndown, created-vs-resolved and bugs-by-priority charts help you talk about quality with facts instead of opinions.
5. **Teams change.** Many companies are moving from Waterfall-style handoffs to Agile boards. A QE who understands boards and workflows can help that move go well.

> Important note about Jira screens: Jira changes frequently. Menu names, button positions and even some feature names differ between Jira Cloud and Data Center, between team-managed and company-managed projects, and from one release to the next. This lesson describes the ideas and the usual paths. Always check the current Atlassian documentation (links at the end) if your screen looks different from what is described.

---

## The Concept

### Part 1: Boards

#### 1.1 What is a board?

A **board** is a visual display of work. Each piece of work (an issue) appears as a **card**, and cards sit in **columns** that represent stages of progress. As work advances, a card moves from the left of the board toward the right.

Analogy: a **factory assembly line**. A product starts at the beginning of the line, passes through stations (cut, assemble, inspect, pack) and leaves at the end. A board is that assembly line drawn on a wall. The "inspect" station is where QA lives, and if nothing is waiting there, you can tell at a glance.

In Jira, a board is not a separate copy of your data. It is a **view** of issues in one or more projects. Move a card and you change the status of the underlying issue; change the status in the issue itself and the card moves on the board.

#### 1.2 Scrum board vs Kanban board

Jira Software offers two main board types.

- A **Scrum board** is built for teams that work in fixed-length iterations called **sprints** (usually 1 to 4 weeks). The board shows only the issues committed to the current sprint, and the sprint ends on a date.
- A **Kanban board** is built for continuous flow. There are no sprints. Work is pulled in as capacity allows, and the focus is on keeping the amount of work in progress low.

| Feature | Scrum board | Kanban board |
|---|---|---|
| Time structure | Fixed sprints with a start and end date | Continuous, no end date |
| What the board shows | Issues in the active sprint only | Issues that are in progress (and optionally a backlog) |
| Backlog | Separate Backlog screen where you plan sprints | Backlog is optional; in many setups it is a leftmost column or a separate view |
| Planning | Sprint planning picks what fits in the sprint | Work is pulled when someone has capacity |
| Work limits | The sprint scope is the limit | WIP (work in progress) limits on columns |
| Typical reports | Burndown, burnup, velocity, sprint report | Cumulative flow diagram, control chart |
| Best for | Product development with regular delivery | Support, maintenance, operations, bug triage, continuous testing |
| Roles and events | Scrum ceremonies (planning, daily, review, retro) | No required ceremonies |
| Changing scope | Discouraged mid-sprint | Allowed any time |

Which should Project 1 use? Because you practiced Scrum ceremonies yesterday, the lab in this lesson uses a **Scrum board** for stories and sprints. You will also see how a **Kanban board** could handle a dedicated bug-triage stream, because many QE teams run one.

> Note: In Jira Cloud, a Kanban board may be called a "Kanban" board template, and some newer team-managed projects present a "Board" and a "Backlog" and optionally "Sprints" as features you switch on. The concepts are the same.

#### 1.3 Anatomy of a board

Here is a sketch of a Scrum board for Project 1 (key: P1QE).

```
Project 1 - QE Foundations  >  P1QE Board          Sprint 1  (5 days left)   [Complete sprint]
Quick filters: [Only My Issues] [Bugs] [High Priority] [Needs Retest]
-------------------------------------------------------------------------------------------
                 TO DO            IN PROGRESS         IN TESTING            DONE
              (3 issues)           (2 issues)         (1 issue)           (2 issues)
-------------------------------------------------------------------------------------------
Swimlane: Alice Tran (3 issues)
              +-----------+       +-----------+      +-----------+
              | P1QE-12   |       | P1QE-9    |      | P1QE-7    |
              | Login     |       | Cart      |      | Search    |
              | page      |       | total bug |      | filter    |
              | [Story]   |       | [Bug] High|      | [Story]   |
              +-----------+       +-----------+      +-----------+
Swimlane: Ben Okafor (3 issues)
              +-----------+       +-----------+                         +-----------+
              | P1QE-14   |       | P1QE-10   |                         | P1QE-5    |
              | Checkout  |       | Reset     |                         | Footer    |
              | [Story]   |       | email bug |                         | links     |
              +-----------+       +-----------+                         +-----------+
Swimlane: Unassigned (0)
```

Let us name each part.

**Columns.** Vertical sections that represent stages of work. Each column is mapped to one or more **statuses** (see Section 1.4). The column name you see ("In Testing") and the status name behind it can differ, though they are usually the same.

**Cards.** Each card is one issue. A card shows the issue key (P1QE-9), a summary, the issue type icon, priority, assignee avatar, and optionally estimate, labels, due date and more. You can click a card to open its details and drag it to another column to change its status.

**Swimlanes.** Horizontal rows that group cards. In the sketch, the swimlanes are by assignee. They help answer questions like "what is each person working on?" or "which epic does this belong to?"

**Quick filters.** Buttons above the board that instantly hide cards that do not match. "Only My Issues" and "Recently Updated" are common built-ins; you can add your own using JQL (Jira Query Language, covered in Monday's introduction).

**Backlog.** The ordered list of work not yet in a sprint. On a Scrum board, the **Backlog** screen is where you plan: you rank issues, estimate them, group them into sprints and create new sprints.

**Active sprint.** The screen that shows the board for the sprint currently running. In many Jira versions this is a tab called "Active sprints" (or just "Board" in newer navigation). It lists only the sprint's issues.

**Epics panel.** An **epic** is a large body of work that groups many stories (for example, "Authentication" containing login, logout and password reset). The epics panel in the backlog lets you see epics, filter the backlog by one epic and drag issues into an epic. (In newer Jira Cloud versions epics are parent issues, and you may see a "Parent" or "Epic" filter instead of a panel.)

**Versions.** A **version** (also called a release) is a named point in time such as "v1.0". Issues can be tagged with a Fix Version to say which release they are meant for. The versions panel lets you see what is planned for each release, and release reports show what shipped. For QE, versions let you ask, "what is the bug count for v1.0?"

#### 1.4 Board configuration

Boards are configurable. The settings differ by edition, but on a company-managed Scrum or Kanban board you typically open the board, then use the three dots menu ("...") and choose **Configure** (or **Board settings**). In team-managed projects, many of these options live under **Board settings** or **Project settings** instead. Exact names vary.

##### Columns and status mapping

A **status** is a state an issue can be in (for example, "In Review"). A column displays one or more statuses. Mapping is the connection between them.

Rules of thumb:

- Every status used in the workflow should appear in exactly one column. A status not mapped to any column is **unmapped** and the issues in that status will not appear on the board (they become invisible!). Most Jira versions list unmapped statuses at the right side of the column setup screen.
- You can put more than one status in a single column. For example, the "Done" column can hold both "Closed" and "Rejected".
- The leftmost column normally represents "ready to start" and the rightmost represents finished work.

Step by step (company-managed, general path):

1. Open your board and select **...** then **Board settings** (or **Configure**).
2. Choose the **Columns** tab.
3. Click **Add column** and type a name such as "In Testing". Choose its status category (To Do, In Progress or Done) if prompted.
4. Drag a status from the "Unmapped statuses" area into the column you want.
5. Drag columns left or right to reorder them.
6. Click the small three-dot or delete control on a column to remove it (its statuses return to the unmapped area; make sure to remap them).
7. Save or confirm. Changes usually apply immediately.

##### Swimlanes

Swimlanes divide the board into rows. Common options:

| Swimlane type | What it does | When to use it |
|---|---|---|
| Queries | You define lanes using JQL | Separate "Expedite" and bugs from normal work |
| Stories | One lane per story, with its sub-tasks beneath | Track a story with its sub-tasks |
| Assignees | One lane per person | Daily stand-up, see everyone's load |
| Epics | One lane per epic | Report progress by feature area |
| Projects | One lane per project (multi-project boards) | Cross-project boards |
| No swimlanes | Single flat board | Small teams, simple boards |

Step by step:

1. Open **Board settings**.
2. Choose **Swimlanes**.
3. Select **Base swimlanes on**, for example Assignees or Queries.
4. If you choose Queries, click **Add swimlane**, enter a name such as "High-priority bugs", and enter a JQL condition such as `issuetype = Bug AND priority in (Highest, High)`.
5. Order the lanes; the first lane that matches an issue claims it. Keep an "Everything else" lane at the bottom so no issue gets lost.

##### Quick filters

A **quick filter** is a saved JQL condition shown as a button above the board. Clicking it hides every card that does not match.

Useful examples for QE:

| Name | JQL | Purpose |
|---|---|---|
| Bugs only | `issuetype = Bug` | Focus on defects |
| High priority | `priority in (Highest, High)` | Triage view |
| Needs retest | `status = "Ready for Retest"` | The tester's to-do list |
| My retests | `status = "Ready for Retest" AND reporter = currentUser()` | Bugs I reported that are waiting for me |
| Stale | `updated <= -3d AND statusCategory != Done` | Anything untouched for 3 days |

Step by step:

1. Open **Board settings** and choose **Quick filters**.
2. Enter a **Name** (keep it short; it appears on a button).
3. Enter the **JQL** in the query box.
4. Optionally add a description.
5. Click **Add**. Return to the board and test the button.

Note: quick filters are only applied on top of what the board already shows. They cannot show an issue the board's own filter excludes.

##### The board's filter (a related idea)

Every board is built from a **saved filter**, a JQL query that decides which issues the board is allowed to display. For example, `project = P1QE ORDER BY Rank ASC`. If a card seems to be "missing", check the board filter first. This is a very common cause.

##### Card layout

**Card layout** controls which extra fields appear on a card, such as Labels, Fix versions, Due date or Environment. A small amount of useful information beats a cluttered card. Typical QE choice: show Priority, Assignee, Labels and the Fix Version.

Step by step:

1. **Board settings** then **Card layout**.
2. Select the field you want and click **Add** for the "Backlog" and "Active sprints" sections.
3. Remove fields nobody uses.

##### Card colors

**Card colors** change a card's left edge or background based on a rule. Choose the basis from:

- **Priority** (for example, Highest in red),
- **Issue type** (bug vs story),
- **Assignee**,
- **Queries** (JQL, for example, "overdue" in red),
- or **Custom** values.

Example: color cards by **Queries**: `labels = blocked` becomes red, `priority = Highest` orange, `duedate < now()` purple. Colors communicate at a glance, but use them lightly. If every card is bright, nothing stands out. Also remember that some people cannot distinguish colors well, so never rely on color alone: pair it with an icon or a label.

Step by step:

1. **Board settings** then **Card colors**.
2. Choose **Based on**: Queries, Issue types, Priorities or Assignees.
3. For queries, click **Add** and enter a JQL and pick a color.
4. Save.

##### Estimation

**Estimation** is a measure of how large an issue is. Scrum boards commonly use **story points**, a relative unit (a 5 is bigger than a 2) rather than hours. You configure the **Estimation statistic** (Story Points, Original Time Estimate or Issue Count) and the **Time tracking** setting under **Board settings** then **Estimation**.

Estimation drives velocity and burndown charts. If you choose Issue Count, those charts count cards instead of points, which is a perfectly good simple choice for beginners.

##### Working days

**Working days** and holidays tell Jira which days count for burndown calculations so a weekend does not look like "no progress". Configure under **Board settings** then **Working days** (names vary). Mark Saturday and Sunday as non-working and add any public holidays.

##### WIP limits and column constraints (Kanban)

**WIP** means **Work In Progress**. A **WIP limit** is a maximum number of cards allowed in a column. If the limit is 3 and the column holds 4, the column turns visibly red. This is a **column constraint**.

Why limit WIP? Imagine a restaurant kitchen. If the chef starts every order at once, nothing leaves the kitchen on time. Finishing a few dishes at a time gets food to the table faster. In QE terms: if 12 bugs wait in "Ready for Retest" and testers are overloaded, a WIP limit makes the bottleneck visible so the team swarms on testing rather than starting yet more development.

Step by step (Kanban board, company-managed):

1. Open the board's **Board settings** then **Columns**.
2. Under **Column constraints** (sometimes "Constraints"), choose the constraint type, such as **Issue count** or **Issue count excluding sub-tasks**.
3. For the "In Progress" column enter **Max 3**; for "In Testing" enter **Max 2**. Optionally set a **Min**.
4. Save and look at the board: each column header shows a count and turns red when its maximum is exceeded.

WIP limits are guidance. They do not stop you from dragging a card in; they warn you so the team can discuss.

#### 1.5 Backlog management and ranking

The **backlog** is the to-do list for the product. Each item is ordered from most important at the top to least important at the bottom. This order is called **rank**.

Key activities:

- **Create** issues directly in the backlog with **Create issue**.
- **Rank** (re-order) by dragging an issue up or down, or by right-clicking and choosing **Send to top** or **Send to bottom**. Rank is stored on the issue, so the board and the backlog stay consistent.
- **Estimate** issues (story points) so you can plan.
- **Group** issues into epics and versions.
- **Refine** (also called grooming): review upcoming items so they are small, clear and testable. QEs add value here by asking, "How will we know this is done?"

Ranking is not the same as priority. **Priority** is a field describing urgency or business importance (Highest, High, Medium, Low). **Rank** is the actual order in which the team will work. Two High priority issues still have one that is first. When priority and rank disagree, ask the Product Owner which is correct.

Ranking tip for bugs: a Highest-priority bug on production normally goes to the top of the backlog or into the active sprint immediately; a Low-priority cosmetic bug can wait.

#### 1.6 Sprint operations

A sprint's life, from planning to review:

```
Create sprint --> Add issues --> Start sprint --> Work (daily) --> Complete sprint --> Review report
                                                       |                |
                                                  add / remove     move incomplete
                                                  (with care)      issues
```

1. **Create a sprint.** On the Backlog screen click **Create sprint**. An empty sprint appears above the backlog and is named automatically ("P1QE Sprint 1").
2. **Add issues.** Drag issues from the backlog into the sprint, or select issues and choose **Move to sprint**. As you add, the sprint header shows the total estimate so you can compare with the team's recent velocity.
3. **Start the sprint.** Click **Start sprint**, confirm the **name**, **duration** (1, 2, 3, 4 weeks or custom), **start date** and an optional **sprint goal**. A **sprint goal** is a one-sentence aim ("Users can log in and see their cart"). Once started, the board shows the sprint's issues.
4. **Add or remove issues mid-sprint.** You can, but it is a change to the team's commitment, so do it deliberately. A high-severity new bug is a good reason; a nice-to-have idea is not. Jira records the change and shows it in the sprint report.
5. **Work the sprint.** Cards move across the board daily. The daily stand-up often happens in front of it.
6. **Complete the sprint.** Click **Complete sprint**. Jira shows how many issues are done and how many are open. For open issues choose where they go: back to the **Backlog**, or into a **new sprint** or another **future sprint**. Completed issues stay in the finished sprint's history.
7. **Review the sprint report.** See Section 1.8.

**Moving incomplete issues.** Unfinished work is not failure; it is information. Ask: Was the estimate wrong? Did a bug interrupt us? Was testing delayed? Do not automatically roll everything into the next sprint without discussion. Re-rank it and re-estimate if needed.

#### 1.7 Kanban flow metrics, explained simply

Kanban boards use flow measures. Imagine a pizza shop.

- **Lead time** is how long from when the customer **orders** until the pizza **arrives**. In Jira terms: from the moment an issue is created (or requested) until it is done. It is the customer's view of waiting.
- **Cycle time** is how long the kitchen actually **works** on the pizza, from when the cook starts until it leaves the oven. In Jira terms: from the moment work begins (the issue moves to In Progress) until done. It is the team's view of effort.

```
   Created ---------- Started (In Progress) ------------------- Done
      |<---------------------- Lead time ------------------------->|
                          |<------- Cycle time ------------------>|
```

For bugs: lead time is how long a defect existed in the team's list from report to closure; cycle time is how long people actively worked on it. A short cycle time with a long lead time means bugs wait around before anyone starts them.

**Cumulative flow diagram (CFD).** A stacked area chart with time along the bottom. Each colored band represents a status: how many issues were in that status each day. Read it like this:

- Bands that stay **parallel** mean smooth flow.
- A band that gets **wider** over time means work is piling up in that status, a **bottleneck**. If the "In Testing" band keeps widening, testing is the choke point.
- The vertical distance across a band at one date is the amount of work in that state; the horizontal distance is roughly the time work spends there.

```
Issues
  ^                                     ____ Backlog
  |                           ______----
  |                     _----'      _____ In Progress
  |               _----'     ______-----
  |         _--'''   ___-----'   (widening = pile-up)
  |    _--''  ___---'   ______ In Testing
  | --'''-----'_________-----'
  |____________________________________ Done
  +----------------------------------------> Time
```

**Control chart.** A scatter plot where each dot is a finished issue. The horizontal axis is the date it finished; the vertical axis is how long it took (its cycle time or lead time). A line shows the rolling average, and shaded areas show the spread. Use it to see **predictability**: tightly clustered dots mean you can reliably say "most bugs get fixed in about 3 days". Dots far above the pack are **outliers** worth investigating ("why did that one take 20 days?").

These are found under **Reports** on a Kanban board (names may differ).

#### 1.8 Reports and dashboards

**Reports** are charts generated from board data. Open a board, then **Reports** in the sidebar (location varies).

| Report | Board type | What it shows | How a QE uses it |
|---|---|---|---|
| Burndown chart | Scrum | Work remaining in the sprint vs ideal line | Spot late-sprint pile-ups of testing |
| Burnup chart | Scrum | Work completed vs total scope over time | Shows scope changes (the scope line rises when issues are added) |
| Velocity chart | Scrum | Committed vs completed per sprint | Plan realistic sprints |
| Sprint report | Scrum | Completed, not completed, added mid-sprint, removed | Retrospective evidence |
| Created vs Resolved | Both | Issues created against resolved over time | Are bugs arriving faster than we fix them? |
| Cumulative flow | Kanban | Issues per status over time | Find bottlenecks |
| Control chart | Kanban | Cycle/lead time per issue | Check predictability |
| Release/version report | Both | Progress toward a version | Release readiness |

**Burndown vs burnup.** A **burndown chart** starts with the total work at the top left and slopes down toward zero as work completes. An ideal straight line shows the pace needed. If the actual line stays flat then drops suddenly at the end, work was not finishing until the last day, often because testing started late.

```
Remaining
work
  |\
  | \        ideal  .
  |  \_______ . . '
  |          \
  |           \_____ actual (flat, then drop)
  |                 \
  +------------------------\--> Days of sprint
```

A **burnup chart** has two lines: total scope (which goes up if you add work) and completed work (which climbs). Burnup makes "scope creep" easy to see and explain.

**Velocity** is the amount of work (story points or issue count) a team completes per sprint. The velocity chart compares "Commitment" with "Completed". It is a planning aid, never a performance ranking between teams.

**Sprint report.** After or during a sprint, it lists issues Completed, Not completed, Removed, and those added after the sprint started (marked with an asterisk). It also shows burndown. Use it in the sprint review and retrospective.

**Created vs Resolved chart.** Two lines: issues created and issues resolved over time. When the "created" line is above "resolved", the open backlog is growing. For a QE this reveals whether defects are being found faster than they are being fixed and is a good indicator before a release.

##### Dashboards and gadgets

A **dashboard** is a customizable page you build from small tiles called **gadgets**. Each gadget shows a chart, list or count, often driven by a saved filter or JQL query. Unlike board reports, dashboards can combine data from several projects and be shared with stakeholders.

Common gadgets: **Filter Results** (a list), **Pie Chart**, **Two-dimensional Filter Statistics** (a grid, such as priority by status), **Created vs Resolved Chart**, **Sprint Burndown Gadget**, **Assigned to Me**, **Activity Stream**.

**A QE dashboard (example).** Create a dashboard called "P1QE Quality Dashboard" with these gadgets:

| Gadget | Filter / JQL | Why |
|---|---|---|
| Pie chart, statistic type Priority | `project = P1QE AND issuetype = Bug AND statusCategory != Done` | Open bugs by priority |
| Two-dimensional filter statistics (rows Priority, columns Status) | `project = P1QE AND issuetype = Bug` | Bugs by priority and status in one grid |
| Created vs Resolved | `project = P1QE AND issuetype = Bug` | Is the bug backlog growing? |
| Filter results | `project = P1QE AND status = "Ready for Retest" ORDER BY priority DESC` | Retest queue |
| Filter results | `project = P1QE AND issuetype = Bug AND priority in (Highest, High) AND statusCategory != Done` | Critical open defects |

```
+--------------------------+   +-------------------------------------+
| Open bugs by priority    |   | Bugs: priority x status             |
|  Highest  ##   2         |   |            Open  InProg Retest Closed|
|  High     ####  4        |   | Highest     1     1      0      3    |
|  Medium   ######  6      |   | High        2     1      1      5    |
|  Low      ###  3         |   | Medium      3     2      1      9    |
+--------------------------+   +-------------------------------------+
+--------------------------+   +-------------------------------------+
| Created vs Resolved      |   | Retest queue (Ready for Retest)     |
|   /\  created            |   | P1QE-21  Cart total wrong   High    |
|  /  \/ resolved          |   | P1QE-30  Typo on login      Low     |
+--------------------------+   +-------------------------------------+
```

Step by step (general path):

1. Click **Dashboards** in the top bar then **Create dashboard**.
2. Name it and set sharing (private or shared with your project team).
3. Click **Add gadget** and choose the gadget type.
4. Select a saved filter or enter JQL and configure the chart options.
5. Click **Save** and arrange tiles by dragging.

Remember: dashboards support conversations; they do not replace them. A number on a chart should lead to a question, such as "why are three High bugs still open?"

---

### Part 2: Workflows

#### 2.1 What is a workflow?

A **workflow** is the set of **statuses** an issue can be in and the **transitions** that move it between them. Back to the airport: statuses are "Checked in", "Through security", "At gate", "Boarded"; transitions are the allowed moves between them. You cannot move directly from "Checked in" to "Boarded".

Definitions:

- **Status**: a named state, such as To Do, In Progress, In Testing or Done.
- **Transition**: a one-way move from one status to another, usually shown on a button (for example "Start progress"). A transition has a name and a destination. The name may differ from the status ("Send to test" leads to "In Testing").
- **Resolution**: a field that records *why* an issue was finished, such as Done, Fixed, Won't Do, Duplicate or Cannot Reproduce. An issue with no resolution is considered **unresolved** (open). Resolution answers "how did it end?" while status answers "where is it now?"
- **Status category**: Jira groups every status into one of three categories that drive reports and board logic: **To Do** (not started, grey/blue), **In Progress** (being worked, yellow) and **Done** (finished, green). You may have ten statuses but each belongs to exactly one category. Reports like Created vs Resolved and JQL such as `statusCategory = Done` rely on this.

```
              transition "Start progress"
  [ To Do ] ------------------------------> [ In Progress ]
  (category: To Do)                          (category: In Progress)
```

#### 2.2 Default workflow vs custom workflow

Jira provides default workflows when you create a project. A typical simple one is:

```
  [ To Do ] <----> [ In Progress ] <----> [ Done ]
```

In many templates every status can move to every other status (an "all transitions" pattern), which is flexible but not very controlled. Some software templates add "In Review".

A **custom workflow** is one you design to match your team's process. For QE, the default is often too coarse: it has no place to show a bug waiting to be retested, no Reopened state, and no way to record Rejected or Deferred distinct from Done. Customizing the workflow encodes the defect lifecycle into the tool.

Guidance: start from the default, add only the statuses that carry real meaning for how the team works, and test the workflow on a sample project before rolling it out.

#### 2.3 Designing a Bug workflow for QE

In today's defect lifecycle lesson you saw these states: New/Open, In Progress, Fixed, Ready for Retest, Verified/Closed, Reopened, Rejected, Deferred and Duplicate. Now we map each onto a Jira status and decide its status category.

| Defect lifecycle state | Jira status | Status category | Meaning in plain words |
|---|---|---|---|
| New / Open | Open | To Do | Bug reported; waiting for triage |
| In Progress | In Progress | In Progress | A developer is working on a fix |
| Fixed | Fixed (optional; see note) | In Progress | Developer finished the code change |
| Ready for Retest | Ready for Retest | In Progress | Fix deployed to the test environment; tester should verify |
| Verified / Closed | Closed | Done | Tester confirmed the fix; resolution Fixed |
| Reopened | Reopened | To Do | Retest failed or bug returned; needs more work |
| Rejected | Rejected | Done | Not a defect (works as designed, or invalid); resolution Won't Fix / Invalid |
| Deferred | Deferred | To Do (or a "parked" status) | A real bug, postponed to a later release |
| Duplicate | Duplicate | Done | Same as an existing bug; resolution Duplicate |

> Design note: Many teams merge "Fixed" and "Ready for Retest" because the developer's work is not truly complete until the build is available for testing. Having both statuses leads to confusing handoffs. Our recommended simplification: keep **Ready for Retest** and skip a separate "Fixed" status; the transition that moves a bug to Ready for Retest is the moment the developer says "fixed". If your team needs to distinguish "code merged" from "deployed to test", add "Fixed" deliberately and document the difference.

The transition diagram (ASCII):

```
                             +----------------------+
                             |      Rejected        |  (Done) resolution: Won't Fix / Cannot Reproduce
                             +----------^-----------+
                                        | Reject
                             +----------+-----------+  Duplicate   +-----------+
        Create bug --------> |        Open          |------------->| Duplicate |  (Done)
                             |      (To Do)         |              +-----------+
                             +----+------------+----+
                       Start      |            | Defer
                       progress   |            v
                                  |       +----------+   Reopen later
                                  |       | Deferred |-----------------> back to Open
                                  |       +----------+
                                  v
                          +---------------+
          Reopen          |  In Progress  |
   +--------------------- |               |
   |                      +-------+-------+
   |                              | Ready for retest ("Fix done")
   |                              v
   |                      +---------------+      Verify (resolution = Fixed)
   |                      |    Ready for  |-----------------------------+
   |                      |    Retest     |                              v
   |                      +-------+-------+                      +--------------+
   |                              |  Retest failed               |    Closed    | (Done)
   |                              +--------------------+         +------+-------+
   |                                                   |                |
   |                                                   v                | Reopen (found again)
   |                                            +-------------+         |
   +------------------------------------------> |  Reopened   | <-------+
                                                | (To Do)     |
                                                +------+------+
                                                       | Start progress
                                                       v
                                                  In Progress
```

Transition table:

| From status | Transition name | To status | Who usually does it | Notes |
|---|---|---|---|---|
| (create) | Create | Open | Tester / anyone | Required fields: summary, steps, environment, severity |
| Open | Start progress | In Progress | Developer | Assignee should be set |
| Open | Reject | Rejected | Triage lead / Developer | Requires a comment and resolution |
| Open | Duplicate | Duplicate | Triage lead | Should link to the original issue |
| Open | Defer | Deferred | Product Owner / Triage lead | Requires a comment and target version |
| In Progress | Ready for retest | Ready for Retest | Developer | Requires a comment: build number, what changed |
| In Progress | Stop progress | Open | Developer | Unassigns or keeps assignee per policy |
| Ready for Retest | Verify and close | Closed | Tester | Requires resolution = Fixed |
| Ready for Retest | Retest failed | Reopened | Tester | Requires a comment with evidence |
| Closed | Reopen | Reopened | Tester / Developer | Requires a comment |
| Rejected | Reopen | Reopened | Reporter / Triage lead | If the rejection is disputed |
| Deferred | Reopen | Open | Product Owner | When the release is planned |
| Reopened | Start progress | In Progress | Developer | Priority may be raised |

Why separate **Closed** and **Rejected** and **Duplicate** when all are Done? Because the reports tell different stories. A high Rejected rate suggests reports are unclear or requirements are misunderstood. A high Duplicate rate suggests testers are not searching before reporting. A closed-and-fixed count shows real fixes. Keeping them separate (while sharing the Done category) preserves meaning.

#### 2.4 Designing a Story workflow with a QA stage

Stories are user-facing requirements. The default "To Do, In Progress, Done" hides testing. Add explicit QA states:

```
   [ To Do ] ---> [ In Progress ] ---> [ In Review ] ---> [ In Testing ] ---> [ Done ]
       ^               |                    |                  |                 |
       |               +<-------------------+                  |                 |
       |               +<----------------------------------------+ (fails testing) |
       +<-------------------------------------------------------------------------+ (reopen)
```

| Status | Category | Meaning | Typical owner |
|---|---|---|---|
| To Do | To Do | Ready to start; refined with acceptance criteria | Product Owner / team |
| In Progress | In Progress | Developer is building | Developer |
| In Review | In Progress | Code review or peer review | Peer / reviewer |
| In Testing | In Progress | QE is verifying against acceptance criteria | QE |
| Done | Done | Meets the Definition of Done | Team |

Transitions: To Do to In Progress; In Progress to In Review; In Review to In Testing (approved) or back to In Progress (changes requested); In Testing to Done (pass) or back to In Progress (fail, with linked bug); Done back to To Do or In Progress (reopen, rarely).

When a story fails testing, create a linked **Bug** and link it to the story (issue link such as "is blocked by"). The story stays in In Testing or returns to In Progress, depending on team agreement. The key is that the board *shows* that QA is happening, so a column full of cards in "In Testing" exposes a bottleneck.

#### 2.5 Transition features: conditions, validators, post functions and screens

In **company-managed** projects, each transition can have extra behavior attached. In team-managed projects a smaller set of "rules" is available. Think of a transition as a doorway with a security guard and some helpful staff.

**Conditions** decide whether a transition is **available** to a user at all. If the condition fails, the button is hidden. Example: only users in the "QA Team" group can use "Verify and close". Or: the transition "Reopen" is only available to the reporter. Analogy: a guard checks your boarding pass before showing you the door.

**Validators** check the data *when you try* to use the transition. If validation fails the transition is blocked and an error message is shown. Example: "Resolution must be set", or "Comment is required", or "Fix Version must not be empty before Deferring". Analogy: the guard checks that your bag is the right size.

**Post functions** are automatic actions that run *after* the transition succeeds. Examples: set the resolution to Fixed, clear the resolution when reopening, assign the issue to the reporter, update a field, or send an email. Analogy: staff who tag your luggage after you pass. (Jira has standard post functions that run automatically on every transition, such as "set issue status" and "create history", which you normally never touch.)

**Screens on transition.** A **screen** is a form (a set of fields). You can attach a screen to a transition so a pop-up asks the user for specific information when they use it. Example: "Ready for retest" shows a screen with *Comment*, *Fix build number* and *Fix version* fields; "Reject" shows a screen with a *Resolution* field and *Comment*.

| Feature | When it runs | Question it answers | QE example |
|---|---|---|---|
| Condition | Before showing the button | May this user see the transition? | Only testers can Verify and close |
| Validator | When the button is clicked | Is the data acceptable? | Resolution is required to close |
| Post function | After the transition succeeds | What should happen automatically? | Reassign bug to reporter on Ready for Retest |
| Screen | When the button is clicked | What should the user fill in? | Ask for a comment and build number |

In team-managed projects some of these ideas appear as **rules** on a transition (for example "restrict who can move an issue to this status" or "require a field"), and you may need Jira Automation for post-function-style behavior. Names and availability vary; check current Atlassian documentation.

#### 2.6 Resolutions

A **resolution** records the outcome when an issue is finished. Standard Jira resolutions include Done, Won't Do, Duplicate and Cannot Reproduce (the list varies; administrators can customize it in company-managed Jira). QE mapping:

| Final status | Typical resolution |
|---|---|
| Closed | Fixed (or Done) |
| Rejected | Won't Fix / Not a Bug / Cannot Reproduce |
| Duplicate | Duplicate |
| Deferred | Usually left **unresolved** (the bug still exists) |

Good practice: set the resolution via the transition (a screen or post function) and **clear** it when the issue is reopened, otherwise a reopened bug could still look "resolved" and vanish from your open-bug filters. In JQL, `resolution = Unresolved` finds issues that are not finished.

#### 2.7 Permissions overview: who may change status?

Permissions control who may do what. In company-managed Jira they are grouped into **permission schemes** assigned to projects. Relevant permissions:

| Permission | What it allows |
|---|---|
| Browse projects | See the project and its issues |
| Create issues | Report a bug or story |
| Edit issues | Change fields |
| Transition issues | Move an issue between statuses |
| Assign issues | Choose an assignee |
| Resolve issues | Set a resolution (in some versions bundled with transitions) |
| Close issues | Use transitions leading to closed states (in some configurations) |
| Administer projects | Change project settings |
| Manage sprints | Create, start and complete sprints |

Who may change status is the combined result of **permissions** (can this user transition issues at all?) plus **transition conditions** (is this specific transition available to them?). For example, a "Customer" role might see bugs but not transition them, while only "Developers" can Start progress and only "QA" can Verify and close. In team-managed projects, access is by project role (Administrator, Member, Viewer) and a smaller set of settings.

Keep permissions as open as your culture allows. Locking every transition tends to slow the team; restrict only transitions where an independent check matters (for example, a tester, not the developer, closes a bug).

#### 2.8 Workflow schemes and issue type schemes (overview)

In company-managed projects:

- A **workflow scheme** says which workflow applies to which issue type in a project. Example: Bugs use "P1QE Bug Workflow", Stories and Tasks use "P1QE Story Workflow", Epics use the default workflow.
- An **issue type scheme** says which issue types (Bug, Story, Task, Epic, Sub-task) a project offers.
- A workflow scheme is assigned to a project. Many projects can share one scheme, so changes affect all of them. This is why administrators are careful.

Analogy: the **workflow** is a recipe; the **workflow scheme** is the menu saying which dish uses which recipe; the **issue type scheme** is the list of dishes the restaurant offers.

In team-managed projects the same idea is simplified: each issue type can have its own workflow directly, and the issue types are managed in the project settings.

#### 2.9 Team-managed vs company-managed projects

Jira Cloud has two project styles. (Jira Data Center has company-managed style only.)

| Aspect | Team-managed | Company-managed |
|---|---|---|
| Who configures it | Project administrators (team members) | Jira administrators (often central) |
| Where workflow is edited | Project settings, then Workflow (visual editor) | Jira Administration, then Issues, then Workflows |
| Scope of changes | Only that project | Can be shared across many projects via schemes |
| Customization depth | Simpler: statuses, transitions, basic rules | Deeper: conditions, validators, post functions, screens, schemes |
| Admin rights needed | Project admin only | Jira admin for workflows and schemes; project admin for some board settings |
| Best for | Single, independent teams | Large organizations needing consistency and governance |
| Reports and boards | Provided, with some differences | Full suite |

Practical implication for trainees: if your training site uses a team-managed project, you can build the bug workflow yourself. If it is company-managed and you lack administrator rights, you can design the workflow on paper, request it from the administrator using the transition table in this lesson, or practice in a free personal Jira Cloud site where you are the administrator.

#### 2.10 Jira Automation: an introduction

**Jira Automation** lets you create **rules** that do repetitive work automatically. Every rule has three building blocks:

- **Trigger**: the event that starts the rule (an issue is created, a status changes, a field changes, a schedule fires).
- **Condition**: an optional check that must be true (the issue is a Bug; priority is High).
- **Action**: what the rule does (assign, comment, send an email, create an issue, transition an issue).

Think of a **rule** as "if this, check that, then do this". Automation is the airport's loudspeaker and ground crew that act without being asked.

Useful QE examples:

| # | Rule | Trigger | Condition | Action |
|---|---|---|---|---|
| 1 | Hand back to tester | Issue transitioned to Ready for Retest | Issue type = Bug | Assign issue to **Reporter**; add comment "Fix is ready for retest" |
| 2 | Comment on reopen | Issue transitioned to Reopened | None | Add comment "Reopened: please add evidence of the failing steps"; set priority up one level (optional) |
| 3 | Escalate stale bugs | Scheduled daily | JQL: `issuetype = Bug AND priority = Highest AND statusCategory != Done AND updated <= -2d` | Send email or Slack message to the team lead |
| 4 | Auto-link duplicates | Issue transitioned to Duplicate | Link to another issue exists | Add comment pointing to the original; close with resolution Duplicate |
| 5 | Story to testing handoff | Issue transitioned to In Testing | Issue type = Story | Assign to the QA lead; notify the channel |

Step by step (company-managed or team-managed, general path):

1. Open the project then **Project settings** then **Automation** (or **Automation** in the main menu).
2. Click **Create rule**.
3. Choose a **trigger** (for example, "Issue transitioned") and set the **To status** to "Ready for Retest".
4. Click **Add component** then **IF: Add a condition** (for example, issue fields condition: Issue Type equals Bug).
5. Click **Add component** then **THEN: Add an action** (for example, **Assign issue** then **Reporter**).
6. Add a second action: **Add comment**.
7. Name the rule, click **Turn it on**, and test it with a sample bug.

Cautions: test rules in a sandbox project; avoid loops (a rule that changes a field which then triggers itself); and keep rules documented so the team knows why issues are changing by themselves. Rule limits and available actions depend on your Jira plan. Check Atlassian documentation.

**Jira AI features (brief and cautious).** Recent Jira releases include AI-assisted capabilities, such as suggesting summaries, drafting descriptions or helping write automation rules and JQL from plain-language requests. Availability depends on your plan and your organization's policy. Treat AI output as a **draft**: always review it for accuracy, make sure no confidential data is entered where your organization disallows it, and verify any generated JQL or rule by testing it. You remain responsible for the quality of what is recorded.

#### 2.11 Notifications overview

**Notifications** tell people when something happens. In Jira, a **notification scheme** (company-managed) or notification settings (team-managed) decides who gets an email or in-app alert for events such as Issue created, Issue assigned, Issue commented, Issue resolved and Issue reopened. Typical recipients: the reporter, the assignee, watchers and project roles.

Practical points:

- A **watcher** is a person who chooses to follow an issue and receive its notifications. Testers often watch the bugs they reported.
- Each user has personal notification preferences (under profile settings) that control email frequency and in-app notifications.
- Too many notifications create noise and people ignore them; too few cause missed handoffs. Aim for notifications on assignment, status changes that hand work to you (such as Ready for Retest), and comments that mention you with `@name`.
- Notification settings differ by edition and may require administrator rights to change.

#### 2.12 Definition of Done enforced through workflow

The **Definition of Done (DoD)** is the team's shared checklist of what must be true before work counts as finished (for example: code reviewed, acceptance criteria verified, no open critical bugs, documentation updated). A workflow can help the team *keep* that promise:

| DoD rule | How the workflow supports it |
|---|---|
| Work must be tested before Done | The workflow has **In Testing** before **Done**, and the board shows it |
| Only QA closes bugs | A **condition** limits "Verify and close" to the QA group |
| Resolution must be recorded | A **validator** requires resolution when moving to Closed |
| Retest evidence is documented | A **screen** on "Verify and close" requires a comment |
| No open linked bugs | Automation or a validator checks that no unresolved linked bugs exist before Done (company-managed or via automation) |
| Reopened work is visible | A **post function** clears the resolution on Reopen |

A workflow does not *guarantee* quality, it makes skipping steps harder and visible. The team's agreement matters more than the tool. Also write the DoD where the team sees it: some teams add it to the sprint board header or a team page and review it in retrospectives.

#### 2.13 Best practices and anti-patterns

Best practices:

- **Keep it simple.** Start with the fewest statuses that reflect real handoffs.
- **One status, one meaning.** Everyone should agree on what "In Review" means.
- **Align the workflow with how the team actually works,** not an idealized process.
- **Use status categories correctly** so reports are accurate.
- **Name statuses as states, not actions** ("In Testing", not "Test it").
- **Document it.** A one-page diagram and table (like those in this lesson) on the team wiki.
- **Review it in retrospectives** and change it when it stops helping.
- **Pilot first.** Try a new workflow with a few issues or in a sandbox project.

Anti-patterns (things to avoid):

| Anti-pattern | Why it hurts | Better approach |
|---|---|---|
| 15+ statuses ("workflow sprawl") | Confusing, slow, cards disappear into tiny columns | 5 to 8 meaningful statuses |
| Statuses for people ("With John") | Breaks when staff change; duplicates the Assignee field | Use Assignee |
| A status for every field value | Overlaps with fields like Priority | Use fields for attributes, statuses for stages |
| Everything can move anywhere | No process, no control | Define sensible transitions |
| Over-restricted transitions | Team works around the tool | Restrict only where independence matters |
| Unmapped statuses | Issues invisible on the board | Map every status to a column |
| Resolution not cleared on reopen | Reopened bugs look resolved | Post function to clear resolution |
| One giant workflow for all issue types | Stories and bugs need different states | Separate workflows via a scheme |
| Board used as a reporting tool for managers only | Team stops updating it | Use it for the daily team conversation |

#### 2.14 Migrating a team from Waterfall-style to an Agile board

Many teams begin with a sequential process: requirements, design, build, test, release, with documents handed from one group to the next and testing at the end. Moving to an Agile board is a change in habits, not just a tool.

A gentle path:

1. **Map the current process first.** Draw the existing stages and handoffs. Do not start by changing Jira.
2. **Start with columns that mirror reality.** If your process has "Requirements, Build, Test, Release", create columns with those names. This gives familiarity.
3. **Introduce small batches.** Replace big requirement documents with small stories that each fit in a sprint.
4. **Pull testing earlier.** Add acceptance criteria during refinement; move QA into the sprint instead of after it. Shorten the gap between "In Progress" and "In Testing".
5. **Start with Kanban, then add sprints.** Visualizing work and limiting WIP is a low-risk first step. Add sprints and ceremonies when the team is comfortable.
6. **Migrate existing items.** Import or recreate open issues; clean up old statuses; map old statuses to new ones so no issue is lost. In company-managed Jira an administrator can map statuses during a workflow change.
7. **Train and coach.** Hold a short walkthrough of the board and workflow, and appoint someone to answer questions in the first sprint.
8. **Inspect and adapt.** After two or three sprints review the board, metrics and the team's feelings, and adjust.

Expect resistance: managers may worry about losing detailed plans, testers may feel they are being pulled into the middle of unfinished work. Explain the benefits (earlier feedback, fewer surprise defects) and celebrate small wins.

#### 2.15 Common mistakes

- **Copying another team's workflow without asking whether it fits.**
- **Creating a status when a field or label would do.**
- **Forgetting to map new statuses to board columns.** The card vanishes.
- **Editing a shared workflow in company-managed Jira without understanding which projects use it.** Changes can affect many teams. Check the scheme first.
- **Using priority and rank interchangeably.**
- **Never clearing resolution on reopen.**
- **Dragging cards without updating details** (assignee, comments), so the board looks tidy but is not trustworthy.
- **Starting sprints with no goal or no estimates.**
- **Overloading the sprint** beyond recent velocity.
- **Leaving stale cards** in columns for days without comment.
- **Ignoring WIP limits** that turn red.
- **Treating charts as targets.** If velocity becomes a goal, teams inflate estimates; charts are conversation starters.
- **Relying on an unverified AI suggestion** for JQL or automation without testing.

---

## Examples

### Example 1: A quick filter in action

The team lead asks, "What is waiting for me to retest?" Alice clicks the quick filter **Needs retest** (JQL `status = "Ready for Retest"`). Cards from other columns fade or hide, leaving only the two bugs waiting in testing. She then clicks **Only My Issues** as well, and the board shows the one she reported. Two clicks replaced a long search.

### Example 2: A bottleneck in the cumulative flow diagram

Over three sprints the "In Testing" band on the CFD gets steadily wider while the "Done" band grows slowly. Work arrives in testing faster than testers can finish it. The team responds with a WIP limit of 3 on "In Testing" and agrees that developers will help with retests before starting new work. Two weeks later the band narrows.

### Example 3: Reopening a bug

Ben marks bug P1QE-9 "Ready for Retest". Automation assigns it to Alice, the reporter. Alice retests, the cart total is still wrong, and she clicks **Retest failed**. A screen asks for a comment; she attaches a screenshot. The status becomes **Reopened**, a post function clears the resolution, and automation adds a comment asking for a failing-step summary. Ben sees it on his board and moves it back into progress.

### Example 4: Resolution mismatch caught

A developer tries to close a bug by dragging it to the Closed column. The validator blocks it with "Resolution is required". The developer uses the transition screen to choose "Fixed". The validator did its job: a bug is never closed without recording why.

---

## Hands-On Lab: Build the Project 1 Board and Bug Workflow

**Goal:** Create a Scrum board and a Bug workflow for "Project 1 - QE Foundations", then run a sample sprint.

**Before you begin:**

- You need access to a Jira Software site. If you have a company-managed project and cannot edit workflows, use a free personal Jira Cloud site (you will be the administrator) or complete the "paper design" fallback at the end of Part B.
- Menu names may differ from the steps below. Use the current Atlassian documentation when something does not match.
- Use the project key **P1QE**. If it exists, use your own variant such as P1QE2.

### Part A: Set up the project and issues

1. Create a Scrum project named **Project 1 - QE Foundations** with key **P1QE** (Monday's lesson showed project creation). Choose a Scrum template.
2. Open **Backlog**. Create an epic named **Authentication**.
3. Create these issues (use **Create issue**; set the type shown):

| Key (example) | Type | Summary | Priority | Points | Epic |
|---|---|---|---|---|---|
| P1QE-1 | Story | As a user I can log in with email and password | High | 5 | Authentication |
| P1QE-2 | Story | As a user I can reset my password by email | Medium | 3 | Authentication |
| P1QE-3 | Story | As a shopper I can add items to my cart | High | 5 | Shopping |
| P1QE-4 | Story | As a shopper I can see my cart total | High | 3 | Shopping |
| P1QE-5 | Task | Prepare the test environment and test data | Medium | 2 | |
| P1QE-6 | Bug | Cart total ignores quantity changes | High | 2 | Shopping |
| P1QE-7 | Bug | Password reset email never arrives | Highest | 3 | Authentication |
| P1QE-8 | Bug | Typo in login page heading | Low | 1 | Authentication |

4. Rank the backlog by dragging so the order is: P1QE-7, P1QE-1, P1QE-3, P1QE-6, P1QE-4, P1QE-2, P1QE-5, P1QE-8.
5. Create an epic **Shopping** if you have not yet, and attach the issues as in the table.

### Part B: Build the Bug workflow

**Company-managed (administrator):**

1. Go to **Jira settings (gear icon)** then **Issues** then **Workflows**.
2. Click **Add workflow** and name it **P1QE Bug Workflow**.
3. Add statuses and set their categories:

| Status | Category |
|---|---|
| Open | To Do |
| In Progress | In Progress |
| Ready for Retest | In Progress |
| Closed | Done |
| Reopened | To Do |
| Rejected | Done |
| Deferred | To Do |
| Duplicate | Done |

4. Add transitions using the table in Section 2.3 (for example, drag from Open to In Progress and name it "Start progress").
5. For the transition **Verify and close**, add a validator requiring the field **Resolution**, and a post function setting resolution to **Fixed** (if the interface offers it; otherwise attach a screen with the Resolution field).
6. For **Reopen** transitions, add a post function to **clear the resolution**.
7. For **Retest failed**, attach a screen requiring a **Comment**.
8. **Publish** the workflow.
9. Go to **Workflow schemes**, create or edit the scheme for P1QE, and assign **Bug** to **P1QE Bug Workflow** (other issue types keep their workflow). Associate the scheme with the project, following the migration prompts to map any existing statuses. Keep the sprint empty during this step if possible.

**Team-managed:**

1. Open the project then **Project settings** then **Work types** (or **Issue types**) then select **Bug** then **Workflow**.
2. Add the statuses above and drag connections to create transitions (the visual editor shows boxes and arrows).
3. Use the status's **category** setting to assign To Do / In Progress / Done.
4. Use **Rules** on a transition if available to require a field or restrict who can move it.
5. Publish or save.

**Fallback if you lack rights:** Draw the workflow in a drawing tool using the ASCII diagram as a model. Fill in the transition table including who may use each transition. Submit it to your instructor or administrator as a "workflow request".

### Part C: Configure the board

1. Open the board then **Board settings** then **Columns**.
2. Create columns and map statuses for the **story** workflow and bugs together. Suggested mapping for the combined board:

| Column | Statuses mapped |
|---|---|
| To Do | To Do, Open, Reopened, Deferred |
| In Progress | In Progress |
| In Testing | In Testing, Ready for Retest |
| Done | Done, Closed, Rejected, Duplicate |

3. Make sure no status remains unmapped.
4. **Swimlanes:** choose **Queries** and add: "Bugs" (`issuetype = Bug`), "Stories and tasks" (`issuetype in (Story, Task)`), and leave the default "Everything else".
5. **Quick filters:** add `Bugs only` (`issuetype = Bug`), `High priority` (`priority in (Highest, High)`), and `Needs retest` (`status = "Ready for Retest"`).
6. **Card colors:** choose **Priority** (or Queries) and make Highest red and High orange.
7. **Card layout:** add Labels and Fix versions to the active sprint display.
8. **Estimation:** set to **Story Points** (or Issue Count if you did not estimate). **Working days:** set Saturday and Sunday as non-working.
9. **Optional Kanban exercise:** create a second board using a Kanban template with the filter `project = P1QE AND issuetype = Bug`. Set a **Max 3** constraint on In Progress and **Max 2** on Ready for Retest.

### Part D: Create a dashboard

1. Create a dashboard named **P1QE Quality Dashboard**.
2. Add the pie chart, two-dimensional filter statistics, Created vs Resolved and retest-queue filter gadgets from Section 1.8.
3. Take a screenshot (blur any personal information) for your portfolio.

### Part E: Run the sample sprint scenario

**Scenario.** You are starting Sprint 1 (5 working days). The sprint goal: "Users can log in and reset their password; cart total is correct."

1. **Create sprint** and drag into it: P1QE-7, P1QE-1, P1QE-3, P1QE-6. Total 13 points (5 + 5 + 3... check your own sums; the aim is to see the total shown in the sprint header).
2. **Start sprint** with a 1-week duration and the goal above.
3. **Day 1.** Move P1QE-7 (bug) from Open to In Progress. Move P1QE-1 (story) from To Do to In Progress. Assign both.
4. **Day 2.** The developer finishes P1QE-7. Use **Ready for retest** and add a comment, "Fixed in build 1.0.3, retry reset email." Check whether automation (if you built the optional rule) assigns it to you as reporter.
5. **Day 3.** You retest P1QE-7. The email arrives, so use **Verify and close** with resolution **Fixed**. The card goes to Done. Move P1QE-1 to In Review and then In Testing (if your story workflow has these).
6. **Day 3, afternoon.** Testing P1QE-1, you find that an incorrect password shows no error message. Create a new bug (P1QE-9, priority High) and link it to P1QE-1 with a "blocks" link. Add P1QE-9 to the sprint (this is a mid-sprint addition; note it).
7. **Day 4.** The developer fixes P1QE-9 and moves it to Ready for Retest. You retest and it fails because the message appears in the wrong place. Use **Retest failed** with a comment and screenshot. The bug moves to Reopened. Check that the resolution is cleared.
8. **Day 5 morning.** The developer fixes it again; you verify and close it. P1QE-1 moves to Done.
9. **Day 5.** P1QE-3 is still In Progress. P1QE-6 is still In Testing waiting for an environment. Click **Complete sprint**. When prompted, move the two open issues to a **new sprint (Sprint 2)**.
10. Open the **Sprint report**, the **Burndown chart**, **Velocity chart** and **Created vs Resolved** and write three sentences: what finished, what did not and why, and one improvement for the next sprint.

**Reflection questions:**

- Which status held cards the longest?
- Did the board make testing visible?
- Which transition rules helped, and which got in the way?

---

## Knowledge Check

1. In your own words, what is the difference between a workflow and a board?
2. Name two differences between a Scrum board and a Kanban board.
3. What happens to an issue whose status is not mapped to any column?
4. What is the difference between a quick filter and the board's filter?
5. What is a WIP limit and why would a QE team use one on "Ready for Retest"?
6. Explain the difference between lead time and cycle time using the pizza shop analogy.
7. On a cumulative flow diagram, the "In Testing" band keeps widening. What does that suggest?
8. What does a burnup chart show that a burndown chart can hide?
9. Name the three status categories. Which category should "Rejected" belong to, and why?
10. What is the difference between a condition, a validator and a post function? Give one QE example of each.
11. Why should the resolution be cleared when a bug is reopened?
12. Which defect lifecycle states are final (Done category) in the Bug workflow of this lesson, and which are not?
13. Give two reasons a team might keep Rejected and Duplicate as separate statuses from Closed.
14. Who can edit a workflow in a company-managed project, and who in a team-managed project?
15. Write the three parts of an automation rule that assigns a bug to its reporter when it moves to Ready for Retest.
16. Give two anti-patterns of workflow design and how to fix each.
17. List three steps you would take when moving a Waterfall team to an Agile board.
18. Why should AI-suggested JQL or automation rules be tested before use?

### Answers

1. A workflow defines the statuses and the allowed transitions between them (the rules). A board is a visual display of issues by status (the picture). Changing the workflow changes what the board can show; moving cards on the board triggers workflow transitions.
2. Any two of: Scrum uses sprints and Kanban is continuous; Scrum shows only the active sprint while Kanban shows ongoing flow; Kanban uses WIP limits and flow charts while Scrum uses burndown and velocity; Scrum has a separate planning backlog and ceremonies.
3. The issue does not appear on the board (it effectively becomes invisible there), though it still exists in the project and in searches. Map every status to a column.
4. The board's filter (a saved JQL query) decides which issues can appear on the board at all. A quick filter is an extra button that further narrows what is already displayed.
5. A WIP limit is a maximum number of cards allowed in a column. Limiting Ready for Retest highlights when testing is overloaded so the team stops starting new work and helps with retests.
6. Lead time is from order placed to pizza delivered (waiting included); cycle time is from the cook starting to the pizza leaving the oven. In Jira, lead time runs from creation to done; cycle time runs from work started to done.
7. Work is piling up in testing, a bottleneck: testers are overloaded, environments are unavailable or work arrives faster than it is verified.
8. A burnup chart shows scope (total work) as a separate line, so added scope is visible. A burndown line may look flat or slow when scope grew, which can be misleading.
9. To Do, In Progress and Done. Rejected belongs in Done because the issue requires no more work; the status name, plus a resolution such as Won't Fix, keeps it distinct from fixed bugs.
10. A condition controls whether a transition is available (only QA can use Verify and close). A validator checks data when the transition is attempted (resolution must be set). A post function runs automatically afterward (assign to the reporter, clear resolution).
11. If the resolution stays set, the reopened bug still looks resolved and may drop out of "unresolved" filters, dashboards and reports, hiding real open work.
12. Done category: Closed, Rejected, Duplicate. Not final: Open, In Progress, Ready for Retest, Reopened and Deferred (Deferred is parked and can return).
13. Reports separate: a high Rejected count signals unclear requirements or reports; a high Duplicate count signals poor searching before reporting; Closed shows genuine fixes. Resolutions can also distinguish them, but separate statuses make the filter and board clearer.
14. Company-managed: a Jira administrator (workflows and schemes are global admin objects). Team-managed: the project administrator, within the project's settings.
15. Trigger: Issue transitioned to Ready for Retest. Condition: Issue type equals Bug. Action: Assign issue to Reporter (optionally add a comment).
16. Examples: too many statuses (reduce to the meaningful handoffs); statuses named after people (use the Assignee field); unmapped statuses (map every status to a column); resolutions not cleared on reopen (add a post function).
17. Any three of: map the current process; mirror existing stages as columns; introduce small stories; pull testing earlier; start with Kanban and WIP limits; migrate and map old statuses; train the team; inspect and adapt after a few sprints.
18. AI output can be wrong or misleading, may not match your project's fields and workflow, and rules can create unintended changes or loops. Testing in a sandbox protects real data and keeps you accountable.

---

## Try It: Quick Activity

Take ten minutes with a partner. On paper, draw the current board for a pretend release of Project 1 with columns To Do, In Progress, In Testing, Done and place eight cards (a mix of stories and bugs). Then:

1. Decide which cards would be red under a "Highest priority" rule.
2. Imagine In Testing has a WIP limit of 2 and holds 4 cards. What would you do first?
3. Move one bug through the full Bug workflow, naming each transition aloud ("Start progress", "Ready for retest", "Retest failed", and so on), and say who performs each.

---

## Key Takeaways

- A **board** shows work as cards in columns; a **workflow** defines the statuses and transitions that decide where cards can go.
- **Scrum boards** suit sprint-based delivery (backlog, active sprint, burndown, velocity); **Kanban boards** suit continuous flow (WIP limits, cumulative flow, control chart).
- Every status should be mapped to a column, or the card disappears from the board.
- Use swimlanes, quick filters (JQL), card colors and card layout to make the board answer the team's daily questions, and keep it uncluttered.
- Rank is the order of work; priority is the importance. They are related but not the same.
- Lead time is the whole wait from request to done; cycle time is the active working time.
- Reports and dashboards (burndown, burnup, velocity, sprint report, created vs resolved, bugs by priority and status) turn board data into conversations about quality.
- A workflow consists of statuses, transitions, resolutions and status categories (To Do, In Progress, Done).
- A QE Bug workflow maps the defect lifecycle (Open, In Progress, Ready for Retest, Closed, Reopened, Rejected, Deferred, Duplicate) onto Jira statuses; a Story workflow adds In Review and In Testing so QA is visible.
- Conditions, validators, post functions and screens add control to transitions; resolutions record how work ended and should be cleared on reopen.
- Team-managed projects let project admins edit workflows; company-managed projects generally need Jira administrators and use workflow and issue type schemes.
- Jira Automation (trigger, condition, action) removes repetitive handoffs; treat AI-generated suggestions as drafts to verify.
- Keep workflows simple, aligned with the real process, and documented; avoid sprawl and person-named statuses.
- Menu names and UI vary by Jira edition and release, so check current Atlassian documentation.

---

## Additional Resources

- Atlassian Support, Jira Software Cloud documentation (boards, backlogs, sprints, reports and dashboards): https://support.atlassian.com/jira-software-cloud/
- Atlassian Support, "Working with workflows" and related Jira administration guides: https://support.atlassian.com/jira-cloud-administration/
- Atlassian Agile Coach (guides on Scrum, Kanban, boards and metrics): https://www.atlassian.com/agile
