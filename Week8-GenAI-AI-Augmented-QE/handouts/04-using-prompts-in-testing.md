# Week 08 · Lecture 04: Using Prompts in Testing

**Topics:**

1. [Common Prompt Failure Modes](#topic-1)
2. [AI-Assisted Test Design](#topic-2)
3. [AI-Assisted Coding and Debugging](#topic-3)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Work in your `week08` folder. It must contain **`cart.py`** from Lecture 02. If it doesn't, create it now:
>    ```python
>    def apply_coupon(total: float, code: str) -> float:
>        """SAVE10 gives 10% off orders of $50.00 or more.
>        Orders under $50.00 are unchanged. Unknown codes raise ValueError."""
>        if code != "SAVE10":
>            raise ValueError(f"Unknown coupon: {code}")
>        if total >= 50:
>            return round(total * 0.9, 2)
>        return total
>    ```
> 2. Check pytest is installed (from Lecture 02):
>    ```bash
>    python -m pytest --version
>    ```
>    If not: `python -m pip install pytest`
> 3. Have your AI assistant open: **ChatGPT, Copilot Chat or Claude**.
> 4. Keep `prompts.txt` from Lecture 03 open. You'll add more prompts today.

---

## How to Use This Handout

Same layout as before: **Definition → Key ideas → Worked example (step by step) → Checkpoint → Your turn → Common errors.** Run your file after every step. Do exercise 1 in class; the rest are for after class.

Lecture 03 taught you **how to write** prompts. Today you **use** them for real testing work, and you learn to **catch the AI when it's wrong**.

> **About AI answers:** your AI's answers will differ from the examples in this handout and from your classmates' answers. Check that the answer has the right **things** in it, not the exact words.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Recognise the **common ways AI answers go wrong**, and catch them with small Python checks.
- Use AI as a **test design partner** by asking for a named technique (Boundary Value Analysis), and check its work.
- Ask AI for **debugging help** with a complete, well-structured prompt.
- Spot the **dangerous "fix"** that makes a test pass by weakening it.

---

<a id="topic-1"></a>

# Topic 1: Common Prompt Failure Modes

## Definition

A **prompt failure mode** is a typical way an AI answer goes wrong, even when the prompt looked fine. Common ones are **hallucination** (made-up facts, functions or rules), **ignored instructions** (wrong count, wrong format), **wrong maths**, **outdated knowledge** (old library methods) and **inconsistency** (a different answer each run). The tester's response is the same as for any defect: **notice it, reproduce it, find the cause and fix the prompt**, and use **small automatic checks** for the failures that are easy to detect in code.

## Key Ideas

1. **A quick map of the most common failures:**

   | Failure mode | What you see | Typical cause | Fix |
   |---|---|---|---|
   | **Hallucination** | Invented rule, function or fact | Missing context; AI fills gaps | Give context; allow "I don't know" / questions |
   | **Ignored instruction** | 4 items instead of 5; extra text | Instruction buried or vague | Put key rules at the end; be exact ("exactly 5") |
   | **Wrong maths** | 49.99 → 44.99 when it should be unchanged | LLMs predict text; they don't calculate | **Check numbers with code** |
   | **Outdated knowledge** | Old Selenium methods like `find_element_by_id` | Training cut-off | Name the version; check the docs |
   | **Inconsistency** | Different answer every run | Temperature / randomness | Lock the format; re-run and compare |

2. **Debug a prompt like a test:** reproduce the failure → change **one thing** → re-run → compare.
3. **Let code catch the easy failures.** Counting items, checking the format and checking maths are quick to automate. Save human attention for judgement calls.
4. **A mismatch needs a human decision.** If the AI's expected value differs from the code's result, **either could be wrong**. The **requirement** decides which.

## Worked Example: Automatic Checks on an AI Test Table

**The situation:** we asked our AI assistant:

```text
Give EXACTLY 5 test rows for the SAVE10 coupon as a JSON list.
Each row: "subtotal" (number), "code" (string), "expected" (number).
```

It returned the reply below. It **looks** fine. Let's check it with code. Create `failure_checks.py` in the same folder as `cart.py`.

### Step 1: The AI's reply

```python
import json
from cart import apply_coupon

# Step 1: we asked for EXACTLY 5 test rows for SAVE10; this is the AI's reply
ai_reply = """[
  {"subtotal": 100.00, "code": "SAVE10", "expected": 90.00},
  {"subtotal": 50.00,  "code": "SAVE10", "expected": 45.00},
  {"subtotal": 49.99,  "code": "SAVE10", "expected": 44.99},
  {"subtotal": 100.00, "code": "save10", "expected": 90.00}
]"""
rows = json.loads(ai_reply)
```

**What this code does:**

- `from cart import apply_coupon` loads the real function from Lecture 02, so we can compare the AI's expectations with what the code actually does.
- `ai_reply` is the AI's answer. This time it's clean JSON, so `json.loads` works directly (Lecture 03, Topic 3).
- `rows` is now a Python **list of dictionaries**, one per test row.

### Step 2: Count check

```python
# Step 2: count check - did we get what we asked for?
ASKED_FOR = 5
if len(rows) != ASKED_FOR:
    print(f"COUNT: asked for {ASKED_FOR} rows, got {len(rows)}")
```

**What this code does:** the simplest check of all. We asked for exactly 5. `len(rows)` counts what we actually got. An **ignored instruction** is caught in two lines.

### Step 3: Maths check against the real code

```python
# Step 3: maths check - compare every expected value with the real code
def actual_result(subtotal, code):
    try:
        return apply_coupon(subtotal, code)
    except ValueError:
        return "ValueError"

problems = 0
for row in rows:
    actual = actual_result(row["subtotal"], row["code"])
    if actual != row["expected"]:
        problems += 1
        print(f"WRONG: {row['subtotal']} + {row['code']}: AI expects "
              f"{row['expected']}, real code gives {actual}")
```

**What this code does:**

- `actual_result` calls the real function. Unknown codes **raise** a `ValueError`, so we catch it and return the text `"ValueError"` instead. That way the loop keeps going instead of crashing.
- For each row, we compare the AI's `expected` value with the real result. Any difference is printed and counted.
- A long f-string can be split over two lines inside the brackets. Python joins them.

### Step 4: Summary

```python
# Step 4: summary
print(f"{problems} of {len(rows)} rows need a human decision")
```

**What this code does:** gives a one-line result. Note the wording: **"need a human decision"**, not "are wrong". The code could be the one with the bug!

### Consolidated File: `failure_checks.py`

```python
import json
from cart import apply_coupon

# Step 1: we asked for EXACTLY 5 test rows for SAVE10; this is the AI's reply
ai_reply = """[
  {"subtotal": 100.00, "code": "SAVE10", "expected": 90.00},
  {"subtotal": 50.00,  "code": "SAVE10", "expected": 45.00},
  {"subtotal": 49.99,  "code": "SAVE10", "expected": 44.99},
  {"subtotal": 100.00, "code": "save10", "expected": 90.00}
]"""
rows = json.loads(ai_reply)

# Step 2: count check - did we get what we asked for?
ASKED_FOR = 5
if len(rows) != ASKED_FOR:
    print(f"COUNT: asked for {ASKED_FOR} rows, got {len(rows)}")

# Step 3: maths check - compare every expected value with the real code
def actual_result(subtotal, code):
    try:
        return apply_coupon(subtotal, code)
    except ValueError:
        return "ValueError"

problems = 0
for row in rows:
    actual = actual_result(row["subtotal"], row["code"])
    if actual != row["expected"]:
        problems += 1
        print(f"WRONG: {row['subtotal']} + {row['code']}: AI expects "
              f"{row['expected']}, real code gives {actual}")

# Step 4: summary
print(f"{problems} of {len(rows)} rows need a human decision")
```

## Checkpoint

```text
COUNT: asked for 5 rows, got 4
WRONG: 49.99 + SAVE10: AI expects 44.99, real code gives 49.99
WRONG: 100.0 + save10: AI expects 90.0, real code gives ValueError
2 of 4 rows need a human decision
```

**Now be the human.** Check each flagged row against the **requirement** (US-205):

| Row | Who is right? | Failure mode |
|---|---|---|
| Only 4 rows | The AI ignored "exactly 5" | Ignored instruction |
| 49.99 → 44.99 | **The code.** Under $50.00 is unchanged | Wrong maths / contradicts requirement |
| `save10` → 90.00 | **The code.** Nothing says lowercase works | Hallucination (invented rule) |

### A Prompt-Debugging Checklist

When an AI answer is wrong, work through this list before you rewrite the whole prompt. Change **one thing at a time** and re-run, just as you would when debugging a test.

| # | Ask yourself | If the answer is "no"… |
|---|---|---|
| 1 | Did I paste the **exact** requirement (not retyped)? | Paste it, fenced with `###` markers |
| 2 | Did I say exactly **how many** items I want? | Say "exactly 5", not "some" |
| 3 | Did I name the **format** and every field? | Add an output format section (Lecture 03) |
| 4 | Did I tell it to use **only the stated rules**? | Add: "Do not invent rules or values" |
| 5 | Did I allow it to **ask** instead of guess? | Add: "If something is unclear, ask a question" |
| 6 | Did I put the most important rule **last**? | Move key rules to the end. AIs pay most attention to the start and the end |
| 7 | Did I start a **new chat** for the retry? | Old messages in the chat can keep steering the answer |

Add this checklist to `prompts.txt`. You'll use it all week.

## Your Turn

1. **(In class, 3 min)** Add a fifth row to `ai_reply`: `{"subtotal": 50.01, "code": "SAVE10", "expected": 45.01}`. Remember the comma after the previous row! Run the file. Which messages disappear?
2. **(After class)** Send the prompt from the top of this worked example to your AI assistant. Paste its **real** reply into `ai_reply` and run the checks. Which failure modes did your AI show, if any?
3. **(After class)** Improve the prompt so the AI is less likely to make these mistakes. (Hints: paste the requirement as context, say "use only these rules", say "expected must follow the rules exactly".) Run your new prompt and the checks again. Save the better prompt in `prompts.txt`.
4. **(After class)** Ask your AI assistant: *"How do I find an element by ID in Selenium with Python?"* Does it suggest `find_element(By.ID, ...)` (current) or `find_element_by_id(...)` (removed in Selenium 4)? How would you check which one is current?

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'cart'` | `cart.py` isn't in the same folder | Copy `cart.py` (see Before Class) into this folder |
| `JSONDecodeError` after adding a row | A missing comma between rows, or a comma after the last row | Rows are separated by commas; there's no comma after the last one |
| `KeyError: 'expected'` | The AI used a different key name | Use the format checks from Lecture 03 first |

---

<a id="topic-2"></a>

# Topic 2: AI-Assisted Test Design

## Definition

**AI-assisted test design** means using an AI assistant as a **thinking partner** to apply test design techniques such as **Equivalence Partitioning (EP)** and **Boundary Value Analysis (BVA)**, which you learned in Week 3. The trick is to stop asking *"write me some tests"* and start asking *"apply BVA to this rule, list the boundaries first, and tell me what you didn't cover."* The AI is fast at producing **breadth** (many ideas quickly). **You** stay responsible for the requirement, the **expected results** and the final decision about what goes into the test suite.

## Key Ideas

1. **Who does what:**

   | AI is good at | The tester owns |
   |---|---|
   | Brainstorming many ideas fast | Choosing the technique |
   | Applying a named technique on request | Checking every expected result |
   | Laying out tables and test data | Spotting missing or invented cases |
   | Turning ideas into Gherkin or pytest drafts | Deciding what goes into the suite |

2. **Technique-driven prompts beat generic prompts.** Name the technique, give the rule, and ask the AI to **show its working** (for example, "list the partitions first").
3. **BVA in one line:** bugs hide at the edges. For a rule "$50.00 or more", test **just below (49.99), on (50.00) and just above (50.01)**.
4. **Ask what wasn't covered.** "List anything you did NOT test" makes gaps visible instead of hidden.

## Worked Example: BVA with an AI Partner

**Goal:** design boundary tests for AC1 (*SAVE10 gives 10% off a subtotal of $50.00 or more*) with the AI's help, check its boundaries **yourself**, and turn the reviewed result into a pytest test.

### Step 1: Ask for a named technique (in your AI assistant)

Paste into a new chat:

```text
You are a test designer. Apply Boundary Value Analysis to this rule:

"SAVE10 gives 10% off a subtotal of $50.00 or more.
Subtotals under $50.00 are unchanged." Money has 2 decimal places.

1. First list the boundary (or boundaries) you found.
2. Then list the test values you would use, with the expected total for each.
3. Finally list anything you did NOT cover.
Use a numbered list. Do not invent other rules.
```

**What to notice:** we named the technique, gave the **precision** (2 decimal places, so the step between values is 0.01) and asked for **working first** and **gaps last**. Write down the test values the AI suggests.

### Step 2: Work out the boundaries yourself

Before trusting the AI, apply BVA by hand. The rule changes at **$50.00**, and money moves in steps of **$0.01**, so the three classic BVA values are:

| Value | Position | Expected total |
|---|---|---|
| **49.99** | Just below the boundary | 49.99 (unchanged) |
| **50.00** | Exactly on the boundary | 45.00 (10% off) |
| **50.01** | Just above the boundary | 45.01 (10% off, rounded to cents) |

**Why these three:** bugs hide at edges. A developer who writes `>` instead of `>=` gets 50.00 wrong, and only a test **at** 50.00 catches it.

### Step 3: Compare with the AI's values

Fill in a comparison table on paper. Here's an example using a typical AI answer that stepped in **whole dollars**: `49.00, 50.00, 51.00, 100.00`.

| BVA value | Did the AI include it? |
|---|---|
| 49.99 | ❌ Missed (it used 49.00) |
| 50.00 | ✅ Yes |
| 50.01 | ❌ Missed (it used 51.00) |

| Extra AI values | Useful? |
|---|---|
| 49.00, 51.00 | Not boundaries: they're a whole dollar away from the edge |
| 100.00 | Fine as a "typical" value, but not a boundary test |

Now do the same with **your** AI's values. Also **check every expected total** it gave. Is 50.01 → 45.01 right? (50.01 × 0.9 = 45.009, which rounds to 45.01.)

### Step 4: Turn the reviewed values into a pytest test

You've used pytest in earlier weeks. Create `test_coupon_bva.py` next to `cart.py`:

```python
import pytest
from cart import apply_coupon

# Step 4: reviewed boundary cases -> one parametrized test
BVA_CASES = [
    (49.99, 49.99),   # just below: unchanged
    (50.00, 45.00),   # exactly on the boundary: 10% off
    (50.01, 45.01),   # just above: 10% off
]

@pytest.mark.parametrize("subtotal, expected", BVA_CASES)
def test_save10_boundaries(subtotal, expected):
    assert apply_coupon(subtotal, "SAVE10") == expected
```

**What this code does:**

- `BVA_CASES` lists our **reviewed** cases from Step 2. **We** wrote every expected value from the requirement, not from the AI.
- `@pytest.mark.parametrize(...)` runs the same test once per row. `"subtotal, expected"` names the two values in each tuple.
- One test function, three test runs. When you add a case, you only add a row.

### Consolidated File: `test_coupon_bva.py`

The Step 4 file is the consolidated result. Your Step 3 comparison table is the review record that goes with it.

## Checkpoint

**Step 3:** for the example AI answer, the AI **missed 49.99 and 50.01**. Check that your own table catches the same kind of gap if your AI made one.

**Step 4:** run `python -m pytest -v test_coupon_bva.py`:

```text
test_coupon_bva.py::test_save10_boundaries[49.99-49.99] PASSED           [ 33%]
test_coupon_bva.py::test_save10_boundaries[50.0-45.0] PASSED             [ 66%]
test_coupon_bva.py::test_save10_boundaries[50.01-45.01] PASSED           [100%]
============================== 3 passed in 0.03s ===============================
```

`-v` (verbose) shows each parametrized case on its own line, with its values in the brackets.

### Reading the AI's "Not Covered" List

Step 1 asked the AI to list what it did **not** cover. This is one of the most useful parts of its answer, because it turns hidden gaps into a visible list. A typical answer looks **something like**:

```text
Not covered:
- Unknown or misspelled coupon codes
- Lowercase "save10"
- Negative or zero subtotals
- Combining SAVE10 with another coupon
```

Treat each line as a **question**, not a fact:

| Item | What the tester does |
|---|---|
| Unknown codes | It's in the story (AC3), so add a test |
| Lowercase "save10" | Not in the story. **Ask the BA**; don't assume either way |
| Negative or zero subtotals | Not in the story. A good question for the BA: what should happen? |
| A second coupon | It's in the story (AC4), so add a test |

The AI is good at **suggesting** what might be missing. Only the requirement (or the BA) can say what is **in scope**.

## Your Turn

1. **(In class, 3 min)** Fill in the Step 3 table with **your** AI's values. Did it find all three real boundary values? Were all its expected totals correct?
2. **(After class)** Ask your AI assistant to apply **Equivalence Partitioning** to the same rule: *"List the partitions first, then one test value per partition."* How many partitions did it find? (Hint: there should be one for **invalid codes** too.)
3. **(After class)** A new rule: *"Customers aged 18 or over can create an account."* What are the three BVA values? (Ages are whole numbers, so the step is 1.) Write a parametrized test for a function `can_register(age)` that you write yourself.
4. **(After class)** Ask your AI to convert your three BVA cases into **Gherkin** (Given/When/Then) scenarios. Check that the numbers in the Gherkin match your reviewed cases exactly.

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'cart'` | `cart.py` isn't in the same folder | Copy `cart.py` (see Before Class) into this folder |
| pytest error: `In test_coupon_bva.py::test_save10_boundaries: function uses no argument 'subtotal'` | The names in `parametrize("subtotal, expected", ...)` don't match the function's parameters | Use exactly the same names in both places |
| A BVA case fails, for example `assert 45.009 == 45.01` | Rounding is missing in the code under test | Good catch: that's a real defect. Check the requirement says money is in cents |

---

<a id="topic-3"></a>

# Topic 3: AI-Assisted Coding and Debugging

## Definition

**AI-assisted coding and debugging** means using an AI assistant to help write, explain, improve and **fix** code, including test code. The AI is most useful when you give it what a helpful colleague would need: the **code**, the **failing test**, the **full error output**, what you **expected versus what happened**, and what you've **already tried**. The biggest risk is a "fix" that makes a red test green by **weakening the test** (changing the expected value or deleting the assertion), so the real bug ships. Every AI-suggested fix must be checked against the **requirement**, not just against "is the test green now?"

## Key Ideas

1. **Ways AI helps with code:** autocomplete, **explaining** unfamiliar code, generating drafts, **refactoring** while keeping behaviour the same, and **debugging**.
2. **A good debugging prompt has 6 parts:**

   | Part | Why |
   |---|---|
   | The code under test | So it can see the bug |
   | The failing test | So it knows what was expected |
   | The **full** error output | The real clue is often in the details |
   | Expected vs. actual | Removes guesswork |
   | What you already tried | Avoids repeated suggestions |
   | What you want back | "Explain the cause first, then the fix" |

3. **The weakened-test trap.** A fix that changes the **test** to match the code is only correct if the **test** was wrong. Always ask: *"Which one does the requirement agree with?"*
4. **Use AI to learn.** "Explain this line" is one of the best uses of an AI assistant for a fresher. You can ask as many times as you like.

## Worked Example: Debug a Failing Boundary Test

**The situation:** a new function calculates shipping. One test fails. We'll ask the AI for help properly, then judge its suggestions.

> **Requirement:** *Orders of $50.00 or more ship free. Other orders pay $4.99.*

### Step 1: The code (it has a bug)

Create `shipping.py`:

```python
def shipping_fee(subtotal: float) -> float:
    """Orders of $50.00 or more ship free. Other orders pay $4.99."""
    if subtotal > 50:
        return 0.00
    return 4.99
```

**What this code does:** returns 0.00 (free) for large orders and 4.99 otherwise. Look closely at `>`… but act as if you haven't spotted the bug yet.

### Step 2: The tests, and the failure

Create `test_shipping.py`:

```python
from shipping import shipping_fee

def test_large_order_ships_free():
    assert shipping_fee(80.00) == 0.00

def test_small_order_pays_shipping():
    assert shipping_fee(20.00) == 4.99

def test_exactly_50_ships_free():
    assert shipping_fee(50.00) == 0.00
```

Run `python -m pytest -q test_shipping.py`. You'll see:

```text
..F                                                                      [100%]
...
>       assert shipping_fee(50.00) == 0.00
E       assert 4.99 == 0.0
E        +  where 4.99 = shipping_fee(50.0)
...
FAILED test_shipping.py::test_exactly_50_ships_free - assert 4.99 == 0.0
1 failed, 2 passed in 0.02s
```

**What this tells us:** the boundary test fails. At exactly $50.00 the function charged $4.99. Two tests pass, so the bug is **only at the boundary**.

### Step 3: Write a complete debugging prompt

Paste this into a new chat. It follows the 6-part structure from Key Idea 2:

```text
I need help with a failing pytest test. Please explain the cause first, then suggest a fix.

### Requirement
Orders of $50.00 or more ship free. Other orders pay $4.99.

### Code under test (shipping.py)
def shipping_fee(subtotal: float) -> float:
    if subtotal > 50:
        return 0.00
    return 4.99

### Failing test (test_shipping.py)
def test_exactly_50_ships_free():
    assert shipping_fee(50.00) == 0.00

### Full pytest output
E       assert 4.99 == 0.0
E        +  where 4.99 = shipping_fee(50.0)
FAILED test_shipping.py::test_exactly_50_ships_free - assert 4.99 == 0.0

### Expected vs actual
Expected 0.00 (free shipping) at exactly $50.00. Actual: 4.99.

### What I already tried
Tests at $80.00 and $20.00 pass, so the problem seems to be only at the boundary.
```

**What to notice:** the `###` headings (Lecture 03's delimiters) make each part easy for the AI to find, and **the requirement is included**. That's what lets the AI judge which side is wrong.

### Step 4: Judge the suggested fixes

AI assistants commonly suggest one of these two fixes. **Only one is correct.**

**Fix A (change the code):**

```python
    if subtotal >= 50:
```

**Fix B (change the test):**

```python
def test_exactly_50_ships_free():
    assert shipping_fee(50.00) == 4.99
```

| | Fix A | Fix B |
|---|---|---|
| Makes the test pass? | ✅ Yes | ✅ Yes |
| Agrees with the requirement ("$50.00 **or more** ships free")? | ✅ Yes | ❌ **No** |
| Verdict | **Accept** | **Reject: weakened test. The bug would ship.** |

> **The rule:** "the test is green" is not enough. **The requirement decides.** Fix B also leaves a test whose name ("ships free") contradicts what it checks, which is a sure sign of a bad fix.

### Step 5: Apply the correct fix and re-run

Change `>` to `>=` in `shipping.py` and run `python -m pytest -q test_shipping.py` again. All three tests now pass.

### Consolidated Files

**`shipping.py` (fixed)**

```python
def shipping_fee(subtotal: float) -> float:
    """Orders of $50.00 or more ship free. Other orders pay $4.99."""
    if subtotal >= 50:
        return 0.00
    return 4.99
```

**`test_shipping.py`**

```python
from shipping import shipping_fee

def test_large_order_ships_free():
    assert shipping_fee(80.00) == 0.00

def test_small_order_pays_shipping():
    assert shipping_fee(20.00) == 4.99

def test_exactly_50_ships_free():
    assert shipping_fee(50.00) == 0.00
```

## Checkpoint

After the fix:

```text
...                                                                      [100%]
3 passed in 0.01s
```

From your AI assistant (Step 3), you should have received **something like**: *"The condition uses `>` (greater than), so 50.00 is not included. The requirement says '$50.00 or more', which needs `>=`."* **Check for:**

- ✅ It explains the **cause** before the fix
- ✅ It mentions `>` vs `>=` and links it to the words "or more"
- ✅ It suggests changing the **code**, not the test. If your AI suggested changing the test, that's exactly the trap from Step 4.

### Before You Accept Any AI Code Fix

Use this five-question check every time, not just for debugging:

1. **Do I understand the change?** If not, ask the AI to explain it line by line before you accept it.
2. **Does it agree with the requirement?** Read the requirement again and compare it word for word.
3. **Did it change the test or the code?** If it changed the test, be suspicious. Was the test really wrong?
4. **Can the test still fail?** Temporarily break the code (for example, change `>=` back to `>`) and check that the test goes red. A test that can't fail protects nothing.
5. **Does the function or method actually exist?** If the fix uses a library function you haven't seen before, check the official documentation. AI sometimes invents them (Topic 1).

## Your Turn

1. **(In class, 3 min)** Add a test for **$49.99** (should pay $4.99). Run all the tests. Do they pass?
2. **(After class)** **Learn with AI.** Paste `test_coupon_bva.py` from Topic 2 into your AI assistant and ask: *"Explain what @pytest.mark.parametrize does, line by line, for a beginner."* Write down one thing you didn't know before.
3. **(After class)** **Spot the weakened test.** Ask your AI to fix the failing test **without** giving it the requirement (send only the code, the test and the error). Does its suggestion change the code or the test? What does this show about including the requirement?
4. **(After class)** Add the debugging prompt template from Step 3 to `prompts.txt`, with empty sections you can fill in next time: `### Requirement`, `### Code under test`, and so on.

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `assert 4.99 == 0.0` | The real bug (`>` instead of `>=`) | Fix the code, as in Step 5 |
| `ImportError: cannot import name 'shipping_fee'` | A typo in the function name, or the file isn't saved | Check the spelling in both files, and save |
| The test passes, but you changed the expected value | You accepted a weakened-test fix | Check the test against the requirement, then put the correct expected value back |

---

## Lecture Wrap-Up: Quick Check

1. Name three common prompt failure modes.
2. The AI says 49.99 with SAVE10 should cost 44.99; the code returns 49.99. Who is right, and how do you decide?
3. What three values does BVA give for the rule "$50.00 or more" (money with cents)?
4. List four things a good debugging prompt contains.
5. An AI "fix" changes the expected value in a test so it passes. When is that acceptable?

<details>
<summary>Answers</summary>

1. Any three of: hallucination, ignored instruction, wrong maths, outdated knowledge, inconsistency.
2. **The code** is right here: the requirement says orders under $50.00 are unchanged. You decide by checking the **requirement**, not by trusting either side.
3. **49.99, 50.00, 50.01**.
4. Any four of: the code, the failing test, the full error output, expected vs. actual, what you tried, what you want back. (Including the requirement also helps!)
5. Only when the **test** was wrong according to the **requirement**. Otherwise it's a weakened test that hides a bug.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Failure mode** | A typical way something goes wrong |
| **Hallucination** | Confident, invented output: a fake rule, function or fact |
| **Ignored instruction** | The AI didn't follow part of the prompt (count, format, limits) |
| **Equivalence Partitioning (EP)** | Splitting inputs into groups that should behave the same, and testing one value per group |
| **Boundary Value Analysis (BVA)** | Testing just below, on and just above each limit |
| **Parametrized test** | One pytest test run once per row of data |
| **Refactoring** | Changing code structure without changing behaviour |
| **Weakened test** | A test changed so it no longer catches the bug it should |
| **Oracle** | The source that decides the correct expected result: here, the **requirement** |

## Summary

- AI answers fail in **predictable ways**. Catch the easy ones (count, format, maths) **with code**, and save your judgement for the rest.
- When the AI and the code disagree, **the requirement decides**.
- For test design, **name the technique** and ask the AI to show its working and its gaps. **You** own the expected results.
- For debugging, give the AI the **full picture**, and **never accept a fix that weakens the test** just to turn it green.
