"""THE LOCATOR CATALOG - the Project 1 milestone artifact. (INSTRUCTOR SOLUTION)

One row per important element: a stable name, CSS and XPath that must agree, the number of
matches we expect, how stable the selector is (1 = best, 7 = worst, see
basic-and-attribute-selectors.md Part 3) and a one-line reason.
"""
from dataclasses import dataclass
from typing import Optional

PAGES = ("login", "login_error", "inventory")

TECHNIQUES = (
    "data-test",         # [data-test='...']
    "id",                # #something
    "attribute",         # [type='password'], [placeholder='...']
    "attr-prefix",       # [attr^='...']  / starts-with()
    "attr-substring",    # [attr*='...']  / contains()
    "tag-class",         # tag.class
    "combinator-child",  # a > b
    "combinator-sibling",  # a + b / following-sibling::
    "pseudo-position",   # :nth-child / :last-child / (...)[n]
    "pseudo-not",        # :not(...) / not(...)
    "pseudo-has",        # :has(...)  (CSS "going up")
    "xpath-axis",        # ancestor:: / following-sibling:: ...
    "xpath-function",    # contains() / starts-with() / text()
)


@dataclass(frozen=True)
class CatalogRow:
    name: str
    page: str
    css: str
    xpath: str
    expected: int
    technique: str
    stability: int
    why: str
    expected_text: Optional[str] = None
    smoke: bool = False

    def __post_init__(self):
        # TODO (Task 5): reject bad rows by raising ValueError with a clear message that contains
        # these phrases (the tests will look for them with pytest.raises(..., match=...)):
        #   page not in PAGES              -> "unknown page"
        #   technique not in TECHNIQUES    -> "unknown technique"
        #   expected < 1                   -> "at least 1"
        #   stability outside 1..7         -> "stability must be 1..7"
        #   expected_text given but expected != 1 -> "expected_text only makes sense"
        pass


CATALOG = [
    # Three finished example rows (one per kind of page). Study them, then add at least 13 more.
    # Columns: name, page, css, xpath, expected, technique, stability, why, [expected_text], [smoke]
    CatalogRow("login_logo", "login", ".login_logo", "//div[@class='login_logo']", 1,
               "tag-class", 5, "semantic class; text is the brand name", "Swag Labs", smoke=True),
    CatalogRow("error_message", "login_error", "[data-test='error']", "//h3[@data-test='error']", 1,
               "data-test", 1, "dedicated test attribute on the message itself",
               "Epic sadface: Username and password do not match any user in this service", smoke=True),
    CatalogRow("cart_link", "inventory", "[data-test='shopping-cart-link']",
               "//a[@data-test='shopping-cart-link']", 1,
               "data-test", 1, "dedicated test attribute"),
    # TODO (Tasks 2 and 3): your rows go here. See README "The rows you must cover".
]


def rows_for(page):
    """All rows that belong to one page name."""
    return [row for row in CATALOG if row.page == page]


def get_row(name):
    """Return the row called `name`.

    TODO (Task 5): if there is no such row, raise KeyError whose message contains
    "No catalog row named 'xyz'" and lists the known row names.
    """
    raise NotImplementedError("TODO Task 5: get_row")
