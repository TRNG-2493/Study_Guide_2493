package com.revature.qea.steps;

import com.revature.qea.pages.CartPage;
import com.revature.qea.pages.InventoryPage;
import com.revature.qea.support.TestContext;
import io.cucumber.datatable.DataTable;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** GIVEN (working code from an earlier day) - steps for cart.feature. */
public class CartSteps {

    private final TestContext context;

    public CartSteps(TestContext context) {
        this.context = context;
    }

    @When("the shopper adds {string} to the cart")
    public void theShopperAddsToTheCart(String product) {
        new InventoryPage(context.driver()).addToCart(product);
    }

    /** One product per row; the step text has no trailing colon. */
    @When("the shopper adds the following products to the cart")
    public void theShopperAddsTheFollowingProducts(DataTable table) {
        InventoryPage inventory = new InventoryPage(context.driver());
        for (String product : table.asList()) {
            inventory.addToCart(product);
        }
    }

    @When("the shopper opens the cart")
    public void theShopperOpensTheCart() {
        new InventoryPage(context.driver()).openCart();
    }

    @When("the shopper removes {string} from the cart")
    public void theShopperRemovesFromTheCart(String product) {
        new CartPage(context.driver()).removeItem(product);
    }

    @Then("the cart count shows {int}")
    public void theCartCountShows(int expected) {
        assertEquals(expected, new InventoryPage(context.driver()).getCartCount(),
                "Unexpected number in the cart badge");
    }

    @Then("the cart lists {string}")
    public void theCartLists(String product) {
        List<String> names = new CartPage(context.driver()).getItemNames();
        assertTrue(names.contains(product), "Expected " + product + " in the cart but found " + names);
    }

    @Then("the cart does not list {string}")
    public void theCartDoesNotList(String product) {
        List<String> names = new CartPage(context.driver()).getItemNames();
        assertFalse(names.contains(product), "Did not expect " + product + " in the cart but found " + names);
    }

    @Then("the cart is empty")
    public void theCartIsEmpty() {
        assertEquals(0, new CartPage(context.driver()).getItemCount(), "Cart should be empty");
    }
}
