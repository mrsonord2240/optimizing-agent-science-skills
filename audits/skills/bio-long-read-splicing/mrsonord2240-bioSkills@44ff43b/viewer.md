> **Audit record for `bio-long-read-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/long-read-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-long-read-splicing

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/long-read-splicing` (first audit, unchanged upstream)
Category: Data Analysis (3) | Mode: D (Hybrid: SKILL.md + one shipped example script) | Complexity: Complex, N = 7

**Result: Static 67, Execution average 68.0, weighted 67.6 -> 68. Research Veto M4 (Code Usability) FAIL -> grade Reject, deployable = false, veto_override = true.**
Numerically 68 would be Beta Only; the veto forces Reject (same rule as `bio-pathway-kegg-pathways` 93 -> Reject in the pre-fix corpus).

Environment: `F:\OpenScience\audit-envs\alternative-splicing` (TOOLS.md read first). WSL `as-lr` (FLAIR 3.0.1, IsoQuant 4.0.0, minimap2 2.31, samtools 1.24, pysam 0.23.3), `as-sqanti` (SQANTI3 6.0.2), `as-rmatslong` (rMATS-long 2.1.0), Windows R 4.4.3 with `r-bambu.sh` (bambu 3.8.3, xgboost 1.7.8.1) and `r.sh` (DRIMSeq 1.34.0, DEXSeq 1.52.0, stageR 1.28.0).
Data: **synthetic** planted-truth data made by `run/make_synth.py` (seed 20260920) and `run/make_micro.py` (seed 777), both under `run/data/`; plus **real** FLAIR-test LRGASP cDNA (hg38 chr12/17/20) and real SG-NEx A549 ONT direct RNA (bambu extdata). Public-data was only read or copied, never written; the external clone was not touched (no `__pycache__`, `git status` clean).

## Step 1 — Skill Veto: PASS
- Stability PASS: failures are loud, deterministic and one-token fixable, not random (counted under M4, not T1). Contract PASS (frontmatter `name`, `description`, `license`, `tool_type` present). Determinism PASS: repeated `flair collapse` and `isoquant` runs gave identical md5 (t12). Security PASS: no eval of user strings, no credentials; example writes only under its output dir.

## Step 2 — Static (25 criteria): 67 / 100
| Category | Score | Note |
|---|---|---|
| Functional Suitability | 8/12 | Broad; correctness 2/4 (wrong FLAIR 3 flags, `isoquant.py`, contradictory `-uf`, false microexon claim, wrong Common Errors rows) |
| Reliability | 7/12 | Failure-mode sections exist but several entries are wrong; example aborts at first IsoQuant call |
| Performance/Context | 5/8 | 488-line SKILL.md loaded at once, usage-guide repeats it, no references/ |
| Agent Usability | 10/16 | Clear decision tree; inconsistent recipes; few output formats specified |
| Human Usability | 5/8 | Natural trigger text; no clarifying question on strandedness/orientation |
| Security | 11/12 | Safe; example does not validate or quote |
| Maintainability | 7/12 | Monolithic; example fails from clean copy; versions not pinned |
| Agent-Specific | 14/20 | Precise trigger; 7/7 Related Skills exist; no handoff/stop conditions |

Shipped-means-present (gate 8): `usage-guide.md`, `examples/longread_splicing_pipeline.sh` exist; the seven Related Skills paths all resolve (`alternative-splicing/{splicing-quantification,isoform-switching,single-cell-splicing,splice-variant-prediction}`, `long-read-sequencing/{isoseq-analysis,long-read-alignment,long-read-qc}`). No missing primary file. Scope (gate 7): research tooling only, no diagnosis or triage.

## Step 4 — Test inputs (Complex -> 7)
1. (Canonical) Bulk HiFi/ONT: align with the SKILL's minimap2 recipe, then FLAIR correct -> collapse -> quantify across 3 v 3 samples, and again on real LRGASP cDNA.
2. (Variant A) IsoQuant discovery + quantification on the same reads (6 FASTQ as 6 samples, BAM input, de novo, ONT stranded/unstranded, real ONT direct RNA).
3. (Variant B) Bambu joint discovery + quantification with the NDR table, synthetic and real ONT.
4. (Edge) SQANTI3 classification + filtering of 10 planted isoforms with known categories, plus FLAIR -> SQANTI3.
5. (Stress) The shipped example pipeline end to end from a clean copy, hifi and ont.
6. (Scope boundary) Differential isoform analysis on long reads: rMATS-long ASM workflow and the DRIMSeq DTU block, planted GA.1:GA.2 70:30 -> 20:80.
7. (Adversarial/ambiguous) "ONT direct cDNA, unstranded: which minimap2 recipe, and does it keep a 10-nt microexon?"

## Summary table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical: minimap2 + FLAIR | 27 | 40 | 67 | 2/5 | yes | PARTIAL (verbatim `flair correct` fails) |
| 2 | Variant A: IsoQuant | 28 | 42 | 70 | 3/5 | yes | PARTIAL (`isoquant.py` not found) |
| 3 | Variant B: Bambu | 33 | 47 | 80 | 4/5 | yes | COMPLETED |
| 4 | Edge: SQANTI3 planted categories | 34 | 51 | 85 | 3/5 | yes | COMPLETED |
| 5 | Stress: shipped example | 20 | 25 | 45 | 0/5 | yes | ERROR |
| 6 | Scope boundary: rMATS-long + DTU | 28 | 41 | 69 | 3/5 | yes | PARTIAL |
| 7 | Adversarial: -uf / microexon | 24 | 36 | 60 | 2/5 | yes | PARTIAL |

**Execution average: 68.0 / 100 (476/7). Assertion pass rate: 17/35.** Layer 1 average 27.7/40, Layer 2 average 40.3/60 (below Limited Release floors 28/42 as well).
7/7 inputs executed at least in part. **Not executed:** single-cell block (`skera`, `lima`, `isoseq3`, `match_cell_barcode` not installed, and `match_cell_barcode` flags unverifiable), `flair diffSplice --test` in `as-lr` (no Rscript; DRIMSeq step run through a patched copy of FLAIR's R script on Windows R), SQANTI3 CAGE/polyA/short-read/ORF arms, uLTRA/deSALT, StringTie2 hybrid, FLAMES/scNanoGPS.

## Research Veto: FAIL
| Dimension | Result |
|---|---|
| M1 Scientific Integrity | PASS (citations real; unsourced rule-of-thumb percentages are P2) |
| M2 Practice Boundaries | PASS |
| M3 Methodological Ground | PASS (contradictions and overclaims logged as P1) |
| **M4 Code Usability** | **FAIL** (see inputs 1, 2, 5, 6: documented code does not run on current FLAIR 3.0.1 / IsoQuant 4.0.0 / SQANTI3 6.0.2 from a clean copy, error text captured) |

## Detailed outputs

### Input 1 — minimap2 + FLAIR (executed: `t1_align.sh`, `t2_flair_synth.sh`, `t2b_flair_sr.sh`, `t3_real_flair.sh`, `t3b_real_flair_k14.sh`, `t_compare_all.sh`)
**Prompt:** "I have 3 control and 3 treated HiFi Iso-Seq samples. Align, then run FLAIR correct, collapse, quantify (and diffSplice) and tell me which isoforms change."
Second method: `junction_check.py` (pysam CIGAR N vs planted truth) and `compare_counts.py` (exact intron-chain match of each tool's models against truth).

Alignment (SKILL recipes, synthetic reads, truth known):
```
hifi_splicehq_uf_sec  reads 1723 mapped 100% spliced 100% exact chain 95.0%  sub-chain 5.0%  false-junction reads 0
```
`flair correct` exactly as SKILL.md:
```
correct: error: unrecognized arguments: --genome .../chrS1.fa --shortread sj.bed        (rc=2)
```
FLAIR 3.0.1 `correct` accepts only `-q -f --junction_tab|--junction_bed --junction_support -o -t --nvrna -w`. Wheels of FLAIR 2.0.0-2.2.0 still define `-g/--genome` and `-j/--shortread` (t13), so the Skill's "FLAIR 2.0+" claim holds only for 2.x.

With the flags that exist, annotation only:
```
truth_tx  truth_n observed_n   err%  matched model
GA1         692      810     +17.1%  GA.1_GA
GA2         852      852      +0.0%
GAN1        147      147      +0.0%
GAN2        118        0    -100.0%  (NOT REPORTED)      <- novel acceptor 24 nt inside intron; 20 reads/sample went to 'inconsistent'
GB1 709/709  GBN1 360/360  GC1 551/551
```
With `--junction_bed` (stand-in for the SKILL's short-read junctions): **all 7 isoforms exact, 0.0% misassigned.**
`flair diffSplice` (no `--test`) inclusion/exclusion table matched planted counts (inclusion of E3 = GA.1 + GA.N1 = 218/220/228 vs 99/95/97). `--test` failed in `as-lr` (no `Rscript`; FLAIR's R script also needs the R `argparse` package). Run through Windows R with a patched argument parser it produced no significant call on the 2-gene toy (DRIMSeq `dmPrecision` degenerates) and writes no plots, so the SKILL's "visual sashimi-like plots" is not what diffSplice outputs.

Real LRGASP cDNA (1883 reads), Skill's HiFi recipe vs FLAIR's own expected output:
```
minimap2 -ax splice:hq -uf --secondary=no : distinct junctions 1566 (2.6% annotated), FLAIR correct 972 corrected / 851 inconsistent
minimap2 -ax splice -k14                   : distinct junctions  242 (15.3% annotated), FLAIR correct 1536 corrected   (expected/test-correct_all_corrected.bed: 1534)
```
**Assertions:** [PASS] alignment recipe correct on oriented reads; [FAIL] verbatim `flair correct` runs; [PASS] repaired FLAIR pipeline reproduces truth; [FAIL] annotation-only keeps the novel-site isoform; [FAIL] `-uf` alignment feeds FLAIR as many corrected reads as expected (972 vs 1534). Scores: Basic 27 / Specialized 40 / Total 67.

### Input 2 — IsoQuant (executed: `t4_isoquant.sh`, `t12_real_sqanti.sh` determinism)
**Prompt:** "Run IsoQuant with the annotation on my six HiFi samples and give me transcript counts including novel isoforms."
```
isoquant.py ... : exec: isoquant.py: not found (rc 127)          [pip wheel entry point is `isoquant`; isoquant.py exists only in a git checkout]
isoquant (same flags, --data_type pacbio_ccs --model_construction_strategy default_pacbio): rc 0, OUT.transcript_models.gtf + counts
```
Against truth: GA.2 852/852, GB.1 709/709, GC.1 551/551; novel skip-E2 136 vs 147; novel GB skip 360/360; **novel 24-nt acceptor (118 reads) not reported, read_info calls it `full_splice_match / unique_minor_difference` and counts it in GA.1 (821 vs 692, +18.6%)**. De novo (no `--genedb`) recovered 6 of 7 planted isoforms (GA split over two novel gene IDs). `--genedb` optional, `--model_construction_strategy` valid, `--bam --prefix` layout matches the example (`isoquant/sample/sample.transcript_models.gtf`). Default quantification is `unique_only` (real ONT slice: IsoQuant 28 vs Bambu 88 counts on 129 reads), not mentioned. Repeat run: identical md5.
**Assertions:** [FAIL] `isoquant.py` runs; [PASS] entry-point run completes; [PASS] annotated counts exact; [FAIL] all novel isoforms reported; [PASS] output path as in example. Scores 28 / 42 / 70.

### Input 3 — Bambu (executed: `t5_bambu.R`, `t5b_bambu_ndr.R`, `t6_bambu_real.R` under `r-bambu.sh`)
**Prompt:** "Use Bambu with NDR 0.1 for joint discovery and quantification on my six BAMs."
SKILL block ran unmodified: `RangedSummarizedExperiment` 4 x 6, six output files, `assays(se)$counts` and `transcriptToGeneExpression(se)` fine. Known isoforms exact (GA.2 852, GB.1 709, GC.1 551). NDR sweep on 3.4k reads: 0.05 -> 0 novel, 0.1 -> 0, 0.3 -> 1, 1.0 -> 2 (Bambu warns "<50 read classes ... NDR approximated"; the Skill states no data-size requirement). Real ONT A549 chr9 slice: 105 transcripts, total 88 at every NDR; 127 of 129 primary reads overlap annotated exons (GenomicAlignments). Needs xgboost 1.x (env `r-bambu.sh`), R segfaults at exit after output (environment).
**Assertions:** [PASS] block runs; [PASS] assays/transcriptToGeneExpression; [PASS] known counts; [FAIL] default NDR reports planted novel isoforms (toy scale); [PASS] real ONT run sane. Scores 33 / 47 / 80.

### Input 4 — SQANTI3 (executed: `t7_sqanti.sh`, `t7b_sqanti_more.sh`, `t12_real_sqanti.sh`)
**Prompt:** "Classify these long-read isoforms against the annotation and filter out intra-priming and RT-switching."
```
Q01 full-splice_match OK | Q02 FSM OK | Q03 incomplete-splice_match (3prime_fragment) OK | Q04 novel_in_catalog (combination_of_known_splicesites) OK
Q05 novel_not_in_catalog (at_least_one_novel_splicesite) OK | Q06 novel_in_catalog (intron_retention) OK | Q07 genic_intron OK | Q08 intergenic OK
Q09 antisense OK | Q10 FSM OK                                           category matches: 10/10
```
Filter: planted A-rich TTS isoform (`perc_A_downstream_TTS` 100 > 59) removed, others pass. FLAIR-collapsed isoforms (GTF and `--fasta` routes): 7/7 correct labels. Failures: `--CAGE_peak refTSS_v3.3...`/`--polyA_motif_list` files have no source in the Skill (run aborts "not found"); `sqanti3_filter.py rules` report step fails in R (`filter_report.log`: tidyselect `stop_subscript_oob`, rc=1; `--skip_report` rc=0); `--skipORF` (not in this Skill, flagged by the tooling pass) is rejected by 6.0.2; category table omits `genic_intron`. Real FLAIR isoforms (36): 7 FSM, 19 ISM, 2 NIC, 2 NNC, 5 antisense, 1 genic, so the "FSM >= 50%" rule of thumb is not met on this subset.
**Assertions:** [PASS] 10/10 categories; [PASS] filter removes planted intra-priming; [PASS] FLAIR -> SQANTI3 labels; [FAIL] inputs obtainable from the Skill; [FAIL] filter completes rc 0 with report. Scores 34 / 51 / 85.

### Input 5 — shipped example from a clean copy (executed: `t10_example.sh`, `patch_example.py`, `check_filter_gtf.sh`)
**Prompt:** "Run the example pipeline on my sample (PLATFORM=hifi)."
```
stage 0 (verbatim): exit 127  ex0.sh: line 44: isoquant.py: command not found
stage 1 (isoquant):  exit 2    flair correct: unrecognized arguments: --genome reference.fa
stage 2 (no --genome): exit 1  sqanti3_qc.py --output longread_output_sample/sqanti3 -> FileNotFoundError .../sqanti3_results/longread_output_sample/sqanti3.qc_params.txt
stage 3 (SQANTI3 --output sqanti3 --dir ...): exit 1  sqanti3_filter.py --filter_gtf <IsoQuant GTF>: AssertionError raw[2]=='transcript'; sqanti3_filtered.filtered.gtf is 0 bytes
root cause check: dropping the 3 `gene` rows from IsoQuant's transcript_models.gtf makes the filter write a 2278-byte GTF (rc 0)
```
The script's classification path `sqanti3/${SAMPLE}_classification.txt` is also wrong (real: `<dir>/sqanti3_classification.txt`). With PLATFORM=ont on unstranded ONT cDNA the example's `splice -uf -k14`: exact chains 46.2%, false-junction reads 51.5%, inferred gene strand wrong for 846/1665.
**Assertions:** all 5 FAIL. Scores 20 / 25 / 45.

### Input 6 — rMATS-long + DTU (executed: `t8_rmatslong.sh`, `t9_dtu.R`, `t9b_dtu_sim.R`)
**Prompt:** "Find differential splicing between my 3 control and 3 treated long-read samples with rMATS-long, then test DTU on the FLAIR counts."
rMATS-long: all seven SKILL commands rc=0, flags match `--help`. Result:
```
asm 0_0 GA  lr 388.4  adj_p 1.8e-86  group1 proportion 0.695  group2 0.209  delta_isoform_proportion 0.486 (planted 0.49)   'exon skipping': 1   GB, GC not called
```
DTU block as written: `read.table('flair_quantified_counts.tsv')` (FLAIR writes `<out>.counts.tsv`) and `dmDSdata(counts=<FLAIR counts>, ...)` stops with `all(c("gene_id","feature_id") %in% colnames(counts)) is not TRUE`; `library(DEXSeq)` after DRIMSeq masks `results()`. Minimal repair + the SKILL's dmFilter on a 300-gene synthetic matrix with 30 planted DTU genes: called 36, TP 30, FP 6, FN 0 (recall 1.00, precision 0.83); stageR 36 genes / 84 transcripts. The SKILL's failure mode "rMATS-long expects per-sample isoform GTFs, not raw alignments" contradicts its own BAM workflow, which ran.
**Assertions:** [PASS] seven commands; [PASS] recovers planted switch; [FAIL] DTU block runs; [PASS] repaired DRIMSeq recovers 30/30; [FAIL] internal consistency. Scores 28 / 41 / 69.

### Input 7 — unstranded ONT cDNA, `-uf`, microexon (executed: `t1_align.sh`, `t11_microexon.sh`, `t3_real_flair.sh`)
**Prompt:** "ONT direct cDNA (PCS-114), unstranded. Which minimap2 recipe? And I need to see a 10-nt microexon."
```
ontunstr  splice -k14        exact 94.7%  false-junction reads 1.1%   strand correct 1665/1665     <- SKILL body
ontunstr  splice -uf -k14    exact 46.3%  false-junction reads 51.5%  strand wrong 846/1665        <- Decision Tree, usage-guide, example
ontstr    splice -uf -k14    exact 93.9%  (direct RNA: -uf correct)
real LRGASP cDNA: -uf 1566 junctions (2.6% annotated) vs no -uf 242 (15.3%)
10-nt microexon (150 inclusion + 150 skipping reads):
  splice:hq -uf --secondary=no          kept 0/150
  splice -uf -k14                        kept 0/150     IsoQuant then reports M.inc = 0
  + --junc-bed                           150/150 (HiFi), 131/150 (ONT)   + --junc-bonus 20: 150/150
```
`minimap2: too many anchors` does not occur in the binary and `-N` sets the number of retained secondaries [5], so the Common Errors row "Use -N 50 to limit secondary alignments" is unfounded. "No quantification uncertainty" is overstated (IsoQuant left 22/300 microexon-test reads ambiguous; 118 novel-site reads absorbed by GA.1).
**Assertions:** [PASS] body recipe correct; [FAIL] guidance consistent; [FAIL] documented recipes keep a microexon; [PASS] `--junc-bed` rescues it; [FAIL] no-uncertainty claim holds. Scores 24 / 36 / 60.

## Step 8 — Final
```
Static 67 x 0.4 = 26.8 | Execution 68.0 x 0.6 = 40.8 | FINAL 67.6 -> 68
Numeric band: Beta Only. Research Veto M4 FAIL -> GRADE Reject, deployable false, veto_override true
Floors (for the record): Static >= 70 not met (67), Execution >= 75 not met (68.0), L1 >= 28 not met (27.7), L2 >= 42 not met (40.3), assertions >= 80% not met (49%)
```
Key strengths: SQANTI3 section (10/10 planted categories, intra-priming filter); rMATS-long workflow (7/7 commands correct, planted dPI recovered); Bambu block runs as written; decision tree and body ONT recipe.

Recommendations (P0 -> P2): see `eval_report_bio-long-read-splicing_result.json`.
- P0 shipped example aborts (four breakages in sequence); P0 FLAIR `--genome/--shortread` and `isoquant.py` do not run on current versions.
- P1 `-uf` prescribed for unstranded ONT cDNA in three places; P1 microexon "no anchor problem" claim false; P1 DTU block does not run on FLAIR output; P1 FLAIR annotation-only drops novel splice-site isoforms and the fix flag is wrong; P1 rMATS-long failure-mode contradiction and overstated "no uncertainty".
- P2 SQANTI3 inputs/report/category table; P2 FLAIR diffSplice prerequisites, manifest format, bogus Common Errors rows; P2 unsourced thresholds and unrun single-cell block; P2 redundant usage-guide, monolithic SKILL.md.

## Run order and files (all in `run/`)
`make_synth.py`, `make_micro.py` (synthetic data) -> `help_probe.sh`, `help_probe2.sh` (every flag vs installed `--help`) -> `t1_align.sh`, `t2_flair_synth.sh`, `t2b_flair_sr.sh`, `t3_real_flair.sh`, `t3b_real_flair_k14.sh`, `t4_isoquant.sh`, `t_compare_all.sh` -> `t5_bambu.R`, `t5b_bambu_ndr.R`, `t6_bambu_real.R` (needs `out/flair/*.bam` from t2; BAMs were deleted after the audit, rerun t2 first) -> `t7_sqanti.sh`, `t7b_sqanti_more.sh`, `t8_rmatslong.sh`, `t9_dtu.R`, `t9b_dtu_sim.R`, `t10_example.sh` (+`patch_example.py`, `check_filter_gtf.sh`), `t11_microexon.sh`, `t12_real_sqanti.sh`, `t13_flair_versions.sh`. Checkers: `junction_check.py`, `compare_counts.py`, `real_junction_concordance.py`. `ds_patched_drimseq.R` is FLAIR's `diffSplice_drimSeq.R` with the R `argparse` call replaced by a manual parser (auditor patch). `build_report.py` writes the JSON. Logs in `run/logs/`; tool outputs in `run/out/`; `skill_copy/` is the unmodified Skill copy (nothing was run inside `external\`).
