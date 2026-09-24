> **Audit record for `bio-entrez-fetch`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0681f5b](https://github.com/mrsonord2240/bioSkills/tree/0681f5b171b43eade5c4d81f0285dd9a5dbadb20/database-access/entrez-fetch) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-entrez-fetch — Phase 2 provenance re-audit

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

**Result: 95/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@0681f5b171b43eade5c4d81f0285dd9a5dbadb20:database-access/entrez-fetch`
- Worktree: `F:\OpenScience\wt\p2-reaudit-bio-entrez-fetch`
- Branch: `audit/phase2-reaudit-bio-entrez-fetch`
- Runtime: `F:\OpenScience\runtime\agent-private\bio-entrez-fetch-reaudit-20260923` (Biopython 1.88)
- Auditor exception: `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The isolated audit worktree began and ended clean at the requested commit. All seven dynamic inputs were explicitly executed without changing source, publishing, or merging.

| Input | Executed evidence | Result |
|---|---|---|
| Version-pinned sequence routes | BRCA1: 7,088 nt, one CDS; E. coli: 4,318 translated CDS; batch and gbwithparts passed | pass |
| Bulk summaries | Four nucleotide and three PubMed docsums; EFetch payload 47.3x ESummary | pass |
| PubMed formats | MEDLINE and XML returned current structured title/MeSH/PMC evidence | pass |
| ClinVar VCV | VCV000005107 parsed with stated Pathogenic classification | pass |
| History-server FASTA | One BRCA1 record, one FASTA header, 7,385 bytes | pass |
| dbSNP | APOE metadata from chromosome 19 parsed without patient inference | pass |
| SRA and taxonomy | SRR000001 runinfo parsed after bytes decode; taxonomy 9606 was Homo sapiens | pass |

Static review scored 94. Dynamic execution scored 95.7 with 29/29 assertions; weighted final score is 95. The provenance defect is repaired: the canonical machine-readable report now names the exact commit and final-pass exception.

See [eval_report_bio-entrez-fetch_result.json](F:\OpenScience\audits\bio-entrez-fetch\eval_report_bio-entrez-fetch_result.json).
