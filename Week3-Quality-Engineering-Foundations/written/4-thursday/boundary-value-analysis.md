# Boundary Value Analysis (BVA)

**Week 3 - Quality Engineering Foundations | Thursday: Test Design Techniques**

---

## Learning Objectives

By the end of this lesson, you will be able to:

1. Explain what a boundary is and why defects cluster at the edges of input ranges.
2. Define Boundary Value Analysis (BVA) and place it among the black-box test design techniques.
3. Draw a number line and mark the valid range, the invalid ranges, and the boundaries between them.
4. Apply both 2-value BVA (the ISTQB convention) and 3-value BVA (common industry practice) to the same requirement, and explain the difference.
5. Calculate boundary values for integer, decimal, string-length, date, and time inputs.
6. Handle one-sided ranges, multiple boundaries (price tiers, grade cutoffs), and non-numeric boundaries such as list sizes, file sizes, and login attempts.
7. Distinguish explicit boundaries (stated in the requirement) from implicit boundaries (imposed by data types and systems).
8. Find boundaries in written requirements using a keyword checklist.
9. Write boundary test cases in a clear table format with expected results.
10. Read and run a small Python program in which a deliberate off-by-one defect is exposed by a boundary test suite.
11. Apply BVA to the registration fields of Project 1 (username, password, date of birth, email).
12. Recognise the limitations and common mistakes of BVA.

---

## Why This Matters

Imagine a nightclub with a sign on the door: "Entry for ages 18 and over." The bouncer checks every ID. Now imagine the bouncer was trained slightly wrong: he lets in people who are "over 18" but turns away people who are exactly 18. Nobody notices for months because most customers are 25, 30, or 40 years old. Then one Saturday a group of friends who have just turned 18 arrive, and every one of them is refused. The software equivalent of that bouncer is a single wrong symbol, `>` where `>=` should be, and it is one of the most common defects in the history of software.

This lesson is about finding that kind of defect on purpose, quickly, and cheaply.

Earlier this week you learned an important testing principle: **exhaustive testing is impossible**. A single age field that accepts whole numbers could, in theory, receive millions of different inputs. You cannot test them all, so you must choose a small number of inputs that give you the most information. Black-box test design techniques exist to help you choose well. This morning you learned the black-box overview and use-case testing. Now you learn the technique that gives arguably the best return on effort for any input that has a range: **Boundary Value Analysis**.

Why does it matter to you as a future AI-enabled Test Automation Engineer?

- **It finds real defects.** Experience across the industry shows that a large share of input-related defects sit exactly at the edges of allowed ranges.
- **It is cheap.** For a numeric range, BVA gives you four to six tests instead of thousands.
- **It is automatable.** Boundary tests are simple to script, and later in the programme you will turn them into data-driven automated tests. In this lesson you will even write a tiny Python helper that generates them.
- **It is a core interview and certification topic.** BVA is part of the ISTQB Foundation syllabus and is asked about in nearly every QA interview.
- **It feeds directly into Project 1.** Today's pair-programming exercise asks you to design tests with three techniques for User Registration and Login. BVA will apply to username length, password length, date of birth, and email length.

---

## The Concept

### 1. What is a boundary?

A **boundary** is the edge between two behaviours of the system, the exact place where the software changes its mind. On one side of the boundary the system does one thing (for example, accepts the input); on the other side it does something different (for example, rejects it).

Everyday boundaries are everywhere:

- **A fence:** the boundary between your garden and your neighbour's garden. A gardener makes mistakes near the fence, not in the middle of the lawn.
- **A speed limit:** a road with a 50 km/h limit. Driving at 49 and 50 is allowed. Driving at 51 is not. The interesting moment is the edge, not 20 km/h.
- **A theme park height rule:** "You must be at least 120 cm tall to ride." A child measured at 119 cm is refused. A child at 120 cm may ride. A child at 121 cm may ride. The attendant's measuring stick is exactly a boundary test.
- **An exam pass mark:** 40 marks passes, 39 fails. The student with 39 marks cares very much that the boundary is where the rules say it is.

In software, a boundary is usually a value in a requirement where the rule changes: a minimum, a maximum, a threshold, a limit, a cut-off.

### 2. Why do defects cluster at the edges?

In the Wednesday lesson on testing principles you met **defect clustering**: a small number of modules or areas contain most of the defects. Boundaries are a very specific, very predictable example of that principle. Within a single input range, the defects are not spread evenly. They collect at the edges. There are several reasons.

**Reason 1: Off-by-one errors.** An **off-by-one error** is a defect where a calculation or comparison is wrong by exactly one unit. A loop runs once too many or once too few. A range includes one value too many or one too few. This is by far the most common boundary defect.

**Reason 2: Operator confusion (`<` versus `<=`).** The requirement says "18 or older." The developer writes `age > 18` instead of `age >= 18`. Both look sensible. Both work for every age except exactly 18. The symbols `<`, `<=`, `>`, and `>=` are called **relational operators** (they compare two values), and mixing them up is a classic slip.

**Reason 3: Fence-post errors.** A **fence-post error** is a special kind of off-by-one error that comes from miscounting items versus gaps. Here is the classic puzzle: you want to build a straight fence 30 metres long with a post every 10 metres. How many posts do you need? Many people say 3. The answer is 4, because you need a post at 0 m, 10 m, 20 m, and 30 m. Counting the segments (3) instead of the posts (4) is the fence-post error. In software: "How many days between the 1st and the 30th, inclusive?" The answer is 30 days, not 29 (30 - 1). Anything involving "from X to Y inclusive" invites this slip.

**Reason 4: Ambiguous requirements.** Phrases such as "over 18," "up to 60," "under 100," and "between 1 and 10" can be read in more than one way. The developer, the tester, and the business analyst may each read the boundary differently. Boundary tests expose the disagreement.

**Reason 5: Zero-based versus one-based counting.** Computer programs often start counting from 0 (the first item in a list is at position 0), while people start counting from 1. Mixing these two conventions creates edge-of-range defects.

**Reason 6: Boundaries are written once and copied many times.** The same limit may be validated in the browser (front end), again in the server code (back end), and again in the database. Any one of the three copies can be wrong, and the boundary is where the mismatch shows.

Put simply: if a developer is going to make a mistake with a range, the mistake will almost certainly happen at the edge. So a smart tester looks at the edge first.

### 3. The definition

> **Boundary Value Analysis (BVA)** is a black-box test design technique in which test cases are designed using the values at the boundaries of input (or output) ranges, and the values immediately next to those boundaries.

Let us unpack that definition.

- **Test design technique:** a systematic method for deciding which test inputs to use.
- **Black-box:** you design the tests from the requirements and the visible behaviour, without looking at the code. (You met this idea this morning.)
- **Boundary values:** the exact first and last values of a range.
- **Values next to the boundary:** the closest value on the other side of the edge.

BVA is based on an assumption that has been confirmed over decades of practice: *if the software handles the edge values correctly, it very likely handles the values in the middle correctly too.* The reverse is not true: software can handle the middle perfectly and still fail at the edges.

### 4. The number line, valid ranges, and invalid ranges

The simplest way to see BVA is to draw a **number line**: a straight line on which every possible input is a point. Mark the values that the system should accept (the **valid range**) and the values it should reject (the **invalid ranges**).

Suppose a form accepts an age from 18 to 60 inclusive (the word **inclusive** means the end values are included). Here is the number line:

```
  INVALID (too low)       VALID RANGE                INVALID (too high)
 <---------------------|====================|--------------------->
 ... 14 15 16 17        18 19 ........ 59 60        61 62 63 64 ...
                  ^     ^                  ^   ^
                  |     |                  |   |
              just      lower              upper   just
              outside   boundary           boundary outside
              (invalid) (min, valid)       (max, valid) (invalid)
```

Key vocabulary for this diagram:

- **Valid range** (also called a valid partition): the set of inputs the system should accept. Here: 18 to 60.
- **Invalid ranges**: the sets of inputs the system should reject. Here there are two: everything below 18, and everything above 60.
- **Lower boundary:** the edge at the bottom of the valid range (18).
- **Upper boundary:** the edge at the top of the valid range (60).

> **A note on a term you will meet next.** Dividing the inputs into groups where the system should behave the same way (such as "valid ages" and "too-low ages") is the idea behind **Equivalence Partitioning**. That technique is explained fully in the next lesson. For now you only need the simple picture of one valid range and its invalid neighbours. BVA and Equivalence Partitioning are best used together: Equivalence Partitioning tells you what the groups are, and BVA tells you exactly which values at the edges of each group to test.

Notice that a single range has **two** boundaries (a lower and an upper), and each boundary has a valid side and an invalid side. That gives us four natural values to test: 17, 18, 60, 61. This is the heart of BVA.

### 5. Two flavours: 2-value BVA and 3-value BVA

There are two widely used versions of BVA. Both are correct. They differ only in how many values you pick around each boundary. To make the difference clear we will use the same requirement for both.

**Requirement:** "The age field accepts whole numbers from 18 to 60 inclusive."

#### 2-value BVA (the ISTQB convention)

In **2-value BVA** (sometimes called two-point BVA), each boundary produces **two** test values: the boundary value itself, and its closest neighbour in the adjacent partition (the neighbouring group on the other side of the edge).

- Lower boundary (18): test **18** (the boundary itself, valid) and **17** (the closest neighbour on the other side, invalid).
- Upper boundary (60): test **60** (the boundary itself, valid) and **61** (the closest neighbour on the other side, invalid).

Result: **4 test values: 17, 18, 60, 61.**

```
              17   18                60   61
 <------------ X----X=================X----X ------------>
             invalid  valid range      valid  invalid
```

The logic: the only way the boundary can be implemented wrongly is if the edge itself is on the wrong side. If the edge is shifted by one in either direction, then one of the two values you test (the edge or its outside neighbour) will behave incorrectly. So two values per boundary are enough to detect any "shifted by one" defect.

The ISTQB Foundation syllabus (the international standard for tester certification) describes both variants. Its primary worked approach for the Foundation level is the 2-value version, which is why you should know it by name for the exam.

#### 3-value BVA (common industry practice)

In **3-value BVA** (three-point BVA), each boundary produces **three** test values: the value just below the boundary, the boundary itself, and the value just above the boundary.

- Lower boundary (18): test **17, 18, 19**.
- Upper boundary (60): test **59, 60, 61**.

Result: **6 test values: 17, 18, 19, 59, 60, 61.**

```
              17   18   19          59   60   61
 <------------ X----X----X===========X----X----X ------------>
             invalid   valid range         valid  invalid
```

The extra values (19 and 59) are on the inside of the range. They catch defects that the 2-value approach can miss. For example, a defective program might wrongly treat the first two or last two values as special cases, or an incorrectly written comparison might behave strangely for the value next to the edge. In practice many companies prefer 3-value BVA because the cost of two extra tests is tiny compared to the added confidence.

#### Side-by-side summary

| Aspect | 2-value BVA | 3-value BVA |
|---|---|---|
| Values per boundary | 2 (the boundary and its outside neighbour) | 3 (the neighbour below, the boundary, the neighbour above) |
| Values for 18 to 60 | 17, 18, 60, 61 | 17, 18, 19, 59, 60, 61 |
| Number of tests | 4 | 6 |
| Detects "shifted by one" defects | Yes | Yes |
| Extra coverage | None | Also checks the value just inside each edge |
| Who uses it | ISTQB Foundation primary convention | Very common in industry; considered more thorough |

**Which should you use?** In a certification exam, read the question carefully and use the variant the question names. If it says "2-value" give the four values; if it says "3-value" give the six. In a real project, use 3-value BVA unless time is very tight; if time is tight, 2-value BVA still catches the classic off-by-one defect. In today's pair-programming exercise, state in your test design which variant you are using, so your reviewer knows what to expect.

### 6. How to calculate boundary values

You do not need to guess boundary values. They follow simple formulas. First, you must know the **smallest step** (also called the **precision** or **increment**) of the input: the smallest difference between two valid values. For whole numbers it is 1. For money with two decimal places it is 0.01. For a measurement with one decimal place it is 0.1.

Let `min` be the smallest valid value and `max` the largest valid value, and `step` the smallest increment.

| Value | Formula | Meaning |
|---|---|---|
| Just below min | `min - step` | Invalid (first value outside the bottom edge) |
| Minimum | `min` | Valid (lower boundary) |
| Just above min | `min + step` | Valid (3-value only) |
| Just below max | `max - step` | Valid (3-value only) |
| Maximum | `max` | Valid (upper boundary) |
| Just above max | `max + step` | Invalid (first value outside the top edge) |

#### Integers (whole numbers)

The step is 1.

For 18 to 60: 17, 18, 19, 59, 60, 61.

#### Decimals (numbers with a fractional part)

The step depends on the number of decimal places the field allows.

- One decimal place: step 0.1. For 0.0 to 5.0: -0.1, 0.0, 0.1, 4.9, 5.0, 5.1.
- Two decimal places: step 0.01. For 0.00 to 100.00: -0.01, 0.00, 0.01, 99.99, 100.00, 100.01.

#### String lengths (text)

For text, the "number" you analyse is the **length**: how many characters the text contains. The step is 1 character. For a password of 8 to 16 characters: lengths 7, 8, 9, 15, 16, 17. You build a test string of exactly that length.

Also consider the **empty string** (length 0) as an extra boundary, because "nothing entered" is a special edge case in almost every text field.

#### Dates and times

The step is the smallest unit the system works with: one day for a date field, one minute or one second for a time field. A booking window of "up to 30 days ahead" gives boundaries at day 30 and day 31. Dates have extra subtleties (leap years, month ends, midnight) that we explore in the worked examples below.

### 7. Reading the keywords: finding boundaries in requirements

Boundaries are hidden in the language of the requirement. Train yourself to highlight the following words whenever you read a requirement. Each one signals a boundary and often shows whether the end value is included.

| Word or phrase | Typical meaning | Boundary notes |
|---|---|---|
| minimum, at least, no fewer than, from X | Value must be >= X | X is the lower boundary and is **included** |
| maximum, at most, up to, no more than, not exceeding | Value must be <= X | X is the upper boundary and is **included** |
| between X and Y | Usually X to Y | **Ambiguous:** may or may not include X and Y. Ask! |
| from X to Y | X to Y | Usually inclusive of both |
| less than, under, below, fewer than | Value must be < X | X is **excluded**; the largest valid value is X minus one step |
| more than, over, above, greater than, exceeds | Value must be > X | X is **excluded**; the smallest valid value is X plus one step |
| within | Inside a limit | Usually inclusive, but confirm (for example "within 30 days") |
| before, after | Date or time comparison | Check whether the stated day itself counts |
| older than, younger than | Age comparison | Check whether the exact birthday counts |
| free if, discount when, applies to | Threshold for a rule | Check whether the threshold value itself triggers the rule |
| limit, cap, quota, allowance | A maximum | Include the value at the limit and the first value above it |
| first, last, empty, none, single | List and position edges | Test the first and last position, and an empty collection |

**Golden rule:** whenever the wording is ambiguous ("between 1 and 10"), do not guess. Ask the product owner, business analyst, or developer, and record the answer. A tester who finds an ambiguous boundary has already found a defect, in the requirement, before any code exists. That is the cheapest defect there is. (Recall Tuesday's requirements analysis lesson.)

### 8. Explicit and implicit boundaries

**Explicit boundaries** are stated in the requirement. "Age must be between 18 and 60" has two explicit boundaries.

**Implicit boundaries** are not written in the requirement but still exist because of the way the system is built. Examples:

- **Data type limits.** A whole number stored in 32 bits (a "32-bit signed integer") can hold values from -2,147,483,648 to 2,147,483,647. Add 1 to the maximum and the number "wraps around" or causes an error. A smaller 16-bit signed integer holds -32,768 to 32,767, and an 8-bit signed integer holds -128 to 127.
- **JavaScript numbers.** JavaScript (the language that runs in web browsers) can safely represent whole numbers only up to 9,007,199,254,740,991 (that is 2 to the power 53, minus 1). Beyond that, numbers silently lose precision.
- **Database column limits.** A database column defined as holding 50 characters will reject, cut off, or fail on the 51st.
- **Screen and field limits.** A text box with a `maxlength` of 20 stops typing at the 20th character.
- **File and request limits.** A web server that refuses uploads over 10 MB, or a form that accepts at most 5 attachments.
- **Time limits.** A session that times out after 30 minutes of inactivity.
- **Calendar limits.** Month lengths, leap years, and daylight-saving changes.

Explicit boundaries come from the specification (the "what the system should do" document). Implicit boundaries come from the technology and from system limits. A strong tester tests both. When you find an implicit boundary that matters, raise it with the team so it can be written down and become explicit.

### 9. Worked Example 1: Age field accepting 18 to 60

**Requirement:** "The Age field accepts whole numbers from 18 to 60 inclusive. Any other value must be rejected with the message 'Age must be between 18 and 60'."

**Step 1: identify the ranges.**

- Invalid range 1: 17 and below (too young).
- Valid range: 18 to 60.
- Invalid range 2: 61 and above (too old).

**Step 2: identify the boundaries.** Lower boundary 18, upper boundary 60.

**Step 3: apply the formulas** (step = 1).

**Step 4: write the test cases.**

| TC ID | Input (age) | Boundary tested | 2-value? | 3-value? | Valid or invalid input | Expected result |
|---|---|---|---|---|---|---|
| BVA-AGE-01 | 17 | Just below minimum | Yes | Yes | Invalid | Rejected, message "Age must be between 18 and 60" |
| BVA-AGE-02 | 18 | Minimum | Yes | Yes | Valid | Accepted |
| BVA-AGE-03 | 19 | Just above minimum | No | Yes | Valid | Accepted |
| BVA-AGE-04 | 59 | Just below maximum | No | Yes | Valid | Accepted |
| BVA-AGE-05 | 60 | Maximum | Yes | Yes | Valid | Accepted |
| BVA-AGE-06 | 61 | Just above maximum | Yes | Yes | Invalid | Rejected, message "Age must be between 18 and 60" |

**Explanation of each row:**

- **17** is the first value that is too low. If the program mistakenly uses `age >= 17`, this test wrongly passes the input, and we catch the defect.
- **18** is the lowest legal age. If the program mistakenly uses `age > 18`, this test wrongly rejects a legal customer, and we catch the defect.
- **19** confirms that values immediately inside the lower edge work. It catches rare defects such as a rule that only treats exactly 18 as special.
- **59** confirms the same at the top.
- **60** is the highest legal age. If the program uses `age < 60`, this test wrongly rejects it.
- **61** is the first value that is too high. If the program uses `age <= 61`, this test wrongly accepts it.

**Which defects do these six tests expose?** Any shift of either boundary by one in either direction. That is exactly the family of defects that BVA targets.

You might also add extras that are not strict BVA values but are sensible companions: 0 (zero), -1 (negative), and an empty field. These come from negative testing, which you learned on Wednesday.

### 10. Worked Example 2: Password length 8 to 16 characters

**Requirement:** "The password must be between 8 and 16 characters long (inclusive)."

**Ranges.**

- Invalid: length 0 to 7 (too short).
- Valid: length 8 to 16.
- Invalid: length 17 and above (too long).

**Boundary values (step = 1 character), 3-value:** 7, 8, 9, 15, 16, 17. The 2-value version is 7, 8, 16, 17. We add the empty password (length 0) as an extra edge.

Important: to test the length boundary cleanly, make the password otherwise valid. If the system also demands a capital letter, a digit, and a symbol, include those in every test string, so that a rejection can only be blamed on the length rule.

| TC ID | Password used | Length | Boundary tested | Expected result |
|---|---|---|---|---|
| BVA-PWD-01 | (empty) | 0 | Empty input (extra edge) | Rejected, message "Password is required" |
| BVA-PWD-02 | `Abcde1!` | 7 | Just below minimum | Rejected, message about minimum length |
| BVA-PWD-03 | `Abcdef1!` | 8 | Minimum | Accepted |
| BVA-PWD-04 | `Abcdefg1!` | 9 | Just above minimum | Accepted |
| BVA-PWD-05 | `Abcdefghijklm1!` | 15 | Just below maximum | Accepted |
| BVA-PWD-06 | `Abcdefghijklmn1!` | 16 | Maximum | Accepted |
| BVA-PWD-07 | `Abcdefghijklmno1!` | 17 | Just above maximum | Rejected, message about maximum length (or input prevented at 16) |

**Practical notes.**

- **Counting characters:** Always count your test strings carefully. A common tester error is a test string that is accidentally one character off, which makes the whole test meaningless. Use a character counter or a line of Python (`len("Abcdef1!")` returns 8).
- **Prevented input:** Some forms stop you typing past 16 characters. In that case the "17 characters" test has a different expected result: the 17th character is not accepted into the box, and what the user sees must match the specification. Try pasting a 17-character string as well, because pasting can bypass the typing limit.
- **Characters versus bytes:** A symbol such as an emoji or an accented letter can use more than one byte. A field limited to a number of bytes (rather than characters) may reject a password that looks short enough. This is a hidden boundary that you will meet in the pitfalls section.

### 11. Worked Example 3: Order quantity with price tiers (multiple boundaries)

Real systems often have more than one boundary in a single field, because the field drives more than one rule. This is a very common exam and interview scenario.

**Requirement:** "A customer can order between 1 and 100 units of a product. The unit price is 20.00. Discount rules apply to the whole order:

- 1 to 9 units: no discount.
- 10 to 49 units: 5% discount.
- 50 to 100 units: 10% discount.
- Any quantity outside 1 to 100 is rejected."

**Ranges (partitions).** Invalid (0 and below), 1 to 9, 10 to 49, 50 to 100, and invalid (101 and above). That is five groups and **four** edges between them. Each edge needs its own boundary values.

```
 INVALID      NO DISCOUNT        5% OFF            10% OFF         INVALID
 <-----|=====================|================|==================|----->
      0 | 1 ............ 9 | 10 ......... 49 | 50 .......... 100 | 101
        ^   ^           ^   ^           ^   ^   ^            ^   ^
   edge A  edge B       edge C         edge D     edge E       edge F
```

There are six edge values on a 3-value basis, but when two valid groups touch (for example 9 and 10), the boundaries share neighbours, so the list is compact. The 3-value set is: 0, 1, 2, 9, 10, 11, 49, 50, 51, 99, 100, 101.

| TC ID | Quantity | Which boundary | Expected result | Expected order total |
|---|---|---|---|---|
| BVA-QTY-01 | 0 | Just below overall minimum | Rejected, message "Quantity must be between 1 and 100" | not calculated |
| BVA-QTY-02 | 1 | Overall minimum | Accepted, no discount | 20.00 |
| BVA-QTY-03 | 2 | Just above overall minimum | Accepted, no discount | 40.00 |
| BVA-QTY-04 | 9 | Last quantity with no discount | Accepted, no discount | 180.00 |
| BVA-QTY-05 | 10 | First quantity with 5% discount | Accepted, 5% discount | 190.00 |
| BVA-QTY-06 | 11 | Just above the 5% start | Accepted, 5% discount | 209.00 |
| BVA-QTY-07 | 49 | Last quantity with 5% discount | Accepted, 5% discount | 931.00 |
| BVA-QTY-08 | 50 | First quantity with 10% discount | Accepted, 10% discount | 900.00 |
| BVA-QTY-09 | 51 | Just above the 10% start | Accepted, 10% discount | 918.00 |
| BVA-QTY-10 | 99 | Just below overall maximum | Accepted, 10% discount | 1,782.00 |
| BVA-QTY-11 | 100 | Overall maximum | Accepted, 10% discount | 1,800.00 |
| BVA-QTY-12 | 101 | Just above overall maximum | Rejected, message "Quantity must be between 1 and 100" | not calculated |

**How the totals are calculated (so you can check them yourself):**

- Quantity 9: 9 x 20.00 = 180.00 (no discount).
- Quantity 10: 10 x 20.00 = 200.00, less 5% (10.00) = 190.00.
- Quantity 11: 11 x 20.00 = 220.00, less 5% (11.00) = 209.00.
- Quantity 49: 49 x 20.00 = 980.00, less 5% (49.00) = 931.00.
- Quantity 50: 50 x 20.00 = 1,000.00, less 10% (100.00) = 900.00.
- Quantity 51: 51 x 20.00 = 1,020.00, less 10% (102.00) = 918.00.
- Quantity 99: 99 x 20.00 = 1,980.00, less 10% (198.00) = 1,782.00.
- Quantity 100: 100 x 20.00 = 2,000.00, less 10% (200.00) = 1,800.00.

**A discovery worth reporting.** Look closely: quantity 49 costs 931.00, but quantity 50 costs 900.00. A customer who buys one more item pays 31.00 less. That is not necessarily a defect in the code (the code may correctly follow the rules), but it is a surprising consequence of the business rule that the business might want to know about. Boundary tests often reveal such design questions. Raise them as questions, not accusations.

**Lesson from this example:** the expected result at a boundary includes more than "accepted or rejected." Here, the important output is the *price*. Always write down the exact expected value, calculated by hand or from the specification, before you run the test.

### 12. Worked Example 4: A decimal field (percentage with two decimal places)

**Requirement:** "A discount percentage field accepts values from 0.00 to 100.00 inclusive, with at most two decimal places."

The step is 0.01, so the boundary values are:

| TC ID | Input | Boundary tested | Expected result |
|---|---|---|---|
| BVA-DEC-01 | -0.01 | Just below minimum | Rejected |
| BVA-DEC-02 | 0.00 | Minimum | Accepted |
| BVA-DEC-03 | 0.01 | Just above minimum | Accepted |
| BVA-DEC-04 | 99.99 | Just below maximum | Accepted |
| BVA-DEC-05 | 100.00 | Maximum | Accepted |
| BVA-DEC-06 | 100.01 | Just above maximum | Rejected |

Three extra things to think about with decimals:

1. **The step depends on the precision.** If the field allows only one decimal place, the neighbour of 100.0 is 100.1, not 100.01. If the field allows three decimal places, the neighbour is 100.001. Always confirm how many decimal places are allowed.
2. **What about 100.001 in a two-decimal field?** Extra digits may be rounded, truncated, or rejected. The specification should say which. If it does not, ask. A value like 100.004 might round to 100.00 and be accepted, or be rejected for having too many decimal places. This is a hidden boundary of precision.
3. **Floating-point surprises in code.** Computers store many decimal numbers approximately, in a format called **floating point**. In Python, `0.1 + 0.2` gives `0.30000000000000004` and `0.1 + 0.2 == 0.3` is `False`. A boundary comparison on a floating-point value can therefore fail unexpectedly. Good developers use exact decimal types for money and percentages (in Python, the `decimal.Decimal` type). As a tester, boundary tests on prices and percentages are among the best at exposing this class of defect.

### 13. Worked Example 5: Date and time boundaries

Dates and times are full of boundaries. Before testing them, agree on what "today" is, which time zone is used, and whether the end day counts.

#### Example 5a: "Bookings can be made up to 30 days in advance."

First clarify: does "up to 30 days" include today? Does day 30 itself count? Suppose the specification answers: "A booking date may be from today up to and including today plus 30 days."

Let today be D.

| TC ID | Booking date | Boundary tested | Expected result |
|---|---|---|---|
| BVA-DATE-01 | D - 1 day (yesterday) | Just below minimum (in the past) | Rejected |
| BVA-DATE-02 | D (today) | Minimum | Accepted |
| BVA-DATE-03 | D + 1 day | Just above minimum | Accepted |
| BVA-DATE-04 | D + 29 days | Just below maximum | Accepted |
| BVA-DATE-05 | D + 30 days | Maximum | Accepted |
| BVA-DATE-06 | D + 31 days | Just above maximum | Rejected |

This is a classic fence-post trap: does the 30-day window include 30 or 31 calendar dates? If today counts as day 0, the window "today to today plus 30" contains 31 different dates. Be sure the team agrees.

#### Example 5b: Midnight

A system that says "orders placed before midnight ship the same day" has a time boundary at 00:00. The values to test, using a 24-hour clock with second precision, are:

- 23:59:59 (the last second of the day, the "before midnight" side).
- 00:00:00 (the first second of the next day).
- 00:00:01 (just after).

Also ask which time zone applies. A customer in one time zone may be placing an order when the server's clock already shows the next day. Another hidden boundary: when the clocks change for daylight-saving time, one hour of the local day is repeated or skipped, and a 24-hour rule can misbehave.

#### Example 5c: Leap years

A **leap year** is a year with an extra day, 29 February. The rules are:

- A year divisible by 4 is a leap year (2024 is a leap year);
- except if it is divisible by 100, then it is not a leap year (2100 is not a leap year);
- except if it is also divisible by 400, then it is a leap year (2000 was a leap year).

So: 2000 yes, 2024 yes, 2025 no, 2100 no.

Boundary tests around the end of February:

| Date | Expected | Why it is a boundary |
|---|---|---|
| 28 Feb 2025 | Valid | Last day of February in a non-leap year |
| 29 Feb 2025 | Rejected as a non-existent date | One day past the end of February in a non-leap year |
| 1 Mar 2025 | Valid | First day after |
| 28 Feb 2024 | Valid | Day before the leap day |
| 29 Feb 2024 | Valid | Leap day, exists only in leap years |
| 1 Mar 2024 | Valid | First day after the leap day |
| 29 Feb 2100 | Rejected | Divisible by 100 but not by 400, so not a leap year |
| 29 Feb 2000 | Valid | Divisible by 400, so it is a leap year |

Leap years also interact with the "30 days in advance" rule. If today is 30 January 2024, then today plus 30 days is **29 February 2024** (a valid date because 2024 is a leap year). If today is 30 January 2025, then today plus 30 days is **1 March 2025**, because February 2025 has only 28 days. A defect in date arithmetic might show up in one year but not the other, so test the same rule in both a leap year and a non-leap year.

**Age from a date of birth.** Rules such as "must be 18 or older" use a date of birth, not an age typed in. The boundary is the birthday itself. Suppose today is 7 October 2026. A person born on 7 October 2008 turns 18 today and must be accepted. A person born on 8 October 2008 turns 18 tomorrow and must be rejected. A person born on 6 October 2008 turned 18 yesterday and must be accepted. We will use exactly these values in the Project 1 table later. (A person born on 29 February has a birthday only in leap years; how the system treats that person in other years is a worthwhile question for the team.)

### 14. Worked Example 6: One-sided ranges and system limits

Some rules have only one limit.

**Example: "Users must be 18 or older" (no upper limit stated).**

```
 INVALID                     VALID (no stated upper limit)
 <----------------------|================================> ...
 ... 15 16 17            18 19 20 ...  ... ... ... ... ...
                   ^     ^
              just below minimum    minimum
```

The lower boundary gives the values 17, 18, and 19 (3-value) or 17 and 18 (2-value). There is no stated upper boundary, so no explicit upper test values exist. Even so:

- Can you type 150? 999? 2,147,483,647 (the largest 32-bit signed integer)? 2,147,483,648?
- Is there an implicit upper boundary? A real age cannot be 500, so a sensible system should refuse it, even if the specification forgot to say so. This is a place where a good tester asks, "What is the maximum? Please add it to the specification."
- If the field is stored in a database column of type "tiny integer" (0 to 255), a value of 256 could fail with a server error.

**Example: "A quantity must be at least 1"** (lower boundary only): 0, 1, 2 (3-value), plus the largest quantity the system can handle (an implicit boundary).

**Example: "Maximum 5 items per cart"** (upper boundary only; zero is also the natural lower limit): 4, 5, 6 plus the empty cart (0 items).

**The principle:** one-sided rules still deserve a test of the stated edge, and a tester's curiosity about the other, unstated edge.

### 15. Worked Example 7: Boundaries that are not numbers on a form

BVA is not limited to numbers typed into a box. Anything that has an order and a limit has boundaries. Think of "size" and "count".

#### List sizes (counts of items)

For any collection (a shopping cart, a search result list, a set of attachments), test:

- **Empty:** 0 items. ("Your cart is empty." Does the checkout button correctly disappear?)
- **One:** exactly 1 item. Single-item collections often reveal singular/plural wording bugs ("1 items") and loop errors.
- **Many:** a typical number of items.
- **Maximum:** the largest allowed number (for example 20 items in a cart).
- **Maximum plus one:** 21 items; the system should refuse or warn.

```
  0 items | 1 item | 2 ... 19 items | 20 items | 21 items
  empty   | one    |    many       |  max     | over max
```

#### Search results and pagination

If a page shows 10 results, test with 9, 10, 11 results in total. With 10 results there should be one page; with 11 there should be two pages, and the second page should contain exactly one item. With 0 results there should be a "no results" message.

#### Array and list index

Programs identify items by position, called an **index**. In most programming languages including Python and JavaScript the first item is at index 0. In a list with 5 items the valid indexes are 0 to 4. Asking for index 5 causes an error (in Python, an `IndexError`). Boundary values: index -1 (in Python, that means "the last item"; in other languages it is an error), 0, 4, 5. Black-box testers meet this as the "first item," "last item," and "one past the last item" in the user interface.

#### File sizes

"Uploads must be 5 MB or smaller." Prepare files of 5 MB minus a little, exactly 5 MB, and 5 MB plus a little. Be aware that "MB" can mean 1,000,000 bytes or 1,048,576 bytes depending on who defines it, and this ambiguity itself is a typical boundary defect. Also test a 0-byte (empty) file.

#### Number of login attempts

**Requirement:** "After 3 consecutive failed login attempts, the account is locked."

Here the "input" is the count of failed attempts. First clarify the wording, because "after 3 failed attempts" can be read in two ways. We will use the common reading: the third failed attempt triggers the lock.

| TC ID | Scenario | Boundary | Expected result |
|---|---|---|---|
| BVA-LOCK-01 | 1 failed attempt, then correct password | Well below | Login succeeds, counter resets |
| BVA-LOCK-02 | 2 failed attempts, then correct password | Just below the lock threshold | Login succeeds; account not locked |
| BVA-LOCK-03 | 3 failed attempts | On the threshold | After the third failure the account is locked; message shown |
| BVA-LOCK-04 | 3 failed attempts, then the correct password | Just above the threshold | Login refused because the account is locked |

So the key numbers are 2, 3, and 4 attempts, matching the pattern "below, on, above." Additional boundary questions: does the failed-attempt counter reset after a successful login? After a time period? Does a lock expire after 15 minutes, and what happens at 14:59, 15:00, and 15:01 minutes? Each answer gives a new boundary.

#### Time limits and timeouts

"A one-time passcode expires after 5 minutes." Test at 4:59, 5:00, and 5:01 (minutes:seconds). Clarify whether at exactly 5:00 the code is still valid.

### 16. Boundaries in outputs

So far every boundary was on an **input**. But boundaries also exist on **outputs**, results the system computes. The idea is: design the inputs so that the **output** lands exactly on, just below, and just above a threshold.

**Example: grade cut-offs.** A school program converts a score (0 to 100) to a letter grade:

| Score range | Grade |
|---|---|
| 90 to 100 | A |
| 80 to 89 | B |
| 70 to 79 | C |
| 60 to 69 | D |
| 0 to 59 | F |

The grade is an output, and each cut-off is an edge between two outputs. Inputs that land on each edge: 59 and 60, 69 and 70, 79 and 80, 89 and 90, plus the extremes 0 and 100 (and invalid inputs -1 and 101).

**Example: free shipping threshold.** "Orders of 50.00 or more get free shipping." Input totals 49.99, 50.00, 50.01 test the output "shipping cost" on both sides of its threshold. A second angle: the total itself is computed (items + tax - discount). Build baskets whose computed total is exactly 50.00 (and 49.99, and 50.01), not just baskets whose items add up to something near it. Many defects appear when the total is computed through several steps, and rounding pushes it across the line.

**Example: output limits.** A report shows at most 100 rows. Create data that produces 99, 100, and 101 rows.

The technique is the same: find the thresholds in the output rules, work backwards to find the input that hits each threshold, and test the value on either side of it.

### 17. Single field versus several fields (introduction)

Most forms have more than one field. Registration has username, password, email, date of birth. How do we combine boundaries across fields? Here is an introduction, kept simple.

**Normal BVA (the standard approach).** Test the boundaries of one field at a time while keeping every other field at a **valid, ordinary** ("nominal") value. For a form with n fields, each with a 2-value approach, you get 4 tests per field, a total of 4n, rather than all possible combinations. Each test then has exactly one unusual input, so if it fails you know which field caused it.

**Robust BVA (a step further).** Normal BVA concentrates on values at and just inside the valid range (and the first value outside, in the versions above). **Robust** BVA also deliberately includes values just beyond the limits in the invalid direction, as extra "beyond the edge" cases such as -1, 0 on one side and max+1, max+2 or extreme values on the other. At the introductory level, think of robust BVA as "normal BVA, plus invalid values just outside each boundary." It tests how well the system handles bad data. Since we already include the first invalid value in both 2-value and 3-value approaches in this lesson, you can think of robust BVA as the habit of also trying clearly absurd values (such as negative numbers or huge numbers) at the same boundary.

**Worst-case combination warning.** A more demanding variant, **worst-case** testing, combines the boundary values of *all* fields together. With 2 fields and 5 values each that is 25 tests; with 4 fields and 5 values each it is 625; with 10 fields it is nearly 10 million. The number explodes. This is the exhaustive-testing trap again. Worst-case combination testing is worthwhile only for a handful of high-risk fields. For everything else, use normal BVA (one field at a time) and rely on other techniques later today, such as decision tables, to handle important combinations of rules.

```
 Fields  | Values per field | Worst-case combinations
 --------+------------------+------------------------
   2     |        5         |           25
   3     |        5         |          125
   4     |        5         |          625
   6     |        5         |       15,625
  10     |        5         |    9,765,625
```

### 18. The test case table format

A boundary test is only as good as its documentation. A clear test case answers: what is being tested, what do I enter, and what must happen? Use this layout (you practised similar tables in Tuesday's test planning lesson):

| Column | Purpose |
|---|---|
| TC ID | A unique, traceable identifier (for example BVA-AGE-01) |
| Requirement or field | Which rule or field the test relates to |
| Boundary description | Which edge is tested (for example "just below minimum") |
| Test data (input) | The exact value or string to enter |
| Precondition | State needed before the test (for example "user is on the registration page") |
| Expected result | The precise outcome: accepted or rejected, the exact message, the computed value |
| Actual result | Filled in at execution |
| Status | Pass or Fail |

Tips for good expected results:

- Write the exact message or value, not just "error."
- Mention what must **not** happen (no account created, no record saved).
- When the expected result depends on an ambiguous requirement, mark the test "Blocked pending clarification" rather than guessing.
- Keep one boundary per test. Do not combine two edges in a single test; if it fails, you will not know why.

### 19. A Python demonstration: exposing an off-by-one defect

Now let us see BVA catching a real defect, in code. You do not need to be a Python expert; the code is short, and every line is explained afterwards. If you want to run it, save it as `bva_demo.py` and run `python bva_demo.py` (you need Python 3.8 or later).

The program contains:

- `is_valid_age_buggy(age)` and `calculate_grade_buggy(score)`, each with a **deliberate off-by-one defect** (a wrong comparison operator).
- Fixed versions of both functions.
- A tiny helper, `boundary_values(...)`, that **generates** boundary values from a minimum and a maximum.
- A small test runner that prints PASS or FAIL for each boundary test.

```python
"""Boundary Value Analysis demo: a buggy function, a boundary test suite, and the fix."""

MIN_AGE = 18
MAX_AGE = 60


def is_valid_age_buggy(age):
    """Spec: ages 18 to 60 inclusive are valid. DEFECT: uses < instead of <= at the lower edge."""
    return MIN_AGE < age <= MAX_AGE


def is_valid_age(age):
    """Fixed version."""
    return MIN_AGE <= age <= MAX_AGE


def calculate_grade_buggy(score):
    """Spec: 90-100 A, 80-89 B, 70-79 C, 60-69 D, 0-59 F. DEFECT: A uses > instead of >=."""
    if score > 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def calculate_grade(score):
    """Fixed version."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def boundary_values(minimum, maximum, step=1, three_value=True):
    """Return a list of (value, expected_validity, label) for an inclusive range."""
    cases = [
        (minimum - step, False, "just below min"),
        (minimum, True, "min"),
        (maximum, True, "max"),
        (maximum + step, False, "just above max"),
    ]
    if three_value:
        cases.insert(2, (minimum + step, True, "just above min"))
        cases.insert(3, (maximum - step, True, "just below max"))
    return cases


def run_suite(title, func, cases):
    print(f"--- {title} ---")
    failures = 0
    for value, expected, label in cases:
        actual = func(value)
        status = "PASS" if actual == expected else "FAIL"
        if status == "FAIL":
            failures += 1
        print(f"{status}  input={value!s:>3}  expected={expected!s:<5}  actual={actual!s:<5}  ({label})")
    print(f"Result: {len(cases) - failures} passed, {failures} failed\n")
    return failures


GRADE_CASES = [
    (-1, "invalid"), (0, "F"), (59, "F"), (60, "D"), (69, "D"), (70, "C"),
    (79, "C"), (80, "B"), (89, "B"), (90, "A"), (100, "A"),
]


def run_grade_suite(title, func):
    print(f"--- {title} ---")
    failures = 0
    for score, expected in GRADE_CASES:
        if expected == "invalid":
            continue
        actual = func(score)
        status = "PASS" if actual == expected else "FAIL"
        failures += status == "FAIL"
        print(f"{status}  score={score:>3}  expected={expected}  actual={actual}")
    print(f"Result: {len(GRADE_CASES) - 1 - failures} passed, {failures} failed\n")


if __name__ == "__main__":
    print(boundary_values(18, 60))
    print()
    cases = boundary_values(MIN_AGE, MAX_AGE)
    run_suite("is_valid_age_buggy", is_valid_age_buggy, cases)
    run_suite("is_valid_age (fixed)", is_valid_age, cases)
    run_grade_suite("calculate_grade_buggy", calculate_grade_buggy)
    run_grade_suite("calculate_grade (fixed)", calculate_grade)
```

#### Line-by-line explanation

**The header and constants**

- `"""Boundary Value Analysis demo: ..."""` is a **docstring**: a text description of the file, written in triple quotes. It is documentation, not an instruction to the computer.
- `MIN_AGE = 18` and `MAX_AGE = 60` create two **constants**: named values that never change. By convention constants are written in capital letters. Naming the boundaries once means they are not repeated as "magic numbers" throughout the code.

**The buggy age function**

- `def is_valid_age_buggy(age):` defines a function (a reusable block of code) named `is_valid_age_buggy` that takes one input called `age`.
- The docstring states the specification the function is supposed to follow, and where the defect is.
- `return MIN_AGE < age <= MAX_AGE` gives back `True` or `False`. Python lets you chain comparisons. This line means "18 is less than age, and age is less than or equal to 60." The first operator is `<` where the specification (18 inclusive) needs `<=`. So age 18 produces `False`. That is the **off-by-one defect**.

**The fixed age function**

- `return MIN_AGE <= age <= MAX_AGE` uses `<=` at both ends, meaning "18 is less than or equal to age, and age is less than or equal to 60." It matches the specification exactly.

**The buggy grade function**

- `def calculate_grade_buggy(score):` takes a score and returns a letter.
- `if score > 90:` is the defect. The specification says 90 and above earns an A, so this must be `>=`. A score of exactly 90 is not greater than 90, so it falls through to the next check.
- `return "A"` returns the letter A when the condition is true.
- `if score >= 80:` ... `return "B"`: if the score has not already been caught by the first check and is at least 80, the grade is B. The checks are made from the top down, so by the time Python reaches a given line, all higher grades have already been ruled out. That is why each line only needs to test the lower edge.
- The same pattern repeats for C (70) and D (60).
- `return "F"` is the default: any score that reaches the end is below 60.
- The buggy function's score-90 problem shows up as a B rather than an A, a "wrong grade" defect that would affect real students.

**The fixed grade function**

- Identical, except `if score >= 90:`. This is the one-character fix (adding `=`).

**The boundary-value generator**

- `def boundary_values(minimum, maximum, step=1, three_value=True):` defines a helper. `step=1` and `three_value=True` are **default values**: if the caller does not supply them, the function assumes a step of 1 and the 3-value method.
- The docstring explains what it returns: a list of tuples (small fixed groups of values) containing the input value, whether it should be valid, and a label.
- `cases = [ ... ]` builds a list of the four 2-value cases. `(minimum - step, False, "just below min")` means: the value one step below the minimum, expected to be invalid (`False`), labelled for readability. `(minimum, True, "min")` is the minimum itself, which should be valid (`True`). The next two lines do the same for the maximum and one step above it.
- `if three_value:` runs the next lines only when the 3-value option is chosen.
- `cases.insert(2, (minimum + step, True, "just above min"))` inserts the value just above the minimum at position 2 in the list. List positions start at 0, so position 2 is the third item, right after the minimum. Now the list reads: below min, min, above min, max, above max.
- `cases.insert(3, (maximum - step, True, "just below max"))` inserts the value just below the maximum at position 3, between "just above min" and "max". Final order from lowest to highest: just below min, min, just above min, just below max, max, just above max.
- `return cases` gives the list back to the caller.

**The test runner**

- `def run_suite(title, func, cases):` takes a title for the report, a function to test (`func`; in Python a function can be passed around like any other value), and the list of cases.
- `print(f"--- {title} ---")` prints a heading. The `f` before the quotes makes it an **f-string**, in which values inside curly braces `{}` are inserted into the text.
- `failures = 0` starts a counter of failed tests.
- `for value, expected, label in cases:` loops over the list; each time it unpacks one tuple into three variables.
- `actual = func(value)` calls the function under test with the input and stores the result. This is the "execute the test" step.
- `status = "PASS" if actual == expected else "FAIL"` compares the actual result with the expected result (`==` means "is equal to") and picks the word.
- `if status == "FAIL": failures += 1` adds one to the failure counter when a test fails.
- The long `print(f"...")` line formats one report row. `{value!s:>3}` converts the value to text and right-aligns it in a space three characters wide; `{expected!s:<5}` left-aligns in five characters. This only keeps the columns tidy.
- The final `print` shows how many tests passed (total minus failures) and failed. `\n` adds a blank line.
- `return failures` hands back the failure count (useful later when you want a script to signal an overall failure).

**The grade test data and runner**

- `GRADE_CASES = [ ... ]` is a list of (score, expected grade) pairs. They are exactly the boundary values of the grade table: the lowest and highest score of each band (0, 59, 60, 69, 70, 79, 80, 89, 90, 100). The entry `(-1, "invalid")` is a placeholder to remind us that an out-of-range score exists; the runner skips it because these simple grade functions do not validate their input.
- `run_grade_suite` works like `run_suite`, but compares letters. `if expected == "invalid": continue` skips the placeholder. `failures += status == "FAIL"` adds 1 when the comparison is true (Python treats `True` as 1 and `False` as 0). The final line prints the totals; `len(GRADE_CASES) - 1` removes the skipped placeholder from the count.

**The main block**

- `if __name__ == "__main__":` means "run the following only when this file is executed directly." It is a standard Python habit.
- `print(boundary_values(18, 60))` shows the generated list so you can see the helper's output.
- `cases = boundary_values(MIN_AGE, MAX_AGE)` generates the six 3-value cases for ages 18 to 60.
- The next two lines run the same cases against the buggy and the fixed function. Reusing the same test data on both versions is exactly how a regression test works.
- The last two lines run the grade suites for the buggy and fixed versions.

#### Expected output

When you run the program, you should see exactly this:

```
[(17, False, 'just below min'), (18, True, 'min'), (19, True, 'just above min'), (59, True, 'just below max'), (60, True, 'max'), (61, False, 'just above max')]

--- is_valid_age_buggy ---
PASS  input= 17  expected=False  actual=False  (just below min)
FAIL  input= 18  expected=True   actual=False  (min)
PASS  input= 19  expected=True   actual=True   (just above min)
PASS  input= 59  expected=True   actual=True   (just below max)
PASS  input= 60  expected=True   actual=True   (max)
PASS  input= 61  expected=False  actual=False  (just above max)
Result: 5 passed, 1 failed

--- is_valid_age (fixed) ---
PASS  input= 17  expected=False  actual=False  (just below min)
PASS  input= 18  expected=True   actual=True   (min)
PASS  input= 19  expected=True   actual=True   (just above min)
PASS  input= 59  expected=True   actual=True   (just below max)
PASS  input= 60  expected=True   actual=True   (max)
PASS  input= 61  expected=False  actual=False  (just above max)
Result: 6 passed, 0 failed

--- calculate_grade_buggy ---
PASS  score=  0  expected=F  actual=F
PASS  score= 59  expected=F  actual=F
PASS  score= 60  expected=D  actual=D
PASS  score= 69  expected=D  actual=D
PASS  score= 70  expected=C  actual=C
PASS  score= 79  expected=C  actual=C
PASS  score= 80  expected=B  actual=B
PASS  score= 89  expected=B  actual=B
FAIL  score= 90  expected=A  actual=B
PASS  score=100  expected=A  actual=A
Result: 9 passed, 1 failed

--- calculate_grade (fixed) ---
PASS  score=  0  expected=F  actual=F
PASS  score= 59  expected=F  actual=F
PASS  score= 60  expected=D  actual=D
PASS  score= 69  expected=D  actual=D
PASS  score= 70  expected=C  actual=C
PASS  score= 79  expected=C  actual=C
PASS  score= 80  expected=B  actual=B
PASS  score= 89  expected=B  actual=B
PASS  score= 90  expected=A  actual=A
PASS  score=100  expected=A  actual=A
Result: 10 passed, 0 failed
```

#### What the output teaches

1. **Only one test in each buggy suite fails, and it is the boundary test.** For the age function, the failing input is **18**, the minimum. For the grade function, the failing input is **90**, the lowest score of the A band. Every test in the middle of the range passes. If you had tested only "typical" ages such as 25 or 40, or typical scores such as 75 or 95, the program would have appeared perfect.
2. **The failure message points straight to the defect.** "Input 18, expected True, actual False" immediately tells a developer to look at how the lower limit is compared.
3. **The fix is one character** (`<` to `<=`, and `>` to `>=`), yet without boundary testing it could have reached real users.
4. **Re-running the same suite after the fix** shows all tests passing: a small example of regression testing.
5. **The helper removes guesswork.** Calling `boundary_values(MIN_AGE, MAX_AGE)` always produces the correct edge values. Change the two constants and the test data updates automatically.

Try this yourself: change `MAX_AGE` to 65 and re-run. Notice that the generated values change to 17, 18, 19, 64, 65, 66 with no further edits.

One more remark about decimals. The helper above uses plain numbers, which is fine for whole numbers. For money and percentages, use Python's `Decimal` type, because floating-point arithmetic is approximate:

```python
from decimal import Decimal

def decimal_boundaries(minimum, maximum, step="0.01"):
    lo, hi, st = Decimal(minimum), Decimal(maximum), Decimal(step)
    return [lo - st, lo, lo + st, hi - st, hi, hi + st]

print([str(v) for v in decimal_boundaries("0.00", "100.00")])
```

This prints `['-0.01', '0.00', '0.01', '99.99', '100.00', '100.01']`, exactly the six values from Worked Example 4. Passing the numbers as text such as `"0.01"` is deliberate: it avoids creating inexact floating-point numbers in the first place.

### 20. BVA applied to Project 1: User Registration

Project 1 is a sample web app with User Registration and Login. Let us apply BVA to the registration form. For this exercise we assume the following requirement (if the real specification in the project differs, use the real one and update the table):

| Field | Rule |
|---|---|
| Username | 3 to 20 characters; letters, digits, and underscore only |
| Password | 8 to 16 characters (plus complexity rules, which are tested separately) |
| Date of birth | User must be 18 years or older on the day of registration |
| Email | Valid format; total length from 6 to 100 characters |

**Preparation tips.**

- For each length test, build otherwise-valid data, so only the length rule can cause a rejection. For example, a username of 3 characters is `abc`; a 20-character username is `abcdefghijklmnopqrst`; a 21-character one is `abcdefghijklmnopqrstu`.
- For the 100-character email, create a local part (the text before `@`) of 88 characters followed by `@example.com` (12 characters), giving exactly 100. Check with a character counter. For 101 characters, use 89.
- For the date of birth, assume today is **7 October 2026**. Always recalculate the dates relative to the day you actually run the test.
- Use unique usernames and emails for each valid test, because duplicate accounts are rejected for a different reason.

**Complete test case table (3-value BVA, with a few extra edge cases).**

| TC ID | Field | Test data | Boundary tested | Expected result |
|---|---|---|---|---|
| TC-REG-BVA-01 | Username | (empty) | Empty input | Rejected: "Username is required" |
| TC-REG-BVA-02 | Username | `ab` (length 2) | Just below minimum | Rejected: username too short |
| TC-REG-BVA-03 | Username | `abc` (length 3) | Minimum | Accepted |
| TC-REG-BVA-04 | Username | `abcd` (length 4) | Just above minimum | Accepted |
| TC-REG-BVA-05 | Username | `abcdefghijklmnopqrs` (length 19) | Just below maximum | Accepted |
| TC-REG-BVA-06 | Username | `abcdefghijklmnopqrst` (length 20) | Maximum | Accepted |
| TC-REG-BVA-07 | Username | `abcdefghijklmnopqrstu` (length 21) | Just above maximum | Rejected: username too long (or input stops at 20 characters) |
| TC-REG-BVA-08 | Password | (empty) | Empty input | Rejected: "Password is required" |
| TC-REG-BVA-09 | Password | `Abcde1!` (length 7) | Just below minimum | Rejected: password too short |
| TC-REG-BVA-10 | Password | `Abcdef1!` (length 8) | Minimum | Accepted |
| TC-REG-BVA-11 | Password | `Abcdefg1!` (length 9) | Just above minimum | Accepted |
| TC-REG-BVA-12 | Password | `Abcdefghijklm1!` (length 15) | Just below maximum | Accepted |
| TC-REG-BVA-13 | Password | `Abcdefghijklmn1!` (length 16) | Maximum | Accepted |
| TC-REG-BVA-14 | Password | `Abcdefghijklmno1!` (length 17) | Just above maximum | Rejected: password too long (or input stops at 16 characters) |
| TC-REG-BVA-15 | Date of birth | 6 Oct 2008 (turned 18 yesterday) | Just above minimum age | Accepted |
| TC-REG-BVA-16 | Date of birth | 7 Oct 2008 (turns 18 today) | Exact minimum age | Accepted |
| TC-REG-BVA-17 | Date of birth | 8 Oct 2008 (turns 18 tomorrow) | Just below minimum age | Rejected: "You must be at least 18" |
| TC-REG-BVA-18 | Date of birth | Tomorrow's date (8 Oct 2026) | Date in the future (implicit boundary) | Rejected: invalid date of birth |
| TC-REG-BVA-19 | Date of birth | 29 Feb 2025 | Non-existent date (2025 is not a leap year) | Rejected: invalid date |
| TC-REG-BVA-20 | Email | `a@b.co` (length 6) | Minimum length | Accepted (if otherwise valid) |
| TC-REG-BVA-21 | Email | `a@b.c` (length 5) | Just below minimum | Rejected (note: may also fail for the format rule; clarify) |
| TC-REG-BVA-22 | Email | 88 letters + `@example.com` (length 100) | Maximum length | Accepted |
| TC-REG-BVA-23 | Email | 87 letters + `@example.com` (length 99) | Just below maximum | Accepted |
| TC-REG-BVA-24 | Email | 89 letters + `@example.com` (length 101) | Just above maximum | Rejected: email too long |

**Notes on the table.**

- In the date-of-birth tests, rows 15 and 16 are both valid; the boundary is between rows 16 and 17. The important pair is 7 Oct 2008 (accepted) and 8 Oct 2008 (rejected), exactly one day apart.
- Rows 18 and 19 are not strictly on the 18-year boundary; they are implicit boundaries of the date input itself.
- Row 21: a 5-character email such as `a@b.c` would probably be rejected anyway for having a one-letter domain ending. If the system rejects it, check the message. Does it say "too short" or "invalid format"? Report any mismatch with the specification.
- Each of these tests can later be converted into an automated, data-driven test where the input and expected result come from this table. That is an excellent bridge to the automation topics later in the programme.
- Also consider a login equivalent: a lock after 3 failed attempts (see Section 15), where you would test 2, 3, and 4 failed attempts.

### 21. How BVA combines with other techniques

BVA is rarely used alone.

- **With Equivalence Partitioning (next lesson).** Equivalence Partitioning splits the inputs into groups that the system should treat the same way, so you need only one typical test per group. BVA then adds extra tests exactly at the edges between the groups, where defects cluster. The two are best used together: partitioning for broad coverage with few tests, boundaries for sharp coverage where bugs hide. The next lesson explains Equivalence Partitioning in full, including how to combine it with the BVA you learned here.
- **With decision tables (later today).** BVA tests the edges of one input at a time. Decision tables handle combinations of conditions and the business rules that depend on them. The inputs that go into a decision table can be chosen using BVA.
- **With state transition testing and error guessing (later today).** The "3 failed login attempts" example is really a state change (unlocked to locked), and state transition testing treats it systematically. Error guessing is the experience-based habit of asking "where might the developer have slipped?", and the first answer is nearly always "at the edges."
- **With use-case testing (earlier today).** Use cases describe the flow of user actions. BVA supplies the precise data values for the steps in those flows, for example the age to type into the form during "register new user."

### 22. Limitations and pitfalls

BVA is powerful but not magical.

1. **It works only for ordered ranges.** You need inputs that can be placed on a line, such as numbers, lengths, dates, and counts. It does not apply to unordered choices such as a list of countries, a payment type (card, bank transfer, wallet), or a yes/no checkbox. Other techniques cover those.
2. **It ignores combinations.** Testing each field's boundaries separately does not reveal defects that occur only when two fields interact (for example, "under 21 and ordering alcohol"). Use decision tables and pairwise-style thinking for that.
3. **It needs a correct specification.** If the requirement says 18 but the business meant 21, BVA will faithfully test the wrong edge. Review the requirements; ask questions about every unclear boundary.
4. **Hidden boundaries.** Some limits are not in the specification: data type sizes, byte limits versus character limits, database column widths, timeouts, memory, and rounding. A tester who checks only the documented edges will miss them. Ask developers and architects what the technical limits are.
5. **The step size must be right.** For decimals, using 1 instead of 0.01 misses the actual neighbours. For dates, using weeks instead of days misses the edge.
6. **It does not tell you everything is fine in the middle.** BVA assumes the middle works if the edges work. Combine it with at least one typical value (a "nominal" value) from Equivalence Partitioning to cover that assumption.
7. **Multiple conditions on one field can hide each other.** If a password must be 8 to 16 characters and contain a digit, a test with an 8-character password without a digit is rejected for the wrong reason, and it does not test the length boundary at all. Always keep other rules satisfied when testing one rule.
8. **Front-end-only testing misses back-end boundaries.** A browser form may stop you typing beyond 20 characters, but the server may still accept 21 characters sent by another route. Boundary-test the application programming interface (API, the way programs talk to the server) later as well.

### 23. Common mistakes

| Mistake | Why it is a problem | Better practice |
|---|---|---|
| Testing only the middle of the range | Misses the places where defects cluster | Always include both edges |
| Testing only the valid side of a boundary | Misses defects that wrongly accept invalid values | Test the invalid neighbour as well |
| Guessing at ambiguous wording ("between 1 and 10") | You may test the wrong edge | Ask, and record the answer |
| Using the wrong step size for decimals or dates | The "just outside" value is not actually the closest | Confirm the precision of the field |
| Miscounting test strings | A password of 9 characters is mistaken for 8 | Use a character counter or a code check |
| Breaking another rule in the same test | The failure cannot be blamed on the boundary | Keep all other fields and rules valid |
| Forgetting the empty value | Empty input is a special boundary | Add an "empty" test |
| Writing "error" as the expected result | Not precise enough to decide pass or fail | State the exact message, value, or behaviour |
| Skipping output boundaries | Thresholds such as free shipping are missed | Work backwards from output thresholds |
| Ignoring implicit boundaries | Data type and system limits are missed | Ask about limits in the technology |
| Testing all combinations of boundaries | Test count explodes | One field at a time, with nominal values for the others |
| Using today's date in a table and never updating it | Date tests become wrong after a day | Express dates relative to today |
| Assuming the user interface enforces the limit | The back end may still accept the bad value | Test the server rule too |

---

## Examples

To consolidate, here are three quick "spot the boundaries" examples.

**Example A: Requirement.** "A user may upload up to 5 photos."
Number line: 0 (none), 1 ... 5 valid, 6 invalid. Boundary values (3-value on the upper edge): 4, 5, 6. Plus 0 (the empty case) and 1 (the single item).

**Example B: Requirement.** "Passengers under 12 travel at the child fare."
"Under 12" means ages less than 12, so 11 is the largest child age and 12 is the first adult age. Boundary values: 11 (child), 12 (not child). The 3-value set is 10, 11, 12 and 11, 12, 13. A careless reader would put the boundary at 12 inclusive. The word **under** makes 12 *excluded*.

**Example C: Requirement.** "Free shipping on orders over 50.00."
"Over" means strictly greater than, so 50.00 itself is *not* free, and 50.01 is the first free value. Boundary values: 49.99, 50.00, 50.01. Compare with "50.00 or more," where 50.00 would qualify. A single word changes which side of the line the boundary value is on.

---

## Try It: Boundary Tests for Project 1 (Pair Activity)

This is a short, hands-on activity you can complete in your pairs during today's pair-programming session. It prepares you for the main exercise, where you will design tests with three techniques and cross-review each other's work.

**Time:** about 30 minutes.

**Roles:** one partner is the **Driver** (writes the test table), the other is the **Navigator** (reads the requirement aloud and checks every value). Swap roles halfway.

**Steps.**

1. Open the Project 1 registration requirements (or use the assumptions from Section 20 if the specification does not give exact limits).
2. For **each** of the four fields (username, password, date of birth, email), write down:
   - the explicit boundaries from the requirement,
   - at least one implicit boundary (for example a database column size, a `maxlength` attribute, or an unrealistic date),
   - any ambiguous wording that you would send back as a question.
3. Draw a number line for each field. Mark the valid and invalid ranges and circle the boundary values.
4. Decide on 2-value or 3-value BVA, and note why you chose it.
5. Produce a test case table with these columns: TC ID, Field, Test data, Boundary tested, Expected result. Aim for at least 20 rows.
6. Add one boundary test for the login lock after 3 failed attempts (2, 3, and 4 attempts).
7. Swap tables with your partner pair. Review each other's tables with this checklist:
   - Are the boundary values calculated correctly (right step size, right inclusive or exclusive reading)?
   - Is every test string the correct length?
   - Is the expected result specific?
   - Are other fields valid in each test?
   - Are there missing edges, for example empty input or future dates?
8. Run a selection of your tests against the actual Project 1 application. For every unexpected result, write a defect report using the structure from Tuesday's defect lifecycle lesson (summary, steps to reproduce, expected result, actual result, severity).

**Stretch goal:** write a short Python function `is_valid_username(name)` that implements the 3 to 20 rule, deliberately introduce an off-by-one defect, and use the `boundary_values` helper from Section 19 (applied to the length) to expose it.

---

## Practice Exercises

Attempt each exercise before looking at the answer key. For each one, state whether you use 2-value or 3-value BVA.

**Exercise 1: Integer field.** A quantity-of-tickets field accepts whole numbers from 1 to 10 inclusive. List the 2-value and 3-value boundary values, and say which are valid.

**Exercise 2: Username length.** A username must be between 5 and 15 characters long inclusive. List the 3-value boundary lengths and add the empty input.

**Exercise 3: Decimal field.** A product rating accepts values from 0.0 to 5.0 inclusive, with one decimal place. List the 3-value boundary values.

**Exercise 4: Age bracket pricing.** A museum charges by age. The age field accepts whole numbers from 0 to 120. Ages 0 to 12 pay the child price, ages 13 to 17 the teen price, ages 18 to 64 the adult price, and ages 65 and above (up to 120) the senior price. List the 2-value boundary values for every boundary, mark each as valid or invalid, and state which price applies.

**Exercise 5: Shipping weight.** A courier accepts parcels with weights greater than 0 kg and up to 30.00 kg, measured to two decimal places. Prices: 0.01 to 0.50 kg costs 5.00; 0.51 to 2.00 kg costs 8.00; 2.01 to 10.00 kg costs 15.00; 10.01 to 30.00 kg costs 30.00. Anything else is rejected. List the 2-value boundary values for every boundary with expected results.

**Exercise 6: Grade cut-offs.** A course marks out of 50: 40 to 50 is Distinction, 30 to 39 is Merit, 20 to 29 is Pass, 0 to 19 is Fail. Whole marks only. List the boundary values and the expected grades, including the invalid inputs.

**Exercise 7: Reading the wording.** For each requirement, give the first valid value and the first invalid value at the boundary:
(a) "Discount applies to orders of more than 100 items."
(b) "Maximum 8 guests per table."
(c) "Applicants must be younger than 65."
(d) "Free delivery for orders of 30.00 or more."

**Exercise 8: Login lockout.** An account is locked after 5 consecutive failed login attempts. List the boundary scenarios and expected results.

**Exercise 9: Time boundary.** A one-time passcode (OTP) is valid for 5 minutes (300 seconds) after it is sent. The specification says "valid for up to and including 5 minutes." List the boundary times and expected results.

**Exercise 10: Find the defect.** A developer wrote the following validation for "quantity from 1 to 100 inclusive": `if quantity > 1 and quantity < 100: accept`. Which boundary values reveal the defect(s), and what does each test show?

---

## Practice Exercises: Answer Key

**Answer 1.** Valid range 1 to 10; step 1.
- 2-value: 0 (invalid), 1 (valid), 10 (valid), 11 (invalid).
- 3-value: 0 (invalid), 1 (valid), 2 (valid), 9 (valid), 10 (valid), 11 (invalid).

**Answer 2.** Valid lengths 5 to 15.
- 3-value: 4 (invalid), 5 (valid), 6 (valid), 14 (valid), 15 (valid), 16 (invalid).
- Extra: 0 characters (empty, invalid; "Username is required").

**Answer 3.** Step is 0.1, valid range 0.0 to 5.0.
- 3-value: -0.1 (invalid), 0.0 (valid), 0.1 (valid), 4.9 (valid), 5.0 (valid), 5.1 (invalid).
- Extra thought: what happens with 5.05 (two decimals in a one-decimal field)? Clarify whether it is rounded or rejected.

**Answer 4.** Boundaries: invalid/child at 0, child/teen at 12/13, teen/adult at 17/18, adult/senior at 64/65, and senior/invalid at 120/121.

| Input | Valid? | Price applied |
|---|---|---|
| -1 | Invalid | Rejected |
| 0 | Valid | Child |
| 12 | Valid | Child |
| 13 | Valid | Teen |
| 17 | Valid | Teen |
| 18 | Valid | Adult |
| 64 | Valid | Adult |
| 65 | Valid | Senior |
| 120 | Valid | Senior |
| 121 | Invalid | Rejected |

That is 10 values. For 3-value BVA add the neighbour inside each band, for example 1, 11, 14, 16, 19, 63, 66, and 119. Notice that 12 and 13 are both valid, and the boundary is the *switch* between two prices.

**Answer 5.** Boundaries: 0 (invalid) to 0.01 (first valid), 0.50 to 0.51 (band change), 2.00 to 2.01, 10.00 to 10.01, and 30.00 to 30.01 (upper limit). Weight must be greater than zero, so 0.00 is invalid.

| Weight (kg) | Expected result |
|---|---|
| 0.00 | Rejected |
| 0.01 | Accepted, price 5.00 |
| 0.50 | Accepted, price 5.00 |
| 0.51 | Accepted, price 8.00 |
| 2.00 | Accepted, price 8.00 |
| 2.01 | Accepted, price 15.00 |
| 10.00 | Accepted, price 15.00 |
| 10.01 | Accepted, price 30.00 |
| 30.00 | Accepted, price 30.00 |
| 30.01 | Rejected |

That is 10 values for 2-value BVA. For 3-value BVA, also test 0.02, 0.49, 0.52, 1.99, 2.02, 9.99, 10.02, and 29.99. Also test -0.01 (a negative weight) as a negative case. Note the step is 0.01 because of the two-decimal precision.

**Answer 6.** Whole marks, 0 to 50. Boundaries between bands: 19/20, 29/30, 39/40, plus the range limits 0 and 50.

| Mark | Expected result |
|---|---|
| -1 | Invalid, rejected |
| 0 | Fail |
| 19 | Fail |
| 20 | Pass |
| 29 | Pass |
| 30 | Merit |
| 39 | Merit |
| 40 | Distinction |
| 50 | Distinction |
| 51 | Invalid, rejected |

Add 1 and 49 for 3-value coverage at the extremes. A common mistake is to forget that -1 and 51 are invalid inputs and not Fail and Distinction.

**Answer 7.**
- (a) "More than 100": first valid (discount applies) = 101; the first value that does not qualify = 100. So test 100 and 101.
- (b) "Maximum 8": first valid at the limit = 8; first invalid = 9. Test 8 and 9.
- (c) "Younger than 65": largest valid age = 64; first invalid = 65. Test 64 and 65.
- (d) "30.00 or more": smallest qualifying value = 30.00; first non-qualifying = 29.99. Test 29.99 and 30.00.

**Answer 8.** Test 4, 5, and 6 attempts (or 4 failed attempts, 5 failed attempts, and a 6th attempt). With the reading that the fifth failure locks the account:
- 4 failed attempts then the correct password: login succeeds, account not locked.
- 5 failed attempts: account locked, message displayed.
- 5 failed attempts then the correct password: refused because the account is locked.
Also check whether the counter resets after a successful login, and whether the lock expires (and test the exact time boundary if it does). Always confirm the reading of "after 5" with the product owner.

**Answer 9.** Boundary times since the code was sent: 299 seconds (4:59) valid, 300 seconds (5:00) valid (the specification says "up to and including"), 301 seconds (5:01) rejected as expired with a clear message. Also test 0 seconds (just sent, valid). Also consider clock and time-zone differences between the user's device and the server.

**Answer 10.** The code uses `>` and `<` where `>=` and `<=` are needed, so it wrongly excludes both 1 and 100. Boundary tests:
- Quantity 1: expected accepted, actual rejected. Reveals the lower-edge defect.
- Quantity 100: expected accepted, actual rejected. Reveals the upper-edge defect.
- Quantity 2 and 99: pass, showing that the middle works, which demonstrates why middle values alone would never have found the defect.
- Quantity 0 and 101: correctly rejected, so they pass. The correct code is `quantity >= 1 and quantity <= 100`.

---

## Knowledge Check

Test your understanding. Answers are below.

1. In your own words, what is a boundary value, and why do defects cluster around boundaries?
2. What is an off-by-one error? Give an example.
3. What is the difference between 2-value and 3-value BVA? List the values each gives for a field that accepts 10 to 50.
4. Which of these defects would the test value 18 detect for the rule "age 18 or older": (a) the code uses `age > 18`; (b) the code uses `age >= 19`; (c) the code uses `age >= 17`?
5. A field accepts whole numbers from 1 to 100. What does the number 101 test, and what is the expected result?
6. What is the step (precision) for a price field with two decimal places, and what is the first invalid value above a maximum of 500.00?
7. A password must be 6 to 12 characters. Give the 3-value boundary lengths.
8. What is the difference between an explicit and an implicit boundary? Give one example of each.
9. In the rule "free shipping for orders over 50.00," is 50.00 eligible? What are the boundary values?
10. An account is locked after 3 failed login attempts. Which numbers of failed attempts do you test?
11. Why is it risky to test all combinations of boundaries across many fields?
12. Name three limitations of BVA.
13. A 17-character test string is used for a field with a maximum of 16, and the field also requires a digit. The test string has no digit. Why is this a poor test?
14. How does BVA relate to the defect clustering principle?
15. Which technique is the best partner for BVA, and where will you learn it?

### Knowledge Check: Answers

1. A boundary value is a value at the edge of a range where the system's behaviour changes (for example the minimum or maximum allowed value). Defects cluster there because of off-by-one errors, confusion between `<` and `<=`, fence-post counting mistakes, ambiguous wording in requirements, and mixed-up zero-based and one-based counting.
2. An off-by-one error is a defect where a comparison or count is wrong by exactly one unit. Example: writing `age > 18` when the rule is "18 or older," which wrongly rejects exactly 18. Another example: a loop that runs 9 times instead of 10.
3. 2-value BVA uses the boundary value and its closest neighbour in the adjacent partition for each boundary: for 10 to 50 it gives 9, 10, 50, 51 (four values). 3-value BVA uses the value below, on, and above each boundary: 9, 10, 11, 49, 50, 51 (six values). The 2-value approach is the ISTQB convention; the 3-value approach is common in industry and more thorough.
4. (a) Detected: 18 would be rejected when it should be accepted. (b) Detected: 18 would be rejected. (c) Not detected by 18 (18 is accepted correctly); it would be detected by 17, which would be wrongly accepted.
5. 101 is the first value above the maximum (just above maximum). The expected result is rejection with an appropriate error message.
6. The step is 0.01. The first invalid value above 500.00 is 500.01.
7. 5, 6, 7, 11, 12, 13.
8. An explicit boundary is stated in the requirement (for example, "age 18 to 60"). An implicit boundary comes from the technology or environment and is not stated (for example, the largest value a 32-bit integer can hold, 2,147,483,647, or a database column that holds 50 characters).
9. No. "Over 50.00" means strictly greater than 50.00. Boundary values: 49.99 (not free), 50.00 (not free), 50.01 (free).
10. Test 2, 3, and 4 failed attempts (below, on, and above the threshold): after 2 the account is still usable, after 3 it becomes locked, and the fourth attempt is refused because of the lock.
11. The number of combinations grows very quickly (for example 5 values across 10 fields is nearly 10 million tests), so it is impractical. It is the exhaustive-testing trap. Instead, test one field's boundaries at a time with the other fields at nominal values, and use other techniques for important combinations.
12. Any three of: works only on ordered ranges; ignores interactions between fields; depends on a correct specification; misses hidden or implicit boundaries; needs the right step size; assumes the middle of a range works; may miss back-end limits if only the user interface is tested.
13. The test would be rejected for the missing digit as well as for the length, so you cannot tell whether the length rule works. Each test should violate only one rule at a time.
14. Defect clustering says that most defects are found in a small number of areas. In input handling, the edges of ranges are exactly such an area, so BVA directs test effort to the places where defects are most concentrated.
15. Equivalence Partitioning, which is covered in the next lesson. It divides the inputs into groups, and BVA then tests the edges of those groups.

---

## Key Takeaways

- A **boundary** is the edge between two behaviours of the system. Defects cluster there because of off-by-one errors, `<` versus `<=` confusion, fence-post errors, and ambiguous wording. This is defect clustering in action.
- **Boundary Value Analysis** is a black-box technique that designs tests from the values at and next to the edges of ranges. If the edges work, the middle almost certainly works.
- **2-value BVA** (ISTQB convention) tests each boundary and its closest neighbour in the adjacent partition: for 18 to 60, the values 17, 18, 60, 61. **3-value BVA** (common industry practice) tests below, on, and above each boundary: 17, 18, 19, 59, 60, 61.
- Use the formulas: `min - step`, `min`, `min + step`, `max - step`, `max`, `max + step`. The step is 1 for integers and character counts, 0.01 for two-decimal numbers, one day for dates, and so on.
- Read requirements for **keywords** such as minimum, maximum, at least, up to, no more than, less than, over, within, between, and from-to. Clarify every ambiguous wording before testing.
- Boundaries are everywhere: string lengths, list sizes (empty, one, many, max), file sizes, array indexes, dates and times (midnight, leap years), login attempts, and outputs (grade cut-offs, price tiers, thresholds).
- Distinguish **explicit** boundaries (from the specification) from **implicit** ones (from data types and system limits). Test both.
- Design clean boundary tests: one boundary per test, all other rules satisfied, exact expected results.
- Never test all combinations of boundaries across many fields. Use one field at a time, then other techniques for combinations.
- A **boundary test suite exposes off-by-one defects** that tests on typical values never find, as the Python demo showed.
- BVA complements **Equivalence Partitioning** (next lesson), and it feeds data into later techniques such as decision tables and state transition testing.
- Be aware of its limits: ordered ranges only, depends on a correct specification, may miss hidden boundaries and combinations.

---

## Additional Resources

- **ISTQB Certified Tester Foundation Level (CTFL) syllabus and glossary**, including the descriptions of boundary value analysis, 2-value and 3-value approaches: [https://www.istqb.org](https://www.istqb.org). (Search the site for "CTFL syllabus" and "glossary.")
- **Guru99, "Equivalence Partitioning and Boundary Value Analysis"** (a beginner-friendly tutorial with worked examples): [https://www.guru99.com/equivalence-partitioning-boundary-value-analysis.html](https://www.guru99.com/equivalence-partitioning-boundary-value-analysis.html)
- **Ministry of Testing**, a community site with articles, courses, and discussions on test design techniques, including boundary value analysis: [https://www.ministryoftesting.com](https://www.ministryoftesting.com)

Come back to this lesson when you reach the Equivalence Partitioning lesson: the two techniques are designed to be used together, and you will design stronger tests for Project 1 once you can combine them.
