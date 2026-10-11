package com.revature.qea.steps;

import com.revature.qea.support.TestContext;
// TODO: add the imports you need (io.cucumber.java.Before, After, BeforeAll, AfterAll, Scenario,
//       org.openqa.selenium.OutputType, org.openqa.selenium.TakesScreenshot)

/**
 * TODO (Part 2) - the browser lifecycle and failure evidence. Read hooks.md before you start.
 *
 * Required (the automated test BddLayerRulesTest checks for these words):
 *   1. @BeforeAll  - a STATIC method that prints one banner line (browser, headless, tags).
 *   2. @Before(order = 0) - logs the scenario name with scenario.log(...) and starts the browser: context.driver().
 *   3. @Before(value = "@slow", order = 5) - a TAGGED hook that only logs a warning for @slow scenarios.
 *   4. @After(order = 10) - runs FIRST on the way out: if scenario.isFailed(), take a screenshot with
 *      ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES) and scenario.attach(png, "image/png", name).
 *      Wrap the screenshot in try/catch so a screenshot problem never hides the real failure.
 *   5. @After(order = 0)  - runs LAST: context.quitDriver().
 *   6. @AfterAll   - a STATIC method that prints one closing line.
 *
 * Remember: BEFORE hooks run in ASCENDING order, AFTER hooks run in DESCENDING order.
 * No sleeps. No By / findElement. Hooks get the SAME TestContext as the steps (constructor injection).
 */
public class Hooks {

    private final TestContext context;

    public Hooks(TestContext context) {
        this.context = context;
    }

    // TODO: @BeforeAll beforeAll()

    // TODO: @Before(order = 0) setUp(Scenario scenario)

    // TODO: @Before(value = "@slow", order = 5) warnAboutSlowScenario(Scenario scenario)

    // TODO: @After(order = 10) attachEvidence(Scenario scenario)

    // TODO: @After(order = 0) tearDown()

    // TODO: @AfterAll afterAll()
}
