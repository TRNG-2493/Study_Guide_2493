"""Shared fixtures. pytest.ini puts the project root on the path so `import membership` works."""
import pytest
from membership import Account


@pytest.fixture
def new_account():
    """A factory: new_account(balance_due=0) returns a fresh Account in state Pending."""
    def _make(balance_due=0):
        return Account(balance_due=balance_due)
    return _make
