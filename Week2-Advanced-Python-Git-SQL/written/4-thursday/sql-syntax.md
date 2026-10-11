# SQL Syntax

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what SQL is, who maintains it, and what it means that SQL is *declarative*.
- Identify the parts of a SQL statement: **keywords, identifiers, literals, operators, expressions, clauses, and the terminator**.
- Write readable, consistently formatted SQL, including **comments**.
- Use the correct quoting rules for **text, numbers, dates, NULL, and identifiers**, including how to include an apostrophe inside a text value.
- Apply **arithmetic, comparison, logical and string operators** in expressions.
- Use a few everyday **built-in functions** such as `UPPER`, `LENGTH`, `ROUND`.
- Describe the *written* order and the *logical* order in which a database processes the clauses of a query.
- Read the most common **syntax error messages** and fix the mistake they point at.
- Recognise the main **dialect differences** between SQLite, MySQL, PostgreSQL, SQL Server and Oracle.

## Why This Matters

In the previous lesson you learned what a relational database is. Now we learn the **language** used to talk to it.

For the Week 2 Epic ("add SQL for QA data validation"), SQL is the tool. Think of the way you used Python's `assert` and `unittest` on Tuesday and Wednesday: you wrote small precise statements that describe what *should* be true. SQL queries do the same job against data: "Show me every order where the quantity is not positive." The better you know the grammar of SQL, the faster you will write correct queries and the more quickly you will diagnose the ones that fail.

A tester who types SQL by trial and error often gets cryptic errors and confusing results. A tester who understands the grammar can read an error message, spot the missing comma or quote, and move on in seconds. Syntax knowledge is also what lets you review a colleague's validation query (for Project 1 you will share and review queries in pairs today) and say with confidence, "This does not do what you think it does."

> **Reminder:** Our practice table is the 15-row `orders` table created in the previous lesson (*Relational Database Concepts*). If you have not created it yet, go back and run the setup script. A condensed copy of the data is shown below so you can follow the results.

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

### 1. What is SQL?

**SQL** stands for **Structured Query Language**. People say either "S-Q-L" or "sequel"; both are accepted. It is the standard language for working with relational databases.

Key facts:

- **Standardised.** SQL is defined by the ANSI and ISO standards. Every major RDBMS implements most of that standard.
- **Dialects.** Each vendor adds its own extras and sometimes uses different spellings. These variants are called **dialects**: SQLite SQL, MySQL SQL, PostgreSQL SQL, Microsoft's **T-SQL**, Oracle's **PL/SQL**. The core of the language (`SELECT`, `WHERE`, `ORDER BY`) is shared.
- **Not case-sensitive for keywords.** `SELECT` and `select` are the same command.
- **Declarative.** This is the big idea, explained next.

#### Declarative versus procedural

In Python, you write **procedural** code: you tell the computer *how* to do something, step by step.

```python
# Python (procedural): HOW to find the pending orders
pending = []
for row in orders:
    if row["status"] == "PENDING":
        pending.append(row)
```

In SQL you are **declarative**: you describe *what* result you want, and the database decides the best way to get it.

```sql
-- SQL (declarative): WHAT we want
SELECT order_id, customer_name, status
FROM orders
WHERE status = 'PENDING';
```

**Result** (4 rows):

| order_id | customer_name | status |
|---|---|---|
| 1004 | David Lee | PENDING |
| 1007 | Grace Kim | PENDING |
| 1011 | Jack O'Brien | PENDING |
| 1014 | Maria Lopez | PENDING |


You did not say "loop over the rows" or "use an index". You only described the result. The database's **query optimiser** chooses the method. This is why SQL is both beginner-friendly (you describe what you see in your head) and powerful (the same query that runs on 15 rows can run on 15 million).

### 2. The anatomy of a SQL statement

Consider this statement:

```sql
SELECT product, quantity * unit_price AS line_total
FROM orders
WHERE status = 'SHIPPED'
ORDER BY line_total DESC;
```

**Result** (4 rows):

| product | line_total |
|---|---|
| Laptop | 2300.0 |
| Office Chair | 220.0 |
| USB-C Cable | 99.9 |
| Wireless Mouse | 51.0 |


It is made of the following building blocks:

| Building block | What it is | Examples in the query above |
|---|---|---|
| **Keyword** | A word with a special meaning in the language | `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `AS`, `DESC` |
| **Identifier** | A name *you* (or the schema designer) chose for a table, column or alias | `product`, `quantity`, `unit_price`, `orders`, `status`, `line_total` |
| **Literal** | A fixed value typed directly in the query | `'SHIPPED'` (text) |
| **Operator** | A symbol that combines or compares values | `*` (multiply), `=` (equals) |
| **Expression** | Anything that produces a value: a column, a literal, or a combination | `quantity * unit_price` |
| **Alias** | A temporary nickname for a column or table, introduced with `AS` | `line_total` |
| **Clause** | A named part of a statement that begins with a keyword | the `SELECT` clause, the `FROM` clause, the `WHERE` clause, the `ORDER BY` clause |
| **Terminator** | The semicolon `;` that ends a statement | the final `;` |

A **statement** (also called a *query* when it only reads data) is one complete command. It is made of **clauses**, and each clause is made of keywords, identifiers, literals and expressions.

#### Reading a query like a sentence

A very useful trick for beginners: read each clause as a short English instruction.

```text
SELECT product, quantity * unit_price AS line_total   -> "Show me the product and the line total..."
FROM orders                                           -> "...from the orders table..."
WHERE status = 'SHIPPED'                              -> "...but only for shipped orders..."
ORDER BY line_total DESC;                             -> "...biggest line total first."
```

If you can say your question in plain English, you can almost always translate it into SQL one clause at a time. We will practise exactly this in the *Basic Query Construction* lesson.

### 3. Case sensitivity: what matters and what does not

| Item | Case-sensitive? | Notes |
|---|---|---|
| **Keywords** (`SELECT`, `from`) | No | `select`, `Select` and `SELECT` are identical. |
| **Column and table names** | Usually no | PostgreSQL folds unquoted names to lower case; SQL Server depends on its collation; **MySQL on Linux treats table names as case-sensitive** (because they map to files). Using a consistent lower-case `snake_case` avoids all trouble. |
| **Text values** (`'SHIPPED'`) | **Depends on the product!** | See below. |

The last row is a famous trap for testers. Look at our data: order `1008` has the status `delivered` in lower case, while all others are `DELIVERED`. Is that the same value?

```sql
SELECT order_id, status
FROM orders
WHERE status = 'DELIVERED';
```

**Result** (5 rows):

| order_id | status |
|---|---|
| 1001 | DELIVERED |
| 1003 | DELIVERED |
| 1009 | DELIVERED |
| 1012 | DELIVERED |
| 1015 | DELIVERED |


In **SQLite** (and PostgreSQL, Oracle) the `=` comparison on text is **case-sensitive**, so order `1008` is *not* returned. In **MySQL** and **SQL Server**, the default collation is case-**in**sensitive, so `1008` *would* be returned. The same query gives different answers on different engines! In QA this is exactly the kind of thing that creates "works on my machine" test failures. We will return to this in the Filtering lesson and in the Data Validation lesson, where order `1008` is a deliberate planted defect.

**Style convention used in this course:**

- Keywords in **UPPER CASE** (`SELECT`, `FROM`, `WHERE`).
- Table and column names in **lower_snake_case** (`order_date`).
- One clause per line.
- A semicolon at the end of every statement.

Conventions are not required by the engine; they exist so humans can read queries quickly. Pick one and stick to it, especially when you share queries in a repository.

### 4. Whitespace and formatting

SQL ignores extra spaces, tabs, and blank lines. These three statements are identical to the database:

```sql
SELECT order_id, status FROM orders WHERE status = 'PENDING';
```

**Result** (4 rows):

| order_id | status |
|---|---|
| 1004 | PENDING |
| 1007 | PENDING |
| 1011 | PENDING |
| 1014 | PENDING |


```sql
SELECT order_id,
       status
FROM   orders
WHERE  status = 'PENDING';
```

**Result** (4 rows):

| order_id | status |
|---|---|
| 1004 | PENDING |
| 1007 | PENDING |
| 1011 | PENDING |
| 1014 | PENDING |


The second layout is much easier to read, to review in Git, and to edit later. (Remember Git from Week 1 and Wednesday: a one-clause-per-line layout produces small, clear diffs when someone changes only the `WHERE` line.)

**Rule of thumb:** If a query does not fit comfortably on one line, break it so that each clause (`SELECT`, `FROM`, `WHERE`, `ORDER BY`) starts on its own line.

### 5. Comments

Comments are notes for humans; the database ignores them. Good comments in validation queries explain **what rule is being tested and why**.

```sql
-- This is a single-line comment. Everything after the two dashes is ignored.
SELECT order_id, quantity   -- you can also put a comment at the end of a line
FROM orders
/* This is a block comment.
   It can span several lines.
   Useful for explaining the purpose of a whole query. */
WHERE quantity <= 0;
```

**Result** (2 rows):

| order_id | quantity |
|---|---|
| 1007 | 0 |
| 1011 | -1 |


**Dialect notes on comments.** `-- text` and `/* ... */` work in all five products. In **MySQL** the `--` form needs a space after the two dashes (`-- comment`), and MySQL also supports `#` for comments. A common beginner mistake is to comment out an important `WHERE` line by accident, so be careful which lines you comment!

### 6. Literals: writing values inside a query

A **literal** is a value you type directly. The quoting rules matter greatly.

| Kind of value | How to write it | Example | Notes |
|---|---|---|---|
| **Text (string)** | **Single** quotes | `'SHIPPED'`, `'Alice Johnson'` | Double quotes are for *identifiers* in standard SQL. |
| **Number** | No quotes | `42`, `-1`, `9.99` | Use `.` as the decimal point; no thousands separators. |
| **Date** | Single quotes, ISO format `YYYY-MM-DD` | `'2025-02-01'` | Dialects differ; see below. |
| **NULL** | The bare word `NULL`, no quotes | `NULL` | Not `'NULL'`! |
| **Boolean** | `TRUE` / `FALSE` in most products | `TRUE` | SQL Server uses `1` / `0` with `BIT`; SQLite uses `1` / `0`. |

#### Putting an apostrophe inside a text value

Text is wrapped in single quotes, so how do we include an apostrophe, as in the surname *O'Brien* (order `1011`)? We **double** the apostrophe:

```sql
SELECT order_id, customer_name
FROM orders
WHERE customer_name = 'Jack O''Brien';
```

**Result** (1 row):

| order_id | customer_name |
|---|---|
| 1011 | Jack O'Brien |


`'Jack O''Brien'` is read by the database as the text `Jack O'Brien`. Two single quotes in a row mean "one literal apostrophe". Do **not** use a double-quote character (`"`) to wrap text, even if some engines tolerate it.

What happens if you forget to double it?

```sql
SELECT order_id
FROM orders
WHERE customer_name = 'Jack O'Brien';
```

**Result (error in SQLite):**

```text
Error: near "Brien": syntax error
```

The database sees the text `'Jack O'`, then the unexpected word `Brien`, then an unterminated `';`. The error message differs by product, but it always involves the quote.

> **QA connection (security).** Quotes in text are also the reason for a famous class of security bugs called *SQL injection*. When test automation builds SQL by gluing strings together, a value such as `O'Brien` can break the statement. Real code uses **parameterised queries** (placeholders) so the database library handles quoting. Python's `sqlite3` module supports this with `?` placeholders, for example `conn.execute("SELECT * FROM orders WHERE order_id = ?", (1001,))`.

#### Dates

In our SQLite table dates are stored as ISO text, so comparing them with text literals works:

```sql
SELECT order_id, order_date
FROM orders
WHERE order_date >= '2025-03-01';
```

**Result** (4 rows):

| order_id | order_date |
|---|---|
| 1012 | 2025-03-02 |
| 1013 | 2025-03-05 |
| 1014 | 2025-03-09 |
| 1015 | 2025-03-12 |


The ISO layout `YYYY-MM-DD` is special: year first, then month, then day, with leading zeros. That makes alphabetical order identical to chronological order. In real engines with a `DATE` column the literal looks the same in PostgreSQL and MySQL (`'2025-03-01'`), while Oracle often prefers `DATE '2025-03-01'`. In SQL Server `'2025-03-01'` works for `DATE` columns, though `'YYYYMMDD'` is the safest format.

### 7. Identifiers and quoting them

An **identifier** is a name of a database object: table, column, alias, schema. Normally you just type it. But what if a name contains a space or equals a reserved word?

In standard SQL you wrap such names in **double quotes**. Other products use their own style:

| Product | Identifier quoting |
|---|---|
| ANSI SQL, PostgreSQL, Oracle, SQLite | `"order date"` (double quotes) |
| MySQL | `` `order date` `` (backticks) |
| SQL Server | `[order date]` (square brackets) or double quotes |
| SQLite | accepts all three styles above |

```sql
SELECT order_id AS "Order Number", customer_name AS "Customer"
FROM orders
WHERE order_id <= 1003;
```

**Result** (3 rows):

| Order Number | Customer |
|---|---|
| 1001 | Alice Johnson |
| 1002 | Bob Smith |
| 1003 | Carla Gomez |


**Reserved words.** Words like `SELECT`, `FROM`, `ORDER`, `GROUP`, `TABLE`, `USER` and `KEY` have special meaning, so you should avoid them as column names. For example, a table called `order` collides with the `ORDER BY` keyword. That is why many teams name tables in the plural (`orders`, `users`). If you ever must reference such a name, quote it. Here is what happens if you do not:

```sql
SELECT * FROM order;
```

**Result (error in SQLite):**

```text
Error: near "order": syntax error
```

**Best practice:** choose simple lower-case names with underscores and no spaces or reserved words, so you never need quoting.

### 8. Operators

Operators combine values into expressions. SQL has four groups that you need today.

#### Arithmetic operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | add | `quantity + 1` | |
| `-` | subtract | `unit_price - 1` | |
| `*` | multiply | `quantity * unit_price` | |
| `/` | divide | `unit_price / 2` | |
| `%` | remainder (modulo) | `quantity % 2` | |

```sql
SELECT order_id,
       quantity,
       unit_price,
       quantity * unit_price AS line_total
FROM orders
WHERE order_id <= 1005;
```

**Result** (5 rows):

| order_id | quantity | unit_price | line_total |
|---|---|---|---|
| 1001 | 1 | 1200.0 | 1200.0 |
| 1002 | 2 | 25.5 | 51.0 |
| 1003 | 5 | 9.99 | 49.95 |
| 1004 | 1 | 300.0 | 300.0 |
| 1005 | 1 | 80.0 | 80.0 |


`quantity * unit_price` is an **expression computed for each row**, and `AS line_total` names the computed column in the output. The `line_total` does not exist in the table; it is calculated on the fly and nothing is stored or changed.

**Integer division trap.** In SQLite, SQL Server and PostgreSQL, dividing two *integers* gives an *integer* (the decimal part is dropped). MySQL's `/` returns a decimal, and uses `DIV` for integer division.

```sql
SELECT 7 / 2 AS int_division, 7 / 2.0 AS decimal_division;
```

**Result** (1 row):

| int_division | decimal_division |
|---|---|
| 3 | 3.5 |


Note that a query can even have **no `FROM` clause** when you only want to calculate something. (Oracle requires `FROM dual` for this; most others do not.)

#### Comparison operators

| Operator | Meaning |
|---|---|
| `=` | equal to (a **single** equals sign in SQL, unlike `==` in Python) |
| `<>` or `!=` | not equal to (`<>` is the standard; `!=` works almost everywhere) |
| `<`, `>` | less than, greater than |
| `<=`, `>=` | less than or equal, greater than or equal |

These produce a truth value for each row. The `WHERE` clause keeps only rows where the result is true. Beginners with a Python background often type `==` out of habit; in SQL that is an error in most engines.

```sql
SELECT order_id, quantity
FROM orders
WHERE quantity == 0;
```

**Result** (1 row):

| order_id | quantity |
|---|---|
| 1007 | 0 |


SQLite is lenient and accepts `==`, but PostgreSQL, MySQL and SQL Server do not. **Always use a single `=`** so that your SQL works everywhere.

#### Logical operators

`AND`, `OR`, and `NOT` combine conditions. They are covered in detail in *Filtering and Sorting Data*, so here is just a sample:

```sql
SELECT order_id, country, status
FROM orders
WHERE country = 'UK' AND status = 'PENDING';
```

**Result** (1 row):

| order_id | country | status |
|---|---|---|
| 1011 | UK | PENDING |


#### String operators and functions

Joining text together is called **concatenation**. The standard operator is `||`, used by SQLite, PostgreSQL and Oracle. MySQL and SQL Server use different spellings:

| Product | Concatenation |
|---|---|
| SQLite, PostgreSQL, Oracle | `a \|\| b` |
| MySQL | `CONCAT(a, b)` (the `\|\|` operator means OR unless a special mode is enabled) |
| SQL Server | `a + b` or `CONCAT(a, b)` |

```sql
SELECT order_id,
       customer_name || ' (' || country || ')' AS buyer
FROM orders
WHERE order_id <= 1003;
```

**Result** (3 rows):

| order_id | buyer |
|---|---|
| 1001 | Alice Johnson (USA) |
| 1002 | Bob Smith (USA) |
| 1003 | Carla Gomez (Canada) |


### 9. Everyday functions

A **function** takes one or more inputs (arguments) in parentheses and returns a value. Here are the ones most useful for QA work today. They operate on **each row** individually.

| Function | Purpose | Example | Dialect note |
|---|---|---|---|
| `UPPER(x)`, `LOWER(x)` | change case | `UPPER(status)` | Same everywhere |
| `LENGTH(x)` | number of characters | `LENGTH(email)` | SQL Server uses `LEN(x)` |
| `TRIM(x)` | remove leading / trailing spaces | `TRIM(country)` | Same everywhere (SQLite, PostgreSQL, MySQL, Oracle, modern SQL Server) |
| `ROUND(x, n)` | round to `n` decimals | `ROUND(9.987, 2)` | Same everywhere |
| `ABS(x)` | absolute value | `ABS(-1)` | Same everywhere |
| `COALESCE(a, b, ...)` | first non-NULL argument | `COALESCE(email, 'none')` | Same everywhere |

```sql
SELECT order_id,
       status,
       UPPER(status) AS status_upper,
       LENGTH(customer_name) AS name_length
FROM orders
WHERE order_id IN (1007, 1008, 1015);
```

**Result** (3 rows):

| order_id | status | status_upper | name_length |
|---|---|---|---|
| 1007 | PENDING | PENDING | 9 |
| 1008 | delivered | DELIVERED | 11 |
| 1015 | DELIVERED | DELIVERED | 10 |


`COALESCE` is handy when displaying NULLs in a report:

```sql
SELECT order_id, COALESCE(email, '(no email)') AS email_shown
FROM orders
WHERE order_id IN (1003, 1004, 1014);
```

**Result** (3 rows):

| order_id | email_shown |
|---|---|
| 1003 | carla.g@example.com |
| 1004 | (no email) |
| 1014 | (no email) |


> **Scope note:** Functions that work on a *whole column of rows at once* and give one summary number (for example totals and averages) are called **aggregate functions**. We will cover them in depth on Friday. Today we only use functions that work row by row.

### 10. How the database reads your query

#### The order you *write* the clauses

For the read-only queries you learn today, clauses must be written in this fixed order:

```text
SELECT   what columns / expressions to show
FROM     which table
WHERE    which rows to keep (optional)
ORDER BY how to sort the result (optional)
LIMIT    how many rows to return (optional; dialect varies)
```

(On Friday you will meet two more clauses that go between `WHERE` and `ORDER BY`. We will introduce them then.)

#### The order the database *processes* the clauses

Surprisingly, the database does not run the clauses in the order you wrote them. Logically it works like this:

1. **FROM**: find the table.
2. **WHERE**: throw away the rows that do not satisfy the condition.
3. **SELECT**: compute the requested columns and expressions (and create aliases).
4. **ORDER BY**: sort what remains.
5. **LIMIT**: cut off the result at the requested number of rows.

This explains two behaviours you will meet:

- You **cannot** use a column alias defined in `SELECT` inside `WHERE` in standard SQL, because `WHERE` runs *before* `SELECT` creates the alias. (SQLite is lenient about this; PostgreSQL, MySQL, SQL Server and Oracle are strict.) Instead, repeat the expression.
- You **can** use the alias in `ORDER BY`, because sorting happens *after* `SELECT`.

```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE quantity * unit_price > 1000
ORDER BY line_total DESC;
```

**Result** (2 rows):

| order_id | line_total |
|---|---|
| 1006 | 2300.0 |
| 1001 | 1200.0 |


Here the `WHERE` repeats the full expression (portable), while `ORDER BY` uses the alias (allowed everywhere).

### 11. Reading syntax errors

Errors are not failures; they are feedback. Here are the commonest mistakes and what the messages look like. (Messages shown are from SQLite; other engines word them differently, but they point to the same place.)

**Misspelled keyword:**

```sql
SELEC order_id FROM orders;
```

**Result (error in SQLite):**

```text
Error: near "SELEC": syntax error
```

**Missing comma between columns:**

```sql
SELECT order_id customer_name
FROM orders
WHERE order_id = 1001;
```

**Result** (1 row):

| customer_name |
|---|
| 1001 |


This is a **sneaky** one. There is no error! Because `AS` is optional, SQL reads `customer_name` as an *alias* for `order_id`, so the output has just one column. The lesson: *always check the column headings of your result.*

**Unknown column:**

```sql
SELECT order_number FROM orders;
```

**Result (error in SQLite):**

```text
Error: no such column: order_number
```

**Unknown table:**

```sql
SELECT * FROM order_items;
```

**Result (error in SQLite):**

```text
Error: no such table: order_items
```

**Trailing comma before FROM:**

```sql
SELECT order_id, FROM orders;
```

**Result (error in SQLite):**

```text
Error: near "FROM": syntax error
```

**A debugging routine:** (1) read the *first* line of the error, (2) note the word or position it mentions, (3) look at the text just *before* that position (the real mistake is often one token earlier), (4) fix one thing at a time, and (5) re-run. This is the same disciplined approach you practised with Python's debugger on Wednesday.

### 12. Multiple statements and the semicolon

A **semicolon** marks the end of a statement. You may run several statements in a script, one after another:

```sql
SELECT COUNT(*) AS total_rows FROM orders;
SELECT order_id FROM orders WHERE order_id = 1001;
```

Run as a script, the first statement returns a single row (`total_rows` = 15) and the second returns a single row (`order_id` = 1001).

(`COUNT(*)` is an *aggregate function* that counts rows. We use it here only as a convenient check; its full explanation comes on Friday.) Some tools run only the *selected* statement; others run the whole script. In Python's `sqlite3`, `execute()` accepts **one** statement, while `executescript()` runs many. Always terminate statements with `;` so that scripts are portable.

### 13. Dialect cheat sheet

| Task | SQLite | MySQL | PostgreSQL | SQL Server | Oracle |
|---|---|---|---|---|---|
| Limit rows | `LIMIT n` | `LIMIT n` | `LIMIT n` | `SELECT TOP n ...` | `FETCH FIRST n ROWS ONLY` (12c+) |
| Concatenate | `a \|\| b` | `CONCAT(a,b)` | `a \|\| b` | `a + b` / `CONCAT` | `a \|\| b` |
| String length | `LENGTH` | `LENGTH` / `CHAR_LENGTH` | `LENGTH` | `LEN` | `LENGTH` |
| Text `=` compare | case-sensitive | case-insensitive (default) | case-sensitive | case-insensitive (default) | case-sensitive |
| Quote identifiers | `"x"` `` `x` `` `[x]` | `` `x` `` | `"x"` | `[x]` or `"x"` | `"x"` |
| Today's date | `date('now')` | `CURDATE()` | `CURRENT_DATE` | `CAST(GETDATE() AS DATE)` | `SYSDATE` |
| Query with no table | `SELECT 1;` | `SELECT 1;` | `SELECT 1;` | `SELECT 1;` | `SELECT 1 FROM dual;` |

You do not need to memorise this table. Know that it exists, and when a query copied from the internet fails in your environment, check dialect first.

---

## Summary / Key Takeaways

- **SQL** is the standard, **declarative** language of relational databases: you describe *what* you want, the engine decides *how*.
- A statement is built from **keywords, identifiers, literals, operators, expressions, and clauses**, and ends with a **semicolon**.
- Keywords are case-insensitive; we write them in UPPER CASE and names in lower_snake_case for readability.
- **Text** goes in **single quotes** (double an apostrophe to include one: `'O''Brien'`); **numbers** have no quotes; **NULL** is a bare word; dates are ISO `'YYYY-MM-DD'` strings.
- Use a single `=` for equality, `<>` for not-equal, and `AND` / `OR` / `NOT` for logic.
- Whether text comparison is **case-sensitive depends on the product**, which can produce different test results across environments.
- Comments: `-- line` and `/* block */`.
- Clauses are written as `SELECT, FROM, WHERE, ORDER BY, LIMIT` but processed as `FROM, WHERE, SELECT, ORDER BY, LIMIT`.
- Read errors calmly: look at the word the message mentions and the token just before it. Beware silent "errors" like a missing comma that turns a column into an alias.
- Dialect differences (`LIMIT` vs `TOP`, `||` vs `CONCAT`, `LENGTH` vs `LEN`) are small but real.

---

## Practice Questions

**Q1.** Label each part of this statement as keyword, identifier, literal, or operator: `SELECT product FROM orders WHERE quantity > 1;`

**Q2.** Rewrite this badly formatted query in the course style: `select order_id,status from orders where country='UK' and status='PENDING'`

**Q3.** Write a query that returns the order with customer `Jack O'Brien`, showing `order_id`, `customer_name` and `status`.

**Q4.** What is wrong with `SELECT order_id, FROM orders;`? What does the fixed version return for `order_id` values below 1003?

**Q5.** Write a query that shows `order_id` and a calculated column called `line_total` (`quantity * unit_price`) for orders 1001 to 1004.

**Q6.** Order `1008` has status `delivered`. Write a query that finds orders whose status is `DELIVERED` regardless of case, using a function from this lesson.

**Q7.** Show `order_id` and the email of orders 1004 and 1005, replacing a NULL email with the text `missing`.

**Q8.** Explain in one or two sentences why `WHERE line_total > 1000` might fail in PostgreSQL if `line_total` is an alias defined in the `SELECT` list.

**Q9.** (Dialect) How would you write "first 3 rows" in SQL Server? In Oracle 12c+?

### Answers

**A1.** Keywords: `SELECT`, `FROM`, `WHERE`. Identifiers: `product`, `orders`, `quantity`. Operator: `>`. Literal: `1`. The `;` is the terminator.

**A2.**

```sql
SELECT order_id, status
FROM orders
WHERE country = 'UK'
  AND status = 'PENDING';
```

**Result** (1 row):

| order_id | status |
|---|---|
| 1011 | PENDING |


**A3.**

```sql
SELECT order_id, customer_name, status
FROM orders
WHERE customer_name = 'Jack O''Brien';
```

**Result** (1 row):

| order_id | customer_name | status |
|---|---|---|
| 1011 | Jack O'Brien | PENDING |


**A4.** There is a trailing comma after `order_id`, so the database expects another column name but finds `FROM`. Fixed:

```sql
SELECT order_id
FROM orders
WHERE order_id < 1003;
```

**Result** (2 rows):

| order_id |
|---|
| 1001 |
| 1002 |


**A5.**

```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE order_id BETWEEN 1001 AND 1004;
```

**Result** (4 rows):

| order_id | line_total |
|---|---|
| 1001 | 1200.0 |
| 1002 | 51.0 |
| 1003 | 49.95 |
| 1004 | 300.0 |


(`BETWEEN` is covered in the next-but-one lesson; `WHERE order_id <= 1004 AND order_id >= 1001` works too.)

**A6.**

```sql
SELECT order_id, status
FROM orders
WHERE UPPER(status) = 'DELIVERED';
```

**Result** (6 rows):

| order_id | status |
|---|---|
| 1001 | DELIVERED |
| 1003 | DELIVERED |
| 1008 | delivered |
| 1009 | DELIVERED |
| 1012 | DELIVERED |
| 1015 | DELIVERED |


Order `1008` is now included. Applying `UPPER` to *both sides* of the comparison is the portable way to get case-insensitive matching.

**A7.**

```sql
SELECT order_id, COALESCE(email, 'missing') AS email
FROM orders
WHERE order_id IN (1004, 1005);
```

**Result** (2 rows):

| order_id | email |
|---|---|
| 1004 | missing |
| 1005 | emma.w@example.com |


**A8.** In standard SQL the `WHERE` clause is logically processed *before* `SELECT`, so the alias does not exist yet. PostgreSQL, MySQL and SQL Server follow the standard and report an unknown column; the fix is to repeat the expression (`WHERE quantity * unit_price > 1000`).

**A9.** SQL Server: `SELECT TOP 3 * FROM orders;`. Oracle 12c and later: `SELECT * FROM orders FETCH FIRST 3 ROWS ONLY;`.

---

## Additional Resources

- PostgreSQL documentation, *SQL Syntax* (lexical structure, identifiers, constants, comments): https://www.postgresql.org/docs/current/sql-syntax.html
- SQLite documentation, *SQL As Understood By SQLite* (every statement and expression): https://www.sqlite.org/lang.html
- MySQL Reference Manual, *Language Structure* (literals, identifiers, comments): https://dev.mysql.com/doc/refman/8.0/en/language-structure.html
