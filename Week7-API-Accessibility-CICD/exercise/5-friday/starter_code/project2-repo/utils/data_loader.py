import csv
import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_csv(name):
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def json_params(name, key):
    """Turn payloads.json[key] (list of {id, ...}) into pytest.param objects with readable ids."""
    return [pytest.param(case, id=case["id"]) for case in read_json(name)[key]]
