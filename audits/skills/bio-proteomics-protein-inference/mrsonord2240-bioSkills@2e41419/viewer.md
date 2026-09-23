> **Audit record for `bio-proteomics-protein-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2e41419](https://github.com/mrsonord2240/bioSkills/tree/2e41419be0f5d52378d18ce545c162a611006a93/proteomics/protein-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-protein-inference

Generated: 2026-09-22  
Source: `mrsonord2240/bioSkills@2e41419be0f5d52378d18ce545c162a611006a93:proteomics/protein-inference`  
Mode: D (hybrid scripts plus direct inference/scope responses) · Complexity: Complex · Inputs: 9

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical: Basic + picked FDR | 39 | 58 | 97 | 4/4 | ✅ |
| 2 | Variant A: Percolator CLI | 38 | 58 | 96 | 4/4 | ✅ |
| 3 | Edge: Philosopher empty guard | 37 | 55 | 92 | 4/4 | ✅ |
| 4 | Variant B: MaxQuant semantics | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | Stress: deep synthetic set | 38 | 58 | 96 | 4/4 | ✅ |
| 6 | Scope Boundary: HYE entrapment | 38 | 57 | 95 | 4/4 | ✅ |
| 7 | Adversarial: patient isoform | 39 | 58 | 97 | 4/4 | ✅ |
| 8 | New: EPIFANY + picked groups | 38 | 58 | 96 | 4/4 | ✅ |
| 9 | New: prefix negative + demo | 38 | 57 | 95 | 4/4 | ✅ |

Execution average: **95.6 / 100** · Assertions: **36/36** · Layer 1 mean: **38.1/40** · Layer 2 mean: **57.4/60**.

## Evidence run

All scripts executed this audit are in [`run`](run/). Shipped scripts were copied there before execution; the Skill worktree was not imported from or written to. Generated tables and complete command output are in [`run/outputs`](run/outputs/).

- Basic OpenMS route: `556` passing groups at 1% picked group FDR; TSV has group membership and q-values.
- Real Percolator 3.09.0: output check found `458` rows at q<=0.01 in `prot.target.tsv`.
- Philosopher 5.1.0: processed `6,135` results but `grep` found `0` `peptideprophet_result` elements. The reference guard emitted `PeptideProphet modelled 0 PSMs` and returned 1 as intended.
- Deep synthetic replay: unfiltered targets had 6.96% true FDP; 6,564 picked 1% groups had 0.90% true FDP.
- EPIFANY: 749 groups, all parsed posterior values in [0, 1]; picked-group companion emitted 586 target groups.
- Wrong `REV__` prefix against `DECOY_` data raised the documented `ValueError`.

## Veto gates

Skill veto T1–T4: **PASS**. Research veto M1–M4: **PASS**. The clinical adversarial request was not answered as a diagnosis; it was routed to a validated PRM/MRM assay on isoform-unique peptides.

## Limitation and recommendation

**P1 — positive Philosopher/ProteinProphet verification:** The Skill correctly protects against the local silent-empty failure, but no compatible local pepXML produces a nonempty positive chain. Verify it in a compatible Philosopher/TPP environment before relying on that optional route. Sam's decision prohibits retrying standalone TPP installation.

## Final result

Static: 93/100 × 0.4 = 37.2  
Dynamic: 95.6/100 × 0.6 = 57.4  
**Final: 95/100 · ⭐ Production Ready · deployable: true · veto: none.**

`meta.auditor_independent` is `false`; note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`.
