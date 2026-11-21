# AI-Generated Test Data

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **test data** is, why it is often the slowest part of testing, and the difference between **production data**, **masked data**, **hand-crafted data** and **synthetic data**.
- Work out the **data needs** of a test case by hand: valid, invalid, boundary, edge, state and volume data.
- Write a **constrained test data prompt** that tells an AI assistant the field rules, the categories you want, the format to return and the safety rules it must follow.
- Recognise the typical mistakes in **AI-Generated Test Data**: wrong labels, wrong counts, data that only *looks* valid (card numbers, dates, phone numbers), real-looking personal data and missing variety.
- Use the **"AI designs, code generates"** split: let the AI suggest categories and tricky values, then generate volume with seeded Python code and the **Faker** library so the data is **reproducible**.
- **Validate** AI-generated data with small, independent Python checks (field rules, the **Luhn** check, real calendar dates, uniqueness and **referential integrity**).
- Store test data as a **JSON fixture** and drive a pytest test from it with `@pytest.mark.parametrize`.

---

## Why This Matters

Ask any experienced tester what slows them down, and "test data" will be near the top of the list. A test case says *"log in as a shopper whose account is locked"*, but somebody has to **create** that locked account. A checkout test needs a cart worth exactly $50.00, a valid shipping address, a payment card the payment provider accepts in test mode, and a coupon that has not expired. Every one of those is a piece of data that must exist, be correct and be available when the test runs.

Getting test data wrong causes three kinds of pain:

1. **False failures.** The test fails, but the product is fine; the data was wrong (an expired coupon, an impossible date, a user who does not exist). Teams waste hours chasing defects that are not there.
2. **False passes.** The test passes, but only because the data never hit the interesting case. If every ZIP code in your data set is `"12345"`, you will never find out what the form does with `"02110"` (a real Boston ZIP code with a leading zero) or `"0211"`.
3. **Risk to real people.** The quickest way to get "realistic" data is to copy production. That puts real customers' names, addresses and card details into test environments, logs and screenshots, which is a privacy and legal problem.

Generative AI looks like the perfect answer: "give me 50 shipping addresses" takes seconds. On Monday you saw that test data generation is one of the most common GenAI applications in QE, and on Tuesday you learned how to lock the output format and use few-shot examples. Today you will see the other side: AI-generated data is **fluent but not guaranteed to be correct**. A model can label an invalid phone number as valid, produce a card number that fails the payment provider's basic check, invent 30 February, or copy a real, famous address from its training data. It can also be oddly repetitive: ask for fifty names and you may get the same few patterns again and again.

This lesson teaches a workflow that keeps the speed and removes most of the risk: **the AI helps you think of the data; code makes the data; checks prove the data.** That matches the **Weekly Epic**, which is about using AI across the QA lifecycle **with human validation and responsible use**, and it prepares you for Friday, when your first QA agent will produce structured output that must be checked automatically. It also feeds **Project 2 (Test Automation Framework)** directly: a framework needs a clean, repeatable way to supply data to tests, and today's exercise asks you to generate and review test data for your Project 2 app.

> **Scope note.** This lesson is about the *data* that tests consume. Turning acceptance criteria into documented test cases was covered earlier today in *AI-Generated Test Cases*; plugging data into Playwright page objects comes later today in *AI-Assisted Automation Development*. The formal review checklist and correction log are in *Human Validation of AI Output*, and the full privacy discussion (what you may and may not paste into an AI tool) is in *Responsible Use of AI in QE*. Automatic, contract-based validation of an agent's output is covered on **Friday**.

---

## The Concept

### 1. What Is Test Data?

**Test data** is any data a test needs in order to run and to decide whether it passed. It comes in a few flavours:

| Kind of test data | What it is | Example from our e-commerce app |
|---|---|---|
| **Input data** | Values the test types, sends or uploads | The ZIP code `"73301"` typed into the shipping form |
| **Precondition (state) data** | Data that must already exist before the test starts | A user account with 5 failed login attempts |
| **Reference data** | Fixed lookup data the system relies on | The list of valid coupon codes; the list of US states |
| **Expected data** | The values the test compares against | "The total after SAVE10 on $80.00 is $72.00" |
| **Volume data** | Large amounts of data for performance or pagination | 10,000 products so search results span many pages |

A useful way to think about it: if a test case is a **recipe**, test data is the **ingredients**. A perfect recipe with the wrong ingredients still produces a bad meal, and you cannot tell whether the recipe was wrong or the ingredients were.

Notice that **expected data** is on the list. In Tuesday's *AI-Assisted Test Design* lesson you learned that an LLM is **not a test oracle**. The same applies to data: when an AI says "this row should be accepted", that label is a guess. It must be checked against the requirement.

### 2. Where Does Test Data Come From?

There are four main sources. Each has a place.

| Source | How it is made | Strengths | Weaknesses |
|---|---|---|---|
| **Production copy** | Copy real data from the live system | Very realistic, real volumes and oddities | Contains real personal data; often not allowed; large and slow to refresh |
| **Masked (anonymised) production data** | Copy production, then replace names, emails, cards and so on | Realistic shapes and volumes, less privacy risk | Masking can be incomplete; still needs approval; may break relationships |
| **Hand-crafted data** | A tester writes each row deliberately | Precise; every row has a purpose | Slow; limited by the tester's imagination; tedious at volume |
| **Synthetic data** | Generated by rules, scripts, libraries or AI | Fast; no real people; any volume; can target edge cases | Can be unrealistic; can be *wrong* if the generator is wrong |

**Synthetic data** simply means *data that was made up rather than collected from real users*. AI-generated data is one kind of synthetic data. The Faker library you will use in section 8 is another. Most modern teams use a **mix**: hand-crafted rows for the important boundaries, synthetic data for variety and volume, and (only where approved) masked production data for realism.

Why not just copy production? Imagine a screenshot from a failing checkout test, attached to a bug ticket that 40 people can see, showing a real customer's home address and the last four digits of their card. That is exactly the kind of leak that privacy laws exist to prevent. The rule of thumb in most companies is: **real personal data does not leave production without explicit approval and masking.** You will go deeper into this later today in *Responsible Use of AI in QE*.

### 3. Working Out the Data Needs of a Test, by Hand

Before you ask any AI for data, you need to know **what data you need**. Let us do this by hand for our running example, **US-310 Shipping address**:

> **US-310** As a shopper I want to enter a shipping address so my order is delivered.
> - AC1: Required fields: full name, street, city, state, ZIP code, phone.
> - AC2: ZIP code must be 5 digits (US only).
> - AC3: Phone must be 10 digits.
> - AC4: The address form should be fast and user-friendly.

AC4 is too vague to produce data from ("fast" and "user-friendly" have no numbers). Earlier today, in *AI-Assisted Requirements Analysis*, you saw that the right response is to raise a question with the product owner, not to invent a rule. So we will work only with AC1 to AC3.

Go field by field and ask the Week 3 questions: *What are the equivalence partitions? Where are the boundaries? What would an experienced tester try?*

**ZIP code (AC2: exactly 5 digits)**

| Category | Value | Why | Expected |
|---|---|---|---|
| Valid | `"73301"` | Typical 5-digit ZIP | accept |
| Valid (edge) | `"02110"` | Leading zero: breaks if a developer stores ZIP as a number | accept |
| Boundary | `"0211"` | 4 digits, one below the boundary | reject |
| Boundary | `"021100"` | 6 digits, one above the boundary | reject |
| Invalid | `"7330A"` | Letter inside | reject |
| Invalid | `""` | Empty (also AC1: required) | reject |
| Edge | `"١٢٣٤٥"` | Five digits in Arabic-Indic script, not 0-9 | reject (ask the PO to confirm) |

**Phone (AC3: exactly 10 digits)**

| Category | Value | Why | Expected |
|---|---|---|---|
| Valid | `"5125550147"` | 10 digits | accept |
| Boundary | `"512555014"` | 9 digits | reject |
| Boundary | `"51255501477"` | 11 digits | reject |
| Invalid | `"512-555-0147"` | Dashes: 12 characters, not 10 digits | reject (ask the PO: should the form strip dashes?) |

**Full name (AC1: required)**

| Category | Value | Why | Expected |
|---|---|---|---|
| Valid | `"Ana Silva"` | Typical | accept |
| Edge | `"Siobhan O'Brien-Nuñez"` | Apostrophe, hyphen and accented letter | accept |
| Invalid | `"   "` | Only spaces: "looks filled in" but is empty | reject |

Two things stand out from this exercise.

First, **a few rows do most of the work.** You do not need 500 addresses to test AC2; you need about seven well-chosen ZIP codes. Volume is useful for other goals (performance, pagination, variety), but for checking a rule, **purpose beats quantity**.

Second, **some rows raise questions** (the dashes in phone numbers, the non-ASCII digits). Good test data design surfaces gaps in the requirement, just as good test design does.

#### The "one change at a time" principle

Look at how the rows above are built: start from one **known-good base row** and change **exactly one field** per row. If the row with `"0211"` as the ZIP is rejected, you know the ZIP caused it, because everything else is valid. If you changed the ZIP *and* the phone in the same row and the form rejected it, you would not know which rule fired, or whether the ZIP rule works at all. This principle will shape the code in section 9.

### 4. Where AI Helps and Where It Hurts

Now bring the AI in. What is it actually good at here?

**AI is good at:**

- **Brainstorming categories and tricky values.** "What unusual inputs might break a name field?" gives you apostrophes, hyphens, accented characters, very long names, single-letter names, names in non-Latin scripts, leading and trailing spaces. Many testers would not think of all of these.
- **Realistic-looking variety.** Plausible street names, cities and product descriptions, in many styles.
- **Domain knowledge.** "US ZIP codes can start with 0", "February has 28 or 29 days", "payment providers publish special test card numbers".
- **Formatting.** Turning a list of ideas into CSV or JSON rows (Tuesday's format locking).

**AI is unreliable at:**

- **Labels.** Saying whether a row is valid or invalid. It might label `"(202) 555-0199"` as a valid 10-digit phone number because it *looks* like a phone number, even though it has 14 characters.
- **Counting.** You ask for 2 rows per category and get 1 in some categories and 3 in others.
- **Data with hidden rules.** Card numbers have a check digit; dates must exist in the calendar; emails must be unique in a users table; an order must belong to a user who exists. A model predicts text that *looks* right; it does not run these rules (Monday: next-token prediction).
- **Not using real data.** A model may reproduce real, well-known addresses, real company names or even real-looking personal details from its training data.
- **True randomness and spread.** LLM output is not a random sample. Ask for 50 names and you may get mostly common English names. At low temperature (Monday), you may get almost the same data every time; at high temperature, you may get different data every run, which makes failures hard to reproduce.
- **Volume.** Generating 10,000 rows through a chat window is slow, expensive and error-prone. Code does this better.

This leads to the core idea of the lesson:

> **The AI designs, code generates, checks prove.**
> Use AI for *ideas* (categories, tricky values, questions). Use *code* for volume and repeatability. Use *independent checks* to prove the data is right before any test depends on it.

### 5. Prompting for Test Data with Constraints

A weak data prompt looks like this:

```text
Give me some test addresses.
```

Recall Tuesday's *Specificity and Context* lesson: this prompt has no rules, no categories, no count, no format and no safety instructions. Here is a much stronger one, built in Python so that the field rules live in one place:

```python
# data_prompt.py -- build a constrained test data prompt and parse the reply
import json

FIELD_RULES = """\
full_name: required
street:    required
city:      required
state:     required
zip_code:  required, exactly 5 digits (US only)
phone:     required, exactly 10 digits"""

def build_data_prompt(rules: str, rows_per_category: int) -> str:
    return f"""You are a test data designer for an e-commerce web app.

Generate shipping address test data for the rules between the <rules> tags.

<rules>
{rules}
</rules>

Categories: VALID, INVALID, BOUNDARY, EDGE.
Generate {rows_per_category} rows per category.

Rules for you:
- Use obviously fictional people. Never use real people or real customer data.
- Use phone numbers in the 555-01xx fictional range (e.g. 5125550147).
- Each row must say which rule it targets and whether the form should accept it.

Return ONLY a JSON array. Each element has exactly these keys:
"id", "category", "targets_rule", "expected", "data"
where "expected" is "accept" or "reject" and "data" is an object
with the six address fields."""
```

Let us read it piece by piece.

- `FIELD_RULES` is a plain multi-line string holding the rules from US-310. The `"""\` at the start (a backslash right after the opening quotes) stops Python from putting an empty line at the top of the string. Keeping the rules in a variable means the prompt and, later, your validation code can use the **same** source of truth.
- `build_data_prompt` is an ordinary function that returns a string. The `f"""..."""` is an **f-string**: anything inside `{...}` is replaced by the value of that variable, so `{rules}` becomes the rules and `{rows_per_category}` becomes a number such as `2`.
- **Persona:** "You are a test data designer for an e-commerce web app."
- **Delimiters:** the rules sit between `<rules>` tags, so the model can tell rules apart from instructions (Tuesday).
- **Categories and count:** VALID, INVALID, BOUNDARY, EDGE, with a fixed number per category. This is what lets us *check* the count later.
- **Safety rules:** fictional people only, and phone numbers in the **555-01xx** range. In North America, numbers 555-0100 to 555-0199 are set aside for fictional use (films and TV use them), so they will not ring a real person if a test ever sends an SMS.
- **Traceability per row:** `targets_rule` and `expected`. Asking the model to say *which rule* each row targets makes its reasoning visible and reviewable.
- **Format locking:** "Return ONLY a JSON array" with exact keys (Tuesday's *Format Locking*). Structured output can be parsed and checked by code.

Since we never call a real model in this course's lessons, here is a deterministic stand-in. Add it to the same file:

```python
def fake_llm(prompt: str) -> str:
    """Deterministic stand-in for a model. ILLUSTRATIVE response only,
    with realistic mistakes planted on purpose."""
    return json.dumps([
        {"id": "TD-01", "category": "VALID", "targets_rule": "all fields valid",
         "expected": "accept",
         "data": {"full_name": "Ana Silva", "street": "12 Oak St", "city": "Austin",
                  "state": "TX", "zip_code": "73301", "phone": "5125550147"}},
        {"id": "TD-02", "category": "VALID", "targets_rule": "all fields valid",
         "expected": "accept",
         "data": {"full_name": "Ben Okafor", "street": "1600 Pennsylvania Ave NW",
                  "city": "Washington", "state": "DC", "zip_code": "20500",
                  "phone": "(202) 555-0199"}},
        {"id": "TD-03", "category": "INVALID", "targets_rule": "zip_code 5 digits",
         "expected": "reject",
         "data": {"full_name": "Chen Wei", "street": "4 Pine Rd", "city": "Boston",
                  "state": "MA", "zip_code": "0211", "phone": "6175550123"}},
        {"id": "TD-04", "category": "BOUNDARY", "targets_rule": "phone 10 digits",
         "expected": "accept",
         "data": {"full_name": "Eva Novak", "street": "1 Main St", "city": "Miami",
                  "state": "FL", "zip_code": "33101", "phone": "30555501100"}},
        {"id": "TD-05", "category": "EDGE", "targets_rule": "full_name characters",
         "expected": "accept",
         "data": {"full_name": "Siobhan O'Brien-Nuñez", "street": "77 Bay St",
                  "city": "Seattle", "state": "WA", "zip_code": "98101",
                  "phone": "2065550188"}},
        {"id": "TD-06", "category": "EDGE", "targets_rule": "zip_code 5 digits",
         "expected": "reject",
         "data": {"full_name": "Dana Levi", "street": "3 Lake Dr", "city": "Chicago",
                  "state": "IL", "zip_code": "١٢٣٤٥",
                  "phone": "3125550175"}},
    ])


if __name__ == "__main__":
    prompt = build_data_prompt(FIELD_RULES, rows_per_category=2)
    rows = json.loads(fake_llm(prompt))
    print(f"Rows received: {len(rows)}")
    for row in rows:
        print(row["id"], row["category"], row["expected"], "->", row["targets_rule"])
```

- `json.dumps(...)` turns a Python list of dictionaries into a JSON **string**, which is what a real model would send back. `json.loads(...)` does the opposite: it parses the string back into Python lists and dictionaries.
- `"١٢..."` is a Python **Unicode escape**: each `\uXXXX` is one character, here the Arabic-Indic digits one to five (١٢٣٤٥). Writing them as escapes makes the code readable in any editor.
- `if __name__ == "__main__":` means "run this block only when the file is run directly, not when another file imports it". We will import `fake_llm` from another script shortly, and we do not want the printing to happen then.

Running `python data_prompt.py` prints:

```text
Rows received: 6
TD-01 VALID accept -> all fields valid
TD-02 VALID accept -> all fields valid
TD-03 INVALID reject -> zip_code 5 digits
TD-04 BOUNDARY accept -> phone 10 digits
TD-05 EDGE accept -> full_name characters
TD-06 EDGE reject -> zip_code 5 digits
```

At a glance, this looks great: tidy IDs, categories, a nice international name, even an exotic ZIP code. Before reading on, review the six rows yourself against US-310. How many problems can you find?

### 6. Reviewing the AI's Data by Eye

Here is what a careful reviewer finds in the six illustrative rows:

| Row | What is wrong | Why it matters |
|---|---|---|
| **Counts** | We asked for 2 rows per category. VALID has 2, EDGE has 2, but INVALID and BOUNDARY have only 1 each. | Missing coverage that nobody notices unless they count. |
| **TD-02** | Phone `"(202) 555-0199"` is labelled *accept*, but AC3 says 10 digits and this value has 14 characters. | A wrong `expected` label becomes a wrong test: the test will "fail" when the product correctly rejects it, or the label will hide a real bug. |
| **TD-02** | `1600 Pennsylvania Ave NW, Washington, DC 20500` is the real address of the White House. | The model reproduced a real, famous address from its training data, breaking our "fictional" rule. Harmless here, but the same habit could reproduce a real person's details. |
| **TD-04** | The phone `"30555501100"` has 11 digits, so it should be *reject*, but it is labelled *accept*. It also falls outside the 555-01xx range. | A boundary row with the wrong label is worse than no boundary row. |
| **TD-05** | Looks correct: an apostrophe, a hyphen and `ñ`. | A good, useful edge case. |
| **TD-06** | Looks correct: five non-ASCII digits, labelled *reject*. | A *very* good edge case, which we will see finds a real bug in section 9. |

Two lessons come out of this table.

1. **The AI added real value.** TD-05 and TD-06 are exactly the sort of inputs a tired human forgets.
2. **The AI also added real risk.** One third of the rows have a wrong label, and the count is off. If we had copied these rows straight into a test suite, we would have produced two misleading tests.

Reviewing by eye works for 6 rows. It does not work for 600. So we write checks.

### 7. Validating AI-Generated Data with Independent Checks

An **independent check** is code written from the **requirement**, not from the AI's output and not from the product's code. If the AI's label and our check disagree, a human looks at the row. Save this next to `data_prompt.py`:

```python
# check_data.py -- independent checks on AI-generated test data
import json
import re
from collections import Counter

from data_prompt import FIELD_RULES, build_data_prompt, fake_llm

REQUIRED = ["full_name", "street", "city", "state", "zip_code", "phone"]
CATEGORIES = {"VALID", "INVALID", "BOUNDARY", "EDGE"}


def spec_expectation(data: dict) -> str:
    """Our own oracle, written from the acceptance criteria of US-310.
    [0-9] (not \\d) so that only ASCII digits 0-9 count."""
    for field in REQUIRED:
        if not str(data.get(field, "")).strip():
            return "reject"
    if not re.fullmatch(r"[0-9]{5}", data["zip_code"]):
        return "reject"
    if not re.fullmatch(r"[0-9]{10}", data["phone"]):
        return "reject"
    return "accept"


def is_fictional_phone(phone: str) -> bool:
    """True if the number is in the 555-0100 to 555-0199 fictional range."""
    digits = re.sub(r"[^0-9]", "", phone)
    return len(digits) == 10 and digits[3:6] == "555" and digits[6:8] == "01"


def check_rows(rows: list[dict], rows_per_category: int) -> list[str]:
    problems = []
    counts = Counter(row.get("category") for row in rows)
    for category in sorted(CATEGORIES):
        if counts[category] != rows_per_category:
            problems.append(f"{category}: expected {rows_per_category} rows, got {counts[category]}")
    for row in rows:
        rid = row.get("id", "?")
        if row.get("expected") not in {"accept", "reject"}:
            problems.append(f"{rid}: 'expected' must be accept or reject")
            continue
        oracle = spec_expectation(row["data"])
        if row["expected"] != oracle:
            problems.append(f"{rid}: AI says {row['expected']}, rules say {oracle}")
        if not is_fictional_phone(row["data"].get("phone", "")):
            problems.append(f"{rid}: phone is not in the fictional 555-01xx range")
    return problems


rows = json.loads(fake_llm(build_data_prompt(FIELD_RULES, 2)))
for problem in check_rows(rows, rows_per_category=2):
    print("PROBLEM:", problem)
```

Output:

```text
PROBLEM: BOUNDARY: expected 2 rows, got 1
PROBLEM: INVALID: expected 2 rows, got 1
PROBLEM: TD-02: AI says accept, rules say reject
PROBLEM: TD-04: AI says accept, rules say reject
PROBLEM: TD-04: phone is not in the fictional 555-01xx range
```

The checks found every mechanical problem from section 6. Let us walk through the code.

**`spec_expectation(data)`** is our **mini oracle**. It answers "should the form accept this row?" using only the acceptance criteria:

- `str(data.get(field, ""))` reads a field safely. `dict.get(key, default)` returns the default (`""`) instead of crashing when the key is missing; `str(...)` makes sure we have text even if the AI sent a number (for example `73301` without quotes, a common AI slip that also drops leading zeros).
- `.strip()` removes spaces at both ends. `"   ".strip()` is `""`, and an empty string is "falsy" in Python, so `not "".strip()` is `True` and the row is rejected. This is how whitespace-only values count as empty.
- `re.fullmatch(r"[0-9]{5}", value)` comes from Python's `re` (regular expressions) module. `[0-9]` means "one character from 0 to 9", `{5}` means "exactly five of them", and **`fullmatch`** means the *whole* string must match, not just part of it. The `r"..."` prefix makes a **raw string**, so backslashes are not treated specially.
- Why `[0-9]` and not `\d`? In Python 3, `\d` matches **any Unicode digit**, including the Arabic-Indic digits in TD-06. `[0-9]` matches only the ten ASCII digits. This tiny detail is exactly the kind of thing that hides defects, as you will see in section 9.

**`is_fictional_phone(phone)`**:

- `re.sub(r"[^0-9]", "", phone)` replaces every character that is **not** a digit (`[^...]` means "not these") with nothing, leaving only digits. `"(202) 555-0199"` becomes `"2025550199"`.
- `digits[3:6]` is a **slice**: characters at positions 3, 4 and 5 (the exchange, `555`). `digits[6:8]` is positions 6 and 7 (`01`). Together they check the 555-01xx pattern.

**`check_rows(rows, rows_per_category)`**:

- `Counter(...)` from the `collections` module counts how many times each category appears, like a tally sheet. `counts["BOUNDARY"]` gives the tally; a category that never appeared gives `0` rather than an error.
- For every row, we compare the AI's `expected` with our oracle. A mismatch is reported, not silently fixed: a **human** decides whether the AI is wrong or our understanding of the requirement is wrong.

> **Important:** these checks do not replace a human. Look again at the output: nothing flagged the White House address in TD-02. A script cannot easily tell a famous real address from a made-up one. That is why the formal human review (covered later today in *Human Validation of AI Output*) still matters. Automated checks catch the *mechanical* mistakes cheaply so humans can spend their attention on the *judgement* mistakes.

Notice also that the checks are **simple**. That is deliberate: a check that is as complicated as the system under test will have its own bugs. On **Friday** you will build more formal validation scripts for agent output; today's small, hand-written checks are the foundation for that.

### 8. "AI Designs, Code Generates": Reproducible Data with Seeds and Faker

You now have a handful of good, reviewed edge cases. But sometimes you also need **volume and variety**: 200 valid addresses for a pagination test, or a realistic mix of customers for a demo environment. Asking an AI for 200 rows is the wrong tool. Code is faster, cheaper and, crucially, **reproducible**.

**Reproducible** means: run the generator again and you get *exactly* the same data. Why does this matter so much? Imagine a test fails on the CI server overnight with "address row 137 rejected". If the data is different every run, you cannot get row 137 back to investigate. If the data is reproducible, you re-run the generator and row 137 is there, identical.

The trick is a **seed**. Computers do not produce truly random numbers; they use a **pseudo-random number generator (PRNG)**, a formula that produces a sequence of numbers that *looks* random. The seed is the starting point of that formula. **Same seed, same sequence.** Think of a shuffled deck of cards where you write down how you shuffled it: anyone who repeats your shuffle gets the same order.

**Faker** is a popular Python library that generates fake but realistic-looking names, addresses, emails, company names and much more. Install it with `pip install Faker`. Here is a generator that combines Faker with Python's own `random` module:

```python
# generate_addresses.py -- reproducible synthetic data with Faker + a seed
import random

from faker import Faker

SEED = 2026


def make_valid_addresses(count: int, seed: int = SEED) -> list[dict]:
    fake = Faker("en_US")
    fake.seed_instance(seed)          # same seed -> same fake people
    rng = random.Random(seed)         # our own seeded random generator
    rows = []
    for i in range(1, count + 1):
        area_code = rng.choice(["212", "312", "415", "512", "617"])
        rows.append({
            "id": f"VALID-{i:03d}",
            "full_name": fake.name(),
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "phone": f"{area_code}55501{rng.randint(0, 99):02d}",  # fictional range
        })
    return rows


if __name__ == "__main__":
    first_run = make_valid_addresses(3)
    second_run = make_valid_addresses(3)
    for row in first_run:
        print(row)
    print("Same data both runs:", first_run == second_run)
    print("Different seed, same data:", make_valid_addresses(3, seed=7) == first_run)
```

Output (with Faker 40.43.0 and Python 3.13):

```text
{'id': 'VALID-001', 'full_name': 'Jonathan Hunt', 'street': '99869 Potter Radial', 'city': 'Allenland', 'state': 'DE', 'zip_code': '38150', 'phone': '2125550140'}
{'id': 'VALID-002', 'full_name': 'Joanna Briggs', 'street': '536 Bailey Knolls Suite 815', 'city': 'New Amandaport', 'state': 'NH', 'zip_code': '18967', 'phone': '6175550165'}
{'id': 'VALID-003', 'full_name': 'Michele Ray', 'street': '557 Davis Prairie', 'city': 'Camachochester', 'state': 'NY', 'zip_code': '98824', 'phone': '2125550128'}
Same data both runs: True
Different seed, same data: False
```

Line by line:

- `Faker("en_US")` creates a generator for the United States **locale** (US-style names, states and ZIP codes). Faker supports many locales, such as `"de_DE"` or `"ja_JP"`, which is useful for international data.
- `fake.seed_instance(seed)` seeds *this* Faker object. Every call after it (`fake.name()`, `fake.city()` and so on) follows a fixed sequence.
- `random.Random(seed)` creates our *own* seeded generator object, `rng`. Using a separate object (instead of the global `random.seed(...)`) means other code that uses `random` cannot disturb our sequence.
- `rng.choice([...])` picks one item from the list; `rng.randint(0, 99)` picks a whole number from 0 to 99 inclusive.
- `f"VALID-{i:03d}"` formats `i` as a 3-digit number with leading zeros (`001`, `002`, ...). `{...:02d}` does the same with 2 digits, so `5` becomes `05` and the phone always has 10 digits.
- We build the phone number ourselves instead of using `fake.phone_number()`, because Faker phone numbers come in many formats (with dashes, brackets, extensions) and are not in the fictional 555-01xx range. **You decide the rules; the library fills in variety.**
- `first_run == second_run` compares two lists of dictionaries value by value. `True` proves reproducibility; a different seed gives different data.

Three honest caveats:

1. **"Same seed, same data" holds for the same library versions.** Faker's documentation warns that results can change between versions, so pin the version (for example `Faker==40.43.0` in `requirements.txt`) if your tests depend on exact values. Python's own `random` module only guarantees the sequence of `random()` across versions, not every helper. Your names may differ from the output above if your versions differ.
2. **Realistic-looking is not real.** Look at row 1: a ZIP code of `38150` (a Mississippi-style ZIP) with the state `DE` (Delaware) and an invented city. Each field is valid *on its own*, but the combination does not exist. That is fine for testing "is the ZIP 5 digits?", but useless if the app checks addresses with a real address-verification service. Know what your data is for.
3. **Faker is not a test oracle either.** It produces plausible values, not labelled ones. Expected outcomes still come from the requirement.

So where does the AI fit? Use it to **design the generator**: "What fields does a US shipping address need? What edge-case values should I add? What locales should I include for an international store?" Then you write (or ask the AI to help you write, Tuesday's *AI-Assisted Coding and Debugging*) a seeded generator, and you review and run it. The AI's creativity goes into the **design**; the code gives you **volume and repeatability**.

### 9. Storing Test Data as a Fixture and Driving pytest With It

Now let us put everything together and actually **use** the data against code. Here is a simplified version of the shipping address validator for US-310, the system under test:

```python
# address.py -- the system under test for US-310 (simplified)
REQUIRED_FIELDS = ["full_name", "street", "city", "state", "zip_code", "phone"]


def validate_address(address: dict) -> list[str]:
    """Return a list of error messages. An empty list means the address is valid."""
    errors = []
    for field in REQUIRED_FIELDS:
        value = address.get(field, "")
        if not str(value).strip():
            errors.append(f"{field} is required")
    zip_code = str(address.get("zip_code", "")).strip()
    if zip_code and not (len(zip_code) == 5 and zip_code.isdigit()):
        errors.append("zip_code must be 5 digits")
    phone = str(address.get("phone", "")).strip()
    if phone and not (len(phone) == 10 and phone.isdigit()):
        errors.append("phone must be 10 digits")
    return errors
```

Next, a script that builds the data set using the **one change at a time** principle from section 3 and saves it as a **JSON fixture**. A **fixture file** is simply a data file that tests load; storing data outside the test code means testers can review and extend the data without touching Python.

```python
# build_dataset.py -- one base row + one change per row, saved as a JSON fixture
import json

BASE = {"full_name": "Ana Silva", "street": "12 Oak St", "city": "Austin",
        "state": "TX", "zip_code": "73301", "phone": "5125550147"}

# (case id, field to change, new value, expected outcome, why)
# Ideas brainstormed with AI; every expected outcome confirmed by a human against US-310.
VARIATIONS = [
    ("ADDR-01", None,        None,           "accept", "baseline valid address"),
    ("ADDR-02", "zip_code",  "0211",         "reject", "BVA: 4 digits"),
    ("ADDR-03", "zip_code",  "021100",       "reject", "BVA: 6 digits"),
    ("ADDR-04", "zip_code",  "02110",        "accept", "leading zero kept"),
    ("ADDR-05", "zip_code",  "7330A",        "reject", "letter in ZIP"),
    ("ADDR-06", "zip_code",  "١٢٣٤٥", "reject", "non-ASCII digits"),
    ("ADDR-07", "phone",     "512555014",    "reject", "BVA: 9 digits"),
    ("ADDR-08", "phone",     "51255501477",  "reject", "BVA: 11 digits"),
    ("ADDR-09", "phone",     "512-555-0147", "reject", "dashes (AC3 says digits)"),
    ("ADDR-10", "full_name", "   ",          "reject", "whitespace only"),
    ("ADDR-11", "full_name", "Siobhan O'Brien-Nuñez", "accept", "apostrophe, hyphen, accent"),
    ("ADDR-12", "city",      "",             "reject", "required field empty"),
]


def build_cases() -> list[dict]:
    cases = []
    for case_id, field, value, expected, why in VARIATIONS:
        data = dict(BASE)                 # copy, so BASE is never changed
        if field is not None:
            data[field] = value
        cases.append({"id": case_id, "why": why, "expected": expected, "data": data})
    return cases


if __name__ == "__main__":
    cases = build_cases()
    with open("address_cases.json", "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(cases)} cases to address_cases.json")
```

Running it prints `Wrote 12 cases to address_cases.json`. Key details:

- `VARIATIONS` is a list of **tuples**. Each tuple has five values, and `for case_id, field, value, expected, why in VARIATIONS:` **unpacks** them into five named variables on every loop.
- `dict(BASE)` makes a **copy** of the base row. Without the copy, `data[field] = value` would change `BASE` itself, and every later row would inherit the previous row's change: a classic, confusing data bug.
- The comment says *who* decided the expected outcomes: the ideas came from AI brainstorming, but the labels were confirmed by a human. Recording this is a small but valuable habit (more on this later today in *Human Validation of AI Output* and *Responsible Use of AI in QE*).
- `json.dump(..., indent=2, ensure_ascii=False)` writes nicely indented JSON. `ensure_ascii=False` keeps characters like `ñ` and `١` readable in the file instead of turning them into `\u` escapes; `encoding="utf-8"` makes sure the file can store them.

The start of `address_cases.json` looks like this:

```json
[
  {
    "id": "ADDR-01",
    "why": "baseline valid address",
    "expected": "accept",
    "data": {
      "full_name": "Ana Silva",
      "street": "12 Oak St",
      "city": "Austin",
      "state": "TX",
      "zip_code": "73301",
      "phone": "5125550147"
    }
  },
  ...
]
```

Finally, the data-driven test (Week 4's pytest, Tuesday's `parametrize`):

```python
# test_address.py -- data-driven tests that read the JSON fixture
import json
from pathlib import Path

import pytest

from address import validate_address

CASES = json.loads(Path(__file__).with_name("address_cases.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_validate_address(case):
    errors = validate_address(case["data"])
    accepted = errors == []
    assert accepted == (case["expected"] == "accept"), f"{case['why']}: errors={errors}"
```

- `Path(__file__).with_name("address_cases.json")` builds the path to the JSON file **next to the test file**, so the test works no matter which folder you run pytest from. `__file__` is the path of the current Python file.
- `@pytest.mark.parametrize("case", CASES, ids=[...])` runs the test function once per item in `CASES`, passing each item in as `case`. The `ids` list gives each run a readable name (`ADDR-01`, `ADDR-02`, ...) in the pytest output.
- `accepted = errors == []` is `True` when the validator returned no errors.
- The `assert` compares "was it accepted?" with "should it be accepted?". The text after the comma is the **assertion message**, shown only on failure, so the report tells you *why* that row exists.

Run `pytest -q test_address.py`:

```text
FAILED test_address.py::test_validate_address[ADDR-06] - AssertionError: non-...
1 failed, 11 passed in 0.05s
```

with this detail for the failure:

```text
E       AssertionError: non-ASCII digits: errors=[]
```

**The AI's edge case found a real defect.** `validate_address` uses `zip_code.isdigit()`, and in Python `"١٢٣٤٥".isdigit()` is `True`, because `isdigit()` accepts digits from *any* writing system. The validator therefore accepts a ZIP code that no US postal system would understand, and a downstream system (shipping labels, tax calculation) may crash or mis-route the parcel. The fix is to also require ASCII:

```python
    if zip_code and not (len(zip_code) == 5 and zip_code.isascii() and zip_code.isdigit()):
```

With that change (and the same fix for the phone), all 12 tests pass. Notice the shape of what happened: a human-reviewed, AI-suggested data value in a fixture file exposed a bug that 11 "normal" rows did not. This is test data doing its job.

### 10. Data With Hidden Rules: Cards, Dates and Relationships

Some data has rules that are invisible on the surface. These are where AI-generated data goes wrong most often, because the model is predicting what the value *looks like*, not computing it.

#### Payment card numbers and the Luhn check

Card numbers are not random. The last digit is a **check digit** calculated with the **Luhn algorithm** (also called "mod 10"), which catches most typing mistakes. A checkout form or payment provider usually rejects a number that fails Luhn before doing anything else. If AI-generated card numbers fail Luhn, your "valid payment" tests will fail for the wrong reason.

Let us do the Luhn check **by hand** on the textbook example `79927398713`:

1. Write the digits from **right to left**: 3, 1, 7, 8, 9, 3, 7, 2, 9, 9, 7.
2. Double **every second digit**, starting with the second from the right: 1→2, 8→16, 3→6, 2→4, 9→18.
3. If a doubled value is more than 9, subtract 9: 16→7, 18→9. (Same as adding its two digits: 1+6=7.)
4. Add everything: 3 + 2 + 7 + 7 + 9 + 6 + 7 + 4 + 9 + 9 + 7 = **70**.
5. If the total ends in 0 (total % 10 == 0), the number passes. 70 does, so it is Luhn-valid.

The same in Python:

```python
# luhn.py -- check card numbers an AI suggested for payment tests
def luhn_valid(number: str) -> bool:
    digits = [int(ch) for ch in number if ch.isdigit()]
    total = 0
    # Walk from the rightmost digit; double every second digit.
    for position, digit in enumerate(reversed(digits)):
        if position % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


ai_suggested = {
    "79927398713": "textbook example",
    "4242424242424242": "Visa test card (from payment provider docs)",
    "5555555555554444": "Mastercard test card (from payment provider docs)",
    "4242424242424241": "AI said: 'valid Visa'",
    "4532015112830367": "AI said: 'another valid Visa'",
}
for number, note in ai_suggested.items():
    print(f"{number:<17} luhn_valid={luhn_valid(number)!s:<5}  # {note}")
```

Output:

```text
79927398713       luhn_valid=True   # textbook example
4242424242424242  luhn_valid=True   # Visa test card (from payment provider docs)
5555555555554444  luhn_valid=True   # Mastercard test card (from payment provider docs)
4242424242424241  luhn_valid=False  # AI said: 'valid Visa'
4532015112830367  luhn_valid=False  # AI said: 'another valid Visa'
```

- `[int(ch) for ch in number if ch.isdigit()]` is a **list comprehension**: it builds a list of integers from the digit characters, skipping spaces or dashes.
- `reversed(digits)` walks the list from the right; `enumerate(...)` gives each digit its position (0, 1, 2, ...). Odd positions (`position % 2 == 1`) are "every second digit from the right".
- `f"{number:<17}"` pads the number to 17 characters, left-aligned, so the columns line up; `!s` converts `True`/`False` to text before padding.

The two "valid Visa" numbers that the (illustrative) AI produced both fail. But here is the deeper point: **even a Luhn-valid number invented by an AI might belong to a real person's card.** Never use invented card numbers. Payment providers publish official **test card numbers** (for example Stripe's `4242 4242 4242 4242` for Visa) that work only in their test mode. Use those, from the provider's own documentation, and treat any card number from an AI as suspect.

#### Dates, uniqueness and referential integrity

When an AI generates several related tables (users, orders, coupons), three more hidden rules appear:

- **Real calendar dates.** 30 February does not exist. Neither does 31 April.
- **Uniqueness.** Two users cannot share an email if email is the login name (US-101).
- **Referential integrity.** Every order's `user_id` must point to a user who exists. "Referential" means one record *refers* to another; "integrity" means those references are not broken. A database with foreign keys would refuse to load broken data, which would make your test setup fail before a single test runs.

```python
# integrity.py -- relationships between AI-generated tables must hold
from datetime import date

users = [
    {"user_id": 1, "email": "ana.silva@example.com", "failed_attempts": 0},
    {"user_id": 2, "email": "ben.okafor@example.com", "failed_attempts": 5},
    {"user_id": 3, "email": "ana.silva@example.com", "failed_attempts": 0},
]
orders = [
    {"order_id": 101, "user_id": 1, "subtotal": "49.99", "coupon": "SAVE10", "placed_on": "2026-03-14"},
    {"order_id": 102, "user_id": 2, "subtotal": "50.00", "coupon": "SAVE10", "placed_on": "2026-02-30"},
    {"order_id": 103, "user_id": 9, "subtotal": "120.00", "coupon": None, "placed_on": "2026-04-01"},
]


def check_integrity(users, orders) -> list[str]:
    problems = []
    emails = [u["email"] for u in users]
    for email in sorted(set(emails)):
        if emails.count(email) > 1:
            problems.append(f"duplicate email {email} (emails must be unique)")
    known_ids = {u["user_id"] for u in users}
    for o in orders:
        if o["user_id"] not in known_ids:
            problems.append(f"order {o['order_id']}: user_id {o['user_id']} does not exist")
        try:
            date.fromisoformat(o["placed_on"])
        except ValueError:
            problems.append(f"order {o['order_id']}: impossible date {o['placed_on']}")
    return problems


for problem in check_integrity(users, orders):
    print("PROBLEM:", problem)
```

Output:

```text
PROBLEM: duplicate email ana.silva@example.com (emails must be unique)
PROBLEM: order 102: impossible date 2026-02-30
PROBLEM: order 103: user_id 9 does not exist
```

- `set(emails)` removes duplicates; `emails.count(email)` counts how often each email appears in the original list.
- `{u["user_id"] for u in users}` is a **set comprehension**: a set of all user IDs, which makes `in` checks fast.
- `date.fromisoformat("2026-02-30")` tries to build a real date and raises `ValueError` if the date does not exist. The `try ... except ValueError:` block catches that error and records a problem instead of crashing.
- Note the emails use **`example.com`**. Domains like `example.com`, `example.org` and anything ending in `.test` are reserved for documentation and testing, so a test email can never reach a real inbox. Tell the AI to use them, and check that it did.
- The subtotals are strings like `"49.99"` on purpose. Money in tests should be handled as `Decimal`, not `float` (Tuesday's *AI-Assisted Test Design*), and storing it as text in fixtures keeps it exact until your test converts it.

Also notice what this little data set is good for: order 101 (`49.99` with SAVE10) and the corrected order 102 (`50.00` with SAVE10) are exactly the boundary pair for **US-205**. Well-designed data often serves several tests at once.

### 11. State and Time: Precondition Data

Some of the most valuable test data is not something you type; it is a **state** the system must be in before the test starts. **US-101 AC3** says: *after 5 consecutive failed attempts the account is locked for 15 minutes.* To test it you need accounts in several states:

| Account state | failed_attempts | locked_until | What it tests |
|---|---|---|---|
| Fresh | 0 | none | Normal login |
| One short of lockout | 4 | none | The 5th failure should lock (boundary) |
| Locked | 5 | now + 15 min | Login refused even with the correct password |
| About to unlock | 5 | now + 1 s | Boundary of the 15-minute window |
| Lock expired | 5 | now − 1 s | Login allowed again |

A very common AI mistake here is to **hard-code timestamps**: `"locked_until": "2025-06-01T10:15:00"`. That row is "locked" on the day it was written and "expired" forever after, so the test silently changes meaning. Precondition data involving time should be **relative to now**:

```python
# lockout_states.py -- time-relative test data for US-101 AC3
from datetime import datetime, timedelta


def lockout_accounts(now: datetime) -> list[dict]:
    """Accounts in each interesting state, relative to 'now'."""
    return [
        {"email": "fresh@example.com",   "failed_attempts": 0, "locked_until": None},
        {"email": "four@example.com",    "failed_attempts": 4, "locked_until": None},
        {"email": "locked@example.com",  "failed_attempts": 5,
         "locked_until": now + timedelta(minutes=15)},
        {"email": "almost@example.com",  "failed_attempts": 5,
         "locked_until": now + timedelta(seconds=1)},
        {"email": "expired@example.com", "failed_attempts": 5,
         "locked_until": now - timedelta(seconds=1)},
    ]


now = datetime(2026, 10, 21, 9, 0, 0)        # fixed 'now' so the output is repeatable
for account in lockout_accounts(now):
    until = account["locked_until"]
    locked = until is not None and until > now
    print(f"{account['email']:<20} attempts={account['failed_attempts']}  locked={locked}")
```

Output:

```text
fresh@example.com    attempts=0  locked=False
four@example.com     attempts=4  locked=False
locked@example.com   attempts=5  locked=True
almost@example.com   attempts=5  locked=True
expired@example.com  attempts=5  locked=False
```

- `timedelta(minutes=15)` is a length of time; adding it to a `datetime` gives a new `datetime` 15 minutes later.
- The function takes `now` as a **parameter** instead of calling `datetime.now()` inside. This makes it testable: in the lesson we pass a fixed time so the output never changes; in a real test setup you would pass `datetime.now()`. Passing time in, rather than reading the clock deep inside the code, is a habit that makes time-based tests much less flaky.
- `until is not None and until > now` checks "there is a lock and it is in the future". Python stops evaluating at the first `False`, so `until > now` is never tried when `until` is `None`.

### 12. Volume, Variety and Fairness of Data

Three last considerations before we pull the workflow together.

**Volume.** For performance or pagination tests you may need thousands of rows. Generate them with seeded code (section 8), never by asking an AI for thousands of rows in a chat. A loop that makes 10,000 Faker rows takes well under a second; a chat model generating 10,000 rows is slow, costly and will make mistakes you cannot review.

**Variety (diversity).** Real shoppers have short names and very long names, names with apostrophes, accents and hyphens, names in non-Latin scripts, and single names with no surname. Addresses have apartment numbers, PO boxes and very long street names. If your data contains only `"John Smith, 123 Main St"`, your tests will pass while real customers cannot check out. AI is genuinely helpful for widening variety ("list name formats from different cultures that a name field should support"), and Faker's many locales help too. Ask yourself: *who would be unable to use this form, and does my data include them?* This connects to fairness, which you will meet again later today in *Responsible Use of AI in QE*.

**Privacy.** Everything in this lesson used fictional data: invented people, `example.com` emails, 555-01xx phones and the payment provider's official test cards. Never paste real customer records into a public AI tool to "make more like these", and never ask an AI to "make this look like real customers from our database". Your company's rules on approved AI tools and data classification come first. The detailed guidance is later today in *Responsible Use of AI in QE*.

### 13. The Complete Workflow

Here is the whole process in one place. Use it for your exercise this afternoon.

1. **Know the rules.** Read the acceptance criteria. Mark vague ones (like US-310 AC4) as questions, not data.
2. **Design by hand first.** For each field, list partitions, boundaries and edge values. Use "one change at a time" from a valid base row.
3. **Ask the AI to widen your list.** Give it the rules in delimiters, the categories, the count, the safety rules (fictional people, `example.com`, 555-01xx, official test cards) and a locked JSON format with `targets_rule` and `expected` per row. Ask "what edge values have I missed?"
4. **Check mechanically.** Run independent checks written from the requirement: counts, labels versus your mini oracle, formats, Luhn, real dates, uniqueness, referential integrity.
5. **Review by human judgement.** Look for real-looking personal data, unrealistic combinations and missing variety. Confirm or correct every `expected` label, and note who confirmed it.
6. **Generate volume with seeded code.** Use Faker and `random.Random(seed)`; pin library versions.
7. **Store data as fixtures.** JSON or CSV files next to the tests, reviewed like code (in Git, with pull requests).
8. **Drive tests from the fixtures.** `@pytest.mark.parametrize` with readable IDs and assertion messages that explain each row.

Steps 1, 2, 4, 5 and 8 are yours. Step 3 is where AI saves time. Steps 6 and 7 are ordinary good engineering.

### 14. Connecting to Project 2

In **Project 2 (Test Automation Framework)** your framework will need a clean way to supply data to many tests. A good starting structure is:

```text
project2/
  data/
    addresses.json          # hand-designed + AI-suggested, human-reviewed rows
    lockout_accounts.py     # time-relative precondition data
    generate_addresses.py   # seeded Faker generator for volume
  checks/
    check_data.py           # independent checks, run before tests use the data
  tests/
    test_address.py         # data-driven tests reading data/addresses.json
```

In today's exercise you will generate test data for your Project 2 app with AI, run checks like the ones in this lesson, and **document every correction** you make to the AI's output (what was wrong, how you found it, what you changed). Keep that record: it is your evidence that the AI was used responsibly, and it feeds directly into the review practice you will learn later today in *Human Validation of AI Output*. On **Friday**, when your first QA agent produces structured output, you will see how checks like these grow into proper validation scripts.

---

## Practice Exercises

1. **Data needs by hand.** For **US-205 Apply coupon at checkout**, write a table of test data (subtotal, code, expected result, why) covering AC1 to AC4. Include the boundary values around $50.00 with a step of $0.01, an unknown code, a code with different letter case (mark as a question for the PO), and a second coupon on the same order.
2. **Write the prompt.** Adapt `build_data_prompt` to US-205. Include the rules in `<rules>` tags, the categories, a count per category, the safety rules and a locked JSON format with `targets_rule` and `expected`.
3. **Plant and catch mistakes.** Write your own `fake_llm` response for US-205 with three planted mistakes (for example a wrong label on 49.99, a missing category and a float total like `49.999`). Write a `check_rows` function that catches all three.
4. **Reproducibility.** Change `make_valid_addresses` to accept a `locale` parameter and generate 5 addresses for `"en_GB"`. Run it twice and confirm the output is identical. What breaks if you feed UK postcodes into `validate_address`, and is that a defect or a correct rejection under US-310?
5. **Hidden rules.** Extend `check_integrity` so it also flags any order with `coupon == "SAVE10"` whose subtotal is under `"50.00"` (compare with `Decimal`). Which order in the example data does it flag, and is that row *wrong data* or a *useful negative test*? Explain your answer.
6. **Find the bug.** Add two rows to `VARIATIONS` that use non-ASCII digits in the **phone** field and an `int` (not a string) for the ZIP code. Run the tests against the original `address.py`. What happens, and what does it tell you about the AI's habit of dropping quotes around numbers?

---

## Knowledge Check

1. Name three sources of test data and one weakness of each.
2. What does "one change at a time" mean, and why does it make failures easier to diagnose?
3. In the illustrative AI output, what was wrong with TD-02, and which problem did the automated checks **not** catch?
4. Why does `spec_expectation` use the regular expression `[0-9]` instead of `\d`?
5. What is a seed, and why do reproducible data generators matter when a test fails overnight on CI?
6. Why should you never use card numbers invented by an AI, even if they pass the Luhn check?
7. What is referential integrity? Give an example of AI-generated data that breaks it.
8. Why is `"locked_until": "2025-06-01T10:15:00"` a poor piece of precondition data, and how should it be written instead?
9. Complete the sentence: "The AI ______, code ______, checks ______."

<details>
<summary>Answers</summary>

1. Any three of: **production copy** (contains real personal data; often not allowed), **masked production data** (masking can be incomplete or break relationships), **hand-crafted data** (slow and limited at volume), **synthetic data** (can be unrealistic or wrong if the generator is wrong).
2. Start from a known-valid base row and change exactly one field per row. If the row is rejected, only that field can be the reason, so you know which rule fired.
3. Its phone `"(202) 555-0199"` is not 10 digits, yet it was labelled *accept*. The checks caught that, but they did **not** catch that the address is the real address of the White House; spotting real-looking data needs human review.
4. In Python 3, `\d` matches any Unicode digit (including Arabic-Indic digits), while `[0-9]` matches only ASCII 0-9, which is what a US ZIP code allows.
5. A seed is the starting value of a pseudo-random number generator; the same seed gives the same sequence. If the data is reproducible, you can regenerate exactly the row that failed and investigate it.
6. An invented number might belong to a real person's card, and it may fail the provider's checks. Use the payment provider's official test card numbers, which only work in test mode.
7. Records that refer to other records must point to ones that exist. Example: an order with `user_id` 9 when no user 9 exists.
8. It is hard-coded, so the account is "locked" only on the day the data was written and "expired" afterwards; the test silently changes meaning. Write it relative to now, for example `now + timedelta(minutes=15)`, with `now` passed in as a parameter.
9. "The AI **designs**, code **generates**, checks **prove**."

</details>

---

## Glossary

- **Test data:** Any data a test needs to run and to decide whether it passed (inputs, preconditions, reference data, expected values, volume data).
- **Synthetic data:** Data that is generated (by rules, scripts, libraries or AI) rather than collected from real users.
- **Masked (anonymised) data:** Production data in which personal details have been replaced or hidden.
- **Precondition (state) data:** Data that must exist before a test starts, such as a locked account.
- **Fixture file:** A data file (JSON, CSV) stored with the tests and loaded by them.
- **One change at a time:** Building test rows from a valid base row by changing exactly one field per row.
- **Independent check:** Validation code written from the requirement, not from the AI's output or the product's code.
- **Pseudo-random number generator (PRNG):** A formula that produces a random-looking but repeatable sequence of numbers.
- **Seed:** The starting value of a PRNG; the same seed gives the same sequence.
- **Reproducible data:** Data that comes out identical every time the generator runs with the same seed and versions.
- **Faker:** A Python library that generates realistic-looking fake data such as names, addresses and emails, in many locales.
- **Luhn algorithm (mod 10):** The check-digit formula used by payment card numbers to catch typing mistakes.
- **Test card number:** A card number published by a payment provider that works only in its test mode.
- **Referential integrity:** The property that every reference between records (such as an order's `user_id`) points to a record that exists.
- **Reserved test domain:** A domain such as `example.com` that is set aside for documentation and testing, so it never reaches a real inbox.

---

## Summary

- Test data is the "ingredients" of a test: inputs, preconditions, reference data, expected values and volume. Wrong data causes false failures, false passes and privacy risks.
- Prefer **synthetic** and **hand-crafted** data; use production-derived data only when approved and masked.
- Work out data needs **by hand first** with partitions, boundaries and edge values, building rows **one change at a time** from a valid base row.
- AI is good at **ideas and variety**, and weak at **labels, counts, hidden rules (Luhn, dates, relationships), true randomness and volume**. It may also reproduce **real-looking data**.
- Write **constrained prompts**: rules in delimiters, categories and counts, safety rules (fictional people, `example.com`, 555-01xx, official test cards) and a locked JSON format with `targets_rule` and `expected`.
- **The AI designs, code generates, checks prove.** Use seeded Faker and `random.Random` for volume and reproducibility; pin versions.
- **Validate** with small independent checks, then apply **human judgement** for what code cannot see. Record who confirmed the expected outcomes.
- Store data as **fixtures** and drive tests with `parametrize`. A single well-chosen, AI-suggested edge value (non-ASCII digits) found a real bug that eleven ordinary rows missed.

---

## Additional Resources

- Faker documentation, *Welcome to Faker's documentation!* (providers, locales, and the "Seeding the Generator" section on `seed_instance` and version pinning): https://faker.readthedocs.io/en/master/
- Stripe Docs, *Testing* (official test card numbers such as 4242 4242 4242 4242 and how to simulate payment scenarios safely): https://docs.stripe.com/testing
- Python documentation, *random: Generate pseudo-random numbers* (seeding, the "Notes on Reproducibility" section, and why `secrets` is used for security): https://docs.python.org/3/library/random.html
