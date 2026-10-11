# Requirements Analysis: Reviewing What Will Be Built Before It Is Built

**Week 3 - Quality Engineering Foundations | Tuesday: Test Management and Defect Lifecycle**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define what a requirement is and explain why a tester cares about it before any code exists.
2. Identify the common sources of requirements (stakeholders, BRD, SRS, user stories, use cases, prototypes, existing systems, regulations).
3. Distinguish business, user, and system requirements; functional and non-functional requirements; constraints; and assumptions.
4. Evaluate a requirement against eight quality characteristics: clear, unambiguous, complete, consistent, testable, feasible, traceable, and prioritized.
5. Explain what requirement testing (static review) is and describe reviews, walkthroughs, and inspections at an introductory level.
6. Spot ambiguity, gaps, contradictions, and untestable words such as "fast", "user-friendly", and "etc." in a requirement document.
7. Write good clarifying questions and maintain a question log.
8. Write and assess acceptance criteria and perform a basic testability analysis.
9. Evaluate user stories using the INVEST checklist and prioritize requirements using MoSCoW.
10. Derive testable conditions from a requirement.
11. Build a Requirement Traceability Matrix (RTM) and explain how it supports coverage and change impact analysis.
12. Describe how requirement changes are managed and how they affect testing.
13. State the entry criteria, exit criteria, and deliverables of the requirements analysis phase.
14. Apply all of the above to a "User Registration and Login" requirement document for Project 1.

---

## Why This Matters

### In the industry

Studies of software projects, reported repeatedly over several decades, show that a large share of defects originate in the requirements stage, not in coding. A requirement that is vague, missing, or contradictory does not fix itself. It travels forward: the designer interprets it one way, the developer another, and the tester a third. The mistake is only discovered when the software is nearly finished, and by then fixing it is far more expensive than correcting a sentence in a document.

A widely accepted rule of thumb in quality engineering is that **the later a defect is found, the more it costs to fix**. A confusing sentence caught during a review costs a few minutes of conversation. The same confusion, found after release, can cost rework, retesting, patches, lost customers, and sometimes legal exposure.

Think of an architect reviewing a blueprint before the builders arrive. If the architect notices that the blueprint shows a staircase but no room for it, the fix is an eraser. If the same problem is discovered after the walls are built, the fix is a demolition crew. A tester who reads requirements carefully plays the architect's reviewer role: finding the missing staircase while it is still a drawing.

This is why modern teams practice **shift-left testing**: moving quality activities earlier (to the "left") on the project timeline. Requirements analysis is the leftmost testing activity there is, and it needs no code, no test environment, and no automation framework. It needs a careful reader who asks good questions.

### In this week's Weekly Epic

This week you are building the quality-engineering mindset. On Monday you learned the SDLC phases, Agile and Scrum, the six STLC phases (where "requirement analysis" was introduced at overview level), and the basics of Jira. Today we open up that first STLC phase and work through it in depth. Everything you do for the rest of the week depends on it:

- Wednesday's defect discussions and testing principles will refer to requirements as the "expected behavior" against which defects are judged.
- Thursday's test design techniques need clear, testable requirements as raw material. You cannot design good tests from a vague sentence.
- Friday's non-functional testing builds on the introduction to non-functional requirements you receive today.

For **Project 1 - QE Foundations**, a sample web app you are planning quality for, you will analyze the "User Registration and Login" requirements today and produce the first real quality-planning artifacts: a requirement review report, a question log, and a draft RTM.

---

## The Concept

### 1. What Is a Requirement?

A **requirement** is a statement describing something a system must do, or a quality it must have, or a limit it must respect, in order to satisfy a stakeholder's need or a rule of the business.

A **stakeholder** is anyone with an interest in the product: customers, end users, business owners, developers, testers, support staff, regulators, and so on.

Requirements answer the question, "What should this product do, and how well should it do it?" They deliberately avoid answering "How will we build it?", which belongs to design.

| Statement | Requirement or design decision? |
|---|---|
| "Users must be able to reset a forgotten password." | Requirement (what) |
| "The reset feature will use a JWT stored in Redis." | Design decision (how) |
| "A user account is locked for 15 minutes after 5 failed login attempts." | Requirement |
| "The lockout counter is a column in the Users table." | Design decision |

**Why a tester cares.** A requirement is the tester's primary **test basis**: the body of knowledge from which tests are derived. It is also the main **test oracle**: the source we consult to decide whether the observed behavior is correct. If the requirement says nothing, or says something ambiguous, there is no reliable way to say whether the software passed or failed.

**The tester's perspective versus the analyst's perspective.** A business analyst asks, "Did we capture what the business needs?" A tester asks an overlapping but different question: "Can I tell, objectively, whether this has been done correctly?" Both questions matter, and a good tester asks both.

---

### 2. Sources of Requirements

Requirements do not fall from the sky. They come from a variety of sources, and each source has its own strengths and weaknesses. A tester should know where a requirement came from so they know whom to ask when something is unclear.

| Source | What it is | Typical strengths | Typical weaknesses |
|---|---|---|---|
| **Stakeholders** | Conversations, interviews, workshops with people who care about the product | Rich in context and real needs | Opinions conflict; people forget to mention obvious things |
| **BRD (Business Requirements Document)** | A document describing business goals, the problem being solved, and high-level business needs | Explains the "why"; good for scope | Too high-level to test directly |
| **SRS (Software Requirements Specification)** | A detailed document describing what the software will do, including functional and non-functional requirements | Detailed and structured; a strong test basis | Can become outdated; long and hard to read |
| **User stories** | Short statements from the user's point of view, common in Agile ("As a ... I want ... so that ...") | Easy to read; focused on value | Brief by design; details live in acceptance criteria and conversations |
| **Use cases** | Step-by-step descriptions of how an actor (user or system) interacts with the system to reach a goal, including alternate and exception flows | Show flows and alternatives clearly | Take time to write; can miss non-functional needs |
| **Prototypes and wireframes** | Sketches or clickable mock-ups of screens | Make ideas visible; reveal missing fields and flows | Show the "what it looks like", rarely the rules behind it |
| **Existing system** | The current product, when a new version or replacement is being built | Shows real behavior | May contain old defects that should not be copied; undocumented rules |
| **Regulations and standards** | Laws or industry rules (data privacy rules, accessibility standards, payment security standards) | Mandatory and often precise | Written in legal language; easy to misread |

Two important points for testers:

- **Requirements can be implicit.** Nobody writes "the Submit button must work", yet everybody expects it. Part of analysis is surfacing these unwritten expectations.
- **Sources can disagree.** The wireframe may show a "Date of Birth" field that the SRS never mentions. Whenever sources conflict, record it and ask. Do not silently choose one.

---

### 3. Types of Requirements

Requirements are classified in several overlapping ways. Do not worry about memorizing a single "correct" taxonomy; focus on understanding why each classification helps.

#### 3.1 Business, user, and system requirements

These describe requirements at three levels of detail, moving from "why" to "what the software does".

| Level | Describes | Example (Project 1) |
|---|---|---|
| **Business requirement** | A high-level goal of the organization | "We want to grow our registered customer base by 20 percent this year." |
| **User (stakeholder) requirement** | What a user group needs to accomplish | "A visitor can create an account to access personalized features." |
| **System (solution) requirement** | What the software must do in specific, detailed terms | "The system shall require a password of at least 8 characters containing at least one letter and one digit." |

Notice how each level feeds the next: the business goal motivates user needs, which are refined into precise system behavior. Testers mostly work with system requirements, but they use the higher levels to understand intent.

#### 3.2 Functional versus non-functional requirements (introduction)

- A **functional requirement** describes *what* the system does: a behavior, feature, or function. Example: "The system shall send a verification email after registration."
- A **non-functional requirement (NFR)** describes *how well* the system does it, or the qualities it must have. Typical categories are performance, security, usability, reliability, compatibility, accessibility, and maintainability. Example: "The login page shall respond within 2 seconds for 95 percent of requests under a load of 500 concurrent users."

NFRs are often forgotten, or written in untestable form ("the system should be fast"). Today we only learn to recognize them and to flag when they are missing or vague. **Friday's lesson is the deep dive** into non-functional testing.

| Requirement | Functional or NFR? |
|---|---|
| "A user can log out from any page." | Functional |
| "Passwords must be stored in a hashed, non-reversible form." | Non-functional (security) |
| "The registration form must be usable on screens from 360 px to 1920 px wide." | Non-functional (compatibility/usability) |
| "An administrator can deactivate a user account." | Functional |

#### 3.3 Constraints

A **constraint** is a restriction on how the solution may be designed or delivered. It is not a feature; it is a boundary. Examples:

- "The system must run on the company's existing cloud provider."
- "The release must be live by 30 November."
- "The budget for third-party services is capped at a fixed amount."
- "The product must comply with the data privacy law of the markets it serves."

Constraints matter to testers because they limit the test environment, the schedule, the tools, and sometimes the data we are allowed to use.

#### 3.4 Assumptions

An **assumption** is something the team believes to be true but has not confirmed. Examples:

- "Users have a working email address."
- "The email provider will deliver messages within one minute."
- "Users will register from a modern browser released within the last two years."

Assumptions are dangerous because they are invisible risks. If an assumption turns out to be false, requirements and tests built on it collapse. A good tester **writes assumptions down** and asks whether they are confirmed. In your question log, an assumption often becomes a question: "Can we confirm that every user is expected to have an email address?"

---

### 4. Characteristics of a Good Requirement

How do we judge whether a requirement is ready to be built and tested? Quality-engineering practice (and standards such as those on requirements engineering) describe a set of characteristics. We use eight, which you can remember by reading them as a checklist.

#### 4.1 Clear

A clear requirement can be understood the first time by its intended readers, using plain words and short sentences, without needing decoding.

- **Bad:** "The system shall facilitate the provisioning of end-user credentials leveraging an established authentication paradigm."
- **Good:** "The system shall let a visitor create an account using an email address and a password."

#### 4.2 Unambiguous

An unambiguous requirement has exactly one reasonable interpretation. Ambiguity is the enemy of testing because two people can read the same sentence and build or test two different things.

- **Bad:** "Old accounts will be deleted automatically." (How old? Deleted or deactivated? Is the user warned?)
- **Good:** "Accounts with no login for 24 consecutive months shall be deactivated, and the owner shall receive an email warning 30 days before deactivation."

#### 4.3 Complete

A complete requirement contains all the information needed to build and test it: inputs, conditions, outputs, error behavior, and limits.

- **Bad:** "The user can register with an email and password." (What are the password rules? What if the email already exists? What happens after success?)
- **Good:** "A visitor can register by supplying a unique email address and a password that meets the password policy (REQ-PW-01). On success the system creates an unverified account and sends a verification email. If the email already exists, the system shows the message 'An account with this email already exists.'"

#### 4.4 Consistent

A consistent requirement does not contradict other requirements, other documents, or itself.

- **Bad:** Section 3.1 says "Passwords must be at least 8 characters." Section 5.4 says "Passwords of 6 or more characters are accepted."
- **Good:** One password policy stated once (for example, REQ-PW-01), and referenced everywhere else.

#### 4.5 Testable

A testable requirement can be verified by a test with a definite pass or fail result. If you cannot imagine how you would prove it was met, it is not testable.

- **Bad:** "The login page must be user-friendly."
- **Good:** "A first-time user shall be able to complete login in no more than 3 user actions (enter email, enter password, click 'Log in')."

Be careful with the "good" example: even this one deserves discussion with the team, because "user-friendly" is a quality that we have chosen to *measure* in a specific way. Turning vague qualities into measurable statements is one of your most valuable skills.

#### 4.6 Feasible

A feasible requirement can actually be implemented within the project's technology, budget, schedule, and legal limits.

- **Bad:** "The system shall detect and block every possible fraudulent registration with 100 percent accuracy."
- **Good:** "The system shall limit registrations to 5 per IP address per hour and shall present a CAPTCHA after 3 failed attempts."

Testers are not the only judges of feasibility (developers and architects are), but a tester who notices "100 percent" or "never" or "always" should raise a flag.

#### 4.7 Traceable

A traceable requirement has a unique identifier and can be linked backward to its source (who asked for it, and why) and forward to its design, code, and tests. Without an ID, you cannot say which tests cover which requirement.

- **Bad:** A paragraph of prose with no numbering: "The system will handle login stuff in a secure way."
- **Good:** "REQ-LOGIN-03: The system shall lock an account for 15 minutes after 5 consecutive failed login attempts. Source: Security policy SP-12."

#### 4.8 Prioritized

A prioritized requirement states how important it is relative to others, so the team knows what to build first, what to test first, and what can be dropped if time runs short.

- **Bad:** A list of 40 requirements, all marked "high".
- **Good:** Each requirement carries a priority (for example Must, Should, Could, Won't), agreed with the business owner.

#### 4.9 Summary table

| Characteristic | The question to ask | Warning signs |
|---|---|---|
| Clear | Can I understand it on first read? | Jargon, long sentences, passive voice |
| Unambiguous | Is there only one possible meaning? | "appropriate", "as needed", "etc.", "and/or" |
| Complete | Do I know inputs, outputs, errors, and limits? | No error handling; "TBD"; missing numbers |
| Consistent | Does it agree with everything else? | Two values for the same rule |
| Testable | Can I define a pass/fail check? | "fast", "easy", "robust", "user-friendly" |
| Feasible | Can it really be built, within constraints? | "always", "never", "100 percent", "instantly" |
| Traceable | Does it have an ID and a known source? | No numbering; unknown origin |
| Prioritized | Do I know how important it is? | Everything is "high" or nothing is ranked |

---

### 5. Requirement Testing: Static Review

**Testing does not require running software.** Testing a requirement document is called **static testing**: examining work products (documents, designs, code) without executing them. Running the software, by contrast, is **dynamic testing**. Static testing of requirements is sometimes called **requirement testing** or **requirement review**.

Why do it? Because finding a problem in a requirement is the cheapest possible point to fix it. Static review also trains the whole team toward a shared understanding.

There are several review approaches, ranging from informal to formal. At introductory level, know these three.

| Review type | How it works | Formality | Typical purpose |
|---|---|---|---|
| **Informal review** (including "buddy check" or "desk check") | One colleague reads the document and gives comments; no fixed process | Low | Quick feedback |
| **Walkthrough** | The **author** leads the team through the document, explains it, and collects questions and feedback | Low to medium | Share understanding; gather feedback; educate |
| **Inspection** | A formal, rule-based process with defined roles (moderator, author, reviewer, scribe), preparation time, checklists, and recorded defects with measured results | High | Find as many defects as possible; improve the process |

Note that there is also a **technical review** (experts discuss a document and decide on technical matters) which sits between these in formality; you will meet it in more detail in the ISTQB syllabus.

**A tester's practical review process:**

1. **Read once for understanding.** Do not criticize yet. Understand the goal.
2. **Read again with the eight characteristics as a checklist.** Mark every sentence that is unclear, ambiguous, incomplete, contradictory, or untestable.
3. **Compare sources.** Check the wireframe against the SRS against the user story.
4. **Write questions.** For every issue, write a specific question (see section 7).
5. **Raise them in a review meeting or on the ticket.** Record answers.
6. **Update the requirements** (the business analyst or product owner does this, not the tester) and confirm the changes.

Reviews are about the *document*, not the *person*. Use phrases like "I could not find what should happen when..." rather than "You forgot...". Being a collaborative, curious reviewer wins you allies, which you will need for the rest of the project.

---

### 6. Finding Problems: Ambiguity, Gaps, Contradictions, and Untestable Words

Learn to recognize four families of requirement problems.

#### 6.1 Ambiguity

A sentence is ambiguous when it can be read in more than one way.

| Problem | Example | Why it is a problem |
|---|---|---|
| Vague quantity | "The system should handle a large number of users." | How large? 100? 1,000,000? |
| Vague time | "Emails are sent quickly." | Seconds? Minutes? Hours? |
| Unclear reference | "When the user submits it, it is stored." | What does "it" refer to? |
| Unclear scope | "All users can edit their profile." | All users including admins? Guests? |
| Ambiguous conjunction | "Users must provide a phone number and/or email." | Which combinations are valid? |
| Unclear negation | "Not all fields are mandatory." | Which ones are mandatory? |

#### 6.2 Gaps (missing information)

A gap is something that should be said but is not. Common gaps:

- **Missing error handling:** what happens on invalid input, a timeout, or a service outage.
- **Missing boundaries:** minimum and maximum lengths, ranges, limits.
- **Missing roles:** what each role (guest, registered user, administrator) can or cannot do.
- **Missing states:** what happens when an account is locked, unverified, or deactivated.
- **Missing messages:** the exact wording or at least the intent of user-facing messages.
- **Missing non-functional needs:** performance, security, accessibility, browsers supported.
- **Missing data rules:** which fields are optional, what formats are accepted.

A useful technique is to read each requirement and ask "what if...?" questions: *What if the user does nothing? What if they do it twice? What if the network drops? What if they are not allowed?*

#### 6.3 Contradictions

Two statements conflict. Contradictions can be hidden far apart in the same document, or between documents (the SRS says one thing, the wireframe shows another).

Example: "Section 2: Users log in with their username." and "Section 6: Users log in with their email address."

#### 6.4 Untestable words (the "red flag" list)

Some words and phrases are warning signs because they cannot be measured. When you see them, ask for a measurable alternative.

| Red-flag word or phrase | Why it is untestable | Ask |
|---|---|---|
| fast, quick, rapid, responsive | No number | "How many seconds, under what load?" |
| user-friendly, intuitive, easy, simple | Subjective | "How will we measure ease? Number of steps? Task completion rate?" |
| etc., and so on, such as | The list is open-ended | "Please list every item that must be supported." |
| appropriate, adequate, suitable, reasonable | Opinion-based | "What are the exact criteria?" |
| flexible, robust, scalable, secure (alone) | Too broad | "What specific threats, limits, or growth targets?" |
| as needed, if necessary, when possible | Undefined condition | "Under what exact conditions?" |
| should (in some documents) | Unclear if mandatory | "Is this a must or a nice-to-have?" |
| always, never, all, every, 100 percent | Often infeasible or unproven | "Is there really no exception?" |
| minimal, maximum (without value) | No value | "What is the number?" |
| TBD, to be decided | Missing | "When will it be decided and by whom?" |

A note on "shall", "should", and "may": many organizations use **"shall"** for mandatory requirements, **"should"** for recommended, and **"may"** for optional. If a document uses them inconsistently, ask what the team's convention is.

---

### 7. Asking Clarifying Questions and Keeping a Question Log

Finding an issue is only half the job. The other half is getting it resolved, and that depends on asking well.

#### 7.1 How to write a good clarifying question

A good question is **specific, answerable, neutral, and tied to a requirement**. It also explains *why* the answer matters, so the person understands the urgency.

| Weak question | Strong question |
|---|---|
| "Is the password thing okay?" | "REQ-PW-01 requires 8 or more characters. Is there a maximum length? If so, what is it, and what message should users see when it is exceeded?" |
| "What about errors?" | "What should the user see if the verification email cannot be sent at registration time? Should the account still be created?" |
| "Why is this written so badly?" | "The phrase 'the system should respond quickly' appears in 3.2. What response time (in seconds) and under what load should we treat as acceptable?" |

Guidelines:

1. **Be specific.** Quote the requirement ID and sentence.
2. **Ask one thing per question** where possible.
3. **Offer options** when you can: "Should it be A or B?" is easier to answer than "What should it be?"
4. **State the impact.** "Without this, we cannot define a pass/fail check for the lockout rule."
5. **Direct it to the right person** (product owner, business analyst, architect, or compliance specialist).
6. **Be polite and curious**, not accusatory.

#### 7.2 The question log

A **question log** (also called a clarification log or query log) is a simple table that tracks every question from the moment it is asked until it is answered and incorporated. It protects the team from forgotten questions and "I thought we agreed" arguments.

| ID | Req ID | Question | Raised by | Date raised | Directed to | Status | Answer | Date answered | Requirement updated? |
|---|---|---|---|---|---|---|---|---|---|
| Q-001 | REQ-PW-01 | What is the maximum password length? | Tester A | 06 Oct | Product Owner | Answered | 64 characters | 07 Oct | Yes (v1.2) |
| Q-002 | REQ-REG-04 | Should the account be created if the verification email fails to send? | Tester A | 06 Oct | Business Analyst | Open | - | - | No |
| Q-003 | REQ-LOGIN-03 | Does the lockout reset after a successful login? | Tester B | 06 Oct | Product Owner | Escalated | - | - | No |

Typical statuses are **Open**, **Answered**, **Escalated** (when the person cannot decide), and **Closed** (answer applied to the requirement). Keep it visible, for example as a shared spreadsheet or as Jira issues linked to the story.

---

### 8. Acceptance Criteria and Testability Analysis

#### 8.1 What are acceptance criteria?

**Acceptance criteria** are the specific conditions a feature must satisfy to be accepted by the product owner or customer. They turn a general requirement or user story into something verifiable: a checklist of "this is done when...".

A popular way to write them is the **Given / When / Then** format (also called Gherkin style):

- **Given** a starting context
- **When** an action occurs
- **Then** an expected outcome results

Example for a login story:

> **Given** a registered, verified user with a correct email and password,
> **When** the user submits the login form,
> **Then** the user is taken to the dashboard and sees their name in the header.

Acceptance criteria can also be written as a simple bulleted checklist, which is just as valid. What matters is that each criterion is specific and checkable.

**Acceptance criteria are not test cases.** They define what "done" means from the business view. Test cases (designed later, with the techniques you will learn on Thursday) are the detailed steps and data used to check them. However, good acceptance criteria give you a very strong starting point.

#### 8.2 Testability analysis

**Testability** is the degree to which a requirement (or the software) allows us to establish test conditions and run tests to determine whether they are met. When you review a requirement, ask these testability questions.

| Question | Why it matters |
|---|---|
| Is the expected result observable? | We must be able to see an outcome (a message, a state change, a record, a log entry). |
| Is it measurable? | We need a number, a list, or a clear yes/no. |
| Can I control the inputs? | If the behavior depends on something I cannot set (such as time, or an external service), I may need a stub, a test hook, or a special environment. |
| Is the needed data available or creatable? | Some tests need accounts in particular states (locked, unverified, expired). |
| Is the needed environment available? | Email delivery, third-party services, and certain devices must be accessible. |
| Is the behavior deterministic? | If the answer changes randomly, tests become unreliable. |
| Can the whole requirement be verified, or only part of it? | Some parts may need a different method (inspection, analysis, demonstration). |

Record the answers as **testability notes**. For example: "REQ-LOGIN-03 (lockout for 15 minutes) is hard to test in real time. We will request a configurable lockout duration in the test environment, or a way to move the system clock."

This kind of note, written early, saves days later, because the team can build the needed hooks during development rather than discovering the problem at test time.

---

### 9. User Stories and the INVEST Checklist

A **user story** is a short, plain-language description of a feature from the perspective of the person who wants it. The usual template is:

> **As a** [type of user], **I want** [a goal], **so that** [a benefit].

Example: "As a visitor, I want to register with my email address, so that I can save my preferences."

A user story is often called "a promise for a conversation". It is intentionally short; the details come from discussion and are captured in acceptance criteria. In Jira (which you met on Monday), stories are typically issues of type "Story" in the backlog, with acceptance criteria in the description.

#### The INVEST checklist

**INVEST** is a well-known mnemonic for judging whether a user story is well formed.

| Letter | Meaning | Question to ask | Example of failure |
|---|---|---|---|
| **I** - Independent | The story can be developed and delivered without depending too heavily on others | Can this be built in any order? | "Login cannot be started until the Admin Dashboard story is done." |
| **N** - Negotiable | Details are open to discussion; it is not a rigid contract | Is the "how" left to conversation? | A story that dictates the database table design |
| **V** - Valuable | It delivers value to a user or the business | Why do we need it? Is there a "so that"? | "As a developer, I want to rename the tables." (no user value stated) |
| **E** - Estimable | The team can estimate its size | Do we understand it well enough? | "As a user, I want the system to be great." |
| **S** - Small | Small enough to complete within one sprint | Can it fit in a sprint? | "As a user, I want a complete account management system." |
| **T** - Testable | It has clear criteria to confirm completion | Can I write acceptance criteria? | "As a user, I want the app to feel modern." |

A story that fails INVEST is a signal to refine it, usually by splitting it into smaller stories or sharpening the acceptance criteria. As a tester, you are especially responsible for the **T** in INVEST, but you can speak up on all six letters.

**Refinement example.**

- Original: "As a user, I want an account system."
- Problems: not small, not estimable, not testable.
- Split into: (1) register with email and password, (2) verify email, (3) log in, (4) log out, (5) reset forgotten password, (6) lock account after repeated failures. Each now has its own acceptance criteria.

---

### 10. Requirement Prioritization with MoSCoW

Not everything can be built or tested first. **Prioritization** orders requirements by importance. One very common technique is **MoSCoW**, where the lowercase letters "o" are only there to make the word pronounceable.

| Category | Meaning | Test implications | Example (Project 1) |
|---|---|---|---|
| **M**ust have | Without it, the release has no value or is illegal or unsafe | Test first and most thoroughly; blocks release if failing | Register with valid email and password; log in with correct credentials |
| **S**hould have | Important, but a workaround exists; painful to omit | Test thoroughly after the Musts | Password reset by email |
| **C**ould have | Nice to have; included if time and budget allow | Test lightly or last | "Remember me" checkbox |
| **W**on't have (this time) | Agreed to be out of scope for this release | Do not plan tests; record the decision | Login with social media accounts (planned for a later release) |

Why testers should care:

- **Test effort is limited.** Priority tells us where to spend it. A Must requirement deserves deeper coverage than a Could.
- **Risk follows priority** (partly). The impact of a failure in a Must requirement is high. In later lessons you will connect this to risk-based testing.
- **When the schedule shrinks**, testers help the team decide what to cut by showing the risk of each choice.

Priority is decided by the **business** (typically the product owner), not by the tester. Your role is to ask, "What priority does each requirement have?" and to point out when everything is marked as Must, which defeats the purpose.

---

### 11. Defining Testable Conditions from Requirements

A **test condition** is an item or event of a component or system that could be verified by one or more test cases. In plain words: a specific thing worth checking. Test conditions are the bridge between requirements and test cases.

At the requirements analysis stage, you do not write detailed test cases yet. You **identify what needs to be tested**, the "to-do list of checks", which later will be turned into cases. (How to design the best set of inputs for these checks is Thursday's topic: test design techniques.)

**Method:**

1. Take one requirement.
2. Break it into its separate rules (every "if", "must", "only", "unless", "after" is a rule).
3. For each rule, write at least one condition covering the success path, and conditions for each failure or exception path.
4. Note any condition you cannot formulate (because of a gap), and turn it into a question.

**Example.**

Requirement REQ-LOGIN-03: "The system shall lock an account for 15 minutes after 5 consecutive failed login attempts."

| Condition ID | Test condition |
|---|---|
| TC-LOGIN-03-a | Account is not locked after fewer than 5 consecutive failures |
| TC-LOGIN-03-b | Account becomes locked on the 5th consecutive failure |
| TC-LOGIN-03-c | A locked account rejects login even with the correct password |
| TC-LOGIN-03-d | The user sees a message that explains the lockout |
| TC-LOGIN-03-e | The account can be used again after the 15 minutes have passed |
| TC-LOGIN-03-f | (Question needed) Does a successful login before 5 failures reset the counter? |

Notice that the last condition exposes a gap: the requirement did not say whether the counter resets. Writing conditions is itself a powerful review technique, because every time you cannot write a clean condition, you have found a weakness in the requirement.

---

### 12. The Requirement Traceability Matrix (RTM)

#### 12.1 What it is

A **Requirement Traceability Matrix (RTM)** is a table that links each requirement to the other artifacts that implement or verify it, most importantly **test conditions and test cases**, and later **defects**. *Traceability* means the ability to follow a requirement forward (to tests and results) and backward (to its source).

Think of it as an index at the back of a book, or a map between "what was promised" and "how we know it was delivered".

#### 12.2 What it is used for

| Use | Explanation |
|---|---|
| **Coverage check** | Quickly spot requirements with no tests (a coverage gap), and tests that do not map to any requirement (possibly unnecessary or revealing a missing requirement). |
| **Impact analysis** | When a requirement changes, see exactly which tests must be updated or rerun. |
| **Progress reporting** | Show how many requirements have tests designed, executed, and passed. |
| **Audit and compliance** | In regulated industries, show evidence that every requirement was verified. |
| **Defect linking** | See which requirements are affected by open defects. |

#### 12.3 Directions of traceability

- **Forward traceability:** from requirement to tests (are all requirements covered?).
- **Backward traceability:** from tests (or design) back to requirements (does every test have a purpose?).
- **Bidirectional traceability:** both directions maintained together. This is the usual goal.

#### 12.4 A full RTM example

The table below shows part of an RTM for Project 1's registration and login area. Columns are filled gradually as the project progresses. At the end of requirements analysis, you typically have the first columns plus planned test conditions; the execution and defect columns are filled in later.

| Req ID | Requirement summary | Source | Priority | Type | Test condition IDs | Test case IDs (planned) | Execution status | Defect IDs | Coverage status |
|---|---|---|---|---|---|---|---|---|---|
| REQ-REG-01 | Visitor can register with unique email and compliant password | US-101 | Must | Functional | TC-REG-01-a to -d | TBD (Thursday) | Not run | - | Covered (conditions defined) |
| REQ-REG-02 | Email format is validated; error message shown if invalid | US-101 | Must | Functional | TC-REG-02-a to -c | TBD | Not run | - | Covered |
| REQ-REG-03 | Verification email sent after registration | US-102 | Must | Functional | TC-REG-03-a to -e | TBD | Not run | - | Covered |
| REQ-REG-04 | Behavior when verification email fails to send | US-102 | Should | Functional | None (question Q-002 open) | - | - | - | **Gap: blocked by open question** |
| REQ-PW-01 | Password policy: 8 to 64 chars, at least 1 letter and 1 digit | SP-05 | Must | Functional / security | TC-PW-01-a to -f | TBD | Not run | - | Covered |
| REQ-LOGIN-01 | Verified user can log in with email and password | US-103 | Must | Functional | TC-LOGIN-01-a to -d | TBD | Not run | - | Covered |
| REQ-LOGIN-02 | Generic error message for wrong email or password | US-103 | Must | Functional / security | TC-LOGIN-02-a to -c | TBD | Not run | - | Covered |
| REQ-LOGIN-03 | Account lock for 15 minutes after 5 failed attempts | SP-12 | Should | Functional / security | TC-LOGIN-03-a to -f | TBD | Not run | - | Partially covered (counter reset question) |
| REQ-LOGIN-04 | Login response time within 2 seconds for 95 percent of requests | NFR-02 | Should | Non-functional (performance) | TC-LOGIN-04-a | TBD (Friday) | Not run | - | Covered (needs load tool) |
| REQ-LOGIN-05 | "Remember me" keeps the user signed in for 14 days | US-104 | Could | Functional | TC-LOGIN-05-a to -c | TBD | Not run | - | Covered |

**How to read it:**

- A row with "None" or "Gap" in coverage tells us where the requirements are not yet testable.
- If REQ-LOGIN-03 changes (say, to 30 minutes), we scan the "Req ID" column and immediately see which conditions and test cases to update.
- Over the life of the project, the "Execution status" and "Defect IDs" columns become the dashboard for coverage.

#### 12.5 Practical tips

- Use stable IDs. Never reuse an ID for a different requirement.
- Keep the RTM in a spreadsheet at first; later tools (Jira with linked issues, or test management tools) can maintain links automatically.
- Update it every time a requirement, test, or defect changes. A stale RTM is worse than none, because people trust it.
- Do not over-engineer it: a simple, accurate matrix beats a perfect one nobody maintains.

---

### 13. Requirements Change Management and Its Impact on Testing

**Requirements change.** Markets shift, the customer learns something, a law is passed, a technical limit appears. In Agile, change is expected and welcomed; in Waterfall, it is formally controlled; either way, it must be managed.

**Change management** is the process of capturing, evaluating, approving, implementing, and communicating changes to requirements in a controlled way.

A typical flow:

1. **Request** the change (someone raises it, ideally as a ticket).
2. **Analyze impact** on scope, schedule, cost, design, existing code, and tests.
3. **Decide** (approve, reject, or defer), usually by the product owner or a change control board.
4. **Implement** the change in the requirement and, later, in the product.
5. **Communicate** to everyone affected, including testers.
6. **Update** the requirement version, the RTM, and test artifacts.

**Impact of a change on testing:**

| Area | Typical effect |
|---|---|
| **Test conditions and cases** | Some must be modified, added, or retired |
| **Test data and environment** | New data states or configuration may be needed |
| **Regression testing** | Previously passing features may break; we must retest related areas |
| **Estimates and schedule** | More or less effort is required |
| **Automation** | Scripts may need maintenance |
| **Risk** | New or changed features carry new risk; late changes carry more |

**Tester's duties during change:**

- Participate in the **impact analysis**, using the RTM to answer "what is affected?".
- Ask for **versioning** of requirement documents, so everyone knows which version a test was written against.
- Insist that changes are **written down**, not just spoken in a hallway.
- Update the **question log** and **RTM**.
- Raise the **risk** of late changes honestly, without blame.

**Example.** The product owner decides that passwords must now be at least 10 characters. Using the RTM, the tester sees that REQ-PW-01 is linked to TC-PW-01-a to -f and that REQ-REG-01 uses the same rule. Those conditions are updated, test data (previously 8-character passwords) is replaced, and any automated scripts using old passwords are scheduled for correction. A regression check of login for existing users is added, because their old 8-character passwords may now be a special case. This question, "what happens to existing users?", is an important gap exposed by the change.

---

### 14. Entry and Exit Criteria for the Requirements Analysis Phase

In the STLC, each phase has **entry criteria** (conditions that must be met to start) and **exit criteria** (conditions that must be met to declare the phase complete). They prevent starting too early or stopping too early.

| | Entry criteria | Exit criteria |
|---|---|---|
| **Typical items** | Requirements documents (BRD, SRS, user stories, wireframes) are available in a baseline version | All requirements have been reviewed |
| | Access to stakeholders (product owner, BA) is arranged | All significant issues are logged in the question log |
| | Review team and schedule identified | Critical and high-priority questions are answered (or escalated with a plan) |
| | Basic project context known (scope, timeline, release goals) | Clarified requirements are agreed and versioned |
| | Tools in place (Jira, shared spreadsheet, document access) | Testability notes recorded |
| | Acceptance criteria drafts available for in-scope stories | Draft RTM created with unique IDs for all in-scope requirements |
| | | Requirement review report shared and accepted |

**Example judgment.** If 12 of 40 requirements still have open Must-level questions, the exit criteria are not met. The team may agree to proceed with the clarified requirements while continuing to resolve the rest, but that decision should be **conscious and recorded**, along with the risk. In Agile teams, the same ideas appear as the **Definition of Ready** for a story (it is clear and small enough to start) and the **Definition of Done**.

---

### 15. Deliverables of the Requirements Analysis Phase

At the end, you hand over tangible work products. These are your evidence and the inputs to test planning and test design.

| Deliverable | Description | Typical contents |
|---|---|---|
| **Requirement review report** | A summary of the review's findings | Documents reviewed and versions; the list of issues by type and severity; counts; overall assessment; recommendations; risks |
| **Clarified (updated) requirements** | The corrected versions of the requirements after answers are applied | New version numbers, rewritten statements, acceptance criteria |
| **Question log** | The tracked list of questions and answers | See section 7.2 |
| **RTM draft** | The first version of the traceability matrix | Req ID, source, priority, test conditions, coverage status |
| **Testability notes** | Observations about what is hard to test and what is needed | Data, environment, tool, and hook needs; automation candidates |
| **Early inputs to the test plan** | Scope, risks, and assumptions discovered | Items in and out of scope; identified product risks |

---

## Worked Example: Reviewing the Project 1 "User Registration and Login" Requirement Document

We now apply everything to a realistic document. Read it first as a tester would.

### The document (version 0.3, draft)

> **Project 1 - QE Foundations: User Registration and Login Requirements**
>
> **1. Introduction**
> The application will allow users to register and log in to access the system quickly and easily.
>
> **2. Registration**
> 2.1 A user can register by providing their name, email, and a password.
> 2.2 The password must be strong.
> 2.3 The system should validate the email address.
> 2.4 After registration, the user is sent a confirmation email.
> 2.5 The registration page should be user-friendly and load fast.
>
> **3. Login**
> 3.1 Users log in with their username and password.
> 3.2 If the login fails, an appropriate error is shown.
> 3.3 After too many failed attempts, the account will be locked.
> 3.4 Users can choose to stay logged in.
>
> **4. Password**
> 4.1 Passwords must be at least 6 characters.
> 4.2 Users can reset their password if they forget it.
>
> **5. General**
> 5.1 The system must be secure, scalable, and support all popular browsers, devices, etc.
> 5.2 All users can update their profile.

### Step 1: Issues found

| # | Ref | Issue | Type | Characteristic violated | Severity |
|---|---|---|---|---|---|
| 1 | 1 | "quickly and easily" is not measurable | Untestable word | Testable | Medium |
| 2 | 2.1 | Name rules missing (length, allowed characters, optional or mandatory); email uniqueness not stated; behavior on duplicate email missing | Gap | Complete | High |
| 3 | 2.2 | "Strong" is undefined | Ambiguity | Unambiguous, Testable | High |
| 4 | 2.3 | "Validate" is unclear (format only? existence?); "should" is ambiguous in priority; no error message | Ambiguity / Gap | Unambiguous, Complete | Medium |
| 5 | 2.4 | Email content, timing, and sender unspecified; failure behavior missing; is verification required before login? ("confirmation" versus "verification" not distinguished) | Gap | Complete, Clear | High |
| 6 | 2.5 | "user-friendly" and "fast" are untestable | Untestable words | Testable | Medium |
| 7 | 3.1 vs 2.1 | Login uses "username", but registration collects name and email; no username field exists | Contradiction | Consistent | High |
| 8 | 3.2 | "appropriate error" undefined; whether to reveal which field was wrong (security) is not stated | Ambiguity | Unambiguous, Testable | High |
| 9 | 3.3 | "Too many" and "locked" undefined: number of attempts, duration, unlock method, counter reset | Ambiguity / Gap | Unambiguous, Complete | High |
| 10 | 3.4 | "Stay logged in" has no duration or behavior on shared devices | Gap | Complete | Low |
| 11 | 4.1 vs 2.2 | Minimum of 6 characters conflicts with the idea of "strong"; no maximum, no composition rules | Contradiction / Gap | Consistent, Complete | High |
| 12 | 4.2 | Reset process undefined: link expiry, how identity is verified, whether old password is invalidated | Gap | Complete | High |
| 13 | 5.1 | "secure", "scalable", "all popular", "etc." untestable; no measurable NFRs; no supported browser list | Untestable words | Testable, Feasible | High |
| 14 | 5.2 | "All users" is unclear (admins, guests, unverified users?); which profile fields? | Ambiguity | Unambiguous | Medium |
| 15 | Whole doc | No requirement IDs, no sources, no priorities, no acceptance criteria | Missing attributes | Traceable, Prioritized | High |
| 16 | Whole doc | No logout requirement and no unverified-account behavior | Gap | Complete | Medium |
| 17 | Whole doc | Assumptions not stated (email access, browser support, third-party mail service) | Gap | Complete | Medium |

### Step 2: Clarifying questions (a sample from the log)

| ID | Ref | Question |
|---|---|---|
| Q-001 | 3.1 / 2.1 | Do users log in with email or a username? If a username, where is it created during registration? |
| Q-002 | 2.2 / 4.1 | What is the full password policy (minimum, maximum, required character types, banned passwords)? |
| Q-003 | 3.3 | How many consecutive failed attempts trigger a lock, for how long, and does a successful login reset the count? |
| Q-004 | 2.4 | Must the email be verified before the first login? What is the link's expiry? |
| Q-005 | 3.2 | Should the error message reveal whether the email or password was wrong? |
| Q-006 | 5.1 | Which browsers, versions, and devices are in scope? What are the response-time and concurrent-user targets? |
| Q-007 | 4.2 | What is the lifetime of a reset link, and are old sessions ended after a reset? |
| Q-008 | 5.2 | Who can update a profile, and which fields are editable? |

### Step 3: Answers received (assume the product owner replies)

- Users log in with **email**; there is no separate username.
- Password: 8 to 64 characters, at least one letter and one digit.
- Lock: 5 consecutive failures, 15 minutes, successful login resets the counter.
- Email verification is **required** before login; link valid for 24 hours.
- Generic error message ("Email or password is incorrect.") for any login failure.
- Browsers: the latest two versions of Chrome, Firefox, Edge, and Safari; mobile browsers on iOS and Android at the latest two major versions.
- Performance: login and registration respond within 2 seconds for 95 percent of requests with 500 concurrent users.
- Reset link valid for 1 hour; all other sessions are ended after a reset.
- Only the logged-in account owner can edit their own profile; editable fields are name and display preferences (email change is out of scope).

### Step 4: Rewritten requirements

| New ID | Rewritten requirement | Priority | Source |
|---|---|---|---|
| REQ-REG-01 | A visitor shall be able to register by providing a name (1 to 50 characters), an email address, and a password that meets REQ-PW-01. | Must | US-101 |
| REQ-REG-02 | The system shall reject a registration where the email address is not in a valid format (for example missing "@" or domain) and display the message "Enter a valid email address." | Must | US-101 |
| REQ-REG-03 | The system shall reject a registration if the email is already registered and display "An account with this email already exists." | Must | US-101 |
| REQ-REG-04 | After successful registration, the system shall create the account in an "unverified" state and send a verification email to the supplied address within 1 minute. The email shall contain a verification link valid for 24 hours. | Must | US-102 |
| REQ-REG-05 | An unverified user shall not be able to log in; the system shall display "Please verify your email address." | Must | US-102 |
| REQ-PW-01 | Passwords shall be 8 to 64 characters and contain at least one letter and one digit. | Must | SP-05 |
| REQ-LOGIN-01 | A verified user shall be able to log in using their email address and password. | Must | US-103 |
| REQ-LOGIN-02 | For any failed login, the system shall display the single message "Email or password is incorrect." without indicating which was wrong. | Must | US-103 |
| REQ-LOGIN-03 | The system shall lock an account for 15 minutes after 5 consecutive failed login attempts; a successful login shall reset the failure count. A locked account shall display "Your account is temporarily locked. Try again in 15 minutes." | Should | SP-12 |
| REQ-LOGIN-04 | The login and registration pages shall respond within 2 seconds for 95 percent of requests with 500 concurrent users. | Should | NFR-02 |
| REQ-LOGIN-05 | The system shall offer a "Remember me" option that keeps the user signed in for 14 days on the same browser. | Could | US-104 |
| REQ-RESET-01 | A user shall be able to request a password reset by email; the reset link shall be valid for 1 hour and, once used, shall end all other sessions. | Should | US-105 |
| REQ-NFR-01 | The application shall be supported on the latest two versions of Chrome, Firefox, Edge, and Safari, and on the latest two major versions of iOS and Android mobile browsers. | Must | NFR-03 |
| REQ-PROF-01 | A logged-in user shall be able to edit only their own name and display preferences. | Could | US-106 |

Also noted: "user-friendly" in 2.5 was replaced by a measurable usability goal agreed with the business ("a first-time user can complete registration in no more than 4 steps"), which we log as **REQ-REG-06 (Could)**. Security and scalability were split into specific, measurable statements to be refined on Friday.

### Step 5: Acceptance criteria for one rewritten requirement

For REQ-LOGIN-03:

- **Given** a verified user who has failed login 4 times consecutively, **when** the user enters the wrong password a 5th time, **then** the account is locked and the lockout message is displayed.
- **Given** a locked account, **when** the user enters the correct credentials within the 15 minutes, **then** the login is rejected and the lockout message is displayed.
- **Given** a locked account, **when** 15 minutes have passed, **then** the user can log in with the correct credentials.
- **Given** a user with 3 failed attempts, **when** they log in successfully, **then** the failure count is reset to zero.

Testability note: the 15-minute duration makes manual testing slow; request a configurable lockout duration (or a way to set the clock) in the test environment.

### Step 6: RTM rows built from the clarified requirements

| Req ID | Requirement summary | Priority | Source | Test conditions (identified) | Coverage status |
|---|---|---|---|---|---|
| REQ-REG-01 | Register with name, email, compliant password | Must | US-101 | Registration succeeds with all valid fields; fails when any field missing; name length limits enforced; account created as unverified | Covered |
| REQ-REG-03 | Duplicate email rejected | Must | US-101 | Duplicate email shows exact message; duplicate check is case-insensitive (question pending) | Partially covered |
| REQ-REG-04 | Verification email within 1 minute, link valid 24 hours | Must | US-102 | Email received; arrives within time limit; link activates the account; expired link rejected; already-used link behavior | Covered (needs email test inbox) |
| REQ-PW-01 | Password 8-64 characters, letter and digit | Must | SP-05 | Accepted when compliant; rejected when too short, too long, missing letter, missing digit; message displayed | Covered |
| REQ-LOGIN-02 | Generic failure message | Must | US-103 | Same message for wrong password and unknown email | Covered |
| REQ-LOGIN-03 | Lock after 5 failures for 15 minutes | Should | SP-12 | Four failures do not lock; fifth locks; correct password rejected while locked; unlocks after 15 minutes; counter resets after success | Covered (needs configurable duration) |
| REQ-LOGIN-04 | Response time 2 seconds at 500 users | Should | NFR-02 | Response time measured under load (Friday) | Covered (needs load tool) |
| REQ-RESET-01 | Reset link 1 hour, ends other sessions | Should | US-105 | Link works within the hour; expired link rejected; other sessions ended; link single-use | Covered |

### Step 7: The requirement review report (summary)

| Item | Result |
|---|---|
| Document reviewed | User Registration and Login Requirements v0.3 |
| Review method | Individual review followed by a walkthrough with the product owner |
| Issues found | 17 (10 High, 6 Medium, 1 Low) |
| Main categories | Ambiguity (5), Gaps (7), Contradictions (2), Untestable words (3) |
| Overall assessment | Not ready for design or test design in current form; ready after clarified version v0.4 is baselined |
| Key risks | Security rules undefined (lockout, errors, reset); inconsistent login identifier; no measurable NFRs |
| Recommendations | Adopt clarified requirements; assign IDs and priorities; add acceptance criteria for every story; provide a test email inbox and configurable lockout in the test environment |

---

## Common Mistakes

| Mistake | Why it hurts | What to do instead |
|---|---|---|
| Waiting for the software before reading requirements | Defects found late cost far more | Review requirements as soon as they exist |
| Assuming the meaning of a vague sentence | Your assumption may differ from the developer's | Ask, and record the answer |
| Asking questions verbally and never recording them | Answers get forgotten or disputed | Use a question log or Jira comments |
| Accepting words like "fast", "easy", "etc." | They can never pass or fail | Request measurable values |
| Writing test cases directly from unreviewed requirements | Tests inherit the requirement's defects | Analyze first, then design tests |
| Ignoring non-functional requirements | Performance, security, and compatibility failures surface late | Always ask "what are the quality expectations?" |
| Treating everything as "high priority" | No guidance for effort or trade-offs | Ask the business to rank with MoSCoW |
| Not versioning requirements | Tests are written against the wrong version | Record version numbers and keep the RTM current |
| Blaming the author | Damages cooperation | Review the document, not the person |
| Building an RTM and never updating it | A stale RTM misleads | Update at every change; keep it simple |
| Assuming testers do not belong in requirement discussions | Testers bring a unique "how could this fail?" view | Join refinement, planning, and review sessions |
| Mixing design with requirements | Over-constrains the solution | Focus on "what", leave "how" to design |
| Ignoring unwritten (implicit) requirements | Obvious needs are often missed | Check conventions, standards, and similar products |
| Forgetting assumptions and constraints | Hidden risks grow | List them and confirm them |

---

## Try It: Review a Flawed Requirement Document (Project 1 Activity)

**Scenario.** The Project 1 team is adding a **"Forgot Password and Profile Update"** feature to the QE Foundations web app. You have received the draft below (version 0.1). Your job is to review it as a tester.

### The flawed document

> **Feature: Password Reset and Profile Update (Draft v0.1)**
>
> 1. Users can reset their password if they forget it. The reset should be quick.
> 2. The user enters their email on the "Forgot Password" page. The system sends them a reset link.
> 3. The reset link works for a reasonable time.
> 4. When the user clicks the link, they enter a new password. The new password must be at least 6 characters.
> 5. The user is shown an appropriate message after the reset.
> 6. Users can update their profile at any time. The profile includes name, phone, address, etc.
> 7. The profile page must be easy to use and work well on all devices.
> 8. Only authorized users can update the profile.
> 9. The system shall allow the user to change their email address. Email address cannot be changed after registration.
> 10. When a profile is updated, the user is notified.
> 11. The system should be secure and handle many users.

### Your tasks

1. **Read** the document twice: once for understanding, once with the eight characteristics as a checklist.
2. **List every issue** you find, identify its type (ambiguity, gap, contradiction, untestable word, missing attribute), and note which characteristic is violated.
3. **Write at least eight clarifying questions** in a question-log table (ID, requirement reference, question, directed to, status).
4. **Rewrite** three of the requirements so they are clear, unambiguous, testable, and traceable (give them IDs, make reasonable assumptions, and label your assumptions).
5. **Write acceptance criteria** (Given / When / Then) for one of your rewritten requirements.
6. **Prioritize** all requirements with MoSCoW and justify one choice.
7. **Create three RTM rows** for your rewritten requirements, including test conditions (not detailed cases).
8. **Write testability notes** (at least three) covering data, environment, and control issues.

When you finish, compare your work with the **Answer Key** at the end of this lesson. You will not match it word for word, and you do not have to; what matters is that you caught the same kinds of problems and asked useful questions.

**Stretch goal.** Create the Jira issues for your five most important questions, link them to a sample "Password Reset" story, and use a JQL filter (from Monday) to list your open question issues.

---

## Knowledge Check

Answer these questions in your own words, then compare with the answers at the end.

1. In one sentence, what is a requirement, and why is it called a "test basis"?
2. Name four sources of requirements.
3. What is the difference between a business requirement and a system requirement? Give one example of each.
4. Is this functional or non-functional: "The checkout page shall load in under 3 seconds"? Explain.
5. What is the difference between a constraint and an assumption?
6. List the eight characteristics of a good requirement discussed in this lesson.
7. Why is "The system should be user-friendly" a poor requirement? Suggest an improvement.
8. What are the key differences among an informal review, a walkthrough, and an inspection?
9. List five "red flag" words and explain why they are red flags.
10. What makes a clarifying question good? Rewrite this weak question: "Is the lock thing okay?"
11. What is the role of a question log?
12. What does the INVEST mnemonic stand for? Which letter relates most directly to testing?
13. Explain MoSCoW and give an example of a "Won't have" for Project 1.
14. What is a test condition, and how is it different from a test case?
15. What is a Requirement Traceability Matrix, and name three uses of it.
16. What is the difference between forward and backward traceability?
17. A requirement changes from "lock after 5 failures" to "lock after 3 failures". List four testing activities affected.
18. State three entry criteria and three exit criteria for the requirements analysis phase.
19. List four deliverables of the requirements analysis phase.
20. Why should testers be involved in requirement reviews rather than waiting until the software is built?

---

## Key Takeaways

- A **requirement** states what the system must do, how well, or within what limits. It is the tester's main test basis and test oracle.
- Requirements come from stakeholders, documents (BRD, SRS), user stories, use cases, prototypes, existing systems, and regulations. Know the source so you know whom to ask.
- Classify requirements as **business, user, or system**, and as **functional or non-functional**. Track **constraints** and write down **assumptions**.
- A good requirement is **clear, unambiguous, complete, consistent, testable, feasible, traceable, and prioritized**.
- **Static testing** of requirements (reviews, walkthroughs, inspections) finds defects at the lowest possible cost. This is **shift-left** in practice.
- Hunt for **ambiguity, gaps, contradictions, and untestable words** such as "fast", "user-friendly", "etc.", and "appropriate".
- Ask **specific, answerable, polite questions** and record them in a **question log**.
- **Acceptance criteria** (often Given / When / Then) make "done" verifiable; **testability analysis** tells us what we need to be able to test.
- Judge user stories with **INVEST**; prioritize with **MoSCoW**.
- Write **test conditions** from requirements; every condition you cannot write reveals a weakness.
- The **RTM** links requirements to tests and defects, shows coverage gaps, and drives **change impact analysis**.
- Manage **requirement changes** with versions, impact analysis, and an updated RTM and test set.
- The phase ends with **exit criteria** met and deliverables handed over: review report, clarified requirements, question log, RTM draft, and testability notes.
- Test design techniques (equivalence partitioning, boundary value analysis, decision tables, and others) come on **Thursday**; defects versus errors versus failures and the principles of testing come on **Wednesday**; deep non-functional testing comes on **Friday**.

---

## Additional Resources

- **ISTQB Certified Tester Foundation Level (CTFL) syllabus and glossary** - https://www.istqb.org (the glossary and syllabus cover static testing, reviews, test basis, test conditions, and traceability).
- **Atlassian Agile Coach: User Stories** - https://www.atlassian.com/agile/project-management/user-stories (user story format, acceptance criteria, and examples for Jira users).
- **IIBA - BABOK Guide** - https://www.iiba.org/business-analysis-body-of-knowledge/ (the business analysis body of knowledge, with in-depth treatment of requirements elicitation, analysis, and management).
- **Guru99: Requirement Traceability Matrix** - https://www.guru99.com/traceability-matrix.html (a beginner-friendly explanation of the RTM with examples).

---

## Answer Key

### Hands-On Practice: Review of "Password Reset and Profile Update (Draft v0.1)"

**1. Issues found**

| # | Ref | Issue | Type | Characteristic violated |
|---|---|---|---|---|
| 1 | 1 | "quick" is unmeasurable | Untestable word | Testable |
| 2 | 1 | No requirement IDs, sources, or priorities anywhere in the document | Missing attributes | Traceable, Prioritized |
| 3 | 2 | Behavior for an unregistered email is missing (reveal or not?); no message defined; delivery time of the email missing; whether an unverified user can reset is unstated | Gap | Complete |
| 4 | 3 | "reasonable time" is subjective | Ambiguity / Untestable | Unambiguous, Testable |
| 5 | 3 | Single-use or reusable link is not stated; behavior on expired link missing | Gap | Complete |
| 6 | 4 | Minimum password length of 6 may conflict with the existing policy (8 to 64 characters, letter and digit) | Contradiction (with other documents) | Consistent |
| 7 | 4 | No maximum length, composition rules, or rule against reusing the old password | Gap | Complete |
| 8 | 5 | "appropriate message" is undefined | Ambiguity | Unambiguous, Testable |
| 9 | 5 | Missing: whether the user is logged in automatically, and whether other sessions end | Gap | Complete |
| 10 | 6 | "etc." leaves profile fields undefined; "at any time" ignores states (locked or unverified accounts) | Untestable word / Gap | Testable, Complete |
| 11 | 6 | No validation rules for name, phone, and address (formats, lengths, mandatory or optional) | Gap | Complete |
| 12 | 7 | "easy to use" and "work well" are unmeasurable; "all devices" is infeasible and undefined | Untestable words | Testable, Feasible |
| 13 | 8 | "Authorized users" is undefined (which roles? only the owner?) | Ambiguity | Unambiguous |
| 14 | 9 | The two sentences directly contradict each other | Contradiction (within the requirement) | Consistent |
| 15 | 9 | If email change is allowed, re-verification behavior is missing | Gap | Complete |
| 16 | 10 | Notification channel (email, on-screen), content, and recipient (old and new email) are undefined | Gap | Complete |
| 17 | 11 | "secure" and "many users" are unmeasurable | Untestable words | Testable |
| 18 | 11 | "should" makes the priority unclear | Ambiguity | Prioritized |
| 19 | Whole doc | No NFRs: browsers, performance targets, accessibility, audit logging | Gap | Complete |
| 20 | Whole doc | No acceptance criteria, no assumptions or constraints listed | Missing attributes | Testable, Complete |
| 21 | Whole doc | Email-sending dependency is an unstated assumption | Gap (assumption) | Complete |

**2. Sample question log (8 or more; yours may differ)**

| ID | Ref | Question | Directed to | Status |
|---|---|---|---|---|
| Q-001 | 1 | What response time (in seconds, at what load) is acceptable for the reset request and the new-password page? | Product Owner | Open |
| Q-002 | 2 | If the entered email is not registered, should the page show the same confirmation message to avoid revealing which emails exist? | Product Owner / Security | Open |
| Q-003 | 2 | Within how many minutes must the reset email be delivered? Can unverified users request a reset? | Business Analyst | Open |
| Q-004 | 3 | How long is the reset link valid, and can it be used more than once? What message appears when it is expired or used? | Product Owner | Open |
| Q-005 | 4 | Does the new password follow the existing policy (8 to 64 characters, letter and digit)? Can it equal the previous password? | Product Owner | Open |
| Q-006 | 5 | What exact message appears after a successful reset? Is the user logged in automatically? Are other sessions ended? | Business Analyst | Open |
| Q-007 | 6 | Which profile fields exist, which are mandatory, and what are their formats and length limits? | Business Analyst | Open |
| Q-008 | 7 | Which browsers, devices, and screen sizes must be supported? How will "easy to use" be measured? | Product Owner / UX | Open |
| Q-009 | 8 | Which roles may update a profile? May an administrator edit another user's profile? | Product Owner | Open |
| Q-010 | 9 | May users change their email address? If so, is re-verification required and does the old address get notified? | Product Owner | Open |
| Q-011 | 10 | How is the user notified (email or on-screen), what does the notice say, and which address receives it? | Business Analyst | Open |
| Q-012 | 11 | What are the security expectations (for example, rate limits on reset requests) and the targeted number of concurrent users? | Architect / Security | Open |

**3. Sample rewrites (assumptions labeled)**

- **REQ-RESET-01 (Must):** The system shall provide a "Forgot Password" page where a user enters their registered email address. The system shall always display the message "If this email is registered, a reset link has been sent." and, if the email is registered and verified, send a reset link within 1 minute. *Assumption: generic message to avoid revealing registered emails.*
- **REQ-RESET-02 (Must):** A reset link shall be valid for 1 hour and usable once. An expired or used link shall display "This reset link is invalid or has expired." *Assumption: lifetime of 1 hour, pending Q-004.*
- **REQ-PW-02 (Must):** A new password set through reset shall meet REQ-PW-01 (8 to 64 characters, at least one letter and one digit) and shall differ from the current password. On success, the system shall display "Your password has been changed." and end all other sessions. *Assumption: reuse of the existing policy.*
- Alternative rewrite for item 9: **REQ-PROF-02 (Won't, this release):** Email address change is out of scope for this release; the email field is read-only on the profile page. *Assumption: resolves the contradiction in the safest direction until Q-010 is answered.*

**4. Sample acceptance criteria for REQ-RESET-02**

- **Given** a reset link issued less than 1 hour ago and not yet used, **when** the user opens it, **then** the "Set new password" page is displayed.
- **Given** a reset link issued more than 1 hour ago, **when** the user opens it, **then** the message "This reset link is invalid or has expired." is displayed and no password change is possible.
- **Given** a reset link that has already been used to change a password, **when** the user opens it again, **then** the same invalid or expired message is displayed.

**5. Sample MoSCoW**

| Req | Priority | Justification |
|---|---|---|
| Reset request and reset link (1, 2, 3) | Must | Users locked out of their accounts cannot use the product at all. |
| New password rule and result message (4, 5) | Must | Needed to complete the reset flow safely. |
| Profile update of name | Should | Valuable but not blocking; workaround is support request. |
| Phone and address fields | Could | Not essential to the core flows. |
| Email change | Won't (this release) | Needs re-verification design; out of scope. |
| Update notification (10) | Should | Security value, but the feature works without it. |
| NFRs: browsers, performance (7, 11) | Must for supported browsers; Should for load target | Compatibility is essential for use; load target can be refined. |

**6. Sample RTM rows**

| Req ID | Summary | Priority | Test conditions | Coverage status |
|---|---|---|---|---|
| REQ-RESET-01 | Forgot Password with generic message; email within 1 minute | Must | Registered email receives link; unregistered email shows same message and receives none; invalid email format rejected; unverified user behavior (pending question); delivery time within 1 minute | Partially covered (Q-003 open) |
| REQ-RESET-02 | Link valid 1 hour, single use | Must | Link works inside the hour; expired link rejected with message; used link rejected; link tampered with is rejected | Covered |
| REQ-PW-02 | New password meets policy, differs from old, ends other sessions | Must | Compliant password accepted; non-compliant rejected with message; same as old password rejected; confirmation message shown; other sessions ended | Covered |

**7. Sample testability notes**

1. The 1-hour link expiry is slow to test; request a way to set a short expiry (for example 1 minute) or to set the clock in the test environment.
2. Email delivery must be observable; request a test mailbox or an email capture tool (mail trap) in the test environment.
3. Testing "other sessions ended" requires multiple concurrent sessions or browsers; plan test data and tooling accordingly.
4. Testing "unregistered email shows the same message" requires verifying that no email is sent, which needs mailbox access and, ideally, logs.
5. Response-time requirements will need a load tool; defer to Friday and note the dependency.

### Knowledge Check Answers

1. A requirement is a statement of something the system must do, a quality it must have, or a limit it must respect to satisfy a need. It is called a test basis because tests are derived from it and results are judged against it.
2. Any four of: stakeholders, BRD, SRS, user stories, use cases, prototypes/wireframes, existing system, regulations.
3. A business requirement is a high-level organizational goal (for example, "grow registered customers by 20 percent"). A system requirement is a detailed statement of what the software must do (for example, "The system shall lock an account for 15 minutes after 5 failed attempts.").
4. Non-functional (performance). It describes how well the system performs, not what function it performs.
5. A constraint is a restriction on the solution or delivery (for example, a fixed deadline or required platform). An assumption is something believed true but not confirmed (for example, "all users have an email address").
6. Clear, unambiguous, complete, consistent, testable, feasible, traceable, prioritized.
7. "User-friendly" is subjective and cannot produce a pass/fail result. An improvement: "A first-time user shall be able to complete registration in no more than 4 steps without help text, and at least 90 percent of test participants shall succeed on the first attempt." (Values to be agreed with the business.)
8. An informal review has no fixed process and is a quick check by a colleague. A walkthrough is led by the author, who explains the document to gather feedback and share understanding. An inspection is a formal, rules-based process with defined roles, preparation, checklists, and recorded, measured defects.
9. Any five from: fast, user-friendly, easy, etc., appropriate, reasonable, secure (alone), scalable, as needed, always, never, all, TBD. Each lacks a measurable value or an exact scope.
10. A good question is specific, answerable, neutral, references the requirement, states the impact, and is directed to the right person. Rewrite: "REQ-LOGIN-03 says the account will be locked after too many failures. How many consecutive failures cause a lock, how long does it last, and does a successful login reset the count?"
11. It tracks every question from raise to answer to requirement update, so nothing is forgotten and there is a record of decisions.
12. Independent, Negotiable, Valuable, Estimable, Small, Testable. The "T" relates most directly to testing.
13. MoSCoW ranks requirements as Must have, Should have, Could have, and Won't have (this time). Example "Won't have" for Project 1: login with social media accounts (planned for a later release).
14. A test condition is something worth verifying (for example, "the account is locked on the 5th consecutive failure"). A test case is the detailed set of inputs, steps, and expected results used to check one or more conditions.
15. An RTM is a table linking requirements to test conditions, test cases, results, and defects. Uses: coverage checking, change impact analysis, progress reporting, audit evidence, defect linking.
16. Forward traceability goes from requirements to tests (are all requirements covered?). Backward traceability goes from tests back to requirements (does each test serve a requirement?).
17. Any four of: update or add test conditions and cases; change test data (for example, use 3 failed attempts rather than 5); rerun affected tests; perform regression testing of login; update automation scripts; update the RTM and estimates; communicate the change to the team.
18. Entry (any three): baselined requirement documents available; stakeholder access arranged; review team and schedule identified; tools available; project context known. Exit (any three): all requirements reviewed; issues logged; critical questions answered or escalated; clarified requirements versioned; RTM draft created; review report shared.
19. Any four of: requirement review report, clarified requirements, question log, RTM draft, testability notes, early inputs to the test plan.
20. Because defects found in requirements are cheapest to fix, testers bring a "how could this fail?" view, early involvement shares understanding, and it prevents defects from being built and tested later at far greater cost (shift-left).
