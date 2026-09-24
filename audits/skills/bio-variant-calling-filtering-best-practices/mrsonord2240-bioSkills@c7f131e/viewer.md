> **Audit record for `bio-variant-calling-filtering-best-practices`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c7f131e](https://github.com/mrsonord2240/bioSkills/tree/c7f131e61134fb550457f761e76bd07dc0a840a8/variant-calling/filtering-best-practices) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0-final-pass.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-variant-calling-filtering-best-practices — final-pass audit

**Result: 91/100 — Production Ready.** Source: `mrsonord2240/bioSkills@c7f131e61134fb550457f761e76bd07dc0a840a8:variant-calling/filtering-best-practices`.

Final-pass declaration: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The previous canonical report and viewer were preserved at `runs/pre-final-20260924/` before this replacement. This report is the canonical raw final-pass record.

## Evidence

Nine archived prompts were replayed in `runs/fp1` through `runs/fp9`; fresh boundary inputs are `runs/fp10` and `runs/fp11`.

| Input | Result | Evidence |
|---|---|---|
| 1 | PASS | Shipped SNP/indel filter example exit 0; all 285 planted true calls survived. |
| 2 | PASS | Guarded bcftools filter retained 25/25 hom-alt calls. |
| 3 | PASS | Small-panel VQSR failure mode reproduced; hard filter retained far fewer artifacts. |
| 4 | PASS | 23 low-quality genotypes nulled without dropping 299 sites. |
| 5 | PASS | End-to-end filtering, BED exclusion, and QC completed. |
| 6 | PASS | DeepVariant route avoids incompatible GATK annotations. |
| 7 | PASS | Tumor sample resolved by exact column index. |
| 8 | PASS | Archived three-layout prompt replayed; the repaired missing-header route is verified separately below. |
| 9 | PASS | Current genotype-level AB branch retains hom-alt calls; no site-level include is recommended. |
| 10 | PASS | Stripped tumor header emits an actionable error and exits before `bcftools` can use `-1`. |
| 11 | PASS | Current cyvcf2 predicate rejects `DP=0` and `MQ=0`; missing and rank-sum-missing records remain eligible. |

`fp11` is an exact-predicate logic execution using an audit VCF-shaped stub, not a cyvcf2 integration claim: cyvcf2 is absent from both currently available runtimes. The prior cyvcf2 package output is preserved with the old evidence.

## Fixes verified

- The somatic block stops cleanly if `##tumor_sample` is missing.
- The usage guide uses genotype-level allele-balance no-calls, retaining hom-alt-only sites.
- The cyvcf2 filter has QD, SOR, and rank-sum safeguards.
- Zero DP/MQ now fail; only missing DP/MQ pass through.

Static: 93/100. Dynamic: 90.3/100 with 44/44 assertions. Weighted final: `93 × 0.4 + 90.3 × 0.6 = 91.4`, rounded to **91**.

Open P0/P1/P2: none in the scoped final-pass findings.
