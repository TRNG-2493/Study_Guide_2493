# Using SQL for QA Data Validation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **data validation** is and why QA / test automation engineers validate data in the database and not only in the user interface.
- Describe the main **data-quality dimensions** (completeness, validity, consistency, uniqueness, accuracy, timeliness) and match each to a SQL check.
- Write **violation queries**: queries that return the rows that break a business rule, where an empty result means "pass".
- Write **positive (expectation) queries** that check that a specific record was saved with the expected values.
- Build a **catalogue of validation rules** for a table, using only the Thursday toolkit: `SELECT`, `WHERE`, comparison operators, `AND` / `OR` / `NOT`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`, `DISTINCT`, `ORDER BY`, `LIMIT` and simple scalar functions.
- Interpret validation results, separate genuine defects from false alarms, and **report** them clearly.
- Automate a set of validation queries from **Python**, with helpful failure messages.
- Apply safe-working practices when querying test and shared databases.
- Recognise the limits of single-table validation and know what **Friday** will add.

## Why This Matters

Picture a typical test day. An automated UI test fills in the checkout form and clicks **Place Order**. The page shows "Thank you, your order is confirmed!" and the test goes green. Is the system correct?

Not necessarily. The page might say *confirmed* while the database holds:

- an order with a **negative quantity**,
- a **missing email**, so no confirmation can ever be sent,
- a **status in the wrong case**, which a later batch job does not recognise,
- a **price of 0.00**, so the customer is not charged.

None of these are visible on the success page. They are visible only to a tester who looks **behind the UI**, at the data. That is the value of SQL-based validation: it lets you test the *state of the system*, not just its appearance.

This is the heart of the Week 2 Epic. Trainees have spent the week making their Python robust (modules, exceptions, files, debugging, unit tests), and they are now adding SQL "for QA data validation". Everything from today's earlier lessons comes together here:

| Earlier lesson | What it contributes to validation |
|---|---|
| Relational database concepts | Understanding tables, rows, columns, NULL, data types; knowing *what* can be wrong with data |
| SQL syntax | Quoting, operators, comments, reading errors |
| SELECT statements | Choosing and calculating the columns that expose a problem |
| Filtering and sorting | Describing "bad data" with `WHERE` and presenting findings with `ORDER BY` |
| Basic query construction | A method, patterns, style, and troubleshooting |

Today's **Project 1 milestone** (QE Foundations) is to write data validation queries. This lesson is your blueprint: it shows what a good validation suite looks like for the `orders` table, how to automate it, and how to report what you find.

> **Reminder:** We use the 15-row `orders` table from *Relational Database Concepts*. It contains several **deliberately planted defects**. Part of the learning is discovering them with queries. You will find all of them in this lesson, and you can compare your own findings to the answer key at the end.

<details open>
<summary>Dataset recap: the <code>orders</code> table</summary>

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

### 1. What is data validation?

**Data validation** is the activity of checking that the data in a system is **correct, complete, consistent and follows the business rules**.

It is related to, but different from, other kinds of testing:

| Kind | Question it answers | Example |
|---|---|---|
| UI test | Does the screen behave correctly for the user? | The confirmation page appears |
| API test | Does the service return the correct response? | `POST /orders` returns 201 |
| **Data validation** | **Is the stored data correct?** | The new row in `orders` has the right quantity, price, and status |
| Unit test | Does one function compute the right result? | `calculate_total(2, 25.5) == 51.0` |

Good test strategies use *all* of these. SQL validation is especially strong at:

- verifying **side effects** (what the system saved, changed, or failed to save);
- inspecting **large volumes** of data quickly, in a way no UI test can;
- catching **silent corruption** that produces no visible error;
- **preparing and cleaning up test data** (read-only discovery today; changing data on Friday).

### 2. Where QA engineers use SQL validation

1. **Post-action verification.** After a UI or API test creates an order, confirm that exactly the expected row exists.
2. **Test-data discovery.** "Give me a pending UK order that I can cancel in my test." (A `SELECT` with `WHERE ... LIMIT 1`.)
3. **Environment health checks.** Before a regression suite runs, verify that baseline data is present and clean.
4. **Data migration / ETL testing.** After data is moved from an old system to a new one, verify it arrived intact.
5. **Defect investigation.** A customer reports wrong data; you query the record to see exactly what is stored.
6. **Regression guards.** A fixed bug gets a permanent SQL check so it can never silently return.

### 3. Data-quality dimensions and what to check

Quality people describe data quality using a handful of **dimensions**. They give you a checklist of *kinds* of problems to look for. Here they are, with the SQL idea behind each and what we can do **with today's toolkit**:

| Dimension | Question | SQL approach (Thursday tools) |
|---|---|---|
| **Completeness** | Is required data present? | `IS NULL`, blank-string checks |
| **Validity** | Are values allowed (type, format, range, list)? | `NOT IN`, `NOT BETWEEN`, `<`, `>`, `NOT LIKE` |
| **Consistency** | Is the data uniform and non-contradictory? | `DISTINCT` to reveal variants; case and whitespace checks; rules across columns of one row |
| **Uniqueness** | Is each real-world thing stored once? | Primary key (enforced by the database); `DISTINCT` to compare; deeper duplicate-finding on Friday |
| **Accuracy** | Does it match the real world or the source? | Compare against known expected values, calculated columns |
| **Timeliness** | Is it up to date and in the expected time window? | Date comparisons, `ORDER BY date DESC LIMIT` |

The next sections turn each dimension into concrete queries.

### 4. The core idea: the violation query

There are two styles of check.

#### Style A: the violation query (the workhorse)

Describe **what is wrong**. Run it. **If it returns no rows, the rule holds.** If it returns rows, each row is a defect.

```text
Business rule:      "Quantity must be at least 1."
Violation query:    SELECT ... WHERE quantity < 1;
Expected result:    0 rows
```

This is powerful because:

- one query checks *every* row, not just a sample;
- the offending rows are the evidence you attach to a bug report;
- the pass condition is simple: empty.

#### Style B: the expectation query (positive check)

Describe the **record you expect to exist** and check it appears with the right values. Typical after a test has created or changed something.

```text
Expectation:  "Order 1012 exists, belongs to Karen White, is for 2 Monitors and is DELIVERED."
Query:        SELECT ... WHERE order_id = 1012;
Check:        1 row, with those values
```

Use **both** styles. Violation queries guard against *unknown unknowns* in the data. Expectation queries confirm *specific known outcomes*.

> **Mind the false pass.** A violation query that returns nothing might mean "no problems", or it might mean "my query is wrong". Protect yourself by testing a rule against data you *know* is bad (our planted defects) and confirming it catches them. This is the same idea as making a unit test fail first.

### 5. Building the validation rules for `orders`

We will create a numbered catalogue, as you would for a real project. Each rule has an ID, a description, a dimension, and a violation query. Run each against the sample data and read the results.

#### V-01: Required email present (Completeness)

*Rule: every order must have an email so a confirmation can be sent.*

```sql
-- V-01: Email must not be NULL or blank. Expected: 0 rows.
SELECT order_id, customer_name, email
FROM orders
WHERE email IS NULL
   OR TRIM(email) = ''
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | customer_name | email |
|---|---|---|
| 1004 | David Lee | NULL |
| 1014 | Maria Lopez | NULL |


**Finding:** orders `1004` (David Lee) and `1014` (Maria Lopez) have no email. Two defects.

Why both `IS NULL` and `TRIM(email) = ''`? Because "missing" can be stored as NULL *or* as an empty or space-only string; checking only one lets the other slip through. Our data has only NULLs, but the second condition protects future runs.

#### V-02: Email looks valid (Validity)

*Rule: an email must contain `@` and a dot somewhere after it.*

```sql
-- V-02: Email must contain '@' followed later by '.'. Expected: 0 rows.
SELECT order_id, email
FROM orders
WHERE email IS NOT NULL
  AND email NOT LIKE '%@%.%'
ORDER BY order_id;
```

**Result** (1 row):

| order_id | email |
|---|---|
| 1006 | frank.moore@example |


**Finding:** order `1006` has the email `frank.moore@example`, which has no top-level domain. One defect.

Observe `email IS NOT NULL AND ...`. We exclude NULLs here deliberately, so each defect is reported by **one** rule, not two (the NULLs belong to V-01). Without that clause the NULL rows would silently not match anyway (unknown is not true), but being explicit makes the intent clear to the reader.

**Limitations:** `LIKE` is a coarse check. It would accept `a@b.c` and `@.`. For rigorous email validation use regular expressions in your test code, or engine-specific functions (`REGEXP` in MySQL, `~` in PostgreSQL, `REGEXP_LIKE` in Oracle). SQLite has no built-in regex function by default. As a quick smoke test, though, `LIKE` finds the worst offenders.

#### V-03: Quantity is positive (Validity: range)

```sql
-- V-03: Quantity must be at least 1. Expected: 0 rows.
SELECT order_id, product, quantity
FROM orders
WHERE quantity < 1
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | product | quantity |
|---|---|---|
| 1007 | Webcam | 0 |
| 1011 | Wireless Mouse | -1 |


**Findings:** order `1007` has quantity `0`; order `1011` has quantity `-1`. Two defects. A negative quantity is especially nasty: it could *reduce* stock or *credit* a customer.

You may also want an **upper bound**, say a maximum order of 100 units:

```sql
-- V-03b: Quantity must be between 1 and 100. Expected: 0 rows.
SELECT order_id, product, quantity
FROM orders
WHERE quantity NOT BETWEEN 1 AND 100
   OR quantity IS NULL
ORDER BY order_id;
```

**Result** (2 rows):

| order_id | product | quantity |
|---|---|---|
| 1007 | Webcam | 0 |
| 1011 | Wireless Mouse | -1 |


`OR quantity IS NULL` catches a missing quantity, which `NOT BETWEEN` alone would skip (NULL again!).

#### V-04: Price is positive (Validity: range)

```sql
-- V-04: Unit price must be greater than 0. Expected: 0 rows.
SELECT order_id, product, unit_price
FROM orders
WHERE unit_price <= 0
   OR unit_price IS NULL
ORDER BY order_id;
```

**Result** (1 row):

| order_id | product | unit_price |
|---|---|---|
| 1015 | Keyboard | 0.0 |


**Finding:** order `1015` has a price of `0.0` for a Keyboard. Unless the business runs a free-giveaway promotion, this is a defect, and it is the kind of data bug that costs real money. (Whether a price of zero is acceptable is a **business decision**; the query surfaces it, the team decides.)

#### V-05: Status uses an allowed value (Validity: domain list; Consistency)

```sql
-- V-05: Status must be exactly PENDING, SHIPPED, DELIVERED or CANCELLED. Expected: 0 rows.
SELECT order_id, status
FROM orders
WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
   OR status IS NULL
ORDER BY order_id;
```

**Result** (1 row):

| order_id | status |
|---|---|
| 1008 | delivered |


**Finding:** order `1008` has `delivered` in lower case. In a case-sensitive engine (SQLite, PostgreSQL, Oracle) it is not an allowed value, and a filter like `WHERE status = 'DELIVERED'` in application code would **miss it**. In a case-insensitive default (MySQL, SQL Server) the same check would pass silently, which is a good reminder that **validation queries must be tested on the real target engine**.

To see the *consistency* problem more directly, discover the real values:

```sql
-- Discovery: what statuses really exist?
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


Five values where the specification lists four. `DISTINCT` is your friend for finding inconsistent spellings (`USA` vs `U.S.A.`), stray spaces, and case variants.

#### V-06: Category and country in allowed lists (Validity; Consistency)

```sql
-- V-06a: Category must be Electronics, Accessories or Home Office. Expected: 0 rows.
SELECT order_id, category
FROM orders
WHERE category NOT IN ('Electronics', 'Accessories', 'Home Office')
   OR category IS NULL
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | category |
|---|---|


```sql
-- V-06b: Country must be one of the shop's markets. Expected: 0 rows.
SELECT order_id, country
FROM orders
WHERE country NOT IN ('USA', 'UK', 'Canada', 'Mexico')
   OR country IS NULL
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | country |
|---|---|


Both pass: empty results. A passing rule is good news, and also worth recording: you proved it holds *today*. These checks become **regression guards**: if a future code change starts writing `'usa'` or `'Great Britain'`, the rule will fail and tell you.

#### V-07: No stray whitespace (Consistency)

```sql
-- V-07: Text must not have leading or trailing spaces. Expected: 0 rows.
SELECT order_id, customer_name, email, status
FROM orders
WHERE customer_name <> TRIM(customer_name)
   OR email <> TRIM(email)
   OR status <> TRIM(status)
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | customer_name | email | status |
|---|---|---|---|


Passes. Trailing spaces are invisible in a grid but cause comparison failures (`'SHIPPED '` is not equal to `'SHIPPED'`). A cheap check with high value. (`TRIM` removes spaces from both ends. Combining it with `<>` finds values that change when trimmed.)

#### V-08: Date format and plausibility (Validity; Timeliness)

*Rule: `order_date` must follow `YYYY-MM-DD`, and must not be in the future.*

```sql
-- V-08a: order_date must match the pattern ____-__-__ (10 chars). Expected: 0 rows.
SELECT order_id, order_date
FROM orders
WHERE order_date NOT LIKE '____-__-__'
   OR order_date IS NULL
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | order_date |
|---|---|


Each `_` matches exactly one character, so `'____-__-__'` demands four characters, a dash, two characters, a dash, two characters. This catches `'01/05/2025'` or `'Jan 5'`. (It does not verify that the month is in 01 to 12; a real `DATE` column in MySQL, PostgreSQL or SQL Server would reject impossible dates when stored, one more reason production databases use proper date types.)

```sql
-- V-08b: Orders must not be dated in the future. Expected: 0 rows.
SELECT order_id, order_date
FROM orders
WHERE order_date > date('now')
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | order_date |
|---|---|


`date('now')` is SQLite's way of getting today's date. The equivalents are `CURRENT_DATE` (PostgreSQL, standard), `CURDATE()` (MySQL), `CAST(GETDATE() AS DATE)` (SQL Server) and `TRUNC(SYSDATE)` (Oracle). Our sample orders are all in early 2025, so none lie in the future.

And a *window* check, relevant if a nightly job should load only a particular month:

```sql
-- V-08c: All orders must fall in Jan 1 - Mar 31 2025 (the loaded period). Expected: 0 rows.
SELECT order_id, order_date
FROM orders
WHERE order_date < '2025-01-01'
   OR order_date > '2025-03-31'
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | order_date |
|---|---|


#### V-09: Cross-column logic within one row (Consistency / Accuracy)

Some rules compare columns of the **same row**. For example "the line total must not be absurdly large", or "a cancelled order should not also look delivered". Using a calculated expression:

```sql
-- V-09: A single line total above 5000 needs manual review. Expected: 0 rows.
SELECT order_id, product, quantity, unit_price,
       quantity * unit_price AS line_total
FROM orders
WHERE quantity * unit_price > 5000
ORDER BY line_total DESC;
```

**Result** (0 rows):

| order_id | product | quantity | unit_price | line_total |
|---|---|---|---|---|


The largest line total in our data is `2300.0` (order `1006`), so nothing is flagged. This kind of threshold rule is common for **outlier detection** and fraud-style sanity checks.

#### V-10: Duplicates (Uniqueness): what we can and cannot do today

`order_id` is the **primary key**, so the database itself refuses duplicate ids. That is a *constraint* doing validation for us. (Constraints are covered in depth on Friday.) But *business* duplicates can still exist: the same customer, product and date entered twice with different ids.

With today's tools we can **inspect** potential duplicates by looking at the rows side by side:

```sql
-- Eyeball check: orders per customer for repeat buyers.
SELECT customer_name, order_id, product, order_date
FROM orders
WHERE customer_name = 'Alice Johnson'
ORDER BY order_date, order_id;
```

**Result** (2 rows):

| customer_name | order_id | product | order_date |
|---|---|---|---|
| Alice Johnson | 1001 | Laptop | 2025-01-05 |
| Alice Johnson | 1009 | Headphones | 2025-02-10 |


Alice has two orders for *different* products on *different* dates: legitimate repeat business, not a duplicate. And `DISTINCT` helps to see how many different combinations there are:

```sql
SELECT DISTINCT customer_name, email
FROM orders
ORDER BY customer_name;
```

**Result** (14 rows):

| customer_name | email |
|---|---|
| Alice Johnson | alice.j@example.com |
| Bob Smith | bob.smith@example.com |
| Carla Gomez | carla.g@example.com |
| David Lee | NULL |
| Emma Wilson | emma.w@example.com |
| Frank Moore | frank.moore@example |
| Grace Kim | grace.k@example.com |
| Henry Adams | henry.a@example.com |
| Isabel Torres | isabel.t@example.com |
| Jack O'Brien | jack.ob@example.com |
| Karen White | karen.w@example.com |
| Liam Chen | liam.c@example.com |
| Maria Lopez | NULL |
| Noah Brown | noah.b@example.com |


There are 14 distinct customer/email pairs for 15 orders, because Alice appears twice with the same data. Finding *all* duplicates automatically across a large table requires **grouping and counting**, which we will learn in depth on Friday (**GROUP BY / HAVING** and aggregate functions). For now, the point is to recognise that uniqueness is a validation dimension and to know that Friday gives you the proper tool.

### 6. Putting rules together: the combined "dirty rows" query

Sometimes you want a quick overview: *which rows break any rule?* Combine the violation conditions with `OR`:

```sql
-- Overview: any order that violates at least one basic rule.
SELECT order_id, customer_name, email, quantity, unit_price, status
FROM orders
WHERE email IS NULL
   OR email NOT LIKE '%@%.%'
   OR quantity < 1
   OR unit_price <= 0
   OR status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
ORDER BY order_id;
```

**Result** (7 rows):

| order_id | customer_name | email | quantity | unit_price | status |
|---|---|---|---|---|---|
| 1004 | David Lee | NULL | 1 | 300.0 | PENDING |
| 1006 | Frank Moore | frank.moore@example | 2 | 1150.0 | SHIPPED |
| 1007 | Grace Kim | grace.k@example.com | 0 | 49.99 | PENDING |
| 1008 | Henry Adams | henry.a@example.com | 3 | 19.99 | delivered |
| 1011 | Jack O'Brien | jack.ob@example.com | -1 | 25.5 | PENDING |
| 1014 | Maria Lopez | NULL | 1 | 450.0 | PENDING |
| 1015 | Noah Brown | noah.b@example.com | 1 | 0.0 | DELIVERED |


**Seven** of the 15 orders (nearly half!) are dirty: `1004`, `1006`, `1007`, `1008`, `1011`, `1014`, `1015`. Reading across each row you can see *why* it was flagged: a NULL email, a malformed email, a zero quantity, a lower-case status, a negative quantity, another NULL email, a zero price.

**Trade-off:** one combined query is a great *summary*, but individual numbered rules are better for **reporting** and for **automation**, since each test then fails with a specific message ("V-03 failed for orders 1007, 1011"). Keep both: the overview for exploring, the numbered rules for the suite.

And the **clean** rows, the complement, are useful for choosing reliable test data:

```sql
-- Clean rows only: safe to use as baseline test data.
SELECT order_id, customer_name, product, status
FROM orders
WHERE email IS NOT NULL
  AND email LIKE '%@%.%'
  AND quantity >= 1
  AND unit_price > 0
  AND status IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
ORDER BY order_id;
```

**Result** (8 rows):

| order_id | customer_name | product | status |
|---|---|---|---|
| 1001 | Alice Johnson | Laptop | DELIVERED |
| 1002 | Bob Smith | Wireless Mouse | SHIPPED |
| 1003 | Carla Gomez | USB-C Cable | DELIVERED |
| 1005 | Emma Wilson | Keyboard | CANCELLED |
| 1009 | Alice Johnson | Headphones | DELIVERED |
| 1010 | Isabel Torres | Office Chair | SHIPPED |
| 1012 | Karen White | Monitor | DELIVERED |
| 1013 | Liam Chen | USB-C Cable | SHIPPED |


Eight clean rows. Notice that the "clean" query is **not** simply the dirty query with `NOT` slapped on the front. The NULL handling means you must write the positive conditions carefully (`IS NOT NULL` first). Check that dirty rows plus clean rows add up to 15 (7 + 8 = 15). This reconciliation is a good validation of your own validation.

### 7. Expectation (positive) queries

After a test runs, we confirm a specific record. Suppose a test claims to have placed an order for a Standing Desk. We expect the following state in the database:

| Column | Expected |
|---|---|
| `order_id` | 1014 |
| `customer_name` | Maria Lopez |
| `product` | Standing Desk |
| `quantity` | 1 |
| `unit_price` | 450 |
| `status` | PENDING |

```sql
-- Expectation: order 1014 exists with the expected values.
SELECT order_id, customer_name, product, quantity, unit_price, status
FROM orders
WHERE order_id = 1014;
```

**Result** (1 row):

| order_id | customer_name | product | quantity | unit_price | status |
|---|---|---|---|---|---|
| 1014 | Maria Lopez | Standing Desk | 1 | 450.0 | PENDING |


A strict check bakes every expected value into the `WHERE` clause. If the row comes back, **every** value matched:

```sql
SELECT order_id
FROM orders
WHERE order_id = 1014
  AND customer_name = 'Maria Lopez'
  AND product = 'Standing Desk'
  AND quantity = 1
  AND unit_price = 450
  AND status = 'PENDING';
```

**Result** (1 row):

| order_id |
|---|
| 1014 |


The advantage of this strict form: it returns exactly one row or none, which is easy to assert (`assert len(rows) == 1`). The disadvantage: when it returns none, you do not know *which* value differed. So the practical approach is a two-step one: first fetch the row by key and compare each field in Python, which gives a precise message per field (see the automation section).

> **Floating-point caution.** Comparing decimal numbers for exact equality (`unit_price = 450`) is safe here, but `0.1 + 0.2 = 0.3` is *false* in binary floating point. In production, store money as `DECIMAL`, and compare with a tolerance (`ABS(a - b) < 0.005`) when values come from calculations.

### 8. Row-count style checks (with a preview of aggregates)

Many validations are about **how many** rows exist: "The migration should have moved 15 orders." "My test created exactly one new row." We can already see the number of rows because the tool tells us ("15 rows"), and in Python we can use `len(rows)`. SQL has a dedicated function for counting, `COUNT(*)`, which belongs to the family of **aggregate functions**. We will study it properly on Friday, but you can use it now as a convenience:

```sql
-- Preview only: aggregates are explained in depth on Friday.
SELECT COUNT(*) AS pending_orders
FROM orders
WHERE status = 'PENDING';
```

**Result** (1 row):

| pending_orders |
|---|
| 4 |


For today, treat `COUNT(*)` as "how many rows match my `WHERE`?" and no more. If your instructor allows only Thursday's tools in your exercise, use `len(rows)` in Python or simply count the rows displayed.

### 9. Automating validation from Python

Running queries by hand is perfect for exploring. For a **suite** that runs on every build, put the rules into code. Below is a small, complete runner in Python. (It is Python because your test framework is Python; the SQL strings inside are what you learned today.)

```python
import sqlite3

RULES = [
    ("V-01", "Email must not be NULL or blank",
     "SELECT order_id, email FROM orders "
     "WHERE email IS NULL OR TRIM(email) = '' ORDER BY order_id"),
    ("V-02", "Email must look like an address (contain @ and a dot after it)",
     "SELECT order_id, email FROM orders "
     "WHERE email NOT LIKE '%@%.%' ORDER BY order_id"),
    ("V-03", "Quantity must be at least 1",
     "SELECT order_id, quantity FROM orders WHERE quantity < 1 ORDER BY order_id"),
    ("V-04", "Unit price must be greater than 0",
     "SELECT order_id, unit_price FROM orders WHERE unit_price <= 0 ORDER BY order_id"),
    ("V-05", "Status must be one of the four upper-case values",
     "SELECT order_id, status FROM orders "
     "WHERE status NOT IN ('PENDING','SHIPPED','DELIVERED','CANCELLED') "
     "OR status IS NULL ORDER BY order_id"),
    ("V-06", "Category must be an allowed value",
     "SELECT order_id, category FROM orders "
     "WHERE category NOT IN ('Electronics','Accessories','Home Office') "
     "OR category IS NULL ORDER BY order_id"),
    ("V-07", "Customer name must have no leading or trailing spaces",
     "SELECT order_id, customer_name FROM orders "
     "WHERE customer_name <> TRIM(customer_name) ORDER BY order_id"),
]

def run_rules(conn):
    """Run every rule. Return a dict {rule_id: violating_rows} for failures."""
    failures = {}
    for rule_id, description, sql in RULES:
        rows = conn.execute(sql).fetchall()
        status = "PASS" if not rows else "FAIL"
        print(f"{rule_id} {status:4}  {description}  ({len(rows)} violating row(s))")
        if rows:
            failures[rule_id] = rows
    return failures

if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    conn.executescript(open("setup.sql").read())
    failed = run_rules(conn)
    print()
    for rule_id, rows in failed.items():
        print(rule_id, rows)
```

Output when run against the sample data:

```text
V-01 FAIL  Email must not be NULL or blank  (2 violating row(s))
V-02 FAIL  Email must look like an address (contain @ and a dot after it)  (1 violating row(s))
V-03 FAIL  Quantity must be at least 1  (2 violating row(s))
V-04 FAIL  Unit price must be greater than 0  (1 violating row(s))
V-05 FAIL  Status must be one of the four upper-case values  (1 violating row(s))
V-06 PASS  Category must be an allowed value  (0 violating row(s))
V-07 PASS  Customer name must have no leading or trailing spaces  (0 violating row(s))

V-01 [(1004, None), (1014, None)]
V-02 [(1006, 'frank.moore@example')]
V-03 [(1007, 0), (1011, -1)]
V-04 [(1015, 0.0)]
V-05 [(1008, 'delivered')]
```

How it works, step by step:

- **`RULES`** is a list of tuples `(id, description, sql)`: the *data* of the suite. Adding a rule means adding one entry, with no new logic.
- **`conn.execute(sql).fetchall()`** runs the violation query and gets all violating rows as a list. (Remember: *empty list means pass*.)
- **`status = "PASS" if not rows else "FAIL"`**: an empty list is "falsy" in Python, so `not rows` is `True` when there are no violations.
- **`print(f"... {status:4} ...")`** formats a readable report line; `:4` pads the word to four characters so columns line up.
- **`failures`** collects the evidence (the actual bad rows) so that it can be logged, attached to a bug, or asserted on.
- **`":memory:"` and `executescript`** build a throw-away database from our setup script, so the example is repeatable. In a real project you would connect to the test environment's database instead.

In a pytest or unittest suite, each rule becomes a test:

```python
import pytest

@pytest.mark.parametrize("rule_id, description, sql", RULES)
def test_rule(conn, rule_id, description, sql):
    rows = conn.execute(sql).fetchall()
    assert rows == [], f"{rule_id} ({description}) violated by: {rows}"
```

Each rule shows up as its own test result, and the failure message names the rule and lists the offending rows. (You wrote `unittest` cases on Wednesday; `pytest` parametrisation does the same with less code. Whichever framework your project uses, the idea is identical: **one violation query, one assertion that the result is empty, one descriptive message.** The `conn` argument would come from a fixture that opens your test database.)

### 10. Reporting what you find

Finding a defect is half the job. The other half is communicating it so someone can fix it. A good data-defect report contains:

1. **Title**: what is wrong, in one line. "Orders can be saved with a negative quantity."
2. **Environment**: which database, which environment (dev/test/staging), and when you ran the check.
3. **Rule**: which business rule it breaks, with ID (V-03) and its source (spec section, acceptance criteria).
4. **Query**: the exact SQL, so anyone can reproduce your finding.
5. **Evidence**: the result rows (copy the table).
6. **Impact**: why it matters (inventory miscounts, revenue loss, customer harm).
7. **Suspected cause or steps** (if known): "Order 1011 was created via the mobile app on 2025-02-18."
8. **Severity / priority** (your suggestion).

Example write-up:

> **Title:** Orders accepted with zero or negative quantity
> **Rule:** V-03, "Quantity must be at least 1" (spec 4.2)
> **Query:** `SELECT order_id, product, quantity FROM orders WHERE quantity < 1;`
> **Evidence:** order 1007 (quantity 0, Webcam), order 1011 (quantity -1, Wireless Mouse)
> **Impact:** Negative quantity could increase stock or issue a credit; zero-quantity orders create empty shipments.
> **Suggested priority:** High.

Also distinguish **defects** from **false alarms** and **questions**. Zero-price order `1015` might be a legitimate promotion. The right report says, "Please confirm whether a price of 0.00 is allowed. If not, this is a defect." Good testers present evidence and ask clear questions instead of declaring everything a bug.

### 11. Working safely with databases

Today's work is read-only, which is naturally safe. Still, adopt these habits now, because you will rely on them on Friday when you start changing data:

- **Use a test or practice database**, never production, unless explicitly authorised and read-only.
- **Prefer read-only database accounts** for validation.
- **Limit output** when exploring large tables (`LIMIT 20`). A careless `SELECT *` on a table with 100 million rows can slow a shared server.
- **Mind personal data.** Emails, names and addresses are personal data. Do not paste them into public chats or bug trackers without masking.
- **Do not hard-code secrets** (passwords, connection strings) into scripts committed to Git. Use environment variables or a secrets manager.
- **Record the query** you ran with the date and environment, so results can be reproduced.
- **Check which database you are connected to** before running anything. A very common mistake is querying staging while thinking it is dev.

### 12. Dialect considerations for validation

| Task | SQLite | MySQL | PostgreSQL | SQL Server | Oracle |
|---|---|---|---|---|---|
| Today's date | `date('now')` | `CURDATE()` | `CURRENT_DATE` | `CAST(GETDATE() AS DATE)` | `TRUNC(SYSDATE)` |
| Regex match | (extension needed) | `col REGEXP 'pat'` | `col ~ 'pat'` | (use `LIKE` / CLR) | `REGEXP_LIKE(col, 'pat')` |
| Text equality case | sensitive | insensitive | sensitive | insensitive | sensitive |
| String length | `LENGTH` | `LENGTH` / `CHAR_LENGTH` | `LENGTH` | `LEN` | `LENGTH` |
| Blank vs NULL | different | different | different | different | `''` **is** NULL |
| Limit rows | `LIMIT` | `LIMIT` | `LIMIT` | `TOP` | `FETCH FIRST` |
| Type strictness | lenient | strict | strict | strict | strict |

The takeaways:

1. **Case sensitivity** can make a rule pass on one engine and fail on another. Test on the real target.
2. **Oracle's empty-string-is-NULL** behaviour changes how you write "missing" checks.
3. **SQLite is lenient with types**, so it may let bad data in that stricter engines would reject, so more validation is needed, not less.

### 13. What single-table validation cannot do (and what comes next)

Everything today was about **one table**. Real validation often needs more:

| Need | Today | Coming |
|---|---|---|
| Find duplicate business keys automatically | Eyeball with `ORDER BY` / `DISTINCT` | **Friday:** `GROUP BY`, `HAVING` |
| Totals, averages, min/max, counts | Calculated columns only | **Friday:** aggregate functions |
| Compare data across tables (orders vs customers) | Not possible | **Friday:** JOINs, multi-table queries |
| Find "orphan" rows (orders with no customer) | Not possible | **Friday:** LEFT JOIN, subqueries |
| Enforce rules inside the database | Only noticed in passing (`PRIMARY KEY`, `NOT NULL`) | **Friday:** constraints, primary and foreign keys |
| Create or fix test data | Only read | **Friday:** `INSERT`, `UPDATE`, `DELETE` |

We will cover each of these in depth on Friday, under *Test-data validation using SQL*. Today's skills are the foundation: every Friday query still has a `SELECT`, a `FROM` and a `WHERE`.

### 14. A short guide for pair working (today's exercise format)

Today's exercise is done in pairs, with a **driver** (types) and a **navigator** (thinks, reads the spec, spots problems), swapping roles every 30 minutes. Some tips that suit validation work in particular:

- The **navigator** reads the *rule* in plain English; the **driver** writes the SQL. Then swap: the navigator should be able to *explain the query back* in plain English (the reading skill from the previous lesson).
- Before you run a violation query, **predict** the result aloud: "I expect two rows: 1007 and 1011". Surprising results are where learning happens.
- Keep each rule in its own `.sql` file with a header comment, and commit often with clear messages.
- In your short retrospective, note which rule was hardest to write, which dialect pitfalls surprised you, and which defect you found that you did not expect.

---

## Summary / Key Takeaways

- **Data validation** checks that stored data is correct, complete, consistent and rule-abiding. It finds problems that the UI hides.
- Think in **quality dimensions**: completeness, validity, consistency, uniqueness, accuracy, timeliness. Each maps to a style of SQL check.
- A **violation query** describes bad data; **an empty result means the rule holds**. An **expectation query** confirms a specific known record.
- Protect against false passes: test each rule against data you know is bad.
- With only Thursday's toolkit, you can check: NULL / blank values (`IS NULL`, `TRIM`), ranges (`<`, `NOT BETWEEN`), allowed lists (`NOT IN`), formats (`LIKE`), whitespace (`<> TRIM`), date windows, calculated outliers, and discover real values with `DISTINCT`.
- Always handle **NULL** explicitly (`OR col IS NULL`) because NULLs slip past `<>`, `NOT IN`, `NOT BETWEEN` and `NOT LIKE`.
- In our sample data the planted defects are: NULL emails (`1004`, `1014`), a malformed email (`1006`), zero quantity (`1007`), negative quantity (`1011`), zero price (`1015`), and a lower-case status (`1008`).
- Automate rules as data (`ID`, description, SQL) plus one assertion that the result is empty, with a message that names the rule and shows the offending rows.
- Report defects with a clear title, rule, query, evidence, impact and priority, and separate defects from questions.
- Work safely: test databases, read-only accounts, limited output, masked personal data, no committed secrets.
- Dialect differences (case sensitivity, empty string vs NULL, date functions, regex) mean you must validate on the **actual** target engine.
- Friday adds `GROUP BY`, aggregates, JOINs, subqueries, constraints and DML for deeper, multi-table validation.

---

## Practice Questions

**Q1.** In your own words, what does it mean when a violation query returns zero rows? Give an example of a situation in which zero rows would actually mean the query is wrong.

**Q2.** Write a violation query for the rule "`country` must be one of `USA`, `UK`, `Canada`, `Mexico`, and must not be NULL."

**Q3.** Write a violation query for "order dates must be in 2025." Does the sample data pass?

**Q4.** Write a query that returns the clean orders from the USA (all five rules from the "clean rows" query), sorted by `order_id`.

**Q5.** Write a violation query for "A pending order must have `quantity` of at least 1 and a non-NULL email." Which orders does it flag?

**Q6.** The product owner says unit prices for `Accessories` should never exceed 100. Write the violation query, and then write the test for a different rule: Electronics prices must be at least 10.

**Q7.** Why does `WHERE status <> 'DELIVERED'` fail to flag order `1008` as inconsistent, and what query would reveal the inconsistency?

**Q8.** Write an expectation query verifying that order `1010` is for `Isabel Torres`, an `Office Chair`, quantity `1`, status `SHIPPED`, country `Mexico`.

**Q9.** Add a rule `V-08` to the Python `RULES` list to flag orders dated before `2025-01-01`. Write the tuple.

**Q10.** Write a short defect report (title, rule, query, evidence, impact) for the negative quantity issue.

**Q11.** (Challenge) Using only Thursday's tools, produce a list of the orders that have at least one problem *and* are not yet delivered or cancelled (so the warehouse could still intervene). Show `order_id`, `status`, and the problem columns.

**Q12.** (Reflection) Name two kinds of data defect that you cannot reliably detect with single-table queries and the Thursday toolkit, and say what Friday will give you to catch them.

### Answers

**A1.** Zero rows means that no row breaks the rule: the rule *holds* on the data checked. Zero rows is misleading when the query itself is faulty. For example, writing `WHERE email = NULL` (always returns zero rows), checking the wrong table, using the wrong case (`'delivered'` vs `'DELIVERED'`), or running against an empty database or an empty test environment. That is why you test a rule against known bad data.

**A2.**

```sql
SELECT order_id, country
FROM orders
WHERE country NOT IN ('USA', 'UK', 'Canada', 'Mexico')
   OR country IS NULL
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | country |
|---|---|


**A3.**

```sql
SELECT order_id, order_date
FROM orders
WHERE order_date < '2025-01-01'
   OR order_date >= '2026-01-01'
   OR order_date IS NULL
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | order_date |
|---|---|


The sample data passes: no violations.

**A4.**

```sql
SELECT order_id, customer_name, product, status
FROM orders
WHERE country = 'USA'
  AND email IS NOT NULL
  AND email LIKE '%@%.%'
  AND quantity >= 1
  AND unit_price > 0
  AND status IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
ORDER BY order_id;
```

**Result** (4 rows):

| order_id | customer_name | product | status |
|---|---|---|---|
| 1001 | Alice Johnson | Laptop | DELIVERED |
| 1002 | Bob Smith | Wireless Mouse | SHIPPED |
| 1009 | Alice Johnson | Headphones | DELIVERED |
| 1012 | Karen White | Monitor | DELIVERED |


**A5.**

```sql
SELECT order_id, status, quantity, email
FROM orders
WHERE status = 'PENDING'
  AND (quantity < 1 OR email IS NULL)
ORDER BY order_id;
```

**Result** (4 rows):

| order_id | status | quantity | email |
|---|---|---|---|
| 1004 | PENDING | 1 | NULL |
| 1007 | PENDING | 0 | grace.k@example.com |
| 1011 | PENDING | -1 | jack.ob@example.com |
| 1014 | PENDING | 1 | NULL |


Flagged: `1004` (NULL email), `1007` (quantity 0), `1011` (quantity -1), `1014` (NULL email). Note the parentheses around the `OR`; without them the precedence would change the meaning.

**A6.**

```sql
-- Accessories must not exceed 100
SELECT order_id, product, category, unit_price
FROM orders
WHERE category = 'Accessories'
  AND unit_price > 100
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | product | category | unit_price |
|---|---|---|---|


```sql
-- Electronics must cost at least 10
SELECT order_id, product, category, unit_price
FROM orders
WHERE category = 'Electronics'
  AND unit_price < 10
ORDER BY order_id;
```

**Result** (0 rows):

| order_id | product | category | unit_price |
|---|---|---|---|


Both return no rows, so both rules hold on this data.

**A7.** In SQLite, `'delivered' <> 'DELIVERED'` is true, so order `1008` *does* appear in a `<> 'DELIVERED'` result, but that listing mixes it with genuinely undelivered orders and does not tell you that the value is a mis-cased variant. In MySQL or SQL Server it would be hidden altogether. The revealing queries are `SELECT DISTINCT status FROM orders;` (shows both spellings) or the allowed-list rule `WHERE status NOT IN ('PENDING','SHIPPED','DELIVERED','CANCELLED')`.

**A8.**

```sql
SELECT order_id
FROM orders
WHERE order_id = 1010
  AND customer_name = 'Isabel Torres'
  AND product = 'Office Chair'
  AND quantity = 1
  AND status = 'SHIPPED'
  AND country = 'Mexico';
```

**Result** (1 row):

| order_id |
|---|
| 1010 |


One row means every expected value matched.

**A9.**

```python
("V-08", "Order date must not be before 2025-01-01",
 "SELECT order_id, order_date FROM orders "
 "WHERE order_date < '2025-01-01' ORDER BY order_id"),
```

**A10.** Example report:

> **Title:** Orders accepted with zero or negative quantity
> **Rule:** V-03, "Quantity must be at least 1"
> **Query:** `SELECT order_id, product, quantity FROM orders WHERE quantity < 1 ORDER BY order_id;`
> **Evidence:** order 1007 (Webcam, quantity 0); order 1011 (Wireless Mouse, quantity -1)
> **Impact:** A negative quantity could raise stock counts or generate credits; a zero quantity produces an empty shipment.
> **Suggested priority:** High.

**A11.**

```sql
SELECT order_id, status, email, quantity, unit_price
FROM orders
WHERE status IN ('PENDING', 'SHIPPED')
  AND (email IS NULL
       OR email NOT LIKE '%@%.%'
       OR quantity < 1
       OR unit_price <= 0)
ORDER BY order_id;
```

**Result** (5 rows):

| order_id | status | email | quantity | unit_price |
|---|---|---|---|---|
| 1004 | PENDING | NULL | 1 | 300.0 |
| 1006 | SHIPPED | frank.moore@example | 2 | 1150.0 |
| 1007 | PENDING | grace.k@example.com | 0 | 49.99 |
| 1011 | PENDING | jack.ob@example.com | -1 | 25.5 |
| 1014 | PENDING | NULL | 1 | 450.0 |


Orders `1004`, `1006`, `1007`, `1011` and `1014` are still actionable. Orders `1008` (lower-case status) and `1015` (price 0, already `DELIVERED`) are excluded because they are already delivered. (`1008`'s status does not match `'PENDING'` or `'SHIPPED'` either way.)

**A12.** Examples: (1) **duplicate business records** (the same customer, product and date entered twice) need grouping and counting: `GROUP BY`, `HAVING` and aggregate functions on Friday; (2) **orphan or mismatched records across tables** (an order whose customer does not exist) need JOINs and foreign keys on Friday; (3) **totals that must reconcile** (the sum of line items equals the order total) need aggregates and subqueries on Friday.

---

## Additional Resources

- PostgreSQL documentation, *Pattern Matching* (`LIKE`, `SIMILAR TO`, regular expressions): https://www.postgresql.org/docs/current/functions-matching.html
- SQLite documentation, *Date And Time Functions* (`date('now')` and friends): https://www.sqlite.org/lang_datefunc.html
- Python documentation, *sqlite3 module* (running parameterised queries from tests): https://docs.python.org/3/library/sqlite3.html
