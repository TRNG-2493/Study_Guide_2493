# Waterfall, Agile, Scrum, Kanban and Hybrid Approaches

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain what a software development methodology (a "delivery model") is and why teams need one.
- Describe the Waterfall model, its phases, strengths, weaknesses, and the "late-testing problem."
- Explain the V-Model and match each development phase to its paired test level.
- State the four values and twelve principles of the Agile Manifesto in plain language, and explain why Agile emerged.
- Describe iterative and incremental delivery, and explain how testing works in Agile (continuous testing and the whole-team approach).
- Give a high-level overview of Scrum: the three pillars of empiricism, sprints, and the three artifacts.
- Describe Kanban: its board, columns, WIP limits, pull system, flow, and cycle time versus lead time.
- Compare Scrum and Kanban, and explain hybrid approaches such as Water-Scrum-Fall and Scrumban.
- Choose a delivery model for a given project and justify the choice.
- Describe where the Quality Engineer (QE) or tester fits in every model.

---

## Why This Matters

Every software team answers one question before writing a single line of code: "How will we organize our work?" The answer is the team's delivery model, and it shapes almost everything a Quality Engineer does: when you get to see the product, how much time you have to test it, how often requirements change, how quickly bugs are fixed, and how you talk to developers and business people.

In the previous lesson on the Software Development Life Cycle (SDLC), you learned the phases every product passes through: planning, requirements, design, development, testing, deployment, and maintenance. That lesson told you what phases exist. This lesson tells you how teams arrange those phases. Do we do them once, in order? Or do we repeat them in small loops? The same phases appear in every model; only their order, size, and overlap change.

Industry relevance is direct and immediate. Job descriptions for test automation engineers routinely say "experience working in an Agile/Scrum environment." In interviews you will be asked, "What is the difference between Waterfall and Agile?" and "Where does testing fit in a sprint?" In your first week on a real team, you will join a daily meeting, see a board of work items, and hear words like "backlog," "sprint," and "WIP." This lesson makes those words familiar.

This lesson also supports this week's Weekly Epic: building the quality-engineering mindset. Quality is not something added at the end; it depends on how work flows through the team. Over the week you will learn the STLC, Jira, defect lifecycle, testing principles, and test-design techniques, and you will apply each idea to **Project 1 - QE Foundations**, a sample web app you plan quality for. Today's step: decide which delivery model suits that project, because every later quality activity (test planning, defect tracking, test design) is scheduled inside that model.

---

## The Concept

### 1. What is a delivery model (methodology)?

A **software development methodology** (also called a **delivery model** or **process model**) is an agreed way of organizing the work of building software: who does what, in what order, how often, and how progress is checked.

An analogy: cooking.

- **Cooking a banquet for 200 guests (Waterfall).** The menu is fixed weeks in advance. You shop for every ingredient, prepare every dish, and plate everything. Only at the banquet do the guests taste the food. If the soup is too salty, it is discovered when it is too late and too costly to fix.
- **Cooking for friends at home, tasting as you go (Agile).** You make one dish, taste it, ask people what they think, adjust the seasoning, and then make the next dish. Surprises are caught early because feedback is constant.

Neither style is "wrong." A banquet needs planning and discipline; a home dinner needs flexibility. Software teams also choose styles that fit their situation. Keep this analogy in mind; we will return to it.

Two terms you will see throughout:

- **Iterative**: repeating a cycle (plan, build, test, review) several times, improving the product each round.
- **Incremental**: delivering the product in usable pieces (increments), each adding new capability to what already exists.

Think of drawing a portrait. *Incremental* is finishing the left eye perfectly, then the right eye, then the nose. *Iterative* is sketching the whole face roughly, then refining it again and again. Agile teams usually do both: each cycle produces a small, working, improved piece.

---

### 2. Waterfall

#### 2.1 History

The **Waterfall model** is the classic, sequential approach. It is commonly traced to a 1970 paper by Winston W. Royce, titled "Managing the Development of Large Software Systems." Royce drew the sequence of stages that later became famous as the waterfall picture. Interestingly, Royce himself warned that a strictly one-pass sequence was risky and recommended feedback between stages. The industry, however, adopted the simple one-way version, and for decades it was the standard, especially in government, defense, and large engineering projects. The name comes from the picture: work "flows" downward from one phase to the next, like water over a series of steps, and does not flow back up.

#### 2.2 Phases

In Waterfall, each phase is completed fully before the next begins. The output of one phase is the input of the next, and a formal **sign-off** (written approval) usually closes each phase.

```
 Requirements
      |
      v
   Design
      |
      v
Implementation (coding)
      |
      v
   Testing (verification)
      |
      v
 Deployment
      |
      v
  Maintenance
```

| Phase | What happens | Typical output |
|---|---|---|
| Requirements | Gather and document everything the system must do | Requirements specification document |
| Design | Plan the architecture, database, screens | Design documents |
| Implementation | Developers write the code | Working code |
| Testing | The whole system is verified against the requirements | Test results, defect reports |
| Deployment | Release to users | Live system |
| Maintenance | Fix problems, make later changes | Patches and updates |

(These are the same SDLC phases from the previous lesson, now arranged strictly one after another.)

#### 2.3 Strengths

- **Simple and easy to understand.** Everyone knows what phase the project is in.
- **Clear structure and milestones.** Each phase has defined start and end points.
- **Thorough documentation.** Valuable for audits, handovers, and long-lived systems.
- **Predictable planning.** When requirements are stable, cost and schedule can be estimated up front.
- **Easy to manage large, distributed teams** because responsibilities are well defined.

#### 2.4 Weaknesses

- **Changes are expensive.** Going back to an earlier phase is difficult and costly.
- **Users see nothing until late.** Working software appears only near the end, so misunderstandings stay hidden for months.
- **Assumes requirements are complete and correct at the start.** In real life, people rarely know exactly what they want until they see something.
- **Risk is pushed to the end.** The hardest integration problems appear when time and budget are almost gone.
- **Testing is squeezed.** See the next section.

#### 2.5 Testing's role and the late-testing problem

In pure Waterfall, testing is its own phase that begins only after coding is finished. This creates the **late-testing problem**:

1. **Defects (bugs) are found late.** A mistake made in the requirements phase might not be discovered until testing, months later. It is possible a wrong requirement was built into everything.
2. **Late defects cost more to fix.** A widely repeated rule of thumb in software engineering is that the later a defect is found, the more expensive it is to fix, because more work (design, code, documents, other features) has been built on top of it. Fixing a typo in a requirement costs minutes; fixing the same misunderstanding after release can cost weeks.
3. **Schedule pressure lands on testers.** If earlier phases run late, the deadline usually stays fixed, so the testing phase gets shortened. Testers are then asked to test thoroughly in the least time.
4. **Everything is tested at once.** Large amounts of untested code arrive together, so finding the cause of a failure is harder.

Analogy: tasting the banquet only when the guests sit down.

A good QE does not wait for the testing phase even in Waterfall. They review requirements and designs for gaps and ambiguities (this is called **static testing**, checking documents without running code), and prepare test plans early. This idea of testing early is formalized in the V-Model below.

#### 2.6 When to use Waterfall

Waterfall fits when:

- Requirements are well understood, stable, and unlikely to change.
- The technology is familiar, and the work is similar to past projects.
- Regulations or contracts demand heavy documentation and formal approvals (for example, medical device software or aviation systems).
- The project is short, small, and simple.
- Fixed-price contracts require a fixed scope up front.
- Hardware is involved and cannot easily be changed late (for example, embedded systems).

#### 2.7 Worked example: an online bookstore, Waterfall style

A company, PageTurn, wants an online bookstore. They choose Waterfall and plan a 9-month project.

- Months 1-2 (Requirements): Business analysts interview stakeholders and write a 120-page requirements document. It says customers can search, add to cart, check out with a credit card, and track orders. Everyone signs it.
- Month 3 (Design): Architects design the database and screens. Signed off.
- Months 4-7 (Implementation): Developers build search, cart, checkout, and order tracking.
- Months 8-9 (Testing): Testers receive the complete system for the first time. They find that checkout fails when the cart holds more than 10 items, search is slow, and, worse, the requirements never mentioned discount codes, which marketing assumed were included.
- Deployment is delayed by 6 weeks. Discount codes are postponed to a "phase 2."

What went well: clear plan, good documentation. What went wrong: bugs and a missing feature were found only after 7 months of work, and testers had just 8 weeks to test everything. This is the late-testing problem in action.

---

### 3. The V-Model (a Waterfall variant)

The **V-Model** (Verification and Validation model) keeps Waterfall's sequential nature but makes the testing story much stronger. Each development phase on the left side of the "V" is paired with a test level on the right side. The key idea: **test planning and test design for each level start when the matching phase starts**, not after coding.

```
Requirements ------------------------------------ Acceptance Testing
    \                                                  /
   System Design -------------------------- System Testing
        \                                          /
     Architecture/High-level Design ---- Integration Testing
              \                                /
          Detailed (Module) Design --- Unit Testing
                       \              /
                          CODING
```

| Development phase (left side) | Paired test level (right side) | What the test level checks |
|---|---|---|
| Business requirements | Acceptance testing | Does the product meet the business needs and are users satisfied? |
| System requirements / design | System testing | Does the complete system work as specified? |
| Architecture / high-level design | Integration testing | Do the modules work correctly together? |
| Module / detailed design | Unit testing | Does each small piece of code work on its own? |

Two terms:

- **Verification** answers "Are we building the product right?" (does it follow the specification?). It is checked while moving down the left side.
- **Validation** answers "Are we building the right product?" (does it meet real user needs?). It is checked on the right side.

Strengths: testing is planned early, each phase has a matching quality check, and defects in requirements are more likely to be discovered by test-minded reviewers. Weaknesses: it is still sequential, still inflexible to change, and working software still arrives late. The V-Model is common in regulated fields (automotive, medical, aerospace). Test levels are explained in detail later in the curriculum; for now, just remember the pairing idea: every build phase has a test partner.

---

### 4. Agile

#### 4.1 Why Agile emerged

By the 1990s, many teams were frustrated. Projects ran over budget, finished late, or delivered software that no longer matched what users needed because the business had changed during a long build. Heavy documentation and rigid phases made reacting to change painful. Several lighter methods (Extreme Programming, Scrum, Crystal, DSDM, and others) appeared. In February 2001, seventeen software practitioners met in Snowbird, Utah, and wrote the **Manifesto for Agile Software Development**: a short statement of shared values. "Agile" means able to move quickly and adapt easily.

Important: Agile is **not a single process**. It is a set of values and principles. Scrum and Kanban are specific frameworks and methods that put those values into practice. (Others include XP, or Extreme Programming.)

#### 4.2 The four values of the Agile Manifesto

The manifesto says: "We are uncovering better ways of developing software... Through this work we have come to value:"

| We value more | ...over | Plain-language meaning |
|---|---|---|
| **Individuals and interactions** | processes and tools | Good conversations and a team that works well together matter more than following a procedure or owning a fancy tool. |
| **Working software** | comprehensive documentation | A product that actually runs is the best measure of progress; documents are useful but are not the goal. |
| **Customer collaboration** | contract negotiation | Work with the customer continuously rather than arguing over a contract line by line. |
| **Responding to change** | following a plan | A plan is a guide, not a prison; when facts change, change the plan. |

The manifesto adds: "while there is value in the items on the right, we value the items on the left more." Agile does not say "no documents, no plans, no tools." It says what to prioritize when you must choose. This is the most commonly misunderstood sentence in Agile.

#### 4.3 The twelve principles in plain language

1. **Satisfy the customer through early and continuous delivery of valuable software.** Deliver something useful soon, then keep delivering.
2. **Welcome changing requirements, even late in development.** Change is a competitive advantage, not a nuisance.
3. **Deliver working software frequently**, from a couple of weeks to a couple of months, with a preference for the shorter time.
4. **Business people and developers must work together daily.** No "throwing requirements over the wall."
5. **Build projects around motivated individuals.** Give them the environment and support they need, and trust them to get the job done.
6. **Face-to-face conversation is the most efficient way to convey information.** (Today, this includes video calls.) Talk, rather than only emailing documents.
7. **Working software is the primary measure of progress.** "90 percent done" means little; "it works and you can try it" means a lot.
8. **Agile processes promote sustainable development.** Teams should keep a pace they can maintain indefinitely; no endless overtime.
9. **Continuous attention to technical excellence and good design enhances agility.** Clean work stays easier to change.
10. **Simplicity, the art of maximizing the amount of work not done, is essential.** Do not build what nobody needs.
11. **The best architectures, requirements, and designs emerge from self-organizing teams.** Teams closest to the work decide how to do it.
12. **At regular intervals, the team reflects on how to become more effective, then tunes and adjusts its behavior.** Keep improving the way you work.

Notice how many principles touch quality: working software, technical excellence, sustainable pace, and regular reflection. Agile and quality go hand in hand.

#### 4.4 Iterative and incremental delivery

Instead of one big journey, Agile slices the project into short cycles (often 1-4 weeks). In each cycle the team plans a small set of features, designs, builds, tests, and releases a **working increment**. Then feedback shapes the next cycle.

```
Waterfall:  [Requirements][Design][Code............][Test][Release]
                                                           ^ users see it here

Agile:      [Plan>Build>Test>Review]  -> Release 1 (small, usable)
                 [Plan>Build>Test>Review]  -> Release 2 (more features)
                      [Plan>Build>Test>Review]  -> Release 3 ...
                       ^ users give feedback after every cycle
```

This is the home dinner: make a dish, taste it, adjust, and make the next dish.

#### 4.5 Benefits

- Faster delivery of value; users can use early versions.
- Constant feedback reduces the risk of building the wrong thing.
- Changes are welcome and cheaper because each step is small.
- Defects are found sooner and cost less to fix.
- Greater transparency; stakeholders see real progress.
- Higher team motivation through ownership and collaboration.

#### 4.6 Challenges

- **Less predictability** of the final scope, cost, and date, which is difficult for fixed-price contracts.
- **Requires discipline and cultural change.** Teams that "go Agile" by only skipping documents get chaos, not agility.
- **Needs customer involvement,** which busy stakeholders may not provide.
- **Risk of scope creep** if changes are accepted without limit.
- **Regression risk.** Because the product changes every cycle, old features can break. Without test automation, repeated manual re-testing becomes overwhelming. (This is one major reason test automation engineers are in demand.)
- **Scaling** to many teams requires extra coordination.

#### 4.7 Testing in Agile: continuous testing and the whole-team approach

In Agile, testing is not a phase; it is an **activity that happens throughout**, starting on day one.

- **Continuous testing** means running tests all the time, at every stage, so the team gets fast feedback on quality. Automated checks run whenever code changes (this practice connects to Continuous Integration, covered later in the program). A change that breaks something is noticed in minutes, not months.
- **The whole-team approach** means quality is everyone's responsibility, not only the testers'. Developers write unit tests, business people clarify acceptance criteria, testers help the team think about risks, and everyone shares the goal of a quality product. A tester is a quality coach and teammate, not a "gatekeeper" at the end.
- **Testing happens inside the cycle.** A feature is not "done" until it is tested. Test activities run in parallel with development (testers prepare tests while developers code, and test each small piece as soon as it is ready).
- **Early involvement ("shift left").** Testers join conversations about requirements, ask "what if" questions, and help define clear **acceptance criteria**: the conditions a feature must meet to be accepted as complete.
- **Regression testing is constant** and is largely automated.
- **Exploratory testing** (testing by simultaneously learning, designing, and executing without fully scripted steps) complements automation.

Compare with Waterfall: there, testers are a separate group at the end; in Agile, testers are embedded in the team throughout.

---

### 5. Scrum (overview)

#### 5.1 What is Scrum?

**Scrum** is the most widely used Agile **framework**. A framework is a light structure that gives teams a few rules and leaves the details to them. Scrum is described in the official **Scrum Guide**, written by Ken Schwaber and Jeff Sutherland, and describes Scrum as a lightweight framework that helps people, teams, and organizations generate value through adaptive solutions for complex problems. The name comes from rugby, where a team works together to move the ball forward.

Scrum is deliberately simple to understand but takes practice to do well. In this lesson we cover only the big picture. **Scrum roles and Scrum ceremonies each have their own lesson coming next, so here we only name them.**

#### 5.2 The three pillars of empiricism

Scrum is based on **empiricism**: knowledge comes from experience, and decisions are based on what is observed rather than guessed. Three pillars support it:

| Pillar | Meaning | Everyday example |
|---|---|---|
| **Transparency** | Important work and progress are visible to everyone who needs to see them, and described in a shared language. | A visible board showing exactly what is done and not done. |
| **Inspection** | Frequently and diligently check progress and the product to detect problems. | Looking at the working product at the end of each cycle. |
| **Adaptation** | If inspection shows something is off, adjust the process or the product as soon as possible. | Changing priorities after users react to the demo. |

Think of driving with a map app: you can see the route (transparency), you check where you are regularly (inspection), and you re-route when there is traffic (adaptation).

#### 5.3 The Sprint

The **Sprint** is the heartbeat of Scrum: a fixed-length time-box, typically one to four weeks (two weeks is very common), during which the team builds a usable, potentially releasable piece of the product. Key facts:

- Sprints run back-to-back with no gaps.
- The length stays the same, which gives the team a steady rhythm.
- A **Sprint Goal** (one clear objective) guides the sprint.
- Quality does not decrease during a sprint; scope may be clarified as more is learned.

```
Sprint 1 (2 weeks)      Sprint 2 (2 weeks)      Sprint 3 (2 weeks)
[Plan][Build/Test....][Review][Retro] [Plan][Build/Test....][Review][Retro] ...
   -> Increment 1          -> Increment 2          -> Increment 3
```

#### 5.4 The three artifacts

An **artifact** is something Scrum produces or uses to make work visible. Each has a commitment tied to it to increase transparency.

| Artifact | What it is | Commitment |
|---|---|---|
| **Product Backlog** | An ordered, ever-changing list of everything that might be needed in the product: features, fixes, improvements. The single source of work. | **Product Goal** (the long-term objective) |
| **Sprint Backlog** | The items chosen from the Product Backlog for this sprint plus the team's plan for delivering them. | **Sprint Goal** |
| **Increment** | A concrete, usable step toward the Product Goal; the sum of all completed backlog items so far. Each increment must meet the team's Definition of Done. | **Definition of Done** |

The **Definition of Done (DoD)** is a shared checklist stating what "finished" means (for example: code reviewed, automated tests passing, tested by a QE, no open critical defects). It is a quality tool: it prevents "done, except for testing." Notice that testing is built into the meaning of done.

#### 5.5 Just naming the rest

Scrum also has three accountabilities (roles: the Product Owner, the Scrum Master, and the Developers) and five events (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective, plus the Sprint itself). **These are covered in the next lessons ("Agile roles" and "Scrum ceremonies"), so you do not need to memorize them now.** One important point for testers: in Scrum, there is no separate "Tester" role in the official framework; testers are part of the Developers group, meaning all people who create the increment.

---

### 6. Kanban

#### 6.1 What is Kanban?

**Kanban** (Japanese for "signboard" or "visual card") began at Toyota in the 1940s-50s as a way to run manufacturing efficiently. Cards signaled when parts were needed, so factories produced only what was required. In software, it was adapted by David J. Anderson in the 2000s as a method to visualize work and improve flow. Unlike Scrum, Kanban has no required sprints, no required roles, and no mandatory meetings. You start with your current process and improve it gradually.

#### 6.2 Core principles and practices

Kanban's guiding ideas:

- **Start with what you do now.** No big-bang reorganization.
- **Agree to pursue incremental, evolutionary change.**
- **Respect current roles and responsibilities.**
- **Visualize the workflow.** Make all work visible.
- **Limit work in progress (WIP).** Do less at once to finish more.
- **Manage flow.** Watch how work moves and remove blockages.
- **Make policies explicit.** Everyone knows the rules (what "ready for test" means, for example).
- **Improve collaboratively and use feedback loops.**

#### 6.3 The Kanban board

A **Kanban board** is a visual display of work. Each work item is a **card**; each stage of the workflow is a **column**; cards move from left to right.

```
 BACKLOG   |  TO DO  | IN PROGRESS | IN TESTING | DONE
           |         |   (WIP 3)   |  (WIP 2)   |
 ----------+---------+-------------+------------+------
 [Wishlist]| [Search | [Cart       | [Login     | [Home
 [Reviews ]|  filter]|  discount]  |  page]     |  page]
 [Gift    ]| [Order  | [Checkout   | [Pay by    |
 [cards   ]|  email] |  fix]       |  card]     |
           |         | [Book page] |            |
```

Columns reflect your real process. A software team might have: Backlog, Ready, In Development, Code Review, In Testing, Ready for Release, Done. Notice that testing is a visible column, so a pile-up of cards in "In Testing" instantly reveals a testing bottleneck.

#### 6.4 WIP limits

A **WIP (Work In Progress) limit** is a maximum number of cards allowed in a column (or in the whole system) at once. If "In Testing" has a limit of 2 and already holds 2 cards, nobody can pull a third in until one moves on.

Why limit? Starting many things at once feels productive but is not. It causes context switching (mentally jumping between tasks), delays everything, hides problems, and creates unfinished "inventory." Analogy: a restaurant kitchen cooking 30 orders simultaneously produces 30 cold, late meals; cooking 5 at a time sends hot food out quickly. The motto is "**stop starting, start finishing.**"

WIP limits also expose bottlenecks. If developers finish code faster than testers can test it, the "In Testing" column fills up, hits its limit, and developers must help with testing or fix defects instead of starting new features. The whole team feels the problem and solves it, which fits the whole-team approach.

#### 6.5 Pull system and flow

Kanban is a **pull system**: a team member **pulls** a new card into their column only when they have capacity, rather than work being **pushed** onto them by a manager or the previous stage. This prevents overload.

**Flow** is how smoothly and quickly work items move through the board from start to finish. The goal is steady, predictable flow without long waiting times.

#### 6.6 Cycle time and lead time

Two key metrics:

- **Lead time:** the total time from when a request is made (the card is created or the customer asks) until it is delivered (Done). This is what the customer experiences.
- **Cycle time:** the time from when the team actually **starts working** on an item until it is finished. This is what the team controls.

Example: A customer requests "gift cards" on March 1. The card waits in the backlog until March 10, work starts March 10, and it is released March 15. Lead time = 14 days (March 1 to March 15). Cycle time = 5 days (March 10 to March 15).

Teams track these to see if flow improves and to forecast delivery ("most items take 3-6 days").

#### 6.7 When to use Kanban

- Work arrives unpredictably and priorities shift constantly (support teams, maintenance, operations, bug-fix streams).
- Items are small and similar in size.
- You want continuous delivery with no fixed iterations.
- A team wants to improve its existing process gradually.
- Many teams also use it alongside Scrum.

#### 6.8 Kanban vs. Scrum

| Aspect | Scrum | Kanban |
|---|---|---|
| Cadence | Fixed-length sprints (1-4 weeks) | Continuous flow, no sprints |
| Delivery | At the end of each sprint (an increment) | Whenever an item is ready |
| Roles | Defined (Product Owner, Scrum Master, Developers) | No prescribed roles |
| Meetings | Defined events (planning, daily, review, retrospective) | None required (teams add what helps) |
| Work limits | Limited by the sprint scope | Limited by WIP limits per column |
| Changes mid-cycle | Discouraged within a sprint, absorbed in the next planning | Allowed any time, provided WIP limits are respected |
| Key metrics | Velocity (work completed per sprint), burndown | Lead time, cycle time, throughput |
| Board | Reset every sprint | Persistent and continuous |
| Best for | Product development with planned increments | Continuous, unpredictable, or support-type work |

Neither is better; they answer different needs.

---

### 7. Hybrid approaches

Real organizations rarely follow a textbook. A **hybrid approach** blends elements from more than one model to fit real constraints.

#### 7.1 Waterfall + Agile mixes

Common patterns:

- **Waterfall up front, Agile for building:** requirements and budget are approved in a traditional phase, then development happens in sprints.
- **Agile software on top of Waterfall hardware:** a device's physical design is sequential, while its software is built in sprints.
- **Agile teams in a Waterfall organization:** teams run sprints, but contracts, budgeting, and release approvals still follow a traditional plan.

#### 7.2 Water-Scrum-Fall

**Water-Scrum-Fall** is a half-joking name for a very common reality: the project starts and ends in a Waterfall way, with Scrum in the middle.

```
 [Requirements & Approval]  -> [ Scrum sprints: Build & Test ] -> [Final Testing & Release]
      (Waterfall)                      (Agile)                       (Waterfall)
```

It is not "pure," and critics note that it keeps the late-testing and late-feedback problems at the end, but it is realistic where governance, budgets, and release processes cannot change overnight.

#### 7.3 Scrumban

**Scrumban** combines Scrum and Kanban. The team keeps Scrum's rhythm and some of its roles or meetings, and adds Kanban's visual board, WIP limits, and pull flow. Teams often adopt it when sprints feel too rigid (for example, a team that handles both new features and a constant stream of urgent bugs).

#### 7.4 Regulated industries

In healthcare, finance, aviation, and automotive, laws and standards require evidence: traceability from requirement to test, formal sign-offs, and documentation. These teams often use a V-Model or Waterfall for the overall safety-critical system, with Agile inside, such as short sprints that still produce the required documentation as part of "done." The lesson: Agile is possible in regulated settings, but the Definition of Done must include compliance activities.

#### 7.5 How to choose

There is no universal best. Choose by looking at your project's characteristics, as described in the decision guide below.

---

### 8. Side-by-side comparison of all approaches

| Dimension | Waterfall | V-Model | Agile (general) | Scrum | Kanban | Hybrid |
|---|---|---|---|---|---|---|
| Nature | Sequential process | Sequential with paired test levels | Values and principles | Time-boxed framework | Flow-based method | Mix of models |
| Structure | Phases, one pass | Phases in a V, one pass | Short iterations | Sprints (1-4 weeks) | Continuous board | Depends on mix |
| Requirements | Fixed up front | Fixed up front | Evolve continuously | Evolve via backlog | Evolve continuously | Partly fixed, partly evolving |
| Change handling | Difficult, formal change control | Difficult | Welcomed | Welcomed between sprints | Welcomed anytime | Varies |
| Customer involvement | At start and end | At start and end | Constant | Frequent (reviews, Product Owner) | As needed | Varies |
| First working software | Near the end | Near the end | Early | End of the first sprint | First item completed | Varies |
| Documentation | Heavy | Heavy | Just enough | Just enough | Light | Varies |
| Testing timing | After coding (late) | Planned early; run after each build phase | Continuous, in every cycle | Inside every sprint | Continuous, a board column | Mixed |
| Tester involvement | Late; separate team | Early planning, formal levels | Early and ongoing, embedded | Embedded in the team | Embedded; watches testing column | Varies |
| Predictability of scope | High (if stable) | High | Lower | Medium (per sprint) | Medium | Medium |
| Risk discovery | Late | Somewhat earlier | Early | Early | Early | Mixed |
| Best for | Stable, regulated, simple projects | Safety-critical, regulated systems | Changing, uncertain needs | Product work with planned increments | Support, maintenance, steady streams | Real-world constraints |
| Main weakness | Late feedback, rigid | Rigid, late working software | Less predictability, needs discipline | Can be misused as ritual | No inherent time-boxed focus | Can inherit weaknesses of both |

---

### 9. Decision guide: choosing a model

Ask these questions in order. The more "yes" answers in a column, the more it fits.

| Question | Leans Waterfall / V-Model | Leans Agile (Scrum) | Leans Kanban |
|---|---|---|---|
| Are requirements stable and well known? | Yes | No, they will evolve | Items are small and independent |
| How much will priorities change? | Rarely | Often between cycles | Constantly, even daily |
| Is heavy documentation or formal approval legally required? | Yes | Possible, but include it in Definition of Done | Rarely |
| Is the customer available to give frequent feedback? | Not available | Yes | Yes |
| Is the work building a new product in increments? | One big release | Yes | Not necessarily |
| Is the work continuous support or maintenance? | No | Sometimes | Yes |
| Is the contract fixed-scope, fixed-price? | Often fits | Needs flexible contracts | Flexible |
| Is the team experienced with Agile? | Not needed | Helpful | Easy to start |

Quick rules of thumb:

1. Stable, regulated, contract-driven: Waterfall or V-Model (perhaps with Agile inside).
2. Uncertain, fast-changing product with available stakeholders: Scrum.
3. Constant stream of varied requests: Kanban.
4. Sprints too rigid but you want structure: Scrumban.
5. Constraints from both sides: a deliberate hybrid, with the compromises written down.

---

### 10. One product, four models: the online bookstore

Let us plan the same product, "PageTurn Books," an online bookstore with features: browse, search, cart, checkout, order tracking, discount codes, reviews.

**Under Waterfall**
- Write all requirements first (about 2 months), then design, build everything, and test in a final phase. Release once, at month 9.
- The QE reviews requirements, writes a test plan, and executes a big test cycle after development.
- Risk: users see the product only at month 9; mistakes found late.

**Under the V-Model**
- Same sequence, but test planning is paired with each phase: acceptance tests are drafted from business requirements, system tests from system design, integration tests from architecture, and developers write unit tests from module design.
- The QE writes test designs early and checks that every requirement has a matching test.
- Risk: still no working software until late.

**Under Scrum**
- Build a Product Backlog of all features, ordered by value. Two-week sprints:
  - Sprint 1: browse and search books. Increment: users can find books.
  - Sprint 2: shopping cart. Sprint 3: checkout. Sprint 4: order tracking. Sprint 5: discount codes (added after feedback from the Sprint 3 review).
- A QE joins backlog conversations, helps define acceptance criteria, tests each story inside the sprint, and builds automated regression checks that grow every sprint.
- Benefit: working software after two weeks; discount codes discovered and added early.

**Under Kanban**
- After launch, the team handles a continuing stream: "fix the price rounding bug," "add Visa Debit," "update the home banner."
- Cards flow through Backlog, In Development, In Testing, Done, with WIP limits of 3 and 2. The QE watches the testing column; when it fills up, the team stops starting new items and helps finish tested ones.
- Benefit: urgent items can be pulled in quickly without waiting for a sprint boundary.

**Under a Hybrid (Water-Scrum-Fall)**
- The company's finance rules need an approved budget and a final security and compliance check. So: 6 weeks of upfront planning (Waterfall), 8 two-week sprints (Scrum), then a 3-week hardening and release phase (Waterfall).
- The QE tests continuously during sprints and runs the formal acceptance and compliance testing at the end.

---

### 11. Practical scenarios

**Scenario A: A hospital billing system.** Regulations demand traceable requirements and signed documents. Requirements are fixed by law. Suitable: V-Model, possibly with Agile sprints for internal screens, with compliance included in the Definition of Done.

**Scenario B: A start-up building a social-media app.** Nobody knows which features users will love. Competitors move fast. Suitable: Scrum with short sprints and frequent releases.

**Scenario C: An IT help-desk tool team.** Daily requests arrive unpredictably (small fixes, new reports, urgent outages). Suitable: Kanban with WIP limits and a fast lane for urgent items.

**Scenario D: A bank mobile app.** The business wants Agile speed, but security audits and release windows are strict. Suitable: Hybrid; Scrum for development, formal gates for security review and release.

**Scenario E: A small, one-off website for a local event with fixed content and a 3-week deadline.** Requirements are simple and stable. Suitable: simple Waterfall-style sequence, small enough that formal Agile overhead is not needed.

For each scenario, practice stating: the main reason for the choice, one risk, and what the QE does.

---

### 12. Where does the QE / tester fit in each model?

| Model | Tester's position and key activities |
|---|---|
| **Waterfall** | Often a separate team joining later. Best practice: review requirements and designs early (static testing), write the test plan during design, execute system testing after coding, report defects, and give a release recommendation. |
| **V-Model** | Plans tests in parallel with every development phase; designs acceptance, system, and integration tests early; ensures traceability from requirements to tests; coordinates the test levels. |
| **Agile (general)** | Embedded in the team from day one; asks questions about requirements, helps with acceptance criteria, tests each increment immediately, automates regression checks, and promotes quality across the team. |
| **Scrum** | Part of the Developers group; participates in all events; tests stories within the sprint; helps define the Definition of Done; keeps the increment releasable. |
| **Kanban** | Owns or shares the testing column; watches for bottlenecks; tests items as soon as they are pulled in; helps enforce WIP limits and policies such as "ready for test." |
| **Hybrid** | Adapts: continuous testing inside sprints, plus formal test phases (such as a compliance or acceptance test) at the edges. Must clearly understand which part of the process they are in. |

The universal lesson: in every model, the QE's mission is the same: help the team deliver the right product with the right quality. Only the timing and style of the work change.

---

### 13. Common misconceptions

1. **"Agile means no planning and no documentation."** False. Agile plans continuously in small steps and documents "just enough." The manifesto explicitly says the items on the right still have value.
2. **"Agile means faster, so testing can be skipped."** False. Frequent releases demand more testing discipline, including automation.
3. **"Waterfall is obsolete and always bad."** False. It remains a sound choice for stable, regulated, or small projects.
4. **"Scrum and Agile are the same thing."** False. Agile is the philosophy; Scrum is one framework that implements it.
5. **"There is no tester in Scrum, so testing is nobody's job."** False. Testing is everyone's job; testers are part of the Developers group and bring quality expertise.
6. **"Kanban has no rules."** False. It has clear principles, WIP limits, and explicit policies; it simply does not prescribe sprints or roles.
7. **"A sprint is a mini-Waterfall (design, then code, then test, each week)."** Often a warning sign. Within a sprint the team works on small slices together, testing continuously rather than handing work over in stages.
8. **"Hybrid means we couldn't decide."** False. A deliberate hybrid is a thoughtful response to real constraints, as long as the compromises are understood.
9. **"Our team uses stand-up meetings and boards, so we are Agile."** Rituals alone do not make a team Agile; the values (collaboration, working software, responding to change) matter.
10. **"One model fits every project forever."** False. Teams should reassess and adapt their model as the product and context change.

---

## Examples (quick recap)

- **Waterfall:** A company ordering a custom payroll system for a law that takes effect next year. Requirements are fixed by the law; the date cannot move.
- **V-Model:** Software for a car's braking controller, where each requirement must trace to a test.
- **Scrum:** A team building a new mobile game in two-week sprints, releasing playable builds and adjusting after player feedback.
- **Kanban:** A website operations team handling support tickets, with WIP limits and cards flowing through "New, Investigating, Fixing, Verifying, Closed."
- **Hybrid:** An insurance company running Scrum teams under a yearly budget approval and a final regulatory sign-off.

---

## Knowledge Check

1. **What is the main difference between Waterfall and Agile in how phases are arranged?**
   *Answer:* Waterfall completes each phase fully, once, in sequence. Agile repeats short cycles, each containing planning, building, and testing, delivering working increments frequently.

2. **What is the "late-testing problem" in Waterfall?**
   *Answer:* Testing begins only after coding, so defects (even ones introduced in requirements) are found late, when fixing them is costly, and the testing phase gets squeezed by earlier delays.

3. **In the V-Model, which test level pairs with module (detailed) design, and which with business requirements?**
   *Answer:* Unit testing pairs with module design; acceptance testing pairs with business requirements.

4. **State the four values of the Agile Manifesto.**
   *Answer:* Individuals and interactions over processes and tools; working software over comprehensive documentation; customer collaboration over contract negotiation; responding to change over following a plan.

5. **Does the Agile Manifesto say documentation and plans are worthless?**
   *Answer:* No. It says there is value in them, but the items on the left are valued more.

6. **What is the whole-team approach to quality?**
   *Answer:* Quality is the responsibility of everyone on the team (developers, testers, business people), not only the testers, and testing happens continuously through the cycle.

7. **Name the three pillars of Scrum's empiricism and give a one-line meaning of each.**
   *Answer:* Transparency (work is visible), inspection (frequently check progress and product), adaptation (adjust when something is off).

8. **Name the three Scrum artifacts and the commitment tied to each.**
   *Answer:* Product Backlog (Product Goal), Sprint Backlog (Sprint Goal), Increment (Definition of Done).

9. **What is a WIP limit and why does it help?**
   *Answer:* A cap on the number of items in a column or system at once. It reduces context switching, exposes bottlenecks, and encourages finishing work before starting new work.

10. **Item requested on 1 June, work started 8 June, finished 12 June. What are the lead time and cycle time?**
    *Answer:* Lead time = 11 days (1 June to 12 June); cycle time = 4 days (8 June to 12 June).

11. **Give two differences between Scrum and Kanban.**
    *Answer:* Scrum uses fixed-length sprints and defined roles/events; Kanban is continuous flow with WIP limits and no prescribed roles or meetings. (Also: Scrum measures velocity; Kanban measures lead/cycle time.)

12. **What is Water-Scrum-Fall?**
    *Answer:* A hybrid where requirements and approvals happen in a Waterfall manner, development occurs in Scrum sprints, and final testing and release are again Waterfall-style.

13. **A team gets a constant stream of unpredictable, small, urgent requests. Which model fits best and why?**
    *Answer:* Kanban, because it handles continuous flow and shifting priorities without waiting for sprint boundaries.

14. **Where in the Scrum Guide is there a separate "Tester" role?**
    *Answer:* Nowhere. Testers belong to the Developers group; testing is a shared responsibility.

---

## Try It: Choose and Justify a Model for Project 1

**Goal:** Practice selecting a delivery model and describing the quality engineer's role, using your **Project 1 - QE Foundations** sample web app.

**Time:** 30-40 minutes. **Deliverable:** one page, saved in your Project 1 folder as `delivery-model-decision.md` (you will refer back to it all week).

**Steps:**

1. **Describe the app.** In 3-5 sentences, write what the Project 1 web app does and who uses it. List five to eight main features (for example, registration, login, product search, cart, checkout).
2. **Answer the decision questions.** Using the decision guide in section 9, answer each question for your app (stable requirements? changing priorities? regulations? customer availability?). Write a one-line answer for each.
3. **Choose a model.** Pick one: Waterfall, V-Model, Scrum, Kanban, Scrumban, or a named Hybrid. Write at least three reasons based on your answers in step 2.
4. **Name the risks.** Write two risks of your chosen model for this app and one way you would reduce each (for example, "late feedback: demo every two weeks").
5. **Sketch the plan.** Depending on your choice, either:
   - draw an ASCII timeline showing phases or sprints and what feature arrives when; or
   - draw an ASCII Kanban board with your columns and WIP limits, placing at least six cards.
6. **Define the QE's role.** In a short table, list what *you* would do as the QE at the start, middle, and end of the project under your chosen model.
7. **Write a "what would change my mind" note.** Describe one change in circumstances (for example, "the company is audited by a regulator") that would make you choose a different model, and which one.

**Self-check:** Did you justify the choice with facts about the project rather than preference? Did testing appear early in your plan? Did you mention the Definition of Done or equivalent quality gate?

**Stretch (optional):** Write the same plan under a second model and list three differences in how your QE work would change.

---

## Key Takeaways

- A delivery model decides how SDLC phases are arranged: the phases are the same; their order, size, and overlap differ.
- **Waterfall** is sequential and document-driven. It is predictable for stable requirements but suffers from late feedback and the late-testing problem.
- The **V-Model** pairs every development phase with a test level (acceptance, system, integration, unit) so testing is planned early; it is still sequential.
- **Agile** is a set of values and principles (not a single process) that welcomes change, delivers working software often, and relies on collaboration. Its testing style is continuous and whole-team.
- **Scrum** is an Agile framework built on transparency, inspection, and adaptation, with time-boxed sprints and three artifacts: Product Backlog, Sprint Backlog, and Increment. Its roles and events are covered next.
- **Kanban** visualizes work on a board, limits WIP, uses a pull system, and measures lead time and cycle time. It suits continuous, unpredictable work.
- **Hybrid approaches** (Water-Scrum-Fall, Scrumban, Agile within regulated frameworks) are common and legitimate responses to real constraints.
- There is no single best model; choose based on requirement stability, change frequency, regulation, customer availability, and team context.
- In every model the QE's mission is the same, but in modern teams the QE is embedded, involved early, and focused on preventing defects as well as finding them.

---

## Additional Resources

- **Agile Manifesto and Principles:** https://agilemanifesto.org (the original four values, and the twelve principles at https://agilemanifesto.org/principles.html)
- **The Scrum Guide:** https://scrumguides.org (the official, short definition of Scrum by Ken Schwaber and Jeff Sutherland)
- **Atlassian Agile Coach:** https://www.atlassian.com/agile (beginner-friendly guides on Agile, Scrum, and Kanban, including boards and WIP limits)
