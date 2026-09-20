> **Audit record for `bio-long-read-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@887eaed](https://github.com/mrsonord2240/bioSkills/tree/887eaeddf09532feee6caaf5f325d0c9b3ce7101/alternative-splicing/long-read-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-long-read-splicing (SECOND RE-AUDIT of the fixed Skill)

Generated: 2026-09-20  
Source: `mrsonord2240/bioSkills@887eaeddf09532feee6caaf5f325d0c9b3ce7101:alternative-splicing/long-read-splicing` (fix branch `fix/as-longread`, round 2 on top of c07c53c). Read from the worktree, run from a copy in `run/skill_copy/` (sha1 of SKILL.md, usage-guide.md and the example identical to the worktree; nothing written into the worktree, `external\` or `public-data\`).  
Previous: first re-audit 80, Limited Release, 2 open P1 (`_pre-fix-20260920b`); original audit 68, Reject (`_pre-fix-20260920`).  
Category 3 Data Analysis, mode D (hybrid), Complex, N = 8. The fix log was read for orientation only; every number below comes from my own runs (logs in `run/logs/`, scripts in `run/`).

**Result: static 78, execution average 86.5, final 83, Limited Release, deployable true, no veto, no open P0, no open P1, 5 P2.**  
Layer averages: L1 33.8/40, L2 52.8/60, assertions 34/40 (85%). Floors for Limited Release met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%); Production Ready floors not met (static 78 < 80).

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical - FLAIR workflow (correct-collapse-quantify-diffSplice --test) on planted 3v3 HiFi and real LRGASP cDNA | 34 | 54 | 88 | 4/5 | ✅ |
| 2 | Variant A - IsoQuant discovery/quantification and Bambu with NDR 0.1 | 34 | 53 | 87 | 5/5 | ✅ |
| 3 | Variant B - SQANTI3 classification and filtering, with CAGE and polyA support | 35 | 54 | 89 | 5/5 | ✅ |
| 4 | Stress - Shipped example from a clean copy: hifi, ont, drna, +SR_JUNCTIONS, real ONT cDNA, real direct RNA | 35 | 55 | 90 | 5/5 | ✅ |
| 5 | Scope Boundary - Differential isoform analysis: DRIMSeq/stageR DTU, rMATS-long ASM mode with failure paths | 34 | 53 | 87 | 4/5 | ✅ |
| 6 | Adversarial - Unstranded ONT cDNA or unoriented HiFi: which minimap2 recipe, is -uf right? | 35 | 55 | 90 | 5/5 | ✅ |
| 7 | Edge - NEW: microexon recipe on my own 3-27 nt set, both directions, tandem pairs, real-read side effects | 32 | 50 | 82 | 3/5 | ✅ |
| 8 | Edge - NEW: Kinnex array de-concatenation with skera, then lima and isoseq refine | 31 | 48 | 79 | 3/5 | ✅ |

**Execution average 86.5 / 100.** Static 78 x 0.4 = 31.2; dynamic 86.5 x 0.6 = 51.9; 83.1 -> **83**.

Inputs 1-6 re-run the previous audits' inputs as regression tests, on data I regenerated from the first re-auditor's generators (`gen_planted.py`, `gen_micro.py`; same md5 on regeneration) and the first auditor's (`prior_make_*.py`), plus real reads. Inputs 7 and 8 are new and use generators of my own (`gen_micro2.py`, seed 9191, GC 0.58, 12 microexon sizes 3-27 nt plus two tandem pairs; `mk_kinnex3.py`, a 6-fold Kinnex array with reversed and defective arrays), so the score does not only measure what the fixers were told about. Input 7 also carries the real-read consequences of the bonus setting.

## Research Veto, re-judged

| | Result | Evidence |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated identifiers or results. The fixer's new numbers reproduce on independent data: -uf false-junction 48.2% and 30.5% (unoriented HiFi), ts:+ 1.000/0.502/0.503, bonus-20 recoding of skipping reads (HiFi 6-nt exon: skipping 0 of 150), bonus 17 dangling junctions on real reads 12 (0 at <=16) with a flair correct crash at 17-20, DTU 20/20, rMATS-long 20/20, flair diffSplice --test 20/20. Two claims are scoped to one sequence or one error profile (uLTRA 150/150 for a 10-nt exon; dRNA 99% at bonus 16), see P2 items. |
| M2 Practice boundaries | PASS | Research tooling only; ALS cryptic-exon and ASO items are pointers, nothing diagnostic or prescriptive. |
| M3 Methodological baseline | PASS | The microexon recipe now carries the skipping-read control the previous audit asked for and it holds on my independent set of 12 sizes in both directions (HiFi 100.0 inc / 99.9 skip, ONT 99.6 / 99.2 at bonus 16); -uf guidance consistent in body, decision tree, usage-guide and example. |
| M4 Code usability | PASS | 12 of the 14 fenced blocks of SKILL.md were extracted and run verbatim (the install line only dry-run, the ESPRESSO abundance-mode rMATS-long command not run: it needs a user-supplied file): alignment recipes, microexon awk and pysam snippet, FLAIR block incl. diffSplice --test, IsoQuant, SQANTI3, rMATS-long, DTU R block, the short-read-junction BED recipe, skera block (Bambu with ncore = 1 as the block instructs on Windows R). The shipped example ran end to end from a clean copy for hifi, ont, drna (with and without SR_JUNCTIONS), real ONT cDNA and real direct RNA, exit 0 with content asserted. |

## Regression: what the first re-audit found and what changed

| Round-1 re-audit finding | Now | How I know |
|---|---|---|
| P1 microexon `--junc-bonus 20` flips skipping reads to inclusion | fixed | recipe is HiFi `--junc-bed` alone, ONT/dRNA bonus 16; on my set bonus 20 gives HiFi skipping 58.3%, bonus 16 99.9% (input 7) |
| P1 rMATS-long block lacks `mkdir alignment_info`, silent empty tables | fixed | block verbatim rc 0, 20/20; truncated / header-only BAM rc 1 (input 5) |
| P2 IsoQuant `transcript_model_counts.tsv` named | fixed | file list checked (input 2) |
| P2 Bambu `ncore = 8` on Windows | fixed (documented) | fails as documented, `ncore = 1` runs (input 2) |
| P2 `flair diffSplice --test` prerequisites | fixed, one gap | verified 20/20 with as-lr-drim; an event type with no genes after DRIMSeq's filter fails silently (input 1) |
| P2 unverified Common Errors rows | fixed | `prepareAnnotations` row reproduced on an empty and a 6-column GTF (`t30`) |
| P2 monolithic SKILL.md | not fixed, worse | 38.8 kB, 580 lines (33 kB / 546 before) |

**What round 2 introduced:** nothing that breaks a recipe. The `--junc-bonus 16` choice is the right one (17 crashes `flair correct` on real ONT reads, reproduced). Small things: uLTRA overgeneralised, `--test` gap, an error-rate dependence not stated, the lima explanation, the file grew.

---

## Input 1 - Canonical: FLAIR workflow (correct-collapse-quantify-diffSplice --test) on planted 3v3 HiFi and real LRGASP cDNA

**Prompt:** I have 3 v 3 PacBio HiFi Iso-Seq samples, a GENCODE-style annotation and STAR junctions. Align, correct, collapse, quantify and test differential isoform usage with FLAIR (also on real ONT cDNA).

**Ran:** `t8_flair6.sh` (six planted HiFi samples aligned with the SKILL recipe, merged BAM, the FLAIR block extracted verbatim by `extract_blocks.py` and run with an `Rscript` wrapper for env `as-lr-drim` first on PATH), `t5_real.sh` (real LRGASP reads; alignment block, orientation awk and FLAIR block verbatim), `eval_diffsplice.py`.

**Printed (trimmed):**
```
planted: rc=0; Flair correct 0:00:12 / collapse 0:00:09 / quantify 0:00:11 / diffsplice 0:00:59
         corrected reads 49665, inconsistent 0, collapsed isoforms 124 (truth 124 chains)
         counts.tsv: ids  ctrl1_ctrl_b0 ... trt3_trt_b0 ; G001A_G001 54 55 44 22 10 13
         alt3 / ir: "event matrix file empty, not running DRIMSeq"
         eval_diffsplice: ES events in quant table 63 ; tested by DRIMSeq 22 ; planted DTU genes recovered 20/20 ; other genes ['G037', 'G042']
real:    align block rc=0 ; ts:A:+ ont_cdna 0.503, isoseq recipe 0.498 ; FLAIR block rc=0
         corrected 1672, inconsistent 214, isoforms 33 ; drimseq_alt3/es/ir written
         alt5: "!No genes left after filtering!" + R traceback, FLAIR rc 0, no drimseq_alt5 file
```
**Scores:** Basic 34/40 | Specialized 54/60 | Total 88/100 ✅

**Assertions:**
- [PASS] FLAIR block extracted verbatim from SKILL.md (correct, collapse, quantify, diffSplice --test) runs on 6 planted HiFi samples and on real LRGASP reads - rc 0 both; planted: 49665 corrected, 0 inconsistent, 124 isoforms; real: 1672 corrected / 214 inconsistent, 33 isoforms
- [PASS] All 124 planted isoforms, incl. the two unannotated ones, are recovered when the SJ.out.tab junctions are passed - 124 collapsed isoforms = 124 truth chains; SQANTI3 later calls G057N novel_in_catalog, G058N novel_not_in_catalog
- [PASS] flair diffSplice --test works with the prerequisites the SKILL lists (Rscript with DRIMSeq, argparse, data.table) - as-lr-drim Rscript first on PATH: drimseq_es tested 22 events, planted DTU 20/20, 2 other genes (G037, G042); alt3/ir 'event matrix file empty, not running DRIMSeq' as the text says
- [PASS] Orientation check on real cDNA reads gives the SKILL's ~0.5 - 0.503 (ONT recipe), 0.498 (HiFi recipe) on LRGASP; planted 1.000 (HiFi) / 0.502 (ONT unstranded)
- [FAIL] A failed DRIMSeq test for an event type is reported, not silent - real 6-sample data: alt5 has events but none survive dmFilter; R prints '!No genes left after filtering!' + traceback, FLAIR exits 0 and writes no drimseq_alt5 file; the SKILL only describes empty event types

---

## Input 2 - Variant A: IsoQuant discovery/quantification and Bambu with NDR 0.1

**Prompt:** Discover and quantify isoforms from my HiFi samples with IsoQuant, then use Bambu with NDR 0.1.

**Ran:** `t6_isoquant.sh` (block verbatim on two planted FASTQ files, default prefix; then `--illumina_bam` with 125,055 simulated short reads, `gen_sr.py`, `iq_novel_check.py`), `t19_denovo_novelsite.sh`, `t7a_bambu_bams.sh` + `t7c_bambu_run.sh` + `t7b_bambu_eval.R` (Windows R via `r-bambu.sh`), `t13_bambu_real.R` (real A549 dRNA).

**Printed (trimmed):**
```
isoquant block rc=0 ; OUT.transcript_models.gtf / transcript_counts.tsv / transcript_grouped_file_name_counts.tsv EXIST ; transcript_model_counts.tsv MISSING (not claimed any more)
grouped file header: gene_id sample1.fastq sample2.fastq ; G001A 54 22 ; G001B 14 44   (ctrl1 truth 54/14)
--illumina_bam: no illumina: G057N 37 reads, G058N no model ; with illumina: identical
de novo (no --genedb) on the example HiFi BAM: 121 models, 121/124 truth chains, G057N and G058N found
Bambu block verbatim (ncore = 8): "BiocParallel errors ... could not find function seqlengths", exit 1
Bambu ncore = 1: 122 transcripts x 3 samples; r vs truth 0.9992 / 0.9989 / 0.9990 ; novel transcripts 0 ("NDR approximated" warning)
real A549 dRNA (129 reads): 105 transcripts, total count 88 (11 with count > 0), 0 novel ; R segfaults at exit (rc 139) after 'Finished running Bambu'
```
**Scores:** Basic 34/40 | Specialized 53/60 | Total 87/100 ✅

**Assertions:**
- [PASS] IsoQuant block runs verbatim (2 FASTQ inputs, default prefix) and every output name the SKILL lists exists - rc 0; OUT.transcript_models.gtf, OUT.transcript_counts.tsv, OUT.transcript_grouped_file_name_counts.tsv, OUT.discovered_transcript_counts.tsv present; transcript_model_counts.tsv absent and no longer claimed
- [PASS] Per-sample IsoQuant counts match planted truth - G001A 54=54, G001B 14=14 (ctrl1), G001A 22 (trt1); annotated planted isoforms matched by exact chain 123/123
- [PASS] Bambu block: ncore=8 fails on Windows R (as the comment says) and ncore=1 gives counts matching truth; NDR caveat holds - ncore=8: 'BiocParallel errors ... could not find function seqlengths'; ncore=1: r 0.9992/0.9989/0.9990, 0 novel transcripts with the 'NDR approximated' warning; real A549 dRNA 105 transcripts, total 88
- [PASS] IsoQuant statements about novel sites and --illumina_bam hold: 30-nt donor shift has no model with --genedb, with or without short reads; de novo models it - iq_noillu = iq_illu: G057N 37 reads modelled, G058N none (125,055 short reads); de novo run: 121 models, 121/124 truth chains incl. G058N
- [PASS] IsoQuant counts the inclusion isoform for a microexon when fed the recipe alignment - micro2: HiFi --junc-bed 149.0/150 inclusion and 148.6/150 skipping (plain 87.0 / 210.5); ONT bonus 16 148.2 / 148.2 (plain 25.8 / 223.2)

Note: R exiting with a segfault after Bambu finishes is the machine's Windows-R/xgboost combination (TOOLS.md item 12), not the Skill's; the Skill does not mention it.

---

## Input 3 - Variant B: SQANTI3 classification and filtering, with CAGE and polyA support

**Prompt:** Classify my collapsed isoforms with SQANTI3 including CAGE and polyA support and filter artifacts.

**Ran:** `t0_download_support.sh` (the SKILL's Magdoll/images_public URLs: 4,811,158-byte CAGE BED.gz and the polyA list, HTTP 200), `t11_sqanti_real.sh` (block verbatim on real FLAIR `isoforms.gtf`, then on the planted FLAIR isoforms), `sqanti_check.py` (id-safe check), `t10_prior.sh` (first auditor's 10 query isoforms), `t17_filter_needs_awk.sh`.

**Printed (trimmed):**
```
real: rc=0 ; 33 isoforms {FSM 8, ISM 18, antisense 5, NIC 1, genic 1} ; within_CAGE_peak TRUE 7 / FALSE 26 ; polyA_motif_found TRUE 17 / FALSE 16 ; filter pass 29, filtered.gtf 143 lines
planted (sqanti_check.py): 124 isoforms {FSM 122, NIC 1, NNC 1}; annotated -> FSM 122/122
   G057N novel_in_catalog (combination_of_known_splicesites) ; G058N novel_not_in_catalog (at_least_one_novel_splicesite)
first auditor's 10 isoforms: 9/10 by his labels (Q07 genic_intron; his truth said genic) ; filter 10 pass, 44 GTF lines
full IsoQuant GTF into sqanti3_filter.py rules: rc=1 AssertionError
```
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 ✅

**Assertions:**
- [PASS] SQANTI3 block runs verbatim with the CAGE and polyA files fetched from the URLs the SKILL names - rc 0; 33 real isoforms: FSM 8, ISM 18, antisense 5, NIC 1, genic 1; within_CAGE_peak TRUE 7, polyA_motif_found TRUE 17; filter 29 pass, filtered GTF 143 lines
- [PASS] Planted annotated isoforms are FSM and the two unannotated ones get the right novel category - 122/122 FSM; G057N novel_in_catalog (combination_of_known_splicesites); G058N novel_not_in_catalog (at_least_one_novel_splicesite)
- [PASS] First auditor's 10 query isoforms classified as planted - 9/10 by his labels; Q07 is genic_intron, the correct SQANTI3 label for an exon inside an intron (his truth said genic)
- [PASS] The transcript/exon-only awk before the filter is necessary - full IsoQuant GTF into sqanti3_filter.py rules: rc 1 AssertionError; awk-filtered GTF passes
- [PASS] Filter step needs --skip_report on small inputs and the QC step accepts --report skip - used in the block and the example, both ran rc 0 on 6, 10, 33 and 123 isoforms

My first planted check (inline python in `t11`) keyed isoform ids wrongly and printed `None` for the novel ones; `sqanti_check.py` (id-safe, from the previous audit) is the check I score on.

---

## Input 4 - Stress: Shipped example from a clean copy: hifi, ont, drna, +SR_JUNCTIONS, real ONT cDNA, real direct RNA

**Prompt:** Run the shipped examples/longread_splicing_pipeline.sh on my HiFi / ONT cDNA / direct RNA sample (and on real reads).

**Ran:** `par_example.sh`, `par_example_sj.sh` -> `t4_example.sh <hifi|ont|drna> [sj]` (verbatim copy under `run/skill_copy/examples/`, inputs overridden through the environment variables its header documents), `t4b_eval.sh` + `eval_example.py` (pysam chains, IsoQuant/FLAIR counts vs truth by exact intron chain, SQANTI3 categories, filter output), `t10_prior.sh` (first auditor's reads + `prior_junction_check.py`), `t12_realdrna.sh` (real A549 dRNA), `t27_example_realont.sh` (real LRGASP cDNA, without and with SR_JUNCTIONS). The first SR_JUNCTIONS launch failed because `data/plant/SJ.out.tab` had not been made yet (my step order, fixed with `make_sj.py`).

**Printed (trimmed):**
```
                      hifi        ont (unstranded)   drna
exit code             0           0                  0          (also with SR_JUNCTIONS: 0 / 0 / 0)
exact chains          91.5%       82.8%              65.2%      (5'-truncated reads: consistent 100 / 99.9 / 99.8%)
false-junction reads  0.0%        0.0%               0.0%
"Reads with an intron next to a soft clip": 0 in every run ; ts:A:+ 1.000 / 0.502
FLAIR r vs truth      0.9996      0.9990             0.9935     IsoQuant 0.9987 / 0.9956 / 0.9817 (__ambiguous 87 / 165 / 426)
IsoQuant models 123 = 123 truth chains ; SQANTI3 FSM 122 + NIC 1 (G057N) in all three ; filter 123 pass, filtered GTF 673 lines
+SR_JUNCTIONS: FLAIR G058N 0/9 -> 9/9 (hifi), 9/9 (ont), 10/10 (drna) ; IsoQuant G058N still no model
first auditor's reads: PLATFORM=hifi exact 95.6%, ont 96.0%, 0 false junctions, filter 6 pass / 29 lines
real A549 dRNA (129 reads): exit 0 ; 114 spliced ; IsoQuant 6 models (61 CDS rows kept by the awk step) 29 reads counted + 54 ambiguous ; FLAIR 10 isoforms ; SQANTI3 6 FSM ; filter 6 pass, 70 lines
== real ONT cDNA, nosj: example exit code 0
Spliced reads with ts:A:+ (transcript orientation): 0.503 (n=1510)
Reads with an intron next to a soft clip: 0
IsoQuant models: 10; counted to annotated transcripts: 1188; __ rows: __ambiguous=477 __no_feature=1 __not_aligned=0 
FLAIR isoforms: 33; corrected 1672 inconsistent 214
SQANTI3 rows 10 {'full-splice_match': 10}
filter: pass 10, filtered.gtf 94
== real ONT cDNA, sj: example exit code 0
Spliced reads with ts:A:+ (transcript orientation): 0.503 (n=1510)
Reads with an intron next to a soft clip: 0
IsoQuant models: 10; counted to annotated transcripts: 1188; __ rows: __ambiguous=477 __no_feature=1 __not_aligned=0 
FLAIR isoforms: 33; corrected 1672 inconsistent 214
SQANTI3 rows 10 {'full-splice_match': 10}
filter: pass 10, filtered.gtf 94
```
**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100 ✅

**Assertions:**
- [PASS] examples/longread_splicing_pipeline.sh, run from a clean copy, exits 0 for PLATFORM=hifi, ont, drna and with SR_JUNCTIONS - 6/6 runs exit 0; first auditor's synthetic reads: hifi 95.6% and ont 96.0% exact chains, 0 false-junction reads, filter 6 pass
- [PASS] Alignment content is right: exact chains, no false junctions, orientation and dangling-junction checks print the expected values - planted exact chains 91.5 / 82.8 / 65.2% (5'-truncated reads consistent 100 / 99.9 / 99.8%), false-junction 0.0 / 0.0 / 0.0%; ts:+ 1.000 / 0.502; intron-next-to-soft-clip 0 in all runs
- [PASS] IsoQuant, FLAIR and SQANTI3 outputs match planted truth - IsoQuant r 0.9987 / 0.9956 / 0.9817 vs truth, FLAIR 0.9996 / 0.9990 / 0.9935; 123/123 IsoQuant models = truth chains; SQANTI3 FSM 122 + NIC 1 in all three; filtered GTF 673 lines
- [PASS] SR_JUNCTIONS makes flair correct keep the unannotated 30-nt isoform - G058N 0/9 -> 9/9 (hifi), 9/9 (ont), 10/10 (drna); IsoQuant still has no model (merged), as the SKILL says
- [PASS] Runs on real reads: LRGASP ONT cDNA (with and without real short-read junctions) and A549 direct RNA - real LRGASP cDNA (1883 reads): exit 0 both ways, ts:A:+ 0.503, dangling 0, IsoQuant 10 models (1188 reads counted, 477 ambiguous), FLAIR 33 isoforms (1672 corrected / 214 inconsistent), SQANTI3 10 FSM, filter 10 pass; SR_JUNCTIONS changes nothing there because the test junction file has 8 rows (7 annotated); real A549 dRNA (129 reads): exit 0, 6 models, FLAIR 10 isoforms, SQANTI3 6 FSM

---

## Input 5 - Scope Boundary: Differential isoform analysis: DRIMSeq/stageR DTU, rMATS-long ASM mode with failure paths

**Prompt:** Test differential isoform usage between my 3 v 3 long-read groups: DTU with DRIMSeq/stageR, FLAIR diffSplice, and rMATS-long.

**Ran:** `t9_dtu.R` (the DTU block sourced verbatim; Windows R via `r.sh`) on the planted FLAIR output and on the real 6-sample output, `t9_rmatslong.sh` (block verbatim on 6 planted BAMs plus three failure paths), `eval_rmatslong.py`.

**Printed (trimmed):**
```
DTU on planted FLAIR counts: genes tested 60 (planted 20/20 tested); stage-wise significant 22; planted 20/20; other G037, G042
DTU on real LRGASP counts: runs to the end; "No genes were found to be significant on a 5% OFDR level"; dtu NULL
rMATS-long (a) planted 3v3: rc=0; samples.tsv 6 rows; alignment_info 6 TSV + index; differential_asms.tsv 65 lines, differential_isoforms.tsv 131 lines
   ASM rows 64 genes 60 ; adj p < 0.05: 25 genes, planted DTU 20/20, other 5 ; < 0.01: 23 / 20 / 3
(b) truncated BAM: rc=1, "[E::bgzf_read_block] ... samtools view: error reading file ctrl2.bam", no output dir
(c) header-only BAM: rc=1, "empty or missing alignment_info/trt3.tsv", no output dir
(d) contig names differ (chrQ vs Q): rc=1, "KeyError: 'ctrl1'" (rmats-long), no result tables
```
**Scores:** Basic 34/40 | Specialized 53/60 | Total 87/100 ✅

**Assertions:**
- [PASS] DTU block sourced verbatim on the FLAIR quantify output recovers the planted DTU genes - 60 genes tested, 22 stage-wise significant, planted 20/20, other G037 G042
- [PASS] DTU block runs to the end on the real 6-sample FLAIR counts and reports no significant gene - 'No genes were found to be significant on a 5% OFDR level', dtu NULL (as the block comment says)
- [PASS] rMATS-long block as written (mkdir, samples.tsv, set -euo pipefail) runs and recovers the planted DTU genes - rc 0; alignment_info 6 TSVs + indexes; differential_asms.tsv 65 lines; adj p < 0.05: 25 genes, planted 20/20, 5 other (0.01: 23/20/3)
- [PASS] rMATS-long preprocessing failure is loud, not header-only tables - truncated BAM rc 1 (samtools error), header-only BAM rc 1 'empty or missing alignment_info/trt3.tsv', no output dir in either
- [FAIL] Annotation with the wrong contig names is reported in an actionable way - rc 1 but the message is a bare 'KeyError: ctrl1' from rmats-long; the block's own emptiness checks are never reached

My first launch of `t9_rmatslong.sh` used relative BAM paths after a `cd`, so cases (c) and (d) copied nothing and 'failed' for my reason; fixed to absolute paths and rerun before scoring.

---

## Input 6 - Adversarial: Unstranded ONT cDNA or unoriented HiFi: which minimap2 recipe, is -uf right?

**Prompt:** My library is ONT cDNA (unstranded), or maybe HiFi that never went through orientation fixing. Which minimap2 recipe, is -uf right, and how do I check?

**Ran:** `t1_uf.sh` (4 platforms, SKILL recipes with `--junc-bed`, with and without `-uf`, orientation awk verbatim), `t16_unoriented_hifi.sh`, `t23_real_dangle.sh` and `t5_real.sh` for the real check.

**Printed (trimmed):**
```
platform   ts:A:+   no -uf: exact / false-junc     -uf: exact / false-junc
hifi       1.000    91.5% / 0.0%                   91.5% / 0.0%
ontunstr   0.502    82.7% / 0.0%                   42.2% / 48.2%
ontstr     1.000    83.3% / 0.0%                   83.3% / 0.0%
drna       1.000    64.9% / 0.1%                   64.9% / 0.1%
HiFi made unoriented (p=0.5 reverse-complement): ts:A:+ 0.493 ; splice:hq 91.5% / 0.0% ; splice:hq -uf 62.9% / 30.5%
real LRGASP cDNA: ts:A:+ 0.503 (ONT recipe) / 0.498 (HiFi recipe)
```
**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100 ✅

**Assertions:**
- [PASS] Unstranded ONT cDNA with -uf yields the false junctions the SKILL reports; without -uf it does not - exact chains 42.2% vs 82.7%; false-junction reads 48.2% vs 0.0% (SKILL: 47%/50% vs 94%/1.1% on other reads)
- [PASS] Unoriented HiFi with splice:hq -uf shows ~29% false-junction reads - 30.5% with -uf (exact 62.9%), 0.0% without; orientation check 0.493
- [PASS] On oriented reads (HiFi, stranded ONT, direct RNA) -uf and no -uf give identical chains - hifi 91.5 = 91.5%, ontstr 83.3 = 83.3%, drna 64.9 = 64.9%
- [PASS] Orientation-check awk separates oriented from unoriented reads and works on real reads - planted hifi 1.000, ontunstr 0.502, ontstr 1.000; real LRGASP cDNA 0.503
- [PASS] -uf appears only for direct RNA in decision tree, recipes, usage-guide and example - grep of SKILL.md, usage-guide.md and the example: direct-RNA recipe and warnings only

---

## Input 7 - Edge: NEW: microexon recipe on my own 3-27 nt set, both directions, tandem pairs, real-read side effects

**Prompt:** NEW. I want microexon inclusion in neural samples. My alignment loses 3-27 nt exons: apply the Microexons recipe, check both isoforms, and tell me what breaks on real reads.

**Ran:** `gen_micro2.py` (12 single microexons 3, 5, 6, 8, 9, 11, 13, 16, 19, 22, 25, 27 nt + tandem T1 6+9 nt and T2 4+12 nt; 150 inclusion + 150 skipping reads per gene; hifi, ontunstr, drna at 7.2% and drnalow at 4% error; 5'/3' exon trimming), `t22_micro2_sweep.sh <platform>` (plain, `--junc-bed` at default, bonus 9, 12, 14-18, 20; `micro2_eval.py` two-way from CIGAR N; dangling count), `t26_snippet_check.sh` (the SKILL's pysam snippet verbatim), `t28_iq_micro2.sh` (IsoQuant on the plain and rescued BAMs), `t25_ultra_micro2.sh` + `t29_post_checks.sh` (uLTRA), `t23_real_dangle.sh` + `chain_diff.py` (real LRGASP cDNA and A549 dRNA at each bonus, `flair correct`), `t10_prior.sh` (the fixer's 10-nt set), `t31_srbed_micro2.sh` (unannotated route: SJ.out.tab -> the SKILL's awk -> 6-column BED, no annotation given to minimap2).

**Printed (trimmed):**
```
(inclusion mean % over 12 genes / skipping mean %; # genes below 90% in brackets)
HiFi   plain 58.2 / 100.0 [5 inc]   --junc-bed 99.9 / 100.0 [0]   b16 100.0 / 99.9 [0]   b17 100.0 / 99.9   b18 100.0 / 83.3 [2 skip]   b20 100.0 / 58.3 [5 skip]  (tandem b20: 100 / 0)
ONT    plain 16.4 / 96.6 [12]       --junc-bed 73.2 / 99.2 [4]    b14 96.1 / 99.2    b15 98.7   b16 99.6 / 99.2 [0]   b17 99.8   b20 99.8 / 82.2 [2 skip]
dRNA 7.2% err: plain 8.7 / 91.4 ; --junc-bed 67.5 / 94.9 ; b16 93.2 / 94.9 [4 inc <90: 3, 6, 19, 27 nt] ; b20 93.7 / 79.1 [3 skip]
dRNA 4% err  : plain 15.1 / 96.6 ; --junc-bed 72.7 / 99.2 ; b16 99.1 / 99.2 [0] ; b20 99.4 / 82.1 [2 skip]
dangling junctions (aligned reads 4200): 0 in every micro2 alignment
SKILL pysam snippet, HiFi M03 (6 nt): plain 0/300, --junc-bed 150/150, b16 150/150, b20 300/0 ; ONT M03: plain 0/284, b16 150/147, b20 297/0
IsoQuant (recipe alignment, truth 150/150): HiFi --junc-bed 149.0 / 148.6, tandem 150/150 ; ONT b16 148.2 / 148.2 ; plain HiFi 87.0 / 210.5, plain ONT 25.8 / 223.2
fixer's 10-nt set: plain 0/150 (skip 150), HiFi --junc-bed 150/150, ONT --junc-bed 131/150, ONT b20 150/150 (skip 150) - reproduces his table
SJ.out.tab -> awk -> --junc-bed (no annotation), HiFi default bonus 99.9 / 100.0 ; ONT b16 99.6 / 99.2 ; dRNA(4%) b16 99.1 / 99.2 ; dangling 0
uLTRA (annotation has the exon): HiFi inc 91.4 [3-nt 0%, T2 0/100] ; ONT 76.6 [6 genes < 90%: 3 nt 0%, 5 nt 53%, 8 nt 55%, 9 nt 71%] ; dRNA 78.6 ; skip >= 94.7 everywhere
REAL LRGASP cDNA (1883 reads), dangling / annotated-intron observations:  default 0 (97.5%), 12: 0, 14: 0, 15: 0, 16: 0 (97.7%), 17: 12, 18: 18, 20: 27
   flair correct: default 1691 corrected / 195 inconsistent, 15: 1682/204, 16: 1672/214 (rc 0); 17, 18, 20: rc 1 "Error: juncsToBed12 start/end"
   chain_diff default -> 16: 109 reads (5.8%) change chain, 109/109 to a fully annotated chain (97 already all-annotated, gaining an extra annotated intron); default -> 17: 129 (6.9%)
REAL A549 dRNA (129 reads): dangling 0 at every bonus; flair correct rc 0 (104 corrected / 25 inconsistent at 16-20 vs 103/26 default); 3 reads change chain at 16
```
**Scores:** Basic 32/40 | Specialized 50/60 | Total 82/100 ✅

**Assertions:**
- [PASS] HiFi --junc-bed alone and ONT --junc-bed --junc-bonus 16 keep both isoforms on an independent set (3-27 nt, two tandem pairs, 150+150 reads/gene) - HiFi juncbed inc 99.9 / skip 100.0 (min 98.7); ONT bonus16 inc 99.6 / skip 99.2 (min 97.3), tandem T1 100/99, T2 96/100; plain HiFi 58.2 / 100, plain ONT 16.4 / 96.6
- [PASS] The danger of a high bonus is real and the SKILL's check catches it: skipping reads recoded to inclusion - bonus 20 HiFi skip mean 58.3% (5/12 genes < 90%, tandem 0%), ONT 82.2%; the SKILL's pysam snippet verbatim: M03 HiFi plain 0/300, bonus 20 300/0 (SKILL example 0/399, 400/0)
- [PASS] Real ONT reads: bonus 16 leaves no intron next to a soft clip, 17+ does and flair correct fails - LRGASP 1883 reads: dangling 0 at default..16, 12 at 17, 18 at 18, 27 at 20; flair correct rc 0 at default/15/16, rc 1 'juncsToBed12 start/end' at 17, 18, 20
- [FAIL] Direct-RNA recipe reaches >=90% of inclusion reads for every size at bonus 16 - at 4% error 99.1% (min 96.0); at 7.2% error mean 93.2%, 4/12 genes < 90% (largest 27-nt exon 84.7%): the SKILL's 99% depends on the read error rate, which it does not state
- [FAIL] uLTRA with the exon in the annotation is an equivalent route - micro2: HiFi inc 91.4% (3-nt and 4+12 tandem 0%), ONT 76.6% (6/12 genes < 90%, worst 53%), dRNA 78.6%; the SKILL's 150/150 is one 10-nt exon

Reading: the recipe stands on independent data, in both directions, for 12 sizes and both tandem pairs, and the SKILL's own check snippet detects the failure mode it warns about. What did not generalise is uLTRA and the dRNA figure at high error. On real ONT reads the SKILL is right to choose 16, not 17.

---

## Input 8 - Edge: NEW: Kinnex array de-concatenation with skera, then lima and isoseq refine

**Prompt:** NEW. De-array my Kinnex (MAS-Iso-seq) HiFi reads with skera, then take the S-reads through lima and isoseq refine.

**Ran:** `mk_kinnex3.py` (24 ZMWs of a 6-fold array with seven adapters: the five printed on skera.how/adapters plus two random 16-mers; segments are Iso-Seq 5' primer + 150-2500 nt cDNA + polyA + rc 3' primer; 16 full arrays of which 8 are stored reverse-complemented, 4 with the last adapter missing, 4 with a middle adapter missing), `t24_kinnex.sh` (SKILL block verbatim with `as-pb` on PATH; `chk_kinnex3.py`), `t24c_isoseq.sh`, `t24b_lima.sh` (same array without the `zm` tag).

**Printed (trimmed):**
```
skera block rc=0 ; summary: Input Reads 24, S-Reads 132, mean length 1315, Percentage of Reads with Full Array 66.67, mean array size 5.5
kind                    expected / skera S-reads / equal to a planted segment
full                     96 /  96 /  96     (dl/dr tags (0,1) (1,2) ... (5,6))
last_adapter_missing     24 /  20 /  20     (the open final segment is not output)
middle_adapter_missing   20 /  16 /  16     (the fused segment is withheld)
lima --isoseq on 132 S-reads: 132 above all thresholds ; isoseq refine --require-polya: 132 flnc ; isoseq cluster2 rc 0 (0 transcripts, 132 distinct random cDNAs)
without the zm tag: skera names S-reads movie/?/ccs/16_1700 and lima --isoseq is killed by a 60-s timeout (rc 124)
skera.how/adapters: five adapters A-E and a link to downloads.pacbcloud.com (connection failed) ; file name mas16_primers.fasta not found
```
**Scores:** Basic 31/40 | Specialized 48/60 | Total 79/100 ✅

**Assertions:**
- [PASS] skera split block runs verbatim on a Kinnex array and returns the planted segments - 24 ZMWs: 16 full arrays -> 96 S-reads, 96/96 sequences equal planted segments (8 arrays stored reverse-complemented); dl/dr tags (0,1)...(5,6); total 132/132 output S-reads equal planted segments
- [PASS] skera withholds segments it cannot bound correctly - 4 arrays missing the last adapter: 20 of 24 (final open segment dropped); 4 arrays with a middle adapter missing: 16 of 20 (fused segment dropped); summary 'Percentage of Reads with Full Array 66.67'
- [PASS] lima --isoseq and isoseq refine run on the S-reads - with the zm tag: lima 132 in / 132 out, refine 132 flnc; without zm the S-read names are movie/?/ccs/... and lima hangs (killed at 60 s, rc 124)
- [FAIL] The SKILL's account of the lima stall is accurate and complete - it says 'on that toy BAM lima did not finish' without the cause (missing zm tag in the toy BAM) and still lists lima/isoseq as --help only
- [FAIL] The adapter file name in the block can be obtained from the source the SKILL names - skera.how/adapters shows only five sample adapters (A-E) and a link to downloads.pacbcloud.com, unreachable from here; 'mas16_primers.fasta' not verifiable

My first run of this input had no `zm` tag either and lima stalled exactly as the SKILL says; adding the tag is what made it work, so the SKILL's 'did not finish' is a property of the toy BAM. No real Kinnex data was available, so the claim that the chain works on real data is not tested.

---

## Other checks

- **Loadability of SKILL.md** (`t18_frontmatter.py`): YAML frontmatter parses (985-char description); 38,796 bytes, 580 lines, about 9.7k tokens; 28 code fences balanced (14 blocks); the 7 Related Skills all exist in the repo; neither SKILL.md nor usage-guide.md mentions `examples/`.
- **Blocks run**: 12 of 14 fenced blocks extracted by `extract_blocks.py` and run verbatim; `install_1.sh` only dry-run (package names resolve on conda-forge/bioconda and the one-line solve dry-runs, `t15_install_names.sh`; the search-output check there is weak); the ESPRESSO abundance-mode rMATS-long command not run (needs a user-supplied file).
- **Regression of the first re-auditor's microexon sets** (`t2_micro.sh`, `t3_microscan.sh`, regenerated by `gen_micro.py`): his table reproduces on regeneration (HiFi `--junc-bed` inclusion 200/200 at every size 4-21 nt with skipping 200/200; HiFi bonus 20 skipping 0/200 for the 5-nt and 10-nt genes; ONT/dRNA `--junc-bed` alone loses 4-8 nt exons (0-132/200 inclusion), bonus 20 rescues them but drops skipping to 188-198/200 in places). The SKILL's recipe (16, not 20) is the answer to exactly this. The uLTRA legs of `t2_micro.sh` were stopped after the HiFi leg (99.7% exact chains, 596/600 microexon inclusion; ONT/dRNA legs ran over 20 min under load); the uLTRA question is answered on my set by `t25`.
- **usage-guide.md**: prompts consistent with the SKILL (`-uf`, 10-nt microexon prompt).
- **Not executed**: real Kinnex data; lima/isoseq beyond my synthetic array; Bambu multicore on Linux; deSALT.
- **Auditor errors caught**: relative paths in my first `t9_rmatslong.sh`; `t11` inline planted-category check keyed wrongly (replaced by `sqanti_check.py`); SJ.out.tab generated after my first SR launch; toy Kinnex BAM without `zm` (informative, see input 8); my `t26` first argument parsing; CRLF in two copied scripts (`sed -i 's/\r$//'`).
- Nothing was written into `external\`, the worktree, `public-data\` or another audit's folder; no `__pycache__`; big intermediates (`run/out/` except the extracted blocks, `run/data/` except the small prior/regeneration inputs) were deleted before publishing.

## Recommendations

**P2** uLTRA offered as an equivalent microexon route (inputs [7]): Decision tree and 'Other routes' present uLTRA next to --junc-bed, backed by 150/150 on one 10-nt exon. On 14 microexon genes uLTRA lost 3-nt exons and the 4+12 tandem pair (0%), recovered 53-80% of 5-11 nt exons on ONT and dRNA (mean inclusion 76.6% ONT, 78.6% dRNA, 91.4% HiFi) against 99.6% for the recipe. Fix: State the per-size range measured (or say uLTRA is weaker below ~12 nt and on ONT/dRNA) and drop 'or uLTRA' from the decision-tree row.

**P2** flair diffSplice --test hides a failed event type (inputs [1]): On real 6-sample data alt5 has events but none survive DRIMSeq's filter: R prints '!No genes left after filtering!' with a traceback, FLAIR exits 0 and writes no drimseq_alt5 file. The text only says empty event types are skipped. Fix: Add one sentence: an event type can also fail with '!No genes left after filtering!' (rc stays 0); check that drimseq_<event>_*.tsv exists for every event type you need.

**P2** Microexon numbers depend on read error rate, which is not stated (inputs [7]): Bonus 16 gives 99.1% / 99.2% for direct RNA at ~4% error but 93.2% / 94.9% at 7.2% error (4/12 genes < 90%, including a 27-nt exon); the table gives one figure per platform. Also on real LRGASP cDNA bonus 16 changes the chain of 5.8% of reads (109/1883, all to fully annotated chains, flair correct inconsistent 195 -> 214), whereas the text says 'changed nothing outside microexons' (true only for its planted set). Fix: Name the simulated error rates next to the table and say that on real reads the bonus also extends some reads by an annotated intron.

**P2** Lima/isoseq status and adapter file name not verifiable (inputs [8]): The text says lima did not finish on the toy BAM and that lima/isoseq are help-only; with a zm tag on the toy BAM skera -> lima --isoseq -> isoseq refine all ran (132 -> 132 -> 132). 'mas16_primers.fasta' cannot be confirmed from skera.how/adapters. Fix: Say the toy BAM needed a zm tag, that skera -> lima -> refine ran on a synthetic array, and quote the file name only after fetching it.

**P2** SKILL.md 38.8 kB / 580 lines, no references/; example not referenced (inputs []): Evidence paragraphs grew the file from 33 kB; microexon section, DTU code and failure modes load together. Neither SKILL.md nor usage-guide.md mentions examples/longread_splicing_pipeline.sh. Fix: Move the microexon evidence and the DTU/rMATS-long blocks to references/, keep the recipe and the checks in SKILL.md, and link the example.

## Scripts (all in `run/`)

Data: `gen_planted.py`, `gen_micro.py`, `gen_sr.py`, `make_sj.py`, `prior_make_synth.py`, `prior_make_micro.py`, **`gen_micro2.py`**, **`mk_kinnex3.py`**. Checks: `eval_bam.py`, `eval_example.py`, `eval_diffsplice.py`, `eval_rmatslong.py`, `micro_table.py`, `micro2_eval.py`, `iq_micro2_score.py`, `iq_novel_check.py`, `iq_persample.py`, `pertx_check.py`, `sqanti_check.py`, `prior_junction_check.py`, `chain_diff.py`, `chk_kinnex3.py`, `real_conc.py`, `t18_frontmatter.py`. Blocks: `extract_blocks.py`. Runs: `par_example.sh`, `par_example_sj.sh`, `chain_a.sh`, `chain_b.sh`, `chain_c.sh`, `t0`-`t31` shell/R scripts, `build_report.py`, `viewer_details.py`, `build_viewer.py`, `validate_report.py`. Logs: `run/logs/`.
