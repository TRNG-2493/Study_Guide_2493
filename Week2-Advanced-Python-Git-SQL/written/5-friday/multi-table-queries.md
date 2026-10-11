# Multi-Table Queries

## Learning Objectives

By the end of this lesson you will be able to:

- Read a schema diagram and find the **join path** between two tables that are not directly related.
- Build a query across three, four or five tables **incrementally**, checking row counts at each step.
- Mix `INNER JOIN` and `LEFT JOIN` in one query and predict the effect of their order.
- Recognise and fix **fan-out** (row multiplication) when joining two "many" tables to the same parent.
- Combine joins with `GROUP BY` and aggregates to build multi-table reports.
- Use a **self join** (a table joined to itself) to compare rows within the same table.
- Apply multi-table queries to realistic QA checks such as "an order must agree with its customer, items, products and payments".

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

This week's epic is "use SQL for QA data validation", and your Project 1 "QE Foundations" capstone needs validation queries that span the whole data model. Real business rules rarely involve just two tables:

- "The customer's name on the invoice must match the customer record, the product names must match the catalogue, and the amount charged must match the payment." That is **four or five tables** in one assertion.
- "Which products with open defects were sold to which customers?" crosses `defects`, `products`, `order_items`, `orders` and `customers`.

You already know how to join two tables. Today's skill is *scaling that up safely*: finding the path, adding tables one at a time, controlling what disappears, and not accidentally inflating your numbers. These are the skills that turn simple SQL knowledge into reliable test automation.

## The Concept

### 1. Reading the map: the join path

Our practice database as a map (arrows point from the child's foreign key to the parent's primary key):

```text
 customers <---- orders <---- order_items ----> products <---- defects
                    ^
                    |
                 payments
```

To connect two tables that are not directly linked, **walk the arrows** between them. Examples:

| You want to connect... | Join path |
|---|---|
| customers and products | customers -> orders -> order_items -> products |
| customers and payments | customers -> orders -> payments |
| defects and customers | defects -> products -> order_items -> orders -> customers |
| payments and products | payments -> orders -> order_items -> products |

Each arrow in the path becomes one `JOIN ... ON child.fk = parent.pk`. Five tables means four joins. Always join along real foreign key relationships; joining unrelated columns (for example `payments.amount = products.unit_price`) runs but produces coincidental, meaningless matches.

`order_items` is also a **bridge table** (or *junction table*): an order can contain many products and a product can appear on many orders (a many-to-many relationship), and `order_items` records each pairing with its quantity and price.

### 2. Build incrementally and count rows at each step

The professional way to write a big query is **one join at a time**, checking the result after each step. This turns a scary query into several small, verifiable steps and instantly reveals the step where rows disappear or multiply.

**Step 0: the base table.**

```sql
SELECT COUNT(*) AS rows_now FROM orders;
```

**Result:**

```text
rows_now
--------
12
(1 row)
```

**Step 1: add customers (INNER JOIN).**

```sql
SELECT COUNT(*) AS rows_now
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id;
```

**Result:**

```text
rows_now
--------
10
(1 row)
```

12 became 10: orders 107 and 108 dropped out. You learned this in the INNER JOIN lesson, and now you see it as a measurable step.

**Step 2: add order items.**

```sql
SELECT COUNT(*) AS rows_now
FROM orders AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id;
```

**Result:**

```text
rows_now
--------
13
(1 row)
```

The count went *up* to 13 even though we are joining more tables: orders with several items repeat (101, 102, 103 and 105 have two item rows each). Order 109 (no items) vanished.

**Step 3: add products.**

```sql
SELECT COUNT(*) AS rows_now
FROM orders AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
INNER JOIN products    AS p ON p.product_id  = i.product_id;
```

**Result:**

```text
rows_now
--------
12
(1 row)
```

One more row dropped: item 15 (product 999 does not exist, belonging to order 111). Now we have the full "order detail" report:

```sql
SELECT o.order_id,
       c.full_name         AS customer,
       p.product_name      AS product,
       i.quantity,
       i.unit_price,
       i.quantity * i.unit_price AS line_total
FROM orders AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
INNER JOIN products    AS p ON p.product_id  = i.product_id
ORDER BY o.order_id, i.item_id;
```

**Result:**

```text
order_id | customer      | product        | quantity | unit_price | line_total
---------+---------------+----------------+----------+------------+-----------
101      | Alice Johnson | Laptop Pro     | 1        | 1200.0     | 1200.0
101      | Alice Johnson | Wireless Mouse | 1        | 25.0       | 25.0
102      | Alice Johnson | USB-C Cable    | 2        | 9.99       | 19.98
102      | Alice Johnson | Notebook       | 3        | 3.5        | 10.5
103      | Bob Smith     | Desk Chair     | 1        | 150.0      | 150.0
103      | Bob Smith     | Desk Chair     | 1        | 150.0      | 150.0
104      | Carla Gomez   | Monitor 27in   | 2        | 300.0      | 600.0
105      | Dev Patel     | Wireless Mouse | 1        | 25.0       | 25.0
105      | Dev Patel     | USB-C Cable    | 1        | 9.99       | 9.99
106      | Eve Muller    | Laptop Pro     | 1        | 1200.0     | 1200.0
110      | Bob Smith     | Wireless Mouse | 2        | 25.0       | 50.0
112      | Grace Kim     | USB-C Cable    | -1       | 9.99       | -9.99
(12 rows)
```

By following the counts (12 -> 10 -> 13 -> 12) you can *explain every row* in the final result and every row that is absent. When a test fails because "the report is missing orders", this technique finds the exact join that dropped them.

### 3. Mixing INNER and LEFT joins

When some relationships are optional, use `LEFT JOIN` for them. The rule of thumb: **start from the table you want to keep in full, and use LEFT JOIN for optional children or parents.**

Suppose we want every order, with the customer name if any (a guest or orphan order should still be listed), and the number of items:

```sql
SELECT o.order_id,
       COALESCE(c.full_name, '(no customer)') AS customer,
       o.status,
       COUNT(i.item_id)  AS item_rows
FROM orders AS o
LEFT JOIN customers   AS c ON c.customer_id = o.customer_id
LEFT JOIN order_items AS i ON i.order_id    = o.order_id
GROUP BY o.order_id, c.full_name, o.status
ORDER BY o.order_id;
```

**Result:**

```text
order_id | customer      | status    | item_rows
---------+---------------+-----------+----------
101      | Alice Johnson | completed | 2
102      | Alice Johnson | completed | 2
103      | Bob Smith     | completed | 2
104      | Carla Gomez   | shipped   | 1
105      | Dev Patel     | pending   | 2
106      | Eve Muller    | cancelled | 1
107      | (no customer) | completed | 1
108      | (no customer) | completed | 1
109      | Grace Kim     | pending   | 0
110      | Bob Smith     | completed | 1
111      | Carla Gomez   | completed | 1
112      | Grace Kim     | completed | 1
(12 rows)
```

All 12 orders are present. Orders 107 and 108 show `(no customer)`, and order 109 shows `0` item rows (we used `COUNT(i.item_id)`, not `COUNT(*)`).

#### The danger of an INNER JOIN after a LEFT JOIN

Join order matters. Compare these two queries; the only difference is the type of the *second* join:

```sql
SELECT o.order_id, c.full_name, i.item_id
FROM orders AS o
LEFT JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
WHERE o.order_id IN (107, 108, 109);
```

**Result:**

```text
order_id | full_name | item_id
---------+-----------+--------
107      | NULL      | 10
108      | NULL      | 11
(2 rows)
```

Order 109 vanished. We *meant* to keep every order via the `LEFT JOIN`, but the later `INNER JOIN order_items` removed order 109 because it has no items. An inner join anywhere in the chain can cancel the protection that earlier left joins gave you. Rule: **once you start with LEFT JOINs to keep unmatched rows, continue with LEFT JOINs for the rest of the chain** (unless you deliberately want to drop rows).

```sql
SELECT o.order_id, c.full_name, i.item_id
FROM orders AS o
LEFT JOIN customers   AS c ON c.customer_id = o.customer_id
LEFT JOIN order_items AS i ON i.order_id    = o.order_id
WHERE o.order_id IN (107, 108, 109);
```

**Result:**

```text
order_id | full_name | item_id
---------+-----------+--------
107      | NULL      | 10
108      | NULL      | 11
109      | Grace Kim | NULL
(3 rows)
```

Now all three survive, with NULLs where there is no partner.

### 4. The fan-out trap: two "many" tables on the same parent

A *fan-out* is row multiplication caused by joining **two independent one-to-many tables** to the same parent. Consider order 102. It has 2 item rows and (because of the planted double payment) 2 payment rows. If we join both children to the order:

```sql
SELECT o.order_id, i.item_id, pay.payment_id
FROM orders AS o
INNER JOIN order_items AS i   ON i.order_id   = o.order_id
INNER JOIN payments    AS pay ON pay.order_id = o.order_id
WHERE o.order_id = 102
ORDER BY i.item_id, pay.payment_id;
```

**Result:**

```text
order_id | item_id | payment_id
---------+---------+-----------
102      | 3       | 2
102      | 3       | 11
102      | 4       | 2
102      | 4       | 11
(4 rows)
```

2 items x 2 payments = **4 rows**. Each item is paired with each payment, though they are unrelated. If you now sum the payment amount, the order's payments are counted once per item:

```sql
SELECT o.order_id,
       SUM(pay.amount) AS payments_total_wrong,
       SUM(i.quantity * i.unit_price) AS items_total_wrong
FROM orders AS o
INNER JOIN order_items AS i   ON i.order_id   = o.order_id
INNER JOIN payments    AS pay ON pay.order_id = o.order_id
WHERE o.order_id = 102
GROUP BY o.order_id;
```

**Result:**

```text
order_id | payments_total_wrong | items_total_wrong
---------+----------------------+------------------
102      | 121.92               | 60.96
(1 row)
```

The true payments total is 60.96 (two rows of 30.48) and items total is 30.48; the result shows both figures doubled, because every row is repeated twice. **Fix: aggregate each child table separately first (as a subquery), then join the one-row-per-order results.**

```sql
SELECT o.order_id,
       o.total_amount        AS header_total,
       it.items_total,
       pa.paid_total
FROM orders AS o
LEFT JOIN (SELECT order_id, SUM(quantity * unit_price) AS items_total
           FROM order_items GROUP BY order_id) AS it ON it.order_id = o.order_id
LEFT JOIN (SELECT order_id, SUM(amount) AS paid_total
           FROM payments WHERE status = 'paid' GROUP BY order_id) AS pa ON pa.order_id = o.order_id
ORDER BY o.order_id;
```

**Result:**

```text
order_id | header_total | items_total | paid_total
---------+--------------+-------------+-----------
101      | 1225.0       | 1225.0      | 1225.0
102      | 30.48        | 30.48       | 60.96
103      | 150.0        | 300.0       | 150.0
104      | 600.0        | 600.0       | 600.0
105      | 34.99        | 34.99       | NULL
106      | 1200.0       | 1200.0      | NULL
107      | 35.0         | 35.0        | 35.0
108      | 9.99         | 9.99        | 9.99
109      | 80.0         | NULL        | NULL
110      | 55.0         | 50.0        | 55.0
111      | 19.99        | 19.99       | 19.99
112      | 9.99         | -9.99       | NULL
(12 rows)
```

Each derived table has exactly one row per order, so no multiplication can happen. Now each order shows its header total, the recomputed items total and the paid total side by side. Reading it row by row:

- **101, 104:** header, items and paid all agree.
- **102:** items 30.48 but paid 60.96, the double payment.
- **103:** header 150, items 300 (the duplicate item row).
- **105:** items match the header, no payment (pending, probably fine).
- **106:** items match, no `paid` payment because it was refunded (cancelled order).
- **107 and 108:** the numbers are internally consistent, but the customer is missing (found by other checks).
- **109:** header 80 but no items.
- **110:** header 55, items 50, paid 55.
- **111:** all three agree, but the item's product does not exist.
- **112:** negative items total, no payment.

This single table is a miniature **order integrity report**, built from four tables. You will use similar queries in the validation lesson and in your Project 1 work.

### 5. Multi-table aggregation reports

**Revenue per customer, per product category** (customers -> orders -> items -> products):

```sql
SELECT c.full_name,
       p.category,
       SUM(i.quantity * i.unit_price) AS revenue
FROM customers   AS c
INNER JOIN orders      AS o ON o.customer_id = c.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
INNER JOIN products    AS p ON p.product_id  = i.product_id
WHERE o.status <> 'cancelled'
GROUP BY c.customer_id, c.full_name, p.category
ORDER BY c.full_name, p.category;
```

**Result:**

```text
full_name     | category    | revenue
--------------+-------------+--------
Alice Johnson | Accessories | 19.98
Alice Johnson | Electronics | 1225.0
Alice Johnson | Stationery  | 10.5
Bob Smith     | Electronics | 50.0
Bob Smith     | Furniture   | 300.0
Carla Gomez   | Electronics | 600.0
Dev Patel     | Accessories | 9.99
Dev Patel     | Electronics | 25.0
Grace Kim     | Accessories | -9.99
(9 rows)
```

Cancelled orders are excluded with a `WHERE` condition on `orders`. Because we group by the customer's `customer_id` and name, the two "Bob Smith" rows are not merged (customer 8 has no orders anyway).

**Products with open defects, and who bought them** (five tables!):

```sql
SELECT d.defect_id, d.title, d.severity,
       p.product_name,
       o.order_id, c.full_name
FROM defects AS d
INNER JOIN products    AS p ON p.product_id  = d.product_id
INNER JOIN order_items AS i ON i.product_id  = p.product_id
INNER JOIN orders      AS o ON o.order_id    = i.order_id
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
WHERE d.status = 'open'
ORDER BY d.defect_id, o.order_id;
```

**Result:**

```text
defect_id | title                           | severity | product_name | order_id | full_name
----------+---------------------------------+----------+--------------+----------+--------------
1         | Laptop price rounds incorrectly | high     | Laptop Pro   | 101      | Alice Johnson
1         | Laptop price rounds incorrectly | high     | Laptop Pro   | 106      | Eve Muller
4         | Cable image missing             | low      | USB-C Cable  | 102      | Alice Johnson
4         | Cable image missing             | low      | USB-C Cable  | 105      | Dev Patel
4         | Cable image missing             | low      | USB-C Cable  | 112      | Grace Kim
6         | Chair colour option missing     | medium   | Desk Chair   | 103      | Bob Smith
6         | Chair colour option missing     | medium   | Desk Chair   | 103      | Bob Smith
(7 rows)
```

This answers a real triage question: "who is impacted by each open defect?" The defect for the desk chair (defect 6) lists Bob Smith twice because of the duplicated item row; the USB-C Cable defect lists the orders that include cables. Defect 3 (no product) cannot be connected to any customer and is absent.

### 6. Self joins: a table joined to itself

A **self join** joins a table to *another copy of itself*, using two different aliases. It is how you compare rows within one table, for example finding duplicates, or employees and their managers.

**Finding customer pairs with the same email:**

```sql
SELECT a.customer_id AS id_a, b.customer_id AS id_b, a.full_name, a.email
FROM customers AS a
INNER JOIN customers AS b
        ON a.email = b.email
       AND a.customer_id < b.customer_id
ORDER BY a.customer_id;
```

**Result:**

```text
id_a | id_b | full_name | email
-----+------+-----------+----------------
2    | 8    | Bob Smith | bob@example.com
(1 row)
```

Why `a.customer_id < b.customer_id`? Without it, every row would also match *itself* (a with a), and each pair would appear twice (a with b, then b with a). The `<` condition keeps each pair once and removes self-pairs. This is another way to detect duplicates besides `GROUP BY ... HAVING`. Notice customer 6 (NULL email) is not matched at all, because `NULL = NULL` is not true.

**Orders placed by the same customer on later dates than another order** (pairs of orders by one customer, earlier then later):

```sql
SELECT o1.customer_id, o1.order_id AS earlier_order, o2.order_id AS later_order,
       o1.order_date, o2.order_date AS later_date
FROM orders AS o1
INNER JOIN orders AS o2
        ON o1.customer_id = o2.customer_id
       AND o1.order_date < o2.order_date
ORDER BY o1.customer_id, o1.order_date;
```

**Result:**

```text
customer_id | earlier_order | later_order | order_date | later_date
------------+---------------+-------------+------------+-----------
1           | 101           | 102         | 2025-06-01 | 2025-06-15
2           | 103           | 110         | 2025-06-20 | 2025-07-20
3           | 104           | 111         | 2025-07-02 | 2025-07-22
7           | 109           | 112         | 2025-07-18 | 2025-07-25
(4 rows)
```

### 7. Real-world QA scenario: the "order integrity" validation

Combine what you learned: list every order that has *any* problem, with a plain-language reason. We use `LEFT JOIN`s to the one-row-per-order summaries from section 4, so no fan-out occurs:

```sql
SELECT o.order_id,
       CASE
         WHEN c.customer_id IS NULL AND o.customer_id IS NOT NULL THEN 'customer does not exist'
         WHEN o.customer_id IS NULL                              THEN 'no customer on order'
         WHEN it.items_total IS NULL                             THEN 'order has no items'
         WHEN ROUND(it.items_total,2) <> ROUND(o.total_amount,2) THEN 'header total differs from items'
         WHEN o.status = 'completed' AND pa.paid_total IS NULL   THEN 'completed but unpaid'
         ELSE 'ok'
       END AS finding,
       o.total_amount, it.items_total, pa.paid_total
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
LEFT JOIN (SELECT order_id, SUM(quantity * unit_price) AS items_total
           FROM order_items GROUP BY order_id) AS it ON it.order_id = o.order_id
LEFT JOIN (SELECT order_id, SUM(amount) AS paid_total
           FROM payments WHERE status = 'paid' GROUP BY order_id) AS pa ON pa.order_id = o.order_id
ORDER BY o.order_id;
```

**Result:**

```text
order_id | finding                         | total_amount | items_total | paid_total
---------+---------------------------------+--------------+-------------+-----------
101      | ok                              | 1225.0       | 1225.0      | 1225.0
102      | ok                              | 30.48        | 30.48       | 60.96
103      | header total differs from items | 150.0        | 300.0       | 150.0
104      | ok                              | 600.0        | 600.0       | 600.0
105      | ok                              | 34.99        | 34.99       | NULL
106      | ok                              | 1200.0       | 1200.0      | NULL
107      | customer does not exist         | 35.0         | 35.0        | 35.0
108      | no customer on order            | 9.99         | 9.99        | 9.99
109      | order has no items              | 80.0         | NULL        | NULL
110      | header total differs from items | 55.0         | 50.0        | 55.0
111      | ok                              | 19.99        | 19.99       | 19.99
112      | header total differs from items | 9.99         | -9.99       | NULL
(12 rows)
```

The `CASE` returns the first matching reason for each order, so order matters: the most fundamental problem is listed first. Read the `finding` column in the result: orders 101, 104, 111 and others show `ok` as far as these rules go. (Note that the double payment on order 102 is *not* caught by this query because we only test for a missing payment; "paid more than the total" would be another `WHEN`. Validation rules are only as good as the rules you write.)

### 8. Tips for writing and debugging multi-table queries

1. **Draw the join path first**, then write the query.
2. **Add one table at a time** and check the row count and a few rows.
3. **Alias every table** with a short consistent name (`c`, `o`, `i`, `p`, `pay`) and qualify every column.
4. **Name the key you test** for NULL in anti-joins: the primary key of the table that might be missing.
5. **Beware fan-out** whenever two one-to-many tables hang off the same parent; pre-aggregate in subqueries.
6. **Use LEFT JOIN chains** when you need to keep the base rows; mix in INNER JOIN only on purpose.
7. **Write the expected row count** before running the query. A mismatch means a misunderstanding of the data, or a bug.
8. **Keep it readable**: one join per line, `ON` aligned, short comments for tricky logic.

Performance of large multi-table queries (indexes, execution plans) will be covered in a later week; for now, correctness is the goal.

### 9. Common mistakes

1. Joining two child tables to the same parent and summing (fan-out).
2. Following an early `LEFT JOIN` with an `INNER JOIN` that removes the preserved rows.
3. Joining along a wrong or non-key column.
4. Forgetting a join condition between one of the tables (accidental Cartesian product).
5. Selecting `*` from many tables and ending up with duplicate column names (use explicit columns).
6. Grouping by a non-unique column such as a name.

## Practice Questions

**Q1.** List, for every *completed* order that has items, the customer name and the number of distinct products on the order.

**Q2.** For each customer who has at least one order item, show total quantity of items bought (customers -> orders -> order_items). Which customer bought the most units?

**Q3.** Using a self join on `customers`, list pairs of customers from the same country (each pair once).

**Q4.** Why would `SELECT SUM(pay.amount) FROM orders o JOIN order_items i ON ... JOIN payments pay ON ...` give a wrong figure? How do you fix it?

**Q5.** Write a query listing all products together with the names of customers who bought them. Include products that nobody has bought.

### Answers

**A1.**

```sql
SELECT o.order_id, c.full_name, COUNT(DISTINCT i.product_id) AS distinct_products
FROM orders AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
WHERE o.status = 'completed'
GROUP BY o.order_id, c.full_name
ORDER BY o.order_id;
```

**Result:**

```text
order_id | full_name     | distinct_products
---------+---------------+------------------
101      | Alice Johnson | 2
102      | Alice Johnson | 2
103      | Bob Smith     | 1
110      | Bob Smith     | 1
111      | Carla Gomez   | 1
112      | Grace Kim     | 1
(6 rows)
```

Order 103 shows `1` distinct product even though it has two item rows, thanks to `DISTINCT` (the duplicate row is for the same product).

**A2.**

```sql
SELECT c.customer_id, c.full_name, SUM(i.quantity) AS units
FROM customers AS c
INNER JOIN orders      AS o ON o.customer_id = c.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
GROUP BY c.customer_id, c.full_name
ORDER BY units DESC;
```

**Result:**

```text
customer_id | full_name     | units
------------+---------------+------
1           | Alice Johnson | 7
2           | Bob Smith     | 4
3           | Carla Gomez   | 3
4           | Dev Patel     | 2
5           | Eve Muller    | 1
7           | Grace Kim     | -1
(6 rows)
```

Alice bought the most (7 units). Grace Kim shows `-1` because her only item line is the negative-quantity bug (item 16), an invalid value that a plain list hides but an aggregate exposes.

**A3.**

```sql
SELECT a.full_name AS customer_a, b.full_name AS customer_b, a.country
FROM customers AS a
INNER JOIN customers AS b
        ON a.country = b.country AND a.customer_id < b.customer_id
ORDER BY a.country, a.customer_id, b.customer_id;
```

**Result:**

```text
customer_a    | customer_b | country
--------------+------------+--------
Alice Johnson | Bob Smith  | US
Alice Johnson | Grace Kim  | US
Alice Johnson | Bob Smith  | US
Bob Smith     | Grace Kim  | US
Bob Smith     | Bob Smith  | US
Grace Kim     | Bob Smith  | US
(6 rows)
```

**A4.** Joining both `order_items` and `payments` to `orders` multiplies each payment by the number of item rows for that order (fan-out), so the payment sum is inflated. Fix by aggregating payments in a subquery (one row per order) and joining that, or by summing payments in a query that does not join to `order_items`.

**A5.**

```sql
SELECT p.product_name, c.full_name
FROM products AS p
LEFT JOIN order_items AS i ON i.product_id = p.product_id
LEFT JOIN orders      AS o ON o.order_id   = i.order_id
LEFT JOIN customers   AS c ON c.customer_id = o.customer_id
ORDER BY p.product_id, c.full_name;
```

**Result:**

```text
product_name   | full_name
---------------+--------------
Laptop Pro     | Alice Johnson
Laptop Pro     | Eve Muller
Wireless Mouse | NULL
Wireless Mouse | Alice Johnson
Wireless Mouse | Bob Smith
Wireless Mouse | Dev Patel
USB-C Cable    | NULL
USB-C Cable    | Alice Johnson
USB-C Cable    | Dev Patel
USB-C Cable    | Grace Kim
Desk Chair     | Bob Smith
Desk Chair     | Bob Smith
Notebook       | NULL
Notebook       | Alice Johnson
Monitor 27in   | Carla Gomez
Webcam HD      | NULL
Standing Desk  | NULL
(17 rows)
```

Products 7 (Webcam HD) and 8 (Standing Desk) appear with NULL customer names because nobody bought them. Every join after `products` is a `LEFT JOIN`, so unsold products are kept. Other NULL names have a different cause: the item belongs to an order whose customer is missing (orders 107 and 108) or to the orphan item 14 (order 999 does not exist). The same NULL can mean different problems, so investigate before drawing conclusions.

## Summary / Key Takeaways

- Find the **join path** by walking primary-key/foreign-key arrows; `n` tables need `n-1` joins.
- Build queries **incrementally** and count rows after each join to see exactly where rows vanish or multiply.
- Start with the table to preserve and use `LEFT JOIN` along the chain; a later `INNER JOIN` can silently cancel earlier left joins.
- **Fan-out**: two one-to-many tables joined to the same parent multiply rows and inflate sums; pre-aggregate each child in a subquery.
- A **self join** compares rows within one table using two aliases (and `a.id < b.id` to avoid self-pairs and mirror pairs).
- Multi-table queries are the backbone of data-integrity reports: header totals vs items vs payments, orphans, missing links.

## Additional Resources

- SQLite documentation, SELECT (join-clause details): https://www.sqlite.org/lang_select.html
- PostgreSQL documentation, Joins Between Tables (includes self joins): https://www.postgresql.org/docs/current/tutorial-join.html
- MySQL Reference Manual, Join Syntax: https://dev.mysql.com/doc/refman/8.0/en/join.html
