# Creating Reusable Prompt Templates

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** how a template filled by code differs from one filled by hand, and why it is safer.
- **Write** `build_prompts.py`, which builds one ready-to-paste prompt per story from the instructions, the examples and the template.
- **Explain** what `string.Template.substitute` does, and why stopping with an error is better than sending a broken prompt.
- **Run** each prompt in your AI tool and save the replies in the right place.
- **Fix** the common errors: a missing file, a missing story field and a renamed placeholder.

---

## Why This Matters

On Thursday, in *Prompt Templates*, you filled `input_template.txt` by hand for US-311: copy the file, replace four placeholders, check for leftovers, paste the instructions on top. It took a few minutes, and you saw how easy it was to miss a placeholder or paste the wrong part.

Now imagine doing it for every story in a sprint, then again for every new version of the instructions, then again when a story changes. Each manual fill is a chance for a small mistake: an old copy of the instructions, a missing example, a `$max_cases` left in the text. Worse, each mistake makes the prompts **different from each other**, which is exactly what the template was meant to prevent.

Code removes those chances. A short script, `build_prompts.py`, reads the three fixed parts of the agent (instructions, examples and template), fills the template with each story's data, and saves one ready-to-paste prompt per story. It does it the same way every time: we ran it twice on the same files and got **byte-for-byte identical** prompts. And if something is missing, it **stops with an error** instead of producing a broken prompt.

This is the first of three short programs that turn your text files into a working agent. It uses only standard Python: nothing to install.

> **Using this with the handout:** this lesson goes deeper into **Handout 09, Topic 2**. It uses the same `build_prompts.py`, the same terminal output, the same prompt and reply folders, and the same sample replies.

---

## The Concept

### 1. A Template Filled by Code

A **reusable prompt template** is used by **code** instead of being filled by hand. The idea is the same as on Thursday; only the worker changes:

| | Filled by hand (Thursday) | Filled by code (today) |
|---|---|---|
| Who fills it | You, in an editor | `build_prompts.py` |
| How many stories | One at a time | All of them, in one run |
| Instructions and examples | Pasted on top by you | Added automatically, always the current version |
| A missed placeholder | Easy to miss | The script stops with an error |
| Same input, same output? | Usually | **Always** |

The last row is the important one. Thursday's lessons made the **story** the only thing that changes between prompts. Code makes sure that promise is actually kept.

### 2. One Full Prompt Per Story

The handout's first key idea: **one full prompt per story** = instructions + examples + filled template, saved as `prompts/v1/<story id>.txt`.

That is the full agent prompt from *Prompt Templates*, in the same order: rules first, examples next, the real story last. The script writes it to a file, so the prompt you paste is **exactly** the prompt the script built. You never assemble it yourself.

Saving each prompt as a file has a second benefit: **evidence**. Later today, when you compare v1 with v1.1, the prompt files show exactly what the AI was given in each version. If a reply looks strange, you can open its prompt and check what the AI actually saw.

### 3. `string.Template`

The second key idea: **`string.Template`**, built into Python, fills `$placeholders` with values. You chose the `$` style for placeholders on Thursday partly because it matches this tool.

It has two ways to fill a template, and the difference matters:

| Method | If a placeholder has no value | Result |
|---|---|---|
| `substitute(...)` | Stops with a `KeyError` | No prompt is produced |
| `safe_substitute(...)` | Leaves the placeholder in the text | A prompt **with `$name` still in it** |

We tried both on a template line containing `$name`, with values for `title` and `max_cases` only:

```text
safe_substitute -> 'Title: $name\nMaximum test cases: 3'
substitute      -> KeyError: 'name'
```

`safe_substitute` sounds safer, but for an agent it is the dangerous one. It quietly produces a prompt with `$name` in it, which you would paste into the AI without noticing. The AI would then see a story with no title, and you would never know why its reply was odd.

`substitute` refuses to continue, and the error tells you exactly which placeholder is missing. **A loud failure is better than a quiet wrong answer.** That is the same principle as a test that fails clearly instead of passing for the wrong reason.

### 4. The Version Is Part of the Path

The third key idea: prompts built from `instructions_v1.md` go into `prompts/v1/`, and later v1.1 prompts go into `prompts/v1.1/`. They never get mixed up.

The same applies to replies: `replies/v1/` and, later, `replies/v1.1/`. This is the versioning principle from *Building Agent Instructions*, carried into the folders. Every file produced by a version is labelled with that version, for good.

### 5. The Manual Step

The fourth key idea: **you** paste each prompt file into your AI tool and save the reply in `replies/v1/<story id>.txt`. This is the one step code does not do this week, and it needs the most care, because nothing checks it until the reply is saved. Section 8 gives a routine.

It is also the step that will change first when the agent grows up. Next week, a few lines of code can send each prompt file to an AI service and save its reply automatically. Notice that nothing else would need to change: the prompts would be built the same way, saved in the same folders, and checked by the same checker. Building the agent in separate, simple steps is what makes that future change small.

### 6. Worked Example: `build_prompts.py`

Create `build_prompts.py` in your `agent` folder. Open a terminal **inside the `agent` folder**; every command today runs from there.

#### Step 1 (Editor): Load the three fixed parts

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
- `build_prompts(version)` is a **function**: a named, reusable block of code. Making it a function means it can be called later with `"v1"` or `"v1.1"`, and reused by another script.
- `f"instructions_{version}.md"` builds the file name from the version: for `"v1"` it is `instructions_v1.md`. This is why the exact file name mattered in *Building Agent Instructions*.
- `with open(..., encoding="utf-8") as f:` opens a file and closes it automatically. `encoding="utf-8"` avoids problems with special characters on Windows.

#### Step 2 (Editor): Fill the template for every story and save

Add **inside** the function, indented by four spaces:

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

- `os.makedirs(..., exist_ok=True)` creates the `prompts/v1` folder if it does not exist yet, and does nothing if it does.
- `glob.glob("stories/*.json")` lists every story file. `sorted` keeps the order the same every time, so the output is predictable.
- `json.load(f)` reads a story file into a Python **dictionary**, so `story["title"]` gives `"Apply coupon at checkout"`.
- The `acs` line turns the list of criteria into lines like `AC1: SAVE10 gives...`, one per line, joined with `"\n"` (a new line). That is exactly the "one AC per line, each starting with its id" habit from *Prompt Templates*.
- `template.substitute(...)` replaces each `$placeholder` with its value. The four names, `story_id`, `title`, `max_cases` and `acceptance_criteria`, must match the template **exactly**.
- `prompt = instructions + "\n\n" + examples + "\n\n" + story_text` joins the three parts, with a blank line between them. That is the full agent prompt.
- The last lines save it as `prompts/v1/US-205.txt` (and so on) and print a message.

Notice one detail. The `$` signs in the **story data**, such as `$50.00`, are not a problem. `substitute` only looks for placeholders in the **template's** text, not in the values it puts in. So "Spend $50.00 to use SAVE10" goes into the prompt unchanged.

#### Step 3 (Editor, then Terminal): Run it

Add at the bottom of the file, **not** indented:

```python
if __name__ == "__main__":
    build_prompts("v1")
```

**What this does:** runs the function for version `v1` when you start this file directly. Later today, another script will **import** `build_prompts` to reuse it, and this line stops it running a second time on import. When Python runs a file directly, it sets the special name `__name__` to `"__main__"`; when the file is imported, `__name__` is the module's name instead ([Python docs](https://docs.python.org/3/library/__main__.html)).

Now, in the terminal:

```bash
python build_prompts.py
```

It prints:

```text
Saved prompts/v1/US-205.txt
Saved prompts/v1/US-311.txt
Saved prompts/v1/US-312.txt
```

#### The consolidated file

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

About 25 lines, as the handout promises. Read it once more from top to bottom and notice what is **not** there: no rules, no knowledge of US-205, no special cases. Everything about the agent lives in the text files. The script only puts them together. That is why adding a story, or a new version of the instructions, needs no change to the code.

### 7. Inside a Built Prompt

Open `prompts/v1/US-312.txt`. Its end should look exactly like this:

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

Now find the three parts in `prompts/v1/US-205.txt`. In our run, the instructions start at line 1 (`## Role and goal` is line 4), `### Example 1` starts at line 32, and `### Story` at line 53. Every prompt has the same structure; only the story section differs.

Two numbers are worth knowing. The US-205 prompt is about **400 words**. On Monday you met the rule of thumb that one token is roughly three-quarters of a word, so that is roughly **530 tokens**: small for any current AI tool. And the three v1 prompts differ only in their last dozen or so lines. If you ever see two prompts that differ in their **instructions** or **examples**, something has gone wrong.

A quick check before pasting is still a good habit: search the prompt for `$` followed by letters, as you did on Thursday. With `substitute`, you should never find one, because the script would have stopped first. Finding one would mean the template contains a placeholder that the script does not fill, which is worth knowing.

### 8. Worked Example: Run Each Prompt and Save the Reply

Create a folder `replies`, and inside it a folder `v1`. Then, **for each of the three prompt files**:

1. Open `prompts/v1/US-205.txt` in your editor, select everything (**Ctrl+A** / **Cmd+A**) and copy it.
2. Open a **new chat** in your AI tool, paste it, and send it.
3. Copy the AI's **whole reply** and save it as `replies/v1/US-205.txt`, with the same name as the prompt file.

Repeat for `US-311` and `US-312`. **Always use a new chat for each story**, so one story cannot influence the next.

Three details save trouble later:

- **Copy the whole reply**, including any "Here you go!" text. The checker in the next lesson knows how to find the JSON inside it. Copying only part of it risks cutting the JSON short.
- **Use the exact file name.** The checker and the runner look for `replies/v1/US-205.txt`; `US205.txt` or `us-205.txt` will not be found.
- **Never edit a reply.** If it is wrong, that is a result. Fixing it by hand would hide the agent's real behaviour.

After this step your folder has:

```text
agent/
├── prompts/v1/   US-205.txt  US-311.txt  US-312.txt   ← built by code
└── replies/v1/   US-205.txt  US-311.txt  US-312.txt   ← saved by you
```

### 9. The Sample Replies

If your AI tool is not working, the handout provides sample replies to save instead. They are worth reading even if your tool works, because they contain **typical mistakes**, which makes them good for testing the checker in the next lesson.

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

Before the checker sees them, try spotting the problems yourself, using Thursday's rules and human checklist. Hints: count US-205's test cases; look for AC4; read TC-205-05's title against the story; ask where "2 seconds" came from; and compare TC-312-02's expected result with AC2's message. The next lesson's checker will find some of these. Which ones do you think it will **miss**? Write your predictions down before the next lesson. Comparing them with the checker's output is one of the quickest ways to understand what code can and cannot see.

### 10. When the Script Stops: Common Errors

The script is short, so its errors are easy to read once you know what they mean. We triggered each of these on purpose:

| Error you see | What happened | What to do |
|---|---|---|
| `FileNotFoundError: ... 'instructions_v1.md'` | The file has a different name, or the terminal is not in the `agent` folder | Check the name; run `cd agent` first |
| `KeyError: 'max_cases'` | A story file has no `max_cases` field | Add `"max_cases": 3` to that story file |
| `KeyError: 'name'` | The template contains `$name`, but the script only provides `title` | Make the template and the script use the same placeholder names |
| `json.decoder.JSONDecodeError` | A typo in a story file, such as a missing comma or quote | The error shows the line number; compare with Thursday's files |

The two `KeyError`s look alike but come from opposite sides. `KeyError: 'max_cases'` happens when the script asks a **story** for a field it does not have. `KeyError: 'name'` happens when the **template** asks for a value the script did not provide. On Thursday you were asked to predict what would happen if someone renamed `$title` to `$name` in the template only. This is the answer: the script stops, before any prompt is saved.

Why is it **good** that the script stops? Because the alternative is worse. Without the error, the prompt would reach the AI with a blank or a stray `$name`, the AI would answer anyway, and the mistake would show up later, if at all, as a slightly odd reply. A clear error at the first step costs ten seconds to fix.

### 11. Testing the Prompt Builder

`build_prompts.py` is a tool your agent depends on, so it deserves the same treatment as any code a tester relies on: **test it**. You do not need a test framework. A short script can check that every built prompt has the shape it should. This one, `check_prompts.py`, is optional, but it shows the idea:

```python
import glob
import re

version = "v1"
instructions = open(f"instructions_{version}.md", encoding="utf-8").read()
examples = open("examples.txt", encoding="utf-8").read()

for path in sorted(glob.glob(f"prompts/{version}/*.txt")):
    prompt = open(path, encoding="utf-8").read()
    problems = []
    if not prompt.startswith(instructions):
        problems.append("does not start with the instructions")
    if examples not in prompt:
        problems.append("examples missing")
    if not prompt.rstrip().endswith("Now write the JSON reply for this story."):
        problems.append("does not end with the task line")
    if re.search(r"\$[a-z_]+", prompt):
        problems.append("unfilled placeholder")
    print(path, "OK" if not problems else problems)
```

On our four prompts it printed `OK` for each. Then we tried a realistic mistake: we added a line to `instructions_v1.md` **without** rebuilding the prompts. The first line of output became:

```text
prompts/v1/US-205.txt ['does not start with the instructions']
```

That is exactly the situation from *Building Agent Instructions*, where results no longer match the instructions, caught in a second. (Afterwards we removed the line again: v1 must not change.)

Each check tests one promise the design makes:

| Check | The promise it tests |
|---|---|
| Starts with the instructions | The prompt uses the **current** instructions for this version |
| Contains the examples | No example was lost |
| Ends with the task line | The real story comes **last** |
| No `$` followed by letters | Every placeholder was filled (prices such as `$30.00` do not match) |

This is a small taste of a big idea: **the tools that build and check your agent are code, and code needs tests.** A broken prompt builder would quietly damage every run, and every check after it would be checking the wrong prompts.

### 12. Same Input, Same Prompts

One more property is worth confirming, because the comparisons later today depend on it. We ran `build_prompts.py` twice on the same files and compared the outputs byte by byte: **identical**. The script contains nothing random and nothing that depends on the time or the computer, and `sorted` fixes the order of the stories.

That means a difference between the v1 and v1.1 prompts can only come from a difference between `instructions_v1.md` and `instructions_v1.1.md`. The builder itself adds no noise. When you compare versions later today, any change in the AI's replies comes from the instructions, or from the AI's own variation, never from the way the prompts were put together.

### 13. Adding a Story Needs No Code

The handout's exercise 2 is worth doing, because it shows the design working. Add `stories/US-313.json` from Thursday and run `python build_prompts.py` again. We got:

```text
Saved prompts/v1/US-205.txt
Saved prompts/v1/US-311.txt
Saved prompts/v1/US-312.txt
Saved prompts/v1/US-313.txt
```

Four prompts, with **no change to the code**. The same is true for a new version of the instructions: call `build_prompts("v1.1")` and a new folder of prompts appears. The script is reusable because it knows nothing about any particular story or version. That separation, **data in files, logic in code**, is what lets the agent grow without the code growing.

### 14. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `FileNotFoundError: instructions_v1.md` | The file has a different name, or the terminal is not in the `agent` folder | Check the name; run `cd agent` first |
| `KeyError: 'max_cases'` | A story file has no `max_cases` | Add `"max_cases": 3` to that story file |
| `json.decoder.JSONDecodeError` | A typo in a story file (a missing comma or quote) | The error shows the line number; compare with Thursday's story files |
| Only part of the prompt got pasted | The prompt is long | Use **Ctrl+A** / **Cmd+A** in the editor before copying |
| Prompts still show old instructions | You changed the instructions but did not rerun the script | Rerun `python build_prompts.py` (and never change a version that has already run) |
| `IndentationError` | Step 2 was not indented inside the function | Steps 1 and 2 are indented four spaces; the `if __name__` block is not |

---

## Practice Exercises

1. **Find the parts (editor, 5 min).** Open `prompts/v1/US-205.txt`. Find where the instructions end, where the examples start, and where the story starts. Is there any `$` left that is not part of a price?

2. **Add a story (editor, terminal and AI tool, 15 min).** Add your `US-313.json` story from Thursday to the `stories` folder and run `python build_prompts.py` again. How many prompt files are there now? Run the new one in your AI tool, in a new chat, and save the reply as `replies/v1/US-313.txt`.

3. **Break the template (editor and terminal, 5 min).** In `input_template.txt`, temporarily change `$title` to `$name` and run the script. Read the error. Why is it **good** that the script stops? Change it back and run again.

4. **Safe or loud? (code, 10 min).** In a **copy** of `build_prompts.py`, change `substitute` to `safe_substitute`, keep `$name` in a copy of the template, and run it. Open the prompt. What would the AI see? Write one sentence on why the original script uses `substitute`.

5. **Explain it (AI tool, 10 min).** Ask your AI: *"Explain this Python function line by line for a beginner."* and paste `build_prompts`. Check its explanation of `substitute` and of `if __name__ == "__main__":` against this lesson.

---

## Knowledge Check

1. What three parts does `build_prompts.py` combine into each prompt, and in what order?

<details><summary>Answer</summary>

The instructions, the examples and the filled template, in that order, with the story last.

</details>

2. Where are the v1 prompts saved, and why is the version part of the path?

<details><summary>Answer</summary>

In `prompts/v1/<story id>.txt`. The version in the path keeps prompts from different versions separate, so they can never be mixed up.

</details>

3. What is the difference between `substitute` and `safe_substitute`, and why does the agent use `substitute`?

<details><summary>Answer</summary>

`substitute` stops with a `KeyError` if a placeholder has no value; `safe_substitute` leaves the placeholder in the text. A loud stop is better than a prompt with `$name` still in it.

</details>

4. The template contains "Spend $50.00 to use SAVE10" after filling. Why does `substitute` not treat `$50` as a placeholder?

<details><summary>Answer</summary>

That text is part of a value being inserted, not part of the template. `substitute` only looks for placeholders in the template's own text.

</details>

5. What does `if __name__ == "__main__":` do in `build_prompts.py`?

<details><summary>Answer</summary>

It runs `build_prompts("v1")` only when the file is started directly, not when another script imports the function.

</details>

6. `KeyError: 'max_cases'` and `KeyError: 'name'` look similar. What causes each?

<details><summary>Answer</summary>

`max_cases`: a story file is missing that field. `name`: the template has a placeholder the script does not fill.

</details>

7. Which step does code not do this week, and what three habits make it reliable?

<details><summary>Answer</summary>

Pasting each prompt into the AI tool and saving the reply. Use a new chat per story, copy the whole reply, and save it with the exact file name, without editing it.

</details>

8. Why does adding US-313 need no change to `build_prompts.py`?

<details><summary>Answer</summary>

The script finds every story file in `stories/` and knows nothing about particular stories. Data lives in files; logic lives in code.

</details>

9. What does `check_prompts.py` report if you change `instructions_v1.md` without rebuilding the prompts, and why does that matter?

<details><summary>Answer</summary>

"does not start with the instructions". It means the saved prompts no longer match the instructions, so any replies from them could not be traced to the current file.

</details>

---

## Glossary

- **Reusable prompt template:** a template filled by code for every story.
- **`build_prompts.py`:** the script that builds one full prompt per story.
- **`string.Template`:** Python's built-in tool for filling `$placeholders`.
- **`substitute` / `safe_substitute`:** fill placeholders and stop on a missing one / leave missing ones in the text.
- **Function:** a named, reusable block of code, such as `build_prompts(version)`.
- **Dictionary:** a Python collection of named values, such as a story loaded from JSON.
- **`if __name__ == "__main__":`:** "run this part only when this file is started directly".
- **Import:** loading code from another file so it can be reused.
- **`KeyError`:** Python's error when a requested key or placeholder value is not there.
- **Byte-for-byte identical:** two files with exactly the same content, down to every character.
- **Manual step:** the one step done by a person this week: pasting each prompt and saving the reply.
- **`check_prompts.py`:** an optional script that tests every built prompt has the expected shape.
- **Deterministic (script):** producing exactly the same output from the same input every time.

---

## Summary

- **`build_prompts.py`** fills the template for every story and saves one full prompt per story in `prompts/v1/`.
- It uses **`substitute`**, which **stops** on a missing placeholder. A loud failure is better than a quiet broken prompt.
- The **version is part of the path**, so prompts and replies from different versions never mix.
- **You** paste each prompt into a new chat and save the whole reply, unedited, as `replies/v1/<story id>.txt`.
- **Data in files, logic in code:** new stories and new versions need no code changes.

---

## Additional Resources

- Python documentation, *string — Template strings*: https://docs.python.org/3/library/string.html#template-strings
- Python documentation, *`__main__` — Top-level code environment*: https://docs.python.org/3/library/__main__.html
- Python documentation, *glob — Unix style pathname pattern expansion*: https://docs.python.org/3/library/glob.html
