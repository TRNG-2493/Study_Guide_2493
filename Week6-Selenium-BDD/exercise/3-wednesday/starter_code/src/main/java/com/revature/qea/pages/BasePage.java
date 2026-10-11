package com.revature.qea.pages;

import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

/**
 * TODO (Task 2.1) - the base of every page object.
 *
 * Reference: written/3-wednesday/page-object-model-and-page-factory.md and demos/3-wednesday Stage 5.
 *
 * Design rules
 *   * Holds the WebDriver and a WaitUtils (reuse Tuesday's helper - do NOT create new WebDriverWait here).
 *   * Wraps the common actions so pages and tests never repeat wait logic.
 *   * Pages never contain assertions (no Check, no JUnit) - they expose state; tests judge it.
 */
public abstract class BasePage {

    protected final WebDriver driver;
    protected final WaitUtils waits;

    /** TODO: assign both fields. */
    protected BasePage(WebDriver driver) {
        throw new UnsupportedOperationException("TODO");
    }

    /** TODO: wait for clickable, then click. */
    protected void click(By locator) {
        throw new UnsupportedOperationException("TODO");
    }

    /** TODO: wait for visible, clear, type. */
    protected void type(By locator, String text) {
        throw new UnsupportedOperationException("TODO");
    }

    /** TODO: wait for visible, return text. */
    protected String textOf(By locator) {
        throw new UnsupportedOperationException("TODO");
    }

    /** TODO (non-waiting): true when the element exists AND is displayed right now. Use findElements, not findElement. */
    protected boolean isDisplayed(By locator) {
        throw new UnsupportedOperationException("TODO");
    }

    /** TODO (non-waiting): texts of all matches; an empty list is a valid answer (for example an empty cart). */
    protected List<String> textsOf(By locator) {
        throw new UnsupportedOperationException("TODO");
    }

    /** TODO: delegate to WaitUtils. */
    protected void waitForUrlContaining(String fragment) {
        throw new UnsupportedOperationException("TODO");
    }
}
