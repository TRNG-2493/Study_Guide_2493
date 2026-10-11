package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.ScreenshotUtil;
import org.openqa.selenium.WebDriver;

import java.nio.file.Path;

/** GIVEN (working code from an earlier day) - Project 2 skeleton smoke check. */
public class SkeletonSmokeCheck {

    public static void main(String[] args) throws Exception {
        WebDriver driver = DriverFactory.createDriver();      // honours -Dbrowser and -Dheadless
        try {
            driver.get("https://www.saucedemo.com/");
            Check.equal("title", "Swag Labs", driver.getTitle());
            Path shot = ScreenshotUtil.capture(driver, "skeleton-smoke");
            Check.that("screenshot saved", shot.toFile().exists());
            System.out.println("Screenshot: " + shot.toAbsolutePath());
        } finally {
            driver.quit();
        }
    }
}
