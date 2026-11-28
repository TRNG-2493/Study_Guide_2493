# Building Validation Scripts

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what a validation script, or runner, does for an agent, and why it saves time and mistakes.
- **Read** `run_agent.py` and find its five parts: build, the manual step, check, record and compare.
- **Run** the agent over every story with one command, and read the WAITING, PASS and FAIL results.
- **Explain** how the runner reuses `build_prompts` and `check_reply`, and why it contains no rules of its own.
- **Identify** the one line that would change if the agent sent prompts to an AI service automatically.

---

## Why This Matters

In *Agent Output Validation*, getting the script verdicts for three stories meant editing two file names in `check_reply.py`, running it, writing down the result, and repeating. For three stories that is tolerable. For thirty stories, or for the same stories under two versions of the instructions, it is slow, boring and easy to get wrong: one forgotten file name and you have checked US-205's reply against US-312's story.

A **validation script** removes that work. Ours, `run_agent.py`, runs **all** the checks for **all** the stories in one command, and writes the results to a file. It also knows which stories are still waiting for you to do the manual step, and tells you exactly what to do for each one.

You do not write this script. The handout provides it ready-made, and your job is to **read it and run it**. That is a realistic skill: in a real team, much of the automation you use was written by someone else, and you need to understand it well enough to trust it, run it and notice when it is wrong. It also uses your two files from earlier today without changing them, which is the payoff for writing them as reusable functions.

> **Using this with the handout:** this lesson goes deeper into **Handout 10, Topic 2**. It uses the same `run_agent.py`, the same five parts, the same results table, the same WAITING example and the same exercises.

---

## The Concept

### 1. What Is a Validation Script?

A **validation script** for the agent runs **all** the checks for **all** the stories in one go and records the results. Our runner, `run_agent.py`:

1. calls `build_prompts` to make every prompt;
2. looks for a saved reply for each story;
3. calls `check_reply` on each reply it finds;
4. writes a **results table**;
5. and, if you give it more than one version, compares them.

A story whose reply has not been saved yet is marked **WAITING**, with an instruction telling you exactly what to do in your AI tool.

You may also hear this kind of script called a **runner** or a **test harness**: the code that runs the checks and collects the results, as opposed to the checks themselves. pytest, which you have used all week, is a test harness for Python tests. `run_agent.py` is a small one for agent replies.

### 2. The Five Parts

| # | Who | What |
|---|---|---|
| 1 | Code | Build a prompt for every story (`build_prompts`) |
| 2 | **You** | Paste each prompt into your AI tool and save the reply |
| 3 | Code | Check every saved reply (`check_reply`) |
| 4 | Code | Write the results table to `results_v1.md` |
| 5 | Code | Compare versions, if you give more than one |

Four of the five parts are code. Part 2 is you, and the runner handles it in the simplest possible way: it **looks** for the reply file. If it is there, the runner checks it. If not, the runner tells you what to paste and where to save the reply, and moves on to the next story.

### 3. WAITING, PASS and FAIL

The second key idea: every story is in **exactly one** state:

| State | Meaning | Your next action |
|---|---|---|
| **WAITING** | No reply saved yet | Paste the prompt into a new chat; save the reply where the message says |
| **PASS** | The reply passed the checker | Do the human review |
| **FAIL** | The reply broke at least one rule | Read the details; fix the instructions or rerun |

Because the states cover every possibility and never overlap, the results table is also a **to-do list**. Here is how a four-story backlog might look half-way through a session, **illustrative**:

| Story | Result | What it tells you |
|---|---|---|
| US-205 | FAIL | Analyse: read the details, note the rules for the next version |
| US-311 | PASS | Review: human checklist next |
| US-312 | WAITING | Manual step: paste the prompt, save the reply |
| US-313 | WAITING | Manual step |

Two rows need you in the AI tool, one needs a human review, and one needs analysis. You can read the plan for the next half hour straight off the table. Glance at it and you know what is left: WAITING rows need you in the AI tool, PASS rows need your human review, FAIL rows need analysis. Nothing falls through the gaps.

Notice what PASS's "next action" is: **do the human review**. A PASS is not the end, as *Agent Output Validation* showed with US-311.

### 4. Reuse, Don't Repeat

The third key idea: **the runner contains no checking rules of its own.** It calls `check_reply`. That has a powerful consequence: **fix a rule once, and every run uses the fix.**

Imagine the opposite design: a runner with its own copy of the rules. Now there are two places where R4 lives. Someone improves R4 in `check_reply.py`; the runner still uses the old copy; the two give different answers for the same reply; and nobody knows which is right. Software engineers have a name for avoiding this: **DRY**, "don't repeat yourself". Each rule should live in exactly one place.

The same goes for prompt building. The runner calls `build_prompts`, so every run uses exactly the same prompt-building code you tested earlier today.

### 5. Results Are Saved to a File

The fourth key idea: the runner writes `results_v1.md`. A table on the screen disappears when you close the terminal. A file can be compared with tomorrow's results, attached to a report, or shown to a colleague. Later today, `results_v1.md` and `results_v1.1.md` side by side are the evidence that the agent improved.

Saving results also changes how a team works. Instead of "I ran the agent and it looked fine", you can share `results_v1.md` and your human review: anyone can see what passed, what failed and why, and check your conclusions. That is the same habit as attaching evidence to a bug report.

The file is in **Markdown**, the same format as these lessons, so it shows as a neat table in your editor's Markdown preview, and as plain readable text anywhere else.

### 6. Worked Example: Add and Run `run_agent.py`

#### Step 1 (Editor): Create the file

Create `run_agent.py` in your `agent` folder and copy this in exactly:

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

You do not need to understand every line to run it. But reading it carefully is the best way to trust it, so the next step walks through it.

#### Step 2 (Paper): Read it and find the five parts

Find the five numbered comments (`# 1.` to `# 5.`) in the code, and match each to the table in section 2. Then look at these details:

- **`from build_prompts import build_prompts` and `from check_reply import check_reply`** reuse your files from earlier today. This is why those files have `if __name__ == "__main__":`: their bottom block **does not** run when another file imports them. Only the functions are loaded.
- **`if not os.path.exists(reply_path):`** is where the runner notices that **you** have not saved a reply yet, and marks the story WAITING. `continue` then skips to the next story, so a missing reply never stops the whole run.
- **`rows.append((sid, "FAIL" if problems else "PASS", ...))`** records one row per story as a **tuple**: a fixed group of three values (story, result, details). An empty `problems` list counts as false in Python, so no problems means `"PASS"`.
- **`"; ".join(problems) or "-"`** joins all the problems into one line, separated by semicolons. If there are none, the joined text is empty, and `or "-"` puts a dash there instead, so the table never has an empty cell.
- **`lines = [...]` and `lines += [...]`** build the Markdown table line by line: a heading, a blank line, the header row, the separator row, then one row per story.
- **`sys.argv[1:]`** reads the versions you type after the command, for example `python run_agent.py v1 v1.1`. `sys.argv` is the list of words on the command line; item 0 is the script's own name, so `[1:]` is everything after it. If you type no version, `or ["v1"]` uses `v1`.
- **`summary[version] = sum(1 for row in rows if row[1] == "PASS")`** counts the PASS rows for each version, for the comparison at the end.

#### Step 3 (Terminal): Run it for v1

```bash
python run_agent.py v1
```

It rebuilds the prompts, checks every saved reply, prints the results table and saves it as `results_v1.md`. With the sample replies:

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

If you added US-313 earlier today, you will also see a fourth row.

Compare it with the story-by-story results from *Agent Output Validation*. They are identical, as they must be: the runner calls the same `check_reply` with the same stories and replies. The difference is that this took one command instead of three edits and three runs.

#### Step 4 (Terminal): See a WAITING story

Rename `replies/v1/US-312.txt` to `replies/v1/US-312.bak` (in your editor's file panel), and run the command again. The US-312 row becomes:

```text
| US-312 | WAITING | paste prompts/v1/US-312.txt into your AI tool, save the reply as replies/v1/US-312.txt |
```

Then rename it back to `US-312.txt` and run once more. The FAIL row returns.

This small experiment shows that the runner **does not remember anything** between runs. Each run looks at the folders as they are now. Rename a file and the state changes; rename it back and it changes back. That is exactly what you want: the results always describe the files on disk, never an old run.

### 7. Your Agent's Three Pieces of Code

Your agent folder now has all its code:

| File | Written by | Job |
|---|---|---|
| `build_prompts.py` | You (earlier today) | Build one prompt per story |
| `check_reply.py` | You (earlier today) | Check one reply |
| `run_agent.py` | Provided (this lesson) | Run everything, record and compare |

Count the lines: about 25, 45 and 40. Fewer than 120 lines of standard Python, and most of the agent is still in the **text files**: instructions, template, contract, examples and stories.

That balance is deliberate and typical of good agent design. It also means the code is the part least likely to change. Over the rest of today, you will change the instructions and add stories, and none of that will touch these three files. The behaviour lives in text people can read and review; the code only connects the pieces.

### 8. Reuse in Action: Change a Rule Once

The handout's exercise 2 shows the "reuse, don't repeat" idea working. Add `"seamlessly"` to `VAGUE_WORDS` in `check_reply.py`, and rerun:

```bash
python run_agent.py v1
```

You did **not** change `run_agent.py`, and you did not need to. The runner calls `check_reply`, and `check_reply` now knows the new word. Every story is checked with the updated rule, in this run and every future one. (With the sample replies, the results table stays the same, because none of them use "seamlessly". To see the rule fire, add a test reply that does, as in *Implementing IO Contracts*.)

That is the practical value of putting each rule in one place. If you extended the checker with S1 and S2 in *Implementing IO Contracts*, the same applies: the runner uses them automatically. One caution from that lesson still holds: if you change the checker, rerun **every** version you plan to compare, so they are all judged by the same rules.

### 9. When Something Goes Wrong

We tried the common mistakes on purpose, so you know what they look like:

**The `__main__` guard is missing from `check_reply.py`.** We replaced the guard with code that always runs and started the runner. Before the results table, the output began with:

```text
FAIL
 - R3: 6 test cases, maximum is 5
 - R4: AC4 has no test case and no open question
```

That is `check_reply.py`'s **own** test block, running as soon as the runner imported it. The table that follows is still correct, but the extra output is confusing and, in a bigger project, could be slow or harmful. The fix is to put the `if __name__ == "__main__":` line back.

**The version has no instructions file.** `python run_agent.py v2` stops straight away:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'instructions_v2.md'
```

The runner calls `build_prompts("v2")`, which cannot find the file. A version only exists if its instructions file exists.

**No replies saved for a version.** For a new version with an instructions file but no replies, every row is WAITING, each with its own instruction. That is not an error; it is the runner telling you the manual step has not been done yet.

These three cover most first-run problems; the Common Problems table at the end of the lesson lists them with the others.

### 10. The One Line That Would Change

The handout's exercise 3 asks an AI which line would change if the script sent prompts to an AI service automatically. The answer is worth knowing before you ask: it is the **step 2** block, the `if not os.path.exists(reply_path):` part.

Today, that block says "if the reply file is missing, ask the person to make it". An automated version would say instead: "if the reply file is missing, send `prompts/v1/US-205.txt` to the AI service, and save what comes back as `replies/v1/US-205.txt`". Code talks to the service through its **API**: an Application Programming Interface, a way for one program to send requests to another.

Everything else would stay **exactly** the same: the prompts, the replies folder, the checker, the results table, the comparison. That is the reward for building the agent in small, separate steps. Automating the manual step is next week's topic, in Week 9. When you get there, you will change a handful of lines, not rebuild the agent.

One thing would **not** become automatic: the human review. An automated agent produces replies faster, which makes the human layer more important, not less.

### 11. Reading the Results Table

Open `results_v1.md` in your editor, or its Markdown preview. The handout's exercise 1 asks: which story would you look at first, and why?

There is no single right answer, but a good tester's reasoning might go like this:

- **US-311 first.** It **passed**, which is exactly where a hidden problem is most dangerous: nothing will prompt anyone to look at it. And it is a vague story, the kind most likely to tempt the AI into inventing a value.
- **Then US-205.** Two FAILs, and it is about money, so it is high risk.
- **Then US-312.** One FAIL, a vague expected result, likely quick to diagnose.

Notice that this reasoning does **not** start with the FAILs. FAILs announce themselves; they will get looked at. A PASS on a risky story is quieter. That habit, looking hardest where the tools are least likely to raise an alarm, is one of the most valuable a tester can bring to AI-assisted work.

The same reasoning tells you what to do with a table where **everything** passes. An all-PASS table is good news about the shape of the replies, and no news at all about their meaning. It is the moment to be most careful with the human review, not the moment to skip it. Later today, the v1.1 table is all PASS, and the human review is still the step that proves the improvement is real.

### 12. A Small Extension: Counting the States

`run` **returns** its rows as well as printing them, so other scripts can reuse it, exactly as the runner reuses `check_reply`. Here is an optional four-line script, `count_states.py`, that does just that, to print a one-line summary:

```python
from collections import Counter
from run_agent import run

rows = run("v1")
counts = Counter(result for _, result, _ in rows)
print(f"PASS {counts['PASS']}  FAIL {counts['FAIL']}  WAITING {counts['WAITING']}")
```

After the results table, it prints:

```text
PASS 1  FAIL 2  WAITING 0
```

And with US-312's reply renamed, as in Step 4:

```text
PASS 1  FAIL 1  WAITING 1
```

`Counter`, from Python's built-in `collections` module, counts how often each value appears. `for _, result, _ in rows` unpacks each three-part row and keeps only the middle part; `_` is a common name for "a value I do not need".

The point is not the summary itself, but **how** it was added: without changing a single line of `run_agent.py`. Because `run` returns its results, new reports can be built on top of it. That is the same reuse principle again, one level up.

### 13. A Realistic Routine for a Backlog

With the runner, working through a backlog of stories becomes a short, repeatable routine:

1. **Add** any new story files to `stories/`.
2. **Run** `python run_agent.py v1`. New stories appear as WAITING.
3. **Do the manual step** for each WAITING row: open the prompt, new chat, paste, save the whole reply under the name the message gives.
4. **Run again.** Every row is now PASS or FAIL.
5. **Review** every PASS with the human checklist, and look at the FAILs' details.
6. **Decide and record**: accept, send questions to the BA, or note the problem for the next version of the instructions.

Steps 2 and 4 are the same command. You can run it as often as you like: it rebuilds the same prompts (byte-for-byte identical, as *Creating Reusable Prompt Templates* showed), re-checks the same replies, and rewrites the results file. Running it **too often** costs nothing; running it **too rarely** means the results file may describe an old state of the folders.

### 14. What the Runner Does Not Do

Knowing a tool's limits is part of trusting it. Four things `run_agent.py` deliberately does not do:

- **It does not review meaning.** Every PASS still needs the human checklist.
- **It does not call the AI.** The manual step is yours this week.
- **It does not keep history.** Each run **overwrites** `results_v1.md`. If you want to keep an old result, copy the file first, or, better, keep the folder in version control, which you will use in your Project 2 work.
- **It compares counts, not stories.** The comparison at the end says how many stories passed in each version. To see **which** stories changed, read the two tables side by side, which is exactly what *Agent Testing and Refinement* does next.

None of these is a flaw; each keeps the script short enough for a beginner to read in one sitting. But each is a place where **you** fill the gap.

### 15. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'build_prompts'` | The terminal is not in the `agent` folder, or the file has a different name | `cd agent`; check the file names exactly |
| Every story is WAITING | Replies were saved in the wrong folder | Move them into `replies/<version>/` |
| `check_reply` output appears before the table | The `if __name__ == "__main__":` line is missing in `check_reply.py` | Add it back |
| A story is missing from the table | Its file is not in `stories/`, or does not end in `.json` | Check the folder and the file name |
| A results file shows old results | The runner was not rerun after a change | Rerun; the file is rewritten every run |
| Two versions give different results for the same reply | The checker was changed between runs | Rerun both versions with the same checker |

---

## Practice Exercises

1. **First look (editor, 5 min).** Open `results_v1.md` in your editor, or its Markdown preview. Which story would you look at first, and why? Compare your reasoning with section 11.

2. **Change a rule once (code and terminal, 10 min).** Add `"seamlessly"` to `VAGUE_WORDS` in `check_reply.py`, if you did not earlier today, and rerun `python run_agent.py v1`. Did you have to change `run_agent.py`? Why not? Then add a test reply that uses "seamlessly" and confirm the runner reports it.

3. **Explain the runner (AI tool, 10 min).** Follow this week's four steps:
   - **Prompt:** paste `run_agent.py` into your AI tool and ask: *"Explain what this script does, step by step, for a beginner. Which line would change if the script sent prompts to an AI service automatically?"*
   - **Review:** does its answer point at step 2, as in section 10?
   - **Run:** test one claim it makes, for example by renaming a reply file and rerunning.
   - **Record:** in `prompts.txt`, note anything it explained wrongly.

4. **Trace a row (paper, 10 min).** Pick the US-205 row of the results table. Trace it backwards: which line of `run_agent.py` wrote it, which function produced its details, and which lines of `check_reply.py` produced each problem?

5. **Count the states (code, 10 min).** Create `count_states.py` from section 12 and run it. Then add `stories/US-313.json` without a reply, and run it again. What does the summary line say, and which row of the results table explains it?

---

## Knowledge Check

1. What are the five parts of `run_agent.py`, and which one is done by a person?

<details><summary>Answer</summary>

Build the prompts, run each prompt in the AI tool (the person), check every reply, write the results table, and compare versions.

</details>

2. What does WAITING mean, and what do you do about it?

<details><summary>Answer</summary>

No reply has been saved for that story and version yet. Paste the prompt into a new chat and save the reply where the message says.

</details>

3. Why does the runner contain no checking rules of its own?

<details><summary>Answer</summary>

So each rule lives in one place, `check_reply`. Fix a rule once and every run uses the fix; there is no second copy to fall out of step.

</details>

4. Why do `build_prompts.py` and `check_reply.py` need `if __name__ == "__main__":`?

<details><summary>Answer</summary>

So their own test blocks do not run when the runner imports them. Only their functions are loaded.

</details>

5. What does `"; ".join(problems) or "-"` produce for a reply with no problems?

<details><summary>Answer</summary>

A dash, "-". The joined text is empty, so `or` uses the dash instead.

</details>

6. What does `sys.argv[1:]` contain when you run `python run_agent.py v1 v1.1`?

<details><summary>Answer</summary>

The list `["v1", "v1.1"]`: every word after the script's name.

</details>

7. Which part of the runner would change if prompts were sent to an AI service automatically?

<details><summary>Answer</summary>

The step 2 block, where a missing reply file is reported. It would send the prompt through the service's API and save the reply instead. Everything else would stay the same.

</details>

8. Why might a tester look at US-311 before the two FAILs?

<details><summary>Answer</summary>

It passed, so nothing will prompt anyone to look at it, and it is a vague story, where invented values are most likely. FAILs announce themselves; a PASS on a risky story does not.

</details>

9. The runner overwrites `results_v1.md` every time. How do you keep an old result?

<details><summary>Answer</summary>

Copy the file before rerunning, or keep the agent folder in version control so every version of the results is kept.

</details>

---

## Glossary

- **Validation script / runner:** code that runs all checks for all stories and records the results.
- **Test harness:** the code that runs checks and collects results, as opposed to the checks themselves.
- **WAITING / PASS / FAIL:** no reply yet / passed the checker / broke at least one rule.
- **Results table:** the Markdown table written to `results_<version>.md`.
- **Reuse:** calling existing functions instead of copying their code.
- **DRY (don't repeat yourself):** the principle that each piece of logic should live in one place.
- **Tuple:** a fixed group of values, such as (story, result, details).
- **`sys.argv`:** the list of words typed on the command line when running a script.
- **`Counter`:** a Python tool, from the `collections` module, that counts how often each value appears.
- **Overwrite:** replace a file's contents completely, as the runner does with the results file on every run.
- **API (Application Programming Interface):** a way for one program to send requests to another, such as sending prompts to an AI service.

---

## Summary

- **`run_agent.py`** runs the whole backlog with one command: build, (you run the AI), check, record and compare.
- Every story is **WAITING, PASS or FAIL**, so the results table doubles as a to-do list.
- The runner **reuses** `build_prompts` and `check_reply` and has **no rules of its own**: change a rule once, every run uses it.
- Results are **saved to a file**, ready to compare between versions.
- Only the **step 2** block would change to automate the agent through an API, next week. The **human review** stays.

---

## Additional Resources

- Python documentation, *sys.argv*: https://docs.python.org/3/library/sys.html#sys.argv
- Python documentation, *os.path.exists*: https://docs.python.org/3/library/os.path.html#os.path.exists
- Python documentation, *`__main__` — Top-level code environment*: https://docs.python.org/3/library/__main__.html
