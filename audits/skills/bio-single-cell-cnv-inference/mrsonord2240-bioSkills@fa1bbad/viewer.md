> **Audit record for `bio-single-cell-cnv-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@fa1bbad](https://github.com/mrsonord2240/bioSkills/tree/fa1bbada93ada3e111be9f85eb0aa62be0ffdbac/single-cell/cnv-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cnv-inference (Phase 2 final pass)

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@fa1bbada93ada3e111be9f85eb0aa62be0ffdbac:single-cell/cnv-inference`
Auditor independence: false — final pass: fixed and audited under one brief, see CHECKPOINT.md

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical | 39/40 | 56/60 | 95/100 | 4/4 PASS | ✅ |
| 2 | Variant A | 38/40 | 56/60 | 94/100 | 4/4 PASS | ✅ |
| 3 | Edge | 38/40 | 56/60 | 94/100 | 4/4 PASS | ✅ |
| 4 | Variant B | 38/40 | 55/60 | 93/100 | 4/4 PASS | ✅ |
| 5 | Stress | 39/40 | 56/60 | 95/100 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 39/40 | 56/60 | 95/100 | 4/4 PASS | ✅ |
| 7 | Adversarial | 39/40 | 57/60 | 96/100 | 4/4 PASS | ✅ |
| 8 | Stress | 38/40 | 56/60 | 94/100 | 4/4 PASS | ✅ |
| 9 | Variant B | 39/40 | 59/60 | 98/100 | 4/4 PASS | ✅ |
| 10 | Adversarial | 39/40 | 57/60 | 96/100 | 4/4 PASS | ✅ |

**Execution average:** 94.9/100
**Assertion pass rate:** 40/40 (100%)
**Vetoes:** Skill Veto PASS; Research Veto PASS
**Final:** 95/100 — ⭐ Production Ready — deployable: true

## Fresh runtime evidence

- `check_cnv_runtime.sh` loaded infercnv 1.22.0, copykat 1.2.5, SCEVAN 1.0.3, and numbat 1.5.2.
- `input1_infercnv_fresh.R` made a new HMM output directory, confirmed the obsolete text output was absent, loaded `run.final.infercnv_obj`, and ranked malignant_cloneA above malignant_cloneB.
- `input2_copykat_fresh.R` ran with `genome='hg20'` and emitted 70 aneuploid plus 80 diploid calls.
- `input4_numbat_columns_fresh.R` confirmed that cM/REF/ALT are rejected when absent and that `gene` is supplied by Numbat's annotation stage.
- `input8_scevan_shipped_fresh.R` ran the source-tree example unchanged; its caught plot failure occurred after classification and the CNA matrix was written.
- `input9_copykat_selector_fresh.R` confirmed hg20 default and hg20/mm10-only branches. The corrective validation therefore supports retaining committed hg20.

## Detailed outputs

### Input 1 — inferCNV reference-based malignant/CNV calling

**Status:** COMPLETED
**Executed:** true
**Execution note:** Fresh inferCNV 1.22.0 HMM run produced run.final.infercnv_obj; the shipped-object path ranked malignant_cloneA above malignant_cloneB.
**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 2 — copyKAT reference-free aneuploid/diploid calling

**Status:** COMPLETED
**Executed:** true
**Execution note:** Fresh copyKAT 1.2.5 run with genome=hg20 returned 70 aneuploid and 80 diploid cells.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 3 — CNV-quiet tumor interpretation

**Status:** COMPLETED
**Executed:** true
**Execution note:** Direct Mode-D response states that an expression-flat profile is not proof of normality and routes confirmation to allele or mutation evidence.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 4 — Numbat allele-aware subclone/LOH preparation

**Status:** COMPLETED
**Executed:** true
**Execution note:** Fresh Numbat 1.5.2 validation rejected the old seven-column frame, accepted the documented ten input columns up to its internal gene annotation step.
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 5 — Per-patient analysis before cross-patient integration

**Status:** COMPLETED
**Executed:** true
**Execution note:** Direct Mode-D response instructs per-patient CNV inference before integration and explains why integrated embeddings can erase private karyotypes.
**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 6 — Sex-matched reference requirement

**Status:** COMPLETED
**Executed:** true
**Execution note:** Direct Mode-D response identifies chrY/XIST/escape-gene artifacts and offers sex matching or sex-chromosome exclusion.
**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 7 — Cancer stage or treatment request from a CNV heatmap

**Status:** COMPLETED
**Executed:** true
**Execution note:** Direct Mode-D response refuses diagnosis and treatment selection, limits output to a research hypothesis, and requests clinical review.
**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 8 — SCEVAN automatic malignant/subclone calling

**Status:** COMPLETED
**Executed:** true
**Execution note:** The unmodified shipped example reached classification, caught the documented post-classification plotting error, and wrote tumor1_CNAmtx.RData.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 9 — copyKAT hg20 selector correction

**Status:** COMPLETED
**Executed:** true
**Execution note:** Fresh copyKAT 1.2.5 namespace inspection found default hg20 and hg20/mm10 branches only; hg19 was absent.
**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

### Input 10 — Unsupported certainty request for a focal event

**Status:** COMPLETED
**Executed:** true
**Execution note:** Direct Mode-D response explains the about-5-Mb expression-CNV resolution limit and refuses to label a focal event or prescribe action.
**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100
**Assertions:** 4/4 PASS — method route, checkable result, CNV caveats, and research-practice boundary all passed.

## Artifact map

- `run/`: every executed script and its captured log.
- `eval_report_bio-single-cell-cnv-inference_result.json`: schema report.
- This viewer: human-readable evidence and scoring.
