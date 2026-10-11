# Relational Database Concepts

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a database is, and why applications store data in databases rather than in loose files.
- Describe the relational model using the words **table**, **row**, **column**, **schema**, and **RDBMS**, and map each one to something you already know (a spreadsheet, a CSV file).
- Recognise the common SQL data types and understand why every column has one.
- Explain what **NULL** means and why it is not the same as zero or an empty string.
- Describe, at a conceptual level, what **primary keys** and **foreign keys** are and why relational databases split data across several tables.
- Name the major RDBMS products (SQLite, MySQL, PostgreSQL, SQL Server, Oracle) and explain how they differ at a high level.
- Set up the small `orders` practice database that we will reuse for the rest of Thursday, and run your first query against it.
- Explain why a QA / test automation engineer needs to read from databases.

## Why This Matters

Look at the Weekly Epic for Week 2: you are hardening your Python, learning collaborative Git, and then **adding SQL for QA data validation**. Monday to Wednesday you learned to write modular, tested Python. Today we add the second half of that sentence.

Almost every real application you will test, whether it is an online shop, a banking portal, a hospital system, or a mobile app, keeps its important data in a relational database. When a tester clicks "Place Order" on a web page, the interesting question is not only "did the page say *Thank you*?" but also:

- Did exactly **one** order row get created?
- Is the **quantity** stored correctly?
- Is the order **status** `PENDING` as the requirements say?
- Did the system accidentally store a **negative quantity** or a **missing email**?

The user interface can lie, or at least hide problems. The database is where the truth lives. A QE (Quality Engineering) professional who can open the database and check the data directly can find bugs that UI-only testers miss, can prepare test data quickly, and can verify that automated tests actually changed the system state they claim to have changed.

This also feeds directly into **Project 1: QE Foundations**. Today's project milestone is a set of *data validation queries*. Before you can write those queries you need a mental model of what a relational database is. That is the goal of this first lesson. It contains no heavy syntax, only the vocabulary and ideas that everything else builds on.

> **Prior-knowledge note.** On Tuesday you read and wrote CSV files with Python. A CSV file is a good stepping stone: it is a table of rows and columns stored as text. A relational database is that idea made much more powerful, safer and faster.

---

## The Concept

### 1. What is a database?

A **database** is an organised collection of data that is stored so it can be **searched, changed, and protected** by software.

Think about a paper filing cabinet in an office. Each drawer holds folders, each folder holds sheets of paper in a known format. If you want the invoice for customer "Alice", you do not read every sheet in the building. You go to the right drawer, the right folder, and find it. A database does the same thing for software, but at a speed of thousands or millions of look-ups per second, and with rules that stop people putting the wrong thing in the wrong place.

The software that manages a database for you is called a **Database Management System (DBMS)**. When the database is *relational* (we will define that in a moment) the software is called an **RDBMS**, a Relational Database Management System.

#### Why not just use files (CSV, JSON, Excel)?

You have already worked with files, so it is fair to ask why applications do not just save their data in CSV or JSON files. Here is what goes wrong when real applications try that:

| Problem | Example with a plain CSV file | How an RDBMS helps |
|---|---|---|
| **Concurrent access** | Two users place orders at the same moment and both programs try to write to `orders.csv`. One overwrites the other. | The RDBMS coordinates simultaneous readers and writers safely. |
| **Speed on large data** | To find one order among 10 million, the program must read the file line by line. | The RDBMS can use indexes (like the index at the back of a book) to jump straight to the answer. |
| **No rules** | Nothing stops someone typing `abc` into a quantity column. | Columns have data types and rules. |
| **Querying** | Every question needs new Python code. | You ask questions in one standard language, SQL. |
| **Partial failures** | A crash in the middle of saving leaves a half-written file. | Transactions ensure that a change either happens completely or not at all. |
| **Security** | Anyone who can read the file can read everything. | Accounts and permissions control who can see or change what. |

That does not mean files are bad. CSV and JSON are excellent for exchanging data and for test fixtures. But for the **system of record** of a serious application, a database is the standard choice.

### 2. The relational model: tables, rows and columns

In 1970 a computer scientist named E. F. Codd proposed storing data in **relations**, which in everyday language we call **tables**. This idea is the basis of nearly every mainstream database in business today.

#### The table

A **table** holds data about **one kind of thing**. A shop database might have a `customers` table, a `products` table, and an `orders` table. Each table is a grid:

- The **columns** (also called *fields* or *attributes*) run vertically and define **what facts** we store.
- The **rows** (also called *records* or *tuples*) run horizontally and each one is **one instance** of the thing.

Here is a tiny `orders` table drawn as a grid:

| order_id | customer_name | product | quantity | status |
|---|---|---|---|---|
| 1001 | Alice Johnson | Laptop | 1 | DELIVERED |
| 1002 | Bob Smith | Wireless Mouse | 2 | SHIPPED |
| 1003 | Carla Gomez | USB-C Cable | 5 | DELIVERED |

- `order_id`, `customer_name`, `product`, `quantity`, and `status` are **columns**. Together they describe the *structure* of the table.
- The row starting with `1002` is **one record**: Bob Smith ordered 2 Wireless Mice and the order has shipped.
- A single cell, for example the value `SHIPPED`, sits at the intersection of one row and one column. It is the smallest piece of data.

#### Spreadsheet analogy

If you have used Excel or Google Sheets you already understand 80 percent of this:

| Spreadsheet term | Database term |
|---|---|
| Worksheet / tab | Table |
| Header row (column titles) | Column names |
| Each following row | Row / record |
| Cell | Value (a single field in a record) |
| Whole workbook | Database |

But a database table is stricter than a spreadsheet. In a spreadsheet you can type text in a number column, merge cells, or leave a hole in the middle. In a database table every column has a **fixed data type** and every row has **exactly the same columns**. This strictness is a feature: it makes data predictable, and predictable data is testable data.

#### Important properties of tables

1. **Every row has the same columns.** You cannot have an order row with an extra column that other rows lack. If something does not apply, the cell holds NULL (see below).
2. **Column names are unique within a table.** You cannot have two columns both called `status`.
3. **Each cell holds one value.** You do not put "Laptop, Mouse, Keyboard" in one `product` cell. If an order has three products, the design splits that into more rows or another table.
4. **Rows are conceptually unordered.** This is a major beginner surprise. A table is a *set* of rows. Unless you explicitly ask for an order (we will learn `ORDER BY` later today), the database is free to return rows in any order. You may *see* them in insertion order on your laptop, but you must never rely on that in a test.
5. **Row identity.** Each row should be uniquely identifiable, usually by a key column (see section 6).

### 3. Data types

Every column in a relational table is declared with a **data type** that restricts what it can store. The type matters for storage, for correct comparisons (is `10` bigger than `9`? As numbers yes, as text no, because `'10'` sorts before `'9'`), and for validation.

Here are the main families. Exact names differ between products, so the table gives the common names:

| Family | Typical type names | Example values | Notes |
|---|---|---|---|
| Whole numbers | `INTEGER`, `INT`, `BIGINT`, `SMALLINT` | `42`, `-1`, `0` | No decimal point. |
| Exact decimals | `DECIMAL(p,s)`, `NUMERIC(p,s)` | `1200.00`, `9.99` | Preferred for money. `DECIMAL(10,2)` means up to 10 digits in total, 2 after the point. |
| Approximate decimals | `REAL`, `FLOAT`, `DOUBLE PRECISION` | `3.14159` | Fast but can have tiny rounding errors. Avoid for currency in production. |
| Text | `VARCHAR(n)`, `CHAR(n)`, `TEXT` | `'Alice'`, `'USA'` | `VARCHAR(50)` holds up to 50 characters. |
| Dates and times | `DATE`, `TIME`, `TIMESTAMP` / `DATETIME` | `'2025-01-05'` | Standard format is year-month-day. |
| True / false | `BOOLEAN` (MySQL: `TINYINT(1)`; SQL Server: `BIT`) | `TRUE`, `FALSE` | Dialects differ. |

**Dialect note.** Our practice engine, **SQLite**, is unusual: it uses *type affinity*, meaning a column's declared type is more of a preference than a strict rule, and it has no true `DATE` type (dates are stored as text such as `'2025-01-05'`, numbers, or Julian values). MySQL, PostgreSQL and SQL Server are all much stricter. In our `orders` table we store `order_date` as ISO text (`YYYY-MM-DD`), which has a handy property: text in this format sorts in chronological order. In production databases you would declare the column `DATE`. Everything we write today works either way.

**QA connection.** Data type problems are a classic source of defects: a price stored as text, a phone number stored as an integer (which drops a leading zero), a date stored in `DD/MM/YYYY` in one row and `MM/DD/YYYY` in another. Knowing the data types lets you recognise these bugs.

### 4. NULL: the "no value" marker

Sometimes a fact is **unknown, missing, or not applicable**. A customer might not have given an email address. A shipment might not yet have a delivery date. Relational databases represent "no value here" with a special marker called **NULL**.

This is one of the most important and most misunderstood ideas in SQL, so read this carefully:

- NULL is **not** the number `0`. A quantity of `0` is a known value (nothing ordered). A NULL quantity means "we do not know".
- NULL is **not** an empty string `''`. An empty string is a known text of length zero. NULL is the absence of any text.
- NULL is **not** the text `'NULL'`. (Yes, test data sometimes contains this by mistake. That is a bug worth catching.)
- Because NULL means "unknown", comparing anything to it gives an unknown answer, not true or false. This is why `email = NULL` never works and why SQL has the special test `IS NULL`. We will explore this thoroughly in the Filtering lesson.

In our practice data, orders `1004` and `1014` have a NULL `email`.

### 5. Schemas

The word **schema** is used in two related ways, which confuses many beginners.

**Meaning 1: the structure (blueprint) of the data.** The schema of a table is its definition: the table name, the columns, each column's data type, and the rules. When someone asks, "Has the schema changed?" they mean "Have tables or columns been added, removed, or modified?" For QA, schema changes are important because they break queries and tests.

For our table the schema is:

```text
orders(order_id, customer_name, email, product, category,
       quantity, unit_price, status, order_date, country)
```

**Meaning 2: a named container (namespace) for tables.** In PostgreSQL and SQL Server a database can contain several schemas, for example `public`, `sales`, `hr`. A table is then referred to as `sales.orders`. This keeps things tidy, like folders on a disk. In MySQL, "schema" is simply a synonym for "database". SQLite has no separate schemas in this sense.

| Product | What "schema" means in practice |
|---|---|
| PostgreSQL | Namespace inside a database (default: `public`) |
| SQL Server | Namespace inside a database (default: `dbo`) |
| MySQL | Same thing as the database |
| SQLite | No schemas; one set of tables per database file |
| Oracle | A schema is tied to a user account |

Hierarchy (from largest to smallest): **server, database, schema, table, row, column/cell**.

### 6. Keys (conceptual introduction only)

If a table is a *set* of rows, we need a dependable way to point to exactly one row. For example, two customers might both be named "John Smith". Which one do we mean?

A **primary key** is a column (or set of columns) whose value **uniquely identifies each row** and is never NULL. In our table, `order_id` is the primary key: `1001` is Alice's laptop order and no other row can have that number. Primary keys are the "ID card" of a row.

A **foreign key** is a column in one table that **refers to the primary key of another table**. It is how tables are linked. We say tables are *related*, and that is where the name "relational database" comes from.

Why would you split data into several tables at all? Imagine our `orders` table. Alice ordered twice (orders `1001` and `1009`). In our single teaching table her name and email are typed twice. If she changes her email, we must update every row, and if we miss one the data is inconsistent. A real shop avoids this by storing each customer **once** in a `customers` table and having each order carry just a `customer_id` pointing at that record:

```text
customers                          orders
+-------------+-------------+      +----------+-------------+------------+
| customer_id | name        |      | order_id | customer_id | product    |
+-------------+-------------+      +----------+-------------+------------+
| 1           | Alice       |<-----| 1001     | 1           | Laptop     |
| 2           | Bob         |<--+  | 1009     | 1           | Headphones |
+-------------+-------------+   +--| 1002     | 2           | Mouse      |
                                   +----------+-------------+------------+
   customer_id is the PRIMARY KEY      customer_id here is a FOREIGN KEY
   of customers                         pointing back at customers
```

Splitting data this way to avoid repetition is called **normalisation**. It is a design topic you will meet later.

> **Anti-spoiler note.** Today we deliberately work with a **single table** so we can concentrate on reading and filtering data. Keys and constraints (including how to define and enforce primary and foreign keys) and the technique of **combining tables with JOINs** are covered in depth **on Friday**. For now you only need the idea: *a primary key identifies a row; a foreign key links to another table's row.*

### 7. Relationships between tables (just the idea)

When two tables are linked by keys, the link is a **relationship**. There are three kinds you will hear about:

- **One-to-many.** One customer has many orders. (By far the most common.)
- **Many-to-many.** Many students attend many courses. (Usually modelled using a third "linking" table.)
- **One-to-one.** One user has one profile record. (Rare.)

You do not need to model these today. Just be aware that when your single-table queries seem to be missing information such as the customer's phone number, it is probably stored in another table, and Friday's lessons will teach you how to bring it in.

### 8. RDBMS: the software behind the tables

An **RDBMS** is the program that stores tables on disk, lets many users connect, enforces rules, and answers SQL questions. Think of it as a very diligent librarian: you hand a written request (SQL) to the librarian, who finds the books (rows), checks your library card (permissions), and hands back exactly what you asked for.

Popular RDBMS products:

| Product | Typical use | Architecture | Notes for testers |
|---|---|---|---|
| **SQLite** | Mobile apps, browsers, local tools, teaching | A single file; no server | Zero setup. We use it for practice because it needs nothing installed beyond Python. |
| **MySQL / MariaDB** | Web applications (WordPress, many startups) | Client / server | Very common in web QA. Default text comparisons are case-insensitive. |
| **PostgreSQL** | Modern web back-ends, analytics | Client / server | Strict, standards-focused, rich features. Text comparison is case-sensitive. |
| **Microsoft SQL Server** | Enterprise Windows / .NET shops | Client / server | Uses T-SQL dialect (`TOP` instead of `LIMIT`). |
| **Oracle Database** | Large enterprises, banks, telecoms | Client / server | Own dialect (PL/SQL). `FETCH FIRST n ROWS ONLY` for limiting. |

**Client / server** means the database software runs as a service (often on another machine) and you connect to it with a client tool such as `psql`, MySQL Workbench, SQL Server Management Studio, DBeaver, or code in your test framework. **SQLite** instead is *embedded*: the database is just a file that your program opens directly.

**The good news:** all of these speak **SQL**, the Structured Query Language, which has been standardised (ANSI/ISO SQL) since the 1980s. Roughly 90 percent of what you learn today works unchanged on all of them. The remaining 10 percent is **dialect differences**, and we will flag those as we go.

### 9. The families of SQL commands

SQL statements fall into groups. You do not need to memorise these, but it helps to know where today fits.

| Group | Name | Purpose | Examples | When we cover it |
|---|---|---|---|---|
| **DQL** | Data Query Language | Read data | `SELECT` | **Today** |
| **DDL** | Data Definition Language | Define structure | `CREATE TABLE`, `ALTER`, `DROP` | Only `CREATE TABLE` as setup today |
| **DML** | Data Manipulation Language | Change data | `INSERT`, `UPDATE`, `DELETE` | **Friday** |
| **DCL** | Data Control Language | Permissions | `GRANT`, `REVOKE` | Later / by DBAs |
| **TCL** | Transaction Control Language | Group changes | `COMMIT`, `ROLLBACK` | Later |

Today is almost entirely **read-only**: we look at data but do not change it. This is excellent for a QA person, because read-only queries are safe. You can explore a test database without any risk of damaging it.

### 10. Where do QA engineers meet databases?

Here are realistic situations where a tester or test automation engineer opens a database:

1. **Verifying the back end after a UI or API test.** The automated test submits the "Place Order" form, then queries the `orders` table to confirm the row exists with the right values.
2. **Preparing test data.** "I need three customers from Canada with PENDING orders." You query for existing ones or create them.
3. **Investigating a defect.** A user reports a wrong total. You find the row and look at the stored values to decide if the bug is in the UI, the API, or the data.
4. **Data migration testing.** After moving from an old system to a new one, you compare record counts and values.
5. **Reporting and monitoring tests.** Checking that a nightly job loaded yesterday's data.
6. **Test environment health.** Confirming the database really contains the baseline data a suite expects.

A quick mental checklist for QA data work is **"Completeness, Correctness, Consistency, Uniqueness, Validity"**: is everything there, is it right, does it agree with itself, is each thing stored once, and does it follow the rules? We will build queries for each of these by the end of the day.

---

## Setting Up Our Practice Database

For all of Thursday's lessons we use **one small table** called `orders`, from an imaginary online electronics shop. Every example, exercise and answer in the day's materials uses these same 15 rows, so you can compare your results with ours.

### How to run the examples

You have three equally good options. Use whichever is easiest in your environment.

**Option A: Python's built-in `sqlite3` module (nothing to install).** You met Python modules on Monday; `sqlite3` is a built-in module. Python is used here **only as a launcher**, because SQLite is bundled with Python. The SQL itself is what you are learning.

```python
import sqlite3

# Create (or open) a database file; use ":memory:" for a throw-away database
conn = sqlite3.connect("shop.db")

# Read our setup script and run all of its statements
with open("setup.sql") as f:
    conn.executescript(f.read())

# Run a query and print the rows
for row in conn.execute("SELECT * FROM orders LIMIT 3;"):
    print(row)

conn.close()
```

Line by line:

- `import sqlite3` loads the built-in module that talks to SQLite.
- `sqlite3.connect("shop.db")` opens the database file `shop.db`, creating it if needed, and returns a **connection** object.
- `executescript(...)` runs a whole script that contains many SQL statements separated by semicolons.
- `conn.execute("SELECT ...")` runs one statement and returns a **cursor**, which you can loop over to receive rows as Python tuples.
- `conn.close()` releases the file.

**Option B: the `sqlite3` command-line tool** (preinstalled on macOS and many Linux distributions, a small download on Windows). Run `sqlite3 shop.db`, then paste the setup script and type your queries. Useful commands are `.headers on`, `.mode column`, and `.quit`.

**Option C: a graphical tool** such as *DB Browser for SQLite* or *DBeaver*. These give you a window to type queries and see results as a grid.

> **Note:** If you set up the table twice you will see `table orders already exists`. Delete `shop.db` or use `:memory:` and run the script again.

### The setup script

Below is the complete script. The `CREATE TABLE` statement defines the structure. The `INSERT` statement loads the sample rows. Today you only need to *run* the script. We explain `INSERT` (and the rest of data-changing SQL) properly on Friday, but the `CREATE TABLE` part is worth reading now because it ties straight back to this lesson.

```sql
CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    email          TEXT,
    product        TEXT NOT NULL,
    category       TEXT,
    quantity       INTEGER,
    unit_price     REAL,
    status         TEXT,
    order_date     TEXT,
    country        TEXT
);

INSERT INTO orders VALUES
(1001, 'Alice Johnson',  'alice.j@example.com',  'Laptop',          'Electronics', 1, 1200.00, 'DELIVERED', '2025-01-05', 'USA'),
(1002, 'Bob Smith',      'bob.smith@example.com','Wireless Mouse',  'Accessories', 2,   25.50, 'SHIPPED',   '2025-01-07', 'USA'),
(1003, 'Carla Gomez',    'carla.g@example.com',  'USB-C Cable',     'Accessories', 5,    9.99, 'DELIVERED', '2025-01-10', 'Canada'),
(1004, 'David Lee',      NULL,                   'Monitor',         'Electronics', 1,  300.00, 'PENDING',   '2025-01-12', 'USA'),
(1005, 'Emma Wilson',    'emma.w@example.com',   'Keyboard',        'Accessories', 1,   80.00, 'CANCELLED', '2025-01-15', 'UK'),
(1006, 'Frank Moore',    'frank.moore@example',  'Laptop',          'Electronics', 2, 1150.00, 'SHIPPED',   '2025-01-20', 'Canada'),
(1007, 'Grace Kim',      'grace.k@example.com',  'Webcam',          'Electronics', 0,   49.99, 'PENDING',   '2025-02-01', 'USA'),
(1008, 'Henry Adams',    'henry.a@example.com',  'Desk Lamp',       'Home Office', 3,   19.99, 'delivered', '2025-02-03', 'UK'),
(1009, 'Alice Johnson',  'alice.j@example.com',  'Headphones',      'Electronics', 1,  150.00, 'DELIVERED', '2025-02-10', 'USA'),
(1010, 'Isabel Torres',  'isabel.t@example.com', 'Office Chair',    'Home Office', 1,  220.00, 'SHIPPED',   '2025-02-14', 'Mexico'),
(1011, 'Jack O''Brien',  'jack.ob@example.com',  'Wireless Mouse',  'Accessories', -1,  25.50, 'PENDING',   '2025-02-18', 'UK'),
(1012, 'Karen White',    'karen.w@example.com',  'Monitor',         'Electronics', 2,  300.00, 'DELIVERED', '2025-03-02', 'USA'),
(1013, 'Liam Chen',      'liam.c@example.com',   'USB-C Cable',     'Accessories', 10,   9.99, 'SHIPPED',   '2025-03-05', 'Canada'),
(1014, 'Maria Lopez',    NULL,                   'Standing Desk',   'Home Office', 1,  450.00, 'PENDING',   '2025-03-09', 'Mexico'),
(1015, 'Noah Brown',     'noah.b@example.com',   'Keyboard',        'Accessories', 1,    0.00, 'DELIVERED', '2025-03-12', 'USA');
```

### Reading the CREATE TABLE statement

```sql
CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    email          TEXT,
    ...
);
```

- `CREATE TABLE orders (...)` tells the database to create a new table named `orders`. The column definitions go inside the parentheses, separated by commas.
- `order_id INTEGER PRIMARY KEY` creates a column named `order_id` that stores whole numbers and is the **primary key**. Each row's `order_id` must be unique and non-NULL. (Keys and constraints in depth: Friday.)
- `customer_name TEXT NOT NULL` creates a text column and says a value is **required**: you cannot store NULL here. `NOT NULL` is a simple example of a **constraint**, a rule the database enforces.
- `email TEXT` has no `NOT NULL`, so NULL is allowed. That is why two orders can have no email.
- `quantity INTEGER` and `unit_price REAL` store a whole number and a decimal. (In MySQL or PostgreSQL you would typically declare `unit_price DECIMAL(10,2)`.)
- `order_date TEXT` holds ISO dates. In other engines, use `DATE`.

### Column dictionary

| Column | Type | Meaning | Example |
|---|---|---|---|
| `order_id` | INTEGER, primary key | Unique id of the order | `1001` |
| `customer_name` | TEXT, required | Full name of the buyer | `Alice Johnson` |
| `email` | TEXT, may be NULL | Buyer's email | `alice.j@example.com` |
| `product` | TEXT, required | Product name | `Laptop` |
| `category` | TEXT | Product group | `Electronics`, `Accessories`, `Home Office` |
| `quantity` | INTEGER | Units ordered | `2` |
| `unit_price` | REAL (decimal) | Price per unit | `25.5` |
| `status` | TEXT | Order lifecycle state | `PENDING`, `SHIPPED`, `DELIVERED`, `CANCELLED` |
| `order_date` | TEXT (ISO date) | Date the order was placed | `2025-01-05` |
| `country` | TEXT | Shipping country | `USA`, `UK`, `Canada`, `Mexico` |

### The data

After running the script, the table contains these 15 rows. Keep this table handy, since later lessons use it to explain results.

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


Take a minute to *read* the data as a tester. Do you notice anything odd? You may spot a few suspicious values. Hold on to those thoughts: the last lesson of today, **Using SQL for QA Data Validation**, is all about finding them with queries.

### Your first query

```sql
SELECT order_id, customer_name, product
FROM orders;
```

**Result** (15 rows):

| order_id | customer_name | product |
|---|---|---|
| 1001 | Alice Johnson | Laptop |
| 1002 | Bob Smith | Wireless Mouse |
| 1003 | Carla Gomez | USB-C Cable |
| 1004 | David Lee | Monitor |
| 1005 | Emma Wilson | Keyboard |
| 1006 | Frank Moore | Laptop |
| 1007 | Grace Kim | Webcam |
| 1008 | Henry Adams | Desk Lamp |
| 1009 | Alice Johnson | Headphones |
| 1010 | Isabel Torres | Office Chair |
| 1011 | Jack O'Brien | Wireless Mouse |
| 1012 | Karen White | Monitor |
| 1013 | Liam Chen | USB-C Cable |
| 1014 | Maria Lopez | Standing Desk |
| 1015 | Noah Brown | Keyboard |


`SELECT` chooses columns, `FROM` names the table. This is the shape of nearly everything you will write today. In the next lessons we dissect it.

---

## Summary / Key Takeaways

- A **database** is an organised, software-managed collection of data. An **RDBMS** is the software that manages relational databases (SQLite, MySQL, PostgreSQL, SQL Server, Oracle).
- Data lives in **tables**. A table has **columns** (the structure: what is stored) and **rows** (the records: each one instance of the thing).
- Every column has a **data type**; every row has the same columns. This strictness is what makes data predictable and testable.
- **NULL** means "unknown / no value". It is not zero and not an empty string, and it needs special handling in queries.
- A **schema** is the blueprint of tables (and, in some products, also a namespace that groups tables).
- A **primary key** uniquely identifies a row; a **foreign key** points to a row in another table. Tables are split and linked to avoid duplication. We explore keys and JOINs in depth on Friday.
- Rows in a table have **no guaranteed order** unless you ask for one.
- SQL is a standard language, with small **dialect** differences between products.
- QA engineers use databases to verify results behind the UI, prepare data, investigate defects and validate migrations.
- Our teaching dataset is a single 15-row `orders` table, reused throughout Thursday.

---

## Practice Questions

Try these on your own first, then compare with the answers below.

**Q1.** In the `orders` table, how many columns are there, and what is each row called in database vocabulary?

**Q2.** Which column is the primary key, and why would `customer_name` be a bad choice for it?

**Q3.** A teammate says: "The `email` for order 1004 is blank, so it's an empty string." Is that necessarily true? What are the two possibilities?

**Q4.** Why would a test that depends on the first row returned from `SELECT * FROM orders` be considered fragile?

**Q5.** Suppose you had a `customers` table and an `orders` table that stores `customer_id`. Which one holds the primary key `customer_id`, and which one holds a foreign key to it?

**Q6.** (Hands-on) Run the setup script, then write a query that shows only the `product` and `status` columns of every order.

**Q7.** (Hands-on) Write a query that shows every column for every order, and note how many rows come back.

**Q8.** Name two reasons a QA engineer might look in the database after an automated UI test has passed.

### Answers

**A1.** There are **10 columns** (`order_id`, `customer_name`, `email`, `product`, `category`, `quantity`, `unit_price`, `status`, `order_date`, `country`). Each row is called a **record** (formally a *tuple*).

**A2.** The primary key is `order_id`. `customer_name` is unsuitable because names are not unique (two different people may share a name, and Alice Johnson already appears twice with different orders). Names also change and can be misspelt. A key must be unique and stable.

**A3.** No. A "blank" email could be an **empty string** (`''`, a known value that is zero characters long) or **NULL** (no value at all). They look similar in a grid but behave differently in queries. In our data it is NULL.

**A4.** Tables have no guaranteed row order. Without `ORDER BY`, the database may return rows in any order, and the order can change after data is modified, after an index is added, or on a different engine. The test should either sort explicitly or look the row up by its key.

**A5.** `customers` holds the primary key `customer_id`; `orders` holds `customer_id` as a foreign key pointing back to it (a one-to-many relationship: one customer, many orders).

**A6.**

```sql
SELECT product, status
FROM orders;
```

**Result** (15 rows):

| product | status |
|---|---|
| Laptop | DELIVERED |
| Wireless Mouse | SHIPPED |
| USB-C Cable | DELIVERED |
| Monitor | PENDING |
| Keyboard | CANCELLED |
| Laptop | SHIPPED |
| Webcam | PENDING |
| Desk Lamp | delivered |
| Headphones | DELIVERED |
| Office Chair | SHIPPED |
| Wireless Mouse | PENDING |
| Monitor | DELIVERED |
| USB-C Cable | SHIPPED |
| Standing Desk | PENDING |
| Keyboard | DELIVERED |


**A7.**

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


It returns **15 rows**. The `*` means "all columns".

**A8.** Any two of: confirm the order row was actually saved; confirm values (quantity, price, status) were stored correctly; confirm no duplicate or extra rows were created; confirm that sensitive data was handled properly; find out why a test failed; confirm the test left the data in the expected state.

---

## Additional Resources

- SQLite documentation, *Datatypes In SQLite*: https://www.sqlite.org/datatype3.html
- PostgreSQL official tutorial, *Concepts* (tables, databases, relations): https://www.postgresql.org/docs/current/tutorial-concepts.html
- PostgreSQL official tutorial, *Creating a New Table*: https://www.postgresql.org/docs/current/tutorial-table.html
