# Error Guessing

**Week 3 - Quality Engineering Foundations | Thursday: Test Design Techniques**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define **error guessing** and explain why it is called an experience-based technique.
2. Explain why error guessing works, using ideas such as defect clustering, repeated developer mistakes, and common human error patterns.
3. Name at least eight sources of experience that feed good error guesses (past defects, bug databases, production incidents, user complaints, checklists, and more).
4. Follow a step-by-step process to build an error-guessing checklist (a fault list) and run a timeboxed fault-attack session.
5. Use a categorized catalog of error-guessing ideas for forms and inputs: empty values, spaces, long text, special characters, numbers, dates, files, timing, and network problems.
6. Apply domain-specific checklists for login/registration, search, payment/checkout, file upload, date pickers, and APIs.
7. Compare error guessing with negative testing and exploratory testing and explain how it complements the systematic techniques you learned earlier today (use-case testing, Boundary Value Analysis, Equivalence Partitioning).
8. Describe the strengths and weaknesses of error guessing and ways to make it more systematic.
9. Derive 30+ test ideas for Project 1 (Registration and Login) and use a defect history table to derive new tests through defect-based reasoning.
10. Read and run a short Python demo in which guessed inputs expose failures in a buggy function.
11. Use an AI assistant to brainstorm error-guessing ideas safely, and verify what it says.
12. Describe pair testing and a bug bash as ways to share experience.

---

## Why This Matters

Imagine you are a tester on Project 1, the sample web app with User Registration and Login. Earlier today you learned systematic techniques. Use-case testing walked you through realistic user journeys. Equivalence Partitioning (EP) divided inputs into groups that the system should treat the same way. Boundary Value Analysis (BVA) focused on the edges of those groups, where developers make the most "off by one" mistakes.

These techniques are powerful because they are **repeatable** and **explainable**. But they have a blind spot. They are built from the specification (the written description of how the software should behave). If the requirements say "password must be 8 to 20 characters", EP and BVA will give you excellent tests for the length. They will not, by themselves, tell you to try a password made entirely of spaces, a password pasted from a password manager with a hidden trailing space, a username with an apostrophe in it, or a double-click on the "Register" button that creates two accounts.

Those tests come from somewhere else: from **experience**. An experienced tester has seen these problems before, remembers where the software broke last time, and tries those things first. That is error guessing.

In real teams, many of the most embarrassing production bugs are not boundary errors. They are things like "the app crashes when a name contains an apostrophe" or "the report breaks on February 29". A tester who has seen such a bug once will never forget to try it again. After this lesson, you will be that tester, because you will have a catalog of ideas and a habit of building your own.

Error guessing is also quick and cheap. You do not need a formal model, a large document, or special tools. You need curiosity, a list, and a few minutes. That makes it one of the best return-on-effort techniques you can learn in your first weeks as a quality engineer.

---

## The Concept

### 1. What is error guessing?

**Error guessing** is an **experience-based test design technique** in which the tester **anticipates defects** based on their knowledge, intuition, and past experience, and then **designs tests specifically to expose those defects**.

Let us define the words in that sentence:

- **Test design technique**: a defined way of deciding which tests to create. EP and BVA are test design techniques.
- **Experience-based technique**: a technique that relies on the tester's skills, knowledge, and history rather than on a formal model built from a document. The other well-known experience-based techniques are exploratory testing and checklist-based testing.
- **Defect**: a flaw in the software (in code, configuration, or a document) that can cause it to behave incorrectly. You learned on Wednesday that a human makes an **error** (a mistake), the error puts a **defect** (a fault or bug) into the product, and when that defect is executed the system may show a **failure** (visible wrong behavior).
- **Anticipate**: to predict in advance. You are not waiting for a bug to appear. You are saying "I bet the software mishandles X" and then testing X.

The word "error" in "error guessing" is used loosely. In practice, you are guessing **defects and failures**: "what might be wrong in this software, and what input or action would reveal it?"

> **Important:** Error guessing **complements** systematic techniques. It does **not replace** them. Think of EP, BVA, and use-case testing as your main road map. Error guessing is the local knowledge that tells you "that bridge floods every spring, check it first."

### 2. An analogy: the mechanic and the detective

**The mechanic.** Take your car to an experienced mechanic and say "it makes a strange noise." Before opening the hood, the mechanic listens. "That sounds like the water pump bearing. I have seen it a hundred times on this model." The mechanic does not run every diagnostic in the manual in order. They go straight to the likely fault. If they are wrong, they move to the next likely fault. This is error guessing: experience narrows a huge search space into a short list of likely suspects.

**The detective.** A detective arrives at a new case and recalls past cases: "In the last three burglaries in this area, the thief came through an unlocked back window." The detective checks the back windows first. The detective is not certain. The hunch comes from past cases, and it is cheap to check. When a detective's hunch is based on patterns, it is not magic. It is **pattern recognition**.

A tester's version: "In the last three projects I worked on, the registration form broke when a name had an apostrophe. Let me try O'Brien first."

Notice that the mechanic and the detective still use systematic methods when needed. They combine hunches with procedures. So do good testers.

### 3. Why does error guessing work?

It might sound unscientific, but there are solid reasons it finds real bugs.

**Reason 1: Defects cluster.** On Wednesday you learned the testing principle of **defect clustering**: a small number of modules usually contain most of the defects. If the date-handling module had bugs last release, it likely has more now. Experience tells you where the cluster is. Error guessing lets you aim extra tests at it.

**Reason 2: Developers repeat mistakes.** Developers are human. A developer who forgot to handle empty input in one function often forgets it in the next. Teams copy and paste code, so one bug is often duplicated in several places. A team that never validates the length of text fields will not validate them in any form. So one bug found is evidence that many similar bugs exist.

**Reason 3: Human error patterns are predictable.** People make the same kinds of mistakes everywhere: they forget the "nothing" case, they forget the "too many" case, they assume text contains only letters, they assume dates are in their own country's format, they assume the user clicks once, they assume the network never fails. Psychologists and software engineers have catalogued such patterns for decades. A fault list based on these patterns is a map of where mistakes hide.

**Reason 4: Requirements describe the happy path; bugs live in the gaps.** Specifications rarely say "what should happen if the name is 5,000 characters long". Silent areas of the specification are exactly where developers made their own undocumented decisions, and where bugs hide. Systematic techniques follow the specification. Error guessing explores the silence around it.

**Reason 5: The pesticide paradox.** You learned that running the same tests again and again stops finding new bugs. Error guessing refreshes your test set with new ideas from new experience, which helps you avoid the pesticide paradox.

### 4. Sources of experience

You may be a beginner, but you are not empty-handed. Experience can be borrowed from many places. Here are the main sources.

| Source | What it is | Example of a guess it produces |
|---|---|---|
| **Past defects** | Bugs found earlier in this product or similar ones | "Last release, the email field accepted spaces. Try spaces in the new phone field." |
| **Defect logs / bug databases** | The team's recorded history of defects, such as tickets in Jira | "Search the bug tracker for 'login': 12 of 15 login bugs involve session timeout." |
| **Known failure patterns** | Widely recognized ways that software fails | "Off-by-one errors, null handling, race conditions." |
| **Developer knowledge** | What the programmers know about risky or messy code | A developer says "the date logic was rushed; I am not sure about time zones." |
| **Domain knowledge** | Understanding of the business area, such as banking or healthcare | "Currency must round to two decimals; refunds must never exceed the original payment." |
| **Production incidents** | Failures that happened with real users in live systems | "Last month, a customer in another time zone saw yesterday's date." |
| **User complaints** | Support tickets, reviews, and feedback | "Several users say the password reset email never arrives." |
| **Common error lists and checklists** | Published or internal lists of typical faults | "A checklist for form fields: empty, long, special characters, and so on." |
| **Your own earlier testing** | Notes and memory from earlier sessions | "I remember the back button re-submitted the form." |
| **Colleagues and community** | Other testers' stories, blogs, and conferences | "A tester on a forum described a bug with emoji in names." |

If you are new and have no personal history, start with the last four rows. Read the bug list, talk to the developers, read the support tickets, and borrow checklists. Within a few weeks you will have your own stories.

### 5. How to do error guessing, step by step

Error guessing can be done informally (just "try some things") but it works far better with a light structure. Here is a simple, repeatable process.

**Step 1: Understand what you are testing.**
Read the requirement or user story. Identify the inputs, outputs, and the actions a user can take. Note which parts are new, which are complex, and which were changed recently (recent changes are a common source of defects).

**Step 2: Gather sources of experience.**
Look at your sources: search the defect tracker, ask developers where they feel uneasy, check support tickets, and open the team's checklist. Write down anything that sounds relevant.

**Step 3: Build a defect taxonomy or fault list.**
A **defect taxonomy** is a classification of defects into categories, for example "input handling", "date and time", "calculations", "state and ordering", "environment and network", "security-related input handling". A **fault list** (also called an **error-guessing checklist**) is a list of specific faults you suspect, grouped under those categories. Each item is something short like "empty string in required field" or "double click on submit".

You can start from the catalog later in this lesson and add items from your own sources.

**Step 4: Choose the "attack" (fault attack).**
A **fault attack** (the term comes from the testing literature, and "attack" here means a deliberate, targeted attempt to provoke a failure, not hacking) is an approach in which you take each item on the fault list and design a test that attacks it. The aim is to cause the failure if the fault exists. You are not trying to confirm that things work; you are trying to break them in a specific, targeted way. In effect, you work from the list of suspected faults towards the tests, rather than from requirements.

**Step 5: Timebox the session.**
A **timebox** is a fixed, limited amount of time (for example, 45 minutes) that you set before you start and stop at when it ends. Timeboxing matters because error guessing has no natural finish line. Without a limit, you could keep guessing forever. A timebox keeps the session focused, makes the effort estimate easy, and makes you prioritize the most likely faults first.

A common pattern is: 5 minutes to pick faults from the list, 35 minutes to test, 5 minutes to write up.

**Step 6: Execute and observe carefully.**
Run each test. Observe not only the obvious message on screen but also the side effects: was a record created? Was an error logged? Was a confusing technical message shown? Did the page slow down? Often the bug is not the screen message but the damage behind it, for example a half-created account.

**Step 7: Document tests and results.**
Write down what you tried, with the exact input, the expected result, the actual result, and the verdict (pass or fail). Report any defect through your defect tracker (Jira) following the defect lifecycle you learned on Tuesday. Documenting turns your private hunches into **shared, reusable knowledge**, which also addresses the biggest weakness of this technique (it is hard to repeat).

**Step 8: Update the checklist.**
If you found a new type of defect, add it to the fault list. If some items never find anything, mark them as lower priority. The checklist is a living document. This is how your team's experience grows.

```
Sources of experience
        |
        v
  Fault list / checklist  <----------------+
        |                                  |
        v                                  |
  Fault attack (design tests)              |
        |                                  |
        v                                  |
  Timeboxed session (execute)              |
        |                                  |
        v                                  |
  Document tests and results --------------+
  (new defects enrich the list)
```

### 6. A catalog of error-guessing ideas for forms and inputs

This is the heart of the lesson. Keep it nearby while you test. The catalog is grouped into categories. For each idea you will see what to try and what a **sensible system** should do. Always compare against the specification and your team's decisions. If the specification is silent, ask the product owner or analyst what the expected behavior should be instead of assuming.

> **Safety note for the security-flavored items.** A few ideas below involve text that looks like code (HTML or database keywords). The testing purpose here is conceptual: to confirm that the application treats such text as **plain data**, stores or rejects it safely, and never interprets it as instructions. This lesson does not teach anyone how to attack a system. Only run these tests on systems you are authorized to test, such as the course practice app, and follow your organization's rules. The OWASP guide in the resources section explains the topic conceptually.

#### 6.1 Empty, null, blank, and whitespace

| Idea | What to try | Typical fault it exposes |
|---|---|---|
| Empty | Leave a required field empty and submit | Required check missing or only on the browser side |
| Null (no value at all) | In an API, omit the field or send `null` | Crash with a null reference error |
| Blank | Field with nothing but cleared characters | Same as empty, but check both |
| Whitespace only | Enter only spaces, tabs | Treated as valid because "it is not empty" |
| Leading spaces | `"   ada"` | Saved with spaces; later login or search fails |
| Trailing spaces | `"ada   "` (also a copy-paste accident) | Username with trailing space does not match at login |
| Internal multiple spaces | `"Ada     Lovelace"` | Not collapsed; shown oddly |
| Line break in a single-line field | Paste text with a newline | Breaks layout, exports, or CSV files |

#### 6.2 Length

| Idea | What to try | Typical fault |
|---|---|---|
| Very long input | 5,000 or 100,000 characters in a text field | Crash, slow response, database error, cut-off without warning |
| Exactly at the limit, and one over | If the maximum is 50, try 50 and 51 | Off-by-one (this overlaps with BVA, on purpose) |
| One character | `"a"` | Fails a hidden minimum rule or crashes a parser |
| Long word without spaces | `"WWWWWWWW..."` | Layout overflow, text escapes its box |

#### 6.3 Special characters, Unicode, and emoji

| Idea | What to try | Typical fault |
|---|---|---|
| Punctuation and symbols | `! @ # $ % ^ & * ( ) _ + - = { } [ ] \| \ : ; " ' < > , . ? /` | Rejected without explanation, or breaks processing |
| Accented letters | `"Zoe"` with accents, `"Jose"` with accent, `"Muller"` with umlaut | Letters replaced by question marks or garbage ("mojibake") |
| Non-Latin scripts | Chinese, Arabic (right-to-left), Hindi, Cyrillic | Rejected or displayed incorrectly |
| Emoji | A smiley or flag emoji in a name or comment | Database error or truncation (some systems count one emoji as several characters) |
| Zero-width or invisible characters | Characters that are not visible on screen | Two usernames look identical but are different |
| Control characters | Tab, null byte (conceptually) | Parsing failures |

**Unicode** is the international standard that gives a number to every character in every writing system, including emoji. Software that does not handle it correctly breaks on names and text from around the world.

#### 6.4 Quotes and apostrophes

The apostrophe in names such as **O'Brien**, **D'Angelo**, or **N'Golo** is a classic. Single quotes, double quotes, backticks, and backslashes all play special roles in programming languages and databases. Code that builds text by gluing strings together can break or behave strangely when these characters appear. Test names with apostrophes, hyphens (Mary-Jane), and quotes in every text field, and check they are stored and displayed exactly as typed.

#### 6.5 Code-like text treated as data (conceptual)

| Idea | What to try | What a healthy system does |
|---|---|---|
| HTML or script-like text | Enter something that looks like a tag, such as an angle-bracketed word, into a comment or name field | Shows it as literal text (or rejects it), never as part of the page layout or active content |
| SQL-keyword-like text | Enter words such as `SELECT`, `DROP`, or `--` as a name | Stores it as ordinary text; no error, no change in behavior |
| Template-like text | Enter text with curly braces, such as `{{name}}` or `%s` | Displayed literally |
| Path-like text | `../` or backslashes in a name or file name | Treated as text, never as a location |

The testing question is always the same: **does the application treat what the user types as data, and never as instructions?** If something odd happens (the page layout changes, a database error appears, a stack trace is shown), report it immediately as a potentially serious defect and follow your company's security reporting process. Do not try to push further to "see how bad it is" without authorization.

#### 6.6 Numbers

| Idea | What to try | Typical fault |
|---|---|---|
| Negative numbers | `-1`, `-100` in quantity, age, amount | Negative quantity creates a credit or refund |
| Zero | `0` as quantity or price | Division by zero, free item, "required" check wrongly triggered |
| Decimal numbers | `1.5` in a whole-number field | Rounded silently or crash |
| Decimal separators | `1,5` and `1.5`, thousands separators like `1,000.50` or `1.000,50` | Different locales read the same text as different numbers |
| Large numbers | `99999999999`, `2147483648` | Overflow (value too large for the storage type, sometimes wrapping to a negative number) |
| Leading zeros | `007` | Treated as octal, or zeros lost (matters for zip codes and IDs) |
| Scientific notation | `1e5` | Accepted when it should not be |
| Letters in a number field | `12abc`, `NaN`, `Infinity` | Accepted or crash |
| Plus sign, minus sign alone | `+`, `-` | Parsing error |

#### 6.7 Copy, paste, and case

| Idea | What to try | Typical fault |
|---|---|---|
| Copy-paste | Paste text copied from Word, a PDF, or a web page | Hidden characters, smart quotes, or trailing spaces come along |
| Paste into a field that blocks paste | Confirm behavior is deliberate | Annoying for password managers (see accessibility) |
| Case sensitivity | `ADA@Mail.com` versus `ada@mail.com` | Duplicate accounts; login fails with different case |
| Mixed case in passwords | Confirm passwords are case-sensitive | Password accepted regardless of case |
| Turkish "I" and similar | Letters with locale-specific case rules | Case conversion changes the wrong letters |

#### 6.8 Actions, timing, and state

| Idea | What to try | Typical fault |
|---|---|---|
| Double submit | Double-click the submit button, or press Enter twice | Duplicate records, double charge |
| Back button | Submit, then press Back, then submit again | Re-submission, stale data |
| Refresh | Refresh after submitting | "Resubmit form?" duplicates the action |
| Session expiry | Wait until the session times out, then submit | Lost data, cryptic error, or worse, the action works without login |
| Multi-tab | Same user in two tabs, change in one, act in the other | Stale state, conflicting updates |
| Concurrency | Two users at the same time doing the same action | Race condition (outcome depends on timing), lost updates |
| Repeated actions | Do the same action 20 times | Memory leak, limit not enforced |
| State/ordering mistakes | Do steps in the wrong order: pay before adding items; log out then go Back | Pages visible after logout; steps skipped |
| Cancel midway | Start a process then cancel or close the browser | Half-created records |

**Race condition**: a defect where the result depends on which of two operations happens first, and the system was only designed for one order.

#### 6.9 Dates and times

| Idea | What to try | Typical fault |
|---|---|---|
| Leap years | 29 Feb in a leap year (for example 2028) and 29 Feb in a non-leap year (for example 2027) | Invalid date accepted, or valid date rejected |
| Century rule | 29 Feb 2100 (not a leap year) and 29 Feb 2000 (a leap year) | Simplified leap-year code gets these wrong |
| Month ends | 31 Jan, 30 Apr, 31 Apr (invalid), 28/29 Feb | Wrong number of days, "add one month" errors |
| Year boundaries | 31 Dec to 1 Jan | Wrong year in reports |
| Time zones | User in one zone, server in another | Dates shift by one day |
| Daylight saving time (DST) | The hour when clocks move forward or back | Missing or duplicated hour; timers wrong |
| Midnight and noon | 00:00, 12:00, 24:00 | AM/PM confusion |
| Date formats | 03/04/2026 (is it 3 April or 4 March?) | Day and month swapped |
| Far past and future | Year 1900, year 9999, today | Rejected or crash; unrealistic ages accepted |
| Time passing | Link or token that expires | Expired link still works, or valid link expires too early |

#### 6.10 Files and uploads

| Idea | What to try | Typical fault |
|---|---|---|
| Empty file | A file with 0 bytes | Crash or "success" with nothing |
| Huge file | A file bigger than the limit | Timeout, server error, hangs |
| Wrong type | A text file renamed with an image extension | Accepted because only the name was checked |
| Double extension | `report.pdf.exe` or `photo.jpg.txt` | Wrong type detected |
| No extension | A file named `report` | Rejected or mishandled |
| Special characters in name | Spaces, accents, very long names | Cannot be downloaded again |
| Same name twice | Upload the same file name again | Silently overwritten |
| Corrupt file | A damaged image | Server error when generating a preview |
| Cancel upload midway | Stop in the middle | Partial file left behind |

#### 6.11 Calculations and money

| Idea | What to try | Typical fault |
|---|---|---|
| Division by zero | Average of zero items, cost per unit with quantity zero | Crash or "Infinity" shown |
| Currency rounding | 0.1 + 0.2 and totals like 19.995 | Floating-point error; a cent lost or gained |
| Rounding rule | Rounding each line versus rounding the total | Different totals |
| Tax and discount order | Apply discount before and after tax | Wrong total |
| Currency formats | Symbols, codes, number of decimal places (some currencies have none) | Wrong display |
| Very small or very large amounts | 0.01 and 999,999,999.99 | Overflow or rejected |

#### 6.12 Locale and format differences

**Locale** means the language and regional settings of a user, which control date format, number format, currency, and text direction.

| Idea | What to try | Typical fault |
|---|---|---|
| Different regional settings | Switch the browser or operating system region | Dates and numbers misread |
| Right-to-left text | Arabic or Hebrew text | Layout broken |
| Long translations | Switch to a language with longer words | Text overflows buttons |
| Phone and address formats | International numbers with plus sign and spaces | Rejected valid numbers |
| Name formats | One name only, several surnames, no spaces | "Last name required" blocks real people |

#### 6.13 Network, environment, and permissions

| Idea | What to try | Typical fault |
|---|---|---|
| Network loss | Turn off Wi-Fi or throttle the connection while submitting | Spinner forever, or data lost silently |
| Slow network | Use a slow connection profile | Timeouts, double submit because "nothing happened" |
| Server error | Simulate or find a way to get a 500 error | Raw technical error shown to user |
| Permission errors | Try an action without permission (user opens admin page URL) | Page accessible when it should not be |
| Read-only or full disk | Where applicable (file saving) | Crash with no message |
| Different browsers and devices | Small screen, older browser | Layout or function broken (also covered by other testing) |
| Cookies or JavaScript disabled | Turn them off | Blank page or silent failure |

You will not use all of these in every session. Choose the categories that match the feature in front of you. A date picker needs the dates category. A file upload needs the files category. A login form needs empty, whitespace, case, session, and state ideas.

### 7. Domain-specific checklists

Below are short checklists you can copy and extend. Each item is a guess about a likely fault.

#### 7.1 Login and registration

- Empty username, empty password, both empty
- Whitespace-only username or password
- Trailing or leading spaces in email or username
- Email in different case, and the same email twice with different case
- Email with unusual but valid characters (plus sign, dots, long domain)
- Password with spaces, emoji, and very long length
- Password and "confirm password" differ by one character or by a trailing space
- Error messages that reveal too much ("this email exists" versus a general message), as a design question to raise
- Many failed logins in a row: is there lockout or delay?
- Double-click on Register or Login
- Back button after login and after logout
- Session expiry in the middle of filling a form
- Login from two browsers, or two tabs
- Password reset: link used twice, link expired, link for a different account
- "Remember me" after logout
- Copy-pasted credentials with hidden spaces
- Registration with a username that is only digits, or looks like another user's (visually similar characters)
- Terms checkbox unchecked, but form submitted by pressing Enter

#### 7.2 Search

- Empty search; search with only spaces
- Very long search text
- Special characters, quotes, and wildcard-like characters (`*`, `%`, `?`)
- Case differences
- Accents ("cafe" versus the accented spelling)
- One result, zero results, and thousands of results (paging)
- Searching the same text twice quickly
- Pagination: first page, last page, a page number beyond the last
- Sorting with equal values; sorting with empty values
- Back button preserves search? Refresh keeps filters?
- Text that looks like code or markup is shown literally

#### 7.3 Payment and checkout

- Quantity zero, negative, decimal, very large
- Price or total with many decimals
- Discount code: empty, expired, used twice, mixed case, with spaces
- Double-click on "Pay"; pay then press Back
- Network loss during payment: is the customer charged without an order?
- Session expires with a full basket
- Different currencies and rounding
- Card number with spaces and dashes, too short, too long, expired date, past date, far future date
- Changing the basket in another tab during checkout
- Order of steps: pay without an address, skip a step through the URL
- Refund greater than the amount paid

#### 7.4 File upload

- Empty file, huge file, exactly at the size limit and one byte over
- Wrong type, double extension, no extension, uppercase extension (`.JPG`)
- File name with spaces, accents, very long name, path-like text
- Same file twice; two files with the same name
- Multiple files at once, more than the allowed number
- Cancel during upload; lose network during upload
- Corrupt file
- Upload then delete then upload again

#### 7.5 Date pickers

- Leap day, invalid day such as 31 April (typed manually if allowed)
- First and last day of month and year
- Past dates where only future dates are allowed, and the reverse
- Today at midnight; time zones; daylight saving change
- Date typed in a different format
- Start date after end date
- Same start and end date
- Clearing the date after selecting one
- Keyboard-only use

#### 7.6 APIs (at name level)

An **API** (Application Programming Interface) is a way for programs to talk to each other, often by sending requests over the web and receiving structured responses. Error-guessing ideas, at the level of names:

- Missing required field; field set to `null`; wrong data type (text where a number is expected)
- Extra unexpected fields
- Empty request body; malformed request body
- Very large request body
- Wrong request method (using a "get" where a "post" is expected)
- Missing, invalid, or expired authentication token
- Request repeated twice (idempotency, which means repeating a request should not repeat its effect when it should not)
- Requests in the wrong order
- Unusual status codes returned and how the client reacts (404, 500, timeouts)
- Different character encodings and very long values

### 8. Error guessing versus negative testing versus exploratory testing

Beginners often mix these up. Here is how they relate.

**Negative testing** (Wednesday) is testing with **invalid or unexpected conditions** to confirm the software rejects them gracefully. It describes the **kind of test** (invalid input, unexpected action). Many error-guessing tests are negative tests: empty, too long, wrong type. But some are not: the "double submit" test uses a valid input, and the "leap day" test might use a perfectly valid date that happens to be hard.

**Error guessing** describes **how you chose the test**: by anticipating faults from experience. A negative test can be chosen systematically (for example, an invalid partition from EP) or by guessing. A guessed test can be positive or negative.

**Exploratory testing** (covered in depth on Friday; here is only a pointer) is a style of testing in which learning, test design, and execution happen at the same time, guided by the tester's observations. Error guessing is often one of the **ideas used inside** an exploratory session ("let me try a very long name here"), but exploratory testing is a broader approach with its own structure, such as charters and session notes.

| | Error guessing | Negative testing | Exploratory testing |
|---|---|---|---|
| What is it? | A way to **choose** tests from anticipated faults | A **type** of test using invalid or unexpected conditions | A **style** of testing: learn, design, and execute together |
| Based on | Experience, past defects, checklists | Requirements and invalid partitions, plus ideas | Tester's live discovery |
| Overlap | Many guessed tests are negative | Many negative tests are guessed | Often uses guessing as one tool |
| Covered | Today | Wednesday | Friday |

### 9. Strengths and weaknesses

**Strengths**

- **Fast.** You can start with no preparation.
- **Finds unusual defects.** It targets defects that systematic techniques miss, particularly in the silent areas of the specification.
- **Cheap.** No special tools or models.
- **No formal specification needed.** Useful when requirements are poor, late, or missing.
- **Uses accumulated team knowledge.** Turns past pain into future prevention.
- **Flexible.** Fits into any time gap, from five minutes to a full session.

**Weaknesses**

- **Depends on the tester's skill and experience.** A beginner with a weak list will find fewer bugs than an expert.
- **Not easily repeatable.** Two testers will guess differently, and the same tester may forget what they did.
- **No measure of coverage.** You cannot say "we covered 85 percent of the requirements" through guessing alone.
- **Bias.** You guess what you already know, so you may miss new kinds of faults. (This connects to the cognitive biases from Wednesday: confirmation bias and the "I have seen this before" trap.)
- **Hard to estimate and plan.** It is difficult to know how long guessing will take or how many defects it will find.
- **Can be wasteful.** Without limits, testers can spend hours on unlikely scenarios.

### 10. Making error guessing more systematic

The weaknesses are real, but they can be reduced.

1. **Use checklists.** A written checklist makes the technique repeatable, shareable, and reviewable. Different testers can run the same list. The catalog in this lesson is a starting point.
2. **Use fault attacks.** Work through a fault list one item at a time, as described earlier.
3. **Use defect-based testing.** In **defect-based testing**, tests are designed from a taxonomy of defect types, or from the history of defects found in the past. You will do this in the worked example later.
4. **Use past bug reports.** Mine the bug tracker systematically: group bugs by module and cause, then design tests for the top groups.
5. **Timebox sessions** and take notes.
6. **Pair up.** Two minds guess more than one (see pair testing below).
7. **Measure effectiveness.** One practical measure is the **number of defects found** (and their severity) per hour of error-guessing. If the technique found 8 defects in 2 hours, and a systematic suite found 3 in 2 hours, you have evidence of its value. Another approach is to measure how many guessed-fault checklist items led to real defects, and keep refining the list so that high-yield items rise to the top. Remember that defects found is a measure of **effectiveness**, not coverage.
8. **Feed the loop.** Every defect found by guessing is added back to the checklist.

---

## Examples

### Example 1: Building an error-guessing checklist for Project 1 (Registration and Login)

**Context.** Project 1 has a registration page and a login page. Registration collects: first name, last name, email, password, confirm password, and date of birth, plus a terms checkbox. Login takes email and password. Assume the specification says: email must be a valid format and unique; password 8 to 20 characters with at least one letter and one digit; names up to 50 characters.

**Step 1: Gather sources.** We have no bug database for this new app, so we use a general checklist (the catalog above), developer conversation ("I used a regular expression for the email"), and domain knowledge about accounts (emails are case-insensitive, people have apostrophes in names).

**Step 2: Build the fault list (grouped by taxonomy category).**

- Input handling (empty, whitespace, long text, special characters)
- Identity and uniqueness (case, duplicates, look-alike values)
- State and timing (double submit, session, back/refresh)
- Dates (date of birth)
- Security-related input handling (code-like text treated as data)
- Environment (network failure)

**Step 3: Derive test ideas.** The table below lists 36 test ideas. For each we state the guessed fault, the test input, and the expected result. (Expected results reflect the assumed specification; always confirm against your real requirements.)

| # | Area | Guessed fault | Test input / action | Expected result |
|---|---|---|---|---|
| 1 | Registration - first name | Required check missing | Leave first name empty, fill all else, submit | Clear message "First name is required"; no account created |
| 2 | Registration - first name | Whitespace counts as a value | First name = five spaces | Rejected as required/invalid; no account created |
| 3 | Registration - first name | Apostrophe breaks saving | First name = `Sean`, last name = `O'Brien` | Account created; name shown as `O'Brien` everywhere |
| 4 | Registration - last name | Hyphen or double name rejected | Last name = `Smith-Jones` | Accepted and displayed exactly |
| 5 | Registration - first name | Non-Latin or accented letters corrupted | First name = accented name (for example, Jose with accent) or a name in another script | Accepted and displayed correctly, with no question marks or garbage |
| 6 | Registration - first name | Emoji crashes database | First name = a smiley emoji | Either rejected with a clear message or stored and shown correctly; no server error |
| 7 | Registration - last name | Over-length not handled | Last name = 5,000 characters | Rejected with a length message (or trimmed with a warning); no crash or slow response |
| 8 | Registration - last name | Off-by-one at limit | Last name = 50 characters, then 51 | 50 accepted; 51 rejected |
| 9 | Registration - first name | Leading and trailing spaces saved | First name = `  Ada  ` | Spaces trimmed, or rejected; shown as `Ada` |
| 10 | Registration - name | Code-like text interpreted | First name = text that looks like an HTML tag | Treated as plain text (shown literally or rejected); page layout unchanged |
| 11 | Registration - name | Database keywords interpreted | Last name = `DROP TABLE users; --` as plain words | Stored or rejected as plain text; no error, application continues to work |
| 12 | Registration - email | Case-sensitive duplicate check | Register `Ada@Mail.com`, then register `ada@mail.com` | Second registration rejected as duplicate |
| 13 | Registration - email | Trailing space saved | Email = `ada@mail.com ` (trailing space) | Space trimmed or rejected; login works later |
| 14 | Registration - email | Valid special format rejected | Email = `ada+test@mail.com` | Accepted (plus addressing is valid) |
| 15 | Registration - email | Missing at-sign or domain accepted | Emails `ada.mail.com`, `ada@`, `@mail.com`, `ada@@mail.com` | All rejected with an email format message |
| 16 | Registration - email | Very long email | 300-character email | Rejected with a length message; no crash |
| 17 | Registration - email | Two spaces or newline pasted | Paste an email copied from a document with a hidden line break | Rejected or cleaned; no broken record |
| 18 | Registration - password | Whitespace-only password | Password = eight spaces | Rejected (fails letter and digit rule) |
| 19 | Registration - password | Spaces in the middle handled badly | Password = `Pass word1` | Behavior matches specification (accepted or clearly rejected); login with the same text works if accepted |
| 20 | Registration - password | Length limit off-by-one | Passwords of 7, 8, 20, and 21 characters (with letter and digit) | 7 and 21 rejected; 8 and 20 accepted |
| 21 | Registration - password | Very long password crashes hashing | Password = 10,000 characters | Rejected with a message or handled; no crash |
| 22 | Registration - password | Emoji in password | Password = `Passw0rd` plus an emoji | Accepted and login works, or clearly rejected |
| 23 | Registration - confirm password | Confirm check ignores case or trailing space | Password `Passw0rd1`; confirm `passw0rd1`, then `Passw0rd1 ` | Both rejected as "passwords do not match" |
| 24 | Registration - date of birth | Leap day mishandled | DOB = 29 Feb 2000 (valid), 29 Feb 2001 (invalid) | First accepted; second rejected |
| 25 | Registration - date of birth | Future or impossible date accepted | DOB = tomorrow; DOB = 31 Apr 1990; DOB = year 1800 | All rejected with a clear message |
| 26 | Registration - date of birth | Date format confusion | DOB typed as `03/04/2000` | Interpreted according to the displayed format; shown back consistently |
| 27 | Registration - submit | Double submit creates two accounts | Fill a valid form, double-click Register | Exactly one account; one confirmation |
| 28 | Registration - submit | Refresh resubmits | Register, then refresh the confirmation page and accept the resubmission prompt | No second account; clear message about duplicate |
| 29 | Registration - terms | Checkbox bypassed | Leave terms unchecked, press Enter in a text field | Not submitted; message to accept terms |
| 30 | Registration - network | Half-created account | Submit, then lose the network connection | Clear error; either a complete account or none; no duplicate on retry |
| 31 | Login - fields | Empty fields | Submit with both empty; with only one empty | Field-specific messages; no server error |
| 32 | Login - email | Case sensitivity in login | Log in with `ADA@MAIL.COM` | Login succeeds (if emails are case-insensitive per specification) |
| 33 | Login - password | Password case ignored | Log in with `passw0rd1` for account `Passw0rd1` | Login fails with a general message |
| 34 | Login - password | Pasted trailing space | Paste correct password with one trailing space | Behavior is deliberate: either fails with a clear general message or is trimmed (as specified) |
| 35 | Login - repeated attempts | No lockout or delay | 10 wrong passwords in a row | Lockout, delay, or captcha as specified; message does not reveal which field was wrong |
| 36 | Login - session | Back button after logout | Log in, log out, press Back | Protected page not shown; login required |
| 37 | Login - session | Expired session accepted | Log in, wait past the timeout, perform an action | Redirect to login; no action performed |
| 38 | Login - multi-tab | Conflicting sessions | Log in in two tabs; log out in one; act in the other | Second tab handled gracefully; login required |
| 39 | Login - double submit | Two sessions created | Double-click Login | One login; no error |
| 40 | Login - message | Error message leaks information | Wrong email versus wrong password | Same general message ("email or password is incorrect") |

That is 40 test ideas from one short checklist and about an hour of thinking. Notice how many involve experience: the apostrophe, the trailing space, the double-click, and the Back button. None of them would have come from EP or BVA alone, although a few (rows 8 and 20) deliberately overlap with BVA to double-check the edges.

**Step 4: Prioritize.** With a 45-minute timebox, you would pick the tests most likely to find high-impact defects: duplicate account creation (12, 27), data loss (30), session issues (36, 37), and name handling (3, 5, 6, 7). Mark the rest as "if time permits".

### Example 2: Defect-based reasoning with a defect history

Suppose Project 1's team keeps a defect history. Here are 10 past bugs, from this app's earlier versions and its sister project. We will derive new tests from them.

| ID | Module | Defect summary | Root cause (as found) | Severity |
|---|---|---|---|---|
| D-101 | Registration | Account created with email containing trailing space | Input not trimmed | Medium |
| D-102 | Registration | Crash when last name has an apostrophe | Text joined into a database command by gluing strings | High |
| D-103 | Login | Login failed for users who typed email in capital letters | Case-sensitive comparison | High |
| D-104 | Registration | Two accounts created on double click | No duplicate-submit protection | High |
| D-105 | Profile | Date of birth 29 Feb saved as 1 Mar | Date arithmetic mistake | Medium |
| D-106 | Login | Protected page still visible after logout and Back | Page cached; no server-side check | High |
| D-107 | Profile | Upload of a 0-byte avatar caused a server error | Empty file not handled | Medium |
| D-108 | Registration | 300-character name truncated silently in database | No length validation | Low |
| D-109 | Password reset | Reset link worked twice | Token not invalidated after use | High |
| D-110 | Search (admin) | Search for `%` returned every record | Special character treated as wildcard | Low |

**Defect-based reasoning** asks three questions about each bug:

1. **Where else could the same cause exist?** (similar places in the code)
2. **What nearby variants of this fault might exist?** (neighbors of the fault)
3. **Was the fix itself complete?** (regression of the fix; here we only point out that rerunning tests after a fix belongs to regression testing, covered Friday)

| Past defect | Where else? / New variant | New test ideas |
|---|---|---|
| D-101 trailing space in email | Trailing spaces in first name, last name, password, search box, discount code; leading spaces; spaces inside | Add trailing, leading, and internal spaces to every text field, and check login after registering with such values |
| D-102 apostrophe crash | Other names with quotes, backslashes, hyphens; every field that stores text, including profile and comments | O'Brien in each text field; double quote; backslash; a name made only of punctuation |
| D-103 case in login | Case in registration duplicate check, in password reset, in "forgot email" lookup, in username search | Register `A@x.com` then `a@x.com`; reset password using a different case; log in with mixed case |
| D-104 double click duplicates | Double click on Login, Reset, Upload, Pay; pressing Enter twice; slow network making the user click again | Double-click or rapid Enter on every submit action; throttle the network and click twice |
| D-105 29 Feb | Other date fields; 31 Apr; 28 Feb; year 2100; time zones for dates | Dates of 29 Feb in leap and non-leap years; 29 Feb 2100; time zone change on the date |
| D-106 Back after logout | Back after password change; Back after account deletion; protected URL typed directly; second tab after logout | Open a protected URL after logout; use Back after each sensitive action; check the second tab |
| D-107 empty avatar | Wrong type, huge file, double extension, corrupt image | 0 bytes, huge, `.png` that is really text, `.jpg.exe`, damaged image, upload cancelled |
| D-108 long name | Other fields without limits (email, address, comments, search) | 5,000 characters in every text field; check truncation warning |
| D-109 reset link twice | Other one-time links: email verification, invitation; expired link; link for the wrong user | Use each one-time link twice; use after expiry; use after a newer link was issued |
| D-110 `%` search | Other wildcard-like characters (`_`, `*`, `?`); quotes; empty search; very long search | Search for `_`, `*`, `?`, quotes; compare results with literal text |

This is how a defect history turns into a living test library. Two other useful moves: **count by module** (here Registration has four bugs: that is a hint of defect clustering, so give Registration extra attention), and **count by cause** (input not handled correctly shows up at least five times: so error-guessing in every input field is well justified).

### Example 3: A Python demo - a buggy function and guessed inputs

Now we move to code. This small demo shows what error guessing looks like at the level of a function. We write a function `parse_full_name` that splits a full name into a first name and last name. The first version is a typical beginner version that works for the happy path. Then we guess faults, write tests for them, watch them fail, and fix the function.

Save the following file as `name_demo.py` and run it with `python name_demo.py`. It uses only the Python standard library, so no installation is needed.

```python
"""Error guessing demo: a buggy name parser, guessed-input tests, and a fix."""

MAX_NAME_LENGTH = 100


def parse_full_name_buggy(full_name):
    """First version: works for 'Ada Lovelace' and little else."""
    parts = full_name.split(" ")
    first = parts[0]
    last = parts[-1]
    return {"first": first.capitalize(), "last": last.capitalize()}


def parse_full_name_fixed(full_name):
    """Second version: written after the guessed failures were found."""
    if not isinstance(full_name, str):
        raise ValueError("name must be text")
    cleaned = " ".join(full_name.split())
    if cleaned == "":
        raise ValueError("name must not be empty")
    if len(cleaned) > MAX_NAME_LENGTH:
        raise ValueError("name is too long")
    parts = cleaned.split(" ")
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""
    return {"first": first, "last": last}


# Each case: (guessed fault, input, expected outcome)
# expected is a dict, or the text "error" meaning a clear ValueError is expected.
CASES = [
    ("normal name", "Ada Lovelace", {"first": "Ada", "last": "Lovelace"}),
    ("None input", None, "error"),
    ("empty string", "", "error"),
    ("whitespace only", "     ", "error"),
    ("extra spaces", "  Ada   Lovelace  ", {"first": "Ada", "last": "Lovelace"}),
    ("apostrophe", "Sean O'Brien", {"first": "Sean", "last": "O'Brien"}),
    ("single name", "Prince", {"first": "Prince", "last": ""}),
    ("very long", "A" * 5000 + " Smith", "error"),
]


def run(func):
    passed = 0
    for label, value, expected in CASES:
        shown = repr(value) if len(repr(value)) < 30 else repr(value)[:27] + "..."
        try:
            actual = func(value)
            outcome = actual
        except ValueError as exc:
            outcome = "error"
        except Exception as exc:
            outcome = "CRASH " + type(exc).__name__
        ok = outcome == expected
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:<16} input={shown:<32} got={str(outcome)[:45]}")
    print(f"  Result: {passed}/{len(CASES)} passed\n")


if __name__ == "__main__":
    print("Testing parse_full_name_buggy")
    run(parse_full_name_buggy)
    print("Testing parse_full_name_fixed")
    run(parse_full_name_fixed)
```

**Expected output** (this is the real output from running the file):

```
Testing parse_full_name_buggy
  [PASS] normal name      input='Ada Lovelace'                   got={'first': 'Ada', 'last': 'Lovelace'}
  [FAIL] None input       input=None                             got=CRASH AttributeError
  [FAIL] empty string     input=''                               got={'first': '', 'last': ''}
  [FAIL] whitespace only  input='     '                          got={'first': '', 'last': ''}
  [FAIL] extra spaces     input='  Ada   Lovelace  '             got={'first': '', 'last': ''}
  [FAIL] apostrophe       input="Sean O'Brien"                   got={'first': 'Sean', 'last': "O'brien"}
  [FAIL] single name      input='Prince'                         got={'first': 'Prince', 'last': 'Prince'}
  [FAIL] very long        input='AAAAAAAAAAAAAAAAAAAAAAAAAA...   got={'first': 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  Result: 1/8 passed

Testing parse_full_name_fixed
  [PASS] normal name      input='Ada Lovelace'                   got={'first': 'Ada', 'last': 'Lovelace'}
  [PASS] None input       input=None                             got=error
  [PASS] empty string     input=''                               got=error
  [PASS] whitespace only  input='     '                          got=error
  [PASS] extra spaces     input='  Ada   Lovelace  '             got={'first': 'Ada', 'last': 'Lovelace'}
  [PASS] apostrophe       input="Sean O'Brien"                   got={'first': 'Sean', 'last': "O'Brien"}
  [PASS] single name      input='Prince'                         got={'first': 'Prince', 'last': ''}
  [PASS] very long        input='AAAAAAAAAAAAAAAAAAAAAAAAAA...   got=error
  Result: 8/8 passed
```

#### Line-by-line explanation

**The module docstring and constant**

- `"""Error guessing demo: ..."""` is a **docstring**, a text in triple quotes at the top of a file that describes it. Python ignores it when running.
- `MAX_NAME_LENGTH = 100` defines a **constant** (a value that should not change), written in capital letters by convention. We decide that names longer than 100 characters are not valid. In a real project this number would come from the requirement. Putting it in one named place avoids "magic numbers" scattered in the code.

**The buggy function**

- `def parse_full_name_buggy(full_name):` defines a function that takes one input called `full_name`.
- The docstring says it works for the happy path only.
- `parts = full_name.split(" ")` cuts the text into a list wherever there is a single space. For `"Ada Lovelace"` we get `["Ada", "Lovelace"]`. **Fault 1:** if `full_name` is `None`, Python has no `.split` to call, so it crashes with an `AttributeError`. **Fault 2:** if the text has extra spaces, `split(" ")` produces empty pieces, so `"  Ada   Lovelace  "` becomes a list that starts with empty strings.
- `first = parts[0]` takes the first piece. With leading spaces this is an empty string, which is wrong.
- `last = parts[-1]` takes the last piece (index `-1` means "last item"). With trailing spaces this is also an empty string. With a single name like `"Prince"` the first and last pieces are the same item, so the last name wrongly becomes `"Prince"`.
- `return {"first": first.capitalize(), ...}` builds a **dictionary** (a set of labeled values) and applies `.capitalize()`, which makes the first letter capital and **all other letters lowercase**. That turns `O'Brien` into `O'brien`, which is a data-damaging bug. The same call also quietly lowercases names such as `McDonald` (becoming `Mcdonald`) and `DeSouza`.
- For an empty string, `"".split(" ")` gives `[""]`, so the function "succeeds" with empty names, silently returning garbage instead of a clear error.
- A very long input is accepted without any limit, which could later overflow a database column.

**The fixed function**

- `if not isinstance(full_name, str):` checks that the input is text. `isinstance(x, str)` returns `True` if `x` is a string. `None`, numbers, and lists fail this check.
- `raise ValueError("name must be text")` stops the function and signals a clear, intentional error. A **ValueError** is Python's standard way of saying "the value you gave me is not acceptable". This is much better than an accidental crash with an unclear message.
- `cleaned = " ".join(full_name.split())` is a neat trick. Calling `.split()` with **no argument** splits on any run of whitespace (spaces, tabs, new lines) and drops empty pieces. `" ".join(...)` then glues the pieces back with exactly one space. So `"  Ada   Lovelace  "` becomes `"Ada Lovelace"`, and a whitespace-only string becomes an empty string.
- `if cleaned == "":` catches both the empty string and the whitespace-only string, because both are empty after cleaning. We raise a `ValueError` saying the name must not be empty.
- `if len(cleaned) > MAX_NAME_LENGTH:` rejects overly long input using the constant defined at the top.
- `parts = cleaned.split(" ")` now safely splits the clean text on single spaces.
- `first = parts[0]` is always safe because we know the text is not empty.
- `last = parts[-1] if len(parts) > 1 else ""` is a **conditional expression** (a compact if/else). If there is more than one piece, the last piece is the last name. If there is only one piece, we return an empty last name instead of copying the first name.
- `return {"first": first, "last": last}` returns the names exactly as the user typed them. We deliberately removed `.capitalize()`, because forcing capitalization damages real names. This is a good example of a **design decision** to discuss with the team: automatic capitalization looks tidy but breaks `O'Brien`, `McDonald`, `van der Berg`, and others.

**The test data**

- `CASES = [...]` is a list of tuples. Each tuple holds three things: a label naming the guessed fault, the input, and the expected outcome. Putting test data in one table keeps the tests readable and makes it easy to add a new guess later. This is a small preview of data-driven testing, which you will meet on Friday.
- `"A" * 5000 + " Smith"` builds a 5,006-character string: 5,000 letter A characters followed by a space and "Smith". Python's `*` operator repeats text.
- The expected outcome is either a dictionary or the word `"error"`, meaning we expect a clean `ValueError`.

**The test runner**

- `def run(func):` takes any function and runs every case against it, so we can use the same cases on both versions.
- `passed = 0` counts passes.
- `for label, value, expected in CASES:` loops over the cases and unpacks each tuple into three names.
- `shown = ...` makes a short printable version of the input, truncated with `...` if it is long, so the output stays readable. `repr(value)` shows the value as Python code, so quotes and `None` are visible.
- `try:` starts a block where errors can be caught.
- `actual = func(value)` calls the function under test.
- `except ValueError as exc:` catches the deliberate error and records it as `"error"`.
- `except Exception as exc:` catches any other, unexpected error (such as the `AttributeError`) and records it as a `CRASH` with the name of the error. This is the important distinction: a clean `ValueError` is acceptable behavior, but a crash is a defect.
- `ok = outcome == expected` compares what we got with what we expected. This is the **test oracle** (the source of the expected result).
- `passed += ok` adds one when `ok` is `True`, because `True` counts as 1.
- The `print(f"...")` line prints a formatted line. The `f` before the quote makes it an **f-string**, in which `{...}` is replaced by values. `{label:<16}` pads the label to 16 characters, left-aligned, so the columns line up.
- `if __name__ == "__main__":` means "run this part only when the file is executed directly, not when imported". Inside it we run the whole case list against the buggy function and then the fixed one.

**What the output teaches us**

The buggy function passed only the happy-path test (1 of 8). Seven guessed inputs exposed seven distinct faults: a crash on `None`, silent acceptance of empty and whitespace-only text, wrong handling of extra spaces, damaged capitalization of the apostrophe name, a wrong last name for a single name, and no length limit. A tester who only tried `"Ada Lovelace"` would have declared the function working. Notice that these inputs were not derived from any specification. They were guessed from experience. After the fix, all 8 pass.

> **Note on the expected results.** We decided that a single name gets an empty last name and that over-100-character names are rejected. These are assumptions for the demo. In a real project, you would confirm such rules with the product owner before writing the expected results.

---

## Using AI Assistants to Brainstorm Error-Guessing Ideas

AI assistants can be excellent brainstorming partners for error guessing because they have "read" far more software bug stories than any individual. You can ask:

- "List 30 error-guessing ideas for a registration form with first name, last name, email, password, and date of birth. Group them by category."
- "Here are 10 past bugs from our tracker. Suggest related faults that might exist elsewhere in the system."
- "Create a checklist of fault ideas for a file-upload feature."
- "What would a developer commonly forget when handling dates?"

A good prompt gives context (type of app, fields, rules), asks for a format (a table with input and expected result), and asks for categories. Then you **review and refine**.

**Cautions you must remember:**

1. **Verify everything.** An AI can produce confident but wrong statements. It may call something a defect when it is acceptable behavior in your product.
2. **Beware of hallucinated expectations.** A **hallucination** is a confident answer that is invented or incorrect. An AI may state "the expected result is that the system rejects emojis" when your specification allows them. The expected result must come from **your requirements**, not from the assistant's guess. Treat AI output as a list of *ideas to test*, never as a source of truth about *what is correct*.
3. **Do not paste confidential data.** Avoid real customer data, secrets, passwords, or proprietary code in prompts, unless your company has approved the tool for that purpose.
4. **Beware of generic lists.** An AI does not know your product's history. Your own bug database is still the richest source. Combine both.
5. **Stay accountable.** You are responsible for the tests you run and the defects you report. Re-run and confirm a failure yourself before logging it.
6. **Security-style ideas.** If an assistant suggests inputs aimed at breaking in, remember the safety note earlier: test only with authorization, and keep it at the "treated as data" level.

A healthy workflow: (1) write your own list first, (2) ask the AI for additional ideas, (3) review each idea against the requirements, (4) keep, reword, or discard, (5) add the keepers to the checklist. Writing your own list first guards against anchoring on the AI's suggestions.

---

## Pair Testing, Mob Testing, and Bug Bashes

Because error guessing depends on personal experience, one of the best ways to improve it is to **share experience**.

**Pair testing** means two people test together at one computer: one drives (types and operates the software) and one navigates (observes, suggests ideas, takes notes). They swap roles regularly. A developer and a tester, or a beginner and an experienced tester, make a great pair because they bring different guesses. Thursday's exercise uses this approach: you will design tests and cross-review each other's work.

**Mob testing** is the same idea with a small group (three or more) around one screen, rotating the driver.

**A bug bash** is a time-limited event in which many people from different roles (testers, developers, product owners, designers, support staff) test the same application at once, often just before a release, to find as many defects as possible. A bug bash is error guessing at scale: each person tries what they would guess to be risky. Typical bug-bash tips:

- Set a timebox (for example, 60 to 90 minutes).
- Share a starter checklist of fault ideas and areas, and assign areas so people do not all test the same page.
- Agree on how to report (one shared sheet or Jira labels), and how to avoid duplicates.
- Give a small prize for the most valuable bug, to keep it fun.
- Triage (sort and prioritize) the reported issues afterwards and add new fault ideas to the checklist.

The benefit is diversity: a support agent knows what customers complain about, a developer knows where the code is fragile, and a tester knows the catalog. Together they cover more ground than any single person.

---

## Common Mistakes

1. **Treating error guessing as random clicking.** Guessing without a list, a timebox, or notes is hard to defend and hard to repeat. Use the process.
2. **Using it instead of systematic techniques.** It complements EP, BVA, and use-case testing. Do the systematic work first, then add guesses.
3. **Never writing guesses down.** Undocumented tests cannot be reviewed, repeated, or reused, and defects are harder to reproduce.
4. **Not stating expected results.** A guess without an expected result is a poke at the software, not a test. Write what should happen, based on the requirement.
5. **Only guessing what you already know.** Bias keeps you in your comfort zone. Borrow ideas from colleagues, checklists, and defect history.
6. **Over-investing in unlikely faults.** Prioritize by likelihood and impact.
7. **Ignoring the side effects.** Check the data created, logs written, and emails sent, not just the screen message.
8. **Reporting every oddity as a defect.** Check the requirement. Sometimes the behavior is correct or a deliberate design decision. Ask first.
9. **Skipping the checklist update.** If the checklist never grows, the technique never improves.
10. **Going too far with security-style inputs.** Stay within authorization and your company's rules.
11. **Trusting AI-suggested expectations.** The requirement is the oracle, not the assistant.
12. **Forgetting to retest after fixes.** Bugs found by guessing deserve a follow-up check once fixed (regression, covered Friday).

---

## Try It: Error Guessing on Project 1

**Format:** Pair activity (pair programming style: driver and navigator, swapping roles every 15 minutes). **Time:** about 60 minutes.

**Part A - Build the checklist (15 minutes).**
1. Open the Project 1 Registration and Login pages and the requirements.
2. Together, build a fault list with at least 6 categories, using the catalog in this lesson. Add at least **five items of your own** that are specific to Project 1.
3. Decide on a timebox for the testing part.

**Part B - Derive test ideas (15 minutes).**
Write at least **20 test ideas** in a table with the columns: ID, area, guessed fault, test input or action, expected result. Make sure at least 5 do not fit any EP or BVA partition (for example, double submit, Back button, and session expiry).

**Part C - Run the attack (20 minutes).**
Run your tests against the app. Record actual results and a verdict. Take screenshots of any failure. Log any real defect with clear steps (using the defect lifecycle you practiced on Tuesday).

**Part D - Cross-review (10 minutes).**
Swap your table with another pair. Review their expected results against the requirements. Ask: Are any expected results guessed instead of taken from the requirements? Is there a missing category? Add at least three tests you think they missed, and ask them to review yours.

**Part E - Reflect (briefly).**
Which guesses found defects? Which never will? What goes at the top of the checklist next time?

**Deliverable:** your checklist, your test table with results, any defect reports, and three lines of reflection.

---

## Practice Exercises

Try each exercise on your own first, then compare with the sample answers.

### Exercise 1: A search box
List at least 10 faults you would guess.

**Sample answers:**
1. Empty search and spaces-only search
2. Very long search text (thousands of characters)
3. Special characters and wildcard-like characters (`%`, `*`, `_`, `?`, quotes)
4. Code-like text (tags, database words) is displayed as plain text
5. Case differences and accented letters
6. Zero results: friendly message instead of blank or error
7. Thousands of results: performance and paging
8. Page number beyond the last page, and page zero
9. Pressing Enter twice or searching again while the first search is running
10. Back button and refresh keep or lose the search term
11. Emoji or non-Latin text
12. Sorting with identical or empty values

### Exercise 2: A date-of-birth field
List at least 10 faults you would guess.

**Sample answers:**
1. Leap day in a leap year (29 Feb 2000) and in a non-leap year (29 Feb 2001)
2. 29 Feb 2100 (not a leap year)
3. Impossible dates: 31 Apr, 32 Jan, month 13, day 0
4. Future date (tomorrow), today, and a date a very long time ago (year 1800)
5. Age boundaries: user turns 18 today, tomorrow, yesterday (relates to BVA)
6. Format confusion: 03/04/2000 (day/month or month/day?)
7. Typed text instead of a date, or a date with letters
8. Time zone: a user near midnight in another time zone; the date saved as a different day
9. Clearing the field after selecting a date
10. Leading zeros missing (`3/4/2000`)
11. Copy-pasted date with spaces
12. Two-digit year (`00` meaning 1900 or 2000?)

### Exercise 3: A file-upload feature
List at least 10 faults you would guess.

**Sample answers:**
1. Empty (0-byte) file
2. File exactly at the size limit and one byte above it
3. Huge file; timeout behavior
4. Wrong type (text file renamed to `.jpg`)
5. Double extension (`photo.jpg.exe`) and uppercase extension (`.JPG`)
6. No extension, or file with only an extension (`.png`)
7. Special characters, spaces, and very long file name
8. Same file uploaded twice, or two different files with the same name
9. Multiple files at once and more than the allowed number
10. Network lost during upload; cancel during upload
11. Corrupt or password-protected file
12. Upload then delete then upload again; downloading the file back gives identical content

### Exercise 4: A "transfer money" form
List at least 12 faults you would guess.

**Sample answers:**
1. Amount zero, negative, empty
2. Amount with many decimals (10.005) and rounding
3. Decimal separator comma vs point (`10,50`)
4. Very large amount (overflow) and the smallest amount (0.01)
5. Amount greater than the balance, exactly equal to the balance, and one cent more
6. Transfer to the same account (from = to)
7. Invalid or closed destination account; account number with spaces or letters
8. Double-click on Submit (money sent twice)
9. Refresh or Back after submitting
10. Network failure after submit: is the money moved, and is the user told correctly?
11. Session expiry before confirming
12. Two transfers at the same time from the same account (race condition, overdraft)
13. Transfer limit per day and per transaction
14. Reference text with special characters, emoji, very long text
15. Scheduling a transfer on 29 Feb, on a weekend or holiday, or across a time zone
16. Currency conversion rounding and rate changing between screens
17. Two users editing the same account in two tabs

---

## Knowledge Check

**Q1. Define error guessing in one sentence.**
*Answer:* An experience-based technique where the tester anticipates likely defects from knowledge, intuition, and past defects, and designs tests to expose them.

**Q2. Name three reasons it finds real defects.**
*Answer:* Defects cluster in certain areas; developers repeat the same kinds of mistakes; human error patterns are predictable; specifications are silent on many situations. (Any three.)

**Q3. Name five sources of experience for error guessing.**
*Answer:* Past defects; defect logs/bug databases; production incidents; user complaints; developer knowledge; domain knowledge; known failure patterns; checklists. (Any five.)

**Q4. What is a fault attack?**
*Answer:* A targeted approach in which tests are designed from a list of suspected faults, each test deliberately trying to provoke the failure if the fault exists.

**Q5. Why do we timebox error-guessing sessions?**
*Answer:* Because there is no natural end to guessing. A timebox keeps the session focused, prioritizes the most likely faults, and makes effort easy to plan.

**Q6. A registration form fails for the name "D'Angelo". Which category of the catalog does this belong to, and which other fields should you check?**
*Answer:* Quotes and apostrophes (special characters). Check every text field that stores or displays user text: other names, address, comments, search, profile.

**Q7. How does error guessing relate to negative testing and exploratory testing?**
*Answer:* Error guessing describes how tests are chosen (from anticipated faults). Negative testing describes the type of test (invalid or unexpected conditions); many guessed tests are negative. Exploratory testing (Friday) is a broader style of simultaneous learning, design, and execution, and often uses error guessing as one tool.

**Q8. Give two strengths and two weaknesses of error guessing.**
*Answer:* Strengths: fast; cheap; finds unusual defects; no formal specification needed. Weaknesses: depends on tester skill; not repeatable; no coverage measure; bias.

**Q9. Name three ways to make error guessing more systematic.**
*Answer:* Checklists; fault attacks; defect-based testing from past bugs; timeboxing and note-taking; pairing; measuring defects found.

**Q10. In the Python demo, why did the buggy function pass only one of eight tests?**
*Answer:* It was written only for the happy path. It crashed on `None`, accepted empty and whitespace-only text, mishandled extra spaces and single names, damaged apostrophe capitalization with `.capitalize()`, and had no length limit.

**Q11. Using the defect history table, which module shows signs of defect clustering, and which root cause is most common?**
*Answer:* Registration (four of ten bugs); and the most common cause is poor handling of input (trimming, special characters, length, and duplicate submission).

**Q12. An AI assistant says the expected result for emoji in a name is "reject". Can you use that as the expected result?**
*Answer:* No. Expected results come from your requirements or the product owner. The AI output is only an idea to test.

**Q13. What is a bug bash and why does it suit error guessing?**
*Answer:* A time-limited event where people from many roles test the same app together to find defects. It combines many different experiences and guesses.

**Q14. Why is it risky to rely only on error guessing?**
*Answer:* It depends on the tester, is hard to repeat, has no coverage measure, and can miss faults outside the tester's experience. It should complement systematic techniques.

**Q15. Why might a leap-day test be called both an error guess and a boundary test?**
*Answer:* 29 Feb is an edge of the valid day range for February (BVA thinking) but it is also a famous fault area known from experience (error guessing). Techniques often overlap.

---

## Key Takeaways

- **Error guessing** is an experience-based technique: anticipate defects, then design tests that expose them. It complements, and never replaces, EP, BVA, and use-case testing.
- It works because **defects cluster**, **developers repeat mistakes**, **human error patterns are predictable**, and **specifications are silent** in many places.
- Sources of experience include past defects, bug databases, production incidents, user complaints, developer and domain knowledge, and checklists. Beginners can borrow experience from others.
- A good process is: understand, gather sources, build a fault list, run a fault attack, timebox, document, and update the checklist.
- The catalog (empty and whitespace, length, special characters and Unicode, quotes, code-like text treated as data, numbers, copy-paste and case, double submit and Back, session and concurrency, dates, files, money, locale, network, permissions) gives you a head start on any feature.
- Compare to negative testing (a type of test) and exploratory testing (a style, Friday). They overlap but are not the same.
- Strengths: fast, cheap, finds unusual defects. Weaknesses: skill-dependent, hard to repeat, no coverage measure, bias.
- Make it systematic with checklists, fault attacks, defect-based testing, timeboxes, note-taking, and pairing, and measure it by defects found.
- Use AI assistants for ideas, never for expected results. Verify everything against the requirements.
- Share experience through **pair testing** and **bug bashes**.
- Next: decision tables and state transition testing add more systematic techniques to your toolbox, and Friday brings exploratory, regression, and data-driven testing.

---

## Additional Resources

- **ISTQB Glossary** (definitions of error guessing, experience-based testing, defect-based testing): https://glossary.istqb.org/
- **Guru99 - Error Guessing Technique**: https://www.guru99.com/error-guessing.html
- **Ministry of Testing** (articles, community, and talks about testing ideas and heuristics): https://www.ministryoftesting.com/
- **OWASP Web Security Testing Guide** (a conceptual introduction to input validation testing; use only on systems you are authorized to test): https://owasp.org/www-project-web-security-testing-guide/
