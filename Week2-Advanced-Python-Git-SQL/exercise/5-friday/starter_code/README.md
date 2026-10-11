# starter_code - 5-friday

Everything you need for Parts A-F. Read `../README.md` first.

| Path | What it is |
|---|---|
| `sql/schema.sql`, `sql/seed.sql` | the "Release Tracker" database and its dirty seed data (read-only: never edit) |
| `sql/part_a_dml.sql` .. `part_d_aggregates.sql` | task files for Parts A-D: replace each TODO placeholder |
| `sql/part_e_checks.sql` | the 20-check validation suite (17 to write, 3 worked examples) |
| `lab_runner.py` | runs a task file or the check suite against a fresh in-memory copy of the database |
| `data/` | the same rows as CSV/JSON for Part F, plus `data/clean/` (no defects) and `data/malformed/` (broken JSON) |
| `repo_overlay/` | skeleton files to copy into your qe-foundations repo for Part F |
| `EXPECTED_FINDINGS.md` | the findings template (copy it to `docs/DATA_QUALITY_FINDINGS.md` in your repo) |
| `check_exercise.py` | the self-check: `python check_exercise.py` (Parts A-E) and `--repo PATH` (adds Part F) |

Quick start (PowerShell and bash are identical here):

    python lab_runner.py sql/part_a_dml.sql
    python lab_runner.py sql/part_b_joins.sql --only B1
    python lab_runner.py --checks sql/part_e_checks.sql
    python check_exercise.py
