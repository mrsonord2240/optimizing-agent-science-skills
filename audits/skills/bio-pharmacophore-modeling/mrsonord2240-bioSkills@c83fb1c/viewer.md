> **Audit record for `bio-pharmacophore-modeling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c83fb1c](https://github.com/mrsonord2240/bioSkills/tree/c83fb1c4c8c3c40079e8cf653c3ed266fa7b1d8c/chemoinformatics/pharmacophore-modeling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pharmacophore-modeling (FINAL PASS PHASE 2)

Generated: 2026-09-22
Source: `mrsonord2240/bioSkills@c83fb1c4c8c3c40079e8cf653c3ed266fa7b1d8c:chemoinformatics/pharmacophore-modeling`
Status: final-pass exception — `auditor_independent: false`; see `F:\OpenScience\audits\_final_pass\bio-pharmacophore-modeling\CHECKPOINT.md`.

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The prior Phase-1/re-audit record was preserved at `F:\OpenScience\audits\_pre-fix-20260922\bio-pharmacophore-modeling\`. This audit used fresh scripts under `run/`; no source file was modified.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Execution |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical: 1HSG PLIP regression | 38 | 56 | 94 | 4/4 | ✅ |
| 2 | Variant A: strict/relaxed real-drug filtering | 37 | 55 | 92 | 5/5 | ✅ |
| 3 | Edge: verbatim RDKit embedding block | 38 | 56 | 94 | 4/4 | ✅ |
| 4 | Variant B: shipped demo twice | 39 | 56 | 95 | 4/4 | ✅ |
| 5 | Stress: ten-drug library | 36 | 54 | 90 | 4/4 | ✅ |
| 6 | Scope: 3PTB PLIP regression | 37 | 56 | 93 | 4/4 | ✅ |
| 7 | Adversarial + new validation edge | 36 | 55 | 91 | 4/4 | ✅ |

Execution average: **92.7/100**. Assertions: **29/29**.

## What ran

- `01_plip_1hsg.py`: real 1HSG, documented PLIP workaround → hbond 6, hydrophobic 15, saltbridge 2, waterbridge 4.
- `02_relaxation.py`: prior real drug route plus a new `min_shared_fraction=0.6` case → strict `[]`; relaxed includes ritonavir while caffeine/metformin remain out. Aspirin and acetaminophen also pass, as expected for a coarse prefilter and explicitly requiring a 3D follow-up.
- `03_embed_block.py`: the SKILL.md RDKit application block → `CAN_MATCH True`, `EMBEDDINGS 10`, `N_FAILED 0`.
- archived exact source `04_pharmacophore_demo_source.py`: shipped demo twice → same one-member hit list and identical complete stdout SHA-256.
- `05_stress.py`: prior ten-drug test → 10 processed, 6 hits, 4 typed rejections.
- `06_plip_3ptb.py`: real 3PTB → 9 typed records (`hbond`, `hydroph_interaction`, `metal_complex`).
- `07_enrichment.py`: new quality-validation boundary → `inf` when no inactive matches; clear `ValueError` for an empty active class.
- `08_documentation_checks.py`: prior scope/false-premise checks → placeholder warning placement and both scope corrections present.

All command output and assertion evidence are saved in `run/*.out.txt`; `run_all.ps1` is the reproducible orchestration script.

## Gates and score

Skill Veto: T1/T2/T3/T4 **PASS**. Research Veto: M1/M2/M3/M4 **PASS**.
Static: **90/100 × 0.4 = 36.0**. Dynamic: **92.7/100 × 0.6 = 55.6**.
Final: **92/100 — ⭐ Production Ready — deployable: true**. No P0, P1, or P2 recommendation remains.
