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

---

## 2026-09-19 — fix round 2 (T3 determinism veto)

Fixer for `single-cell/scatac-analysis` (fork branch `fix/sc-atac`, worktree
`F:\OpenScience\wt\sc-atac`, commit `4c65703`, on top of round 1's `1935af7`).
Source: the re-audit that independently re-verified round 1's two P1 fixes as
correct, then found a **new** defect while doing so — `chromVAR`'s
`getBackgroundPeaks()` is unseeded, giving 24/4/4 significant motifs and only
3/10 top-motif overlap across 3 reruns of the same object. This fired a T3
Result Determinism Skill Veto, forcing the Skill from 89 (Limited Release) to
a diagnostic Reject; it was pulled off the published shelf pending this fix.
Report: `F:\OpenScience\audits\bio-single-cell-scatac-analysis\eval_viewer_bio-single-cell-scatac-analysis.md`.
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` — reused
as-is, no installs, no version changes.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `chromVAR::getBackgroundPeaks()` is unseeded — SKILL.md's documented chromVAR block gave different differential-motif results (24/4/4 significant motifs, 3/10 top-10 overlap) across identical reruns of the same object | P1 (T3 Skill Veto) | `SKILL.md` chromVAR section: added `set.seed(1)` immediately before the `getBackgroundPeaks()` call | ran — copied the re-audit's `obj_qc.rds` (160 cells, 3 cell types) to scratch and ran the exact documented block as a fresh function call 4 times: byte-identical `bg_peaks` and z-score matrices, 10/10 top-10 motif overlap, identical significant-motif counts (4/4/4/4) across all 4 runs; confirmed `computeDeviations()` is already deterministic given identical background peaks, so seeding only `getBackgroundPeaks()` is sufficient | this is the exact fix the re-audit itself validated; independently reconfirmed here rather than trusted |
| Common Errors table still named the dead `RunChromVAR()` function (removed by round 1's own fix) as an option for GC-rich-background troubleshooting | P2 (internal contradiction, cheap) | Replaced with the current `getBackgroundPeaks()` API; added a new row for the determinism failure mode and its fix | re-read against the corrected chromVAR section above — no remaining `RunChromVAR` mentions in the file | found incidentally while fixing the determinism issue in the same table |

All 6 R code blocks in `SKILL.md` re-parsed clean after the edit
(`Rscript -e "parse(file=...)"` per block, via the env's `tools/rs.sh`
wrapper).

### Findings fixed: 1/1 P1 (the T3 veto). 1 incidental P2 fixed (dead
`RunChromVAR` reference). 2 pre-existing P2s from round 1 re-checked and
still left unfixed:
- **Escape-hatch section** — still a substantial addition, not a correction.
- **NucleosomeSignal()/TSSEnrichment() deprecation** — checked further this
  round: Signac's replacement `ATACqc()` is not a drop-in swap, it requires
  an external `fragtk.path` binary (confirmed via `getAnywhere("ATACqc.Seurat")`
  in the audit env), so this remains beyond a cheap fix.

Not merged, not re-audited — per dispatch, that is a separate agent's job.
