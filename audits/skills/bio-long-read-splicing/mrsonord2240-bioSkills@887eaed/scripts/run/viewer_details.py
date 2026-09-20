#!/usr/bin/env python3
"""Per-input run details for the eval viewer (numbers copied from run/logs). Writes viewer_details.json; RO = real-ONT example log text read from logs/t27_example_realont.log."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
RO = open(os.path.join(HERE, "logs", "t27_example_realont.log"), encoding="utf-8", errors="replace").read().strip()
D = {}
D["intro"] = """Inputs 1-6 re-run the previous audits' inputs as regression tests, on data I regenerated from the first re-auditor's generators (`gen_planted.py`, `gen_micro.py`; same md5 on regeneration) and the first auditor's (`prior_make_*.py`), plus real reads. Inputs 7 and 8 are new and use generators of my own (`gen_micro2.py`, seed 9191, GC 0.58, 12 microexon sizes 3-27 nt plus two tandem pairs; `mk_kinnex3.py`, a 6-fold Kinnex array with reversed and defective arrays), so the score does not only measure what the fixers were told about. Input 7 also carries the real-read consequences of the bonus setting."""
D["regression"] = """| Round-1 re-audit finding | Now | How I know |
|---|---|---|
| P1 microexon `--junc-bonus 20` flips skipping reads to inclusion | fixed | recipe is HiFi `--junc-bed` alone, ONT/dRNA bonus 16; on my set bonus 20 gives HiFi skipping 58.3%, bonus 16 99.9% (input 7) |
| P1 rMATS-long block lacks `mkdir alignment_info`, silent empty tables | fixed | block verbatim rc 0, 20/20; truncated / header-only BAM rc 1 (input 5) |
| P2 IsoQuant `transcript_model_counts.tsv` named | fixed | file list checked (input 2) |
| P2 Bambu `ncore = 8` on Windows | fixed (documented) | fails as documented, `ncore = 1` runs (input 2) |
| P2 `flair diffSplice --test` prerequisites | fixed, one gap | verified 20/20 with as-lr-drim; an event type with no genes after DRIMSeq's filter fails silently (input 1) |
| P2 unverified Common Errors rows | fixed | `prepareAnnotations` row reproduced on an empty and a 6-column GTF (`t30`) |
| P2 monolithic SKILL.md | not fixed, worse | 38.8 kB, 580 lines (33 kB / 546 before) |

**What round 2 introduced:** nothing that breaks a recipe. The `--junc-bonus 16` choice is the right one (17 crashes `flair correct` on real ONT reads, reproduced). Small things: uLTRA overgeneralised, `--test` gap, an error-rate dependence not stated, the lima explanation, the file grew."""
D["inputs"] = {}
D["inputs"]["1"] = dict(prompt="I have 3 v 3 PacBio HiFi Iso-Seq samples, a GENCODE-style annotation and STAR junctions. Align, correct, collapse, quantify and test differential isoform usage with FLAIR (also on real ONT cDNA).",
 ran="`t8_flair6.sh` (six planted HiFi samples aligned with the SKILL recipe, merged BAM, the FLAIR block extracted verbatim by `extract_blocks.py` and run with an `Rscript` wrapper for env `as-lr-drim` first on PATH), `t5_real.sh` (real LRGASP reads; alignment block, orientation awk and FLAIR block verbatim), `eval_diffsplice.py`.",
 printed="""planted: rc=0; Flair correct 0:00:12 / collapse 0:00:09 / quantify 0:00:11 / diffsplice 0:00:59
         corrected reads 49665, inconsistent 0, collapsed isoforms 124 (truth 124 chains)
         counts.tsv: ids  ctrl1_ctrl_b0 ... trt3_trt_b0 ; G001A_G001 54 55 44 22 10 13
         alt3 / ir: "event matrix file empty, not running DRIMSeq"
         eval_diffsplice: ES events in quant table 63 ; tested by DRIMSeq 22 ; planted DTU genes recovered 20/20 ; other genes ['G037', 'G042']
real:    align block rc=0 ; ts:A:+ ont_cdna 0.503, isoseq recipe 0.498 ; FLAIR block rc=0
         corrected 1672, inconsistent 214, isoforms 33 ; drimseq_alt3/es/ir written
         alt5: "!No genes left after filtering!" + R traceback, FLAIR rc 0, no drimseq_alt5 file""")
D["inputs"]["2"] = dict(prompt="Discover and quantify isoforms from my HiFi samples with IsoQuant, then use Bambu with NDR 0.1.",
 ran="`t6_isoquant.sh` (block verbatim on two planted FASTQ files, default prefix; then `--illumina_bam` with 125,055 simulated short reads, `gen_sr.py`, `iq_novel_check.py`), `t19_denovo_novelsite.sh`, `t7a_bambu_bams.sh` + `t7c_bambu_run.sh` + `t7b_bambu_eval.R` (Windows R via `r-bambu.sh`), `t13_bambu_real.R` (real A549 dRNA).",
 printed="""isoquant block rc=0 ; OUT.transcript_models.gtf / transcript_counts.tsv / transcript_grouped_file_name_counts.tsv EXIST ; transcript_model_counts.tsv MISSING (not claimed any more)
grouped file header: gene_id sample1.fastq sample2.fastq ; G001A 54 22 ; G001B 14 44   (ctrl1 truth 54/14)
--illumina_bam: no illumina: G057N 37 reads, G058N no model ; with illumina: identical
de novo (no --genedb) on the example HiFi BAM: 121 models, 121/124 truth chains, G057N and G058N found
Bambu block verbatim (ncore = 8): "BiocParallel errors ... could not find function seqlengths", exit 1
Bambu ncore = 1: 122 transcripts x 3 samples; r vs truth 0.9992 / 0.9989 / 0.9990 ; novel transcripts 0 ("NDR approximated" warning)
real A549 dRNA (129 reads): 105 transcripts, total count 88 (11 with count > 0), 0 novel ; R segfaults at exit (rc 139) after 'Finished running Bambu'""",
 after="Note: R exiting with a segfault after Bambu finishes is the machine's Windows-R/xgboost combination (TOOLS.md item 12), not the Skill's; the Skill does not mention it.")
D["inputs"]["3"] = dict(prompt="Classify my collapsed isoforms with SQANTI3 including CAGE and polyA support and filter artifacts.",
 ran="`t0_download_support.sh` (the SKILL's Magdoll/images_public URLs: 4,811,158-byte CAGE BED.gz and the polyA list, HTTP 200), `t11_sqanti_real.sh` (block verbatim on real FLAIR `isoforms.gtf`, then on the planted FLAIR isoforms), `sqanti_check.py` (id-safe check), `t10_prior.sh` (first auditor's 10 query isoforms), `t17_filter_needs_awk.sh`.",
 printed="""real: rc=0 ; 33 isoforms {FSM 8, ISM 18, antisense 5, NIC 1, genic 1} ; within_CAGE_peak TRUE 7 / FALSE 26 ; polyA_motif_found TRUE 17 / FALSE 16 ; filter pass 29, filtered.gtf 143 lines
planted (sqanti_check.py): 124 isoforms {FSM 122, NIC 1, NNC 1}; annotated -> FSM 122/122
   G057N novel_in_catalog (combination_of_known_splicesites) ; G058N novel_not_in_catalog (at_least_one_novel_splicesite)
first auditor's 10 isoforms: 9/10 by his labels (Q07 genic_intron; his truth said genic) ; filter 10 pass, 44 GTF lines
full IsoQuant GTF into sqanti3_filter.py rules: rc=1 AssertionError""",
 after="My first planted check (inline python in `t11`) keyed isoform ids wrongly and printed `None` for the novel ones; `sqanti_check.py` (id-safe, from the previous audit) is the check I score on.")
D["inputs"]["4"] = dict(prompt="Run the shipped examples/longread_splicing_pipeline.sh on my HiFi / ONT cDNA / direct RNA sample (and on real reads).",
 ran="`par_example.sh`, `par_example_sj.sh` -> `t4_example.sh <hifi|ont|drna> [sj]` (verbatim copy under `run/skill_copy/examples/`, inputs overridden through the environment variables its header documents), `t4b_eval.sh` + `eval_example.py` (pysam chains, IsoQuant/FLAIR counts vs truth by exact intron chain, SQANTI3 categories, filter output), `t10_prior.sh` (first auditor's reads + `prior_junction_check.py`), `t12_realdrna.sh` (real A549 dRNA), `t27_example_realont.sh` (real LRGASP cDNA, without and with SR_JUNCTIONS). The first SR_JUNCTIONS launch failed because `data/plant/SJ.out.tab` had not been made yet (my step order, fixed with `make_sj.py`).",
 printed="""                      hifi        ont (unstranded)   drna
exit code             0           0                  0          (also with SR_JUNCTIONS: 0 / 0 / 0)
exact chains          91.5%       82.8%              65.2%      (5'-truncated reads: consistent 100 / 99.9 / 99.8%)
false-junction reads  0.0%        0.0%               0.0%
"Reads with an intron next to a soft clip": 0 in every run ; ts:A:+ 1.000 / 0.502
FLAIR r vs truth      0.9996      0.9990             0.9935     IsoQuant 0.9987 / 0.9956 / 0.9817 (__ambiguous 87 / 165 / 426)
IsoQuant models 123 = 123 truth chains ; SQANTI3 FSM 122 + NIC 1 (G057N) in all three ; filter 123 pass, filtered GTF 673 lines
+SR_JUNCTIONS: FLAIR G058N 0/9 -> 9/9 (hifi), 9/9 (ont), 10/10 (drna) ; IsoQuant G058N still no model
first auditor's reads: PLATFORM=hifi exact 95.6%, ont 96.0%, 0 false junctions, filter 6 pass / 29 lines
real A549 dRNA (129 reads): exit 0 ; 114 spliced ; IsoQuant 6 models (61 CDS rows kept by the awk step) 29 reads counted + 54 ambiguous ; FLAIR 10 isoforms ; SQANTI3 6 FSM ; filter 6 pass, 70 lines
""" + RO)
D["inputs"]["5"] = dict(prompt="Test differential isoform usage between my 3 v 3 long-read groups: DTU with DRIMSeq/stageR, FLAIR diffSplice, and rMATS-long.",
 ran="`t9_dtu.R` (the DTU block sourced verbatim; Windows R via `r.sh`) on the planted FLAIR output and on the real 6-sample output, `t9_rmatslong.sh` (block verbatim on 6 planted BAMs plus three failure paths), `eval_rmatslong.py`.",
 printed="""DTU on planted FLAIR counts: genes tested 60 (planted 20/20 tested); stage-wise significant 22; planted 20/20; other G037, G042
DTU on real LRGASP counts: runs to the end; "No genes were found to be significant on a 5% OFDR level"; dtu NULL
rMATS-long (a) planted 3v3: rc=0; samples.tsv 6 rows; alignment_info 6 TSV + index; differential_asms.tsv 65 lines, differential_isoforms.tsv 131 lines
   ASM rows 64 genes 60 ; adj p < 0.05: 25 genes, planted DTU 20/20, other 5 ; < 0.01: 23 / 20 / 3
(b) truncated BAM: rc=1, "[E::bgzf_read_block] ... samtools view: error reading file ctrl2.bam", no output dir
(c) header-only BAM: rc=1, "empty or missing alignment_info/trt3.tsv", no output dir
(d) contig names differ (chrQ vs Q): rc=1, "KeyError: 'ctrl1'" (rmats-long), no result tables""",
 after="My first launch of `t9_rmatslong.sh` used relative BAM paths after a `cd`, so cases (c) and (d) copied nothing and 'failed' for my reason; fixed to absolute paths and rerun before scoring.")
D["inputs"]["6"] = dict(prompt="My library is ONT cDNA (unstranded), or maybe HiFi that never went through orientation fixing. Which minimap2 recipe, is -uf right, and how do I check?",
 ran="`t1_uf.sh` (4 platforms, SKILL recipes with `--junc-bed`, with and without `-uf`, orientation awk verbatim), `t16_unoriented_hifi.sh`, `t23_real_dangle.sh` and `t5_real.sh` for the real check.",
 printed="""platform   ts:A:+   no -uf: exact / false-junc     -uf: exact / false-junc
hifi       1.000    91.5% / 0.0%                   91.5% / 0.0%
ontunstr   0.502    82.7% / 0.0%                   42.2% / 48.2%
ontstr     1.000    83.3% / 0.0%                   83.3% / 0.0%
drna       1.000    64.9% / 0.1%                   64.9% / 0.1%
HiFi made unoriented (p=0.5 reverse-complement): ts:A:+ 0.493 ; splice:hq 91.5% / 0.0% ; splice:hq -uf 62.9% / 30.5%
real LRGASP cDNA: ts:A:+ 0.503 (ONT recipe) / 0.498 (HiFi recipe)""")
D["inputs"]["7"] = dict(prompt="NEW. I want microexon inclusion in neural samples. My alignment loses 3-27 nt exons: apply the Microexons recipe, check both isoforms, and tell me what breaks on real reads.",
 ran="`gen_micro2.py` (12 single microexons 3, 5, 6, 8, 9, 11, 13, 16, 19, 22, 25, 27 nt + tandem T1 6+9 nt and T2 4+12 nt; 150 inclusion + 150 skipping reads per gene; hifi, ontunstr, drna at 7.2% and drnalow at 4% error; 5'/3' exon trimming), `t22_micro2_sweep.sh <platform>` (plain, `--junc-bed` at default, bonus 9, 12, 14-18, 20; `micro2_eval.py` two-way from CIGAR N; dangling count), `t26_snippet_check.sh` (the SKILL's pysam snippet verbatim), `t28_iq_micro2.sh` (IsoQuant on the plain and rescued BAMs), `t25_ultra_micro2.sh` + `t29_post_checks.sh` (uLTRA), `t23_real_dangle.sh` + `chain_diff.py` (real LRGASP cDNA and A549 dRNA at each bonus, `flair correct`), `t10_prior.sh` (the fixer's 10-nt set), `t31_srbed_micro2.sh` (unannotated route: SJ.out.tab -> the SKILL's awk -> 6-column BED, no annotation given to minimap2).",
 printed="""(inclusion mean % over 12 genes / skipping mean %; # genes below 90% in brackets)
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
REAL A549 dRNA (129 reads): dangling 0 at every bonus; flair correct rc 0 (104 corrected / 25 inconsistent at 16-20 vs 103/26 default); 3 reads change chain at 16""",
 after="Reading: the recipe stands on independent data, in both directions, for 12 sizes and both tandem pairs, and the SKILL's own check snippet detects the failure mode it warns about. What did not generalise is uLTRA and the dRNA figure at high error. On real ONT reads the SKILL is right to choose 16, not 17.")
D["inputs"]["8"] = dict(prompt="NEW. De-array my Kinnex (MAS-Iso-seq) HiFi reads with skera, then take the S-reads through lima and isoseq refine.",
 ran="`mk_kinnex3.py` (24 ZMWs of a 6-fold array with seven adapters: the five printed on skera.how/adapters plus two random 16-mers; segments are Iso-Seq 5' primer + 150-2500 nt cDNA + polyA + rc 3' primer; 16 full arrays of which 8 are stored reverse-complemented, 4 with the last adapter missing, 4 with a middle adapter missing), `t24_kinnex.sh` (SKILL block verbatim with `as-pb` on PATH; `chk_kinnex3.py`), `t24c_isoseq.sh`, `t24b_lima.sh` (same array without the `zm` tag).",
 printed="""skera block rc=0 ; summary: Input Reads 24, S-Reads 132, mean length 1315, Percentage of Reads with Full Array 66.67, mean array size 5.5
kind                    expected / skera S-reads / equal to a planted segment
full                     96 /  96 /  96     (dl/dr tags (0,1) (1,2) ... (5,6))
last_adapter_missing     24 /  20 /  20     (the open final segment is not output)
middle_adapter_missing   20 /  16 /  16     (the fused segment is withheld)
lima --isoseq on 132 S-reads: 132 above all thresholds ; isoseq refine --require-polya: 132 flnc ; isoseq cluster2 rc 0 (0 transcripts, 132 distinct random cDNAs)
without the zm tag: skera names S-reads movie/?/ccs/16_1700 and lima --isoseq is killed by a 60-s timeout (rc 124)
skera.how/adapters: five adapters A-E and a link to downloads.pacbcloud.com (connection failed) ; file name mas16_primers.fasta not found""",
 after="My first run of this input had no `zm` tag either and lima stalled exactly as the SKILL says; adding the tag is what made it work, so the SKILL's 'did not finish' is a property of the toy BAM. No real Kinnex data was available, so the claim that the chain works on real data is not tested.")
D["other"] = """- **Loadability of SKILL.md** (`t18_frontmatter.py`): YAML frontmatter parses (985-char description); 38,796 bytes, 580 lines, about 9.7k tokens; 28 code fences balanced (14 blocks); the 7 Related Skills all exist in the repo; neither SKILL.md nor usage-guide.md mentions `examples/`.
- **Blocks run**: 12 of 14 fenced blocks extracted by `extract_blocks.py` and run verbatim; `install_1.sh` only dry-run (package names resolve on conda-forge/bioconda and the one-line solve dry-runs, `t15_install_names.sh`; the search-output check there is weak); the ESPRESSO abundance-mode rMATS-long command not run (needs a user-supplied file).
- **Regression of the first re-auditor's microexon sets** (`t2_micro.sh`, `t3_microscan.sh`, regenerated by `gen_micro.py`): his table reproduces on regeneration (HiFi `--junc-bed` inclusion 200/200 at every size 4-21 nt with skipping 200/200; HiFi bonus 20 skipping 0/200 for the 5-nt and 10-nt genes; ONT/dRNA `--junc-bed` alone loses 4-8 nt exons (0-132/200 inclusion), bonus 20 rescues them but drops skipping to 188-198/200 in places). The SKILL's recipe (16, not 20) is the answer to exactly this. The uLTRA legs of `t2_micro.sh` were stopped after the HiFi leg (99.7% exact chains, 596/600 microexon inclusion; ONT/dRNA legs ran over 20 min under load); the uLTRA question is answered on my set by `t25`.
- **usage-guide.md**: prompts consistent with the SKILL (`-uf`, 10-nt microexon prompt).
- **Not executed**: real Kinnex data; lima/isoseq beyond my synthetic array; Bambu multicore on Linux; deSALT.
- **Auditor errors caught**: relative paths in my first `t9_rmatslong.sh`; `t11` inline planted-category check keyed wrongly (replaced by `sqanti_check.py`); SJ.out.tab generated after my first SR launch; toy Kinnex BAM without `zm` (informative, see input 8); my `t26` first argument parsing; CRLF in two copied scripts (`sed -i 's/\\r$//'`).
- Nothing was written into `external\\`, the worktree, `public-data\\` or another audit's folder; no `__pycache__`; big intermediates (`run/out/` except the extracted blocks, `run/data/` except the small prior/regeneration inputs) were deleted before publishing."""
D["scripts"] = """Data: `gen_planted.py`, `gen_micro.py`, `gen_sr.py`, `make_sj.py`, `prior_make_synth.py`, `prior_make_micro.py`, **`gen_micro2.py`**, **`mk_kinnex3.py`**. Checks: `eval_bam.py`, `eval_example.py`, `eval_diffsplice.py`, `eval_rmatslong.py`, `micro_table.py`, `micro2_eval.py`, `iq_micro2_score.py`, `iq_novel_check.py`, `iq_persample.py`, `pertx_check.py`, `sqanti_check.py`, `prior_junction_check.py`, `chain_diff.py`, `chk_kinnex3.py`, `real_conc.py`, `t18_frontmatter.py`. Blocks: `extract_blocks.py`. Runs: `par_example.sh`, `par_example_sj.sh`, `chain_a.sh`, `chain_b.sh`, `chain_c.sh`, `t0`-`t31` shell/R scripts, `build_report.py`, `viewer_details.py`, `build_viewer.py`, `validate_report.py`. Logs: `run/logs/`."""
json.dump(D, open(os.path.join(HERE, "viewer_details.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("details written")
