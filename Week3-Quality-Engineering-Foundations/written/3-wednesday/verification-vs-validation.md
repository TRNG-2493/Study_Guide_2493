# Verification vs. Validation

## Learning Objectives

By the end of this lesson, you will be able to:

- State the two classic questions that separate verification from validation, and explain each in plain language.
- Define verification and validation using ISTQB- and IEEE-style wording (paraphrased).
- Describe the main static verification activities: informal reviews, walkthroughs, technical reviews, inspections, static analysis (linting), checklists, and standards checks.
- Describe the main dynamic validation activities: executing the software through unit, integration, system, and acceptance testing, UAT, alpha and beta testing, and usability checks.
- Read and draw a V-Model diagram and pair each development phase with its verification and validation activity.
- Explain the relationship between static/dynamic testing and verification/validation, and why they are not the same classification.
- Explain the benefits of static testing, especially early defect detection and cost savings.
- Compare verification and validation across focus, timing, techniques, people, deliverables, and examples.
- Recognise a product that passes verification but fails validation, and the reverse.
- List verification and validation activities for the "User Registration and Login" feature of Project 1.
- Describe how V&V works in Agile teams (Definition of Done, demos, pull-request reviews, CI checks).
- Perform a mini document review and classify everyday QE activities as verification or validation.

---

## Why This Matters

Earlier today you learned about the testing mindset and the difference between Quality Assurance (QA) and Quality Control (QC). You saw that quality is not something added at the end, and that teams need both prevention and detection. This lesson gives you a sharper pair of tools to describe what a team is actually doing at any moment: **verification** and **validation**, often written together as **V&V**.

Why does a Test Automation Engineer need this?

1. **You will be asked "what kind of testing is this?"** In interviews, sprint planning, and test strategy documents, people expect you to know whether an activity checks "built right" or "right thing."
2. **It prevents expensive surprises.** Many of the costliest software failures are not bugs in the code. They are products that were built correctly but solved the wrong problem, or products that solved the right problem on paper but were built carelessly. V&V gives you vocabulary to catch both.
3. **It shows you where your automation fits.** Automated UI and API tests mostly perform validation. Linters, static analyzers, and code-quality gates in a CI pipeline perform verification. A strong AI-enabled test automation engineer knows both sides.
4. **It sets up the rest of the week.** Tomorrow's test design techniques and the next lessons on errors, defects, failures, and testing principles all assume you can say what you are checking and against what.

Think of this lesson as learning to ask two different questions of any piece of work. Good engineers ask both.

---

## The Concept

### 1. The Two Classic Questions

Every introduction to V&V starts with two sentences, usually credited to the software engineering pioneer Barry Boehm:

> **Verification:** "Are we building the product **right**?"
> **Validation:** "Are we building the **right** product?"

The words are almost identical, but the questions are very different.

**"Are we building the product right?"** asks whether the thing we are making matches what we *said* we would make. We wrote down requirements, designs, and standards. Does the work follow them? Is it consistent, complete, and free of mistakes compared to those documents? The reference point is the **specification**.

**"Are we building the right product?"** asks whether what we are making actually meets the *real need* of the people who will use it. Even if every document was followed perfectly, would the user be happy? Does it solve their problem? The reference point is the **user's needs and expectations**.

#### The house analogy

Imagine a family hires a builder to construct a house.

- The architect draws **blueprints**. An inspector visits during construction and checks: Are the walls where the blueprint says? Is the wiring to electrical code? Are the beams the specified thickness? That is **verification**. The inspector compares the house to the plan and the standards. The inspector does not ask whether the family will like living there.
- When the house is finished, the family moves in. They ask: Is the kitchen big enough for us? Does it suit our daily routine? Is it comfortable in winter? That is **validation**. They are judging the house against their own needs, not against the blueprint.

Notice that both can fail independently:

- A house can match the blueprint perfectly but have a tiny kitchen that the family hates. (Verified, not valid.)
- A house can be exactly what the family wanted, yet have cracked walls and leaking pipes because the builder was careless. (Valid idea, poor build; it would fail verification against the plan and standards.)

Software works the same way. Specifications are the blueprints. Users are the family.

#### A quick everyday version

You order a birthday cake. The baker has a recipe card and a checklist: correct flour weight, correct oven temperature, "Happy Birthday" spelled correctly in icing. Checking the cake against that list is verification. Cutting the cake at the party and finding out that the birthday person is allergic to almonds, or really wanted chocolate, not vanilla, is validation.

---

### 2. Definitions

Two widely used sources define these terms: the **ISTQB** (International Software Testing Qualifications Board) glossary and the **IEEE** (Institute of Electrical and Electronics Engineers) standards. Their exact wording changes between editions, so here are paraphrased versions that capture the shared idea.

| Term | Paraphrased definition | Reference point |
|---|---|---|
| **Verification** | Confirming, by examining and gathering objective evidence, that a work product (a requirement, a design, a piece of code) meets the specified requirements and standards set for it at that stage. | The specification, standards, and the output of the previous phase |
| **Validation** | Confirming, through evidence, that the finished or in-progress product satisfies the needs and intended use of its users and stakeholders in its real or simulated environment. | The user's and stakeholders' needs |

A few supporting terms you will see throughout this lesson:

- **Work product** (also called **artifact** or **deliverable**): anything produced during development, such as a requirements document, a design diagram, source code, a test plan, or a test case.
- **Specification**: a written description of what something should do or be. Requirements, designs, and API contracts are specifications.
- **Stakeholder**: any person or group with an interest in the product, including users, customers, business owners, developers, testers, and support staff.
- **Review**: a form of static testing in which people examine a work product to find problems.
- **Static testing**: testing in which the software is *not* run; work products are examined by people or tools.
- **Dynamic testing**: testing in which the software *is* run, with inputs supplied and outputs observed.
- **Standard**: an agreed set of rules, for example a coding standard ("variables use snake_case") or an industry standard (accessibility guidelines).

You will notice the definitions use the word "evidence." V&V is not opinion. A reviewer says "requirement R-12 contradicts R-15, see line 3." A test says "expected message X, actual message Y." Evidence is what makes V&V professional.

---

### 3. Verification in Depth: Static Activities

Verification is mostly done through **static** activities. That means the software is not executed. Instead, people or tools look at work products and compare them with what they should be.

Verification happens at **every phase**. It is not something you save for the end. At each stage, you ask: does this output correctly and completely follow from the previous stage and the standards?

- Requirements checked: are they clear, consistent, complete, testable?
- Design checked: does it implement all requirements, with nothing missing or extra?
- Code checked: does it follow the design and the coding standard?
- Test cases checked: do they cover the requirements?

#### 3.1 Reviews

A **review** is a static testing technique where one or more people examine a work product to find defects, improve understanding, or reach agreement. Reviews range from casual to highly formal. The four types you should know:

**1. Informal review**

- Casual, no strict process, no required documentation.
- Example: you ask a teammate, "Can you take a quick look at this test case before I commit it?"
- Typical output: verbal feedback or a few comments. Little or no record.
- Strength: fast and cheap. Weakness: results depend on who happens to look, and nothing is tracked.

**2. Walkthrough**

- The **author** leads the session, "walking" the group through the work product step by step.
- Purpose: share knowledge, collect feedback, help the group understand the work, and sometimes find defects.
- Example: a developer walks the team through a new login-page design before building it.
- Typical output: a list of questions, comments, and agreed changes.
- Preparation by attendees is often optional.

**3. Technical review**

- A group of technically qualified peers examines the work product, typically focused on technical correctness and suitability, and aims for consensus on whether it is fit for purpose.
- Usually led by a trained moderator or facilitator, not the author.
- Example: senior engineers review an architecture proposal for how the registration service stores passwords.
- Typical output: documented findings, decisions, and a conclusion (approve, approve with changes, or rework).

**4. Inspection**

- The most formal type. It follows a defined process with defined roles, entry and exit criteria, and recorded metrics.
- The main goal is **finding defects** and also improving the process that creates them.
- The process commonly includes: planning, overview/kick-off, individual preparation, the review meeting, rework, and follow-up.
- Typical output: a formal defect log, metrics (defects found per page, time spent), and a signed-off or re-inspected work product.

**Roles in a formal review**

Not every review uses every role, but inspections usually do:

| Role | What they do |
|---|---|
| **Author** | Creates the work product and fixes the defects found. |
| **Moderator / facilitator** | Plans the review, runs the meeting, keeps it focused and on time. |
| **Reviewer (inspector)** | Examines the work product beforehand and raises issues. Different reviewers may take different viewpoints (user, tester, developer). |
| **Scribe (recorder)** | Writes down defects, decisions, and actions during the meeting. |
| **Review leader / manager** | Decides that a review will happen and allocates people and time. |

**Comparison of review types**

| Aspect | Informal review | Walkthrough | Technical review | Inspection |
|---|---|---|---|---|
| Formality | Very low | Low to medium | Medium | High |
| Led by | Anyone | Author | Moderator | Trained moderator |
| Preparation | None | Optional | Expected | Required |
| Main goal | Quick feedback | Share knowledge, feedback | Technical consensus | Find defects, improve process |
| Documented output | Minimal | Notes | Findings and decision | Defect log and metrics |
| Example | "Look at this for me" | Design walkthrough | Architecture review | Formal requirements inspection |

A single project often uses several. For instance, you might informally review a test case, run a walkthrough of a design, hold a technical review of the architecture, and run a formal inspection on a safety-critical requirement.

#### 3.2 Requirement, design, and code reviews

The type of review is about *how* it is run. The subject is about *what* is reviewed.

- **Requirement review:** Checks requirements for being clear, unambiguous, complete, consistent, testable, and traceable. You practiced analyzing requirements on Tuesday; reviewing is the group version.
  - Example finding: "Requirement 4 says the password must be 'strong' but never defines strong."
- **Design review:** Checks that the design satisfies the requirements and is sound.
  - Example finding: "Requirement 7 (lock account after 5 failed logins) has no corresponding design element."
- **Code review:** Checks source code for logic errors, readability, security problems, and adherence to the coding standard.
  - Example finding: "This function builds a database query by joining strings with user input, which risks SQL injection."
- **Test case review:** Checks tests for coverage, correctness, and clarity. Yes, your own test cases get verified too.
  - Example finding: "Test case TC-09 expects the wrong error message compared to requirement R-3."

#### 3.3 Checking documents against standards

Organizations and industries have standards for documents and code: naming conventions, document templates, accessibility rules, security guidelines, and style guides. Checking a work product against them is verification.

Examples:

- Does the test plan include every section in the company template?
- Does the requirement document use the agreed ID format ("REQ-LOGIN-001")?
- Do the web pages follow the accessibility guidelines the company committed to?
- Does the API documentation follow the API style guide?

#### 3.4 Checklists

A **checklist** is a list of questions or items used to guide a review so that common problems are not forgotten. Checklists turn experience into a repeatable tool, which is especially helpful for beginners.

A short requirements-review checklist:

- Is each requirement stated clearly, with one meaning?
- Is each requirement testable (could I write a pass/fail test)?
- Are there any conflicting requirements?
- Are all terms defined (for example, "valid email," "strong password")?
- Are error and boundary situations covered?
- Does each requirement have a unique ID?
- Is there any requirement that looks like a design decision rather than a need?

A short code-review checklist:

- Does the code do what the requirement says?
- Are inputs validated?
- Are errors handled, and do error messages avoid leaking sensitive data?
- Are names clear and consistent with the standard?
- Is there duplicated code that should be shared?
- Are there unit tests for the new behavior?

#### 3.5 Static analysis

**Static analysis** is the use of tools to examine code or other work products without running them, to find defects or risky patterns. It is verification performed by machines, which means it can run on every commit, consistently, tirelessly.

Common forms:

- **Linters:** tools that flag stylistic problems, suspicious constructs, and likely bugs. Examples: Pylint and Flake8 (Python), ESLint (JavaScript), Checkstyle (Java).
- **Compilers and type checkers:** a compiler error such as "undefined variable" is static analysis. So is a type checker such as mypy (Python) or TypeScript's compiler.
- **Security scanners (SAST):** tools that look for patterns known to create vulnerabilities.
- **Complexity and duplication analyzers:** tools that measure how complicated or repetitive code is.
- **Document analyzers:** tools that check requirements for vague words ("fast," "user-friendly," "etc.").

**A small code example**

Here is a short Python function a trainee might write for Project 1's registration feature:

```python
import os

def validate_password(pwd):
    result = False
    if len(pwd) >= 8:
        if pwd != pwd.lower():
            return True
    else:
        return Fals
    return result

print(unused_variable)
```

Without running anything, a linter such as Pylint or Flake8 would report problems like these (the exact message wording differs by tool):

```
example.py:1:0: F401 'os' imported but unused
example.py:11:16: F821 undefined name 'Fals'
example.py:13:7: F821 undefined name 'unused_variable'
example.py:3:0: C0116 Missing function or method docstring
```

What happened here? The tool read the text and noticed:

1. An imported module that is never used (clutter, a maintainability issue).
2. A misspelled name, `Fals` instead of `False`, which would crash the program only when that line executes. A dynamic test might not reach that line for a while; the linter finds it instantly.
3. A name that was never defined anywhere.
4. A missing docstring, which breaks a documentation standard.

Nobody executed the function. No test data was needed. This is the central appeal of static analysis: it finds certain defects in seconds, before any test is even written. Notice also that it cannot tell you whether "at least 8 characters and one uppercase" is the *right password rule* for your users. That is a validation question.

---

### 4. Validation in Depth: Dynamic Activities

Validation is mostly done through **dynamic** activities. That means the software, or a working part of it, is **executed**. You supply inputs, observe outputs and behavior, and judge whether it meets the need.

Validation also happens throughout the lifecycle, but the work product being checked is a running piece of software (or a prototype) rather than a document.

#### 4.1 Test levels at overview

Dynamic testing is organised into **test levels**. You will study each in detail in later lessons; for now just recognise them.

| Level | What is tested | Typical tester | Main question |
|---|---|---|---|
| **Unit (component) testing** | The smallest pieces of code, such as a single function or class, in isolation | Developer | Does this piece behave as intended? |
| **Integration testing** | Interactions between components or systems, for example the registration form talking to the database | Developers and testers | Do the parts work together? |
| **System testing** | The complete, integrated system against the overall requirements | Test team | Does the whole system do what was specified end to end? |
| **Acceptance testing** | The system against business needs and user expectations, to decide whether to accept it | Customers, users, business representatives, with QE support | Is this ready and suitable for real use? |

#### 4.2 Acceptance testing and its forms

**Acceptance testing** is the level most closely tied to validation, since it asks "does it meet the need?" Its common forms:

- **User Acceptance Testing (UAT):** real users or their representatives run realistic scenarios to confirm the system supports their work. Example: a front-desk employee registers a new customer using the system exactly as in daily work.
- **Business acceptance testing:** checks that business rules and processes are supported.
- **Contractual and regulatory acceptance testing:** checks against contract terms or legal and regulatory rules.
- **Operational acceptance testing:** checks that backup, recovery, maintenance, and security procedures work.
- **Alpha testing:** performed at the developer's site (or in a simulated environment) by internal staff or selected users before release.
- **Beta testing:** performed at real users' sites, in real environments, by a selected group of external users before a general release. A "public beta" invites many users to try a near-final product and report problems.

#### 4.3 Usability checks against user needs

**Usability** is how easily and satisfactorily real users can accomplish their goals. A usability check puts the product, or a prototype, in front of representative users and watches them.

Example: you watch five new users try to register. Three of them do not notice the "Terms and Conditions" checkbox and keep seeing an error. The software does exactly what the specification says (the checkbox is required), yet users struggle. That is a validation finding: the product is not meeting the user's need to register smoothly.

Usability checks include:

- Moderated sessions, where an observer watches users complete tasks.
- Prototype feedback sessions, before any code exists.
- Surveys and satisfaction ratings.
- Accessibility checks with real assistive technologies.

#### 4.4 Validation can happen before the software is complete

Validation does not require finished software. Early on, teams validate with **prototypes**, **wireframes**, and **mockups**: simple drawings or clickable mock screens shown to users. "Does this registration flow make sense to you?" is already a validation question.

---

### 5. The V-Model Mapping

On Monday you saw the V-Model as one of the software development models. Now we can use it as the best picture of V&V. The left arm of the V represents development (specification and building); the right arm represents testing activities that check the matching work. The horizontal connections show which test level validates which development phase.

```
 Development / Specification                                  Testing / Validation

 +--------------------------+                          +--------------------------+
 |  Business / User         | <---------------------> |  Acceptance Testing      |
 |  Requirements            |   "Right product?"       |  (UAT, alpha, beta)      |
 +--------------------------+                          +--------------------------+
        \                                                        /
         \   +---------------------+          +-------------------+   /
          \  |  System Design      | <------> |  System Testing   |  /
           \ |  (functional spec)  |          |                   | /
            \+---------------------+          +-------------------+/
             \                                                    /
              \  +-----------------+      +---------------------+
               \ |  Architecture / | <--> |  Integration        |
                \|  High-level     |      |  Testing            |
                 +-----------------+      +---------------------+
                  \                                      /
                   \   +----------------+  +-----------+
                    \  |  Module Design | <|  Unit      |
                     \ |  (low-level)   |  |  Testing   |
                      \+----------------+  +-----------+
                       \                        /
                        \                      /
                         +--------------------+
                         |  Coding / Build    |
                         +--------------------+

   Going DOWN the left side: each phase is checked by VERIFICATION (static reviews,
   inspections, standards checks) before the next phase starts.
   Going UP the right side: running software is checked by VALIDATION (dynamic testing).
```

A simpler and clearer version of the same mapping:

```
 REQUIREMENTS ---------------------------------------------- ACCEPTANCE TESTING
      \                                                          /
       \  SYSTEM DESIGN ----------------------- SYSTEM TESTING  /
        \      \                                      /        /
         \      \ ARCHITECTURE ----- INTEGRATION TEST /       /
          \      \        \                /         /       /
           \      \        \ MODULE DESIGN - UNIT TEST     /
            \      \        \        |       |            /
             \      \        \       CODING               /
              \______\________\______|_______|____________/
               (Verification down the left)  (Validation up the right)
```

**Phase-to-activity pairing**

| Development phase | Verification activity (static, on the left) | Matching test level (on the right) | Validated against |
|---|---|---|---|
| Business / user requirements | Requirement review, inspection, checklist | **Acceptance testing** (UAT, alpha, beta) | User and business needs |
| System design (functional specification) | Design review against requirements | **System testing** | System requirements and functional specification |
| Architecture (high-level design) | Architecture review, technical review | **Integration testing** | Architecture and interface specifications |
| Module (low-level) design | Code-level design review, standards check | **Unit (component) testing** | Module design |
| Coding | Code review, static analysis, linting | (feeds unit tests) | Coding standards and module design |

Two important notes for beginners:

1. **The V-Model shows both V&V in one picture.** Many learners wrongly think the left side is "verification" and the right side is "validation" in a strict sense. The usual teaching view is simplified: reviews on the left verify each work product; tests on the right run the software against the corresponding level of specification or need. In reality, every test level also verifies something against its specification, and every level contributes evidence about whether the product is right for its purpose. Do not obsess over exact labels; understand the reasoning.
2. **The pairing implies early test planning.** Because "requirements <-> acceptance testing" are linked, you can start designing acceptance tests as soon as requirements exist, long before code is written. Doing so often reveals vague requirements. This is the V-Model's most useful lesson for testers: **test design starts on the left side of the V.**

---

### 6. Static Testing vs. Dynamic Testing, and How It Relates to V&V

This is the point that confuses many beginners, so take it slowly. There are **two different ways of classifying** testing activities:

- **Static vs. dynamic** is about *how* you examine something: without running code, or by running it.
- **Verification vs. validation** is about *what question* you are answering: built right (against specifications), or right product (against needs).

These two classifications overlap strongly, but they are not identical.

| | **Static** (no execution) | **Dynamic** (execution) |
|---|---|---|
| **Verification** ("built right?") | Reviews, inspections, linting, standards checks. This is the most common home of verification. | Running unit or system tests to check that the code matches the specification. Yes, this is verification, done dynamically. |
| **Validation** ("right product?") | Reviewing requirements with users, walking users through wireframes, reviewing a prototype on paper to see whether the need is understood. | UAT, beta testing, usability sessions with working software. This is the most common home of validation. |

So the picture is:

```
                     STATIC                         DYNAMIC
              (software not run)               (software is run)
            +-----------------------+-----------------------+
VERIFICATION|  Reviews, inspection, |  Unit/system tests    |
(vs. spec)  |  linting, checklists  |  checking spec        |
            +-----------------------+-----------------------+
VALIDATION  |  Prototype reviews,   |  UAT, beta, usability |
(vs. need)  |  requirements         |  testing with real    |
            |  sign-off with users  |  users                |
            +-----------------------+-----------------------+
```

The simple rule that works in most exams and interviews:

- **Verification is usually static. Validation is usually dynamic.**

But the more precise understanding is:

- **Static/dynamic describes the technique.** **Verification/validation describes the purpose.**
- A system test executed against a written functional specification is dynamic testing that verifies the build against the spec. The same system, put in front of real users to see whether it solves their problem, is dynamic testing that validates.

When you answer a certification question, give the textbook answer ("verification is static, validation is dynamic"). When you work in a real project, remember the nuance so that you do not misclassify an activity just because it runs code.

---

### 7. Benefits of Static Testing

Static testing, whether manual reviews or automated analysis, offers advantages that dynamic testing cannot match:

1. **Early defect detection.** You can review a requirement the day it is written. A defect found there never reaches the code. Dynamic testing must wait until there is something to run.
2. **Lower cost of fixing.** The classic observation, repeated across many studies, is that the later a defect is found, the more expensive it is to fix. Changing a sentence in a requirement document is cheap. Changing code that was designed, built, tested, and deployed to thousands of users is not.

Here is an illustrative (not exact) picture of relative cost:

```
Relative cost to fix a defect, by the stage where it is found

Requirements   |#                       1x
Design         |###                     3x
Coding         |#####                   5x
System test    |##########             10x
Acceptance     |###############        15x
Production     |##############################   30x to 100x
```

The exact numbers vary by project and study, but the shape is consistent: the cost climbs steeply.

3. **Finding defects dynamic tests miss.** Reviews can detect missing requirements, contradictions, and unclear wording, which no execution can reveal because the thing that is missing is not in the code.
4. **Finding defects that are hard to trigger.** A misspelled variable inside a rarely used error path may never execute during tests; a linter sees it anyway.
5. **Improving shared understanding.** Reviews spread knowledge and build common vocabulary across developers, testers, and business analysts.
6. **Better maintainability.** Standards and consistent style make code easier to read and change.
7. **Reducing later test effort.** Fewer defects at test time means fewer retests, fewer defect reports, and less rework.
8. **Training and process improvement.** Inspection metrics show which kinds of defects recur, so the team can improve how it works.

Static testing is not a replacement for dynamic testing. Static methods cannot show how a system behaves under load, how it looks in a real browser, or whether the pieces integrate in the real environment. The two complement each other.

---

### 8. Verification vs. Validation: Comparison Table

| Aspect | Verification | Validation |
|---|---|---|
| **Core question** | Are we building the product right? | Are we building the right product? |
| **Focus** | Conformance to specifications, standards, and previous-phase outputs | Fitness for the user's needs and intended use |
| **Checks against** | Requirements, designs, standards, checklists | User needs, business goals, real-world scenarios |
| **Timing** | Throughout development, starting with the earliest documents | Mainly when working software or prototypes exist; also early via prototypes |
| **Typical techniques** | Reviews (informal, walkthrough, technical, inspection), static analysis, checklists, standards audits | Dynamic testing (system, acceptance), UAT, alpha/beta, usability testing, demos |
| **Static or dynamic** | Mostly static | Mostly dynamic |
| **Who performs it** | Developers, testers, business analysts, architects, peers, QA specialists (everyone) | End users, customers, product owners, testers, business representatives |
| **Typical deliverables** | Review reports, inspection logs, static analysis reports, checklists completed, approved documents | Test results, UAT sign-off, beta feedback, usability findings, defect reports |
| **Finds what kinds of problems** | Ambiguity, inconsistency, missing items, standards violations, coding mistakes | Unmet needs, poor usability, wrong behavior in real context, missing features users expect |
| **Example** | A peer reviews the registration requirements and finds that the password rules conflict | A group of customers tries registration and finds the process confusing |
| **Relation to QA/QC** | Often seen as preventive (a QA-type activity) | Often seen as detective (a QC-type activity) |
| **Error it prevents** | Building the thing incorrectly | Building the wrong thing |

Remember: both are essential, and neither replaces the other.

---

## Examples

### Story 1: Passes verification, fails validation (built right, wrong product)

A bank's mobile team receives a requirement from a manager: "Add a transaction-history screen that displays the last 500 transactions in a table, sortable by any column."

The team does everything correctly:

- The requirement was reviewed and approved.
- The design matched the requirement.
- The code passed code review and static analysis with zero warnings.
- System tests confirmed 500 rows displayed, all columns sortable, every acceptance criterion in the specification met.

On paper, **verification is complete**. Every work product matches its specification.

Then real customers get the app. Usage data and feedback show that almost nobody opens the screen. Customers use their phones while shopping or commuting and want something different: a quick "what did I spend this week?" summary with search by merchant. A 500-row sortable table on a small screen is unwieldy. The manager had imagined a desktop analyst's tool; the customers needed a glanceable mobile summary.

**What went wrong?** The product was built *right* but was not the *right product*. Nobody validated the idea with actual users before building. A short prototype session with five customers would likely have exposed the mismatch for a tiny fraction of the cost.

**Lesson:** A perfectly coded feature that nobody needs is a failure of validation, no matter how clean the code is.

### Story 2: Valid need, poor build (right product, built wrong)

A small online shop owner asks developers for a discount-code feature, because customers frequently ask for coupons. The need is real and valuable. It would pass any validation discussion.

The feature is built quickly. When it is released:

- Applying a code sometimes charges the customer twice.
- The code field accepts spaces and then rejects valid codes.
- Codes that should expire after one use work repeatedly.
- The pages do not follow the shop's own design and accessibility standards.

No one reviewed the requirement for details like "one use per customer" or "expiry date." No code review caught the faulty total calculation. No static checks were configured. Customers want discount codes (valid idea), but this implementation fails to meet the specification and standards (poor verification).

**What went wrong?** The right product was built *wrong*. Early reviews and automated checks would have caught most of these problems.

**Lesson:** A good idea does not excuse a careless build. Verification is what ensures the idea is delivered correctly.

### Story 3: Both succeed

A team building an appointment-booking app interviews clinic receptionists, builds a clickable prototype, and watches them try it (validation, early). They write clear requirements, hold a requirement inspection and design review, run linting in CI, and have every pull request reviewed (verification). They then run system tests and finally let two clinics try the pilot (validation again). The app is both well built and well liked.

This is what a mature V&V approach looks like: **both questions asked repeatedly, from the first idea to the last release.**

---

### Worked Project 1 Example: "User Registration and Login"

Project 1 ("QE Foundations") has a "User Registration and Login" feature. Here is how verification and validation activities appear across the lifecycle. Use this as a model for your own thinking, because today's exercise writes test cases for this same feature.

**Sample requirements (simplified for illustration):**

- REQ-01: A visitor can register with an email address, a password, and a confirmation of the password.
- REQ-02: The email must be unique and in valid format.
- REQ-03: The password must be at least 8 characters and include at least one letter and one number.
- REQ-04: After successful registration, the user is told so and can log in.
- REQ-05: A registered user can log in with correct email and password.
- REQ-06: Invalid login attempts show an error message and do not reveal which field was wrong.

| Lifecycle phase | Verification activities (static, built right?) | Validation activities (dynamic or user-focused, right product?) |
|---|---|---|
| **Requirements** | Review REQ-01 to REQ-06 with a checklist for ambiguity, testability, and consistency. Inspect whether "valid format" is defined. Check that each requirement has a unique ID and acceptance criteria. | Interview or survey sample users: "Would you register with email? Do you expect social login?" Show a paper wireframe of the registration page to users and gather reactions. |
| **System design** | Review the design to confirm it covers every requirement (including REQ-06 error behavior). Check the design against security standards for password storage. | Show a clickable prototype of registration and login screens to real users and watch whether they complete the tasks. |
| **Architecture** | Technical review of how the registration service, database, and email-verification service connect. Review interface definitions between the front end and API. | Early proof-of-concept run with real data volumes to confirm the approach fits realistic usage. |
| **Module design / coding** | Pair review of the password-validation function. Pull-request review. Linting and static analysis (for example, flagging hard-coded secrets or unused variables). Check code against the team coding standard. | Developers run unit tests on the password validator: does it accept "abc12345" and reject "abc"? (Dynamic, checking the code against module design.) |
| **Integration** | Review API contracts and data mappings between registration form and database. | Integration tests: submit the registration form and confirm the user record appears in the database and a confirmation message returns. |
| **System testing** | Review the system test cases against requirements for coverage (traceability matrix check). Review test data and environment setup documents. | Execute end-to-end tests for registration and login, including negative cases: duplicate email, weak password, wrong password. Check browser and device behavior. |
| **Acceptance** | Verify that acceptance criteria and test documentation are complete and match approved requirements. | UAT with real customers or business representatives. Usability session: do users find the error messages clear? Beta release to a small group before general availability. |
| **After release** | Review incident reports for patterns; update checklists. | Monitor real usage: how many registrations are abandoned at the password step? Collect user feedback and support tickets. |

**Notice:** The test cases you write today are themselves work products. They will be verified (reviewed for coverage and correctness) and then executed (dynamic testing). Your positive and negative test cases will be most valuable if you write them carefully against requirements like REQ-03: it must accept a password with exactly 8 characters and one number, and reject 7 characters. That is the kind of specificity reviews help you reach.

---

## V&V in Agile Teams

Agile teams do not wait for a "verification phase" followed by a "validation phase." They build in short iterations (sprints) and do both **continuously**. You learned about Scrum ceremonies on Monday; here is how V&V appears in them.

**Continuous checking, not phases.** In each sprint, the team refines user stories, builds them, tests them, and demonstrates them. Verification and validation are interleaved from the first day of the sprint.

**Verification in Agile**

- **Backlog refinement and "three amigos" conversations:** a developer, a tester, and a product owner discuss a user story before development to ensure it is clear, testable, and complete. This is a lightweight requirement review.
- **Acceptance criteria review:** the team checks that each criterion is specific and measurable.
- **Pair programming and pair reviews:** two people work on, or look at, the same code, giving instant review.
- **Pull-request (PR) reviews:** before code merges into the main branch, teammates review the change. This is verification, performed by peers.
- **CI static checks:** the **Continuous Integration (CI)** pipeline automatically runs linters, formatters, type checkers, and security scanners on every commit. A failing check blocks the merge. This is automated verification.
- **Definition of Done (DoD):** a shared checklist that every user story must satisfy before it counts as complete. A DoD often includes verification items such as "code reviewed," "static analysis passes with no new warnings," and "unit tests written." It also includes validation items such as "acceptance criteria demonstrated to the Product Owner."

An example Definition of Done:

```
Definition of Done (sample)
[ ] Acceptance criteria met and demonstrated      (validation)
[ ] Code reviewed via pull request               (verification)
[ ] Linter and static analysis pass in CI        (verification)
[ ] Unit and integration tests pass in CI        (dynamic checks)
[ ] No open critical or high defects             (quality gate)
[ ] Documentation and test cases updated         (verification of artifacts)
[ ] Product Owner accepted the story             (validation)
```

**Validation in Agile**

- **Sprint review / demo:** at the end of the sprint, the team demonstrates working software to stakeholders. Their reactions ("this is not what we meant," or "great, but can we also...") are validation in action. A demo is the most direct validation moment in Scrum.
- **Product Owner acceptance:** the Product Owner, who represents the customer, accepts or rejects each story.
- **Early user feedback and beta programs:** frequent releases mean real users give feedback every few weeks.
- **Exploratory testing and usability sessions** during the sprint.
- **Retrospectives** (a verification-style look at the *process*): what built-in checks did we miss?

The short-feedback-loop nature of Agile reduces the risk in Story 1 above, because the "right product" question is asked every sprint rather than once at the end.

---

## Independent Verification and Validation (IV&V)

**Independent Verification and Validation (IV&V)** means that V&V is performed by an organization or team that is technically, managerially, and financially independent from the team building the product. The independence reduces the risk that builders miss their own blind spots, or that schedule pressure influences the findings.

- Typical in high-risk domains such as aerospace, medical devices, defense, nuclear, and some financial and government systems.
- The independent team reviews requirements and designs, performs its own analysis and testing, and reports directly to stakeholders rather than to the development manager.
- It is more expensive, so it is used when the cost of failure is very high.

For most commercial web projects, IV&V is not used formally, but the *principle* of independence appears in daily life: a tester reviewing a developer's work, or a developer reviewing a tester's automation script, adds a fresh perspective.

---

## How to Perform a Mini Document Review

You will often be asked to review a requirement, user story, or test case. Here is a repeatable, beginner-friendly approach.

**Steps**

1. **Understand the purpose and scope.** What is this document for? What is it supposed to describe? Who will use it?
2. **Gather the context and references.** Find the related documents (parent requirement, template, standard, glossary). Know what you are comparing against.
3. **Choose or create a checklist.** Use a short list such as: Clear? Complete? Consistent? Testable? Unambiguous? Traceable?
4. **Read the whole document once for understanding.** Do not log defects yet; simply understand.
5. **Read again, line by line, with the checklist.** Mark anything that is unclear, missing, contradictory, or untestable. Look for vague words ("fast," "user-friendly," "appropriate," "etc.," "as needed"), undefined terms, missing error cases, and implied assumptions.
6. **Ask "how would I test this?"** If you cannot write a clear pass/fail check, the requirement is probably vague.
7. **Record each finding** with the location, a short description of the problem, why it matters, and a suggested improvement. Be specific and neutral.
8. **Classify and prioritize** findings (for example: defect, question, suggestion; severity high, medium, low).
9. **Share findings respectfully.** Critique the document, not the person. Phrase observations as questions where possible: "What should happen if the email already exists?"
10. **Follow up.** Confirm that the author updated the document and that the fix actually resolves the finding.

### Sample Requirement Review Exercise

Here is a short requirement for a feature similar to Project 1. Review it using the steps above before reading the answer key.

> **REQ-X: Registration**
> 1. The registration page shall let users sign up quickly.
> 2. The user enters a username, an email, and a password. The password must be strong.
> 3. If the email is already in use, the system shall display an appropriate message.
> 4. After registering, the user shall be able to log in as soon as possible.
> 5. The system must be user-friendly and support all browsers.
> 6. Passwords must be at least 8 characters. Passwords must be at least 6 characters.
> 7. The system shall lock out users who try too many times.

Find as many problems as you can. Aim for at least eight. Then compare with the key.

**Answer Key (sample findings)**

| # | Location | Problem | Type | Suggested improvement |
|---|---|---|---|---|
| 1 | Item 1 | "quickly" is vague and not testable. | Ambiguity | Specify a measurable target, for example "registration completes within 3 seconds under normal load," or remove it. |
| 2 | Item 2 | "strong" password is undefined. | Ambiguity / missing detail | Define rules: minimum length, required character types. |
| 3 | Item 2 | Is the confirmation (re-enter password) field required? Not stated. | Missing requirement | State whether a confirm field exists and what happens on mismatch. |
| 4 | Item 2 | No rules for username or email format or length. | Missing detail | Define allowed characters, length limits, and valid email format. |
| 5 | Item 3 | "appropriate message" is vague; exact text or behavior is unspecified. | Ambiguity | Provide the message text or the guideline for it, and also consider security (do not reveal account existence if policy forbids). |
| 6 | Item 4 | "as soon as possible" is vague. Is email verification required first? | Ambiguity / missing detail | Specify whether login is immediate or after email confirmation, and any time limit. |
| 7 | Item 5 | "user-friendly" is subjective and untestable. | Untestable | Replace with measurable usability criteria or accessibility standard references. |
| 8 | Item 5 | "all browsers" is unrealistic and unbounded. | Unrealistic / ambiguous | List supported browsers and versions. |
| 9 | Items 6a and 6b | Contradiction: minimum of 8 and minimum of 6 characters. | Inconsistency | Decide the correct number; remove the other; check related requirements. |
| 10 | Item 7 | "too many times" is undefined; no lockout duration or unlock method. | Ambiguity / missing detail | Define the number of attempts, lockout duration, and recovery process. |
| 11 | Overall | No error handling for empty fields, invalid formats, or system errors. | Missing requirement | Add negative-case requirements. |
| 12 | Overall | No unique IDs per statement (requirements are numbered inside one block), so traceability is weak. | Traceability | Give each statement its own ID (REQ-X-01, REQ-X-02, ...). |

If you found eight or more, you are reviewing like a professional. Notice that every finding is made **without running anything**. This is static testing, and it just prevented defects from ever being coded.

---

## Classification Exercise: Verification or Validation?

Classify each activity as **V (Verification)** or **VAL (Validation)**. Think about whether the activity checks "built right against the spec/standards" or "right product for the user's need." Decide first, then check the key. Where an activity might be argued either way, the key explains the most common classification.

1. A peer inspects the requirements document for contradictions.
2. Real customers try the beta version of the app and submit feedback.
3. A linter runs on every commit and flags unused variables.
4. A business user performs UAT on the new invoicing screen using real invoices.
5. A developer walks the team through the database design to get feedback.
6. A usability session where new users attempt to register while an observer takes notes.
7. A tester checks that the test plan follows the company's template.
8. The Product Owner accepts a user story after the sprint demo.
9. A pull-request review of the login-validation code.
10. A team shows paper wireframes to potential users and asks if the flow makes sense.
11. A check that the API documentation matches the API style guide.
12. A reviewer verifies that every requirement has at least one test case in the traceability matrix.
13. Alpha testing of the product by internal staff acting as typical users before release.
14. A security scanner analyses the source code for known vulnerable patterns (without running the app).
15. A survey of users after release asks how well the product fits their daily tasks.
16. A technical review of the architecture by senior engineers to confirm it satisfies the design specification.
17. A senior tester reads another tester's test cases to confirm they match the requirements.
18. A pilot where one clinic uses the new system in real daily operations for two weeks.
19. A compiler stops the build because of a type mismatch.
20. A checklist-based review of the user stories at backlog refinement to confirm each has testable acceptance criteria.

**Answer Key**

| # | Answer | Explanation |
|---|---|---|
| 1 | V | Static review of a document for internal consistency. |
| 2 | VAL | Real users judge the product against their needs. |
| 3 | V | Automated static analysis against coding rules. |
| 4 | VAL | UAT checks suitability for real business use. |
| 5 | V | A walkthrough of a design; mainly sharing and checking the work product (it could also surface validation questions, but it is typically classed as verification). |
| 6 | VAL | Watching real users against their goals. |
| 7 | V | Checking a document against a standard template. |
| 8 | VAL | Acceptance by the Product Owner who represents the customer. |
| 9 | V | Peer review of code against requirements and standards. |
| 10 | VAL | Early validation of the idea with users, even though nothing runs. (This also shows that validation can be static.) |
| 11 | V | Conformance to a standard. |
| 12 | V | Checking completeness of coverage against requirements. |
| 13 | VAL | Alpha testing is acceptance-type testing with users before release. |
| 14 | V | Static analysis, software not run. |
| 15 | VAL | Measuring fitness for real use. |
| 16 | V | Review of design against specification. |
| 17 | V | Review of test cases against requirements. |
| 18 | VAL | Real-world operational use to confirm suitability. |
| 19 | V | Compiler type checking is static analysis against language rules. |
| 20 | V | Review of stories for quality (clarity, testability) against a checklist. |

Score yourself: 18 to 20 is excellent; 14 to 17 is solid; fewer than 14 means re-read sections 1, 3, and 4 and try again. Items 5 and 10 show that the boundary can be fuzzy; the key is to understand the reasoning.

---

## Common Misconceptions

**Misconception 1: "Verification is only done by testers."**
False. Verification involves *everyone*. Developers do code reviews and run linters. Business analysts review requirements. Architects review designs. Product owners review user stories. Testers contribute by reviewing requirements for testability and reviewing each other's test cases, but they are one group among many. Quality is a team responsibility, as you saw in the QA vs. QC discussion today.

**Misconception 2: "Validation is only UAT."**
False. UAT is one form of validation, and an important one, but validation happens throughout: prototype feedback, usability testing, demos, alpha and beta testing, early user interviews, and post-release monitoring. Waiting until UAT to ask "is this the right product?" is exactly how Story 1 happened.

**Misconception 3: "Verification means no running code; validation means running code, always."**
Partly true but too simple. Verification is *usually* static and validation *usually* dynamic, yet running a system test against a specification is dynamic verification, and showing a paper prototype to users is static validation. See Section 6.

**Misconception 4: "If it passes all the tests, it is valid."**
Not necessarily. Tests are written from specifications, so they check conformance. If the specification itself is wrong or incomplete, passing tests still produce an unsatisfactory product.

**Misconception 5: "Reviews are a waste of time compared to testing."**
Reviews find different kinds of defects and find them earlier and more cheaply. They complement rather than compete with dynamic testing.

**Misconception 6: "Verification and validation are the same as QA and QC."**
They overlap in spirit, since verification is often preventive and validation often detective, but they are different concepts. QA/QC is about process-oriented versus product-oriented quality activities; V&V is about checking against specifications versus checking against needs.

**Misconception 7: "A linter passing means the code is correct."**
No. Static analysis can find certain classes of problems. It cannot know whether the logic satisfies the business need.

---

## Pointers to What Comes Next

This lesson stayed on the "what are we checking and against what" level. Later lessons go deeper:

- **Test levels** (unit, integration, system, acceptance) will each get their own detailed treatment later in the course.
- **Errors, defects, and failures** (what exactly do we find when V&V succeeds, and how are these terms different?) is the next lesson.
- **Testing principles** (such as "testing shows the presence of defects, not their absence" and "early testing saves time and money") follow after that. You already felt the second one in this lesson.
- **Test design techniques** (equivalence partitioning, boundary value analysis, and more) are covered tomorrow. They will help you design the dynamic tests that validate features such as registration and login.

---

## Try It: Hands-On Activity

Work individually, then compare with a partner. Allow about 30 to 40 minutes.

**Part A: Mini review of a Project 1 requirement (15 minutes)**

1. Open the Project 1 documentation or the requirement for "User Registration and Login" provided by your instructor.
2. Using the ten-step mini review process in this lesson, review the requirement. Use this checklist: Clear? Complete? Consistent? Testable? Traceable?
3. Record at least **six findings** in a table with these columns: ID, location, problem, type (ambiguity, missing, contradiction, untestable), and suggested fix.
4. Swap tables with a partner. Does your partner see anything you missed? Add those findings, with credit.

**Part B: Sort your own activities (10 minutes)**

1. List **eight** activities you could perform on the Project 1 login feature this week (for example, "reviewing the requirement," "running the registration form with an existing email," "asking a classmate to try logging in and watching what they do," "running a linter on the validation function").
2. Mark each as Verification or Validation, and as Static or Dynamic. Place each in the two-by-two grid from Section 6.
3. Pick one activity from each quadrant and write one sentence on what evidence it would produce.

**Part C: Link to today's exercise (10 minutes)**

1. Take two requirements from your review (for example, REQ-03 on password rules).
2. Draft one positive and one negative test case for each. Include preconditions, steps, test data, and expected results.
3. Ask yourself: "Is this test checking that the build matches the spec (verification), or that the user need is met (validation)?" Most system-level tests do some of both. Write down your answer and your reasoning.

**Reflection questions**

- Which problems did your review find that no test could have found?
- Which question was harder for you to answer: "built right?" or "right product?" Why?
- If you could add one automated static check to the Project 1 pipeline, what would it be?

---

## Knowledge Check

Answer first, then compare with the answers below.

1. In one sentence each, what question does verification answer, and what question does validation answer?
2. A team reviews a requirements document for contradictions and unclear wording. Is this verification or validation, and is it static or dynamic?
3. Name the four review types from least formal to most formal.
4. Which review type is led by the author and mainly aims at sharing knowledge and gathering feedback?
5. Which role in a formal review records defects and decisions?
6. In the V-Model, which test level is paired with the business/user requirements phase?
7. In the V-Model, which test level is paired with module (low-level) design?
8. Give two benefits of static testing.
9. A product passes all its tests against the written specification, but users do not like it. Which activity was weak: verification or validation? Explain.
10. True or false: validation is only done during UAT.
11. True or false: only testers perform verification.
12. Give one example of an automated verification activity and one of a validation activity in an Agile team.
13. What is the purpose of a Definition of Done in terms of V&V?
14. What does IV&V stand for, and why would a project use it?
15. A linter reports that a variable is never used. Does this tell you whether the product meets user needs? Why or why not?
16. Is running a system test against a written functional specification a verification or a validation activity? Explain the nuance.

**Answers**

1. Verification: "Are we building the product right?" (does it conform to specifications and standards). Validation: "Are we building the right product?" (does it meet user needs).
2. Verification, static. The software is not run; a document is examined against quality criteria.
3. Informal review, walkthrough, technical review, inspection.
4. The walkthrough.
5. The scribe (recorder).
6. Acceptance testing.
7. Unit (component) testing.
8. Any two of: early defect detection, lower cost of fixing defects, finding defects dynamic tests miss (such as missing requirements), improved shared understanding, better maintainability, reduced later testing effort, process improvement.
9. Validation was weak. The product met the specification (verification looks fine) but did not satisfy real users, which means the right product was not built or the specification itself did not capture the need.
10. False. Validation also includes prototype feedback, usability testing, demos, alpha/beta testing, and post-release monitoring.
11. False. Developers, business analysts, architects, product owners, and peers all perform verification; testers participate but are not the only ones.
12. Automated verification: a CI pipeline running a linter or static analyser on each commit. Validation: the sprint demo where the Product Owner and stakeholders give feedback on working software (or UAT or beta feedback).
13. The Definition of Done is a shared checklist that makes sure both kinds of checks (for example, code review and linting for verification; Product Owner acceptance for validation) happen before a story counts as finished.
14. Independent Verification and Validation. A separate team, independent from the developers, performs V&V to reduce bias and risk, used in high-risk domains such as aerospace or medical devices.
15. No. A linter checks code against technical rules (verification). It cannot judge whether the feature solves the user's problem (validation).
16. It is dynamic testing that checks the build against the specification, so it is verification in purpose. If the same system is placed in front of users to see whether it meets their needs, it becomes validation. This shows that static/dynamic and V/V are different classifications.

---

## Key Takeaways

- **Verification asks "Are we building the product right?"** It checks work products against specifications and standards. **Validation asks "Are we building the right product?"** It checks the product against real user and business needs.
- Think of the **house analogy**: the inspector checking the blueprint is verification; the family living in the house is validation.
- **Verification is mostly static** (reviews, inspections, walkthroughs, linting, checklists, standards checks). **Validation is mostly dynamic** (running software in acceptance testing, UAT, alpha/beta, usability testing). The precise truth is that static/dynamic describes *technique*, while V/V describes *purpose*.
- The four review types, from informal to formal, are **informal review, walkthrough, technical review, and inspection**. Formal reviews use roles such as author, moderator, reviewers, and scribe.
- The **V-Model** pairs requirements with acceptance testing, system design with system testing, architecture with integration testing, and module design with unit testing. Test design can start on the left side of the V, as soon as requirements exist.
- **Static testing finds defects early and cheaply.** The later a defect is found, the more it costs to fix.
- A product can **pass verification and fail validation** (a perfect feature nobody needs) or **be valid and fail verification** (a wanted feature that is poorly built). You need both.
- **In Agile**, V&V is continuous: three amigos conversations, pull-request reviews, CI static checks, Definition of Done, sprint demos, and Product Owner acceptance.
- **IV&V** adds independence for high-risk systems.
- **Everyone** verifies, and validation is **more than UAT**.
- A good reviewer asks of every requirement: "Is it clear, complete, consistent, and testable?"

---

## Additional Resources

- ISTQB Glossary, authoritative definitions of verification, validation, static testing, review, inspection, and walkthrough: https://glossary.istqb.org/
- Guru99, "Verification vs Validation in Software Testing" (beginner-friendly comparison with examples): https://www.guru99.com/verification-v-s-validation-in-software-testing.html
- Atlassian Continuous Delivery, software testing overview (how testing and quality checks fit into modern pipelines): https://www.atlassian.com/continuous-delivery/software-testing
- Pylint documentation, a real Python static analysis tool you can try on your own code: https://pylint.readthedocs.io/
