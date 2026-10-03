> **Audit record for `bio-data-visualization-volcano-and-ma-plots`**
> - Audited working candidate `fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/data-visualization/volcano-and-ma-plots), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-volcano-and-ma-plots

Generated: 2026-10-03  
Audit type: independent final re-audit (certification), fresh auditor  
Exact candidate content SHA-256: `fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 2 | Variant A | 33 | 49 | 82 | 4/5 | ✅ COMPLETED |
| 3 | Variant B | 36 | 56 | 92 | 5/5 | ✅ COMPLETED |
| 4 | Edge | 35 | 54 | 89 | 4/4 | ✅ COMPLETED |
| 5 | Stress | 31 | 48 | 79 | 4/5 | ✅ COMPLETED |

**Execution average:** 86.8 / 100 (Layer 1 avg 34.2 / 40, Layer 2 avg 52.6 / 60)  
**Assertion pass rate:** 22 / 24 (91.7 percent)  
**Static score:** 87 / 100  
**Final score:** 87 / 100 - ⭐ Production Ready  
**Research veto:** PASS

## Readiness decision

**Candidate-ready** for the exact identity above. Gate: final 87, static 87, execution average 86.8, Layer 1 average 34.2, Layer 2 average 52.6, assertion pass rate 22/24 = 91.7 percent, no veto, no open P0, and an inspected execution for every output family (ggplot2 volcano and MA PDFs, EnhancedVolcano, matplotlib MA, sanbomics, R and Python scripts). Two open P2 findings (VOL-009, VOL-010) are not blocking; both are text-level fixes (VOL-010 may touch about a dozen script lines) and are listed for the orchestrator.

## Prior findings (initial audit b94e14b191a0, Beta Only 70), each retested here

| ID | Sev | Verdict | Independent evidence (scripts/logs) |
|---|---|---|---|
| VOL-001 | P1 | resolved | no cap by default: 17,994 of 17,994 non-NA genes and 817 of 817 significant plotted; y_cap=30 keeps all genes, 118 triangles (115 significant), legend entry, hline unchanged (r1, r2) |
| VOL-002 | P1 | resolved | y = -log10(padj); hline 1.30103 equals -log10(0.05); coloured points all at y>=1.349, all 14,000 points below the line grey; also fdr 0.01 / lfc 1.5 (r1, r2) |
| VOL-003 | P2 | resolved | EnhancedVolcano with colCustom: Up #D55E00 (451), Down #0072B2 (366); default col shares one colour for 817 points; y label adjusted P (r1, r3, r6) |
| VOL-004 | P2 | resolved | svalue=TRUE returns baseMean, log2FoldChange, lfcSE, svalue for apeglm and ashr, no padj; type='normal' errors; default has no svalue (r3) |
| VOL-005 | P2 | resolved | sanbomics.plots.volcano exists, symbol and padj defaults, DE points one grey class (1,319 = 701+618), sanbomics.tools not importable (r5) |
| VOL-006 | P2 | resolved | selectLab keeps a non-significant listed gene (SCYL3 padj 0.91), ignores absent and NA-padj names; EnhancedVolcano draws 17,994 of 29,391 rows (r3) |
| VOL-007 | P2 | resolved | apeglm exceeds MLE in 108 of 29,391 genes (9.51 to 10.99, largest +1.48, median baseMean 1444), ashr 0; s-value counts 4,684 / 3,994 / 3,842 (r3) |
| VOL-008 | P2 | resolved | 5 MB+/crash claims gone; measured sizes: volcano.pdf 0.56 MB, ma_plot.pdf 0.69 MB, ggrastr 540 to 38 KB (bare plot), MA 444 to 23 KB (r1, r4, r5) |

Fixer-added inline changes retested: zero-length repel segments no longer draw blobs (min.segment.length 0.3; volcano and EnhancedVolcano figures opened), padj=NA message ('11397 genes with padj = NA are not drawn'), missing-label warning by name. New findings VOL-009 and VOL-010 are not regressions of the fix; they are residues the fix left or defects it did not reach.

## Executed versus static-only

| Surface | Class | Evidence |
|---|---|---|
| scripts/volcano_phd.R (apeglm, volcano, MA, cairo_pdf, EnhancedVolcano) | executed | r1, pdfinfo, pdffonts, figures opened |
| scripts/volcano_plot.R volcano_plot() with/without y_cap, thresholds, labels, data.frame | executed | r2, figures opened |
| SKILL.md R blocks (lfcShrink, EnhancedVolcano colCustom, plotMA) | executed | r6 |
| svalue, apeglm/ashr/normal, selectLab, EnhancedVolcano NA, default colours, shrinkage numbers | executed | r3 |
| scripts/ma_plot.py on real shrunken table, size claims | executed | r5, r4 |
| sanbomics.plots.volcano | executed | r5 |
| ggbreak scale_y_break | executed | r2 |
| edgeR glmTreat paragraph | static-only | prose; tooling smoke exists, not rerun here |
| usage-guide.md prompts and prerequisites | static-only | prose |

Environment: fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (R 4.4.3, DESeq2 1.46.0, apeglm 1.28.0, ashr 2.2.63, EnhancedVolcano 1.24.0, ggplot2 4.0.3, ggrastr 1.0.2; Python matplotlib 3.11.2, sanbomics 0.1.0 from py-extra). Input: staged fitted airway dds (29,391 genes; 17,994 with padj). pdffonts and pdfinfo through the recorded WSL dv-cli route.

## Veto review

- Skill veto: PASS.
- Research veto: PASS
  - scientific_integrity: PASS - Quoted airway counts re-measured; two stale numbers (49 vs 39 hidden genes, median 0.77 vs 0.76) are minor and recorded as VOL-009, none are fabricated identifiers or results.
  - practice_boundaries: PASS - Plotting guidance only; no clinical or prescriptive content.
  - methodological_ground: PASS - Plotted quantity -log10(padj) equals the threshold line quantity; Up/Down colour boundary equals the line; 817 significant genes plotted equals 817 in the table; shrunken LFC used and svalue/apeglm/ashr statements verified.
  - code_usability: PASS - volcano_phd.R, volcano_plot.R, ma_plot.py and all three SKILL.md R blocks run verbatim on the airway dds; no unrunnable code found.

## Static categories

- functional_suitability: 10/12 - Covers shrinkage choice, ggplot2, EnhancedVolcano, MA and sanbomics with verified API facts; some quoted airway numbers are stale (VOL-009) and the capped-axis labelling is unreadable (VOL-010).
- reliability: 11/12 - NA padj reported, absent label genes warn, zero-length repel segments suppressed; the cap-with-top-labels path still overplots.
- performance_context: 7/8 - SKILL.md about 160 lines with detail routed to two references; some measured numbers repeat across four files.
- agent_usability: 14/16 - Operational rule and design choices are explicit and each tested; stale numbers in failure-modes and reconciliation could mislead a check against real data.
- human_usability: 7/8 - Natural trigger language and example prompts; the y_cap prompt in usage-guide produces overlapping labels.
- security: 11/12 - No credentials, network or shell strings; local plot files only.
- maintainability: 10/12 - Three scripts with documented signatures and comments; no test ties the quoted counts to the airway data, so they drifted when the y axis changed.
- agent_specific: 17/20 - Precise trigger, version note, escape hatches for raw-p input and svalue; Python volcano labelling is only pointed at, not shipped.

## Detailed outputs

### Input 1 - Canonical: scripts/volcano_phd.R unchanged on the fitted airway dds (29,391 genes, 17,994 with padj): volcano, MA, cairo_pdf, EnhancedVolcano

**Status:** COMPLETED - Ran to the end; both PDFs at stated size, TrueType, counts and boundary consistent, EnhancedVolcano Up and Down differ.  
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100

**Assertions:**

- PASS - volcano.pdf and ma_plot.pdf have the stated 89x90 and 89x70 mm page sizes. (pdfinfo 252x255 pt and 252x198 pt (88.9x90.0 and 88.9x69.9 mm).)
- PASS - pdffonts reports embedded TrueType only for both PDFs. (ArialMT, SymbolMT, Arial-ItalicMT TrueType, no Type 3.)
- PASS - The volcano plots every non-NA-padj gene and its Up and Down counts equal the table counts (451 Up, 366 Down). (17,994 points drawn; 451/366 coloured vs 451/366 in the shrunken results.)
- PASS - The dashed threshold line equals the colour boundary in the plotted quantity. (yintercept 1.30103 = -log10(0.05); all 817 coloured points at y>=1.349, all 14,000 points below the line grey.)
- PASS - The EnhancedVolcano figure colours Up orange and Down blue, labels TP53/MYC/BRCA1 and names the adjusted P axis. (Distinct #D55E00/#0072B2/#999999; figure opened, labels present, y label adjusted P.)

### Input 2 - Variant A: scripts/volcano_plot.R volcano_plot(): uncapped, y_cap = 30, other fdr/lfc cutoffs, absent label gene

**Status:** COMPLETED - Counts and boundaries are exact with and without the cap; capped labels collide.  
**Scores:** Basic 33/40 | Specialized 49/60 | Total 82/100

**Assertions:**

- PASS - Without y_cap every non-NA-padj gene is plotted, Up/Down equal the table, the maximum y is 131 and the NA count is reported. (17,994 points; 451/366; max 131.4; message '11397 genes with padj = NA are not drawn'.)
- PASS - With y_cap = 30 no gene is dropped, capped genes are exactly those above 30 and are triangles with a legend entry. (118 triangles (115 significant) = genes with -log10(padj)>30; all 17,994 still plotted; legend 'capped at 30'.)
- PASS - The threshold line equals the colour boundary for fdr 0.05 and for fdr 0.01 with lfc 1.5, with and without the cap. (hline at 1.301 and 2.0; coloured points on or above it; vlines at +-1.5.)
- PASS - An absent label gene warns by name and a plain data.frame input works. (Warning names NOT_A_GENE; 3,000-row data.frame ran.)
- FAIL - The y_cap = 30 figure with default top-10 labels is legible at 89 mm. (Several top-rank labels all sit at y = 30 and print on top of each other (DUSP1, SAMHD1, ZBTB16, SPARCL1, GPX3) (VOL-010).)

### Input 3 - Variant B: Every SKILL.md R block verbatim: DESeq + lfcShrink apeglm/ashr/svalue, EnhancedVolcano with colCustom, plotMA; shrinkage and svalue statements

**Status:** COMPLETED - All three blocks ran verbatim; svalue, contrast, normal and default-type statements reproduce.  
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100

**Assertions:**

- PASS - All three SKILL.md R blocks execute verbatim without error. (DESeq refit and three lfcShrink calls 80 s; EnhancedVolcano with setNames(okabe_ito[sig], sig); plotMA wrote a plot.)
- PASS - The EnhancedVolcano block draws Up and Down in different colours matching the table counts. (#D55E00 count = 451, #0072B2 count = 366.)
- PASS - svalue = TRUE returns columns baseMean, log2FoldChange, lfcSE, svalue (no pvalue/padj) for apeglm and ashr and errors for type='normal'. (Columns identical; normal errors (object 'coefAlphaSpaces' not found).)
- PASS - apeglm rejects contrast=, ashr accepts coef=, and the default lfcShrink type is apeglm in DESeq2 1.46.0. (apeglm error 'only for use with coef'; ashr coef ran; formals first choice apeglm.)
- PASS - The s-value and shrinkage counts reproduce (4,684 vs 3,994, 3,842 shared; 108 genes raised by apeglm, ashr 0, 9.51 to 10.99). (All reproduced exactly on the airway dds.)

### Input 4 - Edge: scripts/ma_plot.py on the real shrunken airway table, matplotlib size claim, sanbomics.plots.volcano statements

**Status:** COMPLETED - ma_plot draws all 29,391 rows; sanbomics statements reproduce; size claim reproduces on all rows.  
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**

- PASS - ma_plot() draws every row and colours exactly the padj<0.05 genes orange. (25,397 grey + 3,994 orange = 29,391; 3,994 equals the table.)
- PASS - The rasterized-versus-vector size statement (23 KB vs 444 KB) reproduces for ma_plot() at 3.5 x 3 in. (444 KB vector, 23 KB rasterized on all 29,391 rows.)
- PASS - sanbomics.plots.volcano exists with symbol and padj defaults and draws every DE point in one grey class, no Up/Down colours; sanbomics.tools is not importable. (1,319 DE points (701+618) in dimgrey/black, legend DE/not DE/picked; sanbomics.tools fails on pkg_resources.)
- PASS - The matplotlib MA figure is legible and shows the low-count fan with significant genes highlighted. (Opened: axes labelled, orange significant, grey fan at low baseMean.)

### Input 5 - Stress: failure-modes.md and reconciliation-thresholds-pushback.md quoted behaviours and numbers re-measured

**Status:** COMPLETED - API behaviour reproduces; three quoted numbers are stale or off.  
**Scores:** Basic 31/40 | Specialized 48/60 | Total 79/100

**Assertions:**

- PASS - selectLab keeps a listed non-significant gene, ignores a name absent from lab and an NA-padj gene, and EnhancedVolcano draws only non-NA-padj rows. (SCYL3 (padj 0.91) labelled; absent and NA genes not drawn; 17,994 of 29,391 points drawn.)
- PASS - Default EnhancedVolcano col gives Up and Down one shared colour and ggbreak scale_y_break draws on the volcano. (817 points in one colour; ggbreak PNG written.)
- PASS - Rasterizing the point layer cuts the 17,994-point PDF by an order of magnitude. (ggrastr 1.0.2: 540 to 38 KB on a bare geom_point plot; 638 to 66 KB with the volcano's alpha and size.)
- FAIL - Measured numbers quoted in the references equal re-measured values. ('cap of 50 hid 49 significant genes' is 39; 'median |LFC| 0.77' is 0.7648; volcano_phd.R comment says 29,391 vector points ~1 MB but 17,994 are drawn and the PDFs are 0.56 and 0.69 MB; SKILL.md ties 23/444 KB to 17,994 points but ma_plot() draws 29,391 (VOL-009).)
- PASS - The common-errors table and reviewer pushback rows give correct actions for padj=NA, threshold-line mismatch and max.overlaps. (Verified by the line-versus-boundary assertions and the NA-count message.)

## Key strengths

- The plotted quantity, threshold line and colour boundary now agree exactly: -log10(padj) on y, line at 1.30103, 817 significant genes plotted equals 817 in the table, with and without y_cap.
- y_cap draws capped genes as marked triangles with a legend entry and none are dropped (118 triangles, 115 significant), replacing the old silent clipping.
- EnhancedVolcano Up and Down now differ via colCustom; svalue, apeglm contrast, ashr coef and sanbomics.plots.volcano statements reproduce on the real airway dds.
- All shipped code and all three SKILL.md R blocks run verbatim; PDFs are exact mm with embedded TrueType.

## Recommendations

- **[P2] VOL-009 Stale quoted numbers in references and comments** (inputs [5]): failure-modes.md and reconciliation-thresholds-pushback.md say a cap of 50 hid 49 significant genes (39 measured now that y is padj); SKILL.md says median |LFC| 0.77 (0.7648); the volcano_phd.R save comment says 29,391 vector points gave about 1 MB (17,994 are drawn; 0.56 and 0.69 MB); SKILL.md ties the 23/444 KB MA sizes to 17,994 points though ma_plot() draws 29,391. Fix: Replace 49 with 39, 0.77 with 0.76, the comment with 17,994 points and 0.56/0.69 MB, and state 29,391 rows for the MA sizes.
- **[P2] VOL-010 y_cap labels pile onto the cap and overlap** (inputs [2]): volcano_plot(res, y_cap = 30) with default top_n labels places every high-rank label at y = 30, where ggrepel with max.overlaps = Inf prints them on top of each other; usage-guide suggests exactly this cap. Fix: Document label_genes with capped genes excluded or spread horizontally (direction = 'x', ylim expansion), or default top_n labels to genes below the cap.
