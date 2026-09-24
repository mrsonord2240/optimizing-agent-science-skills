> **Audit record for `bio-pileup-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3eac20f](https://github.com/mrsonord2240/bioSkills/tree/3eac20f00989e1b287984d13e92c59e7ff5c86a2/alignment-files/pileup-generation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pileup-generation

Generated: 2026-09-24 · rendered from the final-pass audit report.

Source: `mrsonord2240/bioSkills@3eac20f00989e1b287984d13e92c59e7ff5c86a2:alignment-files/pileup-generation`

Final pass: fixed and audited under one brief. The source fixer performed this
audit (`auditor_independent: false`).

## Result

**95/100 — ⭐ Production Ready — deployable**

- Static: 94/100
- Dynamic: 96.0/100
- Assertions: 27/27 summarised audit assertions passed
- Inputs: 9/9 executed
- Veto gates: PASS
- Recommendations: none

## Evidence summary

| Input | Coverage | Result |
|---|---|---|
| 1 | Archived real text pileup, defaults, output format, pysam table | 28/28 checks pass |
| 2 | Archived planted SNVs, helpers, CLI | 28/28 checks pass |
| 3 | Archived depth, flags, BAQ, hostile-input edges | 41/41 checks pass |
| 4 | Archived bcftools pipelines | 21/21 checks pass |
| 5 | Archived real library-specific matrix | 28/28 checks pass |
| 6 | Archived planted and randomized CIGAR differential matrix | 56/56 checks pass |
| 7 | Archived real/synthetic parameter matrix | 28/28 checks pass |
| 8 | Fresh read-N denominator and trailing-deletion regression | pass |
| 9 | Fresh padded-CIGAR boundary and shipped self-test | pass |

The fresh CIGAR parity check compared 3,784 ordinary-CIGAR rows under each of
five option sets. The trailing-deletion route compared 3,187 rows to samtools
without an exception. `allele_counts` now omits read-base `N`, matching
`find_variants` denominators. Padded CIGARs receive a named `ValueError` rather
than silently producing a wrong text pileup.
