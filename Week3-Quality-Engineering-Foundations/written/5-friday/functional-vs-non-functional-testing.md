# Functional vs. Non-Functional Testing

**Week 3, Friday: Advanced Testing Concepts**
**Course:** AI enabled Test Automation Engineer - QEA v1
**Applied to:** Project 1 - QE Foundations (User Registration and Login)

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define functional testing and explain what it verifies, using the vocabulary of features, business rules, data handling, and user interactions.
2. Describe the main levels and types of functional testing (unit, integration, system, smoke, sanity, acceptance, end-to-end, and API, GUI, and database functional testing), and say what each is, when it runs, who runs it, and give an example.
3. Distinguish smoke testing, sanity testing, and regression testing, and explain why they are often confused.
4. Define non-functional testing and name its major types: performance, reliability, scalability, security, usability, accessibility, compatibility, portability, installability, maintainability, localization and internationalization, compliance, disaster recovery, and observability.
5. Describe the ISO/IEC 25010 quality model and explain where functional suitability sits among the other quality characteristics.
6. Rewrite a vague quality wish such as "the system should be fast" into a measurable non-functional requirement, using SMART thinking, the Planguage idea, and Given/When/Then wording.
7. Compare functional and non-functional testing across focus, source of requirements, techniques, tools, lifecycle timing, ownership, measurability, and failure impact.
8. Explain how functional and non-functional quality interact, and why "it works but takes 30 seconds" is still a failure.
9. Tell apart test levels, test types, and test techniques, and choose non-functional tests using risk.
10. Explain how non-functional testing shifts left and fits into Agile and CI/CD quality gates, and use AI tools in this area with appropriate caution.
11. Design 10 functional and 10 non-functional test ideas for Project 1 registration and login, and run a small Python demonstration of one functional and one non-functional check.

---

## Why This Matters

Imagine you are shopping for a car. The brochure lists the features: air conditioning, a sunroof, a reversing camera, a music system. You test-sit in the car, press every button, and each one does what the brochure says. Every feature works. Then you start the engine and take it on the highway. The car shakes at 80 km/h, takes 40 seconds to reach cruising speed, the seat is painful after ten minutes, the brakes feel soft, and the doors do not lock properly. You would not buy it, even though every single feature "works".

That is the difference between **functional** and **non-functional** quality. Functional quality asks, "Does the car have the features, and does each feature do what it should?" Non-functional quality asks, "How well does the car drive? Is it safe, comfortable, reliable, and efficient?"

Software is exactly the same. A login page can accept a correct password and show the dashboard (functional success) but take 30 seconds to do it, break on a phone, leak passwords in logs, or be unusable by a person who relies on a screen reader. Real users judge the whole experience, not just whether a feature technically exists.

For you as a future Test Automation Engineer, this matters for four reasons:

- **Most serious production failures are non-functional.** Outages under load, security breaches, slow pages, and data loss after a crash are the stories that make the news. Few teams get fired because a button label was wrong; many get into trouble because the system fell over on launch day.
- **Non-functional requirements are the most often neglected.** Requirements documents list features in detail and quality expectations in a single sentence, if at all. A tester who knows how to ask the right questions adds value immediately.
- **Interviewers love this topic.** "What is the difference between functional and non-functional testing?" is one of the most common QA interview questions. After this lesson you will answer it with examples, not just definitions.
- **Your automation career depends on it.** Automating functional checks is where most engineers start, but modern teams also automate performance checks, accessibility scans, and security scans inside their pipelines. Understanding the landscape tells you what to learn next.

On Wednesday you learned that **validation** asks "Are we building the right product?" and that the **absence-of-errors fallacy** says a product with no bugs can still fail if it does not meet users' needs. Today's lesson is where that idea becomes concrete: a system can pass every functional test and still be the wrong product because of how it behaves.

---

## The Concept

### 1. Two Big Questions

Every test you will ever write answers one of two big questions, or sometimes both:

| Question | Name | Car analogy |
|---|---|---|
| **What** does the system do? | Functional | The car has air conditioning, and pressing the button makes the air cool. |
| **How well** does the system do it? | Non-functional | The air conditioning cools the cabin from 40 degrees to 24 degrees within five minutes and does not rattle. |

Hold on to this simple picture. The rest of the lesson fills in detail.

### 2. Functional Testing Defined

**Functional testing** is testing that verifies that the system's functions behave according to the **functional requirements**. A **function** is something the system does: an action, a calculation, a rule, a response to a user or to another system. A **functional requirement** is a written statement of such a thing, for example, "The system shall allow a visitor to register with a unique email address and a password of at least 8 characters."

Functional testing focuses on four broad areas:

1. **Features.** The things the product offers, such as registration, login, password reset, and logout.
2. **Business rules.** The rules the organization wants enforced, such as "an email address can be used for only one account" or "an account locks after five failed login attempts."
3. **Data handling.** How information is captured, validated, stored, changed, retrieved, and displayed. Functional tests absolutely check data: that the record saved to the database matches what the user typed, that a calculation is right, that trailing spaces are trimmed as specified. (This is a common misconception we will return to: functional testing is not only about clicking buttons.)
4. **User interactions.** How the system responds to what users do: clicking, typing, selecting, navigating, submitting, cancelling, and going back.

Functional testing is mostly done as **black-box testing** (you test inputs and outputs without needing to see the code), which is why the techniques you learned on Thursday (equivalence partitioning, boundary value analysis, decision tables, state transition testing, error guessing, use-case testing) are the core toolkit for functional test design. White-box testing, which you studied earlier today, also contributes to functional verification at the unit level, where developers check code paths against intended behavior.

A functional test generally has a **clear expected result** that can be judged as pass or fail: "After entering a valid email and password and clicking Register, the system shows the message 'Registration successful' and a new user record exists."

### 3. Levels and Types of Functional Testing

Functional testing is not one activity. It is carried out at different **levels** (how big a piece of the system is under test) and in different **types** (what particular purpose the test serves). Let us walk through the important ones.

#### 3.1 Unit Testing

A **unit** is the smallest testable piece of code, usually a function or a method. **Unit testing** checks a unit in isolation. In Project 1, a unit might be a function `is_valid_email(text)` that returns True or False. Developers usually write unit tests (often before or alongside the code), and they run in milliseconds. As a test automation engineer, you will often review unit test coverage and sometimes write unit tests yourself.

#### 3.2 Integration Testing

**Integration testing** checks that separate units or components work correctly **together**. Each piece may pass its own unit tests and still fail when connected, because of mismatched data formats, wrong assumptions, or timing problems. In Project 1, an integration test might confirm that when the registration form component sends data to the user service, the service saves it to the database and returns the correct response. Integration testing can be done in steps: **incremental** (adding components one by one) or **big bang** (connecting everything at once, which makes defects harder to locate).

#### 3.3 System Testing

**System testing** checks the **complete, integrated system** against the specified requirements, in an environment that resembles production. It looks at the product as a whole, as a black box. In Project 1, system testing covers the whole registration and login application: forms, server, database, and email service together. System testing is typically performed by an independent QA team. Importantly, system testing includes both functional and non-functional checks; the "functional system testing" part is what we discuss here.

#### 3.4 Smoke Testing

**Smoke testing** is a quick, shallow set of tests run on a new build to confirm that the **most critical functions work** and that the build is stable enough for deeper testing. The name comes from hardware: switch the device on, and if smoke comes out, there is no point testing further. In software, a smoke test for Project 1 might be: "The application opens, the registration page loads, a valid user can log in, and the dashboard appears." If any of these fail, the build is rejected and sent back. A smoke test is **broad and shallow**, usually automated, and run on every new build.

#### 3.5 Sanity Testing

**Sanity testing** is a quick, **narrow and focused** check, usually performed after a small change or bug fix, to confirm that the change works and has not obviously broken closely related behavior. If a developer fixes "password with a space is wrongly accepted", the tester performs a sanity check on the password rules and the registration flow around it, rather than running the entire suite. Sanity testing is **narrow and deeper in one area**, often (though not always) manual, and decides whether it is worth proceeding to more thorough testing of that build.

#### 3.6 Acceptance Testing

**Acceptance testing** checks whether the system meets the needs of the business and users and is **ready to be accepted** (released or delivered). It answers the validation question: "Is this the right product for us?" Common forms:

- **User Acceptance Testing (UAT):** Real users or business representatives run realistic scenarios in a production-like environment to decide whether to accept the system. For Project 1, a product owner and sample users try to register and log in following real-life scenarios.
- **Alpha testing:** Acceptance-style testing performed **inside the organization** (by staff who are not on the development team, or by an independent test group) before the product goes to outside users. It happens at the developer's site or an internal environment.
- **Beta testing:** Testing performed by a **limited group of real external users** in their own environments, before the general release. Feedback about defects and usability is collected from real conditions. Many apps you use have had a "beta" period.
- Other forms include **operational acceptance** (is it ready to run and be supported, including backups and recovery?), **contractual acceptance** (does it meet contract criteria?), and **regulatory acceptance** (does it meet laws and regulations?).

#### 3.7 End-to-End (E2E) Testing

**End-to-end testing** verifies a complete user journey from start to finish through all the systems involved, simulating real usage. For Project 1: a new visitor opens the site, registers, receives a confirmation email, clicks the verification link, logs in, views the dashboard, and logs out. The test crosses the user interface, the server, the database, and the email service. E2E tests are valuable because they reflect what users actually do, but they are slower and more fragile than lower-level tests, so teams use them sparingly for the most important journeys.

#### 3.8 API, GUI, and Database Functional Testing

Functional testing can also be classified by **where** you test:

- **GUI (Graphical User Interface) functional testing** exercises the system through its screens, as a user would: typing into fields, clicking buttons, checking messages. It is the most realistic but also the slowest and most fragile layer.
- **API (Application Programming Interface) functional testing** sends requests directly to the application's interfaces (for example, an HTTP request to a `/register` endpoint) and checks the responses (status codes, response body, headers). It is faster and more stable than GUI testing, and it can test business rules without needing a screen. You will do a lot of this in later weeks.
- **Database functional testing** checks the data layer: that records are created, updated, and deleted correctly; that constraints (such as a unique email) are enforced; that stored data matches what the application showed; and that sensitive data (such as passwords) is stored in the right form, for example hashed rather than as plain text.

#### 3.9 The Summary Table: What / When / Who / Example

| Level or type | What it checks | When it runs | Who usually does it | Project 1 example |
|---|---|---|---|---|
| **Unit** | One function or method in isolation | While coding, on every code commit | Developers (sometimes SDETs) | `is_valid_email("a@b.com")` returns True; `is_valid_email("a@b")` returns False |
| **Integration** | Components working together | After units are ready, on every integration or merge | Developers and test engineers | Registration service saves the user to the database and returns "created" |
| **System** | The whole integrated system against requirements | When a complete build is available in a test environment | Independent QA/test team | Run all registration and login requirements through the full application |
| **Smoke** | Critical functions work; build is testable | On every new build or deployment | Automated pipeline, QA | App loads; a valid user can log in; dashboard appears |
| **Sanity** | A specific change or fix works and nearby behavior is intact | After a small fix or change | QA tester | After a password-rule bug fix, recheck password rules and registration |
| **Acceptance (UAT)** | The system meets business needs and is ready to accept | Near the end, before release | Business users, product owner, customers | Product owner registers and logs in using realistic scenarios and signs off |
| **Alpha** | Early acceptance feedback inside the organization | Before beta | Internal staff outside the dev team | Employees from other departments use the pre-release app |
| **Beta** | Real-world feedback from a limited external group | Before general release | Selected real external users | 200 volunteer users register using their own devices and report issues |
| **End-to-end** | A full user journey across all components | When the full system is available; for critical journeys | QA/automation engineers | Register, verify email, log in, view dashboard, log out |
| **GUI functional** | Behavior through the user interface | When the UI is ready | QA/automation engineers | Fill in the registration form and check the on-screen success message |
| **API functional** | Behavior through application interfaces | As soon as the API exists, often before the UI | QA/automation engineers, developers | POST to `/register` with a duplicate email returns a 409 conflict style error |
| **Database functional** | Correctness, integrity, and rules of stored data | With integration and system testing | QA, developers, data testers | After registration, exactly one user row exists with a hashed password |

#### 3.10 Smoke vs. Sanity vs. Regression

These three are among the most confused terms in testing. A clear way to separate them is by **purpose, scope, and trigger**.

| | Smoke testing | Sanity testing | Regression testing |
|---|---|---|---|
| **Purpose** | Is this build stable enough to test at all? | Does this specific fix or small change work, and is the nearby area sensible? | Did the change break anything that worked before? |
| **Scope** | Broad and shallow: the most critical functions | Narrow and deep: one area or feature | Wide: previously working functionality (full or selected suite) |
| **Trigger** | Every new build or deployment | A small change, patch, or bug fix | Any change to code, configuration, or environment |
| **Typically** | Automated, fast (minutes) | Often manual, targeted | Largely automated, can be long |
| **Outcome** | Accept or reject the build for further testing | Proceed or return to developers for more fixing | Confidence that existing behavior is preserved |
| **Analogy** | Turn the car's key: does the engine start? | After the mechanic fixes the brake light, does the brake light work (and do the brakes still feel right)? | After any repair, take the car through a full checklist of everything that used to work |

A useful memory trick: **smoke is "wide and shallow", sanity is "narrow and deep", regression is "wide and thorough"**. Regression testing is a big topic of its own and has its own lesson later today, so we will not go deeper here.

### 4. Non-Functional Testing Defined

**Non-functional testing** verifies **how well** the system performs its functions: the **quality attributes** (also called quality characteristics, "-ilities", or **non-functional requirements, NFRs**) such as speed, security, usability, reliability, and compatibility. It does not ask "does the login work?" It asks "how fast is the login, how secure is it, who can use it, on which devices, and what happens when things go wrong?"

Some key points that help beginners:

- Non-functional requirements describe **qualities and constraints**, not features. "The system shall let users reset a password" is functional. "Password reset emails shall arrive within 60 seconds in 99% of cases" is non-functional.
- Non-functional tests are usually **measurable**: you can attach numbers (seconds, percentages, counts) and compare them with thresholds.
- Non-functional testing often needs **special tools, environments, and skills**: load generators, security scanners, accessibility checkers, and device labs.
- The failures are often **systemic**: they affect everyone at once (the entire site is slow) rather than one user flow.
- The name "non-functional" is a little unfortunate, because it sounds like "not important". It is not. Many practitioners prefer the phrase **quality attributes** or "how well" requirements. Whatever it is called, it is not optional.

### 5. A Tour of Non-Functional Test Types

Here is a guided tour. For each type you will see the definition, the goal, a Project 1 example, typical measures, and example tools. **Tools are mentioned by name only; you do not need to learn them today.** We also point to lessons later today that give a fuller treatment of some types.

#### 5.1 Performance Testing

**Definition:** Testing how the system behaves in terms of speed, responsiveness, and resource usage under a given workload.
**Goal:** Make sure the system is fast enough and uses resources sensibly for the expected number of users.

Performance testing is a family:

| Sub-type | What it does | Project 1 example |
|---|---|---|
| **Load testing** | Applies the **expected** normal and peak load to see if targets are met | 500 users log in over 10 minutes; check response times |
| **Stress testing** | Pushes the load **beyond** limits to find the breaking point and see how the system fails and recovers | Keep increasing login traffic until errors appear; does it recover gracefully? |
| **Spike testing** | Hits the system with a sudden, sharp increase in load | 5,000 users try to log in within 30 seconds after a marketing email |
| **Endurance (soak) testing** | Runs a normal load for a **long time** to reveal leaks and slow degradation | Run 200 logins per minute for 24 hours; does memory keep growing? |
| **Volume testing** | Tests with a large **amount of data** | Registration database holds 10 million users; do searches and logins still work? |

**Typical measures:** response time (average and percentiles such as the 95th percentile), throughput (requests per second), error rate, CPU and memory use, number of concurrent users.
**Example tools (names only):** Apache JMeter, k6, Gatling, Locust.
**Pointer:** Performance and stress testing have their own lesson today, so we will keep this at overview level here.

#### 5.2 Reliability, Availability, and Recoverability Testing

**Definitions:**
- **Reliability** is the ability of the system to perform its required functions without failure for a specified time under specified conditions.
- **Availability** is the proportion of time the system is up and usable (for example, 99.9% availability allows roughly 8.8 hours of downtime per year).
- **Recoverability** is the ability to restore normal operation and data after a failure, and how quickly.

**Goal:** Make sure the system keeps working, and if it does fail, comes back quickly without losing data.
**Project 1 example:** Restart the authentication service during a login; the user should see a clear retry message, and no half-created accounts should remain. After the service restarts, logins work again within 2 minutes.
**Typical measures:** mean time between failures (MTBF), mean time to repair or recover (MTTR), uptime percentage, failure rate.
**Tools (names only):** chaos engineering tools such as Chaos Monkey, monitoring platforms such as Prometheus and Grafana, plus custom scripts.
**Pointer:** Reliability has its own lesson today.

#### 5.3 Scalability Testing

**Definition:** Testing the system's ability to handle growth, either more users and data or more resources added to cope with them.
**Goal:** Know how performance changes as load increases, and whether adding servers (scaling out) or bigger servers (scaling up) actually helps.
**Project 1 example:** Run the login test at 100, 200, 400, and 800 users, adding a second server instance at each step. Does response time stay within target?
**Typical measures:** response time and throughput versus load; resource use per user; the point at which adding resources stops helping.
**Tools (names only):** The same load tools as performance testing (JMeter, k6, Gatling, Locust), together with cloud autoscaling dashboards.
**Pointer:** Scalability is covered in the reliability/scalability lesson today.

#### 5.4 Security Testing

**Definition:** Testing that the system protects data and functionality from unauthorized access, misuse, and attack, and that it keeps its promises about confidentiality, integrity, and availability.
**Goal:** Reduce the risk of breaches, data theft, and fraud.

Security testing is especially important for registration and login, because these pages are the front door of the system. Conceptual areas to know:

- **Authentication:** Verifying that users are who they claim to be. Does login require correct credentials? Are weak passwords rejected? Is the number of failed attempts limited? Is there protection against automated guessing?
- **Authorization:** Verifying that authenticated users can only do what they are permitted to do. Can a normal user reach an administrator page by changing the web address?
- **Input validation:** Verifying that the system treats all input as untrusted and rejects or safely handles malformed, oversized, or unexpected input, so the input cannot be used to manipulate the system.
- **Session handling:** Verifying that after login, the "session" (the system's memory that you are logged in) is created securely, expires after inactivity, ends on logout, and cannot be reused by someone else.
- **Data protection:** Verifying that sensitive data is protected in transit (encrypted connections such as HTTPS) and at rest (passwords stored hashed, not as readable text), and is not leaked in error messages or logs.

**OWASP Top 10 (names only):** The **Open Worldwide Application Security Project (OWASP)** publishes a well-known awareness list of the most critical web application security risks, called the **OWASP Top 10**. It includes categories such as broken access control, cryptographic failures, injection, insecure design, security misconfiguration, vulnerable and outdated components, identification and authentication failures, software and data integrity failures, security logging and monitoring failures, and server-side request forgery. Categories and ordering change between editions, so always check the current list on the OWASP website. In this course we study these at the level of names and ideas; we do not practise attacks.

**Typical measures:** number and severity of vulnerabilities found, compliance with security checklists, time to fix.
**Project 1 conceptual examples:** After five failed logins the account is temporarily locked; passwords are never visible in logs; the session ends after 15 minutes of inactivity; the login page is only available over HTTPS.
**Tools (names only):** OWASP ZAP, Burp Suite, static analysis tools such as SonarQube, dependency scanners such as OWASP Dependency-Check.

#### 5.5 Usability Testing

**Definition:** Testing how easily, efficiently, and satisfyingly real users can accomplish their goals with the system.
**Goal:** Ensure the system is easy to learn and pleasant to use, with few user errors.
**Project 1 example:** Five first-time users try to register; at least four complete registration without help in under 90 seconds; error messages tell users exactly how to fix the problem.
**Typical measures:** task completion rate, time on task, number of errors, satisfaction scores (such as the System Usability Scale, SUS).
**Tools (names only):** Moderated sessions with screen recording, UserTesting, Hotjar for behavior recordings, simple surveys. Much usability testing is manual and human-centered.

#### 5.6 Accessibility Testing

**Definition:** Testing that people with disabilities, such as people who are blind, have low vision, are deaf or hard of hearing, have motor impairments, or have cognitive differences, can perceive, understand, navigate, and interact with the system.
**Goal:** Make the system usable by everyone, and meet accessibility standards and laws.
**Standard:** The **Web Content Accessibility Guidelines (WCAG)**, published by the World Wide Web Consortium (W3C), are the widely used international standard. They are organized around four principles, remembered as **POUR**: Perceivable, Operable, Understandable, Robust. Conformance is described in levels A, AA, and AAA; many organizations and laws target level AA.
**Project 1 example:** A user who cannot use a mouse can complete registration using only the keyboard; a screen reader announces each field label and each error message.

**Quick manual accessibility checklist for the registration and login pages:**

1. **Keyboard navigation:** Put the mouse aside. Can you reach every field, link, and button with the Tab key, in a logical order? Can you submit with Enter? Is there a visible focus outline showing where you are? Can you leave every element (no "keyboard trap")?
2. **Screen reader:** Turn on a screen reader (such as NVDA or VoiceOver) and listen. Does every field have a label that is read aloud ("Email address, edit text")? Are error messages announced? Are images given meaningful alternative text (or marked decorative)?
3. **Color contrast:** Is text sufficiently different in brightness from its background? WCAG AA asks for a contrast ratio of at least 4.5:1 for normal text. Is information conveyed by color alone (for example, a red border as the only error signal)? It should also have text or an icon.
4. **Text size and zoom:** Can the page be zoomed to 200% without losing content or function?
5. **Labels and instructions:** Are fields labeled visibly, not only with placeholder text that disappears? Are required fields indicated by more than color?
6. **Error handling:** Are errors described in text, tied to the field, and easy to find?
7. **Page structure:** Does the page have a clear title and headings in a sensible order?

**Typical measures:** number of WCAG success criteria passed, count of automated-tool violations, results of manual checks.
**Tools (names only):** axe (axe DevTools), Lighthouse, WAVE, Pa11y, plus screen readers NVDA, JAWS, and VoiceOver.

Automated tools catch only a portion of accessibility problems (often cited as roughly a third to a half), so manual checks like the above remain essential.

#### 5.7 Compatibility Testing

**Definition:** Testing that the system works correctly across the different environments in which users will use it.
**Goal:** Avoid "works on my machine" surprises.
**Dimensions to cover:**
- **Browsers** and versions (Chrome, Firefox, Safari, Edge).
- **Devices** (desktop, laptop, tablet, phone of different makes).
- **Operating systems** (Windows, macOS, Linux, Android, iOS) and versions.
- **Screen sizes and resolutions**, plus orientation (portrait or landscape).
- Sometimes **network conditions** (slow mobile connection) and **assistive technologies**.

**Project 1 example:** The registration form displays properly and works on the latest two versions of Chrome, Firefox, Safari, and Edge, and on screens from 360 pixels wide (small phone) to 1920 pixels wide (desktop).
**Typical measures:** a compatibility matrix with pass or fail for each combination; number of defects by environment.
**Tools (names only):** BrowserStack, Sauce Labs, LambdaTest, browser developer tools device emulation, Selenium Grid and Playwright for running across browsers.

Because testing every possible combination is impossible (remember the principle that exhaustive testing is impossible), teams use usage analytics to pick the most important combinations. This is risk-based thinking again.

#### 5.8 Portability Testing

**Definition:** Testing how easily the software can be moved from one environment to another (different operating systems, platforms, cloud providers, or database engines) and still work.
**Goal:** Reduce lock-in and migration pain.
**Project 1 example:** The application runs the same on the Linux test server and on the cloud-hosted staging environment, and can switch from one database engine to another through configuration only.
**Measures:** effort (hours) to move; number of environment-specific defects; percentage of tests passing in the new environment.
**Tools (names only):** Docker and containers, virtual machines, configuration management tools.

#### 5.9 Installability Testing

**Definition:** Testing that the software can be installed, upgraded, and uninstalled successfully in the supported environments.
**Goal:** Make sure users and operations teams can get the product running without problems.
**Project 1 example:** If Project 1 ships as a mobile app, the app installs from the store in a supported device, upgrades from the previous version without losing the user's login state or data, and uninstalls cleanly. For a web app, the equivalent is deploying a new release to the server and rolling it back.
**Measures:** installation success rate; install time; number of steps; whether upgrade preserves data.
**Tools (names only):** Installer test scripts, device farms, deployment pipeline tools.

#### 5.10 Maintainability Testing

**Definition:** Assessing how easily the software can be understood, changed, corrected, and extended. In practice this is evaluated through code and design reviews, static analysis, and measuring how hard changes are.
**Goal:** Keep the cost and risk of future changes low.
**Project 1 example:** Static analysis reports show low code complexity in the password validation module; a small rule change (increase minimum length to 10) requires a change in only one place and the automated tests tell the team immediately if something breaks.
**Measures:** cyclomatic complexity (a count of independent code paths, which you met in white-box testing), code duplication percentage, test coverage, time to fix a typical defect.
**Tools (names only):** SonarQube, linters such as ESLint or pylint, code review tools.

Maintainability applies to **test code** as well. Automation scripts that are hard to change become a burden quickly. You will learn design patterns for maintainable automation in later weeks.

#### 5.11 Localization and Internationalization Testing

**Definitions:**
- **Internationalization (often written i18n)** is designing the software so it *can* support multiple languages, regions, and cultures without code changes (for example, text is kept in language files rather than hard-coded).
- **Localization (l10n)** is adapting the software for a *specific* language and region: translated text, date and number formats, currency, time zones, and cultural conventions.

**Goal:** Make the product correct and comfortable for users everywhere it is offered.
**Project 1 example:** The registration page in Spanish shows all labels and errors in Spanish; date of birth appears in day/month/year format for regions that use it; names with accents and non-Latin characters (such as "Jose", "Zoe", or names in other scripts) are accepted and shown correctly; right-to-left languages such as Arabic lay out properly.
**Measures:** number of untranslated or truncated strings; correct format checks; character set support.
**Tools (names only):** Pseudo-localization tools, translation management platforms, native-speaker reviews.

#### 5.12 Compliance Testing

**Definition:** Testing that the system meets the relevant laws, regulations, standards, and contractual or internal policies.
**Goal:** Avoid legal penalties, lost certifications, and loss of trust.
**Project 1 example:** Because registration collects personal data (email, possibly name), the application should follow privacy rules: it explains what data is collected, obtains consent where required, allows users to request deletion of their data, and does not store more than needed. Privacy laws you may hear about, **named here only so you recognize them**, include the **GDPR** (General Data Protection Regulation, European Union), the **CCPA/CPRA** (California), and sector rules such as **HIPAA** (US health data) and **PCI DSS** (payment card industry standard). This lesson is not legal advice; in real projects, compliance questions are decided with legal and compliance specialists, and testers verify the resulting requirements.
**Measures:** checklist items satisfied; audit findings.
**Tools (names only):** Compliance checklists, audit and governance platforms, data discovery tools.

#### 5.13 Disaster Recovery Testing

**Definition:** Testing the ability to restore the system and its data after a major disruption such as a data center outage, serious data corruption, or a cyber-attack.
**Goal:** Meet the recovery targets the business has defined, usually described by two numbers: the **Recovery Time Objective (RTO)**, how long the business can accept being down, and the **Recovery Point Objective (RPO)**, how much recent data the business can accept losing.
**Project 1 example:** The primary database is lost. The team restores from backup into a secondary environment within the 4-hour RTO, with no more than 15 minutes of registrations lost (RPO).
**Measures:** actual recovery time versus RTO; actual data loss versus RPO; success of backup restores.
**Tools (names only):** Backup and restore tools, failover tooling from cloud providers, scheduled disaster recovery drills.

#### 5.14 Observability and Logging Testing

**Definition:** **Observability** is how well you can understand what is happening inside a running system from the outside, using its **logs** (records of events), **metrics** (numbers over time), and **traces** (the path of a request through components). Observability testing checks that these signals are produced, are accurate, and are useful, without exposing sensitive data.
**Goal:** Detect and diagnose problems quickly in production.
**Project 1 example:** Every failed login writes a log entry with a timestamp, a request identifier, and the reason code, but never the password; a dashboard shows the login success rate; an alert fires when failures exceed a threshold.
**Measures:** presence and correctness of log entries; alert accuracy; time to detect an incident.
**Tools (names only):** ELK stack (Elasticsearch, Logstash, Kibana), Prometheus, Grafana, OpenTelemetry, Datadog.

### 6. The Quality Model: ISO/IEC 25010

You have just toured more than a dozen non-functional types. Is there an agreed way to organize them? Yes. **ISO/IEC 25010** is an international standard in the SQuaRE family (Systems and software Quality Requirements and Evaluation) that defines a **product quality model**: a structured list of characteristics that describe the quality of a software product. Testers use it as a checklist so that no quality area is forgotten.

The 2011 edition lists **eight** product quality characteristics, each with sub-characteristics. A later edition (2023) refined the model, adding "safety" and renaming some characteristics, so check the current version of the standard when you need precise wording. The eight classic characteristics are:

| Characteristic | Plain-language meaning | Sub-characteristics (names) |
|---|---|---|
| **Functional suitability** | Does the system provide functions that meet stated and implied needs? | Functional completeness, functional correctness, functional appropriateness |
| **Performance efficiency** | How well does it perform relative to the resources used? | Time behavior, resource utilization, capacity |
| **Compatibility** | Can it exchange information and work alongside other systems and in shared environments? | Co-existence, interoperability |
| **Usability** | How easy and pleasant is it to use? | Appropriateness recognizability, learnability, operability, user error protection, user interface aesthetics, accessibility |
| **Reliability** | Does it perform consistently under stated conditions? | Maturity, availability, fault tolerance, recoverability |
| **Security** | Does it protect information and data? | Confidentiality, integrity, non-repudiation, accountability, authenticity |
| **Maintainability** | How easily can it be modified? | Modularity, reusability, analysability, modifiability, testability |
| **Portability** | Can it be moved between environments? | Adaptability, installability, replaceability |

**How functional suitability fits:** Notice that **functional suitability is one of the eight characteristics, not a separate world**. Functional testing is therefore testing of one quality characteristic, an essential one. The other seven are the "non-functional" characteristics in everyday language. This is a helpful mental shift: functional quality is *one part of quality*, not the whole thing. Inside functional suitability, even the sub-characteristics show the idea: **completeness** (are all the needed functions present?), **correctness** (do they give right results?), and **appropriateness** (do the functions help users achieve their goals?). Also notice that accessibility sits inside usability, installability sits inside portability, and testability sits inside maintainability. The standard also has a separate "quality in use" model describing outcomes for users, such as effectiveness, efficiency, satisfaction, and freedom from risk.

Mapping our tour to ISO/IEC 25010: performance, scalability, and volume relate to performance efficiency; reliability, availability, and disaster recovery relate to reliability; security stays security; usability and accessibility relate to usability; compatibility stays compatibility; portability and installability relate to portability; maintainability stays maintainability. Localization, compliance, and observability are widely tested in practice, though they do not map neatly to a single characteristic; they are often treated as cross-cutting concerns.

### 7. Writing Measurable Non-Functional Requirements

The most useful skill in this lesson may be this one. Non-functional requirements are usually written vaguely, and vague requirements cannot be tested. A requirement is **testable** only if two testers would independently reach the same pass or fail verdict.

#### 7.1 Bad vs. Good

| Vague (bad) | Why it fails | Measurable (good) |
|---|---|---|
| "The system should be fast." | "Fast" means different things to different people. No scenario, no number. | "95% of login requests shall respond within 2 seconds under 500 concurrent users." |
| "The system must be secure." | Which threats? How would we know? | "Passwords shall be stored using a salted, slow hashing algorithm; accounts shall lock for 15 minutes after 5 consecutive failed logins; all traffic shall use HTTPS." |
| "The site should be easy to use." | "Easy" is subjective. | "At least 90% of first-time test users shall complete registration without assistance in under 2 minutes." |
| "The system should always be available." | "Always" is impossible and untestable. | "The login service shall be available 99.9% of each calendar month, excluding planned maintenance windows." |
| "It should work on all devices." | "All" is unbounded. | "The registration page shall render and function correctly on the latest two major versions of Chrome, Firefox, Safari, and Edge, at widths from 360 to 1920 pixels." |

#### 7.2 The SMART Idea

You may have met **SMART** goals before. Applied to requirements, a good non-functional requirement is:

- **Specific:** names exactly what is being measured (login response time, not "speed").
- **Measurable:** includes a number and a unit.
- **Achievable:** possible with the technology and budget.
- **Relevant:** matters to users or the business.
- **Time-bound or Testable under stated conditions:** says under what load, data, environment, or period it applies.

Notice how the good performance example above has all of these: login (specific), 95% within 2 seconds (measurable), 500 concurrent users (conditions), a number the team believes feasible (achievable), and obviously relevant to users.

#### 7.3 The Planguage Idea

**Planguage** (Planning Language) is a method created by Tom Gilb for specifying quality requirements in a structured, quantified way. You do not need to master it today. The idea is that every quality requirement can be described by a few standard parts:

- **Tag:** a short name (for example, Login.ResponseTime).
- **Scale:** the unit of measurement ("seconds from clicking Login to the dashboard being displayed").
- **Meter:** how it will be measured ("timing in the load-test tool, measured at the server and the browser").
- **Past:** the current or previous level ("3.5 seconds").
- **Must:** the minimum acceptable level ("no worse than 3 seconds").
- **Plan:** the target level ("2 seconds").
- **Wish:** the ideal level ("1 second").

Even if you use only Scale, Meter, Must, and Plan, you force the conversation from "fast" to a concrete number and a way to check it. That is exactly what testers need.

#### 7.4 Given/When/Then for NFRs

In Agile teams, acceptance criteria are often written in the **Given/When/Then** style (from behavior-driven development): *Given* a starting context, *When* an action happens, *Then* an outcome is observed. This works for non-functional requirements too, as long as the "Then" includes a measurable condition.

> **Given** 500 registered users are logged in and active,
> **When** another user submits valid login credentials,
> **Then** the dashboard is displayed within 2 seconds in at least 95% of attempts.

> **Given** a user's account has had 5 consecutive failed login attempts,
> **When** the user tries a 6th time with the correct password within 15 minutes,
> **Then** the login is refused with the message "Account temporarily locked" and a security log entry is recorded.

> **Given** a user who navigates only with the keyboard,
> **When** they open the registration page and press Tab repeatedly,
> **Then** focus moves through every field and button in a logical order and a visible focus indicator is always shown.

These are written so both a person and an automation script can judge pass or fail.

### 8. The Detailed Comparison

Here is the master comparison table you can keep as a revision sheet.

| Aspect | Functional testing | Non-functional testing |
|---|---|---|
| **Focus** | What the system does: features, rules, data, interactions | How well the system does it: quality attributes |
| **Question answered** | "Does it work as specified?" | "Does it work well enough, safely, and under real conditions?" |
| **Requirements source** | Functional requirements, user stories, use cases, business rules | Non-functional requirements, quality standards, service level agreements, regulations, user expectations (often implicit and must be elicited) |
| **Techniques** | Black-box techniques: equivalence partitioning, boundary value analysis, decision tables, state transition, use-case testing, error guessing; white-box at unit level | Load and stress modeling, benchmarking, threat modeling, vulnerability scanning, heuristic evaluation, compatibility matrices, checklists, monitoring and analysis |
| **Tools** | Test management tools, Selenium, Playwright, Cypress, API tools such as Postman, unit test frameworks such as pytest and JUnit | JMeter, k6, Gatling, OWASP ZAP, axe, Lighthouse, BrowserStack, Prometheus, Grafana |
| **When in lifecycle** | At every level from unit to acceptance; starts early with the first code | Some at design time (architecture, security design), many once a stable, integrated, production-like system exists; ideally some checks run continuously |
| **Who** | Developers (unit/integration), testers (system), business users (acceptance) | Specialists plus the whole team: performance engineers, security testers, accessibility specialists, DevOps/SRE, UX researchers; testers coordinate |
| **Measurability** | Usually binary: pass or fail against expected result | Usually numeric: measured against thresholds, trends, and percentiles |
| **Failure impact** | A feature fails or gives wrong results for some users or flows | Possibly the whole system degrades, crashes, is breached, or excludes users; often higher business and legal impact |
| **Example (Project 1)** | Entering a duplicate email shows "Email already registered" | Under 500 concurrent users, 95% of logins respond within 2 seconds |

A warning: the table makes the two sides look cleanly separated, but in practice they overlap and depend on each other, as the next section explains.

### 9. How Functional and Non-Functional Quality Interact

#### 9.1 A Feature That Works But Takes 30 Seconds Is a Failure

Suppose a login passes every functional test: right password gets in, wrong password is refused with the correct message. But in real use it takes 30 seconds. From the user's point of view, the login is **broken**. Most users abandon a page that takes more than a few seconds. No functional test fails, yet the business loses customers. This is the **absence-of-errors fallacy** from Wednesday: finding and fixing all the functional defects does not make the system useful if the system does not satisfy users' needs, and speed is one of those needs. It is also the **validation** question ("Are we building the right product?") in action: users need a login that is quick, not merely correct.

#### 9.2 They Depend on Each Other

- **A non-functional failure can look like a functional failure.** Under heavy load, a login request may time out and the user sees an error. The same feature that passed alone fails under load. The root cause is non-functional (capacity), but the symptom is functional (login failed).
- **A functional fix can cause a non-functional problem.** A developer adds a database check to prevent duplicate emails (functional fix) but forgets an index, so registration slows dramatically as the user table grows (performance problem).
- **Security is functional and non-functional at once.** "A user can log in only with a correct password" is a functional rule; "the system resists password-guessing attacks" is a non-functional quality.
- **Accessibility affects whether functions can be used at all.** If a button cannot be reached by keyboard, the function exists but is unavailable to some users.

#### 9.3 One Test, Two Lenses

You can often use one test scenario and look through both lenses. Take "register a new user". Functionally: is the account created with the right data? Non-functionally: how long did it take, was the connection encrypted, was the form usable with a screen reader, did it work on a phone? Good testers learn to add the second set of questions every time.

#### 9.4 Non-Functional Quality Is Easier to Break Than to Rescue

Retrofitting quality is expensive. An architecture chosen without thinking about security or scale can be very costly to change after launch. This leads us to shift-left.

### 10. Shift-Left for Non-Functional Requirements

**Shift-left** means moving testing and quality activities earlier in the lifecycle (to the "left" on a timeline), because defects found earlier are cheaper to fix. This applies strongly to non-functional qualities, which are traditionally left to a late "performance test phase" when it is too late to change the design.

Examples of shifting NFRs left:

- **Performance budgets.** Agree early on limits, such as "the registration page must load in under 2 seconds on a typical 4G connection and must not exceed 500 KB of resources." Check them automatically on every build, and fail the build if the budget is exceeded.
- **Security in design (threat modeling).** During design, ask "what could go wrong, and how do we prevent it?" Choose secure approaches (such as hashed passwords and limited login attempts) before coding. Add static security analysis and dependency scanning to the developers' routine.
- **Accessibility linting.** Developers can use automated accessibility checks in the code editor and in the build pipeline, so that a missing label or low contrast is flagged while the code is being written, not after release.
- **Review requirements for testability.** In requirements analysis (Tuesday's topic), testers ask "what does 'fast' mean here?" and get numbers agreed up front.
- **Early, small performance checks.** Time a critical function or API call in a small test long before the full load test is possible. The Python demonstration later in this lesson is a tiny example of this idea.
- **Observability from the start.** Build logging and metrics into features as they are written, not as an afterthought.

### 11. Test Levels vs. Test Types vs. Test Techniques

Beginners often use these three words interchangeably. They answer three different questions.

| Concept | Question it answers | Meaning | Examples |
|---|---|---|---|
| **Test level** | **Where** in the system, at what size of piece, are we testing? | A group of test activities organized by the scope of what is tested | Unit, integration, system, acceptance |
| **Test type** | **What** quality or purpose are we testing for? | A group of test activities focused on a particular quality characteristic or goal | Functional, performance, security, usability, accessibility, regression, smoke, sanity |
| **Test technique** | **How** do we design the tests or find defects? | A systematic method used to derive test cases | Equivalence partitioning, boundary value analysis, decision tables, state transition, error guessing, statement coverage (white-box) |

Putting them together in one sentence: "At the **system level**, we run **functional** tests, designed using **boundary value analysis**, for the registration password length rule." And another: "At the **system level**, we run a **performance** test, designed with a **workload model**, for the login page." The same level can host many types, and the same technique can serve different levels and types.

A note on terms: some people call smoke and sanity "types", others "approaches". Do not worry about the exact label; focus on the purpose.

### 12. Risk-Based Selection of Non-Functional Tests

You cannot test every quality attribute to the maximum. **Risk-based testing** means focusing effort where the chance of failure and the impact of failure are highest. Apply it to non-functional tests as follows:

1. **List the quality attributes** that could matter (use ISO/IEC 25010 as your checklist).
2. **For each, estimate likelihood and impact.** Likelihood: How likely is it to fail given the technology, team experience, and past incidents? Impact: What happens to users and the business if it fails?
3. **Prioritize.** High likelihood and high impact come first.
4. **Choose depth accordingly.** Deep testing for high risks, light checks for low risks.
5. **Revisit** as the product and its usage change.

Example for Project 1:

| Quality attribute | Likelihood of problem | Impact if it fails | Priority | Planned depth |
|---|---|---|---|---|
| Security of login | Medium (public target) | Very high (data breach, legal) | Very high | Threat modeling, automated scans, manual review, repeated each release |
| Performance of login at peak | Medium | High (users cannot enter) | High | Load and spike tests before each major release |
| Accessibility of forms | Medium | High (excludes users, legal risk) | High | Automated scan on each build, manual check each release |
| Compatibility with major browsers | Medium | Medium to high | Medium-High | Automated cross-browser smoke checks; deeper checks on top 4 browsers |
| Localization | Low now (single language) | Low now | Low | Revisit when new languages are planned |
| Installability (web app) | Low | Low | Low | Covered by deployment pipeline |

The result is a plan that spends effort on the right things rather than trying to do everything. Today's exercise will ask you to apply this thinking in the regression and risk plan.

### 13. Non-Functional Testing in Agile and CI/CD

In Agile, work happens in short **sprints**, and the team delivers small increments. A common mistake is treating non-functional work as "something for later" while sprints deliver functional stories. Better practices:

- **Include NFRs in the Definition of Done.** For example: "Done means unit tests pass, accessibility scan has no new serious violations, and no new high-severity security findings."
- **Write NFR acceptance criteria into user stories** using the Given/When/Then style shown above, especially for stories that touch critical paths such as login.
- **Make NFRs visible as backlog items.** Some qualities, like "improve login performance" or "add audit logging", are work items in their own right (sometimes called technical stories or enabler stories).
- **Test continuously, not just once.** Quality can degrade silently with each change, so repeat the checks.

In **CI/CD (Continuous Integration / Continuous Delivery or Deployment)**, every code change automatically triggers a pipeline that builds, tests, and may deploy the software. Within this pipeline, **quality gates** are automatic checkpoints with pass or fail thresholds. If the criteria are not met, the pipeline stops and the change is not promoted. Examples of non-functional gates:

| Pipeline stage | Example quality gate |
|---|---|
| On every commit | Linting and static analysis: no new critical code-quality issues; complexity below threshold |
| On every build | Dependency scan: no known critical vulnerabilities; accessibility scan: no new serious violations |
| After deployment to test environment | Smoke test passes; a short performance check: 95th percentile login time under 2 seconds at 50 virtual users |
| Before release | Full load test meets targets; security scan clean of high-severity findings; compatibility checks pass on the priority browser list |
| After release (production) | Monitoring and alerts: error rate and response times within limits; automatic rollback if they are not |

Notice that heavy tests (a 24-hour soak test) do not run on every commit; they are scheduled (for example, nightly or weekly) or run before big releases. Choosing what to run when is part of your skill as a test engineer.

### 14. AI in Non-Functional Testing

Artificial intelligence is increasingly used to support quality work. Some realistic uses in the non-functional area:

- **Anomaly detection in monitoring.** Machine-learning models learn what "normal" looks like for response times, error rates, and resource use, and flag unusual patterns, such as a slow growth in login latency, that fixed thresholds might miss. This is useful in observability.
- **Accessibility checkers.** AI-assisted tools can suggest alternative text for images, spot unlabeled controls, estimate reading order, or group issues by severity.
- **Test and workload generation.** AI assistants can help draft load scripts, suggest realistic user behavior mixes from production logs, or propose edge-case inputs for robustness checks.
- **Log analysis.** AI can summarize large volumes of logs, cluster similar failures, and point to likely causes, saving investigation time.
- **Visual and compatibility checks.** AI-based visual comparison can detect layout differences across browsers and screen sizes better than naive pixel comparison.
- **Security assistance.** AI can help prioritize scanner findings or review code for common weaknesses, as one input among many.

**Cautions** (very important for a professional tester):

1. **AI can be confidently wrong.** Suggested alternative text may be inaccurate; a "no anomaly" result does not prove health. Always verify.
2. **AI-generated tests and requirements still need human judgment.** An AI may invent thresholds that have no connection to your real users or business. The numbers must come from agreed requirements and data.
3. **Do not paste sensitive data** (real user data, secrets, internal architecture, vulnerability details) into AI tools that are not approved by your organization. Registration and login data is exactly the kind of sensitive information at stake.
4. **Automated checks, AI or not, cover only part of the picture.** Accessibility tools miss many issues; AI-based security suggestions can miss real vulnerabilities and produce false alarms.
5. **Models can drift and can be biased.** An anomaly detector trained on a quiet period may misjudge a busy period.
6. **You remain accountable.** Treat AI output as a draft from a fast but fallible assistant, and review it as you would a new colleague's work.

---

## Examples

### Example 1: Same Feature, Two Sets of Tests

Feature: **User Registration** in Project 1.

**Functional tests (what it does):**
- A valid email and a valid password create an account and show "Registration successful."
- A duplicate email is refused with "Email already registered."
- A password of 7 characters is refused; 8 characters is accepted (boundary).
- The saved record in the database contains the email exactly as entered (trimmed of spaces, if the rule says so) and a hashed password.

**Non-functional tests (how well):**
- 95% of registration submissions complete within 3 seconds under 200 concurrent users (performance).
- The form is completely usable with a keyboard and a screen reader (accessibility).
- The form displays correctly on a 360-pixel-wide phone and in the latest Safari (compatibility).
- The registration request is sent only over HTTPS and the password never appears in logs (security).
- First-time users complete the form in under 2 minutes without help (usability).

All of these are about the same feature, yet each test tells you something different.

### Example 2: Classifying a Single Requirement

Requirement: "After a user submits the login form, the dashboard shall appear within 3 seconds."

At first glance this mentions a function (login). But the requirement's **point** is the time limit, so it is **non-functional (performance, time behavior)**. A good functional counterpart would be: "If the email and password match a registered user, the system shall show the dashboard." A tester can check both in the same test run, with a timer.

### Example 3: Smoke, Sanity, and Regression in One Day

Imagine today is a release day for Project 1:

1. A new build is deployed. The pipeline runs the **smoke test**: app loads, login works for a valid user, registration page opens. All green: the build is accepted.
2. A developer has fixed a bug: "Password of exactly 8 characters is rejected." The tester performs a **sanity test** on password length rules (7, 8, 9 characters) and the registration flow that uses them. All good.
3. Because the fix touched shared validation code, the team runs the **regression suite** overnight to make sure the login, password reset, and profile pages still behave as before.

Same day, three different purposes.

---

## A Python Demonstration: One Functional Check and Two Simple Non-Functional Checks

Time to see the idea in code. Do not worry if you are new to Python; every line is explained afterward. The program has a small function that validates a password (the **function under test**), one functional test, and two simple non-functional tests: a response-time check and an oversized-input and memory check. In real projects you would use a test framework such as pytest and proper load tools, but this plain script keeps the idea visible.

### The Code

Save this as `nfr_demo.py` (anywhere outside your project's graded folders, such as a practice folder) and run it with `python nfr_demo.py`.

```python
import time
import tracemalloc

MAX_PASSWORD_LENGTH = 64


def is_valid_password(password):
    """Return True if the password meets the Project 1 registration rules."""
    if not isinstance(password, str):
        return False
    if len(password) < 8 or len(password) > MAX_PASSWORD_LENGTH:
        return False
    has_digit = any(ch.isdigit() for ch in password)
    has_letter = any(ch.isalpha() for ch in password)
    return has_digit and has_letter


# ---------- Functional check ----------
def test_functional_password_rules():
    assert is_valid_password("Pass1234") is True
    assert is_valid_password("short1") is False
    assert is_valid_password("alllettersonly") is False
    assert is_valid_password("12345678") is False
    print("Functional check passed: password rules behave as specified")


# ---------- Non-functional check 1: response time ----------
def test_nonfunctional_response_time():
    runs = 1000
    start = time.perf_counter()
    for _ in range(runs):
        is_valid_password("Pass1234")
    elapsed = time.perf_counter() - start
    average_ms = (elapsed / runs) * 1000
    print(f"Average time per validation: {average_ms:.4f} ms")
    assert average_ms < 5.0, f"Too slow: {average_ms:.4f} ms (limit 5 ms)"
    print("Non-functional check passed: average time is under 5 ms")


# ---------- Non-functional check 2: input length and memory ----------
def test_nonfunctional_large_input():
    huge = "a1" * 500_000  # 1,000,000 characters
    tracemalloc.start()
    start = time.perf_counter()
    result = is_valid_password(huge)
    elapsed_ms = (time.perf_counter() - start) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_kb = peak / 1024
    print(f"Huge input rejected: {result is False}; took {elapsed_ms:.4f} ms; peak memory {peak_kb:.2f} KB")
    assert result is False
    assert elapsed_ms < 50, "Rejecting oversized input took too long"
    assert peak_kb < 100, "Validation used too much memory"
    print("Non-functional check passed: oversized input handled quickly and cheaply")


if __name__ == "__main__":
    test_functional_password_rules()
    test_nonfunctional_response_time()
    test_nonfunctional_large_input()
    print("All checks passed")
```

### Expected Output

When run, the program prints something like the following. **The exact timing numbers will differ on your machine and from run to run**, because speed depends on your processor, what else the computer is doing, and the Python version. The messages that say "passed" and the final line should match.

```
Functional check passed: password rules behave as specified
Average time per validation: 0.0007 ms
Non-functional check passed: average time is under 5 ms
Huge input rejected: True; took 0.0103 ms; peak memory 0.03 KB
Non-functional check passed: oversized input handled quickly and cheaply
All checks passed
```

(We ran this exact program to produce this sample; a second run gave 0.0014 ms and 0.0111 ms, which shows the variation.)

### Line-by-Line Explanation

**Imports and constant**

- `import time`: loads Python's built-in time module, which gives us `time.perf_counter()`, a high-resolution stopwatch.
- `import tracemalloc`: loads a built-in module that tracks how much memory Python code allocates, so we can measure a simple memory figure.
- `MAX_PASSWORD_LENGTH = 64`: a named constant for the longest password we accept. Naming it avoids a "magic number" and documents the business rule.

**The function under test**

- `def is_valid_password(password):` defines a function that takes one input and returns True or False.
- The triple-quoted line is a **docstring**, a description of what the function does.
- `if not isinstance(password, str): return False`: if the input is not text (for example `None` or a number), reject it. This is defensive handling of unexpected input.
- `if len(password) < 8 or len(password) > MAX_PASSWORD_LENGTH: return False`: rejects passwords that are too short or too long. `len()` counts characters. This is the length rule you can test with boundary values (7, 8, 64, 65).
- `has_digit = any(ch.isdigit() for ch in password)`: goes through each character `ch` and asks whether it is a digit; `any(...)` is True if at least one is.
- `has_letter = any(ch.isalpha() for ch in password)`: the same for letters.
- `return has_digit and has_letter`: valid only if the password contains both a digit and a letter.

**The functional test**

- `def test_functional_password_rules():` a test function (its name starts with `test_`, a convention that test frameworks recognize).
- `assert is_valid_password("Pass1234") is True`: an **assertion** states what we expect. If the condition is not true, Python raises an error and the test fails. "Pass1234" has 8 characters, letters, and digits, so it should be valid.
- `assert is_valid_password("short1") is False`: 6 characters, so too short; expected False.
- `assert is_valid_password("alllettersonly") is False`: long enough but no digit; expected False.
- `assert is_valid_password("12345678") is False`: long enough but no letter; expected False.
- The `print` line runs only if every assertion passed. This test is **functional** because it checks *what* the function returns for given inputs, a clear pass or fail against specified rules.

**Non-functional check 1: response time**

- `runs = 1000`: we repeat the call 1000 times, because a single call is too quick to measure reliably and one measurement can be noisy. Repetition gives a more stable average.
- `start = time.perf_counter()`: records the stopwatch reading before the loop.
- `for _ in range(runs):` loops 1000 times; the underscore means "we do not need the loop counter."
- `is_valid_password("Pass1234")`: calls the function under test.
- `elapsed = time.perf_counter() - start`: total seconds taken by the loop.
- `average_ms = (elapsed / runs) * 1000`: divides by the number of runs for the average seconds per call, then multiplies by 1000 to get milliseconds.
- `print(f"Average time per validation: {average_ms:.4f} ms")`: shows the result; the `f` before the quote lets us insert values in braces and `:.4f` shows four decimal places.
- `assert average_ms < 5.0, f"Too slow: ..."`: **the non-functional assertion.** It sets a threshold of 5 milliseconds. If the average is slower, the test fails and shows the message after the comma. Here the threshold is intentionally generous so the test is not flaky on a slow laptop; in real projects, thresholds come from the agreed requirement (for example, the 2-second login target) and are checked in a controlled environment.

**Non-functional check 2: oversized input and memory**

- `huge = "a1" * 500_000`: builds a text of 1,000,000 characters by repeating "a1" 500,000 times. (The underscore in `500_000` is just for readability.) This simulates a user, or a malicious script, sending an enormous password.
- `tracemalloc.start()`: begins tracking memory allocations.
- `start = time.perf_counter()`: starts the stopwatch.
- `result = is_valid_password(huge)`: runs the function on the huge input.
- `elapsed_ms = (time.perf_counter() - start) * 1000`: elapsed time converted to milliseconds.
- `_, peak = tracemalloc.get_traced_memory()`: asks for two numbers (current and peak memory use); we ignore the first with `_` and keep the peak, the highest memory use while tracking.
- `tracemalloc.stop()`: stops tracking, to avoid slowing down later code.
- `peak_kb = peak / 1024`: converts bytes to kilobytes.
- The `print` shows whether the input was rejected, how long it took, and the peak memory.
- `assert result is False`: a functional expectation: oversized input must be rejected.
- `assert elapsed_ms < 50, ...`: non-functional: rejecting the input must take under 50 milliseconds. Because the length check happens first and returns right away, it is quick. If someone changed the code to check each character *before* the length check, this test could catch the slowdown on large inputs.
- `assert peak_kb < 100, ...`: non-functional: the check must not use more than 100 kilobytes of additional memory. (The big text itself was created before tracking began, so only the function's own allocations are counted.)

**The main block**

- `if __name__ == "__main__":` means "run the following only when this file is run directly." It lets the file be imported later without running the tests.
- The three calls run the tests in order, and the last `print` appears only if none of them raised an assertion error.

### What to Notice

1. The same function is checked for **what it returns** (functional) and **how quickly and cheaply it does it** (non-functional).
2. Non-functional checks need **thresholds** to produce a pass or fail. Without a number, you only have a measurement.
3. **Timing results vary by machine.** In real pipelines, teams compare against baselines on the same environment, run repeated measurements, use percentiles, and avoid thresholds so tight that they fail randomly.
4. This is a tiny **unit-level** performance check, a good example of shift-left. It does **not** replace load testing of the real system with many concurrent users, which is a different, larger activity covered in the performance lesson.

---

## Project 1: Test Idea Matrix for Registration and Login

Use these test ideas as a model when you complete today's test-design document. Each one includes a measurable or clearly observable pass criterion.

### Ten Functional Test Ideas

| # | Area | Test idea | Measurable / observable criterion |
|---|---|---|---|
| F1 | Registration | Register with a valid, unused email and a valid password | Account created; message "Registration successful" shown; exactly one new user record exists |
| F2 | Registration | Register again with the same email (different case, such as `USER@x.com` vs `user@x.com`) | Registration refused; message "Email already registered"; user count unchanged (per the agreed rule on case) |
| F3 | Password rules (boundary) | Try passwords of 7, 8, 64, and 65 characters (with letters and digits) | 7 and 65 rejected with the specified message; 8 and 64 accepted |
| F4 | Email format (equivalence partitioning) | Try valid and invalid email formats (missing `@`, missing domain, spaces) | Valid formats accepted; each invalid class rejected with a field-level message |
| F5 | Required fields | Submit the form with each required field left empty in turn | Submission blocked; message appears for the empty field; no record created |
| F6 | Login success | Log in with correct credentials | Dashboard displayed; session established; username shown in header |
| F7 | Login failure | Log in with a correct email and wrong password; then with an unknown email | Both refused with the same generic message (not revealing which part was wrong); no session created |
| F8 | Account lock (decision table / state transition) | Enter the wrong password 5 times, then the correct one | Account moves to "locked" state; correct password refused during lock; message explains the lock |
| F9 | Logout and session | Log out, then press the browser Back button | Login page or "signed out" page shown; protected pages cannot be viewed without logging in again |
| F10 | Data handling (database) | After registration, inspect the stored record | Email stored as specified (trimmed, in the agreed case); password stored hashed and not readable; creation timestamp present |

### Ten Non-Functional Test Ideas

| # | Quality attribute | Test idea | Measurable criterion |
|---|---|---|---|
| N1 | Performance (load) | 500 concurrent users log in over 10 minutes | 95% of requests respond within 2 seconds; error rate below 1% |
| N2 | Performance (spike) | Jump from 50 to 1,000 login attempts per minute within 30 seconds | No request fails with a server error; response time returns to normal within 2 minutes after the spike |
| N3 | Reliability / recoverability | Restart the authentication service while users are logging in | No account data corrupted; service accepts logins again within 2 minutes; users see a clear retry message |
| N4 | Security (authentication) | Attempt repeated failed logins; inspect password storage | Lockout after 5 failures for 15 minutes; passwords stored using a salted, slow hash; no plain-text passwords anywhere |
| N5 | Security (session / transport) | Check the connection and session behavior | All login traffic uses HTTPS; session expires after 15 minutes of inactivity; logging out invalidates the session |
| N6 | Usability | Observe 5 first-time users registering without help | At least 4 of 5 complete registration in under 2 minutes; error messages understood without explanation |
| N7 | Accessibility | Complete registration and login using only the keyboard, then with a screen reader; run an automated scan | Every control reachable in logical order with visible focus; every field announced with its label; zero critical violations in the automated scan; text contrast at least 4.5:1 |
| N8 | Compatibility | Run registration and login on the latest two versions of Chrome, Firefox, Safari, and Edge, and at widths 360, 768, and 1920 pixels | All functional smoke checks pass in every combination; no layout overlap or cut-off controls |
| N9 | Localization | Switch the interface to Spanish and enter names with accents and non-Latin characters | All visible text translated; special characters accepted and displayed correctly; no truncated labels |
| N10 | Observability / logging | Trigger failed logins and view logs and dashboards | Each failure logged with timestamp, request ID, and reason; no passwords or full tokens in logs; alert fires within 5 minutes when failures exceed 50 per minute |

---

## Try It: Project 1 Activity

**Goal:** Extend your Project 1 test-design document with a functional and non-functional view.

**Time:** About 45 to 60 minutes.

**Steps:**

1. **Open your Project 1 test-design document** (the one you have been building during the week).
2. **Add a section called "Non-Functional Requirements".** Using ISO/IEC 25010 as your checklist, list each quality characteristic and decide whether it matters for registration and login. Write "not applicable for now" with a reason where it does not matter.
3. **Choose your six most important non-functional qualities** using the risk-based table from this lesson. For each, give likelihood, impact, priority, and planned depth.
4. **Write a measurable requirement for each of your six qualities.** Use the pattern "X percent of Y within Z under condition W" or Given/When/Then. Ask: could two testers reach the same verdict?
5. **Add at least five new functional and five new non-functional test cases** to your document, different from the sample matrix, each with an ID, objective, steps, expected result, and (for non-functional tests) the measure, threshold, and tool or approach you would use (name level only).
6. **Classify each of your test cases by level, type, and technique** using the three-column idea from this lesson.
7. **Mark which tests would be part of a smoke set** (the 3 to 5 checks that tell you a build is worth testing) and write a one-line reason for each.
8. **Run the Python demonstration** on your computer, then change the threshold and the input to see tests fail. For example, change `5.0` to `0.0000001`, or reduce `MAX_PASSWORD_LENGTH` so the password check changes. Write down in two or three sentences what you observed and why timing results are not identical each time.

**Self-check:** Does every non-functional test have a number, a condition, and a way to measure? If not, rewrite it.

---

## Exercise 1: Classification (20 Requirements)

For each requirement, decide: **Functional (F)** or **Non-Functional (NF)**. If non-functional, name the type (for example performance, security, usability, accessibility, compatibility, reliability, scalability, localization, compliance, maintainability, portability, observability, disaster recovery). Try it on your own before reading the answer key.

1. The system shall allow a visitor to register using an email address and password.
2. 95% of login requests shall complete within 2 seconds with 500 concurrent users.
3. The system shall send a verification email after registration.
4. All pages shall be navigable using only the keyboard.
5. An account shall be locked for 15 minutes after 5 consecutive failed login attempts.
6. The login page shall display correctly on the latest two versions of Chrome, Firefox, Safari, and Edge.
7. Passwords shall be stored using a salted hashing algorithm.
8. The system shall be available 99.9% of each month, excluding planned maintenance.
9. The system shall support registration pages in English, Spanish, and French.
10. A registered user shall be able to reset a forgotten password through an emailed link.
11. After a database failure, service shall be restored within 4 hours and no more than 15 minutes of data shall be lost.
12. The system shall handle growth from 10,000 to 100,000 registered users without redesign, keeping login response targets.
13. Text shall have a contrast ratio of at least 4.5:1 against its background.
14. The system shall display an error message "Email already registered" when a duplicate email is submitted.
15. Every failed login shall be recorded in an audit log with timestamp and reason, excluding the password.
16. The system shall comply with the applicable data-protection laws when storing personal data, including honoring deletion requests.
17. New developers shall be able to change a password rule by modifying one module, with unit tests verifying the change.
18. At least 90% of first-time users shall complete registration in under 2 minutes without help.
19. The application shall run unchanged on both Linux and Windows servers.
20. The dashboard shall display the user's name after successful login.

### Answer Key

| # | Answer | Type / reasoning |
|---|---|---|
| 1 | F | Core feature: registration |
| 2 | NF | Performance (load, response time) |
| 3 | F | Feature: system sends a verification email (behavior) |
| 4 | NF | Accessibility (keyboard navigation) |
| 5 | F | Business rule on account locking. (The rule itself is functional; whether attackers can be resisted overall is a security quality. This is a good example of overlap; most teams treat the specified lock behavior as functional, with a security flavor.) |
| 6 | NF | Compatibility (browsers) |
| 7 | NF | Security (data protection). The quality of how data is protected, not a user-facing feature |
| 8 | NF | Reliability / availability |
| 9 | NF | Localization (internationalization). Some teams may treat language support as a feature; the quality focus here is language and region adaptation, so we classify it non-functional |
| 10 | F | Feature: password reset |
| 11 | NF | Disaster recovery (RTO and RPO) |
| 12 | NF | Scalability (with performance) |
| 13 | NF | Accessibility (color contrast) |
| 14 | F | Specified behavior and message for a business rule (duplicate email) |
| 15 | NF | Observability / logging (also supports security auditing) |
| 16 | NF | Compliance (privacy laws). The deletion capability itself would be a functional requirement that comes out of the compliance need |
| 17 | NF | Maintainability (modifiability, testability) |
| 18 | NF | Usability (effectiveness, efficiency) |
| 19 | NF | Portability |
| 20 | F | Feature behavior: display of user's name |

**Discussion:** Some items sit on the boundary (numbers 5, 9, and 16). In practice, a single quality need often produces both functional requirements (the lock rule, the deletion function) and non-functional requirements (the response time of those functions, the security of the data). If your classification of a borderline item differs from the key but you can justify it, that is a sign of good thinking; the real goal is that each requirement ends up **testable**.

---

## Exercise 2: Rewrite the Vague Non-Functional Requirement

Rewrite each vague statement as a measurable requirement. State the measure, the number, and the conditions. Then compare with the sample answers (yours may differ; many correct answers exist, provided they are specific, measurable, and testable).

1. "The registration page should load quickly."
2. "Login must be secure."
3. "The system should be reliable."
4. "The app should be easy for everyone to use."
5. "The site must work on mobile."
6. "Errors should be handled well."
7. "The system must scale."
8. "We need good logging."

### Sample Answers

1. "On a simulated 4G connection, the registration page shall display its main content (largest visible element) within 2.5 seconds in 90% of test runs, and total page weight shall not exceed 500 KB."
2. "Login shall be served only over HTTPS; passwords shall be stored with a salted, slow hash; the account shall lock for 15 minutes after 5 consecutive failed attempts; sessions shall expire after 15 minutes of inactivity; and an automated security scan shall report no high-severity findings before release."
3. "The login service shall have no more than 1 unplanned outage per quarter, a mean time to recover under 15 minutes, and an availability of at least 99.9% per calendar month."
4. "The registration and login pages shall meet WCAG 2.1 (or the current agreed version) level AA, shall be fully operable by keyboard, and at least 90% of first-time users shall complete registration without help in under 2 minutes."
5. "The registration and login flows shall function correctly on the latest two major versions of Chrome and Safari on Android and iOS, at viewport widths from 360 to 430 pixels, with all tap targets at least 44 by 44 pixels."
6. "For each of the 12 listed error conditions, the system shall show a message in plain language that names the problem and the fix, display it next to the relevant field, and never show technical details such as stack traces; 100% of server errors shall return a friendly page and a reference code, and be logged."
7. "When the number of concurrent users rises from 500 to 2,000, adding application servers shall keep the 95th percentile login response time under 2 seconds, with throughput increasing by at least 70% of the added capacity, and the database CPU staying below 75%."
8. "Each login attempt (successful or failed) shall create a log entry within 1 second containing timestamp, request ID, result, and reason code, with no passwords or tokens; logs shall be retained for 90 days and searchable within 10 seconds; an alert shall be raised within 5 minutes if failures exceed 50 per minute."

**Tip:** After rewriting, ask three questions. What would I measure? What number would make it pass or fail? Under what conditions?

---

## Common Misconceptions

**1. "Non-functional testing is optional; we can do it if there is time."**
It is not optional. A product can fail in the market, legally, or in security because of non-functional weaknesses even if every feature works. The depth of non-functional testing is chosen by risk, but the question must always be asked.

**2. "Functional testing is only about clicking buttons on the screen."**
Functional testing includes API and database checks, business rules, calculations, and data handling. It checks that data is stored, transformed, and retrieved correctly, not only that screens look right.

**3. "Non-functional tests can only be done at the end."**
Many can and should start early: performance budgets, static security scans, accessibility linting, requirement reviews, and small unit-level timing checks. Only some, such as full-scale load tests, need a stable, production-like environment.

**4. "Non-functional means non-working or less important."**
The name only means the tests do not verify a specific feature. Many people prefer "quality attributes".

**5. "Smoke, sanity, and regression are the same thing."**
They differ in purpose and scope, as the comparison table shows.

**6. "Performance testing is just checking the page loads fast on my laptop."**
Performance is about behavior under realistic conditions and loads, with realistic data and networks. Your machine on a fast connection with one user tells you little.

**7. "Automated accessibility tools tell me the site is accessible."**
They catch only a portion of issues. Manual testing with a keyboard and screen reader is essential.

**8. "If all the tests pass, the product is good."**
Tests only reveal what they check. If no one defined or tested the non-functional qualities, passing tests can give false confidence. This is the absence-of-errors fallacy again.

**9. "Only specialists handle non-functional testing, so the average tester does not need to know it."**
Specialists may run complex performance or security work, but every tester should raise questions, spot untestable requirements, run basic checks (keyboard navigation, browser variations), and understand results.

**10. "AI tools will handle non-functional testing for us."**
AI can assist, but it needs human-defined requirements, verification, and judgment, and it can make confident mistakes.

---

## Knowledge Check

Try to answer each question before opening the answer.

**1. In one sentence each, explain what functional and non-functional testing check.**
*Answer:* Functional testing checks that the system does what it is supposed to do (features, business rules, data handling, user interactions) according to functional requirements. Non-functional testing checks how well the system does it, in terms of quality attributes such as performance, security, usability, accessibility, and reliability.

**2. A login feature accepts the right password and rejects the wrong one, but takes 30 seconds. Is this a pass or a fail, and why?**
*Answer:* From the user's viewpoint it is a fail. It passes functional tests but fails a non-functional (performance) expectation. This illustrates the absence-of-errors fallacy and validation: the product must satisfy user needs, not only specifications about features.

**3. Which of these is a functional requirement and which is non-functional? (a) "The system shall let users change their email address." (b) "Changing the email address shall complete within 2 seconds for 95% of requests."**
*Answer:* (a) is functional; (b) is non-functional (performance).

**4. What is the difference between smoke testing and sanity testing?**
*Answer:* Smoke testing is broad and shallow: it checks that the most critical functions of a new build work so that deeper testing is worthwhile. Sanity testing is narrow and deeper: it checks that a specific change or bug fix works and that the closely related area is reasonable.

**5. Name the three main parts of the explanation that separate test levels, types, and techniques.**
*Answer:* Level answers "where/what size of piece" (unit, integration, system, acceptance); type answers "what quality or purpose" (functional, performance, security, smoke); technique answers "how we design tests" (equivalence partitioning, boundary value analysis, decision tables).

**6. Which functional test level is typically run by business users or customers, and what are its two common pre-release forms?**
*Answer:* Acceptance testing (User Acceptance Testing). Alpha testing is internal; beta testing is performed by a limited group of real external users.

**7. Which five areas of security should a beginner consider for the login page conceptually?**
*Answer:* Authentication, authorization, input validation, session handling, and data protection.

**8. What does POUR stand for in accessibility?**
*Answer:* Perceivable, Operable, Understandable, Robust (the four principles of WCAG).

**9. Where does functional suitability sit in ISO/IEC 25010?**
*Answer:* It is one of the product quality characteristics, alongside performance efficiency, compatibility, usability, reliability, security, maintainability, and portability. Functional testing tests that one characteristic; the others are what we call non-functional.

**10. Why is "The system should be fast" a poor requirement, and how could you improve it?**
*Answer:* It is vague and untestable: no measure, number, or conditions. Improve it: "95% of login requests shall respond within 2 seconds under 500 concurrent users."

**11. What do RTO and RPO mean?**
*Answer:* Recovery Time Objective: the maximum acceptable time to restore service after a disaster. Recovery Point Objective: the maximum acceptable amount of data loss, measured in time.

**12. Give two examples of shifting non-functional testing left.**
*Answer:* Examples: performance budgets checked on every build; threat modeling during design; accessibility linting in the code editor or pipeline; reviewing requirements for measurable NFRs; early unit-level timing checks.

**13. What is a quality gate in a CI/CD pipeline?**
*Answer:* An automatic checkpoint with defined pass or fail criteria (for example, no critical vulnerabilities, accessibility violations below a limit, 95th percentile response time under a target) that must be met before the change moves to the next stage.

**14. How should risk influence which non-functional tests you run?**
*Answer:* You estimate the likelihood and impact of failure for each quality attribute and put the most effort into the ones with high likelihood and high impact, with lighter checks for low-risk ones, then review as things change.

**15. Give two cautions when using AI in non-functional testing.**
*Answer:* For example: AI output can be confidently wrong and must be verified; thresholds and requirements must come from real data and agreement, not AI invention; do not share sensitive data with unapproved tools; automated checks cover only part of the picture; you remain accountable for the results.

**16. In the Python demonstration, why do we run the function 1000 times before computing an average, and why does the output change each time we run it?**
*Answer:* A single call is too fast to measure reliably and one measurement is noisy; repeating and averaging gives a steadier figure. The output changes because timing depends on the machine, its current workload, and the Python environment, which is why thresholds should be realistic and measured in a controlled environment.

---

## Key Takeaways

- **Functional testing** asks "what does the system do?" and verifies features, business rules, data handling, and user interactions against functional requirements. **Non-functional testing** asks "how well?" and verifies quality attributes.
- Functional testing happens at multiple **levels** (unit, integration, system, acceptance) and in multiple **types** (smoke, sanity, end-to-end, API, GUI, database, UAT, alpha, beta). Know what, when, who, and an example for each.
- **Smoke** is broad and shallow (is the build testable?), **sanity** is narrow and focused (does this fix work?), and **regression** is wide and thorough (did we break anything?).
- Non-functional testing includes performance (load, stress, spike, endurance, volume), reliability, availability, recoverability, scalability, security, usability, accessibility, compatibility, portability, installability, maintainability, localization and internationalization, compliance, disaster recovery, and observability.
- **ISO/IEC 25010** organizes quality into characteristics; **functional suitability is one of them**, which reminds us that functional quality is only part of overall quality.
- Vague quality wishes cannot be tested. Make requirements **measurable** with numbers, conditions, and a method of measurement, using SMART thinking, Planguage ideas, or Given/When/Then.
- Functional and non-functional quality **interact**: a feature that works but takes 30 seconds is a failure from the user's viewpoint. This connects to validation and the absence-of-errors fallacy.
- **Shift left**: set performance budgets, build security into design, lint for accessibility, and review requirements for testability early.
- Do not confuse **levels** (where), **types** (what quality or purpose), and **techniques** (how to design tests).
- Select non-functional tests by **risk**, and place them in **Agile** workflows and **CI/CD quality gates** in a sensible schedule.
- **AI** can help with anomaly detection, accessibility suggestions, and log analysis, but it needs verification, human-defined thresholds, and careful data handling.
- Non-functional testing is **not optional**, and functional testing **does** check data, not only clicks.

---

## Additional Resources

- **ISTQB (International Software Testing Qualifications Board)**: the official site, with the Foundation Level syllabus and glossary that define terms such as functional testing, non-functional testing, test level, and test type. https://www.istqb.org
- **ISO/IEC 25010 product quality model**: the ISO standard page for the system and software quality models discussed in this lesson. https://www.iso.org/standard/78176.html
- **W3C Web Content Accessibility Guidelines (WCAG) overview**: an introduction to WCAG and its POUR principles from the W3C Web Accessibility Initiative. https://www.w3.org/WAI/standards-guidelines/wcag/
- **OWASP Top Ten**: the awareness document for the most critical web application security risks. https://owasp.org/www-project-top-ten/

*Note: Websites and standards are updated over time; always check for the latest version of any standard or list before relying on specific details.*

---

*Coming up next today: regression testing, performance and stress testing, reliability and scalability, and the exercise that completes your Project 1 test-design document and regression/risk plan. The ideas in this lesson, especially measurable requirements and risk-based selection, will feed directly into that work.*
