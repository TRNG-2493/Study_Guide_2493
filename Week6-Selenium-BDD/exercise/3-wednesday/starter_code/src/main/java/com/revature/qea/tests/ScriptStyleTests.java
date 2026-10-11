package com.revature.qea.tests;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.DropdownUtils;
import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * GIVEN - do not edit. These are the "Project 2 tests" as they exist TODAY, in script style.
 *
 * Look at them with a critical eye BEFORE you refactor:
 *   * how many times does By.id("user-name") appear?   * how many lines are login boilerplate?
 *   * if SauceDemo renames the login button, how many places must change?
 *
 * Run:  mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.tests.ScriptStyleTests -Dheadless=true
 * Your Page Object version (PomTests) must print the SAME PASS lines.
 */
public class ScriptStyleTests {

    private static final String URL = "https://www.saucedemo.com/";

    public static void main(String[] args) {
        t1LoginSucceeds();
        t2LockedOutUser();
        t3AddTwoProducts();
        t4RemoveFromCart();
        t5SortByPrice();
    }

    static void t1LoginSucceeds() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(URL);
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.id("password"), "secret_sauce");
            waits.click(By.id("login-button"));
            waits.waitForUrlContains("inventory");
            Check.equal("T1 heading after login", "Products", waits.textOf(By.className("title")));
        } finally {
            driver.quit();
        }
    }

    static void t2LockedOutUser() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(URL);
            waits.type(By.id("user-name"), "locked_out_user");
            waits.type(By.id("password"), "secret_sauce");
            waits.click(By.id("login-button"));
            Check.equal("T2 locked-out message",
                    "Epic sadface: Sorry, this user has been locked out.",
                    waits.textOf(By.cssSelector("[data-test='error']")));
        } finally {
            driver.quit();
        }
    }

    static void t3AddTwoProducts() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(URL);
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.id("password"), "secret_sauce");
            waits.click(By.id("login-button"));
            waits.waitForUrlContains("inventory");

            waits.click(By.id("add-to-cart-sauce-labs-backpack"));
            waits.click(By.id("add-to-cart-sauce-labs-bike-light"));
            Check.equal("T3 cart badge", "2", waits.textOf(By.className("shopping_cart_badge")));

            waits.click(By.className("shopping_cart_link"));
            waits.waitForUrlContains("cart");
            List<String> names = waits.allVisible(By.className("inventory_item_name")).stream()
                    .map(WebElement::getText).collect(Collectors.toList());
            Check.equal("T3 cart contents", Arrays.asList("Sauce Labs Backpack", "Sauce Labs Bike Light"), names);
        } finally {
            driver.quit();
        }
    }

    static void t4RemoveFromCart() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            driver.get(URL);
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.id("password"), "secret_sauce");
            waits.click(By.id("login-button"));
            waits.waitForUrlContains("inventory");

            waits.click(By.id("add-to-cart-sauce-labs-backpack"));
            waits.click(By.id("add-to-cart-sauce-labs-bike-light"));
            waits.click(By.className("shopping_cart_link"));
            waits.waitForUrlContains("cart");

            waits.click(By.id("remove-sauce-labs-backpack"));
            waits.countToBe(By.className("cart_item"), 1);
            Check.equal("T4 items left in cart", 1, driver.findElements(By.className("cart_item")).size());
            Check.equal("T4 remaining item", "Sauce Labs Bike Light", waits.textOf(By.className("inventory_item_name")));
        } finally {
            driver.quit();
        }
    }

    static void t5SortByPrice() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            DropdownUtils dropdowns = new DropdownUtils(driver);
            driver.get(URL);
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.id("password"), "secret_sauce");
            waits.click(By.id("login-button"));
            waits.waitForUrlContains("inventory");

            dropdowns.chooseByText(By.cssSelector("[data-test='product-sort-container']"), "Price (low to high)");
            List<WebElement> prices = waits.allVisible(By.className("inventory_item_price"));
            Check.equal("T5 cheapest first", "$7.99", prices.get(0).getText());
            Check.equal("T5 dearest last", "$49.99", prices.get(prices.size() - 1).getText());
        } finally {
            driver.quit();
        }
    }
}
