package com.revature.qea.support;

import com.revature.qea.drivers.DriverFactory;
import org.openqa.selenium.WebDriver;

import java.util.ArrayList;
import java.util.List;

/**
 * GIVEN - shared per-scenario state (step-definitions.md, section 9).
 * PicoContainer creates ONE instance per scenario and hands the SAME instance to every step class whose
 * constructor asks for it.
 *
 * BROWSER CLEANUP (temporary - Friday's @After hook replaces it)
 *   The demo closed the browser inside the last Then step. That breaks as soon as a scenario has more than one
 *   Then/And/But after it. So this class uses a simpler rule that works for any scenario shape:
 *     * when a scenario asks for its first driver, any browser left over from the PREVIOUS scenario is closed first;
 *     * the very last browser is closed when the JVM exits.
 *   Consequences: at most one browser is open at a time, a failed scenario leaves its window open for you to
 *   look at, and your step classes need no try/finally. (Scenarios run one after another, never in parallel.)
 */
public class TestContext {

    private static final List<WebDriver> OPEN_DRIVERS = new ArrayList<>();

    static {
        Runtime.getRuntime().addShutdownHook(new Thread(TestContext::closeLeftovers));
    }

    private WebDriver driver;

    /** Lazily creates the browser on first use. Reads -Dbrowser and -Dheadless (Monday). */
    public WebDriver driver() {
        if (driver == null) {
            closeLeftovers();                                   // previous scenario's window, if any
            driver = DriverFactory.createDriver(
                    System.getProperty("browser", "chrome"),
                    Boolean.parseBoolean(System.getProperty("headless", "false")));
            synchronized (OPEN_DRIVERS) {
                OPEN_DRIVERS.add(driver);
            }
        }
        return driver;
    }

    public boolean hasDriver() {
        return driver != null;
    }

    /** Optional explicit cleanup (not required on Thursday). */
    public void quitDriver() {
        if (driver != null) {
            try {
                driver.quit();
            } finally {
                synchronized (OPEN_DRIVERS) {
                    OPEN_DRIVERS.remove(driver);
                }
                driver = null;
            }
        }
    }

    private static void closeLeftovers() {
        synchronized (OPEN_DRIVERS) {
            for (WebDriver leaked : OPEN_DRIVERS) {
                try {
                    leaked.quit();
                } catch (RuntimeException ignored) {
                    // already closed
                }
            }
            OPEN_DRIVERS.clear();
        }
    }
}
