import pytest
# Stage hints: use fixtures, @pytest.mark.parametrize with ids, and replace pytest.skip with real asserts.

@pytest.mark.regression
def test_pagination():
    pytest.skip('TODO')

@pytest.mark.regression
def test_bad_paging_is_400():
    pytest.skip('TODO')

@pytest.mark.regression
def test_category_filter():
    pytest.skip('TODO')

@pytest.mark.regression
def test_name_search_is_case_insensitive():
    pytest.skip('TODO')

