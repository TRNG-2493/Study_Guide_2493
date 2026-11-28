# Week 08 · Lecture 05: AI in the QA Lifecycle

**Topics:**

1. [AI within the QA Lifecycle](#topic-1)
2. [AI-Assisted Requirements Analysis](#topic-2)
3. [AI-Generated Test Cases](#topic-3)
4. [AI-Generated Test Data](#topic-4)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Work in your `week08` folder.
> 2. Today's code uses **only standard Python**: nothing to install.
>    ```bash
>    python --version
>    ```
> 3. Have your AI assistant open: **ChatGPT, Copilot Chat or Claude**.
> 4. Keep `prompts.txt` open. You'll add two more prompts today.

---

## How to Use This Handout

Same layout as before: **Definition → Key ideas → Worked example (step by step) → Checkpoint → Your turn → Common errors.** Topic 1 is a **thinking** topic (we build a table together). Topic 2 is an AI-assistant activity with an optional demo script. Topics 3 and 4 use short Python files that check AI output, a skill your AI agent will need at the end of the week.

Today we follow the **whole testing life cycle**, from requirements to test data, and at every stage we ask the same question: **"How do we check what the AI gave us?"**

**Our running example** (from Lectures 03–04):

```text
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

---

## Learning Objectives

By the end of this lecture you will be able to:

- Explain where AI can help in each phase of the **Software Testing Life Cycle (STLC)**, and why an early AI mistake **spreads** to later phases.
- Use a simple **weak-word check** and an AI review prompt to find **untestable requirements**.
- **Review AI-generated test cases** with small checks: missing fields, coverage and exact messages.
- **Validate AI-generated test data** against the rules, and generate **reproducible** data with code.

---

<a id="topic-1"></a>

# Topic 1: AI within the QA Lifecycle

## Definition

The **Software Testing Life Cycle (STLC)** is the sequence of testing activities: **requirements analysis → test planning → test design → test data and environment → test execution → defect reporting → test closure**. AI can help in **every** phase, but in different ways and with different risks. Each phase hands its output (a requirement, a test case, a defect report) to the next, like runners passing a baton in a **relay race**. If AI drops the baton early, for example by inventing a rule during requirements analysis, every later phase carries that mistake forward **very efficiently**. That's why each hand-over needs a **human check**.

## Key Ideas

1. **Three levels of AI involvement:**

   | Level | What the AI does | Example |
   |---|---|---|
   | **Assist** | Suggests; the human writes | "Here are 10 test ideas for AC1" |
   | **Draft** | Writes a first version; the human reviews and edits | A full set of test cases for US-205 |
   | **Automate** | Runs on its own; the human checks samples or results | A nightly job that summarises failures |

   The higher the level, the **stronger** your checks must be.
2. **Error propagation:** one invented rule in phase 1 becomes a wrong test case, then wrong test data, then a failing automated test, then a false bug report.
3. **Review every hand-over**, not just the final output. Catching the mistake early is cheaper.
4. **Today's lessons zoom in on the early phases:** requirements (Topic 2), test design (Topic 3) and test data (Topic 4). Lecture 06 covers automation, human validation and the rules for using AI responsibly.

## Worked Example: Trace One AI Mistake Through the Lifecycle

**The situation:** while reviewing US-205, an AI assistant confidently added: *"Coupon codes are case-insensitive, so save10 also works."* That's **not** in the story. Let's trace what happens if nobody checks. We'll build a table, one column at a time. Draw it on paper or in a spreadsheet as you follow along.

### Step 1: List the phases

| Phase |
|---|
| 1. Requirements analysis |
| 2. Test design |
| 3. Test data |
| 4. Test automation |
| 5. Execution and defect reporting |

### Step 2: Add how AI helps in each phase

| Phase | How AI helps |
|---|---|
| 1. Requirements analysis | Reviews the story, finds gaps and questions |
| 2. Test design | Drafts test cases from the acceptance criteria |
| 3. Test data | Generates input values and users |
| 4. Test automation | Writes the pytest / Playwright code |
| 5. Execution and defect reporting | Summarises failures and drafts bug reports |

### Step 3: Follow the invented rule through every phase

| Phase | How AI helps | What the invented rule causes |
|---|---|---|
| 1. Requirements analysis | Reviews the story | Adds "codes are case-insensitive" as if it were fact |
| 2. Test design | Drafts test cases | Writes TC: "lowercase save10 gives 10% off" |
| 3. Test data | Generates inputs | Adds `save10`, `Save10`, `sAvE10` as **valid** codes |
| 4. Test automation | Writes code | Writes `assert apply_coupon(100, "save10") == 90` |
| 5. Execution and defect reporting | Drafts bug reports | Test fails → files a **false bug**: "lowercase coupon rejected" |

**What to notice:** **one** invented sentence produced a wrong test case, wrong data, a failing test and a false bug report. A developer then wastes time on a "bug" that isn't one. Remember Lecture 02: the code was correct!

### Step 4: Add the human check at each hand-over

| Phase | How AI helps | What the invented rule causes | Human check that stops it |
|---|---|---|---|
| 1. Requirements analysis | Reviews the story | Adds "codes are case-insensitive" | **Is every statement in the story? If not, ask the BA.** |
| 2. Test design | Drafts test cases | TC for lowercase codes | **Does every test case trace to an AC?** |
| 3. Test data | Generates inputs | Lowercase codes marked valid | **Does every value follow a stated rule?** |
| 4. Test automation | Writes code | An assert on lowercase codes | **Does each assert match a reviewed test case?** |
| 5. Execution and defect reporting | Drafts bug reports | A false bug | **Does the bug report quote the requirement it breaks?** |

### Consolidated Result

The Step 4 table is your **lifecycle checklist**. The key lesson: the **cheapest** place to catch the mistake is **phase 1**. One question to the BA would have saved all the later work. Keep this table in your notes. Topics 2–4 turn the first three checks into code.

## Checkpoint

You've got it if you can answer: *"Where is the best place to catch an invented rule, and what single question catches it?"*
→ **Requirements analysis: "Is this statement actually in the story?"**

## Your Turn

1. **(In class, 3 min)** A different AI mistake: during test design, the AI wrote the AC2 message as `"Spend $50 to use SAVE10"` (missing `.00`). Which later phases does this mistake reach? Which human check stops it?
2. **(After class)** For each task, choose the AI **level** (assist, draft or automate) you'd be comfortable with **as a fresher**, and say why: (a) writing a bug report, (b) deciding whether a release can ship, (c) brainstorming edge cases.
3. **(After class)** Ask your AI assistant: *"List the phases of the Software Testing Life Cycle and one way AI can help in each."* Compare its list with Step 2. Did it add or skip any phases?

---

<a id="topic-2"></a>

# Topic 2: AI-Assisted Requirements Analysis

## Definition

**Requirements analysis** is checking that requirements are **clear, complete and testable** before anyone designs tests. A requirement is **testable** when you can write a test with a clear **pass/fail** result, for example "the page loads in under 2 seconds" rather than "the page loads fast". AI can help by spotting **vague words**, **missing values**, **contradictions** and **unanswered situations**, and by drafting questions for the business analyst (BA). But AI suggests; **the BA and product owner decide** what the requirement really means. A good approach is to run a simple, predictable check **first**, then ask the AI for a deeper review.

## Key Ideas

1. **Common requirement defects:**

   | Defect | Example | Why it's a problem |
   |---|---|---|
   | **Vague word** | "should load **fast**" | No pass/fail value |
   | **Missing value** | "locked after **several** failed logins" | How many? 3? 5? |
   | **Missing behaviour** | "Only one coupon per order" | What does the user **see** if they try a second one? |
   | **Weak obligation** | "**may** be locked" | Is it required or optional? |

2. **Deterministic first, AI second.** A word list always gives the same result and never invents anything, but it misses problems that aren't about words. AI catches more, but can also invent problems. Use **both**.
3. **Turn every problem into a question for the BA**, not into your own assumption.
4. **Every test traces back to a requirement.** If a test can't name its AC, something is wrong.

## Worked Example: Find Untestable Requirements

**Goal:** find untestable requirements in two stories, US-205 (coupon) and a new one, US-310 (checkout performance and login). You'll do a quick word check yourself, ask the AI for a deeper review, and compare the two.

```text
US-205 AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
US-205 AC4: Only one coupon per order.
US-310 AC1: The checkout page should load fast.
US-310 AC2: Error messages must be user-friendly.
US-310 AC3: The account may be locked after several failed logins.
```

### Step 1: The weak-word check (by hand)

Here's a list of words that **usually** signal a vague or unmeasurable requirement:

```text
fast, quickly, user-friendly, easy, several, some, may, should, appropriate, etc
```

Go through the five requirements and circle every weak word. Then fill in:

| Requirement | Weak words found |
|---|---|
| US-205 AC1 | ? |
| US-205 AC4 | ? |
| US-310 AC1 | ? |
| US-310 AC2 | ? |
| US-310 AC3 | ? |

**Why do this first:** a word list is **deterministic**: same input, same result, every time, and it never invents a problem. Teams often automate it (see Step 4).

### Step 2: Ask the AI for a deeper review

A word list only finds **words**. Now ask the AI to look at **meaning**. Paste into a new chat:

```text
You are a QA engineer reviewing requirements before test design.
For each requirement below, say whether it is testable as written.
If not, explain why in one sentence and write ONE question for the business analyst.
Do not suggest answers to your own questions.

### Requirements
US-205 AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
US-205 AC4: Only one coupon per order.
US-310 AC1: The checkout page should load fast.
US-310 AC2: Error messages must be user-friendly.
US-310 AC3: The account may be locked after several failed logins.
### End

Reply as a table: ID | Testable? | Why not | Question for the BA
```

**Why it's built this way:** a role, a precise task, the requirements fenced off with `###`, one question per problem, and a **ban on answering its own questions**, so the AI can't quietly invent the missing values.

### Step 3: Compare your check with the AI's review

Put the two side by side:

| Requirement | Your word check flagged it? | AI flagged it? | Who's right? |
|---|---|---|---|
| US-205 AC1 | | | |
| US-205 AC4 | | | |
| US-310 AC1 | | | |
| US-310 AC2 | | | |
| US-310 AC3 | | | |

Pay special attention to **US-205 AC4**. Did the word check flag it? Did the AI?

### Step 4: See the word check automated (demo)

Teams often turn Step 1 into a tiny script that runs on every new story. To try it, save it as `word_check.py` and run `python word_check.py`. It uses standard Python only. You don't need to understand every line.

```python
import re

REQUIREMENTS = {
    "US-205 AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "US-205 AC4": "Only one coupon per order.",
    "US-310 AC1": "The checkout page should load fast.",
    "US-310 AC2": "Error messages must be user-friendly.",
    "US-310 AC3": "The account may be locked after several failed logins.",
}
WEAK_WORDS = ["fast", "quickly", "user-friendly", "easy", "several", "some",
              "may", "should", "appropriate", "etc"]

for req_id, text in REQUIREMENTS.items():
    words = re.findall(r"[a-z\-]+", text.lower())          # split into lowercase words
    hits = [w for w in WEAK_WORDS if w in words]
    if hits:
        print(f"{req_id}: {hits}")
```

It prints:

```text
US-310 AC1: ['fast', 'should']
US-310 AC2: ['user-friendly']
US-310 AC3: ['several', 'may']
```

It gives the same result as your hand check, in milliseconds, every time.

### Consolidated Prompt

Add the Step 2 prompt to `prompts.txt`, with its requirements:

```text
=== Requirements review - v1 ===
Use: find untestable requirements and draft questions for the BA.
Source: Handout 05, Topic 2

--- Prompt (new chat) ---
You are a QA engineer reviewing requirements before test design.
For each requirement below, say whether it is testable as written.
If not, explain why in one sentence and write ONE question for the business analyst.
Do not suggest answers to your own questions.

### Requirements
US-205 AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
US-205 AC4: Only one coupon per order.
US-310 AC1: The checkout page should load fast.
US-310 AC2: Error messages must be user-friendly.
US-310 AC3: The account may be locked after several failed logins.
### End

Reply as a table: ID | Testable? | Why not | Question for the BA
```

The recommended routine is: **word check first, AI review second, human decision last.**

## Checkpoint

**Answer key, Step 1:**

| Requirement | Weak words |
|---|---|
| US-205 AC1 | none |
| US-205 AC4 | **none**, but it's still incomplete (see below) |
| US-310 AC1 | fast, should |
| US-310 AC2 | user-friendly |
| US-310 AC3 | several, may |

**The key lesson:** US-205 AC4 ("Only one coupon per order.") has **no** weak words, but it doesn't say what the user **sees** when they try a second coupon. That's a **meaning** problem, which a word list can't find.

**From the AI (Step 2)**, expect **something like**:

```text
| ID         | Testable? | Why not                                     | Question for the BA                                  |
|------------|-----------|---------------------------------------------|------------------------------------------------------|
| US-205 AC1 | Yes       | -                                           | -                                                    |
| US-205 AC4 | Partly    | Doesn't say what happens on a second coupon | What message is shown when a second coupon is used?  |
| US-310 AC1 | No        | "fast" has no measurable value               | What is the maximum load time, in seconds?            |
| US-310 AC2 | No        | "user-friendly" can't be measured            | What makes an error message acceptable?               |
| US-310 AC3 | No        | "may" and "several" are unclear              | Is locking required, and after how many failures?     |
```

**Mark your AI's answer:**

- ✅ AC4 flagged as incomplete. That's the one the word check missed.
- ✅ Questions, not invented answers (for example, it must **not** state "lock after 5 attempts" as fact)
- ✅ US-205 AC1 marked testable

## Your Turn

1. **(In class, 3 min)** Do the hand word check on `"Search results appear quickly in an appropriate order."` Which words do you flag? Would the AI flag anything else?
2. **(After class)** Try `"The page loads in good time."` Does the word list catch it? Why not? Ask your AI the same question. This shows the **limit** of a word list.
3. **(After class)** **False alarm:** `"Users may not apply an expired coupon."` The word list flags `may`, but "may not" here is a clear **prohibition**. Is it really vague? Write one sentence on why a human still needs to read every finding.
4. **(After class)** Rewrite US-310 AC1–AC3 so they're testable. Invent sensible values, and mark them **"(to confirm with the BA)"**.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI "answers" its own questions ("Assume 5 attempts…") | The prompt's ban was missing or ignored | Re-ask: "Do not suggest answers. Only ask questions." |
| The AI rewrites the requirements instead of reviewing them | It drifted from the task | Re-ask with the table format, as in Step 2 |
| The AI flags everything as untestable | It's being over-cautious | Ask: "Which of these could a tester write a pass/fail test for today?" |

---

<a id="topic-3"></a>

# Topic 3: AI-Generated Test Cases

## Definition

A **test case** is a documented check with an **ID**, the **requirement** it covers, **steps**, **test data** and an **expected result**. AI can draft a full set of test cases from a user story in seconds, saving lots of typing, but the draft often contains **missing fields**, **uncovered criteria**, **wrong or paraphrased messages**, **duplicates** and **invented rules**. Reviewing an AI draft is a **systematic** activity: check the structure with code, then check the **meaning** yourself, case by case, against the requirement.

## Key Ideas

1. **The anatomy of a good test case:**

   | Field | Example |
   |---|---|
   | ID | TC-02 |
   | Requirement (AC) | US-205 AC1 |
   | Title | SAVE10 on exactly $50.00 |
   | Steps | 1. Add items to the cart totalling $50.00. 2. Enter SAVE10. 3. Click Apply. |
   | Expected result | Total is $45.00 |

2. **What AI typically gets right:** structure, wording and many positive cases. **What it typically gets wrong:** boundaries, **exact** messages, uncovered criteria, and **invented** rules.
3. **Let code check structure; let humans check meaning.** Code can check that fields exist, that every AC is covered, and that messages match exactly. Only a human can say whether a test **makes sense**.
4. **Exact messages matter.** Automation compares text **character by character**: "Spend $50 to use SAVE10" ≠ "Spend $50.00 to use SAVE10".

## Worked Example: Review an AI Draft with Code

**The situation:** we asked our AI assistant to *"Write test cases for US-205 with id, ac, title and expected."* Here's its draft. Create `review_cases.py`.

### Step 1: The story and the draft

```python
# Step 1: the story and the AI's draft test cases
STORY = {
    "AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "AC2": 'Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".',
    "AC3": 'Unknown codes show "Coupon code not recognised".',
    "AC4": "Only one coupon per order.",
}
draft = [
    {"id": "TC-01", "ac": "AC1", "title": "SAVE10 on $100.00", "expected": "Total is $90.00"},
    {"id": "TC-02", "ac": "AC1", "title": "SAVE10 on exactly $50.00", "expected": "Total is $45.00"},
    {"id": "TC-03", "ac": "AC2", "title": "SAVE10 on $49.99",
     "expected": 'Total is $49.99 and "Spend $50 to use SAVE10" is shown'},
    {"id": "TC-04", "ac": "AC3", "title": "Unknown code BOGUS",
     "expected": 'Message "Coupon code not recognised" is shown'},
    {"id": "TC-05", "ac": "AC3", "title": "Lowercase save10 is accepted", "expected": ""},
]
```

**What this code does:**

- `STORY` maps each AC ID to its text. AC2 and AC3 contain quoted messages, so we wrap those strings in **single** quotes `'...'` so the double quotes inside are kept.
- `draft` is the AI's answer as a **list of dictionaries** (we kept the steps out to keep the example short).
- Read the draft yourself first: it **looks** professional.

### Step 2: Check required fields

```python
# Step 2: every test case needs all fields filled in
for tc in draft:
    for field in ("id", "ac", "title", "expected"):
        if not tc.get(field):
            print(f"{tc['id']}: missing '{field}'")
```

**What this code does:**

- `tc.get(field)` returns the value, or `None` if the key doesn't exist. **Both** a missing key and an empty string `""` count as "not filled in", because `not ""` and `not None` are both `True`.
- A test case without an expected result **can't pass or fail**, so it isn't a test.

### Step 3: Check coverage

```python
# Step 3: coverage - does every AC have at least one test case?
covered = {tc["ac"] for tc in draft}
for ac in STORY:
    if ac not in covered:
        print(f"{ac}: no test case covers this criterion")
```

**What this code does:**

- `{tc["ac"] for tc in draft}` is a **set comprehension**: the set of AC IDs that appear in the draft.
- Looping over `STORY` (its keys are AC1–AC4) shows any AC that **no** test case covers. This is a mini **traceability matrix**.

### Step 4: Check exact messages

```python
# Step 4: exact messages - quoted text in an AC must be copied exactly
for tc in draft:
    if '"' in STORY[tc["ac"]]:
        message = STORY[tc["ac"]].split('"')[1]
        if message not in tc["expected"]:
            print(f"{tc['id']}: expected result does not contain \"{message}\"")
```

**What this code does:**

- If the AC a test case covers contains a quoted message, we extract it: `split('"')` cuts the text at each `"`, and `[1]` is the part **between** the first pair of quotes.
- Then we check that the **exact** message appears in the expected result. Any small difference is caught.

### Consolidated File: `review_cases.py`

```python
# Step 1: the story and the AI's draft test cases
STORY = {
    "AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "AC2": 'Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".',
    "AC3": 'Unknown codes show "Coupon code not recognised".',
    "AC4": "Only one coupon per order.",
}
draft = [
    {"id": "TC-01", "ac": "AC1", "title": "SAVE10 on $100.00", "expected": "Total is $90.00"},
    {"id": "TC-02", "ac": "AC1", "title": "SAVE10 on exactly $50.00", "expected": "Total is $45.00"},
    {"id": "TC-03", "ac": "AC2", "title": "SAVE10 on $49.99",
     "expected": 'Total is $49.99 and "Spend $50 to use SAVE10" is shown'},
    {"id": "TC-04", "ac": "AC3", "title": "Unknown code BOGUS",
     "expected": 'Message "Coupon code not recognised" is shown'},
    {"id": "TC-05", "ac": "AC3", "title": "Lowercase save10 is accepted", "expected": ""},
]

# Step 2: every test case needs all fields filled in
for tc in draft:
    for field in ("id", "ac", "title", "expected"):
        if not tc.get(field):
            print(f"{tc['id']}: missing '{field}'")

# Step 3: coverage - does every AC have at least one test case?
covered = {tc["ac"] for tc in draft}
for ac in STORY:
    if ac not in covered:
        print(f"{ac}: no test case covers this criterion")

# Step 4: exact messages - quoted text in an AC must be copied exactly
for tc in draft:
    if '"' in STORY[tc["ac"]]:
        message = STORY[tc["ac"]].split('"')[1]
        if message not in tc["expected"]:
            print(f"{tc['id']}: expected result does not contain \"{message}\"")
```

## Checkpoint

```text
TC-05: missing 'expected'
AC4: no test case covers this criterion
TC-03: expected result does not contain "Spend $50.00 to use SAVE10"
TC-05: expected result does not contain "Coupon code not recognised"
```

**Now the human review.** The code found four problems. What did it **not** find?

| Test case | Code found | Human adds |
|---|---|---|
| TC-03 | Wrong message | Fix: copy the message exactly: `"Spend $50.00 to use SAVE10"` |
| TC-05 | Empty expected | **Invented rule**: nothing says lowercase works. **Remove it and ask the BA.** The code can't know this. |
| AC4 | Not covered | Add a test case, but first ask the BA what message appears (Topic 2!) |
| — | — | **Missing boundary:** no test above the boundary at $50.01 |

## Your Turn

1. **(In class, 3 min)** Fix TC-03's expected result so it contains the exact message. Run the file again. Which message disappears?
2. **(After class)** Add a test case for AC4: `{"id": "TC-06", "ac": "AC4", "title": "Second coupon is rejected", "expected": "Only the first coupon is applied"}`. Run the checks. Is AC4 now covered? Is this expected result **confirmed** by the story, or a guess?
3. **(After class)** Add a duplicate check: print a warning if two test cases have the same `title`. (Hint: use a `set` called `seen`, like the email check in Topic 4.)
4. **(After class)** Ask your AI assistant to write test cases for US-205 using the format in Key Idea 1. Convert 3 of its test cases into the `draft` format and run your checks on them.

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `KeyError: 'AC5'` | A test case refers to an AC that isn't in `STORY` | Check the `ac` value. This could also be an AI hallucination worth reporting! |
| `IndexError: list index out of range` in Step 4 | The AC text has only one `"` | Make sure quoted messages have opening **and** closing quotes |
| `KeyError: 'id'` | A draft item has no `id` key, and the print uses `tc['id']` | Use `tc.get('id', '?')` in the print |

---

<a id="topic-4"></a>

# Topic 4: AI-Generated Test Data

## Definition

**Test data** is the input values and records that tests use: users, orders, addresses, coupon codes. AI can generate realistic-looking data in seconds, but it often breaks **hidden rules**: invalid formats, values outside allowed ranges, duplicates, or codes that don't exist (for example "UK" where the system expects the ISO country code "GB"). So the AI's data is only a **draft**: every row must be **checked against the rules** before a test uses it. And because the AI gives different data each time you ask, tests that must be **repeatable** need data that's saved or generated by code, not asked for fresh every run.

## Key Ideas

1. **Work out what data you need first:** valid data for positive tests, **deliberately invalid** data for negative tests, and **boundary** data. Each row should have a **purpose**.
2. **Never trust generated data blindly.** Check it against the rules yourself or with a small script. Don't just ask the same AI "is this data valid?".
3. **Repeatable data:** ask the AI twice and you get different data. A failing test must fail the same way tomorrow, so **save** the reviewed data (or generate it with code using a fixed **seed**).
4. **Never use real personal data.** Use `example.com` emails and made-up names (Lecture 03). The `example.com` domain is reserved for testing, so it can never reach a real person.

## Worked Example: Get Data from the AI, Then Check It

**The situation:** for **positive** sign-up tests, we need 5 **valid** users. The rules:

| Field | Rule |
|---|---|
| email | A valid email address |
| age | 18 to 120 |
| country | One of US, CA, GB, IN |
| (all rows) | Emails must be unique |

### Step 1: Ask the AI for data

Paste into a new chat:

```text
Give me 5 VALID test users for a sign-up form, as a Python list of dictionaries.
Each user has: "email" (use the example.com domain), "age" (18 to 120),
"country" (one of US, CA, GB, IN). Emails must be unique.
Reply with the Python list only.
```

**Why it's built this way:** the rules are stated exactly, the format is locked (Lecture 03) so you can paste it straight into Python, and `example.com` keeps the data safe.

### Step 2: Check the data by hand

Here's a typical AI answer. It **looks** realistic:

```python
[
    {"email": "maria.lopez@example.com", "age": 34, "country": "US"},
    {"email": "raj.patel@example",       "age": 27, "country": "IN"},
    {"email": "li.wei@example.com",      "age": 16, "country": "CA"},
    {"email": "maria.lopez@example.com", "age": 41, "country": "GB"},
    {"email": "tom.brown@example.com",   "age": 52, "country": "UK"},
]
```

Check each row against the rules table and fill in:

| Row | Email valid? | Age 18–120? | Country allowed? | Unique email? | OK? |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### Step 3: Let a short script do the checking

Checking 5 rows by hand is fine. Checking 500 isn't. Create `check_users.py`:

```python
import re

ALLOWED_COUNTRIES = {"US", "CA", "GB", "IN"}
ai_users = [                                    # paste your AI's users here
    {"email": "maria.lopez@example.com", "age": 34, "country": "US"},
    {"email": "raj.patel@example",       "age": 27, "country": "IN"},
    {"email": "li.wei@example.com",      "age": 16, "country": "CA"},
    {"email": "maria.lopez@example.com", "age": 41, "country": "GB"},
    {"email": "tom.brown@example.com",   "age": 52, "country": "UK"},
]

seen = set()
for i, user in enumerate(ai_users, start=1):
    problems = []
    if not re.fullmatch(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", user["email"]):
        problems.append("invalid email")
    if not 18 <= user["age"] <= 120:
        problems.append("age outside 18-120")
    if user["country"] not in ALLOWED_COUNTRIES:
        problems.append(f"country '{user['country']}' not allowed")
    if user["email"] in seen:
        problems.append("duplicate email")
    seen.add(user["email"])
    print(f"Row {i}: {'OK' if not problems else ', '.join(problems)}")
```

**What this code does:**

- One `if` per rule, in the same order as the rules table. Each failed rule adds a readable message to `problems`.
- `re.fullmatch(...)` checks that the **whole** email looks like `name@domain.xx`. It's a simple pattern, but enough to catch obvious mistakes. (Regex was introduced in Lecture 02.)
- `18 <= age <= 120` is Python's neat way to write a **range check**.
- Duplicates can't be spotted from one row alone, so `seen` remembers every email so far.

Then paste **your** AI's list (from Step 1) in place of the example and run it again.

### Step 4: Ask again, and see why data must be saved

Send the **same** Step 1 prompt in a **new chat**. Compare the two lists of users.

**What to notice:** different names, ages and countries. If your tests asked the AI for fresh data every run, a failure today might not happen tomorrow. That's why reviewed test data is **saved in a file** (or generated by code with a fixed seed), so every run uses exactly the same data.

### Consolidated Files

Add the Step 1 prompt to `prompts.txt`:

```text
=== Test data - valid users v1 ===
Use: generate valid sign-up users to a set of rules (check them before use!).
Source: Handout 05, Topic 4

--- Prompt (new chat) ---
Give me 5 VALID test users for a sign-up form, as a Python list of dictionaries.
Each user has: "email" (use the example.com domain), "age" (18 to 120),
"country" (one of US, CA, GB, IN). Emails must be unique.
Reply with the Python list only.
```

`check_users.py` from Step 3 is the consolidated code.

## Checkpoint

**Answer key, Step 2:**

| Row | Problem |
|---|---|
| 1 | ✅ OK |
| 2 | ❌ Invalid email: `raj.patel@example` has no `.com` |
| 3 | ❌ Age 16 is under 18 |
| 4 | ❌ Duplicate email (same as row 1) |
| 5 | ❌ "UK" isn't allowed: the code is **GB** |

**Step 3 output** (`python check_users.py`):

```text
Row 1: OK
Row 2: invalid email
Row 3: age outside 18-120
Row 4: duplicate email
Row 5: country 'UK' not allowed
```

**Only 1 of the 5 "valid" users was actually valid.** Row 5 is a classic AI mistake: "UK" is what people say, but the official country code is "GB".

> **Wait, isn't invalid data useful?** Yes, for **negative** tests. But we asked for **valid** users. Invalid data is only useful when it's **deliberate and labelled** (for example, "Row 3: under-age user, expect *You must be 18 or older*"). Accidentally invalid data in a positive test makes the test fail for the wrong reason.

## Your Turn

1. **(In class, 3 min)** Run `check_users.py` with **your** AI's users from Step 1. How many rows were valid?
2. **(After class)** Ask your AI for a **negative** data set on purpose: *"Give 4 invalid test users, each breaking exactly ONE rule, and add a 'breaks' field naming the rule."* Paste the list into `check_users.py` (you can leave the extra field in). Does each row show exactly the problem it claims?
3. **(After class)** Ask your AI: *"What kinds of test data do I need to test a sign-up form with email, age and country? List categories only, no data."* Compare its categories with your own.
4. **(After class)** Add a check for an **empty** email (`""`). Which existing check already catches it?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `TypeError: '<=' not supported between instances of 'int' and 'str'` | The AI wrote the age as a string (`"34"`) instead of a number (`34`) | Fix the data, and note it: wrong types are a common AI data mistake |
| `NameError: name 'true' is not defined` | The AI replied in JSON (`true`/`false`/`null`) instead of Python | Ask again for a "Python list", or change to `True`/`False`/`None` |
| `SyntaxError` after pasting | The AI added text before or after the list | Paste only the part from `[` to `]` |

---

## Lecture Wrap-Up: Quick Check

1. Why does an AI mistake in requirements analysis cause problems in **later** phases?
2. Name two things a weak-word check can find and one thing it can't.
3. What three checks can code do on an AI-drafted test suite?
4. Why must AI-generated test data be checked before a test uses it?
5. Why shouldn't a test ask the AI for fresh data on every run?

<details>
<summary>Answers</summary>

1. Each phase uses the previous phase's output. An invented rule becomes a wrong test case, wrong data, a failing test and a false bug (error propagation).
2. It can find vague words ("fast") and weak obligations ("may"). It can't find **missing behaviour** (like AC4's missing message) or vague phrases that aren't on its list.
3. Required fields present, every AC covered, exact messages copied correctly. (Also duplicates.)
4. AI data often breaks hidden rules (formats, ranges, duplicates, wrong codes such as "UK"), so every row must be checked against the rules.
5. The AI gives different data each time, so failures wouldn't be repeatable. Save the reviewed data (or generate it with code and a fixed seed).

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **STLC** | Software Testing Life Cycle: the phases of testing work |
| **Error propagation** | An early mistake carried forward into later phases |
| **Testable requirement** | A requirement you can write a clear pass/fail test for |
| **Weak word** | A word that makes a requirement vague ("fast", "several", "may") |
| **Deterministic** | Always gives the same output for the same input |
| **Traceability** | Every test case links back to the requirement it checks |
| **Coverage** | Which requirements have at least one test |
| **Test data** | Input values and records used by tests |
| **Seed** | A starting number that makes "random" generation repeatable |
| **Positive / negative test data** | Data that should be accepted / should be rejected |

## Summary

- AI helps in **every STLC phase**, but mistakes **propagate**, so check every hand-over. The cheapest place to catch an invented rule is **requirements analysis**.
- For requirements, run a **deterministic check first** (weak words), then an **AI review** for meaning. Turn problems into **questions for the BA**.
- For test cases, let **code check structure** (fields, coverage, exact messages) and let **humans check meaning** (invented rules, missing boundaries).
- For test data: the AI drafts, and **you check every row against the rules**. Save reviewed data so tests are repeatable, and never use real personal data.
