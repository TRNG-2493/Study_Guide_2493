package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.DropdownUtils;
import com.revature.qea.utils.ScreenshotUtil;
import com.revature.qea.utils.WaitUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/** GIVEN (working code from an earlier day) - stable sort flow (WaitUtils + DropdownUtils only, no sleeps). */
public class SortFlow {

    private static final String BASE_URL = "https://www.saucedemo.com/";
    private static final By SORT = By.cssSelector("[data-test='product-sort-container']");
    private static final By PRICE = By.className("inventory_item_price");
    private static final By NAME = By.className("inventory_item_name");

    public static void main(String[] args) throws Exception {
        sortProducts();
    }

    static void sortProducts() throws Exception {
        WebDriver driver = DriverFactory.createDriver();
        try {
            WaitUtils waits = new WaitUtils(driver);
            DropdownUtils dropdowns = new DropdownUtils(driver);

            // 2.3a
            driver.get(BASE_URL);
            waits.type(By.id("user-name"), "standard_user");
            waits.type(By.id("password"), "secret_sauce");
            waits.click(By.id("login-button"));
            waits.waitForUrlContains("inventory");

            // 2.3b
            Check.equal("2.3b sort options",
                    Arrays.asList("Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"),
                    dropdowns.optionTexts(SORT));
            Check.equal("2.3b default selection", "Name (A to Z)", dropdowns.selectedText(SORT));

            // 2.3c
            dropdowns.chooseByText(SORT, "Price (low to high)");
            List<Double> asc = prices(waits.allVisible(PRICE));
            List<Double> expectedAsc = new ArrayList<>(asc);
            Collections.sort(expectedAsc);
            Check.that("2.3c prices ascending " + asc, asc.equals(expectedAsc));
            Check.equal("2.3c cheapest", "$7.99", waits.allVisible(PRICE).get(0).getText());
            List<WebElement> all = waits.allVisible(PRICE);
            Check.equal("2.3c most expensive", "$49.99", all.get(all.size() - 1).getText());

            // 2.3d
            dropdowns.chooseByText(SORT, "Price (high to low)");
            List<Double> desc = prices(waits.allVisible(PRICE));
            List<Double> expectedDesc = new ArrayList<>(desc);
            expectedDesc.sort(Collections.reverseOrder());
            Check.that("2.3d prices descending " + desc, desc.equals(expectedDesc));

            // 2.3e
            dropdowns.chooseByText(SORT, "Name (Z to A)");
            List<String> names = waits.allVisible(NAME).stream().map(WebElement::getText).collect(Collectors.toList());
            List<String> expectedNames = new ArrayList<>(names);
            expectedNames.sort(Collections.reverseOrder());
            Check.that("2.3e names Z to A " + names, names.equals(expectedNames));

            // 2.3f
            ScreenshotUtil.capture(driver, "tuesday-sorted");
        } finally {
            driver.quit();
        }
    }

    static double toPrice(String text) {
        return Double.parseDouble(text.replace("$", "").trim());
    }

    private static List<Double> prices(List<WebElement> elements) {
        return elements.stream().map(e -> toPrice(e.getText())).collect(Collectors.toList());
    }
}
