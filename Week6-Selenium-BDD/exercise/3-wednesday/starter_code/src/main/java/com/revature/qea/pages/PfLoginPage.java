package com.revature.qea.pages;

import org.openqa.selenium.WebDriver;

/**
 * TODO (Task 3.1) - the SAME login screen, written in Page Factory style.
 *
 * Reference: page-object-model-and-page-factory.md (Page Factory section) and demos/3-wednesday Stage 6.
 *
 * Rules
 *   * Declare the four elements as @FindBy fields (id / css) of type WebElement - NOT final.
 *   * Call PageFactory.initElements(driver, this) in the constructor.
 *   * The proxies do NOT wait: combine every use with an explicit wait (ExpectedConditions.visibilityOf(element)).
 *   * Methods: open(), loginExpectingFailure(user, password), getErrorMessage().
 *   * Keep it a stand-alone class (it does not have to extend BasePage - BasePage uses By-locators).
 */
public class PfLoginPage {

    public PfLoginPage(WebDriver driver) {
        throw new UnsupportedOperationException("TODO");
    }

    public PfLoginPage open() {
        throw new UnsupportedOperationException("TODO");
    }

    public PfLoginPage loginExpectingFailure(String username, String password) {
        throw new UnsupportedOperationException("TODO");
    }

    public String getErrorMessage() {
        throw new UnsupportedOperationException("TODO");
    }
}
