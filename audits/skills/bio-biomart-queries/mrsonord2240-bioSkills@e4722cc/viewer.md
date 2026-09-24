> **Audit record for `bio-biomart-queries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e4722cc](https://github.com/mrsonord2240/bioSkills/tree/e4722ccd1616cc79568c1674be726d950d9297d5/database-access/biomart-queries) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-biomart-queries

Generated: 2026-09-24  
Source: `mrsonord2240/bioSkills@e4722ccd1616cc79568c1674be726d950d9297d5:database-access/biomart-queries`  
Final-pass note: fixed and audited under one brief; `auditor_independent: false`. See `F:\OpenScience\audits\_final_pass\bio-biomart-queries\CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical bulk mapping | 38 | 57 | 95 | 3/3 | ✅ |
| 2 | chr17 coordinates | 38 | 56 | 94 | 3/3 | ✅ |
| 3 | Discovery semantics | 38 | 56 | 94 | 3/3 | ✅ |
| 4 | Ortholog table | 38 | 57 | 95 | 3/3 | ✅ |
| 5 | GO and renamed symbol | 38 | 56 | 94 | 3/3 | ✅ |
| 6 | Scope boundary and adversarial fixtures | 38 | 57 | 95 | 4/4 | ✅ |
| 7 | Fresh deterministic batching | 39 | 57 | 96 | 3/3 | ✅ |
| 8 | Fresh live batching | 38 | 57 | 95 | 3/3 | ✅ |

Execution average: **94.8 / 100**. Assertion pass rate: **25/25**.

## What ran

`run/finalpass_rerun_archived_inputs.py` reran archived scenarios 1-7 against the current branch (the scope and adversarial scenarios share one report row) and added two fresh scale tests. `www.ensembl.org` was returning a 200 HTML outage page, captured by `run/finalpass_check_hosts.py`; the documented release-110 archive was live and used for the Python runs.

- Bulk mapping returned 49 rows for BRCA2, TP53, PTEN, EGFR, and MYC.
- Coordinates returned 1,186 chr17 protein-coding genes with the `Gene type` output column.
- Ortholog retrieval returned 3,773 chr17 rows and valid mouse/zebrafish one-to-one matches.
- GO retrieval returned 510 rows, found TP53, and did not silently substitute obsolete `MARCH1`.
- The source now rejects an empty list before network I/O, classifies outage HTML separately, and escapes XML filter values.
- The deterministic 1,001-ID fixture made three bounded requests. The live 1,001-ID archive query returned 1,001 rows after adaptive 414 splitting.

Changed Python files were compiled successfully. `examples/coordinate_table.sh` passed `bash -n`.

## R follow-up

`run/input_r_gene_biotype.R` loaded biomaRt 2.62.1 but could not complete any live connection: `useEnsembl(version=110)`, current `useEnsembl()`, and direct archive `useMart()` all failed before `getBM`. This is an explicit external evidence limitation, not an open source-fix recommendation: the source’s `gene_biotype` attribute is schema-correct, and corresponding live Python checks completed.

## Final assessment

Static score: **96/100**. Dynamic score: **94.8/100**. Final score: **95/100 — ⭐ Production Ready**.

No veto fired, no P0/P1/P2 source recommendation remains, and the Skill is deployable. When a biomaRt-compatible Ensembl mirror is available, the R evidence can be refreshed without changing this source.
