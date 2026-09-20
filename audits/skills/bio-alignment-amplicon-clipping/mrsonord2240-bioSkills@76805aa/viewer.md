> **Audit record for `bio-alignment-amplicon-clipping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@76805aa](https://github.com/mrsonord2240/bioSkills/tree/76805aaab9347c8022c25df34c533cc3abd0b898/alignment-files/alignment-amplicon-clipping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-amplicon-clipping (RE-AUDIT of the fixed Skill)
Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@76805aaab9347c8022c25df34c533cc3abd0b898:alignment-files/alignment-amplicon-clipping` (branch `fix/af-ampclip`) | pre-fix report: 68, Beta Only (`_pre-fix-20260920`)

Category: Data Analysis | Mode: B (CLI + shipped example + shipped checker) | Complexity: Complex, N=7 | Executed: **7/7**
Tools: samtools 1.24, bcftools 1.24, pysam 0.24.1, iVar 1.4.4, minimap2 2.31, fgbio 4.1.1 (side env), WSL `science` env `alignment-files`.
Data: real nf-core ARTIC v5.3.2 nanopore BAM (4916 reads) + `v5.3.2.primer.bed` + `MN908947.3.fasta`; real nf-core Illumina PE BAM (MT192765.1); ARTIC v3.0.0 BED. SYNTHETIC (labelled): 800-read PE amplicon panel, 8 single-read strand cases, 21 tolerance reads, 900-read HiFi-like 16S set, planted-residual BAMs.
The Skill was copied to `run/skill` (md5 of all four files equals the commit) and every script ran from copies; nothing was written under `external\` or the worktree. Scripts and logs: `run/*.sh|py`, `run/logs/`, text outputs `run/out/`. Big intermediate BAMs were deleted.

## Result

**Final 85 / 100 (85.4), grade Limited Release after the assertion floor, deployable: true, no veto, no P0, 1 P1, 5 P2.** Pre-fix 68 Beta Only.
Static 85 x 0.4 = 34.0; execution average 85.6 x 0.6 = 51.4. Floors (scoring_rubric section 5): static 85 ok, execution 85.6 ok, Layer 1 avg 34.4 ok, Layer 2 avg 51.1 ok, **assertions 29/35 = 82.9 % < 90 %** so the grade drops one tier from Production Ready. The numeric score is exactly 85, so the orchestrator's "core >= 85, deployable, no P0, no veto" landing test is met.

## Step 1 — Skill Veto

| | | |
|---|---|---|
| T1 Stability | PASS | Every documented block, the shipped example and the checker ran on real and synthetic data; failures are non-zero exits by design |
| T2 Contract | PASS | `name`, `description` present; all 4 shipped files exist; all Related Skills paths exist in the worktree (incl. `read-qc/quality-reports`) |
| T3 Determinism | PASS | Example on real ARTIC: identical record md5 `38df635d7d5b` at THREADS=4/1/4 |
| T4 Security | PASS | No eval/exec, quoted variables, `mktemp -d` + trap, no credentials; `CLIP_OPTS` is intentionally a flag string |

## Step 2 — Static (25 criteria) = 85 / 100

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 10/12 | Complete, and every mode/strand number reproduces. Left: stale BAQ comment in example, iVar "needs indexed" overstated, `--tolerance` wording, wrong-BED detection over-attributed to checker |
| Reliability | 8/12 | Loud failures on the pre-fix traps; misleading messages for track-header / space-delimited BED; residual check silently skipped without pysam; output BAM left after late failure |
| Performance/Context | 7/8 | SKILL 202 lines + 39-line usage-guide (was duplicated) |
| Agent Usability | 15/16 | Measured tables, a verify step; small inconsistencies (comment vs SKILL, checker exit-code docs) |
| Human Usability | 7/8 | Natural prompts; strict BED validation fine, wrong cause named in some rejections |
| Security | 11/12 | Safe scripting |
| Maintainability | 10/12 | Clean file split, independent checker; no shipped test data/expected output |
| Agent-Specific | 17/20 | Precise trigger, idempotent, stop conditions; no handoff for low-yield/NTC or wrong BED |

## Step 3 — Classification

Data Analysis, Mode B. Complexity Complex (4 shipped files, many task types: four clip modes, BED formats, tag repair, verify, iVar alternative, markdup rationale, long-read rule) so N=7 inputs: 5 regressions of the pre-fix inputs, 2 new.

## Step 4 — Inputs

1. (Canonical, regression) "I have the ARTIC v5.3.2 nanopore BAM aligned to MN908947.3 and the v5.3.2 primer BED. Trim the primers, repair the tags and give me an indexed BAM ready for consensus, and check no primer bases remain."
2. (Variant A, regression) "Paired-end amplicon panel BAM with primer BED and reference: run the example workflow and tell me whether VAF under the primers is fixed; what if I use --strand only?" (synthetic, planted SNPs)
3. (Edge, regression) "Which of --strand / --both-ends do I need? My BED came from UCSC with a track line / is space-delimited; what does --tolerance do?" (synthetic single reads)
4. (Variant B, regression) "Hard-clipped archive copy, iVar alternative, IUPAC consensus, and does BAQ need MD?" (synthetic PE + real ARTIC)
5. (Adversarial, regression) "Here is my Illumina BAM (MT192765.1) and the ARTIC BED; also a wrong FASTA, name-sorted input, a sparse sample. Run your example." + false-positive probes.
6. (Stress, NEW) "PacBio HiFi full-length 16S amplicons with 27F/1492R primers: trim them." (synthetic HiFi-like)
7. (Scope Boundary, NEW) "Does your residual checker actually catch leftover primers, and a wrong scheme version?" (planted + real)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (real ARTIC) | 36 | 55 | 91 | 5/5 | yes | ✅ |
| 2 | Variant A (synthetic PE + example) | 36 | 55 | 91 | 5/5 | yes | ✅ |
| 3 | Edge (strand table, BED, tolerance) | 34 | 49 | 83 | 3/5 | yes | ✅ |
| 4 | Variant B (tools, hard clip, BAQ) | 34 | 51 | 85 | 4/5 | yes | ✅ |
| 5 | Adversarial (mismatches, false positives) | 34 | 50 | 84 | 4/5 | yes | ✅ |
| 6 | Stress (HiFi-like, NEW) | 35 | 53 | 88 | 5/5 | yes | ✅ |
| 7 | Scope Boundary (checker, wrong BED, NEW) | 32 | 45 | 77 | 3/5 | yes | ✅ |

**Execution Average: 85.6 / 100. Assertion pass rate: 29/35 (82.9 %).**

## Detailed Outputs

### Input 1 — Canonical, real ARTIC v5.3.2 nanopore BAM
Code: `run/s1_extract_blocks.py` pulls the fenced bash blocks out of SKILL.md; `s1_real_artic.sh` copies the real data under the block's own names (`input.bam primers.bed reference.fa`) and runs `basic_ampliconclip_workflow_1.sh` **verbatim**; `s1_oracle.py`, `s1_indep_residual.py`, `s1b_modes_ivar.sh`, `s1c_example_real.sh` are the cross-checks.
Printed (workflow block, rc 0):
```
MN908947.3                      <- step 0 contig intersection
TOTAL READS: 4916  TOTAL CLIPPED: 9617  FORWARD CLIPPED: 4817  REVERSE CLIPPED: 4800  BOTH CLIPPED: 4708  NOT CLIPPED: 7  WRITTEN: 4916
4916 / 4916                     <- mapped reads / reads with MD
mapped reads=4916  5' end inside a primer=0 (0.0%)  3' end inside a primer=0 (0.0%)
```
Oracle (BED only): `left ok 4817, right ok 4800, bad 0`; MD/NM vs independent recompute over 4916 reads: 0 / 0 mismatches; raw output NM on 7 reads (the unclipped ones), MD 0.
Mode table reproduced (checker and independent count agree): default 97.5 %, `--strand` 97.5 %, `--both-ends` 0 %, `--both-ends --strand` 0 % 3' residual; TOTAL CLIPPED 4834 / 4824 / 9644 / 9617; NOT CLIPPED 82 / 92 / 7 / 7. `--clipped` writes 4909, `--strand --clipped` 4824, `--fail` 7 QCFAIL, `--original` OA on 4909, `--keep-tag` NM 4916 (raw default output 7), `--primer-counts` 194 lines, raw header `SO:unknown` and `samtools index` fails. `--tolerance 0/5/20` identical (7 NOT CLIPPED).
iVar block verbatim: `Trimmed primers from 99.86% (4909)`; 4909 records, 4701 identical (name,flag,pos,cigar) to `ampliconclip --both-ends --strand --clipped`, residual 5' 93 (1.9 %), 3' 79 (1.6 %); defaults: `Minimum Read Length ... 205`, 0 records written; `-e` writes 4916.
Shipped example (default): rc 0, `records mapped=4916 with MD=4916`, residual 0/0; `CLIP_OPTS=--strand` rc 0 with `3' end inside a primer=4793 (97.5%) (3' not enforced)`; THREADS 4/1/4 md5 identical; checker 0.22 s.
Scores: Basic 36/40 (FC 9, RC 9, Eff 9, S&S 9); Specialized 55/60 (method 18, code 14, QC 9, repro 9, security 5).
Assertions: 5/5 PASS (see JSON).

### Input 2 — Variant A, synthetic PE panel through the shipped example (SYNTHETIC)
Code: `make_synth.py` (regenerated, md5 identical to pre-fix data), `s2_synth.sh`, `s2_check.py`. Four amplicons (one 80 bp), 25-base primers, SNPs at 310 and 335 under primers (primer bases carry REF).
Printed: eight runs (default, `--strand`, `--both-ends`, `--both-ends --strand`, `--strand --hard-clip`, example default / `--strand` / `--both-ends`): every line `clip-truth ok=800 bad=0 | MPOS bad=0 TLEN bad=0 MC wrong=0 ms missing=0 | MD/NM wrong=0`; allele counts pos310 `{T:100,C:100}` -> `{T:100}`, pos335 `{A:100,G:100}` -> `{G:100}`. Example `--strand`: `3' end inside a primer=200 (25.0%) (3' not enforced)` (the Skill's "200/800"); unclipped BAM through the checker: rc 1, `5' end inside a primer=800 (100.0%)`. `samtools markdup -s`: `DUPLICATE PAIR: 710`.
Scores: Basic 36, Specialized 55 = 91. Assertions 5/5.

### Input 3 — Edge, strand table, BED formats, tolerance (SYNTHETIC)
Code: `s3a_strand_cases_make.py`, `s3_strand_bed.sh`, `s3_table_assert.py`, `s3_tol_make.py`.
Printed: **`SKILL table cells: 16 match, 0 mismatch (of 16)`** (each row/mode typed from SKILL.md and compared to samtools 1.24 output). 5-column BED with `--strand`: `Parsed 5 columns, but need at least 6`, rc 1; example rc 1 `ERROR: --strand needs the strand in BED column 6 ...` before clipping. BED variants through samtools vs the example:
```
variant           samtools --both-ends --strand   example
tab / comment / blank / CRLF   TOTAL CLIPPED: 1000     rc 0
space-delimited                TOTAL CLIPPED: 1000     rc 1 "no contig shared by BAM header (amp1) and BED (amp1 100 125 A1_LEFT 60 +,...)"
track header line              TOTAL CLIPPED: 1000     rc 1 "--strand needs the strand in BED column 6 ... 5-column BED is rejected"
```
`--tolerance` (fwd 60-bp reads at primer start + d, primer [300,325)): tol 0 clips d>=0 (including d=+12 inside the primer), tol 5 clips d>=-5, tol 10 clips d>=-8 (the tested minimum): N only extends the match upstream of the primer start.
Scores: Basic 34, Specialized 49 = 83. Assertions 3/5 (BED-variant handling and tolerance wording FAIL).

### Input 4 — Variant B, tools and removed claims (SYNTHETIC + real)
Code: `s4_tools.sh`, `s4_check.py`.
Printed: Quick Reference hard-clip line `TOTAL CLIPPED: 1000`; piped repair line rc `0 0 0 0`; `orig mean SEQ len 94.89, hard 64.07, H reads 800`; soft-clip SEQ byte-identical 800 of 800; consensus unclipped `...GYGG...GARA...` (Y/R) vs soft `...GTGG...GAGA...` (T/G); truth scoring `hard 800 (100 %)`, `soft 800`, `iVar 800`, ClipBam fixed-25 control 632 (79 %); `ClipBam --help lines mentioning bed/primer/amplicon: 0 (of 101)`; pointers: `samtools mpileup -aa -A -d 600000 -B` ok, `bcftools mpileup -aa` -> `Could not parse tag "a"`, `--max-depth 600000 -a FORMAT/AD,FORMAT/DP -B` ok; BAQ: `clipped_final.bam` and `noMD.bam` give identical VCF bodies (md5 377ccda153 / ed659a15fa with `-B`), 32,150 records each. (An earlier md5 differed only because it included the `#CHROM` header line naming the file; fixed in the script.)
Left over: `examples/ampliconclip_workflow.sh` line 62 still claims bcftools BAQ depends on MD/NM.
Scores: Basic 34, Specialized 51 = 85. Assertions 4/5.

### Input 5 — Adversarial, regressions and false-positive probes
Code: `s5_adversarial.sh`. Each case runs the shipped example from a copy.
```
F1 Illumina BAM + ARTIC BED      rc 1  ERROR: no contig shared by BAM header (MT192765.1) and BED (MN908947.3)   no output BAM  (pre-fix: rc 0)
F2 wrong FASTA                   rc 1  ERROR: reference FASTA lacks contig(s) the BAM and BED use: MN908947.3    no output BAM  (pre-fix: rc 0)
F2b pre-check deleted            rc 1  [bam_fillmd] fail to find sequence ... | ERROR: calmd wrote no MD tags     BAM left behind
F3 name-sorted input             rc 0, 4916 records (works; prerequisite not enforced)
F4 no .fai                       rc 1  ERROR: index the reference first: samtools faidx nofai.fa
P1 multi-contig BAM/FASTA, P2 FASTA lacking unused contig, P3 BED with extra contig, P5 real Illumina PE + renamed BED (both option sets): rc 0
P4 sparse sample (1 primer-free read): rc 1  ERROR: ampliconclip clipped nothing: BED coordinates do not match the reads
```
Scores: Basic 34, Specialized 50 = 84. Assertions 4/5 (failed run leaves output BAM; sparse sample message).

### Input 6 — Stress, HiFi-like 16S (NEW, SYNTHETIC)
Code: `s6_make_hifi.py` (3 contigs 1489-1521 bp, 900 reads, 0.10 % substitution / 0.03 % indel errors, 50/50 orientation, 5 % 1-3 bp end jitter, 5 % 25-40 bp deep truncation), `s6_hifi.sh`, `s6_check.py`; alignment `minimap2 -ax map-hifi`.
Printed: 900/900 mapped, mean length 1502.9; workflow block rc 0, `NOT CLIPPED: 0`, residual 0/0. Modes: default/`--strand` 3' residual 883 (98.1 %), checker rc 1; `--both-ends` and `--both-ends --strand` 0, rc 0 (independent count agrees). Planted truth: `{'reads': 900, 'left ok': 900, 'right ok': 900}` for both the workflow output and the shipped example. iVar (`-q 0 -m 1`): `Trimmed primers from 100% (900)`, residual 0/0. Hard clip: H on 900 reads.
Judgement on PacBio HiFi (not tested by the fixer): the Skill's rule (`--both-ends --strand` when reads can reach the opposite primer) holds on HiFi-like reads, and the example works unchanged. Limits: synthetic reads; real HiFi heteropolymer indels, degenerate primers and multi-primer barcoding are not modelled, and the Skill's own "measured" wording correctly covers ONT only.
Scores: Basic 35, Specialized 53 = 88. Assertions 5/5.

### Input 7 — Scope Boundary, residual checker and wrong-scheme BED (NEW)
Code: `s7_run.sh`, `s7_checker_tests.py`, `s7_plant.py`, `s7b_wrong_scheme.sh`, `s8_misc_claims.sh`.
Checker unit cases (synthetic, planted): 17 of 17 detection/boundary cases as expected (start 300 and 324 flagged, 325 clean; reverse read end at 340 flagged, 325 clean; 3' residual only enforced with `--three-prime`; soft/hard-clipped primers, off-contig reads and wrong-strand primers not flagged; unmapped-only BAM rc 2). One residual planted in a real clipped BAM (read start moved 3 bp into a primer): `5' end inside a primer=1`, rc 1; clean clipped BAM rc 0; unclipped real BAM `98.1 % / 97.5 %`, rc 1. 98,320 reads in 2.3 s.
Not met: bad-input exits are 1 (5-col BED via `sys.exit(msg)`, missing BED/BAM traceback), the docstring says 2; false-negative probe (read starting 3 bp upstream of a primer and running through it) is not flagged (ampliconclip would clip it within `--tolerance`, so this only matters if clipping was skipped).
Wrong BED through the shipped example on the real v5.3.2 BAM:
```
CONTROL v5.3.2 BED            rc 0  TOTAL CLIPPED 9617  NOT CLIPPED 7
W1 v3.0.0 BED, default        rc 1  TOTAL CLIPPED 480   NOT CLIPPED 4445   (only because 1 read's 3' end hit a primer)
W2 v5.3.2 shifted +9 bp       rc 0  TOTAL CLIPPED 5141  NOT CLIPPED 122
W3 v3.0.0, CLIP_OPTS=--strand rc 0  TOTAL CLIPPED 224   NOT CLIPPED 4692
```
Judged against the correct BED the wrong-scheme output has 97.4 % / 96.7 % residual. Also: calmd with a wrong-contig FASTA exits 0 and writes no MD (message `Reference MN908947.3 not found in FASTA file`, then `[bam_fillmd] fail to find sequence`), iVar 1.4.4 trimmed an unindexed BAM.
Scores: Basic 32, Specialized 45 = 77. Assertions 3/5.

## Research Veto (Data Analysis)

- Scientific Integrity: PASS — every measured figure in the Skill reproduced; citations correct.
- Practice Boundaries: PASS — no diagnostic or prescriptive content.
- Methodological Ground: PASS — clip-mode guidance now matches samtools 1.24; the wrong-BED gap is P1, not a fallacy.
- Code Usability: PASS — all blocks, the example and the checker ran (7/7 inputs).

## Step 8 — Final

Static 85 x 0.4 = 34.0; execution 85.6 x 0.6 = 51.4; **85.4, rounded 85; assertion floor 82.9 % < 90 % -> one tier down: Limited Release ✅, deployable true, veto_override false.**

### What the fix changed, as measured (pre-fix 68 -> 85)
Fixed and verified by my own runs: silent success on mismatched inputs (F1/F2 now rc 1), inverted `--strand`/`--both-ends` claims (16/16 table cells + 4 mode rows reproduce), 5-column BED example, ClipBam/BAMClipper listings, `--strand` leaving 97.5 % of ARTIC 3' primers (default now `--both-ends --strand`, residual 0), unsorted/unclipped/tag notes, usage-guide dedup (nothing lost: each of its prompts is answered in SKILL.md), invalid `-aa` bcftools pointer, BAQ claim in SKILL.md. New residual defects: below.

### Recommendations
- [P1] Wrong primer BED passes the example silently and the checker is credited with catching it (Input 7) — assert NOT CLIPPED share from `clip.stats`; drop the "other scheme version" cause from the checker row.
- [P2] Refuted BAQ/MD claim survives in `examples/ampliconclip_workflow.sh` line 62 (Input 4).
- [P2] Example rejects samtools-valid BEDs (track header, space-delimited) with the wrong message; 5-col BED without `--strand` fails late as "primer bases remain" (Input 3).
- [P2] `check_primer_residual.py` bad-input exit code is 1 not 2; pysam-missing skip exits 0 (Input 7).
- [P2] Failed example run leaves an output BAM; sparse/NTC sample gets a misleading stop (Input 5).
- [P2] iVar "needs indexed" and `--tolerance` wording (Inputs 1, 3).

## Tooling notes
`ampliconclip` tolerance semantics, wrong-BED behaviour and HiFi results are on samtools 1.24 / iVar 1.4.4 only. HiFi data are synthetic. Real Illumina nf-core test reads are shotgun-like, not amplicon, so they exercise only the "no false positive" path.
