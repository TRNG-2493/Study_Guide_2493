"""Load the four Release Tracker data files into SQLite.   (Part F - Tuesday ingestion meets Friday SQL)

Files in data/:   builds.csv   test_cases.csv   test_runs.json   defects.json
(builds.csv was saved from Excel: it starts with a byte-order mark. Tuesday's "csv, json and xml" and "reading files" lessons cover that.)

THE CONTRACT (this is what check_exercise.py and your own tests will rely on)
  1. Only STRUCTURAL problems stop the load -> raise one of YOUR Tuesday custom exceptions:
       file missing, unsupported extension, unparsable JSON/CSV, missing column, id that is not an integer, duplicate primary key.
  2. DIRTY DATA is loaded as it is (orphan keys, NULLs, bad values, duplicates of non-key columns...).
     Finding it is the job of the SQL checks, not of the loader.
  3. CSV gives '' for an empty cell and JSON gives null: BOTH must become SQL NULL. Integer columns become int.
  4. Foreign keys stay OFF (do not run PRAGMA foreign_keys = ON here: it would reject the rows we want to measure).
  5. Calling load_all twice on the same connection must work (drop + create the tables first).
"""
import logging
from pathlib import Path

# TODO 1: import your Tuesday exceptions and loaders, for example
#   from qe_foundations.ingestion.exceptions import IngestionError, SourceNotFoundError, MalformedSourceError, ...
#   from qe_foundations.ingestion.readers import read_csv_records, read_json_records
# If a Tuesday exception does not exist yet (for example "duplicate id"), add it to your exceptions module.

log = logging.getLogger(__name__)

# table -> (file name, columns in table order, columns that must be integers)   [given]
SOURCES = {
    "builds": ("builds.csv",
               ["build_id", "build_name", "release", "built_date", "reported_total", "reported_passed", "reported_failed"],
               ["build_id", "reported_total", "reported_passed", "reported_failed"]),
    "test_cases": ("test_cases.csv",
                   ["case_id", "title", "module", "priority", "status", "created_date"],
                   ["case_id"]),
    "test_runs": ("test_runs.json",
                  ["run_id", "build_id", "case_id", "tester", "run_date", "result", "duration_sec"],
                  ["run_id", "build_id", "case_id", "duration_sec"]),
    "defects": ("defects.json",
                ["defect_id", "run_id", "case_id", "title", "severity", "status", "opened_date", "closed_date"],
                ["defect_id", "run_id", "case_id"]),
}
LOAD_ORDER = ["builds", "test_cases", "test_runs", "defects"]
PRIMARY_KEY = {"builds": "build_id", "test_cases": "case_id", "test_runs": "run_id", "defects": "defect_id"}


def convert_records(table, records):
    """Turn a list of raw records (dicts) into a list of tuples in table-column order.

    TODO 2: for every record
      - raise your MissingColumnsError if a required column is absent
      - '' or None -> None; integer columns -> int(...) (raise your invalid-value exception if that fails)
      - raise a record error if the primary key is empty and a duplicate-id error if it repeats
    Pure function (no database, no files): that makes it easy to unit test.
    """
    raise NotImplementedError("TODO 2: implement convert_records")


def create_schema(conn, schema_path):
    """TODO 3: DROP TABLE IF EXISTS for the four tables (children first), then conn.executescript(<schema.sql text>)."""
    raise NotImplementedError("TODO 3: implement create_schema")


def load_all(conn, data_dir, schema_path):
    """Create the tables and load all four files. Return {table: number_of_rows_loaded}.

    TODO 4: for each table in LOAD_ORDER: read the file (your Tuesday reader), convert_records, executemany INSERT
            with ? placeholders, commit, log.info how many rows were loaded. Let exceptions propagate (report.py handles them).
    """
    raise NotImplementedError("TODO 4: implement load_all")
