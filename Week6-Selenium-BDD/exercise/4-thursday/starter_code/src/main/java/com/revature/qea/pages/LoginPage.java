package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/** GIVEN (working code from an earlier day) - Page Object for https://www.saucedemo.com (login screen). */
public class LoginPage extends BasePage {

    private static final String URL = "https://www.saucedemo.com";

    private final By usernameField = By.id("user-name");
    private final By passwordField = By.id("password");
    private final By loginButton = By.id("login-button");
    private final By errorMessage = By.cssSelector("[data-test='error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    public LoginPage open() {
        driver.get(URL);
        waits.visible(loginButton);
        return this;
    }

    public LoginPage enterUsername(String username) {
        type(usernameField, username);
        return this;
    }

    public LoginPage enterPassword(String password) {
        type(passwordField, password);
        return this;
    }

    /** Success path: the user lands on the inventory page. */
    public InventoryPage loginAs(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        click(loginButton);
        return new InventoryPage(driver);
    }

    /** Negative path: we expect to STAY on the login page. */
    public LoginPage loginExpectingFailure(String username, String password) {
        enterUsername(username);
        enterPassword(password);
        click(loginButton);
        return this;
    }

    public String getErrorMessage() {
        return textOf(errorMessage);
    }

    public boolean isErrorDisplayed() {
        return isDisplayed(errorMessage);
    }
}
