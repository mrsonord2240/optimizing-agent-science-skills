> **Audit record for `bio-single-cell-multimodal-integration`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4f7306b](https://github.com/mrsonord2240/bioSkills/tree/4f7306b54e8c445d251d352bb85e01ced4c7a3b4/single-cell/multimodal-integration) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-multimodal-integration

## Canonical final summary

**Final:** 91/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@4f7306b54e8c445d251d352bb85e01ced4c7a3b4:single-cell/multimodal-integration`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.
Mode: D · Data Analysis · Complex · 10 inputs

## Result: ⭐ Production Ready — 91/100

This is the fresh final-pass Phase 2 re-audit at the exact pushed source tip.
`auditor_independent` is `false`: the source was corrected and audited under
one final-pass brief. The checkout was clean at both boundaries.

| Input | Route | Total | Assertions | Status |
|---:|---|---:|---:|---|
| 1 | R CITE-seq DSB/WNN | 79 | 3/4 | ⚠️ |
| 2 | totalVI | 86 | 4/4 | ✅ |
| 3 | Multiome WNN | 77 | 3/4 | ⚠️ |
| 4 | Mosaic MultiVI | 87 | 4/4 | ✅ |
| 5 | GLUE capability boundary | 92 | 4/4 | ✅ |
| 6 | Exact Seurat v5 bridge, private R | 100 | 4/4 | ✅ |
| 7 | Exact Python CITE-seq WNN/UMAP | 100 | 4/4 | ✅ |
| 8 | Mosaic and patient-risk boundary | 100 | 4/4 | ✅ |
| 9 | Muon WNN/UMAP regression | 100 | 4/4 | ✅ |
| 10 | Native-versus-private Seurat runtime | 86 | 3/4 | ⚠️ |

Static: **92/100** · Dynamic: **90.7/100** · Assertions: **37/40**.

## Critical fresh evidence

All new evidence is in `run/phase2_reaudit_4f7306b_20260923/`.

- The exact current `examples/cite_seq_analysis.py` ran in the private WSL
  stack (Muon 0.1.9, Scanpy 1.12.4, MuData 0.4.1, leidenalg 0.11.0) on the
  valid 90-cell paired 10x fixture. It exited naturally and wrote the H5MU and
  PDF. Independent readback found a 1,738-nonzero WNN graph, `X_umap` shape
  `(90, 2)`, and three clusters. This verifies the correction from
  `scanpy.tl.umap` to `muon.tl.umap` for MuData WNN metadata.
- The exact current `scripts/seurat_bridge_integration.R` ran in the isolated
  private WSL R runtime and exited zero. Its 150-cell result read back with
  predicted labels/scores and `ref.umap`; mean prediction score was 0.6038.
- The native Windows `rs.sh` Seurat probe was also rerun. It loaded Seurat
  5.5.0 and reached its end marker, then returned **2816**. That remains a
  host teardown fault, not a successful source command; the isolated WSL R
  route is the supported clean execution path.
- The GLUE boundary was rechecked without installing into a shared environment:
  `scglue` is not provisioned in the private runtime, and the response correctly
  requires a supported Linux/macOS host rather than claiming alignment ran.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | Supported Python WNN/UMAP and R bridge processes exit naturally at zero. |
| T2 Contract | PASS | Required source files, frontmatter, documented inputs, and declared outputs are present. |
| T3 Determinism | PASS | Seeded totalVI/MultiVI contracts remain intact; corrected Python WNN source has a fixed UMAP seed. |
| T4 Security | PASS | No credentials, destructive operations, or raw user-code execution. |
| M1 Scientific integrity | PASS | Fixture outputs and host behavior are explicitly labeled. |
| M2 Practice boundaries | PASS | Mosaic inference is distinguished from measurement; individual lupus risk is declined. |
| M3 Methodological ground | PASS | DSB, depth, WNN, and imputation caveats remain explicit. |
| M4 Code usability | PASS | Exact current Python and bridge source routes are clean-output and clean-exit verified in supported private runtimes. |

## Non-blocking follow-ups

- **P2:** retain the private WSL R route while native Windows Seurat teardown
  returns 2816 after successful work.
- **P2:** provision a separate supported `scglue` Linux/macOS environment for
  truth-bearing GLUE alignment and seed-stability execution.

Canonical report: `eval_report_bio-single-cell-multimodal-integration_result.json`.
