import json
from pathlib import Path
p = Path(r"F:\OpenScience\audits\bio-proteomics-spectral-libraries\eval_report_bio-proteomics-spectral-libraries_result.json")
j = json.loads(p.read_text(encoding="utf-8"))
assert set(j) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert j["meta"]["auditor_independent"] is False
assert j["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert j["meta"]["source"] == "mrsonord2240/bioSkills@09467a99deaa8ac30799074803a8b87af6d60858:proteomics/spectral-libraries"
cats = j["static_score"]["categories"]
assert len(cats) == 8 and sum(x["score"] for x in cats.values()) == j["static_score"]["subtotal"] == 96
ins = j["dynamic_score"]["inputs"]
assert len(ins) == j["meta"]["n_inputs"] == 7
for item in ins:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
    assert item["basic"] + item["specialized"] == item["total"]
assert sum(a["result"] == "PASS" for i in ins for a in i["assertions"]) == 28
assert round(sum(i["total"] for i in ins) / len(ins), 1) == j["dynamic_score"]["execution_avg"] == 93.9
assert j["final"] == {"static_weighted": 38.4, "dynamic_weighted": 56.3, "score": 95, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert 2 <= len(j["key_strengths"]) <= 5
assert [x["priority"] for x in j["recommendations"]] == ["P2", "P2"]
print("REPORT_SCHEMA_CHECK=PASS; inputs=7; assertions=28/28; final=95; deployable=true")
