package com.revature.qea.pages;

import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;
import java.util.stream.Collectors;

/**
 * GIVEN (working code from an earlier day) - the base of every page object. Wraps WaitUtils so pages never call Selenium waits directly.
 * Pages: locators private, methods named for user intent, NO assertions, navigation returns the next page.
 */
public abstract class BasePage {

    protected final WebDriver driver;
    protected final WaitUtils waits;

    protected BasePage(WebDriver driver) {
        this.driver = driver;
        this.waits = new WaitUtils(driver);
    }

    protected void click(By locator) {
        waits.click(locator);
    }

    protected void type(By locator, String text) {
        waits.type(locator, text);
    }

    protected String textOf(By locator) {
        return waits.textOf(locator);
    }

    /** Non-waiting: is it there AND displayed right now? */
    protected boolean isDisplayed(By locator) {
        List<WebElement> found = driver.findElements(locator);
        return !found.isEmpty() && found.get(0).isDisplayed();
    }

    /** Non-waiting list read; an empty list is a valid answer (for example an empty cart). */
    protected List<String> textsOf(By locator) {
        return driver.findElements(locator).stream().map(WebElement::getText).collect(Collectors.toList());
    }

    protected void waitForUrlContaining(String fragment) {
        waits.waitForUrlContains(fragment);
    }
}
