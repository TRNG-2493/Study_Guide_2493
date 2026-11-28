# AI-Generated Test Data

## Learning Objectives

By the end of this lesson you will be able to:

- **Work out** the test data a feature needs, by purpose: valid, deliberately invalid and boundary.
- **Prompt** an AI for test data with exact rules and a locked format.
- **Validate** AI-generated data against the rules, by hand and with a short script, instead of asking the AI whether its own data is valid.
- **Explain** why tests need repeatable data, and generate it with code and a fixed seed.
- **Protect** privacy by using reserved test domains and invented values, never real personal data.

---

## Why This Matters

Tests are only as good as their data. A perfect test case for "valid users can sign up" proves nothing if the "valid" user in the data is actually 16 years old: the test fails, and someone spends an hour hunting a bug in the sign-up code that does not exist.

AI is very good at producing data that **looks** right: plausible names, tidy email addresses, sensible ages. That is exactly the danger.

Realistic-looking data hides **hidden rules** it breaks: an email with no `.com`, an age outside the allowed range, the same email used twice, or a country code that people say but systems do not accept. The classic example is the United Kingdom. People say "UK", but the official two-letter code in the international standard ISO 3166-1 is **GB**, with "UK" only exceptionally reserved ([Wikipedia: ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1)). A system that expects ISO codes rejects "UK", and an AI writing what people usually say will often produce it.

There is a second problem that matters just as much to testers: **repeatability**. Ask an AI for five users twice and you get two different lists. A test that fails today must fail the same way tomorrow, or nobody can debug it. So AI-generated data is a **draft**: you check it, and then you **save** it, or generate it with code you control.

> **Using this with the handout:** this lesson goes deeper into **Handout 05, Topic 4**. It uses the same sign-up rules, the same AI prompt, the same five "valid" users (only one of which is valid) and the same `check_users.py`.

---

## The Concept

### 1. What Is Test Data?

**Test data** is the input values and records that tests use: users, orders, addresses, coupon codes, files. It comes in three main kinds:

| Kind | Purpose | Sign-up example |
|---|---|---|
| **Valid (positive)** | Should be accepted | `maria.lopez@example.com`, age 34, country US |
| **Invalid (negative)** | Should be rejected, with the right message | Age 16: under the minimum |
| **Boundary** | Sits exactly on or next to a limit | Ages 17, 18, 120 and 121 |

The key rule from the handout: **every row should have a purpose.** "A user" is not a purpose. "A valid user from Canada, to check CA is accepted" is a purpose. "A user aged exactly 18, the youngest allowed" is a purpose. When each row has a purpose, you can tell whether the data is complete, and you can tell what a failure means.

### 2. Working Out What Data You Need

Before asking an AI for anything, work out the data needs yourself. Here are the handout's rules for a sign-up form:

| Field | Rule |
|---|---|
| email | A valid email address |
| age | 18 to 120 |
| country | One of US, CA, GB, IN |
| (all rows) | Emails must be unique |

From these four rules, a tester can list the categories of data needed, without writing a single value yet:

| Category | Why | How many rows (minimum) |
|---|---|---|
| Valid users | Prove a normal sign-up works | 1, plus one per country to cover all four |
| Invalid email | Each rule broken on its own | 1 or more (no `@`, no domain ending) |
| Age boundaries | The range has two edges | 4: ages 17, 18, 120, 121 |
| Invalid country | Codes outside the list | 1 or more (for example "UK", "FR") |
| Duplicate email | The uniqueness rule | 2 rows sharing one email |
| Empty values | Missing input | 1 per field |

Notice two habits from this week. The boundary rows come from boundary value analysis, which you used on Tuesday for the $50.00 coupon limit. And each invalid row breaks **exactly one** rule, so that when it is rejected you know which rule did it.

This list is also the best way to **check** an AI's data: compare its rows with your categories and see which are missing.

### 3. The Hidden Rules AI Breaks

AI-generated data fails in predictable ways:

| Mistake | Example | Why AI makes it |
|---|---|---|
| Invalid format | `raj.patel@example` (no `.com`) | It writes text that looks like an email |
| Out of range | Age 16 in a "valid" set | It does not check numbers against the rule |
| Duplicates | The same email in rows 1 and 4 | Each row is written without "remembering" the others carefully |
| Wrong code | "UK" instead of "GB" | It writes what people commonly say |
| Wrong type | `"34"` (text) instead of `34` (a number) | Text and numbers look the same in a sentence |
| Wrong language syntax | `true` and `null` (JSON) instead of `True` and `None` (Python) | It mixes formats it has seen |

You can head off some of these in the prompt itself. Instead of "country (one of US, CA, GB, IN)", you could write "country: an ISO 3166-1 alpha-2 code, one of US, CA, GB, IN". Instead of "age", write "age as a whole number, not text". Each extra sentence targets one row of the table. As with test cases, a better prompt **reduces** the mistakes; it does not remove them, so the check in Step 3 stays.

The handout's checkpoint shows several of these mistakes in just five rows. Keep the table in mind while you work through the example.

### 4. Worked Example: Get Data from the AI, Then Check It

**The situation:** for **positive** sign-up tests, you need 5 **valid** users that follow the rules in section 2.

#### Step 1: Ask the AI for data

Paste this into a new chat:

```text
Give me 5 VALID test users for a sign-up form, as a Python list of dictionaries.
Each user has: "email" (use the example.com domain), "age" (18 to 120),
"country" (one of US, CA, GB, IN). Emails must be unique.
Reply with the Python list only.
```

**Why it is built this way:** the rules are stated exactly, the format is locked (Tuesday's *Format Locking*) so you can paste the reply straight into Python, and `example.com` keeps the data safe (section 8).

#### Step 2: Check the data by hand

Here is a typical AI answer. It **looks** realistic:

```python
[
    {"email": "maria.lopez@example.com", "age": 34, "country": "US"},
    {"email": "raj.patel@example",       "age": 27, "country": "IN"},
    {"email": "li.wei@example.com",      "age": 16, "country": "CA"},
    {"email": "maria.lopez@example.com", "age": 41, "country": "GB"},
    {"email": "tom.brown@example.com",   "age": 52, "country": "UK"},
]
```

Check each row against the rules table and fill in a table like this one on paper before you read the answer:

| Row | Email valid? | Age 18–120? | Country allowed? | Unique email? | OK? |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Answer:**

| Row | Problem |
|---|---|
| 1 | ✅ OK |
| 2 | ❌ Invalid email: `raj.patel@example` has no `.com` |
| 3 | ❌ Age 16 is under 18 |
| 4 | ❌ Duplicate email: same as row 1 |
| 5 | ❌ "UK" is not allowed: the code is **GB** |

**Only 1 of the 5 "valid" users is actually valid.** Every one of the four bad rows looks like something a person might type, which is why they are easy to miss.

#### Step 3: Let a short script do the checking

Checking 5 rows by hand is fine. Checking 500 is not. Create `check_users.py`:

```python
import re

ALLOWED_COUNTRIES = {"US", "CA", "GB", "IN"}
ai_users = [                                    # paste your AI's users here
    {"email": "maria.lopez@example.com", "age": 34, "country": "US"},
    {"email": "raj.patel@example",       "age": 27, "country": "IN"},
    {"email": "li.wei@example.com",      "age": 16, "country": "CA"},
    {"email": "maria.lopez@example.com", "age": 41, "country": "GB"},
    {"email": "tom.brown@example.com",   "age": 52, "country": "UK"},
]

seen = set()
for i, user in enumerate(ai_users, start=1):
    problems = []
    if not re.fullmatch(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", user["email"]):
        problems.append("invalid email")
    if not 18 <= user["age"] <= 120:
        problems.append("age outside 18-120")
    if user["country"] not in ALLOWED_COUNTRIES:
        problems.append(f"country '{user['country']}' not allowed")
    if user["email"] in seen:
        problems.append("duplicate email")
    seen.add(user["email"])
    print(f"Row {i}: {'OK' if not problems else ', '.join(problems)}")
```

Run `python check_users.py`:

```text
Row 1: OK
Row 2: invalid email
Row 3: age outside 18-120
Row 4: duplicate email
Row 5: country 'UK' not allowed
```

**What this code does:**

- **One `if` per rule**, in the same order as the rules table. Each failed rule adds a readable message to `problems`, so a row that breaks two rules shows both.
- `re.fullmatch(...)` checks that the **whole** email looks like `name@domain.xx`. `fullmatch` matters: plain `re.match` only checks the start of the text, so it would accept `ok@example.com!!!`. The pattern is deliberately simple; real email rules are far more complicated, but this catches the obvious mistakes.
- `18 <= user["age"] <= 120` is Python's neat way to write a **range check**. Both ends are included, matching "18 to 120".
- Duplicates cannot be spotted from one row alone, so `seen` remembers every email so far. The check happens **before** `seen.add(...)`, which is why row 1 is OK and row 4 is the duplicate.
- `enumerate(ai_users, start=1)` numbers the rows from 1, like the hand-check table, instead of Python's usual 0.

Then paste **your** AI's list from Step 1 in place of the example and run it again.

#### Step 4: Ask again, and see why data must be saved

Send the **same** Step 1 prompt in a **new chat** and compare the two lists.

You will see different names, ages and countries. That is normal for an AI (remember temperature, from Monday's *Generative AI Concepts*).

Think about what it would mean for a test. If a test asked the AI for fresh users on every run, a failure today might use a user with age 16; tomorrow's run might not. Nobody could repeat the failure to debug it. That is why reviewed test data is **saved in a file**, or **generated by code with a fixed seed** (section 7), so every run uses exactly the same data.

### 5. Why Not Ask the AI "Is This Data Valid?"

It is tempting to paste the AI's data back and ask *"Are all of these users valid?"*. The handout advises against relying on that, for a good reason: the same kind of process that produced the mistakes is being asked to find them. It may well find some, but you cannot tell which ones it will miss, and its answer may change if you ask again.

A rule-based script is an **independent** check. It does not care how plausible a row looks; it only applies the rules, and it gives the same answer every time. That is the same reason you ran the deterministic word check before the AI review in *AI-Assisted Requirements Analysis*.

An AI can still help, in a different role: ask it to **write** a checking script like `check_users.py` for your rules. Then review the script, and test it on rows you know are good and bad. A checker you have tested is worth far more than an opinion you cannot check.

### 6. Deliberate Negative Data, Labelled

Invalid data is not bad in itself. For **negative** tests you need it on purpose. The rule from the handout is that invalid data must be **deliberate and labelled**: each row says which rule it breaks and what the system should do.

Here is an AI's answer to *"Give 4 invalid test users, each breaking exactly ONE rule, and add a 'breaks' field naming the rule"*, **illustrative**:

```python
ai_users = [
    {"email": "no-at-sign.example.com", "age": 30, "country": "US", "breaks": "email"},
    {"email": "kid@example.com",        "age": 17, "country": "GB", "breaks": "age"},
    {"email": "old@example.com",        "age": 120, "country": "IN", "breaks": "age"},
    {"email": "fr@example.com",         "age": 45, "country": "FR", "breaks": "country"},
]
```

Put these rows in `check_users.py` (the extra `breaks` field does no harm) and change the print to show the claim: `print(f"Row {i} (claims {user['breaks']}): ...")`. The output:

```text
Row 1 (claims email): invalid email
Row 2 (claims age): age outside 18-120
Row 3 (claims age): OK
Row 4 (claims country): country 'FR' not allowed
```

Row 3 is the interesting one. The AI says age 120 breaks the age rule, but the rule is "18 to 120", so 120 is **valid**: it is the top boundary. The label is wrong. If this row went into a negative test expecting "age not allowed", the test would fail against correct code, and the bug report would be false.

This is the same off-by-one boundary mistake you have seen all week, now in data. A labelled data set lets you catch it, because you can compare what each row **claims** with what the checker **finds**.

### 7. Repeatable Data: Save It or Seed It

There are two good ways to make test data repeatable.

**Option 1: save the reviewed data.** Once a data set has passed your checks, save it in a file, such as `users.json`, and have every test read the file. The data never changes unless someone changes it on purpose, and the change shows up in version control.

**Option 2: generate it with code and a fixed seed.** Python's `random` module produces **pseudo-random** numbers: they look random, but they come from a starting value called a **seed**. Python's documentation notes that re-using a seed lets the same sequence be reproduced from run to run ([Python docs: random](https://docs.python.org/3/library/random.html)). Here is a generator, `make_users.py`:

```python
import json
import random

rng = random.Random(42)            # fixed seed: same users on every run
NAMES = ["asha", "ben", "chen", "dana", "eli", "farah", "gus", "hana"]
COUNTRIES = ["US", "CA", "GB", "IN"]

users = []
for i, name in enumerate(rng.sample(NAMES, 5), start=1):
    users.append({
        "email": f"{name}.{i}@example.com",     # reserved test domain, unique by i
        "age": rng.randint(18, 120),
        "country": rng.choice(COUNTRIES),
    })

with open("users.json", "w") as f:
    json.dump(users, f, indent=2)
print(f"Saved {len(users)} users to users.json")
```

Running it saves these five users, the same on every run (we checked on Python 3.10 and 3.13):

```text
{'email': 'ben.1@example.com', 'age': 46, 'country': 'CA'}
{'email': 'asha.2@example.com', 'age': 112, 'country': 'US'}
{'email': 'farah.3@example.com', 'age': 104, 'country': 'US'}
{'email': 'chen.4@example.com', 'age': 93, 'country': 'IN'}
{'email': 'hana.5@example.com', 'age': 22, 'country': 'US'}
```

**What this code does:**

- `random.Random(42)` creates a generator with seed 42. Change the seed and you get different users; keep it and you always get these.
- `rng.sample(NAMES, 5)` picks 5 **different** names, and the row number `i` is added to each email, so emails are unique by construction.
- `rng.randint(18, 120)` and `rng.choice(COUNTRIES)` can **only** produce allowed values, so the rules are built into the generator.
- `json.dump(..., indent=2)` saves the list as readable JSON, combining both options: generated by code, then saved.

Paste these users into `check_users.py` and every row prints `OK`. That is expected, but still worth doing: if someone edits the generator later, the checker will notice when it breaks a rule.

Now look critically at the output. Three of the five ages are over 90. Random does **not** mean realistic: real sign-ups are mostly far younger. And random rarely lands **on** a boundary: none of these users is 18 or 120. A generator is good for volume; boundary and negative rows still need to be written **deliberately**, as in section 2.

A useful division of labour is **"AI designs, code generates"**: ask an AI to help you list the categories and write the generator, then review the generator and let the code produce the data.

### 8. Test Data for the Running Example

The same ideas apply to US-205, where the data is subtotals and coupon codes rather than users. Written with a purpose column, a small data set for the coupon tests looks like this:

| Subtotal | Code | Purpose | Expected (from the story) |
|---|---|---|---|
| 100.00 | SAVE10 | Well above the boundary (AC1) | 90.00 |
| 50.00 | SAVE10 | On the boundary (AC1) | 45.00 |
| 50.01 | SAVE10 | Just above the boundary; checks rounding (AC1) | 45.01 |
| 49.99 | SAVE10 | Just below the boundary (AC2) | 49.99 and "Spend $50.00 to use SAVE10" |
| 100.00 | BOGUS | Unknown code (AC3) | "Coupon code not recognised" |
| 100.00 | save10 | **Question for the BA**: not covered by any AC | (none until the BA answers) |

Read the last row carefully. It is fine to keep `save10` in your data **as a question**, because a shopper might really type it. It is not fine to give it an expected result, because US-205 does not provide one. This is the data version of the invented rule from *AI within the QA Lifecycle*, where `save10`, `Save10` and `sAvE10` were listed as **valid** codes. The difference between a useful row and a harmful one is the purpose and expected columns.

A purpose column also makes AI-generated data much easier to review. When you ask an AI for coupon data, ask it to fill in the purpose and the AC for each row. Any row whose purpose names no AC, or names one that does not exist, deserves a second look.

### 9. Data That Depends on State

Some test data is not a single input but a **state** the system must be in before the test starts. Two examples from this lesson:

- **The duplicate-email rule.** To test that a second sign-up with `maria.lopez@example.com` is rejected, the first user must **already exist** in the system. The data is not one row; it is "this user exists, then this sign-up is attempted".
- **AC4, one coupon per order.** To test a second coupon, an order must already have SAVE10 applied. That is part of the test's **precondition**, as described in *AI-Generated Test Cases*.

AI drafts often miss this kind of data, because the prompt asks for rows and the state is not a row. When you review generated data, ask for each test: **what must already be true before the first step?**

If the answer involves existing records, the data set needs setup steps, and the test needs to clean up afterwards so the next run starts from the same state. You will build tests like this in later weeks; for now, the habit is to notice when a test needs state as well as input.

### 10. Never Use Real Personal Data

Test data should never contain real people's information. Three habits from the handout keep you safe:

- **Use reserved test domains for emails.** The domains `example.com`, `example.net` and `example.org` are reserved for examples and testing by the internet standards body, in RFC 2606 ([RFC Editor](https://www.rfc-editor.org/rfc/rfc2606)). An email to `anyone@example.com` can never reach a real person.
- **Use invented names and values.** Not colleagues' names, not customers' names, not "realistic" data copied from somewhere.
- **Never copy production data into test environments without approval.** Real customer records belong to the customers. Even "just for testing", copying them can break privacy laws and company policy.

When you ask an AI for test data, tell it which domain to use, as the Step 1 prompt does. And check the result: an AI asked for "realistic emails" may produce addresses at real providers such as `gmail.com`, which could belong to someone. You will look at the wider rules for handling sensitive data in *Responsible Use of AI in QE* this afternoon.

### 11. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| `TypeError: '<=' not supported between instances of 'int' and 'str'` | The AI wrote an age as text (`"34"`) instead of a number (`34`) | Fix the data, and note it: wrong types are a common AI data mistake |
| `NameError: name 'true' is not defined` | The AI replied in JSON (`true`, `false`, `null`) instead of Python | Ask again for a "Python list", or change to `True`, `False`, `None` |
| `SyntaxError` after pasting | The AI added text before or after the list | Paste only the part from `[` to `]` |
| The same test fails one day and passes the next | Data is fetched fresh each run | Save reviewed data, or seed the generator |
| Emails at real providers such as `gmail.com` | The prompt asked for "realistic" emails | Ask for `example.com` only, and check every row |
| All rows look fine, but no boundary is tested | Random or AI data clusters in the middle | Add boundary rows deliberately |

---

## Practice Exercises

1. **Check your AI's users (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** send the Step 1 prompt to your AI assistant.
   - **Review:** check its rows by hand with the rules table.
   - **Run:** paste its list into `check_users.py` and run it.
   - **Record:** in `prompts.txt`, note how many rows were valid and which hidden rules it broke.

2. **A labelled negative set (AI tool, 15 min).** Ask your AI: *"Give 4 invalid test users, each breaking exactly ONE rule, and add a 'breaks' field naming the rule."* Run them through `check_users.py` with the print from section 6. Does each row show exactly the problem it claims? Look closely at any row on a boundary.

3. **Categories first (AI tool, 10 min).** Ask your AI: *"What kinds of test data do I need to test a sign-up form with email, age and country? List categories only, no data."* Compare its categories with the table in section 2. Which did it add, and which did it miss?

4. **Empty email (code, 10 min).** Add a row with `"email": ""` to `check_users.py` and run it. Which existing check catches it, and why? (Hint: what does `re.fullmatch` return for an empty string?)

5. **Add the boundaries (code, 15 min).** Change `make_users.py` so that, after the five random users, it adds two fixed users at ages **18** and **120**, with unique `example.com` emails. Run it twice and confirm both runs save the same seven users. Then run them through `check_users.py`.

---

## Knowledge Check

1. Name the three main kinds of test data, with an example of each for the sign-up form.

<details><summary>Answer</summary>

Valid (age 34, country US), invalid (age 16) and boundary (ages 17, 18, 120, 121).

</details>

2. Why should each invalid row break exactly one rule?

<details><summary>Answer</summary>

So that when the row is rejected, you know which rule caused it. A row breaking two rules cannot tell you whether each rule works.

</details>

3. Why is "UK" a classic AI test data mistake?

<details><summary>Answer</summary>

People commonly say "UK", but the ISO 3166-1 alpha-2 code for the United Kingdom is GB. A system expecting ISO codes rejects "UK".

</details>

4. Why is a rule-based script a better check than asking the same AI "is this data valid?"?

<details><summary>Answer</summary>

The script is independent and deterministic: it applies the rules the same way every time, however plausible a row looks. The AI may miss mistakes, and you cannot tell which.

</details>

5. The AI labelled a user aged 120 as breaking the age rule. Who is right, and why does it matter?

<details><summary>Answer</summary>

The checker: the rule is 18 to 120, so 120 is valid. A negative test using that row would fail against correct code and lead to a false bug report.

</details>

6. Why should a test not ask an AI for fresh data on every run?

<details><summary>Answer</summary>

The AI gives different data each time, so failures would not be repeatable. Save reviewed data, or generate it with code and a fixed seed.

</details>

7. Why use `example.com` for test emails?

<details><summary>Answer</summary>

It is reserved for examples and testing (RFC 2606), so a test email can never reach a real person.

</details>

8. In the US-205 data, why does the `save10` row have no expected result?

<details><summary>Answer</summary>

No acceptance criterion covers lower-case codes, so any expected result would be an invented rule. The row stays as a question for the BA until they answer.

</details>

---

## Glossary

- **Test data:** input values and records used by tests.
- **Positive / negative test data:** data that should be accepted / should be rejected.
- **Boundary data:** values on or next to a limit, such as ages 17, 18, 120 and 121.
- **Hidden rule:** a rule the data must follow that is easy to break without noticing, such as ISO country codes.
- **ISO 3166-1 alpha-2:** the international standard of two-letter country codes (US, CA, GB, IN).
- **Independent check:** a check that does not rely on the same source that produced the output.
- **Labelled data:** data where each row states its purpose, such as which rule it breaks.
- **Repeatable data:** data that is the same on every test run.
- **Seed:** a starting number that makes pseudo-random generation repeatable.
- **Pseudo-random:** numbers that look random but are produced by a fixed process from a seed.
- **JSON:** a common text format for data, using `true`, `false` and `null`.
- **State (test data):** records or settings that must already exist before a test starts, such as an existing user.
- **Purpose column:** a column stating why each data row exists and which rule or AC it checks.
- **Reserved test domain:** a domain such as `example.com` set aside for examples and testing.

---

## Summary

- **Work out the data you need first**, by purpose: valid, invalid (one rule broken per row) and boundary.
- **AI data looks realistic but breaks hidden rules**: formats, ranges, duplicates, codes like "UK" for GB, and wrong types.
- **Check every row against the rules** with an independent script, not by asking the same AI. In the worked example, only **1 of 5** "valid" users was valid.
- **Label deliberate negative data**, and compare each row's claim with the checker's finding. The AI mislabelled the boundary age 120.
- **Make data repeatable** by saving it or generating it with a fixed seed, and add boundary rows deliberately.
- **Never use real personal data.** Use `example.com` and invented values.

---

## Additional Resources

- Python documentation, *random — Generate pseudo-random numbers*: https://docs.python.org/3/library/random.html
- RFC 2606, *Reserved Top Level DNS Names* (includes example.com): https://www.rfc-editor.org/rfc/rfc2606
- Python documentation, *json — JSON encoder and decoder*: https://docs.python.org/3/library/json.html
