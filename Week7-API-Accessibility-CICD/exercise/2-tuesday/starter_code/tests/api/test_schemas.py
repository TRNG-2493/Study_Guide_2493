import pytest
# Stage hints: use fixtures, @pytest.mark.parametrize with ids, and replace pytest.skip with real asserts.

@pytest.mark.smoke
def test_item_list_matches_schema():
    pytest.skip('TODO')

@pytest.mark.regression
def test_single_item_matches_schema():
    pytest.skip('TODO')

