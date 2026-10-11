package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.ScreenshotUtil;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

/**
 * Monday's flow (given, working) - TODO Task 2.1: REFACTOR it for stability.
 *
 *   * Replace EVERY pause(...) with a proper wait from WaitUtils (and then delete the pause helper).
 *   * Use WaitUtils for the typing and clicking too, so the flow no longer depends on timing.
 *   * Keep every Check exactly as it is - same expectations, same labels.
 *   * Acceptance test: grep the project for "Thread.sleep" - zero hits.
 */
public class LoginSearchFlow {

    private static final String BASE_URL = "https://www.saucedemo.com/";
    private static final String PASSWORD = "secret_sauce";

    public static void main(String[] args) throws Exception {
        happyPathLoginAndSearch();
        lockedOutUser();
    }

    static void happyPathLoginAndSearch() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // 1.1
            driver.get(BASE_URL);
            Check.equal("1.1 login page title", "Swag Labs", driver.getTitle());

            // 1.2  (id, id, id strategies)
            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.name("password")).sendKeys(PASSWORD);
            driver.findElement(By.cssSelector("input[data-test='login-button']")).click();
            pause(1000);   // TEMPORARY: replaced by a proper wait on Tuesday
            Check.that("1.2 URL contains inventory", driver.getCurrentUrl().contains("inventory"));
            Check.equal("1.2 heading", "Products", driver.findElement(By.className("title")).getText());

            // 1.3 search: loop over the product cards, scoped lookups inside the matching card
            List<WebElement> cards = driver.findElements(By.className("inventory_item"));
            Check.equal("1.3 product count", 6, cards.size());

            WebElement match = null;
            int position = -1;
            for (int i = 0; i < cards.size(); i++) {
                String name = cards.get(i).findElement(By.className("inventory_item_name")).getText();
                if (name.equals("Sauce Labs Fleece Jacket")) {
                    match = cards.get(i);
                    position = i + 1;
                    break;
                }
            }
            Check.that("1.3 product found", match != null);
            String listName = match.findElement(By.className("inventory_item_name")).getText();
            String listPrice = match.findElement(By.xpath(".//div[@class='inventory_item_price']")).getText();
            System.out.println("INFO  '" + listName + "' is product #" + position + " at " + listPrice);
            Check.equal("1.3 price on list page", "$49.99", listPrice);

            // 1.4 open the product and compare
            match.findElement(By.className("inventory_item_name")).click();
            pause(500);    // TEMPORARY: replaced by a proper wait on Tuesday
            Check.that("1.4 URL contains inventory-item", driver.getCurrentUrl().contains("inventory-item"));
            Check.equal("1.4 detail name", listName, driver.findElement(By.className("inventory_details_name")).getText());
            Check.equal("1.4 detail price", listPrice, driver.findElement(By.className("inventory_details_price")).getText());

            driver.navigate().back();
            pause(500);    // TEMPORARY: replaced by a proper wait on Tuesday
            Check.that("1.4 back on inventory page", driver.getCurrentUrl().contains("inventory.html"));
            ScreenshotUtil.capture(driver, "monday-search-pass");
        } finally {
            driver.quit();
        }
    }

    static void lockedOutUser() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            driver.get(BASE_URL);
            Check.equal("1.5 no error banner before login", 0,
                    driver.findElements(By.cssSelector("[data-test='error']")).size());

            driver.findElement(By.id("user-name")).sendKeys("locked_out_user");
            driver.findElement(By.id("password")).sendKeys(PASSWORD);
            driver.findElement(By.id("login-button")).click();
            pause(500);    // TEMPORARY: replaced by a proper wait on Tuesday

            String error = driver.findElement(By.cssSelector("[data-test='error']")).getText();
            Check.equal("1.5 locked-out message", "Epic sadface: Sorry, this user has been locked out.", error);
            ScreenshotUtil.capture(driver, "monday-locked-out");
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
