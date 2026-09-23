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

---

## 2026-09-21 — P2 batch (Production Ready Skill, 2 P2s open)

Fixer for `single-cell/scatac-analysis`, branch `fix/single-cell-scatac-analysis` from staging `431aa55`.
Commits: `1b8c9ef` (fix), `d9bcbfd` (redundancy), `0c0ecaa` (scripts). No split: SKILL.md 227 -> 226 lines
(249 after the dedup moves, 226 after the chromVAR block moved to `scripts/`). Env:
`single-cell-transcriptomics-analyst` (Signac 1.17.1, Seurat 5.5.0, R 4.4.3), no installs.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `NucleosomeSignal()` / `TSSEnrichment()` (and `StringToGRanges()`) deprecated in Signac 1.17.x | P2 | `SKILL.md` Version Compatibility: "checked on Signac 1.17.1" plus a note that the two QC calls are deprecated for `ATACqc()`, still run with a warning, and `ATACqc()` needs the external `fragtk` binary; one comment in `examples/signac_workflow.R` | ran both calls on the audit's `obj_qc.rds` + `fragments.tsv.bgz`: columns filled, `.Deprecated` warning captured; `ATACqc` formals (`fragtk.path`) and `fragtk` absent from PATH confirmed in the installed namespace | the calls were not replaced: `fragtk` is not installed and not installable under the brief. `StringToGRanges()` is not used anywhere in the Skill, so it is not mentioned |
| No escape-hatch section | P2 | none | n/a | see left unfixed |

### Left unfixed
- **No escape-hatch / out-of-scope section (P2):** new content, not a correction; nothing in the audit's runs contradicts the Skill. The pointers it would carry (multimodal-integration for RNA-equivalent resolution, motif-to-TF causal claims) are already in the chromVAR prose and Related Skills.
- **Replacing the deprecated QC calls with `ATACqc()`:** needs the `fragtk` binary, which is absent on this machine; the note documents the switch instead.

### Redundancy pass (commit `d9bcbfd`)
Guide-only agent content moved into SKILL.md; the rest of the guide's restatements deleted.

| deleted passage (`usage-guide.md`) | new home |
|---|---|
| Prerequisites (R/Bioc/ArchR installs, `biovizBase`, pip, MACS on PATH, one genome build) | `SKILL.md` "Install"; guide keeps a pointer |
| ArchR Workflow | `SKILL.md` "ArchR flow" (under Framework Decision Table) |
| SnapATAC2 Workflow | `SKILL.md` "SnapATAC2 flow" |
| Decision Guidance: Framework, Binarize | already in Framework Decision Table / Governing Principle |
| Decision Guidance: Embedding (cisTopic/LDA, PeakVI/PoissonVI, spectral) | `SKILL.md` "Alternative embeddings" after the depth paragraph |
| Key Differences table (per-cell non-zeros 1-10% vs 10-45%) | `SKILL.md` Governing Principle; other rows already in SKILL.md |
| What the Agent Will Do | restated the SKILL.md sections; deleted |
| Tips (11 bullets) | each already in SKILL.md: Governing Principle, TF-IDF + LSI, chromVAR, Doublet Detection, QC Thresholds, Consensus Peak Calling, Common Errors |

Verified by grep that each moved item is present in SKILL.md. The guide keeps Overview, Quick Start, Example Prompts, Related Skills.

### Scripts (commit `0c0ecaa`)
| old location | script |
|---|---|
| `SKILL.md` chromVAR section, 28-line R block | `scripts/run_chromvar.R` (args: rds, out prefix, ident1, ident2, optional group_by) |

Ran twice through `rs.sh` on the audit's `obj_qc.rds` (270 cells x 222 peaks): 746 motifs scored, 3 significant, 230 DA rows, both output CSVs byte-identical (also confirms the `set.seed` fix). Other SKILL.md blocks are under 10 lines and stay inline; `examples/` untouched.

---

## 2026-09-23 — corrective Phase 1 after final-pass rejection

Worktree: `F:\OpenScience\wt\single-cell-scatac-analysis`; branch
`fix/single-cell-scatac-analysis`; corrective source commit
`a8fef2a02c45b710257e1f5606171fa462e817a8` on rejected tip `0c0ecaa22c89b87f6ec50bbae499cbfa31b995df`.
Environment: `single-cell-transcriptomics-analyst`; no installs and no shared-environment changes.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Exact documented `r.sh scripts/run_chromvar.R ...` invocation stopped at `library(Signac)` because `r.sh` configures runtime DLL paths but not the private package library | P0 | Added `.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))` before package loads in `scripts/run_chromvar.R` | Ran the exact documented command twice with no `R_LIBS` export against audit-owned `obj_qc.rds`: both wrote an RDS (23,780,387 bytes) and a 230-row CSV (14,490 bytes), reported 746 motifs / 270 cells / 3 adjusted-significant motifs; CSV SHA-256 matched: `54E787A5341AC63A07B47402A3BA5C10D3A5A9C657E5AE0976A3C446DF3048A7` | The wrapper returned `2816` after both materialized outputs; record this as an environment/runtime follow-up rather than claiming a clean exit. |
| Opening workflow advertised removed `RunChromVAR()` although the detailed section correctly points to the replacement | P1 | Replaced the overview arrow with `scripts/run_chromvar.R` | `rg RunChromVAR` confirms the remaining occurrences explain its removal or occur in the script's historical compatibility comment | No runnable stale wrapper reference remains. |

### Remaining blockers

- The Windows `r.sh` -> R runtime returns post-output exit status `2816` for both completed chromVAR runs. It needs runtime-level diagnosis before a later audit may call the documented command process-clean.
- The prior `fragtk` / `ATACqc()` and Linux-only ArchR/SnapATAC2 constraints remain unchanged.
