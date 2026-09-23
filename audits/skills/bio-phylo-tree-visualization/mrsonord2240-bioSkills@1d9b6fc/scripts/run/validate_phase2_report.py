import json
from pathlib import Path

p = Path(r"F:\OpenScience\audits\bio-phylo-tree-visualization\eval_report_bio-phylo-tree-visualization_result.json")
r = json.loads(p.read_text(encoding="utf-8"))
assert r["meta"]["auditor_independent"] is False
assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert r["meta"]["source"].startswith("mrsonord2240/bioSkills@1d9b6fcb44d3e728d78d653e437abfed59ecb55a")
assert len(r["static_score"]["categories"]) == 8
assert sum(v["score"] for v in r["static_score"]["categories"].values()) == r["static_score"]["subtotal"]
inputs = r["dynamic_score"]["inputs"]
assert len(inputs) == r["meta"]["n_inputs"] == 7
assert all(x["executed"] is True and x["execution_note"] for x in inputs)
assert all(3 <= len(x["assertions"]) <= 5 and x["basic"] + x["specialized"] == x["total"] for x in inputs)
assert sum(x["assertions_passed"] for x in inputs) == 21
assert sum(x["assertions_total"] for x in inputs) == 21
assert r["dynamic_score"]["execution_avg"] == round(sum(x["total"] for x in inputs) / 7, 1)
assert r["final"]["score"] == 96 and r["final"]["deployable"] is True and r["final"]["veto_override"] is False
print("report_schema=ok")
