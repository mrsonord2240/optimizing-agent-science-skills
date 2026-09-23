> **Audit record for `bio-microbiome-amplicon-processing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0e9a568](https://github.com/mrsonord2240/bioSkills/tree/0e9a568381ac039886853ff13f167acce8e92229/microbiome/amplicon-processing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0-final-pass-phase2.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-amplicon-processing

Generated: 2026-09-23. Final-pass Phase 2 audit of `mrsonord2240/bioSkills@0e9a568381ac039886853ff13f167acce8e92229:microbiome/amplicon-processing`.

Prior report preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-microbiome-amplicon-processing\`. This final-pass report deliberately records `auditor_independent: false`: fixed and audited under one brief; see `CHECKPOINT.md`.

## Summary

| Input | Scenario | Executed | Basic | Specialized | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Two-run V4 DADA2 example | yes | 39 | 58 | 97 | 4/4 | ✅ |
| 2 | decontam with controls | yes | 39 | 59 | 98 | 4/4 | ✅ |
| 3 | V3-V4 merge budget | yes | 37 | 53 | 90 | 3/3 | ✅ |
| 4 | Real ITS2 ITSxpress | yes | 38 | 57 | 95 | 4/4 | ✅ |
| 5 | Primer-left-on stress | yes | 39 | 57 | 96 | 4/4 | ✅ |
| 6 | Species/OTU scope boundary | yes | 37 | 54 | 91 | 3/3 | ✅ |
| 7 | Abundance-cutoff adversarial case | yes | 38 | 54 | 92 | 3/3 | ✅ |
| 8 | Deterministic repeat | yes | 39 | 57 | 96 | 3/3 | ✅ |
| 9 | truncLen ceiling boundary | yes | 39 | 58 | 97 | 3/3 | ✅ |
| 10 | cutadapt discard-untrimmed | yes | 39 | 57 | 96 | 3/3 | ✅ |
| 11 | QIIME2 Deblur equivalent | yes, errored | 32 | 46 | 78 | 1/3 | ❌ |

Execution average: **93.3/100**. Assertions: **35/37**. Static score: **95/100**. Final score: **94/100, Production Ready, deployable**.

## Execution evidence

All runnable scripts and their assertion logs are in `run/final_pass_20260923/`.

- Input 1: `01_remove_primers.sh` and unchanged `02_dada2_workflow.R` processed ten samples over two runs. Fresh outputs: 11 ASVs, 19,681 reads, 99.5% post-chimera retained.
- Input 2: `04_assert_core.R` verified all eight community ASVs and exactly one kit-contaminant flag from `isContaminant(method='combined')`.
- Input 3: `05_v3v4_budget.py` asserted 28 bp slack for V3-V4 at 2x250 with DADA2's 12 bp merge overlap.
- Input 4: `10_itsxpress_real.sh` fetched public KT459474.1, created 200 overlapping reads, and ran ITSxpress `--region ITS2 --taxa Fungi`; 200 trimmed reads were written.
- Input 5: `06_primers_left_on.R` measured 99.5% versus 68.3% retention when primer removal was the only changed condition.
- Inputs 6–7: `07_scope_and_abundance.py` confirmed taxonomy routing, the non-organism ASV boundary, and the explicitly named abundance-cutoff warning.
- Input 8: independent repeat of the unchanged example plus `08_compare_determinism.R` gave identical ASV dimensions, sequence IDs, and counts.
- Input 9: `09_ceiling_boundary.R` gave 11,974 reads at 231/230, zero at 232/230, and 12,017 at the shipped 220/200 default.
- Input 10: `10_cutadapt_discard_assert.py` found one untrimmed pair discarded and 19,785 retained across ten fresh cutadapt runs.
- Input 11: `11_qiime2_deblur.sh` reached live q2-deblur execution twice, but neither tested artifact produced output after `max() arg is an empty sequence`; this is the lone P2.

## Gates and verdict

Structural veto: **PASS** (stability, contract, determinism, security). Research veto: **PASS** (scientific integrity, practice boundaries, methodological ground, code usability). The optional Deblur error is retained as transparent test evidence and a P2 usability recommendation; it does not invalidate the successfully executed primary DADA2 and ITS code paths.

## Recommendation

- P2 — Add a QIIME2 Deblur preflight that checks read-length suitability and whether reads survive before users encounter q2-deblur's opaque empty-sequence error.
