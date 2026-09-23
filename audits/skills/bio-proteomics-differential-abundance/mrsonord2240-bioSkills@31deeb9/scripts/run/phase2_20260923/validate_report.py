"""Validate the emitted Phase-2 report contract and evidence paths."""
import json, pathlib, sys
if len(sys.argv) != 2: raise SystemExit("usage: validate_report.py <audit-dir>")
a=pathlib.Path(sys.argv[1])
r=json.loads((a/"eval_report_bio-proteomics-differential-abundance_result.json").read_text(encoding="utf-8"))
assert r["meta"]["auditor_independent"] is False
assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert r["meta"]["source"] == "mrsonord2240/bioSkills@31deeb9912f6e318ed11069f05a55be98577ff5e:proteomics/differential-abundance"
assert r["source"] == "mrsonord2240/bioSkills@31deeb9912f6e318ed11069f05a55be98577ff5e:proteomics/differential-abundance"
ins=r["dynamic_score"]["inputs"]; assert len(ins)==13 and all("executed" in x and "execution_note" in x for x in ins)
assert sum(x["assertions_passed"] for x in ins)==37 and sum(x["assertions_total"] for x in ins)==39
assert round(sum(x["total"] for x in ins)/len(ins),1)==r["dynamic_score"]["execution_avg"]
assert r["final"]["score"]==round(r["final"]["static_weighted"]+r["final"]["dynamic_weighted"])
assert r["final"]["deployable"] is True and r["final"]["veto_override"] is False
assert (a/"eval_viewer_bio-proteomics-differential-abundance.md").exists()
assert (a/"run"/"phase2_20260923"/"input1_3_5_8_10_11.log").exists()
print("REPORT_VALID score=%s deployable=%s executed=%d/%d assertions=37/39" % (r["final"]["score"],r["final"]["deployable"],sum(x["executed"] for x in ins),len(ins)))
