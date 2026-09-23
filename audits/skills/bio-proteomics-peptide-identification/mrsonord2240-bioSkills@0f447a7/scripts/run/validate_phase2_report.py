"""Phase-2 report contract check; the environment validator is date-pinned to 2026-09-11."""
import json
from pathlib import Path

p = Path(r"F:\OpenScience\audits\bio-proteomics-peptide-identification\eval_report_bio-proteomics-peptide-identification_result.json")
r = json.loads(p.read_text(encoding="utf-8"))
assert r["meta"]["evaluated_on"] == "2026-09-22"
assert r["meta"]["source"] == "mrsonord2240/bioSkills@0f447a7a628052aac81acecb85c3d52d442a974a:proteomics/peptide-identification"
assert r["meta"]["auditor_independent"] is False
assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert set(r) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert len(r["dynamic_score"]["inputs"]) == 12
assert all(x["executed"] for x in r["dynamic_score"]["inputs"])
assert all(3 <= len(x["assertions"]) <= 5 for x in r["dynamic_score"]["inputs"])
assert r["dynamic_score"]["assertion_pass_rate"] == {"passed": 46, "total": 46}
assert r["final"] == {"static_weighted": 38.0, "dynamic_weighted": 56.8, "score": 95, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
print("ASSERT report: exact source, Phase-2 meta exception, 12 executed inputs, 46/46 assertions, 95 Production Ready")
