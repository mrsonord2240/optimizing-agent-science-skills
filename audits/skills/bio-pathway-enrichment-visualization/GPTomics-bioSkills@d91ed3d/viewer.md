> **Audit record for `bio-pathway-enrichment-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/pathway-analysis/enrichment-visualization) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-enrichment-visualization
Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:pathway-analysis/enrichment-visualization`
Category: Data Analysis (3) | Execution Mode: A (Claude writes/runs R following SKILL.md) | Complexity: Moderate → 5 inputs
Environment: `crispr-screen-analyst` (R 4.4.3 / Bioconductor 3.20 via `audit-envs\crispr-screen-analyst\r.sh`); clusterProfiler 4.14.6, enrichplot 1.26.6, ggplot2 4.0.3, org.Hs.eg.db 3.20.0 — all pre-installed, nothing installed for this audit.

## Skill Veto (Step 1)
| Dimension | Result |
|---|---|
| T1 Stability | PASS — both shipped examples and all 5 constructed inputs ran; no crash of the R process itself, no infinite loops |
| T2 Contract | PASS — valid frontmatter (`name`, `description`, `tool_type: r`, `primary_tool: enrichplot`) |
| T3 Determinism | PASS — GSEA example fixes `set.seed`; the one stochastic element (emapplot's force-directed layout) is openly disclosed by the Skill itself, not hidden |
| T4 Security | PASS — no `eval`/raw-string execution, no injection vectors, no credentials |

## Research Veto (Step 6, Category 3 applies)
| Dimension | Result |
|---|---|
| M1 Scientific Integrity | PASS — all 6 citations checked against real papers; no fabricated statistics (every number traced to live clusterProfiler/enrichplot output) |
| M2 Practice Boundaries | PASS — pure visualization of researcher-supplied objects, no patient-facing content |
| M3 Methodological Ground | PASS — GeneRatio≠FoldEnrichment, signed-NES, and DAG-redundancy claims all independently verified |
| M4 Code Usability | PASS — both shipped examples ran unmodified end-to-end; all 5 constructed inputs executed real R code (no syntax errors, no unresolvable imports) |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 35 | 52 | 87 | 4/4 PASS | ✅ |
| 3 | Edge | 34 | 54 | 88 | 4/4 PASS | ✅ |
| 4 | Variant B | 30 | 46 | 76 | 3/4 PASS | ❌ |
| 5 | Stress | 33 | 51 | 84 | 4/5 PASS | ✅ |

**Execution Average: 85.8 / 100**
**Assertion Pass Rate: 19/21 (90.5%)**

**Static Score: 95/100** (functional_suitability 11/12, reliability 11/12, performance_context 7/8, agent_usability 16/16, human_usability 7/8, security 12/12, maintainability 12/12, agent_specific 19/20)

**Final Score = 95×0.4 + 85.8×0.6 = 38.0 + 51.5 = 90 → ⭐ Production Ready, deployable, no veto.**

Floor check (scoring_rubric.md §5): Static 95≥80 ✓ | Exec avg 85.8≥85 ✓ (barely) | Layer1 avg 34.0≥32 ✓ | Layer2 avg 51.8≥48 ✓ | Assertion rate 90.5%≥90% ✓ (barely) — every Production-Ready floor is met, two of them by a narrow margin; see the P1 findings below before treating this as a comfortable pass.

> **Note for reviewer:** Two real, execution-verified defects (Inputs 4 and 5) are the reason the exec average and assertion rate sit this close to the floor rather than comfortably above it. Neither breaks the Skill's own worked examples.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I ran enrichGO on my DE hit list (BP ontology) and got a bunch of significant terms, but the default dotplot looks like the same theme repeated 20 times. Simplify the redundancy and make a clean dotplot, and tell me how many terms survived and how many were in the raw result."

**Code:** `run/input1_canonical.R` (real 24-gene synthetic cell-cycle Entrez list, `run/prep_data.R`)

**Output (stdout):**
```
Raw significant terms: 203
After simplify(cutoff=0.7): 77 terms survived (of 203 raw)
Wrote input1_output.pdf
Raw top-3 terms (by orderBy=x default, i.e. GeneRatio):
[1] "mitotic cell cycle phase transition"
[2] "DNA replication"
[3] "regulation of mitotic cell cycle phase transition"
[4] "regulation of cell cycle phase transition"
[5] "G1/S transition of mitotic cell cycle"
```
`run/input1_output.pdf` — 12,243 bytes, 3 PDF page objects, opens cleanly. The top-5 raw terms are visibly near-duplicate ("cell cycle phase transition" appears three times), directly reproducing the redundancy the Skill exists to address.

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] Output computes and reports both the raw and simplified GO term counts — 203 → 77 printed
- [PASS] Output produces a valid, non-empty, multi-page PDF figure — verified by PDF page-object count
- [PASS] Output does not fabricate p-values or enrichment statistics — real clusterProfiler output throughout
- [PASS] Output follows the Skill's prescribed collapse-then-dotplot workflow — `simplify()` called before the second `dotplot()`

---

### Input 2 — Variant A
**Prompt:** "Plot my gseGO GSEA result the way that keeps the direction (activated vs suppressed) — an overview across all significant pathways and a detailed running-score plot for the top one."

**Code:** `run/input2_variantA.R` (synthetic 3000-gene ranked list, cell-cycle genes pushed to the top, `set.seed(123)`)

**Output (stdout):**
```
GSEA significant sets: 347
NES range: 1.19 to 3.25 | n positive: 347 | n negative: 0
ridgeplot ERROR: The package "ggridges" is required for `ridgeplot()`.
barplot method exists for gseaResult: FALSE
barplot(gse) attempt: ERROR (expected): 'height' must be a vector or a matrix
Wrote input2_output.pdf
```
`run/input2_output.pdf` — 66,003 bytes (NES dotplot + gseaplot2 pages). `ggridges` is deliberately not installed (audit rule: install nothing into the shared env) — its absence is exactly the failure the Skill's own `usage-guide.md` Prerequisites section documents, verbatim.

**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100

**Assertions:**
- [PASS] Output preserves GSEA direction (signed NES) — `dotplot(gse, x='NES', color='p.adjust')`, all 347 sets shown with sign intact
- [PASS] Output does not force a barplot onto the gseaResult — confirmed no S4 method exists, and a forced attempt throws
- [PASS] Missing optional dependency fails with the exact message the Skill documents — text match confirmed
- [PASS] Output produces a valid non-empty PDF with the plots that did succeed

---

### Input 3 — Edge
**Prompt:** "My enrichResult only has a couple of significant GO terms after FDR correction. Build a gene-concept network for my top terms, colored by log2 fold change, and tell me if a term-similarity map even makes sense at this scale."

**Code:** `run/input3_edge.R` + supplementary `run/check_single_term.R`

**Output (stdout):**
```
Significant terms at strict cutoff: 28
n terms available for similarity map: 28 -- a map is only informative with several terms;
at n<=2 there is nothing for redundancy structure to show.
Wrote input3_output.pdf
```
Note (recorded honestly): the 6-gene subset still produced 28 significant terms, not the near-empty result the prompt's premise implied — this is disclosed rather than silently re-framed as a clean match. A direct supplementary test forcing an `enrichResult` to exactly 1 row (`run/check_single_term.R`) confirmed the actual property being probed: `emapplot` degrades to a benign warning (`no non-missing arguments to max`) rather than crashing, even at n=1.

**Scores:** Basic: 34/40 | Specialized: 54/60 | Total: 88/100

**Assertions:**
- [PASS] Output attempts the requested cnetplot colored by fold change
- [PASS] Output reasons about whether a similarity map is informative at the observed term count
- [PASS] `pairwise_termsim`/`emapplot` does not hard-crash at very low term counts — n=1 supplementary test
- [PASS] Output produces a valid non-empty PDF (17,582 bytes)

---

### Input 4 — Variant B
**Prompt:** "I ran compareCluster across my up- and down-regulated gene sets and want a faceted dotplot comparing them. Also show the redundancy structure with an enrichment map and a treeplot with 5 named clusters."

**Code:** `run/input4_variantB.R` + confirmation `run/check_treeplot_ck.R`

**Output (stdout, abridged):**
```
Up: 22 genes | Down: 4 genes
compareCluster rows: 661
treeplot ERROR: Problem while computing aesthetics.
  Caused by error in `check_aesthetics()`:
  ! Aesthetics must be either length 1 or the same as the data (51).
  Fix the following mappings: `from`, `to`, and `.panel`.
Wrote input4_output.pdf
```
`dotplot(ck)` (faceted Up/Down comparison) and `emapplot(pairwise_termsim(ck))` both rendered correctly (pages 1–2 of the PDF). `treeplot(ck_ts, nCluster=5)` crashed. **Re-tested** with the deprecation-suggested replacement `cluster.params=list(n=5)` (`run/check_treeplot_ck.R`) — **same crash**, confirming this is not the `nCluster` deprecation but a genuine `treeplot`-on-`compareClusterResult` incompatibility under the installed `enrichplot 1.26.6` / `ggplot2 4.0.3`. Not covered by `SKILL.md`'s Version Compatibility note (which anticipates `cnetplot`/`emapplot`/`goplot` churn, not this).

**Scores:** Basic: 30/40 | Specialized: 46/60 | Total: 76/100

**Assertions:**
- [PASS] Output produces the requested faceted dotplot
- [PASS] Output produces the requested enrichment map on the compareCluster result
- [FAIL] Output produces the requested treeplot with 5 named clusters — crashed, reproducibly, both argument forms
- [PASS] Output surfaces a clear, legible error rather than failing silently

---

### Input 5 — Stress
**Prompt:** "Give me the full modeling-choice figure set from my enrichGO BP result: raw top-20 dotplot AND simplify()+dotplot; pairwise_termsim → emapplot and treeplot; a gene-concept network for the top 6 terms colored by fold change; a heatplot; and an upsetplot of gene overlaps. Order the dotplot by fold enrichment instead of GeneRatio and explain why that differs from the default in the caption."

**Code:** `run/input5_stress.R`

**Output (stdout, abridged):**
```
Raw significant terms: 203
GeneRatio vs computed FoldEnrichment -- Spearman rho: -0.113 (1.0 would mean the two orderings never differ)
upsetplot ERROR: The package "ggupset" is required for `upsetplot()`.
Plots produced: raw_dotplot, simplified_dotplot, foldenrichment_dotplot, emapplot, treeplot, cnetplot, heatplot
Wrote input5_output.pdf
```
7 of 8 requested plots succeeded — notably `treeplot` succeeded here on a plain `enrichResult` (contrast with Input 4's `compareClusterResult` crash, isolating the bug to that one class). The Spearman rho of −0.113 quantitatively confirms the Skill's claim that GeneRatio and FoldEnrichment orderings meaningfully disagree. `upsetplot()` failed on a **previously-undocumented** dependency: `ggupset` is never mentioned anywhere in `SKILL.md` or `usage-guide.md`, unlike `ggridges`/`ggarchery` which are explicitly listed.

**Scores:** Basic: 33/40 | Specialized: 51/60 | Total: 84/100

**Assertions:**
- [PASS] Output reports both raw and simplified term counts
- [PASS] Output produces the FoldEnrichment-ordered dotplot and quantifies the ordering difference
- [PASS] Output produces the requested emapplot, treeplot, cnetplot, and heatplot
- [FAIL] Output produces the requested upsetplot — `ggupset` missing and undocumented
- [PASS] Output produces a valid non-empty PDF (42,838 bytes)

---

## Additional verification (not a scored input, supporting evidence)

- **Both shipped example scripts ran unmodified, end-to-end, exit 0:** `run/examples_test_ora.R` (copy of `examples/visualization_ora.R`) and `run/examples_test_gsea.R` (copy of `examples/visualization_gsea.R`). The GSEA example's own random-noise synthetic input correctly triggers its `if (nrow(...) > 0)` branch and prints "No enriched sets in this synthetic run" instead of crashing — the Skill's own code already models the defensive pattern recommended in P2 recommendation 3.
- **API-currency checks** (`run/check_args.R`, `check_args2.R`, `check_pkgs.R`): confirmed the installed `cnetplot()` signature matches the Skill's documented post-churn arguments (`color_item`, `node_label`, no `circular`/`colorEdge`); confirmed `barplot` has no S4 method for `gseaResult`; confirmed `GOSemSim`, `viridis`, `ggtangle` are present, `ggridges`/`ggupset`/`ggarchery` are not (Suggests-only, not installed per audit rules).

## Files
- `run/prep_data.R` — synthetic data generator (labelled synthetic; real public Entrez IDs, fabricated hit-list membership and fold-change values)
- `run/input1_canonical.R` … `run/input5_stress.R` — the 5 scored inputs
- `run/input*_output.pdf` — their rendered figures
- `run/examples_test_ora.R`, `run/examples_test_gsea.R` — verbatim-copy runs of the Skill's own shipped examples
- `run/check_*.R` — supporting API/dependency verification scripts
- `data/gene_data.rds`, `data/README.md` — the synthetic dataset
