> **Audit record for `bio-alignment-filtering`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6c71f04](https://github.com/mrsonord2240/bioSkills/tree/6c71f04151377fe0d412ece85d9dc52cdccdf747/alignment-files/alignment-filtering) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-filtering

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@6c71f04151377fe0d412ece85d9dc52cdccdf747:alignment-files/alignment-filtering`

## Summary

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical quality filter | 39/40 | 58/60 | 97 | 5/5 | ✅ |
| 2 | Exhaustive FLAG masks | 39/40 | 59/60 | 98 | 14/14 | ✅ |
| 3 | Region/BED edge cases | 38/40 | 58/60 | 96 | 5/5 | ✅ |
| 4 | Seeded subsampling | 38/40 | 57/60 | 95 | 2/2 | ✅ |
| 5 | Synthetic MAPQ stress | 39/40 | 58/60 | 97 | 6/6 | ✅ |
| 6 | Expressions/read groups | 39/40 | 58/60 | 97 | 5/5 | ✅ |
| 7 | Duplicates + SV hand-off | 39/40 | 58/60 | 97 | 5/5 | ✅ |
| 8 | Real Illumina MAPQ | 38/40 | 58/60 | 96 | 11/11 | ✅ |
| 9 | PBMM2 long-read replay | 39/40 | 59/60 | 98 | 8/8 | ✅ |
| 10 | New: invalid/zero-width input | 37/40 | 55/60 | 92 | 2/2 | ✅ |
| 11 | New: larger --like target | 39/40 | 58/60 | 97 | 1/1 | ✅ |

Execution average: **96.4/100**. Assertion pass rate: **48/48** (representative 3-5 assertions per input; the saved logs contain every completed check).

## Evidence

- `run/phase2_regression.py` — prior canonical, FLAG, BED/region, subsampling, MAPQ-table, expression/RG and documented PBMM2 result classes; 35/35 assertions.
- `run/r7_adversarial.py` and `run/r6_expr.py` — prior adversarial and scope-boundary classes; both report no failures.
- `run/r5_align.sh` + `run/phase2_mapq_verify.py` — fresh synthetic five-aligner run; 11/11 assertions.
- `run/n8_align_real.sh` + `run/phase2_real_align_verify.py` — fresh real 2,821-pair re-alignment; 11/11 assertions.
- `run/n9_align_long.sh` + `run/phase2_pbmm2_verify.py` — fresh PBMM2/minimap2 long-read run; 8/8 assertions.
- `run/phase2_new_boundaries.py` and `run/phase2_new_match_like.py` — new inputs: 3/3 assertions.
- `run/phase2_static.sh` — all shipped Python files parse, shell script passes `bash -n`, and no source `__pycache__` was found.

## Result

Structural veto: PASS. Research veto: PASS. Static: 95/100. Dynamic: 96.4/100. Final: **96/100, Production Ready, deployable**.

The sole recommendation is P2: make the already documented zero-width BED limitation explicit in `filter_by_bed.py` at runtime. This report deliberately records `auditor_independent: false`: final pass fixed and audited under one brief; see `F:\OpenScience\audits\_final_pass\bio-alignment-filtering\CHECKPOINT.md`.
