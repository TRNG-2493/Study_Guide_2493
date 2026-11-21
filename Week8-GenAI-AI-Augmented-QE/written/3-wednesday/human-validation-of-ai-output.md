# Human Validation of AI Output

## Learning Objectives

By the end of this lesson you will be able to:

- Explain **why** AI output must be validated by a human, using the ideas of **fluency is not correctness**, **automation bias** and **anchoring**.
- Describe the main **human-in-the-loop** roles (author, reviewer, approver) and why a named person, not the AI, is accountable for every AI-assisted QA artifact.
- Apply a nine-point **human review checklist** (correct, complete, grounded, relevant, consistent, executable, traceable, safe, non-duplicated) to AI-generated test cases, test data, automation code and other QA artifacts.
- Decide **how much** review an artifact needs using **risk-based review depth**, and review large volumes fairly using **sampling** with an escalation rule.
- Keep a **correction log** that records what the AI got wrong, why, what you changed it to and what evidence you used.
- Calculate simple **review metrics** (acceptance rate, edit rate, rejection rate, top correction categories) and use them to improve your prompts.
- Write small Python **review aids** that point a reviewer at suspicious items, while keeping the final decision with the human.

---

## Why This Matters

On Monday you learned that a large language model (LLM) works by **next-token prediction**: it produces text that is statistically likely, not text that has been checked. On Tuesday you learned to steer it with specific, format-locked, few-shot prompts. Earlier today you used AI to analyse requirements and to generate test cases, test data and automation.

All of that work produces **drafts**, and any draft can contain a mistake that looks perfectly professional: a neat ID, a clear title, a confident expected result, and a boundary in the wrong place. A wrong test does one of two bad things:

- It **fails on correct software**, wasting time on a false alarm and teaching the team to ignore failures.
- It **passes on broken software**, because the expected result agrees with the defect. This is the worst outcome in testing: a green build that hides a real bug.

Human validation is the step that turns an AI draft into a trustworthy QA artifact. Teams that adopt AI in testing successfully do not remove the human; they **move** the human from writing everything by hand to **reviewing, correcting and approving**. That is a different skill, and it is the skill this lesson teaches.

This is the "with human validation" part of the **Weekly Epic**, and it matters even more on Thursday and Friday, when you build a QA agent that produces output automatically and repeatedly. It also feeds **Project 2 (Test Automation Framework)**: today's exercise asks you to generate AI test cases and data for the e-commerce app and to **document your corrections**. The correction log in this lesson is exactly that document.

> **Scope note.** This lesson is about how **people** review AI output: the checklist, review depth, sampling, correction logs, metrics and sign-off. You will write a few small Python helpers that support a reviewer, but they are aids, not judges. Automated, schema-based validation of an agent's output and full validation scripts are covered on **Friday**. A formal taxonomy of hallucination types and using one model to grade another (**LLM-as-judge**) are covered in **Week 10**. Here we only name them.

---

## The Concept

### 1. The Running Example: An AI Draft for US-205

We will use one AI-generated draft throughout the lesson. It comes from our Project 2 e-commerce app. Here is the user story it was generated from:

> **US-205 Apply coupon at checkout.** As a shopper I want to apply a coupon code so that I pay less.
>
> - **AC1:** SAVE10 gives 10% off a subtotal of $50.00 or more.
> - **AC2:** Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
> - **AC3:** Unknown codes show "Coupon code not recognised".
> - **AC4:** Only one coupon per order.

A tester sent a format-locked prompt (Tuesday) asking for test cases as a JSON array, one object per test case, with the fields `id`, `title`, `ac`, `subtotal`, `code`, `expected_total` and `expected_message`. We cannot call a real model in a lesson (the answer would change every time and would need an account and network access), so we use the same approach as Monday and Tuesday: a **deterministic stand-in** called `fake_llm` that always returns the same canned answer. The answer below is **illustrative**: it was written to show the kinds of mistakes real models make, not copied from a specific model.

```python
# ai_draft.py
import json

def fake_llm(prompt: str) -> str:
    """Deterministic stand-in for an LLM. Returns a canned, ILLUSTRATIVE
    response so the lesson runs offline and gives the same output every time."""
    return json.dumps([
        {"id": "TC-01", "title": "Discount applied at exactly $50.00", "ac": "AC1",
         "subtotal": 50.00, "code": "SAVE10", "expected_total": 45.00, "expected_message": None},
        {"id": "TC-02", "title": "Discount applied above threshold", "ac": "AC1",
         "subtotal": 120.00, "code": "SAVE10", "expected_total": 108.00, "expected_message": None},
        {"id": "TC-03", "title": "Discount just below threshold", "ac": "AC1",
         "subtotal": 49.99, "code": "SAVE10", "expected_total": 44.99, "expected_message": None},
        {"id": "TC-04", "title": "Lower-case code is accepted", "ac": "AC1",
         "subtotal": 80.00, "code": "save10", "expected_total": 72.00, "expected_message": None},
        {"id": "TC-05", "title": "Unknown code is rejected", "ac": "AC3",
         "subtotal": 60.00, "code": "FREESHIP", "expected_total": 60.00,
         "expected_message": "Invalid coupon"},
        {"id": "TC-06", "title": "Discount at threshold", "ac": "AC1",
         "subtotal": 50.00, "code": "SAVE10", "expected_total": 45.00, "expected_message": None},
        {"id": "TC-07", "title": "Coupon removed after logout", "ac": "AC5",
         "subtotal": 75.00, "code": "SAVE10", "expected_total": None, "expected_message": None},
    ])

if __name__ == "__main__":
    draft = json.loads(fake_llm("Generate test cases for US-205 ..."))
    for tc in draft:
        print(tc["id"], tc["ac"], tc["subtotal"], tc["code"], "->",
              tc["expected_total"], tc["expected_message"])
```

Let's walk through it:

- `fake_llm(prompt)` takes a prompt string (which it ignores) and returns a **string** of JSON, just like a real model returns text. `json.dumps(...)` turns the Python list of dictionaries into that JSON string. Python's `None` becomes JSON's `null`.
- `json.loads(...)` does the reverse: it parses the text back into Python objects. This is the same "parse the model's text" step you practised in Tuesday's format-locking lesson.
- `if __name__ == "__main__":` means "only run this block when the file is executed directly". Later we will **import** `fake_llm` from this file, and we do not want the printing to happen on import.

Running it prints:

```text
TC-01 AC1 50.0 SAVE10 -> 45.0 None
TC-02 AC1 120.0 SAVE10 -> 108.0 None
TC-03 AC1 49.99 SAVE10 -> 44.99 None
TC-04 AC1 80.0 save10 -> 72.0 None
TC-05 AC3 60.0 FREESHIP -> 60.0 Invalid coupon
TC-06 AC1 50.0 SAVE10 -> 45.0 None
TC-07 AC5 75.0 SAVE10 -> None None
```

Before reading on, **pause and review these seven test cases yourself** against AC1-AC4. Write down every problem you can find. We will come back to your list in section 5. This is the core skill of the lesson, so it is worth the two minutes.

### 2. Why AI Output Needs a Human: Three Traps

It is tempting to think "the AI is usually right, so a quick glance is enough". Three well-studied human tendencies make that quick glance much less reliable than it feels.

#### Trap 1: Fluency is not correctness

An LLM is trained to produce text that **reads well**; correctness depends on facts (the requirement, the product's real behaviour) that the model may not have or may mix up. Humans, however, use fluency as a shortcut for trust: a neat table with consistent IDs *feels* reliable. In the draft above, TC-03 has a perfectly reasonable title, "Discount just below threshold", and a precise-looking expected total of 44.99. Nothing about its *form* tells you it is wrong. Only comparing it with AC2 does.

**Analogy:** a confident tour guide who has never visited the city. Every sentence sounds authoritative; some of the directions are invented. You only find out by checking the map.

#### Trap 2: Automation bias

**Automation bias** is the tendency to favour suggestions from an automated system and to under-check them, even when other information contradicts them. In QA it looks like this:

- The AI says the expected total is 44.99, so the reviewer types 44.99 into the test without recomputing it.
- The AI lists seven test cases, so the reviewer assumes seven is "complete" and does not ask what is missing.
- The AI did not mention case-sensitivity as a question, so the reviewer assumes there is no question.

Automation bias has two forms. An **error of commission** is acting on a wrong suggestion (accepting TC-03). An **error of omission** is failing to notice something because the system did not flag it (never noticing that AC4 has no test). Both are visible in our example.

#### Trap 3: Anchoring

**Anchoring** is the tendency to rely too heavily on the first piece of information you see. Once you have read the AI's draft, you tend to *adjust* it (fix a word, a number) rather than ask whether the whole approach is right. If the AI organised the cases around the discount and forgot the one-coupon rule, a reviewer who starts from that draft is likely to forget it too.

A simple defence against anchoring is to **write down your own expectations before you read the AI output**: which acceptance criteria exist, which boundaries matter, which error messages the requirement specifies. Then compare the AI's draft with *your* list, not the other way round.

#### Calibrated trust

The goal is not to distrust AI completely (re-doing everything by hand throws away the speed benefit). The goal is **calibrated trust**: trusting the AI where it has earned it and checking it where it is weak. Google's People + AI Guidebook describes this as helping users "calibrate their trust" so that they rely on a system in some situations and double-check it in others. In QA terms, AI is usually strong at structure, breadth of ideas and formatting, and usually weak at exact expected results, precise boundaries, exact wording of messages and knowing what the requirement does **not** say. Your review effort should go where the AI is weak.

### 3. Human-in-the-Loop: Roles and Accountability

**Human-in-the-loop (HITL)** means a person reviews and approves AI output **before** it is used. It is one point on a spectrum:

| Pattern | What the human does | Example in QA | When it fits |
|---|---|---|---|
| **Human-in-the-loop** | Reviews and approves every output before use | A tester approves AI test cases before they enter the test management tool | New use, high risk, anything that becomes a test oracle |
| **Human-on-the-loop** | Monitors outputs and can intervene, but does not approve each one | A lead samples AI-written defect summaries each week | Proven, lower-risk uses with good monitoring |
| **Human-out-of-the-loop** | No human review | AI auto-merges its own test changes | Rarely appropriate in QA today |

For anything in this course (test cases, test data, automation code, defect reports) assume **human-in-the-loop**.

Within HITL there are three roles, even if one person sometimes plays two of them:

- **Author (the AI plus the prompter):** the model produced the draft; the tester who wrote the prompt is responsible for asking the right question with the right context.
- **Reviewer:** checks the draft against the checklist and the requirement, corrects or rejects items and records each correction.
- **Approver:** accepts the reviewed result into the project. On a small team the reviewer may also approve; for high-risk work a **second person** approves.

The key principle is **accountability**: *the AI is never the accountable party*. If an AI-generated test lets a pricing defect reach production, "the AI wrote it" is not an acceptable answer; the person who approved the test owns it, exactly as if they had written it by hand. That is why team policies often require AI-assisted artifacts to be **labelled** and to record **who reviewed them**. (The wider ethics and policy side of this, including disclosure, is covered later today in *Responsible Use of AI in QE*.)

### 4. The Human Review Checklist

A checklist turns "have a look at it" into a repeatable process. Pilots and surgeons use checklists because even experts skip steps when they are busy or confident. Checklists also make reviews **comparable** between reviewers and **auditable** later. Here is the nine-point checklist we will use for AI-generated QA artifacts:

| # | Check | Question to ask | Typical AI failure |
|---|---|---|---|
| C1 | **Correct** | Does every expected result match the requirement (the oracle), not just look plausible? | A wrong total at a boundary; a status code the API never returns |
| C2 | **Complete** | Is every acceptance criterion covered, including error paths and boundaries? | Happy paths only; one AC silently skipped |
| C3 | **Grounded** | Is everything traceable to the source? No invented rules, fields or messages? | "Codes are case-insensitive" when the requirement says nothing |
| C4 | **Relevant** | Does each item test something that matters for this story and its risk? | Generic "page loads within 2 seconds" added to every story |
| C5 | **Consistent** | Are terms, IDs, messages and formats consistent with each other and the app? | "Invalid coupon" in one case, "Coupon code not recognised" in another |
| C6 | **Executable** | Could another tester run it as written: preconditions, data, steps, expected? | "Log in as a user" with no user specified; missing expected result |
| C7 | **Traceable** | Does each item point to a real requirement or AC ID? | A reference to AC5 when the story has four ACs |
| C8 | **Safe** | Is it free of real personal data, secrets and confidential details? | A real customer's email in test data; an API key in a script |
| C9 | **Non-duplicated** | Is each item unique, with no near-copies? | Two cases with the same inputs and different titles |

Let's look more closely at the checks that matter most.

#### C1 Correct: verify against the oracle

Recall from Week 3 and Tuesday that a **test oracle** is the source of truth used to decide whether a test passed: the requirement, a specification, the product owner, a reference implementation. The AI is **not** an oracle. For every expected result, ask: *"Where in the requirement does this come from?"* and then **recompute** it yourself. For a numeric rule like AC1, that means doing the arithmetic: 10% off $120.00 is $12.00, so the expected total is $108.00. For a message, it means comparing character by character with the requirement: "Invalid coupon" is not "Coupon code not recognised".

A subtle but critical point: **do not use the application code as the oracle for its own tests**. If you check the AI's expected result by running the app and copying whatever it returns, your test will agree with the app's bugs. The oracle must come from the requirement or from someone who owns the requirement.

#### C2 Complete: look for what is missing

Errors of omission are the hardest to see because there is nothing on the page to look at. Two techniques help:

1. **Walk the source, not the draft.** Go through the requirement one acceptance criterion at a time and find the test(s) for each. If you walk the AI's list instead, you only check what is there.
2. **Use your Week 3 techniques as a lens.** For AC1/AC2, Boundary Value Analysis says you need $49.99, $50.00 and $50.01 (precision $0.01). For AC4, ask what "only one coupon" means as a test: should a second code after SAVE10 be refused, or replace the first? The requirement does not say, which is itself a finding.

#### C3 Grounded: catch invented requirements

When a requirement is silent on something, models often **fill the gap** with a plausible assumption and state it as fact. TC-04, "Lower-case code is accepted", is a classic example. US-205 does not say whether coupon codes are case-sensitive. The AI picked an answer and wrote a test that would enforce it.

The right response is **not** to flip the expected result to the opposite assumption. It is to **turn the assumption into a question** for the product owner and park the test until the answer arrives. Grounding is about honesty: a test should only enforce rules someone actually decided.

#### C6 Executable and C8 Safe

A test case is **executable** when another tester (or a script) could run it **without guessing**: preconditions, concrete data, clear steps and an observable expected result. TC-07 has no expected result, so it cannot pass or fail; it is not a test yet. **Safe** means no real personal data or secrets made it into the output; how to keep them out of prompts in the first place is covered later today in *Responsible Use of AI in QE*.

#### Applying the checklist to other artifact types

The same nine questions work for every kind of AI output you produced today; only the examples change:

| Artifact | What C1 (Correct) means | A C3 (Grounded) red flag | A C6 (Executable) check |
|---|---|---|---|
| Requirements findings | Is each flagged ambiguity really ambiguous? | A "missing requirement" that is actually in another story | Is each question specific enough for the PO to answer? |
| Test cases | Expected results match the AC | Invented rules or messages | Preconditions, data, steps, expected all present |
| Test data | Each value is valid/invalid as labelled | Fields the system does not have | Data loads into the fixture without errors |
| Automation code | Assertions check the right thing | Locators for elements that do not exist | The test actually runs and fails when it should |
| Defect report draft | Steps reproduce the issue | A root cause the AI guessed | A developer could reproduce it from the report |

Keep the checklist short enough that people actually use it; nine items is near the upper limit.

### 5. Worked Review: The US-205 Draft by Hand

Now let's review the draft from section 1 properly, one test case at a time, using the checklist. Compare this with the list you wrote earlier.

First, as a defence against anchoring, write down **your own expectations from the requirement** before looking at the AI's answers:

| Input | Expected (from the requirement) | Source |
|---|---|---|
| $50.00, SAVE10 | $45.00, no message | AC1 (boundary, "or more") |
| $120.00, SAVE10 | $108.00, no message | AC1 |
| $49.99, SAVE10 | $49.99, "Spend $50.00 to use SAVE10" | AC2 (just below the boundary) |
| $60.00, FREESHIP | $60.00, "Coupon code not recognised" | AC3 |
| SAVE10 then a second code | ? (refused or replaced: not specified) | AC4, question for PO |
| save10 (lower case) | ? (case-sensitivity not specified) | Gap, question for PO |

Now the review:

| Test case | Verdict | Failed checks | Reason and evidence |
|---|---|---|---|
| TC-01 | Accept | none | $50.00 is "or more", 10% off gives $45.00 (AC1). |
| TC-02 | Accept | none | $120.00 × 0.9 = $108.00 (AC1). |
| TC-03 | **Edit** | C1, C7 | $49.99 is under $50.00, so AC2 applies: total unchanged at $49.99 **and** the message "Spend $50.00 to use SAVE10". The AI applied the discount (44.99) and traced the case to AC1. Fix the expected result and change the trace to AC2. |
| TC-04 | **Reject** (park) | C3 | Invented requirement: US-205 does not say codes are case-insensitive. Remove the test and send the PO a question: "Should 'save10' be accepted?" |
| TC-05 | **Edit** | C1, C5 | Right idea, wrong wording. AC3 specifies "Coupon code not recognised", not "Invalid coupon". A UI test with the AI's text would fail on correct software. |
| TC-06 | **Reject** | C9 | Same inputs as TC-01 ($50.00, SAVE10) with a slightly different title. Adds no coverage. |
| TC-07 | **Reject** | C3, C6, C7 | Traces to AC5, which does not exist; "removed after logout" is an invented rule; no expected result, so it cannot pass or fail. |
| *(missing)* | **Add** | C2 | No test for AC4 (one coupon per order) and none correctly traced to AC2. Add them, after asking the PO what AC4 should do with a second code. |

Notice a few things about this review:

- **Two of seven cases were fine as written.** AI drafts are useful: the structure, IDs and the two AC1 cases saved real time.
- **The most dangerous error is TC-03.** It looks like a sensible boundary test, and if automated as written it would **pass on a buggy app** that applied the discount below $50.00. That is precisely the "green build hiding a bug" outcome from the start of the lesson.
- **The reviewer produced two questions for the product owner.** Validation does not only fix the AI's output; it often exposes gaps in the requirement itself. That is valuable QA work.
- **Each verdict has evidence** (an AC number or a PO question). "Looks wrong" is not a review comment; "contradicts AC2" is.

### 6. Review Aids: Let Code Point, Let Humans Decide

Doing that review by hand for seven cases is fine. For seventy, you will get tired, and tired reviewers miss things. Simple, deterministic Python checks can **point** you at suspicious items so you spend your attention where it is needed. They are review **aids**: they flag, you decide.

Save this next to `ai_draft.py` (it imports `fake_llm` from it):

```python
# review_aids.py -- small helpers that POINT a human reviewer at suspicious rows.
# They do not approve anything; the reviewer decides.
import json
from ai_draft import fake_llm

ACCEPTANCE_CRITERIA = {
    "AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "AC2": "Subtotals under $50.00 are unchanged and show 'Spend $50.00 to use SAVE10'.",
    "AC3": "Unknown codes show 'Coupon code not recognised'.",
    "AC4": "Only one coupon per order.",
}

def expected_from_requirement(subtotal: float, code: str):
    """Our independent oracle, written by a human straight from AC1-AC3.
    It does NOT call the application code and does NOT reuse the AI's answers."""
    if code != "SAVE10":
        return subtotal, "Coupon code not recognised"          # AC3
    if subtotal >= 50.00:
        return round(subtotal * 0.9, 2), None                 # AC1
    return subtotal, "Spend $50.00 to use SAVE10"             # AC2

def review_flags(draft):
    flags = []
    seen_inputs = {}
    for tc in draft:
        tid = tc["id"]
        # 1. Traceability: does the AC this case claims to test exist?
        if tc["ac"] not in ACCEPTANCE_CRITERIA:
            flags.append((tid, "TRACE", f"refers to {tc['ac']}, which is not in US-205"))
        # 2. Completeness of the case itself: is there an expected result at all?
        if tc["expected_total"] is None and tc["expected_message"] is None:
            flags.append((tid, "NO-EXPECTED", "no expected result"))
            continue
        # 3. Correctness: compare with the requirement-based oracle.
        want_total, want_msg = expected_from_requirement(tc["subtotal"], tc["code"])
        if tc["expected_total"] != want_total or tc["expected_message"] != want_msg:
            flags.append((tid, "MISMATCH",
                          f"AI says ({tc['expected_total']}, {tc['expected_message']!r}); "
                          f"requirement says ({want_total}, {want_msg!r})"))
        # 4. Duplicates: same inputs already seen?
        key = (tc["subtotal"], tc["code"])
        if key in seen_inputs:
            flags.append((tid, "DUPLICATE", f"same inputs as {seen_inputs[key]}"))
        else:
            seen_inputs[key] = tid
    # 5. Coverage: which acceptance criteria have no test case at all?
    covered = {tc["ac"] for tc in draft}
    for ac in ACCEPTANCE_CRITERIA:
        if ac not in covered:
            flags.append(("(suite)", "GAP", f"no test case traces to {ac}"))
    return flags

if __name__ == "__main__":
    draft = json.loads(fake_llm("Generate test cases for US-205 ..."))
    for tid, kind, detail in review_flags(draft):
        print(f"{tid:8} {kind:12} {detail}")
```

How it works, piece by piece:

- **`ACCEPTANCE_CRITERIA`** is a dictionary that maps each AC ID to its text. It gives the script a list of the IDs that really exist, which is all the traceability check needs.
- **`expected_from_requirement`** is our **independent oracle**. A human wrote it by reading AC1-AC3, so it encodes the *requirement*, not the AI's opinion and not the app's behaviour. The `if` order matters: an unknown code is checked first (AC3), then the $50.00 threshold with `>=` because the requirement says "or more" (AC1), and everything else falls through to AC2. It returns a **tuple** `(total, message)`, so the caller can unpack both values in one line.
- **`review_flags`** loops over every test case and collects findings in a list of `(id, kind, detail)` tuples:
  1. `if tc["ac"] not in ACCEPTANCE_CRITERIA` checks traceability (C7).
  2. If both expected fields are `None`, the case has no expected result (C6); `continue` skips the remaining checks for that case, because there is nothing to compare.
  3. The oracle's answer is compared with the AI's answer; any difference is a `MISMATCH` (C1). `!r` in an f-string shows the value with quotes, so you can see exact wording differences.
  4. `seen_inputs` is a dictionary from `(subtotal, code)` to the first test ID that used it. A repeated key means a duplicate (C9).
  5. Finally, a **set comprehension** `{tc["ac"] for tc in draft}` collects the AC IDs that the suite claims to cover; any AC not in that set is a `GAP` (C2).
- The `f"{tid:8} {kind:12} ..."` formatting pads the columns so the output lines up.

Running `python review_aids.py` prints:

```text
TC-03    MISMATCH     AI says (44.99, None); requirement says (49.99, 'Spend $50.00 to use SAVE10')
TC-04    MISMATCH     AI says (72.0, None); requirement says (80.0, 'Coupon code not recognised')
TC-05    MISMATCH     AI says (60.0, 'Invalid coupon'); requirement says (60.0, 'Coupon code not recognised')
TC-06    DUPLICATE    same inputs as TC-01
TC-07    TRACE        refers to AC5, which is not in US-205
TC-07    NO-EXPECTED  no expected result
(suite)  GAP          no test case traces to AC2
(suite)  GAP          no test case traces to AC4
```

The script found every row our manual review found. But look closely at what it **cannot** decide:

- **TC-04 is reported as a plain mismatch.** The script treats `save10` as an unknown code because our oracle compares strings exactly. That is *one* reading of the requirement, but the requirement does not actually say. Only a human can recognise this as an **open question** and send it to the product owner rather than "correcting" the test to the script's assumption.
- **The AC2 gap is partly the AI's mis-trace.** TC-03 actually tests the AC2 boundary; once a human corrects its trace, the AC2 gap disappears. The script cannot know that a case is labelled with the wrong AC.
- **Relevance (C4) and safety (C8) are not checked at all.** Whether a case matters, and whether the data is safe, need judgement and context.
- **The oracle itself could be wrong.** If the human who wrote `expected_from_requirement` had typed `>` instead of `>=`, the script would flag the correct TC-01 as a mismatch. Review aids need reviewing too, which is why we keep them tiny and obvious.

This is the right division of labour: **code is fast and never tired; humans understand meaning and context.** Use both. (Turning checks like these into full, reusable validation scripts for an agent's output is covered on **Friday**.)

### 7. Risk-Based Review Depth

Not everything the AI produces deserves the same amount of review. A suggested rename for a test function and the expected totals for checkout pricing are very different in risk. Spending the same effort on both wastes time on the first and probably under-reviews the second.

You already know **risk-based testing** from Week 3: test effort follows risk, where risk combines **impact** (how bad if it fails) and **likelihood** (how likely it is to fail). We apply the same idea to reviewing AI output, with one extra factor, **reach**: how far will this artifact travel? A single exploratory note reaches one person; a shared fixture or a test that gates the CI pipeline reaches everyone.

```python
# review_depth.py -- decide HOW MUCH human review an AI-generated artifact needs.

def risk_score(impact: int, likelihood_wrong: int, reach: int) -> int:
    """Each factor is rated 1 (low) to 3 (high) by the tester.
    impact           -- how bad is it if this artifact is wrong?
    likelihood_wrong -- how likely is the AI to get it wrong here?
    reach            -- how far will the artifact travel (one test vs. the whole suite/CI)?"""
    for value in (impact, likelihood_wrong, reach):
        if value not in (1, 2, 3):
            raise ValueError("ratings must be 1, 2 or 3")
    return impact * likelihood_wrong * reach          # 1 .. 27

def review_tier(score: int) -> str:
    if score >= 12:
        return "FULL: line-by-line review + second reviewer + run it"
    if score >= 4:
        return "STANDARD: full checklist by one reviewer"
    return "LIGHT: spot-check against the checklist"

artifacts = [
    # name,                                         impact, likelihood, reach
    ("Payment/checkout test cases (US-205)",            3, 2, 3),
    ("Login lockout test cases (US-101 AC3)",           3, 2, 2),
    ("Synthetic shipping addresses (US-310)",           2, 2, 2),
    ("Draft test summary email to the team",            1, 2, 1),
    ("Renaming suggestions for test functions",         1, 1, 1),
]

for name, i, l, r in artifacts:
    s = risk_score(i, l, r)
    print(f"{s:>2}  {name:42} {review_tier(s)}")
```

Explanation:

- Each factor is a small rating, 1 to 3, chosen by the tester. **Multiplying** them (rather than adding) means one low factor pulls the score down a lot, and three high factors push it right up: the range is 1 to 27.
- The `for value in (...)` loop is a **guard clause**: it rejects ratings outside 1-3 so a typo like `33` cannot silently create a huge score.
- `review_tier` maps the score to a review depth. The thresholds (12 and 4) are a team decision, not a law of nature; start with something like this and adjust.
- `f"{s:>2}"` right-aligns the score in two characters so the column lines up.

Output:

```text
18  Payment/checkout test cases (US-205)       FULL: line-by-line review + second reviewer + run it
12  Login lockout test cases (US-101 AC3)      FULL: line-by-line review + second reviewer + run it
 8  Synthetic shipping addresses (US-310)      STANDARD: full checklist by one reviewer
 2  Draft test summary email to the team       LIGHT: spot-check against the checklist
 1  Renaming suggestions for test functions    LIGHT: spot-check against the checklist
```

Why the ratings are what they are:

- **Checkout test cases:** impact 3 (money and customer trust), likelihood 2 (we just saw the AI get a boundary wrong), reach 3 (they gate every release). Full review.
- **Login lockout:** impact 3 (security and lock-outs of real customers), likelihood 2 (counting "5 consecutive failures" and a 15-minute window is easy to get subtly wrong), reach 2. Full review.
- **Synthetic addresses:** impact 2, because a bad ZIP code wastes time rather than hiding a pricing bug, so a standard review is enough.
- **Summary email and renames:** low on everything. A light check is fine; even here, read it before sending.

Two rules sit on top of any score:

1. **Anything that becomes an expected result (an oracle) gets at least a STANDARD review**, however small it looks. Expected results are where wrong AI output turns into green builds that hide bugs.
2. **"LIGHT" never means "none".** Every AI output that leaves your machine has been read by a human.

### 8. Reviewing at Volume: Sampling with Escalation

Suppose the AI produced sixty test cases for the search feature. Reviewing every one at FULL depth may not be realistic. **Sampling** lets you review a fair subset, as long as you do it in a principled way:

1. **Always review every high-risk item.** Sampling is for the rest.
2. **Pick the sample randomly**, not by scrolling and picking the ones that "look interesting". Human picking is biased towards items that look unusual, which are not necessarily the wrong ones.
3. **Make the sample reproducible** with a fixed random seed, so someone else can see exactly which items were checked.
4. **Escalate if the sample is bad.** Decide in advance: "if more than one in ten sampled items needs a correction, review everything".

```python
# sampling.py -- choose which AI-generated test cases a human reviews when there are many.
import random

def choose_for_review(cases, sample_rate=0.2, seed=2026):
    """Always review every high-risk case; review a random sample of the rest.
    A fixed seed makes the sample reproducible, so a second reviewer (or an auditor)
    can see exactly which cases were picked."""
    must = [c for c in cases if c["risk"] == "high"]
    rest = [c for c in cases if c["risk"] != "high"]
    k = max(1, round(len(rest) * sample_rate)) if rest else 0
    rng = random.Random(seed)
    sampled = rng.sample(rest, k)
    return must, sampled

# 60 generated cases: every 6th one touches payment, so it is high risk.
cases = [{"id": f"TC-{n:03}", "risk": "high" if n % 6 == 0 else "normal"}
         for n in range(1, 61)]

must, sampled = choose_for_review(cases)
print("Always reviewed :", len(must), [c["id"] for c in must][:4], "...")
print("Random sample   :", len(sampled), sorted(c["id"] for c in sampled))
print("Total to review :", len(must) + len(sampled), "of", len(cases))
```

Line by line:

- Two **list comprehensions** split the cases into `must` (high risk) and `rest`.
- `k` is the sample size: 20% of the rest, rounded, but at least 1 (`max(1, ...)`) so a small batch is never skipped entirely. The `if rest else 0` handles the case where everything is high risk.
- `random.Random(seed)` creates a **private random number generator** with a fixed seed. Using it (instead of the global `random.sample`) means the same seed always picks the same sample, on any machine, which makes the review auditable. You met seeded randomness on Tuesday when simulating non-determinism.
- `rng.sample(rest, k)` picks `k` **different** items at random (no repeats).
- `f"TC-{n:03}"` pads the number with zeros to three digits (TC-006), and `n % 6 == 0` marks every sixth case as high risk for this demonstration.

Output:

```text
Always reviewed : 10 ['TC-006', 'TC-012', 'TC-018', 'TC-024'] ...
Random sample   : 10 ['TC-008', 'TC-009', 'TC-017', 'TC-025', 'TC-039', 'TC-043', 'TC-046', 'TC-047', 'TC-050', 'TC-057']
Total to review : 20 of 60
```

Twenty reviews instead of sixty. Now apply the **escalation rule**: if, say, two of the ten sampled cases need corrections (20%, above the 10% threshold you set in advance), you stop sampling and review all fifty normal-risk cases. A bad sample is evidence that the batch, or the prompt behind it, has a systematic problem.

Sampling is a tool for **mature, proven** prompts with a good track record (see the metrics in section 10). For a new prompt, or for anything at FULL depth, review everything.

### 9. Recording Corrections: The Correction Log

A review that leaves no trace cannot be audited, cannot be learned from and cannot be measured. The **correction log** is the record of every human decision about AI output. Today's exercise asks you to produce one for your Project 2 test cases and data.

A useful entry records **which item**, the **decision** (accepted, edited, rejected), the **category** of problem, **what the AI said**, **what you changed it to**, the **evidence** (an AC, a spec section or a PO answer) and **who** decided.

The **category** is what makes the log useful later. Use a small, fixed list so entries can be counted. A good starting set for test cases:

- **WRONG_EXPECTED**: the expected result contradicts the requirement.
- **INVENTED_REQUIREMENT**: the item enforces a rule nobody specified.
- **WRONG_TRACE**: linked to the wrong or a non-existent requirement.
- **DUPLICATE**: adds no new coverage.
- **MISSING_INFO**: preconditions, data or expected result missing.
- **WRONG_WORDING**: right idea, wrong message text or terminology.

Here is the log for our review, built with a Python **dataclass** and written to CSV so it can be opened in a spreadsheet or imported into a test management tool:

```python
# correction_log.py -- record every human decision about an AI-generated test case.
import csv
from collections import Counter
from dataclasses import dataclass, asdict, fields

DECISIONS = {"ACCEPTED", "EDITED", "REJECTED"}
CATEGORIES = {"", "WRONG_EXPECTED", "INVENTED_REQUIREMENT", "WRONG_TRACE",
              "DUPLICATE", "MISSING_INFO", "WRONG_WORDING"}

@dataclass
class Correction:
    item_id: str        # which AI output item
    decision: str       # ACCEPTED / EDITED / REJECTED
    category: str       # why it was changed ("" if accepted as-is)
    ai_said: str        # what the AI produced
    fixed_to: str       # what the human changed it to
    source: str         # the evidence: AC, PO answer, spec section
    reviewer: str

    def __post_init__(self):
        if self.decision not in DECISIONS:
            raise ValueError(f"bad decision: {self.decision}")
        if self.category not in CATEGORIES:
            raise ValueError(f"bad category: {self.category}")
        if self.decision != "ACCEPTED" and not self.category:
            raise ValueError(f"{self.item_id}: an edit or rejection needs a category")

log = [
    Correction("TC-01", "ACCEPTED", "", "50.00 -> 45.00", "", "AC1", "a.tester"),
    Correction("TC-02", "ACCEPTED", "", "120.00 -> 108.00", "", "AC1", "a.tester"),
    Correction("TC-03", "EDITED", "WRONG_EXPECTED", "49.99 -> 44.99, AC1",
               "49.99 -> 49.99 + 'Spend $50.00 to use SAVE10', AC2", "AC2", "a.tester"),
    Correction("TC-04", "REJECTED", "INVENTED_REQUIREMENT", "save10 accepted",
               "removed; question Q-1 sent to PO about case-sensitivity", "AC3", "a.tester"),
    Correction("TC-05", "EDITED", "WRONG_WORDING", "'Invalid coupon'",
               "'Coupon code not recognised'", "AC3", "a.tester"),
    Correction("TC-06", "REJECTED", "DUPLICATE", "same as TC-01", "removed", "-", "a.tester"),
    Correction("TC-07", "REJECTED", "WRONG_TRACE", "traces to AC5, no expected result",
               "removed; AC5 does not exist", "US-205", "a.tester"),
]

with open("correction_log.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[fl.name for fl in fields(Correction)])
    writer.writeheader()
    for entry in log:
        writer.writerow(asdict(entry))

# --- metrics -------------------------------------------------------------
total = len(log)
decisions = Counter(e.decision for e in log)
categories = Counter(e.category for e in log if e.category)

print(f"Items reviewed : {total}")
for d in ("ACCEPTED", "EDITED", "REJECTED"):
    print(f"{d:<15}: {decisions[d]}  ({decisions[d] / total:.0%})")
print("Usable as-is   :", f"{decisions['ACCEPTED'] / total:.0%}")
print("Usable at all  :", f"{(decisions['ACCEPTED'] + decisions['EDITED']) / total:.0%}")
print("Top problems   :", categories.most_common(3))
```

What the new pieces of Python do:

- **`@dataclass`** generates `__init__`, a readable `__repr__` and equality from the typed fields you list. Each `Correction(...)` call creates one log entry.
- **`__post_init__`** runs right after the generated `__init__`. We use it to **validate** each entry: the decision and category must come from the allowed sets, and an EDITED or REJECTED entry *must* have a category. A log that accepts "rejected, no reason" quickly becomes useless.
- **`fields(Correction)`** lists the dataclass's fields, so the CSV header always matches the class, and **`asdict(entry)`** turns an entry into a dictionary that `csv.DictWriter` can write as one row.
- `newline=""` is what the `csv` module expects (it avoids blank lines between rows on Windows); `encoding="utf-8"` keeps non-ASCII characters safe.
- **`Counter`** counts how often each value appears. `categories.most_common(3)` returns the three most frequent categories as `(name, count)` pairs.
- `{... :.0%}` formats a fraction as a whole-number percentage (0.2857 becomes 29%).

The CSV file starts like this:

```csv
item_id,decision,category,ai_said,fixed_to,source,reviewer
TC-01,ACCEPTED,,50.00 -> 45.00,,AC1,a.tester
TC-02,ACCEPTED,,120.00 -> 108.00,,AC1,a.tester
TC-03,EDITED,WRONG_EXPECTED,"49.99 -> 44.99, AC1","49.99 -> 49.99 + 'Spend $50.00 to use SAVE10', AC2",AC2,a.tester
```

Notice that the `csv` module put quotes around values containing commas automatically. And if you try to record an edit without a category, the dataclass refuses:

```python
Correction("TC-08", "EDITED", "", "x", "y", "AC1", "a.tester")
# ValueError: TC-08: an edit or rejection needs a category
```

Two more entries belong in a complete log, even though the AI did not produce them: the **cases you added** to fill the AC2 and AC4 gaps, and the **questions you sent** to the product owner (Q-1 about case-sensitivity, Q-2 about what a second coupon should do). Many teams keep these in the same file with a decision value such as ADDED, or in a short "open questions" list next to it. Either way, the gaps the AI missed are part of the story of the review.

### 10. Review Metrics: Learning from Your Corrections

Running `correction_log.py` also prints a small metrics report:

```text
Items reviewed : 7
ACCEPTED       : 2  (29%)
EDITED         : 2  (29%)
REJECTED       : 3  (43%)
Usable as-is   : 29%
Usable at all  : 57%
Top problems   : [('WRONG_EXPECTED', 1), ('INVENTED_REQUIREMENT', 1), ('WRONG_WORDING', 1)]
```

What these numbers mean:

- **Acceptance rate** (usable as-is): the share of AI items accepted without change. Here 29%.
- **Edit rate**: the share that needed a correction but were worth keeping. Here 29%.
- **Rejection rate**: the share thrown away. Here 43%.
- **Usable at all** (accepted + edited): 57%. This is a rough measure of how much the AI actually contributed.
- **Top problems**: which categories occur most often. With only seven items every category appears once; over a sprint of reviews, a clear pattern usually emerges.

They are useful in three ways:

1. **They improve your prompts.** If WRONG_WORDING dominates, your prompt probably did not include the exact messages from the requirement; add them inside delimiters (Tuesday). If INVENTED_REQUIREMENT dominates, add an explicit rule such as "If the requirement does not specify something, list it under `open_questions` instead of writing a test for it". If DUPLICATE dominates, ask for distinct inputs and a coverage table first. The correction log is a **feedback loop** from review back to prompt engineering.
2. **They tell you how much to trust a prompt.** A prompt that has run for three sprints with a 90% acceptance rate and no WRONG_EXPECTED corrections is a candidate for sampling (section 8). A prompt at 29% is not.
3. **They make the value of AI honest.** If only 20% of output is usable after review, AI may cost more time than it saves for that task; that is a legitimate finding to report.

Be careful with one thing: **a high acceptance rate is only meaningful if the review is real.** If reviewers rubber-stamp, the acceptance rate goes up while quality goes down. That is why we pair the metrics with a per-item checklist record and, for high-risk work, a second reviewer. Some teams also track **escaped defects**: bugs found later that a reviewed AI test should have caught. One escaped defect traced to an accepted AI test is a strong signal to tighten the review for that area.

### 11. Sign-Off: From Reviewed Draft to Approved Suite

The last step is **sign-off**: an explicit decision that an artifact is approved for use. In practice, AI-assisted QA artifacts move through a small set of states:

```text
AI-DRAFT  -->  IN-REVIEW  -->  NEEDS-CHANGES  -->  IN-REVIEW  -->  APPROVED
                                                                \
                                                                 -->  REJECTED
```

- **AI-DRAFT**: produced by the AI, labelled as such, not yet trusted.
- **IN-REVIEW**: a reviewer is applying the checklist.
- **NEEDS-CHANGES**: at least one check failed; it goes back for correction (by hand or with a better prompt).
- **APPROVED**: passed review; a named person signed off; it may enter the suite.
- **REJECTED**: removed, with a reason in the correction log.

Each move to APPROVED should leave a **review record**: the item ID, the answer to each of C1-C9 (yes, no or n/a, with no question skipped) and the reviewer's name. In a real team this lives in your test management tool (a review workflow state or custom field) or in a pull request template with one checkbox per checklist item. The tool does not matter; what matters is that the review leaves a trace.

A good habit is to make the approved status part of what the test suite actually runs, so an unreviewed AI draft **cannot** slip into the regression suite by accident. Here is a small pytest example. It uses the same `cart.py` / `apply_coupon` function from Monday and Tuesday (save it next to this test):

```python
# test_reviewed_coupon.py -- only rows a human has approved make it into the suite.
import pytest
from cart import apply_coupon

# (id, total, expected total, review status) -- the status comes from the review record
ALL_ROWS = [
    ("TC-01", 50.00, 45.00, "APPROVED"),
    ("TC-02", 120.00, 108.00, "APPROVED"),
    ("TC-03", 49.99, 49.99, "APPROVED"),   # corrected by the reviewer (AI said 44.99)
    ("TC-06", 50.00, 45.00, "REJECTED"),   # duplicate of TC-01
]
APPROVED = [row[:3] for row in ALL_ROWS if row[3] == "APPROVED"]

@pytest.mark.parametrize("tc_id,total,expected", APPROVED, ids=[r[0] for r in APPROVED])
def test_save10_totals(tc_id, total, expected):
    assert apply_coupon(total, "SAVE10") == expected

def test_tc05_unknown_code_is_rejected():
    with pytest.raises(ValueError):
        apply_coupon(60.00, "FREESHIP")
```

- `ALL_ROWS` keeps the review status next to each row; `APPROVED` is a list comprehension that keeps only approved rows and slices each tuple with `row[:3]` to drop the status column.
- `@pytest.mark.parametrize` (Week 4) runs the test once per approved row; `ids=[...]` names each run after its test case ID, so reports trace straight back to the review.
- `pytest.raises(ValueError)` asserts that an unknown code raises an error at the function level (the UI message from AC3 would be checked in a UI test).

Running `pytest -v test_reviewed_coupon.py`:

```text
test_reviewed_coupon.py::test_save10_totals[TC-01] PASSED                [ 25%]
test_reviewed_coupon.py::test_save10_totals[TC-02] PASSED                [ 50%]
test_reviewed_coupon.py::test_save10_totals[TC-03] PASSED                [ 75%]
test_reviewed_coupon.py::test_tc05_unknown_code_is_rejected PASSED       [100%]
============================== 4 passed in 0.07s ===============================
```

Notice that TC-03 passes with the **corrected** expected result, 49.99. Had we kept the AI's 44.99, this test would have failed against correct code. Running the tests is part of review for executable artifacts (check C6), but remember the lesson of section 4: **a passing test is not proof the expected result is right**; it only proves the code and the test agree. The requirement is still the oracle. (Your exact timing, `0.07s`, will differ.)

### 12. Review Anti-Patterns to Avoid

Even with a checklist, reviews go wrong in predictable ways. Watch for these in yourself and your team:

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| **Rubber-stamping** | "LGTM" on 50 test cases in two minutes | Require a checklist record per item; spot-check reviewers' work |
| **Format-only review** | Fixing typos and IDs, never recomputing expected results | Start every review with C1 (correct) and C2 (complete) |
| **Reviewing the draft, not the requirement** | Only checking what is on the page | Walk the requirement AC by AC (anchoring defence) |
| **"The AI said so" as evidence** | `source` column says "AI" | Evidence must be a requirement, spec or PO answer |
| **Fixing by flipping** | Changing an invented rule to the opposite invented rule | Turn the gap into a PO question; park the test |
| **Using the app as the oracle** | Copying actual results into expected results | Derive expected results from the requirement |
| **AI reviewing AI, with no human** | Asking a second chatbot "is this correct?" and accepting the answer | A second model can be a helpful extra opinion, but a human still signs off. Systematic model-graded evaluation (LLM-as-judge) is covered in Week 10. |
| **Review fatigue** | Quality of review drops after the first 20 items | Smaller batches, breaks, sampling with escalation, risk-based depth |
| **Silent correction** | Fixing things without logging them | Every edit or rejection goes in the correction log |

### 13. Putting It Together: A Review Workflow

Here is the whole process in one place. You will follow it in today's exercise.

1. **Before reading the AI output**, list the requirement's ACs, key boundaries and exact messages (anchoring defence).
2. **Rate the risk** (impact, likelihood, reach) and choose the review depth: LIGHT, STANDARD or FULL.
3. **Run your review aids** (traceability, oracle comparison, duplicates, AC coverage) to get a list of suspicious items.
4. **Apply the checklist** to every item (or to every high-risk item plus a seeded random sample, with an escalation rule).
5. **Decide** for each item: accept, edit or reject. Never "fix by flipping"; turn gaps into PO questions.
6. **Log** every decision with category, before/after and evidence. Add the cases you created for gaps and the questions you raised.
7. **Run** any executable artifacts (tests, data loaders, scripts) and confirm they behave as expected.
8. **Sign off**: a named person marks the items APPROVED; for FULL-depth work, a second person approves.
9. **Feed back**: read your metrics and update the prompt so the next batch has fewer of your top correction categories.

### 14. Connecting to Project 2

In today's exercise you generate AI test cases and data for the Project 2 e-commerce app and document your corrections. Apply this lesson directly: use the checklist on every item for US-101, US-205 and US-310; treat login lockout and checkout pricing as **FULL** review; keep a `correction_log.csv` (section 9 fields) next to the reviewed test cases; mark AI-assisted artifacts with a status and keep only APPROVED rows in the suite that runs in CI; and finish with two or three sentences on your metrics and the prompt change they suggest. When you build a QA agent on Thursday and Friday, its output will need the same reviewer, log and feedback loop; how parts of that checking become automated is covered on **Friday**.

---

## Practice Exercises

1. **Manual review.** Using the checklist, review this illustrative AI draft for **US-101 Login** (AC1: valid credentials go to "My Account"; AC2: wrong password shows "Invalid email or password", same message for unknown email; AC3: after 5 consecutive failed attempts the account is locked for 15 minutes). For each case give a verdict, failed checks and evidence.
   - TC-L1: valid email and password → "My Account" page (AC1)
   - TC-L2: wrong password → "Incorrect password" (AC2)
   - TC-L3: unknown email → "No account found for this email" (AC2)
   - TC-L4: 3 failed attempts → account locked (AC3)
   - TC-L5: 5 failed attempts, then wait 15 minutes → can log in again (AC3)
   - TC-L6: password field masks characters (AC4)
2. **Find the gaps.** What important test is missing from the US-101 draft? (Hint: what happens on the 4th failed attempt, and what does "consecutive" mean after a successful login?) Write the missing cases and at least one question for the product owner.
3. **Extend the review aid.** Adapt `review_flags` for US-101 so it checks that every expected message is exactly one of the messages in the acceptance criteria. Which of TC-L1 to TC-L6 does it flag?
4. **Rate the risk.** Use `risk_score` to rate (a) AI-generated search test cases, (b) AI-generated passwords for test accounts, (c) an AI-written README for your test framework. Justify each rating in one sentence.
5. **Correction log and metrics.** Record your US-101 review from exercise 1 as `Correction` entries, write the CSV and print the metrics. Based on the top category, write one sentence you would add to the prompt.

---

## Knowledge Check

1. What is the difference between **fluency** and **correctness**, and why does the difference matter when reviewing AI output?
2. Define **automation bias** and give one example of an error of commission and one of an error of omission in AI-assisted testing.
3. Who is accountable for an AI-generated test case that lets a defect reach production?
4. An AI test case says "Coupon codes are case-insensitive" but the requirement is silent. Which checklist item fails, and what should the reviewer do?
5. Why should you **not** use the application's actual output as the oracle when checking AI expected results?
6. In `review_aids.py`, why is TC-04 reported as a `MISMATCH`, and why does a human still need to interpret that flag?
7. Name the three factors in the risk-based review score and explain why "reach" matters.
8. What does a high acceptance rate tell you, and what must also be true for it to be meaningful?

<details>
<summary>Answers</summary>

1. Fluency is how well the text reads (structure, grammar, confident tone); correctness is whether it matches the requirement and the real behaviour. LLMs are very good at fluency, and humans tend to treat fluent text as trustworthy, so wrong AI output can look as professional as right output. Only checking against the oracle reveals the difference.
2. Automation bias is the tendency to favour an automated system's suggestions and under-check them. Commission: copying the AI's expected total of 44.99 for a $49.99 order into a test. Omission: not noticing that no test covers AC4 because the AI did not mention it.
3. The person who approved it (and the team whose process accepted it). The AI is never the accountable party.
4. C3 (Grounded) fails: it is an invented requirement. The reviewer should not flip the rule to the opposite assumption; they should remove or park the test, log it as INVENTED_REQUIREMENT and send a question to the product owner.
5. Because the test would then agree with any defect in the application. A test whose expected result came from the code cannot detect that the code is wrong. The oracle must come from the requirement or its owner.
6. The oracle compares codes exactly, so `save10` is treated as an unknown code and the expected result differs from the AI's. But the requirement does not say whether codes are case-sensitive, so the script's reading is only one interpretation. A human must recognise this as an open question, not a simple correction.
7. Impact (how bad if wrong), likelihood the AI is wrong, and reach (how far the artifact travels). Reach matters because a wrong shared fixture or CI-gating test affects many tests and people, while a wrong personal note affects one.
8. It suggests the prompt produces output that reviewers accept without change, which may justify lighter review or sampling. It is only meaningful if the reviews are real (checklist records, second reviewers for high risk, few escaped defects); otherwise it may just measure rubber-stamping.

</details>

---

## Glossary

- **Human-in-the-loop (HITL):** A workflow in which a person reviews and approves AI output before it is used.
- **Automation bias:** The tendency to favour an automated system's output and under-check it; errors of commission (acting on a wrong suggestion) and omission (missing what was not flagged).
- **Anchoring:** Relying too heavily on the first information seen, such as an AI draft, and only adjusting it.
- **Calibrated trust:** Trusting an AI system where it is reliable and checking it where it is weak.
- **Invented requirement:** A rule in AI output that the source requirement does not specify.
- **Review aid:** A small deterministic script that flags suspicious items for a human reviewer without making the final decision.
- **Risk-based review depth:** Choosing LIGHT, STANDARD or FULL review based on impact, likelihood of error and reach.
- **Sampling with escalation:** Reviewing all high-risk items plus a random sample of the rest, and reviewing everything if the sample's correction rate exceeds a threshold.
- **Correction log:** A record of each review decision with category, before/after values, evidence and reviewer.
- **Acceptance / edit / rejection rate:** The shares of AI items accepted unchanged, corrected, or discarded during review.
- **Sign-off:** An explicit, recorded approval by a named person that an artifact is fit for use.

---

## Summary

- AI drafts are **fluent but not guaranteed correct**. A wrong AI test can fail on correct software or, worse, pass on broken software.
- Three human traps make quick reviews unreliable: **fluency**, **automation bias** and **anchoring**. Aim for **calibrated trust**, and write your own expectations before reading AI output.
- Use **human-in-the-loop** for QA artifacts. The AI is never accountable; the person who approves is.
- Review every item against the nine-point checklist: **correct, complete, grounded, relevant, consistent, executable, traceable, safe, non-duplicated**. Derive expected results from the **requirement**, never from the app.
- Small Python **review aids** (oracle comparison, traceability, duplicates, coverage) point you at problems quickly; humans interpret them, especially for gaps and open questions.
- Match review effort to **risk** (impact, likelihood, reach), and at volume use **seeded random sampling with an escalation rule**.
- Record every decision in a **correction log** and use the **metrics** to improve your prompts. Only **APPROVED** items enter the suite.
- Automated schema-based validation of agent output follows on **Friday**; hallucination taxonomy and LLM-as-judge follow in **Week 10**.

---

## Additional Resources

- Microsoft Research, *Overreliance on AI: Literature Review* (Passi and Vorvoreanu; how and why people accept wrong AI output, and how to reduce it): https://www.microsoft.com/en-us/research/publication/overreliance-on-ai-literature-review/
- Google PAIR, *People + AI Guidebook: Explainability + Trust* (practical guidance on calibrating trust in AI systems): https://pair.withgoogle.com/chapter/explainability-trust/
- ISTQB, *Certified Tester Testing with Generative AI (CT-GenAI)* (syllabus v1.1 download; covers GenAI across the test process, including risks such as hallucinations and the need for human oversight): https://istqb.org/certifications/gen-ai/
