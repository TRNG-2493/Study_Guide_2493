import pytest
# Stage hints: use fixtures, @pytest.mark.parametrize with ids, and replace pytest.skip with real asserts.

@pytest.mark.smoke
def test_health():
    pytest.skip('TODO')

@pytest.mark.smoke
def test_create_item():
    pytest.skip('TODO')

@pytest.mark.regression
def test_get_item_by_id():
    pytest.skip('TODO')

@pytest.mark.regression
def test_put_replaces_item():
    pytest.skip('TODO')

@pytest.mark.regression
def test_patch_changes_only_sent_fields():
    pytest.skip('TODO')

@pytest.mark.regression
def test_delete_then_get_is_404():
    pytest.skip('TODO')

