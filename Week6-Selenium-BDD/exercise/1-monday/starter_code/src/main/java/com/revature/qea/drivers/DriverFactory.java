package com.revature.qea.drivers;

import org.openqa.selenium.WebDriver;

/**
 * TODO (Project 2 milestone, Part 2, Task 2.2)
 *
 * The ONLY class in the framework that knows browser names.
 * Written lesson: written/1-monday/driver-configuration.md  and  browser-options.md
 * Demo reference: demos/1-monday  (Stage 2 and Stage 3)
 *
 * Requirements
 *   1. createDriver(String browserName, boolean headless) returns the WebDriver INTERFACE.
 *   2. Support "chrome", "firefox" and "edge" (trim + lower-case the name first).
 *   3. null or unknown browser names -> throw IllegalArgumentException with a helpful message.
 *   4. Headless: Chrome/Edge  --headless=new (+ --window-size=1920,1080 for Chrome);  Firefox  -headless
 *   5. Headed (not headless): maximise the window.
 *   6. Convenience: createDriver() with no arguments reads -Dbrowser (default "chrome") and
 *      -Dheadless (default "false") and calls the two-argument method.
 */
public final class DriverFactory {

    private DriverFactory() { }

    public static WebDriver createDriver() {
        // TODO read System.getProperty("browser", "chrome") and System.getProperty("headless", "false")
        throw new UnsupportedOperationException("TODO: implement createDriver()");
    }

    public static WebDriver createDriver(String browserName, boolean headless) {
        // TODO switch on the normalised browser name and build the matching Options object
        throw new UnsupportedOperationException("TODO: implement createDriver(browserName, headless)");
    }
}
