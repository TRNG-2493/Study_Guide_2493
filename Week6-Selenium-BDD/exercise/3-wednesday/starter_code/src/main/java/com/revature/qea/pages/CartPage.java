package com.revature.qea.pages;

import org.openqa.selenium.WebDriver;

import java.util.List;

/**
 * TODO (Task 2.4) - Page Object for the SauceDemo cart.
 *
 * Locators:  item rows By.className("cart_item")   names By.className("inventory_item_name")
 *            remove By.id("remove-" + slug)         continue By.id("continue-shopping")
 *
 * The constructor must wait for the URL to contain "cart".
 * removeItem must WAIT until the row count has dropped (do not read the count immediately).
 */
public class CartPage extends BasePage {

    public CartPage(WebDriver driver) {
        super(driver);
        // TODO: waitForUrlContaining("cart")
    }

    public List<String> getItemNames() {
        throw new UnsupportedOperationException("TODO");
    }

    public int getItemCount() {
        throw new UnsupportedOperationException("TODO");
    }

    public CartPage removeItem(String productName) {
        throw new UnsupportedOperationException("TODO");
    }

    public InventoryPage continueShopping() {
        throw new UnsupportedOperationException("TODO");
    }
}
