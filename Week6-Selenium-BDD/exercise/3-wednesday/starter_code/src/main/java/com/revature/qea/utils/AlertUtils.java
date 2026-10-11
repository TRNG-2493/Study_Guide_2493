package com.revature.qea.utils;

import org.openqa.selenium.WebDriver;

/**
 * TODO (Task 1.1) - helper for JavaScript alert / confirm / prompt dialogs.
 *
 * Reference: written/3-wednesday/alerts.md (section 10) and demos/3-wednesday Stage 2.
 *
 * Rules
 *   * Wait for the alert with ExpectedConditions.alertIsPresent() (5 second wait is enough).
 *   * READ the text BEFORE accept()/dismiss() - after closing, the Alert object is unusable.
 *   * isPresent() must NOT wait: it answers "is an alert open right now?" (switchTo().alert() and catch
 *     NoAlertPresentException).
 *   * Never swallow a TimeoutException in the methods that expect an alert.
 */
public class AlertUtils {

    public AlertUtils(WebDriver driver) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Non-waiting check: is an alert open RIGHT NOW? */
    public boolean isPresent() {
        throw new UnsupportedOperationException("TODO");
    }

    /** Wait for the alert, return its text, then accept (OK). */
    public String acceptAndGetText() {
        throw new UnsupportedOperationException("TODO");
    }

    /** Wait for the alert, return its text, then dismiss (Cancel). */
    public String dismissAndGetText() {
        throw new UnsupportedOperationException("TODO");
    }

    /** Wait for a prompt, type the answer, accept. */
    public void answerPrompt(String answer) {
        throw new UnsupportedOperationException("TODO");
    }

    /** True when NO alert appears within the wait (a timeout is the SUCCESS case here). */
    public boolean noAlertAppears() {
        throw new UnsupportedOperationException("TODO");
    }
}
