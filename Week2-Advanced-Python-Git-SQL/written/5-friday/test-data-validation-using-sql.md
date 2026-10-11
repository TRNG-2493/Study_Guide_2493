# Test-Data Validation Using SQL

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **test-data validation** is and why QA engineers check the database directly, not only the user interface.
- Classify data checks into categories: row counts, uniqueness, completeness, referential integrity, validity (ranges and formats), consistency (cross-table totals) and business rules.
- Write each check as a query that returns the **violating rows**, so that "zero rows = pass".
- Combine many checks into one reusable **validation suite** that reports a name, a severity and a violation count for each.
- Reconcile data between a source and a target (row counts, aggregate checksums, and two-way `EXCEPT`).
- Design safe test-data set-up and tear-down with recognisable markers and a verification step.
- Plug SQL checks into automation by running them from a short Python script and failing the run when a check finds violations.

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

This is the capstone lesson of the SQL part of your week. Week 2's epic is "use SQL for QA data validation" and to begin the Project 1 "QE Foundations" capstone, where you will build a data-validation component for a small test framework. Everything you learned today comes together here: DML, constraints, joins, subqueries, grouping and aggregates.

Why should a tester care about the database at all?

- **The UI can lie, or hide.** A page may display a total that is calculated on the fly while the stored value is wrong. A report might silently drop orders that have no customer (recall the inner join). Only the database shows what was really stored.
- **Bugs are cheaper to find in the data.** An orphan order or a negative quantity today becomes a failed invoice, a wrong refund or a crashed report next month.
- **Automation needs fast, precise assertions.** A SQL check is quick to run, independent of the UI, and easy to repeat after every deployment or data load.
- **Test data itself must be trustworthy.** If the data you test against is already broken, test results are meaningless. Validating the test data is the first step of reliable testing.

## The Concept

### 1. What is test-data validation?

**Test-data validation** is the practice of using queries to check that data in a database is **correct, complete, consistent and fit for purpose**, either before tests run (is the starting data good?), during tests (did the application store the right thing?) or after loads and migrations (did every record arrive intact?).

The core idea of this lesson is a simple convention:

> **Write every check as a query that returns the rows that BREAK the rule. If it returns no rows (or a count of 0), the check passes. Any row returned is a failure, and it is your evidence.**

This "violations query" pattern has three big advantages: it is easy to read, it works for any rule, and the failing rows tell you exactly what to fix or report.

### 2. Categories of checks

Think of validation as a checklist with these families. We will write queries for each.

| # | Category | Question it answers | Typical tool |
|---|---|---|---|
| 1 | **Row counts / completeness of load** | Did all the rows arrive? | `COUNT(*)` |
| 2 | **Uniqueness** | Are there duplicates where there should be none? | `GROUP BY ... HAVING COUNT(*) > 1` |
| 3 | **Completeness of fields** | Are required values missing (NULL/empty)? | `WHERE col IS NULL` |
| 4 | **Referential integrity** | Does every foreign key point to a real parent? | `LEFT JOIN ... IS NULL`, `NOT EXISTS` |
| 5 | **Validity** | Are values inside allowed ranges, formats and lists? | `WHERE` with comparisons, `LIKE`, `IN` |
| 6 | **Consistency** | Do related tables agree (totals, statuses)? | joins + aggregates |
| 7 | **Business rules** | Is the data logically sensible for the domain? | any combination |
| 8 | **Reconciliation** | Does the target equal the source? | counts, sums, `EXCEPT`, `FULL JOIN` |

#### Our target: the "QA Shop" database

You have met it all day. A short reminder of its planted problems is in the recap table above. Our goal is to write checks that find *every one* of them.

### 3. Category 1: row counts

The simplest check, and the first after any data load. Compare with the expected number (from a source file, a spec or a previous run). Here all six tables in one result:

```sql
SELECT 'customers'   AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'products',    COUNT(*) FROM products
UNION ALL SELECT 'orders',      COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'payments',    COUNT(*) FROM payments
UNION ALL SELECT 'defects',     COUNT(*) FROM defects;
```

**Result:**

```text
table_name  | row_count
------------+----------
customers   | 10
products    | 8
orders      | 12
order_items | 16
payments    | 11
defects     | 6
(6 rows)
```

If the load specification says "10 customers, 8 products, 12 orders, 16 order lines, 11 payments, 6 defects", this check passes. If a CSV had 12 customers and only 10 arrived, you have found a data-loss bug, before any test has even run.

### 4. Category 2: uniqueness

Rule: emails should be unique among customers. The violating rows:

```sql
SELECT email, COUNT(*) AS occurrences, GROUP_CONCAT(customer_id) AS customer_ids
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;
```

**Result:**

```text
email           | occurrences | customer_ids
----------------+-------------+-------------
bob@example.com | 2           | 2,8
(1 row)
```

Rule: an order should not list the same product twice (it should be one line with a larger quantity):

```sql
SELECT order_id, product_id, COUNT(*) AS occurrences, GROUP_CONCAT(item_id) AS item_ids
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;
```

**Result:**

```text
order_id | product_id | occurrences | item_ids
---------+------------+-------------+---------
103      | 4          | 2           | 5,13
(1 row)
```

Rule: an order should be paid at most once per payment (same amount, same order, same status twice looks like a double charge):

```sql
SELECT order_id, amount, status, COUNT(*) AS occurrences, GROUP_CONCAT(payment_id) AS payment_ids
FROM payments
GROUP BY order_id, amount, status
HAVING COUNT(*) > 1;
```

**Result:**

```text
order_id | amount | status | occurrences | payment_ids
---------+--------+--------+-------------+------------
102      | 30.48  | paid   | 2           | 2,11
(1 row)
```

Rule: names alone are *not* a uniqueness rule (two people may share a name), so check on the business key, which is the email here, not on `full_name`. Choosing the right key is part of the QA analysis.

### 5. Category 3: completeness of fields (NULL and empty checks)

```sql
SELECT customer_id, full_name
FROM customers
WHERE email IS NULL OR TRIM(email) = '';
```

**Result:**

```text
customer_id | full_name
------------+----------
6           | Frank Lee
(1 row)
```

`TRIM(email) = ''` also catches emails that are empty or only spaces, which are *not* NULL but are still missing. Always test both. A summary of NULLs across a few important columns:

```sql
SELECT SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS orders_without_customer,
       SUM(CASE WHEN order_date  IS NULL THEN 1 ELSE 0 END) AS orders_without_date,
       SUM(CASE WHEN status      IS NULL THEN 1 ELSE 0 END) AS orders_without_status
FROM orders;
```

**Result:**

```text
orders_without_customer | orders_without_date | orders_without_status
------------------------+---------------------+----------------------
1                       | 0                   | 0
(1 row)
```

### 6. Category 4: referential integrity

You saw each of these in the left-join lesson. Here are the checks packaged as violations queries.

**Orders pointing to a customer that does not exist** (NULL is not counted: NULL means "no parent"):

```sql
SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.customer_id IS NOT NULL AND c.customer_id IS NULL;
```

**Result:**

```text
order_id | customer_id
---------+------------
107      | 99
(1 row)
```

**Order lines whose order or product is missing:**

```sql
SELECT i.item_id,
       CASE WHEN o.order_id   IS NULL THEN 'order missing'   ELSE '' END AS order_problem,
       CASE WHEN p.product_id IS NULL THEN 'product missing' ELSE '' END AS product_problem
FROM order_items AS i
LEFT JOIN orders   AS o ON o.order_id   = i.order_id
LEFT JOIN products AS p ON p.product_id = i.product_id
WHERE o.order_id IS NULL OR p.product_id IS NULL
ORDER BY i.item_id;
```

**Result:**

```text
item_id | order_problem | product_problem
--------+---------------+----------------
14      | order missing |
15      |               | product missing
(2 rows)
```

**Payments without an order:**

```sql
SELECT pay.payment_id, pay.order_id, pay.amount
FROM payments AS pay
WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.order_id = pay.order_id);
```

**Result:**

```text
payment_id | order_id | amount
-----------+----------+-------
10         | 888      | 10.0
(1 row)
```

**Parent without required children** (orders with no lines):

```sql
SELECT o.order_id, o.status, o.total_amount
FROM orders AS o
WHERE NOT EXISTS (SELECT 1 FROM order_items AS i WHERE i.order_id = o.order_id);
```

**Result:**

```text
order_id | status  | total_amount
---------+---------+-------------
109      | pending | 80.0
(1 row)
```

SQLite can also list foreign-key violations in one command, as you saw earlier today in the constraints lesson: `PRAGMA foreign_key_check;`. The join-based queries above are portable to every database.

### 7. Category 5: validity (ranges, formats, allowed values)

**Impossible numbers:**

```sql
SELECT item_id, order_id, quantity, unit_price
FROM order_items
WHERE quantity <= 0 OR unit_price <= 0;
```

**Result:**

```text
item_id | order_id | quantity | unit_price
--------+----------+----------+-----------
16      | 112      | -1       | 9.99
(1 row)
```

**Allowed values (a status must be one of a known list).** Any status outside the list would be returned; here none is, which is what a passing check looks like:

```sql
SELECT order_id, status
FROM orders
WHERE status IS NULL
   OR status NOT IN ('pending', 'shipped', 'completed', 'cancelled');
```

**Result:**

```text
order_id | status
---------+-------
(0 rows)
```

**Format checks.** Dates stored as text should follow `YYYY-MM-DD`. SQLite's `GLOB` uses `[0-9]` for "a digit" (other databases offer regular expressions or `LIKE` patterns):

```sql
SELECT customer_id, created_date
FROM customers
WHERE created_date IS NULL
   OR created_date NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]';
```

**Result:**

```text
customer_id | created_date
------------+-------------
(0 rows)
```

A rough email shape check using `LIKE` (an email should contain `@` with something before and a dot after):

```sql
SELECT customer_id, email
FROM customers
WHERE email IS NOT NULL
  AND email NOT LIKE '%_@_%._%';
```

**Result:**

```text
customer_id | email
------------+------
(0 rows)
```

Zero rows again: all nine non-NULL addresses are well formed. (Real email validation is far more complex; this is a smoke check.)

**Logical date rule:** an order cannot be placed before the customer existed.

```sql
SELECT o.order_id, o.order_date, c.customer_id, c.created_date
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.order_date < c.created_date;
```

**Result:**

```text
order_id | order_date | customer_id | created_date
---------+------------+-------------+-------------
(0 rows)
```

It passes. A check that always passes might be a useless check, so a good QA engineer also proves that a check *can* fail, by testing it against deliberately bad data (see section 11).

### 8. Category 6: consistency across tables

**Header total vs sum of its lines**, using a derived table (from the subqueries lesson) and a `LEFT JOIN` so orders without lines are included too:

```sql
SELECT o.order_id, o.total_amount AS header_total, it.items_total
FROM orders AS o
LEFT JOIN (
    SELECT order_id, SUM(quantity * unit_price) AS items_total
    FROM order_items
    GROUP BY order_id
) AS it ON it.order_id = o.order_id
WHERE ROUND(o.total_amount, 2) <> ROUND(COALESCE(it.items_total, 0), 2)
ORDER BY o.order_id;
```

**Result:**

```text
order_id | header_total | items_total
---------+--------------+------------
103      | 150.0        | 300.0
109      | 80.0         | NULL
110      | 55.0         | 50.0
112      | 9.99         | -9.99
(4 rows)
```

Four orders break the rule: 103 (duplicate line), 109 (no lines at all, a header total with nothing behind it), 110 (55 vs 50) and 112 (negative line). The `COALESCE(..., 0)` treats "no lines" as a total of zero so that order 109 is reported.

**Paid amount vs order total for completed orders:**

```sql
SELECT o.order_id, o.total_amount, COALESCE(pa.paid_total, 0) AS paid_total
FROM orders AS o
LEFT JOIN (
    SELECT order_id, SUM(amount) AS paid_total
    FROM payments
    WHERE status = 'paid'
    GROUP BY order_id
) AS pa ON pa.order_id = o.order_id
WHERE o.status = 'completed'
  AND ROUND(o.total_amount, 2) <> ROUND(COALESCE(pa.paid_total, 0), 2)
ORDER BY o.order_id;
```

**Result:**

```text
order_id | total_amount | paid_total
---------+--------------+-----------
102      | 30.48        | 60.96
112      | 9.99         | 0
(2 rows)
```

Order 102 was paid twice (60.96 against 30.48) and order 112 was completed with no payment at all. Either is a defect in the payment flow.

**Line price vs catalogue price** (sold price should match current list price, unless discounts are allowed):

```sql
SELECT i.item_id, i.product_id, i.unit_price AS sold_price, p.unit_price AS list_price
FROM order_items AS i
INNER JOIN products AS p ON p.product_id = i.product_id
WHERE i.unit_price <> p.unit_price;
```

**Result:**

```text
item_id | product_id | sold_price | list_price
--------+------------+------------+-----------
(0 rows)
```

This one passes (zero rows). Note the check can only examine lines whose product exists.

### 9. Category 7: business rules

Business rules come from the product owner or specification, not from SQL itself. Examples for our shop:

- A **cancelled** order should not have an active (`paid`) payment; it should have been refunded.
- A **refunded** payment should belong to a cancelled order.
- A **completed** order must have at least one item and at least one paid payment.

```sql
-- cancelled orders that still hold a 'paid' payment
SELECT o.order_id, pay.payment_id, pay.status
FROM orders AS o
INNER JOIN payments AS pay ON pay.order_id = o.order_id
WHERE o.status = 'cancelled' AND pay.status = 'paid';
```

**Result:**

```text
order_id | payment_id | status
---------+------------+-------
(0 rows)
```

```sql
-- refunded payments on orders that are not cancelled
SELECT pay.payment_id, o.order_id, o.status
FROM payments AS pay
INNER JOIN orders AS o ON o.order_id = pay.order_id
WHERE pay.status = 'refunded' AND o.status <> 'cancelled';
```

**Result:**

```text
payment_id | order_id | status
-----------+----------+-------
(0 rows)
```

Both pass (zero rows): order 106 is cancelled and its payment is refunded, exactly as the rule expects. The check for "completed orders must have items and a paid payment" is already covered by the consistency queries above.

### 10. A reusable validation suite in one query

Now combine the checks into a single result with one row per check: **name, severity, number of violations, and PASS/FAIL**. This is the shape that automated tests and dashboards consume.

```sql
WITH checks AS (
  SELECT 'duplicate customer emails' AS check_name, 'HIGH' AS severity, COUNT(*) AS violations FROM (
      SELECT email FROM customers WHERE email IS NOT NULL GROUP BY email HAVING COUNT(*) > 1)
  UNION ALL
  SELECT 'customers with missing email', 'LOW', COUNT(*) FROM customers WHERE email IS NULL OR TRIM(email) = ''
  UNION ALL
  SELECT 'orders pointing to missing customer', 'HIGH', COUNT(*)
  FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id
  WHERE o.customer_id IS NOT NULL AND c.customer_id IS NULL
  UNION ALL
  SELECT 'orders with no customer (guest)', 'MEDIUM', COUNT(*) FROM orders WHERE customer_id IS NULL
  UNION ALL
  SELECT 'order lines without a valid order', 'HIGH', COUNT(*)
  FROM order_items i WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = i.order_id)
  UNION ALL
  SELECT 'order lines without a valid product', 'HIGH', COUNT(*)
  FROM order_items i WHERE NOT EXISTS (SELECT 1 FROM products p WHERE p.product_id = i.product_id)
  UNION ALL
  SELECT 'payments without a valid order', 'HIGH', COUNT(*)
  FROM payments pay WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = pay.order_id)
  UNION ALL
  SELECT 'orders without lines', 'MEDIUM', COUNT(*)
  FROM orders o WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.order_id = o.order_id)
  UNION ALL
  SELECT 'duplicate order lines', 'MEDIUM', COUNT(*) FROM (
      SELECT 1 FROM order_items GROUP BY order_id, product_id HAVING COUNT(*) > 1)
  UNION ALL
  SELECT 'duplicate payments', 'HIGH', COUNT(*) FROM (
      SELECT 1 FROM payments GROUP BY order_id, amount, status HAVING COUNT(*) > 1)
  UNION ALL
  SELECT 'non-positive quantities', 'HIGH', COUNT(*) FROM order_items WHERE quantity <= 0
  UNION ALL
  SELECT 'order totals differing from lines', 'HIGH', COUNT(*) FROM orders o
  LEFT JOIN (SELECT order_id, SUM(quantity*unit_price) AS t FROM order_items GROUP BY order_id) it
         ON it.order_id = o.order_id
  WHERE ROUND(o.total_amount,2) <> ROUND(COALESCE(it.t,0),2)
  UNION ALL
  SELECT 'completed orders not fully paid', 'HIGH', COUNT(*) FROM orders o
  LEFT JOIN (SELECT order_id, SUM(amount) AS t FROM payments WHERE status='paid' GROUP BY order_id) pa
         ON pa.order_id = o.order_id
  WHERE o.status = 'completed' AND ROUND(o.total_amount,2) <> ROUND(COALESCE(pa.t,0),2)
  UNION ALL
  SELECT 'invalid order status', 'MEDIUM', COUNT(*) FROM orders
  WHERE status IS NULL OR status NOT IN ('pending','shipped','completed','cancelled')
)
SELECT check_name, severity, violations,
       CASE WHEN violations = 0 THEN 'PASS' ELSE 'FAIL' END AS result
FROM checks
ORDER BY CASE result WHEN 'FAIL' THEN 0 ELSE 1 END, severity, check_name;
```

**Result:**

```text
check_name                          | severity | violations | result
------------------------------------+----------+------------+-------
completed orders not fully paid     | HIGH     | 2          | FAIL
duplicate customer emails           | HIGH     | 1          | FAIL
duplicate payments                  | HIGH     | 1          | FAIL
non-positive quantities             | HIGH     | 1          | FAIL
order lines without a valid order   | HIGH     | 1          | FAIL
order lines without a valid product | HIGH     | 1          | FAIL
order totals differing from lines   | HIGH     | 4          | FAIL
orders pointing to missing customer | HIGH     | 1          | FAIL
payments without a valid order      | HIGH     | 1          | FAIL
customers with missing email        | LOW      | 1          | FAIL
duplicate order lines               | MEDIUM   | 1          | FAIL
orders with no customer (guest)     | MEDIUM   | 1          | FAIL
orders without lines                | MEDIUM   | 1          | FAIL
invalid order status                | MEDIUM   | 0          | PASS
(14 rows)
```

Take a moment to read the structure:

- `WITH checks AS (...)` names the big union of checks as a temporary result called `checks`, to be queried like a table.
- Every inner `SELECT` returns the same three columns: a text name, a severity label and an integer count, so `UNION ALL` can stack them.
- The outer query adds `PASS`/`FAIL` with `CASE` and sorts failures first.

The result is a **test report in table form**: 13 of the 14 checks fail and only one passes (see the output above for the exact rows). In an automated pipeline you would assert "no HIGH severity failures" and attach the table to the build report. To investigate one failing check, run its violations query to get the evidence rows.

One important idea to carry into Project 1: **keep each check small, named and independent**, so that one failing check does not hide another.

### 11. Proving a check can fail (testing the test)

A passing validation is only meaningful if it *would* have failed on bad data. Standard technique: insert a known-bad row inside a transaction, run the check, then roll back:

```sql
BEGIN;

-- plant a bad row: negative price
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (101, 1, 1, -5.00);

SELECT item_id, unit_price FROM order_items WHERE quantity <= 0 OR unit_price <= 0 ORDER BY item_id;

ROLLBACK;

SELECT COUNT(*) AS bad_rows_after_rollback FROM order_items WHERE quantity <= 0 OR unit_price <= 0;
```

**Result:**

```text
OK

OK: 1 row(s) affected

item_id | unit_price
--------+-----------
16      | 9.99
17      | -5.0
(2 rows)

OK

bad_rows_after_rollback
-----------------------
1
(1 row)
```

Inside the transaction the check caught the planted row (17), in addition to the original problem (16). After the rollback the data is back to its original state. This is a **negative test of your validation**, and good teams always do it for new checks.

### 12. Reconciliation: comparing source and target

After a migration, ETL job or file import, compare the **target** with the **source** using three levels of rigour, from quick to thorough:

1. **Row counts** must match.
2. **Aggregate checksums** (sums, min, max of key numeric columns) must match.
3. **Row-level comparison** with `EXCEPT` (rows in one but not the other).

We simulate a source and a target using copies of `customers` (a scratch copy per side):

```sql
CREATE TABLE demo_source AS SELECT customer_id, full_name, email, country FROM customers;
CREATE TABLE demo_target AS SELECT customer_id, full_name, email, country FROM customers;

-- simulate faulty migration: one row lost, one value corrupted, one extra row
DELETE FROM demo_target WHERE customer_id = 9;
UPDATE demo_target SET country = 'XX' WHERE customer_id = 4;
INSERT INTO demo_target VALUES (77, 'Ghost Customer', 'ghost@example.com', 'US');
```

**Result:**

```text
OK

OK

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected
```

**Level 1 and 2: counts and checksums:**

```sql
SELECT 'source' AS side, COUNT(*) AS row_count, SUM(customer_id) AS id_checksum, COUNT(DISTINCT country) AS countries FROM demo_source
UNION ALL
SELECT 'target', COUNT(*), SUM(customer_id), COUNT(DISTINCT country) FROM demo_target;
```

**Result:**

```text
side   | row_count | id_checksum | countries
-------+-----------+-------------+----------
source | 10        | 55          | 7
target | 10        | 123         | 6
(2 rows)
```

Counts are equal (10 and 10), so a naive "row count" check **passes** even though the migration is wrong: one row lost, one extra, one corrupted. The checksum and country count differ, which shows why one check alone is not enough.

**Level 3: row-level differences with EXCEPT:**

```sql
SELECT 'in source, not in target' AS problem, customer_id, full_name, country
FROM (SELECT * FROM demo_source EXCEPT SELECT * FROM demo_target)
UNION ALL
SELECT 'in target, not in source', customer_id, full_name, country
FROM (SELECT * FROM demo_target EXCEPT SELECT * FROM demo_source)
ORDER BY problem, customer_id;
```

**Result:**

```text
problem                  | customer_id | full_name      | country
-------------------------+-------------+----------------+--------
in source, not in target | 4           | Dev Patel      | IN
in source, not in target | 9           | Hana Sato      | JP
in target, not in source | 4           | Dev Patel      | XX
in target, not in source | 77          | Ghost Customer | US
(4 rows)
```

The report shows exactly what went wrong: customer 4 appears on both sides with *different* content (original IN, corrupted XX), customer 9 is missing from the target, and customer 77 exists only in the target. `EXCEPT` compares entire rows, so any changed column makes the row appear. (A `FULL JOIN` on the key, from the FULL JOIN lesson, can instead tell you *which column* differs.)

```sql
DROP TABLE demo_source;
DROP TABLE demo_target;
```

**Result:**

```text
OK

OK
```

### 13. Safe test-data set-up and tear-down

Tests that write data must clean up after themselves, otherwise the next run starts dirty. A reliable pattern:

1. **Mark** every test record with a recognisable marker (a name prefix such as `TEST_`, or an ID range such as 9000 to 9999).
2. **Insert in parent-to-child order.**
3. **Delete in child-to-parent order.**
4. **Verify** that nothing with the marker remains.

```sql
BEGIN;

INSERT INTO customers (customer_id, full_name, email, country, created_date)
VALUES (9001, 'TEST_checkout_user', 'test_checkout@example.com', 'US', '2025-09-01');
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (9001, 9001, '2025-09-01', 'completed', 20.00);
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (9001, 5, 2, 10.00);
INSERT INTO payments (payment_id, order_id, amount, method, status)
VALUES (9001, 9001, 20.00, 'card', 'paid');

-- ... the test would run here ...

DELETE FROM payments    WHERE order_id = 9001;
DELETE FROM order_items WHERE order_id = 9001;
DELETE FROM orders      WHERE order_id = 9001;
DELETE FROM customers   WHERE customer_id = 9001;

COMMIT;

SELECT (SELECT COUNT(*) FROM customers WHERE full_name LIKE 'TEST_%')
     + (SELECT COUNT(*) FROM orders    WHERE order_id >= 9000)
     + (SELECT COUNT(*) FROM order_items WHERE order_id >= 9000)
     + (SELECT COUNT(*) FROM payments  WHERE order_id >= 9000) AS leftover_test_rows;
```

**Result:**

```text
OK

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK

leftover_test_rows
------------------
0
(1 row)
```

`leftover_test_rows` must be `0`. Many teams make this verification part of every test's tear-down, or run it once at the end of the suite. Hard rules: never run destructive clean-up on a shared or production database, use a dedicated test database, and always include the marker in the `WHERE` clause of every `DELETE`.

### 14. Plugging SQL checks into automation (a first look)

Each violations query can be run from any programming language. Because you learned Python this week, here is a short Python script (the right tool here because Python is your automation language, and the SQL is passed as text). It runs a list of checks against the database file and reports PASS or FAIL, so a build can stop when a check fails. Python's built-in `sqlite3` module provides the connection.

```python
import sqlite3

conn = sqlite3.connect("qa_shop.db")          # the database created from the setup script

# Each check: (name, SQL that returns the VIOLATING rows)
CHECKS = [
    ("duplicate customer emails",
     "SELECT email FROM customers WHERE email IS NOT NULL GROUP BY email HAVING COUNT(*) > 1"),
    ("order items with quantity <= 0",
     "SELECT item_id FROM order_items WHERE quantity <= 0"),
    ("orders pointing to a missing customer",
     "SELECT o.order_id FROM orders o LEFT JOIN customers c ON c.customer_id = o.customer_id "
     "WHERE o.customer_id IS NOT NULL AND c.customer_id IS NULL"),
    ("negative order totals",
     "SELECT order_id FROM orders WHERE total_amount < 0"),
]

failures = 0
for name, sql in CHECKS:
    rows = conn.execute(sql).fetchall()      # list of violating rows
    status = "PASS" if len(rows) == 0 else "FAIL"
    print(f"{status}  {name}  ({len(rows)} violation(s))  {rows}")
    if rows:
        failures += 1

print(f"\n{failures} of {len(CHECKS)} checks failed")
conn.close()
```

Explanation, line by line:

- `sqlite3.connect("qa_shop.db")` opens the database file created from the setup script.
- `CHECKS` is a list of tuples `(name, sql)`. Each SQL string is a violations query, exactly as we wrote in SQL above.
- `conn.execute(sql).fetchall()` runs the query and returns all violating rows as a list of tuples.
- An empty list means the check passed; a non-empty list means failure, and the list *is* the evidence printed in the message.
- `failures` counts failing checks; in a real framework you would raise an exception or use an assertion (as in the unit-testing lesson) so the test runner marks the run as failed.

Output when run against our practice database:

```text
FAIL  duplicate customer emails  (1 violation(s))  [('bob@example.com',)]
FAIL  order items with quantity <= 0  (1 violation(s))  [(16,)]
FAIL  orders pointing to a missing customer  (1 violation(s))  [(107,)]
PASS  negative order totals  (0 violation(s))  []

3 of 4 checks failed
```

Project 1 asks you to organise checks like this into a proper module. We will cover testing frameworks for databases and APIs in depth in a later week.

### 15. Good habits for data validation

1. **Define the rule in words first** ("every order has a customer who exists"), then write the query.
2. **Return violating rows, not just counts**, during investigation; counts are for dashboards.
3. **Name and classify each check** (category and severity) so results are triaged quickly.
4. **Test your checks** against deliberately bad data.
5. **Know your NULLs**: decide whether NULL is allowed for each column and test accordingly.
6. **Mind the join type**: an inner join in a validation query can hide exactly the problems you are looking for.
7. **Use a read-only account or a copy** when you only need to read; keep destructive set-up/tear-down in a dedicated test database.
8. **Record what you found**: query, expected result, actual result, and the offending IDs make perfect defect reports.
9. **Automate repeatable checks** and run them after every data load or deployment.

### 16. Dialect notes

- The patterns (`LEFT JOIN ... IS NULL`, `NOT EXISTS`, `GROUP BY ... HAVING`, `EXCEPT`) are standard and portable. Oracle names `EXCEPT` as `MINUS`; MySQL added `EXCEPT` in version 8.0.31.
- Format checks differ: SQLite `GLOB`, PostgreSQL `~` regular expressions, MySQL `REGEXP`, SQL Server `LIKE` with character ranges or `TRY_CAST`.
- `WITH ... AS` is supported in modern versions of all major databases.
- `PRAGMA foreign_key_check` is SQLite-specific.
- SQLite lets you run a non-aggregated column with `GROUP BY` freely; other databases enforce the rule, so write portable grouping.

### 17. Common mistakes

1. Testing only with clean data and never confirming that a check can fail.
2. Using `INNER JOIN` where a `LEFT JOIN` is required to see the missing rows.
3. Using `NOT IN` against a nullable column.
4. Treating NULL and empty string as the same, or ignoring one of them.
5. Comparing money with `=` without `ROUND`.
6. Cleaning up test data by guesswork instead of by marker.
7. Counting rows only: counts can be equal while the data is wrong.
8. Running destructive set-up or clean-up on the wrong environment.

## Practice Questions

**Q1.** Write a violations query for the rule "every payment amount must be positive and every payment must have a method". What does it return?

**Q2.** Write a check "no customer may have two orders on the same date". Does the data pass?

**Q3.** Write a check listing completed orders whose total is greater than 100 but which have no payment of any status.

**Q4.** The target table has 10 rows and the source table has 10 rows, but a tester says "migration verified". Give two reasons that statement may be wrong, and the query technique that gives stronger evidence.

**Q5.** Extend the validation suite with one new check: "products with a non-positive price". Show the single `SELECT` row you would add.

### Answers

**A1.**

```sql
SELECT payment_id, amount, method
FROM payments
WHERE amount <= 0 OR method IS NULL OR TRIM(method) = '';
```

**Result:**

```text
payment_id | amount | method
-----------+--------+-------
(0 rows)
```

No rows: this rule passes.

**A2.**

```sql
SELECT customer_id, order_date, COUNT(*) AS orders_that_day, GROUP_CONCAT(order_id) AS order_ids
FROM orders
WHERE customer_id IS NOT NULL
GROUP BY customer_id, order_date
HAVING COUNT(*) > 1;
```

**Result:**

```text
customer_id | order_date | orders_that_day | order_ids
------------+------------+-----------------+----------
(0 rows)
```

No rows: it passes. (Customers with two orders placed them on different dates.)

**A3.**

```sql
SELECT o.order_id, o.total_amount
FROM orders AS o
WHERE o.status = 'completed'
  AND o.total_amount > 100
  AND NOT EXISTS (SELECT 1 FROM payments AS p WHERE p.order_id = o.order_id);
```

**Result:**

```text
order_id | total_amount
---------+-------------
(0 rows)
```

No rows: the only completed order with no payment is 112, and its total (9.99) is below 100. Changing the threshold to `> 0` would return 112.

**A4.** Equal counts do not prove equality: rows can be lost *and* extra rows added in the same load, or values can be corrupted without changing the count. Stronger evidence: compare aggregate checksums (sums of numeric columns, distinct counts) and, best of all, a two-way `EXCEPT` (or a `FULL JOIN` on the key) that lists the exact differing rows.

**A5.**

```sql
SELECT 'products with non-positive price' AS check_name, 'HIGH' AS severity, COUNT(*) AS violations
FROM products
WHERE unit_price <= 0;
```

**Result:**

```text
check_name                       | severity | violations
---------------------------------+----------+-----------
products with non-positive price | HIGH     | 0
(1 row)
```

Add it to the suite with `UNION ALL`. It returns 0 violations here, so it would show as `PASS`.

## Summary / Key Takeaways

- Test-data validation uses SQL to prove that stored data is correct, complete and consistent, independent of the UI.
- Write every check as a **violations query**: no rows (or a zero count) means pass; returned rows are your evidence.
- Cover the eight families: counts, uniqueness, completeness, referential integrity, validity, consistency, business rules and reconciliation.
- Combine checks with `UNION ALL` into a suite that reports check name, severity, violations and PASS/FAIL.
- Equal row counts prove little; add checksums and a two-way `EXCEPT` for source/target reconciliation.
- Prove that checks can fail by planting bad data inside a transaction and rolling back.
- Set up and tear down test data using markers, parent-to-child inserts and child-to-parent deletes, then verify that nothing is left.
- The same queries plug directly into automation (for example from Python) so a build can fail when data is bad, which is the foundation of your Project 1 data-validation work.

## Additional Resources

- SQLite documentation, Query Language overview (SELECT, compound SELECT with EXCEPT, WITH clause): https://www.sqlite.org/lang.html
- SQLite documentation, Foreign Key Support (including PRAGMA foreign_key_check): https://www.sqlite.org/foreignkeys.html
- Python documentation, sqlite3 module: https://docs.python.org/3/library/sqlite3.html
