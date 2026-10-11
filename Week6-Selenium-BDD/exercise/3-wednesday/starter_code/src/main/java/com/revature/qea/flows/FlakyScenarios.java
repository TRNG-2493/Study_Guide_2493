package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * GIVEN (working code from an earlier day) - the four scenarios, stabilised with WaitUtils (no sleeps, no implicit wait).
 *
 * Root causes
 *   S1  hidden element        -> getText() on a hidden element returns "" (no exception!): wait for VISIBILITY.
 *   S2  element added later   -> NoSuchElementException: wait for the element to EXIST and be visible.
 *   S3  dynamic controls      -> NoSuchElement (#message not there yet), StaleElementReference (checkbox left the DOM),
 *                                ElementNotInteractable (disabled input): wait for the spinner to go, for the count to be 0,
 *                                and for the input to be clickable (enabled).
 *   S4  bad login             -> race between click and banner render: wait for the banner to be VISIBLE.
 */
public class FlakyScenarios {

    private static final String INTERNET = "https://the-internet.herokuapp.com/";
    private static final String SAUCE = "https://www.saucedemo.com/";

    static void s1HiddenElement() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(INTERNET + "dynamic_loading/1");
            waits.click(By.cssSelector("#start button"));
            String text = waits.textOf(By.cssSelector("#finish h4"));   // waits for VISIBLE, not just present
            Check.equal("S1 loaded text", "Hello World!", text);
        } finally {
            driver.quit();
        }
    }

    static void s2ElementAddedLater() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(INTERNET + "dynamic_loading/2");
            waits.click(By.cssSelector("#start button"));
            String text = waits.textOf(By.cssSelector("#finish h4"));
            Check.equal("S2 loaded text", "Hello World!", text);
        } finally {
            driver.quit();
        }
    }

    static void s3DynamicControls() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(INTERNET + "dynamic_controls");

            // (a) remove the checkbox - never hold a WebElement across a DOM change; use By + counts
            waits.visible(By.id("checkbox"));
            waits.click(By.cssSelector("#checkbox-example button"));
            waits.disappears(By.id("loading"));
            Check.equal("S3a message", "It's gone!", waits.textOf(By.id("message")));
            waits.countToBe(By.id("checkbox"), 0);
            Check.that("S3a checkbox is gone from the page", driver.findElements(By.id("checkbox")).isEmpty());

            // (b) enable the input - clickable = displayed AND enabled
            waits.click(By.cssSelector("#input-example button"));
            WebElement input = waits.clickable(By.cssSelector("#input-example input"));
            input.sendKeys("hello");
            Check.equal("S3b typed text", "hello", input.getAttribute("value"));
        } finally {
            driver.quit();
        }
    }

    static void s4BadLoginError() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(SAUCE);
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.id("password"), "wrong_password");
            waits.click(By.id("login-button"));
            String error = waits.textOf(By.cssSelector("[data-test='error']"));
            Check.equal("S4 error banner",
                    "Epic sadface: Username and password do not match any user in this service", error);
        } finally {
            driver.quit();
        }
    }
}
