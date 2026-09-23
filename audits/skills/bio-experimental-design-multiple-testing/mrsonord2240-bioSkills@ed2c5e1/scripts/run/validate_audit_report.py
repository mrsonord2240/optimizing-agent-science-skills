"""Validate required Phase 2 report invariants for this audit artifact."""
from __future__ import annotations

import json
from pathlib import Path
import sys

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert all(row["assertions_passed"] == sum(a["result"] == "PASS" for a in row["assertions"])
           for row in inputs)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 27, "total": 28}
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == 86.4
assert report["final"]["static_weighted"] == 31.2
assert report["final"]["dynamic_weighted"] == 51.8
assert report["final"]["score"] == 83
assert report["final"]["veto_override"] is True and report["final"]["deployable"] is False
print("REPORT_INVARIANTS_PASS")
