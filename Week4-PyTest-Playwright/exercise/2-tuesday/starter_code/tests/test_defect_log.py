"""TASKS 2, 3, 4 - fixtures, scopes, indirect parametrization for DefectLog.

Fixtures live in tests/conftest.py. Test names tell you the behaviour to check; the TODO in
each body tells you what to assert. Replace each pytest.fail(...) with real assertions.
"""
import pytest

from defect_log import SEVERITIES, DefectLog


# ---------------- Task 2: fixtures --------------------------------------------------------------
def test_new_log_is_empty(empty_log):
    pytest.fail("TODO: total_count() and open_count() are both 0")


def test_add_returns_incrementing_ids(empty_log):
    pytest.fail("TODO: first add returns 1, second returns 2")


def test_open_count_after_population(populated_log):
    pytest.fail("TODO: total 3 and open 3")


def test_close_reduces_open_count(populated_log):
    pytest.fail("TODO: close defect 1 -> open_count 2, total_count still 3")


def test_fixtures_are_isolated(populated_log):
    pytest.fail("TODO: this test must see 3 open defects even though the previous test closed one. Why does it?")


def test_titles_by_severity_only_returns_open(populated_log):
    pytest.fail("TODO: close the critical one; critical list is empty; high list has exactly the 'high' title")


def test_close_unknown_id_raises(populated_log):
    pytest.fail("TODO: pytest.raises(KeyError) for id 99")


def test_close_twice_raises(populated_log):
    pytest.fail("TODO: pytest.raises(ValueError, match='already closed') on the second close")


def test_export_csv_writes_header_and_rows(populated_log, export_file):
    pytest.fail("TODO: export, read the file back with the csv module, check header row and the first data row")


# Task 2b: turn these four invalid inputs into ONE parametrized test with ids
def test_add_rejects_bad_input(empty_log):
    pytest.fail("TODO: parametrize (title, severity): ('', 'low'), ('   ', 'low'), ('Real', 'urgent'), ('Real', '')")


# Task 2c: one test per severity without writing four functions
def test_add_accepts_every_severity(empty_log):
    pytest.fail("TODO: parametrize over SEVERITIES; add one defect, check titles_by_severity returns it")


# ---------------- Task 3: scopes -------------------------------------------------------------------
def test_session_config_is_read_only(qa_config):
    pytest.fail("TODO: check release == '1.0' and that assigning to the config raises TypeError")


def test_big_log_counts(big_log):
    pytest.fail("TODO: total 200; 'high' defects are those with number % 4 == 0 -> how many? (build it in conftest first)")


def test_big_log_second_reader(big_log):
    pytest.fail("TODO: another READ-ONLY check on big_log (e.g. the first 'low' title)")


def test_big_log_was_built_only_once_in_this_module(big_log, setup_calls):
    pytest.fail("TODO: assert setup_calls.count('big_log') == 1")


# ---------------- Task 4: indirect -------------------------------------------------------------------
def test_open_count_matches_built_log(log_with_open_defects):
    pytest.fail("TODO: parametrize with indirect so 0, 1, 5 are sent THROUGH the fixture; add a second, direct parameter for the expected count")


def test_closing_everything_leaves_zero_open(log_with_open_defects):
    pytest.fail("TODO: indirect=True with 2 and 3; close every defect; open_count() == 0")


# ---------------- Stretch A / B ------------------------------------------------------------------------
@pytest.mark.skip(reason="Stretch A: write a fixture with params=[...severities...] and a test using it")
def test_stretch_parametrized_fixture():
    ...


@pytest.mark.skip(reason="Stretch B: use pytest.param(..., marks=pytest.mark.xfail(strict=True)) for a 500-char title")
def test_stretch_param_with_marks():
    ...
