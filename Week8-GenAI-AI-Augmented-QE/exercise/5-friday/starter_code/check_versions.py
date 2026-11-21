# check_versions.py
"""One contract version everywhere? Exit 0 = AGREE, 1 = DISAGREE.
Usage:  python check_versions.py [--config agent.json]
Provided complete. Lesson: written/5-friday/implementing-io-contracts.md, section 8.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from rr.contract import CONTRACT_VERSION
from rr.instructions import HEADER

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--config", default="agent.json")
config = json.loads((ROOT / parser.parse_args().config).read_text(encoding="utf-8"))
tpl = (ROOT / "agent" / "templates" / f"{config['template']['name']}_v{config['template']['version']}.txt").read_text(encoding="utf-8")
rows = [
    ("agent config contract_version", config["contract_version"]),
    ("rr/contract.py CONTRACT_VERSION", CONTRACT_VERSION),
    ("instructions header", HEADER.search((ROOT / config["instructions"]).read_text(encoding="utf-8"))["contract"]),
    ("template format reminder", re.search(r'contract_version "([\d.]+)"', tpl).group(1)),
    ("output schema const", json.loads((ROOT / "agent/schemas/rr_output.schema.json").read_text())["properties"]["contract_version"]["const"]),
    ("output schema $id", json.loads((ROOT / "agent/schemas/rr_output.schema.json").read_text())["$id"].rsplit("/", 1)[-1]),
    ("input schema $id", json.loads((ROOT / "agent/schemas/rr_input.schema.json").read_text())["$id"].rsplit("/", 1)[-1]),
]
rows += [(f"samples/{p.name}", json.loads(p.read_text(encoding="utf-8"))["contract_version"])
         for p in sorted((ROOT / "agent" / "samples").glob("*.json"))]
for label, value in rows:
    print(f"{label:<42}{value}")
values = sorted({v for _, v in rows})
print("AGREE" if len(values) == 1 else f"DISAGREE: {values}")
sys.exit(0 if len(values) == 1 else 1)
