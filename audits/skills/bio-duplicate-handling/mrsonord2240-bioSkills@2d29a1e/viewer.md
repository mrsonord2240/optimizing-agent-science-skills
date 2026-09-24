> **Audit record for `bio-duplicate-handling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2d29a1e](https://github.com/mrsonord2240/bioSkills/tree/2d29a1e3460345c6877ecf9f33c58a210ee5c727/alignment-files/duplicate-handling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-duplicate-handling

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-22
Source: `mrsonord2240/bioSkills@2d29a1e3460345c6877ecf9f33c58a210ee5c727:alignment-files/duplicate-handling`

Final-pass Phase 2 fresh audit. The previous report and its entire run directory were preserved at `F:\OpenScience\audits\_pre-fix-2026-09-22\bio-duplicate-handling\`. This report sets `meta.auditor_independent: false`: final pass fixed and audited under one brief; see `F:\OpenScience\audits\_final_pass\bio-duplicate-handling\CHECKPOINT.md`.

Category: Data Analysis | Mode: B | Complexity: Complex | 7 evaluation inputs

## Summary

| Input | Coverage | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---|---|
| 1 | Old canonical: standard samtools, pysam, Picard | 39 | 58 | 97 | 5/5 | ✅ |
| 2 | Old pipeline/example: output cleanup and RNA heuristic | 38 | 58 | 96 | 5/5 | ✅ |
| 3 | Old edge: Common Errors and `-c` | 38 | 58 | 96 | 5/5 | ✅ |
| 4 | Old stress: UMI-tools and fgbio branches | 39 | 58 | 97 | 5/5 | ✅ |
| 5 | Old alternatives: biobambam2, sambamba, samblaster, Picard UMI, mapDamage | 38 | 58 | 96 | 5/5 | ✅ |
| 6 | New: declared RNA-seq and amplicon refusal | 39 | 58 | 97 | 5/5 | ✅ |
| 7 | New: PacBio HiFi synthetic planted truth | 37 | 55 | 92 | 4/5 | ✅ |

Execution average: **95.9/100**. Assertions: **34/35 (97.1%)**. Layer 1 average: **38.3/40**. Layer 2 average: **57.6/60**.

Static score: **92/100**. Final: **92 x 0.4 + 95.9 x 0.6 = 94/100, Production Ready, deployable**. Both vetoes passed; no P0 or P1.

## What ran

All commands were executed from the saved scripts below in WSL `science`, using the `alignment-files` environment plus its documented side environments. Each asserted output is in the logs or generated files under `run/work/`.

| Script / log | Checked results |
|---|---|
| `run/phase2_audit.sh`, `run/phase2_audit.log` | Canonical 100/500 duplicate truth; pysam 100 and 20.00%; Picard 100; shipped pipeline 100 and stats; unset/RNA failures exit 2 and leave no output; RNA override writes a BAM; three verbatim errors; UMI 5689/5646/4042; biobambam2/sambamba/samblaster each 100; RNA and amplicon labels refused; pbmarkdup 12 flags and 48 retained after removal. |
| `run/phase2_old_extra.sh`, `run/phase2_old_extra.stdout.log`, `run/phase2_old_extra.stderr.log` | Picard UMI-aware marking: 10,127 flags. mapDamage `--rescale`: input and output BAM each 5,644 records; `misincorporation.txt` and parsed rescaled BAM written. |
| `run/make_hifi.py` | Deterministic synthetic PacBio-style unaligned BAM: 60 reads with 12 exact planted duplicates. |

Regression coverage re-ran all prior-report use-case families: canonical standard workflow; piped/example workflow; errors and re-marking; shipped assay-gated example; UMI and fgbio on the real UMI BAM; assay decision boundary; and alternate markers including Picard UMI-aware marking and mapDamage. The former planted-duplex scenario is represented by the current duplex-script run; the PacBio synthetic run is a fresh Phase 2 case. Inputs 6 and 7 are new beyond the prior report.

## Gates

- Skill veto: PASS — stable runs, complete frontmatter, deterministic seeded UMI path, and no raw-code execution or credential handling.
- Research veto: PASS — no fabricated scientific claims, no diagnostic or treatment content, assay routing is methodologically appropriate, and every executed code path had a checked output.

## Recommendation

- P2 — Validate `pbmarkdup` on a small real public HiFi amplicon BAM or FASTQ. The deterministic synthetic run proves the documented flags and `--rmdup` behavior, but not real-library performance. This is the sole open item recorded in the final-pass checkpoint.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@2d29a1e3460345c6877ecf9f33c58a210ee5c727:alignment-files/duplicate-handling`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
