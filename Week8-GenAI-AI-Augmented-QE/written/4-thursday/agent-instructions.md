# Agent Instructions

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what agent instructions are and why they are the most important part of an agent.
- **Write** instructions with five sections: role and goal, scope, rules, output, and what to do when something is unclear.
- **Rewrite** vague rules as specific, checkable ones.
- **Explain** why giving the AI a "way out" reduces invented answers.
- **Test** a set of instructions with a real story, and trace a failed check back to the section that needs improving.

---

## Why This Matters

In *Agent Architecture* you met the six parts of TestCaseDesigner. Of those six, the **instructions** do the most work. They are sent with every story, so every strength and every weakness in them is repeated on every run. A vague rule produces vague test cases for **every** story. A missing rule lets the same mistake through **every** time.

This is not a new skill. On Tuesday you learned the principles of good prompts: a role, a precise task, context, delimiters, a locked format and a way out. Agent instructions use all of them. The difference is that they are written **once**, tested carefully, and then reused, so they deserve far more care than a prompt you type once.

The guides from the companies that build these models say the same. OpenAI's guide to building agents advises giving models smaller, clearer steps, to minimise ambiguity and help the model follow instructions better ([OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)). The test of good instructions, in this lesson, is simple and very testerly: **for every rule, can you look at an answer and say whether the rule was followed?**

> **Using this with the handout:** this lesson goes deeper into **Handout 07, Topic 2**. It uses the same five sections, the same `instructions_draft.md`, the same US-205 test, the same checklist and the same sample reply.

---

## The Concept

### 1. What Are Agent Instructions?

**Agent instructions** are the agent's **standing orders**: a fixed text that tells the AI:

- **who it is**, and what its **one job** is;
- what is **in and out of scope**;
- which **rules** to follow;
- **exactly what format** to reply in;
- and **what to do when something is unclear**.

The same instructions are sent with **every** story, so every story gets the same treatment. That is what makes the agent's answers comparable from one story to the next.

Good instructions are **specific and checkable**. That phrase is the heart of this lesson, and it comes straight from testing: a requirement is testable when you can write a pass/fail test for it. A rule in the instructions is useful when you can look at a reply and say **"followed" or "not followed"**. You will improve these instructions on Friday, using exactly that test.

### 2. The Five Sections

TestCaseDesigner's instructions have five sections, each answering one question:

| Section | Answers |
|---|---|
| **Role and goal** | Who are you, and what is your one job? |
| **Scope** | What is in, and what is explicitly **out**? |
| **Rules** | What must you always or never do? |
| **Output** | Exactly what shape is the reply? |
| **When something is unclear** | What do you do instead of guessing? |

The order matters. The role sets the point of view for everything after it. Scope limits the job before any rules are given. The rules shape the content, the output section shapes the form, and the last section handles the cases the rules do not cover. A reader, human or AI, can follow the instructions top to bottom without needing to jump back.

### 3. Checkable Rules

The handout's key idea: **every rule should be checkable.** "Write good tests" cannot be checked. "Test the limit and just below it ($50.00 and $49.99)" can.

Here are some rules an inexperienced agent builder might write, and checkable versions of each:

| Vague rule | Why it cannot be checked | Checkable version |
|---|---|---|
| "Write good test cases" | What is "good"? | "Every test case names at least one AC id" and "Every expected result states an exact value or message" |
| "Cover the edge cases" | Which ones? | "For every numeric limit, test the limit and just below it" |
| "Be accurate with messages" | How accurate? | "Copy expected messages exactly, character for character" |
| "Don't write too many" | How many is too many? | "Never return more than the maximum number of test cases" |
| "Use a sensible ID format" | Sensible to whom? | "Number test cases TC-<story number>-<two digits>, e.g. TC-205-01" |
| "Don't make things up" | Hard to check alone | "Use only facts stated in the acceptance criteria" plus the "when unclear" section |

Two patterns stand out. Checkable rules often contain a **number** or an **example** ("e.g. TC-205-01", "$50.00 and $49.99"). And some vague rules split into **two** checkable ones, because "good" usually means several different things.

There is a practical reason this matters beyond clarity. Tomorrow you will write `check_reply.py`, which checks replies automatically. Code can only check rules that are checkable. Writing checkable rules today is what makes automatic checking possible tomorrow.

### 4. Give the AI a Way Out

The third key idea is one you met on Tuesday: **give the AI a way out.**

When a prompt demands test cases and the story is vague, the AI is stuck between two bad choices: refuse (which the prompt did not allow) or invent something (which looks like obeying). Most AIs choose to invent. US-311 says "search results should appear fast", and without a way out, a typical reply invents "within 2 seconds".

A **way out** is an explicit, permitted alternative to guessing. TestCaseDesigner's is:

```text
## When something is unclear
- If a criterion is unclear or incomplete, do not guess. Add a question to
  open_questions that starts with the criterion id, e.g. "AC4: ...".
```

It works because it does three things:

1. It **names the situation**: "unclear or incomplete".
2. It **forbids the bad behaviour**: "do not guess".
3. It **gives a specific alternative, and says where it goes**: a question, in `open_questions`, starting with the AC id.

The third point is what turns a hope into a rule. "Ask if unsure" is a hope. "Add a question to `open_questions` that starts with the criterion id" is checkable: you can look at the reply and see whether an AC4 question is there.

### 5. Instructions vs Template

The last key idea separates two things that are easy to mix up:

| | Instructions | Prompt template |
|---|---|---|
| Changes between stories? | **Never** | Yes: it carries the story |
| Contains | Role, scope, rules, output, "when unclear" | The story's ID, title, maximum and ACs |
| File | `instructions_draft.md` | `input_template.txt` (next lesson) |

Keeping them apart has a practical benefit. When you improve a rule, you change **one** file, and every story benefits. When you add a story, you change **no** instructions at all. If the story text were mixed into the instructions, every story would need its own copy, and an improvement would have to be made in every copy.

### 6. Worked Example: Write `instructions_draft.md`

Build the file one section at a time, in your `agent` folder.

#### Step 1 (Editor): Role and goal

Create `instructions_draft.md` and type:

```text
# TestCaseDesigner - Instructions (draft)

## Role and goal
You are TestCaseDesigner, a QA agent on an e-commerce test team.
Your job: turn ONE user story into functional test cases that a tester can review.
```

**Why:** the role sets the expertise, and "e-commerce test team" gives context, so the AI does not have to ask what kind of product this is. "ONE user story" in capitals stresses the unit of work. "That a tester can review" tells the AI what "good" means: something a person will read and judge, not something to impress.

#### Step 2 (Editor): Scope

Add:

```text
## Scope
Only functional test cases for the acceptance criteria you are given.
No performance, security or accessibility tests. No automation code.
```

**Why:** AIs like to be "extra helpful". Each out-of-scope item is something an AI often adds when nobody tells it not to. Without this section, a reply for US-205 might include "verify the coupon field resists SQL injection" or a Playwright script. Both might be useful one day, but neither is this agent's job, and both make the reply harder to check.

Notice that scope has two halves: what is **in** ("only functional test cases for the acceptance criteria you are given") and what is **out** (the named exclusions). The "out" list is not complete, and cannot be, but it names the additions that are most likely.

#### Step 3 (Editor): Rules

Add:

```text
## Rules
- Use only facts stated in the acceptance criteria. Do not invent rules or values.
- For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
- Copy expected messages exactly, character for character.
- Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
- Never return more than the maximum number of test cases.
```

**Why:** each rule fixes a mistake you have already seen this week:

| Rule | The mistake it prevents | Where you saw it |
|---|---|---|
| Use only facts stated | Invented rules ("lowercase save10 works") | *Generative AI Concepts* (Monday) and all week |
| Test the limit and just below | Missed boundaries | *AI-Assisted Test Design* (Tuesday) |
| Copy messages exactly | Paraphrased messages ("Spend $50 to use SAVE10") | *AI-Generated Test Cases* (Wednesday) |
| Number TC-<story>-<two digits> | IDs nobody can refer to consistently | *AI-Generated Test Cases* (Wednesday) |
| Never more than the maximum | Too many cases to review | *Agent Architecture* (6 to 15 cases per run) |

A rule written from a real, observed mistake is almost always a good rule: you know it is needed, and you know what "followed" looks like.

#### Step 4 (Editor): Output and "when unclear"

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

**Why:** the Output section is **format locking**, from Tuesday: every key is named, and "nothing else" stops the AI adding chat before or after the JSON. The `status` field gives the agent a way to say **"I can't test this story at all"**, which matters for US-311. The last section is the way out from section 4.

The output format is only sketched here. In *Input/Output Contracts* you will write it down exactly, field by field, and in *JSON Schema* you will see it in a form a computer can check.

#### The consolidated file

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

#### Step 5 (AI tool): Test the instructions

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

Send it as **one message**.

Why paste the instructions into the chat? Chat tools do not let you set an agent's hidden standing orders, so pasting them at the top of the first message is the closest equivalent, and it works the same in ChatGPT, Copilot and Claude. When developers build agents with code, they usually send instructions separately, as a **system message**: a part of the request that sets the model's behaviour before the user's message. The idea is the same; only the delivery differs.

### 7. Marking the Reply

Mark your AI's reply with the handout's checklist:

- ✅ JSON **only**, with no sentence before or after (some tools still add one; tomorrow's checker handles that)
- ✅ All four keys: `story_id`, `status`, `test_cases`, `open_questions`
- ✅ IDs like `TC-205-01`, and **no more than 5** test cases
- ✅ Tests at **$50.00** and **$49.99**
- ✅ Messages copied **exactly** (`"Spend $50.00 to use SAVE10"`, `"Coupon code not recognised"`)
- ✅ An **open question about AC4** instead of invented behaviour

Here is the handout's sample reply, shortened, for use if your tool is not working:

```json
{"story_id": "US-205", "status": "ok", "test_cases": [
 {"id": "TC-205-01", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
 {"id": "TC-205-02", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"],
  "expected_result": "Total stays $49.99 and \"Spend $50.00 to use SAVE10\" is shown"}
], "open_questions": ["AC4: What message is shown when a second coupon is entered?"]}
```

Compare it with your replies in *Agent Architecture*. The same story now comes back in a **fixed, checkable** shape, and AC4 produced a **question**, not an invented rule.

Every item on the checklist maps to a section of the instructions. That mapping is how you improve them:

| Checklist item failed | Section to improve |
|---|---|
| Extra text around the JSON | Output ("nothing else") |
| A key missing | Output (the list of keys) |
| Wrong ID format, or too many cases | Rules |
| No $49.99 case | Rules (the boundary rule) |
| A paraphrased message | Rules (the exact-message rule) |
| Invented AC4 behaviour | When something is unclear |

Reading a reply this way is a skill you will use all of Friday: **don't just fix the reply; find the section that allowed the mistake.**

### 8. Instruction Smells

A **smell** is a warning sign that something is probably wrong, even if it has not caused a problem yet. Instructions have their own smells:

| Smell | Example | Problem |
|---|---|---|
| **Vague words** | "Write good, thorough tests" | Cannot be checked (section 3) |
| **Contradiction** | "Write at least 6 test cases" plus "Maximum test cases: 5" | The AI must break one rule; you cannot predict which |
| **Only negatives** | "Don't guess" with no alternative | The AI still has to do something, so it guesses anyway |
| **Hidden assumption** | "Use the usual ID format" | The AI does not know your "usual" |
| **Wall of text** | Rules written as one long paragraph | Rules get missed, by the AI and by reviewers |
| **Rule nobody checks** | A rule no checklist item or script tests | Breaking it goes unnoticed |

The **contradiction** smell is the most dangerous, because each rule looks reasonable on its own. It often appears when instructions grow over time: someone adds "at least 6" to get more coverage, forgetting the maximum set elsewhere. Read the whole file every time you change it, not just the line you added.

The **only negatives** smell explains why the "when unclear" section matters so much. "Do not guess" alone is a negative. Paired with "add a question to `open_questions`", it becomes a choice the AI can actually make.

### 9. Testing the Instructions

Instructions are a kind of code: they control behaviour, so they should be **tested**. Two simple tests, from the handout's Your Turn exercises:

**Remove a section and see what changes.** Delete the "When something is unclear" section, run Step 5 again in a **new chat**, and look at AC4. A typical result, **illustrative**, is a test case such as *"TC-205-05: Second coupon replaces the first"*, with an invented expected result, and an empty `open_questions` list. Put the section back.

You have just proved that the section is doing real work. Testers call this kind of experiment, removing one part to see its effect, a **controlled change**: everything else stays the same, so any difference is caused by the part you removed.

**Run the same instructions in a different AI tool.** Instructions that work only in one tool are fragile. If ChatGPT follows the exact-message rule but another tool paraphrases, the rule may need to be stronger or clearer, for example by adding an example of an exactly copied message. On Friday you will see that examples are often the fix.

Both tests use the checklist from section 7 to compare results, so "it seemed better" becomes "it passed 6 of 6 checks instead of 4 of 6".

### 10. One Set of Instructions, Three Different Stories

The instructions must work for **every** story, not just US-205. A good habit is to read each rule against each story before running anything, and predict what a correct reply should contain:

| Rule or section | US-205 (coupon) | US-311 (fast search) | US-312 (gift wrap) |
|---|---|---|---|
| Use only facts stated | No lowercase rule; no AC4 behaviour | **No** time limit may be invented | No rule for exactly how wrap is offered |
| Limit and just below | $50.00 and $49.99 | No numeric limit at all | **10 and 9** items |
| Copy messages exactly | "Spend $50.00 to use SAVE10", "Coupon code not recognised" | No message | "Add 10 items for free gift wrap" |
| Maximum test cases | 5 | 3 | 3 |
| When unclear | A question starting "AC4:" | A question starting "AC1:" asking for the time | Probably none needed |
| Expected `status` | `"ok"` | `"needs_clarification"` | `"ok"` |

This table is a small **test plan for the instructions**. It turns "does the agent work?" into specific expectations, story by story. Notice how differently the same rules play out. For US-312, the boundary rule means whole numbers of items, not dollars: the "e.g. $50.00 and $49.99" in the rule is only an example, and a good reply generalises it to 10 and 9. For US-311, the most important rule is the one that says **do not** do something: invent a number.

US-311 is also where the draft instructions are weakest. The "when unclear" section says what to do with an unclear criterion, but it does not say clearly what to do when **every** criterion is unclear. You will see in the next lesson that some AIs still produce an invented test case for US-311. That is not a failure of this lesson; it is exactly the kind of finding that drives the improvements on Friday.

### 11. Write for Human Readers Too

The AI is not the only reader of your instructions. A reviewer reads them to understand why the agent behaved as it did. A teammate reads them before changing a rule. **You** read them next month, having forgotten why a rule is there.

Three habits help every reader:

- **One rule per line**, as bullets. Easy to scan, easy to quote in a review comment, easy to change.
- **Plain words.** If a new team member would not understand a rule, an AI may not follow it reliably either.
- **Record the reason somewhere.** The instructions themselves should stay short, but each rule's reason belongs in a changelog or review note: "Added the exact-message rule after replies paraphrased the AC2 message." On Friday this becomes `CHANGELOG.md`.

### 12. Instructions Are Versioned

The file is called `instructions_draft.md` for a reason. It will change:

- **Today:** `instructions_draft.md`, tested on one story.
- **Friday:** `instructions_v1.md`, the finished version the agent runs with.
- **Friday, after testing:** `instructions_v1.1.md`, improved from what the results show, with a `CHANGELOG.md` explaining each change.

Keeping old versions matters for the same reason test results matter: when a change makes things worse, you need to know what changed and be able to go back. It also lets you compare versions fairly: the same stories, run with v1 and with v1.1, show whether a change helped.

### 13. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI replies with a table, not JSON | The Output section was missed in the paste | Paste the **whole** file, then the story, in **one** message |
| The AI adds "Sure! Here's your JSON:" | Chat tools like to be friendly | Fine for now. Tomorrow's checker ignores text around the JSON |
| The AI invents what happens with a second coupon | The "unclear" rule was weak or missing | Check the last section is there. Examples, later today, make this stronger |
| The AI writes performance or security tests | The scope section was missing or vague | Name the out-of-scope items explicitly |
| Two rules contradict each other | Instructions grew without a full re-read | Re-read the whole file after every change |

---

## Practice Exercises

1. **Tick the checklist (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** run Step 5 with your `instructions_draft.md`.
   - **Review:** tick each item on the checklist in section 7.
   - **Run:** if any item failed, use the table in section 7 to find the section to improve, change one line, and run again in a new chat.
   - **Record:** in `prompts.txt`, note which item failed, what you changed, and whether it helped.

2. **Remove the way out (AI tool, 10 min).** Delete the "When something is unclear" section, run Step 5 again in a new chat, and look at AC4. Did the AI invent behaviour this time? Put the section back.

3. **Make it checkable (paper, 10 min).** This rule is weak: *"Write good test cases."* Rewrite it as **two** specific, checkable rules. For each, write how you would check it in a reply.

4. **Different tool (AI tool, 15 min).** Run Step 5 in a **different** AI tool. Mark both replies with the checklist. Does the second tool follow the same instructions equally well? Which rule, if any, does it break?

5. **Find the smell (paper, 5 min).** Which smells from section 8 does this rule set have? *"Write thorough tests. Use our normal ID style. Don't guess. Always write at least 8 test cases. Maximum test cases: 5."*

---

## Knowledge Check

1. Name the five sections of TestCaseDesigner's instructions.

<details><summary>Answer</summary>

Role and goal, scope, rules, output, and when something is unclear.

</details>

2. What makes a rule "checkable"?

<details><summary>Answer</summary>

You can look at a reply and say clearly whether the rule was followed. Checkable rules often contain a number, an exact format or an example.

</details>

3. Why does the "When something is unclear" section reduce invented answers?

<details><summary>Answer</summary>

It gives the AI a permitted alternative to guessing: add a question to `open_questions`, starting with the AC id. Without it, the AI's easiest option is to invent a value.

</details>

4. What is the difference between the instructions and the prompt template?

<details><summary>Answer</summary>

The instructions never change between stories. The template carries the part that changes: the story itself.

</details>

5. Why does the Scope section name specific exclusions, such as performance and security tests?

<details><summary>Answer</summary>

AIs like to be extra helpful and often add them when not told otherwise. Naming them makes the reply smaller and easier to check.

</details>

6. A reply paraphrases "Spend $50.00 to use SAVE10". Which section should you improve?

<details><summary>Answer</summary>

The Rules section, specifically the exact-message rule. You might strengthen it or, later, add an example showing a message copied exactly.

</details>

7. The instructions say "Write at least 6 test cases" and the story says "Maximum test cases: 5". What smell is this, and why is it dangerous?

<details><summary>Answer</summary>

A contradiction. The AI must break one of the rules, and you cannot predict which one, so results become inconsistent.

</details>

8. How can you prove that a section of the instructions is doing real work?

<details><summary>Answer</summary>

Make a controlled change: remove only that section, run the same story in a new chat, and compare the replies with the checklist.

</details>

---

## Glossary

- **Agent instructions:** the agent's standing orders, the same for every story.
- **Role and goal:** who the AI is and what its one job is.
- **Scope:** what the agent should and should not do.
- **Checkable rule:** a rule whose effect you can confirm by looking at a reply.
- **Way out:** an explicit, permitted alternative to guessing, such as asking a question.
- **`needs_clarification`:** the status the agent uses when it cannot test a story without more information.
- **System message:** a part of an AI request, used when building with code, that sets the model's behaviour before the user's message.
- **Instruction smell:** a warning sign of a likely problem in instructions, such as a contradiction.
- **Contradiction:** two rules that cannot both be followed.
- **Controlled change:** changing one thing only, so any difference in results is caused by that change.
- **Test plan for instructions:** a table of what a correct reply should contain for each story, written before running the agent.
- **Versioning:** keeping numbered versions of a file, so changes can be compared and undone.

---

## Summary

- **Instructions are the agent's standing orders**, sent with every story, so their strengths and weaknesses repeat on every run.
- Use **five sections**: role and goal, scope, rules, output, and when something is unclear.
- Make **every rule checkable**. A rule written from an observed mistake usually is.
- **Give the AI a way out**: name the situation, forbid guessing, and say exactly where the question goes.
- **Test the instructions** with a checklist, and when a check fails, **fix the section that allowed it**, not just the reply.

---

## Additional Resources

- OpenAI, *A practical guide to building agents* (PDF; see the section on instructions): https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- OpenAI, *Prompt engineering* guide: https://developers.openai.com/api/docs/guides/prompt-engineering
- Anthropic, *Prompt engineering overview*: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
