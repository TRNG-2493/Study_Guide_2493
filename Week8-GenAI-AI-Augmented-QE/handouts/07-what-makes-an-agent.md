# Week 08 · Lecture 07: What Makes an Agent

**Topics:**

1. [Agent Architecture](#topic-1)
2. [Agent Instructions](#topic-2)
3. [Prompt Templates](#topic-3)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. In your `week08` folder, create a new folder called **`agent`** and open it in your editor. From now until Lecture 10, you'll build your AI agent in this folder.
> 2. Open your AI assistant: **ChatGPT, Copilot Chat or Claude**. Copilot users in VS Code: use the **chat panel**.
> 3. Nothing to install today. There's **no code** in this lecture: you'll write the agent's text files and try them in your AI tool.

---

## How to Use This Handout

Lectures 07–10 build **one AI agent**, step by step: **TestCaseDesigner**, which turns a user story into test cases. Every lecture adds files to your `agent` folder.

**Every step tells you where to do it:**

| Label | Where | What you do |
|---|---|---|
| 🤖 **AI tool** | ChatGPT, Copilot Chat or Claude | Open a **new chat**, paste exactly what the step shows, and read the reply |
| 📝 **Editor** | VS Code (or any editor) | Create or edit a file in your `agent` folder |
| 💻 **Terminal** | Command prompt / terminal, inside the `agent` folder | Run the command shown (from Lecture 09 on) |
| ✍️ **Paper** | Pen and paper, or a text file | Work something out yourself |

Each topic has the usual parts: **Definition → Key ideas → Worked example → Checkpoint → Your turn → Common problems.** Do exercise 1 in class; the rest are for after class.

> **About AI answers:** ChatGPT, Copilot and Claude answer differently, and even the same tool varies between runs. Mark your AI's answer with the checklist. If your tool isn't working, use the **sample AI answer** in the checkpoint.

**The stories we'll use** in Lectures 07–10:

| Story | Title | Acceptance criteria | Why it's useful |
|---|---|---|---|
| **US-205** | Apply coupon at checkout | AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.<br>AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".<br>AC3: Unknown codes show "Coupon code not recognised".<br>AC4: Only one coupon per order. | Our running example since Lecture 03: a boundary, exact messages, and an incomplete AC (AC4) |
| **US-311** | Fast search | AC1: Search results should appear fast. | Too vague to test ("fast" has no number). Used first in Topic 3 |
| **US-312** | Free gift wrap | AC1: Orders of 10 or more items get free gift wrap.<br>AC2: Orders under 10 items show "Add 10 items for free gift wrap". | A boundary with whole numbers (10 vs. 9) |

---

## Learning Objectives

By the end of this lecture you will be able to:

- Explain what an **AI agent** is, how it differs from a one-off prompt, and name its **six parts**.
- Describe **how our agent will run**: which steps code does, and which step you do in your AI tool.
- Write clear **agent instructions**: role, scope, rules, output and what to do when unsure.
- Write a **prompt template** with placeholders, fill it for a story and run it.

---

<a id="topic-1"></a>

# Topic 1: Agent Architecture

## Definition

An **AI agent** is an AI model set up to do **one specific job, the same way every time**. A one-off prompt is something you type once; an agent is a **package** you build once and reuse: fixed **instructions**, an **input template** that you fill with new data each time, a fixed **output format**, a few **examples** of good answers, and **checks** that test every answer. Our agent, **TestCaseDesigner**, has one job: turn **one user story** into **test cases** in a fixed JSON format. Building an agent is mostly careful writing and checking, not heavy programming.

## Key Ideas

1. **One-off prompt vs. agent:**

   | | One-off prompt | Agent |
   |---|---|---|
   | Written | Fresh each time | Once, then reused |
   | Instructions | Whatever you remember to type | The same tested instructions every run |
   | Answer format | Different every time | Fixed (JSON), so code can read it |
   | Checked? | By eye, if at all | Every answer, by a script and a person |

2. **The six parts of our agent:**

   | Part | What it does | File in your `agent` folder | Built in |
   |---|---|---|---|
   | **Role and goal** | Tells the AI who it is and its one job | Top of `instructions_v1.md` | Lecture 07 |
   | **Instructions (rules)** | What it must always / never do | `instructions_v1.md` | Lectures 07, 09 |
   | **Input template** | The fixed shape every story is sent in | `input_template.txt` | Lecture 07 |
   | **Output format** | The exact JSON it must reply with | Part of the instructions | Lecture 08 |
   | **Examples** | Good answers to copy the pattern from | `examples.txt` | Lecture 08 |
   | **Checks** | Code and human review of every answer | `check_reply.py` + a checklist | Lectures 09–10 |

3. **How our agent runs (this week):** code does everything **except** talk to the AI. You do that step in your AI tool.

   ```text
   stories/*.json ──► [CODE] build one prompt per story ──► prompts/v1/US-205.txt
                                                                  │
                                    🤖 YOU paste it into your AI tool (new chat)
                                                                  │
                      replies/v1/US-205.txt ◄── 📝 YOU save the AI's reply
                                │
               [CODE] check every reply ──► [CODE] write a results table ──► 👀 YOU review
   ```

   Next week, one small piece of code can replace the two "YOU" steps, and the agent will run on its own.
4. **One agent, one job.** "Design test cases for one story" is a good job. "Do all our testing" isn't. Small jobs are easier to check and improve.

## Worked Example: From a One-Off Prompt to an Agent

### Step 1 (🤖 AI tool): Try a one-off prompt

Open a **new chat** and paste:

```text
Write test cases for this user story.

US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

Read the reply. Note **how many** test cases it gave and **what format** it used (a list, a table, paragraphs?).

### Step 2 (🤖 AI tool): Run it again

Open **another new chat** and paste exactly the same text. Compare the two replies.

**What to notice:** different numbers of test cases, different formats, maybe different assumptions (did either one invent what happens with a second coupon?). A one-off prompt gives a **different shape every time**, so code can't read it reliably and nobody can compare runs. This is the problem an agent solves.

### Step 3 (✍️ Paper): Match the problems to the agent parts

For each problem you noticed, write which agent part (Key Idea 2) would fix it:

| Problem in Steps 1–2 | Agent part that fixes it |
|---|---|
| Different format each time | ? |
| Different number of test cases | ? |
| Invented behaviour for AC4 | ? |
| No way to know if the answer is good | ? |

### Step 4 (📝 Editor): Plan your agent folder

Your `agent` folder will grow like this over the next four lectures. Copy this plan into a file called `README.txt` in the folder, so you always know what goes where:

```text
agent/
├── instructions_draft.md   (Lecture 07)  first version of the instructions
├── input_template.txt      (Lecture 07)  the shape every story is sent in
├── contract.md             (Lecture 08)  what goes in and what must come out
├── examples.txt            (Lecture 08)  two good example answers
├── stories/                (Lecture 08)  the stories, one JSON file each
├── instructions_v1.md      (Lecture 09)  the finished instructions
├── build_prompts.py        (Lecture 09)  code: builds one prompt per story
├── check_reply.py          (Lecture 09)  code: checks one AI reply
├── prompts/  replies/      (Lecture 09)  prompts to paste / replies you save
├── run_agent.py            (Lecture 10)  code: runs everything and records results
├── results_v1.md           (Lecture 10)  results table written by run_agent.py
└── instructions_v1.1.md    (Lecture 10)  improved instructions, plus CHANGELOG.md
```

### Consolidated Result

Your completed Step 3 table and `README.txt` are the result. You now know the **parts** of the agent and **how it will run**.

## Checkpoint

**Answer key, Step 3:**

| Problem | Fixed by |
|---|---|
| Different format each time | **Output format** (a fixed JSON shape) |
| Different number of test cases | **Instructions** (a rule like "at most 5") and the **input template** (states the maximum) |
| Invented behaviour for AC4 | **Instructions** ("don't guess; ask a question") and **examples** showing how to ask |
| No way to know if the answer is good | **Checks** (a script plus a human checklist) |

**Steps 1–2 check:** most students see different numbers of test cases (often 6–15), different formats, and at least one run that **assumes** something about AC4 (for example "the second coupon replaces the first"). That's normal for a one-off prompt.

## Your Turn

1. **(In class, 3 min)** Compare your Step 1 reply with a classmate who used a **different** AI tool. List two differences.
2. **(After class)** Using Key Idea 3, explain in your own words which steps **code** will do and which step **you** will do in the AI tool.
3. **(After class)** Think of another one-job agent that would help a tester (for example "turn a bug description into a bug report"). Fill in the six parts from Key Idea 2 for it, one line each.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| Both runs in Step 2 look identical | You used the same chat, so the AI remembered the first answer | Always use a **new chat** for a fair comparison |
| The AI asks "What platform is this for?" | It's missing context | That's fine; note it. Agents remove this by giving context in the instructions |

---

<a id="topic-2"></a>

# Topic 2: Agent Instructions

## Definition

**Agent instructions** are the agent's **standing orders**: a fixed text that tells the AI **who it is, what its one job is, what's in and out of scope, which rules to follow, exactly what format to reply in, and what to do when something is unclear**. The same instructions are sent with **every** story, so every story gets the same treatment. Good instructions are **specific and checkable**: for every rule, you should be able to look at an answer and say whether the rule was followed. They are the most important part of the agent, and you'll improve them in Lecture 10.

## Key Ideas

1. **The five sections of our instructions:**

   | Section | Answers |
   |---|---|
   | **Role and goal** | Who are you, and what's your one job? |
   | **Scope** | What's in, and what's explicitly **out**? |
   | **Rules** | What must you always or never do? |
   | **Output** | Exactly what shape is the reply? |
   | **When something is unclear** | What do you do instead of guessing? |

2. **Every rule should be checkable.** "Write good tests" can't be checked. "Test the limit and just below it ($50.00 and $49.99)" can.
3. **Give the AI a way out.** "If unclear, ask a question" stops the AI from inventing answers (hallucinating).
4. **Instructions vs. prompt template:** the instructions **never change** between stories; the template (Topic 3) holds the part that **does** change: the story itself.

## Worked Example: Write `instructions_draft.md`

Build the file one section at a time.

### Step 1 (📝 Editor): Role and goal

Create `instructions_draft.md` in your `agent` folder and type:

```text
# TestCaseDesigner - Instructions (draft)

## Role and goal
You are TestCaseDesigner, a QA agent on an e-commerce test team.
Your job: turn ONE user story into functional test cases that a tester can review.
```

**Why:** the role sets the expertise. "ONE user story" in capitals stresses the unit of work, and "a tester can review" tells the AI what "good" means.

### Step 2 (📝 Editor): Scope

Add:

```text
## Scope
Only functional test cases for the acceptance criteria you are given.
No performance, security or accessibility tests. No automation code.
```

**Why:** AIs like to be "extra helpful". Each out-of-scope item is something an AI often adds when nobody tells it not to.

### Step 3 (📝 Editor): Rules

Add:

```text
## Rules
- Use only facts stated in the acceptance criteria. Do not invent rules or values.
- For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
- Copy expected messages exactly, character for character.
- Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
- Never return more than the maximum number of test cases.
```

**Why:** each rule fixes a mistake you've already seen this week: invented rules (Lecture 02), missed boundaries (Lecture 04), paraphrased messages (Lecture 05), and too many cases.

### Step 4 (📝 Editor): Output and "when unclear"

Add:

```text
## Output
Reply with ONE JSON object and nothing else. Keys:
- story_id: copied from the story
- status: "ok", or "needs_clarification" if no criterion can be tested
- test_cases: a list; each has id, title, ac_ids (a list), type
  (positive, negative or boundary), steps (a list), expected_result
- open_questions: a list of strings

## When something is unclear
- If a criterion is unclear or incomplete, do not guess. Add a question to
  open_questions that starts with the criterion id, e.g. "AC4: ...".
```

**Why:** the Output section is **format locking** (Lecture 03): every key is named, and "nothing else" stops extra chat. The last section gives the AI a **permitted alternative to guessing**, and says exactly **where** questions go. You'll study the output format in detail in Lecture 08.

### Step 5 (🤖 AI tool): Test the instructions

Open a **new chat**. Paste the **whole** of `instructions_draft.md`, then directly underneath it paste:

```text
### Story
ID: US-205
Title: Apply coupon at checkout
Maximum test cases: 5
Acceptance criteria:
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
### End of story

Now write the JSON reply for this story.
```

Send it as **one message**, and mark the reply with the Checkpoint checklist.

> **Why paste the instructions into the chat?** Chat tools don't let you set an agent's hidden standing orders, so pasting them at the top of the first message is the closest equivalent, and it works the same in ChatGPT, Copilot and Claude.

### Consolidated File: `instructions_draft.md`

```text
# TestCaseDesigner - Instructions (draft)

## Role and goal
You are TestCaseDesigner, a QA agent on an e-commerce test team.
Your job: turn ONE user story into functional test cases that a tester can review.

## Scope
Only functional test cases for the acceptance criteria you are given.
No performance, security or accessibility tests. No automation code.

## Rules
- Use only facts stated in the acceptance criteria. Do not invent rules or values.
- For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
- Copy expected messages exactly, character for character.
- Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
- Never return more than the maximum number of test cases.

## Output
Reply with ONE JSON object and nothing else. Keys:
- story_id: copied from the story
- status: "ok", or "needs_clarification" if no criterion can be tested
- test_cases: a list; each has id, title, ac_ids (a list), type
  (positive, negative or boundary), steps (a list), expected_result
- open_questions: a list of strings

## When something is unclear
- If a criterion is unclear or incomplete, do not guess. Add a question to
  open_questions that starts with the criterion id, e.g. "AC4: ...".
```

## Checkpoint

**Mark your AI's reply (Step 5):**

- ✅ JSON **only**, with no sentence before or after (some tools still add one; Lecture 09's checker handles that)
- ✅ All four keys: `story_id`, `status`, `test_cases`, `open_questions`
- ✅ IDs like `TC-205-01`, and **no more than 5** test cases
- ✅ Tests at **$50.00** and **$49.99**
- ✅ Messages copied **exactly** (`"Spend $50.00 to use SAVE10"`, `"Coupon code not recognised"`)
- ✅ An **open question about AC4** instead of invented behaviour

**Sample AI reply** (shortened; use it if your tool isn't working):

```json
{"story_id": "US-205", "status": "ok", "test_cases": [
 {"id": "TC-205-01", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
 {"id": "TC-205-02", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"],
  "expected_result": "Total stays $49.99 and \"Spend $50.00 to use SAVE10\" is shown"}
], "open_questions": ["AC4: What message is shown when a second coupon is entered?"]}
```

Compare it with your Topic 1 replies: the same story now comes back in a **fixed, checkable** shape.

## Your Turn

1. **(In class, 3 min)** Tick the checklist for your AI's reply. Which item failed, if any? Which **section** of the instructions should be improved to fix it?
2. **(After class)** Delete the **"When something is unclear"** section, run Step 5 again in a new chat, and look at AC4. Did the AI invent behaviour this time? Put the section back.
3. **(After class)** This rule is weak: *"Write good test cases."* Rewrite it as two specific, checkable rules.
4. **(After class)** Run Step 5 in a **different** AI tool. Does it follow the same instructions equally well?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI replies with a table, not JSON | The Output section was missed in the paste | Paste the **whole** file, then the story, in **one** message |
| The AI adds "Sure! Here's your JSON:" | Chat tools like to be friendly | Fine for now. The checker in Lecture 09 ignores text around the JSON |
| The AI invents what happens with a second coupon | The "unclear" rule was weak or missing | Check the last section is there; Lecture 08's examples make this stronger |

---

<a id="topic-3"></a>

# Topic 3: Prompt Templates

## Definition

A **prompt template** is the part of the prompt that **changes with every story**, written once with **placeholders** (blanks) such as `$story_id` and `$title`. To use it, you **fill** the placeholders with one story's details. The instructions stay the same; the template carries the data. Templates make the agent **consistent** (every story is presented in exactly the same shape, so the AI never has to guess where the criteria are) and **automatable**: in Lecture 09 a short script will fill the template for every story for you.

## Key Ideas

1. **Template = fixed text + `$placeholders`.** Each placeholder starts with `$` and is replaced by real data.
2. **Fence off the data.** `### Story` … `### End of story` shows the AI exactly where the story starts and ends (delimiters, Lecture 03).
3. **Same shape, every story.** If US-205 and US-311 are presented differently, the AI may treat them differently. A template prevents that.
4. **The full agent prompt** = instructions + (examples, from Lecture 08) + the **filled** template.

## Worked Example: Write and Fill `input_template.txt`

### Step 1 (📝 Editor): Write the template

Create `input_template.txt` in your `agent` folder:

```text
### Story
ID: $story_id
Title: $title
Maximum test cases: $max_cases
Acceptance criteria:
$acceptance_criteria
### End of story

Now write the JSON reply for this story.
```

**What's in it:** four placeholders (`$story_id`, `$title`, `$max_cases`, `$acceptance_criteria`), fences around the story, and a final line telling the AI what to do next.

### Step 2 (📝 Editor): Fill it by hand for US-311

We'll use **US-311**, one of the three stories listed at the start of this handout. Its details are:

| Placeholder | Value for US-311 |
|---|---|
| `$story_id` | US-311 |
| `$title` | Fast search |
| `$max_cases` | 3 |
| `$acceptance_criteria` | AC1: Search results should appear fast. |

Make a copy of `input_template.txt` called **`filled_US-311.txt`**, and in the copy replace each placeholder (including the `$`) with its value from the table. Leave everything else exactly as it is. The finished file is shown in the Checkpoint, so you can check yours.

### Step 3 (🤖 AI tool): Run the agent on US-311

Open a **new chat** and paste these two parts, one after the other, as **one message**:

1. The **whole** of `instructions_draft.md` (from Topic 2).
2. Directly underneath it, the **whole** of `filled_US-311.txt` (from Step 2). It should look exactly like this; if yours is different, fix it first:

```text
### Story
ID: US-311
Title: Fast search
Maximum test cases: 3
Acceptance criteria:
AC1: Search results should appear fast.
### End of story

Now write the JSON reply for this story.
```

Send the message and read the reply.

**What to look for:** "fast" has **no number**, so it can't be tested as written. A good reply should **not** invent a time limit (like "2 seconds"). It should ask a question in `open_questions` and, ideally, set `status` to `"needs_clarification"`.

### Step 4 (✍️ Paper): Notice the repetition

You just did by hand what a program will do in Lecture 09: take the instructions, fill the template with one story, and put them together. Imagine doing that for 30 stories. That's why we'll let code build the prompts, and why the template must be **exact**, with placeholder names that never change.

### Consolidated File: `input_template.txt`

```text
### Story
ID: $story_id
Title: $title
Maximum test cases: $max_cases
Acceptance criteria:
$acceptance_criteria
### End of story

Now write the JSON reply for this story.
```

Your `agent` folder now contains `README.txt`, `instructions_draft.md` and `input_template.txt`.

## Checkpoint

**Answer key, Step 2 (`filled_US-311.txt`):**

```text
### Story
ID: US-311
Title: Fast search
Maximum test cases: 3
Acceptance criteria:
AC1: Search results should appear fast.
### End of story

Now write the JSON reply for this story.
```

**Mark your AI's reply (Step 3):**

- ✅ JSON with the four keys, `story_id` = `"US-311"`
- ✅ An **open question** starting with `AC1:` asking for the time limit
- ✅ **No invented number** (no "within 2 seconds")
- ⭐ Best: `status` is `"needs_clarification"` and `test_cases` is empty

**Sample AI reply (a typical mistake):**

```json
{"story_id": "US-311", "status": "ok", "test_cases": [
 {"id": "TC-311-01", "title": "Search results appear within 2 seconds", "ac_ids": ["AC1"],
  "type": "positive", "steps": ["Open the search page", "Search for \"shoes\""],
  "expected_result": "Results are displayed within 2 seconds"}
], "open_questions": []}
```

The format is perfect, but **"2 seconds" was invented**. Our draft instructions don't yet say clearly enough what to do with an unmeasurable criterion. You'll fix that in Lecture 10, and Lecture 08's examples will already help.

## Your Turn

1. **(In class, 3 min)** Did your AI invent a time limit for US-311? Compare with a neighbour.
2. **(After class)** Make **`filled_US-312.txt`** the same way, for **US-312 Free gift wrap** (maximum 3): *AC1: Orders of 10 or more items get free gift wrap. AC2: Orders under 10 items show "Add 10 items for free gift wrap".* Run it with the instructions in a new chat. Did the AI test **10** and **9** items?
3. **(After class)** What would go wrong if someone renamed `$title` to `$name` in the template but nobody updated the program that fills it? (You'll see the answer in Lecture 09.)

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| A `$placeholder` was left in the prompt | You missed one when filling by hand | Search the filled text for `$` before pasting |
| The AI treats the story as part of the instructions | The fences are missing | Keep `### Story` and `### End of story` |
| The AI answers a different story | You pasted into an old chat | Always start a **new chat** per story |

---

## Lecture Wrap-Up: Quick Check

1. What's the difference between a one-off prompt and an agent?
2. Name the six parts of our agent.
3. In this week's agent, which step do **you** do in the AI tool, and what does code do?
4. Why does the "When something is unclear" section reduce hallucinations?
5. What changes between stories: the instructions or the template?

<details>
<summary>Answers</summary>

1. A one-off prompt is typed fresh and gives a different shape each time. An agent reuses the same instructions, template and output format, and its answers are checked.
2. Role and goal, instructions (rules), input template, output format, examples, checks.
3. You paste each prompt into your AI tool and save the reply. Code builds the prompts, checks the replies and records the results.
4. It gives the AI a permitted alternative to guessing: ask a question in `open_questions`.
5. The **template's data** (the story). The instructions stay the same.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **AI agent** | An AI model set up to do one job the same way every time, with fixed instructions, format, examples and checks |
| **One-off prompt** | A prompt typed fresh for a single answer |
| **Instructions** | The agent's standing orders, the same for every story |
| **Scope** | What the agent should and shouldn't do |
| **Prompt template** | Fixed text with `$placeholders`, filled with one story's data |
| **Placeholder** | A blank in a template, such as `$story_id` |
| **Delimiters** | Markers like `### Story` that fence off data |
| **needs_clarification** | The status the agent uses when it can't test a story without more information |

## Summary

- An **agent** is a reusable package: instructions, input template, output format, examples and checks, for **one job**.
- This week, **code** builds prompts, checks replies and records results; **you** run each prompt in your AI tool and save the reply.
- **Instructions** are the agent's standing orders: make every rule specific and checkable, and give the AI a way to say "I'm not sure".
- **Templates** hold the part that changes: every story is sent in exactly the same shape.
