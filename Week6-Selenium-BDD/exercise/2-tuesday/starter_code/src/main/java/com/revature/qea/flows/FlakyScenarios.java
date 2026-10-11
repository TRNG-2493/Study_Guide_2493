package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * TODO (Part 1) - STABILISE THESE FLAKY SCENARIOS.
 *
 * Four scenarios written by a colleague who "ran them once and they passed" (they were
 * checked on a fast laptop). They race the browser: they act before the page is ready.
 *
 * YOUR JOB
 *   1. (Task 1.1) Run each scenario as-is and record the baseline pass-rate (FlakinessRun).
 *   2. (Task 1.3) Fix every scenario using WaitUtils - NO Thread.sleep, NO implicit wait.
 *   3. (Task 1.4) Re-run until each scenario passes 10/10.
 *   4. (Task 1.5) Record the root cause of every scenario in FLAKINESS_REPORT.md.
 *
 * Rules: do not change what a scenario CHECKS (the expected texts stay the same) - change HOW it waits.
 * Search for the markers "// BUG?" to find suspicious lines. Each scenario fails with a DIFFERENT exception
 * (or a wrong value) - the exception name is your clue.
 */
public class FlakyScenarios {

    private static final String INTERNET = "https://the-internet.herokuapp.com/";
    private static final String SAUCE = "https://www.saucedemo.com/";

    /**
     * S1 - dynamic_loading/1: the "Hello World!" heading IS in the page from the start, but hidden.
     * Click Start; after ~5 s of loading the heading becomes visible.
     */
    static void s1HiddenElement() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            driver.get(INTERNET + "dynamic_loading/1");
            driver.findElement(By.cssSelector("#start button")).click();
            String text = driver.findElement(By.cssSelector("#finish h4")).getText();   // BUG?
            Check.equal("S1 loaded text", "Hello World!", text);
        } finally {
            driver.quit();
        }
    }

    /**
     * S2 - dynamic_loading/2: here the heading does NOT exist until loading finishes (~5 s).
     * Same check as S1, different failure. Think: is this the same wait as S1?
     */
    static void s2ElementAddedLater() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            driver.get(INTERNET + "dynamic_loading/2");
            driver.findElement(By.cssSelector("#start button")).click();
            String text = driver.findElement(By.cssSelector("#finish h4")).getText();   // BUG?
            Check.equal("S2 loaded text", "Hello World!", text);
        } finally {
            driver.quit();
        }
    }

    /**
     * S3 - dynamic_controls: two AJAX actions.
     *   (a) "Remove" deletes the checkbox after ~a second and then shows the message "It's gone!"
     *   (b) "Enable" turns a DISABLED text box into an enabled one after ~a few seconds.
     */
    static void s3DynamicControls() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            driver.get(INTERNET + "dynamic_controls");

            WebElement checkbox = driver.findElement(By.id("checkbox"));                 // BUG?
            driver.findElement(By.cssSelector("#checkbox-example button")).click();
            String message = driver.findElement(By.id("message")).getText();             // BUG?
            Check.equal("S3a message", "It's gone!", message);
            Check.that("S3a checkbox is gone from the page", !checkbox.isDisplayed());   // BUG?

            driver.findElement(By.cssSelector("#input-example button")).click();
            WebElement input = driver.findElement(By.cssSelector("#input-example input"));
            input.sendKeys("hello");                                                     // BUG?
            Check.equal("S3b typed text", "hello", input.getAttribute("value"));
        } finally {
            driver.quit();
        }
    }

    /**
     * S4 - SauceDemo: a wrong password must show an error banner.
     * This one often passes on a fast machine - "it passed once" is not "it is stable".
     * Fix it with the same discipline anyway (WaitUtils for every interaction).
     */
    static void s4BadLoginError() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            driver.get(SAUCE);
            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.id("password")).sendKeys("wrong_password");
            driver.findElement(By.id("login-button")).click();
            String error = driver.findElement(By.cssSelector("[data-test='error']")).getText();   // BUG?
            Check.equal("S4 error banner",
                    "Epic sadface: Username and password do not match any user in this service", error);
        } finally {
            driver.quit();
        }
    }
}
