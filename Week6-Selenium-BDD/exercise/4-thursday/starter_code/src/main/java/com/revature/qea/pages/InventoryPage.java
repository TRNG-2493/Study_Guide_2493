package com.revature.qea.pages;

import com.revature.qea.utils.DropdownUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;
import java.util.stream.Collectors;

/** GIVEN (working code from an earlier day) - Page Object for the SauceDemo product list. */
public class InventoryPage extends BasePage {

    private final By pageTitle = By.className("title");
    private final By productNames = By.className("inventory_item_name");
    private final By productPrices = By.className("inventory_item_price");
    private final By sortDropdown = By.cssSelector("[data-test='product-sort-container']");
    private final By cartBadge = By.className("shopping_cart_badge");
    private final By cartLink = By.className("shopping_cart_link");

    private final DropdownUtils dropdowns;

    public InventoryPage(WebDriver driver) {
        super(driver);
        this.dropdowns = new DropdownUtils(driver);
        waitForUrlContaining("inventory");      // fail fast if we are on the wrong page
    }

    public boolean isLoaded() {
        return getTitle().equals("Products");
    }

    public String getTitle() {
        return textOf(pageTitle);
    }

    public List<String> getProductNames() {
        waits.allVisible(productNames);
        return textsOf(productNames);
    }

    public List<Double> getProductPrices() {
        waits.allVisible(productPrices);
        return textsOf(productPrices).stream()
                .map(t -> Double.parseDouble(t.replace("$", "")))
                .collect(Collectors.toList());
    }

    public InventoryPage sortBy(String visibleText) {
        dropdowns.chooseByText(sortDropdown, visibleText);
        return this;
    }

    public InventoryPage addToCart(String productName) {
        click(By.id("add-to-cart-" + slug(productName)));
        waits.visible(By.id("remove-" + slug(productName)));      // the button flips to "Remove": the add is done
        return this;
    }

    public InventoryPage removeFromCart(String productName) {
        click(By.id("remove-" + slug(productName)));
        waits.visible(By.id("add-to-cart-" + slug(productName)));  // the button flips back to "Add to cart"
        return this;
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

    private String slug(String productName) {
        return productName.toLowerCase().replace(' ', '-');
    }
}
