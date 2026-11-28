# Week 08 · Lecture 09: Build the Agent

**Topics:**

1. [Building Agent Instructions](#topic-1)
2. [Creating Reusable Prompt Templates](#topic-2)
3. [Implementing IO Contracts](#topic-3)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Open your `week08/agent` folder. From Lectures 07–08 it should contain `instructions_draft.md`, `input_template.txt`, `contract.md`, `examples.txt` and the `stories` folder with **US-205.json**, **US-311.json** and **US-312.json**.
> 2. Check Python works:
>    ```bash
>    python --version
>    ```
>    Nothing to install: today's code uses standard Python only.
> 3. Open a terminal **inside the `agent` folder** (in VS Code: *Terminal → New Terminal*, then `cd` into `agent`). Every command today runs from there.
> 4. Open your AI assistant: **ChatGPT, Copilot Chat or Claude**.

---

## How to Use This Handout

**Every step tells you where to do it:**

| Label | Where | What you do |
|---|---|---|
| 🤖 **AI tool** | ChatGPT, Copilot Chat or Claude | Open a **new chat**, paste exactly what the step says, and read the reply |
| 📝 **Editor** | VS Code (or any editor) | Create or edit a file in your `agent` folder |
| 💻 **Terminal** | Terminal, inside the `agent` folder | Run the command shown |
| ✍️ **Paper** | Pen and paper, or a text file | Work something out yourself |

Today you **build** the agent. You'll write just **two short Python files**:

| File | Its one job | Lines |
|---|---|---|
| `build_prompts.py` | Fill the template for every story and save one ready-to-paste prompt per story | ~25 |
| `check_reply.py` | Check one AI reply against the contract and rules R1–R4, Q1 | ~45 |

Between them is the step **you** do: paste each prompt into your AI tool and save the reply.

> **About AI answers:** your AI's replies will differ from the samples here. That's fine; the checker works on any reply. If your tool isn't working, use the **sample replies** in Topic 2.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Turn draft instructions into a **versioned** file where every rule has an **ID** and a way to be **checked**.
- Use a short script to **fill the prompt template** for every story, and run the prompts in your AI tool.
- Write a **checker** that tests an AI reply against the contract and the rules, and run it on real replies.

---

<a id="topic-1"></a>

# Topic 1: Building Agent Instructions

## Definition

**Building agent instructions** means turning the draft from Lecture 07 into the **official version** the agent uses. Two things change: every rule gets a short **ID** (like `B1` for boundaries), and the file gets a **version number** (`v1`). Rule IDs let you talk about rules precisely ("this reply breaks B1") and link each rule to the **check** that tests it. The version number matters because you'll improve the instructions in Lecture 10, and you'll need to know exactly which version produced which reply.

## Key Ideas

1. **Every rule gets an ID and a check.** If a rule can't be checked, ask: "How would we ever know it was broken?"
2. **The rule map** links instruction rules to checks:

   | Instruction rule | Checked by |
   |---|---|
   | G1: no invented rules or values | 👀 Human review |
   | B1: test each limit and just below it | 👀 Human review |
   | M1: copy messages exactly | 👀 Human review |
   | F1: ID format TC-205-01 | 👀 Human review (you could add a code check later) |
   | F2: at most `max_cases` test cases | 🐍 `check_reply.py` rule **R3** |
   | U1: unclear AC → question starting with its id | 🐍 `check_reply.py` rule **R4** |
   | Output section: four fields | 🐍 `check_reply.py` required fields |

3. **Version the file.** The version is in the **file name** (`instructions_v1.md`) and at the **top of the file** (`Version: v1`). You never edit v1 later; you create v1.1.
4. **Keep it short.** Instructions that are too long get partly ignored. Every line should earn its place.

## Worked Example: Create `instructions_v1.md`

### Step 1 (📝 Editor): Copy the draft and add the version

Copy `instructions_draft.md` to a new file called **`instructions_v1.md`**. Change the first line and add a version line:

```text
# TestCaseDesigner - Instructions
Version: v1
```

### Step 2 (📝 Editor): Add rule IDs

Change the **Rules** section so each rule starts with its ID in square brackets:

```text
## Rules
- [G1] Use only facts stated in the acceptance criteria. Do not invent rules or values.
- [B1] For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
- [M1] Copy expected messages exactly, character for character.
- [F1] Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
- [F2] Never return more than the maximum number of test cases.
```

And the last section:

```text
## When something is unclear
- [U1] If a criterion is unclear or incomplete, do not guess. Add a question to
  open_questions that starts with the criterion id, e.g. "AC4: ...".
```

**ID letters:** G = grounding (stick to the facts), B = boundaries, M = messages, F = format, U = uncertainty.

### Step 3 (🤖 AI tool): Ask for a review of the instructions

Open a **new chat** and paste the following, followed by the whole of `instructions_v1.md`:

```text
You are reviewing instructions for an AI agent that writes test cases.
List any rule below that is vague, contradicts another rule, or could not be checked
by looking at the agent's answer. For each one, suggest a clearer wording.
If every rule is clear and checkable, say so.

### Instructions
```

**What to notice:** the AI may suggest useful improvements, or nit-pick. **You** decide; write down any suggestion you'd like to use in Lecture 10.

### Consolidated File: `instructions_v1.md`

```text
# TestCaseDesigner - Instructions
Version: v1

## Role and goal
You are TestCaseDesigner, a QA agent on an e-commerce test team.
Your job: turn ONE user story into functional test cases that a tester can review.

## Scope
Only functional test cases for the acceptance criteria you are given.
No performance, security or accessibility tests. No automation code.

## Rules
- [G1] Use only facts stated in the acceptance criteria. Do not invent rules or values.
- [B1] For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
- [M1] Copy expected messages exactly, character for character.
- [F1] Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
- [F2] Never return more than the maximum number of test cases.

## Output
Reply with ONE JSON object and nothing else. Keys:
- story_id: copied from the story
- status: "ok", or "needs_clarification" if no criterion can be tested
- test_cases: a list; each has id, title, ac_ids (a list), type
  (positive, negative or boundary), steps (a list), expected_result
- open_questions: a list of strings

## When something is unclear
- [U1] If a criterion is unclear or incomplete, do not guess. Add a question to
  open_questions that starts with the criterion id, e.g. "AC4: ...".
```

## Checkpoint

- ✅ The file is called exactly `instructions_v1.md` and line 2 says `Version: v1`. The code in Topic 2 looks for this exact name.
- ✅ Six rule IDs: G1, B1, M1, F1, F2, U1.
- ✅ You can say, for each rule, how it's checked (the rule map).

**Sample AI review (Step 3):** *Most rules are clear and checkable. Suggestions: (1) U1 doesn't say what to do when NO criterion can be tested; consider "set status to needs_clarification". (2) Q: "vague expected results" aren't mentioned; consider forbidding words like "works correctly". (3) F2: ask the agent to count its test cases before replying.* These are exactly the kinds of improvements you'll make in Lecture 10, based on real results.

## Your Turn

1. **(In class, 3 min)** In the rule map, which rules can only a **human** check? Why can't a simple script check G1?
2. **(After class)** Pick one suggestion from your AI's review that you agree with. Write the new rule (with an ID) in a note for Lecture 10. Don't edit v1.
3. **(After class)** Why should you never edit `instructions_v1.md` after you've run it? (Hint: think about comparing results later.)

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| File saved as `instructions_v1.md.txt` | Some editors add `.txt` | Rename it so it ends exactly in `.md` |
| You edited the draft instead of making a copy | Easy to do | Keep the draft as it is; `instructions_v1.md` is the new official file |

---

<a id="topic-2"></a>

# Topic 2: Creating Reusable Prompt Templates

## Definition

A **reusable prompt template** is used by **code** instead of being filled by hand. In Lecture 07 you filled `input_template.txt` by hand for one story. Now a short script does it for **every** story: it reads the instructions, the examples and the template, fills the template with each story's data, and saves one **ready-to-paste prompt file** per story. This removes copy-paste mistakes (a missed placeholder, the wrong instructions, a forgotten example) and makes sure every story is presented to the AI in **exactly** the same way.

## Key Ideas

1. **One full prompt per story** = instructions + examples + filled template, saved as `prompts/v1/<story id>.txt`.
2. **`string.Template`** (built into Python) fills `$placeholders` with values. If a value is missing, it **stops with an error** instead of sending a broken prompt.
3. **The version is part of the path.** Prompts built from `instructions_v1.md` go into `prompts/v1/`, and later v1.1 prompts go into `prompts/v1.1/`, so they never get mixed up.
4. **The manual step:** you paste each prompt file into your AI tool and save the reply in `replies/v1/<story id>.txt`.

## Worked Example: `build_prompts.py`, Then Run the Prompts

### Step 1 (📝 Editor): Load the three fixed parts

Create `build_prompts.py` in your `agent` folder:

```python
import glob
import json
import os
from string import Template

def build_prompts(version):
    # Step 1: load the three fixed parts of the agent
    with open(f"instructions_{version}.md", encoding="utf-8") as f:
        instructions = f.read()
    with open("examples.txt", encoding="utf-8") as f:
        examples = f.read()
    with open("input_template.txt", encoding="utf-8") as f:
        template = Template(f.read())
```

**What this code does:**

- The four `import` lines load built-in tools: `glob` finds files, `json` reads JSON, `os` creates folders, and `Template` fills placeholders.
- `build_prompts(version)` is a **function**, so we can later call it with `"v1"` or `"v1.1"`.
- `f"instructions_{version}.md"` builds the file name from the version: for `"v1"` it's `instructions_v1.md`.
- `with open(..., encoding="utf-8") as f:` opens a file and closes it automatically. `encoding="utf-8"` avoids problems with special characters on Windows.

### Step 2 (📝 Editor): Fill the template for every story and save

Add **inside** the function (indented):

```python
    # Step 2: fill the template for every story and save one prompt file per story
    os.makedirs(f"prompts/{version}", exist_ok=True)
    for path in sorted(glob.glob("stories/*.json")):
        with open(path, encoding="utf-8") as f:
            story = json.load(f)
        acs = "\n".join(f"{ac['id']}: {ac['text']}" for ac in story["acceptance_criteria"])
        story_text = template.substitute(story_id=story["story_id"], title=story["title"],
                                         max_cases=story["max_cases"], acceptance_criteria=acs)
        prompt = instructions + "\n\n" + examples + "\n\n" + story_text
        out_path = f"prompts/{version}/{story['story_id']}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        print("Saved", out_path)
```

**What this code does:**

- `os.makedirs(..., exist_ok=True)` creates the `prompts/v1` folder if it doesn't exist yet.
- `glob.glob("stories/*.json")` lists every story file; `sorted` keeps the order the same every time.
- `json.load(f)` reads a story file into a Python dictionary, so `story["title"]` gives `"Apply coupon at checkout"`.
- The `acs` line turns the list of criteria into lines like `AC1: SAVE10 gives…`, one per line.
- `template.substitute(...)` replaces each `$placeholder` with its value. The names (`story_id`, `title`, `max_cases`, `acceptance_criteria`) must match the template **exactly**.
- `prompt = instructions + examples + story_text` joins the three parts, with blank lines between them. That's the full agent prompt.
- The last lines save it as `prompts/v1/US-205.txt` (and so on) and print a message.

### Step 3 (📝 Editor, then 💻 Terminal): Run it

Add at the bottom of the file, **not** indented:

```python
if __name__ == "__main__":
    build_prompts("v1")
```

**What this does:** runs the function for version `v1` when you start this file directly. (In Lecture 10 another script will **reuse** `build_prompts`, and this line stops it from running twice.)

Now, in the terminal:

```bash
python build_prompts.py
```

### Step 4 (🤖 AI tool + 📝 Editor): Run each prompt and save the reply

Create a folder `replies`, and inside it a folder `v1`. Then, **for each of the three prompt files**:

1. 📝 Open `prompts/v1/US-205.txt` in your editor, select everything (**Ctrl+A** / **Cmd+A**) and copy it.
2. 🤖 Open a **new chat** in your AI tool, paste it, and send it.
3. 📝 Copy the AI's **whole reply** and save it as `replies/v1/US-205.txt` (same name as the prompt file).

Repeat for `US-311` and `US-312`. **Always use a new chat for each story**, so one story can't influence the next.

> **If your AI tool isn't working,** save the sample replies at the end of this topic instead. They contain typical mistakes, which makes them good for testing your checker.

### Consolidated File: `build_prompts.py`

```python
import glob
import json
import os
from string import Template

def build_prompts(version):
    # Step 1: load the three fixed parts of the agent
    with open(f"instructions_{version}.md", encoding="utf-8") as f:
        instructions = f.read()
    with open("examples.txt", encoding="utf-8") as f:
        examples = f.read()
    with open("input_template.txt", encoding="utf-8") as f:
        template = Template(f.read())

    # Step 2: fill the template for every story and save one prompt file per story
    os.makedirs(f"prompts/{version}", exist_ok=True)
    for path in sorted(glob.glob("stories/*.json")):
        with open(path, encoding="utf-8") as f:
            story = json.load(f)
        acs = "\n".join(f"{ac['id']}: {ac['text']}" for ac in story["acceptance_criteria"])
        story_text = template.substitute(story_id=story["story_id"], title=story["title"],
                                         max_cases=story["max_cases"], acceptance_criteria=acs)
        prompt = instructions + "\n\n" + examples + "\n\n" + story_text
        out_path = f"prompts/{version}/{story['story_id']}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        print("Saved", out_path)

if __name__ == "__main__":
    build_prompts("v1")
```

## Checkpoint

**Terminal output (Step 3):**

```text
Saved prompts/v1/US-205.txt
Saved prompts/v1/US-311.txt
Saved prompts/v1/US-312.txt
```

**The end of `prompts/v1/US-312.txt`** should look like this (the instructions and examples come before it):

```text
### Story
ID: US-312
Title: Free gift wrap
Maximum test cases: 3
Acceptance criteria:
AC1: Orders of 10 or more items get free gift wrap.
AC2: Orders under 10 items show "Add 10 items for free gift wrap".
### End of story

Now write the JSON reply for this story.
```

**After Step 4, your folder has:**

```text
agent/
├── prompts/v1/   US-205.txt  US-311.txt  US-312.txt   ← built by code
└── replies/v1/   US-205.txt  US-311.txt  US-312.txt   ← saved by you
```

**Sample replies** (save these in `replies/v1/` if your AI tool isn't working):

**`replies/v1/US-205.txt`**

````text
Here are the test cases for US-205:
```json
{"story_id": "US-205", "status": "ok", "test_cases": [
 {"id": "TC-205-01", "title": "SAVE10 on a $100.00 subtotal", "ac_ids": ["AC1"], "type": "positive",
  "steps": ["Add items totalling $100.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $90.00"},
 {"id": "TC-205-02", "title": "SAVE10 on exactly $50.00", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.00", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.00"},
 {"id": "TC-205-03", "title": "SAVE10 on $49.99", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add items totalling $49.99", "Enter SAVE10", "Click Apply"],
  "expected_result": "Total stays $49.99 and \"Spend $50.00 to use SAVE10\" is shown"},
 {"id": "TC-205-04", "title": "Unknown code BOGUS", "ac_ids": ["AC3"], "type": "negative",
  "steps": ["Add items totalling $60.00", "Enter BOGUS", "Click Apply"],
  "expected_result": "\"Coupon code not recognised\" is shown"},
 {"id": "TC-205-05", "title": "Lowercase save10 is accepted", "ac_ids": ["AC3"], "type": "positive",
  "steps": ["Add items totalling $60.00", "Enter save10", "Click Apply"], "expected_result": "Total is $54.00"},
 {"id": "TC-205-06", "title": "SAVE10 on $50.01", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add items totalling $50.01", "Enter SAVE10", "Click Apply"], "expected_result": "Total is $45.01"}
], "open_questions": []}
```
````

**`replies/v1/US-311.txt`**

```text
{"story_id": "US-311", "status": "ok", "test_cases": [
 {"id": "TC-311-01", "title": "Search results appear within 2 seconds", "ac_ids": ["AC1"], "type": "positive",
  "steps": ["Open the search page", "Search for \"shoes\""],
  "expected_result": "Results are displayed within 2 seconds"}
], "open_questions": []}
```

**`replies/v1/US-312.txt`**

```text
{"story_id": "US-312", "status": "ok", "test_cases": [
 {"id": "TC-312-01", "title": "Order with exactly 10 items", "ac_ids": ["AC1"], "type": "boundary",
  "steps": ["Add 10 items to the cart", "Go to checkout"], "expected_result": "Free gift wrap is offered"},
 {"id": "TC-312-02", "title": "Order with 9 items", "ac_ids": ["AC2"], "type": "boundary",
  "steps": ["Add 9 items to the cart", "Go to checkout"], "expected_result": "The message works as expected"}
], "open_questions": []}
```

## Your Turn

1. **(In class, 3 min)** Open `prompts/v1/US-205.txt`. Find where the instructions end, where the examples start, and where the story starts. Is there any `$` left?
2. **(After class)** Add your `US-313.json` story from Lecture 08 to the `stories` folder and run `python build_prompts.py` again. How many prompt files are there now? Run the new one in your AI tool and save the reply.
3. **(After class)** In `input_template.txt`, temporarily change `$title` to `$name` and run the script. Read the error (it's a `KeyError: 'name'`). Why is it **good** that the script stops? Change it back.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `FileNotFoundError: instructions_v1.md` | The file has a different name, or the terminal isn't in the `agent` folder | Check the name; run `cd agent` first |
| `KeyError: 'max_cases'` | A story file has no `max_cases` | Add `"max_cases": 3` to that story file |
| `json.decoder.JSONDecodeError` | A typo in a story file (a missing comma or quote) | The error shows the line number; compare with Lecture 08 |
| Only part of the prompt got pasted | The prompt is long | Use **Ctrl+A** / **Cmd+A** in the editor before copying |

---

<a id="topic-3"></a>

# Topic 3: Implementing IO Contracts

## Definition

**Implementing the IO contract** means turning the contract and rules from Lecture 08 into **code that checks every AI reply**. Our checker, `check_reply.py`, does what you did by hand: it finds the JSON in the reply, checks the **required fields**, then checks rules **R1–R4** and **Q1** against the story. It returns a list of problems: an **empty list** means the reply passes. The checker is completely predictable: the same reply always gets the same result, which is exactly what we need to compare versions of the agent fairly in Lecture 10.

## Key Ideas

1. **The checker runs the checks in order**, and stops early when a reply is too broken to continue:

   ```text
   reply text ─► find the JSON ─► required fields ─► rules R1–R4 ─► quality Q1 ─► list of problems
                     │                  │
                 stop if none     stop if any missing
   ```

2. **Defensive parsing** (Lecture 03): AI replies often add "Here you go!" or ```` ```json ```` fences. The checker keeps only the part from the first `{` to the last `}`.
3. **One function, reused everywhere.** `check_reply(story, reply_text)` will also be used by the runner in Lecture 10.
4. **Code checks the contract; people check the meaning.** A reply can pass every rule and still contain an invented value. That's Lecture 10's human review.

## Worked Example: `check_reply.py`

Create `check_reply.py` in your `agent` folder and build it step by step.

### Step 1 (📝 Editor): Find and read the JSON

```python
import json

REQUIRED = ["story_id", "status", "test_cases", "open_questions"]
VAGUE_WORDS = ["works", "correctly", "properly", "as expected", "successfully"]

def check_reply(story, reply_text):
    # Step 1: find the JSON object in the reply and read it
    start, end = reply_text.find("{"), reply_text.rfind("}")
    if start == -1 or end == -1:
        return ["Not JSON: no { ... } found in the reply"]
    try:
        reply = json.loads(reply_text[start:end + 1])
    except json.JSONDecodeError as err:
        return [f"Not valid JSON: {err.msg}"]
```

**What this code does:**

- `REQUIRED` and `VAGUE_WORDS` are lists taken straight from `contract.md`.
- `find("{")` is the position of the **first** `{`, and `rfind("}")` is the position of the **last** `}`. Everything between them is the JSON. Any chat text or fences around it are ignored.
- If there's no `{` or `}`, `find` returns `-1`, so we return one clear problem straight away.
- `json.loads` turns the JSON text into a Python dictionary. If the JSON is broken, `try/except` catches the error and returns it as a problem instead of crashing.

### Step 2 (📝 Editor): Required fields

Add inside the function:

```python
    # Step 2: required fields
    missing = [field for field in REQUIRED if field not in reply]
    if missing:
        return [f"Missing field: {field}" for field in missing]
```

**What this code does:** lists every required field that is **missing**. If any are missing, it stops here, because the rules below need those fields. (An **empty** list such as `"test_cases": []` is **not** missing, so it passes this check, just as the contract says.)

### Step 3 (📝 Editor): Rules R1–R4

Add:

```python
    # Step 3: rules that compare the reply with the story
    problems = []
    if reply["story_id"] != story["story_id"]:
        problems.append("R1: story_id does not match the story")
    story_acs = {ac["id"] for ac in story["acceptance_criteria"]}
    covered = {ac for tc in reply["test_cases"] for ac in tc.get("ac_ids", [])}
    asked = {q.split(":")[0].strip() for q in reply["open_questions"]}
    for ac in sorted(covered - story_acs):
        problems.append(f"R2: {ac} is not in the story (invented)")
    if len(reply["test_cases"]) > story["max_cases"]:
        problems.append(f"R3: {len(reply['test_cases'])} test cases, maximum is {story['max_cases']}")
    for ac in sorted(story_acs - covered - asked):
        problems.append(f"R4: {ac} has no test case and no open question")
```

**What this code does, rule by rule:**

- **R1:** compares the two story IDs.
- Three **sets** (collections without duplicates) make the other rules easy:
  - `story_acs`: the AC ids in the story, e.g. {AC1, AC2, AC3, AC4}
  - `covered`: the AC ids used in the test cases
  - `asked`: the AC ids that open questions start with (`"AC4: What…".split(":")[0]` gives `"AC4"`)
- **R2:** `covered - story_acs` = AC ids in the reply that aren't in the story, i.e. **invented**.
- **R3:** counts the test cases and compares with `max_cases`.
- **R4:** `story_acs - covered - asked` = ACs with **no** test case **and** no question, i.e. **forgotten**.
- `sorted(...)` keeps the order the same every time.

### Step 4 (📝 Editor): Quality rule Q1, and return the result

Add:

```python
    # Step 4: a quality rule - expected results must be exact
    for tc in reply["test_cases"]:
        if any(word in tc.get("expected_result", "").lower() for word in VAGUE_WORDS):
            problems.append(f"Q1: {tc.get('id', '?')} has a vague expected result")
    return problems
```

**What this code does:** for each test case, checks whether the expected result contains any vague word. `.lower()` makes "Works" and "works" the same. `tc.get(..., "")` avoids a crash if a field is missing. Finally, the function returns the list of problems.

### Step 5 (📝 Editor, then 💻 Terminal): Try it on one reply

Add at the bottom, **not** indented:

```python
if __name__ == "__main__":
    with open("stories/US-205.json", encoding="utf-8") as f:
        story = json.load(f)
    with open("replies/v1/US-205.txt", encoding="utf-8") as f:
        reply_text = f.read()
    problems = check_reply(story, reply_text)
    print("PASS" if not problems else "FAIL")
    for problem in problems:
        print(" -", problem)
```

Then run:

```bash
python check_reply.py
```

### Consolidated File: `check_reply.py`

```python
import json

REQUIRED = ["story_id", "status", "test_cases", "open_questions"]
VAGUE_WORDS = ["works", "correctly", "properly", "as expected", "successfully"]

def check_reply(story, reply_text):
    # Step 1: find the JSON object in the reply and read it
    start, end = reply_text.find("{"), reply_text.rfind("}")
    if start == -1 or end == -1:
        return ["Not JSON: no { ... } found in the reply"]
    try:
        reply = json.loads(reply_text[start:end + 1])
    except json.JSONDecodeError as err:
        return [f"Not valid JSON: {err.msg}"]

    # Step 2: required fields
    missing = [field for field in REQUIRED if field not in reply]
    if missing:
        return [f"Missing field: {field}" for field in missing]

    # Step 3: rules that compare the reply with the story
    problems = []
    if reply["story_id"] != story["story_id"]:
        problems.append("R1: story_id does not match the story")
    story_acs = {ac["id"] for ac in story["acceptance_criteria"]}
    covered = {ac for tc in reply["test_cases"] for ac in tc.get("ac_ids", [])}
    asked = {q.split(":")[0].strip() for q in reply["open_questions"]}
    for ac in sorted(covered - story_acs):
        problems.append(f"R2: {ac} is not in the story (invented)")
    if len(reply["test_cases"]) > story["max_cases"]:
        problems.append(f"R3: {len(reply['test_cases'])} test cases, maximum is {story['max_cases']}")
    for ac in sorted(story_acs - covered - asked):
        problems.append(f"R4: {ac} has no test case and no open question")

    # Step 4: a quality rule - expected results must be exact
    for tc in reply["test_cases"]:
        if any(word in tc.get("expected_result", "").lower() for word in VAGUE_WORDS):
            problems.append(f"Q1: {tc.get('id', '?')} has a vague expected result")
    return problems

if __name__ == "__main__":
    with open("stories/US-205.json", encoding="utf-8") as f:
        story = json.load(f)
    with open("replies/v1/US-205.txt", encoding="utf-8") as f:
        reply_text = f.read()
    problems = check_reply(story, reply_text)
    print("PASS" if not problems else "FAIL")
    for problem in problems:
        print(" -", problem)
```

## Checkpoint

**With the sample reply for US-205**, `python check_reply.py` prints:

```text
FAIL
 - R3: 6 test cases, maximum is 5
 - R4: AC4 has no test case and no open question
```

Notice the checker **ignored** the "Here are the test cases" line and the ```` ```json ```` fences: defensive parsing at work.

**With your own AI's reply**, you'll see `PASS` or a different list of problems. Either is fine. **Check one problem by hand** to make sure you agree with the checker.

**For the other stories** (exercise 1), the sample replies give:

| Story | Result |
|---|---|
| US-311 | `PASS` (but look at it: is "2 seconds" in the story? You'll come back to this in Lecture 10) |
| US-312 | `FAIL` · Q1: TC-312-02 has a vague expected result |

## Your Turn

1. **(In class, 3 min)** In the `if __name__ == "__main__":` block, change **both** `US-205` file names to `US-312` and run it again. Then do the same for `US-311`. Write down the results.
2. **(After class)** Paste Reply A from Lecture 08, Topic 3 into a file `replies/v1/test-A.txt`, point the bottom block at it (with `stories/US-312.json`), and run the checker. Does it find the same four problems you found by hand?
3. **(After class)** Add `"seamlessly"` to `VAGUE_WORDS`. Create a reply that uses it and check that Q1 fires.
4. **(After class)** 🤖 Ask your AI: *"Explain this Python function line by line for a beginner"* and paste the `check_reply` function. Is its explanation of the three **sets** correct?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `FileNotFoundError: replies/v1/US-205.txt` | The reply wasn't saved, or was saved with a different name | Save it as exactly `replies/v1/US-205.txt` |
| `Not JSON: no { ... } found in the reply` | You saved only the AI's intro sentence, not the JSON | Copy the AI's **whole** reply |
| `Not valid JSON: ...` | The reply was cut off, or the AI made a JSON mistake | Check the reply ends with `}`. If the AI broke the JSON, that's a real agent failure: note it |
| `IndentationError` | A step was added at the wrong indentation | Steps 2–4 are **inside** the function (4 spaces); Step 5 is **not** indented |

---

## Lecture Wrap-Up: Quick Check

1. Why does every instruction rule get an ID?
2. Name two instruction rules that only a **human** can check.
3. What does `build_prompts.py` produce, and where does it save it?
4. Which step of the agent do **you** still do by hand?
5. A reply has `"test_cases": []`. Does the required-fields check fail? Why?
6. What does `story_acs - covered - asked` find?

<details>
<summary>Answers</summary>

1. So you can talk about rules precisely and link each one to the check that tests it.
2. Any two of: G1 (no invented facts), B1 (boundaries), M1 (exact messages), F1 (ID format, unless you add a code check).
3. One full prompt per story (instructions + examples + filled template), saved in `prompts/v1/`.
4. Paste each prompt into a new chat in the AI tool, and save the reply in `replies/v1/`.
5. No. The field is **present** but **empty**, which the contract allows.
6. ACs that have **no test case and no open question**: forgotten ACs (rule R4).

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Rule ID** | A short label for an instruction rule (G1, B1, F2…) |
| **Rule map** | A table linking each instruction rule to the check that tests it |
| **Version** | A label (v1, v1.1) that says exactly which instructions were used |
| **`string.Template`** | Python's built-in tool for filling `$placeholders` |
| **Function** | A named, reusable block of code, such as `build_prompts(version)` |
| **`if __name__ == "__main__":`** | "Run this part only when this file is started directly" |
| **Defensive parsing** | Keeping only the JSON part of a reply and handling broken JSON safely |
| **Set** | A Python collection without duplicates; `a - b` gives the items in `a` but not in `b` |

## Summary

- **Instructions v1** are versioned, every rule has an ID, and the **rule map** shows how each rule is checked: by code or by a person.
- **`build_prompts.py`** fills the template for every story and saves ready-to-paste prompts. **You** run them in your AI tool and save the replies.
- **`check_reply.py`** checks any reply against the contract: JSON, required fields, R1–R4 and Q1. The same reply always gets the same result.
- Next lecture: run everything together, add human review, and **improve** the agent.
