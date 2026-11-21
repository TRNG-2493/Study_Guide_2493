# AI-Assisted Coding and Debugging

## Learning Objectives

By the end of this lesson you will be able to:

- Describe the main **modes of AI coding assistance** (inline completion, chat, explain, refactor, generate tests, debug) and when each one is useful.
- Write **effective prompts for code**: stating language, versions and framework, pasting the right code, stating conventions and choosing the response style you want.
- Use an assistant to **explain unfamiliar code** line by line as a learning tool, without letting it replace your own understanding.
- Write **refactoring prompts** that keep behaviour identical, and check that they did.
- Follow a disciplined **AI-assisted debugging workflow**: reproduce first, read the traceback yourself, then give the AI the full traceback, the minimal code, expected versus actual behaviour and what you already tried.
- Ask for **ranked hypotheses with ways to confirm each**, instead of asking the AI to "just fix it".
- Use AI to help analyse **flaky tests** and to act as a **rubber duck**.
- **Verify AI-produced code**: run it, read the diff, check that imports and APIs exist, refuse fixes that weaken assertions, and prove that a test can fail with a small **mutation check**.

---

## Why This Matters

This week's epic is about using AI across quality engineering *with human validation and responsible use*, and ending the week with your first QA agent. Before you can build an agent that writes or checks test code, you need to be good at the everyday version of that job: **one engineer, one assistant, one piece of test code**.

This is where most quality engineers meet AI first. You open an editor, an assistant offers to finish your line, or you paste a failing test into a chat window and ask "why is this broken?". Used well, this saves real time:

- You get unstuck faster on unfamiliar libraries (a Playwright locator method you have not used, a pytest fixture scope you are unsure about).
- You turn a 60-line traceback into a short list of likely causes.
- You clean up repetitive tests into tidy, parametrized ones.
- You learn faster, because you can ask "explain this line" as many times as you like.

Used badly, it does damage that is hard to see:

- Test code that *looks* professional but calls methods that do not exist.
- "Fixes" that make a red test green by **weakening the assertion**, so the bug ships.
- Tests that can never fail, which is worse than having no test, because they give false confidence.

As a QE, your job is to protect quality. That includes the quality of the test code you write with AI help. In **Project 2 (Test Automation Framework)** you will be writing and debugging a lot of pytest, Playwright and requests code against our running e-commerce example (login, search, cart and checkout). The habits in this lesson are the ones you will use every day on that project.

> This lesson stays at the level of an individual engineer working on a piece of test code. Using AI to build automation at framework scale (scaffolding, page objects across a whole suite) is **AI-assisted automation development**, covered on **Wednesday**.

---

## The Concept

### 1. Modes of AI Coding Assistance

On Monday you met the main categories of AI tools for QE: **chat assistants** (a conversation in a browser or app) and **IDE coding assistants** (built into your editor), plus AI features inside test platforms and LLM APIs. For coding and debugging, it helps to think less about *which product* and more about *which mode of help* you are using. Most assistants offer several of these.

| Mode | What it does | Good for | Watch out for |
|------|--------------|----------|---------------|
| **Inline completion** | Predicts the next few characters, lines or a whole function as you type ("ghost text"). | Boilerplate, repetitive patterns, finishing an obvious line. | It only sees nearby code. It completes *plausibly*, not *correctly*. Easy to accept without reading. |
| **Chat** | A conversation where you ask questions and paste code. | Open questions, design discussions, longer explanations. | Answers depend completely on what context you give it. |
| **Explain** | Describes what a piece of code does. | Learning a new codebase, unfamiliar syntax, onboarding. | Explanations can be confidently wrong on subtle details. |
| **Refactor** | Rewrites code to be cleaner without changing behaviour. | Removing duplication, renaming, extracting fixtures. | "Without changing behaviour" must be checked, not trusted. |
| **Generate tests** | Drafts unit or UI tests for given code. | A first draft of test ideas and structure. | Weak assertions, wrong expected values, tests that cannot fail. (Test design itself is today's lesson on AI-assisted test design.) |
| **Debug** | Helps interpret errors, tracebacks and odd behaviour. | Long tracebacks, unfamiliar errors, flaky tests. | Guessing a fix instead of finding the cause. |

Recall from Monday how these tools work under the hood: a large language model predicts the next token based on the **context** it is given. That single fact explains most of this lesson:

- If the context is missing something (your Python version, the code under test, the actual error), the model fills the gap with **what is most common in its training data**, which may not match your project.
- The model has no built-in way to *run* your code. Unless a tool runs it for you, its answer is a prediction of what *probably* works. **You** are the one who runs it.

### 2. Prompting for Code: Give the Assistant What a Colleague Would Need

Imagine asking a new colleague for help with a test. You would not just say "my test doesn't work". You would show the code, the error, and explain what you expected. Prompting an AI assistant is the same. Today's lessons on **specificity and context** and **format locking** go deeper into these ideas in general; here is how they apply to code.

#### 2.1 State the language, versions and framework

Code that is correct in one version can be wrong in another. Always say:

- **Language and version:** "Python 3.12"
- **Framework and version:** "pytest 8", "Playwright for Python, sync API", "requests 2.x"
- **Where it runs** if relevant: "runs in GitLab CI on Linux" (Week 7)

Why this matters for Playwright in particular: Playwright for Python has both a **sync** API (`page.click(...)`, used in Week 4) and an **async** API (`await page.click(...)`). If you do not say which, you may get async code full of `await` that does not fit your project.

You can find your versions quickly:

```bash
python --version
pytest --version
pip show playwright requests
```

#### 2.2 Paste the code under test, not just the test

An assistant cannot reason about `apply_coupon` if it has never seen `apply_coupon`. If you ask "write tests for my coupon function" without pasting it, the model will invent a function signature and invent the business rules. Paste:

- The function or class being tested.
- Any related constants or configuration (for example `MINIMUM_ORDER = 50.00`).
- The relevant requirement in plain words ("SAVE10 gives 10% off orders of $50 or more; unknown codes raise ValueError").

Keep it **minimal but complete**: enough for the code to make sense, not your whole repository. More text is not automatically better; unrelated code is noise that can pull the answer in the wrong direction.

#### 2.3 State your conventions

Every team has conventions. Tell the assistant yours, otherwise it will use whatever is most common:

- "Use plain `assert` statements, not `unittest` style `self.assertEqual`."
- "Use `pytest.mark.parametrize` for data variations."
- "Put shared fixtures in `conftest.py`."
- "Use Playwright's built-in locators such as `get_by_role` and `get_by_label`, not raw XPath." (Week 4)
- "Follow our naming pattern: `test_<feature>_<condition>_<expected>`."

#### 2.4 Choose the response style

Decide what you want back:

- **Code only:** useful when you know what you want and just need the typing done.
- **Code plus explanation:** better when you are learning or when the change is subtle.
- **Explanation first, then code:** best for debugging, so you can judge the reasoning before looking at a fix.

You will learn to lock output into strict structures (for example JSON) in today's lesson on **format locking**. For everyday coding, a clear instruction such as "Reply with a single Python code block followed by a 3-bullet explanation" is usually enough.

#### 2.5 A weak prompt and a strong prompt

Weak:

```text
write tests for the coupon thing
```

Strong:

```text
I am testing an e-commerce checkout in Python 3.12 with pytest 8.

Here is the function under test:

    COUPONS = {"SAVE10": 0.10}
    MINIMUM_ORDER = 50.00

    def apply_coupon(total, code):
        if code not in COUPONS:
            raise ValueError(f"Unknown coupon code: {code}")
        if total >= MINIMUM_ORDER:
            return round(total * (1 - COUPONS[code]), 2)
        return total

Business rule: SAVE10 gives 10% off orders of $50.00 or more.
Unknown codes must raise ValueError.

Write pytest tests for it.
Conventions: plain assert, use pytest.mark.parametrize for the totals,
use pytest.raises for the error case, one test file named test_cart.py.
Reply with one code block, then a short list of which cases you covered and why.
```

The strong prompt gives the model the code, the rule, the tools, the conventions and the shape of the answer. The result is far more likely to be useful, and it is also **easier for you to review**, because you know exactly what you asked for.

### 3. Using AI to Explain Code (A Learning Tool)

One of the most valuable and lowest-risk uses of an assistant is **explanation**. You do not have to ship an explanation, so a wrong one costs less than wrong code. It is still worth reading critically.

Good uses:

- You inherit a test suite and see a fixture like `@pytest.fixture(scope="session", autouse=True)`. Ask: "Explain what `scope='session'` and `autouse=True` do in this fixture and what would change if I removed each one."
- You see a Playwright line you do not understand: `page.get_by_role("button", name="Checkout").click()`. Ask for a line-by-line breakdown.
- You see a confusing comprehension or regular expression in a helper.

A useful explanation prompt:

```text
Explain this pytest fixture line by line for someone who knows basic Python
but is new to pytest. For each line, say what it does and why it is there.
Then tell me one mistake people commonly make with this pattern.

<paste the fixture here>
```

How to use explanations well:

1. **Predict first.** Before asking, write down what *you* think the code does. Then compare. This turns the assistant into a tutor rather than a crutch.
2. **Check one claim.** Pick one specific statement from the explanation and verify it: run the code, add a `print`, or look it up in the official docs (pytest, Playwright, Python).
3. **Ask "what if" questions.** "What happens if the coupon code is lowercase?" Then test that yourself.

The goal is that after the conversation **you** understand the code. If you could not explain it to a teammate without the AI open, you have not finished learning it.

### 4. Refactoring with AI: "Keep Behaviour Identical"

Refactoring means changing the structure of code **without changing what it does**. In test code, common refactors are:

- Merging near-duplicate tests into one parametrized test (Week 4).
- Moving repeated setup into a fixture, and shared fixtures into `conftest.py`.
- Renaming tests to describe behaviour clearly.

Here is a typical "before" file. The three tests are almost identical:

```python
# test_before.py  -- three near-identical tests
from cart import apply_coupon

def test_save10_on_80():
    assert apply_coupon(80.00, "SAVE10") == 72.00

def test_save10_on_50():
    assert apply_coupon(50.00, "SAVE10") == 45.00

def test_save10_on_49_99():
    assert apply_coupon(49.99, "SAVE10") == 49.99
```

A good refactoring prompt is explicit about the one thing that must not change:

```text
Refactor these three pytest tests into a single test using
pytest.mark.parametrize.

Rules:
- Keep behaviour identical: same inputs, same expected values, same number of cases.
- Do not change, remove or loosen any assertion.
- Add readable ids for each case.
- Do not change cart.py.

Reply with only the new test file.
```

A good answer looks like this:

```python
# test_after.py  -- the same three checks, parametrized
import pytest
from cart import apply_coupon

@pytest.mark.parametrize(
    "total, expected",
    [
        (80.00, 72.00),
        (50.00, 45.00),
        (49.99, 49.99),
    ],
    ids=["above_minimum", "at_minimum", "below_minimum"],
)
def test_save10(total, expected):
    assert apply_coupon(total, "SAVE10") == expected
```

Line by line:

- `@pytest.mark.parametrize("total, expected", [...])` tells pytest to run `test_save10` once for each tuple in the list, passing the values in as the `total` and `expected` arguments.
- Each tuple is one test case: `(80.00, 72.00)` means "for a total of 80.00, expect 72.00".
- `ids=[...]` gives each case a readable name in the report instead of `test_save10[80.0-72.0]`.
- The body has a **single, strict** `==` assertion, identical to the original tests.

How do you *check* that behaviour stayed the same? Run both versions side by side (the `cart.py` here is the correct version of the function shown in section 2.5):

```text
$ pytest -v
collecting ... collected 6 items

test_after.py::test_save10[above_minimum] PASSED                         [ 16%]
test_after.py::test_save10[at_minimum] PASSED                            [ 33%]
test_after.py::test_save10[below_minimum] PASSED                         [ 50%]
test_before.py::test_save10_on_80 PASSED                                 [ 66%]
test_before.py::test_save10_on_50 PASSED                                 [ 83%]
test_before.py::test_save10_on_49_99 PASSED                              [100%]

============================== 6 passed in 0.02s ===============================
```

Three cases before, three cases after, same inputs, same expected values. Then compare the two files carefully (or use `git diff` after replacing the file) to confirm that no value was changed and no case was dropped. Only then delete the old file. Section 7 shows a stronger check you can add: making sure the refactored tests can still **fail**.

### 5. The AI-Assisted Debugging Workflow

Debugging is where assistants can save the most time, and where they can cause the most harm if you skip steps. The workflow below keeps **you** in charge of finding the cause.

```text
1. Reproduce        -> Can I make it fail on demand? Every time, or sometimes?
2. Read it yourself -> What does the traceback say? Which line? Which values?
3. Minimise         -> What is the smallest code that still shows the problem?
4. Ask well         -> Full traceback + minimal code + expected vs actual + what I tried
5. Get hypotheses   -> Ranked causes, each with a way to confirm or rule it out
6. Confirm          -> Test the top hypothesis myself
7. Fix the cause    -> Smallest change; never weaken the test
8. Verify           -> Re-run the failing test, then the whole suite
```

Let us walk through it with a real bug.

#### 5.1 The bug

Here is a version of `cart.py` with a subtle mistake, and a test file for it:

```python
# cart.py  (buggy version)
COUPONS = {"SAVE10": 0.10}
MINIMUM_ORDER = 50.00

def apply_coupon(total, code):
    """Return the order total after applying a coupon code."""
    if code not in COUPONS:
        raise ValueError(f"Unknown coupon code: {code}")
    if total > MINIMUM_ORDER:
        return round(total * (1 - COUPONS[code]), 2)
    return total
```

```python
# test_cart.py
import pytest
from cart import apply_coupon

def test_discount_applied_above_minimum():
    assert apply_coupon(80.00, "SAVE10") == 72.00

def test_discount_applied_at_exact_minimum():
    assert apply_coupon(50.00, "SAVE10") == 45.00

def test_no_discount_below_minimum():
    assert apply_coupon(49.99, "SAVE10") == 49.99

def test_unknown_code_raises():
    with pytest.raises(ValueError):
        apply_coupon(80.00, "BOGUS")
```

Notice the test file is a direct application of **Boundary Value Analysis** from Week 3: a value above the boundary (80.00), exactly on it (50.00) and just below it (49.99). The boundary test is the one that catches the bug.

#### 5.2 Step 1: Reproduce

Run the tests. Then run them again. A bug that fails **every time** is deterministic and much easier to debug than a flaky one (section 6).

```text
$ pytest -q
.F..                                                                     [100%]
=================================== FAILURES ===================================
____________________ test_discount_applied_at_exact_minimum ____________________

    def test_discount_applied_at_exact_minimum():
>       assert apply_coupon(50.00, "SAVE10") == 45.00
E       AssertionError: assert 50.0 == 45.0
E        +  where 50.0 = apply_coupon(50.0, 'SAVE10')

test_cart.py:9: AssertionError
=========================== short test summary info ============================
FAILED test_cart.py::test_discount_applied_at_exact_minimum - AssertionError:...
1 failed, 3 passed in 0.02s
```

#### 5.3 Step 2: Read the traceback yourself first

Before involving any AI, spend one minute reading. pytest gives you a lot of information for free (this is called **assertion introspection**, from Week 4):

- `.F..` : four tests ran; the second one failed, the other three passed.
- `test_discount_applied_at_exact_minimum` : *which* test failed. Its name already hints at a boundary problem.
- `>` marks the line that failed: `assert apply_coupon(50.00, "SAVE10") == 45.00`.
- `E       AssertionError: assert 50.0 == 45.0` : the **actual** value was `50.0`, the **expected** was `45.0`.
- `where 50.0 = apply_coupon(50.0, 'SAVE10')` : pytest shows which call produced the actual value.
- `test_cart.py:9` : file and line number.

From this alone you can form a hypothesis: at exactly $50.00 the discount was **not** applied, while at $80.00 it was. That points at the comparison with the minimum. Many times, reading the traceback carefully is enough to solve the problem without any AI at all. That is the best outcome: faster, and you learned something.

Reading tracebacks yourself also matters because you need to judge whether the AI's explanation is reasonable. If you never read them, you cannot tell a good answer from a confident wrong one.

#### 5.4 Step 3 and 4: Minimise, then ask well

Suppose you are still unsure. Now you ask for help. A good debugging request contains five things:

1. **The full error output**, copied exactly, not paraphrased ("it says something about assert").
2. **The minimal relevant code**: the function and the failing test, not the whole project.
3. **Expected versus actual**, tied to the requirement.
4. **What you already tried**, so the assistant does not repeat it (and so it knows the bug is not flaky).
5. **What kind of answer you want**: causes and how to confirm them, before any fix.

It helps to build this request the same way every time. The script below assembles it as a list of chat messages in the `role`/`content` format that most chat APIs use (a "system" message sets the assistant's overall behaviour; the "user" message is your request). Nothing is sent anywhere: it only builds and prints the request so you can see its structure.

````python
# build_debug_prompt.py
from pathlib import Path

def build_debug_prompt(code, test, failure, expected, tried):
    """Assemble a structured debugging request as a chat message list."""
    system = (
        "You are a senior Python test engineer. "
        "Environment: Python 3.12, pytest 8. "
        "Do not rewrite or weaken the test assertions."
    )
    user = f"""I have a failing pytest test and need help finding the cause.

## Code under test (cart.py)
```python
{code}
```

## Test file (test_cart.py)
```python
{test}
```

## Full pytest output
```text
{failure}
```

## Expected vs actual
{expected}

## What I already tried
{tried}

## What I want from you
1. List the 3 most likely causes, ranked from most to least likely.
2. For each cause, give one quick way I can confirm or rule it out.
3. Only after that, propose the smallest code change that fixes the root cause.
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

if __name__ == "__main__":
    messages = build_debug_prompt(
        code=Path("cart.py").read_text(),
        test=Path("test_cart.py").read_text(),
        failure="E       AssertionError: assert 50.0 == 45.0\n"
                "E        +  where 50.0 = apply_coupon(50.0, 'SAVE10')",
        expected="Requirement: SAVE10 gives 10% off orders of $50 or more. "
                 "For a $50.00 order I expect 45.00, but I get 50.0.",
        tried="Re-ran the test 3 times: it fails every time (not flaky). "
              "The $80.00 test passes.",
    )
    for m in messages:
        print(f"[{m['role']}] {len(m['content'])} characters")
    print(messages[1]["content"][:120])
````

Output (run in the folder containing the buggy `cart.py` and `test_cart.py`):

~~~text
[system] 120 characters
[user] 1564 characters
I have a failing pytest test and need help finding the cause.

## Code under test (cart.py)
```python
# cart.py  (buggy
~~~

How the code works:

- `from pathlib import Path` and `Path("cart.py").read_text()` read the source files directly, so you paste the **real** current code rather than retyping it (retyping is how typos and outdated versions sneak in).
- The function takes five pieces of information, matching the five things a good request needs.
- The `f"""..."""` string is a multi-line **f-string**: anything inside `{...}` is replaced with the variable's value.
- The headings (`## Code under test`, `## Full pytest output`) and the fenced blocks act as **delimiters**: they make it obvious to the model where the code ends and the error output begins. You will see more on delimiters in today's lesson on specificity and context.
- The **system** message holds rules that apply to the whole conversation, including an important guard: "Do not rewrite or weaken the test assertions."
- The final "What I want from you" section asks for **ranked hypotheses and confirmation steps first**, and a fix only after that.
- The `if __name__ == "__main__":` block runs only when you execute the file directly. It prints each message's role and size and the first 120 characters, so you can check the request looks right before sending it.

(For a short failure like this one, the five-line `failure` string is enough. For a long failure, paste the **whole** pytest output; the lines above the `E` lines often contain the clue.)

#### 5.5 Step 5: Hypotheses, not "fix it"

Why ask for **ranked hypotheses with confirmation steps** instead of "fix it"?

- "Fix it" invites the model to change *something* until the test would pass. The easiest change that makes a test pass is often to change the **test**, which hides the bug.
- A list of hypotheses keeps you thinking about the **cause**. You stay the investigator; the AI is a well-read assistant suggesting where to look.
- Each hypothesis comes with a **cheap experiment**. You run the experiment and the evidence decides, not the model's confidence.

Here is the kind of answer you might get back. *This is an illustrative example written for this lesson, not output from a real model run*; real answers vary from run to run (remember **temperature** from Monday).

```text
Most likely causes, ranked:

1. Boundary comparison uses > instead of >=.
   The rule says "$50 or more", but `if total > MINIMUM_ORDER` excludes 50.00.
   Confirm: call apply_coupon(50.00, "SAVE10") and apply_coupon(50.01, "SAVE10").
   If 50.01 is discounted and 50.00 is not, this is the cause.

2. MINIMUM_ORDER is set to the wrong value somewhere else.
   Confirm: print(cart.MINIMUM_ORDER) inside the test, or search the project for
   other assignments to MINIMUM_ORDER.

3. Floating-point representation of 50.00 is slightly above or below 50.
   Confirm: print(repr(50.00)) and print(50.00 == 50). (Unlikely: 50.0 is
   represented exactly in binary floating point.)

Smallest fix for cause 1: change `if total > MINIMUM_ORDER:` to
`if total >= MINIMUM_ORDER:` in cart.py. Do not change the test; it matches
the requirement.
```

Notice what makes this a good answer: it connects the code to the **requirement** ("$50 or more"), it proposes experiments you can run in seconds, it ranks unlikely causes lower and says why, and it explicitly keeps the test unchanged.

#### 5.6 Step 6 to 8: Confirm, fix, verify

You run the first experiment: 50.01 is discounted, 50.00 is not. Hypothesis 1 is confirmed by **evidence**. You make the one-character fix in `cart.py`:

```python
    if total >= MINIMUM_ORDER:
```

Then you re-run the failing test, and then the **whole** suite (a fix in one place can break something elsewhere):

```text
$ pytest -v
collecting ... collected 4 items

test_cart.py::test_discount_applied_above_minimum PASSED                 [ 25%]
test_cart.py::test_discount_applied_at_exact_minimum PASSED              [ 50%]
test_cart.py::test_no_discount_below_minimum PASSED                      [ 75%]
test_cart.py::test_unknown_code_raises PASSED                            [100%]

============================== 4 passed in 0.02s ===============================
```

Finally, commit the fix as a **small, focused commit** (Week 1-2 Git skills) with a message that explains the cause, for example `Fix SAVE10 boundary: apply discount at exactly $50 (>= not >)`. Small commits make AI-assisted changes easy for reviewers to read and easy to revert if something turns out wrong.

#### 5.7 Useful pytest options while debugging

These are not AI features, but they make the information you give an AI (and read yourself) much better. They are described in the pytest documentation on handling failures (see Additional Resources):

| Command | What it does |
|---------|--------------|
| `pytest -x` | Stop at the first failure, so you focus on one problem at a time. |
| `pytest -k "exact_minimum"` | Run only tests whose names match the expression. |
| `pytest -v` | Verbose: one line per test with its result. |
| `pytest -l` | Show local variable values in tracebacks. Very useful context to paste. |
| `pytest --lf` | Re-run only the tests that failed last time. |
| `pytest --pdb` | Drop into the Python debugger at the point of failure so you can inspect values yourself. |

### 6. Flaky Tests and Rubber-Duck Debugging

#### 6.1 Analysing flaky tests with AI

A **flaky test** passes sometimes and fails sometimes without any code change. Flaky tests are among the most expensive problems in automation: they waste time, and they teach teams to ignore red builds.

An assistant can help you think through the possible causes, but you must give it the right evidence. A flaky test cannot be debugged from a single failure output, because one run tells you nothing about the pattern. Collect first:

- How often does it fail? (For example, "3 out of 20 runs".)
- Does it fail alone, or only when run with other tests? Does order matter?
- Does it fail only in CI (Week 7) and not locally?
- The full output of a **failing** run and, if possible, a **passing** run.

The most common causes in UI and API test code are:

| Cause | Typical sign | What to check |
|-------|--------------|---------------|
| **Timing and waits** | Element "not found" or "not visible" sometimes; fails more on slower CI machines. | Hard-coded `time.sleep(...)`, reading a value before the page has updated, or bypassing Playwright's **auto-waiting** (Week 4). Prefer Playwright locators and web-first assertions such as `expect(locator).to_have_text(...)`, which wait automatically. |
| **Shared state** | Fails only when run after another test. | A module-level variable, a fixture with `scope="session"` that one test modifies, a shared test user whose cart is not emptied. |
| **Test order dependence** | Passes alone (`pytest -k name`), fails in the full run. | One test relies on data another test created. Each test should set up what it needs. |
| **External dependencies** | Network errors, timeouts, different data each run. | Real services, real time (`datetime.now()`), random data without a fixed seed. Week 7's mocking techniques help isolate these. |

A useful flaky-test prompt:

```text
This Playwright (Python, sync API) + pytest test fails about 3 times in 20 runs
in GitLab CI, and has never failed locally. Code and two outputs (one failing,
one passing) are below.

List the most likely causes of the flakiness, ranked, considering timing and
waits, shared state between tests, test order and external dependencies.
For each cause, tell me what evidence in the outputs supports or contradicts
it, and one experiment to confirm it.
Do not suggest adding time.sleep or retries as a fix.

<code>
<failing output>
<passing output>
```

The last line is important. An assistant's most "likely" suggestion for flakiness is often to add a `sleep` or to retry the test until it passes. Both **hide** the problem rather than fix it. (Retry strategies in automated AI pipelines are a separate topic covered in **Week 9**.)

#### 6.2 Rubber-duck debugging with AI

**Rubber-duck debugging** is an old programming technique: you explain your code, line by line, to a rubber duck on your desk. Very often, in the middle of explaining, you notice the bug yourself, because explaining forces you to check every assumption.

An AI assistant makes a good rubber duck because it can ask questions back. A prompt for this:

```text
I want to debug this myself. Do not give me the answer.
I will explain what my test does step by step. After each step, ask me one
question that checks whether my assumption is correct.
```

This mode is especially useful while you are learning, because the understanding stays with you. It also avoids the risk of pasting large amounts of code at all.

### 7. Verifying AI-Produced Code

Everything an assistant gives you is a **draft**. The rule for this week is simple: **you are responsible for every line you commit, whoever typed it.** The formal human-validation process and checklists for AI output are covered on **Wednesday**. This section gives you the hands-on, coding-level checks you need today.

#### 7.1 Run it

The most basic and most important check: **run the code**. Run the specific test, then the whole suite. Code that "looks right" has not been tested until it has run.

#### 7.2 Read the diff

When an assistant edits a file, look at exactly what changed. `git diff` (Week 1-2) shows every line added and removed. Look especially for:

- Changes you did not ask for (a "refactor" that also changed an expected value).
- Removed tests or removed assertions.
- New dependencies or imports.
- Deleted error handling.

#### 7.3 Check that imports and APIs exist

Monday introduced **hallucination**: the model producing confident, plausible content that is not true. In code, this often looks like a function or method that *sounds* right but does not exist, or an API from an older version that has since been removed (a **deprecated** API). Typical examples:

- `json.parse(...)` in Python (that is JavaScript; Python uses `json.loads`).
- `pytest.assert_raises(...)` (pytest uses `pytest.raises`).
- A Playwright method name that mixes up Selenium (Week 6) and Playwright (Week 4) styles.

You can check quickly in Python whether a name exists:

```python
# check_apis.py
import importlib

# Names an assistant used in a suggested snippet: (module, attribute path)
SUGGESTED = [
    ("json", "loads"),
    ("json", "parse"),            # JavaScript habit, not Python
    ("pytest", "raises"),
    ("pytest", "assert_raises"),  # sounds plausible, does not exist
    ("pytest", "mark.parametrize"),
    ("pytest", "mark.parameterize"),  # common misspelling
]

def exists(module_name, attr_path):
    obj = importlib.import_module(module_name)
    for part in attr_path.split("."):
        if not hasattr(obj, part):
            return False
        obj = getattr(obj, part)
    return True

for module_name, attr_path in SUGGESTED:
    status = "ok" if exists(module_name, attr_path) else "NOT FOUND"
    print(f"{module_name}.{attr_path:22} {status}")
```

Output:

```text
json.loads                  ok
json.parse                  NOT FOUND
pytest.raises                 ok
pytest.assert_raises          NOT FOUND
pytest.mark.parametrize       ok
pytest.mark.parameterize      ok
```

How it works:

- `importlib.import_module("json")` imports a module from its name as a string.
- `attr_path.split(".")` turns `"mark.parametrize"` into `["mark", "parametrize"]` so we can walk down one attribute at a time.
- `hasattr(obj, part)` returns `True` if the object has an attribute with that name; `getattr` then fetches it so we can check the next part.

Look closely at the last line: the misspelled `pytest.mark.parameterize` reports **ok**. That is because `pytest.mark` creates marks dynamically for *any* name you ask for, so `hasattr` cannot tell you the name is wrong. Only **running** the test reveals it:

```text
test_typo.py:3: in <module>
    @pytest.mark.parameterize("x", [1, 2])
     ^^^^^^^^^^^^^^^^^^^^^^^^
E   Failed: Unknown 'parameterize' mark, did you mean 'parametrize'?
```

The lesson: quick existence checks are useful, but they are not a substitute for running the code and reading the **official documentation**. When an assistant uses an API you do not recognise, look it up in the official docs for your version.

#### 7.4 Never accept a fix that weakens the test

This is the most important rule in the lesson, so here is a concrete example. Go back to the buggy `cart.py` from section 5.1 (still using `>`). Suppose you asked an assistant to "make the failing test pass", and it suggested this:

```python
# test_weakened.py  -- the AI's "fix" (DO NOT ACCEPT)
from cart import apply_coupon

def test_discount_applied_at_exact_minimum():
    result = apply_coupon(50.00, "SAVE10")
    # AI comment: "Accept either value to handle the edge case"
    assert result in (45.00, 50.00)
```

Run it against the **buggy** code:

```text
$ pytest -q test_weakened.py
.                                                                        [100%]
1 passed in 0.01s
```

The test is green, and the bug is still there. A customer with a $50.00 cart will be charged $50.00 instead of $45.00. The "fix" did not fix anything; it **removed the test's ability to detect the bug**. The comment even makes it sound reasonable ("handle the edge case").

Ways a test gets weakened, all of which you should reject unless the **requirement** itself changed:

- Changing the expected value to match the actual (wrong) output.
- Accepting several possible values (`in (...)`), or using a very loose comparison.
- Replacing a specific check with a vague one (`assert result` or `assert result > 0`).
- Wrapping the code in `try/except` that swallows the error.
- Adding `@pytest.mark.skip` or `@pytest.mark.xfail` to make the failure disappear.
- Deleting the test.

The question to ask every time: **"Did the code change, or did the test change?"** If the test changed, the change must be justified by the requirement, not by the code's current behaviour. A failing test is information. Your job is to understand it, not silence it.

#### 7.5 Make sure the test can fail: a small mutation check

A test that can never fail gives you false confidence. AI-drafted tests are especially prone to this, because "make sure the test passes" is an easy target for a model. How do you know a test can catch a bug? **Put a bug in on purpose and see whether the test notices.** This idea is called **mutation testing**: each deliberate small change is a **mutant**; if a test fails, the mutant is **killed** (good); if all tests still pass, the mutant **survived** (your tests have a gap).

Here is a correct `cart.py` and two tests an assistant might draft for it:

```python
# cart.py  (correct version)
COUPONS = {"SAVE10": 0.10}
MINIMUM_ORDER = 50.00

def apply_coupon(total, code):
    if code not in COUPONS:
        raise ValueError(f"Unknown coupon code: {code}")
    if total >= MINIMUM_ORDER:
        return round(total * (1 - COUPONS[code]), 2)
    return total
```

```python
# test_ai_generated.py  -- tests an assistant drafted
from cart import apply_coupon

def test_coupon_returns_a_value():
    result = apply_coupon(80.00, "SAVE10")
    assert result is not None

def test_coupon_at_minimum():
    result = apply_coupon(50.00, "SAVE10")
    assert result > 0
```

Both tests pass. They even have sensible names, and one of them targets the boundary. But are they useful? This small script finds out by introducing three bugs, one at a time, and running the tests against each:

```python
# mutation_check.py
import subprocess
import sys
from pathlib import Path

SOURCE = Path("cart.py")
ORIGINAL = SOURCE.read_text()

# Each mutation is a small, deliberate bug: (description, old text, new text)
MUTATIONS = [
    ("boundary: >= becomes >", "total >= MINIMUM_ORDER", "total > MINIMUM_ORDER"),
    ("discount rate: 0.10 becomes 0.20", '"SAVE10": 0.10', '"SAVE10": 0.20'),
    ("discount removed", "return round(total * (1 - COUPONS[code]), 2)", "return total"),
]

def tests_pass():
    """Run pytest quietly; return True if every test passed."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        capture_output=True, text=True,
    )
    return result.returncode == 0

try:
    for description, old, new in MUTATIONS:
        assert old in ORIGINAL, f"mutation target not found: {old}"
        SOURCE.write_text(ORIGINAL.replace(old, new))
        verdict = "SURVIVED (tests missed it)" if tests_pass() else "KILLED (tests caught it)"
        print(f"{description:38} -> {verdict}")
finally:
    SOURCE.write_text(ORIGINAL)  # always restore the real code
```

Output:

```text
boundary: >= becomes >                 -> SURVIVED (tests missed it)
discount rate: 0.10 becomes 0.20       -> SURVIVED (tests missed it)
discount removed                       -> SURVIVED (tests missed it)
```

Every mutant survived. These tests would pass even if the discount were removed completely. They test that the function *returns something*, not that it returns the *right thing*.

How the script works:

- `ORIGINAL = SOURCE.read_text()` saves the correct code so it can always be restored.
- `MUTATIONS` lists three realistic bugs as `(description, old text, new text)` tuples. Each one mirrors a real mistake: an off-by-one boundary, a wrong constant, missing logic.
- `assert old in ORIGINAL` is a safety check: if the text to replace is not found, the "mutation" would silently do nothing and give a misleading result.
- `SOURCE.write_text(ORIGINAL.replace(old, new))` writes the bugged version of the file.
- `tests_pass()` uses `subprocess.run` to run pytest as a separate process. `sys.executable` is the path of the Python running this script, so pytest runs in the same environment. A **return code** of `0` means all tests passed. `-p no:cacheprovider` stops pytest writing its cache folder during these throwaway runs.
- The `try/finally` block guarantees the original code is written back **even if something crashes**. Never skip this when a script modifies source files. (Running it on a clean Git working tree is a second safety net: `git diff` should show nothing afterwards.)

Now strengthen the tests with strict expected values chosen by Boundary Value Analysis:

```python
# test_ai_generated.py  -- strengthened after the mutation check
import pytest
from cart import apply_coupon

@pytest.mark.parametrize("total, expected", [
    (80.00, 72.00),   # well above the minimum
    (50.00, 45.00),   # exactly on the boundary
    (49.99, 49.99),   # just below the boundary: no discount
])
def test_save10(total, expected):
    assert apply_coupon(total, "SAVE10") == expected
```

Run the same mutation check again:

```text
boundary: >= becomes >                 -> KILLED (tests caught it)
discount rate: 0.10 becomes 0.20       -> KILLED (tests caught it)
discount removed                       -> KILLED (tests caught it)
```

All three mutants are now killed. This is evidence, not opinion, that the tests protect the behaviour you care about. Professional tools exist that generate many mutants automatically, but a hand-written check like this one, on the function you are working on, is often enough to expose a weak AI-drafted test in a couple of minutes.

#### 7.6 Do not paste secrets or real customer data

Never paste passwords, API keys, tokens, `.env` contents, real customer data or confidential source code into an assistant your organisation has not approved. Replace them with placeholders (`API_KEY = "<redacted>"`) before sharing a snippet. The full topic of responsible use (privacy, data leakage, bias and organisational policy) is covered on **Wednesday**.

### 8. Putting It Together: A Daily Workflow

Here is a compact routine you can use on Project 2 starting today:

| Situation | What you do | What you ask the AI |
|-----------|-------------|---------------------|
| Writing new test code | Decide the cases yourself (Week 3 techniques), then use the assistant for typing and syntax. | "Write pytest code for these cases. Python 3.12, pytest 8, plain assert, parametrize." |
| Reading unfamiliar code | Predict what it does first. | "Explain this line by line; tell me one common mistake with this pattern." |
| Cleaning up tests | Commit first so you can compare. | "Refactor into parametrize. Keep behaviour identical. Do not change any assertion." |
| A test fails | Reproduce, read the traceback, minimise. | "Here is the full output, minimal code, expected vs actual and what I tried. Rank the likely causes and how to confirm each." |
| A test is flaky | Collect failure rate and failing plus passing outputs. | "Rank likely causes (timing, shared state, order, external). No sleeps or retries as a fix." |
| Before committing | Run all tests, read the diff, check unknown APIs, try a mutation. | Nothing. This part is yours. |

The pattern across every row: **you decide what correct means; the AI helps you get there faster; you verify.**

---

## Practice Exercises

1. **Reproduce and read.** Create `cart.py` (buggy version with `>`) and `test_cart.py` from section 5.1. Run `pytest -q`. Without using any AI, write down in two sentences what the traceback tells you and your top hypothesis. Then run `pytest -l` and note what extra information appears.

2. **Build a debugging request.** Run `build_debug_prompt.py` from section 5.4 against your files. Modify it so the `failure` argument contains the **entire** pytest output (hint: run pytest with `subprocess.run(..., capture_output=True, text=True)` and use `result.stdout`). Print the full user message and check that every section is filled in.

3. **Spot the weakening.** For each of these suggested "fixes" to the failing boundary test, say whether you would accept it and why:
   a. Change `if total > MINIMUM_ORDER:` to `if total >= MINIMUM_ORDER:` in `cart.py`.
   b. Change the expected value in the test from `45.00` to `50.00`.
   c. Add `@pytest.mark.xfail` to the test.
   d. Change the assertion to `assert result <= 50.00`.

4. **Mutation check your own tests.** Write two tests for `apply_coupon` that check the `ValueError` case. Add a fourth mutation to `mutation_check.py` that removes the error (replace the `raise ValueError(...)` line with `return total`). Does your test kill it? If not, improve the test.

5. **Refactor with a guard.** Write four near-identical tests for `apply_coupon` (include an unknown-code case using `pytest.raises`). Write a refactoring prompt that would turn them into parametrized tests. Then do the refactor yourself, run both versions together with `pytest -v`, and confirm the case count and values match.

6. **Rubber duck.** Pick a piece of test code you wrote in Week 4 or Week 7 that you found confusing. Use the rubber-duck prompt from section 6.2 with an approved assistant and write down the one assumption the conversation made you check.

---

## Knowledge Check

1. Name three modes of AI coding assistance and give one good use for each.
2. Why should you state "Playwright for Python, sync API" in a prompt?
3. List the five things a good debugging request should contain.
4. Why is asking for "ranked hypotheses with a way to confirm each" safer than asking the AI to "fix it"?
5. A test passes when run alone but fails in the full suite. Which category of flaky-test cause does this suggest, and what would you check first?
6. An assistant changes `assert total == 45.00` to `assert total in (45.00, 50.00)` and the build goes green. What has happened, and what should you do?
7. In the API existence check, why did `pytest.mark.parameterize` report "ok" even though it is misspelled? What does this teach you?
8. What does it mean when a mutant "survives"?
9. Why does `mutation_check.py` use a `try/finally` block?

<details>
<summary>Answers</summary>

1. Any three of: inline completion (boilerplate, finishing obvious lines), chat (open questions), explain (learning unfamiliar code), refactor (removing duplication), generate tests (a first draft of test structure), debug (interpreting tracebacks).
2. Playwright for Python has sync and async APIs; without saying which, the model may produce async code with `await` that does not fit your project. Versions and frameworks change what correct code looks like.
3. The full error output copied exactly; the minimal relevant code; expected versus actual behaviour tied to the requirement; what you already tried; and what kind of answer you want (causes and confirmations before a fix).
4. "Fix it" invites any change that makes the test pass, often weakening the test and hiding the bug. Ranked hypotheses keep the focus on the root cause, and confirmation steps mean evidence, not the model's confidence, decides.
5. Shared state or test order dependence. Check whether the test relies on data or state created or modified by another test (module-level variables, session-scoped fixtures, shared test users).
6. The test was weakened: it now accepts the buggy result, so it can no longer detect the bug. Reject the change, fix the code (or the requirement understanding), and keep the strict assertion.
7. `pytest.mark` creates marks dynamically for any attribute name, so `hasattr` returns True. Only running the test revealed the error. Existence checks help, but running the code and reading the official docs are the real verification.
8. The deliberately introduced bug did not make any test fail, so the tests have a gap: they would not catch that kind of bug.
9. To guarantee the original source file is restored even if an error occurs during the mutation runs, so the script never leaves a bugged file behind.

</details>

---

## Glossary

- **Inline completion:** An assistant feature that suggests the next part of the code as you type.
- **Refactoring:** Changing the structure of code without changing its behaviour.
- **Traceback:** The report Python and pytest print when an error occurs, showing where it happened and why.
- **Assertion introspection:** pytest's feature of showing the actual values involved in a failed `assert`.
- **Reproduce:** To make a bug happen again on demand, the first step of any debugging.
- **Hypothesis (debugging):** A possible cause of a bug that can be confirmed or ruled out with an experiment.
- **Flaky test:** A test that passes and fails intermittently without any code change.
- **Auto-waiting:** Playwright's built-in behaviour of waiting for elements to be ready before acting on them (Week 4).
- **Rubber-duck debugging:** Finding bugs by explaining code step by step to someone (or something) else.
- **Hallucinated API:** A function, method or parameter suggested by an AI that does not exist.
- **Deprecated API:** An API that still exists or used to exist but is no longer recommended and may be removed.
- **Weakened assertion:** A change that makes a test accept wrong results, so it can no longer detect the bug it was written for.
- **Mutation testing:** Deliberately introducing small bugs (mutants) to check whether tests detect them. A detected mutant is **killed**; an undetected one **survived**.
- **Diff:** A line-by-line view of what changed between two versions of a file (`git diff`).

---

## Summary

- AI coding assistance comes in several **modes**: inline completion, chat, explain, refactor, generate tests and debug. Each has its own strengths and risks.
- Good code prompts state the **language, versions and framework**, paste the **code under test** and the **requirement**, state your **conventions** and say what **response style** you want.
- **Explanation** is a low-risk, high-value use. Predict first, verify one claim, and make sure you understand the code yourself.
- **Refactoring prompts** must say "keep behaviour identical" and forbid changes to assertions. Then check: same cases, same values, all passing.
- The **debugging workflow** is: reproduce, read the traceback yourself, minimise, ask with full context, get **ranked hypotheses with confirmation steps**, confirm with evidence, fix the cause, verify the whole suite, commit small.
- For **flaky tests**, collect the failure pattern first and consider timing and waits, shared state, test order and external dependencies. Reject sleeps and blind retries as fixes.
- **Verify everything**: run it, read the diff, check APIs exist (and remember that running is the real check), **never accept a weakened assertion**, and use a quick **mutation check** to prove a test can fail.
- Never paste secrets or real customer data. Responsible use, human validation checklists and AI-assisted automation at framework scale are covered on **Wednesday**.

---

## Additional Resources

- pytest documentation, *How to handle test failures* (`-x`, `--maxfail`, `--pdb` and related debugging options): https://docs.pytest.org/en/stable/how-to/failures.html
- GitHub Docs, *Best practices for using GitHub Copilot* (choosing the right mode of help, giving context and checking the assistant's work): https://docs.github.com/en/copilot/get-started/best-practices
- GitHub Blog, *How to debug code with GitHub Copilot* (a practical walkthrough of AI-assisted debugging in the IDE and in pull requests): https://github.blog/developer-skills/github/how-to-debug-code-with-github-copilot/
