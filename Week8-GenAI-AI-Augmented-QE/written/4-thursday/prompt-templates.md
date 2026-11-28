# Prompt Templates

## Learning Objectives

By the end of this lesson you will be able to:

- **Define** a prompt template and a placeholder, and explain how a template differs from the instructions.
- **Write** TestCaseDesigner's input template, with placeholders and delimiters.
- **Fill** the template by hand for a story, and check that no placeholder was left unfilled.
- **Explain** why every story must be sent in exactly the same shape.
- **Evaluate** the agent's reply for a vague story, and recognise an invented value even when the format is perfect.

---

## Why This Matters

In *Agent Instructions* you wrote the part of the agent that **never** changes. This lesson is about the part that **always** changes: the story.

You could, of course, just paste each story below the instructions however you like: a bullet list one day, a sentence the next, the ACs in a different order. Each change seems harmless.

But every difference in presentation is a difference the AI might react to. If US-205 arrives as a neat list with "Maximum test cases: 5" and US-311 arrives as a sentence with no maximum, the AI may treat them differently, and you will not know whether a difference in the replies came from the **story** or from the **way you typed it**.

A **prompt template** removes that doubt. Every story goes in exactly the same shape, so the only thing that changes between runs is the story itself. That is the same principle as a controlled experiment, and the same principle behind a test case template: change one thing at a time.

There is a second benefit, which you will use tomorrow. A template with clearly named blanks can be filled by a **program**. Filling one template by hand takes a minute. Filling it for thirty stories by hand takes half an hour and invites mistakes. A short script does it in a fraction of a second, the same way every time.

> **Using this with the handout:** this lesson goes deeper into **Handout 07, Topic 3**. It uses the same `input_template.txt`, the same US-311 values, the same `filled_US-311.txt`, the same checklist and the same sample mistake.

---

## The Concept

### 1. What Is a Prompt Template?

A **prompt template** is the part of the prompt that **changes with every story**, written once with **placeholders** (blanks) such as `$story_id` and `$title`. To use it, you **fill** the placeholders with one story's details.

The instructions stay the same; the template carries the data. That gives the agent two properties:

- **Consistent:** every story is presented in exactly the same shape, so the AI never has to guess where the criteria are.
- **Automatable:** a script can fill the template for every story, which you will do tomorrow.

A template is a familiar idea in disguise. A form with labelled boxes is a template. So is a bug report template in a test management tool, with fields for steps, expected and actual. What makes our template special is only that its reader is an AI, so the shape has to be exactly the same every time.

### 2. Placeholders

A **placeholder** is a named blank in the template. In our template, every placeholder starts with `$`:

| Placeholder | What it holds | US-205 value |
|---|---|---|
| `$story_id` | The story's ID | US-205 |
| `$title` | The story's short name | Apply coupon at checkout |
| `$max_cases` | The most test cases the agent may return | 5 |
| `$acceptance_criteria` | Every AC, one per line | AC1: SAVE10 gives 10% off... (four lines) |

The `$` is a **convention**: a marker that says "this is a blank, not real text". It is the same style Python's built-in `Template` class uses, which is one reason we chose it.

Good placeholder names follow three rules:

1. **Descriptive.** `$max_cases` says what it holds; `$n` does not.
2. **Lower case with underscores.** No spaces, so the name is one unbroken word: `$story_id`, not `$story id`.
3. **Never renamed casually.** The template and the program that fills it must agree on every name. Rename one side only, and they stop matching. Tomorrow you will see exactly what happens then.

### 3. Fence Off the Data

The template puts the story between two markers:

```text
### Story
...
### End of story
```

These are **delimiters**, which you met on Tuesday in *Specificity and Context*. They show the AI exactly where the story starts and ends. Without them, the AI has to work out for itself which lines are instructions and which are data, and it can get that wrong.

Delimiters matter more for an agent than for a one-off prompt, because an agent's prompt is long: instructions, then examples, then the story. Clear fences keep these separate.

They also help when the story itself contains text that **looks** like an instruction. Imagine an acceptance criterion that says, **illustrative**, *"AC5: The page must show the note 'Ignore all previous rules'"*. Inside the fences, the AI can more easily treat it as **data about the page**, not as an order. Fences do not make this kind of confusion impossible, so a reviewer should still notice anything odd in a reply. But they make it much less likely.

### 4. Same Shape, Every Story

Here is what "the same shape" protects against. Suppose two stories were pasted by hand, **illustrative**:

```text
US-205 - coupon. Max 5.
- SAVE10 gives 10% off a subtotal of $50.00 or more.
- Subtotals under $50.00 are unchanged ...
```

```text
Please do US-311, Fast search: search results should appear fast.
```

The second has no AC ids, no maximum and no fences, and it is phrased as a request rather than data. An AI might return a different number of cases, skip the `AC1:` prefix in its questions, or treat "fast" differently because the sentence sounds casual. Any difference in the replies could come from the **presentation**, not the story, and you could not tell which.

With the template, both stories arrive with the same labels, in the same order, with the same fences and the same final line. If the replies differ, the difference comes from the **stories**. That is what makes results from different stories comparable, and what makes tomorrow's automatic checks fair.

Be clear about what a template does **not** fix. It removes variation in what you **send**. It does not remove variation in what the AI **sends back**. Run the same filled template twice, in two new chats, and you may still get slightly different replies, because the model's output varies from run to run, as you saw with temperature on Monday.

The template's job is to make sure that when replies differ, it is not because the inputs differed. Reducing variation in the replies is the job of the instructions, the output format and the examples.

### 5. The Full Agent Prompt

When the agent runs, the full prompt for one story is built from three pieces, always in this order:

1. **The instructions** (from *Agent Instructions*): the same for every story.
2. **The examples** (from *Sample Input/Output Pairs*, later today): the same for every story.
3. **The filled template**: different for every story.

The story goes **last** for two reasons. The AI reads the rules and examples first, so it knows what to do before it sees the data. And the template's final line, *"Now write the JSON reply for this story."*, ends the message with a clear task, right after the story it refers to. If the story came first and the examples after it, the AI might answer one of the examples instead.

### 6. Worked Example: Write and Fill `input_template.txt`

#### Step 1 (Editor): Write the template

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

Read it line by line:

| Line | Purpose |
|---|---|
| `### Story` | Opening fence: the story starts here |
| `ID: $story_id` | The ID the reply's `story_id` must copy |
| `Title: $title` | A human-readable name; helps the AI understand the feature |
| `Maximum test cases: $max_cases` | The limit the "never more than the maximum" rule refers to |
| `Acceptance criteria:` then `$acceptance_criteria` | The ACs, one per line, each starting with its id |
| `### End of story` | Closing fence: the story ends here |
| `Now write the JSON reply for this story.` | The task, placed last |

Notice the `Maximum test cases` line. In *Agent Architecture*, the fix for "different number of test cases" needed **two** parts: a rule in the instructions and the maximum in the input. This is the second half. The rule says "never more than the maximum"; the template says what the maximum **is**, story by story.

#### Step 2 (Editor): Fill it by hand for US-311

We use **US-311**, one of the three stories for this part of the week. Its details:

| Placeholder | Value for US-311 |
|---|---|
| `$story_id` | US-311 |
| `$title` | Fast search |
| `$max_cases` | 3 |
| `$acceptance_criteria` | AC1: Search results should appear fast. |

Make a copy of `input_template.txt` called **`filled_US-311.txt`**. In the copy, replace each placeholder, **including the `$`**, with its value from the table. Leave everything else exactly as it is. The finished file should look exactly like this:

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

Check your file against this answer character by character. A missing colon after `AC1` or a changed word in the title is a small difference, but the point of a template is that **nothing** differs except the values.

Why fill a copy rather than the original? Because the template is reused for every story. If you overwrite it with US-311's values, the blanks are gone, and the next story has nothing to fill.

#### Step 3 (AI tool): Run the agent on US-311

Open a **new chat** and paste these two parts, one after the other, as **one message**:

1. The **whole** of `instructions_draft.md` (from *Agent Instructions*).
2. Directly underneath it, the **whole** of `filled_US-311.txt`.

Send the message and read the reply.

**What to look for:** "fast" has **no number**, so it cannot be tested as written. A good reply should **not** invent a time limit (like "2 seconds"). It should ask a question in `open_questions` and, ideally, set `status` to `"needs_clarification"`.

Mark your AI's reply:

- ✅ JSON with the four keys, `story_id` = `"US-311"`
- ✅ An **open question** starting with `AC1:` asking for the time limit
- ✅ **No invented number** (no "within 2 seconds")
- ⭐ Best: `status` is `"needs_clarification"` and `test_cases` is empty

#### Step 4 (Paper): Notice the repetition

You just did by hand what a program will do tomorrow: take the instructions, fill the template with one story, and put them together. Imagine doing that for 30 stories, every sprint. That is why code will build the prompts, and why the template must be **exact**, with placeholder names that never change.

### 7. A Typical Mistake: Perfect Format, Invented Value

Here is the handout's sample reply for US-311, showing a **typical mistake**:

```json
{"story_id": "US-311", "status": "ok", "test_cases": [
 {"id": "TC-311-01", "title": "Search results appear within 2 seconds", "ac_ids": ["AC1"],
  "type": "positive", "steps": ["Open the search page", "Search for \"shoes\""],
  "expected_result": "Results are displayed within 2 seconds"}
], "open_questions": []}
```

Check it against the checklist:

| Checklist item | Result |
|---|---|
| JSON with the four keys, `story_id` = `"US-311"` | ✅ Passed |
| An open question starting with `AC1:` | ❌ `open_questions` is empty |
| No invented number | ❌ **"2 seconds" was invented** |
| `status` is `"needs_clarification"` | ❌ It says `"ok"` |

The format is perfect. Every key is there, the ID follows the pattern, the type is a valid value. And the content is wrong in exactly the way that matters most: "2 seconds" appears nowhere in US-311. It is the **invented rule** problem from all week, now in a perfectly formatted agent reply.

This example teaches the most important lesson about formats: **a correct shape does not mean a correct answer.** A format check would pass this reply. Only a check that compares the reply with the **story**, or a person reading it, catches the invented value. You will write down exactly that kind of check in *Required Fields and Validation Rules*.

Why did the AI do it, despite the rule "Do not invent rules or values"? The draft instructions do not say clearly enough what to do when **no** criterion can be tested. The "when unclear" section talks about **a** criterion being unclear, and the `status` field mentions `needs_clarification`, but nothing **shows** the AI an example of refusing. Later today, *Sample Input/Output Pairs* adds exactly that example, and Friday adds a rule aimed at this mistake.

### 8. Checking a Filled Template

The handout's most common template problem is a **placeholder left in the prompt**: you missed one when filling by hand. Its advice: **search the filled text for `$` before pasting.**

That works for US-311. But try it on US-205, which is full of money:

```text
### Story
ID: US-205
Title: Apply coupon at checkout
Maximum test cases: $max_cases
Acceptance criteria:
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
...
```

Here `$max_cases` was missed. A search for `$` finds **three** lines, and only one of them is a problem: the other two are dollar amounts. On a long story, the real leftover is easy to overlook among the prices.

A slightly smarter search looks for `$` followed by **letters**, which is what a placeholder name looks like. This short script, `leftover_check.py`, does both searches so you can compare them:

```python
import re
import sys

text = open(sys.argv[1]).read()
print("Lines containing '$':", sum(1 for line in text.splitlines() if "$" in line))
leftovers = re.findall(r"\$[a-z_]+", text)      # $ followed by letters: a placeholder
print("Unfilled placeholders:", leftovers if leftovers else "none")
```

Running `python leftover_check.py filled_US-205.txt` on the file above prints:

```text
Lines containing '$': 3
Unfilled placeholders: ['$max_cases']
```

The pattern `\$[a-z_]+` means "a dollar sign, then one or more lower-case letters or underscores". `$50.00` does not match, because a digit follows the `$`. That is one more reason for the naming rules in section 2: placeholders that are always lower-case letters and underscores are easy to find, and easy to tell apart from data.

You do not need this script today; searching by eye is fine for one story. It is here to show the idea that tomorrow's prompt builder relies on: a template and its data must be **checkable**, and a check that confuses data with placeholders is not much help.

### 9. The Multi-Line Placeholder: `$acceptance_criteria`

Three of the four placeholders hold one short value. The fourth, `$acceptance_criteria`, holds **several lines**, and how those lines are written matters:

```text
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
```

Three habits keep it reliable:

- **One AC per line.** A paragraph containing three criteria invites the AI to miss one, and makes it impossible to say which AC a test case covers.
- **Every line starts with its id and a colon.** The instructions ask for `ac_ids` in every test case, and for open questions that start with the AC id. The AI can only copy ids that it can see. If the input says "SAVE10 gives 10% off..." with no `AC1:`, the reply's `ac_ids` will be guesses.
- **The text is copied exactly from the story.** Quotation marks, cents and capital letters stay as they are. The exact-message rule can only work if the message reaching the AI is the exact message.

The second habit links this placeholder to the checks you will meet later today. Rules that compare the reply with the story, such as "every AC id in the reply exists in the story", depend on the ids being present and consistent on **both** sides.

### 10. Template or Instructions? Where a Change Belongs

As the agent grows, you will want to add things. Some belong in the template, some in the instructions. The test is simple: **does it change from story to story?**

| What you want to add | Changes per story? | Where it goes |
|---|---|---|
| The environment the story runs in (web, mobile) | Yes | Template: a new placeholder such as `$platform` |
| A rule: "never test more than one AC per test case" | No | Instructions: a new line under Rules |
| A link to the story in the team's tracker | Yes | Template |
| The JSON format of the reply | No | Instructions (and the contract, later today) |
| A note that a story is a bug fix, not a new feature | Yes | Template |

Putting something in the wrong place causes trouble. A per-story detail written into the instructions is wrong for every other story. A fixed rule written into the template has to be copied into every filled file, and the copies drift apart. When in doubt, ask the question in the middle column.

Adding a placeholder is a **change to the template**, and like any change it should be deliberate. Tomorrow's program will fill exactly the placeholders it knows about. A new placeholder needs a matching value in every story file, or it will be left unfilled.

### 11. A Template for Another Agent

In *Agent Architecture* you designed **BugReportWriter**, an agent that turns a tester's rough notes into a structured bug report. Its input template follows the same pattern:

```text
### Notes
Story: $story_id
Environment: $environment
Tester's notes:
$notes
### End of notes

Now write the JSON bug report for these notes.
```

The same ideas are all here: named placeholders, fences around the data, and a final line that states the task. The only differences are the names and the job. Once you can write one template well, you can write them for any repeated task.

### 12. A Careful Routine for Filling by Hand

Until tomorrow, filling is a manual job. A routine that avoids the common problems:

1. **Copy** `input_template.txt` to `filled_<story id>.txt`.
2. **Replace one placeholder at a time**, including its `$`, working top to bottom.
3. **Check for leftovers**: search for `$` followed by letters.
4. **Compare** with the story: every AC present, one per line, ids and messages exact.
5. **Paste** instructions plus filled template into a **new chat**, as one message.

Step 4 is the one people skip. It is also the one that catches a missing AC, which no leftover search can find.

### 13. Templates Make Problems Visible

A fixed template has a quieter benefit: it makes problems with the **stories** easier to see. When every story is shown in the same shape, gaps stand out:

| What you notice when filling | What it tells you |
|---|---|
| There is no value for `$max_cases` | Nobody decided how many cases this story needs |
| An AC has no id | The story was written informally; ask for it to be fixed |
| The ACs are paragraphs, not one per line | The story may hide several criteria in one |
| The title says "Fast search" and the only AC says "fast" | The whole story may be vague, not just one AC |

That last row is exactly US-311. Filling the template forces you to look at the story's parts one by one, which is a small version of the requirements analysis you did on Wednesday. Sometimes the most useful result of filling a template is a question for the BA, before any AI is involved.

### 14. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| A `$placeholder` was left in the prompt | You missed one when filling by hand | Search the filled text for `$` followed by letters before pasting |
| The AI treats the story as part of the instructions | The fences are missing | Keep `### Story` and `### End of story` |
| The AI answers a different story | You pasted into an old chat | Always start a **new chat** per story |
| An AC is missing from the filled file | Copying several lines by hand is easy to get wrong | Compare the filled file with the story, AC by AC, before pasting |
| You overwrote `input_template.txt` with real values | You filled the original, not a copy | Keep the template blank; fill copies named `filled_<story>.txt` |
| A placeholder was renamed in one place only | The template and its filler no longer agree | Never rename a placeholder without updating everything that uses it |

---

## Practice Exercises

1. **Did it invent a number? (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** run Step 3 with `instructions_draft.md` and `filled_US-311.txt`.
   - **Review:** mark the reply with the checklist in Step 3.
   - **Run:** compare with a neighbour, or run it again in a different AI tool.
   - **Record:** in `prompts.txt`, note whether a time limit was invented and what `status` was.

2. **Fill US-312 (editor and AI tool, 15 min).** Make **`filled_US-312.txt`** the same way, for **US-312 Free gift wrap** (maximum 3): *AC1: Orders of 10 or more items get free gift wrap. AC2: Orders under 10 items show "Add 10 items for free gift wrap".* Put each AC on its own line. Run it with the instructions in a new chat. Did the AI test **10** and **9** items, and copy the AC2 message exactly?

3. **What breaks? (paper, 5 min).** What could go wrong if someone renamed `$title` to `$name` in the template, but nobody updated the program that fills it? Write your prediction; tomorrow you will see the answer.

4. **Find the leftover (paper or code, 10 min).** Fill the template for US-205, but deliberately leave `$max_cases` unfilled. Search for `$` by eye and count the matches. Then, if you like, run `leftover_check.py` on it. Which search would you trust on a story with ten prices in it?

5. **Same input, different output (AI tool, 10 min).** Paste your instructions and `filled_US-312.txt` into **two** new chats. Compare the replies field by field. What stayed the same, and what changed? Which agent part would you improve to reduce the differences?

---

## Knowledge Check

1. What is a prompt template, and what is a placeholder?

<details><summary>Answer</summary>

A prompt template is the part of the prompt that changes with every story, written once with placeholders. A placeholder is a named blank, such as `$story_id`, that is replaced with real data.

</details>

2. What changes between stories: the instructions or the template's data?

<details><summary>Answer</summary>

The template's data: the story. The instructions stay the same.

</details>

3. Why does the template put the story between `### Story` and `### End of story`?

<details><summary>Answer</summary>

These delimiters show the AI exactly where the story starts and ends, so it does not confuse the story with the instructions or examples.

</details>

4. Why does the filled template go last in the full agent prompt?

<details><summary>Answer</summary>

So the AI reads the rules and examples first, and the message ends with the task right after the story it refers to. If examples came after it, the AI might answer an example instead.

</details>

5. The sample US-311 reply has all four keys and a valid ID. Why is it still wrong?

<details><summary>Answer</summary>

It invented "2 seconds", which is not in the story. It should have set `status` to `"needs_clarification"` and asked an AC1 question. A correct format does not mean a correct answer.

</details>

6. Why can searching a filled US-205 prompt for `$` be misleading?

<details><summary>Answer</summary>

US-205 contains dollar amounts such as $50.00, so the search finds lines that are fine. A real leftover such as `$max_cases` is easy to miss among them. Searching for `$` followed by letters finds only placeholders.

</details>

7. Why should you fill a copy of the template, not the template itself?

<details><summary>Answer</summary>

The template is reused for every story. Overwriting it removes the placeholders, so the next story has no blanks to fill.

</details>

8. You want the agent to know whether each story is for the web or the mobile app. Should this go in the instructions or the template?

<details><summary>Answer</summary>

The template, as a new placeholder such as `$platform`, because it changes from story to story. Fixed rules go in the instructions.

</details>

---

## Glossary

- **Prompt template:** fixed text with placeholders, filled with one story's data for each run.
- **Placeholder:** a named blank in a template, such as `$story_id`.
- **Filling a template:** replacing every placeholder with its value for one story.
- **Delimiters:** markers such as `### Story` and `### End of story` that fence off data.
- **Full agent prompt:** instructions, then examples, then the filled template.
- **Fence (delimiter):** the opening or closing marker around data, such as `### Story`.
- **Template change:** any change to the template's text or placeholders; it must be matched in every story file and in the program that fills it.
- **Leftover placeholder:** a placeholder that was not replaced, so it reaches the AI as `$name`.
- **Convention:** an agreed way of doing something, such as starting placeholders with `$`.
- **Consistent presentation:** sending every story in exactly the same shape, so differences in replies come from the stories.
- **Multi-line placeholder:** a placeholder, such as `$acceptance_criteria`, that is filled with several lines.
- **Invented value:** a number or fact in a reply that does not appear in the story, such as "2 seconds".

---

## Summary

- A **prompt template** holds the part that changes: the story, in **exactly the same shape** every time.
- **Placeholders** (`$story_id`, `$title`, `$max_cases`, `$acceptance_criteria`) are filled with each story's data, in a **copy** of the template.
- **Fences** separate the story from the instructions and examples, and the story goes **last**.
- The US-311 sample reply had a **perfect format and an invented value**: a correct shape does not mean a correct answer.
- Filling templates by hand is slow and error-prone. Tomorrow, code does it, which is why placeholder names must be exact and never change.

---

## Additional Resources

- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API* (separating instructions and context): https://help.openai.com/en/articles/6654000
- Python documentation, *string — Template strings*: https://docs.python.org/3/library/string.html#template-strings
- Anthropic, *Prompt engineering overview*: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
