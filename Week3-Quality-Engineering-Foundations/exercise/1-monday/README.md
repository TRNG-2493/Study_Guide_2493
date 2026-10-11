# Exercise: Map Project 1 to an SDLC/STLC Plan and Set Up Jira

Week 3 - Quality Engineering Foundations | Monday: SDLC, STLC and Agile | Individual exercise | 2 to 3 hours

## Scenario

You have just joined the Project 1 team as the Quality Engineer (QE). The product is a small web app where a visitor can register an account and log in. The team is about five people: a Product Owner, a Scrum Master, two Developers (front end and back end) and you.

On your first day, the Scrum Master asks you for two things:

1. A short, written plan that shows how the team will build the app (SDLC) and how you will test it (STLC), side by side.
2. A working Jira project where the team can see the backlog and start Sprint 1.

The Monday demo walked through the same kind of work with a worked example. This exercise asks you to produce your own version, in your own words, with your own Jira site.

## Project 1 milestone for today

**Milestone 1: SDLC/STLC plan v1 and Jira project QEA ready.**

By the end of the exercise you have (a) a written SDLC/STLC plan for Project 1, (b) a lifecycle diagram, and (c) a Jira Scrum project with an epic, at least 5 user stories, a ranked backlog, and Sprint 1 started. Tomorrow you will keep using this Jira project, so keep it.

## Learning objectives

By the end of this exercise you can:

- Choose a delivery model for a real product and justify it with the decision criteria from the lessons.
- Describe what happens in each SDLC phase and where the QE is involved.
- Map STLC phases to SDLC phases and write entry and exit criteria for them.
- Draw a lifecycle diagram that shows the SDLC with the STLC running alongside.
- Create a Jira Scrum project, write user stories with Given/When/Then acceptance criteria, estimate with story points, and run the first steps of a sprint.
- Explain what a QE does in each Scrum ceremony.

## Prerequisites: what to review first

Skim these Monday lessons (you do not need to memorise them; use them as a reference while you work).

| Lesson (written/1-monday) | Sections to review |
|---|---|
| SDLC Fundamentals | "3. What is the SDLC?", phases 1 to 7 (sections 6 to 12), "13. Phase summary table", "16. Roles at a glance", "Connecting SDLC to Project 1 - QE Foundations" |
| Software Testing Life Cycle (STLC) | "4. How the STLC runs in parallel with the SDLC", "5. Key vocabulary", "12. All six phases at a glance", "14. How the STLC adapts inside Agile sprints", "15. Worked example: User Login through all six phases" |
| Waterfall, Agile, Scrum, Kanban and Hybrid Approaches | "8. Side-by-side comparison of all approaches", "9. Decision guide: choosing a model", "12. Where does the QE / tester fit in each model?" |
| Agile Roles and Responsibilities | "3.4 Where Do Testers and QE Fit?", Definition of Ready and Definition of Done |
| Scrum Ceremonies and the Sprint Lifecycle | "5. User Stories", "6. Acceptance Criteria and Given/When/Then", "7. Estimation Basics", the five Events in Depth, "Testing Activities by Sprint Phase" |
| Introduction to Jira | "5. Core Vocabulary", "6. Creating an Account and a Site", "8. Creating a Project", "9. The Backlog View and Creating Your First Issues", "11. Running a Sprint in Jira", "15. Inviting Users and Basic Permissions" |

The Monday demo file `demos/1-monday/code/demo_sdlc_stlc_agile.md` holds the worked examples: the Project 1 product brief (section 1), the model scoring matrix (section 2), the STLC-to-SDLC mapping table (section 3), and the Jira assets (section 4). Look at them when you need to see what "good" looks like, but write your own answers.

## The Project 1 product brief (summary)

| Item | Value |
|---|---|
| Product goal | "Give new visitors a simple, safe way to create an account and sign in." |
| Platforms | Web, latest Chrome and Firefox |
| Features | F1 Register with email and password; F2 Registration validation messages; F3 Log in; F4 Safe, generic message when login fails; F5 Account lockout after 5 failed attempts; F6 Log out; F7 My account page (later); F8 Reset a forgotten password (later, not yet refined) |
| Rules | Password at least 8 characters with a letter and a digit; emails are not case-sensitive; never reveal whether an email is registered; no single sign-on and no "Remember me" in this release |
| Quality risks | Messages that reveal registered emails; lockout is slow to test; weak password validation; test data that gets used up |

## Time estimate and suggested time plan

Total: 2 to 3 hours. Aim for about 2 hours 45 minutes including breaks.

| Part | Task | Suggested time |
|---|---|---|
| 0 | Read this brief, review lessons, set up files | 15 min |
| 1 | Choose and justify an SDLC model | 20 min |
| 2 | SDLC phases table | 20 min |
| 3 | STLC to SDLC mapping with entry/exit criteria | 25 min |
| 4 | Lifecycle diagram | 15 min |
| 5 | Jira setup (project, epic, stories, sprint, screenshots, export) | 55 min |
| 6 | Reflection on Scrum ceremonies | 10 min |
| - | Final check against the Definition of Done | 5 min |
| | **Total** | **165 min (2 h 45 min)** |

## Tools needed

- A free Jira Cloud account (sign up with your own email; the free plan is enough).
- A text or markdown editor (VS Code, Notepad++, or any editor you like).
- Optional: the Mermaid live editor (https://mermaid.live) to preview your diagram. You can also hand-draw the diagram and submit a photo.
- A screenshot tool.

## Starter files

Copy the `templates/` folder to your working folder. It contains:

| File | Use |
|---|---|
| `my-sdlc-stlc-plan-template.md` | Worksheet for Parts 1, 2, 3 and 6 (rename to `my-sdlc-stlc-plan.md`) |
| `lifecycle-diagram-template.mermaid` | Skeleton for Part 4 |
| `jira-setup-checklist.md` | Step-by-step checklist for Part 5 |
| `user-story-template.md` | Story format, Given/When/Then, points, Definition of Ready |

## Tasks

### Part 1: Choose and justify an SDLC model (about 20 min)

Pick one delivery model for Project 1 from: Waterfall, V-Model, Agile/Scrum, Kanban, Hybrid.

1. Use the decision criteria in the lessons (requirements stability, risk, delivery speed, customer involvement, testing timing, documentation, change tolerance, team size). In your plan, fill a small table that rates each criterion for Project 1 (what is true about this project) and says which model it favours.
2. Write a justification of **150 to 250 words**. It must name your chosen model, give at least three criteria as reasons, and say why one other model is a weaker fit.

### Part 2: Fill the SDLC phases table (about 20 min)

For each of the 7 SDLC phases (Planning, Requirements Analysis, Design, Implementation, Testing, Deployment, Maintenance), write for Project 1:

- Key activities (2 or more, specific to registration and login),
- Deliverables (1 or more),
- QE involvement (what you personally do in this phase).

Even though you chose an Agile model, phases still happen; they just repeat in each sprint. Add one line saying how they repeat in your chosen model.

### Part 3: Map STLC phases to SDLC phases (about 25 min)

1. List the 6 STLC phases (Requirement Analysis, Test Planning, Test Case Development, Test Environment Setup, Test Execution, Test Cycle Closure).
2. For each, name the SDLC phase it lines up with and give one activity for the **login/registration feature**.
3. Write **entry and exit criteria for at least 3** STLC phases. Criteria must be checkable (for example "questions logged and answered", not "everything is clear").
4. Test cases appear only as titles today (for example "Valid login"). Detailed test design comes later in the week.

### Part 4: Draw a one-page lifecycle diagram (about 15 min)

Create a single diagram that shows the SDLC phases in one lane and the STLC phases in a second lane alongside, with links between them. Use the Mermaid template, or draw it by hand and submit a clear photo. It must be readable on one page.

### Part 5: Jira setup (about 55 min)

Follow `jira-setup-checklist.md`. In summary:

1. Create a free Jira Cloud site and a **Scrum** project named "Project 1 - QE Foundations" with key **QEA** (if QEA is already taken on your site, use a unique variation such as QEA plus your initials, for example `QEAJS`; Jira keys cannot contain a hyphen, so write it without one, and note the key you used in your plan).
2. Create **1 epic**: "User Registration and Login".
3. Create **at least 5 user stories** under that epic. Each story needs: the "As a ... I want ... so that ..." sentence, **at least 2 acceptance criteria in Given/When/Then** form, and **story points** (use the Fibonacci scale from the Scrum lesson).
4. **Order the backlog** so the most valuable and riskiest stories are at the top.
5. **Roles:** you are the project admin. Invite a placeholder teammate (a second email you own, or invite a classmate) and assign one story to them; state in your plan which Scrum role each person plays (for example you as QE, placeholder as Product Owner).
6. **Plan Sprint 1:** create a sprint, drag in stories that fit a sensible capacity, write a **sprint goal**, and **start the sprint**.
7. **Move one card** on the board from To Do to In Progress.
8. Capture screenshots: backlog, epic with stories, one story detail showing acceptance criteria, active sprint board with the sprint goal and a moved card, and the burndown or sprint report (if the burndown shows no data yet, screenshot the empty chart; Jira needs a day or two to draw it).
9. Export the backlog to CSV.

### Part 6: Reflection (about 10 min)

Write **5 sentences** (one per Scrum event) on what a QE does in each: Backlog Refinement, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective. Put these at the bottom of your plan file.

## Deliverables (exact filenames)

Place everything in a folder named `week3-monday-exercise-<your-name>/`.

| File or folder | Contents |
|---|---|
| `my-sdlc-stlc-plan.md` | Parts 1, 2, 3 and 6 (model choice and justification, SDLC table, STLC mapping with entry/exit criteria, reflection) |
| `lifecycle-diagram.mermaid` (or `lifecycle-diagram.png` / `.jpg` for a hand-drawn or exported version) | Part 4 |
| `jira-screenshots/` | `01-backlog.png`, `02-epic-and-stories.png`, `03-story-detail.png`, `04-sprint-board.png`, `05-burndown-or-sprint-report.png` |
| `jira-backlog-export.csv` | Part 5 export of the epic and stories |

## Definition of Done (checklist)

Tick each item before you submit.

**Part 1**
- [ ] A single model is chosen and named.
- [ ] The criteria table covers at least 6 criteria with a Project 1 rating each.
- [ ] The justification is 150 to 250 words, cites at least 3 criteria, and compares against at least one other model.

**Part 2**
- [ ] The table has all 7 SDLC phases.
- [ ] Every phase has at least 2 activities, at least 1 deliverable, and a QE involvement entry specific to registration/login.
- [ ] One sentence explains how the phases repeat in your chosen model.

**Part 3**
- [ ] The plan includes all 6 STLC phases, each mapped to an SDLC phase.
- [ ] At least 3 STLC phases have both entry and exit criteria, and every criterion is checkable.
- [ ] Each mapped phase has a login/registration activity (test cases appear only as titles).

**Part 4**
- [ ] The diagram shows the 7 SDLC phases and the 6 STLC phases, in two distinguishable lanes.
- [ ] At least 6 links connect STLC phases to the SDLC phases they line up with.
- [ ] The diagram fits on one page and is readable (no cut-off text).

**Part 5**
- [ ] A Scrum project exists with key QEA (or QEA variation) and 1 epic.
- [ ] At least 5 stories are under the epic, each with at least 2 Given/When/Then acceptance criteria and a story point value.
- [ ] The backlog is ordered, and the order is explained in one sentence in your plan.
- [ ] A second person (placeholder) is invited, and roles are listed in your plan.
- [ ] Sprint 1 has a written sprint goal, contains stories, and is started.
- [ ] At least one card is moved on the board.
- [ ] All 5 named screenshots are in `jira-screenshots/`.
- [ ] `jira-backlog-export.csv` opens and lists the epic and at least 5 stories.

**Part 6**
- [ ] The reflection has 5 sentences, one per Scrum event, each naming a concrete QE action.

**General**
- [ ] File names match the Deliverables table exactly.
- [ ] You can explain every answer in your own words.

## Grading rubric (100 points)

| Criterion | Weight | Excellent | OK | Needs work |
|---|---|---|---|---|
| Part 1: Model choice and justification | 10 | Clear choice, 3+ criteria applied to Project 1, compares another model, 150 to 250 words | Choice made but reasons are generic or only 2 criteria | No choice, or reasoning not tied to Project 1 |
| Part 2: SDLC phases table | 15 | All 7 phases, specific activities/deliverables, QE role clear in each | All phases but some entries generic or QE role vague | Missing phases or copied lesson text without Project 1 detail |
| Part 3: STLC mapping and criteria | 20 | All 6 STLC phases mapped; 3+ with checkable entry and exit criteria; login-specific activities | Mapping correct but criteria vague or only partly checkable | Mapping wrong or criteria missing |
| Part 4: Lifecycle diagram | 10 | Both lanes, all phases, 6+ links, readable | Both lanes but some phases or links missing | Single lane or unreadable |
| Part 5a: Jira project, epic, stories | 20 | 5+ stories, each with 2+ Given/When/Then criteria and points; ordered backlog with reason | 5 stories but weak criteria (not testable) or missing points | Fewer than 5 stories or no acceptance criteria |
| Part 5b: Sprint, roles, evidence | 15 | Sprint goal written, sprint started, card moved, all 5 screenshots, CSV export | Sprint started but goal vague, or 1 to 2 screenshots missing | Sprint not started or evidence missing |
| Part 6: Reflection | 5 | 5 sentences, one concrete QE action per event | Events covered but actions generic | Missing events |
| Quality of submission | 5 | Correct filenames, tidy, consistent names with Project 1 | Minor naming issues | Disorganised or incomplete submission |
| **Total** | **100** | | | |

## Stuck? Hints (try first, then open)

<details>
<summary>Part 1 hint</summary>

Start with the project facts: team size, whether details will change, how available the Product Owner is, and how early you want testing. Then ask which model each fact favours. Write the model name only after you have filled the criteria table.
</details>

<details>
<summary>Part 2 hint</summary>

For each phase ask three questions: what happens, what is produced, and what could I, as the QE, do here to prevent a defect later? "Reviewing requirements" is a QE activity before any code exists.
</details>

<details>
<summary>Part 3 hint</summary>

An entry criterion answers "what must be true before this phase may start?" An exit criterion answers "how do we know it is finished?" If you cannot check it with a yes or no, rewrite it. Remember that STLC phases overlap and sometimes loop.
</details>

<details>
<summary>Part 4 hint</summary>

Use two subgraphs, one per lane, and connect each STLC box to the SDLC box it starts with. Preview in the Mermaid live editor; if it shows an error, check for missing quotation marks or stray brackets.
</details>

<details>
<summary>Part 5 hint</summary>

If a story is hard to estimate, compare it with another story: is it bigger or smaller? If you cannot write two testable Given/When/Then criteria, the story is probably too vague; split it or ask a question. If Jira does not show the field for story points, look at project settings for issue fields.
</details>

<details>
<summary>Part 6 hint</summary>

Think about what questions, preparations or checks a QE brings to each event, not what the whole team does.
</details>

## Common mistakes

- Choosing a model because it sounds modern, without tying reasons to Project 1 facts.
- Writing "test the app" as QE involvement in every phase.
- Entry/exit criteria that cannot be checked ("good quality", "all clear").
- Acceptance criteria that describe screens instead of behaviour, or that have no concrete expected message.
- Stories that are really tasks ("Create database table") rather than user value.
- A sprint goal that is just a list of ticket numbers.
- Starting the sprint without a goal, or forgetting to move a card before taking the board screenshot.
- Re-saving the CSV in a spreadsheet tool and breaking the quoting of multi-line descriptions.
- Using later-week topics (defect states, BVA/EP) in your plan; they are not needed today.

## Stretch goals (optional)

1. Add a **Kanban board view** for the same backlog (create a Kanban project or filter) and write 3 sentences comparing it with your Scrum board.
2. **Use an AI assistant to draft stories, then critique them.** Ask the assistant for 5 more stories for Project 1 and review the output with these questions:
   1. Is every story testable? Can you write at least two Given/When/Then criteria with a concrete expected result?
   2. Does anything contradict the product brief (password rules, generic error message, lockout after 5 attempts, no single sign-on)?
   3. Did the assistant invent features, numbers or rules that nobody asked for, and would you be comfortable defending each one to the Product Owner?

   Keep only what you can defend, and note what you changed.

## Submission instructions

Place all deliverables in your `week3-monday-exercise-<your-name>/` folder and share them using the course's submission method (as announced by your trainer). Make sure your Jira site stays active, since your trainer may ask to view it.

## What's next

Tuesday builds directly on this Jira project: you will keep working in the QEA project, so do not delete it. Keep your story keys and sprint intact.

## Note on demo materials

The Monday demo materials are the worked examples for this exercise. Use them to check your approach and naming (QEA key, "User Registration and Login" epic, the story style), but your plan, stories and screenshots must be your own work.
