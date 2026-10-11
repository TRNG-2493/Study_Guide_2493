# Features and Scenarios

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **feature** and a **scenario** represent and how they relate to user stories and acceptance criteria.
- Decide how to **divide functionality into feature files** and how to name and organize them.
- Write a well-formed **Feature** with a story description.
- Write **scenarios** that each test exactly **one behavior** and are independent, short, and meaningful.
- Choose **good scenario titles** and meaningful, realistic example data.
- Cover the **happy path, negative cases, and edge cases** without writing redundant scenarios.
- Recognize and fix common scenario **anti-patterns** (too long, too technical, dependent on other scenarios, testing multiple things).
- Organize a **feature folder structure** that suits Project 2.
- Review a feature file against a checklist and give specific improvement suggestions.
- Turn a three-amigos conversation about a saucedemo.com feature into a reviewed feature file.

---

## Why This Matters

Writing syntactically correct Gherkin is easy; writing **good** Gherkin is a craft. A badly organized suite of feature files becomes a maintenance burden: 300 scenarios that all repeat the same login steps, with titles like "Test 17", where nobody can tell which behavior is covered or which scenario to update when the product changes.

A well-organized suite, on the other hand, is a **map of the product's behavior**. You can open `shopping-cart.feature` and see exactly what a cart is supposed to do. When a business rule changes, you know which scenario to edit.

**Analogy: a library.** A library with all books piled in one heap has the same content as an organized library, but you cannot find anything. A good library groups books by subject (feature folders), gives each book a clear title (scenario titles), and keeps each book about one topic (one feature per file). Feature files are the shelves of your product's knowledge.

**Where you will use this:**

- **Today**, in the Project 2 pair-programming exercise: each pair writes features and scenarios for saucedemo.com. The ideas in this lesson will be the criteria your reviewer uses.
- **Daily on the job**: you will add scenarios to existing files, fix titles, and decide whether a new behavior belongs in an existing feature or a new one.
- **In code review**: feature files are reviewed like code; a reviewer who knows these rules gives faster, more useful feedback.

Earlier lessons today gave you the grammar of Gherkin and the process of turning stories into acceptance criteria. This lesson is the bridge: how to **shape** those criteria into features and scenarios that will still make sense in a year.

---

## The Concept

### 1. Feature: A Piece of Functionality That Matters to Users

A **feature** is a cohesive capability of the system that provides value to a user. A feature file is the *specification* of that capability. Examples: Login, Product sorting, Shopping cart, Checkout, Password reset, Search.

A feature file begins with:

```gherkin
Feature: Shopping cart
  As a shopper
  I want to manage the products in my cart
  so that I only buy what I really want
```

- **The title** is a short noun phrase naming the capability.
- **The description** captures the **user story** (role, goal, benefit), and optionally business notes, assumptions, or links to tickets. It is the only place where you explain *why* in the feature file.

**Rule of thumb:** one feature file = one user story, or a small group of closely related stories on the same capability. Do **not** mix unrelated functionality in one file ("Login and shipping and reports"). Conversely, do not split one capability into ten files of two scenarios each.

**How do you decide what a feature is?** Use these questions:

1. **Does it have one clear user goal?** "Log in" is one goal; "log in, shop, and pay" is three.
2. **Would the business give it one name?** If the product owner says "the cart", that is a feature; "the stuff on the second page" is not.
3. **Do the scenarios share vocabulary and starting state?** Cart scenarios all talk about items and counts; they belong together.
4. **Could it be assigned to a team or developed independently?** A rough sign of a feature boundary.

**Examples of too big, too small, and just right:**

| Feature file | Verdict | Reason |
|---|---|---|
| `store.feature` with login, cart, checkout and sorting | Too big | Several user goals; 60 scenarios; impossible to navigate |
| `add-to-cart-button-color.feature` | Too small | A detail of the cart, not a capability |
| `shopping-cart.feature` | Just right | One capability, 5-12 scenarios |

**Feature title versus story title.** In Jira the story may be called "SHOP-142 As a shopper I want to remove items". In the file, use the capability name ("Shopping cart") and put the ticket reference or story into the description. Several stories (add, remove, view) can share one feature file as long as they are about the same capability.

### 2. Scenario: One Concrete Example of Behavior

A **scenario** is a single concrete example that illustrates one aspect (usually one rule or acceptance criterion) of the feature. In test terms, it is **one test case**. In BDD terms, it is **one example agreed upon in the conversation**.

```gherkin
Scenario: Adding a product increases the cart count
  Given the shopper has an empty cart
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1
```

**Line-by-line:**

- `Scenario: Adding a product increases the cart count` names the behavior and tells a reader (and a report) what is being demonstrated.
- `Given the shopper has an empty cart` is the context. It tells us that the example *starts* with no items, so the result "1" is unambiguous.
- `When the shopper adds "Sauce Labs Backpack" to the cart` is the single action under test. The quoted text is the data of this example.
- `Then the cart count shows 1` is the observable outcome. If the badge showed 2 (for example because an item was left from a previous test), this step fails, which is precisely why the `Given` is needed.

Properties of a good scenario:

| Property | Meaning |
|---|---|
| **Focused** | Tests exactly one behavior or rule |
| **Independent** | Can run alone, in any order, and sets up its own context |
| **Readable** | Understandable by a business person without explanation |
| **Concrete** | Uses specific example data, not abstractions like "a valid value" |
| **Deterministic** | Gives the same result each time (no dependence on random data or time of day) |
| **Short** | Typically 3-7 steps; more suggests it is doing too much or is too detailed |
| **Meaningful title** | The title states the behavior |

**Analogy: a worked example in a textbook.** A math textbook explains a rule and then shows one fully worked example. Each worked example has given values, a step, and a result, and a good book uses a different example for each variation of the rule. Scenarios are the worked examples of your product: small, concrete, and each illustrating exactly one idea.

**Scenario or Example?** Gherkin accepts `Example:` as a synonym of `Scenario:`. Teams choose one and stick to it. This course uses `Scenario:`.

### 3. From Acceptance Criteria to Scenarios

Take the acceptance criteria from the previous lesson for the sort feature:

1. Products can be sorted by name (A-Z, Z-A) and price (low-high, high-low).
2. The default sort is Name (A to Z).
3. Price (low to high) lists products in ascending order.
4. Price (high to low) lists products in descending order.
5. Changing the sort does not change which products are shown.

Each criterion (or a pair) becomes one scenario:

```gherkin
Feature: Product sorting
  As a shopper
  I want to sort the product list
  so that I can find the products I am interested in quickly

  Scenario: Products are sorted by name by default
    Given the shopper is logged in
    When the shopper opens the products page
    Then the products are listed by name from A to Z

  Scenario: Sort by price from low to high
    Given the shopper is on the products page
    When the shopper sorts the products by "Price (low to high)"
    Then the products are listed from the cheapest to the most expensive

  Scenario: Sort by price from high to low
    Given the shopper is on the products page
    When the shopper sorts the products by "Price (high to low)"
    Then the products are listed from the most expensive to the cheapest

  Scenario: Sorting does not remove products
    Given the shopper is on the products page
    And 6 products are listed
    When the shopper sorts the products by "Name (Z to A)"
    Then 6 products are still listed
```

Observe the mapping: **rule -> scenario**. Many similar scenarios like the two price scenarios could be merged using a `Scenario Outline` (Friday); today we write them separately to learn the basics.

**The mapping table, so you can see the traceability:**

| Acceptance criterion | Scenario that covers it |
|---|---|
| 2. Default sort is Name (A to Z) | "Products are sorted by name by default" |
| 3. Price low to high | "Sort by price from low to high" |
| 4. Price high to low | "Sort by price from high to low" |
| 5. Sorting does not change which products are shown | "Sorting does not remove products" |
| 1. All four sort options exist | Covered indirectly by the sort scenarios; a further scenario could list the options in the dropdown |

If you find a criterion without any scenario, you have a coverage gap. If you find a scenario without any criterion, either a criterion is missing (talk to the product owner) or the scenario is unnecessary.

**A step-by-step method for converting a criterion:**

1. Read the criterion and underline the **condition** (when/if), the **action**, and the **result**.
2. Write the title as "result when condition".
3. Write the `Given` lines that create the condition with specific data.
4. Write one `When` for the action.
5. Write the `Then` lines for the result with exact values or messages.
6. Remove any word a customer would not say.
7. Read it aloud.

### 4. Choosing Good Scenario Titles

A title should tell a reader **what behavior is being verified and under what condition**, without reading the steps.

| Weak title | Better title |
|---|---|
| `Test 1` | `Customer with valid credentials logs in` |
| `Login` | `Locked-out customer is refused at login` |
| `Cart` | `Removing the last item leaves the cart empty` |
| `Negative test` | `Checkout is rejected when the postal code is missing` |
| `Check the sort works` | `Sort by price from low to high` |

When a test fails, the report shows the **title**; a good title lets you understand the failure at a glance, before opening the file.

**A title recipe:** *subject + behavior + condition*. For example: "Locked-out customer" (subject) "is refused" (behavior) "at login" (condition). Another: "Checkout" "is rejected" "when the postal code is missing".

**Titles to avoid:**

- Numbering ("Scenario 4").
- Words about testing instead of behavior ("Verify that...", "Check...", "Test..."). The scenario is an example, not an instruction to a tester.
- Mentions of the UI ("Click login button scenario").
- Very long titles (over about 80 characters); the report truncates them.

### 5. Coverage: Happy Path, Negative Paths, and Edge Cases

For each feature think in three categories:

| Category | Question | Example (login) |
|---|---|---|
| **Happy path** | What is the normal successful behavior? | Valid user logs in |
| **Negative paths** | What should happen when the user or system does something wrong? | Wrong password, empty username, locked-out account |
| **Edge cases / boundaries** | What happens at the limits? | 0 items, maximum quantity, very long names, special characters |

**Do not try to cover everything.** The BDD goal is **key examples** that document the rules, not exhaustive testing. Exhaustive combinations of input values belong in lower-level tests (unit/API), or in data-driven techniques such as outlines (covered Friday). A feature with 5-12 scenarios is typical; if you reach 30, ask whether the feature should be split or the examples reduced.

**A quick way to pick key examples:** for each rule, ask "what is the smallest set of examples such that if all pass, I trust the rule, and if the rule changes, I know exactly which example to edit?" Usually that is one positive example and one or two examples at the boundary or in the failure condition.

**Worked coverage map for checkout on saucedemo.com** (three-stage flow: information, overview, finish):

| Rule | Happy | Negative | Edge |
|---|---|---|---|
| All delivery details are required | Complete details accepted | Missing first name; missing last name; missing postal code | (not needed; each field is a separate rule) |
| Overview shows the item total | Total of two items is the sum | | Single item total |
| Finishing the order shows confirmation | Confirmation displayed, cart emptied | | |
| Cancel returns to the cart | Items still in the cart | | |

From this map you derive about 8 scenarios, each pinning one rule. Notice we did *not* add scenarios for every combination of empty fields (first and last empty, first and postal empty, and so on); the rule "each field is required" is demonstrated by one example per field.

### 6. One Scenario, One Behavior (and Why)

**Bad (two behaviors in one scenario):**

```gherkin
Scenario: Cart works
  Given the shopper is logged in
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1
  When the shopper removes "Sauce Labs Backpack" from the cart
  Then the cart count shows 0
  When the shopper adds "Sauce Labs Bike Light" and "Sauce Labs Onesie"
  Then the cart count shows 2
```

Problems:

- If the second Then fails, you do not know whether adding or removing is broken; the later steps are skipped, so they were never tested.
- The title says nothing precise.
- It is long and hard to maintain.

**Good (split):**

```gherkin
Scenario: Adding a product increases the cart count
  Given the shopper has an empty cart
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart count shows 1

Scenario: Removing the only product empties the cart
  Given the shopper has "Sauce Labs Backpack" in the cart
  When the shopper removes "Sauce Labs Backpack" from the cart
  Then the cart count shows 0

Scenario: Adding two different products
  Given the shopper has an empty cart
  When the shopper adds "Sauce Labs Bike Light" and "Sauce Labs Onesie" to the cart
  Then the cart count shows 2
```

A very useful self-test: **"If this scenario fails, do I know exactly what is broken from the title?"**

**Why many `When`s signal trouble.** A `When` is the *trigger* of the behavior. A scenario with several triggers is really a story of several behaviors chained, like testing a car by driving from London to Paris and checking only whether you arrived: if you did not, you do not know whether the engine, the tyres, or the map failed. When you do need to reach a state that took several actions, do it in `Given` (hidden inside a business-level step), and test only the final action in `When`.

**An exception worth knowing.** A short, natural flow such as "When the shopper checks out with valid details And the shopper confirms the order" has two `When` lines, but they are two halves of one business action (placing an order). That is fine. The test is: could the two lines be described in one sentence a customer would use? ("She placed the order.") If yes, they are one behavior.

### 7. Independence: No Scenario Depends on Another

Each scenario must create its own starting state in the **Given** steps. Never write "this scenario assumes the previous one added the backpack".

Reasons:

- Scenarios may run in any order, or in parallel, or alone (when you re-run just a failing one).
- A failure in one scenario would cascade into false failures in others.

If the setup is long and repeated in every scenario, do **not** copy-paste it; instead hide it behind a business-level step (`Given the shopper has "Sauce Labs Backpack" in the cart`), whose *implementation* in Java may do several UI actions. (The `Background` keyword offers another way to share setup steps and is covered on Friday.)

**What this looks like in your Java framework.** The step `Given the shopper has "Sauce Labs Backpack" in the cart` could be implemented like this (a preview of what you will write in the *Step Definitions* lesson; the classes `LoginPage`, `ProductsPage`, and the shared `TestContext` come from your earlier work this week):

```java
@Given("the shopper has {string} in the cart")
public void theShopperHasInTheCart(String productName) {
    loginPage.loginAs("standard_user", "secret_sauce");   // get to the products page
    productsPage.addToCart(productName);                  // add the product
}
```

Even though this method performs two page-object calls, the feature file shows only one business-level sentence. Because Cucumber starts a **fresh browser state for every scenario** (you will arrange that in the setup lesson, so each scenario gets a new `WebDriver` and a clean session), the cart really does start empty each time, and independence is guaranteed.

**Spotting dependency.** Ask for every `Given`: "Where does this state come from?" If the honest answer is "from a previous scenario" or "from data someone entered by hand last week", the scenario is dependent.

### 8. The Right Level of Detail

Aim for scenarios that read like **business rules**, not UI scripts, as discussed earlier. Questions to ask when writing each step:

- *Would the product owner say this sentence naturally?* If it contains element ids, URLs, wait times, or "click the third button", it is too detailed.
- *Is any information that matters for this behavior missing?* If the rule depends on the quantity, the quantity should be visible in the scenario.

Compare:

```gherkin
# Too much detail
When the shopper clicks "Add to cart" next to the first product
And the shopper clicks the cart icon in the top right corner
And the shopper clicks "Checkout"
And the shopper types "Ada" in the first name field
...

# Right level
When the shopper checks out with the shipping details:
  | first name | last name | postal code |
  | Ada        | Lovelace  | 10001       |
```

And the opposite problem, **too vague**:

```gherkin
Given a user
When they do stuff
Then it works
```

**A scale of abstraction.** Think of three levels, from lowest to highest:

| Level | Example step | Verdict |
|---|---|---|
| 1. Mechanics | `When I click the element with id "checkout"` | Too low: UI detail |
| 2. Business action | `When the shopper checks out with the shipping details:` | Right level |
| 3. Whole journey | `When the shopper buys a product` | Often too high: hides data that matters |

The right level is the **lowest level at which the business still recognizes the behavior**, and no lower. If the rule is about the postal code, the postal code must appear; if the rule is about the total, the product prices must appear; everything else can be hidden.

**Link to page objects.** This is the same separation you used on Wednesday: page objects hide *how* to click; step definitions hide *which page objects to call in what order*; the feature file hides both. A step at business level is typically implemented by one or two page-object method calls.

### 9. Choosing Example Data

- Use **realistic, meaningful values** that illustrate the rule: `"standard_user"`, `"locked_out_user"` tell a story; `"abc"`, `"test123"` do not.
- Show only the data that **matters to the behavior**. If the discount depends on order total, show the total; do not list the customer's phone number.
- Keep **sensitive data** out of feature files (real passwords, personal data). Demo passwords of public practice sites are acceptable for this course; for real projects, steps should refer to *roles* ("a registered customer") and the credentials live in configuration or a secrets store.

**Example data from saucedemo.com that tells a story:**

| Value | Story it tells |
|---|---|
| `standard_user` | A normal customer; the happy path |
| `locked_out_user` | A blocked customer; the refusal rule |
| `problem_user` | A customer whose experience has known problems (useful for exploring defects) |
| `performance_glitch_user` | A customer who experiences delays (a reminder to use proper waits, as you learned earlier this week) |
| `Sauce Labs Backpack` (29.99) | A named product with a known price, so totals can be computed |
| `Sauce Labs Bike Light` (9.99) | A second product, so sums are interesting |

Using these names in scenarios makes them immediately understandable to anyone who has looked at the site.

**Data that is deterministic.** Avoid values that change with time ("today's date", "a random user") in the feature text. If the behavior depends on a date, state the relationship explicitly ("a booking for a date 3 days from now") and let the step definition calculate it.

### 10. Naming and Organizing Feature Files

**File names:** lowercase, hyphen-separated, noun phrase: `login.feature`, `product-sorting.feature`, `shopping-cart.feature`, `checkout.feature`.

**Folder structure** (inside `src/test/resources`):

```
src/test/resources/
 +-- features/
      +-- authentication/
      |     +-- login.feature
      |     +-- logout.feature
      +-- catalog/
      |     +-- product-sorting.feature
      |     +-- product-details.feature
      +-- ordering/
            +-- shopping-cart.feature
            +-- checkout.feature
```

Group by **business domain**, not by technical layer or by sprint. Cucumber can run the entire `features` folder, a subfolder, or a single file.

**A parallel structure on the Java side.** It helps to mirror the domain split in your step-definition packages, so that finding the code for a feature is easy:

```
src/test/java/
 +-- com/yourname/project2/
      +-- pages/            <- page objects (Wednesday)
      +-- steps/
      |     +-- LoginSteps.java
      |     +-- CartSteps.java
      |     +-- CheckoutSteps.java
      +-- support/          <- shared TestContext, driver factory
```

You do not need a step class per feature file, but grouping by domain keeps things findable. The step-definition and setup lessons explain how Cucumber discovers these classes.

**Why not group by sprint or by test type?** "sprint-12" means nothing after a year; "smoke" or "regression" are *purposes*, and you will handle them with tags on Friday rather than with folders.

### 11. Common Anti-Patterns

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **The script** | Steps like "click", "type", "wait 5 seconds", XPath in text | Rewrite declaratively in business language |
| **The marathon** | A scenario with 20+ steps and several Whens | Split into focused scenarios |
| **Dependent scenarios** | Scenario B assumes A has run | Give B its own Given steps |
| **Copy-paste explosion** | 15 near-identical scenarios that differ by one value | Reduce to key examples; use outlines (Friday) |
| **Vague titles** | "Test 1", "Happy path" | State the behavior |
| **Assertion overload** | Then step with 8 And-checks of unrelated things | One outcome per scenario |
| **Hidden state** | Result depends on data that is not shown in the scenario | Make the relevant data explicit or documented |
| **Testing the UI framework** | "Then the button is blue" for business features | Test behavior; use visual tools for appearance |
| **Technical jargon** | "HTTP 200", "NullPointerException" in scenarios the business reads | Describe the user-visible outcome |

#### 11.1 A before-and-after rewrite

**Before** (script, marathon, vague title, and technical detail all at once):

```gherkin
Scenario: Test 7
  Given I open "https://www.saucedemo.com"
  And I type "standard_user" into "#user-name"
  And I type "secret_sauce" into "#password"
  And I click "#login-button"
  And I click "#add-to-cart-sauce-labs-backpack"
  And I click ".shopping_cart_link"
  And I click "#checkout"
  And I type "" into "#first-name"
  And I type "Silva" into "#last-name"
  And I type "12345" into "#postal-code"
  When I click "#continue"
  Then ".error-message-container" is visible
  And ".error-message-container" has text "Error: First Name is required"
  And the URL is "https://www.saucedemo.com/checkout-step-one.html"
  And the page title is "Swag Labs"
```

Problems: title says nothing; every step is mechanics; locators and URLs will break with UI changes; the final two `And` checks are unrelated to the rule.

**After:**

```gherkin
Scenario: Checkout is refused when the first name is missing
  Given the shopper has "Sauce Labs Backpack" in the cart
  When the shopper checks out without a first name but with last name "Silva" and postal code "12345"
  Then the shopper sees the error "Error: First Name is required"
  And the shopper is still on the delivery details page
```

What changed: the title states the rule and condition; the first nine mechanical steps collapsed into one `Given`; the action is one business sentence including only the relevant data; the outcome states what the shopper sees (message plus the fact that checkout did not move on). The locators moved into page objects.

#### 11.2 Quick diagnosis table

| If you see this in a review | Say this |
|---|---|
| A step contains `#`, `//`, `.` selectors | "Move the locator into the page object; describe the action." |
| More than one `When` that cannot be one sentence | "Split this into two scenarios." |
| `Given` that refers to "the previous scenario" | "Make this scenario create its own state." |
| Title starts with "Test" or "Check" | "Rename it to state the behavior." |
| A `Then` that checks three unrelated things | "Keep the check that matches the title; others belong in their own scenarios." |

### 12. A Review Checklist

Before committing a feature file, ask:

1. Does the **title** name a capability, and does the **description** state the story?
2. Does each scenario test **one** behavior, and is its **title** meaningful?
3. Are scenarios **independent** and **deterministic**?
4. Are steps in **business language**, with no locators or implementation details?
5. Is the **step wording consistent** with existing steps (to maximize reuse)?
6. Are **happy path, key negative cases, and key edge cases** covered, without duplicates?
7. Would a product owner **understand and confirm** it?

**Using the checklist in a pair.** Take turns: one person reads each scenario aloud as if they were the product owner, the other follows the checklist. Stop at every place where the reader hesitates; hesitation means unclear wording.

### 13. A Full Walk from Conversation to Feature File (Project 2 Style)

This section demonstrates what you will do in today's pair-programming activity. The scenario is a **booking** domain (so you see the pattern outside the shop) followed by guidance for saucedemo.com.

**The story:** As a traveller, I want to cancel a hotel booking, so that I am not charged for a stay I will not take.

**Three-amigos output (rules and examples):**

| Rule | Examples |
|---|---|
| R1. Cancelling at least 48 hours before check-in is free | Check-in in 5 days, cancel now: refund 100%. Check-in in exactly 2 days, cancel now: refund 100% (boundary). |
| R2. Cancelling less than 48 hours before check-in costs the first night | Check-in tomorrow, rate 120.00 per night, 3 nights booked: charge 120.00, refund 240.00. |
| R3. A cancelled booking cannot be cancelled again | Cancel a cancelled booking: message "Booking is already cancelled". |
| Question | Which time zone defines "48 hours"? (Open: product owner to answer.) |

**Step 1: Decide the feature boundary.** Everything here is about cancelling bookings. One feature file: `booking-cancellation.feature`. The "which time zone" question is open, so we exclude any scenario that depends on it and note it in the description.

**Step 2: Write the file.**

```gherkin
Feature: Booking cancellation
  As a traveller
  I want to cancel a hotel booking
  so that I am not charged for a stay I will not take

  Open question: the time zone that defines the 48-hour limit is being confirmed.

  Scenario: Cancelling well before check-in is free
    Given the traveller has a booking that starts in 5 days
    When the traveller cancels the booking
    Then the traveller is refunded the full amount

  Scenario: Cancelling exactly 48 hours before check-in is still free
    Given the traveller has a booking that starts in 2 days
    When the traveller cancels the booking
    Then the traveller is refunded the full amount

  Scenario: Cancelling the day before check-in costs the first night
    Given the traveller has a booking of 3 nights at 120.00 per night that starts tomorrow
    When the traveller cancels the booking
    Then the traveller is charged 120.00
    And the traveller is refunded 240.00

  Scenario: A cancelled booking cannot be cancelled again
    Given the traveller has a cancelled booking
    When the traveller cancels the booking again
    Then the traveller sees the message "Booking is already cancelled"
```

**Step 3: Review with the checklist.**

- Title names the capability, description states the story, with the open question noted. Yes.
- One behavior per scenario. Yes.
- Independent: each scenario creates its own booking in `Given`. Yes.
- Business language: no ids or URLs. Yes.
- Deterministic: "in 5 days" and "tomorrow" are relative to the test run time, which the step definition will compute. Yes.
- Boundary covered (exactly 48 hours). Yes.

**Step 4: Apply the same process to your Project 2 feature.** For saucedemo.com, do the following in your pair:

1. Pick one feature (login, product sorting, cart, or checkout).
2. Hold a 15-20 minute three-amigos conversation; record rules, examples, questions.
3. Verify examples against the real site; correct any wrong assumption.
4. Decide the feature file name and folder.
5. Write the description (story) and one scenario per key example.
6. Review with the checklist and swap with another pair.
7. Collect the distinct step texts; those become your step definitions in the next lesson.

---

## Complete Example: Shopping Cart Feature

```gherkin
Feature: Shopping cart
  As a shopper
  I want to manage the products in my cart
  so that I only buy the items I really want

  Scenario: A new customer starts with an empty cart
    Given the shopper is logged in
    Then the cart is empty

  Scenario: Adding a product increases the cart count
    Given the shopper is logged in
    When the shopper adds "Sauce Labs Backpack" to the cart
    Then the cart count shows 1
    And the cart contains "Sauce Labs Backpack"

  Scenario: Adding two different products
    Given the shopper is logged in
    When the shopper adds the following products to the cart:
      | product               |
      | Sauce Labs Bike Light |
      | Sauce Labs Onesie     |
    Then the cart count shows 2

  Scenario: Removing the only product empties the cart
    Given the shopper is logged in
    And the shopper has "Sauce Labs Backpack" in the cart
    When the shopper removes "Sauce Labs Backpack" from the cart
    Then the cart is empty

  Scenario: The cart is kept when the shopper continues shopping
    Given the shopper is logged in
    And the shopper has "Sauce Labs Backpack" in the cart
    When the shopper opens the cart and continues shopping
    Then the cart count still shows 1
```

Notice that every scenario repeats `Given the shopper is logged in`. This repetition is acceptable now; on Friday you will learn how `Background` removes it elegantly. Also note how the wording `the cart count shows 1` is used consistently, so one step definition (with a number parameter) can serve several scenarios.

**Line-by-line reading of two of the scenarios:**

*Scenario "Adding a product increases the cart count":*

- `Given the shopper is logged in`: context; the step definition will use the login page object with the demo user.
- `When the shopper adds "Sauce Labs Backpack" to the cart`: the single action; the quoted product name is passed to the Java method as a `String`, which the `ProductsPage` page object uses to find the correct "Add to cart" button.
- `Then the cart count shows 1`: the number is passed as an `int`; the step compares it with the badge text on the cart icon.
- `And the cart contains "Sauce Labs Backpack"`: a second outcome; it ensures not only the count but also the identity of the item.

*Scenario "Adding two different products":*

- The data table lists the two products. The step method receives a `DataTable`, loops over the rows, and calls `addToCart` for each.
- The table has one column; its header `product` names it. The `Then` checks the combined count.

**Which step texts are reused?** `the shopper is logged in` (5 times), `the shopper has {string} in the cart` (2 times), `the cart count shows {int}` (2 times), and `the cart is empty` (2 times). Five scenarios are served by about nine step definitions. This reuse is why consistent phrasing matters.

---

## Hands-On Guided Lab: Design a Feature File from a Conversation

**Goal:** Practice moving from rules and examples to a clean feature file, then review it.

**Time:** 50 minutes. **Prerequisites:** Browser, text editor, partner (you can do it alone, but play both roles).

**Steps:**

1. **Choose the capability.** "Logout" on saucedemo.com. Log in as `standard_user` / `secret_sauce`, open the menu at the top left, and find "Logout".
2. **Explore and note observations.** Click Logout. What page do you land on? Are the username and password fields empty? Press the browser Back button. What happens? Write your findings down.
3. **Write the story.**
   ```
   As a logged-in shopper,
   I want to log out,
   so that nobody else can use my account on a shared computer.
   ```
4. **List rules and examples** (three amigos in miniature):

   | Rule | Example |
   |---|---|
   | After logout, the shopper is on the login page | Log in, log out: login page shown |
   | After logout, the login form is empty | Fields are empty |
   | After logout, protected pages are not accessible | Open the products page URL directly: redirected to login with an error message (verify what the site does) |
5. **Decide the file name and folder:** `src/test/resources/features/authentication/logout.feature`.
6. **Write the feature file.**
   ```gherkin
   Feature: Logout
     As a logged-in shopper
     I want to log out
     so that nobody else can use my account on a shared computer

     Scenario: Logging out returns the shopper to the login page
       Given the shopper is logged in
       When the shopper logs out
       Then the shopper sees the login page

     Scenario: The login form is empty after logging out
       Given the shopper is logged in
       When the shopper logs out
       Then the login form has no username and no password entered

     Scenario: The products page cannot be opened after logging out
       Given the shopper has logged out
       When the shopper tries to open the products page directly
       Then the shopper sees the login page
       And the shopper sees the error "Epic sadface: You can only access '/inventory.html' when you are logged in."
   ```
   (On saucedemo.com opening the inventory page directly without logging in redirects to the login page and shows an error about access. Check the exact text in your browser and adjust the scenario if it differs.)
7. **Review with the checklist** from Section 12. Write a tick or a fix beside each of the seven questions.
8. **Count distinct step texts.** You should find about six: `the shopper is logged in`, `the shopper logs out`, `the shopper sees the login page`, `the login form has no username and no password entered`, `the shopper has logged out`, `the shopper tries to open the products page directly`, and the error message step. Note which can reuse steps from your login feature (for example "sees the login page").
9. **Swap** with another pair and let them review. Collect two suggestions.

**Expected output:** a `logout.feature` file in the correct folder with a three-scenario feature, a completed checklist, and a list of distinct step texts to implement in the next lesson. When you later run Cucumber without step definitions, you should see three scenarios reported as *undefined*, with snippets for each distinct step.

---

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| Scenario passes alone but fails after another scenario | Hidden dependency or shared state | Give the scenario its own `Given` setup; check that the browser session is fresh per scenario |
| Report titles are meaningless | Titles like "Test 3" | Rename to state behavior |
| 40 scenarios in one file | Feature too big | Split by capability or rule; remove duplicates |
| Scenarios need constant editing after UI changes | Locators or mechanics in the feature | Push details into page objects and step definitions |
| The same step has five slightly different wordings | No agreed vocabulary | Agree on terms (shopper vs. customer vs. user); update files |
| The product owner will not read the file | Too technical or too long | Show the shortest scenario; use business words; ask what is missing |
| You cannot decide whether to split a feature | Unclear boundary | Apply the four boundary questions of Section 1 |

---

## Common Mistakes

1. **Writing one giant feature for the whole application.** Split by capability.
2. **Treating each click as a step.** Describe business actions.
3. **Putting several behaviors in one scenario.** Split; one title, one behavior.
4. **Using "Test" or numbers as titles.** Use subject, behavior, and condition.
5. **Chaining scenarios.** Always create the state in `Given`.
6. **Over-testing.** Writing every combination as a scenario; pick key examples.
7. **Leaving out the description.** The story and its "so that" explain why the file exists.
8. **Changing wording casually.** "Shopper", "customer", and "user" for the same role create duplicate step definitions and confusion.
9. **Using future-day features too early.** Do not copy `Scenario Outline`, `Background`, or tags from the internet and paste them into today's files; they come on Friday.

---

## Practice Exercises

1. **Split the marathon.** Split this scenario into focused scenarios with meaningful titles:

   ```gherkin
   Scenario: Checkout
     Given I am on the login page
     When I log in
     And I add a backpack
     And I go to the cart
     Then I see the backpack
     When I click checkout
     And I fill in the form with first name "" and everything else valid
     Then I see an error
     When I fill in the form correctly
     Then I see the overview
     When I click finish
     Then I see "Thank you for your order!"
   ```
2. **Titles.** Rewrite these titles so they state behavior: "Login test", "Negative scenario 2", "Cart", "Test sort".
3. **From criteria to scenarios.** Take the story "As a shopper, I want to check out with my shipping details, so that I can receive my order". Write acceptance criteria and then **five** scenarios (one happy path, three negative cases, one edge case).
4. **Level of detail.** Rewrite the following scenario at the right level:

   ```gherkin
   Given I navigate to https://www.saucedemo.com
   When I type "problem_user" in id=user-name
   And I type "secret_sauce" in id=password
   And I click id=login-button
   And I wait 3 seconds
   Then css "[data-test='title']" has text "Products"
   ```
5. **Independence check.** Find the dependency in: *Scenario A: add item to cart. Scenario B: Given the cart contains the item from the previous scenario, when the shopper removes it, then the cart is empty.* Fix B.
6. **Organize.** For Project 2, list five feature files with names, and place them in a folder structure by business domain.
7. **Peer review.** Using the review checklist, review a classmate's feature file and give three specific suggestions.
8. **Data choice.** For the rule "orders of $100 or more get free shipping", choose example totals that document the **boundary** (hint: $99.99, $100.00, $100.01) and write three scenarios.
9. **Feature boundary.** A teammate proposes one file `shop.feature` containing login, sorting, cart, and checkout scenarios (42 scenarios). Explain what is wrong and propose a split with file names.
10. **Assertion overload.** Fix this scenario so that it tests one behavior:
    ```gherkin
    Scenario: Login works
      Given the customer is on the login page
      When the customer logs in with username "standard_user" and password "secret_sauce"
      Then the customer sees the products page
      And the page title is "Swag Labs"
      And the cart is empty
      And 6 products are listed
      And the footer shows the social media links
    ```
11. **Coverage map.** Create a coverage map (rules by happy path, negative, edge) for the saucedemo.com login feature, then decide which cells deserve a scenario.
12. **Pair activity rehearsal.** In your pair, pick one Project 2 feature, run the 7-step process of Section 13 (step 4), and produce a reviewed feature file with a description, a name, a folder, and 5-8 scenarios. Keep the list of distinct step texts.

---

## Solutions and Hints

**1. Split the marathon.** Sample result:

```gherkin
Scenario: Added product is shown in the cart
  Given the shopper is logged in
  When the shopper adds "Sauce Labs Backpack" to the cart
  Then the cart contains "Sauce Labs Backpack"

Scenario: Checkout is refused when the first name is missing
  Given the shopper has "Sauce Labs Backpack" in the cart
  When the shopper checks out without a first name
  Then the shopper sees the error "Error: First Name is required"

Scenario: Checkout with all details shows the overview
  Given the shopper has "Sauce Labs Backpack" in the cart
  When the shopper checks out with valid delivery details
  Then the shopper sees the order overview

Scenario: Finishing the order shows a confirmation
  Given the shopper has reached the order overview with "Sauce Labs Backpack"
  When the shopper confirms the order
  Then the shopper sees the message "Thank you for your order!"
```

Hint: the original had five `Then`s and four `When`s; each pair became its own scenario. Note that the original also mixed login mechanics into the checkout, now hidden behind `the shopper is logged in`.

**2. Titles.** "Customer with valid credentials logs in"; "Checkout is refused when the postal code is missing" (or whatever the scenario does); "Removing the last item empties the cart"; "Sort by price from low to high". Any title that follows subject, behavior, and condition is acceptable.

**3. From criteria to scenarios.** Sample criteria: all three details required; each empty field shows its message; valid details lead to the overview; the overview shows the item total. Scenarios: happy path (valid details lead to the overview); negatives (missing first name, missing last name, missing postal code); edge (a very long first name, or a single-character postal code, depending on the rule agreed; if the rule is not defined, write it as an open question rather than inventing it).

**4. Level of detail.**

```gherkin
Scenario: Problem user can log in and sees the product list
  Given the customer is on the login page
  When the customer logs in with username "problem_user" and password "secret_sauce"
  Then the customer sees the products page
```

The URL, locators, and the three-second wait are gone (waits belong in the page object, using explicit waits as learned earlier this week).

**5. Independence check.** B depends on A having left the item in the cart. Fix: `Given the shopper has "Sauce Labs Backpack" in the cart`, `When the shopper removes "Sauce Labs Backpack" from the cart`, `Then the cart is empty`.

**6. Organize.** Sample: `authentication/login.feature`, `authentication/logout.feature`, `catalog/product-sorting.feature`, `ordering/shopping-cart.feature`, `ordering/checkout.feature`.

**7. Peer review.** Check each point of the seven-question checklist and quote the exact line you suggest changing.

**8. Data choice.**

```gherkin
Scenario: An order of 99.99 pays for shipping
  Given the shopper's order total is 99.99
  When the shopper views the order overview
  Then shipping is charged

Scenario: An order of exactly 100.00 ships free
  Given the shopper's order total is 100.00
  When the shopper views the order overview
  Then shipping is free

Scenario: An order above 100.00 ships free
  Given the shopper's order total is 100.01
  When the shopper views the order overview
  Then shipping is free
```

(The third scenario is optional; the two on either side of the boundary carry most of the value.)

**9. Feature boundary.** Problem: several unrelated user goals; 42 scenarios are hard to navigate; changes cause merge conflicts; reports are unclear. Split: `authentication/login.feature`, `catalog/product-sorting.feature`, `ordering/shopping-cart.feature`, `ordering/checkout.feature`.

**10. Assertion overload.** Keep the check that matches the title ("sees the products page"). The page title, empty cart, count, and footer are separate concerns; each might deserve its own scenario or none at all (a footer is rarely a business rule).

```gherkin
Scenario: Customer with valid credentials reaches the products page
  Given the customer is on the login page
  When the customer logs in with username "standard_user" and password "secret_sauce"
  Then the customer sees the products page
```

**11. Coverage map.** Rules: valid credentials accepted (happy); wrong password refused (negative); locked-out user refused (negative); each field required (negative, two examples: empty username, empty password); empty both (edge, optional). Probably 5-6 scenarios.

**12. Pair rehearsal.** Check against the review checklist and verify every example against the real site.

---

## Self-Check Questions

1. **What does a feature file represent?** One cohesive, user-valued capability, with its story in the description.
2. **What does a scenario represent?** One concrete example of one behavior or rule; one test case.
3. **Why should each scenario create its own starting state?** So scenarios can run alone, in any order, or in parallel, and failures do not cascade.
4. **Name the three coverage categories.** Happy path, negative paths, edge cases.
5. **Why is "Test 7" a bad title?** It says nothing about the behavior, so a failing report cannot be understood without opening the file.
6. **How do you decide the right level of detail for a step?** Use the lowest level at which the business still recognizes the behavior, including only the data that matters to the rule.
7. **What is wrong with a scenario that has several unrelated `When` lines?** It covers several behaviors, so a failure does not tell you which behavior is broken and later steps are skipped.
8. **How should feature files be grouped into folders?** By business domain (authentication, catalog, ordering), not by sprint or technical layer.

---

## Summary

- A **feature** is a cohesive user-valued capability, specified in one `.feature` file; its **description** holds the user story. A **scenario** is one concrete example of one behavior or rule.
- Derive scenarios from **acceptance criteria**: typically one scenario per rule or key example, and check traceability both ways.
- Give scenarios **meaningful titles** (subject, behavior, condition); make them **focused, independent, deterministic, short, and written in business language**.
- Cover the **happy path, key negatives, and edge cases**, but only the **key examples**: avoid exhaustive combinations.
- **One scenario = one behavior**; avoid marathons, dependent scenarios, vague titles, and UI-script style.
- Choose the right level of detail: business actions, with only the data that matters; push mechanics into step definitions and page objects.
- Name files by capability (`shopping-cart.feature`) and group them in folders by **business domain**.
- Review with the seven-question checklist, ideally in pairs.
- Repeated setup (like logging in) and repeated similar scenarios are handled on Friday by `Background` and `Scenario Outline`.
- For Project 2: conversation, then rules and examples, then a feature file per capability, then step definitions.

---

## Additional Resources

- Cucumber documentation, *Writing better Gherkin*: https://cucumber.io/docs/bdd/better-gherkin/
- Cucumber documentation, *Gherkin reference: Feature and Scenario*: https://cucumber.io/docs/gherkin/reference/
- Cucumber blog, *Behaviour-Driven Development: Common mistakes*: https://cucumber.io/docs/bdd/
- Swag Labs practice site used in Project 2: https://www.saucedemo.com
