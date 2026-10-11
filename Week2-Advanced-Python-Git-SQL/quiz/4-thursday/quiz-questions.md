# Daily Knowledge Check: Week2-Advanced-Python-Git-SQL — Thursday: SQL Fundamentals

Try each question before opening the solution. Every question names the written lesson it comes from, so you can go back and re-read.

**Practice data:** all query questions use the 15-row `orders` table from today's lessons (columns: `order_id`, `customer_name`, `email`, `product`, `category`, `quantity`, `unit_price`, `status`, `order_date`, `country`), or a tiny inline expression. **Unless a question names another engine, assume SQLite**, the engine we practise on today. Keep your `orders` table open next to you.

---


## Part 1: Multiple Choice

### 1. Order 1004 has no email address stored. Which statement best describes the value in that `email` cell?
- [ ] A) It is the number `0`
- [ ] B) It is `NULL`, a marker meaning the value is unknown or missing, which is different from `0` or an empty string
- [ ] C) It is an empty string `''`, which is the same thing as NULL
- [ ] D) It is the four-letter text `'NULL'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It is `NULL`, a marker meaning the value is unknown or missing, which is different from `0` or an empty string

**Explanation:** NULL means "no value / unknown". In the `orders` table orders 1004 and 1014 have a genuine NULL email. Because it means "unknown", NULL needs special handling in queries (`IS NULL`).
- **Why others are wrong:**
  - A) `0` is a known number; a quantity of 0 is different from an unknown quantity.
  - C) An empty string is a known text of length zero; it looks similar in a grid but behaves differently in queries.
  - D) The text `'NULL'` is an ordinary string (and a bug if it shows up in test data), not the NULL marker.

**Source:** `relational-database-concepts.md`
</details>

---

### 2. Why is `order_id` a good primary key for the `orders` table, while `customer_name` would be a poor one?
- [ ] A) Because `order_id` is the first column in the table
- [ ] B) Because `order_id` is a number, and only numeric columns can be primary keys
- [ ] C) Because the database sorts the table by whichever column is the primary key
- [ ] D) Because `order_id` uniquely identifies each row and is never NULL, whereas names can repeat (Alice Johnson appears twice)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Because `order_id` uniquely identifies each row and is never NULL, whereas names can repeat (Alice Johnson appears twice)

**Explanation:** A primary key is the "ID card" of a row: unique and never NULL. `customer_name` is unsuitable because two rows can share a name (orders 1001 and 1009 are both Alice Johnson), and names can change or be misspelt.
- **Why others are wrong:**
  - A) Column position has nothing to do with being a key.
  - B) Keys are about uniqueness, not data type; the lesson does not limit keys to numbers.
  - C) A table is a set of rows with no guaranteed order; the key does not guarantee sorted output (only `ORDER BY` does).

**Source:** `relational-database-concepts.md`
</details>

---

### 3. A column stores quantities as **text**. When sorted ascending, `'10'` appears before `'9'`. Why?
- [ ] A) Because 10 is numerically smaller than 9
- [ ] B) Text is compared character by character, and `'1'` sorts before `'9'`, so numbers belong in numeric columns
- [ ] C) Because `ORDER BY` ignores data types and always uses insertion order
- [ ] D) Because SQLite has a bug that other engines avoid

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Text is compared character by character, and `'1'` sorts before `'9'`, so numbers belong in numeric columns

**Explanation:** The data type decides how comparison and sorting work. Text `'10'` starts with the character `'1'`, which sorts before `'9'`, while the number 10 is larger than 9.
- **Why others are wrong:**
  - A) As numbers, 10 is bigger than 9; the odd order only appears when the values are stored as text.
  - C) `ORDER BY` respects the column's type and collation; it never falls back to insertion order.
  - D) Every engine sorts text this way; the lesson's advice is to store numbers in numeric columns.

**Source:** `relational-database-concepts.md`
</details>

---

### 4. Which statement about SQLite compared with MySQL or PostgreSQL is correct?
- [ ] A) SQLite needs a separate database server running, just like PostgreSQL
- [ ] B) SQLite enforces column data types more strictly than MySQL
- [ ] C) SQLite uses the T-SQL dialect, so it limits rows with `TOP`
- [ ] D) SQLite is embedded: the whole database is one file that your program opens directly, with no server needed

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) SQLite is embedded: the whole database is one file that your program opens directly, with no server needed

**Explanation:** SQLite is an embedded engine bundled with Python, which is why it needs nothing installed for practice. That also makes it lenient about types, so validation matters more, not less.
- **Why others are wrong:**
  - A) That describes client/server products; SQLite has no server process.
  - B) The opposite is true: SQLite uses type affinity, so a declared type is more of a preference, while MySQL is much stricter.
  - C) T-SQL and `TOP` belong to Microsoft SQL Server; SQLite uses `LIMIT`.

**Source:** `relational-database-concepts.md`
</details>

---

### 5. Which pairing of SQL command family and statement is correct?
- [ ] A) `SELECT` is DQL (Data Query Language), while `INSERT`, `UPDATE` and `DELETE` are DML (Data Manipulation Language)
- [ ] B) `SELECT` is DML, and `INSERT` is DDL
- [ ] C) `SELECT` is DCL, because it controls who can see data
- [ ] D) `SELECT` is DDL, because it defines the structure of the result

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `SELECT` is DQL (Data Query Language), while `INSERT`, `UPDATE` and `DELETE` are DML (Data Manipulation Language)

**Explanation:** Today is almost entirely read-only DQL, which is safe for exploring a test database; data-changing DML comes on Friday.
- **Why others are wrong:**
  - B) `INSERT` changes data (DML), and DDL defines structure (`CREATE TABLE`, `ALTER`, `DROP`).
  - C) DCL means `GRANT` and `REVOKE` (permissions); `SELECT` simply reads data.
  - D) DDL defines the structure of tables, not of a result set; `SELECT` is the read-only query statement.

**Source:** `relational-database-concepts.md`
</details>

---

### 6. Which `WHERE` clause correctly finds the order placed by `Jack O'Brien` (order 1011)?
- [ ] A) `WHERE customer_name = 'Jack O''Brien';`
- [ ] B) `WHERE customer_name = 'Jack O\'Brien';`
- [ ] C) `WHERE customer_name = "Jack O'Brien";`
- [ ] D) `WHERE customer_name = 'Jack O'Brien';`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `WHERE customer_name = 'Jack O''Brien';`

**Explanation:** Text literals are wrapped in single quotes, and a literal apostrophe inside the text is written by doubling it (`''`). The database reads `'Jack O''Brien'` as the text `Jack O'Brien`.
- **Why others are wrong:**
  - B) A backslash is not the standard way to escape an apostrophe in SQL; the lesson's rule is to double it.
  - C) Double quotes are for identifiers (table/column names) in standard SQL, not for text values.
  - D) The apostrophe ends the text early, leaving `Brien';` behind, which causes `near "Brien": syntax error`.

**Source:** `sql-syntax.md`
</details>

---

### 7. A trainee forgets the comma and runs this query. What happens?
```sql
SELECT order_id customer_name
FROM orders
WHERE order_id = 1001;
```
- [ ] A) A syntax error: `near "customer_name"`
- [ ] B) Two columns come back: `order_id` and `customer_name`
- [ ] C) One column comes back, headed `customer_name`, containing the value `1001`
- [ ] D) No rows come back, because the query is ambiguous

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) One column comes back, headed `customer_name`, containing the value `1001`

**Explanation:** `AS` is optional, so SQL reads `customer_name` as an alias for `order_id`. There is no error at all, which is why you should always check the column headings of your result.
- **Why others are wrong:**
  - A) This is the "sneaky" case: the statement is valid, so no error is raised.
  - B) Without a comma there is only one select-list item, so only one column is returned.
  - D) The `WHERE` clause still matches order 1001, so one row is returned.

**Source:** `sql-syntax.md`
</details>

---

### 8. In what order does the database logically **process** the clauses of `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT`?
- [ ] A) `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`
- [ ] B) `FROM`, `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
- [ ] C) `FROM`, `WHERE`, `SELECT`, `ORDER BY`, `LIMIT`
- [ ] D) `WHERE`, `FROM`, `SELECT`, `LIMIT`, `ORDER BY`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `FROM`, `WHERE`, `SELECT`, `ORDER BY`, `LIMIT`

**Explanation:** The database finds the table, throws away non-matching rows, computes the select list (and aliases), sorts what remains, and finally cuts the result off.
- **Why others are wrong:**
  - A) That is the order the clauses are *written*, not the order they are processed.
  - B) `WHERE` runs before `SELECT`, which is why a `SELECT` alias cannot be used in `WHERE` in standard SQL.
  - D) The table must be located first (`FROM`), and sorting must happen before cutting off rows with `LIMIT`.

**Source:** `sql-syntax.md`
</details>

---

### 9. Run on PostgreSQL, what happens with this query?
```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE line_total > 1000;
```
- [ ] A) It fails with an unknown-column error, because `WHERE` is processed before `SELECT` creates the alias; repeat the expression instead
- [ ] B) It works, because aliases are defined in `SELECT`, which is written first
- [ ] C) It works but returns the rows unsorted
- [ ] D) It works only if an `ORDER BY line_total` is added

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It fails with an unknown-column error, because `WHERE` is processed before `SELECT` creates the alias; repeat the expression instead

**Explanation:** Standard engines (PostgreSQL, MySQL, SQL Server, Oracle) reject the alias in `WHERE`. SQLite is lenient and would accept it, which is another reason to write portable SQL.
- **Why others are wrong:**
  - B) Written order is not processing order; the alias does not exist yet when `WHERE` runs.
  - C) It does not work in standard SQL at all; sorting has nothing to do with the problem.
  - D) `ORDER BY` can use the alias, but adding it does not make the alias visible to `WHERE`.

**Source:** `sql-syntax.md`
</details>

---

### 10. You port `SELECT customer_name || ' (' || country || ')' FROM orders;` from SQLite to MySQL in its default mode. What should you do?
- [ ] A) Nothing: `||` is the standard concatenation operator on every database
- [ ] B) Rewrite it with `CONCAT(customer_name, ' (', country, ')')`, because in MySQL `||` means OR
- [ ] C) Use the `+` operator, which MySQL uses for text
- [ ] D) Wrap each piece in double quotes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Rewrite it with `CONCAT(customer_name, ' (', country, ')')`, because in MySQL `||` means OR

**Explanation:** Concatenation is a classic dialect difference: `||` in SQLite, PostgreSQL and Oracle, `CONCAT()` in MySQL, and `+` or `CONCAT()` in SQL Server.
- **Why others are wrong:**
  - A) MySQL (default mode) treats `||` as a logical OR, so the query would not concatenate.
  - C) `+` is SQL Server's text operator; in MySQL it is only arithmetic.
  - D) Double quotes are for identifiers in standard SQL and do not join text.

**Source:** `sql-syntax.md`
</details>

---

### 11. What does this query return in the `contact` column for order 1004 (David Lee, whose `email` is NULL)?
```sql
SELECT order_id, customer_name || ' <' || email || '>' AS contact
FROM orders
WHERE order_id = 1004;
```
- [ ] A) `David Lee <>`
- [ ] B) `David Lee <NULL>`
- [ ] C) An error, because you cannot concatenate a NULL
- [ ] D) `NULL`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `NULL`

**Explanation:** NULL propagates: any arithmetic or concatenation involving NULL produces NULL, because "known text glued to unknown text" is unknown. Wrapping the column in `COALESCE(email, 'no email')` would supply a default.
- **Why others are wrong:**
  - A) That would treat NULL as an empty string, which SQLite's `||` does not do.
  - B) The word `NULL` is never inserted as text.
  - C) The expression is valid; it simply evaluates to NULL.

**Source:** `select-statements.md`
</details>

---

### 12. A teammate's automated test reads `row[5]` from a `SELECT *` result to get the quantity. What is the main risk, and the better approach?
- [ ] A) `SELECT *` is a syntax error inside Python's `sqlite3` module
- [ ] B) `SELECT *` modifies the table while it reads
- [ ] C) `SELECT *` returns only the first column, so `row[5]` raises an error
- [ ] D) If someone adds, removes or reorders a column, index 5 silently points at the wrong value; select named columns and read them by name

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) If someone adds, removes or reorders a column, index 5 silently points at the wrong value; select named columns and read them by name

**Explanation:** Use `*` for exploring and named columns (with a dict-style row such as `row["quantity"]`) for anything you keep. Named columns make the test stable and self-documenting.
- **Why others are wrong:**
  - A) `SELECT *` is valid SQL and runs fine from Python; the problem is fragility, not syntax.
  - B) `SELECT` is read-only and never changes stored data.
  - C) `*` returns every column; the issue is that the position of each column can change.

**Source:** `select-statements.md`
</details>

---

### 13. What does this query return, and what happens to the table afterwards?
```sql
SELECT unit_price AS price, order_id
FROM orders
WHERE order_id = 1002;
```
- [ ] A) The columns come back in the table's definition order, `order_id` first
- [ ] B) One row with columns in the written order (`price` = 25.5, then `order_id` = 1002); the table itself is unchanged
- [ ] C) The table's column is permanently renamed to `price`
- [ ] D) An error, because `AS` can only be used on calculated columns

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) One row with columns in the written order (`price` = 25.5, then `order_id` = 1002); the table itself is unchanged

**Explanation:** A `SELECT` list controls which columns appear, in which order, and under which names, while `SELECT` itself never changes the stored data.
- **Why others are wrong:**
  - A) A column list controls the order of the result; only `*` follows the table's definition order.
  - C) An alias exists only in the result set; nothing is stored or renamed.
  - D) `AS` works on any column or expression.

**Source:** `select-statements.md`
</details>

---

### 14. In a Python test you write `conn.execute("SELECT * FROM orders WHERE order_id = ?", (1001,))`. Why the `?` and the trailing comma in `(1001,)`?
- [ ] A) The comma separates two parameters, `1001` and an empty one
- [ ] B) `?` tells SQLite to ignore rows with NULL values
- [ ] C) `?` is a placeholder that the library fills in safely, avoiding quoting bugs and SQL injection, and the trailing comma makes a one-element tuple
- [ ] D) SQLite cannot parse numbers written directly in the SQL text

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `?` is a placeholder that the library fills in safely, avoiding quoting bugs and SQL injection, and the trailing comma makes a one-element tuple

**Explanation:** Parameterised queries let the database library handle quoting, so a value such as `O'Brien` cannot break the statement or inject SQL.
- **Why others are wrong:**
  - A) There is only one parameter; the comma is what turns `(1001)` into a tuple instead of a plain number.
  - B) `?` has nothing to do with NULL; it marks where a parameter value goes.
  - D) SQLite reads number literals perfectly well; placeholders are about safe handling of values.

**Source:** `select-statements.md`
</details>

---

### 15. Why do the lessons warn against storing money in `REAL` (floating-point) columns?
- [ ] A) Binary floating point cannot represent values like 0.1 exactly, which is a classic source of one-cent defects; exact `DECIMAL` types are preferred
- [ ] B) `REAL` columns reject values with two decimal places
- [ ] C) `ROUND` is not available on `REAL` columns
- [ ] D) `DECIMAL` stores money as text, which sorts correctly

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Binary floating point cannot represent values like 0.1 exactly, which is a classic source of one-cent defects; exact `DECIMAL` types are preferred

**Explanation:** We use `REAL` for convenience in SQLite, but production systems use `DECIMAL(10,2)` and compare calculated values with a tolerance.
- **Why others are wrong:**
  - B) `REAL` happily stores 9.99; the issue is tiny rounding errors.
  - C) `ROUND(unit_price * 1.0825, 2)` works on `REAL` values, as the lesson shows.
  - D) `DECIMAL(p,s)` is an exact numeric type, not text.

**Source:** `select-statements.md`
</details>

---

### 16. What is special about how Oracle treats an empty string `''`?
- [ ] A) Oracle forbids empty strings and rejects the statement
- [ ] B) Oracle treats `''` as NULL, unlike all the other major databases
- [ ] C) Oracle treats NULL as an empty string during concatenation
- [ ] D) Oracle treats `''` as the number 0

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Oracle treats `''` as NULL, unlike all the other major databases

**Explanation:** This is why a `TRIM(email) = ''` check is never true on Oracle, and why null-handling must always be tested on your actual engine.
- **Why others are wrong:**
  - A) Oracle accepts it, but stores it as NULL.
  - C) That is the reverse; the lesson says Oracle turns an empty string into NULL.
  - D) An empty string is never converted to 0; it becomes NULL.

**Source:** `select-statements.md`
</details>

---

### 17. Which condition is exactly equivalent to `country IN ('UK', 'Mexico')`?
- [ ] A) `country = 'UK' OR country = 'Mexico'`
- [ ] B) `country = 'UK' AND country = 'Mexico'`
- [ ] C) `country BETWEEN 'UK' AND 'Mexico'`
- [ ] D) `country LIKE 'UK%Mexico'`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `country = 'UK' OR country = 'Mexico'`

**Explanation:** `IN` is shorthand for several `OR`s on the same column: shorter and easier to read for long lists.
- **Why others are wrong:**
  - B) One cell cannot equal two different values at once, so this returns nothing.
  - C) `BETWEEN` is a range, not a list; and here the bounds are even reversed (alphabetically `'UK'` is after `'Mexico'`), so it returns no rows.
  - D) This pattern would require one value containing both words in that order.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 18. A trainee wants prices from 25 to 300 and writes `WHERE unit_price BETWEEN 300 AND 25`. What happens?
- [ ] A) The database swaps the bounds automatically and returns prices 25 to 300
- [ ] B) It raises a syntax error
- [ ] C) It returns no rows, because no value is both at least 300 and at most 25
- [ ] D) It returns every row

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It returns no rows, because no value is both at least 300 and at most 25

**Explanation:** Reversed `BETWEEN` bounds silently return zero rows. Always write the low value first.
- **Why others are wrong:**
  - A) SQL does not reorder the bounds; `BETWEEN` means `>= low AND <= high` exactly as written.
  - B) The statement is valid, which is what makes it a silent bug.
  - D) Nothing satisfies both halves of the condition, so every row is rejected.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 19. What does this query return?
```sql
SELECT order_id
FROM orders
WHERE status NOT IN ('PENDING', NULL);
```
- [ ] A) All orders that are not pending
- [ ] B) An error, because NULL is not allowed inside a list
- [ ] C) Only the orders whose status is NULL
- [ ] D) No rows at all, because a NULL in a `NOT IN` list makes the condition UNKNOWN for every row

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) No rows at all, because a NULL in a `NOT IN` list makes the condition UNKNOWN for every row

**Explanation:** A single NULL in a `NOT IN` list ruins the whole condition. Never put NULLs in `IN` lists.
- **Why others are wrong:**
  - A) That is what the author intended, but the NULL in the list prevents it.
  - B) The statement is valid; it simply never evaluates to TRUE.
  - C) `status NOT IN (..., NULL)` expands to `status <> 'PENDING' AND status <> NULL`; the second part is always UNKNOWN, so even NULL rows are rejected.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 20. Which query returns "the most recently placed order", and returns it reliably even if two orders share the same date?
- [ ] A) `SELECT order_id, order_date FROM orders ORDER BY order_date LIMIT 1;`
- [ ] B) `SELECT order_id, order_date FROM orders ORDER BY order_date DESC, order_id DESC LIMIT 1;`
- [ ] C) `SELECT order_id, order_date FROM orders LIMIT 1 ORDER BY order_date DESC;`
- [ ] D) `SELECT order_id, order_date FROM orders ORDER BY order_date DESC;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `SELECT order_id, order_date FROM orders ORDER BY order_date DESC, order_id DESC LIMIT 1;`

**Explanation:** `DESC` puts the newest date first, `LIMIT 1` keeps only that row, and the second sort key `order_id DESC` is a unique tiebreaker that makes the result deterministic. This `ORDER BY ... DESC LIMIT 1` pattern is how a test finds the order it just created.
- **Why others are wrong:**
  - A) Ascending order puts the *oldest* order first, so this returns order 1001.
  - C) `LIMIT` must be written after `ORDER BY`; this clause order is a syntax error.
  - D) With no `LIMIT`, all 15 rows come back, not just the latest one.

**Source:** `basic-query-construction.md`
</details>

---

### 21. You build a query one clause at a time (`FROM`, then `SELECT`, then `WHERE`, then `ORDER BY`), running it after each addition. After adding the `WHERE` line, the result suddenly looks wrong. Where should you look first?
- [ ] A) At the `WHERE` condition you just added
- [ ] B) At the `FROM` clause, because it was written first
- [ ] C) Nowhere in particular; the whole query has to be rewritten from scratch
- [ ] D) At the `ORDER BY` clause, even though you have not written it yet

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) At the `WHERE` condition you just added

**Explanation:** The point of building incrementally is that the defect is always in the last thing you added. If you had written all four clauses at once you would have four suspects instead of one.
- **Why others are wrong:**
  - B) `FROM` already ran correctly in the previous step.
  - C) Rewriting throws away the advantage of the step-by-step method.
  - D) A clause that does not exist yet cannot be the cause.

**Source:** `basic-query-construction.md`
</details>

---

### 22. A query with five conditions returns nothing. What is the "peel the onion" technique?
- [ ] A) Add more `OR` branches until rows appear
- [ ] B) Replace the `WHERE` clause with `SELECT *` and give up filtering
- [ ] C) Rewrite the whole query from scratch in one go
- [ ] D) Remove or comment out the conditions one at a time and re-run until rows appear; the last condition removed is the culprit

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Remove or comment out the conditions one at a time and re-run until rows appear; the last condition removed is the culprit

**Explanation:** This is the same one-change-at-a-time discipline as incremental building, applied in reverse to a query that returns too few rows.
- **Why others are wrong:**
  - A) This widens the query and hides which condition is wrong.
  - B) You lose the information you need; the aim is to find the faulty condition.
  - C) Rewriting everything at once gives you many suspects instead of one.

**Source:** `basic-query-construction.md`
</details>

---

### 23. Your query is meant to find the order your automated test just created, and it returns an empty result. What does that mean?
- [ ] A) It always means the test passed
- [ ] B) It means the table is empty, which is never possible
- [ ] C) It is a failure: the expected row is missing, whereas for a "find bad data" query an empty result is the goal
- [ ] D) It means the query has a syntax error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is a failure: the expected row is missing, whereas for a "find bad data" query an empty result is the goal

**Explanation:** Always know in advance whether you expect zero, one or many rows. The same empty result means success for one query and failure for another.
- **Why others are wrong:**
  - A) Only for violation queries; here you expected a row to exist.
  - B) An empty result can have many causes (wrong filter, wrong environment, row not saved); it does not prove the table is empty.
  - D) A syntax error produces an error message, not an empty result.

**Source:** `basic-query-construction.md`
</details>

---

### 24. The business rule says "quantity must be at least 1". Which is the correct **violation query** (the query whose rows are the defects)?
- [ ] A) `SELECT order_id, quantity FROM orders WHERE quantity >= 1;`
- [ ] B) `SELECT order_id, quantity FROM orders WHERE quantity = NULL;`
- [ ] C) `SELECT order_id, quantity FROM orders WHERE quantity < 1;`
- [ ] D) `SELECT order_id, quantity FROM orders WHERE quantity > 1;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `SELECT order_id, quantity FROM orders WHERE quantity < 1;`

**Explanation:** A violation query describes the *opposite* of the rule, so that an empty result means the data passes. Here it returns orders 1007 (quantity 0) and 1011 (quantity -1), so the data fails the rule.
- **Why others are wrong:**
  - A) That describes the rows that *obey* the rule, not the defects.
  - B) `= NULL` never matches anything (it is never true), and it tests the wrong thing anyway.
  - D) That excludes legitimate quantity-1 orders and misses the actual violations (0 and -1).

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---

### 25. Rule V-03b is written as `WHERE quantity NOT BETWEEN 1 AND 100 OR quantity IS NULL`. Why does it need the `OR quantity IS NULL` part?
- [ ] A) Because `BETWEEN` excludes its end values, so NULL has to be added by hand
- [ ] B) Because for a NULL quantity `NOT BETWEEN` evaluates to UNKNOWN, and `WHERE` keeps only TRUE, so a missing quantity would be silently skipped
- [ ] C) Because SQL treats NULL as equal to 0, which is outside the 1 to 100 range
- [ ] D) Because `IS NULL` makes the query run faster

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because for a NULL quantity `NOT BETWEEN` evaluates to UNKNOWN, and `WHERE` keeps only TRUE, so a missing quantity would be silently skipped

**Explanation:** Any comparison with NULL is UNKNOWN, and rows whose condition is UNKNOWN are dropped. A completeness gap (missing quantity) would therefore pass the range check unnoticed unless you test for it explicitly.
- **Why others are wrong:**
  - A) `BETWEEN` is inclusive of both ends; that is not the reason.
  - C) NULL is not zero; it means unknown.
  - D) The extra condition is about correctness, not speed.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---

### 26. The lessons report 7 dirty rows and 8 clean rows from the 15-row `orders` table. Why is it useful to check that 7 + 8 = 15?
- [ ] A) It reconciles your own validation: if the totals did not add up, some rows would be falling through a gap (often a NULL) in your conditions
- [ ] B) SQL requires the dirty and clean counts to sum to the table size
- [ ] C) It proves every row in the table is valid
- [ ] D) It is the only way to count rows with `COUNT(*)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It reconciles your own validation: if the totals did not add up, some rows would be falling through a gap (often a NULL) in your conditions

**Explanation:** Rows with NULL values are the usual cause of missing rows, because comparisons with NULL are UNKNOWN. Reconciliation is a good validation of your own validation.
- **Why others are wrong:**
  - B) SQL does not require this; it is a sanity check you choose to make.
  - C) Seven rows are dirty, so the data is far from valid.
  - D) The check is about confidence in your queries, not about how counting works.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---

### 27. Rule V-02 is written `WHERE email IS NOT NULL AND email NOT LIKE '%@%.%'`. Why include `email IS NOT NULL`?
- [ ] A) Because without it `NOT LIKE` would raise an error on NULL values
- [ ] B) Because `IS NOT NULL` makes `LIKE` case-insensitive
- [ ] C) So that each defect is reported by one rule only: the NULL emails belong to V-01, and being explicit makes the intent clear
- [ ] D) Because `LIKE` can only be used with non-NULL columns declared `NOT NULL`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) So that each defect is reported by one rule only: the NULL emails belong to V-01, and being explicit makes the intent clear

**Explanation:** The query returns only order 1006 (`frank.moore@example`) either way. The extra clause documents that missing emails are V-01's job.
- **Why others are wrong:**
  - A) `NULL NOT LIKE ...` is simply UNKNOWN, not an error, so those rows would just not match.
  - B) `IS NOT NULL` has no effect on case rules.
  - D) `LIKE` works on any text column; the extra condition is about clarity and avoiding double reporting.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---


## Part 2: True / False

### 28. True or False: If you run `SELECT * FROM orders;` with no `ORDER BY`, the database guarantees the rows come back in the order they were inserted.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A table is conceptually an unordered set of rows. You may *see* insertion order on your laptop, but only `ORDER BY` guarantees an order, so a test must never rely on it (use `ORDER BY` or look the row up by its key).

**Source:** `relational-database-concepts.md`
</details>

---

### 29. True or False: A relational table cell may hold the list `Laptop, Mouse, Keyboard` when an order contains three products, because a cell can hold any text.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Each cell holds one value. If an order has three products the design uses more rows or another table, which keeps data predictable and testable.

**Source:** `relational-database-concepts.md`
</details>

---

### 30. True or False: In the `orders` table, `customer_name` is declared `NOT NULL` while `email` is not, which is why two orders can have no email but no order can lack a customer name.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `customer_name TEXT NOT NULL` is a constraint requiring a value, whereas `email TEXT` allows NULL, so orders 1004 and 1014 can have a missing email.

**Source:** `relational-database-concepts.md`
</details>

---

### 31. True or False: In SQLite, `SELECT order_id FROM orders WHERE status = 'DELIVERED';` also returns order 1008, whose status is stored as `delivered` in lower case.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** In SQLite (and PostgreSQL and Oracle) text comparison with `=` is case-sensitive, so the query returns only the five upper-case rows (1001, 1003, 1009, 1012, 1015). MySQL and SQL Server default to case-insensitive comparison and *would* return 1008, which is why the same query can give different answers on different engines.

**Source:** `sql-syntax.md`
</details>

---

### 32. True or False: `WHERE quantity == 0` is valid on every major database because it matches Python's equality operator.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** SQLite is lenient and accepts `==`, but PostgreSQL, MySQL and SQL Server do not. Always use a single `=` so the SQL is portable.

**Source:** `sql-syntax.md`
</details>

---

### 33. True or False: Any arithmetic or concatenation that involves a NULL value produces NULL.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** NULL means "unknown", and "unknown + 1" is still unknown. That is why `customer_name || ' <' || email || '>'` is NULL for orders with a NULL email, and why `COALESCE` is used to supply a default.

**Source:** `select-statements.md`
</details>

---

### 34. True or False: `SELECT DISTINCT status FROM orders;` returns `delivered` and `DELIVERED` as two separate values.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** DISTINCT compares exact values, and SQLite text comparison is case-sensitive, so the result has five values. Spotting such variants is a real validation win.

**Source:** `select-statements.md`
</details>

---

### 35. True or False: `SELECT order_id, email FROM orders WHERE email <> 'alice.j@example.com';` silently skips the orders whose email is NULL, even though a missing email is certainly "not Alice's".
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** For a NULL email the condition `NULL <> 'alice.j@example.com'` is UNKNOWN, and `WHERE` keeps only rows where the condition is TRUE. If you want NULL rows included you must say so: `WHERE email <> '...' OR email IS NULL`.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 36. True or False: In SQLite, `WHERE product LIKE 'laptop'` returns no rows because `LIKE` is case-sensitive.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** SQLite's `LIKE` is case-insensitive for ordinary English letters, so it matches orders 1001 and 1006. PostgreSQL and Oracle are case-sensitive; for portable code write `LOWER(product) LIKE 'laptop'`.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 37. True or False: `NULL IS NULL` evaluates to TRUE, while `NULL = NULL` evaluates to UNKNOWN.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Comparisons with NULL give UNKNOWN, which is why `= NULL` never finds anything. `IS NULL` is the special test designed for missing values.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 38. True or False: `SELECT order_id, email FROM orders WHERE email NOT LIKE '%@%.%';` on its own will list the orders whose email is NULL (1004 and 1014) as well as the malformed email on order 1006.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** For a NULL email, `NULL NOT LIKE ...` is UNKNOWN, so those rows are dropped. The query returns only order 1006 (`frank.moore@example`). To catch the NULLs too you need a separate `email IS NULL` branch joined with `OR`.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---

### 39. True or False: A violation query that returns zero rows may still be wrong, for example `WHERE email = NULL`, so you should test each rule against data you know is bad.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Zero rows might mean "no problems" or "my query is faulty". Catching the planted defects proves the rule can fail, the same idea as making a unit test fail first.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---


## Part 3: Query Result Prediction

### 40. What does this query return in SQLite?
```sql
SELECT 7 / 2 AS int_division, 7 / 2.0 AS decimal_division;
```
- [ ] A) `3.5` and `3.5`
- [ ] B) `3` and `3`
- [ ] C) `3` and `3.5`
- [ ] D) An error, because there is no `FROM` clause

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `3` and `3.5`

**Explanation:** In SQLite, dividing two integers gives an integer (the decimal part is dropped), so `7 / 2` is `3`. Making one operand a decimal (`2.0`) gives `3.5`. A query with no `FROM` is allowed in SQLite when you only want to calculate something.
- **Why others are wrong:**
  - A) That is MySQL-style `/` behaviour for integers, not SQLite.
  - B) `7 / 2.0` involves a decimal, so it is not truncated.
  - D) SQLite (and most engines other than Oracle) accept a `SELECT` with no table.

**Source:** `sql-syntax.md`
</details>

---

### 41. What does this query return in SQLite?
```sql
SELECT 10 / 4 AS a, 10 % 4 AS b, 10 / 4.0 AS c;
```
- [ ] A) `2.5`, `2` and `2.5`
- [ ] B) `2`, `0` and `2.5`
- [ ] C) `2`, `2` and `2`
- [ ] D) `2`, `2` and `2.5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `2`, `2` and `2.5`

**Explanation:** Integer division drops the decimal part, `%` is the remainder (modulo), and making one operand a decimal gives a decimal result.
- **Why others are wrong:**
  - A) Dividing two integers in SQLite gives an integer, so `10 / 4` is 2, not 2.5.
  - B) `%` returns the remainder of the division: 10 = 2 x 4 + 2, so the remainder is 2, not 0.
  - C) `10 / 4.0` has a decimal operand, so the decimal part is kept and the result is 2.5.

**Source:** `sql-syntax.md`
</details>

---

### 42. Which rows does this query return, in this order?
```sql
SELECT order_id
FROM orders
-- WHERE country = 'UK'
ORDER BY order_id DESC
LIMIT 2;
```
- [ ] A) 1015, 1014
- [ ] B) 1011, 1008
- [ ] C) 1001, 1002
- [ ] D) A syntax error, because a comment cannot appear inside a statement

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 1015, 1014

**Explanation:** Everything after `--` on a line is ignored, so there is no filter. The two highest ids are 1015 and 1014. Accidentally commenting out an important `WHERE` line is a common beginner mistake.
- **Why others are wrong:**
  - B) That would be the result if the `WHERE country = 'UK'` line were active (UK orders are 1005, 1008, 1011); it is commented out.
  - C) That is ascending order; `DESC` puts the highest `order_id` first.
  - D) Comments are ignored by the database wherever they appear, so the statement is valid.

**Source:** `sql-syntax.md`
</details>

---

### 43. Which rows does this query return?
```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE order_id IN (1003, 1007, 1011);
```
- [ ] A) `1003 | 49.95`, `1007 | 0.0`, `1011 | 25.5`
- [ ] B) `1003 | 5`, `1007 | 0`, `1011 | -1`
- [ ] C) `1003 | 49.95` and `1007 | 0.0` only, because a negative total is filtered out
- [ ] D) `1003 | 49.95`, `1007 | 0.0`, `1011 | -25.5`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1003 | 49.95`, `1007 | 0.0`, `1011 | -25.5`

**Explanation:** The expression is computed per row: 5 x 9.99 = 49.95, 0 x 49.99 = 0.0, and (-1) x 25.5 = -25.5. The negative total exposes the planted negative-quantity defect on order 1011. The `WHERE` only filters by `order_id`, not by the sign of the total.
- **Why others are wrong:**
  - A) The sign is wrong: a negative quantity gives a negative total.
  - B) Those are just the quantities, not the product of quantity and price.
  - C) Nothing in the `WHERE` clause removes negative totals; all three listed IDs match.

**Source:** `select-statements.md`
</details>

---

### 44. What does this query return?
```sql
SELECT order_id, quantity * unit_price AS line_total
FROM orders
WHERE category = 'Home Office'
ORDER BY line_total DESC;
```
- [ ] A) `1008 | 59.97`, `1010 | 220.0`, `1014 | 450.0`
- [ ] B) `1014 | 450.0`, `1010 | 220.0`, `1008 | 59.97`
- [ ] C) `1014 | 450.0`, `1010 | 220.0`, `1008 | 19.99`
- [ ] D) `1014 | 450.0`, `1010 | 220.0`, `1009 | 150.0`, `1008 | 59.97`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `1014 | 450.0`, `1010 | 220.0`, `1008 | 59.97`

**Explanation:** Three orders are in the Home Office category (1008, 1010 and 1014). Each line total is calculated per row at query time, then sorted descending.
- **Why others are wrong:**
  - A) `DESC` sorts the biggest value first; this list is in ascending order.
  - C) 19.99 is the unit price; the line total of order 1008 is 3 x 19.99 = 59.97.
  - D) Order 1009 is Headphones in the Electronics category, so the `WHERE` clause removes it.

**Source:** `select-statements.md`
</details>

---

### 45. How many rows does this query return, and which ones?
```sql
SELECT order_id, country, status
FROM orders
WHERE status = 'PENDING' OR status = 'SHIPPED' AND country = 'UK';
```
- [ ] A) 1 row: order 1011
- [ ] B) 4 rows: orders 1004, 1007, 1011 and 1014
- [ ] C) 0 rows
- [ ] D) 8 rows: every pending and every shipped order

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 4 rows: orders 1004, 1007, 1011 and 1014

**Explanation:** `AND` binds tighter than `OR`, so the condition means `status = 'PENDING' OR (status = 'SHIPPED' AND country = 'UK')`. All four pending orders match (from USA, USA, UK, Mexico), and no shipped order is from the UK, so nothing else is added. Parentheses around the `OR` would have given only order 1011.
- **Why others are wrong:**
  - A) That is the result of the *parenthesised* version `(PENDING OR SHIPPED) AND UK`, not of this query.
  - C) Pending orders certainly exist, so the result is not empty.
  - D) That would require `status = 'SHIPPED'` to match without the country condition, but it is tied to `AND country = 'UK'`.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 46. How many rows does this query return?
```sql
SELECT order_id
FROM orders
WHERE order_date BETWEEN '2025-01-10' AND '2025-01-20';
```
- [ ] A) 4 rows: orders 1003, 1004, 1005 and 1006
- [ ] B) 3 rows: orders 1004, 1005 and 1006
- [ ] C) 2 rows: orders 1004 and 1005
- [ ] D) 0 rows, because dates are text and cannot be compared

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 4 rows: orders 1003, 1004, 1005 and 1006

**Explanation:** `BETWEEN` is inclusive at both ends, so the orders dated exactly 2025-01-10 (1003) and exactly 2025-01-20 (1006) are included, along with 1004 (01-12) and 1005 (01-15).
- **Why others are wrong:**
  - B) That drops the lower bound; `BETWEEN` includes it.
  - C) That drops both bounds, which would be `>` and `<` instead of `BETWEEN`.
  - D) ISO dates (`YYYY-MM-DD`) stored as text sort in chronological order, so comparisons work.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 47. Which rows does this query return?
```sql
SELECT order_id
FROM orders
WHERE status NOT IN ('DELIVERED', 'SHIPPED')
  AND country IN ('UK', 'Mexico')
ORDER BY order_id;
```
- [ ] A) 1005, 1011, 1014
- [ ] B) 1004, 1005, 1007, 1008, 1011, 1014
- [ ] C) 1005, 1008, 1011, 1014
- [ ] D) 1005, 1008, 1010, 1011, 1014

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 1005, 1008, 1011, 1014

**Explanation:** UK and Mexico orders are 1005, 1008, 1010, 1011 and 1014. Removing the `SHIPPED` one (1010) leaves four, including the lower-case `delivered` defect.
- **Why others are wrong:**
  - A) Order 1008 has status `delivered` in lower case, which is not equal to `'DELIVERED'` in SQLite, so it passes the `NOT IN` test.
  - B) That ignores the country condition; orders 1004 and 1007 are from the USA.
  - D) Order 1010 is from Mexico but its status is `SHIPPED`, which is in the excluded list.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 48. Which rows does this query return?
```sql
SELECT order_id
FROM orders
WHERE email NOT IN ('alice.j@example.com', 'bob.smith@example.com')
  AND order_id <= 1005
ORDER BY order_id;
```
- [ ] A) 1003, 1005
- [ ] B) 1003, 1004, 1005
- [ ] C) 1004 only
- [ ] D) No rows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 1003, 1005

**Explanation:** Orders 1001 and 1002 are excluded by the list, 1004 is silently skipped because its email is NULL, leaving 1003 and 1005. Add `OR email IS NULL` if NULL rows should count.
- **Why others are wrong:**
  - B) Order 1004 has a NULL email, so `NULL NOT IN (...)` is UNKNOWN and the row is dropped.
  - C) The NULL row is exactly the one that is skipped; the rows with real, different emails are kept.
  - D) There is no NULL inside the list, so the NULL-in-list trap does not apply; the rows with other emails are returned.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 49. Which rows does this query return, in this order?
```sql
SELECT order_id
FROM orders
WHERE unit_price > 0
ORDER BY unit_price, order_id
LIMIT 3;
```
- [ ] A) 1015, 1003, 1013
- [ ] B) 1001, 1006, 1014
- [ ] C) 1003, 1013, 1008
- [ ] D) 1003, 1008, 1013

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 1003, 1013, 1008

**Explanation:** The three cheapest non-zero prices are 9.99 (orders 1003 and 1013, tied, so `order_id` breaks the tie) and then 19.99 (order 1008). Order 1015 costs 0.0, so `WHERE unit_price > 0` filters it out *before* sorting and limiting.
- **Why others are wrong:**
  - A) That includes order 1015, whose price of 0.0 is excluded by the `WHERE` clause.
  - B) Those are the three *most* expensive orders, which would need `DESC`.
  - D) Order 1008 costs 19.99, which is more than 9.99, so it sorts after 1013.

**Source:** `basic-query-construction.md`
</details>

---

### 50. What does this query return?
```sql
SELECT DISTINCT country
FROM orders
WHERE category = 'Accessories'
ORDER BY country;
```
- [ ] A) `Canada`, `Mexico`, `UK`, `USA`
- [ ] B) `Canada`, `UK`, `USA`
- [ ] C) `Canada`, `Canada`, `UK`, `UK`, `USA`, `USA`
- [ ] D) `USA`, `UK`, `Canada`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `Canada`, `UK`, `USA`

**Explanation:** The six Accessories orders ship to USA, Canada, UK, UK, Canada and USA. Filter first, remove duplicates, then sort A to Z.
- **Why others are wrong:**
  - A) Mexico appears only in Home Office orders (1010 and 1014), which the `WHERE` clause removes.
  - C) `DISTINCT` removes the repeats, so each country appears once.
  - D) `ORDER BY country` sorts alphabetically, not in the order the rows were inserted.

**Source:** `basic-query-construction.md`
</details>

---

### 51. What does this query return?
```sql
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2025-03-01' AND '2025-03-12'
ORDER BY order_date DESC
LIMIT 2;
```
- [ ] A) `1014 | 2025-03-09` and `1013 | 2025-03-05`
- [ ] B) `1012 | 2025-03-02` and `1013 | 2025-03-05`
- [ ] C) `1015`, `1014`, `1013` and `1012`
- [ ] D) `1015 | 2025-03-12` and `1014 | 2025-03-09`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1015 | 2025-03-12` and `1014 | 2025-03-09`

**Explanation:** Rows are filtered first (four March orders, inclusive of the 12th), sorted newest first, and then limited to two.
- **Why others are wrong:**
  - A) `BETWEEN` includes the upper bound, so order 1015 (dated exactly 2025-03-12) qualifies and sorts first.
  - B) That is ascending order; the query sorts newest first with `DESC`.
  - C) `LIMIT 2` cuts the result off after two rows.

**Source:** `basic-query-construction.md`
</details>

---

### 52. Which rows does this validation query return?
```sql
SELECT order_id, status
FROM orders
WHERE status IN ('PENDING', 'SHIPPED')
  AND (quantity < 1 OR unit_price <= 0)
ORDER BY order_id;
```
- [ ] A) `1007 | PENDING`, `1011 | PENDING` and `1015 | DELIVERED`
- [ ] B) `1004`, `1007`, `1011` and `1014`
- [ ] C) `1007 | PENDING` and `1011 | PENDING`
- [ ] D) `1011 | PENDING` only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1007 | PENDING` and `1011 | PENDING`

**Explanation:** Only orders that are still pending or shipped *and* have a quantity below 1 or a price of 0 or less are returned: 1007 (quantity 0) and 1011 (quantity -1).
- **Why others are wrong:**
  - A) Order 1015 has a zero price, but its status is `DELIVERED`, so the status filter removes it.
  - B) That is every pending order; the parenthesised condition keeps only those with a bad quantity or price.
  - D) `quantity < 1` also matches a quantity of 0, so order 1007 is flagged too.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---


## Part 4: Fill in the Blank

### 53. A column in one table that refers to the primary key of another table is called a ________ key.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** foreign

**Explanation:** A foreign key links one table to another table's primary key (for example, `customer_id` in `orders` pointing at `customers`). This linking is where the name "relational database" comes from; how to define and use keys in depth is Friday's topic.

**Source:** `relational-database-concepts.md`
</details>

---

### 54. The program that stores tables on disk, lets many users connect, enforces rules and answers SQL requests is called an ________ (give the four-to-five-letter abbreviation for Relational Database Management System).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** RDBMS

**Explanation:** An RDBMS (SQLite, MySQL, PostgreSQL, SQL Server, Oracle) is the software behind the tables. The lesson compares it to a diligent librarian who finds the rows you ask for.

**Source:** `relational-database-concepts.md`
</details>

---

### 55. To return only the first 3 rows in **SQL Server**, you write `SELECT ________ 3 * FROM orders;`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** TOP

**Explanation:** SQL Server uses `TOP n` where SQLite, MySQL and PostgreSQL use `LIMIT n`, and Oracle 12c+ uses `FETCH FIRST n ROWS ONLY`.

**Source:** `sql-syntax.md`
</details>

---

### 56. To show the text `N/A` instead of NULL in the email column, complete the query:
```sql
SELECT order_id, ________(email, 'N/A') AS email
FROM orders;
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `COALESCE`

**Explanation:** `COALESCE(a, b, ...)` returns the first non-NULL argument, so a NULL email is replaced by `'N/A'` while real emails are shown unchanged. The stored data is not modified; only the result changes.

**Source:** `select-statements.md`
</details>

---

### 57. To round a calculated price to two decimals, complete the query:
```sql
SELECT order_id, ________(unit_price * 0.90, 2) AS discounted_price
FROM orders;
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ROUND

**Explanation:** `ROUND(value, digits)` tidies long decimal fractions. For order 1003 it turns 8.991 into 8.99.

**Source:** `select-statements.md`
</details>

---

### 58. To find orders with a missing email, complete the condition (not the operator `=`):
```sql
SELECT order_id, customer_name
FROM orders
WHERE email ________ NULL;
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `IS`

**Explanation:** The test is `IS NULL`. Writing `email = NULL` compares an unknown value with an unknown value, which is UNKNOWN, so it returns 0 rows even though orders 1004 and 1014 have a NULL email. The correct query returns those two orders.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 59. To list the 3 most expensive orders by `unit_price`, with the largest first, complete the query:
```sql
SELECT order_id, product, unit_price
FROM orders
ORDER BY unit_price ________
LIMIT 3;
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `DESC`

**Explanation:** `ORDER BY` sorts ascending by default; `DESC` reverses it so the biggest price comes first, and `LIMIT 3` then keeps the top three (orders 1001, 1006 and 1014). This is the Top-N pattern.

**Source:** `basic-query-construction.md`
</details>

---

### 60. To find rows where `customer_name` has stray leading or trailing spaces, complete the rule:
```sql
SELECT order_id
FROM orders
WHERE customer_name <> ________(customer_name);
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** TRIM

**Explanation:** `TRIM` removes spaces from both ends, so comparing the original with the trimmed value finds text that changes when trimmed. Trailing spaces are invisible in a grid but break comparisons such as `'SHIPPED '` versus `'SHIPPED'`.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---


## Part 5: Scenario-Based Questions

### 61. The orders screen shows **4 orders per page**, sorted by `order_id`. A tester needs the rows behind **page 3** (expected: 1009 to 1012). Which query returns them reliably?
- [ ] A) `SELECT order_id FROM orders ORDER BY order_id LIMIT 4 OFFSET 12;`
- [ ] B) `SELECT order_id FROM orders ORDER BY order_id LIMIT 4 OFFSET 3;`
- [ ] C) `SELECT order_id FROM orders LIMIT 4 OFFSET 8;`
- [ ] D) `SELECT order_id FROM orders ORDER BY order_id LIMIT 4 OFFSET 8;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `SELECT order_id FROM orders ORDER BY order_id LIMIT 4 OFFSET 8;`

**Explanation:** `OFFSET` skips rows before counting, and offset = (page - 1) x page size. Always combine `LIMIT` and `OFFSET` with `ORDER BY`.
- **Why others are wrong:**
  - A) The offset is (page - 1) x page size = 2 x 4 = 8; an offset of 12 is page 4 (only 1013 to 1015).
  - B) This skips only 3 rows and returns 1004 to 1007, mixing up the page number with the offset.
  - C) Without `ORDER BY` the database does not guarantee which rows come "first", so the page contents are not reliable.

**Source:** `filtering-and-sorting-data.md`
</details>

---

### 62. You run a violation query for the rule "a cancelled order must not have `quantity` greater than 0", and it returns order 1005 (CANCELLED, quantity 1). What is the best next step?
- [ ] A) Confirm the rule with the product owner first, because cancelled orders often keep their original quantity, so this may be perfectly normal
- [ ] B) Log a high-severity defect immediately
- [ ] C) Update the row to quantity 0 so the query returns nothing
- [ ] D) Rewrite the query so that it returns no rows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Confirm the rule with the product owner first, because cancelled orders often keep their original quantity, so this may be perfectly normal

**Explanation:** A violation query only surfaces rows; whether they are defects depends on the business rule. Good testers present evidence and ask clear questions instead of declaring everything a bug.
- **Why others are wrong:**
  - B) The rule was only an example; reporting it as a bug without checking the business rule would be a false alarm.
  - C) Changing data to make a check pass hides the issue (and data-changing statements are Friday's topic); validation should report, not silently fix.
  - D) Making the query return nothing just produces a false pass; the query correctly matched the rule as worded.

**Source:** `basic-query-construction.md`
</details>

---

### 63. Customer service says some customers never received a confirmation email. As the QA engineer, you must list every order that has **no usable email address**, meaning the email is missing (NULL) **or** does not look like an address (no `@` followed later by a `.`). Which query finds all of them?
- [ ] A) `SELECT order_id, email FROM orders WHERE email NOT LIKE '%@%.%';`
- [ ] B) `SELECT order_id, email FROM orders WHERE email IS NULL OR email NOT LIKE '%@%.%' ORDER BY order_id;`
- [ ] C) `SELECT order_id, email FROM orders WHERE email = NULL OR email NOT LIKE '%@%.%';`
- [ ] D) `SELECT order_id, email FROM orders WHERE email IS NOT NULL AND email NOT LIKE '%@%.%';`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `SELECT order_id, email FROM orders WHERE email IS NULL OR email NOT LIKE '%@%.%' ORDER BY order_id;`

**Explanation:** Each definition of "unusable" becomes one `OR` branch: `IS NULL` catches the missing emails and `NOT LIKE '%@%.%'` catches the malformed one. The query returns 3 rows: 1004 (NULL), 1006 (`frank.moore@example`) and 1014 (NULL).
- **Why others are wrong:**
  - A) `NULL NOT LIKE ...` is UNKNOWN, so the NULL rows are skipped; this returns only order 1006.
  - C) `email = NULL` is never true, so this behaves like A and also returns only order 1006.
  - D) `IS NOT NULL AND ...` deliberately excludes the NULL rows, so again only order 1006 is returned (useful only if NULLs are reported by a separate rule).

**Source:** `using-sql-for-qa-data-validation.md` (also `basic-query-construction.md`)
</details>

---

### 64. The specification says `status` may only be exactly `PENDING`, `SHIPPED`, `DELIVERED` or `CANCELLED` (upper case). You run the check on SQLite and want it to flag the planted defect, order 1008 (`delivered`), and nothing else. Which query does that?
- [ ] A) `SELECT order_id, status FROM orders WHERE status <> 'DELIVERED';`
- [ ] B) `SELECT order_id, status FROM orders WHERE UPPER(status) NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED');`
- [ ] C) `SELECT order_id, status FROM orders WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED') OR status IS NULL;`
- [ ] D) `SELECT order_id, status FROM orders WHERE status = NULL;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `SELECT order_id, status FROM orders WHERE status NOT IN ('PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED') OR status IS NULL;`

**Explanation:** This lists the allowed values and flags anything outside them, plus a missing status. Because SQLite compares text case-sensitively, `delivered` is not in the list, so only order 1008 is returned.
- **Why others are wrong:**
  - A) That returns 10 rows (every order that is not exactly `DELIVERED`), mostly valid ones.
  - B) Applying `UPPER` to the column turns `delivered` into `DELIVERED`, which is in the list, so the query returns 0 rows: a **false pass** that hides the very defect you are hunting.
  - D) `= NULL` is never true, so it returns 0 rows and tests the wrong thing.

**Source:** `using-sql-for-qa-data-validation.md` (also `filtering-and-sorting-data.md`)
</details>

---

### 65. Your V-04 check (`unit_price <= 0 OR unit_price IS NULL`) returns order 1015: a Keyboard with a unit price of 0.0. Which report best follows the lesson's advice?
- [ ] A) Mark it as a critical defect with no discussion
- [ ] B) Ignore it, because the order is already DELIVERED
- [ ] C) Report it with the rule ID, the exact query, the evidence row and the impact, and ask whether a zero price is allowed (it could be a promotion); if not, it is a defect
- [ ] D) Delete the row from the shared database

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Report it with the rule ID, the exact query, the evidence row and the impact, and ask whether a zero price is allowed (it could be a promotion); if not, it is a defect

**Explanation:** A good data-defect report contains title, environment, rule, query, evidence, impact and priority, and it states clearly when something is a question for the business rather than a confirmed bug.
- **Why others are wrong:**
  - A) A zero price might be a legitimate giveaway; the lesson says to separate defects from questions.
  - B) Delivery does not make bad price data acceptable; a free item that was not meant to be free costs real money.
  - D) Validation is read-only here, and deleting evidence would remove the very thing you need to report.

**Source:** `using-sql-for-qa-data-validation.md`
</details>

---


## Answer Key

| # | Topic | Format | Answer |
|---|---|---|---|

| 1 | Relational database concepts | Multiple Choice | B |
| 2 | Relational database concepts | Multiple Choice | D |
| 3 | Relational database concepts | Multiple Choice | B |
| 4 | Relational database concepts | Multiple Choice | D |
| 5 | Relational database concepts | Multiple Choice | A |
| 6 | SQL syntax | Multiple Choice | A |
| 7 | SQL syntax | Multiple Choice | C |
| 8 | SQL syntax | Multiple Choice | C |
| 9 | SQL syntax | Multiple Choice | A |
| 10 | SQL syntax | Multiple Choice | B |
| 11 | SELECT statements | Multiple Choice | D |
| 12 | SELECT statements | Multiple Choice | D |
| 13 | SELECT statements | Multiple Choice | B |
| 14 | SELECT statements | Multiple Choice | C |
| 15 | SELECT statements | Multiple Choice | A |
| 16 | SELECT statements | Multiple Choice | B |
| 17 | Filtering and sorting | Multiple Choice | A |
| 18 | Filtering and sorting | Multiple Choice | C |
| 19 | Filtering and sorting | Multiple Choice | D |
| 20 | Basic query construction | Multiple Choice | B |
| 21 | Basic query construction | Multiple Choice | A |
| 22 | Basic query construction | Multiple Choice | D |
| 23 | Basic query construction | Multiple Choice | C |
| 24 | SQL for QA data validation | Multiple Choice | C |
| 25 | SQL for QA data validation | Multiple Choice | B |
| 26 | SQL for QA data validation | Multiple Choice | A |
| 27 | SQL for QA data validation | Multiple Choice | C |
| 28 | Relational database concepts | True/False | False |
| 29 | Relational database concepts | True/False | False |
| 30 | Relational database concepts | True/False | True |
| 31 | SQL syntax | True/False | False |
| 32 | SQL syntax | True/False | False |
| 33 | SELECT statements | True/False | True |
| 34 | SELECT statements | True/False | True |
| 35 | Filtering and sorting | True/False | True |
| 36 | Filtering and sorting | True/False | False |
| 37 | Filtering and sorting | True/False | True |
| 38 | SQL for QA data validation | True/False | False |
| 39 | SQL for QA data validation | True/False | True |
| 40 | SQL syntax | Query Prediction | C |
| 41 | SQL syntax | Query Prediction | D |
| 42 | SQL syntax | Query Prediction | A |
| 43 | SELECT statements | Query Prediction | D |
| 44 | SELECT statements | Query Prediction | B |
| 45 | Filtering and sorting | Query Prediction | B |
| 46 | Filtering and sorting | Query Prediction | A |
| 47 | Filtering and sorting | Query Prediction | C |
| 48 | Filtering and sorting | Query Prediction | A |
| 49 | Basic query construction | Query Prediction | C |
| 50 | Basic query construction | Query Prediction | B |
| 51 | Basic query construction | Query Prediction | D |
| 52 | SQL for QA data validation | Query Prediction | C |
| 53 | Relational database concepts | Fill-in-the-Blank | foreign |
| 54 | Relational database concepts | Fill-in-the-Blank | RDBMS |
| 55 | SQL syntax | Fill-in-the-Blank | TOP |
| 56 | SELECT statements | Fill-in-the-Blank | COALESCE |
| 57 | SELECT statements | Fill-in-the-Blank | ROUND |
| 58 | Filtering and sorting | Fill-in-the-Blank | IS |
| 59 | Basic query construction | Fill-in-the-Blank | DESC |
| 60 | SQL for QA data validation | Fill-in-the-Blank | TRIM |
| 61 | Filtering and sorting | Scenario | D |
| 62 | Basic query construction | Scenario | A |
| 63 | SQL for QA data validation | Scenario | B |
| 64 | SQL for QA data validation | Scenario | C |
| 65 | SQL for QA data validation | Scenario | C |
