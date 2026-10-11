"""Turn catalog rows into pytest.param objects (Tuesday: parametrize; Monday: markers)."""
import pytest

from locator_catalog.catalog import rows_for


def catalog_params(page):
    """One pytest.param per row of `page`.

    TODO (Task 6): give each param id=row.name (readable test names), and put
    @pytest.mark.smoke on the rows whose `smoke` flag is True (marks=[...]).
    """
    return [pytest.param(row) for row in rows_for(page)]
