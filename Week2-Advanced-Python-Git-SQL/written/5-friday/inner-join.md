# INNER JOIN

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why relational databases split data across tables and why we need joins to put it back together.
- Describe how a join works conceptually: pairing rows from two tables whenever a condition matches.
- Write an `INNER JOIN ... ON ...` query using table aliases and qualified column names.
- Predict which rows survive an inner join and which rows silently disappear (unmatched rows and NULL keys).
- Recognise "row multiplication" when one row matches several rows on the other side.
- Combine `INNER JOIN` with `WHERE`, `ORDER BY` and column aliases.
- Use inner joins in realistic QA checks, and understand why an inner join can **hide** data problems.

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

Your week-two goal is to use SQL for QA data validation, and to start your Project 1 "QE Foundations" capstone. On Thursday every query you wrote touched **one** table. But a real application never stores everything in one big table. An order screen shows the customer's name, the product names and the prices, and in the database that information lives in four different tables.

If an automated test wants to confirm "the order page shows the right customer name for order 101", it must bring `orders` and `customers` together. If you want to verify "the total for order 101 equals the sum of its items", you must connect `orders` to `order_items`. **Joins are the tool for this.** `INNER JOIN` is the most common join, and it is the foundation for every other join type you will learn today.

## The Concept

### 1. Why is data split into several tables?

Imagine storing an order in one flat table where every row repeats the customer's details:

```text
order_id | customer_name | customer_email    | product    | qty
101      | Alice Johnson | alice@example.com | Laptop Pro | 1
101      | Alice Johnson | alice@example.com | Mouse      | 1
102      | Alice Johnson | alice@example.com | Cable      | 2
```

Alice's name and email are repeated on every row. If she changes her email, you must update every row, and if you miss one, the data contradicts itself. Relational design avoids this by storing each fact **once** (this idea is called *normalisation*) and linking tables using keys:

- Alice's details are stored once in `customers`.
- Each order stores only her `customer_id`.
- The link is the primary key / foreign key pair you learned in the previous lesson.

A **join** is how a query reassembles the linked information on demand.

### 2. First, understand the "all combinations" idea (CROSS JOIN)

To understand what `ON` does, first see what happens with no condition at all. A `CROSS JOIN` pairs **every** row of the first table with **every** row of the second. It is also called a *Cartesian product*.

```sql
SELECT COUNT(*) AS combos FROM customers CROSS JOIN products;
```

**Result:**

```text
combos
------
80
(1 row)
```

10 customers x 8 products = 80 combinations. A few of them:

```sql
SELECT c.full_name, p.product_name
FROM customers AS c
CROSS JOIN products AS p
ORDER BY c.customer_id, p.product_id
LIMIT 5;
```

**Result:**

```text
full_name     | product_name
--------------+---------------
Alice Johnson | Laptop Pro
Alice Johnson | Wireless Mouse
Alice Johnson | USB-C Cable
Alice Johnson | Desk Chair
Alice Johnson | Notebook
(5 rows)
```

Alice paired with the first five products. Most of these pairs mean nothing ("Alice" and "Standing Desk" are unrelated). An **inner join** is a cross join where we keep only the pairs that satisfy a condition, normally "the foreign key equals the primary key". If you forget the join condition accidentally, you get a cross join, and the row count explodes (for two tables of 100,000 rows each, 10 billion rows!). A suspiciously large result is a classic sign of a missing `ON`.

### 3. INNER JOIN syntax

```text
SELECT   columns
FROM     table_a
INNER JOIN table_b
         ON table_a.key = table_b.key;
```

Reading it in words: "Take each row of `table_a`. Find the rows of `table_b` where the ON condition is true. For each match produce one combined row. Rows with no match are dropped."

The word `INNER` is optional; plain `JOIN` means `INNER JOIN`. Most teams write `INNER JOIN` or `JOIN` consistently. We will write `INNER JOIN` to be explicit.

#### Your first join: orders with customer names

```sql
SELECT orders.order_id, customers.full_name, orders.status, orders.total_amount
FROM orders
INNER JOIN customers
        ON orders.customer_id = customers.customer_id
ORDER BY orders.order_id;
```

**Result:**

```text
order_id | full_name     | status    | total_amount
---------+---------------+-----------+-------------
101      | Alice Johnson | completed | 1225.0
102      | Alice Johnson | completed | 30.48
103      | Bob Smith     | completed | 150.0
104      | Carla Gomez   | shipped   | 600.0
105      | Dev Patel     | pending   | 34.99
106      | Eve Muller    | cancelled | 1200.0
109      | Grace Kim     | pending   | 80.0
110      | Bob Smith     | completed | 55.0
111      | Carla Gomez   | completed | 19.99
112      | Grace Kim     | completed | 9.99
(10 rows)
```

Step by step:

1. `FROM orders` makes `orders` the "left" table (the one we start from). It has 12 rows.
2. `INNER JOIN customers` brings in the second table.
3. `ON orders.customer_id = customers.customer_id` is the **join condition**: a row of `orders` pairs with a row of `customers` only when these two values are equal. This is the foreign key matched to the primary key.
4. `SELECT orders.order_id, customers.full_name, ...` chooses columns from either table. Writing `table.column` is called **qualifying** the column.
5. `ORDER BY` sorts the final output.

**Notice: only 10 rows came back, but the `orders` table has 12.** Which two are missing? Order **107** (customer 99, who does not exist) and order **108** (customer NULL). Neither can be matched to any customer, so the inner join drops them **silently**, with no error and no warning. This is one of the most important facts about inner joins and we will return to it in the QA section.

### 4. Table aliases: making queries readable

Typing `orders.` and `customers.` repeatedly is tiring. An **alias** gives a table a short temporary nickname, defined right after its name (`AS` is optional but clearer):

```sql
SELECT o.order_id,
       c.full_name      AS customer,
       o.status,
       o.total_amount   AS total
FROM orders AS o
INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
ORDER BY o.total_amount DESC;
```

**Result:**

```text
order_id | customer      | status    | total
---------+---------------+-----------+-------
101      | Alice Johnson | completed | 1225.0
103      | Bob Smith     | completed | 150.0
110      | Bob Smith     | completed | 55.0
102      | Alice Johnson | completed | 30.48
111      | Carla Gomez   | completed | 19.99
112      | Grace Kim     | completed | 9.99
(6 rows)
```

Things to notice:

- `orders AS o` and `customers AS c` define the aliases; from then on you must use `o.` and `c.` (not the full table names).
- `c.full_name AS customer` is a **column alias**, renaming the output column header. Useful for readable reports and for test code that reads columns by name.
- `WHERE o.status = 'completed'` filters rows *after* matching. It works exactly like Thursday's `WHERE`.
- `ORDER BY o.total_amount DESC` sorts largest first.

#### Why qualify columns? The ambiguity error

Both `orders` and `customers` have a column named `customer_id`. If you write it without a prefix, the database cannot know which one you mean:

```sql
SELECT customer_id, full_name
FROM orders AS o
INNER JOIN customers AS c ON o.customer_id = c.customer_id;
```

**Result:**

```text
Error: ambiguous column name: customer_id
```

The error `ambiguous column name` is the database asking for clarification. Fix it by writing `c.customer_id` or `o.customer_id`. A good habit is to prefix **every** column in a join query, even when not required, so a future reader (or a future column added to a table) cannot break it.

### 5. What exactly is kept? A picture

Think of two circles (a Venn diagram): the left circle is the rows of the left table, the right circle the rows of the right table. The overlap is "rows that have a match on the other side".

```text
   orders only        matched         customers only
 (107, 108 here)   (10 orders)   (customers 6, 8, 9, 10)
 +--------------+--------------+--------------+
 |   dropped    |   KEPT       |   dropped    |
 +--------------+--------------+--------------+
```

An inner join keeps **only the overlap**. Rows only on one side vanish. We can check this from the other direction by counting how many distinct customers appear in the result:

```sql
SELECT COUNT(DISTINCT c.customer_id) AS customers_with_orders
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.customer_id;
```

**Result:**

```text
customers_with_orders
---------------------
6
(1 row)
```

Six customers have at least one order (customers 1, 2, 3, 4, 5, 7). The other four customers (6, 8, 9, 10) never appear in the join result, since none of their rows match.

### 6. NULL never matches

`NULL` means "unknown". Comparing NULL with anything, even another NULL, gives "unknown", not "true". That is why guest order 108 vanished: `NULL = anything` is never true. This also means an inner join cannot be used to find rows with missing keys. For that you need `LEFT JOIN ... WHERE ... IS NULL`, covered in the next lesson.

```sql
SELECT NULL = NULL AS null_equals_null, NULL IS NULL AS null_is_null;
```

**Result:**

```text
null_equals_null | null_is_null
-----------------+-------------
NULL             | 1
(1 row)
```

`NULL = NULL` produces NULL (shown as `NULL`), not 1 (true). `IS NULL` is the correct test and gives 1.

### 7. Row multiplication: one row matching many

If one row on the left matches several rows on the right, the left row appears several times in the result: once per match. Let us join customers and orders:

```sql
SELECT c.customer_id, c.full_name, o.order_id
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.customer_id
WHERE c.customer_id IN (1, 2, 3)
ORDER BY c.customer_id, o.order_id;
```

**Result:**

```text
customer_id | full_name     | order_id
------------+---------------+---------
1           | Alice Johnson | 101
1           | Alice Johnson | 102
2           | Bob Smith     | 103
2           | Bob Smith     | 110
3           | Carla Gomez   | 104
3           | Carla Gomez   | 111
(6 rows)
```

Alice has two orders so she appears twice; Bob (customer 2) has orders 103 and 110; Carla has 104 and 111. This is correct and expected: one customer to many orders. But it is also the reason **counts and sums can go wrong** after a join if you are not careful. For instance, joining `orders` to `order_items` repeats each order once per item:

```sql
SELECT o.order_id, o.total_amount, i.item_id, i.product_id, i.quantity
FROM orders AS o
INNER JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.order_id IN (101, 103)
ORDER BY o.order_id, i.item_id;
```

**Result:**

```text
order_id | total_amount | item_id | product_id | quantity
---------+--------------+---------+------------+---------
101      | 1225.0       | 1       | 1          | 1
101      | 1225.0       | 2       | 2          | 1
103      | 150.0        | 5       | 4          | 1
103      | 150.0        | 13      | 4          | 1
(4 rows)
```

Order 101 appears twice (two items), and order 103 appears twice because of the planted duplicate item row (items 5 and 13). If you now `SUM(o.total_amount)` over this result you would count the order total twice, an error that causes many wrong reports. Remember: **after a join to a "many" side, each parent row is repeated.**

### 8. Joining on more than two tables

You can chain joins. Each `INNER JOIN` adds one more table, and each needs its own `ON`. Let us list each order line with the customer name and product name:

```sql
SELECT o.order_id,
       c.full_name,
       p.product_name,
       i.quantity,
       i.unit_price
FROM orders       AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
INNER JOIN products    AS p ON p.product_id  = i.product_id
WHERE o.order_id <= 104
ORDER BY o.order_id, i.item_id;
```

**Result:**

```text
order_id | full_name     | product_name   | quantity | unit_price
---------+---------------+----------------+----------+-----------
101      | Alice Johnson | Laptop Pro     | 1        | 1200.0
101      | Alice Johnson | Wireless Mouse | 1        | 25.0
102      | Alice Johnson | USB-C Cable    | 2        | 9.99
102      | Alice Johnson | Notebook       | 3        | 3.5
103      | Bob Smith     | Desk Chair     | 1        | 150.0
103      | Bob Smith     | Desk Chair     | 1        | 150.0
104      | Carla Gomez   | Monitor 27in   | 2        | 300.0
(7 rows)
```

How to read this: start with `orders`; attach the customer for each order; attach each item for each order; attach the product for each item. Each join is another link in the chain from customers to products. (The "Multi-table queries" lesson goes deeper on designing such chains.)

### 9. Joining with extra conditions, and other join styles

You can add more conditions to `ON` using `AND`. Typically, though, put filters on the final result in `WHERE`. For an inner join the two are equivalent, but the difference matters with outer joins (next lesson).

```sql
SELECT p.product_name, d.title, d.severity
FROM products AS p
INNER JOIN defects AS d
        ON d.product_id = p.product_id AND d.status = 'open'
ORDER BY p.product_id;
```

**Result:**

```text
product_name | title                           | severity
-------------+---------------------------------+---------
Laptop Pro   | Laptop price rounds incorrectly | high
USB-C Cable  | Cable image missing             | low
Desk Chair   | Chair colour option missing     | medium
(3 rows)
```

This lists open defects with their product. Defect 3 (NULL product) is not shown, nor are products without open defects.

**Older syntax you may meet in legacy code:**

```sql
SELECT o.order_id, c.full_name
FROM orders o, customers c
WHERE o.customer_id = c.customer_id
ORDER BY o.order_id
LIMIT 3;
```

**Result:**

```text
order_id | full_name
---------+--------------
101      | Alice Johnson
102      | Alice Johnson
103      | Bob Smith
(3 rows)
```

A comma between tables plus a `WHERE` condition is the old "implicit join". It produces the same result as `INNER JOIN` but is easy to get wrong (forget the `WHERE` and you get a cross join), so modern style uses explicit `JOIN ... ON`.

**`USING`:** if the key has the same name in both tables you may write `USING (customer_id)` instead of `ON`. It is supported by SQLite, MySQL and PostgreSQL (SQL Server does not support it), so many teams stick with `ON`.

```sql
SELECT order_id, full_name, status
FROM orders
INNER JOIN customers USING (customer_id)
WHERE order_id < 103;
```

**Result:**

```text
order_id | full_name     | status
---------+---------------+----------
101      | Alice Johnson | completed
102      | Alice Johnson | completed
(2 rows)
```

### 10. Self-check: ON vs WHERE

- `ON` says **how rows match**.
- `WHERE` says **which result rows to keep**.

If you put the matching condition in `WHERE` with a cross join it still works, but mixing the two roles makes queries harder to read. Keep each in its role.

### 11. Real-world QA scenarios

**Scenario 1: verifying an order screen.** A UI test opens order 104 and reads the customer name "Carla Gomez". The database check:

```sql
SELECT c.full_name
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.order_id = 104;
```

**Result:**

```text
full_name
-----------
Carla Gomez
(1 row)
```

Your test asserts the UI value equals this value.

**Scenario 2: the silent-drop trap.** A tester writes "the number of completed orders should equal the number of completed orders joined to customers":

```sql
SELECT
  (SELECT COUNT(*) FROM orders WHERE status = 'completed') AS completed_orders,
  (SELECT COUNT(*)
     FROM orders AS o
     INNER JOIN customers AS c ON c.customer_id = o.customer_id
     WHERE o.status = 'completed')                         AS completed_with_customer;
```

**Result:**

```text
completed_orders | completed_with_customer
-----------------+------------------------
8                | 6
(1 row)
```

There are 8 completed orders, but only 6 of them match a customer. The inner join *quietly* removed orders 107 and 108. If a report is built with an inner join, those orders vanish from the revenue figure, and nobody gets an error message. A good validation always compares counts **before and after** the join.

**Scenario 3: price audit.** Which order lines were sold at a price different from the current product price?

```sql
SELECT i.item_id, p.product_name, i.unit_price AS sold_price, p.unit_price AS list_price
FROM order_items AS i
INNER JOIN products AS p ON p.product_id = i.product_id
WHERE i.unit_price <> p.unit_price;
```

**Result:**

```text
item_id | product_name | sold_price | list_price
--------+--------------+------------+-----------
(0 rows)
```

No rows mean all matched items were sold at list price. Item 15 (product 999) was not even checked because it matches no product, which, again, is invisible to the inner join.

### 12. Dialect notes

`INNER JOIN` behaves identically in SQLite, MySQL, PostgreSQL, SQL Server and Oracle. Differences exist in the *optional* features: `USING` is not in SQL Server, and string quoting and `LIMIT` vs `TOP` vary. How the database physically executes a join (and how to make it fast) is a performance topic we will cover in a later week.

### 13. Common mistakes

1. Forgetting the `ON` condition, producing a cross join.
2. Joining on the wrong columns (for example `o.order_id = c.customer_id`). This runs without error and returns wrong, confusing rows.
3. Not qualifying columns that exist in both tables.
4. Assuming an inner join keeps all rows from the first table.
5. Summing or counting after a join without thinking about row multiplication.
6. Expecting a join on NULL keys to match.

## Practice Questions

**Q1.** List each payment with the customer name who made it (join `payments`, `orders`, `customers`). How many rows come back, and why fewer than the 11 payments?

**Q2.** Show the product name and total quantity ever ordered for each product that appears on order lines (hint: join `order_items` and `products`, use `GROUP BY`; you will learn `GROUP BY` fully later today).

**Q3.** Which customers have an order with status `pending`? Show name and order ID.

**Q4.** A colleague wrote `SELECT * FROM customers JOIN orders;` and got 120 rows. What mistake did they make and what is the correct query?

**Q5.** Why does order 108 never show up in any inner join with `customers`, and how many customers rows would you need to add to make it match?

### Answers

**A1.**

```sql
SELECT pay.payment_id, c.full_name, pay.amount, pay.status
FROM payments AS pay
INNER JOIN orders    AS o ON o.order_id    = pay.order_id
INNER JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY pay.payment_id;
```

**Result:**

```text
payment_id | full_name     | amount | status
-----------+---------------+--------+---------
1          | Alice Johnson | 1225.0 | paid
2          | Alice Johnson | 30.48  | paid
3          | Bob Smith     | 150.0  | paid
4          | Carla Gomez   | 600.0  | paid
5          | Eve Muller    | 1200.0 | refunded
8          | Bob Smith     | 55.0   | paid
9          | Carla Gomez   | 19.99  | paid
11         | Alice Johnson | 30.48  | paid
(8 rows)
```

Eight rows. Payment 10 (order 888 does not exist) is dropped by the first join; payments 6 and 7 are dropped by the second join (order 107 has customer 99, order 108 has a NULL customer).

**A2.**

```sql
SELECT p.product_name, SUM(i.quantity) AS total_qty
FROM order_items AS i
INNER JOIN products AS p ON p.product_id = i.product_id
GROUP BY p.product_name
ORDER BY total_qty DESC;
```

**Result:**

```text
product_name   | total_qty
---------------+----------
Notebook       | 13
Wireless Mouse | 5
USB-C Cable    | 3
Monitor 27in   | 2
Laptop Pro     | 2
Desk Chair     | 2
(6 rows)
```

**A3.**

```sql
SELECT c.full_name, o.order_id
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.status = 'pending';
```

**Result:**

```text
full_name | order_id
----------+---------
Dev Patel | 105
Grace Kim | 109
(2 rows)
```

**A4.** They omitted `ON`, so SQLite produced a Cartesian product: 10 customers x 12 orders = 120 rows. Correct: `SELECT * FROM customers c JOIN orders o ON o.customer_id = c.customer_id;` (returns the 10 matched pairs).

**A5.** Its `customer_id` is NULL, and NULL never equals anything, so no customer can match, not even a new one. To make it join you would need to set a real `customer_id` on the order.

## Summary / Key Takeaways

- Data is split across tables to avoid repetition; **joins** reconnect it at query time.
- `INNER JOIN ... ON a.key = b.key` returns only the rows that have a match on both sides.
- Unmatched rows and rows whose key is NULL are silently dropped.
- Use table aliases and qualify every column to avoid ambiguity errors.
- One-to-many joins repeat the "one" side; be careful when summing or counting afterwards.
- A missing or wrong `ON` gives a Cartesian product or nonsense results.
- Inner joins can **hide** orphans and missing data; validate by comparing counts before and after joining.
- Next: `LEFT` and `RIGHT JOIN` keep unmatched rows, which is how we *find* the orphans.

## Additional Resources

- SQLite documentation, SELECT (the JOIN clause): https://www.sqlite.org/lang_select.html
- PostgreSQL documentation, Joins Between Tables: https://www.postgresql.org/docs/current/tutorial-join.html
- MySQL Reference Manual, JOIN clause: https://dev.mysql.com/doc/refman/8.0/en/join.html
