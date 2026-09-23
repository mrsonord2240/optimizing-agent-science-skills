"""Phase 2 Input 7: execute the Skill's no-overclaim decision gate."""
from pathlib import Path

skill = Path(r"F:\OpenScience\wt\single-cell-trajectory-inference\single-cell\trajectory-inference\SKILL.md").read_text(encoding="utf-8")
required = {
    "pseudotime is not elapsed time": "Pseudotime is geometry, not a clock.",
    "single snapshot is non-identifiable": "Snapshot dynamics are formally non-identifiable",
    "fate calls are predictions": "Frame fate calls as predictions, not measurements",
    "mature velocity is invalid": "velocity is invalid here; do not interpret arrows",
}
missing = [name for name, phrase in required.items() if phrase not in skill]
print(f"boundary_clauses_present={len(required) - len(missing)}/{len(required)}; missing={missing}")
print(f"ASSERTION_scope_boundary_refusal_ready={not missing}")
