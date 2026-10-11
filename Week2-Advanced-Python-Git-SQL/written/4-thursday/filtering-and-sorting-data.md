# Filtering and Sorting Data

## Learning Objectives

By the end of this lesson you will be able to:

- Use the **`WHERE`** clause to return only the rows that satisfy a condition.
- Apply **comparison operators** (`=`, `<>`, `<`, `>`, `<=`, `>=`) to numbers, text and dates.
- Combine conditions with **`AND`, `OR`, `NOT`**, and use **parentheses** to control evaluation order.
- Use **`IN`** and **`NOT IN`** for lists of values, and **`BETWEEN`** for ranges (and know that it is inclusive).
- Search text patterns with **`LIKE`** and the wildcards `%` and `_`.
- Test for missing values correctly with **`IS NULL`** and **`IS NOT NULL`**, and explain why `= NULL` never works.
- Remove duplicate rows with **`DISTINCT`**.
- Sort results with **`ORDER BY`** (ascending / descending, several columns) and make sorts **deterministic**.
- Restrict the number of rows with **`LIMIT`** (and its dialect equivalents `TOP` and `FETCH FIRST`).
- Combine filtering, sorting and limiting in a single query.

## Why This Matters

Real tables are big. A production `orders` table can hold millions of rows; even our 15-row practice table is awkward to scan by eye. A tester almost never wants "all the data". A tester wants **the specific rows that matter to the test**:

- "The order I just created through the UI." (`WHERE order_id = ...`)
- "All orders that are still `PENDING` and older than a week." (`WHERE ... AND ...`)
- "Any order with a missing email." (`WHERE email IS NULL`)
- "The 5 most recent orders." (`ORDER BY order_date DESC LIMIT 5`)

In the Week 2 Epic ("SQL for QA data validation") this lesson supplies the most important validation tool: **a condition that describes bad data**. Finding defects in a database is essentially writing a `WHERE` clause that matches rows which *should not exist*, and expecting the result to be empty. The next lessons, *Basic Query Construction* and *Using SQL for QA Data Validation*, assemble exactly the tools you learn here, and today's Project 1 milestone (data validation queries) relies on them.

You will also learn the single most common source of wrong answers in SQL, the behaviour of **NULL**, so that you do not fall into the trap yourself or let a defect slip through a faulty check.

> **Reminder:** We use the 15-row `orders` table from *Relational Database Concepts*. The data is repeated here for reference. Keep it open next to you while reading the results.

<details open>
<summary>Dataset recap: the <code>orders</code> table</summary>

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

# Part A: Filtering rows

### 1. The WHERE clause

`WHERE` filters rows. After `FROM` picks the table, the database checks **each row** against your condition. If the condition is **true** for the row, the row is kept. If it is **false** (or unknown, see NULL below), the row is discarded.

```text
SELECT   columns
FROM     table
WHERE    condition;
```

Example: find all orders from Canada.

```sql
SELECT order_id, customer_name, country
FROM orders
WHERE country = 'Canada';
```

**Result** (3 rows):

| order_id | customer_name | country |
|---|---|---|
| 1003 | Carla Gomez | Canada |
| 1006 | Frank Moore | Canada |
| 1013 | Liam Chen | Canada |


How to think about it: the database walks down the 15 rows. For each one it asks, "Is `country` equal to `'Canada'`?" Three rows say yes, so they are returned.

**Important:** `WHERE` filters **rows**, and `SELECT` chooses **columns**. You can filter on a column that you do not display:

```sql
SELECT customer_name
FROM orders
WHERE country = 'Mexico';
```

**Result** (2 rows):

| customer_name |
|---|
| Isabel Torres |
| Maria Lopez |


Here `country` is used in the condition but not shown.

### 2. Comparison operators

| Operator | Meaning | Works on |
|---|---|---|
| `=` | equal | numbers, text, dates |
| `<>` (or `!=`) | not equal | numbers, text, dates |
| `<` / `<=` | less than / less than or equal | numbers, text, dates |
| `>` / `>=` | greater than / greater than or equal | numbers, text, dates |

#### Numbers

```sql
SELECT order_id, product, quantity
FROM orders
WHERE quantity > 2;
```

**Result** (3 rows):

| order_id | product | quantity |
|---|---|---|
| 1003 | USB-C Cable | 5 |
| 1008 | Desk Lamp | 3 |
| 1013 | USB-C Cable | 10 |


```sql
SELECT order_id, product, unit_price
FROM orders
WHERE unit_price >= 300;
```

**Result** (5 rows):

| order_id | product | unit_price |
|---|---|---|
| 1001 | Laptop | 1200.0 |
| 1004 | Monitor | 300.0 |
| 1006 | Laptop | 1150.0 |
| 1012 | Monitor | 300.0 |
| 1014 | Standing Desk | 450.0 |


Numbers are written **without quotes**. Writing `'300'` (with quotes) turns it into text, which some engines will convert for you and others will reject. Do not rely on automatic conversion.

#### Text

Text is written in **single quotes**, and the comparison is exact:

```sql
SELECT order_id, status
FROM orders
WHERE status = 'PENDING';
```

**Result** (4 rows):

| order_id | status |
|---|---|
| 1004 | PENDING |
| 1007 | PENDING |
| 1011 | PENDING |
| 1014 | PENDING |


```sql
SELECT order_id, status
FROM orders
WHERE status <> 'DELIVERED';
```

**Result** (10 rows):

| order_id | status |
|---|---|
| 1002 | SHIPPED |
| 1004 | PENDING |
| 1005 | CANCELLED |
| 1006 | SHIPPED |
| 1007 | PENDING |
| 1008 | delivered |
| 1010 | SHIPPED |
| 1011 | PENDING |
| 1013 | SHIPPED |
| 1014 | PENDING |


Look carefully at the second result: order `1008` (status `delivered` in lower case) **appears**, because in SQLite `'delivered' <> 'DELIVERED'`. In MySQL and SQL Server (default case-insensitive collations) it would *not* appear. This is the case-sensitivity trap from the syntax lesson, and it is a data-quality bug in our table (inconsistent casing). To compare ignoring case in a way that works on every engine, normalise both sides:

```sql
SELECT order_id, status
FROM orders
WHERE UPPER(status) <> 'DELIVERED';
```

**Result** (9 rows):

| order_id | status |
|---|---|
| 1002 | SHIPPED |
| 1004 | PENDING |
| 1005 | CANCELLED |
| 1006 | SHIPPED |
| 1007 | PENDING |
| 1010 | SHIPPED |
| 1011 | PENDING |
| 1013 | SHIPPED |
| 1014 | PENDING |


Now order `1008` is correctly treated as delivered.

#### Dates

Our dates are ISO-formatted text, so comparisons follow calendar order:

```sql
SELECT order_id, order_date
FROM orders
WHERE order_date > '2025-02-15';
```

**Result** (5 rows):

| order_id | order_date |
|---|---|
| 1011 | 2025-02-18 |
| 1012 | 2025-03-02 |
| 1013 | 2025-03-05 |
| 1014 | 2025-03-09 |
| 1015 | 2025-03-12 |


```sql
SELECT order_id, order_date
FROM orders
WHERE order_date >= '2025-02-01' AND order_date < '2025-03-01';
```

**Result** (5 rows):

| order_id | order_date |
|---|---|
| 1007 | 2025-02-01 |
| 1008 | 2025-02-03 |
| 1009 | 2025-02-10 |
| 1010 | 2025-02-14 |
| 1011 | 2025-02-18 |


The second query returns "everything in February". Writing the end as `< '2025-03-01'` (the first moment of the next month) is a robust pattern: it works for date columns **and** for timestamp columns where `'2025-02-28 15:30:00'` must still count as February.

### 3. Combining conditions: AND, OR, NOT

| Operator | Result is true when... |
|---|---|
| `A AND B` | **both** A and B are true |
| `A OR B` | **at least one** of A, B is true |
| `NOT A` | A is **not** true |

#### AND narrows

```sql
SELECT order_id, country, status
FROM orders
WHERE country = 'USA' AND status = 'PENDING';
```

**Result** (2 rows):

| order_id | country | status |
|---|---|---|
| 1004 | USA | PENDING |
| 1007 | USA | PENDING |


Each additional `AND` makes the filter stricter: fewer rows come back.

#### OR widens

```sql
SELECT order_id, status
FROM orders
WHERE status = 'PENDING' OR status = 'CANCELLED';
```

**Result** (5 rows):

| order_id | status |
|---|---|
| 1004 | PENDING |
| 1005 | CANCELLED |
| 1007 | PENDING |
| 1011 | PENDING |
| 1014 | PENDING |


Each additional `OR` makes the filter looser: more rows can come back.

#### NOT negates

```sql
SELECT order_id, country
FROM orders
WHERE NOT country = 'USA';
```

**Result** (8 rows):

| order_id | country |
|---|---|
| 1003 | Canada |
| 1005 | UK |
| 1006 | Canada |
| 1008 | UK |
| 1010 | Mexico |
| 1011 | UK |
| 1013 | Canada |
| 1014 | Mexico |


This is equivalent to `country <> 'USA'`. `NOT` is most useful in front of `IN`, `BETWEEN`, `LIKE` and `IS NULL` (`NOT IN`, `NOT BETWEEN`, `NOT LIKE`, `IS NOT NULL`).

#### Precedence and parentheses (a classic bug)

When `AND` and `OR` appear together, **`AND` is evaluated before `OR`**, just as multiplication happens before addition in arithmetic. Parentheses override this. Study these two queries. They look similar but mean different things.

Goal: "Pending or shipped orders from the UK".

**Wrong version** (no parentheses):

```sql
SELECT order_id, country, status
FROM orders
WHERE status = 'PENDING' OR status = 'SHIPPED' AND country = 'UK';
```

**Result** (4 rows):

| order_id | country | status |
|---|---|---|
| 1004 | USA | PENDING |
| 1007 | USA | PENDING |
| 1011 | UK | PENDING |
| 1014 | Mexico | PENDING |


The database reads this as `status = 'PENDING' OR (status = 'SHIPPED' AND country = 'UK')`. Result: *all* pending orders from any country, plus only shipped UK orders. That is why USA and Mexico pending orders appear.

**Correct version**:

```sql
SELECT order_id, country, status
FROM orders
WHERE (status = 'PENDING' OR status = 'SHIPPED') AND country = 'UK';
```

**Result** (1 row):

| order_id | country | status |
|---|---|---|
| 1011 | UK | PENDING |


Only one order is both (pending or shipped) and from the UK: order `1011`.

> **Habit for testers:** whenever you mix `AND` and `OR`, add parentheses, even when you are confident about precedence. A validation query with a missing pair of parentheses can return *nothing wrong* when there *is* something wrong, a false pass, which is the worst kind of test failure.

### 4. IN and NOT IN: matching a list

`IN` is a shorthand for several `OR`s on the same column.

```sql
SELECT order_id, country
FROM orders
WHERE country IN ('UK', 'Mexico');
```

**Result** (5 rows):

| order_id | country |
|---|---|
| 1005 | UK |
| 1008 | UK |
| 1010 | Mexico |
| 1011 | UK |
| 1014 | Mexico |


This is exactly `country = 'UK' OR country = 'Mexico'`, but shorter and easier to read, especially for long lists. Numbers work too: `order_id IN (1001, 1005, 1010)`.

`NOT IN` returns rows whose value is **not** in the list:

```sql
SELECT order_id, status
FROM orders
WHERE status NOT IN ('DELIVERED', 'SHIPPED');
```

**Result** (6 rows):

| order_id | status |
|---|---|
| 1004 | PENDING |
| 1005 | CANCELLED |
| 1007 | PENDING |
| 1008 | delivered |
| 1011 | PENDING |
| 1014 | PENDING |


**Valid-values check (a very useful QA pattern):** if the specification says status may only be `PENDING`, `SHIPPED`, `DELIVERED` or `CANCELLED`, find rows that violate it:

```sql
SELECT order_id, status
FROM orders
WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED');
```

**Result** (1 row):

| order_id | status |
|---|---|
| 1008 | delivered |


Order `1008` (lower-case `delivered`) is flagged as invalid. Its spelling is right but its case is wrong, and in a case-sensitive system the application may mishandle it. Good catch.

**NULL warning for `NOT IN`:** if the list itself contains a `NULL`, `NOT IN` returns **no rows at all** (see section 7). Do not put NULLs in IN lists.

### 5. BETWEEN: ranges

`BETWEEN low AND high` is a shorthand for `>= low AND <= high`. **Both ends are included (inclusive).**

```sql
SELECT order_id, unit_price
FROM orders
WHERE unit_price BETWEEN 20 AND 100;
```

**Result** (4 rows):

| order_id | unit_price |
|---|---|
| 1002 | 25.5 |
| 1005 | 80.0 |
| 1007 | 49.99 |
| 1011 | 25.5 |


Order `1002` costs exactly 25.5 and is included; nothing costing exactly 20 or 100 exists, but if it did, it would be included too.

It works on dates:

```sql
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2025-01-10' AND '2025-01-20';
```

**Result** (4 rows):

| order_id | order_date |
|---|---|
| 1003 | 2025-01-10 |
| 1004 | 2025-01-12 |
| 1005 | 2025-01-15 |
| 1006 | 2025-01-20 |


Orders on exactly 2025-01-10 (`1003`) and 2025-01-20 (`1006`) are both in.

**Pitfalls:**

- **Order of bounds matters.** `BETWEEN 100 AND 20` returns nothing, because no value is both at least 100 and at most 20.
- **Dates with times.** With a `TIMESTAMP` column, `BETWEEN '2025-01-10' AND '2025-01-20'` stops at midnight at the *start* of the 20th, so you lose most of that day. Use `>= ... AND < next_day` as shown earlier.
- `NOT BETWEEN` gives everything outside the range.

```sql
SELECT order_id, quantity
FROM orders
WHERE quantity NOT BETWEEN 1 AND 5;
```

**Result** (3 rows):

| order_id | quantity |
|---|---|
| 1007 | 0 |
| 1011 | -1 |
| 1013 | 10 |


This finds quantities outside the *allowed* range of 1 to 5 (if that were the business rule): the zero, the negative number, and the bulk order of 10. A tester would then ask the team whether a quantity of 10 is legitimate.

### 6. LIKE: pattern matching on text

Sometimes you do not know the exact value; you know part of it. `LIKE` matches text against a **pattern** that can contain two wildcards:

| Wildcard | Matches | Example |
|---|---|---|
| `%` | **any number** of characters (including zero) | `'A%'` matches `Alice`, `Alan`, `A` |
| `_` | **exactly one** character | `'_at'` matches `Bat`, `Cat`, not `At` or `Chat` |

```sql
SELECT order_id, customer_name
FROM orders
WHERE customer_name LIKE 'A%';
```

**Result** (2 rows):

| order_id | customer_name |
|---|---|
| 1001 | Alice Johnson |
| 1009 | Alice Johnson |


Names starting with `A`. Common pattern shapes:

| Pattern | Meaning |
|---|---|
| `'A%'` | starts with A |
| `'%son'` | ends with `son` |
| `'%an%'` | contains `an` anywhere |
| `'_o%'` | second letter is `o` |
| `'%@example.com'` | ends with `@example.com` |

```sql
SELECT order_id, customer_name
FROM orders
WHERE customer_name LIKE '%son';
```

**Result** (3 rows):

| order_id | customer_name |
|---|---|
| 1001 | Alice Johnson |
| 1005 | Emma Wilson |
| 1009 | Alice Johnson |


```sql
SELECT order_id, product
FROM orders
WHERE product LIKE '%USB%';
```

**Result** (2 rows):

| order_id | product |
|---|---|
| 1003 | USB-C Cable |
| 1013 | USB-C Cable |


```sql
SELECT order_id, customer_name
FROM orders
WHERE customer_name LIKE '_a%';
```

**Result** (5 rows):

| order_id | customer_name |
|---|---|
| 1003 | Carla Gomez |
| 1004 | David Lee |
| 1011 | Jack O'Brien |
| 1012 | Karen White |
| 1014 | Maria Lopez |


Names whose second letter is `a`: Carla, David, Jack, Karen and Maria. The `_` stands for exactly one character (the first letter), the `a` must come next, and `%` covers whatever follows. Frank (second letter `r`) and Isabel (second letter `s`) do not match.

`NOT LIKE` inverts the match.

#### A QA use: spotting malformed emails

A valid email should end with a domain such as `.com`. Our table contains an email `frank.moore@example` that is missing it. Find emails that do *not* match the expected shape:

```sql
SELECT order_id, email
FROM orders
WHERE email NOT LIKE '%@%.%';
```

**Result** (1 row):

| order_id | email |
|---|---|
| 1006 | frank.moore@example |


The pattern `'%@%.%'` means "some text, an `@`, some text, a `.`, some text". Only order `1006` fails it. (Orders with NULL email do not appear either. Why? Because `NULL NOT LIKE ...` is *unknown*, not true. Section 7 explains.) A real validation might need more thorough checks, but this is a quick and powerful smoke test. Regular expressions (`REGEXP` in MySQL, `~` in PostgreSQL) are more precise but not portable.

#### Case sensitivity of LIKE (dialects!)

```sql
SELECT order_id, product
FROM orders
WHERE product LIKE 'laptop';
```

**Result** (2 rows):

| order_id | product |
|---|---|
| 1001 | Laptop |
| 1006 | Laptop |


In **SQLite** `LIKE` is case-insensitive for ordinary English letters, so `'laptop'` matches `Laptop`. In **MySQL** and **SQL Server** it is also case-insensitive by default. In **PostgreSQL** and **Oracle** `LIKE` is case-**sensitive**, so nothing would match; PostgreSQL provides `ILIKE` for case-insensitive matching. For portable code write `LOWER(product) LIKE 'laptop'`.

#### Searching for a literal `%` or `_`

If the data itself contains `%` or `_` (for example a discount code `SAVE_10%`), tell the database to treat the character literally with `ESCAPE`:

```sql
SELECT 'SAVE_10%' AS code
WHERE 'SAVE_10%' LIKE 'SAVE\_10\%' ESCAPE '\';
```

**Result** (1 row):

| code |
|---|
| SAVE_10% |


`ESCAPE '\'` declares `\` as the escape character, so `\_` and `\%` mean the literal characters. (SQL Server also lets you use `[_]` and `[%]`. The `SELECT ... WHERE` with no `FROM` used in this demo works in SQLite and PostgreSQL; MySQL and Oracle may need `FROM DUAL`.)

#### Performance note

`LIKE 'abc%'` (starts with) can use an index, but `LIKE '%abc'` or `'%abc%'` usually forces the database to read every row. On small test databases this is fine; on production-sized data, ask a developer before running leading-wildcard searches.

### 7. NULL: IS NULL and IS NOT NULL

This is the most important subsection of the lesson.

Recall that NULL means "no value / unknown". Comparing to unknown gives unknown. Let us try the obvious (and wrong) query:

```sql
SELECT order_id, email
FROM orders
WHERE email = NULL;
```

**Result** (0 rows):

| order_id | email |
|---|---|


**Zero rows**, even though two orders have a NULL email. Why? For each row the database evaluates `email = NULL`. For a row where email is NULL, that is `NULL = NULL`, which means "is an unknown value equal to an unknown value?" The honest answer is "unknown". `WHERE` keeps only rows where the condition is **true**, so unknown rows are dropped.

The same problem occurs with `<> NULL`:

```sql
SELECT order_id, email
FROM orders
WHERE email <> NULL;
```

**Result** (0 rows):

| order_id | email |
|---|---|


Also zero rows. The correct tools are **`IS NULL`** and **`IS NOT NULL`**:

```sql
SELECT order_id, customer_name, email
FROM orders
WHERE email IS NULL;
```

**Result** (2 rows):

| order_id | customer_name | email |
|---|---|---|
| 1004 | David Lee | NULL |
| 1014 | Maria Lopez | NULL |


```sql
SELECT order_id, email
FROM orders
WHERE email IS NOT NULL
  AND order_id <= 1003;
```

**Result** (3 rows):

| order_id | email |
|---|---|
| 1001 | alice.j@example.com |
| 1002 | bob.smith@example.com |
| 1003 | carla.g@example.com |


#### Three-valued logic

SQL has **three** truth values: **TRUE**, **FALSE**, and **UNKNOWN**. Any comparison with NULL gives UNKNOWN. `WHERE` keeps only TRUE. Remember:

| Expression | Result |
|---|---|
| `NULL = NULL` | UNKNOWN |
| `NULL <> 5` | UNKNOWN |
| `5 > NULL` | UNKNOWN |
| `NULL IS NULL` | TRUE |
| `TRUE AND UNKNOWN` | UNKNOWN |
| `FALSE AND UNKNOWN` | FALSE |
| `TRUE OR UNKNOWN` | TRUE |
| `NOT UNKNOWN` | UNKNOWN |

The consequence for validation: **"not equal" queries silently skip NULL rows.** Compare:

```sql
SELECT order_id, email
FROM orders
WHERE email <> 'alice.j@example.com'
  AND order_id <= 1004;
```

**Result** (2 rows):

| order_id | email |
|---|---|
| 1002 | bob.smith@example.com |
| 1003 | carla.g@example.com |


Order `1004` (NULL email) is *not* in the output, even though its email certainly isn't Alice's. If you want NULLs included you must say so:

```sql
SELECT order_id, email
FROM orders
WHERE (email <> 'alice.j@example.com' OR email IS NULL)
  AND order_id <= 1004;
```

**Result** (3 rows):

| order_id | email |
|---|---|
| 1002 | bob.smith@example.com |
| 1003 | carla.g@example.com |
| 1004 | NULL |


#### The NOT IN trap

```sql
SELECT order_id, status
FROM orders
WHERE status NOT IN ('PENDING', NULL);
```

**Result** (0 rows):

| order_id | status |
|---|---|


You might expect all non-pending orders. You get **nothing**, because for every row `status NOT IN ('PENDING', NULL)` expands to `status <> 'PENDING' AND status <> NULL`, and the second part is always UNKNOWN. A single NULL in the list ruins the whole condition. This is why the earlier warning mattered.

#### Empty string versus NULL

A missing value can also be stored as an empty string `''` or a placeholder like `'N/A'` or `'NULL'`. These are **not** NULL, so `IS NULL` will not find them. A thorough validation therefore checks several shapes of "missing":

```sql
SELECT order_id, email
FROM orders
WHERE email IS NULL
   OR TRIM(email) = ''
   OR UPPER(email) IN ('NULL', 'N/A');
```

**Result** (2 rows):

| order_id | email |
|---|---|
| 1004 | NULL |
| 1014 | NULL |


In our dataset only genuine NULLs exist; but in real test data, "blank" is often hiding in other disguises. (On Oracle, `''` is NULL, so `TRIM(email) = ''` is never true there.)

### 8. DISTINCT: removing duplicates

Our table has several orders for the same country, product and status. If you only want to know **which different values exist**, use `DISTINCT` right after `SELECT`:

```sql
SELECT country
FROM orders;
```

**Result** (15 rows):

| country |
|---|
| USA |
| USA |
| Canada |
| USA |
| UK |
| Canada |
| USA |
| UK |
| USA |
| Mexico |
| UK |
| USA |
| Canada |
| Mexico |
| USA |


That is 15 rows with repeats. Compare:

```sql
SELECT DISTINCT country
FROM orders;
```

**Result** (4 rows):

| country |
|---|
| USA |
| Canada |
| UK |
| Mexico |


Four different countries. `DISTINCT` applies to the **whole row of selected columns**, not just the first column:

```sql
SELECT DISTINCT country, status
FROM orders;
```

**Result** (10 rows):

| country | status |
|---|---|
| USA | DELIVERED |
| USA | SHIPPED |
| Canada | DELIVERED |
| USA | PENDING |
| UK | CANCELLED |
| Canada | SHIPPED |
| UK | delivered |
| Mexico | SHIPPED |
| UK | PENDING |
| Mexico | PENDING |


This lists each *combination* of country and status once.

**QA uses for DISTINCT:**

- **Discover the actual set of values** in a column, and compare it to the specification. Try `SELECT DISTINCT status FROM orders;`; you will see five values, including the lower-case `delivered`, which the spec says should not exist.
- **Check consistency** of categories, countries, or codes.
- **Spot typos and variants** (`USA`, `U.S.A.`, `United States`).

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


**NULL and DISTINCT:** NULLs are treated as equal to each other for `DISTINCT`, so all NULLs collapse into one:

```sql
SELECT DISTINCT email
FROM orders
WHERE order_id IN (1001, 1004, 1009, 1014);
```

**Result** (2 rows):

| email |
|---|
| alice.j@example.com |
| NULL |


Alice's repeated email appears once, and the two NULLs appear as one NULL row.

*Dialect:* `DISTINCT` is standard everywhere. Counting distinct values and finding duplicate rows more thoroughly belongs to the aggregate functions and `GROUP BY` that we will cover in depth on Friday.

---

# Part B: Sorting and limiting rows

### 9. ORDER BY: sorting the result

Without `ORDER BY` the order of the rows is **not guaranteed** (you learned this in the first lesson). `ORDER BY` is the *only* way to get a reliable order. It is always written near the end of the query.

```sql
SELECT order_id, product, unit_price
FROM orders
ORDER BY unit_price;
```

**Result** (15 rows):

| order_id | product | unit_price |
|---|---|---|
| 1015 | Keyboard | 0.0 |
| 1003 | USB-C Cable | 9.99 |
| 1013 | USB-C Cable | 9.99 |
| 1008 | Desk Lamp | 19.99 |
| 1002 | Wireless Mouse | 25.5 |
| 1011 | Wireless Mouse | 25.5 |
| 1007 | Webcam | 49.99 |
| 1005 | Keyboard | 80.0 |
| 1009 | Headphones | 150.0 |
| 1010 | Office Chair | 220.0 |
| 1004 | Monitor | 300.0 |
| 1012 | Monitor | 300.0 |
| 1014 | Standing Desk | 450.0 |
| 1006 | Laptop | 1150.0 |
| 1001 | Laptop | 1200.0 |


By default, sorting is **ascending** (`ASC`): smallest to largest, A to Z, oldest to newest. Use `DESC` for the reverse:

```sql
SELECT order_id, product, unit_price
FROM orders
ORDER BY unit_price DESC;
```

**Result** (15 rows):

| order_id | product | unit_price |
|---|---|---|
| 1001 | Laptop | 1200.0 |
| 1006 | Laptop | 1150.0 |
| 1014 | Standing Desk | 450.0 |
| 1004 | Monitor | 300.0 |
| 1012 | Monitor | 300.0 |
| 1010 | Office Chair | 220.0 |
| 1009 | Headphones | 150.0 |
| 1005 | Keyboard | 80.0 |
| 1007 | Webcam | 49.99 |
| 1002 | Wireless Mouse | 25.5 |
| 1011 | Wireless Mouse | 25.5 |
| 1008 | Desk Lamp | 19.99 |
| 1003 | USB-C Cable | 9.99 |
| 1013 | USB-C Cable | 9.99 |
| 1015 | Keyboard | 0.0 |


`ASC` is the default and can be omitted, but writing it explicitly can improve readability.

#### Sorting by text and by dates

```sql
SELECT order_id, customer_name
FROM orders
ORDER BY customer_name;
```

**Result** (15 rows):

| order_id | customer_name |
|---|---|
| 1001 | Alice Johnson |
| 1009 | Alice Johnson |
| 1002 | Bob Smith |
| 1003 | Carla Gomez |
| 1004 | David Lee |
| 1005 | Emma Wilson |
| 1006 | Frank Moore |
| 1007 | Grace Kim |
| 1008 | Henry Adams |
| 1010 | Isabel Torres |
| 1011 | Jack O'Brien |
| 1012 | Karen White |
| 1013 | Liam Chen |
| 1014 | Maria Lopez |
| 1015 | Noah Brown |


Text sorts alphabetically (according to the database's *collation*, a rule set about case and accents). Dates in ISO format sort chronologically:

```sql
SELECT order_id, order_date
FROM orders
ORDER BY order_date DESC;
```

**Result** (15 rows):

| order_id | order_date |
|---|---|
| 1015 | 2025-03-12 |
| 1014 | 2025-03-09 |
| 1013 | 2025-03-05 |
| 1012 | 2025-03-02 |
| 1011 | 2025-02-18 |
| 1010 | 2025-02-14 |
| 1009 | 2025-02-10 |
| 1008 | 2025-02-03 |
| 1007 | 2025-02-01 |
| 1006 | 2025-01-20 |
| 1005 | 2025-01-15 |
| 1004 | 2025-01-12 |
| 1003 | 2025-01-10 |
| 1002 | 2025-01-07 |
| 1001 | 2025-01-05 |


Newest first. This is the pattern for "most recent first", which testers use constantly to find "the order I just created".

**Text numbers sort wrongly:** if a numeric value were stored as text, `'10'` sorts *before* `'9'` (because `'1'` < `'9'`). This is why numbers belong in numeric columns. If you ever see surprising sort order in a test, check the column type.

#### Sorting by several columns

When two rows tie on the first sort key, the second key decides. List the columns separated by commas; each can have its own direction.

```sql
SELECT order_id, country, unit_price
FROM orders
ORDER BY country ASC, unit_price DESC;
```

**Result** (15 rows):

| order_id | country | unit_price |
|---|---|---|
| 1006 | Canada | 1150.0 |
| 1003 | Canada | 9.99 |
| 1013 | Canada | 9.99 |
| 1014 | Mexico | 450.0 |
| 1010 | Mexico | 220.0 |
| 1005 | UK | 80.0 |
| 1011 | UK | 25.5 |
| 1008 | UK | 19.99 |
| 1001 | USA | 1200.0 |
| 1004 | USA | 300.0 |
| 1012 | USA | 300.0 |
| 1009 | USA | 150.0 |
| 1007 | USA | 49.99 |
| 1002 | USA | 25.5 |
| 1015 | USA | 0.0 |


Reading this: sort by `country` A to Z; *within each country*, the most expensive first. Within Canada: 1150, 9.99, 9.99. Notice the final tie: orders `1003` and `1013` both cost 9.99 and are in Canada. The database may return them in either order. That brings us to determinism.

#### Making a sort deterministic

If sort keys tie, the relative order of tied rows is **unspecified**. A test that compares output to an expected list could pass one day and fail the next. The fix is to add a **tiebreaker**, a final sort key that is unique, usually the primary key:

```sql
SELECT order_id, country, unit_price
FROM orders
ORDER BY country ASC, unit_price DESC, order_id ASC;
```

**Result** (15 rows):

| order_id | country | unit_price |
|---|---|---|
| 1006 | Canada | 1150.0 |
| 1003 | Canada | 9.99 |
| 1013 | Canada | 9.99 |
| 1014 | Mexico | 450.0 |
| 1010 | Mexico | 220.0 |
| 1005 | UK | 80.0 |
| 1011 | UK | 25.5 |
| 1008 | UK | 19.99 |
| 1001 | USA | 1200.0 |
| 1004 | USA | 300.0 |
| 1012 | USA | 300.0 |
| 1009 | USA | 150.0 |
| 1007 | USA | 49.99 |
| 1002 | USA | 25.5 |
| 1015 | USA | 0.0 |


Now `1003` always comes before `1013`.

#### Sorting by an alias, an expression, or a position

```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
ORDER BY line_total DESC;
```

**Result** (15 rows):

| order_id | line_total |
|---|---|
| 1006 | 2300.0 |
| 1001 | 1200.0 |
| 1012 | 600.0 |
| 1014 | 450.0 |
| 1004 | 300.0 |
| 1010 | 220.0 |
| 1009 | 150.0 |
| 1013 | 99.9 |
| 1005 | 80.0 |
| 1008 | 59.97 |
| 1002 | 51.0 |
| 1003 | 49.95 |
| 1007 | 0.0 |
| 1015 | 0.0 |
| 1011 | -25.5 |


You can sort by an alias (allowed because `ORDER BY` is processed after `SELECT`), by an expression (`ORDER BY quantity * unit_price DESC`), or by the column's **position** in the select list (`ORDER BY 2 DESC`). Position numbers are short but fragile; if someone reorders the columns the sort changes silently. Prefer names.

You can also sort by a column you do not show:

```sql
SELECT customer_name
FROM orders
ORDER BY order_date
LIMIT 3;
```

**Result** (3 rows):

| customer_name |
|---|
| Alice Johnson |
| Bob Smith |
| Carla Gomez |


#### Where do NULLs go when sorting?

NULL is neither bigger nor smaller than anything, yet the database must put it somewhere. The answer differs by product:

| Product | NULLs in ascending order |
|---|---|
| SQLite, MySQL, SQL Server | **first** (treated as the smallest) |
| PostgreSQL, Oracle | **last** (treated as the largest) |

```sql
SELECT order_id, email
FROM orders
WHERE order_id IN (1003, 1004, 1005, 1014)
ORDER BY email;
```

**Result** (4 rows):

| order_id | email |
|---|---|
| 1004 | NULL |
| 1014 | NULL |
| 1003 | carla.g@example.com |
| 1005 | emma.w@example.com |


PostgreSQL, Oracle, and recent SQLite/others support explicit control: `ORDER BY email NULLS LAST` (or `NULLS FIRST`). MySQL and SQL Server do not have this syntax; the common workaround is `ORDER BY email IS NULL, email` (MySQL) or `ORDER BY CASE WHEN email IS NULL THEN 1 ELSE 0 END, email` (SQL Server).

```sql
SELECT order_id, email
FROM orders
WHERE order_id IN (1003, 1004, 1005, 1014)
ORDER BY email NULLS LAST;
```

**Result** (4 rows):

| order_id | email |
|---|---|
| 1003 | carla.g@example.com |
| 1005 | emma.w@example.com |
| 1004 | NULL |
| 1014 | NULL |


### 10. LIMIT: returning only the first N rows

`LIMIT n` returns at most `n` rows. It goes at the very end of the query.

```sql
SELECT order_id, customer_name
FROM orders
LIMIT 3;
```

**Result** (3 rows):

| order_id | customer_name |
|---|---|
| 1001 | Alice Johnson |
| 1002 | Bob Smith |
| 1003 | Carla Gomez |


**Warning:** `LIMIT` without `ORDER BY` returns *some* three rows, not necessarily "the first three" in any meaningful sense. Always pair `LIMIT` with `ORDER BY` unless you only need "any sample rows".

The famous **Top-N** pattern combines both:

```sql
-- The 3 most expensive products ordered
SELECT order_id, product, unit_price
FROM orders
ORDER BY unit_price DESC
LIMIT 3;
```

**Result** (3 rows):

| order_id | product | unit_price |
|---|---|---|
| 1001 | Laptop | 1200.0 |
| 1006 | Laptop | 1150.0 |
| 1014 | Standing Desk | 450.0 |


```sql
-- The most recent order
SELECT order_id, customer_name, order_date
FROM orders
ORDER BY order_date DESC, order_id DESC
LIMIT 1;
```

**Result** (1 row):

| order_id | customer_name | order_date |
|---|---|---|
| 1015 | Noah Brown | 2025-03-12 |


For automated tests, "the latest order" (`ORDER BY ... DESC LIMIT 1`) is how you find the record your test just created, when you do not know its id.

#### OFFSET: skipping rows (paging)

`OFFSET m` skips the first `m` rows before counting. `LIMIT 5 OFFSET 5` means "the second page of five".

```sql
SELECT order_id, customer_name
FROM orders
ORDER BY order_id
LIMIT 5 OFFSET 5;
```

**Result** (5 rows):

| order_id | customer_name |
|---|---|
| 1006 | Frank Moore |
| 1007 | Grace Kim |
| 1008 | Henry Adams |
| 1009 | Alice Johnson |
| 1010 | Isabel Torres |


This is how applications build "page 2" screens, so testers use it to verify pagination. (MySQL also accepts `LIMIT 5, 5`, offset first, which is confusing. Avoid it.)

#### Limiting rows in other databases

| Product | Syntax |
|---|---|
| SQLite, MySQL, PostgreSQL | `... ORDER BY x LIMIT 3 OFFSET 5` |
| SQL Server | `SELECT TOP 3 ... ORDER BY x` or `ORDER BY x OFFSET 5 ROWS FETCH NEXT 3 ROWS ONLY` |
| Oracle 12c+ | `ORDER BY x OFFSET 5 ROWS FETCH NEXT 3 ROWS ONLY` (or `FETCH FIRST 3 ROWS ONLY`) |
| Standard SQL | `OFFSET 5 ROWS FETCH FIRST 3 ROWS ONLY` |

Older Oracle (before 12c) used the pseudo-column `ROWNUM`, which you may meet in legacy systems.

---

# Part C: Putting it together

### 11. The full order of a filtered, sorted, limited query

```text
SELECT   [DISTINCT] columns / expressions
FROM     table
WHERE    row conditions
ORDER BY sort keys
LIMIT    count [OFFSET skip];
```

The database processes them as `FROM` then `WHERE` then `SELECT` (with `DISTINCT`) then `ORDER BY` then `LIMIT`. So rows are filtered **first**, sorted **second**, and limited **last**.

Example: "Show the two largest pending orders by value."

```sql
SELECT order_id,
       customer_name,
       quantity * unit_price AS line_total
FROM orders
WHERE status = 'PENDING'
ORDER BY line_total DESC
LIMIT 2;
```

**Result** (2 rows):

| order_id | customer_name | line_total |
|---|---|---|
| 1014 | Maria Lopez | 450.0 |
| 1004 | David Lee | 300.0 |


Walk-through: (1) keep only PENDING rows (`1004`, `1007`, `1011`, `1014`), (2) compute each line total (300, 0, -25.5, 450), (3) sort descending (450, 300, 0, -25.5), (4) take the first two.

### 12. Real-world QA scenarios

**Scenario 1: "Did my test order arrive?"** Your UI test placed an order for customer `Karen White` and now needs to confirm it exists.

```sql
SELECT order_id, customer_name, product, status
FROM orders
WHERE customer_name = 'Karen White'
ORDER BY order_id DESC
LIMIT 1;
```

**Result** (1 row):

| order_id | customer_name | product | status |
|---|---|---|---|
| 1012 | Karen White | Monitor | DELIVERED |


**Scenario 2: "Find test data."** You need a pending order from the UK to test the cancel feature.

```sql
SELECT order_id, customer_name, status, country
FROM orders
WHERE status = 'PENDING'
  AND country = 'UK'
ORDER BY order_id
LIMIT 1;
```

**Result** (1 row):

| order_id | customer_name | status | country |
|---|---|---|---|
| 1011 | Jack O'Brien | PENDING | UK |


**Scenario 3: "Orders that need business attention."** Large (quantity of 5 or more) or expensive (price at least 1000) orders that are not yet delivered.

```sql
SELECT order_id, product, quantity, unit_price, status
FROM orders
WHERE (quantity >= 5 OR unit_price >= 1000)
  AND UPPER(status) <> 'DELIVERED'
ORDER BY unit_price DESC, order_id;
```

**Result** (2 rows):

| order_id | product | quantity | unit_price | status |
|---|---|---|---|---|
| 1006 | Laptop | 2 | 1150.0 | SHIPPED |
| 1013 | USB-C Cable | 10 | 9.99 | SHIPPED |


**Scenario 4: "Is the data clean?"** Orders with quantity outside 1..100 or a zero price.

```sql
SELECT order_id, product, quantity, unit_price
FROM orders
WHERE quantity NOT BETWEEN 1 AND 100
   OR unit_price <= 0
ORDER BY order_id;
```

**Result** (3 rows):

| order_id | product | quantity | unit_price |
|---|---|---|---|
| 1007 | Webcam | 0 | 49.99 |
| 1011 | Wireless Mouse | -1 | 25.5 |
| 1015 | Keyboard | 1 | 0.0 |


Each of these returned rows is a potential defect to investigate. Three suspicious rows from one short query.

### 13. Common mistakes (checklist)

| Mistake | What goes wrong | Fix |
|---|---|---|
| `WHERE col = NULL` | Zero rows, silently | `IS NULL` |
| `NOT IN` list containing NULL | Zero rows | Remove NULLs from the list |
| `AND`/`OR` without parentheses | Wrong rows | Add parentheses |
| `BETWEEN` with reversed bounds | Zero rows | Low value first |
| `BETWEEN` on timestamps | Last day truncated | `>= start AND < next_day` |
| Comparing text with wrong case | Missed (or extra) rows depending on engine | `UPPER(col) = 'VALUE'` |
| `LIKE '%x'` on large tables | Slow query | Avoid leading wildcards where possible |
| `LIMIT` without `ORDER BY` | Random-looking rows | Always sort first |
| Ties in `ORDER BY` | Unstable order between runs | Add the primary key last |
| `<>` expecting NULL rows | NULL rows skipped | `OR col IS NULL` |

---

## Summary / Key Takeaways

- **`WHERE`** keeps rows whose condition is TRUE. It filters rows; `SELECT` chooses columns.
- Use `=`, `<>`, `<`, `<=`, `>`, `>=` for comparisons. Text and dates go in single quotes; numbers do not.
- **`AND`** narrows, **`OR`** widens, **`NOT`** negates. `AND` binds tighter than `OR`: use **parentheses** whenever you mix them.
- **`IN (...)`** matches a list, **`BETWEEN a AND b`** matches an *inclusive* range, **`LIKE`** matches patterns using `%` (any characters) and `_` (one character).
- NULL is "unknown". Test with **`IS NULL` / `IS NOT NULL`**, never `= NULL`. Comparisons with NULL are UNKNOWN and are filtered out, so `<>` and `NOT IN` skip NULL rows, and a NULL in a `NOT IN` list returns nothing.
- **`DISTINCT`** removes duplicate rows and reveals the real set of values in a column.
- **`ORDER BY`** is the only way to guarantee order. Use `ASC` / `DESC`, multiple keys, and a unique tiebreaker for repeatability.
- **`LIMIT`** (with `OFFSET`) restricts rows; always combine it with `ORDER BY`. Other engines use `TOP` or `FETCH FIRST`.
- Processing order: `FROM`, `WHERE`, `SELECT`/`DISTINCT`, `ORDER BY`, `LIMIT`.
- Dialect watch-outs: text comparison case rules, `LIKE` case rules, NULL sort position, and row-limiting syntax.

---

## Practice Questions

**Q1.** List `order_id`, `product` and `quantity` for orders where `quantity` is greater than or equal to 3.

**Q2.** List all orders (`order_id`, `status`) whose status is `SHIPPED` and whose country is `Canada`.

**Q3.** List orders from the UK or Mexico that are not `PENDING`. Use parentheses correctly.

**Q4.** Use `BETWEEN` to find orders placed in January 2025 (`order_id`, `order_date`).

**Q5.** Use `IN` to show orders whose product is `Laptop`, `Monitor` or `Webcam`.

**Q6.** Use `LIKE` to find all customers whose name ends with `n` (case-insensitive in SQLite).

**Q7.** Write a query that finds orders with missing emails, and explain why `WHERE email = ''` would not find them.

**Q8.** List the distinct `category` values.

**Q9.** Show the three cheapest orders by `unit_price` that are greater than zero. Break ties by `order_id`.

**Q10.** Show the order IDs and dates of the two most recent orders.

**Q11.** Page 2 (3 rows per page) of orders sorted by `order_id`.

**Q12.** Find all orders whose `status` is not exactly one of the four allowed upper-case values.

**Q13.** Explain why `WHERE country <> 'USA'` would not return a row whose country is NULL, even though NULL is "not USA". (No NULL countries exist here; answer conceptually.)

**Q14.** (Challenge) Find orders that are "suspicious" if any of these is true: quantity less than 1, price of 0 or less, or email is NULL. Show `order_id` and the three columns, sorted by `order_id`.

### Answers

**A1.**

```sql
SELECT order_id, product, quantity
FROM orders
WHERE quantity >= 3;
```

**Result** (3 rows):

| order_id | product | quantity |
|---|---|---|
| 1003 | USB-C Cable | 5 |
| 1008 | Desk Lamp | 3 |
| 1013 | USB-C Cable | 10 |


**A2.**

```sql
SELECT order_id, status
FROM orders
WHERE status = 'SHIPPED'
  AND country = 'Canada';
```

**Result** (2 rows):

| order_id | status |
|---|---|
| 1006 | SHIPPED |
| 1013 | SHIPPED |


**A3.**

```sql
SELECT order_id, country, status
FROM orders
WHERE country IN ('UK', 'Mexico')
  AND status <> 'PENDING';
```

**Result** (3 rows):

| order_id | country | status |
|---|---|---|
| 1005 | UK | CANCELLED |
| 1008 | UK | delivered |
| 1010 | Mexico | SHIPPED |


**A4.**

```sql
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2025-01-01' AND '2025-01-31';
```

**Result** (6 rows):

| order_id | order_date |
|---|---|
| 1001 | 2025-01-05 |
| 1002 | 2025-01-07 |
| 1003 | 2025-01-10 |
| 1004 | 2025-01-12 |
| 1005 | 2025-01-15 |
| 1006 | 2025-01-20 |


**A5.**

```sql
SELECT order_id, product
FROM orders
WHERE product IN ('Laptop', 'Monitor', 'Webcam');
```

**Result** (5 rows):

| order_id | product |
|---|---|
| 1001 | Laptop |
| 1004 | Monitor |
| 1006 | Laptop |
| 1007 | Webcam |
| 1012 | Monitor |


**A6.**

```sql
SELECT order_id, customer_name
FROM orders
WHERE customer_name LIKE '%n';
```

**Result** (6 rows):

| order_id | customer_name |
|---|---|
| 1001 | Alice Johnson |
| 1005 | Emma Wilson |
| 1009 | Alice Johnson |
| 1011 | Jack O'Brien |
| 1013 | Liam Chen |
| 1015 | Noah Brown |


**A7.**

```sql
SELECT order_id, customer_name
FROM orders
WHERE email IS NULL;
```

**Result** (2 rows):

| order_id | customer_name |
|---|---|
| 1004 | David Lee |
| 1014 | Maria Lopez |


`email = ''` tests for an *empty string*, which is a real value. A NULL is *no value*, and a comparison involving NULL is never true.

**A8.**

```sql
SELECT DISTINCT category
FROM orders;
```

**Result** (3 rows):

| category |
|---|
| Electronics |
| Accessories |
| Home Office |


**A9.**

```sql
SELECT order_id, product, unit_price
FROM orders
WHERE unit_price > 0
ORDER BY unit_price ASC, order_id ASC
LIMIT 3;
```

**Result** (3 rows):

| order_id | product | unit_price |
|---|---|---|
| 1003 | USB-C Cable | 9.99 |
| 1013 | USB-C Cable | 9.99 |
| 1008 | Desk Lamp | 19.99 |


**A10.**

```sql
SELECT order_id, order_date
FROM orders
ORDER BY order_date DESC, order_id DESC
LIMIT 2;
```

**Result** (2 rows):

| order_id | order_date |
|---|---|
| 1015 | 2025-03-12 |
| 1014 | 2025-03-09 |


**A11.**

```sql
SELECT order_id, customer_name
FROM orders
ORDER BY order_id
LIMIT 3 OFFSET 3;
```

**Result** (3 rows):

| order_id | customer_name |
|---|---|
| 1004 | David Lee |
| 1005 | Emma Wilson |
| 1006 | Frank Moore |


(Page 1 is `OFFSET 0`, page 2 is `OFFSET 3`, page 3 is `OFFSET 6`: offset = (page - 1) x page size.)

**A12.**

```sql
SELECT order_id, status
FROM orders
WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED')
   OR status IS NULL;
```

**Result** (1 row):

| order_id | status |
|---|---|
| 1008 | delivered |


The `OR status IS NULL` makes sure that NULL statuses (which `NOT IN` would skip) are flagged as well.

**A13.** For a row with NULL country the comparison `NULL <> 'USA'` evaluates to UNKNOWN, not TRUE. `WHERE` keeps only TRUE rows. To include NULLs add `OR country IS NULL`.

**A14.**

```sql
SELECT order_id, quantity, unit_price, email
FROM orders
WHERE quantity < 1
   OR unit_price <= 0
   OR email IS NULL
ORDER BY order_id;
```

**Result** (5 rows):

| order_id | quantity | unit_price | email |
|---|---|---|---|
| 1004 | 1 | 300.0 | NULL |
| 1007 | 0 | 49.99 | grace.k@example.com |
| 1011 | -1 | 25.5 | jack.ob@example.com |
| 1014 | 1 | 450.0 | NULL |
| 1015 | 1 | 0.0 | noah.b@example.com |


Five defect candidates: two missing emails (`1004`, `1014`), a zero quantity (`1007`), a negative quantity (`1011`) and a zero price (`1015`).

---

## Additional Resources

- PostgreSQL documentation, *Table Expressions: the WHERE clause*: https://www.postgresql.org/docs/current/queries-table-expressions.html
- PostgreSQL documentation, *Sorting Rows (ORDER BY)* and *LIMIT and OFFSET*: https://www.postgresql.org/docs/current/queries-order.html and https://www.postgresql.org/docs/current/queries-limit.html
- SQLite documentation, *NULL Handling in SQLite*: https://www.sqlite.org/nulls.html
