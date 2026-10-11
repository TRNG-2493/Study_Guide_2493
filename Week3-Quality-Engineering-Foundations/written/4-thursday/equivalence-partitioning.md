# Equivalence Partitioning

## Learning Objectives

By the end of this lesson, you will be able to:

- Explain the core idea of Equivalence Partitioning (EP) and why testing one representative value per partition gives good coverage with far fewer tests.
- Connect EP to the testing principle "exhaustive testing is impossible" that you learned on Wednesday.
- Define and correctly use the terms equivalence class, valid partition, invalid partition, and representative value.
- Describe the assumption behind EP and recognize situations where that assumption can fail.
- Apply the six-step EP procedure: identify inputs, identify rules, partition into valid and invalid classes, pick representatives, create test cases, and define expected results.
- Use partitioning heuristics for ranges, sets, booleans, specific values, formats, lengths, character classes, file types, and multiple fields.
- Build complete EP test tables for an age field, a grade mapping, a shipping-cost rule, password rules, a user-type dropdown, and email formats.
- Combine partitions across several fields without causing a "cartesian-product explosion", and explain why invalid inputs must be tested one at a time.
- Calculate EP coverage using the formula (partitions covered / total partitions) x 100.
- Combine EP with Boundary Value Analysis (BVA) and compare the number of tests needed by each approach.
- Read and run a small Python program whose tests are chosen by EP.
- Apply EP to the Project 1 registration form and avoid the most common EP mistakes.

---

## Why This Matters

Imagine you are asked to test an "Age" field on the Project 1 registration form. The field accepts ages from 18 to 60. How many different things could a user type into that box?

Whole numbers alone give you hundreds of possibilities. Add negative numbers, decimals, letters, symbols, emojis, pasted text, empty input, and spaces, and the number of possible inputs becomes effectively infinite. You cannot test them all. On Wednesday you learned this as a testing principle: exhaustive testing is impossible.

So what do professional testers do? They do not give up, and they do not pick random values and hope for the best. They use test design techniques: systematic, repeatable methods for choosing a small set of test cases that still has a high chance of finding defects. Equivalence Partitioning is one of the most important and most widely used of these techniques. It is one of the first things tested in the ISTQB Foundation Level exam, and it is used every day by working testers at companies of every size.

Here is why EP matters to you as a future AI enabled Test Automation Engineer:

- It saves time. A well-partitioned field might need 6 tests instead of 600.
- It gives you a defensible answer when someone asks, "How do you know you tested enough?" You can point to a list of partitions and show that each one was covered.
- It makes your test cases easier to review. A teammate can look at your partition table and immediately spot a missing class.
- It is the foundation of data-driven automation. When you automate tests later in this program, you will feed representative values from EP tables into parametrized tests.
- It pairs naturally with Boundary Value Analysis, which you just learned. Together, EP and BVA form the most common one-two punch in black-box test design.

Today's pair-programming exercise asks you to design tests for Project 1 with three techniques. EP is one of them, so the habits you build in this lesson will be used right away.

---

## The Concept

### The Core Idea in Plain Language

Equivalence Partitioning is a black-box test design technique. Remember that "black-box" means we design tests from the outside, based on requirements and expected behavior, without looking at the code.

The idea has two parts:

1. **Divide** all possible inputs into groups (called partitions or equivalence classes) so that every input in the same group should be treated the same way by the system.
2. **Test** just one representative value from each group, because if the system handles one member of the group correctly, it is reasonable to expect it handles the others the same way.

That is the whole technique. Everything else in this lesson is about doing those two steps carefully.

### Analogy 1: Tasting One Spoon of Soup

You are cooking a big pot of soup and want to know if it needs salt. Do you eat the whole pot? Of course not. You stir it, taste one spoonful, and decide. You trust that every spoonful of a well-stirred pot tastes about the same.

EP works the same way. The pot is the huge set of possible inputs. A spoonful is one representative value. You are betting, reasonably, that the soup is uniform.

But notice what makes this work: you stirred. If the pot has a layer of salt at the bottom and plain broth at the top, one spoonful will mislead you. In testing, "stirring" is the careful work of forming partitions correctly so that each really does behave uniformly. Good partitioning is the stirring.

### Analogy 2: Sorting Fruit Baskets

Suppose a delivery truck brings 10,000 pieces of fruit and you must check quality. You do not inspect every piece. First you sort them into baskets: apples, oranges, bananas, and "not fruit at all" (a stray rock, a plastic toy). Then you inspect one or two pieces from each basket.

- Each basket is an equivalence class.
- The apple basket, orange basket, and banana basket are "valid" baskets.
- The rock-and-toy basket is an "invalid" basket. You still check it, because you want to know what happens when something unexpected arrives.
- The piece you pull out of each basket is the representative value.

Notice that you would never skip the invalid basket. Many serious bugs hide in how a system reacts to things it was never meant to receive.

### The Link to "Exhaustive Testing Is Impossible"

On Wednesday you learned seven testing principles. One of them said that testing everything (all combinations of inputs and preconditions) is not feasible except for trivial cases. Instead of exhaustive testing, we use risk and priorities to focus our effort.

EP is the practical answer to that principle. It does not pretend you can test everything. It gives you a rigorous way to decide what to test instead. The reasoning chain is:

1. Exhaustive testing is impossible.
2. Therefore, we must select a small number of inputs.
3. We want the selection to be systematic, not random.
4. EP provides that structure by grouping inputs that should behave the same and sampling each group.

A quick numerical picture. Suppose an age field accepts whole numbers from 0 to 120. Testing every legitimate number means 121 tests, before we even consider text or decimals. With EP we reduce this to a handful of tests. The savings grow dramatically when you have many fields.

### Key Definitions

Let us define every term precisely. These are the words that will appear in your test documentation and in conversations with other testers.

- **Equivalence class (or equivalence partition):** A group of input values that the system is expected to process in the same way. If one value in the class exposes a defect, we expect the other values in the class to expose it too. If one passes, we expect the others to pass.
- **Valid partition (valid equivalence class):** A class of inputs that the system should accept and process normally. For an age field of 18 to 60, the valid partition is "whole numbers from 18 to 60".
- **Invalid partition (invalid equivalence class):** A class of inputs that the system should reject, or handle with an error message or a defined fallback. For the age field, examples are "numbers below 18", "numbers above 60", "text", "empty", and "decimals".
- **Representative value:** The single value you pick from a partition to stand in for the whole class. For the valid age partition, 35 is a good representative.
- **Test condition:** Something about the system that can be tested. In EP, each partition is a test condition.
- **Expected result:** What the system should do with the input, as defined by the requirement. You decide this before you run the test, never after.

A small but important point: "valid" and "invalid" are about whether the input is acceptable according to the requirement, not about whether the input is good or bad in some other sense. A negative age is an invalid input. Testing it is a valuable test, not a wasted one.

### The Assumption Behind EP, and When It Can Fail

Every technique rests on an assumption. EP's assumption is:

> All values in the same partition are processed by the system in the same way, so testing one representative is as good as testing any other value from that partition.

This is called the **equivalence assumption**. It is not a law of nature. It is an assumption about how the software is likely to be built. When it is true, EP is powerful. When it is false, EP can miss defects.

Situations where the assumption can fail:

1. **The partitions were drawn wrongly.** If you put 12 and 13 in the same "child" group but the rule actually changes at 13, one group hides two behaviors. This is the most common cause of failure, and it comes from misreading or not fully understanding the requirement.
2. **The code has hidden special cases.** A developer might write special handling for one value, such as age 42 or the username "admin". Black-box testing cannot see this. It is one reason we also use error guessing and experience-based techniques (coming up later today).
3. **Boundary mistakes.** Developers frequently make off-by-one errors, writing less-than where they meant less-than-or-equal. A representative from the middle of a partition will not reveal this. That is exactly why Boundary Value Analysis exists, and why we use both techniques together.
4. **Interactions between fields.** Two fields that are each fine alone may behave badly together. EP applied to one field at a time does not see that.
5. **State and history.** The same input may behave differently depending on what happened before, such as whether a user is already logged in or an email is already registered.

The lesson is not "EP is unreliable". The lesson is "EP is a strong tool whose assumption you must keep in mind, and which you should complement with other techniques".

### The Six-Step EP Procedure

Follow these steps every time. With practice they become automatic.

**Step 1: Identify the inputs.** List every field, parameter, or condition that a user or another system can supply. For a registration form: username, email, age, password, country, terms checkbox.

**Step 2: Identify the rules for each input.** Read the requirement, user story, or acceptance criteria and write down what is allowed and what is not. Ranges, allowed characters, lengths, required or optional, formats. If the requirement is vague, ask questions now. Unclear rules lead to wrong partitions.

**Step 3: Partition the inputs into valid and invalid classes.** For each input, divide the possible values into non-overlapping groups where behavior should be uniform. Make sure the groups together cover everything: every possible input must belong to exactly one partition. Label each partition clearly.

**Step 4: Pick a representative from each partition.** Choose any value inside the partition. Prefer values that are easy to read and verify, such as 35 for the age field. Avoid picking a boundary value just to be "safe" unless you are deliberately combining EP with BVA.

**Step 5: Create test cases.** Turn each representative into a test case with an ID, a clear description, the input data, and preconditions if needed. For single-field tests, keep other fields at known good values so that only one thing varies.

**Step 6: Define the expected results.** For every test case, write down exactly what should happen: accepted, rejected, which error message, which output, which price. Write expected results from the requirement, not from what the system currently does.

A handy mnemonic: **I-R-P-R-T-E** (Inputs, Rules, Partitions, Representatives, Tests, Expected results). You do not need the mnemonic. You need the habit.

### Visualizing a Partition: the Number Line

For numeric ranges, a number line makes the idea easy to see. Here is the Project 1 age field, valid from 18 to 60:

```
 Invalid                    Valid                      Invalid
 (too young)             (18 to 60)                  (too old)
<-----------------|------------------------|------------------->
 ... 15 16 17     |  18 ....... 35 ....... 60  |   61 62 63 ...
                  ^                        ^
              lowest valid            highest valid

 Partition 1:  age < 18         representative: 15
 Partition 2:  18 <= age <= 60  representative: 35
 Partition 3:  age > 60         representative: 70
```

Every whole number belongs to exactly one of the three partitions. We then add the non-number cases:

```
 All possible inputs to the Age field
 +--------------------------------------------------------------+
 |  Numbers                                                     |
 |  +----------+  +------------------+  +----------+            |
 |  | age < 18 |  | 18 <= age <= 60  |  | age > 60 |            |
 |  | INVALID  |  |      VALID       |  | INVALID  |            |
 |  +----------+  +------------------+  +----------+            |
 |                                                              |
 |  Not whole numbers                                           |
 |  +----------+  +-------------+  +----------------+           |
 |  | Text and |  |   Empty     |  |    Decimal     |           |
 |  | symbols  |  |   INVALID   |  |    INVALID     |           |
 |  | INVALID  |  |             |  |                |           |
 |  +----------+  +-------------+  +----------------+           |
 +--------------------------------------------------------------+
```

Six partitions, one valid and five invalid. We will test each with one value.

---

## Partitioning Rules and Heuristics

Different kinds of input suggest different ways of partitioning. These rules of thumb will carry you through most real situations. Treat them as a checklist you can run against any field.

### Rule 1: Ranges

When an input accepts a range of values (such as 18 to 60):

- Create **one valid partition** for the values inside the range.
- Create **two invalid partitions**: below the range and above the range.
- Add invalid partitions for values of the wrong type (text, decimal, empty) if the field is numeric.

```
   below range     |     in range     |    above range
      INVALID      |      VALID       |      INVALID
```

If the range is "open" at one end (for example, "at least 18" with no maximum), you only have one invalid numeric partition, the values below 18.

### Rule 2: Sets and Enumerations

When an input comes from a defined list (a country dropdown, user roles, payment methods):

- Create **one valid partition per member** when each member triggers different behavior. For user roles Guest, Member, and Admin, each role sees different screens and permissions, so each is its own partition.
- Create **one shared valid partition** when all members are processed identically. If a country dropdown only stores the name and nothing else depends on it, "any listed country" can be one partition.
- Create **one invalid partition** for "a value not in the set" (this can occur if someone tampers with the request).
- Consider **"nothing selected"** or a placeholder such as "Select a country" as another invalid partition.

### Rule 3: Booleans and Checkboxes

A true or false input has exactly two partitions: true (checked) and false (unchecked). Whether each is valid or invalid depends on the requirement. For a "I accept the Terms and Conditions" checkbox on registration, checked is valid and unchecked is invalid (registration is blocked). For an optional "Subscribe to newsletter" checkbox, both are valid, with different outcomes.

### Rule 4: Specific Values and "Must Be Exactly"

When the requirement says an input must be a specific value (for example, a confirmation box where the user must type the word DELETE), you have **one valid partition** (exactly that value) and **one invalid partition** (anything else). You may refine the invalid class: wrong case ("delete"), extra spaces, partial match ("DELET"), and empty.

### Rule 5: Formats (Email, Phone, Date)

When an input must follow a pattern:

- One valid partition for each meaningfully different valid format. For email, a simple address and an address with a subdomain or plus sign may be handled by different parts of the validation logic.
- One invalid partition for each distinct way the format can be broken: missing a required symbol, symbol in the wrong place, repeated symbol, illegal character, missing section.
- An invalid partition for empty.

For a phone number requirement of "10 digits, numbers only": valid is exactly 10 digits; invalid classes are fewer than 10 digits, more than 10 digits, containing letters, containing symbols such as dashes (if not permitted), and empty.

For a date in the format DD/MM/YYYY: valid is a real calendar date in the right format; invalid classes include wrong format (2024-05-10), impossible day (45/01/2024), impossible month (10/15/2024), a date that does not exist (30/02/2024), and non-date text.

### Rule 6: Lengths

When a rule restricts length (for example, 8 to 20 characters), treat length as its own dimension:

- Too short, valid length, too long, and empty.

Length partitions are numeric ranges applied to the count of characters, so they follow Rule 1.

### Rule 7: String Character Classes

When a rule restricts which characters are allowed, partition by character class:

- Uppercase letters, lowercase letters, digits, special characters (such as !, @, #), spaces, and other (accented letters, emojis, non-Latin scripts).
- For each rule such as "must contain a digit", create one invalid partition where that class is missing.

The key discipline is to **isolate the rule**. When you test "no digit", make sure everything else in that value is valid (right length, has uppercase, and so on) so that the only reason for rejection is the missing digit. We will see this in the password example.

### Rule 8: File Types and Sizes

For an upload feature:

- Each permitted file type (for example, JPG, PNG) is a valid partition when handling differs; otherwise "permitted image types" may be one.
- Not permitted types (PDF, EXE, GIF if not allowed) are invalid partitions.
- Size is a separate dimension: within limit, above limit, and zero bytes.
- "No file selected" is another invalid partition.
- A file with a permitted extension but wrong content (an EXE renamed to .jpg) is a valuable negative partition.

### Rule 9: Multiple Fields

When a form has many fields, apply EP to each field first, then decide how to combine the partitions. This is covered in its own section below, because blindly combining everything leads to an explosion in the number of tests.

### Rule 10: Do Not Forget Empty and Null

For almost every field, "empty" (nothing entered), "only spaces", and sometimes "null" (no value supplied at all, relevant for APIs) are separate partitions with their own behavior. Beginners often forget them. Make "empty" part of your checklist.

### Quick Reference Table

| Input type | Valid partitions | Invalid partitions to consider |
|---|---|---|
| Numeric range | Inside range | Below, above, text, decimal, empty |
| Set / list | Each member (or shared class) | Not in set, nothing selected |
| Boolean | Depends on requirement | Depends on requirement |
| Specific value | Exactly that value | Anything else, wrong case, empty |
| Format | Each valid format | Each way to break the format, empty |
| Length | Within allowed length | Too short, too long, empty |
| Character classes | Allowed classes | Each missing or forbidden class |
| File | Permitted types within size | Wrong type, too big, zero bytes, none |

---

## Worked Examples

### Example 1: Age Field (18 to 60)

**Requirement:** The Age field accepts whole numbers from 18 to 60 inclusive. Any other input is rejected with the message "Please enter a valid age between 18 and 60."

**Step 1: Inputs.** One input: Age.

**Step 2: Rules.** Whole numbers only; minimum 18; maximum 60; required.

**Step 3: Partitions.**

| ID | Partition | Type |
|---|---|---|
| P1 | Whole numbers less than 18 | Invalid |
| P2 | Whole numbers from 18 to 60 | Valid |
| P3 | Whole numbers greater than 60 | Invalid |
| P4 | Non-numeric (letters, symbols) | Invalid |
| P5 | Empty | Invalid |
| P6 | Decimal numbers | Invalid |

**Steps 4 to 6: Representatives, test cases, expected results.**

| Test ID | Partition | Representative value | Valid / Invalid | Expected result |
|---|---|---|---|---|
| TC-AGE-01 | P1: below 18 | 15 | Invalid | Rejected; error "Please enter a valid age between 18 and 60." |
| TC-AGE-02 | P2: 18 to 60 | 35 | Valid | Accepted; no error; form proceeds |
| TC-AGE-03 | P3: above 60 | 70 | Invalid | Rejected; same error message |
| TC-AGE-04 | P4: non-numeric | abc | Invalid | Rejected; error shown (or letters blocked from entry) |
| TC-AGE-05 | P5: empty | (leave blank) | Invalid | Rejected; "Age is required" or the standard age error |
| TC-AGE-06 | P6: decimal | 25.5 | Invalid | Rejected; error shown |

Six tests give us coverage of every partition. Compared with testing the 121 whole numbers from 0 to 120 plus endless text, this is an enormous saving.

Notice what we did not do: we did not pick 18 or 60 as the representative of the valid partition. Those values are special, and they belong to Boundary Value Analysis. EP's representative is a "typical" interior value.

### Example 2: Grade Mapping (Several Valid Partitions)

So far our example had one valid partition. Many real rules have several.

**Requirement:** A grading screen accepts a whole-number score from 0 to 100 and shows a letter grade:

- 0 to 59: F
- 60 to 69: D
- 70 to 79: C
- 80 to 89: B
- 90 to 100: A

Scores outside 0 to 100, non-numeric entries, empty, and decimals are rejected with "Invalid score".

Number line:

```
 invalid |    F    |    D    |    C    |    B    |    A     | invalid
 <-------|---------|---------|---------|---------|----------|------->
  -1     0        59 60    69 70    79 80    89 90      100   101

  Five VALID partitions (each produces a different output)
  Two numeric INVALID partitions (below 0, above 100)
  Plus non-numeric, empty, decimal
```

Why five valid partitions rather than one? Because the system must behave differently in each: the expected output is different. This is the key test for deciding whether two values belong in the same partition: **would the system treat them the same way?** A score of 55 and a score of 85 are both "valid scores" but they produce different outputs, so they belong to different classes.

| Test ID | Partition | Representative | Valid / Invalid | Expected result |
|---|---|---|---|---|
| TC-GR-01 | 0 to 59 | 30 | Valid | Grade F |
| TC-GR-02 | 60 to 69 | 65 | Valid | Grade D |
| TC-GR-03 | 70 to 79 | 75 | Valid | Grade C |
| TC-GR-04 | 80 to 89 | 85 | Valid | Grade B |
| TC-GR-05 | 90 to 100 | 95 | Valid | Grade A |
| TC-GR-06 | Below 0 | -10 | Invalid | "Invalid score" |
| TC-GR-07 | Above 100 | 150 | Invalid | "Invalid score" |
| TC-GR-08 | Non-numeric | abc | Invalid | "Invalid score" |
| TC-GR-09 | Empty | (blank) | Invalid | "Invalid score" |
| TC-GR-10 | Decimal | 85.5 | Invalid | "Invalid score" |

Ten partitions, ten tests. With ranges this wide, EP drastically reduces effort: instead of 101 tests for 0 to 100, we run 5 valid tests.

### Example 3: Shipping Cost by Weight

**Requirement:** An online shop calculates shipping by package weight in kilograms (decimals allowed to two places):

- More than 0 and up to 1 kg: $5
- More than 1 and up to 5 kg: $9
- More than 5 and up to 20 kg: $15
- More than 20 kg: cannot be shipped; show "Package too heavy for standard shipping"
- Zero, negative, non-numeric, or empty: show "Enter a valid weight"

Partitions:

```
 invalid |  $5   |   $9    |    $15     |  too heavy
 <-------|-------|---------|------------|----------->
   0     0.01   1  1.01    5  5.01     20  20.01
```

| Test ID | Partition | Representative | Valid / Invalid | Expected result |
|---|---|---|---|---|
| TC-SH-01 | 0 < w <= 1 | 0.5 | Valid | Cost $5 |
| TC-SH-02 | 1 < w <= 5 | 3 | Valid | Cost $9 |
| TC-SH-03 | 5 < w <= 20 | 12 | Valid | Cost $15 |
| TC-SH-04 | w > 20 | 25 | Invalid (rejected by business rule) | "Package too heavy for standard shipping" |
| TC-SH-05 | w = 0 or negative | -2 | Invalid | "Enter a valid weight" |
| TC-SH-06 | Non-numeric | abc | Invalid | "Enter a valid weight" |
| TC-SH-07 | Empty | (blank) | Invalid | "Enter a valid weight" |

A teaching point: "w > 20" is not malformed input; it is a perfectly good number that the business rule refuses. We still treat it as an invalid partition for the shipping calculation because the system must respond differently, with a defined message. Another teaching point: zero and negative could be argued as two partitions if the requirement defined separate messages. When in doubt, split only if the expected behavior differs.

Also notice that 1, 5, and 20 are exactly where the cost changes. Those are boundary values, which BVA handles. EP chose "safe middle" values: 0.5, 3, and 12.

### Example 4: Password Rules for Project 1

**Requirement (Project 1 registration):** A password must:

- Be 8 to 20 characters long.
- Contain at least one uppercase letter, one lowercase letter, one digit, and one special character (from !@#$%^&*).

Here length and character classes are two separate rules. We partition each and then build tests that violate exactly one rule at a time.

**Length partitions**

| ID | Partition | Type |
|---|---|---|
| L1 | Fewer than 8 characters | Invalid |
| L2 | 8 to 20 characters | Valid |
| L3 | More than 20 characters | Invalid |
| L4 | Empty | Invalid |

**Character class partitions**

| ID | Partition | Type |
|---|---|---|
| C1 | Has all four classes | Valid |
| C2 | Missing uppercase | Invalid |
| C3 | Missing lowercase | Invalid |
| C4 | Missing digit | Invalid |
| C5 | Missing special character | Invalid |

**Test cases.** Each invalid test breaks one rule only; everything else is valid.

| Test ID | Partition(s) | Password | Length | Expected result |
|---|---|---|---|---|
| TC-PW-01 | L2 + C1 (all valid) | Test@1234 | 9 | Accepted |
| TC-PW-02 | L1 (too short) | Ab1! | 4 | Rejected: "Password must be 8 to 20 characters" |
| TC-PW-03 | L3 (too long) | Abcdefghij1234567890! | 21 | Rejected: "Password must be 8 to 20 characters" |
| TC-PW-04 | L4 (empty) | (blank) | 0 | Rejected: "Password is required" |
| TC-PW-05 | C2 (no uppercase) | test@1234 | 9 | Rejected: "Include an uppercase letter" |
| TC-PW-06 | C3 (no lowercase) | TEST@1234 | 9 | Rejected: "Include a lowercase letter" |
| TC-PW-07 | C4 (no digit) | Test@abcd | 9 | Rejected: "Include a digit" |
| TC-PW-08 | C5 (no special) | Test12345 | 9 | Rejected: "Include a special character" |

Why does TC-PW-02 use "Ab1!"? Because it contains all four character classes. If we used "abc" as the too-short test, it would be rejected for two reasons, and we could not tell whether the length rule worked. Isolating the rule is what makes the test meaningful.

Eight tests cover nine partitions (L2 and C1 are covered together by TC-PW-01). A real project may also add partitions such as "contains spaces" or "contains disallowed characters", depending on the requirement.

### Example 5: Dropdown or Enumeration (User Type)

**Requirement:** The registration form has a "User type" dropdown with three options: Guest, Member, and Admin. Guest users see a read-only dashboard. Members see a full dashboard. Admins see the dashboard plus an Admin Panel. User type is required.

Partitions:

| ID | Partition | Type |
|---|---|---|
| U1 | Guest | Valid |
| U2 | Member | Valid |
| U3 | Admin | Valid |
| U4 | Nothing selected (placeholder "Select user type") | Invalid |
| U5 | Value not in the list (tampered request, for example "SuperUser") | Invalid |

| Test ID | Partition | Input | Expected result |
|---|---|---|---|
| TC-UT-01 | U1 | Guest | Account created; read-only dashboard |
| TC-UT-02 | U2 | Member | Account created; full dashboard |
| TC-UT-03 | U3 | Admin | Account created; dashboard with Admin Panel |
| TC-UT-04 | U4 | (leave placeholder) | Rejected: "Please select a user type" |
| TC-UT-05 | U5 | SuperUser (sent outside the UI, for example via an API tool) | Rejected; no account with unknown role created |

Here each valid option is its own partition because behavior differs. Compare this with a country dropdown used only to store an address: there, one representative country might represent all valid choices, and one test for "nothing selected" covers the rest. Always ask: does the choice change what the system does?

U5 is a good example of a partition that cannot be reached through the normal screen. It is still worth testing at the API level, because attackers and buggy clients do not use the dropdown.

### Example 6: Email Format

**Requirement:** The Email field must contain exactly one "@", have at least one character before it, and have a domain after it with at least one dot (for example, name@example.com). No spaces are allowed. Maximum length is 254 characters. The field is required.

Partitions:

| ID | Partition | Type |
|---|---|---|
| E1 | Standard valid address | Valid |
| E2 | Valid address with subdomain, dots, or plus sign | Valid |
| E3 | Missing "@" | Invalid |
| E4 | More than one "@" | Invalid |
| E5 | Nothing before "@" (missing local part) | Invalid |
| E6 | Nothing after "@" (missing domain) | Invalid |
| E7 | Domain without a dot | Invalid |
| E8 | Contains a space | Invalid |
| E9 | Longer than 254 characters | Invalid |
| E10 | Empty | Invalid |

| Test ID | Partition | Input | Expected result |
|---|---|---|---|
| TC-EM-01 | E1 | jane@example.com | Accepted |
| TC-EM-02 | E2 | first.last+tag@mail.example.co.uk | Accepted |
| TC-EM-03 | E3 | jane.example.com | Rejected: "Enter a valid email" |
| TC-EM-04 | E4 | jane@@example.com | Rejected |
| TC-EM-05 | E5 | @example.com | Rejected |
| TC-EM-06 | E6 | jane@ | Rejected |
| TC-EM-07 | E7 | jane@example | Rejected |
| TC-EM-08 | E8 | jane doe@example.com | Rejected |
| TC-EM-09 | E9 | (255-character address, for example 243 letter a's followed by @example.com) | Rejected |
| TC-EM-10 | E10 | (blank) | Rejected: "Email is required" |

Email shows how a format becomes a family of partitions: one per distinct way of breaking the rule. Again, each invalid input breaks only one thing, so that when the system rejects it we know which check worked.

(Real-world email validation is notoriously complicated. Always base your partitions on the rules in your own requirement, not on what you think an email "should" look like.)

---

## Combining EP Across Multiple Fields

Real forms have many fields. EP gives you partitions for each. Now comes a trap.

### The Cartesian-Product Explosion

Suppose you test a form with three fields:

- Age: 6 partitions
- Email: 7 partitions
- Password: 8 partitions

If you test every combination of partitions (the cartesian product), you need 6 x 7 x 8 = **336 tests**. Add three more fields and you can easily reach thousands. The whole point of EP was to reduce the number of tests, and now we have lost the benefit.

For the Project 1 registration form we will meet shortly, with six fields and 33 partitions in total, the full product is 7 x 7 x 6 x 8 x 3 x 2 = **14,112 tests**. Nobody would run these. We need a smarter strategy.

### Strategy: Cover Each Valid Partition Once, Then Test One Invalid at a Time

The strategy used by most practitioners has two phases.

**Phase 1: Valid partitions, "each choice" coverage.** Build test cases that together cover every valid partition at least once. You do not need every combination; you just need each valid partition to appear in at least one test. The minimum number of valid tests equals the largest number of valid partitions in any single field. If one field has 2 valid partitions and the others have 1, you need only 2 valid tests (the single valid partitions simply repeat).

**Phase 2: Invalid partitions, one at a time.** For each invalid partition, build a test where that field contains the invalid value and **every other field contains a valid value**. One invalid input per test case.

The total is: (largest number of valid partitions in a field) + (total number of invalid partitions across all fields).

### Why Only One Invalid Input per Test? Masking

This is the most important idea in this section. Invalid inputs can **mask** each other. Masking means that one defect or one error message hides another, so a test with several invalid inputs cannot tell you whether each check works.

Example. A registration form has Age and Email. Suppose a developer wrote the validation like this:

```
if age is invalid:
    show age error and stop
if email is invalid:
    show email error and stop
```

(This "stop at the first error" pattern is common.) Now consider the test:

- Age = "abc" (invalid), Email = "jane.example.com" (invalid)

The system shows only the age error. You see a "correct" rejection and you might mark the test as passed. But you have learned nothing about the email check. If the email validation were completely broken and accepted anything, this test would still pass, and the bug would reach users.

There is a second masking risk: an error in one field can prevent the system from even reaching the code that handles the other field. And a third: when a test fails, you cannot tell which invalid input caused the failure, which makes debugging harder.

The fix is simple: **one invalid input per test, everything else valid.**

```
 BAD (masking)                     GOOD (isolated)
 Age   = abc    (invalid)          TC-A: Age = abc    Email = jane@example.com
 Email = nope   (invalid)          TC-B: Age = 35     Email = nope
 --> which check worked?           --> each check proven separately
```

### Valid Partitions Can Be Combined Safely

Valid inputs do not mask each other, because nothing is rejected. That is why in Phase 1 we are happy to put many valid partitions into one test: Age = 35 with Email = jane@example.com and Password = Test@1234 in one test case, then a second test that uses the second valid email format, and so on.

### Counting the Savings

For the Age (6), Email (7), Password (8) example:

- Each valid partition: Age has 1 valid, Email has 2 valid, Password has 1 valid. Largest is 2, so Phase 1 needs **2 tests**.
- Invalid partitions: Age has 5, Email has 5, Password has 7. Total 17, so Phase 2 needs **17 tests**.
- Total: 2 + 17 = **19 tests** instead of 336. Every partition is still covered.

### What About Combinations We Skipped?

By skipping combinations, we accept a risk: defects caused by specific combinations of valid values (for example, age 18 with country X triggers a bug) will not be found by this strategy. When requirements say two fields interact, test those interactions deliberately. Techniques such as decision tables (a later lesson today) are designed for exactly this. EP handles each input; decision tables handle the rules that combine them.

---

## EP Coverage

How do you know how thoroughly your EP tests cover your design? There is a simple measure.

**EP coverage = (number of partitions covered by at least one test / total number of partitions) x 100%**

Coverage is always measured against the partitions you identified, not against all the inputs in the universe.

### Worked Numbers

**Age field.** There are 6 partitions. Suppose you only run a "happy path" check plus two quick negatives: 35 (P2), 15 (P1), and 70 (P3).

- Partitions covered: 3 (P1, P2, P3)
- Total partitions: 6
- Coverage = 3 / 6 x 100 = **50%**

Add "abc" (P4): 4 / 6 = **66.7%**. Add empty (P5): 5 / 6 = **83.3%**. Add 25.5 (P6): 6 / 6 = **100%**.

**Project 1 registration form.** Total 33 partitions (7 valid, 26 invalid).

- Only the two valid tests: partitions covered = 7. Coverage = 7 / 33 x 100 = **21.2%**.
- Valid tests plus 18 of the 26 invalid tests: covered = 7 + 18 = 25. Coverage = 25 / 33 x 100 = **75.8%**.
- All 28 tests: covered = 33. Coverage = 33 / 33 x 100 = **100%**.

Notice what the first number tells us. A tester who only runs "everything valid" tests feels like they have tested the form, yet they have covered barely a fifth of the partitions. Coverage numbers expose that false confidence.

Two cautions:

1. 100% EP coverage does not mean 100% of defects found. It means every partition you identified was sampled. If your partitions are wrong or incomplete, the number is misleading.
2. Coverage is a tool for communication and gap-finding, not a goal in itself. Use it to ask, "Which partitions have we not touched, and is that acceptable given the risk?"

---

## EP Beyond Inputs: Outputs, Time, State, and Configuration

Most beginners apply EP only to input fields. The technique is more general: anything that can be divided into groups with uniform behavior can be partitioned. This is an introduction; you will meet these ideas again in later lessons.

### Output Partitions

Instead of asking "what can go in?", ask "what can come out?" and design tests so that every kind of output appears at least once.

For the grade example, the output partitions are the letters F, D, C, B, A, and the "Invalid score" message. Even if you forget the input rules, you can check that your tests produce each output at least once. For a discount engine, the outputs might be 0%, 5%, 10%, and 20%; make sure each discount tier is triggered by some test.

### Time Partitions

Time-based behavior divides naturally into classes. Consider a session timeout of 15 minutes of inactivity:

- Active within the timeout window (for example, 5 minutes idle): session continues.
- Idle beyond the timeout (for example, 20 minutes idle): session expires, user must log in again.

Another example: a "Happy Hour" discount from 5 pm to 7 pm. Partitions are before 5 pm, between 5 pm and 7 pm, and after 7 pm. As with numeric ranges, the edges of these intervals are good places for boundary tests.

### State Partitions

The same input can be handled differently depending on the system state. For Project 1 login, an account may be:

- Active (login succeeds with correct credentials).
- Locked after too many failed attempts (login refused).
- Not yet verified (login refused with a "verify your email" message).
- Deleted (login refused, as with unknown account).

Each state is a partition of the "account status" condition. Testing login with correct credentials against each state gives four tests. Full treatment of states and the transitions between them is the subject of the State Transition Testing lesson later today.

### Configuration and Environment Partitions

Software runs on many combinations of browsers, devices, operating systems, and languages. You cannot test all of them either, so you partition them. For example, browsers might be grouped as "Chromium-based" (Chrome, Edge), "Firefox", and "Safari", with one representative from each. Screen sizes can be partitioned into phone, tablet, and desktop. Languages can be grouped as left-to-right and right-to-left. The same logic applies: pick a representative from each class, based on risk and usage data.

---

## Combining EP and BVA

You learned Boundary Value Analysis just before this lesson. Let us see how it fits with EP.

### The Relationship

- **EP asks:** which groups of inputs behave alike? Test one from each group.
- **BVA asks:** where do the groups meet? Test values on and next to the edges, because that is where developers make mistakes.

BVA is not a competitor to EP. It is an extension that refines EP for ordered data such as numbers, dates, and lengths. In practice, you almost always partition first (EP) and then add boundary tests (BVA) for each numeric edge.

### Combined Worked Example: Age 18 to 60

Valid range 18 to 60. We use 3-value BVA (the value just below, on, and just above each boundary).

```
 invalid           |           valid            |           invalid
 <-----------------|----------------------------|------------------->
        15     17 18 19        35          59 60 61       70
        EP     BVA BVA BVA     EP          BVA BVA BVA    EP
```

**The three approaches compared**

| Approach | Tests for the age field | What it finds |
|---|---|---|
| Exhaustive | At least 121 numeric tests (whole numbers 0 to 120) plus unlimited non-numeric inputs | Everything, in theory, but impossible in practice |
| EP only | 6 tests: 15, 35, 70, abc, empty, 25.5 | Gross mistakes in each class; will miss off-by-one errors |
| EP + BVA | 9 tests: 17, 18, 19, 59, 60, 61, abc, empty, 25.5 | Class-level and edge-level defects |

**The combined test set (EP + BVA)**

| Test ID | Value | Partition covered | Technique | Expected result |
|---|---|---|---|---|
| TC-AGE-C01 | 17 | Below 18 (invalid) | BVA (just below minimum) | Rejected |
| TC-AGE-C02 | 18 | 18 to 60 (valid) | BVA (minimum) | Accepted |
| TC-AGE-C03 | 19 | 18 to 60 (valid) | BVA (just above minimum) | Accepted |
| TC-AGE-C04 | 59 | 18 to 60 (valid) | BVA (just below maximum) | Accepted |
| TC-AGE-C05 | 60 | 18 to 60 (valid) | BVA (maximum) | Accepted |
| TC-AGE-C06 | 61 | Above 60 (invalid) | BVA (just above maximum) | Rejected |
| TC-AGE-C07 | abc | Non-numeric (invalid) | EP | Rejected |
| TC-AGE-C08 | (blank) | Empty (invalid) | EP | Rejected |
| TC-AGE-C09 | 25.5 | Decimal (invalid) | EP | Rejected |

Notice something elegant: the boundary values also serve as representatives. 17 stands in for the whole "below 18" class, and 61 stands in for "above 60". So we do not need separate EP tests of 15 and 70. If you still want a typical interior value such as 35 to confirm normal behavior, add it: 10 tests. Even then, we are at 10 tests instead of 121 or more.

**Counting**

- Exhaustive: 121+ (and infinite for non-numeric)
- EP only: 6
- EP + BVA: 9 (or 10 with an interior value)

The extra three or four tests buy us protection against the off-by-one bugs that EP alone cannot see. For most fields, that is an excellent trade.

### EP vs BVA Comparison

| Aspect | Equivalence Partitioning | Boundary Value Analysis |
|---|---|---|
| Core question | Which inputs behave the same way? | Where does behavior change? |
| What it selects | One representative per partition | Values at and next to each boundary |
| Typical values | Middle of a partition (for example, 35) | Edges (17, 18, 19 and 59, 60, 61) |
| Works on | Any input with classes: ranges, sets, formats, booleans | Ordered, bounded data: numbers, dates, lengths, sizes |
| Strength | Covers every kind of class, including invalid types | Catches off-by-one and comparison errors |
| Weakness | Cannot see boundary mistakes | Does not apply to unordered sets or booleans |
| Number of tests | One per partition | Two or three per boundary |
| Relationship | Foundation | Extension of EP; used together |

---

## A Python Demo: EP Tests in Code

Seeing EP in code makes the idea concrete, and it prepares you for the automation work coming up in this program. We will test a function that returns a ticket price based on age.

**Requirement for `get_ticket_price(age)`:**

- Age must be a whole number from 0 to 120. Anything else is an error (the function raises a `ValueError`).
- Ages 0 to 12 (child): $8
- Ages 13 to 64 (adult): $15
- Ages 65 to 120 (senior): $10

### Partitions

| ID | Partition | Type | Representative | Expected |
|---|---|---|---|---|
| T1 | Child, 0 to 12 | Valid | 7 | 8 |
| T2 | Adult, 13 to 64 | Valid | 40 | 15 |
| T3 | Senior, 65 to 120 | Valid | 80 | 10 |
| T4 | Negative | Invalid | -5 | ValueError |
| T5 | Above 120 | Invalid | 200 | ValueError |
| T6 | Decimal | Invalid | 12.5 | ValueError |
| T7 | Text | Invalid | "abc" | ValueError |
| T8 | Empty (None) | Invalid | None | ValueError |

### File 1: `ticket_price.py` (the code under test)

```python
def get_ticket_price(age):
    """Return the ticket price in dollars for a given age."""
    if isinstance(age, bool) or not isinstance(age, int):
        raise ValueError("Age must be a whole number")
    if age < 0 or age > 120:
        raise ValueError("Age must be between 0 and 120")
    if age <= 12:
        return 8
    if age <= 64:
        return 15
    return 10
```

Line-by-line explanation:

- `def get_ticket_price(age):` defines a function named `get_ticket_price` that takes one input called `age`.
- The triple-quoted line is a docstring, a short description of what the function does.
- `if isinstance(age, bool) or not isinstance(age, int):` checks the type of the input. `isinstance(age, int)` is True when `age` is a whole number. In Python, `True` and `False` are technically integers, so we check `bool` first to reject them. Text, decimals, and `None` are not integers, so the `not isinstance(...)` part catches them.
- `raise ValueError("Age must be a whole number")` stops the function and signals an error with a message. This is how the function "rejects" invalid input.
- `if age < 0 or age > 120:` handles whole numbers that are outside the allowed range.
- `raise ValueError("Age must be between 0 and 120")` rejects them with a different message.
- `if age <= 12: return 8` is the child price. Because earlier checks have already rejected negatives, any age that reaches this line is 0 or higher.
- `if age <= 64: return 15` is the adult price. Only ages 13 to 64 get here, because ages 0 to 12 have already returned.
- `return 10` is the senior price. Only ages 65 to 120 reach this line.

### File 2: `ticket_ep.py` (the EP test script, plain Python)

```python
# ticket_ep.py - Equivalence Partitioning demo
from ticket_price import get_ticket_price

# Each row: (partition name, representative age, expected price)
valid_cases = [
    ("Child (0-12)", 7, 8),
    ("Adult (13-64)", 40, 15),
    ("Senior (65-120)", 80, 10),
]

# Each row: (partition name, representative input)
invalid_cases = [
    ("Negative age", -5),
    ("Above maximum", 200),
    ("Decimal", 12.5),
    ("Text", "abc"),
    ("Empty (None)", None),
]

passed = 0
failed = 0

print("--- Valid partitions ---")
for name, age, expected in valid_cases:
    actual = get_ticket_price(age)
    if actual == expected:
        passed += 1
        print(f"PASS  {name:<18} age={age!r:<6} expected={expected} actual={actual}")
    else:
        failed += 1
        print(f"FAIL  {name:<18} age={age!r:<6} expected={expected} actual={actual}")

print("--- Invalid partitions ---")
for name, value in invalid_cases:
    try:
        get_ticket_price(value)
        failed += 1
        print(f"FAIL  {name:<18} input={value!r:<6} no error was raised")
    except ValueError as err:
        passed += 1
        print(f"PASS  {name:<18} input={value!r:<6} rejected: {err}")

total = passed + failed
print(f"\nResult: {passed} passed, {failed} failed, {total} total")
print(f"Partition coverage: {passed}/{total} = {passed / total * 100:.0f}%")
```

Line-by-line explanation:

- `from ticket_price import get_ticket_price` loads the function from the first file so we can call it. Both files must be in the same folder.
- `valid_cases = [...]` is a list of tuples. Each tuple holds a partition name, the representative age, and the expected price. This is our EP table written as data. One row equals one partition.
- `invalid_cases = [...]` is the same idea for invalid partitions, but there is no expected price, because the expected result for all of them is "an error is raised".
- `passed = 0` and `failed = 0` are counters that we update as tests run.
- `for name, age, expected in valid_cases:` loops through each row, unpacking the three parts into variables.
- `actual = get_ticket_price(age)` calls the function under test with the representative value.
- `if actual == expected:` compares the real result with the expected result. This is the test oracle: the check that decides pass or fail.
- `passed += 1` or `failed += 1` updates the counters.
- The `print(f"...")` lines show a formatted result. The `{name:<18}` part pads the name to 18 characters so the columns line up, and `!r` shows the value as Python would write it (so the text "abc" shows with quotes).
- In the invalid loop, `try:` attempts the call. If the function wrongly accepts the bad input, no error occurs, so we count a failure and print "no error was raised".
- `except ValueError as err:` runs only when the function raises a `ValueError`, which is what we want. We count a pass and print the error message.
- The final lines compute the total and print a summary. `:.0f` formats the percentage with no decimals.

**Run it:**

```
python ticket_ep.py
```

**Expected output:**

```
--- Valid partitions ---
PASS  Child (0-12)       age=7      expected=8 actual=8
PASS  Adult (13-64)      age=40     expected=15 actual=15
PASS  Senior (65-120)    age=80     expected=10 actual=10
--- Invalid partitions ---
PASS  Negative age       input=-5     rejected: Age must be between 0 and 120
PASS  Above maximum      input=200    rejected: Age must be between 0 and 120
PASS  Decimal            input=12.5   rejected: Age must be a whole number
PASS  Text               input='abc'  rejected: Age must be a whole number
PASS  Empty (None)       input=None   rejected: Age must be a whole number

Result: 8 passed, 0 failed, 8 total
Partition coverage: 8/8 = 100%
```

Eight partitions, eight tests, 100% EP coverage. (The slightly uneven column spacing in the invalid section is just formatting and is harmless.)

### File 3: `test_ticket_pytest.py` (the same tests with pytest, parametrized)

If you have pytest installed (`pip install pytest`), the same EP table can be written even more compactly with parametrization, which runs one test function once for each row of data:

```python
import pytest
from ticket_price import get_ticket_price

@pytest.mark.parametrize("age, expected", [(7, 8), (40, 15), (80, 10)])
def test_valid_partitions(age, expected):
    assert get_ticket_price(age) == expected

@pytest.mark.parametrize("bad_input", [-5, 200, 12.5, "abc", None])
def test_invalid_partitions(bad_input):
    with pytest.raises(ValueError):
        get_ticket_price(bad_input)
```

Explanation:

- `import pytest` loads the testing library.
- `@pytest.mark.parametrize("age, expected", [...])` is a decorator that tells pytest: run the function below once for each pair in the list. The first run uses age 7 and expected 8, the second uses 40 and 15, the third 80 and 10. The data list is our list of representatives.
- `def test_valid_partitions(age, expected):` is the test function. Pytest finds it because its name starts with `test_`.
- `assert get_ticket_price(age) == expected` is the check. If the condition is False, pytest marks the test as failed.
- The second decorator lists the five invalid representatives.
- `with pytest.raises(ValueError):` says "the code inside this block must raise a ValueError; if it does not, fail the test."

**Run it:**

```
python -m pytest -q test_ticket_pytest.py
```

**Expected output:**

```
........                                                                 [100%]
8 passed in 0.01s
```

(The time will vary on your computer.) Each dot is one passing test: three valid and five invalid, matching our eight partitions.

### Where EP Alone Falls Short, Shown in Code

Now imagine a developer makes a classic off-by-one slip and writes `age < 12` instead of `age <= 12` for the child price:

```python
def buggy_price(age):
    if age < 12:      # BUG: should be age <= 12
        return 8
    if age < 65:
        return 15
    return 10
```

Our three valid EP tests (ages 7, 40, 80) all still pass, because the bug only affects age 12 exactly. Running a boundary test shows it:

```
PASS  EP child       age=7   expected=8 actual=8
PASS  EP adult       age=40  expected=15 actual=15
PASS  EP senior      age=80  expected=10 actual=10
FAIL  BVA child max  age=12  expected=8 actual=15
```

This is the practical reason we pair EP with BVA. EP verified that each class works; BVA caught the edge. Keep this picture in mind whenever you are tempted to stop after EP.

---

## Applying EP to the Project 1 Registration Form

Let us apply the whole procedure to the User Registration feature of Project 1.

### Step 1 and 2: Inputs and Rules

| Field | Rule |
|---|---|
| Username | Required; 3 to 15 characters; letters, digits, and underscore only; must start with a letter |
| Email | Required; valid format (one "@", domain with a dot, no spaces); up to 254 characters |
| Age | Required; whole number from 18 to 60 |
| Password | Required; 8 to 20 characters; at least one uppercase, lowercase, digit, and special character |
| Country | Required; select from a dropdown of supported countries (all supported countries behave the same) |
| Terms checkbox | Must be checked to register |

### Step 3: Partitions per Field

| Field | Valid partitions | Invalid partitions | Total |
|---|---|---|---|
| Username | UN-V1: 3 to 15 chars, allowed characters, starts with a letter | UN-I1: fewer than 3 chars; UN-I2: more than 15 chars; UN-I3: starts with a digit; UN-I4: contains a disallowed character (space, @); UN-I5: empty; UN-I6: already registered (state) | 1 + 6 = 7 |
| Email | EM-V1: standard address; EM-V2: address with subdomain or plus sign | EM-I1: no "@"; EM-I2: two "@"; EM-I3: no domain dot; EM-I4: contains a space; EM-I5: empty | 2 + 5 = 7 |
| Age | AG-V1: 18 to 60 | AG-I1: below 18; AG-I2: above 60; AG-I3: non-numeric; AG-I4: decimal; AG-I5: empty | 1 + 5 = 6 |
| Password | PW-V1: 8 to 20 chars with all four classes | PW-I1: too short; PW-I2: too long; PW-I3: no uppercase; PW-I4: no lowercase; PW-I5: no digit; PW-I6: no special; PW-I7: empty | 1 + 7 = 8 |
| Country | CT-V1: a supported country | CT-I1: nothing selected; CT-I2: unsupported value (sent outside the UI) | 1 + 2 = 3 |
| Terms | TM-V1: checked | TM-I1: unchecked | 1 + 1 = 2 |
| **Totals** | **7 valid** | **26 invalid** | **33** |

### Steps 4 to 6: Test Cases

**Base valid data** used wherever a field is not the one being varied: Username `jane_doe`, Email `jane@example.com`, Age `30`, Password `Test@1234`, Country `Canada`, Terms checked.

Phase 1 (valid, each choice): 2 tests. Phase 2 (one invalid at a time): 26 tests. Total: 28.

| Test ID | Field varied | Partition | Input for that field | Expected result |
|---|---|---|---|---|
| TC-REG-01 | All valid | UN-V1, EM-V1, AG-V1, PW-V1, CT-V1, TM-V1 | Base data | Account created; confirmation shown |
| TC-REG-02 | Email | EM-V2 | first.last+tag@mail.example.co.uk | Account created |
| TC-REG-03 | Username | UN-I1 | ab | Rejected: username length error |
| TC-REG-04 | Username | UN-I2 | abcdefghijklmnop (16 chars) | Rejected: username length error |
| TC-REG-05 | Username | UN-I3 | 9lives | Rejected: must start with a letter |
| TC-REG-06 | Username | UN-I4 | jane doe | Rejected: invalid characters |
| TC-REG-07 | Username | UN-I5 | (blank) | Rejected: "Username is required" |
| TC-REG-08 | Username | UN-I6 | (a username that already exists) | Rejected: "Username already taken" (needs prepared data) |
| TC-REG-09 | Email | EM-I1 | jane.example.com | Rejected: invalid email |
| TC-REG-10 | Email | EM-I2 | jane@@example.com | Rejected: invalid email |
| TC-REG-11 | Email | EM-I3 | jane@example | Rejected: invalid email |
| TC-REG-12 | Email | EM-I4 | jane doe@example.com | Rejected: invalid email |
| TC-REG-13 | Email | EM-I5 | (blank) | Rejected: "Email is required" |
| TC-REG-14 | Age | AG-I1 | 15 | Rejected: age error |
| TC-REG-15 | Age | AG-I2 | 70 | Rejected: age error |
| TC-REG-16 | Age | AG-I3 | abc | Rejected: age error |
| TC-REG-17 | Age | AG-I4 | 25.5 | Rejected: age error |
| TC-REG-18 | Age | AG-I5 | (blank) | Rejected: "Age is required" |
| TC-REG-19 | Password | PW-I1 | Ab1! | Rejected: length error |
| TC-REG-20 | Password | PW-I2 | Abcdefghij1234567890! | Rejected: length error |
| TC-REG-21 | Password | PW-I3 | test@1234 | Rejected: needs uppercase |
| TC-REG-22 | Password | PW-I4 | TEST@1234 | Rejected: needs lowercase |
| TC-REG-23 | Password | PW-I5 | Test@abcd | Rejected: needs digit |
| TC-REG-24 | Password | PW-I6 | Test12345 | Rejected: needs special character |
| TC-REG-25 | Password | PW-I7 | (blank) | Rejected: "Password is required" |
| TC-REG-26 | Country | CT-I1 | (placeholder "Select country") | Rejected: "Please select a country" |
| TC-REG-27 | Country | CT-I2 | Atlantis (sent outside the UI) | Rejected; no account created |
| TC-REG-28 | Terms | TM-I1 | Unchecked | Rejected: "You must accept the terms" |

Compare: 14,112 full combinations versus 28 tests with 100% partition coverage. That is a reduction of more than 99.8 percent, and every partition is still exercised. Remember the caveats: boundaries (BVA adds tests at 17/18/19 and 59/60/61 for age, and 2/3/4 and 15/16 for username length), combinations (decision tables), and state (state transition) are handled by other techniques.

---

## Try It: Pair Activity with Project 1

Today's exercise is pair programming. Use this EP activity as one of your three techniques.

**Setup.** Work in pairs. One person is the **driver** (writes in the shared document or spreadsheet), the other is the **navigator** (reads the requirement, questions each decision, and watches for gaps). Swap roles halfway through.

**Part 1: Partition the Login form (about 25 minutes).**

1. Open the Project 1 Login requirements. List the inputs (for example, Email or Username, Password, "Remember me" checkbox).
2. For each input, write the rules from the requirement. If a rule is unclear, write the question you would ask the product owner.
3. Build a partition table in the same format as the registration table above: field, valid partitions, invalid partitions, total.
4. Include at least one state partition (for example, locked account or unverified account) and one boolean partition ("Remember me").

**Part 2: Create the test cases (about 20 minutes).**

1. Define base valid data.
2. Write a test case table with ID, field varied, partition, input, and expected result.
3. Apply the "valid each choice, then one invalid at a time" strategy.
4. Calculate your EP coverage using the formula. It should be 100% if every partition has a test.

**Part 3: Cross-review (about 15 minutes).** Swap tables with another pair. Using the checklist below, review their work and leave written comments.

Cross-review checklist:

- Do the partitions overlap anywhere? (Any value in two classes?)
- Is every possible input in some partition? (Any gaps?)
- Is "empty" covered for every required field?
- Does every invalid test change only one thing?
- Is every expected result written from the requirement, with a specific message or behavior?
- Did they use an interior value rather than a boundary as the representative?
- Where would BVA add value? Mark those fields.

**Deliverable.** A partition table, a test case table, a coverage calculation, and a list of review comments received and how you resolved them.

---

## Limitations of Equivalence Partitioning

EP is excellent, but not complete. Be honest about what it cannot do.

1. **It does not test boundaries well.** A representative from the middle of a class will not reveal off-by-one errors. Use BVA alongside it.
2. **It does not test combinations.** Using "one invalid at a time" and "each choice" coverage means interactions between fields are not examined. Use decision tables or pairwise techniques where fields interact.
3. **It does not consider state or sequence.** The same input can behave differently depending on history. State transition testing handles this.
4. **It depends on the quality of the requirement.** If the requirement is wrong, vague, or missing, the partitions will be as well. EP cannot test a rule nobody wrote down.
5. **It relies on the equivalence assumption.** Hidden special cases in the code, such as a special-cased value, will not be discovered. Error guessing and experienced judgment help here.
6. **It tests what you think of.** A partition you did not imagine (for example, emoji in a name field) is not tested at all. Checklists and peer review reduce this risk.

---

## Common Mistakes (and How to Avoid Them)

### Mistake 1: Overlapping Partitions

Overlapping partitions put the same value in two classes. For example, "age 18 to 30" and "age 30 to 60": age 30 is in both. Overlaps make it unclear what the expected result is and signal that you have not read the requirement closely. **Fix:** write partitions with precise inequalities (18 <= age <= 29 and 30 <= age <= 60) and check that every value belongs to exactly one class.

### Mistake 2: Gaps, or Missing Invalid Partitions

Beginners often list only the valid class and the "too high" and "too low" classes, forgetting types of invalid input such as text, symbols, decimals, negative numbers, and special characters. They also forget to partition the invalid side finely enough, treating "bad email" as one class when there are many different ways for an email to be bad. **Fix:** for each field, run through the Rules checklist in this lesson and ask, "What are all the ways this could be wrong?"

### Mistake 3: Picking Boundary Values and Thinking It Is Only EP

If you choose 18 as the representative for the valid age class, you are doing boundary testing, not EP, and you will be left with no interior value. That is not a catastrophe, but it confuses your documentation and can leave you thinking you have used two techniques when you have not. **Fix:** be deliberate. For EP, pick interior values. For BVA, pick edges, and label them as such (as in our combined table).

### Mistake 4: Forgetting Empty and Null

A required field left blank is one of the most common real-world inputs, and one of the most common sources of unhandled errors (crashes, silent acceptance, "null" saved in the database). **Fix:** add "empty" and, where relevant, "only spaces" to every field's partition list.

### Mistake 5: Testing Several Invalid Inputs at Once

Multiple invalid inputs in one test lead to masking, as we saw. **Fix:** one invalid input per test, all other fields valid.

### Mistake 6: Partitioning by What the Screen Shows Rather Than What the Rules Say

If the UI uses a dropdown, you might assume bad values cannot occur. They can, through API calls, edited requests, or old cached pages. **Fix:** consider invalid partitions that cannot be created through the UI, and test them through the layer where they can occur.

### Mistake 7: Inventing Expected Results from the Current Behavior

If you run the system first and write down whatever happens, you are not testing, you are recording. **Fix:** write the expected result from the requirement before execution.

### Mistake 8: Making Partitions Too Coarse or Too Fine

Too coarse (one big "valid" class when the system actually has five behaviors) hides defects. Too fine (a partition per value) defeats the purpose. **Fix:** ask "would the system behave differently?" If yes, separate them; if no, merge them.

---

## Practice Exercises

Try these on your own or with your pair before checking the answer key. For each, list the partitions, mark them valid or invalid, pick representatives, and state the expected result.

### Exercise 1: Payment Method Dropdown

An online checkout has a required "Payment method" dropdown with options Credit Card, PayPal, and Bank Transfer. Credit Card shows a card number form. PayPal redirects to the PayPal site. Bank Transfer shows bank details and marks the order "Awaiting payment".

### Exercise 2: Insurance Premium by Age Bracket

A motor insurance calculator accepts the driver's age (whole numbers) and returns a monthly premium:

- Under 18: not eligible ("Must be 18 or older")
- 18 to 25: $200
- 26 to 40: $150
- 41 to 65: $120
- Over 65: not eligible online ("Please call us")
- Non-numeric, decimal, or empty: "Enter a valid age"

### Exercise 3: Coupon Code Formats

A coupon field accepts codes in the format three uppercase letters, a hyphen, and four digits (for example, ABC-1234). Anything else shows "Invalid coupon". Empty shows "Enter a coupon code". (Assume that a correctly formatted code is then checked for existence; for this exercise, partition format only and treat any correctly formatted code as accepted.)

### Exercise 4: File Upload Types

A profile photo upload accepts JPG and PNG files up to 2 MB. Other types and larger files are rejected with specific messages. Submitting without choosing a file shows "Please choose a file".

### Exercise 5: Username Rules

A username must be 4 to 12 characters long and contain only lowercase letters and digits. Anything else is rejected.

### Exercise 6: Shipping Zones

A shipping calculator takes a destination country from a dropdown and assigns a zone:

- Zone 1 (United States): $5
- Zone 2 (Canada, Mexico): $12
- Zone 3 (any country in the European Union): $25
- Any other country: "We do not ship there"
- No country selected: "Select a destination"

### Exercise 7 (Challenge): Newsletter Checkbox and Age Together

A form has an optional "Subscribe to newsletter" checkbox and the Age field (18 to 60). Using the multi-field strategy, how many tests do you need for 100% partition coverage? List them.

---

## Answer Key

### Answer 1: Payment Method Dropdown

| Partition | Type | Representative | Expected result |
|---|---|---|---|
| Credit Card | Valid | Credit Card | Card number form displayed |
| PayPal | Valid | PayPal | Redirect to PayPal |
| Bank Transfer | Valid | Bank Transfer | Bank details shown; order status "Awaiting payment" |
| Nothing selected | Invalid | (placeholder) | Error: "Select a payment method" |
| Value not in list | Invalid | "Cheque" (sent outside the UI) | Rejected; no order created |

Each option is its own valid partition because behavior differs. Five tests.

### Answer 2: Insurance Premium

| Partition | Type | Representative | Expected result |
|---|---|---|---|
| Under 18 | Invalid | 16 | "Must be 18 or older" |
| 18 to 25 | Valid | 21 | $200 |
| 26 to 40 | Valid | 33 | $150 |
| 41 to 65 | Valid | 50 | $120 |
| Over 65 | Invalid | 70 | "Please call us" |
| Non-numeric | Invalid | abc | "Enter a valid age" |
| Decimal | Invalid | 30.5 | "Enter a valid age" |
| Empty | Invalid | (blank) | "Enter a valid age" |
| Negative | Invalid (optional, include if the requirement treats it separately) | -4 | "Must be 18 or older" or "Enter a valid age" per requirement; clarify with the product owner |

Eight or nine tests. Note the negative case: the requirement does not state what to show, which is a good reason to raise a question. Boundary values to add with BVA: 17, 18, 25, 26, 40, 41, 65, 66.

### Answer 3: Coupon Code Formats

| Partition | Type | Representative | Expected result |
|---|---|---|---|
| Correct format | Valid | ABC-1234 | Accepted as correctly formatted |
| Lowercase letters | Invalid | abc-1234 | "Invalid coupon" |
| Missing hyphen | Invalid | ABC1234 | "Invalid coupon" |
| Too few letters | Invalid | AB-1234 | "Invalid coupon" |
| Too many letters | Invalid | ABCD-1234 | "Invalid coupon" |
| Too few digits | Invalid | ABC-123 | "Invalid coupon" |
| Too many digits | Invalid | ABC-12345 | "Invalid coupon" |
| Letters in digit part | Invalid | ABC-12A4 | "Invalid coupon" |
| Digits in letter part | Invalid | AB1-1234 | "Invalid coupon" |
| Contains spaces | Invalid | ABC- 1234 | "Invalid coupon" |
| Empty | Invalid | (blank) | "Enter a coupon code" |

Eleven tests. Each invalid input breaks exactly one aspect of the format.

### Answer 4: File Upload Types

| Partition | Type | Representative | Expected result |
|---|---|---|---|
| JPG within 2 MB | Valid | photo.jpg, 500 KB | Uploaded |
| PNG within 2 MB | Valid | photo.png, 500 KB | Uploaded |
| Unsupported type | Invalid | document.pdf, 100 KB | Rejected: type not allowed |
| Another unsupported type | Invalid | animation.gif, 100 KB | Rejected: type not allowed |
| JPG over 2 MB | Invalid | big.jpg, 5 MB | Rejected: file too large |
| Zero-byte file | Invalid | empty.jpg, 0 KB | Rejected: file is empty or corrupt |
| Wrong content, right extension | Invalid | script.exe renamed to script.jpg | Rejected; not stored as an image |
| No file chosen | Invalid | (no file) | "Please choose a file" |

Eight tests. Whether JPG and PNG are separate partitions depends on whether they are processed differently (for example, different image libraries). If unsure, test both; it is cheap.

### Answer 5: Username Rules

Length partitions: fewer than 4, 4 to 12, more than 12, empty. Character partitions: lowercase letters and digits only (valid), contains uppercase, contains a space, contains a special character.

| Partition | Type | Representative | Expected result |
|---|---|---|---|
| 4 to 12 chars, lowercase and digits | Valid | jane99 | Accepted |
| Fewer than 4 | Invalid | ab1 | Rejected: length |
| More than 12 | Invalid | abcdefghijklm1 (14 chars) | Rejected: length |
| Contains uppercase | Invalid | Jane99 | Rejected: invalid characters |
| Contains space | Invalid | jane 99 | Rejected: invalid characters |
| Contains special character | Invalid | jane_99 | Rejected: invalid characters (underscore is not allowed here) |
| Empty | Invalid | (blank) | Rejected: required |

Seven tests. Notice that each invalid test keeps the other rule satisfied: "Jane99" has a valid length; "ab1" has valid characters. Boundary lengths to add with BVA: 3, 4, 5 and 11, 12, 13.

### Answer 6: Shipping Zones

| Partition | Type | Representative | Expected result |
|---|---|---|---|
| Zone 1 | Valid | United States | $5 |
| Zone 2 | Valid | Canada (or Mexico) | $12 |
| Zone 3 | Valid | Germany (any EU country) | $25 |
| Other country | Invalid for shipping | Japan | "We do not ship there" |
| Nothing selected | Invalid | (placeholder) | "Select a destination" |

Five tests. Zone 2 has two members; testing one is enough under EP, though a cautious tester might test both because the list is short. Note that the EU list could change over time, which is a good reason to confirm how the system defines "EU country".

### Answer 7: Newsletter Checkbox and Age

Partitions: Age has 6 (1 valid, 5 invalid). Newsletter has 2, both valid (checked and unchecked have different outcomes: with and without subscription). Total 8 partitions.

Phase 1: the largest number of valid partitions in any field is 2 (the checkbox), so we need 2 valid tests:

1. Age 35, newsletter checked (covers AG-V1 and Checked).
2. Age 35, newsletter unchecked (covers Unchecked).

Phase 2: invalid age partitions, one at a time, with the checkbox at a valid value: 15, 70, abc, 25.5, blank. That is 5 tests.

Total: 7 tests, covering 8 of 8 partitions (100%). The full cartesian product would be 6 x 2 = 12 tests; the saving is small here but grows quickly as fields are added.

---

## Knowledge Check

Test yourself. Answers follow the questions.

1. In one sentence, what is the core idea of Equivalence Partitioning?
2. What is the difference between a valid partition and an invalid partition?
3. A field accepts whole numbers from 1 to 50. How many partitions would you create, and what are they? (Include non-numeric, empty, and decimal.)
4. What is the equivalence assumption, and name one situation where it can fail.
5. Why do we test only one invalid input per test case when combining fields?
6. A form has four fields with 5, 6, 4, and 3 partitions. How many tests does the full cartesian product need?
7. A feature has 20 partitions, and your tests cover 15 of them. What is the EP coverage?
8. True or false: if you pick 18 and 60 as your representatives for the valid age partition, you are applying pure EP. Explain.
9. Name two partitions you might create for an "Account status" condition on Project 1 login, and say what kind of partition this is.
10. Your teammate's age partitions are "18 to 30" and "30 to 60". What is wrong, and how do you fix it?
11. Why did our `get_ticket_price` EP tests not catch the `age < 12` bug, and which technique would?
12. For a requirement "Phone number: exactly 10 digits, numbers only", list at least five partitions.

### Answers

1. Divide all possible inputs into groups that the system should treat the same, then test one representative value from each group.
2. A valid partition contains inputs the system should accept and process normally; an invalid partition contains inputs the system should reject or handle with an error or defined fallback.
3. Six partitions: below 1 (invalid), 1 to 50 (valid), above 50 (invalid), non-numeric (invalid), empty (invalid), decimal (invalid).
4. The assumption is that all values in a partition are processed the same way, so one representative is as good as any other. It can fail when partitions are drawn incorrectly, when the code has hidden special cases, at boundaries (off-by-one errors), when fields interact, or when state matters. Any one of these is an acceptable answer.
5. Because invalid inputs can mask each other: one error message or early exit can hide whether the other check works, and a failure becomes harder to diagnose. One invalid input with everything else valid proves each check separately.
6. 5 x 6 x 4 x 3 = 360 tests.
7. 15 / 20 x 100 = 75%.
8. False. Those values are boundaries, so you are applying BVA, not pure EP. EP would use an interior value such as 35. (Using 18 and 60 is perfectly good test design; the point is to label the technique correctly and note that you still need a representative if you want to confirm interior behavior.)
9. For example "Active" and "Locked" (also "Unverified" and "Deleted"). This is a state partition.
10. The partitions overlap at age 30, so it is unclear what the expected result is for 30. Fix: "18 to 29" and "30 to 60" (or "18 to 30" and "31 to 60").
11. Because the bug only affects age 12 exactly, and our representatives (7, 40, 80) were interior values far from the edges. Boundary Value Analysis (testing 12 and 13, and 64 and 65) would catch it.
12. For example: exactly 10 digits (valid); fewer than 10 digits (invalid); more than 10 digits (invalid); contains letters (invalid); contains symbols such as dashes or spaces (invalid); empty (invalid).

---

## Key Takeaways

- Equivalence Partitioning divides inputs into classes that should behave the same and tests one representative from each class. It is the practical answer to "exhaustive testing is impossible".
- Learn the vocabulary: equivalence class, valid partition, invalid partition, representative value, and the equivalence assumption.
- The procedure is: identify inputs, identify rules, partition into valid and invalid classes, pick representatives, create test cases, define expected results. Write expected results from the requirement, before running anything.
- Partitions must not overlap and must not leave gaps. Every possible input belongs to exactly one partition.
- Use the heuristics: ranges (below, in, above), sets (each member if behavior differs, plus not-in-set and nothing-selected), booleans, formats, lengths, character classes, file types. Always add empty.
- Where the rules produce different outputs (grades, shipping tiers, user roles), each output is its own valid partition.
- For multiple fields, avoid the cartesian-product explosion: cover each valid partition at least once (each choice), then test invalid partitions one at a time with all other fields valid, to avoid masking.
- EP coverage = (partitions covered / total partitions) x 100. It reveals false confidence from happy-path-only testing, but it only measures the partitions you identified.
- EP applies to outputs, time, state, and configuration as well as inputs.
- EP and BVA work best together: EP finds class-level defects, BVA finds edge-level defects. For the 18 to 60 age field, EP needs 6 tests, EP plus BVA needs 9, and exhaustive testing needs well over 121.
- EP does not test boundaries, combinations, or state, and it depends on a good requirement. Use the other techniques in today's lessons (error guessing, decision tables, state transition testing) to fill the gaps.
- The most common mistakes are overlapping partitions, missing invalid partitions, mislabeling boundary values as EP, forgetting empty, and combining several invalid inputs in one test.

---

## Additional Resources

- ISTQB Glossary, entry for "equivalence partitioning" (official definitions of EP and related terms): https://glossary.istqb.org/
- ISTQB Certified Tester Foundation Level overview (the syllabus that includes EP, BVA, decision tables, and state transition testing): https://www.istqb.org/certifications/certified-tester-foundation-level
- Guru99, "Equivalence Partitioning and Boundary Value Analysis" (beginner-friendly explanation with examples): https://www.guru99.com/equivalence-partitioning-boundary-value-analysis.html
- Ministry of Testing, articles and community discussion on test design techniques: https://www.ministryoftesting.com/
- pytest documentation on parametrization (for the automation examples in this lesson): https://docs.pytest.org/en/stable/how-to/parametrize.html

Coming up next today: Error Guessing, Decision Tables, and State Transition Testing, which fill in the gaps EP leaves behind.
