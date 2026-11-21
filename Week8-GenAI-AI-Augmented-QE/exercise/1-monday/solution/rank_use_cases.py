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


# Exemplar candidates (instructor reference). Trainee scores will differ; grade the reasons.
def _uc(name, scores, reasons):
    return UseCase(name, *scores, why=dict(zip(CRITERIA, reasons)))


CANDIDATES: list[UseCase] = [
    _uc("Review new user stories (US-101..103) for ambiguity before automation", (4, 4, 4, 2, 1), (
        "defects found before code are cheapest", "every sprint brings new stories",
        "tester reads a short list of questions in minutes", "a bad question wastes minutes; PO decides",
        "stories are internal but contain no personal data")),
    _uc("Draft boundary and negative test ideas plus pytest skeletons for new rules (shipping)", (4, 4, 4, 2, 1), (
        "saves design time and adds forgotten edge cases", "new rules most sprints",
        "pytest run plus BVA review against the docstring", "wrong expected results are caught by review",
        "business rules only, synthetic")),
    _uc("Generate synthetic registration data for data-driven tests", (3, 3, 5, 2, 1), (
        "replaces repetitive hand-written CSV rows", "whenever a form or rule changes",
        "a 20-line rules checker validates every row in seconds", "a mislabelled row breaks a test, not production",
        "synthetic by design, reserved example domains")),
    _uc("Summarise the nightly CI failures for the morning stand-up", (4, 5, 3, 3, 3), (
        "frees the first hour of the day", "every night",
        "must re-read log lines to confirm each cause", "a wrong cause sends someone down the wrong path",
        "real logs can hold tokens and hosts; needs redaction")),
    _uc("Turn exploratory notes into structured bug reports", (3, 4, 4, 3, 2), (
        "clearer, consistent reports", "several per week",
        "the reporter re-reads steps against what they did", "AI can change steps or overstate severity",
        "notes may mention test accounts")),
    _uc("Draft page-object skeletons for new pages", (3, 2, 3, 3, 1), (
        "less boilerplate", "a few new pages per release",
        "needs a run against the real page and locator review", "hallucinated methods or brittle locators",
        "page structure only")),
    _uc("Write the Friday plain-language quality summary for the PO", (3, 2, 2, 4, 2), (
        "saves writing time", "weekly",
        "numbers and omissions must be checked against the report", "a reassuring but wrong summary misleads decisions",
        "internal results")),
    _uc("Auto-approve releases from AI test summaries", (5, 3, 1, 5, 2), (
        "would remove a manual gate", "weekly releases",
        "nobody can check a go/no-go call quickly", "a wrong all-clear ships a defect",
        "internal results")),
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


# SENSITIVITY NOTES (exemplar, verified output)
# Default weights, top 3: story review (26), boundary ideas + pytest skeletons (26), synthetic data (24).
# verifiability=0, top 3: story review (14), boundary ideas (14), CI summary (10); synthetic data drops to 9.
# What moved and why: the CI summary overtakes synthetic data because its frequency and value are no
# longer offset by how hard it is to check, while synthetic data loses its main strength (a script can
# check every row). Auto-approve climbs from 9 points behind bug reports to a tie with them. Ignoring
# verifiability rewards ideas nobody can check, which is exactly the failure QE exists to prevent.
