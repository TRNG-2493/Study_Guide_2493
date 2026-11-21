# rr/simulated.py
"""A SIMULATED model for practising agent testing offline.

It starts from the reviewed answer for each sample-pair story (sim_answers.json) and injects
typical mistakes at rates WE CHOSE for teaching. Some rates fall when the instructions
contain a rule that targets the mistake; others do not depend on the instructions at all.
The numbers are illustrative, not measurements of any real model.

Read this file only AFTER your error analysis (Stage 6, step 4). Reading MISTAKES first is
like reading the answer key: you would fix the simulator, not learn to analyse failures.
Provided complete. Lesson: written/5-friday/agent-testing-and-refinement.md, section 4.2.
"""
import copy
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# mistake: (rate without a targeting rule, rate with one, regex that recognises such a rule in the instructions)
MISTAKES = {
    "fences":          (0.08, 0.08, None),
    "wrong_ac":        (0.30, 0.04, r"quote\w*\b[^.]*\b(appears?|found|present|contained|occurs?|is in|comes? from|exists?|belongs?)\b[^.]*\b(criterion|ac_id|ac)\b"),
    "id_gap":          (0.20, 0.03, r"\b(without|no) gaps?\b|\bconsecutive(ly)?\b|\bsequential(ly)?\b|\bin sequence\b|\bskip\w* (a )?numbers?\b"),
    "duplicate":       (0.20, 0.04, r"\b(only|exactly) once\b|\bdo not repeat\b|\bno duplicates?\b|\bduplicate findings?\b|\bsame problem (twice|again|more than once)\b"),
    "proposed_answer": (0.10, 0.10, None),
    "over_limit":      (0.15, 0.15, None),
    "obey_request":    (0.35, 0.05, r"(test cases|tests|scripts|code)\b[^.]*\b(even|also)\b[^.]*\b(criteri\w*|story|ac)\b|\b(criteri\w*|ac)\b[^.]*\b(asks?|requests?)\b[^.]*\b(test cases|tests|scripts|code)\b"),
}


def rule_present(pattern: str, instructions: str) -> bool:
    return bool(pattern) and re.search(pattern, " ".join(instructions.split()), re.IGNORECASE) is not None


class SimulatedModel:
    def __init__(self, seed: int, answers: str = "sim_answers.json"):
        self.seed = seed
        self.answers = json.loads((ROOT / answers).read_text(encoding="utf-8"))
        self.calls = 0

    def complete(self, messages: list, settings: dict) -> str:
        self.calls += 1
        system, user = messages[0]["content"], messages[-1]["content"]
        story_id = re.search(r"^ID: (US-\d+)$", user, re.MULTILINE).group(1)
        limit = int(re.search(r"at most (\d+) findings", user).group(1))
        acs = re.findall(r"^- (AC\d+): (.+)$", user, re.MULTILINE)
        rng = random.Random(f"{self.seed}-{story_id}")          # same seed -> same dice for every version
        entry = self.answers[story_id]
        out = copy.deepcopy(entry["reply"])
        fs = out["findings"]
        number = story_id.split("-")[1]

        def happens(name):
            without, with_rule, pattern = MISTAKES[name]
            return rng.random() < (with_rule if rule_present(pattern, system) else without)

        # One draw per mistake, always in this order, so v1.0.0 and v1.1.0 see the SAME dice.
        if happens("obey_request") and entry["kind"] == "out_of_scope":      # does the job it was asked
            out["status"], out["open_questions"] = "ok", []
            fs.append({"id": f"F-{number}-01", "ac_id": acs[0][0], "category": "UNTESTABLE",
                       "quote": acs[0][1][:40].strip(), "explanation": "The criterion does not say which checkout flows the scripts must cover.",
                       "question": "Which checkout flows must the 20 scripts cover?", "severity": "medium"})
        if happens("wrong_ac") and len(fs) >= 1 and len(acs) >= 2:          # quote cited against the wrong AC
            others = [a for a, _ in acs if a != fs[-1]["ac_id"]]
            fs[-1]["ac_id"] = others[0]
        if happens("duplicate") and fs:                                     # the same problem reported twice
            fs.append(dict(fs[0], question=fs[0]["question"].rstrip("?") + " exactly?"))
        if happens("proposed_answer") and fs:                               # asks AND answers
            fs[0]["question"] = fs[0]["question"].rstrip("?") + ", for example within 2 seconds?"
        if happens("over_limit") and fs and len(fs) >= limit:               # one finding too many
            ac_id, ac_text = acs[-1]
            fs.append({"id": "", "ac_id": ac_id, "category": "AMBIGUOUS", "quote": " ".join(ac_text.split()[:3]),
                       "explanation": "The wording could be read in more than one way.",
                       "question": f"What exactly does {ac_id} require?", "severity": "low"})
        for i, f in enumerate(fs):                                          # renumber 01..n
            f["id"] = f"F-{number}-{i + 1:02d}"
        if happens("id_gap") and len(fs) >= 2:                              # skips a number
            fs[-1]["id"] = f"F-{number}-{len(fs) + 1:02d}"
        text = json.dumps(out, indent=2)
        if happens("fences"):
            text = "```json\n" + text + "\n```"
        return text
