package com.revature.qea.steps;

import com.revature.qea.pages.LoginPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Given;

/** GIVEN (working code from an earlier day) - steps shared by more than one feature (one step text = one definition, in one class). */
public class CommonSteps {

    private final TestContext context;

    public CommonSteps(TestContext context) {
        this.context = context;
    }

    @Given("the shopper is logged in")
    public void theShopperIsLoggedIn() {
        new LoginPage(context.driver()).open().loginAs("standard_user", "secret_sauce");
    }

    // TODO (Part 1, step 5): add the second shared step here, in business language:
    //   @Given("the shopper has {string} in the cart")
    // It must add the product through InventoryPage (no By / findElement in a step class).
    // Both cart.feature (Rule Background) and sort.feature will use it.
}
