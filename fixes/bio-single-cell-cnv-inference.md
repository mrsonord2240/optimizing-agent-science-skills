# bio-single-cell-cnv-inference — fix log (2026-09-19)

Fixer for `single-cell/cnv-inference` (fork branch `fix/sc-cnv`, worktree
`F:\OpenScience\wt\sc-cnv`, commit `6f65c08`). Source audit: 87/100,
Limited Release, deployable, no P0, 3 P1s open (assertion pass rate missed
the 90% Production Ready floor). Env: WSL2 "science" distro, conda env
`cnv-audit` (inferCNV 1.22.0, numbat 1.5.2, copyKAT 1.2.5, SCEVAN 1.0.3,
JAGS) — the original auditor's env, still present and reused as-is (no
installs, no version changes).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| inferCNV malignant-calling code reads `infercnv.observations.txt`, which 1.22's default HMM=TRUE no longer writes | P1 | `SKILL.md` + `examples/infercnv_malignant_calling.R`: replaced `read.table('infercnv_out/infercnv.observations.txt', ...)` with `readRDS('infercnv_out/run.final.infercnv_obj')`, indexing `@expr.data` by `@observation_grouped_cell_indices` | ran, against the audit's real `infercnv_out_input1/run.final.infercnv_obj` (inferCNV 1.22.0) | `cnv_score` correctly ranked the true CloneA cells highest, matching the audit's own result |
| Numbat `df_allele` documented with 7 columns; `check_allele_df()` also requires `cM`, `REF`, `ALT` | P1 | `SKILL.md`: added the 3 missing columns to the `df_allele` prose and to the parameter reference table, noted `cM` comes from the genetic-map file | checked against numbat 1.5.2's real `check_allele_df()` error text (matches the audit's captured error) | no code to re-run here (Numbat's real path needs a BAM/phasing this env doesn't have, per the audit's own note) |
| SCEVAN recommended in the method table with zero example code | P1 | `SKILL.md`: added a "SCEVAN - reference-free automatic malignant + subclone calling" section (code block + prose), matching the other 3 methods' depth; added `examples/scevan_calling.R` | ran end to end (exit 0) against the audit's synthetic panel, extended with copy-neutral filler genes across all 22 autosomes (SCEVAN's own per-chromosome coverage filter otherwise fails outright on the audit's 3-chromosome panel: "all cells are filtered") — correctly found 70/70 true CloneA cells as tumor and called the right chr7-gain/chr10-loss segments; see below | see caveat below |
| Parameter table missing copyKAT `min.gene.per.cell` and Numbat `cM`/`REF`/`ALT` | P2 | `SKILL.md`: added both to the parameter reference table (Numbat row folded into the `df_allele` fix above); also added SCEVAN's `ngenes_chr` | n/a (table-only) | cheap, in scope, done alongside the P1s |
| No clinical-boundary disclaimer near Governing Principle | P2 | not fixed | — | out of this pass's "correction" scope; content addition, not a defect fix |
| No patient-privacy note | P2 | not fixed | — | same reason |

## SCEVAN caveat (found during verification, documented in the fix)

`pipelineCNA()` has no `plot=FALSE` argument — it unconditionally writes
heatmap/segment PNGs to `./output/` as a side effect of the call. On the
audit's synthetic cohort (150 cells, one dominant clone, extended to span
all 22 autosomes) this internal plotting step reliably throws
(`arguments imply differing number of rows: 0, 70`, inside
`heatmapConsensusPlot`/`plotTSNE`) *after* classification has already
completed and printed `"found 70 tumor cells"` — the correct count.
Reproduced under every `SUBCLONES`/`ClonalCN` combination tried (`TRUE`/
`TRUE`, `FALSE`/`TRUE`, `FALSE`/`FALSE`); the failure moves between
`plotCNclonal → heatmapConsensusPlot` and `subcloneAnalysisPipeline →
plotTSNE` but never goes away, and there is no parameter that skips
plotting. This is a real, reproducible SCEVAN 1.0.3 behavior, not an
install issue — documented in `SKILL.md`'s new SCEVAN section, the
parameter table isn't the right place for it so it's in prose plus two new
Common Errors rows, and both `SKILL.md`'s code block and
`examples/scevan_calling.R` wrap the call in `tryCatch()` so a user still
gets the (already-correct) classification instead of a script abort.
Verified by rerunning the exact shipped `examples/scevan_calling.R` file
end to end (exit 0, `"found 70 tumor cells"` in the log, `tryCatch`
message printed, script reaches `"SCEVAN complete"`).

Not filed upstream (out of scope for this pass); worth a GitHub issue
against `AntonioDeFalco/SCEVAN` if anyone picks it up later.

## Findings fixed: 4/6 (3 P1 + 1 P2); 2 P2 left unfixed (reasons above)
