import pytest
# Stage hints: use fixtures, @pytest.mark.parametrize with ids, and replace pytest.skip with real asserts.

@pytest.mark.regression
def test_missing_item_is_404():
    pytest.skip('TODO')

@pytest.mark.regression
def test_duplicate_name_is_409():
    pytest.skip('TODO')

@pytest.mark.regression
def test_invalid_create_is_422():
    pytest.skip('TODO')

@pytest.mark.regression
def test_invalid_json_is_400():
    pytest.skip('TODO')

