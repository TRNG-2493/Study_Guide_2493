# Quality Assurance vs. Quality Control

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain what "quality" means using three common definitions: fitness for use, conformance to requirements, and user satisfaction.
2. Name the main product quality characteristics described by ISO/IEC 25010.
3. Describe the four categories of the cost of quality (prevention, appraisal, internal failure, external failure) and calculate a simple example.
4. Define Quality Assurance (QA) and list at least eight QA activities.
5. Define Quality Control (QC) and list at least four QC activities.
6. Explain where software testing fits (it is a QC activity) and what Quality Engineering (QE) adds on top of QA and QC.
7. Compare QA and QC across focus, orientation, timing, goal, responsibility, activities, examples, tools and people.
8. Classify everyday software activities as QA or QC.
9. Describe the PDCA cycle and how it drives continuous improvement.
10. Recognize the purpose of ISO 9001, ISO/IEC 25010, CMMI, ISO/IEC/IEEE 29119 and ISTQB.
11. Explain how QA and QC work in Agile and DevOps teams, including quality gates and shift-left.
12. Apply QA and QC thinking to "Project 1 - QE Foundations".

---

## Why This Matters

Imagine you are on a new team and a manager asks, "Who is responsible for quality here?" Many beginners answer, "The testers." That answer is understandable, but it is incomplete, and it is one of the most common reasons software projects struggle with quality.

If quality is only "checked" at the end by testers, the team finds problems late, when they are expensive and stressful to fix. If quality is also "built in" from the start, through clear requirements, good practices, reviews, and automated checks, then fewer problems are created in the first place, and the ones that do appear are found early.

This lesson gives you the vocabulary and the mental model to talk about both sides of that coin:

- **Quality Assurance (QA)** is about the **process**: doing the work in a way that makes good results likely.
- **Quality Control (QC)** is about the **product**: checking the actual result to find out whether it is good.
- **Quality Engineering (QE)** is the modern approach that combines both, uses engineering skills such as automation and CI/CD, and makes quality everyone's job.

You will hear the terms "QA" and "QC" constantly in your career, often used incorrectly. Job postings say "QA Engineer" when they mean "tester". Colleagues say "send it to QA" when they mean "send it to be tested". After today you will understand the real meaning behind these words, and you will be able to explain the difference clearly in interviews and in team meetings.

This lesson builds directly on what you have already learned this week:

- **Monday** you learned about the SDLC, the STLC and how Agile teams work. QA activities happen across the whole SDLC, not only in the testing phase.
- **Tuesday** you learned about requirements analysis, test planning and execution, and the defect lifecycle. Requirements analysis is a QA activity (preventing defects), while test execution and defect reporting are QC activities (detecting defects).
- **Earlier today** you learned about the testing mindset. That mindset (curiosity, healthy skepticism, thinking about what could go wrong) is exactly what drives both QA and QC.

---

## The Concept

### 1. What Is "Quality"?

Before we can talk about assuring or controlling quality, we need to agree on what it is. This is harder than it sounds, because "quality" means different things to different people. A cheap pen and a luxury pen can both be "high quality" in the sense that each does its job well for its intended buyer.

Three widely used ways of thinking about quality are:

**a) Fitness for use.** Quality is how well a product serves the purpose its user needs it for. A hammer that cannot hit a nail is poor quality, no matter how pretty it looks. This definition is associated with the quality expert Joseph Juran. In software: does the app help the person get their job done?

**b) Conformance to requirements.** Quality is how closely the product matches what was specified. If the requirement says "the login page must lock an account after 5 failed attempts" and it does so, it conforms. This definition is associated with Philip Crosby. In software: does the product do what the requirements, user stories and acceptance criteria say it should?

**c) User (customer) satisfaction.** Quality is whether the people using the product are happy with it: it is easy, it is reliable, it feels good, and it meets or exceeds their expectations.

Notice that these three definitions can disagree. A product can conform perfectly to its requirements and still be unfit for use if the requirements were wrong (for example, a form that correctly follows a requirement but asks users for information they do not have). A product can also satisfy users in a way that no requirement captured. This is why good quality work looks at all three: **Are we building it right? Is it right for the user? Is the user happy?**

> Pointer: the first two questions ("built right" and "right thing") are closely related to **verification** and **validation**, which are the topic of an upcoming lesson. For now, just remember that quality has more than one angle.

**Quality is multi-dimensional.** A product is not simply "good" or "bad". It may be very fast but hard to use, or very secure but slow. To discuss this precisely, the industry uses a standard list of quality characteristics.

### 2. Product Quality Characteristics (ISO/IEC 25010 Overview)

**ISO/IEC 25010** is an international standard that defines a **product quality model** for software. It lists characteristics that describe different aspects of software quality. The widely taught 2011 version names eight characteristics:

| Characteristic | Plain-language question it answers |
|---|---|
| Functional suitability | Does it do the things it is supposed to do, correctly and completely? |
| Performance efficiency | Is it fast enough and does it use resources sensibly? |
| Compatibility | Does it work with other systems, browsers, devices and coexist with other software? |
| Usability | Can people learn it and use it easily and comfortably? |
| Reliability | Does it keep working over time and recover from problems? |
| Security | Does it protect data and allow only authorized access? |
| Maintainability | Can developers change and fix it without breaking things? |
| Portability | Can it be moved or installed in different environments? |

The standard was revised in 2023. The revised version updates some names and adds a characteristic (for example, it includes safety, and uses the term "interaction capability" in place of usability). You do not need to memorize the revision details. What matters for you is the big idea: **quality is not just "no bugs". It includes speed, security, usability, reliability and more.** When you design tests for Project 1, you will find yourself asking questions from several of these characteristics, not only "does the button work?".

At this stage we only need the names. Details of how each characteristic is tested come in later lessons.

### 3. The Cost of Quality

Why do organizations invest in QA and QC at all? Because poor quality costs money, and so does good quality. The **cost of quality (CoQ)** is a way of adding up all the money spent on achieving quality and the money lost by not achieving it. It is traditionally divided into four categories.

**Cost of good quality (the cost of doing things right):**

1. **Prevention costs** are what you spend to stop defects from happening. Examples: training, writing coding standards, requirement reviews, setting up templates and checklists, improving processes.
2. **Appraisal costs** are what you spend to measure and check quality. Examples: test execution, inspections, audits, test environments, test tools, reviewing deliverables.

**Cost of poor quality (the cost of things going wrong):**

3. **Internal failure costs** are the cost of problems found before the product reaches the customer. Examples: fixing defects found during testing, re-testing, re-doing work, delayed schedules.
4. **External failure costs** are the cost of problems found after the product reaches the customer. Examples: production support, emergency patches, refunds, lost customers, legal exposure, damage to reputation.

#### A simple numeric example

Suppose a team releases a feature in a quarter. Here is what happened with their old way of working:

| Category | What was spent | Cost |
|---|---|---|
| Prevention | Basic coding guidelines, one training session | $2,000 |
| Appraisal | Testing effort at the end of the project | $5,000 |
| Internal failure | 30 defects found in testing, rework about $100 each | $3,000 |
| External failure | 5 defects escaped to customers, about $1,000 each to handle (support, hotfix, goodwill) | $5,000 |
| **Total cost of quality** | | **$15,000** |

Now the team invests more in prevention: they run requirement reviews, adopt a code review checklist, and add automated checks to the build. In the next comparable quarter:

| Category | What was spent | Cost |
|---|---|---|
| Prevention | Reviews, checklists, additional training | $4,000 |
| Appraisal | Same testing effort | $5,000 |
| Internal failure | 18 defects found in testing, about $100 each | $1,800 |
| External failure | 1 defect escaped, about $1,000 | $1,000 |
| **Total cost of quality** | | **$11,800** |

The team spent $2,000 more on prevention but saved $3,200 in failure costs, and the customers had a better experience. The numbers here are invented for illustration, and real costs vary widely. The pattern, however, is widely observed: **spending more on prevention tends to reduce failure costs, and failures found late cost far more than failures found early.**

A well-known rule of thumb is that the cost of fixing a defect rises sharply the later it is found: a misunderstanding caught while reading the requirements costs a conversation, while the same misunderstanding discovered in production costs a hotfix, a support backlog and unhappy users. Treat the exact multipliers you may read about as rough illustrations, not precise laws. The direction, however, is reliable.

This is the business case for QA: **it is cheaper to prevent a defect than to find and fix one**, and it is cheaper to find it in-house than in front of a customer.

### 4. Quality Assurance (QA)

**Quality Assurance (QA)** is the set of planned, systematic activities that make sure the way the team works is capable of producing a good product, and that give confidence that quality requirements will be met. The key word is **process**.

QA characteristics:

- **Process-oriented.** It looks at *how* the product is built, not only at the finished product.
- **Preventive.** It aims to stop defects from being introduced.
- **Proactive.** It acts before problems occur, rather than reacting to them.
- **Whole-lifecycle.** It applies from the first idea through requirements, design, coding, release and maintenance.

A helpful way to remember it: **QA asks, "Are we working in a way that will produce good results?"**

#### Common QA activities

| QA activity | What it is | Why it prevents defects |
|---|---|---|
| Defining standards and guidelines | Writing agreed rules such as coding conventions, naming rules, documentation templates, and a defect severity scale | Everyone works the same way, reducing confusion and inconsistency |
| Process audits | Checking whether the team actually follows its agreed process (for example, are code reviews really happening?) | Finds process gaps before they cause defects |
| Reviews and inspections | Having peers examine requirements, designs, user stories or code *before* they move forward | Catches mistakes when they are cheapest to fix |
| Training and onboarding | Teaching the team tools, domain knowledge and good practices | Skilled people make fewer mistakes |
| Checklists | Short lists that guide repeatable tasks (release checklist, code review checklist) | Reduces forgotten steps |
| Tool and process improvement | Choosing and refining tools, templates and workflows | Removes error-prone manual steps |
| CI quality gates | Rules in the build pipeline that block a change unless it meets criteria (for example, build passes, tests pass, coverage threshold met) | Stops bad changes from moving forward automatically |
| Definition of Done (DoD) | A shared, written list of conditions a work item must meet to count as finished | Prevents "done" from meaning different things to different people |
| Retrospectives | Regular team meetings to reflect and improve how the team works | Turns lessons into process improvements |

Some of these you have already met. The **Definition of Done** and the **retrospective** came up in Scrum on Monday. **Requirements review** (Tuesday) is a classic QA activity: it looks at the work item before anything is built.

Notice that most of these activities do not involve running the software at all. That is a hallmark of QA: it improves the *way of working*.

### 5. Quality Control (QC)

**Quality Control (QC)** is the set of activities that examine the actual product (or its parts and deliverables) to find out whether it meets the specified quality criteria. The key word is **product**.

QC characteristics:

- **Product-oriented.** It looks at the built thing: the software, the documents, the feature.
- **Detective** (and corrective). It aims to *find* defects, and the findings lead to corrections (fixes).
- **Reactive.** It responds to what has been produced.
- **Mostly after something is built.** You can only check what exists.

A helpful way to remember it: **QC asks, "Does this actual product meet the criteria?"**

#### Common QC activities

| QC activity | What it is |
|---|---|
| Testing | Running the software (or examining it) with chosen inputs and comparing actual results with expected results |
| Inspection of deliverables | Examining a finished artifact (a build, a document, a release package) against criteria |
| Defect finding and reporting | Logging defects clearly so they can be fixed (Tuesday's defect lifecycle) |
| Measuring against acceptance criteria | Checking whether each acceptance criterion of a user story is met |
| Re-testing and regression checks | Confirming fixes work and nothing else broke |
| Reporting quality status | Sharing results: pass/fail counts, open defects, release readiness |

The corrective part of QC means that after a defect is found, someone fixes it, and the fix is verified. QC does not stop at "found a problem".

### 6. Where Does Testing Fit?

This is where beginners get confused, so let us be precise.

**Testing is a QC activity.** It is one of the main ways to check a product. But QC is bigger than only testing (it also includes inspection and measurement), and quality work overall is bigger than QC (it includes QA).

Now we can place a third idea: **Quality Engineering (QE)**.

**Quality Engineering (QE)** is an approach in which quality is **built into** the whole engineering process rather than checked at the end. Quality Engineers use engineering skills to do this. QE typically adds:

- **Building quality in:** working with developers and product owners from the beginning.
- **Automation:** writing code and using tools so that checks run quickly and repeatedly.
- **CI/CD integration:** making automated checks part of the pipeline so every change is verified.
- **Shift-left:** moving quality activities earlier in the lifecycle (reviewing requirements, testing early, checking code as it is written).
- **Shift-right:** extending quality activities into production (monitoring, observability, learning from real usage, gradual rollouts).
- **An engineering mindset:** treating quality problems as engineering problems to be solved with design, tooling and data.

Here is a picture of how these ideas relate:

```
+---------------------------------------------------------------+
|  QUALITY ENGINEERING (QE)                                     |
|  Build quality in. Automate. CI/CD. Shift-left & shift-right. |
|                                                               |
|   +-------------------------------------------------------+   |
|   |  QUALITY ASSURANCE (QA)   - process, preventive       |   |
|   |  Standards, reviews, audits, training, checklists,    |   |
|   |  quality gates, Definition of Done, retrospectives    |   |
|   |                                                       |   |
|   |   +-----------------------------------------------+   |   |
|   |   |  QUALITY CONTROL (QC)  - product, detective   |   |   |
|   |   |  Inspection, measuring against criteria,      |   |   |
|   |   |  defect finding                               |   |   |
|   |   |                                               |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   |   |  TESTING                              |   |   |   |
|   |   |   |  Running and examining the product    |   |   |   |
|   |   |   |  to find defects and give information |   |   |   |
|   |   |   +---------------------------------------+   |   |   |
|   |   +-----------------------------------------------+   |   |
|   +-------------------------------------------------------+   |
+---------------------------------------------------------------+
```

Read the diagram from the inside out:

- **Testing** is one of the main QC activities.
- **QC** is the product-checking part of the overall quality effort.
- **QA** includes the process side and, in many organizations, QC is considered part of the broader QA effort (in practice many teams say "QA" to mean both).
- **QE** surrounds all of it with engineering practice, automation and a "build it in" attitude.

A word of caution: textbooks and companies draw this picture in slightly different ways. Some show QA and QC as overlapping circles; some treat QC as part of QA. The nesting above is a useful teaching model, not a law. What does not change is the key idea: **prevent where you can, detect what slips through, and keep improving the system.**

You could also think of the same idea as a Venn diagram of emphasis:

```
         QA (process)                    QC (product)
   +--------------------+         +--------------------+
   |  Standards         |         |  Test execution    |
   |  Audits            |  Shared |  Defect detection  |
   |  Training          |<------->|  Acceptance checks |
   |  Retrospectives    |  Areas: |  Inspection of     |
   |                    |  Reviews|  finished deliver- |
   |                    |  Checklists  ables           |
   +--------------------+  Metrics+--------------------+
```

Reviews, checklists and metrics are "shared areas". A code review prevents defects from being merged (QA flavor) but also examines an actual work product for defects (QC flavor). Real life is often blurry like this, and that is fine.

### 7. Detailed Comparison: QA vs. QC

| Aspect | Quality Assurance (QA) | Quality Control (QC) |
|---|---|---|
| **Focus** | The process used to create the product | The product (or deliverable) itself |
| **Orientation** | Process-oriented | Product-oriented |
| **Nature** | Preventive: stop defects from occurring | Detective and corrective: find and fix defects |
| **Approach** | Proactive | Reactive |
| **Timing** | Throughout the lifecycle, from the start | Mostly after something has been built or changed |
| **Goal** | Give confidence that quality requirements will be met; improve the process | Verify the product meets criteria; identify defects before release |
| **Key question** | "Are we doing the right things, the right way?" | "Is what we built good enough?" |
| **Responsibility** | Shared by the whole team and organization; often led by a QA lead, manager or process owner | Typically carried out by testers/QC engineers, with developers also checking their own work |
| **Typical activities** | Standards, audits, reviews, training, checklists, quality gates, Definition of Done, retrospectives | Testing, inspection, defect finding, acceptance criteria checks, regression checks |
| **Examples** | Creating a code review checklist; agreeing a Definition of Done | Running a login test case; verifying a bug fix |
| **Typical tools** | Process documents, wikis, templates, pipeline gate configuration, review tools (for example, pull request reviews), audit checklists | Test management tools, defect trackers (such as Jira), test execution tools, browsers and devices, automation tools |
| **Who** | QA analysts and leads, QE, Scrum Master (process), the whole team | QC testers, QE and SDETs executing and automating checks, developers (unit tests) |
| **Output** | Better processes, standards, trained people | Test results, defect reports, quality status reports |
| **Effect on defects** | Reduces the number of defects introduced | Finds defects that were introduced |
| **Cost impact** | Prevention costs | Appraisal and failure costs |
| **Feedback speed** | Slower, long-term improvement | Faster, immediate information about the current product |

Two truths to keep in mind: **you need both** (prevention is never perfect, so detection is essential, and detection alone is wasteful), and **the best teams blend them** so that the people who build the product also care about checking it.

### 8. A Non-Software Analogy: The Bakery

Software can feel abstract, so let us use something you can picture: a **bakery that sells cakes**.

**The goal:** every customer who buys a chocolate cake should get a delicious, safe, good-looking cake that matches what the menu promised.

#### QA in the bakery (the process)

Before and while the cakes are made, the bakery does things to make good cakes *likely*:

- **A written recipe standard.** Exact quantities, oven temperature and timing, so every baker makes the cake the same way. (Standards.)
- **Kitchen hygiene rules.** Hand washing, clean surfaces, allergen separation. (Process rules that prevent contamination.)
- **Training.** New bakers learn the techniques before they bake for customers. (Training.)
- **A pre-opening checklist.** Oven calibrated, ingredients not expired, scales working. (Checklists.)
- **A manager walks through and checks that staff follow the process.** (Process audit.)
- **Buying good-quality ingredients from approved suppliers.** (Prevention at the source.)
- **Weekly team talk: "Customers said the sponge was dry last week. How do we fix our process?"** (Retrospective and continuous improvement.)

None of these touch a specific finished cake. They all aim to make the cakes come out well in the first place. That is **QA**.

#### QC in the bakery (the product)

After a cake is baked, the bakery examines the actual cake:

- **Tasting a slice** from the batch. (Testing.)
- **Looking at it:** is it the right shape and size, is the icing smooth, is the writing on top correct? (Inspection.)
- **Measuring:** is the center cooked through? Use a thermometer or skewer. (Measuring against criteria.)
- **Rejecting or fixing** a cake that fails: scrape off messy icing, re-do the cake. (Corrective action.)

These activities check a specific product against criteria. That is **QC**.

#### What happens if the bakery does only one?

- **Only QC, no QA:** the bakery bakes cakes carelessly, tastes each one, and throws away many. It wastes ingredients and time, some bad cakes still slip through (nobody can taste every possible problem, such as a tiny hygiene issue), and bakers never learn.
- **Only QA, no QC:** the bakery has beautiful recipes and spotless kitchens but never tastes a cake. One day the oven thermostat quietly breaks, and a batch comes out raw. Nobody notices until customers complain.

Good bakeries do both. They follow recipes and hygiene (QA) **and** taste and inspect (QC). They also notice patterns: "We reject lots of cakes on Mondays. Why?" That leads to a process fix, which is QA again.

#### And Quality Engineering?

Now imagine the bakery installs an oven with automatic temperature control that alerts the baker if the temperature drifts, a scale that refuses to proceed unless the weight matches the recipe, and cameras that check icing patterns. They are **engineering quality into the process** and automating the checks. They also read customer reviews and sales data to learn what happens after the cake leaves the shop (shift-right). That is the spirit of **QE**.

#### Mapping the analogy to software

| Bakery | Software team |
|---|---|
| Recipe standard | Coding standards, requirement templates, Definition of Done |
| Kitchen hygiene rules | Secure coding practices, environment rules, review rules |
| Training new bakers | Onboarding and training developers and testers |
| Pre-opening checklist | Release checklist, code review checklist |
| Manager checks staff follow the process | Process audit |
| Tasting a slice | Running tests |
| Inspecting the icing | Inspecting a build or a document |
| Thermometer in the cake | Measuring against acceptance criteria |
| Automatic oven temperature alarm | Automated CI quality gate |
| Customer reviews after sale | Production monitoring and user feedback |

A second analogy you may like is a **car factory**: the assembly-line procedures, torque standards and worker training are QA, while the end-of-line inspection where someone checks the finished car's brakes is QC. The ideas are the same.

### 9. PDCA: The Cycle of Continuous Improvement

Quality is not a one-time achievement. Good teams keep improving. A classic model for this is the **PDCA cycle** (also called the Deming cycle or Shewhart cycle). It has four steps that repeat:

```
          +-----------+
     +--->|   PLAN    |----+
     |    +-----------+    |
     |                     v
+-----------+         +-----------+
|    ACT    |         |    DO     |
+-----------+         +-----------+
     ^                     |
     |    +-----------+    |
     +----|   CHECK   |<---+
          +-----------+
```

| Step | Meaning | Software example |
|---|---|---|
| **Plan** | Identify a problem or goal and decide what to change | "Many bugs come from unclear login requirements. We will add a requirements review step." |
| **Do** | Try the change, usually on a small scale first | "For the next sprint, every user story gets a 15-minute review before development." |
| **Check** | Measure the results and compare with expectations | "Defects traced to unclear requirements dropped from 12 to 5." |
| **Act** | If it worked, adopt it as the standard; if not, adjust and go around again | "Make requirement review part of the Definition of Done. Then plan the next improvement." |

Notice how PDCA connects QA and QC. The **Check** step needs data, which QC activities produce (test results, defect counts). The **Plan** and **Act** steps are QA decisions that change the process. In Scrum, the **sprint retrospective** is a natural place to run a PDCA loop, which is why retrospectives appear in the QA list.

Continuous improvement means we never claim the process is perfect. We keep looking at evidence and making small, steady improvements.

### 10. Standards and Models: A Name-and-Purpose Overview

You will encounter several standards and models in the industry. You do **not** need to know their details at this stage. You only need to know what each is *for*, so that when you hear the name you are not lost.

| Name | What it is, in one or two sentences |
|---|---|
| **ISO 9001** | An international standard for **quality management systems**. It is not specific to software. It describes requirements for how an organization manages quality in a consistent, improving way. Organizations can be certified against it. |
| **ISO/IEC 25010** | A standard defining a **model of software and system quality** (the quality characteristics listed earlier in this lesson). It gives teams a shared vocabulary for discussing quality. |
| **CMMI** (Capability Maturity Model Integration) | A **process improvement model** that helps organizations assess and improve how mature their processes are. It is used by many software and engineering organizations. |
| **ISO/IEC/IEEE 29119** | A series of international standards about **software testing**: concepts, processes, documentation and techniques. Some organizations use it as a reference for how to organize testing. |
| **ISTQB** (International Software Testing Qualifications Board) | An organization that defines a widely recognized **testing certification scheme** and a standard glossary of testing terms. Many employers value its certifications, such as the Foundation Level. |

Remember the pattern: ISO 9001 and CMMI are about **how an organization works** (QA flavored), ISO/IEC 25010 is about **what we mean by software quality**, 29119 is about **how to do testing** (QC flavored), and ISTQB is about **people's knowledge and a shared language**. We will not go deeper than this today. If your future employer uses one of them, you will learn the specifics on the job.

### 11. QA and QC in Agile and DevOps

Older models, such as the Waterfall model you studied on Monday, often had a testing phase at the end. This made QC a late gate: build everything, then test. QA was often a separate department that audited from the outside.

In **Agile** and **DevOps** teams, things look different:

- **Quality is a team responsibility.** Developers, testers, product owners and the whole team share ownership. "Quality is everyone's job."
- **Testing happens continuously**, inside every sprint, not only at the end.
- **Shift-left.** Quality activities move earlier. Testers join backlog refinement and review user stories and acceptance criteria *before* coding. Developers write unit tests as they code. This is QA and QC both moving left.
- **Automation and CI/CD.** Whenever code changes, the pipeline builds it and runs automated checks. Details of automation come later in the curriculum, but you should know the idea now.
- **Quality gates in the pipeline.** A quality gate is an automated checkpoint that a change must pass to move forward.
- **Shift-right.** After release, teams monitor real behavior, review logs and error rates, and gather user feedback to learn and improve.

Here is a simplified pipeline with quality gates. Each gate mixes QA (the rule exists to prevent bad changes moving on) with QC (the checks examine the actual change):

```
 Developer      Code        Build &       Automated      Deploy to     Smoke &       Release
 commits   -->  Review  --> Unit Tests --> Checks    --> Test Env  --> Acceptance --> to
 code           (Gate 1)    (Gate 2)      (Gate 3)       (Gate 4)      Checks         Users
                                                                       (Gate 5)         |
    ^                                                                                    |
    |                                                                                    v
    +----------------  Monitoring, feedback, retrospectives (shift-right) <--------------+
```

Here is how the gates relate to QA and QC:

| Gate | What it checks | QA or QC flavor |
|---|---|---|
| Code review | Peers examine the change against team standards | Both: QA (standard followed) and QC (inspecting the product) |
| Build and unit tests | Does the code compile; do small tests pass | QC checks, enforced by a QA rule |
| Automated checks | Broader automated tests, style checks, security scans | QC checks, enforced by a QA rule |
| Test environment checks | Behavior in a realistic environment | QC |
| Acceptance checks | Does it meet the acceptance criteria | QC |
| Feedback loop | Monitoring and retrospectives | QA (improvement) using QC data |

Notice the key insight: **the gate itself (the rule "no change goes forward unless it passes") is a QA mechanism, while the checks it runs are QC activities.** This is a good example of how the two work hand in hand in modern teams.

In Scrum, the **Definition of Done** acts as a quality gate for every work item. If a story does not meet the DoD (for example, "code reviewed, tests written and passing, acceptance criteria verified"), it is not done, however nice the demo looks.

### 12. Roles and the Job-Title Confusion

The industry is not consistent with job titles. A title may mean different things at different companies. Here are the common roles and what they typically mean. Always read the actual job description.

| Role | Typical meaning |
|---|---|
| **QA Analyst** | Often someone who analyzes requirements, designs test cases, executes tests and reports defects. Despite the "QA" in the title, much of the daily work is QC (testing). Some QA analysts also do process work. |
| **QC Tester** | Someone who focuses on examining the product: executing tests, finding and reporting defects. The title "QC" is less common in software than "QA" or "Tester", but common in manufacturing. |
| **Quality Engineer (QE)** | An engineer who builds quality into the delivery process: designs test strategy, writes automation, works with CI/CD, partners with developers, and thinks about prevention as well as detection. |
| **SDET** (Software Development Engineer in Test) | A role that blends software development and testing: building test frameworks, automation and tooling. Strong coding skills are expected. |
| **QA Lead / QA Manager** | Leads the quality effort: plans testing, mentors testers, defines processes and standards, reports quality status to management, and manages risk. |

**Why the confusion?** Historically, many companies had a "QA department" that tested software at the end. The label "QA" stuck to the people who tested, even though testing is strictly a QC activity. In some companies "QA" means testers; in others it means process people; in many it means both. Meanwhile "QE" and "SDET" became popular as companies wanted engineers who could automate and shape quality earlier.

**Practical advice for your career:**

- Do not argue about titles in interviews. Ask: "What does a typical day look like for this role?"
- Be ready to explain the real distinction (what you learned today), politely, as a sign of professionalism.
- Notice how this program's name, "AI enabled Test Automation Engineer - QEA", points toward the engineering-minded end of the spectrum.

### 13. Applying QA and QC to Project 1 - QE Foundations

Project 1 is a sample web app with, among other features, login and registration. Tomorrow and through the week you will use it to practice. Today, tie the concepts to it. Here are five QA activities and five QC activities for Project 1.

#### Five QA activities for Project 1

1. **Review the login and registration requirements before testing.** Read the user stories and acceptance criteria and look for gaps: What is the password rule? What happens after too many failed attempts? Is the email unique? Raise questions early. (Prevention through requirement review, building on Tuesday's requirements analysis.)
2. **Agree a test case template and naming convention.** Decide together what every test case includes (ID, title, preconditions, steps, expected result) so the whole team writes consistently.
3. **Define a Definition of Done for Project 1 stories.** For example: acceptance criteria written, test cases reviewed, tests executed, no open critical defects, defects logged in Jira.
4. **Create a peer review checklist for test cases.** Before running tests, a teammate reviews your test cases against a short checklist (covers positive and negative paths, clear expected results, no duplicates).
5. **Run a short retrospective after the exercise.** Ask what went well, what confused the team, and what to change next time. Record one improvement action (a PDCA loop).

Other possible QA activities include agreeing a defect severity scale, a short training on how to log a good defect report, and setting a rule that a story cannot move to "Done" in Jira without the checks passing.

#### Five QC activities for Project 1

1. **Execute positive test cases for registration.** For example, register with valid details and confirm the account is created and the success message appears.
2. **Execute negative test cases for login.** For example, enter a wrong password, an empty field, or an unregistered email and confirm the app shows the correct error and does not log you in.
3. **Check the delivered feature against each acceptance criterion** and record pass or fail for each.
4. **Log defects found in Jira** with clear steps to reproduce, expected result, actual result and severity (using Tuesday's defect lifecycle).
5. **Re-test a fixed defect and perform a quick regression check** on related features, such as confirming login still works after a registration fix.

Notice that the QA list is about how you work (reviews, templates, rules, improvement), and the QC list is about checking the actual application. Wednesday's exercise on writing positive and negative test cases for login and registration is where these two worlds meet: **designing good test cases is a QA-flavored act of planning, and executing them is QC.**

### 14. Common Misconceptions

| Misconception | Reality |
|---|---|
| "QA and QC are the same thing." | They are related, but QA focuses on the process and prevention, while QC focuses on the product and detection. |
| "Testing is QA." | Testing is a QC activity. It is one important part of overall quality work. |
| "The QA team is responsible for quality." | Quality is the responsibility of the whole team. Testers provide information and expertise, but cannot "test quality into" a product that was built carelessly. |
| "If we test enough, we will find all the bugs." | Exhaustive testing is not possible. (This is one of the testing principles we will study soon.) QA reduces the number of defects introduced, which testing alone cannot do. |
| "QA activities slow the team down." | Well-chosen QA activities save time overall by reducing rework and failures, as the cost of quality example showed. |
| "Automation replaces QA/QC." | Automation is a tool that performs checks faster and more often. It still needs people to decide what to check and to improve the process. |
| "Quality means zero defects." | Quality means being fit for use and meeting agreed criteria with acceptable risk. Perfection is neither achievable nor always worth the cost. |
| "QE is just a new name for tester." | QE emphasizes engineering practice: automation, pipelines, early involvement, and building quality in. The scope is broader, though in practice titles overlap. |
| "Quality is only about the code." | Quality includes requirements, design, documentation, process, usability, security and the customer experience. |

---

## Examples

### Example 1: The Same Bug, Three Approaches

A requirement says: "Password must be at least 8 characters."

- **QA approach:** During the requirement review, a tester asks, "Is there a maximum length? Are spaces allowed? What message do we show?" The requirement is clarified before any code is written. The team also adds password rules to the Definition of Done. *Result: the defect never happens.*
- **QC approach:** After the feature is built, a tester enters a 7-character password and checks that the app rejects it. The tester finds that the app accepts a 7-character password, logs the defect, and the developer fixes it. *Result: the defect was found and fixed.*
- **QE approach:** The team also adds an automated check to the pipeline that tries short passwords on every build, and monitors production for unusual registration failures. *Result: the issue is caught on every future change, within minutes.*

All three together give the best outcome.

### Example 2: A Retrospective Becomes a Process Improvement

After a sprint, the team notices that three defects were caused by missing error messages. In the retrospective they agree: "Every user story must list error scenarios in its acceptance criteria." They add this to the Definition of Done. Next sprint, they track how many error-message defects occur. This is a full PDCA loop, and it produced a QA change driven by QC data.

### Example 3: A Quality Gate in Action

A developer submits a change that breaks the existing login test. The pipeline's automated test step fails, and the pipeline refuses to deploy the change to the test environment. The developer sees the failure within minutes and fixes it. The **rule** that blocks deployment is QA. The **test that failed** is QC. No tester had to intervene, and the customer never saw the problem.

---

## Try It Activity

### Part A: Classify the Activities (Individual, 15 minutes)

For each of the 20 items below, write **QA** or **QC** (or write "Both" and explain, if you think it truly blends). Decide based on this test: *Is the activity mainly about improving or enforcing the way we work (QA), or about examining an actual product or deliverable to find problems (QC)?*

1. Writing a coding standard for the team.
2. Executing a test case that tries to log in with a wrong password.
3. Holding a sprint retrospective.
4. Logging a defect in Jira with steps to reproduce.
5. Training new team members on the test management tool.
6. Checking that a finished user story meets each of its acceptance criteria.
7. Defining the Definition of Done.
8. Re-testing a bug after the developer says it is fixed.
9. Configuring the pipeline so a build fails if automated tests fail.
10. Auditing whether the team actually performs code reviews on every pull request.
11. Running a regression test before release.
12. Creating a checklist for release readiness.
13. Inspecting the final installation package to make sure it contains the right files.
14. Choosing and rolling out a better defect tracking tool.
15. Measuring how many defects were found per module after testing.
16. Reviewing requirements for ambiguity before development starts.
17. Creating a template for test cases.
18. Performing exploratory testing on the registration page.
19. Analyzing the causes of last month's production defects and changing the process to prevent them.
20. Verifying that a response time target (for example, "page loads in under 3 seconds") is met in the test environment.

### Part B: Answer Key

| # | Answer | Reasoning |
|---|---|---|
| 1 | QA | A standard shapes how work is done; it prevents defects. |
| 2 | QC | Running a test checks the actual product. |
| 3 | QA | A retrospective improves the team's process. |
| 4 | QC | Reporting a defect is part of finding and handling product problems. |
| 5 | QA | Training improves people and process. |
| 6 | QC | Measuring the product against acceptance criteria. |
| 7 | QA | The DoD is a process agreement that defines "done". |
| 8 | QC | Re-testing checks the corrected product (confirmation of a fix). |
| 9 | QA | The gate rule is a process control. (The tests it runs are QC.) |
| 10 | QA | A process audit checks that the agreed process is followed. |
| 11 | QC | Regression testing examines the product for unintended breakage. |
| 12 | QA | A checklist is a process tool that prevents forgotten steps. |
| 13 | QC | Inspection of a finished deliverable. |
| 14 | QA | Tool and process improvement. |
| 15 | QC | Measuring and reporting on product defects. (The measurement results are often used by QA to improve the process.) |
| 16 | QA (with QC flavor) | A review happens before the product exists, so it prevents defects. It does examine a work product (the requirements), so some teams call it a QC activity on a document. In this course we treat early reviews as QA because their goal is prevention. Both answers can be defended if you explain why. |
| 17 | QA | A template standardizes how the team works. |
| 18 | QC | Exploratory testing executes the product to find defects. |
| 19 | QA | Root cause analysis with process change is preventive and improvement-focused. |
| 20 | QC | Measuring the product against a performance criterion. |

Count your score: 18 or more correct is strong, 14-17 is good, and below 14 means re-read sections 4 and 5. Items 9, 15 and 16 are intentionally on the boundary. If you got them "wrong" but can justify your reasoning, that is a sign of real understanding.

### Part C: Apply It (Pairs, 20 minutes)

1. Open the Project 1 login and registration description.
2. Without writing any test cases yet, write **three additional QA activities** (beyond the five listed in this lesson) that would help your pair deliver better quality. For each, say what defect or problem it prevents.
3. Write **three additional QC activities** and, for each, name one specific input you would try (for example, "register with an email that already exists").
4. Choose one of your QA activities and describe how you would measure whether it worked, using the PDCA cycle (Plan, Do, Check, Act).
5. Share one idea with the class.

### Part D: Cost of Quality Mini-Calculation (Individual, 10 minutes)

A small team spends $1,000 on prevention, $4,000 on appraisal, finds 20 defects internally at $150 rework each, and has 4 defects escape to customers at $800 each.

1. Calculate each category and the total. (Answer: prevention $1,000; appraisal $4,000; internal failure $3,000; external failure $3,200; total $11,200.)
2. The team then adds $1,500 of prevention (reviews and checklists). If this reduces internal defects to 12 and escaped defects to 1, what is the new total? (Answer: prevention $2,500; appraisal $4,000; internal failure $1,800; external failure $800; total $9,100.)
3. In one sentence, explain what this tells you about prevention.

---

## Knowledge Check

Try these questions first, then compare with the answers below.

**Questions**

1. Give three definitions of quality discussed in this lesson.
2. Name the four categories of the cost of quality and classify each as "good quality" or "poor quality" cost.
3. In one sentence each, define QA and QC.
4. Is testing a QA activity or a QC activity?
5. Which is preventive, QA or QC? Which is detective?
6. Give three examples of QA activities and three examples of QC activities.
7. What does "shift-left" mean?
8. What does "shift-right" mean?
9. What is a quality gate, and is it QA or QC?
10. What does the "C" in PDCA stand for, and what happens at that step?
11. Name the five standards or organizations listed in the overview and give the purpose of each in a few words.
12. Why is the title "QA Engineer" often misleading?
13. What does Quality Engineering add beyond QA and QC?
14. True or false: "The tester is solely responsible for quality." Explain.
15. Why can QC alone never be enough?

**Answers**

1. Fitness for use, conformance to requirements, and user (customer) satisfaction.
2. Prevention and appraisal are costs of good quality (the cost of doing things right). Internal failure and external failure are costs of poor quality.
3. QA is the set of planned, process-oriented, preventive activities that help ensure the way we work will produce good quality. QC is the set of product-oriented activities that examine the actual product to detect defects and verify it meets criteria.
4. Testing is a QC activity.
5. QA is preventive. QC is detective (and corrective).
6. QA: defining standards, process audits, training, checklists, reviews, quality gates, Definition of Done, retrospectives (any three). QC: running tests, inspecting deliverables, logging defects, measuring against acceptance criteria, regression checks (any three).
7. Moving quality activities earlier in the lifecycle (for example, reviewing requirements and testing early) so problems are found sooner and cost less.
8. Extending quality activities into production through monitoring, observability, user feedback and controlled rollouts to learn from real usage.
9. A quality gate is an automated or defined checkpoint that a change must pass to move forward. The rule that enforces the gate is a QA mechanism; the checks it runs are QC activities.
10. "Check". It is the step where you measure the results of the change and compare them with what you expected.
11. ISO 9001: quality management systems. ISO/IEC 25010: software quality model. CMMI: process improvement and maturity. ISO/IEC/IEEE 29119: software testing standards. ISTQB: testing certification and glossary.
12. Because much of the daily work of many "QA Engineers" is testing, which is technically QC. Titles vary between companies, so always check the job description.
13. Building quality in from the start, automation, CI/CD integration, shift-left and shift-right practices, and an engineering mindset that treats quality as a design and tooling challenge shared by the whole team.
14. False. Quality is a whole-team responsibility. Testers provide expertise and information, but developers, product owners and others all influence quality. Testing cannot add quality to something built carelessly.
15. Because QC only finds problems after they have been created, which is more expensive, and testing can never find every defect. Prevention (QA) reduces how many defects exist in the first place.

---

## Key Takeaways

- **Quality** can be viewed as fitness for use, conformance to requirements, and user satisfaction. It has many dimensions (ISO/IEC 25010 names characteristics such as functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability and portability).
- The **cost of quality** has four parts: prevention, appraisal, internal failure and external failure. Investing in prevention tends to reduce failure costs, and defects found late cost much more.
- **QA** is process-oriented, preventive, proactive and spans the whole lifecycle. Examples: standards, audits, reviews, training, checklists, quality gates, Definition of Done and retrospectives.
- **QC** is product-oriented, detective and corrective, reactive and mostly happens after something is built. Examples: testing, inspection, defect finding and measuring against criteria.
- **Testing is a QC activity.** QC is part of the overall quality effort, and **Quality Engineering** surrounds both with automation, CI/CD, shift-left and shift-right practice, and an engineering mindset.
- **PDCA** (Plan, Do, Check, Act) is the cycle of continuous improvement. QC data feeds the Check step, and QA decisions drive Plan and Act.
- **ISO 9001, ISO/IEC 25010, CMMI, ISO/IEC/IEEE 29119 and ISTQB** each serve a different purpose: quality management, software quality model, process maturity, testing standards and testing certification/vocabulary.
- In **Agile and DevOps**, quality is a team responsibility, testing is continuous, and quality gates in the pipeline enforce standards automatically.
- **Job titles are inconsistent.** QA Analyst, QC Tester, QE, SDET and QA Lead can mean different things at different companies, so focus on the actual responsibilities.
- For **Project 1**, QA work (reviewing requirements, templates, Definition of Done, review checklists, retrospectives) and QC work (executing positive and negative tests, checking acceptance criteria, logging defects, re-testing) support each other.
- **You need both prevention and detection.** Neither alone is enough.

### What Comes Next

In the upcoming lessons you will go deeper into the ideas this lesson only pointed toward: the difference between **verification and validation**, the precise meaning of **error, defect and failure**, and the **principles of testing**. Later in the curriculum you will learn the details of **test automation**. Today's QA/QC framework is the foundation that makes those topics easier to place in context.

---

## Additional Resources

- **ISTQB Glossary** (official definitions of testing and quality terms, including quality assurance, quality control and testing): https://glossary.istqb.org/
- **ASQ: Quality Assurance vs. Quality Control** (an overview from the American Society for Quality, a long-established quality organization): https://asq.org/quality-resources/quality-assurance-vs-quality-control
- **ASQ: Cost of Quality** (explains prevention, appraisal, internal failure and external failure costs): https://asq.org/quality-resources/cost-of-quality
