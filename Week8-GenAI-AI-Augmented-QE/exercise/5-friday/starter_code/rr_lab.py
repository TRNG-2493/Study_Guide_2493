# rr_lab.py
"""Helper for the Friday exercise. Provided complete.

    python rr_lab.py check              # environment, start-up checks, and what is still missing
    python rr_lab.py prompt US-470      # the exact prompt for one backlog story, to paste into Claude
"""
import argparse
import importlib.metadata as md
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def row(label, ok, note=""):
    print(f"  {label:<52} {'OK     ' if ok else 'MISSING'} {note}")
    return ok


def cmd_check(_):
    print("== Environment")
    row("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0])
    try:
        v = md.version("jsonschema")
        row("jsonschema 4.18+", tuple(int(x) for x in v.split(".")[:2]) >= (4, 18), v)
    except md.PackageNotFoundError:
        row("jsonschema 4.18+", False, "not installed")
    print("== Start-up (the agent assembles)")
    try:
        from rr.agent import RequirementReviewer
        from rr.model import ScriptedModel
        RequirementReviewer(ScriptedModel(), "agent.json")
        row("agent.json assembles", True)
    except Exception as exc:  # noqa: BLE001
        row("agent.json assembles", False, f"{type(exc).__name__}: {exc}")
    print("== Your implementation (pytest, no model calls)")
    for name in ("tests/test_contract.py", "tests/test_validation.py", "tests/test_cli.py"):
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", name], cwd=ROOT, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["no output"])[-1]
        row(name, r.returncode == 0, last)


def cmd_prompt(a):
    from rr.agent import RequirementReviewer
    from rr.contract import check_input
    from rr.model import ScriptedModel
    from run_requirements import fingerprint, load_backlog
    story = {s["story_id"]: s for s in load_backlog(a.backlog)}[a.story_id]
    agent = RequirementReviewer(ScriptedModel(), a.config)
    messages = agent.build_messages(check_input(story))
    print(f"fingerprint {fingerprint(messages)}  (agent {agent.config['version']}, instructions {agent.instructions.version})")
    print("Paste EVERYTHING between the lines as ONE message into a FRESH Claude chat.")
    print(f"Save the reply exactly as it came as live/{a.story_id}.reply.txt (UTF-8).")
    print("=" * 72)
    print("=== SYSTEM: agent instructions ===")
    print(messages[0]["content"].rstrip())
    print("\n=== USER: rendered template ===")
    print(messages[1]["content"].rstrip())
    print("=" * 72)


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest="cmd", required=True)
sub.add_parser("check").set_defaults(fn=cmd_check)
s = sub.add_parser("prompt"); s.add_argument("story_id")
s.add_argument("--backlog", default="requirements/backlog.csv"); s.add_argument("--config", default="agent.json")
s.set_defaults(fn=cmd_prompt)
a = p.parse_args()
a.fn(a)
