#!/usr/bin/env python3
"""Usage: make_docs_reaudit.py <run-dir> <extra-md-file>  -> viewer.md from report.json + source-identity.json.
The extra file holds the executed/static-only table, prior-finding dispositions, and the readiness decision (hand-written Markdown)."""
import json
import sys
from pathlib import Path

run = Path(sys.argv[1])
extra = Path(sys.argv[2]).read_text(encoding="utf-8")
r = json.loads((run / "report.json").read_text(encoding="utf-8"))
ident = json.loads((run / "source-identity.json").read_text(encoding="utf-8"))["candidate"]["content_sha256"]
m, f, d, s, v = r["meta"], r["final"], r["dynamic_score"], r["static_score"], r["veto_gates"]
inputs = d["inputs"]
l1 = round(sum(i["basic"] for i in inputs) / len(inputs), 1)
l2 = round(sum(i["specialized"] for i in inputs) / len(inputs), 1)
ap = d["assertion_pass_rate"]
L = [f"# Eval Viewer - {m['skill_name']}", "", f"Generated: {m['evaluated_on']}  ",
     "Audit type: independent final re-audit (certification), fresh auditor  ",
     f"Exact candidate content SHA-256: `{ident}`", "", "## Summary", "",
     "| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |", "|---|---|---:|---:|---:|---:|---|"]
for i in inputs:
    L.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} {i['status']} |")
L += ["", f"**Execution average:** {d['execution_avg']} / 100 (Layer 1 avg {l1} / 40, Layer 2 avg {l2} / 60)  ",
      f"**Assertion pass rate:** {ap['passed']} / {ap['total']} ({round(100 * ap['passed'] / ap['total'], 1)} percent)  ",
      f"**Static score:** {s['subtotal']} / 100  ", f"**Final score:** {f['score']} / 100 - {f['grade_symbol']} {f['grade']}  ",
      f"**Research veto:** {v['research_veto']['gate']}", "", extra.strip(), "", "## Veto review", "",
      f"- Skill veto: {v['skill_veto']['gate']}.", f"- Research veto: {v['research_veto']['gate']}"]
for k in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    L.append(f"  - {k}: {v['research_veto'][k]['result']} - {v['research_veto'][k]['detail']}")
L += ["", "## Static categories", ""]
for k, c in s["categories"].items():
    L.append(f"- {k}: {c['score']}/{c['max']} - {c['note']}")
L += ["", "## Detailed outputs", ""]
for i in inputs:
    L += [f"### Input {i['index']} - {i['type']}: {i['label']}", "", f"**Status:** {i['status']} - {i['note']}  ",
          f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100", "", "**Assertions:**", ""]
    L += [f"- {a['result']} - {a['text']} ({a['note']})" for a in i["assertions"]]
    L.append("")
L += ["## Key strengths", ""] + [f"- {x}" for x in r["key_strengths"]]
L += ["", "## Recommendations", ""]
for x in r["recommendations"]:
    L.append(f"- **[{x['priority']}] {x['title']}** (inputs {x['observed_in']}): {x['problem']} Fix: {x['fix']}")
(run / "viewer.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("ok", l1, l2)
