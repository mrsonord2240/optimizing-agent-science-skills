# bio-data-visualization-volcano-and-ma-plots fix pass - 2026-10-03

`volcano_phd.R` capped the y axis at 50 unconditionally, hiding 39 significant genes on airway, and both volcano scripts drew the FDR threshold line on a raw-p axis, away from the colour boundary. The default is now no cap (an optional cap draws capped points as triangles) and the y axis is `-log10(padj)`, so the line is the colour boundary and all 817 significant genes are plotted. EnhancedVolcano Up and Down now take different colours, the `sanbomics` call uses the function that exists, the `svalue`, `selectLab` and apeglm-versus-MLE statements say what was measured, and unreproduced file-size claims were replaced by measurements. Later text-only passes corrected stale quoted numbers and reduced the frontmatter description to its trigger.

- Final candidate audit: `audits/skills/bio-data-visualization-volcano-and-ma-plots/candidate@0bc1e67d46d6-delta-desc-20261003`
- Result: **89/100, Production Ready**; open P2 VOL-010 (capped labels overprint at the cap).
- Candidate identity: `0bc1e67d46d6b7cfdffd1d42ef1f35779a7f0fe712d8460e3ee602684bd4aeeb`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.
