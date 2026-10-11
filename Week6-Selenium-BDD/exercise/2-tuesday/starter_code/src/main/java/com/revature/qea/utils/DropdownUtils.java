package com.revature.qea.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

/**
 * TODO (Task 2.2) - helper around Selenium's Select class.
 *
 * Reference: written/2-tuesday/select-elements.md (section 9) and demos/2-tuesday (Stage 8).
 *
 * Rules
 *   * Wait for the <select> to be visible, THEN wrap it in new Select(element).
 *     (You may create your own WaitUtils inside, or a WebDriverWait - but only here, not in flows.)
 *   * Methods take a By so the element is always freshly located.
 *   * Select only works on real <select> tags (SauceDemo's sort control is one).
 */
public class DropdownUtils {

    // TODO: keep whatever you need (e.g. a WaitUtils) in a field
    public DropdownUtils(WebDriver driver) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Select the option whose visible text matches exactly. */
    public void chooseByText(By locator, String text) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Select the option whose value attribute matches. */
    public void chooseByValue(By locator, String value) {
        throw new UnsupportedOperationException("TODO");
    }

    /** @return the visible text of the currently selected option */
    public String selectedText(By locator) {
        throw new UnsupportedOperationException("TODO");
    }

    /** @return the visible text of every option, in page order */
    public List<String> optionTexts(By locator) {
        throw new UnsupportedOperationException("TODO");
    }
}
