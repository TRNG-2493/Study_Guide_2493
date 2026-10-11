# QEA Test Automation Framework (Project 2)

Selenium WebDriver (Java) framework that tests the SauceDemo practice shop (https://www.saucedemo.com).
It grows during Week 6: Monday skeleton -> waits -> Page Objects -> Cucumber BDD layer -> tags and reports.

## Requirements
- JDK 17+, Maven 3.9+, Chrome (Firefox/Edge optional)

## How to run
```
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck -Dheadless=true
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck -Dbrowser=firefox
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.LoginSearchFlow
```
Flows added Tuesday:
```
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SortFlow
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.FlakyScenarios   # (see FlakinessRun)
mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.FlakinessRun -Dtimes=5 -Dheadless=true
```
Screenshots are written to `target/screenshots/`.

## Project structure
- `drivers/DriverFactory` - creates browsers; reads -Dbrowser and -Dheadless
- `utils/ScreenshotUtil` - PNG evidence; `utils/Check` - PASS/FAIL helper (counts failures)
- `utils/WaitUtils` - the ONLY place that owns timeouts (explicit waits, default 10 s, no implicit wait)
- `utils/DropdownUtils` - wraps Selenium's Select; `utils/RepeatRunner` - runs a flow N times and prints the pass rate
- `flows/` - runnable automation flows (later: Page Objects and Cucumber steps)

## Team / author
(add your name)

## Stability rules (adopted Tuesday)
1. No `Thread.sleep` anywhere in the project.
2. No implicit wait; all waiting goes through `WaitUtils`.
3. Helpers take a `By`, never a stored `WebElement`.
4. A flow is "stable" only when `FlakinessRun` shows 10/10.
