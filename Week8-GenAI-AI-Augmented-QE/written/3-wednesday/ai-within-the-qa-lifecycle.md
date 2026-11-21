# AI within the QA Lifecycle

## Learning Objectives

By the end of this lesson you will be able to:

- Recall the phases of the **Software Testing Life Cycle (STLC)** and describe the main inputs, activities and outputs of each phase.
- Describe, phase by phase, **where an AI assistant helps**, **where it can hurt**, and **what the tester must always own**.
- Distinguish three **levels of AI involvement** (assist, augment, autonomous) and explain why today's QA teams keep a human in the loop at every phase.
- Explain **error propagation**: why small, unchecked AI mistakes early in the lifecycle grow into large problems later, and calculate the effect with simple arithmetic.
- Apply the rule **"let code count, let AI write"** to defect reports and test summary reports.
- Use small Python programs to support AI-augmented QA: a **risk-priority table**, a **defect-report fact check**, **failure-log clustering** with TF-IDF and k-means, a **summary-report number check** and an end-to-end **traceability check**.
- Map today's remaining lessons (requirements, test cases, test data, automation, human validation, responsible use) onto the lifecycle so you know where each one fits.

---

## Why This Matters

On Monday you learned what AI, machine learning and generative AI are, and you saw a first list of ways GenAI shows up in Quality Engineering (QE). On Tuesday you learned how to *talk* to a large language model (LLM) well: be specific, give context, lock the format, show examples, and watch for common failure modes. You also used AI as a test design thinking partner.

Today we zoom out. Testing is not one activity; it is a **lifecycle**. A tester reads requirements, plans, designs tests, prepares data and environments, runs tests, reports defects and finally tells the team whether the product is ready. AI can help in every one of those phases, but it helps in *different ways* and with *different risks* in each. A prompt that is perfect for brainstorming edge cases is dangerous if you use the same "trust the output" mindset when the AI is counting test results for a release decision.

Think of the lifecycle as a **relay race**. Each phase hands a baton (an artifact: a requirement, a plan, a test case, a defect) to the next. If the AI drops the baton in phase one, for example by silently inventing a requirement, every later runner carries the wrong baton very efficiently. The faster AI makes each leg, the more important it is that someone checks each hand-over.

This lesson is the **map** for the whole day. The six lessons that follow each zoom in on one part of the map:

| Lesson (today) | Lifecycle phase it zooms into |
|---|---|
| AI-assisted requirements analysis | Requirements analysis |
| AI-generated test cases | Test design |
| AI-generated test data | Environment and data preparation |
| AI-assisted automation development | Test implementation and execution |
| Human validation of AI output | Every phase (the review step) |
| Responsible use of AI in QE | Every phase (the rules of the road) |

This directly supports the **Weekly Epic**: you are learning AI across the QA lifecycle *with human validation and responsible use*, so that on Thursday and Friday you can design and build your first QA agent. An agent is only useful if you know which lifecycle job it is doing and where its output goes next. It also supports **Project 2 (Test Automation Framework)**: our generic e-commerce web app (login, search, cart and checkout) will be the running example, and today's exercise asks you to generate and review AI test cases and data for Project 2 and document your corrections.

> **Scope note.** This lesson gives you the big picture. Requirements analysis, test case generation, test data generation, automation development, human validation and responsible use each get a full lesson later today, so here they are covered at overview level only. Agents, their instructions and their input/output contracts are covered on **Thursday**; validation scripts for agent output are covered on **Friday**.

---

## The Concept

### 1. A Quick Refresher: The Software Testing Life Cycle (STLC)

In Week 3 you met the **Software Testing Life Cycle (STLC)**: the ordered set of activities a test team goes through for a release, a sprint or a project. Different books and companies draw it slightly differently. The ISTQB Foundation syllabus, for example, talks about *test planning, monitoring and control, analysis, design, implementation, execution and completion*. The names vary, but the work is the same. In this lesson we use eight phases:

| # | Phase | Main question | Typical inputs | Typical outputs |
|---|---|---|---|---|
| 1 | **Requirements analysis** | What exactly must the product do, and is it testable? | User stories, acceptance criteria (AC), designs | Questions for the product owner, list of testable conditions |
| 2 | **Test planning** | What will we test, how, when, by whom, and what are the risks? | Requirements, deadlines, team size, risk information | Test plan, risk register, estimates, entry/exit criteria |
| 3 | **Test design** | Which test cases do we need? | Testable conditions, techniques (EP, BVA, ...) | Test cases with expected results, traceability to AC |
| 4 | **Environment and data preparation** | Where will tests run, with what data? | Test cases, system architecture | Test environment, test data sets |
| 5 | **Test implementation and execution** | Run the tests, manual and automated | Test cases, data, automation code | Test results (pass/fail/skip), logs, screenshots |
| 6 | **Defect reporting and triage** | What failed, why, and how serious is it? | Failed results, logs | Defect reports with severity and priority |
| 7 | **Reporting and closure** | Are we ready to release? What did we learn? | Results, defects, coverage | Test summary report, release recommendation, lessons learned |
| 8 | **Maintenance** | Keep the test assets healthy | Product changes, flaky tests | Updated tests, refactored automation |

Two ideas from Week 3 matter a lot today:

- **Entry and exit criteria.** Each phase has conditions for starting (entry) and finishing (exit). For example, "test design may start when the acceptance criteria are reviewed" or "testing is complete when all high-priority tests have passed and no critical defects are open". AI can speed up a phase, but it must not let you skip its exit criteria.
- **Traceability.** Every test case should trace back to a requirement, every result to a test case, and every defect to a failed result. Traceability is how you prove coverage and how you find gaps. As you will see in section 10, AI can quietly break traceability, so we check it with code.

In agile teams, these phases do not happen once per project. They happen in small loops inside every sprint, sometimes several times a day. That makes speed attractive, which is exactly why AI has become so common in QA, and exactly why the review habits in this lesson matter.

### 2. Three Levels of AI Involvement

Not all AI use is the same. A helpful way to describe *how much* the AI is doing is a three-level scale:

| Level | What the AI does | What the human does | Everyday analogy |
|---|---|---|---|
| **Assist** | Answers questions and makes suggestions when asked | Does the work; uses suggestions as input | A colleague you ask for ideas |
| **Augment** | Produces a first draft of a real artifact (test cases, data, code) | Reviews, corrects and approves every artifact before it is used | A junior team member whose work you review |
| **Autonomous** | Produces and *uses* artifacts without a human checking each one | Sets goals and monitors overall results | A self-driving car |

Most QA teams today work at the **assist** and **augment** levels. Why not autonomous? Three reasons, all of which you already know from Monday and Tuesday:

1. **An LLM is not a test oracle.** It predicts plausible text. Its expected results are guesses that are usually, but not always, right.
2. **LLMs are confident when they are wrong.** A wrong answer is written in the same fluent, professional style as a right one, so you cannot spot errors by tone.
3. **Accountability stays with people.** If a critical defect escapes to production, "the AI said it was fine" is not an acceptable answer to your manager, your customer or a regulator.

Two related terms you will hear in industry:

- **Human-in-the-loop (HITL):** a human must review or approve the AI's output *before* it is used. This is the augment level.
- **Human-on-the-loop:** the AI acts on its own, and a human *monitors* and can step in. This is closer to the autonomous level and is only appropriate for low-risk, easily reversible tasks (for example, an AI that suggests labels for failed tests in a dashboard, where a wrong label costs little).

A good rule: **the higher the risk and the harder it is to undo, the more human review you need.** Choosing which tests to run in a release candidate is high-risk. Suggesting a name for a test function is low-risk. The full human review process, including a checklist and a way of recording corrections, is the subject of the later lesson *Human Validation of AI Output*.

Here is a tiny Python model of the lifecycle with the level of AI involvement we recommend for each phase. It is simple on purpose: it is a way of writing your team's agreement down so that everyone can see it.

```python
# lifecycle_map.py
from dataclasses import dataclass


@dataclass
class PhaseAI:
    phase: str
    ai_helps_with: str
    human_owns: str
    level: str  # "assist", "augment" or "autonomous"


LIFECYCLE = [
    PhaseAI("Requirements analysis", "spot ambiguity, draft questions",
            "answers from the product owner", "assist"),
    PhaseAI("Test planning", "draft risk list, estimates, plan outline",
            "scope, priorities, sign-off", "assist"),
    PhaseAI("Test design", "draft test cases from acceptance criteria",
            "expected results (the oracle)", "augment"),
    PhaseAI("Environment and data", "generate synthetic test data",
            "data rules, privacy", "augment"),
    PhaseAI("Execution", "write and fix automation code",
            "what runs, reviewing the code", "augment"),
    PhaseAI("Defect reporting", "draft reports, cluster failures",
            "is it really a defect? severity", "assist"),
    PhaseAI("Reporting and closure", "write summary narrative",
            "the numbers and the release advice", "assist"),
]

for p in LIFECYCLE:
    print(f"{p.phase:<22} | {p.level:<8} | AI: {p.ai_helps_with}")
    print(f"{'':<22} | {'':<8} | Human: {p.human_owns}")

autonomous = [p.phase for p in LIFECYCLE if p.level == "autonomous"]
print("\nPhases where AI acts without review:", autonomous or "none")
```

Output:

```text
Requirements analysis  | assist   | AI: spot ambiguity, draft questions
                       |          | Human: answers from the product owner
Test planning          | assist   | AI: draft risk list, estimates, plan outline
                       |          | Human: scope, priorities, sign-off
Test design            | augment  | AI: draft test cases from acceptance criteria
                       |          | Human: expected results (the oracle)
Environment and data   | augment  | AI: generate synthetic test data
                       |          | Human: data rules, privacy
Execution              | augment  | AI: write and fix automation code
                       |          | Human: what runs, reviewing the code
Defect reporting       | assist   | AI: draft reports, cluster failures
                       |          | Human: is it really a defect? severity
Reporting and closure  | assist   | AI: write summary narrative
                       |          | Human: the numbers and the release advice

Phases where AI acts without review: none
```

How the code works:

- `@dataclass` (from the standard library module `dataclasses`) automatically creates an `__init__` method for the class, so `PhaseAI("Requirements analysis", ...)` stores the four values as attributes. It saves you writing boilerplate.
- `LIFECYCLE` is a plain list of `PhaseAI` objects, one per phase.
- In the f-strings, `{p.phase:<22}` means "left-align in a column 22 characters wide". That is how the output lines up into columns.
- The last two lines use a **list comprehension** to collect the names of phases marked `"autonomous"`. The expression `autonomous or "none"` prints `"none"` when the list is empty, because an empty list counts as false in Python.

Notice that the phases where the AI produces artifacts that are *used directly* (test cases, data, code) are marked **augment**, not assist. That is where most of today's review effort goes.

### 3. Why Review Every Hand-Over: Error Propagation

Let us put a number on the relay race idea. Suppose an AI assistant is used at four hand-overs in a row:

1. It reads the user story and lists the testable conditions.
2. It turns the conditions into test cases.
3. It generates test data for those test cases.
4. It writes automation code for the test cases.

Suppose that at each step the AI's output is **90% correct** (which is optimistic for some tasks and pessimistic for others; the exact number does not matter, the shape does). If nobody checks anything, the chance that a given test is correct *all the way through* is the product of the four steps:

```text
0.9 x 0.9 x 0.9 x 0.9 = 0.6561   (about 65.6%)
```

Worked out step by step:

| Steps without review | Calculation | Chance still correct |
|---|---|---|
| 1 | 0.9 | 90.0% |
| 2 | 0.9 x 0.9 | 81.0% |
| 3 | 0.81 x 0.9 | 72.9% |
| 4 | 0.729 x 0.9 | 65.6% |
| 5 | 0.6561 x 0.9 | 59.0% |

So a pipeline of individually "pretty good" steps can produce a test suite where a third of the tests are wrong in some way. Worse, the mistakes *compound* in a sneaky manner: an invented requirement in step 1 produces test cases for it in step 2, data for it in step 3 and code for it in step 4. Each later step looks perfectly consistent with the one before, so nothing looks wrong. Everyone has worked very efficiently on the wrong thing.

Now suppose a human review after each step catches most mistakes and brings each step back to, say, 99% correct. Four reviewed steps give `0.99 x 0.99 x 0.99 x 0.99 ≈ 0.96`, about 96%. That is the whole argument for **human checkpoints between phases** in one calculation.

You can reproduce the table in one line of Python:

```python
for n in range(1, 6):
    print(n, round(0.9 ** n * 100, 1))
```

```text
1 90.0
2 81.0
3 72.9
4 65.6
5 59.0
```

Here `0.9 ** n` means "0.9 to the power n" (0.9 multiplied by itself n times), and `round(..., 1)` keeps one decimal place.

> **Key idea.** Review cost is paid once per step. Error cost is paid at every later step. Checking early is almost always cheaper than checking late. This is the familiar "shift left" idea (find problems as early as possible), applied to AI output.

### 4. Phase by Phase: Requirements Analysis and Test Planning

For each phase we will answer the same four questions: **What can AI help with? What can go wrong? What does the human own? What does a good prompt look like?**

#### 4.1 Requirements analysis

**What AI helps with.** Reading a user story and its acceptance criteria and pointing out words that cannot be tested ("fast", "user-friendly"), missing error paths, unclear roles and contradictions. Turning those findings into a list of **questions for the product owner**.

**What can go wrong.** The AI may quietly *fill in* the gaps instead of reporting them. For example, given US-310 AC4 ("The address form should be fast and user-friendly"), an AI might write a test that says "the form loads in under 2 seconds". The number 2 came from nowhere. It sounds reasonable, which is exactly why it is dangerous: it becomes a requirement nobody agreed to.

**What the human owns.** The answers. Only the product owner (or another stakeholder) can decide what "fast" means. Your job is to make sure the question is asked and the answer is recorded.

**A good prompt shape** (from Tuesday's specificity and format-locking lessons):

```text
You are a QA analyst reviewing user stories for an e-commerce web app.
Review the story between <story> tags.
List (1) words or phrases that cannot be tested as written,
(2) missing scenarios such as error paths, and (3) questions for the product owner.
Do NOT invent answers or numbers. If something is unclear, ask a question.
<story>
US-310 Shipping address ...
</story>
```

The full technique, including a Python ambiguity linter, is the subject of **AI-Assisted Requirements Analysis** later today.

#### 4.2 Test planning

Test planning answers *what, how, when, who* and, above all, *what are the risks?* AI can help draft:

- An **outline of the test plan** (scope, out of scope, approach, environments, entry and exit criteria, schedule, roles).
- A first **risk list**: things that could go wrong, with suggested likelihood and impact.
- Rough **estimates** ("how many test cases might a checkout flow need?").
- A **checklist of test types** to consider: functional, accessibility, performance, security, compatibility, and so on.

**What can go wrong.** The AI does not know your project. It does not know that the coupon code was rewritten this sprint, that last release had three payment defects, or that the business makes most of its money on Black Friday. Its risk scores are generic. Its estimates are averages from text it has seen, not measurements of your team.

**What the human owns.** Scope decisions, priorities and the sign-off of the plan. These depend on business context, history and politics that are not in any prompt.

A useful way to combine both is **risk-based testing**, which you met in Week 3. Each feature gets a **likelihood** score (how likely is it to fail?) and an **impact** score (how bad is it if it fails?). Multiplying them gives a **risk score**, and you test the highest-risk features first and most deeply.

Let us work an example by hand first. An AI assistant suggests these scores (1 = low, 5 = high) for four Project 2 features:

| Feature | Likelihood (L) | Impact (I) | Risk = L x I |
|---|---|---|---|
| US-101 Login | 3 | 5 | 15 |
| US-205 Apply coupon | 2 | 3 | 6 |
| US-310 Shipping address | 3 | 3 | 9 |
| Product search | 4 | 2 | 8 |

Sorted by risk, the AI's order is Login (15), Shipping address (9), Search (8), Coupon (6). Coupon is last.

But you know two things the AI does not: the coupon logic was **rewritten this sprint** (new code fails more often, so likelihood goes up to 4), and coupons directly change **how much money the shop collects** (impact goes up to 4). The coupon risk becomes 4 x 4 = 16, and it jumps to the top. That is the human adding context, not the human throwing the AI away. The AI gave you a fast, reasonable starting table; you corrected the two numbers that depended on knowledge only you had.

Here is the same idea in code. The AI's scores and the human's overrides are kept **separately**, so you can always see what the human changed and why:

```python
# risk_priority.py
# Likelihood and impact are scored 1 (low) to 5 (high).
# Illustrative scores an AI assistant suggested for Project 2 features:
ai_suggested = {
    "US-101 Login":            {"likelihood": 3, "impact": 5},
    "US-205 Apply coupon":     {"likelihood": 2, "impact": 3},
    "US-310 Shipping address": {"likelihood": 3, "impact": 3},
    "Product search":          {"likelihood": 4, "impact": 2},
}

# The tester's corrections, based on things the AI could not know:
human_overrides = {
    # The coupon code was rewritten this sprint and coupons hit revenue.
    "US-205 Apply coupon": {"likelihood": 4, "impact": 4},
}


def risk_table(scores):
    rows = []
    for feature, s in scores.items():
        rows.append((feature, s["likelihood"], s["impact"],
                     s["likelihood"] * s["impact"]))
    # Highest risk first; ties broken by feature name for a stable order.
    return sorted(rows, key=lambda r: (-r[3], r[0]))


final_scores = {**ai_suggested, **human_overrides}

for title, scores in [("AI draft", ai_suggested), ("After review", final_scores)]:
    print(title)
    for rank, (feature, lik, imp, risk) in enumerate(risk_table(scores), start=1):
        print(f"  {rank}. {feature:<24} L={lik} I={imp} risk={risk}")
```

Output:

```text
AI draft
  1. US-101 Login             L=3 I=5 risk=15
  2. US-310 Shipping address  L=3 I=3 risk=9
  3. Product search           L=4 I=2 risk=8
  4. US-205 Apply coupon      L=2 I=3 risk=6
After review
  1. US-205 Apply coupon      L=4 I=4 risk=16
  2. US-101 Login             L=3 I=5 risk=15
  3. US-310 Shipping address  L=3 I=3 risk=9
  4. Product search           L=4 I=2 risk=8
```

Line by line:

- `ai_suggested` is a **dictionary of dictionaries**: the outer key is the feature name, the inner dictionary holds the two scores.
- `human_overrides` contains only the features the tester changed. Keeping it separate creates an **audit trail**: anyone can see that the human changed the coupon scores and read the comment explaining why.
- `risk_table` loops over the scores with `.items()` (which gives key and value pairs), builds a tuple `(feature, likelihood, impact, risk)` for each one and sorts the list.
- `sorted(rows, key=lambda r: (-r[3], r[0]))` sorts by a **key**. The `lambda` is a tiny anonymous function. For each row `r` it returns a tuple: `-r[3]` (the risk score, negated so that the biggest comes first) and `r[0]` (the feature name, used only to break ties). Python compares tuples element by element.
- `{**ai_suggested, **human_overrides}` merges two dictionaries. The `**` "unpacks" each dictionary into the new one; when both have the same key, the **later** one wins. So the human's values replace the AI's for the coupon only.
- `enumerate(..., start=1)` gives a counter alongside each row, which we use as the rank.

The lesson is not the code; it is the **pattern**: AI proposes, human adjusts with reasons, and both versions stay visible.

### 5. Phase by Phase: Test Design, Data and Execution

These three phases are where AI produces the most *concrete* artifacts, so they each get a full lesson later today. Here is the overview.

#### 5.1 Test design

**AI helps with:** turning acceptance criteria into documented test cases (ID, title, preconditions, steps, expected result, priority, link to the AC), suggesting positive, negative and edge cases, and laying them out in a test-management-friendly format. On Tuesday you used AI to apply individual techniques (EP, BVA, decision tables); today's **AI-Generated Test Cases** lesson is about turning that into complete, traceable test case *suites*.

**What can go wrong:** wrong expected results (the AI is not an oracle), duplicate tests with different wording, tests for requirements that do not exist, and acceptance criteria with no tests at all.

**Human owns:** expected results, coverage decisions and traceability.

#### 5.2 Environment and data preparation

**AI helps with:** suggesting categories of test data (valid, invalid, boundary, unusual characters), generating synthetic records, and writing scripts or configuration for test environments.

**What can go wrong:** data that *looks* valid but is not (a "credit card number" that fails the checksum, a date like 31 April), data that accidentally contains real personal information, and data that is not reproducible from one run to the next.

**Human owns:** the data rules, privacy decisions and the choice of environment. The full story is in **AI-Generated Test Data** later today.

#### 5.3 Test implementation and execution

**AI helps with:** turning a manual test case into Playwright and pytest code (Week 4), generating page objects, suggesting locators, writing fixtures, and explaining or fixing failing code (Tuesday's AI-assisted coding and debugging lesson).

**What can go wrong:** brittle locators, hard-coded `time.sleep(...)` waits, assertions that are too weak to fail, hard-coded passwords, and code that "passes" because it never really checks anything.

**Human owns:** deciding what runs where (local, CI, which environment), and reviewing every line of automation before it is merged. The full story is in **AI-Assisted Automation Development** later today.

Note what is **not** on the AI's side of the line in any of these phases: the decision that a test result is *correct*. Executing tests is something a machine (pytest, Playwright, a CI server) does very well and deterministically. Judging whether the expected result was right in the first place is a human job.

### 6. Phase by Phase: Defect Reporting

When a test fails, a tester writes a **defect report** (also called a bug report). In Week 3 you learned what a good report contains: a clear title, steps to reproduce, expected result, actual result, environment, severity and priority, and attachments such as screenshots or logs.

Writing good reports is slow, and testers' raw notes are often messy. This makes defect reporting a very natural place for AI help: give the model your rough notes and ask for a well-structured report.

**What can go wrong?** The model wants to produce a *complete-looking* report. If your notes do not mention the browser, the model may simply add one ("Chrome 129") because reports usually have one. That detail is now false information in your bug tracker, and a developer may waste time trying to reproduce the bug in the wrong browser.

So we apply a principle you met on Tuesday ("do not invent; write UNKNOWN") in the prompt, and then we **check** the output with a few lines of code. Here are the raw notes a tester wrote while testing US-205:

```text
cart had 1 item, subtotal 50.00
typed SAVE10, clicked Apply
total still 50.00, no discount, no error message
tried 60.00 -> got 54.00, ok
build 2.3.1, staging
```

By hand, what should the report say? AC1 says SAVE10 gives 10% off a subtotal **of $50.00 or more**. A subtotal of exactly $50.00 is on the boundary, so the expected total is 50.00 x 0.9 = **$45.00**. The actual total stayed $50.00. At $60.00 the discount worked (60.00 x 0.9 = 54.00). So this looks like a classic boundary defect: the code probably uses `>` where it should use `>=` (you saw this exact bug on Tuesday). The environment we know is "staging, build 2.3.1". We do **not** know the browser.

Now the code:

```python
# defect_draft.py
import json
import re

RAW_NOTES = """\
cart had 1 item, subtotal 50.00
typed SAVE10, clicked Apply
total still 50.00, no discount, no error message
tried 60.00 -> got 54.00, ok
build 2.3.1, staging
"""

REQUIRED_FIELDS = ["title", "steps", "expected", "actual", "environment", "severity"]


def build_defect_prompt(notes: str) -> str:
    return (
        "You are a QA engineer writing a defect report for an e-commerce web app.\n"
        "Turn the tester's notes between <notes> tags into a defect report.\n"
        "Use ONLY facts that appear in the notes. If a fact is missing, write \"UNKNOWN\".\n"
        "The requirement is US-205 AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.\n"
        "Return JSON with exactly these keys: " + ", ".join(REQUIRED_FIELDS) + ".\n"
        f"<notes>\n{notes}</notes>"
    )


def fake_llm(prompt: str) -> str:
    """Stand-in for a real model. Returns an ILLUSTRATIVE canned answer."""
    return json.dumps({
        "title": "SAVE10 not applied when subtotal is exactly $50.00",
        "steps": ["Add 1 item so subtotal is $50.00", "Enter SAVE10", "Click Apply"],
        "expected": "Total is $45.00 (10% off, US-205 AC1)",
        "actual": "Total stays $50.00; no discount and no error message",
        "environment": "Staging, build 2.3.1, Chrome 129",
        "severity": "High",
    })


def check_draft(draft: dict, notes: str) -> list[str]:
    problems = []
    for field in REQUIRED_FIELDS:
        if not draft.get(field):
            problems.append(f"missing field: {field}")
    # Every number in 'actual' and 'environment' should come from the notes.
    for field in ["actual", "environment"]:
        for number in re.findall(r"\d+(?:\.\d+)*", draft.get(field, "")):
            if number not in notes:
                problems.append(f"{field}: '{number}' is not in the notes")
    return problems


prompt = build_defect_prompt(RAW_NOTES)
draft = json.loads(fake_llm(prompt))
print("Draft title:", draft["title"])
for problem in check_draft(draft, RAW_NOTES) or ["no problems found"]:
    print("CHECK:", problem)
```

Output:

```text
Draft title: SAVE10 not applied when subtotal is exactly $50.00
CHECK: environment: '129' is not in the notes
```

What is happening:

- `RAW_NOTES` is a multi-line string (triple quotes). The backslash after the opening `"""` stops Python from adding an empty first line.
- `build_defect_prompt` builds the prompt the way you learned on Tuesday: a role, a task, delimiters (`<notes>`), an explicit "do not invent" rule and a locked output format (JSON with named keys). `", ".join(REQUIRED_FIELDS)` turns the list into the text `title, steps, expected, ...`.
- `fake_llm` stands in for a real model so the example runs offline and gives the same answer every time. Its answer is **illustrative**: it is the kind of thing a real model often produces, including the invented browser version.
- `json.loads(...)` turns the JSON text into a Python dictionary (Tuesday's format locking lesson).
- `check_draft` does two cheap checks. First, every required field must be present and non-empty (`draft.get(field)` returns `None` if the key is missing, and `not None` is `True`). Second, it uses a **regular expression** to find every number in the `actual` and `environment` fields and checks that each one appears somewhere in the notes. The pattern `\d+(?:\.\d+)*` means "one or more digits, optionally followed by groups of a dot and more digits", so it matches `50.00`, `2.3.1` and `129`.
- The `or ["no problems found"]` trick prints a friendly line when the list of problems is empty.

The check found the invented `129`. Note how *narrow* the check is: it does not prove the report is correct. It catches **one** common kind of mistake (invented numbers) automatically, so that the human reviewer can spend their attention on the harder questions: Is this really a defect, or did the requirement change? Is the severity right? Is the title clear to a developer? Severity in particular is a judgement call based on business impact; the AI's "High" is a suggestion.

> **Pattern: AI drafts, code checks the facts, human judges.** You will see this three-part pattern again and again today.

### 7. Phase by Phase: Failure Triage with Clustering

In a real automation suite (Project 2 will grow to dozens, then hundreds of tests), a bad night in CI can produce many failures at once. Reading them one by one is slow. Often, many failures share **one root cause**: the staging database was down, a button's label changed, or one piece of logic broke.

Grouping similar failures is called **failure triage** or **failure clustering**. It is a perfect job for the **unsupervised learning** you met on Monday: we do not have labels saying "this failure belongs to root cause X", we just want the computer to put similar messages together. And we can turn text into numbers using **TF-IDF**, also from Monday's NLP lesson.

A quick reminder of both ideas:

- **TF-IDF** (term frequency-inverse document frequency) turns each message into a vector of numbers, one per word. A word gets a high score in a message if it appears in that message but *not* in most other messages. Words such as "ConnectionError" are distinctive; words that appear everywhere get low scores.
- **k-means** places `k` centre points and assigns each vector to the nearest centre, moving the centres until they settle. Messages with similar words end up in the same cluster.

Here are nine failure messages from an imaginary nightly run. Before reading the code, try grouping them by eye:

```python
# triage_clusters.py
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

failures = [
    "test_login_valid: TimeoutError waiting for locator 'My Account' heading",
    "test_login_locked: TimeoutError waiting for locator 'My Account' heading",
    "test_search_shoes: TimeoutError waiting for locator search results list",
    "test_coupon_save10_at_50: AssertionError expected 45.00 got 50.00",
    "test_coupon_save10_at_60: AssertionError expected 54.00 got 60.00",
    "test_coupon_two_codes: AssertionError expected error message got 45.00",
    "test_address_zip: ConnectionError staging database refused connection",
    "test_address_phone: ConnectionError staging database refused connection",
    "test_checkout_total: ConnectionError staging database refused connection",
]

# 1. Turn each error message (the part after ": ") into a TF-IDF vector
#    (Monday's NLP lesson). The token_pattern keeps words of 2+ letters, so
#    numbers such as 45.00 are ignored; stop_words drops "for", "the", ...
vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
                             stop_words="english")
X = vectorizer.fit_transform([f.split(": ", 1)[1] for f in failures])

# 2. Group similar vectors with k-means (Monday's unsupervised learning lesson).
kmeans = KMeans(n_clusters=3, n_init=10, random_state=0)
labels = kmeans.fit_predict(X)

# 3. Print each cluster with its most important words.
terms = vectorizer.get_feature_names_out()
for cluster in sorted(set(labels)):
    top = kmeans.cluster_centers_[cluster].argsort()[::-1][:3]
    print(f"Cluster {cluster} (top words: {', '.join(terms[i] for i in top)})")
    for message, label in zip(failures, labels):
        if label == cluster:
            print("   ", message.split(":")[0])
```

Output:

```text
Cluster 0 (top words: assertionerror, expected, got)
    test_coupon_save10_at_50
    test_coupon_save10_at_60
    test_coupon_two_codes
Cluster 1 (top words: refused, staging, connection)
    test_address_zip
    test_address_phone
    test_checkout_total
Cluster 2 (top words: waiting, timeouterror, locator)
    test_login_valid
    test_login_locked
    test_search_shoes
```

Step by step:

- `f.split(": ", 1)[1]` splits each line at the first `": "` and keeps the second part, the error message itself. We drop the test name so the clustering is based on *what went wrong*, not on what the test is called.
- `TfidfVectorizer(...)` creates the converter. `token_pattern` is a regular expression that decides what counts as a word: here, words of two or more letters, so numbers like `45.00` are ignored. `stop_words="english"` removes very common English words.
- `fit_transform` learns the vocabulary from all messages (*fit*) and converts each message into a vector (*transform*). `X` is a matrix with one row per failure and one column per word.
- `KMeans(n_clusters=3, n_init=10, random_state=0)` asks for 3 clusters. `n_init=10` runs the algorithm 10 times from different starting points and keeps the best result. `random_state=0` fixes the random seed so you get the same clusters every run, which matters for reproducible lessons and reproducible triage.
- `fit_predict(X)` trains the model and returns a cluster number for each failure.
- `kmeans.cluster_centers_[cluster]` is the centre of a cluster: one number per word. `argsort()` returns the word positions sorted from smallest to largest; `[::-1]` reverses that, and `[:3]` takes the first three. These are the words that best describe the cluster.
- `zip(failures, labels)` walks through the failures and their labels side by side.

The result tells a clear story: three failures are **assertion** problems in the coupon logic (a real product defect, probably the `>=` boundary bug from section 6), three are **connection** problems with the staging database (an environment problem, not a product defect), and three are **timeouts** waiting for elements (possibly a slow environment, possibly a changed page). Instead of nine investigations, you have three.

Important limits, so you use this well:

- **You chose k = 3.** k-means does not decide how many root causes there are. If you pick the wrong `k`, you get merged or split groups. With real data you would try a few values and look at the result.
- **Clustering groups symptoms, not causes.** The three timeouts may have three different causes. A cluster is a *hypothesis* to investigate, not a diagnosis.
- **A human still decides** which clusters are product defects (raise a bug), which are environment problems (talk to DevOps) and which are test problems (fix the test).

A generative model can add value *on top of* this: once you have a cluster, you can ask an LLM to summarise the cluster's messages and suggest likely causes. The clustering itself, though, is cheaper, faster and more predictable with classic machine learning than with an LLM. Choosing the simplest tool that does the job well is part of using AI responsibly.

### 8. Phase by Phase: Reporting and Closure

At the end of a sprint or release, the test lead writes a **test summary report**: what was tested, how many tests passed, failed or were skipped, which defects are open, what risks remain and whether the team recommends release. Managers read the first paragraph and make decisions from it.

LLMs write fluent paragraphs, so it is tempting to paste in the raw results and ask for "a summary for the release meeting". The problem: **LLMs are poor at counting and arithmetic.** On Monday you learned that a model predicts the next token; it does not run a calculation. It may write "6 passed" when 5 passed, simply because "6 passed and 2 failed" reads naturally next to "8 tests".

The fix is a rule worth memorising:

> **Let code count, let AI write.** Compute every number with code. Give the numbers to the AI as facts. Then check that the numbers in the AI's text match the numbers you computed.

```python
# summary_report.py
import re

results = [
    {"test": "test_login_valid",         "story": "US-101", "status": "passed"},
    {"test": "test_login_wrong_password", "story": "US-101", "status": "passed"},
    {"test": "test_login_lockout",       "story": "US-101", "status": "failed"},
    {"test": "test_coupon_at_50",        "story": "US-205", "status": "failed"},
    {"test": "test_coupon_at_60",        "story": "US-205", "status": "passed"},
    {"test": "test_coupon_unknown",      "story": "US-205", "status": "passed"},
    {"test": "test_address_zip",         "story": "US-310", "status": "passed"},
    {"test": "test_address_phone",       "story": "US-310", "status": "skipped"},
]

# 1. CODE does the counting. Never ask a language model to count.
facts = {
    "total": len(results),
    "passed": sum(r["status"] == "passed" for r in results),
    "failed": sum(r["status"] == "failed" for r in results),
    "skipped": sum(r["status"] == "skipped" for r in results),
}
facts["pass_rate"] = round(100 * facts["passed"] / facts["total"])
print("Facts:", facts)

# 2. The AI only writes the narrative, from facts we give it.
prompt = (
    "Write a 3-sentence test summary for a release meeting. "
    f"Use only these facts: {facts}. Failed tests: "
    + ", ".join(r["test"] for r in results if r["status"] == "failed")
)


def fake_llm(prompt: str) -> str:
    """ILLUSTRATIVE canned answer, with a mistake on purpose."""
    return ("We ran 8 tests: 6 passed and 2 failed, a pass rate of 75%. "
            "Failures are in login lockout and the $50.00 coupon boundary. "
            "We recommend fixing both before release.")


narrative = fake_llm(prompt)

# 3. CHECK the narrative against the facts before anyone reads it.
claims = {
    "total": r"ran (\d+) tests",
    "passed": r"(\d+) passed",
    "failed": r"(\d+) failed",
    "pass_rate": r"(\d+)%",
}
for key, pattern in claims.items():
    match = re.search(pattern, narrative)
    if match and int(match.group(1)) != facts[key]:
        print(f"MISMATCH {key}: narrative says {match.group(1)}, data says {facts[key]}")
```

Output:

```text
Facts: {'total': 8, 'passed': 5, 'failed': 2, 'skipped': 1, 'pass_rate': 62}
MISMATCH passed: narrative says 6, data says 5
MISMATCH pass_rate: narrative says 75, data says 62
```

How it works:

- `sum(r["status"] == "passed" for r in results)` is a neat Python counting trick. The comparison gives `True` or `False` for each result, and Python treats `True` as 1 and `False` as 0 when adding, so the sum is the count.
- The pass rate is 5 / 8 = 0.625, so 62.5%. `round(62.5)` gives `62` because Python rounds exact halves to the nearest **even** number ("banker's rounding"). If your team prefers 63%, decide that rule in code, once, rather than leaving it to whatever the model writes.
- The prompt passes the computed `facts` dictionary into the text. The model's job is wording, not arithmetic.
- `re.search(pattern, narrative)` finds the first match of each pattern. `(\d+)` is a **capture group**: the digits inside the brackets are available as `match.group(1)`. We convert them with `int(...)` and compare with our fact.

The illustrative narrative forgot that one test was **skipped**, so it said 6 passed and 75%. A manager reading "75% pass rate, 6 passed" gets a rosier picture than reality. The check catches it in a millisecond.

What the human still owns in this phase:

- The **release recommendation.** "Fix both before release" is a business decision that weighs risk, deadlines and customer impact. The AI can draft the sentence; a person must decide whether it is true.
- The **why** behind skipped tests. A skipped test is not a passed test. Someone must explain why `test_address_phone` was skipped and whether that leaves a risk.
- **Lessons learned.** AI can summarise retrospective notes, but deciding what the team will change is a team decision.

### 9. End-to-End Traceability

Traceability is the thread that ties the whole lifecycle together:

```text
Requirement (AC)  ->  Test case  ->  Test result  ->  Defect
   US-205-AC1          TC-04           failed          BUG-18
```

- **Forward traceability** (requirement to tests) answers: *is every acceptance criterion tested?*
- **Backward traceability** (test to requirement) answers: *does every test exist for a real reason?*

AI can damage traceability in both directions. It can skip an acceptance criterion completely (a **coverage gap**), and it can produce tests that trace to requirements nobody wrote (an **invented requirement**, such as "US-205-AC5: coupons are case-insensitive"). Because each AI-generated test looks reasonable on its own, these problems are invisible until you look at the whole set. A **traceability check** in code makes them visible:

```python
# traceability.py
acceptance_criteria = [
    "US-101-AC1", "US-101-AC2", "US-101-AC3",
    "US-205-AC1", "US-205-AC2", "US-205-AC3", "US-205-AC4",
]

# Which acceptance criteria each test case claims to cover
test_cases = {
    "TC-01": ["US-101-AC1"],
    "TC-02": ["US-101-AC2"],
    "TC-03": ["US-101-AC3"],
    "TC-04": ["US-205-AC1"],
    "TC-05": ["US-205-AC1", "US-205-AC2"],
    "TC-06": ["US-205-AC3"],
    "TC-07": ["US-205-AC5"],   # an AC that does not exist!
}

last_run = {"TC-01": "passed", "TC-02": "passed", "TC-03": "failed",
            "TC-04": "failed", "TC-05": "passed", "TC-06": "passed"}

defects = {"TC-03": "BUG-17", "TC-04": "BUG-18"}

# Forward trace: AC -> tests -> results -> defects
for ac in acceptance_criteria:
    tests = [tc for tc, acs in test_cases.items() if ac in acs]
    if not tests:
        print(f"{ac}: NOT COVERED")
        continue
    parts = []
    for tc in tests:
        status = last_run.get(tc, "not run")
        bug = f" ({defects[tc]})" if tc in defects else ""
        parts.append(f"{tc} {status}{bug}")
    print(f"{ac}: " + ", ".join(parts))

# Backward trace: every test must point at a real AC
for tc, acs in test_cases.items():
    for ac in acs:
        if ac not in acceptance_criteria:
            print(f"{tc}: traces to unknown {ac} (invented requirement?)")
```

Output:

```text
US-101-AC1: TC-01 passed
US-101-AC2: TC-02 passed
US-101-AC3: TC-03 failed (BUG-17)
US-205-AC1: TC-04 failed (BUG-18), TC-05 passed
US-205-AC2: TC-05 passed
US-205-AC3: TC-06 passed
US-205-AC4: NOT COVERED
TC-07: traces to unknown US-205-AC5 (invented requirement?)
```

Reading the code:

- `test_cases` maps each test ID to a **list** of AC IDs, because one test can cover more than one criterion (TC-05 covers AC1 and AC2).
- The forward loop uses a list comprehension, `[tc for tc, acs in test_cases.items() if ac in acs]`, to find all tests whose list contains the current AC. An empty list means the AC is not covered; `continue` skips to the next AC.
- `last_run.get(tc, "not run")` looks up the test's last result and returns `"not run"` if the test has never run. `TC-07` has no result, which is another small warning sign.
- The backward loop checks every AC that every test claims to cover against the real list.

Two findings, both typical of AI-generated suites: **US-205-AC4 ("only one coupon per order") has no test**, and **TC-07 traces to an AC that does not exist**. Neither the AI nor a quick skim of the test list would have shown you this. The check also shows something useful for the summary report: US-205-AC1 has one failing and one passing test, so the coupon feature is only partly working.

In practice your test management tool (Jira with a test plugin, TestRail, Azure Test Plans and so on) produces this kind of **traceability matrix** for you. The point here is to understand *what* it checks and *why* it matters more, not less, when AI writes your tests.

### 10. Maintenance: Keeping AI-Assisted Test Assets Healthy

The lifecycle does not end at release. Products change, and tests must change with them. AI is useful here too:

- **Impact analysis.** Given a change ("the Apply button is now labelled Redeem"), an AI can suggest which tests and page objects are likely affected. You confirm by running the tests.
- **Refactoring.** Asking an AI to remove duplication in test code or to update deprecated calls (for example old Selenium `find_element_by_*` calls, which you saw on Tuesday) can save hours. You review the diff and run the suite.
- **Flaky test analysis.** Feeding an AI the history of a test that sometimes fails can surface patterns such as timing problems. You still confirm the cause.

Two maintenance risks are specific to AI-assisted test suites:

1. **Silent drift.** If AI-generated tests are regenerated every sprint, the suite can change in ways nobody reviewed. Keep generated tests in version control (Git) like any other code, and review the diff.
2. **Loss of understanding.** If nobody on the team understands why a test exists, nobody can maintain it safely. Traceability links and short comments ("covers US-205-AC1, boundary at $50.00") keep that understanding alive.

### 11. Where AI Hurts: Lifecycle Anti-Patterns

Here are the most common ways teams misuse AI across the lifecycle. Learn to recognise them; you will meet several in your own Project 2 work.

| Anti-pattern | What it looks like | Why it hurts | Better practice |
|---|---|---|---|
| **Copy-paste pipeline** | Output of one AI step is pasted straight into the next with no review | Errors propagate and compound (section 3) | Human checkpoint at every hand-over |
| **AI as oracle** | Expected results taken from the AI without checking the requirement | Tests confirm the AI's guess, not the product's rules | Expected results come from the requirement or product owner |
| **Filled-in gaps** | Vague requirements silently turned into specific numbers | Invented requirements become "truth" | Turn gaps into questions; record the answers |
| **AI does the maths** | Pass rates, counts and totals written by the model | Wrong numbers in release decisions | Let code count, let AI write (section 8) |
| **Volume over value** | 200 generated tests nobody has read | Slow suites, duplicates, false confidence | Fewer, reviewed, traceable tests |
| **Automation bias** | "It looks professional, so it must be right" | Reviewers stop looking critically | Review with a checklist (later today) |
| **Leaking data** | Real customer data or secrets pasted into a public AI tool | Privacy, legal and security incidents | Use approved tools and synthetic data (later today) |

The last two rows are big enough to have their own lessons: **Human Validation of AI Output** and **Responsible Use of AI in QE**, both later today.

### 12. Putting It Together: One Story Through the Lifecycle

Let us follow **US-205 Apply coupon** through the whole lifecycle with AI in the loop, noting the human checkpoint at each step.

| Phase | AI's contribution | Human checkpoint | What the checkpoint caught |
|---|---|---|---|
| Requirements analysis | Flags that AC4 "only one coupon per order" does not say what message the user sees | Tester asks the product owner | PO supplies the message: "Only one coupon can be used per order" |
| Test planning | Drafts a risk table | Tester raises coupon risk (rewritten code, revenue impact) | Coupon moved to top priority (section 4.2) |
| Test design | Drafts test cases from AC1 to AC4 | Tester runs the traceability check | AC4 not covered; one test traced to invented AC5 (section 9) |
| Data | Suggests subtotals 49.99, 50.00, 50.01, 60.00 and odd codes | Tester recalculates expected totals by hand | All good; adds lowercase "save10" as a question for the PO |
| Automation | Generates Playwright tests | Tester reviews code before merge | Replaces a `time.sleep(3)` with a web-first assertion |
| Execution and triage | Clusters 9 nightly failures into 3 groups | Tester investigates each group | One real defect (boundary), one environment issue, one to investigate (section 7) |
| Defect reporting | Drafts BUG-18 from notes | Code fact-check, then human review | Invented "Chrome 129" removed (section 6) |
| Reporting | Writes summary narrative | Code checks numbers; lead decides on release | Wrong pass rate corrected (section 8) |

Look at the right-hand column. **Every single phase** had something worth catching, and none of the catches needed advanced tools. They needed a human who knew the requirement, a few lines of Python, and the habit of checking each hand-over.

### 13. Connecting to Project 2

For Project 2 (Test Automation Framework) you are building a framework against a generic e-commerce web app. Today's exercise asks you to generate and review AI test cases and test data for Project 2 and **document your corrections**. As you work, keep this lifecycle map in mind:

- Write down, for each AI-assisted step, **which phase** you are in and **what the human checkpoint is**.
- Keep AI suggestions and your corrections **separate and visible** (like `ai_suggested` and `human_overrides` in section 4.2). This record is valuable evidence of your judgement.
- Keep **traceability** from the start: every test case gets an AC ID.
- Apply **let code count, let AI write** to any numbers in your reports.

On Thursday you will look at how a QA **agent** is put together, and on Friday you will build one. Knowing *which lifecycle job* your agent does, and *where a human checks its output*, is the most important design decision you will make.

---

## Practice Exercises

1. **Map your own lifecycle.** Copy `lifecycle_map.py` and edit it for your Project 2 team. Add a column `checkpoint` that says how the human verifies the AI's output in each phase (for example "PO answers questions" or "traceability check"). Print it.
2. **Error propagation.** Using Python, calculate the chance that an output is correct after 4 unreviewed steps if each step is 80% correct. Then calculate it if a review after each step raises each step to 98%. Write one sentence explaining the difference to a manager.
3. **Risk table.** Add two features to `risk_priority.py` ("Payment" and "Order history"). Give AI-style scores, then add a human override for one of them with a comment explaining the context the AI could not have known.
4. **Defect fact check.** Change `fake_llm` in `defect_draft.py` so that the `actual` field says "Total stays $49.99". Run the check. Does it catch the problem? Then extend `check_draft` to also check the `steps` field (hint: `" ".join(draft["steps"])`).
5. **Triage.** Add three new failure messages to `triage_clusters.py` that share a new root cause (for example "ElementNotFound: button 'Apply' not visible"). Try `n_clusters=3` and `n_clusters=4`. Which gives more useful groups? Why must a human choose?
6. **Summary check.** Extend `claims` in `summary_report.py` with a pattern for the number of skipped tests. Then change `fake_llm` to mention skipped tests correctly and confirm that no mismatches are printed.
7. **Traceability.** Add US-310 AC1 to AC4 to `traceability.py`, add test cases for three of them, and confirm the check reports the fourth as not covered.

---

## Knowledge Check

1. Name the eight STLC phases used in this lesson in order.
2. What is the difference between the *assist*, *augment* and *autonomous* levels of AI involvement? Which levels do most QA teams use today, and why?
3. Each of four unreviewed AI steps is 90% correct. Roughly what fraction of outputs is correct at the end? What does this tell you about reviews?
4. An AI suggests a likelihood of 2 for the coupon feature. Give one piece of context a tester might know that would raise it.
5. Why should a defect report prompt include "If a fact is missing, write UNKNOWN"? What kind of mistake does `check_draft` catch, and what can it *not* catch?
6. In the triage example, why do we remove the test names before clustering, and why do we set `random_state=0`?
7. Explain the rule "let code count, let AI write" with an example.
8. What are forward and backward traceability? Give one AI mistake that each one catches.
9. Name three lifecycle anti-patterns and the better practice for each.
10. Which phase's output is the riskiest to accept without review, in your opinion, and why?

<details>
<summary>Answers</summary>

1. Requirements analysis; test planning; test design; environment and data preparation; test implementation and execution; defect reporting and triage; reporting and closure; maintenance.
2. Assist: the AI suggests, the human does the work. Augment: the AI drafts real artifacts, the human reviews and approves each one. Autonomous: the AI produces and uses artifacts without per-item review. Most teams use assist and augment because an LLM is not a test oracle, it is confidently wrong in the same style as when it is right, and accountability stays with people.
3. 0.9 x 0.9 x 0.9 x 0.9 ≈ 0.656, so about two-thirds. Errors compound across hand-overs, so a checkpoint after each step is much cheaper than finding problems at the end.
4. Examples: the coupon code was rewritten this sprint; the feature had defects last release; the developer who built it has left; a big promotion is planned.
5. Because models tend to fill gaps with plausible but invented details to make the report look complete. `check_draft` catches missing fields and numbers that do not appear in the notes. It cannot tell whether the title is clear, whether the severity is right, or whether the issue is really a defect.
6. Removing the test names makes the grouping depend on what went wrong, not on what the test is called (otherwise all `test_coupon_*` tests might cluster together just because of their names). `random_state=0` fixes the randomness in k-means so the same input always gives the same clusters.
7. Compute counts, totals and percentages in code; give those numbers to the model only to write the wording; then check the numbers in the text. Example: code computes 5 passed of 8 (62%); the model wrote 6 passed (75%); the check caught the mismatch.
8. Forward: from each requirement to its tests; catches coverage gaps (US-205-AC4 not covered). Backward: from each test to its requirement; catches invented requirements (TC-07 traced to a non-existent AC5).
9. Any three from the table in section 11, for example: copy-paste pipeline → human checkpoint at each hand-over; AI as oracle → expected results from requirements; AI does the maths → let code count.
10. Many answers are acceptable if justified. A strong answer: test design expected results, because a wrong oracle turns every later step (data, automation, execution, reporting) into confident confirmation of the wrong behaviour.

</details>

---

## Glossary

- **Software Testing Life Cycle (STLC):** The ordered set of testing activities from requirements analysis to closure and maintenance.
- **Entry / exit criteria:** Conditions that must be true before a phase starts / before it is considered finished.
- **Assist / augment / autonomous:** Three levels of AI involvement: suggesting, drafting artifacts that a human approves, and acting without per-item review.
- **Human-in-the-loop (HITL):** A human reviews or approves AI output before it is used.
- **Human-on-the-loop:** The AI acts on its own while a human monitors and can intervene.
- **Error propagation:** Mistakes made early in a chain of steps being carried into, and multiplied by, later steps.
- **Risk-based testing:** Prioritising testing by risk, usually likelihood x impact.
- **Audit trail:** A record that shows what was changed, by whom and why (for example, AI scores versus human overrides).
- **Failure triage / clustering:** Grouping failed tests by similar symptoms to find shared root causes faster.
- **TF-IDF:** A way of turning text into numbers that gives high scores to words that are frequent in one document but rare across all documents.
- **k-means:** An unsupervised algorithm that groups vectors into `k` clusters around centre points.
- **Test summary report:** The end-of-cycle report of results, defects, risks and a release recommendation.
- **Let code count, let AI write:** The rule that numbers are computed by code and only the wording is generated by AI.
- **Traceability (forward / backward):** Links from requirements to tests (forward) and from tests back to requirements (backward).
- **Coverage gap:** A requirement or acceptance criterion with no test.
- **Invented requirement:** A rule that appears in AI output but not in any agreed requirement.
- **Automation bias:** The human tendency to trust the output of an automated system too much.

---

## Summary

- Testing is a **lifecycle**, and AI can help in every phase, but in different ways and with different risks. Today's other lessons zoom into requirements, test cases, data, automation, validation and responsible use.
- Most QA teams use AI at the **assist** and **augment** levels, with a **human in the loop**, because an LLM is not a test oracle and accountability stays with people.
- **Errors propagate.** Four 90%-correct unreviewed steps give about 66% correct results. A human checkpoint at each hand-over is the cheapest protection.
- In planning, **AI proposes and the human adjusts with reasons**; keep both versions visible.
- In defect reporting and summary reporting, use the pattern **AI drafts, code checks the facts, human judges**, and the rule **let code count, let AI write**.
- Classic ML (TF-IDF + k-means) is a cheap, predictable way to **cluster failures**; clusters are hypotheses for a human to investigate.
- **Traceability** checks in both directions catch the two most common AI test-suite mistakes: coverage gaps and invented requirements.
- Watch for the lifecycle **anti-patterns**: copy-paste pipelines, AI as oracle, filled-in gaps, AI doing maths, volume over value, automation bias and data leaks.

---

## Additional Resources

- ISTQB, *Certified Tester Foundation Level (CTFL) v4.0* (overview and free syllabus download; covers the test process, test activities, risk-based testing and defect management that this lesson builds on): https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0
- ISTQB, *Certified Tester – Testing with Generative AI (CT-GenAI)* (specialist syllabus v1.1 on using GenAI across testing, including prompting, risks such as hallucination and data privacy, and adopting GenAI in test organisations): https://istqb.org/certifications/gen-ai/
- scikit-learn, *Clustering text documents using k-means* (official worked example of TF-IDF + k-means on text, with notes on how the choice of settings affects cluster quality): https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html
