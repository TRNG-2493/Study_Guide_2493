package com.revature.qea.utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * TODO (Task 1.2) - helper for new windows/tabs and frames.
 *
 * Reference: written/3-wednesday/window-handling.md (section 10) and demos/3-wednesday Stage 3.
 *
 * Rules
 *   * Window handles are NOT ordered: never guess "the second one". Use the snapshot pattern:
 *       1. remember getWindowHandles() BEFORE the action
 *       2. run the action that opens the window
 *       3. wait until the handle count grows
 *       4. switch to the handle that was not in the snapshot
 *   * After closing a window you MUST switch back explicitly - the driver does not do it for you.
 *   * Frames: use frameToBeAvailableAndSwitchToIt so the switch waits for the frame.
 */
public class WindowUtils {

    public WindowUtils(WebDriver driver) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Run the action, switch to the NEW window, return the ORIGINAL window's handle. */
    public String switchToNewWindowAfter(Runnable actionThatOpensWindow) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Close the current window, then switch to the given handle. */
    public void closeCurrentAndSwitchTo(String handle) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Switch to the first window whose title contains the text; throw NoSuchWindowException if none. */
    public void switchToWindowByTitleContains(String partialTitle) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Wait for the frame and switch into it. */
    public void switchToFrame(By frameLocator) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Switch back to the top-level page (defaultContent). */
    public void backToMainPage() {
        throw new UnsupportedOperationException("TODO");
    }
}
