# validate_output.py
"""Command-line validator for RequirementReviewer replies.

Single:  python validate_output.py --story story.json --reply reply.txt
Batch:   python validate_output.py --run runs/demo      (pairs X.input.json with X.reply.txt)
Exit codes: 0 = all valid, 1 = at least one reply failed, 2 = the check itself could not run.

Lesson: written/5-friday/building-validation-scripts.md, section 4.
"""
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from rr.contract import ContractError, check_input
from rr.validation import validate_reply

EXIT_OK, EXIT_FAILED, EXIT_UNUSABLE = 0, 1, 2


def load_pairs(args) -> list:
    """Return [(story_dict, reply_path), ...] for single or batch mode."""
    if args.story:
        story = json.loads(Path(args.story).read_text(encoding="utf-8"))
        return [(story, Path(args.reply))]
    pairs = []
    for input_path in sorted(Path(args.run).glob("*.input.json")):
        reply_path = input_path.with_name(input_path.name.replace(".input.json", ".reply.txt"))
        story = json.loads(input_path.read_text(encoding="utf-8"))
        pairs.append((story, reply_path))              # a missing reply -> OSError later
    return pairs


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate RequirementReviewer replies.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--story", help="input story JSON (single mode, needs --reply)")
    mode.add_argument("--run", help="folder of X.input.json + X.reply.txt files (batch mode)")
    parser.add_argument("--reply", help="raw reply text file (single mode)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--json", metavar="FILE", help="also write a machine-readable report")
    args = parser.parse_args(argv)
    if args.story and not args.reply:
        parser.error("--story needs --reply")           # argparse exits with code 2

    try:
        pairs = load_pairs(args)
        results = []
        for story, reply_path in pairs:
            gated = check_input(story)                    # a bad story is a usage problem
            report = validate_reply(gated, reply_path.read_text(encoding="utf-8"))
            results.append((reply_path, report))
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(f"cannot validate: {exc}", file=sys.stderr)
        return EXIT_UNUSABLE
    if not results:
        print("cannot validate: no replies found", file=sys.stderr)
        return EXIT_UNUSABLE

    failed = 0
    for reply_path, report in results:
        verdict = report.verdict
        if args.strict and verdict == "PASS_WITH_WARNINGS":
            verdict = "FAIL (strict)"
        failed += verdict.startswith("FAIL")
        print(f"{verdict:<19} {reply_path.as_posix()}")
        for f in report.findings:
            print(f"    {f.severity.upper():<7} {f.rule:<3} {f.where}: {f.message}")
    print(f"{len(results)} checked, {len(results) - failed} passed, {failed} failed")

    if args.json:
        payload = [{"reply": p.as_posix(), "verdict": r.verdict, "stopped_at": r.stopped_at,
                    "findings": [asdict(f) for f in r.findings]} for p, r in results]
        Path(args.json).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return EXIT_FAILED if failed else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
