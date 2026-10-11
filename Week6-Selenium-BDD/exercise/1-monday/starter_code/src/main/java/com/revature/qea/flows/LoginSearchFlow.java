package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.ScreenshotUtil;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

/**
 * TODO (Part 1 - the individual lab): automate a LOGIN and a PRODUCT-SEARCH flow on https://www.saucedemo.com
 *
 * Run it with:
 *   mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.LoginSearchFlow
 *   (add -Dbrowser=firefox  or  -Dheadless=true)
 *
 * Rules for this lab (Monday topics only - waits come tomorrow)
 *   * Always create the browser with DriverFactory.createDriver() and always quit() it in a finally block.
 *   * You may use ONE clearly commented pause(...) helper where SauceDemo needs a moment after login
 *     ("TEMPORARY: replaced by a proper wait on Tuesday"). No other Thread.sleep.
 *   * Use at least 4 different By strategies across the lab (id, name, className, cssSelector, xpath, ...).
 */
public class LoginSearchFlow {

    private static final String BASE_URL = "https://www.saucedemo.com/";
    private static final String PASSWORD = "secret_sauce";

    public static void main(String[] args) throws Exception {
        happyPathLoginAndSearch();
        lockedOutUser();
    }

    /** Task 1.1 - 1.4 */
    static void happyPathLoginAndSearch() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO 1.1  open BASE_URL and Check.equal the page title ("Swag Labs")
            // TODO 1.2  log in as standard_user (locate the fields, type, click Login), then pause(...) briefly
            //           Check.that the URL contains "inventory" and Check.equal the heading text is "Products"
            // TODO 1.3  SEARCH: use findElements(By.className("inventory_item_name")) and loop through the names
            //           to find "Sauce Labs Fleece Jacket"; record its position and read its price from the SAME
            //           product card (scoped search from the card element: card.findElement(...)).
            //           Check.equal the price is "$49.99" and Check.equal the product count is 6
            // TODO 1.4  click the product's name, Check.that the URL contains "inventory-item", read the detail-page
            //           name and price, Check.equal they match what you read on the list page,
            //           navigate().back() and Check.that you are on the inventory page again.
            //           Take a screenshot named "monday-search-pass" with ScreenshotUtil.
        } finally {
            driver.quit();
        }
    }

    /** Task 1.5 - negative path */
    static void lockedOutUser() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO 1.5  log in as locked_out_user; use findElements(...) to Check.equal that NO error banner exists
            //           BEFORE login (size 0), then after login read the error text
            //           ("Epic sadface: Sorry, this user has been locked out.") and screenshot it ("monday-locked-out").
        } finally {
            driver.quit();
        }
    }

    /** The ONLY allowed sleep. TEMPORARY: replaced by a proper wait on Tuesday. */
    private static void pause(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
