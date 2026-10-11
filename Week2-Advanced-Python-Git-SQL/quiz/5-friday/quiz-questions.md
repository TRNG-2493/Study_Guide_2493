# Daily Knowledge Check: Week2-Advanced-Python-Git-SQL — Friday: SQL Joins & Data Validation

Try each question before opening the solution. Every question names the written lesson it comes from, so you can go back and re-read.

All questions use the "QA Shop" practice database exactly as created by the setup script in `insert-update-and-delete.md` (10 customers, 8 products, 12 orders, 16 order items, 11 payments, 6 defects, with the planted data problems). Answers were checked by running the queries on SQLite 3.45.1. Where a question depends on the database engine, it says "SQLite".

---

## Part 1: Multiple Choice

### 1. Why does the lesson insist on writing the column list in `INSERT INTO customers (customer_id, full_name, email, country, created_date) VALUES (...)`?
- [ ] A) Without a column list SQL assumes you are supplying every column in the table's defined order, so adding or reordering a column later can break the script or silently put values in the wrong columns
- [ ] B) The column list makes the insert run faster than a `VALUES` clause without one
- [ ] C) Without the column list, `INSERT` refuses to run on any table that has a primary key
- [ ] D) The column list is what makes SQLite generate the primary key automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Without a column list SQL assumes you are supplying every column in the table's defined order, so adding or reordering a column later can break the script or silently put values in the wrong columns

**Explanation:** An explicit list makes each value's destination clear and keeps the statement stable when the table changes.
- **Why others are wrong:**
  - B) The lesson makes no speed claim; the reason is safety and clarity.
  - C) It runs; it is merely fragile when the table definition changes.
  - D) SQLite generates an `INTEGER PRIMARY KEY` when you leave it out (or give NULL); the list itself does not do that.

**Source:** `insert-update-and-delete.md`
</details>

---

### 2. In SQLite, which statement empties the `defects` table but leaves the (empty) table in place?
- [ ] A) `TRUNCATE TABLE defects;`
- [ ] B) `DROP TABLE defects;`
- [ ] C) `DELETE * FROM defects;`
- [ ] D) `DELETE FROM defects;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `DELETE FROM defects;`

**Explanation:** `DELETE` without a `WHERE` removes every row and keeps the table structure. SQLite has no `TRUNCATE`, so `DELETE FROM t;` is how you empty a table there.
- **Why others are wrong:**
  - A) It exists in MySQL, PostgreSQL, SQL Server and Oracle, but SQLite reports a syntax error.
  - B) This removes the data and the structure, so the table no longer exists.
  - C) `DELETE` removes whole rows and takes no column list; the `*` is a syntax error.

**Source:** `insert-update-and-delete.md`
</details>

---

### 3. The QA Shop `orders` table is declared with `FOREIGN KEY (customer_id) REFERENCES customers(customer_id)`, yet order 107 points to customer 99, who does not exist. Which explanation fits SQLite?
- [ ] A) SQLite does not support `FOREIGN KEY` at all; it parses the declaration and throws it away
- [ ] B) SQLite only enforces foreign keys after `PRAGMA foreign_keys = ON` is run on the connection, and the practice data was loaded with enforcement off
- [ ] C) The foreign key was declared on `customers` instead of `orders`, so `orders` is not protected
- [ ] D) A foreign key column accepts any value as long as the column is not declared `NOT NULL`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) SQLite only enforces foreign keys after `PRAGMA foreign_keys = ON` is run on the connection, and the practice data was loaded with enforcement off

**Explanation:** For historical reasons SQLite ignores declared foreign keys unless you switch enforcement on for each connection (`PRAGMA foreign_keys;` prints `0` by default). Turning it on does not repair rows already stored, which is why `PRAGMA foreign_key_check` is used to list the existing violations (here orders 107, order_items 14 and 15, payments 10).
- **Why others are wrong:**
  - A) SQLite supports foreign keys; it just does not enforce them until asked.
  - C) The declaration is on `orders` (see the `CREATE TABLE orders` statement), the child table.
  - D) A foreign key value must match an existing parent row or be NULL; being "not NOT NULL" does not let arbitrary values through once enforcement is on.

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 4. Item 16 in `order_items` has `quantity = -1`. Which constraint, added to the table, would have stopped that row from being stored?
- [ ] A) `NOT NULL` on `quantity`
- [ ] B) `UNIQUE (order_id, product_id)`
- [ ] C) `FOREIGN KEY (order_id) REFERENCES orders(order_id)`
- [ ] D) `CHECK (quantity > 0)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `CHECK (quantity > 0)`

**Explanation:** A `CHECK` constraint rejects any row for which its condition is false. The lesson points out that `order_items.quantity` has no such rule, which is how the negative value got in; a missing constraint is itself a QA finding.
- **Why others are wrong:**
  - A) `quantity` is already `NOT NULL`; `-1` is a real value, not NULL.
  - B) `UNIQUE (order_id, product_id)` targets duplicate lines such as items 5 and 13, and says nothing about the sign of a quantity.
  - C) Item 16 belongs to order 112, which exists, so a foreign key on `order_id` would accept it. That constraint addresses orphans such as item 14.

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 5. With foreign key enforcement on, `demo_cart_line` is declared with `ON DELETE CASCADE` and `demo_cart_gift` with `ON DELETE SET NULL`, both referencing `demo_cart(cart_id)`. Cart 1 has two line rows (A and B) and one gift row. What is the state after `DELETE FROM demo_cart WHERE cart_id = 1;`?
- [ ] A) The delete is rejected with `FOREIGN KEY constraint failed` because cart 1 still has children
- [ ] B) Both the line rows and the gift row are deleted, because every foreign key cascades
- [ ] C) Both line rows of cart 1 are deleted, and the gift row stays but its `cart_id` becomes NULL
- [ ] D) The line rows are kept with `cart_id = NULL` and the gift row is deleted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Both line rows of cart 1 are deleted, and the gift row stays but its `cart_id` becomes NULL

**Explanation:** `CASCADE` deletes the children together with the parent, while `SET NULL` keeps the child row and detaches it. In the lesson demo only line C (cart 2) survives and the gift row shows `cart_id = NULL`.
- **Why others are wrong:**
  - A) That is the default `RESTRICT` / `NO ACTION` behaviour; here both child tables define a different `ON DELETE` action, so the parent can be deleted.
  - B) Foreign keys do not cascade by default; only `demo_cart_line` asked for `CASCADE`, and the gift row is kept.
  - D) This swaps the two actions: `CASCADE` belongs to the lines (they are deleted), `SET NULL` to the gift (it is kept).

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 6. `PRAGMA foreign_key_check;` on the QA Shop database prints the row `order_items | 15 | products | 0`. What does that row tell you?
- [ ] A) Order line 15 has a `product_id` that does not exist in `products` (it points to product 999)
- [ ] B) Product 15 is missing from `products`
- [ ] C) Order 15 has no order lines
- [ ] D) `products` contains rows that no order line refers to

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Order line 15 has a `product_id` that does not exist in `products` (it points to product 999)

**Explanation:** Each output row names the child table, the rowid of the offending child row (for `order_items` that is the `item_id`), the parent table it should point to and the number of the FK definition. Item 15 is planted problem 10.
- **Why others are wrong:**
  - B) 15 is the rowid of the child row in `order_items`, not a product ID.
  - C) The reported table is `order_items` (the child), and the parent that is missing is `products`; there is no order 15 involved.
  - D) Unsold products (7 and 8) are a different finding; `foreign_key_check` only reports child rows whose parent is missing.

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 7. `SELECT customer_id, full_name FROM orders AS o INNER JOIN customers AS c ON o.customer_id = c.customer_id;` fails. What is the error and the fix?
- [ ] A) `no such table: orders`; remove the aliases
- [ ] B) `misuse of aggregate`; add a `GROUP BY`
- [ ] C) `ambiguous column name: customer_id`; qualify the column as `o.customer_id` or `c.customer_id`
- [ ] D) `FOREIGN KEY constraint failed`; run `PRAGMA foreign_keys = OFF`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `ambiguous column name: customer_id`; qualify the column as `o.customer_id` or `c.customer_id`

**Explanation:** Both tables have a column called `customer_id`, so the database cannot tell which one you mean. Qualifying every column in a join query avoids this and protects against columns added later.
- **Why others are wrong:**
  - A) Both tables exist; aliases are legal and are used in the same query's `ON` clause.
  - B) The query has no aggregate function, so this error cannot occur.
  - D) Foreign key checks apply to `INSERT`, `UPDATE` and `DELETE`, not to a `SELECT`.

**Source:** `inner-join.md`
</details>

---

### 8. You want the customers who have never placed an order (expected: 6, 8, 9 and 10). Which `WHERE` clause completes this anti-join correctly?
```sql
SELECT c.customer_id
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE ...
```
- [ ] A) `o.order_id IS NULL`
- [ ] B) `o.order_id = NULL`
- [ ] C) `c.customer_id IS NULL`
- [ ] D) `o.order_id IS NULL`, after changing `LEFT JOIN` to `INNER JOIN`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `o.order_id IS NULL`

**Explanation:** For a customer with no orders the LEFT JOIN fills every `orders` column with NULL, so testing the right table's primary key with `IS NULL` isolates exactly those customers (6, 8, 9, 10).
- **Why others are wrong:**
  - B) `= NULL` is never true (comparing with NULL gives unknown), so it returns 0 rows. Always use `IS NULL`.
  - C) `c.customer_id` is the left table's primary key and is never NULL, so this returns 0 rows.
  - D) An INNER JOIN drops the unmatched customers before the `WHERE` runs, so nothing is left to be NULL: 0 rows.

**Source:** `left-and-right-join.md`
</details>

---

### 9. Which query lists the products that have never appeared on an order line (expected: products 7 and 8)?
- [ ] A) `SELECT p.product_id FROM order_items AS i LEFT JOIN products AS p ON p.product_id = i.product_id WHERE i.item_id IS NULL;`
- [ ] B) `SELECT p.product_id FROM products AS p INNER JOIN order_items AS i ON i.product_id = p.product_id WHERE i.item_id IS NULL;`
- [ ] C) `SELECT p.product_id FROM products AS p LEFT JOIN order_items AS i ON i.product_id = p.product_id WHERE i.item_id = NULL;`
- [ ] D) `SELECT p.product_id FROM products AS p LEFT JOIN order_items AS i ON i.product_id = p.product_id WHERE i.item_id IS NULL;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `SELECT p.product_id FROM products AS p LEFT JOIN order_items AS i ON i.product_id = p.product_id WHERE i.item_id IS NULL;`

**Explanation:** Keeping every product with a `LEFT JOIN` and then testing the child table's primary key with `IS NULL` isolates the products without a partner row (the anti-join pattern).
- **Why others are wrong:**
  - A) The tables are the wrong way round: this keeps every order line, and a real line never has a NULL `item_id`, so 0 rows come back.
  - B) An `INNER JOIN` throws away unmatched products before the `WHERE` runs, so nothing is left to be NULL: 0 rows.
  - C) `= NULL` is never true (comparison with NULL is unknown), so this returns 0 rows. Always use `IS NULL`.

**Source:** `left-and-right-join.md`
</details>

---

### 10. A teammate on an old SQLite (before 3.39) cannot run `FROM orders AS o RIGHT JOIN payments AS pay ON pay.order_id = o.order_id`. Which rewrite returns exactly the same rows?
- [ ] A) `FROM orders AS o LEFT JOIN payments AS pay ON pay.order_id = o.order_id`
- [ ] B) `FROM payments AS pay LEFT JOIN orders AS o ON pay.order_id = o.order_id`
- [ ] C) `FROM orders AS o INNER JOIN payments AS pay ON pay.order_id = o.order_id`
- [ ] D) `FROM payments AS pay LEFT JOIN orders AS o ON pay.order_id = o.order_id WHERE o.order_id IS NULL`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `FROM payments AS pay LEFT JOIN orders AS o ON pay.order_id = o.order_id`

**Explanation:** A `RIGHT JOIN` is a `LEFT JOIN` with the two tables swapped, so putting `payments` (the table to keep in full) first reproduces it: 11 rows, one per payment.
- **Why others are wrong:**
  - A) This keeps every order instead of every payment (13 rows, including the unpaid orders 105, 109 and 112).
  - C) An inner join drops the orphan payment 10 (order 888 does not exist), giving 10 rows instead of 11.
  - D) The added anti-join filter keeps only the orphan payment 10 (1 row); it is a different query, not an equivalent rewrite.

**Source:** `left-and-right-join.md`
</details>

---

### 11. You reconcile `orders` against `payments` with `orders AS o FULL JOIN payments AS pay ON pay.order_id = o.order_id`. Which `WHERE` returns exactly the four problem rows (payment 10 whose order 888 does not exist, and orders 105, 109 and 112 that have no payment)?
- [ ] A) `WHERE o.order_id IS NULL AND pay.payment_id IS NULL`
- [ ] B) `WHERE o.order_id = pay.order_id`
- [ ] C) `WHERE o.order_id IS NULL OR pay.payment_id IS NULL`
- [ ] D) Use `LEFT JOIN` instead of `FULL JOIN` and keep the `OR` condition from option C

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `WHERE o.order_id IS NULL OR pay.payment_id IS NULL`

**Explanation:** A row from a FULL JOIN is either matched, left-only or right-only. A NULL primary key on either side means "no partner", so the `OR` keeps both kinds of mismatch in one query (here 1 orphan payment plus 3 unpaid orders).
- **Why others are wrong:**
  - A) A row cannot lack a partner on both sides at once, so `AND` returns 0 rows.
  - B) This keeps only the matched rows (10 rows), the opposite of what you want.
  - D) A LEFT JOIN from `orders` returns only 105, 109 and 112 and misses the orphan payment 10, which is why the lesson uses FULL JOIN for two-sided checks.

**Source:** `full-join.md`
</details>

---

### 12. `customers AS c FULL JOIN orders AS o ON o.customer_id = c.customer_id` returns 16 rows on QA Shop. How do those rows break down?
- [ ] A) 12 matched rows, 4 left-only rows and 0 right-only rows
- [ ] B) 10 matched rows, 2 left-only rows and 4 right-only rows
- [ ] C) 10 matched rows, 4 left-only rows (customers 6, 8, 9, 10) and 2 right-only rows (orders 107 and 108)
- [ ] D) 14 matched rows and 2 right-only rows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 10 matched rows, 4 left-only rows (customers 6, 8, 9, 10) and 2 right-only rows (orders 107 and 108)

**Explanation:** A full join is matched rows plus left-only rows plus right-only rows: 10 + 4 + 2 = 16. Customers without orders are left-only; orders without a customer (orphan 107, guest 108) are right-only.
- **Why others are wrong:**
  - A) Only 10 orders match a customer, and orders 107 and 108 are real right-only rows, so this split cannot be right (and does not add up to 16 either).
  - B) The two sides are swapped: the four unmatched rows are customers (left-only) and the two unmatched rows are orders (right-only).
  - D) 14 is the row count of the `LEFT JOIN`, which already includes the four customers with no orders; those are unmatched, not matched.

**Source:** `full-join.md`
</details>

---

### 13. Your MySQL test database has no `FULL JOIN`. Which recipe reproduces `customers FULL JOIN orders` exactly (16 rows) without double-counting or merging identical rows?
- [ ] A) `customers LEFT JOIN orders` combined with `UNION ALL` and the orders that have no customer (`orders LEFT JOIN customers ... WHERE c.customer_id IS NULL`, with NULLs for the customer columns)
- [ ] B) `customers LEFT JOIN orders` combined with `UNION ALL` of `orders LEFT JOIN customers`, with no filter
- [ ] C) `customers INNER JOIN orders` combined with `UNION` of `orders INNER JOIN customers`
- [ ] D) `customers LEFT JOIN orders` alone

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `customers LEFT JOIN orders` combined with `UNION ALL` and the orders that have no customer (`orders LEFT JOIN customers ... WHERE c.customer_id IS NULL`, with NULLs for the customer columns)

**Explanation:** The first half supplies the matched and left-only rows, and the anti-join half supplies only the right-only rows, so nothing is counted twice. The lesson verified this with a two-way `EXCEPT`.
- **Why others are wrong:**
  - B) The matched rows appear in both halves, so `UNION ALL` doubles them (26 rows instead of 16).
  - C) Inner joins contain only matched rows, so the unmatched customers and orders never appear (10 rows).
  - D) This gives 14 rows and misses the right-only orders 107 and 108.

**Source:** `full-join.md`
</details>

---

### 14. You build the order-detail report one join at a time and count rows: `orders` = 12; plus `INNER JOIN customers` = 10; plus `INNER JOIN order_items` = 13. Why did the count go **up** from 10 to 13 after adding a table?
- [ ] A) The join condition was forgotten, so the query became a Cartesian product
- [ ] B) The inner join brought back orders 107 and 108, which the customers join had removed
- [ ] C) NULL values in `order_items` are counted as extra rows
- [ ] D) It is one-to-many: orders 101, 102, 103 and 105 have two item rows each (+4), while order 109 has no items and drops out (-1), so 10 + 4 - 1 = 13

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It is one-to-many: orders 101, 102, 103 and 105 have two item rows each (+4), while order 109 has no items and drops out (-1), so 10 + 4 - 1 = 13

**Explanation:** After a join to the "many" side, each parent row is repeated once per matching child row, and parents with no children vanish from an inner join. Counting rows after every step lets you account for every row.
- **Why others are wrong:**
  - A) The `ON` condition is present. Without it the result would be a far larger Cartesian product, not 13.
  - B) Once removed by the inner join with `customers`, orders 107 and 108 cannot reappear; they are not in the rows being joined.
  - C) No NULLs are involved in this join; the extra rows come from orders that have several item rows.

**Source:** `multi-table-queries.md`
</details>

---

### 15. In the self join `customers AS a INNER JOIN customers AS b ON a.email = b.email AND a.customer_id < b.customer_id`, what is the job of the condition `a.customer_id < b.customer_id`?
- [ ] A) It stops each row from pairing with itself and stops each pair from appearing twice (a with b and b with a), leaving the single pair 2 and 8
- [ ] B) It sorts the output by customer ID
- [ ] C) It removes the customers whose email is NULL
- [ ] D) It switches the join from the email column to the customer ID column

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It stops each row from pairing with itself and stops each pair from appearing twice (a with b and b with a), leaving the single pair 2 and 8

**Explanation:** Without the `<` test, every customer matches itself and the Bob Smith pair shows up in both directions (11 rows instead of 1). The `<` keeps one copy of each pair.
- **Why others are wrong:**
  - B) Sorting is the job of `ORDER BY`; a join condition only decides which row pairs match.
  - C) NULL emails are already excluded because `NULL = NULL` is not true (customer 6 never matches); the `<` has nothing to do with NULL.
  - D) The rows are still matched on `a.email = b.email`; the `<` only adds a filter on the matched pairs.

**Source:** `multi-table-queries.md`
</details>

---

### 16. The query `orders LEFT JOIN customers ... INNER JOIN order_items ON i.order_id = o.order_id` was meant to keep every order, yet order 109 is missing. Why?
- [ ] A) Order 109 is pending, and `INNER JOIN` excludes pending orders
- [ ] B) Any join that follows a `LEFT JOIN` is always converted to an inner join
- [ ] C) Grace Kim (the customer of order 109) does not exist, so the `LEFT JOIN` drops it
- [ ] D) Order 109 has no item rows, so the later `INNER JOIN` removes it and cancels the protection of the earlier `LEFT JOIN`; the whole chain should use `LEFT JOIN`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Order 109 has no item rows, so the later `INNER JOIN` removes it and cancels the protection of the earlier `LEFT JOIN`; the whole chain should use `LEFT JOIN`

**Explanation:** An inner join anywhere in the chain drops left rows that have no partner. Once you start with `LEFT JOIN`s to keep unmatched rows, continue with `LEFT JOIN`s unless you deliberately want to drop rows.
- **Why others are wrong:**
  - A) A join looks at keys, not statuses; only a `WHERE` condition could filter by status.
  - B) The `LEFT JOIN customers` still works (orders 107 and 108 are kept); only the join that has no partner for order 109 removes it.
  - C) Grace Kim is customer 7 and exists, and a `LEFT JOIN` never drops rows from its left table anyway.

**Source:** `multi-table-queries.md`
</details>

---

### 17. This check compares each order's header total with the total of its lines:
```sql
SELECT o.order_id, o.total_amount AS header_total, t.items_total
FROM orders AS o
INNER JOIN (
    SELECT order_id, SUM(quantity * unit_price) AS items_total
    FROM order_items
    GROUP BY order_id
) AS t ON t.order_id = o.order_id
WHERE ROUND(o.total_amount, 2) <> ROUND(t.items_total, 2);
```
It reports orders 103, 110 and 112. Why is order 109 (header 80.00, no items at all) missing from the result?
- [ ] A) Order 109 is `pending`, and pending orders are excluded by the `WHERE` clause
- [ ] B) `ROUND(o.total_amount, 2)` rounds 80.00 down to 0
- [ ] C) The derived table has no row for order 109, so the `INNER JOIN` drops it; a `LEFT JOIN` with `COALESCE(t.items_total, 0)` would catch it
- [ ] D) `GROUP BY order_id` removes orders that have fewer than two lines

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The derived table has no row for order 109, so the `INNER JOIN` drops it; a `LEFT JOIN` with `COALESCE(t.items_total, 0)` would catch it

**Explanation:** `GROUP BY` can only produce a group for an `order_id` that appears in `order_items`. Order 109 has no items, so it never appears in the derived table and the inner join silently drops it. With `LEFT JOIN` and `COALESCE(..., 0)` the check returns 103, 109, 110 and 112.
- **Why others are wrong:**
  - A) The `WHERE` clause compares totals only; it has no status filter.
  - B) `ROUND(80.0, 2)` is still 80.0.
  - D) `GROUP BY` keeps groups of any size (order 104, for example, has one line and is grouped normally).

**Source:** `subqueries.md`
</details>

---

### 18. Which query returns customers 1, 2, 3 and 7, each exactly once (the customers with at least one completed order)?
- [ ] A) `SELECT c.customer_id FROM customers AS c WHERE EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id AND o.status = 'completed');`
- [ ] B) `SELECT c.customer_id FROM customers AS c INNER JOIN orders AS o ON o.customer_id = c.customer_id WHERE o.status = 'completed';`
- [ ] C) `SELECT c.customer_id FROM customers AS c WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id AND o.status = 'completed');`
- [ ] D) `SELECT customer_id FROM customers WHERE customer_id IN (SELECT customer_id FROM orders);`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) the `EXISTS` query

**Explanation:** `EXISTS` is a correlated test: for each customer it asks whether at least one completed order exists, and it stops at the first hit, so there is no row multiplication. It returns 1, 2, 3, 7 once each.
- **Why others are wrong:**
  - B) The join returns one row per completed order: 6 rows (customers 1 and 2 appear twice).
  - C) `NOT EXISTS` reverses the logic and returns the customers without a completed order (4, 5, 6, 8, 9, 10).
  - D) This ignores the status, so customers 4 and 5 (pending and cancelled orders only) are returned too.

**Source:** `subqueries.md`
</details>

---

### 19. Which kind of subquery must be given an alias in most databases?
- [ ] A) A list subquery in `WHERE`, such as `customer_id IN (SELECT customer_id FROM orders)`
- [ ] B) A subquery in the `FROM` clause (a derived table), such as `FROM (SELECT order_id, SUM(quantity * unit_price) AS items_total FROM order_items GROUP BY order_id) AS t`
- [ ] C) A subquery inside `EXISTS (SELECT 1 FROM orders ...)`
- [ ] D) A scalar subquery in `WHERE`, such as `total_amount > (SELECT AVG(total_amount) FROM orders)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A subquery in the `FROM` clause (a derived table), such as `FROM (SELECT order_id, SUM(quantity * unit_price) AS items_total FROM order_items GROUP BY order_id) AS t`

**Explanation:** A subquery in `FROM` acts as a temporary table, and a table needs a name so that the outer query can refer to its columns (`t.items_total`).
- **Why others are wrong:**
  - A) It is an expression, not a table, and nothing refers to it by name, so no alias is needed.
  - C) `EXISTS` only tests whether at least one row comes back; it needs no alias.
  - D) It returns a single value used like a constant, so no alias is required.

**Source:** `subqueries.md`
</details>

---

### 20. `SELECT ... FROM customers WHERE customer_id IN (SELECT customer_id FROM orders)` returns 6 rows, while `customers INNER JOIN orders` on the same key returns 10. Why do the counts differ?
- [ ] A) The `IN` version silently drops customers whose orders are not completed
- [ ] B) `IN` treats the NULL in the list as a match, so it returns fewer rows
- [ ] C) The join copies the `customers` table once for every product
- [ ] D) The join returns one row per matching order (customers 1, 2, 3 and 7 have two orders each), whereas `IN` only tests membership and keeps each customer once

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The join returns one row per matching order (customers 1, 2, 3 and 7 have two orders each), whereas `IN` only tests membership and keeps each customer once

**Explanation:** The join multiplies a customer by the number of orders (4 x 2 + 2 x 1 = 10), while `IN` returns one row per customer who appears in the list (6). Adding `DISTINCT` to the join would also give 6.
- **Why others are wrong:**
  - A) Neither query has any status filter; both look at all orders.
  - B) NULL never matches anything, and it would not remove rows anyway; it is simply ignored for a positive `IN` test.
  - C) No products are involved; a join repeats a parent row only for each matching child row.

**Source:** `subqueries.md`
</details>

---

### 21. Which query correctly lists the customers who have more than one order?
- [ ] A) `SELECT customer_id, COUNT(*) FROM orders WHERE COUNT(*) > 1 GROUP BY customer_id;`
- [ ] B) `SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id HAVING COUNT(*) > 1;`
- [ ] C) `SELECT customer_id, COUNT(*) FROM orders WHERE customer_id > 1 GROUP BY customer_id;`
- [ ] D) `SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id ORDER BY COUNT(*) > 1;`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) the `GROUP BY ... HAVING COUNT(*) > 1` query

**Explanation:** `WHERE` runs before the groups exist, so only `HAVING` (evaluated after grouping) can filter on an aggregate. The result is customers 1, 2, 3 and 7, each with 2 orders.
- **Why others are wrong:**
  - A) `WHERE` cannot use an aggregate; SQLite stops with `misuse of aggregate: COUNT()`.
  - C) It runs, but it filters on the customer ID, not the count, so single-order customers (4, 5, 99) are still returned.
  - D) `ORDER BY` only sorts. Every group is still returned (including the NULL guest group and customers with one order); nothing is filtered out.

**Source:** `group-by-and-having.md`
</details>

---

### 22. In SQLite, `SELECT status, order_id, COUNT(*) FROM orders GROUP BY status;` runs without an error and shows one `order_id` per status. What should a QA engineer conclude about the `order_id` column?
- [ ] A) It is the smallest `order_id` in each group, so the result can be trusted
- [ ] B) It is the list of all order IDs in the group
- [ ] C) It is the value from one arbitrary row of each group and should be treated as a bug; PostgreSQL, SQL Server and strict MySQL would reject the query
- [ ] D) The query is valid standard SQL because `order_id` is the primary key

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is the value from one arbitrary row of each group and should be treated as a bug; PostgreSQL, SQL Server and strict MySQL would reject the query

**Explanation:** After grouping there is one row per status, so there is no single `order_id` to show. SQLite lets the query run and picks a value from some row; other databases demand that every selected column is grouped or aggregated.
- **Why others are wrong:**
  - A) SQLite makes no such promise. A smallest-looking value in the sample output is a coincidence, not a rule.
  - B) The column holds a single value; to list all IDs you would need `GROUP_CONCAT(order_id)`.
  - D) Standard SQL requires non-aggregated columns to appear in `GROUP BY`; here the grouping is by `status`, and the primary key does not change that.

**Source:** `group-by-and-having.md`
</details>

---

### 23. Which sequence is the logical order in which a database processes the clauses of a query that uses all of these?
- [ ] A) `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`
- [ ] B) `FROM / JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`
- [ ] C) `FROM`, `GROUP BY`, `WHERE`, `HAVING`, `SELECT`, `ORDER BY`
- [ ] D) `FROM`, `WHERE`, `SELECT`, `GROUP BY`, `HAVING`, `ORDER BY`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `FROM / JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`

**Explanation:** Rows are built and filtered first, then grouped, then the groups are filtered, and only then are the output columns (and their aliases) computed and sorted. This is why `WHERE` cannot use aggregates but `ORDER BY` can use a `SELECT` alias.
- **Why others are wrong:**
  - A) That is the order in which the clauses are written, not the order in which they are processed.
  - C) `WHERE` runs before grouping; if it ran after, it could use aggregates, and it cannot.
  - D) `SELECT` is evaluated after `GROUP BY` and `HAVING`, so the aggregates it computes are available only after the groups exist.

**Source:** `group-by-and-having.md`
</details>

---

### 24. A teammate computes the share of pending orders with `SELECT COUNT(CASE WHEN status = 'pending' THEN 1 END) / COUNT(*) * 100 FROM orders;` and gets `0`, although 2 of the 12 orders are pending. Why?
- [ ] A) Both counts are integers, so SQLite performs integer division: 2 / 12 is 0 before it is multiplied by 100
- [ ] B) `COUNT(CASE ...)` ignores the rows that are `pending` and counts the others
- [ ] C) The query needs a `GROUP BY status` to count anything
- [ ] D) `CASE` without an `ELSE` makes the whole result NULL, which is displayed as 0

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Both counts are integers, so SQLite performs integer division: 2 / 12 is 0 before it is multiplied by 100

**Explanation:** Integer divided by integer gives an integer, discarding the fraction. Force decimal arithmetic by multiplying by `100.0` first: `ROUND(100.0 * COUNT(CASE WHEN status = 'pending' THEN 1 END) / COUNT(*), 1)` returns 16.7.
- **Why others are wrong:**
  - B) `CASE` returns 1 for pending rows and NULL for the rest; `COUNT` counts the non-NULL values, so it correctly counts the 2 pending orders.
  - C) Without `GROUP BY` the aggregate simply covers the whole table (12 rows).
  - D) The `CASE` NULLs are skipped by `COUNT`; the result is a real number (0 from integer division), not NULL.

**Source:** `aggregate-functions.md`
</details>

---

### 25. Which expression returns the number of customers with a missing email (expected: 1)?
- [ ] A) `COUNT(email)`
- [ ] B) `COUNT(*) - COUNT(email)`
- [ ] C) `COUNT(DISTINCT email)`
- [ ] D) `COUNT(*) + COUNT(email)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `COUNT(*) - COUNT(email)`

**Explanation:** `COUNT(*)` counts all 10 rows and `COUNT(email)` counts only the 9 non-NULL emails, so the difference is the number of NULL emails. It is a standard validation expression.
- **Why others are wrong:**
  - A) This counts the non-NULL emails (9), the opposite of what is asked.
  - C) This counts different non-NULL values (8); it is affected by duplicates but ignores NULL.
  - D) Adding the counts gives 19, which has no meaning here.

**Source:** `aggregate-functions.md`
</details>

---

### 26. What does `SELECT SUM(total_amount) FROM orders WHERE status = 'returned';` return on QA Shop, where no order has that status?
- [ ] A) `0`
- [ ] B) An error, because there are no rows to add
- [ ] C) One row containing `NULL`
- [ ] D) No rows at all

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) One row containing `NULL`

**Explanation:** An aggregate without `GROUP BY` always returns exactly one row. Over an empty set `COUNT` gives 0 but `SUM`, `AVG`, `MIN` and `MAX` give NULL, so test code should use `COALESCE(SUM(...), 0)` before comparing.
- **Why others are wrong:**
  - A) Only `COUNT` returns 0 for an empty set; `SUM` returns NULL (SQLite's own `TOTAL()` would return 0.0, but that is not `SUM`).
  - B) SQL does not raise an error; an empty set is perfectly valid input for an aggregate.
  - D) Without `GROUP BY` the aggregate collapses the (empty) input to one result row, so one row comes back.

**Source:** `aggregate-functions.md`
</details>

---

### 27. A migration check shows 10 rows in the source table and 10 rows in the target table, and the tester writes "migration verified". What is the strongest objection?
- [ ] A) Row counts can never be compared across two tables
- [ ] B) Equal counts can hide a lost row plus an extra row, or a corrupted value; a two-way `EXCEPT` (or a `FULL JOIN` on the key) lists the exact differences
- [ ] C) Counts only work if the table has a primary key
- [ ] D) Only `SUM` checksums are valid evidence, and `EXCEPT` works on a single table only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Equal counts can hide a lost row plus an extra row, or a corrupted value; a two-way `EXCEPT` (or a `FULL JOIN` on the key) lists the exact differences

**Explanation:** In the lesson demo the target had 10 rows too, yet customer 9 was lost, customer 77 appeared from nowhere and customer 4's country was corrupted. Only a row-level comparison shows that.
- **Why others are wrong:**
  - A) They can; a count is a valid first-level check, it is just not enough on its own.
  - C) A count does not depend on keys. Its weakness is that it cannot see which rows differ.
  - D) Checksums are a useful second level, but `EXCEPT` compares two result sets and is the thorough third level.

**Source:** `test-data-validation-using-sql.md`
</details>

---

## Part 2: True / False

### 28. True or False: Running `UPDATE orders SET status = 'cancelled';` (no `WHERE` clause) changes all 12 orders, not just one.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `WHERE` chooses which rows to change. Without it, the statement applies to every row (the lesson shows "12 row(s) affected"). That is why you preview with a `SELECT`, check the rows-affected count, and wrap risky changes in `BEGIN ... ROLLBACK`.

**Source:** `insert-update-and-delete.md`
</details>

---

### 29. True or False: `DROP TABLE completed_orders_archive;` and `DELETE FROM completed_orders_archive;` have the same effect.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `DELETE` without `WHERE` removes all rows but keeps the (empty) table; `DROP TABLE` removes the data and the table structure itself.

**Source:** `insert-update-and-delete.md`
</details>

---

### 30. True or False: With foreign key enforcement switched on, an order with `customer_id = NULL` (like guest order 108) is rejected because it does not match any customer.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A foreign key column may hold NULL (unless it is also declared `NOT NULL`); NULL means "no parent", not "missing parent". That is why `PRAGMA foreign_key_check` does not report order 108 but does report order 107, whose customer 99 does not exist.

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 31. True or False: An `INNER JOIN` of `orders` and `customers` on `customer_id` keeps order 108 (its `customer_id` is NULL), because NULL equals NULL.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `NULL = NULL` evaluates to NULL (unknown), not true, so a NULL key can never match anything. Order 108 (and the orphan order 107) is silently dropped, which is why only 10 of the 12 orders come back.

**Source:** `inner-join.md`
</details>

---

### 32. True or False: In `customers AS c LEFT JOIN orders AS o ON o.customer_id = c.customer_id WHERE o.status = 'completed'`, the `WHERE` throws away the customers without orders, so the query behaves like an `INNER JOIN`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** For an unmatched customer `o.status` is NULL, and `NULL = 'completed'` is not true, so the `WHERE` removes those rows. The query returns 6 rows; moving the status test into the `ON` clause keeps every customer and returns 12 rows.

**Source:** `left-and-right-join.md`
</details>

---

### 33. True or False: For customer 9 (Hana Sato, who has no orders), `customers LEFT JOIN orders` still returns one row, so `COUNT(*)` would wrongly claim she has one order while `COUNT(o.order_id)` correctly gives 0.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The unmatched customer survives the `LEFT JOIN` as one row with NULLs on the order side. `COUNT(*)` counts that row, `COUNT(o.order_id)` skips the NULL; after a left join, count a column of the right table.

**Source:** `left-and-right-join.md`
</details>

---

### 34. True or False: Because SQLite 3.45 runs `customers AS c FULL JOIN orders AS o ON o.customer_id = c.customer_id`, the identical statement also runs unchanged on MySQL.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** SQLite supports `RIGHT` and `FULL JOIN` only from version 3.39, and MySQL/MariaDB have no `FULL JOIN` at all. There you emulate it, for example with a `LEFT JOIN` plus a second `LEFT JOIN` (tables swapped) combined with `UNION ALL` and an anti-join, or with `UNION`.

**Source:** `full-join.md`
</details>

---

### 35. True or False: A `FULL JOIN` of `orders` and `payments` on `order_id` flags the double payment on order 102 (payments 2 and 11) as a mismatch.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Both payments match order 102, so they are ordinary matched rows. A join finds missing partners, not duplicates; duplicates need `GROUP BY ... HAVING COUNT(*) > 1`.

**Source:** `full-join.md`
</details>

---

### 36. True or False: `WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id)` still returns customers 6, 8, 9 and 10, even though `orders.customer_id` contains a NULL (order 108).
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `NOT EXISTS` only asks whether a matching row exists for each customer, so the NULL in the orders table cannot poison the test the way it does with `NOT IN`.

**Source:** `subqueries.md`
</details>

---

### 37. True or False: `HAVING` may use an aggregate that is not in the `SELECT` list, as in `SELECT order_id, SUM(quantity * unit_price) FROM order_items GROUP BY order_id HAVING MIN(quantity) < 1;`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `HAVING` filters groups after they are formed, so it can use any aggregate. This query returns only order 112 (items total -9.99), pinpointing the negative-quantity line.

**Source:** `group-by-and-having.md`
</details>

---

### 38. True or False: `AVG(x)` over the three rows 10, 20 and NULL returns 15, not 10.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `AVG` ignores NULLs, so it divides the sum (30) by the count of non-NULL values (2), giving 15. If "missing means zero" is the business rule, use `AVG(COALESCE(x, 0))`, which returns 10.

**Source:** `aggregate-functions.md`
</details>

---

### 39. True or False: In SQLite, `SELECT 7 / 2;` returns 3.5, because SQLite always divides with decimals.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Dividing two integers gives an integer, so `7 / 2` is 3. To force decimal division write `7 / 2.0`, `CAST(7 AS REAL) / 2`, or multiply by `100.0` first when computing percentages.

**Source:** `aggregate-functions.md`
</details>

---

## Part 3: Query Prediction

*Assume a fresh copy of the QA Shop database for each question.*

### 40. What do the two `SELECT` statements print?
```sql
BEGIN;
DELETE FROM defects WHERE status = 'closed';
SELECT COUNT(*) AS inside_transaction FROM defects;
ROLLBACK;
SELECT COUNT(*) AS after_rollback FROM defects;
```
- [ ] A) 4 and 4
- [ ] B) 4 and 6
- [ ] C) 6 and 6
- [ ] D) 2 and 6

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 4 and 6

**Explanation:** The table has 6 defects, 2 of them closed (defects 2 and 5). Inside the transaction the `DELETE` leaves 4, but `ROLLBACK` undoes everything since `BEGIN`, so the table is back to 6.
- **Why others are wrong:**
  - A) That would mean the `ROLLBACK` did not restore the deleted rows.
  - C) That would mean the `DELETE` removed nothing, but 2 rows match `status = 'closed'`.
  - D) 2 is the number of rows deleted, not the number left.

**Source:** `insert-update-and-delete.md`
</details>

---

### 41. How many rows does this query return? (The `orders` table has 8 completed orders.)
```sql
SELECT o.order_id, c.full_name
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.status = 'completed';
```
- [ ] A) 8
- [ ] B) 10
- [ ] C) 6
- [ ] D) 12

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 6

**Explanation:** Completed orders are 101, 102, 103, 107, 108, 110, 111 and 112. Order 107 (customer 99 does not exist) and order 108 (customer NULL) find no customer and are silently dropped, leaving 6 rows (101, 102, 103, 110, 111, 112).
- **Why others are wrong:**
  - A) 8 is the count of completed orders before the join; the inner join removes 107 and 108.
  - B) 10 is the number of all orders that match a customer, regardless of status.
  - D) 12 is the total number of orders in the table.

**Source:** `inner-join.md`
</details>

---

### 42. What does this query return? (Order 103 has a header total of 150.00 and two item rows, items 5 and 13.)
```sql
SELECT SUM(o.total_amount) AS summed
FROM orders AS o
INNER JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.order_id = 103;
```
- [ ] A) `150.0`
- [ ] B) `2`
- [ ] C) `NULL`
- [ ] D) `300.0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `300.0`

**Explanation:** The join repeats the order row once per item row (2 rows), and each repeated row carries the header total of 150.00, so `SUM` adds it twice. This is the row-multiplication trap after joining to the "many" side.
- **Why others are wrong:**
  - A) That would be the header total counted once, but the joined result holds two copies of the order row.
  - B) 2 is the number of joined rows (what `COUNT(*)` would give); `SUM` adds the amounts.
  - C) `SUM` ignores NULLs, and here both rows hold a real value, so the result is a number.

**Source:** `inner-join.md`
</details>

---

### 43. What does this query return?
```sql
SELECT COUNT(*) AS rows_in_result, COUNT(o.order_id) AS real_orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE c.customer_id = 9;
```
- [ ] A) `rows_in_result = 1`, `real_orders = 0`
- [ ] B) `rows_in_result = 0`, `real_orders = 0`
- [ ] C) `rows_in_result = 1`, `real_orders = 1`
- [ ] D) `rows_in_result = 0`, `real_orders = 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `rows_in_result = 1`, `real_orders = 0`

**Explanation:** Customer 9 (Hana Sato) has no orders, but the LEFT JOIN still outputs one row for her with NULLs on the order side. `COUNT(*)` counts that row (1); `COUNT(o.order_id)` skips NULLs (0). After a LEFT JOIN, count a column of the right table, not `*`.
- **Why others are wrong:**
  - B) A LEFT JOIN never drops a left row, so there is 1 row.
  - C) That would only be true if she had an order; `COUNT(*)` would then wrongly claim an order for her.
  - D) `COUNT(o.order_id)` can never exceed `COUNT(*)` for the same rows.

**Source:** `left-and-right-join.md`
</details>

---

### 44. What does this query return, as (customer_id, completed_orders) rows?
```sql
SELECT c.customer_id, COUNT(o.order_id) AS completed_orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id AND o.status = 'completed'
WHERE c.country = 'US'
GROUP BY c.customer_id
ORDER BY c.customer_id;
```
- [ ] A) `(1, 2)`, `(2, 2)`, `(7, 1)`, `(8, 0)`
- [ ] B) `(1, 2)`, `(2, 2)`, `(7, 1)`
- [ ] C) `(1, 2)`, `(2, 2)`, `(7, 1)`, `(8, 1)`
- [ ] D) `(1, 2)`, `(2, 2)`, `(7, 2)`, `(8, 0)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `(1, 2)`, `(2, 2)`, `(7, 1)`, `(8, 0)`

**Explanation:** The status test sits in `ON`, so every US customer (1, 2, 7 and 8) is kept, and `COUNT(o.order_id)` counts only real completed orders. Customer 8 has no orders and gets 0; customer 7 has one completed order (112) and one pending order (109).
- **Why others are wrong:**
  - B) That is what you get when the status filter is placed in `WHERE`: customer 8 is thrown away and the join behaves like an inner join.
  - C) That would need `COUNT(*)`, which counts customer 8's single NULL-filled row as 1; the query counts `o.order_id`.
  - D) Customer 7 has two orders in total, but order 109 is pending and the `ON` condition excludes it, so the count is 1.

**Source:** `left-and-right-join.md`
</details>

---

### 45. How many rows does this query return?
```sql
SELECT COUNT(*) AS problem_rows
FROM products AS p
FULL JOIN order_items AS i ON i.product_id = p.product_id
WHERE p.product_id IS NULL OR i.item_id IS NULL;
```
- [ ] A) 2
- [ ] B) 4
- [ ] C) 18
- [ ] D) 3

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 3

**Explanation:** The two-sided anti-join finds products 7 and 8 (never sold, left-only) and order line 15 (product 999 does not exist, right-only): 2 + 1 = 3.
- **Why others are wrong:**
  - A) That counts only the two unsold products and forgets the right-only line 15, whose product 999 does not exist.
  - B) Item 14 is not a problem for this join: it points to product 2, which exists, so it matches (its missing order is a different check).
  - C) That is the row count of the full join without the `WHERE`; the filter keeps only the mismatches.

**Source:** `full-join.md`
</details>

---

### 46. How many rows does this query return?
```sql
SELECT COUNT(*) AS rows_now
FROM orders AS o
INNER JOIN customers   AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
INNER JOIN products    AS p ON p.product_id  = i.product_id;
```
- [ ] A) 10
- [ ] B) 13
- [ ] C) 16
- [ ] D) 12

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 12

**Explanation:** Counting step by step: 12 orders, 10 after the customer join (107 and 108 drop), 13 after the item join (four orders have two lines, order 109 has none), and 12 after the product join because item 15 points to the missing product 999.
- **Why others are wrong:**
  - A) That is the count after only the `customers` join; the item join then changes the count.
  - B) That is the count before the `products` join; the last join removes item 15 (product 999 does not exist).
  - C) 16 is the number of rows in `order_items`; the earlier inner joins already removed some of them.

**Source:** `multi-table-queries.md`
</details>

---

### 47. What does this query return?
```sql
SELECT customer_id, full_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```
- [ ] A) Four rows: customers 6, 8, 9 and 10
- [ ] B) Six rows: customers 1, 2, 3, 4, 5 and 7
- [ ] C) An error, because the subquery returns a NULL
- [ ] D) Zero rows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Zero rows

**Explanation:** The subquery's list contains a NULL (order 108 has no customer). `x NOT IN (1, 2, ..., NULL)` expands to a chain of `<>` tests that includes `x <> NULL`, which is never true, so no customer can qualify. Fix it with `WHERE customer_id IS NOT NULL` inside the subquery, or use `NOT EXISTS`.
- **Why others are wrong:**
  - A) That is the answer you would want, and what the fixed versions return, but the unfiltered `NOT IN` cannot produce it.
  - B) Those are the customers who did place orders (the `IN` version).
  - C) There is no error; the query runs and silently returns nothing, which is what makes the bug dangerous.

**Source:** `subqueries.md`
</details>

---

### 48. Which products does this query return? (The average product price is about 272.94.)
```sql
SELECT product_name
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY product_id;
```
- [ ] A) Laptop Pro and Monitor 27in
- [ ] B) Laptop Pro, Monitor 27in and Standing Desk
- [ ] C) Laptop Pro only
- [ ] D) Laptop Pro, Desk Chair, Monitor 27in and Standing Desk

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Laptop Pro, Monitor 27in and Standing Desk

**Explanation:** The scalar subquery is evaluated once (about 272.94) and compared with every product price; 1200.00, 300.00 and 450.00 are above it.
- **Why others are wrong:**
  - A) Standing Desk costs 450.00, which is above the average, so it qualifies too.
  - C) That would be `unit_price = (SELECT MAX(unit_price) ...)`; the query uses `>` with the average.
  - D) Desk Chair costs 150.00, below the average of about 272.94, so it is excluded.

**Source:** `subqueries.md`
</details>

---

### 49. What does this query return?
```sql
SELECT method, COUNT(*) AS n
FROM payments
WHERE status = 'paid'
GROUP BY method
HAVING COUNT(*) > 2;
```
- [ ] A) `card | 9`
- [ ] B) `card | 8` and `paypal | 2`
- [ ] C) `card | 8`
- [ ] D) No rows

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `card | 8`

**Explanation:** `WHERE` runs first and keeps the 10 paid payments (card: 1, 2, 4, 6, 8, 9, 10, 11; paypal: 3 and 7). After grouping, `HAVING COUNT(*) > 2` keeps only groups with more than 2 rows: card (8). Paypal has exactly 2, which is not greater than 2.
- **Why others are wrong:**
  - A) 9 would include the refunded card payment 5, which the `WHERE` already removed.
  - B) Paypal's count is 2, and `HAVING` requires more than 2.
  - D) The card group has 8 rows and passes the `HAVING` test.

**Source:** `group-by-and-having.md`
</details>

---

### 50. How many rows does this query return?
```sql
SELECT customer_id, COUNT(*) AS n
FROM orders
GROUP BY customer_id;
```
- [ ] A) 6
- [ ] B) 7
- [ ] C) 8
- [ ] D) 12

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 8

**Explanation:** There are seven distinct non-NULL IDs (1, 2, 3, 4, 5, 7 and the orphan 99), and all rows with a NULL `customer_id` (the guest order 108) form one more group: 7 + 1 = 8.
- **Why others are wrong:**
  - A) That counts only customers who exist; the orphan group 99 and the NULL group are groups too.
  - B) That ignores the NULL group; NULLs are treated as the same value for grouping and get a group of their own.
  - D) That is the number of orders; `GROUP BY` returns one row per group, not per order.

**Source:** `group-by-and-having.md`
</details>

---

### 51. What does this query return (three columns, in order)?
```sql
SELECT COUNT(*), COUNT(email), COUNT(DISTINCT email)
FROM customers;
```
- [ ] A) 10, 10, 9
- [ ] B) 10, 9, 8
- [ ] C) 9, 9, 8
- [ ] D) 10, 9, 9

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 10, 9, 8

**Explanation:** `COUNT(*)` counts all 10 rows. `COUNT(email)` skips the NULL email of Frank Lee (customer 6), giving 9. `COUNT(DISTINCT email)` also collapses the duplicate `bob@example.com` (customers 2 and 8), giving 8.
- **Why others are wrong:**
  - A) `COUNT(email)` ignores NULLs, so it cannot equal the row count here.
  - C) `COUNT(*)` counts rows regardless of NULLs, so it is 10, not 9.
  - D) `COUNT(DISTINCT email)` removes the duplicated Bob email, so it is smaller than `COUNT(email)`.

**Source:** `aggregate-functions.md`
</details>

---

### 52. What does this query return (three columns, in order)?
```sql
SELECT MIN(quantity) AS min_q, MAX(quantity) AS max_q, SUM(quantity) AS sum_q
FROM order_items;
```
- [ ] A) `-1 | 10 | 28`
- [ ] B) `1 | 10 | 29`
- [ ] C) `-1 | 10 | 16`
- [ ] D) `-1 | 16 | 28`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `-1 | 10 | 28`

**Explanation:** The 16 order lines hold quantities from -1 (item 16, the planted bug) to 10 (item 10), and they add up to 28. A range check with `MIN` exposes the negative quantity immediately.
- **Why others are wrong:**
  - B) That would be the result if the -1 line were left out; aggregates cannot know a value is "bad" and include it, which also lowers the sum.
  - C) 16 is `COUNT(*)`, the number of rows; the third column is a `SUM`.
  - D) `MAX(quantity)` is the largest quantity (10), not the number of rows (16).

**Source:** `aggregate-functions.md`
</details>

---

## Part 4: Fill-in-the-Blank

### 53. To copy the completed orders into a scratch table, you complete the statement with `INSERT INTO completed_orders_archive (order_id, customer_id, total_amount) ________ order_id, customer_id, total_amount FROM orders WHERE status = 'completed';`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `SELECT` (this is `INSERT ... SELECT`)

**Explanation:** Instead of `VALUES`, an `INSERT` can be fed by a `SELECT`: the query runs first and each result row is inserted. The column lists must match in count and order. On the QA Shop data this copies the 8 completed orders.

**Source:** `insert-update-and-delete.md`
</details>

---

### 54. A transaction started with `BEGIN;` ends either with `________;` to keep the changes or with `________;` to undo them.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `COMMIT` (first blank) and `ROLLBACK` (second blank)

**Explanation:** `COMMIT` makes everything since `BEGIN` permanent, while `ROLLBACK` undoes it. QA engineers use `BEGIN ... ROLLBACK` as a cheap way to experiment without damage.

**Source:** `insert-update-and-delete.md`
</details>

---

### 55. An order whose `customer_id` is ________ is a legitimate guest order, not an orphan, because a foreign key column may hold this value to mean "no parent".

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `NULL`

**Explanation:** A foreign key must either match an existing parent or be NULL (unless the column is also `NOT NULL`). Order 108 has a NULL customer and is not reported by `PRAGMA foreign_key_check`, whereas order 107 (customer 99, which does not exist) is a true orphan.

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 56. In SQLite, foreign keys declared in `CREATE TABLE` are only enforced after you run `PRAGMA ________ = ON;` on the connection.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `foreign_keys`

**Explanation:** SQLite ignores declared foreign keys unless you switch enforcement on for each connection (`PRAGMA foreign_keys;` prints 0 by default). That is how orphans such as order 107 exist in the practice data.

**Source:** `basic-database-constraints-primary-and-foreign-keys.md`
</details>

---

### 57. When the key column has the same name in both tables, you can write `FROM orders INNER JOIN customers ________ (customer_id)` instead of an `ON` condition (SQL Server does not support this form).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `USING`

**Explanation:** `USING (customer_id)` is shorthand for matching the same-named column on both sides. It works in SQLite, MySQL and PostgreSQL, which is why many teams stay with the more portable `ON`.

**Source:** `inner-join.md`
</details>

---

### 58. In test-data validation, every check is written as a query that returns the rows that ________ the rule, so that zero rows (or a count of 0) means the check passes.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `break` (or `violate`)

**Explanation:** This is the "violations query" convention. Because the query returns only offending rows, an empty result means PASS, and any returned row is both the failure and the evidence (for example, the IDs to put in a defect report).

**Source:** `test-data-validation-using-sql.md`
</details>

---

### 59. Test data is torn down in ________-to-________ order (for example `payments` and `order_items`, then `orders`, then `customers`) so that foreign keys are not violated.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `child` (first blank) and `parent` (second blank)

**Explanation:** A parent row cannot be deleted while child rows still point to it. Insert in parent-to-child order, delete in child-to-parent order, then verify that no marked test rows remain.

**Source:** `test-data-validation-using-sql.md`
</details>

---

### 60. To list exactly which rows differ between a source and a target table, run `SELECT ... FROM demo_source ________ SELECT ... FROM demo_target;` and then repeat it with the two tables swapped.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `EXCEPT`

**Explanation:** `EXCEPT` returns the rows of the first result that are not in the second. Running it in both directions exposes lost rows, extra rows and changed values, which equal row counts alone cannot.

**Source:** `test-data-validation-using-sql.md`
</details>

---

## Part 5: Scenario-Based

### 61. The finance dashboard shows revenue from completed orders of 1535.45. Your report `SELECT SUM(o.total_amount) FROM orders AS o INNER JOIN customers AS c ON c.customer_id = o.customer_id WHERE o.status = 'completed';` returns 1490.46. Which explanation fits the data?
- [ ] A) Completed orders 107 (customer 99 does not exist, 35.00) and 108 (NULL customer, 9.99) cannot match any customer, so the inner join silently drops 44.99
- [ ] B) Floating-point rounding makes the two sums differ by a few cents
- [ ] C) The duplicate customer Bob Smith (customer 8) was counted twice
- [ ] D) Order 109, which has no item rows, was dropped by the join

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Completed orders 107 (customer 99 does not exist, 35.00) and 108 (NULL customer, 9.99) cannot match any customer, so the inner join silently drops 44.99

**Explanation:** 1535.45 - 1490.46 = 44.99 = 35.00 + 9.99. An inner join removes rows with an orphan or NULL key without any error, so a good validation compares figures before and after the join.
- **Why others are wrong:**
  - B) The gap is 44.99, far too large for rounding noise; rounding differences would be around a fraction of a cent.
  - C) Customer 8 has no orders, and a join can only repeat an order when several customer rows match it, which does not happen here.
  - D) The report does not join `order_items`, and order 109 is pending, so it is not in the completed total at all.

**Source:** `inner-join.md`
</details>

---

### 62. You extend an integrity query by joining `orders` to both `order_items` and `payments`. For order 102 it reports `SUM(pay.amount) = 121.92`, although the `payments` table holds two rows of 30.48 for that order (60.96 in total). What is the best fix?
```sql
SELECT SUM(pay.amount)
FROM orders AS o
INNER JOIN order_items AS i   ON i.order_id   = o.order_id
INNER JOIN payments    AS pay ON pay.order_id = o.order_id
WHERE o.order_id = 102;
```
- [ ] A) Use `SUM(DISTINCT pay.amount)` so repeated values are counted once
- [ ] B) Aggregate each child table in its own subquery (one row per order) and `LEFT JOIN` those results to `orders`
- [ ] C) Change both `INNER JOIN`s to `LEFT JOIN`s
- [ ] D) Delete one of the two item rows for order 102 so each payment is repeated only once

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Aggregate each child table in its own subquery (one row per order) and `LEFT JOIN` those results to `orders`

**Explanation:** This is the fan-out trap: order 102 has 2 item rows and 2 payment rows, so the join produces 2 x 2 = 4 rows and every payment is counted twice (4 x 30.48 = 121.92). Pre-aggregating each child table gives one row per order, so no multiplication can occur: items 30.48 and paid 60.96, which also exposes the double payment.
- **Why others are wrong:**
  - A) `SUM(DISTINCT ...)` returns 30.48, because the two payments have the same amount. It hides the double payment, the very defect the check should find.
  - C) Outer joins multiply rows in exactly the same way; the sum is still 121.92.
  - D) Items 3 and 4 are different products (USB-C Cable and Notebook), both legitimate lines. Deleting one destroys valid data to make a number look right.

**Source:** `multi-table-queries.md`
</details>

---

### 63. Your report must list every order with the customer name (or "(no customer)") and its number of item rows. A colleague's query returns 11 rows and order 109 is missing. What is the best fix?
```sql
SELECT o.order_id,
       COALESCE(c.full_name, '(no customer)') AS customer,
       COUNT(i.item_id) AS item_rows
FROM orders AS o
LEFT JOIN customers    AS c ON c.customer_id = o.customer_id
INNER JOIN order_items AS i ON i.order_id    = o.order_id
GROUP BY o.order_id, c.full_name;
```
- [ ] A) Change `COUNT(i.item_id)` to `COUNT(*)`
- [ ] B) Add `WHERE o.status = 'pending'`
- [ ] C) Change `INNER JOIN order_items` to `LEFT JOIN order_items`, so the whole chain keeps unmatched orders; `COUNT(i.item_id)` then reports 0 for order 109 (12 rows)
- [ ] D) Put `customers` in the `FROM` clause and join `orders` to it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Change `INNER JOIN order_items` to `LEFT JOIN order_items`, so the whole chain keeps unmatched orders; `COUNT(i.item_id)` then reports 0 for order 109 (12 rows)

**Explanation:** Order 109 has no item rows, so the inner join discards it even though the earlier `LEFT JOIN` was meant to protect every order. With a `LEFT JOIN` chain all 12 orders appear, and counting the child key gives 0 for order 109.
- **Why others are wrong:**
  - A) The row for order 109 is already gone before counting, so changing the counting expression cannot bring it back.
  - B) A `WHERE` filter can only remove rows; it cannot restore the order that the inner join dropped.
  - D) That preserves customers instead of orders and would lose the orphan order 107 and guest order 108, which the report must show.

**Source:** `multi-table-queries.md`
</details>

---

### 64. After a nightly load, the release gate has this rule: every completed order must have a paid total (payments with `status = 'paid'`) equal to its header total. You run:
```sql
SELECT o.order_id, o.total_amount, COALESCE(pa.paid_total, 0) AS paid_total
FROM orders AS o
LEFT JOIN (
    SELECT order_id, SUM(amount) AS paid_total
    FROM payments
    WHERE status = 'paid'
    GROUP BY order_id
) AS pa ON pa.order_id = o.order_id
WHERE o.status = 'completed'
  AND ROUND(o.total_amount, 2) <> ROUND(COALESCE(pa.paid_total, 0), 2);
```
Which rows does it return, and what do they mean?
- [ ] A) Orders 105 and 109: pending orders with no payment
- [ ] B) Orders 103, 109, 110 and 112: orders whose header total differs from the total of their items
- [ ] C) Order 102 only: it was paid twice; order 112 is not returned because it has no payment row to compare
- [ ] D) Orders 102 and 112: order 102 shows 60.96 paid against a 30.48 header (the double payment), and order 112 is completed with nothing paid (0 against 9.99)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Orders 102 and 112

**Explanation:** The derived table sums paid payments per order (order 102 has payments 2 and 11, 30.48 each, so 60.96). The `LEFT JOIN` keeps orders with no payment, and `COALESCE(..., 0)` turns their NULL into 0, so completed order 112 (9.99 vs 0) is flagged along with 102. Completed orders 101, 103, 107, 108, 110 and 111 are paid exactly their header total, so they pass this rule.
- **Why others are wrong:**
  - A) The `WHERE` restricts the check to completed orders; 105 and 109 are pending.
  - B) That is the result of the header-versus-items check from the subqueries and validation lessons. This query compares the header with payments, so 103 and 110 (paid = header) are not returned.
  - C) Order 112 is returned precisely because of the `LEFT JOIN` plus `COALESCE`: the missing payment becomes 0, which is not equal to 9.99.

**Source:** `test-data-validation-using-sql.md`
</details>

---

### 65. Your validation suite has the check "order totals differing from lines": it compares each order's header total with the recomputed item total, using a `LEFT JOIN` to per-order item sums and `COALESCE(..., 0)`. It reports 4 violations. Which orders do you list as evidence in the defect report?
- [ ] A) Orders 103, 110 and 112 only
- [ ] B) Orders 102, 103, 110 and 112
- [ ] C) Orders 103, 109, 110 and 112
- [ ] D) Orders 105, 109 and 112

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Orders 103, 109, 110 and 112

**Explanation:** Order 103 has a duplicate line (items total 300.00 vs 150.00), 109 has a header of 80.00 but no lines, 110 has 55.00 vs 50.00, and 112 has a negative line (-9.99 vs 9.99). The `LEFT JOIN` with `COALESCE` is what brings in order 109.
- **Why others are wrong:**
  - A) That is the result of the `INNER JOIN` version, which cannot see order 109 because it has no item rows.
  - B) Order 102's items total equals its header (30.48); its problem is the double payment, which a different check reports.
  - D) Those are the orders with no payment, found by a payments check, not by the header-versus-lines comparison.

**Source:** `test-data-validation-using-sql.md`
</details>

---

## Answer Key

| Q# | Answer | Q# | Answer | Q# | Answer |
|----|--------|----|--------|----|--------|
| 1 | A | 23 | B | 45 | D |
| 2 | D | 24 | A | 46 | D |
| 3 | B | 25 | B | 47 | D |
| 4 | D | 26 | C | 48 | B |
| 5 | C | 27 | B | 49 | C |
| 6 | A | 28 | A (True) | 50 | C |
| 7 | C | 29 | B (False) | 51 | B |
| 8 | A | 30 | B (False) | 52 | A |
| 9 | D | 31 | B (False) | 53 | `SELECT` |
| 10 | B | 32 | A (True) | 54 | `COMMIT` / `ROLLBACK` |
| 11 | C | 33 | A (True) | 55 | `NULL` |
| 12 | C | 34 | B (False) | 56 | `foreign_keys` |
| 13 | A | 35 | B (False) | 57 | `USING` |
| 14 | D | 36 | A (True) | 58 | `break` / `violate` |
| 15 | A | 37 | A (True) | 59 | `child` / `parent` |
| 16 | D | 38 | A (True) | 60 | `EXCEPT` |
| 17 | C | 39 | B (False) | 61 | A |
| 18 | A | 40 | B | 62 | B |
| 19 | B | 41 | C | 63 | C |
| 20 | D | 42 | D | 64 | D |
| 21 | B | 43 | A | 65 | C |
| 22 | C | 44 | A |  |  |
