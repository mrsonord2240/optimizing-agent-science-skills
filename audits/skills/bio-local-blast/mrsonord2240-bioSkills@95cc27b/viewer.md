> **Audit record for `bio-local-blast`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@95cc27b](https://github.com/mrsonord2240/bioSkills/tree/95cc27bafcad6395ddac4c678b3224d951ff86f6/database-access/local-blast) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-local-blast final pass

Source: `mrsonord2240/bioSkills@95cc27bafcad6395ddac4c678b3224d951ff86f6:database-access/local-blast`  
Final-pass declaration: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Result

| Metric | Result |
|---|---|
| Final score | **95/100** |
| Grade | **⭐ Production Ready** |
| Deployable | **true** |
| Assertions | **35/35 PASS** |
| Inputs | **10/10 executed** |
| Open P0 / P1 / P2 | **0 / 0 / 0** |

| # | Type | Score | Assertions |
|---:|---|---:|---|
| 1 | Canonical | 95 | 4/4 PASS |
| 2 | Variant A | 95 | 3/3 PASS |
| 3 | Regression | 96 | 4/4 PASS |
| 4 | Edge | 95 | 3/3 PASS |
| 5 | Stress | 95 | 4/4 PASS |
| 6 | Scope boundary | 96 | 3/3 PASS |
| 7 | Adversarial | 94 | 3/3 PASS |
| 8 | Regression | 97 | 4/4 PASS |
| 9 | Regression | 96 | 3/3 PASS |
| 10 | Fresh | 97 | 4/4 PASS |

## Evidence and result

Archived Inputs 1-8 were re-executed with BLAST+ 2.17.0+: custom v5 search, cross-species dc-megablast, v5 taxonomy no-op and recovery, primer mode, RBH extraction, clinical boundary, adversarial thread/hitlist request, and v4 taxid-map storage. The archived Input 9 shell runner referenced a deleted worktree, so its Biopython and shipped-surface checks were rerun directly against this exact source. Two fresh checks confirmed the v4 nonzero filtering error with `taxdb.bti`, `taxdb.btd`, and `taxonomy4blast.sqlite3` installed, and checked all current documentation routes and shipped examples.

The correction establishes the tested distinction: v4 can retain assigned per-sequence taxids, but only v5 can apply `-taxids` or `-taxidlist`; v5 without taxonomy data can silently return unfiltered rows at exit 0, while v4 with taxonomy data fails loudly. No recommendation remains open.
