"""Build the final-pass audit report from retained exact-commit evidence."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path


AUDIT = Path(r"F:\OpenScience\audits\bio-proteomics-dia-analysis")
SOURCE = Path(r"F:\OpenScience\wt\bio-proteomics-dia-final")
SKILL = "bio-proteomics-dia-analysis"
NOTE = "final pass: fixed and audited under one brief, see CHECKPOINT.md"
COMMIT = subprocess.check_output(["git", "-C", str(SOURCE), "rev-parse", "HEAD"], text=True).strip()

report = {
    "meta": {
        "skill_name": SKILL,
        "evaluated_on": "2026-09-24",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "A",
        "complexity": "Moderate",
        "n_inputs": 9,
        "source": f"mrsonord2240/bioSkills@{COMMIT}:proteomics/dia-analysis",
        "audit_type": "final pass re-audit",
        "auditor_independent": False,
        "note": NOTE,
        "environment": "DIA-NN 2.6.1 archived public outputs; ProteoWizard msconvert 3.0.26253; EasyPQP 0.1.59; pandas 3.0.5; numpy 2.5.3.",
        "execution_note": "Seven archived logical inputs and two fresh inputs were checked by scripts retained in run/finalpass_20260924. The public raw DIA search itself was not rerun because its prior complete execution is multi-hour; its real 2.6.1 report/log were re-filtered with the exact committed source block. The fresh two-stage command check uses a contract stub, not a claim that a new DIA-NN search was completed.",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "detail": "Exact source filter ran deterministically on synthetic 8-run, synthetic 600-run, and public 2.6.1 reports; example validates its two DIA-NN stages and spaced input names."},
        "research_veto": {"applicable": True, "gate": "PASS", "scientific_integrity": {"result": "PASS", "detail": "The final source now states the DIA-NN 2.x separate prediction/search requirement and does not assert a universal matrix-row direction."}, "code_usability": {"result": "PASS", "detail": "Canonical filter, two-stage shell contract, staggered demultiplex command, and EasyPQP library contract were executed or checked against installed tools."}},
    },
    "static_score": {"subtotal": 94, "max": 100, "note": "All prior P1/P2 findings are corrected: two-stage prediction, version-aware matrix interpretation, third-party TSV fragment fields, expanded outputs, de-duplicated runnable command, and a small synthetic Parquet fixture."},
    "dynamic_score": {"execution_avg": 90, "max": 100, "assertion_pass_rate": {"passed": 25, "total": 25}, "note": "Score is deliberately below a fresh end-to-end raw-search maximum because the public raw search was not repeated in this final pass."},
    "inputs": [
        {"id": 1, "type": "archived canonical", "result": "PASS", "evidence": "01_verify_exact_source.out.txt: synthetic 8-run report -> 887x8, LOWCONF=0, no -Inf."},
        {"id": 2, "type": "archived variant", "result": "PASS", "evidence": "01_verify_exact_source.out.txt: public DIA-NN 2.6.1 filter -> 4375x3; pg_matrix 4440, demonstrating no fixed count direction."},
        {"id": 3, "type": "archived edge", "result": "PASS", "evidence": "02_rerun_archived_tools.out.txt: msconvert staggered demultiplex exit 0."},
        {"id": 4, "type": "archived library-build variant", "result": "PASS", "evidence": "02_rerun_archived_tools.out.txt: EasyPQP 0.1.59 library help and documented fragment-field gate."},
        {"id": 5, "type": "archived stress", "result": "PASS", "evidence": "01_verify_exact_source.out.txt: seeded synthetic 600-run report -> 2000x600, FALSE=0, no -Inf."},
        {"id": 6, "type": "archived public predicted-library output", "result": "PASS", "evidence": "01_verify_exact_source.out.txt: exact committed filter re-ran on real 2.6.1 report/log."},
        {"id": 7, "type": "archived public library-based output", "result": "PASS", "evidence": "02_rerun_archived_tools.out.txt: global filter matrix 771x3."},
        {"id": 8, "type": "fresh fixture", "result": "PASS", "evidence": "01_verify_exact_source.out.txt: shipped synthetic Parquet fixture excludes global-only low-confidence group and maps zero to NaN."},
        {"id": 9, "type": "fresh command contract", "result": "PASS", "evidence": "01_verify_exact_source.out.txt: stub observed prediction with no raw --f arguments and stage-two library search preserving a spaced filename."},
    ],
    "findings": {"p0": [], "p1": [], "p2": []},
    "final": {"score": 92, "max": 100, "grade": "Production Ready", "deployable": True, "rationale": "All prior P0/P1/P2 corrections pass. The score retains an execution discount for not re-running the expensive public raw search in this final pass."},
}

assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == NOTE
assert report["final"]["score"] == 92
(AUDIT / f"eval_report_{SKILL}_result.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

viewer = f"""# Skill Audit Viewer — `{SKILL}` (final pass)

**Source:** `mrsonord2240/bioSkills@{COMMIT}:proteomics/dia-analysis`  
**Final score:** **92/100 — Production Ready** · Deployable: **yes**

Final-pass exception: `auditor_independent: false` — {NOTE}

All prior P0/P1/P2 findings are closed. The committed skill now uses a DIA-NN 2.x-compatible two-stage predicted-library route; directs matrix/report discrepancies to the installed run log instead of claiming a fixed direction; names required third-party-library fragment annotations; lists current outputs; keeps the runnable route in one file; and ships a synthetic Parquet fixture.

| Evidence set | Result |
|---|---|
| Archived synthetic report and public DIA-NN 2.6.1 report/log | PASS — exact source filter produced 887x8 and 4375x3 matrices, no `-Inf`; public matrix rows (4440) exceeded globally filtered report rows (4375). |
| Archived 600-run synthetic stress report | PASS — 2000x600, no `FALSE*`, no `-Inf`. |
| Archived staggered data / installed msconvert | PASS — demultiplex command exited 0. |
| Archived EasyPQP and public library-based output | PASS — installed help checked; library report produced 771x3 after global filter. |
| Fresh fixture and command-contract checks | PASS — global-only low-confidence group removed; Stage 1 had no raw files and Stage 2 used the produced library. |

The score is intentionally not higher: this pass did not repeat the prior multi-hour public raw DIA-NN search. It re-filtered the retained real 2.6.1 output and log with the exact committed source block, and the fresh shell test validates argument/stage structure with a stub rather than representing a new raw-data search.

Raw evidence: `run/finalpass_20260924/01_verify_exact_source.py`, `01_verify_exact_source.out.txt`, `02_rerun_archived_tools.py`, `02_rerun_archived_tools.out.txt`, and `easypqp_library_help.txt`.
"""
(AUDIT / f"eval_viewer_{SKILL}.md").write_text(viewer, encoding="utf-8")
print(f"report=PASS commit={COMMIT} score=92 auditor_independent=false")
