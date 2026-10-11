-- ============================================================================
-- Part B - Joins: INNER, LEFT, RIGHT, FULL (time-box: 30 min)
-- Run:  python lab_runner.py sql/part_b_joins.sql [--only B3]
-- Fresh, untouched seed data every run. Return EXACTLY the columns named in RETURNS, in that order
-- (aliases are yours to choose, row order does not matter unless the task says so).
-- Your SQLite must be 3.39 or newer for B4/B5. Check:  python -c "import sqlite3; print(sqlite3.sqlite_version)"
-- If it is older (or you are on MySQL), skip B4/B5 and do their "emulation" versions in B6 + the note in the README.
-- ============================================================================

-- @Q B1 INNER JOIN across three tables: every "usable" run
-- TASK: list each run together with its build name and test case title. A run that has no matching
--       build OR no matching case must NOT appear.
-- RETURNS: run_id, build_name, title, result   (expect 40 rows: 44 runs minus 4 unusable ones)
-- HINT-1: test_runs is the "many" side; join it to builds and to test_cases on their keys.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q B2 LEFT JOIN + IS NULL (anti-join): cases that were never run
-- TASK: every test case that has no row in test_runs. Include retired cases for now.
-- RETURNS: case_id, title, status
-- HINT-1: keep ALL test_cases (left side), try to match runs, then keep the rows where the match failed.
-- HINT-2: after LEFT JOIN, test a column of the RIGHT table that can never be NULL in a real match (its primary key).
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q B3 LEFT JOIN + IS NULL again: builds without any run
-- RETURNS: build_id, build_name
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q B4 RIGHT JOIN: runs that point at a test case that does not exist
-- TASK: write it as a RIGHT JOIN with test_runs on the right (needs SQLite 3.39+). Return the runs that found no case.
-- RETURNS: run_id, case_id        (expect 3 rows - read the case_id column: why 3 and not 2?)
-- HINT-1: FROM test_cases AS c RIGHT JOIN test_runs AS r ON ... WHERE c.case_id IS NULL
-- HINT-2: if your SQLite is older: swap the table order and use LEFT JOIN (a RIGHT JOIN is a LEFT JOIN with the tables swapped).
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q B5 FULL JOIN: mismatches on BOTH sides in one query
-- TASK: FULL JOIN test_cases and test_runs on case_id, keep only rows where one side is missing,
--       and label them with a CASE expression: 'case without run' or 'run without case'.
-- RETURNS: case_id, run_id, side     (case_id / run_id come from the table that has the row; expect 6 rows)
-- HINT-1: WHERE c.case_id IS NULL OR r.run_id IS NULL
-- HINT-2: side = CASE WHEN r.run_id IS NULL THEN 'case without run' ELSE 'run without case' END
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q B6 Emulate the FULL JOIN of B5 WITHOUT RIGHT/FULL JOIN (works on any SQLite and on MySQL)
-- TASK: produce the SAME 6 rows as B5 using LEFT JOINs and UNION ALL (one anti-join per side).
--       Then (stretch, not auto-checked) prove equality with two EXCEPT queries as in the FULL JOIN lesson.
-- RETURNS: case_id, run_id, side     (identical to B5)
-- HINT-1: part 1 = cases LEFT JOIN runs WHERE run missing;  part 2 = runs LEFT JOIN cases WHERE case missing.
-- HINT-2: UNION ALL is correct here because the two halves can never overlap; plain UNION would also work but hides that fact.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q B7 Multi-table query: defects with their full context
-- TASK: for every defect that points to an existing run, show the defect, the build it was found in,
--       the title of the test case of that RUN, and the defect severity. (4 tables, 3 joins.)
-- RETURNS: defect_id, build_name, title, severity   (expect 10 rows; 2 defects have no usable run)
-- HINT-1: defects -> test_runs (on run_id) -> builds (on build_id) and test_runs -> test_cases (on case_id).
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;
