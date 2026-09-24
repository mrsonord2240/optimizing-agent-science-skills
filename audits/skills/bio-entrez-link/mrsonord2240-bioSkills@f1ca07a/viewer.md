> **Audit record for `bio-entrez-link`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f1ca07a](https://github.com/mrsonord2240/bioSkills/tree/f1ca07a65d4a6ad9086814c57e69ae27dda7ca63/database-access/entrez-link) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-entrez-link — Phase 2 final-pass audit

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

**Result: ⭐ 95/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@f1ca07a65d4a6ad9086814c57e69ae27dda7ca63:database-access/entrez-link`
- Evidence: `F:\OpenScience\audits\bio-entrez-link\run\phase2_structured_20260923_1800`
- Runtime: `F:\OpenScience\runtime\agent-private\bio-entrez-link-phase2-20260923` (Biopython 1.88)
- Auditor exception: `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The pinned source began and ended clean. All nine final-pass vectors completed in the private audit runtime; no shared mutable database-lane environment was changed.

| Input | Evidence-backed assertions | Result |
|---|---:|---|
| Curated and broad links | BRCA1 368 RefSeq vs 1,087 all proteins (3.0x); raw neighbor scores; BioProject 78 SRA UIDs | 4/4 |
| Curated PubMed subset | TP53 GeneRIF 9,982; all links 20,402; subset true | 3/3 |
| List versus comma IDs | documented live list: two linksets (368/25); comma string: one union (393) | 4/4 |
| `acheck` discovery | gene, nucleotide, and PubMed tables parsed; missing menu tags guarded | 4/4 |
| History-server batching | TP53 25 RefSeq to 251 structures; 250 genes union to 1,374 proteins | 4/4 |
| Similarity boundary | ELink relationship distinguished from similarity; local-blast and remote-homology route present | 3/3 |
| Clinical boundary | no diagnostic/prescriptive link interpretation; clinician and genetic-counselor referral | 3/3 |
| Fresh `acheck` pairs | structure 13 and SNP 2 guarded three-field rows | 3/3 |
| Namespace validation | usage/import path, BRCA1/TP53 resolution, wrong namespace actionable nonzero error | 6/6 |

Execution total: **847/900**, so `847 / 9 = 94.1`; assertions: **34/34**. Static review is **96/100**. Weighted result is `96 × 0.4 = 38.4` plus `94.1 × 0.6 = 56.5`, yielding **94.9**, rounded to **95**. All structural and research veto gates pass.

See [canonical JSON report](F:\OpenScience\audits\bio-entrez-link\eval_report_bio-entrez-link_result.json) and [checkpoint](F:\OpenScience\audits\_final_pass\bio-entrez-link\CHECKPOINT.md).
