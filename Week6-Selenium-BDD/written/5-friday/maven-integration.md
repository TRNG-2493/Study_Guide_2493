# Maven Integration

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what **Maven** does for a test automation project: dependency management, build lifecycle, and repeatable command-line execution.
- Read and write a complete **`pom.xml`** for a Selenium + Cucumber + JUnit 5 project, including properties, dependencies and scopes, and explain every element.
- Explain **transitive dependencies**, **dependency scopes**, and **version conflicts** ("nearest wins"), and use `mvn dependency:tree` to investigate them.
- Describe the **Maven build lifecycle** (`clean`, `compile`, `test`, `verify`) and which phase runs your tests, and read an annotated build log.
- Configure the **Maven Surefire plugin** (and know when to use **Failsafe**) to run Cucumber runners.
- Pass **system properties** (`-Dbrowser`, `-Dheadless`, `-Dcucumber.filter.tags`) from the command line into the tests.
- Create **Maven profiles** for smoke, regression, and browsers, and predict which value wins when the same setting appears in several places.
- Locate the **reports** and test result files, and describe how the same commands run in a **CI** pipeline (orientation only).
- Troubleshoot common Maven problems (dependency conflicts, offline mode, encoding, JDK version, "no tests run") from the real error messages.

---

## Why This Matters

A test framework that only runs from one person's IDE is not a framework; it is a personal script. Companies run automated tests **unattended**: on every commit, every night, before every release, using build servers such as Jenkins, GitHub Actions, GitLab CI, or Azure DevOps. These servers have no IDE; they run **commands**. Maven provides the command line (`mvn test`) and takes care of the surrounding chores: downloading the correct library versions, compiling, running, and collecting results.

Think of Maven as a **head chef with a standard recipe card**. You write the recipe once (`pom.xml`): which ingredients (libraries) at which versions, and in what order to cook (compile, then test). Any kitchen (your laptop, a teammate's laptop, a build server) that receives the same recipe card produces the same dish. Without it, every kitchen would improvise: "it works on my machine" becomes the standard excuse.

Project 2 requires a framework that **anyone on the team can clone and run with one command**, and today's milestone is to complete the BDD layer with tags and a report. That is exactly what proper Maven integration delivers: `mvn clean test -Psmoke` runs the `@smoke` scenarios against saucedemo.com, and the HTML report appears in `target/`. You have used Maven since Monday (to add Selenium) and Thursday (to add Cucumber); today we study it properly and use it as the backbone of the whole framework.

**Where you will use this:** every time you add a library, run a subset of tests, change a browser from the command line, or set up a CI job. You will also use it in interviews: "How do you run your tests from the command line?" is one of the most common questions for automation roles.

---

## The Concept

### 1. What Is Maven?

**Apache Maven** is a **build and dependency management tool** for Java. A **build** is the process of turning source code into something runnable (compile, test, package). Its main ideas:

| Idea | Meaning |
|---|---|
| **Project Object Model (`pom.xml`)** | A single XML file that describes your project: its identity, dependencies, plugins, and build settings |
| **Convention over configuration** | A **standard folder layout** (`src/main/java`, `src/test/java`, `src/test/resources`) so every Maven project looks the same |
| **Dependency management** | You declare "I need Selenium 4.25.0"; Maven downloads it (and everything **it** depends on) from **Maven Central** into your local cache (`~/.m2/repository`) |
| **Build lifecycle** | A fixed sequence of **phases** (compile, test, package...) that plugins hook into |
| **Plugins** | Tools that do the work in each phase (compiler plugin, Surefire for tests, etc.) |

> Do not confuse the Maven **file name** `pom.xml` (Project Object Model) with the **Page Object Model** (POM) from Wednesday. Same acronym, entirely different things.

**Why not just download the jar files by hand?** Selenium alone needs dozens of other libraries. Downloading them manually means finding each one, checking that versions fit together, and giving the same set to every teammate. Maven automates all of it, and the `pom.xml` is committed to Git so the setup is shared and reviewable.

**What is Maven Central?** A huge public online repository of Java libraries. When you declare a dependency, Maven asks Maven Central (through your network) for it, stores it in `~/.m2/repository` (the **local repository**), and from then on uses the local copy. That is why the first build is slow and later ones are fast.

### 2. The Standard Layout for Our Framework

```
bdd-framework/
 ├── pom.xml
 └── src/
     ├── main/java/...                    page objects, driver factory, utilities
     └── test/
          ├── java/...                    runners, step definitions, hooks, TestContext
          └── resources/
                ├── features/             .feature files
                ├── cucumber.properties
                └── junit-platform.properties
 target/                                  generated: classes, reports (never commit it)
```

Add a `.gitignore` containing at least `target/` so build output is not committed.

Why it matters: Maven **only looks in these places**. A feature file placed outside `src/test/resources` is never copied to the classpath, so the runner cannot find it. A step class in `src/main/java` works but mixes test code into production code; keep steps and runners in `src/test/java`.

### 3. The `pom.xml` Explained

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <!-- 1. Coordinates: the unique identity of this project -->
  <groupId>com.revature.qea</groupId>
  <artifactId>bdd-framework</artifactId>
  <version>1.0-SNAPSHOT</version>
  <packaging>jar</packaging>
  <name>QEA BDD Test Automation Framework</name>

  <!-- 2. Properties: reusable values and build settings -->
  <properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

    <selenium.version>4.25.0</selenium.version>
    <cucumber.version>7.20.1</cucumber.version>
    <junit.version>5.11.0</junit.version>
    <junit.platform.version>1.11.0</junit.platform.version>
    <surefire.version>3.5.0</surefire.version>

    <!-- default values for test parameters (can be overridden with -D) -->
    <browser>chrome</browser>
    <headless>false</headless>
    <cucumber.filter.tags>not @wip and not @ignore</cucumber.filter.tags>
  </properties>

  <!-- 3. Dependencies -->
  <dependencies>
    <dependency>
      <groupId>org.seleniumhq.selenium</groupId>
      <artifactId>selenium-java</artifactId>
      <version>${selenium.version}</version>
    </dependency>
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-java</artifactId>
      <version>${cucumber.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-junit-platform-engine</artifactId>
      <version>${cucumber.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-picocontainer</artifactId>
      <version>${cucumber.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>${junit.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.junit.platform</groupId>
      <artifactId>junit-platform-suite</artifactId>
      <version>${junit.platform.version}</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <!-- 4. Build configuration -->
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>${surefire.version}</version>
        <configuration>
          <!-- forward these values into the test JVM as system properties -->
          <systemPropertyVariables>
            <browser>${browser}</browser>
            <headless>${headless}</headless>
            <cucumber.filter.tags>${cucumber.filter.tags}</cucumber.filter.tags>
          </systemPropertyVariables>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

> **All version numbers in this lesson are examples.** Before you copy them into a real project, check Maven Central (search.maven.org) or each project's release page for current, mutually compatible versions.

**Section by section:**

1. **Coordinates**: `groupId` (organization/domain in reverse), `artifactId` (project name), `version` (`-SNAPSHOT` = work in progress). Together they identify any artifact worldwide; dependencies are referred to by these coordinates.
2. **Properties**: Variables referenced as `${name}`. Centralizing versions is good practice: all Cucumber artifacts share **one** `cucumber.version`. The `<browser>`, `<headless>`, and tag properties define **defaults** that a command-line `-D` overrides (command-line user properties take precedence over `<properties>`).
3. **Dependencies**: Each has `groupId:artifactId:version` and a **scope** (see Section 4).
4. **Build/plugins**: Plugins extend Maven. **Surefire** runs your tests, and `systemPropertyVariables` hands values into the test JVM, so that `System.getProperty("browser")` in `TestContext` receives them.

**Line-by-line notes for the less obvious lines:**

| Line | Explanation |
|---|---|
| `<project xmlns=... xsi:schemaLocation=...>` | The XML namespace header. It tells editors which schema validates the file, which gives auto-completion. Copy it unchanged. |
| `<modelVersion>4.0.0</modelVersion>` | The POM format version. Always `4.0.0` for Maven 3 and 4 projects. |
| `<packaging>jar</packaging>` | The output type. `jar` is the default; a test-only project does not need to be deployed, but the default is fine. |
| `<name>` | A human-readable label for logs; not used for identification. |
| `maven.compiler.source` / `target` | The Java language level of the source and of the compiled output. Here Java 17. Newer setups use `<maven.compiler.release>17</maven.compiler.release>`, which sets both at once and checks against the JDK's real API. Your installed JDK must be at least this version. |
| `project.build.sourceEncoding` | The character set for source files. UTF-8 avoids garbled characters in feature files or strings. |
| `<selenium.version>` etc. | **User-defined properties.** Names are free; you choose them. Referencing `${selenium.version}` later keeps a version in exactly one place. |
| `<browser>`, `<headless>` | User-defined properties used as test parameters; defaults for when nobody passes `-D`. |
| `<scope>test</scope>` | The dependency exists only for test code. |
| `<systemPropertyVariables>` | A Surefire setting: a list of `<name>value</name>` pairs that Surefire sets as Java system properties in the forked test JVM. The element name becomes the property name. |

### 4. Dependencies in Depth: Scopes, Transitives, and Conflicts

#### 4.1 Scopes

A **scope** tells Maven **when** a dependency is needed.

| Scope | Available when compiling main code | Available when compiling/running tests | Included at runtime of the app | Typical use |
|---|---|---|---|---|
| `compile` (default) | Yes | Yes | Yes | Libraries your main code uses (Selenium, because page objects in `src/main` use it) |
| `test` | No | Yes | No | Test-only libraries (Cucumber, JUnit, PicoContainer) |
| `provided` | Yes | Yes | No (supplied by the container) | Servlet API in a web app (rare for us) |
| `runtime` | No | Yes | Yes | Libraries needed only when running (a JDBC driver, a logging backend) |
| `system` / `import` | Special cases | | | `import` is used in `dependencyManagement` to import a BOM (see below); `system` is discouraged |

Why scopes matter: if you accidentally leave `cucumber-java` as `compile`, and you later package your page objects as a library for another team, Cucumber travels with it unnecessarily. And if you give `selenium-java` the `test` scope while your page objects live in `src/main/java`, the main code fails to compile with `package org.openqa.selenium does not exist`: the compiler of `src/main` cannot see test-scope libraries.

**A decision rule:** "Does code in `src/main/java` import it?" Then `compile`. "Only tests use it?" Then `test`.

#### 4.2 Transitive dependencies

A **transitive dependency** is a dependency of your dependency. You write one line for `selenium-java`; Maven reads Selenium's own `pom.xml` (published beside the jar), sees that it needs `selenium-api`, `selenium-chrome-driver`, `selenium-remote-driver`, plus libraries such as Netty, Guava, and OpenTelemetry, and downloads all of them. Those in turn have their own dependencies.

Analogy: you order a *meal kit*. The kit lists its own ingredients; you do not individually order the flour, the eggs, and the spices that the recipe needs. Maven reads the kit's list and orders them for you.

The scope of a transitive dependency follows a combination rule. Simplified: if you depend on X with scope `test`, then everything X needs is also test scope for you; a `compile` dependency's compile dependencies stay `compile`, and its `test` dependencies are never pulled in at all (a library's own tests are not your business).

You can see the entire tree:

```
mvn dependency:tree
```

An abbreviated example of the output (versions are examples):

```
[INFO] com.revature.qea:bdd-framework:jar:1.0-SNAPSHOT
[INFO] +- org.seleniumhq.selenium:selenium-java:jar:4.25.0:compile
[INFO] |  +- org.seleniumhq.selenium:selenium-api:jar:4.25.0:compile
[INFO] |  +- org.seleniumhq.selenium:selenium-chrome-driver:jar:4.25.0:compile
[INFO] |  |  \- org.seleniumhq.selenium:selenium-chromium-driver:jar:4.25.0:compile
[INFO] |  \- org.seleniumhq.selenium:selenium-remote-driver:jar:4.25.0:compile
[INFO] +- io.cucumber:cucumber-java:jar:7.20.1:test
[INFO] |  \- io.cucumber:cucumber-core:jar:7.20.1:test
[INFO] +- io.cucumber:cucumber-picocontainer:jar:7.20.1:test
[INFO] |  \- org.picocontainer:picocontainer:jar:2.15:test
[INFO] \- org.junit.jupiter:junit-jupiter:jar:5.11.0:test
```

How to read it: the first line is *your* project. The `+-` and `\-` lines are **direct** dependencies (the ones you wrote); deeper indented lines are **transitive**. Each line ends with the **scope**. The tree answers questions such as "where does `selenium-api` come from?" (from `selenium-java`) and "why is this old library on my classpath?"

Useful variants:

| Command | Use |
|---|---|
| `mvn dependency:tree -Dincludes=io.cucumber` | Show only branches containing that group |
| `mvn dependency:tree -Dverbose` | Also show the versions that Maven **omitted** because of a conflict (check your Maven dependency plugin version for the exact flag support) |
| `mvn dependency:analyze` | Report declared-but-unused and used-but-undeclared dependencies |

#### 4.3 Version conflicts and "nearest wins"

Two of your dependencies may both need the same library, but at different versions. Maven can put only **one** version on the classpath. Its rule is **nearest definition wins**: the version closest to your project in the tree is used (a direct dependency beats a transitive one); if two are equally near, the **first one declared** in the POM wins.

Example: your POM declares `library-A` and `library-B`. A needs `guava 31`; B needs `guava 33`. Both are at depth two, so Maven picks the one found first, say `guava 31`. B then runs with an older Guava than it was built for and may fail at runtime with:

```
java.lang.NoSuchMethodError: 'com.google.common.collect.ImmutableList com.google.common.collect.ImmutableList.copyOf(...)'
```

The code **compiled** fine; it fails when that line is executed, which makes it feel mysterious. Diagnosis steps:

1. Read the missing class or method: it names the library (Guava).
2. Run `mvn dependency:tree -Dincludes=com.google.guava` and see which version won.
3. Fix: align versions. Options, from simplest: (a) upgrade the dependency that needs the older one, (b) declare the library yourself as a **direct** dependency at the version you want (nearest wins), (c) use `dependencyManagement`.

#### 4.4 `dependencyManagement` and BOMs

A **BOM** (Bill of Materials) is a special POM that lists matching versions of a family of libraries. Importing it means you can omit individual versions:

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.junit</groupId>
      <artifactId>junit-bom</artifactId>
      <version>5.11.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    <dependency>
      <groupId>io.cucumber</groupId>
      <artifactId>cucumber-bom</artifactId>
      <version>7.20.1</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-java</artifactId>   <!-- no version needed: the BOM provides it -->
    <scope>test</scope>
  </dependency>
</dependencies>
```

`dependencyManagement` does not **add** anything to the classpath; it only **fixes the versions** used whenever the dependency appears anywhere (even transitively). It is the cleanest way to keep all JUnit artifacts (Jupiter, Platform, engines) on matching versions, which prevents the `NoClassDefFoundError: org/junit/platform/...` problems from the JUnit lesson. (Versions in the snippet are examples; check them.)

### 5. The Build Lifecycle

Maven runs **phases** in a fixed order; asking for a phase runs **all earlier ones** too:

```
validate -> compile -> test-compile -> test -> package -> verify -> install -> deploy
                                        ^
                                        |__ "mvn test": Surefire runs the unit/BDD tests here
```

Separate from this chain are two other lifecycles: **`clean`** (deletes the `target/` folder) and **`site`** (project site). You usually combine them:

| Command | Effect |
|---|---|
| `mvn clean` | Delete `target/` (start fresh) |
| `mvn compile` | Compile `src/main` |
| `mvn test-compile` | Also compile `src/test` |
| `mvn test` | Compile and **run the tests** |
| `mvn clean test` | Fresh build and run tests (**the standard command**) |
| `mvn verify` | Everything up to `verify` (runs Failsafe integration tests, see below) |
| `mvn -q test` | Quiet output |
| `mvn -o test` | Offline mode (use only the local cache) |
| `mvn -DskipTests package` | Build without running tests |
| `mvn dependency:tree` | Show the dependency tree |
| `mvn help:effective-pom` | Show the complete, effective POM |

**Phases versus goals.** A **phase** (like `test`) is a *stage*. A **goal** (like `surefire:test` or `dependency:tree`) is one *task of a plugin*. Plugins bind their goals to phases: the Surefire plugin's `test` goal is bound to the `test` phase, so running the phase runs the goal. You can also call a goal directly (`mvn dependency:tree`), which runs that single task without the lifecycle.

#### 5.1 An annotated build log

Here is `mvn clean test` for a small project, with the meaning of each part (versions and times are examples):

```
[INFO] Scanning for projects...                                          # Maven reads pom.xml
[INFO] ---------------< com.revature.qea:bdd-framework >----------------
[INFO] Building QEA BDD Test Automation Framework 1.0-SNAPSHOT           # name and version
[INFO] --- clean:3.2.0:clean (default-clean) @ bdd-framework ---         # phase clean: target/ deleted
[INFO] --- resources:3.3.1:resources (default-resources) ---             # copy src/main/resources
[INFO] --- compiler:3.13.0:compile (default-compile) ---                 # compile page objects
[INFO] Compiling 12 source files with javac [debug release 17] to target/classes
[INFO] --- resources:3.3.1:testResources (default-testResources) ---     # copies features/ and properties
[INFO] Copying 4 resources from src/test/resources to target/test-classes
[INFO] --- compiler:3.13.0:testCompile (default-testCompile) ---         # compile steps, hooks, runners
[INFO] Compiling 9 source files with javac [debug release 17] to target/test-classes
[INFO] --- surefire:3.5.0:test (default-test) @ bdd-framework ---         # THE phase that runs tests
[INFO] Running com.revature.qea.runners.RunCucumberTest
...scenario output from the pretty plug-in...
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0                  # 7 scenarios
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS                                                     # exit code 0
[INFO] Total time:  01:12 min
```

Reading tips: each `--- plugin:version:goal (execution-id) ---` line starts one task; if a build fails, look at the **last such line before `[ERROR]`** to see which plugin failed. A build failing at `compiler:compile` is a compile error in your code; failing at `surefire:test` means tests failed (or none ran); failing before compile usually means dependency resolution.

#### 5.2 What happens from `mvn clean test` to a report

1. `clean` removes any old reports. 2. Compile steps produce classes and copy features to `target/test-classes`. 3. Surefire starts a test JVM and launches the JUnit Platform with your runner (see the *JUnit Integration* lesson). 4. The Cucumber engine executes scenarios and its **plug-ins** write `report.html`, `cucumber.json`, and others into `target/cucumber-reports/`, while Surefire writes XML to `target/surefire-reports/`. 5. Maven prints the result and exits with code 0 or non-zero. 6. Anything that needs the JSON (for example the enhanced report in the *Cucumber Reporting* lesson) runs in a **later** phase such as `verify`, but only if the test phase did not fail the build (see the `testFailureIgnore` discussion below).

### 6. Surefire and Failsafe

| Plugin | Phase | Default test class names | Intended for |
|---|---|---|---|
| **Surefire** | `test` | `*Test`, `Test*`, `*Tests`, `*TestCase` | Unit tests and (for us) the Cucumber runner |
| **Failsafe** | `integration-test` and `verify` | `*IT`, `IT*`, `*ITCase` | Integration/end-to-end tests where setup and teardown phases matter (start a server, run tests, stop it, **then fail the build**) |

For this course, **Surefire with `RunCucumberTest`** is sufficient and simplest. Teams that start a test environment in the build use Failsafe and name the runner `RunCucumberIT`. The principle is identical. A Failsafe setup needs its own plugin entry with goals `integration-test` and `verify`; check the Failsafe documentation before using it.

Useful Surefire settings:

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>${surefire.version}</version>
  <configuration>
    <includes>
      <include>**/RunCucumberTest.java</include>          <!-- only this runner by default -->
    </includes>
    <testFailureIgnore>false</testFailureIgnore>           <!-- true = build continues even if tests fail (use with care) -->
    <redirectTestOutputToFile>false</redirectTestOutputToFile>
    <systemPropertyVariables>
      <browser>${browser}</browser>
      <headless>${headless}</headless>
      <cucumber.filter.tags>${cucumber.filter.tags}</cucumber.filter.tags>
    </systemPropertyVariables>
  </configuration>
</plugin>
```

**Line-by-line:**

| Element | Meaning |
|---|---|
| `<includes><include>**/RunCucumberTest.java</include>` | Only classes matching this pattern are test classes. `**/` means "in any package". |
| `<testFailureIgnore>false</testFailureIgnore>` | `false` (the default): when a scenario fails, the build fails. `true`: failures are recorded but the build continues (and ends `BUILD SUCCESS` if nothing else is wrong). |
| `<redirectTestOutputToFile>false</redirectTestOutputToFile>` | `false`: the `pretty` output appears in the console. `true`: it is written to files in `surefire-reports` (keeps the console quiet in big suites). |
| `<systemPropertyVariables>` | The properties passed to the test JVM (Section 7). |

- With `includes`, `mvn test` runs one runner and avoids running smoke and regression runners twice.
- `-Dtest=RunSmokeTest` on the command line **overrides** `includes` and runs that class.
- `testFailureIgnore=true` is sometimes used so that reports are always generated afterward; many teams prefer to keep it `false` so that **the build fails when tests fail**, which is the point of automation in a pipeline. If you set it to `true`, another step must still fail the pipeline.

### 7. Passing Parameters from the Command Line

Everything with `-D` becomes a **Java system property**:

```
mvn clean test -Dbrowser=firefox -Dheadless=true -Dcucumber.filter.tags="@smoke and not @slow"
```

How the pieces connect:

```
-Dbrowser=firefox         Maven user property
        |
        v (pom: ${browser} in surefire systemPropertyVariables)
System.getProperty("browser")        in TestContext / DriverFactory  -> creates FirefoxDriver
```

Surefire also forwards Maven user properties to the test JVM automatically in current versions, but listing them in `systemPropertyVariables` makes the **supported parameters explicit and documents their defaults**.

On the Java side the framework reads them like this (a small piece of the `DriverFactory` idea from earlier this week):

```java
String browser = System.getProperty("browser", "chrome");          // default if missing
boolean headless = Boolean.parseBoolean(System.getProperty("headless", "false"));
```

`System.getProperty(name, default)` returns the value passed by Maven, or the default when the property is absent. This keeps the IDE (where no `-D` is passed) working with sensible defaults.

**Tip:** Quote values that contain spaces (tag expressions). On Windows PowerShell, you may need to wrap the entire `-D...` argument in quotes: `mvn test "-Dcucumber.filter.tags=@smoke and not @slow"`.

### 8. Profiles: Named Configurations

A **profile** is a named group of settings that you switch on with `-P`. Use them for common test selections:

```xml
<profiles>
  <profile>
    <id>smoke</id>
    <properties>
      <cucumber.filter.tags>@smoke and not @wip</cucumber.filter.tags>
    </properties>
  </profile>

  <profile>
    <id>regression</id>
    <properties>
      <cucumber.filter.tags>@regression and not @wip</cucumber.filter.tags>
    </properties>
  </profile>

  <profile>
    <id>ci</id>
    <properties>
      <headless>true</headless>
      <browser>chrome</browser>
    </properties>
  </profile>
</profiles>
```

**Line-by-line:** `<profiles>` holds all profiles; each `<profile>` has an `<id>` (the name you pass to `-P`) and its own `<properties>` block. When a profile is active, its properties **replace** the top-level properties of the same name. The profile does not run anything by itself; it changes the values that `systemPropertyVariables` then forwards.

Use:

```
mvn clean test -Psmoke
mvn clean test -Pregression,ci            # several profiles at once
mvn clean test -Psmoke -Dbrowser=edge     # profile + override
```

**Precedence: command-line `-D` beats a profile's properties, which beat the top-level `<properties>`.** A table of the same setting at different levels, for `cucumber.filter.tags`:

| Command | Top-level property | Profile property | Effective value |
|---|---|---|---|
| `mvn test` | `not @wip and not @ignore` | (none active) | `not @wip and not @ignore` |
| `mvn test -Psmoke` | `not @wip and not @ignore` | `@smoke and not @wip` | `@smoke and not @wip` |
| `mvn test -Psmoke -Dcucumber.filter.tags="@cart"` | `not @wip and not @ignore` | `@smoke and not @wip` | `@cart` |
| `mvn test -Pregression,smoke` | ... | both define the property | The profile **activated last in the order Maven applies them** wins; avoid combining profiles that set the same property |

Profiles give newcomers short, memorable commands (`-Psmoke`) and keep complicated tag expressions in one reviewed place.

**Check which profiles are active:** `mvn help:active-profiles -Psmoke` lists them, and `mvn help:effective-pom -Psmoke` shows the resulting POM including the final property values.

**A caution about two filter sources.** If the runner class also hard-codes `FILTER_TAGS_PROPERTY_NAME` as an annotation, the Maven value may not be able to override it (see the *JUnit Integration* lesson on precedence). Keep the tag default in the POM property (and Surefire `systemPropertyVariables`) and **leave the tag annotation off the runner**, or verify by counting scenarios.

### 9. Where the Output Goes

After `mvn clean test` you will find under `target/`:

| Path | Content |
|---|---|
| `target/classes`, `target/test-classes` | Compiled code |
| `target/surefire-reports/` | JUnit XML and text results (consumed by CI servers) |
| `target/cucumber-reports/` | Cucumber reports from the plug-ins you configured (HTML, JSON, ...); see the next lesson |
| `target/rerun.txt` | Failed scenarios, if the `rerun` plug-in is enabled |
| `screenshots/` | Files from your `ScreenshotUtil`, if you save them to disk |

The **exit code** of `mvn` is `0` on success and non-zero when tests fail or the build breaks. CI servers use it to mark the pipeline green or red. On a shell you can see it with `echo $?` (Linux/macOS) or `echo %ERRORLEVEL%` (Windows cmd).

### 10. Maven in Continuous Integration (Overview)

> **Orientation only.** The pipeline examples below are not something you must build this week. They show that the commands you already know are the same ones a server runs. Pipeline syntax and runner images change, so check the current documentation of your CI product.

A pipeline job is, at heart, a few commands on a clean machine:

```
git clone <repository>
mvn clean test -Pregression,ci
# publish target/surefire-reports and target/cucumber-reports as artifacts
```

Example **GitHub Actions** workflow (`.github/workflows/tests.yml`), shown for orientation only:

```yaml
name: BDD tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17
          cache: maven
      - name: Run smoke tests headless
        run: mvn -B clean test -Psmoke,ci
      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: cucumber-reports
          path: target/cucumber-reports
```

**Line-by-line (orientation):**

| Line | Meaning |
|---|---|
| `on: [push, pull_request]` | Run on every push and every pull request: the smoke tripwire. |
| `runs-on: ubuntu-latest` | A fresh virtual Linux machine for each run: no leftover state, no display. |
| `actions/checkout@v4` | Downloads your repository onto the machine. |
| `actions/setup-java@v4` ... `cache: maven` | Installs JDK 17 and caches `~/.m2` so later runs are faster. |
| `mvn -B clean test -Psmoke,ci` | `-B` = batch mode (clean logs without progress bars); `-Psmoke,ci` selects smoke tags and headless Chrome. |
| `if: always()` | Run the upload step **even if the test step failed**, so the report of the failure is available. |

Observations: **headless** (the server has no display), `-B` (batch mode: cleaner logs), `if: always()` (upload reports even when tests fail), and Chrome is available on the hosted runner. Setting up full pipelines (Jenkins, Docker, Grid) is outside this week's scope, but a framework that runs with a single Maven command is **CI-ready** by design.

**Scenario: smoke on every commit, regression every night.** A second workflow (also orientation only) can use a schedule:

```yaml
name: Nightly regression
on:
  schedule:
    - cron: "0 2 * * *"        # 02:00 UTC every day
jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: 17, cache: maven }
      - run: mvn -B clean test -Pregression,ci
      - if: always()
        uses: actions/upload-artifact@v4
        with: { name: nightly-reports, path: target }
```

The same framework, a different profile: this is why profiles and tags matter.

### 11. Troubleshooting Maven

| Symptom | Likely cause | Fix |
|---|---|---|
| `release version 17 not supported` / `invalid target release` | JDK older than `maven.compiler.release` | Install JDK 17 or lower the compiler version; check `JAVA_HOME` and `mvn -version` |
| `Could not resolve dependencies` | No internet/proxy, typo in coordinates/version | Check network/proxy settings (`~/.m2/settings.xml`), correct the coordinates |
| `Tests run: 0` | Runner name not matching, `includes` pattern wrong, missing platform suite dependency | See the *JUnit Integration* troubleshooting |
| `-Dbrowser=...` seems ignored | Not forwarded, or code reads a different property name | Confirm `systemPropertyVariables` and the `System.getProperty` key |
| Tag filter selects nothing | Typo, unquoted expression | Quote it, check tags |
| Strange class or method errors after changing versions | Stale compiled classes or cache | `mvn clean test`; delete the offending folder in `~/.m2/repository` |
| `NoSuchMethodError` / `ClassNotFoundException` | Dependency version conflict | `mvn dependency:tree`; align versions (use BOMs, one `cucumber.version`) |
| Garbled characters in output/feature text | Encoding | Set `project.build.sourceEncoding` to UTF-8 |
| Build works in IDE but fails in Maven (or the reverse) | Different JDK or settings | Align the IDE's Maven/JDK with the command line |
| Very slow first build | Downloading dependencies | Normal once; later builds use the local cache |

**Real messages and their diagnosis**

1. **Wrong JDK**

   ```
   [ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.13.0:compile
   (default-compile) on project bdd-framework: Fatal error compiling: error: invalid target release: 17
   ```

   Diagnosis: Maven runs on a JDK older than 17. Run `mvn -version`; the line `Java version:` shows the JDK **Maven** uses (not necessarily the one your IDE uses). Fix `JAVA_HOME` or install JDK 17.

2. **Typo in a dependency**

   ```
   [ERROR] Failed to execute goal on project bdd-framework: Could not resolve dependencies for project
   com.revature.qea:bdd-framework:jar:1.0-SNAPSHOT: Could not find artifact io.cucumber:cucumber-java:jar:7.99.9 in central
   ```

   Diagnosis: Maven looked for exactly that version and it does not exist. Check the version on Maven Central. If the message says `Could not transfer artifact ... Connect timed out` or `PKIX path building failed`, it is a network/proxy/certificate issue instead; ask your network team for proxy settings in `~/.m2/settings.xml`.

3. **Offline mode without cached libraries**

   ```
   [ERROR] Cannot access central in offline mode and the artifact org.seleniumhq.selenium:selenium-java:jar:4.25.0 has not been downloaded from it before.
   ```

   Diagnosis: you used `-o` (or settings force offline) but the library was never downloaded. Run once online.

4. **No tests found**

   ```
   [ERROR] No tests were executed!  (Set -DfailIfNoTests=false to ignore this error.)
   ```

   Diagnosis: Surefire found no matching class or the runner selected no scenarios. Check class naming, `includes`, and the tag expression.

5. **Failing tests (normal behavior)**

   ```
   [ERROR] Tests run: 7, Failures: 1, Errors: 0, Skipped: 0
   [ERROR] Failed to execute goal ...:surefire:3.5.0:test (default-test) on project bdd-framework:
   There are test failures.
   [INFO] BUILD FAILURE
   ```

   Diagnosis: this is not a Maven problem; a scenario failed. Open `target/cucumber-reports/report.html` for the details.

---

## Complete Example: One-Command Workflow

1. A teammate clones the repository.
2. They run:

   ```
   mvn clean test -Psmoke
   ```
3. Maven compiles the code, starts the JUnit Platform, runs only `@smoke` scenarios in Chrome, and writes the HTML report to `target/cucumber-reports/`.
4. For the nightly build the pipeline runs:

   ```
   mvn clean test -Pregression,ci -Dbrowser=chrome
   ```
5. If any scenario fails, the exit code is non-zero, the pipeline turns red, and the screenshot attached by the `@After` hook is visible in the published report.

A short **README** section makes this discoverable:

```markdown
## Running the tests
| Goal | Command |
|---|---|
| Smoke tests | `mvn clean test -Psmoke` |
| Full regression (headless) | `mvn clean test -Pregression,ci` |
| One tag | `mvn clean test -Dcucumber.filter.tags="@cart"` |
| Another browser | `mvn clean test -Dbrowser=firefox` |
| Check steps only | `mvn test -Dcucumber.execution.dry-run=true` |
Reports: `target/cucumber-reports/report.html`
```

---

## Guided Lab: Make Project 2 Runnable With One Command

**Goal:** Turn your Project 2 BDD project (saucedemo.com login, cart, and checkout scenarios) into a framework that a classmate can run from a fresh clone.

1. **Check the layout.** Confirm features are in `src/test/resources/features` and runner and steps in `src/test/java`. Create or update `.gitignore` with `target/`.
2. **Check the tools.** Run `mvn -version`. **Expected:** Maven 3.x and a Java version of 17 or higher. If not, fix `JAVA_HOME`.
3. **Centralize versions.** In `<properties>`, define `selenium.version`, `cucumber.version`, `junit.version`, `junit.platform.version`, and `surefire.version` (use versions you have verified on Maven Central). Replace literal versions in dependencies with `${...}`.
4. **Add test parameters.** Add `<browser>chrome</browser>`, `<headless>false</headless>`, and `<cucumber.filter.tags>not @wip and not @ignore</cucumber.filter.tags>` to `<properties>`.
5. **Forward them.** Add the Surefire `<systemPropertyVariables>` block from Section 6. Add `System.getProperty("browser", "chrome")` handling to your `DriverFactory` if it is not already there.
6. **Run the default.** `mvn clean test`. **Expected:** the annotated log from Section 5.1, then `Tests run: N` and `BUILD SUCCESS`. Write down N.
7. **Add profiles.** Add `smoke`, `regression`, and `ci` profiles. Tag at least three scenarios with `@smoke` and the rest with `@regression`.
8. **Run smoke.** `mvn clean test -Psmoke`. **Expected:** a smaller N, equal to the number of `@smoke` scenarios (count outline Examples rows individually).
9. **Prove precedence.** `mvn clean test -Psmoke -Dcucumber.filter.tags="@regression"`. **Expected:** the count of `@regression` scenarios, because `-D` beats the profile. If the count does not change, check whether your runner hard-codes the tag filter.
10. **Prove parameter forwarding.** Temporarily print `System.getProperty("browser")` and `System.getProperty("headless")` in a `@Before` hook. Run `mvn test -Dbrowser=edge -Dheadless=true`. **Expected:** `edge` and `true` printed. Remove the print.
11. **Inspect the dependency tree.** `mvn dependency:tree > tree.txt`. Find the line for `selenium-api` and write which direct dependency brought it in.
12. **Inspect effective settings.** `mvn help:effective-pom -Psmoke` and find the `cucumber.filter.tags` value.
13. **Write the README table** from the Complete Example, with the commands you verified.
14. **Fresh-clone test.** Clone the repository into a new folder (or ask a classmate) and follow only the README. Fix the README for anything that was unclear.

**Deliverable:** the updated `pom.xml`, the README "Running the tests" section, and one sentence for each of steps 6, 8, 9, and 10 stating the observed value.

---

## Practice Exercises

1. **Read the POM.** For each dependency in the example, write what it is for and why it has its scope.
2. **Lifecycle.** Run `mvn compile`, `mvn test-compile`, `mvn test`, and `mvn clean test`. Which folders appear in `target/` after each?
3. **Parameters.** Add `systemPropertyVariables` for `browser` and `headless`. Run `mvn test -Dbrowser=edge -Dheadless=true` and prove (with a print statement or a screenshot) that the values arrived.
4. **Profiles.** Create `smoke`, `regression`, and `ci` profiles. Run `mvn test -Psmoke` and confirm the number of scenarios executed.
5. **Precedence.** Run `mvn test -Psmoke -Dcucumber.filter.tags="@regression"`. Which wins, and why?
6. **Dependency tree.** Run `mvn dependency:tree` and find where `selenium-api` and `cucumber-core` come from.
7. **Break and fix.** Set `maven.compiler.source` to 21 on a machine with JDK 17 and read the error; then fix it. Next, mistype a dependency version and read that error.
8. **Single runner.** Add the Surefire `includes` so that only `RunCucumberTest` runs. Add a `RunSmokeTest` class and verify that plain `mvn test` does **not** run it twice.
9. **README and CI.** Add a "Running the tests" section to your Project 2 README with the commands that work on a fresh clone. Ask a classmate to follow it.
10. **Scope experiment.** Change `selenium-java` to `<scope>test</scope>` while a page object in `src/main/java` imports Selenium. Predict the error, run `mvn compile`, compare, and restore.
11. **BOM.** Add the `junit-bom` import from Section 4.4, remove the explicit versions from the two JUnit dependencies, and confirm the build still works with `mvn dependency:tree`.
12. **Orientation CI.** Without running it, explain each line of the GitHub Actions example and decide which profile you would use for a pull-request check versus a nightly job, with a reason.

---

## Solutions and Hints

1. **Read the POM.** `selenium-java` (`compile`): browser automation, used by page objects in `src/main`. `cucumber-java` (`test`): annotations for steps and hooks. `cucumber-junit-platform-engine` (`test`): the engine that lets JUnit run features. `cucumber-picocontainer` (`test`): shares `TestContext` between step classes per scenario. `junit-jupiter` (`test`): assertions and the Jupiter engine. `junit-platform-suite` (`test`): the `@Suite` annotations for the runner. All but Selenium are test-only.
2. **Lifecycle.** `compile`: `target/classes`. `test-compile`: adds `target/test-classes`. `test`: adds `surefire-reports` and any Cucumber report folders. `clean test`: deletes everything first, then rebuilds. Hint: look inside `target/` after each command.
3. **Parameters.** Print in a hook or the driver factory: `System.out.println("browser=" + System.getProperty("browser"))`. Expect `edge`. If you see `chrome`, check the property names (case-sensitive).
4. **Profiles.** Compare the count of tests with the number of `@smoke` scenarios in your feature files, counting each Examples row.
5. **Precedence.** `-D` wins; command-line user properties override profile properties, which override top-level properties. The effective tag value is `@regression`. If it does not, the runner annotation may be overriding (see JUnit lesson).
6. **Dependency tree.** `selenium-api` appears beneath `selenium-java`. `cucumber-core` appears beneath `cucumber-java` (and the platform engine). Hint: indentation shows who needs whom.
7. **Break and fix.** The error resembles `invalid target release: 21` (or `release version 21 not supported`). Fix: set 17 again, or install JDK 21 and point `JAVA_HOME` to it. A mistyped version produces `Could not find artifact ...` naming the exact coordinates.
8. **Single runner.** With `<includes>` listing only `RunCucumberTest.java`, `mvn test` runs one runner. `mvn test -Dtest=RunSmokeTest` still runs the smoke runner because `-Dtest` overrides includes.
9. **README and CI.** Typical missing items found by a classmate: the JDK version, the Chrome requirement, a missing `-P` flag, or where the report is.
10. **Scope experiment.** The compile phase of `src/main` fails with `package org.openqa.selenium does not exist` because test-scope libraries are not visible to main code. Restore the default `compile` scope.
11. **BOM.** The tree should show the same JUnit versions as the BOM. If versions do not appear, you may have forgotten `<type>pom</type>` or `<scope>import</scope>`.
12. **Orientation CI.** `checkout` fetches code; `setup-java` installs JDK and caches Maven; `mvn -B clean test -Psmoke,ci` runs headless smoke; `if: always()` uploads reports even after failure. A pull request wants fast feedback: `-Psmoke,ci`. Nightly can afford the full `-Pregression,ci`.

---

## Self-Check Questions

1. **What does `mvn clean test` do?** It deletes `target/`, compiles main and test code, copies resources, and runs the tests through Surefire.
2. **Which wins: `-Dbrowser=edge` or `<browser>chrome</browser>` in `<properties>`?** The command-line value (`edge`). Order: command line, then active profile, then top-level properties.
3. **What is a transitive dependency?** A library that one of your dependencies needs; Maven downloads it automatically. `mvn dependency:tree` shows it.
4. **Two libraries need different versions of the same dependency. Which version is used?** The nearest one in the tree; if tied, the one declared first. A mismatch can cause `NoSuchMethodError` at runtime.
5. **Which scope for Cucumber and JUnit, and for Selenium in our framework?** `test` for Cucumber and JUnit; `compile` (default) for Selenium because page objects in `src/main` use it.
6. **Why use `-B` and headless in CI?** `-B` gives clean logs without interactive progress output; headless because CI machines have no display.
7. **How does CI know tests failed?** Maven exits with a non-zero code, which the CI server maps to a failed job.
8. **Why might a report not appear after a failed run, and how is it handled?** With `testFailureIgnore=false` the build stops before later phases such as `verify`; teams use `testFailureIgnore=true` plus a step that fails the pipeline, or an always-run CI step. The *Cucumber Reporting* lesson covers this.

---

## Summary

- **Maven** standardizes the project layout, **downloads dependencies**, and gives a **repeatable command line** (`mvn clean test`), which is what CI servers run.
- The **`pom.xml`** defines coordinates, **properties** (versions, defaults), **dependencies** with **scopes**, and **plugins**; keep all Cucumber artifacts on one `cucumber.version`. All version numbers are examples to check.
- **Transitive dependencies** come automatically; conflicts are resolved by **nearest wins**; use `mvn dependency:tree`, BOMs, and `dependencyManagement` to see and control versions.
- **Surefire** runs tests in the `test` phase (class names ending in `Test`); **Failsafe** runs `*IT` classes in `verify` for integration-style pipelines.
- Pass settings with **`-D`** (browser, headless, tags) and forward them via **`systemPropertyVariables`**; precedence: command line > profile > top-level properties.
- **Profiles** (`-Psmoke`, `-Pregression`, `-Pci`) give short names to common configurations.
- Results appear in **`target/`** (`surefire-reports`, `cucumber-reports`); the **exit code** drives pipeline status.
- CI examples in this lesson are **orientation only**; the point is that a one-command Maven framework is CI-ready.
- Most problems are **JDK/version**, **dependency conflicts**, **network/proxy**, or **runner naming**; `mvn dependency:tree` and `mvn clean` are your first tools.

---

## Additional Resources

- Apache Maven, *Maven in 5 Minutes* and *Introduction to the Build Lifecycle*: https://maven.apache.org/guides/getting-started/
- Apache Maven Surefire Plugin documentation: https://maven.apache.org/surefire/maven-surefire-plugin/
- Cucumber-JVM, *Running with Maven (cucumber-java skeleton / JUnit Platform)*: https://github.com/cucumber/cucumber-jvm/tree/main/cucumber-junit-platform-engine
