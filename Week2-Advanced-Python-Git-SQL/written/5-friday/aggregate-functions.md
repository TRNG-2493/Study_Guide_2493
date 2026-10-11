# Aggregate Functions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an aggregate function is and how it differs from a row-by-row function.
- Use `COUNT(*)`, `COUNT(column)`, `COUNT(DISTINCT column)`, `SUM`, `AVG`, `MIN` and `MAX`.
- Predict how each aggregate treats `NULL` values and empty sets.
- Avoid the integer-division and floating-point rounding traps (`ROUND`, `CAST`).
- Use `GROUP_CONCAT` to list values, and conditional aggregation (`SUM(CASE WHEN ...)`) to count categories in one pass.
- Build a **data-profiling** query that summarises a table's size, NULLs, duplicates and value ranges.
- Use aggregates to write simple, repeatable validation assertions.

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

Your weekly goal is to use SQL for QA data validation and to begin the Project 1 "QE Foundations" capstone. When you test an application, you often cannot (and should not) look at every record. Instead you ask summarising questions:

- "Is the number of rows loaded equal to the number in the source file?" (`COUNT`)
- "Does the sum of order lines equal the order total?" (`SUM`)
- "Is the smallest quantity at least 1 and the largest below a sensible maximum?" (`MIN`, `MAX`)
- "How many customers are missing an email?" (`COUNT(*) - COUNT(email)`)
- "Is any value suspiciously far from the average?" (`AVG`)

Aggregate functions answer such questions in one line. They are the building blocks of **data-profiling** and of countless automated checks ("assert that this count is 0"). The previous lesson used them with `GROUP BY`; here we study them in depth, including the subtle NULL behaviour that causes many wrong test results.

## The Concept

### 1. What is an aggregate function?

A **scalar** (row) function takes one row's values and returns one value per row. For example, `ROUND(price, 1)` or `UPPER(name)` operate on each row separately.

An **aggregate function** takes the values from **many rows** and returns **one value**. Without `GROUP BY`, the "many rows" are *all* rows that survive the `WHERE` clause, and the result is one single row:

```text
rows in  --->  [ COUNT / SUM / AVG / MIN / MAX ]  --->  one value out
```

Analogy: scanning all till receipts at the end of the day and writing down "number of receipts", "total takings", "biggest sale". You compress many pieces of information into a few numbers.

| Function | Returns | Works on |
|---|---|---|
| `COUNT(*)` | number of rows | rows |
| `COUNT(col)` | number of non-NULL values | any column |
| `COUNT(DISTINCT col)` | number of different non-NULL values | any column |
| `SUM(col)` | total | numbers |
| `AVG(col)` | mean | numbers |
| `MIN(col)` / `MAX(col)` | smallest / largest | numbers, text, dates |
| `GROUP_CONCAT(col)` | values joined into one string | any (SQLite/MySQL) |

### 2. COUNT in its three forms

#### COUNT(*): count rows

```sql
SELECT COUNT(*) AS total_customers FROM customers;
```

**Result:**

```text
total_customers
---------------
10
(1 row)
```

`COUNT(*)` counts rows regardless of what the columns contain, NULLs included. Use it for "how many rows are there?".

#### COUNT(column): count non-NULL values

```sql
SELECT COUNT(*)     AS all_rows,
       COUNT(email) AS customers_with_email
FROM customers;
```

**Result:**

```text
all_rows | customers_with_email
---------+---------------------
10       | 9
(1 row)
```

10 rows but only 9 emails: Frank Lee (customer 6) has `NULL`. `COUNT(email)` skips NULLs, so **`COUNT(*) - COUNT(email)` is the number of missing emails** (here 1). This is a standard validation expression.

#### COUNT(DISTINCT column): count unique values

```sql
SELECT COUNT(email)          AS non_null_emails,
       COUNT(DISTINCT email) AS unique_emails
FROM customers;
```

**Result:**

```text
non_null_emails | unique_emails
----------------+--------------
9               | 8
(1 row)
```

9 non-NULL emails but only 8 unique ones: one email is duplicated (bob@example.com). If a rule says "email is unique", then `COUNT(email) = COUNT(DISTINCT email)` should hold, and it does not. That is a one-line duplicate check.

```sql
SELECT COUNT(*) AS orders,
       COUNT(customer_id) AS orders_with_customer,
       COUNT(DISTINCT customer_id) AS distinct_customers_ordering
FROM orders;
```

**Result:**

```text
orders | orders_with_customer | distinct_customers_ordering
-------+----------------------+----------------------------
12     | 11                   | 7
(1 row)
```

12 orders, 11 with a customer ID (order 108 is NULL), and 7 distinct IDs (1, 2, 3, 4, 5, 7 and the orphan 99).

### 3. SUM and AVG

`SUM` adds the non-NULL values; `AVG` is the sum divided by the *count of non-NULL values*.

```sql
SELECT SUM(total_amount)  AS sum_totals,
       AVG(total_amount)  AS avg_total,
       COUNT(total_amount) AS n
FROM orders;
```

**Result:**

```text
sum_totals | avg_total         | n
-----------+-------------------+---
3450.44    | 287.5366666666667 | 12
(1 row)
```

#### Arithmetic inside aggregates

You can calculate per row, then aggregate. The value of all order lines:

```sql
SELECT SUM(quantity * unit_price) AS items_value FROM order_items;
```

**Result:**

```text
items_value
-----------
3520.46
(1 row)
```

(`quantity * unit_price` is computed for each row, then summed.) Compare this with the sum of order header totals above; they differ, which proves that headers and lines disagree somewhere.

#### Aggregates with a WHERE filter

`WHERE` is applied *first*, then the aggregate sees only the surviving rows:

```sql
SELECT SUM(total_amount) AS completed_revenue, COUNT(*) AS completed_orders
FROM orders
WHERE status = 'completed';
```

**Result:**

```text
completed_revenue | completed_orders
------------------+-----------------
1535.45           | 8
(1 row)
```

#### Rounding

Floating-point numbers cannot represent every decimal exactly, so sums and averages can show trailing digits. Use `ROUND(value, digits)` for display and for comparisons:

```sql
SELECT AVG(total_amount)           AS raw_avg,
       ROUND(AVG(total_amount), 2) AS rounded_avg
FROM orders;
```

**Result:**

```text
raw_avg           | rounded_avg
------------------+------------
287.5366666666667 | 287.54
(1 row)
```

**Important for QA:** never compare money values with a bare `=` after arithmetic; compare `ROUND(a, 2) = ROUND(b, 2)`, or better, store money as integer cents in real systems. A classic example is `0.1 + 0.2`, which is not exactly `0.3` in floating point:

```sql
SELECT 0.1 + 0.2 AS sum_raw, (0.1 + 0.2) = 0.3 AS equals_point_three, ROUND(0.1 + 0.2, 2) = 0.3 AS equals_after_round;
```

**Result:**

```text
sum_raw             | equals_point_three | equals_after_round
--------------------+--------------------+-------------------
0.30000000000000004 | 0                  | 1
(1 row)
```

### 4. MIN and MAX

`MIN` and `MAX` work on numbers, text (alphabetical order) and dates (ISO date strings like `2025-07-25` sort chronologically):

```sql
SELECT MIN(unit_price) AS cheapest,
       MAX(unit_price) AS dearest,
       MIN(order_date) AS first_order_date,
       MAX(order_date) AS last_order_date
FROM (SELECT unit_price, NULL AS order_date FROM products
      UNION ALL
      SELECT NULL, order_date FROM orders);
```

**Result:**

```text
cheapest | dearest | first_order_date | last_order_date
---------+---------+------------------+----------------
3.5      | 1200.0  | 2025-06-01       | 2025-07-25
(1 row)
```

(The inner `UNION ALL` is only a trick to show product and order columns in a single result; usually you would run `MIN`/`MAX` on a single table.) Simpler examples:

```sql
SELECT MIN(order_date) AS first_order, MAX(order_date) AS last_order FROM orders;
```

**Result:**

```text
first_order | last_order
------------+-----------
2025-06-01  | 2025-07-25
(1 row)
```

```sql
SELECT MIN(full_name) AS first_alphabetically, MAX(full_name) AS last_alphabetically FROM customers;
```

**Result:**

```text
first_alphabetically | last_alphabetically
---------------------+--------------------
Alice Johnson        | Ian Brooks
(1 row)
```

**Range checks** with `MIN`/`MAX` are very effective in data validation: they spot impossible values without scanning rows.

```sql
SELECT MIN(quantity) AS min_qty, MAX(quantity) AS max_qty,
       MIN(unit_price) AS min_price, MAX(unit_price) AS max_price
FROM order_items;
```

**Result:**

```text
min_qty | max_qty | min_price | max_price
--------+---------+-----------+----------
-1      | 10      | 3.5       | 1200.0
(1 row)
```

`min_qty = -1` immediately exposes the negative-quantity bug (item 16), and `max_qty = 10` can be compared with the business maximum.

### 5. How aggregates treat NULL (and empty sets)

Remember these rules; they explain most "my total looks wrong" questions:

| Situation | `COUNT(*)` | `COUNT(col)` | `SUM(col)` | `AVG(col)` | `MIN/MAX(col)` |
|---|---|---|---|---|---|
| NULL values in `col` | counted | **ignored** | **ignored** | **ignored** (not counted in the divisor) | **ignored** |
| No rows at all | 0 | 0 | **NULL** | **NULL** | **NULL** |
| All values NULL | rows counted | 0 | **NULL** | **NULL** | **NULL** |

A demonstration with a tiny inline table built using `VALUES`:

```sql
SELECT COUNT(*)  AS count_star,
       COUNT(x)  AS count_x,
       SUM(x)    AS sum_x,
       AVG(x)    AS avg_x
FROM (SELECT 10 AS x UNION ALL SELECT 20 UNION ALL SELECT NULL);
```

**Result:**

```text
count_star | count_x | sum_x | avg_x
-----------+---------+-------+------
3          | 2       | 30    | 15.0
(1 row)
```

Three rows, but only two values: the sum is 30 and the average is **15** (30 divided by 2), not 10 (30 divided by 3). NULLs are ignored, not treated as zero. If your business rule says "missing means zero", write `AVG(COALESCE(x, 0))` which gives 10.

```sql
SELECT AVG(COALESCE(x, 0)) AS avg_missing_as_zero
FROM (SELECT 10 AS x UNION ALL SELECT 20 UNION ALL SELECT NULL);
```

**Result:**

```text
avg_missing_as_zero
-------------------
10.0
(1 row)
```

Empty sets:

```sql
SELECT COUNT(*) AS n, SUM(total_amount) AS total, AVG(total_amount) AS average, MAX(total_amount) AS biggest
FROM orders
WHERE status = 'returned';      -- no such status exists
```

**Result:**

```text
n | total | average | biggest
--+-------+---------+--------
0 | NULL  | NULL    | NULL
(1 row)
```

`COUNT` gives `0` but the others give `NULL`. In test code, remember that "no rows" produces NULL for `SUM`, and handle it (for example `COALESCE(SUM(...), 0)`) before comparing.

SQLite also has a `TOTAL()` function that returns `0.0` instead of NULL for an empty set; it is SQLite-only, so we mention it but do not rely on it.

### 6. Integer division: a hidden trap

In SQLite (and PostgreSQL, SQL Server), dividing two **integers** gives an integer, discarding the fraction. (MySQL's `/` gives a decimal.)

```sql
SELECT 7 / 2      AS integer_division,
       7 / 2.0    AS decimal_division,
       CAST(7 AS REAL) / 2 AS cast_division;
```

**Result:**

```text
integer_division | decimal_division | cast_division
-----------------+------------------+--------------
3                | 3.5              | 3.5
(1 row)
```

`7 / 2` is `3`, not `3.5`. When you compute percentages or ratios from `COUNT(*)` values (which are integers), force decimal division by multiplying by `1.0` or using `CAST`. Percentage of orders that are completed:

```sql
SELECT ROUND(100.0 * SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_completed
FROM orders;
```

**Result:**

```text
pct_completed
-------------
66.7
(1 row)
```

(`100.0 *` first makes everything decimal. `SUM(CASE ...)` is explained in the next section.)

### 7. Conditional aggregation: SUM(CASE WHEN ...)

`CASE` returns a value depending on a condition. Combined with `SUM` (or `COUNT`) it lets you count several categories **in a single pass**, producing a one-row "pivot" summary:

```sql
SELECT COUNT(*) AS total_orders,
       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed,
       SUM(CASE WHEN status = 'pending'   THEN 1 ELSE 0 END) AS pending,
       SUM(CASE WHEN status = 'shipped'   THEN 1 ELSE 0 END) AS shipped,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM orders;
```

**Result:**

```text
total_orders | completed | pending | shipped | cancelled
-------------+-----------+---------+---------+----------
12           | 8         | 2       | 1       | 1
(1 row)
```

How it works: for each row, `CASE` yields `1` if the status matches and `0` otherwise; `SUM` adds those 1s and 0s, which counts the matching rows. The result is a compact summary that a test can compare against a dashboard's tiles. The same trick works with amounts:

```sql
SELECT SUM(CASE WHEN method = 'card'   THEN amount ELSE 0 END) AS card_total,
       SUM(CASE WHEN method = 'paypal' THEN amount ELSE 0 END) AS paypal_total,
       SUM(amount) AS all_total
FROM payments
WHERE status = 'paid';
```

**Result:**

```text
card_total | paypal_total | all_total
-----------+--------------+----------
2005.95    | 159.99       | 2165.94
(1 row)
```

### 8. GROUP_CONCAT: aggregating text

`GROUP_CONCAT(column, separator)` joins values from many rows into one string. It is a SQLite and MySQL function; PostgreSQL and SQL Server use `STRING_AGG(column, separator)`. It is handy to produce readable evidence in a failure message:

```sql
SELECT GROUP_CONCAT(full_name, ', ') AS us_customers
FROM customers
WHERE country = 'US';
```

**Result:**

```text
us_customers
----------------------------------------------
Alice Johnson, Bob Smith, Grace Kim, Bob Smith
(1 row)
```

### 9. Aggregates together with GROUP BY and joins (quick revision)

All aggregates work per group when you add `GROUP BY` (previous lesson). Highest spenders, using a join, grouping and several aggregates:

```sql
SELECT c.full_name,
       COUNT(o.order_id)    AS orders,
       SUM(o.total_amount)  AS total,
       ROUND(AVG(o.total_amount), 2) AS avg_order,
       MAX(o.total_amount)  AS biggest
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY total DESC;
```

**Result:**

```text
full_name     | orders | total   | avg_order | biggest
--------------+--------+---------+-----------+--------
Alice Johnson | 2      | 1255.48 | 627.74    | 1225.0
Eve Muller    | 1      | 1200.0  | 1200.0    | 1200.0
Carla Gomez   | 2      | 619.99  | 310.0     | 600.0
Bob Smith     | 2      | 205.0   | 102.5     | 150.0
Grace Kim     | 2      | 89.99   | 44.99     | 80.0
Dev Patel     | 1      | 34.99   | 34.99     | 34.99
(6 rows)
```

**Aggregates cannot be nested directly** in a single `SELECT` (for example `AVG(SUM(x))` is an error in most databases). Use a subquery: first compute the per-group sums, then average them.

```sql
SELECT ROUND(AVG(customer_total), 2) AS avg_spend_per_customer
FROM (
    SELECT customer_id, SUM(total_amount) AS customer_total
    FROM orders
    WHERE customer_id IS NOT NULL
    GROUP BY customer_id
);
```

**Result:**

```text
avg_spend_per_customer
----------------------
491.49
(1 row)
```

### 10. A data-profiling query

**Data profiling** means measuring a table's basic properties before you trust it. One query can report many facts. For `customers`:

```sql
SELECT COUNT(*)                                  AS row_count,
       COUNT(DISTINCT customer_id)               AS distinct_ids,
       COUNT(*) - COUNT(email)                   AS null_emails,
       COUNT(email) - COUNT(DISTINCT email)      AS duplicate_email_rows,
       COUNT(*) - COUNT(country)                 AS null_countries,
       MIN(created_date)                         AS earliest_created,
       MAX(created_date)                         AS latest_created
FROM customers;
```

**Result:**

```text
row_count | distinct_ids | null_emails | duplicate_email_rows | null_countries | earliest_created | latest_created
----------+--------------+-------------+----------------------+----------------+------------------+---------------
10        | 10           | 1           | 1                    | 0              | 2025-01-10       | 2025-05-09
(1 row)
```

For `order_items`:

```sql
SELECT COUNT(*)                                    AS row_count,
       SUM(CASE WHEN quantity <= 0 THEN 1 ELSE 0 END)  AS bad_quantity_rows,
       SUM(CASE WHEN unit_price <= 0 THEN 1 ELSE 0 END) AS bad_price_rows,
       MIN(quantity) AS min_qty,
       MAX(quantity) AS max_qty
FROM order_items;
```

**Result:**

```text
row_count | bad_quantity_rows | bad_price_rows | min_qty | max_qty
----------+-------------------+----------------+---------+--------
16        | 1                 | 0              | -1      | 10
(1 row)
```

A QA engineer reads a profile like a doctor reads a blood test: the numbers that are not as expected (1 NULL email, 1 duplicate email, 1 bad quantity) become the starting point for investigation. You will formalise this into reusable checks in the last lesson of the day.

### 11. Aggregates as test assertions

An aggregate that returns **a single number** is perfect for assertions in test code, because you can compare it to an expected value. Examples:

| Rule | Query that should return 0 (or the expected value) |
|---|---|
| No negative quantities | `SELECT COUNT(*) FROM order_items WHERE quantity <= 0` |
| Row counts match after load | `SELECT COUNT(*) FROM customers` equals 10 |
| Revenue matches report | `SELECT ROUND(SUM(total_amount),2) FROM orders WHERE status='completed'` equals the dashboard figure |
| Emails unique | `SELECT COUNT(email) - COUNT(DISTINCT email) FROM customers` equals 0 |

Run the first one:

```sql
SELECT COUNT(*) AS bad_rows FROM order_items WHERE quantity <= 0;
```

**Result:**

```text
bad_rows
--------
1
(1 row)
```

A non-zero result fails the check. Many teams write the failing rows' IDs into the test report; combine with `GROUP_CONCAT(item_id)` for that.

```sql
SELECT COUNT(*) AS bad_rows, GROUP_CONCAT(item_id) AS offending_item_ids
FROM order_items
WHERE quantity <= 0;
```

**Result:**

```text
bad_rows | offending_item_ids
---------+-------------------
1        | 16
(1 row)
```

### 12. Dialect notes

- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` work the same in all major databases.
- `AVG` of an *integer* column returns an integer in SQL Server; cast to decimal if needed.
- Integer division differs by database (see section 6).
- String aggregation: `GROUP_CONCAT` (SQLite, MySQL); `STRING_AGG` (PostgreSQL, SQL Server 2017+).
- Statistical aggregates (median, standard deviation) and window functions (running totals, rankings) vary by database and are covered later; we will cover window functions in depth in a later week.

### 13. Common mistakes

1. Assuming `COUNT(column)` counts NULLs (it does not).
2. Averaging when NULLs should have been counted as zero (or the reverse).
3. Using integer division and getting `0` for a percentage.
4. Comparing floating-point sums with `=` without rounding.
5. Forgetting that `SUM` over no rows is `NULL`, not `0`.
6. Using an aggregate in `WHERE` (use `HAVING` or a subquery).
7. Summing a column after a join that multiplied the rows.

## Practice Questions

**Q1.** How many distinct product categories exist? How many products have each category? (Two queries.)

**Q2.** What is the total quantity sold of "Wireless Mouse" (product 2) across all order lines?

**Q3.** What is the average payment amount for `paid` card payments, rounded to 2 decimals?

**Q4.** Write one query returning: number of payments, number of distinct orders paid, and the difference between them (hinting at duplicate payments).

**Q5.** A teammate computes the percentage of pending orders as `COUNT(CASE WHEN status='pending' THEN 1 END) / COUNT(*) * 100` and gets `0`. Why, and what is the fix?

### Answers

**A1.**

```sql
SELECT COUNT(DISTINCT category) AS distinct_categories FROM products;
```

**Result:**

```text
distinct_categories
-------------------
4
(1 row)
```

```sql
SELECT category, COUNT(*) AS products
FROM products
GROUP BY category
ORDER BY products DESC, category;
```

**Result:**

```text
category    | products
------------+---------
Electronics | 4
Furniture   | 2
Accessories | 1
Stationery  | 1
(4 rows)
```

**A2.**

```sql
SELECT SUM(quantity) AS units_of_mouse
FROM order_items
WHERE product_id = 2;
```

**Result:**

```text
units_of_mouse
--------------
5
(1 row)
```

(This includes the orphan item 14 whose order does not exist; a good reminder that aggregates do not validate keys.)

**A3.**

```sql
SELECT ROUND(AVG(amount), 2) AS avg_card_paid
FROM payments
WHERE method = 'card' AND status = 'paid';
```

**Result:**

```text
avg_card_paid
-------------
250.74
(1 row)
```

**A4.**

```sql
SELECT COUNT(*)                  AS payment_rows,
       COUNT(DISTINCT order_id)  AS distinct_orders,
       COUNT(*) - COUNT(DISTINCT order_id) AS extra_rows
FROM payments;
```

**Result:**

```text
payment_rows | distinct_orders | extra_rows
-------------+-----------------+-----------
11           | 10              | 1
(1 row)
```

11 rows but only 10 distinct orders: one extra row means at least one order has more than one payment (order 102).

**A5.** `COUNT(...)` returns an integer and `COUNT(*)` is an integer, so SQLite performs **integer division**: 2 / 12 = 0 before multiplying by 100. Fix: multiply by `100.0` first, e.g. `ROUND(100.0 * COUNT(CASE WHEN status='pending' THEN 1 END) / COUNT(*), 1)`.

```sql
SELECT ROUND(100.0 * COUNT(CASE WHEN status = 'pending' THEN 1 END) / COUNT(*), 1) AS pct_pending
FROM orders;
```

**Result:**

```text
pct_pending
-----------
16.7
(1 row)
```

## Summary / Key Takeaways

- Aggregate functions collapse many rows into one value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` (plus `GROUP_CONCAT` / `STRING_AGG`).
- `COUNT(*)` counts rows; `COUNT(col)` skips NULLs; `COUNT(DISTINCT col)` counts unique non-NULL values.
- `SUM`, `AVG`, `MIN`, `MAX` ignore NULLs; over an empty set they return NULL, not 0.
- Beware integer division and floating-point rounding; use `100.0 *`, `CAST`, and `ROUND`.
- `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` gives several conditional counts in one pass.
- Profile tables with one aggregate query: row counts, NULL counts, duplicate counts, min/max ranges.
- A single-number aggregate is an ideal test assertion, as in "this count must be 0".

## Additional Resources

- SQLite documentation, Built-in Aggregate Functions: https://www.sqlite.org/lang_aggfunc.html
- SQLite documentation, Core functions (ROUND, COALESCE and others): https://www.sqlite.org/lang_corefunc.html
- PostgreSQL documentation, Aggregate Functions: https://www.postgresql.org/docs/current/functions-aggregate.html
