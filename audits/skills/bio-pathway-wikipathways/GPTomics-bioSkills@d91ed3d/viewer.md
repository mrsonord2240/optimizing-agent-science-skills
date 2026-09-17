> **Audit record for `bio-pathway-wikipathways`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/pathway-analysis/wikipathways) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-wikipathways
Generated: 2026-09-17

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:pathway-analysis/wikipathways`
Category: Data Analysis | Execution Mode: A (Direct — SKILL.md instructions + `examples/` reference scripts) | Complexity: Complex (N=7)
Environment: `crispr-screen-analyst` audit env — R 4.4.3 via `r.sh` (clusterProfiler 4.14.6, rWikiPathways 1.26.0, org.Hs.eg.db 3.20.0, tidyr 1.3.2). All WikiPathways calls hit the live, public, unauthenticated API/archive.

## Synthetic data
`data/make_wp_inputs.R` builds a synthetic DE-results table (`de_results_synthetic.csv`, 3048 genes) over **real** human gene identities (org.Hs.eg.db). Two **real** WikiPathways pathways were queried live and planted as signal:
- **WP554 "ACE inhibitor pathway"** (17 real Entrez genes) → planted UP (log2FC 2–4, padj 1e-6–1e-3)
- **WP430 "Statin inhibition of cholesterol production"** (31 real Entrez genes) → planted DOWN (log2FC −4…−2, padj 1e-6–1e-3)
- ~3000 background genes: log2FC ~ N(0, 0.4), padj ~ U(0.1, 1), plus 15 random genes nudged past the significance threshold by chance (realistic noise).
Only the DE call (log2FC/padj/significance) is fabricated; gene identities and WikiPathways membership are real, queried live.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (ORA) | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 2 | Variant A (GSEA) | 37 | 59 | 96 | 5/5 PASS | ✅ |
| 3 | Edge (universe) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Variant B (dated GMT) | 33 | 49 | 82 | 3/5 PASS | ❌ |
| 5 | Stress (compareCluster) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (zebrafish) | 37 | 56 | 93 | 4/5 PASS | ✅ |
| 7 | Adversarial (raw symbols) | 38 | 57 | 95 | 4/4 PASS | ✅ |

**Execution Average: 93.0 / 100**
**Assertion Pass Rate: 29/32 (90.6%)**
**Static Score: 90/100** | **Final Score: 92/100 → ⭐ Production Ready, deployable**

> Reviewer note: check Input 4 (❌) first — it is the only non-trivial finding, and it hits the Skill's own headline claim.

---

## Detailed Outputs

### Input 1 — Canonical: ORA
**Prompt:** "I have ~200 significant human genes as symbols and the ~13,000 tested genes as the background. Convert them to Entrez, run WikiPathways over-representation with the tested set as the universe, and give me the top 15 pathways by adjusted p-value with the gene symbols readable." *(usage-guide.md's own example prompt; run against the synthetic 63-gene/3048-gene DE table)*

**Code:** `run/in1_canonical.R` (bitr → enrichWP(universe=) → setReadable → top 15)

**Output (trimmed):**
```
n significant symbols: 63
bitr sig conversion: 63 / 63
bitr universe conversion: 3080 / 3048
n significant terms: 15
     ID                                  Description GeneRatio   p.adjust Count
  WP430 Statin inhibition of cholesterol production     31/49  9.49e-22    31
 WP5304                       Cholesterol metabolism     26/49  3.24e-15    26
  WP554                        ACE inhibitor pathway     17/49  6.86e-11    17
 ...
WP554 present: TRUE  rank 3 of 15, p.adjust 6.86e-11, Count 17
```
Both planted pathways recovered with their exact planted gene counts (17/17, 31/31).

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 5/5 PASS — see JSON for full text/justification.

---

### Input 2 — Variant A: GSEA
**Prompt:** "I have a full ranked DESeq2 result for every gene with no clear cutoff. Should I run WikiPathways ORA or GSEA, and run whichever is appropriate." *(usage-guide.md's "ORA vs GSEA" example)*

**Code:** `run/in2_gsea.R` (named decreasing Entrez vector → `set.seed(123)` → gseWP → re-run determinism check)

**Output (trimmed):**
```
ranked vector length: 3080
gseWP took 61.3 s
n significant terms: 16
     ID                                  Description       NES     p.adjust
  WP430 Statin inhibition of cholesterol production -3.054897 1.14e-10
  WP554                        ACE inhibitor pathway  2.766785 1.14e-10
...
Re-run with same seed -> identical term set: TRUE ; NES match: TRUE
```
Both planted pathways recovered with the biologically correct NES sign; determinism verified by re-running with the same seed.

**Scores:** Basic: 37/40 | Specialized: 59/60 | Total: 96/100
**Assertions:** 5/5 PASS.

---

### Input 3 — Edge: universe=NULL vs matched universe
**Prompt:** "Show me what happens if I forget to set the background universe for WikiPathways enrichment, versus setting it properly." *(direct test of the SKILL's own "Default universe inflates significance" failure-mode entry)*

**Code:** `run/in3_universe.R`

**Output (trimmed):**
```
--- Planted-signal list, unfiltered (pvalueCutoff=1) ---
matched universe WP554 p.adjust: 6.8642e-11   BgRatio: 17/186
default universe(NULL) WP554 p.adjust: 9.335318e-39   BgRatio: 17/9031
```
Background N balloons from 186 (tested-gene universe) to 9031 (all-WP-genes default), and the *same* true-positive hit's p.adjust becomes ~28 orders of magnitude more "significant" — this is exactly the risk the SKILL.md Common Errors table warns about, reproduced live.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS.

---

### Input 4 — Variant B: reproducible dated-GMT analysis ❌
**Prompt:** "Run WikiPathways enrichment but make it reproducible: pin a dated GMT release, split the term field into the WPID and name, run enrichment on the pinned sets, and tell me which release date to report in the methods." *(usage-guide.md's own "Reproducible analysis" example, using SKILL.md's own worked date)*

**Code:** `run/in4_dated_gmt.R`

**Output (trimmed):**
```
trying URL 'https://data.wikipathways.org/20240310/gmt/wikipathways-20240310-gmt-Homo_sapiens.gmt'
Warning: cannot open URL ...: HTTP status was '404 Not Found'
downloadPathwayArchive ERROR: cannot open URL ...
```
Live check of `https://data.wikipathways.org/` confirms the site's own pro-tip: *"This site hosts monthly data releases for the last 12 months."* The folder listing jumps from a 3-file `20230810` stray straight to `20260110` — every month between Aug 2023 and Jan 2026 is gone. `date='20240310'`, the exact value in both SKILL.md and usage-guide.md, is stale.

Substituting a currently-valid date (`20260810`) makes the rest of the pattern work exactly as documented:
```
WP554 present in this dated (2026-08-10) archive: TRUE
WP430 present in this dated (2026-08-10) archive: TRUE
n significant terms (dated archive): 14
  WP430 ... p.adjust 8.90e-22   WP554 ... p.adjust 6.44e-11
gson_WP() ran without error (current/-snapshot, not a date pin, as documented)
```

**Scores:** Basic: 33/40 | Specialized: 49/60 | Total: 82/100
**Assertions:** 3/5 PASS — the two FAILs are both about the stale example/undocumented retention window, not the underlying mechanism. **→ see P1 recommendation.**

---

### Input 5 — Stress: compareCluster up vs down
**Prompt:** "Run enrichment against WikiPathways for both my up- and down-regulated genes and show me which pathways are specific to each direction."

**Code:** `run/in5_comparecluster.R`

**Output (trimmed):**
```
n up: 30  n down: 33
n rows: 16
 Cluster     ID   Description                                    p.adjust  Count
      up  WP554  ACE inhibitor pathway                           1.43e-22    17
    down  WP430  Statin inhibition of cholesterol production     6.68e-35    31
...
WP554 (planted UP) assigned to up cluster only: TRUE
WP430 (planted DOWN) assigned to down cluster only: TRUE
terms unique to up: 3  unique to down: 13  shared: 0
```
Perfect cluster separation, no cross-contamination.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary: zebrafish (non-model organism)
**Prompt:** "Run WikiPathways enrichment for zebrafish Entrez genes, and first confirm the exact organism string WikiPathways expects."

**Code:** `run/in6_zebrafish.R`

**Output (trimmed):**
```
Danio rerio in get_wp_organisms(): TRUE
Danio rerio in listOrganisms(): TRUE
WP468 (zebrafish ACE inhibitor pathway) n genes: 7
n significant terms: 1
    ID           Description    p.adjust Count
 WP468 ACE inhibitor pathway 1.15e-09     7
organism='zebrafish' (common name) -> NULL result
```
Real zebrafish pathway (WP468) recovered exactly. Wrong organism string fails silently (NULL, no error) — this specific consequence isn't in the SKILL's failure-mode tables. **→ see P2 recommendation.**

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100
**Assertions:** 4/5 PASS.

---

### Input 7 — Adversarial: skip ID conversion
**Prompt:** "Just run enrichWP directly on my significant gene symbols, don't bother converting IDs, I want the fastest result."

**Code:** `run/in7_adversarial_symbols.R`

**Output (trimmed):**
```
n significant SYMBOLs (not converted to Entrez): 63
--> No gene can be mapped....
enrichWP on raw SYMBOLs returned NULL -- matches the documented failure mode (empty result, no error)
```
Exactly reproduces the SKILL's own documented "enrichWP returns 0 terms | passed SYMBOL/ENSEMBL not Entrez" Common Errors entry.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS.

---

## Shipped example scripts run verbatim (`run/verbatim_examples/`)

Both files under the Skill's own `examples/` were copied byte-for-byte and run unmodified (only supplying `de_results.csv`, the input filename both scripts already assume):

- **`wikipathways_ora.R`** — ran end-to-end with no edits: bitr → enrichWP → setReadable → GSEA (`gseWP`) → `pairwise_termsim` → `dotplot`/`emapplot` → PDF in `tempdir()` → CSV. Recovered both planted pathways with real gene-symbol lists after `setReadable()` (e.g. WP554: `BDKRB2/ACE2/MAS1/AGTR2/NOS3/CTSG/CYP11B2/TGFB1/KNG1/AGT/CMA1/ACE/REN/AGTR1/NR3C2/ATP6AP2/BDKRB1`, all real renin-angiotensin-system genes). One cosmetic ggplot2 deprecation warning (`size` → `linewidth`, from the `ggtangle` dependency), not a Skill defect.
- **`wikipathways_explore.R`** — halts with an unhandled R error (`Execution halted`) at `downloadPathwayArchive(date='20240310', organism='Homo sapiens', format='gmt', ...)`, the same stale-date 404 as Input 4. Everything before that line (listOrganisms, get_wp_organisms, listPathways, findPathwaysByText, getPathwayInfo, getXrefList) ran correctly and printed real, live WikiPathways data. This is the shipped file itself failing, not just a prose example — confirms Input 4's finding is a genuine, reproducible defect rather than an artifact of how the input was phrased.

Outputs: `run/verbatim_examples/wikipathways_ora.out`, `run/verbatim_examples/wikipathways_explore.out`.

## Other claims spot-checked (not separate scored inputs)
- `searchPathways('cancer','Homo sapiens')` → confirmed removed (`could not find function`), matching the documented "gone" claim.
- `args(downloadPathwayArchive)$format` → confirmed `c('gpml','gmt','svg')`, i.e. `gpml` is the default, matching the documented claim.
- `get_wp_organisms()` → confirmed to be a real, exported **clusterProfiler** function (not rWikiPathways), and it works correctly whenever clusterProfiler is loaded — which every SKILL.md code block that calls it already does. Initially looked like a bug (calling it with only `rWikiPathways` loaded fails) but this does not reflect how the Skill actually sequences its `library()` calls; verified with a second independent check (namespace inspection) before ruling it out. **No defect.**
- `getXrefList('WP554', code)` for `'L'`/`'H'`/`'En'` → all three BridgeDb codes confirmed correct (Entrez/HGNC symbol/Ensembl).

## Recommendations
See JSON `recommendations` for full text. Summary:
- **P1** — SKILL.md's/usage-guide.md's own reproducibility worked example, and the shipped `examples/wikipathways_explore.R` itself, use a date (`20240310`) that 404s today because WikiPathways' live archive retains only 12 months; running the shipped file unmodified halts with an unhandled R error. The Skill never states this retention window or the Zenodo long-term fallback.
- **P2** — A wrong organism string (e.g. `'zebrafish'` instead of `'Danio rerio'`) fails silently (NULL, no error); this specific consequence is missing from the otherwise-thorough failure-mode tables.

## Floors check (THRESHOLD.md / scoring_rubric.md)
| Floor | Value | Core (≥85) | Supporting (≥75) |
|---|---|---|---|
| Static Score | 90 | ✓ (≥80) | ✓ (≥70) |
| Execution Average | 93.0 | ✓ (≥85) | ✓ (≥75) |
| Layer 1 avg (Basic) | 37.0/40 | ✓ (≥32) | ✓ (≥28) |
| Layer 2 avg (Specialized) | 56.0/60 | ✓ (≥48) | ✓ (≥42) |
| Assertion pass rate | 90.6% | ✓ (≥90%) | ✓ (≥80%) |
| **Final Score** | **92** | **✓ Production Ready (≥85)** | ✓ (≥75) |

No veto fired (Skill Veto: PASS all four; Research Veto: PASS all four). **Deployable against both the core (85) and supporting (75) floor.**
