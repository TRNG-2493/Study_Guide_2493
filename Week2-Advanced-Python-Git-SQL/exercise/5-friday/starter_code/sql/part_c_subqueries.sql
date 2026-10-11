-- ============================================================================
-- Part C - Subqueries (time-box: 25 min)
-- Run:  python lab_runner.py sql/part_c_subqueries.sql [--only C2]
-- Return EXACTLY the columns named in RETURNS, in that order.
-- ============================================================================

-- @Q C1 IN (subquery): cases that failed at least once
-- RETURNS: case_id, title
-- HINT-1: WHERE case_id IN (SELECT case_id FROM test_runs WHERE result = 'fail')
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q C2 THE NOT IN TRAP: never-run cases, written with NOT IN
-- TASK: write "cases that have no run" with NOT IN (SELECT case_id FROM test_runs). Run it.
--       It returns ZERO rows although B2 found three cases. In EXPECTED_FINDINGS.md explain WHY in one sentence.
-- RETURNS: case_id, title      (expected here: 0 rows - the bug is the lesson)
-- HINT-1: look at the case_id column of test_runs: is there anything in it that is not a number?
-- HINT-2: x NOT IN (1, 2, NULL) is never TRUE. See "three-valued logic" in Thursday's WHERE lesson.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q C3 NOT EXISTS: the correct anti-join with a correlated subquery
-- TASK: cases with no run, written with NOT EXISTS. Compare with B2 (same 3 rows).
-- RETURNS: case_id, title
-- HINT-1: WHERE NOT EXISTS (SELECT 1 FROM test_runs AS r WHERE r.case_id = c.case_id)
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q C4a Scalar subquery: runs slower than average (naive)
-- TASK: runs whose duration_sec is greater than the average duration_sec of ALL runs. Use a scalar subquery.
-- RETURNS: run_id, duration_sec     (look at the result: only ONE row. Why?)
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q C4b Scalar subquery: slower than the average of VALID durations
-- TASK: same, but the average must only use durations between 1 and 3600 seconds.
--       (Out-of-range values are data defects; do not let them distort the baseline.)
-- RETURNS: run_id, duration_sec
-- HINT-1: put the filter INSIDE the subquery: (SELECT AVG(duration_sec) FROM test_runs WHERE duration_sec BETWEEN 1 AND 3600)
-- HINT-2: the outer query may still return the 86400 row: that is fine, it IS slower than average.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q C5 EXISTS with a condition: defects logged against a run that PASSED
-- RETURNS: defect_id
-- HINT-1: WHERE EXISTS (SELECT 1 FROM test_runs AS r WHERE r.run_id = d.run_id AND r.result = 'pass')
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;
