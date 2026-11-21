# Common Prompt Failure Modes

## Learning Objectives

By the end of this lesson you will be able to:

- Treat a disappointing AI answer the way you treat a failing test: describe the **symptom**, find the **root cause**, apply a **fix** and **re-run**.
- Recognise the most common ways prompts fail in Quality Engineering work, including vague output, invented assumptions, hallucinated APIs, format drift, sycophancy and arithmetic slips.
- Explain **why** each failure happens, using what you learned on Monday about next-token prediction, training data, context windows and temperature.
- Rewrite a failing prompt so the failure becomes less likely.
- Write small, deterministic **Python checks** that catch several failure modes automatically (wrong counts, wrong expected results, invented functions, outdated Selenium calls).
- Use a **prompt-debugging checklist** and a quick-reference table during day-to-day work.

---

## Why This Matters

Earlier today you learned the principles of a good prompt, how specificity and context shape the answer, how to lock the output format and how to steer a model with examples. Those lessons describe what a good prompt looks like. This lesson covers the other side: **what goes wrong, and how to tell.**

As a quality engineer you already have the right instincts. When a test fails you do not delete it and write a new one at random. You read the error, form a hypothesis, change one thing and run again. Prompts deserve the same discipline. A prompt is a small program written in natural language; its "runtime" is a model that predicts likely text. When the output is wrong, the cause is usually something specific and fixable in the prompt, or something the model cannot do reliably, which you then have to check outside the model.

This connects directly to the Weekly Epic. By Friday you will build your first QA agent, and an agent is essentially a prompt that runs many times without you watching each answer. Every failure mode in this lesson becomes more expensive inside an agent, because nobody is there to notice that the model invented a function or returned nine test cases instead of ten. Learning to spot these failures by hand today is the foundation for the contracts (Thursday) and validation scripts (Friday) that catch them automatically later in the week.

For **Project 2**, you will use AI to help design tests and write automation code for an e-commerce web app (login, search, cart and checkout). The failure modes below are the ones you are most likely to meet while doing that work.

---

## The Concept

### 1. Debugging a Prompt Like Debugging a Test

Here is the loop you already use for a failing test:

| Step | Failing test | Failing prompt |
|------|--------------|----------------|
| **Symptom** | `AssertionError: expected 45.0, got 49.99` | "The AI said a $49.99 order gets 10% off." |
| **Root cause** | The discount condition uses `>` instead of `>=`. | The prompt never stated the $50 threshold, so the model guessed. |
| **Fix** | Change the condition. | Add the business rule to the prompt. |
| **Re-run** | Run the test again (and the suite). | Run the prompt again, **more than once**, and check the answer. |

Three habits make this loop work for prompts:

1. **Name the symptom precisely.** "The answer is bad" is not a symptom. "It returned 9 tests when I asked for 10" or "It used `find_element_by_id`, which no longer exists" is.
2. **Change one thing at a time.** If you rewrite the whole prompt, you will not know which change helped. Keep old versions (a text file or Git, from Week 1, works well) so you can compare.
3. **Re-run more than once.** Model output varies between runs (Section 3.11). One good answer after a fix proves little.

A useful mental model from Monday: an LLM does not "know" what you want. It predicts the most likely continuation of the text you gave it, based on patterns from its training data. Almost every failure in this lesson is a consequence of that one fact:

- If your prompt leaves a gap, the model fills it with whatever is **most typical** in its training data, not what is true for your project.
- If your prompt suggests an answer, the model treats that suggestion as strong evidence of what comes next.
- If the "most likely" text is wrong (an old API, a plausible-looking number), the model still produces it fluently.

Keep this in mind as you read each failure mode. For each one you will see four parts: **what it looks like**, **why it happens**, **how to fix it in the prompt** and **how to detect it**.

> All the "AI output" shown in this lesson is **illustrative**: it was written to show the typical shape of each failure, not copied from a specific model run. Real outputs vary by model, version and settings.

---

### 2. A Quick Map of the Failure Modes

Before going through them one by one, it helps to group them. Most prompt failures fall into three families:

| Family | Root cause lives in... | Failure modes in this lesson |
|--------|------------------------|------------------------------|
| **Input problems** | What you wrote (or failed to write) | Vagueness, missing context, overloaded prompts, conflicting instructions, negative-only instructions, buried instructions, leading questions |
| **Model limitations** | How LLMs work | Hallucination, outdated knowledge, non-determinism, counting and arithmetic errors, over-refusal |
| **Output problems** | The gap between what you asked for and what came back | Format drift |

Input problems are usually fixed **in the prompt**. Model limitations can be reduced by the prompt but must also be caught by **checks outside the model**, because no wording removes them completely. That second point is why this lesson includes Python code.

---

### 3. The Failure Modes in Detail

#### 3.1 Vagueness leads to generic output

**What it looks like (illustrative).**

Prompt:

```text
Write some tests for the checkout.
```

Response:

```text
1. Verify the user can complete checkout successfully.
2. Verify an error appears for invalid payment details.
3. Verify the order confirmation page is displayed.
4. Verify the cart total is correct.
```

Nothing here is wrong, but nothing is useful either. These tests could belong to any shop on the internet. They have no specific inputs, no expected values and no link to your requirements.

**Why it happens.** With so little to go on, the most probable continuation is the *average* checkout test list the model has seen in training data: blog posts, tutorials and templates. Generic input produces generic output.

**How to fix it.** Say who the tests are for, what feature, which rules, which technique and what form you want:

```text
You are helping a QA engineer test the coupon step of an e-commerce checkout.
Business rule: coupon SAVE10 gives 10% off orders of $50.00 or more.
Orders below $50.00 are unchanged. Unknown codes raise a ValueError.
Using Boundary Value Analysis, list 6 test cases as a table with columns:
ID, order total, code, expected result.
```

Today's lesson on **specificity and context** covers this in depth.

**How to detect it.** Ask yourself: "Could this answer apply unchanged to a different product?" If yes, it is too generic. Another quick signal is the absence of concrete values (no numbers, no field names, no error messages).

---

#### 3.2 Missing context leads to invented assumptions

**What it looks like (illustrative).**

Prompt:

```text
What is the expected total when SAVE10 is applied to a $49.99 order?
```

Response:

```text
SAVE10 gives 10% off, so the expected total is $44.99.
```

The model has **assumed** the coupon applies to every order. In your project it does not, because of the $50 threshold. The answer is confident, specific and wrong.

**Why it happens.** The model has never seen your requirements. The name "SAVE10" strongly suggests "save 10%", so that is the most likely continuation. The model does not stop and say "I do not know your business rules" unless you invite it to.

**How to fix it.**

1. Paste the actual rule or acceptance criterion into the prompt.
2. Give the model explicit permission to ask questions or to say when information is missing:

```text
If any rule needed to answer is not stated above, do not guess.
Instead, list the missing information as questions.
```

This "permission to say I don't know" is one of the techniques Anthropic recommends for reducing invented answers (see Additional Resources).

**How to detect it.** Look for statements in the answer that are **not traceable** to anything in your prompt or requirements. A useful habit is to ask: "Where did this fact come from?" If it came from nowhere in your input, it is an assumption.

---

#### 3.3 Hallucination: invented APIs, fixtures, requirements and flags

On Monday you met the term **hallucination**: fluent, confident output that is not true. In QE work it has some very specific and very common shapes:

| Shape | Illustrative example |
|-------|----------------------|
| Invented library function | `json.load_string(text)` (the real function is `json.loads`) |
| Invented pytest fixture | Using a fixture called `browser_session` that does not exist in your `conftest.py` |
| Invented CLI flag | `pytest --retry-failed 3` (not a built-in pytest option) |
| Invented requirement | "Coupons are case-insensitive, so `save10` should also work." Your spec never said that. |
| Invented locator | `page.get_by_test_id("checkout-btn")` when your page has no such test ID |

**Why it happens.** The model generates text that *looks like* the code and documentation it was trained on. `load_string` sounds like a reasonable name for a JSON function, so it can appear even though it does not exist. The model has no built-in step that checks a name against a real library.

**How to fix it in the prompt.**

- Provide the real material: paste your `conftest.py` fixture names, the relevant page HTML, or the library version you use.
- Restrict the model to that material: "Use only the fixtures listed above. If you need one that is not listed, say so."
- Ask the model to mark anything it is unsure about: "Mark any function you are not certain exists with `# VERIFY`."

**How to detect it.** This is where prompt wording is not enough and you need checks. The simplest check is to **run the code**. For Python names, you can also check existence directly:

```python
# api_exists_check.py - does the function the AI told us to use actually exist?
import importlib

# Illustrative AI suggestions: (module name, attribute name)
suggestions = [
    ("json", "loads"),            # real
    ("json", "load_string"),      # invented
    ("statistics", "median"),     # real
    ("statistics", "percentile"), # invented (not in the stdlib statistics module)
    ("pathlib", "Path"),          # real
]

for module_name, attr in suggestions:
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"MISSING MODULE  {module_name}")
        continue
    found = hasattr(module, attr)
    print(f"{'exists ' if found else 'INVENTED'}  {module_name}.{attr}")
```

Output:

```text
exists   json.loads
INVENTED  json.load_string
exists   statistics.median
INVENTED  statistics.percentile
exists   pathlib.Path
```

Line by line:

- `import importlib` loads the standard-library module that can import other modules **by name**, using a string.
- `suggestions` is a list of tuples. Each tuple is `(module name, attribute name)` that an AI answer told us to use.
- `importlib.import_module(module_name)` imports the module whose name is in the string, exactly like writing `import json`, but at runtime.
- The `try` / `except ModuleNotFoundError` block handles the case where the module itself was invented.
- `hasattr(module, attr)` returns `True` if the module has an attribute (function, class or constant) with that name.
- The f-string prints a label and the full dotted name.

For invented requirements there is no code check: you trace each claim back to the requirement document. Wednesday's lessons cover structured human validation of AI output, and Week 10 covers a full classification (taxonomy) of hallucination types. For today, the practical rule is: **nothing the AI names is real until you have checked it.**

---

#### 3.4 Overloaded prompts: too many tasks at once

**What it looks like (illustrative).**

```text
Review this user story for ambiguity, write 15 test cases using BVA and EP,
generate Playwright code for all of them, create test data for each one,
write a bug report for any defect you find, and summarise everything for
the product owner.
```

Typical results: some tasks are skipped, the test cases are shallow, the code covers only the first few cases, and the summary describes work that was never done.

**Why it happens.** Each part of the answer competes for attention and output length. The model produces text one token at a time, and a very long requested answer is more likely to be cut short, to lose track of earlier instructions or to blur tasks together. There is also no chance for you to correct step 1 before step 2 builds on it.

**How to fix it.** Split the work into a sequence of smaller prompts, and review the output of each before using it as input to the next:

1. Prompt A: "Review this user story for ambiguity. List questions only."
2. You answer the questions or update the story.
3. Prompt B: "Using BVA and EP, list test cases for the updated story."
4. You review and trim the list.
5. Prompt C: "Write pytest code for test cases TC1 to TC4 only."

Doing this by hand is a useful skill in itself. Linking such steps together automatically is the idea behind **agent chains**, which you will cover in Week 9.

**How to detect it.** Make a checklist of the tasks you asked for and tick each one against the answer. Missing or thin sections are the signal.

---

#### 3.5 Conflicting or contradictory instructions

**What it looks like (illustrative).**

```text
Be as detailed as possible. Keep the answer under 100 words.
Write the test cases in Gherkin. Return the result as a CSV table.
```

The model must break at least one instruction. Which one it breaks is unpredictable and can change between runs.

Contradictions are often less obvious than this. They sneak in when a prompt grows over time ("we added a line last week"), or when your instructions contradict the pasted material, for example the prompt says "the threshold is $50" while the pasted acceptance criterion still says "$40" from an older version.

**Why it happens.** The model has no rule for resolving conflicts. It weighs everything in the prompt together and produces the most likely continuation. Sometimes the instruction nearest the end wins, sometimes the most common pattern wins.

**How to fix it.**

- Read the prompt as a reviewer would read a requirement: look for words like "detailed" next to "brief", or two different output formats.
- Decide which instruction matters more and delete or rewrite the other.
- When priorities are real, state them: "If you cannot meet both the length limit and full coverage, prefer full coverage."
- Make sure the pasted material is the current version.

**How to detect it.** If an answer obeys some instructions and ignores others in a different way on each run, suspect a conflict.

---

#### 3.6 Format drift: the format you asked for is ignored

**What it looks like (illustrative).** You asked for "a JSON list of test case titles". You get:

~~~~text
Sure! Here are the test cases you requested:

```json
["Valid SAVE10 on $50 order", "SAVE10 on $49.99 order"]
```

Let me know if you'd like more!
~~~~

A human can read this easily. A Python script that calls `json.loads()` on the whole response fails, because of the friendly sentences and the Markdown code fence around the JSON.

Other forms of drift: a table with an extra column, Gherkin steps without `Given`, the format being correct in the first answer and slowly changing over a long conversation.

**Why it happens.** Chat models are trained on a great deal of friendly, conversational text, so polite framing ("Sure! Here are...") is a highly likely continuation. A format instruction is one signal among many, and a weak one if stated only once, briefly, in the middle of a long prompt.

**How to fix it.** This is the subject of today's lesson on **format locking**: stating the format exactly, showing a skeleton, saying "respond with only the JSON, no other text" and placing the instruction where it carries weight. Few-shot examples (another of today's lessons) also strongly anchor the format.

**How to detect it.** Parse the output. If `json.loads()` raises an error, or a table has the wrong number of columns, the format has drifted. Formal output contracts using JSON Schema are covered on Thursday.

---

#### 3.7 Leading questions and sycophancy

**What it looks like (illustrative).**

Prompt:

```text
I wrote this test and I'm pretty sure it's correct. Can you confirm?

def test_save10_small_order():
    assert apply_coupon(49.99, "SAVE10") == 44.99
```

Response:

```text
Yes, this test looks correct! It checks that SAVE10 applies a 10% discount
to the order total.
```

The test is wrong: a $49.99 order is below the $50 threshold and should not be discounted. The model agreed with you anyway.

**Sycophancy** is the tendency of a model to agree with the user, flatter the user or follow a wrong premise in the question. A **leading question** is one that suggests the answer you want ("confirm this is correct", "this is a bug, right?").

**Why it happens.** Models are tuned using human feedback, and people tend to rate agreeable answers more highly. In addition, your words "I'm pretty sure it's correct" become part of the context the model continues from, which raises the probability of an agreeing answer.

**How to fix it.**

- Ask neutral, open questions: "Review this test against the rule below. List any problems you find. If there are none, say 'No problems found'."
- Provide the rule, so the model has something to check against.
- Ask for criticism explicitly: "Act as a strict code reviewer. Find at least the weakest point in this test."
- Do not reveal what you expect the answer to be.

**How to detect it.** Be suspicious of answers that simply repeat your own claim back to you. A good test: ask the same question with the opposite framing ("I think this test is wrong. Can you confirm?"). If the model agrees both times, neither answer is evidence of anything.

---

#### 3.8 Negative-only instructions and the "pink elephant" effect

**What it looks like (illustrative).**

```text
Write Selenium code for the login page.
Don't use XPath. Don't use time.sleep. Don't hard-code the password.
```

The answer may still contain a `time.sleep(2)` or an XPath locator.

The name comes from the old challenge "Don't think of a pink elephant": the instruction itself puts the forbidden idea in your head.

**Why it happens.** Every word in the prompt influences the prediction. Writing "time.sleep" in the prompt, even inside "don't", makes those tokens part of the context. A "don't" instruction also tells the model what to avoid but not what to do **instead**, so the gap is filled with the most typical pattern, which may be the very thing you banned.

**How to fix it.** State what you want, positively, and keep the negative only as a short backup:

```text
Write Selenium 4 code for the login page.
Locate elements with By.ID or By.CSS_SELECTOR.
Wait for elements with WebDriverWait and expected_conditions.
Read the password from the environment variable SHOP_PASSWORD.
```

The positive version gives the model a clear target for each concern.

**How to detect it.** Search the output for the banned patterns. A simple text search or regular expression works (Section 4 shows an example).

---

#### 3.9 Instructions lost in long pasted material

**What it looks like (illustrative).** You paste a 300-line log file, then a full user story, then a long HTML page, and somewhere in the middle you write "Only report errors from the payment service." The answer reports errors from every service.

**Why it happens.** Research on long inputs (the "Lost in the Middle" paper in Additional Resources) found that models tend to use information at the **beginning** and **end** of a long input more reliably than information buried in the **middle**. An instruction surrounded by hundreds of lines of pasted text can effectively be lost.

**How to fix it (practical tips).**

- Put the task instructions at the **start**, and repeat the key instruction at the **end**, after the pasted material.
- Clearly separate pasted material from instructions with delimiters, for example:

```text
Task: list errors from the payment service only.

<log>
... 300 lines ...
</log>

Reminder: report only errors from the payment service.
```

- Paste only what is needed. Trim the log to the relevant time window rather than including everything.

How models behave at the limits of their context window, and how to test that behaviour, is covered in Week 10. For today, the habit is: **short inputs, instructions at the edges, clear delimiters.**

**How to detect it.** Check whether every instruction you gave is visible in the answer. If the instruction you placed in the middle is the one that was ignored, this is the likely cause.

---

#### 3.10 Outdated knowledge

**What it looks like (illustrative).**

```python
driver.find_element_by_id("username").send_keys("alice")
```

You learned in Week 6 that Selenium 4 uses `driver.find_element(By.ID, "username")`. The older `find_element_by_*` helper methods were deprecated in Selenium 4 and later removed from the Python bindings, so this line raises an `AttributeError` with a current Selenium version.

**Why it happens.** A model is trained on data up to a cutoff date, and the internet contains years of tutorials using older APIs. Old patterns may simply be **more common** in the training data than new ones, so they are more likely to be predicted, even by a model trained after the change.

**How to fix it.**

- State versions explicitly: "Use Selenium 4 with Python 3.12" or "Use pytest 8 and Playwright for Python".
- Paste a small example of the current style from your own codebase. The model will tend to copy it.
- For anything that changed recently, check the official documentation rather than trusting the model.

**How to detect it.** Run the code against your pinned versions. For known deprecated patterns, a regular expression scan is quick (Section 4). Also look for warnings such as `DeprecationWarning` when you run tests.

---

#### 3.11 Non-determinism: the same prompt, different answers

On Monday you learned that an LLM picks each next token by **sampling** from a probability distribution, and that **temperature** controls how adventurous that sampling is. A consequence is that the same prompt can produce different answers on different runs.

To see why one good run proves little, here is a small **simulation**. It is not a real LLM. It pretends the model has three possible answers to one question, with fixed probabilities, and samples from them the way an LLM samples tokens:

```python
# nondeterminism_sim.py - a SIMULATION of sampling, not a real LLM
import random

# Pretend next-"answer" probabilities for the prompt
# "Is a $49.99 order eligible for SAVE10?"
answers = ["No - the minimum is $50.", "Yes, 10% off applies.", "It depends on the cart."]
weights = [0.70, 0.20, 0.10]

def fake_llm(prompt: str, temperature: float, rng: random.Random) -> str:
    """Stand-in for an LLM. temperature 0 -> always the most likely answer."""
    if temperature == 0:
        return answers[weights.index(max(weights))]
    return rng.choices(answers, weights=weights, k=1)[0]

prompt = "Is a $49.99 order eligible for SAVE10?"
rng = random.Random(42)          # fixed seed so this demo prints the same every run

print("temperature=0:")
for run in range(1, 4):
    print(f"  run {run}: {fake_llm(prompt, 0, rng)}")

print("temperature=1, 10 runs:")
results = [fake_llm(prompt, 1, rng) for _ in range(10)]
for answer in answers:
    print(f"  {results.count(answer):>2} x {answer}")
```

Output:

```text
temperature=0:
  run 1: No - the minimum is $50.
  run 2: No - the minimum is $50.
  run 3: No - the minimum is $50.
temperature=1, 10 runs:
   8 x No - the minimum is $50.
   2 x Yes, 10% off applies.
   0 x It depends on the cart.
```

Line by line:

- `answers` and `weights` stand in for the model's probability distribution. The correct answer is the most likely (70%), but the wrong answer still has a 20% chance.
- `fake_llm` imitates two settings. At `temperature == 0` it always returns the most likely answer (`max(weights)` finds the highest weight, `weights.index(...)` finds its position). Otherwise it samples using `rng.choices(..., weights=weights, k=1)`, which picks one item with the given probabilities.
- `random.Random(42)` creates a random number generator with a fixed **seed**, so this demonstration prints the same output every time you run it. A real hosted model does not let you fix the randomness this precisely.
- The list comprehension `[fake_llm(...) for _ in range(10)]` runs the "model" ten times.
- `results.count(answer)` counts how many times each answer appeared; `:>2` right-aligns the number in two characters.

What this shows:

- At temperature 1, the wrong answer appeared **2 times out of 10**. If you happened to look only at one of the eight good runs, you would conclude the prompt works. In a test suite or an agent that runs hundreds of times, a 20% error rate is a serious defect.
- Lower temperature makes output more consistent. But note that consistency is not correctness: at temperature 0 the model always gives the *most likely* answer, and the most likely answer can still be wrong if the prompt lacks context. Also, in practice even low-temperature settings on real services can show small variations between runs.

**How to fix it.**

- For QE tasks that need repeatable, factual output (expected results, code), use a low temperature where your tool allows it.
- Improve the prompt so the correct answer becomes much more likely (context, examples, format).
- Never treat AI-generated expected results as truth. Compare them with the real rule or the real code.

**How to detect it.** Run important prompts **several times** (three to five is a reasonable start) and compare the answers. Disagreement between runs is a strong signal that the prompt is under-specified or that the task is at the edge of what the model does reliably. Measuring this kind of variation systematically is part of LLM evaluation, covered in Week 10.

---

#### 3.12 Counting and arithmetic errors

**What it looks like (illustrative).**

- "Generate exactly 10 test cases" returns 9 or 11.
- An expected-results table says `75.50 * 0.9 = 67.50` (the correct value is `67.95`).
- "Each test title must be under 60 characters" is ignored for a few titles.

**Why it happens.** On Monday you learned that models work on **tokens**, not characters or numbers. The model does not count items in a list or carry digits the way a calculator does; it predicts text that looks like a count or a sum. For short, common calculations it is often right; for anything else it can make small, plausible errors. Long lists make counting errors more likely.

**How to fix it.**

- Ask the model to **number** the items (TC1, TC2, ...). Numbering makes counting part of the text it generates, and it makes your own check quick.
- Give the formula and ask the model to show the working: "expected = total x 0.9, rounded to 2 decimals; show the calculation."
- Better still, do not ask the model for the arithmetic at all. Ask it for the **inputs** (the interesting order totals) and compute expected values with your real code or a trusted calculation.

**How to detect it.** Count and calculate in code. These checks are cheap and deterministic, and Section 4 shows both.

---

#### 3.13 Over-refusal and over-caution

**What it looks like (illustrative).** You ask for "a list of SQL injection strings to test the search box of our own test environment", and the model refuses or answers only with general advice. Or every answer arrives wrapped in long warnings.

**Why it happens.** Models are trained to avoid harmful content. Requests that resemble harmful ones on the surface ("injection", "attack", "password") can trigger caution even when the purpose is legitimate testing.

**How to fix it.** Give the legitimate context plainly: you are a QA engineer, the system is your team's own test environment, and the goal is to verify input validation. Ask for what you need in testing terms ("negative test inputs for input validation"). If the tool still declines, use established, documented test resources for that area rather than trying to trick the model. Your organisation's AI usage policy also applies; responsible use is covered on Wednesday.

**How to detect it.** Easy: the answer says it cannot help, or it is mostly warnings with little content.

---

#### 3.14 Untrusted text inside the prompt

When you paste text you did not write (a user review, a web page, a bug report from an external user), instructions hidden inside that text can change how the model behaves; this risk is named on Wednesday in the lesson on responsible use and is studied in depth as **prompt injection** in Week 10.

---

### 4. Catching Failures with Small Python Checks

Some failure modes (vagueness, sycophancy) need your judgement. Others can be caught by simple, deterministic code. "Deterministic" means the check gives the same result every time for the same input, which is exactly what the model does not guarantee. You already wrote checks like these in Week 4 and Week 7: they are ordinary assertions applied to AI output instead of application output.

All AI outputs below are illustrative, hard-coded strings, so you can run the scripts without any API key.

#### 4.1 Count check

```python
# count_check.py - did the AI give us exactly what we asked for?
import json

# Illustrative AI output: we asked for "exactly 10 test case titles as a JSON list".
ai_output = """[
  "Valid SAVE10 on $50 order",
  "Valid SAVE10 on $100 order",
  "SAVE10 on $49.99 order",
  "Unknown code raises ValueError",
  "Empty code string",
  "Lowercase save10",
  "Code with trailing space",
  "Zero total",
  "Negative total"
]"""

REQUESTED = 10

titles = json.loads(ai_output)          # turn the JSON text into a Python list
print(f"Requested: {REQUESTED}, received: {len(titles)}")

duplicates = {t for t in titles if titles.count(t) > 1}
print("Duplicates:", sorted(duplicates) if duplicates else "none")

if len(titles) != REQUESTED:
    print("FAIL: count mismatch - do not trust 'exactly N' without checking")
```

Output:

```text
Requested: 10, received: 9
Duplicates: none
FAIL: count mismatch - do not trust 'exactly N' without checking
```

Line by line:

- The triple-quoted string `ai_output` holds the AI's answer as text, just as you would receive it.
- `json.loads(ai_output)` converts JSON text into a Python list. If the format had drifted (Section 3.6), this line would raise `json.JSONDecodeError`, which is itself a useful detection.
- `len(titles)` counts the items. Nine, not ten.
- The set comprehension `{t for t in titles if titles.count(t) > 1}` collects any title that appears more than once. Duplicates are a common way for a model to "reach" a requested count.
- The final `if` reports the mismatch.

#### 4.2 Expected-result check against the real code

The most valuable check in QE: never accept an AI-calculated expected result without comparing it to the source of truth.

```python
# math_check.py - compare the AI's expected results with the real code
def apply_coupon(total: float, code: str) -> float:
    """Project 2 running example: SAVE10 = 10% off orders of $50 or more."""
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon code: {code}")
    if total >= 50:
        return round(total * 0.9, 2)
    return total

# Illustrative AI-suggested test table: (total, code, expected_total)
ai_table = [
    (50.00, "SAVE10", 45.00),
    (100.00, "SAVE10", 90.00),
    (49.99, "SAVE10", 44.99),   # AI applied the discount below the threshold
    (75.50, "SAVE10", 67.50),   # AI arithmetic slip: 75.50 * 0.9 = 67.95
]

for total, code, expected in ai_table:
    actual = apply_coupon(total, code)
    status = "OK  " if actual == expected else "DIFF"
    print(f"{status} total={total:>6} AI expected={expected:>6} real={actual:>6}")
```

Output:

```text
OK   total=  50.0 AI expected=  45.0 real=  45.0
OK   total= 100.0 AI expected=  90.0 real=  90.0
DIFF total= 49.99 AI expected= 44.99 real= 49.99
DIFF total=  75.5 AI expected=  67.5 real= 67.95
```

Line by line:

- `apply_coupon` is the running example function. In a real project you would import it from the application code instead of redefining it.
- `ai_table` is a list of tuples suggested by the AI. Two rows contain the errors from Sections 3.2 and 3.12.
- The `for` loop **unpacks** each tuple into `total`, `code` and `expected`.
- `apply_coupon(total, code)` computes the real answer.
- The conditional expression `"OK  " if actual == expected else "DIFF"` labels each row.
- `:>6` in the f-string right-aligns each number in six characters, making the table easy to read. Note that Python prints `50.00` as `50.0`; the value is the same.

Notice what each `DIFF` tells you. Row 3 is a **missing-context** failure (the model did not know the threshold). Row 4 is an **arithmetic** failure. Different root causes, different fixes, same detection technique.

> A caution: when the AI output and your code disagree, either one could be wrong. Here the code matches the written requirement, so the AI is wrong. If the code did *not* match the requirement, you would have found a real defect in the application. Always compare against the **requirement**, not just against whichever side you trust more.

#### 4.3 Existence check for suggested functions

Section 3.3 showed `api_exists_check.py`, which uses `importlib` and `hasattr` to confirm that a suggested module attribute exists. You can apply the same idea to your own project modules (for example, checking that a page-object method the AI used really exists on your class) as long as the module can be imported.

#### 4.4 Outdated API scan

```python
# deprecated_check.py - flag outdated Selenium calls in AI-generated code
import re

ai_code = '''
driver.get("https://shop.example.com/login")
driver.find_element_by_id("username").send_keys("alice")
driver.find_element(By.ID, "password").send_keys("secret")
driver.find_elements_by_css_selector(".cart-item")
'''

# Selenium 4 removed the find_element(s)_by_* helper methods.
DEPRECATED = re.compile(r"\bfind_elements?_by_\w+")

for line_no, line in enumerate(ai_code.strip().splitlines(), start=1):
    match = DEPRECATED.search(line)
    if match:
        print(f"line {line_no}: outdated API '{match.group()}' -> use find_element(By..., ...)")
```

Output:

```text
line 2: outdated API 'find_element_by_id' -> use find_element(By..., ...)
line 4: outdated API 'find_elements_by_css_selector' -> use find_element(By..., ...)
```

Line by line:

- `import re` loads Python's regular expression module.
- `ai_code` holds a short, illustrative piece of AI-generated Selenium code.
- The pattern `r"\bfind_elements?_by_\w+"` means: a word boundary (`\b`), the text `find_element`, an optional `s` (`s?`), then `_by_`, then one or more word characters (`\w+`). It matches both `find_element_by_id` and `find_elements_by_css_selector`, but not the modern `find_element(By.ID, ...)`.
- `re.compile` prepares the pattern once so it can be reused.
- `ai_code.strip().splitlines()` removes the blank first and last lines and splits the text into a list of lines.
- `enumerate(..., start=1)` gives each line a number starting at 1, which matches how editors number lines.
- `DEPRECATED.search(line)` finds the first match in the line, or returns `None`. `match.group()` returns the matched text.

The same technique catches "pink elephant" leaks from Section 3.8: scan for `time.sleep`, `//` XPath expressions or hard-coded passwords.

#### 4.5 Why these checks matter beyond today

Each script above is a tiny, hand-written version of an idea you will develop properly later this week. On Thursday you will describe the expected shape of AI output formally, and on Friday you will build validation scripts that run checks like these automatically against an agent's output. Today, the point is the mindset: **if a failure can be detected by code, detect it by code.** Your eyes are better spent on the failures that code cannot see.

---

### 5. Putting It Together: Debugging One Prompt Step by Step

Here is the full loop applied to one realistic case.

**Version 1 (illustrative):**

```text
Is this test right?

def test_save10_small_order():
    assert apply_coupon(49.99, "SAVE10") == 44.99
```

- **Symptom:** The model says "Yes, this looks correct."
- **Root causes:** Leading question (3.7) and missing context (3.2): the threshold is not stated.

**Version 2:**

```text
Business rule: SAVE10 gives 10% off orders of $50.00 or more.
Orders below $50.00 are unchanged. Unknown codes raise ValueError.

Review the test below against this rule. List any problems.
If there are none, reply exactly: No problems found.

def test_save10_small_order():
    assert apply_coupon(49.99, "SAVE10") == 44.99
```

- **Symptom:** The model now points out that $49.99 is below the threshold and the expected value should be 49.99. Good, but it also suggests the coupon "should be case-insensitive".
- **Root cause:** Hallucinated requirement (3.3).

**Version 3:** add one line:

```text
Judge only against the rule stated above. Do not add new rules.
If you think a rule is missing, list it separately under "Questions".
```

- **Re-run several times (3.11).** The problem is reported consistently; the case-sensitivity idea now appears, when it appears at all, as a question for the product owner rather than as a fact. That is the right outcome: it is a valid question to raise, but not the model's decision.
- **Detect (Section 4):** independently, `math_check.py` confirms the expected value for $49.99 is 49.99.

Each version changed one thing in response to one observed symptom. That is debugging.

---

### 6. Prompt-Debugging Checklist

Use this list when an AI answer disappoints you. Work from top to bottom; the early items are the most common causes.

1. **Symptom:** Can I describe exactly what is wrong, in one sentence?
2. **Specificity:** Did I state the feature, the goal, the technique and the expected form of the answer?
3. **Context:** Did I include the actual requirement, rule, code or versions the answer depends on?
4. **Permission to not know:** Did I tell the model to ask or flag missing information instead of guessing?
5. **One task:** Is this prompt asking for one job, or several? Should I split it?
6. **Conflicts:** Do any two instructions contradict each other, or contradict the pasted material?
7. **Positive phrasing:** Did I say what to do, not only what to avoid?
8. **Placement:** Are key instructions at the start (and repeated at the end) of long prompts, with pasted material clearly delimited?
9. **Neutral wording:** Did I avoid suggesting the answer I expect?
10. **Format:** Did I specify the output format exactly, ideally with a skeleton or example?
11. **Versions:** Did I name the library and language versions?
12. **Repeatability:** Did I run the prompt more than once and compare?
13. **Checks:** Which parts of the answer can I verify with code (counts, calculations, names, patterns), and have I done so?
14. **Change one thing:** After this fix, will I know whether it helped?

---

### 7. Quick-Reference Table

| # | Failure mode | Typical symptom in QE | Root cause | Prompt fix | Detection |
|---|--------------|------------------------|-----------|------------|-----------|
| 1 | Vagueness | Generic tests with no values | Model fills gaps with the "average" answer | Name feature, rule, technique, format | "Would this fit any product?" |
| 2 | Missing context | Confident wrong expected result | Model assumes typical behaviour | Paste the rule; allow "I don't know" | Trace every claim to your input |
| 3 | Hallucination | Invented function, fixture, flag, requirement | Predicts plausible-looking text | Provide real material; restrict to it; mark uncertain items | Run code; `hasattr`/`importlib`; trace to spec |
| 4 | Overloaded prompt | Skipped or shallow tasks | Attention and length spread thin | Split into reviewed steps | Tick each requested task |
| 5 | Conflicting instructions | Different rule broken each run | No conflict-resolution rule | Remove conflict; state priority | Inconsistent obedience across runs |
| 6 | Format drift | Extra prose, code fences, wrong columns | Conversational style is highly likely | Exact format, skeleton, "only" (format locking) | Parse it (`json.loads`, column count) |
| 7 | Sycophancy | "Yes, looks correct!" to a wrong test | Tuned toward agreeable answers; premise in context | Neutral question, provide rule, ask for critique | Flip the framing and compare |
| 8 | Negative-only instructions | Banned pattern still appears | Mentioned tokens raise probability; no alternative given | State the desired alternative | Search output for banned patterns |
| 9 | Buried instructions | Middle instruction ignored | Middle of long input used less reliably | Instructions at start and end; delimiters; trim input | Check each instruction is reflected |
| 10 | Outdated knowledge | `find_element_by_id` | Old patterns common in training data | Name versions; show current-style example | Run on pinned versions; regex scan |
| 11 | Non-determinism | Correct today, wrong tomorrow | Sampling; temperature | Lower temperature; stronger prompt | Run several times; compare |
| 12 | Counting/arithmetic | 9 of 10 tests; 75.50 x 0.9 = 67.50 | Tokens, not numbers | Number items; give formula; compute yourself | `len()`; compare to real code |
| 13 | Over-refusal | Declines legitimate test request | Surface similarity to harmful requests | State legitimate testing context | Answer is refusal or warnings |
| 14 | Untrusted text in prompt | Behaviour changes after pasting external text | Covered Wednesday and Week 10 | Covered Wednesday and Week 10 | Covered Wednesday and Week 10 |

---

## Practice Exercises

1. **Diagnose the prompt.** For each prompt below, name the most likely failure mode(s) and rewrite it.
   - a) "Write tests for search."
   - b) "This login test is correct, isn't it? `assert login('alice', '') is True`"
   - c) "Give me a detailed explanation in one sentence of how to test the cart, as a Gherkin feature and as a CSV."
   - d) "Write Playwright code for checkout. Don't use waits. Don't use CSS selectors."

2. **Extend the count check.** Modify `count_check.py` so it also fails if any title is longer than 60 characters, and prints the offending titles.

3. **Extend the math check.** Add three rows to `ai_table` in `math_check.py`: `(50.01, "SAVE10", 45.01)`, `(0.00, "SAVE10", 0.00)` and `(60.00, "save10", 54.00)`. Predict the output of each row before running it. Which row raises an exception, and why? How would you change the loop to report exceptions instead of crashing (hint: `try` / `except ValueError`)?

4. **Pink-elephant scanner.** Write `banned_patterns_check.py` that scans a string of AI-generated code for `time.sleep(`, XPath strings starting with `//` and any line containing `password = "`. Test it on a short, made-up snippet that contains all three.

5. **Flip the framing.** Take a small piece of your own Week 4 pytest code. In your AI tool, ask once "Confirm this test is correct" and once "Find problems in this test". Compare the answers and write two sentences on what you observed.

6. **Repeatability experiment.** Pick one prompt from your Project 2 work (for example, "list boundary values for the checkout quantity field, 1 to 99"). Run it five times in your AI tool. Record how many answers were identical and how many differed. Then improve the prompt using the checklist and repeat.

---

## Knowledge Check

1. Describe the four-step loop for debugging a prompt and relate each step to debugging a failing test.
2. Why does a vague prompt tend to produce generic output? Use the idea of next-token prediction in your answer.
3. An AI tells you to use `pytest --retry-failed 3`. Which failure mode is this, and how would you check it?
4. What is sycophancy, and give one prompt change that reduces it.
5. Why can "Don't use `time.sleep`" lead to code that uses `time.sleep`? What is the better instruction?
6. Where in a long prompt should the key instructions go, and why?
7. A prompt gave the correct answer the one time you ran it. Why is that weak evidence that the prompt is reliable?
8. You need expected totals for ten coupon test cases. Why is it better to ask the AI for the *inputs* and calculate the expected values yourself?
9. Which failure modes in this lesson can be detected reliably by code, and which mainly need human judgement? Give two of each.
10. In `math_check.py`, the AI and the code disagree on a row. Why must you check the requirement before deciding which one is wrong?

<details>
<summary>Answers</summary>

1. Symptom (describe precisely what is wrong, like reading the assertion error), root cause (find what in the prompt or model behaviour caused it, like finding the bug in the code), fix (change one thing in the prompt, like fixing one line), re-run (run the prompt again, several times, like re-running the test and the suite).
2. The model predicts the most likely continuation of the text it is given. With few details, the most likely continuation is the average, typical answer from its training data, which is generic rather than specific to your product.
3. Hallucination (an invented CLI flag). Check the pytest documentation or run `pytest --help`; better still, try the command and see whether pytest reports an unrecognised argument.
4. Sycophancy is the model's tendency to agree with the user or follow a wrong premise. Ask a neutral question ("Review this test against the rule below and list any problems") instead of "Confirm this is correct", and include the rule to check against.
5. The words `time.sleep` become part of the context and raise the probability of those tokens, and the instruction gives no alternative, so the model may fill the gap with the common pattern. Better: "Wait for elements using WebDriverWait with expected_conditions."
6. At the start, and repeated at the end, with pasted material clearly delimited in between. Models tend to use information at the beginning and end of a long input more reliably than information in the middle.
7. Output is sampled, so the same prompt can produce different answers. A wrong answer with, say, a 20% probability will often not appear in a single run. Run important prompts several times and compare.
8. Models work on tokens and can make plausible arithmetic slips. Your own code or calculation is deterministic and trustworthy; the AI's value is in suggesting interesting inputs (boundaries, edge cases).
9. Code: counts, arithmetic/expected values, existence of functions, deprecated patterns, format (parsing). Human judgement: vagueness/genericness, sycophancy, invented requirements, overloaded or conflicting prompts.
10. Either side could be wrong. If the code does not match the requirement, you have found a real application defect, not an AI error. The requirement is the source of truth.

</details>

---

## Glossary

- **Failure mode:** A recurring way in which something goes wrong, with a typical symptom and cause.
- **Symptom:** The observable sign of a problem (for example, nine tests returned instead of ten).
- **Root cause:** The underlying reason a problem happens (for example, the model cannot count reliably).
- **Hallucination:** Fluent, confident output that is not true, such as an invented function or requirement (introduced Monday; detailed taxonomy in Week 10).
- **Sycophancy:** A model's tendency to agree with the user or accept a wrong premise.
- **Leading question:** A question that suggests the answer the asker expects.
- **Pink-elephant effect:** Mentioning something in a "don't" instruction makes it more likely to appear.
- **Format drift:** Output that departs from the requested format (extra prose, code fences, wrong structure).
- **Lost in the middle:** The tendency of models to use information in the middle of a long input less reliably than at the beginning or end.
- **Non-determinism:** Getting different outputs from the same input on different runs.
- **Seed:** A starting value for a random number generator; the same seed produces the same sequence of "random" numbers.
- **Deterministic check:** A check that always gives the same result for the same input, such as counting list items in code.
- **Over-refusal:** A model declining a legitimate request because it superficially resembles a harmful one.

---

## Summary

- Debug prompts the way you debug tests: **symptom, root cause, fix, re-run**, changing one thing at a time and keeping old versions.
- Most failures follow from one fact: the model **predicts likely text**. Gaps get filled with typical content, suggestions get treated as evidence and plausible-but-wrong text comes out fluently.
- **Input problems** (vagueness, missing context, overloading, conflicts, negative-only wording, buried instructions, leading questions) are fixed mainly in the prompt.
- **Model limitations** (hallucination, outdated knowledge, non-determinism, counting and arithmetic, over-refusal) can be reduced by the prompt but must be **caught by checks**.
- Simple Python checks (counts, expected values against real code, `importlib`/`hasattr` existence checks, regex scans for outdated APIs) catch many failures cheaply and deterministically.
- **Run important prompts more than once.** One good answer proves little.
- These habits prepare you for Thursday's formal contracts and Friday's validation scripts, where the same checks become automatic parts of a QA agent.

---

## Additional Resources

- Anthropic, *Reduce hallucinations* (Claude Platform Docs): practical techniques such as allowing the model to say "I don't know", grounding answers in quotes and requiring citations: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (arXiv): the research behind placing key instructions at the start and end of long prompts: https://arxiv.org/abs/2307.03172
- Selenium blog, *Locate your locators - Python bindings changes upcoming*: the official notice that `find_element_by_*` methods were being removed, a classic source of outdated AI-generated code: https://www.selenium.dev/blog/2022/python-locators-se4/
