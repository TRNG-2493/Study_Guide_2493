# Basic Query Construction

## Learning Objectives

By the end of this lesson you will be able to:

- Turn a plain-English question or test requirement into a correct SQL query using a repeatable **step-by-step method**.
- **Build a query incrementally**, one clause at a time, checking the result after every step.
- Assemble `SELECT`, `FROM`, `WHERE`, `DISTINCT`, `ORDER BY` and `LIMIT` into well-structured queries in the correct clause order.
- Format and comment queries so that teammates (and Git diffs) can read them easily.
- **Read** an unfamiliar query and explain it in plain English, clause by clause.
- Diagnose queries that return **too many rows, too few rows, or the wrong rows**.
- Use a small library of reusable **query patterns** (find by key, find latest, find missing, find invalid, find recent).
- Sanity-check a query result against an expected answer you can verify by hand.
- Store validation queries as `.sql` files in a repository and run them from a Python test.

## Why This Matters

In the previous three lessons you collected the individual pieces: tables and rows, the grammar of SQL, `SELECT` lists, and the filtering and sorting tools. Knowing the parts of a car is not the same as being able to drive. This lesson is about **driving**: combining the parts into correct queries, reliably, under real working conditions.

For a QA or test automation engineer, the stakes are particular:

- A query that returns **too few rows** can hide a defect (a false pass).
- A query that returns **too many rows** wastes investigation time (a false alarm) or, worse, makes a test fail for the wrong reason.
- A query nobody else can read cannot be reviewed, maintained, or trusted.

In the Week 2 Epic, trainees build SQL into their QA toolkit, and today's **Project 1 milestone** is a set of data validation queries. Those queries will be committed to your repository, reviewed by your pair-programming partner, and run again and again. A disciplined construction method is what makes them dependable. On Friday, when you add INSERT/UPDATE/DELETE, joins, subqueries and aggregates, exactly the same method will still apply. You will simply have more clauses to add.

> **Reminder:** We continue with the 15-row `orders` table from *Relational Database Concepts*. All results below were produced by running the queries against that table.

<details>
<summary>Dataset recap: the <code>orders</code> table (click to expand)</summary>

Columns: `order_id` (primary key), `customer_name`, `email`, `product`, `category`, `quantity`, `unit_price`, `status`, `order_date`, `country`.

| order_id | customer_name | email | product | category | quantity | unit_price | status | order_date | country |
|---|---|---|---|---|---|---|---|---|---|
| 1001 | Alice Johnson | alice.j@example.com | Laptop | Electronics | 1 | 1200.0 | DELIVERED | 2025-01-05 | USA |
| 1002 | Bob Smith | bob.smith@example.com | Wireless Mouse | Accessories | 2 | 25.5 | SHIPPED | 2025-01-07 | USA |
| 1003 | Carla Gomez | carla.g@example.com | USB-C Cable | Accessories | 5 | 9.99 | DELIVERED | 2025-01-10 | Canada |
| 1004 | David Lee | NULL | Monitor | Electronics | 1 | 300.0 | PENDING | 2025-01-12 | USA |
| 1005 | Emma Wilson | emma.w@example.com | Keyboard | Accessories | 1 | 80.0 | CANCELLED | 2025-01-15 | UK |
| 1006 | Frank Moore | frank.moore@example | Laptop | Electronics | 2 | 1150.0 | SHIPPED | 2025-01-20 | Canada |
| 1007 | Grace Kim | grace.k@example.com | Webcam | Electronics | 0 | 49.99 | PENDING | 2025-02-01 | USA |
| 1008 | Henry Adams | henry.a@example.com | Desk Lamp | Home Office | 3 | 19.99 | delivered | 2025-02-03 | UK |
| 1009 | Alice Johnson | alice.j@example.com | Headphones | Electronics | 1 | 150.0 | DELIVERED | 2025-02-10 | USA |
| 1010 | Isabel Torres | isabel.t@example.com | Office Chair | Home Office | 1 | 220.0 | SHIPPED | 2025-02-14 | Mexico |
| 1011 | Jack O'Brien | jack.ob@example.com | Wireless Mouse | Accessories | -1 | 25.5 | PENDING | 2025-02-18 | UK |
| 1012 | Karen White | karen.w@example.com | Monitor | Electronics | 2 | 300.0 | DELIVERED | 2025-03-02 | USA |
| 1013 | Liam Chen | liam.c@example.com | USB-C Cable | Accessories | 10 | 9.99 | SHIPPED | 2025-03-05 | Canada |
| 1014 | Maria Lopez | NULL | Standing Desk | Home Office | 1 | 450.0 | PENDING | 2025-03-09 | Mexico |
| 1015 | Noah Brown | noah.b@example.com | Keyboard | Accessories | 1 | 0.0 | DELIVERED | 2025-03-12 | USA |


</details>

---

## The Concept

### 1. A method for writing any query

Beginners often stare at an empty editor and try to write the whole query in one go. Professionals do not. They follow a short routine. Here it is. We will use it throughout the lesson.

| Step | Question to ask | Clause it produces |
|---|---|---|
| **1. Understand** | What exactly is being asked? What would a correct answer look like? | (none yet: restate the question) |
| **2. Locate** | Which table holds the data? Which columns are involved? | `FROM` |
| **3. Choose output** | What columns does the person need to *see*? | `SELECT` |
| **4. Filter** | Which rows qualify? What are the conditions? | `WHERE` |
| **5. Order & limit** | Does order matter? Do I need only the top N? | `ORDER BY`, `LIMIT` |
| **6. Run & inspect** | Does the result look right? Are headings correct? | (check) |
| **7. Verify** | Can I confirm at least one row, or the row count, by hand? | (check) |
| **8. Tidy** | Is it formatted, commented, and named well? | (style) |

A helpful memory aid for the *order you think* (which differs from the order you *write*): **"Where is it, what do I want, which ones?"** Table, columns, conditions.

### 2. Worked example 1: a simple lookup

**Request (from a test case):** "After the checkout test runs, verify that the order for *Karen White* exists and show its status."

**Step 1: Understand.** One customer, find her order(s), report the status.

**Step 2: Locate.** The `orders` table. Relevant columns: `customer_name`, `status`.

**Step 3: Choose output.** The tester wants to identify the order and read the status: `order_id`, `customer_name`, `product`, `status`.

**Step 4: Filter.** `customer_name = 'Karen White'` (text, so single quotes).

**Step 5: Order/limit.** Only one customer; sorting not important. But in a real test, if she had several orders, we would want the latest, so add `ORDER BY order_id DESC`.

Now the **incremental build**. Start with the smallest query that runs, then add one thing at a time.

*Build 1: just the table.*

```sql
SELECT *
FROM orders;
```

(Runs fine, returns 15 rows. We know the table exists and the spelling of its name is right. We do not print the full output again.)

*Build 2: choose the columns.*

```sql
SELECT order_id, customer_name, product, status
FROM orders;
```

*Build 3: add the filter.*

```sql
SELECT order_id, customer_name, product, status
FROM orders
WHERE customer_name = 'Karen White';
```

**Result** (1 row):

| order_id | customer_name | product | status |
|---|---|---|---|
| 1012 | Karen White | Monitor | DELIVERED |


*Build 4: add the order.*

```sql
SELECT order_id, customer_name, product, status
FROM orders
WHERE customer_name = 'Karen White'
ORDER BY order_id DESC;
```

**Result** (1 row):

| order_id | customer_name | product | status |
|---|---|---|---|
| 1012 | Karen White | Monitor | DELIVERED |


**Step 7: Verify.** Looking at the dataset recap above, Karen White appears once (order `1012`, a Monitor, `DELIVERED`). The query matches what we see.

Why build incrementally? If you write all four clauses at once and the result is wrong, you have *four* suspects. If you run after every addition, the defect is always in the **last thing you added**. This is exactly the same debugging principle you applied on Wednesday: change one thing at a time.

### 3. Worked example 2: a business rule with two conditions

**Request:** "Find orders from the USA that have not shipped yet. We need them for the warehouse team."

**Step 1: Understand.** "Not shipped yet" is ambiguous. In this dataset the lifecycle is `PENDING` → `SHIPPED` → `DELIVERED`, with `CANCELLED` as a side exit. "Not shipped yet" most likely means `PENDING`. A cancelled order will never ship, so the warehouse does not want it either. **When requirements are ambiguous, a tester asks.** Let us assume the answer is "PENDING only".

**Step 2/3.** Table `orders`; columns the warehouse needs: `order_id`, `product`, `quantity`, `status`, `country`.

**Step 4.** Two conditions that must both be true, so `AND`:

```sql
SELECT order_id, product, quantity, status, country
FROM orders
WHERE country = 'USA'
  AND status = 'PENDING'
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | product | quantity | status | country |
|---|---|---|---|---|
| 1004 | Monitor | 1 | PENDING | USA |
| 1007 | Webcam | 0 | PENDING | USA |


**Step 7: Verify.** From the data: USA orders are 1001, 1002, 1004, 1007, 1009, 1012, 1015. Of those, the `PENDING` ones are `1004` and `1007`. The result matches.

**Notice** order `1007` has `quantity` 0. The query answered the question, but you spotted a data oddity on the way. Good testers keep their eyes open and report such observations separately.

### 4. Worked example 3: ranges and several allowed values

**Request:** "Give me orders placed in February 2025 for Electronics or Home Office, most expensive first."

**Plan:**

- Date range: `order_date >= '2025-02-01' AND order_date < '2025-03-01'`.
- Allowed categories: `category IN ('Electronics', 'Home Office')`.
- Sorting: `unit_price DESC`, tiebreaker `order_id`.

```sql
SELECT order_id, product, category, unit_price, order_date
FROM orders
WHERE order_date >= '2025-02-01'
  AND order_date <  '2025-03-01'
  AND category IN ('Electronics', 'Home Office')
ORDER BY unit_price DESC, order_id;
```

**Result** (4 rows):

| order_id | product | category | unit_price | order_date |
|---|---|---|---|---|
| 1010 | Office Chair | Home Office | 220.0 | 2025-02-14 |
| 1009 | Headphones | Electronics | 150.0 | 2025-02-10 |
| 1007 | Webcam | Electronics | 49.99 | 2025-02-01 |
| 1008 | Desk Lamp | Home Office | 19.99 | 2025-02-03 |


**Verify by hand:** February orders are `1007` (Webcam, Electronics), `1008` (Desk Lamp, Home Office), `1009` (Headphones, Electronics), `1010` (Office Chair, Home Office), `1011` (Wireless Mouse, **Accessories**). The mouse is excluded by the category filter. So four rows, sorted by price: 220, 150, 49.99, 19.99. Correct.

### 5. Worked example 4: the "latest" pattern

**Request:** "What is the most recently placed order?" or "Which order did my automated test just create?"

```sql
SELECT order_id, customer_name, order_date, status
FROM orders
ORDER BY order_date DESC, order_id DESC
LIMIT 1;
```

**Result** (1 row):

| order_id | customer_name | order_date | status |
|---|---|---|---|
| 1015 | Noah Brown | 2025-03-12 | DELIVERED |


Why both `order_date DESC` **and** `order_id DESC`? If two orders were placed on the same date the first key ties; the second key makes the result deterministic. This `ORDER BY ... DESC LIMIT 1` is perhaps the single most common SQL pattern in test automation. (SQL Server: `SELECT TOP 1 ... ORDER BY ...`; Oracle 12c+: `... FETCH FIRST 1 ROW ONLY`.)

### 6. Worked example 5: finding what is missing or wrong

**Request:** "Customer service says some customers never received a confirmation email. Find orders where we have no usable email address."

Think about what "no usable email" means: (a) email is NULL; (b) email is blank; (c) email does not look like an address.

```sql
SELECT order_id, customer_name, email
FROM orders
WHERE email IS NULL
   OR TRIM(email) = ''
   OR email NOT LIKE '%@%.%'
ORDER BY order_id;
```

**Result** (3 rows):

| order_id | customer_name | email |
|---|---|---|
| 1004 | David Lee | NULL |
| 1006 | Frank Moore | frank.moore@example |
| 1014 | Maria Lopez | NULL |


Three rows: two NULLs (`1004`, `1014`) and one malformed value (`1006`, `frank.moore@example`, no top-level domain). Note how each of the three definitions of "unusable" became one `OR` branch. Translating a vague requirement into a **list of concrete conditions** is a core QA skill: SQL simply forces you to be precise.

An important subtlety: the `NOT LIKE` branch alone would *not* have caught the NULL emails (NULL `NOT LIKE` anything is unknown). That is why the `IS NULL` branch is written separately. This is the NULL behaviour from the filtering lesson in action.

### 7. Worked example 6: a calculated value with a filter and a limit

**Request:** "Which are the three largest orders by value (quantity times price), excluding cancelled orders?"

```sql
SELECT order_id,
       product,
       quantity,
       unit_price,
       quantity * unit_price AS line_total
FROM orders
WHERE status <> 'CANCELLED'
ORDER BY line_total DESC, order_id
LIMIT 3;
```

**Result** (3 rows):

| order_id | product | quantity | unit_price | line_total |
|---|---|---|---|---|
| 1006 | Laptop | 2 | 1150.0 | 2300.0 |
| 1001 | Laptop | 1 | 1200.0 | 1200.0 |
| 1012 | Monitor | 2 | 300.0 | 600.0 |


Check: Order `1006` is 2 × 1150 = 2300; `1001` is 1 × 1200 = 1200; `1012` is 2 × 300 = 600. Next is `1014` (450). Verified.

### 8. Reading a query: translating SQL back into English

You will spend as much time **reading** other people's queries (code reviews, inherited test suites, bug reports) as writing your own. The technique is the reverse of the construction method: go clause by clause and say each one in plain English.

Try it on this query:

```sql
SELECT DISTINCT country
FROM orders
WHERE status IN ('SHIPPED', 'DELIVERED')
  AND unit_price > 100
ORDER BY country;
```

**Result** (3 rows):

| country |
|---|
| Canada |
| Mexico |
| USA |


Reading:

1. `FROM orders`: we are looking in the orders table.
2. `WHERE status IN ('SHIPPED', 'DELIVERED')`: only orders that have shipped or been delivered...
3. `AND unit_price > 100`: ...and whose unit price is above 100.
4. `SELECT DISTINCT country`: show each country **once**.
5. `ORDER BY country`: alphabetically.

Summary in English: **"In which countries have we shipped or delivered an item priced above 100?"** Notice that case-sensitivity matters here: `delivered` in lower case (order `1008`) would not match `'DELIVERED'` in SQLite, but its price (19.99) is below 100 anyway.

#### Exercise in reading: spot the problem

```sql
SELECT order_id, status, country
FROM orders
WHERE status = 'PENDING' OR status = 'SHIPPED' AND country = 'UK';
```

What does the author *probably* intend, and what does it *actually* do? (Answer: they probably want pending-or-shipped orders from the UK. Because `AND` binds tighter than `OR`, the query returns all pending orders from every country plus shipped UK orders. Parentheses fix it. You saw this in the filtering lesson.) Spotting this kind of problem in review is a valuable skill.

### 9. When the result is wrong: a troubleshooting guide

Even experienced people sometimes get surprising results. Use this table to diagnose.

#### Too many rows

| Likely cause | How to check | Fix |
|---|---|---|
| Missing `WHERE` clause | Does the query have one? | Add the condition |
| `OR` where `AND` was meant | Re-read the English: "both" vs "either" | Use `AND` |
| `AND`/`OR` mixed without parentheses | Look for both in one `WHERE` | Add parentheses |
| Pattern too broad (`LIKE '%an%'`) | Look at the unexpected rows | Tighten the pattern |
| Duplicates in the data | Compare with `SELECT DISTINCT` | Decide if duplicates are legitimate |
| (Friday) Combining tables incorrectly | Not applicable today | Learn joins on Friday |

#### Too few rows (or none)

| Likely cause | How to check | Fix |
|---|---|---|
| Case mismatch (`'Delivered'` vs `'DELIVERED'`) | `SELECT DISTINCT col` to see the real values | Use the exact value or `UPPER(col)` |
| Trailing / leading spaces in data | `LENGTH(col)` versus the expected length | `TRIM(col)` |
| `= NULL` used instead of `IS NULL` | Look for `NULL` in the `WHERE` | `IS NULL` |
| `<>` or `NOT IN` skipping NULL rows | Is NULL possible in that column? | Add `OR col IS NULL` |
| `AND` where `OR` was meant | Re-read the English | Use `OR` |
| Reversed `BETWEEN` bounds | Low value first? | Swap |
| Wrong data type literal (`'5'` vs `5`, wrong date format) | Look at the column type | Match the type; use ISO dates |
| The data genuinely is not there | Remove conditions one at a time | The result may be *correct*: report it |

The last row deserves emphasis. **An empty result may be the right answer.** For a "find bad data" query an empty result is the *goal*. For a "find the order I just created" query it is a *failure*. Always know in advance which one you expect.

#### The "peel the onion" technique

If a query with many conditions returns nothing, remove conditions one at a time (or comment them out with `--`) and rerun until rows appear. The condition you removed last is the culprit.

```sql
SELECT order_id, status, country, quantity
FROM orders
WHERE status = 'PENDING'
  AND country = 'UK'
  -- AND quantity > 0
  ;
```

**Result** (1 row):

| order_id | status | country | quantity |
|---|---|---|---|
| 1011 | PENDING | UK | -1 |


With the last condition commented out we see that order `1011` qualifies on status and country, but has `quantity` -1, so adding `AND quantity > 0` would hide it. In a data-validation setting that is probably exactly why you would *not* want such a condition.

### 10. A small library of reusable query patterns

Memorise the shapes below. In practice most QA queries are variations of these. Replace the names in `<angle brackets>`.

#### Pattern 1: Find by key (the exact record)

```sql
SELECT <columns>
FROM <table>
WHERE <primary_key> = <value>;
```

```sql
SELECT order_id, customer_name, status
FROM orders
WHERE order_id = 1010;
```

**Result** (1 row):

| order_id | customer_name | status |
|---|---|---|
| 1010 | Isabel Torres | SHIPPED |


Expect exactly **one** row (primary keys are unique). Zero rows means "does not exist"; more than one would be a serious data problem.

#### Pattern 2: Find the latest N

```sql
SELECT <columns> FROM <table>
ORDER BY <date_or_id> DESC
LIMIT <N>;
```

```sql
SELECT order_id, order_date
FROM orders
ORDER BY order_date DESC, order_id DESC
LIMIT 3;
```

**Result** (3 rows):

| order_id | order_date |
|---|---|
| 1015 | 2025-03-12 |
| 1014 | 2025-03-09 |
| 1013 | 2025-03-05 |


#### Pattern 3: Find rows with an allowed set / a forbidden set

```sql
SELECT order_id, country
FROM orders
WHERE country IN ('USA', 'Canada')
ORDER BY order_id
LIMIT 4;
```

**Result** (4 rows):

| order_id | country |
|---|---|
| 1001 | USA |
| 1002 | USA |
| 1003 | Canada |
| 1004 | USA |


#### Pattern 4: Find missing data

```sql
SELECT <key>, <column> FROM <table>
WHERE <column> IS NULL;
```

```sql
SELECT order_id, customer_name
FROM orders
WHERE email IS NULL
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | customer_name |
|---|---|
| 1004 | David Lee |
| 1014 | Maria Lopez |


#### Pattern 5: Find invalid values (the "violation" query)

Describe the *opposite* of the business rule. If the rule is "quantity must be at least 1", the violation is `quantity < 1`. An **empty result means the data passes**.

```sql
SELECT order_id, quantity
FROM orders
WHERE quantity < 1
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | quantity |
|---|---|
| 1007 | 0 |
| 1011 | -1 |


This query does not return empty here, so the data **fails** the rule: two violating rows (`1007` and `1011`).

#### Pattern 6: Find values in a date window

```sql
SELECT order_id, order_date, status
FROM orders
WHERE order_date >= '2025-02-10'
  AND order_date <  '2025-02-20'
ORDER BY order_date;
```

**Result** (3 rows):

| order_id | order_date | status |
|---|---|---|
| 1009 | 2025-02-10 | DELIVERED |
| 1010 | 2025-02-14 | SHIPPED |
| 1011 | 2025-02-18 | PENDING |


(Half-open range: start inclusive, end exclusive. It never misses the last day, and consecutive windows never overlap.)

#### Pattern 7: Discover the real values of a column

```sql
SELECT DISTINCT status
FROM orders
ORDER BY status;
```

**Result** (5 rows):

| status |
|---|
| CANCELLED |
| DELIVERED |
| PENDING |
| SHIPPED |
| delivered |


Always run this when you start working with an unfamiliar column. It tells you what you are *really* dealing with, not what the documentation promises. Here it reveals the case variant `delivered`.

### 11. Style and formatting rules for shared queries

Because queries live in Git and are reviewed by colleagues, adopt a consistent layout. These are the conventions for this course.

1. **Keywords in UPPER CASE**; table and column names in lower_snake_case.
2. **One clause per line**, aligned at the left margin.
3. **One condition per line** in `WHERE`, with `AND` / `OR` at the start of the line, indented by two spaces.
4. **Parentheses** around any `OR` group, with a line break if long.
5. **List columns explicitly**; avoid `SELECT *` in saved queries.
6. **Aliases** with `AS`, descriptive names.
7. **Always** `ORDER BY` when order matters; add a unique tiebreaker.
8. **Comment the intent**, not the syntax. A comment should say *what rule is being checked and why*.
9. End with a **semicolon**.

A model query following all rules:

```sql
-- Rule V-03: Orders must have a quantity of at least 1.
-- Expected result: 0 rows. Any row returned is a data defect.
SELECT order_id,
       customer_name,
       quantity
FROM orders
WHERE quantity < 1
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | customer_name | quantity |
|---|---|---|
| 1007 | Grace Kim | 0 |
| 1011 | Jack O'Brien | -1 |


**Bad comment:** `-- selects orders`. (Obvious from the code.)
**Good comment:** `-- Rule V-03: quantity must be >= 1 (spec section 4.2)`. (Tells the reader *why*.)

A good header comment for each validation query includes the rule ID, a one-line description, the expected result, and optionally the author and date.

### 12. Saving queries as files and running them from Python

A query that only lives in your head or in a chat window is lost the moment you close it. Treat validation queries as **code**:

- Store each in a `.sql` file in your repository (for example `sql/validation/v03_quantity_positive.sql`).
- Commit them with Git, with meaningful messages (you practised that in Week 1 and during this week).
- Review them with pull requests.

The first file in your project might look like this:

```sql
-- File: sql/validation/v03_quantity_positive.sql
-- Rule V-03: quantity must be at least 1. Expected: 0 rows.
SELECT order_id, quantity
FROM orders
WHERE quantity < 1
ORDER BY order_id;
```

Your Python tests can then load and run it. This is Python code that *carries* SQL, because the test suite is written in Python:

```python
import sqlite3
from pathlib import Path

def run_validation(db_path, sql_file):
    """Run a validation query and return the offending rows."""
    sql = Path(sql_file).read_text()
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(sql).fetchall()
    finally:
        conn.close()

def test_quantity_is_positive():
    bad_rows = run_validation("shop.db", "sql/validation/v03_quantity_positive.sql")
    assert bad_rows == [], f"Rows with invalid quantity: {bad_rows}"
```

Explanation:

- `Path(sql_file).read_text()` reads the query text from disk (reading files was Tuesday's topic; `pathlib.Path` is a convenient built-in way to do it).
- `conn.execute(sql).fetchall()` runs it and returns a list of tuples; an empty list means "no violations".
- `try / finally` guarantees the connection is closed even if the query fails (the same idea as the context managers you studied on Tuesday).
- The assertion message includes the offending rows, so a failing test tells you *which* data is bad. That is the same principle as writing helpful assertion messages in unit tests.
- With our sample data this test **would fail**, correctly, because orders `1007` and `1011` violate the rule. That is the validation working as designed.

### 13. A construction checklist

Print this and keep it next to you while you work on the Project 1 milestone.

- [ ] Can I say what the query should return **in one English sentence**?
- [ ] Did I identify the **table** and **columns**?
- [ ] Do I know whether I expect **zero, one, or many** rows?
- [ ] Are **text values in single quotes**, numbers bare, dates ISO?
- [ ] Did I use **`IS NULL`**, not `= NULL`?
- [ ] Did I think about **NULLs** when using `<>` or `NOT IN`?
- [ ] Did I think about **upper/lower case and spaces** in text comparisons?
- [ ] Did I add **parentheses** around mixed `AND` / `OR`?
- [ ] If I used `LIMIT`, did I also use **`ORDER BY`** (with a tiebreaker)?
- [ ] Did I build and run it **incrementally**?
- [ ] Did I **verify** at least one row or the row count by hand?
- [ ] Is it **formatted and commented**?
- [ ] Does it avoid anything not available in my dialect (and have I noted dialect differences)?

### 14. Dialect considerations when building queries

| Concern | Portable approach |
|---|---|
| Limiting rows | Know all three: `LIMIT`, `TOP`, `FETCH FIRST`. Ask which engine the project uses. |
| Case-insensitive text matching | `UPPER(col) = 'VALUE'` or `LOWER(...)`; works everywhere. |
| Concatenation | `CONCAT()` exists in MySQL, PostgreSQL, SQL Server; `\|\|` in SQLite, PostgreSQL, Oracle. |
| Dates | ISO `'YYYY-MM-DD'` literals work almost everywhere; use half-open ranges. |
| String length | `LENGTH()` (most) vs `LEN()` (SQL Server). |
| NULL ordering | Add an explicit tiebreaker or `NULLS FIRST/LAST` where supported. |
| Identifier quoting | Avoid needing it: use plain snake_case names. |
| Statement terminator | End with `;` (SQL Server tolerates omission in most cases but not always). |

If a team uses more than one database product (for example SQLite locally and PostgreSQL in CI), write for the **common subset** and test on both.

---

## Summary / Key Takeaways

- Writing SQL is a **process**: understand the request, locate the table, choose the columns, filter the rows, order and limit, run, verify, tidy.
- **Build incrementally**: start with the simplest query that runs and add one clause at a time, so any problem is in the last thing you added.
- Convert vague requirements into **concrete conditions**; ask when requirements are ambiguous.
- Write clauses in the order `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`. Think in the order *table, columns, conditions*.
- A **violation query** describes the *opposite* of a business rule; **an empty result means the rule holds.**
- **Read** queries by translating each clause into English; this is how you review colleagues' work.
- Troubleshoot "too many / too few rows" with a checklist: NULLs, case, whitespace, `AND`/`OR` precedence, `BETWEEN` bounds, data types.
- Reusable patterns (find by key, latest N, missing, invalid, date window, discover values) cover most everyday QA needs.
- Treat queries as **code**: consistent style, intent-revealing comments, `.sql` files in Git, run from Python tests with helpful assertion messages.
- Always verify at least one result by hand, and know in advance what result you expect.

---

## Practice Questions

For each task, first write the English sentence describing the result, then the SQL, then verify against the dataset.

**Q1.** Show `order_id`, `customer_name` and `product` for orders from Canada, sorted by `order_id`.

**Q2.** Find all orders that are neither `DELIVERED` nor `CANCELLED` (use `UPPER` to be safe). Show `order_id` and `status`.

**Q3.** Which orders were placed in March 2025? Show `order_id`, `order_date`, and `product`, newest first.

**Q4.** List the five cheapest *valid* orders: `unit_price` greater than 0 and `quantity` at least 1. Show `order_id`, `product`, `unit_price`, with a deterministic order.

**Q5.** Show the distinct customers (names) who have ordered Electronics.

**Q6.** Show orders where `quantity * unit_price` is more than 500, with the calculated value labelled `line_total`, sorted largest first.

**Q7.** Explain the following query in one English sentence, and say how many rows you expect:

```sql
SELECT order_id, status
FROM orders
WHERE country = 'Mexico'
  AND status = 'PENDING';
```

**Q8.** Write a violation query for the rule "A cancelled order must not have `quantity` greater than 0" and explain what an empty result means. (Hint: also think whether the sample data has any cancelled orders.)

**Q9.** This query is meant to find US or UK orders that are `SHIPPED`. What is wrong, and what is the fix?

```sql
SELECT order_id, country, status
FROM orders
WHERE country = 'USA' OR country = 'UK' AND status = 'SHIPPED';
```

**Q10.** Write a query to find the most recent order for customer `Alice Johnson`.

**Q11.** Write a violation query for the rule "an email must contain an `@`" and say which order(s) it should *not* flag even though they have a problem with email.

**Q12.** (Challenge) Write one query that lists all orders failing at least one of these rules: quantity at least 1; unit_price greater than 0; email not NULL; status in the four upper-case allowed values. Show `order_id` and the columns involved, sorted by `order_id`. (This is a preview of what you will build in the next lesson.)

### Answers

**A1.** English: "Orders shipped to Canada, in id order."

```sql
SELECT order_id, customer_name, product
FROM orders
WHERE country = 'Canada'
ORDER BY order_id;
```

**Result** (3 rows):

| order_id | customer_name | product |
|---|---|---|
| 1003 | Carla Gomez | USB-C Cable |
| 1006 | Frank Moore | Laptop |
| 1013 | Liam Chen | USB-C Cable |


**A2.** English: "Orders still in progress."

```sql
SELECT order_id, status
FROM orders
WHERE UPPER(status) NOT IN ('DELIVERED', 'CANCELLED')
ORDER BY order_id;
```

**Result** (8 rows):

| order_id | status |
|---|---|
| 1002 | SHIPPED |
| 1004 | PENDING |
| 1006 | SHIPPED |
| 1007 | PENDING |
| 1010 | SHIPPED |
| 1011 | PENDING |
| 1013 | SHIPPED |
| 1014 | PENDING |


Order `1008` (lower-case `delivered`) is correctly excluded thanks to `UPPER`.

**A3.**

```sql
SELECT order_id, order_date, product
FROM orders
WHERE order_date >= '2025-03-01'
  AND order_date <  '2025-04-01'
ORDER BY order_date DESC, order_id DESC;
```

**Result** (4 rows):

| order_id | order_date | product |
|---|---|---|
| 1015 | 2025-03-12 | Keyboard |
| 1014 | 2025-03-09 | Standing Desk |
| 1013 | 2025-03-05 | USB-C Cable |
| 1012 | 2025-03-02 | Monitor |


**A4.**

```sql
SELECT order_id, product, unit_price
FROM orders
WHERE unit_price > 0
  AND quantity >= 1
ORDER BY unit_price ASC, order_id ASC
LIMIT 5;
```

**Result** (5 rows):

| order_id | product | unit_price |
|---|---|---|
| 1003 | USB-C Cable | 9.99 |
| 1013 | USB-C Cable | 9.99 |
| 1008 | Desk Lamp | 19.99 |
| 1002 | Wireless Mouse | 25.5 |
| 1005 | Keyboard | 80.0 |


Orders `1007` (quantity 0), `1011` (quantity -1) and `1015` (price 0) are excluded as invalid.

**A5.**

```sql
SELECT DISTINCT customer_name
FROM orders
WHERE category = 'Electronics'
ORDER BY customer_name;
```

**Result** (5 rows):

| customer_name |
|---|
| Alice Johnson |
| David Lee |
| Frank Moore |
| Grace Kim |
| Karen White |


Alice appears once even though she has two Electronics orders.

**A6.**

```sql
SELECT order_id, product, quantity * unit_price AS line_total
FROM orders
WHERE quantity * unit_price > 500
ORDER BY line_total DESC;
```

**Result** (3 rows):

| order_id | product | line_total |
|---|---|---|
| 1006 | Laptop | 2300.0 |
| 1001 | Laptop | 1200.0 |
| 1012 | Monitor | 600.0 |


**A7.** "Which Mexican orders are still pending?" Expected: one row (order `1014`, Maria Lopez). Order `1010` is Mexican but `SHIPPED`.

```sql
SELECT order_id, status
FROM orders
WHERE country = 'Mexico'
  AND status = 'PENDING';
```

**Result** (1 row):

| order_id | status |
|---|---|
| 1014 | PENDING |


**A8.**

```sql
SELECT order_id, status, quantity
FROM orders
WHERE status = 'CANCELLED'
  AND quantity > 0;
```

**Result** (1 row):

| order_id | status | quantity |
|---|---|---|
| 1005 | CANCELLED | 1 |


One row comes back (order `1005`). Whether that is a **defect** depends on the business rule you were given, which is just an example here. The key idea: for a violation query, **an empty result means the rule holds**, while any returned row is a violation to investigate. Here the rule as worded would flag a cancelled order that still has quantity, which in many real shops is perfectly normal. This is why you confirm the rule with the product owner before reporting it as a bug.

**A9.** `AND` binds tighter than `OR`, so it returns all USA orders plus only shipped UK orders. Fix:

```sql
SELECT order_id, country, status
FROM orders
WHERE (country = 'USA' OR country = 'UK')
  AND status = 'SHIPPED';
```

**Result** (1 row):

| order_id | country | status |
|---|---|---|
| 1002 | USA | SHIPPED |


**A10.**

```sql
SELECT order_id, customer_name, order_date
FROM orders
WHERE customer_name = 'Alice Johnson'
ORDER BY order_date DESC, order_id DESC
LIMIT 1;
```

**Result** (1 row):

| order_id | customer_name | order_date |
|---|---|---|
| 1009 | Alice Johnson | 2025-02-10 |


**A11.**

```sql
SELECT order_id, email
FROM orders
WHERE email NOT LIKE '%@%'
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | email |
|---|---|


It returns no rows. Two things are hiding: the NULL emails (`1004`, `1014`) are **not** flagged, because `NULL NOT LIKE ...` is unknown; and `frank.moore@example` (`1006`) passes this rule because it does contain an `@` even though it lacks a domain suffix. A single rule rarely catches every kind of bad data; combine checks.

**A12.**

```sql
SELECT order_id, quantity, unit_price, email, status
FROM orders
WHERE quantity < 1
   OR unit_price <= 0
   OR email IS NULL
   OR status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
ORDER BY order_id;
```

**Result** (6 rows):

| order_id | quantity | unit_price | email | status |
|---|---|---|---|---|
| 1004 | 1 | 300.0 | NULL | PENDING |
| 1007 | 0 | 49.99 | grace.k@example.com | PENDING |
| 1008 | 3 | 19.99 | henry.a@example.com | delivered |
| 1011 | -1 | 25.5 | jack.ob@example.com | PENDING |
| 1014 | 1 | 450.0 | NULL | PENDING |
| 1015 | 1 | 0.0 | noah.b@example.com | DELIVERED |


Six rows are flagged: `1004` and `1014` (NULL email), `1007` (zero quantity), `1008` (lower-case status), `1011` (negative quantity) and `1015` (zero price). The next lesson will organise checks like these into a proper validation suite.

---

## Additional Resources

- PostgreSQL Tutorial, *The SQL Language: Queries* (a gentle walkthrough of querying a table): https://www.postgresql.org/docs/current/tutorial-sql.html
- SQLite documentation, *SELECT* (full syntax diagrams for every clause): https://www.sqlite.org/lang_select.html
- Python documentation, *sqlite3: How to use placeholders to bind values* and cursor objects: https://docs.python.org/3/library/sqlite3.html
