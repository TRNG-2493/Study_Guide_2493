package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * TODO (Task 2.2) - Page Object for https://www.saucedemo.com (login screen).
 *
 * Locators (private, final, as By fields):
 *   username  By.id("user-name")      password  By.id("password")
 *   login     By.id("login-button")   error     By.cssSelector("[data-test='error']")
 *
 * Rules: methods describe USER INTENT; navigation methods RETURN the next page object;
 * the success path returns InventoryPage, the failure path returns this page.
 */
public class LoginPage extends BasePage {

    // TODO: declare the four By locators here

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    /** Open the site and wait until the login button is visible; return this. */
    public LoginPage open() {
        throw new UnsupportedOperationException("TODO");
    }

    /** Type into the username field; return this (fluent). */
    public LoginPage enterUsername(String username) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Type into the password field; return this (fluent). */
    public LoginPage enterPassword(String password) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Success path: enter both, click Login, return the next page (InventoryPage). */
    public InventoryPage loginAs(String username, String password) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Negative path: enter both, click Login, stay on this page. */
    public LoginPage loginExpectingFailure(String username, String password) {
        throw new UnsupportedOperationException("TODO");
    }

    public String getErrorMessage() {
        throw new UnsupportedOperationException("TODO");
    }

    public boolean isErrorDisplayed() {
        throw new UnsupportedOperationException("TODO");
    }
}
