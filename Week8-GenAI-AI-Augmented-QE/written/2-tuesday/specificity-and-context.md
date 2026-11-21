# Specificity and Context

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **why vague prompts produce generic output**, using what you learned on Monday about next-token prediction.
- Name the **dimensions of specificity** (task verb, scope, quantity, techniques, audience, depth, tone, length and done-criteria) and add each one to a prompt deliberately.
- Walk a prompt from **vague to specific** in small, testable iterations, and describe what changes in the output at each step.
- Identify the **types of context** a QE prompt needs (product and domain, requirement and acceptance criteria, tech stack and versions, existing code and conventions, constraints and non-goals, audience) and where to find each one.
- Decide **how much context** to include, and explain why more is not always better (signal versus noise, "lost in the middle").
- **Delimit pasted material** with triple quotes or XML-style tags so the model can tell your instructions from your data.
- Ask the model to **state its assumptions** or **ask clarifying questions** when context is missing.
- Build a context-rich prompt in Python with a small `PromptSpec` class, and score prompts with a simple **specificity linter**.

---

## Why This Matters

Imagine you hire a new contractor for your QA team and, on their first morning, you say: "Write some tests for the coupon feature." No requirement document, no idea which framework the team uses, no sense of how many tests you need or who will read them. What do you get back? Probably a handful of reasonable-sounding but generic ideas: "test a valid coupon", "test an invalid coupon", "test an expired coupon". None of them is wrong, but none of them is *useful* either. They don't mention the $50 threshold, they assume an "expired" state that may not exist, and they aren't written in a form your team can automate.

A Large Language Model (LLM) is in the same position as that contractor, except it can't walk over to your desk and ask. It only knows what is in the prompt plus what it absorbed during training. When the prompt is vague, the model fills the gaps with the most typical, average answer it has seen for similar requests. That is the single biggest reason people say "AI gives me generic rubbish": the prompt was generic.

This week's **Epic** is to move you from AI fundamentals, through prompt engineering for QE, to designing and building your first QA agent. Specificity and context sit right at the centre of that journey:

- Every AI-assisted test design or debugging task you do today depends on the model understanding *your* requirement, *your* framework and *your* expectations.
- On Thursday and Friday, when you design an agent, the instructions you write for it will be judged by exactly the same standard: are they specific enough, and do they carry the right context?

For **Project 2 (Test Automation Framework)**, you will soon be asking AI tools to help with test ideas, pytest code, Playwright locators and failure analysis for an e-commerce web app (login, search, cart and checkout). The difference between a useful answer and a waste of time will usually be the five extra sentences of context you chose to include. This lesson teaches you which sentences those are.

---

## The Concept

### 1. Why Vague Prompts Produce Generic Output

On Monday you learned that an LLM generates text by repeatedly predicting **the next token**, based on everything that came before it in the context window. It picks from a probability distribution, shaped by temperature and top-p.

Think about what that means for a vague prompt. If you write:

```text
Write some tests for the coupon feature.
```

the model has very little to condition on. The words "tests" and "coupon feature" appear in thousands of training examples: blog posts, tutorials, Stack Overflow answers, sample projects. The most probable continuation is therefore a blend of all of those: a short, middle-of-the-road list that would fit *almost any* coupon feature in *almost any* application. In statistical terms, the model is giving you something close to the **average** answer.

Now compare:

```text
Design 8 boundary value and equivalence partitioning test ideas for
apply_coupon(total, code). SAVE10 gives 10% off orders of $50.00 or more.
Unknown codes raise ValueError. Return a Markdown table.
```

Every extra detail narrows the space of plausible continuations. The token "$50.00" makes boundary values like 49.99, 50.00 and 50.01 far more likely to appear. The words "boundary value" pull in the vocabulary and structure of that technique, which you learned in Week 3. "Markdown table" fixes the shape of the answer. The model is no longer guessing what kind of coupon feature you have; you told it.

A useful mental model:

> **The model cannot read your mind, your Jira board or your repository. Whatever you leave out, it replaces with a guess, and its guess is the most common answer on the internet.**

This leads to two complementary skills:

1. **Specificity**: being precise about *what you want back* (the task, the amount, the format, the depth).
2. **Context**: giving the model the *facts it needs* to do the task well (the requirement, the tech stack, the conventions).

A prompt can be specific but context-poor ("Give me exactly 8 boundary tests in a table" with no requirement), or context-rich but unspecific (a pasted 3-page spec followed by "thoughts?"). You want both.

#### A quick note on "illustrative" outputs

Throughout this lesson, when we show what a model "might" return, the responses are **illustrative**: written to show the typical pattern you will see, not copied from a specific model run. Real outputs vary between models, versions and even repeated runs (remember temperature from Monday). What does not vary is the direction of the effect: more specificity and better context reliably give more targeted results.

---

### 2. The Dimensions of Specificity

"Be specific" is easy advice to give and hard to apply, because it does not say *specific about what*. It helps to break specificity into separate dimensions you can check one by one.

| Dimension | Question it answers | Vague example | Specific example |
|-----------|---------------------|---------------|------------------|
| **Task verb** | What action should the model take? | "Help with tests" | "Design", "Review", "Rewrite", "List", "Explain" |
| **Scope** | What exactly is in and out? | "the checkout" | "the `apply_coupon` function only, not payment or shipping" |
| **Quantity** | How many items? | "some tests" | "8 to 10 test ideas" |
| **Techniques** | Which method should be applied? | (none) | "boundary value analysis and equivalence partitioning" |
| **Audience** | Who will read or use the result? | (none) | "QA engineers who will automate these in pytest" |
| **Depth** | How detailed should each item be? | (none) | "one line per idea, with input and expected result" |
| **Tone** | What register or style? | (none) | "neutral, suitable for a test plan document" |
| **Length** | How long overall? | (none) | "no more than 200 words of explanation" |
| **Done-criteria** | How will you know the answer is complete? | (none) | "every partition and every boundary must be covered at least once" |

Let's look at each in a little more detail.

**Task verb.** Verbs carry a lot of meaning. "Review this test" and "rewrite this test" lead to very different outputs: the first produces comments, the second produces code. "List" suggests short items; "explain" suggests paragraphs. Start every prompt with the verb that describes the action you want.

**Scope.** Real features are connected. "Test the checkout" could include the cart, coupons, taxes, shipping, payment, emails and order history. If you only care about coupons, say so, and say what is *out* of scope. Saying what you do **not** want is one of the most effective ways to stop a model wandering.

**Quantity.** Without a number, the model picks one, usually somewhere between 3 and 10 because that is common in training data. If you need exhaustive coverage of six boundaries, "some tests" will likely miss some. Give a number or a range, or tie the number to the done-criteria ("one test per boundary").

**Techniques.** This is where your QE knowledge pays off. The model has seen descriptions of boundary value analysis (BVA), equivalence partitioning (EP), decision tables, state transition testing and error guessing. If you *name* the technique, you activate that knowledge. If you don't, the model may produce a random mix of happy paths. Today's lesson on AI-assisted test design goes deeper into prompting with specific techniques.

**Audience.** The same content should be written differently for a junior tester, a developer, or a product manager. Naming the audience changes vocabulary, level of detail and what is assumed to be known.

**Depth.** Do you want a one-line idea per test, or a fully written test case with preconditions, steps and expected results? Without guidance, depth will vary from item to item.

**Tone.** Less critical for test design, but important for bug reports, stakeholder summaries and documentation. "Factual and neutral, no blame" is a useful instruction for defect descriptions.

**Length.** LLMs tend to be generous with words. A length limit forces focus and saves you editing time.

**Done-criteria.** This is the most overlooked dimension, and the most powerful for QE. A done-criterion tells the model what "complete" means: "every equivalence class must appear at least once", "include at least two negative tests", "each expected result must be a specific value, not 'works correctly'". It gives the model a target, and it gives *you* a checklist for reviewing the result.

You do not need all nine dimensions in every prompt. A quick question to a chat assistant may need only two or three. But when the output matters, run through the list and ask: *which of these did I leave for the model to guess?*

---

### 3. A Worked Example: From Vague to Specific in Five Iterations

Let's take the running example from Monday and improve a prompt one step at a time. Here is the requirement for our Project 2 e-commerce app:

> `apply_coupon(total, code)` returns the order total after applying a coupon. The coupon `SAVE10` gives 10% off orders of $50.00 or more. Orders under $50.00 with `SAVE10` are not discounted. Unknown coupon codes raise `ValueError`.

We want test ideas we can later automate in pytest. All responses below are **illustrative**.

#### Iteration 1: The vague prompt

```text
Write some tests for the coupon feature.
```

*Illustrative response:*

```text
1. Test applying a valid coupon code.
2. Test applying an invalid coupon code.
3. Test applying an expired coupon.
4. Test applying a coupon to an empty cart.
5. Test that only one coupon can be used per order.
```

**What went wrong:** The model had no requirement, so it invented a generic coupon system. "Expired coupon" and "one coupon per order" may not exist in our app at all; they are guesses. There are no concrete values, no mention of the $50 threshold, and no expected results. You cannot automate "test a valid coupon code".

#### Iteration 2: Add the requirement (context)

```text
Write some tests for this feature:

"""
apply_coupon(total, code) returns the order total after applying a coupon.
SAVE10 gives 10% off orders of $50.00 or more.
Orders under $50.00 with SAVE10 are not discounted.
Unknown coupon codes raise ValueError.
"""
```

*Illustrative response:*

```text
1. apply_coupon(100, "SAVE10") should return 90.
2. apply_coupon(30, "SAVE10") should return 30.
3. apply_coupon(100, "BOGUS") should raise ValueError.
4. apply_coupon(50, "SAVE10") should return 45.
```

**What improved:** The tests now match *our* feature. There are concrete inputs and expected outputs, and the invented "expired coupon" has disappeared because the requirement says nothing about expiry.

**What is still missing:** Only four tests. No 49.99 or 50.01. No idea of why each test exists. The amounts are integers, while money in our app has two decimal places.

#### Iteration 3: Name the techniques and the quantity (specificity)

```text
Design 8 to 10 test ideas for the function below using equivalence
partitioning and boundary value analysis. Label each idea with the
technique it comes from.

"""
(same requirement as above)
"""
```

*Illustrative response:*

```text
EP-1  Valid code, total in "discount" partition (e.g. 120.00) -> 108.00
EP-2  Valid code, total in "no discount" partition (e.g. 20.00) -> 20.00
EP-3  Unknown code (e.g. "BOGUS") -> ValueError
BVA-1 total = 49.99 with SAVE10 -> 49.99 (just below threshold)
BVA-2 total = 50.00 with SAVE10 -> 45.00 (on threshold)
BVA-3 total = 50.01 with SAVE10 -> 45.01 (just above; 45.009 rounded)
BVA-4 total = 0.00 with SAVE10 -> 0.00
EP-4  Empty string code -> ValueError
EP-5  Lowercase "save10" -> ValueError? (requirement does not say)
```

**What improved:** The boundaries around $50.00 now appear, which is exactly what BVA is for. Each test is traceable to a technique, so you can check coverage. The model even flagged an ambiguity ("requirement does not say") about lowercase codes.

**What is still missing:** The format is loose (we'll want a table we can turn into a `pytest.mark.parametrize` list), rounding is mentioned but not specified, and the model is not sure whether negative totals are valid.

#### Iteration 4: Add audience, format and constraints

```text
Design 8 to 10 test ideas for the function below using equivalence
partitioning and boundary value analysis.

Audience: QA engineers who will automate these with pytest parametrize.

<requirement>
apply_coupon(total, code) returns the order total after applying a coupon.
SAVE10 gives 10% off orders of $50.00 or more.
Orders under $50.00 with SAVE10 are not discounted.
Unknown coupon codes raise ValueError.
</requirement>

Constraints:
- Only SAVE10 exists today; do not invent other coupons.
- Use dollar amounts with two decimal places.
- Expected results must be exact values or "raises ValueError".

Output: a Markdown table with columns ID, Total, Code, Expected, Technique.
```

*Illustrative response:*

```text
| ID | Total  | Code   | Expected          | Technique |
|----|--------|--------|-------------------|-----------|
| 1  | 49.99  | SAVE10 | 49.99             | BVA       |
| 2  | 50.00  | SAVE10 | 45.00             | BVA       |
| 3  | 50.01  | SAVE10 | 45.01             | BVA       |
| 4  | 20.00  | SAVE10 | 20.00             | EP        |
| 5  | 200.00 | SAVE10 | 180.00            | EP        |
| 6  | 100.00 | BOGUS  | raises ValueError | EP        |
| 7  | 100.00 | ""     | raises ValueError | EP        |
| 8  | 0.00   | SAVE10 | 0.00              | BVA       |
```

**What improved:** This output is almost ready to paste into a test file. The format is consistent, values have two decimal places, nothing has been invented, and the audience line nudged the model toward automatable rows. Locking the output format so tightly that a program can parse it is the subject of today's lesson on format locking.

#### Iteration 5: Add done-criteria and permission to raise assumptions

```text
(everything from iteration 4, plus:)

Done when: every equivalence class (discount, no discount, unknown code)
has at least one test, and the values 49.99, 50.00 and 50.01 are all
covered.

Before the table, list any assumptions you had to make because the
requirement is silent (for example about rounding, negative totals or
letter case). Do not resolve them silently.
```

*Illustrative response (start):*

```text
Assumptions:
1. Results are rounded to 2 decimal places using standard rounding
   (50.01 * 0.9 = 45.009 -> 45.01). The requirement does not specify.
2. Negative totals are not tested; behaviour is unspecified.
3. Codes are case-sensitive, so "save10" is treated as unknown.

| ID | Total | Code | Expected | Technique |
...
```

**What improved:** The model now tells you where it guessed. That is enormously valuable to a tester: each assumption is a **question for the product owner** and possibly a missing acceptance criterion. You learned in Week 3 that ambiguous requirements are a major source of defects; here the AI helped surface them because you asked it to.

#### What the five iterations teach us

| Iteration | What we added | Main effect on output |
|-----------|---------------|-----------------------|
| 1 | Nothing | Generic, partly invented, not automatable |
| 2 | The requirement (context) | Correct feature, concrete values |
| 3 | Techniques + quantity | Boundaries found, traceable ideas |
| 4 | Audience + constraints + format | Consistent, near-automatable rows |
| 5 | Done-criteria + assumptions | Complete coverage, gaps made visible |

Two lessons stand out. First, **the biggest single jump came from adding context** (iteration 2). Without the requirement, no amount of wording would have produced the right tests. Second, **each change was small and testable**. You changed one or two things, looked at the output, and decided what to fix next. That iterative loop is the heart of prompt engineering, introduced in today's lesson on prompt engineering principles and practised in this afternoon's demo.

One important caution: even the iteration 5 output must be checked. Is 45.01 right, or should the business round down? Does `apply_coupon(0.00, "SAVE10")` even make sense? The AI makes a strong first draft; you remain responsible for the expected results. Formal human validation of AI output is covered on Wednesday.

---

### 4. Types of Context for QE Prompts

Specificity describes what you want back. Context is the information the model needs to produce it. For quality engineering work, context usually falls into six types.

#### 4.1 Product and domain context

**What it is:** What the application does, who uses it, and the business rules of the domain.

**Example:** "This is an e-commerce web app. Customers browse products, add them to a cart and check out. Prices are in USD with two decimal places. Coupons are applied before tax."

**Why it matters:** Domain knowledge tells the model which risks matter. In e-commerce, money calculations and rounding are high-risk; in a healthcare app, data privacy and correctness of dosages would be. Without it, the model treats your app like a generic one.

**Where it comes from:** The product overview in your project README, the product owner, the "about" page, onboarding docs.

#### 4.2 The requirement: user story and acceptance criteria

**What it is:** The specific behaviour under test, ideally as a user story with acceptance criteria (Week 3 and Week 6).

**Example:**

```text
As a shopper, I want to apply a coupon code at checkout
so that I pay less for qualifying orders.

Acceptance criteria:
- Given my cart total is $50.00 or more, when I apply SAVE10,
  then the total is reduced by 10%.
- Given my cart total is below $50.00, when I apply SAVE10,
  then the total is unchanged and a message explains the minimum.
- Given I enter an unknown code, then an error "Invalid coupon" is shown.
```

**Why it matters:** This is the **test basis**: the source of truth for expected results. Without it, the model invents behaviour (like "expired coupons" in iteration 1). This is usually the most important piece of context in any test design prompt.

**Where it comes from:** Your Jira story (Week 3), the feature file (Week 6), the API specification (Week 7).

#### 4.3 System and tech-stack context, including versions

**What it is:** The languages, frameworks, libraries and versions you are using.

**Example:** "Tests use Python 3.12, pytest 8 and Playwright for Python (sync API). We use the Page Object Model."

**Why it matters:** The model has been trained on many frameworks and many versions of each. If you say "write a test" without naming the stack, you might get JavaScript Playwright, Selenium with Java, or an older API that has since changed. Naming versions matters because libraries evolve: method names change, features are added and deprecated. Saying "Playwright for Python, sync API" rules out a large set of wrong answers immediately.

**Where it comes from:** `requirements.txt` or `pyproject.toml`, `pip show <package>`, your project's README, the CI configuration from Week 7.

#### 4.4 Existing code and conventions

**What it is:** Snippets of your current code, plus your team's style rules.

**Example:** "Here is an existing test from our suite. Follow the same naming pattern (`test_<feature>_<condition>_<result>`), use the `cart` fixture from conftest.py, and do not use `time.sleep`."

**Why it matters:** Without your code, the model writes in its own default style. You then spend time reshaping the output to fit. One short example of "how we do it here" is often worth more than a paragraph of description. (Showing examples in a structured way is the topic of today's lesson on few-shot prompting.)

**Where it comes from:** Your repository; specifically a representative test file, your `conftest.py`, your page objects, any coding guidelines.

#### 4.5 Constraints and non-goals

**What it is:** Rules the output must follow, and things you explicitly do *not* want.

**Examples:**

- "Do not add new dependencies."
- "Only SAVE10 exists; do not invent other coupons."
- "Do not test payment; that is covered by another team."
- "Locators must use `get_by_role` or `get_by_test_id`, never XPath."

**Why it matters:** Models try to be helpful, which often means doing *more* than you asked. Non-goals stop scope creep. Constraints also encode team decisions the model cannot possibly know.

**Where it comes from:** Team agreements, your test plan's "out of scope" section (Week 3), code review feedback you have received before.

#### 4.6 Audience context

**What it is:** Who will read or use the output, and what they already know.

**Example:** "The reader is a product manager with no coding background" versus "The reader is a senior SDET reviewing a pull request."

**Why it matters:** Audience changes everything about presentation: vocabulary, length, level of technical detail, whether code is included at all. A failure summary for a developer should include the stack trace; the same summary for a manager should explain impact and next steps.

**Where it comes from:** You. You know who asked for the work.

#### Summary table

| Context type | Typical source | Prevents |
|--------------|---------------|----------|
| Product/domain | README, product owner | Generic risks, wrong priorities |
| Requirement + acceptance criteria | Jira story, feature file, API spec | Invented behaviour, wrong expected results |
| Tech stack + versions | `requirements.txt`, `pyproject.toml`, CI config | Wrong language, framework or outdated API |
| Existing code + conventions | Repository, `conftest.py`, style guide | Off-style code, ignored fixtures |
| Constraints + non-goals | Test plan, team agreements | Scope creep, forbidden techniques |
| Audience | You | Wrong level of detail or vocabulary |

---

### 5. How Much Context Is Enough?

If context is so valuable, why not paste everything: the whole repository, every Jira ticket, all the logs? There are three reasons not to.

#### 5.1 The context window is finite

On Monday you learned that every model has a **context window**: the maximum number of tokens it can process at once, including both your prompt and its response. Modern windows are large, but they are not unlimited, and every token you add also costs time and (on paid APIs) money. Pasting a 5,000-line log when only 40 lines are relevant wastes all three.

#### 5.2 Irrelevant context dilutes attention

Recall the idea of **attention** from Monday's Generative AI concepts lesson: when producing each token, the model weighs every earlier token to decide what is relevant. Irrelevant material competes for that attention. If your prompt contains the coupon requirement *and* the shipping rules *and* the tax rules *and* the login flow, the model may start mixing them; for example, adding tax to its expected coupon totals, because tax was mentioned.

Think of context in terms of **signal and noise**:

- **Signal** is anything the model needs to do this specific task correctly.
- **Noise** is anything else, even if it is true and interesting.

The goal is the highest ratio of signal to noise, not the largest volume of text. A useful test: for each block you paste, ask "if I removed this, would the answer get worse?" If not, remove it.

#### 5.3 Position matters: "lost in the middle"

Research has shown that models do not use all parts of a long input equally well. A 2023 study by Liu and colleagues, *Lost in the Middle*, found that language models tended to use relevant information best when it appeared near the **beginning or end** of a long input, and performed noticeably worse when the key information was buried in the **middle**. Newer models have improved, but the practical advice still holds:

- Keep prompts as short as the task allows.
- Put **long reference material first** and your **instructions and question at the end**, or state the key instructions clearly at the start and briefly restate the most important one at the end.
- Do not bury the one critical rule ("only SAVE10 exists") in the middle of a long paste.

(How to systematically test an LLM-based product's behaviour as its context grows is a separate topic, covered in Week 10. Here we only care about writing good prompts.)

#### 5.4 A rule of thumb

> Give the model **everything it needs to do the task, and nothing it needs to ignore.**

In practice for QE tasks:

| Task | Usually enough | Usually too much |
|------|----------------|------------------|
| Test ideas for one function | The function's requirement + signature | The whole module's docs |
| Fix one failing test | The test, the error message, the relevant fixture | The entire test suite |
| Review a page object | The page object + one test that uses it | Every page object in the project |
| Summarise a test run | The failure summary lines | Full verbose logs of passing tests |

---

### 6. Delimiting Pasted Material

When you paste a requirement, a log or a block of code into a prompt, the model sees one long stream of text. How does it know where *your instructions* end and *your data* begins? If the pasted requirement contains a sentence like "Write the result to the database", is that an instruction for the model or part of the requirement?

**Delimiters** solve this. They are clear markers around pasted material.

#### 6.1 Triple quotes

```text
Summarise the following bug report in two sentences for a product manager.

"""
Steps: add 2 items ($24.99 each) to cart, apply SAVE10, click Checkout.
Expected: total $49.98, message "SAVE10 requires orders of $50 or more".
Actual: total $44.98, discount applied.
Environment: Chrome 129, staging.
"""
```

Simple and widely understood. Good for a single block of pasted text.

#### 6.2 XML-style tags

```text
Using the requirement and the existing test as a guide, write two more
tests in the same style.

<requirement>
SAVE10 gives 10% off orders of $50.00 or more.
Unknown coupon codes raise ValueError.
</requirement>

<existing_test>
def test_apply_coupon_on_threshold_gives_discount():
    assert apply_coupon(50.00, "SAVE10") == 45.00
</existing_test>
```

XML-style tags are especially useful when you have **several** pieces of material, because each tag has a name. You can then refer to them in your instructions: "Use the `<requirement>` as the source of truth; copy the style of `<existing_test>`." Several model providers' documentation recommends this style. The tag names are not special keywords; the model simply understands the structure. Pick clear, descriptive names.

#### 6.3 Markdown headings and code fences

```text
### Instructions
Explain why this test fails.

### Test code
(code in a fenced block)

### Error output
(error in a fenced block)
```

This works well in chat interfaces, where Markdown is natural.

#### 6.4 Why delimiters help

1. **Clarity:** The model can see exactly which text is data.
2. **Reference:** You can point to a block by name.
3. **Safety:** Instructions that happen to appear *inside* pasted text are less likely to be followed as if you wrote them. (This is a basic hygiene habit. The security topic of deliberately malicious text hidden in inputs, known as prompt injection, is covered in Week 10.)
4. **Reuse:** A prompt with clearly delimited slots is easy to fill with different data each time. Turning that into reusable prompt templates for agents is covered on Thursday.

---

### 7. When Context Is Missing: Assumptions and Clarifying Questions

Sometimes you do not *have* all the context: the story is incomplete, the product owner is on holiday, or you are exploring a new feature. You still have two good options, both of which you saw in iteration 5.

#### 7.1 Ask the model to state its assumptions

```text
If the requirement is silent on something you need, state your
assumption explicitly in a list before your answer.
```

The model still produces an answer, but now every guess is visible. You review the assumptions list first; any wrong assumption tells you which parts of the answer to throw away.

#### 7.2 Ask the model to ask *you* clarifying questions

```text
Before designing tests, ask me up to 5 clarifying questions about
anything that is ambiguous or missing. Wait for my answers.
```

This turns the AI into a requirements reviewer. It is particularly useful early in a feature, when you yourself are not sure what is missing. The model's questions often mirror the questions a good tester would ask in a refinement meeting. (Using AI systematically for requirements analysis is Wednesday's topic; here we just use it as a context-gathering tactic.)

#### 7.3 A small demonstration

The code below uses a **fake LLM**: a tiny deterministic function that imitates how a real model tends to respond in each situation. It is a teaching stand-in, not a real model, so the behaviour is fixed and repeatable. It lets us show the *round trip* (prompt in, response out) without an API key.

```python
def fake_llm(prompt: str) -> str:
    """A deterministic stand-in for a real LLM, for teaching only."""
    asks_for_questions = "ask me clarifying questions" in prompt.lower()
    has_requirement = "<requirement>" in prompt
    if asks_for_questions and not has_requirement:
        return ("Before I design tests, I need to know:\n"
                "1. What discount does the coupon give?\n"
                "2. Is there a minimum order total?\n"
                "3. What should happen with an unknown code?")
    if has_requirement:
        return "ID | Total | Code | Expected\nT1 | 50.00 | SAVE10 | 45.00"
    return "1. Test a valid coupon.\n2. Test an invalid coupon.\n3. Test an expired coupon."


instruction = ("Design boundary tests for our coupon feature. "
               "If you are missing information, ask me clarifying questions "
               "instead of guessing.")

print("--- Without the requirement ---")
print(fake_llm(instruction))

with_context = instruction + """
<requirement>
SAVE10 gives 10% off orders of $50.00 or more. Unknown codes raise ValueError.
</requirement>"""

print("--- With the requirement ---")
print(fake_llm(with_context))

print("--- Vague prompt, no permission to ask ---")
print(fake_llm("Write tests for coupons."))
```

Output:

```text
--- Without the requirement ---
Before I design tests, I need to know:
1. What discount does the coupon give?
2. Is there a minimum order total?
3. What should happen with an unknown code?
--- With the requirement ---
ID | Total | Code | Expected
T1 | 50.00 | SAVE10 | 45.00
--- Vague prompt, no permission to ask ---
1. Test a valid coupon.
2. Test an invalid coupon.
3. Test an expired coupon.
```

**How the code works, line by line:**

- `def fake_llm(prompt: str) -> str:` defines a function that takes the prompt text and returns a response string. The `: str` and `-> str` are type hints (Week 2): they document the expected types.
- `prompt.lower()` converts the prompt to lowercase so the check `"ask me clarifying questions" in ...` works regardless of capitalisation. The `in` operator checks whether one string appears inside another.
- `has_requirement = "<requirement>" in prompt` checks whether we delimited a requirement block.
- The `if` branches choose a response. Real models are not this simple, but the three branches capture three real patterns: asking questions when allowed and context is missing, answering specifically when context is present, and producing a generic list when neither applies.
- `instruction + """..."""` concatenates the instruction with a triple-quoted string containing the requirement, building a context-rich prompt.

The third case is the important warning: **if you give no context and no permission to ask, the model guesses**, and you get the same generic list as in iteration 1 of the worked example.

---

### 8. What Not to Paste

Context is valuable, but some information must never go into a prompt for an external AI tool: passwords, API keys and tokens, real customer personal data (names, emails, addresses, card numbers), and confidential company information your organisation has not approved for AI use. When you need realistic examples, use made-up values such as `test.user@example.com`. The full topic of responsible use, including privacy, data leakage and company policy, is covered on Wednesday.

---

### 9. Building Context-Rich Prompts in Python

So far we have written prompts by hand. In automation work you will often **build prompts in code**, filling in the same structure with different requirements. This keeps prompts consistent and makes them easy to review in Git like any other code. Let's build a small helper.

#### 9.1 The `PromptSpec` class

```python
import textwrap
from dataclasses import dataclass, field


@dataclass
class PromptSpec:
    task: str                      # what to do (starts with a verb)
    audience: str                  # who will read the output
    techniques: list               # test design techniques to apply
    count: str                     # how many items
    output_format: str             # what the answer should look like
    context: dict = field(default_factory=dict)      # name -> pasted text
    constraints: list = field(default_factory=list)  # rules and non-goals

    def build(self) -> str:
        lines = [f"Task: {self.task}"]
        lines.append(f"Audience: {self.audience}")
        lines.append("Apply these techniques: " + ", ".join(self.techniques))
        lines.append(f"Quantity: {self.count}")
        lines.append("")
        for name, text in self.context.items():
            lines.append(f"<{name}>")
            lines.append(textwrap.dedent(text).strip())
            lines.append(f"</{name}>")
            lines.append("")
        if self.constraints:
            lines.append("Constraints:")
            for rule in self.constraints:
                lines.append(f"- {rule}")
            lines.append("")
        lines.append(f"Output format: {self.output_format}")
        lines.append("If any information you need is missing, list your "
                     "assumptions before the answer.")
        return "\n".join(lines)


spec = PromptSpec(
    task="Design test ideas for the apply_coupon function described below.",
    audience="QA engineers on an e-commerce team who will automate them in pytest",
    techniques=["equivalence partitioning", "boundary value analysis"],
    count="8 to 10 test ideas",
    output_format="a Markdown table with columns: ID, Input total, "
                  "Input code, Expected result, Technique",
    context={
        "requirement": """
            apply_coupon(total, code) returns the order total after a coupon.
            SAVE10 gives 10% off orders of $50.00 or more.
            Orders under $50.00 with SAVE10 are not discounted.
            Unknown codes raise ValueError.
        """,
    },
    constraints=["Do not test other coupon codes; only SAVE10 exists today.",
                 "Use dollar amounts with two decimal places."],
)

print(spec.build())
```

Output:

```text
Task: Design test ideas for the apply_coupon function described below.
Audience: QA engineers on an e-commerce team who will automate them in pytest
Apply these techniques: equivalence partitioning, boundary value analysis
Quantity: 8 to 10 test ideas

<requirement>
apply_coupon(total, code) returns the order total after a coupon.
SAVE10 gives 10% off orders of $50.00 or more.
Orders under $50.00 with SAVE10 are not discounted.
Unknown codes raise ValueError.
</requirement>

Constraints:
- Do not test other coupon codes; only SAVE10 exists today.
- Use dollar amounts with two decimal places.

Output format: a Markdown table with columns: ID, Input total, Input code, Expected result, Technique
If any information you need is missing, list your assumptions before the answer.
```

**Explaining the code:**

- `import textwrap` brings in a standard-library module for working with blocks of text. We use `textwrap.dedent`, which removes the common leading spaces from every line. Without it, the requirement would keep the indentation it has inside our Python source.
- `from dataclasses import dataclass, field`: a **dataclass** is a Python class whose main job is to hold data. The `@dataclass` decorator automatically writes the `__init__` method for us, so we can create a `PromptSpec` by passing named arguments.
- The lines like `task: str` declare the **fields** of the class. Each field corresponds to one dimension of specificity or one type of context from this lesson. That is the point of the design: the class *forces* you to think about task, audience, techniques, quantity and format every time.
- `context: dict = field(default_factory=dict)` declares an optional field that defaults to an empty dictionary. We use `field(default_factory=dict)` instead of `= {}` because Python dataclasses do not allow a shared mutable default; `default_factory` creates a fresh empty dict for each new object.
- `def build(self) -> str:` is a method that assembles the final prompt. It builds a list called `lines` and joins them with newline characters at the end (`"\n".join(lines)`). Building a list and joining once is a common, efficient Python pattern for constructing text.
- `", ".join(self.techniques)` turns the list `["equivalence partitioning", "boundary value analysis"]` into one string separated by commas.
- The `for name, text in self.context.items():` loop wraps **each piece of context in XML-style tags** named after its dictionary key. Adding a second block, for example `"existing_test": "..."`, automatically produces a second tagged section.
- `.strip()` removes leading and trailing blank lines from the pasted text.
- `if self.constraints:` only adds the "Constraints" section if there are any; an empty list counts as false in Python.
- The final line always asks the model to list its assumptions, the habit from Section 7.

Notice that the code does not call any AI model. It only produces text. You could paste this output into any chat assistant, or send it through an API. Keeping "build the prompt" separate from "send the prompt" makes the prompt easy to test and review.

#### 9.2 A tiny specificity linter

In Week 7 you added linting and automated checks to a CI pipeline. We can apply the same idea to prompts: a small script that checks a prompt for the dimensions of specificity and flags what is missing. It is crude (it only looks for keywords), but it builds a useful habit.

```python
import re

CHECKS = {
    "task verb": r"\b(design|write|list|generate|review|identify|create|explain)\b",
    "technique": r"boundary|equivalence|decision table|state transition|error guessing|negative",
    "quantity": r"\b\d+\b|\b(three|five|eight|ten)\b",
    "output format": r"table|json|gherkin|bullet|csv|columns",
    "audience": r"audience|for (a|the) (junior|senior|qa|developer|manager)|qa engineers",
    "context block": r"<\w+>|\"\"\"|###",
    "constraints": r"\bdo not\b|\bonly\b|\bavoid\b|\bmust\b",
}


def lint(prompt: str) -> tuple[int, list[str]]:
    text = prompt.lower()
    missing = [name for name, pattern in CHECKS.items()
               if not re.search(pattern, text)]
    score = len(CHECKS) - len(missing)
    return score, missing


vague = "Write some tests for the coupon feature."

specific = """Design 8 test ideas for apply_coupon using boundary value
analysis and equivalence partitioning. Audience: QA engineers who will
automate them in pytest.
<requirement>
SAVE10 gives 10% off orders of $50.00 or more. Unknown codes raise ValueError.
</requirement>
Only test SAVE10. Return a Markdown table with columns ID, Input, Expected, Technique."""

for label, prompt in [("vague", vague), ("specific", specific)]:
    score, missing = lint(prompt)
    print(f"{label:8} score {score}/{len(CHECKS)}  missing: {missing or 'nothing'}")
```

Output:

```text
vague    score 1/7  missing: ['technique', 'quantity', 'output format', 'audience', 'context block', 'constraints']
specific score 7/7  missing: nothing
```

**Explaining the code:**

- `import re` loads Python's **regular expression** module. A regular expression (regex) is a pattern for matching text.
- `CHECKS` is a dictionary. Each key is the name of a dimension; each value is a regex pattern that suggests the dimension is present.
  - `\b` means "word boundary", so `\bonly\b` matches the word "only" but not "commonly".
  - `|` means "or": `table|json|gherkin` matches any of those words.
  - `\d+` means "one or more digits", so it detects numbers like "8" or "10".
  - `<\w+>` matches an opening XML-style tag such as `<requirement>`; `\w+` means one or more letters, digits or underscores. `\"\"\"` matches triple quotes (the backslashes escape the quote characters inside the Python string).
- `def lint(prompt: str) -> tuple[int, list[str]]:` declares a function that returns two things: a score and a list of missing dimensions.
- `text = prompt.lower()` lowercases the prompt so "Design" and "design" both match.
- The **list comprehension** `[name for name, pattern in CHECKS.items() if not re.search(pattern, text)]` loops over every check and keeps the names whose pattern was *not* found. `re.search` returns a match object if the pattern appears anywhere, or `None` if it does not.
- `score = len(CHECKS) - len(missing)` counts how many checks passed.
- In the loop at the bottom, `f"{label:8}"` pads the label to 8 characters so the output lines up, and `missing or 'nothing'` prints `'nothing'` when the list is empty (an empty list is false in Python).

The vague prompt scores 1 out of 7: only the verb "write" is present. The specific prompt passes every check.

**Limitations to keep in mind.** A keyword linter can be fooled: a prompt that says "do not use a table" would still pass the "output format" check. A high score means the prompt *mentions* the right things, not that the prompt is good. Treat it as a reminder, the way a spell-checker reminds you without guaranteeing good writing. In this week's later lessons you will see more rigorous ways to check AI *outputs* (validation scripts are covered on Friday); this linter only checks the *input*.

---

### 10. A Reusable Specificity and Context Checklist

Before sending any prompt whose output matters, run through this list. You will not need every item every time, but you should *decide* to leave each one out rather than forget it.

**Specificity**

- [ ] Does the prompt start with a clear **task verb** (design, review, rewrite, explain, list)?
- [ ] Is the **scope** stated, including what is out of scope?
- [ ] Is there a **quantity** or range?
- [ ] Are the **test design techniques** named (BVA, EP, decision table, state transition, error guessing, negative testing)?
- [ ] Is the **audience** named?
- [ ] Is the **depth** per item clear?
- [ ] Is the **output format** stated?
- [ ] Is there a **length** limit where it matters?
- [ ] Are there **done-criteria** that define a complete answer?

**Context**

- [ ] Is the **requirement or acceptance criteria** included as the source of truth?
- [ ] Is the **tech stack with versions** stated (for example Python 3.12, pytest, Playwright for Python)?
- [ ] Is a short sample of **existing code or conventions** included where style matters?
- [ ] Are **constraints and non-goals** listed?
- [ ] Is relevant **domain** information included (currency, rounding, business rules)?
- [ ] Is all pasted material **delimited** (triple quotes or named tags)?
- [ ] Has irrelevant material been **removed** (signal over noise)?
- [ ] Are the most important instructions at the **start or end**, not buried in the middle?
- [ ] Does the prompt ask the model to **state assumptions** or **ask clarifying questions**?
- [ ] Is the prompt free of **secrets and real personal data**?

You will put this checklist to work in today's exercise, where you build a prompt library for test design and debugging as part of your Project 2 milestone.

---

## Practice Exercises

1. **Diagnose the gaps.** For each prompt below, list which dimensions of specificity and which types of context are missing.
   - a) "Write Playwright tests for login."
   - b) "Here's our search page HTML. Thoughts?"
   - c) "Give me 5 negative tests in a table."

2. **Five-step improvement.** Take the prompt "Test the cart" and improve it in at least four iterations, following Section 3. At each step, write one sentence on what you added and what you expect to change. Use this requirement: *"The cart shows the number of items and the subtotal. Quantity per item must be between 1 and 10. Setting quantity to 0 removes the item."*

3. **Context hunt.** For your Project 2 repository (or a sample project from Week 4), find and write down: the exact versions of Python, pytest and Playwright; one representative test you would paste as a style example; and two constraints your team follows that an AI tool would not know.

4. **Extend `PromptSpec`.** Add a `done_criteria: list` field and update `build()` so that it prints a "Done when:" section. Then create a spec for testing the login page with state transition testing (states: logged out, logged in, locked after 3 failed attempts).

5. **Improve the linter.** Add a `"done criteria"` check (look for phrases such as "done when", "every", "at least") and a `"tech stack"` check (look for "pytest", "playwright", "selenium", "python"). Run it on the prompts from exercise 1 and on your improved prompt from exercise 2.

6. **Assumptions drill.** Write a prompt for the cart requirement in exercise 2 that asks the model to ask up to five clarifying questions first. Then, without using any AI tool, write the five questions *you* would expect a good tester to ask. Compare them with what an AI tool returns if you have access to one.

---

## Knowledge Check

1. Using the idea of next-token prediction, explain why a vague prompt tends to produce a generic answer.
2. Name four dimensions of specificity and give a QE example of each.
3. In the five-iteration example, which single change produced the largest improvement, and why?
4. What is a "done-criterion", and why is it especially useful for test design prompts?
5. Why might pasting an entire 5,000-line log make an answer *worse* rather than better?
6. What did the *Lost in the Middle* research find, and how should it affect where you place instructions in a long prompt?
7. Give two reasons to wrap pasted material in XML-style tags.
8. You do not know whether coupon codes are case-sensitive. Name two prompt techniques that stop the model from silently guessing.
9. Why does the `PromptSpec` class use `field(default_factory=dict)` rather than `= {}`?
10. Give one way the keyword-based specificity linter can be fooled.

<details>
<summary>Answers</summary>

1. The model predicts the most probable next tokens given the prompt. With little detail, the most probable continuation is a blend of the many similar examples in its training data: the "average" answer, which fits any coupon feature rather than yours.
2. Any four, for example: task verb ("design" test ideas), quantity ("8 to 10"), techniques ("boundary value analysis"), audience ("QA engineers automating in pytest"), scope ("apply_coupon only, not payment"), format ("Markdown table"), done-criteria ("49.99, 50.00 and 50.01 all covered").
3. Adding the requirement (iteration 2). Without the test basis the model had to invent behaviour; with it, tests matched the real feature and had concrete expected results.
4. A statement of what makes the answer complete (for example "every equivalence class has at least one test"). It gives the model a target and gives the reviewer a checklist for coverage.
5. Irrelevant content dilutes the model's attention, can lead it to mix in unrelated details, wastes context-window space, and costs time and money. Key lines may also be "lost in the middle".
6. Models used relevant information best when it was near the beginning or end of a long input and worse when it was in the middle. Put long reference material first and key instructions clearly at the start or end, not buried mid-prompt.
7. Any two: the model can distinguish instructions from data; you can refer to blocks by name; instructions inside pasted text are less likely to be followed; prompts become easy to reuse with different data.
8. Ask the model to list its assumptions before answering, or ask it to ask you clarifying questions before it starts.
9. Dataclasses forbid shared mutable defaults; `default_factory=dict` creates a new empty dictionary for each `PromptSpec` object, so two specs never accidentally share the same context dictionary.
10. It only checks for keywords. For example, "do not use a table" passes the output-format check, and a prompt could contain the word "boundary" without actually asking for boundary value analysis.

</details>

---

## Glossary

- **Specificity:** How precisely a prompt states what output is wanted (task, scope, quantity, technique, audience, depth, tone, length, done-criteria).
- **Context:** The facts the model needs to complete a task well, supplied in the prompt (requirement, domain, tech stack, code, constraints, audience).
- **Test basis:** The source of truth from which tests and expected results are derived, such as a requirement or acceptance criteria.
- **Done-criteria:** Conditions that define when an answer is complete, for example "every boundary is covered".
- **Non-goal:** Something explicitly out of scope for the task.
- **Signal versus noise:** The relevant versus irrelevant parts of the context you supply.
- **Lost in the middle:** The finding that models tend to use information at the start and end of long inputs better than information in the middle.
- **Delimiter:** A marker (triple quotes, XML-style tags, headings) that separates pasted material from instructions.
- **Clarifying question:** A question the model asks you to fill a gap in context before answering.
- **Dataclass:** A Python class, created with `@dataclass`, designed mainly to hold data, with an automatically generated constructor.
- **Regular expression (regex):** A pattern language for matching text, available in Python's `re` module.
- **Linter:** A tool that automatically checks text or code for common problems.

---

## Summary

- Vague prompts produce generic answers because the model fills every gap with the most typical continuation from its training data.
- **Specificity** has distinct dimensions (task verb, scope, quantity, techniques, audience, depth, tone, length and done-criteria) that you can check one at a time.
- Improve prompts **iteratively**: change one or two things, inspect the output, repeat. In the worked example, adding the requirement gave the largest single gain.
- QE prompts need six types of **context**: product/domain, requirement and acceptance criteria, tech stack with versions, existing code and conventions, constraints and non-goals, and audience.
- More context is not always better. Aim for **high signal, low noise**, keep key instructions at the start or end, and do not bury critical rules in the middle of long pastes.
- **Delimit** pasted material with triple quotes or named XML-style tags.
- When context is missing, ask the model to **state assumptions** or **ask clarifying questions**; never let it guess silently.
- Never paste secrets or real personal data (responsible use is covered on Wednesday).
- Building prompts in code (`PromptSpec`) and checking them with a simple **linter** brings software-engineering discipline to prompt writing. All AI output still needs your review.

---

## Additional Resources

- Anthropic, *Prompting best practices* (sections "Be clear and direct", "Add context to improve performance" and "Long context prompting"): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- DAIR.AI Prompt Engineering Guide, *General Tips for Designing Prompts* (sections on specificity and avoiding impreciseness): https://www.promptingguide.ai/introduction/tips
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (the research behind Section 5.3): https://arxiv.org/abs/2307.03172
