"""Shared fixtures for all tests in this folder. PyTest loads this file automatically.

NEVER `import conftest` in a test file; just request a fixture by its parameter name.
Every fixture below is a STUB: it skips so the suite runs from minute one.
Replace the `pytest.skip(...)` line with the real implementation as you reach each task.
"""
import pytest

# from defect_log import DefectLog      # TODO (Task 2): uncomment when you need it


def pytest_configure(config):
    # TODO (Stretch D): register an extra marker here with config.addinivalue_line(...)
    pass


# ---- Task 5: safety net ------------------------------------------------------------------
# TODO (Task 5): add an AUTOUSE fixture `block_real_network(monkeypatch)` that replaces
#   socket.socket.connect with a function raising RuntimeError("Real network access attempted").
#   You will need `import socket` at the top of this file.


# ---- Task 2: function-scope fixtures ----------------------------------------------------------
@pytest.fixture
def empty_log():
    pytest.skip("TODO (Task 2): return a brand-new DefectLog()")


@pytest.fixture
def populated_log():
    pytest.skip("TODO (Task 2): DefectLog with 3 OPEN defects: critical, low, high (in that order)")


@pytest.fixture
def export_file(tmp_path):
    pytest.skip("TODO (Task 2): YIELD tmp_path / 'defects.csv'; after the yield, delete the file")


# ---- Task 3: scopes ---------------------------------------------------------------------------
@pytest.fixture
def qa_config():
    pytest.skip("TODO (Task 3): SESSION scope, read-only mapping with max_title_length=80, release='1.0'")


@pytest.fixture
def setup_calls():
    pytest.skip("TODO (Task 3): SESSION scope, returns an empty list shared by the whole run")


@pytest.fixture
def big_log(setup_calls):
    pytest.skip("TODO (Task 3): MODULE scope, 200 defects; append 'big_log' to setup_calls when built")


# ---- Task 4: indirect parametrization -------------------------------------------------------------
@pytest.fixture
def log_with_open_defects(request):
    pytest.skip("TODO (Task 4): build a log containing request.param open defects")
