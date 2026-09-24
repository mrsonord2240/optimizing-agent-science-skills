#!/usr/bin/env python3
"""Writes eval_viewer_bio-long-read-splicing.md from the JSON report (scores, assertions) plus the per-input run details below (numbers quoted from run/logs)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
d = json.load(open(os.path.join(ROOT, "eval_report_bio-long-read-splicing_result.json"), encoding="utf-8"))
ins = d["dynamic_score"]["inputs"]; f = d["final"]; st = d["static_score"]
n = len(ins); L1 = sum(i["basic"] for i in ins) / n; L2 = sum(i["specialized"] for i in ins) / n
ap = d["dynamic_score"]["assertion_pass_rate"]
DETAIL = json.load(open(os.path.join(HERE, "viewer_details.json"), encoding="utf-8"))
o = []
o.append("# Eval Viewer - bio-long-read-splicing (SECOND RE-AUDIT of the fixed Skill)\n")
o.append("Generated: 2026-09-20  ")
o.append("Source: `mrsonord2240/bioSkills@887eaeddf09532feee6caaf5f325d0c9b3ce7101:alternative-splicing/long-read-splicing` (fix branch `fix/as-longread`, round 2 on top of c07c53c). Read from the worktree, run from a copy in `run/skill_copy/` (sha1 of SKILL.md, usage-guide.md and the example identical to the worktree; nothing written into the worktree, `external\\` or `public-data\\`).  ")
o.append("Previous: first re-audit 80, Limited Release, 2 open P1 (`_pre-fix-20260920b`); original audit 68, Reject (`_pre-fix-20260920`).  ")
o.append("Category 3 Data Analysis, mode D (hybrid), Complex, N = 8. The fix log was read for orientation only; every number below comes from my own runs (logs in `run/logs/`, scripts in `run/`).\n")
o.append("**Result: static %d, execution average %.1f, final %d, %s, deployable %s, no veto, no open P0, no open P1, 5 P2.**  " % (st["subtotal"], d["dynamic_score"]["execution_avg"], f["score"], f["grade"], str(f["deployable"]).lower()))
o.append("Layer averages: L1 %.1f/40, L2 %.1f/60, assertions %d/%d (%.0f%%). Floors for Limited Release met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%%); Production Ready floors not met (static %d < 80)." % (L1, L2, ap["passed"], ap["total"], 100.0 * ap["passed"] / ap["total"], st["subtotal"]))
o.append("\n## Summary table\n")
o.append("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|")
for i in ins:
    o.append("| %d | %s - %s | %d | %d | %d | %d/%d | %s |" % (i["index"], i["type"], i["label"], i["basic"], i["specialized"], i["total"], i["assertions_passed"], i["assertions_total"], i["status_flag"]))
o.append("\n**Execution average %.1f / 100.** Static %d x 0.4 = %.1f; dynamic %.1f x 0.6 = %.1f; %.1f -> **%d**.\n" % (d["dynamic_score"]["execution_avg"], st["subtotal"], f["static_weighted"], d["dynamic_score"]["execution_avg"], f["dynamic_weighted"], f["static_weighted"] + f["dynamic_weighted"], f["score"]))
o.append(DETAIL["intro"])
o.append("\n## Research Veto, re-judged\n\n| | Result | Evidence |\n|---|---|---|")
rv = d["veto_gates"]["research_veto"]
for k, lab in (("scientific_integrity", "M1 Scientific integrity"), ("practice_boundaries", "M2 Practice boundaries"), ("methodological_ground", "M3 Methodological baseline"), ("code_usability", "M4 Code usability")):
    o.append("| %s | %s | %s |" % (lab, rv[k]["result"], rv[k]["detail"]))
o.append("\n## Regression: what the first re-audit found and what changed\n")
o.append(DETAIL["regression"])
o.append("\n---\n")
for i in ins:
    dd = DETAIL["inputs"][str(i["index"])]
    o.append("## Input %d - %s: %s\n" % (i["index"], i["type"], i["label"]))
    o.append("**Prompt:** %s\n" % dd["prompt"])
    o.append("**Ran:** %s\n" % dd["ran"])
    o.append("**Printed (trimmed):**\n```\n%s\n```" % dd["printed"])
    o.append("**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100 %s\n" % (i["basic"], i["specialized"], i["total"], i["status_flag"]))
    o.append("**Assertions:**")
    for a in i["assertions"]:
        o.append("- [%s] %s - %s" % (a["result"], a["text"], a["note"]))
    if dd.get("after"): o.append("\n" + dd["after"])
    o.append("\n---\n")
o.append("## Other checks\n")
o.append(DETAIL["other"])
o.append("\n## Recommendations\n")
for r in d["recommendations"]:
    o.append("**%s** %s (inputs %s): %s Fix: %s\n" % (r["priority"], r["title"], r["observed_in"], r["problem"], r["fix"]))
o.append("## Scripts (all in `run/`)\n")
o.append(DETAIL["scripts"])
open(os.path.join(ROOT, "eval_viewer_bio-long-read-splicing.md"), "w", encoding="utf-8", newline="\n").write("\n".join(o) + "\n")
print("viewer written")
