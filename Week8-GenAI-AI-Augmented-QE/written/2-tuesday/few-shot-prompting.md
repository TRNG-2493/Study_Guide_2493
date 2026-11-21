# Few-Shot Prompting

## Learning Objectives

By the end of this lesson you will be able to:

- Define **zero-shot**, **one-shot** and **few-shot** prompting and recognise each in a real prompt.
- Explain **in-context learning**: how a model can follow your examples without being retrained, and how this differs from the supervised training you studied on Monday.
- Explain **why examples work** so well for controlling format, style, granularity and labels ("show, don't tell").
- Build a well-structured few-shot prompt (instruction, examples, new input, delimiters), both as a single text prompt and as a list of chat **messages**.
- Choose **good examples**: representative, diverse, correct, consistently formatted, label-balanced and including edge cases.
- Decide **how many** examples to use and describe how **example order** can bias the answer.
- Recognise the main **risks** of few-shot prompting: over-copying, example leakage and outdated examples.
- Write a small Python **example selector** that picks the most relevant examples for each new input, and a **label-balance check** that warns you when your examples are lopsided.
- Apply few-shot prompting to three QE tasks: **bug report classification**, **test cases in your team's house style** and **acceptance criteria to Gherkin**.

---

## Why This Matters

Imagine you join a new QE team. On your first morning, your lead could give you a two-page document describing how the team writes bug reports. Or she could open Jira and say: "Here are three bug reports we were happy with. Write yours like these." Most people learn faster from the three examples. The examples show the tone, the level of detail, the field order and the naming conventions all at once, without anyone having to put them into words.

Large language models behave in a very similar way. You can describe the output you want in instructions (and you should; see today's lessons on **prompt engineering principles** and **specificity and context**). But for many QE tasks, the fastest way to get output that *looks like your team's work* is to include a few worked examples in the prompt. This technique is called **few-shot prompting**, and it is one of the most reliable tools a prompt engineer has.

This matters for the Weekly Epic. This week you move from using AI as a chat assistant to designing your **first QA agent** on Thursday and Friday. An agent must produce consistent, predictable output every time it runs, because other code (and other people) depend on it. Examples are one of the main ways you make an LLM's output consistent. On Thursday you will meet **sample input/output pairs** as a formal part of an agent's design; today you learn the underlying skill they rely on.

It also matters for **Project 2**. In today's exercise you build a prompt library for test design and debugging. Several of the prompts in that library will be few-shot prompts: prompts that hold examples of good test cases, good bug classifications or good Gherkin scenarios from your own e-commerce application, so that every new output matches your framework's conventions.

---

## The Concept

### 1. Zero-Shot, One-Shot and Few-Shot

The word **"shot"** here means **"example"**. The terms describe how many worked examples of the task you include in the prompt.

| Term | Number of examples in the prompt | What the model has to go on |
|------|----------------------------------|-----------------------------|
| **Zero-shot** | 0 | Only your instruction (plus everything it learned in pre-training). |
| **One-shot** | 1 | Your instruction plus a single worked example. |
| **Few-shot** | Usually 2 to 5 (sometimes more) | Your instruction plus several worked examples. |

Here is the same task, classifying a bug report by severity, written all three ways.

**Zero-shot:**

```text
Classify this bug report as Critical, Major or Minor.

Bug report: Removing an item from the cart leaves its price in the total.
```

**One-shot:**

```text
Classify each bug report as Critical, Major or Minor.

Bug report: Clicking 'Pay now' charges the card twice.
Severity: Critical

Bug report: Removing an item from the cart leaves its price in the total.
Severity:
```

**Few-shot:**

```text
Classify each bug report as Critical, Major or Minor.

Bug report: Clicking 'Pay now' charges the card twice.
Severity: Critical

Bug report: Search results page shows 'Reslts' instead of 'Results'.
Severity: Minor

Bug report: Users cannot log in after resetting their password.
Severity: Major

Bug report: Removing an item from the cart leaves its price in the total.
Severity:
```

Notice three things:

1. The **instruction** is still there in every version. Examples add to instructions; they rarely replace them.
2. In the one-shot and few-shot versions, the prompt **ends with an unfinished pattern** (`Severity:`). Remember from Monday that an LLM works by predicting the next token. A clear, repeated pattern makes the most likely next tokens the ones you want: a single severity word.
3. With zero examples, the model might answer "This is probably a Major issue because customers would be overcharged…" (a paragraph). With three examples, it is far more likely to answer with exactly one word, because every example answered with one word.

You will also see the term **multishot prompting**, which some vendors (for example Anthropic) use as a synonym for few-shot prompting.

### 2. In-Context Learning: Learning Without Retraining

On Monday you studied **supervised learning**. A model is shown many labelled examples, it makes predictions, a loss function measures its errors, and an optimiser (gradient descent and backpropagation) **changes the model's weights** to reduce those errors. Learning in that sense means **the model itself changes**.

Few-shot prompting is different. When you put three examples into a prompt:

- **No weights change.** The model is exactly the same model before and after your request.
- The examples only exist inside the **context window** for that single request (you met the context window on Monday).
- The next request starts fresh. If you do not include the examples again, the model has no memory of them.

The model's ability to pick up a task from examples placed in its input is called **in-context learning**. It was made famous by the 2020 GPT-3 paper *Language Models are Few-Shot Learners* (Brown et al.), which showed that a large enough model could perform many tasks from a handful of demonstrations "without any gradient updates or fine-tuning".

| | Supervised training (Monday) | Few-shot prompting (today) |
|--|-----------------------------|----------------------------|
| Where the examples go | Into a training dataset | Into the prompt |
| Typical number of examples | Thousands to millions | 1 to 5 (sometimes up to a few dozen) |
| Do the weights change? | Yes | No |
| How long does it last? | Permanently (until retrained) | Only for this one request |
| Cost of changing behaviour | Retraining run (hours, money, ML skills) | Edit a text prompt (seconds) |
| Who can do it | ML engineers with data and compute | Anyone who can write a prompt |

An analogy: supervised training is like **sending someone on a six-week course**; they come back permanently changed. Few-shot prompting is like **handing an experienced colleague a sticky note with three examples** before a task. They already have the general skill; the note tells them exactly how *you* want it done today. Tomorrow, without the note, they will not remember.

Why does this work at all? During pre-training the model saw enormous amounts of text that contains patterns of the form "here are some items, here is another one that follows the same pattern" (lists, tables, Q&A pages, test files full of similar test functions). It became very good at **continuing patterns**. A few-shot prompt sets up a pattern, and the model continues it.

### 3. Why Examples Work: "Show, Don't Tell"

Try to describe, in words only, how your team writes a test case title. You might write: "Use a short title that starts with a verb, names the feature, mentions the key condition, avoids filler words, uses sentence case, and stays under about ten words." That is already a long instruction, and the model may still interpret "short" or "key condition" differently from you.

Now compare with one example:

```text
Title: Apply SAVE10 to an order of exactly $50.00
```

The example communicates all of those rules at once, and some you did not think to mention (the dollar format with two decimals, the use of the real coupon code). Examples are especially strong at showing:

| What examples show well | QE illustration |
|-------------------------|-----------------|
| **Format** | One line per answer; a table; Gherkin keywords; a fixed field order. |
| **Style and tone** | Neutral, factual bug report language rather than dramatic language ("app is totally broken!!"). |
| **Granularity** (level of detail) | One test case per boundary value, rather than one vague test that "checks coupons". |
| **Labels and categories** | The exact allowed values (`Critical`, `Major`, `Minor`), with the exact spelling and capitalisation. |
| **Decision boundaries** | Where your team draws the line, for example that a spelling error is `Minor` even on the checkout page. |
| **Implicit conventions** | ID schemes (`TC-CART-001`), naming of test data, which preconditions you always state. |

The last two rows deserve attention. Every team has conventions nobody has written down. Instructions can only describe the conventions you remember to describe. Examples carry the ones you forget as well, which is both a strength and, as you will see in Section 8, a risk.

Instructions and examples work best **together**:

- The **instruction** states the task and the rules that must never be broken ("Use only these four component names").
- The **examples** show what following those rules looks like in practice.

If the instruction and the examples disagree (for example, the instruction says "answer in one word" but an example answers with a sentence), the model often follows the **examples**. Keep them consistent.

### 4. Anatomy of a Few-Shot Prompt

A well-built few-shot prompt has four parts:

1. **Instruction**: what the task is and any hard rules (allowed values, output format).
2. **Examples**: input → output pairs that demonstrate the task.
3. **New input**: the item you actually want handled.
4. **Delimiters**: clear markers that separate the parts, so the model can tell examples from instructions and from the real input.

Delimiters can be headings (`### Example 1`), labels (`Input:` / `Output:`), XML-style tags (`<example>…</example>`, which Anthropic's documentation recommends for Claude) or triple quotes. Which style you choose matters less than **using one style consistently**.

Writing these prompts by hand gets tedious and error-prone, so in practice you build them with code. The following script stores the examples as a list of Python dictionaries and assembles the prompt.

```python
# build_few_shot.py
INSTRUCTION = (
    "Classify each bug report by severity (Critical, Major, Minor) "
    "and component (Login, Search, Cart, Checkout). "
    "Answer in exactly this format: Severity: <value> | Component: <value>"
)

EXAMPLES = [
    {"input": "Clicking 'Pay now' charges the card twice.",
     "output": "Severity: Critical | Component: Checkout"},
    {"input": "Search results page shows 'Reslts' instead of 'Results'.",
     "output": "Severity: Minor | Component: Search"},
    {"input": "Users cannot log in after resetting their password.",
     "output": "Severity: Major | Component: Login"},
]

def build_few_shot_prompt(instruction, examples, new_input):
    parts = [instruction, ""]
    for i, ex in enumerate(examples, start=1):
        parts.append(f"### Example {i}")
        parts.append(f"Bug report: {ex['input']}")
        parts.append(ex["output"])
        parts.append("")
    parts.append("### Now classify this one")
    parts.append(f"Bug report: {new_input}")
    return "\n".join(parts)

prompt = build_few_shot_prompt(
    INSTRUCTION, EXAMPLES,
    "Removing an item from the cart leaves its price in the total.")
print(prompt)
```

Output:

```text
Classify each bug report by severity (Critical, Major, Minor) and component (Login, Search, Cart, Checkout). Answer in exactly this format: Severity: <value> | Component: <value>

### Example 1
Bug report: Clicking 'Pay now' charges the card twice.
Severity: Critical | Component: Checkout

### Example 2
Bug report: Search results page shows 'Reslts' instead of 'Results'.
Severity: Minor | Component: Search

### Example 3
Bug report: Users cannot log in after resetting their password.
Severity: Major | Component: Login

### Now classify this one
Bug report: Removing an item from the cart leaves its price in the total.
```

How the code works, line by line:

- `INSTRUCTION = ( ... )`: three string literals placed next to each other inside parentheses are joined into one string by Python. This is a tidy way to write a long string across several lines.
- `EXAMPLES = [ {...}, {...}, {...} ]`: a **list of dictionaries**. Each dictionary is one example with two keys: `"input"` (the bug report) and `"output"` (the answer we want). Keeping examples as data, separate from the code that formats them, means you can add, remove or reorder examples without touching the prompt-building logic.
- `def build_few_shot_prompt(instruction, examples, new_input):` defines a function with three parameters, so the same function works for any instruction, any examples and any new bug report.
- `parts = [instruction, ""]` starts a list of lines. The empty string `""` becomes a blank line, which visually separates the instruction from the examples.
- `for i, ex in enumerate(examples, start=1):` loops over the examples. `enumerate` gives you a counter `i` alongside each item `ex`; `start=1` makes the counter start at 1 instead of 0, so the headings read "Example 1, 2, 3".
- `parts.append(f"### Example {i}")` adds a **delimiter heading**. The `f"..."` is an f-string (Week 1): `{i}` is replaced by the counter value.
- `parts.append(f"Bug report: {ex['input']}")` adds the example input with a consistent label. Note the single quotes inside the double-quoted f-string; using the same quote type would end the string early.
- `parts.append(ex["output"])` adds the desired answer exactly as written.
- After the loop, the final heading `### Now classify this one` and the new bug report are added. The prompt ends with the new input, so the model's next tokens should be the classification.
- `"\n".join(parts)` glues all lines together with newline characters between them, producing one string.

The prompt itself sends nothing to a model; it is just a string. Today's demo shows the same kind of prompt being sent to a real LLM.

### 5. Choosing Good Examples

The quality of a few-shot prompt depends almost entirely on the quality of its examples. Use this checklist.

**1. Representative.** Examples should look like the real inputs the prompt will receive. If real bug reports are three-sentence Jira descriptions with steps to reproduce, one-line toy examples teach the model the wrong length and style. Anthropic's documentation puts it as: make examples **relevant**, mirroring your actual use case closely.

**2. Diverse.** Cover different components, different severities and different writing styles. If all three examples are about checkout, the model may lean towards labelling everything `Checkout`. Diversity also stops the model latching onto an accidental shared feature (see "over-copying" in Section 8).

**3. Include edge and negative cases.** Include at least one example that sits near a decision boundary or that shows a "nothing to report" answer. For example, a spelling mistake on the payment page: is it `Critical` because it is on checkout, or `Minor` because it is cosmetic? If your team says `Minor`, an example showing that is worth more than a paragraph of rules. This is **error guessing** and **boundary thinking** from Week 3 applied to the prompt itself.

**4. Consistent format.** Every example must use exactly the same labels, separators, capitalisation and field order. If one example says `Severity: major` and another `Severity: Major`, you will get both forms back, and any code that parses the output will break.

**5. Correct.** This sounds obvious, but it is the most damaging mistake. The model copies what it sees, **including mistakes**. If an example test case says SAVE10 gives 10% off a $40 order (the real rule is orders of $50 or more), you have just taught the model a wrong rule. Review examples as carefully as production test code.

**6. Balanced labels.** If four of your five examples are labelled `Major`, the model will be pulled towards `Major` (see "majority-label bias" in Section 7). Aim for a roughly even spread across the labels, unless you deliberately want to reflect real-world frequency.

**7. Realistic difficulty.** If all examples are easy and obvious, the model learns nothing about the hard cases. Include at least one example that a junior tester might get wrong.

Here is a poor example set and an improved one for the same classification task:

| Poor set | Problem | Improved set |
|----------|---------|--------------|
| "Checkout broken." → `Severity: Critical \| Component: Checkout` | Too short, unrealistic | "Clicking 'Pay now' charges the card twice." → `Severity: Critical \| Component: Checkout` |
| "Checkout page slow." → `Severity: major \| Component: Checkout` | Lowercase label, same component again | "Search results page shows 'Reslts' instead of 'Results'." → `Severity: Minor \| Component: Search` |
| "Checkout button wrong colour." → `Severity: Critical \| Component: Checkout` | Wrong label (cosmetic should not be Critical), no diversity | "Users cannot log in after resetting their password." → `Severity: Major \| Component: Login` |

The poor set has every one of the problems on the checklist: unrealistic inputs, one component only, an inconsistent label and an incorrect label.

### 6. How Many Examples?

There is no single correct number, but there are useful rules of thumb.

- **Zero** when the task is common and the format is simple (for example, "Summarise this log in two sentences").
- **One** when you mainly need to show a format or a template.
- **Two to five** for most classification and generation tasks. Anthropic's prompting guide suggests **3 to 5 examples** for best results.
- **More** only when the task has many categories or subtle distinctions, and only if testing shows it helps.

Two forces limit the number:

**Diminishing returns.** The first example usually produces the biggest improvement, because it establishes the format. The second and third show variety. After that, each additional example typically adds less, and beyond a point it may add nothing.

**Token cost.** Every example is sent with **every** request. Suppose each example is about 40 tokens and you include 5 examples: that is 200 extra input tokens per request. If a test pipeline classifies 2,000 failure messages per day, that is 400,000 extra tokens per day, and more if the examples are long test files rather than one-line bug reports. Long examples also use up the **context window**, leaving less room for the real input. (Monday covered tokens and the context window; Week 10 looks at token usage and cost in detail.)

The practical approach is **empirical**: start with two or three examples, try the prompt on a set of real inputs, and add an example only when you see a specific kind of mistake that the new example would correct. Treat each added example like a test case added to cover a defect.

### 7. Order Matters: Recency Bias and Majority-Label Bias

Researchers have found that LLMs can be sensitive to the **order** in which examples appear. Two effects are especially relevant.

**Recency bias.** Examples near the **end** of the list (closest to the new input) tend to have more influence. If your last example is labelled `Critical`, the model may be slightly more likely to answer `Critical` for the new input.

**Majority-label bias.** If most examples share a label, the model is pulled towards that label, regardless of the new input.

These effects do not mean few-shot prompting is unreliable; they mean you should be deliberate:

- **Balance** labels across the examples (Section 5).
- **Vary** the position of each label; do not always put `Critical` last.
- When the stakes are high, **test** a few different orders on the same inputs and check that the answers do not change. If they do change, your examples are not clear enough on their own.
- If you deliberately want the most relevant example to have the most influence, put it **last**. You will see this used in the example selector in Section 10.

### 8. Risks of Few-Shot Prompting

Examples are powerful, and that power can work against you.

**Over-copying (anchoring on surface details).** The model may copy features of the examples that you did not intend to be part of the pattern. If every example test case uses the coupon `SAVE10` and an $80 order, generated test cases for a new feature (say, gift cards) may still mention `SAVE10` or $80. If every example has exactly three steps, new test cases may be squeezed into three steps even when they need six. Diversity in your examples (Section 5) is the main defence.

**Example leakage.** Sometimes the model returns content **from an example** instead of a new answer, especially when the new input is short or similar to an example. A typical sign: a generated test case with the same title as Example 2. Clear delimiters (`### Now classify this one`) and an instruction such as "Do not repeat the examples" reduce this. Also check outputs for exact copies of example text.

**Outdated examples.** Examples are often copied from real work and then forgotten. Six months later the UI has renamed the "Pay now" button to "Place order", the `Login` component has been split into `Login` and `Account`, and the examples quietly teach the model the old world. Store examples in version control (Week 1 Git) next to your test code, and review them when the application changes.

**Sensitive data in examples.** Examples copied from real bug reports or logs may contain customer names, emails or tokens. Whatever you put in an example is sent to the AI provider with every request. How to handle this responsibly is covered on **Wednesday** (responsible use of AI in QE); for today, only use synthetic or sanitised examples.

**False confidence.** A model that produces output in exactly the right format can look more trustworthy than it is. Correct format does not mean correct content. Formal approaches to reviewing AI output are covered on **Wednesday** (human validation of AI output).

### 9. Few-Shot as Inline Text or as Chat Messages

So far the examples have been written **inline**, inside one block of text. Chat-based LLM APIs offer a second option. Their input is a list of **messages**, each with a **role**:

- `system`: overall instructions for the conversation.
- `user`: what the person (or your code) says.
- `assistant`: what the model said.

You can present each example as a **fake earlier turn** of the conversation: a `user` message containing the example input, followed by an `assistant` message containing the ideal answer. The model then sees a conversation in which it has already answered three times in exactly the right style, and it tends to continue in the same style.

The following script builds such a message list and shows a round trip. Because we are not calling a real model in this lesson, it uses `fake_llm`, a small **stand-in** function that looks for keywords. It is not an LLM and does not learn from the examples; it exists only so you can see the full flow (build messages, get a reply, parse the reply) run on your machine.

```python
# few_shot_messages.py
SYSTEM = (
    "You classify bug reports for an e-commerce web app. "
    "Reply with exactly: Severity: <Critical|Major|Minor> | Component: <Login|Search|Cart|Checkout>"
)

EXAMPLES = [
    {"input": "Clicking 'Pay now' charges the card twice.",
     "output": "Severity: Critical | Component: Checkout"},
    {"input": "Search results page shows 'Reslts' instead of 'Results'.",
     "output": "Severity: Minor | Component: Search"},
    {"input": "Users cannot log in after resetting their password.",
     "output": "Severity: Major | Component: Login"},
]

def build_messages(system, examples, new_input):
    messages = [{"role": "system", "content": system}]
    for ex in examples:
        messages.append({"role": "user", "content": ex["input"]})
        messages.append({"role": "assistant", "content": ex["output"]})
    messages.append({"role": "user", "content": new_input})
    return messages

def fake_llm(messages):
    """A deterministic STAND-IN for a real model. It only looks for keywords."""
    text = messages[-1]["content"].lower()
    component = "Cart" if "cart" in text else "Checkout" if "pay" in text else "Search"
    severity = "Major" if "total" in text or "cannot" in text else "Minor"
    return f"Severity: {severity} | Component: {component}"

def parse_label(reply):
    severity_part, component_part = reply.split("|")
    return {
        "severity": severity_part.split(":")[1].strip(),
        "component": component_part.split(":")[1].strip(),
    }

msgs = build_messages(SYSTEM, EXAMPLES,
                      "Removing an item from the cart leaves its price in the total.")
print("Number of messages:", len(msgs))
for m in msgs:
    print(f"{m['role']:>9}: {m['content'][:60]}")

reply = fake_llm(msgs)
print("\nModel reply:", reply)
print("Parsed:", parse_label(reply))
```

Output:

```text
Number of messages: 8
   system: You classify bug reports for an e-commerce web app. Reply wi
     user: Clicking 'Pay now' charges the card twice.
assistant: Severity: Critical | Component: Checkout
     user: Search results page shows 'Reslts' instead of 'Results'.
assistant: Severity: Minor | Component: Search
     user: Users cannot log in after resetting their password.
assistant: Severity: Major | Component: Login
     user: Removing an item from the cart leaves its price in the total

Model reply: Severity: Major | Component: Cart
Parsed: {'severity': 'Major', 'component': 'Cart'}
```

How the code works:

- `build_messages` starts the list with one `system` message holding the instruction.
- For each example it appends **two** messages: a `user` message with the example input and an `assistant` message with the ideal output. Three examples therefore produce six messages.
- Finally it appends the real input as a `user` message. 1 system + 6 example messages + 1 real input = **8 messages**, which matches the printed count.
- The printing loop uses `f"{m['role']:>9}"`. The `:>9` format specifier right-aligns the role name in a 9-character column so the output lines up, and `m['content'][:60]` uses **slicing** to show only the first 60 characters of each message.
- `fake_llm(messages)` looks only at the last message (`messages[-1]`, the real input), lower-cases it and uses simple `if ... else` expressions to choose a component and severity. Again: this is a stand-in to make the example runnable, not a model.
- `parse_label(reply)` turns the reply text into a dictionary. `reply.split("|")` splits `"Severity: Major | Component: Cart"` into two parts at the `|` character; each part is then split at `:` and `.strip()` removes the surrounding spaces. This parsing only works because the examples locked the format so firmly. (Making output reliably machine-readable is the subject of today's lesson on **format locking**.)

**Inline or messages: which should you use?**

| | Inline examples | Example messages (user/assistant pairs) |
|--|-----------------|-----------------------------------------|
| Works in a chat UI (copy and paste) | Yes | Not directly |
| Works with an API | Yes | Yes |
| Clear separation between examples | Depends on your delimiters | Built into the message structure |
| Model sees examples as "its own" earlier answers | No | Yes, which can strengthen style copying |
| Easy to read and review in a prompt library | Very easy | Easy once you are used to the structure |

Both are valid. For your prompt library today, inline examples are simpler because you can paste them into any chat tool. When you build agents later this week, you will work with message lists directly.

### 10. Choosing Examples Dynamically

So far the examples have been fixed: the same three examples for every bug report. That works when the inputs are similar. But imagine your team keeps a **pool** of 50 good, reviewed classifications. Sending all 50 every time is expensive, and many would be irrelevant. A better approach is to pick, for each new input, the few examples that are **most similar** to it. This is called **dynamic example selection**.

To do that, you need a way to measure how similar two pieces of text are. On Monday you met **embeddings**, which capture meaning; they are what production systems usually use. Here we use a much simpler measure that you can compute by hand: **Jaccard similarity**.

**Jaccard similarity** of two texts = (number of distinct words they share) ÷ (number of distinct words that appear in either one).

Let us compute one by hand. New bug report: *"Applying coupon SAVE10 to a $45 order still gives a discount."*

- Its distinct words (lower-cased, punctuation removed): applying, coupon, save10, to, a, 45, order, still, gives, discount → **10 words**.

Pool example: *"Coupon SAVE10 is accepted on a $20 order."*

- Its distinct words: coupon, save10, is, accepted, on, a, 20, order → **8 words**.
- Shared words (the **intersection**): coupon, save10, a, order → **4 words**.
- Words in either (the **union**): 10 + 8 − 4 = **14 words** (we subtract the shared words so they are not counted twice).
- Jaccard = 4 ÷ 14 ≈ **0.29**.

A score of 1.0 means identical word sets; 0.0 means no words in common. Now the code:

```python
# select_examples.py
import re

EXAMPLE_POOL = [
    {"input": "Clicking 'Pay now' charges the card twice.", "label": "Critical"},
    {"input": "Coupon SAVE10 is accepted on a $20 order.", "label": "Major"},
    {"input": "Search returns no results for 'T-shirt' but works for 'tshirt'.", "label": "Major"},
    {"input": "Login button is misaligned on mobile screens.", "label": "Minor"},
    {"input": "Cart badge shows 0 items after adding a product.", "label": "Major"},
    {"input": "Footer copyright year is out of date.", "label": "Minor"},
    {"input": "Order total ignores the SAVE10 coupon on a $80 order.", "label": "Major"},
    {"input": "Checkout page crashes when the address has an apostrophe.", "label": "Critical"},
]

def tokenize(text):
    """Lower-case the text and return the SET of its words."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def jaccard(a, b):
    """Shared words divided by all distinct words in either text."""
    set_a, set_b = tokenize(a), tokenize(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def select_examples(pool, new_input, k=3):
    scored = [(jaccard(ex["input"], new_input), ex) for ex in pool]
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:k]

new_bug = "Applying coupon SAVE10 to a $45 order still gives a discount."
for score, ex in select_examples(EXAMPLE_POOL, new_bug, k=3):
    print(f"{score:.2f}  [{ex['label']}]  {ex['input']}")
```

Output:

```text
0.29  [Major]  Coupon SAVE10 is accepted on a $20 order.
0.27  [Major]  Order total ignores the SAVE10 coupon on a $80 order.
0.06  [Major]  Cart badge shows 0 items after adding a product.
```

The top score, 0.29, matches the value we calculated by hand.

How the code works:

- `import re` loads Python's **regular expression** module.
- `tokenize(text)`: `text.lower()` makes the comparison case-insensitive (`Coupon` and `coupon` count as the same word). `re.findall(r"[a-z0-9]+", ...)` finds every run of letters and digits, which drops punctuation such as `$`, `.` and `'`. Wrapping the result in `set(...)` removes duplicates, because Jaccard works on **distinct** words. (This is the same idea as the simple tokenisation you saw in Monday's NLP lesson.)
- `jaccard(a, b)`: `set_a & set_b` is the set **intersection** (words in both) and `set_a | set_b` is the set **union** (words in either). `len(...)` counts them. The `if not set_a or not set_b` guard avoids dividing by zero when a text is empty.
- `select_examples(pool, new_input, k=3)`: the **list comprehension** builds a list of `(score, example)` pairs, one per example in the pool. `scored.sort(key=lambda pair: pair[0], reverse=True)` sorts by the score (the first item of each pair) from highest to lowest; `lambda pair: pair[0]` is a tiny unnamed function that says "sort by the score". `scored[:k]` keeps the top `k`.
- The print uses `{score:.2f}` to show the score with two decimal places.

**Spot the problem.** Look at the labels: all three selected examples are `Major`. The selector did exactly what we asked (find similar examples), but it has produced a set with **100% one label**, which is the majority-label bias from Section 7. The new bug report *is* probably `Major`, but the model is no longer being shown what `Critical` or `Minor` look like, so it has nothing to compare against. A QE mindset means testing your own tools, so let us write a check for this.

```python
# label_balance.py
from collections import Counter

def check_label_balance(examples, max_share=0.5):
    counts = Counter(ex["label"] for ex in examples)
    total = len(examples)
    print("Label counts:", dict(counts))
    warnings = []
    for label, count in counts.items():
        share = count / total
        if share > max_share:
            warnings.append(f"'{label}' is {share:.0%} of the examples")
    return warnings

chosen = [
    {"input": "Coupon SAVE10 is accepted on a $20 order.", "label": "Major"},
    {"input": "Order total ignores the SAVE10 coupon on a $80 order.", "label": "Major"},
    {"input": "Cart badge shows 0 items after adding a product.", "label": "Major"},
]
print(check_label_balance(chosen))

better = [
    {"input": "Coupon SAVE10 is accepted on a $20 order.", "label": "Major"},
    {"input": "Clicking 'Pay now' charges the card twice.", "label": "Critical"},
    {"input": "Footer copyright year is out of date.", "label": "Minor"},
]
print(check_label_balance(better))
```

Output:

```text
Label counts: {'Major': 3}
["'Major' is 100% of the examples"]
Label counts: {'Major': 1, 'Critical': 1, 'Minor': 1}
[]
```

How the code works:

- `Counter` (from the standard `collections` module) counts how many times each value appears. `Counter(ex["label"] for ex in examples)` feeds it every label using a **generator expression** (like a list comprehension, without building the list first).
- `max_share=0.5` is a **default parameter**: unless the caller says otherwise, any label making up more than half of the examples triggers a warning.
- For each label, `share = count / total` computes its fraction. `f"{share:.0%}"` formats a fraction as a percentage with no decimals (1.0 becomes `100%`).
- The function **returns a list of warnings**. An empty list `[]` means "no problems found", a pattern that makes the function easy to use in a pytest assertion such as `assert check_label_balance(examples) == []`.

Now combine the two ideas: pick the most similar example **for each label**, so the model always sees every label once, and the most relevant example still appears.

```python
# select_balanced.py
import re

EXAMPLE_POOL = [
    {"input": "Clicking 'Pay now' charges the card twice.", "label": "Critical"},
    {"input": "Coupon SAVE10 is accepted on a $20 order.", "label": "Major"},
    {"input": "Search returns no results for 'T-shirt' but works for 'tshirt'.", "label": "Major"},
    {"input": "Login button is misaligned on mobile screens.", "label": "Minor"},
    {"input": "Cart badge shows 0 items after adding a product.", "label": "Major"},
    {"input": "Footer copyright year is out of date.", "label": "Minor"},
    {"input": "Order total ignores the SAVE10 coupon on a $80 order.", "label": "Major"},
    {"input": "Checkout page crashes when the address has an apostrophe.", "label": "Critical"},
]

def tokenize(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def jaccard(a, b):
    set_a, set_b = tokenize(a), tokenize(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def select_balanced(pool, new_input):
    """Pick the single most similar example for EACH label."""
    best = {}
    for ex in pool:
        score = jaccard(ex["input"], new_input)
        label = ex["label"]
        if label not in best or score > best[label][0]:
            best[label] = (score, ex)
    # Sort so the most similar example comes LAST (closest to the new input).
    return sorted(best.values(), key=lambda pair: pair[0])

new_bug = "Applying coupon SAVE10 to a $45 order still gives a discount."
for score, ex in select_balanced(EXAMPLE_POOL, new_bug):
    print(f"{score:.2f}  [{ex['label']}]  {ex['input']}")
```

Output:

```text
0.00  [Critical]  Clicking 'Pay now' charges the card twice.
0.00  [Minor]  Login button is misaligned on mobile screens.
0.29  [Major]  Coupon SAVE10 is accepted on a $20 order.
```

How the code works:

- `best = {}` is a dictionary that maps each label to the best `(score, example)` pair seen so far.
- For each example, the `if` statement stores it when the label has not been seen yet (`label not in best`) **or** when it beats the stored score (`score > best[label][0]`; index `[0]` is the score inside the pair). When two examples tie, the first one found is kept, which is why the `Critical` and `Minor` choices are the first examples of those labels in the pool.
- `sorted(best.values(), key=lambda pair: pair[0])` sorts the winners from **lowest to highest** score, so the most relevant example is placed **last**, right before the new input. This is a deliberate use of recency (Section 7): we want the closest example to have the most influence. The trade-off is that it also nudges the model slightly towards that example's label, so for high-stakes classification you would test both orders.

Notes on the technique:

- Jaccard compares **words, not meaning**. "Cannot sign in" and "login fails" share no words, so Jaccard scores them 0.0 even though they describe the same problem. Production tools use **embeddings** (Monday) for this reason. You could also use TF-IDF with cosine similarity from scikit-learn as a middle ground. The selection logic around the similarity function stays the same.
- Dynamic selection only works as well as your **pool**. A pool of reviewed, correct, diverse examples is a valuable team asset. On **Thursday** you will treat curated **sample input/output pairs** as a formal part of an agent's design.

### 11. Few-Shot Chain-of-Thought: Examples That Show Their Reasoning

Some tasks need a few steps of reasoning, not just a label. For these, you can include the **reasoning** in each example, not only the final answer. This is called **few-shot chain-of-thought** prompting. The model then tends to produce its own reasoning in the same steps before giving its answer, which often improves accuracy on multi-step problems, and it also gives you something to review.

A QE example: deciding the expected result for a coupon test using the SAVE10 rule.

```text
Work out the expected order total. Show your reasoning, then the answer.

Order: total $80.00, coupon SAVE10
Reasoning: SAVE10 applies to orders of $50.00 or more. $80.00 >= $50.00, so the
coupon applies. 10% of $80.00 is $8.00. $80.00 - $8.00 = $72.00.
Answer: $72.00

Order: total $49.99, coupon SAVE10
Reasoning: SAVE10 applies to orders of $50.00 or more. $49.99 < $50.00, so the
coupon does not apply. The total is unchanged.
Answer: $49.99

Order: total $50.00, coupon SAVE10
Reasoning:
```

Notice that the two examples sit on either side of the **boundary** (Week 3 BVA), and the new input is exactly on it. The examples demonstrate the comparison step explicitly ("$80.00 >= $50.00"), which is exactly where a careless answer would go wrong. The correct continuation is "$50.00 >= $50.00, so the coupon applies… Answer: $45.00".

Use few-shot chain-of-thought sparingly: it makes outputs (and token bills) longer, and the reasoning text is harder to parse automatically. It is most useful when you want to **review** how the model reached an answer, or when the task requires several calculations or rule checks.

### 12. Three QE Use Cases

#### 12.1 Classifying bug reports

You have already seen this throughout the lesson. It is a natural fit for few-shot prompting because:

- The output is a small set of **labels**, which examples define precisely.
- Teams draw severity boundaries differently, and examples communicate *your* team's boundaries.
- The output is easy to check and to parse.

Use the label-balance check and diverse components, and include at least one "tricky" example (for instance, a cosmetic issue on the checkout page labelled `Minor`).

#### 12.2 Writing test cases in the team's house style

Most teams have a **house style** for manual test cases: an ID scheme, a fixed set of fields, a way of writing steps. Describing it in words is long; one or two examples show it instantly.

```text
Write ONE test case for the requirement below, in exactly the same style as the examples.

<example>
Requirement: Users can log in with a valid email and password.
ID: TC-LOGIN-001
Title: Log in with valid credentials
Preconditions: User account test.user@example.com exists with password Passw0rd!
Steps:
  1. Open the login page.
  2. Enter test.user@example.com in the Email field.
  3. Enter Passw0rd! in the Password field.
  4. Click "Log in".
Expected result: The account dashboard is displayed with the heading "My account".
</example>

<example>
Requirement: Searching for a product shows matching results.
ID: TC-SEARCH-004
Title: Search with a term that has no matches
Preconditions: No product name contains "zzqx".
Steps:
  1. Open the home page.
  2. Enter zzqx in the search box.
  3. Press Enter.
Expected result: The message "No products found" is displayed and no product cards are shown.
</example>

Requirement: Removing an item from the cart updates the cart total.
```

What these two examples teach without a single extra instruction:

- The ID pattern `TC-<AREA>-<number>`.
- Titles that start with a verb and name the specific condition.
- Preconditions that name concrete test data.
- Numbered steps, one action per step, with exact UI labels in quotes.
- An expected result that is **observable** (a specific message or element), not vague ("it works").
- That a negative case (no matches) is a normal part of the suite, not an afterthought.

The two examples are deliberately from **different areas** (login, search) and show **one positive and one negative** case, so the model does not over-copy a single feature or assume every test is a happy path. Generating complete sets of test cases from requirements is covered on **Wednesday**; today's focus is how examples control their style.

#### 12.3 Worked example: acceptance criteria to Gherkin

In Week 6 you wrote BDD scenarios in **Gherkin** (`Feature`, `Scenario`, `Given/When/Then`, `Scenario Outline` with `Examples`). Converting a user story's acceptance criteria into Gherkin is repetitive and pattern-based, which makes it a good few-shot task. Let us build the full prompt step by step.

**Step 1: The instruction.** State the task and the hard rules.

```text
Convert the acceptance criteria into a Gherkin feature.
Rules:
- Use one Scenario per criterion, or a Scenario Outline when criteria differ only by data.
- Write steps from the shopper's point of view ("I").
- Put exact values (amounts, codes, messages) in the steps.
- Output only the Gherkin, with no explanation.
```

**Step 2: Choose examples.** We want examples that show both a plain `Scenario` and a `Scenario Outline`, from features **other than** coupons, so the model learns the structure rather than coupon-specific wording.

```text
<example>
Acceptance criteria:
- Given a registered shopper, logging in with the correct password opens "My account".
- Logging in with a wrong password shows "Invalid email or password".

Gherkin:
Feature: Shopper login

  Scenario: Log in with the correct password
    Given I am a registered shopper with email "test.user@example.com"
    When I log in with password "Passw0rd!"
    Then I should see the "My account" page

  Scenario: Log in with a wrong password
    Given I am a registered shopper with email "test.user@example.com"
    When I log in with password "wrong-pass"
    Then I should see the message "Invalid email or password"
</example>

<example>
Acceptance criteria:
- Search is case-insensitive: "Mug", "mug" and "MUG" all return the product "Coffee Mug".

Gherkin:
Feature: Product search

  Scenario Outline: Search ignores letter case
    Given the catalogue contains the product "Coffee Mug"
    When I search for "<term>"
    Then the results should include "Coffee Mug"

    Examples:
      | term |
      | Mug  |
      | mug  |
      | MUG  |
</example>
```

**Step 3: The new input.** The acceptance criteria for our running example:

```text
Acceptance criteria:
- SAVE10 gives 10% off orders of $50.00 or more.
- SAVE10 does not change orders below $50.00.
- An unknown coupon code shows "Coupon code not recognised".

Gherkin:
```

The prompt ends with `Gherkin:`, continuing the pattern of the examples.

**Step 4: A typical response.** A capable model would typically return something like the following. (This is an illustrative response written for this lesson, not output from a live model run.)

```gherkin
Feature: Apply coupon at checkout

  Scenario Outline: SAVE10 is applied only to orders of $50 or more
    Given my cart total is <total>
    When I apply the coupon "SAVE10"
    Then the order total should be <new_total>

    Examples:
      | total  | new_total |
      | 49.99  | 49.99     |
      | 50.00  | 45.00     |
      | 80.00  | 72.00     |

  Scenario: Apply an unknown coupon code
    Given my cart total is 80.00
    When I apply the coupon "BOGUS"
    Then I should see the message "Coupon code not recognised"
```

Look at what the examples achieved:

- The model used a `Scenario Outline` for the two data-driven criteria, exactly as the search example demonstrated.
- It used first-person steps and quoted exact values, as both examples did.
- It produced only Gherkin, with no explanation, matching the examples.

**Step 5: Review it.** Format being right is not the same as content being right. Check the content against the requirement, using your Week 3 skills:

- **Boundaries:** 49.99 (just below), 50.00 (on the boundary) and 80.00 (well above) are all present. Good BVA coverage.
- **Arithmetic:** 10% of 50.00 is 5.00, so 45.00 is correct; 10% of 80.00 is 8.00, so 72.00 is correct.
- **Gaps:** Is the coupon code case-sensitive (`save10`)? What about an empty code? The acceptance criteria do not say, so the model (correctly) did not invent behaviour. These are questions to take back to the product owner, not things to guess.

A tiny bit of code can automate the most basic **shape** check: are the Gherkin keywords present at all?

```python
# check_gherkin_shape.py
REQUIRED_KEYWORDS = ("Feature:", "Scenario", "Given ", "When ", "Then ")

def check_gherkin_shape(text):
    """Return the Gherkin keywords that are missing from the model's reply."""
    return [kw for kw in REQUIRED_KEYWORDS if kw not in text]

reply = """Feature: Apply coupon at checkout

  Scenario Outline: SAVE10 is applied only to orders of $50 or more
    Given my cart total is <total>
    When I apply the coupon "SAVE10"
    Then the order total should be <new_total>

    Examples:
      | total  | new_total |
      | 49.99  | 49.99     |
      | 50.00  | 45.00     |
      | 80.00  | 72.00     |
"""
print("Missing keywords:", check_gherkin_shape(reply))
print("Missing keywords:", check_gherkin_shape("Test 1: apply SAVE10 and check total"))
```

Output:

```text
Missing keywords: []
Missing keywords: ['Feature:', 'Scenario', 'Given ', 'When ', 'Then ']
```

How it works: `REQUIRED_KEYWORDS` is a **tuple** of strings that every valid reply must contain. The list comprehension keeps each keyword for which `kw not in text` is true, so the function returns the **missing** keywords; an empty list means the shape looks right. The trailing spaces in `"Given "`, `"When "` and `"Then "` make sure we match the keywords and not, for example, the word "Thenceforth". The triple-quoted string `"""..."""` lets the sample reply span many lines.

This check catches a reply that ignored the format entirely (the second call), but it cannot tell whether 45.00 is the right number. That still needs a human, or a proper test run. More rigorous ways to validate AI output are covered later this week: human validation on **Wednesday**, and automated validation scripts on **Friday**.

### 13. When Zero-Shot Is Enough (and When Few-Shot Is Not)

Few-shot prompting is not always the right tool.

**Zero-shot is often enough when:**

- The task is common and well understood by models (summarise a log, explain a stack trace, translate a sentence).
- The output format is simple and easy to describe ("Answer yes or no").
- You are exploring and do not yet know what good output looks like. Start zero-shot, look at the results, then add examples to fix what you do not like.
- You want **variety** (for example, brainstorming unusual test ideas). Examples can narrow the model's output towards their pattern, which reduces creativity.

**Few-shot is worth it when:**

- The output must follow a specific **format** that code will parse.
- The task uses **your own labels or conventions** that the model cannot know (severity rules, ID schemes, house style).
- Zero-shot results are **inconsistent** from run to run.
- The decision boundaries are **subtle** and easier to show than to describe.

**Few-shot may not be enough when:**

- The task needs knowledge the model does not have (your private business rules, which only appear if you supply them as context; see today's lesson on **specificity and context**).
- The task needs long, complex reasoning; few-shot chain-of-thought helps, but some problems still fail.
- You need the behaviour across thousands of very different inputs and examples alone cannot cover the variety. Organisations then consider **fine-tuning** (actually retraining the model on many examples, which changes the weights, as in Monday's supervised learning). Fine-tuning is outside the scope of this week.

A good default workflow is: **instruction first, then zero-shot test, then add examples to fix specific problems**, re-testing each time.

### 14. Connecting to Project 2

For today's exercise (a prompt library for test design and debugging), consider adding at least these few-shot prompts, using examples from your own Project 2 e-commerce application:

- **Bug triage prompt** with 3 to 5 balanced, reviewed classifications from your app's components (login, search, cart, checkout).
- **House-style test case prompt** with one positive and one negative example from different features.
- **Acceptance criteria to Gherkin prompt** with one `Scenario` example and one `Scenario Outline` example.

Store the examples as data (for example, a Python list of dictionaries or a separate file) in your Project 2 repository, under version control, so they can be reviewed and updated when the application changes. On **Thursday**, you will see how prompts and sample input/output pairs become formal building blocks of a QA agent.

---

## Practice Exercises

1. **Zero to few.** Write a zero-shot prompt that asks for a single test case title for "Add a product to the cart". Then write a one-shot and a three-shot version using house-style titles of your own. If you have access to an approved AI tool, compare the three outputs and write two sentences on what changed.

2. **Fix the example set.** The following examples are intended for classifying bug components. List every problem you can find (use the checklist in Section 5), then rewrite the set.

   ```text
   Bug: Pay button broken -> component: checkout
   Bug: Payment page slow -> Component: Checkout
   Bug: Coupon SAVE10 accepted on $20 order -> Component: Checkout
   Bug: Card charged twice -> Component: Checkout
   ```

3. **Compute Jaccard by hand.** Calculate the Jaccard similarity between "Cart total is wrong after removing an item" and "Removing an item from the cart leaves its price in the total". Then run `jaccard()` from Section 10 to check your answer.

4. **Extend the selector.** Modify `select_balanced` so it returns the top **two** examples per label instead of one. Then use `check_label_balance` to confirm the result is balanced.

5. **Few-shot Gherkin.** Write a few-shot prompt (two examples) that converts acceptance criteria for "Shoppers can change the quantity of an item in the cart (1 to 10)" into Gherkin. Make sure your examples come from different features and that at least one shows a `Scenario Outline`. Write down which boundary values you expect to see in a good answer.

6. **Test the order effect.** Using `build_few_shot_prompt` from Section 4, write a short script that generates the same prompt with the examples in every possible order (hint: `itertools.permutations`). How many different prompts do three examples produce? Why would you send all of them to a model when testing an important prompt?

---

## Knowledge Check

1. What does "shot" mean in zero-shot, one-shot and few-shot prompting?
2. When a model follows the examples in a few-shot prompt, have its weights changed? Explain how this differs from supervised training.
3. Give three things that examples communicate more effectively than written instructions.
4. Your prompt's five examples are labelled Major, Major, Major, Major, Critical. Name two biases this could introduce and how you would fix them.
5. Every example test case in your prompt uses an $80 order and the SAVE10 coupon. You ask for gift card test cases and the output mentions SAVE10. What is this risk called, and how do you reduce it?
6. Why does `select_examples` in Section 10 score "Cannot sign in" and "Login fails" as completely dissimilar, and what would a production system use instead?
7. Give one situation where zero-shot prompting is the better choice.
8. In the Gherkin worked example, the shape check returned an empty list. Does that mean the scenarios are correct? Explain.

<details>
<summary>Answers</summary>

1. "Shot" means a worked example (an input with its desired output) included in the prompt. Zero-shot has none, one-shot has one and few-shot has several (typically 2 to 5).
2. No. Few-shot prompting is in-context learning: the examples exist only in the context window for that request, and the model's weights are unchanged. Supervised training updates the weights using many labelled examples, so the change is permanent; few-shot behaviour disappears on the next request unless the examples are sent again.
3. Any three of: output format, style and tone, level of detail (granularity), exact label values and spelling, decision boundaries between labels, and implicit conventions such as ID schemes.
4. Majority-label bias (most examples are Major, pulling answers towards Major) and recency bias (the last example, Critical, may have extra influence). Fix by balancing labels across Critical, Major and Minor, varying label positions, and testing different orders.
5. Over-copying (anchoring on surface details). Reduce it by making examples diverse: different features, amounts and data, and by stating in the instruction that the examples show style only.
6. Jaccard compares exact words, and the two phrases share no words. Production systems typically use embeddings (Monday), which place texts with similar meaning close together even when the words differ.
7. Any of: a common, well-understood task with a simple output format; early exploration before you know what good output looks like; or when you want varied, creative output (for example, brainstorming unusual test ideas).
8. No. The shape check only confirms that Gherkin keywords are present. It cannot verify that expected values (such as 45.00 for a $50.00 order) are correct or that all requirements are covered. That needs human review or real test execution (covered on Wednesday and Friday).

</details>

---

## Glossary

- **Shot:** A worked example (input plus desired output) included in a prompt.
- **Zero-shot prompting:** Prompting with instructions only, no examples.
- **One-shot prompting:** Prompting with exactly one example.
- **Few-shot prompting:** Prompting with several examples, typically 2 to 5. Also called **multishot prompting**.
- **In-context learning:** A model's ability to perform a task from instructions and examples in its input, without any change to its weights.
- **Delimiter:** A marker (heading, label, tag, quotes) that separates parts of a prompt, such as examples from the real input.
- **Recency bias:** The tendency of examples near the end of a prompt to have more influence on the answer.
- **Majority-label bias:** The tendency of the model to favour the label that appears most often in the examples.
- **Over-copying (anchoring):** The model copying incidental surface details from examples into new outputs.
- **Example leakage:** The model returning an example's content instead of a new answer.
- **Dynamic example selection:** Choosing, for each new input, the most relevant examples from a larger pool.
- **Jaccard similarity:** Number of shared distinct words divided by the number of distinct words in either text; ranges from 0.0 to 1.0.
- **Few-shot chain-of-thought:** Few-shot prompting in which each example includes its step-by-step reasoning, not just the answer.
- **Fine-tuning:** Further training of a model on task-specific examples, which changes its weights.
- **House style:** A team's agreed conventions for writing artefacts such as test cases and bug reports.

---

## Summary

- **Few-shot prompting** places worked input → output examples in the prompt. Zero-shot uses none, one-shot uses one, few-shot uses several.
- It works through **in-context learning**: the model continues the pattern it sees, and **no weights change**. The examples must be sent with every request.
- Examples **show** format, style, granularity, labels, decision boundaries and unwritten conventions far more efficiently than instructions can **tell** them. Use instructions and examples together, and keep them consistent.
- A good few-shot prompt has an **instruction**, **examples**, the **new input** and consistent **delimiters**. It can be written inline or as **user/assistant message pairs**.
- Good examples are **representative, diverse, correct, consistently formatted, label-balanced**, include **edge cases** and reflect **realistic difficulty**.
- **Two to five** examples is typical; more examples bring diminishing returns and cost tokens on every request.
- Watch for **recency bias** and **majority-label bias**, **over-copying**, **example leakage** and **outdated examples**. Version-control and review your examples like test code.
- **Dynamic example selection** picks the most relevant examples per input; check the result for **label balance**.
- **Few-shot chain-of-thought** shows reasoning in the examples, useful for multi-step rules such as boundary checks.
- In QE, few-shot prompting is ideal for **bug classification**, **house-style test cases** and **acceptance criteria to Gherkin**. Correct format is not correct content: always review the output.

---

## Additional Resources

- Anthropic, *Prompting best practices* (see the "Use examples effectively" section on relevant, diverse and structured examples): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- DAIR.AI Prompt Engineering Guide, *Few-Shot Prompting* (worked examples, findings on labels and format, and limitations): https://www.promptingguide.ai/techniques/fewshot
- Brown et al., *Language Models are Few-Shot Learners* (the 2020 GPT-3 paper that introduced in-context few-shot learning at scale): https://arxiv.org/abs/2005.14165
