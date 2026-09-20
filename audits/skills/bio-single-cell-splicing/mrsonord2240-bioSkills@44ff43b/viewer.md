> **Audit record for `bio-single-cell-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/single-cell-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-splicing

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/single-cell-splicing` (first audit)
Category: Data Analysis | Mode: D (hybrid: instructions + CLI/R/Python snippets + one example script) | Complexity: Complex, N = 7 (11 tools named, 3 task families, 3 files)

**Final: 69 -> grade forced to Reject by Research Veto M4 (code usability). Deployable: false. Static 68, execution average 70.3, assertions 22/35.**
All 7 inputs executed (inputs 4 and 6 in part). Every script is in `run\`; raw outputs in `run\out\*.log`. Synthetic data is labelled in `run\data\README_SYNTHETIC.md`. Nothing was written under `external\` (no `__pycache__` found in the clone afterwards).

## Step 1 — Skill Veto

| T | Result | Evidence |
| --- | --- | --- |
| T1 Stability | PASS | Nothing loops or crashes at random; examples fail deterministically on wrong arguments (recorded under M4 like the sibling audits) |
| T2 Contract | PASS | frontmatter name/description present |
| T3 Determinism | PASS | identical `brie-quant` rerun: same events, max abs Psi diff 0.033 (mean 0.003), ELBO_gain corr 0.9999, identical fdr<0.05 set (33 = 33); no `--seed` flag exists (`run\44_determinism.sh`) |
| T4 Security | PASS | subprocess uses list arguments; no eval, no credentials |

## Step 2 — Static score 68/100

| Category | Score | Note |
| --- | --- | --- |
| Functional suitability | 8/12 | right framing, verified numbers; three named tool blocks call non-existent arguments; `brie.tl.fit` invented |
| Reliability | 5/12 | wrong failure rows; silent gene filtering; silent zeros in `pseudobulk_junctions` |
| Performance/context | 6/8 | 447 lines, no `references/` |
| Agent usability | 11/16 | clear decision tables; output keys vague |
| Human usability | 6/8 | natural triggers |
| Security | 11/12 | |
| Maintainability | 6/12 | monolith, 2 of 5 helpers crash, no tests |
| Agent-specific | 15/20 | excellent escape hatches; no layering; phantom version numbers |

Shipped-means-present: SKILL.md, usage-guide.md and `examples/sc_splicing_brie2.py` all exist; no missing primary file. No `references/` directory is promised.

## Inputs and results

| # | Type | Label | Basic /40 | Spec /60 | Total | Assertions | Executed | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Canonical | BRIE2 on real Smart-seq2 (130 cells) | 32 | 46 | 78 | 3/5 | yes | ✅ |
| 2 | Variant A | BRIE2 differential splicing, planted + dropout + null | 33 | 48 | 81 | 4/5 | yes | ✅ |
| 3 | Edge | sparse real plate data, random-label null | 29 | 42 | 71 | 3/5 | yes | ⚠️ |
| 4 | Variant B | MARVEL: SKILL block on real demo, corrected chain on planted truth | 24 | 33 | 57 | 3/5 | yes (dts not run) | ❌ |
| 5 | Stress | pseudobulk -> leafcutter, planted + overdispersion | 27 | 38 | 65 | 2/5 | yes | ⚠️ |
| 6 | Scope Boundary | Psix trajectory, Sierra APA, SpliZ | 24 | 31 | 55 | 3/5 | Psix and Sierra call yes; SpliZ no (no nextflow) | ❌ |
| 7 | Adversarial | per-cell PSI from 10x 3-prime v3 | 35 | 50 | 85 | 4/5 | yes | ✅ |

Execution average 70.3 (Layer 1 mean 29.1/40, Layer 2 mean 41.1/60). Static 68 x 0.4 = 27.2; 70.3 x 0.6 = 42.2; final 69.

### Input 1 — Canonical: BRIE2 on real Smart-seq2
**Prompt:** "I have plate-based Smart-seq2 BAMs from 130 mouse cells and a GFF3 of 50 skipped-exon events. Estimate per-cell PSI with BRIE2 and test association with a cell covariate."
**Code that ran:** `run\01_brie_real_count.sh`, `03_brie_real_quant.sh` (SKILL flags verbatim: `-a -S -o -p 16`; `-i -c -o --interceptMode gene --LRTindex All --testBase null --MCsize 3 --batchSize 1000000 -p 16`), `02_brie_real_check.py`, `04_inspect_quant.py`, `05_example_funcs_real.py`.
**Output kept:**
- counts `(130, 50)`, layers ambiguous/isoform1/isoform2/poorQual; quant `(130, 19)` (31 events removed by default gene filters), layers `Psi, Psi_95CI, Z_std`, `varm: ELBO_gain, cell_coeff, fdr, pval, sigma, intercept`.
- pysam cross-check: Spearman 0.975 (skip junction) and 0.917 (inclusion); BRIE isoform2 total 5,737 vs pysam 7,381 (ratio 0.78, BRIE requires `--minMatch 10/--maxMiss 2`). `ASSERT OK`.
- Example helpers on real output: `find_variable_splicing` and `differential_splicing_pseudobulk` run; `pseudobulk_by_celltype` -> `AttributeError: 'Series' object has no attribute 'nonzero'`; `prepare_splicing_events` -> `FileNotFoundError: briekit-event` (see input 1 addendum in `run\out\41_briekit.log`: when built with numpy present the console script dies with `ModuleNotFoundError: parseTables`).
**Assertions:** PASS CLI runs; PASS counts match pysam; PASS output keys exist (Skill never names `pval/fdr`); FAIL every example helper runs; FAIL Skill says how to make the GFF3 events.

### Input 2 — Variant A: planted two-group differential splicing
**Prompt:** "Cells from two types, 40 each, some with almost no reads. Which cassette exons differ in inclusion between the types, and in which direction?"
**Data (SYNTHETIC):** `run\10_gen_planted_sc.py`: 80 cells, 100 SE events (20 x dPSI 0.7, 10 x 0.3, 70 null), 75-nt SE reads, 15% dropout cells; per-cell PSI beta noise (concentration 20).
**Code:** `11_brie_planted.sh`, `12_eval_planted.py`, `13_null_ss2.sh`.
**Output kept:**
```
big  20 events: 20 fdr<0.05, median ELBO_gain 58.8    mid 10: 10 fdr<0.05, median 23.3    null 70: 3 fdr<0.05
sign(cell_coeff) == planted sign: big 1.0, mid 1.0
observed FDP among fdr<0.05 calls: 0.091
mean |Psi - true group PSI|: normal cells 0.077 (20.0 unique reads/event), dropout cells 0.091 (1.4 reads/event)
PURE NULL (100 events, random groups): raw p<0.05 11, fdr<0.05 0, ELBO_gain>3 6, max ELBO 3.94
example differential_splicing_pseudobulk: 20/20, 10/10, null 2/70 fdr<0.05, sign agreement 1.0
```
**Assertions:** PASS recovery; PASS direction; PASS null control; PASS dropout shrinkage; FAIL ELBO_gain>~3 stated as a test (6% of pure-null events pass; fdr column unmentioned).

### Input 3 — Edge: sparse real plate data
Real 130-cell run from input 1 with a **random** binary label and a log-depth covariate (`03a_make_cellfeat.py`, `43_real_null.py`): rand_group 0/19 FDR<0.05 (raw 3/19, max ELBO 2.16); log_depth 0/19. Median unique reads per cell per event 0; 18% of pairs >= 5 reads; mean 95% CI width of per-cell Psi 0.30. **Assertions:** PASS null; PASS thresholds match sparsity; FAIL filtering not warned (31/50 dropped); PASS two helpers run; FAIL `pseudobulk_by_celltype` crashes.

### Input 4 — Variant B: MARVEL plate workflow
**Prompt:** "Run MARVEL on Smart-seq2 STAR junctions: PSI for skipped exons, modality per cell type, differential splicing iPSC vs endoderm."
**Data:** MARVEL package's own real demo (30 Smart-seq2 cells) rewritten to per-cell STAR `SJ.out.tab` by `23_marvel_prep.R`; Skill block run verbatim by `25_marvel_skill_literal.R`.
```
[OK]   CreateMarvelObject (Skill args)          SJ matrix 134 x 31 via rbindlist/dcast(fill=0)
[OK]   ComputePSI(CoverageThreshold=10, EventType=SE)   PSI SE 10 x 31
[FAIL] AssignModality(marvel, EventType='SE')   -> unused argument (EventType = "SE")
[FAIL] CompareValues(... n.cells=25 ...)         -> argument "level" is missing, with no default
       Exp after read.table(row.names=1): first column ERR1562084 (MARVEL needs gene_id)
[FAIL] CheckAlignment(level="gene")              -> undefined columns selected
[OK]   AssignModality(sample.ids=..., min.cells=5)   [installed signature]
[OK]   CompareValues(level="splicing", event.type="SE", method="wilcox", min.cells=5)
```
PSI vs hand computation (`27_marvel_psi_check.R`): max |diff| 0 over 109 cell-event pairs (0-1 scale). Planted truth (`28_marvel_planted.R`, 200 events x 60 cells, 22% low-coverage cells, 3 minus-strand events because `ComputePSI.SE` crashes with none): wilcox 40/40 big, 20/20 mid, 0/140 null at adj p<0.05 (raw 6/140), sign agreement 1.0; three label permutations 0 adj p<0.05. `method='dts'` needs `twosamples`, not installed with MARVEL (not run).
**Assertions:** FAIL block runs; PASS PSI equals hand; PASS recovery; PASS null; FAIL pre-flight/gene_id/event tables.

### Input 5 — Stress: pseudobulk then leafcutter
**Prompt:** "Aggregate junction counts per cell type and use leafcutter to compare the two types."
`34_pseudobulk.py`, `35_pb_leafcutter.py/.sh`, `36_pb_eval.py`. Skill function conserves counts (269,534 + 301,486 = 571,020) but with a default-RangeIndex metadata table returns **A = 0, B = 0 with no message**. Pooled Fisher on the pseudobulk: 40/40, 20/20 planted but **34/140 null events FDR<0.05** (32% raw p<0.05). leafcutter on the function's n=1 v 1 output needs `-g 1 -i 1` (defaults `-g 3 -i 5`) and then reports p-values without replicates: 40/40, 20/20, null 2/140. leafcutter on 5 v 5 replicate pseudobulks: 40/40, 20/20, null 7/140 FDR<0.05 (FDP 0.10).
**Assertions:** PASS conserves counts; FAIL silent zeros; PASS replicate leafcutter recovers; FAIL no replicate warning; FAIL leafcutter defaults not stated.

### Input 6 — Scope Boundary: Psix, Sierra, SpliZ
`30*_psix_api.py`, `31_psix_planted.py`, `32_sierra_sig.R`, `33_sierra_literal.R`, `40_pip_claims.sh`.
```
Skill Psix(adata, psi_matrix_path=...)  -> TypeError: unexpected keyword argument 'psi_matrix_path'
Skill .query("psix_score > 1.5 and pvalue < 0.05") -> UndefinedVariableError: 'pvalue' (columns: psix_score, pvals, qvals)
real API (psi_table, mrna_table, latent file), 300 cells / 150 exons: q<0.05 -> 30/30 dynamic, 1/120 static; psix_score median 1.85 vs -0.04
Skill FindPeaks(bam.file=...) -> unused argument (argument is bamfile; junctions.file has no default)
SpliZ: config keys in nextflow.config match; pip install line has no setup.py; nextflow not installed -> not run
```
**Assertions:** FAIL Psix snippet; PASS Psix (real API) recovers; FAIL Sierra snippet; PASS SpliZ config; PASS APA kept out of splicing claims.

### Input 7 — Adversarial: per-cell cassette exon PSI from 10x 3-prime
**Prompt:** "Give me per-cell cassette-exon PSI and the cell-type-specific exons from my 10x 3-prime v3 data."
**What an agent following the Skill says (verified):** no; 10x 3-prime cannot resolve internal exons per cell; pseudobulk between annotated cell types or Sierra for APA; long-read or Smart-seq3 for per-cell isoforms.
`15_real_10x.py` (real 10x neuron subset, 1,301 cells): mean 0.035 unique reads/cell/event, median 0, >= 5 reads in 0.1% of pairs, 4/50 events with >= 100 reads overall; 22.8% of whitelisted-CB reads in the BAM carry an N in the CIGAR. `14_brie_10x.py` (SYNTHETIC 3-prime reads, uses the shipped `count_splicing_reads`): far-3-prime events 0.000 discriminating reads/cell/event (ambiguous 3.04) and are dropped by `brie-quant`; near-3-prime events 2.55 reads/cell/event and 10/10 big, 5/5 mid recovered, 1/35 null.
**Assertions:** PASS refusal; PASS "<0.1" claim; PASS far-exon claim; PASS near-3-prime claim; FAIL suggested Sierra call does not run.

## Step 6 — Research Veto (Data Analysis)

| Dimension | Result | Reason |
| --- | --- | --- |
| M1 Scientific integrity | PASS | no fabricated numbers; core quantitative claim reproduced (0.035 vs "<0.1") |
| M2 Practice boundaries | PASS | research tooling only |
| M3 Methodological baseline | PASS | chemistry gate, no imputation sound; pseudobulk without replicates is a P1 gap, not a fallacy |
| **M4 Code usability** | **FAIL** | MARVEL block (primary_tool), Psix snippet, Sierra call and two example helpers do not run; only BRIE2 CLI and `pseudobulk_junctions` ran as written |

## Recommendations

- **P0 MARVEL block:** use `AssignModality(marvel, sample.ids=..., min.cells=5, seed=1)` and `CompareValues(marvel, cell.group.g1=, cell.group.g2=, min.cells=5, method='wilcox', level='splicing', event.type='SE')`; keep `gene_id` in Exp; say event tables come from rMATS `fromGTF.*.txt`, RI needs IntronCounts, PSI is 0-1, `ComputePSI` (SE) errors with no minus-strand event.
- **P0 Psix and Sierra:** `Psix(psi_table=, mrna_table=)` + `run_psix(latent=<tsv>)` + `query('qvals < 0.05')`; `FindPeaks(bamfile=, junctions.file=)`; fix the Psix failure row.
- **P1 example script:** drop `briekit-event` (broken), fix `pseudobulk_by_celltype`, rename the per-cell differential helper, install BRIE2 from GitHub (`pip install brie` fails), remove the SpliZ pip line.
- **P1 pseudobulk:** per sample x cell type replicates (>= 3 per group), assert the summed total, set leafcutter `-g/-i/-c`.
- **P1 BRIE2 outputs:** name `varm[ELBO_gain, pval, fdr, cell_coeff]`, threshold on fdr, list the gene-filter flags, remove invented errors (`brie.tl.fit`, `min_reads=20`).
- **P2:** version line (Sierra 1.0+, BRIE2 0.2.4+), `tool_type`/`primary_tool` mismatch, no `references/`, `dts` dependency.

## Notes on the environment
brie-quant emits TensorFlow CUDA warnings on the CPU build (harmless). `Rscript` was only called through `r.sh`. The real BRIE tutorial BAMs were copied into `run\data\real` for the run and removed afterwards (scripts 01-05, 15, 43 need them restored from `public-data\singlecell`). The `briekit` build test used a throwaway venv in WSL `/tmp` (deleted); no shared env was modified.
