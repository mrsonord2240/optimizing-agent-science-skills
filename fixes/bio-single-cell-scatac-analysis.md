# bio-single-cell-scatac-analysis — fix log (2026-09-19)

Fixer for `single-cell/scatac-analysis` (fork branch `fix/sc-atac`, worktree
`F:\OpenScience\wt\sc-atac`, commit `1935af7`). Source audit: 89/100,
Limited Release, deployable, no P0, 2 P1s open (23/26 assertion pass rate
missed the 90% Production Ready floor by a fraction). Env:
`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (Signac
1.17.1, chromVAR 1.28.0, motifmatchr 1.28.0, JASPAR2020,
BSgenome.Hsapiens.UCSC.hg38) — reused as-is; no installs, no version
changes. `biovizBase` and `Rsamtools` were already installed into this
shared env by the auditor (0 version changes recorded in `TOOLS.md`).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `SKILL.md`'s documented `RunChromVAR(obj, genome=...)` throws `could not find function "RunChromVAR"` on Signac 1.17.1 — removed upstream in Signac 1.17.0 because chromVAR became unavailable in Bioconductor 3.23 (Signac's own NEWS.md) | P1 | `SKILL.md` chromVAR section: replaced the `RunChromVAR()` call with chromVAR's own `addGCBias`/`matchMotifs`/`getBackgroundPeaks`/`computeDeviations` sequence (the same steps `RunChromVAR()` used to wrap), plus `BiocParallel::register(SerialParam())` since the default multicore backend hangs silently on Windows | ran — copied the audit's real synthetic `obj_qc.rds` (270 cells x 222 peaks) to scratch and executed the exact replacement block independently of the audit's own script: confirmed `RunChromVAR` absent from the Signac namespace, then produced a real 746-motif x 270-cell deviation matrix, 225 differential motifs with p-values, and named top TFs (GATA5/GATA4/GATA3/GATA2/Lhx3) | version-proof going forward: this is chromVAR's stable public API, not the removed wrapper, so it does not break again on the next Signac release the way the old call did |
| `biovizBase` is a required but undocumented dependency — `GetGRangesFromEnsDb()` throws `Please install biovizBase` unless already present | P1 | `usage-guide.md` Prerequisites: added `biovizBase` to the `BiocManager::install()` list with an inline comment naming the call that needs it | checked against the audit's own captured error and confirmed the package is genuinely needed by `GetGRangesFromEnsDb()`, used throughout `SKILL.md`'s QC section and `examples/signac_workflow.R` | `Rsamtools` (also installed by the auditor) was **not** added — it is a dependency of the auditor's own synthetic-fragment-file generation (bgzip/tabix), not of anything the Skill itself documents or calls; real 10x fragments.tsv.gz already arrive bgzipped/tabixed from CellRanger-ATAC |

All 6 R code blocks in `SKILL.md` re-parsed clean after the edit
(`Rscript -e "parse('block.R')"` per block, via the env's `tools/rs.sh`
wrapper).

## Findings fixed: 2/2 P1s. No P2s touched (all 4 are either substantial
additions — escape-hatch section, independent chromVAR-determinism rerun —
or scoped restructuring beyond a cheap fix (NucleosomeSignal/TSSEnrichment/
StringToGRanges deprecation-warning update); left for a future pass, not a
correction in scope here.
