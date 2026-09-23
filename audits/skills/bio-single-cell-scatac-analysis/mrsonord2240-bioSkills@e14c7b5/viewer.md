> **Audit record for `bio-single-cell-scatac-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e14c7b5](https://github.com/mrsonord2240/bioSkills/tree/e14c7b581acaa271a9bf643febcb5ff0dd40d966/single-cell/scatac-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-scatac-analysis

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@e14c7b581acaa271a9bf643febcb5ff0dd40d966:single-cell/scatac-analysis`  
Mode: A (direct Skill execution) · Category: Data Analysis · Complexity: Complex (7 inputs)

## Result: ✅ Production Ready — 96/100

This is a fresh final-pass Phase 2 re-audit at the exact pushed tip above. All
executable checks were run in the private isolated WSL runtime, not the known
defective native Windows Signac route. The source checkout was clean at both
boundaries. `auditor_independent` is `false`: this was the requested fixed-and-
audited-under-one-brief pass.

| Input | Type | Total | Assertions | Status |
|---|---|---:|---:|---|
| 1 | Canonical — Signac TF-IDF/LSI and depth diagnosis | 92 | 4/4 | ✅ |
| 2 | Variant A — framework selection for a two-million-cell atlas | 95 | 4/4 | ✅ |
| 3 | Edge — multiple depth-correlated LSI components | 98 | 4/4 | ✅ |
| 4 | Variant B — depth-aware differential accessibility | 98 | 4/4 | ✅ |
| 5 | Stress — exact shipped chromVAR workflow twice | 100 | 4/4 | ✅ |
| 6 | Scope boundary — unsupported local large-atlas execution | 96 | 4/4 | ✅ |
| 7 | Adversarial — causal GATA claim with QC bypass | 98 | 4/4 | ✅ |

Static: **94/100** · Dynamic: **96.7/100** · Passed assertions: **28/28**.

## Execution evidence

All evidence is under `run/phase2_reaudit_e14c7b5_20260923/`.

- The private runtime cleanly loaded Signac **1.17.1**, Seurat **5.5.1**, and
  chromVAR **1.32.0**.
- `01_core_lsi.R` completed TF-IDF/SVD/graph/clustering on 270 cells and 222
  peaks. It diagnosed and removed depth-correlated components **1** and **3**;
  it retained 28 components.
- `03_depth_aware_da.R` completed a 222-row logistic-regression DA result with
  `latent.vars = nCount_peaks`.
- The exact current source `scripts/run_chromvar.R` was invoked twice. Each
  invocation reached natural clean exit, scored **746** motifs across **270**
  cells, and produced a 230-row differential motif table. `cmp` passed for
  both output RDS files and both CSV files; the independent R assertion also
  passed.
- The source R script and Signac example parsed; the SnapATAC2 example compiled
  to an audit-owned `.pyc`, with no source cache created.
- The three direct Mode-A records were validated at natural clean exit. They
  route large-scale work to ArchR/SnapATAC2 without inventing execution and
  reject both causal motif overclaiming and QC bypass.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | All relevant executable routes exited naturally at zero. |
| T2 Contract | PASS | Required frontmatter, examples, script, and output contract are present. |
| T3 Determinism | PASS | Identical reruns from the seeded chromVAR path produced byte-identical RDS and CSV outputs. |
| T4 Security | PASS | No credentials, destructive operations, or raw-user-code execution. |
| M1 Scientific integrity | PASS | Values are traceable to the labeled synthetic fixture or direct response. |
| M2 Practice boundaries | PASS | No clinical inference; causal and QC-bypass requests were rejected. |
| M3 Methodological ground | PASS | Depth filtering, depth-aware DA, GC-matched motif deviations, and interpretation limits were exercised. |
| M4 Code usability | PASS | The exact documented isolated WSL command is process-clean and output-verified. |

## Follow-ups (non-blocking)

- **P2:** retain the isolated WSL/Linux route as the Windows escape hatch until
  a native Windows Signac runtime is independently proven process-clean.
- **P2:** migrate the deprecated QC example to `ATACqc()` only after a supported
  `fragtk` installation is available and compatibility-tested.

Canonical report: `eval_report_bio-single-cell-scatac-analysis_result.json`.
The rejected pre-fix report remains archived at
`F:/OpenScience/audits/_pre-fix-20260923/bio-single-cell-scatac-analysis/rejected-final-pass-0c0ecaa/`.
