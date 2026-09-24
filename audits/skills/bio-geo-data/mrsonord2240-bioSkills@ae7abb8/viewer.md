> **Audit record for `bio-geo-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ae7abb8](https://github.com/mrsonord2240/bioSkills/tree/ae7abb81bc209cc856ab3ea55e4cd47eaf0e2364/database-access/geo-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-geo-data

Source: `mrsonord2240/bioSkills@ae7abb81bc209cc856ab3ea55e4cd47eaf0e2364:database-access/geo-data`
Generated: 2026-09-23
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

**⭐ Production Ready — 90.9/100; deployable true.** Static: 95/100. Dynamic: 88.2/100. Assertion ledger: 35 passed of 39; the four non-passing assertions are the two unavailable R GEOquery vectors, not a failed Python execution.

## Retained-evidence assembly

No vector was rerun. This canonical record is assembled solely from the completed retained private runtime at `F:\OpenScience\audits\bio-geo-data\run\phase2_structured_20260923_1815`, its exact source snapshot, the prior canonical evidence, and the final-pass checkpoint. The source provenance is exactly `ae7abb81bc209cc856ab3ea55e4cd47eaf0e2364`.

Both vetoes pass. The source protects against SuperSeries mixing, makes processed-versus-raw/SRA boundaries explicit, and has no clinical interpretation path. The Python selftest and all applicable Python vectors completed. The source snapshot separates runnable scripts from references and has an explicit Windows encoding regression guard.

## Static scoring

| Functional | Reliability | Performance | Agent | Human | Security | Maintainability | Agent-specific |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 12/12 | 12/12 | 8/8 | 16/16 | 8/8 | 12/12 | 10/12 | 17/20 |

## Dynamic evidence

| # | Vector | Executed | Basic | Specialized | Total | Assertions | Retained evidence |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | Breast-cancer GEO search + relation checks | yes | 38/40 | 56/60 | 94 | 4/4 | 10 current GSE records; FTP relation checks |
| 2 | GEO-to-SRA preferred + fallback | yes | 38/40 | 55/60 | 93 | 5/5 | both routes: 329 SRRs |
| 3 | GSE470 matrix + absent notes | yes | 39/40 | 57/60 | 96 | 4/4 | 12,625 features × 12 samples |
| 4 | PubMed-to-GEO | yes | 38/40 | 56/60 | 94 | 4/4 | PMID 32416070 → GSE147507 |
| 5 | GSE122288 platform decision | yes | 37/40 | 53/60 | 90 | 3/3 | standalone; methylation array |
| 6 | R GEOquery / Python GSE470 parity | **no** | 28/40 | 37/60 | 65 | 2/4 | Rscript unavailable; Python counterpart ran |
| 7 | SuperSeries-skip adversarial boundary | yes | 39/40 | 56/60 | 95 | 3/3 | source requires relation check/SubSeries split |
| 8 | Literal GSE346738 relation | yes | 39/40 | 56/60 | 95 | 3/3 | children GSE283260/GSE346737 |
| 9 | Alzheimer search + relation | yes | 38/40 | 54/60 | 92 | 3/3 | 5 results; parent relation found |
| 10 | GSE283260 matrix edge | yes | 37/40 | 54/60 | 91 | 3/3 | 41 samples; HDF5 note; no decode error |
| 11 | R non-ASCII GEOquery parity | **no** | 27/40 | 38/60 | 65 | 1/3 | Rscript unavailable |

The unexecuted R vectors are truthfully marked `executed: false` with `NOT_EXECUTED_ENVIRONMENT_UNAVAILABLE`; only their runtime capability checks ran. No shared/system R installation or package library was reused or mutated to force them.

## P2 follow-up

Provision a dedicated isolated R/Bioconductor GEOquery runtime for the two R parity vectors. This is an environment-capability follow-up, not evidence of a Python route defect.

Canonical structured record: [eval_report_bio-geo-data_result.json](eval_report_bio-geo-data_result.json).

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@ae7abb81bc209cc856ab3ea55e4cd47eaf0e2364:database-access/geo-data`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
