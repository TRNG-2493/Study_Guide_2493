# AI-Generated Test Cases

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the difference between a **test idea**, a **test condition** and a **test case**, and why a test case is a documented, repeatable artifact rather than a one-line idea.
- Describe the **anatomy of a good test case**: ID, title, traceability, type, priority, preconditions, steps, test data and an observable expected result.
- Write a **test case generation prompt** that turns a user story and its acceptance criteria into a complete, traceable suite in a locked JSON format.
- Recognise the **typical flaws** in AI-generated test cases: invented rules, drifting messages, vague expected results, untraced cases, near-duplicates, missing acceptance criteria and happy-path bias.
- Review an AI-generated suite with small **Python checks**: field completeness, a traceability matrix with acceptance-criteria coverage, duplicate detection, expected-result checks against the requirement, and suite balance.
- Fix the suite with human decisions (keep, fix, retire, add) and a **gap-filling prompt**, then export it to **CSV** for a test management tool, to **Gherkin** and to a **pytest** file.

---

## Why This Matters

Every QA team keeps a library of test cases, in a test management tool such as TestRail, Xray or Zephyr, in spreadsheets, in Gherkin feature files or as automated tests. The test case is the unit of work that testers execute, report against and hand to automation engineers. Writing test cases by hand is slow and repetitive: one story with four acceptance criteria can need ten or more documented cases, most of them sharing the same "open the checkout page, enter the code, click Apply" steps.

Generative AI is very good at exactly this repetitive part. Given a story and a clear format, a model produces a neatly structured suite in seconds, which is why it appeared in Monday's list of GenAI applications within QE.

But this is also where AI does the most quiet damage. A generated suite **looks** finished, so it is tempting to import it straight into the test management tool. Hidden inside there are usually a few cases that test behaviour nobody asked for, a message that does not match the story, an expected result that says "works correctly", and an acceptance criterion with no test at all. A story can then be reported as "100% of test cases passed" while one of its acceptance criteria was never tested.

This lesson teaches the full loop: **prompt → draft → review → fix → export**. The AI drafts; you own the review and the final suite. That is today's theme, **AI across the QA lifecycle with human validation**, and it feeds the **Weekly Epic**: on Thursday and Friday you build your first QA agent, and generating test cases from requirements is one of the most common jobs such an agent is given. It also feeds **Project 2 (Test Automation Framework)**, where today's exercise asks you to generate and review AI test cases and data for the e-commerce app and document your corrections.

> **Scope note.** Earlier today, *AI within the QA Lifecycle* gave the big picture and *AI-Assisted Requirements Analysis* showed how to clean up the requirements themselves. This lesson starts from a story that is good enough to test and focuses on **test case artifacts**. Generating the *data* those cases need is the next lesson (*AI-Generated Test Data*); turning the cases into Playwright code is *AI-Assisted Automation Development*; and the formal **human review checklist and correction log** are in *Human Validation of AI Output*. Formal input/output contracts and JSON Schema are covered on **Thursday**, and automated validation scripts for agent output on **Friday**. Here we use plain Python checks only.

---

## The Concept

### 1. From Test Ideas to Test Cases

On Tuesday, in *AI-assisted test design*, you asked an AI to apply named techniques such as Equivalence Partitioning (EP) and Boundary Value Analysis (BVA). The output of that work was mostly **test ideas** and **test conditions**: "test a subtotal of exactly $50.00", "test an unknown code". Today we turn those into **test cases**. The words sound similar, so let us define them carefully. These definitions follow the ISTQB terminology you met in Week 3.

- **Test condition:** *what* to test. A testable aspect of the requirement, for example "the discount boundary at $50.00" or "unknown coupon codes are rejected".
- **Test case:** *how* to test one condition, written down so that anyone can run it and get the same verdict. It has preconditions, inputs (test data), steps and an expected result.
- **Test procedure (or test script):** the order in which one or more test cases are run, sometimes with setup and cleanup. When a test case is automated, the code is often also called a test script.

An analogy: a **test condition** is "make a cake for six people". A **test case** is the recipe: ingredients (test data), what must be ready first (preconditions), steps, and what the result should look like (expected result). Two testers following the same test case should reach the same pass or fail verdict.

This matters for AI because a model asked for "test cases" will produce anything from one-line ideas to long scripts. Unless you name the exact **fields** you want, you get a mixture that cannot be imported, reviewed or traced.

### 2. The Anatomy of a Good Test Case

Most teams and tools use a similar set of fields. The international standard for test documentation, ISO/IEC/IEEE 29119-3, describes test case specifications with the same core ideas: an identifier, the item and requirement being tested, preconditions, inputs, expected results and priority. Here is the field set we will use in this lesson:

| Field | What it holds | Why it matters | Good example | Bad example |
|---|---|---|---|---|
| `id` | A unique, stable identifier | Lets you refer to, report on and automate the case | `TC-02` | `Test 2 (new)` |
| `title` | One line saying what is tested | Lets a reader scan the suite | `Apply SAVE10 at exactly $50.00` | `Coupon test` |
| `ac` | The acceptance criterion it traces to | **Traceability**: proves each requirement is tested | `AC1` | *(empty)* |
| `type` | positive, negative or boundary | Shows the balance of the suite | `boundary` | `normal` |
| `priority` | High, Medium or Low | Decides what runs first when time is short | `High` | `Important!!` |
| `preconditions` | The state before step 1 | Without it, results differ between testers | `Shopper is logged in; cart subtotal is $50.00` | `Have stuff in cart` |
| `steps` | Numbered actions, one action per step | Makes the case repeatable | `Enter SAVE10 in the coupon field` | `Do the coupon thing` |
| `test_data` | The exact input values | Removes guesswork; feeds data-driven automation | `{"subtotal": "50.00", "code": "SAVE10"}` | `some valid amount` |
| `expected_result` | The observable outcome, from the requirement | This is the **test oracle** in written form | `Order total shows $45.00` | `Works correctly` |

Three fields deserve extra attention, because AI gets them wrong most often:

- **The expected result must be observable and specific.** "Works correctly" can never fail, and a test that cannot fail is not a test. Name an exact total, the exact message text (quoted **word for word** from the story), a page or a state.
- **The expected result must come from the requirement, not the model.** An LLM predicts plausible text; it is not a test oracle. "Order total shows $72.00" was not calculated, it was predicted. Your review must make sure it is right every time.
- **Traceability must be explicit.** Each case names its acceptance criterion, so you can build a **traceability matrix** and answer "Is every requirement tested?" and "If this requirement changes, which tests change?"

Let us look at one complete, well-written test case, in plain text, before we involve any AI:

```text
ID:             TC-02
Title:          Apply SAVE10 at exactly $50.00
Requirement:    US-205 AC1
Type:           boundary
Priority:       High
Preconditions:  Shopper is logged in; cart subtotal is $50.00
Steps:          1. Open the checkout page
                2. Enter SAVE10 in the coupon field
                3. Click Apply
Test data:      subtotal = 50.00; code = SAVE10
Expected:       Order total shows $45.00
```

A new tester could run this without asking a single question, and an automation engineer could turn each line into code. That is the standard we want the AI to meet.

### 3. The Running Example: US-205 Apply Coupon at Checkout

Throughout the lesson we use the coupon story from our generic e-commerce web app (the Project 2 application: login, search, cart and checkout):

```text
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

Behind the user interface sits the `apply_coupon` function you have used since Monday:

```python
# cart.py
def apply_coupon(total: float, code: str) -> float:
    """SAVE10 gives 10% off orders of $50.00 or more.
    Orders under $50.00 are unchanged. Unknown codes raise ValueError."""
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon: {code}")
    if total >= 50:
        return round(total * 0.9, 2)
    return total
```

Before asking any AI for help, do a quick manual pass: if you know roughly what a good answer looks like, you will notice when the AI's answer is wrong.

| AC | Test conditions you would expect | Minimum number of cases |
|---|---|---|
| AC1 | A subtotal well above $50.00 gets 10% off; the boundary $50.00 itself gets 10% off | 2 |
| AC2 | The value just under the boundary ($49.99) is unchanged and shows the "Spend $50.00..." message | 1 |
| AC3 | An unknown code shows "Coupon code not recognised" | 1 |
| AC4 | A second coupon on the same order is not accepted | 1 |

So a sensible minimum suite has about **five** cases. Let us also do the arithmetic by hand, because the expected results depend on it:

- $80.00 with 10% off: 80.00 × 0.9 = **72.00**
- $50.00 with 10% off: 50.00 × 0.9 = **45.00**
- $49.99 is under $50.00, so it stays **49.99**

Write these numbers down. In a few minutes you will compare them with what the AI says.

Notice also what the story does **not** say: is the code case-sensitive? What happens with an empty cart? What message appears when a second coupon is tried? These **gaps** go to the product owner as questions (earlier today, *AI-Assisted Requirements Analysis*). A good test case generator must do the same and never quietly fill in the answers.

### 4. What AI Does Well, and What It Gets Wrong

AI is useful here for **speed** (a full draft in seconds), **consistent structure** (every field filled, which humans often forget), **breadth** (it suggests conditions you had not listed) and **tedious reformatting** (plain steps to Gherkin). Its weaknesses are just as predictable. Learn this table well; the checks later in the lesson are built around it.

| Flaw | What it looks like | Why it happens | How we will catch it |
|---|---|---|---|
| **Invented rule** | "Coupon code is not case-sensitive", expected: discount applied for `save10` | The model fills gaps with what is *common* in other apps | Recompute the expected result from the requirement; flag assumptions |
| **Message drift** | Expected "Invalid coupon" instead of "Coupon code not recognised" | The model paraphrases; it does not copy exactly unless told | Every quoted message must appear word for word in the story |
| **Vague expected result** | "Verify it works correctly" | Filling the field with something plausible-sounding | Search for vague phrases |
| **Untraced case** | `ac` is empty | The case came from the model's general knowledge, not the story | Field completeness check; traceability matrix |
| **Missing coverage** | No test for AC4 | Some ACs are harder to test, so the model skips them | Traceability matrix: an AC with zero tests is a gap |
| **Near-duplicate** | "...above $50.00" and "...over $50.00" with $80 and $100 | The model pads the suite to look thorough | Title similarity and same-partition checks |
| **Happy-path bias** | Most cases are positive | Training text contains more success stories than failures | Count cases by type |
| **Inconsistent data** | Title says $50.00, test data says 55.00 | Each field is generated separately | Compare fields (a good practice exercise) |

Almost every AI-generated suite of more than a handful of cases contains at least one of these. That is not a reason to avoid AI; it is a reason to **review** systematically.

### 5. Writing a Test Case Generation Prompt

Everything you learned on Tuesday applies here: a clear persona, specific context, delimiters around the requirement, explicit rules and a locked output format. Let us build the prompt in Python so that it is reusable and versionable (you saw in *Prompt engineering principles* why prompts belong in Git).

```python
# tc_prompt.py
STORY_US205 = """US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order."""

FIELDS = ["id", "title", "ac", "type", "priority", "preconditions",
          "steps", "test_data", "expected_result"]


def build_test_case_prompt(story: str, max_cases: int = 10) -> str:
    field_list = ", ".join(FIELDS)
    return f"""You are a senior QA engineer writing manual test cases for an
e-commerce web app (login, search, cart and checkout).

Write test cases for the user story between the <story> tags.

<story>
{story}
</story>

Rules:
1. Every test case must trace to exactly one acceptance criterion (AC1, AC2, ...).
2. Cover every acceptance criterion at least once.
3. Include positive, negative and boundary cases. Money has a precision of $0.01.
4. Expected results must be specific and observable: exact totals or the
   exact message text from the story. Never write "works correctly".
5. Do NOT invent behaviour the story does not state. If something is unclear,
   add it to "open_questions" instead of writing a test for it.
6. At most {max_cases} test cases.

Return ONLY a JSON object with two keys:
"test_cases": a list of objects with the keys {field_list}
  ("steps" is a list of strings, "test_data" is an object,
   "type" is one of positive/negative/boundary,
   "priority" is one of High/Medium/Low)
"open_questions": a list of strings."""


if __name__ == "__main__":
    prompt = build_test_case_prompt(STORY_US205)
    print(prompt[:420])
    print("...")
    print(f"Prompt length: {len(prompt)} characters")
```

Output:

```text
You are a senior QA engineer writing manual test cases for an
e-commerce web app (login, search, cart and checkout).

Write test cases for the user story between the <story> tags.

<story>
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
...
Prompt length: 1402 characters
```

Code notes: the story lives in a variable so the same function works for any story. `FIELDS` is used twice, once in the prompt and later in our review code, so the prompt and the checks can never disagree about which fields exist. The **f-string** (`f"""..."""`) fills in `{story}`, `{max_cases}` and `{field_list}`; `", ".join(FIELDS)` turns the list into the text `id, title, ac, ...`; and `prompt[:420]` **slices** the first 420 characters for printing.

Each rule targets one flaw from the table:

1. **"Trace to exactly one AC"** prevents untraced cases and enables the matrix. "Exactly one" keeps cases focused: when a case testing three ACs fails, you do not know which AC broke.
2. **"Cover every AC"** reduces missing coverage (it will not eliminate it; our check catches the rest).
3. **"Positive, negative and boundary... precision of $0.01"** fights happy-path bias and defines "just under" for money ($49.99, not $49).
4. **"Exact message text"** targets vague results and message drift.
5. **"Do NOT invent... add it to open_questions"** targets invented rules. Giving the model a *place* for its doubts works better than only forbidding guesses (Tuesday's "KNOWN / ASK PO" idea).
6. **"At most 10"** stops padding with near-duplicates.

The final block is Tuesday's **format locking**, which makes the reply machine-readable for our checks.

> **Tip: one story per prompt.** Long prompts with many stories suffer from Tuesday's "lost in the middle" problem: stories in the middle get fewer and weaker tests.

### 6. Getting a Draft and Parsing It

As in previous lessons, we use a deterministic `fake_llm` instead of a live model. It always returns the same **illustrative** draft, with the kind of mistakes real assistants make, so we can practise reviewing it.

```python
# fake_llm.py
# A deterministic stand-in for a real model. The draft below is ILLUSTRATIVE:
# it imitates what an AI assistant typically produces, mistakes included.
import json

STEPS = ["Open the checkout page", "Enter {code} in the coupon field", "Click Apply"]

# (id, title, ac, type, priority, subtotal, code, expected_result)
_DRAFT = [
    ("TC-01", "Apply SAVE10 to a subtotal above $50.00", "AC1", "positive",
     "High", "80.00", "SAVE10", "Order total shows $72.00"),
    ("TC-02", "Apply SAVE10 at exactly $50.00", "AC1", "boundary",
     "High", "50.00", "SAVE10", "Order total shows $45.00"),
    ("TC-03", "Apply SAVE10 just under $50.00", "AC2", "boundary", "High",
     "49.99", "SAVE10", 'Order total shows $49.99 and the message '
     '"Spend $50.00 to use SAVE10" is displayed'),
    ("TC-04", "Apply an unknown coupon code", "AC3", "negative",
     "Medium", "80.00", "SAVE20", 'The message "Invalid coupon" is displayed'),
    ("TC-05", "Coupon code is not case-sensitive", "AC1", "positive",
     "Medium", "80.00", "save10", "Order total shows $72.00"),
    ("TC-06", "Apply SAVE10 to a subtotal over $50.00", "AC1", "positive",
     "High", "100.00", "SAVE10", "Order total shows $90.00"),
    ("TC-07", "Coupon with an empty cart", "", "negative",
     "Low", "0.00", "SAVE10", "Verify it works correctly"),
]


def fake_llm(prompt: str) -> str:
    """Return the same illustrative JSON draft for any test case prompt."""
    cases = [{"id": cid, "title": title, "ac": ac, "type": ctype,
              "priority": prio,
              "preconditions": f"Shopper is logged in; cart subtotal is ${sub}",
              "steps": [s.format(code=code) for s in STEPS],
              "test_data": {"subtotal": sub, "code": code},
              "expected_result": expected}
             for cid, title, ac, ctype, prio, sub, code, expected in _DRAFT]
    reply = {"test_cases": cases,
             "open_questions": ["Can a coupon be removed after it is applied?"]}
    return json.dumps(reply, indent=2)
```

How it works: each tuple in `_DRAFT` holds the values of one test case, and the **list comprehension** inside `fake_llm` unpacks each tuple (`for cid, title, ... in _DRAFT`) into a full test case dictionary with all nine fields. `json.dumps(..., indent=2)` then turns the Python data into a JSON **string**, exactly like the text a real model sends back. A real model returns text, never Python objects, so our code must always start by parsing text. This is what one case looks like inside that string:

```json
{
  "id": "TC-05",
  "title": "Coupon code is not case-sensitive",
  "ac": "AC1",
  "type": "positive",
  "priority": "Medium",
  "preconditions": "Shopper is logged in; cart subtotal is $80.00",
  "steps": [
    "Open the checkout page",
    "Enter save10 in the coupon field",
    "Click Apply"
  ],
  "test_data": {
    "subtotal": "80.00",
    "code": "save10"
  },
  "expected_result": "Order total shows $72.00"
}
```

The parser applies Tuesday's **defensive parsing**: models sometimes wrap JSON in a Markdown fence even when told not to, so we strip it first.

```python
# parse_suite.py
import json

from fake_llm import fake_llm
from tc_prompt import STORY_US205, build_test_case_prompt


def parse_suite(raw: str) -> dict:
    """Parse the model's reply. Strip a ```json fence if the model added one."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]        # drop the first line (```json)
        text = text.rsplit("```", 1)[0]      # drop the closing fence
    data = json.loads(text)
    if "test_cases" not in data:
        raise ValueError("Reply has no 'test_cases' key")
    return data


if __name__ == "__main__":
    reply = fake_llm(build_test_case_prompt(STORY_US205))
    suite = parse_suite(reply)
    cases = suite["test_cases"]
    print(f"{len(cases)} test cases, {len(suite['open_questions'])} open question(s)")
    for case in cases:
        print(f"{case['id']}  {case['ac'] or '--':4} {case['type']:9} {case['title']}")
```

Output:

```text
7 test cases, 1 open question(s)
TC-01  AC1  positive  Apply SAVE10 to a subtotal above $50.00
TC-02  AC1  boundary  Apply SAVE10 at exactly $50.00
TC-03  AC2  boundary  Apply SAVE10 just under $50.00
TC-04  AC3  negative  Apply an unknown coupon code
TC-05  AC1  positive  Coupon code is not case-sensitive
TC-06  AC1  positive  Apply SAVE10 to a subtotal over $50.00
TC-07  --   negative  Coupon with an empty cart
```

Code notes:

- `text.split("\n", 1)[1]` splits at the **first** newline only and keeps the rest, removing the opening fence line; `rsplit("```", 1)[0]` splits at the **last** fence and keeps what comes before it.
- `json.loads` turns JSON text into Python dictionaries and lists, and raises `json.JSONDecodeError` on invalid JSON (Tuesday showed how to respond with one re-ask).
- `case['ac'] or '--'` prints `--` when `ac` is an empty string, because an empty string counts as false. `:4` and `:9` pad values so the columns line up.
- The `if __name__ == "__main__":` block runs only when you execute the file directly, not when another file imports it. Our later scripts rely on this when they import `parse_suite`.

Save all the files in this lesson in the **same folder** so the imports work.

At first glance the draft looks good: seven cases, a mix of types, an open question. This is exactly the moment when people stop checking.

### 7. Reviewing the Draft, Step by Step

Review has two halves: **reading it yourself** and **running cheap automatic checks**. Checks never get tired but only find what they were written to find. Do both.

#### 7.1 Read it first, like a reviewer

Compare the draft with your hand analysis from section 3, asking of each case: *Which AC? Is the expected result what the story says? New condition or repeat?*

| Case | Traces to | Expected result vs. story | New condition? | First impression |
|---|---|---|---|---|
| TC-01 | AC1 | $80.00 → $72.00, matches our arithmetic | Yes | Keep |
| TC-02 | AC1 | $50.00 → $45.00, matches | Yes (boundary) | Keep |
| TC-03 | AC2 | $49.99 unchanged + exact message, matches | Yes (boundary) | Keep |
| TC-04 | AC3 | "Invalid coupon", but the story says "Coupon code not recognised" | Yes | Fix the message |
| TC-05 | AC1 | Assumes `save10` works; the story never says codes are case-insensitive | Not from the story | Invented rule |
| TC-06 | AC1 | $100.00 → $90.00 is correct arithmetic | No, same as TC-01 | Duplicate |
| TC-07 | none | "Verify it works correctly" | Not from the story | Vague, untraced |
| (none) | AC4 | | | **Gap**: no test for AC4 |

Five of the eight rows need action, in a draft that looked fine at a glance. The rest of this section automates most of this review, so your attention goes to what checks cannot see.

#### 7.2 Check 1: are all fields present and valid?

The cheapest check is structural: every field present, allowed values for `type` and `priority`, unique IDs.

```python
# check_fields.py
from fake_llm import fake_llm
from parse_suite import parse_suite
from tc_prompt import FIELDS, STORY_US205, build_test_case_prompt

ALLOWED = {
    "type": {"positive", "negative", "boundary"},
    "priority": {"High", "Medium", "Low"},
}


def check_fields(cases: list[dict]) -> list[str]:
    problems = []
    for case in cases:
        cid = case.get("id", "<no id>")
        for field in FIELDS:
            value = case.get(field)
            if value in (None, "", [], {}):
                problems.append(f"{cid}: '{field}' is missing or empty")
        for field, allowed in ALLOWED.items():
            if case.get(field) not in allowed:
                problems.append(f"{cid}: '{field}' = {case.get(field)!r} "
                                f"is not one of {sorted(allowed)}")
    ids = [case.get("id") for case in cases]
    duplicates = {i for i in ids if ids.count(i) > 1}
    for dup in sorted(duplicates):
        problems.append(f"ID {dup} is used more than once")
    return problems


if __name__ == "__main__":
    cases = parse_suite(fake_llm(build_test_case_prompt(STORY_US205)))["test_cases"]
    problems = check_fields(cases)
    print(f"{len(problems)} problem(s)")
    for p in problems:
        print(" -", p)
```

Output:

```text
1 problem(s)
 - TC-07: 'ac' is missing or empty
```

How it works:

- `case.get(field)` returns `None` instead of crashing when a key is missing, which matters because AI output can leave keys out entirely. `value in (None, "", [], {})` treats missing, empty strings, empty lists and empty dictionaries all as "empty".
- `ALLOWED` maps each restricted field to a **set** of allowed values. `!r` prints the value with quotes, which makes values like `'high'` or `'High '` (trailing space) easy to spot.
- The **set comprehension** `{i for i in ids if ids.count(i) > 1}` collects every ID used more than once.

One real problem. But TC-04, TC-05 and TC-06 all passed: correct structure says nothing about correct content.

#### 7.3 Check 2: the traceability matrix and AC coverage

A **traceability matrix** lists each requirement and the tests that cover it. We extract the ACs from the story text automatically, so the matrix always matches the current story.

```python
# trace_matrix.py
import re

from fake_llm import fake_llm
from parse_suite import parse_suite
from tc_prompt import STORY_US205, build_test_case_prompt


def acceptance_criteria(story: str) -> dict[str, str]:
    """Pull 'AC1: text' lines out of the story into {'AC1': 'text', ...}."""
    return dict(re.findall(r"^(AC\d+):\s*(.+)$", story, flags=re.MULTILINE))


def traceability_matrix(cases: list[dict], acs: dict[str, str]) -> dict[str, list[str]]:
    matrix = {ac: [] for ac in acs}          # every AC starts with no tests
    matrix["(untraced)"] = []
    for case in cases:
        key = case.get("ac") if case.get("ac") in acs else "(untraced)"
        matrix[key].append(case["id"])
    return matrix


if __name__ == "__main__":
    acs = acceptance_criteria(STORY_US205)
    cases = parse_suite(fake_llm(build_test_case_prompt(STORY_US205)))["test_cases"]
    matrix = traceability_matrix(cases, acs)

    print(f"{'AC':11} {'Tests':28} Status")
    for ac, ids in matrix.items():
        if ac == "(untraced)":
            status = "REVIEW" if ids else "ok"
        else:
            status = "covered" if ids else "GAP - no test"
        print(f"{ac:11} {', '.join(ids) or '-':28} {status}")

    covered = sum(1 for ac in acs if matrix[ac])
    print(f"\nAC coverage: {covered}/{len(acs)} = {covered / len(acs):.0%}")
```

Output:

```text
AC          Tests                        Status
AC1         TC-01, TC-02, TC-05, TC-06   covered
AC2         TC-03                        covered
AC3         TC-04                        covered
AC4         -                            GAP - no test
(untraced)  TC-07                        REVIEW

AC coverage: 3/4 = 75%
```

Unpacking the regular expression `r"^(AC\d+):\s*(.+)$"`:

- `r"..."` is a **raw string**, so backslashes are kept as typed.
- `^` and `$` mean start and end of a **line** because of `flags=re.MULTILINE`.
- `(AC\d+)` captures `AC` plus one or more digits; `:\s*` matches the colon and spaces; `(.+)` captures the rest of the line.
- `re.findall` returns tuples such as `("AC1", "SAVE10 gives...")`, and `dict(...)` turns them into keys and values.

The key trick is `{ac: [] for ac in acs}`: every AC starts with an empty list, so an untested AC stays **visibly empty**. Built only from the cases, AC4 would simply not appear, and missing things are the hardest to notice. Coverage `sum(1 for ac in acs if matrix[ac])` counts non-empty lists: 3 ÷ 4 = 75% (`:.0%` formats it as a percentage).

Two warnings about this number. First, **75% AC coverage is not "75% tested"**: one quarter of the requirement is completely untested, which is a serious finding. Second, **100% AC coverage is not proof of good testing**: TC-05 counts toward AC1 even though it tests an invented rule. Coverage numbers count links; they do not judge them.

#### 7.4 Check 3: duplicates, by text and by meaning

Duplicates waste execution time and make coverage look better than it is. We look for them in two ways.

**By text: Jaccard similarity of titles.** You met Jaccard similarity on Tuesday. It compares two sets: the size of what they share divided by the size of everything they contain together.

Jaccard(A, B) = |A ∩ B| ÷ |A ∪ B|

Let us compute it by hand for TC-01 and TC-06, using the lowercase words of each title:

- TC-01: {apply, save10, to, a, subtotal, above, $50.00}, 7 words
- TC-06: {apply, save10, to, a, subtotal, over, $50.00}, 7 words
- Shared (∩): {apply, save10, to, a, subtotal, $50.00}, 6 words
- Together (∪): the 6 shared words plus "above" and "over", 8 words
- Jaccard = 6 ÷ 8 = **0.75**

Three-quarters the same: worth a closer look.

**By meaning: same AC, same partition.** Text similarity misses reworded duplicates and can flag similar-looking cases that test different things. Tuesday's **Equivalence Partitioning** gives a stronger test: two cases with the same AC and values from the same partition test the same thing. Boundary values are always kept, because each has its own job.

```python
# duplicates.py
import re
from decimal import Decimal
from itertools import combinations

from fake_llm import fake_llm
from parse_suite import parse_suite
from tc_prompt import STORY_US205, build_test_case_prompt


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9.$]+", text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def partition(case: dict) -> tuple:
    """Which equivalence partition does this case exercise? (Tuesday's EP)"""
    code = case["test_data"].get("code", "")
    subtotal = Decimal(case["test_data"].get("subtotal", "0"))
    code_class = "valid code" if code == "SAVE10" else "other code"
    if subtotal == Decimal("50.00") or subtotal == Decimal("49.99"):
        band = f"boundary {subtotal}"          # boundaries are always kept
    else:
        band = ">= 50" if subtotal >= Decimal("50.00") else "< 50"
    return (case["ac"], code_class, band)


if __name__ == "__main__":
    cases = parse_suite(fake_llm(build_test_case_prompt(STORY_US205)))["test_cases"]

    print("1) Title similarity (Jaccard >= 0.6)")
    for a, b in combinations(cases, 2):
        score = jaccard(words(a["title"]), words(b["title"]))
        if score >= 0.6:
            print(f"   {a['id']} vs {b['id']}: {score:.2f}")

    print("2) Same AC + same partition")
    seen = {}
    for case in cases:
        key = partition(case)
        if key in seen:
            print(f"   {case['id']} repeats {seen[key]} -> {key}")
        else:
            seen[key] = case["id"]
```

Output:

```text
1) Title similarity (Jaccard >= 0.6)
   TC-01 vs TC-06: 0.75
2) Same AC + same partition
   TC-06 repeats TC-01 -> ('AC1', 'valid code', '>= 50')
```

Code notes:

- `words` keeps letters, digits, dots and dollar signs together, so `$50.00` is one token; `set(...)` removes repeats.
- `a & b` is set **intersection**, `a | b` is **union**; `if a | b else 0.0` avoids dividing by zero.
- `itertools.combinations(cases, 2)` yields every **pair** once: 7 × 6 ÷ 2 = 21 pairs.
- `Decimal` is used for money, as on Tuesday; always build it from a **string** (`Decimal("50.00")`), never from a float.
- `partition` returns a **tuple**, which can be a dictionary key, so `seen` remembers the first case per partition and reports later repeats.

Both methods agree on TC-06. The partition function is specific to this story; for another story you would describe other partitions. The point is to answer "is this really a new test?" deliberately. Note that TC-05 (`save10`) is **not** a duplicate: it is the only AC1 case with another code. It is a different kind of problem, which the next check finds.

#### 7.5 Check 4: are the expected results right?

The most important check, because the expected result is the oracle. We look for:

1. **Vague phrases** such as "works correctly" that can never fail.
2. **Message drift**: any message in double quotes must appear **word for word** in the story.
3. **Wrong or invented outcomes**: we recompute the expected total from the acceptance criteria and compare it with the draft. The recomputation is written by a **human** from the story, so it is an independent oracle, not another AI guess.

```python
# check_expected.py
import re
from decimal import Decimal, ROUND_HALF_UP

from fake_llm import fake_llm
from parse_suite import parse_suite
from tc_prompt import STORY_US205, build_test_case_prompt

VAGUE_PHRASES = ["works correctly", "works as expected", "is correct",
                 "behaves properly", "verify it works", "appropriate"]


def check_vague(case: dict) -> list[str]:
    text = case["expected_result"].lower()
    return [f"{case['id']}: vague expected result ('{p}')"
            for p in VAGUE_PHRASES if p in text]


def check_quoted_messages(case: dict, story: str) -> list[str]:
    """Every message in double quotes must appear word for word in the story."""
    quoted = re.findall(r'"([^"]+)"', case["expected_result"])
    return [f"{case['id']}: message \"{m}\" is not in the story"
            for m in quoted if m not in story]


def oracle_total(subtotal: str, code: str) -> Decimal | None:
    """Expected order total, written by a human from AC1-AC3.
    Returns None when the story says the code is rejected."""
    amount = Decimal(subtotal)
    if code != "SAVE10":                      # AC3: unknown code
        return None
    if amount >= Decimal("50.00"):            # AC1: 10% off
        return (amount * Decimal("0.9")).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return amount                             # AC2: unchanged


def check_totals(case: dict) -> list[str]:
    data = case["test_data"]
    if "subtotal" not in data or "code" not in data:
        return []
    claimed = re.search(r"total shows \$(\d+\.\d{2})", case["expected_result"])
    expected = oracle_total(data["subtotal"], data["code"])
    if claimed and expected is None:
        return [f"{case['id']}: assumes code {data['code']!r} gives a discount; "
                f"the story only names SAVE10 (invented rule? ask the PO)"]
    if claimed and Decimal(claimed.group(1)) != expected:
        return [f"{case['id']}: claims ${claimed.group(1)}, story gives ${expected}"]
    return []


if __name__ == "__main__":
    cases = parse_suite(fake_llm(build_test_case_prompt(STORY_US205)))["test_cases"]
    findings = []
    for case in cases:
        findings += check_vague(case)
        findings += check_quoted_messages(case, STORY_US205)
        findings += check_totals(case)
    for f in findings:
        print("-", f)
```

Output:

```text
- TC-04: message "Invalid coupon" is not in the story
- TC-05: assumes code 'save10' gives a discount; the story only names SAVE10 (invented rule? ask the PO)
- TC-07: vague expected result ('works correctly')
- TC-07: vague expected result ('verify it works')
```

Walking through each function:

- **`check_vague`** is a **list comprehension** with a condition, returning one finding per vague phrase found. Extend the phrase list with whatever your AI tools produce.
- **`check_quoted_messages`** captures everything between double quotes with `r'"([^"]+)"'` (`[^"]+` means "one or more characters that are not a quote") and requires each message to be a substring of the story. "Invalid coupon" is not.
- **`oracle_total`** is the heart of the check: read it next to the story (AC3, AC1, AC2). `quantize(Decimal("0.01"), ROUND_HALF_UP)` rounds to cents the way people expect for money. `Decimal | None` means it returns a `Decimal` or `None`.
- **`check_totals`** finds a claimed total with `r"total shows \$(\d+\.\d{2})"`: `\$` is an escaped dollar sign (a bare `$` means end of line), then digits, a dot and exactly two digits. `claimed.group(1)` returns the captured text, such as `"72.00"`.

Note how TC-05 is reported. The code does **not** say "TC-05 is wrong": the story is silent on `save10`, so nobody knows. What we know is that the draft **assumed** an answer, despite our prompt's rule. The response is to remove the assumption and ask the product owner. TC-01, TC-02, TC-03 and TC-06 produced no findings, agreeing with our hand arithmetic.

#### 7.6 Check 5: the balance of the suite

Finally, look at the whole suite: is it mostly happy path? Is everything High priority (meaning nothing is prioritised)?

```python
# suite_mix.py
from collections import Counter

from fake_llm import fake_llm
from parse_suite import parse_suite
from tc_prompt import STORY_US205, build_test_case_prompt

cases = parse_suite(fake_llm(build_test_case_prompt(STORY_US205)))["test_cases"]

by_type = Counter(case["type"] for case in cases)
by_priority = Counter(case["priority"] for case in cases)

print("By type:    ", dict(by_type))
print("By priority:", dict(by_priority))
share_positive = by_type["positive"] / len(cases)
print(f"Positive share: {share_positive:.0%}")
if share_positive > 0.5:
    print("Warning: more than half the suite is happy-path testing")
```

Output:

```text
By type:     {'positive': 3, 'boundary': 2, 'negative': 2}
By priority: {'High': 4, 'Medium': 2, 'Low': 1}
Positive share: 43%
```

`collections.Counter` counts how often each value appears. 3 positive cases out of 7 is 3 ÷ 7 ≈ 0.43, so 43%. It looks acceptable, but two of the three positive cases (TC-05, TC-06) are about to be removed, so re-run balance checks **after** fixing. The 50% threshold is a team choice; a validation-heavy story such as US-310 should be mostly negative cases.

#### 7.7 What the checks cannot tell you

The scripts found every problem in our table, but no script can write the missing AC4 test, decide whether an empty cart matters, or notice that "Shopper is logged in" is itself an assumption (the story never says guests cannot use coupons). Checks narrow down **where** to look; they do not replace **looking**. The formal review checklist is the subject of *Human Validation of AI Output* later today.

### 8. Fixing the Suite

Now we decide, recording each decision and its reason (the full **correction log** format comes later today):

| Case | Problem found | Decision | Reason |
|---|---|---|---|
| TC-01 | none | **Keep** | Correct, traced to AC1 |
| TC-02 | none | **Keep** | Correct boundary for AC1 |
| TC-03 | none | **Keep** | Correct boundary and exact message for AC2 |
| TC-04 | Message drift | **Fix** | Use the exact text "Coupon code not recognised" (AC3) |
| TC-05 | Invented rule (case-insensitive codes) | **Retire**, raise question | The story is silent; ask the PO before testing |
| TC-06 | Duplicate of TC-01 | **Retire** | Same AC and same partition |
| TC-07 | Untraced, vague expected result | **Retire**, raise question | Empty cart is not in the story; ask the PO |
| (new) | AC4 has no test | **Add** TC-08 | Close the coverage gap |

Open questions for the product owner, combining the model's question with ours:

1. Are coupon codes case-sensitive (does `save10` work)?
2. What should happen when a coupon is applied to an empty cart?
3. Which message is shown when a second coupon is tried (AC4)?
4. Can a coupon be removed after it is applied? (from the AI draft)

#### Never reuse IDs

We **retire** TC-05 to TC-07 rather than renumbering. IDs appear in bug reports, run histories and automation code; if TC-06 later meant something else, an old "TC-06 failed" report would point to the wrong test. New cases get new numbers (TC-08).

#### Using AI to fill the gap

This is a good place for Tuesday's **critique-and-extend** pattern: give the model the existing suite and ask **only** for what is missing, so it cannot rewrite cases you have already reviewed. The core of such a prompt (story and existing tests go in delimiters above it):

```text
These acceptance criteria have no test yet: AC4.
Write test cases ONLY for those criteria, using the same JSON fields as the
existing tests. Do not repeat or rewrite existing tests. Do not invent
messages or rules that are not in the story; put anything unclear in
"open_questions".
```

The list of gaps came straight from the traceability matrix: code finds precisely what is missing, the model drafts a fill, and you review it again.

AC4 is tricky because the story does not say what message appears when a second coupon is tried. A good test can still be written **without inventing a message**, by checking something the story does guarantee: the discount is not applied twice. Here is the reviewed suite, including TC-08, written as Python data so we can re-run every check on it:

```python
# reviewed_suite.py
# The suite AFTER human review: TC-04 message fixed, TC-05/TC-06/TC-07 retired,
# TC-08 added for AC4. IDs are never reused.
STEPS = ["Open the checkout page", "Enter {code} in the coupon field", "Click Apply"]


def make_case(cid, title, ac, ctype, priority, subtotal, code, expected):
    return {
        "id": cid, "title": title, "ac": ac, "type": ctype, "priority": priority,
        "preconditions": f"Shopper is logged in; cart subtotal is ${subtotal}",
        "steps": [s.format(code=code) for s in STEPS],
        "test_data": {"subtotal": subtotal, "code": code},
        "expected_result": expected,
    }


REVIEWED = [
    make_case("TC-01", "Apply SAVE10 to a subtotal above $50.00", "AC1",
              "positive", "High", "80.00", "SAVE10", "Order total shows $72.00"),
    make_case("TC-02", "Apply SAVE10 at exactly $50.00", "AC1",
              "boundary", "High", "50.00", "SAVE10", "Order total shows $45.00"),
    make_case("TC-03", "Apply SAVE10 just under $50.00", "AC2", "boundary", "High",
              "49.99", "SAVE10", 'Order total shows $49.99 and the message '
              '"Spend $50.00 to use SAVE10" is displayed'),
    make_case("TC-04", "Apply an unknown coupon code", "AC3", "negative", "Medium",
              "80.00", "SAVE20", 'The message "Coupon code not recognised" '
              'is displayed and no discount is applied'),
]
tc08 = make_case("TC-08", "Apply SAVE10 a second time to the same order", "AC4",
                 "negative", "Medium", "80.00", "SAVE10",
                 "Order total still shows $72.00 (discount not applied twice)")
tc08["preconditions"] = ("Shopper is logged in; cart subtotal is $80.00; "
                         "SAVE10 is already applied")
REVIEWED.append(tc08)
```

Code notes:

- `make_case` is a small **factory function**: shared parts (steps, preconditions) are written once, which avoids inconsistencies such as a title saying $50.00 while the data says $55.00.
- `s.format(code=code)` fills the `{code}` placeholder in each step template (the same trick `fake_llm` uses).
- Python joins string literals that sit next to each other into one string; single quotes outside let us use double quotes inside.
- TC-08's preconditions differ (SAVE10 is already applied), so we overwrite that one field.

Re-run every check against the reviewed suite; fixes introduce mistakes too.

```python
# rereview.py -- run every check again on the reviewed suite
from check_expected import check_quoted_messages, check_totals, check_vague
from check_fields import check_fields
from reviewed_suite import REVIEWED
from tc_prompt import STORY_US205
from trace_matrix import acceptance_criteria, traceability_matrix

findings = check_fields(REVIEWED)
for case in REVIEWED:
    findings += check_vague(case)
    findings += check_quoted_messages(case, STORY_US205)
    findings += check_totals(case)

matrix = traceability_matrix(REVIEWED, acceptance_criteria(STORY_US205))
gaps = [ac for ac, ids in matrix.items() if ac != "(untraced)" and not ids]

print(f"Findings: {len(findings)}")
print(f"Gaps: {gaps or 'none'}")
print(f"Untraced: {matrix['(untraced)'] or 'none'}")
```

Output:

```text
Findings: 0
Gaps: none
Untraced: none
```

Five cases, 100% AC coverage, every expected result matching the story or the human-written oracle. Five is also exactly the minimum we predicted by hand: the AI draft had seven cases but covered less.

### 9. Prompting Tips for Bigger and Better Suites

The coupon story is small; real stories are bigger. These habits help as the work grows:

- **One story (or one group of related ACs) per prompt.** Mixing stories weakens coverage of the stories in the middle of the prompt.
- **Conditions before cases, in the same reply.** Add a rule such as *"First list the test conditions for each AC in a key called `conditions`, then write cases per condition."* This is Tuesday's "partitions before tests" idea applied to suites: a wrong condition is quicker to spot than ten wrong cases built on it.
- **A reason with each priority.** "High, because a wrong discount loses money on every order" can be checked; a bare "High" cannot, and bare priorities drift towards "everything is High".
- **Name the test level.** AC3 at UI level checks a message on screen; at unit level it checks that `apply_coupon` raises `ValueError`.
- **Non-functional ideas go in a separate `suggestions` list.** Without a measurable criterion, "performance" or "usability" cases get invented expected results such as "page loads quickly". US-310 AC4 ("fast and user-friendly") must be clarified first, as you saw in *AI-Assisted Requirements Analysis*.
- **One good example** (few-shot, from Tuesday), taken from a *different* story so the model copies the style, not the content.
- **Low temperature** for consistent output (Monday's *Generative AI concepts*); brainstorm separately if you want unusual ideas.
- **Always ask for open questions.** Even when the model ignores the "do not invent" rule, its questions often point to the gaps you need to raise.

### 10. Exporting the Reviewed Suite

A reviewed suite must reach the place where your team works: **CSV** for a test management tool, **Gherkin** for BDD (Week 6) and **pytest** for unit-level automation (Week 4).

#### 10.1 CSV for a test management tool

Most test management tools import CSV. TestRail, for example, supports a single-row layout (one case per row, steps in one cell) and a multi-row layout (one step per row). We produce the simpler single-row layout.

```python
# export_csv.py
import csv

from reviewed_suite import REVIEWED

COLUMNS = ["ID", "Title", "Requirement", "Type", "Priority",
           "Preconditions", "Steps", "Test Data", "Expected Result"]

with open("us205_test_cases.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLUMNS)
    writer.writeheader()
    for case in REVIEWED:
        writer.writerow({
            "ID": case["id"],
            "Title": case["title"],
            "Requirement": f"US-205 {case['ac']}",
            "Type": case["type"],
            "Priority": case["priority"],
            "Preconditions": case["preconditions"],
            "Steps": "\n".join(f"{n}. {s}" for n, s in enumerate(case["steps"], 1)),
            "Test Data": "; ".join(f"{k}={v}" for k, v in case["test_data"].items()),
            "Expected Result": case["expected_result"],
        })

print(f"Wrote {len(REVIEWED)} test cases to us205_test_cases.csv")
```

Output:

```text
Wrote 5 test cases to us205_test_cases.csv
```

The first rows of the file:

```csv
ID,Title,Requirement,Type,Priority,Preconditions,Steps,Test Data,Expected Result
TC-01,Apply SAVE10 to a subtotal above $50.00,US-205 AC1,positive,High,Shopper is logged in; cart subtotal is $80.00,"1. Open the checkout page
2. Enter SAVE10 in the coupon field
3. Click Apply",subtotal=80.00; code=SAVE10,Order total shows $72.00
```

How it works:

- `newline=""` is recommended by the Python documentation for CSV files, because the `csv` module handles line endings itself (otherwise you can get blank rows on Windows).
- `csv.DictWriter` writes dictionaries as rows in the `fieldnames` order; `writeheader()` writes the column names.
- `enumerate(case["steps"], 1)` numbers the steps from 1, and `"\n".join(...)` puts them on separate lines **inside one cell**. The `csv` module wraps that cell in quotes automatically. Building CSV by string concatenation breaks on line breaks and commas, so always use the module.
- The `Requirement` column (`US-205 AC1`) keeps traceability after import.

During import, the tool asks you to map CSV columns to its fields; save that mapping for next time.

#### 10.2 Gherkin scenarios

If your team uses BDD, the same reviewed cases become Gherkin scenarios (Week 6). A short script (`to_gherkin.py` in the practice exercises) produced these from the first two reviewed cases:

```gherkin
Feature: US-205 Apply coupon at checkout

  @TC-01 @US-205-AC1
  Scenario: Apply SAVE10 to a subtotal above $50.00
    Given my cart subtotal is $80.00
    When I apply the coupon code "SAVE10"
    Then the order total shows $72.00

  @TC-02 @US-205-AC1
  Scenario: Apply SAVE10 at exactly $50.00
    Given my cart subtotal is $50.00
    When I apply the coupon code "SAVE10"
    Then the order total shows $45.00
```

The tags `@TC-01` and `@US-205-AC1` carry traceability: they let you run scenarios by test case or by acceptance criterion (for example `behave --tags=@US-205-AC1` if your BDD runner is behave) and link each scenario back to your test management tool.

Asking an AI to do this conversion is a good use of AI (pure reformatting). Add the rule *"Do not change any value, message or expected result; only change the format"*, then diff the result against the reviewed suite: conversions are where silent changes sneak in.

#### 10.3 A pytest file for the unit level

Totals (AC1, AC2) and rejecting unknown codes (AC3) are owned by `apply_coupon`, so they suit fast unit tests. The **messages** and the AC4 rule are UI behaviour. Choosing the level for each case is your design decision, not the AI's.

```python
# test_apply_coupon_suite.py
# Unit-level checks for the reviewed US-205 test cases that apply_coupon owns.
# Messages (AC2, AC3) and AC4 are UI behaviour, automated with Playwright (see AI-Assisted Automation Development).
import pytest

from cart import apply_coupon


@pytest.mark.parametrize(
    "subtotal, code, expected",
    [
        pytest.param(80.00, "SAVE10", 72.00, id="TC-01-AC1-above-50"),
        pytest.param(50.00, "SAVE10", 45.00, id="TC-02-AC1-exactly-50"),
        pytest.param(49.99, "SAVE10", 49.99, id="TC-03-AC2-just-under-50"),
    ],
)
def test_coupon_totals(subtotal, code, expected):
    assert apply_coupon(subtotal, code) == pytest.approx(expected)


def test_tc04_ac3_unknown_code_is_rejected():
    with pytest.raises(ValueError, match="Unknown coupon"):
        apply_coupon(80.00, "SAVE20")
```

Run it with `pytest -v test_apply_coupon_suite.py` (with `cart.py` from section 3 in the same folder):

```text
test_apply_coupon_suite.py::test_coupon_totals[TC-01-AC1-above-50] PASSED [ 25%]
test_apply_coupon_suite.py::test_coupon_totals[TC-02-AC1-exactly-50] PASSED [ 50%]
test_apply_coupon_suite.py::test_coupon_totals[TC-03-AC2-just-under-50] PASSED [ 75%]
test_apply_coupon_suite.py::test_tc04_ac3_unknown_code_is_rejected PASSED [100%]

============================== 4 passed in 0.05s ===============================
```

What to notice:

- `pytest.param(..., id="TC-01-AC1-above-50")` gives each row a test ID containing the test case ID and the AC, so a CI failure points straight to the documented case and requirement: traceability carried into automation.
- `pytest.approx` tolerates float rounding (the function uses floats; Tuesday showed why `Decimal` is safer for money). `pytest.raises(ValueError, match=...)` passes only if that exception is raised with a matching message. Your timing will differ slightly.

The UI-level versions of TC-03, TC-04 and TC-08 are a job for Playwright, later today in *AI-Assisted Automation Development*.

### 11. A Second Example: US-101 Login

The same approach adapts to the login story, US-101 (AC1: valid credentials → "My Account"; AC2: wrong password **or** unknown email → "Invalid email or password"; AC3: 5 consecutive failures lock the account for 15 minutes). `build_test_case_prompt`, `acceptance_criteria`, `traceability_matrix`, `check_fields`, `check_vague` and `check_quoted_messages` all work unchanged; only the story-specific partition and oracle functions need rewriting. The minimum suite, sketched by hand:

| AC | Condition | Type | Expected result |
|---|---|---|---|
| AC1 | Valid email and password | positive | "My Account" page is shown |
| AC2 | Registered email, wrong password | negative | "Invalid email or password" |
| AC2 | Unknown email | negative | The **same** message |
| AC3 | 4 failures, then the correct password | boundary | Logged in (not yet locked) |
| AC3 | 5 failures, then the correct password | boundary | Locked: login refused |
| AC3 | Locked account after 15 minutes | boundary | Login succeeds again |

Things to watch for in an AI draft of this story:

- **Message drift becomes a security problem.** The shared message stops attackers discovering which emails are registered. A draft expecting "Email not found" for an unknown email would test for (and so encourage) a security weakness.
- **"Consecutive" hides an assumption.** Does a successful login reset the count? A model will usually assume so; it is still a guess for `open_questions`.
- **Time-based ACs need testability.** A step saying "wait 15 minutes" is impractical; a better case asks developers for a test hook to control the lock time. AI rarely offers this judgement unprompted.

### 12. The Complete Workflow

The flow for today's exercise:

1. **Analyse the story by hand**: ACs, minimum conditions, computable expected results, gaps.
2. **Generate** with a structured prompt (one story, explicit fields, traceability, "do not invent" plus `open_questions`, a case limit, locked JSON).
3. **Parse** defensively, then **read** the draft against your analysis.
4. **Run the checks**: fields, traceability, duplicates, expected results against the oracle, balance.
5. **Decide** keep, fix, retire or add for every case, with a reason.
6. **Fill gaps** with critique-and-extend and review the new cases the same way.
7. **Re-run all checks**, send open questions to the product owner, then **export** with IDs and AC links intact.

Steps 1, 3, 5 and the questions are human work; the AI saves typing in steps 2 and 6; the checks make your review faster and more reliable.

### 13. Connecting to Project 2

Today's **Project 2** milestone asks you to generate and review AI test cases (and, next lesson, test data) for the e-commerce app, documenting corrections:

- Start with **US-205** (small, exact oracle) and **US-310** (ZIP and phone rules suit boundary and negative cases; vague AC4 tempts the AI into invented expected results).
- Keep prompts in `prompts/`, review scripts in `tools/` and the reviewed suite (CSV or JSON) in your repository under Git. Later automation should point back to its test case IDs.
- Save the **unreviewed** AI draft next to the reviewed version. The difference is your evidence of human review and the raw material for your correction log.

---

## Practice Exercises

1. **Run the pipeline.** Put all the files from this lesson in one folder and run `parse_suite.py`, `check_fields.py`, `trace_matrix.py`, `duplicates.py`, `check_expected.py` and `rereview.py`. Confirm that your output matches the lesson.
2. **Break it on purpose.** Edit `fake_llm.py` so that TC-02 expects "$46.00" and TC-03 has `"priority": "Urgent"`. Which checks catch each change? Then remove TC-04 entirely and see what the traceability matrix reports.
3. **Add a consistency check.** Write `check_consistency(case)` that compares the subtotal in `preconditions` (for example "cart subtotal is $80.00") with `test_data["subtotal"]` and reports any mismatch. Test it by introducing a mismatch in one case.
4. **Real AI comparison.** Paste the prompt from `build_test_case_prompt(STORY_US205)` into the AI assistant your team uses. Save its reply as `draft.json`, change `fake_llm` to return the file's contents, and run the checks. Record every finding in a table like the one in section 8.
5. **Gherkin.** Write `to_gherkin.py`, which turns each case in `REVIEWED` into a tagged scenario like the ones in section 10.2. Then rewrite TC-01 to TC-03 as one **Scenario Outline** with an Examples table (Week 6), keeping the test case IDs in an extra column.
6. **US-310.** Write the minimum suite for US-310 by hand (AC1 to AC3), then generate one with AI. Which AC did the AI handle worst? What did it do with AC4?

---

## Knowledge Check

1. What is the difference between a test condition and a test case?
2. Why is "Verify it works correctly" an unacceptable expected result?
3. A draft suite has 100% acceptance-criteria coverage. Name two reasons why it might still be a poor suite.
4. Calculate the Jaccard similarity of the title word sets {apply, save10, at, exactly, $50.00} and {apply, save10, just, under, $50.00}.
5. The story does not say whether coupon codes are case-sensitive, and the AI wrote a test expecting `save10` to work. What should you do with that test, and why?
6. Why should you retire an incorrect test case's ID instead of renumbering the suite?
7. Which US-205 cases can be checked with a unit test of `apply_coupon`, and which need a UI test? Explain why.
8. Why must the oracle function `oracle_total` be written by a human from the story, rather than generated by the same AI that wrote the test cases?

<details>
<summary>Answers</summary>

1. A test condition is *what* to test (a testable aspect of a requirement, such as "the $50.00 boundary"). A test case is *how* to test it: a documented, repeatable set of preconditions, test data, steps and an expected result.
2. It is not observable or specific, so it can never fail. A tester cannot decide pass or fail from it. Expected results should name an exact total, message, page or state from the requirement.
3. Any two of: a case can trace to an AC but test an invented rule (like TC-05); expected results can be wrong; duplicates; missing boundary or negative cases; some ACs with only one weak test. Coverage counts links, not quality.
4. Shared words: {apply, save10, $50.00} = 3. All words together: {apply, save10, at, exactly, just, under, $50.00} = 7. Jaccard = 3 ÷ 7 ≈ 0.43, below our 0.6 threshold, which is correct: these two titles describe different boundary values.
5. Remove (retire) it from the suite and raise the question with the product owner. The test is based on an invented rule; until the requirement is clarified there is no oracle, so the test cannot have a trustworthy expected result.
6. IDs appear in bug reports, run histories and automation code; renumbering would make those references point to the wrong test.
7. TC-01, TC-02 and the totals of TC-03 can be checked at unit level, because `apply_coupon` computes them; TC-04's rejection can be checked as a `ValueError`. The exact messages in TC-03 and TC-04, and the "only one coupon" rule in TC-08, are user interface behaviour and need a UI (Playwright) test.
8. The oracle must be independent of the thing being checked. If the same AI wrote both, a misunderstanding of the requirement could appear in both and the check would happily agree with itself. A human-written oracle based on the story is a separate source of truth.

</details>

---

## Glossary

- **Test condition:** A testable aspect of a requirement; *what* to test.
- **Test case:** A documented set of preconditions, test data, steps and an expected result for testing one condition; *how* to test it.
- **Expected result:** The observable outcome that decides pass or fail; the written form of the test oracle.
- **Test oracle:** The source of truth for expected results (requirement, specification, product owner, reference implementation). An LLM is not an oracle.
- **Traceability:** The link between a test case and the requirement or acceptance criterion it tests.
- **Traceability matrix:** A table showing which tests cover which requirements; it reveals untested requirements and untraced tests.
- **Invented rule:** Behaviour that a generated test case assumes but the requirement does not state.
- **Message drift:** An expected result that paraphrases a required message instead of quoting it exactly.
- **Critique-and-extend:** A prompt pattern that gives the model an existing artifact and asks only for corrections or additions.

---

## Summary

- A **test case** is a documented, repeatable artifact: ID, title, traced AC, type, priority, preconditions, steps, test data and an **observable expected result**. Ask the AI for exactly these fields.
- A good generation prompt covers **one story**, requires **traceability to one AC**, demands **exact messages and totals**, forbids invention and provides **`open_questions`**, limits the case count and **locks the format**.
- AI drafts look finished but typically contain **invented rules, message drift, vague results, untraced cases, duplicates and coverage gaps**.
- Small Python checks catch most of them: **fields**, a **traceability matrix**, **duplicates** (Jaccard and partitions), **expected results** against a human-written oracle, and **balance**.
- Decide **keep, fix, retire or add**, never reuse IDs, fill gaps with **critique-and-extend**, and **re-run every check**.
- Export to **CSV**, **Gherkin** and **pytest** with IDs and AC links intact, choosing the right test level for each case.
- The AI saves typing; **you** own the requirement, the oracle, the decisions and the final suite.

---

## Additional Resources

- TestRail Support Center, *Import test cases from CSV or Excel* (how real tools map CSV columns to test case fields, including single-row and multi-row step layouts): https://support.testrail.com/hc/en-us/articles/7101779988372
- Python documentation, *csv: CSV File Reading and Writing* (`DictWriter`, quoting and why to open files with `newline=""`): https://docs.python.org/3/library/csv.html
- Cucumber, *Gherkin Reference* (keywords, tags, Scenario Outline and Examples for turning test cases into scenarios): https://cucumber.io/docs/gherkin/reference/
