# Exploratory Testing

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define exploratory testing as simultaneous learning, test design, and test execution, and explain why it is a disciplined, skilled activity and not "random clicking."
2. Distinguish scripted testing, exploratory testing, and ad-hoc testing across planning, documentation, repeatability, skill, coverage evidence, and best-fit situations.
3. Recognize when exploratory testing is the right choice and when it is the wrong one.
4. Describe the exploratory testing cycle: learn, design, execute, observe, and decide what to do next.
5. Write clear, focused test charters using the "Explore... with... to discover..." template, and tell good charters from bad ones.
6. Explain session-based test management (SBTM): time-boxed sessions, session sheets, debriefs, and metrics, including their honest limitations.
7. Apply common heuristics and mnemonics (SFDIPOT, CRUD, Goldilocks, Zero-One-Many, Some-None-All, HICCUPPS, and testing tours) to generate test ideas and recognize problems.
8. Capture evidence and notes during a session, and turn findings into bug reports, new regression or automated test candidates, and new test ideas.
9. Explain pair testing, mob testing, and bug bashes, and how exploratory testing fits into Agile teams and CI/CD pipelines.
10. Discuss how AI can assist exploratory testing, and what cautions apply.
11. Plan, run, and report on a time-boxed exploratory testing session against Project 1 (User Registration and Login) and complete the Project 1 test-design and regression/risk documentation with the new ideas you discover.

---

## Why This Matters

Imagine you have spent the week building a strong set of test cases for Project 1. You used equivalence partitioning to choose representative inputs, boundary value analysis to probe the edges, decision tables to cover combinations of rules, and state transition diagrams to check how an account moves between states. Your test cases are well designed. You run them all, and they all pass.

Does that mean the registration and login features are bug-free? No. It means the product behaves correctly for the situations you thought of in advance. Every scripted test is limited by what the person who wrote it could imagine at the time they wrote it, which was usually before they had touched the working software. Real products contain surprises: a screen that behaves strangely after you press the Back button, an error message that reveals too much, a field that accepts something nobody expected, a combination of actions that nobody wrote a requirement for.

Exploratory testing is the discipline of looking for those surprises on purpose. You sit with the working product, learn from it as you go, and let what you discover guide what you test next. It is how skilled testers find the problems that no test case anticipated, which testers sometimes call "unknown unknowns."

Here is why this matters for you as a future AI-enabled Test Automation Engineer:

- **Automation only checks what you told it to check.** An automated suite is excellent at repeating known checks quickly and reliably, but it cannot notice a problem it was not programmed to look for. Exploratory testing is the human activity that finds new things worth automating.
- **Employers value it.** Test engineers who can explore a product thoughtfully, explain what they did, and report clear findings are far more valuable than those who can only follow a script.
- **It is where test ideas come from.** The test design techniques you learned on Thursday help you design tests. Exploratory testing helps you discover what needs designing in the first place.
- **It teaches product understanding.** Every automation script you write later will be better if you first understand how the product really behaves, including its odd corners.

Think of it this way: scripted tests and automation protect you against known risks. Exploratory testing is how you hunt for risks you have not met yet. A balanced quality-engineering approach uses both.

---

## The Concept

### 1. What exploratory testing is

**Exploratory testing** is an approach to testing in which the tester **simultaneously learns about the product, designs tests, and executes them**, using the results of each test to decide what to do next. The tester's own skill, experience, curiosity, and judgment guide the work.

Let us unpack each part of that definition.

- **Simultaneous.** In scripted testing, the activities happen in separate phases: someone first reads requirements and designs test cases, then later someone runs them. In exploratory testing, learning, design, and execution are interwoven. You try something, you see what happens, you learn from it, you design the next test immediately, and you run it.
- **Learning.** You are continuously building a mental model of the product: what it does, how it is structured, what its users want, where it seems fragile. Every observation updates that model.
- **Test design.** You create tests as you go. Techniques you already know, such as boundary value analysis, equivalence partitioning, error guessing, and state transition thinking, are all available to you in the moment.
- **Execution.** You run the test right away and carefully observe the product's response, not only the one thing you expected to check, but everything on the screen and around it.
- **Skill guides the testing.** The quality of exploratory testing depends on the tester. A tester who understands users, risks, technology, and test techniques will find more important problems than one who does not. This is a strength (it uses human intelligence) and a responsibility (you must keep building your skills).

#### What exploratory testing is NOT

A very common misunderstanding is that exploratory testing means "clicking around randomly" or "just playing with the app." That is not what skilled exploratory testing is. Compare the two:

| Random clicking | Exploratory testing |
|---|---|
| No goal; the tester drifts | A clear mission (a charter) focuses the effort |
| No record of what was done | Notes and evidence are captured as the work happens |
| Depends on mood and chance | Guided by risks, heuristics, and techniques |
| Cannot be explained afterwards | Can be explained, reviewed, and discussed in a debrief |
| Findings are hard to reproduce | Steps are noted so bugs can be reproduced and reported |

A useful analogy: imagine exploring a new city. **Random clicking** is wandering aimlessly with no map and no purpose, and afterwards you cannot say where you went or what you saw. **Scripted testing** is following a fixed guided tour: every stop is decided in advance, and the tour never changes. **Exploratory testing** is arriving with a map and a mission, for example "find the best places to eat near the old town and note anything that looks unsafe," and then following interesting side streets as they appear, keeping a travel diary, and adjusting your plan based on what you find. You have direction and discipline, but you stay free to follow what you learn.

#### Exploratory testing is a way of testing, not a separate technique

Exploratory testing is not an alternative to the black-box techniques you learned on Thursday. It is a style of working. During an exploratory session you will likely use equivalence partitions, boundary values, error guessing, and state-based thinking, but you choose them on the fly, in response to what you observe, rather than writing them all down in advance. It also applies to both black-box and, for testers with code knowledge, white-box viewpoints. Likewise, it can address both functional and non-functional qualities such as usability, performance impressions, and security-minded probing, which you studied earlier today.

### 2. A brief history and context

Software testing has always involved people experimenting with software. The name "exploratory testing" was given to the practice by **Cem Kaner**, a software testing researcher and educator, who is credited with coining the term in the 1980s. It appears in his writing on software testing and became a recognized term in the testing community afterwards. Kaner's central point was that testing is a skilled, cognitive activity, where learning and test design continue throughout testing instead of finishing before it begins.

Later, **James Bach**, together with Jonathan Bach and other contributors, developed and promoted ways to make exploratory testing more structured and accountable. One well-known result is **session-based test management (SBTM)**, which you will study later in this lesson. It is a way of managing exploratory work using time-boxed sessions, charters, and debriefs, so that managers can see and discuss what exploratory testers did without turning it into a rigid script. Bach and others, notably Michael Bolton, also contributed many of the heuristics and mnemonics used to guide exploration, several of which you will learn here. Other practitioners, such as Elisabeth Hendrickson (author of *Explore It!*) and James Whittaker (who wrote about "tours"), added widely used practical templates and metaphors.

You do not need to memorize names and dates. What matters is the general idea: exploratory testing is an established, respected practice with a body of thinking behind it, and it is not an excuse for being unstructured.

### 3. Scripted vs exploratory vs ad-hoc testing

You will hear these three terms constantly, and they are often confused. Let us define each.

- **Scripted testing** (also called test-case-based testing): tests are designed in advance, written down with steps and expected results, and later executed, either by a person following the steps or by an automated script. The design and execution are separated in time.
- **Exploratory testing**: learning, design, and execution happen together, guided by a charter and the tester's skill, with notes recorded as you go.
- **Ad-hoc testing**: informal, unplanned testing with no particular structure, no charter, and usually no documentation. It is a quick "let me try something" check. It can occasionally reveal a bug, but it is not repeatable or accountable. Some people use "ad-hoc" casually as a synonym for exploratory testing, but in this course we treat them as different: exploratory testing is deliberate and structured around a mission, while ad-hoc is unstructured.

Here is a comparison:

| Aspect | Scripted testing | Exploratory testing | Ad-hoc testing |
|---|---|---|---|
| **Planning** | Detailed, done in advance (test cases designed before execution) | Light but purposeful: a charter and time box defined in advance; specific tests decided during the session | Little or none |
| **Documentation** | Written test cases with steps and expected results; execution results recorded | Charter, session notes, bugs, questions, and evidence captured during and after the session | Usually none, or a quick comment |
| **Repeatability** | High: the same steps can be run again exactly | Moderate: the charter can be reused and notes allow partial repetition, but the exact path will differ each time | Low: nobody can reliably repeat it |
| **Skill required** | Lower for execution (follow the steps); higher for design | High: the tester designs, observes, and judges in real time | Varies; no guidance on how it is used |
| **Coverage evidence** | Clear: you can count executed test cases against requirements | Reasonable: charters covered, session counts, notes, and mind maps show where effort went | Weak: hard to show what was covered |
| **Best used when** | Compliance evidence, regression checks, highly repetitive checks, precise requirements, automation | New features, thin specifications, time pressure, hunting unknown risks, complementing automated checks | Very quick sanity looks, brief curiosity checks; not a primary strategy |

A key point: **scripted and exploratory testing are not opposites you must choose between.** Almost every real test effort mixes them. Even a person following a script notices things beyond the script (and a good one reports them), and even an exploratory tester may follow a short checklist. The difference is a matter of emphasis: how much of the testing is pre-decided versus decided in the moment.

### 4. When exploratory testing shines and when it does not

#### When exploratory testing shines

1. **New features.** When a feature has just been built, nobody yet knows how it really behaves. Exploring is the fastest way to learn it and find the earliest problems.
2. **Thin or missing specifications.** If requirements are vague or incomplete, writing detailed scripted test cases is difficult and may be wasteful. Exploring reveals what the product does and raises questions about what it should do.
3. **Time pressure.** When a release is close, you may not have time to design and document many test cases. A focused session can find important problems quickly, since there is no up-front documentation delay.
4. **Finding unknown unknowns.** Scripted tests cover what you knew to check. Exploration is how you discover what you did not know to check.
5. **Complementing automation.** Automated suites quickly check known behaviors. Exploratory testing covers the space automation does not, and it finds the things worth adding to the suite.
6. **After the automated suite passes.** A green automated run tells you the known checks still pass. It does not tell you the product is good. Exploring after a green run is a smart way to look for what the suite cannot see.
7. **Investigating a reported or suspected problem.** When a bug is reported vaguely or a failure appears intermittent, exploring around it helps understand its boundaries, causes, and related issues.
8. **Assessing usability and overall feel.** Human judgment about "does this make sense?" is central to exploration.

#### When exploratory testing is not the best choice

1. **When compliance or audit evidence is required.** Some industries and contracts demand documented proof that specific, pre-approved checks were run with recorded results. Exploratory testing can supplement this, but it is not a substitute for detailed traceable scripts when formal evidence is mandated.
2. **Highly repetitive checks.** Verifying the same large set of known behaviors on every build, such as a long regression suite, is exactly what automation does best. Having a human re-explore the same paths repeatedly is wasteful and error-prone.
3. **When the tester lacks product or testing knowledge and has no support.** Exploration depends on skill. A brand-new tester can still do it, but should be supported with clear charters, paired with an experienced colleague, and given heuristics (as you are being given in this lesson).
4. **When precise, exact expected results are needed for every step.** For example, calculations with strict rules (tax, interest) where each combination must be verified against known values may call for well-specified scripted or data-driven tests.

The honest summary: exploratory testing is powerful, but it is one tool among several. A mature test strategy mixes approaches based on risk, context, and evidence needs.

### 5. The exploratory testing cycle

Exploratory testing follows a continuous loop. You may circle it hundreds of times in a single session, often in seconds at a time.

```
   +--> LEARN ---> DESIGN ---> EXECUTE ---> OBSERVE --+
   |                                                  |
   +------------------ DECIDE NEXT <------------------+
```

1. **Learn.** Absorb what you know: the charter, the requirements you have, the behavior you have seen so far, the users, and the risks. Ask: "What is this thing supposed to do? Who uses it? What could go wrong?"
2. **Design.** Come up with a test or small experiment. For example: "What happens if I register with an email address that already exists but written in different capital letters?"
3. **Execute.** Run the test: enter the data, press the button, perform the sequence.
4. **Observe.** Watch carefully, and not only for the expected result. Check the displayed message, the page layout, the URL, the timing, the browser console, and anything that feels odd. A trained observer notices the small things. Ask: "Is this what I expected? If not, is it a problem, or did I misunderstand?"
5. **Decide what next.** Based on what you saw, choose your next move. Perhaps you dig deeper into a suspicious behavior, vary the input, pursue a new idea that popped up, record a bug, ask a question, or return to the charter.

The key idea is that **each result feeds the next test.** In scripted testing, test 7 is the same regardless of what test 6 revealed. In exploratory testing, test 7 depends on what test 6 taught you.

An analogy: think of a doctor examining a patient. The doctor does not follow an identical checklist for every person regardless of symptoms. They ask a question, listen to the answer, decide what to examine next, and adapt. They are still disciplined (they follow professional methods and keep records), but their next step is guided by what they learn.

### 6. Test charters in depth

#### What is a charter?

A **test charter** is a short statement of the mission for an exploratory testing session. It tells the tester what to explore and what kind of information to look for, without prescribing exactly which steps to take. Think of it as the "destination and purpose" of your trip, but not the route.

A charter is deliberately **open enough** to give the tester freedom to follow what they learn, yet **focused enough** that the tester knows what the session is about and can tell when they have drifted off-mission.

#### The standard template

A widely used charter template comes from **Elisabeth Hendrickson**, from her book *Explore It!*:

> **Explore** <target>
> **With** <resources, tools, data, techniques>
> **To discover** <information, risks, or problems>

Each part has a job:

- **Explore <target>**: the area, feature, or aspect of the product under investigation. For example, "the registration form."
- **With <resources>**: what you will use. This might be a technique ("boundary values"), data ("very long names, special characters"), a tool ("browser developer tools"), or a condition ("on a mobile viewport").
- **To discover <information>**: what you hope to learn. This might be risks, problems, or information about a quality ("how the form handles invalid input," "whether sensitive information leaks in error messages").

Example:

> **Explore** the registration form
> **With** boundary values and special characters in every text field
> **To discover** how invalid input is validated and whether error messages are clear and consistent

#### Good vs bad charters

A charter can fail in two opposite directions.

- **Too broad:** "Test the application." This is a whole career's worth of work. The tester cannot tell where to start or when they are done.
- **Too narrow:** "Enter 'abc' in the password field and verify an error appears." This is just a scripted test case wearing a charter's coat. It leaves no room to explore.
- **Just right (the Goldilocks idea):** a charter that can be explored in one session (about an hour or two), with a clear focus, and room for discovery.

| Bad charter | Why it is bad | Better charter |
|---|---|---|
| "Test the login." | Too broad; no focus, no information goal | "Explore the login page with invalid and unusual credentials to discover how failed attempts are handled and what messages users see" |
| "Check that the Register button works." | A single check, not exploration; the answer is yes/no | "Explore the registration submit flow with slow network conditions and repeated clicks to discover duplicate-submission and feedback problems" |
| "Find bugs." | No target and no method; nobody can plan or review it | "Explore the password rules with boundary lengths and character types to discover gaps between displayed and enforced rules" |
| "Try everything on the site." | Impossible to finish or measure | Split into several focused charters, each aimed at one feature or risk |
| "Verify requirement REQ-12." | Confirmation-only; this is verification by script | "Explore the email field with varied formats to discover whether validation matches the stated requirement and user expectations" |
| "Look at the login for 5 minutes." | Time is stated but no purpose | "Explore the login page on a mobile viewport with the keyboard open to discover layout and usability problems" |

A quick test for any charter: Can I finish this in one session? Do I know where to begin? Is there room for me to follow my curiosity? Does it say what kind of information I am seeking? If all four are "yes," the charter is probably good.

#### Charter examples for Project 1

Here are fourteen sample charters for Project 1 (User Registration and Login). Notice how each focuses on a different target, resource, or risk.

1. **Explore** the registration form **with** valid, boundary, and invalid values in every field **to discover** validation gaps and inconsistent error messages.
2. **Explore** the password rules **with** boundary lengths, character-type combinations, and pasted values **to discover** differences between the rules shown to users and the rules actually enforced.
3. **Explore** the email field **with** unusual but valid addresses (plus signs, subdomains, capital letters) and almost-valid addresses **to discover** whether validation is too strict, too lenient, or inconsistent.
4. **Explore** duplicate registration **with** the same email in different letter cases and with leading or trailing spaces **to discover** whether the system correctly prevents duplicate accounts and how it communicates this.
5. **Explore** the login page **with** wrong, empty, and unusual credentials **to discover** how failed logins are handled, whether messages reveal too much information, and whether any lock-out rule exists.
6. **Explore** the sequence of registering, logging out, and logging in again **with** browser Back, Forward, and Refresh actions **to discover** state and navigation problems (what happens to the session and the page).
7. **Explore** the registration flow **with** repeated button clicks and a throttled network speed in browser developer tools **to discover** duplicate submissions, missing feedback, and confusing loading states.
8. **Explore** the registration and login forms **with** keyboard-only navigation and a screen-reader-friendly mindset **to discover** accessibility and usability problems.
9. **Explore** the forms **on** a small mobile viewport and different browsers **to discover** layout, readability, and compatibility problems.
10. **Explore** the session behavior after login **with** multiple tabs, an expired session, and direct URL access to protected pages **to discover** security-minded and state-handling problems.
11. **Explore** the "forgot password" or account recovery behavior (if present) **with** unknown, known, and malformed email addresses **to discover** whether the messages leak whether an account exists and how robust the flow is.
12. **Explore** the text content of the pages **with** a review for spelling, tone, and consistency **to discover** wording problems and mismatches between messages and actual behavior.
13. **Explore** the data entered during registration **with** special characters, very long strings, and non-English letters **to discover** whether data is stored and displayed correctly after login.
14. **Explore** the Terms and Conditions or consent checkbox (if present) **with** attempts to submit with and without it **to discover** whether the rule is enforced on screen and consistently on submission.

Notice how none of these is a yes/no check. Each contains a question that cannot be fully answered in advance.

### 7. Session-based test management (SBTM)

A natural worry about exploratory testing is: "If nothing is scripted, how does a manager know what was tested? How do we avoid chaos?" **Session-based test management (SBTM)** is a lightweight framework designed to answer exactly that. It was developed by James Bach and Jonathan Bach and is widely taught.

SBTM organizes exploratory testing into **sessions**, with just enough structure to make the work visible and accountable, without removing the tester's freedom.

#### The session

A **session** is an uninterrupted, time-boxed block of exploratory testing focused on one charter.

- **Time-boxed.** A session has a fixed length. Typical guidance is:
  - **Short:** about 60 minutes
  - **Normal:** about 90 minutes
  - **Long:** about 120 minutes

  The exact numbers are conventions, not laws. Many teams settle on 60 to 90 minutes because intense, focused thinking is tiring. For you as a learner, 30 to 60 minutes is a very reasonable starting point.
- **Uninterrupted.** During the session, the tester does not check messages, attend meetings, or switch tasks. Focus is part of what makes exploration effective, since you are holding a detailed mental model of the product in your head, and interruptions destroy it.
- **Charter-driven.** The session is anchored by one charter. If you find something that is not on the charter but looks important, you note it and may pursue it briefly, but you track that time separately (see on-charter vs opportunity time below).
- **Reviewable.** At the end, the tester produces a session sheet and discusses it in a debrief.

#### The session sheet

A **session sheet** is a short record of what happened. Typical contents:

| Section | Purpose |
|---|---|
| **Charter** | The mission for this session |
| **Tester** | Who ran the session |
| **Date and start time** | When it began |
| **Duration** | Short, normal, or long (or actual minutes) |
| **On-charter vs opportunity time** | How much time went to the chartered work versus new areas the tester chose to investigate along the way |
| **Test notes** | What was tested and observed, in rough chronological order |
| **Bugs** | Defects found, with brief reproduction details |
| **Issues / questions** | Non-bug concerns: unclear requirements, blocked work, environment trouble, open questions |
| **Debrief notes** | Discussion points and outcomes of the review |

(Some SBTM forms also split time into test design and execution, bug investigation and reporting, and setup. We keep the simpler on-charter versus opportunity split here, plus a note of any time lost to setup or interruptions.)

**On-charter time** is time spent on the work the charter describes. **Opportunity time** is time spent investigating something valuable that was not in the charter but that you stumbled upon. It is perfectly acceptable, and often productive, to follow an opportunity. The point of recording it is honesty: the charter was only partly covered, and the manager can see why.

#### The debrief

After a session, the tester talks with a lead, manager, or teammate in a short **debrief**, often 10 to 15 minutes. The debrief makes the session accountable and shares learning. A well-known aid is the mnemonic **PROOF**, associated with Jon Bach's debriefing approach:

- **P: Past.** What happened during the session? What did you do?
- **R: Results.** What did you achieve? What did you find? What was learned?
- **O: Obstacles.** What got in the way of good testing? (Environment problems, missing information, unstable builds.)
- **O: Outlook.** What still needs to be done? What should be tested next?
- **F: Feelings.** How do you feel about the product and the testing? (Confidence, concern, hunches.)

The "Feelings" element may seem unusual in a professional setting, but a tester's hunch ("something about the password reset feels unreliable") is often valuable information that deserves attention, even if it has not yet been proven.

#### Metrics in SBTM, and their honest limits

Because sessions are countable and consistent, managers can gather simple numbers:

- **Number of sessions** completed (per feature, per person, per week).
- **Bugs found per session** (and perhaps bug severity breakdown).
- **Charter coverage:** how many planned charters have been completed, and how many remain.
- **On-charter vs opportunity percentage.**
- **Session length mix** (short, normal, long).

These can be useful for planning and reporting: "We completed 9 of 12 planned sessions for the registration area and have raised 14 bugs, 3 of them high severity."

But be honest about the caveats:

- **A session is not a standard unit of work.** One session might find five bugs and another none, depending on the area, tester, and luck. Counting sessions is not like counting identical items.
- **Bugs per session is a weak quality signal on its own.** Zero bugs may mean a healthy area, a skilled developer, a shallow session, or the wrong charter. A large number may mean a very buggy area, or a very thorough tester. Numbers need interpretation and conversation.
- **Charter coverage does not equal product coverage.** Completing all charters means you explored the areas you thought of. It does not prove the product is free of problems.
- **Metrics can be gamed.** If people are rewarded for the number of bugs per session, they may split a single problem into many reports.
- **Use metrics to start conversations, not to judge people.** Always pair numbers with a story: what was found, what remains risky, and what the tester thinks.

### 8. Heuristics and mnemonics

A **heuristic** is a fallible rule of thumb, a thinking aid that often helps but is not guaranteed to work. A **mnemonic** is a memory aid, often an acronym, that helps you remember a heuristic. Skilled exploratory testers carry many of these in their heads. They do not guarantee finding bugs; they help you generate ideas when you might otherwise get stuck.

Think of heuristics as a traveler's checklist of questions: "Have I looked at the food? The transport? The safety? The cost?" They prompt you to look at things you might forget.

#### SFDIPOT: product elements to explore

**SFDIPOT** (often pronounced "San Francisco Depot") is a mnemonic from James Bach's Heuristic Test Strategy Model. It lists dimensions of a product you can examine when generating test ideas.

| Letter | Stands for | Meaning | Project 1 example |
|---|---|---|---|
| **S** | Structure | What the product is made of: code, files, components, pages, database | Are there shared components between registration and login (like the password field)? Does a change in one affect the other? |
| **F** | Function | What the product does | Register, log in, log out, validate inputs, show messages |
| **D** | Data | What the product processes: inputs, outputs, stored data; valid, invalid, boundaries | Names with apostrophes, emails with plus signs, very long passwords |
| **I** | Interfaces | How the product connects to users and other systems: UI, APIs, imports/exports | The forms, error messages, any email confirmation, any back-end calls visible in developer tools |
| **P** | Platform | What the product depends on: browsers, operating systems, devices, screen sizes, network | Chrome vs Firefox vs Edge, mobile viewport, slow network |
| **O** | Operations | How the product is used in real life: typical users, common and unusual scenarios, stress, error conditions | A user who registers, forgets the password, and returns days later; a user who gets distracted mid-form |
| **T** | Time | Anything related to time: timing, delays, order of events, timeouts, dates | Session expiry, double-click timing, concurrent actions, behavior after long idle |

You can use SFDIPOT as a checklist at the start of planning charters ("Do I have a charter touching each dimension?") or in the middle of a session when you are out of ideas ("I have tested Function and Data; what about Time?").

#### CRUD

**CRUD** stands for **Create, Read, Update, Delete**, the four basic operations on stored data. For any kind of data in the product, ask: can it be created? Can it be viewed (read)? Can it be changed? Can it be deleted? And, importantly, how do these interact?

For Project 1, the "data" is the user account:

- **Create:** register a new account. What if some details are missing or already used?
- **Read:** log in and view profile or account details. Does the displayed data match what was entered?
- **Update:** change password or profile information (if available). Does the change take effect everywhere? Does the old password stop working?
- **Delete:** delete or deactivate the account (if available). Can the same email be registered again afterwards? What happens to a logged-in session?

CRUD reminds you to test the full lifecycle of data, not just its creation. Many bugs live in the "U" and "D."

#### Goldilocks: too big, too small, just right

The **Goldilocks heuristic** (named after the fairy tale) asks you to test with values that are **too big, too small, and just right**. It is a quick cousin of boundary value analysis.

- **Too small:** an empty field, one character, zero, a negative number.
- **Too big:** an extremely long name, a huge number, a very large file.
- **Just right:** a normal, valid value inside the expected range.

Applied to a Project 1 password with a stated length of 8 to 20 characters: 1 character and 7 characters (too small), 8 to 20 characters (just right), 21 characters and 500 characters (too big). The heuristic also nudges you to test the "just right" case, because a product can fail even on normal input.

#### Zero-One-Many

**Zero-One-Many** says: whenever something can occur multiple times, test with zero of them, one of them, and many of them. Bugs frequently hide at these transitions.

- **Zero:** no failed login attempts; no accounts registered; an empty cart.
- **One:** exactly one failed attempt; a single account; a single item.
- **Many:** many failed attempts in a row; thousands of accounts; fifty items.

For Project 1: how does the product behave after zero, one, three, and ten failed login attempts in a row? Is the behavior consistent with what the requirements say about lock-outs?

#### Some-None-All

**Some-None-All** is similar. When there is a group of options, test with **some, none, or all** selected or filled in.

- **None:** no required fields filled; no checkboxes ticked.
- **Some:** only some fields filled in (for example, filled in everything except the last name).
- **All:** every field filled, every checkbox ticked.

Registration forms are a natural fit: submitting with all fields empty, with only some completed, and with everything complete. Some-None-All also helps with permission options, notification preferences, and filters.

#### Follow the money

**Follow the money** means focusing on what matters most to the business or the user, typically where money, value, or critical data flows. In an online store, that is the checkout and payment. In Project 1, "the money" is arguably the **account creation and login flow itself**: if users cannot sign up or sign in, nothing else in the product is reachable, and any security failure here could expose user data. Prioritize your exploration where failure would hurt most. Ask: "What could cost the business or the user the most?"

#### Tours

James Whittaker popularized the idea of **tours** in exploratory testing. A **tour** is a themed way of exploring a product, much like a sightseeing tour has a theme (historic sites, food, nightlife). Choosing a tour gives your exploration a clear flavor and helps you avoid wandering.

The **touring metaphor** reminds us that a tester is like a tourist or a guide visiting a new place: you can take many different tours of the same city and see different things each time. Likewise you can tour the same product in many ways, and each tour reveals different problems.

Here are a handful of widely discussed tours, with ideas for Project 1:

| Tour | Idea | Project 1 example |
|---|---|---|
| **Feature tour** | Visit each feature or control in turn, to learn what exists and see that each does something sensible | Click every link, button, and field across the registration and login pages and note what each does |
| **Money tour** | Concentrate on the features that bring the most value to users or the business | Walk through the complete happy path from registration through first login, as a real new customer would |
| **Landmark tour** | Identify the key "landmark" features and navigate between them in different orders | Move between register, login, logout, and any account page, in many different sequences |
| **Back-alley tour** | Visit the least-used, least-visible corners of the product that few people touch | Rarely used pages, footer links, help text, error pages, unusual URLs |
| **All-nighter tour** | Keep the product running and in use for a long time without restarting, to find problems that appear over time | Leave a session logged in for a long period and then try to act; keep a form half-filled for a long time before submitting |
| **Saboteur tour** | Try to break the product by making its operations fail or by interfering with it (sometimes described as attacking the product like a saboteur) | Submit forms while the network is dropped; close the tab mid-submission; clear cookies while logged in |
| **Supermodel tour** | Look only at the surface: how things look, not how they work (focusing on layout, visual consistency, and polish) | Alignment, fonts, colors, spacing, truncated text, mismatched button styles |

(The supermodel tour is sometimes jokingly called the "shallow" tour. It is valuable because users judge a product quickly by how it looks.)

Other tours exist, such as the **antisocial tour** (using the least expected or least cooperative inputs) and the **garbage collector tour** (systematically going through every item or area one by one). You do not need to memorize them all. The lesson is that choosing a *theme* for your exploration is an effective way to generate focused charters.

#### Boundary and variation heuristics

Several heuristics encourage you to vary conditions systematically:

- **Variability tours.** Look for anything that can be changed in the product (settings, data values, options, order of operations) and change it. Each variable you find is a place where behavior may differ. In Project 1: field values, the browser, the language setting, the screen size, the order in which you fill fields.
- **Data type attacks.** Deliberately give an input a value of the *wrong type* or an unexpected kind. Put letters in a numeric field, numbers in a name, emoji or accented characters in an email, spaces only, extremely long text, symbols such as `<`, `>`, `&`, quotes, or a string that looks like code. The goal is to see whether the product handles unexpected data gracefully. (Note: at this foundational level, this is about observing handling and messages, not about attacking real systems. Only test applications you are authorized to test.)
- **Boundary heuristics.** Everything you learned about boundary value analysis applies in the moment: just inside, on, and just outside a limit.

#### HICCUPPS: recognizing a problem

A big question in exploratory testing is: **how do you know something is a problem when there is no written expected result?** You use *oracles*. An **oracle** is any means by which you decide whether the product's behavior is right or wrong. **HICCUPPS** is a mnemonic for common consistency oracles, developed by James Bach and Michael Bolton. It says: *a product is probably wrong if it is inconsistent with any of these.*

| Letter | Oracle | Short explanation | Project 1 example |
|---|---|---|---|
| **H** | History | The product should be consistent with its own past behavior (earlier versions or earlier in this session), unless a change was intended | Last release, an invalid email showed a clear error; now it shows nothing. Something has regressed. |
| **I** | Image | The product should be consistent with the image the organization wants to project (brand, professionalism, quality) | A raw technical error code or a rude message appears on a polished consumer site |
| **C** | Comparable products | The product should be consistent with similar products people know | Most sign-up pages show a password strength hint or a show/hide icon; ours is much harder to use |
| **U** | User expectations | The product should do what reasonable users would expect | A user expects pressing Enter in the last field to submit the form |
| **P** | Product | The product should be consistent with itself: similar things should behave similarly in different places | The registration page trims spaces in the email, but the login page does not |
| **P** | Purpose | The product should be consistent with the explicit and implicit purpose of the feature | A "Log out" button that leaves the user still logged in contradicts its purpose |
| **C** | Claims | The product should be consistent with what it, its documentation, or people say about it (requirements, help text, marketing, messages) | The page says "Password must be at least 8 characters," but 6 characters are accepted |
| **S** | Statutes | The product should be consistent with laws, regulations, and standards | Privacy rules about handling personal data; accessibility requirements |

(HICCUPPS is usually written with "Statutes" at the end, giving the pronounceable acronym. The order of the letters is just a convenience.)

HICCUPPS is extremely useful for beginners. When you see something odd, run through the list and ask: "What is this inconsistent with?" If you can name the oracle ("it is inconsistent with the claim on the page," or "with user expectations"), you can explain your bug report convincingly. Remember, oracles are fallible. Sometimes the product is right and your expectation is wrong. That is why the answer is often a *question* ("Is this intended?") instead of an immediate bug report.

### 9. Note-taking and evidence capture

Exploratory testing leaves no pre-written script, so your **notes and evidence are your record**. Without them, you cannot reproduce bugs, explain your coverage, or learn from the session. Good practice:

- **Take notes as you go.** Write in short, time-stamped lines: what you tried, what you saw, what you will try next. Do not wait until the end; memory fades quickly. A text file, a notebook, or a note section in your session sheet works.
- **Record steps and data precisely when something looks wrong.** Note the exact input values, the sequence, the browser, the time. This is what makes a bug reproducible.
- **Capture screenshots.** For visible problems, take a screenshot immediately. Annotate it if useful.
- **Use screen recordings.** For problems involving sequences, timing, or hard-to-explain behavior, record your screen. A short video can replace paragraphs of description. Many operating systems and browsers include built-in screen recording tools, and there are free screen recorder tools available.
- **Use browser developer tools.** The console shows errors; the network panel shows requests and responses; these are often valuable evidence for a bug report (for example, a request that returned an unexpected error).
- **Use mind maps.** A mind map is a diagram with a central idea branching into related ideas. Testers often use one to plan a session or to show what has been covered, with branches such as "Fields," "Messages," "Navigation," "Platforms." It gives a visual picture of coverage and can be shared in a debrief.
- **Use a consistent system for markers.** Many testers prefix notes with simple tags, for example: `BUG:`, `Q:` (question), `IDEA:` (a new test idea), `RISK:`, `TODO:`. This makes sorting notes after the session fast.
- **Log defects in your tracker.** Jira (which you learned on Tuesday) is the usual home for bug reports, with attachments such as screenshots and recordings.

A practical tip: keep a second window or note file open beside the browser, and write something at least every few minutes. If you notice you have not written anything for a long time, you may be drifting into random clicking.

### 10. Turning findings into value

The session itself is only the beginning. Three kinds of output follow.

#### Bug reports

When you find a defect, you report it using the practices from Tuesday's lesson on the defect lifecycle: a clear title, steps to reproduce, expected result, actual result, environment, severity and priority, and evidence. A few points particular to exploratory testing:

- **Reproduce before reporting.** Because you may have reached the problem by a winding path, try to find the *shortest* reliable sequence of steps. If it does not reproduce, note that honestly and record what you did.
- **Isolate the cause.** Does it happen in other browsers? With other data? Narrowing it makes the bug more useful to developers.
- **State the oracle.** Say *why* you believe it is a problem ("The page claims at least 8 characters but accepted 6").
- **Separate bugs from questions.** If you are unsure whether it is a defect, raise it as a question to the product owner or business analyst, not as a bug.

#### New regression and automated tests

Many exploratory findings deserve to become permanent checks. When you find and the team fixes a defect, ask: "Should this be added to the regression suite so it can never silently come back?" If it is a stable, repeatable behavior, it may be a candidate for automation. (Automation tooling is beyond today's scope; at this point, simply *flag* the candidates.) Exploratory testing is therefore a **source of automation candidates**: the humans discover, and the machines guard.

#### New test ideas and the pesticide paradox

You met the **pesticide paradox** in Wednesday's principles of testing: if you keep running the same tests over and over, they eventually stop finding new defects, just as pests become resistant to the same pesticide. Exploratory testing is a powerful counter. Because each session takes a different path, it produces *fresh* test ideas. Feed the best ones back into your scripted test suites and your test design document, so your scripts evolve instead of going stale. In your Project 1 documentation, keep a section called "Ideas from exploratory sessions" and review it at the end of each week.

### 11. Pair, mob, and bug-bash exploratory testing

Exploratory testing does not have to be a solo activity.

- **Pair testing.** Two people explore together at one computer, with one driving (operating the product) and the other observing, asking questions, and taking notes. The pairing might be tester and tester, tester and developer, or tester and business analyst. Pairs often discover more because each person notices different things and prompts the other's thinking. It is also a superb way for beginners to learn from experienced testers.
- **Mob testing.** A small group (three or more) explores together on one shared screen, taking turns driving. It spreads knowledge across the team and brings in diverse viewpoints, though it requires good facilitation and uses more people's time.
- **Bug bash.** A time-boxed event, often an hour or two, where many people (testers, developers, designers, product owners, sometimes other staff) test the product together, each exploring and reporting problems, often just before a release. Bug bashes bring many fresh perspectives cheaply. They work best when you provide a clear scope, basic instructions, a place to log bugs, and a plan to triage the incoming reports quickly, since a bash can produce many duplicates and minor items.

### 12. Exploratory testing in Agile and CI/CD

In Agile teams, working software is delivered in small increments, and requirements often evolve. Exploratory testing fits naturally.

- **At the end of a story.** When a user story is built, a short exploratory session on that story helps confirm that it works and finds issues the acceptance criteria did not mention, before the story is called "done."
- **Sprint-level sessions.** Toward the end of a sprint, run broader sessions that combine the stories delivered so far, looking for integration problems and surprises across features.
- **Test the increment.** The sprint's output is a working increment of the product. Exploring the whole increment, like a user would, checks that the pieces work together.
- **In the Definition of Done.** Some teams include "exploratory testing completed" as a condition of being done.
- **In CI/CD.** A **CI/CD pipeline** (continuous integration and continuous delivery or deployment) automatically builds, tests, and delivers changes. Automated checks in the pipeline provide fast feedback. Exploratory testing sits *beside* the pipeline: testers explore a freshly deployed build in a test environment, often in parallel with or after the automated checks, and they feed discoveries back into the automated suite. In some teams, exploratory testing also happens on production-like environments, or for new features behind feature flags (switches that show a feature only to some users), to learn early.
- **Fast feedback.** Because exploration needs no heavy preparation, a tester can begin the moment a build is available.

A balanced Agile test approach: automate the known checks so they run on every change; use exploratory testing to investigate, question, and learn, especially for new and changed areas.

### 13. Exploratory testing and AI

AI tools, such as large language models, can support exploratory testing. You will use these more in later weeks, but here are some early ideas and cautions.

**Helpful uses:**

- **Suggesting charters and risks.** You can describe a feature ("a registration form with email, password, and consent checkbox") and ask an AI assistant to propose charters or risks to explore. It can quickly broaden your thinking.
- **Generating test data ideas.** It can propose unusual input values, edge cases, or character sets for your data type attacks.
- **Acting as a test partner.** You can describe what you observed and ask, "What else might I try?" or "What might cause this behavior?" It can act as a thinking partner, much like a colleague in pair testing.
- **Applying heuristics.** You can ask it to walk through SFDIPOT or HICCUPPS for a feature, to prompt your own thinking.
- **Summarizing notes.** It can help organize messy session notes into a tidy session sheet or draft a bug report from your notes (which you must then check).

**Cautions:**

- **AI does not see the real product behavior unless you show it.** Its suggestions are guesses based on patterns. You still must run the tests and observe the actual results.
- **It can be confidently wrong.** AI can invent features, requirements, or "bugs" that do not exist. Verify before acting.
- **It lacks your context.** It does not know your users, business risks, or the history of your product unless you tell it, and even then it may miss nuance.
- **Do not paste confidential data.** Never put private customer data, credentials, or proprietary information into AI tools unless your organization has approved that tool for that use.
- **Judgment remains yours.** The decision about what matters, what is a bug, and what is risky stays with the tester. Treat AI output as input to your thinking, not as a replacement for it.

### 14. Measuring and reporting exploratory testing to managers

Managers rightly want to know: What was tested? What did you find? How confident should we be? Because exploratory testing has no list of executed test cases, you need to report differently. Useful approaches:

- **Tell the story of testing.** Report in terms of charters and sessions: "We ran 8 sessions across registration and login. Here are the areas covered, the main findings, and the areas not yet explored."
- **Use a coverage map.** A simple table or mind map of product areas against sessions run shows where effort went and where gaps remain.
- **Report risks and findings, not just counts.** "Three high-severity issues in password handling, and we are not confident in session expiry behavior" says far more than "18 bugs."
- **Include what was NOT tested.** A strong report states what was out of scope or not reached, and why.
- **Use the simple metrics (with caveats).** Sessions completed, bugs per session, charters covered, and on-charter versus opportunity time. Present them as indicators, never as proof of quality.
- **Share debrief outcomes.** What the testing team feels, what worries them, and what they recommend next.
- **Present evidence on request.** Session sheets, screenshots, recordings, and bug links give transparency without requiring scripts.

A sample reporting line: "Registration: 3 of 4 planned sessions complete; 9 bugs raised (2 high severity, both in duplicate-account handling); 3 open questions on password rules awaiting product owner; remaining risk: behavior under slow networks has not yet been explored."

### 15. Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Finds unexpected problems that scripts miss | Depends heavily on tester skill and experience |
| Fast to start; little preparation needed | Less repeatable; the exact path cannot be rerun precisely |
| Adapts quickly to changing products and new information | Weaker as formal, traceable evidence for audits |
| Builds deep product knowledge and tester engagement | Coverage is harder to prove and measure |
| Generates new test ideas and automation candidates | Can drift without a good charter and time box |
| Works well when specifications are thin | Results vary between testers and sessions |
| Encourages critical thinking and curiosity | Notes quality varies; poor notes lose value quickly |

The best way to use its strengths while managing its weaknesses is through charters, time boxes, notes, debriefs, and by pairing it with scripted and automated testing.

---

## Examples

### Worked Example 1: A 60-minute session on the Project 1 registration page

This is a complete, realistic example of one exploratory testing session. The details are illustrative. In your own work, use whatever your Project 1 application actually does.

#### Session Sheet

| Field | Value |
|---|---|
| **Charter** | Explore the registration form with boundary values, special characters, and unusual formats in every field to discover validation gaps and inconsistent error messages. |
| **Tester** | A. Learner |
| **Date** | Friday, week 3 |
| **Start time** | 10:00 |
| **Duration** | Short session (60 minutes planned; 60 actual) |
| **Build / environment** | Project 1 test environment, build 0.3; Chrome (latest), Windows laptop |
| **Time split** | On-charter: about 70% (42 minutes). Opportunity: about 20% (12 minutes). Setup and interruptions: about 10% (6 minutes) |

**Project 1 registration fields assumed for this example:** Full name, Email, Password, Confirm password, and a Terms checkbox, with a Register button. The page states: "Password must be 8 to 20 characters and include a letter and a number."

#### Time log

| Time | Activity |
|---|---|
| 10:00 - 10:06 | Setup: open the page, open browser developer tools, create a notes file, read the on-page rules |
| 10:06 - 10:16 | Feature tour of the form, then the valid happy-path registration to get a baseline |
| 10:16 - 10:30 | Password rules: lengths, character types |
| 10:30 - 10:38 | Email formats |
| 10:38 - 10:46 | Name field with special characters and long text |
| 10:46 - 10:58 | Opportunity: duplicate registration and response behavior (found while testing email) |
| 10:58 - 11:00 | Wrap-up: review notes, mark bugs, write questions and ideas |

#### Test notes (in order)

1. **10:08** Page loads; labels: Full name, Email, Password, Confirm password, Terms checkbox. Page says password must be 8 to 20 characters with a letter and a number. Baseline noted.
2. **10:12** Happy path: "Asha Rao", `asha.rao@example.com`, `Passw0rd123` registers successfully; success message "Registration successful." and redirect to login page. Baseline works.
3. **10:18** Password with 7 characters (`Abc1234`): rejected with "Invalid password." The message does not say why. (User expectation: tell me the rule.)
4. **10:20** Password with exactly 8 characters (`Abcde123`): accepted. Boundary behaves as stated.
5. **10:22** Password with 20 characters accepted; 21 characters accepted too, with no error. **BUG: upper boundary not enforced (contradicts the on-page claim).**
6. **10:25** Password of 8 letters only (`Abcdefgh`) is rejected, as expected; 8 digits only (`12345678`) is also rejected. The message is the same "Invalid password." for all failures.
7. **10:27** Password with leading and trailing spaces (` Abcde123 `) accepted. Unclear whether the spaces are stored. **Q: Should spaces be trimmed or rejected?**
8. **10:31** Email `asha.rao+test@example.com` (plus sign): rejected as invalid. Plus signs are valid in real email addresses. **BUG: valid email format wrongly rejected.**
9. **10:33** Email `ASHA.RAO@EXAMPLE.COM` (same address as in note 2, in capitals): registration succeeds, creating a second account. **BUG candidate (found during email testing; investigated later as opportunity).**
10. **10:35** Email `asha@` and `asha@example` rejected with the same generic message "Invalid email." as expected; email without `@` also rejected.
11. **10:39** Name field with an apostrophe and hyphen (`Mary-Ann O'Neil`): accepted; displayed correctly after login. Good.
12. **10:41** Name with 300 characters: accepted; the success page layout breaks, as the name overflows the welcome banner on the following page. **BUG: no maximum length on name; layout breaks.**
13. **10:43** Name with only spaces: accepted as valid. **Q: Is a blank name allowed?** Probably not, but there is no requirement text.
14. **10:44** Name with `<b>test</b>`: displayed as literal text after login (not rendered as bold). Good; handled safely as plain text.
15. **10:47** (Opportunity) Register `ASHA.RAO@EXAMPLE.COM` again: now rejected as "already exists", while the first capitalized registration was accepted. So duplicates are detected case-sensitively, yet the first case-variant was allowed. Confirms note 9.
16. **10:52** Login with the capital-letter account works; login with the lowercase account also works. Two separate accounts for what is the same email in practice.
17. **10:55** Submit button clicked twice quickly with valid new data: appears to submit once; no duplicate error. Good, but I did not test under a slow network. **IDEA: retest under throttled network.**
18. **10:57** Terms checkbox unticked: Register button still active and the form submits but displays "Please accept terms" only after the page reloads, clearing all entered fields. **BUG (usability): entered data lost when terms unchecked.**

#### Bugs found

| ID (illustrative) | Title | Severity | Evidence |
|---|---|---|---|
| BUG-1 | Password length upper bound (20 characters) not enforced: 21+ characters accepted despite on-page rule | Medium | Screenshot of page rule plus accepted 21-character password; steps noted |
| BUG-2 | Valid email with plus sign (`asha.rao+test@example.com`) rejected as invalid | Medium | Screenshot of error; steps noted |
| BUG-3 | Duplicate accounts can be created with the same email address using different letter case | High (data integrity and account security implications) | Screen recording of the two registrations and two successful logins |
| BUG-4 | A 300-character name is accepted and breaks the layout of the welcome banner after login | Low to Medium (cosmetic, but shows missing length limit) | Screenshot of the broken banner |

(A fifth item, losing entered data when the Terms box is unchecked, was recorded as a usability bug of low severity in the notes but is not counted in the four above for the purpose of this example. In practice you would log all of them.)

Severity here refers to the impact of the defect on the product and users (as covered in Tuesday's defect lifecycle lesson); priority would be decided with the team.

#### Questions and issues

1. **Q1:** Should leading and trailing spaces in passwords be trimmed, rejected, or kept as part of the password? (No requirement states this.)
2. **Q2:** Is a name consisting only of spaces allowed? What is the intended minimum and maximum length for the name field?
3. **Q3:** Should the error messages be more specific (for example, "Password must be at least 8 characters") or are generic messages a deliberate decision? The on-page claims are specific, but the error messages are generic.

#### New test ideas

1. **IDEA 1:** Test registration under a throttled network and with rapid repeated clicks to check duplicate submissions and feedback (a follow-up charter).
2. **IDEA 2:** Check whether email handling is consistent between registration and login: does login treat letter case, leading and trailing spaces, and plus signs in the same way as registration?

#### Debrief summary (using PROOF)

- **Past:** Explored the registration form for 60 minutes, covering password rules, email formats, and name inputs, plus a brief investigation of duplicate registration.
- **Results:** Four main bugs recorded (one high, two medium, one low to medium) plus one usability issue; three questions raised for the product owner; two new test ideas.
- **Obstacles:** Requirements do not state limits for name length or the treatment of spaces, so it was difficult to say definitively whether some behaviors were wrong. The generic error messages also made it hard to tell which rule caused a rejection.
- **Outlook:** Next sessions should cover the login page and its consistency with registration; a network-throttling session; and a mobile viewport session. Regression candidates: password boundary checks (7, 8, 20, 21 characters), email with plus sign, case-insensitive duplicate email check.
- **Feelings:** Moderate concern about the registration validation, especially data integrity around duplicate accounts. Fairly comfortable with the handling of special characters in names (they displayed as plain text). Not confident yet about behavior under slow networks.

Notice what made this session valuable: it had a clear charter, notes captured in time order, bugs separated from questions and ideas, time tracked honestly (including an unplanned opportunity), and a debrief tying everything back together.

### A blank session sheet template

You can copy this template for your own sessions.

```markdown
# Session Sheet

**Charter:** Explore <target> with <resources> to discover <information>

**Tester:** 
**Date:** 
**Start time:** 
**Duration:** [ ] Short (~60 min)  [ ] Normal (~90 min)  [ ] Long (~120 min)   Actual: ___ min
**Build / version:** 
**Environment (browser, OS, device):** 

## Time split (approximate % of session)
- On-charter: ___ %
- Opportunity (off-charter investigation): ___ %
- Setup / interruptions / reporting: ___ %

## Test notes (time-stamped, in order; use tags BUG: Q: IDEA: RISK:)
- 
- 
- 

## Bugs (ID, title, severity, evidence link)
| ID | Title | Severity | Evidence |
|---|---|---|---|
|   |   |   |   |

## Issues / questions
1. 
2. 

## New test ideas / regression candidates
1. 
2. 

## Debrief (PROOF)
- Past: 
- Results: 
- Obstacles: 
- Outlook: 
- Feelings: 
```

### Worked Example 2: A mini exploratory tour of an e-commerce cart

Suppose you are testing a simple online shop, and you are given this charter:

> **Explore** the shopping cart **with** a mix of quantities, products, and page navigation **to discover** problems with totals, item handling, and cart persistence.

You decide to use a **money tour** combined with **Zero-One-Many** and the **saboteur tour**. Here is a short account of what such a 30-minute exploration might look like.

| Step | What you did | What you observed | What you decided next |
|---|---|---|---|
| 1 | Opened the empty cart (**zero** items) | Message "Your cart is empty" and a link to continue shopping. Looks fine. | Add one item |
| 2 | Added **one** item at 19.99 | Cart shows 1 item, total 19.99 | Increase quantity |
| 3 | Changed quantity to 3 | Total 59.97. Correct. | Try boundaries: 0 and a negative number |
| 4 | Quantity set to 0 | Item removed from the cart. Reasonable behavior (the user would probably expect this). Noted. | Try a negative number |
| 5 | Quantity set to -1 | Total shows -19.99, and the cart accepts it. **Suspect: serious bug (negative total).** | Reproduce; capture a screenshot; test with a very large number |
| 6 | Quantity set to 9999999 | Total overflows the layout; the page scrolls horizontally. | Note a usability issue; go on to **many** items |
| 7 | Added **many** different items (20) | Cart works but page slows noticeably. | Note performance observation; try removing items |
| 8 | Removed items one at a time | After removing the last item, the total still shows 4.99 for a moment. | Refresh to see if it persists |
| 9 | Refreshed the page (saboteur-style interruption) | Cart contents persist, which is good. Total now correct. | Try opening the cart in a second tab |
| 10 | Changed quantity in tab 1, then looked at tab 2 | Tab 2 still shows the old quantity. Proceeding to checkout in tab 2 uses the old value. **Suspect bug: inconsistency across tabs.** | Verify and record. Log findings. |

Findings: a negative quantity creating a negative total (high severity, because it affects money), a layout break with huge quantities (low), a stale total after removing the last item (low), and inconsistency between tabs (medium). Questions for the team: what is the maximum quantity per item, and should multiple tabs share live cart state?

Notice the way the **tester's observations drove the next step**, and notice how several heuristics combined naturally: Zero-One-Many and Goldilocks (too small and too big) for quantities, a money tour because the total is where the business risk lies, and a touch of saboteur-style behavior (refreshing, switching tabs).

---

## Try It: Hands-On Activity

This activity has two parts. Part A adds to your Project 1 documentation. Part B gives you practice on a public site, so you can run a session even if your Project 1 application is not available.

### Part A: Write five charters for Project 1

Write five charters for Project 1 in the "Explore... with... to discover..." template. Requirements:

1. Cover at least four different targets (for example registration, login, password rules, session behavior, navigation, messages, platform).
2. Use at least three different heuristics or tours from this lesson (for example SFDIPOT, Goldilocks, Zero-One-Many, a tour) in the "with" part or as the reason for the charter.
3. Each charter should be doable in a single session of 30 to 60 minutes.
4. Test each of your charters against the four-question check: Can I finish it in one session? Do I know where to start? Is there room to follow my curiosity? Does it say what information I seek?

### Part B: Run a 30-minute session on a public practice site

Choose one of these publicly available practice sites (availability may change over time, so if one is down, pick another or ask your instructor):

- **saucedemo.com** (Swag Labs): a sample online store with a login page, product list, cart, and checkout. It publishes sample usernames and a shared password on its login page. Be aware that some of the sample users are designed to behave strangely, which is useful for exploration.
- **the-internet.herokuapp.com**: a collection of small pages that demonstrate common web behaviors, such as a login form, checkboxes, dropdowns, dynamic content, and file upload.

Note: always use practice sites as intended, do not attempt to harm them or overload them, and never enter real personal information.

**Steps:**

1. **Pick one of your charters** (or write a new one suited to the practice site, such as "Explore the login form on the practice site with invalid and unusual credentials to discover how errors and lockouts are handled").
2. **Prepare** (about 3 minutes): open the site, open browser developer tools, open your notes file or the blank session sheet template.
3. **Set a 30-minute timer** and work without interruption. Use the cycle: learn, design, execute, observe, decide.
4. **Use at least three heuristics** during the session (for example Goldilocks values, Zero-One-Many, and a HICCUPPS check on anything surprising).
5. **Take time-stamped notes**, tagging with BUG:, Q:, IDEA:, and RISK:.
6. **Capture evidence** (screenshots or a short recording) for anything suspicious.
7. **Record how time was split** between on-charter work, opportunity work, and setup or interruptions.
8. **Debrief yourself using PROOF** (Past, Results, Obstacles, Outlook, Feelings) in four to six sentences. If possible, run a short debrief with a classmate who reviews your notes and asks questions.
9. **Complete your session sheet** and, if you found something that looks like a real defect, write one bug report using the structure from Tuesday's lesson.

**What to submit or keep:**

- Your five charters.
- A completed session sheet.
- At least two new test ideas you would add to the Project 1 test-design document.
- At least one candidate for the Project 1 regression/risk plan, with a sentence about why it is important.

### Connecting back to Project 1

Add a short section named "Exploratory testing" to your Project 1 test-design document containing your five charters and a note about which sessions you plan to run and when. In the regression/risk plan, record the highest-risk areas identified by your exploration and any scripted or automation candidates it suggested. This closes the loop between exploration and your scripted test suite.

---

## Common Mistakes

1. **Treating exploratory testing as random clicking.** Without a charter and notes, you cannot show what you did or reproduce what you found.
2. **Writing charters that are too broad or too narrow.** "Test everything" cannot be completed; "enter abc and check an error appears" is a scripted test in disguise. Aim for the Goldilocks zone.
3. **Skipping notes.** If you do not write as you go, you will forget the path to the bug, and your session cannot be reviewed.
4. **Letting sessions run too long or be interrupted.** Fatigue lowers attention, and interruptions break your mental model. Use time boxes, and protect your focus.
5. **Chasing every shiny object.** Opportunity testing is fine, but if more than a small share of the session goes off-charter, write a new charter instead.
6. **Reporting every oddity as a bug without checking.** Some odd behavior is intended. Check against oracles and requirements; raise questions where you are unsure.
7. **Never reproducing before reporting.** Developers need reliable steps. Find the shortest repeatable path.
8. **Ignoring what you did not test.** Always note areas not covered, so managers do not assume more coverage than exists.
9. **Keeping findings to yourself.** If new ideas and regression candidates are never fed back into your scripted suite and risk plan, the learning is wasted.
10. **Using metrics as a scoreboard.** Counting bugs per session to rank testers encourages bad behavior and hides the real story.
11. **Treating exploratory testing as a replacement for scripted or automated testing.** They are partners. Each covers what the other does poorly.
12. **Trusting AI suggestions without verification.** Run the tests yourself, and check any claim an AI makes about the product.
13. **Exploring only the happy path.** Remember the lessons on negative testing and error guessing; many valuable discoveries come from unusual, invalid, and interrupted actions.
14. **Testing systems you are not authorized to test.** Only explore applications you have permission to test, such as your own project or designated practice sites.

---

## Practice Exercises

### Exercise 1: Turn vague missions into charters

Rewrite each vague mission as a good charter using the "Explore... with... to discover..." template.

1. "Check the login."
2. "See if the registration page is okay on phones."
3. "Make sure passwords are secure."
4. "Test error messages."
5. "Look for bugs in the account area."

**Sample answers:**

1. **Explore** the login page **with** valid, invalid, empty, and unusual credentials (spaces, capital letters, very long values) **to discover** how failed attempts are handled, whether messages are clear without revealing too much, and whether any lock-out rule applies.
2. **Explore** the registration page **on** small mobile screen sizes in the browser's device mode, in portrait and landscape orientation, **to discover** layout, readability, and usability problems when filling in and submitting the form.
3. **Explore** the password field and password rules **with** boundary lengths, character types, pasted values, and the show/hide control **to discover** whether the stated rules are enforced, and whether the way passwords are displayed, hidden, and handled in error messages could expose them.
4. **Explore** every error message on the registration and login pages **with** the invalid inputs that trigger them **to discover** unclear, inconsistent, misleading, or missing messages, using HICCUPPS to judge them.
5. **Explore** the post-login account area **with** CRUD thinking (create, read, update, delete) applied to account details **to discover** problems in how account information is displayed, changed, and removed.

### Exercise 2: Classify as scripted, exploratory, or ad-hoc

For each situation, say whether it is scripted, exploratory, or ad-hoc testing, and give a reason.

1. A tester follows a written test case, TC-014, step by step, recording pass or fail for each step.
2. A tester is given the charter "Explore the cart with extreme quantities to discover total errors," keeps timed notes, and decides each next action from what they see.
3. A developer quickly clicks around the new page for two minutes "just to see if it looks okay," without notes.
4. An automated script logs in with a fixed set of credentials and checks that the dashboard heading appears.
5. A pair of testers spends 60 minutes with a charter, one driving and one noting, then discusses the findings.
6. A tester mid-way through TC-014 notices an odd error message, sets the script aside for ten minutes to investigate it with a note about what they did, then returns to the script.

**Sample answers:**

1. **Scripted.** Pre-written steps and expected results; design and execution are separate.
2. **Exploratory.** Has a charter, notes, and test design driven by observations.
3. **Ad-hoc.** Informal, unstructured, no charter or notes.
4. **Scripted** (automated). Pre-decided checks run by a machine.
5. **Exploratory** (pair testing). Charter, time box, notes, and debrief.
6. **A mix.** The main activity is scripted, but the investigation of the odd message is exploratory. This shows that the boundaries are blurry, and that good testers explore even within scripts. A good tester would also record the finding.

### Exercise 3: Apply a heuristic

Choose a heuristic and generate at least four test ideas for a "change password" feature on Project 1.

**Sample answer (using Zero-One-Many, Goldilocks, and HICCUPPS):**

- Zero: submit with the old password, new password, and confirmation all empty.
- One: change the password once; log out; confirm that the new password works and the old one fails.
- Many: change the password several times in a row; check that old passwords do not work and that any password-history rule is applied.
- Too small: a new password of 1 and 7 characters; too big: 21 and 500 characters; just right: 8 to 20 characters.
- HICCUPPS (Product): the new password should obey the same rules as registration. Check that the rules are identical on both pages.
- HICCUPPS (Claims): any message that promises "Your password has been changed" should be true. Verify by logging in.
- Time: change the password in one browser tab while logged in elsewhere. Does the other session continue or end?

### Exercise 4: Spot the oracle

For each observation, name the HICCUPPS oracle(s) that suggest a problem.

1. The login page says "Welcome back, Asha!" but after registering with the name "Asha Rao" the welcome message on the home page shows the email address instead.
2. Registration says "Password must be 8-20 characters" but accepts a 5-character password.
3. A page that looked polished earlier now shows the message "NullReferenceException at line 42."
4. Every other form on the site trims leading spaces, but the registration form does not.

**Sample answers:**

1. **Product** (inconsistent with itself) and **User expectations**.
2. **Claims** (contradicts the stated rule).
3. **Image** (damages the professional impression) and possibly **User expectations**.
4. **Product** (inconsistent behavior within the same product), and possibly **Comparable products**.

---

## Knowledge Check

1. In one sentence, define exploratory testing.
2. Give two ways exploratory testing differs from random clicking.
3. Who is credited with coining the term "exploratory testing"? Who is associated with developing session-based test management?
4. Name three situations where exploratory testing is especially valuable and two where it is not the best choice.
5. List the steps of the exploratory testing cycle.
6. What are the three parts of Elisabeth Hendrickson's charter template?
7. Why is "Test the application" a poor charter? Why is "Enter 'abc' in the field and check an error appears" also a poor charter?
8. What is the typical length of a short, normal, and long session in SBTM?
9. What are on-charter time and opportunity time?
10. What does PROOF stand for?
11. Name two metrics used in SBTM and one caveat about using metrics.
12. What does SFDIPOT stand for?
13. Describe Zero-One-Many using a login example.
14. What is an oracle, and what does HICCUPPS help you do?
15. Explain the money tour and the back-alley tour.
16. How does exploratory testing help against the pesticide paradox?
17. What is a bug bash, and what is one thing that helps it succeed?
18. Give two cautions when using AI in exploratory testing.

**Answers:**

1. Exploratory testing is an approach in which the tester simultaneously learns about the product, designs tests, and executes them, using what they discover to guide the next step.
2. Any two of: it has a charter and goal; notes and evidence are captured; it is guided by risks, heuristics, and techniques; it can be explained and reviewed in a debrief; bugs are reproducible from notes.
3. Cem Kaner is credited with coining the term. James Bach (with Jonathan Bach) is associated with developing session-based test management.
4. Valuable: new features, thin specifications, time pressure, finding unknown risks, complementing automation, after the automated suite passes (any three). Not best: when compliance evidence with documented, traceable results is required, and for highly repetitive checks that automation can do (also, when exact expected results are needed for every step).
5. Learn, design, execute, observe, decide what to do next (then repeat).
6. Explore <target>, with <resources/tools/data>, to discover <information/risks>.
7. "Test the application" is too broad: no focus and no way to know when done. "Enter 'abc' and check an error appears" is too narrow: it is a single scripted check with a yes/no answer and no room to explore.
8. Roughly 60 minutes (short), 90 minutes (normal), and 120 minutes (long). These are conventions.
9. On-charter time is spent on the work the charter describes; opportunity time is spent investigating valuable things outside the charter that were found along the way.
10. Past, Results, Obstacles, Outlook, Feelings.
11. Any two of: number of sessions, bugs per session, charter coverage, on-charter versus opportunity percentage. Caveats: sessions are not uniform units; bugs per session is weak as a quality signal; metrics can be gamed; charter coverage is not product coverage.
12. Structure, Function, Data, Interfaces, Platform, Operations, Time.
13. Zero, one, and many failed login attempts: for example, test behavior after zero failed attempts, exactly one, and many in a row (such as five or ten), to see whether lock-out or warning rules apply correctly.
14. An oracle is a means of deciding whether behavior is right or wrong. HICCUPPS is a list of consistency oracles (History, Image, Comparable products, Claims, User expectations, Product, Purpose, Statutes) that helps you recognize and justify a problem.
15. Money tour: focus on the features that bring the most value to users or the business (for example, the complete new-customer registration and login path). Back-alley tour: visit the least-used corners of the product, such as rarely visited pages, footer links, and error pages.
16. Because each session follows a new path and produces fresh test ideas, which can be fed back into scripted suites so they do not become stale and ineffective at finding new defects.
17. A bug bash is a time-boxed event where many people explore the product and report issues. Success is helped by clear scope, instructions, a place to log bugs, and prompt triage of the reports.
18. Any two of: AI may be confidently wrong; it does not see actual product behavior unless shown; it lacks business context; do not paste confidential data; final judgment stays with the tester.

---

## Key Takeaways

- Exploratory testing means **simultaneous learning, test design, and execution**, guided by the tester's skill. It is structured and purposeful, not random clicking.
- It was named by **Cem Kaner**, and later work by **James Bach**, Jonathan Bach, and others gave us session-based test management and many heuristics.
- **Scripted, exploratory, and ad-hoc** testing differ in planning, documentation, repeatability, skill, coverage evidence, and best-fit use. Most real work blends scripted and exploratory.
- Exploratory testing shines on **new features, thin specifications, tight deadlines, unknown risks, and alongside automation.** It is a poor fit where formal evidence is required or checks are highly repetitive.
- The cycle is **learn, design, execute, observe, decide next**, repeated continuously.
- A **charter** states the mission: **Explore** <target> **with** <resources> **to discover** <information>. Aim for charters that are neither too broad nor too narrow.
- **SBTM** uses time-boxed, uninterrupted sessions, session sheets (with on-charter versus opportunity time), and **PROOF** debriefs. Metrics are conversation starters, not proof of quality.
- **Heuristics** such as SFDIPOT, CRUD, Goldilocks, Zero-One-Many, Some-None-All, tours, data type attacks, and **HICCUPPS** help you generate ideas and recognize problems.
- Capture **notes and evidence** as you go: time-stamped notes, screenshots, screen recordings, browser developer tools, mind maps, and bugs logged in Jira.
- Turn findings into **bug reports, regression and automation candidates, and new test ideas** that keep your scripted tests fresh and counter the pesticide paradox.
- Exploration can be done in **pairs, mobs, and bug bashes**, and fits Agile (end of story, sprint-level sessions, testing the increment) and CI/CD (beside the automated pipeline).
- **AI** can suggest charters, risks, and data ideas, and be a thinking partner, but it can be wrong and does not replace your observation and judgment.
- Report exploratory testing as a **story of charters, sessions, findings, risks, and what was not covered**, not just a count of bugs.

---

## Additional Resources

- **Satisfice (James Bach's site):** https://www.satisfice.com. Articles, handouts, and the Heuristic Test Strategy Model, including material on exploratory testing and session-based test management.
- **Ministry of Testing, Exploratory Testing topic:** https://www.ministryoftesting.com (search for "exploratory testing" on the site). A community site with articles, talks, and practical guidance for testers.
- **ISTQB:** https://www.istqb.org. The International Software Testing Qualifications Board publishes syllabi and glossaries that include exploratory testing and related terms.
- **Book:** *Explore It!* by Elisabeth Hendrickson, which introduced the charter template used in this lesson.
- **Practice sites:** https://www.saucedemo.com and https://the-internet.herokuapp.com (availability may change; if either is unavailable, ask your instructor for an alternative).

*Next steps:* use your charters and session notes to complete the Project 1 test-design document and the regression/risk plan, and bring your session sheet to the next review.
