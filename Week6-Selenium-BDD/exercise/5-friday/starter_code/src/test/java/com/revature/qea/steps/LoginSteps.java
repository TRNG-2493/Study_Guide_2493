package com.revature.qea.steps;

import com.revature.qea.pages.InventoryPage;
import com.revature.qea.pages.LoginPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * GIVEN (working code from an earlier day) - the login steps. The three new login scenarios REUSE these steps unchanged. Notice how it:
 *   * gets the shared TestContext through the constructor (PicoContainer),
 *   * calls ONLY page objects (no By, no findElement),
 *   * keeps assertions in the Then steps (no browser cleanup needed - TestContext handles it).
 */
public class LoginSteps {

    private final TestContext context;     // injected by PicoContainer
    private LoginPage loginPage;

    public LoginSteps(TestContext context) {
        this.context = context;
    }

    @Given("the customer is on the login page")
    public void theCustomerIsOnTheLoginPage() {
        loginPage = new LoginPage(context.driver()).open();
    }

    @When("the customer logs in with username {string} and password {string}")
    public void theCustomerLogsInWith(String username, String password) {
        loginPage.loginExpectingFailure(username, password);   // clicks Login and stays on the page object
    }

    @Then("the customer sees the products page")
    public void theCustomerSeesTheProductsPage() {
        assertTrue(new InventoryPage(context.driver()).isLoaded(), "Products page was not displayed");
    }

    @Then("the error message {string} is displayed")
    public void theErrorMessageIsDisplayed(String expectedMessage) {
        assertEquals(expectedMessage, loginPage.getErrorMessage());
    }
}
