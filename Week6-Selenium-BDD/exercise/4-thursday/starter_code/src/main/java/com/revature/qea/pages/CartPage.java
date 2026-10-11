package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

import java.util.List;

/** GIVEN (working code from an earlier day) - Page Object for the SauceDemo cart. */
public class CartPage extends BasePage {

    private final By cartItemNames = By.className("inventory_item_name");
    private final By cartItems = By.className("cart_item");
    private final By continueShopping = By.id("continue-shopping");

    public CartPage(WebDriver driver) {
        super(driver);
        waitForUrlContaining("cart");
    }

    public List<String> getItemNames() {
        return textsOf(cartItemNames);
    }

    public int getItemCount() {
        return driver.findElements(cartItems).size();
    }

    public CartPage removeItem(String productName) {
        int before = getItemCount();
        click(By.id("remove-" + productName.toLowerCase().replace(' ', '-')));
        waits.countToBe(cartItems, before - 1);        // wait for the DOM to catch up
        return this;
    }

    public InventoryPage continueShopping() {
        click(continueShopping);
        return new InventoryPage(driver);
    }
}
