"""
design_lab.py - Week 8 Thursday pair exercise: check your requirements-agent DESIGN.

Same commands as the demo's anatomy_lab.py, pointed at YOUR agent/ folder. No model calls.

    python design_lab.py dissect                     # 12 design questions from agent/manifest.json
    python design_lab.py check-instructions [FILE]   # nine sections, version header, weak words, DANGER lines
    python design_lab.py check-schemas               # both schemas valid Draft 2020-12 + contract design rules
    python design_lab.py render INPUT.json           # template filled once; leftover placeholders
    python design_lab.py messages INPUT.json [--full]  # what you paste into Claude (one message)
    python design_lab.py check-input FILE            # input contract gate (S2)
    python design_lab.py check-output FILE [--explain] # parse + output contract (S1)
    python design_lab.py pairs                       # pairs obey the contract + coverage matrix
    python design_lab.py versions                    # one contract version across every organ?
    python design_lab.py gate                        # everything above that can be checked, one verdict
Do not edit.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import design_parts as dp


def cmd_dissect(_):
    m = dp.load_json(dp.MANIFEST)
    ag = m["agent"]
    print(f"== Dissecting {ag.get('name') or 'UNNAMED'} (version {ag.get('version') or 'NONE'}, "
          f"autonomy {ag.get('autonomy') or 'NONE'})")
    gaps = 0
    parts = {p["id"]: p for p in m.get("parts", [])}
    for q in m["design_questions"]:
        ans, ev, topic = q.get("answer", ""), q.get("evidence"), q["topic"]
        verdict, note = "OK", ""
        if not ans or "TODO" in ans:
            verdict, note = "GAP", "no answer"
        elif ev and not (dp.AGENT.parent / ev).exists():
            verdict, note = "GAP", f"evidence {ev} missing"
        elif topic == "job":
            n_and = len(re.findall(r"\band\b", ans, re.IGNORECASE))
            if n_and:
                verdict, note = "GAP", f"'and' appears {n_and} time(s): more than one job?"
            if ans.strip() != ag.get("job", "").strip():
                verdict, note = "GAP", "answer differs from agent.job"
        elif topic == "autonomy" and ag.get("autonomy") == "autonomous":
            verdict, note = "FLAG", "autonomous: hardest to test; is it justified for QA?"
        elif topic == "tools":
            risky = [t.get("name") for t in parts.get("tools", {}).get("items", [])
                     if t.get("effect") in ("write", "delete", "send")]
            if risky:
                verdict, note = "FLAG", f"can change the world: {', '.join(risky)}"
        elif topic == "context_memory" and re.search(r"\bever\b|forever|everything", ans, re.IGNORECASE):
            verdict, note = "FLAG", "unbounded memory: runs are not repeatable"
        if verdict != "OK":
            gaps += 1
        shown = ans if len(ans) <= 60 else ans[:57] + "..."
        print(f"{q['n']:>2}. {topic:<16}{verdict:<5} {shown or '-'}")
        if note:
            print(f"    {'':<16}      -> {note}")
    owners = [p["id"] for p in m.get("parts", []) if not p.get("owner") or "TODO" in p.get("owner", "")]
    print(f"parts without an owner: {owners or 'none'}")
    print(f"design gaps or flags: {gaps}")
    return gaps + len(owners)


def cmd_check_instructions(a):
    path = Path(a.file) if a.file else dp.INSTRUCTIONS
    text = dp.read(path)
    missing = [s for s in dp.REQUIRED_SECTIONS if s not in dp.headings(text)]
    hdr = dp.instruction_header(text)
    print(f"== {path}")
    print(f"sections present: {len(dp.REQUIRED_SECTIONS) - len(missing)}/{len(dp.REQUIRED_SECTIONS)}")
    print(f"missing: {missing or 'none'}")
    print(f"version header: {'Version ' + hdr['version'] + ', output contract ' + hdr['contract'] if hdr else 'NONE'}")
    weak = dp.weak_words(text)
    print(f"weak words: {len(weak)}")
    for n, w in weak:
        print(f"  line {n}: '{w}'")
    danger = dp.danger_lines(text)
    for n, p in danger:
        print(f"  DANGER line {n}: '{p}' tells the model to INVENT requirements")
    todos = [t for t in text.splitlines() if "TODO" in t]
    if todos:
        print(f"TODO lines left: {len(todos)}")
    return len(missing) + (0 if hdr else 1) + len(danger) + len(todos)


def cmd_check_schemas(_):
    bad = 0
    for label, getter in (("input", dp.input_schema_path), ("output", dp.output_schema_path)):
        try:
            path = getter()
            dp.validator(path)
            print(f"{label} schema {path.name}: valid Draft 2020-12")
        except Exception as e:  # noqa: BLE001 - report any problem with the schema itself
            bad += 1
            print(f"{label} schema: INVALID - {str(e).splitlines()[0]}")
    if not bad:
        for rule, ok in dp.output_contract_facts().items():
            print(f"  {'OK  ' if ok else 'GAP '} output contract: {rule}")
            bad += not ok
    return bad


def _load_input(path):
    return dp.load_json(path)


def cmd_render(a):
    story = _load_input(a.input)
    tpl = dp.template_path()
    print(f"template: {tpl.name} | placeholders: {dp.placeholders(dp.read(tpl))}")
    print("-" * 72)
    try:
        text = dp.render(story)
    except KeyError as e:
        print(f"KeyError: {e}  <- a placeholder has no value and no schema default (loud, as it should be)")
        return 1
    print(text.rstrip())
    print("-" * 72)
    left = dp.LEFTOVER.findall(text)
    print(f"leftover placeholders: {left or 'none'}")
    return len(left)


def cmd_messages(a):
    msgs = dp.messages(_load_input(a.input))
    if a.full:
        print("Paste EVERYTHING between the lines as ONE message into a FRESH Claude chat.")
        print("=" * 72)
        print("=== SYSTEM: agent instructions ===")
        print(msgs[0]["content"].rstrip())
        print()
        print("=== USER: rendered template ===")
        print(msgs[1]["content"].rstrip())
        print("=" * 72)
    else:
        for m in msgs:
            print(f"{m['role']:<6} | {len(m['content']):>5} chars | starts: {m['content'].splitlines()[0]}")
    return 0


def cmd_check_input(a):
    errs = dp.check_input(_load_input(a.file))
    if errs:
        print("S2 REJECTED before calling the model:")
        for e in errs:
            print(f"  - at {dp.where(e)}: {e.message}")
        print("model calls made: 0")
    else:
        print("S2 ACCEPTED: safe to send to the agent")
    return len(errs)


def cmd_check_output(a):
    obj, verdict = dp.parse_reply(dp.read(a.file))
    print(f"PARSE: {verdict}")
    if obj is None:
        return 1
    errs = dp.check_output(obj)
    if not errs:
        print("S1 PASS: shape matches the output contract (shape only; rules and a human come next)")
        return 0
    print(f"S1 FAIL: {len(errs)} error(s)")
    for e in errs:
        msg = e.message if len(e.message) <= 90 else e.message[:87] + "..."
        print(f"  {dp.where(e):<26} {msg}")
    if a.explain:
        e = errs[0]
        print(f"\nWHERE: {dp.where(e)}\nWHAT:  '{e.validator}' rule failed\n"
              f"EXPECTED: {json.dumps(e.validator_value)[:70]}\nACTUAL:   {json.dumps(e.instance)[:70]}")
    return len(errs)


def cmd_pairs(_):
    files = sorted(dp.SAMPLES.glob("*.json"))
    if not files:
        print("no sample pairs yet in agent/samples/")
        return 1
    statuses = dp.load_json(dp.output_schema_path()).get("properties", {}).get("status", {}).get("enum", [])
    problems = 0
    print("== Step 1: do the pairs obey the contract? ==")
    pairs = []
    for f in files:
        pair = dp.load_json(f)
        pairs.append(pair)
        pid = pair.get("pair_id", f.stem)
        for key in ("contract_version", "pair_id", "category", "purpose", "input", "input_should_be_valid",
                    "expected_output", "expectations"):
            if key not in pair:
                problems += 1
                print(f"{pid}: PROBLEM - missing key '{key}'")
        if "input" not in pair:
            continue
        in_err = dp.check_input(pair["input"])
        if (not in_err) != pair.get("input_should_be_valid"):
            problems += 1
            print(f"{pid}: PROBLEM - input valid={not in_err}, pair says {pair.get('input_should_be_valid')}")
        elif in_err:
            print(f"{pid}: input rejected as intended ({'; '.join(e.message for e in in_err)[:80]})")
        else:
            print(f"{pid}: input valid")
        exp = pair.get("expected_output")
        if exp is not None:
            out_err = dp.check_output(exp)
            for e in out_err:
                problems += 1
                print(f"{pid}: PROBLEM in expected output at {dp.where(e)}: {e.message}")
            if not out_err:
                print(f"{pid}: expected output valid")
        musts = pair.get("expectations", {}).get("must", [])
        if not musts:
            problems += 1
            print(f"{pid}: PROBLEM - no 'must' expectations")
    print(f"problems found: {problems}")
    print("\n== Step 2: coverage matrix ==")
    cols = dp.REQUIRED_CATEGORIES + [f"status:{s}" for s in statuses] + ["rejected"]
    short = lambda c: {"happy_path": "happy", "invalid_input": "invalid", "out_of_scope": "out_scope",
                       "clarification": "clarify"}.get(c, c).replace("status:", "st:").replace(
                           "needs_clarification", "needs_cl")
    print(f"{'pair':<26}" + "".join(f"{short(c):>12}" for c in cols))
    totals = {c: 0 for c in cols}
    for pair in pairs:
        hits = {pair.get("category")}
        exp = pair.get("expected_output")
        hits.add("rejected" if exp is None else f"status:{exp.get('status')}")
        print(f"{(pair.get('pair_id', '?') + ' ' + str(pair.get('category')))[:25]:<26}"
              + "".join(f"{('x' if c in hits else '.'):>12}" for c in cols))
        for c in hits:
            if c in totals:
                totals[c] += 1
    gaps = [c for c in cols if totals[c] == 0]
    print(f"gaps (no pair): {gaps or 'none'}")
    print(f"thin (only one pair): {[c for c in cols if totals[c] == 1] or 'none'}")
    return problems + len(gaps)


def cmd_versions(_):
    rows = dp.version_rows()
    truth = dict(rows)["output schema contract_version const"]
    drift = 0
    for label, value in rows:
        mark = "" if value == truth else "   <- DRIFT"
        drift += bool(mark)
        print(f"{label:<40}{value}{mark}")
    print(f"\nsource of truth (output schema const): {truth}")
    print("ALIGNED: every organ promises the same contract" if not drift
          else f"DRIFT in {drift} place(s): change them in ONE commit, with a CHANGELOG entry")
    return drift


def cmd_gate(_):
    steps = [("instructions", lambda: cmd_check_instructions(argparse.Namespace(file=None))),
             ("schemas", lambda: cmd_check_schemas(None)),
             ("pairs", lambda: cmd_pairs(None)),
             ("versions", lambda: cmd_versions(None)),
             ("manifest", lambda: cmd_dissect(None))]
    results = []
    for name, fn in steps:
        print(f"\n######## {name}")
        try:
            results.append((name, fn()))
        except Exception as e:  # noqa: BLE001
            print(f"ERROR: {e}")
            results.append((name, 1))
    todos = dp.todo_markers()
    print("\n######## summary")
    for name, n in results:
        print(f"  {'PASS' if not n else 'FAIL'}  {name}")
    print(f"  {'PASS' if not todos else 'FAIL'}  no TODO left in agent/ ({len(todos)} found)")
    ok = all(n == 0 for _, n in results) and not todos
    print("DESIGN GATE: PASS" if ok else "DESIGN GATE: FAIL")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="Week 8 Thursday: requirements agent design lab")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("dissect").set_defaults(fn=cmd_dissect)
    s = sub.add_parser("check-instructions"); s.add_argument("file", nargs="?"); s.set_defaults(fn=cmd_check_instructions)
    sub.add_parser("check-schemas").set_defaults(fn=cmd_check_schemas)
    s = sub.add_parser("render"); s.add_argument("input"); s.set_defaults(fn=cmd_render)
    s = sub.add_parser("messages"); s.add_argument("input"); s.add_argument("--full", action="store_true")
    s.set_defaults(fn=cmd_messages)
    s = sub.add_parser("check-input"); s.add_argument("file"); s.set_defaults(fn=cmd_check_input)
    s = sub.add_parser("check-output"); s.add_argument("file"); s.add_argument("--explain", action="store_true")
    s.set_defaults(fn=cmd_check_output)
    sub.add_parser("pairs").set_defaults(fn=cmd_pairs)
    sub.add_parser("versions").set_defaults(fn=cmd_versions)
    sub.add_parser("gate").set_defaults(fn=cmd_gate)
    a = p.parse_args()
    rc = a.fn(a)
    sys.exit(0 if a.cmd != "gate" and not isinstance(rc, int) else (1 if rc else 0))


if __name__ == "__main__":
    main()
