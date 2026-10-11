# Selenium WebDriver Architecture

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what Selenium is, what problem it solves, and where it fits in the Selenium suite (WebDriver, IDE, Grid).
- Describe, step by step, what happens between a line of Java code such as `driver.get(...)` and the browser actually opening a page.
- Name and explain the four main components of the architecture: the Selenium client library (language bindings), the W3C WebDriver protocol, the browser driver, and the browser itself.
- Understand the difference between the `WebDriver` interface and concrete classes such as `ChromeDriver`, and explain why professional code is written against the interface.
- Explain what a session is, what a capability is, and what a `WebElement` really holds.
- Set up a Maven project with the Selenium dependency and run your first test.
- Diagnose the most common beginner errors by reasoning about which layer of the architecture failed.

---

## Why This Matters

Imagine you have just joined a QA team. The product has 400 manual regression test cases that must be executed before every release. Each run takes two testers three days. Releases happen every two weeks. Nobody enjoys this work, people make mistakes when tired, and the team can never keep up.

**Test automation** solves this: a program performs the same clicks, typing and verification that a human tester would, in minutes instead of days, and it never gets tired. **Selenium WebDriver** is the most widely used open-source tool for automating web browsers, and Selenium skills appear in a huge share of Test Automation Engineer job descriptions.

This week's **Epic** is to learn Selenium WebDriver, grow from basic scripts to a well-structured framework, add BDD (Behaviour-Driven Development) with Cucumber, and begin **Project 2: Test Automation Framework**. Everything you build this week sits on top of the architecture explained in this lesson. When a test fails at 2 a.m. in a CI pipeline with a message such as `session not created: This version of ChromeDriver only supports Chrome version 120`, the people who can fix it quickly are the people who understand the architecture. Learning how the pieces fit together is the cheapest debugging skill you can acquire.

### A tester's day, with and without this knowledge

Consider two junior engineers who both see the same red build on Monday morning. The error is `Connection refused: localhost:41233`.

- Engineer A has only memorised commands. They re-run the build three times, hoping it goes away, and then message the team: "Selenium is broken."
- Engineer B knows that every Selenium command is an HTTP request sent to a small local server (the browser driver). "Connection refused" means nobody is listening on that port, so the driver process has died or was never started. They check the build log just above the error, find that Chrome crashed because the CI machine ran out of memory, and ask the DevOps team to give the container more RAM. The fix takes ten minutes.

The only difference between A and B is a mental model of the architecture. That is what this lesson gives you.

### Where this lesson fits

Earlier in the course you learned Java (classes, interfaces, exceptions) and Maven (dependencies and `pom.xml`). Today you use both. This is the first lesson of the Selenium week, so everything else this week (driver configuration, browser options, locators, find methods, navigation, screenshots on Monday; waits and interactions on Tuesday; and so on) is built on the picture you form here.

---

## The Concept

### 1. What is Selenium?

**Selenium** is not one tool; it is a *suite* of tools for automating web browsers:

| Component | What it is | Used for |
|---|---|---|
| **Selenium WebDriver** | A library (API) and a protocol for controlling browsers programmatically | The core of modern test automation; this is what we use all week |
| **Selenium IDE** | A browser extension that records and replays actions | Quick prototypes, learning; not for serious frameworks |
| **Selenium Grid** | A system for running tests on many machines/browsers in parallel | Scaling tests across browsers and operating systems (we only mention it today) |

> **Note:** When people say "Selenium" in a job interview or at work, they almost always mean **Selenium WebDriver**. That is what this lesson, and the rest of the week, covers.

Selenium automates **web applications in browsers**. It cannot automate desktop applications (such as Notepad) or native mobile apps by itself. It supports many programming languages (Java, Python, C#, JavaScript, Ruby) and many browsers (Chrome, Firefox, Edge, Safari). In this course we use **Java**.

**What Selenium is not.** Beginners sometimes expect Selenium to do more than it does. It is not a test framework (it does not tell you whether a test passed; you will add assertions and a runner such as JUnit later in the week), it is not a reporting tool, and it does not manage your test data. Selenium does exactly one job: *drive a browser the way a user would*. Everything else is built around it. This is why the Epic of this week is a *framework*: Selenium is the engine, but a car also needs a chassis, steering and a dashboard.

**When is Selenium the right tool?** Use it when the thing you must verify happens in a real browser: logging in, filling a checkout form, checking that a menu opens. It is a poor fit for checking a back-end calculation (a unit test is faster) or the raw correctness of an API response (an API testing tool is better). A healthy test strategy uses Selenium for a *small number* of important end-to-end user journeys, not for everything.

### 2. A Short History (and Why It Explains the Design)

- **Selenium RC (Remote Control)** was the first generation. It injected JavaScript into the page and needed a separate server. It was slow and had security limitations (browsers refuse to let a page's own JavaScript do certain things).
- **WebDriver** was a separate project that took a different approach: instead of injecting JavaScript, talk directly to the browser using the browser's own native automation support. It behaved much more like a real user.
- The two projects merged to form **Selenium 2**, then matured through **Selenium 3** and today's **Selenium 4**.
- In Selenium 4, the communication language between your test and the browser became an official web standard: the **W3C WebDriver specification** (W3C is the World Wide Web Consortium, the same body that standardises HTML). This is why Selenium works with every major browser in a consistent way.

> **Why you should care:** if you read older blog posts or Stack Overflow answers, you will see terms such as "Selenium RC", "JSON Wire Protocol", and `DesiredCapabilities`. Those belong to older generations. Knowing the history lets you recognise outdated advice quickly.

### 3. The Big Picture: Four Layers

Here is the full path of a command, from your code to the browser:

```
 ┌──────────────────────────┐
 │  1. YOUR TEST CODE        │   driver.get("https://www.saucedemo.com");
 │     (Java + Selenium      │
 │      client library)      │
 └────────────┬─────────────┘
              │   HTTP request (JSON), W3C WebDriver protocol
              │   e.g.  POST /session/{id}/url   {"url": "https://..."}
              ▼
 ┌──────────────────────────┐
 │  2. BROWSER DRIVER        │   chromedriver.exe / geckodriver.exe / msedgedriver.exe
 │     (a small HTTP server) │
 └────────────┬─────────────┘
              │   Browser-specific native automation commands
              ▼
 ┌──────────────────────────┐
 │  3. THE BROWSER           │   Chrome / Firefox / Edge
 │                           │   performs the action (navigates, clicks, types)
 └────────────┬─────────────┘
              │   Result travels back up the same path
              ▼
 ┌──────────────────────────┐
 │  4. RESPONSE              │   HTTP response (JSON): {"value": null}  or an error
 │     back to your code     │   → returns normally OR throws an exception
 └──────────────────────────┘
```

Strictly speaking the W3C protocol is the "language" spoken on the first arrow rather than a box of its own, but it is easiest to remember the architecture as four cooperating parts: **client library, protocol, driver, browser**.

Let us examine each piece.

#### Layer 1: The Selenium Client Library (Language Bindings)

This is the code you write against. In Java, it is a set of `.jar` files delivered through Maven (`selenium-java`). It gives you classes and interfaces such as `WebDriver`, `WebElement`, `By`, `ChromeDriver`, and many more.

The client library's job is **translation**. When you write:

```java
driver.get("https://www.saucedemo.com");
```

the library does *not* open the browser. It builds an HTTP request and sends it to the browser driver. Because every language binding speaks the same protocol, the Java, Python and C# versions of Selenium behave the same way.

**What happens when this line runs (step by step):**

1. Java calls the `get` method on your `driver` object.
2. The method creates a small JSON body: `{"url": "https://www.saucedemo.com"}`.
3. It opens an HTTP connection to the driver's address and sends `POST /session/<your-session-id>/url`.
4. Your Java thread now **blocks** (stops and waits) until the driver replies.
5. When the reply arrives, `get` returns (or throws an exception if the reply was an error).

**Why this matters:** you never write HTTP code yourself. The library hides it, the same way a `FileReader` hides the details of talking to the disk.

#### Layer 2: The W3C WebDriver Protocol

The protocol is the **shared language** between the client library and the browser driver. It is a REST-style API over HTTP carrying JSON. A few examples of its endpoints:

| Your Java call | HTTP request sent by the library |
|---|---|
| `new ChromeDriver()` | `POST /session` (create a new browser session) |
| `driver.get(url)` | `POST /session/{id}/url` |
| `driver.getTitle()` | `GET /session/{id}/title` |
| `driver.findElement(By.id("x"))` | `POST /session/{id}/element` |
| `element.click()` | `POST /session/{id}/element/{elementId}/click` |
| `driver.quit()` | `DELETE /session/{id}` |

If you have met REST before (for example while studying API testing), this table should look familiar: `POST` creates or triggers something, `GET` reads something, `DELETE` removes something. The URL path names the thing being acted on. If you have not, the one-line summary is: *a REST API is a set of web addresses where each address plus an HTTP verb means one action.*

Two ideas are important here:

1. **Session:** Starting a browser creates a *session* with a unique ID. All later commands carry that ID so the driver knows which browser window the command is for. `quit()` ends the session.
2. **Statelessness of the client:** Your test is essentially a client sending requests. If the browser driver is not running or the session has ended, your next command fails.

Because it is plain HTTP, the driver and your tests *can* be on different machines. That is the foundation of **Selenium Grid** and cloud testing services; we mention this only so you understand why the architecture was designed this way. How to run tests remotely is beyond today's scope.

**A real request and response.** To make this concrete, here is what the conversation looks like for `driver.getTitle()`:

```
Request  : GET /session/4f3a9c1e/title
Response : 200 OK
           {"value": "Swag Labs"}
```

And for an element that does not exist:

```
Request  : POST /session/4f3a9c1e/element    {"using": "css selector", "value": "#nope"}
Response : 404 Not Found
           {"value": {"error": "no such element",
                      "message": "no such element: Unable to locate element: ..."}}
```

The client library reads the `error` field `"no such element"` and throws the Java exception `NoSuchElementException`. This mapping from protocol error to Java exception is why Selenium exception names look the way they do.

#### Layer 3: The Browser Driver

Every browser needs a small program that understands the WebDriver protocol and converts it into commands that browser understands:

| Browser | Driver executable | Maintained by |
|---|---|---|
| Google Chrome | `chromedriver` | The Chromium team |
| Mozilla Firefox | `geckodriver` | Mozilla |
| Microsoft Edge | `msedgedriver` | Microsoft |
| Safari | `safaridriver` (ships with macOS) | Apple |

The driver is a tiny local web server. When it starts, it listens on a port (for example, `http://localhost:9515`, the traditional chromedriver default; when Selenium starts it for you, it picks any free port) and waits for commands from your code.

> **Analogy:** Think of ordering at a restaurant in a country whose language you do not speak. You (the test code) talk to a *translator* (the driver) who speaks both your language and the kitchen's. The translator tells the *chef* (the browser) what to do, then reports back. If the translator is missing or only speaks an old dialect (an outdated driver), nothing works even though you and the chef are both fine.

**Version compatibility** matters: the driver version must match the browser's major version. In older Selenium versions, mismatches caused endless `SessionNotCreatedException` errors, and teams used a helper library called WebDriverManager to download drivers automatically. **Since Selenium 4.6, a built-in tool called Selenium Manager** finds your installed browser, downloads the correct driver, and caches it, so you usually need to do nothing. We configure drivers in detail in the next lesson, *Driver Configuration*.

**Why does a separate driver exist at all?** Browser makers each have their own internal way of being remote-controlled. Rather than Selenium learning every browser's private language, each browser vendor ships a driver that implements the standard protocol on one side and the private language on the other. This is the *adapter* pattern: one standard plug, many different sockets.

#### Layer 4: The Browser

Finally the real browser performs the action. Because Selenium talks to the *real* browser, you test what users truly experience: real rendering, real JavaScript execution, real cookies. The browser's reply (success, an element reference, an error) flows back through the driver and the protocol to your code.

### 4. The `WebDriver` Interface vs. `ChromeDriver` Class

In the Java client library, `WebDriver` is an **interface** that lists what a driver can do (`get`, `findElement`, `getTitle`, `quit`, ...). `ChromeDriver`, `FirefoxDriver`, and `EdgeDriver` are **classes** that *implement* that interface, each knowing how to start and talk to its own browser driver.

*Quick Java reminder:* an interface is a contract: a list of method signatures with no bodies. A class that `implements` the interface promises to supply a body for every method. A variable whose type is the interface can hold an object of any class that implements it.

```java
WebDriver driver = new ChromeDriver();   // preferred
ChromeDriver driver2 = new ChromeDriver(); // works, but less flexible
```

Why does professional code write `WebDriver driver = new ChromeDriver();`?

- **Programming to an interface.** Everything after that line only uses `WebDriver` methods. To run on Firefox, you change **one line** (`new FirefoxDriver()`) and the remaining test code is untouched.
- It makes it easy to put the browser choice in a configuration file or command-line parameter later in the project.
- Helper methods can accept a `WebDriver` parameter and work with any browser (this becomes important when you split your code into reusable classes later in the week).

The inheritance picture (simplified):

```
SearchContext (interface)         : findElement, findElements
     ▲
WebDriver (interface)             : get, getTitle, getCurrentUrl, quit, close, manage, navigate ...
     ▲
RemoteWebDriver (class)           : implements the HTTP/JSON communication
     ▲
ChromiumDriver
  ├── ChromeDriver
  └── EdgeDriver
FirefoxDriver (extends RemoteWebDriver)
```

You do not need to memorize this hierarchy now; just remember that **all drivers are `RemoteWebDriver` underneath**, which is why the HTTP client/server picture above is accurate even for a browser on your own laptop.

#### When would you use the concrete type instead?

Occasionally you need something only Chrome offers (for example, Chrome-specific developer-tools features). Then you may hold a `ChromeDriver` variable. That is the exception; start with `WebDriver`.

#### Why `SearchContext` is in the picture

`SearchContext` is the small interface that holds `findElement` and `findElements`. Both `WebDriver` (search the whole page) and `WebElement` (search inside one element) extend it. That is why you can write `driver.findElement(...)` and also `form.findElement(...)`. You will exploit this in the Locator Strategies and Find Methods lessons.

### 5. What Happens When You Run `new ChromeDriver()`?

Walking through the lifecycle step by step makes the architecture concrete:

1. **Selenium Manager** checks your installed Chrome version and ensures a matching `chromedriver` exists (downloading it to a cache folder the first time).
2. The client library **launches the chromedriver process** and waits until its HTTP server is ready.
3. It sends `POST /session` with the requested **capabilities** (browser name, options). Chromedriver starts a Chrome browser with those settings and returns a **session ID**.
4. The `ChromeDriver` Java object stores that session ID. You are now "connected".
5. Each later method call (`get`, `click`, ...) becomes an HTTP request carrying that session ID.
6. `driver.quit()` sends `DELETE /session/{id}`, which closes all windows and ends the driver process.

**Capabilities** are a set of key/value requests you send when creating a session: "I want Chrome", "I want it headless", "accept insecure certificates", and so on. The browser driver replies with what it actually granted. You will set capabilities through *Options* classes in the next two lessons.

**Timeline of a single test run:**

| Time | Event | Layer |
|---|---|---|
| t0 | `new ChromeDriver()` called | Your code |
| t0 + 1 s | Selenium Manager resolves the driver (first run may download it) | Client library |
| t0 + 2 s | chromedriver process starts, listens on a port | Driver |
| t0 + 3 s | Chrome window opens, session ID returned | Browser |
| t0 + 4 s | `driver.get(...)` navigates, page loads | Browser |
| t0 + 6 s | `driver.quit()` closes everything | All |

(Times are illustrative; the point is the order of events.)

### 6. WebElement: A Reference, Not the Element Itself

When you call `driver.findElement(...)`, you receive a `WebElement`. Under the hood, the browser sends back a **unique element reference ID**, and the `WebElement` object holds that ID. Each action like `click()` sends the ID back to the browser. A consequence you will meet soon: if the page changes and that element disappears, the ID becomes *stale* and you get a `StaleElementReferenceException`. We will return to that when we study dynamic pages; for now, remember it is a *reference*.

> **Analogy:** a `WebElement` is like a luggage claim ticket. The ticket is not the suitcase; it only lets you ask the airport for the suitcase. If the airport reshuffles the baggage hall and the suitcase is gone, your ticket is worthless, even though you are still holding it.

### 7. Synchronous Commands

Selenium commands are **synchronous** and blocking: `driver.get(url)` returns only after the browser reports the page has loaded (by default). Your test code executes one command at a time, in order, just as a human performs one action at a time. This is easy to reason about, but it hides a trap: the *page* can keep changing after a command returns (for example, JavaScript loading data). Handling this timing problem is its own topic, which we cover on **Tuesday (Waiting Strategies)**. Today we only note that the problem exists.

### 8. Selenium 4 Extras (for awareness only)

Selenium 4 added relative locators, a new `newWindow` API, and support for the browser's developer-tool protocols. You will meet some of these later. For now, hold on to one idea: the four-layer picture still applies, because these features are built on the same foundation.

---

## Hands-On: Your First Selenium Project

### Step 1: Prerequisites

- JDK 11 or later installed (`java -version`). Selenium 4 requires Java 11 or newer; we compile with 17 below.
- Maven installed (`mvn -version`) or an IDE (IntelliJ IDEA / Eclipse) with Maven support.
- Google Chrome installed.

**Check yourself:** open a terminal and run the three commands below. Each should print a version number rather than "command not found".

```bash
java -version
mvn -version
# Windows: "C:\Program Files\Google\Chrome\Application\chrome.exe" --version
# macOS/Linux: google-chrome --version
```

If `java` works but `mvn` does not, Maven is not on your `PATH`. Use your IDE's built-in Maven or fix the `PATH` before continuing.

### Step 2: Create a Maven project and add Selenium

Create a standard Maven project (for example, `selenium-basics`). In `pom.xml`:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.revature.qea</groupId>
  <artifactId>selenium-basics</artifactId>
  <version>1.0-SNAPSHOT</version>

  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <selenium.version>4.25.0</selenium.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.seleniumhq.selenium</groupId>
      <artifactId>selenium-java</artifactId>
      <version>${selenium.version}</version>
    </dependency>
  </dependencies>
</project>
```

**Explanation:**

- `groupId` / `artifactId` / `version` identify your project.
- The `<properties>` block sets the Java version and defines `selenium.version` once so you can upgrade in one place. `${selenium.version}` in the dependency is replaced by that value.
- The single `selenium-java` dependency pulls in the client library, the Chrome/Firefox/Edge driver classes, and Selenium Manager.
- Use the latest stable 4.x version your instructor specifies; the code in this lesson works on all Selenium 4 versions (4.6 and later for automatic driver management).

**What happens when Maven reads this?** The first time you build, Maven downloads `selenium-java` and everything it depends on (called *transitive dependencies*) from Maven Central into a local folder `~/.m2/repository`. Later builds reuse that cache, so only the first build is slow.

### Step 3: Write the first test

Create `src/main/java/com/revature/qea/FirstSeleniumTest.java`:

```java
package com.revature.qea;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class FirstSeleniumTest {

    public static void main(String[] args) {
        // 1. Start Chrome: creates a session through chromedriver
        WebDriver driver = new ChromeDriver();

        // 2. Navigate to a page
        driver.get("https://www.saucedemo.com");

        // 3. Ask the browser for information about the page
        String title = driver.getTitle();
        System.out.println("Page title: " + title);

        // 4. A simple verification (a real framework would use an assertion library)
        if (title.equals("Swag Labs")) {
            System.out.println("PASS: title is correct");
        } else {
            System.out.println("FAIL: unexpected title -> " + title);
        }

        // 5. Always end the session
        driver.quit();
    }
}
```

**Line-by-line explanation:**

| Code | Meaning |
|---|---|
| `package com.revature.qea;` | Declares which package (folder) the class lives in; must match the folder path under `src/main/java` |
| `import org.openqa.selenium.WebDriver;` | The interface we program against |
| `import org.openqa.selenium.chrome.ChromeDriver;` | The class that starts and controls Chrome |
| `public class FirstSeleniumTest` | A normal Java class; the name must match the file name |
| `public static void main(String[] args)` | The entry point Java runs when you start the program |
| `new ChromeDriver()` | Launches chromedriver + Chrome and creates the session. A browser window appears. |
| `WebDriver driver = ...` | Stores the connection in a variable typed as the interface |
| `driver.get(url)` | Sends the browser to the URL and waits for the page load to complete |
| `driver.getTitle()` | Returns the text in the page's `<title>` tag as a `String` |
| `title.equals("Swag Labs")` | Compares text contents. Never use `==` for strings in Java; it compares object identity, not text |
| `driver.quit()` | Closes **all** windows and terminates the driver process |

Run it. A Chrome window opens (labeled "Chrome is being controlled by automated test software"), the SauceDemo login page loads, the console prints the title, and the window closes.

**Expected console output:**

```
Page title: Swag Labs
PASS: title is correct
```

(If the site changed its title since this lesson was written, you will see the FAIL line with the real title; that is a good demonstration of why a test compares against a value you have actually observed.)

### Step 4: Always use `try/finally`

If an exception occurs before `quit()`, the browser and chromedriver processes stay alive in memory (called *zombie processes*). Over a long test run they consume memory and can hang your build machine. A safer pattern:

```java
WebDriver driver = new ChromeDriver();
try {
    driver.get("https://www.saucedemo.com");
    System.out.println(driver.getTitle());
} finally {
    driver.quit();   // runs even if something above throws an exception
}
```

**How `finally` works:** Java guarantees that the `finally` block runs whether the `try` block finishes normally, throws an exception, or even returns early. That makes it the right place for cleanup code.

Later in the week, with JUnit and Cucumber, this cleanup moves into dedicated setup/teardown methods called *hooks*. The principle stays the same: **every browser you start must be quit.**

### Step 5: Making the Architecture Visible

You can *see* the HTTP conversation. Selenium logs the commands it sends. Add this snippet at the start of `main` to enable detailed logging:

```java
java.util.logging.Logger.getLogger("org.openqa.selenium").setLevel(java.util.logging.Level.FINE);
```

When you run it, you will see lines resembling `POST /session`, `POST /session/.../url`. This demonstrates that, underneath, your Java method calls are plain HTTP requests, as described in the architecture section.

Note that, depending on your logging configuration, the default console handler may still hide `FINE` messages. If you see nothing new, use the driver log file approach in the lab below, which is more reliable.

---

## Guided Lab: See the Layers with Your Own Eyes

**Goal:** prove that Selenium is "just HTTP to a local server" by logging the driver's own conversation, and observe the session lifecycle.

**Step 1.** In the project from above, create `src/main/java/com/revature/qea/ArchitectureLab.java`:

```java
package com.revature.qea;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.remote.RemoteWebDriver;

import java.io.File;

public class ArchitectureLab {

    public static void main(String[] args) {
        // Ask the chromedriver service to write a verbose log file
        ChromeDriverService service = new ChromeDriverService.Builder()
                .withLogFile(new File("chromedriver.log"))
                .withVerbose(true)
                .build();

        WebDriver driver = new ChromeDriver(service);
        try {
            // The session ID is the "ticket" that every later request carries
            String sessionId = ((RemoteWebDriver) driver).getSessionId().toString();
            System.out.println("Session ID : " + sessionId);

            driver.get("https://www.saucedemo.com");
            System.out.println("Title      : " + driver.getTitle());
            System.out.println("Current URL: " + driver.getCurrentUrl());
        } finally {
            driver.quit();
        }
    }
}
```

**Line-by-line:**

- `ChromeDriverService.Builder()` lets us configure how the chromedriver *process* is started (the service is the thing that owns the driver process).
- `.withLogFile(new File("chromedriver.log"))` writes the driver's log to a file in the project folder.
- `.withVerbose(true)` makes the log detailed.
- `.build()` creates the service object.
- `new ChromeDriver(service)` uses our configured service rather than a default one.
- `(RemoteWebDriver) driver` is a *cast*. Our variable is typed `WebDriver`, which has no `getSessionId()`; we know the real object is a `RemoteWebDriver` underneath (remember the hierarchy), so we cast to access it. This also proves the hierarchy statement from section 4.
- `getSessionId().toString()` converts the session ID object to text.

**Step 2.** Run the class.

**Expected console output (your ID will differ):**

```
Session ID : 7c1b0d0a6e0e3a8d9f4b2c5a1e8f7d30
Title      : Swag Labs
Current URL: https://www.saucedemo.com/
```

**Step 3.** Open `chromedriver.log` in the project folder. Search for these words and note what you find:

| Search for | You should see |
|---|---|
| `POST /session` or `New Session` | The request that created the session, including your capabilities |
| `url` | The navigation command with the address you passed to `get` |
| `title` | The `getTitle` request and its response |
| `DELETE` or `Quit` | The command sent by `driver.quit()` |

**Step 4.** Answer in your notes: which layer wrote this file? (Answer: the *browser driver* layer; the file records what the driver received from the client library and what it sent to Chrome.)

**Step 5 (experiment).** Delete the `finally` block's `driver.quit()` line, run again, and check your Task Manager/Activity Monitor for leftover `chromedriver` and `chrome` processes. Close them manually and restore the line. You have just reproduced the "zombie process" problem on purpose.

---

## Reading Errors with the Architecture in Mind

Knowing the layers lets you diagnose where a failure is happening:

| Symptom / Exception | Which layer is probably failing? | Typical cause and fix |
|---|---|---|
| `SessionNotCreatedException: This version of ChromeDriver only supports Chrome version X` | Browser driver ↔ Browser | Driver and browser versions are mismatched. Upgrade Selenium (4.6+ uses Selenium Manager) or the browser; remove a manually configured old driver. |
| `IllegalStateException: The path to the driver executable must be set` | Client library cannot find a driver | Very old Selenium, or Selenium Manager blocked by a corporate network/proxy. Check network/proxy settings. |
| `NoSuchElementException` | Browser/page | The element is not on the page *yet* (or at all). Not an installation problem; a locator or timing problem. |
| `WebDriverException: unknown error: cannot find Chrome binary` | Browser | Chrome is not installed where Selenium expects it. |
| `NoSuchSessionException` / `invalid session id` | Session | `quit()` or `close()` was already called, or the browser crashed. |
| `ConnectionClosed` / `Connection refused` | Protocol/Driver | The driver process died or was blocked by a firewall. |

> **Tip for interviews:** A common question is *"Explain the Selenium architecture."* A strong answer mentions: client libraries in multiple languages → W3C WebDriver protocol (earlier the JSON Wire Protocol) over HTTP → browser-specific driver → real browser, with the response travelling back along the same path.

### Troubleshooting walk-through 1: version mismatch

You run your test on a colleague's laptop and see:

```
org.openqa.selenium.SessionNotCreatedException: Could not start a new session.
Response code 500. Message: session not created: This version of ChromeDriver only supports Chrome version 114
Current browser version is 126.0.6478.127
```

**Diagnosis, layer by layer:**

1. The message starts with `SessionNotCreatedException`: the failure happened during `POST /session`, i.e. while *creating* the session. So the client library did reach a driver (layer 1 to 2 worked).
2. The text says the driver supports 114, but the browser is 126. The failing hop is *driver to browser* (layer 2 to 3).
3. Why is there a version-114 driver at all? Selenium Manager would have fetched a 126 driver. So somebody configured an old driver by hand, probably through `System.setProperty("webdriver.chrome.driver", "C:\\old\\chromedriver.exe")` or an old driver earlier on the `PATH`.

**Fix:** delete the `System.setProperty` line (or the stale driver on the `PATH`) and let Selenium Manager choose the driver.

### Troubleshooting walk-through 2: the browser opens and instantly closes

You run a test and the Chrome window flashes and disappears. No error appears.

1. The program finished. In `main`, once the last line runs, the JVM exits. If your last line is `driver.quit()`, closing is *exactly* what you asked for.
2. If you did not call `quit()`, the window may still vanish when your script ends in some environments, because the driver process is terminated with the JVM.

**Fix for learning purposes:** put `Thread.sleep(5000);` (needs `throws InterruptedException` on `main`) before `quit()` to keep the browser visible for five seconds while you look. This is only a demonstration aid; never use fixed sleeps in real tests (Tuesday explains the correct alternative).

### Troubleshooting walk-through 3: `Connection refused`

```
org.openqa.selenium.WebDriverException: java.net.ConnectException: Connection refused
```

1. `ConnectException` is a plain network error, so the client library tried to reach the driver's HTTP server and nobody answered.
2. Possible causes: the driver crashed (look for a `chrome not reachable` error before it), a firewall blocked the local port, or an earlier test called `quit()` and a later one still uses the same `driver` variable.
3. Check whether `quit()` was called earlier in the same run. In suites, the most common cause is *sharing one driver variable across tests while one test quits it*.

**Fix:** ensure each test creates and quits its own driver, or that exactly one place owns the quit.

### Troubleshooting walk-through 4: Selenium Manager cannot download (corporate network)

```
org.openqa.selenium.WebDriverException: Unable to obtain: ... Selenium Manager failed
```

1. Selenium Manager needs internet access to download a driver the first time. Behind a proxy it may be blocked.
2. Diagnose by opening the download site in a browser from the same machine. If it fails, the network is the problem, not your code.
3. **Fix:** ask IT for the proxy settings, or download the matching driver once and point Selenium to it using the driver-configuration techniques in the next lesson.

---

## Worked Examples and Mini Scenarios

### Example A: Running the same test on two browsers

```java
WebDriver driver = new ChromeDriver();    // line to change
driver.get("https://the-internet.herokuapp.com/");
System.out.println(driver.getTitle());
driver.quit();
```

Change the first line to `new FirefoxDriver()` (import `org.openqa.selenium.firefox.FirefoxDriver`). The output is `The Internet` for both. The other three lines never mention a browser; that is the benefit of the interface. Selenium Manager downloads `geckodriver` automatically the first time.

### Example B: Reading several facts from a page

```java
WebDriver driver = new ChromeDriver();
try {
    driver.get("https://example.com");
    System.out.println("Title      : " + driver.getTitle());
    System.out.println("URL        : " + driver.getCurrentUrl());
    System.out.println("Source size: " + driver.getPageSource().length() + " characters");
} finally {
    driver.quit();
}
```

`getCurrentUrl()` returns the address the browser is on *now* (useful after redirects). `getPageSource()` returns the page's HTML as a string. `length()` is the ordinary Java `String` method. Each of the three calls is a separate HTTP request (`GET /title`, `GET /url`, `GET /source`).

### Example C: Scenario, a smoke test in CI

Your team wants a "smoke test" that runs after each deployment: *is the site up, and does it show the right title?* You write the code from Step 3, wrap it in `try/finally`, and run it from the CI server. When the site is down, `getTitle()` returns something like `502 Bad Gateway` and your check prints FAIL. Because the architecture is client-driver-browser, the CI server needs Chrome installed; that is why CI images for Selenium always include a browser. (Browsers on servers have no screen; running them without a visible window is called headless mode and is covered in the *Browser Options* lesson.)

### Example D: Two sessions at once

```java
WebDriver first  = new ChromeDriver();
WebDriver second = new ChromeDriver();
first.get("https://www.saucedemo.com");
second.get("https://the-internet.herokuapp.com");
first.quit();
second.quit();
```

Two `ChromeDriver` objects mean two chromedriver processes, two browsers, and two different session IDs. Commands sent to `first` never affect `second`. This is a concrete demonstration of the session concept, and it is the principle that makes parallel test execution possible.

---

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Forgetting `driver.quit()` | Leaves browsers and drivers running (zombies) | Use `try/finally` |
| Using `driver.close()` when you mean `quit()` | `close()` closes only the current window; the driver process may stay alive | Use `quit()` at the end of a test |
| Declaring `ChromeDriver driver` everywhere | Locks code to one browser | Declare `WebDriver driver` |
| Hard-coding a driver path with an old driver | Causes version mismatches | Let Selenium Manager handle it |
| Comparing strings with `==` | Compares references, gives false failures | Use `.equals()` |
| Expecting Selenium to decide pass/fail | Selenium only drives the browser | Add assertions (later this week) |

---

## Practice Exercises

1. **Draw it yourself.** Without looking at this lesson, sketch the four layers and label what technology sits at each. Compare with the diagram above.
2. **Change the browser.** Add `import org.openqa.selenium.firefox.FirefoxDriver;` and change *only* the line `new ChromeDriver()` to `new FirefoxDriver()`. Run it. (If Firefox is not installed, try `EdgeDriver` from `org.openqa.selenium.edge`.) Explain in one sentence why nothing else in the code needed to change.
3. **Observe the layers.** Enable the FINE logging snippet (or the log-file lab) and list three different WebDriver protocol requests you can spot in the output.
4. **Break it on purpose.** Remove `driver.quit()` and run the test three times. Open Task Manager (Windows) or Activity Monitor (macOS) and look for lingering `chromedriver` and `chrome` processes. What do you see? Put `quit()` back inside a `finally` block.
5. **Predict the output.** What does `driver.getTitle()` return for `https://example.com`? Test your prediction.
6. **Map code to HTTP.** For each line, write the HTTP verb and path it produces: `driver.get("https://example.com")`, `driver.getCurrentUrl()`, `driver.quit()`.
7. **Page facts program.** Write a program that opens `https://the-internet.herokuapp.com/` and prints the title, the current URL, and the number of characters in the page source, in a `try/finally`.
8. **Title checker.** Write a method `static boolean titleIs(WebDriver driver, String expected)` that returns whether the current page title equals `expected`. Why does accepting a `WebDriver` parameter (not `ChromeDriver`) help?
9. **Two sessions.** Open SauceDemo in one browser and the-internet in another at the same time, print both session IDs, and confirm they differ.
10. **Diagnose.** A teammate reports `SessionNotCreatedException ... only supports Chrome version 114`. Write the three questions you would ask them, in order, and the most likely fix.
11. **Explain to a friend.** In five sentences, explain to a non-technical friend why a separate "driver" program exists between your code and Chrome.

---

## Solutions and Hints

**1.** Layers: Java test + Selenium client library; W3C WebDriver protocol (HTTP/JSON); browser driver (chromedriver etc.); browser.

**2.** Only the construction line mentions a browser. Every other call uses the `WebDriver` interface, which both classes implement.

**3.** Examples: `POST /session` (create), `POST /session/<id>/url` (navigate), `GET /session/<id>/title`, `DELETE /session/<id>` (quit).

**4.** Each run leaves `chromedriver` and `chrome` processes. A `finally` block guarantees cleanup.

**5.** `Example Domain`.

**6.** `POST /session/{id}/url`; `GET /session/{id}/url`; `DELETE /session/{id}`.

**7.**

```java
WebDriver driver = new ChromeDriver();
try {
    driver.get("https://the-internet.herokuapp.com/");
    System.out.println("Title: " + driver.getTitle());
    System.out.println("URL  : " + driver.getCurrentUrl());
    System.out.println("Size : " + driver.getPageSource().length());
} finally {
    driver.quit();
}
```

**8.**

```java
static boolean titleIs(WebDriver driver, String expected) {
    return driver.getTitle().equals(expected);
}
```

Because the method works for Chrome, Firefox or Edge drivers: programming to the interface.

**9.**

```java
WebDriver a = new ChromeDriver();
WebDriver b = new ChromeDriver();
try {
    a.get("https://www.saucedemo.com");
    b.get("https://the-internet.herokuapp.com");
    System.out.println(((RemoteWebDriver) a).getSessionId());
    System.out.println(((RemoteWebDriver) b).getSessionId());
} finally {
    a.quit();
    b.quit();
}
```

**10.** Questions: Are you setting `webdriver.chrome.driver` anywhere? Which Selenium version is in the `pom.xml` (is it 4.6 or later)? Is an old driver on the `PATH`? Likely fix: remove manual driver configuration and use Selenium 4.6+ so Selenium Manager picks the right driver.

**11.** Sample: "Chrome only understands its own private commands. Our test code speaks a standard language that works for every browser. The driver is a translator between the two. Each browser maker supplies its own translator. Without the translator, the standard instructions would not be understood."

---

## Self-Check Q&A

1. **Which component converts the standard protocol into browser-specific commands?** The browser driver (for example chromedriver).
2. **What is a session?** A unique connection to one browser instance; every command carries its ID, and `quit()` ends it.
3. **Why write `WebDriver driver = new ChromeDriver();`?** It programs to the interface, so switching browsers means changing one line.
4. **What does a `WebElement` actually hold?** A reference ID that the browser issued, not the element itself.
5. **What is Selenium Manager and since when does it exist?** A built-in tool (Selenium 4.6+) that finds the browser and downloads a matching driver automatically.
6. **Difference between `close()` and `quit()`?** `close()` closes the current window; `quit()` closes all windows and ends the session and driver process.
7. **Where would you look first for "Connection refused"?** The driver layer: did the process die or was the driver already quit?

---

## Summary

- **Selenium WebDriver** automates real browsers; it is one part of the Selenium suite (WebDriver, IDE, Grid).
- The architecture has four cooperating parts: your **test code + client library**, the **W3C WebDriver protocol** (JSON over HTTP), the **browser driver** (`chromedriver`, `geckodriver`, ...), and the **browser**.
- Every `driver.xxx()` call is translated into an HTTP request carrying a **session ID**; results or errors return along the same path, where protocol errors become Java exceptions.
- Code against the `WebDriver` **interface** so you can swap browsers by changing one line.
- A `WebElement` is a **reference** to something in the browser, which can go stale.
- Commands are **synchronous**, but pages change on their own timeline; waiting strategies (Tuesday) address this.
- Always end the session with `driver.quit()`, ideally in a `finally` block.
- Understanding the layers helps you diagnose errors quickly. This knowledge carries straight into **Project 2**, where your framework will create and quit drivers in one controlled place.

---

## Additional Resources

- Selenium official documentation, *Selenium Overview and Architecture*: https://www.selenium.dev/documentation/overview/
- W3C WebDriver specification (for the curious; technical): https://www.w3.org/TR/webdriver2/
- Selenium official documentation, *WebDriver* section: https://www.selenium.dev/documentation/webdriver/
- Practice sites used this week: https://www.saucedemo.com and https://the-internet.herokuapp.com
