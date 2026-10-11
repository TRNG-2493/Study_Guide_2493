# Browser Options

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **capabilities** and **Options classes** are, why they exist, and how they connect to the session request you saw in the architecture lesson.
- Configure `ChromeOptions`, `FirefoxOptions`, and `EdgeOptions`.
- Run tests in **headless** mode, explain when to use it, and avoid its classic pitfalls.
- Use common arguments: `--start-maximized`, `--window-size`, `--incognito`, `--disable-notifications`, `--disable-popup-blocking`, `--ignore-certificate-errors`, and others, and say what each is for.
- Set the **page load strategy** and **timeouts**, and choose between them with confidence.
- Use browser **preferences** (for example, a default download folder and turning off the password manager).
- Specify a non-default browser binary.
- Read and diagnose typical option-related errors (unknown argument, wrong option class, driver not reachable).
- Extend the `DriverFactory` from the *Driver Configuration* lesson to pass options and choose headless mode from a command-line flag.

---

## Why This Matters

A browser you launch with no configuration is a *general-purpose consumer browser*. It shows "Save password?" prompts, "Allow notifications?" pop-ups, "Chrome is being controlled by automated software" bars, first-run dialogs, and it keeps cookies from previous sessions. Each of those can intercept clicks, cover elements, or change what the page does, and all of them make tests unreliable.

Think of the difference between **cooking in your own messy kitchen** and **cooking in a lab kitchen**. At home, the counter has yesterday's dishes, the radio is on, and the oven is already warm from someone else. In a lab kitchen, every surface is cleared and every setting is known before you start. Test engineers need the lab kitchen: they **launch browsers in a controlled, repeatable state** so that a result today can be compared with a result next week.

They also need to run the same tests on a build server (CI, "continuous integration") that has no monitor, where the only choice is a **headless** browser. Options are how you do all of that.

**A real scenario.** A team's tests passed on every developer laptop but failed every night on the CI server with `ElementClickInterceptedException`. Screenshots (next lessons) showed a "Save your password?" bubble covering the login button, but only on the server, where a fresh browser profile had no history of the user dismissing it. One line in the options (disabling the password manager) fixed the entire suite. That is the value of options: *the same browser state everywhere*.

In **Project 2**, your framework's driver factory will accept options so that tests run the same way on every laptop and on the CI pipeline. This week's Epic (a Selenium framework with BDD) depends on that: when the Cucumber scenarios you write on Thursday and Friday start a browser, they will ask your `DriverFactory` for it.

---

## The Concept

### 1. Capabilities and Options

**What are capabilities?** When Selenium starts a browser session (`POST /session`, see the architecture lesson), it sends a set of **capabilities**: a JSON object that describes the requested browser (name, version, platform) and its settings. It is like a *booking form* for a hotel room: "one room, non-smoking, sea view, late check-out". The driver reads the form and prepares the browser accordingly.

A tiny example of such JSON:

```json
{
  "capabilities": {
    "alwaysMatch": {
      "browserName": "chrome",
      "pageLoadStrategy": "normal",
      "acceptInsecureCerts": false,
      "goog:chromeOptions": { "args": ["--start-maximized"] }
    }
  }
}
```

**What is an Options class?** In Selenium 4 you do not build that JSON by hand. You use a browser-specific **Options class**: a Java class with friendly methods that, behind the scenes, fills in the JSON for you. You call methods such as `addArguments(...)`; Selenium converts your choices into the correct capability keys.

| Browser | Options class | Package |
|---|---|---|
| Chrome | `ChromeOptions` | `org.openqa.selenium.chrome` |
| Firefox | `FirefoxOptions` | `org.openqa.selenium.firefox` |
| Edge | `EdgeOptions` | `org.openqa.selenium.edge` |
| Safari | `SafariOptions` | `org.openqa.selenium.safari` |

**Why browser-specific?** Capabilities that every browser understands (for example `pageLoadStrategy` or `acceptInsecureCerts`) are defined by the W3C WebDriver standard. But each browser also has **vendor-specific** features (Chrome's `prefs`, Firefox's `about:config` preferences). Those live in vendor-prefixed keys such as `goog:chromeOptions` and `moz:firefoxOptions`. Each Options class knows its own browser's vendor keys.

Pattern: **create options, configure them, pass them into the driver constructor**:

```java
ChromeOptions options = new ChromeOptions();      // 1. create
options.addArguments("--start-maximized");         // 2. configure
WebDriver driver = new ChromeDriver(options);      // 3. pass to the driver
```

What happens when line 3 runs:

1. Selenium turns the `ChromeOptions` object into the capabilities JSON.
2. Selenium Manager (from the Driver Configuration lesson) finds or downloads the matching `chromedriver`.
3. `chromedriver` starts, receives `POST /session` with your JSON, and launches Chrome with the arguments you provided.
4. You get back a `ChromeDriver` already pointed at that configured browser.

The key lesson: **options only take effect if you pass them in at construction time.** Creating a `ChromeOptions` object and then calling `new ChromeDriver()` (with empty parentheses) silently ignores everything you set. Most beginners make this mistake once.

### 2. Command-Line Arguments

**What they are.** Chrome, Edge (which is Chromium-based, so it behaves like Chrome), and Firefox accept command-line *arguments* (also called *switches* or *flags*) that change the browser's behaviour at launch. If you have ever started a program by typing `chrome.exe --incognito`, these are the same switches. You supply them with `addArguments(...)`, which accepts one or many strings:

```java
options.addArguments("--incognito");
options.addArguments("--incognito", "--start-maximized");   // several at once
```

**Frequently used Chrome/Edge arguments**

| Argument | Effect | When to use |
|---|---|---|
| `--start-maximized` | Opens the window maximized | Headed runs where layout matters |
| `--window-size=1920,1080` | Sets a precise window size (important in headless mode) | Headless, or any run needing consistent screenshots |
| `--headless=new` | Runs without a visible window | CI servers, Docker |
| `--incognito` | Private session: no leftover cookies/cache between runs | When you need a clean, no-history state |
| `--disable-notifications` | Suppresses "Allow notifications?" prompts | Sites that ask for notification permission |
| `--disable-popup-blocking` | Lets pop-up windows open | Tests that deliberately open new windows (Wednesday) |
| `--disable-extensions` | Starts without extensions | Avoid interference from installed extensions |
| `--ignore-certificate-errors` | Accepts invalid/self-signed SSL certificates | Internal test environments |
| `--disable-infobars` | Hides some info bars (partly obsolete in recent versions) | Older Chrome versions |
| `--lang=en-US` | Forces the browser language so text locators are predictable | Tests that find elements by visible text |
| `--no-sandbox` | Needed in some Linux container/CI environments (running as root); **security-reducing, use only when required** | Specific Docker/CI setups |
| `--disable-dev-shm-usage` | Avoids crashes in Docker where `/dev/shm` is tiny | Docker containers |
| `--remote-allow-origins=*` | Seen in some Chrome 111+ setups with older Selenium; usually unnecessary with current Selenium | Rare; only with old client libraries |

**Why each category exists.**

- *Appearance and size* (`--start-maximized`, `--window-size`): layouts on responsive sites change with width. A page at 800 pixels wide may hide the menu behind a "hamburger" icon, and your locator then finds nothing.
- *Interruptions* (`--disable-notifications`, `--disable-popup-blocking`, the password manager preference later): these remove things that appear in front of the page.
- *Cleanliness* (`--incognito`): removes state left by earlier runs.
- *Environment* (`--no-sandbox`, `--disable-dev-shm-usage`, `--headless=new`): make browsers work on servers.

**Firefox arguments**

```java
FirefoxOptions options = new FirefoxOptions();
options.addArguments("-headless");              // note: single dash for Firefox
options.addArguments("--width=1920");
options.addArguments("--height=1080");
```

Firefox uses a single dash for `-headless` and separate `--width` and `--height` arguments instead of Chrome's combined `--window-size`. When you move between browsers, **do not copy argument names**; each browser has its own.

**What happens with a wrong argument?** Chrome silently ignores most unknown switches, which makes typos hard to notice. If your option "does nothing", first check spelling character by character. A quick way to prove that an argument was applied: open `chrome://version` in the controlled browser and read the "Command Line" row, which lists every argument the browser was started with.

```java
driver.get("chrome://version");
```

### 3. Headless Mode

**What it is.** **Headless** means the browser runs without displaying a window. Everything else works the same: pages load, JavaScript runs, elements can be clicked, screenshots can be taken. The metaphor is a "headless" computer server: it has no monitor but still does all the work.

```java
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless=new");
options.addArguments("--window-size=1920,1080");
WebDriver driver = new ChromeDriver(options);
```

**Why use headless?**

- CI/CD servers (Jenkins, GitHub Actions) have no screen. A normal browser cannot start there.
- It is faster and uses fewer resources than a visible browser, which matters when a suite has hundreds of tests.
- No stolen focus: you can keep working on your laptop while tests run. (A visible browser pops to the front and steals your keystrokes!)

**When to use headed versus headless.**

| Situation | Choice |
|---|---|
| Writing and debugging a new test | Headed (watch it) |
| Investigating a failure | Headed, then screenshots |
| Nightly or pull-request pipeline | Headless |
| Running many tests in parallel on one machine | Headless |
| Final check before demo | Headed |

**Cautions:**

- **Set the window size.** A headless browser's default window can be small, causing responsive layouts to hide elements. `maximize()` does nothing without a display.
- Some rare behaviors differ between headless and headed. When debugging a failing test, run it headed so you can watch.
- Naming history: Chrome 109 introduced a rebuilt headless mode selected with `--headless=new`, while the older implementation was called "old headless" and was a different, reduced browser. In recent Chrome releases the new implementation became the default meaning of `--headless`, and the old one moved to a separate "chrome-headless-shell" program. Writing `--headless=new` works on both older and recent versions, so it is a safe choice in this course.

**Troubleshooting walk-through: "My test passes headed but fails headless."**

Symptom: `NoSuchElementException` for the shopping cart link, only in headless runs.

1. Add `System.out.println(driver.manage().window().getSize());` before the failing step. Output `(800, 600)` suggests a small default window.
2. A width of 800 may trigger the mobile layout, where the cart is hidden inside a menu.
3. Fix: add `--window-size=1920,1080`.
4. Confirm by re-running and taking a screenshot (next lesson) to see the layout.

### 4. Timeouts and Page Load Strategy

**What it is.** When you call `driver.get(url)`, Selenium waits until the browser reports that the page has loaded. The **page load strategy** decides *what counts as loaded*. Options can control it:

```java
import org.openqa.selenium.PageLoadStrategy;

ChromeOptions options = new ChromeOptions();
options.setPageLoadStrategy(PageLoadStrategy.EAGER);
```

| Strategy | Selenium returns from `get()` when... | Use when |
|---|---|---|
| `NORMAL` (default) | The `load` event fires (all resources loaded) | Most tests |
| `EAGER` | The DOM is ready (`DOMContentLoaded`); images/styles may still load | Pages with slow third-party resources (ads, trackers, analytics) |
| `NONE` | Immediately after the navigation starts | Advanced; you must wait yourself |

**Analogy.** Imagine ordering a pizza. `NORMAL` means "I am ready when the pizza, the drinks and the dessert have all arrived". `EAGER` means "I am ready when the pizza arrives; the dessert can come later". `NONE` means "I am ready the moment the order is placed", and now you have to check yourself whether the pizza is there.

**Choosing.** Start with `NORMAL`. If a page loads quickly but `get()` takes forever because of a slow advertisement or tracking script, `EAGER` is a good fix. Use `NONE` only after you have learned explicit waits on Tuesday, because with `NONE` your next `findElement` may run before anything exists.

**Timeouts** are set on the driver after creation (they are *session* settings rather than browser options):

```java
driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
driver.manage().timeouts().scriptTimeout(Duration.ofSeconds(20));
// The implicit wait timeout is introduced on Tuesday together with the other waits.
```

- `pageLoadTimeout`: the maximum time `get()` (or a click that triggers navigation) may take before Selenium throws `TimeoutException`. The default is 300 seconds (5 minutes), which is far too long for a test; a failing page would stall your build for minutes. 30 to 60 seconds is typical.
- `scriptTimeout`: the maximum time an asynchronous JavaScript snippet may run. Rarely needed by beginners.

`Duration` comes from `java.time.Duration`; do not forget the import. You can also set timeouts through options (`options.setPageLoadTimeout(Duration.ofSeconds(30))`), which applies them from the very first command.

**What the failure looks like:**

```
org.openqa.selenium.TimeoutException: timeout: Timed out receiving message from renderer: 30.000
```

This tells you the page did not finish loading in time. Diagnose by opening the same URL manually and checking whether it is slow; then consider `EAGER` or a longer timeout.

### 5. Browser Preferences (Chrome Example: Download Folder)

**What they are.** Some settings are not command-line flags but **preferences**, stored as key/value pairs (the same ones you see in the browser's settings page). For example, to download files without a prompt into a folder of your choice:

```java
import java.util.HashMap;
import java.util.Map;

Map<String, Object> prefs = new HashMap<>();
prefs.put("download.default_directory", "C:\\temp\\downloads");
prefs.put("download.prompt_for_download", false);
prefs.put("credentials_enable_service", false);       // disable "save password" bubble
prefs.put("profile.password_manager_enabled", false);

ChromeOptions options = new ChromeOptions();
options.setExperimentalOption("prefs", prefs);
```

Line by line:

- `Map<String, Object> prefs = new HashMap<>();` creates a dictionary-like collection: each *key* (a preference name) is a `String`, each *value* can be a string, boolean or number, hence `Object`.
- `prefs.put(key, value)` adds one preference. Chrome names are dotted paths such as `download.default_directory`.
- `download.prompt_for_download = false` tells Chrome to save straight to the folder instead of showing a "Save as" dialog (which Selenium cannot control, because it is an operating-system dialog, not a web page).
- The two password settings stop the "Save password?" bubble.
- `setExperimentalOption("prefs", prefs)` hands the whole map to Chrome. The word "experimental" does not mean unstable; it is simply the name Selenium uses for Chrome-specific extras that are not W3C standard.

Notes:

- The Windows path needs doubled backslashes in a Java string; better, build it with `Paths.get(...)` for portability (see the example below).
- The "Save password / password leak" bubble is a frequent real-world disrupter on sites like SauceDemo; disabling the password manager removes it.
- Chrome needs an **absolute** path for the download directory, and the folder should exist.

A portable download folder:

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

Path downloadDir = Paths.get(System.getProperty("user.dir"), "target", "downloads");
Files.createDirectories(downloadDir);                         // throws IOException
prefs.put("download.default_directory", downloadDir.toAbsolutePath().toString());
```

`System.getProperty("user.dir")` is the folder you run Maven from (your project root), so the same code works on Windows, macOS, Linux, and CI. Storing downloads under `target/` means `mvn clean` removes them automatically.

For Firefox, you use `FirefoxProfile` or `options.addPreference(...)`:

```java
FirefoxOptions ff = new FirefoxOptions();
ff.addPreference("browser.download.folderList", 2);       // 2 = use a custom folder
ff.addPreference("browser.download.dir", downloadDir.toAbsolutePath().toString());
ff.addPreference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,text/plain");
```

Firefox preference names are the ones you would see on the `about:config` page.

### 6. Excluding the "Automation" Banner and Switches

```java
options.setExperimentalOption("excludeSwitches", new String[]{"enable-automation"});
```

By default, Selenium launches Chrome with an `enable-automation` switch that shows the "Chrome is being controlled by automated test software" bar. This line removes that switch. It is cosmetic and optional, but some pages mis-render around the bar (it pushes the page down a few pixels), and some sites behave differently when they detect automation. Note that you should not use this to hide automation from sites you do not own; it is for tidying your own test runs.

### 7. Using a Specific Browser Binary

If Chrome is installed in a non-standard place, or you want to test a specific build (Chrome for Testing, Chrome Beta):

```java
options.setBinary("C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe");
```

Selenium Manager (see *Driver Configuration*) will then match the driver to *that* binary's version. This is useful when your company laptop has an outdated Chrome you are not allowed to update, or when you want to test against the upcoming Beta release before your users get it.

Typical error when the path is wrong:

```
org.openqa.selenium.SessionNotCreatedException: session not created: probably user data directory is already in use...
```

or

```
org.openqa.selenium.WebDriverException: unknown error: cannot find Chrome binary
```

Diagnosis: print `new File(path).exists()` and fix the path. On Linux and macOS use forward slashes.

### 8. Accepting Insecure Certificates

Internal test environments often use self-signed HTTPS certificates. Chrome shows "Your connection is not private" and blocks the page, so your `findElement` calls look at a warning page and fail. Two equivalent ways:

```java
options.setAcceptInsecureCerts(true);               // W3C standard capability (works across browsers)
options.addArguments("--ignore-certificate-errors"); // Chrome/Edge argument
```

Prefer `setAcceptInsecureCerts(true)` because it is a standard and works the same in Firefox. Use this only for **test** environments, never to hide certificate issues on production tests where certificates are part of what you verify.

### 9. Mobile Emulation (Brief Mention)

Chrome can emulate a phone's screen and user agent to test responsive designs:

```java
Map<String, String> mobile = new HashMap<>();
mobile.put("deviceName", "iPhone 12 Pro");
options.setExperimentalOption("mobileEmulation", mobile);
```

This is not a replacement for testing on real devices, but is a quick check of layout. It makes the page believe it is on a phone (narrow screen, touch events, mobile user-agent string), so mobile-specific menus appear. The `deviceName` must be one that exists in Chrome DevTools' device list.

### 10. Putting It Together: An Options-Aware `DriverFactory`

Here is the extension of the factory from *Driver Configuration*. It reads two system properties (`browser` and `headless`) and creates a correctly configured driver:

```java
package com.revature.qea.drivers;

import org.openqa.selenium.PageLoadStrategy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

public class DriverFactory {

    private DriverFactory() { }

    public static WebDriver createDriver(String browserName, boolean headless) {
        WebDriver driver;

        switch (browserName.trim().toLowerCase()) {
            case "chrome":
                driver = new ChromeDriver(chromeOptions(headless));
                break;
            case "firefox":
                driver = new FirefoxDriver(firefoxOptions(headless));
                break;
            case "edge":
                driver = new EdgeDriver(edgeOptions(headless));
                break;
            default:
                throw new IllegalArgumentException("Unsupported browser: " + browserName);
        }

        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(30));
        if (!headless) {
            driver.manage().window().maximize();
        }
        return driver;
    }

    private static ChromeOptions chromeOptions(boolean headless) {
        ChromeOptions options = new ChromeOptions();
        options.setPageLoadStrategy(PageLoadStrategy.NORMAL);
        options.addArguments("--disable-notifications", "--lang=en-US");

        Map<String, Object> prefs = new HashMap<>();
        prefs.put("credentials_enable_service", false);
        prefs.put("profile.password_manager_enabled", false);
        options.setExperimentalOption("prefs", prefs);

        if (headless) {
            options.addArguments("--headless=new", "--window-size=1920,1080");
        }
        return options;
    }

    private static FirefoxOptions firefoxOptions(boolean headless) {
        FirefoxOptions options = new FirefoxOptions();
        if (headless) {
            options.addArguments("-headless", "--width=1920", "--height=1080");
        }
        return options;
    }

    private static EdgeOptions edgeOptions(boolean headless) {
        EdgeOptions options = new EdgeOptions();
        options.addArguments("--disable-notifications");
        if (headless) {
            options.addArguments("--headless=new", "--window-size=1920,1080");
        }
        return options;
    }
}
```

**Usage:**

```java
String browser  = System.getProperty("browser", "chrome");
boolean headless = Boolean.parseBoolean(System.getProperty("headless", "false"));
WebDriver driver = DriverFactory.createDriver(browser, headless);
```

Run from a terminal:

```
mvn test -Dbrowser=chrome -Dheadless=true
```

**Explanation, line by line:**

- `private DriverFactory() { }`: a private constructor stops anyone from writing `new DriverFactory()`; the class only has static methods.
- `switch (browserName.trim().toLowerCase())`: `trim()` removes accidental spaces, `toLowerCase()` makes `Chrome`, `CHROME`, and `chrome` all work. The `switch` jumps to the matching `case`; each `break` prevents "fall through" into the next case.
- `default: throw new IllegalArgumentException(...)` fails fast with a clear message when someone passes `-Dbrowser=opera`, instead of returning `null` and causing a confusing `NullPointerException` later.
- Each browser has a private helper method creating its own options object, keeping the `switch` short and readable.
- `driver.manage().timeouts().pageLoadTimeout(...)`: a safety net so no page load can stall the build for 5 minutes.
- Headless runs set a fixed window size; headed runs maximize.
- `System.getProperty("browser", "chrome")` reads a value given with `-Dbrowser=...`, or the default `chrome` if none was given. `Boolean.parseBoolean("true")` converts the text into a real `boolean`; any text other than `true` (ignoring case) becomes `false`.
- Defaults (`chrome`, `false`) make "just run it" work, while a CI pipeline overrides with `-D` flags.

**Why a factory?** If options were scattered across fifty test classes, changing one setting would mean fifty edits. In one place, one edit changes everything. This is the single-responsibility idea you will rely on all week: the Cucumber hooks you build on Friday will simply call `DriverFactory.createDriver(...)` and never mention an option.

**A note on `mvn test -D...`.** For `-D` flags to reach your Java code, the Maven Surefire plugin passes system properties from the Maven command line to the test JVM. In most standard setups this works automatically. If your property seems to be ignored, check that you spelled it the same in the command and in `System.getProperty`.

---

## Code Example: A Quick Options Demo

```java
package com.revature.qea.options;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.HashMap;
import java.util.Map;

public class OptionsDemo {
    public static void main(String[] args) {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--incognito", "--start-maximized", "--disable-notifications");
        options.setAcceptInsecureCerts(true);

        Map<String, Object> prefs = new HashMap<>();
        prefs.put("credentials_enable_service", false);
        prefs.put("profile.password_manager_enabled", false);
        options.setExperimentalOption("prefs", prefs);

        WebDriver driver = new ChromeDriver(options);
        try {
            driver.get("https://www.saucedemo.com");
            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.id("password")).sendKeys("secret_sauce");
            driver.findElement(By.id("login-button")).click();
            System.out.println("Landed on: " + driver.getCurrentUrl());
        } finally {
            driver.quit();
        }
    }
}
```

**Explanation:**

- The first three lines in `main` build the options object; no browser exists yet.
- `addArguments` accepts several strings at once (it is a "varargs" method).
- `setAcceptInsecureCerts(true)` is harmless on SauceDemo but shows the call.
- The `prefs` map turns off the password manager; on SauceDemo's inventory page Chrome would otherwise sometimes show a "Change your password" breach warning that covers part of the page.
- `new ChromeDriver(options)` is the moment everything takes effect.
- The remaining lines are the login flow you already know from the Find Methods lesson. `getCurrentUrl()` should print `https://www.saucedemo.com/inventory.html`.

**Expected output:**

```
Landed on: https://www.saucedemo.com/inventory.html
```

---

## Guided Lab: Prove Your Options Work (30 minutes)

**Goal:** apply options and prove with evidence (not guesswork) that each one took effect.

**Steps:**

1. Create `OptionsLab.java` in `src/test/java/com/revature/qea/options/` with a `main` method.
2. Build `ChromeOptions` with `--headless=new` and `--window-size=1280,720`.
3. Create the driver, then print `driver.manage().window().getSize()`. **Expected:** about `(1280, 720)`. If it prints `(800, 600)`, the argument was not applied (check spelling and that you passed `options` to the constructor).
4. Navigate to `https://www.saucedemo.com`, print the page title. **Expected:** `Swag Labs`.
5. Navigate to `chrome://version` and print `driver.findElement(By.id("command_line")).getText()`. **Expected:** a long line containing `--headless=new` and `--window-size=1280,720`. This proves the arguments reached the browser. (If this element id is not found in your Chrome version, use `driver.getPageSource()` and search it for `window-size`.)
6. Quit, remove `--headless=new`, add `--start-maximized`, run again, and observe the browser window.
7. Add a `download.default_directory` preference pointing to `target/downloads` (build the path with `Paths.get(System.getProperty("user.dir"), "target", "downloads")`). Visit `https://the-internet.herokuapp.com/download`, click the first file link, and wait a few seconds with `Thread.sleep(3000)` (acceptable in a *lab*; Tuesday teaches the proper way). Print the names of files in the folder with `new File(path).list()`.
8. Compare: does the file appear in your folder and not in your normal Downloads? **Expected:** yes.

**Reflection questions:** Which of these steps would fail if you created the options but called `new ChromeDriver()` with no arguments? (All the option-based checks: steps 3, 5, and 7.)

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Headless without window size | Mobile layout, missing elements | Add `--window-size=1920,1080` |
| Using `-headless` for Chrome or `--headless` for Firefox | Argument ignored or error | Chrome/Edge: `--headless=new`; Firefox: `-headless` |
| Creating options but not passing them to the driver | Settings ignored | `new ChromeDriver(options)` |
| Using `--no-sandbox` on a laptop by habit | Reduces browser security unnecessarily | Use only where required (certain Linux/Docker CI setups) |
| Hard-coding download paths like `C:\temp` | Fails on other machines and CI | Build paths from `System.getProperty("user.dir")` or temp dir |
| Using options of one browser class with another driver | Compile error / wrong settings | Match `ChromeOptions` with `ChromeDriver`, etc. |
| Typing a wrong switch name | Silently ignored | Verify at `chrome://version` |
| Relative path for the download directory | Files land in an unexpected place | Use an absolute path |
| Leaving the 5-minute default page load timeout | A bad page stalls the whole run | Set `pageLoadTimeout` to 30-60 s |
| Using `--ignore-certificate-errors` in a test that verifies certificates | Hides a real defect | Use only in test environments |

---

## Practice Exercises

1. **Headless login.** Modify the login script from the previous lesson to run headless. Print the page title and URL after login to prove it worked, even though you cannot see the browser.
2. **Size matters.** Run headless *without* `--window-size`, then with `1920,1080`. Print `driver.manage().window().getSize()` in each case. What differs?
3. **Incognito check.** Log into SauceDemo, quit, run again with and without `--incognito`. Does the site remember you? (Hint: SauceDemo stores the cart in browser storage.)
4. **Download folder.** Set Chrome's download directory to a `downloads` folder under your project, then visit `https://the-internet.herokuapp.com/download`, click a file link, and verify with Java (`java.io.File.exists()`) that the file was downloaded.
5. **Extend the factory.** Add a `"--lang"` argument driven by a system property `lang` (default `en-US`).
6. **Pick the strategy.** Explain in two sentences when you would choose `PageLoadStrategy.EAGER` over `NORMAL`.
7. **Reflect:** list three things a CI server needs that your laptop does not (display? installed browsers? fixed window size?).
8. **Prove the argument.** Start Chrome with `--window-size=1000,700`, then print the window size, and open `chrome://version` to find your argument in the command line.
9. **Page load timeout.** Set `pageLoadTimeout` to 1 second and load `https://www.saucedemo.com`. Catch the `TimeoutException` and print its first line. Then restore a sensible value. What does this teach about default timeouts?
10. **Firefox headless.** Write a method `firefoxHeadless()` that returns a `FirefoxOptions` for headless 1920x1080, and run the SauceDemo login with it (if Firefox is installed).
11. **Config switch.** Add a third system property, `baseUrl`, defaulting to `https://www.saucedemo.com`, and print it. Explain why URLs also belong in configuration rather than in test code.
12. **Insecure cert.** Open `https://self-signed.badssl.com/` (a public demo site with an invalid certificate) first without and then with `setAcceptInsecureCerts(true)`. Compare `driver.getTitle()` in both cases.

---

## Solutions and Hints

**1.** Add `options.addArguments("--headless=new", "--window-size=1920,1080");`, create `new ChromeDriver(options)`, log in, and print `driver.getTitle()` and `driver.getCurrentUrl()`. Expected: title `Swag Labs`, URL ending `/inventory.html`.

**2.** Without the argument the size is often small (for example 800x600); with it you get about 1920x1080. A smaller width can trigger the responsive layout and hide elements. Hint: the printed value may include small differences due to window decorations.

**3.** Without incognito the browser starts with a temporary automation profile anyway, so you may see little difference; the point is to understand that `--incognito` guarantees a fresh state. SauceDemo keeps cart contents in local storage; within one session, add an item, then confirm in a second run that the cart badge is absent when you start fresh.

**4.**

```java
Path dir = Paths.get(System.getProperty("user.dir"), "target", "downloads");
Files.createDirectories(dir);
Map<String, Object> prefs = new HashMap<>();
prefs.put("download.default_directory", dir.toAbsolutePath().toString());
prefs.put("download.prompt_for_download", false);
ChromeOptions options = new ChromeOptions();
options.setExperimentalOption("prefs", prefs);
WebDriver driver = new ChromeDriver(options);
driver.get("https://the-internet.herokuapp.com/download");
driver.findElement(By.cssSelector(".example a")).click();   // first file link
Thread.sleep(3000);                                         // lab only; Tuesday shows proper waiting
System.out.println(Arrays.toString(dir.toFile().list()));
```

Add `throws Exception` to `main` for `Files.createDirectories` and `Thread.sleep`, and `import java.util.Arrays;`.

**5.**

```java
String lang = System.getProperty("lang", "en-US");
options.addArguments("--lang=" + lang);
```

Pass `-Dlang=fr` to test the French UI.

**6.** Choose `EAGER` when a page's own content is ready quickly but the full `load` event is delayed by slow third-party resources such as ads or analytics, so waiting for them only slows the test without adding value.

**7.** Any three: no display (needs headless), browsers and drivers installed or downloadable, fixed and known window size, no interactive prompts, access to the network and test environment, writable folders for reports/screenshots, correct locale and timezone settings.

**8.** `--window-size=1000,700` should print roughly `(1000, 700)`. At `chrome://version`, the "Command Line" row lists the switch.

**9.** With one second the load usually fails with `TimeoutException: timeout: Timed out receiving message from renderer`. Lesson: the default is 300 seconds, so without setting it a broken page would delay failure for five minutes.

**10.**

```java
static FirefoxOptions firefoxHeadless() {
    FirefoxOptions o = new FirefoxOptions();
    o.addArguments("-headless", "--width=1920", "--height=1080");
    return o;
}
```

**11.** `String baseUrl = System.getProperty("baseUrl", "https://www.saucedemo.com");`. URLs belong in configuration because the same tests must run against dev, staging, and production-like environments without changing code.

**12.** Without the option, Chrome shows an interstitial warning page whose title is typically something like "Privacy error". With `setAcceptInsecureCerts(true)` the real page loads and the title is `self-signed.badssl.com`. (Exact titles may vary.)

---

## Self-Check Questions

**Q1. What is the relationship between an Options class and capabilities?**
The Options class is a friendly Java builder that converts your settings into the capabilities JSON sent in the new-session request.

**Q2. You wrote `ChromeOptions options = ...; options.addArguments("--incognito"); WebDriver driver = new ChromeDriver();` and the browser is not incognito. Why?**
The options were never passed to the constructor. Use `new ChromeDriver(options)`.

**Q3. Why must you set a window size in headless mode?**
Headless has no real window to maximize and its default size may be small, triggering responsive layouts that hide elements.

**Q4. What is the difference between `NORMAL` and `EAGER` page load strategies?**
`NORMAL` waits for the `load` event (all resources); `EAGER` returns once the DOM is ready, without waiting for images and styles.

**Q5. Why is `download.prompt_for_download=false` used?**
The "Save as" dialog is an operating-system window that Selenium cannot control, so downloads must go straight to a folder.

**Q6. Which argument spells headless for Firefox?**
`-headless` (single dash).

**Q7. Why centralize options in a `DriverFactory`?**
So every test gets the same configuration and one change updates the entire suite; command-line flags choose browser and mode.

**Q8. When is `--no-sandbox` acceptable?**
Only where required, such as some Linux/Docker CI environments, because it lowers browser security.

---

## Summary

- Browser **Options classes** (`ChromeOptions`, `FirefoxOptions`, `EdgeOptions`) configure the browser session, become the capabilities JSON, and are passed to the driver constructor.
- Common **arguments**: `--headless=new`, `--window-size`, `--start-maximized`, `--incognito`, `--disable-notifications`, `--ignore-certificate-errors`. Each browser has its own spelling; verify at `chrome://version`.
- **Headless** mode is essential for CI; always set a window size with it, and debug headed.
- **Page load strategy** (`NORMAL`, `EAGER`, `NONE`) and **timeouts** control how long Selenium waits for navigation; always replace the 5-minute default page load timeout.
- **Preferences** (`setExperimentalOption("prefs", ...)`) control behaviors such as the download folder and the password manager.
- Use `setAcceptInsecureCerts(true)` and `setBinary(...)` for special environments.
- Centralize all of this in the **`DriverFactory`**, driven by `-Dbrowser` and `-Dheadless` flags, which is the foundation of your Project 2 framework skeleton and of the Cucumber hooks you will write later this week.

---

## Additional Resources

- Selenium documentation, *Browser options*: https://www.selenium.dev/documentation/webdriver/browsers/
- Selenium documentation, *Chrome specific functionality*: https://www.selenium.dev/documentation/webdriver/browsers/chrome/
- Chromium command-line switches reference list: https://peter.sh/experiments/chromium-command-line-switches/
