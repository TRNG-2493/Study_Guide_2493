# Driver Configuration

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a browser driver is and why its version must match the browser.
- Use Selenium Manager (built into Selenium 4.6+) to get drivers automatically, and explain step by step how it works.
- Configure drivers manually when automatic management is not possible (system properties, `ChromeDriverService`).
- Start Chrome, Firefox, and Edge with the correct classes.
- Write a small reusable `DriverFactory` that chooses a browser by name, and explain every line of it.
- Understand the lifecycle methods `close()` vs. `quit()`, and why driver cleanup matters.
- Troubleshoot typical configuration problems such as version mismatches, permission problems and blocked downloads, by reading the error text.

---

## Why This Matters

In the previous lesson you saw that every Selenium test passes through a **browser driver**. In real projects, driver configuration is the number-one cause of "it works on my machine but not on the build server" problems. Teams lose hours when Chrome auto-updates overnight and every test in the pipeline fails the next morning with a driver mismatch error.

For **Project 2 (Test Automation Framework)**, you will build a framework other people will run on their laptops and on a CI server. A good framework hides driver details behind a single, well-tested place so no individual test cares which browser is being used or where the driver executable lives. Today's lesson prepares the first building block of that framework skeleton.

### A real-world scenario

It is Tuesday at 9:00. Last night the QA team's 120 Selenium tests were all green. This morning the CI dashboard shows 120 red tests. Nobody changed any code. The log says:

```
session not created: This version of ChromeDriver only supports Chrome version 124
Current browser version is 126.0.6478.127
```

What happened? The build server's Chrome updated itself overnight, but the team had pinned an old chromedriver in a `drivers/` folder. This is exactly the problem that driver configuration (and Selenium Manager) exists to solve. After this lesson you will know why it happened, three ways to fix it, and how to design your framework so it cannot happen again.

### How this connects to what you already know

- *Architecture lesson:* the driver is layer 3, the local HTTP server between your code and the browser. Here we learn how to obtain it, start it, and stop it.
- *Java fundamentals:* we will use `static` methods, `switch`, exceptions and `System.getProperty`, all of which you have already met. We recap each one where it appears.

---

## The Concept

### 1. What Is a Browser Driver, Again?

A **browser driver** is an executable (for example `chromedriver.exe`) that implements the WebDriver protocol for one specific browser. Your Java code never talks to Chrome directly; it talks to chromedriver, which talks to Chrome.

| Browser | Selenium class | Driver executable |
|---|---|---|
| Chrome | `ChromeDriver` | chromedriver |
| Firefox | `FirefoxDriver` | geckodriver |
| Edge | `EdgeDriver` | msedgedriver |
| Safari | `SafariDriver` | safaridriver (pre-installed on macOS) |

**Why must versions match?** Browsers change their internals often (Chrome releases a major version roughly every four weeks). The driver is built against specific browser internals; a driver for Chrome 120 may not work with Chrome 125. This is the single most common configuration error.

> **Analogy:** A driver is like a charger cable for a phone. The plug shape (the protocol) is standard, but the voltage details (the browser internals) change with each phone model. An old cable might fit but not charge, which is exactly why a mismatched driver produces confusing errors rather than a clear "wrong part".

**Understanding "major version".** Chrome version `126.0.6478.127` has four numbers. The first (`126`) is the *major* version; that is the one that must match the driver. Minor differences in the last numbers are generally fine. When we say "Chrome 126" we mean major version 126.

**What is the difference between the *driver* and the *browser*?** Beginners often install a driver thinking it is the browser, or vice versa. Remember: you install the *browser* like any application (the same Chrome you use daily). The *driver* is a small helper file that you never open yourself. Selenium starts it for you.

### 2. Three Eras of Driver Management

Understanding history helps you read older tutorials (and old company code!) without getting confused.

**Era 1: Manual download and system property (Selenium 3 and earlier).**

1. Check your browser version.
2. Visit the driver's download site and pick the matching version.
3. Unzip it somewhere and tell Selenium where it is:

```java
System.setProperty("webdriver.chrome.driver", "C:\\drivers\\chromedriver.exe");
WebDriver driver = new ChromeDriver();
```

**Line by line:**

- `System.setProperty(key, value)` is a standard Java method that stores a named setting in the running JVM. It is not a Selenium method.
- `"webdriver.chrome.driver"` is the exact name Selenium looks up when it needs the chromedriver path. If the name is misspelled, Selenium silently ignores it.
- `"C:\\drivers\\chromedriver.exe"` is the path. In a Java string, a backslash must be written twice (`\\`) because a single backslash begins an escape sequence such as `\n`.
- `new ChromeDriver()` finds the property, starts that executable, and creates the session.

Problems: every team member must repeat this; the path differs on each machine; every browser update breaks the setup.

**Era 2: WebDriverManager (third-party library).**

A popular library by Boni García automated the download:

```java
// Requires an extra dependency: io.github.bonigarcia:webdrivermanager
WebDriverManager.chromedriver().setup();
WebDriver driver = new ChromeDriver();
```

You will still see this in many existing code bases. It works well, but it is an extra dependency to maintain. If you meet it, you do not need to remove it urgently; just know that Selenium 4.6+ makes it unnecessary.

**Era 3: Selenium Manager (built into Selenium 4.6 and later). This is today's recommended approach.**

```java
WebDriver driver = new ChromeDriver();  // that's it
```

Nothing else is needed. Selenium Manager is a small command-line program bundled with the Selenium jar. When you create a driver and no driver path has been configured, Selenium calls it to:

1. Detect the browser version installed on the machine (or download the browser itself, if allowed and missing).
2. Determine the matching driver version.
3. Download the driver into a cache folder (`~/.cache/selenium` on Linux/macOS, `%USERPROFILE%\.cache\selenium` on Windows) the first time, and reuse it afterwards.
4. Hand the driver's path back to Selenium.

> **Practical note:** The first run on a machine is slower because of the download. Machines without internet access (or behind strict proxies) cannot download drivers; in those cases you use the manual method in Section 5.

**What happens when `new ChromeDriver()` runs, in detail:**

| Step | Who acts | What happens |
|---|---|---|
| 1 | `ChromeDriver` constructor | Checks: is `webdriver.chrome.driver` set? Is a driver given through a service? |
| 2 | Selenium | If nothing is configured, it runs Selenium Manager |
| 3 | Selenium Manager | Finds Chrome on your machine, reads its version, looks up the matching driver |
| 4 | Selenium Manager | Checks the cache; if the driver is there, uses it; otherwise downloads it |
| 5 | Selenium | Starts chromedriver on a free port |
| 6 | Selenium | Sends `POST /session`; Chrome opens |

**The order of precedence** is worth remembering: an explicit driver you configured always wins; only if none is configured does Selenium Manager run. That is why a stale manual setting can override the automation and cause the mismatch from the scenario above.

**When to rely on Selenium Manager:** laptops, most CI servers with internet access, and almost every new project. **When not to:** locked-down networks, air-gapped environments, or when your organisation requires a pinned, approved driver version.

### 3. Using Selenium Manager: Complete Example

Your `pom.xml` only needs the `selenium-java` dependency (see Architecture lesson). Then:

```java
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class DriverBasics {
    public static void main(String[] args) {
        WebDriver chrome = new ChromeDriver();
        chrome.get("https://www.saucedemo.com");
        System.out.println("Chrome: " + chrome.getTitle());
        chrome.quit();

        WebDriver firefox = new FirefoxDriver();
        firefox.get("https://www.saucedemo.com");
        System.out.println("Firefox: " + firefox.getTitle());
        firefox.quit();

        WebDriver edge = new EdgeDriver();
        edge.get("https://www.saucedemo.com");
        System.out.println("Edge: " + edge.getTitle());
        edge.quit();
    }
}
```

**What the code teaches:**

- Each browser has its own class in its own package (`chrome`, `firefox`, `edge`).
- Because all implement `WebDriver`, the variable type is the same.
- Each requires its browser to be installed on your machine (Selenium Manager can fetch drivers; it will not necessarily install every browser for you).

**Walk-through of the program:**

1. The three `import` lines for browser classes tell Java where to find `ChromeDriver`, `EdgeDriver`, `FirefoxDriver`. The first `import` brings in the `WebDriver` interface.
2. `new ChromeDriver()` starts chromedriver and Chrome; `get` opens SauceDemo; `getTitle()` returns `Swag Labs`; `quit()` closes the browser.
3. The same four-step pattern repeats for Firefox and Edge. Only the class name differs.
4. The browsers open **one after another**, not at the same time, because each is quit before the next starts.

**Expected output** (if all three browsers are installed):

```
Chrome: Swag Labs
Firefox: Swag Labs
Edge: Swag Labs
```

If a browser is not installed, that line is replaced by an exception (see the troubleshooting table). In that case, delete that block and keep the others.

### 4. Where the Driver Comes From: Inspecting What Selenium Manager Did

Many learners find "magic" uncomfortable. You can verify what Selenium Manager did:

1. Run any test once.
2. Open the cache folder (`%USERPROFILE%\.cache\selenium` on Windows; `~/.cache/selenium` on macOS/Linux).
3. You will find a folder per driver type (such as `chromedriver`) with sub-folders named by platform and version, and a file `se-metadata.json` that records what was resolved and when.

Why the cache matters in practice: on CI servers that start from a clean container every time, the cache is empty on each run, so each run downloads the driver again. Teams then either keep the cache folder between runs or bake the driver into the container image. If your pipeline is mysteriously 15 seconds slower than your laptop, this is a common reason.

### 5. Manual Configuration (When You Need It)

You will occasionally need to specify the driver yourself:

- Corporate machines with **no internet access** to the driver download servers.
- A requirement to use an **approved, pinned driver version**.
- Testing against a **custom browser location** (for example a portable Chrome install).

**Option A: System property (global, simple)**

```java
System.setProperty("webdriver.chrome.driver", "C:\\tools\\drivers\\chromedriver.exe");
WebDriver driver = new ChromeDriver();
```

Property names: `webdriver.chrome.driver`, `webdriver.gecko.driver` (Firefox), `webdriver.edge.driver`.

> Use **relative** paths or paths from a configuration file in real projects. Hard-coded `C:\` paths break on other machines.

*Why "global"?* A system property affects the whole running program, so *every* `ChromeDriver` created afterwards uses that file. This is convenient and also risky: someone's forgotten line in a corner of the code base can override Selenium Manager for all tests. When you debug a version mismatch, search the project for `webdriver.chrome.driver` first.

You can also supply the property from outside the code, which keeps paths out of source control:

```
mvn test -Dwebdriver.chrome.driver=/opt/drivers/chromedriver
```

**Option B: Driver service (explicit, per instance)**

```java
import org.openqa.selenium.chrome.ChromeDriverService;
import java.io.File;

ChromeDriverService service = new ChromeDriverService.Builder()
        .usingDriverExecutable(new File("drivers/chromedriver.exe"))
        .usingAnyFreePort()
        .build();

WebDriver driver = new ChromeDriver(service);
```

**Line by line:**

- A *service* is the object that represents the chromedriver **process** (start it, stop it, choose its port and log file).
- `new ChromeDriverService.Builder()` begins building one. A *builder* is a Java pattern where you chain method calls and finish with `build()`.
- `.usingDriverExecutable(new File(...))` points at the driver file. `File` is the standard Java class for a path.
- `.usingAnyFreePort()` lets the operating system choose an unused port, which avoids "port already in use" clashes when running several drivers.
- `.build()` creates the finished service.
- `new ChromeDriver(service)` starts the process described by the service rather than a default one.

Other useful builder methods: `.withLogFile(new File("chromedriver.log"))` (write the driver's log to a file), `.withVerbose(true)` (log more detail, as used in the Architecture lab), `.usingPort(9515)` (fixed port), `.withSilent(true)` (less log noise). The Firefox and Edge equivalents are `GeckoDriverService.Builder` and `EdgeDriverService.Builder`.

**When to use A vs. B:** use A for a quick fix or a CI environment variable; use B when you need per-driver control such as log files or ports, or when different tests need different driver files.

**Option C: Specify the browser binary** (the browser itself, not the driver) through options. This belongs to the *Browser Options* lesson later today; we mention only that it exists.

### 6. The Driver Lifecycle: `close()` vs. `quit()`

| Method | What it does |
|---|---|
| `driver.close()` | Closes the **current window/tab** only. If it is the last window, the browser closes but the **driver process may keep running**. |
| `driver.quit()` | Closes **all** windows, ends the session, and **stops the driver process**. |

**Rule of thumb:** use `quit()` at the end of every test (or test class). Use `close()` only when you deliberately want to close one window while keeping the session alive (we explore multiple windows on Wednesday).

**The complete lifecycle of a driver:**

```
create  ->  use (get, find, click ...)  ->  quit
  |                                           |
  +--  if anything fails in the middle, quit must STILL happen
```

**Why cleanup matters beyond tidiness:**

- Each leftover browser can use 200 MB or more of RAM. Fifty leftover browsers can freeze a build server.
- Leftover drivers hold network ports, so later runs can fail with "port in use".
- On shared CI agents, zombie processes from your build can break *another team's* build.

**After `quit()` the driver object is dead.** Calling any method on it throws an exception (`NoSuchSessionException` or similar). Create a new driver if you need a fresh browser.

```java
WebDriver driver = new ChromeDriver();
driver.quit();
driver.get("https://www.saucedemo.com");   // throws: the session no longer exists
```

### 7. A Reusable `DriverFactory`

Imagine 50 tests each calling `new ChromeDriver()`. When your manager asks you to run everything on Firefox, you must edit 50 files. The professional solution is one class that creates drivers:

```java
package com.revature.qea.drivers;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class DriverFactory {

    private DriverFactory() {
        // utility class: prevent instantiation
    }

    public static WebDriver createDriver(String browserName) {
        if (browserName == null) {
            throw new IllegalArgumentException("Browser name must not be null");
        }

        switch (browserName.trim().toLowerCase()) {
            case "chrome":
                return new ChromeDriver();
            case "firefox":
                return new FirefoxDriver();
            case "edge":
                return new EdgeDriver();
            default:
                throw new IllegalArgumentException(
                    "Unsupported browser: '" + browserName + "'. Use chrome, firefox or edge.");
        }
    }
}
```

**Usage:**

```java
String browser = System.getProperty("browser", "chrome");   // default: chrome
WebDriver driver = DriverFactory.createDriver(browser);
```

Run with a different browser from the command line (Maven passes `-D` values as system properties; this requires the Surefire test plugin and a test class, which you will set up with JUnit later in the week; for now run `main` methods from the IDE and set `-Dbrowser=...` as a VM option):

```
mvn test -Dbrowser=firefox
```

**Explanations, line by line:**

- `package com.revature.qea.drivers;` puts the class in a `drivers` package, separate from tests. Separation of concerns: tests describe *what* to check; the factory knows *how* to start browsers.
- `private DriverFactory()` makes the class a pure utility; nobody can create an instance with `new DriverFactory()`.
- `public static WebDriver createDriver(String browserName)`: `static` means you call `DriverFactory.createDriver(...)` without creating an object; the **return type is the interface** `WebDriver`, so callers never see `ChromeDriver`.
- `if (browserName == null)`: a `null` name would cause a confusing `NullPointerException` on the next line, so we check first and throw a clear exception.
- `browserName.trim().toLowerCase()` normalises input: `" Chrome "`, `"CHROME"` and `"chrome"` all work.
- `switch` compares the normalised text against each `case`. Each case `return`s, so there is no need for `break`.
- `default:` handles everything else; throwing `IllegalArgumentException` with a helpful message **fails fast** on typos like `"crome"`, naming the valid choices.
- `System.getProperty("browser", "chrome")` reads the `-Dbrowser` value or falls back to `"chrome"`.

This is exactly the seed of the **Project 2 framework skeleton**: a `drivers` package with one place that decides how browsers start. Later (Browser Options lesson) we add headless and other settings to it.

#### Variation: a modern `switch` expression (Java 14+)

```java
public static WebDriver createDriver(String browserName) {
    return switch (browserName.trim().toLowerCase()) {
        case "chrome"  -> new ChromeDriver();
        case "firefox" -> new FirefoxDriver();
        case "edge"    -> new EdgeDriver();
        default -> throw new IllegalArgumentException("Unsupported browser: " + browserName);
    };
}
```

The `->` form is shorter, cannot "fall through" by accident, and produces a value. Use it if your project targets Java 17 (as ours does); use the classic form if you must support older Java.

#### Variation: an `enum` instead of strings

```java
public enum Browser { CHROME, FIREFOX, EDGE }

public static WebDriver createDriver(Browser browser) {
    return switch (browser) {
        case CHROME  -> new ChromeDriver();
        case FIREFOX -> new FirefoxDriver();
        case EDGE    -> new EdgeDriver();
    };
}
```

With an enum the compiler rejects a misspelt browser at compile time, instead of failing at run time. The trade-off: you must convert the text from the command line with `Browser.valueOf(text.toUpperCase())`. Strings are friendlier for configuration; enums are safer inside code. Many frameworks do both.

#### Variation: keep the driver in one place

Tests often need the same driver in several helper classes. A very small holder avoids passing it around everywhere:

```java
public class DriverHolder {
    private static WebDriver driver;

    public static WebDriver start(String browser) {
        driver = DriverFactory.createDriver(browser);
        return driver;
    }

    public static WebDriver get() {
        if (driver == null) {
            throw new IllegalStateException("Driver not started. Call start() first.");
        }
        return driver;
    }

    public static void stop() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }
}
```

`stop()` quits *and* sets the variable back to `null`, so a second `stop()` call is harmless. (This simple version supports one browser at a time. Running tests in parallel needs a more careful design, which is a later framework topic.)

### 8. Where to Store the Driver in a Framework

With Selenium Manager you do not store drivers at all. If you must store manually-managed drivers:

```
project-root/
 ├── drivers/            <- chromedriver.exe, geckodriver.exe (do NOT commit large binaries to Git if avoidable)
 ├── src/
 └── pom.xml
```

Resolve the path *relative to the project*:

```java
String driverPath = System.getProperty("user.dir") + "/drivers/chromedriver.exe";
System.setProperty("webdriver.chrome.driver", driverPath);
```

`user.dir` is the working directory (the project root when run from Maven or an IDE). `System.getProperty("user.dir")` is a built-in JVM property, so it needs no setup. Concatenating it with `/drivers/...` yields an absolute path that is correct on whichever machine runs the code (with `/` accepted on Windows by Java).

### 9. Cross-Platform Notes

- On Windows the driver file ends in `.exe`; on macOS/Linux there is no extension and the file must be executable (`chmod +x chromedriver`).
- Safari requires you to enable *Develop → Allow Remote Automation* once on macOS.
- On Linux servers without a display, you need a headless browser (see *Browser Options*).
- On macOS, a downloaded driver may be blocked by Gatekeeper ("cannot be opened because the developer cannot be verified"). Selenium Manager's downloads avoid this in most cases; for manual downloads you may need to approve the file in System Settings.

---

## Troubleshooting Guide

| Error message (shortened) | Likely cause | What to do |
|---|---|---|
| `session not created: This version of ChromeDriver only supports Chrome version N` | Driver/browser mismatch | Remove any manual `webdriver.chrome.driver` setting so Selenium Manager chooses the right one; update Selenium to a current 4.x. |
| `Unable to obtain driver using Selenium Manager` / timeout downloading | No internet, proxy, firewall | Configure the proxy (see the Selenium Manager documentation for proxy options), or download the driver manually and use Option A/B. |
| `cannot find Chrome binary` | Chrome not installed or in a non-standard folder | Install Chrome, or specify the binary in `ChromeOptions` (next lessons). |
| `Permission denied` running the driver (macOS/Linux) | Driver file not executable | `chmod +x path/to/chromedriver`. |
| Browser opens, then immediately closes | `quit()` called too early, or an exception and no wait | Check your flow; read the stack trace. |
| Many `chromedriver.exe` processes left in Task Manager | `quit()` not executed | Use `try/finally` or teardown hooks. |

### Troubleshooting walk-through A: stale pinned driver

Symptom in the build log:

```
org.openqa.selenium.SessionNotCreatedException: Could not start a new session.
Response code 500. Message: session not created: This version of ChromeDriver only supports Chrome version 124
Current browser version is 126.0.6478.127
```

Diagnosis, step by step:

1. `SessionNotCreatedException` tells us the failure was while creating the session (the `POST /session` step), so the driver *did* start.
2. The message gives two numbers: driver supports 124, browser is 126. Mismatch confirmed.
3. Selenium Manager would never choose a 124 driver for a 126 browser, so something overrode it. Search the repository for `webdriver.chrome.driver`, for `usingDriverExecutable`, and check the machine's `PATH` for an old `chromedriver`.
4. Found: a `System.setProperty` line in an old utility class. Delete it. Re-run. The test passes, and Selenium Manager downloads the right driver.

### Troubleshooting walk-through B: works at home, fails at work

Symptom:

```
org.openqa.selenium.WebDriverException: Unable to obtain: Capabilities {browserName: chrome}, ...
Selenium Manager ... error sending request ... connection timed out
```

1. The words "Selenium Manager" and "timed out" point to the download step, not to your test logic.
2. Open `https://googlechromelabs.github.io/chrome-for-testing/` in a browser on the same machine. If it needs a proxy or is blocked, that confirms the network is at fault.
3. Short-term fix: have IT whitelist the download hosts or provide the proxy settings; or download the matching chromedriver by hand once and use Option A or B.
4. Long-term fix: ask the team to put an approved driver on a shared location, and read its path from a config file or `-D` property so no code change is needed on each machine.

### Troubleshooting walk-through C: `Permission denied` on Linux

Symptom:

```
java.io.IOException: Cannot run program "/home/dev/drivers/chromedriver": error=13, Permission denied
```

1. `Cannot run program ... error=13` is an operating-system message: the file exists (otherwise it would say "No such file") but is not executable.
2. Check with `ls -l /home/dev/drivers/chromedriver`. If the permissions lack an `x`, that is the cause.
3. Fix: `chmod +x /home/dev/drivers/chromedriver`.

### Troubleshooting walk-through D: "no such file" with a path that looks right

Symptom:

```
java.lang.IllegalStateException: The driver executable does not exist: C:\drivers\chromedriver.exe
```

1. The message is explicit: the file is not at that path. Do not assume your eyes are right; paste the path into File Explorer.
2. Typical causes: the file is still inside the downloaded `.zip` (not unzipped), it is in a sub-folder (`chromedriver-win64\chromedriver.exe`), or a `\` was typed instead of `\\` in the Java string.
3. Fix the path, or better, switch to the `user.dir`-relative approach so the path is portable.

---

## Guided Lab: Build and Test Your DriverFactory

**Goal:** create the first reusable class of your framework and prove it picks the browser from a setting.

**Step 1.** In your `selenium-basics` project from the Architecture lesson, create the package `com.revature.qea.drivers` and the class `DriverFactory` exactly as shown in section 7 (use the classic `switch` first).

**Step 2.** Create `src/main/java/com/revature/qea/FactoryDemo.java`:

```java
package com.revature.qea;

import com.revature.qea.drivers.DriverFactory;
import org.openqa.selenium.WebDriver;

public class FactoryDemo {

    public static void main(String[] args) {
        String browser = System.getProperty("browser", "chrome");
        System.out.println("Starting browser: " + browser);

        WebDriver driver = DriverFactory.createDriver(browser);
        try {
            driver.get("https://the-internet.herokuapp.com/");
            System.out.println("Title: " + driver.getTitle());
        } finally {
            driver.quit();
            System.out.println("Browser closed.");
        }
    }
}
```

**What this does:** reads the browser name (default `chrome`), asks the factory for a driver, opens the-internet, prints the title, and always quits.

**Step 3.** Run it with no arguments. **Expected output:**

```
Starting browser: chrome
Title: The Internet
Browser closed.
```

**Step 4.** In IntelliJ: *Run | Edit Configurations | VM options*, add `-Dbrowser=firefox` (or `edge`), and run again. **Expected output:** `Starting browser: firefox`, then the same title, and a Firefox window this time.

**Step 5.** Run with `-Dbrowser=safari`. **Expected output:** an `IllegalArgumentException` with the message `Unsupported browser: 'safari'. Use chrome, firefox or edge.` and **no browser window** (the factory throws before any browser starts, which is the whole point of failing fast).

**Step 6.** Optional upgrade: replace the classic `switch` with the `switch` expression from the variations, re-run steps 3 to 5, and confirm that behaviour is identical. Refactoring means changing structure without changing behaviour; repeating the same checks is how you know you did not break anything.

**Step 7.** Reflect: write two sentences in your notes explaining how this factory will help in Project 2.

---

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Leaving an old `System.setProperty("webdriver.chrome.driver", ...)` in code | Overrides Selenium Manager and causes mismatches after browser updates | Remove it unless you truly need a pinned driver |
| Typing `"C:\drivers\chromedriver.exe"` with a single backslash | Java reads `\d` as an invalid escape: compile error | Use `\\` or forward slashes |
| Forgetting `quit()` on the failure path | Zombie processes | `try/finally` |
| Calling `new ChromeDriver()` all over the tests | Browser change means editing everything | Use the factory |
| Returning `ChromeDriver` from the factory | Locks callers to Chrome | Return `WebDriver` |
| Using `close()` as the final cleanup | Driver process may stay alive | Use `quit()` |
| Committing driver binaries to Git | Bloats the repository; goes stale | Use Selenium Manager |

---

## Practice Exercises

1. **Three browsers.** Run the `DriverBasics` example with whichever two browsers you have installed. Record the time of the first run vs. the second run for the same browser. Why is the second run faster?
2. **Find the cache.** Locate the folder where Selenium Manager stored the driver on your machine (`%USERPROFILE%\.cache\selenium` on Windows). What files are in there?
3. **Build the factory.** Create `DriverFactory` exactly as shown, then write a `main` method that reads the browser name from `System.getProperty("browser", "chrome")`. Run it from the IDE (set a VM option `-Dbrowser=edge`) and from Maven.
4. **Defensive test.** Call `DriverFactory.createDriver("crome")` (typo). Confirm that you get your helpful exception message.
5. **Manual mode.** Download chromedriver manually, store it in a `drivers/` folder, and configure it using `System.setProperty`. Then delete the property line and confirm that Selenium Manager takes over again.
6. **Think question:** Why is `quit()` better placed in a `finally` block than at the last line of `main`?
7. **Service builder.** Start Chrome using `ChromeDriverService.Builder()` with `.withLogFile(...)`. Open the log file and find the line that shows the port chromedriver listens on.
8. **Case-insensitive input.** Test the factory with `"CHROME"` and `" Firefox "`. Do both work? Explain which line of the factory makes this possible.
9. **Enum version.** Convert the factory to the `enum Browser` version and add a helper `static Browser fromString(String s)` that returns the right constant or throws an `IllegalArgumentException`.
10. **Lifecycle test.** Write code that calls `driver.quit()` and then `driver.getTitle()`. Run it, copy the exception name, and explain in one sentence why it is thrown.
11. **Edge-case design.** The factory currently ignores `safari`. List what you would need to add to support it (class to import, platform restriction, setting on the Mac).
12. **Scenario.** Chrome updated on the CI server overnight and 120 tests failed. List three possible root causes in order of likelihood and the command or search you would use to confirm each.

---

## Solutions and Hints

**1.** The first run includes Selenium Manager downloading the driver; later runs use the cached copy, so they skip the download.

**2.** Expect a `chromedriver` folder containing platform/version sub-folders with the executable, plus `se-metadata.json`.

**3.** Hint: IntelliJ's *Run | Edit Configurations | VM options* field takes `-Dbrowser=edge`. From a terminal: `java -Dbrowser=edge -cp ... com.revature.qea.FactoryDemo` (or the equivalent Maven `exec` command if configured).

**4.** The output should read `IllegalArgumentException: Unsupported browser: 'crome'. Use chrome, firefox or edge.`

**5.** After deleting `System.setProperty`, the test still passes because Selenium Manager resolves the driver again. If it fails, check that you did not leave a driver on the `PATH`.

**6.** If an exception is thrown in the middle of `main`, the last line never runs and the browser leaks. `finally` always runs.

**7.**

```java
ChromeDriverService service = new ChromeDriverService.Builder()
        .withLogFile(new java.io.File("chromedriver.log"))
        .withVerbose(true)
        .build();
WebDriver driver = new ChromeDriver(service);
try {
    driver.get("https://www.saucedemo.com");
} finally {
    driver.quit();
}
```

Search the log for `Starting ChromeDriver` and `port`; the line lists the port number.

**8.** Yes. `browserName.trim().toLowerCase()` removes spaces and lowercases the text before the `switch`.

**9.**

```java
public enum Browser {
    CHROME, FIREFOX, EDGE;

    public static Browser fromString(String s) {
        if (s == null) {
            throw new IllegalArgumentException("Browser name must not be null");
        }
        try {
            return Browser.valueOf(s.trim().toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("Unsupported browser: '" + s + "'");
        }
    }
}
```

**10.** `NoSuchSessionException` (or a `WebDriverException` mentioning an invalid session id): after `quit()` the session ID no longer exists on the driver side, so any request carrying it is rejected.

**11.** Import `org.openqa.selenium.safari.SafariDriver`, add `case "safari": return new SafariDriver();`, make sure it only runs on macOS, and enable *Develop > Allow Remote Automation* in Safari.

**12.** (1) Stale pinned driver: search for `webdriver.chrome.driver` and `usingDriverExecutable`. (2) Old driver on the `PATH`: `where chromedriver` (Windows) or `which chromedriver` (macOS/Linux). (3) Selenium version older than 4.6 (so no Selenium Manager): check the `pom.xml`, or run `mvn dependency:tree | grep selenium`.

---

## Self-Check Q&A

1. **Why must driver and browser versions match?** The driver is built against specific browser internals; browsers change often, so mismatches fail or misbehave.
2. **Which takes precedence: a configured driver path or Selenium Manager?** The configured path. Selenium Manager runs only when none is set.
3. **Where does Selenium Manager keep downloaded drivers?** In `~/.cache/selenium` (Windows: `%USERPROFILE%\.cache\selenium`).
4. **When would you use `ChromeDriverService`?** When you need per-instance control, such as a specific executable, port or log file.
5. **Difference between `close()` and `quit()`?** `close()` closes one window; `quit()` closes all windows and ends the session and driver process.
6. **Why should a factory return `WebDriver` and not `ChromeDriver`?** So callers depend on the interface and any browser can be swapped in.
7. **Why throw an exception for an unknown browser name?** To fail fast with a clear message rather than start the wrong browser or hit a `NullPointerException` later.

---

## Summary

- A **browser driver** is the translator between Selenium and a specific browser; versions must match.
- **Selenium Manager** (Selenium 4.6+) detects your browser and downloads/caches the correct driver automatically; `new ChromeDriver()` is usually all you need.
- An explicitly configured driver always wins over Selenium Manager, so stale manual settings are a classic cause of mismatch errors.
- Manual configuration (`System.setProperty("webdriver.chrome.driver", ...)` or `ChromeDriverService`) is still needed for offline or pinned-version situations.
- `close()` closes one window; `quit()` ends the session and the driver process. Use `quit()` for cleanup, inside `finally`.
- Centralize driver creation in a **`DriverFactory`** so tests do not depend on a specific browser; select the browser with a `-Dbrowser=...` system property.
- Most "driver" errors are version, path, permission, or network problems; the error message usually says which. Read it, name the layer, then fix.

---

## Additional Resources

- Selenium documentation, *Driver Requirements*: https://www.selenium.dev/documentation/webdriver/troubleshooting/drivers/ (and the *Getting started → Install a Selenium library* pages)
- Selenium documentation, *Selenium Manager*: https://www.selenium.dev/documentation/selenium_manager/
- ChromeDriver official site: https://developer.chrome.com/docs/chromedriver
- Practice sites used this week: https://www.saucedemo.com and https://the-internet.herokuapp.com
