# trace_matrix.py
"""Traceability for a run: AC -> findings, and stories blocked on the product owner.
Usage:  python trace_matrix.py runs/<run-id>
Provided complete. Lesson: written/5-friday/executing-agents-against-qa-requirements.md, section 9.
"""
import json
import sys
from pathlib import Path

from rr.contract import ContractError, check_output_schema, parse_reply

run = Path(sys.argv[1])
print(f"{'story':<8} {'AC':<5} {'findings':<22} status")
for inp in sorted(run.glob("*.input.json")):
    story = json.loads(inp.read_text(encoding="utf-8"))
    reply = inp.with_name(inp.name.replace(".input.json", ".reply.txt")).read_text(encoding="utf-8")
    try:
        out = check_output_schema(parse_reply(reply))
    except ContractError as exc:
        print(f"{story['story_id']:<8} {'-':<5} {'(reply unusable: ' + exc.stage + ')':<22}")
        continue
    if out["status"] == "needs_clarification":
        print(f"{story['story_id']:<8} {'all':<5} {'-':<22} BLOCKED: {out['open_questions'][0][:50]}")
        continue
    for ac in story["acceptance_criteria"]:
        ids = [f["id"] for f in out["findings"] if f["ac_id"] == ac["id"]]
        print(f"{story['story_id']:<8} {ac['id']:<5} {', '.join(ids) or '-':<22} {'questions for PO' if ids else 'no finding'}")
