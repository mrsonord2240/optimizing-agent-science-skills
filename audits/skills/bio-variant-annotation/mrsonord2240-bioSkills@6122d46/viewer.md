> **Audit record for `bio-variant-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6122d46](https://github.com/mrsonord2240/bioSkills/tree/6122d469f440f6030b278a155d8e4e78c8788dbf/variant-calling/variant-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final-pass audit — bio-variant-annotation

Source audited: `mrsonord2240__bioSkills` commit `6122d469f440f6030b278a155d8e4e78c8788dbf` on `agent/finalpass-bio-variant-annotation-20260924`.

Final score: **91/100 — Production Ready (self-audited)**.

Final-pass disclosure: `auditor_independent=false`. The operator who made the correction audited this exact commit, so this is useful execution evidence but not independent acceptance evidence.

## Corrected finding

| Priority | Finding | Correction | Result |
|---|---|---|---|
| P2 | `examples/annotate_vcf.sh` used undeclared `bc` for its final percentage. In the supported bcftools 1.24 Windows environment, the pipeline succeeded but printed `With rsID: 7 (%)`. It also silently skipped a nonexistent `GNOMAD_VCF`; `bcftools annotate` can exit 0 on a full `chr1`/`1` contig mismatch. | Replaced `bc` with `awk`; require indexed target/source VCFs; reject a set-but-missing `GNOMAD_VCF`; reject no shared input/gnomAD contigs; document the index and contig preflight in the usage guide. | Fixed and exercised below. |

No P0, P1, or P2 finding remains open in the audited scope.

## Execution evidence

All tests used synthetic data from `data/` and bcftools 1.24 in `F:/OpenScience/audit-envs/variant-annotation-curation-analyst/msys`.

| Type | Case | Result | Raw evidence |
|---|---|---|---|
| Archived regression | Current SKILL.md canonical csq → dbSNP → indexed gnomAD block | 12 split records; 8 rsIDs; 7 gnomAD FAF values; rc=0 | `runs/finalpass_archived_canonical/out.txt` |
| Archived regression | Rare-variant recipe | Annotation and csq pipeline exit 0; cohort AF stays 0.5; absent gnomAD variants remain | `runs/p_in3/finalpass_out.txt` |
| Archived regression | csq phase-mode edge | Observed `-p a`, `-p s`, and `-p m` behavior agrees with the corrected guidance | `runs/in9/finalpass_out.txt` |
| Fresh | Valid helper without `bc` | 11 variants; 7 rsIDs; correct `63.6%`; rc=0 | `runs/finalpass_fresh_valid/out.txt` |
| Fresh | `chr1` input vs `1` gnomAD source | Explicit no-shared-contigs error; rc=1, no false success | `runs/finalpass_fresh_mismatch/out.txt` |
| Fresh | Unindexed target | Explicit indexing instruction; rc=1 | `runs/finalpass_fresh_unindexed/out.txt` |
| Fresh | Invalid `GNOMAD_VCF` path | Explicit path error; rc=1 | `runs/finalpass_fresh_badenv/out.txt` |

## Scope and limits

- The final pass did not rerun VEP with a production cache, SnpEff, or ANNOVAR: required databases/registration were unavailable.
- The archived cyvcf2 parser fixture could not run because the dedicated Windows environment lacks `cyvcf2` and the agents WSL runtime lacks `python`; that parser was not changed by the audited commit.
- The score is deliberately capped at 91 because this is a self-audit and those unchanged integration paths were not re-executed.

The raw machine-readable result is `eval_report_bio-variant-annotation_result.json` beside this viewer.
