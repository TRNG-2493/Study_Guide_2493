"""qe_foundations/ingestion/readers.py  -  TASK 4 (about 35 min)

One reader per format. Each returns a LIST OF RAW RECORDS and only deals with
FORMAT problems (is this valid CSV / JSON / XML? are the columns there?).
Business rules (is the status allowed? is the duration negative?) belong to
validation.py, NOT here.

Always open files through open_source() from contexts.py.
See README Task 4 for the exact contract of each reader.
"""

import csv
import json
import xml.etree.ElementTree as ET

from .contexts import open_source
from .exceptions import MalformedSourceError, MissingColumnsError
from .validation import REQUIRED_FIELDS


def read_csv_records(path):
    """CSV -> list of raw dicts, one per data row (use csv.DictReader)."""
    raise NotImplementedError("Task 4A: write read_csv_records")


def read_json_records(path):
    """JSON -> list of raw records. Expected shape: {"suite": ..., "tests": [...]}."""
    raise NotImplementedError("Task 4B: write read_json_records")


def read_xml_records(path):
    """XML -> list of raw dicts, one per <testcase> element at ANY depth."""
    raise NotImplementedError("Task 4C: write read_xml_records")
