# SELECT Statements

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a `SELECT` statement does and what a **result set** is.
- Write a `SELECT ... FROM ...` query that returns **all columns** (`*`) or a **chosen list of columns**.
- Decide when `SELECT *` is acceptable and when to list columns explicitly.
- Create **aliases** for columns with `AS` to give readable headings.
- Write **calculated columns** using arithmetic, string functions and literals.
- Explain how **NULL** behaves inside expressions in a `SELECT` list.
- Qualify column names with the table name and understand why it will matter later.
- Run a `SELECT` from **Python** (`sqlite3`) and read the rows back, the way test automation does.
- Understand that `SELECT` is **read-only** and therefore safe for exploring a test database.

## Why This Matters

`SELECT` is the single most-used statement in SQL. For a QA or test automation engineer it is *the* statement: a tester inspects data far more often than they change it. Every validation check you will write this week begins as a `SELECT` that makes the data visible:

- "Show me everything the system saved for order 1004." (`SELECT *` with a condition)
- "Show only the columns I need to compare against the UI." (a column list)
- "Show me a calculated total so I can compare it to the amount on the invoice." (a calculated column)

In the Week 2 Epic you are adding SQL as a data-validation skill. Everything in the next lessons (filtering, sorting, limiting, validation rules) builds on this one clause. If you master `SELECT` and `FROM` today, adding `WHERE` and `ORDER BY` will feel natural.

Today's **Project 1 milestone** (data validation queries) will be made up of `SELECT` statements, so the habits you form now, such as listing columns deliberately, giving clear aliases, and reading your output carefully, carry straight into your project.

> **Reminder:** We use the 15-row `orders` table from *Relational Database Concepts*. The data is repeated below for convenience.

<details>
<summary>Dataset recap: the <code>orders</code> table (click to expand)</summary>

Columns: `order_id` (primary key), `customer_name`, `email`, `product`, `category`, `quantity`, `unit_price`, `status`, `order_date`, `country`.

| order_id | customer_name | email | product | category | quantity | unit_price | status | order_date | country |
|---|---|---|---|---|---|---|---|---|---|
| 1001 | Alice Johnson | alice.j@example.com | Laptop | Electronics | 1 | 1200.0 | DELIVERED | 2025-01-05 | USA |
| 1002 | Bob Smith | bob.smith@example.com | Wireless Mouse | Accessories | 2 | 25.5 | SHIPPED | 2025-01-07 | USA |
| 1003 | Carla Gomez | carla.g@example.com | USB-C Cable | Accessories | 5 | 9.99 | DELIVERED | 2025-01-10 | Canada |
| 1004 | David Lee | NULL | Monitor | Electronics | 1 | 300.0 | PENDING | 2025-01-12 | USA |
| 1005 | Emma Wilson | emma.w@example.com | Keyboard | Accessories | 1 | 80.0 | CANCELLED | 2025-01-15 | UK |
| 1006 | Frank Moore | frank.moore@example | Laptop | Electronics | 2 | 1150.0 | SHIPPED | 2025-01-20 | Canada |
| 1007 | Grace Kim | grace.k@example.com | Webcam | Electronics | 0 | 49.99 | PENDING | 2025-02-01 | USA |
| 1008 | Henry Adams | henry.a@example.com | Desk Lamp | Home Office | 3 | 19.99 | delivered | 2025-02-03 | UK |
| 1009 | Alice Johnson | alice.j@example.com | Headphones | Electronics | 1 | 150.0 | DELIVERED | 2025-02-10 | USA |
| 1010 | Isabel Torres | isabel.t@example.com | Office Chair | Home Office | 1 | 220.0 | SHIPPED | 2025-02-14 | Mexico |
| 1011 | Jack O'Brien | jack.ob@example.com | Wireless Mouse | Accessories | -1 | 25.5 | PENDING | 2025-02-18 | UK |
| 1012 | Karen White | karen.w@example.com | Monitor | Electronics | 2 | 300.0 | DELIVERED | 2025-03-02 | USA |
| 1013 | Liam Chen | liam.c@example.com | USB-C Cable | Accessories | 10 | 9.99 | SHIPPED | 2025-03-05 | Canada |
| 1014 | Maria Lopez | NULL | Standing Desk | Home Office | 1 | 450.0 | PENDING | 2025-03-09 | Mexico |
| 1015 | Noah Brown | noah.b@example.com | Keyboard | Accessories | 1 | 0.0 | DELIVERED | 2025-03-12 | USA |


</details>

---

## The Concept

### 1. What does SELECT do?

`SELECT` **retrieves data** from one or more tables and presents it as a new table called a **result set**.

Two important ideas:

1. **It only reads.** `SELECT` never changes the stored data. You can run it as often as you like without damaging anything. (Statements that change data, `INSERT`, `UPDATE`, `DELETE`, are covered on Friday.)
2. **The result is itself a table.** It has columns and rows, but it is temporary. It exists only while you look at it. It is like a photocopy of part of the cabinet, not the cabinet itself.

The simplest possible shape is:

```text
SELECT  <what to show>
FROM    <where it lives>;
```

`SELECT` is the *projection* part (which columns), `FROM` is the *source* (which table). A third clause, `WHERE`, will later decide *which rows*. Together:

| Clause | Chooses | Think of it as |
|---|---|---|
| `SELECT` | **columns** (and calculated values) | Which *vertical slices* do I want? |
| `FROM` | **table** | Where is the data? |
| `WHERE` | **rows** | Which *horizontal slices* do I want? (next lesson) |

### 2. Selecting all columns with `*`

The asterisk `*` is a wildcard meaning "every column, in the order they were defined in the table".

```sql
SELECT *
FROM orders;
```

**Result** (15 rows):

| order_id | customer_name | email | product | category | quantity | unit_price | status | order_date | country |
|---|---|---|---|---|---|---|---|---|---|
| 1001 | Alice Johnson | alice.j@example.com | Laptop | Electronics | 1 | 1200.0 | DELIVERED | 2025-01-05 | USA |
| 1002 | Bob Smith | bob.smith@example.com | Wireless Mouse | Accessories | 2 | 25.5 | SHIPPED | 2025-01-07 | USA |
| 1003 | Carla Gomez | carla.g@example.com | USB-C Cable | Accessories | 5 | 9.99 | DELIVERED | 2025-01-10 | Canada |
| 1004 | David Lee | NULL | Monitor | Electronics | 1 | 300.0 | PENDING | 2025-01-12 | USA |
| 1005 | Emma Wilson | emma.w@example.com | Keyboard | Accessories | 1 | 80.0 | CANCELLED | 2025-01-15 | UK |
| 1006 | Frank Moore | frank.moore@example | Laptop | Electronics | 2 | 1150.0 | SHIPPED | 2025-01-20 | Canada |
| 1007 | Grace Kim | grace.k@example.com | Webcam | Electronics | 0 | 49.99 | PENDING | 2025-02-01 | USA |
| 1008 | Henry Adams | henry.a@example.com | Desk Lamp | Home Office | 3 | 19.99 | delivered | 2025-02-03 | UK |
| 1009 | Alice Johnson | alice.j@example.com | Headphones | Electronics | 1 | 150.0 | DELIVERED | 2025-02-10 | USA |
| 1010 | Isabel Torres | isabel.t@example.com | Office Chair | Home Office | 1 | 220.0 | SHIPPED | 2025-02-14 | Mexico |
| 1011 | Jack O'Brien | jack.ob@example.com | Wireless Mouse | Accessories | -1 | 25.5 | PENDING | 2025-02-18 | UK |
| 1012 | Karen White | karen.w@example.com | Monitor | Electronics | 2 | 300.0 | DELIVERED | 2025-03-02 | USA |
| 1013 | Liam Chen | liam.c@example.com | USB-C Cable | Accessories | 10 | 9.99 | SHIPPED | 2025-03-05 | Canada |
| 1014 | Maria Lopez | NULL | Standing Desk | Home Office | 1 | 450.0 | PENDING | 2025-03-09 | Mexico |
| 1015 | Noah Brown | noah.b@example.com | Keyboard | Accessories | 1 | 0.0 | DELIVERED | 2025-03-12 | USA |


This returns every column of every row. In the grid above you can see all ten columns for all 15 rows.

**When `SELECT *` is a good idea:**

- Exploring an unfamiliar table for the first time ("what does this data look like?").
- Quickly eyeballing the one or two rows involved in a bug.
- Ad hoc checks you will throw away.

**When to avoid `SELECT *`:**

- **In automated tests and saved queries.** If someone later adds, removes or reorders a column, your test that reads `row[3]` silently starts reading the wrong thing. Naming the columns makes the test stable and self-documenting.
- **On large tables.** Fetching every column of millions of rows is slow and wastes network and memory.
- **When columns contain sensitive data** (passwords, personal data) that you do not need.

A good rule: *`*` for exploring, named columns for anything you keep.*

### 3. Selecting specific columns

List the columns you want, separated by commas. The result shows them **in the order you wrote them**, which can be different from the order in the table.

```sql
SELECT customer_name, product, quantity
FROM orders;
```

**Result** (15 rows):

| customer_name | product | quantity |
|---|---|---|
| Alice Johnson | Laptop | 1 |
| Bob Smith | Wireless Mouse | 2 |
| Carla Gomez | USB-C Cable | 5 |
| David Lee | Monitor | 1 |
| Emma Wilson | Keyboard | 1 |
| Frank Moore | Laptop | 2 |
| Grace Kim | Webcam | 0 |
| Henry Adams | Desk Lamp | 3 |
| Alice Johnson | Headphones | 1 |
| Isabel Torres | Office Chair | 1 |
| Jack O'Brien | Wireless Mouse | -1 |
| Karen White | Monitor | 2 |
| Liam Chen | USB-C Cable | 10 |
| Maria Lopez | Standing Desk | 1 |
| Noah Brown | Keyboard | 1 |


Things to notice:

- Only three columns appear. The other seven exist in the table but are not part of this result.
- All 15 rows came back, because there is no `WHERE` clause.
- There is **no comma after the last column** (before `FROM`). A trailing comma is a syntax error.

You can also change the order or repeat a column:

```sql
SELECT status, order_id, order_id
FROM orders
WHERE order_id <= 1002;
```

**Result** (2 rows):

| status | order_id | order_id |
|---|---|---|
| DELIVERED | 1001 | 1001 |
| SHIPPED | 1002 | 1002 |


(We used a small `WHERE` just to keep the output short. It is explained in the next lesson. Notice that the repeated column simply appears twice.)

#### Why choose columns deliberately?

When you are validating data against the application, you rarely need everything. Suppose the UI order confirmation page shows the product, quantity and unit price. Select exactly those columns so you can place them side by side with the screen:

```sql
SELECT order_id, product, quantity, unit_price
FROM orders
WHERE order_id = 1002;
```

**Result** (1 row):

| order_id | product | quantity | unit_price |
|---|---|---|---|
| 1002 | Wireless Mouse | 2 | 25.5 |


### 4. Column aliases with `AS`

An **alias** gives a column a different name *in the result*. The underlying table is untouched.

```sql
SELECT order_id    AS id,
       customer_name AS customer,
       unit_price  AS price
FROM orders
WHERE order_id <= 1003;
```

**Result** (3 rows):

| id | customer | price |
|---|---|---|
| 1001 | Alice Johnson | 1200.0 |
| 1002 | Bob Smith | 25.5 |
| 1003 | Carla Gomez | 9.99 |


Why use aliases?

- **Readable headings.** Reports and test logs are clearer with `customer` than with `customer_name`.
- **Naming calculated columns.** An expression like `quantity * unit_price` has no natural name. Without an alias, the engine invents an ugly heading (such as `quantity * unit_price`).
- **Matching expected names.** If your test compares the result to a dictionary or a CSV whose headers are `Order ID`, aliasing makes the keys line up.

**Syntax details:**

- `AS` is optional in most dialects (`order_id id` works), but writing it makes the code clearer and avoids the accidental-alias bug you saw in the previous lesson (a forgotten comma silently turns the next column into an alias). Oracle allows `AS` for columns but not for table aliases.
- If the alias contains spaces or mixed case you want to keep, quote it with double quotes (or brackets in SQL Server, backticks in MySQL):

```sql
SELECT order_id AS "Order Number",
       customer_name AS "Customer Name"
FROM orders
WHERE order_id = 1001;
```

**Result** (1 row):

| Order Number | Customer Name |
|---|---|
| 1001 | Alice Johnson |


### 5. Calculated columns (expressions in the SELECT list)

The `SELECT` list can contain more than column names. It can contain any **expression**: arithmetic, functions, literals.

#### Arithmetic

```sql
SELECT order_id,
       product,
       quantity,
       unit_price,
       quantity * unit_price AS line_total
FROM orders;
```

**Result** (15 rows):

| order_id | product | quantity | unit_price | line_total |
|---|---|---|---|---|
| 1001 | Laptop | 1 | 1200.0 | 1200.0 |
| 1002 | Wireless Mouse | 2 | 25.5 | 51.0 |
| 1003 | USB-C Cable | 5 | 9.99 | 49.95 |
| 1004 | Monitor | 1 | 300.0 | 300.0 |
| 1005 | Keyboard | 1 | 80.0 | 80.0 |
| 1006 | Laptop | 2 | 1150.0 | 2300.0 |
| 1007 | Webcam | 0 | 49.99 | 0.0 |
| 1008 | Desk Lamp | 3 | 19.99 | 59.97 |
| 1009 | Headphones | 1 | 150.0 | 150.0 |
| 1010 | Office Chair | 1 | 220.0 | 220.0 |
| 1011 | Wireless Mouse | -1 | 25.5 | -25.5 |
| 1012 | Monitor | 2 | 300.0 | 600.0 |
| 1013 | USB-C Cable | 10 | 9.99 | 99.9 |
| 1014 | Standing Desk | 1 | 450.0 | 450.0 |
| 1015 | Keyboard | 1 | 0.0 | 0.0 |


For each row, the database multiplies that row's `quantity` and `unit_price`. Check some by hand: order `1002` is 2 × 25.50 = 51.0; order `1003` is 5 × 9.99 = 49.95.

Interesting observations as a tester:

- Order `1007` has a `line_total` of **0.0**, because the quantity is 0. Is it valid to have an order of zero items? That looks like a bug.
- Order `1011` has a **negative** line total (-25.5), because its quantity is -1. A negative order quantity is almost certainly invalid.
- Order `1015` has a line total of **0.0** because its unit price is 0.00. Is a free keyboard intentional?

You have just found three suspicious rows without writing any filter, only by selecting a calculated column and reading it carefully. This is the spirit of data validation.

**Number formatting differs by engine.** SQLite prints `1200.0`; PostgreSQL with a `NUMERIC(10,2)` column would show `1200.00`; MySQL similar. The values are the same, only the display differs. If your test compares text output, be aware of that.

#### Rounding

Decimal arithmetic can produce long fractions. `ROUND(value, digits)` tidies them:

```sql
SELECT order_id,
       unit_price,
       ROUND(unit_price * 1.0825, 2) AS price_with_tax
FROM orders
WHERE order_id IN (1002, 1003, 1008);
```

**Result** (3 rows):

| order_id | unit_price | price_with_tax |
|---|---|---|
| 1002 | 25.5 | 27.6 |
| 1003 | 9.99 | 10.81 |
| 1008 | 19.99 | 21.64 |


Here `1.0825` represents 8.25% tax purely as an example. (Money in real systems should use exact `DECIMAL` types rather than floating-point `REAL`, because binary floating-point cannot represent values like 0.1 exactly. That is a classic source of one-cent defects.)

#### String expressions

You can build text from several columns with the concatenation operator `||` (SQLite, PostgreSQL, Oracle; use `CONCAT()` in MySQL, `+` or `CONCAT()` in SQL Server):

```sql
SELECT order_id,
       customer_name || ' <' || email || '>' AS contact
FROM orders
WHERE order_id IN (1001, 1002);
```

**Result** (2 rows):

| order_id | contact |
|---|---|
| 1001 | Alice Johnson <alice.j@example.com> |
| 1002 | Bob Smith <bob.smith@example.com> |


Functions work too:

```sql
SELECT order_id,
       UPPER(country) AS country_upper,
       LENGTH(product) AS product_name_length
FROM orders
WHERE order_id <= 1003;
```

**Result** (3 rows):

| order_id | country_upper | product_name_length |
|---|---|---|
| 1001 | USA | 6 |
| 1002 | USA | 14 |
| 1003 | CANADA | 11 |


#### Literals as columns

A constant can be a column. It is repeated for every row. This is useful for labelling the output of several queries you plan to combine or compare:

```sql
SELECT order_id,
       'orders' AS source_table,
       1 AS check_number
FROM orders
WHERE order_id <= 1002;
```

**Result** (2 rows):

| order_id | source_table | check_number |
|---|---|---|
| 1001 | orders | 1 |
| 1002 | orders | 1 |


#### A SELECT with no table

If you just need to calculate something, many engines let you omit `FROM`:

```sql
SELECT 2 + 3 AS five, 'hello' AS greeting, 10 / 4 AS integer_division;
```

**Result** (1 row):

| five | greeting | integer_division |
|---|---|---|
| 5 | hello | 2 |


Handy for testing a function in isolation (Oracle needs `FROM dual`). Notice that `10 / 4` is `2`, not `2.5`, because both numbers are integers in SQLite, PostgreSQL and SQL Server.

### 6. NULL inside expressions

Recall from *Relational Database Concepts*: NULL means "unknown". What is "unknown + 1"? Still unknown. So **any arithmetic or concatenation involving NULL produces NULL**.

Orders `1004` and `1014` have a NULL email. Watch what happens when we concatenate:

```sql
SELECT order_id,
       email,
       customer_name || ' <' || email || '>' AS contact
FROM orders
WHERE order_id IN (1003, 1004, 1014);
```

**Result** (3 rows):

| order_id | email | contact |
|---|---|---|
| 1003 | carla.g@example.com | Carla Gomez <carla.g@example.com> |
| 1004 | NULL | NULL |
| 1014 | NULL | NULL |


For the rows with no email the entire `contact` becomes NULL, not just the missing part, because "unknown text glued to known text" is unknown.

Two ways to handle this, depending on what you want:

1. **Show a default** using `COALESCE(value, replacement)`, which returns the first non-NULL argument:

```sql
SELECT order_id,
       customer_name || ' <' || COALESCE(email, 'no email') || '>' AS contact
FROM orders
WHERE order_id IN (1003, 1004, 1014);
```

**Result** (3 rows):

| order_id | contact |
|---|---|
| 1003 | Carla Gomez <carla.g@example.com> |
| 1004 | David Lee <no email> |
| 1014 | Maria Lopez <no email> |


2. **Leave it NULL on purpose** if you *want* the gap to be visible during validation.

**Dialect note:** In **Oracle**, an empty string `''` is treated as NULL, unlike all other major databases. In **MySQL**, `CONCAT(a, NULL)` also returns NULL, while in **SQL Server** the `CONCAT()` *function* treats NULL as an empty string (but the `+` operator returns NULL by default). Always test null-handling on your actual engine.

### 7. Qualifying column names with the table name

You can write a column as `table_name.column_name`:

```sql
SELECT orders.order_id, orders.product, orders.status
FROM orders
WHERE orders.order_id = 1001;
```

**Result** (1 row):

| order_id | product | status |
|---|---|---|
| 1001 | Laptop | DELIVERED |


With one table this is redundant. It becomes essential when a query uses **two or more tables that have columns with the same name**, because the database would not know which one you mean. That situation arises when you combine tables with JOINs on Friday. Developing the habit of recognising `table.column` now will make Friday easier. You can also give the *table* a short alias (`FROM orders AS o`, then `o.order_id`). We will use that in the multi-table lessons.

### 8. Everything together: reading the column order of your result

A `SELECT` statement gives you control over three things: **which columns**, **in which order**, and **with which names**. Compare these two queries that return the same data in a different presentation:

```sql
SELECT order_id, customer_name, status
FROM orders
WHERE order_id <= 1002;
```

**Result** (2 rows):

| order_id | customer_name | status |
|---|---|---|
| 1001 | Alice Johnson | DELIVERED |
| 1002 | Bob Smith | SHIPPED |


```sql
SELECT status AS order_state,
       customer_name AS buyer,
       order_id AS id
FROM orders
WHERE order_id <= 1002;
```

**Result** (2 rows):

| order_state | buyer | id |
|---|---|---|
| DELIVERED | Alice Johnson | 1001 |
| SHIPPED | Bob Smith | 1002 |


### 9. A note on `DISTINCT` and `LIMIT` (preview)

Two small additions to `SELECT` are covered fully in the next lesson, *Filtering and Sorting Data*: `DISTINCT` (remove duplicate rows from the result) and `LIMIT` (return only the first N rows). Here is just one taste so you recognise them:

```sql
SELECT DISTINCT status
FROM orders;
```

**Result** (5 rows):

| status |
|---|
| DELIVERED |
| SHIPPED |
| PENDING |
| CANCELLED |
| delivered |


`DISTINCT` returned each different status once. Look closely: you will see `delivered` and `DELIVERED` as *separate* values. Spotting that kind of inconsistency is a real validation win.

### 10. Running a SELECT from Python (how test automation does it)

Your automated tests are written in Python, so this is how you will most often execute a `SELECT`. This is **Python code that carries SQL**, because the test framework is Python. The SQL text inside is exactly what you have been learning.

```python
import sqlite3

conn = sqlite3.connect("shop.db")
conn.row_factory = sqlite3.Row   # lets us access columns by name

cursor = conn.execute(
    "SELECT order_id, customer_name, status FROM orders WHERE order_id = ?",
    (1001,),
)
row = cursor.fetchone()

assert row is not None, "Order 1001 should exist"
assert row["status"] == "DELIVERED"
print(dict(row))

conn.close()
```

Line by line:

- `sqlite3.connect("shop.db")` opens the database file.
- `conn.row_factory = sqlite3.Row` makes each row behave like a dictionary, so `row["status"]` works instead of fragile index numbers like `row[2]`. (It is the same reason we prefer named columns to `*`.)
- `conn.execute(sql, params)` runs the query. The **`?` placeholder** is replaced safely by the value `1001` from the tuple `(1001,)`. This avoids quoting bugs and SQL injection. (The trailing comma makes a one-element tuple.)
- `cursor.fetchone()` returns the next row, or `None` if there are none. `fetchall()` returns a list of all rows.
- The two `assert` statements are the validation. This is the Wednesday unit-testing skills (`assert`, clear failure messages) applied to database content.
- Other engines have similar libraries (`psycopg2` for PostgreSQL, `mysql-connector-python` for MySQL, `pyodbc` for SQL Server) with nearly the same pattern: connect, execute, fetch.

### 11. Common mistakes with SELECT

| Mistake | Symptom | Fix |
|---|---|---|
| Trailing comma before `FROM` | `syntax error near "FROM"` | Remove the last comma |
| Missing comma between two columns | One column silently becomes an alias of the other | Check headings; add the comma |
| Misspelled column | `no such column` | Compare with the schema (`SELECT * ... LIMIT 1` shows the names) |
| Using double quotes for text values | Works in SQLite by accident, fails elsewhere | Use single quotes for text |
| Relying on row order | Test passes locally, fails in CI | Add `ORDER BY` (next lesson) or look up by key |
| Assuming calculated columns are saved | Looking for `line_total` in the table | They exist only in the result |
| `SELECT *` inside automated tests | Test breaks when schema changes | List the columns |

---

## Summary / Key Takeaways

- `SELECT` **reads** data and returns a **result set**, a temporary table; it never changes the stored data.
- `SELECT *` returns all columns: good for exploring, poor for saved or automated queries.
- List specific columns to control **which** columns, their **order**, and (with `AS`) their **names**.
- The `SELECT` list can include **expressions**: arithmetic (`quantity * unit_price`), functions (`UPPER`, `LENGTH`, `ROUND`), concatenation, and literals.
- Calculated columns are computed per row **at query time** and are not stored.
- **NULL propagates**: any arithmetic or concatenation involving NULL gives NULL. `COALESCE` supplies a default.
- `table.column` qualification is optional with one table, mandatory when column names clash across tables (Friday).
- In Python tests, fetch with named columns and parameter placeholders (`?`), then `assert` on the values.
- Dialect watch-outs: number formatting, concatenation syntax, empty-string-as-NULL in Oracle, integer division.

---

## Practice Questions

**Q1.** Write a query that returns only `order_id`, `product` and `category` for every order.

**Q2.** Write a query that shows `customer_name` and `country`, renaming the columns to `buyer` and `ships_to`, for orders 1001 through 1004.

**Q3.** Write a query that calculates `quantity * unit_price` as `line_total` and also shows `order_id`, for orders 1005 to 1008.

**Q4.** Show `order_id` and the **lower-case** version of `status`, labelled `status_lower`, for orders 1007 and 1008.

**Q5.** Build a text column called `label` that looks like `1001 - Laptop` for orders 1001 and 1002.

**Q6.** For orders 1003, 1004 and 1014 show `order_id` and the `email`, replacing NULL with the text `N/A`.

**Q7.** Explain why `SELECT customer_name || email FROM orders` shows empty (NULL) results for some rows.

**Q8.** Write a query without `FROM` that computes `3 * 4`.

**Q9.** A teammate's automated test does `row[5]` on a `SELECT *` result to get the `quantity`. Give two problems with this approach and a better alternative.

**Q10.** (Challenge) Show `order_id`, `unit_price`, and a column `discounted_price` which is `unit_price` reduced by 10 percent and rounded to 2 decimals, for orders 1001, 1002 and 1003.

### Answers

**A1.**

```sql
SELECT order_id, product, category
FROM orders;
```

**Result** (15 rows):

| order_id | product | category |
|---|---|---|
| 1001 | Laptop | Electronics |
| 1002 | Wireless Mouse | Accessories |
| 1003 | USB-C Cable | Accessories |
| 1004 | Monitor | Electronics |
| 1005 | Keyboard | Accessories |
| 1006 | Laptop | Electronics |
| 1007 | Webcam | Electronics |
| 1008 | Desk Lamp | Home Office |
| 1009 | Headphones | Electronics |
| 1010 | Office Chair | Home Office |
| 1011 | Wireless Mouse | Accessories |
| 1012 | Monitor | Electronics |
| 1013 | USB-C Cable | Accessories |
| 1014 | Standing Desk | Home Office |
| 1015 | Keyboard | Accessories |


**A2.**

```sql
SELECT customer_name AS buyer, country AS ships_to
FROM orders
WHERE order_id <= 1004;
```

**Result** (4 rows):

| buyer | ships_to |
|---|---|
| Alice Johnson | USA |
| Bob Smith | USA |
| Carla Gomez | Canada |
| David Lee | USA |


**A3.**

```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE order_id >= 1005 AND order_id <= 1008;
```

**Result** (4 rows):

| order_id | line_total |
|---|---|
| 1005 | 80.0 |
| 1006 | 2300.0 |
| 1007 | 0.0 |
| 1008 | 59.97 |


**A4.**

```sql
SELECT order_id, LOWER(status) AS status_lower
FROM orders
WHERE order_id IN (1007, 1008);
```

**Result** (2 rows):

| order_id | status_lower |
|---|---|
| 1007 | pending |
| 1008 | delivered |


**A5.**

```sql
SELECT order_id || ' - ' || product AS label
FROM orders
WHERE order_id IN (1001, 1002);
```

**Result** (2 rows):

| label |
|---|
| 1001 - Laptop |
| 1002 - Wireless Mouse |


(In SQLite and PostgreSQL the number is converted to text automatically by `||`. In PostgreSQL strictly typed contexts you may need `CAST(order_id AS TEXT)`; in MySQL use `CONCAT(order_id, ' - ', product)`.)

**A6.**

```sql
SELECT order_id, COALESCE(email, 'N/A') AS email
FROM orders
WHERE order_id IN (1003, 1004, 1014);
```

**Result** (3 rows):

| order_id | email |
|---|---|
| 1003 | carla.g@example.com |
| 1004 | N/A |
| 1014 | N/A |


**A7.** For rows where `email` is NULL, concatenating anything with NULL yields NULL (unknown), so the whole expression is NULL. Use `COALESCE(email, '')` if you want an empty string instead.

**A8.**

```sql
SELECT 3 * 4 AS product;
```

**Result** (1 row):

| product |
|---|
| 12 |


**A9.** (1) `SELECT *` order depends on the table definition, so adding or reordering a column makes index 5 point at the wrong value; (2) `row[5]` is unreadable: nobody knows what it means. Better: select named columns (`SELECT order_id, quantity ...`) and use a dict-style row (`row["quantity"]`).

**A10.**

```sql
SELECT order_id,
       unit_price,
       ROUND(unit_price * 0.90, 2) AS discounted_price
FROM orders
WHERE order_id IN (1001, 1002, 1003);
```

**Result** (3 rows):

| order_id | unit_price | discounted_price |
|---|---|---|
| 1001 | 1200.0 | 1080.0 |
| 1002 | 25.5 | 22.95 |
| 1003 | 9.99 | 8.99 |


---

## Additional Resources

- PostgreSQL documentation, *Select Lists* (choosing columns, aliases, `DISTINCT`): https://www.postgresql.org/docs/current/queries-select-lists.html
- SQLite documentation, *SELECT* statement syntax: https://www.sqlite.org/lang_select.html
- Python documentation, *sqlite3 module* (cursors, placeholders, `Row` objects): https://docs.python.org/3/library/sqlite3.html
