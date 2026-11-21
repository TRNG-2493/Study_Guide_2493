# evaluate.py
"""Evaluate RequirementReviewer over the sample pairs: many seeded runs, property checks, a scorecard.

Lesson: written/5-friday/agent-testing-and-refinement.md, sections 4 to 8.
Usage:  python evaluate.py [--config agent_v1.1.0.json] [--runs 20]
The model is rr/simulated.py: mistake rates are ILLUSTRATIVE, chosen for teaching.
A run passes a pair when validation does not FAIL **and** every MUST / MUST NOT check holds.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from rr.agent import RequirementReviewer
from rr.simulated import SimulatedModel
from rr.validation import check_q1

ROOT = Path(__file__).resolve().parent


def text_of(out: dict) -> str:
    return json.dumps(out)


def acs_with(out: dict, category: str) -> set:
    return {f["ac_id"] for f in out["findings"] if f["category"] == category}


def no_duplicates(o: dict) -> bool:
    keys = [(f["ac_id"], " ".join(f["quote"].lower().split())) for f in o["findings"]]
    return len(keys) == len(set(keys))


# MUST NOT rules every pair shares: report each problem once; ask, never answer.
GLOBAL_CHECKS = [
    ("MUST NOT report the same problem twice", lambda o, story: no_duplicates(o)),
    ("MUST NOT propose an answer (Q1)",        lambda o, story: not check_q1(story, o)),
]

# Executable versions of each pair's MUST / MUST NOT expectations (agent/samples/*.json).
PAIR_CHECKS = {
    "P01": [
        ("status is ok",                          lambda o: o["status"] == "ok"),
        ("AC5 'quickly' flagged UNMEASURABLE",    lambda o: "AC5" in acs_with(o, "UNMEASURABLE")),
        ("a finding on AC1 (case or separators)", lambda o: any(f["ac_id"] == "AC1" for f in o["findings"])),
        ("MUST NOT propose a number for quickly", lambda o: "second" not in text_of(o).lower()),
        ("no more than 6 findings",               lambda o: len(o["findings"]) <= 6),
    ],
    # TODO Stage 6 (step 2): turn the MUST / MUST NOT lists of P02, P03, P05 and P06
    # (agent/samples/*.json) into executable checks, in the same style as P01.
}


def load_pairs() -> dict:
    return {p["pair_id"]: p for p in (json.loads(f.read_text(encoding="utf-8"))
                                      for f in sorted((ROOT / "agent" / "samples").glob("P*.json")))}


def evaluate(config: str, runs: int) -> dict:
    pairs = load_pairs()
    scores, failed_checks, rule_errors, rule_warnings = {}, Counter(), Counter(), Counter()
    for pid, pair in pairs.items():                         # invalid-input pairs: gate must reject, model never called
        if not pair["input_should_be_valid"]:
            model = SimulatedModel(seed=0)
            result = RequirementReviewer(model, config).run(pair["input"])
            scores[pid] = (int(result.outcome == "rejected_input" and model.calls == 0), 1)
    for pid, checks in PAIR_CHECKS.items():
        passed = 0
        for seed in range(runs):
            run = RequirementReviewer(SimulatedModel(seed), config).run(pairs[pid]["input"])
            rule_errors.update(f.rule for f in run.report.errors)
            rule_warnings.update(f.rule for f in run.report.warnings)
            ok = run.outcome != "FAIL"
            if ok:
                out = json.loads(run.reply)
                broken = [name for name, check in checks if not check(out)]
                broken += [name for name, check in GLOBAL_CHECKS if not check(out, run.story)]
                failed_checks.update(f"{pid}: {b}" for b in broken)
                ok = not broken
            passed += ok
        scores[pid] = (passed, runs)
    return {"scores": scores, "rule_errors": rule_errors, "rule_warnings": rule_warnings,
            "failed_checks": failed_checks}


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RequirementReviewer over the sample pairs.")
    parser.add_argument("--config", default="agent.json")
    parser.add_argument("--runs", type=int, default=20)
    args = parser.parse_args()
    r = evaluate(args.config, args.runs)
    print(f"config {args.config}, {args.runs} runs per pair")
    tp = tr = 0
    for pid in sorted(r["scores"]):
        p, n = r["scores"][pid]
        tp, tr = tp + p, tr + n
        print(f"  {pid}: {p:>2}/{n:<4} {p / n:>4.0%}")
    print(f"  overall: {tp}/{tr} = {tp / tr:.0%}")
    print(f"  errors by rule:      {dict(sorted(r['rule_errors'].items()))}")
    print(f"  warnings by rule:    {dict(sorted(r['rule_warnings'].items()))}")
    print(f"  failed pair checks:  {dict(sorted(r['failed_checks'].items()))}")


if __name__ == "__main__":
    main()
