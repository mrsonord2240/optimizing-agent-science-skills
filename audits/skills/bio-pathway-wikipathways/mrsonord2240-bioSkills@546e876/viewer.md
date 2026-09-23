> **Audit record for `bio-pathway-wikipathways`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@546e876](https://github.com/mrsonord2240/bioSkills/tree/546e876725c9db99b4be698f03975ffa6f9b1e99/pathway-analysis/wikipathways) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-wikipathways

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@546e876725c9db99b4be698f03975ffa6f9b1e99:pathway-analysis/wikipathways`

## Verdict

**❌ Reject; deployable: false.** The numeric score is 90.0, but Research Veto M4 (code usability) fires because a documented rWikiPathways-only command invokes a function that that package does not export. This requires the P0 correction below before deployment.

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical API | 38 | 58 | 96 | 3/3 | ✅ |
| 2 | Reproducible ORA | 38 | 58 | 96 | 3/3 | ✅ |
| 3 | Variant A | 38 | 57 | 95 | 3/3 | ✅ |
| 4 | Method Boundary | 38 | 58 | 96 | 3/3 | ✅ |
| 5 | API Compatibility | 27 | 39 | 66 | 1/3 | ⚠️ |
| 6 | Shipped Example | 38 | 58 | 96 | 3/3 | ✅ |
| 7 | Shipped Example | 38 | 58 | 96 | 3/3 | ✅ |

Execution average: **91.6 / 100**. Assertion pass rate: **19/21 (90.5%)**.

## Environment and evidence

All inputs were fresh executions in the agent-specific `wikipathways-phase2` micromamba environment: R 4.5.3, clusterProfiler 4.18.4, rWikiPathways 1.30.0, org.Hs.eg.db 3.22.0, tidyr 1.3.2, and enrichplot 1.30.5. No shared environment was changed. The synthetic data generator, all executed scripts, and full outputs are in `run/`; generated input is `run/de_results.csv`.

### Input 1 — Human discovery API

**Prompt:** List supported organisms and human pathways, then inspect the community pathway WP554 and retrieve its Entrez gene set.

**Output:** `listOrganisms()` returned 41 organisms; `listPathways('Homo sapiens')` returned 1,131 pathways; WP554 returned metadata and 17 Entrez IDs.

- [PASS] Organism enumeration works.
- [PASS] Human pathway listing works.
- [PASS] Metadata and Entrez xrefs work.

### Input 2 — Dated-GMT reproducible ORA

**Prompt:** Run the shipped `wikipathways_pinned_enrich.R` script on synthetic Entrez IDs and record the monthly archive used.

**Output:** The shipped script selected 20260710, parsed its GMT, wrote `pinned.csv`, and recovered WP554 (adjusted p=4.013e-29) among six terms.

- [PASS] The newest-first archive retry selected a valid release.
- [PASS] GMT-term splitting produced usable IDs and descriptions.
- [PASS] The planted WP554 pathway was recovered.

### Input 3 — Live ORA and GSEA

**Prompt:** Enrich an explicit-universe Entrez list and run seeded GSEA on a decreasing named ranking.

**Output:** ORA returned six terms including WP554; GSEA returned 30. fgsea emitted its explicit tie and extreme-p-value precision warnings.

- [PASS] Explicit-universe ORA executes.
- [PASS] Named decreasing GSEA executes.
- [PASS] Numerical caveats are visible, not hidden.

### Input 4 — Universe boundary

**Prompt:** Compare the same WP554 query with a measured background versus `universe=NULL`.

**Output:** Matched background was 17/420 (p.adjust 4.013e-29); the default was 17/9031 (p.adjust 2.716e-51), directly confirming the Skill's warning about inflated significance.

- [PASS] Both calls completed.
- [PASS] The background changed from 420 to 9,031 mapped genes.
- [PASS] The default background inflated apparent significance.

### Input 5 — rWikiPathways-only organism validation

**Prompt:** Follow the `library(rWikiPathways)` direct-query/other-organism guidance and validate the organism accessor it names.

**Output:** The code parses, but `exists('get_wp_organisms', asNamespace('rWikiPathways'))` is false and calling it with only rWikiPathways attached errors. `clusterProfiler` separately exports the name, which is why the shipped exploration script (which loads both packages) masks the defect.

- [PASS] The code parses.
- [FAIL] rWikiPathways exports `get_wp_organisms()` as claimed.
- [FAIL] The rWikiPathways-only validation call runs.

### Input 6 — Shipped ORA example

**Prompt:** Run `examples/wikipathways_ora.R` unmodified against fresh synthetic input.

**Output:** The example completed with exit 0, ran ORA and GSEA, rendered its temporary PDF, and placed WP554 first in its ORA table.

- [PASS] Unmodified example exits 0.
- [PASS] Readable ORA output includes WP554.
- [PASS] GSEA and plotting branches complete.

### Input 7 — Shipped exploration example

**Prompt:** Run `examples/wikipathways_explore.R` unmodified.

**Output:** It completed with exit 0, listed/queryed live data, pinned 20260710, and recovered WP554. It succeeds because it also attaches clusterProfiler, which masks the documented standalone error rather than correcting it.

- [PASS] Unmodified example exits 0.
- [PASS] Live inspection and dated archive steps complete.
- [PASS] Self-contained pinned enrichment recovers WP554.

## Veto assessment

Skill veto: PASS. Research Veto: **FAIL** at M4 Code Usability. The source has no research-integrity, patient-care, or methodological redline, but user-followable rWikiPathways-only code is not runnable in the declared compatible runtime. Its separate successful example does not remove that failure because it relies on an accidental `clusterProfiler` namespace mask.

## P0 recommendation

Replace `get_wp_organisms()` with `rWikiPathways::listOrganisms()` wherever only rWikiPathways is loaded, or explicitly state and namespace `clusterProfiler::get_wp_organisms()`. Re-run the standalone direct-query block and a non-human organism check after the correction.
