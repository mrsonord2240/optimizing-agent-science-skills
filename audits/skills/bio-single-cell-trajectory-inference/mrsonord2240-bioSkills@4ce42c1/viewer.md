> **Audit record for `bio-single-cell-trajectory-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4ce42c1](https://github.com/mrsonord2240/bioSkills/tree/4ce42c1553b0f2ae3e4c068a8d5f7e1566b5c2d1/single-cell/trajectory-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-trajectory-inference

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@4ce42c1553b0f2ae3e4c068a8d5f7e1566b5c2d1:single-cell/trajectory-inference`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The prior canonical report was preserved before this audit at `F:\OpenScience\audits\_pre-fix-20260923\bio-single-cell-trajectory-inference\`.

Category: Data Analysis | Mode: D (hybrid instructions plus shipped scripts) | Complexity: Complex (N=7)

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Execution |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical: PAGA + DPT | 37 | 56 | 93 | 4/4 | Real Paul15, completed |
| 2 | Variant A: Palantir | 37 | 57 | 94 | 4/4 | Real Paul15, completed |
| 3 | Edge: discrete PBMC | 36 | 54 | 90 | 4/4 | Real PBMC 1k, completed |
| 4 | Variant B: scVelo | 38 | 58 | 96 | 4/4 | Real pancreas, completed |
| 5 | Stress: Slingshot/tradeSeq | 38 | 57 | 95 | 4/4 | Real Paul15, completed |
| 6 | Scope boundary: CellRank | 38 | 57 | 95 | 4/4 | Real Paul15, completed |
| 7 | Adversarial: overclaim boundary | 37 | 57 | 94 | 4/4 | Source-grounded response, completed |

Execution average: **93.9/100**. Assertion pass rate: **28/28 (100%)**.

Static: **95/100**. Final: `95 × 0.4 + 93.9 × 0.6 = 94.3`, reported as **94/100, Production Ready, deployable**. All Production Ready floors pass: static >=80, execution >=85, Layer 1 average 37.3/40, Layer 2 average 56.6/60, assertions >=90%, and no veto.

## Vetoes

Skill Veto T1-T4: PASS. Research Veto M1-M4: PASS. The code paths were syntax-checked and all runnable primary workflows completed. The Skill neither diagnoses individuals nor turns pseudotime into duration; it explicitly frames fate as prediction and single-snapshot dynamics as non-identifiable.

## Executed evidence

1. `run/phase2_input1_paga_dpt.py`: after the exact documented `sc.pl.paga(..., threshold=0.03)` call, PAGA-initialized UMAP and marker-rooted DPT completed on 2,730 Paul15 cells. MEP mean was 0.0332 versus 0.3790 for mature populations.
2. `run/phase2_input2_palantir.py`: Palantir found three terminal states; MEP entropy was 0.6995 and mature entropy 0.0599.
3. `run/phase2_input3_pbmc_boundary.py`: real PBMC 1k gave 15 clusters, 0 isolated at 0.03, 3 at 0.5, and median connectivity 0.2574. This confirms the Skill's warning against a one-threshold continuum decision.
4. `run/phase2_input4_scvelo.py`: the source-faithful deterministic core completed on 3,696 pancreatic cells, mean confidence 0.7126, with Ductal earliest at 0.1301.
5. `run/phase2_input5_slingshot_tradeseq.R`: through the prescribed `tools/rs.sh`, Slingshot found five lineages. `fitGAM` rejected scaled values exactly as documented and succeeded from raw counts with 150 association-test rows.
6. `run/phase2_input6_cellrank.py`: the isolated CellRank environment completed transition matrices, GPCCA, fate probabilities, and lineage drivers. MEP entropy 1.7858 exceeded mature entropy 0.8189. An initial unguarded audit harness failure is retained in `phase2_input6_cellrank.log`; the source script already has the required guard and the guarded rerun is `phase2_input6_cellrank_rerun.log`.
7. `run/phase2_input7_scope_boundary.py`: all four source clauses needed to refuse diagnostic, duration, and overconfident fate claims were present.

The first PAGA run likewise records an audit-transcription omission in `phase2_input1_paga_dpt.log`; `phase2_input1_paga_dpt_rerun.log` is the successful exact source sequence. These are not source failures.

## Static evaluation

| Category | Score |
|---|---:|
| Functional suitability | 12/12 |
| Reliability | 11/12 |
| Performance and context | 8/8 |
| Agent usability | 15/16 |
| Human usability | 8/8 |
| Security | 12/12 |
| Maintainability | 11/12 |
| Agent-specific quality | 18/20 |

## Recommendations

- P2 — Make Scanpy neighbor construction explicit before `scv.pp.moments`; current scVelo reports that automatic neighbor construction will be removed in 0.4.0.
- P2 — Split the generic R install fence into Windows and non-Windows branches so a Windows user sees the supported PAGA/DPT/Slingshot/tradeSeq route before unsupported GitHub-only commands.

No P0 or P1 remains.
