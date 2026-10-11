# SDLC Fundamentals: How Software Gets Built, and Where Quality Fits In

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain what software is and why building it needs a structured process.
- Define the Software Development Life Cycle (SDLC) in your own words.
- Describe each of the seven SDLC phases: planning, requirements analysis, design, implementation, testing, deployment and maintenance.
- State, for every phase, its purpose, main activities, inputs, outputs (deliverables), the people involved and the quality engineer's role.
- Explain why defects found late are far more expensive to fix than defects found early, and describe the "shift-left" idea.
- Walk a real-world application (an online food-ordering app) through every phase.
- Identify what goes wrong when phases are skipped or rushed.
- Map the Week 3 sample web app, "Project 1 - QE Foundations", onto the SDLC phases.

---

## Why This Matters

Imagine being hired as a Test Automation Engineer on your first day. Your team lead says, "We are in the design phase, and the requirements were signed off last week. Can you review them for testability before sprint planning?" If you do not know what "design phase", "sign-off" or "testability" mean, you will struggle to take part in the conversation, let alone add value.

The SDLC is the shared vocabulary and the shared map of every software team in the industry. Banks, hospitals, airlines, e-commerce sites and mobile game studios all follow some version of it. Knowing it helps you:

- **Understand where you fit.** Testing is not something that happens only at the end. A skilled quality engineer contributes in every phase.
- **Find problems cheaper.** Teams that involve quality people early catch misunderstandings before they become expensive code.
- **Communicate with the whole team.** Business analysts, architects, developers, operations engineers and product owners all talk in SDLC terms.
- **Build automation that makes sense.** You cannot automate what you do not understand. Knowing how a feature travels from idea to production tells you where automation pays off.

**Tie to the Weekly Epic.** This week you are building the quality-engineering mindset: SDLC and STLC, Agile, the defect lifecycle, Jira, testing principles and test-design techniques. Every one of those topics hangs off the SDLC. Think of today's lesson as the skeleton; the rest of the week adds muscles and nerves. By the end of the week you will apply everything, day by day, to Project 1 - QE Foundations, a sample web app that you will plan quality for.

---

## The Concept

### 1. What is software?

**Software** is a set of instructions (programs), together with the data and documentation that go with them, that tells a computer what to do. Hardware is the physical machine (screen, processor, memory); software is the "thinking" that runs on it.

You use software constantly:

- The app that lets you order dinner from your phone.
- The website your bank uses to show your balance.
- The program inside a car that controls the braking system.
- The operating system on your laptop.

Software has some properties that make it different from most physical products:

| Property | What it means | Why it matters for quality |
|---|---|---|
| Invisible | You cannot look at it and see whether it is "finished" or "broken". | We need deliberate checks (testing) to reveal its condition. |
| Easy to change | Changing a line of code is cheap compared with rebuilding a bridge. | Changes happen often, and each change can break something that worked before. |
| Complex | Even small apps contain thousands of decisions and paths. | It is impossible to rely on "it looks fine"; we need a structured approach. |
| Built by teams | Many people with different roles and views work on the same product. | Misunderstandings between people are a major source of defects. |

A **defect** (also called a bug) is a flaw in the software that makes it behave differently from what is expected. A **tester** or **quality engineer** is the person who helps the team find defects and, more importantly, helps prevent them.

### 2. Why does software development need a process?

Suppose ten friends decide to build a house with no plan. One starts laying bricks, another buys a roof, a third paints walls before the plumbing exists. The result would be chaotic, expensive and probably unsafe.

Software projects face the same risk. Without a process:

- Nobody agrees on what is being built, so people build different things.
- Work is repeated or forgotten.
- Problems are discovered when the product is "finished" and it is too late to change cheaply.
- Deadlines and budgets are missed because nobody can predict progress.
- Customers receive something that does not match what they needed.

A **process** is an agreed, repeatable way of working: the steps, the order, who does what, and what must exist before moving on. The SDLC is the name for the process of building software.

### 3. What is the SDLC?

**SDLC** stands for **Software Development Life Cycle**. It is a structured framework that describes all the stages a piece of software passes through, from the first idea to the day it is retired. The word "life cycle" is important: software has a life. It is conceived, built, released, maintained for years and eventually replaced, just as a house is planned, built, lived in, repaired and one day demolished.

The goals of an SDLC are to:

1. Deliver software that meets the real needs of users and the business.
2. Deliver it with high quality (it works, it is reliable, it is secure).
3. Deliver it within the agreed time and budget.
4. Make the work visible, measurable and predictable.

Most descriptions of the SDLC list about six or seven phases. In this lesson we use seven:

```
  +-----------+    +--------------+    +----------+    +----------------+
  | 1.Planning| -> | 2.Requirements| -> | 3.Design | -> | 4.Implementation|
  |           |    |   Analysis    |    |          |    |   (Coding)     |
  +-----------+    +--------------+    +----------+    +----------------+
                                                               |
                                                               v
  +-----------+    +--------------+    +----------+
  |7.Maintenan| <- | 6.Deployment | <- | 5.Testing|  <--------+
  |   ce      |    |              |    |          |
  +-----------+    +--------------+    +----------+
        |
        +----> feedback and new needs flow back to Planning
```

Important notes before we go deeper:

- The phases are conceptual building blocks. Real teams arrange them in different ways: some do them once in order, others repeat small versions of all of them every two weeks. Those arrangements are called SDLC models, and we will study them in the next lesson. For now, learn what each phase is.
- Different books name the phases slightly differently (for example, "analysis" or "feasibility study"). The ideas are the same.

### 4. The building-a-house analogy

We will use this analogy throughout. It maps neatly onto the phases:

| SDLC phase | Building a house |
|---|---|
| Planning | Decide if you should build at all: budget, land, timeline, who will help. |
| Requirements analysis | Talk to the family: how many bedrooms, accessible for grandparents, a garden. |
| Design | The architect draws floor plans (high level) and the electrician draws wiring diagrams (detailed). |
| Implementation | Builders lay foundations, raise walls, install pipes and wiring. |
| Testing | The inspector checks the structure, tests the plumbing, switches every light on. |
| Deployment | Hand over the keys; the family moves in. |
| Maintenance | Fix a leaking tap, repaint, add a room later. |

Notice that a good inspector does not wait until the walls are painted to read the plans. If the plan says the staircase is too steep, it is much cheaper to find that on paper than after the stairs are built. Keep this thought: we will return to it when we discuss the cost of late defects.

### 5. Our running example: "QuickBite", an online food-ordering app

To make every phase concrete, we will follow a fictional company building **QuickBite**, a mobile and web app where customers browse restaurants, add dishes to a cart, pay online and track delivery. Look for the "QuickBite" boxes in each phase below.

---

### 6. Phase 1: Planning

**Purpose.** Decide whether the project should be done at all, and if so, how. Planning establishes the big picture: goals, scope, cost, time, risks and resources.

**Key activities.**

- Define the business goal ("Increase our monthly orders by 30%").
- Study feasibility: is it technically possible, financially worthwhile and legally allowed?
- Estimate effort, cost and timeline at a high level.
- Identify major risks (for example, "payment integration is new to us").
- Decide on the team, tools and approach.
- Define the scope: what is in the project and, just as important, what is out.

**Inputs.** A business idea or problem, market research, budget limits, company strategy, knowledge of existing systems.

**Outputs (deliverables).** A project plan, a feasibility or business-case document, a rough schedule and budget, a risk list, a statement of scope.

**Who is involved.** Business owners and sponsors, project or product managers, senior technical leads and sometimes a lead quality engineer.

**The quality engineer's role.**

- Raise quality-related risks early ("online payments are high risk; we should allocate time for security and performance checks").
- Help estimate how much testing effort the project needs.
- Ask what "good quality" means for this product and who decides.
- Identify what test environments, tools and skills will be needed so they can be budgeted.

> **QuickBite.** Leadership wants to capture the evening-meal market. The project manager defines scope: customers can order from partner restaurants and pay by card. Loyalty points and a grocery section are "out of scope for version 1". The QA lead notes that card payments and live delivery tracking are risky and asks for a test environment that can simulate payments without moving real money.

### 7. Phase 2: Requirements Analysis

**Purpose.** Understand, in detail, what the software must do and how well it must do it. This is where vague wishes become clear, written statements.

**Key terms.**

- A **requirement** is a documented need or condition that the software must satisfy.
- **Functional requirements** describe what the system does (for example, "A customer can add a dish to the cart").
- **Non-functional requirements** describe how well it does it: speed, security, usability, availability, compatibility (for example, "The menu page loads within 3 seconds on a standard mobile connection").
- A **stakeholder** is anyone with an interest in the product: customers, business owners, support staff, regulators.

**Key activities.**

- Interview stakeholders, run workshops, observe how users work today.
- Write requirements in a clear, agreed format (for example, as formal statements or as user stories such as "As a customer, I want to save my address so that I do not retype it").
- Review requirements for gaps, conflicts and ambiguity.
- Get formal agreement ("sign-off") from the business.
- Define **acceptance criteria**: the conditions that must be true for a requirement to count as satisfied.

**Inputs.** The project plan and scope, stakeholder knowledge, existing systems and documents, regulations.

**Outputs.** A Software Requirements Specification (SRS) or a backlog of user stories with acceptance criteria, and a record of agreed changes to scope.

**Who is involved.** Business analysts, product owners, stakeholders, developers (to confirm what is feasible), and quality engineers.

**The quality engineer's role.** This is one of the highest-value places for a tester.

- Review each requirement and ask: Is it clear? Is it complete? Is it consistent with others? Can it be tested?
- Spot ambiguous words such as "fast", "user-friendly" or "easy" and ask for measurable targets.
- Help write acceptance criteria.
- Begin thinking about how each requirement will later be checked. Requirements that cannot be checked are a warning sign.

> **QuickBite.** A requirement reads: "The app should show delivery time quickly." The tester asks, "What is quickly? Is it within one second? Is the time an estimate, and how accurate must it be?" The business analyst updates it: "The estimated delivery time is displayed within 2 seconds of the customer opening the order screen, and is accurate to within 10 minutes for 90% of orders." Now it is testable.

We will study how to analyze requirements and plan testing in detail on Tuesday. Today, just remember that testers are valuable in this phase.

### 8. Phase 3: Design

**Purpose.** Decide how the software will be built to satisfy the requirements. If requirements say what, design says how.

Design is often split in two levels:

- **High-Level Design (HLD)** gives the overall architecture: the major components (for example, mobile app, web server, database, payment service), how they connect, which technologies to use, and how data flows between them. Analogy: the architect's floor plan of the house.
- **Low-Level Design (LLD)** zooms into each component: classes and modules, database tables and columns, screen layouts, exact rules and algorithms, error messages. Analogy: the electrician's detailed wiring diagram for one room.

**Key activities.**

- Choose the architecture and technology stack.
- Design the database structure.
- Design user interface screens and flows (wireframes and mock-ups).
- Define interfaces between components, for example how the app talks to the payment provider.
- Plan for security, performance and scalability (the ability to handle growth in users).
- Review the design for risks and gaps.

**Inputs.** The approved requirements, technical standards, existing architecture, non-functional needs.

**Outputs.** HLD and LLD documents, architecture diagrams, database designs, UI wireframes and prototypes, interface specifications.

**Who is involved.** Solution architects, senior developers, UI/UX designers, database designers, security specialists, and quality engineers.

**The quality engineer's role.**

- Review designs for testability: can each component be tested on its own? Are there clear inputs and outputs?
- Ask "what if" questions: what happens if the payment provider is down?
- Identify where test data and test environments will be needed.
- Plan which parts will be good candidates for automation.
- Review wireframes against requirements to make sure nothing is missing.

> **QuickBite.** The HLD shows a mobile app and web site talking to an "Orders" service, a "Restaurants" service, a database and an external payment provider. The LLD for the cart specifies a table with columns for customer, dish, quantity and price, and says that quantity must be between 1 and 20. The tester notices that nothing says what happens when a dish becomes unavailable while it is in someone's cart, and raises it. The designer adds a rule and an error message.

### 9. Phase 4: Implementation (Coding)

**Purpose.** Turn the design into working software by writing code.

**Key activities.**

- Developers write code following the design and agreed coding standards.
- Developers write **unit tests**: small automated checks that verify individual pieces of code (for example, one function that calculates the cart total).
- Code is reviewed by peers (**code review**).
- Code is stored in a **version control** system (for example, Git), which keeps a history of every change and lets many people work together safely.
- Parts of the system are combined (**integration**) and built into a runnable version, often automatically by a **build** process.

**Inputs.** Design documents, requirements, coding standards, development tools and environments.

**Outputs.** Source code, unit tests, build artifacts (the runnable package), technical notes, and a working build ready for testing.

**Who is involved.** Developers, tech leads, and often DevOps engineers who set up the build tools. Quality engineers contribute in several ways.

**The quality engineer's role.**

- Prepare test cases, test data and test environments while developers code.
- Begin writing automation for stable areas.
- Take part in code reviews where appropriate, or at least read the changes to understand what is affected.
- Check that builds are available and stable for testing, and that unit tests are running.
- Communicate with developers about what is ready to test and what is not.

> **QuickBite.** Developers code the cart, using Git to track changes. Each pull request is reviewed by a colleague, and an automated build runs the unit tests. Meanwhile the QA engineer writes test cases for the checkout flow and prepares test accounts.

### 10. Phase 5: Testing

**Purpose.** Evaluate the software to find defects, confirm it meets the requirements and give the team confidence (or honest warnings) about its quality before release.

**Key activities.**

- Run planned tests on the software: checking features, how components work together, and the whole system end to end.
- Compare actual results with expected results.
- Log defects clearly so developers can fix them.
- Re-test fixes and check that fixes did not break other things (**regression testing**).
- Perform non-functional checks such as performance, security and usability.
- Business users confirm the product suits their needs (**user acceptance testing**, UAT).
- Report progress and quality status to the team.

**Inputs.** The built software, requirements and designs, test cases, test data, test environments.

**Outputs.** Test results, defect reports, test summary reports, and a recommendation on whether the product is ready to release.

**Who is involved.** Quality engineers and testers lead this phase, supported by developers (who fix defects), business analysts, product owners and sometimes real users.

**The quality engineer's role.** This is the core of the job: designing and running tests, reporting defects precisely, automating repeatable checks, and giving stakeholders accurate information to decide whether to release.

Testing as a phase has its own detailed process, called the Software Testing Life Cycle (STLC). We will cover it later today in its own lesson. The defect life cycle (what happens to a bug from discovery to closure) is covered on Tuesday, and test design techniques on Thursday.

> **QuickBite.** Testers run the checkout tests and discover that if a customer applies a discount code and then changes the quantity, the discount is counted twice. They log a defect with clear steps, developers fix it, and the tester re-tests and also re-runs related tests to confirm nothing else broke. Finally, the restaurant partners try the system in UAT and confirm the order screen works for their staff.

### 11. Phase 6: Deployment

**Purpose.** Release the tested software to the environment where real users can use it (the **production** environment).

**Key activities.**

- Prepare the release: final approvals, release notes, a go/no-go decision.
- Move the software to production, often in stages (for example, to a small group of users first).
- Configure servers, databases and monitoring.
- Prepare a **rollback plan**: the steps to undo the release quickly if something goes badly wrong.
- Run quick checks right after release to confirm the essentials work (**smoke testing**, covered in more detail later in the course).
- Train users and support staff, publish documentation.

**Inputs.** The approved build, release notes, deployment instructions, infrastructure.

**Outputs.** Live software, a release record, updated documentation, monitoring in place.

**Who is involved.** DevOps and operations engineers, release managers, developers, support teams, product owners, and quality engineers.

**The quality engineer's role.**

- Take part in the go/no-go decision with a clear summary of known risks and open defects.
- Verify the deployment itself: right version, right configuration.
- Run post-release smoke checks in production.
- Watch early monitoring and user feedback for problems that testing did not reveal.

> **QuickBite.** The release goes first to 5% of customers in one city. The QA engineer runs a short set of checks in production using a test account (browse, add to cart, place a low-value test order that is later cancelled). Everything passes, so the release expands to all customers.

### 12. Phase 7: Maintenance

**Purpose.** Keep the software working, useful and secure after release. For most successful products, this phase is the longest, often years, and costs more in total than the original build.

**Types of maintenance.**

| Type | Meaning | Example |
|---|---|---|
| Corrective | Fixing defects found after release | Orders fail when an address contains an apostrophe. |
| Adaptive | Changing the software to suit a changed environment | A new mobile operating system version is released; the app must still work. |
| Perfective | Improving or adding features | Customers ask for a "reorder last meal" button. |
| Preventive | Cleaning up to avoid future problems | Rewriting a fragile part of the code that keeps causing bugs. |

**Key activities.** Monitoring system health, handling support tickets, fixing bugs, releasing updates and patches, planning enhancements, and eventually retiring the product.

**Inputs.** User feedback, support tickets, monitoring data, change requests, new business needs.

**Outputs.** Patches, new versions, updated documentation, retirement plans.

**Who is involved.** Support teams, developers, operations, product owners, quality engineers.

**The quality engineer's role.**

- Test every fix and every change.
- Maintain and grow the **regression test suite** (the collection of tests that confirm existing features still work after changes). Automation is especially valuable here.
- Analyze production defects to find out why testing missed them, and improve.
- Contribute to the next cycle's planning with lessons learned.

> **QuickBite.** Six months later, customers report that orders are slow on Friday evenings. The team fixes a database inefficiency (corrective), then adds a "reorder" feature (perfective). Each change goes back through the phases, in small form, with regression tests run before release.

### 13. Phase summary table

| Phase | Main purpose | Typical outputs | Quality engineer's focus |
|---|---|---|---|
| Planning | Decide whether and how to proceed | Project plan, feasibility, risk list | Quality risks, effort estimates |
| Requirements analysis | Define what to build | SRS or user stories, acceptance criteria | Review for clarity and testability |
| Design | Decide how to build it | HLD, LLD, wireframes | Review for testability, plan environments |
| Implementation | Write the code | Source code, unit tests, builds | Prepare tests and automation |
| Testing | Find defects, confirm quality | Test results, defect reports, summary | Execute tests, report, advise |
| Deployment | Release to real users | Live system, release notes | Go/no-go input, smoke checks |
| Maintenance | Keep it working and evolving | Patches, updates | Regression tests, learn from escapes |

A key lesson from this table: a quality engineer has something useful to do in every row.

---

### 14. The cost of finding defects late

A defect is not a physical object that sits somewhere; it is a mistake made by a person at some point in the life cycle. A defect may be:

- *introduced* in one phase (for example, a misunderstood requirement),
- but only *found* in a later one (for example, in testing or by a customer).

The longer a defect remains hidden, the more work has been built on top of it, and the more it costs to fix. Consider the house analogy: finding that the bathroom is in the wrong place on the drawing costs an eraser. Finding it after the pipes are laid and walls built costs demolition and rebuilding.

A widely cited rule of thumb (based on research by Barry Boehm and others, and used in many textbooks) is that the relative cost of fixing a defect grows steeply the later it is found. Exact numbers vary between organizations and projects, so treat the following as an illustration of the trend rather than a measurement:

| Phase where defect is found | Illustrative relative cost to fix |
|---|---|
| Requirements | 1x |
| Design | about 5x |
| Implementation (coding) | about 10x |
| Testing | about 20x |
| After release (production) | 50x to 100x or more |

Why does cost climb so quickly?

- More people are affected: documents, designs, code and tests built on the wrong assumption all need changing.
- Re-work: code must be rewritten, re-tested and re-released.
- Production problems add support effort, emergency fixes, lost sales and possible fines.
- Reputation damage is hard to measure but real. A bank app that shows wrong balances loses trust quickly.

**Shift-left.** If you imagine the SDLC drawn left to right (planning on the left, maintenance on the right), then **shift-left** means moving quality activities earlier, toward the left. Instead of waiting for finished software, we review requirements, review designs, write tests early and run automated checks as soon as code exists. The goal is to prevent defects or find them while they are cheap.

```
   Early (cheap to fix)                                   Late (expensive to fix)
   Plan -> Requirements -> Design -> Code -> Test -> Deploy -> Maintain
   <------------- SHIFT-LEFT: put quality effort here ----------------
```

Shift-left does not mean "stop testing at the end"; it means "start quality work at the beginning" and keep going.

> **Worked mini-example.** In QuickBite's requirements, "free delivery for orders over 20" never says whether that is before or after discounts. If a tester asks this question during requirements review, the fix is one sentence. If it is found after release, customers who used discount codes receive free delivery they should not, the company loses money, the code must be changed, regression tests re-run and a patch released.

### 15. What goes wrong when phases are skipped or rushed

| Skipped or rushed phase | Typical consequences | Example |
|---|---|---|
| Planning | Unrealistic deadlines, no budget for testing, surprise risks, scope that keeps growing ("scope creep") | The team discovers in month four that the payment provider requires a certification nobody planned for. |
| Requirements analysis | Building the wrong thing, endless rework, arguments about what was "supposed" to happen | The business wanted guest checkout; developers built mandatory sign-up. |
| Design | Fragile, hard-to-change software; performance and security problems; "spaghetti code" | The app works for 100 users but crashes at 10,000 because the database design cannot scale. |
| Implementation (poor practices) | Many defects, hard-to-maintain code, no unit tests | A small change in the cart breaks the discount logic because nothing detects it. |
| Testing | Defects reach customers; emergency fixes; loss of trust | Customers are charged twice because payment retry logic was never tested. |
| Deployment | Failed releases, downtime, no way back | A release overwrites production data, and there is no rollback plan. |
| Maintenance | Software decays, security holes remain open, users leave | An unpatched library is exploited by attackers. |

Another common mistake is treating testing as the "safety net" for all earlier mistakes. Testing finds defects; it cannot easily fix a wrong requirement or a poor design. Quality has to be built into every phase.

### 16. Roles at a glance

Different organizations use different job titles, but you will meet these roles repeatedly:

| Role | What they do |
|---|---|
| Product owner / business analyst | Represents business needs; writes and clarifies requirements |
| Project / delivery manager | Plans, tracks progress and manages risks and people |
| Architect | Decides the overall technical structure |
| UI/UX designer | Designs how the product looks and feels |
| Developer | Writes and unit-tests code, fixes defects |
| Quality engineer / tester | Plans and runs tests, reports defects, automates checks, advises on quality |
| DevOps / operations engineer | Builds pipelines, deploys, monitors infrastructure |
| Support team | Helps users, records problems, feeds back to the team |

Quality is a shared responsibility. The quality engineer leads on testing and quality advocacy, but everyone contributes to building a good product.

### 17. A second example in brief: a banking app

To show the SDLC is not specific to food delivery, here is how the same ideas appear in a banking app feature, "transfer money to another account":

| Phase | What happens |
|---|---|
| Planning | The bank decides to add instant transfers; regulators and security risk are highlighted; budget set. |
| Requirements | "A customer can transfer up to 5,000 per day to a saved payee; the transfer completes in under 5 seconds; every transfer is recorded for audit." |
| Design | Components defined: mobile app, transfer service, fraud-check service, core banking database; rules for rounding and limits specified. |
| Implementation | Developers code the transfer service with strong unit tests, because money is involved. |
| Testing | Testers check limits (what if the amount is exactly 5,000? or 5,000.01?), insufficient funds, network failure mid-transfer, and security. |
| Deployment | Rolled out gradually with a rollback plan and close monitoring. |
| Maintenance | Regulations change the daily limit; the team updates and regression-tests the feature. |

Notice how the cost of an error is higher in banking (wrong amounts, legal exposure), so the team invests more heavily in early quality activities. The amount of effort a team puts into each phase depends on the risk.

---

### 18. What comes next

This lesson described the phases themselves. Real teams organize those phases in different ways, such as working through them in one long sequence or repeating small versions of them again and again. Those organizing patterns are called **SDLC models**, and the very next lesson introduces them. Later today you will also study the **Software Testing Life Cycle (STLC)**, which zooms into the testing phase and shows how testing work itself is organized. Throughout the week, we will add topics (requirements analysis and the defect lifecycle on Tuesday, testing principles on Wednesday, test design techniques on Thursday, advanced testing on Friday) onto the structure you learned here.

---

## Connecting SDLC to Project 1 - QE Foundations

All week you will plan quality for **Project 1 - QE Foundations**, a sample web application. Treat it exactly as a real team would treat a new product. The table below shows how its life maps onto the phases and what you, as the quality engineer, will be doing.

| SDLC phase | What it means for Project 1 | Your quality activity this week |
|---|---|---|
| Planning | Understand the app's purpose, scope and risks | Write a short list of quality risks and what is in and out of scope for testing |
| Requirements analysis | Read or draft the app's features as requirements and user stories | Review them for clarity and testability; write acceptance criteria (Tuesday) |
| Design | Look at the app's screens, pages and how they connect | Identify components and flows; note testability concerns and test data needs |
| Implementation | The app already exists as code to be tested | Prepare test ideas and decide where automation could help |
| Testing | Plan and design tests for the app | Create a test plan, design test cases (Thursday), and log defects in Jira (Tuesday) |
| Deployment | The app runs in a test environment (and, in real life, production) | Define what "ready to release" would mean; identify smoke checks |
| Maintenance | Imagine future changes and bug fixes | Plan a regression suite for later |

Keep a simple "Project 1 notebook" (a document or a notes page) and add to it each day. Today's entry will be the phase map.

---

## Examples and Practical Scenarios

### Scenario 1: The vague requirement

A requirement says: "The search page must be fast and easy to use."

- Which phase should catch the problem? Requirements analysis.
- What should the tester ask? "What does fast mean in seconds? Which devices and connections? How will we judge 'easy'?"
- Possible improved requirement: "Search results appear within 2 seconds for 95% of searches on a standard broadband connection; a first-time user can find and open a product in three clicks or fewer."

### Scenario 2: The missed design case

The design for a password-reset feature describes sending an email link, but not what happens if the link is used twice or after it expires.

- Phase where it should be found: Design review.
- Cost if found now: an extra paragraph in the design.
- Cost if found in production: a security risk where old links might still reset passwords, an emergency patch and possibly user data exposure.

### Scenario 3: The skipped deployment plan

A team releases on Friday afternoon with no rollback plan. A defect corrupts some orders. The team works through the weekend to repair data by hand.

- Lessons: rehearse deployments, prepare rollbacks, avoid risky releases right before the team is away, and include quality input in the go/no-go decision.

---

## Knowledge Check

Try to answer each question before reading the short answer.

**1. In your own words, what is the SDLC and why does it exist?**
*Answer:* The SDLC is a structured framework describing all the stages software goes through from idea to retirement. It exists so teams build the right thing, with good quality, in a predictable time and cost, with everyone working in an agreed order.

**2. Name the seven phases used in this lesson in order.**
*Answer:* Planning, requirements analysis, design, implementation (coding), testing, deployment, maintenance.

**3. What is the difference between functional and non-functional requirements? Give one example of each for a food-ordering app.**
*Answer:* Functional requirements say what the system does ("a customer can add a dish to the cart"); non-functional requirements say how well ("the menu loads in under 3 seconds").

**4. What is the difference between HLD and LLD?**
*Answer:* HLD shows the overall architecture and major components and how they connect; LLD details the inside of each component such as tables, classes and screen rules.

**5. Why is a defect found in production typically so much more expensive than one found during requirements?**
*Answer:* More work has been built on it (designs, code, tests), fixing it requires re-work and re-release, customers may be harmed, and support and reputation costs add up.

**6. What does "shift-left" mean?**
*Answer:* Moving quality activities earlier in the life cycle (reviewing requirements and designs, writing tests early, automating checks early) to prevent or find defects while they are cheap to fix.

**7. List two things a quality engineer can do during the design phase.**
*Answer:* Review designs for testability, ask "what if" questions about failure cases, plan test data and environments, identify automation candidates. (Any two.)

**8. Match the maintenance type to the example: (a) fixing a bug found by customers; (b) updating the app for a new phone operating system; (c) adding a new feature; (d) cleaning up fragile code.**
*Answer:* (a) corrective, (b) adaptive, (c) perfective, (d) preventive.

**9. A team skips the requirements phase because "we all know what the customer wants". Predict two problems.**
*Answer:* Different people build different things, features do not match what the customer needed, arguments about expected behavior, large re-work late in the project, and nothing clear to test against.

**10. Hint-based challenge:** Think of an app you use every day. Pick one feature and describe, in one sentence per phase, what you imagine happened in each SDLC phase to produce it. *Hint:* start with "Why would the company want this feature?" (planning) and "What exactly should it do?" (requirements).

---

## Try It: Map Project 1 to the SDLC

**Time:** about 30 to 40 minutes. **Format:** individual, in your Project 1 notebook.

**Steps.**

1. Open Project 1 - QE Foundations and spend 10 minutes exploring it as a user. Note the main pages, features and user actions.
2. Create a table with the seven SDLC phases as rows and these columns: *What this phase means for Project 1*, *Inputs I can see or would need*, *Outputs I would expect*, *My quality activity*.
3. For the **Requirements** row, write three requirements you think the app is meant to satisfy, one of them non-functional. Mark any that are vague and rewrite one so it can be tested.
4. For the **Planning** row, list at least three quality risks (for example, "login security", "form validation", "browser compatibility") and give each a high, medium or low priority with a one-line reason.
5. For the **Design** row, sketch a simple box diagram of the app's main parts and how they connect (for example, browser, web server, database).
6. Write a short note: "If a defect were found in the login feature, in which phase could it have been prevented, and what would have been the cheapest way to prevent it?"

**Self-check.** Your table should have all seven rows filled, at least one rewritten testable requirement, and a prioritized risk list. Keep it; you will reuse it for test planning on Tuesday.

---

## Key Takeaways

- Software is invisible, complex and easy to change, which is why building it needs a disciplined process.
- The **SDLC** is the life cycle of software from idea to retirement. This lesson's seven phases are planning, requirements analysis, design (HLD and LLD), implementation, testing, deployment and maintenance.
- Each phase has a purpose, activities, inputs, outputs and people involved, and **quality has a role in every one of them**, not just testing.
- Requirements say *what*, design says *how*, implementation *builds* it, testing *checks* it, deployment *releases* it, and maintenance *sustains* it.
- Defects get dramatically more expensive the later they are found. **Shift-left** means doing quality work early to prevent or catch them cheaply.
- Skipping phases leads to predictable problems: wrong product, fragile design, escaped defects, failed releases and decaying software.
- The same life cycle applies whether you are building a food app, a banking feature or Project 1.
- Next, you will learn how teams organize these phases (SDLC models), followed by the STLC, which zooms into the testing phase.

---

## Additional Resources

- **Guru99 - Software Development Life Cycle (SDLC) tutorial:** https://www.guru99.com/software-development-life-cycle-tutorial.html. A beginner-friendly walkthrough of the phases with diagrams.
- **ISTQB Certified Tester Foundation Level (syllabus and glossary access):** https://www.istqb.org/certifications/certified-tester-foundation-level. The international standard body for software-testing terminology and the foundation of many testing careers.
- **Atlassian - Agile and software development resources:** https://www.atlassian.com/agile. Useful background reading you can return to after the next lesson on SDLC models.
