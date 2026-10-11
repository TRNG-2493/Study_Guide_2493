package com.revature.qea.utils;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.io.IOException;
import java.nio.file.Path;

/**
 * TODO (Project 2 milestone, Part 2, Task 2.3)
 *
 * Written lesson: written/1-monday/screenshots.md      Demo reference: demos/1-monday (Stage 7)
 *
 * Requirements
 *   1. capture(WebDriver, String name): save a viewport PNG to  target/screenshots/<safeName>-<timestamp>.png
 *      and return its Path. The file name must be safe (replace characters other than letters, digits,
 *      '-' and '_' with '_') and unique (timestamp).
 *   2. capture(WebElement, String name): the same, but for a single element.
 *   3. captureBytes(WebDriver): return the PNG as byte[] (you will attach it to reports on Friday).
 *   Hint: ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE / BYTES). COPY the temp file - do not rely on it.
 */
public final class ScreenshotUtil {

    private ScreenshotUtil() { }

    public static Path capture(WebDriver driver, String name) throws IOException {
        throw new UnsupportedOperationException("TODO: implement capture(driver, name)");
    }

    public static Path capture(WebElement element, String name) throws IOException {
        throw new UnsupportedOperationException("TODO: implement capture(element, name)");
    }

    public static byte[] captureBytes(WebDriver driver) {
        throw new UnsupportedOperationException("TODO: implement captureBytes(driver)");
    }
}
