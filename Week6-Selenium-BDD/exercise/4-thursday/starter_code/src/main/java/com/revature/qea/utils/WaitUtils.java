package com.revature.qea.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.List;

/** GIVEN (working code from an earlier day) - reusable explicit-wait helper (waiting-strategies.md section 9). */
public class WaitUtils {

    private static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(10);

    private final WebDriverWait wait;

    public WaitUtils(WebDriver driver) {
        this(driver, DEFAULT_TIMEOUT);
    }

    public WaitUtils(WebDriver driver, Duration timeout) {
        this.wait = new WebDriverWait(driver, timeout);
    }

    public WebElement visible(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    public WebElement clickable(By locator) {
        return wait.until(ExpectedConditions.elementToBeClickable(locator));
    }

    public void click(By locator) {
        clickable(locator).click();
    }

    public void type(By locator, String text) {
        WebElement element = visible(locator);
        element.clear();
        element.sendKeys(text);
    }

    public String textOf(By locator) {
        return visible(locator).getText();
    }

    public boolean disappears(By locator) {
        return wait.until(ExpectedConditions.invisibilityOfElementLocated(locator));
    }

    public List<WebElement> allVisible(By locator) {
        return wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(locator));
    }

    public void countToBe(By locator, int expected) {
        wait.until(ExpectedConditions.numberOfElementsToBe(locator, expected));
    }

    public void waitForUrlContains(String fragment) {
        wait.until(ExpectedConditions.urlContains(fragment));
    }

    public void setCheckbox(By locator, boolean shouldBeChecked) {
        WebElement box = wait.until(ExpectedConditions.presenceOfElementLocated(locator));
        if (box.isSelected() != shouldBeChecked) {
            box.click();
        }
    }
}
