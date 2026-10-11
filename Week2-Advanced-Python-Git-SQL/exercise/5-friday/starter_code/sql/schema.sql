-- schema.sql : "Release Tracker" - four tables used in the Week 2 / 5-friday exercise.
-- Think of this as a LEGACY STAGING database: it declares keys, but it is deliberately loose
-- (no CHECK constraints, few NOT NULLs) so that dirty data can be loaded and then MEASURED with SQL.
-- Foreign keys are declared but SQLite does NOT enforce them until you run PRAGMA foreign_keys = ON.

CREATE TABLE builds (
    build_id        INTEGER PRIMARY KEY,
    build_name      TEXT NOT NULL,
    release         TEXT,
    built_date      TEXT,              -- ISO date 'YYYY-MM-DD'
    reported_total  INTEGER,           -- totals copied from the CI summary page
    reported_passed INTEGER,
    reported_failed INTEGER
);

CREATE TABLE test_cases (
    case_id      INTEGER PRIMARY KEY,
    title        TEXT NOT NULL,
    module       TEXT,                 -- login, cart, checkout, search, profile
    priority     TEXT,                 -- allowed: P1, P2, P3
    status       TEXT,                 -- allowed: active, retired
    created_date TEXT
);

CREATE TABLE test_runs (
    run_id       INTEGER PRIMARY KEY,
    build_id     INTEGER,
    case_id      INTEGER,
    tester       TEXT,
    run_date     TEXT,
    result       TEXT,                 -- allowed: pass, fail, skip
    duration_sec INTEGER,              -- allowed: 1 .. 3600
    FOREIGN KEY (build_id) REFERENCES builds(build_id),
    FOREIGN KEY (case_id)  REFERENCES test_cases(case_id)
);

CREATE TABLE defects (
    defect_id   INTEGER PRIMARY KEY,
    run_id      INTEGER,               -- NULL allowed: defect found outside a recorded run
    case_id     INTEGER,
    title       TEXT NOT NULL,
    severity    TEXT,                  -- allowed: low, medium, high, critical
    status      TEXT,                  -- allowed: open, fixed, closed
    opened_date TEXT,
    closed_date TEXT,
    FOREIGN KEY (run_id)  REFERENCES test_runs(run_id),
    FOREIGN KEY (case_id) REFERENCES test_cases(case_id)
);
