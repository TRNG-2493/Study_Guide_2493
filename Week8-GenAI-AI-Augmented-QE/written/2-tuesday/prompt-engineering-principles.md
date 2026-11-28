# Prompt Engineering Principles

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what a prompt is, and why the prompt is the only thing steering an AI assistant's answer.
- **Build** a prompt from its five parts: role, task, context, constraints and output format.
- **Describe** the difference between system, user and assistant messages.
- **Apply** the prompt-refinement loop: write, run, check, change one thing, run again.
- **Check** an AI's answer against your own constraints, by hand and with a short script.

---

## Why This Matters

On Monday you learned how an LLM works: it predicts likely text, one token at a time, based on **everything in front of it**. That has a direct consequence for anyone using an AI assistant: **the prompt is the only steering wheel you have.** The model cannot read your mind, your Jira board or your requirements document, unless you put them in the prompt.

Prompt engineering is also a testing skill. A good prompt is like a good bug report: clear, complete and easy to act on. Improving a prompt is like debugging a test: run it, compare the result with what you expected, change one thing, run it again. Testers already have the habits this needs.

This week's Epic ends with you building a QA agent on Friday. An agent is, at its core, a carefully written prompt with checks around it. Everything you learn today goes straight into that agent.

AI providers agree that clear, specific prompts matter. Anthropic's documentation gives a simple test, which it calls the golden rule of clear prompting: show your prompt to a colleague who knows little about the task, and see whether they can follow it. If they are confused, the model probably will be too ([Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)).

> **Using this with the handout:** this lesson goes deeper into **Handout 03, Topic 1**. It uses the same story (US-205), the same five-step prompt for AC1, and the same `prompts.txt` entry, `=== AC test cases - v1 ===`.

---

## The Concept

### 1. What Is a Prompt? What Is Prompt Engineering?

A **prompt** is the text you give an AI assistant: your question, your instructions, and any material you paste in, such as a user story or an error message.

**Prompt engineering** is the skill of writing prompts that **reliably** get useful, correct and well-formatted answers. The word "reliably" matters. Anyone can get a good answer once by luck. Prompt engineering is about getting good answers again and again, from different runs and even different tools.

Here is the running example for today, from the handout:

```text
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

An **AC** (acceptance criterion) is one rule the feature must follow. It is the same SAVE10 rule you tested on Monday, now written as a full user story.

### 2. How an LLM "Reads" a Prompt

Three ideas from Monday's *Generative AI Concepts* explain almost every prompting principle:

1. **It predicts likely text.** If your prompt is vague, the most likely continuation is a generic answer. "Write test cases for a coupon feature" is most likely followed by the kind of coupon tests that appear all over the internet: expiry dates, minimum spends, one per customer. None of those are in US-205.
2. **It only knows what is in its context window.** If the acceptance criteria are not in the prompt, the model does not have them. It will fill the gap with plausible guesses, which is how invented requirements appear.
3. **It samples.** The same prompt can give different answers. A good prompt narrows the range of likely answers, so even different runs land close to what you need.

Put simply: **every word in your prompt shifts the probabilities.** Prompt engineering is choosing those words on purpose.

### 3. The Anatomy of a Good Prompt

Most strong prompts have five parts. Not every prompt needs all five, but knowing them lets you see what a weak prompt is missing.

| Part | Question it answers | Example |
|---|---|---|
| **Role** | Who should the AI act as? | "You are a senior QA engineer." |
| **Task** | What exactly should it do? | "Write test cases for AC1." |
| **Context** | What background does it need? | The user story and its rules |
| **Constraints** | What are the limits? | "Only use facts stated in AC1." |
| **Output format** | What should the answer look like? | "A table with 4 columns: …" |

What each part does, and why:

- **Role** sets the tone, vocabulary and level of detail. "Senior QA engineer" makes the model more likely to write preconditions and expected results, because that is how QA engineers write.
- **Task** is the actual request. Use a clear verb: write, review, list, compare, explain.
- **Context** is the material the model must work from. For testing, this is usually the requirement. Without it, the model invents one.
- **Constraints** are the rules for the answer: what to include, what to avoid, how many items. Good constraints are **checkable**: you can look at the answer and say yes or no.
- **Output format** fixes the shape of the answer, so you can use it straight away, or read it with code. You go deeper on this later today, in *Format Locking*.

**An everyday analogy:** briefing a contractor. "Fix the kitchen" gets you whatever they think a kitchen needs. "You're a plumber (role). Replace the kitchen tap (task). It's a single-lever mixer on a granite worktop (context). Don't touch the dishwasher pipe, and finish by 5 pm (constraints). Send me a photo and an invoice (output format)" gets you what you actually wanted.

### 4. System, User and Assistant Messages

Behind the scenes, chat tools send the model a list of **messages**, each with a **role**:

| Message role | Who writes it | What it holds |
|---|---|---|
| **System** | The tool, or a developer building an app | Standing instructions that apply to the whole conversation |
| **User** | You | Your questions and pasted material |
| **Assistant** | The model | Its earlier replies in the conversation |

In a chat app, you only type **user** messages; the tool adds its own hidden system message. When developers call a model from code, they write the system message themselves. Some providers call it the **developer** message instead. The idea is the same: standing instructions that take priority over the user's request.

Here is what a request looks like as data, written as a Python list:

```python
messages = [
    {"role": "system", "content": "You are a senior QA engineer. Only use facts from the story."},
    {"role": "user", "content": "Write 3 test cases for AC1 of US-205: SAVE10 gives 10% off a subtotal of $50.00 or more."},
]
```

Two things to notice:

- The **system** message holds rules that should apply to every request: the role, and "only use facts from the story".
- The **user** message holds this particular request, with its context.

On Thursday you write the system-style instructions for your own agent. For now, the important idea is that **standing rules and the specific request are different things**, and good prompts keep them apart.

### 5. Core Principles of Good Prompting

Six principles cover most of what makes a prompt work:

1. **Be clear about the task.** One prompt, one job. "Write test cases and also review the story and suggest UI improvements" splits the model's attention three ways.
2. **Give the real context.** Paste the actual acceptance criteria, not your summary of them. Your summary may already have lost a detail.
3. **Make constraints checkable.** "Write good tests" cannot be checked. "Include a test at exactly $50.00" can.
4. **Say what to do, not only what not to do.** "Don't make it long" leaves the length open. "Write no more than 5 test cases" closes it.
5. **Fix the output format.** A predictable shape saves you time, and lets code check the answer.
6. **Allow the model to say "I don't know".** "If the story does not say, write NOT SPECIFIED instead of guessing" gives the model a safe alternative to inventing an answer.

Principle 6 deserves special attention for testers. From *Generative AI Concepts*, you know that assistants are trained to be helpful, so they tend to produce an answer even when the honest answer is "the requirement doesn't say". Giving them an explicit way out reduces invented requirements. You go deeper on this later today, in *Specificity and Context*.

### 6. Worked Example: Build a Prompt One Part at a Time

**Goal:** useful test cases for **AC1** of US-205. In the handout, you start with a lazy prompt and add one part at a time, pasting the full prompt into a **new chat** after each step. A new chat matters: in the same chat, the model can see your earlier attempts, and that changes the answer.

#### Step 1: The lazy prompt (task only)

```text
Write test cases for a coupon feature.
```

The model has to **guess** everything: which coupon, which rules, how many tests, which format. You typically get a long, generic list, including rules that are not in US-205, such as expiry dates and "one use per customer". Each invented rule is a test you would have to delete.

#### Step 2: Add a role

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for a coupon feature.
```

The answer usually becomes more structured and uses testing language: preconditions, steps, expected results. But it is **still guessing the rules**. A role improves the style, not the facts.

#### Step 3: Add context

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for this acceptance criterion:

AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
```

This is usually the **biggest single improvement**. The model now works from **our** rule. Look at the answer: does it include a test at exactly $50.00? Often it does; sometimes it does not. Context makes good answers likely, not certain.

#### Step 4: Add constraints

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for this acceptance criterion:

AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.

Constraints:
- Use only the facts stated in AC1. Do not invent rules (for example expiry dates).
- Include boundary tests at $50.00 and just below it ($49.99).
- Write no more than 5 test cases.
```

Each constraint does a job:

- **"Use only the facts stated in AC1"** removes invented rules.
- **"Include boundary tests at $50.00 and $49.99"** forces the most important cases, using **Boundary Value Analysis** from Week 3.
- **"No more than 5"** stops the answer sprawling.

Every one of them can be checked in the answer.

#### Step 5: Add an output format

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for this acceptance criterion:

AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.

Constraints:
- Use only the facts stated in AC1. Do not invent rules (for example expiry dates).
- Include boundary tests at $50.00 and just below it ($49.99).
- Write no more than 5 test cases.

Output format:
A Markdown table with exactly these columns:
ID | Title | Subtotal | Expected total
Use IDs TC-01, TC-02 and so on. No text before or after the table.
```

The answer now has a **predictable shape** you can paste into a test plan or spreadsheet, and read with code. This is the final version, and the handout saves it in `prompts.txt` as `=== AC test cases - v1 ===`.

#### What changed at each step

| Step | Part added | Main effect |
|---|---|---|
| 1 | Task only | Generic answer; invented rules |
| 2 | Role | Better structure and vocabulary; still guessing |
| 3 | Context | Works from our rule: the biggest jump |
| 4 | Constraints | Removes unwanted content; forces boundaries |
| 5 | Output format | Predictable, reusable, checkable shape |

### 7. Checking the Answer

Even a five-part prompt does not guarantee a correct answer. Here is the kind of reply the Step 5 prompt produces. It is **illustrative**, written for this lesson, and it contains one typical mistake:

```text
| ID    | Title                                | Subtotal | Expected total |
|-------|--------------------------------------|----------|----------------|
| TC-01 | Subtotal well above $50 gets 10% off | 100.00   | 90.00          |
| TC-02 | Subtotal exactly $50.00 gets 10% off | 50.00    | 45.00          |
| TC-03 | Subtotal $49.99 gets no discount     | 49.99    | 49.99          |
| TC-04 | Subtotal $50.01 gets 10% off         | 50.01    | 45.00          |
| TC-05 | Subtotal $75.00 gets 10% off         | 75.00    | 67.50          |
```

#### 7.1 Check it by hand

Go through your constraints one by one:

- **Four columns, nothing before or after?** Yes.
- **No more than 5 rows?** Yes, exactly 5.
- **Boundaries at $50.00 and $49.99?** Yes: TC-02 and TC-03.
- **No invented rules?** Yes: every row is about the subtotal and the 10% discount.
- **Every expected total correct?** Work each one out. 100 × 0.9 = 90.00 ✅. 50 × 0.9 = 45.00 ✅. 49.99 is under $50, so unchanged ✅. 50.01 × 0.9 = 45.009, which rounds to **45.01**, but the table says **45.00** ❌. 75 × 0.9 = 67.50 ✅.

The format is perfect and the maths is wrong in one row. That is typical: the model is excellent at shape and less reliable at arithmetic, as you saw in *Generative AI Concepts*.

#### 7.2 Let a short script check the maths

Because the format is fixed, a few lines of Python can check every row against the rule:

```python
# check_table.py
REPLY = """| ID    | Title                                | Subtotal | Expected total |
|-------|--------------------------------------|----------|----------------|
| TC-01 | Subtotal well above $50 gets 10% off | 100.00   | 90.00          |
| TC-02 | Subtotal exactly $50.00 gets 10% off | 50.00    | 45.00          |
| TC-03 | Subtotal $49.99 gets no discount     | 49.99    | 49.99          |
| TC-04 | Subtotal $50.01 gets 10% off         | 50.01    | 45.00          |
| TC-05 | Subtotal $75.00 gets 10% off         | 75.00    | 67.50          |"""

def ac1_total(subtotal):                      # the rule, written by a person from AC1
    return round(subtotal * 0.9, 2) if subtotal >= 50 else subtotal

rows = [line.strip("|").split("|") for line in REPLY.splitlines()[2:]]
print(f"{len(rows)} rows (limit 5)")
for test_id, title, subtotal, expected in rows:
    sub, exp = float(subtotal), float(expected)
    correct = ac1_total(sub)
    status = "OK" if exp == correct else f"WRONG: should be {correct:.2f}"
    print(f"{test_id.strip()}  {sub:7.2f} -> {exp:7.2f}  {status}")
```

Output:

```text
5 rows (limit 5)
TC-01   100.00 ->   90.00  OK
TC-02    50.00 ->   45.00  OK
TC-03    49.99 ->   49.99  OK
TC-04    50.01 ->   45.00  WRONG: should be 45.01
TC-05    75.00 ->   67.50  OK
```

What to notice:

- `ac1_total` is the rule written by a **person**, from AC1. The check is only as good as this function, so it must come from the requirement, not from the AI's answer.
- `splitlines()[2:]` skips the header row and the `|---|` separator row.
- `line.strip("|").split("|")` turns each row into a list of four cells. This only works because the prompt locked the format to exactly four columns.
- The script never trusts the table. It recalculates every expected total and compares.

This is the pattern for the whole week: **the prompt sets a shape, and the shape makes the answer checkable.**

### 8. Zero-Shot Prompting

Every prompt in this lesson is a **zero-shot** prompt: it gives instructions but **no examples** of a finished answer. Zero-shot is the right place to start. It is quick, and for many tasks it is enough.

When zero-shot results are not good enough, you have three next steps, each covered later today:

- Add **more specific context and constraints** (*Specificity and Context*).
- **Lock the format** more strictly, and read it safely in code (*Format Locking*).
- **Show examples** of the answer you want (*Few-Shot Prompting*).

### 9. The Prompt-Refinement Loop: Prompting as Testing

Improving a prompt follows the same loop as debugging a test:

1. **Write** the prompt.
2. **Run** it, in a new chat.
3. **Check** the answer against what you needed: your constraints, the requirement, the maths.
4. **Change one thing.** Add a constraint, paste the missing context, tighten the format.
5. **Run again**, and compare.

The rule **change one thing at a time** matters for the same reason it does in debugging. If you change the role, the constraints and the format all at once and the answer improves, you do not know which change helped, or whether one of them made something worse.

Because answers vary between runs, judge a prompt on **more than one run**. If a constraint is obeyed in two runs out of three, the prompt is not reliable yet. On Friday you will automate exactly this: running an agent's prompt many times and counting how often the output passes its checks.

**An illustrative scenario.** A tester asks for "test cases for the coupon field" and gets 14 tests. Three are about expiry dates, which the story never mentions, and none checks $50.00. The tester adds "use only the facts in AC1": the expiry tests disappear. They add "include $50.00 and $49.99": the boundaries appear. They add the table format: the answer becomes checkable, and a script finds one wrong total. Four small, single changes, each checked, turned a generic list into a usable draft.

### 10. Prompts Are Artifacts: Save and Version Them

A prompt that works is worth keeping, just like a test. The handout has you save every working prompt in `prompts.txt` with a heading, a version, a "Use" line and a source:

```text
=== AC test cases - v1 ===
Use: draft test cases for one acceptance criterion, as a fixed-format table.
Source: Handout 03, Topic 1
```

Why bother?

- **Repeatability.** You can rerun exactly the prompt that worked, with its data.
- **Improvement.** When you change it, you save `v2` and can compare.
- **Sharing.** A teammate can use your prompt instead of starting from scratch.

AI providers give the same advice for prompts used in real applications. OpenAI's documentation recommends treating prompts as application code: keeping them in named, versioned places and reviewing changes to them like any other change ([OpenAI docs](https://developers.openai.com/api/docs/guides/prompting)). By the end of today, your `prompts.txt` becomes a small **prompt library** for Project 2.

### 11. The Five Parts Beyond Test Cases

The five parts work for any QE task, not only test cases. Two more examples:

**Turning rough notes into a bug report:**

```text
Role: You are a QA engineer writing a bug report for developers.
Task: Turn my notes below into a bug report.
Context:
"""
safari, applied SAVE10 on 80 dollar cart, checkout btn does nothing, chrome fine, no console error
"""
Constraints:
- Use only the facts in my notes. If something is missing (for example the app version), write NOT PROVIDED.
- Do not guess the cause.
Output format: Title, Environment, Steps to reproduce (numbered), Expected result, Actual result.
```

**Summarising failures for a stand-up:**

```text
Role: You are a test lead preparing a stand-up update.
Task: Summarise the failed tests below for the team.
Context: (paste the failure lines from last night's run)
Constraints:
- At most 5 bullet points.
- Every number you state must appear in the pasted results.
Output format: Bullets, then one line starting "Biggest risk:".
```

Notice two habits repeated in both. The pasted material is fenced off clearly, here with triple quotes, so the model can tell your notes from your instructions. And each prompt includes a **way out**: "write NOT PROVIDED" and "every number must appear in the results" both stop the model from filling gaps with guesses.

### 12. Common Prompting Mistakes

| Mistake | What you get | Fix |
|---|---|---|
| Summarising the requirement instead of pasting it | Answers based on your summary, which may have lost a detail | Paste the real acceptance criteria |
| Asking for several jobs at once | Shallow answers to each | One prompt, one job |
| Only negative instructions ("don't be vague") | The model still guesses what you want | Say what you want: "at most 5 tests, each with an expected total" |
| No output format | A different shape every run | Fix the columns or fields |
| Reusing a long chat for a new task | Old messages leak into the new answer | Start a new chat for each new task |
| Trusting a neat answer | Hidden mistakes, like the wrong total in section 7 | Check against your constraints and the requirement |

### 13. A Prompt Checklist

Before you send a prompt that matters, run through this checklist:

- [ ] **Role:** have I said who the AI should act as?
- [ ] **Task:** is there one clear job, with a clear verb?
- [ ] **Context:** have I pasted the real requirement, not my summary?
- [ ] **Constraints:** can each one be checked in the answer?
- [ ] **Output format:** have I said exactly what shape the answer should take?
- [ ] **Way out:** have I told it what to do if the information is missing?
- [ ] **Check:** do I know how I will check the answer: by hand, with a script, or both?

---

## Practice Exercises

1. **Spot the missing parts (paper, 10 min).** For each prompt, list which of the five parts it has and which are missing, then rewrite it with all five:
   - (a) *"Review this login story."*
   - (b) *"You are a tester. Give me some negative tests for the password field, as a list."*

2. **Make constraints checkable (paper, 10 min).** Rewrite each vague constraint so you could check it with a yes or no: "keep it short"; "cover the important cases"; "don't make stuff up"; "use a nice format".

3. **Write and check a prompt for AC2 (AI tool, 20 min).** Follow this week's four steps:
   - **Prompt:** write a five-part prompt for **AC2** (*Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10"*). Ask for a table with the columns `ID | Title | Subtotal | Expected total | Expected message`.
   - **Review:** check every constraint by hand. Is the message copied **exactly**, including the full stop and capital letters?
   - **Run:** add a message check to `check_table.py`: every row under $50.00 must show exactly `Spend $50.00 to use SAVE10`.
   - **Record:** save the prompt in `prompts.txt` as `=== AC2 test cases - v1 ===`, and note any mistakes the AI made.

   *Hint:* exact messages are a common place for AI drafts to drift, for example to "Spend $50 to use SAVE10".

4. **One change at a time (AI tool, 15 min).** Take the Step 5 prompt and remove only the line *"Use only the facts stated in AC1"*. Run it three times in new chats. How many of the three answers invent a rule? What does that tell you about that one constraint?

---

## Knowledge Check

1. Why is the prompt "the only steering wheel" for an AI assistant?

<details><summary>Answer</summary>

The model predicts likely text from what is in its context window. It cannot see your requirements or intentions unless they are in the prompt, so the prompt is the only thing shaping the answer.

</details>

2. Name the five parts of a good prompt.

<details><summary>Answer</summary>

Role, task, context, constraints and output format.

</details>

3. In the worked example, which single step usually improves the answer most, and why?

<details><summary>Answer</summary>

Adding context (the actual AC1). Without it, the model guesses the rules from generic coupon features; with it, the model works from our requirement.

</details>

4. What is the difference between a system message and a user message?

<details><summary>Answer</summary>

A system message holds standing instructions for the whole conversation, written by the tool or a developer. A user message holds a particular request, written by the user.

</details>

5. The AI's table had the right shape but one wrong total. What does this show, and how did the script help?

<details><summary>Answer</summary>

Models are good at format and less reliable at arithmetic. Because the format was fixed, the script could read every row, recalculate the total from the rule in AC1, and flag the wrong one.

</details>

6. Why should you change only one thing at a time when improving a prompt?

<details><summary>Answer</summary>

So that you know which change caused the improvement (or the problem), just as when debugging a test.

</details>

---

## Glossary

- **Prompt:** the text you give an AI assistant: questions, instructions and pasted material.
- **Prompt engineering:** writing prompts that reliably get useful, correct, well-formatted answers.
- **Acceptance criterion (AC):** one rule a feature must follow, from a user story.
- **Role:** who the prompt asks the AI to act as.
- **Task:** the job the prompt asks for.
- **Context:** the background material the AI must work from.
- **Constraint:** a rule for the answer; good constraints can be checked.
- **Output format:** the shape the answer must take.
- **System message:** standing instructions for a whole conversation.
- **User message:** a particular request from the user.
- **Assistant message:** an earlier reply from the model.
- **Zero-shot prompting:** asking with instructions only, no examples.
- **Prompt-refinement loop:** write, run, check, change one thing, run again.
- **Prompt library:** a saved, versioned collection of prompts that work.

---

## Summary

- **The prompt is the only steering wheel.** The model predicts likely text from what is in front of it, so missing context becomes invented content.
- **Strong prompts have five parts:** role, task, context, constraints and output format. Context usually helps most.
- **Make constraints checkable**, say what to do rather than only what not to do, and give the model a way to say "not specified".
- **A fixed format makes answers checkable.** A short script found the wrong total the table's neat shape was hiding.
- **Refine like you debug:** change one thing at a time, and judge a prompt over several runs.
- **Save working prompts** with a version and a "Use" line, and grow them into a prompt library.

---

## Additional Resources

- OpenAI, *Prompt engineering* guide: https://developers.openai.com/api/docs/guides/prompt-engineering
- Anthropic, *Prompt engineering overview* (Claude documentation): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API*: https://help.openai.com/en/articles/6654000
