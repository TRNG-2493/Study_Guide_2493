# AI-Assisted Requirements Analysis

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **requirements analysis** is, where it sits in the QA lifecycle, and why finding a defect in a requirement is far cheaper than finding it in code.
- Describe the qualities of a **testable requirement** (clear, complete, consistent, measurable, atomic, traceable) and use the **INVEST** checklist for user stories.
- Recognise the most common **requirement defects**: ambiguity, unmeasurable wording, missing information, contradictions and untestable statements.
- Build a small, deterministic **weak-word linter** in Python and explain what it can and cannot catch.
- Write a **requirements review prompt** that asks an AI assistant to find problems and ask questions, without inventing answers.
- Check AI review findings with simple Python **grounding checks** (does the quoted text really exist in the story?).
- Turn findings into a **clarifying question log** for the product owner, and derive **traceable test conditions** from acceptance criteria.
- Rewrite vague acceptance criteria as **Given/When/Then** scenarios, clearly marking anything that still needs product owner confirmation.

---

## Why This Matters

Every test you will ever write is checked against something: a requirement, a user story, an acceptance criterion, a specification. In Week 3 you called this the **test basis**. If the test basis is vague, wrong or incomplete, then the tests built on it are vague, wrong or incomplete too, no matter how good the automation is.

Consider this acceptance criterion from our running example:

> The address form should be fast and user-friendly.

How would you test that? What is "fast"? Half a second? Five seconds? Who decides what "user-friendly" means? A developer can build *something* from this sentence, and a tester can write *some* test for it, but the two of them will almost certainly have different pictures in their heads. The difference only shows up later, as a bug report, an argument in a sprint review, or an unhappy customer.

This is why testers analyse requirements **before** writing tests. Industry experience, and the ISTQB syllabus you met in Week 3, both stress the same idea: **the earlier a defect is found, the cheaper it is to fix.** A misunderstanding caught in a story review costs a five-minute conversation. The same misunderstanding caught in production can cost a hotfix, a data clean-up and lost customers. Reviewing requirements is a form of **static testing**: you test the document without running any code. It is also the purest form of **shift-left testing**, because you cannot get further left than the requirement itself.

Requirements analysis is careful reading work, exactly the kind of language task LLMs handle well (Monday). With Tuesday's prompting skills, an AI assistant can read a story in seconds and list vague words, missing error paths and unanswered questions. What it **cannot** do is know what the business actually wants; only the product owner (PO) can answer that. So the skill you are learning is a partnership: the AI finds candidate problems quickly, and you judge them, ask the right people and record the answers.

This connects directly to the **Weekly Epic**. Requirements analysis is the first stage of the AI-augmented QA lifecycle you met earlier today in *AI within the QA Lifecycle*, and the requirements you clean up here become the input to AI-generated test cases and test data later today. On Thursday, your pair will design a **requirements agent**, and on Friday you will build your first QA agent. The review prompt and checks in this lesson are the raw material for that agent. For **Project 2 (Test Automation Framework)**, the e-commerce app's stories (login, coupons, shipping address) are the requirements you will analyse before you automate anything.

> **Scope note.** This lesson covers analysing requirements with AI help: finding defects, asking questions and deriving test conditions. Turning those conditions into complete, documented test cases is covered later today in *AI-Generated Test Cases*. The formal human review checklist and correction log are covered later today in *Human Validation of AI Output*, and what you may or may not paste into an AI tool is covered in *Responsible Use of AI in QE*. Requirements **agents** are covered on Thursday and Friday.

---

## The Concept

### 1. What Is Requirements Analysis?

A **requirement** is a statement of what a system must do (a **functional requirement**, such as "unknown coupon codes show an error") or how well it must do it (a **non-functional requirement**, or NFR, such as "search results appear within 2 seconds"). In agile teams, requirements usually arrive as **user stories** with **acceptance criteria** (AC):

- A **user story** describes a need from the user's point of view: *As a [role] I want [goal] so that [benefit].*
- **Acceptance criteria** are the specific conditions the story must meet to be accepted as done. They are the part testers care about most, because they are the closest thing to a test oracle.

**Requirements analysis**, from a tester's point of view, means reading the test basis critically and asking three questions:

1. **Can I understand it?** Is there only one reasonable way to read each statement?
2. **Can I test it?** Is there an objective way to decide pass or fail?
3. **Is anything missing?** Error paths, limits, formats, roles, non-functional qualities?

The output of requirements analysis is not tests. It is:

- a list of **findings** (problems in the requirement),
- a list of **clarifying questions** for the product owner,
- improved, agreed **acceptance criteria**, and
- a first list of **test conditions**: short statements of *what* needs to be tested, each traced to the criterion it comes from.

In the STLC from Week 3, this is the **requirements analysis** phase, which happens before test planning and test design.

#### An analogy: proofreading the recipe before you cook

Imagine you are a chef given a recipe that says "add some salt and bake until done". You could start cooking immediately and hope for the best. Or you could stop and ask: how much salt? Bake at what temperature? How do I know when it is "done"? Asking takes one minute. Throwing away a burnt cake takes an hour and the ingredients. Requirements analysis is proofreading the recipe before you turn on the oven.

### 2. Our Running Requirements

We will analyse three stories from the Project 2 e-commerce app throughout this lesson. Read them slowly now; we will return to them many times.

```text
US-101 Login
As a registered shopper I want to log in with my email and password
so that I can see my orders.
  AC1: Valid email + password -> redirected to "My Account" page.
  AC2: Wrong password -> message "Invalid email or password"
       (same message for unknown email).
  AC3: After 5 consecutive failed attempts the account is locked
       for 15 minutes.

US-205 Apply coupon at checkout
As a shopper I want to apply a coupon code so that I pay less.
  AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
  AC2: Subtotals under $50.00 are unchanged and show
       "Spend $50.00 to use SAVE10".
  AC3: Unknown codes show "Coupon code not recognised".
  AC4: Only one coupon per order.

US-310 Shipping address
As a shopper I want to enter a shipping address so my order is delivered.
  AC1: Required fields: full name, street, city, state, ZIP code, phone.
  AC2: ZIP code must be 5 digits (US only).
  AC3: Phone must be 10 digits.
  AC4: The address form should be fast and user-friendly.
```

US-205 is the user-facing version of the `apply_coupon(total, code)` function you have used since Monday. Notice that the function raises `ValueError` for unknown codes, while the story talks about a message on screen. That is normal: the story describes behaviour the shopper sees, and the code describes one piece of the implementation.

Before reading on, take two minutes and write down every question you would ask the product owner about these three stories. Then compare your list with the one we build in this lesson. You will probably find that you and the AI each catch things the other misses. That is the whole point of the partnership.

### 3. What Makes a Requirement Testable?

There is no single official list, but the qualities below appear in nearly every standard and textbook on requirements (for example, ISO/IEC/IEEE 29148, the international standard for requirements engineering). For each quality you will see what it means and an example from our stories.

| Quality | What it means | Problem example | Better version |
|---|---|---|---|
| **Clear (unambiguous)** | Only one reasonable reading | "The form should be user-friendly" | "All fields have visible labels and every error message names the field" |
| **Measurable (verifiable)** | An objective pass/fail is possible | "The form should be fast" | "The form submits and shows the next page within 2 seconds" |
| **Complete** | Covers normal, error and edge behaviour | "Only one coupon per order" (what happens on a second coupon?) | "Applying a second coupon replaces the first and shows 'Only one coupon per order'" |
| **Consistent** | Does not conflict with other requirements | Lockout message vs "same message for unknown email" (see Section 9) | One agreed message for all failed logins |
| **Atomic** | One requirement per statement | "Validate the ZIP and save the address and email a receipt" | Three separate criteria |
| **Traceable** | Has an ID so tests can point back to it | A requirement buried in a meeting note | US-310 AC2 |

The two qualities that matter most to a tester are **clear** and **measurable**. If a statement can be read two ways, the developer and the tester may each pick a different reading. If a statement has no measurable criterion, the test has no oracle: nobody can say whether it passed.

#### Weak words

Some words are reliable warning signs. Requirements engineers call them **weak words** (or "vague terms"). They include:

- **Vague quality words:** fast, quick, easy, simple, user-friendly, intuitive, robust, efficient, secure, modern.
- **Vague quantity words:** some, several, many, few, most, appropriate, adequate, reasonable.
- **Weak obligation words:** should, may, might, could, if possible, as needed. (Does "should" mean the feature is required or optional?)
- **Open-ended words:** etc., and so on, including but not limited to, and/or, TBD.

A weak word does not always mean the requirement is wrong, but it always deserves a second look. US-310 AC4 contains three of them in one short sentence: *should*, *fast* and *user-friendly*.

#### The INVEST checklist for user stories

For user stories, agile teams often use the **INVEST** checklist (popularised by Bill Wake). A good story is:

| Letter | Meaning | Tester's angle |
|---|---|---|
| **I**ndependent | Can be built and delivered on its own | Can I test it without waiting for another story? |
| **N**egotiable | Details can still be discussed | Is there room to ask questions before it is fixed? |
| **V**aluable | Delivers value to a user or the business | Is the "so that" part meaningful? |
| **E**stimable | The team can estimate the effort | Is there enough detail to estimate testing too? |
| **S**mall | Fits in one iteration | Is the test scope manageable in one sprint? |
| **T**estable | There is a clear way to verify it | Can every AC be turned into a pass/fail check? |

The **T** is the tester's letter, but the others matter too. A story that is not **Independent** (for example, a "shipping address" story that cannot be tested until the payment story is done) affects test planning. A story that is too big is usually hard to test thoroughly.

### 4. Common Requirement Defects, Worked by Hand

Before involving any AI, let us do a manual review of our three stories. This is important: you cannot judge an AI's review if you do not know what a good review looks like.

We will use five **defect categories**. The same categories will appear in our AI prompt later, so learn them now:

| Category | Meaning |
|---|---|
| **AMBIGUOUS** | Can reasonably be read in more than one way. |
| **UNMEASURABLE** | No objective pass/fail criterion (often caused by weak words). |
| **INCOMPLETE** | Something needed for testing is missing: an error path, a limit, a format, a role, a message, an NFR. |
| **CONTRADICTION** | Conflicts with another requirement, or with itself. |
| **UNTESTABLE** | Cannot be observed or checked at all, even in principle. |

#### US-310 Shipping address

- **AC1** "Required fields: full name, street, city, state, ZIP code, phone." **INCOMPLETE**: what happens when a required field is empty? What message is shown, and where? Is there a second address line (apartment, suite)? Maximum lengths?
- **AC2** "ZIP code must be 5 digits (US only)." Mostly clear and measurable. But **INCOMPLETE** on edge cases: is the US "ZIP+4" format (12345-6789) accepted? Leading zeros (Massachusetts ZIP codes such as 02134 start with zero, so the field must be text, not a number)? What does "US only" mean for the rest of the form: is there a country field at all?
- **AC3** "Phone must be 10 digits." **INCOMPLETE**: can the shopper type `(555) 123-4567` with brackets and dashes, or only `5551234567`? Is a leading `+1` allowed?
- **AC4** "The address form should be fast and user-friendly." **UNMEASURABLE** ("fast" has no number) and **AMBIGUOUS** ("user-friendly" means different things to different people; "should" might mean optional).

#### US-205 Apply coupon

- **AC1** "SAVE10 gives 10% off a subtotal of $50.00 or more." Clear and measurable, a good criterion. A tester might still ask: is the subtotal before or after tax and shipping? Is the discount rounded, and how? (Our `apply_coupon` function uses `round(total * 0.9, 2)`.)
- **AC2** Clear: the message text is given exactly. Good.
- **AC3** Clear message. Possible **INCOMPLETE**: is the code case-sensitive (`save10`)? What about spaces (`" SAVE10 "`)? On Tuesday you saw an AI *invent* a case-insensitivity rule; here, the right move is to *ask*.
- **AC4** "Only one coupon per order." **INCOMPLETE**: what happens when the shopper tries a second code? Is it rejected with a message, or does it replace the first?

#### US-101 Login

- **AC1** Clear.
- **AC2** Clear message, and the "same message for unknown email" rule is a deliberate security choice: it stops attackers discovering which emails have accounts (called **account enumeration**).
- **AC3** "After 5 consecutive failed attempts the account is locked for 15 minutes." **INCOMPLETE**: what does the shopper see while locked? Does a successful login reset the counter? Does the 15 minutes restart if they keep trying? Which message is shown on the 6th attempt?
- **AC2 + AC3 together**: potential **CONTRADICTION**. The lock message may reveal what AC2 is trying to hide. We work through this one step by step in Section 9.

#### What we found

Our manual review found roughly a dozen candidate issues in three short stories. None of them is exotic; they are the ordinary gaps that turn into ordinary bugs. Keep this list in mind as a **reference answer** for checking the AI review later. When you know what a good review contains, you can tell whether an AI review is good.

### 5. Where AI Helps, and Where It Does Not

You met the "pilot and co-pilot" division of labour on Tuesday for test design. The same idea applies here, with some details specific to requirements.

| Activity | AI assistant is good at... | The tester (and PO) must own... |
|---|---|---|
| Spotting weak words and vague phrases | Finding them quickly and consistently across many stories | Deciding which ones actually matter |
| Finding missing error paths and edge cases | Suggesting "what if" questions you did not think of | Judging which gaps are real risks for *this* product |
| Detecting contradictions | Comparing many criteria at once | Confirming the conflict is real, not a misreading |
| Proposing measurable rewrites | Suggesting a concrete shape ("within N seconds") | **The actual values.** Only the PO can say what N is |
| Writing clarifying questions | Phrasing clear, specific questions | Asking the right person and recording the answer |
| Deriving test conditions | Listing conditions per AC quickly | Checking traceability and relevance |
| Domain and business knowledge | General knowledge of e-commerce, security, accessibility | Company-specific rules, legal constraints, customer context |

The most dangerous row is **proposing measurable rewrites**. If you ask an AI to "make AC4 measurable", it will happily write "The form must load within 2 seconds". The sentence looks great. But where did "2 seconds" come from? The model produced a plausible number (Monday's next-token prediction at work), not a business decision. If that number slides into the story unchallenged, an invented requirement has entered your test basis, and every test downstream will enforce something nobody agreed to.

So the golden rule for this lesson is:

> **The AI may find problems and ask questions. It may not answer them.** Any proposed value must be labelled as a proposal and confirmed by the product owner.

You will build this rule directly into the prompt in Section 7 and check for violations in code in Section 8.

### 6. A Deterministic Baseline: The Weak-Word Linter

Before asking an AI anything, it is worth building a simple, **deterministic** check. "Deterministic" means the same input always gives the same output, unlike an LLM, whose output can vary from run to run (Tuesday's lesson on failure modes showed this with temperature and sampling). A deterministic tool is a useful baseline: it never invents anything, it costs nothing to run, and it gives you something to compare the AI against.

A **linter** is a tool that scans text or code for suspicious patterns. You may have used code linters such as `flake8` or `pylint`. Our linter scans requirement text for the weak words listed in Section 3.

```python
# weak_word_linter.py
import re

# Words and phrases that usually signal an ambiguous or unmeasurable requirement.
WEAK_WORDS = {
    "vague quality": ["fast", "quick", "user-friendly", "easy", "simple",
                      "intuitive", "efficient", "robust", "secure", "modern"],
    "vague quantity": ["some", "several", "many", "few", "most",
                       "appropriate", "adequate", "reasonable"],
    "weak obligation": ["should", "may", "might", "could", "if possible",
                        "as needed", "where applicable"],
    "open-ended": ["etc", "and so on", "including but not limited to",
                   "and/or", "tbd"],
}

def lint_requirement(req_id: str, text: str) -> list[dict]:
    """Return one finding per weak word found in the requirement text."""
    findings = []
    lowered = text.lower()
    for category, words in WEAK_WORDS.items():
        for word in words:
            # \b = word boundary, so "fast" does not match "breakfast"
            pattern = r"\b" + re.escape(word) + r"\b"
            for match in re.finditer(pattern, lowered):
                findings.append({
                    "req_id": req_id,
                    "word": text[match.start():match.end()],
                    "category": category,
                    "position": match.start(),
                })
    return sorted(findings, key=lambda f: f["position"])

if __name__ == "__main__":
    requirements = {
        "US-310 AC1": "Required fields: full name, street, city, state, ZIP code, phone.",
        "US-310 AC2": "ZIP code must be 5 digits (US only).",
        "US-310 AC4": "The address form should be fast and user-friendly.",
        "US-205 AC2": "Subtotals under $50.00 are unchanged and show "
                      "\"Spend $50.00 to use SAVE10\".",
    }

    for req_id, text in requirements.items():
        findings = lint_requirement(req_id, text)
        if not findings:
            print(f"{req_id}: no weak words found")
        for f in findings:
            print(f"{f['req_id']}: '{f['word']}' ({f['category']})")
```

Running it:

```text
US-310 AC1: no weak words found
US-310 AC2: no weak words found
US-310 AC4: 'should' (weak obligation)
US-310 AC4: 'fast' (vague quality)
US-310 AC4: 'user-friendly' (vague quality)
US-205 AC2: no weak words found
```

#### How the code works, line by line

- `import re` loads Python's **regular expression** module. A regular expression (regex) is a mini-language for describing text patterns.
- `WEAK_WORDS` is a **dictionary** that maps a category name (the key) to a **list** of words (the value). Grouping by category lets each finding say *why* the word is suspicious.
- `lint_requirement(req_id, text)` takes an ID and the requirement text and returns a list of findings. The type hint `-> list[dict]` documents that it returns a list of dictionaries.
- `lowered = text.lower()` converts the text to lower case so "Fast" and "fast" both match.
- The nested `for` loops visit every category and every word in it.
- `r"\b" + re.escape(word) + r"\b"` builds the regex.
  - `\b` is a **word boundary**: the position between a letter and a non-letter. Without it, "fast" would match inside "breakfast", and "may" would match inside "mayonnaise".
  - `re.escape(word)` protects any special characters in the word. For example, the `/` in "and/or" or the `.` in "etc." could otherwise be read as regex syntax.
  - The `r"..."` prefix makes a **raw string**, so Python does not treat `\b` as a backspace character.
- `re.finditer(pattern, lowered)` finds **every** match, not just the first, and returns match objects. `match.start()` and `match.end()` give the position of the match.
- `text[match.start():match.end()]` slices the **original** text (not the lowered copy) so the finding shows the word exactly as written.
- `sorted(findings, key=lambda f: f["position"])` orders findings by where they appear in the sentence. The `lambda` is a tiny anonymous function that tells `sorted` which value to compare.
- `if __name__ == "__main__":` means the demo at the bottom only runs when you execute the file directly, not when another file imports `lint_requirement`. We will rely on that in a moment.

#### What the linter cannot do

A word list is useful, but it is blunt. Here are its two classic failure types, which you will recognise from Monday's discussion of precision and recall:

```python
# lint_limits.py
from weak_word_linter import lint_requirement

# False positive: "may not" is a clear prohibition, not a weak obligation.
print(lint_requirement("PW-1", "Shoppers may not reuse their last 3 passwords."))
# False negative: "in good time" is vague, but it is not on our word list.
print(lint_requirement("PERF-1", "Search results appear in good time."))
```

```text
[{'req_id': 'PW-1', 'word': 'may', 'category': 'weak obligation', 'position': 9}]
[]
```

- **False positive:** "Shoppers may not reuse their last 3 passwords" is a perfectly clear prohibition, but the linter flags "may".
- **False negative:** "Search results appear in good time" is just as vague as "fast", but "in good time" is not in our list, so the linter misses it.

The linter also cannot see **missing** information at all. It found nothing wrong with US-310 AC1, yet our manual review found that the error message for an empty field is undefined. A word list can only flag words that are *there*; it cannot notice what is *absent*. Spotting absences requires understanding what a shipping form normally needs, and that is where a language model is genuinely useful.

So the linter and the AI complement each other:

| | Weak-word linter | AI review |
|---|---|---|
| Finds vague words | Yes, consistently | Usually |
| Finds missing information | No | Often |
| Finds contradictions between criteria | No | Often |
| Same output every run | Yes | No |
| Can invent problems or answers | No | Yes |
| Cost | Free, instant | Model call per review |

### 7. Writing a Requirements Review Prompt

Now we ask an AI assistant to review US-310. Everything you learned on Tuesday applies:

- a **persona** (a senior QA analyst),
- clear **context** (an e-commerce app, before tests are written),
- **delimiters** around the requirement (`<story>` tags) so the model knows exactly what to review,
- a **checklist** of defect categories so the review is systematic,
- a **format lock** (a JSON array with fixed keys) so we can check the answer in code,
- and an explicit **"do not invent"** instruction, the golden rule from Section 5.

As on Tuesday, we build the prompt as a list of role/content messages in Python. We do not call a real model in this lesson; in the next section a deterministic stand-in plays that part.

```python
# review_prompt.py
DEFECT_CATEGORIES = [
    "AMBIGUOUS",      # can be read in more than one way
    "UNMEASURABLE",   # no objective pass/fail criterion
    "INCOMPLETE",     # missing error path, rule, role, data format or NFR
    "CONTRADICTION",  # conflicts with another requirement
    "UNTESTABLE",     # cannot be observed or checked at all
]

def build_review_messages(story_id: str, story_text: str) -> list[dict]:
    """Build a role/content message list for a requirements review."""
    system = (
        "You are a senior QA analyst reviewing user stories for an "
        "e-commerce web app before any tests are written. "
        "You find problems; you never invent answers to them."
    )
    categories = ", ".join(DEFECT_CATEGORIES)
    user = f"""Review the user story between the <story> tags.

<story id="{story_id}">
{story_text}
</story>

Instructions:
1. Check every acceptance criterion for these defect categories: {categories}.
2. For each problem, quote the exact words from the story that cause it.
3. Write one clarifying question for the product owner per problem.
4. Do NOT propose answers, numbers or rules that are not in the story.
   If something is missing, ask about it.
5. If an acceptance criterion has no problems, do not mention it.

Return ONLY a JSON array. Each element must have exactly these keys:
"ac", "category", "quote", "explanation", "question".
"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

US_310 = """As a shopper I want to enter a shipping address so my order is delivered.
AC1: Required fields: full name, street, city, state, ZIP code, phone.
AC2: ZIP code must be 5 digits (US only).
AC3: Phone must be 10 digits.
AC4: The address form should be fast and user-friendly."""

if __name__ == "__main__":
    messages = build_review_messages("US-310", US_310)
    for m in messages:
        print(f"--- {m['role']} ---")
        print(m["content"])
```

The printed prompt:

```text
--- system ---
You are a senior QA analyst reviewing user stories for an e-commerce web app before any tests are written. You find problems; you never invent answers to them.
--- user ---
Review the user story between the <story> tags.

<story id="US-310">
As a shopper I want to enter a shipping address so my order is delivered.
AC1: Required fields: full name, street, city, state, ZIP code, phone.
AC2: ZIP code must be 5 digits (US only).
AC3: Phone must be 10 digits.
AC4: The address form should be fast and user-friendly.
</story>

Instructions:
1. Check every acceptance criterion for these defect categories: AMBIGUOUS, UNMEASURABLE, INCOMPLETE, CONTRADICTION, UNTESTABLE.
2. For each problem, quote the exact words from the story that cause it.
3. Write one clarifying question for the product owner per problem.
4. Do NOT propose answers, numbers or rules that are not in the story.
   If something is missing, ask about it.
5. If an acceptance criterion has no problems, do not mention it.

Return ONLY a JSON array. Each element must have exactly these keys:
"ac", "category", "quote", "explanation", "question".
```

#### Why each part of the prompt is there

- **System message:** sets the persona and states the core rule ("You find problems; you never invent answers to them"). Putting the rule in the system message as well as the instructions repeats it in the place models tend to treat as standing guidance.
- **`<story id="US-310">` delimiters:** separate the data (the story) from the instructions. Without them, a sentence in the story could be mistaken for an instruction, and the model might review only part of the text.
- **Instruction 1 (categories):** gives the review a structure. Without categories, models often produce a loose list of opinions such as "consider improving clarity", which is not actionable.
- **Instruction 2 (quote the exact words):** forces the model to **ground** every finding in the actual text. This is what makes the automatic check in Section 8 possible.
- **Instruction 3 (one question per problem):** the output we really want is questions for the PO, not opinions.
- **Instruction 4 (do not propose answers):** the golden rule. If the model writes "the form should load in 2 seconds", it has crossed the line.
- **Instruction 5 (skip clean ACs):** reduces noise, so you are not reading "AC2 looks fine" repeatedly.
- **The JSON format lock:** each finding has the same five keys, so Python can loop over the findings and check them one by one.

### 8. Checking the AI's Findings in Code

A model's review is a draft, not a verdict. Before you spend time reading every finding, a few cheap automatic checks can catch the most common problems:

1. **Shape check:** every finding has exactly the agreed keys.
2. **Category check:** the category is one of our five.
3. **Reference check:** the AC it names actually exists in the story.
4. **Grounding check:** the quoted text really appears in the story. If it does not, the model either paraphrased or invented the problem.
5. **Question check:** the question ends with a question mark (a cheap sign it is a real question, not a statement).

Here is a deterministic `fake_llm` that returns an **illustrative** response (written by hand to show typical good and bad findings; a real model's answer would differ), followed by the checks.

```python
# check_findings.py
import json
import re
from review_prompt import DEFECT_CATEGORIES, US_310, build_review_messages

def fake_llm(messages: list[dict]) -> str:
    """Deterministic stand-in for a real model. The text below is an
    ILLUSTRATIVE response, written to show typical good and bad findings."""
    return """[
  {"ac": "AC4", "category": "UNMEASURABLE", "quote": "fast",
   "explanation": "No time limit is given, so no test can pass or fail.",
   "question": "What is the maximum acceptable time for the form to load and to submit?"},
  {"ac": "AC4", "category": "AMBIGUOUS", "quote": "user-friendly",
   "explanation": "Different readers will judge user-friendliness differently.",
   "question": "Which usability or accessibility standard should the form meet?"},
  {"ac": "AC2", "category": "INCOMPLETE", "quote": "5 digits (US only)",
   "explanation": "The story does not say what happens for ZIP+4 codes such as 12345-6789.",
   "question": "Should ZIP+4 codes (12345-6789) be accepted, rejected or trimmed?"},
  {"ac": "AC3", "category": "INCOMPLETE", "quote": "Phone must be 10 digits",
   "explanation": "Formatting characters such as spaces, dashes or brackets are not covered.",
   "question": "Should (555) 123-4567 be accepted and normalised, or rejected?"},
  {"ac": "AC1", "category": "INCOMPLETE", "quote": "Required fields",
   "explanation": "No error message is defined for a missing field.",
   "question": "What message should appear when a required field is left empty?"},
  {"ac": "AC4", "category": "UNMEASURABLE", "quote": "must load in under 2 seconds",
   "explanation": "Page load must be under 2 seconds.",
   "question": "Is 2 seconds the right target"}
]"""

REQUIRED_KEYS = {"ac", "category", "quote", "explanation", "question"}

def check_finding(finding: dict, story: str) -> list[str]:
    """Return a list of problems with one AI finding (empty list = OK)."""
    problems = []
    if set(finding) != REQUIRED_KEYS:
        problems.append(f"wrong keys: {sorted(finding)}")
        return problems
    if finding["category"] not in DEFECT_CATEGORIES:
        problems.append(f"unknown category {finding['category']!r}")
    # The AC label must exist in the story, e.g. "AC4:" at the start of a line.
    if not re.search(rf"^{re.escape(finding['ac'])}:", story, re.MULTILINE):
        problems.append(f"{finding['ac']} does not exist in the story")
    # Grounding check: the quote must appear word for word in the story.
    if finding["quote"].lower() not in story.lower():
        problems.append(f"quote not found in story: {finding['quote']!r}")
    if not finding["question"].strip().endswith("?"):
        problems.append("question does not end with '?'")
    return problems

raw = fake_llm(build_review_messages("US-310", US_310))
findings = json.loads(raw)
print(f"{len(findings)} findings received\n")

kept = []
for i, f in enumerate(findings, start=1):
    problems = check_finding(f, US_310)
    status = "OK  " if not problems else "FLAG"
    print(f"{status} #{i} {f['ac']} {f['category']}: {f['quote']!r}")
    for p in problems:
        print(f"       - {p}")
    if not problems:
        kept.append(f)

flagged = len(findings) - len(kept)
print(f"\n{len(kept)} passed the automatic checks; "
      f"{flagged} flagged for a closer human look.")
```

```text
6 findings received

OK   #1 AC4 UNMEASURABLE: 'fast'
OK   #2 AC4 AMBIGUOUS: 'user-friendly'
OK   #3 AC2 INCOMPLETE: '5 digits (US only)'
OK   #4 AC3 INCOMPLETE: 'Phone must be 10 digits'
OK   #5 AC1 INCOMPLETE: 'Required fields'
FLAG #6 AC4 UNMEASURABLE: 'must load in under 2 seconds'
       - quote not found in story: 'must load in under 2 seconds'
       - question does not end with '?'

5 passed the automatic checks; 1 flagged for a closer human look.
```

#### How the code works

- `fake_llm(messages)` ignores its input and returns a fixed JSON string. In a real project, this function would call your organisation's approved AI tool. Keeping the same function signature means you can swap in a real model later without changing the checks.
- `json.loads(raw)` parses the JSON text into a Python list of dictionaries. If the model had wrapped the JSON in chatty text, this line would raise an error; Tuesday's *Format locking* lesson showed how to parse defensively and re-ask once.
- `set(finding) != REQUIRED_KEYS` compares the dictionary's keys with the expected set. Sets ignore order, so `{"a", "b"}` equals `{"b", "a"}`.
- `re.search(rf"^{re.escape(finding['ac'])}:", story, re.MULTILINE)` checks that a line in the story starts with, for example, `AC4:`. The `rf"..."` prefix is a raw **f-string**: raw for the regex backslashes, `f` for inserting the AC name. `re.MULTILINE` makes `^` match at the start of every line, not just the start of the whole text.
- `finding["quote"].lower() not in story.lower()` is the grounding check: a simple, case-insensitive substring test.
- `enumerate(findings, start=1)` gives a running number with each finding, starting at 1 so the output reads naturally.

#### Reading the result

Five findings passed and match our manual review from Section 4. Finding #6 was flagged twice:

- Its "quote" (`must load in under 2 seconds`) does not exist in the story. The model has **invented a requirement** and then reported it as if it were a quote. This is exactly the failure the golden rule is meant to prevent.
- Its "question" is really a leading statement without a question mark.

Notice what the checks did **not** do: they did not decide whether findings #1 to #5 are *important*. Passing the checks means "this finding is well-formed and grounded in the text", not "this finding is correct and useful". A human still reads them. For example, you might decide finding #3 (ZIP+4) is important because your company ships to business addresses that often use ZIP+4, while another team might decide it is out of scope. That judgement is yours.

Also notice what the model **missed**: it did not mention leading zeros in ZIP codes, which our manual review found. AI reviews have false negatives too. This is why you compare with your own reading rather than replacing it. The structured way to record what the AI got wrong or missed, and how you corrected it, is covered later today in *Human Validation of AI Output*. Automated, schema-based validation of agent output is covered on Friday.

### 9. Finding Contradictions and Gaps Across Stories

Single-criterion reviews miss problems that only appear when two requirements meet. Let us work through the US-101 example in detail, because it shows the kind of reasoning that a tester must still do personally.

```text
US-101 AC2: Wrong password -> message "Invalid email or password"
            (same message for unknown email).
US-101 AC3: After 5 consecutive failed attempts the account is locked
            for 15 minutes.
```

Step by step:

1. AC2 deliberately uses one message for both "wrong password" and "unknown email". Why? So an attacker cannot type random emails and learn which ones are registered shoppers.
2. AC3 locks an account after 5 failures. A locked shopper needs to be told *something*, otherwise they will keep trying and become frustrated.
3. If the lock message is "Your account is locked", then an attacker who types an email 6 times learns that the email **has an account** (unknown emails never lock). AC3's natural implementation leaks exactly what AC2 tries to hide.
4. So the two criteria are in tension. The resolution is a **business and security decision**: for example, show a generic message such as "Too many attempts, try again later" for both known and unknown emails. That decision belongs to the PO (and possibly the security team), not to the tester and not to the AI.

A good AI review of the two criteria together will often spot this, because account enumeration is a well-documented security topic in the text models learn from. But you should not *depend* on that. For contradiction hunting, put all related stories in the prompt inside separate delimiters and ask the model to quote **both** criteria for every conflict it reports, so you can check the claim in seconds. Even so, train yourself to ask, for every pair of criteria: **"Can both be true at once? Does one reveal what the other hides? Does one make the other impossible to test?"**

#### Gap-hunting prompts

Gaps (the INCOMPLETE category) are where AI assistance pays off most, because models have read thousands of descriptions of login pages, checkout pages and forms, and know what such features usually include. Useful prompt lines include:

```text
List the error paths that this story does not describe.
List the limits (minimum, maximum, length, count, time) that this story does not state.
List the user roles that might use this feature but are not mentioned.
List the non-functional qualities (performance, security, accessibility,
usability) that are relevant to this story but not stated.
For each item, write a question for the product owner. Do not suggest answers.
```

Each line asks for **absences**, phrased as questions. This is the AI equivalent of Tuesday's "What did you not cover?" pattern.

#### Non-functional requirements: from vague to measurable

US-310 AC4 ("fast and user-friendly") is really two hidden NFRs: a **performance** requirement and a **usability/accessibility** requirement. The tester's job is to turn each vague word into a question that, once answered, produces a measurable criterion:

| Vague word | Question for the PO | Shape of a measurable answer (values to be confirmed) |
|---|---|---|
| fast | How long may the form take to load, and to submit and show the next page? Under what load? | "Submit to next page within ___ seconds for ___% of requests" |
| user-friendly | Which accessibility standard must the form meet? Which usability rules matter most? | "Meets WCAG ___ level ___; every error names the field and stays next to it" |
| should | Is AC4 required for release, or a goal? | "Must" (blocking) or "Nice to have" (non-blocking) |

Notice the blanks. The **shape** of the answer can come from you or the AI. The **values** in the blanks must come from the PO. WCAG (the Web Content Accessibility Guidelines) is a widely used accessibility standard; your PO or company policy will say which version and level applies.

### 10. Clarifying Questions and the Question Log

The most valuable output of requirements analysis is often a short list of excellent questions. A good clarifying question:

- **is about one thing** ("What message appears for an empty ZIP code?" not "What about validation and errors and formats?"),
- **points to the requirement** (story and AC ID),
- **offers options where possible**, making it quick to answer ("Should ZIP+4 be accepted, rejected or trimmed?"),
- **is neutral**: it does not smuggle in an answer ("Is 2 seconds the right target?" is leading, because it suggests a number nobody agreed to),
- **explains the risk briefly if needed** ("...because the lock message could reveal which emails are registered").

Compare a weak and a strong version:

| Weak question | Strong question |
|---|---|
| "Is the phone field OK?" | "US-310 AC3: should `(555) 123-4567` with brackets and a dash be accepted and stored as `5551234567`, or rejected?" |
| "What about locked accounts?" | "US-101 AC2/AC3: which message does a locked account see, and may it reveal that the account exists?" |
| "Should the form be under 2 seconds?" | "US-310 AC4: what is the maximum acceptable time from pressing Continue to seeing the next page?" |

AI assistants are good at turning a rough concern into a well-phrased question. A useful prompt pattern is: *"Rewrite each question so it is about one topic, names the AC, offers two or three options where possible, and does not suggest a preferred answer."*

#### Keeping a question log

Questions get lost in chat threads. Keep them in a simple log with an ID, the story and AC, where the question came from, its status and the answer. A CSV file is enough, and it imports into any spreadsheet or test management tool.

```python
# question_log.py
import csv
import sys

questions = [
    {"id": "Q1", "story": "US-310", "ac": "AC4", "source": "AI + linter",
     "question": "What is the maximum acceptable time for the form to load and to submit?",
     "status": "OPEN", "answer": ""},
    {"id": "Q2", "story": "US-310", "ac": "AC2", "source": "AI",
     "question": "Should ZIP+4 codes (12345-6789) be accepted, rejected or trimmed?",
     "status": "ANSWERED", "answer": "Reject; show 'Enter a 5-digit ZIP code'"},
    {"id": "Q3", "story": "US-101", "ac": "AC2/AC3", "source": "Tester",
     "question": "Which message does a locked account see, and may it reveal that the account exists?",
     "status": "OPEN", "answer": ""},
]

writer = csv.DictWriter(sys.stdout, fieldnames=list(questions[0]))
writer.writeheader()
writer.writerows(questions)

open_count = sum(1 for q in questions if q["status"] == "OPEN")
print(f"\n{open_count} of {len(questions)} questions still open")
```

```text
id,story,ac,source,question,status,answer
Q1,US-310,AC4,AI + linter,What is the maximum acceptable time for the form to load and to submit?,OPEN,
Q2,US-310,AC2,AI,"Should ZIP+4 codes (12345-6789) be accepted, rejected or trimmed?",ANSWERED,Reject; show 'Enter a 5-digit ZIP code'
Q3,US-101,AC2/AC3,Tester,"Which message does a locked account see, and may it reveal that the account exists?",OPEN,

2 of 3 questions still open
```

- `csv.DictWriter` writes dictionaries as CSV rows. `fieldnames=list(questions[0])` uses the keys of the first dictionary as the column headers.
- `sys.stdout` sends the CSV to the screen here; in a real project you would open a file with `open("question_log.csv", "w", newline="")` instead.
- Notice that the `csv` module automatically wrapped values containing commas in double quotes, so the CSV stays valid.
- The `source` column records whether the question came from the AI, the linter or a human.
- The last line counts open questions using a **generator expression** inside `sum(...)`: `1 for q in questions if q["status"] == "OPEN"` produces a 1 for each open question, and `sum` adds them up.

A story with open questions is a risk you can report in a stand-up: "US-310 is not ready to test; two questions are open with the PO."

### 11. Deriving Test Conditions with Traceability

Once the questions are answered (or at least logged), you can start deriving **test conditions**. Recall from Week 3:

- A **test condition** is a short statement of *what* to test: "Discount applied at exactly $50.00".
- A **test case** adds *how*: preconditions, steps, test data and expected results.

Test conditions come first because they are quick to review. A list of ten one-line conditions is much easier to check for gaps than ten full test cases. Turning conditions into complete test cases is covered later today in *AI-Generated Test Cases*.

An AI assistant can propose conditions per acceptance criterion very quickly, using the same technique-driven prompting you learned on Tuesday (for example, "apply Boundary Value Analysis to AC1 and AC2"). Your job is to check two things:

1. **Coverage:** does every acceptance criterion have at least one condition?
2. **Traceability:** does every condition trace to a criterion that really exists? A condition with no valid parent is called an **orphan**, and it often means the AI (or a colleague) invented a requirement.

Both checks are mechanical, so let us write them in Python. The list below is a draft for US-205, as an AI assistant might propose it after a light edit by you.

```python
# test_conditions.py
# Test conditions derived from US-205 (apply coupon at checkout).
# Each condition says WHAT to test and traces to one acceptance criterion.
acceptance_criteria = {
    "AC1": "SAVE10 gives 10% off a subtotal of $50.00 or more.",
    "AC2": "Subtotals under $50.00 are unchanged and show "
           "\"Spend $50.00 to use SAVE10\".",
    "AC3": "Unknown codes show \"Coupon code not recognised\".",
    "AC4": "Only one coupon per order.",
}

# Draft list (for example, proposed by an AI assistant and edited by you).
test_conditions = [
    ("TC-205-01", "AC1", "Discount applied at exactly $50.00"),
    ("TC-205-02", "AC1", "Discount applied well above $50.00"),
    ("TC-205-03", "AC2", "No discount just below $50.00 ($49.99)"),
    ("TC-205-04", "AC2", "Spend-more message shown below $50.00"),
    ("TC-205-05", "AC3", "Error message for an unknown code"),
    ("TC-205-06", "AC5", "Coupon removed when cart is emptied"),
]

def trace_report(acs: dict, conditions: list[tuple]) -> None:
    covered = {}
    for cond_id, ac, _ in conditions:
        covered.setdefault(ac, []).append(cond_id)

    for ac in acs:
        ids = covered.get(ac, [])
        mark = ", ".join(ids) if ids else "NOT COVERED"
        print(f"{ac}: {mark}")

    orphans = [c for c in conditions if c[1] not in acs]
    for cond_id, ac, text in orphans:
        print(f"ORPHAN {cond_id} traces to {ac}, which does not exist: {text}")

trace_report(acceptance_criteria, test_conditions)
```

```text
AC1: TC-205-01, TC-205-02
AC2: TC-205-03, TC-205-04
AC3: TC-205-05
AC4: NOT COVERED
ORPHAN TC-205-06 traces to AC5, which does not exist: Coupon removed when cart is emptied
```

#### How the code works

- Each test condition is a **tuple** of three values: `(condition ID, AC ID, description)`. Tuples are like lists but cannot be changed after creation, which suits fixed records.
- `for cond_id, ac, _ in conditions` **unpacks** each tuple into variables. The underscore `_` is a Python convention for "a value I do not need here".
- `covered.setdefault(ac, []).append(cond_id)` builds a dictionary from AC to a list of condition IDs. `setdefault` returns the existing list for that AC, or inserts an empty list first if there is none. This avoids an `if ac not in covered` check.
- The second loop walks through the **acceptance criteria** (not the conditions), so an AC with no conditions is reported as `NOT COVERED`. This direction matters: if you only loop over conditions, you can never see what is missing.
- The **list comprehension** `[c for c in conditions if c[1] not in acs]` collects conditions whose AC does not exist: the orphans.

#### Reading the result

- **AC4 is not covered.** "Only one coupon per order" has no condition yet. This is a typical AI omission: rules phrased as constraints ("only one...") are easier to overlook than rules phrased as features. It is also the AC with an open question (what happens on the second coupon?), so it is not surprising that nobody wrote a condition for it.
- **TC-205-06 is an orphan.** "Coupon removed when cart is emptied" might be sensible behaviour, but no acceptance criterion says so. You have three honest options: delete the condition, raise it as a question to the PO ("Should a coupon be removed when the cart is emptied?"), or, if the PO agrees, add a new AC5 so the condition gains a real parent. What you must **not** do is quietly keep a test for an unagreed rule.

This tiny report is the seed of a **traceability matrix**, which you will build in full for test cases later today.

### 12. Rewriting Acceptance Criteria as Given/When/Then

In Week 6 you wrote Gherkin scenarios for BDD. Acceptance criteria written in **Given/When/Then** form are easier to test because they force three things to be explicit: the starting state (Given), the action (When) and the observable outcome (Then).

AI assistants are good at this rewrite, as long as you insist that they **do not fill gaps**. Here is a prompt fragment that does that:

```text
Rewrite each acceptance criterion of the story below as one or more
Gherkin scenarios (Given/When/Then).
Rules:
- Use only facts stated in the story or in the ANSWERS section.
- If a scenario needs a value that is not stated, write <TO CONFIRM: question>
  in its place. Do not make up values.
- One behaviour per scenario.
```

And here is an **illustrative** result for US-310 AC2 and AC4, after the PO answered Q2 ("Reject ZIP+4; show 'Enter a 5-digit ZIP code'") but before Q1 ("how fast?") was answered:

```gherkin
Feature: Shipping address (US-310)

  Scenario: Valid 5-digit ZIP code is accepted (AC2)
    Given I am on the shipping address form
    When I enter "02134" as the ZIP code
    And I fill in all other required fields with valid values
    And I press "Continue"
    Then I see the payment page

  Scenario: ZIP+4 code is rejected (AC2, answered in Q2)
    Given I am on the shipping address form
    When I enter "02134-1234" as the ZIP code
    And I press "Continue"
    Then I see the message "Enter a 5-digit ZIP code"

  Scenario: Address form responds quickly (AC4)
    Given I have filled in a valid shipping address
    When I press "Continue"
    Then I see the payment page within <TO CONFIRM: maximum time, Q1>
```

Points to notice:

- The first scenario deliberately uses `02134`, a ZIP code with a **leading zero**. That is a test idea from our manual review, made concrete. (Recall that a numeric field would turn `02134` into `2134`.)
- The second scenario cites **Q2**, so anyone reading it knows the rule came from an answered question, not from the original story. This is traceability for decisions, not just for requirements.
- The third scenario contains a visible `<TO CONFIRM: ...>` placeholder. That placeholder is a **feature, not a failure**: it makes the open question impossible to miss and impossible to automate by accident. A scenario with a placeholder is not ready for automation.
- "User-friendly" has not been rewritten at all, because there is not yet any agreed meaning to rewrite it into.

### 13. A Complete Worked Flow

Here is the full requirements analysis flow for one story, combining everything in this lesson. You will follow the same flow in today's exercise for Project 2.

1. **Read the story yourself first.** Write down your own findings and questions before seeing any AI output. This protects you from **anchoring**: once you have read the AI's list, it is hard to think beyond it.
2. **Run the deterministic linter.** Note every weak word. It takes a second and never invents anything.
3. **Run the AI review prompt** (Section 7), with categories, quotes, questions and the "do not invent" rule.
4. **Run the automatic checks** (Section 8): shape, category, AC reference, grounding, question form. Set aside anything flagged.
5. **Compare** the AI findings with your own list and the linter output. Note what the AI found that you missed, and what you found that the AI missed.
6. **Triage** each finding: keep, merge with another, or discard (with a reason).
7. **Write clarifying questions** into the question log, one topic per question, options where possible, no leading suggestions.
8. **Get answers** from the PO and record them in the log.
9. **Update the acceptance criteria**, ideally as Given/When/Then, with `<TO CONFIRM>` placeholders for anything still open.
10. **Derive test conditions** and run the coverage and orphan checks (Section 11).

Steps 3 and 4 take seconds. Steps 1, 5, 6 and 8 are where your value as a tester lies.

### 14. Pitfalls to Watch For

| Pitfall | What it looks like | What to do |
|---|---|---|
| **Invented answers** | The AI "fixes" a vague AC with numbers nobody agreed to | Golden rule in the prompt; grounding check; `<TO CONFIRM>` placeholders |
| **Missing domain rules** | The AI does not know that your company ships to Puerto Rico, or that a regulation applies | Only humans with domain knowledge can catch this; ask the PO |
| **Anchoring** | You only review what the AI flagged | Do your own reading first (step 1 of the flow) |
| **Treating fluent text as correct** | A well-written finding that is actually a misreading | Check the quote against the story; read the AC yourself |
| **Pasting confidential requirements into an unapproved tool** | Copying internal stories into a public chatbot | Use only approved tools; see *Responsible Use of AI in QE* later today |

### 15. Connecting to Project 2

For **Project 2 (Test Automation Framework)**, requirements analysis is the step that decides *what* your framework will test. Before you write a single Playwright test for login, coupons or the shipping form:

- Run the flow in Section 13 on each Project 2 story you are given (or on US-101, US-205 and US-310 if your trainer uses the generic e-commerce app).
- Commit the question log (`question_log.csv`) and the updated acceptance criteria to your repository alongside your tests, so reviewers can see where each test came from.
- Keep the weak-word linter as a small, reusable utility in your project's `tools/` folder.
- Save your review prompt in your prompt library (started on Tuesday). On Thursday you will see how a prompt like this becomes part of an agent's instructions.

Later today you will turn these test conditions into full test cases and test data.

---

## Practice Exercises

1. **Manual review first.** Without any AI help, review this new story and list every finding with a category (AMBIGUOUS, UNMEASURABLE, INCOMPLETE, CONTRADICTION, UNTESTABLE):

   ```text
   US-412 Product search
   As a shopper I want to search for products so that I can find what I need.
     AC1: Search returns relevant results quickly.
     AC2: Searches with no results show a helpful message.
     AC3: The search box accepts up to 100 characters.
     AC4: Results are sorted by relevance, price, etc.
   ```

2. **Extend the linter.** Add the phrases "relevant", "helpful" and "in good time" to `WEAK_WORDS` (choose sensible categories) and run the linter on US-412. Which findings from Exercise 1 does it now catch? Which does it still miss, and why?

3. **Break the checker.** Add two new findings to the `fake_llm` response: one whose `ac` is `"AC7"` and one whose category is `"STYLE"`. Run `check_findings.py` and confirm both are flagged. Then add a sixth check of your own: flag any finding whose `question` contains a whole number that does not appear as a whole number in the story (hint: `re.findall(r"\b\d+\b", text)` returns the whole numbers in a text). This is a simple way to catch questions that suggest invented values. Does finding #6 trip it? Which other findings trip it, and are they real problems or false positives?

4. **Questions for the PO.** Write four clarifying questions for US-412 that follow the rules in Section 10 (one topic, AC reference, options where possible, not leading). Add them to the question log code.

5. **Test conditions and traceability.** Write at least eight test conditions for US-412, run them through `trace_report`, and make sure there are no uncovered ACs and no orphans. If you want a test for a rule that is not in any AC, write a question instead.


---

## Knowledge Check

1. Why is a defect found during requirements analysis usually cheaper to fix than one found during test execution?
2. Name the five defect categories used in this lesson and give one example of each from US-101, US-205 or US-310.
3. Give one example of a false positive and one example of a false negative for the weak-word linter.
4. What is the "golden rule" for AI-assisted requirements analysis, and why does it matter for downstream tests?
5. What does the grounding check in `check_findings.py` verify, and what kind of AI mistake does it catch?
6. Explain the potential contradiction between US-101 AC2 and AC3. Who should resolve it?
7. What is an orphan test condition, and what are the three honest ways to deal with one?
8. Why should you review a story yourself **before** reading the AI's review?

<details>
<summary>Answers</summary>

1. Fixing a requirement means changing a sentence and having a conversation. Fixing the same problem after it is built means changing design, code, tests and possibly data, and, if it reaches production, dealing with customer impact as well. Requirements analysis is static testing done at the earliest possible point (shift-left).
2. AMBIGUOUS: "user-friendly" (US-310 AC4). UNMEASURABLE: "fast" (US-310 AC4). INCOMPLETE: no message defined for an empty required field (US-310 AC1), or no behaviour for a second coupon (US-205 AC4). CONTRADICTION: the lock message could reveal that an account exists, conflicting with the single-message rule (US-101 AC2/AC3). UNTESTABLE: a statement with no observable outcome at all; for example, "user-friendly" with no agreed definition cannot be checked objectively.
3. False positive: "Shoppers may not reuse their last 3 passwords" is flagged for "may" although it is a clear prohibition. False negative: "Search results appear in good time" is vague but not flagged, because "in good time" is not in the word list.
4. The AI may find problems and ask questions, but it may not answer them; any proposed value must be labelled as a proposal and confirmed by the PO. Otherwise invented values become part of the test basis, and tests end up enforcing rules nobody agreed to.
5. It verifies that the text the AI quoted actually appears in the story. It catches findings that paraphrase or invent requirement text, such as "must load in under 2 seconds".
6. AC2 uses one message for wrong passwords and unknown emails so attackers cannot discover registered emails. If a locked account shows "Your account is locked", an attacker can discover that an email is registered, because unknown emails never lock. The PO (with the security team if needed) must decide the message strategy; neither the tester nor the AI should decide it.
7. A test condition that traces to an acceptance criterion that does not exist. You can delete it, turn it into a question for the PO, or (if the PO agrees) add a new acceptance criterion so it has a real parent.
8. To avoid anchoring: once you have read the AI's findings, you tend to think only within them. Your own independent reading also gives you a reference to judge the AI's quality and to spot what it missed.

</details>

---

## Glossary

- **Requirements analysis:** Critically reading the test basis to find defects, ask questions and derive test conditions before test design.
- **Test basis:** The documents and knowledge tests are derived from, such as requirements, user stories and acceptance criteria.
- **Acceptance criteria (AC):** The specific conditions a user story must meet to be accepted as done.
- **Shift-left:** Moving testing activities earlier in the lifecycle to find defects sooner and more cheaply.
- **Weak words:** Vague words such as "fast", "should" or "etc." that often signal ambiguous or unmeasurable requirements.
- **INVEST:** Checklist for user stories: Independent, Negotiable, Valuable, Estimable, Small, Testable.
- **False positive / false negative:** A flag raised where there is no problem / a problem that is not flagged.
- **Grounding check:** Verifying that text an AI claims to quote really appears in the source.
- **Account enumeration:** An attack that discovers which usernames or emails are registered by observing differences in system responses.
- **Clarifying question log:** A tracked list of questions to the PO with ID, source, status and answer.
- **Test condition:** A short statement of what to test, traced to a requirement.
- **Orphan:** A test condition or test case that traces to no valid requirement.
- **Anchoring:** A cognitive bias in which the first information you see limits your later thinking.

---

## Summary

- Requirements analysis is **static, shift-left testing** of the test basis. Its outputs are findings, clarifying questions, improved acceptance criteria and traceable test conditions.
- Testable requirements are **clear, measurable, complete, consistent, atomic, feasible and traceable**. Weak words and INVEST are quick ways to spot problems.
- Do a **manual review first**, then use a **deterministic linter** as a baseline. The linter is consistent but blunt: it has false positives and false negatives and cannot see missing information.
- An AI review prompt uses a persona, delimiters, defect categories, exact quotes, one question per problem, a JSON format lock and the **golden rule: find problems and ask questions, never invent answers**.
- Cheap **automatic checks** (shape, category, AC reference, grounding, question form) catch malformed and invented findings, but a human still judges importance and spots what the AI missed.
- Some of the most important problems, such as the US-101 lockout contradiction, appear only when criteria are read **together** and need **business decisions** from the PO.
- Keep a **question log**, rewrite criteria as **Given/When/Then** with visible `<TO CONFIRM>` placeholders, and check test conditions for **coverage and orphans** before moving on to test cases.

---

## Additional Resources

- ISTQB, *Certified Tester Foundation Level (CTFL) v4.0* (overview and free syllabus download; chapter 3 covers static testing and the review process): https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0
- Agile Alliance, *What does INVEST Stand For?* (short glossary entry on the INVEST criteria for user stories): https://www.agilealliance.org/glossary/invest/
- Cucumber, *Gherkin Reference* (official reference for Feature, Scenario and Given/When/Then keywords used in Section 12): https://cucumber.io/docs/gherkin/reference/
