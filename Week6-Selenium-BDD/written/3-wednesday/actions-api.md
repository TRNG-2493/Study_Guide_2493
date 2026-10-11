# Actions API

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what the **Actions API** is, and why `click()` and `sendKeys()` alone are not enough for some user gestures.
- Create an `Actions` object, build a chain of actions, and run it with `perform()`.
- Explain why `build()` and `perform()` exist, and when `build()` can be omitted.
- Simulate **mouse hover** (`moveToElement`), **right-click** (`contextClick`), **double-click** (`doubleClick`), and **click-and-hold** (`clickAndHold` / `release`).
- Perform **drag and drop** with `dragAndDrop`, `dragAndDropBy`, and the manual `clickAndHold` + `moveToElement` + `release` sequence, and know when each is appropriate.
- Send **keyboard actions** such as `keyDown`, `keyUp`, and key chords for capital letters, shortcuts, and multi-select.
- Use the **scrolling** actions introduced in Selenium 4 (`scrollToElement`, `scrollByAmount`, `scrollFromOrigin`).
- Combine Actions with explicit waits correctly, and diagnose the most common failures from their exception text.
- Decide when Actions is the right tool and when a plain `click()` is better.
- Place Actions-based steps inside page-object methods (preview of the lesson that follows later today).

---

## Why This Matters

A real user does far more than click and type. They **hover** over a menu to open a submenu, **right-click** to see a context menu, **double-click** to edit a spreadsheet cell, **drag** a card from "To Do" to "Done" on a task board, or hold **Shift** while clicking to select a range of rows. Modern web applications are full of these gestures.

On Tuesday you learned the basic interactions (`click`, `sendKeys`, `clear`), plus waits and the `Select` class. Those methods cover straightforward forms, but they cannot hover and they cannot drag. Without the Actions API, a large share of any realistic application would be impossible to test automatically.

Here are three real-world scenarios where a test engineer needs this lesson:

1. **E-commerce navigation.** A shop's top menu shows "Laptops", "Phones", and "Accessories" only when you hover over "Products". A `click()` on "Laptops" fails with `ElementNotInteractableException` because the item is hidden until the hover happens.
2. **Project board.** A tool like Trello lets users drag a card between columns. The business-critical feature "move a task to Done" can only be tested by dragging.
3. **Data tables.** An admin screen reveals a "Delete" icon only when the mouse is over a row. A tester must hover first, then click.

In **Project 2**, any realistic site (a dashboard, a drag-and-drop board, a hover menu) needs these skills. Later today you will wrap Actions-based steps inside **Page Object** methods such as `header.openProductsMenu()`, so the test reads like plain English and the low-level gesture lives in one place.

---

## The Concept

### 1. What Is the Actions API?

**Definition.** The **Actions API** is a part of Selenium that lets you describe low-level input devices and their movements, then execute that description as one continuous gesture. The devices are:

- a **pointer** (the mouse): move, press, release, click
- a **keyboard**: key down, key up
- a **wheel**: scroll (new in Selenium 4)

**Why does it exist?** `element.click()` does exactly one thing: it clicks the middle of an element. Real gestures are made of *sequences*: "move here, press the button, move there, release the button." A single method call cannot express that, so Selenium provides a way to describe the sequence.

**Standards background.** Selenium 4 implements the W3C WebDriver "Actions" specification. In Java the entry point is the `Actions` class. The import and the creation line are:

```java
import org.openqa.selenium.interactions.Actions;

Actions actions = new Actions(driver);
```

**Line-by-line.**

- `import org.openqa.selenium.interactions.Actions;` brings the class into scope. Without it the compiler reports `cannot find symbol: class Actions`.
- `new Actions(driver)` creates a builder tied to one browser session. The `driver` variable is the `WebDriver` you created in Monday's lessons (or got from your `DriverFactory`).

**Analogy.** Think of `Actions` as a **recipe card**. You write the steps on the card ("move to the menu, wait half a second, click the submenu item") and nothing is cooked until you say "go". The word "go" is `perform()`.

**When to use it.** Use Actions when the user gesture is not a simple click or typing: hover, right-click, double-click, drag, key combinations, or wheel scrolling. If `element.click()` or `element.sendKeys()` does the job, use those; they are simpler and more reliable.

### 2. `build()` and `perform()`

```java
actions.moveToElement(menu)     // step 1: hover over the menu
       .click(submenuItem)      // step 2: click the submenu item
       .build()                 // compile the steps into a single Action object
       .perform();              // execute them
```

**Step-by-step explanation.**

1. `actions.moveToElement(menu)` does **not** move the mouse yet. It *adds* a "move" step to the recipe and returns the same `Actions` object.
2. `.click(submenuItem)` adds a "click" step to the same recipe. Because each method returns the `Actions` object, you can keep chaining with dots. This is called a **fluent** style.
3. `.build()` turns the recipe into an executable object of type `Action` (singular, from `org.openqa.selenium.interactions.Action`).
4. `.perform()` sends the whole recipe to the browser, which carries it out.

**Key facts.**

- **If you forget `perform()`, nothing happens, and there is no error.** This is the single most common beginner mistake. The code compiles and runs; the browser simply never receives the instruction.
- You can call `perform()` directly on the `Actions` object: `actions.moveToElement(menu).click().perform();`. In Selenium 4, `perform()` calls `build()` for you. Both forms are valid and you will see both in real projects.
- Use the explicit `build()` form only when you want to keep the compiled `Action` and run it more than once, for example `Action hoverThenClick = actions.moveToElement(menu).click().build();` and later `hoverThenClick.perform();`.
- After `perform()`, the steps are cleared, so the same `Actions` object can be reused for a new chain. Creating a fresh `Actions` is also cheap; it is common to write `new Actions(driver)` inline.

**Variation table: three ways to run a chain.**

| Style | Code | When to use |
|---|---|---|
| Short | `actions.moveToElement(e).click().perform();` | Most everyday code |
| Explicit | `actions.moveToElement(e).click().build().perform();` | Older tutorials, readers who like seeing the build step |
| Stored | `Action a = actions.moveToElement(e).click().build(); a.perform();` | Re-running the same gesture several times |

### 3. Mouse Actions

#### 3.1 Hover: `moveToElement`

**What.** Moves the mouse pointer to the **center** of an element, which triggers CSS `:hover` styles and JavaScript `mouseover` / `mouseenter` events.

**Why.** Many pages hide content until the mouse is over a parent element. The hidden content is in the page, but it is not *visible*, so Selenium refuses to click it. Hovering makes it visible.

**How.**

```java
WebElement menu = driver.findElement(By.id("products-menu"));
new Actions(driver).moveToElement(menu).perform();
```

**Line-by-line.**

- Line 1 finds the menu element, the way you learned on Monday.
- Line 2 creates a new `Actions`, adds a move-to-element step, and runs it. The pointer ends up in the middle of the menu, as if a person had placed their mouse there.

**When and where.** Dropdown menus that open on hover, tooltips, "Delete" icons that appear on table rows, image captions (the Hovers page on the-internet), and product cards that show "Add to cart" on hover.

After the hover, the revealed element must be **waited for**, because it may take a moment to appear (animations are common):

```java
new Actions(driver).moveToElement(menu).perform();
WebElement item = wait.until(ExpectedConditions.visibilityOfElementLocated(By.linkText("Laptops")));
item.click();
```

- `wait` is a `WebDriverWait` from Tuesday's lesson.
- `visibilityOfElementLocated` polls until the element exists **and** is displayed.
- `item.click()` then uses a normal click. Notice that we did not need Actions for the click, only for the hover. Using the simplest tool for each step is good practice.

**Offset variation.** `moveToElement(element, xOffset, yOffset)` moves relative to the element's **center** in Selenium 4 (in Selenium 3 it was relative to the top-left corner; many old blog posts still describe the old behaviour). Example: `moveToElement(chart, 100, -20)` moves 100 pixels right of and 20 pixels above the chart's center, useful for hovering a specific bar to see its tooltip.

**Another variation.** `moveByOffset(x, y)` moves the pointer relative to its *current* position, not an element. It is handy for sliders but fragile, because it depends on where the pointer already is.

#### 3.2 Click, Double-Click, and Right-Click

```java
Actions actions = new Actions(driver);

actions.click(element).perform();            // like element.click(), done as a pointer gesture
actions.doubleClick(element).perform();      // two quick clicks, e.g., edit a cell, select a word
actions.contextClick(element).perform();     // right-click: opens the context menu
```

**Explanation of each.**

- `click(element)` moves to the element and presses and releases the left button. It differs from `element.click()` in that it is a real pointer movement; sometimes this succeeds where `element.click()` is intercepted, but do not use it as a first choice.
- `click()` with **no argument** clicks wherever the pointer currently is. Example: `actions.moveToElement(menu).click().perform();` hovers then clicks the same place.
- `doubleClick(element)` sends two clicks fast enough for the page to treat it as a double-click (the `dblclick` event). Used for inline editing in tables, opening files in a file manager UI, or selecting a word.
- `contextClick(element)` is a right-click. The page may show a **custom** HTML menu, which Selenium can test, or the **browser's native** menu, which Selenium cannot see or click.

**Important note about context menus.** If the site does not replace the right-click menu, the native browser menu opens. Selenium cannot interact with native browser menus, so you cannot click "Inspect" or "Save image as". Test only sites that use custom HTML context menus (like the jQuery ContextMenu demo), where each menu entry is a normal element you can find and click.

**Mini scenario.** A file-manager web app shows "Rename / Delete / Share" on right-click. Test: `contextClick(fileRow)`, wait for the menu entry "Rename" to be visible, click it, type a new name, press Enter, assert the new name appears in the list.

#### 3.3 Click and Hold, Release

```java
actions.clickAndHold(element).perform();   // press the left button and keep it down
// ... do something while it is held ...
actions.release().perform();               // let go
```

**Explanation.** `clickAndHold(element)` moves to the element and presses the left mouse button without letting go. `release()` lets go wherever the pointer currently is. Typical uses: press-and-hold buttons ("hold to confirm"), sliders, resizable panels, and the manual drag-and-drop sequence in the next section.

**Rule.** If you press, always release. A stuck button can confuse later steps in the same session.

### 4. Drag and Drop

**Definition.** Drag and drop means pressing on a **source**, moving the pointer, and releasing over a **target** (or at an offset).

**Why it is tricky.** It is not one event but a chain: mouse down, many mouse moves, mouse up. Pages respond to each part, and some pages use special browser drag events that automation does not always trigger.

**Method A: the convenience method.**

```java
WebElement source = driver.findElement(By.id("draggable"));
WebElement target = driver.findElement(By.id("droppable"));

new Actions(driver).dragAndDrop(source, target).perform();
```

- `dragAndDrop(source, target)` is shorthand for: move to source, press, move to target, release.
- Use it first. It is the shortest and works on many pages.

**Method B: drag by an offset** (for sliders, resizable panels, or any case without a target element).

```java
new Actions(driver).dragAndDropBy(slider, 50, 0).perform();   // 50 pixels right, 0 pixels down
```

- The second and third arguments are `xOffset` and `yOffset` in pixels. Positive x is right, positive y is down.
- Use it when the "target" is just a position.

**Method C: the manual sequence.** It gives you control and is often more reliable on JavaScript-heavy pages.

```java
new Actions(driver)
        .clickAndHold(source)                  // press on the source
        .moveToElement(target)                 // move over the target
        .pause(Duration.ofMillis(300))         // let the page react to the hover
        .release()                             // drop
        .perform();
```

**Line-by-line.**

- `clickAndHold(source)` presses the button on the source.
- `moveToElement(target)` moves the pointer while the button is held. Many libraries only highlight a drop zone after they receive a "move" event; this step supplies it.
- `pause(Duration.ofMillis(300))` waits inside the gesture. `Duration` is `java.time.Duration`; import it.
- `release()` lets go, which is the "drop".

**When to choose which.**

| Situation | Use |
|---|---|
| Source and target are both elements, simple page | `dragAndDrop` |
| Slider handle, resize handle, no target | `dragAndDropBy` |
| `dragAndDrop` does nothing, library needs intermediate moves | manual sequence (Method C) |
| Page uses native HTML5 drag events | see compatibility note below |

**Compatibility note.** There are two families of drag-and-drop on the web:

1. **Mouse-event based** (jQuery UI and many libraries). The Actions API works.
2. **HTML5 native drag and drop** (`draggable="true"` with `dragstart` / `drop` events). Browsers sometimes do not fire these events for synthetic pointer movements, so Actions may do nothing, and Selenium reports no error. Workarounds are a small JavaScript snippet that dispatches the drag events, or testing the behaviour through an API instead. The `the-internet.herokuapp.com/drag_and_drop` page is an example of this HTML5 situation, which is a useful lesson in itself: **always assert the result** of a drag (for example, that column A now has the text "B"), so a silent failure is noticed. The `jqueryui.com/droppable` demo (inside an iframe) works well with Actions.

**Worked example: assert the outcome.**

```java
driver.get("https://jqueryui.com/droppable/");
driver.switchTo().frame(driver.findElement(By.className("demo-frame")));
WebElement source = driver.findElement(By.id("draggable"));
WebElement target = driver.findElement(By.id("droppable"));
new Actions(driver).dragAndDrop(source, target).perform();
Assert.assertEquals(target.getText(), "Dropped!");
driver.switchTo().defaultContent();
```

- `switchTo().frame(...)` moves Selenium's attention into the iframe; the next lesson today explains this in detail. Elements inside a frame cannot be found until you switch.
- `getText()` reads the visible text; the demo changes it from "Drop here" to "Dropped!" on success.
- `Assert.assertEquals(actual, expected)` is the TestNG-style assertion (use JUnit's `assertEquals(expected, actual)` if your project uses JUnit; note the argument order differs).
- `defaultContent()` returns to the main page.

### 5. Keyboard Actions

`sendKeys` on an element (Tuesday) types into that element. The `Actions` class sends keys to whatever currently has **focus**, and it can **hold** keys down.

```java
Actions actions = new Actions(driver);

// Type capital letters by holding Shift
actions.keyDown(Keys.SHIFT).sendKeys("selenium").keyUp(Keys.SHIFT).perform();   // SELENIUM

// Ctrl+A then Ctrl+C: select all and copy
actions.keyDown(Keys.CONTROL).sendKeys("a").sendKeys("c").keyUp(Keys.CONTROL).perform();

// Ctrl+click to multi-select items in a list
actions.keyDown(Keys.CONTROL)
       .click(item1)
       .click(item3)
       .keyUp(Keys.CONTROL)
       .perform();
```

**Line-by-line.**

- `Keys` is an enum (a fixed list of constants) in `org.openqa.selenium` holding special keys: `SHIFT`, `CONTROL`, `ALT`, `ENTER`, `ESCAPE`, `TAB`, `ARROW_DOWN`, `BACK_SPACE`, and so on.
- `keyDown(Keys.SHIFT)` presses and holds Shift. `sendKeys("selenium")` types the letters while Shift is held, so they come out in capitals. `keyUp(Keys.SHIFT)` releases it.
- In the second chain, Ctrl is held while `a` and `c` are typed: the keyboard shortcut for "select all, copy".
- In the third chain, holding Ctrl while clicking two list items is how most multi-select lists (and file explorers) select non-adjacent items. Use `Keys.SHIFT` the same way to select a **range**: click the first item, hold Shift, click the last.

**Rules of thumb.**

- Every `keyDown` needs a matching `keyUp`; otherwise the key stays "pressed" for later steps.
- On macOS use `Keys.COMMAND` instead of `Keys.CONTROL` for shortcuts. Cross-platform suites often pick the key by checking `System.getProperty("os.name")`.
- `actions.sendKeys(element, "text")` clicks the element to focus it and then types.
- `actions.sendKeys(Keys.ESCAPE).perform()` is how you close many pop-ups and custom menus.
- For plain typing into a field you have located, `element.sendKeys("text")` remains the best choice.

**Pressing a key combination without Actions.** `element.sendKeys(Keys.chord(Keys.CONTROL, "a"))` also works for simple chords on a located element. Use it when only one element is involved.

### 6. Scrolling (Selenium 4)

Selenium 4 added scroll actions based on the **wheel** input device.

```java
// Scroll until the element is in view
new Actions(driver).scrollToElement(footer).perform();

// Scroll by a pixel amount (x, y) from the viewport
new Actions(driver).scrollByAmount(0, 600).perform();

// Scroll from an origin element by an amount
import org.openqa.selenium.interactions.WheelInput;
new Actions(driver)
        .scrollFromOrigin(WheelInput.ScrollOrigin.fromElement(list), 0, 300)
        .perform();
```

**Explanation.**

- `scrollToElement(footer)` scrolls the page just enough to bring the element into view. It is the Actions-style counterpart of the JavaScript `scrollIntoView` you saw on Tuesday.
- `scrollByAmount(0, 600)` scrolls 0 pixels horizontally and 600 pixels down. Negative numbers scroll up or left.
- `scrollFromOrigin` starts the wheel at a chosen origin (here, the center of a scrollable list) and scrolls by the amount. Use it when the **inner** element scrolls, such as a chat panel or a list with its own scrollbar, because scrolling the page would not move it.

**When to use.** Infinite-scroll pages: scroll, wait for new items to load, scroll again until the item count is what you expect. Also for elements hidden below the fold that cause `MoveTargetOutOfBoundsException` or `ElementClickInterceptedException`.

**Mini scenario (infinite scroll).**

```java
By items = By.cssSelector(".feed-item");
int previous = 0;
for (int i = 0; i < 5; i++) {
    new Actions(driver).scrollByAmount(0, 2000).perform();
    final int before = previous;
    wait.until(d -> d.findElements(items).size() > before);
    previous = driver.findElements(items).size();
}
```

- The loop scrolls up to five times. After each scroll, a lambda wait polls until the number of items is larger than before, proving that new content loaded.
- `final int before` is needed because a lambda can only use variables that are not changed afterwards (effectively final).
- The lambda `d -> ...` is a `Function<WebDriver, Boolean>`, which is what `wait.until` accepts; you used this style on Tuesday.

### 7. Pauses

```java
new Actions(driver).moveToElement(menu).pause(Duration.ofMillis(500)).click(item).perform();
```

`pause` adds a delay *inside* the action sequence, for example to let a hover animation finish or to keep the pointer still so a tooltip library registers the hover. Keep it short. **For waiting on page state, still use explicit waits.** `pause` is only for the timing of the gesture. A test full of `pause` calls is slow and still flaky, exactly like the `Thread.sleep` habit you were warned about on Tuesday.

### 8. Actions and Waits

- Wait for the target elements to be **visible or clickable before** building the chain.
- After a hover, wait for the revealed element before clicking it.
- If a chain starts with an element that goes stale, re-find it and rebuild the chain. Create the `Actions` object **fresh** when needed; it is cheap.
- Do not mix implicit and explicit waits (Tuesday): the delays can add up unpredictably.

**Worked pattern: hover, wait, click.**

```java
public void openSubmenuItem(WebElement menu, By itemLocator) {
    new Actions(driver).moveToElement(menu).perform();
    wait.until(ExpectedConditions.elementToBeClickable(itemLocator)).click();
}
```

This is exactly the kind of method that goes into a page object.

### 9. Troubleshooting Actions

| Symptom | Likely cause | What to try |
|---|---|---|
| Nothing happens | Missing `.perform()` | Add `.perform()` |
| `MoveTargetOutOfBoundsException` | Element or offset is outside the visible viewport | Scroll the element into view first (`scrollToElement`); check the offset |
| Hover menu opens then closes | Mouse passed over a gap on the path to the submenu | Move to the menu, then **straight** to the submenu item; add a short `pause` |
| Drag and drop does nothing | HTML5 DnD, or the element is not draggable at the grabbed point | Use the manual sequence; try offsets; use a JavaScript fallback |
| Works headed, fails headless | Window too small, element off-screen | Set `--window-size=1920,1080`; scroll into view |
| Click lands on the wrong element | Layout shifted after hover | Wait for stable layout; locate relative to the revealed menu |
| `StaleElementReferenceException` | Page re-rendered between steps | Re-locate elements and rebuild the chain |

#### Troubleshooting walk-through 1: `MoveTargetOutOfBoundsException`

You run:

```java
new Actions(driver).moveToElement(driver.findElement(By.id("chart-bar-7"))).perform();
```

and see:

```text
org.openqa.selenium.interactions.MoveTargetOutOfBoundsException: move target out of bounds
  (Session info: chrome=...)
```

**Diagnosis.** The words "out of bounds" mean the pointer was asked to go somewhere outside the visible browser window. Either the element is below the fold, or an offset pushed the pointer off-screen. **Fix.** First call `new Actions(driver).scrollToElement(element).perform();`, then hover. If you used an offset, remember that in Selenium 4 it is measured from the element's center, not its top-left corner. In headless mode, also set the window size in your options so the layout resembles a desktop.

#### Troubleshooting walk-through 2: the invisible submenu

You run `driver.findElement(By.linkText("Laptops")).click();` and see:

```text
org.openqa.selenium.ElementNotInteractableException: element not interactable
```

**Diagnosis.** The element exists but is hidden (a CSS `display:none` or zero size) until the menu is hovered. **Fix.** Hover the parent first, wait for the item to be visible, then click, as in the pattern from section 8.

#### Troubleshooting walk-through 3: "it passed once and then failed"

A hover test passes locally and fails in the pipeline. The clue is that the pipeline runs headless on a smaller screen, so the menu collapses into a "hamburger" icon and there is nothing to hover. **Fix.** Set an explicit window size in your `DriverFactory` options and assert in the test that the desktop menu is visible before hovering.

---

## Code Example: A Tour of the Actions API

```java
package com.revature.qea.actions;

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class ActionsDemo {

    public static void main(String[] args) {
        WebDriver driver = new ChromeDriver();
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        Actions actions = new Actions(driver);
        try {
            driver.manage().window().maximize();

            // ---------- 1. Hover reveals hidden content ----------
            driver.get("https://the-internet.herokuapp.com/hovers");
            WebElement firstFigure = driver.findElements(By.className("figure")).get(0);
            actions.moveToElement(firstFigure).perform();
            WebElement caption = wait.until(ExpectedConditions.visibilityOf(
                    firstFigure.findElement(By.className("figcaption"))));
            System.out.println("Revealed caption: " + caption.getText());

            // ---------- 2. Right-click ----------
            driver.get("https://swisnl.github.io/jQuery-contextMenu/demo.html");
            WebElement box = driver.findElement(By.cssSelector(".context-menu-one"));
            actions.contextClick(box).perform();
            System.out.println("Context menu items visible: "
                    + driver.findElements(By.cssSelector(".context-menu-item")).size());
            actions.sendKeys(Keys.ESCAPE).perform();   // close the custom menu

            // ---------- 3. Drag and drop (jQuery UI, mouse-event based) ----------
            driver.get("https://jqueryui.com/droppable/");
            driver.switchTo().frame(driver.findElement(By.className("demo-frame")));
            WebElement source = driver.findElement(By.id("draggable"));
            WebElement target = driver.findElement(By.id("droppable"));
            actions.dragAndDrop(source, target).perform();
            System.out.println("Drop result text: " + target.getText());   // "Dropped!"
            driver.switchTo().defaultContent();

            // ---------- 4. Keyboard: hold SHIFT while typing ----------
            driver.get("https://www.saucedemo.com");
            WebElement username = driver.findElement(By.id("user-name"));
            actions.click(username)
                   .keyDown(Keys.SHIFT)
                   .sendKeys("standard")
                   .keyUp(Keys.SHIFT)
                   .perform();
            System.out.println("Typed with SHIFT: " + username.getAttribute("value"));   // STANDARD

            // ---------- 5. Scroll ----------
            driver.findElement(By.id("user-name")).clear();
            driver.findElement(By.id("user-name")).sendKeys("standard_user");
            driver.findElement(By.id("password")).sendKeys("secret_sauce");
            driver.findElement(By.id("login-button")).click();
            WebElement footer = wait.until(
                    ExpectedConditions.presenceOfElementLocated(By.className("footer")));
            actions.scrollToElement(footer).perform();
            System.out.println("Scrolled to the footer");

        } finally {
            driver.quit();
        }
    }
}
```

**Explanation of the code, section by section.**

- **Imports.** Each class used (`By`, `Keys`, `WebDriver`, `WebElement`, `ChromeDriver`, `Actions`, `ExpectedConditions`, `WebDriverWait`, `Duration`) needs an import. Selenium Manager (built into Selenium 4.6+) downloads the matching chromedriver automatically, so `new ChromeDriver()` needs no setup.
- **Construction.** One driver, one `WebDriverWait` of 10 seconds, and one reusable `Actions` object are created before the `try` block.
- **`try` / `finally`.** `driver.quit()` is in `finally` so the browser closes even if a step throws an exception. Otherwise failed runs leave orphaned Chrome processes.
- **Section 1.** `findElements(...).get(0)` finds all figures and takes the first one (index 0). Hovering shows the caption; `visibilityOf(...)` waits for it. Notice `firstFigure.findElement(...)` searches *inside* the figure: a scoped search, as learned in Tuesday's locator lessons.
- **Section 2.** `contextClick` right-clicks. `findElements` returns a list, so `.size()` counts menu items without throwing if there are none. `Keys.ESCAPE` closes the menu so it does not cover the next steps.
- **Section 3.** Switch into the iframe, drag, read the text, switch back.
- **Section 4.** Click to give the field focus, then type with Shift held. `getAttribute("value")` reads what the field now contains (the typed text is not in `getText()` for input fields).
- **Section 5.** Log in, wait for the footer to exist, scroll to it.
- The sample URLs are public practice pages; if one becomes unavailable, substitute an equivalent demo page.

---

## Guided Lab: Hover, Click and Verify on the-internet

**Goal.** Automate the Hovers page end to end, and build the habit of asserting results.

**Prerequisites.** A Maven project with `selenium-java` 4.x and TestNG or JUnit 5, from earlier this week.

1. Create a class `HoverLabTest` in `src/test/java`.
2. In your `@BeforeMethod` (TestNG) or `@BeforeEach` (JUnit 5), create a `ChromeDriver` and a `WebDriverWait` of 10 seconds. Open `https://the-internet.herokuapp.com/hovers`.
3. Locate all figures with `By.className("figure")` and assert there are 3.
4. Loop over the figures. For each one: hover with `moveToElement`, wait for its `.figcaption` to be visible, read the `h5` text inside it (for example `name: user1`).
5. Click the "View profile" link inside the caption and assert that the URL ends with `/users/1` (then `/users/2`, and so on). Navigate back with `driver.navigate().back()` before the next iteration, and **re-find** the figures after navigating, because the old elements are stale.
6. Close the browser in `@AfterMethod` / `@AfterEach`.

**Expected output (console).**

```text
Figure 1 -> name: user1 -> https://the-internet.herokuapp.com/users/1
Figure 2 -> name: user2 -> https://the-internet.herokuapp.com/users/2
Figure 3 -> name: user3 -> https://the-internet.herokuapp.com/users/3
```

**Reference solution for step 4 and 5.**

```java
for (int i = 0; i < 3; i++) {
    List<WebElement> figures = driver.findElements(By.className("figure"));
    WebElement figure = figures.get(i);
    new Actions(driver).moveToElement(figure).perform();
    WebElement caption = wait.until(ExpectedConditions.visibilityOf(
            figure.findElement(By.className("figcaption"))));
    String name = caption.findElement(By.tagName("h5")).getText();
    caption.findElement(By.tagName("a")).click();
    System.out.println("Figure " + (i + 1) + " -> " + name + " -> " + driver.getCurrentUrl());
    driver.navigate().back();
}
```

- The `figures` list is re-created at the top of each iteration so we never use a stale element after `back()`.
- The caption is searched *within* the figure so we get this figure's link, not another one's.

**Reflection.** Which lines would you move into a `HoversPage` class? (Hint: everything that mentions locators.) You will do exactly that in the Page Object lesson.

---

## Common Mistakes

| Mistake | Result | Fix |
|---|---|---|
| Missing `perform()` | Nothing happens, no error | Always end with `perform()` |
| Missing `keyUp` after `keyDown` | Key remains held in later steps | Pair them |
| Using hover without waiting for the revealed element | `NoSuchElementException` or `ElementNotInteractableException` | Wait for visibility |
| Using `dragAndDrop` on HTML5 draggable elements and trusting it | Silent failure | Verify the result; use the manual sequence or a JS workaround |
| Chain includes an element that has become stale | `StaleElementReferenceException` | Re-find and rebuild |
| Offsets assumed from the top-left corner | Click in the wrong place (Selenium 4 uses the element center) | Compute from the center |
| Using Actions where a normal `click()` would do | Needless complexity | Use the simplest tool that works |
| Long `pause()` calls instead of waits | Slow, flaky tests | Use explicit waits for page state |
| Trying to click a native browser context menu | Cannot be done | Test only custom HTML menus |
| Forgetting to switch into an iframe before dragging inside it | `NoSuchElementException` | `driver.switchTo().frame(...)` first |

---

## Practice Exercises

1. **Hover caption.** On `https://the-internet.herokuapp.com/hovers`, hover over each of the three images and print the user name that is revealed. Use an explicit wait after each hover.
2. **Hover menu.** On a site with a hover navigation menu (for example, `https://www.w3schools.com`), open a submenu by hovering and click an item. Verify by URL.
3. **Right-click.** Use `contextClick` on the jQuery ContextMenu demo, then click one of the menu items and read the result (the demo shows an alert, so you will need the next lesson).
4. **Double-click.** Find a page with a double-click demo (for example, the W3Schools "dblclick" Tryit example, inside an iframe) and trigger it. Assert the visible change.
5. **Drag and drop.** Automate the jQuery UI droppable example using (a) `dragAndDrop` and (b) the manual `clickAndHold` / `moveToElement` / `release` sequence. Then try the HTML5 page `the-internet.herokuapp.com/drag_and_drop` and describe what happens.
6. **Slider.** On `https://the-internet.herokuapp.com/horizontal_slider`, set the slider to 3.5 and verify the displayed value. Do it two ways: arrow keys, and `clickAndHold` + `moveByOffset`.
7. **Keyboard.** Use `keyDown(Keys.SHIFT)` to type a word in capitals on the SauceDemo username field, then use `Keys.CONTROL` + `a` to select all text in the field and press `Keys.BACK_SPACE` to delete it. Assert that the field is empty.
8. **Key presses page.** On `https://the-internet.herokuapp.com/key_presses`, press several keys with `Actions.sendKeys` and verify that the "You entered:" text changes each time.
9. **Scroll.** On `https://the-internet.herokuapp.com/infinite_scroll`, scroll with `scrollByAmount` until at least 10 paragraphs exist. Use an explicit wait between scrolls.
10. **SauceDemo scroll and click.** Log in to `https://www.saucedemo.com`, use `scrollToElement` to reach the footer, then verify the "Twitter" (or "X") footer link is displayed.
11. **Helper method.** Write a method `hoverAndClick(WebElement menu, By item)` that hovers, waits for the item to be clickable, and clicks it. Think about where it would live in a page object.
12. **Think.** Which of these tasks could be done with a plain `click()` and which truly need Actions? Why is using the simplest tool still the better engineering choice?

---

## Solutions and Hints

**1. Hover caption.** Hint: use `findElements(By.className("figure"))`. Solution:

```java
List<WebElement> figures = driver.findElements(By.className("figure"));
for (WebElement figure : figures) {
    new Actions(driver).moveToElement(figure).perform();
    WebElement name = wait.until(ExpectedConditions.visibilityOf(
            figure.findElement(By.cssSelector(".figcaption h5"))));
    System.out.println(name.getText());
}
```

Each iteration hovers the figure, waits for the `h5` inside its caption, and prints it.

**2. Hover menu.** Hint: hover the parent, wait for the child with `elementToBeClickable`, click, then use `wait.until(ExpectedConditions.urlContains("..."))`. Menus change often; inspect the live page and choose stable locators.

**3. Right-click.** Hint: after `contextClick(box)`, wait for `.context-menu-item` to be visible, click one, and handle the alert (see the Alerts lesson).

**4. Double-click.** Hint: the example is inside an iframe, so call `switchTo().frame(...)` first. Then `new Actions(driver).doubleClick(element).perform();` and compare the element's text or colour afterward.

**5. Drag and drop.** Solution for (b) is the code in section 4, Method C. For the HTML5 page, expect the headers (A and B) not to swap. That is the lesson: Actions may report success even when the page did nothing. Assert on the header text, and consider a JavaScript fallback or testing the feature through other means.

**6. Slider.**

```java
WebElement slider = driver.findElement(By.cssSelector("input[type='range']"));
slider.click();                                      // focus the slider
for (int i = 0; i < 7; i++) {
    slider.sendKeys(Keys.ARROW_RIGHT);               // each press moves by one step (0.5)
}
Assert.assertEquals(driver.findElement(By.id("range")).getText(), "3.5");
```

The slider has a step of 0.5 and starts at 0 (the click may move it to the middle, so reading the value first and computing the number of key presses is more robust). The `moveByOffset` approach needs trial and error and is more fragile; that comparison is the point of the exercise.

**7. Keyboard.**

```java
WebElement username = driver.findElement(By.id("user-name"));
new Actions(driver).click(username).keyDown(Keys.SHIFT).sendKeys("abc").keyUp(Keys.SHIFT).perform();
new Actions(driver).keyDown(Keys.CONTROL).sendKeys("a").keyUp(Keys.CONTROL)
        .sendKeys(Keys.BACK_SPACE).perform();
Assert.assertEquals(username.getAttribute("value"), "");
```

On macOS replace `CONTROL` with `COMMAND`.

**8. Key presses.** Hint: the result paragraph has id `result`. Use `new Actions(driver).sendKeys(Keys.ENTER).perform();` then `getText()`.

**9. Scroll.** Hint: loop while `findElements(By.cssSelector(".jscroll-added")).size() < 10`, scroll, then wait for the count to increase. Limit the loop to a maximum number of tries so a broken page cannot loop forever.

**10. SauceDemo footer.** Hint: the social links use classes such as `social_twitter`. Use `isDisplayed()` after `scrollToElement`.

**11. Helper method.**

```java
private void hoverAndClick(WebElement menu, By item) {
    new Actions(driver).moveToElement(menu).perform();
    wait.until(ExpectedConditions.elementToBeClickable(item)).click();
}
```

In a page object this would be a private helper used by public methods such as `openLaptops()`.

**12. Think.** Plain `click()` handles clicking buttons, links, and typing in fields. Actions is truly needed for hover, drag, right-click, double-click, held keys, and wheel scroll. Simpler code has fewer ways to fail and is easier for teammates to read and maintain.

---

## Self-Check Questions

1. **What happens if you build an Actions chain but never call `perform()`?** Nothing; no error is raised, the browser never receives the instructions.
2. **Is `build()` required before `perform()` in Selenium 4?** No. `perform()` builds the chain for you; `build()` is useful only when you want to keep the compiled `Action` for reuse.
3. **Why must you wait after a hover?** The revealed element may take time to appear because of animations or scripts; clicking too early causes `NoSuchElementException` or `ElementNotInteractableException`.
4. **From where is an offset measured in `moveToElement(el, x, y)` in Selenium 4?** From the element's center.
5. **Why can `dragAndDrop` silently fail?** Pages using HTML5 native drag events may not react to synthetic pointer events; the test must assert the outcome.
6. **What is the danger of `keyDown` without `keyUp`?** The key stays logically pressed and affects later actions.
7. **When should you use `scrollFromOrigin`?** When an inner scrollable container (not the whole page) must scroll.
8. **Can Selenium click items in the browser's native right-click menu?** No; only custom HTML menus are testable.

---

## Summary

- The **Actions API** (`new Actions(driver)`) builds sequences of low-level mouse, keyboard, and wheel input and executes them with **`perform()`**.
- Core methods: `moveToElement` (hover), `click`, `doubleClick`, `contextClick`, `clickAndHold`, `release`, `dragAndDrop`, `dragAndDropBy`, `keyDown` / `keyUp`, `sendKeys`, `scrollToElement`, `scrollByAmount`, `scrollFromOrigin`, and `pause`.
- Hover-driven content needs a **wait** after the hover.
- Drag and drop works reliably with mouse-event-based libraries; **HTML5 native** drag and drop may need workarounds, and every drag should be followed by an assertion.
- Always pair `keyDown` with `keyUp`; forgetting `perform()` is the classic bug.
- Use Actions only when plain `click()` / `sendKeys()` cannot express the gesture.
- Wrap Actions gestures in well-named page-object methods so tests stay readable. This is where the next lessons take you.

---

## Additional Resources

- Selenium documentation, *Actions API overview*: https://www.selenium.dev/documentation/webdriver/actions_api/
- Selenium documentation, *Mouse actions*: https://www.selenium.dev/documentation/webdriver/actions_api/mouse/
- Selenium Java API, `Actions` class: https://www.selenium.dev/selenium/docs/api/java/org/openqa/selenium/interactions/Actions.html
