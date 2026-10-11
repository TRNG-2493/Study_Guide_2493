# Positive and Negative Testing

**Week 3 - Quality Engineering Foundations | Wednesday: Testing Fundamentals**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Define positive testing (also called valid-path or "happy path" testing) and negative testing in your own words.
2. Explain why a team needs both kinds of tests, and what each one protects.
3. Distinguish the happy path, alternate paths and exception paths of a feature.
4. Name and recognise at least fifteen categories of negative tests and give an example of each.
5. Describe what a good expected result looks like for a negative test.
6. Derive positive and negative test cases from requirements and acceptance criteria using a repeatable method.
7. Write well-formed test cases (ID, title, priority, preconditions, steps, data, expected result) for registration and login features.
8. Read and run a short Python demonstration of positive and negative tests for a `validate_password` function.
9. Log a failure you discover in a clear, reproducible way.
10. Use a negative-testing checklist when reviewing any form.

---

## Why This Matters

Imagine you are hired to check a new front door before a family moves into a house. The first thing you would do is put the correct key in the lock and turn it. The door opens. Good. But would you hand the keys to the family at that point? Of course not. You would also try a wrong key. You would try no key at all. You might push, pull and (politely) kick the door to see whether it holds. A door that opens for the right key but also opens for the wrong key, or collapses under a firm shove, is not a good door.

Software works the same way. Many beginners test only the situations in which everything goes right: they type a valid email, a valid password, press the button, and the system behaves. That is a necessary first step, but it is only half of the picture. Real users make typing mistakes, paste text with hidden spaces, press buttons twice, lose their connection halfway through, and (occasionally) try to break in. A product that is only checked with perfect input is a product that has not really been checked.

Earlier today you learned about the testing mindset, about errors, defects and failures, and about the testing principles. One of those principles says that **exhaustive testing is impossible**, so we must choose our tests wisely. Another says that **testing shows the presence of defects, not their absence**. Positive and negative testing is the most practical, everyday application of those ideas. It gives you a simple two-question framework to apply to every feature you ever test:

- "Does it work when everything is right?" (positive)
- "Does it behave sensibly when something is wrong?" (negative)

This lesson prepares you directly for this afternoon's exercise, where you will write positive and negative test cases for the Project 1 login and registration feature, and for the demonstration in which we run an exploratory session and classify what we find. The skills here are also the foundation of automation later in the programme: every automated test you write will be, at its heart, either a positive check or a negative check.

---

## The Concept

### 1. Definitions

Let us define the terms carefully, because the whole lesson builds on them.

**Positive testing** is testing that verifies the system does what it should when it is given **valid input** and used in the **expected way**. It is also called **valid-path testing**, **"happy path" testing** or **"sunny day" testing**. The question it answers is: "When a user does everything correctly, does the product deliver the promised result?"

**Negative testing** is testing that verifies the system handles **invalid, unexpected or malicious input and conditions** gracefully. It is sometimes called **invalid-path testing**, **error-path testing** or **"rainy day" testing**. The question it answers is: "When something goes wrong, does the product stay safe, stay stable and tell the user what happened?"

Notice the word **gracefully**. In negative testing, a test does not "pass" because the system accepted bad input, and it does not "pass" merely because nothing exploded. It passes when the system **rejects or handles** the bad situation in a controlled, helpful and safe way. A negative test for a login form with a wrong password *passes* when the system refuses to log the user in and shows a clear, safe message. If the system logs the user in, the test *fails*, even though "login succeeded" looks like a positive outcome.

This is a very common point of confusion, so let us fix it clearly:

> **Positive or negative describes the test input and scenario, not whether the test passed or failed.** A negative test is a test with bad input or a bad situation. It can pass (system handled it well) or fail (system handled it badly), just like a positive test.

**A word about vocabulary.** In this lesson we use these terms:

| Term | Meaning |
|---|---|
| **Input** | Any data or action a user or another system gives to the product (typing text, clicking a button, uploading a file). |
| **Valid input** | Input that follows all the rules the product has set for it. |
| **Invalid input** | Input that breaks one or more of those rules. |
| **Validation** | The checks a product performs to decide whether input is acceptable. |
| **Error message** | The text the product shows to tell the user that something went wrong. |
| **Graceful handling** | Responding to a problem in a controlled way: no crash, no lost data, and a clear message. |
| **Test case** | A documented set of steps, data and an expected result used to check one specific behaviour (you met the structure on Tuesday). |
| **Precondition** | The state that must be true before the test starts (for example, "user account exists"). |
| **Expected result** | What the product should do if it is working correctly. |
| **Actual result** | What the product really did when you ran the test. |

### 2. The door analogy, step by step

Let us return to the door, because it maps neatly onto everything that follows.

| Door scenario | Testing type | What we check |
|---|---|---|
| The correct key opens the door. | Positive | The main purpose works. |
| The door also locks again with the correct key. | Positive | The complementary action works. |
| A wrong key does not open the door. | Negative | Invalid input is rejected. |
| A key that is nearly right (bent, similar teeth) does not open it. | Negative | Near-miss input is also rejected. |
| No key at all; the handle will not turn. | Negative | Missing input is handled. |
| Someone kicks the door. | Negative (robustness) | The system holds under unexpected stress. |
| Someone puts the key in and turns it twice very quickly. | Negative (unusual usage) | Repeated actions do not break the lock. |
| The door is opened in the middle of a storm (unusual conditions). | Negative (environment) | Environmental conditions are handled. |

Notice how many more negative scenarios there are than positive ones. That is normal. There is usually **one** way to do something correctly and **many** ways to do it incorrectly. This is why skilled testers spend a large share of their time thinking about negative situations.

### 3. Why both kinds of testing matter

Positive and negative testing protect different things. A team that skips either one has a blind spot.

**Positive testing builds confidence.** It confirms that the features users actually want do work. If the happy path fails, the product is useless to everyone, so positive tests are usually the first tests run and the first ones that are automated.

**Negative testing builds robustness.** Robustness means the ability to keep working properly under unexpected or hostile conditions. Real users are unpredictable, and the internet is not always friendly. A robust product survives that unpredictability.

Let us look at four specific reasons negative testing matters.

1. **Security.** Many security problems begin with input the developers did not expect: text that is far too long, special characters, or text that looks like code. If a form treats such text as *instructions* instead of as *plain data*, an attacker might read or change information they should never see. Negative tests are one of the first lines of defence. (We discuss this only at a conceptual level here; our goal is to check that the product treats such input safely, not to learn how to attack anything.)

2. **Error messages.** When something goes wrong, the user needs to know what happened and what to do next. A good error message says "Enter a valid email address, for example name@example.com." A bad one says "Error 500", shows a technical stack trace, or says nothing at all. Messages are part of the user experience, and they can also leak private information if written carelessly.

3. **Data integrity.** Data integrity means data stays accurate, consistent and complete. A double-click on a "Pay" button that creates two orders, or a lost connection that leaves half a record saved, damages data integrity. Negative tests find these problems before real customers' data is affected.

4. **Reputation and cost.** A crash or a confusing failure in front of a real user costs trust. Finding it during testing costs a small amount; finding it in production costs far more. (This echoes the principle that early testing saves money.)

A short way to remember it:

> **Positive testing asks "Can it work?" Negative testing asks "Can it fail safely?"**

### 4. Happy path, alternate paths and exception paths

Before we write test cases, we need a good way of thinking about the different routes a user can take through a feature. Testers usually describe three kinds of paths.

**The happy path** (also called the **main success scenario**) is the most common, simplest route that ends successfully. Example for registration: the user opens the page, fills in every field correctly, accepts the terms, presses "Register", and sees "Account created."

**Alternate paths** are other *valid* routes to a successful outcome. They are different from the main route but still correct. Examples for registration:

- The user registers with an email address that contains a plus sign (`jane+test@example.com`), which is valid.
- The user chooses the longest allowed username.
- The user fixes a mistake after the first attempt fails (enters a weak password, sees an error, corrects it, and succeeds).
- The user registers using the keyboard only (Tab and Enter) without a mouse.

**Exception paths** (also called **error paths** or **failure paths**) are routes where something goes wrong. The user is not following the rules, or the situation is abnormal. Examples:

- The email is already registered.
- The password is too weak.
- The network drops as the user presses "Register."
- The user leaves the terms box unchecked.

Here is how these map onto our two testing types:

| Path | Description | Testing type |
|---|---|---|
| Happy path | The simplest successful journey | Positive |
| Alternate path | A different but still valid journey | Positive |
| Exception path | A journey where something goes wrong | Negative |

A common beginner mistake is to treat "alternate path" as a negative test because it feels unusual. Remember: if the input and conditions are *valid* and the expected outcome is *success*, it is a positive test, no matter how unusual it looks. A 20-character username that is exactly the maximum length allowed is unusual but valid, so it is positive.

### 5. Categories of negative tests

Negative tests can feel overwhelming at first because there are so many possible ways to go wrong. The good news is that the ways fall into recognisable **categories**. Learning these categories gives you a mental menu you can apply to any feature. Below, each category has an explanation and examples.

#### 5.1 Invalid data type

A **data type** is the kind of data a field expects: text, a whole number, a decimal, a date, and so on. An invalid data type test enters the wrong kind of data.

Examples: letters in an "Age" field; a word in a "Quantity" field; text in a date field; a decimal like `2.5` where only whole numbers are allowed.

#### 5.2 Empty, null and whitespace values

- **Empty** means nothing was entered at all.
- **Null** means "no value" at a technical level (for example, a field missing entirely from a request).
- **Whitespace** means only spaces, tabs or line breaks. A field containing only spaces *looks* empty, but a careless system may treat it as a real value.

Examples: leaving "Username" blank; typing three spaces in "Username"; typing a space before or after the email address (`" jane@example.com "`).

#### 5.3 Too long and too short

Fields usually have a minimum and maximum length. Negative tests go beyond those limits.

Examples: a one-character username when the minimum is four; a 300-character email when the maximum is 254; a password of 7 characters when the minimum is 8; a 10,000-character comment pasted into a small text box. Very long input can cause layout problems, database errors or slow responses.

(Choosing the *exact* values near the limits is the job of Boundary Value Analysis, which you will learn on Thursday. For now, simply notice that "too long" and "too short" are categories.)

#### 5.4 Special characters

Special characters are symbols such as `! @ # $ % ^ & * ( ) ' " < > / \ ; :` and also characters from other languages, accented letters and emoji. Systems sometimes handle them badly.

Examples: an apostrophe in a name (`O'Brien`), which is perfectly valid in real life and breaks poorly written systems; a username containing `#` when only letters are allowed; emoji in a text field; characters from non-Latin scripts.

Be careful here: some special characters are *valid* in some fields (the apostrophe in a surname) and *invalid* in others (the apostrophe in a username). Always check the requirement before deciding whether a test is positive or negative.

#### 5.5 Code-like strings treated as data (input validation concept)

Some text looks like programming or database instructions. Examples include text with quote marks and the word `DROP`, or text wrapped in angle brackets like a web page tag. The safe expectation is that the product treats such text as **ordinary data**: it either stores or rejects it as plain text, and never "runs" it.

Two well-known families of problems exist where systems fail to do this. Without going into any attack technique, you should know their names:

- **SQL injection:** database instructions smuggled in through an input field.
- **Cross-site scripting (XSS):** web page code smuggled in through an input field so that it runs in another user's browser.

As a beginner tester, your job is limited and safe: enter harmless code-like text *in an environment you are authorised to test* and confirm that the product treats it as plain text, shows no technical error and shows no unexpected behaviour. If you ever see a database error, a stack trace, or the text behaving like code, you have found a potentially serious defect and should report it to the team immediately and follow your organisation's security process. You do not need to (and should not) try to take advantage of it. Dedicated security testing is a specialised discipline, and testing without permission is not acceptable.

#### 5.6 Wrong format

A format is a required pattern. The value may be the right type but still not match the pattern.

Examples: an email without `@` (`jane.example.com`); an email without a domain (`jane@`); a phone number with letters; a date written as `31/02/2025` (a date that does not exist) or in the wrong order; a postal code of the wrong length.

#### 5.7 Out-of-range values

A range is the set of allowed values. Out-of-range input falls outside it.

Examples: age of `-5` or `250`; quantity `0` or `-1` in a shopping cart; a birth date in the future; a start date later than the end date; a discount of 150 percent.

#### 5.8 Duplicate data

Some values must be unique (email, username, national ID). Duplicate testing tries to create the same value twice.

Examples: registering with an email that already exists; registering with the same email in different letter case (`JANE@example.com` versus `jane@example.com`); creating two products with the same SKU; adding the same item to a list twice.

#### 5.9 Missing required fields

Required fields (usually marked with an asterisk) must be filled. Tests leave one empty at a time, and then several or all empty.

Examples: submitting the registration form with only the email missing; submitting with everything blank; submitting without ticking a mandatory terms box.

Why "one at a time"? If you leave three fields empty and see one error, you cannot tell whether the other two fields are validated at all. Testing them individually isolates each rule.

#### 5.10 Wrong order of steps

Many features are a sequence: Step 1, Step 2, Step 3. Users do not always follow the sequence.

Examples: opening the "Order confirmation" web address directly without placing an order; jumping to step 3 of a checkout by editing the address; trying to reset a password using a link before requesting it; submitting a form whose earlier step was skipped.

#### 5.11 Expired session

A **session** is the period during which the system remembers that you are logged in. Sessions end after a time limit or when you log out. An expired session test checks what happens when you keep working after that point.

Examples: leaving a page open past the timeout and then pressing "Save"; being logged out in another tab and then submitting in the first tab; using an old password-reset link after it has expired.

#### 5.12 Unauthorised access

**Authentication** means proving who you are (logging in). **Authorisation** means what you are allowed to do once logged in. Unauthorised access tests check that people cannot reach things they are not allowed to.

Examples: typing the address of a members-only page while logged out; a normal user trying to open an admin page; user A changing a number in the address to view user B's profile; using a feature after the account has been disabled.

#### 5.13 Network interruption

Networks fail. The user's Wi-Fi drops, a server restarts, a request takes too long.

Examples: switching off the connection just after pressing "Submit"; very slow connection making the request time out; losing the connection during a file upload. We expect a clear message, no half-saved data, and the ability to retry safely.

#### 5.14 Double-click and double-submit

Users, especially impatient ones, press buttons repeatedly. Double-submit testing presses a button two or more times quickly, or presses Enter and then the button.

Examples: double-clicking "Register" and checking that only one account is created; double-clicking "Pay now" and checking only one charge happens; pressing Enter twice in a form.

#### 5.15 Browser back button (and refresh, forward)

Browsers have navigation controls that the application does not control.

Examples: after logging out, pressing Back to see if private pages still appear; after submitting a form, pressing Back and re-submitting; refreshing the page right after a successful payment (does it charge again?); opening the same form in two tabs.

#### 5.16 Unsupported file types and files that are too large

Where a product accepts uploads, it should accept only the expected types and sizes.

Examples: uploading an `.exe` file where only `.jpg` and `.png` are allowed; renaming a text file to end with `.jpg`; uploading an empty (zero-byte) file; uploading a file larger than the maximum; uploading a file with a very long name or special characters in its name.

#### Quick summary table of categories

| # | Category | One-line idea | Typical example |
|---|---|---|---|
| 1 | Invalid data type | Wrong kind of data | Letters in a number field |
| 2 | Empty, null, whitespace | Nothing, or only spaces | Username of three spaces |
| 3 | Too long / too short | Beyond length limits | 300-character email |
| 4 | Special characters | Symbols, accents, emoji | `#` in username |
| 5 | Code-like strings | Text that looks like code, handled as data | Quote marks and the word DROP in a name field |
| 6 | Wrong format | Right type, wrong pattern | `jane@` as email |
| 7 | Out of range | Outside allowed values | Age `-5` |
| 8 | Duplicate data | Same unique value twice | Existing email |
| 9 | Missing required field | Required value left out | No username |
| 10 | Wrong order of steps | Skipping or reversing a sequence | Open step 3 directly |
| 11 | Expired session | Acting after timeout | Save after 30 idle minutes |
| 12 | Unauthorised access | Reaching what you should not | Member page while logged out |
| 13 | Network interruption | Connection lost or slow | Offline during submit |
| 14 | Double-click / double-submit | Repeated actions | Two clicks on Pay |
| 15 | Browser back / refresh | Browser navigation | Back after logout |
| 16 | Unsupported file types | Wrong or oversized upload | `.exe` as avatar |

Keep this table nearby. When you meet a new feature, walk down the list and ask, "Does this category apply here?" That single habit will make your testing dramatically more complete.

### 6. Expected-result thinking for negative cases

For a positive test, the expected result is usually obvious: the thing worked. For a negative test, writing the expected result takes more thought, because "it did not work" is not an expected result. We need to describe precisely what **good failure** looks like.

When you write the expected result of a negative test, consider each of the following points.

1. **A clear, helpful error message.** The message should be understandable to an ordinary user, say what was wrong and ideally how to fix it. Example: "Password must be at least 8 characters." A message such as "Invalid input" is weak; "NullReferenceException at line 214" is unacceptable.

2. **No crash.** The page, the application and the server must keep working. No blank white screen, no "500 Internal Server Error", no frozen interface.

3. **No data loss.** Information the user already entered correctly should normally remain in the form (except sensitive fields such as passwords, which are commonly cleared). Saved data elsewhere must not be corrupted.

4. **No sensitive information leak.** Error messages must not reveal passwords, technical details, file paths, database names or whether specific accounts exist where that would help an attacker. A classic example: on login failure, say "Email or password is incorrect" rather than "That email is registered but the password is wrong", because the second message lets an attacker discover which emails have accounts.

5. **Field-level validation.** The error should point at the exact field with the problem (for example, highlighted in red with a message next to it), rather than a vague message at the top of the page.

6. **System state unchanged.** The failed action must not have side effects. A rejected registration must not create a partial account; a failed payment must not reduce stock; a rejected login must not create a session.

7. **Logging.** Where the requirement says so, the system should record the event (for example, a failed login attempt), without recording sensitive values such as the password itself. Testers usually cannot see the logs directly, but they may verify them with developer support or through an admin screen.

You can use this as a template sentence for negative expected results:

> "The system rejects the [action], displays [specific message] next to [field], keeps [other data] intact, does not [create/change/log in], and shows no technical or sensitive details."

Compare two versions of an expected result for "register with an existing email":

| Weak | Strong |
|---|---|
| "Error appears." | "Registration is rejected. The message 'This email is already registered' appears beside the Email field. No new account is created. Other entered values remain in the form, except the password fields. No technical error is shown." |

The strong version can be checked objectively by anyone on the team. That is the aim: **an expected result that two different testers would judge the same way.**

### 7. Deriving positive and negative test cases from requirements

How do we decide *which* tests to write? Not by guessing at random. On Tuesday you learned requirements analysis and acceptance criteria. Now we turn those into test cases with a simple, repeatable method.

**The method: Inputs, Rules, States, then one positive and at least one negative for each rule.**

**Step 1: List the inputs.** What can the user type, choose, click, upload or send? For registration: email, username, password, confirm password, terms checkbox, the Register button.

**Step 2: List the rules.** Read the requirements and underline every rule: required/optional, length, allowed characters, format, uniqueness, relationships between fields (confirm equals password).

**Step 3: List the states.** What conditions of the system or user matter? Logged in or out, account exists or not, account locked or active, session valid or expired, network available or not, item in stock or not.

**Step 4: For every rule, write one positive and at least one negative.**

- The **positive** proves the rule allows what it should.
- The **negative(s)** prove the rule blocks what it should. If a rule can be broken in several different ways, write a negative for each way.

**Step 5: Add scenario-level cases.** Beyond individual rules, add the happy path, alternate paths, and the system-level negatives (network, double-submit, back button, session).

**Step 6: Review and prioritise.** Remove duplicates, assign priorities, and check that every requirement is covered by at least one case (this check is called **traceability**).

Here is a worked mini-example. Suppose the requirement says:

> *REQ-12: The "Quantity" field accepts whole numbers from 1 to 10.*

- Input: Quantity.
- Rule: whole number; minimum 1; maximum 10.
- Positive cases: `5` (typical), `1` and `10` (valid at the edges).
- Negative cases: `0` (below), `11` (above), `-3` (negative), `2.5` (not whole), `abc` (not a number), empty, spaces only.

From a single sentence we have derived roughly ten tests, each with a clear reason for existing. Notice that we did not pick the exact edge values by pure intuition; Thursday's techniques will give you a systematic way of doing that.

### 8. Writing good test cases: the standard fields

On Tuesday you learned the standard structure of a test case. Here it is again, with notes about how positive and negative cases use each field.

| Field | Purpose | Note for positive/negative |
|---|---|---|
| **Test Case ID** | Unique identifier | Use a pattern that shows the feature and type, for example `REG-P-01`, `REG-N-05`. |
| **Title / Summary** | One line describing the check | Start with the situation: "Register with email missing '@'". |
| **Requirement reference** | Which requirement it covers | Supports traceability. |
| **Priority** | How important to run | See below. |
| **Type** | Positive or Negative | Makes filtering easy. |
| **Preconditions** | State before starting | "User is on the registration page; email not registered." |
| **Test data** | Exact values used | Write real values, not "a bad email". |
| **Steps** | Numbered actions | One action per step. |
| **Expected result** | Correct outcome | For negatives, use the points in section 6. |
| **Actual result** | What happened | Filled in during execution. |
| **Status** | Pass / Fail / Blocked | Filled in during execution. |

**Test case IDs.** A good ID is short, unique and meaningful. A popular pattern is `FEATURE-TYPE-NUMBER`. `REG-P-03` means "Registration, Positive, case 3". `LOG-N-12` means "Login, Negative, case 12". Some teams prefer a single running number per feature; either is fine, as long as everyone follows the same convention.

**Priorities.** Priority says which tests to run first when time is short. A common scale:

| Priority | Meaning | Typical examples |
|---|---|---|
| **P1 / High** | Core function or serious risk; must pass before release | Valid login; duplicate account prevention; code-like text handled safely |
| **P2 / Medium** | Important but not blocking | Field-level messages; whitespace trimming |
| **P3 / Low** | Nice to verify; low impact | Cosmetic message wording; rare combinations |

**Ratio guidance.** Students often ask, "How many positive tests versus negative tests should I write?" There is no magic number. Be suspicious of anyone who gives you a precise percentage. The honest answer is: **it depends on risk.** Features that handle money, personal data or security (login, payment, registration) deserve many more negative tests than a simple "About us" page. In practice you will usually find that you write more negative than positive cases for any form-based feature, simply because there are more ways to go wrong than to go right. A healthy sanity check is not a ratio but a question: "For each rule, do I have at least one positive and at least one negative?"

**Rules for good test cases:**

- **One purpose per test case.** If it fails, you should know exactly why.
- **Specific data.** Write the actual values. "Enter invalid email" is vague; "Enter `jane.example.com`" is testable.
- **Specific expected result.** Include the message text if it is in the requirements.
- **Independent where possible.** A test should not depend on the result of another test.
- **Repeatable.** Anyone should get the same result by following the steps.
- **Traceable.** Link it to a requirement.

### 9. Logging failures found by negative tests

When a test fails, the work is not over. You must report it so that it can be fixed. You learned the defect lifecycle and Jira on Tuesday; here is how to apply it to positive and negative failures.

A good defect report for a failed negative test contains:

1. **Title** that states the problem: "Registration accepts email without '@' symbol".
2. **Environment:** application version, browser and version, operating system, test environment.
3. **Preconditions.**
4. **Steps to reproduce:** numbered, exact, including test data.
5. **Expected result:** copied from your test case.
6. **Actual result:** what really happened.
7. **Evidence:** screenshot, short recording, console or network output where relevant.
8. **Severity and priority:** severity is the technical impact; priority is how soon it should be fixed. A failure to block bad input that exposes data is high severity.
9. **Link to the test case ID** and requirement.

Example report:

> **Title:** Registration accepts username containing '#' character
> **Environment:** Project 1 test site v0.3, Chrome 126, Windows 11
> **Steps:** 1. Open /register. 2. Enter email `jane@example.com`. 3. Enter username `jane#1`. 4. Enter valid password and matching confirmation. 5. Tick Terms. 6. Click Register.
> **Expected (REG-N-09):** Registration rejected; message "Username may contain only letters, numbers and underscores" shown beside Username.
> **Actual:** Account created; welcome page displays "jane#1".
> **Severity:** Medium. **Priority:** Medium.

Using the vocabulary from earlier today: the person who wrote the missing validation made an **error** (a human mistake); the missing check in the code is the **defect**; and the **failure** is what you observed when the system accepted the bad username. Your report describes the failure, and developers trace it back to the defect.

### 10. Positive and negative testing together: an overall picture

For any feature, a complete test design contains:

- the **happy path** (positive),
- **alternate paths** (positive),
- **rule-level negatives** (one or more per rule),
- **state-based negatives** (locked, expired, unauthorised),
- **environment and usage negatives** (network, double-submit, back button).

If you were to draw it, the happy path would be a single line through the middle, with many tests branching off it on both sides. Good testers keep that picture in mind.

---

## Examples

### Worked Example 1: Project 1 "User Registration"

Project 1 is our sample web application. Its registration page lets a new visitor create an account. Below are the requirements we will test, followed by a complete set of test cases.

#### Requirements

| Req ID | Requirement |
|---|---|
| REG-01 | **Email** is required. |
| REG-02 | Email must be in a valid format (one `@`, a domain with a dot, no spaces) and at most 254 characters. |
| REG-03 | Email must be unique. Uniqueness ignores letter case. Leading and trailing spaces are removed before checking. |
| REG-04 | **Username** is required, 4 to 20 characters, containing only letters, digits and underscores. |
| REG-05 | Username must be unique. |
| REG-06 | **Password** is required, 8 to 64 characters, with at least one uppercase letter, one lowercase letter, one digit and one special character. Spaces are not allowed. |
| REG-07 | **Confirm password** is required and must exactly match the password. |
| REG-08 | The **Terms and Conditions** checkbox must be ticked. |
| REG-09 | On success the system creates one account, shows "Account created successfully" and redirects to the login page. |
| REG-10 | On any validation failure no account is created, a message appears beside each invalid field and valid entries (except passwords) remain in the form. |
| REG-11 | Pressing Register more than once quickly must create only one account. |
| REG-12 | Password fields mask typed characters, and passwords are never shown in messages. |

#### Test data used in the table

To keep the table readable, we assume the following baseline valid data, referred to as "valid set":

- Email: `jane.doe@example.com`
- Username: `jane_doe`
- Password: `Passw0rd!`
- Confirm password: `Passw0rd!`
- Terms: ticked

Each test changes only what is stated in the Data column; everything else stays at the valid set. This "change one thing at a time" habit makes failures easy to diagnose. Unless stated, the precondition is: the user is on the registration page, and the email and username used are not already registered.

#### Registration test cases

| ID | Type | Pri | Title | Data | Steps | Expected result |
|---|---|---|---|---|---|---|
| REG-P-01 | Positive | P1 | Register with all valid data (happy path) | Valid set | 1. Enter all valid data. 2. Tick Terms. 3. Click Register. | One account is created; "Account created successfully" is shown; user is redirected to the login page (REG-09). |
| REG-P-02 | Positive | P2 | Email with plus sign and subdomain | Email: `jane+qa@mail.example.co.uk` | Enter data; tick Terms; click Register. | Account created; email accepted as valid. |
| REG-P-03 | Positive | P2 | Username of minimum length | Username: `abcd` (4 characters) | Enter data; Register. | Account created. |
| REG-P-04 | Positive | P2 | Username of maximum length | Username: `abcdefghij0123456789` (exactly 20 characters) | Enter data; Register. | Account created; full 20-character username stored. |
| REG-P-05 | Positive | P2 | Username with underscore and digits | Username: `jane_doe_99` | Enter data; Register. | Account created. |
| REG-P-06 | Positive | P2 | Password of minimum length with all character types | Password and confirm: `Abcdef1!` (8 characters) | Enter data; Register. | Account created. |
| REG-P-07 | Positive | P2 | Password of maximum length | Password and confirm: `Aa1!` followed by 60 lowercase letters (64 characters) | Enter data; Register. | Account created. |
| REG-P-08 | Positive | P3 | Email with leading/trailing spaces is trimmed | Email: `  jane.doe@example.com  ` | Enter data; Register. | Account created with email stored as `jane.doe@example.com` (REG-03). |
| REG-P-09 | Positive | P2 | Recover from an earlier failure | First attempt with password `weak`; then correct it to `Passw0rd!` in both fields | 1. Submit with weak password. 2. Observe error. 3. Correct both password fields. 4. Register. | Error shown first; other fields remain filled; second attempt succeeds and creates exactly one account. |
| REG-P-10 | Positive | P3 | Register using keyboard only | Valid set | Use Tab to move between fields, Space to tick Terms, Enter to submit. | Account created; focus order is logical. |
| REG-N-01 | Negative | P1 | All fields blank | All fields empty; Terms unticked | Click Register. | No account created; required-field message beside each of Email, Username, Password, Confirm password, and Terms; no technical error. |
| REG-N-02 | Negative | P1 | Email missing | Email empty | Enter other data; Register. | Rejected; "Email is required" beside Email; other values retained (not passwords). |
| REG-N-03 | Negative | P1 | Email without '@' | Email: `jane.doe.example.com` | Enter data; Register. | Rejected; format message beside Email; no account created. |
| REG-N-04 | Negative | P2 | Email without domain | Email: `jane.doe@` | Enter data; Register. | Rejected with format message. |
| REG-N-05 | Negative | P2 | Email with space inside | Email: `jane doe@example.com` | Enter data; Register. | Rejected with format message. |
| REG-N-06 | Negative | P2 | Email too long | Email: 250 letters followed by `@example.com` (total over 254) | Paste value; Register. | Rejected with length message; page layout intact; no crash. |
| REG-N-07 | Negative | P1 | Duplicate email | Email already registered: `jane.doe@example.com` (precondition: account exists) | Enter data; Register. | Rejected; "This email is already registered" beside Email; no second account created. |
| REG-N-08 | Negative | P2 | Duplicate email in different letter case | Email: `JANE.DOE@EXAMPLE.COM` (precondition: lower-case version exists) | Enter data; Register. | Rejected as duplicate (REG-03). |
| REG-N-09 | Negative | P2 | Username with special character | Username: `jane#1` | Enter data; Register. | Rejected; message that only letters, digits and underscores are allowed. |
| REG-N-10 | Negative | P2 | Username too short | Username: `abc` | Enter data; Register. | Rejected; message states minimum 4 characters. |
| REG-N-11 | Negative | P2 | Username too long | Username: 21 characters, `abcdefghij0123456789X` | Enter data; Register. | Rejected (or input prevented) with message about the 20-character maximum. |
| REG-N-12 | Negative | P2 | Username only spaces | Username: three spaces | Enter data; Register. | Rejected as required/invalid; not treated as a real value. |
| REG-N-13 | Negative | P1 | Duplicate username | Username `jane_doe` already exists | Enter data; Register. | Rejected; "Username is already taken" beside Username. |
| REG-N-14 | Negative | P1 | Password too short | Password and confirm: `Ab1!xyz` (7 characters) | Enter data; Register. | Rejected; message about minimum 8 characters beside Password. |
| REG-N-15 | Negative | P2 | Password too long | Password and confirm: 65 characters meeting all other rules | Enter data; Register. | Rejected with maximum-length message; no crash. |
| REG-N-16 | Negative | P1 | Password without uppercase | `passw0rd!` | Enter data; Register. | Rejected; message names missing uppercase. |
| REG-N-17 | Negative | P1 | Password without lowercase | `PASSW0RD!` | Enter data; Register. | Rejected; message names missing lowercase. |
| REG-N-18 | Negative | P1 | Password without digit | `Password!` | Enter data; Register. | Rejected; message names missing digit. |
| REG-N-19 | Negative | P1 | Password without special character | `Passw0rds` | Enter data; Register. | Rejected; message names missing special character. |
| REG-N-20 | Negative | P2 | Password containing a space | `Pass w0rd!` | Enter data; Register. | Rejected; message states spaces are not allowed. |
| REG-N-21 | Negative | P1 | Confirm password does not match | Password `Passw0rd!`; confirm `Passw0rd?` | Enter data; Register. | Rejected; "Passwords do not match" beside Confirm password; no account created. |
| REG-N-22 | Negative | P2 | Confirm password differs only by letter case | Password `Passw0rd!`; confirm `passw0rd!` | Enter data; Register. | Rejected; matching is case-sensitive. |
| REG-N-23 | Negative | P2 | Confirm password blank | Confirm empty | Enter data; Register. | Rejected; required message beside Confirm password. |
| REG-N-24 | Negative | P1 | Terms not accepted | Terms unticked; all else valid | Enter data; Register. | Rejected; message "You must accept the Terms and Conditions"; no account created. |
| REG-N-25 | Negative | P1 | Code-like text in username treated as plain data | Username: `x';DROP--` | Enter data; Register. | Treated as ordinary text: rejected by the character rule (REG-04) with the standard message; no technical or database error; no unusual behaviour; other accounts unaffected. |
| REG-N-26 | Negative | P2 | Markup-like text in email field | Email: `<b>jane</b>@example.com` | Enter data; Register. | Rejected as invalid format; text is not interpreted or displayed as formatted content. |
| REG-N-27 | Negative | P1 | Double-click on Register | Valid set | Double-click Register quickly. | Exactly one account is created; no duplicate-key error shown; no second confirmation (REG-11). |
| REG-N-28 | Negative | P2 | Network lost during submit | Valid set | Fill form; disconnect network; click Register; reconnect and retry. | Clear connection error shown; form data retained; no partial account; retry succeeds and creates one account. |
| REG-N-29 | Negative | P2 | Browser Back after successful registration, then resubmit | Valid set | Register successfully; press Back; click Register again. | No second account is created; message says email already registered, or form is reset. |
| REG-N-30 | Negative | P2 | Password masking and copy | Password `Passw0rd!` | Type password; try to copy from the field; inspect message after an error. | Characters shown as dots; copy from field yields nothing or masked text; password never shown in any message (REG-12). |
| REG-N-31 | Negative | P1 | Valid entries preserved after a validation failure | Username `jane_doe`; password too short | Enter data; Register. | Error appears; email and username remain filled; password fields cleared (REG-10). |

That is ten positive and thirty-one negative cases, which is typical: a form with many rules has many ways to break. Notice that no two cases test the same thing, each has exact data, and each expected result can be verified.

A few observations worth learning from this table:

- **Single-change principle.** In REG-N-14 only the password is wrong. If we had also changed the username, a failure could not be attributed to one rule.
- **Both sides of each rule.** Rule REG-06 has positives (P-06, P-07) and a negative for each sub-rule (N-14 to N-20).
- **A positive can be unusual.** REG-P-08 (spaces around the email) is valid *because* the requirement says spaces are trimmed. Always check the requirement.
- **Where the requirement is silent, ask.** If the requirements said nothing about the email-with-spaces case, the correct move would be to raise a question with the product owner, not to guess.

### Worked Example 2: Project 1 "Login"

#### Requirements

| Req ID | Requirement |
|---|---|
| LOG-01 | The login page has Email (or username), Password and a Login button, plus a "Remember me" checkbox. |
| LOG-02 | Both fields are required. |
| LOG-03 | Correct credentials log the user in and open the dashboard. |
| LOG-04 | Email is case-insensitive; password is case-sensitive. Leading and trailing spaces in the email are removed; spaces in the password are kept as typed. |
| LOG-05 | A failed login shows "Email or password is incorrect" and does not reveal which was wrong. |
| LOG-06 | After 5 consecutive failed attempts the account is locked for 15 minutes; a message says so. The counter resets after a successful login. |
| LOG-07 | The password field masks characters. |
| LOG-08 | Without "Remember me", the session ends after 30 minutes of inactivity and the user returns to login. With "Remember me", the session persists after closing and reopening the browser (up to 7 days). |
| LOG-09 | Logging out ends the session; protected pages cannot be reached afterwards, including with the browser Back button. |
| LOG-10 | Input is treated as plain data; no technical errors are ever shown. |

**Baseline data ("valid user")**: Email `jane.doe@example.com`, password `Passw0rd!`. Precondition for all cases unless noted: the account exists, is active and not locked; the user is on the login page, logged out.

#### Login test cases

| ID | Type | Pri | Title | Data | Steps | Expected result |
|---|---|---|---|---|---|---|
| LOG-P-01 | Positive | P1 | Valid login (happy path) | `jane.doe@example.com` / `Passw0rd!` | Enter credentials; click Login. | Logged in; dashboard opens showing the user's name (LOG-03). |
| LOG-P-02 | Positive | P2 | Login using the Enter key | Valid credentials | Type credentials; press Enter in the password field. | Logged in as in LOG-P-01. |
| LOG-P-03 | Positive | P2 | Email in different letter case | `JANE.DOE@EXAMPLE.COM` / `Passw0rd!` | Enter; Login. | Logged in (email is case-insensitive, LOG-04). |
| LOG-P-04 | Positive | P3 | Email with leading and trailing spaces | `  jane.doe@example.com  ` / `Passw0rd!` | Enter; Login. | Logged in (spaces trimmed, LOG-04). |
| LOG-P-05 | Positive | P2 | Remember me keeps session | Valid credentials; Remember me ticked | Login; close browser completely; reopen site. | User is still logged in; dashboard accessible (LOG-08). |
| LOG-P-06 | Positive | P2 | Successful login resets failed-attempt counter | 3 wrong passwords, then valid login, then 3 more wrong passwords | Perform in order; then try valid password. | Account is not locked after the second set of 3 failures; valid login still works (LOG-06). |
| LOG-P-07 | Positive | P2 | Logout ends session | Valid credentials | Login; click Logout. | Login page shown; session ended (LOG-09). |
| LOG-N-01 | Negative | P1 | Wrong password | `jane.doe@example.com` / `Wrong1234!` | Enter; Login. | Login refused; "Email or password is incorrect" shown; no session created; password field cleared (LOG-05). |
| LOG-N-02 | Negative | P1 | Unknown user | `nobody@example.com` / `Passw0rd!` | Enter; Login. | Identical message to LOG-N-01, so the response does not reveal that the account does not exist (LOG-05). |
| LOG-N-03 | Negative | P1 | Both fields blank | Empty / empty | Click Login. | Required messages beside both fields; no request treated as a login attempt; no crash (LOG-02). |
| LOG-N-04 | Negative | P1 | Email blank | Empty / `Passw0rd!` | Click Login. | "Email is required" beside Email. |
| LOG-N-05 | Negative | P1 | Password blank | `jane.doe@example.com` / empty | Click Login. | "Password is required" beside Password. |
| LOG-N-06 | Negative | P2 | Password in wrong letter case | `jane.doe@example.com` / `passw0rd!` | Enter; Login. | Refused with the standard message (password is case-sensitive, LOG-04). |
| LOG-N-07 | Negative | P2 | Password with trailing space | `jane.doe@example.com` / `Passw0rd! ` | Enter; Login. | Refused; spaces in the password are significant. |
| LOG-N-08 | Negative | P2 | Whitespace-only fields | Three spaces / three spaces | Enter; Login. | Treated as empty; required messages shown. |
| LOG-N-09 | Negative | P1 | Account locks after 5 failed attempts | Valid email with 5 wrong passwords in a row | Attempt wrong password five times; then attempt the correct password. | Lock message shown after the fifth failure; correct password is also refused while locked (LOG-06). |
| LOG-N-10 | Negative | P1 | Only four failures do not lock | 4 wrong passwords, then correct password | Attempt four wrong; then correct. | Login succeeds; account not locked. |
| LOG-N-11 | Negative | P2 | Locked account unlocks after 15 minutes | Locked account | Wait 15 minutes (or use a test tool to adjust time); log in with correct password. | Login succeeds after the lock period. |
| LOG-N-12 | Negative | P1 | Code-like string in password field | Email valid; password `' OR '1'='1` | Enter; Login. | Refused with the standard message; no database or technical error; treated as ordinary text (LOG-10). |
| LOG-N-13 | Negative | P1 | Code-like string in email field | Email `admin'--`; password `anything` | Enter; Login. | Refused (invalid credentials or format message); no technical error; no login. |
| LOG-N-14 | Negative | P2 | Markup-like text in email field | Email `<script>x</script>`; password `Passw0rd!` | Enter; Login. | Refused; text is not interpreted or displayed as formatted content on the page. |
| LOG-N-15 | Negative | P2 | Very long input | 5,000-character string in the email and password fields | Paste; Login. | Handled without crash, hang or layout break; refused with a message. |
| LOG-N-16 | Negative | P1 | Password is masked | Type `Passw0rd!` | Observe field; attempt to copy text from it. | Characters appear as dots; copying yields nothing readable (LOG-07). |
| LOG-N-17 | Negative | P3 | Paste into password field | Copy `Passw0rd!` from a text editor | Paste into field; Login. | Paste is accepted (or the product's stated policy applies); login succeeds with correct text; no extra spaces added. |
| LOG-N-18 | Negative | P1 | Session expires after 30 minutes inactivity | Logged in, Remember me unticked | Stay idle 30 minutes (or use a time-adjusting test tool); click any link. | User sent to login page with a "session expired" message; protected data not shown (LOG-08). |
| LOG-N-19 | Negative | P1 | Back button after logout | Logged in | Click Logout; press Back. | Login page or "please log in" shown; protected data not displayed (LOG-09). |
| LOG-N-20 | Negative | P1 | Direct address to protected page while logged out | Logged out | Type the dashboard address into the browser. | Redirected to login; dashboard content never shown. |
| LOG-N-21 | Negative | P2 | Double-click on Login | Valid credentials | Double-click Login. | One session; user reaches dashboard; no error. |
| LOG-N-22 | Negative | P2 | Wrong password counted across tabs | Two tabs, wrong password twice in each, then once more | Alternate attempts. | The fifth failure locks the account regardless of tab, because the count is per account. |
| LOG-N-23 | Negative | P2 | Network lost during login | Valid credentials | Disconnect network; click Login; reconnect. | Clear connection message; no session partially created; retry works. |
| LOG-N-24 | Negative | P3 | Error message reveals no sensitive data | Any failed login | Inspect all messages and page source visible to the user. | No stack traces, file paths, database terms or password values shown. |

That is seven positive and twenty-four negative cases. Notice the interplay of **states** (locked, logged out, session expired) with **inputs** (wrong password), which our method in section 7 predicted.

### Worked Example 3: Python demonstration of positive and negative tests

You do not need to be a programmer to understand this example, and we will explain every line. The idea is to show that positive and negative tests are the same two ideas expressed in code. We test a small function called `validate_password`, which follows the same rules as the registration page. (We will return to writing code properly in later weeks; today the goal is to see the two kinds of tests side by side.)

The code was run and verified before being added to this lesson. Save it as `password_checker.py`.

```python
"""A small password validator and plain-Python positive/negative tests."""

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{};:,.?"
MIN_LENGTH = 8
MAX_LENGTH = 64


def validate_password(password):
    """Return True if the password follows every rule, otherwise raise ValueError."""
    if not isinstance(password, str):
        raise TypeError("Password must be text")
    if password.strip() == "":
        raise ValueError("Password is required")
    if len(password) < MIN_LENGTH:
        raise ValueError("Password must be at least 8 characters")
    if len(password) > MAX_LENGTH:
        raise ValueError("Password must be at most 64 characters")
    if " " in password:
        raise ValueError("Password must not contain spaces")
    if not any(c.isupper() for c in password):
        raise ValueError("Password needs an uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password needs a lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password needs a digit")
    if not any(c in SPECIAL_CHARACTERS for c in password):
        raise ValueError("Password needs a special character")
    return True


def run_positive_test(test_id, password):
    try:
        result = validate_password(password)
    except Exception as error:
        print(f"{test_id} FAIL (positive): valid password rejected -> {error}")
        return False
    if result is True:
        print(f"{test_id} PASS (positive)")
        return True
    print(f"{test_id} FAIL (positive): expected True, got {result!r}")
    return False


def run_negative_test(test_id, password, expected_error, expected_message):
    try:
        validate_password(password)
    except expected_error as error:
        if expected_message in str(error):
            print(f"{test_id} PASS (negative): {error}")
            return True
        print(f"{test_id} FAIL (negative): wrong message -> {error}")
        return False
    except Exception as error:
        print(f"{test_id} FAIL (negative): unexpected {type(error).__name__}")
        return False
    print(f"{test_id} FAIL (negative): invalid password was accepted")
    return False


if __name__ == "__main__":
    results = [
        run_positive_test("PW-P01", "Passw0rd!"),
        run_positive_test("PW-P02", "Abcdefg1#"),
        run_positive_test("PW-P03", "A1!" + "a" * 61),
        run_positive_test("PW-P04", "Ab1!';DROP--"),
        run_negative_test("PW-N01", "", ValueError, "required"),
        run_negative_test("PW-N02", "        ", ValueError, "required"),
        run_negative_test("PW-N03", "Pa1!", ValueError, "at least 8"),
        run_negative_test("PW-N04", "A1!" + "a" * 62, ValueError, "at most 64"),
        run_negative_test("PW-N05", "passw0rd!", ValueError, "uppercase"),
        run_negative_test("PW-N06", "PASSW0RD!", ValueError, "lowercase"),
        run_negative_test("PW-N07", "Password!", ValueError, "digit"),
        run_negative_test("PW-N08", "Passw0rds", ValueError, "special"),
        run_negative_test("PW-N09", "Pass w0rd!", ValueError, "spaces"),
        run_negative_test("PW-N10", 12345678, TypeError, "text"),
    ]
    print(f"{sum(results)} of {len(results)} tests passed")
```

Run it with `python password_checker.py`. The output is:

```
PW-P01 PASS (positive)
PW-P02 PASS (positive)
PW-P03 PASS (positive)
PW-P04 PASS (positive)
PW-N01 PASS (negative): Password is required
PW-N02 PASS (negative): Password is required
PW-N03 PASS (negative): Password must be at least 8 characters
PW-N04 PASS (negative): Password must be at most 64 characters
PW-N05 PASS (negative): Password needs an uppercase letter
PW-N06 PASS (negative): Password needs a lowercase letter
PW-N07 PASS (negative): Password needs a digit
PW-N08 PASS (negative): Password needs a special character
PW-N09 PASS (negative): Password must not contain spaces
PW-N10 PASS (negative): Password must be text
14 of 14 tests passed
```

#### Explaining every line

**The top of the file**

- `"""A small password validator ..."""` is a **docstring**: a description of the file, written between triple quotes. Python ignores it when running; it is for humans.
- `SPECIAL_CHARACTERS = "..."` stores the list of characters we count as "special" in a **variable**, a named box holding a value. Capital letters are a convention for values that never change (constants).
- `MIN_LENGTH = 8` and `MAX_LENGTH = 64` store the length limits, so we do not repeat the numbers throughout the code.

**The function under test**

- `def validate_password(password):` defines a **function**, a reusable block of instructions, named `validate_password`, which receives one value called `password`.
- The triple-quoted line beneath it is a docstring explaining what the function does: it returns `True` if all rules pass, otherwise it **raises** an error. To "raise" an error means to stop and signal a problem.
- `if not isinstance(password, str):` checks whether the input is *not* text (`str` stands for string, Python's word for text). `isinstance` asks "is this value of that type?"
- `raise TypeError("Password must be text")` signals the problem if the value is not text, for example a number. `TypeError` is Python's standard error for the wrong kind of data. This handles our **invalid data type** category.
- `if password.strip() == "":` removes spaces from both ends (`strip`) and checks whether nothing is left. It catches both empty and whitespace-only input, covering the **empty/whitespace** category.
- `raise ValueError("Password is required")` signals a bad value. `ValueError` is Python's standard error for "right type, unacceptable value."
- `if len(password) < MIN_LENGTH:` checks whether the length (`len`) is below 8; the next line raises the matching error. This is the **too short** category.
- `if len(password) > MAX_LENGTH:` and its `raise` do the same for **too long**.
- `if " " in password:` checks whether a space appears anywhere in the password; the `raise` reports that spaces are not allowed.
- `if not any(c.isupper() for c in password):` looks at each character `c` in the password, asks whether it is uppercase (`isupper`), and `any(...)` answers "is at least one of them true?" With `not`, the line means "there is no uppercase letter." The following `raise` reports it.
- The lines using `islower()` and `isdigit()` do exactly the same for lowercase letters and digits.
- `if not any(c in SPECIAL_CHARACTERS for c in password):` checks whether at least one character appears in our special-character list, and raises an error if none does.
- `return True` runs only if no earlier check raised an error, meaning the password is valid. Because `raise` stops the function immediately, each check is only reached when all earlier checks passed.

**The positive test helper**

- `def run_positive_test(test_id, password):` defines a helper that takes a label (`test_id`) and a password that should be accepted.
- `try:` begins a protected block: "attempt this, and be ready for errors."
- `result = validate_password(password)` calls the function and stores what it returns.
- `except Exception as error:` runs if *any* error occurred. For a positive test, an error is a failure because a valid password must not be rejected.
- The `print(f"...")` line shows a FAIL message. The `f` before the quote lets us insert values in curly braces, such as `{test_id}` and `{error}`. `return False` reports "test failed" to the caller.
- `if result is True:` runs when no error occurred; we confirm the function returned exactly `True`, then print PASS and `return True`.
- The last two lines handle the unusual case that the function returned something else.

**The negative test helper**

- `def run_negative_test(test_id, password, expected_error, expected_message):` takes four things: a label, the invalid password, the *kind* of error we expect, and a piece of text that must appear in the message.
- `try:` then `validate_password(password)` attempts the call. In a negative test we hope an error occurs.
- `except expected_error as error:` catches only the expected kind of error. If it happens, we proceed to check the message.
- `if expected_message in str(error):` converts the error to text and checks that our expected snippet appears in it. If yes, print PASS and `return True`. If not, the right kind of error was raised but with the wrong message, which we report as FAIL. This reflects the "clear, correct error message" expectation from section 6.
- `except Exception as error:` catches any *other* kind of error. That is a failure because we got an unexpected problem instead of the planned rejection.
- The final two lines, after the `try` block, run only if **no error occurred at all**: the invalid password was accepted. That is exactly the defect negative tests exist to find, so we print FAIL and return `False`.

**The test list**

- `if __name__ == "__main__":` means "run the following only when this file is executed directly." It keeps the tests from running if the file is imported elsewhere.
- `results = [ ... ]` builds a list. Each entry calls a helper, which prints its result and returns `True` or `False`.
- `run_positive_test("PW-P01", "Passw0rd!")` is the happy path: a valid password.
- `PW-P02` is another valid shape; `PW-P03` uses `"A1!" + "a" * 61`, which builds a 64-character password (3 characters plus 61 repetitions of `a`), the longest allowed; `PW-P04` shows a code-like string (`Ab1!';DROP--`) that happens to satisfy every rule: it is accepted and treated as ordinary text. The function never tries to interpret it.
- `run_negative_test("PW-N01", "", ValueError, "required")` passes an empty password and expects a `ValueError` containing "required". The other negative lines follow the same pattern for whitespace only, too short (`Pa1!`), too long (65 characters), missing uppercase, lowercase, digit, special character, a space inside, and a number instead of text (which expects `TypeError`).
- `print(f"{sum(results)} of {len(results)} tests passed")` adds up the results (`True` counts as 1) and prints a summary.

#### The same tests in pytest style

**pytest** is the most widely used Python testing tool, and you will use it later in the programme. It lets you write tests as plain functions that use the word `assert` ("this must be true"). Install it with `pip install pytest`, and save the following as `test_password_checker.py` in the same folder:

```python
import pytest
from password_checker import validate_password


def test_valid_password_is_accepted():
    assert validate_password("Passw0rd!") is True


def test_too_short_password_is_rejected():
    with pytest.raises(ValueError, match="at least 8"):
        validate_password("Pa1!")


@pytest.mark.parametrize("bad_password, message", [
    ("passw0rd!", "uppercase"),
    ("PASSW0RD!", "lowercase"),
    ("Password!", "digit"),
    ("Passw0rds", "special"),
])
def test_each_missing_character_type_is_rejected(bad_password, message):
    with pytest.raises(ValueError, match=message):
        validate_password(bad_password)


def test_non_text_input_is_rejected():
    with pytest.raises(TypeError):
        validate_password(12345678)
```

Run it with `python -m pytest -v`. Output (abbreviated):

```
test_password_checker.py::test_valid_password_is_accepted PASSED
test_password_checker.py::test_too_short_password_is_rejected PASSED
test_password_checker.py::test_each_missing_character_type_is_rejected[passw0rd!-uppercase] PASSED
test_password_checker.py::test_each_missing_character_type_is_rejected[PASSW0RD!-lowercase] PASSED
test_password_checker.py::test_each_missing_character_type_is_rejected[Password!-digit] PASSED
test_password_checker.py::test_each_missing_character_type_is_rejected[Passw0rds-special] PASSED
test_password_checker.py::test_non_text_input_is_rejected PASSED

7 passed
```

Line by line:

- `import pytest` loads the testing tool so we can use its features.
- `from password_checker import validate_password` brings in the function under test from our first file.
- `def test_valid_password_is_accepted():` defines a test. pytest finds any function whose name starts with `test_`. The name is written as a sentence describing the behaviour.
- `assert validate_password("Passw0rd!") is True` is the positive test: the call must return `True`; otherwise the test fails.
- `def test_too_short_password_is_rejected():` begins a negative test.
- `with pytest.raises(ValueError, match="at least 8"):` says, "inside this block, a `ValueError` whose message matches 'at least 8' **must** occur." If no error occurs, or the wrong one occurs, the test fails. This is the pytest equivalent of our hand-written `run_negative_test` helper, and it is how negative expectations are written in real projects.
- `validate_password("Pa1!")` is the indented call inside that block.
- `@pytest.mark.parametrize("bad_password, message", [...])` is a **decorator** (a line placed above a function that changes how it works). It tells pytest to run the same test several times, once for each pair of values in the list, which avoids copy-pasting four near-identical tests.
- `def test_each_missing_character_type_is_rejected(bad_password, message):` receives the values from each pair.
- The `with pytest.raises(ValueError, match=message):` block and call then check each one.
- `def test_non_text_input_is_rejected():` and its `pytest.raises(TypeError)` block check the invalid-data-type case.
- The final result line, `7 passed`, counts four parametrized runs plus three single tests.

**Try breaking it.** An excellent learning exercise: edit `validate_password` and change `MIN_LENGTH = 8` to `MIN_LENGTH = 6`. Re-run the tests. The negative test for a 4-character password still passes, but if you add a negative test for a 7-character password, it will fail, because the faulty function now *accepts* an invalid password. That failure is what a tester "catches", and it demonstrates why you need negative tests designed around each rule.

---

## Classification Exercise

Decide whether each test idea below is **positive** or **negative**. Cover the answer key and try first. Use the rule from this lesson: positive means valid input/conditions and success expected; negative means invalid, unexpected or hostile input/conditions, where the correct behaviour is graceful handling.

1. Log in with correct email and correct password.
2. Log in with a correct email and an incorrect password.
3. Register with a 20-character username when 20 is the allowed maximum.
4. Register with a 21-character username when 20 is the allowed maximum.
5. Upload a `.png` image to a profile picture field that accepts `.png`.
6. Upload an `.exe` file to the profile picture field.
7. Enter `abc` in a field that expects a whole number.
8. Enter `7` in a field that accepts whole numbers 1 to 10.
9. Press "Pay now" twice quickly.
10. Press "Pay now" once and wait for the confirmation.
11. Open a members-only page without logging in.
12. Open the same members-only page after logging in as a member.
13. Enter a surname with an apostrophe (`O'Brien`) in a name field that allows apostrophes.
14. Enter `<b>hello</b>` in the name field and confirm it is shown as plain text, not formatted.
15. Leave the "Email" field blank on a form where it is required.
16. Fill in the optional "Middle name" field with a valid value.
17. Leave the optional "Middle name" field blank (the requirement says it is optional).
18. Click Back after logging out and check whether private pages are visible.
19. Disconnect the network while saving a profile.
20. Change the password using a valid current password and a valid new password.

#### Answer key

| # | Answer | Reason |
|---|---|---|
| 1 | Positive | Valid input, success expected. |
| 2 | Negative | Invalid password; rejection expected. |
| 3 | Positive | Maximum allowed length is valid. |
| 4 | Negative | One over the maximum is invalid. |
| 5 | Positive | Supported file type. |
| 6 | Negative | Unsupported file type. |
| 7 | Negative | Wrong data type. |
| 8 | Positive | Within the allowed range. |
| 9 | Negative | Unusual usage (double-submit); system must not duplicate the payment. |
| 10 | Positive | The normal, expected usage. |
| 11 | Negative | Unauthorised access attempt. |
| 12 | Positive | Authorised access, expected to succeed. |
| 13 | Positive | Valid in this field per the requirement. |
| 14 | Negative | Code-like (markup) text handled as plain data; an input-validation scenario. |
| 15 | Negative | Missing required field. |
| 16 | Positive | Valid optional input. |
| 17 | Positive | Leaving an optional field blank is valid; the form should succeed. This is an alternate path, not a negative test. |
| 18 | Negative | Browser-navigation scenario after logout. |
| 19 | Negative | Network interruption. |
| 20 | Positive | Valid inputs; success expected. |

If you answered 17 incorrectly, remember: blank is only negative when the field is required.

---

## Exercise: Change Password and Search Box

Write test cases for the two features below. Aim for at least six positive and ten negative cases for Change Password, and at least five positive and ten negative cases for Search Box. Use the standard fields (ID, type, priority, data, steps, expected result). Then compare with the sample answers. Your answers will differ; the sample is meant to show the depth and style expected, not to be the only correct set.

### Feature A: Change Password

Requirements:

- CP-01: The user must be logged in.
- CP-02: Fields: Current password, New password, Confirm new password. All are required.
- CP-03: Current password must match the existing password.
- CP-04: New password follows the registration rules (8 to 64 characters; upper, lower, digit, special; no spaces).
- CP-05: New password must be different from the current password.
- CP-06: Confirm must match New password exactly.
- CP-07: On success, the message "Password changed successfully" appears and the next login requires the new password; the old one no longer works.
- CP-08: On failure, the password is unchanged and messages appear beside the faulty fields.

Assume the user `jane.doe@example.com` currently has the password `Passw0rd!`.

#### Sample answers: Change Password

| ID | Type | Pri | Title | Data | Expected result |
|---|---|---|---|---|---|
| CPW-P-01 | Positive | P1 | Valid change (happy path) | Current `Passw0rd!`; new `N3wPass#word`; confirm same | Success message; password updated. |
| CPW-P-02 | Positive | P1 | Login with new password after change | As above, then log out and log in with `N3wPass#word` | Login succeeds. |
| CPW-P-03 | Positive | P1 | Old password stops working | After change, log in with `Passw0rd!` | Login refused with the standard message. |
| CPW-P-04 | Positive | P2 | New password of minimum length | New `Abcdef1!`; confirm same | Success. |
| CPW-P-05 | Positive | P2 | New password of maximum length | 64 valid characters | Success. |
| CPW-P-06 | Positive | P3 | Change twice in a row | Change to `N3wPass#word`, then to `An0ther#Pass` | Both succeed; only the latest works. |
| CPW-N-01 | Negative | P1 | Current password wrong | Current `Wrong123!`; valid new/confirm | Rejected; message beside Current password; password unchanged. |
| CPW-N-02 | Negative | P1 | All fields blank | Empty | Required messages beside each field. |
| CPW-N-03 | Negative | P2 | Current password blank | Only new/confirm filled | Required message beside Current password. |
| CPW-N-04 | Negative | P2 | New password blank | Current valid; new empty | Required message; unchanged. |
| CPW-N-05 | Negative | P1 | New password same as current | New `Passw0rd!` | Rejected with message that the new password must differ. |
| CPW-N-06 | Negative | P1 | Confirm does not match | New `N3wPass#word`; confirm `N3wPass#word1` | Rejected; message beside Confirm; unchanged. |
| CPW-N-07 | Negative | P1 | New password too short | New `Ab1!xyz` | Rejected with length message. |
| CPW-N-08 | Negative | P1 | New password has no special character | New `NewPassw0rd` | Rejected with message naming the rule. |
| CPW-N-09 | Negative | P2 | New password contains a space | New `New Pass1!x` | Rejected; spaces not allowed. |
| CPW-N-10 | Negative | P1 | Session expired before submit | Idle past 30 minutes, then submit valid data | Redirected to login; password unchanged; no data leaked. |
| CPW-N-11 | Negative | P1 | Logged-out access to the page | Open the change-password address while logged out | Redirected to login. |
| CPW-N-12 | Negative | P2 | Double-click Change | Valid data | Success once; no error from a second request; password set once. |
| CPW-N-13 | Negative | P2 | Network lost during change | Valid data, disconnect | Clear message; password unchanged or fully changed, never half-changed; retry possible. |
| CPW-N-14 | Negative | P2 | Code-like string as current password | Current `' OR '1'='1` | Treated as ordinary wrong text; standard rejection; no technical error. |
| CPW-N-15 | Negative | P2 | Fields masked, nothing revealed | Observe fields and messages | Dots shown; no password text appears in any message. |

### Feature B: Search Box

Requirements:

- SB-01: A single text box on the products page with a Search button.
- SB-02: Searching matches product names, ignoring letter case.
- SB-03: Search text is limited to 100 characters.
- SB-04: Leading and trailing spaces are ignored.
- SB-05: Results are displayed with the product name and price; if nothing matches, the message "No products found" is shown.
- SB-06: An empty search shows the message "Please enter a search term".
- SB-07: All search text is treated as plain text.

Assume products named "Laptop Pro", "Laptop Air" and "Wireless Mouse" exist.

#### Sample answers: Search Box

| ID | Type | Pri | Title | Data | Expected result |
|---|---|---|---|---|---|
| SRC-P-01 | Positive | P1 | Search for an existing product (happy path) | `Mouse` | "Wireless Mouse" listed with its price. |
| SRC-P-02 | Positive | P1 | Search matches several products | `Laptop` | Both laptops listed. |
| SRC-P-03 | Positive | P2 | Case-insensitive match | `lAPtop` | Both laptops listed. |
| SRC-P-04 | Positive | P2 | Spaces around term ignored | `  Mouse  ` | "Wireless Mouse" listed. |
| SRC-P-05 | Positive | P2 | Search via the Enter key | `Mouse`, press Enter | Same results as clicking Search. |
| SRC-P-06 | Positive | P3 | Search term of maximum length | 100-character term | No crash; "No products found" shown. |
| SRC-N-01 | Negative | P1 | Empty search | Empty | "Please enter a search term"; no results list. |
| SRC-N-02 | Negative | P2 | Whitespace-only search | Three spaces | Same message as empty search. |
| SRC-N-03 | Negative | P1 | No matching product | `Banana` | "No products found"; no error page. |
| SRC-N-04 | Negative | P2 | Search too long | 101 characters | Input limited or rejected with a message; no crash. |
| SRC-N-05 | Negative | P1 | Code-like database text | `x'; DROP TABLE products;--` | Treated as plain text; "No products found"; no technical error; product list unaffected afterwards. |
| SRC-N-06 | Negative | P1 | Markup-like text | `<script>alert(1)</script>` | Shown, if at all, as plain text; no pop-up or page change; "No products found". |
| SRC-N-07 | Negative | P2 | Special characters | `%`, `_`, `*`, `\` one at a time | No crash; sensible result (no match, or a defined behaviour); never "all products" unless specified. |
| SRC-N-08 | Negative | P3 | Emoji and non-Latin text | `🙂`, `ノートパソコン` | No crash; "No products found" or valid match; characters displayed correctly. |
| SRC-N-09 | Negative | P3 | Only digits or symbols | `12345`, `!!!` | "No products found"; no error. |
| SRC-N-10 | Negative | P2 | Double-click Search | `Laptop` | One set of results; no duplicates. |
| SRC-N-11 | Negative | P2 | Browser Back after search | Search, open a product, press Back | Previous search and results still shown; no error. |
| SRC-N-12 | Negative | P2 | Network lost during search | `Laptop`, disconnect | Clear message; page remains usable; retry works. |

Compare your own list with the samples. Did you cover every requirement at least once? Did every negative case have specific data and a specific expected result?

---

## Common Mistakes

**1. Testing only the happy path.** The most common mistake. A suite with only valid-input tests will pass on a product that falls apart the moment a real user makes a typo. *Fix:* for every rule, write at least one negative case, and use the category table in section 5 as a prompt.

**2. Vague expected results.** "Error is shown" or "It should not work" cannot be checked objectively. *Fix:* state the message, location, state of the system and what must *not* happen.

**3. Unrealistic negative data.** Typing random keyboard mashing or absurd values that no real situation could create (a ten-million-character string in a field with no reason to ever hold one) may waste time. Choose negative data that real users, real networks or real attackers could plausibly produce: common typos, copy-and-paste with spaces, missing `@`, an old session, a double-click. *Fix:* ask "How could this input really arrive?" Conversely, do not be so cautious that you skip realistic extremes such as an over-long paste.

**4. Changing too many things at once.** If a test enters five invalid values together, a failure cannot be traced. *Fix:* change one thing at a time; combine only in deliberate multi-field tests.

**5. Confusing the type with the result.** Believing a "negative test" is one that fails. *Fix:* remember, negative describes the *input*; pass/fail describes the *outcome*.

**6. Treating all unusual input as negative.** Maximum-length usernames, apostrophes in surnames and blank optional fields are valid. *Fix:* check the requirement.

**7. Ignoring the system state and environment.** Locked accounts, expired sessions, lost connections and double-clicks are negative scenarios that no field-level test finds. *Fix:* list states in step 3 of the method.

**8. Testing against assumptions rather than requirements.** If you do not know whether spaces should be trimmed, ask. Guessing creates false failures or false passes.

**9. Trying to "exploit" findings.** When you see a hint of a serious security issue, report it and stop. Do not attempt to access data you are not authorised to see, and never run security tests on systems you have no permission to test.

**10. Forgetting to clean up.** Negative tests that create accounts or lock users can break later tests. *Fix:* note the data created, reset states, and use fresh data where needed.

---

## Relationship to Later Techniques

Today you chose test data by common sense and by the category list. Tomorrow you will learn formal techniques that answer the question "which exact values should I choose?" in a systematic way.

- **Equivalence Partitioning (EP)** groups input values into classes that the system should treat the same way, so you can test one representative from each class instead of every value. It tells you how to pick, for example, one valid and a few invalid representatives for a field.
- **Boundary Value Analysis (BVA)** focuses on the values at the edges of those classes, where defects often hide. It explains why we tested usernames of exactly 4, 3, 20 and 21 characters.
- **Error Guessing** uses your experience and intuition about where defects usually occur to design extra tests. The negative-test category list in this lesson is an early, informal version of that.

Do not worry about the details yet. Today's skills (identifying rules, writing a positive and a negative for each, and thinking about expected results) are the foundation on which Thursday's techniques are built. Those techniques are formal ways to choose the data for the positive and negative cases you are already learning to write.

---

## Checklist: Negative Testing for Forms

Copy this checklist into your notes and use it whenever you test a form. Tick each item as you test it, and add a test case or a note for any that apply.

**Required and empty values**
- [ ] Each required field left empty, one at a time
- [ ] All fields empty
- [ ] Fields containing only spaces
- [ ] Optional fields left empty (this should succeed; check)
- [ ] Leading and trailing spaces around values

**Length**
- [ ] Shorter than the minimum length
- [ ] Longer than the maximum length
- [ ] Very long pasted text (layout, speed, errors)

**Type, format and range**
- [ ] Wrong data type (letters in numeric fields, and so on)
- [ ] Wrong format (email, phone, date, postal code)
- [ ] Impossible values (31 February, month 13)
- [ ] Values below and above the allowed range; zero and negative numbers
- [ ] Start date after end date

**Characters**
- [ ] Special characters and symbols
- [ ] Accented letters, non-Latin scripts and emoji
- [ ] Code-like and markup-like text handled as plain data, with no technical errors

**Uniqueness and relationships**
- [ ] Duplicate values for unique fields (including different letter case)
- [ ] Dependent fields that must match (password and confirmation)
- [ ] Mandatory checkboxes left unticked

**Messages and behaviour**
- [ ] Message is clear, specific and placed beside the faulty field
- [ ] Valid entries are preserved after a failure (except passwords)
- [ ] No technical details, file paths or passwords in any message
- [ ] No partial record created; system state unchanged
- [ ] Focus moves to the first invalid field (accessibility)

**Usage and environment**
- [ ] Double-click or double-submit
- [ ] Pressing Enter versus clicking the button
- [ ] Browser Back, Forward and Refresh after submit
- [ ] Same form open in two tabs
- [ ] Network lost or slow during submit
- [ ] Session expired before submit
- [ ] Access to the form (or its result page) while logged out or without permission

**Files (if the form has an upload)**
- [ ] Unsupported file type; renamed file with wrong extension
- [ ] Empty file; oversized file
- [ ] Unusual file names (very long, special characters)

**Security hygiene**
- [ ] Passwords masked and never echoed in messages
- [ ] Error messages do not reveal whether an account exists
- [ ] Anything suspicious reported immediately through the proper channel

---

## Try It: Your Turn on Project 1 Login

This is a preview of the exercise you will complete this afternoon.

**Task:** Open the Project 1 login page (or use the Login requirements in Worked Example 2 if the application is not yet available). Write **10 positive** and **10 negative** test cases for the login feature.

**Rules:**

1. Use the standard fields: ID, title, type, priority, preconditions, test data, steps, expected result.
2. Do not copy the examples above. Create your own and use different data where you can.
3. Use the ID pattern `LOGIN-P-01` to `LOGIN-P-10` and `LOGIN-N-01` to `LOGIN-N-10`.
4. Make sure your negative cases come from at least **eight different categories** in section 5.
5. Every expected result for a negative case must mention at least three of: message, no crash, no data loss, no sensitive information, state unchanged, logging.
6. Record the requirement each test traces back to. If you find a requirement is unclear, write a question for the product owner next to it.

**Steps:**

1. Read the requirements and list inputs, rules and states.
2. For each rule, write one positive and at least one negative.
3. Add scenario-level cases (session, back button, double-click, network).
4. Check coverage: is every rule covered? Is every category considered?
5. Assign priorities and sort so P1 cases run first.
6. Swap lists with a classmate and review each other's work. Ask: "Could I run this test without asking questions?"

**Stretch goal:** run the tests you wrote against the Project 1 application, record actual results, and log any failure with a full defect report.

---

## Knowledge Check

Answer in your own words first, then compare with the answers.

**Questions**

1. In one sentence each, define positive testing and negative testing.
2. A tester enters a wrong password and the system correctly refuses the login. Is the test positive or negative? Did it pass or fail?
3. What is the difference between an alternate path and an exception path?
4. Give four reasons negative testing matters.
5. Name six categories of negative tests and give an example for each.
6. A login failure message says, "Password incorrect for jane.doe@example.com." What is wrong with this message from a security point of view?
7. List five things to consider when writing the expected result of a negative test.
8. Describe the method for deriving positive and negative cases from requirements.
9. Why is "Enter an invalid email" a poor piece of test data?
10. What is the right answer when someone asks, "What percentage of my tests should be negative?"
11. A form field is optional and a tester leaves it blank. Positive or negative?
12. When a tester sees a database error after entering code-like text in a form, what should they do?
13. In the Python demonstration, what does `with pytest.raises(ValueError, match="at least 8")` mean?
14. In `run_negative_test`, what is the meaning of the final `print` and `return False` that appear after the `try` block?
15. Which Thursday techniques help you choose precise test data, and what does each do?

**Answers**

1. Positive testing verifies that the system works as intended with valid input and expected usage. Negative testing verifies that the system handles invalid, unexpected or malicious input and conditions gracefully.
2. The test is negative (the input is invalid). It passed, because the system behaved correctly by refusing the login.
3. An alternate path is a different but valid route to success (a positive test). An exception path is a route where something goes wrong (a negative test).
4. Any four of: security; clear, safe error messages; data integrity; reliability and robustness with real users; protecting reputation; lower cost of finding defects early.
5. Any six of: invalid data type (letters in a number field); empty/whitespace (spaces-only username); too long/short (one-character username); special characters (`#` in username); wrong format (email missing `@`); out-of-range (age `-5`); duplicate data (existing email); missing required field; wrong order of steps; expired session; unauthorised access; network interruption; double-submit; browser Back; unsupported file type.
6. It reveals that the account exists and that the password was the problem, which helps an attacker discover valid accounts. The correct message is generic: "Email or password is incorrect."
7. Any five of: clear message; no crash; no data loss; no sensitive information leaked; message beside the specific field; system state unchanged; logging of the event.
8. List the inputs, rules and states. For each rule write one positive and at least one negative case. Add scenario-level cases, then review for duplicates, priorities and traceability.
9. It is not specific. Two testers would choose different values, and the result cannot be repeated or compared. Use an exact value, such as `jane.example.com`.
10. There is no correct fixed percentage; it depends on risk. Higher-risk features (security, money, personal data) need more negative tests. A better measure is whether each rule has at least one positive and one negative case.
11. Positive. Leaving an optional field blank is valid input; success is expected.
12. Stop trying to exploit it, capture evidence (screenshot, exact input and steps), report it immediately as a high-severity defect through the proper channel, and follow the organisation's security process.
13. It states that the code inside the block must raise a `ValueError` whose message contains "at least 8". If no error, or a different error or message, appears, the test fails.
14. They run only if no error was raised at all, meaning the invalid password was accepted. That is a defect, so the test reports FAIL and returns `False`.
15. Equivalence Partitioning groups inputs into classes treated the same way so one representative from each class can be tested. Boundary Value Analysis tests values at the edges of those classes. (Error Guessing, also on Thursday, uses experience to guess where defects hide.)

---

## Key Takeaways

- **Positive testing** checks that the product works with valid input; **negative testing** checks that it fails safely with invalid, unexpected or hostile input.
- "Positive" and "negative" describe the **test input and scenario**, not whether the test passed.
- You need both: positive tests build **confidence**; negative tests build **robustness**, protect **security**, improve **error messages** and preserve **data integrity**.
- Features have a **happy path**, **alternate paths** (valid but different) and **exception paths** (something goes wrong).
- There are many ways to go wrong, but they fall into about sixteen **categories**; use the category list as a prompt for every feature.
- A strong negative **expected result** includes a clear message, no crash, no data loss, no sensitive leak, field-level validation, unchanged state and (where required) logging.
- Derive cases methodically: **list inputs, rules and states; for each rule write one positive and at least one negative**; then add scenario-level cases.
- Write test cases with **exact data**, **numbered steps**, **specific expected results**, sensible **IDs** and **priorities**, and traceability to requirements.
- The positive-to-negative ratio **depends on risk**; there is no magic number.
- Code-like input should be treated as **plain data**, and anything suspicious should be reported, not exploited.
- Equivalence Partitioning, Boundary Value Analysis and Error Guessing (Thursday) are formal ways to choose better data for the cases you write today.
- Automated tests, such as the pytest examples, are positive and negative checks written in code.

---

## Additional Resources

- **Guru99 - Positive Testing vs Negative Testing:** a beginner-friendly comparison with examples. https://www.guru99.com/positive-testing-vs-negative-testing.html
- **OWASP Cheat Sheet Series - Input Validation Cheat Sheet:** an authoritative overview of how applications should validate input, useful for understanding what negative tests are checking. https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- **Ministry of Testing:** a community with articles, courses and discussions on testing practice. https://www.ministryoftesting.com/
- **pytest documentation:** the official guide to `pytest.raises` and parametrized tests used in this lesson. https://docs.pytest.org/
