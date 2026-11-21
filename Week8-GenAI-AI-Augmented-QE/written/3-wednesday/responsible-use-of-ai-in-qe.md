# Responsible Use of AI in QE

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **responsible AI use** means for a quality engineer, using eight practical principles: privacy, confidentiality, security, intellectual property, fairness, transparency, accountability and sustainability.
- Classify the data you work with (public, internal, confidential, restricted) and decide **what may and may not go into an AI tool**.
- **Redact** sensitive values (emails, card numbers, phone numbers, passwords, API keys) from bug reports and logs before prompting, and explain the limits of automatic redaction.
- Turn a team AI policy into a small **pre-flight check** in Python, and test your redactor with pytest.
- Recognise intellectual property, licensing and security risks in **AI-generated code**.
- Spot **bias** in AI-generated test data and scenarios, and measure it with a simple coverage check.
- Practise **transparency** (labelling AI-assisted work) and **accountability** (a named human owns every result), and keep an **AI usage log**.
- Describe, at a high level, how the **NIST AI Risk Management Framework**, the **EU AI Act** and **ISO/IEC 42001** relate to everyday QE work.

---

## Why This Matters

All week you have been adding a powerful tool to your kit. On Monday you learned how generative AI works; on Tuesday you learned to prompt it well; today you have seen AI help across the whole QA lifecycle: analysing requirements, generating test cases and test data, writing automation code, and being checked by a human reviewer. This last lesson of the day asks a different question: not "can AI do this?" but **"should I use AI here, with this data, in this way, and who is responsible for the result?"**

Think of a construction site. A nail gun is far faster than a hammer, and every professional crew uses one. But the crew also has rules: safety glasses on, never point it at a person, disconnect the air before clearing a jam, and the site supervisor signs off the work. Nobody thinks those rules are "anti-nail-gun". They are what lets the crew use the tool every day without anyone getting hurt. Responsible AI use is the same: a short set of habits that lets you use AI at full speed without leaking customer data, shipping someone else's licensed code, building biased test suites or handing over decisions nobody owns.

Quality engineers are in a special position here, for three reasons:

1. **You handle sensitive data constantly.** Bug reports contain customer emails. Logs contain session tokens. Test environments are sometimes refreshed from production. A tester who pastes one log into a public chatbot can cause a data breach without writing a single line of code.
2. **You are the last line of defence.** If AI-generated code or tests go wrong, the QE team is where the problem should be caught. A team that trusts AI output blindly removes that safety net.
3. **You are building AI into a framework.** The **Weekly Epic** ends with you designing and building your first QA agent on Thursday and Friday. The habits you form today (what data the agent may see, who reviews its output, how its use is recorded) become the rules that agent runs under.

It also feeds **Project 2 (Test Automation Framework)**: the redaction step, disclosure header and usage log from this lesson can go into your framework repository this week.

> **Scope note.** Earlier today, *Human Validation of AI Output* covered **how** to review AI output (the review checklist and correction log). This lesson covers the wider **rules of use**: what data AI may see, who owns results, how use is disclosed and recorded. **Prompt injection** is named here only; it is covered in depth in **Week 10**, together with the hallucination taxonomy and LLM-as-judge. Automated validation of an agent's output is covered on **Friday**. Nothing in this lesson is legal advice; your organisation's policy and legal team have the final say.

---

## The Concept

### 1. What "Responsible AI Use" Means for a Tester

"Responsible AI" is a phrase you will see in company policies, vendor marketing and government documents. It can sound vague, so let's make it concrete. For a QE using AI tools day to day, it comes down to eight principles. Each one is a question you ask before, during or after using an AI tool.

| # | Principle | The question you ask | A QE example |
|---|---|---|---|
| 1 | **Privacy** | Does this input contain personal data about real people? | A bug report with a customer's email and phone number |
| 2 | **Confidentiality** | Does this input contain company secrets? | Unreleased feature specs, proprietary source code, pricing rules |
| 3 | **Security** | Could this input or output create a security risk? | A pasted API key; AI-generated code that disables TLS checks |
| 4 | **Intellectual property (IP)** | Do we have the right to use this input and this output? | Generated code that copies a licensed open-source function |
| 5 | **Fairness** | Does the output treat all users fairly and represent them all? | Test data in which every customer is called "John Smith" |
| 6 | **Transparency** | Will people know AI was involved? | A test file with no note that it was AI-drafted |
| 7 | **Accountability** | Which named human owns this result? | "The AI wrote the test plan" with no reviewer listed |
| 8 | **Sustainability and cost** | Is AI the right tool for this job at this scale? | Sending 10,000 prompts where a 10-line script would do |

Notice that none of these says "don't use AI". They describe **conditions** for using it well. A useful mental model is a traffic light:

- **Green:** public or synthetic data, an approved tool, a human reviews the output. Go ahead.
- **Amber:** internal data, an approved tool, but the input needs redacting or the output needs extra review. Proceed with care.
- **Red:** restricted data (real customer records, credentials, regulated data), an unapproved tool, or no one available to own the result. Stop.

The rest of this lesson walks through each principle, with examples and small Python tools that turn the principles into habits.

---

### 2. Data Privacy and Confidentiality: What Goes Into the Prompt

#### 2.1 Why the prompt is a data transfer

When you type into an AI tool, your text leaves your machine. Depending on the tool and the contract your company has with the vendor, that text may be:

- **Stored** in the vendor's logs for some period (for abuse monitoring, debugging or your own chat history).
- **Read** by the vendor's staff in limited circumstances (for example, safety reviews).
- **Used to train** future models, in some consumer products or settings, unless that is switched off or excluded by contract.
- **Processed** by sub-processors in other countries.

You do not need to memorise any vendor's terms. You need one habit: **treat every prompt as if you were emailing that text to an outside company**, because in effect you are.

This is why most companies distinguish between:

- **Approved (enterprise) AI tools:** tools your company has a contract with, where inputs are not used for training, retention is limited, and security has reviewed the setup. Examples might be a company-licensed coding assistant or a self-hosted model.
- **Unapproved (consumer) AI tools:** free or personal accounts, browser extensions, random websites. Your company has no contract, so you have no guarantees.

Using unapproved AI tools for work is often called **shadow AI** (like "shadow IT"). It is the most common way well-meaning people leak data. The fix is simple: know which tools your team has approved and for which kinds of data.

#### 2.2 Data classification

Most organisations sort information into classes. The names vary, but four levels are typical:

| Class | Meaning | QE examples | Typical AI rule |
|---|---|---|---|
| **Public** | Already public or harmless if public | Published docs, open-source library code, the coupon rule "SAVE10 gives 10% off $50+" on the marketing site | Any approved tool |
| **Internal** | For employees; mild harm if leaked | Internal test plans, non-sensitive user stories like US-205, test code for the framework | Company-approved tools only |
| **Confidential** | Real harm if leaked | Unreleased features, proprietary algorithms, security test results, architecture diagrams | Only tools approved for confidential data (often self-hosted) |
| **Restricted** | Severe harm; often regulated | Real customer personal data, payment card data, passwords, API keys, health data | Never into an AI tool |

Two points trip up beginners:

1. **Classification follows the most sensitive item.** A bug report about the SAVE10 coupon is internal. The same bug report with a customer's card number pasted in is restricted. One line changes the class of the whole text.
2. **Test environments are not automatically safe.** If a staging database was refreshed from production, the "test" accounts may be real customers. Data is classified by what it is, not where it lives.

#### 2.3 Personal data in a QE's day

**Personal data** (in the EU's GDPR; **PII**, personally identifiable information, in US usage) is any information that relates to an identifiable person. Testers meet it more often than they expect:

- **Bug reports and support tickets:** "Customer maria.lopez@example.com cannot check out."
- **Application logs:** IP addresses, user IDs, emails, session tokens.
- **Screenshots and recordings:** names and addresses on the checkout page.
- **Database dumps and CSV exports:** whole tables of customer records.
- **HAR files and network traces:** cookies and authorisation headers.

Before any of these goes near an AI tool, it must either be **removed**, **replaced with synthetic data** (earlier today, *AI-Generated Test Data* showed why synthetic data is the default for testing), or **redacted**.

#### 2.4 Confidentiality: it is not only about customers

Privacy protects people; confidentiality protects the business. In QE you may handle:

- **Proprietary source code** (the application under test, and your own framework).
- **Unreleased product plans** (a user story for a feature that has not been announced).
- **Security findings** (a vulnerability you found during testing that is not yet fixed). These are among the most sensitive things a tester holds.
- **Third-party material** under NDA (a partner's API documentation).

A good default: if your company has an approved coding assistant, use that one for code. Never paste confidential or third-party material into a personal account.

---

### 3. Redaction Before Prompting

Sometimes you really do want AI help with a real artefact. For example, a checkout bug report is confusing and you want an AI to help you rewrite it clearly. **Redaction** means replacing the sensitive parts with placeholders before you send it, so the AI sees the **structure** of the problem but not the sensitive **values**.

#### 3.1 Redacting by hand first

Here is a real-looking bug report from the Project 2 checkout flow:

```text
Checkout fails for customer maria.lopez@example.com (phone 415-555-0134).
Card used: 4111 1111 1111 1111, exp 12/29.
Repro on staging with header Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc123
Config: STRIPE_KEY=sk_test_51HxYzAbCdEf  password=Winter2026!
Error: 500 Internal Server Error at /api/checkout
```

Go through it line by line and ask, "Does the AI need this exact value to help me?"

| Item | Sensitive? | Does the AI need the real value? | Replace with |
|---|---|---|---|
| `maria.lopez@example.com` | Yes, personal data | No; "a customer" is enough | `<EMAIL_1>` |
| `415-555-0134` | Yes, personal data | No | `<PHONE_1>` |
| `4111 1111 1111 1111` | Yes, card data (treat as real unless you know otherwise) | No | `<CARD_1>` |
| `Bearer eyJ...` | Yes, a credential | No | `<BEARER_1>` |
| `sk_test_51Hx...` | Yes, a secret key | No | `<API_KEY_1>` |
| `Winter2026!` | Yes, a password | No | `<PASSWORD_1>` |
| `500 ... /api/checkout` | No | Yes, this is the actual problem | Keep |

The result keeps everything that matters for debugging and nothing that would hurt if leaked. Notice the numbered placeholders: `<EMAIL_1>`, `<EMAIL_2>` and so on. Numbering keeps the text consistent. If the same customer appears twice, a smarter redactor gives both mentions the same placeholder, so the AI can still tell "the same person" from "a different person". This technique is called **pseudonymisation**: replacing identifiers with stand-ins. It is weaker than full **anonymisation**, where nothing in the text can be linked back to a person, but for prompting it is usually what you need.

> **Why redact the test card number?** `4111 1111 1111 1111` is a widely published test number, so it is harmless. But your redactor cannot know whether a 16-digit number is a test card or a real one. A redaction rule that tries to be clever ("skip known test cards") will one day skip a real card. **Err on the side of redacting.**

#### 3.2 A small regex redactor in Python

Doing this by hand every time is slow and easy to get wrong, so let's automate the common cases with **regular expressions** (regex), the pattern-matching mini-language from Python's `re` module.

```python
# redact.py
import re

# Each rule: (label, compiled pattern). Order matters: specific before general.
RULES = [
    ("API_KEY", re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{8,}\b")),
    ("AWS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("BEARER",  re.compile(r"(?i)\bBearer\s+[A-Za-z0-9\-._~+/]+=*")),
    ("PASSWORD", re.compile(r"(?i)\b(password|passwd|pwd)\s*[:=]\s*\S+")),
    ("EMAIL",   re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("CARD",    re.compile(r"\b\d(?:[ -]?\d){12,18}\b")),
    ("PHONE",   re.compile(r"\(?\b\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}\b")),
]


def redact(text: str) -> tuple[str, dict[str, int]]:
    """Replace sensitive values with placeholders like <EMAIL_1>.
    Returns the redacted text and a count of what was replaced."""
    counts: dict[str, int] = {}
    for label, pattern in RULES:
        def _replace(match: re.Match) -> str:
            counts[label] = counts.get(label, 0) + 1
            if label == "PASSWORD":            # keep the key name, hide the value
                return f"{match.group(1)}=<{label}_{counts[label]}>"
            return f"<{label}_{counts[label]}>"
        text = pattern.sub(_replace, text)
    return text, counts


if __name__ == "__main__":
    bug_report = """Checkout fails for customer maria.lopez@example.com (phone 415-555-0134).
Card used: 4111 1111 1111 1111, exp 12/29.
Repro on staging with header Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc123
Config: STRIPE_KEY=sk_test_51HxYzAbCdEf  password=Winter2026!
Error: 500 Internal Server Error at /api/checkout"""
    clean, found = redact(bug_report)
    print(clean)
    print(found)
```

Output:

```text
Checkout fails for customer <EMAIL_1> (phone <PHONE_1>).
Card used: <CARD_1>, exp 12/29.
Repro on staging with header Authorization: <BEARER_1>
Config: STRIPE_KEY=<API_KEY_1>  password=<PASSWORD_1>
Error: 500 Internal Server Error at /api/checkout
{'API_KEY': 1, 'BEARER': 1, 'PASSWORD': 1, 'EMAIL': 1, 'CARD': 1, 'PHONE': 1}
```

Let's walk through the code.

- **`RULES`** is a list of `(label, pattern)` pairs. `re.compile(...)` turns a regex string into a reusable pattern object. The `r"..."` prefix makes a **raw string**, so a backslash like `\b` reaches the regex engine unchanged instead of being treated as a Python escape.
- **Regex building blocks used here:**
  - `\b` is a **word boundary**: the edge between a word character (letter, digit, underscore) and anything else. It stops `AKIA...` matching inside a longer word.
  - `\d` means one digit; `[A-Za-z0-9]` means one letter or digit; `{8,}` means "8 or more of the previous thing"; `{12,18}` means "between 12 and 18".
  - `(?:...)` is a **non-capturing group**: it groups parts of a pattern without saving them for later.
  - `(...)` without `?:` is a **capturing group**: the PASSWORD rule captures the word `password`, `passwd` or `pwd` so we can keep it in the output.
  - `(?i)` at the start makes the pattern **case-insensitive**, so `Password=`, `PWD:` and `bearer` all match.
  - `\s*` means "any amount of whitespace, including none"; `\S+` means "one or more non-whitespace characters" (the password value).
- **The CARD pattern** `\b\d(?:[ -]?\d){12,18}\b` reads as: a digit, then 12 to 18 more digits, each optionally preceded by a space or hyphen. That covers `4111111111111111`, `4111 1111 1111 1111` and `4111-1111-1111-1111` (13 to 19 digits in total, the range used by payment cards).
- **Order matters.** The rules run top to bottom. `API_KEY` runs before `CARD`, so long digit runs inside a key are already gone before the card rule looks. `EMAIL` runs before `PHONE`, so digits in an email address are not mistaken for a phone number. Putting specific patterns before general ones is a common regex design rule.
- **`pattern.sub(_replace, text)`** finds every match and calls `_replace` with each one. Whatever `_replace` returns is put in place of the match. Defining `_replace` inside the loop lets it see the current `label` and update `counts`.
- **`counts.get(label, 0) + 1`** increments a counter that starts at 0 for a new label. The counter gives us numbered placeholders and a summary of what was found.
- **The return type** `tuple[str, dict[str, int]]` says we return two things: the cleaned text and the counts. Returning the counts matters: it lets other code make decisions (for example, "secrets were found, so warn the user"), which we use in Section 4.

#### 3.3 The limits of automatic redaction

A redactor is a safety net, not a guarantee. It is worth seeing its blind spots with your own eyes:

```python
# limits.py
from redact import redact

samples = [
    "Ship to Maria Lopez, 12 Oak Street, Springfield",   # name + address
    "Order 1234567890123456 was charged twice",           # long order number
    "Customer id: CUST-00921, DOB 1988-03-14",           # internal id + date of birth
]
for s in samples:
    clean, found = redact(s)
    print(clean, "|", found)
```

Output:

```text
Ship to Maria Lopez, 12 Oak Street, Springfield | {}
Order <CARD_1> was charged twice | {'CARD': 1}
Customer id: CUST-00921, DOB 1988-03-14 | {}
```

Three lessons from three lines:

1. **False negatives (missed data).** The name and street address went through untouched. Names and addresses have no fixed pattern, so regex cannot reliably find them. The same goes for the date of birth and the internal customer ID. More advanced tools use NLP **named entity recognition** (you saw spaCy's NER on Monday) to find names and places, but even those miss things.
2. **False positives (over-redaction).** The 16-digit order number was redacted as a card. That is a safe failure: the AI loses a little detail, but nothing leaks. When you design a redactor, **prefer false positives over false negatives**.
3. **A human still reads the text before sending.** The redactor does the boring 90%; you check the last 10%. This is the same "AI or tool does the bulk, human checks" pattern you saw earlier today in *Human Validation of AI Output*, applied to your own inputs.

#### 3.4 Testing the redactor (you are a QE, after all)

A redactor that silently stops working is worse than none, because people trust it. So test it like any other code, with pytest and `parametrize` from Week 4:

```python
# test_redact.py
import pytest
from redact import redact

@pytest.mark.parametrize("text, label", [
    ("contact a.b@example.com", "EMAIL"),
    ("card 4111-1111-1111-1111", "CARD"),
    ("call (415) 555-0134", "PHONE"),
    ("key sk_live_ABCDEFGH1234", "API_KEY"),
    ("AKIAABCDEFGHIJKLMNOP", "AWS_KEY"),
    ("PWD: hunter2", "PASSWORD"),
])
def test_sensitive_value_is_replaced(text, label):
    clean, found = redact(text)
    assert found.get(label) == 1
    assert f"<{label}_1>" in clean

def test_safe_text_is_unchanged():
    text = "HTTP 500 on POST /api/checkout after applying SAVE10"
    assert redact(text) == (text, {})
```

Running `python -m pytest -q test_redact.py` gives:

```text
.......                                                                  [100%]
7 passed in 0.04s
```

- Each row of the `parametrize` list becomes its own test: one per kind of sensitive data, written in a different format than the demo (hyphenated card, bracketed phone, `PWD:` with a colon) to check the patterns are not too narrow.
- `found.get(label) == 1` checks the right rule fired exactly once.
- `test_safe_text_is_unchanged` is the **negative test**: ordinary text, including the word `SAVE10` and the number `500`, must pass through unchanged. Without this test, someone could "improve" the phone pattern until it starts eating status codes, and nobody would notice.

Every time someone reports a leak the redactor missed, add it as a new row. Over time the test file becomes a record of every format your team has met.

---

### 4. Turning Policy into a Pre-Flight Check

Many teams write their AI rules in a wiki page that nobody reads. A QE can do better: turn the rules into a small function that runs before text is sent anywhere. Think of an aircraft **pre-flight checklist**: a short, mechanical check that catches the obvious problems every time.

Our example team policy says:

- A public chatbot may only see **public** data.
- The company-licensed assistant may see **public** and **internal** data.
- A self-hosted model may also see **confidential** data.
- **Restricted** data never goes into any AI tool.
- Everything is redacted first; if secrets were found, the person is reminded to **rotate** them.

```python
# preflight.py
from redact import redact

# Which data classifications each tool is approved for (example team policy).
APPROVED_TOOLS = {
    "public-chatbot": {"public"},
    "company-copilot": {"public", "internal"},
    "self-hosted-llm": {"public", "internal", "confidential"},
}

SECRET_LABELS = {"API_KEY", "AWS_KEY", "BEARER", "PASSWORD"}


def preflight(text: str, tool: str, classification: str) -> tuple[bool, str, list[str]]:
    """Decide whether `text` may be sent to `tool`.
    Returns (allowed, text_to_send, reasons)."""
    reasons = []
    if classification == "restricted":
        return False, "", ["Restricted data never goes into an AI tool."]
    if classification not in APPROVED_TOOLS.get(tool, set()):
        return False, "", [f"'{tool}' is not approved for {classification} data."]

    clean, found = redact(text)
    secrets = SECRET_LABELS & found.keys()
    if secrets:
        reasons.append(f"Secrets were present ({', '.join(sorted(secrets))}); "
                       "rotate them, because they were already copied once.")
    if found:
        reasons.append(f"Redacted before sending: {found}")
    return True, clean, reasons


if __name__ == "__main__":
    log_line = "Login failed for sam.chen@example.com with password=Hunter2 (HTTP 401)"
    for tool, cls in [("public-chatbot", "internal"),
                      ("company-copilot", "internal"),
                      ("company-copilot", "restricted")]:
        ok, to_send, why = preflight(log_line, tool, cls)
        print(f"{tool:16} {cls:11} allowed={ok}")
        if to_send:
            print("   send:", to_send)
        for r in why:
            print("   -", r)
```

Output:

```text
public-chatbot   internal    allowed=False
   - 'public-chatbot' is not approved for internal data.
company-copilot  internal    allowed=True
   send: Login failed for <EMAIL_1> with password=<PASSWORD_1> (HTTP 401)
   - Secrets were present (PASSWORD); rotate them, because they were already copied once.
   - Redacted before sending: {'PASSWORD': 1, 'EMAIL': 1}
company-copilot  restricted  allowed=False
   - Restricted data never goes into an AI tool.
```

How it works:

- **`APPROVED_TOOLS`** is the policy written as data: a dictionary mapping each tool name to a **set** of allowed classifications. Keeping policy as data (rather than buried in `if` statements) means a lead can update it without touching the logic.
- **`APPROVED_TOOLS.get(tool, set())`** returns an empty set for an unknown tool, so **anything not on the list is denied by default**. This "deny unless allowed" design is called an **allow-list**, and it is the safe choice: a new, unreviewed tool is blocked until someone approves it.
- **The order of checks is deliberate.** Restricted data is refused before anything else, with no redaction attempted, because no amount of redaction makes a real customer database export safe to send.
- **`SECRET_LABELS & found.keys()`** is a **set intersection**: which of the secret labels did the redactor actually find? If any, the user is told to rotate them.
- **f-string formatting** `{tool:16}` pads the tool name to 16 characters so the output lines up in columns.

Why "rotate"? A password or key that has been copied into a log, a ticket or a clipboard has already left its safe place. Redacting it before prompting stops it reaching the AI vendor, but it may already sit in the ticket system. The safe response to a leaked secret is to **rotate** it (issue a new one and revoke the old one), not to hope nobody saw it. This applies to test environments too: a staging Stripe test key that is pasted into a public chatbot should be rotated.

> **Real-world note.** Production-grade versions of this idea exist as **secret scanners** (tools that scan commits for keys before they are pushed) and **data loss prevention (DLP)** gateways that sit between employees and AI tools. Your 30-line version is for learning; the principle is the same.

---

### 5. Intellectual Property and Licensing of AI-Generated Code

You learned on Tuesday, in *AI-Assisted Coding and Debugging*, and earlier today, in *AI-Assisted Automation Development*, how AI can draft test code. There is a responsible-use side to that code that is easy to miss: **where did it come from, and are we allowed to use it?**

#### 5.1 The concerns, in plain language

1. **Copied code.** Models are trained on large amounts of public code, much of it open source. Most of the time a model produces new combinations of common patterns. Occasionally it can reproduce a recognisable chunk of a specific project almost word for word. If that project's **licence** has conditions (for example, a "copyleft" licence such as the GPL that requires derivative work to be released under the same licence), your company could be bound by conditions it never agreed to.
2. **Unclear ownership.** Laws in several countries are still settling who, if anyone, owns purely machine-generated output. For a QE this is mostly a matter for the legal team, but it is one reason companies want humans to meaningfully shape and review AI-drafted code.
3. **Your inputs.** IP flows both ways. Pasting a partner's proprietary SDK or a paid book's code examples into an AI tool may break the terms under which you got them.

> This is a high-level overview, not legal advice. Your organisation's policy decides what you do.

#### 5.2 Practical habits for QEs

- **Use the approved tool and its settings.** Some enterprise coding assistants offer a setting that blocks or flags suggestions matching public code, and some show the source and licence of a match. Your company decides how these are configured; know what they are.
- **Be suspicious of large, polished blocks.** Searching a distinctive line (on GitHub code search, for example) shows whether a 200-line "suggestion" exists elsewhere.
- **Prefer standard libraries and your own framework code.** If the AI suggests copying a helper, ask whether pytest, Playwright or the Python standard library already does the job.
- **Do not strip licence headers.** If you knowingly reuse open-source code, keep its licence notice and follow its terms, as you would without AI.
- **Keep a human in the authoring loop.** Code you have read, understood, adapted and tested is your team's work. Code pasted unread is a liability.

---

### 6. Security of AI-Assisted Work

Security overlaps with privacy (Section 2), but it deserves its own checklist, because AI can introduce risks in both directions: **into** the tool (your inputs) and **out of** it (the outputs you run).

#### 6.1 Risks in AI-generated test code

AI models learned from public code, and public code contains plenty of insecure shortcuts. Watch for these in AI-drafted framework code:

| Pattern | Why the AI suggests it | Why it is a problem | Safer approach |
|---|---|---|---|
| `requests.get(url, verify=False)` | It "fixes" a certificate error quickly | Turns off TLS checks, hiding real security defects | Install the correct CA certificate or configure the trust store |
| `PASSWORD = "Winter2026!"` in a test file | Simplest way to make a login test pass | Secrets end up in Git history forever | Read from environment variables or a secrets manager |
| SQL built with f-strings, e.g. `f"... WHERE email='{email}'"` | Short and readable | Opens the door to SQL injection in test utilities | Parameterised queries |
| Printing whole responses or tokens in logs | Helpful for debugging | CI logs are widely readable | Log status codes and IDs, not secrets |
| `pip install` of a package name you have never heard of | The model suggested an import | Models sometimes invent plausible package names; attackers register such names with malicious code | Confirm the package exists on PyPI, is the one you expect and is maintained before installing |

The last row is worth stressing. A model may confidently tell you to `pip install playwright-helpers-pro`. Whether or not that name exists today, someone could register it tomorrow. **Never install a dependency only because an AI named it.** Look it up first.

#### 6.2 Risks in what the AI can do

As AI tools gain the ability to take actions (run commands, open browsers, call APIs), a new class of risk appears: the tool might do something you did not intend. A QE should apply the **principle of least privilege**: give an AI-driven tool only the access the task needs. For example, an AI helper that drafts test cases does not need write access to the production database, or even to the shared staging database.

You will design what your own QA agent can and cannot do on **Thursday** and **Friday**. A related attack, **prompt injection** (where hidden instructions inside the data an AI reads try to take over its behaviour), is named here so you recognise the term; how it works and how to test for it are covered in **Week 10**.

---

### 7. Bias and Fairness in AI-Assisted Testing

#### 7.1 Where bias shows up for a tester

A model learns from its training data, and that data over-represents some languages, countries, names and writing styles. Ask for "8 customer names" and you will often get a list that looks like one country's most common names. Ask for "a shipping address" and you will often get a US address in a big city. None of this is malicious; it is the statistical "most likely" answer you learned about on Monday (next-token prediction favours common patterns). But in testing, **"most likely" is exactly the wrong goal**. Defects live in the uncommon cases.

Bias in AI-assisted testing shows up as:

- **Unrepresentative test data:** names without accents, apostrophes or hyphens; addresses from one country; ages between 25 and 45; only male and female options.
- **Narrow scenarios:** tests that assume a mouse user (no keyboard-only or screen-reader journeys), a fast connection, a desktop screen, English content.
- **Skewed risk judgements:** an AI ranking "rare" user groups as low priority because they are rare in its training data, not because they matter less to your business.

The result is a product that works well for the "typical" user and fails for others, for example a sign-up form that rejects `Siobhán O'Brien` or a checkout that cannot handle a two-letter surname. That is a fairness problem **and** a quality defect.

#### 7.2 Measuring name coverage

Let's make the bias visible. The `fake_llm` below stands in for an AI assistant (no real model is called); its answer is **illustrative**, but typical of what you will see when you ask for names without constraints.

```python
# name_coverage.py
import json

def fake_llm(prompt: str) -> str:
    """Stand-in for an AI assistant. ILLUSTRATIVE output only:
    a typical 'give me 8 customer names' answer with little variety."""
    return json.dumps([
        "John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis",
        "David Wilson", "Jessica Miller", "James Taylor", "Ashley Moore",
    ])

# Name shapes our real shoppers have and the form must accept.
CHECKS = {
    "non-ASCII letters (José, Zoë)":   lambda n: any(ord(c) > 127 for c in n),
    "apostrophe (O'Brien)":            lambda n: "'" in n,
    "hyphen (Smith-Jones)":            lambda n: "-" in n,
    "single name (mononym)":           lambda n: len(n.split()) == 1,
    "3+ parts (Ana María da Silva)":   lambda n: len(n.split()) >= 3,
    "very short part (Al Wu)":         lambda n: any(len(p) <= 2 for p in n.split()),
    "long name (> 30 chars)":          lambda n: len(n) > 30,
}

def coverage_report(names: list[str]) -> dict[str, int]:
    return {label: sum(check(n) for n in names) for label, check in CHECKS.items()}

if __name__ == "__main__":
    ai_names = json.loads(fake_llm("Generate 8 customer full names as a JSON array."))
    report = coverage_report(ai_names)
    for label, count in report.items():
        flag = "MISSING" if count == 0 else "ok"
        print(f"{label:34} {count}  {flag}")

    human_added = ["José Álvarez", "Siobhán O'Brien", "Mary Smith-Jones", "Teguh",
                   "Ana María da Silva Pereira", "Al Wu",
                   "Maximiliana Konstantinopoulou Vasquez"]
    print("\nAfter adding the names a reviewer chose:")
    missing = [l for l, c in coverage_report(ai_names + human_added).items() if c == 0]
    print("Still missing:", missing or "nothing")
```

Output:

```text
non-ASCII letters (José, Zoë)      0  MISSING
apostrophe (O'Brien)               0  MISSING
hyphen (Smith-Jones)               0  MISSING
single name (mononym)              0  MISSING
3+ parts (Ana María da Silva)      0  MISSING
very short part (Al Wu)            0  MISSING
long name (> 30 chars)             0  MISSING

After adding the names a reviewer chose:
Still missing: nothing
```

Walking through it:

- **`CHECKS`** maps a human-readable label to a **lambda**, a small one-line function. Each lambda takes a name `n` and returns `True` or `False`.
  - `ord(c) > 127` is true for any character outside basic ASCII, such as `é`, `ö` or `ñ`.
  - `n.split()` splits on whitespace, so `len(n.split())` counts name parts.
  - `any(...)` is true if at least one item is true.
- **`coverage_report`** uses a **dictionary comprehension**. For each label it counts how many names pass the check. `sum(...)` over `True`/`False` values works because Python treats `True` as 1 and `False` as 0.
- The first report shows that the AI's 8 names, all **valid**, cover **none** of the 7 name shapes. Every one of those test names would pass a buggy form that rejects accents, apostrophes or hyphens.
- The reviewer adds 7 names (one per missing shape), and the second report confirms full coverage.

Two takeaways:

1. **Correct is not the same as representative.** Nothing in the AI's list was wrong. The problem is what is **missing**, and a reviewer only spots missing things by having an explicit checklist. This is the "what did you not cover?" pattern from Tuesday, applied to fairness.
2. **Fix the prompt too, not only the output.** Next time, ask for coverage explicitly: "Include names with accents, apostrophes, hyphens, a single-word name, a name with 4 or more parts, a 2-letter surname and a name over 30 characters." Then still run the check, because the model may not follow every constraint.

#### 7.3 Accessibility is part of fairness

Fairness is not only about data. If your AI-generated test suite contains 40 mouse-driven UI tests and zero keyboard-only or screen-reader checks, it is biased toward one group of users. When you review AI-generated test cases, ask: **"Which users are not represented here?"** For Project 2, a quick win is to include a keyboard-only checkout journey and to prefer role-based locators such as `get_by_role` (Week 4), which also nudge your application toward accessible markup.

#### 7.4 When the product itself contains AI

If your product has AI features (recommendations, a support chatbot, fraud scoring at checkout), fairness also becomes something you **test in the product**, not only something you watch for in your tools. Testing AI features is covered in later weeks.

---

### 8. Transparency and Disclosure

**Transparency** means being open about when and how AI was used. It matters for three groups:

- **Your teammates and reviewers** need to know which parts were AI-drafted so they can review them with the right care (earlier today's *Human Validation of AI Output* lesson explained why fluent AI output tempts reviewers to skim).
- **Auditors and future maintainers** may need to reconstruct how a test suite or a test report was produced, months later.
- **Customers and regulators** increasingly expect it. The EU AI Act, for example, includes transparency obligations for certain AI systems (Section 11).

In QE practice, transparency is simple and cheap:

- A short **header comment** in AI-assisted files: `# AI-assisted: <tool> drafted cases; reviewed by <name> <date>`.
- A line in the **pull request description**: "Test data generator drafted with the company assistant; edge cases added and verified by me."
- A field in the **test case** or **bug report** in your test management tool: "Source: AI-assisted, human-reviewed."
- An entry in the team's **AI usage log** (Section 13).

Transparency only works if it is consistent. Because the usage log (Section 13) lists which files were AI-assisted, a tiny CI script can read it and fail the build if any of those files lacks the `# AI-assisted:` header in its first few lines. Try writing that check yourself as an extension of Practice Exercise 4.

> **Transparency is not a confession.** Labelling AI-assisted work does not mean the work is worse. It tells the reader what kind of review it had. Well-reviewed AI-assisted work, clearly labelled, is a sign of a mature team.

---

### 9. Accountability and Human Oversight

**Accountability** answers one question: **when this is wrong, who is responsible?** The responsible-use answer is always **a named person, never "the AI"**.

Consider two status updates after a defect escaped to production because a coupon boundary test was missing:

- "The AI generated the coupon tests and it missed the $50.00 boundary."
- "I generated the coupon tests with AI help and I did not check the boundary against AC1 of US-205. I have added the test and updated our review checklist."

The first sounds like an explanation but is an evasion: the AI cannot attend a post-mortem or be held to a standard. The second shows ownership and a fix.

In practice, accountability means:

- **Every AI-assisted artefact has an owner** (the person who prompted and shipped it) and, for anything that matters, a **reviewer** (a different person, where risk justifies it).
- **The owner can explain the artefact.** If you cannot explain why a test exists or why an expected result is correct, you are not ready to commit it. This is the same rule you used on Tuesday for AI-written code.
- **Decisions stay with humans.** AI can suggest a release risk rating; a person decides whether to ship. AI can draft a defect severity; a person confirms it. The EU AI Act and the NIST AI RMF (Section 11) both stress **human oversight** for exactly this reason.
- **Review depth matches risk.** A typo fix needs no ceremony; AI-generated tests for payment or login logic deserve the documented review from *Human Validation of AI Output*.

---

### 10. Over-Reliance and Deskilling

There is a quieter risk that does not appear in any data breach report: **getting worse at your job because the AI does the thinking.** This is called **deskilling**. A tester who always asks the AI for boundary values may slowly lose the ability to see boundaries themselves, and then cannot spot when the AI gets them wrong. The more you rely on the tool, the less able you are to check it: a trap.

Related is **automation bias**, which you met earlier today: the tendency to trust a machine's output more than your own judgement, especially when you are tired or busy.

Habits that protect your skills:

- **Think first, then prompt.** Spend two minutes listing your own test ideas for US-205 before asking the AI. Then compare. You learn from the differences, and your list anchors the review.
- **Explain it back.** After accepting AI-generated code, explain each line aloud or in a comment. If you cannot, ask the AI to explain it (Tuesday's line-by-line pattern) and then verify one claim in the official docs.
- **Do "no-AI" reps.** Occasionally design a small suite or a page object entirely by hand, as pilots still practise manual landings.
- **Learn from the corrections.** Your correction log (from *Human Validation of AI Output*) is a list of things the AI got wrong. Read it; it is a personalised study guide.

---

### 11. Frameworks and Regulations (the Big Picture)

You do not need to become a compliance expert, but you should recognise the main frameworks your company may refer to. Here are three, described at a high level.

#### 11.1 NIST AI Risk Management Framework (AI RMF)

The US **National Institute of Standards and Technology (NIST)** published the **AI RMF 1.0** in January 2023, and a companion **Generative AI Profile (NIST AI 600-1)** in July 2024 that lists risks specific to generative AI. It is **voluntary** guidance used widely by organisations, including outside the US. It organises AI risk work into four functions:

| Function | Meaning | What it looks like for a QE team |
|---|---|---|
| **Govern** | Culture, policies, roles and accountability | The team AI usage policy; named owners and reviewers |
| **Map** | Understand the context and identify risks | Knowing which data classes each AI use touches; listing what could go wrong |
| **Measure** | Analyse, assess and track risks | Correction rates from reviews; the name-coverage check; redactor tests |
| **Manage** | Prioritise and act on risks | Blocking unapproved tools; rotating leaked keys; tightening a prompt |

Notice how much of this lesson fits naturally into those four boxes. That is the point: good QE practice already looks like risk management.

#### 11.2 The EU AI Act

The **EU Artificial Intelligence Act** is a law that applies to AI systems placed on the market or used in the EU, including by companies based elsewhere that serve EU users. It takes a **risk-based approach** with four tiers:

- **Unacceptable risk:** banned practices (for example, social scoring).
- **High risk:** allowed, but with strict obligations such as risk management, data quality, logging, documentation and **human oversight** (for example, AI used in hiring, credit scoring or critical infrastructure).
- **Transparency risk:** systems such as chatbots and generated content must be disclosed or labelled.
- **Minimal risk:** most everyday AI (spam filters, for example), with no specific new rules.

Its obligations phase in over several years. As of October 2026 (dates checked against the European Commission's AI Act page):

- **1 August 2024:** the Act entered into force.
- **2 February 2025:** prohibited practices and **AI literacy** obligations began to apply.
- **2 August 2025:** rules for general-purpose AI models and governance began to apply.
- **2 August 2026:** most remaining provisions, including the main transparency rules, apply.
- A 2026 amending regulation, known as the **"AI Omnibus"** (in force since late July 2026), **postponed** the high-risk obligations: to **2 December 2027** for high-risk use cases listed in Annex III, and **2 August 2028** for AI built into regulated products (Annex I). It also softened the AI literacy duty to one of *supporting* staff AI literacy, and added a new prohibited practice from December 2026.

Dates like these can change again, so always check the official source rather than a summary (including this one).

Why does a tester care? Two reasons. First, if your company builds AI features for EU users, QE will be asked to produce **evidence**: test results, logs, documentation of human oversight. Second, the **AI literacy** expectation means companies are training staff to use AI knowingly, which is what this week is.

#### 11.3 ISO/IEC 42001, and how it all reaches you

**ISO/IEC 42001:2023** is an international standard for an **AI management system**: organisational processes for governing AI, similar in spirit to ISO 27001 for information security. For a QE it shows up as process: documented policies, records of AI use and reviews. The AI usage log in Section 13 is exactly that kind of record.

You will rarely read these documents at work. What you will see is your **company's AI policy**, usually written with them in mind. Your job is to follow it, raise questions when a situation is not covered, and produce evidence (logs, reviews, disclosures) that it was followed.

---

### 12. Sustainability and Cost

Every model call uses computing power, energy and money. A single prompt is cheap; a pipeline that sends a 5,000-test regression suite to a large model on every commit is not. Ask, **"Is AI the right tool here?"** Deterministic work (computing boundary values, checking a ZIP code format, deduplicating test IDs) is a job for a few lines of Python: free, instant and exactly repeatable. Use AI for the parts that need language understanding, reuse reviewed output when the input has not changed, and use smaller models for simple formatting tasks.

---

### 13. A Team AI Usage Policy and an AI Usage Log

#### 13.1 A one-page policy

Policies work best when they are short enough to remember. Here is a template a Project 2 team could adapt:

```text
PROJECT 2 – AI USAGE POLICY (v1)

1. Tools: only the company-approved assistant. No personal accounts or browser extensions.
2. Data: public and internal data only. Never customer data, credentials,
   production logs or security findings. Run redact.py on any real artefact first.
3. Secrets: if a secret was pasted anywhere, rotate it the same day.
4. Ownership: the person who prompts owns the output. Payment, login and
   checkout logic also need a second reviewer.
5. Review: use the team review checklist; record corrections in the correction log.
6. Disclosure: AI-assisted files start with "# AI-assisted: <tool>; reviewed by <name> <date>".
   Mention AI help in the pull request description.
7. Dependencies: never install a package only because an AI suggested it. Check it first.
8. Fairness: test data must pass the name and address coverage checks.
9. Logging: record each significant AI use in ai_usage_log.csv.
10. When unsure: ask the QE lead before sending, not after.
```

#### 13.2 Recording AI use

The **AI usage log** is the team's memory: who used which tool, for what, with what data, and who reviewed it. It supports accountability (Section 9), transparency (Section 8) and the "Measure" function of the NIST AI RMF (Section 11).

```python
# ai_usage_log.py
import csv
from dataclasses import dataclass, asdict, fields
from pathlib import Path

@dataclass
class AIUsageRecord:
    date: str            # when the AI was used
    who: str             # the person accountable for the output
    tool: str            # which approved tool
    purpose: str         # what it was used for
    data_class: str      # public / internal / confidential
    redacted: bool       # was the input redacted first?
    artifact: str        # what was produced (file, ticket, PR)
    reviewed_by: str     # human reviewer ("" if not yet reviewed)
    outcome: str         # accepted / edited / rejected

LOG = Path("ai_usage_log.csv")

def append(record: AIUsageRecord) -> None:
    new_file = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[fl.name for fl in fields(AIUsageRecord)])
        if new_file:
            writer.writeheader()
        writer.writerow(asdict(record))

def audit(path: Path = LOG) -> list[str]:
    """Return problems a lead would want to see before a release."""
    problems = []
    with path.open(encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):   # row 1 is the header
            if not row["reviewed_by"]:
                problems.append(f"line {i}: {row['artifact']} has no human reviewer")
            if row["data_class"] != "public" and row["redacted"] != "True":
                problems.append(f"line {i}: {row['data_class']} data sent without redaction")
    return problems

if __name__ == "__main__":
    LOG.unlink(missing_ok=True)
    append(AIUsageRecord("2026-10-21", "priya", "company-copilot",
                         "draft test cases for US-205", "internal", True,
                         "tests/test_coupon.py", "marcus", "edited"))
    append(AIUsageRecord("2026-10-21", "dev-team", "company-copilot",
                         "summarise checkout failure logs", "internal", False,
                         "BUG-482", "", "accepted"))
    print(LOG.read_text(encoding="utf-8"))
    for p in audit():
        print("AUDIT:", p)
```

Output:

```text
date,who,tool,purpose,data_class,redacted,artifact,reviewed_by,outcome
2026-10-21,priya,company-copilot,draft test cases for US-205,internal,True,tests/test_coupon.py,marcus,edited
2026-10-21,dev-team,company-copilot,summarise checkout failure logs,internal,False,BUG-482,,accepted

AUDIT: line 3: BUG-482 has no human reviewer
AUDIT: line 3: internal data sent without redaction
```

Key parts of the code:

- **`@dataclass`** generates the boilerplate for a simple record class: an `__init__` that takes the fields in order, a readable `repr`, and equality. Each field has a type hint and a comment, so the record is self-documenting.
- **`asdict(record)`** converts the dataclass to a dictionary, and **`fields(AIUsageRecord)`** lists its fields in order. Using them means the CSV columns always match the class: add a field to the class and the CSV gets a new column automatically.
- **`csv.DictWriter`** writes dictionaries as CSV rows. `newline=""` is required when opening CSV files in Python, otherwise blank lines can appear on Windows. `encoding="utf-8"` keeps names like `José` intact.
- **`new_file = not LOG.exists()`** writes the header only once, when the file is first created; later calls open the file in append mode (`"a"`).
- **`audit`** reads the log back with `csv.DictReader` and applies two rules: every artefact needs a reviewer, and non-public data must have been redacted. `enumerate(..., start=2)` numbers rows from 2 because line 1 is the header, so the messages match what you see if you open the file.
- **CSV stores everything as text**, so the boolean `True` comes back as the string `"True"`. That is why the audit compares with `!= "True"`. It is a small but classic CSV pitfall.

The second record fails both audit rules. Look again and you will see a third problem the code does not catch: `who` is `dev-team`. A team is not an accountable person. As an exercise below, you will add that check.

---

### 14. Putting It Together: A Worked Scenario

Let's follow one realistic situation from start to finish.

**Situation.** It is Wednesday afternoon. Checkout on the staging environment of the Project 2 e-commerce app fails intermittently after applying `SAVE10`. You have a 300-line server log and a customer-facing support ticket that a colleague forwarded. You want AI help to (1) summarise the log, (2) draft a clear bug report and (3) draft regression tests for US-205.

1. **Classify.** The support ticket holds a real customer's email and card digits: **restricted**. The server log holds session tokens and emails: **internal, and restricted until redacted**. US-205 is **internal**.
2. **Choose the tool.** Policy allows the company assistant for internal data, so you do not use your personal chatbot account, even though it is open in another tab.
3. **Minimise and redact.** You do not need the ticket at all; the log shows the problem. You cut the log to the 40 lines around the failures (**data minimisation**: send only what the task needs), run `preflight.py` and read the result. It replaced 6 emails and 3 bearer tokens and flagged a password in a debug line. You spot a customer's full name in a stack trace that the redactor missed and replace it by hand.
4. **Rotate.** The debug line exposed a staging database password, so you tell the platform team, who rotate it.
5. **Prompt and review.** The AI's draft tests missed the $50.00 boundary and used one customer name; your review checklist catches the first, the name coverage check catches the second.
6. **Disclose and log.** The test file gets an `# AI-assisted:` header, the pull request mentions AI help, and `ai_usage_log.csv` records you as owner and a teammate as reviewer.
7. **Own it.** At stand-up: "I drafted the checkout regression tests with the assistant, reviewed and corrected them, and Marcus reviewed them too."

None of these steps took long. Together they are the difference between "we use AI" and "we use AI responsibly".

---

### 15. Connecting to Project 2

This week's Project 2 work brings AI into your test automation framework. Concrete responsible-use steps you can add now:

- **Add `redact.py`, `preflight.py` and `test_redact.py`** to a `tools/` folder in your framework repository, and run the redactor tests in your normal test run.
- **Add a disclosure header** to every AI-assisted test file and a "Source: AI-assisted, human-reviewed" field to AI-generated test cases.
- **Keep `ai_usage_log.csv`** in the repository (it contains no sensitive values, only descriptions), and run `audit()` before each milestone.
- **Use synthetic data only** in prompts and fixtures (*AI-Generated Test Data*, earlier today), and run the name coverage check on generated customer data.
- **Write your team's one-page AI policy** using the template in Section 13 and agree it as a team.

When you design your QA agent on Thursday and Friday, ask: **What data may it see? What may it do? Who reviews its output? How is its use recorded?**

---

## Practice Exercises

1. **Classify and decide.** For each item, give its data class (public, internal, confidential, restricted) and say whether it may go to (a) a public chatbot, (b) the company-approved assistant: the US-205 acceptance criteria; a staging log line containing `Authorization: Bearer ...`; the SAVE10 rule as printed on the public marketing site; a list of unfixed security defects; a CSV export of 500 real customer addresses.
2. **Extend the redactor.** Add rules for (a) IPv4 addresses (`192.168.1.20`) and (b) US Social Security numbers (`123-45-6789`). Make sure the SSN rule runs before the PHONE rule, and explain why the order matters. Add a parametrized test row for each and a negative test showing that the version string `v1.2.3` is not redacted.
3. **Consistent placeholders.** Change `redact` so that the same value always gets the same placeholder (for example, `maria@example.com` is `<EMAIL_1>` both times it appears, and a different email is `<EMAIL_2>`). Hint: keep a dictionary from original value to placeholder.
4. **Audit accountability.** Extend `audit()` to flag any record whose `who` field contains `team` or is empty, with the message "no accountable person".
5. **Address coverage.** Write `address_coverage.py` in the style of `name_coverage.py` for US-310 shipping addresses. Include checks for: an apartment or unit number, a street name with a non-ASCII character, a city with a space or hyphen, a ZIP code with a leading zero (for example `02134`), and a very long street line. Run it against an illustrative list of five "typical" AI-generated addresses and record what is missing.
6. **Spot the risks.** Review the AI-drafted snippet below and list every responsible-use problem you find (there are at least four):

   ```python
   import requests
   ADMIN_PASSWORD = "Winter2026!"
   def test_checkout_api():
       r = requests.post("https://staging.shop.example/api/checkout",
                         json={"code": "SAVE10"}, auth=("admin", ADMIN_PASSWORD), verify=False)
       print(r.text)
       assert r.status_code
   ```


---

## Knowledge Check

1. Why should you treat every prompt to an AI tool as a data transfer to an outside company?
2. A bug report about the SAVE10 coupon is internal. A colleague pastes a customer's card number into it. What is the data class now, and why?
3. What is the difference between a false negative and a false positive in redaction, and which one should a redactor prefer?
4. In `preflight.py`, why does an unknown tool name get denied, and what is this design called?
5. You accidentally pasted a staging API key into a public chatbot. Redacting the chat afterwards is not possible. What should you do, and why?
6. Name three security risks that commonly appear in AI-generated test code.
7. An AI generates eight valid customer names for your test data. Why might this data still be a quality and fairness problem?
8. Which statement shows accountability: "The AI missed the boundary" or "I missed the boundary when reviewing the AI's tests"? Why does this matter?
9. What are the four functions of the NIST AI RMF?
10. What is the EU AI Act's general approach to regulating AI, and why might a QE team be asked for evidence related to it?

<details>
<summary>Answers</summary>

1. Your text leaves your machine and may be stored, logged, reviewed by vendor staff, processed by sub-processors or (in some products and settings) used for training. Unless your company has a contract that says otherwise, you have no control over what happens to it.
2. Restricted. Classification follows the most sensitive item in the text; one card number makes the whole report restricted.
3. A false negative is sensitive data the redactor misses (it leaks); a false positive is harmless data it redacts unnecessarily (the AI loses a little detail). Prefer false positives, because over-redaction is a safe failure and under-redaction is a leak.
4. `APPROVED_TOOLS.get(tool, set())` returns an empty set for an unknown tool, so no classification is allowed. This is an allow-list ("deny unless explicitly allowed"), which blocks new, unreviewed tools by default.
5. Report it and rotate the key (issue a new one and revoke the old one), the same day. Once a secret has left its safe place you cannot know who has it, so the only safe fix is to make it useless.
6. Any three of: `verify=False` disabling TLS checks; hard-coded passwords or keys; SQL built with string formatting (injection risk); logging tokens or full responses; installing packages an AI named without checking they are genuine.
7. Valid is not the same as representative. If none of the names contain accents, apostrophes, hyphens, single names or unusual lengths, a form that wrongly rejects those names will pass every test. That is a defect that affects some groups of users more than others.
8. "I missed the boundary when reviewing the AI's tests." It names a responsible person who can learn and change the process. "The AI missed it" assigns blame to something that cannot be held accountable or attend a retrospective.
9. Govern, Map, Measure, Manage.
10. It is risk-based: banned practices, high-risk systems with strict obligations (including human oversight, logging and documentation), transparency obligations, and minimal-risk systems. If the company provides or uses AI covered by it, QE may need to supply test results, logs and records of human oversight as evidence.

</details>

---

## Glossary

- **Responsible AI use:** Using AI tools in a way that protects privacy, confidentiality and security, respects IP, is fair and transparent, and keeps a named human accountable.
- **Shadow AI:** Using AI tools that the organisation has not approved for work (personal accounts, unvetted extensions).
- **Data classification:** Sorting information into levels such as public, internal, confidential and restricted, each with its own handling rules.
- **Personal data / PII:** Information relating to an identifiable person, such as name, email, phone number or address.
- **Redaction:** Removing or replacing sensitive values in text before sharing it.
- **Pseudonymisation:** Replacing identifiers with consistent stand-ins (for example, `<EMAIL_1>`), so the structure is kept but the identity is hidden.
- **Allow-list:** A list of explicitly permitted items; anything not on it is denied by default.
- **Secret rotation:** Replacing a credential with a new one and revoking the old one, usually after it may have been exposed.
- **Prompt injection:** An attack in which instructions hidden in data an AI reads try to override its intended behaviour (covered in Week 10).
- **Bias (in AI output):** A systematic skew in output, often toward what is most common in the training data.
- **Transparency / disclosure:** Making it clear when and how AI was used.
- **Accountability:** A named person being responsible for a result and its consequences.
- **NIST AI RMF:** A voluntary US framework for managing AI risk, organised into Govern, Map, Measure and Manage.
- **EU AI Act:** An EU law regulating AI using a risk-based approach, with obligations phased in from 2025 to 2028.
- **AI usage log:** A record of significant AI use: who, which tool, what for, which data, who reviewed it.

---

## Summary

- Responsible AI use is not "less AI"; it is the set of habits that lets you use AI at full speed safely. Eight principles guide it: privacy, confidentiality, security, IP, fairness, transparency, accountability and sustainability.
- **Every prompt is a data transfer.** Classify your data, use only approved tools for each class, and never send restricted data (customer records, credentials, card data) to any AI tool.
- **Redact before prompting** and read the result: regex catches structured values like emails, cards and keys, but misses names and addresses. Prefer over-redaction. Test your redactor like any other code.
- Turn policy into a small **pre-flight check** with an allow-list, and **rotate** any secret that was exposed.
- Treat AI-generated code with care for **licensing** and **security**: watch for copied code, `verify=False`, hard-coded secrets, injection-prone SQL and invented package names.
- AI output tends toward the common case; testing needs the uncommon one. **Measure coverage** of names, addresses and user groups to catch bias.
- **Disclose** AI-assisted work, keep a **named owner** and reviewer for every artefact, and protect your own skills from **over-reliance**.
- NIST AI RMF, the EU AI Act (risk-based, phasing in through 2028 after the 2026 AI Omnibus changes) and ISO/IEC 42001 frame what your company's policy asks of you. A one-page team policy and an AI usage log make it real for Project 2.

---

## Additional Resources

- NIST, *AI Risk Management Framework* (the AI RMF 1.0, its Govern/Map/Measure/Manage functions and the Generative AI Profile, NIST AI 600-1): https://www.nist.gov/itl/ai-risk-management-framework
- European Commission, *AI Act* (official overview of the four risk tiers and the current application timeline, including the AI Omnibus changes): https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- ISO, *ISO/IEC 42001:2023 – AI management systems* (what an organisational AI management system standard covers): https://www.iso.org/standard/42001
