# rr/contract.py
"""The RequirementReviewer IO contract, implemented at four enforcement points:
(A) input gate with defaults, (B) strict parse, (C) output schema gate, (D) typed objects.

Lesson: written/5-friday/implementing-io-contracts.md, sections 3 to 7.
Schemas: agent/schemas/rr_input.schema.json and rr_output.schema.json (Thursday's design).
"""
import json
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit('jsonschema is too old or missing. Fix: pip install "jsonschema>=4.18"')

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "agent" / "schemas"
CONTRACT_VERSION = "1.0.0"


class ContractError(Exception):
    """Data broke the contract. .stage is 'input', 'parse' or 'output'; .errors is one message per problem."""
    def __init__(self, stage: str, errors: list):
        super().__init__(f"{stage}: {len(errors)} contract error(s)")
        self.stage = stage
        self.errors = errors


def _load_validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)            # a broken schema stops the agent at start-up
    return Draft202012Validator(schema)


INPUT_SCHEMA = json.loads((SCHEMAS / "rr_input.schema.json").read_text(encoding="utf-8"))
INPUT_VALIDATOR = _load_validator("rr_input.schema.json")
OUTPUT_VALIDATOR = _load_validator("rr_output.schema.json")
# One fact, one place: READ the defaults from INPUT_SCHEMA (every property that has a "default").
INPUT_DEFAULTS: dict = {}   # TODO Stage 2
SCHEMA_CONTRACT = json.loads((SCHEMAS / "rr_output.schema.json").read_text(encoding="utf-8"))[
    "properties"]["contract_version"]["const"]
if SCHEMA_CONTRACT != CONTRACT_VERSION:
    raise RuntimeError(f"rr/contract.py says {CONTRACT_VERSION}, the output schema says {SCHEMA_CONTRACT}")


def _messages(validator: Draft202012Validator, doc) -> list:
    errors = sorted(validator.iter_errors(doc),
                    key=lambda e: [(0, p) if isinstance(p, int) else (1, str(p)) for p in e.absolute_path])
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}" for e in errors]


# ---- (A) input gate -----------------------------------------------------------
def check_input(story: dict) -> dict:
    """S2. Return a NEW dict with defaults applied (caller's values win), or raise ContractError('input')."""
    # TODO Stage 2: collect ALL schema problems with _messages(); raise ContractError("input", problems)
    # if there are any; otherwise return a NEW dict with INPUT_DEFAULTS applied (caller's values win).
    raise NotImplementedError("Stage 2: check_input")


# ---- (B) strict parse ------------------------------------------------------------
def parse_reply(reply: str) -> dict:
    """One JSON object and nothing else. Fences, prose and lists are contract breaks, not things to repair."""
    # TODO Stage 2: strip; reject fences, invalid JSON and non-objects with ContractError("parse", [message]).
    # Messages must contain "fences", "not valid JSON" or "JSON object" (see tests/test_contract.py).
    raise NotImplementedError("Stage 2: parse_reply")


# ---- (C) output schema gate -----------------------------------------------------
def check_output_schema(output: dict) -> dict:
    """S1, shape only. Meaning-level rules live in rr/validation.py."""
    # TODO Stage 2: collect ALL problems; raise ContractError("output", problems); else return output.
    raise NotImplementedError("Stage 2: check_output_schema")


# ---- (D) typed objects, built ONLY from validated output --------------------------
@dataclass(frozen=True)
class Finding:
    id: str
    ac_id: str
    category: str
    quote: str
    explanation: str
    question: str
    severity: str


@dataclass(frozen=True)
class ReviewResult:
    contract_version: str
    story_id: str
    status: str
    findings: list
    open_questions: list

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewResult":
        return cls(data["contract_version"], data["story_id"], data["status"],
                   [Finding(**f) for f in data["findings"]], list(data["open_questions"]))
