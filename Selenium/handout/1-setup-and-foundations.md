# Selenium In-Class Handout, Group 1: Setup and Foundations

**Topics:** 1.1 Selenium WebDriver architecture · 1.2 Driver configuration · 1.3 Browser options · 1.4 From `main` to a JUnit test

**How to use this handout:** follow along while the trainer codes. Each topic gives you:

- **Definition** and **key terms:** what the topic is and the words you need.
- **Key ideas:** the few points to remember.
- **Worked example:** built together in numbered steps; type only the new lines at each step.
- **Checkpoint:** what you should see once it works.
- **Your turn:** short exercises that practise the same skill.
- **Common errors:** problems beginners actually hit.

In this group you only open pages and read their **title** and **URL**. Finding elements, typing and clicking come in Groups 2 and 3.

---

## Before you start: project setup

**You need:** JDK 17 or later, Maven 3.9+, Google Chrome, and **VS Code** with the **Extension Pack for Java** (by Microsoft; it includes Maven support and the Test Runner for Java). You do **not** need to download a browser driver; topic 1.2 explains why.

**Open the project in VS Code:** *File → Open Folder* and choose the folder that contains `pom.xml`. Whenever you change `pom.xml`, accept VS Code's prompt to **synchronize the Java classpath** (or run **Java: Clean Java Language Server Workspace** from the Command Palette, `Ctrl+Shift+P`).

**Create a Maven project** with this `pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.qea</groupId>
    <artifactId>selenium-week6</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <selenium.version>4.51.0</selenium.version>
        <junit.version>6.1.3</junit.version>
    </properties>

    <dependencies>
        <!-- Selenium for Java: everything needed to control a browser -->
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>${selenium.version}</version>
        </dependency>
        <!-- JUnit: used from topic 1.4 to turn programs into tests -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Runs the tests in src/test/java with: mvn test -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.6.0</version>
            </plugin>
        </plugins>
    </build>
</project>
```

**Where your code goes**

```text
src/main/java/com/qea/selenium/handout/   topics 1.1-1.3 only: small practice programs with a main() method
src/test/java/com/qea/selenium/tests/     topic 1.4 onwards: JUnit tests
src/test/java/com/qea/selenium/pages/     Handout 5: page objects (used only by tests)
```

**How to run in VS Code:**

- A program with `main`: click **Run** in the small links that appear just above `public static void main`.
- A test class or test method: click the green ▷ in the left margin next to it, or open the **Testing** view (the flask icon in the left sidebar).
- From the terminal (*Terminal → New Terminal*): `mvn test` runs all tests.

**Practice sites:** Swag Labs `https://www.saucedemo.com`, a demo shop built for practising test automation, and the-internet `https://the-internet.herokuapp.com`, a collection of small practice pages.

> **Note on the full notes:** the lesson notes keep using `main()` programs until Friday. This handout switches to JUnit tests in topic 1.4, because that is how QE teams write automation.

---

## 1.1 Selenium WebDriver Architecture

### Definition: what is Selenium?

**Selenium** is a free, open-source suite of tools for **automating web browsers**. A Selenium program can do what a person does in a browser: open a page, click links and buttons, type into fields, choose from lists, and read what is on the screen. Testers use it to check that **web applications** work correctly in real browsers (Chrome, Firefox, Edge and Safari) on Windows, macOS and Linux. Selenium is not one program but a **family of tools**; the one we write code with is **Selenium WebDriver**, available for Java, Python, C#, JavaScript and Ruby.

### Where Selenium fits

| | |
|---|---|
| **Where it comes from** | Started in 2004 at ThoughtWorks by Jason Huggins; today run by the open-source Selenium project. Home page: **selenium.dev** |
| **Where you get it** | As a library for your language. In Java: the `selenium-java` dependency in Maven (see the `pom.xml` above) |
| **What it can test** | Anything that runs **in a web browser**: websites and web applications |
| **What it cannot test** | Desktop applications, native mobile apps (use **Appium**, which is built on WebDriver), CAPTCHAs, files on your PC outside the browser |
| **What it does not include** | Test structure, assertions and reports: those come from a test framework such as **JUnit** (topic 1.4) or **Cucumber** |
| **Why teams choose it** | Free, works with all major browsers and languages, a W3C standard, a huge community, and runs on CI servers |

### The Selenium suite: its parts, old and new

| Component | What it is | Status today |
|---|---|---|
| **Selenium Core** | The original tool (2004): a JavaScript program injected into the page to drive it | Retired; its ideas live on in IDE |
| **Selenium RC** (Remote Control) | **Selenium 1**. A **server** sat between your code and the browser and injected Selenium Core's JavaScript into every page. Let you write tests in Java, Python, etc. | **Deprecated and removed**. Slow, and limited by browser security rules on JavaScript |
| **Selenium WebDriver** | Created by Simon Stewart (2006). Controls the browser **directly** through a driver supplied for each browser, without injecting JavaScript and **without a server** in between | **Current**. What this course uses |
| **Selenium IDE** | A **browser extension** for Chrome and Firefox that **records** your clicks and typing and plays them back. Can export recordings as code | Current. Good for quick experiments and learning; not for real test suites |
| **Selenium Grid** | A **server** that sends tests to many machines and browsers at the same time | Current. Used to run large suites in parallel, on several browsers and operating systems |

### Selenium versions

| Version | Year | What changed |
|---|---|---|
| **Selenium 1** | 2004–2011 | Selenium RC + Selenium Core (JavaScript injection) |
| **Selenium 2** | 2011 | **WebDriver merged into Selenium**; RC kept alongside for old tests |
| **Selenium 3** | 2016 | RC removed from the main project; WebDriver only |
| **Selenium 4** | 2021 onwards | Speaks the **W3C WebDriver** standard; new Grid; relative locators; **Selenium Manager** finds drivers automatically (4.6, 2022). Current version: **4.51** |

**Selenium RC vs WebDriver**, the question interviewers love:

| | Selenium RC | Selenium WebDriver |
|---|---|---|
| How it controls the browser | Injects JavaScript into the page | Uses the browser's own driver, directly |
| Needs a separate server | Yes, always | No (only Grid, for remote runs) |
| Speed and realism | Slower; limited by JavaScript security rules | Faster; behaves like a real user |
| Today | Removed | The standard |

### The WebDriver architecture

WebDriver does not control the browser on its own: every command travels through a chain of **four parts**, and that chain is the **Selenium WebDriver architecture**.

| Part | What it is | In our project |
|---|---|---|
| **1. Your test code** | The Java program you write | `FirstScript.java` |
| **2. Selenium client library** (language binding) | The Selenium library for your language. It turns each method call into a standard message. | `selenium-java` from the `pom.xml` |
| **3. Browser driver** | A small program, made by the browser vendor, that receives those messages and controls one kind of browser | `chromedriver` for Chrome |
| **4. Browser** | The real browser that loads the page and does the work | Google Chrome |

```text
 Your code  ──>  Client library  ──(W3C WebDriver messages)──>  chromedriver  ──>  Chrome
 (Java)          (selenium-java)                                (driver)           (browser)
            <──                  <──────────── answers ───────               <──
```

**Key terms:**

- **W3C WebDriver protocol:** the official web standard for the messages between the client library and the driver. Because every browser follows the same standard, the same Java code works with Chrome, Firefox or Edge.
- **Session:** one conversation between your code and one browser. It starts when you create the driver and ends when you call `quit()`.

### Key ideas

- Every Selenium call makes a round trip: **your code → client library → driver → browser**, and the answer comes back the same way.
- `WebDriver` is the Java **interface** for "a browser I can control"; `ChromeDriver` is the class that controls Chrome. Write `WebDriver driver = new ChromeDriver();`.
- Selenium **drives** the browser. It does not decide whether a test passed; that is the job of a test framework such as JUnit (topic 1.4).

### Worked example: your first script (`FirstScript`)

We open Swag Labs, read the page title and URL, and close the browser. Each step is matched to the architecture.

**Step 1: Start a browser.** Create `FirstScript` in `src/main/java/com/qea/selenium/handout` with a `main` method, then add:

```java
WebDriver driver = new ChromeDriver();
```

*Architecture:* the client library starts `chromedriver`, `chromedriver` starts Chrome, and a new **session** begins. A Chrome window opens with the bar "Chrome is being controlled by automated test software".

**Step 2: Open a page.**

```java
driver.get("https://www.saucedemo.com/");
```

*Architecture:* the client library sends a "navigate to URL" message; the driver tells Chrome to load the page; `get` returns once the page has loaded.

**Step 3: Read information from the browser.**

```java
System.out.println("Title: " + driver.getTitle());
System.out.println("URL:   " + driver.getCurrentUrl());
```

*Architecture:* two more round trips. Each one asks Chrome a question and brings the answer back to Java.

**Step 4: End the session.**

```java
driver.quit();
```

*Architecture:* the driver closes every Chrome window, the session ends, and the driver stops.

**Complete program**

```java
// src/main/java/com/qea/selenium/handout/FirstScript.java
package com.qea.selenium.handout;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class FirstScript {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();              // 1. start Chrome: a new session begins

        driver.get("https://www.saucedemo.com/");           // 2. open a page

        System.out.println("Title: " + driver.getTitle());  // 3. read from the browser
        System.out.println("URL:   " + driver.getCurrentUrl());

        driver.quit();                                      // 4. close Chrome: the session ends
    }
}
```

### Checkpoint

A Chrome window opens, shows the Swag Labs login page for a moment, and closes. The console shows:

```text
Title: Swag Labs
URL:   https://www.saucedemo.com/
```

### Your turn

1. Change the program to open `https://the-internet.herokuapp.com` and print its title and URL (expected title: `The Internet`). Then open a second page with another `driver.get(...)`, `https://the-internet.herokuapp.com/login`, and print its title and URL too.
2. Copy the architecture diagram above and, next to the arrows, write which line of your program sends which message.
3. Which Selenium tool fits each job? (a) Record a quick demo of a bug without writing code. (b) Write automated tests in Java. (c) Run 500 tests on Chrome, Firefox and Edge overnight on several machines.
4. In two sentences, explain why WebDriver replaced Selenium RC.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `InvalidArgumentException: invalid argument` | URL without `https://`, e.g. `driver.get("www.saucedemo.com")` | Always give the full URL |
| `SessionNotCreatedException` | Chrome is not installed, or an old `chromedriver` is on your `PATH` | Install Chrome; remove old drivers (see 1.2) |
| Chrome windows stay open after the program ends | `driver.quit()` was not called | Always end with `quit()` (1.2 makes it safe) |

---

## 1.2 Driver Configuration

### Definition

A **browser driver** is the program in the middle of the architecture that receives Selenium's messages and controls the browser. Each browser has its own driver (`chromedriver` for Chrome, `geckodriver` for Firefox, `msedgedriver` for Edge), and the driver's version must match the browser's version. **Driver configuration** means making sure the right driver is found, started and stopped. Since Selenium 4.6, a tool called **Selenium Manager** does the finding automatically, so in most projects driver configuration comes down to two things: create the driver with `new ChromeDriver()`, and always end the session with `quit()`.

### Key terms

| Term | Meaning |
|---|---|
| **Driver version** | The driver's major version must equal the browser's (Chrome 153 needs chromedriver 153) |
| **Selenium Manager** | Part of `selenium-java`. When you create a driver, it checks your browser version and downloads the matching driver if needed. |
| **Driver cache** | Where Selenium Manager keeps downloaded drivers: the `.cache/selenium` folder in your home folder |
| **`quit()`** | Closes **all** browser windows and ends the session. Use it at the end of every program and test. |
| **`close()`** | Closes only the **current** window. Used when you work with several windows (Group 4). |

### Key ideas

- You don't download, unzip or configure `chromedriver` yourself. `new ChromeDriver()` is all the configuration you need.
- The first run can take a few seconds longer while Selenium Manager downloads the driver; later runs use the cache.
- If the program crashes before `quit()`, Chrome stays open. Put `quit()` in a `finally` block so it **always** runs.

### Worked example: a script that always closes the browser (`SafeScript`)

**Step 1: Look at the driver Selenium Manager chose.** Run `FirstScript` from 1.1 again, then open the driver cache folder:

```text
Windows:         C:\Users\<you>\.cache\selenium\chromedriver\...
macOS / Linux:   ~/.cache/selenium/chromedriver/...
```

The folder names contain a version number. Compare it with your Chrome version (Chrome menu → *Help* → *About Google Chrome*): the first number is the same.

**Step 2: A script that fails halfway.** Create `SafeScript` with a mistake on purpose: the second URL has no `https://`.

```java
WebDriver driver = new ChromeDriver();
driver.get("https://www.saucedemo.com/");
System.out.println("Title: " + driver.getTitle());

driver.get("the-internet.herokuapp.com/login");   // mistake: throws InvalidArgumentException
System.out.println("Title: " + driver.getTitle());
driver.quit();                                     // never reached
```

Run it. The program stops with an exception, and **Chrome stays open**, because `quit()` was never reached. Close the window by hand.

**Step 3: Make `quit()` run no matter what.** Wrap the work in `try` and put `quit()` in `finally`:

```java
WebDriver driver = new ChromeDriver();
try {
    driver.get("https://www.saucedemo.com/");
    System.out.println("Title: " + driver.getTitle());

    driver.get("the-internet.herokuapp.com/login");   // still fails...
    System.out.println("Title: " + driver.getTitle());
} finally {
    driver.quit();                                     // ...but this always runs
}
```

Run it again. You still see the exception (the mistake is still there), but this time Chrome closes.

**Step 4: Fix the mistake.** Change the second URL to `https://the-internet.herokuapp.com/login` and run once more. No exception, and Chrome closes.

**Complete program**

```java
// src/main/java/com/qea/selenium/handout/SafeScript.java
package com.qea.selenium.handout;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class SafeScript {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();     // Selenium Manager provides chromedriver
        try {
            driver.get("https://www.saucedemo.com/");
            System.out.println("Title: " + driver.getTitle());

            driver.get("https://the-internet.herokuapp.com/login");
            System.out.println("Title: " + driver.getTitle());
        } finally {
            driver.quit();                         // always runs, even after an exception
        }
    }
}
```

### Checkpoint

| Version | What you see |
|---|---|
| Step 2 (no `try`/`finally`) | `InvalidArgumentException` in the console; **Chrome stays open** |
| Step 3 (with `finally`) | The same exception; **Chrome closes** |
| Step 4 (fixed) | No exception; Chrome closes |

The fixed program prints:

```text
Title: Swag Labs
Title: The Internet
```

### Your turn

1. Replace `driver.quit()` with `driver.close()` and run. With only one window open, what happens to Chrome? Write one sentence on the difference between `close()` and `quit()`. Put `quit()` back.
2. This program leaves Chrome open when it fails. Fix it with `try`/`finally`, then fix the mistake:
   ```java
   WebDriver driver = new ChromeDriver();
   driver.get("https://the-internet.herokuapp.com");
   driver.get("www.saucedemo.com");
   System.out.println(driver.getTitle());
   driver.quit();
   ```
3. Go back to `FirstScript` from 1.1 and add `try`/`finally` to it as well. From now on, every program you write ends this way.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `SessionNotCreatedException: This version of ChromeDriver only supports Chrome version ...` | An old `chromedriver` you downloaded is on your `PATH` and is used instead of Selenium Manager's | Delete the old driver (or remove it from `PATH`) |
| First run fails with a download or network error | Selenium Manager could not download the driver (no internet, or a company proxy) | Check the network; ask your trainer about proxy settings |
| Many Chrome windows left open | Programs crashed before `quit()` | `quit()` in `finally` |
| `NoSuchSessionException` | A command ran after `quit()` | Keep all commands before `quit()` |

---

## 1.3 Browser Options

### Definition

**Browser options** are settings that the browser receives **when it starts**: for example, open maximised, run without a visible window, or use a fixed window size. In Java you collect them in a `ChromeOptions` object and pass it to the driver: `new ChromeDriver(options)`. Most options are **command-line arguments**: the same switches you could give Chrome if you started it from a terminal. Options cannot be changed after the browser has started; to use different options, start a new browser.

### Key terms

| Term | Meaning |
|---|---|
| **`ChromeOptions`** | The Java class that holds Chrome's start-up settings (Firefox has `FirefoxOptions`, Edge has `EdgeOptions`) |
| **Argument** | A start-up switch added with `options.addArguments("--...")` |
| **Headless** | The browser runs normally but **without a visible window**. Used on servers that have no screen, such as CI build machines. |
| **Window size** | The size of the browser window in pixels. Pages can look different at different sizes. |

**Arguments you will actually use:**

| Argument | Effect |
|---|---|
| `--start-maximized` | Opens the window maximised (only with a visible window) |
| `--headless=new` | Runs without a window |
| `--window-size=1280,800` | Fixed window size; always set it when running headless |
| `--incognito` | Opens a private (incognito) window |

### Key ideas

- Build the options **first**, then create the driver with them. Options added after `new ChromeDriver(options)` have no effect.
- Headless runs behave like normal runs; you just can't watch them. Print something (such as the title) to see that the program worked.
- Without options, `new ChromeDriver()` uses Chrome's defaults. That is what our tests use; options are added when a project needs them.

### Worked example: maximised, then headless (`OptionsScript`)

**Step 1: Create options and add one argument.** Start from a copy of `SafeScript` and add, **above** `new ChromeDriver`:

```java
ChromeOptions options = new ChromeOptions();
options.addArguments("--start-maximized");
```

**Step 2: Pass the options to the driver.**

```java
WebDriver driver = new ChromeDriver(options);
```

Run it. Chrome opens **maximised**.

**Step 3: Print the window size** inside the `try` block, so you can see what the options did.

```java
System.out.println("Window size: " + driver.manage().window().getSize());
```

**Step 4: Switch to headless with a fixed size.** Replace `--start-maximized` with these two arguments:

```java
options.addArguments("--headless=new");
options.addArguments("--window-size=1280,800");
```

Run again. **No window appears**, but the console still shows the title, so Chrome really ran.

**Complete program**

```java
// src/main/java/com/qea/selenium/handout/OptionsScript.java
package com.qea.selenium.handout;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class OptionsScript {

    public static void main(String[] args) {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");          // no visible window
        options.addArguments("--window-size=1280,800");  // fixed size, same on every machine

        WebDriver driver = new ChromeDriver(options);    // the options are used at start-up
        try {
            driver.get("https://www.saucedemo.com/");
            System.out.println("Title:       " + driver.getTitle());
            System.out.println("Window size: " + driver.manage().window().getSize());
        } finally {
            driver.quit();
        }
    }
}
```

### Checkpoint

After step 2, Chrome opens maximised. With the complete program, **no window appears** and the console shows:

```text
Title:       Swag Labs
Window size: (1280, 800)
```

### Your turn

1. Replace the two arguments with `--incognito` and run. How can you tell from the Chrome window that it is incognito?
2. Run the complete program again **without** the `--window-size` line. What window size is printed now? Why might a page look different in a headless run on a build server?
3. Combine options: open the-internet's login page (`https://the-internet.herokuapp.com/login`) headless at `1024,768`, and print its title and the window size.

### Common errors

| You see | Why | Fix |
|---|---|---|
| Options have no effect | Driver created with `new ChromeDriver()` instead of `new ChromeDriver(options)`, or arguments added after creating it | Add arguments first, then pass `options` |
| A different page layout in headless runs | Headless without a window size gets a small default window | Always add `--window-size` with `--headless=new` |
| `--start-maximized` seems ignored | It has no effect in headless mode (there is no screen to fill) | Use `--window-size` when headless |
| Typo in an argument (e.g. `--headles=new`) | Chrome silently ignores unknown arguments | Copy argument names exactly |

---

## 1.4 From `main` to a JUnit Test

### Definition

A **test framework** is a tool that runs checks, reports which passed and which failed, and keeps tests separate from each other. **JUnit** is the standard test framework for Java; its current API is called **Jupiter**. In JUnit, a **test** is a method marked with `@Test` that uses **assertions** to compare what you expected with what actually happened. Unlike our `main()` programs, which only print values for a person to read, a JUnit test decides **pass** or **fail** by itself, so hundreds of tests can run without anyone reading the output.

### Key terms

| Term | Meaning |
|---|---|
| **Test class** | A class containing tests, in `src/test/java`, usually named `...Test` |
| **`@Test`** | Marks a method as a test |
| **Assertion** | A check such as `assertEquals(expected, actual)`. If it fails, the test fails and both values are shown. |
| **`@BeforeEach` / `@AfterEach`** | Methods that run **before** / **after** every test, e.g. start and quit the browser |
| **Base class** | A parent class that holds code every test class shares; test classes `extend` it |

### Key ideas

| `main()` program | JUnit test |
|---|---|
| `System.out.println(driver.getTitle());` and a person reads it | `assertEquals("Swag Labs", driver.getTitle());` decides pass/fail |
| `try { ... } finally { driver.quit(); }` | `@BeforeEach` starts the browser, `@AfterEach` quits it |
| One program does one thing | One class holds many independent `@Test` methods |

- **Expected value first:** `assertEquals(expected, actual)`. Swapping them makes failure messages confusing.
- Each test gets **its own fresh browser**, so tests never depend on each other.
- Shared start/quit code goes into one **base class**, `BaseTest`, so it is written once.

### Worked example: `FirstTest`, then `BaseTest`

**Step 1: Create a test class.** In `src/test/java/com/qea/selenium/tests`, create `FirstTest`. Test classes and methods do not need to be `public`.

```java
class FirstTest {

}
```

**Step 2: Start and quit the browser around every test.**

```java
WebDriver driver;

@BeforeEach
void startBrowser() {
    driver = new ChromeDriver();
}

@AfterEach
void stopBrowser() {
    driver.quit();
}
```

**Step 3: The first test: `FirstScript` as an assertion.**

```java
@Test
void titleIsSwagLabs() {
    driver.get("https://www.saucedemo.com/");
    assertEquals("Swag Labs", driver.getTitle());
}
```

Click the green ▷ in the margin next to the class. One browser opens and closes, and the test gets a green tick.

**Step 4: A second test.**

```java
@Test
void urlIsTheLoginPage() {
    driver.get("https://www.saucedemo.com/");
    assertEquals("https://www.saucedemo.com/", driver.getCurrentUrl());
}
```

Run the class again. **Two** browsers open and close, one per test.

**Step 5: Move the shared code into `BaseTest`.** Every test class will need the field and the two methods from step 2, so put them in a base class. Use `protected` so subclasses can use `driver`:

```java
public abstract class BaseTest {

    protected WebDriver driver;

    @BeforeEach
    void startBrowser() {
        driver = new ChromeDriver();
    }

    @AfterEach
    void stopBrowser() {
        driver.quit();
    }
}
```

Then change `FirstTest` to `class FirstTest extends BaseTest`, and **delete** its own `driver` field and the two methods from step 2. Run again: still two green tests.

**Complete code**

```java
// src/test/java/com/qea/selenium/tests/BaseTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

/** Every UI test class extends this: a fresh browser before each test, quit after it. */
public abstract class BaseTest {

    protected WebDriver driver;

    @BeforeEach
    void startBrowser() {
        driver = new ChromeDriver();
    }

    @AfterEach
    void stopBrowser() {
        driver.quit();
    }
}
```

```java
// src/test/java/com/qea/selenium/tests/FirstTest.java
package com.qea.selenium.tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class FirstTest extends BaseTest {

    @Test
    void titleIsSwagLabs() {
        driver.get("https://www.saucedemo.com/");
        assertEquals("Swag Labs", driver.getTitle());
    }

    @Test
    void urlIsTheLoginPage() {
        driver.get("https://www.saucedemo.com/");
        assertEquals("https://www.saucedemo.com/", driver.getCurrentUrl());
    }
}
```

### Checkpoint

In VS Code's **Testing** view (flask icon) or the **Test Results** panel:

```text
✔ FirstTest
   ✔ titleIsSwagLabs()
   ✔ urlIsTheLoginPage()
```

From a terminal, `mvn test` ends with:

```text
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

### Your turn

1. Make a test fail on purpose: change `"Swag Labs"` to `"Swag Lab"`. Run it and find the line `expected: <Swag Lab> but was: <Swag Labs>`. Put it back.
2. Create `InternetTest extends BaseTest` with a test that opens `https://the-internet.herokuapp.com` and checks the title is `The Internet`.
3. Add a second test to `InternetTest` that opens `https://the-internet.herokuapp.com/login` and checks the URL.

### Common errors

| You see | Why | Fix |
|---|---|---|
| "No tests found" / `Tests run: 0` | Test class in `src/main/java`, or the `junit-jupiter` dependency is missing | Put tests in `src/test/java`; check the `pom.xml` |
| Test is ignored | Imported `org.junit.Test` (old JUnit 4), or the method is `private` | Import `org.junit.jupiter.api.Test`; don't make test methods `private` |
| Failure message reads backwards | `assertEquals(actual, expected)` | Expected value first |
| `NullPointerException` on `driver` | `FirstTest` still declares its own `driver` field after extending `BaseTest` | Delete the field from `FirstTest` |

---

**End of Group 1.** You can explain what Selenium is and how its four parts work together, start and safely stop a browser, start it with options, and check results with JUnit tests that share a `BaseTest`. **Next:** Group 2, Navigating and Finding Elements.
