# Building Agent Instructions

## Learning Objectives

By the end of this lesson you will be able to:

- **Turn** draft instructions into an official, versioned file, `instructions_v1.md`.
- **Give** every rule a short ID, and explain why IDs make rules easier to discuss and check.
- **Build** a rule map that links each instruction rule to the check that tests it, by code or by a person.
- **Explain** why a version, once run, is never edited, and how that makes fair comparisons possible.
- **Use** an AI review of the instructions as input, while keeping the decisions yourself.

---

## Why This Matters

On Thursday you wrote `instructions_draft.md` and tested it on a few stories. A draft is for trying ideas. Today the agent goes into use: code will build prompts from the instructions, you will run them, and a checker will judge the replies. From now on, every reply needs to be traceable to **exactly** the instructions that produced it.

Think about what happens without that. On Monday you run the agent and three stories fail. On Tuesday someone tweaks a rule. On Wednesday the results look better. Was it the tweak? Or did the AI simply answer differently this time? If the instructions changed silently, nobody can say. Testers know this problem from software: a bug report is useless if nobody knows which build it was found in.

So two things change today. Every rule gets a short **ID**, so you can say precisely "this reply breaks B1". And the file gets a **version number**, so you always know which instructions produced which reply.

Software teams have long used version numbers this way. The widely used Semantic Versioning scheme, for example, uses numbers such as MAJOR.MINOR.PATCH, where each part signals what kind of change was made ([Semantic Versioning](https://semver.org/)). Our scheme is simpler, v1 then v1.1, but the purpose is the same: **a version number tells everyone exactly what they are looking at.**

> **Using this with the handout:** this lesson goes deeper into **Handout 09, Topic 1**. It uses the same `instructions_v1.md`, the same rule IDs (G1, B1, M1, F1, F2, U1), the same rule map, the same AI review prompt and the same sample AI review.

---

## The Concept

### 1. What Does "Building" the Instructions Mean?

**Building agent instructions** means turning the draft from Thursday into the **official version** the agent uses. Two things change:

1. Every rule gets a short **ID**, such as `B1` for boundaries.
2. The file gets a **version number**: `v1`.

The words of the rules do not change today. That is deliberate. The draft was tested on Thursday and behaved reasonably; today's job is to make it **official and traceable**, not to redesign it. Improving the rules comes later today, in *Agent Testing and Refinement*, and it will be based on evidence from real runs, not on guesses.

### 2. Rule IDs

Each rule gets an ID made of a letter and a number. The letter says what kind of rule it is:

| Letter | Stands for | Rule | What it protects against |
|---|---|---|---|
| **G** | Grounding: stick to the facts | G1 | Invented rules or values |
| **B** | Boundaries | B1 | Missing tests at the limit and just below it |
| **M** | Messages | M1 | Paraphrased messages |
| **F** | Format | F1, F2 | Wrong ID format; too many test cases |
| **U** | Uncertainty | U1 | Guessing instead of asking |

IDs do three useful jobs:

- **Precise discussion.** "The reply breaks B1" is clearer than "the reply doesn't do the boundary thing properly".
- **Linking to checks.** An ID can appear in the instructions, in the checker's output and in a review note, and everyone knows it is the same rule.
- **Stable references.** When the wording of a rule improves in v1.1, its ID stays the same. "G1 got stronger in v1.1" tells a reader exactly what changed.

The letters also help you notice gaps. If you list the rules by letter and find no **Q** for quality, you might ask: is there a rule about the quality of expected results? On Thursday you wrote **Q1** in the contract as a check, but the draft instructions do not yet tell the AI about it. Keep that thought; the sample AI review below notices it too.

### 3. Every Rule Gets an ID and a Check

The handout's first key idea is a question to ask of every rule: **"How would we ever know it was broken?"**

A rule that nobody checks is a hope, not a rule. It may be followed, or it may not, and nobody will know. So every rule in the instructions should be paired with a **check**: either code that tests it, or a question a person answers when reviewing a reply.

This is the same principle as Thursday's checkable rules, applied one step further. On Thursday you made sure each rule **could** be checked. Today you write down **how** it is checked, and **by whom**.

### 4. The Rule Map

The **rule map** is a table that links each instruction rule to the check that tests it:

| Instruction rule | Checked by |
|---|---|
| G1: no invented rules or values | Human review |
| B1: test each limit and just below it | Human review |
| M1: copy messages exactly | Human review |
| F1: ID format TC-205-01 | Human review (you could add a code check later) |
| F2: at most `max_cases` test cases | `check_reply.py` rule **R3** |
| U1: unclear AC → question starting with its id | `check_reply.py` rule **R4** |
| Output section: four fields | `check_reply.py` required fields |

Read the table from top to bottom and a pattern appears. The rules at the top, about **meaning** (invented values, boundaries, exact messages), are checked by people. The rules at the bottom, about **structure** (counts, coverage, fields), are checked by code. That is the same split you saw on Thursday in *Required Fields and Validation Rules*: code checks shape and comparisons, people check meaning.

Why can a script not check G1? Because to know whether a value was invented, you must know which values the story **contains**, and recognise them even when they are written differently. A script could check whether a number such as "2 seconds" appears in the story text, but it would struggle with "two seconds", or with an invented **rule** rather than a value, such as "codes are case-insensitive". A person reading the story sees both immediately.

F1 is an interesting middle case. A format such as `TC-205-01` is easy for code to check with a pattern, as you saw in *JSON Schema*. The handout leaves it as a human check for now, with a note that you could add a code check later. That is a useful reminder: the rule map is not fixed. Any time a human check turns out to be mechanical, it can move to code, and free the reviewer for the checks only a person can do.

### 5. Versioning the File

The handout's third key idea: **version the file.** The version appears in two places:

- In the **file name**: `instructions_v1.md`.
- At the **top of the file**: `Version: v1`.

Why both? The file name is what code uses: tomorrow's prompt builder opens `instructions_v1.md` by name. The line inside the file travels with the text: if someone copies the instructions into a chat, an email or a report, the version goes with them.

And the most important rule: **you never edit v1 after you have run it. You create v1.1.**

Here is why, with a concrete example. Suppose you run v1 on three stories and save the replies in `replies/v1/`. Later you edit `instructions_v1.md` to add a rule. Now `replies/v1/` contains replies produced by instructions **that no longer exist**. If you compare them with new replies, you are comparing against a version nobody can see or reproduce. The evidence has been quietly destroyed.

With a new file, `instructions_v1.1.md`, both versions exist. You can rerun either one, compare them on the same stories, and say exactly what changed and whether it helped. That is the whole basis of the improvement loop later today.

### 6. Keep It Short

The handout's last key idea: **instructions that are too long get partly ignored. Every line should earn its place.**

AI models do not read long instructions with equal attention to every line. Research you met on Tuesday, *Lost in the Middle*, found that language models use information at the start and end of a long input better than information in the middle. A rule buried in a long middle paragraph is more likely to be missed.

Our v1 instructions are about **210 words**. The full prompt for one story, with the examples and the story added, is about **400 words**. That is short, and it should stay short. Before adding any rule, ask: **which failure, that we actually saw, does this rule prevent?** If you cannot name one, the rule probably does not earn its place.

### 7. Worked Example: Create `instructions_v1.md`

#### Step 1 (Editor): Copy the draft and add the version

Copy `instructions_draft.md` to a new file called **`instructions_v1.md`**. Change the first line and add a version line:

```text
# TestCaseDesigner - Instructions
Version: v1
```

Keep `instructions_draft.md` as it is. It is a record of what you tested on Thursday.

#### Step 2 (Editor): Add rule IDs

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

The square brackets make the IDs easy to find, for people scanning the file and for any tool that searches it. The AI sees them too, which does no harm: an AI that knows a rule is called B1 can mention it, and some AIs will refer to rule IDs when asked to explain a reply.

#### Step 3 (AI tool): Ask for a review of the instructions

Open a **new chat** and paste the following, followed by the whole of `instructions_v1.md`:

```text
You are reviewing instructions for an AI agent that writes test cases.
List any rule below that is vague, contradicts another rule, or could not be checked
by looking at the agent's answer. For each one, suggest a clearer wording.
If every rule is clear and checkable, say so.

### Instructions
```

Notice the last sentence of the prompt: *"If every rule is clear and checkable, say so."* It is a **way out**, from Tuesday. Without it, an AI asked to find problems will almost always find some, whether or not they are real.

#### The consolidated file

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

Check it against the handout's checkpoint:

- ✅ The file is called exactly `instructions_v1.md`, and line 2 says `Version: v1`. The prompt builder in the next lesson looks for this exact name.
- ✅ Six rule IDs: G1, B1, M1, F1, F2, U1.
- ✅ You can say, for each rule, how it is checked (the rule map).

### 8. Reading the AI's Review

Here is the handout's sample AI review:

> *Most rules are clear and checkable. Suggestions: (1) U1 doesn't say what to do when NO criterion can be tested; consider "set status to needs_clarification". (2) Q: "vague expected results" aren't mentioned; consider forbidding words like "works correctly". (3) F2: ask the agent to count its test cases before replying.*

Judge each suggestion the way you would judge any AI output:

| Suggestion | Is it right? | Evidence so far |
|---|---|---|
| (1) U1 does not cover "no criterion can be tested" | **Yes** | Thursday's US-311 reply invented "2 seconds" with status "ok" |
| (2) No rule about vague expected results | **Yes** | Thursday's Reply A had "works correctly"; Q1 exists in the contract but not in the instructions |
| (3) Ask the agent to count its test cases | **Plausible** | No evidence yet; wait for real results |

The first two are supported by things you have already seen. The third is a reasonable idea without evidence yet.

The handout's advice is clear: **you decide.** Write down the suggestions you agree with, in a note for later today, but **do not edit v1**. Two reasons. First, v1 is about to be run, and it must stay exactly as it is so the results can be compared. Second, a suggestion is a hypothesis. *Agent Testing and Refinement*, later today, adds rules based on **real results**, which is stronger evidence than any review.

It is also worth noticing what the AI might do **wrong** in a review like this. AIs asked for criticism tend to nit-pick: suggesting rewording for rules that are already clear, or proposing extra rules that would make the instructions longer without fixing a real problem. Section 6's question applies here too: which failure would this change prevent?

### 9. The Rule Map as a Living Document

The rule map in section 4 will grow. Later today, the human checklist gets IDs of its own (H1 to H4), and v1.1 adds new rules. A fuller map, for reference, links three things: the **instruction** that tells the AI what to do, the **automatic check** that tests the reply, and the **human check** that covers what code cannot:

| Instruction (tells the AI) | Automatic check (tests the reply) | Human check (meaning) |
|---|---|---|
| G1: no invented rules or values | (none) | Is every value in the story? |
| B1: limit and just below | (none) | Are both boundary tests there? |
| M1: copy messages exactly | (none) | Is every message copied exactly? |
| F1: ID format | (none yet) | Do the IDs follow the format? |
| F2: at most `max_cases` | R3 | |
| U1: ask, don't guess | R4 | Should the agent have refused? |
| Output: four fields | Required fields | |

A good agent has **no empty rows**: every instruction is covered by at least one check. If you add a rule to the instructions and cannot fill in either check column, that is a warning: you will have no way of knowing whether the rule works.

### 10. Why Never Edit a Version: A Worked Story

The handout asks students to explain why `instructions_v1.md` should never be edited after it has run. Here is a short story, **illustrative**, of what goes wrong when it is.

Asha runs v1 on Monday. US-205 fails R3: six test cases, maximum five. On Tuesday, without telling anyone, she adds "Count them before you reply" to F2 in `instructions_v1.md`. She reruns US-205, and it passes. On Wednesday, her colleague Ben reads Monday's results, sees the R3 failure, opens `instructions_v1.md` to investigate, and finds the rule already says "Count them before you reply". He concludes the AI ignored the rule, and spends an hour trying to make it obey a rule that, on Monday, did not exist.

Nothing in Asha's change was wrong. The **process** was wrong: the results and the instructions no longer matched. With a new file, `instructions_v1.1.md`, and one line in a changelog, Ben would have seen immediately that Monday's run used v1, and that the fix was already made in v1.1.

That is why the version is part of the file name, the prompt folder and the reply folder. Everything produced by v1 is labelled v1, for good.

### 10. Seeing Exactly What Changed

With two files on disk, `instructions_draft.md` and `instructions_v1.md`, you can see **exactly** what changed between them. A tool that compares two files line by line produces a **diff**. Many editors can show one (in VS Code, select both files in the Explorer, right-click and choose **Compare Selected**). Python can produce one too, with its built-in `difflib` module. This short script, `compare_versions.py`, prints the differences between any two files:

```python
import difflib
import sys

old_name, new_name = sys.argv[1], sys.argv[2]
old = open(old_name, encoding="utf-8").read().splitlines()
new = open(new_name, encoding="utf-8").read().splitlines()
for line in difflib.unified_diff(old, new, old_name, new_name, lineterm="", n=0):
    print(line)
```

Running `python compare_versions.py instructions_draft.md instructions_v1.md` prints:

```text
--- instructions_draft.md
+++ instructions_v1.md
@@ -1 +1,2 @@
-# TestCaseDesigner - Instructions (draft)
+# TestCaseDesigner - Instructions
+Version: v1
@@ -12,5 +13,5 @@
-- Use only facts stated in the acceptance criteria. Do not invent rules or values.
-- For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
-- Copy expected messages exactly, character for character.
-- Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
-- Never return more than the maximum number of test cases.
+- [G1] Use only facts stated in the acceptance criteria. Do not invent rules or values.
+- [B1] For every numeric limit, test the limit and just below it (e.g. $50.00 and $49.99).
+- [M1] Copy expected messages exactly, character for character.
+- [F1] Number test cases TC-<story number>-<two digits>, e.g. TC-205-01.
+- [F2] Never return more than the maximum number of test cases.
@@ -27 +28 @@
-- If a criterion is unclear or incomplete, do not guess. Add a question to
+- [U1] If a criterion is unclear or incomplete, do not guess. Add a question to
```

**How to read it:** lines starting with `-` are in the old file only; lines starting with `+` are in the new file only. The `@@` lines say where in each file the change is. (The rules themselves start with `- `, which is why some lines begin with two dashes: the first is the diff's mark, the second is part of the rule.)

The diff confirms what this lesson promised: the **only** changes are the title, the version line and the rule IDs. The words of every rule are identical. That is what you want to see when you make a version official, and a diff proves it in seconds. Later today you will use the same script to see what changed between v1 and v1.1.

### 11. Adding Rules Later: Numbering

Rule IDs need a little discipline as the instructions grow:

- **Use the next free number in the right letter.** A second format rule after F1 and F2 would be F3.
- **Never reuse a retired ID.** If a rule is removed in a later version, its ID is retired with it. Reusing it would make old review notes ambiguous: "breaks F2" would mean different things in different versions.
- **Keep the ID when the wording improves.** A clearer G1 is still G1. The changelog records how its wording changed.
- **A new kind of rule may need a new letter.** The sample review's suggestion about vague expected results is about **quality**, a kind of rule v1 does not have. The contract already calls that check Q1, so a matching instruction rule would naturally be Q1 too.

That last point matters. When the instruction rule and the check that tests it share an ID, the rule map almost writes itself, and a failure such as "Q1: TC-312-02 has a vague expected result" points straight at the rule the AI broke.

### 12. Who Owns the Instructions?

On a real team, someone is the **agent maintainer**: the person responsible for the instructions, the examples and the checks. Changes to the instructions are treated like changes to code:

- They are made in a **new version**, never in place.
- They are **reviewed** by someone else before the new version is used, just as code is reviewed before it is merged.
- Each change has a **reason** in the changelog, tied to evidence: a failed check, a review finding, a correction log entry.

This week, you are the agent maintainer. Later today, when you create v1.1, imagine a colleague reading your changelog and the diff. Would they understand what changed, and why? If yes, the change is well made.

### 13. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| File saved as `instructions_v1.md.txt` | Some editors add `.txt` | Rename it so it ends exactly in `.md` |
| You edited the draft instead of making a copy | Easy to do | Keep the draft as it is; `instructions_v1.md` is the new official file |
| `Version:` line missing or says the wrong version | Copied from the draft without updating | Line 2 must match the file name |
| A rule has no ID | It was added later and the ID was forgotten | Every rule gets an ID, so it can be mapped to a check |
| You changed v1 after the AI review | The suggestions seemed obviously right | Write them down for later; never edit a version that is about to run |

---

## Practice Exercises

1. **Human-only rules (paper, 5 min).** In the rule map, which rules can only a **human** check? Why can a simple script not check G1? Write one sentence for each.

2. **Review the instructions (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** send the Step 3 review prompt with your `instructions_v1.md`.
   - **Review:** for each suggestion, decide whether it is supported by something you have already seen, as in section 8.
   - **Run:** pick the one suggestion you agree with most and write it as a new rule with an ID, in a note (not in v1).
   - **Record:** in `prompts.txt`, note how many suggestions the AI made and how many you would keep.

3. **Never edit v1 (paper, 5 min).** In your own words, explain why you should never edit `instructions_v1.md` after you have run it. Use the idea of comparing results later.

4. **Move a check to code (paper, 10 min).** F1 is currently a human check. Describe in two sentences how a script could check it, using a pattern like those in *JSON Schema*. What would the pattern be for US-312's test case IDs?

---

## Knowledge Check

1. What two things change when you turn the draft into `instructions_v1.md`?

<details><summary>Answer</summary>

Every rule gets a short ID, and the file gets a version number, both in its name and on line 2.

</details>

2. What do the letters G, B, M, F and U stand for in the rule IDs?

<details><summary>Answer</summary>

Grounding (stick to the facts), boundaries, messages, format and uncertainty.

</details>

3. What question should you ask of every rule, according to the handout?

<details><summary>Answer</summary>

"How would we ever know it was broken?" Every rule needs a check, by code or by a person.

</details>

4. Which rules in the rule map are checked by code, and which by people?

<details><summary>Answer</summary>

Code checks F2 (rule R3), U1 (rule R4) and the four output fields. People check G1, B1, M1 and, for now, F1.

</details>

5. Why does the version appear both in the file name and inside the file?

<details><summary>Answer</summary>

The file name is what code uses to find the instructions. The line inside the file travels with the text when it is copied elsewhere.

</details>

6. Why should you never edit v1 after it has run?

<details><summary>Answer</summary>

The replies saved for v1 would no longer match any existing instructions, so results could not be compared or reproduced. Create v1.1 instead.

</details>

7. The AI review suggests three changes. Why not make them in v1 straight away?

<details><summary>Answer</summary>

v1 must stay unchanged so its results can be compared, and suggestions are hypotheses. Changes are made in a new version, based on evidence from real runs.

</details>

8. Two lines in a diff begin with `-` and `+`. What does each mean?

<details><summary>Answer</summary>

`-` marks a line that is only in the old file; `+` marks a line that is only in the new file.

</details>

---

## Glossary

- **Building agent instructions:** turning the draft into the official, versioned file the agent uses.
- **Rule ID:** a short label for an instruction rule, such as G1 or F2.
- **Grounding:** sticking to the facts given, without inventing anything.
- **Rule map:** a table linking each instruction rule to the check that tests it.
- **Version:** a label, such as v1 or v1.1, that says exactly which instructions were used.
- **Traceability (of results):** being able to say which version of the instructions produced each reply.
- **Hypothesis:** a suggested improvement that has not yet been tested with real results.
- **Diff:** a line-by-line comparison of two versions of a file, showing what was removed and added.
- **Agent maintainer:** the person responsible for an agent's instructions, examples and checks.
- **Retired ID:** a rule ID that is no longer used and must never be given to a new rule.
- **Semantic Versioning:** a widely used scheme of MAJOR.MINOR.PATCH version numbers for software.

---

## Summary

- **v1 is the official instructions**: the same words as the draft, plus rule IDs and a version.
- **Every rule gets an ID and a check.** If a rule cannot be checked, ask how you would ever know it was broken.
- The **rule map** links rules to checks: code for structure (R3, R4, fields), people for meaning (G1, B1, M1).
- **Never edit a version after it has run.** Create a new version, so results stay comparable.
- **Keep instructions short**, and treat an AI's review as hypotheses to test, not changes to make.

---

## Additional Resources

- Semantic Versioning 2.0.0: https://semver.org/
- OpenAI, *A practical guide to building agents* (PDF; section on instructions): https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts* (2023): https://arxiv.org/abs/2307.03172
