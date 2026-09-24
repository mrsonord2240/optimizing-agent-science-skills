> **Audit record for `bio-admet-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5889856](https://github.com/mrsonord2240/bioSkills/tree/5889856f17650bafa9b1169bafb5dedb97db79d6/chemoinformatics/admet-prediction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0 exact-commit fix pass.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-admet-prediction

Generated: 2026-09-24 · Exact-commit fix re-audit

Source: `mrsonord2240/bioSkills@5889856f17650bafa9b1169bafb5dedb97db79d6:chemoinformatics/admet-prediction`

This replaces the 2026-09-16 report (86/100, Limited Release). The prior report is retained as `eval_viewer_bio-admet-prediction_pre_fix_d91ed3d.md` and its JSON peer. Changed behavior was freshly executed against the exact commit; unchanged findings reuse the recorded 2026-09-16 execution evidence only where a direct diff showed the relevant code/text was unchanged.

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\admet-ai-venv` (ADMET-AI 2.0.1) and its Chemprop 2.3.1 sibling. Exact-commit script: `run/fix_reaudit.py`; captured output: `run/fix_reaudit_5889856.out`. It ran the committed example's loader/gate/predictor; selected hERG, AMES, DILI, BBB and five CYP columns; tested a 300-compound ChEMBL hERG series and nine OOD probes. Chemprop help is retained in `run/chemprop_2_3_1_seed_help_5889856.out`.

## Summary

| Input | Type | Total /100 | Assertions | Status |
|---|---|---:|---:|---|
| 1 | Canonical | 95 | 4/4 PASS | ✅ |
| 2 | Variant A | 90 | 4/4 PASS | ✅ |
| 3 | Variant B | 93 | 4/4 PASS | ✅ |
| 4 | Edge | 96 | 5/5 PASS | ✅ |
| 5 | Stress | 93 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 92 | 4/4 PASS | ✅ |
| 7 | Adversarial | 96 | 5/5 PASS | ✅ |

**Execution average:** 93.6/100 · **Assertions:** 30/30 (100%)

**Static:** 96/100 · **Final:** **95/100 — Production Ready** · Deployable: yes

## Exact-commit evidence

- Primary ADMET-AI route: committed code produced all nine selected endpoints for 293 gate-passing compounds. The 300-row gate retained seven rejected inputs; it did not silently drop them.
- OOD gate: cisplatin and sodium chloride were rejected before prediction. The macrocycle, cyclic peptide, linear peptide, PROTAC-like probe and paclitaxel were retained as `manual_review` rather than presented as confident point predictions.
- Optional ADMETlab result loader: valid contract passed; missing file, absent uncertainty column, and unrelated CSV each raised a named, actionable failure.
- Chemprop: installed 2.3.1 help confirms `--data-seed` and `--pytorch-seed`; the invalid `--seed` advice is gone.

### Input 1 — Offline batch triage with structural alerts and ADMET-AI

Exact-commit source route predicted hERG/AMES/DILI/BBB and 5 CYP endpoints for 293/300 gate-passing organic molecules; 7 are retained as rejects rather than silently dropped.

**Score:** 95/100 · **Assertions:** 4/4 PASS

### Input 2 — Optional ADMETlab hosted-output contract

The service client remains deliberately external to the live official contract; the exact source validates structure, uncertainty and optional task-ID columns and gives named missing-file/contract errors.

**Score:** 90/100 · **Assertions:** 4/4 PASS

### Input 3 — Chemprop custom-endpoint reproducibility

Exact Chemprop 2.3.1 help exposes --data-seed and --pytorch-seed; the obsolete --seed advice is removed. The unchanged prior model-training evidence is reused.

**Score:** 93/100 · **Assertions:** 4/4 PASS

### Input 4 — hERG triage against measured series

The exact source emits hERG predictions after an auditable gate; no point prediction is offered for rejected chemistry and manual-review results remain visible.

**Score:** 96/100 · **Assertions:** 5/5 PASS

### Input 5 — Five-CYP DDI panel

All five documented CYP inhibitor columns were selected successfully from the exact source route; prior 300-compound inhibitor/substrate ambiguity results are unchanged and reused.

**Score:** 93/100 · **Assertions:** 4/4 PASS

### Input 6 — Safety-to-dose request

Unchanged guardrails continue to reject a clinical or regulatory conclusion from a point prediction; pre-fix text evidence is reused after a direct exact-commit diff check.

**Score:** 92/100 · **Assertions:** 4/4 PASS

### Input 7 — OOD metals, salts, macrocycles, peptides and PROTACs

Exact source rejects cisplatin and sodium chloride and sends macrocycles, peptide, PROTAC and paclitaxel to manual review before prediction.

**Score:** 96/100 · **Assertions:** 5/5 PASS

## Veto and conclusion

Skill Veto and Research Veto both PASS. The original P1s are closed: the primary route is executable, and its OOD mitigation is available in the runnable code. The original P2s are closed: ADMETlab results have a real local contract, Chemprop uses current seed flags, and the ADMET-AI compatibility pin is explicitly 2.x. No P0/P1/P2 findings remain open.
