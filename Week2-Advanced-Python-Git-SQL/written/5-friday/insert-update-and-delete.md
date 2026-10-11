# INSERT, UPDATE and DELETE

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what DML (Data Manipulation Language) is and how it differs from the `SELECT` queries you wrote on Thursday.
- Add new rows to a table with `INSERT INTO ... VALUES`, including multi-row inserts and `INSERT ... SELECT`.
- Change existing rows safely with `UPDATE ... SET ... WHERE`, and explain why a missing `WHERE` clause is dangerous.
- Remove rows with `DELETE FROM ... WHERE`, and describe the difference between `DELETE`, `DROP TABLE` and "soft deletes".
- Use the "SELECT first, then change" habit and simple transactions (`BEGIN`, `ROLLBACK`, `COMMIT`) to protect data.
- Apply INSERT/UPDATE/DELETE to realistic QA tasks such as seeding, fixing and cleaning up test data.
- Read the practice database that we will use for every lesson today, including the deliberate data problems hidden inside it.

## Why This Matters

This week's epic is to harden your Python, add SQL for QA data validation, and start the Project 1 "QE Foundations" capstone. On Thursday you learned to *read* data: `SELECT`, `WHERE`, `ORDER BY`. A tester who can only read data is only half-equipped. Real test automation constantly needs to **change** data:

- **Test set-up:** before a test runs, you often need a known customer, a known product and a known order in the database so the test is repeatable.
- **Test tear-down:** after a test runs, you remove or reset the rows it created so the next run starts clean.
- **Reproducing bugs:** to reproduce a defect ("order total is wrong when quantity is negative"), you insert exactly the broken data that triggers it.
- **Environment hygiene:** test databases accumulate duplicates, half-finished records and stale rows that cause "flaky" failures.

Every one of those tasks uses three statements: `INSERT`, `UPDATE`, `DELETE`. They are powerful, and with power comes risk: an `UPDATE` without a `WHERE` clause changes *every row*; a careless `DELETE` can wipe a whole table. As a QA engineer you must be fluent and careful. This lesson also introduces the **practice database** used in all ten lessons today, so spend time on that section.

## The Concept

### 1. What is DML?

SQL statements fall into families:

| Family | Stands for | Purpose | Examples |
|---|---|---|---|
| DDL | Data **Definition** Language | Create or change the *structure* of the database | `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` |
| DML | Data **Manipulation** Language | Add, change or remove the *rows* inside tables | `INSERT`, `UPDATE`, `DELETE` |
| DQL | Data **Query** Language | Read data | `SELECT` |
| TCL | **Transaction** Control Language | Group changes so they succeed or fail together | `BEGIN`, `COMMIT`, `ROLLBACK` |

(Some books place `SELECT` under DML; the exact grouping is not important. What matters is that `SELECT` never changes data, while `INSERT`, `UPDATE`, `DELETE` always can.)

An analogy: a table is a paper spreadsheet in a filing cabinet. `SELECT` is *looking* at the sheet. `INSERT` writes a new line at the bottom. `UPDATE` crosses out and rewrites values in existing lines. `DELETE` rips lines out. Once a statement is committed there is usually no "undo" button, which is why we build safe habits below.

### 2. Our practice database: "QA Shop"

All ten lessons today use **one** small online-shop database. It has six tables:

| Table | What it stores | Key columns |
|---|---|---|
| `customers` | People who buy things | `customer_id` (PK), `full_name`, `email`, `country`, `created_date` |
| `products` | Things for sale | `product_id` (PK), `product_name`, `category`, `unit_price` |
| `orders` | One row per purchase | `order_id` (PK), `customer_id` (FK), `order_date`, `status`, `total_amount` |
| `order_items` | The lines inside an order | `item_id` (PK), `order_id` (FK), `product_id` (FK), `quantity`, `unit_price` |
| `payments` | Money received for orders | `payment_id` (PK), `order_id` (FK), `amount`, `method`, `status` |
| `defects` | Bugs QA has logged against products | `defect_id` (PK), `product_id` (FK, may be NULL), `title`, `severity`, `status`, `found_date` |

How they relate (`PK` = primary key, `FK` = foreign key; you will study these properly in the next lesson):

```text
customers 1 ──< orders 1 ──< order_items >── 1 products 1 ──< defects
                   │
                   └──< payments
```

Read `1 ──<` as "one-to-many": one customer can have many orders; one order can have many items; one product can appear in many order items.

#### The setup script

Save this as `qa_shop_setup.sql` and run it in the SQLite command line (`sqlite3 qa_shop.db < qa_shop_setup.sql`) or any SQLite tool. Everything we show in this lesson was run against exactly this script on SQLite 3.45. Read the `CREATE TABLE` statements slowly; you saw simple versions on Thursday.

```sql
CREATE TABLE customers (
    customer_id  INTEGER PRIMARY KEY,
    full_name    TEXT NOT NULL,
    email        TEXT,
    country      TEXT,
    created_date TEXT
);
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT,
    unit_price   REAL NOT NULL
);
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER,
    order_date   TEXT,
    status       TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE order_items (
    item_id    INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL,
    amount     REAL NOT NULL,
    method     TEXT,
    status     TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
CREATE TABLE defects (
    defect_id  INTEGER PRIMARY KEY,
    product_id INTEGER,
    title      TEXT NOT NULL,
    severity   TEXT,
    status     TEXT,
    found_date TEXT,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO customers VALUES
 (1,'Alice Johnson','alice@example.com','US','2025-01-10'),
 (2,'Bob Smith','bob@example.com','US','2025-01-15'),
 (3,'Carla Gomez','carla@example.com','MX','2025-02-01'),
 (4,'Dev Patel','dev@example.com','IN','2025-02-11'),
 (5,'Eve Muller','eve@example.com','DE','2025-03-05'),
 (6,'Frank Lee',NULL,'KR','2025-03-20'),
 (7,'Grace Kim','grace@example.com','US','2025-04-02'),
 (8,'Bob Smith','bob@example.com','US','2025-04-10'),
 (9,'Hana Sato','hana@example.com','JP','2025-05-01'),
 (10,'Ian Brooks','ian@example.com','GB','2025-05-09');

INSERT INTO products VALUES
 (1,'Laptop Pro','Electronics',1200.00),
 (2,'Wireless Mouse','Electronics',25.00),
 (3,'USB-C Cable','Accessories',9.99),
 (4,'Desk Chair','Furniture',150.00),
 (5,'Notebook','Stationery',3.50),
 (6,'Monitor 27in','Electronics',300.00),
 (7,'Webcam HD','Electronics',45.00),
 (8,'Standing Desk','Furniture',450.00);

INSERT INTO orders VALUES
 (101,1,'2025-06-01','completed',1225.00),
 (102,1,'2025-06-15','completed',30.48),
 (103,2,'2025-06-20','completed',150.00),
 (104,3,'2025-07-02','shipped',600.00),
 (105,4,'2025-07-05','pending',34.99),
 (106,5,'2025-07-09','cancelled',1200.00),
 (107,99,'2025-07-12','completed',35.00),
 (108,NULL,'2025-07-15','completed',9.99),
 (109,7,'2025-07-18','pending',80.00),
 (110,2,'2025-07-20','completed',55.00),
 (111,3,'2025-07-22','completed',19.99),
 (112,7,'2025-07-25','completed',9.99);

INSERT INTO order_items VALUES
 (1,101,1,1,1200.00),
 (2,101,2,1,25.00),
 (3,102,3,2,9.99),
 (4,102,5,3,3.50),
 (5,103,4,1,150.00),
 (6,104,6,2,300.00),
 (7,105,2,1,25.00),
 (8,105,3,1,9.99),
 (9,106,1,1,1200.00),
 (10,107,5,10,3.50),
 (11,108,3,1,9.99),
 (12,110,2,2,25.00),
 (13,103,4,1,150.00),
 (14,999,2,1,25.00),
 (15,111,999,1,19.99),
 (16,112,3,-1,9.99);

INSERT INTO payments VALUES
 (1,101,1225.00,'card','paid'),
 (2,102,30.48,'card','paid'),
 (3,103,150.00,'paypal','paid'),
 (4,104,600.00,'card','paid'),
 (5,106,1200.00,'card','refunded'),
 (6,107,35.00,'card','paid'),
 (7,108,9.99,'paypal','paid'),
 (8,110,55.00,'card','paid'),
 (9,111,19.99,'card','paid'),
 (10,888,10.00,'card','paid'),
 (11,102,30.48,'card','paid');

INSERT INTO defects VALUES
 (1,1,'Laptop price rounds incorrectly','high','open','2025-07-01'),
 (2,2,'Mouse shown out of stock wrongly','low','closed','2025-07-03'),
 (3,NULL,'Checkout page timeout','critical','open','2025-07-10'),
 (4,3,'Cable image missing','low','open','2025-07-11'),
 (5,6,'Monitor tax calculation wrong','high','closed','2025-07-14'),
 (6,4,'Chair colour option missing','medium','open','2025-07-16');
```

#### The deliberate data problems ("planted bugs")

Real test databases are messy, so ours is too. We planted problems on purpose so that joins and validation queries have something to find. Keep this table handy; we will return to it all day:

| # | Planted problem | Where |
|---|---|---|
| 1 | **Duplicate customer** (same name and email, different ID) | `customers` 2 and 8 |
| 2 | **NULL email** | `customers` 6 (Frank Lee) |
| 3 | **Customers who never ordered** | `customers` 6, 8, 9, 10 |
| 4 | **Orphan order** (customer 99 does not exist) | `orders` 107 |
| 5 | **Guest order** (customer is NULL) | `orders` 108 |
| 6 | **Order with no items** | `orders` 109 |
| 7 | **Order total does not match its items** | `orders` 103 (duplicate item row), 109 (no items), 110, 112 |
| 8 | **Duplicate item row** | `order_items` 5 and 13 (same order, same product, same price) |
| 9 | **Orphan order item** (order 999 does not exist) | `order_items` 14 |
| 10 | **Item pointing at a missing product** (product 999) | `order_items` 15 |
| 11 | **Negative quantity** | `order_items` 16 |
| 12 | **Orphan payment** (order 888 does not exist) | `payments` 10 |
| 13 | **Double payment** (same order, same amount, twice) | `payments` 2 and 11 |
| 14 | **Products never sold** | `products` 7, 8 |
| 15 | **Completed orders with no payment** | `orders` 109 (pending, fine), 112 (completed, suspicious) |
| 16 | **Defect with no product** (NULL product) | `defects` 3 |

Why would real data look like this? Typical causes include a bulk CSV import that bypassed checks, a bug in a checkout service, a test that crashed halfway and left rows behind, or a deleted parent record. QA engineers are often the people who discover such problems.

Let us look at two tables to make sure the data loaded correctly:

```sql
SELECT customer_id, full_name, email, country FROM customers;
```

**Result:**

```text
customer_id | full_name     | email             | country
------------+---------------+-------------------+--------
1           | Alice Johnson | alice@example.com | US
2           | Bob Smith     | bob@example.com   | US
3           | Carla Gomez   | carla@example.com | MX
4           | Dev Patel     | dev@example.com   | IN
5           | Eve Muller    | eve@example.com   | DE
6           | Frank Lee     | NULL              | KR
7           | Grace Kim     | grace@example.com | US
8           | Bob Smith     | bob@example.com   | US
9           | Hana Sato     | hana@example.com  | JP
10          | Ian Brooks    | ian@example.com   | GB
(10 rows)
```

```sql
SELECT order_id, customer_id, status, total_amount FROM orders;
```

**Result:**

```text
order_id | customer_id | status    | total_amount
---------+-------------+-----------+-------------
101      | 1           | completed | 1225.0
102      | 1           | completed | 30.48
103      | 2           | completed | 150.0
104      | 3           | shipped   | 600.0
105      | 4           | pending   | 34.99
106      | 5           | cancelled | 1200.0
107      | 99          | completed | 35.0
108      | NULL        | completed | 9.99
109      | 7           | pending   | 80.0
110      | 2           | completed | 55.0
111      | 3           | completed | 19.99
112      | 7           | completed | 9.99
(12 rows)
```

You will notice that in `orders`, order 108 has `customer_id` `NULL` and order 107 has customer `99`, which does not exist in the customers table. Neither is visible as a problem from `orders` alone. That is exactly why we will need joins.

### 3. INSERT: adding rows

#### Syntax

```text
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

- `INSERT INTO table_name` says where the new row goes.
- The parenthesised column list says *which columns* you are supplying.
- `VALUES (...)` supplies the values **in the same order** as the column list.

Always write the column list. Without it, SQL assumes you are providing *every* column in the table's defined order. That works until someone adds a column and your script breaks (or worse, silently puts values in the wrong columns).

#### Inserting one row

We want to add a new customer, Jordan Rivera from Canada:

```sql
INSERT INTO customers (customer_id, full_name, email, country, created_date)
VALUES (11, 'Jordan Rivera', 'jordan@example.com', 'CA', '2025-08-01');

SELECT * FROM customers WHERE customer_id = 11;
```

**Result:**

```text
OK: 1 row(s) affected

customer_id | full_name     | email              | country | created_date
------------+---------------+--------------------+---------+-------------
11          | Jordan Rivera | jordan@example.com | CA      | 2025-08-01
(1 row)
```

Line by line:

1. `INSERT INTO customers (...)` targets the `customers` table and lists the five columns.
2. `VALUES (11, ..., '2025-08-01')` provides one value per column. Text and dates are in single quotes; numbers are not.
3. The database replies with the number of affected rows (1 here).
4. We immediately `SELECT` to confirm the row exists. **Verify after you write** is a habit worth keeping.

#### Letting the database generate the ID

In `customers`, `customer_id` is declared `INTEGER PRIMARY KEY`. In SQLite that column automatically picks the next free number if you leave it out:

```sql
INSERT INTO customers (full_name, email, country, created_date)
VALUES ('Kai Nakamura', 'kai@example.com', 'JP', '2025-08-02');

SELECT customer_id, full_name FROM customers WHERE customer_id > 10;
```

**Result:**

```text
OK: 1 row(s) affected

customer_id | full_name
------------+--------------
11          | Jordan Rivera
12          | Kai Nakamura
(2 rows)
```

Kai received ID 12 automatically. Other databases use different syntax for this (`AUTO_INCREMENT` in MySQL, `IDENTITY` or `SERIAL` in SQL Server/PostgreSQL), but the idea is the same.

#### Omitted columns become NULL (or a default)

If a column is not listed and has no `DEFAULT`, it becomes `NULL`, provided the column allows NULL. Here we leave out `email` and `country`:

```sql
INSERT INTO customers (full_name, created_date)
VALUES ('Lena Fischer', '2025-08-03');

SELECT customer_id, full_name, email, country FROM customers WHERE full_name = 'Lena Fischer';
```

**Result:**

```text
OK: 1 row(s) affected

customer_id | full_name    | email | country
------------+--------------+-------+--------
13          | Lena Fischer | NULL  | NULL
(1 row)
```

`NULL` means "unknown or not applicable". It is *not* the same as an empty string or zero. (You met `IS NULL` on Thursday; it matters again below.)

#### Inserting several rows at once

List several value groups separated by commas. This is faster and keeps the operation all-or-nothing:

```sql
INSERT INTO products (product_id, product_name, category, unit_price) VALUES
    (9,  'Keyboard',   'Electronics', 70.00),
    (10, 'Mouse Pad',  'Accessories',  8.00),
    (11, 'Headphones', 'Electronics', 89.50);

SELECT product_id, product_name, unit_price FROM products WHERE product_id >= 9;
```

**Result:**

```text
OK: 3 row(s) affected

product_id | product_name | unit_price
-----------+--------------+-----------
9          | Keyboard     | 70.0
10         | Mouse Pad    | 8.0
11         | Headphones   | 89.5
(3 rows)
```

#### Inserting rows copied from another query: INSERT ... SELECT

Instead of `VALUES`, you can feed `INSERT` with a `SELECT`. It copies rows. First, a throw-away archive table (this is DDL, but it is only to give us somewhere to copy to):

```sql
CREATE TABLE completed_orders_archive (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER,
    total_amount REAL
);

INSERT INTO completed_orders_archive (order_id, customer_id, total_amount)
SELECT order_id, customer_id, total_amount
FROM orders
WHERE status = 'completed';

SELECT * FROM completed_orders_archive;
```

**Result:**

```text
OK

OK: 8 row(s) affected

order_id | customer_id | total_amount
---------+-------------+-------------
101      | 1           | 1225.0
102      | 1           | 30.48
103      | 2           | 150.0
107      | 99          | 35.0
108      | NULL        | 9.99
110      | 2           | 55.0
111      | 3           | 19.99
112      | 7           | 9.99
(8 rows)
```

How it works: the `SELECT` runs first and produces a result set; each row of that result set is inserted into the archive table. The column lists must match in count and order. QA use: copy a subset of production-like rows into a scratch table before you experiment on them.

#### When INSERT fails

Constraints protect the table. Let us trigger two common failures deliberately (do not be afraid of errors; they tell you what the database refuses to accept):

```sql
-- 1. Primary key already used
INSERT INTO customers (customer_id, full_name) VALUES (1, 'Duplicate Id Person');

-- 2. NOT NULL column left out (full_name is required)
INSERT INTO customers (customer_id, email) VALUES (50, 'noname@example.com');
```

**Result:**

```text
Error: UNIQUE constraint failed: customers.customer_id

Error: NOT NULL constraint failed: customers.full_name
```

Both rows were rejected, and nothing was inserted. Error messages worth recognising: `UNIQUE constraint failed` (the key is already taken) and `NOT NULL constraint failed` (a required value is missing). We explore constraints properly in the next lesson.

### 4. UPDATE: changing existing rows

#### Syntax

```text
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

- `SET` lists each column and its new value.
- `WHERE` chooses **which rows** to change. It uses exactly the same conditions as in `SELECT`.

#### The golden rule: SELECT before you UPDATE

Before you run an `UPDATE`, run a `SELECT` with the same `WHERE`. If the `SELECT` shows the rows you expected, change `SELECT ...` to `UPDATE ... SET ...`.

Suppose the NULL email of customer 6 (Frank Lee) needs fixing. First, preview:

```sql
SELECT customer_id, full_name, email FROM customers WHERE customer_id = 6;
```

**Result:**

```text
customer_id | full_name | email
------------+-----------+------
6           | Frank Lee | NULL
(1 row)
```

One row, the right one. Now update:

```sql
UPDATE customers
SET email = 'frank@example.com'
WHERE customer_id = 6;

SELECT customer_id, full_name, email FROM customers WHERE customer_id = 6;
```

**Result:**

```text
OK: 1 row(s) affected

customer_id | full_name | email
------------+-----------+------------------
6           | Frank Lee | frank@example.com
(1 row)
```

Note "1 row(s) affected". If you expected one row and the database says 37, **stop**.

#### Updating several columns, and using the old value

`SET` can calculate from the current value. Give every product in the Accessories category a 10% price rise, rounded to cents:

```sql
UPDATE products
SET unit_price = ROUND(unit_price * 1.10, 2)
WHERE category = 'Accessories';

SELECT product_id, product_name, category, unit_price FROM products WHERE category = 'Accessories';
```

**Result:**

```text
OK: 2 row(s) affected

product_id | product_name | category    | unit_price
-----------+--------------+-------------+-----------
3          | USB-C Cable  | Accessories | 10.99
10         | Mouse Pad    | Accessories | 8.8
(2 rows)
```

Here `unit_price * 1.10` uses the old price (9.99 for the cable, 8.00 for the mouse pad) on the right of `=`. `ROUND(x, 2)` rounds to two decimals; without it floating-point arithmetic can leave artefacts like `10.989000000000001`.

Updating two columns at once:

```sql
UPDATE orders
SET status = 'completed', total_amount = 34.99
WHERE order_id = 105;

SELECT order_id, status, total_amount FROM orders WHERE order_id = 105;
```

**Result:**

```text
OK: 1 row(s) affected

order_id | status    | total_amount
---------+-----------+-------------
105      | completed | 34.99
(1 row)
```

#### The disaster: UPDATE without WHERE

We wrap this in a transaction so we can undo it. (Transactions are explained in section 6; just follow along for now.)

```sql
BEGIN;

UPDATE orders SET status = 'cancelled';   -- no WHERE: every row changes

SELECT status, COUNT(*) AS how_many FROM orders GROUP BY status;

ROLLBACK;   -- undo everything since BEGIN

SELECT status, COUNT(*) AS how_many FROM orders GROUP BY status ORDER BY status;
```

**Result:**

```text
OK

OK: 12 row(s) affected

status    | how_many
----------+---------
cancelled | 12
(1 row)

OK

status    | how_many
----------+---------
cancelled | 1
completed | 9
pending   | 1
shipped   | 1
(4 rows)
```

Inside the transaction *all 12* orders became `cancelled`. After `ROLLBACK` the original statuses were restored. Without the transaction, you would have destroyed the test data and have to rebuild it. Forgetting `WHERE` is among the most famous mistakes in all of IT. (The `GROUP BY` and `COUNT(*)` you see here are covered in detail later today.)

#### UPDATE with a subquery

The `WHERE` (or `SET`) can use a subquery, a `SELECT` inside parentheses. Suppose we only want to act on orders whose payment was refunded. Here is the pattern, previewed with `SELECT` first:

```sql
SELECT order_id, status
FROM orders
WHERE order_id IN (SELECT order_id FROM payments WHERE status = 'refunded');
```

**Result:**

```text
order_id | status
---------+----------
106      | cancelled
(1 row)
```

The inner query finds order IDs whose payment was refunded; the outer query returns matching orders. The same `WHERE order_id IN (...)` can be pasted after `UPDATE orders SET ...`. Subqueries have their own lesson later today.

### 5. DELETE: removing rows

#### Syntax

```text
DELETE FROM table_name
WHERE condition;
```

There is no column list because `DELETE` removes *whole rows*. And again: no `WHERE` means every row in the table.

#### Preview, delete, verify

The duplicate customer 8 ("Bob Smith", same email as customer 2) is clearly a mistake and has no orders. Preview first:

```sql
SELECT customer_id, full_name, email FROM customers WHERE customer_id = 8;
```

**Result:**

```text
customer_id | full_name | email
------------+-----------+----------------
8           | Bob Smith | bob@example.com
(1 row)
```

```sql
DELETE FROM customers WHERE customer_id = 8;

SELECT customer_id, full_name, email FROM customers WHERE email = 'bob@example.com';
```

**Result:**

```text
OK: 1 row(s) affected

customer_id | full_name | email
------------+-----------+----------------
2           | Bob Smith | bob@example.com
(1 row)
```

Now only the original Bob remains.

#### Deleting with a condition on several rows

Remove the scratch customers we created earlier in the lesson (IDs above 10):

```sql
DELETE FROM customers WHERE customer_id > 10;

SELECT COUNT(*) AS customers_left FROM customers;
```

**Result:**

```text
OK: 3 row(s) affected

customers_left
--------------
9
(1 row)
```

#### DELETE vs DROP TABLE vs TRUNCATE

| Statement | What it removes | Table still exists? | Can use WHERE? |
|---|---|---|---|
| `DELETE FROM t WHERE ...` | Chosen rows (or all rows if no WHERE) | Yes | Yes |
| `TRUNCATE TABLE t` (MySQL, PostgreSQL, SQL Server, Oracle) | All rows, quickly | Yes | No |
| `DROP TABLE t` | The table's data **and structure** | No | No |

SQLite has no `TRUNCATE`; `DELETE FROM t;` is how you empty a table there.

Let us drop our scratch table now that we have finished with it:

```sql
DROP TABLE completed_orders_archive;
```

**Result:**

```text
OK
```

#### Deleting and foreign keys

If `order_items` rows point to an order and you delete that order, the item rows become **orphans**, exactly like items 14 and 15 in our planted bugs. Databases can prevent this with enforced foreign keys; that is the topic of the next lesson. For now remember: *the order in which you delete matters. Delete children (items) before parents (orders).*

#### Soft delete: the "don't actually delete" pattern

Many real applications never run `DELETE`. Instead they add a column such as `is_deleted` or set `status = 'cancelled'` or `'inactive'`. This keeps history for audits. As a tester you should know both approaches, because "delete a customer" in the UI may map to `UPDATE` in the database, and your automated test should validate the correct one.

### 6. Transactions: a safety net

A **transaction** groups statements so they all take effect together (`COMMIT`) or not at all (`ROLLBACK`). You already used it above. The pattern:

```text
BEGIN;          -- start
   ... INSERT / UPDATE / DELETE statements ...
   ... SELECT to check the result ...
COMMIT;         -- keep it   (or)   ROLLBACK;  -- undo it
```

Real-world analogy: a bank transfer subtracts money from account A and adds it to account B. Both steps must happen or neither. Test engineers use `ROLLBACK` as a cheap way to experiment without any permanent damage, and many test frameworks wrap each test in a transaction and roll it back afterwards. Deeper transaction topics (isolation levels, locking) are for a later week.

### 7. Real-world QA scenarios

**Scenario A: seeding a repeatable test.** You are testing "an order with a negative quantity must be rejected". You insert the exact data you need, with a recognisable marker so you can find and remove it later:

```sql
BEGIN;

INSERT INTO customers (customer_id, full_name, email, country, created_date)
VALUES (9001, 'TEST_USER_neg_qty', 'test_neg@example.com', 'US', '2025-09-01');

INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (9001, 9001, '2025-09-01', 'pending', 0);

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (9001, 3, -5, 9.99);

SELECT i.item_id, i.order_id, i.quantity FROM order_items i WHERE i.order_id = 9001;
```

**Result:**

```text
OK

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

item_id | order_id | quantity
--------+----------+---------
17      | 9001     | -5
(1 row)
```

The `item_id` was generated automatically. Now the tear-down, in child-to-parent order:

```sql
DELETE FROM order_items WHERE order_id = 9001;
DELETE FROM orders      WHERE order_id = 9001;
DELETE FROM customers   WHERE customer_id = 9001;
COMMIT;

SELECT COUNT(*) AS leftover_test_rows FROM customers WHERE full_name LIKE 'TEST_USER%';
```

**Result:**

```text
OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

OK

leftover_test_rows
------------------
0
(1 row)
```

The `TEST_USER_` prefix and the 9001 ID range make cleanup easy and safe: you never clean up by guessing.

**Scenario B: fixing a data bug found by validation.** Order 110 has `total_amount` 55.00 but its items add up to 50.00. After the team agrees the *items* are right, you correct the header:

```sql
UPDATE orders
SET total_amount = (SELECT SUM(quantity * unit_price) FROM order_items WHERE order_id = 110)
WHERE order_id = 110;

SELECT order_id, total_amount FROM orders WHERE order_id = 110;
```

**Result:**

```text
OK: 1 row(s) affected

order_id | total_amount
---------+-------------
110      | 50.0
(1 row)
```

Here a subquery calculates the new total from the items. (In a real project you would investigate which side is wrong before editing; the point of validation is to *find* the discrepancy.)

**Scenario C: removing an exact duplicate row.** Order 103 has two identical item rows (IDs 5 and 13). A safe rule: keep the lowest `item_id` in each duplicate group.

```sql
DELETE FROM order_items
WHERE item_id = 13;

SELECT item_id, order_id, product_id, quantity FROM order_items WHERE order_id = 103;
```

**Result:**

```text
OK: 1 row(s) affected

item_id | order_id | product_id | quantity
--------+----------+------------+---------
5       | 103      | 4          | 1
(1 row)
```

(For many duplicates you would write a rule using `GROUP BY` and `MIN(item_id)`, which you will see in the validation lessons.)

### 8. Common mistakes checklist

1. Forgetting `WHERE` on `UPDATE` or `DELETE`.
2. Not previewing with `SELECT` first.
3. Omitting the column list in `INSERT`.
4. Putting values in a different order from the columns.
5. Using double quotes for text (use single quotes for string values).
6. Deleting parent rows before child rows when constraints are enforced.
7. Running destructive statements on the wrong environment: always check which database you are connected to.
8. Not checking the "rows affected" count.

## Practice Questions

Try each question yourself before reading the answer. All answers below were executed on the practice database (state continues from the lesson above).

**Q1.** Insert a new product: id 12, "Phone Stand", category "Accessories", price 15.00. Confirm it exists.

**Q2.** Increase the price of every `Furniture` product by 5 (add 5.00). Preview first, then update.

**Q3.** Write a statement that deletes all defects whose `status` is `closed`, then count the remaining defects. Do it inside a transaction and roll it back.

**Q4.** What happens if you run `UPDATE products SET unit_price = 0;` without WHERE? How could you protect yourself?

**Q5.** Customer 9 (Hana Sato) has no orders. Show the single `SELECT` you would run to prove that before deleting her, and then delete her.

### Answers

**A1.**

```sql
INSERT INTO products (product_id, product_name, category, unit_price)
VALUES (12, 'Phone Stand', 'Accessories', 15.00);

SELECT * FROM products WHERE product_id = 12;
```

**Result:**

```text
OK: 1 row(s) affected

product_id | product_name | category    | unit_price
-----------+--------------+-------------+-----------
12         | Phone Stand  | Accessories | 15.0
(1 row)
```

**A2.**

```sql
SELECT product_id, product_name, unit_price FROM products WHERE category = 'Furniture';

UPDATE products SET unit_price = unit_price + 5 WHERE category = 'Furniture';

SELECT product_id, product_name, unit_price FROM products WHERE category = 'Furniture';
```

**Result:**

```text
product_id | product_name  | unit_price
-----------+---------------+-----------
4          | Desk Chair    | 150.0
8          | Standing Desk | 450.0
(2 rows)

OK: 2 row(s) affected

product_id | product_name  | unit_price
-----------+---------------+-----------
4          | Desk Chair    | 155.0
8          | Standing Desk | 455.0
(2 rows)
```

**A3.**

```sql
BEGIN;
DELETE FROM defects WHERE status = 'closed';
SELECT COUNT(*) AS defects_left FROM defects;
ROLLBACK;
SELECT COUNT(*) AS defects_after_rollback FROM defects;
```

**Result:**

```text
OK

OK: 2 row(s) affected

defects_left
------------
4
(1 row)

OK

defects_after_rollback
----------------------
6
(1 row)
```

**A4.** Every product would be priced at 0: all rows are affected because there is no `WHERE`. Protect yourself by (a) always writing the `WHERE` first, (b) previewing with `SELECT`, (c) using `BEGIN ... ROLLBACK`, (d) checking the "rows affected" count, and (e) working in a test database, never production.

**A5.**

```sql
SELECT COUNT(*) AS orders_for_customer_9 FROM orders WHERE customer_id = 9;

DELETE FROM customers WHERE customer_id = 9;

SELECT COUNT(*) AS rows_left_for_customer_9 FROM customers WHERE customer_id = 9;
```

**Result:**

```text
orders_for_customer_9
---------------------
0
(1 row)

OK: 1 row(s) affected

rows_left_for_customer_9
------------------------
0
(1 row)
```

## Summary / Key Takeaways

- `INSERT` adds rows, `UPDATE` changes rows, `DELETE` removes rows. All three are DML and all three change data permanently once committed.
- Always list columns in `INSERT`; use multi-row `VALUES` and `INSERT ... SELECT` for efficiency.
- `UPDATE` and `DELETE` need a `WHERE` clause. Without it they affect **every row**.
- Preview with `SELECT`, change, then verify with `SELECT` again. Check the rows-affected count.
- Wrap risky work in `BEGIN ... ROLLBACK/COMMIT`.
- `DELETE` removes rows, `DROP TABLE` removes the table itself, `TRUNCATE` (not in SQLite) empties a table quickly.
- Delete children before parents, and consider soft deletes for audit history.
- Our shared practice database "QA Shop" intentionally contains duplicates, NULLs and orphans so that the joins and validation queries in the next lessons have real work to do.

## Additional Resources

- SQLite documentation, INSERT: https://www.sqlite.org/lang_insert.html
- SQLite documentation, UPDATE: https://www.sqlite.org/lang_update.html
- SQLite documentation, DELETE: https://www.sqlite.org/lang_delete.html
