"""Custom assertions (Wednesday: custom-assertions.md).  TODO Task 4."""


def assert_locator_count(page, selector, expected, label):
    """Assert that `selector` (CSS, or 'xpath=...') matches exactly `expected` elements.

    TODO (Task 4):
      * hide this helper from tracebacks (Wednesday trick)
      * count the matches with page.locator(selector).count()
      * on failure, the message must contain: the label, expected, actual, the selector, page.url
    """
    raise NotImplementedError("TODO Task 4: assert_locator_count")


def assert_locator_text(page, selector, expected_text, label):
    """Assert the single element matched by `selector` has exactly this visible text.

    TODO (Task 4): require exactly 1 match first (explain if not), then compare
    page.locator(selector).inner_text().strip() with expected_text, with a helpful message.
    """
    raise NotImplementedError("TODO Task 4: assert_locator_text")
