# Agile Roles and Responsibilities

## Learning Objectives

By the end of this lesson, you will be able to:

- Describe the three official Scrum roles (Product Owner, Scrum Master, and Developers) and explain what each is accountable for and what each is *not*.
- Explain where QA, QE, and SDET professionals sit inside the Scrum "Developers" accountability, and why Scrum has no separate "tester" role even though testing specialists are essential.
- Identify the wider cast of an Agile team and its stakeholders: business analyst, UX/UI designer, DevOps/release engineer, tech lead/architect, customers and end users, and Agile coach.
- Describe in detail what a Quality Engineer does before, during, and at the end of a sprint.
- Explain the whole-team quality mindset and the Three Amigos practice.
- Distinguish between the Definition of Ready and the Definition of Done, and give examples of each.
- Read a RACI-style responsibility table for a sprint.
- Recognise common role anti-patterns (mini-waterfall, tester as gatekeeper, absent Product Owner, Scrum Master as manager) and suggest fixes.
- Assign roles to a sample team for Project 1 and rehearse a refinement conversation.

---

## Why This Matters

Earlier today you learned how software gets built (the SDLC) and compared delivery approaches: Waterfall, Agile, Scrum, Kanban, and Hybrid. You now know *how work flows*. This lesson answers a different question: **who does what?**

Most quality problems in real projects are not caused by missing tools. They come from unclear responsibilities. Examples you will meet on real teams:

- "I thought the Product Owner was going to clarify that requirement." (Nobody did, so the developer guessed.)
- "QA will catch it." (The developer stopped thinking about edge cases.)
- "Testing is the last step." (Testing was squeezed into the final two days, and bugs shipped.)

Companies hiring Quality Engineers almost never ask only "can you write test cases?" They ask: "How do you work with developers and product owners? How do you contribute during refinement? How do you handle disagreement about whether a story is done?" Knowing the roles, and where quality fits into each, is what separates a tester who waits for work to be handed over from a Quality Engineer who shapes the product from the start.

**Tie to this week's Epic.** This week you are building the quality-engineering mindset (SDLC/STLC, Agile, defect lifecycle, Jira, testing principles, test-design techniques) and applying it daily to **Project 1 - QE Foundations**, a sample web app you plan quality for. Today you decide who is on that team and what each person owns. Every later activity this week, such as writing acceptance criteria, logging defects, and designing tests, assumes you know whose job it is and how the roles collaborate.

> **Terminology note.** Throughout this lesson, **QA** (Quality Assurance) usually means process-focused quality work, **QE** (Quality Engineering) means engineering quality into the whole delivery process, often including automation, and **SDET** (Software Development Engineer in Test) means a testing specialist with strong programming skills who builds test frameworks and tools. In practice, companies use these titles loosely. This lesson uses "QE" as the umbrella term unless it says otherwise.

---

## The Concept

### 1. An Analogy to Hold On To: The Cricket (or Football) Team

Imagine a cricket team. There is a captain who sets direction and makes tactical decisions, a coach who helps the team improve how they play and removes obstacles, and eleven players who actually play the game. Players have specialities (a bowler, a wicketkeeper, an opener), but **the team wins or loses together**. Nobody says, "The wicketkeeper is the only one responsible for catches."

Map it to Scrum:

| Cricket / Football | Scrum | Core idea |
|---|---|---|
| Captain deciding what to aim for and the order of play | **Product Owner** | Decides *what* is most valuable to build, and in what order |
| Coach who improves how the team works, handles logistics and distractions | **Scrum Master** | Helps the team follow Scrum and work effectively |
| The players on the field | **Developers** | Do the work that produces the product increment |
| A specialist wicketkeeper or goalkeeper | **QE / SDET inside Developers** | A specialist skill that belongs to the team, not a separate team |
| Fans, sponsors, club owners | **Stakeholders** | Care about results and influence the team without playing |

Keep this picture in mind. A film crew works too: the director (vision), the producer or assistant director (keeping things running), and the crew (camera, sound, editing). The film's quality is everyone's responsibility, though the sound engineer is the specialist when the audio is bad.

### 2. First, Define "Role" and "Accountability"

- **Role**: a set of responsibilities that a person takes on in a team. A role is not a job title. In Scrum, one person can have a job title of "Senior QE" and fill the *role* of Developer.
- **Accountability**: being answerable for an outcome. If something goes wrong, you are the one who explains it and fixes the system. Scrum deliberately uses "accountabilities" so that each outcome has a clear owner.
- **Scrum Team**: the small group that delivers the product. According to the Scrum Guide, a Scrum Team consists of **one Scrum Master, one Product Owner, and Developers**. It is typically 10 or fewer people, is cross-functional, and is self-managing. There are no sub-teams or hierarchies inside it.
- **Product Backlog**: an ordered list of everything that might be needed in the product (features, fixes, improvements). You will study it in depth later; for now, think of it as the team's prioritised to-do list.
- **Sprint**: a fixed-length period (one to four weeks) during which the team builds a usable piece of the product.
- **Increment**: the usable, finished product piece produced in a sprint.

---

### 3. The Three Official Scrum Roles

#### 3.1 The Product Owner (PO)

**One-line definition:** The Product Owner is the single person accountable for maximising the value of the product that results from the Scrum Team's work.

**What the Product Owner does:**

1. **Owns the product vision and goals.** The PO knows why the product exists, who it is for, and what success looks like. They express this as a Product Goal, a long-term objective the team works toward.
2. **Owns the Product Backlog.** They are accountable for creating and clearly communicating backlog items, and for making sure the backlog is transparent, visible, and understood. They may delegate the *writing* of backlog items, but they remain accountable for them.
3. **Prioritises.** The backlog is ordered. The PO decides what comes first, balancing business value, risk, deadlines, dependencies, and customer needs. Saying "no" or "not now" is a core part of the job.
4. **Accepts or rejects work.** The PO checks whether the finished work delivers the intended value and meets the agreed acceptance criteria. (Acceptance criteria are the specific conditions a story must satisfy to be accepted. You will practise writing them this week.)
5. **Acts as liaison with stakeholders.** They gather input from customers, business leaders, support, and sales, and they communicate decisions and progress back. The PO is the "single voice" so the team is not pulled in ten directions.
6. **Is available to the team.** A good PO answers questions quickly, ideally the same day, because a developer waiting two days for a clarification is a developer guessing.

**Why the QE cares:** The PO is your main source for "what should this feature do?" and "what matters most?" When you ask clarifying questions, they are usually answered by the PO. When you assess risk and decide where to test most deeply, you lean on the PO's view of business value.

**What the Product Owner is NOT:**

- **Not a committee.** One person, even if they consult many. If the PO's decisions can be overridden by anyone with a louder voice, the team loses direction.
- **Not a project manager.** They decide *what* and *why*, not *how* the team does the work or *who* does which task.
- **Not the team's boss.** Developers decide how to build; the PO cannot tell them how many hours to work or what technical approach to use.
- **Not a requirements "thrower".** A PO who writes a long document and disappears is not doing the job. Product ownership is an ongoing conversation.
- **Not a rubber stamp for stakeholders.** Stakeholders give input; the PO decides.

#### 3.2 The Scrum Master (SM)

**One-line definition:** The Scrum Master is accountable for establishing Scrum as defined in the Scrum Guide and for the Scrum Team's effectiveness. They are a true leader who serves the team and the wider organisation.

**What the Scrum Master does:**

1. **Acts as a servant leader.** A servant leader leads by serving: their success is measured by how well the team performs, not by how many orders they give. They ask, "What does the team need from me?" rather than "What do I need the team to do for me?"
2. **Facilitates.** They make sure Scrum events happen, are positive and productive, and stay within their time-box. (The events themselves are covered in the next lesson. For now, note that the Scrum Master helps them run well.)
3. **Removes impediments.** An **impediment** (also called a blocker) is anything slowing or stopping the team: a broken test environment, a missing access permission, an unanswered question from another department. The Scrum Master helps get these resolved, either directly or by escalating.
4. **Coaches.** They coach team members in self-management and cross-functionality, and coach the Product Owner on backlog techniques and product planning. They also help the wider organisation understand and adopt Scrum.
5. **Protects the team.** They shield the team from outside interruptions and from pressure to take on more than it can finish, so the team can focus. Examples: pushing back when a manager tries to add urgent work mid-sprint without discussing it with the PO.
6. **Improves the way of working.** They help the team inspect and adapt: identifying what works, what doesn't, and what to try next.

**Why the QE cares:** The Scrum Master is often your ally when quality practices need support. If you need time to build automation, a stable test environment, or a rule such as "no story is done without tests", the Scrum Master helps raise it as an impediment or an improvement.

**What the Scrum Master is NOT:**

- **Not a project manager.** They do not assign tasks, set deadlines, track individual hours, or report on who is "behind". The team self-organises.
- **Not the team's boss or "manager".** They have no authority over developers' performance reviews in a healthy setup, and they do not approve the team's work.
- **Not the secretary.** They are not there to take minutes, book rooms, and update tickets on behalf of everyone else (although they may help with logistics).
- **Not a "Scrum police officer".** The aim is understanding and improvement, not enforcement for its own sake.
- **Not a fixer who solves everything.** A good Scrum Master helps the team learn to solve its own problems.

#### 3.3 The Developers

**One-line definition:** In Scrum, "Developers" are the people in the Scrum Team who are committed to creating any aspect of a usable Increment each sprint.

Notice the wording. "Developers" does **not** mean only people who write code. It means *everyone on the Scrum Team who does the work of building the product*: programmers, testers, designers, database specialists, and so on. (Older versions of the Guide used the term "Development Team"; you will still hear that phrase.)

**What the Developers are accountable for:**

1. **Creating a plan for the sprint** (the Sprint Backlog): deciding how they will turn the selected backlog items into a working Increment.
2. **Instilling quality by adhering to a Definition of Done.** Quality is not an afterthought; it is a built-in accountability of the people doing the work.
3. **Adapting their plan each day** toward the Sprint Goal (the single objective for the sprint).
4. **Holding each other accountable** as professionals.

**Key characteristics:**

- **Self-organising (self-managing):** The team decides *who* does *what* and *how*. Nobody outside tells them how to turn backlog items into working software.
- **Cross-functional:** Collectively, the team has all the skills needed to deliver a finished increment: coding, testing, design, deployment, and so on. They do not depend on another team to finish their own work.
- **No titles inside the team:** Scrum recognises no sub-teams and no hierarchy such as "the test team". Individuals may have specialist skills and focus areas, but accountability belongs to the Developers as a whole.

#### 3.4 Where Do Testers and QE Fit? (Important)

This is a question every trainee asks, and the honest answer has two parts.

**Part one: Scrum has no separate "tester" role.** The Scrum Guide names three roles' worth of accountabilities: Product Owner, Scrum Master, Developers. Testers, QA engineers, QEs, and SDETs are part of **Developers**. They are on the team, in the same sprint, working toward the same Sprint Goal, and share accountability for the quality of the Increment.

**Part two: testing specialists are still essential.** Scrum says *what* the team is accountable for, not that everyone must be equally skilled at everything. Real teams need people with deep expertise in:

- Designing effective tests and spotting risk
- Exploratory testing (unscripted, curiosity-driven investigation)
- Test automation and building a reliable test pipeline
- Performance, security, accessibility, and usability testing
- Asking the awkward "what if...?" questions nobody else thinks of

Think of the goalkeeper again. Every player defends, and the whole team is responsible for not conceding goals, but you still want someone who specialises in the position. In the same way, **everyone on a Scrum team contributes to quality; the QE is the specialist who leads and enables it.**

| Statement | True or false? | Why |
|---|---|---|
| "Scrum says testers are not needed." | False | Scrum says there is no separate *role*; the *skill* is still essential. |
| "Only the QE is responsible for bugs." | False | The whole Developers group is accountable for quality via the Definition of Done. |
| "A QE sits outside the Scrum Team and receives finished builds." | False (anti-pattern) | The QE is a team member, involved from refinement to review. |
| "A QE has no say in whether a story is done." | False | The QE helps define and verify "done" as part of the team. |

---

### 4. The Broader Agile Team and Stakeholders

Beyond the three Scrum accountabilities, a real project involves many other people. Some sit *inside* the Scrum Team (wearing the "Developer" hat), while others are *around* it. Titles vary between companies, so focus on the *work* each does.

| Role | What they do | How the QE works with them |
|---|---|---|
| **Business Analyst (BA)** | Studies business needs, clarifies requirements, models processes, and helps turn needs into backlog items and acceptance criteria. Sometimes supports or assists the PO. | Reviews requirements together, spots gaps and ambiguity, aligns test scenarios with business rules. |
| **UX/UI Designer** | UX (User Experience) designers study how people use the product and shape flows; UI (User Interface) designers design how screens look. | Checks designs for testability and accessibility, verifies the build matches mockups, gives early feedback on usability. |
| **DevOps / Release Engineer** | Builds and maintains the pipelines, environments, and tooling that build, test, and deploy software. DevOps joins "development" and "operations". | Agrees how automated tests run in the CI/CD pipeline (continuous integration / continuous delivery), requests stable test environments, discusses release readiness. |
| **Tech Lead / Architect** | Guides technical direction, design choices, and code quality standards. An architect focuses on overall system design. | Discusses testability of the design, integration points, non-functional risks (performance, security). |
| **Stakeholders** | Anyone with an interest in the product who is not on the team: executives, sales, support, legal, compliance, partners. | Rarely direct contact; their needs reach you through the PO. They attend the sprint review and give feedback. |
| **Customers / End Users** | The people who actually use or pay for the product. | Their real behaviour and complaints reveal what truly matters. QEs often study support tickets, analytics, and user feedback to target tests. |
| **Agile Coach** | An experienced coach who helps teams or whole organisations adopt Agile ways of working, often across multiple teams, for a limited time. | Supports quality practices at a wider level, e.g. spreading shift-left habits across teams. |

**Customer versus user versus stakeholder.** A *user* uses the product. A *customer* pays for it (the same person in some products, different people in others, such as a company buying software for employees). A *stakeholder* is anyone affected by or interested in it. All three matter to quality, because "quality" means **fit for the people who actually use the product**.

---

### 5. The QA / QE / SDET in an Agile Team, in Detail

In a traditional Waterfall project, testing was a phase after development. In Agile, **testing is an activity that happens continuously, with the QE involved from the first conversation about an idea until the feedback after release.** Let us walk through a sprint's life.

#### 5.1 Before the Sprint: Refinement and Preparation

Refinement (also called backlog grooming) is the ongoing activity of reviewing upcoming backlog items so they are clear and ready to be worked on. It is where the QE adds enormous early value, because **a defect found in a requirement costs a few minutes to fix; the same defect found in production can cost days.**

QE responsibilities:

- **Attend backlog refinement as a full participant**, not an observer.
- **Ask questions** that expose ambiguity and hidden assumptions: "What should happen if the user enters a negative quantity?" "Who is allowed to see this?" "What does 'fast' mean, in seconds?"
- **Help write and sharpen acceptance criteria** so they are specific, testable, and unambiguous.
- **Check testability.** A story is *testable* if you can design a clear test with a clear pass/fail result and can set up the data and environment to run it. If it isn't, raise it now. Example: "How would I test 'the page should feel responsive'? Can we agree on a measurable target such as 'loads in under 2 seconds'?"
- **Identify risks** (what could go wrong, how likely, how severe) and suggest where the testing effort should concentrate.
- **Spot dependencies and test-data needs**: other teams, third-party services, special accounts, or environments.
- **Contribute to estimates.** Testing effort is part of the real effort. If the story looks like "two hours of coding" but "two days of testing", the team should know.
- **Think about the non-functional side**: performance, security, accessibility, compatibility.

#### 5.2 During the Sprint: Build Quality In

This is where the QE role shows how different Agile is from the old "throw it over the wall" model.

- **Test design early.** Begin designing test scenarios and test data from the acceptance criteria while developers are still building. Do not wait for a finished build.
- **Shift-left testing.** "Shift left" means moving quality activities *earlier* (to the left on a timeline that runs from idea to release). Examples: reviewing requirements, reviewing designs, helping developers write unit tests, and checking early builds.
- **Pair with developers.** Sit with a developer (physically or on a call) while they build and run the test ideas together. Pairing catches problems in minutes and spreads quality skills in both directions.
- **Test in small slices.** As soon as a small piece of a story works on a test environment, test it, then give quick feedback. Do not wait for the whole story.
- **Exploratory testing.** Simultaneously learn the product, design tests, and execute them, guided by curiosity and risk. It finds the surprising problems scripted tests miss.
- **Automation.** Build and maintain automated checks (unit, API, UI, regression) so repetitive verification runs quickly and often, freeing humans for thinking-heavy work. The QE/SDET often owns the structure of the automation framework, but developers write many of the checks too.
- **Maintain the regression safety net.** Regression testing re-checks existing functionality to make sure new changes did not break it. Automated regression suites are what make frequent releases safe.
- **Log defects clearly and quickly**, discuss them with the developer directly (a conversation beats a long ticket thread), and re-test fixes.
- **Take part in the daily team sync** and flag testing blockers (such as an unstable environment) immediately.
- **Keep the test status visible**: what's tested, what's at risk, what's left.

#### 5.3 The Three Amigos

The **Three Amigos** is a short collaborative conversation about a user story, held *before* development starts, between three perspectives:

1. **Business / Product** (usually the Product Owner or a BA): *What problem are we solving and why?*
2. **Development**: *How could we build it, and what is technically tricky?*
3. **Testing / Quality** (the QE): *What could go wrong, and how will we know it works?*

The aim is a shared understanding, so everyone leaves with the same picture of the story, concrete examples, and agreed acceptance criteria. It prevents the costly misunderstanding where the PO imagines one thing, the developer builds another, and the QE tests a third. A Three Amigos session is often 15 to 30 minutes per story, and it is not limited to exactly three people; the name refers to the three *perspectives*.

#### 5.4 At the End of the Sprint: Show, Reflect, Improve

(The events themselves are covered in detail in the next lesson; here is the QE's part.)

- **Sprint Review / Demo:** Help demonstrate the finished work to stakeholders, show what was tested and how, speak honestly about known limitations and risks, and capture feedback.
- **Release readiness:** Contribute facts to the decision of whether the Increment is good enough to release: test results, open defects and their severity, risk areas, and coverage.
- **Retrospective:** Bring quality-related observations: "Three bugs came from unclear acceptance criteria", "Our regression suite takes too long." Propose small, concrete improvements.

#### 5.5 Metrics and Quality Advocacy

QEs also help the team see how it is doing. Common quality indicators include:

| Metric | What it tells you | Caution |
|---|---|---|
| Defect escape rate (defects found in production vs. before release) | How well the team catches problems before users do | Do not use to blame individuals |
| Test automation coverage / pass rate | How much repeatable checking is automated and how stable it is | High coverage does not equal high quality |
| Defect trends by severity and area | Where the product is fragile | Look for patterns, not scapegoats |
| Escaped-defect root causes | Which process gap let a bug through | Fix the process, not the person |
| Cycle time / flow of stories through "done" | Whether quality work is slowing or enabling delivery | Combine with other data |

**Quality advocacy** means being the team's voice for the user and for sustainable quality: raising risks early, politely and with evidence; recommending improvements; and teaching others testing skills. A strong QE is influential through collaboration, not through authority.

---

### 6. The Whole-Team Quality Mindset

**Whole-team quality** is the belief that *everyone* is responsible for the quality of the product, not just the testers. It changes behaviour:

| Old mindset ("QA owns quality") | Whole-team mindset |
|---|---|
| Developers write code, QA finds the bugs | Developers write unit tests and self-check; QE helps them test smarter |
| "It's QA's job to catch it" | "We built it, we make sure it works" |
| PO writes the story and disappears | PO joins the conversation about examples and acceptance |
| Quality is checked at the end | Quality is built in at every step |
| Bugs are blamed on people | Bugs are learning opportunities for the process |

The QE's role in this mindset is that of a **quality coach and enabler**: helping the team prevent defects, not only detect them. The famous idea is that you cannot "test quality into" a product at the end; you have to build it in.

---

### 7. Definition of Ready vs. Definition of Done

These two checklists are among the most practical tools for clear responsibilities. Do not confuse them.

#### 7.1 Definition of Ready (DoR)

The **Definition of Ready** is a team-agreed checklist describing what a backlog item must have *before* the team will take it into a sprint. (Note: the DoR is a widely used *practice*; it is not an official Scrum artifact, but many teams find it valuable. Treat it as a guide, not a rigid gate.)

**Example DoR for a user story:**

- The story is written clearly in the agreed format and has a business value statement.
- Acceptance criteria are written, specific, and testable.
- Dependencies (other teams, services, designs) are identified and available.
- The team has discussed the story (for example, in a Three Amigos session) and understands it.
- The story is small enough to finish within one sprint.
- UI designs or mockups (if needed) are attached.
- Test data and environment needs are known.

**Who owns it?** The whole team agrees the DoR. The PO typically drives items towards "ready"; the QE checks testability.

#### 7.2 Definition of Done (DoD)

The **Definition of Done** is a formal description of the state of the Increment when it meets the quality measures required for the product. It *is* an official part of Scrum. When a backlog item meets the DoD, it is considered finished. If it doesn't, **it is not done**, and it cannot be released or even shown as complete. The Developers are accountable for adhering to it.

**Example DoD for a user story:**

- Code is written, reviewed by a peer, and merged.
- Unit tests written and passing.
- Acceptance criteria verified by test (manual and/or automated).
- Automated regression suite passes.
- No open critical or high-severity defects linked to the story.
- Accessibility and cross-browser checks completed for UI changes.
- Documentation updated where needed.
- Deployed to the test/staging environment and checked.
- PO has accepted the story.

#### 7.3 Side-by-Side

| | Definition of Ready | Definition of Done |
|---|---|---|
| **Question it answers** | "Is this story clear enough to start?" | "Is this work truly finished to our quality standard?" |
| **When it applies** | Before the sprint / before work starts | When work is complete |
| **Official Scrum?** | No, a common team practice | Yes, an official commitment for the Increment |
| **Main guard against** | Starting work on vague, risky items | Releasing unfinished or low-quality work |
| **QE focus** | Testability, clarity of criteria, test data | Tests passing, defects resolved, regression safe |
| **Typical owner** | Team (PO leads) | Developers (whole team, including QE) |

A quick way to remember: **Ready is the front door; Done is the exit.** Do not confuse *acceptance criteria* (specific to one story) with the *Definition of Done* (common to every story).

---

### 8. Accountability and Collaboration Matrix (RACI-Style)

A **RACI matrix** shows who is **R**esponsible (does the work), **A**ccountable (answers for the outcome; ideally one person per item), **C**onsulted (gives input before decisions), and **I**nformed (told the result). Scrum does not mandate RACI, and in Scrum "self-managing" means the team shares work, so treat this table as a *conversation starter* about typical responsibilities, not a rulebook. Roles: **PO**, **SM** (Scrum Master), **Dev** (developers writing code), **QE**, **BA/UX/DevOps** (supporting roles).

| Activity | PO | SM | Dev | QE | BA / UX / DevOps |
|---|---|---|---|---|---|
| Define product goal and priorities | A/R | I | C | C | C |
| Write and order backlog items | A/R | I | C | C | R (BA helps) |
| Write acceptance criteria | A | I | C | R (sharpens, checks testability) | R (BA) |
| Three Amigos story discussion | A | I | R | R | C |
| Estimate stories | C | I | A/R | R | I |
| Build the feature | I | I | A/R | C | C (UX, DevOps) |
| Write unit tests | I | I | A/R | C (reviews/coaches) | I |
| Design test cases and test data | I | I | C | A/R | C |
| Exploratory testing | I | I | R | A/R | C |
| Build / maintain test automation | I | I | R | A/R (leads) | C (DevOps) |
| Maintain CI/CD pipeline and environments | I | C (removes blockers) | C | C | A/R (DevOps) |
| Log and triage defects | C (priority) | I | R | R | I |
| Meet the Definition of Done | C | I | A/R | R | C |
| Accept the finished story | A/R | I | C | C | I |
| Remove impediments | I | A/R | R | R | R |
| Facilitate the team's working agreements | I | A/R | R | R | I |
| Demo to stakeholders | A (value) | C | R | R | I |
| Release decision (go/no-go input) | A | C | R | R (provides quality facts) | R (DevOps) |
| Retrospective improvements | R | A (facilitates) | R | R | C |

Reading tips: the QE row entries marked **A/R** are the areas where the QE *leads*; the Developers' **A** for "Meet the Definition of Done" shows that *quality is a collective accountability* in which the QE is a key contributor, not the sole owner. The PO's **A** on acceptance shows who has the final word on value.

---

### 9. Common Anti-Patterns

An **anti-pattern** is a habit that looks like a solution but causes problems. Learning to recognise them is a core QE skill.

| Anti-pattern | What it looks like | Why it hurts | Better approach |
|---|---|---|---|
| **Mini-waterfall inside the sprint** | Developers code during days 1-7; QE tests only in days 8-10 | Bugs surface too late, testing is squeezed, stories carry over | Slice stories small, test each slice as it's built, automate as you go, pair early |
| **Tester as gatekeeper** | QE is seen as the one who "approves" or "blocks" releases | Developers stop owning quality; QE becomes a bottleneck and unpopular | QE provides information on risk; the team and PO decide; quality is shared |
| **Product Owner unavailable** | PO is in other meetings, answers take days, stories are vague | Developers guess; rework; rejected work at the end | Agree PO availability windows; escalate the impediment via the Scrum Master; empower a delegate |
| **Scrum Master as manager** | SM assigns tasks, tracks individual hours, demands status reports | Kills self-organisation and trust | SM facilitates and coaches; the team plans its own work |
| **QE outside the team** | A separate "QA team" receives builds | Handoffs, delays, "us vs. them" | QE embedded in the Scrum Team with shared goals |
| **Stories without acceptance criteria** | "Make the login better" | Everyone interprets differently; testing is guesswork | Use Three Amigos; apply the Definition of Ready |
| **"Done" means "coded"** | Story marked done without testing or review | Hidden unfinished work, technical debt | Enforce a clear Definition of Done |
| **PO as a proxy messenger** | PO relays every question between team and stakeholders slowly | Delays; lost context | Allow direct, timely access to stakeholders where appropriate |
| **Automation only after the sprint** | Automation backlog grows "for later" | Never catches up, fragile suites | Include automation in the DoD for each story |

---

### 10. A Day in the Life of a QE in a Sprint

Imagine a **two-week sprint** (10 working days). The exact timing differs between teams, but the pattern of continuous involvement is the same. Event names are mentioned only briefly; they are covered in the next lesson.

| Time in sprint | Typical QE activities |
|---|---|
| **Day 1 morning** | Sprint planning: help the team understand each selected story, raise testing effort and risks, contribute to the plan. |
| **Day 1 afternoon** | Review acceptance criteria for the first stories; start designing test scenarios and preparing test data. |
| **Day 2** | Daily sync (about 15 minutes) to share progress and blockers. Pair with a developer on the first story; write test ideas as automated checks where possible. |
| **Day 3** | Test the first small slice on the test environment; give same-day feedback; log defects and discuss them directly with the developer. |
| **Day 4** | Exploratory testing session on the completed story; update automation; join a Three Amigos conversation for a story coming up next sprint. |
| **Day 5** | Mid-sprint check: review the sprint board and risks; re-test fixed defects; run regression suite; raise any environment problem to the Scrum Master. |
| **Day 6** | Backlog refinement: ask clarifying questions on upcoming stories; check testability; review UX designs for accessibility. |
| **Day 7** | Test the second story's slices; coordinate with DevOps on the pipeline stability; extend automated API/UI tests. |
| **Day 8** | Verify all acceptance criteria against the Definition of Done; check non-functional items (performance, cross-browser); confirm no critical defects remain. |
| **Day 9** | Final regression run; prepare the demo and a concise quality summary (what's tested, known issues, risks); agree with the PO on acceptance. |
| **Day 10 morning** | Sprint review: demo with the team, discuss limitations honestly, capture stakeholder feedback. |
| **Day 10 afternoon** | Retrospective: share quality observations and suggest one or two small improvements; start preparing for the next sprint's stories. |

Notice that **testing happens every day** and that the QE spends meaningful time on *prevention* (refinement, Three Amigos, pairing) as well as *detection* (testing).

---

### 11. Example Dialogue: Refining a User Story

A **user story** is a short description of a feature from the user's point of view, often in the form "As a [type of user], I want [goal], so that [benefit]." The following is a sample backlog refinement conversation for a shopping app.

**The story:** *As a registered customer, I want to apply a discount code at checkout, so that I can pay less for my order.*

**Participants:** Priya (Product Owner), Marcus (Developer), Aisha (Quality Engineer).

> **Priya (PO):** The goal is simple. A customer enters a discount code at checkout and the order total drops. Marketing wants this for next month's campaign, so it's a high priority.
>
> **Marcus (Dev):** Understood. I can build an input box and a button that calls a discount service. What kinds of codes are there?
>
> **Aisha (QE):** Before that, can I ask a few questions? What happens if the code is expired, or it's already been used, or someone types it in lowercase?
>
> **Priya:** Good questions. Expired and already-used codes should show a clear error message. Codes are not case-sensitive.
>
> **Aisha:** Can a customer apply more than one code to a single order?
>
> **Priya:** Hmm, I hadn't thought about that. Let's say only one code per order for now.
>
> **Marcus:** That simplifies things. What about a percentage code on an order of zero value, or a fixed amount bigger than the cart total? Do we allow a negative total?
>
> **Priya:** No negative totals. The minimum order total is zero.
>
> **Aisha:** And what does "show a clear error" mean? Can we agree on the text, so I can write a precise check?
>
> **Priya:** I'll ask our content designer for the wording, but the message should say whether the code is expired, invalid, or already used.
>
> **Aisha:** One more. For testing, I'll need a few sample codes: valid, expired, used, and invalid. Can we create them in the test environment?
>
> **Marcus:** Yes, I'll add a seed script for that.
>
> **Aisha:** Finally, how will we know it's fast enough? Does the total update within, say, two seconds?
>
> **Priya:** Two seconds is fine.
>
> **Marcus:** I can also write unit tests for the calculation rules so you don't have to retest every number by hand.
>
> **Aisha:** Great. Let me read back the acceptance criteria and see if we agree:
> 1. A valid code reduces the order total and shows the discount line.
> 2. Codes are not case-sensitive.
> 3. An expired, invalid, or already-used code shows a specific error message and the total does not change.
> 4. Only one code can be applied per order.
> 5. The total never goes below zero.
> 6. The total updates within two seconds.
>
> **Priya:** That's exactly what I meant. I'll update the story.

**What happened here?**

- The **PO** supplied purpose, priorities, and decisions (one code per order, no negative totals).
- The **Developer** raised technical considerations and committed to unit tests and test data.
- The **QE** asked "what if?" questions, made vague ideas measurable, and turned the discussion into acceptance criteria *before any code was written*. This is shift-left in action.

---

## Examples: Putting It Together

**Example 1: Who decides? (Quality trade-off)**
The team discovers on day 9 that a minor visual defect exists on one old browser version. Who decides whether to fix it now? The **QE** reports the facts (severity, who is affected, workaround). The **PO** decides about value and priority (fix now, or add to the backlog). The **Developers** estimate the effort. The **Scrum Master** makes sure the conversation is respectful and informed. Nobody "blocks" alone.

**Example 2: An impediment**
The test environment has been down for two days. The QE raises it at the daily sync. The **Scrum Master** takes it as an impediment, contacts the DevOps engineer and the infrastructure manager, and reports back. The QE did not need to give up and wait.

**Example 3: Definition of Ready in action**
A story arrives for planning that says "Improve search." The QE points out that it has no acceptance criteria and no performance expectation. According to the team's DoR, it is *not ready*. The PO and BA refine it with the team before it enters a sprint, saving a week of rework.

---

## Applying It to Project 1 - QE Foundations

Project 1 is a sample web app (for example, an online store or booking site) that you are planning quality for. For the project, imagine a small, realistic team of eight:

| Team member | Role in Project 1 | Key responsibilities for the project |
|---|---|---|
| Person A | **Product Owner** | Defines the Product Goal, orders the backlog, answers questions quickly, accepts finished stories |
| Person B | **Scrum Master** | Helps the team work well, removes blockers (for example, no test environment), coaches on Agile practices |
| Person C | **Developer (front end)** | Builds user interface features, writes unit tests, fixes defects |
| Person D | **Developer (back end)** | Builds APIs and database logic, writes unit and API tests |
| Person E | **Quality Engineer (you)** | Joins refinement, writes testable acceptance criteria, designs tests, performs exploratory testing, starts automation, reports quality status |
| Person F | **Business Analyst** | Clarifies requirements and business rules, helps write backlog items |
| Person G | **UX/UI Designer** | Creates wireframes, checks usability and accessibility |
| Person H | **DevOps Engineer** | Maintains the test environment and the pipeline that runs automated tests |

Outside the team: **stakeholders** (for example, the business owner, marketing, customer support) and **end users** (shoppers or customers of the web app).

For Project 1 this week you will:

1. Confirm who plays each role on your team.
2. Draft a **Definition of Ready** and a **Definition of Done** for the project.
3. Use the roles to decide who you would ask for each type of question (see the activity below).

---

## Knowledge Check

Try to answer each question before reading the short answer.

**1. Name the three accountabilities in a Scrum Team.**
*Answer:* Product Owner, Scrum Master, and Developers.

**2. Where does a QE sit in Scrum?**
*Answer:* Within the Developers. There is no separate tester role; testers and QEs are part of the team that creates the Increment and share accountability for quality.

**3. Who is accountable for ordering the Product Backlog?**
*Answer:* The Product Owner (although they may delegate the work of writing items).

**4. Is the Scrum Master a project manager? Explain.**
*Answer:* No. The Scrum Master is a servant leader who facilitates, coaches, and removes impediments. They do not assign tasks or manage individual performance; the team self-manages.

**5. What does "cross-functional" mean for a Scrum Team?**
*Answer:* The team collectively has all the skills needed to deliver a finished Increment without depending on people outside the team.

**6. Define the Three Amigos and state when it is held.**
*Answer:* A short conversation among business, development, and testing perspectives to build shared understanding of a story, held before development starts.

**7. What is the difference between the Definition of Ready and the Definition of Done?**
*Answer:* Ready is the checklist a story must meet *before* work begins; Done is the checklist that must be met for work to be considered *finished* at the quality standard. Done is an official Scrum commitment; Ready is a common team practice.

**8. Give two things a QE does before the sprint starts.**
*Answer:* Examples: attend refinement, ask clarifying questions, help write acceptance criteria, check testability, identify risks and test-data needs.

**9. What is "shift-left" testing?**
*Answer:* Moving testing and quality activities earlier in the development timeline (such as reviewing requirements and helping with unit tests) so problems are found sooner and cost less to fix.

**10. Identify the anti-pattern: "Developers finish coding on day 8, then the QE has two days to test everything."**
*Answer:* A mini-waterfall inside the sprint. Fix by slicing stories small, testing as you build, and automating early.

**11. Why is a "tester as gatekeeper" approach unhealthy?**
*Answer:* It makes quality the QE's sole responsibility, creates bottlenecks, and encourages developers to stop owning quality. The QE should provide information on risk while the whole team shares accountability.

**12. A story has no acceptance criteria. Which role helps fix this and who accepts the story at the end?**
*Answer:* The PO, BA, developers, and QE work together to write and sharpen the criteria (the QE particularly checks testability); the Product Owner accepts the finished story.

---

## Try It: Role-Play Activity (Project 1)

**Time:** 40 to 50 minutes. **Group size:** 4 or more trainees (or play several parts yourself if working alone).

**Scenario.** Your Project 1 web app needs a new story: *"As a user, I want to reset my forgotten password, so that I can regain access to my account."*

**Step 1: Assign roles (5 minutes).** Choose who plays the Product Owner, Scrum Master, a Developer, and the Quality Engineer. Optional: add a BA and a UX designer. If you have fewer people, rotate.

**Step 2: Prepare (10 minutes).**
- The **PO** writes down three business rules they have in mind (for example, how long the reset link stays valid) but shares them only when asked.
- The **Developer** thinks about technical constraints (email service, security).
- The **QE** prepares at least eight questions covering: valid and invalid inputs, security, error messages, edge cases (unregistered email, expired link, reused link), accessibility, and performance.
- The **Scrum Master** prepares to observe, to keep the conversation on track, and to note any impediment (for example, "no test email service in the test environment").

**Step 3: Hold a Three Amigos conversation (15 minutes).** Discuss the story. The QE leads with questions; the PO answers; the Developer explains feasibility. Write down every agreement.

**Step 4: Write acceptance criteria (10 minutes).** As a group, write 5 to 7 acceptance criteria that are specific and testable.

**Step 5: Check against a Definition of Ready (5 minutes).** Use the example DoR from this lesson. Is the story ready? If not, what is missing?

**Step 6: Debrief (5 minutes).** Discuss:
- Which questions changed the story the most?
- Which role found it hardest to keep to its own accountability?
- Did anyone slip into an anti-pattern (for example, the Scrum Master assigning tasks)?
- What impediment did the Scrum Master identify?

**Deliverable.** Save your acceptance criteria and a one-paragraph reflection for Project 1. You will refine these as you learn the defect lifecycle, Jira, and test-design techniques later this week.

**Stretch challenge.** Write a first draft of your own Definition of Done for Project 1 with at least eight items, and mark which ones the QE would lead on.

---

## Key Takeaways

- Scrum defines **three accountabilities**: the **Product Owner** (value and the backlog), the **Scrum Master** (the team's effectiveness and the Scrum way of working), and the **Developers** (building a quality Increment).
- **QE, QA, and SDET professionals are part of the Developers.** There is no separate tester role in Scrum, but the skill is essential, and QEs lead and enable quality.
- The **Product Owner** is not a project manager, and the **Scrum Master** is not a manager; the Scrum Master serves, coaches, and removes impediments.
- Around the Scrum Team sit supporting roles (BA, UX/UI, DevOps, tech lead/architect, Agile coach) and **stakeholders, customers, and end users**, whose needs shape what quality means.
- A QE contributes **before the sprint** (refinement, questions, acceptance criteria, testability), **during the sprint** (test design, exploratory testing, automation, pairing, shift-left), and **at the end** (demo, review, retrospective, metrics, quality advocacy).
- **Whole-team quality** means everyone shares responsibility for quality; the QE is the specialist and coach.
- The **Three Amigos** (business, development, testing) align understanding before coding starts.
- **Definition of Ready** is the front door for stories; **Definition of Done** is the exit standard for finished work.
- Watch for anti-patterns: **mini-waterfall**, **gatekeeper testers**, **absent Product Owners**, and **Scrum Masters acting as managers**.
- In Project 1, you will practise these roles by assigning them to a team and rehearsing refinement conversations.

---

## Additional Resources

- **The Scrum Guide** (the official definition of Scrum, including the accountabilities of the Scrum Team): https://scrumguides.org
- **Atlassian: Agile team roles and how Scrum teams are organised** (beginner-friendly overview of Scrum roles): https://www.atlassian.com/agile/scrum/roles
- **Agile Alliance Glossary** (clear definitions of terms such as Definition of Done, user story, and Three Amigos): https://www.agilealliance.org/agile101/agile-glossary/
