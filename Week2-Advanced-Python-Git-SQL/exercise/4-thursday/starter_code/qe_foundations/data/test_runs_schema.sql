-- =============================================================================
-- test_runs_schema.sql  --  Project 1 (QE Foundations), Thursday milestone
-- Engine: SQLite (Python's built-in sqlite3 module).
--
-- One table = one kind of thing: a single execution ("run") of an automated test.
-- One row = one test run.  One column = one fact about that run.
--
-- PROVIDED FOR YOU: do not edit. (Friday adds constraints and more tables.)
-- Note how lenient the DDL is: only run_id and test_name are NOT NULL. Almost
-- everything else accepts NULL and ANY text -- which is exactly why the data
-- contains defects, and why your validation queries are needed.
-- =============================================================================
DROP TABLE IF EXISTS test_runs;

CREATE TABLE test_runs (
    run_id          INTEGER PRIMARY KEY,  -- unique id of the run
    test_name       TEXT NOT NULL,        -- e.g. test_login_valid_user
    suite           TEXT,                 -- SMOKE | REGRESSION | API
    environment     TEXT,                 -- DEV | QA | STAGING
    status          TEXT,                 -- PASSED | FAILED | SKIPPED | ERROR
    duration_ms     INTEGER,              -- how long the run took, in milliseconds
    retries         INTEGER,              -- automatic re-runs used (0..3)
    started_at      TEXT,                 -- 'YYYY-MM-DD HH:MM:SS' (SQLite has no DATE type)
    finished_at     TEXT,                 -- 'YYYY-MM-DD HH:MM:SS'
    executed_by     TEXT,                 -- e-mail address of the person/bot who ran it
    build_id        TEXT,                 -- 'B-' followed by 4 digits, e.g. B-1042
    failure_message TEXT                  -- why it failed / was skipped; NULL when none
);
