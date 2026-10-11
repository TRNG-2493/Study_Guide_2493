package com.revature.qea.steps;

import com.revature.qea.support.TestContext;

/**
 * TODO (slot 4) - step definitions for sort.feature.
 *
 * Rules (checked by FeatureStyleTest and by your navigator):
 *   * constructor takes the shared TestContext;
 *   * page objects only - no By, no findElement, no waits in this class;
 *   * assertions only in @Then steps (use org.junit.jupiter.api.Assertions);
 *   * parameters in the step text ({string}, {int}) instead of one method per product/option.
 *
 * Page object methods you will need: InventoryPage.sortBy(String), getProductPrices(), getProductNames().
 * Hint for ordering checks: copy the list, sort the copy, assertEquals(sortedCopy, original).
 */
public class SortSteps {

    private final TestContext context;

    public SortSteps(TestContext context) {
        this.context = context;
    }

    // TODO @When  the shopper sorts the products by {string}
    // TODO @Then  ... one step per ordering your feature file expresses
}
