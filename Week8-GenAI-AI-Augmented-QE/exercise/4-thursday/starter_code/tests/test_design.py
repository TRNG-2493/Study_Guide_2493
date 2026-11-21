"""Design gate as pytest: the same checks as `python design_lab.py gate`, one test each.
Expected at the start: most tests fail. Expected at the end of Thursday: all pass. Do not edit.
Friday's validation script will test the agent's OUTPUT; these tests check the DESIGN."""
import re

import pytest

import design_parts as dp

PAIRS = sorted(dp.SAMPLES.glob("*.json"))


def test_no_todo_left_in_agent_folder():
    assert dp.todo_markers() == []


def test_instructions_nine_sections_header_and_no_danger_line():
    text = dp.read(dp.INSTRUCTIONS)
    assert [s for s in dp.REQUIRED_SECTIONS if s not in dp.headings(text)] == []
    assert dp.instruction_header(text), "missing 'Version: x | Output contract: y | Owner: z' line"
    assert dp.danger_lines(text) == []


def test_both_schemas_are_valid_draft_2020_12():
    dp.validator(dp.input_schema_path())
    dp.validator(dp.output_schema_path())


def test_output_contract_design_rules():
    facts = dp.output_contract_facts()
    assert [k for k, ok in facts.items() if not ok] == []


def test_one_contract_version_everywhere():
    rows = dp.version_rows()
    truth = dict(rows)["output schema contract_version const"]
    assert [label for label, v in rows if v != truth] == []


def test_job_sentence_has_no_and():
    job = dp.load_json(dp.MANIFEST)["agent"]["job"]
    assert job and not re.search(r"\band\b", job, re.IGNORECASE)


def test_rule_catalogue_has_rules_in_every_layer():
    text = dp.read(dp.RULES)
    rows = [r for r in text.splitlines() if r.startswith("| ") and not r.startswith("| Rule")]
    code = [r for r in rows if re.match(r"\| R\d+ ", r) and "| Code" in r]
    warnings = [r for r in rows if re.match(r"\| Q\d+ ", r) and "Warning" in r]
    human = [r for r in rows if "Human" in r]
    assert len(code) >= 6 and len(warnings) >= 2 and len(human) >= 1


def test_every_required_category_has_a_pair():
    categories = {dp.load_json(p).get("category") for p in PAIRS}
    assert [c for c in dp.REQUIRED_CATEGORIES if c not in categories] == []


@pytest.mark.parametrize("pair_file", PAIRS, ids=lambda p: p.stem)
def test_pair_obeys_the_contract(pair_file):
    pair = dp.load_json(pair_file)
    assert (dp.check_input(pair["input"]) == []) == pair["input_should_be_valid"]
    if pair["expected_output"] is not None:
        assert dp.check_output(pair["expected_output"]) == []
    assert pair["expectations"]["must"], "every pair needs at least one MUST expectation"


@pytest.mark.parametrize("pair_file", PAIRS, ids=lambda p: p.stem)
def test_valid_pair_inputs_render_with_no_leftover_placeholder(pair_file):
    pair = dp.load_json(pair_file)
    if not pair["input_should_be_valid"]:
        pytest.skip("invalid input never reaches the template")
    assert dp.LEFTOVER.findall(dp.render(pair["input"])) == []
