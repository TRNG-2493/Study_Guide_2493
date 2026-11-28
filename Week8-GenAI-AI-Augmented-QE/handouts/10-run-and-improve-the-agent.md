# Week 08 · Lecture 10: Run and Improve the Agent

**Topics:**

1. [Agent Output Validation](#topic-1)
2. [Building Validation Scripts](#topic-2)
3. [Executing Agents against QA Requirements](#topic-3)
4. [Agent Testing and Refinement](#topic-4)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Open your `week08/agent` folder from Lecture 09. It should contain `instructions_v1.md`, `examples.txt`, `input_template.txt`, `contract.md`, `build_prompts.py`, `check_reply.py`, the `stories` folder, and the `prompts/v1` and `replies/v1` folders with **three replies** (your AI's, or the sample replies from Lecture 09).
> 2. Open a terminal **inside the `agent` folder**. Nothing to install.
> 3. Open your AI assistant: **ChatGPT, Copilot Chat or Claude**.

---

## How to Use This Handout

**Every step tells you where to do it:**

| Label | Where | What you do |
|---|---|---|
| 🤖 **AI tool** | ChatGPT, Copilot Chat or Claude | Open a **new chat**, paste exactly what the step says, and read the reply |
| 📝 **Editor** | VS Code (or any editor) | Create or edit a file in your `agent` folder |
| 💻 **Terminal** | Terminal, inside the `agent` folder | Run the command shown |
| ✍️ **Paper** | Pen and paper, or a text file | Work something out yourself |

Today you **finish** the agent: review its answers properly, run it over the whole backlog with one command, and **improve** it with evidence. You'll write **no new checking code**. You'll add one ready-made file, `run_agent.py`, which reuses your two files from Lecture 09.

> **About AI answers:** your AI's replies will differ from the samples. The checkpoints show results for the **sample replies**, so everyone has a common reference. Compare your own results with them.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Validate agent answers in **two layers**: the checker script (contract) and a **human checklist** (meaning).
- Run the agent over **every story with one command**, and read the results table.
- Execute the agent on a **new requirement** end to end, and decide what happens to each result.
- **Improve** the agent: find the most common failures, write a new instructions version, rerun and compare.

---

<a id="topic-1"></a>

# Topic 1: Agent Output Validation

## Definition

**Agent output validation** means checking every answer **before anyone uses it**, in two layers. The **checker script** tests the contract: the JSON, the required fields and rules R1–R4 and Q1. It's fast and always gives the same result, but it can't understand meaning. The **human review** checks what code can't: invented rules or values, missing boundaries, messages not copied exactly, and whether the agent should have refused. A reply is only **accepted** when it passes **both** layers. A script "PASS" means "well-formed", **not** "correct".

## Key Ideas

1. **Two layers, different jobs:**

   | Layer | Checks | Strength | Blind spot |
   |---|---|---|---|
   | 🐍 **Script** (`check_reply.py`) | JSON, fields, R1–R4, Q1 | Fast, identical every time | Can't see invented values or meaning |
   | 👀 **Human checklist** | H1–H4 (below) | Understands meaning | Slower; needs care |

2. **The human checklist:**

   | ID | Question | Linked instruction rule |
   |---|---|---|
   | **H1** | Is every rule or value in the test cases actually in the story? | G1 |
   | **H2** | Is every numeric limit tested at the limit **and** just below it? | B1 |
   | **H3** | Is every message copied **exactly**? | M1 |
   | **H4** | Is the status right? (A story with no measurable value should be `needs_clarification`) | U1 |

3. **Every reply gets a decision:**

   | Script | Human | Decision |
   |---|---|---|
   | PASS | OK | ✅ **Accept**: the test cases go to the tester |
   | FAIL | (any) | 🔧 **Fix the instructions** or rerun |
   | PASS | Problem found | 🔧 **Fix the instructions**: the script missed it |
   | PASS, `needs_clarification` | OK | ❓ **Send the questions to the BA** |

4. **Record why.** For every problem, note which rule (R…, Q…, H…) it breaks. In Topic 4 those notes tell you exactly what to improve.

## Worked Example: Review the Three v1 Replies

The checkpoint answers below use the **sample replies** from Lecture 09. If you used your own AI's replies, follow the same steps with yours.

### Step 1 (💻 Terminal): Get the script verdicts

Run the checker for each story. In `check_reply.py`'s bottom block, change the two file names to each story in turn (as in Lecture 09, exercise 1), and run:

```bash
python check_reply.py
```

Write down PASS or FAIL and the problems for US-205, US-311 and US-312. (In Topic 2 a runner will do this for every story in one go.)

### Step 2 (✍️ Paper): Human review with the checklist

Open each reply in your editor and answer H1–H4 for it:

| Story | H1 nothing invented? | H2 boundaries? | H3 exact messages? | H4 right status? |
|---|---|---|---|---|
| US-205 | | | | |
| US-311 | | | | |
| US-312 | | | | |

**Tips:** for US-205, look closely at **TC-205-05**. For US-311, ask: is "2 seconds" anywhere in the story? For US-312, compare TC-312-02's expected result with AC2's message.

### Step 3 (🤖 AI tool): Get a second opinion (optional)

AI can help with the human checklist, but it doesn't replace you. Open a **new chat** and paste:

```text
Review this AI-generated reply against the user story. Answer each question with Yes or No and one line of explanation.
H1: Is every rule or value in the test cases stated in the story?
H2: Is every numeric limit tested at the limit and just below it?
H3: Is every message copied exactly from the story?
H4: If the story has no measurable value, did the reply ask instead of inventing one?

### Story
<paste the story's acceptance criteria here>

### Reply
<paste the reply here>
```

Replace the two `<paste … here>` lines. Compare its answers with yours. Where you disagree, **the story decides**.

### Step 4 (✍️ Paper): Decide

Using Key Idea 3, write a decision for each reply: accept, fix the instructions, or send questions to the BA.

### Consolidated Result

Your completed review table and decisions. Save it as `review_v1.md` in your `agent` folder; you'll use it in Topic 4.

## Checkpoint

**Answer key (sample replies):**

| Story | 🐍 Script | 👀 Human | Decision |
|---|---|---|---|
| US-205 | **FAIL**: R3 (6 test cases, max 5), R4 (AC4 forgotten) | **H1 ✗**: TC-205-05 invents "lowercase save10 is accepted". H2 ✓ ($50.00 and $49.99), H3 ✓, H4 ✓ | 🔧 Fix the instructions |
| US-311 | **PASS** | **H1 ✗**: "2 seconds" is invented. **H4 ✗**: should be `needs_clarification` | 🔧 Fix the instructions. **The script missed this one** |
| US-312 | **FAIL**: Q1 (TC-312-02 vague) | H2 ✓ (10 and 9 items). **H3 ✗**: AC2's message "Add 10 items for free gift wrap" isn't copied | 🔧 Fix the instructions |

**The big lesson:** US-311 **passed the script** and was still **wrong**. Without the human layer, an invented requirement would have reached the test team.

## Your Turn

1. **(In class, 3 min)** Compare your review table with a neighbour's. Did you both catch TC-205-05?
2. **(After class)** Think of a fifth human check that would be useful for this agent (for example about test steps). Write it as H5 with a one-line question.
3. **(After class)** Could any of H1–H4 be turned into code? Pick one and describe in one sentence how a script might check it, and what it would still miss.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| You marked US-311 as "accept" | The script said PASS | PASS = well-formed, not correct. Always do the human checklist |
| The AI second opinion disagrees with you | The AI can be wrong too | Re-read the story. The story is the only source of truth |

---

<a id="topic-2"></a>

# Topic 2: Building Validation Scripts

## Definition

A **validation script** for the agent runs **all** the checks for **all** the stories in one go and records the results, so you don't have to edit file names and run the checker story by story. Our runner, `run_agent.py`, is ready-made: you don't write it, you **read it and run it**. It reuses your two files from Lecture 09: it calls `build_prompts` to make every prompt, looks for a saved reply for each story, calls `check_reply` on each reply, and writes a **results table**. A story whose reply hasn't been saved yet is marked **WAITING**, with an instruction telling you exactly what to do in your AI tool.

## Key Ideas

1. **The runner does five things, in order:**

   | # | Who | What |
   |---|---|---|
   | 1 | 🐍 Code | Build a prompt for every story (`build_prompts`) |
   | 2 | 🤖 **You** | Paste each prompt into your AI tool and save the reply |
   | 3 | 🐍 Code | Check every saved reply (`check_reply`) |
   | 4 | 🐍 Code | Write the results table to `results_v1.md` |
   | 5 | 🐍 Code | Compare versions, if you give more than one |

2. **WAITING / PASS / FAIL:** every story is in exactly one state, so you always know what's left to do.
3. **Reuse, don't repeat.** The runner contains **no** checking rules of its own; it calls `check_reply`. Fix a rule once, and every run uses the fix.
4. **Results are saved to a file**, so you can compare them later and share them with the team.

## Worked Example: Add and Run `run_agent.py`

### Step 1 (📝 Editor): Create the file

Create `run_agent.py` in your `agent` folder and copy this in exactly. You don't need to understand every line; Step 2 explains the important parts.

```python
import glob
import json
import os
import sys
from build_prompts import build_prompts
from check_reply import check_reply

def run(version):
    build_prompts(version)                                   # 1. code builds every prompt
    os.makedirs(f"replies/{version}", exist_ok=True)
    rows = []
    for path in sorted(glob.glob("stories/*.json")):
        with open(path, encoding="utf-8") as f:
            story = json.load(f)
        sid = story["story_id"]
        reply_path = f"replies/{version}/{sid}.txt"
        if not os.path.exists(reply_path):                   # 2. YOU run the prompt in your AI tool
            rows.append((sid, "WAITING", f"paste prompts/{version}/{sid}.txt into your AI tool, "
                                         f"save the reply as {reply_path}"))
            continue
        with open(reply_path, encoding="utf-8") as f:
            problems = check_reply(story, f.read())          # 3. code checks the reply
        rows.append((sid, "FAIL" if problems else "PASS", "; ".join(problems) or "-"))

    lines = [f"# Results {version}", "", "| Story | Result | Details |", "|---|---|---|"]
    lines += [f"| {sid} | {result} | {details} |" for sid, result, details in rows]
    with open(f"results_{version}.md", "w", encoding="utf-8") as f:   # 4. code records the results
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return rows

if __name__ == "__main__":
    versions = sys.argv[1:] or ["v1"]
    summary = {}
    for version in versions:
        rows = run(version)
        summary[version] = sum(1 for row in rows if row[1] == "PASS")
        print()
    if len(versions) > 1:                                    # 5. code compares versions
        for version, passed in summary.items():
            print(f"{version}: {passed} PASS")
```

### Step 2 (✍️ Paper): Read it and find the five parts

Find the five numbered comments (`# 1.` to `# 5.`) in the code, and match each to the table in Key Idea 1. Notice:

- `from build_prompts import build_prompts` and `from check_reply import check_reply` **reuse** your Lecture 09 files. This is why those files have `if __name__ == "__main__":`: their bottom block **doesn't** run when another file imports them.
- `if not os.path.exists(reply_path):` is where the runner notices that **you** haven't saved a reply yet, and marks the story **WAITING**.
- `sys.argv[1:]` reads the versions you type after the command, for example `python run_agent.py v1 v1.1`.

### Step 3 (💻 Terminal): Run it for v1

```bash
python run_agent.py v1
```

It rebuilds the prompts, checks every saved reply, prints the results table and saves it as `results_v1.md`.

### Step 4 (💻 Terminal): See a WAITING story

Rename `replies/v1/US-312.txt` to `replies/v1/US-312.bak` (in your editor's file panel), and run the command again. Then rename it back and run once more.

### Consolidated File: `run_agent.py`

The file in Step 1 is the consolidated file. Your agent folder now has its three pieces of code:

| File | Written by | Job |
|---|---|---|
| `build_prompts.py` | You (Lecture 09) | Build one prompt per story |
| `check_reply.py` | You (Lecture 09) | Check one reply |
| `run_agent.py` | Provided (Lecture 10) | Run everything, record and compare |

## Checkpoint

**Step 3 output** (with the sample replies):

```text
Saved prompts/v1/US-205.txt
Saved prompts/v1/US-311.txt
Saved prompts/v1/US-312.txt
# Results v1

| Story | Result | Details |
|---|---|---|
| US-205 | FAIL | R3: 6 test cases, maximum is 5; R4: AC4 has no test case and no open question |
| US-311 | PASS | - |
| US-312 | FAIL | Q1: TC-312-02 has a vague expected result |
```

(If you added US-313 in Lecture 09, you'll also see a fourth row.)

**Step 4 output** (US-312's reply renamed): the US-312 row becomes:

```text
| US-312 | WAITING | paste prompts/v1/US-312.txt into your AI tool, save the reply as replies/v1/US-312.txt |
```

The results match what you got story by story in Topic 1, but now for every story in one command, saved in `results_v1.md`.

## Your Turn

1. **(In class, 3 min)** Open `results_v1.md` in your editor (or its Markdown preview). Which story would you look at first, and why?
2. **(After class)** Add `"seamlessly"` to `VAGUE_WORDS` in `check_reply.py` (if you didn't in Lecture 09) and rerun `python run_agent.py v1`. Did you have to change `run_agent.py`? Why not?
3. **(After class)** 🤖 Paste `run_agent.py` into your AI tool and ask: *"Explain what this script does, step by step, for a beginner. Which line would change if the script sent prompts to an AI service automatically?"* Does its answer point at step 2?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'build_prompts'` | The terminal isn't in the `agent` folder, or the file has a different name | `cd agent`; check the file names exactly |
| Every story is WAITING | Replies were saved in the wrong folder (for example `replies/` instead of `replies/v1/`) | Move them into `replies/v1/` |
| `check_reply` output (PASS/FAIL for US-205) appears before the table | The `if __name__ == "__main__":` line is missing in `check_reply.py` | Add it back, as in the Lecture 09 consolidated file |

---

<a id="topic-3"></a>

# Topic 3: Executing Agents against QA Requirements

## Definition

**Executing the agent** means running it on **real requirements** from the backlog, end to end: add the story, build its prompt, run it in the AI tool, save the reply, check it with the script and the human checklist, and **act** on the result. Every outcome needs an **action** and an **owner**: an accepted reply goes to a tester, unclear stories go to the business analyst (BA), and failures go back to whoever maintains the agent's instructions. Running the agent is not the end of the job; deciding what happens next is.

## Key Ideas

1. **The run, step by step:**

   ```text
   📝 add story file ─► 💻 run_agent.py (WAITING) ─► 🤖 paste prompt, 📝 save reply
        ─► 💻 run_agent.py (PASS/FAIL) ─► 👀 human checklist ─► decision + owner
   ```

2. **Triage: every result gets an action and an owner:**

   | Result | Action | Owner |
   |---|---|---|
   | Script PASS + human OK | Review and use the test cases | Tester |
   | `needs_clarification` + human OK | Send the open questions | Tester → BA |
   | Script FAIL | Fix the instructions, or rerun | Agent maintainer (you) |
   | Script PASS + human problem | Fix the instructions; add a human-check note | Agent maintainer (you) |

3. **New stories need no new code.** Add a JSON file to `stories/` and run the same command.
4. **Always a new chat per story**, so earlier stories can't influence the answer.

## Worked Example: Run the Agent on a New Story, US-313

### Step 1 (📝 Editor): Add the story

If you didn't create it in Lecture 08, create `stories/US-313.json`:

```json
{
  "story_id": "US-313",
  "title": "Track an order",
  "acceptance_criteria": [
    {"id": "AC1", "text": "Guests can track an order by entering its order number."},
    {"id": "AC2", "text": "An unknown order number shows \"Order not found\"."}
  ],
  "max_cases": 3
}
```

### Step 2 (💻 Terminal): Run the agent

```bash
python run_agent.py v1
```

US-313 shows **WAITING**, and the message says exactly what to do next.

### Step 3 (🤖 AI tool + 📝 Editor): Do the manual step

1. 📝 Open `prompts/v1/US-313.txt`, select everything and copy it.
2. 🤖 Open a **new chat**, paste it and send.
3. 📝 Save the AI's **whole reply** as `replies/v1/US-313.txt`.

> **If your AI tool isn't working,** save this sample reply as `replies/v1/US-313.txt`:
>
> ```text
> {"story_id": "US-313", "status": "ok", "test_cases": [
>  {"id": "TC-313-01", "title": "Guest tracks an order with a valid order number", "ac_ids": ["AC1"], "type": "positive",
>   "steps": ["Open the order tracking page as a guest", "Enter a valid order number", "Click Track"],
>   "expected_result": "The order's tracking details are displayed"},
>  {"id": "TC-313-02", "title": "Unknown order number", "ac_ids": ["AC2"], "type": "negative",
>   "steps": ["Open the order tracking page as a guest", "Enter order number 00000000", "Click Track"],
>   "expected_result": "\"Order not found\" is shown"}
> ], "open_questions": []}
> ```

### Step 4 (💻 Terminal): Run it again

```bash
python run_agent.py v1
```

US-313 now shows PASS or FAIL.

### Step 5 (✍️ Paper): Human checklist and triage

Apply H1–H4 to the US-313 reply, then use Key Idea 2 to decide the action and owner. Add a row for US-313 to your `review_v1.md`.

### Consolidated Result

US-313 is now part of the backlog: a story file, a prompt, a reply, a row in `results_v1.md` and a row in `review_v1.md`.

## Checkpoint

**Step 2:** the new row reads:

```text
| US-313 | WAITING | paste prompts/v1/US-313.txt into your AI tool, save the reply as replies/v1/US-313.txt |
```

**Step 4 (sample reply):**

```text
| US-313 | PASS | - |
```

**Step 5 (sample reply):** H1 ✓ (nothing invented; "a valid order number" isn't a made-up value), H2 ✓ (no numeric limit in this story), H3 ✓ (`"Order not found"` copied exactly), H4 ✓ → **Accept: send to the tester** for review.

## Your Turn

1. **(In class, 3 min)** Compare your AI's US-313 reply with the sample. Did your AI invent anything, such as an order number format or a time limit?
2. **(After class)** Write a story of your own (from Project 2, or invented) with at least one numeric limit. Add it, run the agent, do the manual step, check it and triage it.
3. **(After class)** For your own story, would you trust the test cases without reading them? Explain why the tester still reviews accepted replies.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| US-313 doesn't appear in the results | The story file isn't in `stories/` or doesn't end in `.json` | Check the folder and the file name |
| The AI answered about US-205 instead | You pasted into an old chat | Always use a **new chat** per story |
| `KeyError: 'max_cases'` | The story file has no `max_cases` | Add it, as in Step 1 |

---

<a id="topic-4"></a>

# Topic 4: Agent Testing and Refinement

## Definition

**Agent testing and refinement** is the improvement loop: **measure** how well the current version does, **analyse** the failures (which rules broke, and how often), make **targeted changes** to the instructions, save them as a **new version** with a changelog entry, and **rerun the same stories** to prove the change helped. It's the same test → analyse → fix → retest loop you use for software, applied to the agent's instructions. Comparing versions fairly means changing **only** the instructions: same stories, same checker, same human checklist.

## Key Ideas

1. **Error analysis: read, then count.** Group every problem from the script **and** the human review by rule. The most common ones are what to fix first.
2. **Each fix targets a failure you actually saw.** No guessing; every new rule has a reason.
3. **New version, never an edit.** Copy v1 to v1.1, change it, and record the changes in a **changelog**, so anyone can see what changed and why.
4. **Compare fairly, and keep checking.** Run v1.1 on the same stories, compare the results with v1, and **repeat the human review**, because a script PASS still isn't proof.

## Worked Example: From v1 to v1.1

The checkpoint uses the sample replies. With your own AI's replies, your counts will differ; follow the same steps with **your** results.

### Step 1 (✍️ Paper): Count the failures

Using `results_v1.md` (script) and `review_v1.md` (human), list every problem by rule:

| Rule broken | Stories | Count |
|---|---|---|
| | | |

### Step 2 (✍️ Paper): Decide what to change

For each rule in your list, write one change to the instructions that would prevent it. Keep each change **specific** and **checkable**.

### Step 3 (📝 Editor): Create `instructions_v1.1.md`

Copy `instructions_v1.md` to `instructions_v1.1.md`. **Don't edit v1.** In the copy, make these changes (based on the sample results; adapt them to your own if they differ):

1. Line 2: `Version: v1.1`
2. Replace the G1 rule with:
   ```text
   - [G1] Use only facts stated in the acceptance criteria. Do not invent rules or values
     (for example time limits, or whether codes are case-sensitive).
   ```
3. Replace the F2 rule with:
   ```text
   - [F2] Never return more than the maximum number of test cases. Count them before you reply.
   ```
4. Add a new rule at the end of **Rules**:
   ```text
   - [Q1] Expected results state an exact value or message. Never use vague words
     such as "works", "correctly" or "as expected".
   ```
5. Add two new rules at the end of **When something is unclear**:
   ```text
   - [U2] Every acceptance criterion needs at least one test case OR an open question.
     Before you reply, check each AC id in turn.
   - [U3] If a criterion has no measurable value (for example "fast" or "easy"), do not
     invent one. Set status to "needs_clarification" and ask for the value.
   ```

Then create `CHANGELOG.md`:

```text
# CHANGELOG - TestCaseDesigner instructions

## v1.1
- G1: added examples of things not to invent. Reason: US-205 invented lowercase codes, US-311 invented "2 seconds" (human review).
- F2: "Count them before you reply." Reason: US-205 had 6 test cases, maximum 5 (R3).
- Q1 (new): no vague words in expected results. Reason: US-312 (Q1).
- U2 (new): every AC needs a test case or a question. Reason: US-205 forgot AC4 (R4).
- U3 (new): no measurable value means needs_clarification. Reason: US-311 (human review H4).

## v1
- First version.
```

### Step 4 (💻 Terminal, 🤖 AI tool, 📝 Editor): Run v1.1

```bash
python run_agent.py v1.1
```

Every story shows **WAITING**, because there are no v1.1 replies yet. For **each** story: 📝 open `prompts/v1.1/<story>.txt`, 🤖 paste it into a **new chat**, 📝 save the reply as `replies/v1.1/<story>.txt`.

> **If your AI tool isn't working,** save these sample replies in `replies/v1.1/` (and copy `replies/v1/US-313.txt` to `replies/v1.1/US-313.txt`):
>
> **`US-205.txt`**
> ```text
> {"story_id": "US-205", "status": "ok", "test_cases": [
>  {"id": "TC-205-01", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
>   "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
>  {"id": "TC-205-02", "title": "SAVE10 on a $100.00 subtotal", "ac_ids": ["AC1"], "type": "positive",
>   "steps": ["Add items totalling $100.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $90.00"},
>  {"id": "TC-205-03", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
>   "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"],
>   "expected_result": "Total stays $49.99 and \"Spend $50.00 to use SAVE10\" is shown"},
>  {"id": "TC-205-04", "title": "Unknown code BOGUS", "ac_ids": ["AC3"], "type": "negative",
>   "steps": ["Add items totalling $60.00", "Enter BOGUS", "Click Apply"],
>   "expected_result": "\"Coupon code not recognised\" is shown"}
> ], "open_questions": ["AC4: What happens, and what message is shown, when a second coupon is entered?"]}
> ```
>
> **`US-311.txt`**
> ```text
> {"story_id": "US-311", "status": "needs_clarification", "test_cases": [],
>  "open_questions": ["AC1: What is the maximum time, in seconds, for search results to appear?"]}
> ```
>
> **`US-312.txt`**
> ```text
> {"story_id": "US-312", "status": "ok", "test_cases": [
>  {"id": "TC-312-01", "title": "Order with exactly 10 items", "ac_ids": ["AC1"], "type": "boundary",
>   "steps": ["Add 10 items to the cart", "Go to checkout"], "expected_result": "Free gift wrap is offered"},
>  {"id": "TC-312-02", "title": "Order with 9 items", "ac_ids": ["AC2"], "type": "boundary",
>   "steps": ["Add 9 items to the cart", "Go to checkout"],
>   "expected_result": "\"Add 10 items for free gift wrap\" is shown"}
> ], "open_questions": []}
> ```

### Step 5 (💻 Terminal): Compare v1 and v1.1

```bash
python run_agent.py v1 v1.1
```

The runner prints both results tables and a short comparison at the end.

### Step 6 (✍️ Paper): Human review of v1.1

Repeat the H1–H4 checklist for the v1.1 replies. Pay special attention to **US-311**, the story the script missed in v1.

### Consolidated Result

`instructions_v1.1.md`, `CHANGELOG.md`, the `replies/v1.1` folder, `results_v1.1.md`, and your human review of v1.1. You've completed one full improvement loop.

## Checkpoint

**Step 1 (sample replies):**

| Rule broken | Stories | Count |
|---|---|---|
| H1 (invented) | US-205, US-311 | 2 |
| R3 (too many) | US-205 | 1 |
| R4 (forgotten AC) | US-205 | 1 |
| Q1 (vague) | US-312 | 1 |
| H3 (message not copied) | US-312 | 1 |
| H4 (should have asked) | US-311 | 1 |

**Step 5 output** (end of the output, with US-313 included):

```text
# Results v1.1

| Story | Result | Details |
|---|---|---|
| US-205 | PASS | - |
| US-311 | PASS | - |
| US-312 | PASS | - |
| US-313 | PASS | - |

v1: 2 PASS
v1.1: 4 PASS
```

**Step 6:** US-205 ✓ (no invented test, AC4 is now a question), US-311 ✓ (now `needs_clarification` with a question; nothing invented), US-312 ✓ (message copied exactly), US-313 ✓.

**Read the comparison carefully:** the script says v1 had **2** passes, but your human review showed only **1** of them (US-313) was really acceptable, because US-311 passed with an invented value. With v1.1, all four pass **both** layers. That's a real, measured improvement, and the changelog explains why.

> **Your own AI may still slip** on v1.1 sometimes. That's normal: AI output varies. It's exactly why the agent always checks every reply, and a person always reviews the result.

## Your Turn

1. **(In class, 3 min)** Look at your own v1 → v1.1 comparison. Which change in the changelog had the biggest effect for **your** AI?
2. **(After class)** Run v1.1 a **second** time in new chats (copy the instructions to `instructions_v1.1b.md` with `Version: v1.1b`, so the replies go into a new folder). Are the results the same? Why does one run prove little?
3. **(After class)** Find one problem that v1.1 still has with your AI, or with your own story from Topic 3. Write `instructions_v1.2.md` with one targeted change, add a changelog entry, and compare all three versions: `python run_agent.py v1 v1.1 v1.2`.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `FileNotFoundError: instructions_v1.1.md` | The copy has a different name | It must be exactly `instructions_v1.1.md` |
| v1.1 results look identical to v1 | You saved the old replies into `replies/v1.1/` | Run the **new** prompts from `prompts/v1.1/` in new chats |
| You edited v1 by mistake | Easy to do | Restore it from the Lecture 09 handout; always copy first |

---

## Wrapping Up the Week: What You Built

Your `agent` folder is a complete, working AI agent:

| Part | File(s) |
|---|---|
| Instructions (two versions + changelog) | `instructions_v1.md`, `instructions_v1.1.md`, `CHANGELOG.md` |
| Input template and contract | `input_template.txt`, `contract.md` |
| Examples | `examples.txt` |
| Requirements | `stories/*.json` |
| Code | `build_prompts.py`, `check_reply.py`, `run_agent.py` |
| Evidence | `prompts/`, `replies/`, `results_*.md`, `review_v1.md` |

**The one manual step left** is step 2 in `run_agent.py`: you paste the prompt into the AI tool and save the reply. The next step after this week is to let code do that too, by sending each prompt to an AI service through its **API** (Application Programming Interface) and saving the reply automatically. Everything else you built stays exactly the same.

---

## Lecture Wrap-Up: Quick Check

1. What are the two layers of output validation, and what does each one catch?
2. US-311 passed the checker but was still wrong. Why?
3. What does WAITING mean in the results table, and what do you do about it?
4. Who owns a `needs_clarification` result?
5. Why do we create `instructions_v1.1.md` instead of editing v1?
6. What's the one step of our agent that isn't automated yet, and how would it be automated?

<details>
<summary>Answers</summary>

1. 🐍 The script (JSON, fields, R1–R4, Q1: well-formed, rule-following) and 👀 the human checklist (H1–H4: invented values, boundaries, exact messages, right status).
2. The checker can't tell that "2 seconds" was invented; only a person comparing it with the story can.
3. No reply has been saved for that story yet. Paste its prompt into a new chat and save the reply in the folder shown.
4. The tester, who sends the open questions to the **BA**.
5. So both versions exist and can be compared fairly, and the changelog can say exactly what changed.
6. Sending the prompt to the AI and saving the reply (step 2). It would be automated by calling an AI service's API from the code.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Output validation** | Checking every agent answer before it's used |
| **Human checklist** | Questions H1–H4 that check meaning, which code can't |
| **Validation script / runner** | Code that runs all checks for all stories and records the results |
| **WAITING / PASS / FAIL** | No reply yet / passed the checker / broke at least one rule |
| **Triage** | Deciding the action and owner for each result |
| **Error analysis** | Counting failures by rule to decide what to fix |
| **Changelog** | A record of what changed in each version, and why |
| **API** | A way for code to talk to a service directly, such as sending prompts to an AI |

## Summary

- **Validate in two layers:** the script checks the contract; a person checks the meaning. "PASS" means well-formed, not correct.
- **`run_agent.py`** runs the whole backlog with one command: WAITING tells you what to do in the AI tool, PASS/FAIL tells you what the checker found, and results are saved.
- **Execute and triage:** every result gets an action and an owner (tester, BA or you).
- **Refine with evidence:** count the failures, make targeted changes in a **new version** with a changelog, rerun the same stories and compare. You've built, tested and improved a real AI agent; automating its last manual step is the next stop.
