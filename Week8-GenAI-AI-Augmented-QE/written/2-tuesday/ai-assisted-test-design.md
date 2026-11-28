# AI-Assisted Test Design

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** the division of labour in AI-assisted test design: what the AI does well, and what the tester owns.
- **Write** technique-driven prompts that name the technique, give the rule and its precision, ask for working first and gaps last.
- **Check** an AI's Equivalence Partitioning and Boundary Value Analysis by working the technique yourself.
- **Turn** reviewed test values into a parametrized pytest test.
- **Treat** an AI's "not covered" list as questions, and decide what is in scope using the requirement.

---

## Why This Matters

In Week 3 you learned test design techniques: **Equivalence Partitioning (EP)**, **Boundary Value Analysis (BVA)**, decision tables and state transitions. These techniques exist because nobody can test every possible input. They pick a small set of inputs that is most likely to find defects.

An AI assistant can apply these techniques very quickly. But on Monday you saw an AI draft that missed the $50.00 boundary completely, and that missed boundary was the only test that could catch a `>` instead of `>=` bug. The difference between a useful AI test-design partner and a dangerous one is **how you ask, and whether you check**.

This lesson shows a better way to ask. Instead of *"write me some tests"*, you ask *"apply BVA to this rule, list the boundaries first, and tell me what you didn't cover."* Then you work the technique yourself, compare, and keep only what survives review.

The techniques themselves are standard. The ISTQB Certified Tester Foundation Level syllabus lists equivalence partitioning, boundary value analysis, decision table testing and state transition testing as its black-box test techniques ([ISTQB CTFL syllabus v4.0.1](https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf)). The AI does not replace this knowledge. **You need it to check the AI.**

> **Using this with the handout:** this lesson goes deeper into **Handout 04, Topic 2**. It uses the same BVA prompt for AC1, the same example AI answer (49.00, 50.00, 51.00, 100.00), the same `test_coupon_bva.py` and the same "not covered" list.

---

## The Concept

### 1. The Division of Labour: Who Does What?

**AI-assisted test design** means using an AI assistant as a **thinking partner** to apply test design techniques. The AI is fast at **breadth**: many ideas, laid out quickly. The tester owns **correctness**: the requirement, the expected results and the final decision about what goes into the suite.

| The AI is good at | The tester owns |
|---|---|
| Brainstorming many ideas fast | Choosing the technique |
| Applying a named technique on request | Checking every expected result |
| Laying out tables and test data | Spotting missing or invented cases |
| Turning ideas into Gherkin or pytest drafts | Deciding what goes into the suite |

**An everyday analogy: a junior colleague with a calculator but no experience.** They can list values and fill tables quickly, but they have never seen your product and do not know where its bugs usually hide. You give them a clear method, check their table, and sign off the result.

### 2. From "Write Me Tests" to Technique-Driven Prompts

Compare two prompts:

- **Generic:** *"Write tests for the SAVE10 coupon."* The model produces likely coupon tests, including rules that are not in US-205, and it may or may not hit the boundaries.
- **Technique-driven:** *"Apply Boundary Value Analysis to this rule. List the boundaries first, then the test values with expected totals, then anything you did not cover."*

A technique-driven prompt has four ingredients:

1. **Name the technique.** "Apply BVA", "apply EP", "build a decision table". The technique gives the model a known method to follow, instead of guessing what "tests" means.
2. **Give the rule, exactly.** Paste the acceptance criteria, as in *Specificity and Context*.
3. **Give the precision.** "Money has 2 decimal places" tells the model that the step between values is $0.01, which decides the boundary values.
4. **Ask for working first and gaps last.** "List the boundaries first" makes the model's reasoning visible, so you can check it. "List anything you did not cover" makes gaps visible instead of hidden.

### 3. Worked Example: BVA with an AI Partner

**Goal:** boundary tests for **AC1** (*SAVE10 gives 10% off a subtotal of $50.00 or more*), designed with the AI, checked by you, and turned into a pytest test.

#### Step 1: Ask for a named technique

The handout's prompt:

```text
You are a test designer. Apply Boundary Value Analysis to this rule:

"SAVE10 gives 10% off a subtotal of $50.00 or more.
Subtotals under $50.00 are unchanged." Money has 2 decimal places.

1. First list the boundary (or boundaries) you found.
2. Then list the test values you would use, with the expected total for each.
3. Finally list anything you did NOT cover.
Use a numbered list. Do not invent other rules.
```

Every ingredient from section 2 is there: the technique (BVA), the rule (AC1 and the "unchanged" part of AC2), the precision (2 decimal places), working first (the boundary), and gaps last.

#### Step 2: Work out the boundaries yourself

Before looking at the AI's answer, apply BVA by hand. The rule changes at **$50.00**, and money moves in steps of **$0.01**. The classic three BVA values are:

| Value | Position | Expected total | Why |
|---|---|---|---|
| **49.99** | Just below the boundary | 49.99 (unchanged) | The last value that should **not** get the discount |
| **50.00** | Exactly on the boundary | 45.00 (10% off) | Catches `>` written instead of `>=` |
| **50.01** | Just above the boundary | 45.01 (10% off, rounded) | 50.01 × 0.9 = 45.009, which rounds to 45.01 |

Doing this first matters. If you read the AI's answer before forming your own view, you are more likely to accept it as correct. On Wednesday, in *Human Validation of AI Output*, this effect has a name: **automation bias**.

#### Step 3: Compare with the AI's values

Here is a typical AI answer from the handout, **illustrative**, which stepped in **whole dollars**: `49.00, 50.00, 51.00, 100.00`.

| BVA value | Did the AI include it? |
|---|---|
| 49.99 | ❌ Missed: it used 49.00 |
| 50.00 | ✅ Yes |
| 50.01 | ❌ Missed: it used 51.00 |

| Extra AI values | Useful? |
|---|---|
| 49.00, 51.00 | Not boundaries: a whole dollar away from the edge |
| 100.00 | A fine "typical" value, but not a boundary test |

Why might a model step in whole dollars, even when told "2 decimal places"? Because most BVA examples in training text use whole numbers, such as ages or quantities. The most likely continuation of "apply BVA" is the whole-number pattern. That is the same mechanism behind every failure in *Common Prompt Failure Modes*: likely text, not careful reasoning.

**Check every expected total too.** Is 50.01 → 45.01 right? Yes: 50.01 × 0.9 = 45.009, rounded to cents gives 45.01. An AI might write 45.00 or 45.009; both would be wrong.

#### Step 4: Turn the reviewed values into a pytest test

The handout's `test_coupon_bva.py`, next to Monday's `cart.py`:

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

Run `python -m pytest -v test_coupon_bva.py`. Output (timings will differ):

```text
test_coupon_bva.py::test_save10_boundaries[49.99-49.99] PASSED           [ 33%]
test_coupon_bva.py::test_save10_boundaries[50.0-45.0] PASSED             [ 66%]
test_coupon_bva.py::test_save10_boundaries[50.01-45.01] PASSED           [100%]
============================== 3 passed in 0.02s ===============================
```

What to notice:

- `BVA_CASES` holds the **reviewed** cases from Step 2. **You** wrote every expected value, from the requirement. The AI's role was to suggest; the values in the test come from your review.
- `@pytest.mark.parametrize` (Week 4) runs the same test once per row. The names in `"subtotal, expected"` must match the function's parameters.
- `-v` (verbose) shows each case on its own line, with its values in brackets, so a failure tells you which boundary broke.

#### Step 5: Prove the tests can fail

Passing tests only matter if they would fail on a real bug. Run the same three cases against Monday's buggy `cart_bug.py`, where `total >= 50` became `total > 50`. (Copy `cart.py` to `cart_bug.py`, make that one change, and change the import in a copy of the test file.) We did, and got:

```text
FAILED test_bva_bug.py::test_save10_boundaries[50.0-45.0] - AssertionError: a...
1 failed, 2 passed in 0.01s
```

Exactly one case fails, and it is the one **on** the boundary. Now compare with the AI's original values. Its 49.00 and 51.00 would both pass against the buggy code, because neither sits at the edge. Only its 50.00 would catch the bug, and only because it happened to include it. A whole-dollar answer that had chosen 48.00, 52.00 and 100.00 instead would have missed the bug completely while looking like a reasonable test set.

Breaking the code on purpose to check that a test notices is a habit worth keeping. You will use it again on Wednesday, in *AI-Assisted Automation Development*.

#### Two-value and three-value BVA

The ISTQB syllabus describes two versions of BVA. **Two-value BVA** tests the boundary value and its closest neighbour on the other side: here, 49.99 and 50.00. **Three-value BVA** tests the boundary value and **both** neighbours: 49.99, 50.00 and 50.01. The handout uses three-value BVA. The extra value, 50.01, can catch a different kind of bug, such as a rule coded as `total == 50` by mistake, which would give the discount only at exactly $50.00. When you ask an AI for BVA, say which version you want, so you can check its answer against a clear target.

### 4. Equivalence Partitioning with AI

**Equivalence Partitioning** divides inputs into groups, called **partitions**, that the system should treat the same way. One test value per partition is usually enough, because any value in a partition should behave like any other.

A technique-driven EP prompt:

```text
You are a test designer. Apply Equivalence Partitioning to US-205 AC1-AC3:

### Rules
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
### End of rules

1. First list the partitions, for the coupon code and for the subtotal.
2. Then give one test value per partition, with the expected result.
3. Finally list anything you did NOT cover.
Do not invent other rules.
```

**Work it by hand first.** There are two inputs, so there are partitions for each:

| Input | Partition | Representative value | Expected |
|---|---|---|---|
| Code | Valid: `SAVE10` | `SAVE10` | Depends on the subtotal |
| Code | Invalid: anything else | `BOGUS` | Error: "Coupon code not recognised" |
| Subtotal | $50.00 or more | 80.00 | 10% off: 72.00 |
| Subtotal | Under $50.00 | 20.00 | Unchanged: 20.00 |

A common gap in AI answers is the **invalid-code partition**. Asked about "the SAVE10 rule", a model may partition only the subtotal and forget that the code itself is an input. Your hand-worked table makes that gap obvious.

The reviewed partitions as tests, using Monday's `cart.py` (which raises `ValueError` for unknown codes):

```python
import pytest
from cart import apply_coupon

# Reviewed equivalence partitions: one representative value per partition
EP_CASES = [
    (80.00, "SAVE10", 72.00),        # valid code, subtotal >= 50: discounted
    (20.00, "SAVE10", 20.00),        # valid code, subtotal < 50: unchanged
]

@pytest.mark.parametrize("subtotal, code, expected", EP_CASES)
def test_save10_partitions(subtotal, code, expected):
    assert apply_coupon(subtotal, code) == expected

def test_unknown_code_partition():
    with pytest.raises(ValueError):
        apply_coupon(80.00, "BOGUS")
```

Saved as `test_coupon_ep.py` and run with `python -m pytest -q test_coupon_ep.py`, it gives `3 passed`. EP and BVA work together: EP finds the partitions, and BVA tests the edges between them.

### 5. Decision Tables with AI

When a rule depends on **combinations** of conditions, a **decision table** lists every combination and its expected outcome. US-205 has two conditions that matter together: is the code valid, and is the subtotal at least $50.00?

| Rule | Code valid? | Subtotal ≥ $50.00? | Expected outcome |
|---|---|---|---|
| R1 | Yes | Yes | 10% off (AC1) |
| R2 | Yes | No | Unchanged, show "Spend $50.00 to use SAVE10" (AC2) |
| R3 | No | Yes | "Coupon code not recognised" (AC3) |
| R4 | No | No | "Coupon code not recognised" (AC3) |

Two conditions with two values each give 2 × 2 = 4 combinations. Ask an AI to build the table, and check two things:

- **Are all combinations present?** Count the rows: 4.
- **Is every outcome traceable to an AC?** R4 is interesting. The story does not say which message wins when **both** the code is unknown **and** the subtotal is low. "Coupon code not recognised" is a sensible reading, since an unknown code is checked first, but it is an **interpretation**, not a stated rule. A careful AI answer would flag it as a question; a careless one presents it as fact.

That is the value of a decision table: it forces every combination into the open, including the ones the story forgot.

### 6. Other Techniques, Briefly

The same prompting pattern works for the other techniques from Week 3:

- **State transition testing.** AC4, *only one coupon per order*, describes states: no coupon, one coupon applied. Ask the AI to list the states, the events (apply, remove, apply a second code) and the expected transitions. Check that it covers the **invalid** transition: applying a second coupon while one is applied.
- **Pairwise testing.** When many inputs combine, such as browser × payment method × coupon, pairwise selection picks a small set that covers every **pair** of values. AI can draft the set; a tool or a careful check confirms every pair is covered.
- **Exploratory test charters.** AI is good at suggesting **charters**: short missions such as *"Explore applying and removing coupons quickly, to discover state or timing problems."* A person then does the exploring.

For each, the rule stays the same: name the technique, give the rule, ask for working and gaps, and check the result yourself.

### 7. Reading the AI's "Not Covered" List

The BVA prompt asked the AI to list what it did **not** cover. This is one of the most useful parts of any answer, because it turns hidden gaps into a visible list. A typical answer, **illustrative**:

```text
Not covered:
- Unknown or misspelled coupon codes
- Lowercase "save10"
- Negative or zero subtotals
- Combining SAVE10 with another coupon
```

Treat each line as a **question**, not a fact:

| Item | Is it in the story? | What the tester does |
|---|---|---|
| Unknown codes | Yes, AC3 | Add a test (the EP invalid partition) |
| Lowercase "save10" | No | **Ask the business analyst**; do not assume either way |
| Negative or zero subtotals | No | A good question for the BA: what should happen? |
| A second coupon | Yes, AC4 | Add a test (state transition) |

The AI is good at **suggesting** what might be missing. Only the requirement, or the business analyst, can say what is **in scope**. Notice that the lowercase question appears again; it came up on Monday and in *Specificity and Context* too. When the same question keeps appearing, it is a strong sign the story needs updating.

### 8. From Design to Gherkin and pytest

Reviewed test designs often become **Gherkin** scenarios, which you used with BDD in Week 6. AI is good at this conversion, but it is a place where numbers quietly change. Ask for it, then check the numbers against your reviewed cases.

A correct conversion of the three BVA cases:

```gherkin
Scenario Outline: SAVE10 at the $50.00 boundary
  Given my basket subtotal is <subtotal>
  When I apply the coupon "SAVE10"
  Then my total is <total>

  Examples:
    | subtotal | total |
    | 49.99    | 49.99 |
    | 50.00    | 45.00 |
    | 50.01    | 45.01 |
```

What to check in an AI's conversion:

- **Every value matches your reviewed table.** A converted 45.01 that has turned into 45.00 is a new defect in the test.
- **The coupon code is exact:** `"SAVE10"`, not `"save10"`.
- **Nothing was added.** A conversion should not introduce new scenarios the review did not approve.

### 9. Reusable Prompt Patterns for Test Design

Once a technique-driven prompt works, save it as a pattern in `prompts.txt`, with a placeholder where the rule goes. Three patterns cover most everyday needs:

```text
=== BVA - v1 ===
Use: boundary values for one numeric rule.
--- Prompt (new chat) ---
You are a test designer. Apply three-value Boundary Value Analysis to this rule:
### Rule
<paste the rule here>
### End of rule
Precision: <for example: money has 2 decimal places>.
1. First list the boundary values you found.
2. Then list the test values with the expected result for each.
3. Finally list anything you did NOT cover.
Do not invent other rules.

=== EP - v1 ===
Use: partitions for every input of a story, including invalid ones.
--- Prompt (new chat) ---
Apply Equivalence Partitioning to the rules below. List the partitions for EVERY input,
including invalid inputs, then one test value per partition with its expected result,
then anything you did NOT cover.
### Rules
<paste the acceptance criteria here>
### End of rules

=== Decision table - v1 ===
Use: combinations of conditions.
--- Prompt (new chat) ---
Build a decision table for the rules below. List the conditions first, then every
combination as a row with its expected outcome and the AC it comes from. If a
combination's outcome is not stated in the rules, write NOT SPECIFIED.
### Rules
<paste the acceptance criteria here>
### End of rules
```

Notice how each pattern reuses ideas from today: a named technique, delimiters around the rule, working first and gaps last, and a way out (NOT SPECIFIED). The placeholders in angle brackets are the parts that change each time. On Thursday you will see that a prompt with fixed text and marked slots like these is called a **prompt template**.

### 10. Common Mistakes in AI-Assisted Test Design

| Mistake | What goes wrong | Better habit |
|---|---|---|
| Asking for "tests" without a technique | Generic cases; boundaries left to chance | Name the technique |
| Not giving the precision | Whole-dollar steps; 49.99 and 50.01 missed | State the step size |
| Reading the AI's answer first | You accept its values too easily | Work the technique yourself, then compare |
| Copying the AI's expected values into tests | Wrong expectations become wrong tests | Write expected values from the requirement |
| Forgetting invalid partitions | Unknown codes and bad inputs untested | Ask for partitions for every input, including invalid ones |
| Treating "not covered" as "out of scope" | Real ACs left untested | Check each item against the story |
| Skipping the failure check | Tests that pass on broken code | Break the code on purpose once |

### 11. Light-Touch Sanity Checks Before You Use AI-Designed Tests

Before adding AI-designed tests to a suite, ask:

1. **Traceable?** Can every test be traced to an AC?
2. **Technique applied correctly?** Do the BVA values sit **at** the edges, with the right step size?
3. **Expected results checked?** Did you recalculate every one from the requirement?
4. **Can it fail?** Would a likely bug, such as `>` for `>=`, make at least one test fail?
5. **Gaps recorded?** Did you turn the "not covered" list into tests or questions?
6. **Nothing invented?** Does any test check a rule the story never states, such as case-insensitive codes? If so, remove it and raise a question instead.
7. **Saved?** Is the prompt that produced the design saved in `prompts.txt`, so the design can be repeated and improved?

These are a lighter version of the four quick questions from Monday's *Generative AI Applications within QE*. On Wednesday you get a full review checklist.

### 12. Connecting to Project 2

Today's exercise asks you to build a prompt library for test design and debugging for your Project 2 framework. The patterns in section 9 are a good starting point. For each feature you test in Project 2:

1. Paste its acceptance criteria into the EP pattern, and review the partitions by hand.
2. Run the BVA pattern on every numeric rule, with the right precision.
3. Use the decision-table pattern wherever two or more conditions combine.
4. Turn the reviewed values into parametrized pytest tests, and break the code once to prove they can fail.
5. Keep the "not covered" lists, and turn each item into a test or a question.

Save each working prompt in `prompts.txt` with a version number. By Friday, when you build your QA agent, these patterns become the starting point for its instructions.

---

## Practice Exercises

1. **BVA for a new rule (paper and code, 15 min).** A new rule says: *"Customers aged 18 or over can create an account."* Ages are whole numbers. List the three BVA values and the expected result for each. Then write a function `can_register(age)` and a parametrized pytest test for your three values.

   *Hint:* the step between ages is 1, not 0.01.

2. **Find the AI's gaps (paper, 10 min).** An AI applies EP to US-205 and returns three partitions: subtotal ≥ $50.00, subtotal under $50.00, and subtotal of $0.00. Compare it with the table in section 4. What is missing? Is "$0.00" a separate partition according to the story?

3. **Technique-driven prompt for AC4 (AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** write a prompt asking for **state transition testing** of AC4, *only one coupon per order*. Ask for the states first, then the transitions with expected outcomes, then anything not covered.
   - **Review:** by hand, list the states and events yourself first. Did the AI include applying a second coupon while one is applied? Did it invent a rule, such as "the second coupon replaces the first"?
   - **Run:** turn one approved transition into a pytest test idea in words: precondition, action, expected result.
   - **Record:** list the questions you would send to the business analyst, and save the prompt in `prompts.txt` as `=== AC4 state transitions - v1 ===`.

4. **Check a Gherkin conversion (AI tool, 10 min).** Ask your AI to convert the three reviewed BVA cases into a Gherkin Scenario Outline. Compare every number with `BVA_CASES`. Record any value that changed.

---

## Knowledge Check

1. What does the AI do well in test design, and what does the tester own?

<details><summary>Answer</summary>

The AI is good at breadth: brainstorming, applying a named technique, laying out tables and drafting code. The tester owns the technique choice, every expected result, spotting missing or invented cases, and the final decision.

</details>

2. Name the four ingredients of a technique-driven prompt.

<details><summary>Answer</summary>

Name the technique, give the rule exactly, give the precision (such as 2 decimal places), and ask for working first and gaps last.

</details>

3. What are the three BVA values for "$50.00 or more", with money in cents, and their expected totals?

<details><summary>Answer</summary>

49.99 → 49.99 (unchanged), 50.00 → 45.00, and 50.01 → 45.01.

</details>

4. Why should you work out the boundaries yourself before reading the AI's answer?

<details><summary>Answer</summary>

So that you have an independent view to compare against. Reading the AI's answer first makes you more likely to accept it, even when it is wrong (automation bias).

</details>

5. In the decision table, why is rule R4 (invalid code, low subtotal) worth a question?

<details><summary>Answer</summary>

The story does not say which message wins when both conditions apply. Any expected outcome is an interpretation, so it should be confirmed with the business analyst.

</details>

6. Against the `>` bug, only the 50.00 case failed. What does that tell you about the AI's whole-dollar values 49.00 and 51.00?

<details><summary>Answer</summary>

They cannot catch this bug: both behave the same with `>` and `>=`. Only a value exactly on the boundary shows the difference, which is why BVA picks values at the edge.

</details>

7. An AI's "not covered" list includes "lowercase save10". What should you do?

<details><summary>Answer</summary>

Treat it as a question, not a fact. It is not in the story, so ask the business analyst rather than assuming codes are or are not case-sensitive.

</details>

---

## Glossary

- **AI-assisted test design:** using an AI as a thinking partner to apply test design techniques.
- **Technique-driven prompt:** a prompt that names the technique, gives the rule and precision, and asks for working and gaps.
- **Equivalence Partitioning (EP):** dividing inputs into groups the system should treat the same way, and testing one value per group.
- **Partition:** one such group of inputs.
- **Boundary Value Analysis (BVA):** testing at and just around the edges of partitions.
- **Precision (of a value):** the smallest step between values, such as $0.01 for money in cents.
- **Decision table:** a table of every combination of conditions and its expected outcome.
- **State transition testing:** testing how a system moves between states in response to events.
- **Pairwise testing:** choosing a small set of tests that covers every pair of input values.
- **Exploratory test charter:** a short mission statement for an exploratory testing session.
- **"Not covered" list:** the gaps an AI reports at the end of its answer; to be treated as questions.
- **Automation bias:** the tendency to trust an automated suggestion over your own judgement (covered on Wednesday).
- **Two-value / three-value BVA:** testing the boundary and one neighbour / the boundary and both neighbours.
- **Gherkin Scenario Outline:** a Gherkin scenario run once per row of an Examples table.
- **Prompt pattern:** a saved, technique-driven prompt with placeholders for the rule.

---

## Summary

- **The AI provides breadth; the tester provides correctness.** You own the technique, the expected results and the decision.
- **Ask for a named technique**, with the exact rule and its precision, working first and gaps last.
- **Work the technique yourself before reading the AI's answer**, then compare. Here, the AI stepped in whole dollars and missed 49.99 and 50.01.
- **EP finds the partitions, BVA tests their edges, decision tables cover combinations.** AI often misses invalid partitions and unstated combinations.
- **Put only reviewed values into tests**, using `pytest.mark.parametrize`.
- **Treat the "not covered" list as questions**, and let the requirement decide what is in scope.

---

## Additional Resources

- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* (chapter 4, test analysis and design): https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- pytest documentation, *How to parametrize fixtures and test functions*: https://docs.pytest.org/en/stable/how-to/parametrize.html
- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API*: https://help.openai.com/en/articles/6654000
