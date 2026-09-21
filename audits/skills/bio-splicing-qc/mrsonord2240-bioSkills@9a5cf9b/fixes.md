# bio-splicing-qc - fix log

## 2026-09-20 (fixer, branch `fix/as-qc`, worktree `F:\OpenScience\wt\as-qc`)

First audit: 67, Reject, Research Veto M4 (code usability) fired, P0 open. Evidence: `F:\OpenScience\audits\bio-splicing-qc\`.
Checked on RSeQC 5.0.5, STAR 2.7.11b, samtools 1.24, pysam 0.24.1, pandas 2.3.3 / 2.x, maxentpy 0.0.2, Picard 3.5.0 (`af-picard3`), fastq_screen 0.16.0 + minimap2 2.31, SpliceAI 1.3.1, gffread 0.12.9 (WSL `as-core`, `as-maxent`, `as-spliceai`). Nothing installed anywhere (no new env, no `install.lock` use). Scratch (auditor's synthetic BAMs copied, real chrX GEUVADIS BAMs read-only from `public-data`, STAR re-run): `F:\OpenScience\as-qc-scratch`.

New shipped file: `examples/test_splicing_qc.py` (self-contained: builds a tiny BAM + BED12 with pysam, asserts; RSeQC checks skip if RSeQC is absent, MaxEnt checks skip if maxentpy is absent). Ran green in `as-core` (MaxEnt skipped) and `as-maxent` (RSeQC through the wrapper on PATH, MaxEnt run).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Known/novel snippet prints 0.0% / 0.0% (RSeQC writes `" annotated"` with a leading space) | P0 | SKILL.md snippet and `examples/splicing_qc.py::junction_annotation` strip the column and `assert known + novel == 1`; snippet explains the failure | ran: snippet verbatim on real chrX RSeQC output (known 99.5%, novel 0.5%); CLI on the audit's planted libraries reproduces 93.4% / 22.3% read-weighted (34.6% / 13.0% junction-level); test asserts 0.8 on a planted BAM | |
| junction_annotation / junction_saturation exit 1 without Rscript; Rscript unlisted | P0 | Every RSeQC call in SKILL.md carries `--skip-plot`; the helper adds it unless `plot=True` and Rscript is on PATH; "Before You Run Anything" states the requirement and the exact error; geneBody_coverage also `--skip-plot` | ran: `--rscript /nonexistent` gives `error: Rscript executable not found` rc=1 (reproduced); `--skip-plot` writes `.junction.xls` and `.junctionSaturation_plot.r`; helper with `--plot` and a PATH without Rscript succeeds and writes the tables | |
| `generate_qc_report` crashes on a BAM without spliced reads (EmptyDataError) | P0 | Helper raises `NoSplicedReadsError` with a message; `junction_stats` returns `{}`; Common Errors row for the raw pandas error | ran: RSeQC writes a 0-byte `.junction.xls` (reproduced); test asserts the clear error for annotation and `{}` / 0.0% for the pysam helper | |
| Overhang helper wrong for multi-junction reads; `count_junction_reads` ignores `min_overhang`, `=`/`X`, multi-mappers, mate double counting; unindexed BAM fails | P1 | One implementation, `junction_stats()`, in the example (the divergent inline copy in SKILL.md is replaced by a CLI call and a rules list): overhang = adjacent aligned block only, `min_overhang` honoured (`reads` vs `reads_all`), `=`/`X` handled, secondary/supplementary and NH>1 skipped, mates counted once, `fetch(until_eof=True)` so no index needed | ran: test on `30M1000N4M800N66M` (overhang 4 and 4, not 30), `20=1X29=500N50=` (junction at 5050-5550), NH=4 excluded, 5 pairs -> 5 fragments, unindexed BAM. Real chrX STAR pass-2 BAM vs `SJ.out.tab` (unique reads): equal on 2,765 of 2,765 shared junctions, 371 junctions with >=10 reads both; per-record counting equal on only 2,182 | Real-data rerun regenerated with STAR 2.7.11b (the audit's BAM was gone); numbers differ slightly from the audit's 2,792 |
| rRNA samtools recipe reads 15.6% for a planted 22.2% | P1 | `-F 0x904` on numerator and denominator, reason stated; Picard `PCT_RIBOSOMAL_BASES` named as alternative | ran: 8170 / 36756 = 22.2% (old recipe 8170 / 52282 = 15.6%) on the audit's `pe_rrna.bam` | |
| fastq_screen needs an unlisted aligner, exits 255 / silent 100% unmapped | P1 | Command uses `--aligner minimap2`; states default bowtie2, config `DATABASE` line, that minimap2 mode opens `<prefix>.fa.gz`, and how to read `*_screen.txt` | ran: literal command rc 255 (audit); config without the `.fa.gz` gives rc 0, 100% unmapped and only an `Aligner warning` in the log (reproduced); with the gzipped FASTA next to the `.mmi` rRNA 25.00% on the planted 25% set | bowtie2/bwa/bowtie not installed, not run |
| MaxEnt acceptor example `T*20+CAG` scores -7.20 | P1 | Example acceptor `TTTTTTTTTTTTTTCCTTAGGAG` (11.58) in SKILL.md and helper; the AG requirement stated; old string named as the -7.20 counterexample | ran: `score_splice_sites` prints `[10.86, 2.68] [11.58]` | |
| `score_splice_sites` drops wrong-length inputs, returns None for N (indices shift) | P1 | Returns one float per input, NaN for invalid; catches `SystemExit`/`KeyError`/`ValueError` | ran: test with `['CAGGTAAGT','CAGGTAA','NAGGTAAGT','CAGATAAGT']` -> `[10.86, nan, nan, 2.68]` | maxentpy raises `SystemExit("Wrong length of fa!")`, `KeyError` on N/U (documented now) |
| Failure mode "infer_experiment: 0 of 200000 reads / use -q 30" wrong | P1 | Replaced by observed messages `Total 0 usable reads were sampled` / `Unknown data type: Mixture` and their causes (contig mismatch, GTF given as BED, all reads below `-q`); `-q 30` stated as the default, `-q 0` for low-MAPQ aligners | ran: contig mismatch and GTF-as-BED both reproduce the messages (rc 0); audit: MAPQ-1 BAM `-q 0` gives 1.00 dUTP | |
| STAR `too many SJs in cohort merge` does not exist | P1 | Common Errors uses the real `Fatal LIMIT error ... re-run with at least --limitSjdbInsertNsj N` and the real `--sjdbOverhang` mismatch message | read from the audit's STAR logs (`lim.stdout`, `ovh.stdout`) | |
| `alignIntronMax` default "1 Mb" | P1 | 0 = window-derived max 2^16 x 9 = 589,824 nt (~590 kb) | `STAR --help` (winBinNbits 16, winAnchorDistNbins 9) | |
| `--alignSJoverhangMin 8` "for microexons" | P1 | Microexon rows deleted (see deletions); STAR flags kept at overhang 8 with the rationale (matches the >=8 nt anchor rule) | `STAR --help` (default 5, lower not higher) | chose delete over write: no runnable microexon tool installed |
| Flat saturation curve on deep BAM called uninformative; `samtools view -s` advice | P1 | Replaced: flat from the first steps = saturated; all zeros = no spliced reads / contig mismatch. Advice deleted | ran: planted deep library flat at 154 -> 180 by 10% (audit); mismatch gives all zeros rc 0 (reproduced) | |
| BED12 needed but never explained; BED6 silently gives 0% known | P1 | "Before You Run Anything": `gffread genes.gtf --bed \| cut -f1-12`; helper raises on non-BED12 | ran: gffread pipe gives 12 columns and RSeQC runs; BED6 makes every junction `complete_novel` (reproduced); test asserts the error | gffread 0.12.9 emits 13 columns; the extra one is harmless to RSeQC but cut anyway |
| RSeQC "annotated" semantics and read- vs junction-level known% undocumented | P1 | Definitions paragraph; snippet is read-weighted (thresholds use that), printed summary is junction-level; both returned by the helper | ran: 93.4% of reads vs 34.6% of junctions on the same planted BAM | |
| Merge filter `$5 > 0` is not a novelty filter; whole-line `sort -u` leaves duplicates | P2 | `awk '$6 == 0 && $5 > 0 && $7 >= 3' \| cut -f1-4 \| sort -u`; SJ.out.tab column key added | ran on the 4 real chrX pass-1 SJ.out.tab files: audit filter 5,717 lines / 2,184 distinct / 2,178 already annotated; new filter 6 novel junctions, none in the annotated set; pass 2 with the 4-column file (strand 1/2) ran, 97.67% unique | `--alignSJDBoverhangMin` set to STAR's default 3 in both passes (was 1 in pass 1 and 3 in pass 2, no rationale); pass 1 uses `--outSAMtype None` (only SJ.out.tab is used); `--twopassMode None` removed (default); re-ran pass 1 with the final flags (identical merged file) |
| STAR BAM has no XS tag (`--outSAMstrandField intronMotif` only in a comment); pysam helpers need an index | P2 | Flag added to pass 2 with its side effect (drops non-canonical unannotated reads); `samtools index` added | ran: 20,000 of 20,000 spliced reads have XS with the flag (0 of 20,000 without, audit) | |
| Veeneman 2016 "80-86% vs >=94% novel-junction recovery" and "loses ~14%" | P2 | Numbers deleted; citation reworded to what the paper reports (>=94% of simulated novel junctions had improved quantification, per-sample two-pass); cohort-vs-per-sample stated as STAR-manual rationale, not a figure | audit read the source; not re-fetched here | |
| Threshold tables inconsistent (30-50M vs 50-100M, 75 vs 100 nt, rRNA 1-3% vs <5%, "PE 50nt single-end") | P2 | One Quality Thresholds table for numeric general cut-offs, design targets in the design table, MaxEnt / rRNA / Picard cut-offs each in their own section; read-length and depth bands now contiguous; rRNA table rewritten (poly(A) >5% = degraded/poor selection; 1-3% row deleted); "PE 50nt single-end" pitfall gone with the Pitfalls section | read | `Junctions >=10 reads` cut-off relabelled "convention, depth-dependent" (was attributed to rMATS; unverified); 11% on a 50k-pair chrX sample |
| Saturation numbers unseeded and hard to read | P2 | Helper parses `x/y/z/w` from the `.r` file, applies the 80->100% rule; SKILL.md says the curve is stochastic and how `-l/-u/-s` refine it | ran: 3 repeats on one planted BAM, known at 15%: 51 / 63 / 67; growth 80->100% 4.0-5.3%; real chrX known curve 576 -> 2,698 (growth 6.9%, STILL RISING) | |
| Picard needs a refFlat that is never explained | found while verifying | awk BED12 -> refFlat recipe | ran: Picard 3.5.0 on the planted dUTP BAM with the awk refFlat: `PCT_CORRECT_STRAND_READS` 1.0, `MEDIAN_5PRIME_TO_3PRIME_BIAS` 1.009 (same as the auditor's) | `gtfToGenePred` is not installed here; GTF route not run |
| `MEDIAN_5PRIME_TO_3PRIME_BIAS` ">2 or <0.5 = severe degradation" | found while verifying (audit note) | <0.5 = 3' bias, >2 = 5' bias | audit: 3'-biased library 0.047, uniform 1.009 | |
| Strandedness output strings abbreviated as `++,--`; no advice for 70-90% | audit input 3 | Exact strings for PE and SE, leaky-library rule (report leakage; <0.7 treat as unstranded) | ran: SE `infer_experiment` prints `"++,--"` / `"+-,-+"`; audit: 20% / 40% leakage read 0.80 / 0.59 | leakage advice is a convention, stated as such |
| Research-use scope | brief rule | New "Scope" section; SpliceAI PP3/BP4 cut-offs kept as published references for prioritising sites, not for classifying a patient's variant | read | SpliceAI command added (`-I -O -R -A -D -M`), it was named without a runnable line: ran on the PLCXD1 donor G>A, `DS_DG 0.90 DS_DL 1.00` (audit values) |
| Redundancy (SKILL vs usage-guide; thresholds in 3 tables; Pitfalls section) | brief rule | see deletion list | read | |

Pass-1 re-run with the final SKILL.md flags (`--alignSJDBoverhangMin 3`, `--sjdbOverhang 149`, `--outSAMtype None`, all four chrX samples, rc 0): merged file is 6 lines and byte-identical (`cmp`) to the one from the earlier `--alignSJDBoverhangMin 1` run.

## Findings left unfixed

- **Veeneman 2016 wording not re-fetched** (the audit read the paper; no network fetch here).
- **Picard refFlat from a GTF** (`gtfToGenePred`) not run: tool absent; the BED12 route is verified.
- **fastq_screen with bowtie2 / bwa / bowtie** not run (not installed); only minimap2.
- **`junction_stats` memory on very deep BAMs** not measured; SKILL.md points to `SJ.out.tab` / regtools there.
- **Quality-threshold values** (read length, depth, MaxEnt cut-offs beyond the chrX check, Picard PCT_* bands, leakage advice) remain labelled conventions; only MaxEnt was checked against data.
- **Real-data checks are chrX only** (GRCh37, 50k pairs per sample), not a full-transcriptome GENCODE run.

## Deleted passages and where the content lives

| deleted (from) | now |
| --- | --- |
| usage-guide: Overview tool list, Prerequisites (pip/conda lines, reference files) | short Overview; install line in SKILL.md "Version Compatibility"; reference-file requirements (BED12) in "Before You Run Anything" |
| usage-guide: Quick Start prompt list (5 prompts) | merged into Example Prompts (one added: library checks) |
| usage-guide: "What the Agent Will Do" (6 steps) | SKILL.md section order |
| usage-guide: Tips (8 bullets: IR/rRNA depletion, 50 nt SE, cohort 2-pass, novel% biology, MaxEnt vs SpliceAI, basic vs comprehensive, strandedness, overhang) | Experimental Design Audit; STAR 2-Pass; Novel-vs-Known; Splice Site Strength; Annotation Choice; Strandedness; Junction Read Overhang |
| SKILL: taxonomy "Fails when" column and design-table numbers (<PE 75nt; n<3; <30M; 1-pass loses 14%) | Experimental Design Audit and Quality Thresholds (the "1-pass loses 14%" number is deleted, unverifiable) |
| SKILL: design-table rows Pairing kept, Annotation row, Microexons row | Annotation Choice; Microexons row deleted (VAST-TOOLS / `--alignSJoverhangMin 8` claim unbacked, no tool installed) |
| SKILL: decision-tree row "Are my microexons detectable?" and Troubleshooting row "Microexons missing" (VAST-TOOLS, MicroExonator) | deleted (unbacked mention: delete rather than write); `long-read-splicing` Related Skills text now says "complex isoforms" |
| SKILL: STAR approach comparison table (80-86% / >=94% recovery) and "STAR 2-pass: Per-Sample Inconsistency" failure mode | STAR 2-Pass Approach paragraph |
| SKILL: inline `junction_saturation.py` block plus 10-line subprocess loop over samples | one CLI line + helper in Junction Saturation |
| SKILL: "Junction Saturation: Subsampling Behavior" failure mode (deep BAM / samtools -s) | Junction Saturation last paragraph (corrected) |
| SKILL: inline `junction_stats` pysam function (wrong overhang) | `examples/splicing_qc.py::junction_stats` + rules list in Junction Read Overhang |
| SKILL: "Microexon-aware aligners use overhang as low as 6 nt" | deleted (unbacked) |
| SKILL: "Microbial / viral contamination" bullet under novel-junction biology | deleted (unbacked) |
| SKILL: SpliceAI TensorFlow Memory failure mode (`-D 50` "fastest", OOM) | deleted (unverified); SpliceAI command and checked output in Splice Site Strength |
| SKILL: `infer_experiment.py: Sample Size` failure mode | `infer_experiment.py: "0 usable reads"` (corrected) |
| SKILL: Common Errors rows `RSeQC: BED format error`, `regtools: invalid CIGAR`, `samtools view: missing index`, `MaxEntScan: invalid sequence character N`, `too many SJs` | rows with observed messages (Rscript, EmptyDataError, pysam ValueError, maxentpy SystemExit/KeyError, sjdbOverhang, limitSjdbInsertNsj); `regtools invalid CIGAR` deleted (never reproduced) |
| SKILL: Quality Thresholds rows for 2-pass STAR, 5'ss/3'ss MaxEnt, rRNA in depleted library | STAR 2-Pass; Splice Site Strength; rRNA Contamination Check |
| SKILL: Troubleshooting rows "FDR uncalibrated at low n (use leafcutter or Shiba; avoid SUPPA2 alone)" and "Sashimi plot mismatch (rMATS junction-imbalance, run Shiba)"; design-table "especially SUPPA2" | deleted (unverified tool-specific claims, outside QC) |
| SKILL: Troubleshooting "consider RNA-seq from secondary tissue" | deleted (unbacked) |
| SKILL: Common Pitfalls section (8 bullets) | STAR 2-Pass; Experimental Design Audit; Strandedness; Annotation Choice; Splice Site Strength (MaxEnt with SpliceAI); Novel-vs-Known |
| SKILL: description "STAR 2-pass cohort-style alignment ... MaxEntScan intrinsic + SpliceAI context-aware", "GENCODE" wording | shortened; still names the same layers, dropped "Splicing analysis is more demanding than DGE..." sentence that the body repeats |
| example `run_junction_saturation` / `run_junction_annotation` / `count_junction_reads` / `analyze_junction_coverage` | `junction_saturation`, `junction_annotation`, `junction_stats`, `summarize_junctions` (same jobs, corrected) |

## 2026-09-20 post-re-audit patch (orchestrator, commit after `9a5cf9b`)

Re-audit (85, Production Ready, no P0) found one P1 the fix introduced: the "-l/-u/-s for a finer 80-100% range" tip
gives wrong curves, because RSeQC samples correctly only when `-l` equals `-s`. `junction_saturation()` now raises
`ValueError` when `lo != step`; SKILL.md tip now says lower `-s` and keep `-l` equal to it. Test added
(`lo != step refused`), ran green in `as-core`. These bytes post-date the audit, so the Skill is promoted with
`reaudit: needed`.
