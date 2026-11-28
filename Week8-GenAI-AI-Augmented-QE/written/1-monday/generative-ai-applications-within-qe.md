# Generative AI Applications within QE

## Learning Objectives

By the end of this lesson you will be able to:

- **Describe** where GenAI helps across the testing life cycle, and what the tester still owns at each stage.
- **Choose** between GenAI, classic ML and ordinary code for a testing task, and justify the choice.
- **Review** a set of AI-generated tests against a requirement and sort each one as keep, contradicts, wrong behaviour, invented or gap.
- **Run** AI-drafted pytest tests and explain why failing tests can mean the tests are wrong, and passing tests can still miss a bug.
- **Evaluate** a proposed GenAI use case for value, risk and how easy it is to check.

---

## Why This Matters

The earlier lessons today explained what AI is and how GenAI writes. This one answers the practical question: **what can it do for a tester, and what can go wrong?**

There are two different relationships between AI and Quality Engineering:

- **AI for testing:** using AI tools to help with testing work, such as drafting tests, reviewing requirements and summarising results. **This is the focus of this week.**
- **Testing of AI:** testing products that contain AI, such as a chatbot or a recommendation engine. You meet that in later weeks of the course.

Developers already use these tools widely, and they are wary of them. In Stack Overflow's 2025 Developer Survey, more developers said they actively distrust the accuracy of AI tools (46%) than said they trust it (33%), and only 3% said they highly trust the output ([Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/ai)). That wariness is healthy, and it points to the tester's role: AI produces a **fast first draft**, and a person who knows how to test **checks it**.

This lesson shows exactly what that checking looks like, using a set of AI-written tests that look professional and are mostly wrong.

> **Using this with the handout:** this lesson goes deeper into **Handout 02, Topic 3**. It uses the same requirement (SAVE10), the same `cart.py`, the same AI draft (`test_cart_ai_draft.py`) and the same reviewed tests (`test_cart_reviewed.py`).

---

## The Concept

### 1. GenAI as a Fast Assistant, Not a Replacement

**GenAI in Quality Engineering** means using AI assistants to speed up testing work: understanding requirements, suggesting test ideas, drafting test cases, generating test data, writing and debugging automation code, and summarising results.

The key idea is a **division of labour**:

- **The AI** is fast at producing drafts, variations and summaries, and it never gets bored.
- **The tester** is responsible for whether the result is **right**: whether it matches the requirement, covers the risks and can actually catch a bug.

An everyday analogy: GenAI is like a very fast, very confident new team member who has read a lot but has never seen your product. Their first drafts are useful, but you would never ship their work without a review. You also would not let them decide what the requirement means.

### 2. Where GenAI Fits in the Testing Life Cycle

Here is an overview of where AI helps in each testing activity, and what stays with the person. On Wednesday, in *AI within the QA Lifecycle*, you will go through these phases one by one; for now, the big picture is enough.

| Testing activity | How AI helps | Example | What the human still owns |
|---|---|---|---|
| **Requirements** | Spots vague words, missing rules and contradictions | "'Fast search' has no number. How fast?" | Confirming the answer with the business analyst |
| **Test design** | Brainstorms test ideas and edge cases quickly | "What if the coupon is applied twice?" | Choosing the technique and the expected results |
| **Test data** | Generates many realistic records | 50 shipping addresses in different formats | Checking the data follows the rules |
| **Automation** | Drafts test code and page objects | A first pytest or Playwright test | Making sure each test can actually fail |
| **Debugging** | Explains errors and suggests fixes | "This timeout is probably a missing wait" | Confirming the real cause before changing code |
| **Reporting** | Summarises results and drafts bug reports | A summary of 300 failure messages | Accuracy, and the final decision |

Notice the right-hand column. In every row, the human owns the **judgement**: what is correct, what matters, and what to do next.

### 3. A Closer Look at the Main Applications

#### 3.1 Reviewing requirements

Give an AI a user story, and ask it to point out anything vague or untestable. It is good at spotting words such as "fast", "user-friendly" and "appropriate", which have no measurable meaning. It can also suggest questions to ask.

For example, given *"As a shopper, I want search results to appear fast so that I don't give up"*, a typical reply (illustrative) is:

```text
"Fast" is not measurable. Questions for the product owner:
1. What is the maximum acceptable time, and measured from when to when?
2. Does the limit apply on mobile networks as well as broadband?
3. How many results must appear within that time?
```

Those are good questions, and they would take a person a few minutes to think of.

**The risk:** it may invent an answer to its own question, such as "fast means under 2 seconds", and then write tests for its own number. Only the business can decide that.

#### 3.2 Test ideas and test cases

AI is very good at brainstorming: ask for "edge cases for a coupon field" and you get empty input, very long codes, special characters, codes applied twice, and so on, in seconds.

**The risk:** it may contradict the requirement, invent rules, or miss the most important cases. All three appear in the worked example in section 5.

#### 3.3 Test data

AI can produce realistic names, addresses and orders quickly, in whatever format you ask for.

**The risk:** the data may break the rules it was supposed to follow, such as invalid postcodes or dates in the wrong format. It can also look realistic enough to resemble real people, so treat it with the same care as real data. You will go deeper on Wednesday in *AI-Generated Test Data*.

#### 3.4 Automation code and debugging

AI can draft pytest tests, Playwright scripts and page objects, and explain error messages in plain language.

**The risk:** code that runs but proves nothing, such as a test with an assertion that can never fail, or calls to functions that do not exist (the hallucinations from *Generative AI Concepts*). You will practise this on Tuesday in *AI-Assisted Coding and Debugging*.

#### 3.5 Summaries and reports

AI can turn a long log or a page of results into a short summary for a manager, or draft a clear bug report from rough notes.

**The risk:** a summary that sounds right but leaves out the one failure that matters, or gets a number wrong. Always check summary numbers against the source. If the AI says "12 tests failed, all timeouts", count the failures in the real report, and open at least one that it did not call a timeout.

#### 3.6 What the applications have in common

Look back over the five applications, and the same pattern appears every time:

- **The AI is strongest at volume and variety**: many ideas, many records, many lines of code, quickly.
- **It is weakest at being right about your product**: your requirements, your rules, your edge cases. It has never seen them, unless you paste them in.
- **Every output needs a check that fits it**: a question to the business analyst, a run of the code, a count against the source, or a review against the requirement.

Keep that pattern in mind, and you can judge any new AI testing feature you are offered, even one that does not exist yet.

### 4. GenAI, Classic ML or No AI?

GenAI is not the answer to every problem. Choosing the right tool is part of the job:

| If the task… | Use | Why | Testing example |
|---|---|---|---|
| has a clear, exact rule | **Ordinary code (no AI)** | Code is exact, fast, free and gives the same answer every time | Check that an API returns HTTP 200 |
| needs a prediction from lots of labelled history | **Classic ML** | It learns a consistent rule you can measure | Predict which tests are likely to be flaky, from 2 years of labelled runs |
| involves messy language or creative drafting | **GenAI** | It handles free text and produces first drafts | Draft 20 test ideas from a new user story |

A quick way to decide is to ask three questions in order:

1. **Can I write the rule down exactly?** If yes, write normal code.
2. **Do I have lots of labelled examples, and need the same answer every time?** If yes, consider classic ML.
3. **Is the input messy language, or do I need a draft?** If yes, GenAI may help, and its output needs review.

Many real solutions combine them. For example, GenAI drafts test cases, ordinary code checks their format, and a person reviews their meaning. You will build exactly that combination on Friday.

### 5. Worked Example: Review AI-Generated Tests

This is the heart of the lesson. We have a small function and a set of tests written by an AI assistant. The tests look tidy. **Are they right?**

> **The requirement (our running example for the week):** *SAVE10 gives 10% off orders of **$50.00 or more**. Orders under $50.00 are unchanged. Unknown coupon codes raise a ValueError.*

#### 5.1 The code under test

The handout's `cart.py`:

```python
def apply_coupon(total: float, code: str) -> float:
    """SAVE10 gives 10% off orders of $50.00 or more.
    Orders under $50.00 are unchanged. Unknown codes raise ValueError."""
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon: {code}")
    if total >= 50:
        return round(total * 0.9, 2)
    return total
```

What it does:

- If the code is not exactly `"SAVE10"`, it **raises** a `ValueError`.
- If the total is $50 or more, it takes 10% off (`total * 0.9`) and rounds to cents.
- Otherwise, it returns the total unchanged.

**This code is correct.** In this example, we are testing the **tests**.

#### 5.2 The AI's draft tests

This is the kind of thing an AI assistant typically produces when asked *"Write pytest tests for apply_coupon"*. It is **illustrative**: written for the handout to show typical mistakes, not copied from one real model's reply. The file is `test_cart_ai_draft.py`:

```python
from cart import apply_coupon

def test_save10_applies_discount():
    assert apply_coupon(100, "SAVE10") == 90

def test_save10_small_order_gets_discount():
    assert apply_coupon(20, "SAVE10") < 20

def test_unknown_coupon_returns_original_total():
    assert apply_coupon(100, "BOGUS") == 100

def test_coupon_is_case_insensitive():
    assert apply_coupon(100, "save10") == 90
```

Read the test **names**. They all sound sensible. That is exactly why AI output is easy to trust too quickly.

#### 5.3 Run the draft

```bash
python -m pytest -q test_cart_ai_draft.py
```

Output (the timing will differ on your machine):

```text
FAILED test_cart_ai_draft.py::test_save10_small_order_gets_discount - Asserti...
FAILED test_cart_ai_draft.py::test_unknown_coupon_returns_original_total - Va...
FAILED test_cart_ai_draft.py::test_coupon_is_case_insensitive - ValueError: U...
3 failed, 1 passed in 0.01s
```

A beginner's first thought is *"the code has bugs!"* But read the requirement again. **The code is correct; the tests are wrong.** A failing test tells you that the code and the test disagree. It does not tell you which one is wrong. Only the requirement can settle that.

#### 5.4 Review each test against the requirement

Go through the draft one test at a time:

| Test | Verdict | Why |
|---|---|---|
| `test_save10_applies_discount` | ✅ **Keep** | $100 → $90 matches the requirement |
| `test_save10_small_order_gets_discount` | ❌ **Contradicts the requirement** | Orders under $50 are **unchanged**, not discounted |
| `test_unknown_coupon_returns_original_total` | ❌ **Wrong behaviour** | Unknown codes must **raise ValueError**, not return the total |
| `test_coupon_is_case_insensitive` | ❌ **Invented requirement** | Nothing says lowercase codes work. The AI guessed: a hallucination. Ask the business analyst |
| *(missing)* | ⚠️ **Gap** | No **boundary** tests at exactly $50.00 and just below, at $49.99 |

These are the **three classic AI test mistakes**, plus a gap:

1. **Contradicting** the requirement.
2. **Inventing** a requirement that does not exist.
3. **Missing** important cases, especially boundaries.

The invented rule deserves a second look. Case-insensitive coupon codes are common on real shopping sites, so the AI's guess is plausible: it is the "likely text" from *Generative AI Concepts*. But plausible is not the same as required. If you keep that test, you are quietly changing the requirement. The right move is to **remove the test and raise a question**.

#### 5.5 The reviewed tests

The handout's `test_cart_reviewed.py` keeps the good test, fixes two, removes one with a note, and adds the missing boundaries:

```python
import pytest
from cart import apply_coupon

# Kept from the AI draft: correct and useful
def test_save10_gives_10_percent_off_large_order():
    assert apply_coupon(100, "SAVE10") == 90

# Fixed (1): orders under $50 are UNCHANGED
def test_save10_small_order_is_unchanged():
    assert apply_coupon(20, "SAVE10") == 20

# Fixed (2): unknown codes must RAISE ValueError
def test_unknown_coupon_raises_error():
    with pytest.raises(ValueError):
        apply_coupon(100, "BOGUS")

# Removed (3): case-insensitive test - not in the requirement. Ask the BA!

# Added: boundary tests the AI missed
def test_exactly_50_gets_discount():
    assert apply_coupon(50.00, "SAVE10") == 45.00

def test_just_below_50_is_unchanged():
    assert apply_coupon(49.99, "SAVE10") == 49.99
```

Run it with `python -m pytest -q test_cart_reviewed.py`:

```text
.....                                                                    [100%]
5 passed in 0.01s
```

What to notice:

- `with pytest.raises(ValueError):` means "the code inside this block **must** raise a ValueError, or the test fails". This is how you test expected errors.
- The comment for the removed test records **why** it was removed. Good reviewers leave a trail, so the next person does not add it back.
- The two boundary tests use **Boundary Value Analysis** from Week 3: $50.00 is the first value that gets the discount, and $49.99 is the last one that does not.

#### 5.6 The opposite danger: tests that pass but miss the bug

Failing tests at least make you look. The more dangerous case is the reverse. Suppose a developer makes a one-character mistake and writes `>` instead of `>=`:

```python
    if total > 50:      # bug: $50.00 exactly no longer gets the discount
```

Now an order of exactly $50.00 is charged the full price, which breaks the requirement. Which tests would catch it?

- The AI draft's only correct test uses **$100**, which still gets the discount. It **passes**, and the bug ships.
- In the reviewed suite, `test_exactly_50_gets_discount` **fails**, and the bug is caught.

We checked this by running the large-order, small-order and two boundary tests against the buggy version. The result was `1 failed, 3 passed`, and the one failure was the $50.00 boundary test. The boundary test the AI never wrote is the only one that finds the bug.

This is the most important lesson about AI-generated tests: **a passing test is only as good as the review behind it.** Tests that pass tell you nothing if they do not check the places where bugs hide.

#### 5.7 Four quick questions for any AI-written test

Until Wednesday, when you meet a full review checklist in *Human Validation of AI Output*, ask these four questions of every AI-written test:

1. **Which part of the requirement does it check?** If you cannot point to a sentence, it may be invented.
2. **Is the expected result what the requirement says?** Work it out yourself first, then compare.
3. **Could it fail?** Imagine a likely bug, such as `>` instead of `>=`, and ask whether this test would notice.
4. **What is missing?** Boundaries, errors and invalid inputs are the usual gaps.

Asked of the four draft tests in section 5.2, these questions find every problem in the review table, including the missing boundaries.

### 6. Evaluating a GenAI Use Case

Not every idea for using GenAI is a good one. Before adopting one, score it on three questions:

| Question | What to look for |
|---|---|
| **Value:** how much time or risk does it save? | Repetitive, high-volume work scores high |
| **Risk:** what happens if the AI is wrong? | A wrong summary for a stand-up is low risk; a wrong expected result in a release gate is high risk |
| **Checkability:** how easily can a person or code check the output? | Output with a clear format and a clear requirement is easy to check |

**Work it by hand.** Score three ideas from 1 (poor) to 3 (good), where a higher risk score means *less* risky:

| Use case | Value | Risk (3 = low risk) | Checkability | Total |
|---|---|---|---|---|
| Summarise last night's 300 failures for the stand-up | 3 | 3 | 2 | **8** |
| Draft test ideas from a new user story, reviewed before use | 3 | 2 | 3 | **8** |
| Let AI decide on its own whether a release can ship | 2 | 1 | 1 | **4** |

The first two are good starting points: high value, and a person can check the result. The third keeps the AI's mistakes out of sight until they reach customers.

A low score is not always the end of an idea. Often you can **redesign the use case** to raise it. Take the third row. Instead of letting the AI decide, have it **draft a release-readiness summary** (open defects, failed tests, untested stories) that the release manager reads before deciding. Now the risk score rises, because a person makes the decision. Checkability rises too, because every line of the summary can be traced to the test report. The same AI, used differently, becomes a reasonable idea:

| Use case | Value | Risk (3 = low risk) | Checkability | Total |
|---|---|---|---|---|
| AI drafts a release-readiness summary; the release manager decides | 2 | 3 | 3 | **8** |

This redesign move, **"AI drafts, a person decides, and the draft can be traced to a source"**, is one you will use again and again this week, right up to Friday's agent. A simple rule follows: **start where the output is easy to check, and keep a person on decisions that are hard to undo.**

### 7. Setting Realistic Expectations

Two cautions keep expectations honest:

- **The draft is fast; the review is not.** An AI can draft 50 tests in a minute. Reviewing them properly can take an hour. Measure time saved **after** review, not after drafting.
- **Better prompts reduce mistakes, but do not remove them.** On Tuesday you will learn to write prompts that include the requirement, ask for named techniques and forbid assumptions. That cuts down the errors in section 5, but there will still be some, so the review never goes away.

**An illustrative scenario.** A team asks an AI to generate 200 regression tests for checkout in one afternoon, and merges them after a quick skim because "they all pass". Weeks later, a pricing bug at exactly $50.00 reaches production. On inspection, none of the 200 tests used a boundary value, and a dozen asserted behaviour the requirement never mentioned. The tests were fast to produce and looked thorough; they were never reviewed against the requirement.

### 8. The Tool Landscape

You will meet AI in several kinds of tool. The product names change often, so it helps to think in categories:

| Category | What it does | Examples of the kind |
|---|---|---|
| **Chat assistants** | General-purpose question and answer, drafting and explaining | ChatGPT, Claude, Copilot Chat |
| **Coding assistants in the editor** | Suggest and edit code as you type | Copilot in VS Code and similar tools |
| **AI features in testing tools** | Generate test cases or data inside a test-management or automation tool | Varies by vendor |
| **Self-healing and visual tools** | Repair broken locators or compare screenshots intelligently | Often classic ML or deep learning, not GenAI |

Whatever the tool, the questions are the same: which circle of AI is it, what data does it see, and how will you check its output?

### 9. Common Mistakes When Teams Start Using GenAI

| Mistake | What goes wrong | Better habit |
|---|---|---|
| Treating passing tests as proof | Bugs at the boundaries ship, as in section 5.6 | Check that each test can fail |
| Using GenAI where code would do | Slower, costs money, and gives different answers on different runs | Write ordinary code for exact rules |
| Letting the AI fill requirement gaps | Invented rules become "requirements" without anyone deciding | Turn every gap into a question for the business |
| Measuring speed, not quality | "We wrote 200 tests in an hour" hides weak tests | Count defects caught and review time, not just tests written |
| Not saving the prompts that worked | Results cannot be repeated or improved | Keep prompts in `prompts.txt`, as the handout shows |
| Pasting confidential material | Customer data or secrets leave the company | Use only fictional data in this course; Wednesday covers the rules |

### 10. Connecting to Project 2

This week's Project 2 work starts with choosing where GenAI could help your test automation framework. In today's exercise you research and present three GenAI use cases. Use the three questions from section 6 to choose them, and for each one, say **who reviews the output, and how**.

---

## Practice Exercises

1. **Find the requirement gap (paper, 10 min).** The SAVE10 requirement does not say what happens for a total of **$0.00** or a **negative** total. Write one test you would want for each case, then write the question you would send to the business analyst. Why should you **not** just decide the answer yourself?

2. **Can the AI catch the bug? (AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** paste the **buggy** version of `apply_coupon` (with `total > 50`) into your AI assistant, with the requirement as a comment, and ask: *"Write pytest tests for this function based on the requirement in the comment."*
   - **Review:** sort each test into keep, contradicts, wrong behaviour, invented or gap.
   - **Run:** save the tests and run them against the buggy version, then against the correct `cart.py`. Does any test fail on the buggy version?
   - **Record:** did the AI write a $50.00 boundary test? Did it write tests that **match the bug** instead of the requirement?

   *Hint:* if every test passes against the buggy code, the AI tested what the code does, not what it should do.

3. **Score your Project 2 ideas (paper, 15 min).** List three ways GenAI could help your Project 2 test automation framework. Score each on value, risk and checkability, as in section 6, and say who would review the output.

4. **Pick the tool (paper, 10 min).** Choose GenAI, classic ML or ordinary code, with a one-line reason:
   - (a) Fail the build if any test takes longer than 30 seconds.
   - (b) Turn a tester's rough notes into a clear, well-structured bug report.
   - (c) Rank tomorrow's regression tests by how likely they are to fail, using 18 months of labelled results.
   - (d) Suggest missing negative tests for a new password-reset story.

---

## Knowledge Check

1. Name the two relationships between AI and QE, and say which one this week covers.

<details><summary>Answer</summary>

AI for testing (using AI tools to help testing work) and testing of AI (testing products that contain AI). This week covers AI for testing.

</details>

2. Three of the four AI draft tests failed against a correct `cart.py`. What does that tell you?

<details><summary>Answer</summary>

Only that the tests and the code disagree. The requirement decides which is wrong; here, the code is correct and the tests are wrong.

</details>

3. What are the three classic AI test mistakes?

<details><summary>Answer</summary>

Contradicting the requirement, inventing a requirement that does not exist, and missing important cases such as boundaries.

</details>

4. Why is `test_coupon_is_case_insensitive` removed rather than fixed?

<details><summary>Answer</summary>

The requirement says nothing about lowercase codes, so the test invents a rule. Keeping it would quietly change the requirement. The right step is to remove it, note why, and ask the business analyst.

</details>

5. With the `>` bug, why does the AI draft's correct test still pass?

<details><summary>Answer</summary>

It uses a total of $100, which gets the discount with either `>` or `>=`. Only a test at exactly $50.00 shows the difference.

</details>

6. When should you use ordinary code instead of GenAI for a testing task?

<details><summary>Answer</summary>

When the rule can be written down exactly, such as checking for HTTP 200. Code is exact, fast, free and gives the same answer every time.

</details>

---

## Glossary

- **AI for testing:** using AI tools to help with testing work.
- **Testing of AI:** testing products that contain AI.
- **First draft:** AI output that must be reviewed before use.
- **Division of labour:** the AI drafts quickly; the tester owns correctness.
- **Contradicting the requirement:** a test that expects the opposite of what the requirement says.
- **Invented requirement:** a test that checks a rule nobody asked for; a form of hallucination.
- **Gap:** an important case, such as a boundary, that no test covers.
- **Boundary Value Analysis:** testing at and just around the edges of a rule, such as $50.00 and $49.99.
- **`pytest.raises`:** a pytest helper that checks a block of code raises an expected error.
- **Use-case scoring:** judging a GenAI idea by its value, risk and checkability.
- **Checkability:** how easily a person or code can confirm the output is right.
- **"AI drafts, a person decides":** a way to redesign a risky use case so that a person makes the final call and can trace the draft to its source.

---

## Summary

- **GenAI is a fast assistant, not a replacement.** It drafts; the tester owns whether the result is right.
- **It helps across the life cycle**: requirements, test design, data, automation, debugging and reporting. In every activity, the judgement stays with a person.
- **Choose the right tool:** exact rules call for ordinary code, labelled history for classic ML, and messy language or drafting for GenAI.
- **Watch for the three classic mistakes**: contradicting, inventing and missing, especially boundaries.
- **Failing tests do not prove the code is wrong, and passing tests do not prove it is right.** Review every test against the requirement, and make sure it can fail.
- **Start with use cases that are valuable and easy to check**, and keep people on decisions that are hard to undo.

---

## Additional Resources

- Stack Overflow, *2025 Developer Survey: AI* (how developers use and trust AI tools): https://survey.stackoverflow.co/2025/ai
- pytest documentation, *How to write and report assertions in tests* (including `pytest.raises`): https://docs.pytest.org/en/stable/how-to/assert.html
- Google for Developers, *Machine Learning Crash Course: Large language models* (for more on how the tools behind these applications work): https://developers.google.com/machine-learning/crash-course/llm
