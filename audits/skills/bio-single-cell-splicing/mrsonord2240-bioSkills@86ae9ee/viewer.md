> **Audit record for `bio-single-cell-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@86ae9ee](https://github.com/mrsonord2240/bioSkills/tree/86ae9ee222b5c1ce1e0a9c835c655e2f33b48ccd/alternative-splicing/single-cell-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-splicing (re-audit of the fixed Skill)
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@86ae9ee222b5c1ce1e0a9c835c655e2f33b48ccd:alternative-splicing/single-cell-splicing` (read from a copy in `run/skill/`; the worktree and clone were not written to).
Pre-fix (archived): 69, Reject, Research Veto M4 fired. **Now: 84, Limited Release, deployable, no veto, no open P0, one open P1.**
Category: Data Analysis. Mode D. Complexity: Complex, N = 7. Executed 7/7 (input 6 partial). Every script that was run is in `run/`; logs are in `run/out/`; synthetic data are in `run/data/` and are labelled synthetic in their generator docstrings.

## How the M4 (code usability) question was re-judged
Every fenced block of SKILL.md was extracted to `run/blocks/` by `00_extract_blocks.py` (14 blocks) and parse-checked (`out/01_syntax.log`, `01_syntax_check.sh`: all Python, R and bash parse). Then each block was run from its file:

| block | what | how run | result |
| --- | --- | --- | --- |
| S01/S02 | install lines | `git ls-remote` on every repo; `pip --dry-run --no-deps` in as-sc (`70_install_claims.sh`) | repos exist; brie, psix, scquint resolve; Psix without `--no-build-isolation` fails; SpliZ has no setup.py (as the Skill says). Not real installs |
| S03 | rMATS -> MARVEL event tables | literal, real chrX rMATS output | ran; row counts equal rMATS; `gene_type` NA without GTF gene rows (as stated), 0 NA with them |
| S04 | MARVEL plate workflow | literal, real demo + planted v2 + null | ran; PSI equals hand computation exactly |
| S05, S06 | BRIE2 CLI + readout | literal, real Smart-seq2 + planted v2 + null | ran |
| S07 | scQuint | literal, real STARsolo SmartSeq output + planted | see input 6: works only with chr junctions and non-chr GTF |
| S08 | SpliZ | not run (no Nextflow); config keys checked in the repo | hedged as not run |
| S09 | Psix | literal, planted trajectory | ran, 903 s |
| S10, S11 | regtools + Sierra | literal, package bundled real 10x BAM | ran |
| S12-S14 | pseudobulk + leafcutter | literal (exec), planted replicate design | ran |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: BRIE2 real Smart-seq2 + all example helpers | 37 | 54 | 91 | 5/5 PASS | ✅ |
| 2 | Variant A: BRIE2 planted v2 + null (+ pre-fix sets) | 38 | 55 | 93 | 5/5 PASS | ✅ |
| 3 | Edge: sparse real data, random labels, droplet mode | 35 | 51 | 86 | 4/5 PASS | ✅ |
| 4 | Variant B: MARVEL S03/S04 real demo, planted, other events | 36 | 52 | 88 | 4/5 PASS | ✅ |
| 5 | Stress: replicate pseudobulk + leafcutter, mismatched index | 37 | 55 | 92 | 5/5 PASS | ✅ |
| 6 | Scope: Psix, Sierra, scQuint, SpliZ | 31 | 44 | 75 | 3/5 PASS | ❌ (PARTIAL) |
| 7 | Adversarial: per-cell PSI from 10x 3' v3 | 36 | 52 | 88 | 4/5 PASS | ✅ |

**Execution Average: 87.6 / 100. Assertion Pass Rate: 30/35.** Static 78 x 0.4 = 31.2; dynamic 87.6 x 0.6 = 52.6; **final 84**. Layer 1 average 35.7/40, Layer 2 average 51.9/60 (Limited Release floors met; Production Ready needs 85).

## Detailed Outputs

### Input 1 — Canonical (BRIE2 on real Smart-seq2)
**Prompt:** "Estimate per-cell PSI for cassette exons in my Smart-seq2 mouse E6.5 cells with BRIE2 and tell me which events change with my covariates."
Ran S05 literally (`10_in1_real_brie.sh`), then S06 and checks (`11_in1_pysam_check.py`, `12_in1_readout.py`), then every helper in `examples/` from the clean copy (`13_in1_example_helpers.py`).
```
Filtered out 31 genes with less than 50 total counts or 30 cells with unique counts or 10 unique counts or 0.0010 minor isoform frequency
AnnData 130 x 19; varm: ELBO_gain, cell_coeff, fdr, pval ...; layers: Psi, Psi_95CI, Z_std ...
ASSERT OK: varm keys/layers as SKILL.md states; n events kept 19 of 50
fdr vs independent BH of pval, max abs diff: 0.0        # random covariate: 0 of 19 at fdr<0.05
Spearman brie isoform2 vs pysam skip-junction count: 0.975 ; isoform1 vs inclusion: 0.917
fetch: gene rows 5227 | 10x mean unique reads/cell/event 0.0348 | run_brie2_inference -> (130, 19)
find_variable_splicing helper == hand mean (t1 0.911728 vs 0.911728024) | pb (50,8) sum 5737 == 5737 | 3 failure modes raise
```
**Scores:** 37 / 54 / 91. Assertions 5/5 PASS (see JSON).

### Input 2 — Variant A (planted differential splicing + null)
**Prompt:** "Test which of my 60 cassette exons differ between cell populations A and B (one third of cells are low-coverage)."
Auditor generator `20_gen_planted_v2.py` (synthetic; 60 events, half minus-strand, 12 x dPSI 0.5, 8 x dPSI 0.2, 40 null; 100 cells, 28 low-coverage). S05 run literally (`21_in2_brie_planted.sh`, `22_in2_eval.py`).
```
big   12  fdr05 12   | small 8  fdr05 8 | null 40 fdr05 0 (raw p<0.05: 1)
sign(cell_coeff)==sign(psiB-psiA) among planted fdr<0.05: 1.0 (n 20) ; FDP 0.0
mean|Psi-true|: normal 0.083, low-coverage 0.079 ; naive pooled count-PSI vs truth dPSI Pearson 0.988
NULL set (60 events): fdr<0.05 0, raw p<0.05 2, ELBO_gain>3 1
determinism: significant sets 20 20 identical: True ; max |Psi diff| 0.0334
```
Regression on the pre-fix generator (`regress/run_regress.sh`): big 20/20, mid 10/10, null 2/70 (FDP 0.062); pure null 0/100 at fdr (4 with ELBO_gain > 3, which is why the Skill now says use fdr).
**Scores:** 38 / 55 / 93. Assertions 5/5 PASS.

### Input 3 — Edge (sparse real data, droplet mode)
**Prompt:** "My plate data are very sparse and I also have a 10x BAM: do random labels give false hits, and does droplet mode work?"
Real cells with random 0/1 labels: 0/19 fdr calls. Pre-fix planted 10x set through the helper `count_splicing_reads` (`regress/14_brie_10x.py`): near-3' events 15/15 planted detected, 0/35 null; far-3' events (exon > 1.5 kb from poly-A) 0 discriminating reads over 300 cells. The BRIE2 `--batchSize` default 500000 quoted in the OOM row equals `brie-quant -h`. The TensorFlow-memory, Sierra-annotation-gap and scQuint-sparsity failure-mode rows were not reproduced (assertion 5 FAIL).
**Scores:** 35 / 51 / 86. Assertions 4/5.

### Input 4 — Variant B (MARVEL)
**Prompt:** "Run MARVEL on my plate-based BAMs: build event tables from rMATS, compute PSI, classify modality, test neuron vs glia."
- S03 on real chrX rMATS (2 v 2, rMATS-turbo 4.4.0; `32_marvel_S03_rmats.sh`, `33_marvel_S03.R`): SE 978, MXE 52, RI 162, A5SS 165, A3SS 205 events, each table row-for-row; GTF without gene rows gives `gene_type` NA for all rows (Skill says so); `34_make_gencode_style_gtf.py` adds gene rows -> 0 NA. A hand-built plus-strand `tran_id` is in the table.
- S04 unedited on the real package demo (30 Smart-seq2 cells, `30_marvel_demo_stage.R`, `31_marvel_demo_S04.R`): 10 events tested; `events checked by hand: 10, pairs compared: 249, max |MARVEL - hand| 0`; `mean.g1 x100` matches; `mean.diff == mean.g2 - mean.g1: TRUE`.
- S04 unedited on planted v2 (`35_marvel_planted_gen.R`, `36_marvel_planted_S04.R`; 120 events, 20 minus-strand, 40 cells): big 30/30, mid 17/20, null 0/69; sign 1.0; hand PSI max diff 0 over 2,313 pairs. Null set (`in4_null`): 0/108 (9 raw). Regression set (`regress/28_marvel_planted.R`): 40/40, 20/20, 0/140; permuted labels 0 at adj p.
- Unrun by the fixer, now run (`38_marvel_other_events.R`): `ComputePSI` for MXE, A5SS, A3SS equal the package-shipped PSI (max diff 0); `dts` -> `there is no package called 'twosamples'`. **RI:** `ComputePSI(EventType='RI')` -> `argument is of length zero`; with `thread = 2` it runs (`39b_marvel_RI_src.R`). The Skill only says RI needs `IntronCounts` (P2).
**Scores:** 36 / 52 / 88. Assertions 4/5.

### Input 5 — Stress (pseudobulk + leafcutter)
**Prompt:** "Aggregate my cells by donor and cell type and find differential splicing between the two cell types with leafcutter; my metadata table came from read.csv."
Synthetic replicate design (`40_pb_gen.py`; 84 cells, 7 donors x 2 types, donor random effect). S12/S13 by `exec` of the block files, S14 literally (`42_pb_leafcutter.sh`).
```
pb shape (450, 14)  groups: {'T1': 7, 'T2': 7}; total 113015 conserved; T2__d3 == numpy mask sum
shuffled metadata order -> identical pseudobulk ; reversed matrix column order -> identical
raises ValueError: default RangeIndex metadata: 84 cells not in cell_metadata.index (set index=cell id) ...
raises ValueError: NaN sample / only 1 donor per type (need >= 3 ...) / ids differ by case / 10 cells missing
duplicated cell ids in metadata -> ValueError: Grouper and axis must be same length   (loud, cryptic)
leafcutter -i 5 -g 3 -c 20: clusters 150/150 tested; big 20/20 fdr05 ; mid 12/20 (17 raw) ; null 0/110 (5 raw); direction 1.0
Pooled n=1 vs n=1 Fisher (what the Skill warns against): null 9/110 at FDR<0.05 (17 raw)
```
**Scores:** 37 / 55 / 92. Assertions 5/5.

### Input 6 — Scope boundary (Psix, Sierra, scQuint, SpliZ)
**Prompt:** "Find regulated exons along pseudotime with Psix, call alternative polyadenylation with Sierra, and test differential intron usage with scQuint on my STARsolo Smart-seq output; run SpliZ if you can."
- **Psix** S09 unedited (`50_psix_gen_and_S09.py`, synthetic 240 cells x 100 exons, 25 dynamic): 903 s; `qvals < 0.05` = 31: dynamic 25/25 (sigmoid 15/15, bump 10/10), static 6/75; median psix_score 1.21 vs -0.01.
- **Sierra** S10 + S11 unedited on the bundled real BAM (`51_sierra_stage_S10.sh`, `52_sierra_S11.R`): regtools `-s RF` 333 junctions; FindPeaks 34 peaks; CountPeaks 22,439 UMIs; top-5 peaks Sierra vs Rsamtools distinct (CB,UB): 6253/6284, 2776/2777, 1600/1609, 1250/1261, 899/899; random split -> 0 rows; 8 genes thinned in one group -> 7/8 recovered.
- **scQuint** on REAL STARsolo SmartSeq output (`60_starsolo_real.sh`: 4 real chrX libraries as cells; STAR 2.7.11b): features.tsv is `X 193062 200833 1 1 1 1 0 24`. S07 with the GTF that built the index -> `Filtering to introns associated to 1 and only 1 gene.` then `adata (4, 0)` and `ValueError: Cannot set a DataFrame with multiple columns to the single column intron_group`. Naming variants (`62_scquint_contig_variants.py`): junctions X + GTF X fail; X + chrX fail; **chrX junctions + X GTF** annotates 662 introns and proceeds. Planted data in that layout (`64_scquint_planted.py`, 120 events, 20 minus-strand, 40 cells): 30/30 big, 20/20 mid, 1/70 null at `p_value_adj < 0.05`; direction 1.0 on 50 hits; null set 0/120 groups. Default 30/30 thresholds on those 40 cells: `ValueError: not enough values to unpack (expected 2, got 0)`, not empty tables as the Skill says.
- **SpliZ** not run (no Nextflow); `nextflow.config` in the repo has `dataname, input_file, SICILIAN, grouping_level_1/2, libraryType`, and there is no setup.py (pip line correctly removed). `junctions2psi` not run (hedged in text).
**Scores:** 31 / 44 / 75. Assertions 3/5 (scQuint real-format and empty-table statements FAIL). Status PARTIAL.

### Input 7 — Adversarial (10x 3' v3)
**Prompt:** "Give me per-cell cassette-exon PSI and cell-type-specific exons from my 10x 3-prime v3 data."
The Skill says no (chemistry table, "10X 3' Problem", decision tree) and points to Sierra (ran, input 6), pseudobulk (ran, input 5), plate or long-read chemistries. Measured on the real 10x subset (`regress/15_real_10x.py`): 1301 cells x 50 events, mean 0.0348 unique discriminating reads per cell per event, 0.11% of cell-events reach 5 reads, read length 91. `>70% of unique reads in the 3' UTR` and `median fragment <1 kb` were not measured or cited to a figure.
**Scores:** 36 / 52 / 88. Assertions 4/5.

## Pre-fix defects re-checked
| pre-fix finding | now |
| --- | --- |
| MARVEL `AssignModality(EventType=)`, `CompareValues(n.cells=)`, `Exp` row names | fixed: S04 runs unedited |
| Psix constructor / `pvalue` query / wrong mechanism text | fixed: S09 runs, columns `psix_score, pvals, qvals` |
| Sierra `bam.file`, missing `junctions.file`, Count/Annotate return values | fixed: S10/S11 run |
| example `prepare_splicing_events` (briekit), `pseudobulk_by_celltype`, mislabeled per-cell test | fixed: all helpers run (input 1) |
| pseudobulk without replicates / silent zeros on RangeIndex | fixed: raises; >= 3 replicates enforced |
| BRIE2 keys, silent filter, invented errors | fixed and verified (input 1, 2) |
| usage-guide.md redundancy | now 1.8 KB pointer + prompts; nothing a task needs was lost (install block, tips, prompts all present in SKILL.md) |
| **new (introduced by the fix)**: scQuint block | real-format failure (input 6), P1 |

## Recommendations
- **P1** scQuint block fails on real self-consistent STARsolo output; empty-table statement wrong (input 6).
- **P2** MARVEL RI needs `thread >= 2`; `CoverageThreshold` semantics (input 4).
- **P2** SKILL.md 561 lines, no `references/` split.
- **P2** Two 10X numbers unsupported; install lines not marked unrun; Psix runtime and static-exon rate at defaults (inputs 6, 7).
