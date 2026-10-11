package com.revature.qea.drivers;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;

/** GIVEN (working code from an earlier day) - the only class that knows browser names (written lesson: driver-configuration.md). */
public final class DriverFactory {

    private DriverFactory() { }

    /** Reads -Dbrowser (default chrome) and -Dheadless (default false). */
    public static WebDriver createDriver() {
        return createDriver(
                System.getProperty("browser", "chrome"),
                Boolean.parseBoolean(System.getProperty("headless", "false")));
    }

    public static WebDriver createDriver(String browserName, boolean headless) {
        if (browserName == null) {
            throw new IllegalArgumentException("Browser name must not be null");
        }
        WebDriver driver;
        switch (browserName.trim().toLowerCase()) {
            case "chrome": {
                ChromeOptions options = new ChromeOptions();
                if (headless) {
                    options.addArguments("--headless=new", "--window-size=1920,1080");
                }
                driver = new ChromeDriver(options);
                break;
            }
            case "firefox": {
                FirefoxOptions options = new FirefoxOptions();
                if (headless) {
                    options.addArguments("-headless");
                }
                driver = new FirefoxDriver(options);
                break;
            }
            case "edge": {
                EdgeOptions options = new EdgeOptions();
                if (headless) {
                    options.addArguments("--headless=new");
                }
                driver = new EdgeDriver(options);
                break;
            }
            default:
                throw new IllegalArgumentException(
                        "Unsupported browser: '" + browserName + "'. Use chrome, firefox or edge.");
        }
        if (!headless) {
            driver.manage().window().maximize();
        }
        return driver;
    }
}
