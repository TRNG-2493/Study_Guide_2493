# Starter: RequirementReviewer agent design (Week 8, Thursday, pair programming)

```
pip install -r requirements.txt          # jsonschema 4.18+ and pytest
python -c "import importlib.metadata as m; print(m.version('jsonschema'))"   # must be 4.18 or later
python design_lab.py gate                 # expect: DESIGN GATE: FAIL (you have not designed anything yet)
python -m pytest -q                       # expect: failures; all must pass by the end of the day
```

| Path | What it is | Edit? |
|---|---|---|
| `agent/CONTRACT.md` | The contract in plain English (write first) | Yes |
| `agent/instructions.md` | Nine-section instructions with a version header | Yes |
| `agent/templates/rr_user_v1.0.0.txt` | User-message template with `$placeholders` | Yes |
| `agent/schemas/rr_input.schema.json`, `rr_output.schema.json` | Draft 2020-12 contracts | Yes |
| `agent/rules.md` | Rule catalogue: every rule in one layer | Yes |
| `agent/samples/` | Your sample pairs (start from `agent/_PAIR_TEMPLATE.json`) | Yes |
| `agent/manifest.json` | Anatomy manifest + the 12 design questions | Yes |
| `agent/CHANGELOG.md` | Version history | Yes |
| `design_lab.py`, `design_parts.py` | Design checks (the demo's `anatomy_lab.py`, generalised) | No |
| `tests/test_design.py` | The design gate as pytest | No |
| `materials/inputs/` | Candidate story inputs for pairs and the Claude dry run | No |
| `evidence/` | Claude replies and your review of them | Yes |
| `pairing/` | Pairing log and retrospective | Yes |

Run every command from this folder. Friday you implement and validate this design; keep it clean.
