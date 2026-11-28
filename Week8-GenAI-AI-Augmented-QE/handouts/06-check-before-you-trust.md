# Week 08 · Lecture 06: Check Before You Trust

**Topics:**

1. [AI-Assisted Automation Development](#topic-1)
2. [Human Validation of AI Output](#topic-2)
3. [Responsible Use of AI in QE](#topic-3)

---

## Before Class

> **Setup checklist (do this before the lecture starts)**
>
> 1. Work in your `week08` folder.
> 2. Check pytest is installed:
>    ```bash
>    python -m pytest --version
>    ```
>    If not: `python -m pip install pytest`
> 3. No browser or Playwright install is needed: Topic 1 uses a small Python stand-in for the login page so everyone can follow along offline. Topics 2 and 3 are review and AI-assistant activities.
> 4. Have your AI assistant open: **ChatGPT, Copilot Chat or Claude**.

---

## How to Use This Handout

Same layout as before: **Definition → Key ideas → Worked example (step by step) → Checkpoint → Your turn → Common errors.** Topic 1 uses Python and pytest; Topics 2 and 3 are hands-on review activities (paper, spreadsheet and your AI assistant) with one optional demo script. Do exercise 1 in class; the rest are for after class.

Lecture 05 showed how AI helps across the testing life cycle. Today's theme is in the title: **AI produces drafts, and humans decide what's trusted.** You'll see a test that passes and proves **nothing**, learn how to **record** your review decisions, and learn the rules for using AI **safely** with real-world data.

---

## Learning Objectives

By the end of this lecture you will be able to:

- Explain why an AI-written test that **passes** can still be **useless**, and prove it by breaking the code on purpose.
- Give an AI the **right inputs** for automation work, and prefer **user-facing locators**.
- Review AI output with a **checklist** and record your decisions in a **correction log**.
- **Redact** sensitive data before sending text to an AI tool, and explain **disclosure** and **accountability**.

---

<a id="topic-1"></a>

# Topic 1: AI-Assisted Automation Development

## Definition

**AI-assisted automation development** means using AI to help write automated test code: pytest functions, Playwright or Selenium scripts, page objects and fixtures. To do this well, the AI needs the **reviewed test case**, details of the **page or function** under test, and your team's **conventions**. The biggest danger is a test that **passes but proves nothing**: it runs green whether the feature works or not, because its assertion is too weak (`assert result`) or checks the wrong thing. The tester's job is to make sure every automated test **can fail** when the feature is broken.

## Key Ideas

1. **Give the AI what a colleague would need:**

   | Input | Example |
   |---|---|
   | The **reviewed** test case | "TC-07: valid login shows *Welcome back!*" |
   | The page or function | HTML of the login form, or the function's code |
   | Your conventions | "pytest; test names start with `test_`; use `get_by_role` locators" |

2. **A test that can't fail is worse than no test.** It gives **false confidence**. Watch out for `assert result`, `assert result is not None`, or tests with no assert at all.
3. **The "break it" check:** temporarily break the feature. If the test still passes, the test is useless. (This is a simple form of **mutation testing**.)
4. **Prefer locators a user would see.** AI often suggests fragile CSS or XPath. With Playwright:

   | ❌ Fragile (AI often suggests) | ✅ User-facing (prefer) |
   |---|---|
   | `page.locator("#btn-23 > span")` | `page.get_by_role("button", name="Log in")` |
   | `page.locator("//div[3]/input[1]")` | `page.get_by_label("Email")` |
   | `page.locator(".msg-err")` | `page.get_by_text("Invalid email or password")` |

   User-facing locators break less often when the page layout changes, and they also check what the user actually sees.

## Worked Example: The Test That Proves Nothing

**The situation:** the login page shows *"Welcome back!"* for valid credentials and *"Invalid email or password"* for anything else. So everyone can run this offline, we use a small Python **stand-in** for the page's logic instead of a real browser. The lesson is exactly the same for Playwright tests.

### Step 1: The feature (a stand-in for the login page)

Create `login_app.py`:

```python
USERS = {"tester@example.com": "Test#Pass1"}

def login(email: str, password: str) -> str:
    """Valid credentials show "Welcome back!".
    Anything else shows "Invalid email or password"."""
    if USERS.get(email) == password:
        return "Welcome back!"
    return "Invalid email or password"
```

**What this code does:**

- `USERS` holds one **test-environment** account. These aren't real credentials.
- `USERS.get(email)` looks up the password for that email, or returns `None` if the email is unknown. If it matches, login succeeds.
- The function returns the **message the user would see**.

### Step 2: The AI's draft tests

We asked an AI assistant: *"Write pytest tests for the login function."* It returned this. Create `test_login_ai_draft.py`:

```python
from login_app import login

def test_login_works():
    result = login("tester@example.com", "Test#Pass1")
    assert result

def test_wrong_password_is_handled():
    result = login("tester@example.com", "wrong")
    assert result is not None
```

Run `python -m pytest -q test_login_ai_draft.py`. **Both tests pass.** Looks good?

**Look closely at the asserts:**

- `assert result` passes for **any** non-empty text, including the error message!
- `assert result is not None` passes for **any** returned value.

Neither test checks **which** message appears.

### Step 3: Break the feature on purpose

Edit `login_app.py`: change the line `if USERS.get(email) == password:` to:

```python
    if True:  # BUG: everyone gets in
```

Now **everyone** can log in with any password: a serious security bug. Run the AI draft again:

```bash
python -m pytest -q test_login_ai_draft.py
```

**The AI's tests still pass.** They can't detect the bug they were written to catch.

### Step 4: Write reviewed tests that can fail

Create `test_login_reviewed.py`:

```python
import pytest
from login_app import login

VALID_EMAIL = "tester@example.com"
VALID_PASSWORD = "Test#Pass1"          # test-environment account, not a real one

def test_valid_login_shows_welcome():
    assert login(VALID_EMAIL, VALID_PASSWORD) == "Welcome back!"

@pytest.mark.parametrize("email, password", [
    (VALID_EMAIL, "wrong"),             # wrong password
    ("nobody@example.com", VALID_PASSWORD),  # unknown user
    (VALID_EMAIL, ""),                  # empty password
])
def test_invalid_login_shows_error(email, password):
    assert login(email, password) == "Invalid email or password"
```

**What this code does:**

- Each assert checks the **exact message** the user should see, using `==`.
- The test data lives in named constants at the top, so it's easy to see and change.
- `parametrize` (Lecture 04) covers three different **invalid** situations with one test.

With the bug **still in place**, run `python -m pytest -q test_login_reviewed.py`. Three tests **fail**: they caught the bug.

### Step 5: Fix the feature and confirm

Change `if True:` back to `if USERS.get(email) == password:` and run **both** test files:

```bash
python -m pytest -q test_login_ai_draft.py test_login_reviewed.py
```

Everything passes again. Only the **reviewed** tests proved anything along the way.

### Consolidated Files

**`login_app.py`** (correct version)

```python
USERS = {"tester@example.com": "Test#Pass1"}

def login(email: str, password: str) -> str:
    """Valid credentials show "Welcome back!".
    Anything else shows "Invalid email or password"."""
    if USERS.get(email) == password:
        return "Welcome back!"
    return "Invalid email or password"
```

**`test_login_reviewed.py`**

```python
import pytest
from login_app import login

VALID_EMAIL = "tester@example.com"
VALID_PASSWORD = "Test#Pass1"          # test-environment account, not a real one

def test_valid_login_shows_welcome():
    assert login(VALID_EMAIL, VALID_PASSWORD) == "Welcome back!"

@pytest.mark.parametrize("email, password", [
    (VALID_EMAIL, "wrong"),             # wrong password
    ("nobody@example.com", VALID_PASSWORD),  # unknown user
    (VALID_EMAIL, ""),                  # empty password
])
def test_invalid_login_shows_error(email, password):
    assert login(email, password) == "Invalid email or password"
```

## Checkpoint

| Situation | AI draft tests | Reviewed tests |
|---|---|---|
| Feature correct (Step 2 / Step 5) | `2 passed` | `4 passed` |
| Feature **broken** (Step 3 / Step 4) | `2 passed` ❌ (missed the bug) | `3 failed, 1 passed` ✅ (caught it) |

Running both files together on the correct code gives:

```text
......                                                                   [100%]
6 passed in 0.02s
```

**The lesson:** a passing test means nothing until you've seen it **fail** for the right reason.

### A Prompt Template for Automation Code

When you ask an AI to write automated tests, give it the **reviewed** test cases and your conventions, and tell it what a good assert looks like. Save this template in `prompts.txt` as `Automation - v1`:

```text
You are a test automation engineer. Write pytest tests for the function below.

### Reviewed test cases (use exactly these; do not add others)
TC-07: valid login (tester@example.com / <valid_password>) shows "Welcome back!"
TC-08: wrong password shows "Invalid email or password"
TC-09: unknown email shows "Invalid email or password"

### Code under test
<paste login_app.py here>

### Conventions
- pytest only; test names start with test_ and describe the behaviour
- every assert compares the EXACT expected message with ==
- never use "assert result" or "is not None" as the only check
- put test data in constants at the top of the file
- use parametrize when several cases share the same check

Reply with one Python file only.
```

**Why each part is there:**

| Part | Prevents |
|---|---|
| "use exactly these; do not add others" | Invented test cases |
| `<valid_password>` placeholder | Real secrets in the prompt |
| "compares the EXACT expected message" | Tests that prove nothing |
| "never use assert result" | The exact weakness from Step 2 |
| "one Python file only" | Extra explanation text you'd need to strip out |

## Your Turn

1. **(In class, 3 min)** Introduce a different bug: change `return "Welcome back!"` to `return "Welcome!"`. Which test file catches it?
2. **(After class)** Paste `login_app.py` into your AI assistant and ask: *"Write pytest tests for this function. Every assert must check the exact message returned. Include invalid cases."* Run the "break it" check from Step 3 on **its** tests. Do they catch the bug?
3. **(After class)** The real login page has this HTML: `<label for="email">Email</label><input id="email">` and `<button class="btn btn-primary">Log in</button>`. Write the two **user-facing** Playwright locators for the email field and the button (see Key Idea 4). No need to run them.
4. **(After class)** Find any test you've written in an earlier week. Apply the "break it" check: change the code under test so the feature is wrong. Does your test fail?

## Common Errors

| Error you see | Why it happens | Fix |
|---|---|---|
| `IndentationError` after editing `if True:` | The new line lost its 4-space indent | Keep the same indentation as the line you replaced |
| All tests still pass after "breaking" the code | You didn't save the file, or you edited a different copy | Save, and check you're in the right folder |
| You forgot to undo the bug | The code is still broken for later exercises | Always **restore** after a "break it" check (Step 5) |

---

<a id="topic-2"></a>

# Topic 2: Human Validation of AI Output

## Definition

**Human validation** is the structured review a person does **before** AI output is trusted and used. The reviewer checks each item against the requirement using a **checklist**, then decides to **accept**, **edit** or **reject** it, and **records** that decision and the reason in a **correction log**. This approach is called **human-in-the-loop**: the AI drafts, and a named person approves and stays **accountable** for the result. The log isn't paperwork for its own sake. It shows **what kinds of mistakes** the AI makes, so the team can improve its prompts and know where to look harder.

## Key Ideas

1. **Three traps that make people trust AI too much:**

   | Trap | What happens |
   |---|---|
   | **Fluency trap** | Well-written text *feels* correct |
   | **Volume trap** | 50 test cases look thorough, so nobody checks each one |
   | **Automation bias** | "The tool said so" replaces thinking |

2. **A review checklist for AI-generated test cases:**
   1. Does it **trace** to an acceptance criterion?
   2. Does the **expected result** match the requirement **exactly**?
   3. Is every rule in it **actually stated** in the story (nothing invented)?
   4. Could this test ever **fail**?
3. **Three decisions:** **accept** (use as-is), **edit** (fix and use), **reject** (remove). Edits and rejections must have a **reason category** (for example "wrong expected result", "invented rule").
4. **Code points, humans decide.** Scripts (like Lecture 05's checks) can point at suspicious rows, but the final decision is always a person's.

## Worked Example: Review an AI Draft and Keep a Correction Log

**The situation:** an AI drafted four test cases for US-205. You review each one with the checklist, decide, and record your decision in a **correction log**: a simple table (on paper, in a spreadsheet or in a text file). No code is needed. The **habit** is what matters.

### Step 1: The checklist and the draft

**The review checklist** (from Key Idea 2):

1. Does it trace to an acceptance criterion?
2. Does the expected result match the requirement **exactly**?
3. Is every rule in it **actually stated** in the story?
4. Could this test ever **fail**?

**The AI's draft:**

| ID | AI's test case |
|---|---|
| TC-01 | SAVE10 on $100.00 gives $90.00 |
| TC-02 | SAVE10 on $49.99 gives $44.99 |
| TC-03 | Lowercase save10 gives 10% off |
| TC-04 | Unknown code shows "Coupon code not recognised" |

Before reading on, apply the four questions to each case yourself.

### Step 2: Set up the log

Draw this table. The rules of a good log:

- Only **three** decisions are allowed: **accept**, **edit** or **reject**.
- Every edit or rejection **must** have a **reason category**, such as "wrong expected result" or "invented rule".
- The **note** says **why**, quoting the requirement where possible.

| ID | Decision | Category | Note (why?) |
|---|---|---|---|
| | | | |

### Step 3: Record your decisions

Work through the cases one by one and fill in a row for each.

**Tip:** for TC-02, check the AC2 rule for subtotals **under** $50.00. For TC-03, ask: where in US-205 does it say lowercase works?

### Step 4: Learn from the log

When the log is complete, count:

- How many cases were **accepted as-is**? Divide by the total to get the **accepted-as-is rate**, a simple measure of how good the AI's draft was.
- Which **categories** came up? Each one tells you what to add to your prompt next time. For example, "invented rule" → add *"Use only rules stated in the story."*

### Step 5: Ask the AI to review itself, then compare

Paste the four test cases and US-205 into a **new chat** and ask:

```text
Review these 4 test cases against the user story. For each, answer: accept, edit or reject,
with a one-line reason. Use only the story as the source of truth.

### User story
US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.

### Test cases
TC-01: SAVE10 on $100.00 gives $90.00
TC-02: SAVE10 on $49.99 gives $44.99
TC-03: Lowercase save10 gives 10% off
TC-04: Unknown code shows "Coupon code not recognised"
```

Compare its decisions with **your** log. Where you disagree, **who is right according to the story**?

**What to notice:** an AI can be a useful **second reviewer**, but it isn't the **accountable** one. If both of you missed something, the log still has **your** name on it.

### Consolidated Result

Your completed correction log (Steps 2–4) is the result. Add the Step 5 prompt to `prompts.txt`, with the story and test cases:

```text
=== AI second review - v1 ===
Use: get an AI second opinion on test cases (you stay accountable).
Source: Handout 06, Topic 2

--- Prompt (new chat) ---
Review these 4 test cases against the user story. For each, answer: accept, edit or reject,
with a one-line reason. Use only the story as the source of truth.

### User story
US-205 Apply coupon at checkout
AC1: SAVE10 gives 10% off a subtotal of $50.00 or more.
AC2: Subtotals under $50.00 are unchanged and show "Spend $50.00 to use SAVE10".
AC3: Unknown codes show "Coupon code not recognised".
AC4: Only one coupon per order.

### Test cases
TC-01: SAVE10 on $100.00 gives $90.00
TC-02: SAVE10 on $49.99 gives $44.99
TC-03: Lowercase save10 gives 10% off
TC-04: Unknown code shows "Coupon code not recognised"
```

## Checkpoint

**Answer key: the correction log**

| ID | Decision | Category | Note (why?) |
|---|---|---|---|
| TC-01 | **Accept** | – | Matches AC1 |
| TC-02 | **Edit** | Wrong expected result | AC2: under $50.00 is unchanged → $49.99, plus the message "Spend $50.00 to use SAVE10" |
| TC-03 | **Reject** | Invented rule | Case-insensitivity isn't in US-205. Ask the BA |
| TC-04 | **Accept** | – | Matches AC3 exactly |

**Step 4:** accepted as-is = **2 of 4 = 50%**. Categories: 1 × wrong expected result, 1 × invented rule.

**Also notice:** nothing covers **AC4** or the **$50.00 boundary**. A good reviewer adds a note: *"Missing: AC4 test (ask the BA for the message); boundary test at exactly $50.00."*

**Mark the AI's Step 5 review:** ✅ TC-02 flagged (should be edited) · ✅ TC-03 rejected as not in the story · ✅ TC-01 and TC-04 accepted · ⭐ bonus if it mentions the missing AC4 or boundary tests.

### How Much Review Is Enough?

You can't always review 200 AI-generated test cases one by one with the same care. Match the **depth** of the review to the **risk**:

| Risk of the area | Examples | Review depth |
|---|---|---|
| **High** | Payments, discounts, login and security, personal data | Review **every** item against the checklist |
| **Medium** | Search, filters, error messages | Review every item quickly; check the full checklist for a sample of them |
| **Low** | Cosmetic text, help pages | Review a **sample** (for example 1 in 5). If the sample has problems, review them all |

Two rules always apply, whatever the risk:

1. **Anything involving money or security is high risk.** US-205 is about discounts, so every case gets a full review.
2. **If a sample finds problems, widen the review.** Finding one invented rule means there are probably more.

## Your Turn

1. **(In class, 3 min)** Add a fifth AI case to your log: **TC-05: SAVE10 on exactly $50.00 gives $45.00.** Apply the checklist and record your decision. What's the accepted-as-is rate now?
2. **(After class)** Use your own AI's test cases from Lecture 05 (Topic 3, exercise 4). Review 5 of them with the checklist and log each decision. What's your AI's accepted-as-is rate?
3. **(After class)** Look at your problem categories. Write **one new line** for your test-case prompt in `prompts.txt` that would prevent the most common problem.
4. **(After class)** Turn your log into a spreadsheet with the same four columns. Add a column for the **reviewer's name** and one for the **date**. Why do these two matter?

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| A decision of "edit" with no category | Easy to skip when you're in a hurry | Every edit or rejection needs a category. That's what makes the log useful |
| You and the AI disagree | One of you missed something | The **story** decides. Re-read the exact AC |
| The log says "accept" for everything | Review fatigue (the **volume trap**) | Slow down on money and security cases. Use the review-depth table |

---

<a id="topic-3"></a>

# Topic 3: Responsible Use of AI in QE

## Definition

**Responsible use of AI** means using AI tools in ways that are **safe, legal, fair and honest**: protecting private and confidential data, respecting your organisation's rules, being open about when AI helped, and staying **accountable** for the results. For testers this matters a lot, because we handle sensitive data all the time: bug reports with customer emails, logs with session tokens, test environments copied from production. Pasting one unredacted log into a public AI tool can cause a **data breach** without writing a single line of code. The simple habit that prevents most problems is: **redact before you prompt**, and **if in doubt, don't paste**.

## Key Ideas

1. **The rules of the road for testers:**

   | Rule | In practice |
   |---|---|
   | **Protect data** | Never paste passwords, keys, customer personal data or confidential code into tools your company hasn't approved |
   | **Redact first** | Replace sensitive values with placeholders: `<EMAIL>`, `<CARD>` |
   | **Disclose** | Say when AI helped: "Test cases drafted with AI, reviewed by J. Singh" |
   | **Stay accountable** | You own what you submit, even if AI wrote the first draft |
   | **Check licences and security** | AI-generated code may copy licensed code or contain security flaws, so review it like any code |
   | **Watch for bias** | AI test data can be narrow (only English names, only US addresses), so check that your data reflects your real users |

2. **Follow your organisation's AI policy.** It says which tools are approved and for which data. When unsure, **ask** before pasting.
3. **Automate the safety check.** A small **pre-flight** script that refuses to send text containing sensitive data is more reliable than remembering every time.
4. **Over-reliance is a risk too.** Keep practising your own test design skills. AI should make you faster, not replace your thinking.

## Worked Example: Redact Before You Prompt

**The situation:** a checkout test failed, and you want an AI assistant to help you understand the log. But the log contains private data. **Never paste it as it is.**

```text
2026-11-20 09:14:03 ERROR checkout failed for customer=priya.sharma@gmail.com card=4111 1111 1111 1111 api_key=sk_live_8f2aQ91xZ password=Summer2026!
```

(All the values here are fake. 4111 1111 1111 1111 is a well-known **test** card number.)

### Step 1: Spot the sensitive values

Read the log line and list **every** value that must not be sent to a public AI tool, and **why**:

| Value | Type | Why it's sensitive |
|---|---|---|
| ? | ? | ? |

### Step 2: Redact by hand

Rewrite the line, replacing each sensitive value with a **placeholder** in angle brackets: `<EMAIL>`, `<CARD>`, `<API_KEY>`, `<PASSWORD>`. Keep everything the AI needs to help you debug: the **time**, the **error** and **which fields** were involved.

### Step 3: Ask for help, safely

Paste **your redacted line** (never the original) into your AI assistant:

```text
This checkout test failed. Here is the redacted log line. Sensitive values have been
replaced with placeholders in angle brackets.

<paste your redacted line here>

What are the most likely causes of the failure, and what should I check first?
```

**What to notice:** the AI can still help. The placeholders tell it **what kind** of value was there, which is all it needs.

### Step 4: See the redaction automated (demo)

Doing this by hand for every log isn't realistic. Teams use a small script: a list of patterns for each kind of sensitive data, plus a **pre-flight check** that refuses to send text if anything sensitive is left. To try it, save it as `redact.py` and run `python redact.py`. It uses standard Python only. You don't need to understand every line.

```python
import re

log_text = ("2026-11-20 09:14:03 ERROR checkout failed for customer=priya.sharma@gmail.com "
            "card=4111 1111 1111 1111 api_key=sk_live_8f2aQ91xZ password=Summer2026!")

RULES = [                                        # (label, pattern that finds it)
    ("EMAIL",    r"[\w.+-]+@[\w-]+\.[\w.]+"),
    ("CARD",     r"\b\d(?:[ -]?\d){12,15}\b"),
    ("API_KEY",  r"\bsk_(?:live|test)_\w+"),
    ("PASSWORD", r"(?<=password=)[^<\s]\S*"),
]

def redact(text):
    for label, pattern in RULES:
        text = re.sub(pattern, f"<{label}>", text)
    return text

def safe_to_send(text):                          # the pre-flight check
    return not any(re.search(pattern, text) for _, pattern in RULES)

print(redact(log_text))
print("Original safe to send?", safe_to_send(log_text))
print("Redacted safe to send?", safe_to_send(redact(log_text)))
```

**What to look for:** each rule pairs a **label** with a **pattern** (a regular expression) that finds that kind of value. `redact` replaces every match with `<LABEL>`. `safe_to_send` says **False** if any pattern still matches. It prints:

```text
2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>
Original safe to send? False
Redacted safe to send? True
```

> **Tip:** asking an AI assistant to **explain** a regex like these is a great use of AI. Asking it to **write** one is fine too, but **test the result** on real examples before trusting it.

### Consolidated Result

Your redacted line from Step 2 and the Step 3 prompt are the result. Add the prompt to `prompts.txt` with the **redacted** line filled in (never the original):

```text
=== Debug a log - redacted v1 ===
Use: get debugging help on a log line after redacting sensitive data.
Source: Handout 06, Topic 3

--- Prompt (new chat) ---
This checkout test failed. Here is the redacted log line. Sensitive values have been
replaced with placeholders in angle brackets.

2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>

What are the most likely causes of the failure, and what should I check first?
```

## Checkpoint

**Answer key, Step 1:**

| Value | Type | Why it's sensitive |
|---|---|---|
| `priya.sharma@gmail.com` | Email | A real customer's **personal data** |
| `4111 1111 1111 1111` | Card number | **Payment data** |
| `sk_live_8f2aQ91xZ` | API key | A **secret**: anyone with it can call the system |
| `Summer2026!` | Password | A **secret** |

**Answer key, Step 2:**

```text
2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>
```

**Check your redacted line:**

- ✅ All four values replaced
- ✅ The time, the error and the field names (`customer=`, `card=` …) are kept
- ✅ You pasted only the **redacted** version into the AI

**One more responsible-use habit: disclosure.** When you hand in AI-assisted work, add a line like:

```text
AI use: test cases drafted with an AI assistant; reviewed and corrected by <your name>.
Corrections: 1 edited (wrong expected result), 1 rejected (invented rule).
```

### What If You Pasted Something by Mistake?

It happens. What matters is acting quickly and honestly:

1. **Stop.** Don't send more messages in that chat.
2. **Delete the chat** if your tool allows it. (This may not remove copies the provider has already stored, so continue with the next steps.)
3. **Tell your lead or security contact straight away.** Say what was pasted, which tool you used and when. Hiding it makes things worse.
4. **Rotate secrets.** If a password, API key or token was pasted, it must be changed. Treat it as leaked.
5. **Learn from it.** Add a redaction rule or a pre-flight check so it can't happen the same way again.

## Your Turn

1. **(In class, 3 min)** Redact this line by hand: `user=ali.khan@outlook.com phone=+1-555-0134 token=eyJhbGciOiJIUzI1NiJ9.abc123 status=500`. Which values did you replace? Would the Step 4 script catch **all** of them?
2. **(After class)** **Bias check.** Ask your AI for *"10 test names for a sign-up form."* How many are common English names? Write 5 more that your form must also accept: a name with an apostrophe (O'Brien), a hyphenated name, a name with accents (José), a very short name and a very long name.
3. **(After class)** Ask your AI: *"Explain this regex for a beginner: `[\w.+-]+@[\w-]+\.[\w.]+`"*. Check its explanation against the Step 4 demo.
4. **(After class)** Write a 4-line "AI usage policy" for your Project 2 team: which tool(s), what data must never be pasted, how AI use is disclosed, and who reviews AI output.

## Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| You missed a sensitive value | Sensitive data hides in many forms (phone numbers, tokens, addresses) | When unsure, redact it. Over-redacting is safer than leaking |
| Your redacted line is useless to the AI | You removed the field names or the error too | Keep the structure; replace only the **values** |
| A rule list misses a format (for example a phone number) | Scripts only catch the patterns they know | Always **read** the output before pasting, even when a script has run |

---

## Lecture Wrap-Up: Quick Check

1. An AI-written test uses `assert result`. Why is that a problem, and how do you prove it?
2. Name two user-facing Playwright locators.
3. What are the three review decisions, and what must every edit or rejection have?
4. What does "human-in-the-loop" mean?
5. Name three things you must redact before pasting a log into an AI tool.

<details>
<summary>Answers</summary>

1. It passes for **any** non-empty result, so it can't catch a wrong message. Prove it with the **"break it" check**: break the feature and see that the test still passes.
2. Any two of: `get_by_role`, `get_by_label`, `get_by_text` (also `get_by_placeholder`).
3. Accept, edit, reject. Edits and rejections need a **reason category** (and ideally a note).
4. AI drafts, and a named human reviews, approves and stays **accountable** for the result.
5. Any three of: emails and other personal data, card numbers, passwords, API keys and tokens.

</details>

---

## Glossary

| Term | Meaning |
|---|---|
| **Stand-in** | A simple replacement for a real system, used for learning or testing |
| **Mutation / "break it" check** | Deliberately breaking code to confirm a test fails |
| **User-facing locator** | A locator based on what users see (role, label, text) |
| **Human-in-the-loop** | A person reviews and approves AI output before it's used |
| **Automation bias** | Trusting a tool's output more than you should |
| **Correction log** | A record of each review decision and its reason |
| **Accepted-as-is rate** | The share of AI output used without changes |
| **Redaction** | Replacing sensitive values with placeholders |
| **Pre-flight check** | An automatic check before sending data to an AI tool |
| **Disclosure** | Stating openly that AI helped produce the work |
| **Accountability** | Being responsible for the result, even when AI helped |

## Summary

- A test isn't trustworthy until you've seen it **fail** for the right reason. Use the **"break it" check** on AI-written tests, and prefer **exact asserts** and **user-facing locators**.
- **Human validation** = checklist → accept / edit / reject → **record why**. The correction log shows what to fix in your prompts.
- **Responsible use:** redact before you prompt, follow your organisation's AI policy, disclose AI help, and stay accountable for everything you submit.
