# Tags and Runs - Project 2 BDD layer

Replace every `<<FILL>>` before you submit. The automated test `BddLayerRulesTest` fails while any is left.

## 1. Tag taxonomy

Every tag used in the features must be listed here. One line each: meaning and when to use it.

| Tag | Level | Meaning | Rule for use |
|-----|-------|---------|--------------|
| `@ui` | feature | <<FILL>> | first tag on every feature |
| `@login` / `@cart` / `@sort` | feature | <<FILL>> | <<FILL>> |
| `@smoke` | scenario | <<FILL>> | <<FILL>> (3 to 6 scenarios, from at least 3 features) |
| `@regression` | scenario | <<FILL>> | <<FILL>> |
| `@wip` | scenario | <<FILL>> | <<FILL>> |
| `@slow` | scenario | <<FILL>> | <<FILL>> |
| `@positive` / `@negative` | scenario | <<FILL>> | <<FILL>> |
| `@report-demo` | scenario | <<FILL>> | temporary: used once for the failing-scenario evidence, never committed on a scenario |

## 2. Run matrix

For each command write what runs, roughly how many scenarios, and when a team would use it.

| Command | Tag expression in effect | Scenarios that run | When to use it |
|---------|--------------------------|--------------------|----------------|
| `mvn clean test` | <<FILL>> | <<FILL>> | <<FILL>> |
| `mvn clean test -Psmoke` | <<FILL>> | <<FILL>> | <<FILL>> |
| `mvn clean test -Pregression` | <<FILL>> | <<FILL>> | <<FILL>> |
| `mvn clean test -Pci` | <<FILL>> | <<FILL>> | <<FILL>> |
| `mvn clean test -Dcucumber.filter.tags="@cart and not @slow"` | <<FILL>> | <<FILL>> | <<FILL>> |
| `mvn clean verify -Psmoke -Pci` | <<FILL>> | <<FILL>> | <<FILL>> |

## 3. Where the reports are

| File | Produced by | Who reads it |
|------|-------------|--------------|
| `target/cucumber-reports/report.html` | <<FILL>> | <<FILL>> |
| `target/cucumber-reports/cucumber.json` | <<FILL>> | <<FILL>> |
| `target/cucumber-reports/cucumber.xml` | <<FILL>> | <<FILL>> |
| `target/rerun.txt` | <<FILL>> | <<FILL>> |
| `target/cucumber-html-reports/overview-features.html` | <<FILL>> | <<FILL>> |

## 4. Failure evidence (Part 3, step 6)

Describe the deliberate failure you created, what the report showed (screenshot attached? which step was red?),
and how you reverted it.

<<FILL>>
