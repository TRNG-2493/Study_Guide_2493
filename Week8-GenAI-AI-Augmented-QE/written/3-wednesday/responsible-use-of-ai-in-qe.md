# Responsible Use of AI in QE

## Learning Objectives

By the end of this lesson you will be able to:

- **Explain** what responsible use of AI means for a tester: protecting data, following policy, disclosing AI help and staying accountable.
- **Identify** sensitive values in logs, bug reports and test data before they reach an AI tool.
- **Redact** a log line by hand, and explain how a redaction script and a pre-flight check work.
- **Test** a redaction script, and recognise that it only catches the patterns it knows.
- **Respond** correctly if sensitive data is pasted into an AI tool by mistake.

---

## Why This Matters

Testers handle sensitive data all the time, often without thinking of it that way. Bug reports contain customer emails. Logs contain session tokens. Test environments are sometimes copied from production. A stack trace can include an API key. When something fails and you want help understanding it, the fastest move is to copy the whole thing into an AI assistant, and that is exactly the moment the risk appears.

This is not a theoretical risk. In 2023, Samsung engineers accidentally leaked internal source code by uploading it to ChatGPT, and the company responded by banning generative AI tools on company devices and networks ([Bloomberg, via Yahoo Finance](https://ca.finance.yahoo.com/news/samsung-bans-generative-ai-staff-004831399.html)). Nobody wrote malicious code. Someone pasted text into a chat window to get help with their work.

Security professionals now rank this kind of problem very highly. The OWASP Top 10 for Large Language Model Applications 2025 lists **Sensitive Information Disclosure** as the second most critical risk, up from sixth place in the original 2023 list ([Infosecurity Magazine](https://www.infosecurity-magazine.com/news/owasp-data-exposure-risk-ai/)).

The good news is that one simple habit prevents most problems: **redact before you prompt**, and **if in doubt, don't paste**. This lesson teaches that habit, shows how teams automate it, and is honest about where automation falls short.

> **Using this with the handout:** this lesson goes deeper into **Handout 06, Topic 3**. It uses the same rules of the road, the same failing checkout log line, the same placeholders, the same `redact.py`, the same disclosure line and the same five steps for a mistaken paste.

---

## The Concept

### 1. What Is Responsible Use of AI?

**Responsible use of AI** means using AI tools in ways that are **safe, legal, fair and honest**:

- **Safe:** protecting private and confidential data.
- **Legal:** respecting privacy laws, licences and your organisation's rules.
- **Fair:** checking that AI-assisted work does not leave people out, for example in test data.
- **Honest:** being open about when AI helped, and staying **accountable** for the result.

For testers, the first one matters most day to day, because of the data we handle. But all four come up in ordinary QE work, as the rest of this lesson shows.

### 2. The Rules of the Road

The handout summarises responsible use in six rules:

| Rule | In practice |
|---|---|
| **Protect data** | Never paste passwords, keys, customer personal data or confidential code into tools your company has not approved |
| **Redact first** | Replace sensitive values with placeholders: `<EMAIL>`, `<CARD>` |
| **Disclose** | Say when AI helped: "Test cases drafted with AI, reviewed by J. Singh" |
| **Stay accountable** | You own what you submit, even if AI wrote the first draft |
| **Check licences and security** | AI-generated code may copy licensed code or contain security flaws, so review it like any code |
| **Watch for bias** | AI test data can be narrow (only English names, only US addresses), so check that it reflects your real users |

Two ideas sit behind all six. **Follow your organisation's AI policy**, which says which tools are approved and for which data. And **when unsure, ask before pasting**. Asking takes a minute; a leak cannot be undone.

### 3. What Counts as Sensitive?

Sensitive data is any value that could harm a person or the company if it reached the wrong place. In QE work, it usually falls into a few groups:

| Group | Examples in a tester's day | Why it is sensitive |
|---|---|---|
| **Personal data** | Customer names, emails, phone numbers, addresses | Belongs to real people; protected by privacy laws |
| **Payment data** | Card numbers, bank details | Can be used for fraud; strictly regulated |
| **Secrets** | Passwords, API keys, session tokens | Anyone holding them can act as the system or the user |
| **Confidential company data** | Source code, internal URLs, unreleased features | Belongs to the company; can help attackers or competitors |

Sensitive values also hide in places that do not look like data: a screenshot of a test failure showing a customer's address, a URL with a session ID in it (`?session=...`), a database connection string in a config file, or an error page that prints the server's internal path. Before pasting **anything**, including screenshots, scan it for these.

Notice that "test" data can still be sensitive. A **test-environment** API key can often reach real systems. A test environment **copied from production** contains real customers. The question is not "is this a test?" but "would it matter if this value leaked?"

### 4. Worked Example: Redact Before You Prompt

**The situation:** a checkout test failed, and you want an AI assistant to help you understand the log. But the log contains private data. **Never paste it as it is.**

```text
2026-11-20 09:14:03 ERROR checkout failed for customer=priya.sharma@gmail.com card=4111 1111 1111 1111 api_key=sk_live_8f2aQ91xZ password=Summer2026!
```

All the values here are fake. 4111 1111 1111 1111 is a well-known **test** card number. But treat the line as if it were real: that is the habit you are building.

#### Step 1: Spot the sensitive values

Read the log line and list **every** value that must not be sent to a public AI tool, and **why**. Do it on paper first.

**Answer:**

| Value | Type | Why it is sensitive |
|---|---|---|
| `priya.sharma@gmail.com` | Email | A real customer's **personal data** |
| `4111 1111 1111 1111` | Card number | **Payment data** |
| `sk_live_8f2aQ91xZ` | API key | A **secret**: anyone with it can call the system. The `live` in the name suggests production |
| `Summer2026!` | Password | A **secret**. It should never be in a log at all |

The last row is worth a second thought. A password in a log is a bug in its own right: logging code should never write secrets. A good tester notes it as a separate finding.

#### Step 2: Redact by hand

Rewrite the line, replacing each sensitive value with a **placeholder** in angle brackets: `<EMAIL>`, `<CARD>`, `<API_KEY>`, `<PASSWORD>`. Keep everything the AI needs to help you debug: the **time**, the **error** and **which fields** were involved.

```text
2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>
```

Check your redacted line:

- ✅ All four values replaced.
- ✅ The time, the error and the field names (`customer=`, `card=` and so on) are kept.
- ✅ You will paste only the **redacted** version into the AI.

The second point matters as much as the first. A line redacted to `<REDACTED> <REDACTED>` is safe but useless: the AI cannot help if it cannot see what kind of failure happened.

#### Step 3: Ask for help, safely

Paste **your redacted line**, never the original, into your AI assistant:

```text
This checkout test failed. Here is the redacted log line. Sensitive values have been
replaced with placeholders in angle brackets.

2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>

What are the most likely causes of the failure, and what should I check first?
```

The AI can still help. The placeholders tell it **what kind** of value was there, which is all it needs. A useful reply, **illustrative**, might suggest checking whether the payment service accepted the API key, whether the test card is allowed in that environment, and why a password appears in a checkout log at all.

#### Step 4: See the redaction automated

Doing this by hand for every log is not realistic. Teams use a small script: a list of patterns for each kind of sensitive data, plus a **pre-flight check** that refuses to send text if anything sensitive is left. Save this as `redact.py` and run `python redact.py`. You do not need to understand every line:

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

It prints:

```text
2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>
Original safe to send? False
Redacted safe to send? True
```

The script's output matches your hand-redacted line exactly.

### 5. How the Script Works

Each rule pairs a **label** with a **pattern**: a regular expression, from Monday's NLP lesson, that finds one kind of value. In plain words:

| Label | Pattern, in plain words |
|---|---|
| `EMAIL` | Some name characters, an `@`, a domain, a dot, and more domain |
| `CARD` | A digit followed by 12 to 15 more digits, each optionally after a space or hyphen: 13 to 16 digits in all |
| `API_KEY` | `sk_live_` or `sk_test_` followed by letters and digits |
| `PASSWORD` | Whatever comes straight **after** `password=`, up to the next space |

The `PASSWORD` rule uses a **lookbehind**, `(?<=password=)`: it finds text that comes after `password=` without replacing `password=` itself, which is why the field name survives. The `[^<\s]` part stops the rule from matching a placeholder that is already there.

The two functions do different jobs:

- `redact(text)` replaces every match with `<LABEL>`.
- `safe_to_send(text)` is the **pre-flight check**: it returns `False` if any pattern still matches. In a team's tooling, nothing is sent to an AI unless this returns `True`.

The handout's tip applies here: asking an AI to **explain** a regex like these is a great use of AI. Asking it to **write** one is fine too, but **test the result** on real examples before trusting it. The next section shows why.

### 6. The Limits of a Redaction Script

A script only catches the patterns it knows. Try the handout's Your Turn line on the same `redact.py`:

```text
user=ali.khan@outlook.com phone=+1-555-0134 token=eyJhbGciOiJIUzI1NiJ9.abc123 status=500
```

The redacted line, followed by the pre-flight result for it:

```text
user=<EMAIL> phone=+1-555-0134 token=eyJhbGciOiJIUzI1NiJ9.abc123 status=500
True
```

The email is redacted. The **phone number** and the **token** are not, because there are no rules for them. And the pre-flight check says the result is **safe to send**. This is the most important result in the lesson: **a pre-flight check can only be as good as its rules.** A `True` means "none of my patterns match", not "this text is safe".

So add two rules. A first attempt at a phone rule might look for "a long run of digits, spaces and hyphens":

```python
    ("PHONE",    r"\+?\d[\d -]{7,}\d"),
    ("TOKEN",    r"(?<=token=)[^<\s]\S*"),
```

The new line is now fully redacted. But re-run the **original** checkout log as well, and look at the start of the output:

```text
<PHONE>:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>
```

The phone rule has eaten the **timestamp**: `2026-11-20 09` is a run of digits, spaces and hyphens too. The log is still safe, but the AI can no longer see when the failure happened, and anyone reading it would be confused. This is **over-redaction**: removing information that was not sensitive.

A safer fix uses the field name, like the password rule does:

```python
    ("PHONE",    r"(?<=phone=)[^<\s]\S*"),
```

Now both lines come out right:

```text
user=<EMAIL> phone=<PHONE> token=<TOKEN> status=500
2026-11-20 09:14:03 ERROR checkout failed for customer=<EMAIL> card=<CARD> api_key=<API_KEY> password=<PASSWORD>
```

Three lessons come out of this short experiment:

1. **Rules miss formats they do not know.** Phone numbers, tokens, addresses and names all need their own handling.
2. **Every new rule must be tested on old examples too.** A rule that fixes one line can damage another.
3. **Always read the output before pasting**, even when a script has run. The script is a safety net, not a replacement for looking.

The field-based rule has its own limit: it only works when the value follows `phone=`. A phone number in free text, such as "customer called from +1-555-0134", would slip through. There is no perfect pattern list. That is why the handout's advice for uncertainty is simple: **when unsure, redact it. Over-redacting is safer than leaking.**

### 7. Disclosure and Accountability

**Disclosure** means stating openly that AI helped produce the work. When you hand in AI-assisted work, add a line like this one from the handout:

```text
AI use: test cases drafted with an AI assistant; reviewed and corrected by <your name>.
Corrections: 1 edited (wrong expected result), 1 rejected (invented rule).
```

Notice that the second line comes straight from your correction log in *Human Validation of AI Output*. Disclosure is not a confession; it is useful information. A reviewer who knows the cases were AI-drafted knows to look for the usual AI mistakes, and the correction summary shows that a human really checked them.

**Accountability** means you own what you submit, even if AI wrote the first draft. You saw a company learn this in the Air Canada case in the previous lesson. For a tester, it means you never say "the AI wrote that test" as an excuse. If it is in your pull request, it is your test.

Disclosure works the same way for other kinds of work. A bug report drafted with AI might end: *"Report drafted with an AI assistant from the redacted log; steps reproduced and checked by <your name>."* The important word is **checked**: disclosure only builds trust when the human step is real.

### 8. Licences, Security and Bias

Three more rules of the road deserve a short explanation each.

**Licences.** AI assistants learn from enormous amounts of public code, some of it under licences with conditions. Generated code can occasionally closely resemble existing code. Follow your organisation's guidance on using AI-generated code, and treat large blocks that look suspiciously polished or familiar with care.

**Security.** AI-generated code is not automatically secure. A test helper might disable certificate checks to "fix" a connection error, or log a full request including a password, like the log line in this lesson. Review AI code with the same security eye as any code, including test code.

**Bias.** AI test data can be narrow. Ask an AI for "10 test names" and you will often get mostly common English names. But a real sign-up form must accept names like **O'Brien** (an apostrophe), **Smith-Jones** (a hyphen), **José** (an accent), very short names and very long ones. Data that only contains "John Smith" can hide bugs that affect real users, which is both a quality problem and a fairness problem.

You will study bias and fairness in depth in Week 11; for now, the habit is to ask: **does this data look like our real users?**

### 9. Approved Tools and Where Your Data Goes

"Follow your organisation's AI policy" can sound abstract. In practice, it usually answers three questions:

| Question | Why it matters |
|---|---|
| **Which tools are approved?** | Companies often have agreements with some AI providers that set out how prompts are stored and used, and no agreement with others |
| **Which data may go into which tool?** | A policy might allow internal code in the company's approved assistant but forbid customer data in any AI tool |
| **Which account do I use?** | The same product can behave differently on a personal account and a company account, for example in how long chats are kept |

As a fresher, you do not need to know the details of every provider's terms. You need to know where your company's policy is, and to **ask** when a situation is not covered. "Can I paste this stack trace into the approved assistant?" is a perfectly good question to ask your lead. It shows care, not ignorance.

Two habits help when you are unsure which category a tool falls into:

- **Assume a public chat tool is public.** Paste only what you would be comfortable seeing in a public forum post: redacted, with no company secrets.
- **Never use a personal account for company data**, even if it is quicker. The Samsung guidance asked employees using AI tools on personal devices not to submit company-related information at all.

### 10. Production Data in Test Environments

Testers sometimes work in environments filled with data **copied from production**, because realistic data finds realistic bugs. That convenience has a cost: every customer record in that copy is real personal data, with all the protection rules that apply to it.

Three practices make this safer:

- **Masking:** replacing real values with fake ones of the same shape before the copy reaches testers, so `priya.sharma@gmail.com` becomes `user1042@example.com`.
- **Synthetic data:** generating data instead of copying it, as you did with a seeded generator in *AI-Generated Test Data*.
- **Minimum access:** only the people who need the copied data can see it.

For AI use, the rule is simple: data from a production copy is **production data**. Redact it exactly as you would a live customer record, even though it lives in a test environment. The question from section 3 still decides: would it matter if this value leaked?

### 11. A Quick Check Before Every Prompt

Here is the whole lesson as five questions to ask yourself before you press Enter in an AI tool. They take seconds:

1. **Is this tool approved for this kind of data?**
2. **Have I removed every name, email, number, key, token and password?**
3. **Have I read the text I am about to send, not just run a script on it?**
4. **Does the AI still have what it needs: the error, the fields, the structure?**
5. **If this chat were made public tomorrow, would anyone be harmed?**

If the answer to any of the first three is "no" or "not sure", do not send it yet. Question 5 is the simplest test of all, and the one to remember when nothing else comes to mind.

### 12. Over-Reliance Is a Risk Too

Responsible use also means looking after your own skills. The handout's last key idea: **AI should make you faster, not replace your thinking.**

Every check you have done this week, spotting the invented rule, calculating $45.01, noticing a weak assert, finding the missing AC4 behaviour, needed skills an AI could not supply. Those skills come from practice. If you let AI do all the thinking, you will gradually lose the ability to check it, which is the one thing that makes AI safe to use. A good habit: for each new kind of task, do it yourself once before asking the AI, then compare.

### 13. What If You Pasted Something by Mistake?

It happens, even to careful people. What matters is acting quickly and honestly. The handout's five steps:

1. **Stop.** Do not send more messages in that chat.
2. **Delete the chat** if your tool allows it. This may not remove copies the provider has already stored, so continue with the next steps.
3. **Tell your lead or security contact straight away.** Say what was pasted, which tool you used and when. Hiding it makes things worse.
4. **Rotate secrets.** If a password, API key or token was pasted, it must be changed. Treat it as leaked.
5. **Learn from it.** Add a redaction rule or a pre-flight check so it cannot happen the same way again.

Step 3 is the hardest and the most important. Security teams can only protect what they know about. An early report about a leaked key means one key gets changed; a hidden one can mean an attacker uses it for weeks. Most organisations treat a quick, honest report very differently from a cover-up.

### 14. Common Problems

| Problem | Why it happens | What to do |
|---|---|---|
| You missed a sensitive value | Sensitive data hides in many forms (phone numbers, tokens, addresses) | When unsure, redact it. Over-redacting is safer than leaking |
| Your redacted line is useless to the AI | You removed the field names or the error too | Keep the structure; replace only the **values** |
| A rule list misses a format | Scripts only catch the patterns they know | Always **read** the output before pasting, even when a script has run |
| A new rule breaks other lines | It was only tested on one example | Re-run every old example after adding a rule |
| "It's only test data" | Test values can still reach real systems | Ask: would it matter if this leaked? |

---

## Practice Exercises

1. **Redact by hand (paper, 5 min).** Redact this line: `user=ali.khan@outlook.com phone=+1-555-0134 token=eyJhbGciOiJIUzI1NiJ9.abc123 status=500`. Which values did you replace, and which did you keep? Compare your answer with the final output in section 6.

2. **Bias check (AI tool, 15 min).** Follow this week's four steps:
   - **Prompt:** ask your AI for *"10 test names for a sign-up form."*
   - **Review:** how many are common English names?
   - **Run:** write 5 more names your form must also accept: one with an apostrophe, one hyphenated, one with an accent, one very short and one very long.
   - **Record:** in `prompts.txt`, write one prompt line that would make the AI's list more varied next time.

3. **Explain the regex (AI tool, 10 min).** Ask your AI: *"Explain this regex for a beginner: `[\w.+-]+@[\w-]+\.[\w.]+`"*. Check its explanation against the table in section 5. Then test the pattern yourself on two emails and one non-email.

4. **Write a team policy (paper, 15 min).** Write a 4-line "AI usage policy" for your Project 2 team: which tool or tools, what data must never be pasted, how AI use is disclosed, and who reviews AI output.

5. **Extend the script (code, 20 min).** Write three log lines of your own, with fake values, that contain an IP address, a street address and a customer name in free text. Run them through `redact.py` with the PHONE and TOKEN rules from section 6. Which values survive? Add **one** rule for one of them, then re-run **all** your lines and the original checkout log. Did your rule damage anything?

---

## Knowledge Check

1. What does "redact before you prompt" mean?

<details><summary>Answer</summary>

Replace every sensitive value with a placeholder, such as `<EMAIL>` or `<API_KEY>`, before pasting text into an AI tool, while keeping the structure the AI needs.

</details>

2. Name four groups of sensitive data a tester might handle.

<details><summary>Answer</summary>

Personal data, payment data, secrets (passwords, keys, tokens) and confidential company data (source code, internal URLs).

</details>

3. Why should the redacted line keep the time, the error and the field names?

<details><summary>Answer</summary>

So the AI can still help. The placeholders and field names tell it what kind of value was there and what failed, without revealing the values.

</details>

4. `redact.py` reported the Your Turn line as safe to send, but the phone number and token were still there. What does this show?

<details><summary>Answer</summary>

A pre-flight check is only as good as its rules. "True" means none of its patterns matched, not that the text is safe. Always read the output too.

</details>

5. A new phone rule replaced the log's timestamp. What is this called, and how was it fixed?

<details><summary>Answer</summary>

Over-redaction. It was fixed with a field-based rule that only matches the value after `phone=`, and the fix was checked by re-running the old example.

</details>

6. Why add a disclosure line to AI-assisted work?

<details><summary>Answer</summary>

It is honest, and useful: reviewers know to look for typical AI mistakes, and the correction summary shows a human checked the work.

</details>

7. You accidentally pasted a log containing a live API key. What must happen to the key, and why?

<details><summary>Answer</summary>

It must be rotated (changed), because once pasted it must be treated as leaked. Also stop, delete the chat if possible, and tell your lead or security contact straight away.

</details>

8. Your test environment contains data copied from production. Can you paste a customer's record from it into an AI tool to debug a test?

<details><summary>Answer</summary>

No, not as it is. Data from a production copy is production data, so it must be redacted exactly like a live customer record, and the tool must be approved for that use.

</details>

---

## Glossary

- **Responsible use of AI:** using AI in ways that are safe, legal, fair and honest.
- **Sensitive data:** any value that could harm a person or the company if it leaked.
- **Personal data:** information about an identifiable person, such as a name or email.
- **Secret:** a value that grants access, such as a password, API key or token.
- **Redaction:** replacing sensitive values with placeholders.
- **Placeholder:** a label in angle brackets, such as `<EMAIL>`, that shows what kind of value was removed.
- **Pre-flight check:** an automatic check that refuses to send text to an AI tool if it still contains sensitive data.
- **Lookbehind:** a regex part, such as `(?<=password=)`, that matches text after something without including it.
- **Over-redaction:** removing information that was not sensitive.
- **Disclosure:** stating openly that AI helped produce the work.
- **Accountability:** being responsible for the result, even when AI helped.
- **Rotating a secret:** changing a password, key or token so the old value no longer works.
- **Masking:** replacing real values with fake ones of the same shape before data is copied into a test environment.
- **Synthetic data:** data that is generated rather than copied from real records.
- **OWASP:** the Open Worldwide Application Security Project, a non-profit that publishes widely used lists of security risks.
- **AI usage policy:** an organisation's rules on which AI tools are approved and for which data.

---

## Summary

- **Responsible use** means safe, legal, fair and honest use of AI. For testers, protecting data comes first, because we handle it constantly.
- **Redact before you prompt**: replace values with placeholders and keep the structure. **If in doubt, don't paste.**
- A **redaction script with a pre-flight check** makes the habit reliable, but it **only catches the patterns it knows**. Test new rules on old examples, and read the output before pasting.
- **Disclose** AI help, and stay **accountable** for everything you submit.
- Review AI code for **licence and security** issues, and check AI data for **bias**.
- If you paste something by mistake: **stop, delete, tell, rotate, learn**.

---

## Additional Resources

- OWASP, *Top 10 for Large Language Model Applications*: https://genai.owasp.org/llm-top-10/
- NIST, *AI 600-1: Generative Artificial Intelligence Profile* (2024): https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- Python documentation, *re — Regular expression operations*: https://docs.python.org/3/library/re.html
