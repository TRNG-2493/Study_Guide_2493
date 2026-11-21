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

    # TODO Stage 4. The contract of this script (building-validation-scripts.md, section 4):
    #  - load the pairs; gate each story with check_input (a bad story is a USAGE problem);
    #    validate each reply with validate_reply
    #  - OSError, json.JSONDecodeError or ContractError while loading -> message on stderr, return EXIT_UNUSABLE
    #  - nothing to check -> "cannot validate: no replies found" on stderr, return EXIT_UNUSABLE
    #  - print one line per reply (verdict, path) and one line per finding; then "N checked, P passed, F failed"
    #  - --strict turns PASS_WITH_WARNINGS into a failure
    #  - --json FILE writes [{"reply", "verdict", "stopped_at", "findings": [...]}]
    #  - return EXIT_FAILED if any reply failed, else EXIT_OK
    raise NotImplementedError("Stage 4: validate_output.main")

if __name__ == "__main__":
    sys.exit(main())
