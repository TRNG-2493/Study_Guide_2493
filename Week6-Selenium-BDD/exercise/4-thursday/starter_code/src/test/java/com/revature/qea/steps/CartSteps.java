package com.revature.qea.steps;

import com.revature.qea.support.TestContext;

/**
 * TODO (slot 5) - step definitions for cart.feature.
 *
 * Same rules as SortSteps. For a data table step use io.cucumber.datatable.DataTable
 * (a single-column table becomes a List<String> with table.asList()).
 *
 * Page object methods you will need: InventoryPage.addToCart(String), getCartCount(), openCart();
 * CartPage.getItemNames(), getItemCount(), removeItem(String).
 *
 * Remember: InventoryPage's constructor waits for the inventory URL, CartPage's for the cart URL. Create the page
 * object that matches the page the shopper is ON when the step runs.
 */
public class CartSteps {

    private final TestContext context;

    public CartSteps(TestContext context) {
        this.context = context;
    }

    // TODO @When / @Then steps for your cart scenarios
}
