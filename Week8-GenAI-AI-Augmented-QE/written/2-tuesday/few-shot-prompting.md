# Few-Shot Prompting

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** the difference between zero-shot, one-shot and few-shot prompting, and what in-context learning is.
- **Build** a few-shot prompt whose examples show the exact format, labels and style you want.
- **Choose** good examples: varied, correct, short and similar to the real inputs.
- **Explain** how the number and order of examples can bias the answer, and how to reduce that bias.
- **Check** a few-shot prompt's examples and its replies with a short script.

---

## Why This Matters

In *Format Locking*, you described the format in words: field names, types, a count. Sometimes words are not enough. The model still adds bold text, a second sentence or a 20-word reason. **Few-shot prompting** solves this by **showing** the answer instead of describing it.

Few-shot prompting is one of the most widely used techniques in practice. The term became well known through the 2020 GPT-3 paper, *Language Models are Few-Shot Learners*, which showed that a large model could do a new task from a handful of examples written into the prompt, with no further training ([Brown et al., 2020](https://arxiv.org/abs/2005.14165)).

There is a catch, and testers should know it. Research on few-shot prompting has found that the choice of examples, and even their **order**, can change results a lot. One study found two biases in particular: models lean towards the answer that appears **most often** among the examples, and towards the answer that appears **near the end** ([Zhao et al., *Calibrate Before Use*, 2021](https://arxiv.org/abs/2102.09690)). A few-shot prompt is only as good as its examples.

For QE, few-shot prompting is how you teach an AI your team's way of doing things: your severity scale, your bug-title style, your test-case format. On Thursday and Friday, your QA agent uses the same idea, with reviewed example pairs.

> **Using this with the handout:** this lesson goes deeper into **Handout 03, Topic 4**. It uses the same severity classifier, the same three examples, the same Safari login bug and the same `prompts.txt` entry, `=== Severity classifier - few-shot v1 ===`.

---

## The Concept

### 1. Zero-Shot, One-Shot and Few-Shot

The "shots" are worked examples inside the prompt:

| Name | Examples in the prompt | When to use it |
|---|---|---|
| **Zero-shot** | None, just instructions | The task and format are easy to describe |
| **One-shot** | One example | You need to show a format once |
| **Few-shot** | Usually 2–5 examples | Labels, format or style are hard to describe but easy to show |

Each example is a pair: an **input** and the **exact output** you want for it. The model then sees a new input, and continues the pattern.

**An everyday analogy: training a new colleague to fill in a form.** You could explain every field in a paragraph. Or you could hand them three forms already filled in correctly, one for each kind of case, and say "do this one the same way". Most people learn faster from the filled-in examples. So do language models.

### 2. In-Context Learning: Learning Without Retraining

When a model follows the pattern in your examples, it has not been retrained. None of its weights change. It picks up the pattern from the text in its context window, for this conversation only. This is called **in-context learning**.

Two consequences follow:

- **It is temporary.** Start a new chat without the examples, and the pattern is gone. That is why you save few-shot prompts **with** their examples in `prompts.txt`.
- **It costs tokens.** Every example takes up space in the context window, every time you send the prompt.

Why does it work? Recall the generation loop from *Generative AI Concepts*. After three examples that all end with a line like `Severity: Low | Reason: cosmetic text issue only`, the most likely continuation after the next `Bug:` line is another line in exactly that shape. The examples make the format the most probable text.

### 3. Why Examples Work: "Show, Don't Tell"

Describing a format leaves room for interpretation. Showing it does not. Compare:

- **Told:** "Reply with one line only, in this format: Severity: \<level\> | Reason: \<max 10 words\>." The model may still add bold, write "**Severity:** High", or explain itself afterwards.
- **Shown:** three complete examples, each a single plain line in that exact shape. The model now has concrete evidence of what "one line" and "max 10 words" look like.

Examples also teach things that are hard to put into words:

- **Where the boundaries between labels are.** What separates "High" from "Critical" on your team? Examples show it.
- **Tone and length.** Short, factual reasons, not essays.
- **Domain style.** Your team's way of writing titles, steps or test names.

### 4. Worked Example: A Bug Severity Classifier

**Goal:** the AI should classify a bug report's severity and reply in **one exact line**, so a script could read it. The handout compares three steps, each in a new chat.

#### Step 1: Zero-shot, no format

```text
You are a QA lead. Classify the severity of this bug report as Critical, High, Medium or Low.

Bug: Login button does nothing on Safari; users cannot sign in
```

You probably get a correct-sounding severity, but in the model's own format: a heading, a paragraph of reasoning, maybe a table. Each tool, and each run, formats it differently. A script could not read it reliably.

#### Step 2: Zero-shot, with a described format

```text
You are a QA lead. Classify the severity of this bug report as Critical, High, Medium or Low.
Reply with one line only, in this format: Severity: <level> | Reason: <max 10 words>

Bug: Login button does nothing on Safari; users cannot sign in
```

Better, but models still drift: bold text, a second sentence, a 20-word reason. Describing the format is not always enough.

#### Step 3: Few-shot, with labelled examples

```text
You are a QA lead. Classify the severity of each bug report as Critical, High, Medium or Low.
Reply with one line only, in this format: Severity: <level> | Reason: <max 10 words>

### Example 1
Bug: Checkout crashes when a coupon is applied; no order can be placed
Severity: Critical | Reason: blocks every purchase

### Example 2
Bug: SAVE10 not applied to a $50.00 order; total stays $50.00
Severity: High | Reason: customer is overcharged at the boundary

### Example 3
Bug: Coupon error message has a spelling mistake
Severity: Low | Reason: cosmetic text issue only

### Now classify this one
Bug: Login button does nothing on Safari; users cannot sign in
```

The kind of reply to expect, **illustrative** and written for the handout:

```text
Severity: Critical | Reason: users on Safari cannot sign in at all
```

#### Comparing the three steps

| Step | Format followed? | Why |
|---|---|---|
| 1: zero-shot, no format | Rarely | Nothing says what shape to use |
| 2: zero-shot, described format | Often, but drifts | Words leave room for interpretation |
| 3: few-shot | Most reliably | The examples **are** the format specification |

Is "Critical" right? It is defensible: nobody on Safari can sign in, which blocks every Safari user from buying anything. "High" is also defensible if Safari is a small share of your users. That is a judgement for your team, and it is exactly the kind of judgement your examples should teach. If your team would call this "High", you need an example that shows a browser-specific blocker labelled "High".

### 5. Anatomy of a Few-Shot Prompt

Look at how the Step 3 prompt is built. Each part has a job:

| Part | In the prompt | Job |
|---|---|---|
| **Instruction** | "Classify the severity … as Critical, High, Medium or Low." | States the task and the allowed labels |
| **Format line** | "Reply with one line only, in this format: …" | Describes the shape (the examples then show it) |
| **Examples** | Three `Bug:` / `Severity:` pairs | Show the format, the labels and the style |
| **Delimiters** | `### Example 1`, `### Now classify this one` | Separate the examples from the real input (from *Specificity and Context*) |
| **The new input** | The final `Bug:` line, with nothing after it | Makes the next step obvious: write the `Severity:` line |

The last row matters more than it looks. The prompt ends right after the new bug's `Bug:` line. In every example, a `Bug:` line is followed by a `Severity:` line, so the most likely continuation is a `Severity:` line. Without the "Now classify this one" heading, some models classify the examples again as well.

### 6. Choosing Good Examples

The model copies **everything** in your examples: the format, the length, the tone, and the **mistakes**. So choose them with care:

| Rule | Why | In the handout's prompt |
|---|---|---|
| **Cover different answers** | Three "High" examples teach "everything is High" | Critical, High and Low |
| **Keep them correct** | A wrong label in an example becomes a wrong pattern | Each label fits the team's scale |
| **Keep them short** | Long examples waste tokens and invite long answers | One line each |
| **Make them look like real inputs** | The model generalises from what it sees | Real-looking bug titles from our shop |
| **Keep them consistent** | Mixed formats teach a mixed format | Every answer is `Severity: … \| Reason: …` |
| **Do not make the new input a copy of an example** | The model may copy the example's answer | The Safari bug is unlike all three |

Notice that the handout's prompt has **no Medium example**. That is a small gap. A bug that sits naturally at "Medium" may get pushed up or down, because the model has never seen what Medium looks like on your team. The Practice Exercises ask you to fix it.

### 7. How Many Examples?

More examples are not always better:

- **One** example is often enough to fix a **format**.
- **Two to five** examples usually work well for **labels**, as long as they cover the different labels.
- **Many** examples cost more tokens on every call, make the prompt harder to maintain, and add more chances for a wrong or inconsistent example to slip in.

A practical approach: start with one example per label, test the prompt on several new inputs, and add an example only when you see a specific kind of mistake. Each added example should **fix a problem you observed**, just like adding a test for a bug you found.

**Work out the cost by hand.** Each example in the handout's prompt is about 20 words, which is roughly 27 tokens, using Monday's rule of thumb (100 tokens ≈ 75 words). Three examples add about 80 tokens to every request. Classify 1,000 bug reports, and the examples alone add about 80,000 tokens. Ten longer examples of 60 words each would add about 800 tokens per request, or 800,000 over the same 1,000 bugs. Hosted models charge per token, so every example you add is a small cost paid on every single call. That is one more reason to add examples only when they fix something.

### 8. Order Matters: Recency and Majority-Label Bias

The *Calibrate Before Use* study described two biases that every tester should know:

- **Majority-label bias:** if most examples share one label, the model leans towards that label for new inputs.
- **Recency bias:** the model leans towards the label of the **last** examples in the prompt.

**Work it by hand.** Suppose a prompt has four examples in this order: High, High, High, Low. Count the labels: High appears 3 times out of 4, so majority-label bias pushes towards High. The last example is Low, so recency bias pushes towards Low. A new borderline bug could be labelled differently for reasons that have nothing to do with the bug.

Here is what majority-label bias can look like in practice. Imagine a severity prompt whose three examples are all labelled High. You classify three new bugs: a typo on the help page, a crash at checkout, and a slow search. The replies come back (**illustrative**, written for this lesson):

```text
Severity: High | Reason: incorrect text visible to customers
Severity: High | Reason: checkout crash affects orders
Severity: High | Reason: slow search frustrates users
```

Every reason sounds plausible on its own, which is what makes the problem easy to miss. Only when you look at the **pattern** across several answers do you notice that a typo and a checkout crash got the same severity. A tester who reviews AI output one answer at a time can miss a bias like this; looking at a batch of answers together reveals it.

How to reduce the effect:

- **Balance the labels.** Use roughly one example per label.
- **Mix the order.** Avoid putting all examples of one label together, or always ending on the same label.
- **Test it.** Classify a few inputs whose correct label you already know, then re-order the examples and classify them again. If the answers change, the prompt is fragile.

### 9. Checking a Few-Shot Prompt with Code

The rules in sections 6 and 8 are concrete enough to check. This script checks that every example follows the format, reports the label balance and the last label, and reads a reply using the **same** format rule:

```python
# few_shot_check.py
import re
from collections import Counter

LINE = re.compile(r"^Severity: (Critical|High|Medium|Low) \| Reason: (.+)$")

examples = [
    ("Checkout crashes when a coupon is applied; no order can be placed",
     "Severity: Critical | Reason: blocks every purchase"),
    ("SAVE10 not applied to a $50.00 order; total stays $50.00",
     "Severity: High | Reason: customer is overcharged at the boundary"),
    ("Coupon error message has a spelling mistake",
     "Severity: Low | Reason: cosmetic text issue only"),
]

# 1. Every example answer must follow the format exactly: the examples ARE the spec
for bug, answer in examples:
    assert LINE.match(answer), f"Example breaks the format: {answer!r}"

# 2. Balance: how often does each label appear, and which comes last?
labels = [LINE.match(answer).group(1) for _, answer in examples]
print("Label counts:", dict(Counter(labels)))
print("Last example label:", labels[-1])

# 3. Read a reply with the same rule
def read_severity(reply):
    m = LINE.match(reply.strip())
    if not m:
        return None, "reply does not match the format"
    words = len(m.group(2).split())
    return m.group(1), ("ok" if words <= 10 else f"reason has {words} words")

print(read_severity("Severity: Critical | Reason: users on Safari cannot sign in at all"))
print(read_severity("**Severity:** Critical | Reason: users cannot sign in"))
```

Output:

```text
Label counts: {'Critical': 1, 'High': 1, 'Low': 1}
Last example label: Low
('Critical', 'ok')
(None, 'reply does not match the format')
```

What to notice:

- `LINE` is a **regular expression** (Week 1) that describes the one allowed line. `(Critical|High|Medium|Low)` accepts only the four labels; `\|` matches a literal `|`, which otherwise means "or".
- Check 1 tests the **examples themselves**. A typo in an example would be copied by the model, so the examples deserve testing as much as the replies.
- `Counter(labels)` counts each label. Here the labels are balanced, apart from the missing Medium, and the last one is Low.
- `read_severity` uses the **same** rule as check 1. The second reply fails because of the bold `**`, a typical kind of drift from *Format Locking*.
- The 10-word limit is checked separately. The first reply's reason has 8 words, so it passes.

The same rule now serves three purposes: it defines the format, it checks the examples, and it checks the replies. On Thursday you will meet a more powerful way to write such rules for whole JSON documents, using JSON Schema.

### 10. Risks of Few-Shot Prompting

| Risk | What happens | How to reduce it |
|---|---|---|
| **Copying mistakes** | A wrong label or typo in an example is repeated | Check the examples, as in section 9 |
| **Over-copying wording** | Answers reuse phrases from the examples, even when they do not fit | Use varied examples; keep reasons short and specific |
| **Label bias** | Answers lean towards common or recent labels | Balance and mix the examples (section 8) |
| **Missing cases** | Inputs unlike any example are handled badly | Cover each label and each common kind of input |
| **Stale examples** | The team's rules change, but the examples do not | Version the prompt in `prompts.txt`, and review examples when rules change |
| **Leaking real data** | Real bug reports with customer data used as examples | Use made-up, realistic examples |

### 11. Reusing a Few-Shot Prompt

In the handout's Step 4, you keep the instruction and examples the same, and replace only the **last** bug:

```text
Bug: Footer link to Privacy Policy opens the wrong page
```

The kind of reply to expect is `Severity: Low | Reason: wrong link, no impact on purchases`, or possibly Medium.

This split matters: the prompt now has a **fixed part** (instruction and examples) and a **changing part** (the new bug). A prompt built this way is the idea behind a **prompt template**, which you will study on Thursday and build for your agent. For now, notice that every bug you classify with this prompt is judged against the **same** examples, which is what makes the answers consistent from one bug to the next.

### 12. Few-Shot Beyond Classification

Few-shot prompting works for many QE tasks:

| Task | What the examples show |
|---|---|
| **Bug titles in your team's style** | Input: a rough description. Output: `[Checkout] SAVE10 not applied at $50.00` |
| **Test-case names** | Input: an AC. Output: `test_exactly_50_gets_discount` |
| **Gherkin steps** | Input: a test idea. Output: Given/When/Then lines in your team's wording |
| **Log-line labels** | Input: an error line. Output: `TIMEOUT`, `ASSERTION` or `ENVIRONMENT` |

In every case, the same rules apply: cover the different kinds of answer, keep the examples correct and consistent, and check both the examples and the replies.

Take the test-name row as a short worked case. Three examples could be:

```text
AC: SAVE10 gives 10% off a subtotal of $50.00 or more.  ->  test_save10_discount_at_or_above_50
AC: Subtotals under $50.00 are unchanged.               ->  test_subtotal_under_50_is_unchanged
AC: Unknown codes show "Coupon code not recognised".    ->  test_unknown_code_shows_error_message
```

From these, the model picks up the conventions without being told: the `test_` prefix that pytest needs (Week 4), lower-case words joined by underscores, and a name that says what is checked rather than how. Describing all three rules in words would take longer, and be easier to misread, than showing them.

### 13. Few-Shot as Chat Messages

In *Prompt Engineering Principles*, you saw that a request is really a list of messages with roles: system, user and assistant. When developers write few-shot prompts in code, they often place each example as a **pair of messages**: a user message with the input, followed by an assistant message with the ideal answer. The new input then goes in a final user message:

```python
messages = [
    {"role": "system", "content": "You are a QA lead. Classify severity as Critical, High, Medium or Low. "
                                  "Reply with one line: Severity: <level> | Reason: <max 10 words>"},
    {"role": "user", "content": "Bug: Checkout crashes when a coupon is applied; no order can be placed"},
    {"role": "assistant", "content": "Severity: Critical | Reason: blocks every purchase"},
    {"role": "user", "content": "Bug: Coupon error message has a spelling mistake"},
    {"role": "assistant", "content": "Severity: Low | Reason: cosmetic text issue only"},
    {"role": "user", "content": "Bug: Login button does nothing on Safari; users cannot sign in"},
]
```

The model sees what looks like a conversation in which it has **already** answered twice in exactly the right format, so answering the third time in the same format is very likely. This layout keeps the examples clearly separate from the real input, without needing `###` headings. In a chat app, you cannot write assistant messages yourself, so the single-message layout from the handout is the practical choice there. Both layouts teach the same pattern.

### 14. A Few-Shot Checklist

Before relying on a few-shot prompt, check:

- [ ] **Need:** did zero-shot fail in a way that examples can fix?
- [ ] **Coverage:** is there at least one example of each label or kind of answer?
- [ ] **Correctness:** has someone checked every example's answer?
- [ ] **Consistency:** does every example follow the format exactly?
- [ ] **Balance and order:** are the labels balanced, and is the order mixed?
- [ ] **Separation:** is the new input clearly marked, with nothing after it?
- [ ] **Safety:** are the examples made up, with no real customer data?
- [ ] **Tested:** have you tried it on inputs with known answers, and in a different order?

### 15. When Zero-Shot Is Enough, and When Few-Shot Is Not

Start with zero-shot. Move to few-shot only when you see a problem that examples can fix:

- **Zero-shot is enough** when the format is simple and the task is common, such as "list 5 test ideas for this AC".
- **Few-shot helps** when the format keeps drifting, when labels need your team's definitions, or when you need a particular style.
- **Few-shot is not enough** when the model lacks the **facts**. Examples teach a pattern, not your requirements. If the AI does not know your coupon rules, show it the rules (context), not more examples.

---

## Practice Exercises

1. **Add the missing label (paper, 10 min).** Write a **Medium** example for the severity classifier, in the exact format. Decide where to put it among the three existing examples, and explain your choice using section 8.

2. **Spot the bad examples (paper, 10 min).** A few-shot prompt has these examples: `High | crash on login`, `High | checkout slow`, `High | typo in footer`, and the format line says `Severity: <level> | Reason: <max 10 words>`. List every problem you can find, using sections 6 and 8.

3. **Test the order (AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** take the handout's Step 3 prompt, add your Medium example, and classify these three bugs in separate new chats: (a) *"Search results load in 8 seconds instead of 2"*, (b) *"Order confirmation email has the wrong logo"*, (c) *"Applying SAVE10 twice gives 20% off"*. Then move your Medium example to the end, and classify the same three again.
   - **Review:** did any severity change when only the order changed?
   - **Run:** add your Medium example to `examples` in `few_shot_check.py`, and run each reply through `read_severity`.
   - **Record:** write two sentences on how sensitive this prompt is to order, and save the final version as `=== Severity classifier - few-shot v2 ===`.

4. **Few-shot bug titles (AI tool, 15 min).** Write a few-shot prompt with three examples that turns a rough description into a bug title in the style `[Area] What is wrong, with the key value`. Test it on two new descriptions, and check that each title follows the pattern.

---

## Knowledge Check

1. What is the difference between zero-shot, one-shot and few-shot prompting?

<details><summary>Answer</summary>

The number of worked examples in the prompt: none, one, or a few (usually 2–5).

</details>

2. What is in-context learning, and is it permanent?

<details><summary>Answer</summary>

The model following a pattern shown in the prompt, without any retraining. It is not permanent: it lasts only for that conversation, while the examples are in the context window.

</details>

3. Why did the few-shot prompt follow the format more reliably than the described format in Step 2?

<details><summary>Answer</summary>

The examples show exactly what the format looks like, so the most likely continuation after a new `Bug:` line is a line in that exact shape. A description leaves more room for interpretation.

</details>

4. A prompt's examples are labelled High, High, High, Low. What two biases might affect a new answer?

<details><summary>Answer</summary>

Majority-label bias (towards High, the most common label) and recency bias (towards Low, the last label).

</details>

5. Why should you check the examples themselves, not only the replies?

<details><summary>Answer</summary>

The model copies the examples, including their mistakes. A wrong label or a format typo in an example becomes a wrong pattern in the replies.

</details>

6. Three examples add about 80 tokens to each request. Why does that matter when you classify 1,000 bugs?

<details><summary>Answer</summary>

The examples are sent with every request, so they add about 80,000 tokens in total. Hosted models charge per token, so each extra example is a cost paid on every call.

</details>

7. When is few-shot prompting not enough?

<details><summary>Answer</summary>

When the model lacks the facts, such as your requirements. Examples teach a pattern, not the rules; for missing facts, add context.

</details>

---

## Glossary

- **Shot:** one worked example (an input and its exact output) inside a prompt.
- **Zero-shot / one-shot / few-shot:** prompting with no examples / one example / a few examples.
- **In-context learning:** a model following a pattern shown in the prompt, without retraining.
- **Example pair:** an input together with the exact output you want for it.
- **Label:** one of a fixed set of answers, such as Critical, High, Medium or Low.
- **Majority-label bias:** leaning towards the label that appears most often among the examples.
- **Recency bias:** leaning towards the label of the last examples.
- **Regular expression:** a pattern for matching text, such as one allowed answer line.
- **Fixed part / changing part:** the parts of a reusable prompt that stay the same / change for each input.
- **Prompt template:** a prompt with a fixed part and slots for the changing part (covered on Thursday).
- **Chat-message layout:** placing each example as a user message followed by an assistant message, as developers often do in code.
- **Fragile prompt:** a prompt whose answers change when something unimportant, such as example order, changes.

---

## Summary

- **Few-shot prompting shows the answer instead of describing it.** It is the best tool when format, labels or style are hard to put into words.
- **The model learns from the examples for this conversation only**: in-context learning, with no retraining.
- **The examples are the specification.** Keep them varied, correct, short, consistent and realistic.
- **Order and balance matter.** Majority-label and recency bias can change answers, so balance the labels, mix the order and test it.
- **Check the examples and the replies with the same rule.**
- **Examples teach patterns, not facts.** For missing requirements, add context, not more examples.

---

## Additional Resources

- Brown et al., *Language Models are Few-Shot Learners* (the GPT-3 paper that popularised few-shot prompting): https://arxiv.org/abs/2005.14165
- Zhao et al., *Calibrate Before Use: Improving Few-Shot Performance of Language Models* (majority-label and recency bias): https://arxiv.org/abs/2102.09690
- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API* (showing the output format with examples, and moving from zero-shot to few-shot): https://help.openai.com/en/articles/6654000
