package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.DropdownUtils;
import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * TODO (Project 2 milestone, Task 2.3) - the stable "sort the product list" flow on SauceDemo.
 *
 * Use ONLY WaitUtils and DropdownUtils for waiting/selecting (no sleeps, no raw WebDriverWait here).
 *
 * Sort control locator:  By.cssSelector("[data-test='product-sort-container']")
 * Price locator (list):  By.className("inventory_item_price")     Name locator: By.className("inventory_item_name")
 *
 * Run:  mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SortFlow
 */
public class SortFlow {

    private static final String BASE_URL = "https://www.saucedemo.com/";
    private static final By SORT = By.cssSelector("[data-test='product-sort-container']");

    public static void main(String[] args) throws Exception {
        sortProducts();
    }

    static void sortProducts() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO 2.3a  open BASE_URL and log in as standard_user (WaitUtils type/click), wait for the inventory URL
            // TODO 2.3b  DropdownUtils.optionTexts(SORT): Check.equal the 4 options, in order:
            //            "Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"
            //            and Check.equal selectedText is "Name (A to Z)" (the default)
            // TODO 2.3c  choose "Price (low to high)"; read all prices as doubles (strip the "$");
            //            Check.that the list is sorted ascending (compare with a sorted copy),
            //            Check.equal first price "$7.99" and last price "$49.99"
            // TODO 2.3d  choose "Price (high to low)"; Check.that the list is sorted descending
            // TODO 2.3e  choose "Name (Z to A)"; read all names; Check.that they are sorted in reverse alphabetical order
            //            (careful: the lists re-render after each choice - re-read them AFTER choosing)
            // TODO 2.3f  ScreenshotUtil.capture(driver, "tuesday-sorted") at the end
        } finally {
            driver.quit();
        }
    }

    /** Helper you will probably want: turn "$29.99" into 29.99. */
    static double toPrice(String text) {
        // TODO
        throw new UnsupportedOperationException("TODO");
    }
}
