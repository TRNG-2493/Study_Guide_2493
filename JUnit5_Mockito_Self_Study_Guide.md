# JUnit 5 + Mockito: A Self-Study Guide for pytest Users

> **Audience:** QEA learners who already know **Java** and **pytest**
> **Time:** ~2.5 hours (reading + hands-on)
> **You will learn:** how to write, organize, and run unit tests in Java with **JUnit 5**, how to isolate code with **Mockito**, and how all of it maps to what you already know from pytest.

---

## Table of Contents

0. [Setup](#module-0--setup-15-min)
1. [Your First JUnit Test](#module-1--your-first-junit-test-20-min)
2. [Beyond Basic Assertions](#module-2--beyond-basic-assertions-20-min)
3. [Test Lifecycle (≈ pytest fixtures)](#module-3--test-lifecycle--pytest-fixtures-20-min)
4. [Parameterized Tests](#module-4--parameterized-tests-20-min)
5. [Organizing Tests: Tags, Nested, Assumptions](#module-5--organizing-tests-10-min)
6. [Mockito](#module-6--mockito-40-min)
7. [pytest vs JUnit: Side-by-Side](#module-7--pytest-vs-junit-15-min)
8. [Cheat Sheet](#cheat-sheet)

### How to use this guide

Every module has four parts:

| Part | What you do |
|---|---|
| 📖 **Concept** | Read the explanation |
| 🐍 **pytest bridge** | See how it maps to what you already know |
| 💻 **Demo** | Type (don't paste!) the code and run it |
| ✍️ **Try it** | Do the short exercises before moving on |

### The running example: a tiny Online Store

We use **one small codebase** for the whole guide so you can focus on *testing*, not on learning new business logic.

| Class | Used in | What it does |
|---|---|---|
| `Calculator` | Module 1, 4 | add / subtract / multiply / divide |
| `ShoppingCart` | Modules 1–5 | add/remove items, totals, discount codes |
| `OrderService` | Module 6 | places orders using an `InventoryRepository` and a `PaymentGateway` |

---

## Module 0 – Setup (15 min)

### 📖 Concept

JUnit is **not built into Java** (just like pytest isn't built into Python). We add it as a dependency using **Maven**, Java's build tool (think `pip` + `requirements.txt` + a test runner, all in one).

**JUnit 5** is made of three parts. You don't need to memorize them, but you'll see the names in error messages:

| Part | Role |
|---|---|
| **JUnit Platform** | The engine that discovers and launches tests (used by IDEs and Maven) |
| **JUnit Jupiter** | The API you write tests with (`@Test`, `assertEquals`, …) |
| **JUnit Vintage** | Runs old JUnit 4 tests (we won't use it) |

> ℹ️ **About versions:** this guide uses **JUnit 5.11** and **Mockito 5**. JUnit 6 (released late 2025) uses the *same* Jupiter API, so everything you learn here carries over unchanged.

### Step 1: Create the project structure

Create a Maven project (IntelliJ: *File → New → Project → Maven*, or VS Code with the *Extension Pack for Java*). The layout must be:

```
online-store/
├── pom.xml
└── src/
    ├── main/java/com/store/      ← production code
    │   ├── Calculator.java
    │   ├── ShoppingCart.java
    │   ├── OrderService.java
    │   ├── OrderStatus.java
    │   ├── PaymentGateway.java
    │   └── InventoryRepository.java
    └── test/java/com/store/      ← test code (same package!)
        └── CalculatorTest.java ...
```

> 🐍 **pytest bridge:** in pytest you could put `test_*.py` anywhere. In Maven, **tests must live under `src/test/java`**. Putting the test in the *same package* as the class under test is the convention.

### Step 2: `pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.store</groupId>
    <artifactId>online-store</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!-- The BOM keeps all JUnit artifacts on the same version -->
            <dependency>
                <groupId>org.junit</groupId>
                <artifactId>junit-bom</artifactId>
                <version>5.11.4</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- JUnit 5: API + engine + parameterized tests -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <!-- Mockito + its JUnit 5 extension -->
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-junit-jupiter</artifactId>
            <version>5.14.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Runs the tests during `mvn test` -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.5.2</version>
            </plugin>
        </plugins>
    </build>
</project>
```

`<scope>test</scope>` means "only available to test code" (it won't ship with the application).

### Step 3: Add the production code

Create these files under `src/main/java/com/store/`. **Read them**, because you'll be testing their behavior.

<details>
<summary><b>Calculator.java</b> (click to expand)</summary>

```java
package com.store;

public class Calculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return a / b;
    }
}
```
</details>

<details>
<summary><b>ShoppingCart.java</b></summary>

```java
package com.store;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;

public class ShoppingCart {

    private final Map<String, Integer> quantities = new LinkedHashMap<>();
    private final Map<String, Double> prices = new HashMap<>();

    public void addItem(String name, double price, int quantity) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Item name is required");
        }
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        quantities.merge(name, quantity, Integer::sum); // adds to existing qty
        prices.put(name, price);
    }

    public void removeItem(String name) {
        if (!quantities.containsKey(name)) {
            throw new NoSuchElementException("Item not in cart: " + name);
        }
        quantities.remove(name);
        prices.remove(name);
    }

    public int getItemCount() {
        return quantities.values().stream().mapToInt(Integer::intValue).sum();
    }

    public List<String> getItemNames() {
        return new ArrayList<>(quantities.keySet());
    }

    public double getTotal() {
        double total = 0;
        for (String name : quantities.keySet()) {
            total += prices.get(name) * quantities.get(name);
        }
        return total;
    }

    /** Returns the total after applying a discount code: SAVE10 = 10% off, SAVE20 = 20% off. */
    public double applyDiscount(String code) {
        if (code == null || code.isBlank()) {
            throw new IllegalArgumentException("Discount code is required");
        }
        switch (code.toUpperCase()) {
            case "SAVE10": return getTotal() * 0.90;
            case "SAVE20": return getTotal() * 0.80;
            default: throw new IllegalArgumentException("Invalid discount code: " + code);
        }
    }

    public boolean isEmpty() {
        return quantities.isEmpty();
    }

    public void clear() {
        quantities.clear();
        prices.clear();
    }
}
```
</details>

<details>
<summary><b>PaymentGateway.java, InventoryRepository.java, OrderStatus.java, OrderService.java</b> (used in Module 6)</summary>

```java
package com.store;

public interface PaymentGateway {
    /** Charges the customer. Returns true if the payment succeeded. */
    boolean charge(String customerId, double amount);
}
```

```java
package com.store;

public interface InventoryRepository {
    int getStock(String productId);
    void reduceStock(String productId, int quantity);
}
```

```java
package com.store;

public enum OrderStatus {
    CONFIRMED,
    PAYMENT_FAILED
}
```

```java
package com.store;

public class OrderService {

    private final InventoryRepository inventory;
    private final PaymentGateway paymentGateway;

    public OrderService(InventoryRepository inventory, PaymentGateway paymentGateway) {
        this.inventory = inventory;
        this.paymentGateway = paymentGateway;
    }

    public OrderStatus placeOrder(String customerId, String productId, int quantity, double unitPrice) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }

        int stock = inventory.getStock(productId);
        if (stock < quantity) {
            throw new IllegalStateException("Insufficient stock for " + productId);
        }

        boolean paid = paymentGateway.charge(customerId, quantity * unitPrice);
        if (!paid) {
            return OrderStatus.PAYMENT_FAILED;
        }

        inventory.reduceStock(productId, quantity);
        return OrderStatus.CONFIRMED;
    }
}
```
</details>

### Step 4: Running tests

| How | Command / action | pytest equivalent |
|---|---|---|
| All tests | `mvn test` | `pytest` |
| One class | `mvn test -Dtest=CalculatorTest` | `pytest test_calculator.py` |
| One method | `mvn test -Dtest=CalculatorTest#addReturnsSumOfTwoNumbers` | `pytest test_calculator.py::test_add` |
| By tag | `mvn test -Dgroups=smoke` | `pytest -m smoke` |
| IDE | Click the green ▶ next to a class or method | — |

Test reports are written to `target/surefire-reports/`.

### ✍️ Try it

1. Create the project, add the `pom.xml`, and add all production classes.
2. Run `mvn test`. You should see `BUILD SUCCESS` with `Tests run: 0` (we haven't written any yet). If it fails, fix the setup before continuing.

---

## Module 1 – Your First JUnit Test (20 min)

### 📖 Concept

A JUnit test is just a **method annotated with `@Test`** inside a **test class**.

Rules:
- The test class name ends in `Test` (e.g. `CalculatorTest`). Maven's Surefire plugin looks for `*Test`, `Test*`, `*Tests`, and `*TestCase` by default.
- Test methods are annotated with `@Test`, return `void`, and take no parameters (except in parameterized tests).
- Neither the class nor the methods need to be `public` in JUnit 5.
- Assertions come from `org.junit.jupiter.api.Assertions` (usually imported statically).

### 🐍 pytest bridge

```python
# pytest
def test_add_returns_sum():
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

```java
// JUnit 5
@Test
void addReturnsSumOfTwoNumbers() {
    Calculator calculator = new Calculator();
    assertEquals(5, calculator.add(2, 3));
}
```

> ⚠️ **#1 beginner mistake: argument order.** It's `assertEquals(EXPECTED, ACTUAL)`. If you swap them the test still passes or fails correctly, but the failure message will be backwards: `expected: <7> but was: <5>`, which sends you debugging in the wrong direction.

### The AAA pattern

Structure every test as **Arrange → Act → Assert**, just like you did in pytest.

### 💻 Demo: `CalculatorTest.java`

```java
package com.store;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class CalculatorTest {

    @Test
    void addReturnsSumOfTwoNumbers() {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.add(2, 3);

        // Assert
        assertEquals(5, result);
    }

    @Test
    void subtractReturnsDifference() {
        Calculator calculator = new Calculator();
        assertEquals(6, calculator.subtract(10, 4), "10 - 4 should be 6");
    }
}
```

The optional last argument (`"10 - 4 should be 6"`) is a **failure message**, like `assert x == y, "message"` in pytest.

### The core assertions

| JUnit | pytest |
|---|---|
| `assertEquals(expected, actual)` | `assert actual == expected` |
| `assertNotEquals(a, b)` | `assert a != b` |
| `assertTrue(condition)` | `assert condition` |
| `assertFalse(condition)` | `assert not condition` |
| `assertNull(x)` / `assertNotNull(x)` | `assert x is None` / `assert x is not None` |
| `assertSame(a, b)` | `assert a is b` |
| `assertEquals(0.3, actual, 0.001)` | `assert actual == pytest.approx(0.3)` |

> ⚠️ **Comparing `double`s:** always pass a **delta** (tolerance) as the third argument. `0.1 + 0.2` is `0.30000000000000004` in Java too!

### 💻 Demo: `ShoppingCartBasicsTest.java`

```java
package com.store;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ShoppingCartBasicsTest {

    @Test
    void newCartIsEmpty() {
        ShoppingCart cart = new ShoppingCart();

        assertTrue(cart.isEmpty());
        assertEquals(0, cart.getItemCount());
    }

    @Test
    void addingItemMakesCartNonEmpty() {
        ShoppingCart cart = new ShoppingCart();

        cart.addItem("Pen", 1.50, 2);

        assertFalse(cart.isEmpty());
        assertEquals(2, cart.getItemCount());
    }

    @Test
    void totalIsPriceTimesQuantity() {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Pen", 1.50, 2);
        cart.addItem("Notebook", 4.25, 1);

        // doubles: always pass a delta (tolerance)
        assertEquals(7.25, cart.getTotal(), 0.001);
    }

    @Test
    void itemNamesKeepInsertionOrder() {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Pen", 1.50, 1);
        cart.addItem("Notebook", 4.25, 1);

        assertNotNull(cart.getItemNames());
        assertEquals(List.of("Pen", "Notebook"), cart.getItemNames());
    }
}
```

### Reading a failure

Change `assertEquals(5, result)` to `assertEquals(6, result)` and run it:

```
org.opentest4j.AssertionFailedError: expected: <6> but was: <5>
    at com.store.CalculatorTest.addReturnsSumOfTwoNumbers(CalculatorTest.java:19)
```

You get the expected value, the actual value, and the exact line. Change it back afterwards.

### ✍️ Try it

1. Add a test `multiplyReturnsProduct` to `CalculatorTest` that checks `4 * 5 == 20`.
2. Add a test that checks `multiply(7, 0)` returns `0`.
3. Write a test that adds `"Pen"` twice (qty 1, then qty 2) and asserts `getItemCount()` is `3` **and** that `getItemNames()` has size `1`.
4. Swap the arguments in one `assertEquals` on purpose, make it fail, and read the message. What's misleading about it?
5. **Question:** Why does `assertEquals(0.3, 0.1 + 0.2)` fail, and how do you fix it?

---

## Module 2 – Beyond Basic Assertions (20 min)

### 📖 Concept

Real tests need more than equality checks. You need to verify **exceptions**, check **several things at once**, compare **collections**, enforce **time limits**, and make reports **readable**.

### 🐍 pytest bridge

| pytest | JUnit 5 |
|---|---|
| `with pytest.raises(ValueError):` | `assertThrows(IllegalArgumentException.class, () -> ...)` |
| `with pytest.raises(ValueError, match="neg"):` | `ex = assertThrows(...); assertEquals("...", ex.getMessage())` |
| *(no direct equivalent; pytest-check plugin)* | `assertAll(...)` reports *all* failures in a group |
| `assert list_a == list_b` | `assertEquals` / `assertIterableEquals` / `assertArrayEquals` |
| `pytest-timeout` plugin | `assertTimeout(Duration, ...)` |
| `@pytest.mark.skip(reason=...)` | `@Disabled("reason")` |
| test function name / docstring | `@DisplayName("Readable name")` |

### Lambdas: the `() -> ...` syntax

`assertThrows` needs to *run* the code itself so it can catch the exception. You therefore pass the code in as a **lambda**, a small block of code that runs later. It's the same idea as the `with` block in `pytest.raises`.

```java
() -> cart.addItem("Pen", -1.0, 1)
```

### 💻 Demo: `ShoppingCartAssertionsTest.java`

```java
package com.store;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.util.List;
import java.util.NoSuchElementException;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("ShoppingCart – advanced assertions")
class ShoppingCartAssertionsTest {

    @Test
    @DisplayName("Adding an item with a negative price throws")
    void negativePriceThrows() {
        ShoppingCart cart = new ShoppingCart();

        IllegalArgumentException ex = assertThrows(
                IllegalArgumentException.class,
                () -> cart.addItem("Pen", -1.0, 1));

        assertEquals("Price cannot be negative", ex.getMessage());
    }

    @Test
    @DisplayName("Removing a missing item throws NoSuchElementException")
    void removingMissingItemThrows() {
        ShoppingCart cart = new ShoppingCart();

        assertThrows(NoSuchElementException.class, () -> cart.removeItem("Ghost"));
    }

    @Test
    @DisplayName("Valid input does not throw")
    void validItemDoesNotThrow() {
        ShoppingCart cart = new ShoppingCart();

        assertDoesNotThrow(() -> cart.addItem("Pen", 1.0, 1));
    }

    @Test
    @DisplayName("assertAll reports every failure, not just the first")
    void cartStateAfterAddingItems() {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Pen", 1.50, 2);
        cart.addItem("Pen", 1.50, 3);   // same item again -> quantity adds up

        assertAll("cart state",
                () -> assertEquals(5, cart.getItemCount()),
                () -> assertEquals(7.50, cart.getTotal(), 0.001),
                () -> assertIterableEquals(List.of("Pen"), cart.getItemNames())
        );
    }

    @Test
    @DisplayName("Total is calculated quickly")
    void totalIsFast() {
        ShoppingCart cart = new ShoppingCart();
        for (int i = 0; i < 1_000; i++) {
            cart.addItem("Item" + i, 1.0, 1);
        }

        double total = assertTimeout(Duration.ofMillis(200), () -> cart.getTotal());
        assertEquals(1000.0, total, 0.001);
    }

    @Test
    @Disabled("Gift cards not implemented yet – JIRA-123")
    void giftCardIsApplied() {
        fail("not implemented");
    }
}
```

### Key points

- **`assertThrows` returns the exception**, so you can assert on its message. It also fails if the code throws *nothing*, or throws an unrelated exception type.
- **`assertAll`**: normally a test stops at the first failed assertion. `assertAll` runs *every* assertion in the group and reports all failures together. That's great for checking the state of one object.
- **`fail("msg")`** fails a test unconditionally (like `pytest.fail()`).
- **`@Disabled`** tests show up as *skipped* in the report. Always give a reason.

### ✍️ Try it

1. Write a test proving `calculator.divide(10, 0)` throws `IllegalArgumentException` with the message `"Cannot divide by zero"`.
2. Write a test proving `addItem("", 1.0, 1)` throws, and check the message is `"Item name is required"`.
3. Write a test proving `addItem(null, 1.0, 1)` throws. Do you need a separate test from #2? (Hint: Module 4 will make this neater.)
4. Make one assertion inside the `assertAll` demo fail on purpose, then make **two** fail. Compare the output with what you'd get from two plain `assertEquals` calls.
5. Add `@DisplayName` to every test in `CalculatorTest` and look at how the IDE test tree changes.
6. **Question:** What happens if the code inside `assertThrows` doesn't throw anything?

---

## Module 3 – Test Lifecycle (≈ pytest fixtures) (20 min)

### 📖 Concept

You've probably noticed we keep writing `ShoppingCart cart = new ShoppingCart();` in every test. JUnit's **lifecycle annotations** let you run setup and teardown code automatically.

| Annotation | Runs | Must be `static`? |
|---|---|---|
| `@BeforeAll` | **once** before all tests in the class | ✅ yes |
| `@BeforeEach` | before **every** test | no |
| `@AfterEach` | after **every** test (even if it failed) | no |
| `@AfterAll` | **once** after all tests in the class | ✅ yes |

### 🐍 pytest bridge

```python
# pytest
@pytest.fixture
def cart():
    c = ShoppingCart()           # setup
    c.add_item("Pen", 1.50, 2)
    yield c
    c.clear()                    # teardown

def test_count(cart):
    assert cart.get_item_count() == 2
```

| pytest | JUnit 5 |
|---|---|
| `@pytest.fixture` (function scope), code before `yield` | `@BeforeEach` |
| code after `yield` | `@AfterEach` |
| `@pytest.fixture(scope="class"/"module")` | `@BeforeAll` / `@AfterAll` (static) |
| Fixture injected by **parameter name** | Fixture stored in a **field** of the test class |
| `conftest.py` sharing | A base class, or a JUnit **extension** (advanced) |

### 🔑 Important: a new instance per test

JUnit creates a **brand-new instance of the test class for every test method**. Fields therefore never leak from one test to another, so tests stay **independent**. This is also why `@BeforeAll` must be `static`: it runs before any instance exists.

### 💻 Demo: `ShoppingCartLifecycleTest.java`

```java
package com.store;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class ShoppingCartLifecycleTest {

    private ShoppingCart cart;   // fresh for every test

    @BeforeAll
    static void beforeAll() {
        System.out.println("@BeforeAll  - runs ONCE before all tests (must be static)");
    }

    @BeforeEach
    void setUp() {
        System.out.println("  @BeforeEach - new cart");
        cart = new ShoppingCart();
        cart.addItem("Pen", 1.50, 2);
    }

    @AfterEach
    void tearDown() {
        System.out.println("  @AfterEach  - clearing cart");
        cart.clear();
    }

    @AfterAll
    static void afterAll() {
        System.out.println("@AfterAll   - runs ONCE after all tests (must be static)");
    }

    @Test
    void cartStartsWithOnePenEntry() {
        System.out.println("    test 1");
        assertEquals(2, cart.getItemCount());
    }

    @Test
    void removingPenEmptiesCart() {
        System.out.println("    test 2");
        cart.removeItem("Pen");
        assertTrue(cart.isEmpty());
    }

    @Test
    void eachTestGetsItsOwnCart() {
        System.out.println("    test 3");
        // Even if test 2 ran first and removed the pen, we still have it here
        assertFalse(cart.isEmpty());
    }
}
```

**Expected console output** (test order may vary):

```
@BeforeAll  - runs ONCE before all tests (must be static)
  @BeforeEach - new cart
    test 1
  @AfterEach  - clearing cart
  @BeforeEach - new cart
    test 2
  @AfterEach  - clearing cart
  @BeforeEach - new cart
    test 3
  @AfterEach  - clearing cart
@AfterAll   - runs ONCE after all tests (must be static)
```

> ⚠️ **Test order is not guaranteed** (same as pytest with random-order plugins). Never write a test that depends on another test having run first.

### When to use `@BeforeAll`

Use it for **expensive, read-only** setup: starting a test server, loading a large config file, or opening a database connection. Use `@BeforeEach` for anything a test might **modify**, such as our cart.

### ✍️ Try it

1. Refactor `ShoppingCartBasicsTest` so that the cart is created in a `@BeforeEach` method. How many lines did you remove?
2. Remove `static` from `@BeforeAll` and run the test. What error do you get?
3. In `ShoppingCartLifecycleTest`, make `cart` a `static` field and create it in `@BeforeAll` instead of `@BeforeEach`. Run the tests several times. Which test(s) can now fail, and why? (Put it back afterwards!)
4. **Question:** Which pytest fixture scope is closest to `@BeforeEach`? Which is closest to `@BeforeAll`?

---

## Module 4 – Parameterized Tests (20 min)

### 📖 Concept

When the same test logic should run with **different inputs**, don't copy-paste tests. Write **one** parameterized test instead.

Replace `@Test` with `@ParameterizedTest`, then add a **source** annotation that supplies the data:

| Source | Use it for |
|---|---|
| `@ValueSource(ints = {...})` / `strings` / `doubles` ... | **one** argument per run |
| `@CsvSource({"a, b, expected", ...})` | **several** arguments per run, like table rows |
| `@MethodSource("methodName")` | data built in code (complex objects, generated data) |
| `@NullSource`, `@EmptySource`, `@NullAndEmptySource` | edge cases: `null` and `""` |
| `@EnumSource(MyEnum.class)` | every value of an enum |
| `@CsvFileSource(resources = "/data.csv")` | data from a CSV file in `src/test/resources` |

### 🐍 pytest bridge

```python
# pytest
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-5, 5, 0),
])
def test_add(a, b, expected):
    assert Calculator().add(a, b) == expected
```

```java
// JUnit 5
@ParameterizedTest
@CsvSource({
        "1,  2, 3",
        "0,  0, 0",
        "-5, 5, 0"
})
void addition(int a, int b, int expected) {
    assertEquals(expected, calculator.add(a, b));
}
```

The values in `@CsvSource` are text. JUnit **converts them automatically** to the parameter types (`int`, `double`, `String`, enums, ...).

### 💻 Demo: `ParameterizedExamplesTest.java`

```java
package com.store;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class ParameterizedExamplesTest {

    private final Calculator calculator = new Calculator();

    // 1) One argument per run
    @ParameterizedTest
    @ValueSource(ints = {0, -1, -50})
    void zeroOrNegativeQuantityIsRejected(int quantity) {
        ShoppingCart cart = new ShoppingCart();
        assertThrows(IllegalArgumentException.class,
                () -> cart.addItem("Pen", 1.0, quantity));
    }

    // 2) Several arguments per run (like rows in a table)
    @ParameterizedTest(name = "{0} + {1} = {2}")
    @CsvSource({
            "1,   2,   3",
            "0,   0,   0",
            "-5,  5,   0",
            "100, 250, 350"
    })
    void addition(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    // 3) Discount codes (case-insensitive) -> expected total for a $100 cart
    @ParameterizedTest(name = "code {0} -> {1}")
    @CsvSource({
            "SAVE10, 90.0",
            "save10, 90.0",
            "SAVE20, 80.0"
    })
    void validDiscountCodes(String code, double expectedTotal) {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Headphones", 100.0, 1);

        assertEquals(expectedTotal, cart.applyDiscount(code), 0.001);
    }

    // 4) null, "" and a few bad values all throw
    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"  ", "SAVE50", "FREE"})
    void invalidDiscountCodesThrow(String code) {
        ShoppingCart cart = new ShoppingCart();
        cart.addItem("Headphones", 100.0, 1);

        assertThrows(IllegalArgumentException.class, () -> cart.applyDiscount(code));
    }

    // 5) Arguments from a method – useful for complex objects
    static Stream<Arguments> divisionCases() {
        return Stream.of(
                Arguments.of(10, 2, 5),
                Arguments.of(9, 3, 3),
                Arguments.of(7, 2, 3)     // integer division
        );
    }

    @ParameterizedTest
    @MethodSource("divisionCases")
    void division(int a, int b, int expected) {
        assertEquals(expected, calculator.divide(a, b));
    }
}
```

### Key points

- `name = "{0} + {1} = {2}"` controls how each run is displayed: `{0}` is the first argument, and so on. It's like pytest's `ids=`.
- Each row is reported as a **separate test**. If one row fails, the others still run.
- Example 4 shows that **source annotations can be combined**: `null`, `""`, `"  "`, `"SAVE50"`, and `"FREE"` give five runs from one method.
- A `@MethodSource` method must be **`static`** and return a `Stream` (or a `List`) of `Arguments`.

### ✍️ Try it

1. Write a `@ParameterizedTest` with `@CsvSource` for `multiply` with at least 4 rows, including a negative number and zero.
2. Use `@ValueSource(doubles = {...})` to prove that `addItem` rejects the negative prices `-0.01`, `-1`, and `-999.99`.
3. Use `@NullAndEmptySource` plus `@ValueSource(strings = {"   ", "\t"})` to test that invalid item names are rejected. (This replaces exercises 2–3 from Module 2 with **one** test!)
4. Write a `@MethodSource` test that takes three arguments, `(String item, double price, int qty)`, and checks `getTotal()` equals `price * qty` for a cart containing just that item.
5. **Question:** You have 20 input/output pairs. When would you choose `@CsvSource`, and when `@CsvFileSource`?

---

## Module 5 – Organizing Tests (10 min)

### 📖 Concept

As a test suite grows you need ways to **group**, **filter**, and **conditionally skip** tests.

| Feature | JUnit 5 | pytest equivalent |
|---|---|---|
| Label tests | `@Tag("smoke")` | `@pytest.mark.smoke` |
| Run only some labels | `mvn test -Dgroups=smoke` | `pytest -m smoke` |
| Exclude labels | `mvn test -DexcludedGroups=slow` | `pytest -m "not slow"` |
| Group related tests | `@Nested` inner classes | test classes / modules |
| Skip at runtime | `assumeTrue(condition)` | `pytest.skip()` / `@pytest.mark.skipif` |
| Skip by OS/env (declarative) | `@EnabledOnOs(OS.LINUX)`, `@EnabledIfEnvironmentVariable(...)` | `@pytest.mark.skipif(sys.platform ...)` |

### `@Nested`: describing behavior in context

`@Nested` lets you group tests by **scenario**, so the report reads like a specification:

```
ShoppingCart
 ├─ when empty
 │   ├─ has zero items          ✔
 │   └─ has a total of 0        ✔
 └─ after adding items
     ├─ is not empty            ✔
     └─ is empty again after clear() ✔
```

The outer `@BeforeEach` runs **first**, then the nested class's `@BeforeEach`, so each level adds its own setup.

### 💻 Demo: `ShoppingCartNestedTest.java`

```java
package com.store;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

@DisplayName("ShoppingCart")
class ShoppingCartNestedTest {

    private ShoppingCart cart;

    @BeforeEach
    void createCart() {
        cart = new ShoppingCart();
    }

    @Nested
    @DisplayName("when empty")
    class WhenEmpty {

        @Test
        @Tag("smoke")
        @DisplayName("has zero items")
        void hasZeroItems() {
            assertEquals(0, cart.getItemCount());
        }

        @Test
        @DisplayName("has a total of 0")
        void totalIsZero() {
            assertEquals(0.0, cart.getTotal(), 0.001);
        }
    }

    @Nested
    @DisplayName("after adding items")
    class AfterAddingItems {

        @BeforeEach
        void addItems() {           // runs AFTER the outer @BeforeEach
            cart.addItem("Pen", 2.0, 3);
        }

        @Test
        @Tag("smoke")
        @DisplayName("is not empty")
        void isNotEmpty() {
            assertFalse(cart.isEmpty());
        }

        @Test
        @Tag("regression")
        @DisplayName("is empty again after clear()")
        void clearEmptiesCart() {
            cart.clear();
            assertTrue(cart.isEmpty());
        }
    }

    @Test
    @Tag("integration")
    void runsOnlyOnCi() {
        assumeTrue("true".equals(System.getenv("CI")), "Skipping: not running on CI");
        // ... slow checks that only make sense on the CI server
        assertTrue(true);
    }
}
```

> ℹ️ `@Nested` classes must be **non-static** inner classes, which is how they can see the outer `cart` field.

### `@Disabled` vs assumptions

| | `@Disabled` | `assumeTrue(...)` |
|---|---|---|
| Decided | When writing the code | At runtime |
| Typical use | "Not ready / known bug" | "Only makes sense in this environment" |
| Result | Skipped | Aborted (shown as skipped) |

### ✍️ Try it

1. Run `mvn test -Dgroups=smoke`. How many tests ran?
2. Run `mvn test -DexcludedGroups=integration`. Did `runsOnlyOnCi` run?
3. Add a third `@Nested` class, `"after applying a discount"`, whose `@BeforeEach` adds a $50 item. Write two tests in it: one for `SAVE10` and one for `SAVE20`.
4. **Question:** You tag tests `smoke`, `regression`, and `slow`. Write the Maven command to run `regression` tests but **not** `slow` ones.

---

## Module 6 – Mockito (40 min)

### 📖 Concept: why mock?

Look at `OrderService`. To place an order it needs:

- an `InventoryRepository`, which in real life talks to a **database**, and
- a `PaymentGateway`, which in real life charges a **real credit card**.

In a **unit test** we want to test `OrderService`'s **logic only**:

- Does it check stock first?
- Does it refuse to charge when stock is low?
- Does it reduce stock only after payment succeeds?

We don't want a real database or real payments. Here's how we test `OrderService` alone:

```
            ┌─────────────────────┐
            │    OrderService     │  ← the real code we're testing
            └─────────┬───────────┘
          ┌───────────┴───────────┐
  ┌───────▼────────┐     ┌────────▼───────┐
  │ MOCK Inventory │     │ MOCK Payment   │  ← fakes WE control
  └────────────────┘     └────────────────┘
```

A **mock** is a fake object that:
1. **returns whatever you tell it to** (*stubbing*), and
2. **remembers how it was called**, so you can check it later (*verification*).

**Mockito** is the most widely used mocking library for Java.

### 🐍 pytest bridge

| Python (`unittest.mock` / `pytest-mock`) | Mockito |
|---|---|
| `repo = Mock()` / `mocker.Mock()` | `@Mock InventoryRepository repo;` |
| `repo.get_stock.return_value = 10` | `when(repo.getStock("P1")).thenReturn(10);` |
| `repo.get_stock.side_effect = Exception("x")` | `when(repo.getStock("P1")).thenThrow(new RuntimeException("x"));` |
| `repo.reduce_stock.assert_called_once_with("P1", 3)` | `verify(repo).reduceStock("P1", 3);` |
| `repo.reduce_stock.assert_not_called()` | `verify(repo, never()).reduceStock(anyString(), anyInt());` |
| `assert repo.get_stock.call_count == 2` | `verify(repo, times(2)).getStock(any());` |
| `mock.ANY` | `any()`, `anyString()`, `anyInt()`, `anyDouble()` |
| `mock.call_args` | `ArgumentCaptor` |
| `mocker.patch("module.thing")` | inject the mock via the constructor (`@InjectMocks`) |

### The building blocks

**1. Enable Mockito for the test class**

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest { ... }
```

**2. Create mocks and inject them**

```java
@Mock InventoryRepository inventory;           // fake #1
@Mock PaymentGateway paymentGateway;           // fake #2
@InjectMocks OrderService orderService;        // REAL object, built with the fakes
```

`@InjectMocks` calls `new OrderService(inventory, paymentGateway)` for you, before every test.

**3. Stub: "when this is called, return that"**

```java
when(inventory.getStock("P1")).thenReturn(10);
when(paymentGateway.charge("C1", 30.0)).thenReturn(true);
when(inventory.getStock("BAD")).thenThrow(new RuntimeException("DB down"));
```

Unstubbed methods return **default values**: `0`, `false`, `null`, or an empty collection.

**4. Verify: "was this called, and how?"**

```java
verify(inventory).reduceStock("P1", 3);                  // called exactly once with these args
verify(inventory, times(2)).getStock("P1");              // exactly twice
verify(paymentGateway, never()).charge(anyString(), anyDouble()); // never called
verifyNoInteractions(paymentGateway);                    // nothing at all was called on it
```

**5. Argument matchers: "any value is fine"**

```java
when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(true);
verify(paymentGateway).charge(eq("C1"), anyDouble());
```

### 💻 Demo: `OrderServiceTest.java`

```java
package com.store;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;   // when, verify, times, never, any..., eq

@ExtendWith(MockitoExtension.class)   // turns on @Mock / @InjectMocks
class OrderServiceTest {

    @Mock
    InventoryRepository inventory;

    @Mock
    PaymentGateway paymentGateway;

    @InjectMocks
    OrderService orderService;        // created with the two mocks above

    @Test
    void successfulOrderIsConfirmedAndStockReduced() {
        // Arrange – stub the dependencies
        when(inventory.getStock("P1")).thenReturn(10);
        when(paymentGateway.charge("C1", 30.0)).thenReturn(true);

        // Act
        OrderStatus status = orderService.placeOrder("C1", "P1", 3, 10.0);

        // Assert – the result...
        assertEquals(OrderStatus.CONFIRMED, status);
        // ...and the interactions
        verify(paymentGateway).charge("C1", 30.0);
        verify(inventory).reduceStock("P1", 3);
    }

    @Test
    void failedPaymentDoesNotReduceStock() {
        when(inventory.getStock("P1")).thenReturn(10);
        when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(false);

        OrderStatus status = orderService.placeOrder("C1", "P1", 1, 25.0);

        assertEquals(OrderStatus.PAYMENT_FAILED, status);
        verify(inventory, never()).reduceStock(anyString(), anyInt());
    }

    @Test
    void insufficientStockThrowsAndNeverCharges() {
        when(inventory.getStock("P1")).thenReturn(2);

        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> orderService.placeOrder("C1", "P1", 5, 10.0));

        assertEquals("Insufficient stock for P1", ex.getMessage());
        verify(paymentGateway, never()).charge(anyString(), anyDouble());
    }

    @Test
    void invalidQuantityNeverTouchesDependencies() {
        assertThrows(IllegalArgumentException.class,
                () -> orderService.placeOrder("C1", "P1", 0, 10.0));

        verifyNoInteractions(inventory, paymentGateway);
    }

    @Test
    void repositoryErrorIsPropagated() {
        when(inventory.getStock("P1")).thenThrow(new RuntimeException("DB down"));

        RuntimeException ex = assertThrows(RuntimeException.class,
                () -> orderService.placeOrder("C1", "P1", 1, 10.0));

        assertEquals("DB down", ex.getMessage());
    }

    @Test
    void chargesQuantityTimesUnitPrice() {
        when(inventory.getStock("P1")).thenReturn(100);
        when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(true);

        orderService.placeOrder("C1", "P1", 4, 12.5);

        ArgumentCaptor<Double> amountCaptor = ArgumentCaptor.forClass(Double.class);
        verify(paymentGateway).charge(eq("C1"), amountCaptor.capture());
        assertEquals(50.0, amountCaptor.getValue(), 0.001);
    }

    @Test
    void stockIsCheckedExactlyOnce() {
        when(inventory.getStock("P1")).thenReturn(10);
        when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(true);

        orderService.placeOrder("C1", "P1", 1, 5.0);

        verify(inventory, times(1)).getStock("P1");
    }
}
```

### What each test proves

| Test | Business rule verified |
|---|---|
| `successfulOrderIsConfirmedAndStockReduced` | Happy path: charge the right amount, then reduce stock |
| `failedPaymentDoesNotReduceStock` | Don't give away stock when payment fails |
| `insufficientStockThrowsAndNeverCharges` | Never charge a customer for something you can't ship |
| `invalidQuantityNeverTouchesDependencies` | Validate input **before** calling anything expensive |
| `repositoryErrorIsPropagated` | Errors from dependencies aren't swallowed |
| `chargesQuantityTimesUnitPrice` | **ArgumentCaptor**: grabs the actual value passed, so you can inspect it |
| `stockIsCheckedExactlyOnce` | No redundant database calls |

### Stubbing vs verifying: when to use which

- **Stub** a method when your code **needs its return value** to continue (`getStock`, `charge`).
- **Verify** a method when **calling it is the behavior you're testing** (`reduceStock`, sending an email, saving a record).
- Avoid verifying things you already stubbed *and* whose effect you already asserted. It makes tests brittle.

### ⚠️ Common pitfalls (read these!)

**1. Mixing matchers and raw values**

```java
// ❌ InvalidUseOfMatchersException
verify(paymentGateway).charge("C1", anyDouble());

// ✅ If you use a matcher for one argument, use matchers for ALL of them
verify(paymentGateway).charge(eq("C1"), anyDouble());
```

**2. Using `any()` for a primitive parameter**

```java
// ❌ any() returns null -> NullPointerException when Java unboxes it to double
when(paymentGateway.charge(anyString(), any())).thenReturn(true);

// ✅ Use the typed matcher
when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(true);
```

**3. `UnnecessaryStubbingException`**

`MockitoExtension` is **strict**: if you stub something your test never uses, the test **fails**. This is a feature, because it catches copy-pasted or outdated setup. Fix it by deleting the unused `when(...)`.

**4. Stubbing with the wrong arguments**

```java
when(inventory.getStock("P1")).thenReturn(10);
orderService.placeOrder("C1", "P2", 1, 5.0);   // asks for P2 -> mock returns 0!
```

Mockito matches arguments exactly. A call with different arguments would normally return the default value (`0` here), which causes confusing failures. With `MockitoExtension`'s strict stubs, Mockito fails the test with a `PotentialStubbingProblem` that points you at the mismatch.

**5. Mocking the class under test**

Never put `@Mock` on `OrderService` itself. You'd be testing a fake! Mock its **dependencies**, and use the **real** class under test.

**6. Over-mocking**

Don't mock simple value objects or data classes like `ShoppingCart` or `String`. Mock things that cross a boundary: databases, HTTP calls, the file system, clocks, payment providers, email.

### ✍️ Try it

1. Write a test showing that when payment fails, `charge` was called **exactly once** with `("C1", 25.0)`.
2. Write a test where stock exactly equals the requested quantity (stock `5`, quantity `5`). Is the order confirmed?
3. Write a test for `quantity = -3`, then verify **neither** mock was touched.
4. Write a test where `paymentGateway.charge(...)` **throws** `new RuntimeException("Gateway timeout")`. Assert the exception propagates **and** `reduceStock` was never called.
5. Use an `ArgumentCaptor<Integer>` to capture the quantity passed to `reduceStock` and assert it's `7`.
6. Add a stub that your test doesn't use, run it, and read the `UnnecessaryStubbingException` message. Then remove the stub.
7. **Question:** Why can we mock `PaymentGateway` so easily? (Hint: what *kind* of Java type is it, and how does `OrderService` receive it?)
8. **Question:** In `successfulOrderIsConfirmedAndStockReduced`, is `verify(paymentGateway).charge("C1", 30.0)` actually necessary? Argue both sides.

---

## Module 7 – pytest vs JUnit (15 min)

### Side-by-side comparison

| Topic | pytest (Python) | JUnit 5 (Java) |
|---|---|---|
| **Test discovery** | Files `test_*.py`, functions `test_*` | Classes `*Test`, methods with `@Test` |
| **Where tests live** | Anywhere (convention: `tests/`) | `src/test/java`, same package as the code |
| **Running** | `pytest` | `mvn test` (or `gradle test`) / IDE |
| **Assertions** | Plain `assert` with rich introspection | `Assertions.assertXxx(...)` methods |
| **Argument order** | `assert actual == expected` | `assertEquals(expected, actual)` |
| **Float compare** | `pytest.approx()` | `assertEquals(exp, act, delta)` |
| **Exceptions** | `with pytest.raises(E, match=...)` | `assertThrows(E.class, () -> ...)` |
| **Multiple checks** | Stops at first failure (plugin: `pytest-check`) | `assertAll(...)` built in |
| **Setup/teardown** | Fixtures (`yield`), injected by name | `@BeforeEach` / `@AfterEach` / `@BeforeAll` / `@AfterAll` |
| **Fixture scopes** | function / class / module / package / session | per test / per class (wider scopes via extensions) |
| **Sharing setup** | `conftest.py` | Base classes or extensions (`@ExtendWith`) |
| **Parameterization** | `@pytest.mark.parametrize` | `@ParameterizedTest` + `@ValueSource` / `@CsvSource` / `@MethodSource` |
| **Labels / filtering** | `@pytest.mark.x` + `-m x` | `@Tag("x")` + `-Dgroups=x` |
| **Skipping** | `skip`, `skipif`, `xfail` | `@Disabled`, assumptions, `@EnabledOnOs`, etc. (no built-in `xfail`) |
| **Grouping** | Classes / modules | `@Nested` classes + `@DisplayName` |
| **Mocking** | `unittest.mock`, `pytest-mock` | Mockito (separate library) |
| **Patching** | `mocker.patch("a.b.c")` can patch almost anything | Usually inject mocks via constructor; static mocking needs `mockStatic` |
| **Extensibility** | Huge plugin ecosystem, hooks | Extension model (`@ExtendWith`), e.g. Mockito, Spring, Selenium |
| **Reports** | Terminal; `--junitxml`, `pytest-html` | Surefire XML/TXT reports. pytest's `--junitxml` produces *JUnit's* XML format, which all CI tools understand. |
| **Verbosity** | Very concise | More ceremony (types, annotations, imports) |
| **Type safety** | Errors appear at runtime | Compiler catches many mistakes before tests run |
| **Typical QE use** | API tests, Python apps, data tests, Playwright/Selenium in Python | Java backends (Spring), Selenium/RestAssured frameworks, Android |

### What transfers directly ✅

- The **AAA pattern** and the idea of *one behavior per test*
- **Independence**: no shared mutable state, and no reliance on test order
- **Fixtures**, which become lifecycle methods
- **Parametrize**, which becomes `@ParameterizedTest`
- **Markers**, which become `@Tag`
- **Mocking concepts**: stub return values, verify calls, match arguments, capture arguments

### What's different ⚠️

- `assertEquals(expected, actual)`: **expected comes first**
- Fixtures are **not injected by name**. They're stored in fields and set up in `@BeforeEach`.
- Exceptions are tested with **lambdas**, not `with` blocks.
- `@BeforeAll` methods must be **`static`**.
- Mocks are usually **injected through constructors**, not patched by module path. This pushes you toward better design (dependency injection).
- **Strict stubbing**: Mockito fails tests that have unused stubs, while Python mocks are permissive.
- The **compiler** is your first test: many errors pytest would find at runtime never get past `javac`.

### ✍️ Reflection questions

1. Rewrite `test_add` (with three parametrized cases) from pytest into JUnit, from memory.
2. Your pytest suite uses a `session`-scoped fixture to start a test server once. What's the closest JUnit option, and what's its limitation?
3. Python's `mocker.patch` can replace *anything*. Mockito works best with injected dependencies. Which approach leads to better-designed production code, and why?
4. Name two things you find **easier** in JUnit and two that are **easier** in pytest.

---

## Cheat Sheet

```java
// ── Imports ──────────────────────────────────────────────
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

// ── Basic test ───────────────────────────────────────────
@Test void name() { assertEquals(expected, actual); }

// ── Assertions ───────────────────────────────────────────
assertEquals(exp, act);          assertEquals(0.3, act, 0.001);
assertTrue(c);  assertFalse(c);  assertNull(x);  assertNotNull(x);
assertThrows(Ex.class, () -> code());
assertDoesNotThrow(() -> code());
assertAll(() -> ..., () -> ...);
assertIterableEquals(list1, list2);
assertTimeout(Duration.ofMillis(100), () -> code());
fail("message");

// ── Lifecycle ────────────────────────────────────────────
@BeforeAll static void once() {}    @AfterAll static void end() {}
@BeforeEach void setUp() {}         @AfterEach void tearDown() {}

// ── Parameterized ────────────────────────────────────────
@ParameterizedTest @ValueSource(ints = {1, 2, 3})
@ParameterizedTest @CsvSource({"1, 2, 3", "4, 5, 9"})
@ParameterizedTest @MethodSource("provider")   // static Stream<Arguments> provider()
@ParameterizedTest @NullAndEmptySource

// ── Organizing ───────────────────────────────────────────
@DisplayName("...")  @Disabled("why")  @Tag("smoke")  @Nested class Ctx {}
assumeTrue(condition);

// ── Mockito ──────────────────────────────────────────────
@ExtendWith(MockitoExtension.class)
@Mock Dependency dep;
@InjectMocks ClassUnderTest sut;
when(dep.method(args)).thenReturn(value);
when(dep.method(args)).thenThrow(new RuntimeException());
verify(dep).method(args);
verify(dep, times(2)).method(args);
verify(dep, never()).method(any());
verifyNoInteractions(dep);
any(), anyString(), anyInt(), anyDouble(), eq(value)
ArgumentCaptor<T> c = ArgumentCaptor.forClass(T.class);
verify(dep).method(c.capture());  c.getValue();
```

```bash
mvn test                                   # all tests
mvn test -Dtest=OrderServiceTest           # one class
mvn test -Dtest=OrderServiceTest#method    # one method
mvn test -Dgroups=smoke                    # by tag
mvn test -DexcludedGroups=slow             # exclude tag
```

---

## Further Reading

- JUnit 5 User Guide: <https://junit.org/junit5/docs/current/user-guide/>
- Mockito documentation: <https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html>
- Maven Surefire and JUnit Platform: <https://maven.apache.org/surefire/maven-surefire-plugin/examples/junit-platform.html>

**🎉 Done! Next step: the homework assignment.**
