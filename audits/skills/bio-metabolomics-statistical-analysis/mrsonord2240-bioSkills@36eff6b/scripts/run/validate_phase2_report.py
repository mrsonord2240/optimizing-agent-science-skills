import json
from pathlib import Path

p = Path(r"F:\OpenScience\audits\bio-metabolomics-statistical-analysis\eval_report_bio-metabolomics-statistical-analysis_result.json")
r = json.loads(p.read_text(encoding="utf-8"))
assert r["meta"]["n_inputs"] == len(r["dynamic_score"]["inputs"]) == 11
assert r["meta"]["auditor_independent"] is False
assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert sum(v["score"] for v in r["static_score"]["categories"].values()) == r["static_score"]["subtotal"]
inputs = r["dynamic_score"]["inputs"]
for x in inputs:
    assert x["executed"] is True and x["execution_note"]
    assert 3 <= len(x["assertions"]) <= 5
    assert x["assertions_passed"] == sum(a["result"] == "PASS" for a in x["assertions"])
    assert x["assertions_total"] == len(x["assertions"])
    assert x["basic"] + x["specialized"] == x["total"]
assert r["dynamic_score"]["assertion_pass_rate"] == {"passed": 33, "total": 33}
assert round(sum(x["total"] for x in inputs) / len(inputs), 1) == r["dynamic_score"]["execution_avg"]
assert r["final"]["deployable"] is True and r["final"]["veto_override"] is False
print("REPORT_SCHEMA_AND_FINAL_PASS_METADATA_PASS")
