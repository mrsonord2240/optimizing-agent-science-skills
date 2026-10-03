> **Audit record for `bio-data-visualization-volcano-and-ma-plots`**
> - Audited working candidate `a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/volcano-and-ma-plots), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-volcano-and-ma-plots

Generated: 2026-10-03  
Audit type: delta re-audit (text-only changes to certified bytes)  
Exact candidate content SHA-256: `a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83` (files=7, bytes=37959)  
Certified baseline (carried forward): `fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008` (files=7, bytes=37956), record `candidate@fa3ec8783a79-reaudit-dv1-20261003`

## Delta qualification

- `skill_preflight --offline` on the candidate: PASS, identity a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83, files=7, bytes=37959.
- Reverting the edit pairs listed in the fix log on a scratch copy (`scripts/d1_revert.py`, `scratch/`) reproduces the certified identity exactly.
- Changed files differ only in prose, comments or string literals (per-file diffs in `scripts/diff_*.txt`).
- `scripts/volcano_phd.R`: `deparse(parse(keep.source = FALSE))` identical to the certified bytes (50 lines, `scripts/r_ast_compare.R`); script re-run once, exit 0.
- Environment fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 over `snapshots/lane1_versions.txt`, re-hashed identical at start and end.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 33 | 49 | 82 | 4/5 | ✅ COMPLETED |
| 3 | Variant B | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 4 | Edge | 35 | 54 | 89 | 4/4 | ✅ COMPLETED |
| 5 | Stress | 35 | 54 | 89 | 5/5 | ✅ COMPLETED |

**Execution average:** 88.8 / 100  
**Assertion pass rate:** 23 / 24 (95.8 %)  
**Static score:** 89 / 100  
**Final score:** 89 / 100 — ⭐ Production Ready  
**Research veto:** PASS

Readiness decision: **candidate-ready** for this exact identity (89 final, static 89, execution average 88.8, assertions 23/24, no veto, no open P0 or P1; open P2: VOL-010). Scores are the certifying report's, re-scored only where the change touches (see below).

## Finding verdicts

| Finding | Verdict | Evidence |
|---|---|---|
| VOL-009 (P2) stale quoted numbers | corrected (closed) | failure-modes.md and reconciliation: 39 hidden genes = 39 re-measured (`scripts/logs/d1_cap50.log`); SKILL.md median 0.76 = round(0.7648) (`scripts/logs/d1_stats.log`); volcano_phd.R comment 17,994 drawn points, 0.56 / 0.69 MB = 555,573 / 685,915 B decimal MB (`scripts/logs/d1_core.log`); MA 23/444 KB tied to all 29,391 rows = 23 / 444 KB measured on 29,391 rows (`scripts/logs/d1_ma.log`) |
| VOL-010 (P2) y_cap labels pile onto the cap | open, untouched | no change in the delta (needs code); certifying evidence stands |
| Other certified findings and passes | carried forward unchanged | scripts' executable statements are byte-for-byte equivalent (R parse identical); untouched assertions are the certifying run's |

## Executed versus carried

| Surface | Classification | Evidence |
|---|---|---|
| `scripts/volcano_phd.R` (comment-only edit) | executed | `scripts/d1_core.R`, `scripts/logs/d1_core.log`: ran to the end on the fitted airway dds, exit 0, RESULT PASS; volcano.pdf 555,573 B, ma_plot.pdf 685,915 B; counts, boundary and EnhancedVolcano colours as certified |
| Changed numeric claims (39 genes, median, MA sizes) | executed | `scripts/r2b_cap50.R`, `scripts/r3_stats_claims.R`, `scripts/r5_ma_python.py` re-run on the candidate; the r3 script's own '0.77' assertion is the stale pre-fix claim and fails by design, the Skill now says 0.76 |
| `scripts/volcano_plot.R`, `scripts/ma_plot.py` bytes | carried (hash-identical) | certifying run `reaudit-dv1-20261003`; ma_plot.py also re-run above |
| SKILL.md R blocks, sanbomics and shrinkage statements | carried | certifying run; prose around them unchanged except the two edited sentences |

## Veto review

- Skill veto: PASS (stability, contract, determinism, security all PASS); carried, no executable byte changed.
- Research veto: PASS
  - scientific_integrity: PASS — Quoted airway counts re-measured; two stale numbers (49 vs 39 hidden genes, median 0.77 vs 0.76) are minor and recorded as VOL-009, none are fabricated identifiers or results.
  - practice_boundaries: PASS — Plotting guidance only; no clinical or prescriptive content.
  - methodological_ground: PASS — Plotted quantity -log10(padj) equals the threshold line quantity; Up/Down colour boundary equals the line; 817 significant genes plotted equals 817 in the table; shrunken LFC used and svalue/apeglm/ashr statements verified.
  - code_usability: PASS — volcano_phd.R, volcano_plot.R, ma_plot.py and all three SKILL.md R blocks run verbatim on the airway dds; no unrunnable code found.

## Static categories

- functional_suitability: 11/12 — Covers shrinkage choice, ggplot2, EnhancedVolcano, MA and sanbomics with verified API facts; the quoted airway numbers now equal the re-measured values (VOL-009 closed); the capped-axis labelling is still unreadable (VOL-010).
- reliability: 11/12 — NA padj reported, absent label genes warn, zero-length repel segments suppressed; the cap-with-top-labels path still overplots.
- performance_context: 7/8 — SKILL.md about 160 lines with detail routed to two references; some measured numbers repeat across four files.
- agent_usability: 15/16 — Operational rule and design choices are explicit and each tested; the numbers in failure-modes and reconciliation now match a re-measurement on real data (39 hidden genes, median 0.7648 printed as 0.76).
- human_usability: 7/8 — Natural trigger language and example prompts; the y_cap prompt in usage-guide produces overlapping labels.
- security: 11/12 — No credentials, network or shell strings; local plot files only.
- maintainability: 10/12 — Three scripts with documented signatures and comments; no test ties the quoted counts to the airway data, so they drifted when the y axis changed.
- agent_specific: 17/20 — Precise trigger, version note, escape hatches for raw-p input and svalue; Python volcano labelling is only pointed at, not shipped.

## Detailed outputs

### Input 1 — Canonical: scripts/volcano_phd.R unchanged on the fitted airway dds (29,391 genes, 17,994 with padj): volcano, MA, cairo_pdf, EnhancedVolcano

**Status:** COMPLETED — Ran to the end; both PDFs at stated size, TrueType, counts and boundary consistent, EnhancedVolcano Up and Down differ.  
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100

**Assertions:**

- PASS — volcano.pdf and ma_plot.pdf have the stated 89x90 and 89x70 mm page sizes. (pdfinfo 252x255 pt and 252x198 pt (88.9x90.0 and 88.9x69.9 mm).)
- PASS — pdffonts reports embedded TrueType only for both PDFs. (ArialMT, SymbolMT, Arial-ItalicMT TrueType, no Type 3.)
- PASS — The volcano plots every non-NA-padj gene and its Up and Down counts equal the table counts (451 Up, 366 Down). (17,994 points drawn; 451/366 coloured vs 451/366 in the shrunken results.)
- PASS — The dashed threshold line equals the colour boundary in the plotted quantity. (yintercept 1.30103 = -log10(0.05); all 817 coloured points at y>=1.349, all 14,000 points below the line grey.)
- PASS — The EnhancedVolcano figure colours Up orange and Down blue, labels TP53/MYC/BRCA1 and names the adjusted P axis. (Distinct #D55E00/#0072B2/#999999; figure opened, labels present, y label adjusted P.)

### Input 2 — Variant A: scripts/volcano_plot.R volcano_plot(): uncapped, y_cap = 30, other fdr/lfc cutoffs, absent label gene

**Status:** COMPLETED — Counts and boundaries are exact with and without the cap; capped labels collide.  
**Scores:** Basic 33/40 | Specialized 49/60 | Total 82/100

**Assertions:**

- PASS — Without y_cap every non-NA-padj gene is plotted, Up/Down equal the table, the maximum y is 131 and the NA count is reported. (17,994 points; 451/366; max 131.4; message '11397 genes with padj = NA are not drawn'.)
- PASS — With y_cap = 30 no gene is dropped, capped genes are exactly those above 30 and are triangles with a legend entry. (118 triangles (115 significant) = genes with -log10(padj)>30; all 17,994 still plotted; legend 'capped at 30'.)
- PASS — The threshold line equals the colour boundary for fdr 0.05 and for fdr 0.01 with lfc 1.5, with and without the cap. (hline at 1.301 and 2.0; coloured points on or above it; vlines at +-1.5.)
- PASS — An absent label gene warns by name and a plain data.frame input works. (Warning names NOT_A_GENE; 3,000-row data.frame ran.)
- FAIL — The y_cap = 30 figure with default top-10 labels is legible at 89 mm. (Several top-rank labels all sit at y = 30 and print on top of each other (DUSP1, SAMHD1, ZBTB16, SPARCL1, GPX3) (VOL-010).)

### Input 3 — Variant B: Every SKILL.md R block verbatim: DESeq + lfcShrink apeglm/ashr/svalue, EnhancedVolcano with colCustom, plotMA; shrinkage and svalue statements

**Status:** COMPLETED — All three blocks ran verbatim; svalue, contrast, normal and default-type statements reproduce.  
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100

**Assertions:**

- PASS — All three SKILL.md R blocks execute verbatim without error. (DESeq refit and three lfcShrink calls 80 s; EnhancedVolcano with setNames(okabe_ito[sig], sig); plotMA wrote a plot.)
- PASS — The EnhancedVolcano block draws Up and Down in different colours matching the table counts. (#D55E00 count = 451, #0072B2 count = 366.)
- PASS — svalue = TRUE returns columns baseMean, log2FoldChange, lfcSE, svalue (no pvalue/padj) for apeglm and ashr and errors for type='normal'. (Columns identical; normal errors (object 'coefAlphaSpaces' not found).)
- PASS — apeglm rejects contrast=, ashr accepts coef=, and the default lfcShrink type is apeglm in DESeq2 1.46.0. (apeglm error 'only for use with coef'; ashr coef ran; formals first choice apeglm.)
- PASS — The s-value and shrinkage counts reproduce (4,684 vs 3,994, 3,842 shared; 108 genes raised by apeglm, ashr 0, 9.51 to 10.99). (All reproduced exactly on the airway dds.)

### Input 4 — Edge: scripts/ma_plot.py on the real shrunken airway table, matplotlib size claim, sanbomics.plots.volcano statements

**Status:** COMPLETED — ma_plot draws all 29,391 rows; sanbomics statements reproduce; size claim reproduces on all rows.  
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**

- PASS — ma_plot() draws every row and colours exactly the padj<0.05 genes orange. (25,397 grey + 3,994 orange = 29,391; 3,994 equals the table.)
- PASS — The rasterized-versus-vector size statement (23 KB vs 444 KB) reproduces for ma_plot() at 3.5 x 3 in. (444 KB vector, 23 KB rasterized on all 29,391 rows.)
- PASS — sanbomics.plots.volcano exists with symbol and padj defaults and draws every DE point in one grey class, no Up/Down colours; sanbomics.tools is not importable. (1,319 DE points (701+618) in dimgrey/black, legend DE/not DE/picked; sanbomics.tools fails on pkg_resources.)
- PASS — The matplotlib MA figure is legible and shows the low-count fan with significant genes highlighted. (Opened: axes labelled, orange significant, grey fan at low baseMean.)

### Input 5 — Stress: failure-modes.md and reconciliation-thresholds-pushback.md quoted behaviours and numbers re-measured

**Status:** COMPLETED — API behaviour reproduces and the quoted numbers equal the re-measured values: cap 50 hides 39 significant genes, median |LFC| 0.7648 (printed 0.76), 17,994 drawn points, PDFs 555,573 and 685,915 B (0.56 and 0.69 MB), MA 444/23 KB on all 29,391 rows.  
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**

- PASS — selectLab keeps a listed non-significant gene, ignores a name absent from lab and an NA-padj gene, and EnhancedVolcano draws only non-NA-padj rows. (SCYL3 (padj 0.91) labelled; absent and NA genes not drawn; 17,994 of 29,391 points drawn.)
- PASS — Default EnhancedVolcano col gives Up and Down one shared colour and ggbreak scale_y_break draws on the volcano. (817 points in one colour; ggbreak PNG written.)
- PASS — Rasterizing the point layer cuts the 17,994-point PDF by an order of magnitude. (ggrastr 1.0.2: 540 to 38 KB on a bare geom_point plot; 638 to 66 KB with the volcano's alpha and size.)
- PASS — Measured numbers quoted in the references equal re-measured values. (39 hidden genes (r2b), 0.7648 printed as 0.76 (r3), 17,994 drawn points and 555,573 / 685,915 B PDFs (d1_core), 444 / 23 KB on 29,391 rows (r5), all re-run on the candidate bytes.)
- PASS — The common-errors table and reviewer pushback rows give correct actions for padj=NA, threshold-line mismatch and max.overlaps. (Verified by the line-versus-boundary assertions and the NA-count message.)

## Key strengths

- The plotted quantity, threshold line and colour boundary now agree exactly: -log10(padj) on y, line at 1.30103, 817 significant genes plotted equals 817 in the table, with and without y_cap.
- y_cap draws capped genes as marked triangles with a legend entry and none are dropped (118 triangles, 115 significant), replacing the old silent clipping.
- EnhancedVolcano Up and Down now differ via colCustom; svalue, apeglm contrast, ashr coef and sanbomics.plots.volcano statements reproduce on the real airway dds.
- All shipped code and all three SKILL.md R blocks run verbatim; PDFs are exact mm with embedded TrueType.

## Recommendations

- **[P2] VOL-010 y_cap labels pile onto the cap and overlap** (inputs [2]): volcano_plot(res, y_cap = 30) with default top_n labels places every high-rank label at y = 30, where ggrepel with max.overlaps = Inf prints them on top of each other; usage-guide suggests exactly this cap. Fix: Document label_genes with capped genes excluded or spread horizontally (direction = 'x', ylim expansion), or default top_n labels to genes below the cap.
