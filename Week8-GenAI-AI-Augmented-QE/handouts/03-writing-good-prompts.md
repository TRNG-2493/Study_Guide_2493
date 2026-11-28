# Week 08 · Lecture 03: Writing Good Prompts

**Topics:**

1. [Prompt Engineering Principles](#topic-1)
2. [Specificity and Context](#topic-2)
3. [Format Locking](#topic-3)
4. [Few-Shot Prompting](#topic-4)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Use your `week08` folder from Lectures 01–02.
> 2. Today's code needs **only standard Python**: nothing to install. Check Python works:
>    ```bash
>    python --version
>    ```
> 3. Have your AI assistant open in a browser tab: **ChatGPT, Copilot Chat or Claude**. Today you'll use it a lot. Copilot users in VS Code: use the **chat panel**.
> 4. Open `prompts.txt` from Lectures 01–02 in your editor (create it in your `week08` folder if you don't have it). You'll keep adding prompts, in the same format, and by the end of the day it becomes your **prompt library** for Project 2.

---

## How to Use This Handout

Each topic has the same parts: **Definition → Key ideas → Worked example (step by step) → Checkpoint → Your turn → Common errors** (only where needed).

Three topics are **prompt topics** (no code): the worked example is a prompt that grows step by step, and you paste it into your AI assistant after each step. Topic 3 uses one short Python file, because reading AI output safely in code is a skill your AI agent will need at the end of the week.

> **About AI answers:** ChatGPT, Copilot and Claude each answer differently, and the same tool gives a different answer each time (remember **temperature** from Lecture 02). Checkpoints for AI answers say "**something like**" and give you a list of things to **check for**. Don't expect word-for-word matches.

**Today's running example** is the coupon story you met in Lecture 02. Keep it handy:

```text
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

(*AC* = acceptance criterion: one rule the feature must follow.)

---

## Learning Objectives

By the end of this lecture you will be able to:

- Build a prompt from its parts: **role, task, context, constraints and output format**.
- Turn a **vague** prompt into a **specific** one, and know **what never to paste** into an AI tool.
- **Lock the output format** (for example JSON) and read AI replies safely in Python.
- Use **few-shot prompting**: teach the AI a pattern by showing it examples.

---

<a id="topic-1"></a>

# Topic 1: Prompt Engineering Principles

## Definition

A **prompt** is the text you give an AI assistant: your question, instructions and any material you paste in. **Prompt engineering** is the skill of writing prompts that reliably get **useful, correct and well-formatted** answers. Remember from Lecture 02 that an LLM predicts likely text **based on what's in front of it**, so the prompt is the only thing steering it. A good prompt works like a good bug report: clear, complete and easy to act on. Writing prompts is a lot like testing: **try → check the result → improve → try again**.

## Key Ideas

1. **The anatomy of a good prompt.** Not every prompt needs every part, but the best prompts usually have most of them:

   | Part | Question it answers | Example |
   |---|---|---|
   | **Role** | Who should the AI act as? | "You are a senior QA engineer." |
   | **Task** | What exactly should it do? | "Write test cases for AC1." |
   | **Context** | What background does it need? | The user story and its rules |
   | **Constraints** | What are the limits? | "Only use facts stated in the story." |
   | **Output format** | What should the answer look like? | "A table with 4 columns: …" |

2. **System vs. user messages.** Behind the scenes, AI tools receive a hidden **system message** (standing instructions set by the tool or by a developer) plus your **user message**. In a chat app you only type the user message. On Thursday you'll write system-style instructions for your own agent.
3. **Zero-shot prompting** means asking with **no examples**: just instructions. It's the starting point. If the results aren't good enough, you add specifics (Topic 2), a format (Topic 3) or examples (Topic 4).
4. **The refinement loop:** write → run → **check against what you needed** → change **one thing** → run again. That's exactly how you'd debug a test.

## Worked Example: Build a Prompt One Part at a Time

**Goal:** get useful test cases for **AC1** of US-205. We'll start with a lazy prompt and add one part at a time. **After each step, paste the full prompt into a NEW chat in your AI assistant** and look at what changes.

> Why a new chat each time? The AI remembers earlier messages in the same chat (its **context window**). A new chat gives a fair comparison.

### Step 1: The lazy prompt (task only)

```text
Write test cases for a coupon feature.
```

**What to notice:** the AI has to **guess** everything: which coupon, what rules, how many tests, what format. You'll probably get a long, generic list ("test with valid coupon", "test with expired coupon"…), including things that aren't even in our story, such as expiry dates.

### Step 2: Add a role

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for a coupon feature.
```

**What to notice:** the role sets the **tone and level**. Answers usually become more structured and use testing language (preconditions, expected results). It's still guessing the rules, though.

### Step 3: Add context (the actual requirement)

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for this acceptance criterion:

AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
```

**What to notice:** this is the **biggest improvement**. The AI now works from **our** rule instead of a generic idea of coupons. Look for tests at $50.00. Did it include them?

### Step 4: Add constraints

```text
You are a senior QA engineer testing an e-commerce web app.
Write test cases for this acceptance criterion:

AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.

Constraints:
- Use only the facts stated in AC1. Do not invent rules (for example expiry dates).
- Include boundary tests at $50.00 and just below it ($49.99).
- Write no more than 5 test cases.
```

**What to notice:** constraints **remove** the unwanted stuff (invented rules, too many tests) and **force** the important stuff (boundaries). Each constraint should be something you can **check** in the answer.

### Step 5: Add an output format

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

**What to notice:** the answer now has a **predictable shape** that you can copy straight into a test plan or spreadsheet.

### Consolidated Prompt

The Step 5 prompt is your final version. It has all five parts: role, task, context, constraints and output format. Add it to `prompts.txt`:

```text
=== AC test cases - v1 ===
Use: draft test cases for one acceptance criterion, as a fixed-format table.
Source: Handout 03, Topic 1

--- Prompt (new chat) ---
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

## Checkpoint

With the Step 5 prompt, your AI assistant should reply with **something like**:

```text
| ID    | Title                                   | Subtotal | Expected total |
|-------|-----------------------------------------|----------|----------------|
| TC-01 | Subtotal well above $50 gets 10% off    | 100.00   | 90.00          |
| TC-02 | Subtotal exactly $50.00 gets 10% off    | 50.00    | 45.00          |
| TC-03 | Subtotal $49.99 gets no discount        | 49.99    | 49.99          |
| TC-04 | Subtotal $50.01 gets 10% off            | 50.01    | 45.01          |
| TC-05 | Small subtotal gets no discount         | 20.00    | 20.00          |
```

**Check for:**

- ✅ A table with exactly the 4 columns you asked for, and nothing before or after it
- ✅ No more than 5 rows
- ✅ Rows for **$50.00** (→ $45.00) and **$49.99** (→ unchanged)
- ✅ No invented rules (expiry dates, minimum items, case-insensitive codes…)
- ✅ **Every expected total is correct.** Check the maths yourself! AI sometimes gets arithmetic wrong.

## Your Turn

1. **(In class, 3 min)** Remove the **Constraints** section from the Step 5 prompt and run it in a new chat. What came back that you didn't want? What went missing?
2. **(After class)** Change the role to *"You are a business analyst"* and run the prompt again. How does the answer change? Which role is better for this task, and why?
3. **(After class)** Write a 5-part prompt (role, task, context, constraints, output format) for **AC3**: *Unknown codes show "Coupon code not recognised".* Save it in `prompts.txt`.

---

<a id="topic-2"></a>

# Topic 2: Specificity and Context

## Definition

**Specificity** means saying **exactly** what you want: which feature, which rules, how many results, in what form. **Context** is the background material the AI needs and can't know on its own: your requirement, your code, your error message, your team's conventions. A vague prompt produces a generic answer because the AI fills every gap with a **guess**, and guesses are where hallucinations come from. The more relevant context you give, the less the AI has to guess. But context has a limit: **never paste secrets, personal data or confidential company code** into a public AI tool.

## Key Ideas

1. **Vague in → generic out.** "Test the login" gives a textbook list. "Test that 5 failed logins lock the account for 15 minutes" gives useful tests.
2. **Useful context for QE prompts:**

   | Context type | Example |
   |---|---|
   | The requirement | User story + acceptance criteria |
   | The code or page | The function, or the HTML of the form |
   | The evidence | Error message, test output, logs |
   | Conventions | "We use pytest and Playwright; test names start with `test_`" |
   | What you already tried | "I already checked the locator in DevTools" |

3. **Fence off pasted material with delimiters**, such as `"""…"""` or `### Requirement`. This tells the AI where the instructions end and the data begins.
4. **What NOT to paste:**

   | ❌ Never paste | ✅ Instead |
   |---|---|
   | Passwords, API keys, tokens | Placeholders: `<API_KEY>`, `<valid_password>` |
   | Real customer names, emails, card numbers | Made-up data: `test.user@example.com` |
   | Confidential company code or documents | Only what your team's AI policy allows |

## Worked Example: From Vague to Specific

**Goal:** get the AI to check whether **US-205 is clear enough to test**. We'll improve the prompt in four steps. Paste each version into a new chat.

### Step 1: The vague version

```text
Is this requirement good?
SAVE10 gives 10% off. Under 50 no discount. Bad codes show an error.
```

**What's wrong:** "good" is undefined (good for whom? for what?), and the requirement is retyped from memory, so it's already **different** from the real story ("Under 50" vs. "under $50.00"; "an error" vs. the exact message). The AI will give a polite, general opinion.

### Step 2: Paste the real requirement and fence it off

```text
Review the user story below.

### User story
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
### End of user story
```

**What changed:** the AI now has the **exact** text, copied, not retyped. The `###` markers show clearly where the story starts and ends.

### Step 3: Say exactly what "review" means

Replace the first line with:

```text
You are a QA engineer reviewing a user story BEFORE test design.
For each acceptance criterion, decide whether it is testable as written.
Look for: vague words, missing values, missing error messages,
and situations the story does not cover.
```

**What changed:** "good" became **four concrete things to check**. Now the answer can be judged: did it check all four?

### Step 4: Say how many results and in what form, and allow questions

Add at the end:

```text
Reply with a table: AC | Testable? (Yes/No) | Problem | Question for the business analyst.
List at most 5 problems in total. If something is unclear, ask a question
instead of guessing the answer.
```

**What changed:** a limit (at most 5), a format (a table), and **permission to ask questions instead of guessing**. That last line is one of the best ways to reduce hallucinations.

### Consolidated Prompt

Add the final prompt to `prompts.txt`, with the story included:

```text
=== Story review - v1 ===
Use: check a user story is testable before test design.
Source: Handout 03, Topic 2

--- Prompt (new chat) ---
You are a QA engineer reviewing a user story BEFORE test design.
For each acceptance criterion, decide whether it is testable as written.
Look for: vague words, missing values, missing error messages,
and situations the story does not cover.

### User story
US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
### End of user story

Reply with a table: AC | Testable? (Yes/No) | Problem | Question for the business analyst.
List at most 5 problems in total. If something is unclear, ask a question
instead of guessing the answer.
```

## Checkpoint

You should get **something like**:

```text
| AC  | Testable? | Problem                                       | Question for the BA                               |
|-----|-----------|-----------------------------------------------|---------------------------------------------------|
| AC1 | Yes       | Doesn't say if 10% is on subtotal before tax  | Is the discount applied before or after tax?      |
| AC3 | Yes       | Case sensitivity not stated                   | Is "save10" accepted, or only "SAVE10"?           |
| AC4 | No        | Doesn't say what happens with a second coupon | What message shows when a second coupon is tried? |
```

**Check for:**

- ✅ A table in the requested format, with at most 5 problems
- ✅ **AC4** flagged: it says *what* must happen but not *what the user sees* when they try a second coupon
- ✅ Questions, not invented answers (for example it must **not** say "the second coupon replaces the first" as if that were fact)
- ✅ No changes to the exact messages in AC2 and AC3

## Your Turn

1. **(In class, 3 min)** Run the Step 1 (vague) and consolidated prompts side by side. Write down **two** differences in the answers.
2. **(After class)** Write a specific prompt for this vague request: *"Help me test the login page."* Use this context: *username and password fields; 5 wrong passwords lock the account for 15 minutes; the error message is "Invalid username or password".* Remember: use a **placeholder** for the password, not a real one.
3. **(After class)** You want help with a failing test. Your test log contains `customer_email=priya.sharma@gmail.com` and `api_key=sk_live_8f2a…`. Rewrite those two lines so they're safe to paste into an AI tool.

---

<a id="topic-3"></a>

# Topic 3: Format Locking

## Definition

**Format locking** means telling the AI **exactly** what shape the answer must have, such as a JSON list with fixed field names, a table with fixed columns or one line in a fixed pattern, so that the answer can be **read by code** and not just by people. When AI output feeds into a script, a spreadsheet or a test, a predictable format is essential. Even with a clear format instruction, AIs sometimes **drift**: they add a friendly sentence, wrap the JSON in ```` ```json ```` fences, or rename a field. So we do two things: **lock the format in the prompt**, and **check the format in code**.

## Key Ideas

1. **Choose a format that suits where the answer goes:** a table for people, **JSON** for code, a single fixed line for quick checks.
2. **Lock it with precise words:** name every field, show a tiny example, give an exact count, and say *"No text before or after the JSON."*
3. **Format drift is normal.** Common drift: an extra sentence ("Sure! Here are…"), Markdown fences, missing fields, the wrong number of items.
4. **Defensive parsing:** never assume the reply is clean. Extract the part you need, parse it, check it, and fail with a **clear message** if it's wrong.

## Worked Example: Read an AI Reply Safely

**The prompt we sent** (you can try it in your AI assistant):

```text
Give exactly 3 boundary test cases for: "SAVE10 gives 10% off a subtotal of $50.00 or more."
Reply ONLY with a JSON list. Each item has exactly these keys:
"title" (string), "subtotal" (number), "expected_total" (number).
Example item: {"title": "Subtotal 100.00 gets 10% off", "subtotal": 100.00, "expected_total": 90.00}
No text before or after the JSON.
```

Even so, the reply came back with extra text around it. That's very common. Let's handle it. Create `parse_reply.py`.

### Step 1: The reply, exactly as the AI gave it

````python
import json

# Step 1: a reply copied from an AI assistant (format drift included!)
reply = """Sure! Here are the boundary tests you asked for:
```json
[
  {"title": "Subtotal exactly 50.00 gets 10% off", "subtotal": 50.00, "expected_total": 45.00},
  {"title": "Subtotal 49.99 is unchanged", "subtotal": 49.99, "expected_total": 49.99},
  {"title": "Subtotal 50.01 gets 10% off", "subtotal": 50.01, "expected_total": 45.01}
]
```
Let me know if you need more!"""
````

**What this code does:**

- `import json` loads Python's built-in JSON module.
- `reply` holds the AI's answer as one multi-line string (triple quotes `"""` allow line breaks). It contains **three kinds of drift**: a sentence before, Markdown fences around the JSON, and a sentence after.

### Step 2: Try to read it directly

```python
# Step 2: try to read it as JSON directly
try:
    data = json.loads(reply)
except json.JSONDecodeError as err:
    print("Direct parse failed:", err.msg)
```

**What this code does:**

- `json.loads` turns JSON **text** into Python lists and dictionaries, but only if the text is pure JSON.
- It fails here because the reply starts with "Sure!". The `try/except` catches the error so the program doesn't crash, and prints the reason.

### Step 3: Defensive parsing

```python
# Step 3: defensive parsing - keep only the part between [ and ]
def extract_json_list(text):
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON list found in the reply")
    return json.loads(text[start:end + 1])

data = extract_json_list(reply)
print("Parsed", len(data), "test cases")
```

**What this code does:**

- `text.find("[")` gives the position of the **first** `[`, and `text.rfind("]")` the position of the **last** `]`. Everything between them is the JSON list.
- If either one is missing, `find` returns `-1`, and we raise an error with a **clear message**.
- `text[start:end + 1]` slices out just the list (`+ 1` includes the final `]`), and then `json.loads` parses it.

### Step 4: Check the format you asked for

```python
# Step 4: check the format we asked for
REQUIRED_KEYS = {"title", "subtotal", "expected_total"}
assert isinstance(data, list), "Reply must be a JSON list"
assert len(data) == 3, f"Asked for 3 cases, got {len(data)}"
for i, case in enumerate(data, start=1):
    missing = REQUIRED_KEYS - case.keys()
    assert not missing, f"Case {i} is missing {missing}"
print("Format OK")
```

**What this code does:**

- Parsing only proves it's **valid JSON**. It doesn't prove it's the JSON **we asked for**. These checks do.
- `assert condition, "message"` stops the program with the message if the condition is false. Testers know this from pytest!
- `REQUIRED_KEYS - case.keys()` is a **set difference**: the keys we required that are missing from this case. An empty set means nothing is missing.

### Step 5: Use the data

```python
# Step 5: now the data is safe to use
for case in data:
    print(f"{case['subtotal']:>6.2f} -> {case['expected_total']:>6.2f}  {case['title']}")
```

**What this code does:** prints each case as a neat row. `:>6.2f` means "right-aligned, 6 characters wide, 2 decimal places". The data is now ready to drive a test, which you'll do in Lecture 04.

### Consolidated File: `parse_reply.py`

````python
import json

# Step 1: a reply copied from an AI assistant (format drift included!)
reply = """Sure! Here are the boundary tests you asked for:
```json
[
  {"title": "Subtotal exactly 50.00 gets 10% off", "subtotal": 50.00, "expected_total": 45.00},
  {"title": "Subtotal 49.99 is unchanged", "subtotal": 49.99, "expected_total": 49.99},
  {"title": "Subtotal 50.01 gets 10% off", "subtotal": 50.01, "expected_total": 45.01}
]
```
Let me know if you need more!"""

# Step 2: try to read it as JSON directly
try:
    data = json.loads(reply)
except json.JSONDecodeError as err:
    print("Direct parse failed:", err.msg)

# Step 3: defensive parsing - keep only the part between [ and ]
def extract_json_list(text):
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("No JSON list found in the reply")
    return json.loads(text[start:end + 1])

data = extract_json_list(reply)
print("Parsed", len(data), "test cases")

# Step 4: check the format we asked for
REQUIRED_KEYS = {"title", "subtotal", "expected_total"}
assert isinstance(data, list), "Reply must be a JSON list"
assert len(data) == 3, f"Asked for 3 cases, got {len(data)}"
for i, case in enumerate(data, start=1):
    missing = REQUIRED_KEYS - case.keys()
    assert not missing, f"Case {i} is missing {missing}"
print("Format OK")

# Step 5: now the data is safe to use
for case in data:
    print(f"{case['subtotal']:>6.2f} -> {case['expected_total']:>6.2f}  {case['title']}")
````

## Checkpoint

```text
Direct parse failed: Expecting value
Parsed 3 test cases
Format OK
 50.00 ->  45.00  Subtotal exactly 50.00 gets 10% off
 49.99 ->  49.99  Subtotal 49.99 is unchanged
 50.01 ->  45.01  Subtotal 50.01 gets 10% off
```

The direct parse fails, the defensive parse works, the format checks pass and the data prints cleanly.

## Your Turn

1. **(In class, 3 min)** In the reply, rename `"expected_total"` to `"expected"` in the **second** item. Run the file. What message do you get, and is it clear enough for a teammate to fix the problem?
2. **(After class)** Send the prompt above to your AI assistant. Copy its **real** reply into `reply = """..."""` and run the file. Did your AI drift? How?
3. **(After class)** Delete the second item so the list has only 2 cases. Which check catches it? Then think: why is **"exactly 3"** in the prompt better than **"a few"**?
4. **(After class)** Add a check that every `expected_total` is a number: `isinstance(case["expected_total"], (int, float))`. Test it by changing one value to the string `"45.00"`.

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes` | JSON needs **double** quotes; the AI (or you) used single quotes `'title'` | Change to `"title"`. Add *"use double quotes"* to the prompt |
| `JSONDecodeError: Expecting ',' delimiter` | A missing comma between items, or a trailing comma after the last item | Look at the line number in the error. JSON doesn't allow trailing commas |
| `SyntaxError` on the `reply = """...` line | The reply itself contains `"""` | Use `'''...'''` around the reply instead |
| `KeyError: 'expected_total'` | A field is missing or renamed | That's what the Step 4 check is for. Run the checks **before** using the data |

---

<a id="topic-4"></a>

# Topic 4: Few-Shot Prompting

## Definition

**Few-shot prompting** means including a **few examples** of the input and the exact answer you want, so the AI can **copy the pattern**. *Zero-shot* = no examples, *one-shot* = one example, *few-shot* = usually 2–5 examples. The AI doesn't retrain or learn permanently. It just picks up the pattern from the examples in the prompt (this is called **in-context learning**). Few-shot is the best tool when the **format, labels or style** are hard to describe in words but easy to **show**.

## Key Ideas

1. **Show, don't tell.** One good example often works better than a paragraph of formatting rules.
2. **The AI copies everything in your examples:** the format, the length, the tone **and the mistakes**. Bad examples → bad answers.
3. **Choose examples carefully:**
   - Cover **different** answers (not three examples that are all "High").
   - Keep them **short** and **correct**.
   - Make them look like the **real** inputs you'll send.
4. **Order matters.** AIs lean towards the most recent example and the most common label in the examples. Mix them up.

## Worked Example: A Bug Severity Classifier

**Goal:** the AI should classify a bug report's severity and reply in **one exact line**, so that a script could read the answer later. We'll compare zero-shot with few-shot and see the difference the examples make.

### Step 1: Zero-shot first (no examples)

Paste into a **new chat**:

```text
You are a QA lead. Classify the severity of this bug report as Critical, High, Medium or Low.

Bug: Login button does nothing on Safari; users cannot sign in
```

**What to notice:** the AI probably gives a correct-sounding severity, but in **its own format**: a heading, a paragraph of reasoning, maybe a table. Each tool (and each run) formats it differently. A script couldn't read that reliably.

### Step 2: Add the format, still with no examples

In a **new chat**:

```text
You are a QA lead. Classify the severity of this bug report as Critical, High, Medium or Low.
Reply with one line only, in this format: Severity: <level> | Reason: <max 10 words>

Bug: Login button does nothing on Safari; users cannot sign in
```

**What to notice:** better, but AIs still drift. They write "**Severity:** Critical" in bold, add a second sentence, or use 20 words. Describing a format isn't always enough.

### Step 3: Add labelled examples (few-shot)

In a **new chat**:

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

**Why it's built this way:**

- The three examples cover **three different** severities, so the AI doesn't learn "everything is High".
- Each example answer is written **in the exact output format**. The examples **are** the format specification.
- The examples use the same layout (`Bug:` line, then `Severity:` line). The new bug ends after its `Bug:` line, so the AI's job is obviously to write the `Severity:` line.
- `###` headings fence off each example (delimiters, from Topic 2).

### Step 4: Reuse it for another bug

Copy the Step 3 prompt into a new chat, but replace only the **last** bug with:

```text
Bug: Footer link to Privacy Policy opens the wrong page
```

**What to notice:** the instruction and examples stay the same, and only the new bug changes. A prompt with a fixed part and a changing part is the idea behind **prompt templates**, which you'll build for your AI agent in Lecture 07.

### Consolidated Prompt

The Step 3 prompt is your final version. Add it to `prompts.txt`:

```text
=== Severity classifier - few-shot v1 ===
Use: classify a bug's severity in one fixed-format line.
Source: Handout 03, Topic 4

--- Prompt (new chat) ---
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

To classify another bug, keep everything and replace only the last `Bug:` line.

## Checkpoint

For Step 3 your AI should reply with **something like**:

```text
Severity: Critical | Reason: users on Safari cannot sign in at all
```

**Check for:**

- ✅ **One line only**, in the exact `Severity: … | Reason: …` format, with no bold, heading or extra sentence
- ✅ One of the four allowed levels
- ✅ A short reason (about 10 words or fewer)
- ✅ A sensible severity. "High" is also defensible, so ask yourself why.

**Compare Steps 1–3:**

| Step | Format followed? |
|---|---|
| 1 (zero-shot, no format) | Rarely. Free-form answer |
| 2 (zero-shot + format) | Often, but drifts |
| 3 (few-shot) | Most reliably |

For Step 4, expect something like `Severity: Low | Reason: wrong link, no impact on purchases` (or Medium).

## Your Turn

1. **(In class, 3 min)** Run Step 3 with your AI and compare your line with someone who used a **different** AI tool. Did both follow the format exactly? Did you get the same severity?
2. **(After class)** **Bad examples teach bad habits.** Change all three example answers to `High | Reason: ...` and classify three different bugs. Does the AI start answering "High" more often? Explain why.
3. **(After class)** Add a fourth example with severity **Medium**. Where would you put it in the list, and why? (Hint: Key Idea 4.)
4. **(After class)** Write a few-shot prompt that turns a one-line bug description into a **bug report title** in your team's style (for example `[Checkout] SAVE10 not applied at $50.00`). Use 3 examples.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI replies in a different format | The examples and the instruction disagree, or the examples are inconsistent | Make every example follow the format **exactly** |
| The AI copies the wording of an example | The examples are too similar to the new input | Use more varied examples |
| The AI classifies the examples too | The "Now classify this one" heading was missing | Keep a clear heading before the new bug |

---

## Lecture Wrap-Up: Quick Check

1. Name the five parts of a well-built prompt.
2. Why is pasting the **exact** requirement better than retyping it from memory?
3. Give two things you must never paste into a public AI tool.
4. Your prompt asked for pure JSON, but the reply starts with "Sure! Here you go:". What do you do in code?
5. What's the difference between zero-shot and few-shot prompting? When would you use few-shot?

<details>
<summary>Answers</summary>

1. Role, task, context, constraints, output format.
2. Retyping changes details (values, exact messages), so the AI works from the wrong requirement.
3. Any two of: passwords/API keys/tokens, real customer personal data, confidential company code or documents.
4. **Defensive parsing:** extract the JSON part, parse it, then check that its format matches what you asked for.
5. Zero-shot gives instructions only; few-shot adds examples of input and the desired answer. Use few-shot when the format, labels or style are easier to **show** than to describe.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Prompt** | The text you give an AI: instructions, questions and material |
| **Prompt engineering** | Writing prompts that reliably get useful, correct, well-formatted answers |
| **Role** | Who the AI should act as ("You are a senior QA engineer") |
| **Constraint** | A limit on the answer ("max 5 cases", "only use stated facts") |
| **System message** | Hidden standing instructions, set by the tool or a developer |
| **User message** | What you type into the chat |
| **Zero-shot / few-shot** | Prompting without / with examples |
| **In-context learning** | The AI picking up a pattern from examples in the prompt, without retraining |
| **Delimiter** | A marker that fences off pasted material (`###`, `"""`) |
| **Format locking** | Telling the AI exactly what shape the answer must have |
| **Format drift** | When the AI's answer doesn't quite follow the requested format |
| **Defensive parsing** | Reading AI output carefully: extract, parse, check, and fail clearly |
| **JSON** | A text format for structured data that both people and code can read |

## Summary

- A good prompt has a **role, task, context, constraints and output format**. Improve prompts with the same loop you use for tests: try → check → change one thing → retry.
- **Be specific and give real context.** Paste the exact requirement, fence it off, and allow the AI to ask questions. **Never paste secrets or personal data.**
- **Lock the format** when code will read the answer, and **parse defensively**, because AI output drifts.
- **Few-shot examples teach by showing**, including your mistakes, so choose varied, correct, short examples.
