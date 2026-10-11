# FULL JOIN

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a `FULL (OUTER) JOIN` returns and how it relates to inner, left and right joins.
- Write `FULL JOIN` queries and read the three kinds of rows they produce: matched, left-only and right-only.
- Use `CASE` to label each result row as `matched`, `left only` or `right only`.
- Find mismatches on **both sides at once** (a reconciliation query).
- Emulate a FULL JOIN with `LEFT JOIN ... UNION ... LEFT JOIN` on databases that lack it (MySQL, old SQLite) and prove that the emulation gives the same answer.
- State which databases support `FULL JOIN` and which do not.
- Apply FULL JOIN to QA tasks such as comparing a source and target after a data migration.

## Practice Database Recap

This lesson uses the same six-table **QA Shop** database as the rest of today's lessons (full `CREATE TABLE` and `INSERT` script in the lesson "INSERT, UPDATE and DELETE"; run it once to get a fresh copy):

| Table | Columns |
|---|---|
| `customers` | `customer_id` (PK), `full_name`, `email`, `country`, `created_date` |
| `products` | `product_id` (PK), `product_name`, `category`, `unit_price` |
| `orders` | `order_id` (PK), `customer_id` (FK), `order_date`, `status`, `total_amount` |
| `order_items` | `item_id` (PK), `order_id` (FK), `product_id` (FK), `quantity`, `unit_price` |
| `payments` | `payment_id` (PK), `order_id` (FK), `amount`, `method`, `status` |
| `defects` | `defect_id` (PK), `product_id` (FK, nullable), `title`, `severity`, `status`, `found_date` |

Deliberate data problems (planted bugs) you should keep in mind: duplicate customer (IDs 2 and 8, same email); NULL email (customer 6); customers 6, 8, 9, 10 never ordered; order 107 has customer 99 who does not exist; order 108 has a NULL customer (guest); order 109 has no items; order totals that do not match their items (103, 110, 112; order 109 also fails this check because it has no items at all); duplicate item rows (IDs 5 and 13); item 14 points to missing order 999; item 15 points to missing product 999; item 16 has quantity -1; payment 10 points to missing order 888; payments 2 and 11 are duplicates; products 7 and 8 were never sold; defect 3 has no product.

## Why This Matters

This week's epic is using SQL for QA data validation, and it feeds your Project 1 "QE Foundations" capstone. In the last lesson, you used `LEFT JOIN ... IS NULL` to look in one direction: "which orders have no customer?". But validation is often two-sided:

- After a **data migration**, you must check that nothing was lost (rows in the old system but not the new one) *and* that nothing unexpected appeared (rows in the new system but not the old one).
- When **reconciling** orders and payments you want to find orders with no payment *and* payments with no order, in one report.
- When comparing **expected test data** with **actual** results, both missing and extra rows are failures.

`FULL JOIN` is the join built for that two-sided question. It is less common than `INNER` and `LEFT` in everyday application queries, but for QA reconciliation it is a precise and powerful tool.

## The Concept

### 1. What FULL JOIN does

A `FULL JOIN` (also written `FULL OUTER JOIN`) returns **all rows from both tables**:

- rows that **match** are combined into one row (like an inner join),
- rows from the left table **without a match** appear with NULLs for the right columns (like a left join),
- rows from the right table **without a match** appear with NULLs for the left columns (like a right join).

In a Venn diagram, it is both circles, completely filled:

```text
 INNER JOIN        LEFT JOIN         RIGHT JOIN        FULL JOIN
  (  [##]  )       ([####]  )        (  [####])        ([######])
  overlap only     left + overlap    overlap + right   everything
```

Another way to see it: `FULL JOIN` = `INNER JOIN` + left-only rows + right-only rows.

### 2. Syntax

```text
SELECT  columns
FROM    table_a
FULL JOIN table_b
        ON table_a.key = table_b.key;
```

`FULL OUTER JOIN` is the same thing; `OUTER` is optional.

### 3. Support in SQLite and other databases

SQLite added `RIGHT JOIN` and `FULL JOIN` in version 3.39.0 (2022). Check yours:

```sql
SELECT sqlite_version() AS sqlite_version;
```

**Result:**

```text
sqlite_version
--------------
3.45.1
(1 row)
```

All examples here ran on SQLite 3.45.1, so they use real `FULL JOIN`. If your SQLite is older than 3.39 (you will see "RIGHT and FULL OUTER JOINs are not currently supported"), or if you work in MySQL, use the emulation in section 6.

| Database | FULL JOIN support |
|---|---|
| PostgreSQL | Yes |
| SQL Server | Yes |
| Oracle | Yes |
| SQLite 3.39 and newer | Yes |
| SQLite older than 3.39 | No (emulate) |
| MySQL / MariaDB | **No** (emulate) |

### 4. Our first FULL JOIN: customers and orders

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.customer_id AS order_customer_id, o.status
FROM customers AS c
FULL JOIN orders AS o ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
customer_id | full_name     | order_id | order_customer_id | status
------------+---------------+----------+-------------------+----------
NULL        | NULL          | 107      | 99                | completed
NULL        | NULL          | 108      | NULL              | completed
1           | Alice Johnson | 101      | 1                 | completed
1           | Alice Johnson | 102      | 1                 | completed
2           | Bob Smith     | 103      | 2                 | completed
2           | Bob Smith     | 110      | 2                 | completed
3           | Carla Gomez   | 104      | 3                 | shipped
3           | Carla Gomez   | 111      | 3                 | completed
4           | Dev Patel     | 105      | 4                 | pending
5           | Eve Muller    | 106      | 5                 | cancelled
6           | Frank Lee     | NULL     | NULL              | NULL
7           | Grace Kim     | 109      | 7                 | pending
7           | Grace Kim     | 112      | 7                 | completed
8           | Bob Smith     | NULL     | NULL              | NULL
9           | Hana Sato     | NULL     | NULL              | NULL
10          | Ian Brooks    | NULL     | NULL              | NULL
(16 rows)
```

Study the three kinds of rows:

1. **Matched rows**: for example customer 1 with orders 101 and 102.
2. **Left-only rows**: customers with `order_id` NULL: Frank Lee (6), the duplicate Bob (8), Hana (9), Ian (10). They exist in `customers` but have no orders.
3. **Right-only rows**: the rows at the bottom where `customer_id` and `full_name` are NULL: orders 107 (customer 99) and 108 (NULL customer). They exist in `orders` but have no customer.

(SQLite places NULLs first when sorting ascending, which is why the right-only rows appear at the top of the result. Other databases may sort NULLs last; always add an explicit `ORDER BY` when you need a stable order, and do not depend on where NULLs land.)

Count them: the row total is 10 matched + 4 left-only + 2 right-only = 16.

```sql
SELECT COUNT(*) AS total_rows
FROM customers AS c
FULL JOIN orders AS o ON o.customer_id = c.customer_id;
```

**Result:**

```text
total_rows
----------
16
(1 row)
```

### 5. Labelling rows with CASE

Reading NULLs by eye does not scale. The SQL `CASE` expression works like if / elif / else: it checks conditions in order and returns the value for the first one that is true. (It is not yet a core Week 2 topic; we use it here just as a labelling tool.)

```text
CASE
   WHEN condition1 THEN result1
   WHEN condition2 THEN result2
   ELSE default_result
END
```

Now let us tag every row of the full join:

```sql
SELECT
  CASE
    WHEN c.customer_id IS NULL THEN 'right only (order has no customer)'
    WHEN o.order_id    IS NULL THEN 'left only (customer has no orders)'
    ELSE 'matched'
  END AS row_type,
  c.customer_id,
  c.full_name,
  o.order_id
FROM customers AS c
FULL JOIN orders AS o ON o.customer_id = c.customer_id
ORDER BY row_type, c.customer_id, o.order_id;
```

**Result:**

```text
row_type                           | customer_id | full_name     | order_id
-----------------------------------+-------------+---------------+---------
left only (customer has no orders) | 6           | Frank Lee     | NULL
left only (customer has no orders) | 8           | Bob Smith     | NULL
left only (customer has no orders) | 9           | Hana Sato     | NULL
left only (customer has no orders) | 10          | Ian Brooks    | NULL
matched                            | 1           | Alice Johnson | 101
matched                            | 1           | Alice Johnson | 102
matched                            | 2           | Bob Smith     | 103
matched                            | 2           | Bob Smith     | 110
matched                            | 3           | Carla Gomez   | 104
matched                            | 3           | Carla Gomez   | 111
matched                            | 4           | Dev Patel     | 105
matched                            | 5           | Eve Muller    | 106
matched                            | 7           | Grace Kim     | 109
matched                            | 7           | Grace Kim     | 112
right only (order has no customer) | NULL        | NULL          | 107
right only (order has no customer) | NULL        | NULL          | 108
(16 rows)
```

We test the **primary keys** (`c.customer_id`, `o.order_id`) for NULL, because a primary key is never NULL in a real row; so a NULL key means "no row came from that side".

Now let us summarise by type. Grouping is explained in a later lesson today; for now read it as "count the rows of each type":

```sql
SELECT row_type, COUNT(*) AS row_count
FROM (
    SELECT CASE
             WHEN c.customer_id IS NULL THEN 'right only'
             WHEN o.order_id    IS NULL THEN 'left only'
             ELSE 'matched'
           END AS row_type
    FROM customers AS c
    FULL JOIN orders AS o ON o.customer_id = c.customer_id
)
GROUP BY row_type
ORDER BY row_type;
```

**Result:**

```text
row_type   | row_count
-----------+----------
left only  | 4
matched    | 10
right only | 2
(3 rows)
```

### 6. Keeping only the mismatches (two-sided anti-join)

Add `WHERE left_pk IS NULL OR right_pk IS NULL` to keep only the rows that failed to match on either side. This is the heart of a reconciliation report:

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.customer_id AS order_customer_id
FROM customers AS c
FULL JOIN orders AS o ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL OR o.order_id IS NULL
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
customer_id | full_name  | order_id | order_customer_id
------------+------------+----------+------------------
NULL        | NULL       | 107      | 99
NULL        | NULL       | 108      | NULL
6           | Frank Lee  | NULL     | NULL
8           | Bob Smith  | NULL     | NULL
9           | Hana Sato  | NULL     | NULL
10          | Ian Brooks | NULL     | NULL
(6 rows)
```

Six rows: the four customers with no orders and the two orders with no customer. Compare with the `LEFT JOIN` lesson, where you needed **two separate queries** to find these.

### 7. More FULL JOIN examples on our data

#### Orders vs payments

Which orders have no payment record, and which payments have no order? (Both directions in a single query.)

```sql
SELECT o.order_id, o.status, o.total_amount,
       pay.payment_id, pay.order_id AS payment_order_id, pay.amount
FROM orders AS o
FULL JOIN payments AS pay ON pay.order_id = o.order_id
WHERE o.order_id IS NULL OR pay.payment_id IS NULL
ORDER BY o.order_id, pay.payment_id;
```

**Result:**

```text
order_id | status    | total_amount | payment_id | payment_order_id | amount
---------+-----------+--------------+------------+------------------+-------
NULL     | NULL      | NULL         | 10         | 888              | 10.0
105      | pending   | 34.99        | NULL       | NULL             | NULL
109      | pending   | 80.0         | NULL       | NULL             | NULL
112      | completed | 9.99         | NULL       | NULL             | NULL
(4 rows)
```

Reading the result:

- Payment 10 refers to order 888, which does not exist (right-only: an orphan payment).
- Orders 105, 109 and 112 have no payment. 105 and 109 are `pending` (expected: not paid yet), but **112 is `completed`** with no payment, which is suspicious.

Notice that order 102 (two payment rows, 2 and 11) is *not* in this result, because it matches. FULL JOIN tells you about missing partners, not about duplicates; duplicates require `GROUP BY ... HAVING`, covered in a later lesson today.

#### Order items vs orders

```sql
SELECT i.item_id, i.order_id AS item_order_id,
       o.order_id, o.status
FROM order_items AS i
FULL JOIN orders AS o ON o.order_id = i.order_id
WHERE i.item_id IS NULL OR o.order_id IS NULL
ORDER BY o.order_id, i.item_id;
```

**Result:**

```text
item_id | item_order_id | order_id | status
--------+---------------+----------+--------
14      | 999           | NULL     | NULL
NULL    | NULL          | 109      | pending
(2 rows)
```

Item 14 (order 999 missing) and order 109 (no items) are found together.

### 8. Emulating FULL JOIN where it is not supported

If your database lacks `FULL JOIN`, you build it from parts. A full join is:

> everything from a **LEFT JOIN**, plus the **right-only** rows.

Two standard recipes follow. Both give identical results, and both are widely used in MySQL.

#### Recipe A: UNION of a LEFT JOIN and a RIGHT JOIN

(MySQL supports `RIGHT JOIN`, so this is common there.)

```text
SELECT ... FROM a LEFT  JOIN b ON ...
UNION
SELECT ... FROM a RIGHT JOIN b ON ...
```

#### Recipe B: UNION of two LEFT JOINs (works even on old SQLite, which lacks RIGHT JOIN)

Swap the tables in the second query, so it is also a LEFT JOIN, and **select the same columns in the same order** in both queries:

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id

UNION

SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id

ORDER BY 1, 3;
```

**Result:**

```text
customer_id | full_name     | order_id | status
------------+---------------+----------+----------
NULL        | NULL          | 107      | completed
NULL        | NULL          | 108      | completed
1           | Alice Johnson | 101      | completed
1           | Alice Johnson | 102      | completed
2           | Bob Smith     | 103      | completed
2           | Bob Smith     | 110      | completed
3           | Carla Gomez   | 104      | shipped
3           | Carla Gomez   | 111      | completed
4           | Dev Patel     | 105      | pending
5           | Eve Muller    | 106      | cancelled
6           | Frank Lee     | NULL     | NULL
7           | Grace Kim     | 109      | pending
7           | Grace Kim     | 112      | completed
8           | Bob Smith     | NULL     | NULL
9           | Hana Sato     | NULL     | NULL
10          | Ian Brooks    | NULL     | NULL
(16 rows)
```

How it works:

1. The first query returns all customers plus matching orders (matched + left-only rows).
2. The second query returns all orders plus matching customers (matched + right-only rows). Notice we kept the SELECT list identical, `c.customer_id, c.full_name, o.order_id, o.status`, so the columns line up.
3. `UNION` stacks the two results and **removes duplicate rows**. The matched rows appear in both queries, so `UNION` collapses them into one copy each.
4. `ORDER BY 1, 3` sorts by output column positions 1 and 3 (`customer_id`, `order_id`).

16 rows again, identical to the real FULL JOIN.

#### UNION vs UNION ALL, and a trap

- `UNION` removes duplicates; `UNION ALL` keeps every row.
- Using `UNION ALL` in the emulation would **duplicate the matched rows** (they appear in both halves).
- Using `UNION` can wrongly collapse rows that are *genuinely* identical in your result columns. For example, if two different orders were identical in every selected column, `UNION` would merge them, and your count would be too small.

The most exact emulation avoids both problems by adding the right-only rows with `UNION ALL`:

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id

UNION ALL

SELECT NULL, NULL, o.order_id, o.status
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL

ORDER BY 1, 3;
```

**Result:**

```text
customer_id | full_name     | order_id | status
------------+---------------+----------+----------
NULL        | NULL          | 107      | completed
NULL        | NULL          | 108      | completed
1           | Alice Johnson | 101      | completed
1           | Alice Johnson | 102      | completed
2           | Bob Smith     | 103      | completed
2           | Bob Smith     | 110      | completed
3           | Carla Gomez   | 104      | shipped
3           | Carla Gomez   | 111      | completed
4           | Dev Patel     | 105      | pending
5           | Eve Muller    | 106      | cancelled
6           | Frank Lee     | NULL     | NULL
7           | Grace Kim     | 109      | pending
7           | Grace Kim     | 112      | completed
8           | Bob Smith     | NULL     | NULL
9           | Hana Sato     | NULL     | NULL
10          | Ian Brooks    | NULL     | NULL
(16 rows)
```

The first half gives matched and left-only rows. The second half gives **only right-only rows** (anti-join), so nothing is double-counted; and because no customer exists for those rows we can output `NULL` for the customer columns. Result: the same 16 rows.

#### Proving two queries return the same rows

A tester should not just trust an emulation. We can verify it using `EXCEPT`, which returns rows in the first result that are not in the second. If both directions return zero rows, the results are identical:

```sql
WITH real_full AS (
    SELECT c.customer_id, c.full_name, o.order_id, o.status
    FROM customers AS c
    FULL JOIN orders AS o ON o.customer_id = c.customer_id
),
emulated AS (
    SELECT c.customer_id, c.full_name, o.order_id, o.status
    FROM customers AS c
    LEFT JOIN orders AS o ON o.customer_id = c.customer_id
    UNION ALL
    SELECT NULL, NULL, o.order_id, o.status
    FROM orders AS o
    LEFT JOIN customers AS c ON c.customer_id = o.customer_id
    WHERE c.customer_id IS NULL
)
SELECT 'real minus emulated' AS direction, COUNT(*) AS different_rows
FROM (SELECT * FROM real_full EXCEPT SELECT * FROM emulated)
UNION ALL
SELECT 'emulated minus real', COUNT(*)
FROM (SELECT * FROM emulated EXCEPT SELECT * FROM real_full);
```

**Result:**

```text
direction           | different_rows
--------------------+---------------
real minus emulated | 0
emulated minus real | 0
(2 rows)
```

A short explanation of the new syntax: `WITH name AS ( ... )` gives a query a temporary name so you can use it like a table further down. Here `real_full` is the true FULL JOIN and `emulated` is our recipe. Both `EXCEPT` directions return 0 differing rows, so the emulation is exactly equivalent. (Named temporary queries like this are a handy readability tool; you do not need to master them today.)

This comparison technique (two `EXCEPT`s) is itself a good validation tool: it compares any two result sets. We will use similar thinking in the "Test-data validation using SQL" lesson.

### 9. A QA reconciliation example: before and after a migration

A team migrates customers to a new system. You receive a copy of the migrated table and must check it against the source. We create two small scratch tables for the demonstration:

```sql
CREATE TABLE demo_source_customers (customer_id INTEGER, email TEXT);
CREATE TABLE demo_migrated_customers (customer_id INTEGER, email TEXT);

INSERT INTO demo_source_customers VALUES
   (1, 'alice@example.com'),
   (2, 'bob@example.com'),
   (3, 'carla@example.com'),
   (4, 'dev@example.com');

INSERT INTO demo_migrated_customers VALUES
   (1, 'alice@example.com'),
   (2, 'bob@EXAMPLE.com'),     -- changed case
   (4, 'dev@example.com'),
   (5, 'extra@example.com');    -- appeared from nowhere
```

**Result:**

```text
OK

OK

OK: 4 row(s) affected

OK: 4 row(s) affected
```

Now one FULL JOIN gives the full migration report:

```sql
SELECT
  COALESCE(s.customer_id, m.customer_id) AS customer_id,
  CASE
    WHEN m.customer_id IS NULL THEN 'MISSING in target'
    WHEN s.customer_id IS NULL THEN 'EXTRA in target'
    WHEN s.email <> m.email    THEN 'EMAIL DIFFERS'
    ELSE 'OK'
  END AS result,
  s.email AS source_email,
  m.email AS target_email
FROM demo_source_customers AS s
FULL JOIN demo_migrated_customers AS m ON m.customer_id = s.customer_id
ORDER BY customer_id;
```

**Result:**

```text
customer_id | result            | source_email      | target_email
------------+-------------------+-------------------+------------------
1           | OK                | alice@example.com | alice@example.com
2           | EMAIL DIFFERS     | bob@example.com   | bob@EXAMPLE.com
3           | MISSING in target | carla@example.com | NULL
4           | OK                | dev@example.com   | dev@example.com
5           | EXTRA in target   | NULL              | extra@example.com
(5 rows)
```

In one pass: customer 3 was **lost**, customer 5 is **extra**, customer 2's email was altered (case), and customers 1 and 4 migrated correctly. `COALESCE` picks the ID from whichever side has it. In a real project, tests would assert that the number of non-OK rows is zero.

Clean up the scratch tables:

```sql
DROP TABLE demo_source_customers;
DROP TABLE demo_migrated_customers;
```

**Result:**

```text
OK

OK
```

### 10. When to use which join: a decision guide

| Question you are asking | Join to use |
|---|---|
| Show me related data, ignore anything unmatched | `INNER JOIN` |
| Show all of A, with B where it exists | `LEFT JOIN` |
| Which A rows have no B? | `LEFT JOIN ... WHERE b.pk IS NULL` |
| Compare two sets, find missing **and** extra in either direction | `FULL JOIN ... WHERE a.pk IS NULL OR b.pk IS NULL` |

Because `FULL JOIN` can multiply rows exactly like other joins, remember that one-to-many matches produce several output rows; reconcile on a **unique key** whenever you can.

### 11. Common mistakes

1. Using `FULL JOIN` in MySQL (syntax error) or in old SQLite.
2. Using `UNION ALL` of two full left joins in the emulation, which double-counts matched rows.
3. Using `UNION` when rows can be legitimately identical, silently merging them.
4. Different column lists or different column orders in the two halves of the `UNION`.
5. Detecting "no match" with a nullable column instead of the primary key.
6. Forgetting that duplicate rows (such as the double payment) are not revealed by a join alone.

## Practice Questions

**Q1.** Using `FULL JOIN`, list products and order lines where either side has no partner (products never ordered *and* lines with an unknown product).

**Q2.** How many rows does `payments FULL JOIN orders ON payments.order_id = orders.order_id` return? Explain the number by splitting it into matched, left-only and right-only.

**Q3.** Rewrite the Q1 query for MySQL (without `FULL JOIN`), using two LEFT JOINs and `UNION ALL` and an anti-join in the second half.

**Q4.** Why is `UNION` a risky choice for emulating `FULL JOIN` when your SELECT list contains only a few columns?

**Q5.** In the migration example, which output row would you raise a defect for first, and why?

### Answers

**A1.**

```sql
SELECT p.product_id, p.product_name, i.item_id, i.product_id AS item_product_id
FROM products AS p
FULL JOIN order_items AS i ON i.product_id = p.product_id
WHERE p.product_id IS NULL OR i.item_id IS NULL
ORDER BY p.product_id, i.item_id;
```

**Result:**

```text
product_id | product_name  | item_id | item_product_id
-----------+---------------+---------+----------------
NULL       | NULL          | 15      | 999
7          | Webcam HD     | NULL    | NULL
8          | Standing Desk | NULL    | NULL
(3 rows)
```

**A2.** Count it:

```sql
SELECT COUNT(*) AS total_rows
FROM payments AS pay
FULL JOIN orders AS o ON pay.order_id = o.order_id;
```

**Result:**

```text
total_rows
----------
14
(1 row)
```

Breakdown: there are 11 payments. Ten of them match an existing order (payments 1 to 9 and 11), so matched = 10 rows. Payment 10 refers to the missing order 888, so left-only = 1. The right-only rows are orders with no payment at all; the next query lists them:

```sql
SELECT o.order_id, o.status
FROM orders AS o
LEFT JOIN payments AS pay ON pay.order_id = o.order_id
WHERE pay.payment_id IS NULL
ORDER BY o.order_id;
```

**Result:**

```text
order_id | status
---------+----------
105      | pending
109      | pending
112      | completed
(3 rows)
```

Orders 105, 109 and 112 have no payments, so right-only = 3. Total = 10 + 1 + 3 = 14. (Orders 107 and 108 do have payments, numbers 6 and 7, so they are matched even though their *customer* is missing.)

**A3.**

```sql
SELECT p.product_id, p.product_name, i.item_id, i.product_id AS item_product_id
FROM products AS p
LEFT JOIN order_items AS i ON i.product_id = p.product_id
WHERE i.item_id IS NULL

UNION ALL

SELECT p.product_id, p.product_name, i.item_id, i.product_id
FROM order_items AS i
LEFT JOIN products AS p ON p.product_id = i.product_id
WHERE p.product_id IS NULL

ORDER BY 1, 3;
```

**Result:**

```text
product_id | product_name  | item_id | item_product_id
-----------+---------------+---------+----------------
NULL       | NULL          | 15      | 999
7          | Webcam HD     | NULL    | NULL
8          | Standing Desk | NULL    | NULL
(3 rows)
```

**A4.** `UNION` removes duplicates across the whole row. If two genuinely different source rows have identical values in every selected column, the emulation merges them and returns fewer rows than a real `FULL JOIN`. Including the primary keys of both tables in the SELECT list, or using the `UNION ALL` + anti-join recipe, avoids this.

**A5.** Customer 3 is **MISSING in target**: data loss is usually the most serious type of migration defect (a customer has disappeared). The extra row 5 and the email case difference also need triage, but missing rows are typically highest priority.

## Summary / Key Takeaways

- `FULL JOIN` returns matched rows, left-only rows and right-only rows: everything from both tables.
- Use `WHERE a.pk IS NULL OR b.pk IS NULL` to keep only mismatches, ideal for reconciliation after migrations or loads.
- Label rows with `CASE` and use `COALESCE` to show the key from whichever side has it.
- Supported by PostgreSQL, SQL Server, Oracle and SQLite 3.39+. **MySQL and older SQLite lack it**: emulate with LEFT JOIN + `UNION` (or LEFT JOIN + `UNION ALL` + anti-join).
- Verify emulations with `EXCEPT` in both directions.
- Joins find missing partners, not duplicates; duplicate detection uses grouping (later today).

## Additional Resources

- SQLite documentation, SELECT (outer joins, compound SELECT with UNION and EXCEPT): https://www.sqlite.org/lang_select.html
- PostgreSQL documentation, Joined Tables (FULL OUTER JOIN): https://www.postgresql.org/docs/current/queries-table-expressions.html
- MySQL Reference Manual, UNION clause (used to emulate FULL JOIN): https://dev.mysql.com/doc/refman/8.0/en/union.html
