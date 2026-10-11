package com.revature.qea.steps;

import com.revature.qea.pages.InventoryPage;
import com.revature.qea.support.TestContext;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** GIVEN (working code from an earlier day) - steps for sort.feature (page objects only; assertions only in @Then). */
public class SortSteps {

    private final TestContext context;

    public SortSteps(TestContext context) {
        this.context = context;
    }

    @When("the shopper sorts the products by {string}")
    public void theShopperSortsTheProductsBy(String option) {
        new InventoryPage(context.driver()).sortBy(option);
    }

    @Then("the products are listed from cheapest to most expensive")
    public void thePricesAscend() {
        List<Double> actual = new InventoryPage(context.driver()).getProductPrices();
        List<Double> expected = new ArrayList<>(actual);
        Collections.sort(expected);
        assertEquals(expected, actual, "Prices are not in ascending order");
    }

    @Then("the products are listed from most expensive to cheapest")
    public void thePricesDescend() {
        List<Double> actual = new InventoryPage(context.driver()).getProductPrices();
        List<Double> expected = new ArrayList<>(actual);
        expected.sort(Collections.reverseOrder());
        assertEquals(expected, actual, "Prices are not in descending order");
    }

    @Then("the products are listed in reverse alphabetical order")
    public void theNamesDescend() {
        List<String> actual = new InventoryPage(context.driver()).getProductNames();
        List<String> expected = new ArrayList<>(actual);
        expected.sort(Collections.reverseOrder());
        assertEquals(expected, actual, "Names are not in reverse alphabetical order");
    }
}
