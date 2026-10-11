package com.revature.qea.utils;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/** GIVEN (working code from an earlier day) (written lesson: screenshots.md). */
public final class ScreenshotUtil {

    private static final Path OUTPUT_DIR = Paths.get("target", "screenshots");
    private static final DateTimeFormatter STAMP = DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss-SSS");

    private ScreenshotUtil() { }

    public static Path capture(WebDriver driver, String name) throws IOException {
        Path source = ((TakesScreenshot) driver).getScreenshotAs(OutputType.FILE).toPath();
        return save(source, name);
    }

    public static Path capture(WebElement element, String name) throws IOException {
        Path source = element.getScreenshotAs(OutputType.FILE).toPath();
        return save(source, name);
    }

    public static byte[] captureBytes(WebDriver driver) {
        return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
    }

    private static Path save(Path source, String name) throws IOException {
        Files.createDirectories(OUTPUT_DIR);
        String safe = name.replaceAll("[^a-zA-Z0-9_-]", "_");
        Path target = OUTPUT_DIR.resolve(safe + "-" + LocalDateTime.now().format(STAMP) + ".png");
        return Files.copy(source, target, StandardCopyOption.REPLACE_EXISTING);
    }
}
