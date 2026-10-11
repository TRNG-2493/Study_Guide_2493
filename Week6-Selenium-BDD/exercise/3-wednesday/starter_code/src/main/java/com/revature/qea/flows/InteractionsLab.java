package com.revature.qea.flows;

import com.revature.qea.drivers.DriverFactory;
import com.revature.qea.utils.AlertUtils;
import com.revature.qea.utils.Check;
import com.revature.qea.utils.WaitUtils;
import com.revature.qea.utils.WindowUtils;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;

/**
 * TODO (Part 1) - Actions API, alerts, windows and frames on https://the-internet.herokuapp.com
 *
 * Run:  mvn -q compile exec:java -Dexec.mainClass=com.revature.qea.flows.InteractionsLab -Dheadless=true
 *
 * Rules: use WaitUtils / AlertUtils / WindowUtils for every wait (no sleeps, no implicit wait). Every
 * Actions chain must end with perform(). Each task is its own method with its own driver so one failure
 * cannot hide the others.
 */
public class InteractionsLab {

    private static final String INTERNET = "https://the-internet.herokuapp.com/";
    private static final String SAUCE = "https://www.saucedemo.com/";

    public static void main(String[] args) {
        t1Hover();
        t2Alerts();
        t3NewWindow();
        t4KeyboardChord();
        t5NestedFrames();
    }

    /** Task 1.3  /hovers - the caption is hidden until the mouse hovers the figure. */
    static void t1Hover() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  open INTERNET + "hovers"
            // TODO  wait for the ".figure" elements (allVisible) and take the first one
            // TODO  scoped lookup: firstFigure.findElement(By.className("figcaption")); Check.that it is NOT displayed yet
            //       (a "should be hidden" check - isDisplayed() is right here, not a wait)
            // TODO  hover with new Actions(driver).moveToElement(firstFigure).perform()
            // TODO  wait until a caption is visible (".figure .figcaption"); Check.that the caption text contains "user1"
        } finally {
            driver.quit();
        }
    }

    /** Task 1.4  /javascript_alerts - one of each dialog type. */
    static void t2Alerts() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // Buttons:  button[onclick='jsAlert()']   button[onclick='jsConfirm()']   button[onclick='jsPrompt()']
            // Result text element:  By.id("result")
            // TODO  open INTERNET + "javascript_alerts"
            // TODO  ALERT:   click, acceptAndGetText -> Check.that text contains "I am a JS Alert";
            //                Check.equal result is "You successfully clicked an alert"
            // TODO  CONFIRM: click, dismissAndGetText -> Check.that text contains "I am a JS Confirm";
            //                Check.equal result is "You clicked: Cancel"
            // TODO  PROMPT:  click, answerPrompt("Revature QEA") -> Check.equal result is "You entered: Revature QEA"
            // TODO  Check.that alerts.isPresent() is false afterwards
        } finally {
            driver.quit();
        }
    }

    /** Task 1.5  /windows - a link that opens a new window. */
    static void t3NewWindow() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  open INTERNET + "windows"; remember the heading text of the original page (By.tagName("h3"))
            // TODO  WindowUtils.switchToNewWindowAfter(() -> click the link with By.linkText("Click Here"))
            // TODO  Check.equal the new window's title is "New Window" and its h3 text is "New Window"
            // TODO  close it with closeCurrentAndSwitchTo(original) and Check.equal the h3 text is the original heading again
            // TODO  Check.equal(1, driver.getWindowHandles().size())
        } finally {
            driver.quit();
        }
    }

    /** Task 1.6  Actions keyboard chord on SauceDemo's username field. */
    static void t4KeyboardChord() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  open SAUCE, wait for the field By.id("user-name")
            // TODO  one Actions chain: click(field).keyDown(Keys.SHIFT).sendKeys("standard").keyUp(Keys.SHIFT).perform()
            // TODO  Check.equal the field's "value" attribute is "STANDARD"
        } finally {
            driver.quit();
        }
    }

    /** Task 1.7  /nested_frames - text inside a frame inside a frame. */
    static void t5NestedFrames() {
        WebDriver driver = DriverFactory.createDriver();
        try {
            // TODO  open INTERNET + "nested_frames"
            // TODO  switchToFrame(By.name("frame-top")), then switchToFrame(By.name("frame-middle"))
            // TODO  Check.equal By.id("content") text is "MIDDLE"
            // TODO  backToMainPage(); Check.that driver.findElements(By.tagName("frameset")) is NOT empty
            //       (you are back on the top-level document that owns the frames)
        } finally {
            driver.quit();
        }
    }
}
