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
Screenshots are written to `target/screenshots/`.

## Project structure
- `drivers/DriverFactory` - creates browsers; reads -Dbrowser and -Dheadless
- `utils/ScreenshotUtil` - PNG evidence; `utils/Check` - PASS/FAIL helper
- `flows/` - runnable automation flows (later: Page Objects and Cucumber steps)

## Team / author
(add your name)
