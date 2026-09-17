> **Audit record for `bio-pathway-kegg-pathways`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/pathway-analysis/kegg-pathways) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-kegg-pathways
Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:pathway-analysis/kegg-pathways`
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=7)
Environment: R 4.4.3 / Bioconductor 3.20, `F:\OpenScience\audit-envs\crispr-screen-analyst` — clusterProfiler 4.14.6, org.Hs.eg.db 3.20.0, gson 0.2.1, SPIA 2.58.0, graphite 1.52.0, pathview 1.46.0, KEGGREST 1.46.0.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (human ORA) | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 2 | Variant A (human GSEA) | 40 | 59 | 99 | 4/4 PASS | ✅ |
| 3 | Edge (prokaryote, locus tags) | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 4 | Variant B (SPIA + graphite) | 35 | 50 | 85 | 3/5 PASS | ⚠️ |
| 5 | Stress (pin + modules + compareCluster) | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 6 | Scope boundary (ID misuse, use_internal_data) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 7 | Adversarial (no universe supplied) | 37 | 58 | 95 | 3/4 PASS | ✅ |

**Execution Average: 95.4 / 100**
**Assertion Pass Rate: 26/29 (89.7%)**
**Static Score: 89/100**
**Final Score: 93/100 — but Research Veto M4 (Code Usability) FAILS → Grade forced to ❌ Reject, not deployable. See below.**

> **Note for reviewer:** This Skill performed exceptionally well on 6 of 7 inputs — its two hardest documented claims (universe-omission bias, ID-join zero-hits trap) were reproduced exactly as written on fresh synthetic data. The veto fires on one specific, narrow, well-reproduced defect: the "graphite route" for SPIA never runs as documented, in both SKILL.md's own text and the shipped example script. See Input 4 and the dedicated investigation script for full root-cause detail.

---

## Data

All data under `data/` and `run/gate8/de_results.csv` are **SYNTHETIC**, generated in `data/make_data.R` and `data/make_eco_data.R`. Gene *membership* in the planted pathways is real, fetched live from `rest.kegg.jp`:

- Human: genes in **hsa04110 (Cell cycle)** planted as significantly UP (log2FC ~N(3, 0.6)), genes in **hsa04910 (Insulin signaling pathway)** planted as significantly DOWN (log2FC ~N(-3, 0.6)), against a 3000-gene random background sampled from `org.Hs.eg.db` (log2FC ~N(0, 0.5), non-significant p-values). 3296 total rows, SYMBOL+ENTREZID+log2FoldChange+pvalue+padj columns matching a realistic DESeq2 output and exactly the column names both shipped examples expect.
- E. coli: genes in **eco00010 (Glycolysis)** planted as significantly UP (46 real locus tags), against a ~1245-gene background assembled from other eco metabolic pathways.

## Gate 8 — Shipped Examples Run Verbatim

Both `examples/kegg_enrichment.R` and `examples/kegg_spia_topology.R` were copied unmodified into `run/gate8/` and run against `run/gate8/de_results.csv` (a copy of the synthetic data, columns matching what the examples expect with zero edits).

- **`kegg_enrichment.R`**: ran end-to-end with no modification. `Found 136 enriched KEGG pathways`, `Found 0 enriched KEGG modules` (consistent with the sparse-module caveat), pinned ORA against a fresh gson snapshot reproduced the same 136 pathways. See `run/gate8/kegg_enrichment.out`.
- **`kegg_spia_topology.R`**: first half (direct `spia()`) ran correctly — `SPIA scored 117 pathways; 111 significant after FDR`. Second half (graphite route) crashed: `Error in runSPIA(de = de_vec, all = universe, spia_set) : There is no dataset corresponding to the pathway set name: <tempdir>/kegg_hsa_spia`. See `run/gate8/kegg_spia_topology.out`.

## Root-Cause Investigation — graphite + runSPIA (`run/investigate_graphite_runSPIA_bug.R`)

Two independent, compounding defects, both confirmed by reading the installed `graphite` 1.52.0 source and independently corroborated against the current Bioconductor-release source of `graphite` 1.56.0 (the version SKILL.md's own "Version Compatibility" section declares as tested) fetched live from `rdrr.io/bioc/graphite/src/R/spia.R`:

1. **`runSPIA`'s existence check can never pass for an absolute `pathwaySetName`.** `graphite:::datasetName <- function(n) paste(n, "SPIA.RData", sep="")`; `runSPIA` checks `datasetName(pathwaySetName) %in% dir()`, where bare `dir()` lists only the current working directory's *filenames*. SKILL.md's own documented pattern, `spia_set <- file.path(tempdir(), 'kegg_hsa_spia')`, makes `datasetName()` return a full absolute path — which can never appear in that bare-filename listing, regardless of machine, OS, or whether `prepareSPIA` actually ran. Confirmed: `prepareSPIA` did write the file; `runSPIA` still refused it.
2. **Even worked around (relative name + matching working directory), the result is silently empty.** `convertIdentifiers(db, 'ENTREZID')` prefixes graphite's pathway node IDs (`"ENTREZID:1017"`), which never intersect the plain-numeric Entrez IDs SKILL.md's own `bitr()`-based gene-ID prep produces (`"1017"`) — so even a "successful" call returns 0 usable rows, the exact "exits 0, produces nothing" trap this audit series is calibrated to catch.

Full script, comments, and captured output: `run/investigate_graphite_runSPIA_bug.R` / `.out`.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have 240ish significant genes from a DESeq2 contrast as SYMBOLs and the rest of the expressed genes as background. Convert both to Entrez, run KEGG pathway ORA for human with the measured universe, and give me the top pathways by adjusted p-value with fold enrichment."
**Script:** `run/in1_canonical_ora.R` → `run/in1_canonical_ora.out`, `run/in1_kegg_ora_full.csv`
**Result:** 296 sig genes → 296 Entrez (0% conversion loss), 3312-gene universe. 136 enriched pathways. **hsa04110 (Cell cycle) is the #1 hit** by p.adjust (2.13e-35, Count=157). Fold enrichment computed and reported.
**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100 — 4/4 assertions PASS.

### Input 2 — Variant A
**Prompt:** "Run GSEA against KEGG on my full ranked gene list (no cutoff) and tell me which pathways come up on the up- vs down-regulated side."
**Script:** `run/in2_gsea.R` → `run/in2_gsea.out`, `run/in2_gsea_full.csv`
**Result:** 3296-gene ranked vector, `set.seed(123)` + `seed=TRUE`. **hsa04110 NES=+3.64** (planted up), **hsa04910 NES=-3.67** (planted down), both p.adjust=2.4e-10, the two most significant of 160 hits.
**Scores:** Basic 40/40 | Specialized 59/60 | Total 99/100 — 4/4 assertions PASS.

### Input 3 — Edge
**Prompt:** "This is an E. coli RNA-seq DE list with locus-tag gene IDs. Run KEGG enrichment with the right organism code and keyType, without forcing an OrgDb or bitr."
**Script:** `run/in3_prokaryote.R` → `run/in3_prokaryote.out`
**Result:** `organism='eco', keyType='kegg'`, raw locus tags, no bitr. **eco00010 (Glycolysis) is the #1 hit** (p.adjust=3.65e-84, 46/46 genes). `setReadable(kk, OrgDb=NULL)` correctly errors, matching the documented "cannot run without an OrgDb" guidance.
**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100 — 4/4 assertions PASS.

### Input 4 — Variant B ⚠️
**Prompt:** "I have a human DE list with log2 fold-changes and a universe. Run SPIA so direction and network position are used, tell me which signaling pathways are activated vs inhibited, and explain why this is not appropriate for metabolic pathways."
**Scripts:** `run/in4_spia.R` → `run/in4_spia.out`, `run/in4_spia_full.csv`; `run/investigate_graphite_runSPIA_bug.R` → `.out`
**Result:** Direct `spia()` (nB=200, ~217s): **hsa04110 Activated** (tA=+62.4, pGFdr=3.6e-138), **hsa04910 Inhibited** (tA=-224.6, pGFdr=1.2e-148) — both correct direction. hsa00010 (metabolic) absent from output entirely (not "meaningless", just not scored — SKILL.md's wording is slightly off). Graphite route: **fails as documented** (see root-cause section above). SPIA's own code block never calls `set.seed()` despite the Skill's Quantitative Thresholds table requiring it.
**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100 — 3/5 assertions PASS (2 FAIL: graphite route unrunnable; no seed shown for SPIA).

### Input 5 — Stress
**Prompt:** "Pin the current human KEGG release as a snapshot, record the date, run my ORA against the snapshot so a rerun next year gives the same pathways, also run KEGG module enrichment to localize which sub-process is hit, and compare KEGG enrichment between my up- and down-regulated gene sets in one faceted call."
**Script:** `run/in5_stress_pin_modules_compare.R` → `run/in5_stress_pin_modules_compare.out`, `in5_pinned_ora.csv`, `in5_modules.csv`, `in5_comparecluster.csv`
**Result:** `gson_KEGG('hsa')` fetch+pin 5.7s; pinned `enricher()` run reproduced **the exact same 136 pathways** as the live run, `accessed_date` survived write/read. `enrichMKEGG` correctly returned 0 modules with clusterProfiler's own explanatory message. `compareCluster` correctly segregated hsa04110 under "up" only and hsa04910 under "down" only.
**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100 — 4/4 assertions PASS.

### Input 6 — Scope Boundary
**Prompt:** "I ran enrichKEGG on my Ensembl/SYMBOL gene list directly (no ID conversion) and also tried use_internal_data=TRUE for reproducibility — something feels off, can you check?"
**Script:** `run/in6_scope_boundary_failure_modes.R` → `run/in6_scope_boundary_failure_modes.out`
**Result:** Raw SYMBOL IDs → **0 hits, no error** (exactly the documented "zero hits silently" symptom). `use_internal_data=TRUE` → hard error (`KEGG.db` not installed), matching the Skill's own "(and may simply fail)" caveat.
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 — 4/4 assertions PASS.

### Input 7 — Adversarial
**Prompt:** "Just run KEGG enrichment on my significant genes, I don't have a background set handy."
**Script:** `run/in7_adversarial_no_universe.R` → `run/in7_adversarial_no_universe.out`
**Result:** Without universe: 170 "enriched" pathways vs 136 with an explicit universe; **135/135 shared pathways show smaller (more "significant") p.adjust without the background** (e.g. hsa04110: 6.2e-254 vs 2.1e-35). Confirms the documented tissue-specificity bias precisely. However, the Skill's step-by-step agent workflow (`usage-guide.md`'s "What the Agent Will Do") has no explicit instruction to refuse/warn when no background is available — the warning exists only as reference documentation.
**Scores:** Basic 37/40 | Specialized 58/60 | Total 95/100 — 3/4 assertions PASS (1 FAIL: no explicit refusal/warning instruction in the agent workflow).

---

## Static Evaluation (25 criteria, 8 categories)

| Category | Score | Max |
|---|---|---|
| Functional Suitability | 10 | 12 |
| Reliability | 9 | 12 |
| Performance & Context | 8 | 8 |
| Agent Usability | 14 | 16 |
| Human Usability | 8 | 8 |
| Security | 11 | 12 |
| Maintainability | 11 | 12 |
| Agent-Specific | 18 | 20 |
| **Subtotal** | **89** | **100** |

Full per-criterion notes in `eval_report_bio-pathway-kegg-pathways_result.json` → `static_score`.

## Veto Gates

- **Skill Veto (T1–T4): PASS.** No crashes across 7 inputs + 2 shipped examples + 1 pathview spot-check; frontmatter complete; deterministic outputs (seeded where stochastic); no eval/exec of raw input, no injection vectors.
- **Research Veto (M1–M4): M4 FAILS.** M1 (Scientific Integrity), M2 (Practice Boundaries), M3 (Methodological Ground) all PASS. **M4 (Code Usability) FAILS**: the graphite+runSPIA code pattern, shipped verbatim as `examples/kegg_spia_topology.R`, does not run — confirmed via two independent, compounding, deterministic root causes (see above), corroborated against the currently-published Bioconductor source for the exact graphite version SKILL.md declares compatible. Per the scoring rubric, this forces `final.grade = Reject` and `deployable = false` regardless of the 93/100 numeric score, which is reported for diagnostic purposes only.

## Final Score

```
Static Score   : 89/100  × 40% = 35.6
Dynamic Score  : 95.4/100 × 60% = 57.2
FINAL SCORE    : 93 / 100 (diagnostic only — not the deployment verdict)
RESEARCH VETO  : FAIL (M4 — Code Usability)
GRADE          : ❌ Reject
DEPLOYABLE     : false
```

## Optimization Recommendations

**[P0] graphite + runSPIA code pattern never runs as documented** (Input 4) — see JSON `recommendations[0]` for full detail and fix.
**[P1] SPIA's own worked example omits the seed-fixing step the Skill requires elsewhere** (Input 4).
**[P1] No explicit agent instruction to refuse/warn when no background gene set is available** (Input 7).
**[P2] "Meaningless perturbation scores" wording for SPIA on metabolic maps doesn't match observed behavior** (Input 4).
