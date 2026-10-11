-- ============================================================================
-- Part A - DML and constraints practice (time-box: 25 min)
-- Run:  python lab_runner.py sql/part_a_dml.sql          (all tasks, top to bottom)
--       python lab_runner.py sql/part_a_dml.sql --only A4 (one task)
-- The runner builds a FRESH in-memory copy of the database every time, so you cannot break the seed.
-- Tasks share ONE session and run top to bottom: later tasks see the changes made by earlier ones.
-- Replace every placeholder "SELECT 'TODO' AS todo;" with your own statement(s).
-- Statements marked (given) are already written for you: do not edit them.
-- ============================================================================

-- @Q A1 Find the orphans the database never complained about
-- TASK: foreign keys are declared but not enforced yet. Ask SQLite for every existing violation.
-- RETURNS: the output of PRAGMA foreign_key_check (5 rows).
-- HINT-1: it is a PRAGMA, not a SELECT. See "Finding existing violations" in the constraints lesson.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A2a Turn enforcement on for this connection
-- TASK: switch foreign key enforcement ON, then (given, next task) prove it works.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A2b EXPECT-ERROR: insert a run for a case that does not exist
-- TASK: INSERT one test_runs row with run_id 100, build_id 1, case_id 999, tester 'Sam',
--       run_date '2026-03-03', result 'pass', duration_sec 60. PREDICT first: will it work? It must be REJECTED.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A2c (given) The rejected row must not exist
SELECT COUNT(*) AS rows_with_run_id_100 FROM test_runs WHERE run_id = 100;

-- @Q A3a Insert one new build
-- TASK: INSERT build_id 7, build_name 'b2026.05.2', release 'R3.3', built_date '2026-05-11',
--       reported_total 2, reported_passed 1, reported_failed 1. Name the columns explicitly.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A3b Insert two runs for the new build with ONE statement
-- TASK: one multi-row INSERT into test_runs:
--       (201, build 7, case 1, 'Priya', '2026-05-12', 'pass', 95) and
--       (202, build 7, case 7, 'Marco', '2026-05-12', 'fail', 310).
-- HINT-1: INSERT INTO t (cols) VALUES (...), (...);
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A3v (given) Verify the new build and its runs
SELECT b.build_id, b.build_name, COUNT(r.run_id) AS runs
FROM builds AS b LEFT JOIN test_runs AS r ON r.build_id = b.build_id
WHERE b.build_id = 7
GROUP BY b.build_id, b.build_name;

-- @Q A4a UPDATE step 1: preview with the SAME WHERE you will use
-- TASK: one run has result 'PASSED' (upper case, not an allowed value). SELECT run_id, result for the rows
--       you are about to change. It must show exactly ONE row.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A4b UPDATE step 2: fix exactly those rows
-- TASK: set result to 'pass' for the previewed row(s). Use the same WHERE as the preview.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A4v (given) Result distribution after the fix
SELECT result, COUNT(*) AS n FROM test_runs GROUP BY result ORDER BY result;

-- @Q A5a DELETE step 1: preview the duplicate pair
-- TASK: runs 18 and 44 are the same execution entered twice. SELECT both rows (all columns) so you can see they are identical.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A5b DELETE step 2: remove only the surplus copy (the higher run_id)
-- TASK: delete run 44 and nothing else.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A5v (given) Exactly one of the pair survives
SELECT run_id FROM test_runs WHERE run_id IN (18, 44);

-- @Q A6a Create a quarantine table
-- TASK: CREATE TABLE quarantine_runs with the same 7 columns as test_runs (run_id as INTEGER PRIMARY KEY)
--       plus reason TEXT NOT NULL. No foreign keys: it is a parking lot for bad rows.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A6b Copy the orphan runs into quarantine
-- TASK: INSERT ... SELECT every test_runs row whose case_id is NOT NULL and does not exist in test_cases.
--       Use the literal 'orphan case_id' as the reason. (Part D/E will count these: expect 2 rows.)
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A6c Remove the quarantined rows from test_runs
-- TASK: DELETE from test_runs exactly the rows now present in quarantine_runs (use a subquery, not hard-coded ids).
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A6v1 (given) What is in quarantine
SELECT run_id, case_id, reason FROM quarantine_runs ORDER BY run_id;

-- @Q A6v2 (given) The orphans are gone from test_runs
SELECT COUNT(*) AS orphans_left FROM test_runs WHERE case_id IN (98, 99);

-- @Q A7a Build a strict table
-- TASK: CREATE TABLE test_cases_strict:
--         case_id  INTEGER PRIMARY KEY,
--         title    TEXT NOT NULL,
--         module   TEXT NOT NULL,
--         priority TEXT NOT NULL CHECK (priority IN ('P1','P2','P3')),
--         status   TEXT NOT NULL DEFAULT 'active',
--         UNIQUE (module, title)
--       Then run the (given) INSERTs below. PREDICT each result before you run it.
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A7b (given) A valid row: must succeed
INSERT INTO test_cases_strict (case_id, title, module, priority) VALUES (1, 'Login with valid credentials', 'login', 'P1');

-- @Q A7c (given) EXPECT-ERROR: priority outside the allowed list
INSERT INTO test_cases_strict (case_id, title, module, priority) VALUES (2, 'Logout', 'login', 'P9');

-- @Q A7d (given) EXPECT-ERROR: NOT NULL title
INSERT INTO test_cases_strict (case_id, title, module, priority) VALUES (3, NULL, 'login', 'P2');

-- @Q A7e (given) EXPECT-ERROR: same module + title again
INSERT INTO test_cases_strict (case_id, title, module, priority) VALUES (4, 'Login with valid credentials', 'login', 'P1');

-- @Q A7v (given) Only the valid row got in, and the DEFAULT was applied
SELECT case_id, title, status FROM test_cases_strict ORDER BY case_id;

-- @Q A8a Safety net, step 1: open a transaction
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A8b The classic disaster: DELETE without WHERE
-- TASK: delete ALL rows from defects (yes, on purpose, inside the transaction).
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A8c (given) Inside the transaction the table looks empty
SELECT COUNT(*) AS defects_inside_transaction FROM defects;

-- @Q A8d Safety net, step 2: undo it
-- TODO: write your statement below and delete the placeholder
SELECT 'TODO' AS todo;

-- @Q A8e (given) After ROLLBACK the 12 defects are back
SELECT COUNT(*) AS defects_after_rollback FROM defects;
