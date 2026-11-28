# AI-Generated Test Cases

## Learning Objectives

By the end of this lesson you will be able to:

- **Describe** the anatomy of a good test case, and why each field matters.
- **List** what AI typically gets right and wrong when it drafts test cases.
- **Write** a test case generation prompt that reduces the most common mistakes.
- **Review** an AI draft with short Python checks for missing fields, coverage and exact messages.
- **Complete** the review by hand, finding the problems code cannot: invented rules and missing boundaries.

---

## Why This Matters

Writing test cases by hand is slow. For a story like US-205, a careful tester might spend half an hour writing ten good cases. An AI assistant can draft twenty in ten seconds. That speed is real, and teams use it.

But you have already seen what an unchecked AI draft looks like. On Monday, in *Generative AI Applications within QE*, the AI-drafted tests for `cart.py` gave **3 failed, 1 passed** against correct code: they expected the wrong values. A draft that looks professional can still be wrong in the details that matter most to testers: boundaries, exact messages and rules nobody asked for.

The risk grows with volume. Twenty well-formatted test cases **look** thorough, so it is tempting to accept them in bulk. This lesson teaches a review that scales: **let code check the structure** (are fields filled in, is every requirement covered, are messages copied exactly?), then **let a human check the meaning** (does each case make sense, and is anything invented or missing?).

> **Using this with the handout:** this lesson goes deeper into **Handout 05, Topic 3**. It uses the same AI draft for US-205 (TC-01 to TC-05), the same `review_cases.py` and the same checks.

---

## The Concept

### 1. The Anatomy of a Good Test Case

A **test case** is a documented check with an ID, the requirement it covers, steps, test data and an expected result. Here is one from the handout, field by field:

| Field | Example | Why it matters |
|---|---|---|
| **ID** | TC-02 | So people and tools can refer to it, for example in a bug report |
| **Requirement (AC)** | US-205 AC1 | Traceability: proves it checks something that was asked for |
| **Title** | SAVE10 on exactly $50.00 | Tells a reader what it checks at a glance |
| **Steps** | 1. Add items totalling $50.00. 2. Enter SAVE10. 3. Click Apply. | So anyone can repeat it the same way |
| **Expected result** | Total is $45.00 | The pass/fail rule. Without it, it is not a test |

Two fields deserve extra attention:

- **The requirement field** is what makes review possible. A case that names AC1 can be checked against AC1. A case that names nothing cannot be checked against anything.
- **The expected result** must be **exact**. "Discount applied" is not exact; "Total is $45.00" is. When a message is involved, the expected result must contain the message **character for character**, because automated tests compare text exactly: `"Spend $50 to use SAVE10"` is **not** equal to `"Spend $50.00 to use SAVE10"`.

### 2. What AI Gets Right, and What It Gets Wrong

AI drafts follow a recognisable pattern:

| Usually right | Often wrong |
|---|---|
| Structure and formatting | **Boundaries** (missing $50.00 or $50.01, or the wrong side of the boundary) |
| Clear titles and steps | **Exact messages** (paraphrased: "Spend $50 to use SAVE10") |
| Many **positive** cases | **Uncovered criteria** (AC4 often has no case at all) |
| Obvious **negative** cases | **Invented rules** ("lowercase save10 is accepted") |
| | **Empty or vague expected results** |
| | **Duplicates** (two cases checking the same thing) |

The left column is why AI drafts are useful. The right column is why every draft needs review. Notice that the right column lists the **testing** skills: boundaries and exact expected results are what a tester adds to a feature description. An AI that is good at sounding like a test case is not automatically good at being one.

Why does AI paraphrase messages in particular? Recall *Generative AI Concepts* from Monday: a language model writes the **likely** next words. "Spend $50 to use SAVE10" is a very likely way to write that sentence, because people usually write round dollar amounts without cents. The model is not copying from the story character by character unless something makes it; it is writing a plausible sentence about the story.

That is why the stronger prompt says "copy any quoted message exactly", and why the code check for exact messages is still needed afterwards.

### 3. Prompting for Better Drafts

The handout's worked example uses a deliberately simple prompt, so you can see typical mistakes:

```text
Write test cases for US-205 with id, ac, title and expected.
```

Using Tuesday's techniques, a stronger prompt targets the right-hand column directly:

```text
You are a test analyst. Write test cases for the user story below.

### User story
US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
### End

Rules:
- Use only rules stated in the story. If something is unclear, list it as a question instead.
- Every test case names exactly one AC.
- Every AC has at least one test case.
- Include boundary cases at $49.99, $50.00 and $50.01.
- Copy any quoted message exactly, character for character.

Reply as a Python list of dictionaries with keys: id, ac, title, expected.
```

Each rule answers one item in the "often wrong" column. Better prompts **reduce** mistakes; they do not remove them. You still review the draft, as the rest of this lesson shows. But fewer mistakes means a faster review.

### 4. Worked Example: Review an AI Draft with Code

**The situation:** the handout asked an AI to *"Write test cases for US-205 with id, ac, title and expected."* Here is its draft. Create `review_cases.py`.

#### Step 1: The story and the draft

```python
# Step 1: the story and the AI's draft test cases
STORY = {
    "AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "AC2": 'Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".',
    "AC3": 'Unknown codes show "Coupon code not recognised".',
    "AC4": "Only one coupon per order.",
}
draft = [
    {"id": "TC-01", "ac": "AC1", "title": "SAVE10 on $100.00", "expected": "Total is $90.00"},
    {"id": "TC-02", "ac": "AC1", "title": "SAVE10 on exactly $50.00", "expected": "Total is $45.00"},
    {"id": "TC-03", "ac": "AC2", "title": "SAVE10 on $49.99",
     "expected": 'Total is $49.99 and "Spend $50 to use SAVE10" is shown'},
    {"id": "TC-04", "ac": "AC3", "title": "Unknown code BOGUS",
     "expected": 'Message "Coupon code not recognised" is shown'},
    {"id": "TC-05", "ac": "AC3", "title": "Lowercase save10 is accepted", "expected": ""},
]
```

**What this code does:**

- `STORY` is a **dictionary** mapping each AC ID to its text. AC2 and AC3 contain quoted messages, so those strings use **single** quotes `'...'` on the outside, which keeps the double quotes inside.
- `draft` is the AI's answer as a **list of dictionaries**, one per test case. The steps are left out to keep the example short.

Before running any checks, read the draft yourself. It **looks** professional: consistent IDs, clear titles, money values to the cent. Try to spot the problems before the code does.

#### Step 2: Check required fields

```python
# Step 2: every test case needs all fields filled in
for tc in draft:
    for field in ("id", "ac", "title", "expected"):
        if not tc.get(field):
            print(f"{tc['id']}: missing '{field}'")
```

**What this code does:**

- `tc.get(field)` returns the value, or `None` if the key does not exist.
- `not tc.get(field)` is `True` for **both** a missing key (`None`) and an empty string (`""`), because Python treats both as "empty". So one check catches both problems.
- A test case without an expected result **cannot pass or fail**, so it is not a test.

#### Step 3: Check coverage

```python
# Step 3: coverage - does every AC have at least one test case?
covered = {tc["ac"] for tc in draft}
for ac in STORY:
    if ac not in covered:
        print(f"{ac}: no test case covers this criterion")
```

**What this code does:**

- `{tc["ac"] for tc in draft}` is a **set comprehension**: it builds the set of AC IDs that appear in the draft, here `{"AC1", "AC2", "AC3"}`. A set keeps each value once, even though AC1 appears twice.
- Looping over `STORY` gives the keys AC1 to AC4. Any AC not in the set has **no** test case.

This is a tiny **traceability** check: from each requirement, can we find a test?

#### Step 4: Check exact messages

```python
# Step 4: exact messages - quoted text in an AC must be copied exactly
for tc in draft:
    if '"' in STORY[tc["ac"]]:
        message = STORY[tc["ac"]].split('"')[1]
        if message not in tc["expected"]:
            print(f"{tc['id']}: expected result does not contain \"{message}\"")
```

**What this code does:**

- `STORY[tc["ac"]]` looks up the text of the AC this test case covers.
- If that text contains a `"`, it has a quoted message. `split('"')` cuts the text at each `"`, and `[1]` is the piece **between** the first pair of quotes. For AC2, that is `Spend $50.00 to use SAVE10`.
- `message not in tc["expected"]` checks that the **exact** message appears in the expected result. One missing character is enough to fail.

#### The output

Put the four steps together in `review_cases.py` (the handout's consolidated file) and run `python review_cases.py`:

```text
TC-05: missing 'expected'
AC4: no test case covers this criterion
TC-03: expected result does not contain "Spend $50.00 to use SAVE10"
TC-05: expected result does not contain "Coupon code not recognised"
```

Four findings, in about a millisecond. Notice that TC-05 is reported twice: once for the empty expected result, and once because an empty string cannot contain AC3's message. Two lines about the same case are a strong hint that the case needs a closer look.

### 5. The Human Review: What Code Cannot Find

The code found four problems. Now ask the question that matters: **what did it not find?** Go through each finding, and then through the draft as a whole:

| Test case | Code found | Human adds |
|---|---|---|
| TC-03 | Wrong message | Fix it: copy the message exactly, `"Spend $50.00 to use SAVE10"` |
| TC-05 | Empty expected result | **Invented rule.** Nothing in US-205 says lowercase works. **Remove it and ask the BA.** The code cannot know this. |
| AC4 | Not covered | Add a test case, but first ask the BA what message appears (from *AI-Assisted Requirements Analysis*) |
| — | — | **Missing boundary:** nothing tests just above the boundary, at $50.01 |

The TC-05 row is the most important one. The code reported TC-05 for an **empty field**. A tester who only fixes what the code reports might fill in the field: "expected: total is $90.00". Now TC-05 passes every check, and the invented rule is **in the suite**, looking perfectly valid. The real problem was never the empty field; it was the title. Only a person reading the title against the story can see that.

The last row is a different kind of gap: something **missing**, not something wrong. Code can only check what is there. The tester's knowledge of boundary value analysis, from Tuesday's *AI-Assisted Test Design*, says a boundary at $50.00 needs a case at $49.99, at $50.00 and at $50.01. The draft has the first two only.

This division of work is the core idea of the lesson:

| Code checks **structure** | Humans check **meaning** |
|---|---|
| Are all fields filled in? | Does each case make sense? |
| Is every AC covered? | Is any rule invented? |
| Are messages copied exactly? | Are boundaries and edge cases missing? |
| Are there exact duplicates? | Are two cases really testing the same thing? |

### 6. Fixing the Draft and Re-Running

Apply the human review: fix TC-03's message, remove TC-05, add TC-06 for AC4 (with its expected result marked as unconfirmed), and add TC-07 at $50.01. The new draft:

```python
draft = [
    {"id": "TC-01", "ac": "AC1", "title": "SAVE10 on $100.00", "expected": "Total is $90.00"},
    {"id": "TC-02", "ac": "AC1", "title": "SAVE10 on exactly $50.00", "expected": "Total is $45.00"},
    {"id": "TC-03", "ac": "AC2", "title": "SAVE10 on $49.99",
     "expected": 'Total is $49.99 and "Spend $50.00 to use SAVE10" is shown'},
    {"id": "TC-04", "ac": "AC3", "title": "Unknown code BOGUS",
     "expected": 'Message "Coupon code not recognised" is shown'},
    {"id": "TC-06", "ac": "AC4", "title": "Second coupon is rejected",
     "expected": "Only the first coupon is applied (to confirm with the BA)"},
    {"id": "TC-07", "ac": "AC1", "title": "SAVE10 on $50.01", "expected": "Total is $45.01"},
]
```

Check TC-07 by hand first: 10% off $50.01 is 50.01 × 0.9 = 45.009, which rounds to **$45.01**. (You met this exact calculation in Tuesday's *Prompt Engineering Principles*, where an AI got it wrong.)

Running the three checks on the new draft prints **nothing**: no missing fields, every AC covered, every message exact.

An empty output is good news, but read it precisely. It means the **structure** is now right. It does not mean the suite is complete or correct. The checks would print nothing, for example, if TC-07's expected result said $45.00. Only your hand calculation caught that kind of mistake.

Writing the expected value of every boundary case by hand, before you look at the AI's value, is the habit that catches this. It takes seconds, and none of the scripts in this lesson can do it for you.

Two more things to notice about TC-06. Its ID skips TC-05 on purpose: reusing a removed ID can confuse anyone who saw the old version, for example in a review comment. And its expected result carries the label **(to confirm with the BA)**, because the story does not say what happens on a second coupon. That makes the uncertainty visible instead of hiding it inside a confident sentence.

### 7. A Printed Traceability Matrix

A **traceability matrix** shows which test cases cover each requirement. The coverage check in Step 3 tells you which ACs have **no** cases. Adding three lines lists them all:

```python
for ac in STORY:
    ids = [tc["id"] for tc in draft if tc["ac"] == ac]
    print(f"{ac}: {', '.join(ids) if ids else '-'}")
```

On the fixed draft it prints:

```text
AC1: TC-01, TC-02, TC-07
AC2: TC-03
AC3: TC-04
AC4: TC-06
```

Read it like a reviewer. AC1 has three cases, which makes sense: it contains the boundary. AC2 and AC3 have one each, which is thin; a second AC2 case at, say, $20.00 would show the rule is not only about the boundary. AC4 has one case, which is waiting on the BA. A matrix does not judge whether coverage is **enough**; it makes the question easy to ask.

### 8. Reviewing the Steps

The handout's draft left out the steps to keep the example short. Real AI drafts include them, and they need reviewing too. Here is a typical AI version of TC-02's steps, **illustrative**:

```text
TC-02: SAVE10 on exactly $50.00
Steps:
1. Add items to the cart.
2. Apply the coupon.
3. Verify the discount.
Expected: Discount is applied correctly.
```

It reads smoothly, but apply one test: **could a tester who has never seen this feature repeat it exactly, and decide pass or fail without asking anyone?**

| Line | Problem | Better |
|---|---|---|
| "Add items to the cart" | Which items? The whole point is a $50.00 subtotal | "Add items totalling exactly $50.00 (for example, 2 × $25.00)" |
| "Apply the coupon" | Which coupon? How? | "Type SAVE10 in the coupon field and click Apply" |
| "Verify the discount" | Verify what, exactly? | Remove: the expected result says what to check |
| "Discount is applied correctly" | Not a pass/fail rule | "Total is $45.00" |

Two more things are often missing from AI steps:

- **Preconditions:** the state the system must be in before step 1. For TC-02: "The cart is empty, and no coupon has been applied to this order." Without it, a coupon left from an earlier test could change the result, which also matters for AC4.
- **Test data:** the specific values, written down. "Items totalling exactly $50.00" is better than "some items"; "2 × $25.00" is better still, because anyone can repeat it.

Vague steps are the most common way a test case that **looks** fine turns out to be untestable. They are also something code cannot check: a script cannot tell whether "Verify the discount" is clear enough. Read the steps of every high-risk case yourself.

### 9. Edge Cases AI Tends to Skip

Even with the stronger prompt, AI drafts tend to stick close to the acceptance criteria. That sounds good, and mostly it is. But testers also think about **edge cases**: unusual but possible inputs. For US-205, a tester might list:

| Edge case | Covered by an AC? | What to do |
|---|---|---|
| An empty coupon field, then Apply | No | Ask the BA what is shown |
| `" SAVE10 "` with spaces around it | No | Ask the BA whether spaces are ignored |
| Applying SAVE10, then removing items below $50.00 | No | Ask the BA (found in *AI-Assisted Requirements Analysis*) |
| A subtotal of $0.00 | Partly (AC2 says under $50.00 is unchanged) | Test it: expected unchanged total and the AC2 message |

Look at the last column. Three of the four rows say **ask the BA**, not "write a test case". If you or the AI wrote expected results for those cases now, they would be guesses: invented rules again, created by a well-meaning tester. The fourth row is different: AC2 already covers it, so you can write the case today.

Asking an AI *"Which edge cases does this suite not cover?"* is a good use of it, as long as you treat its answer as a list of **questions** and triage it, exactly as in the requirements lesson.

### 10. When the AI Is Right and You Are Wrong

Reviews work both ways. Sometimes the AI's case is correct and the reviewer's "fix" is the mistake. A classic example: a reviewer reading TC-02 quickly thinks *"$50.00 is not over $50, so there is no discount; the expected result should be $50.00"*. They have misremembered the rule. US-205 says "**$50.00 or more**", so $45.00 is right.

The protection is the same habit you use on AI output: **check the story, not your memory.** Before you change any expected result, quote the AC that justifies the change. If you cannot quote it, do not change it. That one rule protects the suite from both AI mistakes and human ones.

### 11. Reviewing Larger Drafts

Four or six test cases can be reviewed by reading every line. Forty cannot, at least not with equal care for each. A workable routine:

1. **Run the structure checks first.** They take milliseconds at any size and clear out the mechanical problems.
2. **Print the traceability matrix.** Look for ACs with no cases, and ACs with suspiciously many (often duplicates).
3. **Read every title against the story.** Titles are short, and invented rules usually show in the title, as with TC-05.
4. **Check every boundary and every message case in full.** These are where AI mistakes cluster.
5. **Sample the rest**, more heavily for high-risk areas such as money.

You will see this idea, matching review depth to risk, in *Human Validation of AI Output* this afternoon. For US-205, which is about discounts, the answer is simple: money is high risk, so every case gets a full review.

### 12. Common Errors

When you run the checks on your own AI's drafts, these are the errors you are most likely to see:

| Error you see | Why it happens | Fix |
|---|---|---|
| `KeyError: 'AC5'` | A test case refers to an AC that is not in `STORY` | Check the `ac` value. It could also be an AI hallucination worth reporting |
| `IndexError: list index out of range` in Step 4 | The AC text has only one `"` | Make sure quoted messages have opening **and** closing quotes |
| `KeyError: 'id'` | A draft item has no `id` key, and the print uses `tc['id']` | Use `tc.get('id', '?')` in the print |
| `NameError: name 'true' is not defined` | The AI replied in JSON, not Python | Ask again for a "Python list", or use `True` and `None` |
| `SyntaxError` after pasting | The AI added text before or after the list | Paste only the part from `[` to `]` |

The first row deserves a second look. An AI that writes test cases for **AC5** of a story with four ACs has invented a requirement. The `KeyError` is the code's way of telling you so.

---

## Practice Exercises

1. **Fix one message (code, 5 min).** In `review_cases.py`, fix TC-03's expected result so it contains the exact message. Run the file again. Which line disappears from the output, and which remain?

2. **Add AC4 (code, 10 min).** Add `{"id": "TC-06", "ac": "AC4", "title": "Second coupon is rejected", "expected": "Only the first coupon is applied"}` and run the checks. Is AC4 now covered? Is this expected result **confirmed** by the story, or a guess? How would you mark it?

3. **Duplicate check (code, 15 min).** Add a check that prints a warning if two test cases have the same `title`. Hint: create an empty set called `seen` before the loop, and add each title to it after checking. Test it by adding a copy of TC-01 with a new ID.

4. **Review your own AI's draft (AI tool, 25 min).** Follow this week's four steps:
   - **Prompt:** send the stronger prompt from section 3 to your AI assistant.
   - **Review:** read every title against US-205 before running anything. Note any invented rules.
   - **Run:** paste its list into `review_cases.py` as `draft` and run the checks, then print the traceability matrix.
   - **Record:** in `prompts.txt`, note how many problems the code found, how many you found by reading, and which prompt rule (if any) the AI ignored.

5. **Tighten the steps (AI tool, 15 min).** Paste the vague TC-02 from section 8 into your AI assistant and ask: *"Rewrite these steps so a new tester could repeat them exactly. Add a precondition and specific test data. Do not change the requirement."* Check its answer against the "Better" column. Did it add anything not in US-205?

---

## Knowledge Check

1. Name the five fields of a good test case and why the requirement field matters.

<details><summary>Answer</summary>

ID, requirement (AC), title, steps and expected result. The requirement field gives traceability: it lets a reviewer check the case against the criterion it claims to test.

</details>

2. Name three things AI often gets wrong in test case drafts.

<details><summary>Answer</summary>

Any three of: boundaries, exact messages, uncovered criteria, invented rules, empty or vague expected results, duplicates.

</details>

3. Why does `not tc.get(field)` catch both missing keys and empty strings?

<details><summary>Answer</summary>

`get` returns `None` for a missing key, and Python treats both `None` and `""` as false, so `not` makes both `True`.

</details>

4. The code reported TC-05 only for an empty expected result. Why would filling in that field be the wrong fix?

<details><summary>Answer</summary>

The real problem is the title's invented rule: US-205 never says lowercase codes work. Filling in the field would make the invented rule pass every check. The case should be removed and the question taken to the BA.

</details>

5. The checks print nothing for the fixed draft. What does that prove, and what does it not prove?

<details><summary>Answer</summary>

It proves the structure is right: fields filled, every AC covered, messages exact. It does not prove the expected values are correct or that coverage is enough.

</details>

6. Why is $50.01 needed in addition to $49.99 and $50.00?

<details><summary>Answer</summary>

Boundary value analysis tests just below, on and just above a boundary. $50.01 confirms the discount still applies above the boundary, and its expected value ($45.01) checks rounding.

</details>

7. A `KeyError: 'AC5'` appears when you review an AI draft for US-205. What might it mean?

<details><summary>Answer</summary>

A test case refers to an AC that does not exist. Either it is a typo, or the AI has invented a requirement, which is worth noting in your review.

</details>

8. An AI case has the step "Verify the discount" and the expected result "Discount is applied correctly". What is wrong?

<details><summary>Answer</summary>

Neither gives a pass/fail rule. The step should be removed or made specific, and the expected result should state the exact value, such as "Total is $45.00".

</details>

---

## Glossary

- **Test case:** a documented check with an ID, the requirement it covers, steps, test data and an expected result.
- **Expected result:** the exact outcome that decides whether a test passes or fails.
- **Traceability:** the link from each test case back to the requirement it checks.
- **Coverage:** which requirements have at least one test case.
- **Traceability matrix:** a table showing which test cases cover each requirement.
- **Set comprehension:** Python syntax `{expr for item in items}` that builds a set, keeping each value once.
- **Exact match:** text that is identical character for character.
- **Invented rule:** a rule in AI output that is not stated in the requirement.
- **Boundary case:** a test just below, on, or just above a limit.
- **Duplicate test case:** two cases that check the same thing.
- **Precondition:** the state the system must be in before a test's first step.
- **Edge case:** an unusual but possible input or situation, such as an empty coupon field.
- **Structure check:** an automated check of fields, coverage or format, as opposed to meaning.

---

## Summary

- A good test case has an **ID, a requirement, a title, steps and an exact expected result**. The requirement field makes review possible.
- AI drafts are usually well-structured but often wrong on **boundaries, exact messages, coverage and invented rules**.
- A stronger prompt **reduces** these mistakes; review is still essential.
- **Code checks structure** (fields, coverage, exact messages) in milliseconds; **humans check meaning** (invented rules, missing boundaries, whether a case makes sense).
- **An empty check output means the structure is right**, not that the suite is complete. Calculate expected values by hand, and use a traceability matrix to question coverage.

---

## Additional Resources

- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* (test case design and traceability): https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- Python documentation, *Data Structures* (dictionaries, sets and comprehensions): https://docs.python.org/3/tutorial/datastructures.html
- Python documentation, *Built-in Types: `str.split`*: https://docs.python.org/3/library/stdtypes.html#str.split
