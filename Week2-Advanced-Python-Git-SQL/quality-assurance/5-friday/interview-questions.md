# Interview Questions: Week 2 — Friday: SQL Joins & Data Validation

**Scope:** INSERT, UPDATE and DELETE; constraints and keys; INNER JOIN; LEFT and RIGHT JOIN; FULL JOIN; subqueries; GROUP BY and HAVING; multi-table queries; aggregate functions; test-data validation using SQL. Questions use the shared "QA Shop" practice database (customers, products, orders, order_items, payments, defects). Snippets were run on SQLite 3.45.1, and dialect differences are noted where they matter.
**Total:** 20 questions (14 Beginner, 5 Intermediate, 1 Advanced).

---

## Beginner (Foundational)

### Q1: What is the difference between `DELETE`, `TRUNCATE TABLE` and `DROP TABLE`?
**Keywords:** rows, WHERE, structure, TRUNCATE, SQLite
<details>
<summary>Click to Reveal Answer</summary>

`DELETE FROM t WHERE ...` removes chosen rows (or every row if you forget the `WHERE`) and the table still exists. `TRUNCATE TABLE t` empties all rows quickly, cannot use `WHERE`, and is available in MySQL, PostgreSQL, SQL Server and Oracle but not in SQLite, where `DELETE FROM t;` is used instead. `DROP TABLE t` removes the data and the table structure itself. Many applications also use a "soft delete" (for example `status = 'inactive'`) so history is kept.

```sql
DELETE FROM customers WHERE customer_id = 8;   -- one row
DELETE FROM customers;                         -- every row (SQLite way to empty a table)
DROP TABLE completed_orders_archive;           -- the table is gone
```
</details>

*Source:* `insert-update-and-delete.md`

---

### Q2: What is the difference between a primary key and a foreign key?
**Keywords:** unique, not NULL, parent table, child table, referential integrity
<details>
<summary>Click to Reveal Answer</summary>

A primary key (PK) uniquely identifies each row: its values must be unique and not NULL, and a table can have only one. A foreign key (FK) is a column in a child table that refers to the primary key of a parent table, so every value must match an existing parent row (or be NULL). This is called referential integrity, and it is why you cannot have an order for a customer who does not exist. Joins work by matching a foreign key to a primary key.

```sql
-- customers.customer_id is the PK; orders.customer_id is the FK
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
```
</details>

*Source:* `basic-database-constraints-primary-and-foreign-keys.md`

---

### Q3: Name four constraints besides the primary key and foreign key rules, say what each enforces, and give an example of a "negative test" for one of them.
**Keywords:** NOT NULL, UNIQUE, CHECK, DEFAULT, negative test
<details>
<summary>Click to Reveal Answer</summary>

`NOT NULL` requires a value, `UNIQUE` stops two rows sharing a value, `CHECK` requires a condition to be true (such as `age >= 18`), and `DEFAULT` supplies a value when none is given (it is not really a rule). A negative test passes when the database refuses bad data, for example inserting a duplicate and expecting `UNIQUE constraint failed`. Missing constraints are findings too: `customers.email` has no `UNIQUE`, which is how the duplicate Bob Smith got in, and `order_items.quantity` has no `CHECK (quantity > 0)`, which is how `-1` got in.

```sql
CREATE TABLE demo_accounts (
    account_id INTEGER PRIMARY KEY,
    username   TEXT NOT NULL UNIQUE,
    age        INTEGER CHECK (age >= 18),
    status     TEXT NOT NULL DEFAULT 'active'
);
INSERT INTO demo_accounts (username, age) VALUES ('kid_qa', 12);   -- must fail: CHECK constraint
```
</details>

*Source:* `basic-database-constraints-primary-and-foreign-keys.md`

---

### Q4: What is the difference between an `INNER JOIN` and a `LEFT JOIN`?
**Keywords:** match, unmatched rows, NULL, left table, overlap
<details>
<summary>Click to Reveal Answer</summary>

An `INNER JOIN` returns only rows that have a match on both sides (the overlap); unmatched rows are dropped. A `LEFT JOIN` returns every row from the left table (the one in `FROM`), and where there is no match the right table's columns are `NULL`. On QA Shop, `customers INNER JOIN orders` returns 10 rows, while `customers LEFT JOIN orders` returns 14 because the four customers who never ordered (6, 8, 9, 10) are kept.

```sql
SELECT c.customer_id, c.full_name, o.order_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id;   -- 14 rows; INNER JOIN would give 10
```
</details>

*Source:* `inner-join.md`, `left-and-right-join.md`

---

### Q5: The `orders` table has 12 rows, but joining it to `customers` with an `INNER JOIN` returns only 10. Which orders disappeared and why?
**Keywords:** orphan, NULL, silently dropped, no match, compare counts
<details>
<summary>Click to Reveal Answer</summary>

Orders 107 and 108 disappeared. Order 107 has `customer_id` 99, which does not exist in `customers`, and order 108 has a `NULL` customer; since `NULL = anything` is never true, neither can match a customer. An inner join drops such rows silently, with no error, so it can hide exactly the data problems a tester is looking for. A good habit is to compare row counts before and after a join.

```sql
SELECT COUNT(*) FROM orders;                                   -- 12
SELECT COUNT(*) FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id;    -- 10
```
</details>

*Source:* `inner-join.md`

---

### Q6: What does a `RIGHT JOIN` do, and how is it related to a `LEFT JOIN`? Why do many teams write only `LEFT JOIN`?
**Keywords:** mirror image, swap tables, all rows from right, readability, SQLite 3.39
<details>
<summary>Click to Reveal Answer</summary>

A `RIGHT JOIN` keeps all rows from the right table (the one after `JOIN`) and fills the left side with `NULL` when there is no match. It is the mirror image of `LEFT JOIN`: swapping the table order turns one into the other and gives identical rows. Many style guides prefer only `LEFT JOIN`, with the table you want to keep in full in `FROM`, because queries read more easily top to bottom. You should still recognise `RIGHT JOIN`, and note that SQLite added it only in version 3.39.0, so on older SQLite you must rewrite it as a `LEFT JOIN`.

```sql
-- these two return the same rows
SELECT o.order_id, c.customer_id FROM orders AS o RIGHT JOIN customers AS c ON o.customer_id = c.customer_id;
SELECT o.order_id, c.customer_id FROM customers AS c LEFT JOIN orders AS o ON o.customer_id = c.customer_id;
```
</details>

*Source:* `left-and-right-join.md`

---

### Q7: What does a `FULL JOIN` return? Using `customers FULL JOIN orders`, explain how the 16 result rows break down.
**Keywords:** matched, left-only, right-only, both tables, NULL
<details>
<summary>Click to Reveal Answer</summary>

A `FULL JOIN` (`FULL OUTER JOIN`) returns all rows from both tables: matched rows combined, left-only rows with `NULL` on the right, and right-only rows with `NULL` on the left. For `customers FULL JOIN orders` the 16 rows are 10 matched, 4 left-only (customers 6, 8, 9, 10 with no orders) and 2 right-only (orders 107 and 108 with no customer). Keeping only rows where either primary key is `NULL` gives a two-sided mismatch report.

```sql
SELECT c.customer_id, c.full_name, o.order_id
FROM customers AS c
FULL JOIN orders AS o ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL OR o.order_id IS NULL;     -- the 6 mismatching rows
```
</details>

*Source:* `full-join.md`

---

### Q8: Which common databases do not support `FULL JOIN`, and how can you emulate it?
**Keywords:** MySQL, older SQLite, LEFT JOIN, UNION, anti-join
<details>
<summary>Click to Reveal Answer</summary>

MySQL/MariaDB and SQLite versions older than 3.39 do not support `FULL JOIN` (PostgreSQL, SQL Server, Oracle and SQLite 3.39+ do). A full join is everything from a `LEFT JOIN` plus the right-only rows, so you stack a `LEFT JOIN` with a second `LEFT JOIN` with the tables swapped, keeping the same columns in the same order. Plain `UNION` removes the duplicated matched rows but can also merge genuinely identical rows; the exact recipe uses `UNION ALL` and an anti-join (`IS NULL`) in the second half. Both recipes return the same 16 rows as the real `FULL JOIN` on QA Shop.

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM customers AS c LEFT JOIN orders AS o ON o.customer_id = c.customer_id
UNION ALL
SELECT NULL, NULL, o.order_id, o.status
FROM orders AS o LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;
```
</details>

*Source:* `full-join.md`

---

### Q9: What is a subquery? Explain scalar and list subqueries with an example.
**Keywords:** nested SELECT, parentheses, scalar, IN, outer query
<details>
<summary>Click to Reveal Answer</summary>

A subquery is a `SELECT` written inside another statement, wrapped in parentheses; the surrounding statement is the outer query. A scalar subquery returns exactly one value (one row, one column) and can be used where a single value is allowed, such as comparing against an average. A list subquery returns one column of many rows and is used with `IN`. Subqueries can sit in `WHERE`, in `FROM` (where an alias is required) or in the `SELECT` list, and also inside `UPDATE` and `DELETE`.

```sql
-- scalar: orders above the average order total
SELECT order_id, total_amount FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders);

-- list: customers who have at least one order
SELECT customer_id, full_name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders);
```
</details>

*Source:* `subqueries.md`

---

### Q10: What is the difference between `WHERE` and `HAVING`? Why does `WHERE COUNT(*) > 1` fail?
**Keywords:** rows, groups, before grouping, after grouping, aggregate
<details>
<summary>Click to Reveal Answer</summary>

`WHERE` filters individual rows before grouping, so it cannot use aggregates; `HAVING` filters whole groups after `GROUP BY` and is where conditions on aggregates belong. `WHERE COUNT(*) > 1` fails ("misuse of aggregate") because no groups exist yet when `WHERE` runs. A good rule is to put every condition that can go in `WHERE` there, since it removes rows earlier, and use `HAVING` only for aggregate conditions. The logical order is FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT.

```sql
SELECT customer_id, COUNT(*) AS completed_orders
FROM orders
WHERE status = 'completed'      -- row filter, applied first
GROUP BY customer_id
HAVING COUNT(*) > 1;            -- group filter, applied after grouping
```
</details>

*Source:* `group-by-and-having.md`

---

### Q11: You need to connect `customers` and `products`, which are not directly linked. How do you find the join path, and how do you build the query safely?
**Keywords:** foreign key arrows, bridge table, n-1 joins, one join at a time, row counts
<details>
<summary>Click to Reveal Answer</summary>

Walk the primary key/foreign key arrows between the tables: customers, orders, order_items, products (`order_items` is the bridge table between orders and products). Each arrow becomes one `JOIN ... ON child.fk = parent.pk`, so four tables need three joins. Build the query one join at a time and check the row count after each step so you can see exactly where rows disappear or multiply. On QA Shop the counts go 12 (orders), 10 (add customers: 107 and 108 drop), 13 (add items: multi-line orders repeat, order 109 drops), 12 (add products: item 15 drops).

```sql
SELECT COUNT(*) AS rows_now
FROM orders AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
INNER JOIN products    AS p ON p.product_id  = i.product_id;   -- 12
```
</details>

*Source:* `multi-table-queries.md`

---

### Q12: What is the difference between `COUNT(*)`, `COUNT(column)` and `COUNT(DISTINCT column)`? How would you use them to spot missing and duplicate emails?
**Keywords:** rows, non-NULL, DISTINCT, missing values, duplicates
<details>
<summary>Click to Reveal Answer</summary>

`COUNT(*)` counts rows, `COUNT(column)` counts only rows where the column is not NULL, and `COUNT(DISTINCT column)` counts different non-NULL values. On `customers` there are 10 rows, 9 non-NULL emails and 8 distinct emails. So `COUNT(*) - COUNT(email)` is the number of missing emails (1) and `COUNT(email) - COUNT(DISTINCT email)` is the number of duplicate email rows (1). After a `LEFT JOIN`, count a right-table primary key (`COUNT(o.order_id)`), not `COUNT(*)`, or customers with no orders look as if they have one.

```sql
SELECT COUNT(*)                         AS all_rows,
       COUNT(email)                     AS with_email,
       COUNT(DISTINCT email)            AS unique_emails,
       COUNT(*) - COUNT(email)          AS missing_emails,
       COUNT(email) - COUNT(DISTINCT email) AS duplicate_email_rows
FROM customers;      -- 10, 9, 8, 1, 1
```
</details>

*Source:* `aggregate-functions.md`

---

### Q13: How do `SUM`, `AVG`, `MIN` and `MAX` treat `NULL` values, and what do they return over an empty set?
**Keywords:** ignored, divisor, NULL, COALESCE, empty set
<details>
<summary>Click to Reveal Answer</summary>

`SUM`, `AVG`, `MIN` and `MAX` ignore NULLs, and `AVG` divides by the count of non-NULL values only. For the values 10, 20 and NULL, `AVG` is 15 (30 divided by 2), not 10. If the business rule says "missing means zero", use `AVG(COALESCE(x, 0))`. Over an empty set `COUNT(*)` returns 0 but `SUM`, `AVG`, `MIN` and `MAX` return NULL, so test code should handle that, for example with `COALESCE(SUM(...), 0)`.

```sql
SELECT COUNT(*), COUNT(x), SUM(x), AVG(x), AVG(COALESCE(x, 0))
FROM (SELECT 10 AS x UNION ALL SELECT 20 UNION ALL SELECT NULL);   -- 3, 2, 30, 15.0, 10.0

SELECT COUNT(*), SUM(total_amount) FROM orders WHERE status = 'returned';   -- 0, NULL
```
</details>

*Source:* `aggregate-functions.md`

---

### Q14: What is the "violations query" pattern in test-data validation, and why is it useful?
**Keywords:** rows that break the rule, zero rows = pass, evidence, assertion
<details>
<summary>Click to Reveal Answer</summary>

Every check is written as a query that returns the rows that break a rule: no rows (or a count of 0) means the check passes, and any row returned is a failure and your evidence. It is easy to read, works for any rule (uniqueness, referential integrity, ranges, consistency, business rules) and the failing rows tell you exactly what to fix or report. It also suits automation, because a test can simply assert that the result is empty. Return the rows while investigating, and use counts for dashboards.

```sql
-- Rule: quantity must be positive. Passes only if this returns no rows.
SELECT item_id, order_id, quantity
FROM order_items
WHERE quantity <= 0;      -- returns item 16 (quantity -1), so the check FAILS
```
</details>

*Source:* `test-data-validation-using-sql.md`

---

## Intermediate (Application)

### Q15: Order 110 has a `total_amount` of 55.00, but its lines add up to 50.00, and the team agrees the lines are correct. How do you fix the header safely, and how do you protect yourself from a bad `UPDATE` or `DELETE`?
**Hint:** Think "SELECT first, then change", the rows-affected count and `BEGIN`/`ROLLBACK`.
<details>
<summary>Click to Reveal Answer</summary>

Preview the target rows with a `SELECT` that has the same `WHERE`, then run the `UPDATE` with a `WHERE` on the primary key, and verify afterwards. Check the "rows affected" count: if you expected 1 and see 12, stop. Wrap risky work in `BEGIN ... ROLLBACK/COMMIT` so you can undo it, because an `UPDATE` or `DELETE` without `WHERE` changes every row (in the lesson an `UPDATE orders SET status = 'cancelled'` affected all 12 orders until rolled back). Work in a test database, never production, and when deleting remember to delete child rows before parent rows.

```sql
BEGIN;

SELECT order_id, total_amount FROM orders WHERE order_id = 110;      -- preview: 1 row

UPDATE orders
SET total_amount = (SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = 110)
WHERE order_id = 110;                                                -- expect 1 row affected

SELECT order_id, total_amount FROM orders WHERE order_id = 110;      -- verify: 50.0
COMMIT;      -- or ROLLBACK; if anything looks wrong
```
</details>

*Source:* `insert-update-and-delete.md`

---

### Q16: A report built with an `INNER JOIN` between `orders` and `customers` looks fine. How do you find orders whose customer does not exist, and how do you tell a true orphan from a guest order?
**Hint:** Keep every order, then look for `NULL` on the customer side. Which column should you test for `NULL`?
<details>
<summary>Click to Reveal Answer</summary>

Use the anti-join pattern: `LEFT JOIN` from `orders` to `customers` and keep rows where the customer's primary key `IS NULL`, meaning no match was found. Test the right table's primary key, not a nullable column, so a `NULL` can only mean "no match". This returns orders 107 and 108, but they are different cases: order 107 has `customer_id` 99 that matches no customer (a true referential-integrity violation), while order 108 has a `NULL` customer (a guest order, which may be acceptable). Adding `o.customer_id IS NOT NULL` isolates the real orphan, and whether guests are allowed is a question for the product owner.

```sql
SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
  AND o.customer_id IS NOT NULL;      -- only order 107
```
</details>

*Source:* `left-and-right-join.md`

---

### Q17: How would you detect duplicate data in `customers`, `order_items` and `payments`?
**Hint:** Decide which columns define "the same" (the business key), then group by them.
<details>
<summary>Click to Reveal Answer</summary>

Decide which column or combination should be unique, `GROUP BY` it, and keep groups with `HAVING COUNT(*) > 1`. Use the business key rather than a name, because two different people can share a name; for customers use `email` (ignoring NULL, which is a different problem). The same recipe finds the duplicate item row on order 103 (items 5 and 13) and the possible double charge on order 102 (payments 2 and 11); `GROUP_CONCAT` lists the IDs as evidence (SQLite/MySQL; PostgreSQL and SQL Server use `STRING_AGG`). A test would assert that each query returns zero rows. Note that a join alone does not reveal duplicates.

```sql
SELECT email, COUNT(*) AS occurrences, GROUP_CONCAT(customer_id) AS customer_ids
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;                                   -- bob@example.com, 2, '2,8'

SELECT order_id, product_id, COUNT(*) AS n, GROUP_CONCAT(item_id) AS item_ids
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;                                   -- order 103, product 4, '5,13'
```
</details>

*Source:* `group-by-and-having.md`, `test-data-validation-using-sql.md`

---

### Q18: You join `orders` to both `order_items` and `payments` and sum the amounts, and the figures for order 102 come out doubled. What is happening and how do you fix it?
**Hint:** Count how many rows order 102 produces after both joins.
<details>
<summary>Click to Reveal Answer</summary>

This is a fan-out: two independent one-to-many tables (items and payments) are joined to the same parent, so every item row is paired with every payment row. Order 102 has 2 items and 2 payments (the double payment), which gives 2 x 2 = 4 rows, so `SUM(pay.amount)` returns 121.92 instead of 60.96. The fix is to aggregate each child table separately in a subquery (one row per order) and then join those results to `orders`, so no multiplication can occur. The same applies to summing a parent column such as `o.total_amount` after joining to its children.

```sql
SELECT o.order_id, o.total_amount AS header_total, it.items_total, pa.paid_total
FROM orders AS o
LEFT JOIN (SELECT order_id, SUM(quantity * unit_price) AS items_total
           FROM order_items GROUP BY order_id) AS it ON it.order_id = o.order_id
LEFT JOIN (SELECT order_id, SUM(amount) AS paid_total
           FROM payments WHERE status = 'paid' GROUP BY order_id) AS pa ON pa.order_id = o.order_id
WHERE o.order_id = 102;        -- 30.48, 30.48, 60.96 (the paid total exposes the double payment)
```
</details>

*Source:* `multi-table-queries.md`

---

### Q19: Write a check that finds orders whose header `total_amount` does not match the sum of their line items. Which orders should it return on QA Shop, and why must you be careful with the join type?
**Hint:** Which orders have no lines at all, and what happens to them in an `INNER JOIN`?
<details>
<summary>Click to Reveal Answer</summary>

Pre-aggregate the lines per order in a derived table, `LEFT JOIN` it from `orders`, and compare rounded values, using `COALESCE(items_total, 0)` so that an order with no lines is reported. It returns four orders: 103 (the duplicate item row doubles the items total to 300 against a header of 150), 109 (header 80.00 but no lines at all), 110 (55.00 against 50.00) and 112 (the negative-quantity line makes the items total -9.99). With an `INNER JOIN` to the derived table, order 109 would silently drop out and you would report only three. `ROUND(..., 2)` guards against floating-point noise, so never compare money with a bare `=`.

```sql
SELECT o.order_id, o.total_amount AS header_total, it.items_total
FROM orders AS o
LEFT JOIN (SELECT order_id, SUM(quantity * unit_price) AS items_total
           FROM order_items GROUP BY order_id) AS it ON it.order_id = o.order_id
WHERE ROUND(o.total_amount, 2) <> ROUND(COALESCE(it.items_total, 0), 2)
ORDER BY o.order_id;           -- 103, 109, 110, 112
```
</details>

*Source:* `test-data-validation-using-sql.md`, `subqueries.md`

---

## Advanced (Deep Dive)

### Q20: A teammate finds customers who never ordered with `WHERE customer_id NOT IN (SELECT customer_id FROM orders)`, and the query returns zero rows, even though customers 6, 8, 9 and 10 have no orders. What went wrong, and how would you fix it?
**Hint:** Look at the list the subquery produces. Does `orders.customer_id` ever contain a `NULL`?
<details>
<summary>Click to Reveal Answer</summary>

The subquery's list contains a `NULL` (order 108 is a guest order with no customer). `x NOT IN (1, 2, 99, NULL)` means `x <> 1 AND x <> 2 AND x <> 99 AND x <> NULL`, and `x <> NULL` is unknown, never true, so the whole condition can never be true and **a single NULL in the list makes `NOT IN` return nothing**. It is a classic bug because the query looks right and test data without NULLs hides it. Safe fixes are to filter the NULLs out in the subquery, to use the NULL-safe `NOT EXISTS` (preferred), or to use the `LEFT JOIN ... IS NULL` anti-join; all return customers 6, 8, 9 and 10. `NOT IN` is safe only when the subquery column cannot be NULL, such as a primary key, so always ask "can this column be NULL?".

```sql
-- Fix 1: filter NULLs out of the list
SELECT customer_id, full_name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL);

-- Fix 2 (preferred): NOT EXISTS
SELECT c.customer_id, c.full_name FROM customers AS c
WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id);

-- Fix 3: anti-join
SELECT c.customer_id, c.full_name FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```
</details>

*Source:* `subqueries.md`

---

## How to use this bank

This bank is for self-quizzing, so do not read the answers first.

1. Read a question and cover the answer (keep the `<details>` block closed).
2. Say your answer aloud as if you were in an interview, in 30 to 60 seconds. Use the hint only if you are stuck.
3. Open the answer and check that every **keyword** appeared in what you said. If you missed one, repeat the question until you can include it naturally.
4. Work through Beginner first until you can answer without notes, then attempt Intermediate (talk through the scenario step by step, writing the SQL as you go), then the Advanced question.
5. If you struggle with a topic, re-read the lesson named in the *Source* line and try again the next day. Re-running the snippets against the QA Shop setup script (in `insert-update-and-delete.md`) is the fastest way to make them stick.
