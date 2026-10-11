"""BasePage: what every page object shares.  (Task 2c; lesson converting-scripts-to-pom.md Step 3)"""
# TODO: class BasePage with
#   * PATH = ""            (children override, e.g. "/cart.html")
#   * __init__(self, page) storing self.page
#   * expect_loaded()      where the old `expect(page).to_have_url(...)` checks now live.
#
# PITFALL (read the error message if you hit it!): with base_url configured, Playwright
# joins a *relative glob* such as f"**{PATH}" onto the base URL, so it never matches.
# Use a compiled regex instead:   re.compile(rf"{re.escape(self.PATH)}$")
