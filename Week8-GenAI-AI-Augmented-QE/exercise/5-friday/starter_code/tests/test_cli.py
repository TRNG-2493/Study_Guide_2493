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


# TODO Stage 4: add tests for (1) an invalid input story -> exit 2, (2) --strict turning a
# warning into a failure, (3) --json writing a report with verdict and stopped_at.
