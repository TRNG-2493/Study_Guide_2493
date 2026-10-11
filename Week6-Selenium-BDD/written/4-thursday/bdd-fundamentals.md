# BDD Fundamentals

## Learning Objectives

By the end of this lesson you will be able to:

- Define **Behavior-Driven Development (BDD)** in your own words and explain the problem it was invented to solve.
- Explain how BDD relates to (and differs from) TDD and traditional test automation such as the Selenium scripts you wrote on Monday to Wednesday.
- Describe the **Three Amigos** (Business, Development, Testing) and explain why conversation is the heart of BDD.
- Run a small **example-mapping** session using the four card types (story, rules, examples, questions).
- Explain the BDD cycle: **Discovery, Formulation, Automation**, and what each phase produces.
- Describe **living documentation** and why executable specifications stay accurate.
- Explain the role of **Cucumber** and **Gherkin** in the BDD toolchain and see how today's topics fit together with your page objects.
- Recognize common myths and mistakes about BDD (for example, "BDD is just testing with Cucumber").
- Decide when BDD is a good fit and when it is not.
- Run a first, tiny BDD workshop on paper for a saucedemo.com feature as preparation for the Project 2 pair-programming activity.

---

## Why This Matters

Software projects rarely fail because developers cannot write code. They fail because **people misunderstand each other**. A product owner says, "Customers should be able to reset their password." The developer builds an email link that expires after 24 hours. The tester checks that the email arrives. Later the business realizes they also needed the link to expire after one use, and to lock the account after five failed resets. Everyone did their job; nobody built the right thing.

Think of the children's game "telephone" (also called "Chinese whispers"). A message is whispered from one person to the next, and by the time it reaches the end of the line it has changed. A traditional project is a game of telephone with four or five players: the customer tells the business analyst, who writes a document, which the developer reads and interprets, which the tester reads and interprets differently. Every hand-off is an opportunity to distort the message.

The cost of such misunderstandings grows the later they are found. Fixing a requirement misunderstanding in a 20-minute meeting costs minutes; fixing it after release can cost weeks of rework and lost customer trust. Studies of software projects consistently find that a large share of defects originate in requirements, not in coding mistakes. A bug in the requirement is the most expensive kind of bug, because the team builds, tests, and ships it with confidence.

**BDD** is a way of working that attacks this problem at its root. It gets business people, developers, and testers to agree on the expected behavior **before** code is written, records that agreement in a precise, plain-language form, and then turns the same text into **automated tests**. Instead of a game of telephone, everyone is in the same room (or the same call) looking at the same examples.

This week's **Epic** takes you from Selenium WebDriver and the Page Object Model (Monday to Wednesday) to BDD with Cucumber (today and tomorrow), and into **Project 2: Test Automation Framework**. Today's lessons build the BDD layer on top of the page objects you wrote earlier this week: Gherkin scenarios will call step definitions, which call your page objects, which call Selenium. Understanding the *why* of BDD first will keep you from treating Cucumber as "just another syntax".

**Where you will use this:**

- **Today**: in the pair-programming three-amigos activity you will hold a mini discovery session, write stories and scenarios for a Project 2 feature (for example, login or checkout on saucedemo.com), and then implement step definitions.
- **In the job**: most professional QA and SDET teams working in Agile settings use some form of example-based specification. Job descriptions for "AI enabled Test Automation Engineer" and "SDET" roles routinely list Cucumber, Gherkin, and BDD.
- **In your portfolio**: Project 2 is much more convincing to an employer if it shows readable feature files, not only Selenium code.

---

## The Concept

### 1. What Is BDD?

**Behavior-Driven Development (BDD)** is a collaborative software development approach in which teams:

1. **Discuss** concrete examples of how the system should behave,
2. **Document** those examples in a structured, plain-language format everyone can read, and
3. **Automate** the examples as tests that verify the system really behaves that way.

Let us unpack the key words in that definition.

- **Collaborative**: more than one role takes part. The work is not done by a tester alone in a corner.
- **Concrete examples**: not "the system should handle invalid input" (vague), but "when the user enters a quantity of -1, the system shows the message 'Quantity must be at least 1'" (specific, checkable).
- **Structured, plain-language format**: sentences that follow a few simple patterns, so humans can read them and tools can parse them. That format is **Gherkin** (next lesson).
- **Automate**: the same text that the humans agreed on is executed by a tool (Cucumber), so the specification cannot silently drift away from reality.

Dan North introduced the term in the mid-2000s while looking for a better way to teach TDD. He noticed that people struggled with the word "test" and with questions such as "What should I test?" He reframed the question as "What should the system *do*?", that is, its **behavior**. A behavior is a thing the system does that someone cares about: "a customer can add an item to the cart", "a locked-out user is refused entry".

> **BDD is a conversation first, a documentation format second, and an automation tool third.**

The tools (Cucumber, Gherkin) are the least important part. A team that uses Cucumber but never talks to the business is not doing BDD; a team that holds example-mapping workshops and writes plain-text scenarios without any tool is already getting most of the benefit.

**An analogy: the recipe card.** Imagine you ask a friend to cook your grandmother's lasagna. If you say "make lasagna", you get a lasagna, but probably not hers. If you say "layer the noodles, then the sauce, then the ricotta, and bake at 180 degrees for 45 minutes until the top is golden", the friend can succeed. Even better, you both taste the result and compare it with the card. BDD scenarios are the recipe card plus the taste test: a precise description of what "right" looks like, and a way to check it.

### 2. The Problem BDD Solves

Compare how different roles typically communicate:

| Role | Their natural language |
|---|---|
| Business analyst / product owner | Business terms: "A returning customer gets free shipping over $50" |
| Developer | Code and design: classes, methods, APIs |
| Tester | Test cases, steps, expected results |

Each group writes in its own dialect, in its own tool (requirements document, source code, test management tool). Details get lost in translation, and the three artifacts drift apart over time. BDD introduces a **shared language**, sometimes called a **ubiquitous language**, used in conversations, in specifications, in tests, and even in code names.

Let us see the problem in action with a short story. The requirement reads:

> "The system shall give free shipping on large orders."

Here is what three people might understand:

| Person | Their interpretation |
|---|---|
| Product owner | Orders of $50 or more get free shipping for every customer |
| Developer | Orders over $50 (strictly greater than) get free shipping; implements `total > 50` |
| Tester | Orders of $100 or more, since "large" sounds big; tests with a $120 order and everything passes |

The tester's test passes, the developer's code works, and the product owner is unhappy because an order of exactly $50.00 is charged shipping. Nobody lied, nobody was careless. The sentence was ambiguous, and each person filled the gap with an assumption.

Now see what a **concrete example** does to that sentence:

```gherkin
Scenario: Order of exactly 50 dollars qualifies for free shipping
  Given the customer's basket total is 50.00 dollars
  When the customer goes to checkout
  Then the shipping cost is 0.00 dollars
```

(We will explain this syntax properly in the Gherkin lesson. Right now only observe how specific it is.) The example forces the team to decide, at the boundary, whether 50.00 qualifies. The ambiguity is gone. This is why BDD insists on examples: **examples expose assumptions**.

### 3. BDD vs. TDD vs. Traditional Automation

| | Traditional test automation | TDD (Test-Driven Development) | BDD |
|---|---|---|---|
| Who writes it | Testers | Developers | Business + developers + testers together |
| Language | Code (Selenium scripts) | Code (unit tests) | Plain-language examples (Gherkin) backed by code |
| Level | Usually UI/end-to-end | Unit/class level | Behavior of a feature; can be UI, API, or service level |
| Timing | Often after development | Before the code (red-green-refactor) | Before development (discovery), automated alongside it |
| Main goal | Find defects | Drive design of small units | Shared understanding and living documentation |
| Readable by business? | No | No | **Yes** |

BDD **extends** TDD thinking outward: "write the example first" applies to the whole feature, not just a method. They are complementary: a team can use BDD for feature-level acceptance and TDD for unit-level design.

**Red-green-refactor in one paragraph.** In TDD a developer writes a small unit test that fails (red), writes just enough code to make it pass (green), then cleans up the code (refactor). BDD borrows the same rhythm at feature level: a scenario is written first and fails because the feature does not exist yet; the team builds the feature until the scenario passes; then they tidy up.

**A concrete comparison.** The same behavior, "a locked-out user cannot log in", expressed three ways:

Traditional Selenium script (what you wrote Monday to Wednesday):

```java
@Test
void lockedOutUserSeesError() {
    driver.get("https://www.saucedemo.com");
    driver.findElement(By.id("user-name")).sendKeys("locked_out_user");
    driver.findElement(By.id("password")).sendKeys("secret_sauce");
    driver.findElement(By.id("login-button")).click();
    String error = driver.findElement(By.cssSelector("[data-test='error']")).getText();
    Assertions.assertTrue(error.contains("locked out"));
}
```

Unit-level TDD test (a developer testing a single class, no browser):

```java
@Test
void rejectsLockedAccount() {
    AuthService service = new AuthService(userRepositoryWithLockedUser());
    assertThrows(AccountLockedException.class,
        () -> service.login("locked_out_user", "secret_sauce"));
}
```

BDD scenario (readable by everyone):

```gherkin
Scenario: Locked-out user cannot log in
  Given the customer is on the login page
  When the customer logs in as a locked-out user
  Then the customer sees the message "Sorry, this user has been locked out."
```

The first test tells a programmer how the browser is driven. The second tells a programmer how one class behaves. The third tells **everybody** what the business expects. In a BDD project the third one is automated by step definitions that contain essentially the same Selenium code as the first, hidden behind page objects.

### 4. The Three Amigos

The **Three Amigos** is a short collaborative meeting (typically 25-30 minutes) held *before* development of a user story starts. Three perspectives take part:

| Amigo | Brings | Typical questions |
|---|---|---|
| **Business** (product owner / analyst) | What problem we are solving and why | "What does the customer need?" "What is the business rule?" |
| **Development** | What is technically feasible and how it might be built | "What happens if the payment service is down?" "Does this change existing behavior?" |
| **Testing** | The skeptical, what-if mindset | "What if the user enters a negative quantity?" "What about an expired coupon?" |

The meeting produces **concrete examples** of the behavior, including edge cases and rules, which are then written as scenarios. Issues are discovered while still cheap to fix. In many teams more than three people attend (a UX designer, an operations engineer), but the three perspectives remain.

**Why three, and why those three?** Each amigo catches a different kind of mistake:

- Without the **business** voice, the team builds something technically fine that nobody wants.
- Without the **developer** voice, the team agrees to something that is impossible or very expensive to build.
- Without the **tester** voice, the team agrees only on the happy path and forgets the edge cases.

**Who is the "testing" amigo in your career?** That is likely you: a QA engineer or SDET. In a BDD team the tester's most valuable contribution is not clicking through screens, it is asking "what if" questions early. This changes testing from a late-phase checker into an early-phase investigator.

**When to hold the meeting.** After the product owner has a story drafted but **before** the sprint in which developers will build it (often during backlog refinement, or at the start of the sprint). If you hold it after coding is done, you are doing a review, not discovery.

**Ground rules for a good session:**

1. Keep it short and time-boxed (25-30 minutes per story). If a story needs much longer, it is too big; split it.
2. Use **concrete examples** rather than abstract statements.
3. Write down questions you cannot answer; do not guess.
4. Everyone speaks; the loudest voice does not win.
5. Stop when the group feels "we understand this story well enough to start". There is no need for perfection.

#### 4.1 Example mapping: a practical way to run the meeting

**Example mapping** is a technique devised by Matt Wynne (a Cucumber co-founder) to structure the Three Amigos conversation with index cards (physical or virtual, such as sticky notes on Miro or Mural). It uses four colors:

- Yellow: the **story** being discussed (one card, top of the table)
- Blue: the **rules** (business rules and acceptance criteria), one per card, below the story
- Green: **examples** that illustrate each rule, below the related rule
- Red: **questions** that nobody can answer yet (these must be resolved before development)

Layout:

```
                         [ YELLOW: Story ]
                                |
        +-----------------------+------------------------+
        |                       |                        |
  [ BLUE: Rule 1 ]       [ BLUE: Rule 2 ]         [ BLUE: Rule 3 ]
        |                       |                        |
  [GREEN: example]       [GREEN: example]         [GREEN: example]
  [GREEN: example]       [GREEN: example]
                                                  [ RED: question ]
```

**The steps of a session:**

1. **Put the story on the table** (yellow card). The product owner reads it aloud.
2. **Ask for rules.** "What are the rules that govern this story?" Each answer goes on a blue card.
3. **For each rule, ask for examples.** "Can you give me an example where this rule applies? One where it does not?" Each goes on a green card.
4. **Capture questions** (red cards) whenever someone says "I think..." or "I don't know". Do not argue about the answer; park it.
5. **Check the result**. Many red cards or many rules means the story is not ready or is too big. Few cards and no red cards means it is ready for development.

**Reading the result (the "traffic light" of readiness):**

| What the table looks like | What it means |
|---|---|
| Lots of red cards | The story is not ready; the team does not understand it yet. Send it back to the product owner. |
| Too many blue cards (rules) | The story is too big. Split it into several stories. |
| Few cards, mostly green, no red | The story is well understood and ready to be built. |

#### 4.2 A full Three Amigos walkthrough (login on saucedemo.com)

Let us walk through a realistic session. The team is building the login feature for the training site <https://www.saucedemo.com>, a demo shop used throughout Project 2. The participants are Priya (product owner, business amigo), Marcus (developer), and Sam (tester). A facilitator writes cards.

**Step 1: The story card (yellow).**

> As a registered customer, I want to log in with my username and password, so that I can see the products and buy them.

**Step 2: Rules (blue).** Priya is asked: "What rules govern login?"

- Rule A: Only users with a valid username and matching password can log in.
- Rule B: A locked-out user can never log in.
- Rule C: Both username and password are required.

**Step 3: Examples (green).** For each rule the group looks for examples.

| Rule | Examples proposed |
|---|---|
| A: valid credentials only | `standard_user` / `secret_sauce` logs in and sees the products page. `standard_user` / `wrong` is refused with an error. |
| B: locked-out users | `locked_out_user` / `secret_sauce` sees "Epic sadface: Sorry, this user has been locked out." |
| C: both fields required | Empty username shows "Username is required". Empty password (with a username) shows "Password is required". |

**Step 4: Questions (red).** Sam, the tester, asks things Priya has not thought of:

- "Is the username case-sensitive?" (Priya: "I think so, but I am not sure.") This becomes a red card.
- "How many failed attempts before an account is locked?" (Priya: "We do not lock after failed attempts in this release.") This is answered and becomes a note, or an explicit "out of scope" decision.
- "After logging in, where does the user land if they originally tried to open the cart page directly?" (Nobody knows.) Red card.

Marcus, the developer, adds: "The error text comes from the server. Do we want the exact text in the test, or just the fact that an error appears?" The group decides that the exact text matters for the locked-out message because support staff quote it to customers, but for a wrong password the rule is "an error message is shown, mentioning that username and password do not match".

**Step 5: Outcome.** The table has three blue cards, five green cards, and two red cards. Priya takes the red cards away to find answers before the sprint begins. The story is small and clear. Sam and Marcus now have a list of examples that will become scenarios:

```gherkin
Feature: Login

  Scenario: Registered customer logs in with valid credentials
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "secret_sauce"
    Then the customer sees the products page

  Scenario: Customer is refused with a wrong password
    Given the customer is on the login page
    When the customer logs in with username "standard_user" and password "wrong_password"
    Then the customer sees the error "Username and password do not match any user in this service"

  Scenario: Locked-out customer cannot log in
    Given the customer is on the login page
    When the customer logs in with username "locked_out_user" and password "secret_sauce"
    Then the customer sees the error "Sorry, this user has been locked out."

  Scenario: Customer must enter a username
    Given the customer is on the login page
    When the customer logs in with an empty username and password "secret_sauce"
    Then the customer sees the error "Username is required"
```

**Why this session was valuable.** It cost about 25 minutes. It exposed two unanswered questions (case sensitivity, landing page) that would otherwise have been discovered by a developer guessing, or by a customer complaining. It also gave Sam concrete test ideas before a single line of code was written.

Notice the separation of jobs: the *meeting* produced rules and examples (discovery); a person then *wrote* the Gherkin (formulation); later a pair will write step definitions (automation). The meeting itself never touched a keyboard.

You will practice a light version of this in today's pair-programming exercise (the three-amigos style activity) for Project 2. In a pair you will rotate roles: one person speaks as business, one as tester, and both consider the developer's concerns.

### 5. The BDD Cycle: Discovery, Formulation, Automation

The Cucumber community describes BDD as three practices in a loop:

```
   +----------------+      +----------------+      +----------------+
   |   1. DISCOVER  | ---> |  2. FORMULATE  | ---> |  3. AUTOMATE   |
   |  Workshops:    |      |  Write examples|      |  Connect the   |
   |  explore the   |      |  as structured |      |  examples to   |
   |  behavior with |      |  Gherkin       |      |  the system    |
   |  examples      |      |  scenarios     |      |  (step defs)   |
   +----------------+      +----------------+      +-------+--------+
            ^                                              |
            +------------- feedback / new questions <------+
```

1. **Discovery.** Explore the story through conversation. Result: shared understanding, rules, concrete examples, unanswered questions.
2. **Formulation.** Express the examples in **Gherkin**, a plain-language syntax with keywords such as `Feature`, `Scenario`, `Given`, `When`, `Then`. Result: readable specifications. (Gherkin is the topic of its own lesson today.)
3. **Automation.** Write **step definitions** that turn each Gherkin line into executable code. Result: an automated test and a *living* specification. (Step definitions are covered in their own lesson today.)

The order matters. Many teams jump straight to automation (step 3) and skip discovery; they end up with automated tests of the *wrong* behavior.

**What each phase produces and who is involved:**

| Phase | Output | Who | Typical duration | Typical tools |
|---|---|---|---|---|
| Discovery | Rules, examples, questions | Business, developer, tester | 25-30 minutes per story | Index cards, whiteboard, Miro |
| Formulation | `.feature` files | Mostly testers/BAs, reviewed by all | 30-60 minutes per story | Any text editor or IDE |
| Automation | Step definitions, page objects | Developers and automation engineers | Hours to days | Java, Cucumber-JVM, Selenium |

**The feedback loop.** The arrow at the bottom of the diagram matters. When you write step definitions you sometimes discover that a scenario is impossible to run, or ambiguous, or that the feature behaves differently from what was agreed. That feedback returns to the conversation: the scenario is corrected, or the application is fixed. BDD is not a one-way pipeline.

**Where do these phases happen on Project 2?**

| Phase | Your activity today |
|---|---|
| Discovery | Pair three-amigos conversation about a saucedemo.com feature (login, cart, checkout) |
| Formulation | Write `.feature` files in `src/test/resources/features` |
| Automation | Write step definitions that call your Wednesday page objects |

### 6. Living Documentation

Traditional requirement documents go stale: the code changes, the Word document does not. In BDD the scenarios are **executable**. When they run in the pipeline:

- A **green** scenario proves that the described behavior currently works.
- A **red** scenario shows either a bug or an out-of-date specification; either way the team must act.

Therefore the feature files are always as current as the passing tests, which is why they are called **living documentation**. A new team member can read the `features` folder to learn what the system does in plain English, and a business stakeholder can read the Cucumber report to see which behaviors work today.

**Analogy: a map that updates itself.** A paper map is accurate on the day it is printed and wrong a year later when a road changes. A satellite navigation app compares itself with the real world constantly. Executable scenarios are the satellite navigation of requirements: the moment the system and the description disagree, the test goes red and tells you.

**What living documentation is not.** It is not a replacement for everything. Feature files describe *behavior* (what the system does). They do not replace architecture diagrams, API reference documents, or user manuals. Use each document type for what it does best.

**What keeps documentation alive:**

1. The scenarios are run **regularly**, ideally on every code change in a CI pipeline.
2. A failing scenario is **fixed or retired**, never left red and ignored.
3. Feature files live **in the same repository** as the code and are reviewed like code.

### 7. A First Look at a BDD Example

Imagine a story for an online shop: *"As a registered customer, I want to log in so that I can see my products."*

During discovery, the team talks through examples: valid login, wrong password, locked-out account, empty fields. They capture them:

```gherkin
Feature: Login

  Scenario: Successful login with valid credentials
    Given the user is on the login page
    When the user logs in with username "standard_user" and password "secret_sauce"
    Then the user should see the products page

  Scenario: Login fails for a locked-out user
    Given the user is on the login page
    When the user logs in with username "locked_out_user" and password "secret_sauce"
    Then the user should see the error message "Sorry, this user has been locked out."
```

Observe: no CSS selectors, no `driver`, no technical vocabulary. A business person can read it, challenge it ("what about a user who typed the wrong case?"), and approve it. We will learn the syntax line by line in the Gherkin lesson. Right now, notice only the *style*: **concrete examples of behavior in the language of the business**.

**A first, rough line-by-line reading** (no syntax knowledge needed yet):

| Line | What it means in plain English |
|---|---|
| `Feature: Login` | "This file is about the login capability." It is a title for the group of examples below. |
| `Scenario: Successful login with valid credentials` | "Here is one example." The text after the colon names it. |
| `Given the user is on the login page` | The starting situation (context). |
| `When the user logs in with username "standard_user" and password "secret_sauce"` | The action the user performs. The quoted values are the data of this example. |
| `Then the user should see the products page` | The outcome we expect. This is what makes the example a test. |
| (blank line) | Separates the scenarios. |

#### 7.1 Seeing the whole machine run (a preview)

So that "Cucumber executes it" is not magic, here is the idea in miniature. For the line

```gherkin
When the user logs in with username "standard_user" and password "secret_sauce"
```

there is a Java method somewhere:

```java
@When("the user logs in with username {string} and password {string}")
public void theUserLogsInWith(String username, String password) {
    loginPage.login(username, password);   // page object from Wednesday
}
```

Cucumber reads the feature line, finds the method whose text pattern matches, extracts `"standard_user"` and `"secret_sauce"` from the quotes, and calls the method with those values. Inside, the method uses a **page object** to type the values and click login. You will learn this in depth in the Step Definitions lesson and set up the tool in the Cucumber Framework Setup lesson (both today). For now, remember the chain: **sentence, then matching method, then page object, then Selenium**.

### 8. Where Cucumber and Gherkin Fit

| Term | What it is |
|---|---|
| **BDD** | The overall approach (collaboration + examples + automation) |
| **Gherkin** | The plain-language syntax in which scenarios are written (`.feature` files) |
| **Cucumber** | The tool that reads Gherkin files and executes them by matching each line to Java (or other language) methods |
| **Step definition** | A Java method annotated with `@Given`, `@When`, or `@Then` that implements one step |
| **Selenium (and page objects)** | The code inside the step definitions that actually drives the browser |

The stack for your Project 2 BDD layer:

```
feature file (Gherkin)          Business-readable behavior
        | matched by text
        v
step definitions (Java)         Glue: translates steps to calls
        |
        v
page objects (Wednesday)        Know the UI
        |
        v
Selenium WebDriver (Mon-Tue)    Controls the browser
```

BDD tools are available for most languages: **SpecFlow/Reqnroll** (.NET), **Behave** (Python), **Cucumber-JS** (JavaScript), **Cucumber-JVM** (Java, our choice), and others. The ideas are the same everywhere.

**Why the layers matter (a link to what you already know).** On Wednesday you learned that page objects hide locators from tests so that a UI change touches one class rather than fifty tests. BDD adds one more protective layer: Gherkin hides the *mechanics of automation* from the business. Each layer has exactly one reason to change:

| Layer | Changes when... |
|---|---|
| Feature file | The business behavior changes |
| Step definition | The wording of a step changes or the way a step is carried out changes at test level |
| Page object | The page layout or locators change |
| Selenium | A browser or driver change forces it (rarely) |

If a developer renames the login button's id, only the page object changes. The feature files, which the business signed off, stay the same. This is the benefit of keeping scenarios **declarative** (Section 11).

**What about the TestContext idea?** You met the idea of sharing state (such as the `WebDriver`) through a context object earlier this week. In Cucumber, step definitions are spread over several classes and each scenario gets fresh instances, so a shared context object is the standard way to pass the driver and page objects between them. You will see how in the Step Definitions and Cucumber Framework Setup lessons.

### 9. Benefits of BDD

- **Shared understanding** before code is written, so fewer misunderstandings and less rework.
- **Early defect discovery** (in the conversation, not in production).
- **Readable tests** that non-programmers can review.
- **Living documentation** that does not go stale.
- **Focus on value:** only build behavior someone has a concrete example for.
- **Regression safety:** every agreed example is a regression test.

**A worked benefit example: avoiding gold-plating.** A developer is asked to build a "wishlist" feature. Without examples they add sharing, sorting, email reminders, and price alerts "because it might be useful". In an example-mapping session the product owner finds that only "add to wishlist" and "view wishlist" have examples anybody can describe. The rest becomes a question card, then a future story. The team saves weeks building only what the business can actually articulate.

### 10. Challenges and Myths

| Myth / mistake | Reality |
|---|---|
| "BDD is a testing tool." | BDD is a collaboration practice; testing is one outcome. |
| "BDD means writing Selenium tests in Gherkin." | UI-level scenarios are only one use; bad UI-heavy scenarios become slow and brittle. Good scenarios describe **behavior**, not button clicks. |
| "Testers write all the feature files alone." | Without the business and developers in the conversation, you lose the main benefit. |
| "Every test should be a Cucumber scenario." | Unit tests, performance tests, and many technical checks do not belong in Gherkin. |
| "More scenarios = better." | Too many near-duplicate scenarios make the suite slow and hard to maintain. Choose **key examples**. |
| "Gherkin is just a nicer syntax for test scripts." | A scenario written as a click-by-click script ("click the blue button at row 3") defeats the point. |

Costs to be honest about: BDD needs **time for conversations**, **discipline** in writing good scenarios, and **maintenance** of the step-definition layer. It pays off most in domains with complex business rules and many stakeholders. For a tiny script or a throwaway prototype it is probably overkill.

#### 10.1 When BDD is a good fit, and when it is not

| BDD is a good fit when... | BDD is probably not worth it when... |
|---|---|
| There are real business rules that non-technical people own (banking, insurance, e-commerce, booking) | The work is a quick prototype that will be thrown away |
| Misunderstandings between roles have caused rework before | The only "stakeholder" is the developer themselves |
| The team can actually get the business into a short conversation | The business will never read or discuss examples |
| The product will live for years and needs documentation that stays true | You are testing technical qualities such as load time, memory, or pixel layout |
| Regression suites are needed and readable reports help release decisions | A plain unit test says it better and more cheaply |

**A rule of thumb:** if you cannot imagine a non-programmer ever reading a scenario, it probably should not be a Cucumber scenario. Write it as a normal JUnit test instead.

#### 10.2 Common failure patterns in real teams

1. **The "tester-only BDD".** The tester writes all scenarios alone and the rest of the team never reads them. The scenarios become a second, slower test suite. *Fix:* hold the discovery conversation and ask for review of the feature files.
2. **The "UI script in disguise".** Scenarios list every click. They break on every redesign. *Fix:* write at the behavior level (Section 11).
3. **The "giant scenario".** One scenario with 25 steps tests five things. When it fails nobody knows why. *Fix:* one behavior per scenario.
4. **The "orphan suite".** Scenarios fail for weeks and are ignored. Trust is lost. *Fix:* treat red scenarios as production issues.
5. **The "tool-first start".** The team installs Cucumber on day one and writes scenarios before understanding the story. *Fix:* discovery first, tools second.

### 11. Declarative vs. Imperative Scenarios (A Preview of Good Style)

Compare two ways of writing the same scenario:

**Imperative (too detailed, brittle):**

```gherkin
Scenario: Login
  Given I open the browser
  And I navigate to "https://www.saucedemo.com"
  When I type "standard_user" into the field with id "user-name"
  And I type "secret_sauce" into the field with id "password"
  And I click the button with id "login-button"
  Then the URL should contain "inventory"
```

**Declarative (describes behavior):**

```gherkin
Scenario: Registered customer logs in
  Given the customer is on the login page
  When the customer logs in with valid credentials
  Then the customer sees the product catalog
```

The declarative version survives a UI redesign unchanged; only step definitions and page objects change. It is also readable by the business. Writing at the right level of abstraction is the central skill of BDD, and we return to it in the *Features and Scenarios* and *Given/When/Then* lessons.

**Why imperative scenarios hurt, in numbers.** Suppose the login page has 12 scenarios and the id of the login button changes. In the imperative version, each of the 12 scenarios contains the id; you edit 12 scenarios and the business must re-review them. In the declarative version nothing in the feature file changes; you edit one page object. The cost difference grows with the suite.

**A quick test for a step.** Ask yourself three questions:

1. Could a customer say this sentence out loud? ("The customer sees the product catalog": yes. "The element with xpath //div[2] is displayed": no.)
2. Does it describe *what* is wanted, not *how* the screen is operated?
3. Would it still be true if the same feature were delivered on a phone app?

If you answer "no" to any of them, the step is probably too technical.

### 12. Another Short Story: From Vague Requirement to Examples (Banking)

To see discovery on a different domain, here is a compact walkthrough for a banking transfer. The requirement: "Customers can transfer money between their own accounts."

The tester amigo asks: "What if there is not enough money? What if the amount is zero? What about the daily limit?" The group builds this map:

```
Story: As an account holder, I want to transfer money between my own accounts,
       so that I can manage my savings.

Rule 1: The source account must have enough money.
   Example: balance 100, transfer 40 -> balance 60, destination +40
   Example: balance 100, transfer 100 -> balance 0 (allowed)
   Example: balance 100, transfer 100.01 -> refused

Rule 2: The amount must be greater than zero.
   Example: transfer 0 -> refused with "Amount must be greater than zero"

Rule 3: There is a daily transfer limit.
   Question (red): What is the daily limit? Per account or per customer?
```

Observe how the example "transfer 100 from a balance of 100" is the boundary case. Boundary examples are where most bugs live, and the conversation surfaced them without any tooling.

Formulated as Gherkin (simple version, one example only):

```gherkin
Feature: Transfer between own accounts

  Scenario: Transfer an amount smaller than the balance
    Given the customer has a current account with a balance of 100.00
    And the customer has a savings account with a balance of 0.00
    When the customer transfers 40.00 from the current account to the savings account
    Then the current account balance is 60.00
    And the savings account balance is 40.00
```

You will study the keywords `Given`, `When`, `Then`, `And` in the Gherkin and Given/When/Then lessons today.

---

## Hands-On Guided Lab: Your First Discovery Workshop on Paper

**Goal:** Practice the Discovery and Formulation phases for a saucedemo.com feature, with no code. This mirrors what you will do in today's pair activity, only smaller.

**Time:** 40 minutes. **Materials:** a partner, paper or sticky notes (four colors, or write the color on each card), a browser.

**Steps:**

1. **Explore the application (5 minutes).** Open <https://www.saucedemo.com>. Log in as `standard_user` with password `secret_sauce`. Add two products to the cart, open the cart, and start checkout (do not worry about completing it). Note the names of pages and messages you see.
2. **Pick a feature (1 minute).** Choose "Add items to the cart". Write the story on a yellow card:
   `As a shopper, I want to add products to my cart, so that I can buy several items in one order.`
3. **Assign roles (1 minute).** One of you is the **business** amigo (you decide what the shop should do), the other is the **tester** amigo asking "what if". Both consider the developer's viewpoint.
4. **Find rules (8 minutes).** The tester asks "what rules apply?" Write each on a blue card. Example candidates: "The cart badge shows the number of items", "A product can be removed", "Items stay in the cart if the user navigates away".
5. **Find examples (10 minutes).** For each rule write at least two green cards with concrete values. For instance, under "The cart badge shows the number of items": "Add Sauce Labs Backpack: badge shows 1", "Add Backpack and Bike Light: badge shows 2", "Add then remove the Backpack: no badge".
6. **Check the site for answers (5 minutes).** Verify your examples in the browser. If the site behaves differently from what you wrote, decide whether your example or your understanding is wrong. This is the feedback loop at work.
7. **Record questions (3 minutes).** Whatever you could not answer goes on red cards, e.g. "Can the same product be added twice?" (Answer by exploring: on this site, the button changes to Remove, so a second add is not possible.)
8. **Formulate one scenario (7 minutes).** Choose your best example and write it in the style from Section 7:
   ```gherkin
   Scenario: Adding a product updates the cart badge
     Given the shopper is logged in and viewing the products page
     When the shopper adds the "Sauce Labs Backpack" to the cart
     Then the cart badge shows 1
   ```

**Expected output:** a table (or board) with 1 yellow card, 3 or more blue cards, 6 or more green cards, 1-3 red cards, and one written scenario. Read the scenario aloud: if your partner can explain it back without looking at the screen, it is declarative enough.

**Self-check:** Does your scenario mention any id, CSS selector, or XPath? If yes, rewrite it. Does it contain more than one `When`? If yes, split it into two scenarios (the reason is explained in the Given/When/Then lesson).

---

## Troubleshooting: Typical Problems When Starting with BDD

| Symptom | Likely cause | What to do |
|---|---|---|
| The discovery meeting goes on for an hour | Story too big, or discussing implementation | Split the story; move technical design to a separate discussion |
| Everyone nods but nobody can give an example | Understanding is shallow | Ask "can you give me a real value?" until you have numbers and names |
| Scenarios all read like Selenium scripts | Written after the code, from the UI | Rewrite with the business's words; ask "what does the user want to achieve?" |
| The business never reads the feature files | They were never involved in writing them | Bring one or two scenarios to the next planning meeting and ask for corrections |
| Too many scenarios for one story | Testing every combination | Choose the key examples per rule (one happy example plus boundaries) |
| Scenarios fail after every UI change | Imperative style or locators in feature files | Move UI detail into page objects and step definitions |

---

## Common Mistakes

1. **Starting with the tool.** Installing Cucumber before understanding the story. Discovery comes first.
2. **Skipping the "why".** Writing scenarios without knowing the business value in the story.
3. **Vague words.** Using "valid", "large", "quickly", or "appropriate" without a concrete value. Replace them with examples.
4. **Hiding questions.** Guessing an answer rather than writing a red card and asking.
5. **Writing scenarios as test scripts.** Listing every click and locator (imperative style).
6. **Treating BDD as the tester's job alone.** The value is in the conversation.
7. **Automating everything through the UI.** Keep scenarios for behavior that matters; keep unit-level checks in unit tests.
8. **Letting scenarios go stale.** A red scenario that is ignored destroys trust in the whole suite.

---

## Practice Exercises

1. **Explain it.** In three or four sentences, explain BDD to a project manager who has never heard of it. Avoid the words "Cucumber" and "Selenium".
2. **Compare.** Fill in a three-column table (TDD, BDD, script-based Selenium automation) for: who writes it, in what language, and when. Compare with the table above.
3. **Spot the misunderstanding.** A story says "As a shopper, I want to apply a discount code." List five questions that the **testing** amigo might ask and five that the **developer** amigo might ask.
4. **Declarative or imperative?** Classify each step and rewrite imperative ones declaratively:
   - `When I click the element with xpath "//button[3]"`
   - `Given the customer has an item in the cart`
   - `Then the text "Thank you" appears in the div with class "msg"`
5. **Mini example map.** Choose a feature of an app you use (for example "reset password"). On paper make: one story card, three rule cards, two examples per rule, and at least two question cards.
6. **Myth busting.** Pick two myths from the table above and write a short counter-argument for each.
7. **Reflection.** Name one situation in a past project (work, school, or personal) where a misunderstanding of requirements caused rework. How could example-based discussion have helped?
8. **Find the ambiguity.** For the requirement "Users can search for products and the results should load quickly", list every ambiguous word and replace each with a concrete, checkable statement.
9. **Right tool?** For each need, say whether a Cucumber scenario is appropriate or a different kind of test is better: (a) "a customer with a coupon pays less", (b) "the home page loads in under two seconds", (c) "the method `calculateTax(100.0)` returns 8.0", (d) "an expired session redirects to login".
10. **Layer map.** Draw the four-layer stack (feature file, step definitions, page objects, Selenium) for the scenario "Customer adds a backpack to the cart" on saucedemo.com. For each layer write one sentence describing what it would contain for this scenario.
11. **Example map for booking.** Create an example map for the story "As a traveller, I want to cancel my hotel booking, so that I am not charged for a stay I will not take." Include at least three rules (for instance, free cancellation before a deadline, a fee after the deadline, no refund for non-refundable rates), two examples per rule, and two red questions.
12. **Pair rehearsal for Project 2.** With your partner, choose one Project 2 feature (login, product sorting, cart, or checkout). Time-box a 20-minute three-amigos conversation and produce the card set. Keep the cards: you will turn them into stories and a feature file in the next lesson.

---

## Solutions and Hints

**1. Explain it.** Sample answer: "BDD is a way for business people, developers, and testers to agree on exactly how a feature should behave before it is built. They agree by working through real examples, write those examples in plain English, and then a tool runs the same examples as automatic checks. That way the written description and the working software cannot drift apart." Hint: your explanation should mention *agreement before building*, *examples*, and *automated checking*.

**2. Compare.** Selenium scripts: written by testers in Java, usually after development. TDD: written by developers in Java, before the code, at unit level. BDD: written by all three roles, in Gherkin (plain language) backed by Java glue code, before development.

**3. Spot the misunderstanding.** Tester questions: What happens with an expired code? An already-used code? A code typed in lowercase? Can two codes be combined? Is the discount applied before or after tax? Developer questions: Where are codes stored? Is there a limit on attempts to guess codes? Does the discount service have to be available at checkout, and what then if it is down? How do we avoid concurrent use of a single-use code? Does the discount change the stored order total retroactively?

**4. Declarative or imperative?** (a) Imperative; rewrite as `When the customer opens the product details` (or whatever business action the button performs). (b) Declarative; keep. (c) Imperative; rewrite as `Then the customer sees a thank-you confirmation`.

**5. Mini example map.** Check your result with the traffic-light table: no red cards means ready; many blue cards means split.

**6. Myth busting.** Sample for "BDD is a testing tool": BDD begins before any test exists, with a conversation. A team that skipped the conversation and only installed Cucumber would still have misunderstandings, just automated ones. Sample for "More scenarios = better": every scenario costs run-time and maintenance; ten scenarios that repeat the same rule are less useful than three that cover the happy path and the boundaries.

**7. Reflection.** There is no single right answer. A strong answer names a specific ambiguity (for example, "the deadline was Friday, but nobody said which time zone") and shows how a concrete example ("submission at 23:59 Friday in London time is accepted") would have exposed it.

**8. Find the ambiguity.** Ambiguous words: "search" (by name only? by description? by category?), "results" (how many per page? sorted how?), "load" (the whole page or the first result?), "quickly" (a number is needed). Replacement: "When a shopper searches for 'backpack', the first page of up to 20 matching products appears within 2 seconds." Note that the performance claim belongs in a performance test, not in a Cucumber scenario.

**9. Right tool?** (a) Cucumber scenario; it is business behavior. (b) A performance test; not suited to Gherkin. (c) A unit test with JUnit. (d) A Cucumber scenario is appropriate (business-visible behavior), though some teams verify it at API level for speed.

**10. Layer map.** Feature file: `When the shopper adds the "Sauce Labs Backpack" to the cart`. Step definition: a method annotated `@When("the shopper adds the {string} to the cart")` that calls the page object. Page object: `ProductsPage.addToCart(String productName)`, which holds the locator for the product's add button. Selenium: `findElement(...).click()` inside the page object.

**11. Example map for booking.** Possible rules: (1) cancel before the free-cancellation deadline: full refund; (2) cancel after the deadline: first night is charged; (3) non-refundable rate: no refund at any time. Examples: cancel 3 days before a 2-day deadline, full refund of 300.00; cancel exactly on the deadline day at 23:59 (boundary; goes on a red card if unclear). Red questions: "Which time zone defines the deadline?" "Is a partially used stay refunded?"

**12. Pair rehearsal.** Keep the cards in a photo or on a shared board. Check that each rule has at least one example and that each red card has an owner who will find the answer.

---

## Self-Check Questions

1. **What problem was BDD created to solve?** Misunderstanding between business, developers, and testers about what to build, which causes expensive rework.
2. **Name the three amigos and one question each would ask.** Business ("What problem does this solve for the customer?"), Development ("How would this affect existing behavior or the payment service?"), Testing ("What happens if the quantity is negative?").
3. **What are the three phases of the BDD cycle?** Discovery, Formulation, Automation.
4. **What do the four colors of example mapping represent?** Yellow = story, blue = rules, green = examples, red = questions.
5. **What is living documentation, and why is it "living"?** Feature files that are also executable tests; they stay accurate because a failing scenario signals that description and system have diverged.
6. **What is the difference between Gherkin and Cucumber?** Gherkin is the syntax of the plain-language scenarios; Cucumber is the tool that reads them and runs matching Java step definitions.
7. **Why are declarative scenarios better than imperative ones?** They describe business behavior in business language, remain valid when the UI changes, and stay readable by non-programmers.
8. **Give one case in which BDD is not worth the effort.** A throwaway prototype, or a technical check such as a performance measurement.

---

## Summary

- **BDD** is a collaborative approach: *discuss examples, document them in plain language, automate them as tests*. It exists to reduce **misunderstanding** between business, developers, and testers.
- The **Three Amigos** meeting (business, development, testing) explores a story through concrete examples *before* coding. **Example mapping** structures it with yellow (story), blue (rules), green (examples), and red (questions) cards.
- The cycle is **Discovery, Formulation, Automation**; skipping discovery produces well-automated tests of the wrong thing.
- **Gherkin** is the plain-language format; **Cucumber** executes it by matching steps to **step definitions**, which use page objects and Selenium.
- Executable scenarios become **living documentation** that stays accurate.
- Good scenarios are **declarative** (behavior) rather than **imperative** (UI mechanics), so they survive UI change.
- BDD is not "just a tool", it takes collaboration time, and it is not suitable for every kind of test.
- For Project 2, you will hold a small three-amigos conversation, write scenarios for saucedemo.com features, and connect them to your page objects through step definitions.

Next, we look at the raw material of BDD: **user stories and acceptance criteria**.

---

## Additional Resources

- Cucumber documentation, *Behaviour-Driven Development*: https://cucumber.io/docs/bdd/
- Dan North, *Introducing BDD*: https://dannorth.net/introducing-bdd/
- Cucumber documentation, *Example Mapping*: https://cucumber.io/blog/bdd/example-mapping-introduction/
- Cucumber documentation, *Who does what in BDD*: https://cucumber.io/docs/bdd/who-does-what/
