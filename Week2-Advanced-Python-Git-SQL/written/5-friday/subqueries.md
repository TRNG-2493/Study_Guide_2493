# Subqueries

## Learning Objectives

By the end of this lesson you will be able to:

- Define a subquery (nested query) and say where in a SQL statement one may appear.
- Distinguish **scalar**, **single-column (list)** and **table (derived)** subqueries.
- Use subqueries with `IN`, `NOT IN`, `EXISTS`, `NOT EXISTS` and comparison operators.
- Explain the difference between an **uncorrelated** and a **correlated** subquery.
- Avoid the dangerous `NOT IN` + NULL trap.
- Decide when a join or a subquery is the better tool, and rewrite one as the other.
- Use subqueries for QA checks such as "orders whose header total differs from the sum of their items".

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

This week's epic adds SQL for QA data validation and starts the Project 1 "QE Foundations" capstone. Many validation questions are really *two-step* questions:

- "Which orders cost more than the **average** order?" (First compute the average, then compare.)
- "Which customers have **not** placed any order?" (First find who has ordered, then exclude them.)
- "Which products appear in an order that was **cancelled**?" (First find the cancelled orders, then look up their products.)

A **subquery** lets you write the first step *inside* the second, in a single statement. Instead of running two queries and copying a number between them (which fails the moment data changes), one query does both. Test engineers also use subqueries inside automated checks because the check stays self-contained and repeatable.

## The Concept

### 1. What is a subquery?

A **subquery** (also *inner query* or *nested query*) is a `SELECT` statement written inside another SQL statement, wrapped in parentheses. The surrounding statement is the **outer query**.

```text
SELECT ...
FROM   ...
WHERE  column OPERATOR ( SELECT ... FROM ... );   <-- subquery in parentheses
```

Analogy: you ask a colleague, "Who sold more than the team average?" To answer, she first calculates the team average (the inner question), then compares each person's total to it (the outer question). A subquery is that hidden inner question.

Where may a subquery go?

| Position | Typical form | Subquery must return |
|---|---|---|
| `WHERE` / `HAVING` | `col > (SELECT ...)`, `col IN (SELECT ...)`, `EXISTS (SELECT ...)` | one value, one column, or rows (for EXISTS) |
| `FROM` | `FROM (SELECT ...) AS alias` | a table (any shape); an alias is required in most databases |
| `SELECT` list | `SELECT a, (SELECT ...) AS x` | exactly one value (scalar) |
| `INSERT/UPDATE/DELETE` | `... WHERE id IN (SELECT ...)` | as the context needs |

### 2. Scalar subqueries (return one value)

A **scalar subquery** returns exactly one row with one column: one single value. You can use it anywhere a single value is allowed.

First, the helper question on its own: what is the average order total?

```sql
SELECT AVG(total_amount) AS avg_order_total FROM orders;
```

**Result:**

```text
avg_order_total
-----------------
287.5366666666667
(1 row)
```

(`AVG` is an aggregate function: it calculates the mean. Aggregates have their own lesson later today.) Now plug that question into the outer query, so we get orders above the average:

```sql
SELECT order_id, total_amount
FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders)
ORDER BY total_amount DESC;
```

**Result:**

```text
order_id | total_amount
---------+-------------
101      | 1225.0
106      | 1200.0
104      | 600.0
(3 rows)
```

How it executes:

1. The database runs the inner `SELECT AVG(total_amount) FROM orders` once and gets about 287.54.
2. It treats the result as a constant and evaluates `total_amount > 287.54` for every row of the outer query.
3. Orders 101 (1225.00), 106 (1200.00) and 104 (600.00) qualify.

If a scalar subquery returns *more than one row*, most databases raise an error ("subquery returns more than 1 row"). SQLite is permissive and silently uses the first row, which can hide a bug; as a tester you should make scalar subqueries return exactly one row (use an aggregate or a unique key).

More scalar examples:

```sql
-- the most expensive product(s)
SELECT product_id, product_name, unit_price
FROM products
WHERE unit_price = (SELECT MAX(unit_price) FROM products);
```

**Result:**

```text
product_id | product_name | unit_price
-----------+--------------+-----------
1          | Laptop Pro   | 1200.0
(1 row)
```

```sql
-- orders placed on the most recent order date
SELECT order_id, order_date
FROM orders
WHERE order_date = (SELECT MAX(order_date) FROM orders);
```

**Result:**

```text
order_id | order_date
---------+-----------
112      | 2025-07-25
(1 row)
```

### 3. Single-column subqueries with IN and NOT IN

A subquery that returns **one column and many rows** is a list, and works with `IN`.

**Customers who have placed at least one order:**

```sql
SELECT customer_id, full_name
FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)
ORDER BY customer_id;
```

**Result:**

```text
customer_id | full_name
------------+--------------
1           | Alice Johnson
2           | Bob Smith
3           | Carla Gomez
4           | Dev Patel
5           | Eve Muller
7           | Grace Kim
(6 rows)
```

The inner query returns the list `1, 1, 2, 3, 4, 5, 99, NULL, 7, 2, 3, 7` (duplicates are harmless in `IN`). The outer query keeps customers whose ID is in the list. Six customers qualify: 1, 2, 3, 4, 5, 7.

**Products that appear on cancelled orders**, a two-level nesting:

```sql
SELECT product_id, product_name
FROM products
WHERE product_id IN (
    SELECT product_id
    FROM order_items
    WHERE order_id IN (SELECT order_id FROM orders WHERE status = 'cancelled')
);
```

**Result:**

```text
product_id | product_name
-----------+-------------
1          | Laptop Pro
(1 row)
```

Read from the inside out: cancelled orders (just 106) -> items on those orders (product 1) -> the product row (Laptop Pro).

### 4. The NOT IN trap with NULL

It seems natural to find "customers who have never ordered" with `NOT IN`:

```sql
SELECT customer_id, full_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```

**Result:**

```text
customer_id | full_name
------------+----------
(0 rows)
```

**Zero rows!** But we know customers 6, 8, 9, 10 never ordered. What went wrong? The subquery's list contains a `NULL` (order 108 has no customer). `x NOT IN (1, 2, 99, NULL)` means `x <> 1 AND x <> 2 AND x <> 99 AND x <> NULL`, and `x <> NULL` is *unknown*, never true, so the whole condition can never be true. **A single NULL in the list makes `NOT IN` return nothing.** This is a classic bug that passes review because the query "looks right", and test data without NULLs hides it.

Safe fixes:

```sql
-- Fix 1: filter out NULLs in the subquery
SELECT customer_id, full_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY customer_id;
```

**Result:**

```text
customer_id | full_name
------------+-----------
6           | Frank Lee
8           | Bob Smith
9           | Hana Sato
10          | Ian Brooks
(4 rows)
```

```sql
-- Fix 2 (preferred): NOT EXISTS, explained below
SELECT c.customer_id, c.full_name
FROM customers AS c
WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name
------------+-----------
6           | Frank Lee
8           | Bob Smith
9           | Hana Sato
10          | Ian Brooks
(4 rows)
```

Both return customers 6, 8, 9 and 10. (A third alternative is the `LEFT JOIN ... IS NULL` anti-join from the previous lesson.)

### 5. Correlated subqueries and EXISTS

#### Uncorrelated vs correlated

So far each subquery was **uncorrelated**: it can run on its own and is evaluated once. A **correlated** subquery refers to a column of the **outer** query, so conceptually it is re-evaluated for each outer row, like a loop:

```text
for each customer c in the outer query:
    run the inner query using c.customer_id
```

#### EXISTS and NOT EXISTS

`EXISTS (subquery)` is true if the subquery returns **at least one row**. What columns the subquery selects is irrelevant, so we conventionally write `SELECT 1`.

**Customers who have at least one completed order:**

```sql
SELECT c.customer_id, c.full_name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id      -- correlation: uses the OUTER c
      AND o.status = 'completed'
)
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name
------------+--------------
1           | Alice Johnson
2           | Bob Smith
3           | Carla Gomez
7           | Grace Kim
(4 rows)
```

For each customer the inner query asks "is there an order with *this* customer's ID that is completed?" It stops looking at the first hit, which makes `EXISTS` efficient and, importantly, **safe with NULLs**.

`NOT EXISTS` reverses it. Order items whose order is missing (an orphan check done with a subquery):

```sql
SELECT i.item_id, i.order_id
FROM order_items AS i
WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.order_id = i.order_id);
```

**Result:**

```text
item_id | order_id
--------+---------
14      | 999
(1 row)
```

Item 14 is the orphan.

#### Correlated subquery in the SELECT list

A scalar correlated subquery can produce a computed column per row. For each customer, how many orders do they have?

```sql
SELECT c.customer_id,
       c.full_name,
       (SELECT COUNT(*) FROM orders AS o WHERE o.customer_id = c.customer_id) AS order_count
FROM customers AS c
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name     | order_count
------------+---------------+------------
1           | Alice Johnson | 2
2           | Bob Smith     | 2
3           | Carla Gomez   | 2
4           | Dev Patel     | 1
5           | Eve Muller    | 1
6           | Frank Lee     | 0
7           | Grace Kim     | 2
8           | Bob Smith     | 0
9           | Hana Sato     | 0
10          | Ian Brooks    | 0
(10 rows)
```

Every customer appears (even those with 0), because the subquery is evaluated per customer row. This is another way to get the same answer as `LEFT JOIN ... GROUP BY`.

### 6. Subqueries in FROM: derived tables

A subquery in `FROM` acts as a temporary table that exists only for that query. It **must have an alias**. This is useful when you need to aggregate first and then filter or join the aggregated result.

**Step 1:** total of order items per order (the "recomputed" total):

```sql
SELECT order_id, SUM(quantity * unit_price) AS items_total
FROM order_items
GROUP BY order_id
ORDER BY order_id;
```

**Result:**

```text
order_id | items_total
---------+------------
101      | 1225.0
102      | 30.48
103      | 300.0
104      | 600.0
105      | 34.99
106      | 1200.0
107      | 35.0
108      | 9.99
110      | 50.0
111      | 19.99
112      | -9.99
999      | 25.0
(12 rows)
```

**Step 2:** use that as a derived table and compare it with the order header's total:

```sql
SELECT o.order_id, o.total_amount AS header_total, t.items_total
FROM orders AS o
INNER JOIN (
    SELECT order_id, SUM(quantity * unit_price) AS items_total
    FROM order_items
    GROUP BY order_id
) AS t ON t.order_id = o.order_id
WHERE ROUND(o.total_amount, 2) <> ROUND(t.items_total, 2)
ORDER BY o.order_id;
```

**Result:**

```text
order_id | header_total | items_total
---------+--------------+------------
103      | 150.0        | 300.0
110      | 55.0         | 50.0
112      | 9.99         | -9.99
(3 rows)
```

Three orders have a header total that disagrees with their items: **103** (the duplicate item row doubles the items total to 300.00 while the header says 150.00), **110** (header 55.00 versus items 50.00) and **112** (the negative quantity makes the items total -9.99 while the header says 9.99). Notice what the query does *not* report: order 109 (header 80.00 but no items) is invisible because the `INNER JOIN` to the derived table drops orders with no items. A complete validation would add a `LEFT JOIN` for that case (you will build this in the validation lesson). Order 111 is also not listed because its item price happens to equal the header, even though the item points to a missing product, which is a different defect found by a different check. This is a real data-validation query that you will extend in "Test-data validation using SQL".

`ROUND(x, 2)` guards against floating-point noise such as `30.480000000000004` versus `30.48`.

### 7. Subqueries versus joins

Many subqueries can be rewritten as joins and vice versa:

| Task | Subquery form | Join form |
|---|---|---|
| Customers with orders | `WHERE id IN (SELECT customer_id FROM orders)` | `INNER JOIN` + `DISTINCT` |
| Customers without orders | `WHERE NOT EXISTS (...)` | `LEFT JOIN ... IS NULL` |
| Compare to an aggregate | `WHERE x > (SELECT AVG(x) ...)` | usually needs a subquery anyway |

Guidelines:

- Use a **join** when you need *columns from both tables* in the output.
- Use `EXISTS` / `IN` when you only need to *test* for a related row and do not want row multiplication.
- Use a **scalar subquery** for comparing against an aggregate.
- Choose whichever is more readable for your team. How the database optimises each form is a performance topic for a later week.

Compare: customers with orders, using `IN` (no duplicates) versus a join (duplicates unless `DISTINCT`):

```sql
SELECT 'IN subquery' AS form, COUNT(*) AS rows_returned
FROM customers WHERE customer_id IN (SELECT customer_id FROM orders)
UNION ALL
SELECT 'inner join', COUNT(*)
FROM customers AS c INNER JOIN orders AS o ON o.customer_id = c.customer_id
UNION ALL
SELECT 'inner join + DISTINCT', COUNT(*) FROM (
  SELECT DISTINCT c.customer_id FROM customers AS c INNER JOIN orders AS o ON o.customer_id = c.customer_id
);
```

**Result:**

```text
form                  | rows_returned
----------------------+--------------
IN subquery           | 6
inner join            | 10
inner join + DISTINCT | 6
(3 rows)
```

The join returns 10 rows (one per order) while the subquery returns 6 (one per customer). Same logic, different row counts: that matters when you assert on row counts in a test.

### 8. Subqueries with UPDATE and DELETE

As you saw in the DML lesson, subqueries are valid in `UPDATE` and `DELETE`. Inside a safe transaction, delete order items that point to a non-existent order:

```sql
BEGIN;

DELETE FROM order_items
WHERE order_id NOT IN (SELECT order_id FROM orders);

SELECT item_id FROM order_items WHERE item_id = 14;

ROLLBACK;
```

**Result:**

```text
OK

OK: 1 row(s) affected

item_id
-------
(0 rows)

OK
```

Item 14 is gone inside the transaction; the `ROLLBACK` restored it. (Here `NOT IN` is safe because `orders.order_id` is a primary key and can never be NULL. Always ask "can the subquery column be NULL?".)

### 9. Real-world QA scenarios

**1. Find orders whose customer is in a high-risk country list kept in another query.** Replace with any rule table; the idea is identical.

**2. Highest-value order per customer** (a "top row per group" problem; there are more elegant tools for it in later weeks, but a correlated subquery works):

```sql
SELECT o.customer_id, o.order_id, o.total_amount
FROM orders AS o
WHERE o.customer_id IS NOT NULL
  AND o.total_amount = (
        SELECT MAX(o2.total_amount)
        FROM orders AS o2
        WHERE o2.customer_id = o.customer_id
      )
ORDER BY o.customer_id;
```

**Result:**

```text
customer_id | order_id | total_amount
------------+----------+-------------
1           | 101      | 1225.0
2           | 103      | 150.0
3           | 104      | 600.0
4           | 105      | 34.99
5           | 106      | 1200.0
7           | 109      | 80.0
99          | 107      | 35.0
(7 rows)
```

(Customer 99 appears because order 107 is the orphan order, a reminder that these queries do not check key validity.) The inner query uses a second alias `o2` for the *same table* so it can compare each order with that customer's other orders. We will cover more advanced per-group techniques (window functions) in a later week.

**3. Customers who bought a Laptop but never a Mouse** (combining EXISTS and NOT EXISTS):

```sql
SELECT c.customer_id, c.full_name
FROM customers AS c
WHERE EXISTS (
        SELECT 1 FROM orders o JOIN order_items i ON i.order_id = o.order_id
        WHERE o.customer_id = c.customer_id AND i.product_id = 1)
  AND NOT EXISTS (
        SELECT 1 FROM orders o JOIN order_items i ON i.order_id = o.order_id
        WHERE o.customer_id = c.customer_id AND i.product_id = 2);
```

**Result:**

```text
customer_id | full_name
------------+-----------
5           | Eve Muller
(1 row)
```

Alice bought both a laptop and a mouse (in order 101), so she is excluded; Eve bought only a laptop (the cancelled order 106), so she is returned.

**4. Orders with no payment at all** (the same anti-join, written with NOT EXISTS):

```sql
SELECT o.order_id, o.status
FROM orders AS o
WHERE NOT EXISTS (SELECT 1 FROM payments AS p WHERE p.order_id = o.order_id)
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

### 10. Common mistakes

1. Using `NOT IN` against a column that can contain NULL.
2. Writing a scalar subquery that returns more than one row.
3. Forgetting the alias on a subquery in `FROM`.
4. Forgetting to qualify columns inside a correlated subquery so the wrong table is used.
5. Using a join where a duplicate-free `EXISTS` was needed (inflated counts).
6. Selecting multiple columns in an `IN` subquery (`IN` expects one).

## Practice Questions

**Q1.** List products priced above the average product price.

**Q2.** List customers who have never placed an order, using `NOT EXISTS`.

**Q3.** Show orders whose total is larger than every payment made for them (hint: compare to `(SELECT MAX(amount) ...)` per order; use a correlated scalar subquery).

**Q4.** Why does `WHERE customer_id NOT IN (SELECT customer_id FROM orders)` return nothing on our data? Give the one-line fix.

**Q5.** For each product, show the name and the number of order lines it appears on, using a scalar subquery in the `SELECT` list.

### Answers

**A1.**

```sql
SELECT product_id, product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price DESC;
```

**Result:**

```text
product_id | product_name  | unit_price
-----------+---------------+-----------
1          | Laptop Pro    | 1200.0
8          | Standing Desk | 450.0
6          | Monitor 27in  | 300.0
(3 rows)
```

**A2.**

```sql
SELECT c.customer_id, c.full_name
FROM customers AS c
WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id);
```

**Result:**

```text
customer_id | full_name
------------+-----------
6           | Frank Lee
8           | Bob Smith
9           | Hana Sato
10          | Ian Brooks
(4 rows)
```

**A3.**

```sql
SELECT o.order_id, o.total_amount,
       (SELECT MAX(p.amount) FROM payments AS p WHERE p.order_id = o.order_id) AS max_payment
FROM orders AS o
WHERE o.total_amount > (SELECT MAX(p.amount) FROM payments AS p WHERE p.order_id = o.order_id);
```

**Result:**

```text
order_id | total_amount | max_payment
---------+--------------+------------
(0 rows)
```

Orders without payments produce a NULL max, and `total_amount > NULL` is not true, so they are not listed. The query returns no rows here, because wherever a payment exists it equals the header total. (A different question would be needed to catch the unpaid orders; see the earlier NOT EXISTS example.)

**A4.** The subquery list contains a NULL (order 108's customer), and `NOT IN` with a NULL in the list can never be true. Fix: add `WHERE customer_id IS NOT NULL` inside the subquery, or use `NOT EXISTS`.

**A5.**

```sql
SELECT p.product_name,
       (SELECT COUNT(*) FROM order_items AS i WHERE i.product_id = p.product_id) AS order_lines
FROM products AS p
ORDER BY p.product_id;
```

**Result:**

```text
product_name   | order_lines
---------------+------------
Laptop Pro     | 2
Wireless Mouse | 4
USB-C Cable    | 4
Desk Chair     | 2
Notebook       | 2
Monitor 27in   | 1
Webcam HD      | 0
Standing Desk  | 0
(8 rows)
```

## Summary / Key Takeaways

- A subquery is a `SELECT` inside parentheses nested in another statement; it can live in `WHERE`, `FROM` or the `SELECT` list (and in `UPDATE`/`DELETE`).
- Scalar subqueries return one value; list subqueries return one column for `IN`; derived tables in `FROM` need an alias.
- A correlated subquery refers to the outer row and is conceptually run per row; `EXISTS` / `NOT EXISTS` test for related rows and are NULL-safe.
- `NOT IN` plus a NULL in the list returns nothing: prefer `NOT EXISTS` or filter the NULLs out.
- Joins and subqueries often solve the same problem; pick by what columns you need and what reads best, and watch the row counts.
- Subqueries power real validation checks, such as comparing header totals against recomputed item totals.

## Additional Resources

- SQLite documentation, Expressions (subquery expressions, IN, EXISTS): https://www.sqlite.org/lang_expr.html
- PostgreSQL documentation, Subquery Expressions: https://www.postgresql.org/docs/current/functions-subquery.html
- MySQL Reference Manual, Subqueries: https://dev.mysql.com/doc/refman/8.0/en/subqueries.html
