package com.revature.qea.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;

import java.util.List;
import java.util.stream.Collectors;

/** GIVEN (working code from an earlier day) - Select helper (select-elements.md section 9). */
public class DropdownUtils {

    private final WaitUtils waits;

    public DropdownUtils(WebDriver driver) {
        this.waits = new WaitUtils(driver);
    }

    private Select select(By locator) {
        WebElement element = waits.visible(locator);
        return new Select(element);
    }

    public void chooseByText(By locator, String text) {
        select(locator).selectByVisibleText(text);
    }

    public void chooseByValue(By locator, String value) {
        select(locator).selectByValue(value);
    }

    public String selectedText(By locator) {
        return select(locator).getFirstSelectedOption().getText();
    }

    public List<String> optionTexts(By locator) {
        return select(locator).getOptions().stream()
                .map(WebElement::getText)
                .collect(Collectors.toList());
    }
}
