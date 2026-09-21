> **Audit record for `bio-data-visualization-lollipop-protein-maps`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/lollipop-protein-maps) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-lollipop-protein-maps
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/lollipop-protein-maps` (unmodified upstream). First audit; role unspecified, scored as a standalone plotting Skill.
Category: Data Analysis | Mode: A | Complexity: Moderate (3 tools, 5 task types, 3 files) -> N = 5

**Final: 65 / 100 - Beta Only - deployable: false** (static 64 x 0.4 = 25.6; execution avg 66.4 x 0.6 = 39.8). Skill veto PASS; Research veto PASS (M4 borderline, see below). No open P0.

Environment: R 4.4.3 via `r.sh`; maftools 2.22.0, trackViewer 1.42.0, g3viz 1.2.0 (CRAN archive), svglite, webshot2 + Chrome. All scripts are in `run/` (00-13, `helpers.R`, `build_report.py`); figures in `run/out/`. Nothing written into the source clone.

## How correctness was checked (not "it ran")

- **Independent truth.** `run/01_make_synthetic.py` writes a seeded synthetic TP53/KRAS MAF (300 rows: planted hotspots R175H x45, R248Q x38, R248W x12, R273H x29; truncating classes; 12 off-domain singletons; 40 scattered; HGVSp edge cases) plus a truth table computed with a regex written there (per position and per change: mutation rows, unique samples, class). Real data: maftools' TCGA-LAML (193 samples).
- **Drawn geometry, not returned tables.** Base-graphics figures were drawn to svglite; every `<circle>` was converted to (aa position, height) using the axis tick labels (x) and the y-axis labels, and the domain rectangles to aa start/end (`run/helpers.R`). trackViewer draws polygons, so its PNG was measured by pixel centroid vs axis ticks (`run/07_png_measure.py`). g3viz's embedded JSON was parsed and its screenshot opened.
- **Reference values.** UniProt P04637 (cached JSON) and P01116 (public read-only REST); Ensembl REST lookup for two transcript ids.
- All PNGs listed below were opened with the Read tool: non-blank, labels legible.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: maftools TP53, planted hotspots | 33 | 47 | 80 | 3/5 | OK |
| 2 | Variant A: lollipopPlot2 cohort comparison | 32 | 45 | 77 | 2/4 | warn |
| 3 | Edge: HGVSp edge cases + isoform | 26 | 36 | 62 | 1/5 | fail |
| 4 | Variant B: trackViewer + UniProt domains | 24 | 34 | 58 | 2/5 | fail |
| 5 | Stress: g3viz + shipped example end to end | 22 | 33 | 55 | 1/5 | fail |

**Execution Average: 66.4 / 100** | **Assertion pass rate: 9/24** | executed 5/5

## Static score (25 criteria) = 64 / 100

Functional 7/12, Reliability 6/12, Performance/Context 5/8, Agent usability 10/16, Human usability 5/8, Security 10/12, Maintainability 6/12, Agent-specific 15/20. Notes per category are in the JSON.

Shipped-means-present (gate 8): `SKILL.md` and `usage-guide.md` point at no `references/`, `scripts/` or `assets/` file; the one shipped file `examples/lollipop_phd.R` exists. Placeholders `cohort.maf` and `clinical` are undefined. Research scope (gate 7): visualization only, no diagnosis or prescription.

## Detailed Outputs

### Input 1 - Canonical (maftools, synthetic TP53)
**Prompt:** "Build a lollipop plot for TP53 from this cohort MAF. Mark R175H, R248Q, R273H. Color stems by variant class, show the actual count on each lollipop." (`run/04_maftools_synth.R`, SKILL.md block 1 with the Skill's `AACol='HGVSp_Short'`, `labelPos`, `printCount=TRUE`, 7-colour palette.)

Executed: yes. Figure `run/out/S1_tp53_maftools.png` opened: backbone, three labelled hotspots, legend, no counts.

What was checked (from the drawn SVG vs the truth table):
- R175H 46, R248Q 38, R273H 29, R248W 13, R342* 8, X125_splice 6, E286Kfs*9 5, P72Lfs*3 4, K381del 4, E298_S299insG 3: every circle at the right residue and height; the merge of maftools' table with the truth differs only for `p.M1?` (dropped, 2 rows). R175H = 46 is 45 samples plus one duplicate row.
- Colours: 77/77 circles at truth positions carry the `class_col` colour.
- Protein length drawn 393 = UniProt P04637. Domains drawn: P53_TAD 5-29, P53 109-288, P53_tetramer 319-359. UniProt: transactivation 1-44, DNA binding 102-292, oligomerization 325-356. maftools' domains are an NCBI CDD (`db_xref`) table bundled in `extdata/protein_domains.RDs`, not a Pfam query.
- `printCount = TRUE`: the source `print()`s the summary table to the console and draws nothing; the Skill says it annotates each lollipop ("CRITICAL: show counts").
- maftools uses "the longer transcript" (NM_000546) from that table, not "the canonical UniProt isoform"; the return value is a data.table from base graphics, not "a ggplot2 object"; every point has the same radius (3.36) so size does not encode count, height does.

**Scores:** Basic 33/40 | Specialized 47/60 | Total 80/100
**Assertions:**
- [PASS] Each lollipop sits at the right residue with height = independent count - all rows listed above match.
- [PASS] Classes map to the supplied colours - 77/77.
- [FAIL] printCount annotates each lollipop - nothing on the plot.
- [FAIL] Protein length and domains equal UniProt - length yes; domain boundaries no (CDD, not UniProt/Pfam).
- [PASS] labelPos labels appear at the named residues.

### Input 2 - Variant A (two cohorts, lollipopPlot2)
**Prompt:** "Paired lollipop comparing TP53 mutations between the Luminal and Basal cohorts using lollipopPlot2; also DNMT3A in TCGA-LAML by FAB group." (`run/05_maftools_plot2.R`.)

Executed: yes. Figures `P2_tp53_subtype.png`, `P2_laml_dnmt3a_ok.png` opened.
- Drawn heights (SVG): Luminal R175H 46 (+1 R175C), R248Q 18, R248W 8; Basal R248Q 20, R248W 5, R273H 29. Independent counts from the MAF joined to the clinical table: identical. LAML DNMT3A R882H: 9 up, 9 down; independent count by FAB group 9 and 9.
- Panel headers `Luminal [75.32%; N = 154]`, `Basal [68.12%; N = 138]` correct.
- As written (`AACol1 = 'HGVSp_Short'`) on the LAML MAF: `Error: object 'AAChange' not found` (lollipopPlot proper says `Column HGVSp_Short not found.`). With `Protein_Change` it works.
- Domain colours are re-drawn at random per call (TAD blue/P53 salmon/tetramer yellow in lollipopPlot; salmon/yellow/blue in lollipopPlot2), contradicting the Skill's "colour by functional class" advice; domain names overlap on the DNMT3A figure.

**Scores:** Basic 32/40 | Specialized 45/60 | Total 77/100
**Assertions:**
- [PASS] Up/down heights equal per-cohort counts.
- [FAIL] Block as written runs on maftools' own LAML data.
- [FAIL] Domain colours stable / functional.
- [PASS] Cohort N and mutation rate on the figure.

### Input 3 - Edge (HGVSp edge cases, isoform)
**Prompt:** "My MAF has splice, frameshift, start-loss and stop-loss calls, a 3-letter HGVSp, a sample with two hits at one residue, and my calls are on a shorter TP53 isoform. Plot it and tell me what was dropped." (`run/04`, `06`, `06b`, `11`.)

Executed: yes.
- maftools: `p.X125_splice` at 125 (6), `p.E286Kfs*9` at 286 (5), `p.P72Lfs*3` at 72 (4), `p.*394Wext*?` at 394 (past the 393 backbone). `p.M1?` removed by "Removed 2 mutations for which AA position was not available"; `p.=` (Silent) and empty HGVSp removed by `read.maf`; `p.Arg175His` plotted at 175 as its own stem, not merged with R175H.
- The Skill's trackViewer summary code (`sub('p\\.[A-Z](\\d+).*')`) returns NA for `p.Arg175His` and `p.*394Wext*?`; `IRanges(NA)`: `'start' or 'width' cannot contain NAs`. A class not in the 7-colour palette (`Translation_Start_Site`, `Nonstop_Mutation`): `missing values in 'row.names'`. Both reproduced separately (`06b_trackviewer_na.log`).
- `refSeqID = 'NM_001126115'` (261 aa) on a cohort with mutations at 273/286/342/381: the backbone stops at 261 and the later lollipops are clipped, no warning (`I1_short_isoform.png` opened).
- `proteinID = 'P04637'` (UniProt id, from the example): ` not found!`; `proteinID = 'NP_000537'` works.
- Ensembl REST: `ENST00000269305` = TP53-201 (canonical); `ENST00000288602` = BRAF-201. SKILL.md's isoform failure mode names the BRAF transcript as canonical TP53 and gives an invented "R175H plotted at R177H" symptom.
- KRAS: maftools drew G12D (30) and G12V (25) as two stems at residue 12, never the 55 that g3viz shows for the residue; protein length 189 = UniProt P01116.

**Scores:** Basic 26/40 | Specialized 36/60 | Total 62/100
**Assertions:**
- [PASS] Splice/frameshift/extension strings land at the named residue.
- [FAIL] The Skill's own parsing code survives realistic HGVSp.
- [FAIL] Isoform handling behaves as stated.
- [FAIL] Transcript ids quoted are correct.
- [FAIL] Multi-hit positions shown at true recurrence.

### Input 4 - Variant B (trackViewer with UniProt domains)
**Prompt:** "Use UniProt domain coordinates instead of maftools' cached Pfam. Render TP53 with trackViewer::lolliplot." (`run/06_trackviewer.R`, `07_png_measure.py`, `11_extras.R`, `12_factor_color.R`.)

Executed: yes. Figures `T1_skillmd_trackviewer.png`, `T3_trackviewer_uniprot.png`, `E1_example_sec5_trackviewer.png` opened.
- SKILL.md block verbatim: pixel centroids give x = 175.0 / 248.0 / 273.0 and heights 44.9 / 37.9 / 28.9 for scores 45 / 38 / 29 (ticks at 7.375 px/unit). The x window starts at the first feature (102), not residue 1.
- Domain coordinates as coded vs UniProt P04637 (length 393): SKILL.md DNA-binding 102-291 (IRanges width 190 = one short of 102-292), Tetramerization 323-352, Regulatory 363-392. Example: 1-41, 102-291, 323-355, 363-392 while its comment says 1-42, 102-292, 323-356, 363-393. UniProt: transactivation 1-44, DNA binding 102-292, oligomerization 325-356, basic region 368-387; there is no "Regulatory 363-393".
- Example section 5 on a clean MAF (`class_col[mutation_summary$class]`, where `class` is a factor): colours are picked by integer code. The three missense hotspots are `#CC79A7` (Splice_Site pink) instead of `#D55E00`; `12_factor_color.R` counts 55 of 55 lollipops wrong. The figure looks plausible and gives no warning. `names(snps) <- class` also captions every stem with its class name ("Missense_Mutation" x 50) and the residue labels never appear.
- Repaired (`as.character()`, UniProt coordinates, residue names): heads at 47 / 51 / 29 for 175 / 248 / 273, orange missense, four UniProt domains. trackViewer spreads crowded heads away from the true position (dashed guides show the residue).

**Scores:** Basic 24/40 | Specialized 34/60 | Total 58/100
**Assertions:**
- [PASS] Heads at the stated residues and heights.
- [FAIL] Domain boundaries equal UniProt.
- [FAIL] Classes map to intended colours in the example (55/55 wrong).
- [PASS] The repaired code draws the correct map.
- [FAIL] Every lollipop labelled with its residue.

### Input 5 - Stress (g3viz interactive + shipped example end to end)
**Prompt:** "Build an interactive HTML lollipop with g3viz for the online supplement (nature theme), for TP53 and KRAS; run the shipped example." (`run/08_g3viz.R`, `09_g3viz_check.R`, `10_example_run.py`, `10_run_examples.sh`, `13_pylollipop_check.sh`.)

Executed: yes. Screenshot `TP53_g3viz.png` opened (three class colours, hover buttons, domains, 60-count axis).
- `hgvspChange2protein(maf, gene = 'TP53')` (SKILL.md and example): `could not find function "hgvspChange2protein"`; g3viz 1.2.0 exports no such function.
- `g3Lollipop(..., output.filename = 'TP53_lollipop.html')` writes no file; the argument names the PNG/SVG download. `htmlwidgets::saveWidget()` produced the html (394 KB) and a Chrome screenshot.
- The route that works (`readMAF(protein.change.col = 'HGVSp_Short')` -> `g3Lollipop`): TP53 175/248/273 = 48/51/29 and KRAS 12/13/61 = 55/12/8 equal the truth table; only p.M1? has no position. Domains (Pfam) TP53 P53_TAD 6-30, TAD2 35-59, P53 99-289, P53_tetramer 319-358; KRAS Ras 5-165; lengths 393 and 189 equal UniProt. `p.=` is classed "Inframe" with no position.
- Shipped example `examples/lollipop_phd.R`, only `cohort.maf`/`clinical` substituted: V1 halts at `proteinID = 'P04637'` (step 3); V2 (proteinID removed) halts at step 5 `missing values in 'row.names'`; V3 (MAF cleaned of edge cases and unpalette classes) completes steps 1-5 and halts at step 6 on `hgvspChange2protein`. No variant produces the g3viz HTML.
- `pyLollipop` (named in SKILL.md): not on PyPI (`pip index` and HTTP 404). ProteinPaint is hosted-only.

**Scores:** Basic 22/40 | Specialized 33/60 | Total 55/100
**Assertions:**
- [FAIL] The g3viz path in SKILL.md and the example runs.
- [FAIL] `output.filename` writes an HTML file.
- [FAIL] The shipped example runs to completion.
- [PASS] g3viz counts, positions and lengths equal independent values / UniProt.
- [FAIL] Every listed tool can be used (pyLollipop absent).

## Research Veto

| Dimension | Result | Basis |
|---|---|---|
| Scientific integrity | PASS (borderline) | No fabricated result; illustrative counts are labelled. The BRAF transcript named as TP53 canonical and the invented R177H symptom are factual errors (P1). |
| Practice boundaries | PASS | Visualization only. |
| Methodological ground | PASS | Hotspot-validation and isoform cautions are sound. |
| Code usability | PASS (borderline) | maftools, lollipopPlot2, trackViewer and g3viz (via readMAF) all produce correct figures with small corrections; the shipped example and the SKILL g3viz block do not run as written. A stricter reading of M4 fails the example. |

## Recommendations

No P0. P1 (fix before production): shipped example halts/mis-colours; false maftools behaviour statements (printCount, ggplot2 object, point size, CDD not Pfam, longest RefSeq, proteinID); wrong domain coordinates and Ensembl id; g3viz `hgvspChange2protein` / `output.filename`; hard-coded `AACol='HGVSp_Short'` with wrong failure description. P2: undocumented HGVSp/recurrence semantics (rows vs samples, per-change stems, silent drops, clipped isoform positions); pyLollipop/Bio.PDB/ProteinPaint padding; redundant usage guide and label overlap. Full text in the JSON.

## Files
`run/00_explore.R` API/data probe | `01_make_synthetic.py` data + truth | `02_probe_svg.R`, `helpers.R` SVG parser | `03_maftools_laml.R` LAML blocks (as written / corrected, R882H 19 vs 19) | `04_maftools_synth.R` | `05_maftools_plot2.R` | `06_trackviewer.R`, `06b_trackviewer_na.R`, `07_png_measure.py` | `08_g3viz.R`, `09_g3viz_check.R` | `10_example_run.py`, `10_run_examples.sh` | `11_extras.R` | `12_factor_color.R` | `13_pylollipop_check.sh` | `build_report.py`. Logs beside each script. Data: `data/synthetic_lollipop.maf` (synthetic), `synthetic_clinical.tsv` (synthetic), `synthetic_truth.json`, `P04637_uniprot.json`, `P01116_uniprot.json` (UniProt, CC-BY 4.0).
