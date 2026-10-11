"""Root conftest: shared fixtures and report hooks. PyTest finds this file automatically.

Lesson: html-reporting.md sections 8-10.
"""
import pytest  # noqa: F401  (you will need it for the stretch task)

# TODO (Task 6a): customise the report title.
#   def pytest_html_report_title(report):
#       report.title = "..."

# TODO (Task 6b): add rows to the Environment table: Project, Tester (your name), Environment.
#   Use the `pytest_configure` hook and `config.stash[metadata_key]`
#   (from pytest_metadata.plugin import metadata_key). NEVER put passwords or tokens here.

# TODO (Task 6c): add a "Description" column that shows each test's docstring.
#   You need THREE hooks: pytest_html_results_table_header, pytest_html_results_table_row
#   and a hookwrapper pytest_runtest_makereport. The header and the row must add the SAME number of cells.
