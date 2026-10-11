# Interview Questions: Week 2 — Thursday: SQL Fundamentals

**Scope:** relational database concepts, SQL syntax, SELECT statements, filtering and sorting data, basic query construction and using SQL for QA data validation. Examples use the shared 15-row `orders` practice table from the lessons, run on **SQLite** (dialect differences are noted where they matter).
**Total:** 20 questions (14 Beginner, 5 Intermediate, 1 Advanced).

---

## Beginner (Foundational)

### Q1: What is a relational database, and how do the terms table, row, column and RDBMS relate to each other?
**Keywords:** tables, rows (records), columns (fields), data type, RDBMS
<details>
<summary>Click to Reveal Answer</summary>

A relational database stores data in **tables**, and each table holds data about one kind of thing, such as `orders`. The **columns** run vertically and define which facts are stored (each with a fixed data type), while each **row** is one record, one instance of the thing. The **RDBMS** (Relational Database Management System) is the software, for example SQLite, MySQL or PostgreSQL, that stores the tables, enforces rules and answers SQL queries. A spreadsheet is a good analogy, but a database table is stricter: every row has exactly the same columns.

```sql
-- One row of the orders table (a single record)
SELECT order_id, customer_name
FROM orders
WHERE order_id = 1001;
```
</details>

*Source:* `relational-database-concepts.md`

---

### Q2: What is a primary key, and what is a foreign key?
**Keywords:** uniquely identifies, never NULL, refers to another table, relationship
<details>
<summary>Click to Reveal Answer</summary>

A **primary key** is a column (or set of columns) whose value uniquely identifies each row and is never NULL; in the `orders` table, `order_id` is the primary key. A **foreign key** is a column in one table that refers to the primary key of another table, which is how tables are linked and why the model is called "relational". Splitting data across tables this way avoids repeating the same customer details on every order. Today we only need the idea, because constraints and keys in depth are covered later.

```sql
-- Searching by primary key returns exactly one row (or none)
SELECT order_id, customer_name, status
FROM orders
WHERE order_id = 1010;
```
</details>

*Source:* `relational-database-concepts.md`

---

### Q3: What does NULL mean in SQL, and how is it different from `0` and from an empty string?
**Keywords:** unknown / missing, not zero, not empty string, not the text 'NULL', IS NULL
<details>
<summary>Click to Reveal Answer</summary>

NULL is the marker for "no value": a fact that is unknown, missing or not applicable. It is **not** the number `0` (a known value), **not** an empty string `''` (a known text of length zero) and **not** the text `'NULL'` (which in test data is a bug worth catching). Because NULL means unknown, comparing anything to it gives an unknown result, so you must test for it with `IS NULL`. In our data, orders `1004` and `1014` have a NULL email.

```sql
SELECT order_id, email
FROM orders
WHERE email IS NULL;   -- returns 1004 and 1014
```
</details>

*Source:* `relational-database-concepts.md`

---

### Q4: What does it mean that SQL is "declarative", and what is a SQL dialect?
**Keywords:** declarative, what not how, query optimiser, dialect, ANSI/ISO standard
<details>
<summary>Click to Reveal Answer</summary>

In **declarative** SQL you describe *what* result you want, and the database's query optimiser decides *how* to get it. That contrasts with procedural Python, where you write the loop step by step. SQL is standardised by ANSI/ISO, but each product adds its own spellings and extras called **dialects** (SQLite SQL, MySQL, PostgreSQL, T-SQL for SQL Server, PL/SQL for Oracle). The core (`SELECT`, `WHERE`, `ORDER BY`) is shared, but things like row limiting differ (`LIMIT` vs `TOP` vs `FETCH FIRST`).

```sql
-- WHAT we want, not HOW to loop over rows
SELECT order_id, customer_name, status
FROM orders
WHERE status = 'PENDING';
```
</details>

*Source:* `sql-syntax.md`

---

### Q5: How do you write text, number, date and NULL values in a query, and how do you include an apostrophe such as in `O'Brien`?
**Keywords:** single quotes, no quotes for numbers, ISO date, bare NULL, doubled apostrophe
<details>
<summary>Click to Reveal Answer</summary>

Text and dates go in **single quotes** (dates in ISO format `YYYY-MM-DD`), numbers are written with no quotes, and NULL is the bare word `NULL` without quotes. To put an apostrophe inside a text value you **double it**, so `'Jack O''Brien'` is read as `Jack O'Brien`. Forgetting this gives a syntax error (in SQLite: `near "Brien": syntax error`). Double quotes are for identifiers, not text.

```sql
SELECT order_id, customer_name
FROM orders
WHERE customer_name = 'Jack O''Brien';   -- returns order 1011
```
</details>

*Source:* `sql-syntax.md`

---

### Q6: In what order do you write the clauses of a basic query, and in what order does the database logically process them?
**Keywords:** written order, FROM, WHERE, SELECT, ORDER BY, LIMIT
<details>
<summary>Click to Reveal Answer</summary>

You write `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`, but the database logically processes them as `FROM` (find the table), `WHERE` (discard rows), `SELECT` (compute columns and aliases), `ORDER BY` (sort) and `LIMIT` (cut off). Because `WHERE` runs before `SELECT`, standard SQL does not let you use a `SELECT` alias in `WHERE` (SQLite is lenient, other engines are strict), so you repeat the expression. `ORDER BY` runs after `SELECT`, so it can use the alias.

```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE quantity * unit_price > 1000   -- repeat the expression here
ORDER BY line_total DESC;            -- alias allowed here
```
</details>

*Source:* `sql-syntax.md`

---

### Q7: What does `SELECT *` do, and when should you avoid it?
**Keywords:** all columns, exploring, named columns, fragile, large tables
<details>
<summary>Click to Reveal Answer</summary>

`SELECT *` returns every column of the table in the order they were defined. It is fine for exploring an unfamiliar table or quickly eyeballing a row, but avoid it in automated tests and saved queries. If someone adds, removes or reorders a column, code that reads `row[5]` silently starts reading the wrong thing. It is also wasteful on large tables and may expose sensitive columns. The rule of thumb: `*` for exploring, named columns for anything you keep.

```sql
SELECT order_id, product, quantity, unit_price   -- named columns: stable and self-documenting
FROM orders
WHERE order_id = 1002;
```
</details>

*Source:* `select-statements.md`

---

### Q8: What is a column alias, and what is a calculated column?
**Keywords:** `AS`, alias, expression, computed per row, not stored
<details>
<summary>Click to Reveal Answer</summary>

An **alias** (introduced with `AS`) gives a column a different name in the result only; the underlying table is untouched. A **calculated column** is an expression in the `SELECT` list, such as `quantity * unit_price`, computed for each row at query time and never stored. Aliases make headings readable and give a name to calculated columns. Writing `AS` explicitly also avoids the accidental-alias bug, where a forgotten comma turns the next column into an alias.

```sql
SELECT order_id,
       quantity * unit_price AS line_total
FROM orders
WHERE order_id <= 1003;
```
</details>

*Source:* `select-statements.md`

---

### Q9: Explain the different jobs of `SELECT`, `WHERE` and `ORDER BY`.
**Keywords:** columns, rows, filter, sort, result set
<details>
<summary>Click to Reveal Answer</summary>

`SELECT` chooses which **columns** (or expressions) appear in the result, `WHERE` filters which **rows** are kept (only rows where the condition is true), and `ORDER BY` **sorts** the rows that remain. `SELECT` only reads and returns a temporary result set; it never changes the stored data. You can filter on a column you do not display, and sort on one you do not display.

```sql
SELECT customer_name        -- which columns
FROM orders
WHERE country = 'Mexico'    -- which rows
ORDER BY customer_name;     -- in what order
```
</details>

*Source:* `filtering-and-sorting-data.md`

---

### Q10: What is the difference between `=` and `LIKE`? What do `%` and `_` mean?
**Keywords:** exact match, pattern, `%` any characters, `_` one character, case sensitivity
<details>
<summary>Click to Reveal Answer</summary>

`=` tests for an exact match, while `LIKE` matches text against a pattern. In a pattern, `%` stands for any number of characters (including none) and `_` stands for exactly one character. Case rules depend on the engine: in SQLite `=` on text is case-sensitive but `LIKE` is case-insensitive for English letters, while PostgreSQL and Oracle are case-sensitive for both (PostgreSQL offers `ILIKE`). For portable code use `LOWER(col) LIKE 'pattern'`.

```sql
SELECT order_id, customer_name FROM orders WHERE customer_name LIKE 'A%';   -- starts with A (1001, 1009)
SELECT order_id, product FROM orders WHERE product = 'laptop';              -- 0 rows in SQLite (case-sensitive)
SELECT order_id, product FROM orders WHERE product LIKE 'laptop';           -- 1001, 1006 in SQLite
```
</details>

*Source:* `filtering-and-sorting-data.md`

---

### Q11: What do `IN` and `BETWEEN` do, and is `BETWEEN` inclusive?
**Keywords:** list of values, shorthand for OR, range, inclusive, low AND high
<details>
<summary>Click to Reveal Answer</summary>

`IN` matches a value against a list and is shorthand for several `OR`s on the same column. `BETWEEN low AND high` is shorthand for `>= low AND <= high`, so **both ends are included**, and the order of the bounds matters (`BETWEEN 100 AND 20` returns nothing). `NOT IN` and `NOT BETWEEN` give the opposite. `BETWEEN` can also be used on ISO date text.

```sql
SELECT order_id, country FROM orders WHERE country IN ('UK', 'Mexico');
SELECT order_id, unit_price FROM orders WHERE unit_price BETWEEN 20 AND 100;   -- 1002, 1005, 1007, 1011
```
</details>

*Source:* `filtering-and-sorting-data.md`

---

### Q12: How do `ORDER BY`, `ASC`/`DESC` and `LIMIT` work, and why should `LIMIT` be paired with `ORDER BY`?
**Keywords:** no guaranteed order, ascending default, DESC, LIMIT, Top-N
<details>
<summary>Click to Reveal Answer</summary>

Without `ORDER BY` the order of rows is not guaranteed, so `ORDER BY` is the only reliable way to sort. Sorting is ascending (`ASC`) by default and `DESC` reverses it; you can sort by several columns, and a unique final key such as the primary key makes ties deterministic. `LIMIT n` returns at most `n` rows, but without `ORDER BY` it returns *some* rows, not a meaningful "first" ones. Together they give the Top-N pattern. `LIMIT` is written at the very end; SQL Server uses `TOP` and Oracle 12c+ uses `FETCH FIRST`.

```sql
SELECT order_id, product, unit_price
FROM orders
ORDER BY unit_price DESC, order_id
LIMIT 3;   -- 1001, 1006, 1014
```
</details>

*Source:* `filtering-and-sorting-data.md`

---

### Q13: Describe a step-by-step method for writing a query from a plain-English request.
**Keywords:** understand, locate table, choose columns, filter, order/limit, build incrementally, verify
<details>
<summary>Click to Reveal Answer</summary>

First **understand** the request (and ask if it is ambiguous), then **locate** the table and relevant columns, **choose the output** columns, add the **filter** conditions, then add **ordering or limiting**, and finally **verify** the result against what you can see in the data. Build incrementally: start with the smallest query that runs and add one clause at a time, so if the result goes wrong the defect is in the last thing you added. A handy memory aid for the thinking order is "where is it, what do I want, which ones?".

```sql
-- Build 1: SELECT * FROM orders;
-- Build 2: choose columns
-- Build 3: add the filter
-- Build 4: add the order
SELECT order_id, customer_name, product, status
FROM orders
WHERE customer_name = 'Karen White'
ORDER BY order_id DESC;
```
</details>

*Source:* `basic-query-construction.md`

---

### Q14: What is a "violation query" in SQL data validation, and what does an empty result mean?
**Keywords:** describe what is wrong, no rows = rule holds, each row is a defect, business rule
<details>
<summary>Click to Reveal Answer</summary>

A violation query describes the *opposite* of the business rule, that is, what is wrong, so every returned row is a defect and an **empty result means the data passes**. For the rule "quantity must be at least 1", the violation is `quantity < 1`. One query checks every row, and the returned rows are the evidence for a bug report. It is complemented by an expectation query, which confirms that a specific known record exists with the right values.

```sql
-- V-03: Quantity must be at least 1. Expected: 0 rows.
SELECT order_id, product, quantity
FROM orders
WHERE quantity < 1
ORDER BY order_id;   -- returns 1007 (qty 0) and 1011 (qty -1): the rule FAILS
```
</details>

*Source:* `using-sql-for-qa-data-validation.md`

---

## Intermediate (Application)

### Q15: Customer service says some customers never got a confirmation email. Write a query that finds orders with no usable email address.
**Hint:** "Missing" can mean NULL, blank, or not shaped like an address, and `NOT LIKE` alone skips NULLs.
**Keywords:** IS NULL, TRIM, NOT LIKE, OR branches, unknown
<details>
<summary>Click to Reveal Answer</summary>

Translate "no usable email" into concrete conditions and combine them with `OR`: the email is NULL, is blank after trimming, or does not look like an address. The `IS NULL` branch must be written separately because `NULL NOT LIKE ...` is unknown, not true, so the `NOT LIKE` branch would never catch the NULL rows. On the sample data this returns `1004` and `1014` (NULL) and `1006` (`frank.moore@example`, no top-level domain). `LIKE '%@%.%'` is only a coarse smoke test, not rigorous validation.

```sql
SELECT order_id, customer_name, email
FROM orders
WHERE email IS NULL
   OR TRIM(email) = ''
   OR email NOT LIKE '%@%.%'
ORDER BY order_id;
```
</details>

*Source:* `using-sql-for-qa-data-validation.md`

---

### Q16: The spec says status may only be `PENDING`, `SHIPPED`, `DELIVERED` or `CANCELLED`. How do you find orders with an invalid status, and how can you discover the values that really exist?
**Hint:** Think `NOT IN`, plus the NULL case, plus a query that lists the real values.
**Keywords:** NOT IN, IS NULL, case sensitivity, DISTINCT, allowed list
<details>
<summary>Click to Reveal Answer</summary>

Use a violation query with `NOT IN` on the allowed list, and add `OR status IS NULL`, because a NULL status would otherwise be skipped. On the sample data this flags order `1008`, whose status is lower-case `delivered`. To discover the real values, run `SELECT DISTINCT status`, which shows five values where the spec lists four. Note the dialect point: SQLite compares text case-sensitively, so this rule fails there, but in MySQL or SQL Server (case-insensitive by default) the same check would pass silently, so validate on the real target engine.

```sql
SELECT order_id, status
FROM orders
WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
   OR status IS NULL
ORDER BY order_id;          -- 1008

SELECT DISTINCT status FROM orders ORDER BY status;   -- 5 values incl. 'delivered'
```
</details>

*Source:* `using-sql-for-qa-data-validation.md`

---

### Q17: A teammate wrote `WHERE email = NULL` to find orders with a missing email and got zero rows, although two orders have no email. Explain why, and give the fix.
**Hint:** What is the result of comparing an unknown value to another unknown value?
**Keywords:** NULL, unknown, three-valued logic, IS NULL, WHERE keeps only TRUE
<details>
<summary>Click to Reveal Answer</summary>

NULL means "unknown", so `email = NULL` evaluates to UNKNOWN (even `NULL = NULL`), not TRUE. SQL has three truth values (TRUE, FALSE, UNKNOWN) and `WHERE` keeps only rows where the condition is TRUE, so every row is dropped. The same applies to `<> NULL`. The correct tests are `IS NULL` and `IS NOT NULL`. A related consequence is that `<>` and `NOT IN` silently skip NULL rows, so add `OR email IS NULL` if you want them included.

```sql
SELECT order_id, email FROM orders WHERE email = NULL;     -- 0 rows (wrong)
SELECT order_id, email FROM orders WHERE email IS NULL;    -- 1004, 1014 (correct)
```
</details>

*Source:* `filtering-and-sorting-data.md`

---

### Q18: You need "pending or shipped orders from the UK". A colleague wrote `WHERE status = 'PENDING' OR status = 'SHIPPED' AND country = 'UK'`. What does it actually return, and how do you fix it?
**Hint:** Which of `AND` / `OR` is evaluated first?
**Keywords:** precedence, AND before OR, parentheses, review
<details>
<summary>Click to Reveal Answer</summary>

`AND` is evaluated before `OR`, so the database reads it as `status = 'PENDING' OR (status = 'SHIPPED' AND country = 'UK')`. That returns all pending orders from every country (`1004`, `1007`, `1011`, `1014`) plus only shipped UK orders, which is too broad. Wrap the `OR` group in parentheses so the country condition applies to both statuses; the intended query returns only order `1011`. As a habit, add parentheses whenever you mix `AND` and `OR`.

```sql
SELECT order_id, country, status
FROM orders
WHERE (status = 'PENDING' OR status = 'SHIPPED')
  AND country = 'UK';   -- 1011
```
</details>

*Source:* `basic-query-construction.md`

---

### Q19: Your automated UI test just created an order and you do not know its id. Write a query to fetch the most recent order, and explain why you add a second sort column.
**Hint:** Top-N pattern: sort descending, then limit.
**Keywords:** ORDER BY DESC, LIMIT 1, tiebreaker, deterministic, latest
<details>
<summary>Click to Reveal Answer</summary>

Sort newest first and take one row: `ORDER BY order_date DESC LIMIT 1`. Add a second, unique sort key such as `order_id DESC` as a **tiebreaker**, because if two orders share the same date the first key ties and the order of tied rows is unspecified, so a test could pass one day and fail the next. On the sample data this returns order `1015`. In SQL Server use `SELECT TOP 1 ... ORDER BY ...`, and in Oracle 12c+ use `FETCH FIRST 1 ROW ONLY`.

```sql
SELECT order_id, customer_name, order_date, status
FROM orders
ORDER BY order_date DESC, order_id DESC
LIMIT 1;
```
</details>

*Source:* `basic-query-construction.md`

---

## Advanced (Deep Dive)

### Q20: Your validation query returns zero rows. Under what circumstances can that be a "false pass", and how do you protect yourself?
**Hint:** Think about NULL behaviour, parentheses, case sensitivity of the engine, and testing the test.
**Keywords:** false pass, three-valued logic, NULL, validate the query, known-bad data
<details>
<summary>Click to Reveal Answer</summary>

An empty result means "no problems" only if the query itself is correct. It can falsely pass when: (1) you use `= NULL`, which is never true, so it finds none of the missing values; (2) a negative condition such as `NOT LIKE`, `<>`, `NOT BETWEEN` or `NOT IN` silently skips NULL rows, unless you add `OR col IS NULL`; (3) a NULL inside a `NOT IN` list makes the whole condition UNKNOWN, so nothing is returned; (4) the engine's case rules or your own normalisation hide a real defect (the `delivered` status passes on MySQL or SQL Server, and also when you write `UPPER(status) NOT IN (...)`); or (5) missing parentheses around `OR` change the logic. Protect yourself by running each rule against data you know is bad (such as the planted defects `1004`, `1008`, `1011`) and confirming it catches them, and by running it on the real target engine, which is the same idea as making a unit test fail first.

```sql
-- FALSE PASS: 0 rows although orders 1004 and 1014 have no email
SELECT order_id FROM orders WHERE email = NULL;

-- FALSE PASS: 0 rows although order 1008 has 'delivered'
SELECT order_id, status FROM orders
WHERE UPPER(status) NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED');

-- Correct rule: catches 1008 (and any NULL status)
SELECT order_id, status FROM orders
WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
   OR status IS NULL;
```
</details>

*Source:* `using-sql-for-qa-data-validation.md` (with `filtering-and-sorting-data.md`)

---

## How to use this bank

This bank is for self-quizzing, so do not read the answers first.

1. Read a question and cover the answer (keep the `<details>` block closed).
2. Say your answer aloud as if you were in an interview, in 30 to 60 seconds. Use the hint only if you are stuck.
3. Open the answer and check that every **keyword** appeared in what you said. If you missed one, repeat the question until you can include it naturally.
4. Work through Beginner first until you can answer without notes, then attempt Intermediate (talk through the scenario step by step and write the query before revealing it), then the Advanced question. Run the SQL yourself against the `orders` table in SQLite and compare your rows with the answer.
5. If you struggle with a topic, re-read the lesson named in the *Source* line and try again the next day.
