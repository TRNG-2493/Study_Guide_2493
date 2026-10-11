# Scrum Ceremonies and the Sprint Lifecycle

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain what a Sprint is, why it has a fixed length, and why the Sprint Goal is protected from changes that endanger it.
2. Walk through a complete 2-week sprint from the first Sprint Planning session to the final Retrospective, naming every event and what happens on each day.
3. Describe the three Scrum artifacts (Product Backlog, Sprint Backlog, Increment) and the commitment attached to each (Product Goal, Sprint Goal, Definition of Done).
4. Write a user story in the "As a / I want / So that" format and attach simple Given/When/Then acceptance criteria to it.
5. Explain story points, planning poker, velocity, and how to read a basic burndown chart.
6. For each of the five Scrum events (Backlog Refinement, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective), state its purpose, attendees, timebox, inputs, outputs, and what a Quality Engineer (QE) does there.
7. Show where testing activities fit inside a sprint, and recognize that testing is continuous rather than a phase at the end.
8. Describe what a team does when a Sprint Goal is at risk or a serious bug is found late.
9. Apply all of this to "Project 1 - QE Foundations" by drafting a sprint goal and three user stories with acceptance criteria.

---

## Why This Matters

Earlier today you learned the big picture: the Software Development Life Cycle (SDLC), the Software Testing Life Cycle (STLC), a quick tour of delivery models (with Scrum named as one of the most popular), and the Agile roles (Product Owner, Scrum Master, and Developers, which includes Quality Engineers). You now know **who** is on a Scrum team.

This lesson answers the next question: **what do they actually do, and when?**

If you join a software team as a Quality Engineer, the odds are very high that you will be working in sprints. Your calendar will fill with named meetings: Sprint Planning, Daily Scrum, Refinement, Review, Retrospective. If you do not understand why each one exists, they feel like "too many meetings". If you do understand them, each one becomes a moment where quality gets built into the product, long before a defect reaches a customer.

Here is the key idea: **in a Scrum team, quality is not a gate at the end; it is a thread that runs through every event.** Quality Engineers who know how to contribute at each ceremony (asking sharp questions during refinement, raising risks in planning, giving honest test status in the daily meeting, demonstrating verified work in the review, and suggesting process improvements in the retrospective) become the people teams trust and rely on.

You will also use this knowledge directly this week. Every day, you will plan quality for "Project 1 - QE Foundations", a sample web app. Today you will practice thinking in sprints for that app.

A note on scope: this lesson covers the Scrum rhythm and where testing fits. It only points toward Jira (the tool most teams use to track sprint work); Jira mechanics come in the next lesson. Defect lifecycle and test-design techniques are covered on later days, so here we will mention bugs and tests only at the level needed to understand the sprint flow.

---

## The Concept

### 1. An Analogy to Hold Onto: The Restaurant Service Rhythm

Imagine a busy restaurant kitchen. It does not simply "cook food all day". It runs on a rhythm:

- **Before service:** the chef and the manager decide today's menu and what the kitchen can realistically deliver (that is like Sprint Planning).
- **During service:** a short huddle at the pass keeps the line coordinated (that is like the Daily Scrum). Meanwhile, the chef is thinking ahead about tomorrow's specials and checking the pantry (that is like Backlog Refinement).
- **End of service:** the team tastes what was served and hears from the dining room (that is like the Sprint Review).
- **After close:** the staff talk about what slowed them down and what to fix for tomorrow (that is like the Retrospective).

And the quality-control person, the one who tastes every dish before it leaves the kitchen, is not stationed at the exit door at the end of the night. They taste continuously, from the first prep to the last plate. That is exactly how a QE works in a sprint.

A second analogy: **a relay race.** In a traditional "waterfall" project, the baton passes from analysts to developers to testers, and testers only run once everyone else has finished. If the baton is dropped at the end, the whole race is lost. In Scrum, the team runs together in short laps (sprints), and after every lap there is a working, tested product in hand.

### 2. What Is Scrum? A Quick Reminder

**Scrum** is a lightweight framework (a set of rules and roles, not a detailed methodology) that helps teams deliver complex products in small, regular steps. Its official rulebook is the **Scrum Guide** (maintained by Ken Schwaber and Jeff Sutherland, current edition 2020). Scrum rests on three ideas:

- **Transparency:** everyone can see the real state of the work.
- **Inspection:** the team regularly checks its work and progress.
- **Adaptation:** the team changes course when inspection shows a problem.

The five Scrum events exist precisely to create regular chances to inspect and adapt. Many people call the events **ceremonies**; the Scrum Guide itself uses the word "events", but you will hear both in the workplace, and they mean the same thing.

### 3. The Sprint

A **Sprint** is a fixed-length period of time during which the team turns selected work into a usable, finished piece of the product. All the other events happen inside the Sprint (or, in the case of refinement, continuously during it). Think of the Sprint as the container that holds everything else.

**Key rules of a Sprint:**

| Rule | What it means | Why it exists |
|---|---|---|
| **Timeboxed** | A Sprint lasts one month or less. Most teams choose 1, 2, 3, or 4 weeks. | Short cycles mean quick feedback and limit how wrong a plan can go. |
| **Fixed length** | Once a team chooses a length (say, 2 weeks), every Sprint is that length. The Sprint ends on its date, even if work is unfinished. | A steady rhythm makes planning predictable and removes the temptation to "just take a few more days". |
| **Has a goal** | Every Sprint has a Sprint Goal, a single, clear objective for the Sprint. | The goal gives the work meaning and gives the team flexibility in how to achieve it. |
| **Starts right after the previous one** | A new Sprint begins immediately when the last ends. There is no gap. | Continuous flow of value. |
| **No changes that endanger the Sprint Goal** | During the Sprint, no changes are made that would endanger the Sprint Goal; quality does not decrease; the Product Backlog is refined as needed; scope may be clarified and renegotiated with the Product Owner as more is learned. | Protects the team's focus while still allowing sensible learning. |

**Why 2 weeks is the most common choice:** it is long enough to complete meaningful work and short enough that a mistake costs at most two weeks. Throughout this lesson we use a **2-week (10 working days) sprint** as our example.

**Can a Sprint be cancelled?** Only the Product Owner has the authority to cancel a Sprint, and only if the Sprint Goal becomes obsolete (for example, the business pivots and the goal no longer makes sense). This is rare.

**What does "no scope changes that endanger the goal" really mean?** It does **not** mean "nothing can ever change". It means that new work cannot be pushed into the Sprint in a way that threatens the goal. A useful rule of thumb: if a new request arrives mid-Sprint, the Product Owner places it in the Product Backlog for a future Sprint, unless it is truly urgent, in which case the team and Product Owner discuss what to trade out so the Sprint Goal stays achievable. Think of the restaurant: if a customer asks for a dish that is not on the menu while the kitchen is at capacity, the manager does not simply add it; they decide whether it replaces something else or waits until tomorrow.

### 4. The Artifacts and Their Commitments

An **artifact** is something the team creates and maintains that represents work or value. Scrum defines three artifacts, and each has a matching **commitment**, a statement that gives the artifact focus and a way to measure progress.

| Artifact | What it is | Commitment | What the commitment means |
|---|---|---|---|
| **Product Backlog** | An ordered, ever-changing list of everything that might be needed in the product: features, improvements, fixes. Owned by the Product Owner. | **Product Goal** | The long-term objective for the product (for example, "Let first-time shoppers find and buy a product in under three minutes"). The backlog items exist to fulfil it. |
| **Sprint Backlog** | The Product Backlog Items (PBIs) the team selected for this Sprint, plus a plan for delivering them. Owned by the Developers (including QEs). | **Sprint Goal** | The single objective for this Sprint (for example, "A shopper can add items to a cart and see an accurate total"). |
| **Increment** | A concrete, usable step toward the Product Goal. Every Sprint produces at least one Increment, and increments are cumulative: each builds on the last. | **Definition of Done (DoD)** | A shared checklist describing what "finished" means. Work only becomes part of the Increment when it meets the DoD. |

**A closer look at the Definition of Done.** This is the artifact commitment most relevant to QEs. The DoD is a **team-wide, written agreement** about quality. An example DoD for Project 1 might be:

- Code reviewed by at least one other developer.
- Unit tests written and passing.
- Acceptance criteria verified by testing.
- No open critical or high-severity bugs related to the story.
- Regression tests for affected areas executed and passing.
- Documentation or release notes updated.
- Product Owner has accepted the story.

Notice how many items are about quality. As a QE, you will often help write and sharpen the DoD. A story that is "99 percent done" is **not done**. This is an important mindset: in Scrum, work is either Done or it is not; there is no partial credit toward the Increment.

**A related idea: Definition of Ready (DoR).** Many teams also keep a *Definition of Ready*, a checklist that a story must pass before it can be pulled into a Sprint (for example, "has acceptance criteria, has been estimated, has no unresolved dependencies"). It is not an official Scrum artifact, but it is very widely used and QEs often help shape it.

### 5. User Stories

How do we write down what the product should do? Most Scrum teams use **user stories**: short descriptions of a feature told from the point of view of the person who wants it.

**The standard template:**

> **As a** [type of user],
> **I want** [some goal or capability],
> **So that** [the benefit or reason].

**Example:**

> As a returning shopper, I want to log in with my email and password so that I can see my saved cart and past orders.

Each part has a purpose:

- **As a** identifies *who* benefits (a role, not "the system").
- **I want** states *what* they need, without dictating *how* it is built.
- **So that** explains *why*, the value. This is the part teams most often forget, and it is also the part that lets QEs judge whether a solution truly meets the need.

**What makes a good story?** A common checklist is **INVEST**:

| Letter | Meaning | In plain words |
|---|---|---|
| **I** | Independent | Can be built and tested without needing many other stories first. |
| **N** | Negotiable | The details can be discussed; it is a conversation starter, not a contract. |
| **V** | Valuable | Delivers value to a user or the business. |
| **E** | Estimable | The team can roughly judge its size. |
| **S** | Small | Fits comfortably inside one Sprint. |
| **T** | Testable | You can describe how to prove it works. |

The last letter, **Testable**, is the QE's special lens. If you cannot imagine how to test a story, it is not clear enough yet, and the QE should say so during refinement.

### 6. Acceptance Criteria and Given/When/Then

A user story says what the user wants. **Acceptance criteria (AC)** say how we will know it is correctly done. They are the specific, checkable conditions the story must satisfy before the Product Owner accepts it. They are also the seed of your test cases (you will learn formal test design later this week).

Acceptance criteria can be a simple bulleted list:

- The login form has email and password fields.
- A wrong password shows the message "Incorrect email or password".
- After five failed attempts, the account is locked for 15 minutes.

Many teams prefer a scenario format called **Given / When / Then**, which describes behavior as a tiny story:

- **Given** a starting situation (the context or preconditions),
- **When** something happens (an action by the user or system),
- **Then** an observable result is expected (the outcome).

**Example:**

> **Scenario:** Login with a wrong password
> **Given** I am on the login page and I have a registered account
> **When** I enter my correct email and an incorrect password and click "Log in"
> **Then** I see the message "Incorrect email or password" and I stay on the login page

You can add **And** to extend any of the three parts. Notice that every Then is *observable*: you can look at the screen and say yes or no. Vague criteria such as "login should be fast and user friendly" are not testable; improved versions would say "the dashboard appears within 3 seconds of a successful login".

**Tip for beginners:** write one scenario per behavior. If a scenario has many When and Then lines, it probably hides several behaviors and should be split.

### 7. Estimation Basics: Story Points, Planning Poker, Velocity

Teams need a rough sense of how much they can fit in a Sprint. Rather than estimating in hours (which are often wrong and feel like promises), many teams estimate **relative size** using **story points**.

**Story points** are unit-less numbers that represent the overall effort, complexity, and uncertainty of a story compared with other stories. A story worth 8 points is not "8 hours"; it is "roughly twice as big and risky as a 4-point story". Points commonly come from a modified Fibonacci sequence: **1, 2, 3, 5, 8, 13, 21**. The gaps widen as numbers grow because large estimates are naturally less precise.

Notice that estimates include testing effort. A story that is easy to code but difficult to test (for example, it touches many browsers or has many data combinations) should have a higher estimate. This is why QEs must be in the estimation conversation.

**Planning poker** is a friendly technique for estimating together:

1. The Product Owner (or someone) reads the story and answers questions.
2. Each Developer (including QEs) privately picks a card showing their estimate.
3. Everyone reveals at the same time (so nobody is influenced by others).
4. If estimates differ widely, the highest and lowest voters explain their thinking. This is where hidden assumptions come out. A QE who voted 8 while developers voted 3 might say, "this needs checking on three browsers and two payment types".
5. The team re-votes until estimates converge.

**Velocity** is the total number of story points a team completes (meets the DoD) in a Sprint. If a team finished 24 points in Sprint 1, 28 in Sprint 2, and 26 in Sprint 3, their average velocity is about 26 points. The team uses it as a forecasting aid: "next Sprint we will probably take on around 26 points". Two cautions: velocity belongs to **one team** and must never be used to compare teams or to pressure people; and only fully Done stories count. Half-done stories count as zero.

### 8. The Burndown Chart

A **Sprint burndown chart** is a simple graph that shows how much work remains in the Sprint over time.

- The vertical axis shows remaining work (usually story points).
- The horizontal axis shows the days of the Sprint.
- An **ideal line** slopes steadily from the total committed work at the start down to zero at the end.
- The **actual line** shows reality, updated daily.

```
Remaining
points
 30 |*
    | *.
 25 |   *.  (ideal line = dots)
    |     *.        actual = *
 20 |   *    *.
    |      *    *.
 15 |        *     *.
    |          *      *.
 10 |            *       *.
    |              *        *.
  5 |                *         *.
    |                    *        *.
  0 +--+--+--+--+--+--+--+--+--+--+--
    D1 D2 D3 D4 D5 D6 D7 D8 D9 D10
```

How to read it (without over-analyzing):

- **Actual line above the ideal line:** the team is behind. Discuss why at the Daily Scrum.
- **Actual line below the ideal line:** the team is ahead (or may have estimated too generously).
- **Flat line followed by a cliff:** work is piling up as "in testing" and then finishing all at once at the end. This is a classic sign of testing being squeezed to the last days. QEs should recognize this pattern and raise it early.
- **Line going up:** scope was added, or work was re-estimated higher.

A burndown chart is a **conversation tool**, not a report card. It is one way to make progress transparent.

---

## The Sprint Lifecycle End to End

Now let us put everything in order. Below is the lifecycle of a **2-week sprint** (10 working days, Monday to Friday of the following week).

### The Timeline (ASCII)

```
 SPRINT N-1                 SPRINT N  (2 weeks = 10 working days)                    SPRINT N+1
 ends                                                                                  begins
   |                                                                                     |
   v                                                                                     v
 +-----------+------------------------------------------------------------+-----------+------------
 | Sprint    |  WEEK 1                    |  WEEK 2                       | Review +  | Sprint
 | Planning  |  D1  D2  D3  D4  D5        |  D6  D7  D8  D9  D10          | Retro     | Planning
 | (D1 am)   |                            |                               | (D10 pm)  | (next D1)
 +-----------+------------------------------------------------------------+-----------+------------

 Day:        D1   D2   D3   D4   D5   D6   D7   D8   D9   D10
             |    |    |    |    |    |    |    |    |    |
 Planning    [=====]                                          (up to 4h)
 Daily       o    o    o    o    o    o    o    o    o    o   (15 min every day)
 Refinement            [==]                [==]               (ongoing; 1-2 slots)
 Build+Test  ---continuous: stories are built AND tested as they finish---->
 Regression                       [====]           [======]   (targeted, then final)
 Review                                                  [==]  (up to 2h, D10)
 Retro                                                      [=] (up to 1.5h, D10)
```

The important thing to see in this picture is that **building and testing run together the whole way along**, while the events act like regular "check-in stations".

### The Timeline (Table)

| Day | Events and Activities | Typical QE Focus |
|---|---|---|
| **Day 1 (Mon)** | Sprint Planning (morning, up to 4 hours). Daily Scrum starts from this day or the next, according to team habit. | Clarify acceptance criteria, flag risks, estimate testing effort, help set the Sprint Goal, plan test environments and data. |
| **Day 2 (Tue)** | Daily Scrum. Developers begin building the first stories. | Prepare test cases from acceptance criteria; set up test data; review designs and offer early feedback. |
| **Day 3 (Wed)** | Daily Scrum. Refinement session #1 (about 1 hour) for upcoming Sprints. | Test the first finished story (often "story 1 is done in dev"); ask refinement questions about testability of future stories. |
| **Day 4 (Thu)** | Daily Scrum. | Continue testing as stories land; report issues directly to the developer the moment you find them. |
| **Day 5 (Fri)** | Daily Scrum. Mid-sprint check: is the Sprint Goal still on track? | Run first rounds of regression on completed areas; update team on test status. |
| **Day 6 (Mon)** | Daily Scrum. Burndown inspected; adjust plan if needed. | Re-verify fixed defects; look at risk areas. |
| **Day 7 (Tue)** | Daily Scrum. | Test remaining stories; start exploratory sessions on integrated features. |
| **Day 8 (Wed)** | Daily Scrum. Refinement session #2 (about 1 hour) to prepare the next Sprint. | Contribute to estimates for next Sprint; point out missing criteria. |
| **Day 9 (Thu)** | Daily Scrum. "Code freeze" for the Sprint (a team agreement: no new features, only fixes). | Run full regression suite; hardening (see below); verify all stories against the Definition of Done. |
| **Day 10 (Fri)** | Daily Scrum. Sprint Review (up to 2 hours), then Sprint Retrospective (up to 1.5 hours). | Demonstrate or confirm tested work in the review; contribute data and ideas to the retrospective. |
| **Day 11 (Mon)** | The next Sprint starts immediately with its own Sprint Planning. | Bring retrospective actions into practice. |

Note: this is one sensible pattern, not a law. Teams adjust meeting days. What stays fixed is the **order** (Planning first; Review then Retrospective last) and the **fixed length**.

### Timeboxes at a Glance

The Scrum Guide gives *maximum* timeboxes for a **one-month** Sprint. For shorter Sprints the events are usually shorter. The commonly used figures for a 2-week sprint:

| Event | Max for 1-month Sprint (Scrum Guide) | Typical for 2-week Sprint |
|---|---|---|
| Sprint Planning | 8 hours | Up to 4 hours |
| Daily Scrum | 15 minutes | 15 minutes |
| Sprint Review | 4 hours | Up to 2 hours |
| Sprint Retrospective | 3 hours | Up to 1.5 hours |
| Backlog Refinement | Ongoing activity (many teams spend up to about 10 percent of capacity) | 1-2 sessions of about 1 hour each |

---

## The Events in Depth

### Event 1: Backlog Refinement (Grooming)

**What it is.** Refinement (formerly called "grooming") is the ongoing activity of breaking down, clarifying, and estimating Product Backlog items so they are ready to be pulled into future Sprints. The Scrum Guide describes it as an **activity**, not a formal event, because it is not time-boxed in the same strict way and it can happen whenever needed. Most teams nonetheless schedule regular sessions.

**Analogy.** A restaurant chef writing up tomorrow's prep list and checking whether the ingredients for a new dish are actually available, so that when service begins nothing is a surprise.

| Aspect | Details |
|---|---|
| **Purpose** | Make upcoming stories small, clear, estimated, and testable so Sprint Planning runs smoothly. |
| **Who attends** | Product Owner (leads the discussion of value), Developers including QEs, and the Scrum Master (facilitating if asked). |
| **Timebox (2-week sprint)** | Ongoing; typically 1-2 sessions of about 1 hour each, and no more than roughly 10 percent of the team's capacity. |
| **Inputs** | The ordered Product Backlog; fresh feedback from the last Review; business changes; technical discoveries. |
| **Outputs** | Stories that are clearer, split into smaller pieces where needed, with acceptance criteria and estimates; re-ordered Product Backlog; list of open questions with owners. |

**QE responsibilities in refinement:**

- Ask "how will we test this?" for every story. If nobody can answer, the story is not ready.
- Challenge vague words ("fast", "easy", "appropriate") and ask for measurable language.
- Help write or review acceptance criteria, including negative cases ("what happens if the user enters nothing?").
- Raise dependencies and environment needs (test data, third-party services, devices).
- Contribute to estimates, including testing effort.
- Spot stories that are too large to finish and verify in one Sprint, and propose splitting them.

**Example dialogue.**

> **Product Owner:** The next story is "As a shopper, I want to search for products so that I can find what I need quickly."
> **Developer (Dev):** Search by name should be easy. I would say 3 points.
> **QE (Priya):** Before we vote, can we agree what "quickly" means? Is it results within two seconds?
> **Product Owner:** Yes, two seconds is fine for the first release.
> **QE:** And what should happen when nothing matches, or when the user searches for something with special characters?
> **Product Owner:** Show "No products found" with a suggestion to try another word. Special characters should not crash anything.
> **Dev:** That adds some work. Let me reconsider; maybe 5.
> **QE:** I would also say 5, because we need data with many product names and special characters.
> **Scrum Master:** Do we agree on 5, then? ... Great, I will note the acceptance criteria in the story.

**Common mistakes:**

- Treating refinement as a quick "just estimate it" meeting without discussing testing.
- Refining too far ahead (stories go stale), or too little (planning becomes chaotic).
- QEs skipping the session and then discovering untestable stories mid-Sprint.
- The Product Owner showing up without priorities, so the session is aimless.

---

### Event 2: Sprint Planning

**What it is.** The event that starts the Sprint. The whole Scrum Team collaborates to decide what will be worked on and how. The Scrum Guide organizes the discussion around three topics:

1. **Why is this Sprint valuable?** The Product Owner proposes how the product could increase its value in this Sprint, and the whole team collaborates to define a **Sprint Goal** that communicates why.
2. **What can be Done this Sprint?** The Developers select items from the Product Backlog to include, considering their past velocity and capacity (accounting for holidays, leave, other duties).
3. **How will the chosen work get done?** For each selected item, the Developers plan the work needed to create an Increment that meets the Definition of Done, often by breaking items into smaller tasks (a day or less each).

| Aspect | Details |
|---|---|
| **Purpose** | Agree on a Sprint Goal, choose the work that supports it, and plan how to do that work. |
| **Who attends** | The whole Scrum Team: Product Owner, Scrum Master, Developers (including QEs). Others may be invited for advice. |
| **Timebox (2-week sprint)** | Up to 4 hours (the Guide maximum is 8 hours for a one-month Sprint). Experienced teams often finish sooner. |
| **Inputs** | Refined Product Backlog; the Product Goal; the Definition of Done; the team's recent velocity; team capacity for this Sprint; results of the last Retrospective. |
| **Outputs** | The Sprint Goal; the Sprint Backlog (selected items plus a plan); shared understanding of what "done" looks like for each item. |

**QE responsibilities in planning:**

- Confirm each selected story has clear, testable acceptance criteria.
- Estimate testing effort and make sure it is included in the capacity discussion (otherwise the team over-commits, and testing is squeezed at the end).
- Flag risks: new third-party integrations, areas with a history of problems, tight deadlines for a browser or device combination.
- Identify what is needed to test: environments, test data, accounts, tools.
- Propose test tasks inside the Sprint Backlog (for example, "write test scenarios", "set up test data", "run regression for cart area").
- Help ensure the Sprint Goal is realistic and verifiable.
- Make sure planned work leaves time for fixing and retesting, not just first-time testing.

**Example script.**

> **Product Owner (Maria):** Our product goal is a smooth first-purchase experience. For this Sprint, I propose the goal: "A shopper can find a product, add it to a cart, and see an accurate total."
> **Dev (Sam):** That sounds good. We have capacity for about 26 points, based on the last three Sprints. One developer is off on Thursday of week 2.
> **QE (Priya):** Then I would suggest 24 points, to leave room for the leave and for retesting. Also, the cart story depends on product search being finished by Day 4, otherwise I cannot test the cart end to end until too late.
> **Dev (Sam):** Agreed, I will build search first.
> **Scrum Master (Ali):** Do we all agree the goal is clear and achievable?
> **Whole team:** Yes.
> **QE (Priya):** I will add tasks: prepare test data with at least 50 products, draft test scenarios on Day 2, and reserve Day 9 for regression.

**Common mistakes:**

- Over-committing because testing time was not counted.
- Choosing a list of unrelated stories and calling it a goal (a goal ties work together).
- Starting work on stories whose acceptance criteria are unclear.
- Product Owner dictating the amount of work instead of the Developers deciding how much they can take.
- Forgetting leave, holidays, and other commitments when judging capacity.

---

### Event 3: Daily Scrum (Stand-up)

**What it is.** A **15-minute** event for the Developers, held at the same time and place every working day of the Sprint. Its purpose is to inspect progress toward the Sprint Goal and adapt the Sprint Backlog as needed. It is often held standing up, hence the name "stand-up".

**Analogy.** The quick huddle at the kitchen pass: "Table 5 needs the soup first, we are out of salmon, and the grill is slow." It is not a status report to a manager; it is the team coordinating itself.

| Aspect | Details |
|---|---|
| **Purpose** | Check progress toward the Sprint Goal; surface blockers; make a plan for the next 24 hours. |
| **Who attends** | The Developers (including QEs). The Scrum Master ensures it happens and stays within timebox; the Product Owner may listen in but is not required. |
| **Timebox** | 15 minutes, every working day, same time and place. |
| **Inputs** | The Sprint Backlog and the board; the burndown; the Sprint Goal. |
| **Outputs** | An updated plan for the next 24 hours; blockers identified (and owners to resolve them); a possibly updated Sprint Backlog. Detailed discussion is taken offline afterwards. |

**Formats.** The Scrum Guide lets the Developers choose any structure that focuses on the Sprint Goal. A traditional, beginner-friendly format is the **three questions**:

1. What did I do yesterday that helped the team toward the Sprint Goal?
2. What will I do today to help the team toward the Sprint Goal?
3. Do I see any obstacle (blocker) that prevents me or the team from reaching the goal?

Another popular format is **walking the board**: instead of each person speaking, the team goes through the work items from right to left (closest to done first) and asks, "what is needed to finish this one?" This keeps the focus on the work and the goal rather than on the people.

**QE responsibilities:**

- Give a short, honest testing status in terms of stories, not test case counts ("Story 2 passed testing; Story 3 has one open issue the developer is looking at").
- Raise blockers early: environment down, no test data, a story not available for testing.
- Warn when work is piling up in "ready for test", threatening the Sprint Goal.
- Offer to pair with a developer on tricky issues.
- Keep the details short; ask for a follow-up conversation if needed.

**Example QE update (three-question format):**

> "Yesterday I tested the search story and found two issues: results ordering is wrong when two products share a name, and an empty search shows a blank page. I sent both to Sam; he has already fixed the first one. Today I will retest the fix and start testing the add-to-cart story. My blocker: the test environment still shows last week's product list, so I need the data refreshed. Can we sort that out right after this meeting?"

That update is good because it is specific, linked to the Sprint Goal (search and cart), names a blocker, and asks for help rather than complaining.

**Anti-patterns (things to avoid):**

| Anti-pattern | Why it hurts | Better approach |
|---|---|---|
| Status report to the Scrum Master or manager | Turns the team into reporters, not self-organizers. | Developers talk to each other about the goal. |
| Meeting runs to 30 or 45 minutes | Wastes time; people dread it. | Park deep discussions in a "parking lot" for after the meeting. |
| Problem-solving during the stand-up | Only two people care, others wait. | Note it; the relevant people meet right after. |
| "Nothing to report" or vague updates ("working on testing") | Hides risk. | Be specific about stories and status. |
| Always the same order, reading from a script | Becomes ritual with no value. | Walk the board, or vary the format. |
| QEs excluded because "testing is separate" | Hidden test status; late surprises. | QEs are Developers on the team and speak every day. |
| Blockers ignored | The team learns that raising problems is pointless. | Scrum Master tracks and resolves blockers the same day. |

---

### Event 4: Sprint Review (Demo)

**What it is.** The event at the end of the Sprint where the Scrum Team presents the results of its work to key stakeholders and discusses progress toward the Product Goal. It is a **working session**, not a one-way presentation. Many people call it "the demo".

**Analogy.** The end of service when the chef brings out the evening's dishes for the owner and regular customers to taste and comment on. If they say "this needs more spice", the kitchen listens and adjusts the menu.

| Aspect | Details |
|---|---|
| **Purpose** | Inspect the Increment; gather feedback from stakeholders; adapt the Product Backlog based on what was learned. |
| **Who attends** | The Scrum Team and key stakeholders (business representatives, users, support, management, other teams as relevant). |
| **Timebox (2-week sprint)** | Up to 2 hours (the Guide maximum is 4 hours for a one-month Sprint). |
| **Inputs** | The Increment (working, Done software); the Sprint Goal; the Product Backlog; the Definition of Done. |
| **Outputs** | Stakeholder feedback; a revised Product Backlog (new items, changed priorities); a shared view of what to do next; sometimes an updated release plan. |

**QE responsibilities in the review:**

- Make sure only work meeting the Definition of Done is demonstrated. A "demo" of something unverified is dangerous.
- Confirm the demo environment is stable and has realistic test data. Rehearse beforehand.
- Offer an honest view of quality: what is verified, what known issues remain, what was not covered and why.
- Support the demo by driving the application or explaining edge cases handled.
- Capture stakeholder feedback precisely (the QE's note-taking skill is valuable here) and help turn it into backlog items with clear expectations.
- Provide quality metrics only if they help the discussion (for example, "all 5 stories passed their acceptance criteria; 2 minor known issues are in the backlog").

**Example dialogue.**

> **Product Owner (Maria):** Welcome, everyone. Our Sprint Goal was: "A shopper can find a product, add it to a cart, and see an accurate total." Sam, please show us.
> **Dev (Sam):** [demonstrates search, then adding two items to the cart]
> **QE (Priya):** Just to add context: we verified the cart total with discounts, with quantities up to 99, and with an empty cart. One known issue: on very small phone screens the cart button wraps onto two lines. It is in the backlog as low priority.
> **Stakeholder (Dana, Customer Support):** Customers often ask whether the cart saves if they leave. Can we do that next?
> **Product Owner:** Great feedback. I will add "saved cart" to the backlog and we will refine it next week.
> **Scrum Master (Ali):** Any other feedback? ... Thank you everyone.

**Common mistakes:**

- Turning it into a slide presentation with no working software.
- Showing unfinished or unverified work, then apologizing.
- Stakeholders attending but nobody collecting their feedback.
- Treating the Review as an approval meeting rather than a feedback conversation.
- No QE voice in the room, so quality gaps and known issues are hidden.
- Skipping the Review because "nothing exciting was built".

---

### Event 5: Sprint Retrospective

**What it is.** The final event of the Sprint. The Scrum Team inspects how the Sprint went **with regard to individuals, interactions, processes, tools, and the Definition of Done**, and plans ways to increase quality and effectiveness. The Review looks at the *product*; the Retrospective looks at the *way of working*.

**Analogy.** After the restaurant closes, the staff sit down: "Orders got lost between waiters and the kitchen. Next time, let us use a clearer ticket system."

| Aspect | Details |
|---|---|
| **Purpose** | Identify what to keep, what to change, and commit to concrete improvements for the next Sprint. |
| **Who attends** | The Scrum Team only: Product Owner, Scrum Master, Developers (including QEs). It is a safe, private space. |
| **Timebox (2-week sprint)** | Up to 1.5 hours (the Guide maximum is 3 hours for a one-month Sprint). |
| **Inputs** | How the Sprint went: events, data (burndown, velocity, defect counts), the Definition of Done, team feelings. |
| **Outputs** | A short list of improvement actions with owners; the most impactful ones are added to the next Sprint Backlog so they actually happen. |

**Three core questions.** Most retrospectives revolve around:

1. What went well?
2. What did not go well (or what could be better)?
3. What will we change? (Concrete actions.)

**Popular formats:**

| Format | How it works | Best when |
|---|---|---|
| **Start / Stop / Continue** | Team lists what to *start* doing, *stop* doing, and *continue* doing. | A simple first format; beginner teams. |
| **4Ls** | Four columns: **Liked**, **Learned**, **Lacked**, **Longed for**. | The team wants to reflect on feelings and learning, not only process. |
| **Mad / Sad / Glad** | Team members place notes under the feelings they experienced. | There is tension or emotion to surface. |
| **Sailboat** | Wind (what pushed us forward), anchors (what slowed us), rocks (risks ahead). | A visual, creative change of pace. |

A good retrospective follows a rhythm: *set the stage*, *gather data*, *generate insights*, *decide what to do*, *close*. The key rule: **a retrospective that ends without at least one concrete action is wasted time.** Choose one or two improvements, not ten, and name an owner for each.

**QE responsibilities:**

- Share quality observations backed by facts: how many stories were still in testing on Day 9, how many defects were found late, how many came from unclear acceptance criteria, how long environments were unavailable.
- Suggest improvements to the Definition of Done, the testing approach, test automation, or collaboration with developers (for example, "let us have a developer demo each story to the QE before it moves to testing").
- Remain blame-free: focus on the process, not people ("the story arrived late" rather than "Sam was late").
- Volunteer to own improvement actions related to quality.
- Follow up on previous retrospective actions to see whether they helped.

**Example dialogue.**

> **Scrum Master (Ali):** Let us use Start/Stop/Continue. Take five minutes to write sticky notes.
> **QE (Priya):** I noticed that three of our five stories reached testing only on Day 8 or later. I would like us to **start** moving stories to testing as soon as they are built, rather than holding them until a batch is ready.
> **Dev (Sam):** I can accept that. A concern: sometimes the build is unstable when I push early.
> **QE:** Then maybe we **start** a quick smoke check on each build before handing over.
> **Dev (Tom):** I would like us to **stop** starting new stories before finishing the ones in progress.
> **Product Owner (Maria):** I would like to **continue** the daily stand-up on the board; it helped me see where things were stuck.
> **Scrum Master:** Great. Our agreed actions are: (1) hand over stories for testing as soon as they are built, with a smoke check by the developer (owner: Sam and Priya); (2) limit work in progress to three stories (owner: Ali).

**Common mistakes:**

- Skipping the Retrospective when the Sprint was "good" or when "we are too busy".
- Complaining without deciding on actions.
- Having managers or outsiders attend and so silencing honesty.
- Same format every time until it becomes stale.
- Too many actions, so none gets done.
- Never reviewing whether previous actions were completed.

---

## Where Testing Fits Inside a Sprint

A very common beginner (and even experienced-team) mistake is to think: "Developers build in week 1 and QEs test in week 2." This mini-waterfall inside a Sprint is called **Scrum-fall** (or "water-scrum-fall"), and it causes the exact problems Scrum was meant to solve: late bugs, rushed testing, and unfinished stories.

Instead, **testing is continuous**. Here is what that looks like across a 2-week Sprint:

### Testing Activities by Sprint Phase

| Phase of the Sprint | Testing Activities | Notes |
|---|---|---|
| **Before the Sprint (Refinement)** | Review stories for testability; shape acceptance criteria; identify test data and environment needs; flag risks. | The cheapest place to find a defect is in the requirement. |
| **Sprint Planning (Day 1)** | Estimate testing effort; plan test tasks; confirm Definition of Done. | Testing is part of "Done", not an afterthought. |
| **Early Sprint (Days 2-4)** | Write test scenarios from acceptance criteria; prepare data; set up environments; review code or designs for testability; test the first completed stories right away. | QEs and developers work side by side on each story. |
| **Mid Sprint (Days 5-8)** | Test stories as they are completed (**continuous testing**); retest fixes; explore the integrated product; start or update automated checks. | A story should flow Build -> Test -> Fix -> Retest -> Done, one by one, not in a big batch at the end. |
| **Regression testing (throughout and Day 9)** | Re-check that older features still work after new changes. **Regression testing** means re-running selected tests to catch accidental breakage. Run small targeted regressions mid-Sprint and a fuller regression pass near the end. | Automation makes this repeatable (you will learn automation later in the program). |
| **Hardening (late Sprint, Day 9)** | A short stretch near the end where the team stops adding new features and concentrates on stabilizing: fixing remaining defects, running full regression, verifying all stories against the Definition of Done, and confirming the demo environment. | Good teams keep hardening short and reserve it inside the Sprint; they do not postpone it to a separate "testing Sprint". |
| **Sprint Review (Day 10)** | Support the demo; communicate known issues and quality status. | Only Done work is shown. |
| **Retrospective (Day 10)** | Reflect on testing effectiveness; agree on improvements. | Feeds the next Sprint's plan. |

### The Flow of a Single Story

A healthy story moves through the Sprint like this:

```
 Refined   ->  Planned  ->  In Development  ->  In Testing  ->  Fix/Retest  ->  Done
 (AC ready)   (Day 1)      (QE writes tests    (QE tests as     (dev + QE       (meets DoD,
                            while dev codes)     soon as built)   loop quickly)   PO accepts)
```

Notice the overlap. While the developer is coding, the QE is already writing scenarios. The moment the code is available, testing starts, even if other stories are still being built. A technique that helps greatly is a **"three amigos" conversation**: the Product Owner, a Developer, and a QE (the three perspectives: business, build, test) meet briefly before development starts to make sure everyone understands the story the same way.

### Healthy vs Unhealthy Testing Rhythm

| Healthy | Unhealthy |
|---|---|
| Stories arrive for testing steadily from Day 3 onward. | Most stories arrive for testing on Day 8 or 9. |
| QE and developer talk directly about issues the same day. | Issues wait in a queue for days. |
| Regression is small and frequent. | Regression is one giant, stressful event at the end. |
| Burndown goes down gradually. | Burndown is flat, then a cliff on the last day. |
| Hardening is short (a day or less). | Hardening becomes a mini-phase of several days. |

---

## When Things Go Wrong

Real Sprints do not always go to plan. Knowing how the team responds is part of professional maturity.

### What If the Sprint Goal Is at Risk?

The Sprint Goal is the commitment, not every individual story. If the team sees early (for example by Day 5 or 6, from the burndown and the Daily Scrum) that the goal is at risk, the response is:

1. **Say so immediately.** Raise it at the Daily Scrum. Do not hide it until Day 10.
2. **Talk to the Product Owner.** Together, look at the work and negotiate scope: which stories or acceptance criteria could be simplified, postponed, or dropped while still achieving the Sprint Goal?
3. **Swarm.** Developers and QEs gather around the most important unfinished item to help finish it, rather than starting new things.
4. **Protect quality.** The Definition of Done does not shrink to make a deadline. It is better to deliver *less* that is Done than *more* that is not.
5. **Never extend the Sprint.** The timebox is fixed.

### What If the Goal Is Not Met by the End?

It happens, and it is a learning event, not a punishment.

- Unfinished stories are **not** counted toward velocity and are **not** shown as part of the Increment.
- The Product Owner puts unfinished items back in the Product Backlog; they may be re-ordered and re-estimated. They do not automatically roll into the next Sprint.
- The team discusses it in the **Retrospective**: Was the commitment too ambitious? Was the story too large? Did testing start too late? Were there unexpected blockers? The question is "what did we learn?", not "who failed?".
- If the goal becomes completely obsolete mid-Sprint, the Product Owner may cancel the Sprint (rare).

### What If a Bug Is Found Late?

Suppose it is Day 9 and a QE finds a serious problem in a story that was believed finished. (How defects are classified and tracked is the subject of a later lesson; here we focus on the sprint decisions.)

| Step | Action |
|---|---|
| **1. Report immediately** | Tell the developer and the team at once; do not wait for the next meeting. |
| **2. Assess the impact** | Does it break the Sprint Goal or the acceptance criteria? Is it limited to one area? Is there a workaround? |
| **3. Decide with the Product Owner** | Options: fix now within the Sprint (if the time is sufficient and the goal depends on it); reduce scope of the story and ship what is verified; or move the story back to the Product Backlog. |
| **4. Keep the Definition of Done** | A story with a serious open defect is not Done. It is not demonstrated as complete. |
| **5. Be transparent** | At the Review, communicate honestly what was and was not completed. |
| **6. Learn** | In the Retrospective, ask why it was found late. Could better acceptance criteria, earlier testing, or more regression have caught it sooner? |

The guiding principle: **hiding a late bug costs far more than reporting it.** A QE who raises it early, calmly, and with facts is doing precisely what the team needs.

---

## Examples

### Worked Example: A 2-Week Sprint for the Project 1 App

For this worked example, imagine the Project 1 sample web app is a small online shop. (If your actual Project 1 app is different, use it as a pattern and substitute your own features.) The team has four Developers (including Priya, the QE), a Product Owner (Maria), and a Scrum Master (Ali). The recent velocity is about 26 points. Because one developer is on leave for a day, the team commits to **24 points**.

**Product Goal:** "Give first-time shoppers a simple, reliable way to find a product and buy it."

**Sprint Goal (Sprint 1):** *"By the end of this Sprint, a registered shopper can log in, find a product, add it to the cart, and see an accurate cart total."*

**Selected User Stories:**

| # | Story | Points |
|---|---|---|
| **S1** | As a returning shopper, I want to log in with my email and password so that I can access my account. | 3 |
| **S2** | As a shopper, I want to search for products by name so that I can find what I need quickly. | 5 |
| **S3** | As a shopper, I want to view a product's details (name, price, description, image) so that I can decide whether to buy it. | 5 |
| **S4** | As a shopper, I want to add a product to my cart so that I can buy several items at once. | 8 |
| **S5** | As a shopper, I want to see my cart total update when I change quantities so that I know what I will pay. | 3 |

Total: 24 points.

**Acceptance criteria for two of the stories (examples):**

**S1 Login**
- *Scenario 1:* **Given** I have a registered account, **When** I enter my correct email and password and click "Log in", **Then** I am taken to the home page and see my name in the header.
- *Scenario 2:* **Given** I have a registered account, **When** I enter a wrong password, **Then** I see "Incorrect email or password" and stay on the login page.
- *Scenario 3:* **Given** I am on the login page, **When** I leave the email field empty and click "Log in", **Then** I see "Email is required".

**S4 Add to cart**
- *Scenario 1:* **Given** I am viewing a product that is in stock, **When** I click "Add to cart", **Then** the cart icon shows one more item and a confirmation appears.
- *Scenario 2:* **Given** a product already in my cart, **When** I add it again, **Then** its quantity increases by one rather than creating a second line.
- *Scenario 3:* **Given** a product is out of stock, **When** I view it, **Then** the "Add to cart" button is disabled and the text "Out of stock" is shown.

**Day-by-day table for the Sprint:**

| Day | Events | Development | QE Activities (Priya) | Burndown (points remaining, approximate) |
|---|---|---|---|---|
| **1 Mon** | Sprint Planning (3.5 h). Sprint Goal agreed. Daily Scrum begins next day. | Task breakdown; setup of branches. | Contributes to estimates; adds test tasks; raises dependency of S4 on S3 and S2; requests 50 product records as test data. | 24 |
| **2 Tue** | Daily Scrum. | Build S1 (login). | Writes test scenarios for S1 and S2 from acceptance criteria; prepares accounts and data. | 24 |
| **3 Wed** | Daily Scrum. Refinement session (1 h) for the next Sprint (checkout and saved cart stories). | S1 done in dev; start S2. | Tests S1: finds that an empty email shows a generic error; reports to developer, fixed same day. Asks testability questions in refinement. | 21 (S1 done at end of day) |
| **4 Thu** | Daily Scrum. | S2 (search) built. | Tests S2: empty search shows a blank page; result order wrong. Retests S1 fix. | 21 |
| **5 Fri** | Daily Scrum. Mid-sprint check on the Sprint Goal: on track, but S3 and S4 are tight. | S3 (product details). | Verifies S2 fixes; starts S3 tests; first small regression on login and search. | 16 (S2 done) |
| **6 Mon** | Daily Scrum. Burndown inspected. | S4 (cart) started. | Tests S3; finds image missing for one product; logs it. | 16 |
| **7 Tue** | Daily Scrum. | S4 continued; S3 fix. | Verifies S3; begins exploratory testing on integrated flow (login -> search -> details). | 11 (S3 done) |
| **8 Wed** | Daily Scrum. Refinement session #2 (1 h). | S4 complete in dev; S5 started. | Tests S4 against the three scenarios; finds that adding the same product twice creates two lines; developer fixes. | 11 |
| **9 Thu** | Daily Scrum. Feature freeze; hardening begins. | Fix remaining issues; S5 finished. | Retests S4, tests S5; runs full regression across login, search, details, cart; checks the demo environment; confirms the Definition of Done for each story. | 3 (S4 done), S5 awaiting final verification |
| **10 Fri** | Daily Scrum. Sprint Review (1.5 h). Retrospective (1 h). | Last small fix; build for demo. | Verifies S5; supports demo; shares quality status; leads the retrospective talking points on late handovers. | 0 (all Done) |

**What this example shows:**

- Testing begins on Day 3, not Day 8.
- Defects are found and fixed within the same day or the next, because QE and developer talk directly.
- The mid-Sprint check on Day 5 gave an early warning about the tight stories.
- Day 9 is a short hardening day, and the Review on Day 10 shows only Done work.
- The burndown stays reasonably close to the ideal, though S4 and S5 landed late; this becomes a retrospective topic.

### Sample Retrospective Output

**Sprint 1 Retrospective - Format: Start / Stop / Continue (with a short "What went well / what did not" opener)**

| Category | Notes (from the team) |
|---|---|
| **What went well** | Direct QE-developer conversation meant most defects were fixed within a day. Acceptance criteria written in Given/When/Then were clear and easy to test. The mid-sprint goal check on Day 5 gave an early warning. The demo went smoothly. |
| **What did not go well** | S4 (cart) reached testing late (Day 8), leaving little time for retesting. Test data was not ready until Day 3. The staging environment was unavailable for half a day on Day 6. Story S4 was larger than we realized (8 points; it should have been split). |
| **Start** | Splitting any story over 5 points during refinement. Handing over stories to QE as soon as each is built, preceded by a quick developer smoke check. Preparing test data before the Sprint starts. |
| **Stop** | Starting new stories before the current one is tested. Waiting until the Daily Scrum to mention a blocked environment. |
| **Continue** | Writing acceptance criteria in Given/When/Then. The mid-sprint goal check. Brief "three amigos" chats before development of risky stories. |

**Agreed actions for the next Sprint:**

| # | Action | Owner | Due |
|---|---|---|---|
| 1 | Split any story larger than 5 points during refinement. | Maria (Product Owner) and Priya | Before Sprint 2 planning |
| 2 | Developer runs a 5-minute smoke check, then notifies QE immediately when a story is ready. | Sam and all Developers | Ongoing from Sprint 2 Day 1 |
| 3 | Prepare reusable test data set (50 products, 5 accounts) and keep it in the shared location. | Priya | Sprint 2 Day 1 |
| 4 | Report environment outages to the Scrum Master immediately in the team chat. | Everyone | Ongoing |

Note how the actions are concrete, owned, and few. Next Sprint's Retrospective will begin by checking whether these four helped.

---

## Knowledge Check

Try to answer each question yourself before reading the answer.

**Q1. A team has a 2-week sprint but only 8 of the 10 days of work are finished. The team asks the Scrum Master to extend the sprint by 3 days. What is the right response?**
*Answer:* Sprints have a fixed length, so the Sprint is not extended. Unfinished work returns to the Product Backlog, and the team discusses why in the Retrospective.

**Q2. Name the three artifacts and the commitment that belongs to each.**
*Answer:* Product Backlog - Product Goal; Sprint Backlog - Sprint Goal; Increment - Definition of Done.

**Q3. Rewrite this vague story into the correct format: "Add a password reset."**
*Answer (example):* "As a registered shopper, I want to reset my password through an email link so that I can regain access if I forget it."

**Q4. What is wrong with this acceptance criterion: "The page should load quickly"? Improve it.**
*Answer:* It is not measurable or testable. Better: "Given I am logged in, When I open the product list, Then the first page of products is displayed within 3 seconds."

**Q5. In planning poker, why do all players reveal their cards at the same time?**
*Answer:* So that nobody's estimate is influenced by others. Differences then spark useful discussion (for example, a QE may reveal hidden testing effort).

**Q6. A team completed 22, 26, and 24 points in the last three sprints. Roughly what velocity should they plan for? Does a story that is 90 percent finished count?**
*Answer:* About 24 points (the average). A 90 percent finished story does not count; only fully Done stories count.

**Q7. Which event is for the Scrum Team only, and which one involves stakeholders?**
*Answer:* The Retrospective is for the Scrum Team only; the Sprint Review includes key stakeholders.

**Q8. Give two things a QE does during Sprint Planning.**
*Answer (any two):* Confirm acceptance criteria are testable; estimate testing effort; flag risks; identify test data and environment needs; add test tasks to the Sprint Backlog; help ensure the Sprint Goal is verifiable.

**Q9. Why is it a problem if a burndown chart is flat for eight days and then drops sharply on Day 10?**
*Answer:* It suggests work is piling up (often waiting for testing) and finishing all at once, which means testing was squeezed to the end and risk is high. Testing should be continuous.

**Q10. A QE finds a serious bug on Day 9. List three sensible actions.**
*Answer (any three):* Tell the developer and team immediately; assess the impact on the Sprint Goal with the Product Owner; decide to fix, reduce scope, or return the story to the backlog; do not call the story Done until it meets the Definition of Done; be transparent at the Review; discuss at the Retrospective why it was found late.

**Q11. What is the difference between hardening and "a testing phase at the end"?**
*Answer:* Hardening is a short, planned stabilization period inside the Sprint; most testing has already happened continuously. A testing phase at the end implies testing was delayed until after development, which is the Scrum-fall anti-pattern.

**Q12. What is the difference between the Sprint Review and the Retrospective?**
*Answer:* The Review inspects the product (the Increment) with stakeholders and adapts the Product Backlog. The Retrospective inspects the team's way of working and plans improvements.

---

## Try It: Plan a Sprint for Project 1

In this hands-on activity, you will think like a Scrum Team member for your Project 1 sample web app.

**Time:** about 45 to 60 minutes. **Format:** write it in a document (your project notes or a markdown file).

**Step 1 - Recall the app.** Write two or three sentences describing the Project 1 sample web app and its main users. List five features you could imagine in it (for example: sign up, log in, search, view details, add to cart, checkout, profile page).

**Step 2 - Write a Product Goal.** Write one sentence describing the long-term purpose of the app for its users.

**Step 3 - Write a Sprint Goal.** For a 2-week sprint, write **one sentence** that describes a clear, valuable objective. Check it with these questions: Does it describe an outcome rather than a list of tasks? Can the team tell at the end whether it was reached? Could a stakeholder understand it?

**Step 4 - Write three user stories.** Pick three features that support your Sprint Goal. For each, write the story using "As a / I want / So that". Check each against the INVEST list (especially Small and Testable).

**Step 5 - Write acceptance criteria.** For each story, write at least **three** acceptance criteria. Use the Given/When/Then format for at least two per story. Include at least one *negative* case (what happens when something goes wrong, such as invalid input) per story.

**Step 6 - Estimate.** Assign story points (1, 2, 3, 5, 8) to each story, with one sentence explaining the main factor that drove the estimate, including a note on testing effort.

**Step 7 - Plan your QE contribution.** Write a short list answering:
- Which two risks would you raise at Sprint Planning?
- What test data and environments would you need ready by Day 2?
- On which days would you expect to test each story?
- What would you say in the Daily Scrum on Day 4? (Write a 3-sentence update.)

**Step 8 - Self-review.** Swap with a classmate (or reread it the next day) and check: Is every acceptance criterion observable? Could someone else test it without asking you questions?

**Example output for a different feature (for reference only):**

> **Sprint Goal:** "A new visitor can create an account and update their profile details."
> **Story:** As a new visitor, I want to sign up with my email and a password so that I can use the app's member features.
> **Acceptance criteria:**
> 1. **Given** I am on the sign-up page, **When** I enter a valid email and a password of at least 8 characters and click "Sign up", **Then** my account is created and I see the message "Welcome".
> 2. **Given** I am on the sign-up page, **When** I enter an email that is already registered, **Then** I see "This email is already in use" and no new account is created.
> 3. **Given** I am on the sign-up page, **When** I enter a password shorter than 8 characters, **Then** I see "Password must be at least 8 characters".

You will build on this plan during the rest of the week as you learn Jira, testing principles, and test-design techniques; keep your notes.

*Pointer:* the stories and sprint plan you wrote here are the sort of items teams track on a board in a tool like Jira. How to create and manage them there is the topic of the next lesson, so for now a simple document is perfect.

---

## Key Takeaways

- A **Sprint** is a fixed-length timebox (one month or less; 2 weeks is very common) that contains all the other events. Its length does not change, and the Sprint Goal is protected from changes that endanger it.
- The three **artifacts** each carry a **commitment**: Product Backlog with the Product Goal, Sprint Backlog with the Sprint Goal, and Increment with the Definition of Done.
- **Done means Done**: partial work does not count. The Definition of Done is the team's shared quality standard, and QEs help shape it.
- **User stories** describe value (As a / I want / So that); **acceptance criteria**, often in **Given/When/Then** form, define how we recognize success and become the root of test cases.
- **Story points** are relative size, **planning poker** surfaces hidden assumptions, **velocity** guides forecasting for one team only, and a **burndown chart** shows progress transparently.
- The five events, each with a different job: **Refinement** (get stories ready), **Sprint Planning** (decide the goal and the plan), **Daily Scrum** (15-minute daily coordination), **Sprint Review** (inspect the product with stakeholders), **Retrospective** (improve how we work).
- Typical 2-week timeboxes: Planning up to 4 hours, Daily Scrum 15 minutes, Review up to 2 hours, Retrospective up to 1.5 hours, Refinement ongoing.
- **Testing is continuous**, not a phase at the end. Test stories as they are built, keep regression small and frequent, and keep hardening short.
- When the goal is at risk, **speak up early**, negotiate scope with the Product Owner, swarm on key items, and never lower the Definition of Done or extend the Sprint.
- A QE contributes in every event: testability questions in refinement, risk and effort in planning, honest status in the stand-up, quality context in the review, and evidence-based improvements in the retrospective.

---

## Additional Resources

1. **The Scrum Guide (official, 2020 edition)** - the definitive, short description of Scrum, including the Sprint, the events, the artifacts, and their commitments: https://scrumguides.org/scrum-guide.html
2. **Atlassian Agile Coach: Scrum** - clear, beginner-friendly articles on Scrum, sprints, and the events, with diagrams: https://www.atlassian.com/agile/scrum
3. **Scrum.org Resources** - articles, glossary, and learning paths from the organization co-founded by Ken Schwaber, including explanations of Scrum events and the Definition of Done: https://www.scrum.org/resources
