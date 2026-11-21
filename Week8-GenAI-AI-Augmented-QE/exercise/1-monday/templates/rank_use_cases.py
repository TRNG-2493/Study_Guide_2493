"""rank_use_cases.py - Stage 3: score and rank your GenAI candidates.

Based on the helper in written/1-monday/generative-ai-applications-within-qe.md, section 6,
and `python llm_mechanics_lab.py rank` from the Monday demo.

What to do:
1. Add at least 6 of your GenAI candidates from tool-choice-worksheet.md to CANDIDATES.
   Score each criterion from 1 to 5 and write a short reason in `why` for EVERY score.
2. Run:  python rank_use_cases.py
3. Sensitivity experiment: run again with the verifiability weight set to 0:
         python rank_use_cases.py --weight verifiability=0
   Record what moved in the SENSITIVITY NOTES block at the bottom of this file.
4. Optional: add a sixth criterion, effort_to_adopt (1 = trivial, 5 = big project),
   with a negative weight of your choice, and justify the weight.

This is plain Python. No AI is involved. It is a decision aid, not a decision maker:
you may override the ranking in Stage 6, but you must say why.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field


@dataclass
class UseCase:
    name: str
    value: int             # 1 (low) to 5 (high)
    frequency: int         # 1 (rare) to 5 (daily)
    verifiability: int     # 1 (hard to check) to 5 (easy to check)
    risk_if_wrong: int     # 1 (harmless) to 5 (severe)
    data_sensitivity: int  # 1 (public/synthetic) to 5 (highly sensitive)
    why: dict[str, str] = field(default_factory=dict)  # one short reason per score


CRITERIA = ["value", "frequency", "verifiability", "risk_if_wrong", "data_sensitivity"]

# Same starting weights as the lesson. Change them only if you can defend the change.
WEIGHTS = {"value": 3, "frequency": 2, "verifiability": 3, "risk_if_wrong": -2, "data_sensitivity": -2}


# TODO: replace the example below with at least 6 of YOUR GenAI candidates.
# The example is the lesson's anti-pattern; keep it in your list as a reference point if you like.
CANDIDATES: list[UseCase] = [
    UseCase(
        "EXAMPLE - Auto-approve releases from AI test summaries",
        value=5, frequency=3, verifiability=1, risk_if_wrong=5, data_sensitivity=2,
        why={
            "value": "would remove a manual gate every release",
            "frequency": "releases are weekly",
            "verifiability": "nobody can check a go/no-go call quickly",
            "risk_if_wrong": "a wrong 'all clear' ships a defect",
            "data_sensitivity": "summaries contain internal results but no personal data",
        },
    ),
]


def score(uc: UseCase, weights: dict[str, int]) -> int:
    return sum(w * getattr(uc, name) for name, w in weights.items())


def validate(cases: list[UseCase]) -> list[str]:
    """Plain checks on YOUR input. Fix every problem before you trust the ranking."""
    problems = []
    for uc in cases:
        for name in CRITERIA:
            value = getattr(uc, name)
            if not isinstance(value, int) or not 1 <= value <= 5:
                problems.append(f"{uc.name}: {name}={value!r} is not a whole number 1-5")
            if not uc.why.get(name, "").strip():
                problems.append(f"{uc.name}: no reason given for {name}")
    if len(cases) < 6:
        problems.append(f"only {len(cases)} candidate(s); the exercise asks for at least 6")
    return problems


def parse_weight_overrides(argv: list[str]) -> dict[str, int]:
    weights = dict(WEIGHTS)
    if "--weight" in argv:
        for item in argv[argv.index("--weight") + 1:]:
            if item.startswith("--"):
                break
            key, _, val = item.partition("=")
            if key not in weights:
                sys.exit(f"Unknown criterion '{key}'. Choose from: {', '.join(weights)}")
            weights[key] = int(val)
    return weights


def main(argv: list[str]) -> int:
    weights = parse_weight_overrides(argv)
    problems = validate(CANDIDATES)
    for p in problems:
        print(f"CHECK  {p}")
    if problems:
        print()
    print("Weights:", weights)
    print(f"{'score':>5}  use case")
    for uc in sorted(CANDIDATES, key=lambda u: score(u, weights), reverse=True):
        print(f"{score(uc, weights):5d}  {uc.name}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


# SENSITIVITY NOTES (fill in after step 3)
# Ranking with default weights (top 3):
#   1.
#   2.
#   3.
# Ranking with verifiability=0 (top 3):
#   1.
#   2.
#   3.
# What moved and why (2-3 sentences):
#
