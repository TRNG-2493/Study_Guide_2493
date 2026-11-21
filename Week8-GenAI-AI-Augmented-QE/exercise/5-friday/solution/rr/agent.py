# rr/agent.py
"""RequirementReviewer: instructions + template + contract + model + validation, wired.

Start-up checks (fail fast): agent.json and the contract agree; the instruction file loads
(nine sections, header, contract version); the pinned template exists; both schemas are valid
(checked when rr.contract is imported). run() never repairs, retries or edits a reply.
Provided complete. Lesson: written/5-friday/executing-agents-against-qa-requirements.md, section 5.
"""
import json
from dataclasses import dataclass, field
from pathlib import Path

from rr.contract import CONTRACT_VERSION, ContractError, check_input
from rr.instructions import load_instructions
from rr.templates import LEFTOVER, render, template_path
from rr.validation import ValidationReport, validate_reply

ROOT = Path(__file__).resolve().parent.parent


@dataclass
class AgentRun:
    story_id: str
    outcome: str                       # rejected_input | FAIL | PASS | PASS_WITH_WARNINGS
    messages: list = field(default_factory=list)
    reply: str = ""
    report: ValidationReport = None
    input_errors: list = field(default_factory=list)
    story: dict = None                 # the gated input, defaults applied


class RequirementReviewer:
    __test__ = False

    def __init__(self, model, config: str = "agent.json"):
        self.config = json.loads((ROOT / config).read_text(encoding="utf-8"))
        if self.config["contract_version"] != CONTRACT_VERSION:
            raise ValueError("agent.json and rr/contract.py disagree on the contract version")
        self.instructions = load_instructions(ROOT / self.config["instructions"], expected_contract=CONTRACT_VERSION)
        t = self.config["template"]
        template_path(t["name"], t["version"])            # KeyError at start-up if the pin is wrong
        self.model = model

    def build_messages(self, story: dict) -> list:
        t = self.config["template"]
        user = render(t["name"], t["version"], story)
        if LEFTOVER.findall(user):
            raise ValueError(f"unfilled placeholders: {LEFTOVER.findall(user)}")
        return [{"role": "system", "content": self.instructions.text}, {"role": "user", "content": user}]

    def run(self, raw_story: dict) -> AgentRun:
        story_id = str(raw_story.get("story_id"))
        try:
            story = check_input(raw_story)                 # 1. input gate (defaults applied once)
        except ContractError as exc:
            return AgentRun(story_id, "rejected_input", input_errors=exc.errors)
        messages = self.build_messages(story)              # 2. instructions + template
        reply = self.model.complete(messages, self.config["model_settings"])   # 3. model
        report = validate_reply(story, reply)              # 4. validation
        return AgentRun(story_id, report.verdict, messages, reply, report, story=story)
