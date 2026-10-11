# GROUP BY and HAVING

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what grouping does: it collapses many rows into one summary row per group.
- Write `GROUP BY` queries with the basic aggregate functions `COUNT`, `SUM`, `AVG`, `MIN` and `MAX`.
- Group by one column and by several columns.
- State the difference between `WHERE` (filters rows **before** grouping) and `HAVING` (filters groups **after** grouping).
- Describe the logical order in which SQL processes the clauses of a query.
- Know the rule "every selected column is either in `GROUP BY` or inside an aggregate", and what SQLite does differently from other databases.
- Combine joins with grouping to produce per-customer or per-category reports.
- Use `GROUP BY ... HAVING COUNT(*) > 1` to **detect duplicates**, a core QA technique.

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

This week's epic is "use SQL for QA data validation" and to start the Project 1 "QE Foundations" capstone. On Thursday you learned `SELECT`, `WHERE` and `ORDER BY`, which show you individual rows. But many testing questions are about **groups of rows**:

- "How many orders are there in each status?" (Does the count match what the dashboard shows?)
- "What is the total revenue per product category?"
- "Do any two customers share the same email?" (Duplicate data is a classic bug.)
- "Which orders contain more than one line for the same product?"

You cannot answer these by scanning rows by eye once the table has thousands or millions of rows. `GROUP BY` and `HAVING` let the database do the summarising for you, and they are essential to automate checks such as "no duplicate emails exist". The next lesson explores aggregate functions in more detail; here we learn the grouping mechanism itself.

## The Concept

### 1. The idea of grouping

Imagine a shoebox of shop receipts. If someone asks "how much did we sell per day?", you would sort the receipts into piles, one pile per day, then add up each pile. **`GROUP BY` does exactly this**: it sorts rows into piles (groups) based on the value of one or more columns, then lets you calculate one summary value per pile.

Without grouping, an aggregate function summarises the *entire table* into one row:

```sql
SELECT COUNT(*) AS number_of_orders, SUM(total_amount) AS all_totals FROM orders;
```

**Result:**

```text
number_of_orders | all_totals
-----------------+-----------
12               | 3450.44
(1 row)
```

With `GROUP BY`, you get one summary row per group:

```sql
SELECT status, COUNT(*) AS number_of_orders
FROM orders
GROUP BY status
ORDER BY status;
```

**Result:**

```text
status    | number_of_orders
----------+-----------------
cancelled | 1
completed | 8
pending   | 2
shipped   | 1
(4 rows)
```

How it works, step by step:

1. `FROM orders` supplies all 12 rows.
2. `GROUP BY status` puts rows with the same `status` into the same group. The result shows 8 `completed` orders, 2 `pending`, 1 `shipped` and 1 `cancelled`, which adds up to the 12 orders in the table.
3. `COUNT(*)` is calculated **once per group**.
4. `SELECT` returns one row per group: the group's `status` plus its count.

### 2. The five basic aggregate functions

An **aggregate function** takes many values and returns one:

| Function | Meaning |
|---|---|
| `COUNT(*)` | number of rows in the group |
| `COUNT(col)` | number of rows where `col` is not NULL |
| `SUM(col)` | total of the values |
| `AVG(col)` | average of the values |
| `MIN(col)` | smallest value |
| `MAX(col)` | largest value |

(The next lesson is devoted to these, including NULL behaviour.) Here they all appear together, grouped by product category. We join to `products` because the category lives there:

```sql
SELECT p.category,
       COUNT(*)                     AS order_lines,
       SUM(i.quantity)              AS units_sold,
       SUM(i.quantity * i.unit_price) AS revenue,
       MIN(i.unit_price)            AS cheapest,
       MAX(i.unit_price)            AS dearest
FROM order_items AS i
INNER JOIN products AS p ON p.product_id = i.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```

**Result:**

```text
category    | order_lines | units_sold | revenue | cheapest | dearest
------------+-------------+------------+---------+----------+--------
Electronics | 7           | 9          | 3125.0  | 25.0     | 1200.0
Furniture   | 2           | 2          | 300.0   | 150.0    | 150.0
Stationery  | 2           | 13         | 45.5    | 3.5      | 3.5
Accessories | 4           | 3          | 29.97   | 9.99     | 9.99
(4 rows)
```

Line by line:

- `i.quantity * i.unit_price` is arithmetic per row (line total); `SUM(...)` adds those line totals per category.
- `INNER JOIN products` is needed to get the `category`. Item 15, whose product 999 does not exist, is dropped by this join, and so is its revenue, a data-quality issue the report hides.
- `GROUP BY p.category` makes one group per category.
- `ORDER BY revenue DESC` sorts the groups; you can order by an alias that you defined in the `SELECT`.

### 3. The golden rule of GROUP BY

> **Every column in the `SELECT` list must either appear in the `GROUP BY` clause or be inside an aggregate function.**

Why? After grouping there is only *one row per group*. If you select `status` and group by `status`, that is fine: every row in the group has the same status. But if you select `order_id` while grouping by `status`, which of the (say) 8 order IDs should be shown for the single "completed" row? The question has no answer.

Standard SQL databases (PostgreSQL, SQL Server, Oracle, and MySQL with default strict settings) **reject** such a query with an error such as "column must appear in the GROUP BY clause or be used in an aggregate function". **SQLite does not**: it silently picks a value from an arbitrary row:

```sql
SELECT status, order_id, COUNT(*) AS n
FROM orders
GROUP BY status
ORDER BY status;
```

**Result:**

```text
status    | order_id | n
----------+----------+--
cancelled | 106      | 1
completed | 101      | 8
pending   | 105      | 2
shipped   | 104      | 1
(4 rows)
```

This ran without an error, but the `order_id` column is meaningless: it is one arbitrary order from each group. Treat it as a bug. As a QA engineer you should know that this leniency can hide mistakes in SQLite, and that the same query would **fail** on other databases.

### 4. Grouping by several columns

List several columns, separated by commas. A group is then a unique *combination* of values:

```sql
SELECT p.category, i.quantity, COUNT(*) AS lines
FROM order_items AS i
INNER JOIN products AS p ON p.product_id = i.product_id
GROUP BY p.category, i.quantity
ORDER BY p.category, i.quantity;
```

**Result:**

```text
category    | quantity | lines
------------+----------+------
Accessories | -1       | 1
Accessories | 1        | 2
Accessories | 2        | 1
Electronics | 1        | 5
Electronics | 2        | 2
Furniture   | 1        | 2
Stationery  | 3        | 1
Stationery  | 10       | 1
(8 rows)
```

Each row is one `(category, quantity)` pair: for example, how many Accessories lines have quantity 1, quantity 2, and so on. Notice the `-1` quantity line (item 16, the negative-quantity bug) shows up as its own group, which is another reason grouping is a good way to *spot odd values*.

### 5. Grouping and NULL

All rows with a NULL in the grouping column are placed together in **one** group (NULLs are treated as "the same" for grouping, unlike in comparisons):

```sql
SELECT customer_id, COUNT(*) AS orders_in_group, SUM(total_amount) AS revenue
FROM orders
GROUP BY customer_id
ORDER BY customer_id;
```

**Result:**

```text
customer_id | orders_in_group | revenue
------------+-----------------+--------
NULL        | 1               | 9.99
1           | 2               | 1255.48
2           | 2               | 205.0
3           | 2               | 619.99
4           | 1               | 34.99
5           | 1               | 1200.0
7           | 2               | 89.99
99          | 1               | 35.0
(8 rows)
```

The first row has `customer_id = NULL`: the single guest order 108. The customer 99 group is our orphan order. Both are problems that become *visible* when you group, but that you would not notice in a plain `SELECT` of a big table.

### 6. HAVING: filtering groups

Suppose we want only customers with **more than one** order. You might try `WHERE COUNT(*) > 1`:

```sql
SELECT customer_id, COUNT(*) AS orders_placed
FROM orders
WHERE COUNT(*) > 1
GROUP BY customer_id;
```

**Result:**

```text
Error: misuse of aggregate: COUNT()
```

That fails ("misuse of aggregate"), because `WHERE` is evaluated *before* groups exist; at that time there is no count yet. To filter on an aggregate you use **`HAVING`**, which is evaluated **after** grouping:

```sql
SELECT customer_id, COUNT(*) AS orders_placed
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY customer_id;
```

**Result:**

```text
customer_id | orders_placed
------------+--------------
1           | 2
2           | 2
3           | 2
7           | 2
(4 rows)
```

| Clause | Filters | Runs | Can use aggregates? |
|---|---|---|---|
| `WHERE` | individual **rows** | before grouping | No |
| `HAVING` | whole **groups** | after grouping | Yes |

You can use both in one query. Here: "among *completed* orders only, which customers have more than one, and what is their total?"

```sql
SELECT customer_id,
       COUNT(*)          AS completed_orders,
       SUM(total_amount) AS completed_total
FROM orders
WHERE status = 'completed'          -- row filter, applied first
GROUP BY customer_id
HAVING COUNT(*) > 1                 -- group filter, applied second
ORDER BY completed_total DESC;
```

**Result:**

```text
customer_id | completed_orders | completed_total
------------+------------------+----------------
1           | 2                | 1255.48
2           | 2                | 205.0
(2 rows)
```

Order of events: (1) `WHERE` discards non-completed orders; (2) the remaining rows are grouped by customer; (3) `HAVING` keeps only customers with more than one completed order. Customers 1 and 2 qualify. (Customer 3's second order is `shipped`, and customer 7's other order is `pending`, so they have only one completed order and drop out.)

A good rule: **put every condition that can go in `WHERE` in `WHERE`**; it is clearer and removes rows earlier. Use `HAVING` only for conditions on aggregates.

### 7. The logical order of query processing

SQL is *written* in one order but *conceptually executed* in another. This explains many "why can't I use that here?" errors:

```text
Written order:                 Logical execution order:
1. SELECT                      1. FROM / JOIN   (build the row set)
2. FROM                        2. WHERE         (filter rows)
3. JOIN                        3. GROUP BY      (make groups)
4. WHERE                       4. HAVING        (filter groups)
5. GROUP BY                    5. SELECT        (compute columns, aliases)
6. HAVING                      6. ORDER BY      (sort the result)
7. ORDER BY                    7. LIMIT         (cut the result)
```

Consequences:

- `WHERE` cannot use aggregates (groups do not exist yet).
- `WHERE` cannot use a `SELECT` alias in most databases (aliases are created at step 5). `ORDER BY` can, because it runs after.
- `HAVING` is used for conditions on aggregates.

### 8. Joins plus grouping: per-customer and per-product reports

**Revenue per customer** (join first, then group):

```sql
SELECT c.customer_id,
       c.full_name,
       COUNT(o.order_id)  AS orders_placed,
       SUM(o.total_amount) AS total_spent
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY total_spent DESC;
```

**Result:**

```text
customer_id | full_name     | orders_placed | total_spent
------------+---------------+---------------+------------
1           | Alice Johnson | 2             | 1255.48
5           | Eve Muller    | 1             | 1200.0
3           | Carla Gomez   | 2             | 619.99
2           | Bob Smith     | 2             | 205.0
7           | Grace Kim     | 2             | 89.99
4           | Dev Patel     | 1             | 34.99
(6 rows)
```

We group by both `customer_id` and `full_name`. Grouping by ID alone would work in SQLite and some databases, but listing both is portable and safe (names are not unique, so ID must be part of the grouping key; recall the two Bob Smiths).

**Include customers with no orders** by using a `LEFT JOIN` and `COUNT` on the right-hand key:

```sql
SELECT c.customer_id,
       c.full_name,
       COUNT(o.order_id)               AS orders_placed,
       COALESCE(SUM(o.total_amount),0) AS total_spent
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY c.customer_id;
```

**Result:**

```text
customer_id | full_name     | orders_placed | total_spent
------------+---------------+---------------+------------
1           | Alice Johnson | 2             | 1255.48
2           | Bob Smith     | 2             | 205.0
3           | Carla Gomez   | 2             | 619.99
4           | Dev Patel     | 1             | 34.99
5           | Eve Muller    | 1             | 1200.0
6           | Frank Lee     | 0             | 0
7           | Grace Kim     | 2             | 89.99
8           | Bob Smith     | 0             | 0
9           | Hana Sato     | 0             | 0
10          | Ian Brooks    | 0             | 0
(10 rows)
```

`SUM` over no rows returns NULL, so `COALESCE(..., 0)` displays zero instead.

**Row multiplication warning.** A join to a "many" table repeats the parent's values; summing the parent's column afterwards inflates it. For example, `SUM(o.total_amount)` after joining `orders` to `order_items` counts each order once *per item*:

```sql
SELECT SUM(o.total_amount)            AS wrong_sum_after_join,
       (SELECT SUM(total_amount) FROM orders WHERE order_id IN (SELECT order_id FROM order_items)) AS correct_sum
FROM orders AS o
INNER JOIN order_items AS i ON i.order_id = o.order_id;
```

**Result:**

```text
wrong_sum_after_join | correct_sum
---------------------+------------
4810.91              | 3370.44
(1 row)
```

The "wrong" figure is bigger because orders with several lines are counted several times. Sum the parent's amounts in a query that does not join to its children, or sum the children's line totals instead.

### 9. Detecting duplicates: GROUP BY + HAVING COUNT(*) > 1

This is the most important QA use of grouping. The recipe:

1. Decide which column(s) define "the same" (the *natural key*: the combination that should be unique).
2. `GROUP BY` those columns.
3. `HAVING COUNT(*) > 1`.

**Duplicate customer emails** (ignoring NULL, since a missing email is a different problem):

```sql
SELECT email, COUNT(*) AS occurrences
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;
```

**Result:**

```text
email           | occurrences
----------------+------------
bob@example.com | 2
(1 row)
```

`bob@example.com` appears twice (customers 2 and 8). To see *which rows*, join the duplicate list back to the table:

```sql
SELECT c.customer_id, c.full_name, c.email, c.created_date
FROM customers AS c
INNER JOIN (
    SELECT email
    FROM customers
    WHERE email IS NOT NULL
    GROUP BY email
    HAVING COUNT(*) > 1
) AS dup ON dup.email = c.email
ORDER BY c.email, c.customer_id;
```

**Result:**

```text
customer_id | full_name | email           | created_date
------------+-----------+-----------------+-------------
2           | Bob Smith | bob@example.com | 2025-01-15
8           | Bob Smith | bob@example.com | 2025-04-10
(2 rows)
```

**Duplicate order lines** (same order and same product twice):

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

Order 103 has product 4 twice (items 5 and 13). `GROUP_CONCAT` joins the item IDs into one text value; it is a SQLite/MySQL function (PostgreSQL uses `STRING_AGG`, SQL Server `STRING_AGG`), shown here because it makes the finding actionable.

**Double payments** (same order and same amount more than once):

```sql
SELECT order_id, amount, COUNT(*) AS payment_rows, GROUP_CONCAT(payment_id) AS payment_ids
FROM payments
GROUP BY order_id, amount
HAVING COUNT(*) > 1;
```

**Result:**

```text
order_id | amount | payment_rows | payment_ids
---------+--------+--------------+------------
102      | 30.48  | 2            | 2,11
(1 row)
```

Order 102 was charged 30.48 twice (payments 2 and 11): a potential double charge. Whether it is a bug depends on whether two payments were genuinely expected, so QA reports it with evidence.

### 10. Other useful patterns

**Group sizes sorted largest first:**

```sql
SELECT country, COUNT(*) AS customers
FROM customers
GROUP BY country
ORDER BY customers DESC, country;
```

**Result:**

```text
country | customers
--------+----------
US      | 4
DE      | 1
GB      | 1
IN      | 1
JP      | 1
KR      | 1
MX      | 1
(7 rows)
```

**Items per order, only orders with 2 or more lines:**

```sql
SELECT order_id, COUNT(*) AS lines, SUM(quantity) AS units
FROM order_items
GROUP BY order_id
HAVING COUNT(*) >= 2
ORDER BY order_id;
```

**Result:**

```text
order_id | lines | units
---------+-------+------
101      | 2     | 2
102      | 2     | 5
103      | 2     | 2
105      | 2     | 2
(4 rows)
```

**Filtering on a different aggregate than the displayed one** (HAVING can use any aggregate, not just those in the SELECT list):

```sql
SELECT order_id, SUM(quantity * unit_price) AS items_total
FROM order_items
GROUP BY order_id
HAVING MIN(quantity) < 1;
```

**Result:**

```text
order_id | items_total
---------+------------
112      | -9.99
(1 row)
```

Only order 112 has a line with quantity below 1, which pinpoints the negative-quantity bug. That is a one-line validation rule.

### 11. Dialect notes

- `GROUP BY` and `HAVING` work in every major database.
- SQLite allows non-aggregated, non-grouped columns in `SELECT`; PostgreSQL, SQL Server, Oracle (and MySQL with `ONLY_FULL_GROUP_BY`, its default since 5.7) reject them.
- String aggregation differs: `GROUP_CONCAT` (SQLite, MySQL), `STRING_AGG` (PostgreSQL, SQL Server 2017+).
- Some databases let you `GROUP BY` an output alias or column position; others do not. Portable queries repeat the real expression.
- Advanced grouping and window functions (running totals and rankings per group) are covered in a later week.

### 12. Common mistakes

1. Putting an aggregate in `WHERE` instead of `HAVING`.
2. Selecting a non-grouped, non-aggregated column (silently accepted by SQLite, an error elsewhere).
3. Grouping by a non-unique column such as a name when the ID is needed.
4. Summing a parent column after joining to a child table (row multiplication).
5. Using `COUNT(*)` after a `LEFT JOIN` when you mean `COUNT(right.pk)`.
6. Forgetting that NULLs form their own group.

## Practice Questions

**Q1.** How many order lines does each order have? Show only orders with exactly one line.

**Q2.** For each payment method, show the number of payments and the total amount. Which method has the larger total?

**Q3.** Which product categories have total units sold greater than 5 (join `order_items` to `products`)?

**Q4.** Write a query that finds `(order_id, product_id)` combinations appearing more than once in `order_items`. What would a trainee assert in an automated test?

**Q5.** Explain in your own words why `WHERE COUNT(*) > 1` fails but `HAVING COUNT(*) > 1` works.

### Answers

**A1.**

```sql
SELECT order_id, COUNT(*) AS lines
FROM order_items
GROUP BY order_id
HAVING COUNT(*) = 1
ORDER BY order_id;
```

**Result:**

```text
order_id | lines
---------+------
104      | 1
106      | 1
107      | 1
108      | 1
110      | 1
111      | 1
112      | 1
999      | 1
(8 rows)
```

**A2.**

```sql
SELECT method, COUNT(*) AS payments, SUM(amount) AS total
FROM payments
GROUP BY method
ORDER BY total DESC;
```

**Result:**

```text
method | payments | total
-------+----------+--------
card   | 9        | 3205.95
paypal | 2        | 159.99
(2 rows)
```

**A3.**

```sql
SELECT p.category, SUM(i.quantity) AS units
FROM order_items AS i
INNER JOIN products AS p ON p.product_id = i.product_id
GROUP BY p.category
HAVING SUM(i.quantity) > 5
ORDER BY units DESC;
```

**Result:**

```text
category    | units
------------+------
Stationery  | 13
Electronics | 9
(2 rows)
```

**A4.**

```sql
SELECT order_id, product_id, COUNT(*) AS n
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;
```

**Result:**

```text
order_id | product_id | n
---------+------------+--
103      | 4          | 2
(1 row)
```

A test would run this query and assert that the result has **zero rows**; any returned row is a failure that identifies the duplicate.

**A5.** `WHERE` is evaluated before rows are grouped, so no group count exists yet. `HAVING` is evaluated after grouping, when `COUNT(*)` has a value for each group, so it can filter groups.

## Summary / Key Takeaways

- `GROUP BY` sorts rows into groups and returns one row per group; aggregates (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) calculate a value per group.
- Every selected column must be grouped or aggregated; SQLite lets you break this rule silently, other databases do not.
- `WHERE` filters rows before grouping; `HAVING` filters groups after grouping and is the only place for conditions on aggregates.
- Logical order: FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT.
- NULLs form one group of their own, which helps reveal missing keys.
- `GROUP BY key HAVING COUNT(*) > 1` is the standard duplicate detector, and the basis for many automated data checks.
- Joining before grouping multiplies parent rows; sum the right column.

## Additional Resources

- SQLite documentation, Aggregate Functions: https://www.sqlite.org/lang_aggfunc.html
- SQLite documentation, SELECT (GROUP BY and HAVING clauses): https://www.sqlite.org/lang_select.html
- PostgreSQL documentation, Aggregate Functions and GROUP BY/HAVING: https://www.postgresql.org/docs/current/tutorial-agg.html
