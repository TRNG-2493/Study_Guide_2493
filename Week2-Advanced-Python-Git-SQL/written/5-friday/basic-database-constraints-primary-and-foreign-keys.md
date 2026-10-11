# Basic Database Constraints: Primary and Foreign Keys

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a database constraint is and why databases enforce rules on data.
- Define and use `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK` and `DEFAULT`.
- Describe parent and child tables, and what "referential integrity" means.
- Recognise an **orphan row** and explain how it can exist even though a foreign key is declared.
- Turn on foreign key enforcement in SQLite with `PRAGMA foreign_keys = ON` and find existing violations with `PRAGMA foreign_key_check`.
- Explain `ON DELETE RESTRICT`, `CASCADE` and `SET NULL`.
- Write negative tests that prove constraints actually work, and inspect a schema to see which constraints exist.

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

This week you are adding SQL to your QA toolkit so you can validate data, and starting the Project 1 "QE Foundations" capstone. A **constraint** is a rule that the database itself enforces. They matter to a tester for three reasons:

1. **They are requirements you can test.** "A customer's email must be unique" and "an order must belong to a real customer" are business rules. If the database enforces them, there is a constraint to verify. If it does not, there is a gap that may let bad data in, and bad data produces bugs in every layer above.
2. **They explain test failures.** When your automated test inserts data and gets `FOREIGN KEY constraint failed`, you need to understand why: the parent row was missing, or you deleted in the wrong order.
3. **Missing constraints cause the dirty data that joins reveal.** Our practice database contains orphans (an order for customer 99, an item for order 999). Understanding keys is the foundation for the join lessons that follow, because **joins match primary keys to foreign keys**.

## The Concept

### 1. What is a constraint?

A **constraint** is a rule attached to a table or column that the database checks every time you `INSERT`, `UPDATE` or `DELETE`. If a change would break the rule, the database rejects the statement with an error and the data stays unchanged.

Analogy: think of a paper form at a doctor's office. "Name" has a red asterisk (required: `NOT NULL`). "Patient ID" is printed on a numbered pad so no two forms share a number (`PRIMARY KEY`). "Insurance company" must be picked from an approved list (`FOREIGN KEY`). "Age" cannot be negative (`CHECK`). A receptionist who enforces those rules prevents most errors before they reach the filing cabinet; the database does the same job automatically.

| Constraint | Rule it enforces |
|---|---|
| `PRIMARY KEY` | Each row can be uniquely identified; value is unique and not NULL |
| `FOREIGN KEY` | Value must exist in another table's key (or be NULL) |
| `NOT NULL` | The column must have a value |
| `UNIQUE` | No two rows may share the same value |
| `CHECK` | A condition must be true, for example `quantity > 0` |
| `DEFAULT` | Not a rule exactly: the value used if you do not supply one |

### 2. Primary keys

#### Definition

A **primary key (PK)** is a column (or set of columns) whose value uniquely identifies each row in a table. Rules: it must be **unique**, it must be **not NULL**, and each table can have **only one** primary key.

In our database `customers.customer_id` is the primary key. Customer 1 is Alice, and no other customer can ever have ID 1. That lets other tables refer to Alice simply as "1", with no ambiguity. This matters because *names are not unique*: we have two different customer rows both named Bob Smith.

#### Surrogate vs natural keys

- A **surrogate key** is an artificial identifier with no business meaning, such as `customer_id = 7`. It never changes and is easy to index.
- A **natural key** is a real-world value such as an email address or a passport number. These can change or turn out not to be unique, so they are generally used as `UNIQUE` columns rather than primary keys.

Most application databases, including ours, use surrogate integer keys.

#### Composite primary keys

A primary key can be made of more than one column. For example, a table `student_course(student_id, course_id)` might use both columns together as the key: a student can appear many times, a course can appear many times, but the *pair* is unique. We will create one shortly.

#### What the database does with a primary key

Let us look at our table definitions as stored in SQLite:

```sql
SELECT name, sql FROM sqlite_master WHERE type = 'table' AND name = 'customers';
```

**Result:**

```text
name      | sql
----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------
customers | CREATE TABLE customers (
    customer_id  INTEGER PRIMARY KEY,
    full_name    TEXT NOT NULL,
    email        TEXT,
    country      TEXT,
    created_date TEXT
)
(1 row)
```

```sql
PRAGMA table_info(customers);
```

**Result:**

```text
cid | name         | type    | notnull | dflt_value | pk
----+--------------+---------+---------+------------+---
0   | customer_id  | INTEGER | 0       | NULL       | 1
1   | full_name    | TEXT    | 1       | NULL       | 0
2   | email        | TEXT    | 0       | NULL       | 0
3   | country      | TEXT    | 0       | NULL       | 0
4   | created_date | TEXT    | 0       | NULL       | 0
(5 rows)
```

`PRAGMA table_info` is a SQLite command that lists columns. The columns of the output are: `cid` (position), `name`, `type`, `notnull` (1 means NOT NULL), `dflt_value` (default), and `pk` (1 means it is part of the primary key). Notice `customer_id` has `pk = 1` and `full_name` has `notnull = 1`. Other databases use `DESCRIBE customers` (MySQL) or `information_schema.columns` (PostgreSQL, SQL Server) for the same purpose.

Now let us break the rule on purpose:

```sql
-- Customer 1 already exists
INSERT INTO customers (customer_id, full_name) VALUES (1, 'Another Alice');

-- Primary key may not be NULL for a real key; an INTEGER PRIMARY KEY in SQLite
-- instead auto-generates a value when NULL is given
INSERT INTO customers (customer_id, full_name) VALUES (NULL, 'Auto Numbered Person');
SELECT customer_id, full_name FROM customers WHERE customer_id > 10;
```

**Result:**

```text
Error: UNIQUE constraint failed: customers.customer_id

OK: 1 row(s) affected

customer_id | full_name
------------+---------------------
11          | Auto Numbered Person
(1 row)
```

First insert: rejected, because ID 1 is already taken. Second: SQLite is special here and, for a column declared exactly `INTEGER PRIMARY KEY`, turns a NULL into the next free number. (In most other databases, and for non-integer primary keys, NULL in a key column is an error.) Let us tidy that test row:

```sql
DELETE FROM customers WHERE customer_id > 10;
```

**Result:**

```text
OK: 1 row(s) affected
```

### 3. NOT NULL, UNIQUE, CHECK and DEFAULT

We will use small scratch tables prefixed `demo_` so that our main tables stay untouched.

```sql
CREATE TABLE demo_accounts (
    account_id INTEGER PRIMARY KEY,
    username   TEXT    NOT NULL UNIQUE,
    email      TEXT    UNIQUE,
    age        INTEGER CHECK (age >= 18),
    status     TEXT    NOT NULL DEFAULT 'active'
);
```

**Result:**

```text
OK
```

Line by line:

- `account_id INTEGER PRIMARY KEY`: surrogate key, auto-generated.
- `username TEXT NOT NULL UNIQUE`: required, and no two accounts may share it.
- `email TEXT UNIQUE`: optional, but if present must be unique. Most databases allow *several* NULLs in a UNIQUE column because "unknown" is not equal to "unknown".
- `age INTEGER CHECK (age >= 18)`: any value must be 18 or more. A NULL age passes (the condition is not false).
- `status TEXT NOT NULL DEFAULT 'active'`: if you leave it out, it becomes `'active'`.

Valid inserts first, including a row that relies on the default:

```sql
INSERT INTO demo_accounts (username, email, age) VALUES ('alice_qa', 'alice@qa.test', 30);
INSERT INTO demo_accounts (username, email, age, status) VALUES ('bob_qa', NULL, NULL, 'locked');
INSERT INTO demo_accounts (username, email) VALUES ('cara_qa', NULL);

SELECT * FROM demo_accounts;
```

**Result:**

```text
OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

account_id | username | email         | age  | status
-----------+----------+---------------+------+-------
1          | alice_qa | alice@qa.test | 30   | active
2          | bob_qa   | NULL          | NULL | locked
3          | cara_qa  | NULL          | NULL | active
(3 rows)
```

Notice Alice and Cara got `status = active` from the `DEFAULT`, and two different rows have `email = NULL` without violating `UNIQUE`.

Now the invalid ones, each a "negative test" for a different constraint:

```sql
-- NOT NULL violation (username missing)
INSERT INTO demo_accounts (email, age) VALUES ('x@qa.test', 40);

-- UNIQUE violation (username already used)
INSERT INTO demo_accounts (username) VALUES ('alice_qa');

-- UNIQUE violation on email
INSERT INTO demo_accounts (username, email) VALUES ('alice_two', 'alice@qa.test');

-- CHECK violation (too young)
INSERT INTO demo_accounts (username, age) VALUES ('kid_qa', 12);

-- Verify none of the bad rows got in
SELECT COUNT(*) AS rows_in_table FROM demo_accounts;
```

**Result:**

```text
Error: NOT NULL constraint failed: demo_accounts.username

Error: UNIQUE constraint failed: demo_accounts.username

Error: UNIQUE constraint failed: demo_accounts.email

Error: CHECK constraint failed: age >= 18

rows_in_table
-------------
3
(1 row)
```

All four were rejected and the table still has its three valid rows. In test-automation language, these four statements are **negative test cases**: they pass when the database *refuses* the data.

Why does this matter for our shop data? Look back at `customers`: `email` has no `UNIQUE` constraint, which is exactly why the duplicate Bob Smith (customers 2 and 8, same email) exists. And `order_items.quantity` has no `CHECK (quantity > 0)`, which is how `-1` got into item 16. **Missing constraints are findings.**

### 4. Foreign keys

#### Definition

A **foreign key (FK)** is a column in one table that refers to the primary key of another table. It says: "the value here must match an existing row over there."

In our shop:

- `orders.customer_id` is a foreign key to `customers.customer_id`.
- `order_items.order_id` references `orders.order_id`.
- `order_items.product_id` references `products.product_id`.
- `payments.order_id` references `orders.order_id`.
- `defects.product_id` references `products.product_id`.

The table with the primary key is the **parent**; the table holding the foreign key is the **child**. `customers` is the parent of `orders`; `orders` is the parent of `order_items`.

**Referential integrity** means every foreign key value points to a real parent row (or is NULL). When this holds, you never have an order for a customer who does not exist.

Analogy: a library loan card lists a member number. Referential integrity means every number on a loan card belongs to a real member. An orphan row is like a loan card with a member number that was never issued, or whose member was deleted from the records.

#### The declaration syntax

From our `order_items` table:

```text
FOREIGN KEY (order_id) REFERENCES orders(order_id)
```

Read it as: "the column `order_id` in this table must appear as `order_id` in the `orders` table."

#### Surprise: the declaration exists, yet orphans exist

We *declared* foreign keys on every child table. Yet our data contains order 107 for customer 99, who does not exist. How?

SQLite, for historical compatibility, **ignores foreign keys unless you switch enforcement on** for each connection. Our practice data was loaded with enforcement off, just like a bulk import that bypassed checks or a legacy system migration. Let us prove the orphan is there:

```sql
SELECT order_id, customer_id FROM orders WHERE order_id = 107;
SELECT customer_id FROM customers WHERE customer_id = 99;
```

**Result:**

```text
order_id | customer_id
---------+------------
107      | 99
(1 row)

customer_id
-----------
(0 rows)
```

Order 107 exists, and no customer 99 does. Currently (enforcement off), SQLite would even let us add another orphan:

```sql
PRAGMA foreign_keys;

INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (500, 12345, '2025-08-10', 'pending', 10.00);

SELECT order_id, customer_id FROM orders WHERE order_id = 500;
```

**Result:**

```text
foreign_keys
------------
0
(1 row)

OK: 1 row(s) affected

order_id | customer_id
---------+------------
500      | 12345
(1 row)
```

`PRAGMA foreign_keys;` printed `0`, meaning "off", and the orphan order 500 was accepted. Clean it up and switch enforcement on:

```sql
DELETE FROM orders WHERE order_id = 500;

PRAGMA foreign_keys = ON;
PRAGMA foreign_keys;
```

**Result:**

```text
OK: 1 row(s) affected

OK

foreign_keys
------------
1
(1 row)
```

In SQLite you must run `PRAGMA foreign_keys = ON;` at the start of **every connection** (it cannot be changed in the middle of a transaction). PostgreSQL, MySQL (InnoDB) and SQL Server enforce declared foreign keys all the time. QA lesson: *always check whether the test environment actually enforces its constraints.*

#### With enforcement ON

Try inserting an order for a nonexistent customer:

```sql
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (501, 12345, '2025-08-10', 'pending', 10.00);
```

**Result:**

```text
Error: FOREIGN KEY constraint failed
```

Now rejected: `FOREIGN KEY constraint failed`. Valid parent, no problem:

```sql
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (501, 10, '2025-08-10', 'pending', 10.00);

SELECT order_id, customer_id FROM orders WHERE order_id = 501;
```

**Result:**

```text
OK: 1 row(s) affected

order_id | customer_id
---------+------------
501      | 10
(1 row)
```

A foreign key column **may be NULL** (unless it is also declared `NOT NULL`). NULL means "no parent". That is how order 108, the guest checkout, is legitimate under the schema:

```sql
INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
VALUES (502, NULL, '2025-08-11', 'pending', 5.00);

SELECT order_id, customer_id FROM orders WHERE order_id IN (501, 502);
```

**Result:**

```text
OK: 1 row(s) affected

order_id | customer_id
---------+------------
501      | 10
502      | NULL
(2 rows)
```

Deleting a parent that still has children is also blocked:

```sql
-- Customer 10 now has order 501 attached
DELETE FROM customers WHERE customer_id = 10;
```

**Result:**

```text
Error: FOREIGN KEY constraint failed
```

The database refuses because order 501 would become an orphan. (The rule "default action: reject" is called `NO ACTION` or `RESTRICT`.) Delete children first:

```sql
DELETE FROM orders WHERE order_id IN (501, 502);
DELETE FROM customers WHERE customer_id = 10;
SELECT COUNT(*) AS customers_now FROM customers;
```

**Result:**

```text
OK: 2 row(s) affected

OK: 1 row(s) affected

customers_now
-------------
9
(1 row)
```

#### Finding existing violations: PRAGMA foreign_key_check

Turning on enforcement does **not** repair bad rows that are already in the tables. To list them, SQLite offers:

```sql
PRAGMA foreign_key_check;
```

**Result:**

```text
table       | rowid | parent    | fkid
------------+-------+-----------+-----
payments    | 10    | orders    | 0
order_items | 14    | orders    | 1
order_items | 15    | products  | 0
orders      | 107   | customers | 0
(4 rows)
```

Each row identifies a **child table**, the `rowid` of the offending child row, the **parent table** it should point to, and the number of the FK definition. Let us decode it: the `orders` rowid 107 (the order's own ID, because `order_id` is the rowid) is missing a customer; `order_items` rowid 14 is missing an order, rowid 15 is missing a product; `payments` rowid 10 is missing an order. Those are planted problems 4, 9, 10 and 12. (Order 108 with NULL customer is not reported, since NULL is allowed.)

In databases other than SQLite you find orphans with join queries, which is what the next lessons teach you to write. In fact, the join approach is more flexible, and you will write it yourself in the "LEFT and RIGHT JOIN" lesson.

### 5. ON DELETE actions: what should happen to children?

When you define a foreign key you may say what happens when the parent row is deleted:

| Action | Meaning | Typical use |
|---|---|---|
| `RESTRICT` / `NO ACTION` (default) | Refuse to delete the parent while children exist | Orders must not lose their customer |
| `CASCADE` | Delete the children automatically too | A temporary cart and its cart lines |
| `SET NULL` | Keep children but set their FK to NULL | Keep order history, detach from deleted customer |
| `SET DEFAULT` | Set FK to the column default | Rare |

Demonstration with two scratch tables:

```sql
CREATE TABLE demo_cart (
    cart_id INTEGER PRIMARY KEY
);
CREATE TABLE demo_cart_line (
    line_id INTEGER PRIMARY KEY,
    cart_id INTEGER,
    note    TEXT,
    FOREIGN KEY (cart_id) REFERENCES demo_cart(cart_id) ON DELETE CASCADE
);
CREATE TABLE demo_cart_gift (
    gift_id INTEGER PRIMARY KEY,
    cart_id INTEGER,
    note    TEXT,
    FOREIGN KEY (cart_id) REFERENCES demo_cart(cart_id) ON DELETE SET NULL
);

INSERT INTO demo_cart VALUES (1), (2);
INSERT INTO demo_cart_line VALUES (1, 1, 'line A'), (2, 1, 'line B'), (3, 2, 'line C');
INSERT INTO demo_cart_gift VALUES (1, 1, 'gift for cart 1');

DELETE FROM demo_cart WHERE cart_id = 1;

SELECT * FROM demo_cart_line;
SELECT * FROM demo_cart_gift;
```

**Result:**

```text
OK

OK

OK

OK: 2 row(s) affected

OK: 3 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

line_id | cart_id | note
--------+---------+-------
3       | 2       | line C
(1 row)

gift_id | cart_id | note
--------+---------+----------------
1       | NULL    | gift for cart 1
(1 row)
```

Deleting cart 1 removed its two lines (`CASCADE`) but kept the gift row and detached it (`SET NULL`). **Test-automation warning:** `CASCADE` is convenient for clean-up but dangerous for production, and a tester should know when it is configured because a single delete can silently remove many rows.

### 6. Composite keys in practice

```sql
CREATE TABLE demo_enrolment (
    student_id INTEGER,
    course_id  INTEGER,
    enrolled_on TEXT,
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO demo_enrolment VALUES (1, 10, '2025-09-01');
INSERT INTO demo_enrolment VALUES (1, 11, '2025-09-01');
INSERT INTO demo_enrolment VALUES (2, 10, '2025-09-01');
-- same student + same course again: rejected
INSERT INTO demo_enrolment VALUES (1, 10, '2025-09-05');

SELECT * FROM demo_enrolment;
```

**Result:**

```text
OK

OK: 1 row(s) affected

OK: 1 row(s) affected

OK: 1 row(s) affected

Error: UNIQUE constraint failed: demo_enrolment.student_id, demo_enrolment.course_id

student_id | course_id | enrolled_on
-----------+-----------+------------
1          | 10        | 2025-09-01
1          | 11        | 2025-09-01
2          | 10        | 2025-09-01
(3 rows)
```

Student 1 can take several courses; course 10 can have several students; but the pair (1, 10) cannot be added twice. Compare this with our shop's `order_items`: it has its own surrogate `item_id` key, so nothing stops the same product from appearing twice on one order (the duplicate in order 103). Because of a missing `UNIQUE (order_id, product_id)` rule, that duplicate is allowed. Whether duplicates *should* be allowed is a business decision, so the QA engineer asks the question.

### 7. Inspecting constraints (a QA skill)

You can ask SQLite which foreign keys a table has:

```sql
PRAGMA foreign_key_list(order_items);
```

**Result:**

```text
id | seq | table    | from       | to         | on_update | on_delete | match
---+-----+----------+------------+------------+-----------+-----------+------
0  | 0   | products | product_id | product_id | NO ACTION | NO ACTION | NONE
1  | 0   | orders   | order_id   | order_id   | NO ACTION | NO ACTION | NONE
(2 rows)
```

Each row: this table's column (`from`), the parent table and column (`table`, `to`), and the delete/update rules (`on_delete`, `on_update`). A common QA task is a **schema review**: for every child table, confirm that the FK exists, that columns that should be required are `NOT NULL`, and that obvious `CHECK` rules (positive quantity, valid status) exist. Missing ones become defects or improvement suggestions.

Let us clean up our scratch tables:

```sql
DROP TABLE demo_cart_line;
DROP TABLE demo_cart_gift;
DROP TABLE demo_cart;
DROP TABLE demo_enrolment;
DROP TABLE demo_accounts;
```

**Result:**

```text
OK

OK

OK

OK

OK
```

### 8. Real-world QA scenarios

- **Constraint test suite:** for each table, automate a negative test per rule (duplicate PK, NULL in NOT NULL, FK to missing parent, CHECK violation) and assert that the database throws the expected error.
- **Test-data teardown order:** a failing teardown with `FOREIGN KEY constraint failed` means you deleted a parent before its children. Delete from leaf tables upwards: `order_items`, `payments`, `orders`, `customers`.
- **Legacy data migrations:** before turning enforcement on, run an orphan check (`PRAGMA foreign_key_check` or an anti-join query) to find rows that would violate it.
- **Requirement gaps:** "email must be unique" is in the spec, but the schema has no `UNIQUE`. That is a defect worth reporting before duplicate users appear in production.

### 9. Common mistakes

1. Assuming a declared foreign key is automatically enforced (not in SQLite until you enable it).
2. Forgetting `PRAGMA foreign_keys = ON` on a new connection.
3. Treating `NULL` in a foreign key as an error; it is legal unless `NOT NULL` is also declared.
4. Using changeable data (email, name) as a primary key.
5. Testing only valid data and never testing that invalid data is rejected.
6. Deleting parent rows before child rows.

Note on dialects: `ALTER TABLE ... ADD CONSTRAINT` works in PostgreSQL, MySQL and SQL Server. SQLite cannot add a foreign key to an existing table that way (you recreate the table). Constraint syntax in `CREATE TABLE` is otherwise very similar across systems.

## Practice Questions

**Q1.** What is the difference between a primary key and a `UNIQUE` column?

**Q2.** Write a `CREATE TABLE demo_tests` with: an auto-numbered `test_id` primary key, a required `title`, a `priority` that must be between 1 and 5, and a `status` defaulting to `'new'`. Insert one valid row, then show a row rejected by the CHECK.

**Q3.** `PRAGMA foreign_key_check` reported `orders | 107`. In one sentence, what is wrong with order 107?

**Q4.** Can an order have `customer_id = NULL`? Is that an orphan?

**Q5.** Which delete order is correct for removing customer 3 and all their data: `customers -> orders -> order_items`, or `order_items -> orders -> customers`?

### Answers

**A1.** A table has exactly one primary key (unique, not NULL, identifies the row and is what other tables reference). A table can have many `UNIQUE` columns, and those may allow NULL (usually many NULLs). A primary key is the row's identity; `UNIQUE` is an additional business rule such as "email is not reused".

**A2.**

```sql
CREATE TABLE demo_tests (
    test_id  INTEGER PRIMARY KEY,
    title    TEXT NOT NULL,
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    status   TEXT DEFAULT 'new'
);

INSERT INTO demo_tests (title, priority) VALUES ('Login works', 2);
INSERT INTO demo_tests (title, priority) VALUES ('Bad priority', 9);

SELECT * FROM demo_tests;
```

**Result:**

```text
OK

OK: 1 row(s) affected

Error: CHECK constraint failed: priority BETWEEN 1 AND 5

test_id | title       | priority | status
--------+-------------+----------+-------
1       | Login works | 2        | new
(1 row)
```

**A3.** Order 107 refers to customer 99, and no customer 99 exists in `customers`. It is an orphan child row.

**A4.** Yes, if the FK column allows NULL. NULL means "no parent", so it is not an orphan; it is a guest order. An orphan has a non-NULL value that matches no parent.

**A5.** `order_items -> orders -> customers`: children first, then parents. (Customer 3's payments would also be deleted before orders if they had any.) Reverse order fails with a foreign key error when enforcement is on.

```sql
DROP TABLE demo_tests;
```

**Result:**

```text
OK
```

## Summary / Key Takeaways

- Constraints are rules the database enforces, so bad data is refused at the door.
- A **primary key** uniquely identifies each row (unique + not NULL, one per table); we use surrogate integer IDs.
- A **foreign key** links a child column to a parent's key and provides referential integrity; it may be NULL.
- `NOT NULL`, `UNIQUE`, `CHECK` and `DEFAULT` add further guardrails.
- SQLite does not enforce foreign keys until `PRAGMA foreign_keys = ON`; our planted orphans exist because of that, as legacy imports do in real life.
- `PRAGMA foreign_key_check` lists existing FK violations; `ON DELETE CASCADE / SET NULL / RESTRICT` define what happens to children.
- Missing constraints (no UNIQUE on email, no CHECK on quantity) explain several planted bugs and are legitimate QA findings.
- Joins, the next topic, work by matching foreign keys to primary keys.

## Additional Resources

- SQLite documentation, Foreign Key Support: https://www.sqlite.org/foreignkeys.html
- SQLite documentation, CREATE TABLE (constraints): https://www.sqlite.org/lang_createtable.html
- PostgreSQL documentation, Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
