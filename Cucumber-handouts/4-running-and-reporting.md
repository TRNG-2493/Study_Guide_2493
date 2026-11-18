# Cucumber In-Class Handout 4: Running and Reporting

**Topics:** 4.1 Tags · 4.2 JUnit integration · 4.3 Maven integration · 4.4 Cucumber reporting

**How to use this handout:** the same layout as before. Each topic has a **definition** and **key terms**, the **key ideas**, a **worked example** built step by step, a **checkpoint**, **your turn** exercises and **common errors**.

**Builds on Cucumber Handouts 1–3:** two feature files (`login.feature`, version 3.2, with 9 scenarios, and `sorting.feature` with 4: 13 in total), the step classes `LoginSteps` and `SortSteps` extending `BaseSteps`, the `Hooks` class (browser open/close and a screenshot on failure), and the suite class `RunCucumberTest`, with Cucumber's settings in `@ConfigurationParameter` lines.

---

## 4.1 Tags

### Definition

A **tag** is a label that starts with `@`, written on the line **above** a `Feature`, `Rule`, `Scenario`, `Scenario Outline` or `Examples` block. Tags let you **choose which scenarios to run**, for example only the quick `@smoke` checks, or only the scenarios for one story such as `@SL-101`. A scenario **inherits** the tags of the feature, rule and examples it belongs to. You select scenarios with a **tag expression** such as `@smoke and not @wip`, passed to Cucumber in the setting `cucumber.filter.tags`.

### Key terms

| Term | Meaning |
|---|---|
| **Tag** | A label such as `@smoke`, `@SL-101`, `@wip` |
| **Tag inheritance** | A tag on a `Feature` applies to every scenario in it; a tag on `Examples:` applies to those rows only |
| **Tag expression** | A filter built from tags with `and`, `or`, `not` and brackets |
| **`cucumber.filter.tags`** | The setting that holds the tag expression |

**Tag expressions:**

| Expression | Runs scenarios that... |
|---|---|
| `@smoke` | have `@smoke` (directly or inherited) |
| `not @wip` | do **not** have `@wip` |
| `@smoke and @SL-101` | have **both** tags |
| `@SL-101 or @SL-104` | have **either** tag |
| `(@smoke or @SL-102) and not @wip` | brackets group, as in Java |

**Common kinds of tag:** purpose (`@smoke`, `@regression`), story (`@SL-101`), state (`@wip` = work in progress), technical (`@maximized` for a tagged hook, Handout 3).

### Key ideas

- Tags are **case-sensitive**: `@Smoke` and `@smoke` are different tags.
- Use a **story tag** on each feature, so every scenario can be traced back to its user story.
- `@wip` marks scenarios that aren't finished; exclude them with `not @wip` so they don't break the build.

### Worked example: smoke and story tags

**Step 1: A story tag on each feature.** Every scenario in the file inherits it.

```gherkin
@SL-101
Feature: Log in to Swag Labs
```

```gherkin
@SL-104
Feature: Sort the products
```

**Step 2: A story tag on a Rule.** The logout rule belongs to story SL-102, so tag the Rule: its scenario gets **both** `@SL-101` (from the feature) and `@SL-102`.

```gherkin
  @SL-102
  Rule: A logged-in user can log out
```

**Step 3: `@smoke` on the checks that prove the basics work:** the logout scenario (it logs in **and** out, so it covers both), and the price sorts in `sorting.feature` (tag the whole `Examples:` block).

```gherkin
    @smoke
    Scenario: Logged-in user logs out
```

```gherkin
    @smoke
    Examples: Sorting by price
      | order               | first                    |
      | Price (low to high) | Sauce Labs Onesie        |
      | Price (high to low) | Sauce Labs Fleece Jacket |
```

**Step 4: Mark unfinished work.** Add a scenario to the "Everyone else is refused with a message" rule whose steps don't exist yet, and tag it `@wip`.

```gherkin
    @wip
    Scenario: Account is locked after three wrong passwords
      When I log in 3 times with username "standard_user" and a wrong password
      Then I should see the error "Epic sadface: Your account is locked"
```

**Step 5: Run with a tag expression** from VS Code's terminal:

```bash
mvn test -Dtest=RunCucumberTest -Dcucumber.filter.tags="@smoke and not @wip"
```

Tag expressions are easiest to pass on the command line like this; the green ▷ in the editor always runs the suite without a filter.

### Checkpoint

With the tags above, the smoke run executes **3** scenarios (the logout and the two price sorts). Cucumber's summary shows:

```text
3 scenarios (3 passed)
```

JUnit lists the other scenarios as **skipped**: they were filtered out, not run.

With `-Dcucumber.filter.tags="@SL-101 and not @wip"`, only the **9** login scenarios run.

### Your turn

1. Predict the number of scenarios **before** you run each one: (a) `@SL-104`; (b) `@SL-101 and not @SL-102 and not @wip`; (c) `not @wip`.
2. Tag the two "is missing" rows of the refused-login outline `@negative` without tagging the other rows. (Hint: put those rows in a second `Examples:` table, as `sorting.feature` does.)
3. Run `@SL-102 or @SL-104`. How many scenarios run?

### Common errors

| You see | Why | Fix |
|---|---|---|
| `0 scenarios` | Tag spelled differently (`@Smoke` vs `@smoke`) | Use one spelling everywhere |
| Error parsing the tag expression | Missing `@` or unbalanced brackets | e.g. `@smoke and not @wip` |
| The tag has no effect | Tag written on the same line as `Scenario:` | Put tags on the line **above** |

---

## 4.2 JUnit Integration

### Definition

The **JUnit Platform** is the part of JUnit that IDEs, Maven and build servers use to find and run tests. Different kinds of tests plug into it through **test engines**: the **Jupiter** engine runs the `@Test` methods from the Selenium handouts, and the **Cucumber engine** runs feature files. Since Handout 2, our **suite class** `RunCucumberTest` has told the JUnit Platform to run the feature files, so each **scenario** is reported as one JUnit test, in the IDE and in Maven. **JUnit integration** is about using that connection well: filtering scenarios with JUnit tags, creating several suites for different purposes, and choosing **where Cucumber's settings live**.

### Key terms

| Term | Meaning |
|---|---|
| **JUnit Platform** | The common layer that IDEs and Maven use to run tests |
| **Test engine** | A plug-in that runs one kind of test: Jupiter (`@Test`), Cucumber (feature files) |
| **Suite class** | A class whose annotations choose the engine and the features to run |
| **JUnit tag** | A Cucumber tag without the `@`: `@smoke` becomes the JUnit tag `smoke` |
| **`junit-platform.properties`** | A settings file in `src/test/resources`, read by **every** suite |

**Suite annotations:**

| Annotation | Meaning |
|---|---|
| `@Suite` | This class is a suite |
| `@IncludeEngines("cucumber")` | Use the Cucumber engine |
| `@SelectPackages("features")` | Run the feature files in `src/test/resources/features` |
| `@IncludeTags("smoke")` | Only scenarios tagged `@smoke` (written **without** `@`) |
| `@ExcludeTags("wip")` | Leave out scenarios tagged `@wip` |
| `@ConfigurationParameter(key, value)` | One Cucumber setting, for **this suite only** |

### Key ideas

```text
 mvn test / IDE ──> JUnit Platform ──> Jupiter engine  ──> @Test methods (Selenium tests)
                                   └─> Cucumber engine ──> feature files (scenarios)
```

- One `mvn test` runs **both** kinds of test and reports them together.
- **Different suites for different jobs:** everything, smoke only, one story. Each is a small class with different tag annotations.
- **Two places for Cucumber's settings:**

| | `@ConfigurationParameter` on the suite (Handout 2) | `junit-platform.properties` file |
|---|---|---|
| Applies to | That one suite | **Every** suite |
| Good for | One suite; settings that differ per suite | Settings all suites share (glue, plugins) |
| With several suites | The same lines are repeated in each | Written once |

- **Set each key in one place only.** If the same key is in both, the suite's `@ConfigurationParameter` wins, and a change in the file seems to do nothing.

### Worked example: a second suite, and settings moved to a file

**Step 1: Look at what JUnit sees.** Run `mvn test -Dtest=RunCucumberTest` and read the end of the output: `Tests run: 14` (13 scenarios plus the new `@wip` one, which fails). JUnit counts **one test per scenario** (each outline row is one scenario).

**Step 2: Keep unfinished work out of the main suite.** Add `@ExcludeTags("wip")` to `RunCucumberTest`, so the `@wip` scenario no longer breaks the run.

**Step 3: A smoke suite.** Copy `RunCucumberTest` to `RunSmokeTest`, and replace `@ExcludeTags("wip")` with `@IncludeTags("smoke")`. Notice that the three `@ConfigurationParameter` lines are now **repeated** in two classes, and a third suite would repeat them again.

**Step 4: Move the shared settings into a file.** Create `src/test/resources/junit-platform.properties` with the same three settings. The keys are the text values of the `Constants` you used in Handout 2 (`GLUE_PROPERTY_NAME` is `cucumber.glue`, and so on).

```properties
# src/test/resources/junit-platform.properties
cucumber.glue=com.qea.selenium.steps
cucumber.plugin=pretty, summary
cucumber.snippet-type=camelcase
```

**Step 5: Delete the `@ConfigurationParameter` lines (and their imports) from both suites.** Each setting now lives in **one** place, and both suites read it from the file.

```java
@Suite
@IncludeEngines("cucumber")
@SelectPackages("features")
@IncludeTags("smoke")
public class RunSmokeTest {
}
```

**Step 6: Run everything with one command.** `mvn test` runs the Selenium JUnit tests **and** every Cucumber suite.

```bash
mvn test                        # Selenium tests + all suites
mvn test -Dtest=RunSmokeTest    # only the smoke suite
```

**Complete code**

```properties
# src/test/resources/junit-platform.properties
cucumber.glue=com.qea.selenium.steps
cucumber.plugin=pretty, summary
cucumber.snippet-type=camelcase
```

```java
// src/test/java/com/qea/selenium/RunCucumberTest.java
package com.qea.selenium;

import org.junit.platform.suite.api.ExcludeTags;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;

/** Runs every feature file except work in progress. Settings: junit-platform.properties. */
@Suite
@IncludeEngines("cucumber")
@SelectPackages("features")
@ExcludeTags("wip")
public class RunCucumberTest {
}
```

```java
// src/test/java/com/qea/selenium/RunSmokeTest.java
package com.qea.selenium;

import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.IncludeTags;
import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;

/** Runs only the scenarios tagged @smoke. Settings: junit-platform.properties. */
@Suite
@IncludeEngines("cucumber")
@SelectPackages("features")
@IncludeTags("smoke")
public class RunSmokeTest {
}
```

### Checkpoint

```bash
mvn test -Dtest=RunCucumberTest
```

```text
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

13 = the scenarios from Handout 3 (9 login, 4 sorting); the `@wip` scenario is excluded. `mvn test -Dtest=RunSmokeTest` reports `Tests run: 3`. Both suites still print the `pretty` output and find the step definitions, now from the properties file.

### Your turn

1. Remove `@ExcludeTags("wip")` from `RunCucumberTest` and run it. What happens to the `@wip` scenario, and to the build? Put the annotation back.
2. Create `RunLoginTest` that runs only `SL-101` scenarios (keep `@ExcludeTags("wip")`). How many tests does it report? Did you need to repeat any settings?
3. Give **only** `RunSmokeTest` a different output: add `@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME, value = "progress")` back to it. Run both suites and compare their console output. (This is when a suite-level setting is useful.)

### Common errors

| You see | Why | Fix |
|---|---|---|
| `Tests run: 0` | `@IncludeEngines("cucumber")` missing, or the engine dependency is missing | Check the suite class and the `pom.xml` |
| Every step undefined after moving the settings | The properties file is in the wrong folder or misspelled | `src/test/resources/junit-platform.properties`, exactly |
| A change in `junit-platform.properties` has no effect | The suite still has a `@ConfigurationParameter` for the same key, and it wins | Delete it from the suite; set each key in one place |
| `@IncludeTags("@smoke")` finds nothing | JUnit tags are written **without** `@` | `@IncludeTags("smoke")` |
| `NoSuchMethodError` when starting | Different JUnit versions mixed | One version for all JUnit modules (BOM in 4.3) |

---

## 4.3 Maven Integration

### Definition

**Maven** is the build tool that compiles the project and runs its tests the same way on every machine: on your laptop, a colleague's, and the build server. `mvn test` runs the **phases** of Maven's build in order (compile the code, compile the tests, run the tests); the **Surefire** plugin does the actual test run through the JUnit Platform, so it runs the Selenium JUnit tests **and** the Cucumber scenarios. **Maven integration** means setting up `pom.xml` so that this build is reliable: matching versions for related libraries (**BOMs**), fixed plugin versions, and **profiles** and `-D` options to choose what to run.

### Key terms

| Term | Meaning |
|---|---|
| **Phase** | A stage of the build. `mvn test` runs validate → compile → test-compile → test. |
| **`mvn clean`** | Deletes the `target` folder (everything built before) |
| **Surefire** | The Maven plugin that runs tests in the `test` phase |
| **BOM** (bill of materials) | A list of matching versions for a family of libraries, imported in `<dependencyManagement>`. Dependencies then need **no** `<version>`. |
| **Profile** | A named set of extra settings, switched on with `-P<name>`, e.g. `-Psmoke` |
| **`-D` option** | Passes a setting on the command line, e.g. `-Dtest=RunCucumberTest` |

**Commands you will use:**

| Command | Runs |
|---|---|
| `mvn test` | Every test: Selenium JUnit tests and Cucumber suites |
| `mvn clean test` | The same, starting from an empty `target` folder |
| `mvn test -Dtest=RunCucumberTest` | One test class or suite |
| `mvn test -Dgroups=smoke` | Only tests with the JUnit tag `smoke` |
| `mvn test -Psmoke` | The same, through a profile |
| `mvn test -Dtest=RunCucumberTest -Dcucumber.filter.tags="@smoke"` | Filter with a Cucumber tag expression |

### Key ideas

- **One command for everyone:** a new team member, a developer before pushing, and the build server all run `mvn test`.
- **BOMs** keep Cucumber modules on one version and JUnit modules on another; to upgrade, change **one** property.
- If deleted or renamed scenarios still run, old files are left in `target`: run `mvn clean test`.

### Worked example: the final `pom.xml`

**Step 1: Import the BOMs** inside `<dependencyManagement>`.

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-bom</artifactId>
            <version>${cucumber.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <dependency>
            <groupId>org.junit</groupId>
            <artifactId>junit-bom</artifactId>
            <version>${junit.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**Step 2: Remove `<version>` from the Cucumber and JUnit dependencies;** the BOMs supply it.

```xml
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-java</artifactId>
    <scope>test</scope>
</dependency>
```

**Step 3: A `smoke` profile.** It makes Surefire run only tests tagged `smoke`. Since the profile replaces it, **delete `RunSmokeTest.java`**; otherwise the smoke scenarios would run twice (once in each suite).

```xml
<profiles>
    <profile>
        <id>smoke</id>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-surefire-plugin</artifactId>
                    <configuration>
                        <groups>smoke</groups>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

**Complete file**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- pom.xml (final: Selenium + JUnit + Cucumber) -->
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
        <cucumber.version>8.0.4</cucumber.version>
        <junit.version>6.1.3</junit.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>io.cucumber</groupId>
                <artifactId>cucumber-bom</artifactId>
                <version>${cucumber.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>org.junit</groupId>
                <artifactId>junit-bom</artifactId>
                <version>${junit.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <dependency>
            <groupId>org.seleniumhq.selenium</groupId>
            <artifactId>selenium-java</artifactId>
            <version>${selenium.version}</version>
        </dependency>

        <!-- Versions come from the BOMs -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.platform</groupId>
            <artifactId>junit-platform-suite</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-java</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.cucumber</groupId>
            <artifactId>cucumber-junit-platform-engine</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.6.0</version>
            </plugin>
        </plugins>
    </build>

    <profiles>
        <!-- mvn test -Psmoke : only tests and scenarios tagged smoke -->
        <profile>
            <id>smoke</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-surefire-plugin</artifactId>
                        <configuration>
                            <groups>smoke</groups>
                        </configuration>
                    </plugin>
                </plugins>
            </build>
        </profile>
    </profiles>
</project>
```

### Checkpoint

| Command | Expected |
|---|---|
| `mvn clean test` | All Selenium tests and all 13 scenarios run (the `@wip` scenario is excluded); `BUILD SUCCESS` |
| `mvn test -Psmoke` | `Tests run: 3`: only the smoke scenarios (no Selenium test has the tag) |
| `mvn test -Dtest=RunCucumberTest -Dcucumber.filter.tags="@smoke"` | All 13 scenarios are **reported**, but only 3 run; the rest are **skipped** |

### Your turn

1. Run `mvn clean`, then `mvn test-compile`, then `mvn test -Dtest=RunCucumberTest`. After each, look inside `target`. Which command copied the feature files there?
2. Explain why `-Psmoke` reports `Tests run: 3`, while `-Dcucumber.filter.tags="@smoke"` reports every scenario with most of them skipped.
3. Add a second profile, `story104`, that runs only `SL-104` scenarios. Run `mvn test -Pstory104`.

### Common errors

| You see | Why | Fix |
|---|---|---|
| A deleted scenario still runs | Old copy in `target` | `mvn clean test` |
| `-Dgroups=smoke` runs nothing | Tag spelled differently, or written with `@` | `-Dgroups=smoke` (no `@`) |
| Smoke scenarios counted twice | Two suite classes both include them | Keep one suite class; use the profile |
| Selenium tests run when you only wanted scenarios | `mvn test` runs every test class | Use `-Dtest=RunCucumberTest` or a profile |

---

## 4.4 Cucumber Reporting

### Definition

A **test report** shows the results of a run in a form people or tools can read. Cucumber produces reports through **plugins**, listed in the `cucumber.plugin` setting: `pretty` and `summary` print to the console; `html` writes a web page for people; `json` and `junit` (XML) write files for other tools such as build servers; `rerun` writes a list of the failed scenarios. Every plugin except one console plugin writes to a **file**. Screenshots that hooks **attach** to a scenario (Handout 3) appear inside the HTML report, next to the failed step. In Cucumber 8 the file reports need a JSON library, **Jackson**, added as a dependency.

### Key terms

| Plugin | Output | Read by |
|---|---|---|
| `pretty` | Each step in colour, in the console | You, while running |
| `summary` | Totals at the end, in the console | You |
| `html:target/cucumber-reports/cucumber.html` | One web page with every feature, scenario and step | Team, product owner |
| `json:target/cucumber-reports/cucumber.json` | JSON data | Other reporting tools |
| `junit:target/cucumber-reports/cucumber.xml` | JUnit XML | Build servers (Jenkins, GitHub Actions, ...) |
| `rerun:target/cucumber-reports/rerun.txt` | The failed scenarios, as `file:line` | Rerunning only failures |

**Other terms:**

- **Attachment:** a file added to a scenario's results with `scenario.attach(...)`, such as a screenshot.
- **Jackson:** a Java library for reading and writing JSON. Cucumber 8 needs it for the file reports.

### Key ideas

- Only **one** plugin may write to the console; every other plugin needs a file path.
- Put reports under `target` so `mvn clean` removes old ones.
- Attach evidence in **hooks**, not in step definitions.

### Worked example: an HTML report with a screenshot

**Step 1: Add the HTML report** to the `cucumber.plugin` line in `junit-platform.properties` (since 4.2 the settings live there, not in the suite classes), and run `mvn test -Dtest=RunCucumberTest`.

```properties
cucumber.plugin=pretty, summary, html:target/cucumber-reports/cucumber.html
```

The run stops **before any scenario** with: `Cucumber needs a JSON library to write reports.`

**Step 2: Add Jackson** to `pom.xml`.

```xml
<!-- inside <properties> -->
<jackson.version>3.2.4</jackson.version>

<!-- inside <dependencies> -->
<dependency>
    <groupId>tools.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>${jackson.version}</version>
    <scope>test</scope>
</dependency>
```

Run again, then open `target/cucumber-reports/cucumber.html` in a browser.

**Step 3: Add the other reports.** A backslash `\` at the end of a line continues the setting on the next line.

```properties
cucumber.plugin=pretty, summary, \
  html:target/cucumber-reports/cucumber.html, \
  json:target/cucumber-reports/cucumber.json, \
  junit:target/cucumber-reports/cucumber.xml, \
  rerun:target/cucumber-reports/rerun.txt
```

**Step 4: See a failure in the report.** Break one row on purpose (in `sorting.feature`, change `Sauce Labs Onesie` to `Sauce Labs Bolt T-Shirt`), run again, and open the HTML report. Find the failed scenario, the assertion message under the failed step, and the **screenshot** that `Hooks` attached. Then undo the change.

**Complete file**

```properties
# src/test/resources/junit-platform.properties
cucumber.glue=com.qea.selenium.steps
cucumber.snippet-type=camelcase
cucumber.plugin=pretty, summary, \
  html:target/cucumber-reports/cucumber.html, \
  json:target/cucumber-reports/cucumber.json, \
  junit:target/cucumber-reports/cucumber.xml, \
  rerun:target/cucumber-reports/rerun.txt
```

### Checkpoint

After `mvn test -Dtest=RunCucumberTest`:

```text
target/cucumber-reports/
├── cucumber.html      open in a browser: features, scenarios, steps, durations
├── cucumber.json
├── cucumber.xml
└── rerun.txt          empty when everything passed
```

With the deliberate failure from step 4, the HTML report shows **1 failed** scenario in red, with the assertion message and the attached screenshot, and `rerun.txt` contains one line pointing at the failed row.

### Your turn

1. In the HTML report, use the search box to show only `@SL-102` scenarios. Which tags does that scenario have, and why?
2. Open `cucumber.xml` in VS Code. How many `<testcase>` elements are there?
3. In `Hooks.closeBrowser`, add a `Scenario` parameter and the line `scenario.log("Browser closed")`. Run again and find the text in the HTML report.

### Common errors

| You see | Why | Fix |
|---|---|---|
| `Cucumber needs a JSON library to write reports` | Jackson is missing | Add `tools.jackson.core:jackson-databind` (test scope) |
| `Only one plugin can use STDOUT` | Two console plugins | Give every extra plugin a file path |
| No screenshot in the report | The hook saves nothing with `scenario.attach(...)`, or the scenario passed | Attach the bytes as `image/png` in the `@After` hook |
| No report file at all, no error | A suite still has its own `@ConfigurationParameter` for the plugins, which overrides the file | Remove it; keep `cucumber.plugin` only in the file |
| An old report is shown | The browser shows a cached copy | Reload the page; reports are rewritten on every run |

---

**End of Cucumber Handout 4.** One `mvn test` now runs your Selenium tests and your Cucumber scenarios, you can choose scenarios with tags, suites and profiles, and every run produces an HTML report with screenshots of failures. **Next (self-study):** Cucumber Handout 5, Putting It Together: the same project refactored to page objects, plus a shopping-cart feature.
