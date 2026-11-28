# AI-Assisted Coding and Debugging

## Learning Objectives

By the end of this lesson you will be able to:

- **Describe** the main ways AI helps with code: autocomplete, explaining, drafting, refactoring and debugging.
- **Write** a complete debugging prompt with six parts: code, failing test, full error output, expected vs actual, what you tried, and what you want back.
- **Judge** AI-suggested fixes against the requirement, and recognise the weakened-test trap.
- **Check** that an AI refactor keeps behaviour identical, and explain why passing tests may not prove it.
- **Apply** a five-question check before accepting any AI code change.

---

## Why This Matters

As an automation engineer you spend a lot of time with code: writing tests, reading application code, and working out why a test failed. AI coding assistants can speed up all of it, and they are widely used. GitHub's own guidance for its Copilot assistant gives advice that should sound familiar after today: break down complex tasks, be specific about your requirements, and provide examples of inputs and outputs ([GitHub Docs](https://docs.github.com/en/copilot/get-started/best-practices)).

The danger in AI-assisted debugging is specific, and testers should know it well. When a test fails, there are two ways to make it pass: **fix the code**, or **change the test**. Both turn red into green. Only one of them is right, and an AI that has not seen the requirement cannot tell which. A "fix" that quietly weakens the test lets the real bug ship, with a green build to hide it.

This lesson shows how to ask for help properly, how to judge what comes back, and a habit that catches bad fixes before they reach the codebase.

> **Using this with the handout:** this lesson goes deeper into **Handout 04, Topic 3**. It uses the same shipping rule, the same buggy `shipping.py`, the same `test_shipping.py`, the same six-part debugging prompt and the same two suggested fixes.

---

## The Concept

### 1. Ways AI Helps with Code

**AI-assisted coding and debugging** means using an AI assistant to help write, explain, improve and fix code, including test code. The main modes:

| Mode | What it does | Example in QE | Main risk |
|---|---|---|---|
| **Autocomplete** | Suggests the next lines as you type | Finishing a pytest assertion | Plausible but wrong values |
| **Explaining** | Describes what code does, in plain language | "What does this fixture do?" | A confident but wrong explanation |
| **Drafting** | Writes new code from a description | A first Playwright test | Invented or outdated methods |
| **Refactoring** | Restructures code without changing behaviour | Removing duplication in tests | Behaviour changes by accident |
| **Debugging** | Finds the cause of a failure and suggests a fix | Why a boundary test fails | Fixing the test instead of the code |

Every mode carries the failure modes from *Common Prompt Failure Modes*: hallucinated functions, outdated methods, ignored instructions. This lesson focuses on the last three rows, where a tester's judgement matters most.

### 2. Prompting for Code: Give It What a Colleague Would Need

Imagine asking a senior colleague for help with a failing test. You would not just say "my test is broken". You would show them the code, the test, the error, and what you expected. An AI needs the same, and it cannot ask for it unless you invite it to.

A good debugging prompt has **six parts**:

| Part | Why it matters |
|---|---|
| **The code under test** | So it can see the bug |
| **The failing test** | So it knows what was expected |
| **The full error output** | The real clue is often in the details: the values, the line, the traceback |
| **Expected vs actual** | Removes guesswork about what "wrong" means |
| **What you already tried** | Avoids suggestions you have ruled out |
| **What you want back** | For example, "explain the cause first, then the fix" |

There is one more ingredient, and it is the one people most often leave out: **the requirement**. Without it, the AI can only judge the code and the test against each other, and either could be the wrong one.

### 3. Using AI to Explain Code: A Learning Tool

For anyone new to a codebase, "explain this" is one of the most valuable uses of an AI assistant. You can ask as many times as you like, at whatever level you need:

```text
Explain what this pytest test does, line by line, for a beginner.
Then tell me one way it could pass even if the feature were broken.

### Test
@pytest.mark.parametrize("subtotal, expected", BVA_CASES)
def test_save10_boundaries(subtotal, expected):
    assert apply_coupon(subtotal, "SAVE10") == expected
```

A good reply, **illustrative** and written for this lesson, might begin:

```text
1. @pytest.mark.parametrize("subtotal, expected", BVA_CASES) tells pytest to run the
   test once for each pair in BVA_CASES, passing the pair in as subtotal and expected.
2. def test_save10_boundaries(subtotal, expected): the parameter names must match the
   names in the decorator string.
3. The assert calls apply_coupon with the subtotal and the code "SAVE10", and checks the
   result equals the expected value.
How it could pass on broken code: if a value in BVA_CASES is wrong in the same way as
the code, or if BVA_CASES has no value exactly at the boundary.
```

Check an explanation like this the same way as any AI output. Run the test with `-v` and confirm it really runs once per pair. Change one parameter name and confirm pytest complains, as the handout's Common Errors table says it will. An explanation you have confirmed by running the code is knowledge; one you have only read is a claim.

The second sentence of that prompt is a tester's trick. Asking "how could this pass on broken code?" turns an explanation into a **review**: the AI might point out, for example, that the test is only as good as the values in `BVA_CASES`.

Two cautions:

- **Explanations can be wrong too.** If an explanation does not match what you see when you run the code, trust the run.
- **Do not paste code you are not allowed to share.** The rules from *Specificity and Context* apply to code as much as to logs.

### 4. Worked Example: Debug a Failing Boundary Test

**The situation:** a new function calculates shipping, and one test fails.

> **Requirement:** *Orders of $50.00 or more ship free. Other orders pay $4.99.*

#### Step 1: The code (it has a bug)

The handout's `shipping.py`:

```python
def shipping_fee(subtotal: float) -> float:
    """Orders of $50.00 or more ship free. Other orders pay $4.99."""
    if subtotal > 50:
        return 0.00
    return 4.99
```

You may already have spotted the problem, after seeing the same bug in `cart.py` on Monday. Act as if you have not.

#### Step 2: The tests and the failure

The handout's `test_shipping.py`:

```python
from shipping import shipping_fee

def test_large_order_ships_free():
    assert shipping_fee(80.00) == 0.00

def test_small_order_pays_shipping():
    assert shipping_fee(20.00) == 4.99

def test_exactly_50_ships_free():
    assert shipping_fee(50.00) == 0.00
```

Run `python -m pytest -q test_shipping.py`. The key lines of the output:

```text
..F                                                                      [100%]
E       assert 4.99 == 0.0
E        +  where 4.99 = shipping_fee(50.0)
FAILED test_shipping.py::test_exactly_50_ships_free - assert 4.99 == 0.0
1 failed, 2 passed in 0.01s
```

Read it like a tester:

- `..F` means two passes, then a failure.
- `assert 4.99 == 0.0` shows the actual value (4.99) and the expected value (0.0).
- `where 4.99 = shipping_fee(50.0)` shows exactly which call produced it.
- Tests at $80.00 and $20.00 pass, so the problem is **only at the boundary**.

#### Step 3: A complete debugging prompt

The handout's prompt follows the six-part structure, plus the requirement:

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

The `###` headings are the delimiters from *Specificity and Context*, so each part is easy to find. The requirement is included, which is what lets the AI judge **which side** is wrong.

A good answer, **illustrative**, sounds like this: *"The condition uses `>` (greater than), so 50.00 is not included. The requirement says '$50.00 or more', which needs `>=`."* Notice that it explains the **cause** before the fix, and ties the cause to the words "or more".

#### Step 4: Judge the suggested fixes

AI assistants commonly suggest one of two fixes. **Only one is correct.**

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
| Agrees with the requirement ("$50.00 **or more** ships free")? | ✅ Yes | ❌ No |
| Verdict | **Accept** | **Reject: a weakened test. The bug would ship.** |

Fix B has a tell-tale sign: the test is still called `test_exactly_50_ships_free`, but now checks that $50.00 **pays** shipping. A test whose name contradicts its assertion is a strong signal that someone changed the expectation to fit the code.

#### Step 5: Apply the correct fix and re-run

Change `>` to `>=` in `shipping.py`, and run the tests again:

```text
...                                                                      [100%]
3 passed in 0.01s
```

#### Step 6: Prove the fix is real

A green run proves the tests now agree with the code. To prove the boundary test is actually **protecting** the fix, put the bug back for a moment: change `>=` to `>` again and re-run. You should see the same failure as in Step 2, `assert 4.99 == 0.0`, on `test_exactly_50_ships_free`. Then restore `>=`.

This takes thirty seconds and answers the most important question about any fix: **if this bug came back next month, would a test notice?** Here the answer is yes, because a test sits exactly on the boundary. Without that test, the fix would be unprotected, and a later change, perhaps another AI suggestion, could undo it silently.

### 5. The Weakened-Test Trap

A **weakened test** is a test changed so that it no longer checks what the requirement demands. Common forms:

- **Changing the expected value** to match what the code currently returns, as in Fix B.
- **Deleting or commenting out the assertion**, so the test can never fail.
- **Loosening the check**, for example `assert total < 50` instead of `assert total == 45.00`.
- **Skipping the test**, with `@pytest.mark.skip`, "until later".
- **Catching the error too broadly**, so a crash counts as a pass.

Why do AI assistants suggest these? If the prompt only contains the code, the test and the error, the model sees two pieces of text that disagree, and making the test agree with the code is a perfectly likely continuation. It has no way to know the code is the wrong one. **Including the requirement is what makes the correct fix the most likely one.**

A fix that changes the test is **sometimes correct**: tests have bugs too. The rule is not "never change the test". It is: **the requirement decides which side is wrong.**

### 6. Refactoring with AI: "Keep Behaviour Identical"

**Refactoring** means restructuring code to make it cleaner, without changing what it does. AI is good at it, but "without changing what it does" is the hard part.

Suppose you ask an AI to refactor Monday's `cart.py` "to remove magic numbers". It might return this, **illustrative**:

```python
MIN_SUBTOTAL = 50.00
DISCOUNT = 0.10

def apply_coupon(total: float, code: str) -> float:
    """SAVE10 gives 10% off orders of $50.00 or more."""
    if code.strip().upper() != "SAVE10":          # "more robust" input handling
        raise ValueError(f"Unknown coupon: {code}")
    if total >= MIN_SUBTOTAL:
        return round(total * (1 - DISCOUNT), 2)
    return total
```

The constants are a genuine improvement. But look at the first `if`. The AI has added `.strip().upper()`, described as "more robust". That is not a refactor; it is a **behaviour change**. `"save10"` used to raise an error; now it gives 10% off. It is the same invented "case-insensitive codes" rule you have met all week, slipped in through a refactor.

Now the uncomfortable part. We ran Monday's reviewed test suite, `test_cart_reviewed.py`, against this version:

```text
5 passed in 0.01s
```

**All five tests pass.** None of them tries a lower-case code, so none of them notices. Running the two versions side by side shows the difference immediately: the refactored version returns `90.0` for `apply_coupon(100, "save10")`, while the original raises `ValueError: Unknown coupon: save10`.

Two lessons follow:

1. **Tests only protect the behaviour they check.** A green suite after a refactor proves the checked behaviour is unchanged, nothing more.
2. **Ask for, and check, an explicit list of changes.** A good refactoring prompt says: *"Keep behaviour identical. Do not add input handling or new rules. After the code, list every change you made."* Then read that list, and read the diff yourself.

If the refactor is meant to keep a behaviour that has no test yet, add a test **first**. A test that pins down what the code does today, before a change, is called a **characterization test**. For this case:

```python
import pytest
from cart import apply_coupon

def test_lowercase_code_is_rejected():
    # Characterization test: pins today's behaviour (codes are case-sensitive)
    with pytest.raises(ValueError):
        apply_coupon(100, "save10")
```

Against the original `cart.py`, it passes: `1 passed`. Against the refactored version (save it as `cart_refactored.py` and change the import in a copy of the test), we got:

```text
E       Failed: DID NOT RAISE ValueError
FAILED test_char_ref.py::test_lowercase_code_is_rejected - Failed: DID NOT RA...
1 failed in 0.01s
```

`DID NOT RAISE ValueError` is pytest's way of saying the code was expected to raise an error and did not. The behaviour change is now caught by a test, not by luck.

A note on intent: a characterization test records what the code **does**, which may not be what the requirement **wants**. Here they agree, because US-205 does not mention lower-case codes, so case-sensitive is today's behaviour and nobody has asked for a change. If the business analyst later decides lower-case codes should work, this test changes deliberately, with a requirement behind it, which is the opposite of a weakened test.

### 7. Before You Accept Any AI Code Change

Use this five-question check from the handout every time, not just for debugging:

1. **Do I understand the change?** If not, ask the AI to explain it line by line before accepting it.
2. **Does it agree with the requirement?** Read the requirement again and compare word for word.
3. **Did it change the test or the code?** If it changed the test, be suspicious. Was the test really wrong?
4. **Can the test still fail?** Temporarily break the code (for example, change `>=` back to `>`) and check that the test goes red. A test that cannot fail protects nothing.
5. **Does every function or method actually exist?** If the change uses something you have not seen before, check the official documentation.

Question 4 deserves practice. For `shipping.py`, change `>=` back to `>` and run the tests: `test_exactly_50_ships_free` should fail again. If it does not, the test is not protecting the boundary. This is the same "break it on purpose" habit from *AI-Assisted Test Design*.

### 8. Flaky Tests and Rubber-Duck Debugging

Two more debugging situations where AI helps, with care:

**Flaky tests.** A test that passes sometimes and fails sometimes, from Monday's flaky-test example, is hard to debug because the evidence keeps changing. Give the AI **several** failing runs' output, plus a passing one, and ask it to compare them. Good prompts ask for **hypotheses**, not fixes:

```text
This Playwright test fails about 1 run in 5. Below are two failing runs and one passing run.
List three possible causes. For each, give one experiment that would confirm or rule it out.
Do not suggest adding sleeps or retries as a fix.

### Failing run 1
### Failing run 2
### Passing run
```

A useful answer, **illustrative**, might suggest: the test clicks "Apply coupon" before the cart total has finished updating (experiment: wait for the total to change before clicking); another test leaves a coupon applied to a shared account (experiment: run the test alone, then after the other test); or the payment sandbox is slow at some times of day (experiment: record response times across runs).

Notice two choices in the prompt. It asks for **experiments**, which keeps you in charge of the investigation. And it rules out sleeps and retries, because those hide flakiness rather than fix it, which is the debugging version of the weakened-test trap. You then run the experiments, and only change code once one of them confirms a cause.

**Rubber-duck debugging.** Programmers have long known that explaining a problem out loud, even to a rubber duck on the desk, often reveals the answer. An AI assistant is a duck that talks back. Writing the six-part prompt is itself useful: by the time you have written "expected vs actual" and "what I already tried", you may have spotted the bug yourself. That is a good outcome, not a wasted prompt.

### 9. A Reusable Debugging Prompt

Save the structure from section 4 as a template in `prompts.txt`, with empty sections to fill next time:

```text
=== Debug failing test - v1 ===
Use: get the cause and a fix for one failing pytest test.
--- Prompt (new chat) ---
I need help with a failing pytest test. Explain the cause first, then suggest the
smallest fix. Do not change the test's expected values unless the requirement
shows the test is wrong; if you think it is, say so and explain why.

### Requirement
### Code under test
### Failing test
### Full pytest output
### Expected vs actual
### What I already tried
```

The added sentence about expected values guards directly against the weakened-test trap. It does not stop the AI from suggesting a test change when the test really is wrong; it makes the AI **justify** it from the requirement.

### 10. Common Mistakes in AI-Assisted Debugging

| Mistake | What goes wrong | Better habit |
|---|---|---|
| Pasting only the error message | Generic advice, or guesses | Use all six parts, plus the requirement |
| Leaving out the requirement | The AI cannot tell which side is wrong | Always include it |
| Accepting the first green build | Weakened tests slip through | Ask "did it change the test or the code?" |
| Trusting "refactor" to mean "same behaviour" | Hidden behaviour changes | Ask for a list of changes; add characterization tests |
| Not re-breaking the code | Tests that cannot fail | Break it on purpose once |
| Using unfamiliar functions without checking | Invented or outdated APIs | Check the official docs |

---

### 11. When Not to Ask the AI

AI help is not always the fastest route. Debug it yourself first when:

- **The error message already tells you.** `ModuleNotFoundError: No module named 'cart'` means the file is not where Python is looking. Reading the message is quicker than writing a prompt.
- **You cannot share the code.** Confidential code stays out of public tools, whatever the deadline.
- **You need to learn the skill.** If you are new to pytest, working out one failure yourself, then asking the AI to check your reasoning, teaches more than asking for the answer.
- **The failure depends on things the AI cannot see**, such as a test environment's data, network or configuration. The AI can suggest hypotheses, but only you can run the experiments.

### 12. Connecting to Project 2

Today's exercise asks you to build a prompt library for test design **and debugging** for your Project 2 framework. For the debugging half:

- Save the template from section 9 in `prompts.txt`, and use it the next time a Project 2 test fails.
- Keep a short log of each AI-suggested fix you accepted or rejected, with one line on why. Over a week, the log shows which kinds of suggestion you can trust and which need extra checking.
- Add a characterization test before asking an AI to refactor any part of your framework you depend on, such as a shared fixture or a page object.

On Wednesday, in *AI-Assisted Automation Development*, you will apply the same habits to whole AI-generated Playwright tests.

## Practice Exercises

1. **Add the missing boundary (code, 10 min).** Add a test for $49.99 to `test_shipping.py`. What should the fee be? Run it against both the buggy and the fixed `shipping.py`. Which version passes?

2. **Name the weakening (paper, 10 min).** For each change, say whether it weakens the test, and why:
   - (a) `assert shipping_fee(50.00) == 0.00` becomes `assert shipping_fee(50.00) in (0.00, 4.99)`.
   - (b) `assert shipping_fee(20.00) == 4.99` becomes `assert shipping_fee(20.00) > 0`.
   - (c) A test gains `@pytest.mark.skip(reason="flaky")`.
   - (d) A test's expected value changes from 45.00 to 45.01, and the requirement says 50.01 × 0.9 rounded to cents.

   *Hint:* one of these might be a correct fix, not a weakening.

3. **Debug without the requirement (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** send the six-part prompt from section 4, but **remove** the `### Requirement` section.
   - **Review:** does the AI suggest changing the code or the test? Does it ask what the requirement is?
   - **Run:** apply its suggestion to copies of the files and run the tests. Then break the code on purpose and check whether the test notices.
   - **Record:** compare with the answer you get **with** the requirement, and write two sentences on what the requirement changed.

4. **Catch a refactor (AI tool, 20 min).** Ask your AI to refactor Monday's `cart.py` "to make it cleaner and more robust". Read its answer line by line. List every behaviour change, not just style changes. Write one characterization test that would catch each behaviour change, and run it against both versions.

---

## Knowledge Check

1. Name the six parts of a good debugging prompt.

<details><summary>Answer</summary>

The code under test, the failing test, the full error output, expected vs actual, what you already tried, and what you want back. Including the requirement as well is what lets the AI judge which side is wrong.

</details>

2. Fix A and Fix B both make the test pass. Why is only Fix A correct?

<details><summary>Answer</summary>

The requirement says "$50.00 or more ships free". Fix A changes the code to match that. Fix B changes the test to match the buggy code, so the bug would ship.

</details>

3. What is a weakened test? Give two examples.

<details><summary>Answer</summary>

A test changed so it no longer checks what the requirement demands. Examples: changing the expected value to match the code, deleting the assertion, loosening the check, skipping the test, or catching errors too broadly.

</details>

4. Why do AI assistants sometimes suggest changing the test instead of the code?

<details><summary>Answer</summary>

Without the requirement, the model only sees that the code and the test disagree. Making the test agree with the code is a likely continuation, and it cannot know the code is wrong.

</details>

5. The AI's refactor of `cart.py` passed all five reviewed tests. Why was that not enough?

<details><summary>Answer</summary>

None of the tests tried a lower-case code, so they could not detect that the refactor made codes case-insensitive. Tests only protect the behaviour they check.

</details>

6. What does `DID NOT RAISE ValueError` mean in a pytest failure?

<details><summary>Answer</summary>

The test used `pytest.raises(ValueError)`, expecting the code to raise that error, but the code finished without raising it.

</details>

7. How do you check that a fixed test can still fail?

<details><summary>Answer</summary>

Temporarily reintroduce the bug, such as changing `>=` back to `>`, run the test, and confirm it goes red. Then restore the fix.

</details>

---

## Glossary

- **AI-assisted coding and debugging:** using AI to write, explain, improve and fix code, including tests.
- **Autocomplete:** AI suggestions for the next lines as you type.
- **Refactoring:** restructuring code without changing its behaviour, for example replacing "magic numbers" such as 50 and 0.9 with named constants.
- **Magic number:** a bare number in code, such as 50, whose meaning is not stated where it is used.
- **Debugging prompt:** a prompt with the code, the failing test, the full error, expected vs actual, what you tried and what you want back.
- **Weakened test:** a test changed so that it no longer checks what the requirement demands.
- **Behaviour change:** a change in what code does, as opposed to how it is written.
- **Characterization test:** a test that pins down what code does today, before a change.
- **Diff:** the line-by-line difference between two versions of a file.
- **Flaky test:** a test that passes and fails without any code change.
- **Hypothesis (in debugging):** a possible cause, with an experiment to confirm or rule it out.
- **Rubber-duck debugging:** explaining a problem step by step, which often reveals the answer.
- **`DID NOT RAISE`:** pytest's message when code expected to raise an error inside `pytest.raises` finishes without raising it.
- **Traceback:** the list of function calls Python prints when an error happens, showing where it came from.
- **Fix log:** a short record of AI-suggested fixes you accepted or rejected, and why.
- **Re-breaking:** temporarily putting a bug back to confirm that a test catches it.

---

## Summary

- **AI helps with code in five modes**: autocomplete, explaining, drafting, refactoring and debugging, and each carries the usual failure modes.
- **A good debugging prompt has six parts, plus the requirement.** Without the requirement, the AI cannot tell whether the code or the test is wrong.
- **Beware the weakened-test trap.** A green build after changing the test is only correct if the requirement says the test was wrong.
- **"Refactor" does not guarantee "same behaviour".** Ask for a list of changes, read the diff, and pin important behaviour with characterization tests.
- **Before accepting any change**: understand it, check the requirement, check what was changed, prove the test can fail, and check that every API exists.

---

## Additional Resources

- GitHub Docs, *Best practices for using GitHub Copilot*: https://docs.github.com/en/copilot/get-started/best-practices
- pytest documentation, *How to write and report assertions in tests*: https://docs.pytest.org/en/stable/how-to/assert.html
- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API*: https://help.openai.com/en/articles/6654000
