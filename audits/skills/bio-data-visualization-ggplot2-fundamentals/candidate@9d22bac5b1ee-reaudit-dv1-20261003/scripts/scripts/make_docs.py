#!/usr/bin/env python3
"""Usage: make_docs.py <run-dir> <ID-PREFIX> <executed-md-file>  -> viewer.md, finding-ledger.md from report.json"""
import json
import sys
from pathlib import Path

run = Path(sys.argv[1])
r = json.loads((run / "report.json").read_text(encoding="utf-8"))
executed = Path(sys.argv[3]).read_text(encoding="utf-8")
ident = json.loads((run / "source-identity.json").read_text(encoding="utf-8"))["candidate"]["content_sha256"]
m, f, d, s, v = r["meta"], r["final"], r["dynamic_score"], r["static_score"], r["veto_gates"]
L = [f"# Eval Viewer — {m['skill_name']}", "", f"Generated: {m['evaluated_on']}  ",
     "Audit type: final independent re-audit (certification run) of the fixed candidate  ", f"Exact candidate content SHA-256: `{ident}`", "",
     "## Summary", "", "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |", "|---|---|---:|---:|---:|---:|---|"]
for i in d["inputs"]:
    L.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} {i['status']} |")
ap = d["assertion_pass_rate"]
L += ["", f"**Execution average:** {d['execution_avg']} / 100  ", f"**Assertion pass rate:** {ap['passed']} / {ap['total']}  ",
      f"**Static score:** {s['subtotal']} / 100  ", f"**Final score:** {f['score']} / 100 — {f['grade_symbol']} {f['grade']}  ",
      f"**Research veto:** {v['research_veto']['gate']}", "",
      "Readiness decision: **not candidate-ready** (GG-004 P1 still open; assertion pass rate 26/29 = 89.7 % is under the 90 % gate). Exact identity is in [`source-identity.json`](source-identity.json).", "",
      "## Prior findings (initial audit 34a174ab0263)", "", Path(run / "verdicts.md").read_text(encoding="utf-8").strip(), "",
      "## Executed versus static-only", "", executed.strip(), "", "## Veto review", "",
      f"- Skill veto: {v['skill_veto']['gate']} (stability, contract, determinism, security all {v['skill_veto']['stability']}).",
      f"- Research veto: {v['research_veto']['gate']}"]
for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    L.append(f"  - {k}: {v['research_veto'][k]['result']} — {v['research_veto'][k]['detail']}")
L += ["", "## Static categories", ""]
for k, c in s["categories"].items():
    L.append(f"- {k}: {c['score']}/{c['max']} — {c['note']}")
L += ["", "## Detailed outputs", ""]
for i in d["inputs"]:
    L += [f"### Input {i['index']} — {i['type']}: {i['label']}", "", f"**Status:** {i['status']} — {i['note']}  ",
          f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100", "", "**Assertions:**", ""]
    L += [f"- {a['result']} — {a['text']} ({a['note']})" for a in i["assertions"]]
    L.append("")
L += ["## Key strengths", ""] + [f"- {x}" for x in r["key_strengths"]]
L += ["", "## Recommendations", ""]
for x in r["recommendations"]:
    L.append(f"- **[{x['priority']}] {x['title']}** (inputs {x['observed_in']}): {x['problem']} Fix: {x['fix']}")
(run / "viewer.md").write_text("\n".join(L) + "\n", encoding="utf-8")
led = [f"# Ordered finding ledger — {m['skill_name']}", "", f"Audited identity: `{ident}`", "",
       "| Order | ID | Priority | State | Evidence inputs | Required disposition |", "|---:|---|---|---|---|---|"]
for n, x in enumerate(r["recommendations"], 1):
    fid, title = x["title"].split(" ", 1)
    led.append(f"| {n} | {fid} | {x['priority']} | open | {x['observed_in']} | {title}. {x['fix']} |")
led += ["", "GG-001, GG-002, GG-003, GG-005, GG-007 and GG-008 are corrected and not listed. No audit-local repair was made; no Skill bytes changed."]
(run / "finding-ledger.md").write_text("\n".join(led) + "\n", encoding="utf-8")
print("ok")

L += ["", "## Ordered finding ledger", ""] + led[2:]
(run / "viewer.md").write_text(chr(10).join(L) + chr(10), encoding="utf-8")
