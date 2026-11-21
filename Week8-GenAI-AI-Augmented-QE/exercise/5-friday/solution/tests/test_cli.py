"""The validation script's interface: exit codes 0, 1, 2, stderr for problems, a JSON report.
Lesson: written/5-friday/building-validation-scripts.md, sections 4 to 6."""
import json
from pathlib import Path

from validate_output import EXIT_FAILED, EXIT_OK, EXIT_UNUSABLE, main

ROOT = Path(__file__).resolve().parent.parent
P01 = json.loads((ROOT / "agent/samples/P01-happy_path.json").read_text(encoding="utf-8"))


def write_run(tmp_path, reply_text, story=None):
    (tmp_path / "US-420.input.json").write_text(json.dumps(story or P01["input"]), encoding="utf-8")
    (tmp_path / "US-420.reply.txt").write_text(reply_text, encoding="utf-8")
    return str(tmp_path)


def test_all_valid_exits_0(tmp_path):
    assert main(["--run", write_run(tmp_path, json.dumps(P01["expected_output"]))]) == EXIT_OK


def test_a_failing_reply_exits_1(tmp_path):
    assert main(["--run", write_run(tmp_path, "not json")]) == EXIT_FAILED


def test_an_empty_folder_exits_2_and_says_why_on_stderr(tmp_path, capsys):
    assert main(["--run", str(tmp_path)]) == EXIT_UNUSABLE
    assert "no replies found" in capsys.readouterr().err


def test_an_invalid_input_story_exits_2(tmp_path):
    bad = {"story_id": "420", "title": "x", "acceptance_criteria": []}
    assert main(["--run", write_run(tmp_path, "{}", story=bad)]) == EXIT_UNUSABLE


def test_strict_turns_warnings_into_failures(tmp_path):
    out = json.loads(json.dumps(P01["expected_output"]))
    out["findings"][4]["question"] = "Should it be applied within 2 seconds?"
    run = write_run(tmp_path, json.dumps(out))
    assert main(["--run", run]) == EXIT_OK
    assert main(["--run", run, "--strict"]) == EXIT_FAILED


def test_json_report_is_written(tmp_path):
    report = tmp_path / "report.json"
    main(["--run", write_run(tmp_path, "not json"), "--json", str(report)])
    data = json.loads(report.read_text(encoding="utf-8"))
    assert data[0]["verdict"] == "FAIL" and data[0]["stopped_at"] == "parse"
