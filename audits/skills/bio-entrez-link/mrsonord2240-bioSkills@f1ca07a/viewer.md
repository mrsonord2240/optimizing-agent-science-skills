> **Audit record for `bio-entrez-link`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f1ca07a](https://github.com/mrsonord2240/bioSkills/tree/f1ca07a65d4a6ad9086814c57e69ae27dda7ca63/database-access/entrez-link) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-entrez-link — Phase 2 final-pass audit

**Result: 95/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@f1ca07a65d4a6ad9086814c57e69ae27dda7ca63:database-access/entrez-link`
- Worktree: `F:\OpenScience\wt\database-access-entrez-link`
- Runtime: `F:\OpenScience\runtime\agent-private\bio-entrez-link-phase2-20260923` (Biopython 1.88)
- Auditor exception: `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The pinned source began and ended clean. Every one of nine final-pass inputs was executed in the private audit runtime; no shared database-lane environment was reused or changed.

| Input | Executed evidence | Result |
|---|---|---|
| Curated and broad links | BRCA1: 368 RefSeq versus 1,087 all proteins; BioProject: 78 SRA UIDs | pass |
| Curated PubMed subset | TP53 GeneRIF: 9,982, all links: 20,402; subset true | pass |
| List versus comma IDs | two linksets (368/25) versus one union (393) | pass |
| `acheck` discovery | gene, nucleotide, and PubMed current link tables parsed | pass |
| History-server batching | 250 input genes → 1,374 linked proteins after QueryKey union | pass |
| Similarity boundary | source routes true similarity to local-blast/remote-homology | pass |
| Clinical boundary | source requires clinician/genetic-counselor referral for patient-specific link interpretation | pass |
| Fresh `acheck` pairs | structure and SNP schemas returned 13 and 2 guarded rows | pass |
| Namespace validation | BRCA1/TP53 labels resolved; wrong namespace gave actionable failure | pass |

Static review scored 96. Dynamic execution scored 94.1 with 34/34 assertions; weighted final score is 95. The research and structural vetoes pass.

See [eval_report_bio-entrez-link_result.json](F:\OpenScience\audits\bio-entrez-link\eval_report_bio-entrez-link_result.json) and [CHECKPOINT.md](F:\OpenScience\audits\_final_pass\bio-entrez-link\CHECKPOINT.md).
