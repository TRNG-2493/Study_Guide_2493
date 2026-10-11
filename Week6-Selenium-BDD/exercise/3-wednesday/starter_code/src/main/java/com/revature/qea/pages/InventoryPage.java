package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

/**
 * TODO (Task 2.3) - Page Object for the SauceDemo product list.
 *
 * Locators:
 *   title    By.className("title")                 names   By.className("inventory_item_name")
 *   prices   By.className("inventory_item_price")  sort    By.cssSelector("[data-test='product-sort-container']")
 *   badge    By.className("shopping_cart_badge")   cart    By.className("shopping_cart_link")
 *   add      By.id("add-to-cart-" + slug)          remove  By.id("remove-" + slug)
 *   where slug = product name in lower case with spaces replaced by dashes ("Sauce Labs Backpack" -> "sauce-labs-backpack").
 *
 * The constructor must WAIT for the URL to contain "inventory" (fail fast if you landed on the wrong page).
 * Use DropdownUtils for sorting.
 * Stability tip (Tuesday!): addToCart must not return until the add is DONE - after clicking, wait until the
 * matching "remove-<slug>" button is visible; removeFromCart waits for "add-to-cart-<slug>" to come back.
 */
public class InventoryPage extends BasePage {

    // TODO: locators and a DropdownUtils field

    public InventoryPage(WebDriver driver) {
        super(driver);
        // TODO: initialise helpers, then waitForUrlContaining("inventory")
    }

    public boolean isLoaded() {                    // true when the title text is "Products"
        throw new UnsupportedOperationException("TODO");
    }

    public String getTitle() {
        throw new UnsupportedOperationException("TODO");
    }

    public List<String> getProductNames() {
        throw new UnsupportedOperationException("TODO");
    }

    /** "$29.99" -> 29.99 for every product, in page order. */
    public List<Double> getProductPrices() {
        throw new UnsupportedOperationException("TODO");
    }

    public InventoryPage sortBy(String visibleText) {
        throw new UnsupportedOperationException("TODO");
    }

    public InventoryPage addToCart(String productName) {
        throw new UnsupportedOperationException("TODO");
    }

    public InventoryPage removeFromCart(String productName) {
        throw new UnsupportedOperationException("TODO");
    }

    /** The badge is ABSENT (not "0") when the cart is empty - return 0 in that case. */
    public int getCartCount() {
        throw new UnsupportedOperationException("TODO");
    }

    public CartPage openCart() {
        throw new UnsupportedOperationException("TODO");
    }
}
