"""Who tests the tester: one planted defect per rule, and the EXACT set of rules that fire.
Lesson: written/5-friday/building-validation-scripts.md, section 7 (and agent-output-validation.md).
Each mutation changes ONE thing in a known-good reply. If it fires two rules, fix the test data, not the rule."""
import copy
import json
from pathlib import Path

import pytest

from rr.contract import check_input
from rr.validation import validate_reply

ROOT = Path(__file__).resolve().parent.parent
P01 = json.loads((ROOT / "agent/samples/P01-happy_path.json").read_text(encoding="utf-8"))
STORY = check_input(P01["input"])
GOOD = P01["expected_output"]


def mutate(change):
    out = copy.deepcopy(GOOD)
    change(out)
    return json.dumps(out)


PLANTED = {
    "R1": lambda o: o.update(story_id="US-421"),
    "R2": lambda o: o["findings"][1].update(ac_id="AC9"),
    # TODO Stage 3: one minimal mutation for each of R3, R4, R5, R6, R7, Q1, Q2.
    # Each must change ONE thing and fire EXACTLY its own rule (see the test below).
}


def test_every_rule_in_the_catalogue_has_a_planted_defect():
    assert set(PLANTED) == {"R1", "R2", "R3", "R4", "R5", "R6", "R7", "Q1", "Q2"}


def test_the_good_reply_passes_cleanly():
    report = validate_reply(STORY, json.dumps(GOOD))
    assert report.verdict == "PASS" and report.findings == []


@pytest.mark.parametrize("rule", sorted(PLANTED))
def test_each_planted_defect_fires_exactly_its_rule(rule):
    story = dict(STORY, focus=["AMBIGUOUS", "UNMEASURABLE", "INCOMPLETE"]) if rule == "R7" else STORY
    report = validate_reply(story, mutate(PLANTED[rule]))
    assert {f.rule for f in report.findings} == {rule}


def test_warnings_alone_do_not_fail():
    assert "Q1" in PLANTED, "plant Q1 first"
    assert validate_reply(STORY, mutate(PLANTED["Q1"])).verdict == "PASS_WITH_WARNINGS"


def test_shape_failure_stops_before_the_rules():
    report = validate_reply(STORY, "```json\n" + json.dumps(GOOD) + "\n```")
    assert report.stopped_at == "parse" and {f.rule for f in report.findings} == {"S1"}


def test_r3_ignores_case_spaces_and_curly_quotes():
    reply = mutate(lambda o: o["findings"][0].update(quote="Letters  A-Z and DIGITS only"))
    assert validate_reply(STORY, reply).verdict == "PASS"


def test_needs_clarification_with_findings_is_r6():
    reply = mutate(lambda o: o.update(status="needs_clarification", open_questions=["What are the rules?"]))
    assert {f.rule for f in validate_reply(STORY, reply).findings} == {"R6"}
