# LEFT and RIGHT JOIN

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an **outer join** is and how it differs from an inner join.
- Write `LEFT JOIN` queries and describe exactly which rows are kept and where the NULLs come from.
- Use the **anti-join pattern** (`LEFT JOIN ... WHERE right.key IS NULL`) to find rows with no match, such as customers with no orders or orphaned records.
- Explain why a condition placed in `WHERE` can silently turn a `LEFT JOIN` back into an `INNER JOIN`, and how to avoid it.
- Write `RIGHT JOIN` queries, explain they are a mirror image of `LEFT JOIN`, and rewrite them as `LEFT JOIN` by swapping tables.
- Know which databases support `RIGHT JOIN`, including older SQLite versions.
- Use `COUNT(column)` and `COALESCE` correctly on the NULLs that outer joins produce.

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

This week you are learning to use SQL to validate data, and you are beginning your Project 1 "QE Foundations" capstone. In the previous lesson we saw the weakness of the inner join: it only reports rows that have a partner. It *silently drops* order 107 (customer 99 does not exist), order 108 (no customer), and every customer who has never ordered.

A tester's mindset is "what is missing, what is broken, what does not match?" The outer join is the tool that answers those questions. Typical QA questions it answers:

- Which customers registered but never placed an order (a conversion report)?
- Which orders refer to customers that do not exist (orphans)?
- Which products were never sold (candidates for catalogue clean-up)?
- Which orders have no items, and which payments have no order?

If an inner join says "show me what matches", the left join says "show me everything from this side, and tell me whether it matched". The unmatched rows are often precisely the bugs.

## The Concept

### 1. Outer joins in one sentence

An **outer join** keeps **all rows from one table** (or both) even when there is no matching row in the other table. Where no match exists, the columns that would have come from the other table are filled with `NULL`.

There are three kinds:

| Join | Keeps all rows from | Covered in |
|---|---|---|
| `LEFT JOIN` (`LEFT OUTER JOIN`) | the **left** table (the one named in `FROM`) | this lesson |
| `RIGHT JOIN` (`RIGHT OUTER JOIN`) | the **right** table (the one named after `JOIN`) | this lesson |
| `FULL JOIN` (`FULL OUTER JOIN`) | **both** tables | next lesson |

The word `OUTER` is optional: `LEFT JOIN` and `LEFT OUTER JOIN` are identical.

### 2. LEFT JOIN

#### Syntax

```text
SELECT  columns
FROM    left_table
LEFT JOIN right_table
        ON left_table.key = right_table.key;
```

"Left" and "right" refer to the *position in the text of the query*: the table in `FROM` is on the left, the table after `LEFT JOIN` is on the right.

**Algorithm in words:** for each row of the left table, look for matching rows on the right. If there are matches, output one row per match (just like an inner join). If there are **no** matches, still output the left row once, with `NULL` in all right-table columns.

#### Example: customers and their orders

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
customer_id | full_name     | order_id | status
------------+---------------+----------+----------
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
(14 rows)
```

Study this result carefully:

- Customers 1, 2, 3 and 7 have two orders each, so they appear twice (one row per matching order).
- Customers 4 and 5 have one order each.
- Customers **6, 8, 9 and 10 have no orders**, but they still appear, once each, with `NULL` in `order_id` and `status`. With an inner join they would have vanished.
- Orders 107 and 108 do not appear, because they belong to the *right* table and we only keep all rows from the *left* table (customers) in this query.

Total rows: 4 customers x 2 + 2 customers x 1 + 4 customers x 1 (the unmatched ones) = 14.

#### Comparing against the inner join

```sql
SELECT
  (SELECT COUNT(*) FROM customers AS c INNER JOIN orders AS o ON o.customer_id = c.customer_id) AS inner_rows,
  (SELECT COUNT(*) FROM customers AS c LEFT  JOIN orders AS o ON o.customer_id = c.customer_id) AS left_rows;
```

**Result:**

```text
inner_rows | left_rows
-----------+----------
10         | 14
(1 row)
```

`LEFT JOIN` always returns **at least as many rows** as the left table has (here at least 10), and at least as many as the inner join. The difference between the two counts (14 minus 10 = 4) is exactly the number of left rows without a match.

### 3. The anti-join pattern: finding rows with no match

Because unmatched rows have NULLs in the right table's columns, we can keep **only** those rows with `WHERE right_key IS NULL`. This is called an **anti-join**: "left rows that have no partner". It is arguably the most useful pattern in QA data validation.

#### Customers who never ordered

```sql
SELECT c.customer_id, c.full_name, c.email
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name  | email
------------+------------+-----------------
6           | Frank Lee  | NULL
8           | Bob Smith  | bob@example.com
9           | Hana Sato  | hana@example.com
10          | Ian Brooks | ian@example.com
(4 rows)
```

The four customers: Frank Lee (6), the duplicate Bob Smith (8), Hana Sato (9), Ian Brooks (10). Notice we test `o.order_id IS NULL`, using the right table's **primary key**, which can never be NULL in a real row. That guarantees a NULL means "no match", never "a real row with an empty value". Do not test a nullable column such as `o.status` for this.

#### Orphan orders: orders whose customer does not exist

Now we flip the tables: keep every order, and look for the ones without a customer.

```sql
SELECT o.order_id, o.customer_id, o.status, o.total_amount
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
ORDER BY o.order_id;
```

**Result:**

```text
order_id | customer_id | status    | total_amount
---------+-------------+-----------+-------------
107      | 99          | completed | 35.0
108      | NULL        | completed | 9.99
(2 rows)
```

Two orders: **107** (customer 99 does not exist, a true orphan) and **108** (customer is NULL, a guest order). To separate these two cases:

```sql
SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
  AND o.customer_id IS NOT NULL;
```

**Result:**

```text
order_id | customer_id
---------+------------
107      | 99
(1 row)
```

Only order 107 is a genuine referential-integrity violation. Order 108 might be acceptable (guest checkout) or might be a defect, depending on the business rule; QA asks the product owner. The anti-join gives you the evidence for that conversation.

#### Other orphan and gap checks with the same pattern

Order items whose order does not exist:

```sql
SELECT i.item_id, i.order_id, i.product_id
FROM order_items AS i
LEFT JOIN orders AS o ON o.order_id = i.order_id
WHERE o.order_id IS NULL;
```

**Result:**

```text
item_id | order_id | product_id
--------+----------+-----------
14      | 999      | 2
(1 row)
```

Order items whose product does not exist:

```sql
SELECT i.item_id, i.order_id, i.product_id
FROM order_items AS i
LEFT JOIN products AS p ON p.product_id = i.product_id
WHERE p.product_id IS NULL;
```

**Result:**

```text
item_id | order_id | product_id
--------+----------+-----------
15      | 111      | 999
(1 row)
```

Payments whose order does not exist:

```sql
SELECT pay.payment_id, pay.order_id, pay.amount
FROM payments AS pay
LEFT JOIN orders AS o ON o.order_id = pay.order_id
WHERE o.order_id IS NULL;
```

**Result:**

```text
payment_id | order_id | amount
-----------+----------+-------
10         | 888      | 10.0
(1 row)
```

Orders that have no items (this time the *parent* is on the left, looking for missing children):

```sql
SELECT o.order_id, o.status, o.total_amount
FROM orders AS o
LEFT JOIN order_items AS i ON i.order_id = o.order_id
WHERE i.item_id IS NULL
ORDER BY o.order_id;
```

**Result:**

```text
order_id | status  | total_amount
---------+---------+-------------
109      | pending | 80.0
(1 row)
```

Only order 109 has no item rows: it is pending with a header total of 80.00 but no lines to justify that amount. Every other order has at least one item row (even the problematic ones: order 107 has item 10, order 108 has item 11, and order 111 has item 15, which points to a missing product, a different problem).

Products that were never sold:

```sql
SELECT p.product_id, p.product_name, p.category
FROM products AS p
LEFT JOIN order_items AS i ON i.product_id = p.product_id
WHERE i.item_id IS NULL
ORDER BY p.product_id;
```

**Result:**

```text
product_id | product_name  | category
-----------+---------------+------------
7          | Webcam HD     | Electronics
8          | Standing Desk | Furniture
(2 rows)
```

Webcam HD (7) and Standing Desk (8) never appear on an order line. These are the 14th planted bug.

Defects not linked to any product (here the NULL is in the *left* table's own foreign key):

```sql
SELECT d.defect_id, d.title, d.severity
FROM defects AS d
LEFT JOIN products AS p ON p.product_id = d.product_id
WHERE p.product_id IS NULL;
```

**Result:**

```text
defect_id | title                 | severity
----------+-----------------------+---------
3         | Checkout page timeout | critical
(1 row)
```

Defect 3, "Checkout page timeout", is a general defect with no product. Again, whether that is acceptable is a business decision.

### 4. Showing "no match" nicely: COALESCE

`COALESCE(a, b, c, ...)` returns the first argument that is not NULL. It is useful for replacing the NULLs that outer joins create with a readable label:

```sql
SELECT c.full_name,
       COALESCE(o.order_id, 0)        AS order_id_or_zero,
       COALESCE(o.status, 'no orders') AS status_label
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE c.customer_id >= 6
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
full_name  | order_id_or_zero | status_label
-----------+------------------+-------------
Frank Lee  | 0                | no orders
Grace Kim  | 109              | pending
Grace Kim  | 112              | completed
Bob Smith  | 0                | no orders
Hana Sato  | 0                | no orders
Ian Brooks | 0                | no orders
(6 rows)
```

Customers 6, 8, 9, 10 show `0` and `no orders` instead of NULL, which suits reports. Do the NULL replacement only in output; in validation queries keep NULL, because `IS NULL` is the test.

### 5. Counting with LEFT JOIN: COUNT(*) vs COUNT(column)

We use aggregate functions (the next lessons today explain them fully). `COUNT(*)` counts rows; `COUNT(column)` counts rows where that column is **not NULL**. Compare:

```sql
SELECT c.customer_id,
       c.full_name,
       COUNT(*)          AS rows_in_result,
       COUNT(o.order_id) AS real_orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name     | rows_in_result | real_orders
------------+---------------+----------------+------------
1           | Alice Johnson | 2              | 2
2           | Bob Smith     | 2              | 2
3           | Carla Gomez   | 2              | 2
4           | Dev Patel     | 1              | 1
5           | Eve Muller    | 1              | 1
6           | Frank Lee     | 1              | 0
7           | Grace Kim     | 2              | 2
8           | Bob Smith     | 1              | 0
9           | Hana Sato     | 1              | 0
10          | Ian Brooks    | 1              | 0
(10 rows)
```

Customer 9 has `rows_in_result = 1` (the single row with NULLs) but `real_orders = 0`. If you used `COUNT(*)` you would claim that customer 9 has one order. **With a LEFT JOIN, count a column from the right table, normally its primary key.** This is a very common bug in reports.

### 6. The big trap: WHERE vs ON with a LEFT JOIN

Suppose we want "each customer and their *completed* orders, but still list customers without any". Two versions look nearly identical:

**Version A: filter in WHERE**

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
customer_id | full_name     | order_id | status
------------+---------------+----------+----------
1           | Alice Johnson | 101      | completed
1           | Alice Johnson | 102      | completed
2           | Bob Smith     | 103      | completed
2           | Bob Smith     | 110      | completed
3           | Carla Gomez   | 111      | completed
7           | Grace Kim     | 112      | completed
(6 rows)
```

**Version B: filter in ON**

```sql
SELECT c.customer_id, c.full_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
                     AND o.status = 'completed'
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
customer_id | full_name     | order_id | status
------------+---------------+----------+----------
1           | Alice Johnson | 101      | completed
1           | Alice Johnson | 102      | completed
2           | Bob Smith     | 103      | completed
2           | Bob Smith     | 110      | completed
3           | Carla Gomez   | 111      | completed
4           | Dev Patel     | NULL     | NULL
5           | Eve Muller    | NULL     | NULL
6           | Frank Lee     | NULL     | NULL
7           | Grace Kim     | 112      | completed
8           | Bob Smith     | NULL     | NULL
9           | Hana Sato     | NULL     | NULL
10          | Ian Brooks    | NULL     | NULL
(12 rows)
```

Version A returned only customers with completed orders (6 rows): customers 4, 5, 6, 8, 9, 10 vanished. Why? After the join, unmatched customers have `o.status = NULL`, and `NULL = 'completed'` is not true, so `WHERE` throws those rows away. **The LEFT JOIN has been silently turned into an INNER JOIN.** Version B keeps every customer, because the `ON` condition only decides *which right-hand rows can match*; the left rows are always kept.

Rule of thumb:

- A condition on the **left** table: put it in `WHERE`.
- A condition on the **right** table that you want to apply *while keeping unmatched left rows*: put it in `ON`.
- A `WHERE` condition on the right table is only correct when you do want to throw away non-matching rows, or when you test `IS NULL` (the anti-join).

### 7. The order of tables matters

`A LEFT JOIN B` and `B LEFT JOIN A` are **not** the same. Compare the number of rows when we swap:

```sql
SELECT 'customers LEFT JOIN orders' AS query, COUNT(*) AS row_count
FROM customers AS c LEFT JOIN orders AS o ON o.customer_id = c.customer_id
UNION ALL
SELECT 'orders LEFT JOIN customers', COUNT(*)
FROM orders AS o LEFT JOIN customers AS c ON c.customer_id = o.customer_id;
```

**Result:**

```text
query                      | row_count
---------------------------+----------
customers LEFT JOIN orders | 14
orders LEFT JOIN customers | 12
(2 rows)
```

(`UNION ALL` simply stacks two results; it is used here only to display both counts in one table.) The first query keeps all customers (14 rows including the four with no orders), the second keeps all orders (12 rows including the orphan and the guest order). Choose the left table to be **the one you want to preserve in full**.

### 8. RIGHT JOIN

#### What it does

`RIGHT JOIN` is the mirror image: it keeps **all rows from the right table**, with NULLs where the left table has no match.

```text
SELECT columns
FROM   left_table
RIGHT JOIN right_table
        ON left_table.key = right_table.key;
```

#### Which SQLite version do we have?

`RIGHT JOIN` and `FULL JOIN` were added to SQLite in version **3.39.0 (June 2022)**. Older versions (for example the one bundled with older Python or macOS releases) report an error such as `RIGHT and FULL OUTER JOINs are not currently supported`. Check yours:

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

The examples in this lesson were run on 3.45.1, which supports `RIGHT JOIN`. If your version prints something lower than 3.39, use the swap trick shown below instead.

#### Example

All customers, and the orders they placed (keeping every customer): written as a RIGHT JOIN, the customers table must be on the right:

```sql
SELECT o.order_id, c.customer_id, c.full_name
FROM orders AS o
RIGHT JOIN customers AS c
        ON o.customer_id = c.customer_id
WHERE c.customer_id IN (1, 6, 9)
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
order_id | customer_id | full_name
---------+-------------+--------------
101      | 1           | Alice Johnson
102      | 1           | Alice Johnson
NULL     | 6           | Frank Lee
NULL     | 9           | Hana Sato
(4 rows)
```

Here `customers` is the right table, so all customers are kept; customers 6 and 9 show NULL order IDs.

#### RIGHT JOIN is just LEFT JOIN with the tables swapped

The query above is exactly equivalent to this LEFT JOIN, with the tables in the other positions:

```sql
SELECT o.order_id, c.customer_id, c.full_name
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id
WHERE c.customer_id IN (1, 6, 9)
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
order_id | customer_id | full_name
---------+-------------+--------------
101      | 1           | Alice Johnson
102      | 1           | Alice Johnson
NULL     | 6           | Frank Lee
NULL     | 9           | Hana Sato
(4 rows)
```

Same rows, same order. That is why many style guides say: **write LEFT JOIN only**, and put the table you want to keep in full in `FROM`. Reading a query top to bottom is easier when the "main" table comes first. Many teams ban RIGHT JOIN from their SQL standards for readability, but you must still recognise it when reading other people's SQL.

#### A RIGHT JOIN anti-join

Products that were never sold, written with a right join:

```sql
SELECT p.product_id, p.product_name
FROM order_items AS i
RIGHT JOIN products AS p ON p.product_id = i.product_id
WHERE i.item_id IS NULL
ORDER BY p.product_id;
```

**Result:**

```text
product_id | product_name
-----------+--------------
7          | Webcam HD
8          | Standing Desk
(2 rows)
```

Same answer as the left-join version earlier: products 7 and 8.

### 9. Dialect support summary

| Database | LEFT JOIN | RIGHT JOIN | FULL JOIN |
|---|---|---|---|
| SQLite 3.39+ | Yes | Yes | Yes |
| SQLite before 3.39 | Yes | **No** | **No** |
| MySQL / MariaDB | Yes | Yes | **No** (emulate) |
| PostgreSQL | Yes | Yes | Yes |
| SQL Server | Yes | Yes | Yes |
| Oracle | Yes | Yes | Yes |

On older SQLite, rewrite every `RIGHT JOIN` as a `LEFT JOIN` with the table order swapped, exactly as shown above. The FULL JOIN lesson covers how to emulate the join that MySQL and old SQLite lack.

### 10. Real-world QA scenarios

**A reusable orphan-detection report.** Combine several of the checks into one table of counts. Any non-zero result is a finding:

```sql
SELECT 'orders without customer' AS check_name, COUNT(*) AS violations
FROM orders AS o LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.customer_id IS NOT NULL AND c.customer_id IS NULL
UNION ALL
SELECT 'items without order', COUNT(*)
FROM order_items AS i LEFT JOIN orders AS o ON o.order_id = i.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'items without product', COUNT(*)
FROM order_items AS i LEFT JOIN products AS p ON p.product_id = i.product_id
WHERE p.product_id IS NULL
UNION ALL
SELECT 'payments without order', COUNT(*)
FROM payments AS pay LEFT JOIN orders AS o ON o.order_id = pay.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'orders without items', COUNT(*)
FROM orders AS o LEFT JOIN order_items AS i ON i.order_id = o.order_id
WHERE i.item_id IS NULL;
```

**Result:**

```text
check_name              | violations
------------------------+-----------
orders without customer | 1
items without order     | 1
items without product   | 1
payments without order  | 1
orders without items    | 1
(5 rows)
```

You will extend this style in the "Test-data validation using SQL" lesson. In test automation, such a query runs after a data load, and the test fails if any count is above zero.

**Completed orders without a payment.** Left join `orders` to `payments` and look for NULL payments among completed orders:

```sql
SELECT o.order_id, o.status, o.total_amount
FROM orders AS o
LEFT JOIN payments AS pay ON pay.order_id = o.order_id
WHERE o.status = 'completed'
  AND pay.payment_id IS NULL;
```

**Result:**

```text
order_id | status    | total_amount
---------+-----------+-------------
112      | completed | 9.99
(1 row)
```

Order 112 is "completed" but nothing was ever paid, a legitimate business-logic bug candidate.

**Product defect report including products with zero defects:**

```sql
SELECT p.product_name,
       COUNT(d.defect_id) AS defect_count
FROM products AS p
LEFT JOIN defects AS d ON d.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY defect_count DESC, p.product_id;
```

**Result:**

```text
product_name   | defect_count
---------------+-------------
Laptop Pro     | 1
Wireless Mouse | 1
USB-C Cable    | 1
Desk Chair     | 1
Monitor 27in   | 1
Notebook       | 0
Webcam HD      | 0
Standing Desk  | 0
(8 rows)
```

### 11. Common mistakes

1. Filtering the right table in `WHERE` and unknowingly turning the join into an inner join.
2. Using `COUNT(*)` instead of `COUNT(right_table.pk)`.
3. Testing a nullable column (instead of the primary key) for `IS NULL` in an anti-join.
4. Choosing the wrong table as the left table.
5. Assuming a NULL foreign key is an orphan (it is "no parent", not "missing parent").
6. Writing `RIGHT JOIN` on an older SQLite and getting a syntax error.

## Practice Questions

**Q1.** List all products with the number of order lines each appears on (0 for never sold). Use `LEFT JOIN`.

**Q2.** List customers from the `US` who have no completed order.

**Q3.** Why does `SELECT ... FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id WHERE o.total_amount > 100` not return customers with no orders, even though it is a LEFT JOIN?

**Q4.** Rewrite `FROM orders o RIGHT JOIN payments pay ON pay.order_id = o.order_id` as a LEFT JOIN, and use it to find orphan payments.

**Q5.** Which orders have a total of 0 matching payment rows, regardless of status? (Show order id and status.)

### Answers

**A1.**

```sql
SELECT p.product_id, p.product_name, COUNT(i.item_id) AS order_lines
FROM products AS p
LEFT JOIN order_items AS i ON i.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY p.product_id;
```

**Result:**

```text
product_id | product_name   | order_lines
-----------+----------------+------------
1          | Laptop Pro     | 2
2          | Wireless Mouse | 4
3          | USB-C Cable    | 4
4          | Desk Chair     | 2
5          | Notebook       | 2
6          | Monitor 27in   | 1
7          | Webcam HD      | 0
8          | Standing Desk  | 0
(8 rows)
```

**A2.**

```sql
SELECT c.customer_id, c.full_name
FROM customers AS c
LEFT JOIN orders AS o
       ON o.customer_id = c.customer_id AND o.status = 'completed'
WHERE c.country = 'US' AND o.order_id IS NULL
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name
------------+----------
8           | Bob Smith
(1 row)
```

The completed-status filter is in `ON` (so customers still survive), and the anti-join test is in `WHERE`. Customer 8 (duplicate Bob) has no orders at all; the other US customers, 1, 2 and 7, each have a completed order.

**A3.** The `WHERE` condition on the right table compares `NULL > 100`, which is not true, so the unmatched rows are filtered out; the join behaves like an inner join. Move the condition to `ON` to keep unmatched customers.

**A4.**

```sql
SELECT pay.payment_id, pay.order_id
FROM payments AS pay
LEFT JOIN orders AS o ON o.order_id = pay.order_id
WHERE o.order_id IS NULL;
```

**Result:**

```text
payment_id | order_id
-----------+---------
10         | 888
(1 row)
```

Payment 10, which refers to order 888.

**A5.**

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

## Summary / Key Takeaways

- `LEFT JOIN` keeps **every row from the left table**; unmatched rows get NULLs for the right table's columns.
- The **anti-join** (`LEFT JOIN ... WHERE right.pk IS NULL`) finds rows with no partner: orphans, never-ordered customers, unsold products, orders without items.
- A `WHERE` filter on the right table cancels the outer behaviour; put such filters in `ON` if you want to keep unmatched left rows.
- Use `COUNT(right.pk)`, not `COUNT(*)`, when counting matches after a left join.
- `RIGHT JOIN` is a mirror image. Swapping the table order turns it into a `LEFT JOIN`; most teams write only left joins.
- `RIGHT` and `FULL` joins need SQLite 3.39+ (we used 3.45.1). Check with `SELECT sqlite_version();`.
- `NULL` foreign key means "no parent"; a non-NULL value with no matching parent is the real orphan.

## Additional Resources

- SQLite documentation, SELECT (join types and the ON clause): https://www.sqlite.org/lang_select.html
- SQLite release notes for 3.39.0 (RIGHT and FULL OUTER JOIN support): https://www.sqlite.org/releaselog/3_39_0.html
- PostgreSQL documentation, Joined Tables: https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-FROM
