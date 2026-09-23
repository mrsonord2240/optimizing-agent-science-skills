> **Audit record for `bio-geo-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ae7abb8](https://github.com/mrsonord2240/bioSkills/tree/ae7abb81bc209cc856ab3ea55e4cd47eaf0e2364/database-access/geo-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-geo-data — Phase 2 final-pass audit

**Result: 91/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@ae7abb81bc209cc856ab3ea55e4cd47eaf0e2364:database-access/geo-data`
- Worktree: `F:\OpenScience\wt\database-access-geo-data`
- Runtime: `F:\OpenScience\runtime\agent-private\bio-geo-data-phase2-20260923` (Biopython 1.88, GEOparse 2.0.4, pandas 3.0.6, pysradb 2.5.1)
- Auditor exception: `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The pinned source began and ended clean. All eleven inputs were explicitly executed in the agent-specific runtime/process tree; no shared database-lane environment was reused or changed.

| Input | Executed evidence | Result |
|---|---|---|
| Current GEO search example | 10 current human breast-cancer RNA-seq GSE records and FTP relation checks | pass |
| Current GEO-to-SRA example | pysradb and Entrez each returned the same 329-run set for GSE147507 | pass |
| GSE470 matrix | 12,625 features × 12 samples; absent processing notes handled | pass |
| Current PubMed example | PMID 32416070 linked to GSE147507 (110 samples) | pass |
| GSE122288 decision | current relation was standalone; `gdsType` was methylation array | pass |
| GEOquery parity | Python GEOparse passed; Rscript absent from private runtime | partial |
| SuperSeries boundary | source requires relation check and SubSeries processing | pass |
| Literal GSE346738 command | `super_of`: GSE283260 and GSE346737 | pass |
| Fresh Alzheimer search | 5 records; GSE283260 current parent relation found | pass |
| GSE283260 matrix | 41 samples, Cell Ranger HDF5 note, no decode error | pass |
| R non-ASCII parity | Rscript unavailable in private runtime | partial |

`geo_series.py selftest` passed, including its UTF-8 versus Windows cp1252 regression fixture. Static review scored 95. Dynamic execution scored 88.2 with 35/39 assertions; weighted final score is 91. The R GEOquery paths were not claimed as run: no R executable was present, and no shared/system runtime was mutated. This is a P2 environment-parity follow-up, not a Python-route blocker.

See [eval_report_bio-geo-data_result.json](F:\OpenScience\audits\bio-geo-data\eval_report_bio-geo-data_result.json) and [CHECKPOINT.md](F:\OpenScience\audits\_final_pass\bio-geo-data\CHECKPOINT.md).
