"""check_exercise.py - self-check for the Week 2 Day 2 exercise (Project 1 ingestion module).

Run it from the ROOT of your qe-foundations repo (the folder that contains `qe_foundations/`):

    Windows PowerShell :  python check_exercise.py
    macOS / Linux      :  python3 check_exercise.py

Or point it at a repo from anywhere:   python check_exercise.py --repo C:\\path\\to\\qe-foundations

Options:
    --repo PATH   folder containing qe_foundations/ingestion (default: current folder,
                  or the folder of this script)
    --stretch     also run the stretch-goal checks
    -v            show the full Python traceback for every failing check

What it does: it imports YOUR code and feeds it files that this script generates in a
temporary folder (including bad inputs that are NOT in data/ingestion/), then reports
PASS/FAIL per behaviour. It uses only the standard library. Your files are never modified.
It is a safety net, not the whole grade: the rubric in README.md also rewards design and Git.
"""

import argparse
import ast
import csv
import importlib
import math
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

sys.dont_write_bytecode = True  # do not litter your repo with __pycache__

PACKAGE = "qe_foundations.ingestion"
TASK_TITLES = {
    2: "Task 2 - exception hierarchy",
    3: "Task 3 - context managers",
    4: "Task 4 - readers (CSV / JSON / XML)",
    5: "Task 5 - validate_record",
    6: "Task 6 - loader, assertions, batch, rejected-records CSV",
    7: "Task 7 - code hygiene and notes",
    8: "Stretch goals",
}


class CheckFailure(Exception):
    """A check found wrong behaviour (message explains what was expected)."""


def expect(condition, message):
    if not condition:
        raise CheckFailure(message)


# --------------------------------------------------------------------------
# helpers: importing student code and building input files
# --------------------------------------------------------------------------
REPO = Path.cwd()


def mod(name):
    """Import qe_foundations.ingestion.<name> (or the package for name='')."""
    full = PACKAGE + ("." + name if name else "")
    try:
        return importlib.import_module(full)
    except ImportError as error:
        raise CheckFailure(f"cannot import {full}: {error}") from error


def need(module, attribute):
    try:
        return getattr(module, attribute)
    except AttributeError:
        raise CheckFailure(f"{module.__name__} has no name {attribute!r} (is the class/function written?)")


def raises(expected, func, *args, **kwargs):
    """Call func; return the exception if it is an instance of `expected`, else fail clearly."""
    try:
        func(*args, **kwargs)
    except NotImplementedError as error:
        raise CheckFailure(f"not implemented yet: {error}") from error
    except expected as error:
        return error
    except Exception as error:
        raise CheckFailure(
            f"expected {_names(expected)} but got {type(error).__name__}: {error}"
        ) from error
    raise CheckFailure(f"expected {_names(expected)} to be raised, but nothing was raised")


def _names(expected):
    if isinstance(expected, tuple):
        return " or ".join(e.__name__ for e in expected)
    return expected.__name__


def call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except NotImplementedError as error:
        raise CheckFailure(f"not implemented yet: {error}") from error
    except TypeError as error:
        raise CheckFailure(
            f"TypeError: {error} (does the signature/__init__ you wrote match the README? "
            "a class body that is still `pass` has the wrong constructor)"
        ) from error


TMP = None  # set in main()


def write_bytes(name, data):
    path = TMP / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def write_text(name, text):
    return write_bytes(name, text.encode("utf-8"))


# The SAME 9 logical records in three formats (cross-format consistency check).
#   row 1 TC-1 ok | 2 bad status | 3 blank title | 4 duplicate id | 5 nan duration
#   row 6 duration 0 ok | 7 "PASS" upper-case ok | 8 negative duration | 9 no id
EXPECT_VALID_IDS = ["TC-1", "TC-6", "TC-7"]
EXPECT_REJECTED_ROWS = [2, 3, 4, 5, 8, 9]

MESSY_CSV = (
    "id,title,status,duration\n"
    "TC-1,Login,pass,1.2\n"
    "TC-2,Logout,skipped,0.5\n"
    "TC-3,,pass,0.5\n"
    "TC-1,Again,pass,0.9\n"
    "TC-5,Search,pass,nan\n"
    "TC-6,Zero time,blocked,0\n"
    'TC-7,"Comma, and ""quotes""",PASS,2.5\n'
    "TC-8,Negative,fail,-1\n"
    ",No id,pass,1.0\n"
)
MESSY_JSON = """{"suite": "S", "tests": [
 {"id": "TC-1", "title": "Login", "status": "pass", "duration": 1.2},
 {"id": "TC-2", "title": "Logout", "status": "skipped", "duration": 0.5},
 {"id": "TC-3", "title": "", "status": "pass", "duration": 0.5},
 {"id": "TC-1", "title": "Again", "status": "pass", "duration": 0.9},
 {"id": "TC-5", "title": "Search", "status": "pass", "duration": "nan"},
 {"id": "TC-6", "title": "Zero time", "status": "blocked", "duration": 0},
 {"id": "TC-7", "title": "Comma, and quotes", "status": "PASS", "duration": 2.5},
 {"id": "TC-8", "title": "Negative", "status": "fail", "duration": -1},
 {"title": "No id", "status": "pass", "duration": 1.0}
]}"""
MESSY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites><testsuite name="A">
 <testcase id="TC-1" status="pass"><title>Login</title><duration>1.2</duration></testcase>
 <testcase id="TC-2" status="skipped"><title>Logout</title><duration>0.5</duration></testcase>
 <testcase id="TC-3" status="pass"><title></title><duration>0.5</duration></testcase>
</testsuite><testsuite name="B">
 <testcase id="TC-1" status="pass"><title>Again</title><duration>0.9</duration></testcase>
 <testcase id="TC-5" status="pass"><title>Search</title><duration>nan</duration></testcase>
 <testcase id="TC-6" status="blocked"><title>Zero time</title><duration>0</duration></testcase>
 <testcase id="TC-7" status="PASS"><title>Comma, and quotes</title><duration>2.5</duration></testcase>
 <testcase id="TC-8" status="fail"><title>Negative</title><duration>-1</duration></testcase>
 <testcase status="pass"><title>No id</title><duration>1.0</duration></testcase>
</testsuite></testsuites>"""


def messy_files():
    return {
        "csv": write_text("messy.csv", MESSY_CSV),
        "json": write_text("messy.json", MESSY_JSON),
        "xml": write_text("messy.xml", MESSY_XML),
    }


# --------------------------------------------------------------------------
# TASK 2 - exceptions
# --------------------------------------------------------------------------
def c_hierarchy():
    m = mod("exceptions")
    base = need(m, "IngestionError")
    source = need(m, "SourceError")
    record = need(m, "RecordValidationError")
    expect(issubclass(base, Exception), "IngestionError must derive from Exception")
    for name in ("SourceNotFoundError", "SourceUnreadableError", "UnsupportedFormatError",
                 "MalformedSourceError", "MissingColumnsError"):
        cls = need(m, name)
        expect(issubclass(cls, source), f"{name} must be a subclass of SourceError")
    for name in ("MissingFieldError", "InvalidValueError", "DuplicateIdError"):
        cls = need(m, name)
        expect(issubclass(cls, record), f"{name} must be a subclass of RecordValidationError")
    expect(issubclass(source, base) and issubclass(record, base),
           "SourceError and RecordValidationError must both derive from IngestionError")
    expect(not issubclass(source, record) and not issubclass(record, source),
           "SourceError and RecordValidationError must be SIBLINGS (neither derives from the other), "
           "otherwise `except RecordValidationError` would also catch file-level problems")


def c_source_attributes():
    m = mod("exceptions")
    e = call(need(m, "UnsupportedFormatError"), "data/notes.txt", ".txt")
    expect(getattr(e, "suffix", None) == ".txt", "UnsupportedFormatError must store .suffix")
    expect(e.path.endswith("notes.txt"), "SourceError subclasses must keep .path")
    expect("notes.txt" in str(e), "the message should contain the file name")
    e = call(need(m, "MissingColumnsError"), "x.csv", ["duration", "title"])
    expect(e.missing == ["duration", "title"], "MissingColumnsError must store .missing as a list")
    expect("duration" in str(e), "message should list the missing columns")
    e = call(need(m, "SourceUnreadableError"), "folder.csv", PermissionError("denied"))
    expect("PermissionError" in str(e), "SourceUnreadableError message should name the OS error class")
    e = call(need(m, "MalformedSourceError"), "bad.json", "invalid JSON at line 3")
    expect("bad.json" in str(e) and "line 3" in str(e), "MalformedSourceError message must contain file name and detail")


def c_record_attributes():
    m = mod("exceptions")
    e = call(need(m, "MissingFieldError"), 3, "title")
    expect(e.row == 3 and e.field == "title", "MissingFieldError must set .row and .field")
    expect("Row 3" in str(e) and "title" in str(e), "message should contain 'Row 3' and the field name")
    e = call(need(m, "InvalidValueError"), 4, "status", "passed", "one of pass/fail")
    expect(e.row == 4 and e.field == "status", "InvalidValueError must set .row and .field")
    expect(e.value == "passed" and e.expected == "one of pass/fail",
           "InvalidValueError must store .value and .expected")
    expect("passed" in str(e), "message should show the offending value")
    e = call(need(m, "DuplicateIdError"), 5, "TC-1")
    expect(e.row == 5 and e.field == "id" and e.test_id == "TC-1",
           "DuplicateIdError must set .row, .field == 'id' and .test_id")


def c_catch_all():
    m = mod("exceptions")
    samples = [
        call(need(m, "SourceNotFoundError"), "a.csv"),
        call(need(m, "MissingFieldError"), 1, "id"),
        call(need(m, "DuplicateIdError"), 2, "X"),
        call(need(m, "UnsupportedFormatError"), "a.txt", ".txt"),
    ]
    for exc in samples:
        try:
            raise exc
        except need(m, "IngestionError"):
            pass


# --------------------------------------------------------------------------
# TASK 3 - context managers
# --------------------------------------------------------------------------
def c_open_basic():
    m = mod("contexts")
    path = write_bytes("bom.txt", b"\xef\xbb\xbfhello\r\nworld\r\n")
    with call(need(m, "open_source"), path) as handle:
        text = handle.read()
    expect(text.startswith("hello"), "BOM must be stripped (encoding='utf-8-sig')")
    expect(handle.closed, "file must be closed after the with block")
    expect("\r\n" in text, "open with newline='' so line endings are not translated")


def c_open_closes_on_error():
    m = mod("contexts")
    path = write_text("plain.txt", "data")
    holder = {}
    try:
        with call(need(m, "open_source"), path) as handle:
            holder["h"] = handle
            raise KeyError("boom")
    except KeyError:
        pass
    else:
        raise CheckFailure("an exception raised inside the with-body must NOT be swallowed")
    expect(holder["h"].closed, "file must be closed even when the with-body raises")


def c_open_missing():
    m = mod("contexts")
    exc_mod = mod("exceptions")

    def go():
        with need(m, "open_source")(TMP / "nope.csv"):
            pass

    e = raises(need(exc_mod, "SourceNotFoundError"), go)
    expect(isinstance(e.__cause__, FileNotFoundError),
           "use `raise ... from error` so __cause__ is the original FileNotFoundError")


def c_open_directory():
    m = mod("contexts")
    exc_mod = mod("exceptions")
    (TMP / "folder.csv").mkdir(exist_ok=True)

    def go():
        with need(m, "open_source")(TMP / "folder.csv"):
            pass

    e = raises(need(exc_mod, "SourceUnreadableError"), go)
    expect(isinstance(e.__cause__, OSError), "keep the original OSError as __cause__ (raise ... from error)")
    expect(not isinstance(e, need(exc_mod, "SourceNotFoundError")),
           "a folder is not 'file not found': catch FileNotFoundError BEFORE the general OSError")


def c_open_bad_encoding():
    m = mod("contexts")
    exc_mod = mod("exceptions")
    path = write_bytes("latin.txt", "caf\u00e9\n".encode("latin-1"))

    def go():
        with need(m, "open_source")(path) as handle:
            handle.read()

    e = raises(need(exc_mod, "MalformedSourceError"), go)
    expect(isinstance(e.__cause__, UnicodeDecodeError), "keep the UnicodeDecodeError as __cause__")


def c_session_ok():
    m = mod("contexts")
    session = call(need(m, "LoadSession"), "x.csv")
    expect(session.outcome is None, "outcome starts as None")
    with session as inside:
        expect(inside is session, "__enter__ must return the session itself (return self)")
    expect(session.outcome == "completed", f"outcome after a normal block must be 'completed', got {session.outcome!r}")
    expect(isinstance(session.elapsed, float) and session.elapsed >= 0,
           "elapsed must be a float >= 0 (use time.perf_counter())")


def c_session_failed():
    m = mod("contexts")
    session = call(need(m, "LoadSession"), "x.csv")
    try:
        with session:
            raise ValueError("boom")
    except ValueError:
        pass
    else:
        raise CheckFailure("LoadSession must not swallow exceptions (__exit__ must return False/None)")
    expect(session.outcome == "failed", f"outcome after an exception must be 'failed', got {session.outcome!r}")
    expect(isinstance(session.elapsed, float), "elapsed must be recorded even when the block fails")


# --------------------------------------------------------------------------
# TASK 4 - readers
# --------------------------------------------------------------------------
def c_csv_basic():
    m = mod("readers")
    path = write_bytes(
        "r1.csv",
        b'\xef\xbb\xbfid,title,status,duration\r\nT1,"Search, exact",pass,1.5\r\nT2,"Say ""hi""",fail,0.2\r\n\r\n',
    )
    rows = call(need(m, "read_csv_records"), path)
    expect(isinstance(rows, list) and len(rows) == 2, f"expected 2 records, got {rows!r}")
    expect(rows[0].get("id") == "T1", "first column must be named 'id' (is the BOM stripped?)")
    expect(rows[0]["title"] == "Search, exact" and rows[1]["title"] == 'Say "hi"',
           "quoted commas/quotes must be parsed by the csv module, not str.split")
    expect(rows[0]["duration"] == "1.5", "readers return RAW strings; do not convert types in the reader")


def c_csv_missing_cols():
    m = mod("readers")
    exc_mod = mod("exceptions")
    path = write_text("r2.csv", "id,status\nT1,pass\n")
    e = raises(need(exc_mod, "MissingColumnsError"), need(m, "read_csv_records"), path)
    expect(e.missing == ["title", "duration"], f"missing must list absent columns in REQUIRED order, got {e.missing!r}")


def c_csv_empty_and_header_only():
    m = mod("readers")
    exc_mod = mod("exceptions")
    e = raises(need(exc_mod, "MissingColumnsError"), need(m, "read_csv_records"), write_bytes("empty.csv", b""))
    expect(len(e.missing) == 4, "an EMPTY file has no header: all four columns are missing")
    rows = call(need(m, "read_csv_records"), write_text("hdr.csv", "id,title,status,duration\n"))
    expect(rows == [], "a header-only CSV is valid and has zero records")


def c_csv_short_row_survives():
    m = mod("readers")
    path = write_text("short.csv", "id,title,status,duration\nT1,Only three,pass\nT2,Fine,pass,1\n")
    rows = call(need(m, "read_csv_records"), path)
    expect(len(rows) == 2, "a short row must still be returned (validation, not the reader, rejects it)")


def c_json_ok_and_oddities():
    m = mod("readers")
    path = write_text("r.json", '{"tests": [{"id": 1}, "just a string", 7]}')
    rows = call(need(m, "read_json_records"), path)
    expect(rows == [{"id": 1}, "just a string", 7],
           "return the 'tests' list untouched (even non-dict items; validation rejects them later)")


def c_json_malformed():
    m = mod("readers")
    exc_mod = mod("exceptions")
    e = raises(need(exc_mod, "MalformedSourceError"), need(m, "read_json_records"),
               write_text("m.json", '{"tests": [\n{"id": 1},\n]}'))
    expect(isinstance(e.__cause__, ValueError), "keep the JSONDecodeError as __cause__ (raise ... from error)")
    expect("line" in str(e).lower(), "message should tell WHERE the JSON is broken (line number)")
    raises(need(exc_mod, "MalformedSourceError"), need(m, "read_json_records"), write_bytes("e.json", b""))


def c_json_wrong_shape():
    m = mod("readers")
    exc_mod = mod("exceptions")
    for name, text in (("s1.json", "[1, 2]"), ("s2.json", '{"tests": "nope"}'), ("s3.json", '{"suite": "x"}'), ("s4.json", "42")):
        raises(need(exc_mod, "MalformedSourceError"), need(m, "read_json_records"), write_text(name, text))


def c_xml_basic():
    m = mod("readers")
    path = write_text(
        "r.xml",
        '<testsuites><testsuite><testcase id="A" status="pass"><title>One</title><duration>1.5</duration></testcase>'
        '</testsuite><testsuite><testcase status="fail"><title>Two</title></testcase></testsuite></testsuites>',
    )
    rows = call(need(m, "read_xml_records"), path)
    expect(len(rows) == 2, f"find <testcase> elements at ANY depth (got {len(rows)} records, expected 2)")
    expect(rows[0] == {"id": "A", "status": "pass", "title": "One", "duration": "1.5"},
           f"record 1 should be raw strings from attributes/children, got {rows[0]!r}")
    expect(rows[1]["id"] is None and rows[1]["duration"] is None,
           "an absent attribute/child must become None (not crash, not '')")


def c_xml_malformed():
    m = mod("readers")
    exc_mod = mod("exceptions")
    e = raises(need(exc_mod, "MalformedSourceError"), need(m, "read_xml_records"),
               write_text("m.xml", "<testsuite><testcase id='1'></testsuite>"))
    expect(isinstance(e.__cause__, Exception), "keep the ParseError as __cause__ (raise ... from error)")
    raises(need(exc_mod, "MalformedSourceError"), need(m, "read_xml_records"), write_bytes("e.xml", b""))


def c_readers_encoding():
    m = mod("readers")
    exc_mod = mod("exceptions")
    bad = "id,title,status,duration\nT1,caf\u00e9,pass,1\n".encode("latin-1")
    raises(need(exc_mod, "MalformedSourceError"), need(m, "read_csv_records"), write_bytes("l.csv", bad))
    raises(need(exc_mod, "MalformedSourceError"), need(m, "read_json_records"),
           write_bytes("l.json", b'{"tests": [{"title": "caf\xe9"}]}'))


def c_readers_missing_file():
    m = mod("readers")
    exc_mod = mod("exceptions")
    for reader, ext in (("read_csv_records", "csv"), ("read_json_records", "json"), ("read_xml_records", "xml")):
        raises(need(exc_mod, "SourceNotFoundError"), need(m, reader), TMP / f"absent.{ext}")


# --------------------------------------------------------------------------
# TASK 5 - validate_record
# --------------------------------------------------------------------------
def good(**changes):
    record = {"id": "TC-1", "title": "Login", "status": "pass", "duration": 1.5}
    record.update(changes)
    return record


def c_val_clean():
    v = need(mod("validation"), "validate_record")
    result = call(v, 1, {"id": " tc-1 ", "title": "  Login  ", "status": " PASS ", "duration": "1.5"})
    expect(result == {"id": "tc-1", "title": "Login", "status": "pass", "duration": 1.5},
           f"expected trimmed id/title, lower-case status, float duration; got {result!r}")
    expect(isinstance(result["duration"], float), "duration must be a float")
    expect(call(v, 1, good(id=42))["id"] == "42", "a numeric id must become the string '42'")
    for ok in (0, "0", "0.0", "1e2", " 2.5 ", 3):
        call(v, 1, good(duration=ok))
    expect(call(v, 1, good(duration="1e2"))["duration"] == 100.0, "'1e2' is a valid number (100.0)")
    for status in ("pass", "FAIL", "Blocked"):
        call(v, 1, good(status=status))


def c_val_does_not_mutate():
    v = need(mod("validation"), "validate_record")
    raw = {"id": " a ", "title": " b ", "status": "PASS", "duration": "2"}
    snapshot = dict(raw)
    call(v, 1, raw)
    expect(raw == snapshot, "validate_record must not modify the raw record it was given")


def c_val_missing():
    exc_mod = mod("exceptions")
    v = need(mod("validation"), "validate_record")
    MFE = need(exc_mod, "MissingFieldError")
    for field in ("id", "title", "status", "duration"):
        for bad in (None, "", "   "):
            e = raises(MFE, v, 7, good(**{field: bad}))
            expect(e.row == 7 and e.field == field, f"for {field}={bad!r}: expected row 7, field {field!r}; got row {e.row}, field {e.field!r}")
        broken = good()
        del broken[field]
        e = raises(MFE, v, 2, broken)
        expect(e.field == field, f"absent key {field!r}: wrong .field {e.field!r}")


def c_val_status():
    exc_mod = mod("exceptions")
    v = need(mod("validation"), "validate_record")
    IVE = need(exc_mod, "InvalidValueError")
    for bad in ("passed", "skipped", "unknown", "p", True, 1):
        e = raises(IVE, v, 3, good(status=bad))
        expect(e.field == "status" and e.row == 3, f"status={bad!r}: wrong row/field ({e.row}, {e.field!r})")


def c_val_duration():
    exc_mod = mod("exceptions")
    v = need(mod("validation"), "validate_record")
    IVE = need(exc_mod, "InvalidValueError")
    for bad in ("fast", "n/a", "-4", -0.1, "nan", float("nan"), "inf", "-inf", float("inf"), True, False, [], {}, "1,5", "1.2.3"):
        e = raises(IVE, v, 5, good(duration=bad))
        expect(e.field == "duration", f"duration={bad!r}: expected field 'duration', got {e.field!r}")
    expect(math.isfinite(call(v, 1, good(duration="0"))["duration"]), "'0' must be accepted")


def c_val_not_a_dict():
    exc_mod = mod("exceptions")
    v = need(mod("validation"), "validate_record")
    RVE = need(exc_mod, "RecordValidationError")
    for bad in ("TC-1", 42, None, ["a", "b"], 3.5):
        e = raises(RVE, v, 9, bad)
        expect(e.row == 9, "row number must be reported")
        expect(e.field == "record", f"for a non-dict record use field 'record', got {e.field!r}")


def c_val_order():
    exc_mod = mod("exceptions")
    v = need(mod("validation"), "validate_record")
    raises(need(exc_mod, "MissingFieldError"), v, 1, good(title="", status="bogus", duration="x"))
    e = raises(need(exc_mod, "InvalidValueError"), v, 1, good(status="bogus", duration="x"))
    expect(e.field == "status", "when status AND duration are bad, report status first")
    e = raises(need(exc_mod, "MissingFieldError"), v, 1, {"id": "", "title": "", "status": "", "duration": ""})
    expect(e.field == "id", "required fields are checked in the order id, title, status, duration")


def c_val_python_O():
    code = (
        "import sys; sys.dont_write_bytecode = True\n"
        "from qe_foundations.ingestion.validation import validate_record\n"
        "from qe_foundations.ingestion.exceptions import RecordValidationError\n"
        "try:\n"
        "    validate_record(1, {'id':'a','title':'b','status':'bogus','duration':1})\n"
        "    print('NO-ERROR')\n"
        "except RecordValidationError:\n"
        "    print('REJECTED')\n"
        "except BaseException as e:\n"
        "    print('OTHER', type(e).__name__)\n"
    )
    env = dict(os.environ, PYTHONPATH=str(REPO) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    out = subprocess.run([sys.executable, "-O", "-c", code], capture_output=True, text=True, env=env, cwd=str(TMP), timeout=60)
    first = (out.stdout.strip().splitlines() or ["(no output) " + out.stderr.strip()[-200:]])[0]
    if first == "OTHER NotImplementedError":
        raise CheckFailure("not implemented yet: Task 5: write validate_record")
    expect(first == "REJECTED",
           f"under `python -O` validation must still reject bad data (got: {first}). Do you validate with assert?")


# --------------------------------------------------------------------------
# TASK 6 - loader
# --------------------------------------------------------------------------
def _check_messy(report, label):
    ids = [r["id"] for r in report.valid]
    expect(report.rows_seen == 9, f"{label}: rows_seen should be 9, got {report.rows_seen}")
    expect(ids == EXPECT_VALID_IDS, f"{label}: valid ids should be {EXPECT_VALID_IDS}, got {ids}")
    rows = sorted(e.row for e in report.rejected)
    expect(rows == EXPECT_REJECTED_ROWS, f"{label}: rejected rows should be {EXPECT_REJECTED_ROWS}, got {rows}")


def c_load_messy_csv():
    _check_messy(call(need(mod("loader"), "load_test_cases"), messy_files()["csv"]), "CSV")


def c_load_messy_json():
    _check_messy(call(need(mod("loader"), "load_test_cases"), messy_files()["json"]), "JSON")


def c_load_messy_xml():
    _check_messy(call(need(mod("loader"), "load_test_cases"), messy_files()["xml"]), "XML")


def c_load_error_types():
    exc_mod = mod("exceptions")
    load = need(mod("loader"), "load_test_cases")
    report = call(load, messy_files()["csv"])
    kinds = {e.row: type(e).__name__ for e in report.rejected}
    expected = {2: "InvalidValueError", 3: "MissingFieldError", 4: "DuplicateIdError",
                5: "InvalidValueError", 8: "InvalidValueError", 9: "MissingFieldError"}
    expect(kinds == expected, f"error classes per row should be {expected}, got {kinds}")
    expect(report.valid[-1]["title"] == 'Comma, and "quotes"', "quoted CSV field must survive intact")
    expect(isinstance(report.valid[0]["duration"], float), "valid records hold float durations")
    expect(report.source == "messy.csv", f"report.source should be the file NAME, got {report.source!r}")


def c_load_source_errors():
    exc_mod = mod("exceptions")
    load = need(mod("loader"), "load_test_cases")
    e = raises(need(exc_mod, "UnsupportedFormatError"), load, write_text("notes.txt", "hello"))
    expect(e.suffix == ".txt", "UnsupportedFormatError.suffix should be '.txt'")
    raises(need(exc_mod, "SourceNotFoundError"), load, TMP / "missing.json")
    raises(need(exc_mod, "MissingColumnsError"), load, write_text("nocols.csv", "id,title\nT1,x\n"))
    raises(need(exc_mod, "MalformedSourceError"), load, write_text("broken.json", "{oops"))
    raises(need(exc_mod, "MalformedSourceError"), load, write_text("broken.xml", "<a><b></a>"))
    (TMP / "dir.csv").mkdir(exist_ok=True)
    raises(need(exc_mod, "SourceUnreadableError"), load, TMP / "dir.csv")
    # upper-case extensions must work
    report = call(load, write_text("UPPER.CSV", "id,title,status,duration\nT1,x,pass,1\n"))
    expect(len(report.valid) == 1, "extension matching must be case-insensitive (.CSV)")


def c_load_accepts_str_and_path():
    load = need(mod("loader"), "load_test_cases")
    p = write_text("sp.csv", "id,title,status,duration\nT1,x,pass,1\n")
    a, b = call(load, p), call(load, str(p))
    expect(len(a.valid) == len(b.valid) == 1, "both str and pathlib.Path arguments must work")


def c_report_summary_and_rows():
    load = need(mod("loader"), "load_test_cases")
    report = call(load, messy_files()["csv"])
    expect(report.summary() == "messy.csv: 9 rows seen, 3 valid, 6 rejected",
           f"summary() must be exactly 'messy.csv: 9 rows seen, 3 valid, 6 rejected', got {report.summary()!r}")
    rows = report.rejected_rows()
    expect([r["row"] for r in rows] == EXPECT_REJECTED_ROWS, "rejected_rows() must be ordered by row number")
    expect(set(rows[0]) == {"source", "row", "field", "reason"}, f"rejected_rows() keys must be source,row,field,reason; got {sorted(rows[0])}")
    expect(rows[0]["source"] == "messy.csv" and rows[0]["field"] == "status" and "skipped" in rows[0]["reason"],
           f"first rejected row looks wrong: {rows[0]!r}")


def c_invariants():
    if sys.flags.optimize:
        raise CheckFailure("run this check without -O (assertions are disabled under -O)")
    cls = need(mod("loader"), "IngestionReport")
    exc_mod = mod("exceptions")
    ok = cls("ok.csv", rows_seen=2)
    ok.valid.append({"id": "A"})
    ok.rejected.append(call(need(exc_mod, "MissingFieldError"), 2, "title"))
    call(ok.check_invariants)  # consistent report: must not raise

    bad_count = cls("bad.csv", rows_seen=5)
    bad_count.valid.append({"id": "A"})
    e = raises(AssertionError, bad_count.check_invariants)
    expect(str(e).strip() != "", "give each assert a helpful message")

    dup = cls("dup.csv", rows_seen=2)
    dup.valid.extend([{"id": "A"}, {"id": "A"}])
    raises(AssertionError, dup.check_invariants)

    wrong_kind = cls("wk.csv", rows_seen=1)
    wrong_kind.rejected.append(ValueError("not a record error"))
    raises(AssertionError, wrong_kind.check_invariants)


def c_batch():
    exc_mod = mod("exceptions")
    m = mod("loader")
    folder = TMP / "batch"
    folder.mkdir(exist_ok=True)
    (folder / "sub").mkdir(exist_ok=True)
    write_text("batch/a_good.csv", "id,title,status,duration\nT1,x,pass,1\nT2,y,fail,2\n")
    write_text("batch/b_bad.json", "{not json")
    write_text("batch/c_messy.csv", MESSY_CSV)
    write_text("batch/d_notes.txt", "hello")
    write_text("batch/sub/ignored.csv", "id,title,status,duration\nT9,z,pass,1\n")
    result = call(need(m, "load_directory"), folder)
    names = [r.source for r in result.reports]
    expect(names == ["a_good.csv", "c_messy.csv"], f"reports should be ['a_good.csv', 'c_messy.csv'] (sorted, sub-folders skipped), got {names}")
    failed = sorted(type(e).__name__ for e in result.failed_sources)
    expect(failed == ["MalformedSourceError", "UnsupportedFormatError"],
           f"failed_sources should hold the two unusable files, got {failed}")
    expect(all(isinstance(e, need(exc_mod, "SourceError")) for e in result.failed_sources), "failed_sources must hold SourceError objects")
    totals = call(result.totals)
    expect(totals == {"files_ok": 2, "files_failed": 2, "valid": 5, "rejected": 6}, f"totals() wrong: {totals}")
    raises(need(exc_mod, "SourceNotFoundError"), need(m, "load_directory"), TMP / "no_such_folder")
    empty = TMP / "empty_folder"
    empty.mkdir(exist_ok=True)
    expect(call(need(m, "load_directory"), empty).totals() == {"files_ok": 0, "files_failed": 0, "valid": 0, "rejected": 0},
           "an empty folder gives all-zero totals")


def c_write_rejected():
    m = mod("loader")
    report = call(need(m, "load_test_cases"), messy_files()["csv"])
    out = TMP / "reports" / "nested" / "rejected.csv"
    result = call(need(m, "write_rejected_csv"), report, out)
    expect(Path(result) == out and out.exists(), "write_rejected_csv must create parent folders and return the path")
    raw = out.read_bytes()
    expect(b"\r\r\n" not in raw, "blank lines between rows: open the file with newline=''")
    expect(raw.startswith(b"source,row,field,reason"), "header must be exactly: source,row,field,reason")
    with open(out, encoding="utf-8", newline="") as handle:
        back = list(csv.DictReader(handle))
    expect(len(back) == 6, f"expected 6 data rows, got {len(back)}")
    expect([int(r["row"]) for r in back] == EXPECT_REJECTED_ROWS, "rows must be in row order")
    expect(back[0]["reason"] == report.rejected_rows()[0]["reason"], "reason text must round-trip (quotes/commas handled by csv module)")
    clean = call(need(m, "load_test_cases"), write_text("clean.csv", "id,title,status,duration\nT1,x,pass,1\n"))
    out2 = call(need(m, "write_rejected_csv"), clean, TMP / "reports" / "none.csv")
    expect(Path(out2).read_text(encoding="utf-8").strip() == "source,row,field,reason", "no rejected records -> header only")


def c_cli():
    good_file = write_text("cli_ok.csv", "id,title,status,duration\nT1,x,pass,1\nT2,y,nope,1\n")
    env = dict(os.environ, PYTHONPATH=str(REPO) + os.pathsep + os.environ.get("PYTHONPATH", ""))
    run = lambda *a: subprocess.run([sys.executable, "-B", "-m", PACKAGE, *a], capture_output=True, text=True, env=env, cwd=str(TMP), timeout=60)
    out = run(str(good_file))
    expect(out.returncode == 0, f"CLI exit code should be 0 for a readable file; got {out.returncode}. stderr: {out.stderr.strip()[-300:]}")
    expect("2 rows seen, 1 valid, 1 rejected" in out.stdout, f"CLI should print the summary line; got: {out.stdout.strip()[:200]!r}")
    out = run(str(TMP / "nothing.csv"))
    expect(out.returncode == 1 and "SOURCE FAILED" in out.stdout, "CLI must report an unusable source and exit with code 1")


# --------------------------------------------------------------------------
# TASK 7 - hygiene and notes
# --------------------------------------------------------------------------
def package_files():
    folder = REPO / "qe_foundations" / "ingestion"
    return sorted(p for p in folder.glob("*.py"))


def no_stubs_left():
    """Hygiene checks are meaningless on untouched starter code: require real code first."""
    left = []
    for path in package_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Raise) and node.exc is not None:
                target = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
                if isinstance(target, ast.Name) and target.id == "NotImplementedError":
                    left.append(f"{path.name}:{node.lineno}")
    expect(not left, "unfinished: `raise NotImplementedError` still present at " + ", ".join(left))


def c_no_bare_except():
    no_stubs_left()
    problems = []
    for path in package_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    problems.append(f"{path.name}:{node.lineno} bare `except:`")
                elif isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException"):
                    reraises = any(isinstance(n, ast.Raise) for n in ast.walk(node))
                    if not reraises:
                        problems.append(f"{path.name}:{node.lineno} `except {node.type.id}` that never re-raises")
    expect(not problems, "too-broad except clauses: " + "; ".join(problems))


def c_no_assert_in_validation():
    no_stubs_left()
    path = REPO / "qe_foundations" / "ingestion" / "validation.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    lines = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    expect(not lines, f"validation.py uses `assert` on line(s) {lines}: external data must be checked with exceptions")


def c_asserts_exist_in_loader():
    no_stubs_left()
    path = REPO / "qe_foundations" / "ingestion" / "loader.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    count = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
    expect(count >= 3, f"loader.py should contain at least 3 assert statements (the 3 invariants); found {count}")


def c_no_logging_or_prints():
    no_stubs_left()
    problems = []
    for path in package_files():
        if path.name == "__main__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                problems.append(f"{path.name}:{node.lineno}")
    expect(not problems, "library modules should return data / raise, not print (printing belongs in __main__.py): " + ", ".join(problems))


def c_with_used():
    no_stubs_left()
    problems = []
    for name in ("readers.py", "loader.py"):
        text = (REPO / "qe_foundations" / "ingestion" / name).read_text(encoding="utf-8")
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                # open() is allowed only as a with-item
                parent_with = any(isinstance(w, ast.With) and any(item.context_expr is node for item in w.items) for w in ast.walk(tree))
                if not parent_with:
                    problems.append(f"{name}:{node.lineno} open() outside a `with`")
    expect(not problems, "; ".join(problems))


def c_notes():
    path = REPO / "docs" / "ingestion_notes.md"
    expect(path.exists(), "docs/ingestion_notes.md not found (copy it from starter_code/docs/ and answer the 4 questions)")
    text = path.read_text(encoding="utf-8")
    expect("TODO: your answer" not in text and "TODO:" not in text, "docs/ingestion_notes.md still contains TODO placeholders")
    expect(len(text.split()) >= 120, "docs/ingestion_notes.md looks too short (aim for 2-4 sentences per question)")


# --------------------------------------------------------------------------
# STRETCH
# --------------------------------------------------------------------------
def c_s_strict():
    exc_mod = mod("exceptions")
    load = need(mod("loader"), "load_test_cases")
    e = raises(need(exc_mod, "RecordValidationError"), load, messy_files()["csv"], strict=True)
    expect(e.row == 2, f"strict=True must raise the FIRST problem (row 2), got row {e.row}")
    report = call(load, messy_files()["csv"], strict=False)
    expect(len(report.rejected) == 6, "strict=False keeps the default behaviour")
    call(load, write_text("strict_ok.csv", "id,title,status,duration\nT1,x,pass,1\n"), strict=True)


def c_s_max_errors():
    exc_mod = mod("exceptions")
    load = need(mod("loader"), "load_test_cases")
    tme = need(exc_mod, "TooManyErrorsError")
    expect(issubclass(tme, need(exc_mod, "IngestionError")), "TooManyErrorsError must derive from IngestionError")
    e = raises(tme, load, messy_files()["csv"], max_errors=2)
    expect(e.limit == 2 and e.count >= 3, f"store .limit and .count (rejected so far, > limit); got limit={getattr(e, 'limit', None)}, count={getattr(e, 'count', None)}")
    expect(len(call(load, messy_files()["csv"], max_errors=6).rejected) == 6, "exactly max_errors rejected records is allowed (raise only when EXCEEDED)")
    expect(len(call(load, messy_files()["csv"], max_errors=None).rejected) == 6, "max_errors=None means unlimited")


# --------------------------------------------------------------------------
# runner
# --------------------------------------------------------------------------
CHECKS = [
    (2, "hierarchy: parents and siblings", c_hierarchy),
    (2, "source errors carry path/suffix/missing + readable message", c_source_attributes),
    (2, "record errors carry row/field/value/test_id", c_record_attributes),
    (2, "every exception is caught by `except IngestionError`", c_catch_all),
    (3, "open_source: reads UTF-8, strips BOM, closes file", c_open_basic),
    (3, "open_source: closes the file and re-raises when the body fails", c_open_closes_on_error),
    (3, "open_source: missing file -> SourceNotFoundError (from FileNotFoundError)", c_open_missing),
    (3, "open_source: a folder -> SourceUnreadableError (not 'not found')", c_open_directory),
    (3, "open_source: bad encoding -> MalformedSourceError", c_open_bad_encoding),
    (3, "LoadSession: outcome 'completed' + elapsed", c_session_ok),
    (3, "LoadSession: outcome 'failed', exception NOT swallowed", c_session_failed),
    (4, "CSV reader: BOM, quotes, CRLF, blank line, raw strings", c_csv_basic),
    (4, "CSV reader: missing columns reported in required order", c_csv_missing_cols),
    (4, "CSV reader: empty file / header-only file", c_csv_empty_and_header_only),
    (4, "CSV reader: short rows survive for validation", c_csv_short_row_survives),
    (4, "JSON reader: returns the tests list untouched", c_json_ok_and_oddities),
    (4, "JSON reader: malformed JSON (with line number) and empty file", c_json_malformed),
    (4, "JSON reader: wrong shapes -> MalformedSourceError", c_json_wrong_shape),
    (4, "XML reader: any depth, attributes + children, None when absent", c_xml_basic),
    (4, "XML reader: malformed and empty files", c_xml_malformed),
    (4, "CSV/JSON readers: non-UTF-8 bytes -> MalformedSourceError", c_readers_encoding),
    (4, "all readers: missing file -> SourceNotFoundError", c_readers_missing_file),
    (5, "validate_record: clean + normalised output", c_val_clean),
    (5, "validate_record: does not mutate its input", c_val_does_not_mutate),
    (5, "validate_record: missing / None / blank fields", c_val_missing),
    (5, "validate_record: invalid status values", c_val_status),
    (5, "validate_record: invalid durations (nan, inf, bool, negative, text)", c_val_duration),
    (5, "validate_record: a record that is not a dict", c_val_not_a_dict),
    (5, "validate_record: which problem is reported first", c_val_order),
    (5, "validate_record: still rejects under `python -O`", c_val_python_O),
    (6, "load_test_cases: messy CSV", c_load_messy_csv),
    (6, "load_test_cases: messy JSON (same data as CSV)", c_load_messy_json),
    (6, "load_test_cases: messy XML (same data as CSV)", c_load_messy_xml),
    (6, "load_test_cases: right exception class per rejected row", c_load_error_types),
    (6, "load_test_cases: unusable files raise the right SourceError", c_load_source_errors),
    (6, "load_test_cases: accepts str and Path", c_load_accepts_str_and_path),
    (6, "IngestionReport: summary() and rejected_rows()", c_report_summary_and_rows),
    (6, "check_invariants: three assertions fire on inconsistent reports", c_invariants),
    (6, "load_directory + BatchResult.totals", c_batch),
    (6, "write_rejected_csv", c_write_rejected),
    (6, "command line: python -m qe_foundations.ingestion", c_cli),
    (7, "no bare / swallowing `except Exception`", c_no_bare_except),
    (7, "no `assert` in validation.py", c_no_assert_in_validation),
    (7, "at least 3 asserts in loader.py", c_asserts_exist_in_loader),
    (7, "library modules do not print()", c_no_logging_or_prints),
    (7, "open() only inside `with` in readers/loader", c_with_used),
    (7, "docs/ingestion_notes.md answered", c_notes),
    (8, "strict=True raises the first RecordValidationError", c_s_strict),
    (8, "max_errors + TooManyErrorsError", c_s_max_errors),
]


def locate_repo(arg):
    candidates = [Path(arg)] if arg else [Path.cwd(), Path(__file__).resolve().parent]
    for candidate in candidates:
        candidate = candidate.resolve()
        if (candidate / "qe_foundations" / "ingestion").is_dir():
            return candidate
    return None


def main():
    global REPO, TMP
    parser = argparse.ArgumentParser(description="Self-check for the Day 2 ingestion exercise")
    parser.add_argument("--repo", help="folder that contains qe_foundations/ingestion")
    parser.add_argument("--stretch", action="store_true", help="also run the stretch-goal checks")
    parser.add_argument("-v", "--verbose", action="store_true", help="show tracebacks for failures")
    args = parser.parse_args()

    repo = locate_repo(args.repo)
    if repo is None:
        print("ERROR: cannot find qe_foundations/ingestion.")
        print("Run this script from the root of your qe-foundations repo, or pass --repo <path>.")
        return 2
    REPO = repo
    sys.path.insert(0, str(REPO))

    print("=" * 72)
    print("Week 2 Day 2 - ingestion module self-check")
    print(f"Repo: {REPO}")
    print(f"Python {sys.version.split()[0]}")
    print("=" * 72)

    results = {}
    with tempfile.TemporaryDirectory(prefix="ingest_check_") as tmp:
        TMP = Path(tmp)
        current = None
        for task, title, func in CHECKS:
            if task == 8 and not args.stretch:
                continue
            if task != current:
                current = task
                print()
                print(TASK_TITLES[task])
            try:
                func()
            except CheckFailure as failure:
                status, detail = "FAIL", str(failure)
            except Exception as error:  # a crash in YOUR code is a failure, not a crash of the checker
                status = "FAIL"
                detail = f"{type(error).__name__}: {error}"
                if args.verbose:
                    detail += "\n" + traceback.format_exc()
            else:
                status, detail = "PASS", ""
            results.setdefault(task, []).append(status == "PASS")
            print(f"  [{status}] {title}")
            if detail:
                for line in detail.splitlines():
                    print(f"         -> {line}")

    core = [ok for task, flags in results.items() if task != 8 for ok in flags]
    print()
    print("-" * 72)
    for task in sorted(results):
        flags = results[task]
        print(f"  {TASK_TITLES[task]:<62} {sum(flags)}/{len(flags)}")
    print("-" * 72)
    passed, total = sum(core), len(core)
    print(f"CORE CHECKS PASSED: {passed}/{total}  ({round(100 * passed / total)}%)")
    if args.stretch and 8 in results:
        print(f"STRETCH CHECKS PASSED: {sum(results[8])}/{len(results[8])}")
    if passed == total:
        print("All core checks pass. Now work through the Definition of Done in README.md and commit.")
        return 0
    print("Some checks fail. Fix the first failing task, re-run, repeat. Use -v for tracebacks;")
    print("see the hints in README.md for the task named above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
