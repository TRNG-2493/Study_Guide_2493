"""reqs_review.py - Stage 1: AI-assisted requirements analysis (adapted from the Wednesday demo). Do not edit.

    lint_requirements    deterministic baseline (weak words), no AI
    build_review_prompt  the format-locked review prompt to paste into the chat
    extract_json         tolerate fences and chatty wrapping (Tuesday)
    check_findings       grounding checks: shape, category, AC exists, quote, question
    reference_coverage   what did the AI MISS compared with our own manual review?
    build_question_log   turn kept findings into questions for the product owner

Lesson: written/3-wednesday/ai-assisted-requirements-analysis.md
        sections 4 (manual review), 6 (linter), 7 (prompt), 8 (checks), 10 (question log).
Golden rule (section 5): the AI may find problems and ask questions. It may not answer them.
"""
from __future__ import annotations

import json
import re

from qa_flow.stories import REFERENCE_ISSUES, STORIES, parse_acs

DEFECT_CATEGORIES = ["AMBIGUOUS", "UNMEASURABLE", "INCOMPLETE", "CONTRADICTION", "UNTESTABLE"]
FINDING_KEYS = {"ac", "category", "quote", "explanation", "question"}

WEAK_WORDS = {
    "vague quality": ["fast", "quick", "quickly", "user-friendly", "easy", "simple", "intuitive",
                      "efficient", "robust", "secure", "modern"],
    "vague quantity": ["some", "several", "many", "few", "most", "appropriate", "adequate",
                       "reasonable"],
    "weak obligation": ["should", "may", "might", "could", "if possible", "as needed"],
    "open-ended": ["etc", "and so on", "and/or", "tbd"],
}

# ---- 1. deterministic baseline --------------------------------------------
def lint_requirements(story_id: str) -> list[str]:
    """One line per weak word, per AC. Same output every run; never invents."""
    lines = []
    for ac, text in parse_acs(STORIES[story_id]).items():
        hits = []
        for category, words in WEAK_WORDS.items():
            for w in words:
                if re.search(r"\b" + re.escape(w) + r"\b", text.lower()):
                    hits.append(f"'{w}' ({category})")
        lines.append(f"{story_id} {ac}: " + (", ".join(hits) if hits else "no weak words"))
    return lines


# ---- 2. the prompt -------------------------------------------------------
def build_review_prompt(story_id: str) -> str:
    story = STORIES[story_id]
    return f"""You are a senior QA analyst reviewing user stories for an e-commerce web
app before any tests are written. You find problems; you never invent answers to them.

Review the user story between the <story> tags.

<story id="{story_id}">
{story}
</story>

Instructions:
1. Check every acceptance criterion for these defect categories:
   {", ".join(DEFECT_CATEGORIES)}.
2. For each problem, quote the exact words from the story that cause it.
3. Write one clarifying question for the product owner per problem.
4. Do NOT propose answers, numbers or rules that are not in the story.
   If something is missing, ask about it.
5. If an acceptance criterion has no problems, do not mention it.

Return ONLY a JSON array, no prose and no Markdown fences. Each element must
have exactly these keys: "ac", "category", "quote", "explanation", "question"."""


# ---- 3. parse and check --------------------------------------------------
def extract_json(raw: str) -> str:
    """Tolerate wrapping: ```json fences and 'Sure! Here is...' text (Tuesday)."""
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    starts = [i for i in (text.find("["), text.find("{")) if i != -1]
    if starts:
        text = text[min(starts):]
    end = max(text.rfind("]"), text.rfind("}"))
    return text[:end + 1] if end != -1 else text


def check_finding(f: dict, story: str) -> list[str]:
    """Return problems with one finding (empty list = well-formed and grounded)."""
    if not isinstance(f, dict) or set(f) != FINDING_KEYS:
        return [f"wrong keys: {sorted(f) if isinstance(f, dict) else type(f).__name__}"]
    problems = []
    if f["category"] not in DEFECT_CATEGORIES:
        problems.append(f"unknown category {f['category']!r}")
    if f["ac"] not in parse_acs(story):
        problems.append(f"{f['ac']} does not exist in the story")
    if str(f["quote"]).lower() not in story.lower():
        problems.append(f"quote not found in story: {f['quote']!r}")
    if not str(f["question"]).strip().endswith("?"):
        problems.append("question does not end with '?'")
    if re.search(r"\b\d+(\.\d+)?\s*(seconds?|ms|%|characters)\b", str(f["question"]) + " "
                 + str(f["explanation"])) and not re.search(
                     r"\b\d+(\.\d+)?\s*(seconds?|ms|%|characters)\b", story):
        problems.append("proposes a number that is not in the story (golden rule)")
    return problems


def check_findings(raw: str, story_id: str) -> tuple[list[dict], list[tuple[int, dict, list[str]]]]:
    story = STORIES[story_id]
    findings = json.loads(extract_json(raw))
    kept, report = [], []
    for i, f in enumerate(findings, start=1):
        problems = check_finding(f, story)
        report.append((i, f, problems))
        if not problems:
            kept.append(f)
    return kept, report


def reference_coverage(findings: list[dict], story_id: str) -> list[tuple[str, bool]]:
    """Compare ALL findings with our manual review. A missed item is a false negative."""
    blob = " ".join(" ".join(str(v) for v in f.values()) for f in findings if isinstance(f, dict)).lower()
    return [(name, any(k.lower() in blob for k in keys)) for name, keys in REFERENCE_ISSUES.get(story_id, [])]


# ---- 4. question log -----------------------------------------------------
def build_question_log(kept: list[dict], story_id: str) -> str:
    """Markdown question log. The AI wrote the questions; the PO writes the answers."""
    rows = ["| ID | Story | AC | Category | Question | Owner | Status | Answer |",
            "|---|---|---|---|---|---|---|---|"]
    for n, f in enumerate(kept, start=1):
        q = str(f["question"]).replace("|", "/")
        rows.append(f"| Q-{n} | {story_id} | {f['ac']} | {f['category']} | {q} | PO | OPEN | |")
    return "\n".join(rows)
