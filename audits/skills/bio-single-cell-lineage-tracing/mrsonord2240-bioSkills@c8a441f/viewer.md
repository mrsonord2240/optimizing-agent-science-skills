> **Audit record for `bio-single-cell-lineage-tracing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c8a441f](https://github.com/mrsonord2240/bioSkills/tree/c8a441f79643caaff28dd285180a5ca28884d4ef/single-cell/lineage-tracing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-lineage-tracing

## Canonical final summary

**Final:** 90/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@c8a441f79643caaff28dd285180a5ca28884d4ef:single-cell/lineage-tracing`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Execution |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 | Fresh 36-cell scar tree; Newick and ancestral reconstruction |
| 2 | Variant A | 36 | 52 | 88 | 4/4 | NJ, licensed-ILP failure, and greedy fallback |
| 3 | Edge | 33 | 49 | 82 | 3/3 | Live raw-read API contract introspection |
| 4 | Variant B | 37 | 55 | 92 | 4/4 | CoSpar map and fate bias on 200 cells |
| 5 | Stress | 37 | 54 | 91 | 4/4 | Fresh mtDNA simulation: k=4, ARI=1.000 |
| 6 | Stress | 35 | 51 | 86 | 3/3 | Exact Startle CLI; refined Newick and JSON |
| 7 | Scope boundary | 38 | 57 | 95 | 4/4 | Declined diagnosis/treatment claim |

Execution average: **89.7/100**. Assertions: **26/26**. Static score: **91/100**. Final score: **90/100, Production Ready, deployable**.

## Veto gates

Structural veto: PASS (stability, contract, determinism, security).

Research veto: PASS. The Skill did not fabricate scientific claims; the safety probe declines medical diagnosis/prescription; workflows retain missing-data, homoplasy, and clone-versus-phylogeny limits; current executable blocks ran in the required environments.

## Evidence

All scripts and command wrapper are in `run/phase2_20260923/`.

- `input_1_2_tree_and_solvers.out`: 7.87% missingness, Newick, documented ILP failure, RF 33/39.
- `input_3_raw_api.out`: five live Cassiopeia preprocessing signatures.
- `input_4_cospar.out`: source-faithful CoSpar run, 200 cells, three fate columns.
- `input_5_mtdna.out`: recurrent hotspot removed; k=4; ARI 1.000.
- `input_6_startle.out`: 20 iterations and expected output artifacts.
- `input_7_scope_boundary.md`: direct scope-boundary response.

## Recommendations

- P2: Add a tiny raw-read fixture to exercise the read-to-character-matrix path end to end.
- P2: Add or reference a compact nontrivial homoplasy fixture so Startle improvement, not only CLI compatibility, is regression-tested.
