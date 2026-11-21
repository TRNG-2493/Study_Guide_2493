# show_failures.py
"""Read the failures before you count them: one line per failing seed for one pair.
Usage:  python show_failures.py agent.json P01 [--runs 20]
Provided complete. Lesson: written/5-friday/agent-testing-and-refinement.md, section 5.
"""
import argparse
import json

from evaluate import GLOBAL_CHECKS, PAIR_CHECKS, load_pairs
from rr.agent import RequirementReviewer
from rr.simulated import SimulatedModel

parser = argparse.ArgumentParser()
parser.add_argument("config")
parser.add_argument("pair")
parser.add_argument("--runs", type=int, default=20)
args = parser.parse_args()
pair = load_pairs()[args.pair]
for seed in range(args.runs):
    run = RequirementReviewer(SimulatedModel(seed), args.config).run(pair["input"])
    if run.outcome == "FAIL":
        rules = ", ".join(sorted({f.rule for f in run.report.errors}))
        print(f"seed {seed:>2}: {rules:<8} {run.report.errors[0].message}")
        continue
    out = json.loads(run.reply)
    broken = [n for n, c in PAIR_CHECKS.get(args.pair, []) if not c(out)]
    broken += [n for n, c in GLOBAL_CHECKS if not c(out, run.story)]
    if broken:
        print(f"seed {seed:>2}: CHECK    {'; '.join(broken)}")
