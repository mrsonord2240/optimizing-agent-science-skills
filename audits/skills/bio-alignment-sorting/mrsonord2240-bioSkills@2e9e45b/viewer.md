> **Audit record for `bio-alignment-sorting`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2e9e45b](https://github.com/mrsonord2240/bioSkills/tree/2e9e45b14f0a4aa092765f484a020fe3af39e712/alignment-files/alignment-sorting) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-sorting

Generated: 2026-09-24  
Source: `mrsonord2240/bioSkills@2e9e45b14f0a4aa092765f484a020fe3af39e712:alignment-files/alignment-sorting`

Final-pass status: this is a combined fixer/auditor pass. `auditor_independent: false`; see `F:\OpenScience\audits\_final_pass\bio-alignment-sorting\CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical coordinate sort | 38 | 58 | 96 | 4/4 | ✅ |
| 2 | Variant A name sort / Picard | 38 | 58 | 96 | 4/4 | ✅ |
| 3 | Edge sort orders / malformed files | 38 | 57 | 95 | 4/4 | ✅ |
| 4 | Variant B merge | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | Stress downstream / performance | 37 | 57 | 94 | 4/4 | ✅ |
| 6 | Scope Boundary fresh order helper | 39 | 59 | 98 | 4/4 | ✅ |
| 7 | Adversarial fresh pipeline failures | 39 | 59 | 98 | 4/4 | ✅ |

Execution average: **96.1 / 100**. Assertion pass rate: **28 / 28**.

Static score: **94 / 100**. Final score: **95 / 100 — ⭐ Production Ready**. No veto fired; deployable: **true**.

## Evidence

All seven archived input groups were rerun from `run/`: `in01_coordinate.sh`, `in02_namesort_dup.sh`, `in03_edge.sh`, `in04_merge.sh`, the input-5 scripts, `in06_record_order_check.sh`, and `in07_pipeline_real_hostile.sh`. The input-5 timing helper emits Python formatting errors while formatting its timing summary; its actual samtools checks completed, and the issue is confined to the archived audit harness rather than the source skill.

Two new source-tip inputs were run after commit `2e9e45b`:

- `run/finalpass_in08_source_order_checks.sh` extracted the committed helper and verified sorted, shuffled, uBAM, CRAM-with-reference, existing-directory `-T`, and `-@` behavior.
- `run/finalpass_in09_source_pipeline_checks.sh` verified single-end threads, invalid-thread rejection, and preservation of a valid BAM across unequal-mate failure.

## Detailed outputs

### Input 1 — coordinate sort

Shuffled real BAM (5,644 records), 1000 Genomes BAM (9,601), and no-`@HD` UMI BAM (15,788) sorted correctly, preserved their multisets, and indexed. CRAM output and CSI creation succeeded.

### Input 2 — name sort and Picard

`-n` was natural and `-N` ASCII. Picard rejected natural order when it differed from ASCII, accepted `-N`, and accepted a fixed-width case where the orders coincided. The updated rule states precisely that distinction.

### Input 3 — edge conditions

Tag and template-coordinate headers matched the skill. Indexing rejected non-coordinate orders. The record walk caught lying headers and `ensure_coordinate_sorted` repaired them.

### Input 4 — merge

Merge preserved valid records but did not validate a mismatched source order. The RG-collision warning reproduced, and `merge -n`/`merge -N` produced natural/ASCII order respectively.

### Input 5 — downstream and performance

The rerun confirmed CMCR accepts GroupReadsByUmi template-coordinate output but rejects coordinate and MI-tag ordering; Mutect2 completed only for coordinate-sorted indexed input. Existing-directory `-T` created temporary files inside the directory and cleaned them up. Local versus network storage changed collate performance, supporting the qualified text.

### Input 6 — fresh source-tip helper

The committed `is_coordinate_sorted` returned True for coordinate BAM and CRAM with `reference_filename`, False for shuffled BAM, and False (rather than raising) for a uBAM without `@SQ`.

### Input 7 — fresh source-tip pipeline

The committed example accepted `ref r1 output 3` as single-end threads. `abc` was rejected before publication; unequal mates failed the primary-record check without overwriting the pre-existing valid BAM and without leaving a temporary destination.

## Recommendations

None. All six recommendations from the prior canonical report were fixed and rechecked.
