# QEA Test Automation Framework (Project 2)

Selenium WebDriver (Java) + Cucumber (BDD) framework for https://www.saucedemo.com.
Week 6 progress: Monday skeleton -> Tuesday waits -> Wednesday Page Objects -> **Thursday BDD (pair work)** -> Friday tags and reports.

## Requirements
- JDK 17+, Maven 3.9+, Chrome (Firefox/Edge optional)

## How to run
(TODO slot 6: add the exact commands you verified)

    mvn test
    mvn test -Dheadless=true
    mvn test -Dbrowser=firefox -Dheadless=true
    mvn test -Dtest=FeatureStyleTest

## Project structure
- `src/main/java/.../drivers`, `utils`, `pages` - Monday to Wednesday (DriverFactory, WaitUtils, DropdownUtils, page objects)
- `src/test/resources/features` - Gherkin features (login, sort, cart)
- `src/test/java/.../steps` - step definitions (page objects only)
- `src/test/java/.../support/TestContext` - per-scenario shared state (PicoContainer)
- `src/test/java/.../runners/RunCucumberTest` - JUnit 5 Suite runner
- `src/test/java/.../quality/FeatureStyleTest` - automated BDD rules (Definition of Done)
- `docs/` - Three Amigos notes, pair log, retrospective

## Features and scenarios
(TODO: one line per feature with the number of scenarios)

## Team / authors
(TODO: both names)
