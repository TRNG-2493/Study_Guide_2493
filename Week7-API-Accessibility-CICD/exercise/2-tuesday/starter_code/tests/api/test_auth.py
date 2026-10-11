import pytest
# Stage hints: use fixtures, @pytest.mark.parametrize with ids, and replace pytest.skip with real asserts.

@pytest.mark.smoke
def test_login_success():
    pytest.skip('TODO')

@pytest.mark.regression
def test_login_bad_credentials_401():
    pytest.skip('TODO')

@pytest.mark.regression
def test_write_without_token_is_401():
    pytest.skip('TODO')

@pytest.mark.regression
def test_invalid_token_is_401():
    pytest.skip('TODO')

@pytest.mark.regression
def test_user_cannot_delete_is_403():
    pytest.skip('TODO')

