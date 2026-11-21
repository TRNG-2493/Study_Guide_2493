# run_requirements.py
"""Execute RequirementReviewer against every story in a requirements file and record the run.

Usage:  python run_requirements.py requirements/backlog.csv --run-id day1 [--config agent.json] [--model scripted|saved] [--only US-430,US-470]
Writes runs/<run-id>/<story>.input.json, <story>.reply.txt and run.jsonl (one record per story).
--model saved reads live/<story>.reply.txt, the replies you saved from Claude yourself.
Provided complete. Lesson: written/5-friday/executing-agents-against-qa-requirements.md, sections 3 and 6.
"""
import argparse
import csv
import hashlib
import json
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

from rr.agent import RequirementReviewer
from rr.model import SavedReplyModel, ScriptedModel


def load_backlog(path: str) -> list:
    """One CSV row per acceptance criterion -> one input-contract dict per story. Converts; does not check."""
    stories = OrderedDict()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            story = stories.setdefault(row["story_id"], {"story_id": row["story_id"], "title": row["title"],
                                                         "acceptance_criteria": []})
            story["acceptance_criteria"].append({"id": row["ac_id"], "text": row["ac_text"]})
    return list(stories.values())


def fingerprint(messages: list) -> str:
    joined = "\n".join(f"{m['role']}:{m['content']}" for m in messages)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def main() -> None:
    p = argparse.ArgumentParser(description="Run RequirementReviewer over a backlog.")
    p.add_argument("backlog")
    p.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    p.add_argument("--config", default="agent.json")
    p.add_argument("--model", choices=["scripted", "saved"], default="scripted")
    p.add_argument("--only", help="comma-separated story ids to run (default: all)")
    a = p.parse_args()
    model = ScriptedModel("replies") if a.model == "scripted" else SavedReplyModel("live")
    agent = RequirementReviewer(model, a.config)
    run_dir = Path("runs") / a.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    records = []
    wanted = set(a.only.split(",")) if a.only else None
    for story in load_backlog(a.backlog):
        if wanted and story["story_id"] not in wanted:
            continue
        result = agent.run(story)
        record = {"run_id": a.run_id, "story_id": result.story_id, "outcome": result.outcome,
                  "agent_version": agent.config["version"], "instructions_version": agent.instructions.version,
                  "template": f"{agent.config['template']['name']}@{agent.config['template']['version']}",
                  "contract_version": agent.config["contract_version"], "model": a.model,
                  "model_settings": agent.config["model_settings"],
                  "prompt_fingerprint": fingerprint(result.messages) if result.messages else None,
                  "errors": result.input_errors or [f"{f.rule} {f.where}: {f.message}" for f in result.report.errors],
                  "warnings": [] if result.report is None else [f"{f.rule} {f.where}: {f.message}" for f in result.report.warnings],
                  "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        records.append(record)
        if result.outcome != "rejected_input":
            (run_dir / f"{result.story_id}.input.json").write_text(json.dumps(result.story, indent=2), encoding="utf-8")
            (run_dir / f"{result.story_id}.reply.txt").write_text(result.reply, encoding="utf-8")
    with open(run_dir / "run.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"run {a.run_id}: {len(records)} stories, {model.calls} model calls")
    print(f"{'story':<9}{'outcome':<20}{'err':>4}{'warn':>5}  fingerprint")
    for r in records:
        print(f"{r['story_id']:<9}{r['outcome']:<20}{len(r['errors']):>4}{len(r['warnings']):>5}  {r['prompt_fingerprint']}")


if __name__ == "__main__":
    main()
