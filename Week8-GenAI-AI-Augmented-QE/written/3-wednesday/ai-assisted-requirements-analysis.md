# AI-Assisted Requirements Analysis

## Learning Objectives

By the end of this lesson you will be able to:

- **Define** a testable requirement, and recognise common requirement defects: vague words, missing values, missing behaviour and weak obligations.
- **Run** a simple, deterministic weak-word check, by hand and with a short script.
- **Write** an AI review prompt that finds untestable requirements and asks questions without inventing answers.
- **Compare** the word check with the AI review, and explain what each can and cannot find.
- **Turn** every problem into a clear question for the business analyst (BA), instead of an assumption.

---

## Why This Matters

In *AI within the QA Lifecycle* you saw that the cheapest place to catch a mistake is **requirements analysis**: nothing has been built on it yet. This lesson is about doing that phase well, with AI's help.

Requirements problems are some of the most expensive defects a team can have, because everything downstream inherits them. A requirement that says "the page should load fast" cannot be tested as written: one tester passes it at 4 seconds, another fails it at 2. A requirement that says "only one coupon per order" sounds complete, but nobody knows what the shopper should **see** when they try a second coupon, so the developer guesses, the tester guesses, and they guess differently.

Agile teams have long used the **INVEST** checklist to judge user stories, which Bill Wake introduced in a 2003 article ([Agile Alliance](https://agilealliance.org/glossary/invest)). The "T" stands for **Testable**: the story must give enough information to make writing a test possible. Requirements analysis is where testers make sure that is true.

AI is genuinely useful here. It can read a batch of stories in seconds and point out vague words, gaps and contradictions. But it has a dangerous habit: when it finds a gap, it likes to **fill** it. "Locked after several failed logins" becomes "locked after 5 failed logins" in the AI's review, stated as fact. This lesson teaches a routine that gets the benefit without the habit: **word check first, AI review second, human decision last.**

> **Using this with the handout:** this lesson goes deeper into **Handout 05, Topic 2**. It uses the same five requirements from US-205 and US-310, the same weak-word list, the same review prompt and the same `word_check.py`.

---

## The Concept

### 1. What Is Requirements Analysis?

**Requirements analysis** is checking that requirements are **clear, complete and testable** before anyone designs tests.

A requirement is **testable** when you can write a test with a clear **pass/fail** result. Compare:

| Not testable | Testable |
|---|---|
| The page loads fast | The page loads in under 2 seconds on the test network |
| Error messages must be user-friendly | Error messages name the field and say how to fix it |
| The account may be locked after several failed logins | The account is locked after 5 failed logins in a row |

The testable versions contain something a test can **measure** or **compare**: a number, an exact message, a precise condition. But notice: the values in the right-hand column (2 seconds, 5 failed logins) have to come from somewhere. A tester cannot simply choose them. They are business decisions, and the people who make them are the **business analyst (BA)** and the **product owner**.

That is the most important idea in this lesson. **AI suggests; the BA and product owner decide** what the requirement really means. A tester's job in requirements analysis is to **find** the problems and **ask** the right questions, not to answer them.

### 2. Common Requirement Defects

The handout names four common defects. Each one blocks a clear pass/fail test in a different way:

| Defect | Example | Why it is a problem |
|---|---|---|
| **Vague word** | "should load **fast**" | No pass/fail value |
| **Missing value** | "locked after **several** failed logins" | How many? 3? 5? |
| **Missing behaviour** | "Only one coupon per order" | What does the user **see** if they try a second one? |
| **Weak obligation** | "**may** be locked" | Is locking required, or optional? |

Two more defects are worth knowing, because AI is often good at finding them:

| Defect | Example (illustrative) | Why it is a problem |
|---|---|---|
| **Contradiction** | AC1 says "subtotal"; a new AC5 says "the discount applies to the total including shipping" | Which amount is the 10% taken from? |
| **Unanswered situation** | Nothing says what happens if the cart drops below $50.00 **after** SAVE10 is applied | Is the discount removed? Is a message shown? |

The last two are about **meaning**: you cannot find them by looking for particular words. Keep that in mind; it explains why the routine below uses two different checks.

### 3. Deterministic First, AI Second

There are two ways to check a requirement for problems:

| | Word check | AI review |
|---|---|---|
| How it works | Looks for words on a fixed list | Reads the meaning |
| Same input, same result? | **Yes, always** (deterministic) | Not always |
| Can it invent a problem? | Never | Yes |
| Can it find missing behaviour? | No | Often |
| Speed | Milliseconds | Seconds |

A check is **deterministic** when the same input always gives the same output. The word check is deterministic and never invents anything, but it only finds **words**. The AI review finds much more, but it can also be wrong, and may give a different answer tomorrow.

So use **both**, in that order. The word check gives you a reliable baseline in seconds. The AI review then looks deeper. And you, the human, decide what to do with the findings of both.

### 4. Worked Example: Find Untestable Requirements

**Goal:** find the untestable requirements in two stories, US-205 (the coupon) and a new one, **US-310** (checkout performance and login).

```text
US-205 AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
US-205 AC4: Only one coupon per order.
US-310 AC1: The checkout page should load fast.
US-310 AC2: Error messages must be user-friendly.
US-310 AC3: The account may be locked after several failed logins.
```

#### Step 1: The weak-word check, by hand

Here is the handout's list of words that **usually** signal a vague or unmeasurable requirement:

```text
fast, quickly, user-friendly, easy, several, some, may, should, appropriate, etc
```

Go through the five requirements and circle every weak word. Do it on paper before reading on, then compare with the answer:

| Requirement | Weak words found |
|---|---|
| US-205 AC1 | none |
| US-205 AC4 | **none**, but keep reading |
| US-310 AC1 | fast, should |
| US-310 AC2 | user-friendly |
| US-310 AC3 | several, may |

Three of the five requirements contain weak words. US-205 AC1 is clean and testable: it has an exact value ($50.00), an exact rule (10%) and an exact boundary ("or more").

#### Step 2: Ask the AI for a deeper review

A word list only finds words. Now ask the AI to look at **meaning**. Paste this into a new chat:

```text
You are a QA engineer reviewing requirements before test design.
For each requirement below, say whether it is testable as written.
If not, explain why in one sentence and write ONE question for the business analyst.
Do not suggest answers to your own questions.

### Requirements
US-205 AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
US-205 AC4: Only one coupon per order.
US-310 AC1: The checkout page should load fast.
US-310 AC2: Error messages must be user-friendly.
US-310 AC3: The account may be locked after several failed logins.
### End

Reply as a table: ID | Testable? | Why not | Question for the BA
```

Every part of this prompt uses a technique from Tuesday:

| Part | Technique | Why it is there |
|---|---|---|
| "You are a QA engineer..." | Role | Sets the point of view |
| "say whether it is testable", "ONE question" | Precise task | One finding, one question per requirement |
| `### Requirements` ... `### End` | Delimiters | The requirements are clearly separated from the instructions |
| "Do not suggest answers to your own questions" | Constraint | Stops the AI quietly inventing missing values |
| "Reply as a table: ..." | Format lock | Easy to compare with your word check |

The fourth row is the one that matters most. Without it, an AI will often write questions like *"Should the account lock after 5 attempts, as is standard?"*, which is an answer disguised as a question.

#### Step 3: Compare the two checks

A typical AI reply, from the handout, looks **something like** this:

```text
| ID         | Testable? | Why not                                     | Question for the BA                                  |
|------------|-----------|---------------------------------------------|------------------------------------------------------|
| US-205 AC1 | Yes       | -                                           | -                                                    |
| US-205 AC4 | Partly    | Doesn't say what happens on a second coupon | What message is shown when a second coupon is used?  |
| US-310 AC1 | No        | "fast" has no measurable value               | What is the maximum load time, in seconds?            |
| US-310 AC2 | No        | "user-friendly" can't be measured            | What makes an error message acceptable?               |
| US-310 AC3 | No        | "may" and "several" are unclear              | Is locking required, and after how many failures?     |
```

Now put the two checks side by side:

| Requirement | Word check flagged it? | AI flagged it? | Who is right? |
|---|---|---|---|
| US-205 AC1 | No | No (testable) | Both |
| US-205 AC4 | **No** | **Yes (partly)** | **The AI** |
| US-310 AC1 | Yes | Yes | Both |
| US-310 AC2 | Yes | Yes | Both |
| US-310 AC3 | Yes | Yes | Both |

The key row is **US-205 AC4**. "Only one coupon per order." has **no** weak words, so the word check passes it. But it does not say what the user **sees** when they try a second coupon. That is a **missing behaviour**, a meaning problem that no word list can find. The AI found it.

So the AI review is better? On this run, yes. But remember the earlier table: the AI is not deterministic and can invent problems. The word check found three problems **for certain**, in milliseconds, and will find them again tomorrow. The AI found one more, **this time**. You need both.

#### Step 4: See the word check automated

Teams often turn Step 1 into a tiny script that runs on every new story. Save this as `word_check.py` and run `python word_check.py`. You do not need to understand every line:

```python
import re

REQUIREMENTS = {
    "US-205 AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "US-205 AC4": "Only one coupon per order.",
    "US-310 AC1": "The checkout page should load fast.",
    "US-310 AC2": "Error messages must be user-friendly.",
    "US-310 AC3": "The account may be locked after several failed logins.",
}
WEAK_WORDS = ["fast", "quickly", "user-friendly", "easy", "several", "some",
              "may", "should", "appropriate", "etc"]

for req_id, text in REQUIREMENTS.items():
    words = re.findall(r"[a-z\-]+", text.lower())          # split into lowercase words
    hits = [w for w in WEAK_WORDS if w in words]
    if hits:
        print(f"{req_id}: {hits}")
```

It prints:

```text
US-310 AC1: ['fast', 'should']
US-310 AC2: ['user-friendly']
US-310 AC3: ['several', 'may']
```

**What this code does:**

- `text.lower()` makes everything lower case, so "Fast" and "fast" match.
- `re.findall(r"[a-z\-]+", ...)` splits the text into **words** made of letters and hyphens. The hyphen is why `user-friendly` stays one word. Digits and symbols are dropped, so "SAVE10" becomes the word `save` and "$50.00" disappears. That is fine for this check, which only cares about weak words.
- Checking `w in words` (a list of whole words) rather than `w in text` (a string) avoids false matches inside longer words. For example, "**may**" appears inside "dis**may**", and "**some**" inside "hand**some**".

It gives the same result as your hand check, every time.

### 5. The Limits of a Word List

A word list is useful precisely because it is simple. That also defines its limits. The handout's Your Turn exercises show both kinds of limit; here are the results of running them through the same script:

```text
EX-1: ['quickly', 'appropriate']     "Search results appear quickly in an appropriate order."
EX-2: []                             "The page loads in good time."
EX-3: ['may']                        "Users may not apply an expired coupon."
```

- **EX-1 works.** Both weak words are found.
- **EX-2 is a miss.** "In good time" is just as vague as "fast", but none of its words is on the list. You could add "good" to the list, but then "good" would be flagged everywhere, including in perfectly clear sentences. Vague **phrases** are hard to catch with single words. This is a **false negative**: a real problem the check did not report.
- **EX-3 is a false alarm.** "May not apply" is a clear **prohibition**: users are not allowed to apply an expired coupon. The word "may" is on the list because "may be locked" is weak, but here the same word is part of a strong rule. This is a **false positive**: a report of a problem that is not there.

Both are reasons a human reads every finding. A word check is a **pointer**, not a judge.

### 6. Reading the AI's Review Critically

The AI's review needs checking too. The handout gives three things to mark:

- ✅ **AC4 flagged as incomplete.** That is the one the word check missed.
- ✅ **Questions, not invented answers.** For example, it must **not** state "lock after 5 attempts" as fact.
- ✅ **US-205 AC1 marked testable.** An AI that flags everything as untestable is being over-cautious, not thorough.

The second point can be partly automated. A question for the BA should not normally contain a specific number: if it does, the AI may have **answered its own question**. This short check, `answers_check.py`, looks for numbers in the AI's questions:

```python
import re

ai_questions = {                    # the "Question for the BA" column of the AI's reply
    "US-205 AC4": "What message is shown when a second coupon is used?",
    "US-310 AC1": "What is the maximum load time, in seconds?",
    "US-310 AC2": "What makes an error message acceptable?",
    "US-310 AC3": "Should the account lock after 5 failed attempts, as is standard?",
}

for req_id, question in ai_questions.items():
    numbers = re.findall(r"\d+", question)
    if numbers:
        print(f"{req_id}: question contains {numbers} - did the AI answer its own question?")
```

Here the AC3 question has been changed to the kind of reply an AI gives when the ban in the prompt is missing or ignored, **illustrative**. The script prints:

```text
US-310 AC3: question contains ['5'] - did the AI answer its own question?
```

`\d+` means "one or more digits", so the check catches any number. It is a pointer again: a question such as "Does this apply to the 2 regions we launch in?" might contain a number for a good reason. But a flagged question is worth reading twice. "Should the account lock after 5 failed attempts, **as is standard**?" quietly suggests both the value and a reason to accept it. If that reached the BA, they might simply say yes, and an AI's guess would become the requirement.

### 7. Asking the AI What the Story Does Not Cover

The Step 2 prompt reviews the requirements one at a time. A second, broader question often finds more: **what situations does the story not cover at all?** These are the **unanswered situations** from section 2, and AI is often good at listing them because it has seen many similar features.

```text
You are a QA engineer. Read the user story below and list situations a shopper
could be in that the acceptance criteria do NOT say anything about.
List situations only. Do not say what should happen in them.

### User story
US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.
### End
```

A typical reply, **illustrative**:

```text
1. The shopper removes items after applying SAVE10, so the subtotal drops below $50.00.
2. The shopper tries a second coupon (AC4 says one only, but not what is shown).
3. The shopper types the code with spaces before or after it.
4. The shopper types the code in lower case.
5. The order is in a currency other than US dollars.
6. SAVE10 has an expiry date.
```

Now **triage** the list. Not every item is a gap the BA must answer:

| Item | Real gap? | Note |
|---|---|---|
| 1. Subtotal drops after applying | **Yes** | A shopper can easily do this. Ask the BA. |
| 2. Second coupon | **Yes** | Same finding as Step 3; good to see it confirmed |
| 3. Spaces around the code | **Yes** | Common on mobile keyboards. Ask whether they are ignored |
| 4. Lower case | **Yes, as a question** | The story only mentions SAVE10. Ask; never assume it works |
| 5. Other currencies | **Maybe** | Out of scope if the shop only sells in dollars. Check before asking |
| 6. Expiry date | **Maybe** | Ask only if expiry is planned for this release |

Two lessons come out of this table. First, the prompt said *"Do not say what should happen"*, and the reply obeyed: item 4 is a question about lower case, not the claim that "codes are case-insensitive". The same idea, worded as a question instead of a fact, is useful instead of harmful. Second, items 5 and 6 show **scope creep**: an AI will happily list every situation it can imagine. Asking the BA about all of them wastes their time. Your judgement decides which gaps matter **for this release**.

### 8. Turning Problems into Questions for the BA

Every finding should become a **question**, not an assumption. Good questions share three features: they name the requirement, they are **open** (they do not suggest the answer), and they can be answered with a fact.

| Weak question | Why it is weak | Better question |
|---|---|---|
| "Is 2 seconds OK for US-310 AC1?" | Suggests the answer | "What is the maximum load time for the checkout page, in seconds, and on which network?" |
| "What about the second coupon?" | Too vague to answer | "US-205 AC4: what message is shown when a shopper tries a second coupon, and is the first one kept?" |
| "Can you make AC2 clearer?" | Asks the BA to do your analysis | "US-310 AC2: should each error message name the field and say how to fix it?" |

Keep the questions in a simple **question log** with the requirement ID, the question, who you asked, the date and the answer. When the BA answers, update the requirement itself, not just your notes, so that everyone works from the same text.

Until an answer arrives, you can still prepare. A useful habit is to rewrite the requirement with sensible values **clearly marked as unconfirmed**:

```text
US-310 AC1: The checkout page loads in under 2 seconds on the test network. (to confirm with the BA)
US-310 AC3: The account is locked after 5 failed logins in a row. (to confirm with the BA)
```

The label is essential. Without it, a draft becomes a requirement by accident, which is the invented-rule problem again, created by a person this time instead of by an AI.

### 9. The Recommended Routine

Put together, the routine from this lesson is:

1. **Word check** the new stories (by hand or with `word_check.py`).
2. **AI review** with the Step 2 prompt, including the ban on answering its own questions.
3. **Ask what the story does not cover** (section 7), and triage the list.
4. **Compare** the word check with the AI review. Anything only one of them found deserves a closer look.
5. **Check the AI's questions** for invented answers (by eye, or with `answers_check.py`).
6. **Ask the BA**, using open questions, and keep a question log.
7. **Update the requirement** when the answer arrives.

Save the Step 2 prompt in `prompts.txt`, as in the handout:

```text
=== Requirements review - v1 ===
Use: find untestable requirements and draft questions for the BA.
Source: Handout 05, Topic 2

--- Prompt (new chat) ---
You are a QA engineer reviewing requirements before test design.
For each requirement below, say whether it is testable as written.
If not, explain why in one sentence and write ONE question for the business analyst.
Do not suggest answers to your own questions.

### Requirements
<paste requirements here>
### End

Reply as a table: ID | Testable? | Why not | Question for the BA
```

### 10. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| The AI "answers" its own questions ("Assume 5 attempts...") | The ban was missing or ignored | Re-ask: "Do not suggest answers. Only ask questions." |
| The AI rewrites the requirements instead of reviewing them | It drifted from the task | Re-ask with the table format, as in Step 2 |
| The AI flags everything as untestable | It is being over-cautious | Ask: "Which of these could a tester write a pass/fail test for today?" |
| You fill a gap with your own guess | It feels faster than asking | Mark it "(to confirm with the BA)" and ask |
| The word list keeps growing | Trying to catch every phrase | Keep it short; rely on the AI review and a human read for phrases |

---

## Practice Exercises

1. **Hand check (paper, 5 min).** Do the word check by hand on *"Search results appear quickly in an appropriate order."* Which words do you flag? Would an AI flag anything else? (For example: in what order?)

2. **Find the limit (code and AI tool, 15 min).** Add *"The page loads in good time."* to `REQUIREMENTS` in `word_check.py` and run it. Then follow the four steps:
   - **Prompt:** send the same requirement in the Step 2 review prompt.
   - **Review:** does the AI flag it? Does it ask a question or answer one?
   - **Run:** add your AI's questions to `answers_check.py` and run it.
   - **Record:** write one sentence in `prompts.txt` on what the word list missed and why.

3. **False alarm (paper, 5 min).** The word list flags `may` in *"Users may not apply an expired coupon."* Is it really vague? Write one sentence on why a human still needs to read every finding.

4. **Rewrite for testability (paper, 15 min).** Rewrite US-310 AC1 to AC3 so they are testable. Invent sensible values, and mark each one **"(to confirm with the BA)"**. Then write the BA question that would confirm each value, following the rules in section 8.

---

## Knowledge Check

1. What makes a requirement testable?

<details><summary>Answer</summary>

You can write a test for it with a clear pass/fail result, usually because it has a measurable value, an exact message or a precise condition.

</details>

2. Name the four common requirement defects from the handout, with an example of each.

<details><summary>Answer</summary>

Vague word ("fast"), missing value ("several"), missing behaviour (what is shown on a second coupon), weak obligation ("may be locked").

</details>

3. Why run the word check before the AI review?

<details><summary>Answer</summary>

The word check is deterministic and never invents a problem, so it gives a reliable baseline in milliseconds. The AI review then looks deeper for meaning problems, but can be wrong or inconsistent.

</details>

4. Why did the word check miss US-205 AC4, and what did the AI find?

<details><summary>Answer</summary>

AC4 has no weak words. Its problem is missing behaviour: it does not say what the user sees when they try a second coupon. That is a meaning problem a word list cannot find.

</details>

5. Why does the review prompt say "Do not suggest answers to your own questions"?

<details><summary>Answer</summary>

Without it, the AI tends to fill gaps with invented values, such as "lock after 5 attempts", which can then be accepted as the requirement.

</details>

6. "Users may not apply an expired coupon" is flagged by the word check. What kind of result is that?

<details><summary>Answer</summary>

A false positive. "May not" is a clear prohibition here, so the requirement is not vague, even though "may" is on the list.

</details>

7. You must start test design before the BA answers about US-310 AC1. What do you do?

<details><summary>Answer</summary>

Rewrite the requirement with a sensible value, clearly marked "(to confirm with the BA)", keep the question in the question log, and update the requirement when the answer arrives.

</details>

---

## Glossary

- **Requirements analysis:** checking that requirements are clear, complete and testable before test design.
- **Testable requirement:** a requirement you can write a clear pass/fail test for.
- **Business analyst (BA):** the person who clarifies requirements with the business; with the product owner, they decide what a requirement means.
- **Weak word:** a word that often makes a requirement vague, such as "fast", "several" or "may".
- **Missing behaviour:** a requirement that does not say what the user sees or what the system does in a situation.
- **Weak obligation:** wording, such as "may", that leaves unclear whether something is required.
- **Contradiction:** two requirements that cannot both be true.
- **Deterministic:** always giving the same output for the same input.
- **False positive:** a check reports a problem that is not there.
- **False negative:** a check misses a problem that is there.
- **Question log:** a record of questions for the BA, with who was asked, when, and the answer.
- **Unanswered situation:** a situation a user can be in that no acceptance criterion mentions.
- **Triage:** sorting findings by whether, and how urgently, they need action.
- **Scope creep:** extra situations or features that are not part of the current release, added a little at a time.
- **INVEST:** a checklist for good user stories: Independent, Negotiable, Valuable, Estimable, Small, Testable.

---

## Summary

- A requirement is **testable** when it supports a clear pass/fail test. Common defects are **vague words, missing values, missing behaviour and weak obligations**.
- Use **two checks in order**: a deterministic **word check** first, then an **AI review** for meaning.
- The word check missed **US-205 AC4**, which has no weak words but no stated behaviour for a second coupon. The AI found it, but the AI can also be wrong.
- Ban the AI from answering its own questions, and **check for invented answers**.
- Turn every problem into an **open question for the BA**. Mark any temporary values **"(to confirm with the BA)"**.

---

## Additional Resources

- Agile Alliance, *INVEST* glossary entry: https://agilealliance.org/glossary/invest
- ISTQB, *Certified Tester Foundation Level Syllabus v4.0.1* (reviews and testability): https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
- Python documentation, *re — Regular expression operations*: https://docs.python.org/3/library/re.html
