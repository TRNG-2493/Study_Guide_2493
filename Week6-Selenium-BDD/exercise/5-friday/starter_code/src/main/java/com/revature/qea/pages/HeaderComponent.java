package com.revature.qea.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

/**
 * GIVEN - the page header (cart link + badge) exists on the inventory page AND the cart page, so it is a reusable
 * COMPONENT (page-object-model-and-page-factory.md, "Components"; Wednesday's stretch goal 1).
 * Steps can now read the cart count from whichever page the browser is on.
 */
public class HeaderComponent extends BasePage {

    private final By cartBadge = By.className("shopping_cart_badge");
    private final By cartLink = By.className("shopping_cart_link");

    public HeaderComponent(WebDriver driver) {
        super(driver);
    }

    /** The badge is ABSENT (not "0") when the cart is empty. */
    public int getCartCount() {
        List<WebElement> badge = driver.findElements(cartBadge);
        return badge.isEmpty() ? 0 : Integer.parseInt(badge.get(0).getText());
    }

    public CartPage openCart() {
        click(cartLink);
        return new CartPage(driver);
    }
}
