> **Audit record for `bio-single-cell-batch-integration`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@8edc49c](https://github.com/mrsonord2240/bioSkills/tree/8edc49ca40e7eab8a24c1d9555a176ae894e16ac/single-cell/batch-integration) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Exact-commit re-audit — bio-single-cell-batch-integration

Generated: 2026-09-24
Source: `mrsonord2240/bioSkills@8edc49ca40e7eab8a24c1d9555a176ae894e16ac:single-cell/batch-integration`

This is a targeted remediation re-audit of every P1/P2 in the 2026-09-16 audit. It exercises the committed runnable paths and verifies each prose-level correction; the earlier broad seven-prompt method comparison remains available in the preserved pre-fix run files.

| Regression | Result | Evidence |
|---|---|---|
| Harmony script is seeded and runnable | PASS | `run/re_audit_harmony.h5ad`; Harmony converged in 6 iterations |
| scVI/scANVI script pins seed and epochs | PASS | `run/re_audit_scvi.err.log`; both trainers stopped at `max_epochs=2` and emitted `re_audit_scvi.h5ad` |
| Seurat RPCA default is executable | PASS | `run/re_audit_seurat.rds` (5,079,417 bytes), produced by the source script with the 4 GiB future limit |
| Wrapper-only method is actionable | PASS | `FastMNNIntegration is unavailable; ... require SeuratWrappers` |
| Confounded design checks metadata first | PASS | `run/re_audit_policy_checks.py` |
| Scanorama sorting and theta magnitude are stated | PASS | `run/re_audit_policy_checks.py` |
| Shipped paths parse and exist | PASS | Python `py_compile`, R `parse()`, and source-tree reference check |

## Result

**Static: 98/100. Dynamic: 96.0/100. Assertions: 7/7 PASS. Final: 97/100 — Production Ready. Deployable: yes.**

No veto fired and no P0, P1, or P2 remains from the prior audit.

## Fixes verified

- `future.globals.maxSize = 4 * 1024^3` now precedes Seurat RPCA integration and its failure mode is documented.
- SeuratWrappers-only integration methods are no longer represented as built-in bare symbols.
- Harmony gives an observed tuning scale and warns that `theta = 0` remains corrective.
- Scanorama requires stable batch ordering before integration.
- A condition-by-batch cross-tabulation is the decisive confounding guard; cluster cross-tabs only size the visible effect.
- The canonical copied paths are executable scripts with seeds and explicit scVI epoch control.

See `eval_report_bio-single-cell-batch-integration_result.json` for the machine-readable record.
