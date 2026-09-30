> **Audit record for `bio-atac-seq-motif-deviation`**
> - Audited working candidate `d645db4df84650ecf90027b9013e38b0d9adce73fb985a605d769c730d68fefc`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/motif-deviation), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-motif-deviation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/motif-deviation) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent. Initial diagnostic audit only; not a certification.
> - Data: ENCODE GM12878 x3 and K562 x3 ATAC chr1:1-30 Mb (ENCSR095QNB, ENCSR637XSC, ENCSR868FGK); 10x PBMC 5k scATAC chr1:1-30 Mb (CC BY 4.0); JASPAR2024. Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-motif-deviation

Candidate: `sha256-manifest-v1 d645db4df84650ecf90027b9013e38b0d9adce73fb985a605d769c730d68fefc` (6 files), branch `fix/atac-motif-deviation` @ 3186916.
Category: 3 - Data Analysis - Mode D - Moderate, N = 5.
Environment: WSL `science`, micromamba `bio-atac-seq-motif-deviation` (R 4.4.3, Bioc 3.20, chromVAR 1.30.1, motifmatchr 1.30.0, ArchR 1.0.3, Signac 1.17.1 plus a Signac 1.16.0 side library), `-py` (decoupler 1.8.0), `-dc2` (decoupler 2.2.0). Fingerprint `91dcd670...e118ecd`.
Code: `scripts/` (run scripts, patched bulk script, diagnostics). Logs: `logs/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (shipped bulk script) | yes | 10 | 10 | 20 | 2/4 | error |
| 2 | Variant A (patched bulk, hand-check, reseed) | yes | 32 | 42 | 74 | 3/5 | warn |
| 3 | Variant B (Signac) | yes | 22 | 30 | 52 | 3/5 | partial |
| 4 | Variant B (ArchR) | yes | 24 | 32 | 56 | 2/5 | partial |
| 5 | Variant B (DecoupleR) | yes | 28 | 34 | 62 | 3/5 | warn |

**Execution Average: 52.8 / 100** - **Assertion Pass Rate: 13/24 (54.2 %)**
**Static: 71/100** - **Final: 60 (Reject by veto)**. Skill veto FAIL (stability, determinism); research veto FAIL (code usability). Deployable: no. A diagnostic score is not a readiness state.

Surface classifications: bulk script as shipped (failed), bulk script patched (executed), chromVAR hand-check (executed), JASPAR2024/TFBSTools #39 workaround (executed), Signac current 1.17.1 (failed), Signac 1.16.0 (executed), ArchR chain to addDeviationsMatrix (executed) and getMarkerFeatures (failed), DecoupleR 1.8.0 (executed), decoupler 2.x rename (executed). Bulk time-course spline, custom PFM/plant genome, scBasset/SCENIC+ routes: static-only (not exercised). Bioc 3.23 / R 4.6 stack: not built.

## Input 1 - Canonical: shipped script on ENCODE GM12878 vs K562

`chromvar_bulk_analysis.R` unmodified, real peaks (6,357) and counts: exit 1 at `filterSamples`, "colData for object must have column named depth with total reads per sample". chromVAR's `filterSamples` uses `depth` as total reads per sample and computes the in-peaks fraction as fragments-in-peaks over depth; the Skill never says to provide it, and `colSums(counts)` would make the fraction 1.

Findings: MOTDEV-001, MOTDEV-008. **Scores:** 10 + 10 = **20**. Assertions 2/4.

## Input 2 - Variant A: patched script, hand-check, reseed

With one added line (true library depth from `depth.tsv`): 5,340 peaks x 6 samples, 879 motifs, 0 NA; top variable IRF9, STAT1::STAT2, SPIB, IRF3, REL; GM12878-up SPI1, EBF1, IRF/REL; K562-up GATA2, GATA1::TAL1; consistent with B-lymphoid vs erythroid biology. `computeDeviations` equals a hand computation to 1.1e-16 (deviation = raw minus mean background raw; z divides by background SD). Both PDFs rendered and read: variability plot legible; heatmap legible but rows are JASPAR IDs.

Two runs of the same pipeline with different seeds: max |dz| 1.25, median 0.16, top-20 overlap 18/20, significant sets 728 vs 747 (Jaccard 0.88). The script has no `set.seed`.

Findings: MOTDEV-003, -005, -007, -009, -011. **Scores:** 32 + 42 = **74**. Assertions 3/5.

## Input 3 - Variant B: Signac

Signac 1.17.1: `AddMotifs` works (879 PFMs); `RunChromVAR` does not exist (NEWS: removed). Signac 1.16.0: 879 x 1,853 chromvar assay, 0 NA, range -4.2..4.5; `FindAllMarkers(mean.fxn=rowMeans, fc.name='avg_diff')` returns `avg_diff`; cluster hits include TCF7, GATA3 (T), SPIB (B), Spi1 (monocyte).

Findings: MOTDEV-002. **Scores:** 22 + 30 = **52**. Assertions 3/5.

## Input 4 - Variant B: ArchR

Chain runs to `addDeviationsMatrix` (216 cells, 1,185 peaks, MotifMatrix 870 x 216). Verbatim `getMarkerFeatures(useMatrix='MotifMatrix', useSeqnames='z')` fails: 23 NA z in 16 motifs x 6 cells; presto 1.1.0 refuses NA. Diagnosis: the 6 cells carry 26-203 reads in the peak matrix (median 917) and each NA motif has 3-12 matched peaks with zero reads there, so observed and background deviations coincide and the background SD is 0. After removing the 6 cells the call completes (C3: 34 markers, others 0 at this size). Recurrence at full scale unproven.

Findings: MOTDEV-004, -009. **Scores:** 24 + 32 = **56**. Assertions 2/5.

## Input 5 - Variant B: DecoupleR

decoupler 1.8.0 with CollecTRI (43,159 edges) on 6 x 879 z: ulm/mlm/consensus run, 307 overlapping TFs, signs consistent with the contrast. `run_ulm` returns a tuple, `omnipath` is required, `collectri_net` undefined. Conceptually loose: motif (TF) deviations are treated as gene-level features against gene targets. 2.2.0 renames confirmed.

Findings: MOTDEV-006. **Scores:** 28 + 34 = **62**. Assertions 3/5.

## Static notes

Frontmatter and routing are sound; SKILL.md is compact. Problems are correspondence between documented and shipped/runnable surfaces (bulk script, Signac), method prose (MOTDEV-005), stale counts and uncited heuristics (MOTDEV-009, -010), and an untested newest-Bioconductor stack (MOTDEV-012). Static 71: functional 8, reliability 5, performance 7, agent usability 12, human usability 6, security 10, maintainability 8, agent-specific 15.

## Findings ledger (ordered)

| ID | Severity | Title |
|---|---|---|
| MOTDEV-001 | P0 | Bundled bulk script fails as shipped: no colData depth |
| MOTDEV-003 | P0 | No set.seed; z-scores and hit lists change run to run |
| MOTDEV-002 | P1 | RunChromVAR removed in Signac 1.17.x; floor says 1.13+ |
| MOTDEV-004 | P1 | ArchR getMarkerFeatures fails on NA z; no guard |
| MOTDEV-005 | P2 | "What chromVAR computes" definitions wrong |
| MOTDEV-006 | P2 | DecoupleR snippet not runnable; motif z misused |
| MOTDEV-007 | P2 | Bulk outputs and heatmap use JASPAR IDs only |
| MOTDEV-008 | P3 | Depth wording: reads in peaks vs total depth |
| MOTDEV-009 | P3 | Stale numeric claims (879 vs 1,900; 870 vs 5,000; logFC range) |
| MOTDEV-010 | P3 | Uncited guardrail thresholds; untested workflows |
| MOTDEV-011 | P3 | plotVariability aes_string deprecation (ggplot2 4.x) |
| MOTDEV-012 | P3 | Bioc 3.23 not exercised |

Full text: `findings.json`. Restricted-access items: none.
