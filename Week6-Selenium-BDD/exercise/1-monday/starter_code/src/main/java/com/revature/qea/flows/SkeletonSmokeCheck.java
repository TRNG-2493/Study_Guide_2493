package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.ScreenshotUtil;
import org.openqa.selenium.WebDriver;

/**
 * TODO (Project 2 milestone, Part 2, Task 2.4) - the "does my skeleton work?" check.
 *
 * Run:  mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.SkeletonSmokeCheck -Dbrowser=chrome -Dheadless=true
 *
 * Requirements: use DriverFactory.createDriver() (so -Dbrowser / -Dheadless work), open
 * https://www.saucedemo.com/, Check.equal the title, save a screenshot with ScreenshotUtil, and ALWAYS quit().
 * Then run it three ways (default, -Dheadless=true, -Dbrowser=firefox if installed) and record the results in
 * your Project 2 README ("How to run").
 */
public class SkeletonSmokeCheck {

    public static void main(String[] args) throws Exception {
        // TODO implement
    }
}
