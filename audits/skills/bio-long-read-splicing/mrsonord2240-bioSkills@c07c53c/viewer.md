> **Audit record for `bio-long-read-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c07c53c](https://github.com/mrsonord2240/bioSkills/tree/c07c53cbf60daee254c6a0ab56a859f07acf8ddf/alternative-splicing/long-read-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-long-read-splicing (RE-AUDIT of the fixed Skill)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@c07c53cbf60daee254c6a0ab56a859f07acf8ddf:alternative-splicing/long-read-splicing` (branch fix/as-longread; read from the worktree, run from a copy in `run/skill_copy/`, sha1 of the three files identical to the worktree)
Pre-fix report (archived): `audits/_pre-fix-20260920/bio-long-read-splicing/` - 68, Reject, Research Veto M4 fired.
Category 3 Data Analysis, mode D (hybrid), Complex, N = 8. The fix log was read for orientation only; every number below is from my own runs (logs in `run/logs/`, scripts in `run/`).

**Result: static 75, execution average 82.9, final 80, Limited Release, deployable, no veto, no open P0, 2 open P1.**
Layer averages: L1 32.6/40, L2 50.2/60, assertions 32/39 (82%). Floors for Limited Release met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions >= 80%); Production Ready floors not met (exec < 85, assertions < 90%).

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical - FLAIR workflow, planted 3v3 + real LRGASP | 33 | 52 | 85 | 4/5 | ✅ |
| 2 | Variant A - IsoQuant + Bambu blocks | 32 | 49 | 81 | 4/5 | ✅ |
| 3 | Variant B - SQANTI3 classification/filter | 35 | 54 | 89 | 5/5 | ✅ |
| 4 | Stress - shipped example, hifi/ont/drna, clean copy | 35 | 54 | 89 | 5/5 | ✅ |
| 5 | Scope Boundary - DTU block, diffSplice --test, rMATS-long | 28 | 45 | 73 | 3/5 | ⚠️ |
| 6 | Adversarial - ambiguous library, -uf and orientation | 35 | 55 | 90 | 5/5 | ✅ |
| 7 | Edge (NEW) - microexon recipes with skipping-read control | 28 | 40 | 68 | 2/5 | ⚠️ |
| 8 | Edge (NEW) - unannotated splice sites, hybrid evidence | 35 | 53 | 88 | 4/4 | ✅ |

**Execution average 82.9 / 100.** All 8 inputs executed. Static 75 x 0.4 = 30.0; dynamic 82.9 x 0.6 = 49.7; 79.7 -> **80**.

Inputs 1-6 re-run the first audit's seven inputs as regression (Bambu and IsoQuant merged into input 2) but on data I generated myself; inputs 7 and 8 are new questions the fixer was never asked (skipping-read control on microexons, unannotated splice sites with three kinds of short-read help). Data: my own planted genome (seed 5150: 60 genes, 20 planted DTU, 7-nt and 12-nt annotated microexons, two unannotated isoforms, GENCODE-like GTF with valid CDS frames, UTR, start_codon rows; HiFi, ONT cDNA unstranded and stranded, ONT direct RNA), my own microexon sets (seeds 4242 and 4343, 4-24 nt, 200 inclusion + 200 skipping reads each), the first auditor's archived sets, and REAL LRGASP WTC-11 cDNA (1883 reads) and SG-NEx A549 direct RNA (129 reads, chr9 slice). Everything synthetic is regenerable from the generators in `run/` (checked: same md5 on regeneration).

## Research Veto, re-judged

| | Result | Evidence |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated identifiers or results; fixer's new measured numbers reproduce on independent data (below) |
| M2 Practice boundaries | PASS | tooling only |
| M3 Methodological baseline | PASS (P1 noted) | -uf guidance right and consistent; microexon `--junc-bonus 20` recipe lacks a skipping-read control (input 7) |
| M4 Code usability | PASS (borderline on one block) | shipped example ran end to end for hifi, ont, drna in 9 runs from a clean copy; 9 of the 11 SKILL.md code blocks extracted verbatim and run (the install line only dry-run, the skera block checked against `--help`); rMATS-long block lacks `mkdir alignment_info` (P1), no block needs rewriting |

## Regression: the first audit's findings

| Pre-fix finding | Now | How I know |
|---|---|---|
| P0 example aborts (isoquant.py, flair correct --genome, SQANTI3 --output dir, filter on IsoQuant GTF) | fixed | exit 0 x 9; content asserted (input 4) |
| P0 M4 FLAIR/IsoQuant commands rejected | fixed | FLAIR and IsoQuant blocks verbatim rc 0 (inputs 1, 2) |
| P1 -uf prescribed for unstranded cDNA (3 places) | fixed | grep: `-uf` only for dRNA/warnings; 48.2% false-junction reads measured (input 6) |
| P1 microexon "no aligner anchor problem" false | claim corrected, recipe partly wrong | input 7 |
| P1 DTU block cannot read FLAIR output | fixed | verbatim on FLAIR quantify output: 20/20 planted (input 5) |
| P1 FLAIR annotation-only correct drops novel sites, wrong remedy flag | fixed | 0/9 -> 9/9 with either flag (input 8) |
| P1 overstated "no quantification uncertainty", rMATS-long "GTF-only" contradiction | fixed | text checked; IsoQuant `__ambiguous` 87-426 reads per run |
| P2 SQANTI3 inputs/report | fixed | verbatim with CAGE/polyA from the SKILL's URLs (input 3) |
| P2 diffSplice prerequisites/outputs | fixed, `--test` verified | R half through the env's Windows R (input 1) |
| P2 unsourced thresholds, unrun single-cell block | partly | thresholds labelled; skera/isoseq `--help` only |
| P2 redundant usage-guide, monolithic SKILL.md | usage-guide done (nothing needed lost); monolith remains (546 lines, 33 kB) | diff against 44ff43b |

**Nothing the fix touched broke.** What it added and I could not confirm is the `--junc-bonus 20` microexon recipe (input 7).

---

## Input 1 - Canonical: bulk FLAIR workflow (correct -> collapse -> quantify -> diffSplice)

**Prompt:** "I have 3 v 3 PacBio HiFi Iso-Seq samples and a GENCODE-style annotation plus STAR junctions. Align, correct, collapse, quantify and test differential isoform usage with FLAIR." Also on real LRGASP cDNA reads.
**Ran:** `run/t8_flair6.sh` (six planted HiFi samples aligned with the SKILL recipe, merged into `aligned.bam`, `flair-workflow-*_1.sh` extracted VERBATIM by `extract_blocks.py`); `run/t5_real.sh` (real reads, same blocks, files named as the blocks expect); `run/t5b_diffsplice_test.sh` + `t5a_copy_diffsplice_R.sh` + `install_argparse.R` (R half of `--test`).
**Printed (trimmed):**
```
planted: Flair correct took 0:00:08 / collapse 0:00:06 / quantify 0:00:07
         corrected reads 49665, inconsistent 0, collapsed isoforms 124 (truth: 124 chains)
         counts.tsv: ids  ctrl1_ctrl_b0 ... trt3_trt_b0 ; G001A_G001 54 55 44 22 10 13
real:    align block rc=0; orientation check ont_cdna 0.503, isoseq recipe 0.498
         corrected 1691, inconsistent 195, collapsed isoforms 34; counts columns A1_A_b0 ... B3_B_b0
diffSplice --test in WSL as-lr: "FileNotFoundError: 'Rscript'" (documented prerequisite); event tables written
diffSplice_drimSeq.R via r.sh on the planted tables: 22 significant ES events, planted DTU genes 20/20, other genes 2 (G037, G042)
real 6-sample event tables: header-only DRIMSeq results (too few events); alt5 stops at dmFilter
```
**Scores:** Basic 33/40 | Specialized 52/60 | Total 85/100
**Assertions:**
- [PASS] block runs verbatim on real and planted data
- [PASS] 124/124 planted chains recovered (two unannotated ones need the `--junction_tab`, as the SKILL says)
- [PASS] `--test` R half recovers 20/20 planted DTU genes
- [PASS] orientation awk 0.503 on real reads
- [FAIL] `--test` prerequisites complete - also needs python (R argparse), data.table; FLAIR's script errors on empty alt3/ir tables

## Input 2 - Variant A: IsoQuant and Bambu

**Prompt:** "Discover and quantify isoforms from my HiFi samples with IsoQuant; then use Bambu with NDR 0.1."
**Ran:** `run/t6_isoquant.sh` (block verbatim, two FASTQ inputs, default prefix), `run/iq_persample.py`, `run/t19_denovo_novelsite.sh` (de novo), `run/t7a_bambu_bams.sh` + `t7c_bambu_run.sh` + `t7b_bambu_eval.R` (Bambu on 3 planted BAMs), `run/t13_bambu_real.R` (real A549 dRNA).
**Printed (trimmed):**
```
isoquant block rc=0 ; SKILL names: OUT.transcript_models.gtf EXISTS, OUT.transcript_counts.tsv EXISTS,
  OUT.transcript_grouped_file_name_counts.tsv EXISTS, OUT.transcript_model_counts.tsv MISSING
per-sample vs truth: ctrl1 r 0.9988 (G001A 54=54, G001B 14=14), trt1 r 0.9987 (G001A 22=22)
de novo (no --genedb): 121 models, 121/124 truth chains, G057N and G058N both found
Bambu block verbatim (ncore = 8), Windows R: "Error: BiocParallel errors ... could not find function 'seqlengths'"
Bambu ncore = 1: ctrl1 r 0.9992, ctrl2 0.9989, ctrl3 0.9990; novel transcripts 0 ("NDR approximated" warning, as SKILL says)
real A549: 105 transcripts, total count 88 (11 with count > 0), no novel; R segfaults at exit after "Finished running Bambu"
```
**Scores:** Basic 32/40 | Specialized 49/60 | Total 81/100
**Assertions:** [PASS] IsoQuant verbatim; [PASS] per-sample counts equal truth; [FAIL] listed output name `transcript_model_counts.tsv` is not written by 4.0.0; [PASS] Bambu counts match truth and NDR caveat holds (with ncore = 1; `ncore = 8` as written fails on Windows R - P2); [PASS] de novo mode works.

## Input 3 - Variant B: SQANTI3

**Prompt:** "Classify my collapsed isoforms with SQANTI3 with CAGE and polyA support and filter artifacts."
**Ran:** `run/t0_download_support.sh` (the SKILL's Magdoll/images_public URLs: 200), `run/t11_sqanti_real.sh` (block verbatim on the 34 real FLAIR isoforms; then on the planted FLAIR isoforms), `run/sqanti_check.py`, `run/t10c_sqanti_prior.sh` (first auditor's 10 query isoforms), `run/t17_filter_needs_awk.sh`.
**Printed (trimmed):**
```
real:    rc=0 ; 34 rows {FSM 8, ISM 19, antisense 5, NIC 1, genic 1}; within_CAGE_peak TRUE 7 / FALSE 27; polyA_motif_found TRUE 17 / FALSE 17; filter pass 30, filtered.gtf 151 lines
planted: 124 isoforms {FSM 122, NIC 1, NNC 1}; G057N novel_in_catalog (combination_of_known_splicesites); G058N novel_not_in_catalog (at_least_one_novel_splicesite); 122/122 annotated = FSM
first auditor's set: 10/10 (Q07 is genic_intron, the correct SQANTI3 label for an exon inside an intron; the old truth said "genic")
full IsoQuant GTF into sqanti3_filter.py: AssertionError (raw[2] == 'transcript'), filtered GTF 0 lines; awk-filtered: 673 lines
```
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 - all 5 assertions PASS (see JSON).

## Input 4 - Stress: the shipped example, end to end, from a clean copy

**Prompt:** "Run examples/longread_splicing_pipeline.sh on my HiFi / ONT cDNA / direct RNA sample."
**Ran:** `run/t4_example.sh <hifi|ont|drna> [sj]` (verbatim copy under `run/skill_copy/examples/`, inputs overridden through the environment variables the script documents), `run/t4b_eval.sh` + `run/eval_example.py` (pysam chains, IsoQuant/FLAIR counts vs truth by exact intron chain, SQANTI3 categories, filter output), `run/t10_prior.sh` (first auditor's reads + his `junction_check.py`), `run/t12_realdrna.sh` + `t12b_real_conc.sh` (real A549 dRNA).
A first attempt failed inside SQANTI3 (gtfToGenePred: "conflicting frame") - a bug in MY generator (all CDS frames 0), not in the Skill; fixed in `gen_planted.py` (reads unchanged, same md5) and rerun.
**Printed (trimmed):**
```
                     hifi        ont (unstranded)   drna
exit code            0           0                  0
exact chains         91.5%       82.7%              64.9%      (5'-truncated reads: consistent 100 / 99.7 / 99.3%)
false-junction reads 0.0%        0.0%               0.1%
FLAIR r vs truth     0.9996      0.9990             0.9935
IsoQuant r vs truth  0.9987      0.9950             0.9778     (__ambiguous 87 / 165 / 426)
SQANTI3 (IsoQuant models) FSM 122 + NIC 1 in all three; filter: 123 pass, filtered GTF 673 lines
with SR_JUNCTIONS: FLAIR unannotated +30-nt isoform 0/9 -> 9/9 (hifi), 9/9 (ont), 10/10 (drna); IsoQuant 0 (merged)
first auditor's reads: PLATFORM=hifi exact 95.6%, ont 96.0%, 0 false junctions, filter 6 pass / 29 lines
real A549 dRNA (129 reads): exit 0; 114 spliced; 5 IsoQuant models (52 exon, 50 CDS rows), 28 reads counted + 54 ambiguous; FLAIR 9 isoforms; SQANTI3 5 FSM; filter 5 pass, 57 lines
```
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 - 5/5 PASS. The example file is mode 644 (run with `bash`, as its header says).

## Input 5 - Scope Boundary: differential isoform analysis

**Prompt:** "Test differential isoform usage between my 3 v 3 long-read groups: DTU with DRIMSeq/stageR, FLAIR diffSplice, and rMATS-long."
**Ran:** `run/t9b_run_dtu.sh` + `t9_dtu.R` (block sourced VERBATIM from `out/blocks/`), `run/t5b_diffsplice_test.sh` + `eval_diffsplice.py`, `run/t8_flair6.sh` (rMATS-long block verbatim), `run/t8b_rmatslong_fixed.sh` + `eval_rmatslong.py`.
**Printed (trimmed):**
```
DTU block on FLAIR counts (planted): genes tested 60 (planted 20/20 tested); stage-wise significant 22; planted recovered 20/20; other genes: G037, G042
DTU block on real LRGASP counts: runs to the end; dtu is NULL ("No genes were found to be significant on a 5% OFDR level")
diffSplice --test R half: ES events tested 22, 20/20 planted, 2 extra (same G037, G042)
rMATS-long block AS WRITTEN: 6 x FileNotFoundError: 'alignment_info/ctrlN.tsv' (simplify_alignment_info.py); later commands still run;
   rmats_long_output/*.tsv are header-only (coeff.tsv 40 bytes, differential_asms.tsv 39 bytes)
same block + "mkdir -p alignment_info": 64 ASMs; adj p < 0.05 -> 25 genes, planted 20/20, other 5 (0.01: 23 / 20 / 3);
   the abundance-based alternative in the block stops at 'abundance.esp' (user-supplied ESPRESSO file, expected)
```
**Scores:** Basic 28/40 | Specialized 45/60 | Total 73/100 - ⚠️. Assertions: [PASS] DTU 20/20; [PASS] diffSplice --test 20/20; [FAIL] rMATS-long block runs as written; [PASS] recovers 20/20 once the directory exists; [FAIL] failed preprocessing is not silent (empty tables, no error). The first audit's harness had pre-created the directory, which is why this was missed.

## Input 6 - Adversarial: "unstranded ONT cDNA - which minimap2 recipe, is -uf right?"

**Prompt:** "My library is ONT cDNA (unstranded) - or maybe HiFi that never went through orientation fixing. Which minimap2 recipe, and how do I check?"
**Ran:** `run/t1_uf.sh` (4 platforms, SKILL recipes with `--junc-bed`, with and without `-uf`, orientation awk copied verbatim), `run/t16_unoriented_hifi.sh`, `run/t12b_real_conc.sh`, and `t5_real.sh` for the real check.
**Printed:**
```
platform   orientation ts:+   no -uf: exact / false-junc     -uf: exact / false-junc
hifi       1.000              91.5% / 0.0%                   91.5% / 0.0%
ontunstr   0.502              82.7% / 0.0%                   42.2% / 48.2%
ontstr     1.000              83.3% / 0.0%                   83.3% / 0.0%
drna       1.000              64.9% / 0.1%                   64.9% / 0.1%
HiFi made unoriented (p=0.5 reverse-complement): ts:+ 0.493; splice:hq 91.5% / 0.0%; splice:hq -uf 62.9% / 30.5%
real LRGASP cDNA: ts:+ 0.503 (ONT recipe) / 0.498 (isoseq recipe); junction observations on annotated introns 97.5% without -uf, 57.1% with
```
`-uf` appears only for direct RNA in the body, decision tree, usage-guide prompt and example.
**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100 - 5/5 PASS. The SKILL's figures (47-50%, 29%, 0.501, 0.503, 92% -> 54-59%) all reproduce.

## Input 7 - Edge (NEW): does a 4-24 nt microexon survive?

**Prompt:** "Confirm microexon inclusion in neural samples. My HiFi/ONT alignment loses a 7-nt exon - apply the Microexons recipe."
**Ran:** `run/gen_micro.py` (main set 7/12/24 nt; scan set 4,5,6,8,10,15,18,21 nt; 200 inclusion + 200 skip reads each), `run/t2_micro.sh`, `run/t3_microscan.sh`, `run/t3b_microskip.sh`, `run/t10_prior.sh` (fixer's 10-nt set), `run/t21_desalt.sh`, `micro_table.py` (inclusion kept = both flanking junctions in the CIGAR; skip exact = exact skip chain).
**Printed (inclusion kept / skip exact, out of 200; scan set sizes MX1..MX8 = 4,5,6,8,10,15,18,21 nt):**
```
HiFi plain            inc 0 0 0 0 199 200 200 200      skip 200 all
HiFi --junc-bed       inc 200 all sizes                 skip 200 all
HiFi --junc-bed +bonus20  inc 200 all                   skip 0 0 200 200 0 200 200 200    <- skipping reads recoded as inclusion
ONT plain             inc 0 0 0 0 0 0 0 149             (24 nt main set: 132)
ONT --junc-bed        inc 0 0 0 132 193 198 200 200     skip 200 all
ONT --junc-bed +bonus20   inc 200 all                   skip 0 194 200 200 198 200 200 200
dRNA --junc-bed       inc 0 0 0 86 175 194 199 200
dRNA +bonus20         inc 200 all                       skip 0 188 200 200 196 200 200 200
main set 7/12/24 nt, HiFi: plain inc 0/200, 200, 200; --junc-bed all 200 with skip 200; +bonus20 skip 0/200 for the 7-nt gene; noexon annotation +bonus20: 7-nt inc 0/200
main set ONT: --junc-bed inc 0/200 (7 nt), 198, 200; +bonus20 inc 200/200/200, skip 200/197/200; 6-col BED (SKILL awk on SJ.out.tab) same as +bonus20
uLTRA + annotation: HiFi inc 196/200/200; ONT 146/200/198; dRNA 122/198/199; skip >= 191 everywhere
deSALT (no annotation): inclusion 0/200 at every size
fixer's own 10-nt chrM set: plain 0/150; --junc-bed 150 (HiFi) / 131 (ONT); +bonus20 150 / 150 with skip 150/150 (reproduces his table exactly)
```
**Scores:** Basic 28/40 | Specialized 40/60 | Total 68/100 - ⚠️. Assertions: [FAIL] "plain minimap2 drops microexons" (HiFi keeps >= 10 nt, ONT loses more); [PASS] `--junc-bed` rescue on HiFi with skip control; [FAIL] `--junc-bed` alone rescues ONT/dRNA (nothing below about 8 nt); [FAIL] `--junc-bonus 20` leaves skipping reads intact; [PASS] SKILL awk BED and uLTRA rescue inclusion.
The fixer's table is honest for his one 10-nt sequence; the hazard needs a second sequence and a skipping-read control to appear. Mechanism, not proven here: two annotated-junction bonuses (2 x 20) outweigh the mismatch cost of squeezing a short exon into a read that lacks it.

## Input 8 - Edge (NEW): unannotated splice sites with short-read evidence

**Prompt:** "Two isoforms are missing from my annotation: an exon skip and a donor 30 nt into the intron. Recover them."
**Ran:** `run/t20_junction_bed.sh` (flair correct: annotation only / `--junction_bed` from the SKILL awk / `--junction_tab`), `run/t19_denovo_novelsite.sh`, `run/t6_isoquant.sh` + `gen_sr.py` + `iq_novel_check.py` (short reads aligned with `minimap2 -ax splice:sr`, `--illumina_bam`).
**Printed:**
```
flair correct annotation only:  G057N 40/40 kept, G058N 0/9 (9 inconsistent)
flair correct --junction_bed:   G058N 9/9, inconsistent 0
flair correct --junction_tab:   G058N 9/9, inconsistent 0
alignments (--junc-bed annotation): G057N exact 37/40 (HiFi), 21/29 (ONT); G058N exact 8/9 on both -> --junc-bed does not block novel junctions
IsoQuant annotation-guided: G057N model found (37 reads); G058N no model, with or without --illumina_bam (125,055 short reads, 40,278 spliced)
IsoQuant de novo: 121 models, 121/124 truth chains incl. G058N
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100 - 4/4 PASS. (IsoQuant `--illumina_bam` showed no effect here; the SKILL does not claim one. De novo finding the shifted isoform is not mentioned in the SKILL.)

---

## Other checks

- **Loadability of the 33 kB SKILL.md:** `run/t18_frontmatter.py` - YAML frontmatter parses (985-char description), 546 lines, about 8.3k tokens, 22 code fences balanced, all 7 Related Skills exist in the repo. Usable, but above the 500-line guideline with no `references/`.
- **usage-guide.md dedup:** diffed against 44ff43b. Every removed item is in SKILL.md (Install section, Platform matrix, decision tree, failure modes, IsoQuant/Bambu/SQANTI3/DTU sections). The recursive-splicing prompt is gone but the topic stays in the "When Long-Read Wins" table. Nothing needed was lost.
- **Install line:** package names exist on conda-forge/bioconda; dry-run of the one-line install solves (`run/t15_install_names.sh`).
- **skera / lima / isoseq:** `run/t14_pb_help.sh` (env as-pb, help only): `skera split <input> <adapters.fasta> <output>` matches the SKILL's block; `isoseq refine`, `isoseq cluster2` exist. No Kinnex data, not run.
- **Not executed:** Kinnex commands beyond `--help`; IsoQuant `--illumina_bam` beyond the planted set; uLTRA and deSALT beyond the planted microexons; rMATS-long only on planted data; Bambu block only with `ncore = 1` (as written it fails on this Windows R).
- **Auditor bug caught:** `eval_example.py` first double-counted IsoQuant reads (transcript_counts plus discovered_transcript_counts) and my first SQANTI3 novel-isoform check keyed on the wrong id; both fixed before scoring (`sqanti_check.py`). The `t10_prior.sh` SQANTI3 leg (c) had a broken `sed` on its first run; its fixed copy is `t10c_sqanti_prior.sh` (log `t10c_...`).
- Nothing was written into `external\`, the worktree, `public-data\` or another audit's folder; no `__pycache__` anywhere (checked with `find`). Big intermediates (real-data genome copy, FASTQs, BAMs, R private lib) were deleted; `run/out/blocks/` (the extracted verbatim blocks) is kept.

## Recommendations

**P1** Microexon `--junc-bonus 20` rescue flips skipping reads to inclusion (input 7): add the skipping-read control, recommend `--junc-bed` alone for HiFi and bonus/uLTRA for ONT/dRNA only with the control, make the "plain minimap2 drops it" row platform- and size-specific.
**P1** rMATS-long block omits `mkdir -p alignment_info` and fails silently downstream (input 5): add the mkdir, `set -euo pipefail` and a check that the per-sample TSVs exist.
**P2** IsoQuant output list names `transcript_model_counts.tsv`, absent in 4.0.0 (input 2).
**P2** Bambu `ncore = 8` fails on Windows R (input 2).
**P2** `flair diffSplice --test` prerequisites incomplete: python, data.table; empty event tables abort FLAIR's R script (inputs 1, 5).
**P2** SKILL.md 546 lines / 33 kB, no `references/`.
**P2** Common Errors rows for ssw-py, kallisto, prepareAnnotations, skera remain unverified; thresholds unsourced.

## Scripts (all in `run/`)

Data: `gen_planted.py`, `gen_micro.py` (main and scan sets), `gen_sr.py`, `make_sj.py`. Checks: `eval_bam.py`, `micro_table.py`, `pertx_check.py`, `eval_example.py`, `eval_rmatslong.py`, `eval_diffsplice.py`, `iq_novel_check.py`, `iq_persample.py`, `sqanti_check.py`, `real_conc.py`, `t18_frontmatter.py`, `prior_junction_check.py` (the first auditor's, copied from the archive for the regression leg). Blocks: `extract_blocks.py`. Runs: `t0`-`t21` shell/R scripts (order: t0, extract_blocks, t1, t2, t3, t3b, t4, t4b, t5, t5a, t5b, t6, t7a-c, t8, t8b, t9, t9b, t10, t10c, t11, t12, t12b, t13, t14-t21), `install_argparse.R` (argparse + findpython into a private library under `run/out/`, no change to the shared R-lib), `build_report.py` (JSON + schema checklist). Logs: `run/logs/`.
