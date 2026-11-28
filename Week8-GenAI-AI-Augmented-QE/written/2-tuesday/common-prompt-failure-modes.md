# Common Prompt Failure Modes

## Learning Objectives

By the end of this lesson you will be able to:

- **Name** the most common ways AI answers go wrong: hallucination, ignored instructions, wrong maths, outdated knowledge and inconsistency.
- **Explain** the usual cause of each failure mode, using what you know about how LLMs work.
- **Debug** a failing prompt like a failing test: reproduce, change one thing, re-run, compare.
- **Write** small automatic checks that catch the failures that are easy to detect in code.
- **Decide**, using the requirement, whether a mismatch is the AI's mistake or a bug in the code.

---

## Why This Matters

Yesterday and this morning you learned how LLMs work and how to write good prompts. Even good prompts fail sometimes. This lesson is a **catalogue of the ways they fail**, so that you recognise each one quickly and know what to do about it.

For a tester, this is familiar ground. Just as you learned the typical defects in web applications, such as boundary errors, missing validation and timing issues, AI output has its own typical defects. Knowing them turns "the AI was wrong" into a precise report: *which* kind of wrong, *why*, and *how to fix the prompt*.

The failures are not rare edge cases. In *Generative AI Concepts* you saw a study in which code-generating models suggested software packages that do not exist. In *Prompt Engineering Principles* you saw a neat table with one wrong total. This lesson collects these patterns, and shows a short script that catches several of them automatically.

> **Using this with the handout:** this lesson goes deeper into **Handout 04, Topic 1**. It uses the same AI test table, the same `failure_checks.py` with Monday's `cart.py`, and the same prompt-debugging checklist.

---

## The Concept

### 1. Debugging a Prompt Like Debugging a Test

A **prompt failure mode** is a typical way an AI answer goes wrong, even when the prompt looked fine. The tester's response is the same as for any defect:

1. **Notice** the failure, ideally with a check rather than by luck.
2. **Reproduce** it: run the same prompt again, in a new chat. Does it happen every time, or only sometimes?
3. **Find the cause**, using the map in section 2.
4. **Fix the prompt** by changing **one thing**, then re-run and compare.

This is the prompt-refinement loop from *Prompt Engineering Principles*, applied to a specific failure. The one difference from ordinary debugging is randomness: a failure that appears in one run out of three is still a real failure, so reproduce over **several** runs, not one.

### 2. A Quick Map of the Failure Modes

| Failure mode | What you see | Typical cause | Fix |
|---|---|---|---|
| **Hallucination** | An invented rule, function, package or fact | Missing context; the model fills gaps with likely text | Give the context; allow "I don't know" or questions |
| **Ignored instruction** | 4 items instead of 5; extra text; wrong format | Instruction buried, vague or in conflict with another | Be exact ("exactly 5"); put key rules at the end; lock the format |
| **Wrong maths** | 49.99 → 44.99 when it should be unchanged | The model predicts digits as text; it does not calculate | **Check numbers with code** |
| **Outdated knowledge** | Old methods such as Selenium's `find_element_by_id` | Training cut-off; old examples in training data | Name the version; check the official docs |
| **Inconsistency** | A different answer every run | Sampling and temperature | Lock the format; re-run and compare; review a batch |

Behind every row sits the same fact from Monday: **an LLM predicts likely text.** Each failure is that mechanism showing through in a different way.

Notice also that the failure modes **combine**. A single reply can be short by one item (ignored instruction), contain an invented rule (hallucination) and get a boundary wrong (wrong maths), all at once, as the worked example in section 4 shows. So when you find one failure in a reply, keep checking: finding one defect is a reason to look harder, not a reason to stop, exactly as in ordinary testing.

### 3. The Failure Modes in Detail

#### 3.1 Hallucination

**What it is:** confident, fluent content that is false. In QE, the most common forms are:

- **Invented requirements:** "codes are case-insensitive", when the story says nothing.
- **Invented functions or methods:** `pytest.assert_coupon_valid()`, from Monday's hallucination probe.
- **Invented packages:** a `pip install` command for a package that does not exist.
- **Invented facts:** a wrong default timeout, a made-up error code.

**Why it happens:** the request is shaped like many real requests, and the most likely continuation is a plausible answer. Nothing in the generation loop checks that the answer is real.

**How to catch it:** check every requirement-like claim against the story, every function against the official documentation, and every package against its registry. Run the code: invented functions fail fast.

**How to reduce it:** paste the real context, say "use only the stated rules", and give the model a way out, such as "if the story does not say, write NOT SPECIFIED", as in *Specificity and Context*.

#### 3.2 Ignored instructions

**What it is:** the answer breaks a clear instruction: the wrong number of items, text before the JSON, a field renamed, a rule from the start of the prompt forgotten.

**Why it happens:** several reasons combine.

- **Position.** Research has found that models use information at the **beginning** and **end** of a long input best, and that performance drops when the relevant information sits in the **middle** ([Liu et al., *Lost in the Middle*, 2023](https://arxiv.org/abs/2307.03172)). An instruction buried mid-prompt is easier to miss.
- **Vagueness.** "A few tests" or "keep it short" has no exact meaning to obey.
- **Conflict.** "Be thorough" and "at most 3 items" pull in opposite directions; the model may favour one.
- **Strong habits.** Friendly openings such as "Sure! Here are…" are very likely text, as you saw in *Format Locking*.

**How to catch it:** count items, check the format, and check required fields in code.

**How to reduce it:** use exact numbers, lock the format, avoid conflicting instructions, and put the most important rules near the **end** of the prompt, just before the model starts writing.

#### 3.3 Wrong maths

**What it is:** arithmetic errors in expected values: a discount applied to the wrong total, rounding done wrongly, a boundary handled the wrong way.

**Why it happens:** the model writes numbers as tokens, predicting digits rather than calculating them. Simple sums are usually right; boundaries, rounding and multi-step calculations are where slips happen.

**How to catch it:** **never trust an expected value you have not checked.** Recalculate it, by hand or in code, from the requirement.

**How to reduce it:** ask the AI to show its working (which makes slips easier to spot), or, better, let code compute the numbers and use the AI for the test ideas only.

#### 3.4 Outdated knowledge

**What it is:** answers based on how things used to be. A classic example in QE automation: older Selenium tutorials used methods such as `driver.find_element_by_id("x")`. The Selenium project announced that these locator-specific methods would be removed in favour of `driver.find_element(By.ID, "x")` ([Selenium blog, 2022](https://www.selenium.dev/blog/2022/python-locators-se4/)), and they were removed in Selenium 4.3. A model trained on years of older tutorials may still suggest them, and your test fails with an `AttributeError`.

**Why it happens:** the **knowledge cut-off** from *Generative AI Concepts*, plus the fact that older patterns appear in far more training text than newer ones.

**How to catch it:** run the code against the version you actually use, and check the official documentation for anything that looks unfamiliar.

**How to reduce it:** name the version in the prompt ("We use Selenium 4 with Python; use `find_element(By...)`"), and paste a small example of your current code style as context.

#### 3.5 Inconsistency

**What it is:** different answers to the same prompt: different test cases, different severities, different expected values.

**Why it happens:** sampling, from *Generative AI Concepts*. Some variation in wording is harmless. Variation in **facts**, such as a different expected total, means at least one run is wrong.

**How to catch it:** run the prompt several times and compare. Look at a **batch** of answers, not just one: in *Few-Shot Prompting* you saw that a bias across many answers can be invisible in any single one.

**How to reduce it:** lock the format, give examples, lower the temperature where you control it, and make the prompt specific enough that only a narrow range of answers is likely.

**A short check across runs.** Because the format is locked, comparing runs is easy to automate. Here are the expected totals from three runs of the same boundary prompt, collected into a dictionary. They are **illustrative**, written for this lesson:

```python
# compare_runs.py
# Expected totals from three runs of the same prompt (illustrative replies)
runs = {
    "run 1": {50.00: 45.00, 49.99: 49.99, 50.01: 45.01},
    "run 2": {50.00: 45.00, 49.99: 49.99, 50.01: 45.00},
    "run 3": {50.00: 45.00, 49.99: 44.99, 50.01: 45.01},
}

subtotals = sorted({s for answers in runs.values() for s in answers})
for s in subtotals:
    values = {name: answers.get(s) for name, answers in runs.items()}
    agreed = len(set(values.values())) == 1
    print(f"{s:6.2f}: {values}  {'agree' if agreed else 'DISAGREE'}")
```

Output:

```text
 49.99: {'run 1': 49.99, 'run 2': 49.99, 'run 3': 44.99}  DISAGREE
 50.00: {'run 1': 45.0, 'run 2': 45.0, 'run 3': 45.0}  agree
 50.01: {'run 1': 45.01, 'run 2': 45.0, 'run 3': 45.01}  DISAGREE
```

What to notice:

- `{s for answers in runs.values() for s in answers}` is a **set comprehension** that collects every subtotal mentioned in any run.
- `len(set(values.values())) == 1` is true only when all three runs gave the same value.
- Disagreement tells you **where to look**, not which run is right. The 49.99 and 50.01 rows need checking against AC1 and AC2; the majority is not automatically correct. Here the majority happens to be right for both, but two runs out of three agreeing on a wrong value is entirely possible.
- Agreement is not proof either. All three runs could agree on the same mistake. Consistency checks find **instability**; they do not replace checking against the requirement.

### 4. Worked Example: Automatic Checks on an AI Test Table

In the handout, you asked an AI assistant for test rows:

```text
Give EXACTLY 5 test rows for the SAVE10 coupon as a JSON list.
Each row: "subtotal" (number), "code" (string), "expected" (number).
```

Notice what this prompt does **not** include: the requirement. It names SAVE10, but does not paste US-205. That gap matters, as you will see.

The reply is **illustrative**, written for the handout to show several failure modes at once. It looks fine at a glance. Here is the handout's `failure_checks.py`, which checks it against Monday's real `cart.py`:

```python
import json
from cart import apply_coupon

# Step 1: we asked for EXACTLY 5 test rows for SAVE10; this is the AI's reply
ai_reply = """[
  {"subtotal": 100.00, "code": "SAVE10", "expected": 90.00},
  {"subtotal": 50.00,  "code": "SAVE10", "expected": 45.00},
  {"subtotal": 49.99,  "code": "SAVE10", "expected": 44.99},
  {"subtotal": 100.00, "code": "save10", "expected": 90.00}
]"""
rows = json.loads(ai_reply)

# Step 2: count check - did we get what we asked for?
ASKED_FOR = 5
if len(rows) != ASKED_FOR:
    print(f"COUNT: asked for {ASKED_FOR} rows, got {len(rows)}")

# Step 3: maths check - compare every expected value with the real code
def actual_result(subtotal, code):
    try:
        return apply_coupon(subtotal, code)
    except ValueError:
        return "ValueError"

problems = 0
for row in rows:
    actual = actual_result(row["subtotal"], row["code"])
    if actual != row["expected"]:
        problems += 1
        print(f"WRONG: {row['subtotal']} + {row['code']}: AI expects "
              f"{row['expected']}, real code gives {actual}")

# Step 4: summary
print(f"{problems} of {len(rows)} rows need a human decision")
```

Put it in the same folder as `cart.py` and run `python failure_checks.py`. Output:

```text
COUNT: asked for 5 rows, got 4
WRONG: 49.99 + SAVE10: AI expects 44.99, real code gives 49.99
WRONG: 100.0 + save10: AI expects 90.0, real code gives ValueError
2 of 4 rows need a human decision
```

What to notice in the code:

- `from cart import apply_coupon` loads the real function from Monday, so the AI's expectations can be compared with what the code actually does.
- **Step 2** is the simplest check of all. Two lines catch an **ignored instruction**.
- **Step 3** calls the real function for every row. Unknown codes **raise** a `ValueError`, so `actual_result` catches it and returns the text `"ValueError"`, letting the loop continue instead of crashing.
- A long f-string can be split over two lines inside the brackets; Python joins them.
- **Step 4** says "need a human decision", not "are wrong". That wording is deliberate, as section 5 shows.

#### 4.1 Be the human: who is right?

The script found three problems. For each, check the **requirement**, US-205:

| Flagged | Who is right? | Failure mode |
|---|---|---|
| Only 4 rows | The prompt asked for exactly 5 | **Ignored instruction** |
| 49.99 → 44.99 | **The code.** AC2: under $50.00 is unchanged | **Wrong maths** / contradicts the requirement |
| `save10` → 90.00 | **The code.** Nothing says lower-case codes work | **Hallucination**: an invented rule |

Two of the three failures trace back to the missing context. The prompt never pasted AC2 or AC3, so the model fell back on likely coupon behaviour: discounts apply to everything, and codes are not case-sensitive. That is the lesson of *Specificity and Context* showing up as defects.

### 5. A Mismatch Needs a Human Decision

Why does the script say "need a human decision" instead of "the AI is wrong"? Because the code can be wrong too.

**Work it through.** Take Monday's buggy version of `apply_coupon`, with `>` instead of `>=`, so that an order of exactly $50.00 no longer gets the discount. Run the same checks against it. We did, and the output was:

```text
COUNT: asked for 5 rows, got 4
WRONG: 50.0 + SAVE10: AI expects 45.0, real code gives 50.0
WRONG: 49.99 + SAVE10: AI expects 44.99, real code gives 49.99
WRONG: 100.0 + save10: AI expects 90.0, real code gives ValueError
3 of 4 rows need a human decision
```

A new row is flagged: the $50.00 case. This time, the requirement says the **AI is right** and the **code has the bug**. AC1 says $50.00 or more gets 10% off, so $45.00 is correct.

The script cannot tell these cases apart. It only knows the two sources **disagree**. **Only the requirement decides which one is wrong.** This is the oracle problem you met in Week 3: a test needs an independent source of truth, and here that source is US-205, not the AI and not the code.

This also shows why AI-drafted tests can be valuable even when some are wrong. The AI's $50.00 row, checked against the requirement, found a real bug.

### 6. Putting It Together: Debugging One Prompt Step by Step

Here is how a tester might fix the prompt from section 4, one change at a time:

| Run | Change | Result |
|---|---|---|
| 1 | Original prompt | 4 rows; wrong 49.99; invented `save10` |
| 2 | Paste AC1–AC4 from US-205, fenced with `###` | The 49.99 and `save10` mistakes usually disappear |
| 3 | Add "Use only the rules in the story. Do not invent rules." | Fewer invented cases in repeated runs |
| 4 | Move "Return EXACTLY 5 rows" to the last line | The count is obeyed more reliably |
| 5 | Run three times in new chats and run `failure_checks.py` on each | Confidence that the fix holds, not a lucky run |

Notice that each run changes **one** thing and is checked the same way. Run 5 is the step people skip, and it is the one that shows whether the prompt is reliable or lucky.

### 7. The Prompt-Debugging Checklist

When an AI answer is wrong, work through this list from the handout before rewriting the whole prompt. Change one thing at a time and re-run.

| # | Ask yourself | If the answer is "no"… |
|---|---|---|
| 1 | Did I paste the **exact** requirement (not retyped)? | Paste it, fenced with `###` markers |
| 2 | Did I say exactly **how many** items I want? | Say "exactly 5", not "some" |
| 3 | Did I name the **format** and every field? | Add an output-format section |
| 4 | Did I tell it to use **only the stated rules**? | Add: "Do not invent rules or values" |
| 5 | Did I allow it to **ask** instead of guess? | Add: "If something is unclear, ask a question" |
| 6 | Did I put the most important rule **last**? | Move key rules to the end |
| 7 | Did I start a **new chat** for the retry? | Old messages can keep steering the answer |

Each row maps to a failure mode: rows 1, 4 and 5 target hallucination; rows 2, 3 and 6 target ignored instructions; row 7 targets the leftover context of a long chat.

### 8. Which Checks Can Code Do?

Not every failure can be caught automatically. A useful split:

| Failure | Can code catch it? | How |
|---|---|---|
| Wrong count | ✅ Easily | `len(rows)` |
| Wrong format or missing fields | ✅ Easily | The shape checks from *Format Locking* |
| Wrong maths | ✅ If you can compute the right answer | Recalculate from the rule, or call the real code |
| Invented function | ✅ Often | Run it; an `AttributeError` or `ImportError` appears |
| Invented requirement | ⚠️ Partly | Code can flag a mismatch; only the requirement decides |
| Outdated method | ⚠️ Partly | Running against your version catches removed methods, not merely old-fashioned ones |
| Inconsistency | ⚠️ Partly | Run several times and compare outputs |
| A missing important test | ❌ Rarely | Needs a person who knows the risks |

The rule of thumb: **let code catch the easy failures, and save human attention for judgement calls.** On Wednesday you will build a full human review checklist; on Friday your agent will run the automatic checks itself.

### 9. Reporting an AI Failure Like a Bug

When a prompt fails in a way your team should know about, for example in a shared prompt library, report it like a defect. A useful template:

```text
Title: [Prompt: SAVE10 test rows v1] Invents case-insensitive codes
Prompt: SAVE10 test rows - v1 (from prompts.txt)
Tool and date: (the AI tool you used, and when)
Runs: 3 of 3 runs, new chat each time
Expected: only rules from US-205; codes are case-sensitive unless the story says otherwise
Actual: a row expects "save10" to give 90.00
Failure mode: hallucination (invented rule)
Likely cause: US-205 not pasted into the prompt
Suggested fix: paste AC1-AC4, add "Use only the rules in the story"
```

Three fields deserve attention:

- **Runs** says how often the failure happens. "3 of 3" is a reliable failure; "1 of 3" is intermittent and needs more runs to understand, just like a flaky test.
- **Failure mode** uses the vocabulary from this lesson, so teammates know at once what kind of problem it is.
- **Tool and date** matter because models change. A prompt that fails today may behave differently after a model update, and the report tells a reader which version you saw.

### 10. Which Failures to Expect, Task by Task

Different QE tasks tend to trigger different failure modes. Use this table to decide what to check first:

| QE task | Most likely failure modes | Check first |
|---|---|---|
| Drafting test cases from a story | Hallucinated rules; missing boundaries; wrong expected values | Trace each case to an AC; recalculate expected values |
| Generating test data | Ignored format; values that break the rules | Shape checks; rule checks on every record |
| Writing automation code | Invented or outdated methods; tests that cannot fail | Run it against your versions; break the feature on purpose |
| Explaining an error | Confident but wrong cause | Confirm the cause with the evidence before changing code |
| Summarising results | Wrong counts; missing the key failure | Compare numbers with the source report |
| Classifying (severity, duplicates) | Inconsistency; label bias | Run several times; review a batch together |

The pattern is the same in every row: the more the output is **numbers or facts**, the more you check with code; the more it is **judgement**, the more you check with a person and the requirement. Tomorrow's lessons apply this to each stage of the QA lifecycle.

### 11. Other Failures You Will Meet

A few more patterns are worth recognising, even though this lesson does not cover them in depth:

- **Agreeing too easily.** Tell an assistant "I think 49.99 should get the discount" and it may agree, even though AC2 says otherwise. Present the requirement, not your opinion, and ask it to check against the requirement.
- **Over-long answers.** Asked for a summary, it writes an essay. Give an exact length.
- **Prompt injection.** Text inside pasted data tries to give the model instructions. You meet this on Wednesday, in *Responsible Use of AI in QE*.

---

## Practice Exercises

1. **Name the failure (paper, 10 min).** Name the failure mode for each, and suggest one fix:
   - (a) Asked for "exactly 3 test ideas", the AI gives 6.
   - (b) The AI writes a Playwright test using a method you cannot find in the Playwright docs.
   - (c) Two runs of the same prompt give the $50.01 case an expected total of 45.01 and 45.00.
   - (d) The AI suggests `driver.find_element_by_name("email")` for your Selenium 4 project.

2. **Complete the table (paper and code, 15 min).** Add a fifth row to `ai_reply`: `{"subtotal": 50.01, "code": "SAVE10", "expected": 45.01}` (remember the comma after the previous row). Predict which messages disappear, then run the script to check. Then add a sixth row with an unknown code that **should** raise an error, and decide what its `expected` value must be for the check to pass.

   *Hint:* look at what `actual_result` returns for unknown codes.

3. **Fix the prompt, one change at a time (AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** send the handout's original prompt to your AI assistant in a new chat. Then improve it in three separate runs, adding one change each time: paste US-205, add "use only the rules in the story", and move "exactly 5" to the last line.
   - **Review:** for each run, note which failure modes appear.
   - **Run:** paste each reply into `ai_reply` and run `failure_checks.py`.
   - **Record:** build a small table like the one in section 6, and save the best prompt in `prompts.txt` as `=== SAVE10 test rows - v2 ===`.

4. **Outdated knowledge (AI tool, 10 min).** Ask your AI assistant: *"How do I find an element by ID in Selenium with Python?"* Note which form it suggests. Then check the Selenium documentation. Write one line you could add to future prompts to prevent the outdated form.

---

## Knowledge Check

1. What is a prompt failure mode?

<details><summary>Answer</summary>

A typical way an AI answer goes wrong, even when the prompt looked fine, such as hallucination, ignored instructions, wrong maths, outdated knowledge or inconsistency.

</details>

2. Why do LLMs make arithmetic mistakes, and what is the fix?

<details><summary>Answer</summary>

They predict digits as text rather than calculating. The fix is to check every expected value against the rule, by hand or in code.

</details>

3. Why might an instruction in the middle of a long prompt be ignored?

<details><summary>Answer</summary>

Models tend to use information at the start and end of a long input best; information in the middle is used less reliably. Put key rules near the end.

</details>

4. In `failure_checks.py`, why does the summary say "need a human decision" rather than "are wrong"?

<details><summary>Answer</summary>

A mismatch only shows that the AI and the code disagree. Either could be wrong; only the requirement decides.

</details>

5. Against the buggy `>` version of `cart.py`, the $50.00 row was flagged. Who was right, and why?

<details><summary>Answer</summary>

The AI. AC1 says $50.00 or more gets 10% off, so the expected $45.00 is correct and the code has the bug.

</details>

6. Three runs agree on a value. Does that prove the value is right?

<details><summary>Answer</summary>

No. Agreement only shows the prompt is stable; all three runs could share the same mistake. The value still needs checking against the requirement.

</details>

7. Why should you re-run a fixed prompt several times before trusting it?

<details><summary>Answer</summary>

Because of sampling, one good run can be luck. Several runs, each checked, show whether the fix is reliable.

</details>

---

## Glossary

- **Prompt failure mode:** a typical way an AI answer goes wrong.
- **Hallucination:** confident but false content, such as an invented rule, function or package.
- **Ignored instruction:** an answer that breaks a clear instruction in the prompt.
- **Wrong maths:** arithmetic errors in AI-written values.
- **Outdated knowledge:** answers based on old versions or practices, because of the training cut-off.
- **Inconsistency:** different answers to the same prompt.
- **Lost in the middle:** the finding that models use information in the middle of long inputs less reliably.
- **Oracle:** an independent source of truth for a test; here, the requirement.
- **Mismatch:** a disagreement between the AI's expected value and the code's actual result.
- **Reproduce (a failure):** run the same prompt again, in a new chat, to see whether the failure repeats.
- **Consistency check:** comparing the answers from several runs of the same prompt to find unstable values.
- **Intermittent failure:** a failure that appears in some runs but not others, like a flaky test.
- **Prompt failure report:** a bug-report-style record of a prompt's failure, its failure mode and a suggested fix.

---

## Summary

- **AI answers fail in typical ways:** hallucination, ignored instructions, wrong maths, outdated knowledge and inconsistency.
- **Each failure comes from the same root:** the model predicts likely text, and does not check facts, count or calculate.
- **Debug prompts like tests:** reproduce over several runs, change one thing, re-run and compare.
- **Let code catch the easy failures:** counts, formats, maths and missing functions.
- **A mismatch needs a human decision.** The AI or the code could be wrong; the requirement decides.
- **Most failures shrink with better context and exact instructions**: paste the requirement, use exact numbers and put key rules last.

---

## Additional Resources

- Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*: https://arxiv.org/abs/2307.03172
- Selenium blog, *Locate your locators: Python bindings changes upcoming* (the removed `find_element_by_*` methods): https://www.selenium.dev/blog/2022/python-locators-se4/
- OpenAI Help Center, *Best practices for prompt engineering with the OpenAI API*: https://help.openai.com/en/articles/6654000
