# Week 08 · Lecture 02: How AI Handles Language

**Topics:**

1. [NLP Fundamentals](#topic-1)
2. [Generative AI Concepts](#topic-2)
3. [Generative AI Applications within QE](#topic-3)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Open your AI assistant: **ChatGPT, Copilot Chat or Claude**. Copilot users in VS Code: use the **chat panel**.
> 2. Have pen and paper (or a blank text file) ready.
> 3. Check that Python and pytest work. You'll need them for Topic 3, and you've used pytest in earlier weeks:
>    ```bash
>    python -m pytest --version
>    ```
>    If pytest is missing: `python -m pip install pytest`
> 4. Create a folder for this week's work, for example `week08`, and open it in your editor.
>
> **Optional:** to run the demo script in Topic 1 yourself, install scikit-learn: `python -m pip install scikit-learn`.

---

## How to Use This Handout

Same layout as Lecture 01: **Definition → Key ideas → Worked example (step by step) → Checkpoint → Your turn → Common problems.** Most activities use your AI assistant plus your own judgement. Topic 2 has a short script you can run without installing anything, and Topic 3 uses pytest.

> **About AI answers:** ChatGPT, Copilot and Claude each answer differently, and **even the same tool gives a different answer each time you ask**. Mark your AI's answer with the checklist, not by matching words. If your tool isn't working, use the **sample AI answer** in the checkpoint.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Explain why computers must turn **text into numbers**, and why simple **word matching** misses things that **meaning-based** AI catches.
- Explain, in plain words, how an AI assistant generates text: **one token at a time, by prediction**.
- Explain what the **context window** and **temperature** are, and why AI can be **confidently wrong** (hallucination).
- Review AI-generated tests against a requirement and fix them, and explain why **every AI output needs a human reviewer**.

---

<a id="topic-1"></a>

# Topic 1: NLP Fundamentals

## Definition

**Natural Language Processing (NLP)** is the part of AI that helps computers work with **human language**: reading it, sorting it, comparing it and generating it. Computers only understand numbers, so every NLP system first **cleans** the text and then **turns it into numbers**. Older, simpler methods compare **which words** two texts share. Modern AI turns text into numbers that capture **meaning**, so "voucher" and "coupon" end up close together even though they're different words. NLP is the bridge between Lecture 01's machine learning and the AI assistants you'll use all week.

## Key Ideas

1. **Language is hard for computers.** People say the same thing in many ways ("checkout does nothing" / "clicking CHECKOUT doesn't work!"), and the same word can mean different things ("the test *passed*" / "the user *passed* a bad value").
2. **Step one is always cleaning:** lowercase everything, remove IDs and punctuation, split into words (**tokens**), and drop small common words like "the" and "is" (**stop words**).
3. **Word matching:** turn each text into numbers based on its **words**. Distinctive words like "safari" or "coupon" count more than common ones. Texts that share important words score as similar.
4. **Meaning matching:** modern AI uses **embeddings**, numbers that capture **meaning**. That's how an AI assistant can tell that "discount voucher" and "coupon" are about the same thing.

## Worked Example: Is This New Bug a Duplicate?

**The problem:** a tester is about to log a new bug. Is it a **duplicate** of one already reported?

```text
BUG-101: Checkout button does nothing on Safari after applying a coupon
BUG-102: Login page shows a blank screen on slow 3G network
BUG-103: Product images fail to load on the search results page
BUG-104: Cart total is wrong when two coupons are applied

NEW BUG: Safari: clicking CHECKOUT does nothing once a coupon code is applied!
```

### Step 1: Clean the text by hand

Do what an NLP system does first. For the **new bug**, write down its important words: lowercase, no punctuation, no stop words ("a", "is", "once", "does" and so on).

**What to notice:** you should end up with something like `safari, clicking, checkout, nothing, coupon, code, applied`. The "CHECKOUT" vs. "checkout" difference has gone, which is the point of cleaning.

### Step 2: Match words by hand

For each existing bug, count how many of the new bug's important words it **also** contains (same spelling, after lowercasing):

| Bug | Shared important words | Count |
|---|---|---|
| BUG-101 | ? | ? |
| BUG-102 | ? | ? |
| BUG-103 | ? | ? |
| BUG-104 | ? | ? |

The bug with the most shared words is the **likely duplicate**. This is how simple NLP sees text: as **words**, not meaning.

### Step 3: Let the computer do it (demo)

This script does Steps 1 and 2 automatically. To try it, save it as `duplicate_finder.py` and run `python duplicate_finder.py` (it needs scikit-learn: see Before Class). You don't need to understand every line.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

bugs = {
    "BUG-101": "Checkout button does nothing on Safari after applying a coupon",
    "BUG-102": "Login page shows a blank screen on slow 3G network",
    "BUG-103": "Product images fail to load on the search results page",
    "BUG-104": "Cart total is wrong when two coupons are applied",
}
new_bug = "Safari: clicking CHECKOUT does nothing once a coupon code is applied!"

vectors = TfidfVectorizer(stop_words="english").fit_transform(list(bugs.values()) + [new_bug])
scores = cosine_similarity(vectors[-1], vectors[:-1])[0]          # new bug vs each old one
for bug_id, score in sorted(zip(bugs, scores), key=lambda p: p[1], reverse=True):
    print(f"{score:.2f}  {bug_id}  {bugs[bug_id]}")
```

**What to look for (not every line):**

- `TfidfVectorizer` cleans the text (lowercase, stop words) and turns each bug into a list of numbers, giving **distinctive** words higher values.
- `cosine_similarity` scores each pair from **0** (nothing in common) to **1** (identical).
- The output lists the most similar bug first:

```text
0.53  BUG-101  Checkout button does nothing on Safari after applying a coupon
0.13  BUG-104  Cart total is wrong when two coupons are applied
0.00  BUG-102  Login page shows a blank screen on slow 3G network
0.00  BUG-103  Product images fail to load on the search results page
```

It agrees with your hand count: BUG-101 shares the most words, and BUG-104 shares a little.

### Step 4: Find the blind spot

A different tester writes the new bug like this:

```text
NEW BUG: Discount voucher makes the basket price incorrect
```

A human can see it's the **same problem as BUG-104** (wrong cart total with coupons). Repeat Step 2 by hand: how many important words does it share with BUG-104?

If you put this wording into `new_bug` in the demo script and run it again, **every score is 0.00**. Word matching can't see that "voucher" means "coupon", "basket" means "cart" and "price" means "total".

### Step 5: Ask an AI that understands meaning

Paste into a **new chat**:

```text
Here are 4 existing bug reports:
BUG-101: Checkout button does nothing on Safari after applying a coupon
BUG-102: Login page shows a blank screen on slow 3G network
BUG-103: Product images fail to load on the search results page
BUG-104: Cart total is wrong when two coupons are applied

New bug: "Discount voucher makes the basket price incorrect"

Is the new bug a likely duplicate of any existing bug?
Answer with the bug ID (or "none") and a one-line reason.
```

**What this does:** your AI assistant compares **meaning**, not just spelling, so it should spot the link that word matching missed.

### Consolidated Prompt

Add it to `prompts.txt`, with its data:

```text
=== Duplicate check - v1 ===
Use: check whether a new bug duplicates an existing one (by meaning, not just words).
Source: Handout 02, Topic 1

--- Prompt (new chat) ---
Here are 4 existing bug reports:
BUG-101: Checkout button does nothing on Safari after applying a coupon
BUG-102: Login page shows a blank screen on slow 3G network
BUG-103: Product images fail to load on the search results page
BUG-104: Cart total is wrong when two coupons are applied

New bug: "Discount voucher makes the basket price incorrect"

Is the new bug a likely duplicate of any existing bug?
Answer with the bug ID (or "none") and a one-line reason.
```

To use it for a real bug later, replace the bug list and the new bug text.

## Checkpoint

**Answer key:**

| Step | Answer |
|---|---|
| Step 2: BUG-101 | **4**: safari, checkout, nothing, coupon |
| Step 2: BUG-104 | **1**: applied ("coupons" ≠ "coupon" when matching exact words) |
| Step 2: BUG-102, BUG-103 | **0** |
| Step 4: "voucher" bug vs. BUG-104 | **0** shared words, so word matching misses it |
| Step 5: the AI's answer | **BUG-104** |

**Mark your AI's answer:**

- ✅ It picked **BUG-104**
- ✅ Its reason links the **meanings** (voucher ≈ coupon, basket ≈ cart, price ≈ total)
- ✅ It gave one ID and one line, as asked

**Sample AI answer:** *BUG-104: both describe an incorrect cart/basket total when a coupon/voucher discount is used.*

## Your Turn

1. **(In class, 3 min)** Do Step 2 by hand for this new bug: `"Wrong total in cart when 2 coupons are used"`. Which existing bug wins? Then ask your AI the same question. Do you agree?
2. **(After class)** Ask your AI: *"Explain the difference between keyword matching and embeddings for finding duplicate bug reports, for a beginner, in 4 sentences."*
3. **(After class)** Word matching is fast, cheap and always gives the same answer; AI understands meaning but varies and costs more. For a team with 50,000 old bug reports, which would you run **first**, and when would you use the other?
4. **(After class)** Write a new bug that a human would say is **not** a duplicate of anything, but that **shares words** with BUG-103 (for example about "images" or "search"). Would word matching give a false alarm?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Your hand count differs from the key | Different choices about stop words or word forms ("applied" vs. "applying") | That's fine. Simple NLP treats different word forms as different words too |
| The AI says "none" for the voucher bug | It was too cautious, or you pasted the wrong bug text | Re-check the paste; ask "Could it be related to BUG-104?" and see how it reasons |
| The AI picks two bugs | It hedged | Re-ask: "Pick only the single most likely bug ID" |

---

<a id="topic-2"></a>

# Topic 2: Generative AI Concepts

## Definition

**Generative AI** is AI that **creates new content** (text, code, images) instead of only sorting or predicting a label. The AI assistants you'll use this week (ChatGPT, Copilot and Claude) are built on **Large Language Models (LLMs)**: very large neural networks trained on huge amounts of text. An LLM writes **one token at a time** (a token is a word or part of a word). At each step it predicts the most likely next token, given everything so far. It doesn't look facts up in a database, and it doesn't "know" when it's wrong. It produces text that **sounds** right, and that text is often correct, **but not always**.

## Key Ideas

1. **Next-token prediction.** Everything an LLM does, from answering questions to writing code, comes from repeating one step: *"Given the text so far, what token probably comes next?"*
2. **The context window is the model's short-term memory:** the maximum amount of text (your prompt + the conversation + its reply) it can "see" at once. In a long chat, it can "forget" what you said at the start.
3. **Temperature controls randomness.** **Low** = almost always the most likely word (predictable). **High** = less likely words more often (varied, but riskier). This is why **the same question gives different answers**. Chat apps set the temperature for you; developers set it when they call an AI from code.
4. **Limitations every tester must know:**

   | Limitation | What it means | Testing example |
   |---|---|---|
   | **Hallucination** | Confident, fluent, **wrong** content | Invents a pytest function that doesn't exist |
   | **No guaranteed facts** | Predicts likely text; doesn't check sources | States the wrong boundary value |
   | **Knowledge cut-off** | Only knows its training data | Suggests an outdated Selenium method |
   | **Non-deterministic** | Different answer each time | Two testers get different test cases from the same prompt |

## Worked Example: How an LLM Writes, and Where It Goes Wrong

### Step 1: Be the language model

Your training data is these six Gherkin steps:

```text
given the user is on the login page
when the user enters a valid password
then the user sees the dashboard
given the user is on the cart page
when the user applies a valid coupon
then the user sees the discounted total
```

Predict the next word, using **only** what you've seen above:

- `when the user enters a valid ___`
- `then the user sees the ___`
- `given the user is on the ___`

**What to notice:** for the first one you're sure ("password"). For the last two there are several possible answers, so you're **choosing**. LLMs do exactly this, one word at a time, with probabilities.

### Step 2: Run a tiny language model

Save it as `tiny_llm.py` and run `python tiny_llm.py`. It uses **standard Python only**, so there's nothing to install. Don't worry about every line; focus on the output.

```python
import math
import random
from collections import Counter, defaultdict

# Step 1: the "training data" - a few lines of Gherkin
text = """
given the user is on the login page
when the user enters a valid password
then the user sees the dashboard
given the user is on the cart page
when the user applies a valid coupon
then the user sees the discounted total
"""
words = text.split()

# Step 2: "training" - count which word follows which
follows = defaultdict(Counter)
for current, nxt in zip(words, words[1:]):
    follows[current][nxt] += 1
print("After 'the':", dict(follows["the"]))

# Step 3: "generation" - pick the next word again and again
def generate(start, length=6, seed=None):
    rng = random.Random(seed)
    out = [start]
    for _ in range(length):
        options = follows[out[-1]]
        if not options:
            break
        out.append(rng.choices(list(options), weights=list(options.values()))[0])
    return " ".join(out)

for seed in (3, 10, 2):
    print(generate("when", seed=seed))

# Step 4: temperature - low = safe and predictable, high = more random
scores = {"page": 3.0, "screen": 1.9, "form": 1.1, "button": -0.2}
for t in (0.2, 1.0, 2.0):
    exps = {w: math.exp(s / t) for w, s in scores.items()}
    total = sum(exps.values())
    print(f"temperature {t}:", {w: round(e / total, 2) for w, e in exps.items()})
```

**What to look for:**

- **"Training"** just **counts** which word follows which. That count table is the model's entire "knowledge".
- **"Generation"** picks the next word **at random, weighted by those counts**, again and again.
- The **temperature** part shows how the chances for four possible next words change.

It prints:

```text
After 'the': {'user': 6, 'login': 1, 'dashboard': 1, 'cart': 1, 'discounted': 1}
when the user enters a valid password
when the user sees the cart page
when the discounted total
temperature 0.2: {'page': 1.0, 'screen': 0.0, 'form': 0.0, 'button': 0.0}
temperature 1.0: {'page': 0.66, 'screen': 0.22, 'form': 0.1, 'button': 0.03}
temperature 2.0: {'page': 0.46, 'screen': 0.27, 'form': 0.18, 'button': 0.09}
```

### Step 3: Read the output like a tester

| Generated sentence | What happened |
|---|---|
| `when the user enters a valid password` | Copied from the training data. Correct. |
| `when the user sees the cart page` | **Fluent and believable, but never in the training data.** The model joined pieces that "fit". This is a tiny **hallucination**. |
| `when the discounted total` | Nonsense. Big LLMs rarely do this, but the cause is the same: prediction, not understanding. |

**Temperature:** at **0.2**, "page" gets almost 100%, so the output is always the same. At **2.0** the chances are spread out, so "button" gets picked sometimes.

> **The big takeaway:** ChatGPT, Copilot and Claude are this idea scaled up enormously, with billions of weights instead of a count table. They're far better, but still **predicting likely text**. Fluent does not mean correct.

### Step 4: Same question, different answers

Open **two new chats** and ask the **exact same** question in each:

```text
Suggest 5 names for automated tests that check a coupon code on a checkout page.
```

Compare the two answers. What's the same? What's different?

### Step 5: Catch a hallucination

In a new chat, ask:

```text
Explain what the pytest function pytest.assert_coupon_valid() does and show an example.
```

This function **does not exist**. Does your AI say so, or does it confidently invent an explanation?

### Consolidated Result

Add both prompts to `prompts.txt`:

```text
=== Randomness check - v1 ===
Use: show that the same question gives different answers.
Source: Handout 02, Topic 2

--- Prompt (send in TWO separate new chats, then compare) ---
Suggest 5 names for automated tests that check a coupon code on a checkout page.
```

```text
=== Hallucination probe - v1 ===
Use: test whether the AI admits a function doesn't exist.
Source: Handout 02, Topic 2

--- Prompt (new chat) ---
Explain what the pytest function pytest.assert_coupon_valid() does and show an example.
```

`tiny_llm.py` is the demo file. Keep it if you ran it.

## Checkpoint

**Answer key:**

| Step | Expected |
|---|---|
| Step 1 | "password" (certain); "dashboard" or "discounted" (a choice); "login" or "cart" (a choice) |
| Step 3 | The **middle** sentence is the hallucination: believable, but not in the training data |
| Step 4 | Similar **kinds** of names, but different wording and order. That's randomness (temperature) |
| Step 5 | A good answer says the function **doesn't exist** in pytest. An invented explanation is a hallucination |

**Mark your AI's Step 5 answer:**

- ✅ It says `assert_coupon_valid` is **not** a real pytest function
- ✅ It suggests a correct alternative, such as a plain `assert` or a helper function you write yourself
- ❌ If it invented parameters or behaviour, you've caught a hallucination. Note which tool did it.

**How do you check whether a function is real?** Run the code, or search the **official documentation** (docs.pytest.org). Don't ask the same AI "are you sure?" and trust the answer.

## Your Turn

1. **(In class, 3 min)** Compare your Step 4 answers with a classmate who used a **different** AI tool. How many test names appear in both of your lists?
2. **(After class)** If you wanted an AI to generate **test data that must be identical every run**, would you want low or high temperature? Why?
3. **(After class)** Ask your AI: *"What is your knowledge cut-off date, and what does it mean for questions about the latest version of Selenium?"*
4. **(After class)** If you ran `tiny_llm.py`: change the start word from `"when"` to `"given"`. Which sentences are real (in the training data) and which are invented?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Your two Step 4 answers are identical | Some tools remember earlier chats, or use low randomness for short questions | Use a different tool, or ask for 10 names instead of 5 |
| The AI correctly says the function doesn't exist | Good! Tools are getting better at this | Try a more believable fake name, such as `pytest.approx_money()` |
| `tiny_llm.py` gives different sentences | A typo in the training text changes the counts | Compare your text with the handout letter by letter |

---

<a id="topic-3"></a>

# Topic 3: Generative AI Applications within QE

## Definition

**GenAI in Quality Engineering** means using AI assistants to speed up testing work: understanding requirements, suggesting test ideas, drafting test cases, generating test data, writing and debugging automation code, and summarising test results. The AI produces a **first draft quickly**; the tester remains **responsible** for checking it against the requirement and fixing it. AI is a **fast assistant, not a replacement for test design skills**. Without a human reviewer, AI-generated tests can look professional and still check the **wrong thing**.

## Key Ideas

1. **Where AI helps across the testing life cycle:**

   | Testing activity | How AI helps | What the human still owns |
   |---|---|---|
   | Requirements | Spots vague words and missing rules | Confirming with the business analyst |
   | Test design | Brainstorms test ideas and edge cases fast | Choosing the right technique and the expected results |
   | Test data | Generates many realistic records | Checking the data follows the rules |
   | Automation | Drafts test code and page objects | Making sure tests can actually fail |
   | Reporting | Summarises results and drafts bug reports | Accuracy and the final decision |

2. **Not every problem needs GenAI.** A clear rule → write normal code. Lots of labelled data → classic ML (like Lecture 01). Messy language or creative drafting → GenAI.
3. **The three classic AI test mistakes:** (a) **contradicting** the requirement, (b) **inventing** a requirement that doesn't exist (a hallucination), and (c) **missing** important cases such as boundaries.
4. **AI output is a draft. A human approves it.** You'll learn a full review checklist on Wednesday.

## Worked Example: Review AI-Generated Tests

**The situation:** we have a small function for a coupon, and an AI assistant has written tests for it. The tests look tidy. **Are they right?** We'll run them, review them against the requirement, and fix them.

> **The requirement (our running example for the week):** *SAVE10 gives 10% off orders of **$50.00 or more**. Orders under $50.00 are unchanged. Unknown coupon codes raise a ValueError.*

### Step 1: The code under test

Create a file called `cart.py`:

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

**What this code does:**

- The text in triple quotes (the **docstring**) is the requirement.
- If the code isn't exactly `"SAVE10"`, it **raises** a `ValueError` (an error the caller must handle).
- If the total is $50 or more, it takes 10% off (`total * 0.9`) and rounds to 2 decimal places (cents).
- Otherwise, the total comes back **unchanged**.
- **This code is correct.** Today we're testing the *tests*.

### Step 2: The AI's draft tests

This is the kind of thing an AI assistant typically produces when asked *"Write pytest tests for apply_coupon"*. Create `test_cart_ai_draft.py`:

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

**What this code does:**

- `from cart import apply_coupon` loads our function from `cart.py`. Both files must be in the **same folder**.
- Each function whose name starts with `test_` is a **test**. pytest finds and runs them automatically.
- `assert` checks that something is true. If it isn't, the test **fails**.
- Read the test **names**: they look sensible. That's exactly why AI output is easy to trust too quickly.

### Step 3: Run the draft

In the terminal:

```bash
python -m pytest -q test_cart_ai_draft.py
```

**What this does:** `-q` (quiet) gives a short summary. You'll see **3 failed, 1 passed**.

A beginner's first thought is *"the code has bugs!"*. But read the requirement again: **the code is correct, and the tests are wrong.**

### Step 4: Review each test against the requirement

Go through the draft one test at a time, as a reviewer would:

| Test | Verdict | Why |
|---|---|---|
| `test_save10_applies_discount` | ✅ **Keep** | $100 → $90 matches the requirement |
| `test_save10_small_order_gets_discount` | ❌ **Contradicts the requirement** | Orders under $50 are **unchanged**, not discounted |
| `test_unknown_coupon_returns_original_total` | ❌ **Wrong behaviour** | Unknown codes must **raise ValueError**, not return the total |
| `test_coupon_is_case_insensitive` | ❌ **Invented requirement** | Nothing says lowercase codes work. The AI guessed (a hallucination). **Ask the business analyst** before testing it. |
| *(missing)* | ⚠️ **Gap** | No **boundary** tests at exactly $50.00 and just below ($49.99), which is where bugs most often hide |

> **Think about the opposite case:** if the code had a bug and the AI wrote tests that matched the buggy behaviour, every test would **pass**, and the bug would ship. Passing tests are only as good as the human review behind them.

### Step 5: Write the reviewed tests

Create `test_cart_reviewed.py`:

```python
import pytest
from cart import apply_coupon

# Kept from the AI draft: correct and useful
def test_save10_gives_10_percent_off_large_order():
    assert apply_coupon(100, "SAVE10") == 90

# Fixed (1): orders under $50 are UNCHANGED
def test_save10_small_order_is_unchanged():
    assert apply_coupon(20, "SAVE10") == 20
```

Then add the rest:

```python
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

**What this code does:**

- `import pytest` is needed for `pytest.raises`.
- `with pytest.raises(ValueError):` means *"the code inside this block **must** raise a ValueError, or the test fails"*. This is how you test expected errors.
- The comment for (3) records **why** we removed a test. Good reviewers leave a trail.
- The two boundary tests check **exactly $50.00** (should get the discount, so $45.00) and **$49.99** (just under, so unchanged). You learned this technique in Week 3: **Boundary Value Analysis**.

### Consolidated File: `test_cart_reviewed.py`

(`cart.py` from Step 1 stays the same.)

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

## Checkpoint

**Step 3** (the AI draft):

```text
FAILED test_cart_ai_draft.py::test_save10_small_order_gets_discount - Asserti...
FAILED test_cart_ai_draft.py::test_unknown_coupon_returns_original_total - Va...
FAILED test_cart_ai_draft.py::test_coupon_is_case_insensitive - ValueError: U...
3 failed, 1 passed in 0.02s
```

**Step 5** (the reviewed tests), after running `python -m pytest -q test_cart_reviewed.py`:

```text
.....                                                                    [100%]
5 passed in 0.01s
```

Each `.` is a passing test. The timings will differ slightly on your computer.

## Your Turn

1. **(In class, 3 min)** Add one more boundary test of your own: `apply_coupon(50.01, "SAVE10")`. What should the result be? (Hint: 50.01 × 0.9, rounded to 2 decimals.) Run it to check.
2. **(After class)** **Generate your own draft.** Paste `cart.py` into your AI assistant and ask: *"Write pytest tests for this function."* Review **its** answer using the Step 4 table format (Keep / Contradicts / Wrong behaviour / Invented / Gap). Did it make any of the same mistakes? Did it include the $50.00 boundary?
3. **(After class)** Now ask again, but give the AI the requirement **and** a hint: *"Write pytest tests for this function. The requirement is in the docstring. Include boundary value tests and test that unknown codes raise ValueError. Don't assume anything that isn't in the requirement."* Compare the result with exercise 2. What changed? (This is a preview of Lecture 03: **prompt engineering**.)
4. **(After class)** For each task, decide: **GenAI**, **classic ML** or **no AI (normal code)**. Give a one-line reason.
   - (a) Check that an API returns HTTP status 200
   - (b) Draft 20 test ideas from a new user story
   - (c) Predict which tests are likely to be flaky, using 2 years of labelled run history
   - (d) Summarise 300 failed test messages into a short report for a manager

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'cart'` | `cart.py` isn't in the same folder as the test file, or you're running pytest from a different folder | Put both files in one folder and run pytest **from that folder** |
| `no tests ran` | The file or function names don't start with `test_` | Rename them: `test_cart_reviewed.py`, `def test_...` |
| `'pytest' is not recognized...` | The pytest command isn't on your PATH | Use `python -m pytest` instead of `pytest` |
| `NameError: name 'pytest' is not defined` | You used `pytest.raises` without importing pytest | Add `import pytest` at the top |

---

## Lecture Wrap-Up: Quick Check

1. Why must NLP systems turn text into numbers?
2. Word matching gave "Discount voucher makes the basket price incorrect" a score of 0 against BUG-104. Why, and what kind of AI catches it?
3. In one sentence: how does an LLM produce an answer?
4. You ask an AI assistant the same question twice and get two different answers. Is it broken? Which idea from today explains this?
5. An AI assistant wrote 10 tests and all of them pass. Is the feature tested properly? What should you do?

<details>
<summary>Answers</summary>

1. Computers can only do maths with numbers. Once text is numbers, we can measure things like similarity.
2. It shares **no words** with BUG-104 ("voucher" vs. "coupon", "basket" vs. "cart"). AI that uses **embeddings** (meaning), such as an LLM, catches it.
3. It predicts the most likely **next token**, adds it, and repeats until the answer is complete.
4. It's not broken. **Temperature / randomness**: LLMs pick from likely tokens, so the answers vary.
5. Not necessarily. The tests may check the wrong thing (or match a bug). **Review every test against the requirement**, and check for missing cases such as boundaries.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **NLP (Natural Language Processing)** | AI that works with human language |
| **Token** | A piece of text a model works with: a word or part of a word |
| **Stop words** | Very common words ("the", "is") often removed before analysis |
| **Word matching (TF-IDF)** | Comparing texts by the words they share, with distinctive words counting more |
| **Similarity score** | A 0-to-1 number for how alike two texts are |
| **Embedding** | Numbers that capture *meaning*, so synonyms end up close together |
| **Generative AI** | AI that creates new content (text, code, images) |
| **LLM (Large Language Model)** | A very large neural network trained on text to predict the next token |
| **Context window** | The maximum amount of text a model can "see" at once |
| **Temperature** | A setting that controls how random the model's choices are |
| **Hallucination** | Confident, fluent output that is wrong or invented |
| **Knowledge cut-off** | The date after which the model has no training data |
| **Boundary Value Analysis (BVA)** | A test design technique that checks values at and around limits |

## Summary

- **NLP** = clean the text → turn it into numbers → compare. Word matching is fast but blind to synonyms; meaning-based AI (embeddings) can see them.
- **LLMs generate text one token at a time by prediction.** The context window is their short-term memory, and temperature controls how random they are.
- **Fluent ≠ correct.** Hallucinations are a natural side effect of prediction. Check facts against real sources.
- **In QE, AI produces drafts quickly. Testers review them**: check against the requirement, remove invented rules, fix contradictions and add missing cases such as boundaries.
