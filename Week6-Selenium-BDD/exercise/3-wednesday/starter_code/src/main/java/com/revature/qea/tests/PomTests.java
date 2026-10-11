package com.revature.qea.tests;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.pages.CartPage;
import com.revature.qea.pages.InventoryPage;
import com.revature.qea.pages.LoginPage;
import com.revature.qea.pages.PfLoginPage;
import com.revature.qea.utils.Check;
import org.openqa.selenium.WebDriver;

/**
 * TODO (Task 4.1) - rewrite ScriptStyleTests with your Page Objects.
 *
 * Run:  mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.tests.PomTests -Dheadless=true
 *
 * STRICT RULES for this file
 *   * No "By" and no "driver.findElement(s)" anywhere (the only use of driver is creating, passing and quitting it).
 *   * No waits and no sleeps - the pages own all waiting.
 *   * Same Check labels and expectations as ScriptStyleTests, so the two outputs can be compared line by line.
 *   * A test creates its page objects, calls intent-named methods, and ends with Check.* - nothing else.
 *   * Always quit() the driver in a finally block.
 *
 * Tests T3 and T4 expectations:  cart badge is 2 after adding Backpack and Bike Light;
 * cart lists exactly [Sauce Labs Backpack, Sauce Labs Bike Light]; after removing the Backpack one row remains
 * (Sauce Labs Bike Light). T5: low-to-high gives first price 7.99 and last 49.99 (as doubles).
 * T6 (new): Page Factory login with standard_user / wrong_password shows
 * "Epic sadface: Username and password do not match any user in this service".
 */
public class PomTests {

    public static void main(String[] args) {
        t1LoginSucceeds();
        t2LockedOutUser();
        t3AddTwoProducts();
        t4RemoveFromCart();
        t5SortByPrice();
        t6PageFactoryLoginError();
    }

    static void t1LoginSucceeds() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  new LoginPage(driver).open().loginAs("standard_user", "secret_sauce"); Check.equal heading "Products"
        } finally {
            driver.quit();
        }
    }

    static void t2LockedOutUser() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  locked_out_user via loginExpectingFailure; Check.equal the error message
        } finally {
            driver.quit();
        }
    }

    static void t3AddTwoProducts() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  login, add two products (fluent chain), Check.equal badge 2, openCart, Check.equal names
        } finally {
            driver.quit();
        }
    }

    static void t4RemoveFromCart() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  login, add two, open cart, remove the Backpack; Check.equal item count 1 and remaining name
        } finally {
            driver.quit();
        }
    }

    static void t5SortByPrice() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  login, sortBy("Price (low to high)"), Check.equal first/last price (doubles)
        } finally {
            driver.quit();
        }
    }

    static void t6PageFactoryLoginError() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  Page Factory version: new PfLoginPage(driver).open().loginExpectingFailure(...); Check.equal the error text
        } finally {
            driver.quit();
        }
    }
}
