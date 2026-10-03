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
