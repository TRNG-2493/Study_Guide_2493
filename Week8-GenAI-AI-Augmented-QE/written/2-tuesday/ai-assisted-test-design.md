# AI-Assisted Test Design

## Learning Objectives

By the end of this lesson you will be able to:

- Explain the **division of labour** between a tester and an AI assistant during test design: what the AI is good at, and what the tester must always own.
- Write **technique-driven prompts** that ask an AI assistant to apply a *named* Week 3 technique (Equivalence Partitioning, Boundary Value Analysis, decision tables, state transition, error guessing, pairwise) and to **show its work**.
- Use a set of reusable **prompt patterns** for test design: partitions-before-tests, technique labelling, "what did you not cover?", the risk-focused persona and critique-and-extend.
- Combine test design prompts with today's other techniques (**format locking** and **few-shot prompting**) to get output in a shape you can use.
- Turn an AI-assisted test design into **Gherkin scenarios** and a runnable **pytest `parametrize` table**.
- **Sanity-check** AI-designed tests with small Python helpers: recompute boundaries, check partition coverage, check pairwise coverage, and spot duplicates and invented requirements.

---

## Why This Matters

Test design is the heart of a tester's job. Writing test code is important, but a test is only as good as the **idea** behind it: which inputs, which states, which combinations and which expected results. In Week 3 you learned the classic **black-box test design techniques**: Equivalence Partitioning (EP), Boundary Value Analysis (BVA), decision table testing, state transition testing, use-case testing and error guessing. These techniques exist because humans are bad at "just thinking of tests". Without a method we test the happy path, add a couple of obvious negatives, and miss the boundary where the defect lives.

Large language models (LLMs) are very good at one part of this work: **producing breadth quickly**. Ask for "edge cases for a coupon field" and you get twenty ideas in a few seconds, some of which you had not thought of. But on Monday you also saw the danger. In the `apply_coupon` example, an AI draft contradicted the requirement, invented a case-insensitivity rule and skipped the $50.00 boundary entirely. The tests *looked* professional and were wrong.

This lesson sits exactly between those two facts. You will learn to use AI as a **test-design thinking partner**: a fast colleague who brainstorms, applies techniques on request and lays out tables, while **you** stay responsible for the requirement, the expected results and the final judgement. The trick is to stop asking "write me some tests" and start asking "apply Boundary Value Analysis to this rule, list the boundaries first, and tell me what you did not cover". The rest of today's lessons (principles, specificity and context, format locking, few-shot prompting, failure modes) give you the prompting tools; this lesson shows you how to point those tools at test design.

This connects directly to the **Weekly Epic**: by Friday you will build your first QA agent. An agent that designs tests is only as good as the test design knowledge in its instructions. The technique-driven prompts you write today are the raw material for that agent. It also feeds **Project 2 (Test Automation Framework)**: the e-commerce app you are testing (login, search, cart and checkout) is full of thresholds, combinations and state changes that suit these techniques, and today's exercise asks you to start a prompt library for exactly this kind of work.

> **Scope note.** Today is about *designing* tests with AI using named techniques. Generating complete test case suites across the QA life cycle, AI-assisted requirements analysis, AI-generated test data and the formal **human validation checklist** are all covered on **Wednesday**. Here you will do light-touch sanity checks only.

---

## The Concept

### 1. The Running Example

We will use the same small function from Monday throughout this lesson. It belongs to the cart service of a generic e-commerce web app:

```python
# cart.py
def apply_coupon(total: float, code: str) -> float:
    """SAVE10 gives 10% off orders of $50.00 or more.
    Orders under $50.00 are unchanged. Unknown codes raise ValueError."""
    if code != "SAVE10":
        raise ValueError(f"Unknown coupon: {code}")
    if total >= 50:
        return round(total * 0.9, 2)
    return total
```

The requirement (the docstring) has three rules:

1. `SAVE10` gives 10% off orders of **$50.00 or more**.
2. Orders **under $50.00** are unchanged.
3. **Unknown codes** raise `ValueError`.

Notice what the requirement does **not** say: whether negative totals are possible, whether codes are case-sensitive, whether the user must be logged in, or what happens with a total of exactly $0. Keep these gaps in mind; spotting them is part of test design, and a good AI prompt should surface them as **questions** rather than silently filling them in.

### 2. The Division of Labour: Who Does What?

Before writing any prompt, be clear about which parts of test design you can delegate and which you cannot. A useful way to think about it is a **pilot and co-pilot** relationship. The co-pilot can read the checklist, watch instruments and suggest actions; the pilot decides and is accountable.

| Test design activity | AI assistant is good at... | The tester must own... |
|---|---|---|
| Brainstorming test ideas | Producing many ideas fast, including unusual ones | Deciding which ideas matter for *this* product and risk |
| Applying a technique (EP, BVA, ...) | Mechanically listing partitions, boundaries and combinations when asked | Checking the partitions match the **real** requirement |
| Expected results (the **test oracle**) | Suggesting what "probably" happens | Confirming the expected result from the requirement or the product owner |
| Gaps and ambiguities | Listing questions, if you explicitly ask | Getting the answers from the right people |
| Prioritisation | Suggesting a risk ranking | Final priority, based on business knowledge |
| Formatting (tables, Gherkin, pytest) | Laying out content consistently | Making sure the content is correct before it becomes code |

The single most important row is the **test oracle**. Recall from Week 3 that an oracle is the source of truth that tells you whether a test passed: the requirement, a specification, a product owner, a reference implementation. An LLM is **not** an oracle. It predicts plausible text (Monday's "next-token prediction"), so its expected results are guesses that happen to be right most of the time. When the AI says "an order of $49.99 gets a 10% discount", it is not checking anything; it is producing a likely-looking sentence. Your job is to verify every expected result against the requirement.

A practical rule of thumb: **let the AI widen the funnel; you narrow it.** The AI's value is coverage of ideas. Your value is correctness and relevance.

### 3. From "Write Me Tests" to Technique-Driven Prompts

Compare two prompts for the same task.

**Prompt A (vague):**

```text
Write test cases for the coupon feature.
```

**Prompt B (technique-driven):**

```text
You are a risk-focused senior software tester.
Apply Boundary Value Analysis (3-value) to the requirement between the <req> tags.
Step 1: list every boundary you identify and explain why it is a boundary.
Step 2: for each boundary, give the values below, on and above it, using cent
        precision (0.01).
Step 3: give one test per value as a table: id | total | code | expected | technique.
Step 4: list OPEN QUESTIONS (anything the requirement does not specify) and
        anything you deliberately did NOT cover.
Only use behaviour stated in the requirement. Do not invent rules.
<req>
SAVE10 gives 10% off orders of $50.00 or more. Orders under $50.00 are unchanged.
Unknown codes raise ValueError.
</req>
```

Prompt A leaves every decision to the model: which technique, how many tests, which inputs, what format. You will get a generic list, often heavy on the happy path, and quite possibly with invented rules. Prompt B does five things that matter:

1. **Names the technique.** The model has seen many explanations of BVA in its training data. Naming it pulls the response toward that structured way of thinking instead of generic "test ideas".
2. **Asks for the reasoning first** (boundaries before tests). If the boundary list is wrong, you can see it immediately, before reading twenty tests built on top of it.
3. **States precision.** "Cent precision (0.01)" stops the model from choosing $49 and $51 as the "boundary" values, which is a very common mistake.
4. **Locks the format** into a table you can scan and later convert into code.
5. **Asks for gaps and exclusions**, which turns silent assumptions into visible questions.

The general shape of a technique-driven prompt is:

```text
[persona]  +  [named technique and variant]  +  [requirement inside delimiters]
+  [show your work: analysis before tests]  +  [output format]
+  [open questions and exclusions]  +  [constraint: no invented behaviour]
```

You will meet each of these ingredients in more detail in today's other lessons: personas and clear instructions in *Prompt engineering principles*, delimiters and context in *Specificity and context*, tables and JSON in *Format locking*, and examples in *Few-shot prompting*. Here we focus on what goes into each slot for test design.

#### Building the prompt in Python

Because you will reuse this pattern many times, it helps to build it with a small Python function. This also prepares you for later in the week, when prompts become reusable assets. The code below does **not** call a real model. `fake_llm` is a stand-in that returns a canned answer, so the example runs offline without an API key.

```python
# prompt_builder.py
REQUIREMENT = (
    "SAVE10 gives 10% off orders of $50.00 or more. "
    "Orders under $50.00 are unchanged. Unknown codes raise ValueError."
)

def technique_prompt(technique: str, requirement: str) -> list[dict]:
    """Build a chat-style message list asking for ONE named technique."""
    system = (
        "You are a risk-focused senior software tester. "
        "Only use behaviour stated in the requirement. "
        "If something is not specified, list it under OPEN QUESTIONS "
        "instead of guessing."
    )
    user = (
        f"Apply {technique} to the requirement between the <req> tags.\n"
        "Step 1: list the partitions or boundaries you identify, with a reason.\n"
        "Step 2: give one test per item as a table: id | input | expected | technique.\n"
        "Step 3: list OPEN QUESTIONS and anything you did NOT cover.\n"
        f"<req>{requirement}</req>"
    )
    return [{"role": "system", "content": system},
            {"role": "user", "content": user}]

def fake_llm(messages: list[dict]) -> str:
    """Stand-in for a real model so this runs offline. Returns canned text."""
    return (
        "PARTITIONS: P1 total < 50 (no discount); P2 total >= 50 (discount); "
        "P3 code != SAVE10 (error)\n"
        "TESTS:\nT1 | 20.00, SAVE10 | 20.00 | EP-P1\n"
        "T2 | 80.00, SAVE10 | 72.00 | EP-P2\n"
        "T3 | 80.00, BOGUS | ValueError | EP-P3\n"
        "OPEN QUESTIONS: Are negative totals possible? Is the code case-sensitive?"
    )

messages = technique_prompt("Equivalence Partitioning", REQUIREMENT)
for m in messages:
    print(f"[{m['role']}]\n{m['content']}\n")
print("--- model reply (fake) ---")
print(fake_llm(messages))
```

Output:

```text
[system]
You are a risk-focused senior software tester. Only use behaviour stated in the requirement. If something is not specified, list it under OPEN QUESTIONS instead of guessing.

[user]
Apply Equivalence Partitioning to the requirement between the <req> tags.
Step 1: list the partitions or boundaries you identify, with a reason.
Step 2: give one test per item as a table: id | input | expected | technique.
Step 3: list OPEN QUESTIONS and anything you did NOT cover.
<req>SAVE10 gives 10% off orders of $50.00 or more. Orders under $50.00 are unchanged. Unknown codes raise ValueError.</req>

--- model reply (fake) ---
PARTITIONS: P1 total < 50 (no discount); P2 total >= 50 (discount); P3 code != SAVE10 (error)
TESTS:
T1 | 20.00, SAVE10 | 20.00 | EP-P1
T2 | 80.00, SAVE10 | 72.00 | EP-P2
T3 | 80.00, BOGUS | ValueError | EP-P3
OPEN QUESTIONS: Are negative totals possible? Is the code case-sensitive?
```

**How the code works, line by line:**

- `REQUIREMENT = (...)`: Python joins adjacent string literals inside parentheses into one string. This keeps long text readable without `+` signs.
- `def technique_prompt(technique: str, requirement: str) -> list[dict]:` defines a function with **type hints**: two string parameters and a return value that is a list of dictionaries. Type hints do not change behaviour; they document intent.
- `system = (...)` holds the **system message**: the persona and the global rules ("only use behaviour stated", "list it under OPEN QUESTIONS"). Most chat-based LLM APIs accept a list of messages where each message has a `role` (`"system"`, `"user"` or `"assistant"`) and `content`. The system message sets behaviour for the whole conversation.
- `user = (...)` holds the **user message**: the actual task. The f-string `f"Apply {technique} ..."` inserts the technique name, so the same function works for EP, BVA, decision tables and so on.
- `<req>...</req>` are **delimiters**. They make it unmistakable where the requirement starts and ends, which matters when requirements are long or contain their own instructions-like sentences.
- `return [{"role": "system", ...}, {"role": "user", ...}]` returns the message list in the shape a real chat API would accept.
- `fake_llm` ignores its input and returns fixed text. In a real setup this is where an API call would go. Using a stub lets you develop and test the surrounding code (prompt building, output parsing) without paying for or waiting on a model, the same idea as the mocks you used with `unittest.mock` in Week 4.
- The `for m in messages:` loop prints each message with its role so you can read exactly what would be sent.

Notice that the (fake) reply is not perfect: it applied EP correctly but contains **no boundary values** at all, because we asked for EP, not BVA. This is normal and important: **each technique finds different defects**, so you usually run several technique prompts against the same requirement and merge the results.

### 4. Equivalence Partitioning with AI

**Recap:** Equivalence Partitioning divides the input domain into groups (partitions) where every value is expected to behave the same way. You then test **one representative per partition**, because testing two values from the same partition usually finds the same defects.

For `apply_coupon`, the `total` input has these partitions:

| Partition | Values | Expected behaviour | Source |
|---|---|---|---|
| P1 below threshold | 0.00 to 49.99 | unchanged | Rule 2 |
| P2 at or above threshold | 50.00 and up | 10% off | Rule 1 |
| P3 negative total | below 0.00 | **not specified** | Open question |

And the `code` input:

| Partition | Values | Expected behaviour | Source |
|---|---|---|---|
| C1 valid code | `"SAVE10"` | discount rules apply | Rule 1 |
| C2 unknown code | anything else | `ValueError` | Rule 3 |
| C3 different case | `"save10"` | **not specified** (code treats it as unknown) | Open question |

#### The "partitions before tests" pattern

The most useful EP prompt pattern is to ask for the partition list **first** and the tests **second**. There are two reasons:

1. **Reviewability.** A partition list is short. You can check it against the requirement in a minute. A list of twenty tests is much harder to check, and errors in the partitions are hidden inside it.
2. **Better generation.** LLMs generate text one token at a time, and each token is conditioned on what came before (Monday's lesson). When the model first writes out the partitions, the tests it writes afterwards are conditioned on that explicit structure, so they tend to follow it more closely. This is the same idea as asking a student to "show your working".

You can go one step further and run it as **two prompts**: first ask only for partitions, correct them yourself, then paste the corrected list into a second prompt that asks for one test per partition. This takes a little longer but means the tests are built on partitions you have already approved.

```text
Prompt 1: "Apply Equivalence Partitioning to the requirement below. List ONLY the
partitions for each input, with the rule that defines each one and the requirement
sentence it comes from. Mark any partition the requirement does not define as
UNSPECIFIED. Do not write tests yet."

Prompt 2: "Here are the approved partitions: <partitions>...</partitions>.
Write exactly one test per partition as a table: id | total | code | expected |
partition. For UNSPECIFIED partitions, write 'ASK PO' as the expected result."
```

The instruction "write 'ASK PO' as the expected result" is a small but powerful habit. It stops the model from inventing an expected result for behaviour nobody has defined.

#### Checking EP coverage yourself

AI assistants often produce several tests in one partition and none in another (most commonly, they forget invalid partitions). You can check this mechanically. Define the partitions as small Python functions (predicates) and classify every input the AI suggested:

```python
# ep_coverage.py
# Partitions for the 'total' input of apply_coupon(total, "SAVE10")
PARTITIONS = {
    "invalid: negative total": lambda t: t < 0,
    "valid: below threshold (0 to 49.99)": lambda t: 0 <= t < 50,
    "valid: at or above threshold (50+)": lambda t: t >= 50,
}

def classify(total):
    """Return the names of every partition this value belongs to."""
    return [name for name, rule in PARTITIONS.items() if rule(total)]

def coverage_report(inputs):
    covered = {}
    for value in inputs:
        for name in classify(value):
            covered.setdefault(name, []).append(value)
    for name in PARTITIONS:
        hits = covered.get(name, [])
        status = "COVERED" if hits else "MISSING"
        print(f"{status:8} {name:40} {hits}")

ai_inputs = [20.00, 35.50, 50.00, 75.00, 120.00]
coverage_report(ai_inputs)
```

Output:

```text
MISSING  invalid: negative total                  []
COVERED  valid: below threshold (0 to 49.99)      [20.0, 35.5]
COVERED  valid: at or above threshold (50+)       [50.0, 75.0, 120.0]
```

**How it works:**

- `PARTITIONS` is a dictionary. Each **key** is a readable partition name; each **value** is a `lambda`, a small anonymous function that takes a total `t` and returns `True` if `t` belongs to that partition. `lambda t: 0 <= t < 50` is shorthand for `def rule(t): return 0 <= t < 50`. Python allows chained comparisons such as `0 <= t < 50`.
- `classify(total)` uses a **list comprehension** to return every partition name whose rule returns `True`. For well-designed partitions each value should belong to exactly one; if a value lands in two, your partitions overlap, and if it lands in none, you have a gap in your partition definitions.
- `coverage_report` builds a dictionary `covered` mapping partition names to the inputs that hit them. `covered.setdefault(name, [])` returns the existing list for that key or creates an empty one first, so `.append(value)` always works.
- The final loop prints a status for **every** partition, not just the ones that were hit. That is the point: a missing partition is the finding.
- `f"{status:8} {name:40}"` pads the text to fixed widths so the columns line up.

The report tells you two things. First, the AI's five inputs never touched the negative-total partition. Second, three inputs sit in the same "50+" partition, and two in the "below" partition. From an EP point of view those extra inputs are **redundant**; they cost execution time without adding new information. (They may still be useful for *other* reasons, for example 50.00 is a boundary value, which is the next technique.)

Remember that the negative-total partition is an **open question**, not a known behaviour. The finding is not "add a test expecting `ValueError` for -5" (that would be inventing a requirement). The finding is "ask the product owner what should happen, then add the test".

### 5. Boundary Value Analysis with AI

**Recap:** defects cluster at the edges of partitions, because that is where developers write comparisons such as `>` versus `>=`. BVA tests values **on** and **next to** each boundary.

- **2-value BVA** tests the boundary value and its closest neighbour in the adjacent partition: for the $50.00 threshold, **49.99** and **50.00**.
- **3-value BVA** tests the value just below, on and just above the boundary: **49.99**, **50.00** and **50.01**.

The "closest neighbour" depends on the **precision** of the input. Money is measured in cents, so the step is 0.01. If the input were a whole number of items in a cart, the step would be 1.

The most common AI mistake with BVA is ignoring precision and proposing values like 49, 50 and 51. Those values do not test the boundary properly. Imagine the developer mistakenly wrote `total > 49.5` instead of `total >= 50`. Tests at 49, 50 and 51 all **pass** against that buggy code (49 gets no discount, 50 and 51 do), so the bug goes unnoticed. A test at **49.99** would catch it immediately, because the buggy code would wrongly discount it. That is why the technique-driven prompt in section 3 explicitly said "cent precision (0.01)".

#### Computing boundaries yourself

You should never trust boundary values you can calculate yourself in three lines of Python:

```python
# bva.py
from decimal import Decimal

def boundary_values(threshold: str, step: str = "0.01", three_value: bool = False):
    """Return BVA test inputs around a single threshold."""
    t = Decimal(threshold)
    s = Decimal(step)
    if three_value:
        return [t - s, t, t + s]
    return [t - s, t]

print("2-value BVA:", [str(v) for v in boundary_values("50.00")])
print("3-value BVA:", [str(v) for v in boundary_values("50.00", three_value=True)])

ai_suggested = ["49.00", "50.00", "51.00"]
expected = {str(v) for v in boundary_values("50.00", three_value=True)}
missing = sorted(expected - set(ai_suggested))
extra = sorted(set(ai_suggested) - expected)
print("Missing boundary values:", missing)
print("Not boundary values:", extra)
```

Output:

```text
2-value BVA: ['49.99', '50.00']
3-value BVA: ['49.99', '50.00', '50.01']
Missing boundary values: ['49.99', '50.01']
Not boundary values: ['49.00', '51.00']
```

**How it works:**

- `from decimal import Decimal` imports Python's **decimal** type. Ordinary floats are binary approximations, so `50.00 - 0.01` as a float gives `49.99` only approximately (try `print(0.1 + 0.2)` to see why this matters). `Decimal("50.00")` stores the exact decimal value, which is what you want for money. Note that we pass the numbers as **strings** (`"50.00"`), because `Decimal(50.00)` would first create the inexact float.
- `boundary_values` accepts the threshold, the step (default one cent) and a flag choosing 2-value or 3-value BVA. It returns a list of `Decimal` values.
- `[str(v) for v in ...]` converts each Decimal to a string for clean printing.
- The second half compares the AI's suggestions with the correct set using **set operations**: `expected - set(ai_suggested)` gives values we needed but the AI did not suggest, and `set(ai_suggested) - expected` gives values the AI suggested that are not boundary values. `sorted(...)` makes the output order predictable.

The result is a clear, objective finding you can feed back to the AI: "Your BVA used 49.00 and 51.00. With cent precision the boundary values are 49.99, 50.00 and 50.01. Regenerate the table." This **critique-and-correct** loop is much more effective than starting over with a new vague prompt.

#### Hidden boundaries

A good BVA prompt also asks the model to look for boundaries that are **implied** rather than stated. For a cart total, these might include $0.00 (empty cart), the maximum total the system accepts, and the precision of the result after rounding (`round(total * 0.9, 2)`: for example, 50.01 × 0.9 = 45.009, which rounds to 45.01). An AI is useful here because it brainstorms widely, but each implied boundary is an **open question** until the requirement or product owner confirms it.

### 6. Decision Tables with AI

**Recap:** decision table testing models business rules with several **conditions** that combine to produce **actions**. With *n* true/false conditions there are 2ⁿ combinations (rules). Each column (or row) of the table is one rule, and each rule becomes at least one test.

Suppose the checkout page adds a third condition: the user must be logged in to apply a coupon. Now we have three conditions:

- C1: code is `SAVE10`
- C2: total is at least $50.00
- C3: user is logged in

Three binary conditions give 2³ = 8 rules. AI assistants are helpful for laying out decision tables, but they make two typical mistakes: **missing combinations** (they list five or six rules instead of eight) and **inconsistent actions** (two rules with the same conditions but different actions). Both are easy to prevent if you generate the full set of combinations yourself and ask the AI only to help with, or check, the action column.

```python
# decision_table.py
from itertools import product

conditions = {
    "code_is_SAVE10": [True, False],
    "total_at_least_50": [True, False],
    "user_logged_in": [True, False],
}

def expected_action(code_is_SAVE10, total_at_least_50, user_logged_in):
    # Our (assumed) business rules -- confirm these with the product owner!
    if not user_logged_in:
        return "redirect to login"
    if not code_is_SAVE10:
        return "show 'Unknown coupon' error"
    if total_at_least_50:
        return "apply 10% discount"
    return "no discount, total unchanged"

names = list(conditions)
print("Rule | " + " | ".join(names) + " | action")
for number, values in enumerate(product(*conditions.values()), start=1):
    row = dict(zip(names, values))
    flags = " | ".join("T" if v else "F" for v in values)
    print(f"R{number}   | {flags} | {expected_action(**row)}")
```

Output:

```text
Rule | code_is_SAVE10 | total_at_least_50 | user_logged_in | action
R1   | T | T | T | apply 10% discount
R2   | T | T | F | redirect to login
R3   | T | F | T | no discount, total unchanged
R4   | T | F | F | redirect to login
R5   | F | T | T | show 'Unknown coupon' error
R6   | F | T | F | redirect to login
R7   | F | F | T | show 'Unknown coupon' error
R8   | F | F | F | redirect to login
```

**How it works:**

- `itertools.product(*lists)` returns the **Cartesian product**: every combination that takes one value from each list. With three lists of two values each, that is 2 × 2 × 2 = 8 tuples. The `*` in `product(*conditions.values())` **unpacks** the three lists into three separate arguments.
- `enumerate(..., start=1)` numbers the rules R1, R2, ... starting at 1 instead of 0.
- `dict(zip(names, values))` pairs each condition name with its value for this rule, for example `{"code_is_SAVE10": True, "total_at_least_50": True, "user_logged_in": True}`.
- `expected_action(**row)` **unpacks the dictionary** into keyword arguments, so the function receives `code_is_SAVE10=True, total_at_least_50=True, user_logged_in=True`.
- `" | ".join("T" if v else "F" for v in values)` turns `(True, False, True)` into `"T | F | T"`.

Two observations a tester should make from this output:

1. **The table is complete by construction.** `product` cannot forget a combination, which is exactly the mistake an AI might make. Combinations are a mechanical job: let code do it.
2. **The action column contains assumptions.** The comment says "confirm these with the product owner!" Is it right that a logged-out user is redirected *before* the code is checked? The requirement never said so. Notice also that R2, R4, R6 and R8 all have the same action; once the product owner confirms that "logged out always redirects", those four rules can be **collapsed** into one rule with "don't care" (`-`) values for C1 and C2, reducing the tests from 8 to 5.

A good AI collaboration pattern for decision tables is therefore:

1. You (or code) list the conditions and generate all combinations.
2. Ask the AI to propose the action for each rule **and quote the requirement sentence that justifies it**, writing `UNSPECIFIED` where none exists.
3. Ask the AI which rules could be collapsed, and why.
4. You confirm unspecified actions with the product owner.

### 7. State Transition Testing with AI

**Recap:** state transition testing models a system as **states** and **events** that move it between states. Tests cover valid transitions (and, for stronger coverage, invalid ones: events that should be rejected in a given state).

A classic e-commerce example is **login lockout**: after three failed attempts the account is locked for 15 minutes. States might be: `LoggedOut`, `OneFailure`, `TwoFailures`, `Locked`, `LoggedIn`. Events: `correct_password`, `wrong_password`, `lockout_expires`, `logout`.

LLMs are good at drafting a state table from a text description, and they can also produce diagrams in text formats such as Mermaid. A useful prompt:

```text
Apply state transition testing to the login lockout rule between <req> tags.
1. List the states and the events.
2. Produce a state table with one row per (state, event) pair, including pairs
   where the event is NOT allowed. For each row give: current state | event |
   next state | allowed? | requirement sentence.
3. Propose tests that achieve (a) every valid transition at least once (0-switch
   coverage) and (b) every invalid (state, event) pair.
4. List OPEN QUESTIONS, for example: does a correct password in the Locked state
   unlock the account?
<req>After three consecutive failed login attempts the account is locked for
15 minutes. A successful login resets the failure count.</req>
```

Asking for **one row per (state, event) pair** is the key instruction. If you only ask for "transitions", the model will typically list the valid ones and forget the invalid pairs, which is where many real defects live (for example, the system logging in a locked user who types the right password). With five states and four events there are 20 pairs; you can count the rows to check the AI did not skip any, in the same spirit as the decision table check above.

For the cart and checkout flow you might model states such as `Empty`, `HasItems`, `CouponApplied`, `PaymentPending`, `OrderPlaced`, and ask what happens on `remove_last_item` while in `CouponApplied` (does the coupon stay attached to an empty cart?). Questions like that are exactly what state-based thinking uncovers.

### 8. Error Guessing and Negative Tests

**Recap:** error guessing uses experience to anticipate where defects are likely. Negative tests check that the system handles invalid input and misuse gracefully.

This is where AI's breadth shines, because the model has "seen" a huge range of bug reports, checklists and edge cases in its training data. Ask for categories, not just a list:

```text
Act as a risk-focused senior tester using error guessing on the coupon code input
of an e-commerce checkout. Group your ideas under these headings: format and
length, character set and encoding, whitespace, case, repeated use, timing and
concurrency, and state of the cart. For each idea give the input, the risk it
probes, and mark the expected result as KNOWN (quote the requirement) or ASK PO.
```

Typical ideas it might return include: empty string; leading or trailing spaces (`" SAVE10 "`); lowercase `save10`; a 10,000-character code; Unicode look-alike characters; SQL-like text (`SAVE10' OR '1'='1`); applying the same coupon twice; applying a coupon then removing items so the total drops below $50; two browser tabs applying coupons at the same time.

Many of these are **good test ideas** and several (whitespace, case, the drop-below-$50 scenario) are excellent **questions for the product owner**. The "KNOWN or ASK PO" instruction is what keeps this list honest: from our requirement, only "unknown code raises `ValueError`" is known. Whether `" SAVE10 "` should be trimmed is a business decision, not something the AI or the tester gets to invent.

### 9. Pairwise and Combinatorial Testing (Briefly)

When a feature depends on several parameters, testing every combination quickly becomes impossible. Checkout might need to work across:

- Browser: Chrome, Firefox, Safari
- OS: Windows, macOS, Android
- Payment: Card, PayPal, GiftCard

All combinations: 3 × 3 × 3 = 27. **Pairwise testing** relies on the observation that many defects are triggered by the interaction of just **two** parameters, so it chooses a smaller set of rows in which **every pair of values** appears at least once. For three parameters with three values each, 9 rows can be enough.

You can ask an AI to propose a pairwise set, but pairwise sets are easy to get subtly wrong, and dedicated tools (such as Microsoft's open-source PICT, or Python libraries like `allpairspy`) generate them reliably. If you do use an AI suggestion, **check it**:

```python
# pairwise_check.py
from itertools import combinations, product

params = {
    "browser": ["Chrome", "Firefox", "Safari"],
    "os": ["Windows", "macOS", "Android"],
    "payment": ["Card", "PayPal", "GiftCard"],
}

# A pairwise set proposed by an AI assistant (9 rows instead of 27)
ai_rows = [
    ("Chrome", "Windows", "Card"),   ("Chrome", "macOS", "PayPal"),
    ("Chrome", "Android", "GiftCard"), ("Firefox", "Windows", "PayPal"),
    ("Firefox", "macOS", "GiftCard"), ("Firefox", "Android", "Card"),
    ("Safari", "Windows", "GiftCard"), ("Safari", "macOS", "Card"),
    ("Safari", "Android", "Card"),
]

names = list(params)
needed = set()
for (i, a), (j, b) in combinations(enumerate(names), 2):
    for va, vb in product(params[a], params[b]):
        needed.add((a, va, b, vb))

covered = set()
for row in ai_rows:
    for i, j in combinations(range(len(names)), 2):
        covered.add((names[i], row[i], names[j], row[j]))

print("All combinations:", len(list(product(*params.values()))))
print("Rows proposed:", len(ai_rows))
print("Pairs needed:", len(needed), "| pairs covered:", len(needed & covered))
for gap in sorted(needed - covered):
    print("Missing pair:", gap)
```

Output:

```text
All combinations: 27
Rows proposed: 9
Pairs needed: 27 | pairs covered: 25
Missing pair: ('browser', 'Safari', 'payment', 'PayPal')
Missing pair: ('os', 'Android', 'payment', 'PayPal')
```

**How it works:**

- `combinations(enumerate(names), 2)` produces every **pair of parameters**: (browser, os), (browser, payment), (os, payment). `enumerate` attaches positions so we can find the matching column in each row later.
- For each parameter pair, `product(params[a], params[b])` lists every **pair of values** (3 × 3 = 9). Three parameter pairs × 9 value pairs = **27 pairs needed**.
- The second loop walks every proposed row and records which value pairs it contains. Each row of three values contains three pairs.
- `needed & covered` is the set **intersection**; `needed - covered` is the set **difference**, the pairs nobody tests.

The AI's set looks perfect at a glance: nine rows, every browser three times, every OS three times. But its last row repeats `Card` where `PayPal` was needed, so Safari with PayPal and Android with PayPal are never tested. Changing the last row to `("Safari", "Android", "PayPal")` fixes both gaps. This is a perfect illustration of the theme of this lesson: the AI saved you the effort of drafting, and **20 lines of code** caught the mistake that a human eye would likely miss.

### 10. Exploratory Test Charters

Not all test design produces scripted test cases. In Week 3 you met **exploratory testing**, where learning, test design and execution happen together, usually guided by a **charter**: a short mission statement such as

> *Explore* the coupon field *with* unusual input formats *to discover* how the checkout handles malformed or borderline codes.

(This "Explore ... with ... to discover ..." template is widely used in the testing community.)

AI is helpful for drafting a **set of charters** that spread exploration across different risks. A good prompt gives the feature, the known risks and the time box:

```text
Draft 5 exploratory test charters for the checkout coupon feature of an
e-commerce web app, each for a 45-minute session. Use the format
"Explore <target> with <resources/approach> to discover <information>".
Cover different risk areas (input validation, pricing accuracy, cart state
changes, multi-tab use, accessibility of error messages). For each charter add
2-3 starter questions the tester should keep in mind. Do not include steps.
```

The final instruction, "do not include steps", matters: a charter is a mission, not a script. Without it, the model often drifts into writing scripted test cases, which defeats the purpose of exploration.

### 11. Reusable Prompt Patterns for Test Design

Across sections 3 to 10 the same few patterns kept appearing. Here they are collected so you can reuse them, and they are a good starting point for the prompt library in today's exercise.

| Pattern | What you add to the prompt | Why it helps |
|---|---|---|
| **Named technique** | "Apply 3-value Boundary Value Analysis..." | Pulls the model toward a structured method instead of generic ideas |
| **Analysis before tests** | "List partitions/boundaries/states first; then tests" | Makes the reasoning reviewable and the tests more consistent |
| **Technique labelling** | "For each test, name the technique and partition that produced it" | Shows coverage, exposes padding, enables traceability |
| **No invention** | "Only use behaviour stated in the requirement; mark the rest ASK PO" | Turns hidden assumptions into visible questions |
| **What did you not cover?** | "List what you deliberately did not cover and why" | Surfaces gaps; models are often candid when asked directly |
| **Risk-focused persona** | "You are a risk-focused senior tester who prioritises defects that cost money" | Shifts output toward negative, boundary and high-impact tests |
| **Critique-and-extend** | "Here is our current test list. Identify missing partitions/boundaries and duplicates, then propose only the additions" | Builds on your existing work instead of replacing it |
| **Precision statement** | "Money uses cent precision (0.01)" | Prevents the classic BVA mistake |

Two of these deserve a little more explanation.

**"What did you not cover?"** works because an LLM answers the question it is asked. If you ask for tests, it gives tests; it rarely volunteers its own blind spots. Asking explicitly often produces useful items such as "I did not consider currency or locale formatting", "I assumed a single coupon per order", or "performance under many concurrent coupon applications is out of scope". Each of these is either a missing test or a scoping decision you should make consciously.

**Critique-and-extend** is often more valuable than generating from scratch, because your team already has tests. Paste your existing test list (inside delimiters), and ask the model to act as a reviewer: which partitions and boundaries are missing, which tests are duplicates, which expected results do not match the requirement. Asking for **only the additions** keeps the output short and reviewable. It also avoids a common irritation where the model rewrites your whole list with small, unwanted changes.

#### Combining with format locking and few-shot examples

Two of today's other lessons make these patterns much more practical:

- **Format locking** (see today's lesson *Format locking*): asking for a fixed table or a JSON array means you can paste the result into a spreadsheet or parse it with `json.loads` instead of copying from prose. For test design, a locked set of columns such as `id | technique | partition | input | expected | requirement_ref` forces the model to fill in the technique and the requirement reference for *every* row, which is itself a quality check: an empty `requirement_ref` is a red flag for an invented rule.
- **Few-shot prompting** (see today's lesson *Few-shot prompting*): if your team writes tests in a particular style (naming conventions, level of detail, tagging), one or two examples of real tests from your project in the prompt are far more effective than describing the style in words.

You will learn how to make prompts like these into reusable, parameterised **prompt templates** for agents on **Thursday**.

### 12. From Design to Gherkin and pytest

A test design is only useful once it becomes executable tests or reviewable scenarios. AI assistants are good at this **translation** step because it is mostly mechanical, once the design itself is correct. The order matters: **design first, check it, then translate**. Translating an unchecked design simply produces well-formatted wrong tests.

#### To Gherkin (Week 6)

Given the checked EP and BVA design, you might ask:

```text
Convert the approved test design table between <design> tags into ONE Gherkin
Scenario Outline with an Examples table. Use the step wording from the example
scenario between <example> tags. Do not add, remove or change any test rows.
```

The instruction "do not add, remove or change any test rows" is essential. Without it, the model may "helpfully" add rows, which brings back unchecked content. A result in the style you learned in Week 6 might look like this:

```gherkin
Feature: Apply coupon at checkout

  Scenario Outline: SAVE10 discount depends on the order total
    Given my cart total is <total>
    When I apply the coupon "SAVE10"
    Then my cart total should be <expected>

    Examples:
      | case               | total | expected |
      | EP below threshold | 20.00 | 20.00    |
      | BVA just below     | 49.99 | 49.99    |
      | BVA on boundary    | 50.00 | 45.00    |
      | BVA just above     | 50.01 | 45.01    |
      | EP above threshold | 80.00 | 72.00    |
```

Notice the `case` column. Carrying the technique label from the design into the scenario keeps **traceability**: anyone reading a failing example can see why it exists.

#### To a pytest parametrize table (Week 4)

The same design maps naturally onto `@pytest.mark.parametrize`. Here is a runnable test file, written from the design above, with each test ID naming the technique that produced it:

```python
# test_apply_coupon_design.py
import pytest
from cart import apply_coupon

# Each row: (test id, total, expected total) -- designed with EP + 3-value BVA
VALID_CASES = [
    ("EP-below-threshold",   20.00, 20.00),
    ("BVA-just-below",       49.99, 49.99),
    ("BVA-on-boundary",      50.00, 45.00),
    ("BVA-just-above",       50.01, 45.01),
    ("EP-above-threshold",   80.00, 72.00),
]

@pytest.mark.parametrize(
    "total, expected",
    [(total, expected) for _, total, expected in VALID_CASES],
    ids=[case_id for case_id, _, _ in VALID_CASES],
)
def test_save10_totals(total, expected):
    assert apply_coupon(total, "SAVE10") == expected

@pytest.mark.parametrize("code", ["BOGUS", "save10", ""],
                         ids=["unknown-code", "lowercase-code", "empty-code"])
def test_invalid_codes_raise(code):
    with pytest.raises(ValueError):
        apply_coupon(80.00, code)
```

Save `cart.py` (from section 1) and this file in the same folder and run:

```bash
pytest -v test_apply_coupon_design.py
```

Output (timing will vary on your machine):

```text
test_apply_coupon_design.py::test_save10_totals[EP-below-threshold] PASSED [ 12%]
test_apply_coupon_design.py::test_save10_totals[BVA-just-below] PASSED   [ 25%]
test_apply_coupon_design.py::test_save10_totals[BVA-on-boundary] PASSED  [ 37%]
test_apply_coupon_design.py::test_save10_totals[BVA-just-above] PASSED   [ 50%]
test_apply_coupon_design.py::test_save10_totals[EP-above-threshold] PASSED [ 62%]
test_apply_coupon_design.py::test_invalid_codes_raise[unknown-code] PASSED [ 75%]
test_apply_coupon_design.py::test_invalid_codes_raise[lowercase-code] PASSED [ 87%]
test_apply_coupon_design.py::test_invalid_codes_raise[empty-code] PASSED [100%]

============================== 8 passed in 0.02s ===============================
```

**How the code works:**

- `VALID_CASES` keeps the design as data: each tuple is `(id, total, expected)`. Keeping the design in one list makes it easy to review against the design table, and easy to extend.
- `@pytest.mark.parametrize("total, expected", [...], ids=[...])` tells pytest to run the test once per row. The first argument names the parameters; the second is the list of value tuples; `ids` gives each run a readable name.
- `[(total, expected) for _, total, expected in VALID_CASES]` is a list comprehension that **unpacks** each tuple and drops the id (the underscore `_` is a convention for "a value I don't need"). The `ids` list does the opposite: it keeps only the id.
- `test_invalid_codes_raise` uses `pytest.raises(ValueError)` as a **context manager**: the test passes only if the code inside the `with` block raises `ValueError`. This is the correct way to test Rule 3, unlike Monday's AI draft that expected the original total to be returned.
- The `-v` (verbose) flag prints each test with its ID, which is where the technique labels pay off.

Look carefully at the `lowercase-code` test. It **passes**, because the current code treats `"save10"` as unknown. But the requirement never said coupons are case-sensitive; it is one of our open questions. This test therefore documents **current behaviour**, not confirmed **required behaviour**. A good practice is to add a comment or a marker linking it to the open question, and update it once the product owner decides. Also note the expected values for 50.01: 50.01 × 0.9 = 45.009, which `round(..., 2)` turns into 45.01. You should calculate expected results like this yourself (or from the requirement), never copy them blindly from an AI table.

Floats in assertions deserve a brief caution: comparing floats with `==` works here because the function rounds to two decimals and the expected values are exactly what `round` produces. For more complex calculations, `pytest.approx` or the `Decimal` type is safer.

### 13. Light-Touch Sanity Checks Before You Use AI-Designed Tests

Throughout this lesson you have seen small checks. Here they are as a short list you can run through every time an AI helps with test design. (A fuller, structured **human validation** process for AI output is covered on **Wednesday**.)

1. **Trace every test to the requirement.** Can you point to the sentence that justifies the expected result? If not, it is either an open question or an invented rule.
2. **Recompute boundaries.** Use code like `bva.py` with the right precision. Never accept "49 / 50 / 51" for money.
3. **Check partition coverage.** Every partition, valid and invalid, should have at least one test (`ep_coverage.py`).
4. **Check combination coverage.** For decision tables, count the rules (2ⁿ) or generate them with `itertools.product`; for pairwise sets, verify all pairs (`pairwise_check.py`).
5. **Remove duplicates.** Several tests in the same partition with no boundary or risk reason add cost without value.
6. **Recalculate expected results.** Do the arithmetic yourself for anything numeric (rounding, percentages, currency).
7. **Look for invented requirements.** Words like "case-insensitive", "trimmed", "maximum of", "within 24 hours" that do not appear in the requirement are warning signs.
8. **Run the tests.** A test that fails might reveal a product bug **or** a wrong test; investigate before deciding which.

None of these checks needs AI. That is deliberate: you are verifying the AI with **independent** methods, the same principle as not letting a developer be the only reviewer of their own code.

### 14. A Complete Worked Flow

Putting it all together, here is how a tester might design tests for the SAVE10 rule with an AI assistant in about 20 minutes:

1. **Read the requirement yourself** and note your own first ideas and questions (two minutes, before any AI). This protects you from anchoring on the AI's view.
2. **EP prompt, partitions only.** Review and correct the partitions. Add "negative total" and "lowercase code" as UNSPECIFIED.
3. **EP + BVA prompt for tests**, with the approved partitions pasted in, cent precision stated, format locked to a table with `technique` and `requirement_ref` columns.
4. **Run `bva.py` and `ep_coverage.py`** against the suggested inputs. Feed findings back: "You used 49.00 and 51.00; with cent precision use 49.99 and 50.01. Regenerate rows T4 to T6 only."
5. **"What did you not cover?"** prompt. Note new ideas (whitespace, coupon then remove items) as questions or new tests.
6. **Send open questions** to the product owner (negative totals, case sensitivity, whitespace, login requirement).
7. **Translate** the approved design into a pytest parametrize table or a Gherkin Scenario Outline, instructing the AI not to change any rows.
8. **Run the tests** and investigate any failure.

The AI contributed speed and breadth at steps 2, 3, 5 and 7. You contributed the oracle, the corrections and the judgement at steps 1, 2, 4, 6 and 8. That balance is what "AI-assisted" means.

### 15. Connecting to Project 2

Your Project 2 framework will test an e-commerce web app. Some natural candidates for technique-driven prompts:

- **Login:** state transition testing for lockout; EP for username and password formats.
- **Search:** EP for query types (empty, single word, phrase, special characters, very long); BVA on any result-count or length limits.
- **Cart:** BVA on quantity limits (0, 1, max, max + 1); decision tables for discounts combined with shipping rules.
- **Checkout:** pairwise for browser × OS × payment; decision tables for coupon, login and total conditions; exploratory charters for payment error handling.

In today's exercise you will start a **prompt library** for test design and debugging. The patterns in section 11 and the prompts in sections 3 to 10 are a good starting set. Store each prompt with its purpose, the technique it applies and a note about what to check in the output.

---

## Practice Exercises

1. **Technique swap.** Use `technique_prompt` from section 3 to build prompts for "3-value Boundary Value Analysis" and "error guessing" for the SAVE10 requirement. Print both. What differs in the instructions you would *add* for each technique beyond the template (for example, precision for BVA, categories for error guessing)? Extend the function with an optional `extra_instructions` parameter.
2. **EP coverage for codes.** Extend `ep_coverage.py` so it also checks the `code` input with partitions "valid SAVE10", "unknown code" and "different case of SAVE10". Feed it the AI suggestions `["SAVE10", "BOGUS", "SAVE20", "XYZ"]`. Which partition is missing, and is the expected result for it known or an open question?
3. **Fix the pairwise set.** In `pairwise_check.py`, change the last row to `("Safari", "Android", "PayPal")` and rerun. Confirm all 27 pairs are covered. Then add a fourth parameter, `currency: ["USD", "EUR"]`, and see how many pairs are needed and how many your nine rows cover.
4. **Collapse the decision table.** Modify `decision_table.py` to print only the distinct actions and which rules share them. Which rules could be merged into a single rule with "don't care" values, assuming the product owner confirms "logged out always redirects"? How many tests remain?
5. **State table count.** For the login lockout example, list the five states and four events. How many (state, event) rows should a complete state table have? Write a short Python snippet with `itertools.product` that prints them all, so you could compare it with an AI-generated table.
6. **Critique-and-extend.** Write a prompt that gives an AI the five `VALID_CASES` rows from section 12 and asks it to propose only missing tests, each labelled with technique and requirement reference, with unspecified behaviour marked ASK PO. If you have access to an approved AI assistant, run it and apply the section 13 checks to the result.

---

## Knowledge Check

1. Why should the tester, not the AI, own the expected results of a test?
2. What is the benefit of asking an AI to list partitions or boundaries *before* writing tests?
3. With cent precision, what are the 3-value BVA inputs for the $50.00 threshold, and why are 49, 50 and 51 not good enough?
4. A decision table has four binary conditions. How many rules does the full table have, and how can you make sure an AI-generated table has not skipped any?
5. In the pairwise example, the AI's set had nine rows and every value appeared three times. Why was it still incomplete?
6. What does the instruction "mark unspecified behaviour as ASK PO" prevent?
7. The `lowercase-code` pytest case passes. Why does that not prove case-sensitivity is correct?

<details>
<summary>Answers</summary>

1. An LLM predicts plausible text; it does not check facts against the requirement, so it is not a test oracle. Expected results must come from the requirement, specification or product owner, and the tester is accountable for them.
2. The analysis becomes short and reviewable, errors are caught before they spread into many tests, and the tests that follow are generated conditioned on an explicit structure, so they tend to follow it more closely.
3. 49.99, 50.00 and 50.01. With 49, 50 and 51 you cannot distinguish `>= 50` from, for example, `> 49.5`, and you never test the closest values on either side of the boundary.
4. 2⁴ = 16 rules. Generate all combinations yourself (for example with `itertools.product`) and compare, or at least count the AI's rules.
5. Balanced value frequencies do not guarantee pair coverage. The last row repeated `Card` where `PayPal` was needed, so the pairs (Safari, PayPal) and (Android, PayPal) were never tested.
6. It prevents the model from inventing requirements (silently filling gaps with plausible assumptions) and turns those gaps into visible questions for the product owner.
7. The test documents the *current* behaviour of the code. The requirement does not specify case handling, so whether case-sensitivity is *required* is an open question to confirm with the product owner.

</details>

---

## Glossary

- **Test oracle:** The source of truth used to decide whether a test passed (requirement, specification, product owner, reference implementation).
- **Technique-driven prompt:** A prompt that asks an AI to apply a specific, named test design technique and show its intermediate analysis.
- **Equivalence Partitioning (EP):** Dividing inputs into groups expected to behave the same, and testing one representative per group.
- **Boundary Value Analysis (BVA):** Testing values on and adjacent to partition edges; 2-value uses the boundary and its nearest neighbour, 3-value adds the neighbour on the other side.
- **Precision (step):** The smallest meaningful difference between input values, such as 0.01 for money; it determines the "adjacent" values in BVA.
- **Decision table:** A table of condition combinations (rules) and the resulting actions; *n* binary conditions give 2ⁿ rules.
- **State transition testing:** Modelling a system as states and events and testing valid and invalid transitions.
- **Pairwise testing:** Choosing a reduced set of combinations in which every pair of parameter values appears at least once.
- **Exploratory test charter:** A short mission for a time-boxed exploratory session, often in the form "Explore ... with ... to discover ...".
- **Critique-and-extend:** A prompt pattern in which the AI reviews an existing test list and proposes only additions and corrections.
- **Cartesian product:** Every combination formed by taking one value from each of several lists (`itertools.product`).
- **Traceability:** The ability to link each test back to the requirement and technique that produced it.

---

## Summary

- Use AI as a **test-design thinking partner**: it widens the funnel with fast, broad ideas; you narrow it with correct expected results and judgement. The AI is **not** a test oracle.
- Replace "write me tests" with **technique-driven prompts**: persona, named technique, requirement in delimiters, analysis before tests, locked format, open questions and exclusions, and an explicit "do not invent" rule.
- Each Week 3 technique has its own prompt details: **partitions first** for EP, **precision** for BVA, **every combination** for decision tables, **every (state, event) pair** for state transitions, **categories and KNOWN/ASK PO** for error guessing, **verify all pairs** for pairwise, **no steps** for exploratory charters.
- Reusable patterns, including technique labelling, "what did you not cover?", the risk-focused persona and critique-and-extend, form the core of a test design prompt library.
- **Design first, check it, then translate** into Gherkin or a pytest parametrize table, instructing the AI not to change rows.
- Small, independent Python checks (BVA values, EP coverage, decision table completeness, pairwise coverage) catch the mistakes AI makes most often. Formal human validation of AI output follows on Wednesday.

---

## Additional Resources

- ISTQB, *Certified Tester Foundation Level (CTFL) v4.0* (overview and free syllabus download; chapter 4 covers black-box, white-box and experience-based test techniques): https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0
- pytest documentation, *How to parametrize fixtures and test functions*: https://docs.pytest.org/en/stable/how-to/parametrize.html
- Google AI for Developers, *Prompt design strategies* (constraints, response format and few-shot examples, with worked prompts): https://ai.google.dev/gemini-api/docs/prompting-strategies
