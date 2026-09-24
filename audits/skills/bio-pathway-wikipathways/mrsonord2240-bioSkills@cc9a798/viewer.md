> **Audit record for `bio-pathway-wikipathways`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cc9a798](https://github.com/mrsonord2240/bioSkills/tree/cc9a798929c5e73205d5148f5bc6abb37967b518/pathway-analysis/wikipathways) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-wikipathways

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@cc9a798929c5e73205d5148f5bc6abb37967b518:pathway-analysis/wikipathways`

## Verdict

**⭐ Production Ready — 96/100; deployable.** Skill Veto and Research Veto both PASS. The previous M4 rejection is resolved: every standalone organism check now uses `rWikiPathways::listOrganisms()`, and the source ships a focused non-human API smoke regression.

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical API | 38 | 58 | 96 | 3/3 | ✅ |
| 2 | Reproducible ORA | 38 | 58 | 96 | 3/3 | ✅ |
| 3 | Variant A | 38 | 57 | 95 | 3/3 | ✅ |
| 4 | Method Boundary | 38 | 58 | 96 | 3/3 | ✅ |
| 5 | API Compatibility | 39 | 58 | 97 | 3/3 | ✅ |
| 6 | Shipped Example | 38 | 58 | 96 | 3/3 | ✅ |
| 7 | Shipped Example | 38 | 58 | 96 | 3/3 | ✅ |

Execution average: **96.0 / 100**. Assertion pass rate: **21/21 (100%)**.

## Runtime and evidence

All seven inputs were freshly executed in the agent-specific `wikipathways-phase2` runtime: R 4.5.3, clusterProfiler 4.18.4, rWikiPathways 1.30.0, org.Hs.eg.db 3.22.0, tidyr 1.3.2, and enrichplot 1.30.5. No shared environment was changed. The fresh synthetic generator, scripts, and complete output are under `run/`.

1. **Human discovery:** `rWikiPathways::listOrganisms()` returned 41 organisms; `listPathways('Homo sapiens')` returned 1,131 pathways; WP554 returned metadata plus 17 Entrez IDs.
2. **Pinned ORA:** the shipped dated-GMT script selected release 20260710 and recovered WP554 (adjusted p=4.013e-29) in a CSV of six terms.
3. **Live ORA/GSEA:** explicit-universe ORA returned six terms including WP554; seeded GSEA returned 30. fgsea emitted visible tie/precision warnings.
4. **Universe boundary:** the identical WP554 list had matched background 17/420 (p.adjust 4.013e-29) versus default 17/9031 (2.716e-51), confirming the documented inflation risk.
5. **Corrected API boundary:** the new shipped `wikipathways_api_smoke.R` ran with only rWikiPathways plus clusterProfiler for enrichment: 41 organisms including Danio rerio, 55 Danio pathways, and two non-human ORA terms. A focused source scan recorded `stale_accessor=FALSE`.
6. **Shipped ORA example:** `wikipathways_ora.R` ran byte-for-byte on fresh synthetic input, completed ORA/GSEA and temporary plotting, and placed WP554 first.
7. **Shipped exploration example:** `wikipathways_explore.R` ran byte-for-byte with the corrected explicit accessor, completed live exploration and 20260710 pinning, and recovered WP554.

## Assertions

### Input 1 — Human discovery API

- [PASS] Organism enumeration works (41 organisms).
- [PASS] Human pathway listing works (1,131 rows).
- [PASS] WP554 metadata and 17 Entrez xrefs are available.

### Input 2 — Dated-GMT pinning

- [PASS] Newest-first monthly retry selected 20260710.
- [PASS] Compound GMT terms became usable ID/name tables.
- [PASS] Pinned enrichment recovered WP554.

### Input 3 — Live ORA/GSEA

- [PASS] Explicit-universe Entrez ORA completed.
- [PASS] Named decreasing GSEA completed.
- [PASS] Numerical caveats remained visible.

### Input 4 — Default-universe boundary

- [PASS] Both matched and default calls completed.
- [PASS] Their backgrounds differed materially (420 vs 9,031).
- [PASS] The default background inflated apparent significance.

### Input 5 — Standalone organism API and Danio regression

- [PASS] `rWikiPathways::listOrganisms()` resolves standalone and contains Danio rerio.
- [PASS] No invalid accessor call remains in `SKILL.md` or the exploration example.
- [PASS] Source smoke regression completed non-human ORA.

### Inputs 6–7 — Shipped examples

- [PASS] Both shipped examples exit 0 unchanged.
- [PASS] ORA/GSEA, live query, and dated archive branches complete.
- [PASS] WP554 is recovered in each relevant output.

## Veto assessment

Both gates PASS. The previous M4 failure is resolved by replacing the incorrect accessor with the explicitly namespaced rWikiPathways API, validating it in a standalone process, and exercising a live Danio rerio ORA. No diagnostic, treatment, fabrication, security, or methodological redline was observed.
