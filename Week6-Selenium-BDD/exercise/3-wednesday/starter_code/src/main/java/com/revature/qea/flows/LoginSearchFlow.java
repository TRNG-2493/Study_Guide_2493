package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.ScreenshotUtil;
import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

/** GIVEN (working code from an earlier day) - Monday's flow after the Tuesday refactor: zero sleeps, WaitUtils everywhere. */
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
            WaitUtils waits = new WaitUtils(driver);
            // 1.1
            driver.get(BASE_URL);
            Check.equal("1.1 login page title", "Swag Labs", driver.getTitle());

            // 1.2  (id, id, id strategies)
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.name("password"), PASSWORD);
            waits.click(By.cssSelector("input[data-test='login-button']"));
            waits.waitForUrlContains("inventory");
            Check.that("1.2 URL contains inventory", driver.getCurrentUrl().contains("inventory"));
            Check.equal("1.2 heading", "Products", waits.textOf(By.className("title")));

            // 1.3 search: loop over the product cards, scoped lookups inside the matching card
            List<WebElement> cards = waits.allVisible(By.className("inventory_item"));
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
            waits.waitForUrlContains("inventory-item");
            Check.that("1.4 URL contains inventory-item", driver.getCurrentUrl().contains("inventory-item"));
            Check.equal("1.4 detail name", listName, waits.textOf(By.className("inventory_details_name")));
            Check.equal("1.4 detail price", listPrice, waits.textOf(By.className("inventory_details_price")));

            driver.navigate().back();
            waits.waitForUrlContains("inventory.html");
            Check.that("1.4 back on inventory page", driver.getCurrentUrl().contains("inventory.html"));
            ScreenshotUtil.capture(driver, "monday-search-pass");
        } finally {
            driver.quit();
        }
    }

    static void lockedOutUser() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(BASE_URL);
            Check.equal("1.5 no error banner before login", 0,
                    driver.findElements(By.cssSelector("[data-test='error']")).size());

            waits.type(By.id("user-name"), "locked_out_user");
            waits.type(By.id("password"), PASSWORD);
            waits.click(By.id("login-button"));

            String error = waits.textOf(By.cssSelector("[data-test='error']"));
            Check.equal("1.5 locked-out message", "Epic sadface: Sorry, this user has been locked out.", error);
            ScreenshotUtil.capture(driver, "monday-locked-out");
        } finally {
            driver.quit();
        }
    }
}
