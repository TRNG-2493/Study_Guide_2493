"""Contract tests: the four enforcement points. Provided complete: your rr/contract.py must pass them.
The sample pairs are the test data. Lesson: written/5-friday/implementing-io-contracts.md, section 9."""
import json
from pathlib import Path

import pytest

from rr.contract import (CONTRACT_VERSION, INPUT_DEFAULTS, ContractError, ReviewResult, check_input,
                         check_output_schema, parse_reply)

ROOT = Path(__file__).resolve().parent.parent
PAIRS = sorted((ROOT / "agent" / "samples").glob("*.json"))


def pair(name):
    return json.loads(next(p for p in PAIRS if p.name.startswith(name)).read_text(encoding="utf-8"))


def test_defaults_are_read_from_the_input_schema():
    schema = json.loads((ROOT / "agent/schemas/rr_input.schema.json").read_text(encoding="utf-8"))
    assert INPUT_DEFAULTS == {k: v["default"] for k, v in schema["properties"].items() if "default" in v}


def test_gate_applies_defaults_and_keeps_the_callers_values():
    story = pair("P01")["input"]                       # has max_findings 6, no focus
    gated = check_input(story)
    assert gated["max_findings"] == 6 and gated["focus"] == INPUT_DEFAULTS["focus"]
    assert "focus" not in story, "the gate must return a NEW dict, not edit the caller's"


@pytest.mark.parametrize("path", PAIRS, ids=lambda p: p.stem)
def test_pair_inputs_pass_or_fail_the_gate_as_the_pair_says(path):
    p = json.loads(path.read_text(encoding="utf-8"))
    if p["input_should_be_valid"]:
        check_input(p["input"])
    else:
        with pytest.raises(ContractError) as exc:
            check_input(p["input"])
        assert exc.value.stage == "input" and len(exc.value.errors) >= 2   # ALL problems, not the first


@pytest.mark.parametrize("path", PAIRS, ids=lambda p: p.stem)
def test_reference_outputs_pass_parse_and_schema(path):
    p = json.loads(path.read_text(encoding="utf-8"))
    if p["expected_output"] is not None:
        out = check_output_schema(parse_reply(json.dumps(p["expected_output"])))
        assert ReviewResult.from_dict(out).contract_version == CONTRACT_VERSION


@pytest.mark.parametrize("reply, message_part", [
    ('```json\n{"a": 1}\n```', "fences"),
    ("Sure! Here is the review.", "not valid JSON"),
    ("[1, 2]", "JSON object"),
])
def test_strict_parse_rejects(reply, message_part):
    with pytest.raises(ContractError) as exc:
        parse_reply(reply)
    assert exc.value.stage == "parse" and message_part in exc.value.errors[0]


def test_output_gate_collects_every_problem():
    bad = {"contract_version": "0.9.0", "story_id": "US-420", "status": "done", "findings": []}
    with pytest.raises(ContractError) as exc:
        check_output_schema(bad)
    assert exc.value.stage == "output" and len(exc.value.errors) == 3   # version, status, open_questions
