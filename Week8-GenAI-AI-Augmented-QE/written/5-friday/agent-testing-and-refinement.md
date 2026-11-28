# Agent Testing and Refinement

## Learning Objectives

By the end of this lesson you will be able to:

- **Analyse** an agent's failures by counting them by rule, from both the checker and the human review.
- **Write** targeted, checkable changes to the instructions, each tied to a failure you actually saw.
- **Create** a new version, `instructions_v1.1.md`, with a changelog entry for every change.
- **Compare** two versions fairly on the same stories, with the same checker and the same human checklist.
- **Explain** why a script count alone overstates success, and why one run proves little.

---

## Why This Matters

You have now built the whole agent and run it on a backlog. The results were mixed: of the four v1 sample replies, the checker passed two, and the human review accepted only **one**. That is a normal first version. The question now is how to make it better **with evidence**, rather than by tweaking rules until the output "looks better".

Testers already know the method, because it is the one used for software: **test, analyse, fix, retest**. Run the current version, find out exactly what failed and how often, make a targeted change, and run the **same** tests again to prove the change helped. The only difference is what gets fixed: not the application's code, but the agent's **instructions**.

The guides from the companies that build these models recommend the same discipline. Anthropic's guide to building agents describes an iterative pattern that works best when there are **clear evaluation criteria** and when iterative refinement provides measurable value ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents)). Our agent has both: the checker and the human checklist are the evaluation criteria, and the results table measures the change.

By the end of this lesson, you will have completed one full improvement loop: v1 to v1.1, with a changelog explaining each change and a comparison showing what it achieved.

> **Using this with the handout:** this lesson goes deeper into **Handout 10, Topic 4**. It uses the same failure counts, the same five changes, the same `instructions_v1.1.md` and `CHANGELOG.md`, the same v1.1 sample replies and the same comparison.

---

## The Concept

### 1. What Is Agent Testing and Refinement?

**Agent testing and refinement** is the improvement loop:

1. **Measure** how well the current version does.
2. **Analyse** the failures: which rules broke, and how often.
3. Make **targeted changes** to the instructions.
4. Save them as a **new version**, with a changelog entry.
5. **Rerun the same stories** to prove the change helped.

It is the same test, analyse, fix, retest loop you use for software. Comparing versions fairly means changing **only** the instructions: same stories, same checker, same human checklist. If anything else changes at the same time, you cannot tell what caused the difference.

### 2. Error Analysis: Read, Then Count

The handout's first key idea: **group every problem from the script and the human review by rule.** The most common ones are what to fix first.

**Error analysis** is the name for this step. It has two halves, and both matter:

- **Read.** Look at each failure and understand it. "R3: 6 test cases" tells you **what**; reading the reply tells you **why** (the AI added a $50.01 case and a lowercase case on top of the four it needed).
- **Count.** Put every problem in a table by rule. Counting stops you fixing the one failure you happen to remember, and shows which problems are common.

Use **both** sources: `results_v1.md` from the checker and `review_v1.md` from the human review. If you count only the script's findings, you will miss the problems that matter most, because the worst ones (invented values) are exactly the ones the script cannot see.

### 3. Every Fix Targets a Failure You Saw

The second key idea: **no guessing; every new rule has a reason.** A change is justified only if it points to a specific failure: this story, this rule, this evidence.

This protects against a common temptation: adding rules for problems that **might** happen. Every rule makes the instructions longer, and longer instructions get partly ignored, as you saw in *Building Agent Instructions*. A rule written for an imagined problem costs attention and fixes nothing. The changelog enforces the discipline: if you cannot write the "Reason:" part of an entry, you should not make the change.

### 4. A New Version, Never an Edit

The third key idea, from *Building Agent Instructions*: **copy v1 to v1.1, change the copy, and record the changes in a changelog**, so anyone can see what changed and why.

A **changelog** is a file listing the changes in each version, newest first. The widely used Keep a Changelog guidelines put the purpose simply: changelogs are for **humans**, not machines, and there should be an entry for every single version ([Keep a Changelog](https://keepachangelog.com/)). Ours follows that spirit: each line names the rule, says what changed, and gives the **reason**, with the story and the check that showed the problem.

### 5. Compare Fairly, and Keep Checking

The fourth key idea: **run v1.1 on the same stories, compare the results with v1, and repeat the human review**, because a script PASS still is not proof.

"Fairly" means exactly one difference between the two runs: the instructions. The stories, the examples, the template, the checker and the checklist all stay the same. That is why *Implementing IO Contracts* warned against changing the checker between runs, and why *Executing Agents against QA Requirements* warned against changing stories during a comparison.

### 6. Worked Example: From v1 to v1.1

The worked example uses the **sample replies**. With your own AI's replies, your counts will differ; follow the same steps with **your** results.

#### Step 1 (Paper): Count the failures

Using `results_v1.md` (script) and `review_v1.md` (human), list every problem by rule. Do it yourself first, then compare:

| Rule broken | Stories | Count |
|---|---|---|
| H1 (invented) | US-205, US-311 | 2 |
| R3 (too many) | US-205 | 1 |
| R4 (forgotten AC) | US-205 | 1 |
| Q1 (vague) | US-312 | 1 |
| H3 (message not copied) | US-312 | 1 |
| H4 (should have asked) | US-311 | 1 |

The most common problem is **H1, invented content**, in two stories. Notice that it comes entirely from the **human** review. A script-only analysis would have counted R3, R4 and Q1, and missed the most frequent and most serious problem completely.

Notice also that US-205 appears in three rows and US-311 in two. One story can break several rules, and one fix may help several rows. That is why the table is organised by **rule**, not by story: rules are what you change.

#### Step 2 (Paper): Decide what to change

For each rule in your list, write one change to the instructions that would prevent it. Keep each change **specific** and **checkable**. The handout's choices, based on the sample results:

| Problem | Change | Why this change |
|---|---|---|
| H1 (invented) | Strengthen **G1** with examples of things not to invent | The rule existed but was too abstract; naming "time limits" and "case-sensitive" points at the actual inventions |
| R3 (too many) | Add "Count them before you reply" to **F2** | The rule existed but was not followed; asking for an explicit count targets the slip |
| Q1 (vague) | Add a new rule **Q1** to the instructions | The contract checked Q1, but the instructions never told the AI about it |
| R4 (forgotten AC) | Add a new rule **U2**: every AC needs a case or a question | U1 covered unclear ACs, not forgotten ones |
| H4 (should have asked) | Add a new rule **U3**: no measurable value means `needs_clarification` | U1 never said what to do when a whole criterion is unmeasurable |

What about **H3**, the uncopied message? There is no separate change for it. The handout's reasoning is that US-312's vague result and its missing message are the same defect seen from two sides, as *Agent Output Validation* showed, so the new Q1 rule targets both. That is a judgement call worth noticing, and worth checking in the v1.1 review: did the message come back?

Two of these changes **strengthen existing rules**, and three **add new ones**. Strengthening is usually the better first move: an existing rule that is not being followed often needs a clearer example, not a companion.

#### Step 3 (Editor): Create `instructions_v1.1.md`

Copy `instructions_v1.md` to `instructions_v1.1.md`. **Do not edit v1.** In the copy, make these changes:

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

Every line has the three parts that make a changelog useful: **which rule**, **what changed**, and **the reason, with its evidence**. A colleague reading it a month from now can understand every change without asking you.

#### See exactly what changed

Use `compare_versions.py` from *Building Agent Instructions* to check your edits:

```bash
python compare_versions.py instructions_v1.md instructions_v1.1.md
```

We ran it on our files. It prints:

```text
--- instructions_v1.md
+++ instructions_v1.1.md
@@ -2 +2 @@
-Version: v1
+Version: v1.1
@@ -13 +13,2 @@
-- [G1] Use only facts stated in the acceptance criteria. Do not invent rules or values.
+- [G1] Use only facts stated in the acceptance criteria. Do not invent rules or values
+  (for example time limits, or whether codes are case-sensitive).
@@ -17 +18,3 @@
-- [F2] Never return more than the maximum number of test cases.
+- [F2] Never return more than the maximum number of test cases. Count them before you reply.
+- [Q1] Expected results state an exact value or message. Never use vague words
+  such as "works", "correctly" or "as expected".
@@ -29,0 +33,4 @@
+- [U2] Every acceptance criterion needs at least one test case OR an open question.
+  Before you reply, check each AC id in turn.
+- [U3] If a criterion has no measurable value (for example "fast" or "easy"), do not
+  invent one. Set status to "needs_clarification" and ask for the value.
```

Compare the diff with the changelog, line by line. Every change in the diff should have a changelog entry, and every entry should appear in the diff. If they disagree, either an edit was made by accident, or the changelog is incomplete. Both are worth fixing before you run anything.

#### Step 4 (Terminal, AI tool and Editor): Run v1.1

```bash
python run_agent.py v1.1
```

Every story shows **WAITING**, because there are no v1.1 replies yet. For **each** story: open `prompts/v1.1/<story>.txt`, paste it into a **new chat**, and save the reply as `replies/v1.1/<story>.txt`.

If your AI tool is not working, save the handout's v1.1 sample replies in `replies/v1.1/`, and copy `replies/v1/US-313.txt` to `replies/v1.1/US-313.txt`. In the US-205 sample, AC4 is now an open question; US-311 is now `needs_clarification`; and US-312's TC-312-02 now expects `"Add 10 items for free gift wrap"` to be shown.

One honest note about US-313: copying its v1 reply into the v1.1 folder means US-313 is not really **retested** with the new instructions; it is carried over. That is fine for the sample, because US-313 was already good. With your own AI, rerun it with the v1.1 prompt like the others.

#### Step 5 (Terminal): Compare v1 and v1.1

```bash
python run_agent.py v1 v1.1
```

The runner prints both results tables and a short comparison at the end. The end of the output, with US-313 included:

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

We ran this on Python 3.10 and 3.13 and got exactly this output on both.

#### Step 6 (Paper): Human review of v1.1

Repeat the H1 to H4 checklist for the v1.1 replies. Pay special attention to **US-311**, the story the script missed in v1. With the sample replies:

| Story | Human review |
|---|---|
| US-205 | ✓ No invented test; AC4 is now a question |
| US-311 | ✓ Now `needs_clarification` with a question; nothing invented |
| US-312 | ✓ Message copied exactly |
| US-313 | ✓ |

The H3 judgement from Step 2 held: the Q1 rule brought the AC2 message back.

### 7. Reading the Comparison Carefully

The runner says v1 had **2** passes and v1.1 has **4**. Read that carefully, because it is not quite the improvement it seems:

| | v1 | v1.1 |
|---|---|---|
| Script PASS | 2 (US-311, US-313) | 4 |
| Accepted after human review | **1** (US-313) | **4** |

The script's v1 count includes US-311, which passed with an invented value. The real v1 score was **1 out of 4**, not 2. So the true improvement is from 1 to 4, larger than the script suggests, and, more importantly, **measured on both layers**.

This is the general danger of script counts: they measure **well-formed**, not **correct**. A version that invents values neatly can score higher than a version that refuses honestly. If you judged versions by script count alone, you could "improve" the agent into one that invents more confidently. The human review is what keeps the comparison honest.

### 8. One Change at a Time, or Five?

The handout makes five changes in one version. That is efficient, and here it is reasonable, because each change targets a **different** failure. But it has a cost worth understanding: when v1.1 improves, you cannot tell **which** change did the work.

Did "Count them before you reply" fix R3, or did U2's "check each AC id in turn" make the AI more careful generally? Did U3 fix US-311, or did the stronger G1? With five changes at once, the comparison shows that the **bundle** helped, not which part.

The alternative is **one change per version**: v1.1 changes only G1, v1.2 only F2, and so on, each compared with the one before. It is slower, and it tells you exactly which change mattered. A useful rule of thumb:

- **Bundle** changes when each targets a separate, clearly understood failure, and you mainly need the agent to work.
- **Separate** them when a change might have side effects, when two changes target the same failure, or when you need to know which one helped, for example before removing a rule.

Either way, the changelog records every change, so you can always go back and test one on its own.

### 9. One Run Proves Little

The handout's exercise 2 asks you to run v1.1 a **second** time, in new chats, as `instructions_v1.1b.md` with `Version: v1.1b`, so the replies go into a new folder. The point is variation. AI output varies between runs, as you have seen all week. One good run might be luck; one bad run might be bad luck.

| What you see | What it suggests |
|---|---|
| Both runs pass on both layers | The change is probably working |
| One run passes, the other fails the same rule | The rule helps, but not reliably; strengthen it or add an example |
| Both runs fail the same rule | The change did not work; try a different approach |
| Different rules fail in each run | Normal variation; look for any rule that fails repeatedly |

The handout's note applies to your own AI: it **may still slip** on v1.1 sometimes. That is normal, because AI output varies. It is exactly why the agent always checks every reply, and a person always reviews the result. Refinement makes failures **rarer**; checks make sure the remaining ones are **caught**.

### 10. Regression: Did Anything Get Worse?

A **regression** is something that used to work and now does not. When you change instructions, check for regressions as carefully as for improvements:

- **Did a story that passed in v1 still pass in v1.1?** In the sample, US-313 passed in both. (With the copied reply that was guaranteed; with your own AI, it is a real check.)
- **Did a new rule cause a new problem?** For example, U3 might push a **clear** story towards `needs_clarification`. Check that US-205, US-312 and US-313 still have test cases.
- **Do the examples still obey the new rules?** Example 1 in `examples.txt` must not contain vague words now that Q1 is an instruction. It does not: "Delivery cost shows $0.00" and "Delivery cost is not $0.00" are exact.

The last point is easy to forget. *Sample Input/Output Pairs* warned that the AI copies examples closely. A new rule that an existing example breaks sends the AI contradictory signals, and the example often wins.

### 11. The Cost of Refinement

Every change makes the instructions longer. In our files, `instructions_v1.md` is about 209 words and `instructions_v1.1.md` about 295. The full US-205 prompt grew from about 400 words to about 486. That is still small, and the improvement was worth it.

But the trend matters. A team that adds five rules per version would have instructions of over a thousand words within a few versions, and *Building Agent Instructions* explained why long instructions get partly ignored. Good refinement sometimes **removes** or **merges** rules: if U2 reliably prevents forgotten ACs, perhaps part of U1 is no longer needed. Removing a rule is a change too, so it gets its own changelog entry, with evidence, and its own comparison.

### 12. A Next Change, Worked: v1.2

The loop does not stop at v1.1. *Executing Agents against QA Requirements* found a new problem with US-314, a story the v1 instructions had never seen: the reply **assumed** that "within 30 days" includes day 30. Here is how that finding becomes a v1.2 change, **illustrative**, following the same steps.

**Count.** One story, one problem: H1 (an assumption stated as fact) and arguably H4 (it should have asked). It is a single occurrence, so before changing anything, check whether other stories with "within", "after" or "before" show the same pattern.

**Decide.** The problem is about **boundary wording**, so it belongs with B1. A targeted, checkable change:

```text
- [B2] If a limit uses words such as "within", "after" or "before", and the story does not
  say whether the limit itself is included, add an open question about it.
```

**Version.** Copy v1.1 to `instructions_v1.2.md`, change line 2 to `Version: v1.2`, add B2, and write the changelog entry:

```text
## v1.2
- B2 (new): ask whether a limit is included when the wording is unclear.
  Reason: US-314 assumed day 30 is inside "within 30 days" (human review H1).
```

**Compare.** Run `python run_agent.py v1.1 v1.2` on **all** the stories, not just US-314. B2 should add a question for US-314. It should **not** add questions for US-205 ("$50.00 or more" is clear) or US-312 ("10 or more items" is clear). If it does, that is a regression: the rule is over-applying, and its wording needs to be narrower.

Notice that this is a **single** change, as section 8 recommends when you need to know whether a change works. And notice that its reason comes from a story added only today. Refinement never really finishes: each new kind of story can teach the agent something, as long as someone is reviewing the replies and recording what they find.

### 13. Wrapping Up the Week: What You Built

Your `agent` folder is a complete, working AI agent:

| Part | File(s) |
|---|---|
| Instructions (two versions plus changelog) | `instructions_v1.md`, `instructions_v1.1.md`, `CHANGELOG.md` |
| Input template and contract | `input_template.txt`, `contract.md` |
| Examples | `examples.txt` |
| Requirements | `stories/*.json` |
| Code | `build_prompts.py`, `check_reply.py`, `run_agent.py` |
| Evidence | `prompts/`, `replies/`, `results_*.md`, `review_v1.md` |

Look at the last row. A large part of what you built is **evidence**: what the agent was given, what it said, what the checks found and what you decided. That is what makes the agent trustworthy, not the AI model behind it. Anyone can open the folder and check every claim.

**The one manual step left** is step 2 in `run_agent.py`: you paste the prompt into the AI tool and save the reply. The next step after this week is to let code do that too, by sending each prompt to an AI service through its **API** and saving the reply automatically. That is where Week 9 picks up. Everything else you built stays exactly the same, including the checks and the human review.

### 14. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `FileNotFoundError: instructions_v1.1.md` | The copy has a different name | It must be exactly `instructions_v1.1.md` |
| v1.1 results look identical to v1 | You saved the old replies into `replies/v1.1/` | Run the **new** prompts from `prompts/v1.1/` in new chats |
| You edited v1 by mistake | Easy to do | Restore it from the handout; always copy first |
| The diff shows a change with no changelog entry | An accidental edit, or an incomplete changelog | Fix one or the other before running |
| v1.1 passes the script but a clear story now asks questions | A new rule, such as U3, over-applies | Note it as a regression; adjust the rule in the next version |

---

## Practice Exercises

1. **Your biggest change (paper, 5 min).** Look at your own v1 to v1.1 comparison. Which change in the changelog had the biggest effect for **your** AI? How do you know, given that five changes were made at once?

2. **Run it again (AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** copy the instructions to `instructions_v1.1b.md` with `Version: v1.1b`, and run `python run_agent.py v1.1b`; do the manual step for every story in new chats.
   - **Review:** apply the human checklist to the v1.1b replies.
   - **Run:** compare with `python run_agent.py v1.1 v1.1b`.
   - **Record:** are the results the same? Use the table in section 9 to explain why one run proves little.

3. **One more version (editor and AI tool, 30 min).** Find one problem that v1.1 still has with your AI, or with your own story from *Executing Agents against QA Requirements*. Write `instructions_v1.2.md` with **one** targeted change, add a changelog entry with its reason, check it with `compare_versions.py`, and compare all three versions: `python run_agent.py v1 v1.1 v1.2`.

4. **Check for regressions (paper, 10 min).** For your v1.1 replies, answer the three questions in section 10. Did anything that worked in v1 get worse?

---

## Knowledge Check

1. What are the five steps of the improvement loop?

<details><summary>Answer</summary>

Measure the current version, analyse the failures by rule, make targeted changes, save them as a new version with a changelog entry, and rerun the same stories to compare.

</details>

2. Why must error analysis use the human review as well as the script results?

<details><summary>Answer</summary>

The most common and serious problem, invented content (H1), comes only from the human review. A script-only count would miss it entirely.

</details>

3. Why does every change need a "Reason:" in the changelog?

<details><summary>Answer</summary>

Every change must target a failure you actually saw. If you cannot write the reason and its evidence, the change is a guess that makes the instructions longer without fixing anything.

</details>

4. What does "compare fairly" mean for v1 and v1.1?

<details><summary>Answer</summary>

Only the instructions differ. The stories, examples, template, checker and human checklist all stay the same.

</details>

5. The runner reports "v1: 2 PASS". Why was the real v1 score 1?

<details><summary>Answer</summary>

US-311 passed the script with an invented value. After human review, only US-313 was acceptable.

</details>

6. The handout made five changes in one version. What is the drawback?

<details><summary>Answer</summary>

When results improve, you cannot tell which change did the work. One change per version is slower but shows exactly which change mattered.

</details>

7. Why does one run of v1.1 prove little?

<details><summary>Answer</summary>

AI output varies between runs. One good result might be luck; you need repeated runs to see whether a rule works reliably.

</details>

8. What is a regression, and give one example to check for after v1.1.

<details><summary>Answer</summary>

Something that used to work and now does not. For example, U3 pushing a clear story such as US-312 towards `needs_clarification`, or an example that breaks the new Q1 rule.

</details>

---

## Glossary

- **Agent testing and refinement:** the loop of measuring, analysing, changing, versioning and retesting an agent.
- **Error analysis:** reading and counting failures by rule to decide what to fix.
- **Targeted change:** a change to the instructions that addresses one failure you actually saw.
- **Changelog:** a record of what changed in each version, and why.
- **Fair comparison:** comparing versions with only the instructions changed.
- **Bundled changes:** several changes made in one version.
- **Variation (run-to-run):** differences in AI output between runs of the same prompt.
- **Regression:** something that used to work and no longer does.
- **Over-applying rule:** a rule that triggers in situations it was not meant for, such as asking questions about a clear limit.
- **API (Application Programming Interface):** a way for code to send requests to a service, such as prompts to an AI.

---

## Summary

- **Refine with evidence:** count failures by rule from **both** layers, make **targeted** changes, save a **new version** with a changelog, and rerun the **same** stories.
- The script said v1 had **2** passes; the human review showed only **1**. With v1.1, all four passed **both** layers: a real, measured improvement.
- **Bundling** changes is efficient but hides which one helped; **one run** proves little; always check for **regressions**.
- Every rule costs length. Good refinement sometimes **removes** rules too.
- You have built, tested and improved a real AI agent. Automating its last manual step, through an **API**, is next week.

---

## Additional Resources

- Keep a Changelog: https://keepachangelog.com/
- Anthropic, *Building effective agents* (evaluation and iterative refinement): https://www.anthropic.com/engineering/building-effective-agents
- Semantic Versioning 2.0.0: https://semver.org/
