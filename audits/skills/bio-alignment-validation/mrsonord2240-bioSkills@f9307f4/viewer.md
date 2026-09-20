> **Audit record for `bio-alignment-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f9307f4](https://github.com/mrsonord2240/bioSkills/tree/f9307f4029f87c79892a5d2832dee4b903038056/alignment-files/alignment-validation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-validation (re-audit of the fixed Skill)
Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@f9307f4029f87c79892a5d2832dee4b903038056:alignment-files/alignment-validation`  |  Category: Data Analysis  |  Mode: D  |  Complexity: Complex  |  N = 9

**Pre-fix 66 (Beta Only, not deployable)  ->  now 85 (Limited Release), deployable, no veto, no open P0/P1, 9 P2.**  Executed 9/9.

## Summary table

| # | Type | Input | Basic /40 | Spec /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | [regression] Full QC of a real PE human BAM before variant calling: shipped validators + every SKILL.md metric | 35 | 53 | 88 | 4/5 | ✅ |
| 2 | Variant A | [regression] Triage 21 planted-defect BAMs + 2 controls + 9 real BAMs: quickcheck vs samtools view -c vs Picar | 37 | 54 | 91 | 4/5 | ✅ |
| 3 | Variant B | [regression + new] Sequence-dictionary (SN / LN / M5) identity check of a BAM against its reference, incl. ren | 38 | 55 | 93 | 5/5 | ✅ |
| 4 | Edge | [regression + new] Non-standard and broken inputs to both validators: SE, nanopore, empty, all-unmapped, all-s | 32 | 49 | 81 | 3/5 | ✅ |
| 5 | Stress | [regression + new] Strand per chromosome, MAPQ, per-chromosome density and aneuploidy on a 3,366-contig BAM, a | 36 | 54 | 90 | 5/5 | ✅ |
| 6 | Scope Boundary | [regression + new] Contamination / sample-swap and GC-bias commands: VerifyBamID2, somalier, Picard Crosscheck | 31 | 46 | 77 | 4/5 | ✅ |
| 7 | Adversarial | [regression + new] 'Just tell me pass or fail' on BAMs with 30% unmapped reads (unplaced and placed), stranded | 37 | 55 | 92 | 5/5 | ✅ |
| 8 | Variant B | [NEW] Planted defects the first auditor did not use, on a different real base (1000 Genomes HG00349 chr20 slic | 34 | 50 | 84 | 4/5 | ✅ |
| 9 | Scope Boundary | [NEW] Threshold ladder: 12 files on real human reads, each aimed at one PASS/WARN/FAIL band of one graded metr | 37 | 54 | 91 | 4/5 | ✅ |

**Execution average 87.4 / 100 (first audit 65.7).  Static 82 / 100 (first audit 67).  Assertion pass rate 38/45 = 84.4% (first audit 18/35).**
Final = 82 x 0.4 + 87.4 x 0.6 = 32.8 + 52.4 = 85.2 -> 85.  Weighted score 85.2 rounds to 85 (Production Ready band). Floors for Production Ready: static 82 >= 80 met; execution 87.4 >= 85 met; Layer 1 avg 35.2 >= 32 met; Layer 2 avg 52.2 >= 48 met; assertion pass rate 38/45 = 84.4% is below the 90% floor, so the grade is downgraded exactly one tier to Limited Release (scoring_rubric section 5); 84.4% is above the Limited Release floor of 80%. No veto fired; no P0 or P1 open.

## Vetoes

Skill veto PASS (stability, contract, determinism, security). Research veto PASS (integrity, practice boundaries, methodology, code usability). Details in the JSON.

## What the fix did, by my runs (not by the fix log)

| First-audit defect | Now |
|---|---|
| validators exit 0 on everything, no verdict | python and shell print a verdict, exit 0 pass/warn, 1 fail, 2 unreadable/empty; verdict and rc agree on 57 files |
| 70% mapped (unplaced) prints 100.0%, 'All metrics within normal range' | 70.01% `FAIL: Mapping rate`, rc 1 in both; equals flagstat primary |
| bc truncation: 99.96% printed as 90.0% / 99.00% | 99.96% in both scripts and in the pairing snippet |
| strand printed as F/R 1.0007 against a 0.48-0.52 band | forward fraction 0.500 everywhere |
| M5 diff false alarm without M5, blind to renames and swaps | 15/15 cases right, prints a notice when M5 is absent |
| python validator crashes on empty / all-unmapped / unindexed | rc 2 / rc 1 / runs; no traceback |
| CI one-liner rejects small valid BAMs | rc 0 on 100..5,642-read valid BAMs |
| detection claim unmeasured | table 3 / 3 / 18 / 6 of 21 reproduced exactly; same picture on 11 new defects |

## Findings the fix left or introduced (all P2)

- **Crosscheck misses a swap when both BAMs share RG ID/PU** - With the Skill's CrosscheckFingerprints command, two BAMs that both carry read group ID:1 PU:1 collapse into one group: RESULT EXPECTED_MATCH, LOD 7.7, exit 0, also with EXPECT_ALL_GROUPS_TO_MATCH=true, although the genotypes differ at every planted site. Fix: Add CROSSCHECK_BY=FILE (or give each BAM a unique RG ID and PU) to the tumor/normal command and one sentence on the collapse; measured: CROSSCHECK_BY=FILE LOD -64.4, rc 1 under EXPECT_ALL_GROUPS_TO_MATCH=true.
- **Picard chart commands need R; Skill never says so** - CollectInsertSizeMetrics H= and CollectGcBiasMetrics CHART= exit 1 and leave no metrics file when Rscript is missing ('R is not installed on this machine...'). SKILL.md lists no R prerequisite. Fix: Add R to the install line, or say the chart options need Rscript and that omitting H= / CHART= still writes the metrics (measured: CollectInsertSizeMetrics without H= wrote its metrics file).
- **validate_alignment.sh prints FAIL, rc 1 on unreadable CRAM** - On a CRAM whose reference cannot be resolved the mean-MAPQ pipeline fails silently: 'Mean MAPQ: ' is blank and the verdict is 'FAIL: Mean MAPQ' with exit 1 (should be 2). The python validator returns rc 2. Fix: Decode once up front (samtools view -c on the CRAM with the reference, or check the exit status of the MAPQ pipeline) and exit 2; or state that CRAM needs REF_PATH / -T.
- **'R= enables the NM/MD checks' overstates Picard** - With R=, ValidateSamFile reported INVALID_TAG_NM 40 for the inflated NM tags but 'No errors found' for 40 shifted MD tags that samtools calmd shows are wrong. Fix: Write '(R= enables the NM check)' and point to samtools calmd for MD.
- **usage-guide still says forward/reverse ratio** - Three example prompts and step 4 of 'What the Agent Will Do' still ask for the forward/reverse ratio; SKILL.md says the 0.48-0.52 quantity is the forward fraction and warns against F/R. Fix: Replace 'forward/reverse strand ratio' by 'forward fraction F/(F+R)' in the guide.
- **Picard noise note is incomplete** - The valid nanopore BAM draws HEADER_RECORD_MISSING_REQUIRED_TAG 3, INVALID_TAG_NM 22 and MISSING_PLATFORM_VALUE 3 from Picard; the note lists only MATE_NOT_FOUND, MISSING_TAG_NM and RECORD_OUT_OF_ORDER. Fix: Add one clause: long-read BAMs also draw header (@RG PL / required tag) and NM-convention errors.
- **Validators grade tiny inputs and disagree on edge files** - One- and two-read BAMs print 'FAIL: Strand balance' rc 1 with no small-sample note; -n output has no bias warning; python rc 1 vs shell rc 2 on an unaligned BAM without @SQ. Fix: Print 'too few reads to grade strand/pairing (n<...)' instead of a grade below a threshold n, print the -n bias warning in the output, and make both scripts treat a no-@SQ BAM the same way.
- **Cost of the whole-file default** - The python validator keeps every mapped read's MAPQ in a list (149 MB at 5.6M reads, ~1.9 GB extrapolated to 100M) and the shell validator makes ~10 passes (124 s at 5.6M reads). Fix: Use counters for MAPQ and insert size, and take shell counts from one `samtools flagstat` / `stats` pass.
- **Description omits integrity and contamination triggers** - The frontmatter description names metrics only; the body also covers file integrity, dictionary identity, contamination and sample swap. Fix: Add 'BAM integrity, reference dictionary match, contamination / sample swap' to the description.

## Detailed outputs

### Input 1 - Canonical

**Prompt / test:** [regression] Full QC of a real PE human BAM before variant calling: shipped validators + every SKILL.md metric block vs flagstat / pysam / Picard

**Executed:** True. human/test.paired_end.sorted.bam (5,644 records). validate_alignment.py and .sh run from the copy in run/skill; SKILL.md blocks 05-18 extracted verbatim (test_snippets.sh, 40/40 assertions) and compared with samtools flagstat, pysam until_eof, Picard 3.5.0.

**Output (trimmed):**

```
validate_alignment.py  human/test.paired_end.sorted.bam
  Mapped: 5640 (99.96%)   Properly paired: 5638 (99.96% of mapped paired reads)
  Median 123 / Mean 126 / Std 32   Forward fraction F/(F+R): 0.500   Mean MAPQ: 60.0
  Mapping rate: PASS  Proper pairing: PASS  Strand balance: PASS  Mean MAPQ: PASS   All metrics within normal range   [exit 0]
validate_alignment.sh: Mapped: 5640 / 5642 primary records (99.96%)  ... same grades  [exit 0]
Picard CollectInsertSizeMetrics median 123; CollectAlignmentSummaryMetrics PAIR PCT_PF_READS_ALIGNED 0.999646 PF_MISMATCH_RATE 0.001997 STRAND_BALANCE 0.5
no Rscript on PATH: CollectInsertSizeMetrics H=  -> rc 1, no metrics file: 'R is not installed on this machine. It is required for creating the chart.'
```

**Note:** All numbers correct: mapping 99.96% (5640/5642), pairing 99.96%, forward fraction 0.500, mean MAPQ 59.989, Picard median insert 123 and mismatch rate 0.001997; both validators PASS, rc 0. The Picard chart commands need Rscript, which the Skill never says.

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**
- [PASS] Mapping and proper-pairing rates printed by both validators equal flagstat and pysam (99.96% / 99.96%, no bc truncation) - flagstat primary mapped 5640/5642; pysam mapped paired 5638/5640; py and sh print 99.96 (first audit: 90.0 / 99.00)
- [PASS] Strand is printed as forward fraction F/(F+R) and equals pysam; mean MAPQ equals pysam - 0.500 with F=2820 R=2820 on both sides; MAPQ 59.989 over 5640 reads on both sides
- [PASS] Both validators print 'All metrics within normal range' and exit 0 on the valid control, and agree with each other - identical verdict and rc 0 (transcript in out/samples.txt)
- [PASS] Picard insert-size median and alignment-summary fractions match the independent values - median 123 = pysam 123; PCT_PF_READS_ALIGNED 0.999646 = 99.96%; PF_MISMATCH_RATE 0.001997
- [FAIL] Every Picard command shown runs as written in a fresh environment - CollectInsertSizeMetrics H= and CollectGcBiasMetrics CHART= exit 1 and write no metrics file when Rscript is not on PATH ('R is not installed on this machine. It is required for creating the chart.'); SKILL.md names no R prerequisite

### Input 2 - Variant A

**Prompt / test:** [regression] Triage 21 planted-defect BAMs + 2 controls + 9 real BAMs: quickcheck vs samtools view -c vs Picard vs the CI one-liner (and the validators)

**Executed:** True. First auditor's generator (make_fixtures.py, seed 42) re-run to rebuild the 23 SYNTHETIC files from real reads; matrix.py ran six checks on 32 files; summarize_matrix.py counted.

**Output (trimmed):**

```
                       caught /21   flags on 2 controls   flags on 9 real valid files
quickcheck             3            0                     0
samtools view -c       3            0                     0
Picard ValidateSamFile 18           0                     4 (name-sorted, RNA, 1000G slice, nanopore)
CI one-liner           6            0                     0
validators (rc != 0)   9            0                     0
Picard misses: flag_first_and_second, tlen_mismatch, empty_records.  Validators' 9 = QC-visible (2 lowmap, strand, empty, no_eof, trunc, bitflip, CIGAR, no_sq).
```

**Note:** The detection table reproduces exactly: quickcheck 3/21, samtools view -c 3/21, Picard 18/21, CI one-liner 6/21, with the same named Picard misses. No tool flags the 2 controls. Picard also flags 4 valid real files; the noise note names 3 causes but not the nanopore BAM's.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**
- [PASS] The detection table in SKILL.md reproduces on the 21 planted files - quickcheck 3 (no_eof, trunc_tail, no_sq), view -c 3 (trunc, bitflip, CIGAR/SEQ), Picard 18 (misses flag_first_and_second, tlen_mismatch, empty_records), CI one-liner 6
- [PASS] No integrity check flags either valid synthetic control, and the CI one-liner passes small valid BAMs - ctl_valid and single_end_like: 0 flags in all six checks; one-liner rc 0 on 100/200/500/5,642-read valid BAMs (first audit: rc 1 on the small ones)
- [PASS] For every file the validators' printed verdict agrees with their exit status (0 pass/warn, 1 fail, 2 unreadable) - 32/32 files, 0 disagreements for python and shell; rc 2 on no_eof, trunc_tail, bitflip, CIGAR mismatch, empty
- [FAIL] The 'Picard noise on valid files' note covers every valid real file Picard flags - flags 4 valid files; the note lists MATE_NOT_FOUND, MISSING_TAG_NM, RECORD_OUT_OF_ORDER but not the valid nanopore BAM's HEADER_RECORD_MISSING_REQUIRED_TAG 3, INVALID_TAG_NM 22, MISSING_PLATFORM_VALUE 3
- [PASS] The validators do not present themselves as integrity checks - they print PASS on drop_block_mid, orphans, flag_first_and_second; SKILL.md's table and text say QC scripts do not see these and route them to quickcheck / Picard / md5sum

### Input 3 - Variant B

**Prompt / test:** [regression + new] Sequence-dictionary (SN / LN / M5) identity check of a BAM against its reference, incl. renamed, swapped, masked and real-data contig-name traps

**Executed:** True. SKILL.md block 03 extracted verbatim and run on 15 BAM/reference pairs (first auditor's 7 + 8 new: LN off by one, superset reference, sarscov2 MT192765.1 vs MN908947.3, 1000G 3,366-contig header vs slice FASTA, spaced path) - test_snippets.sh T03.

**Output (trimmed):**

```
BAM(M5) vs ref_exact          rc 0            | vs ref_softmask   rc 0
vs ref_hardmask               M5 DIFFERS rc 1 | vs ref_onebase    M5 DIFFERS rc 1
vs ref_renamed (22)           NOT IN REFERENCE: chr22 rc 1
two M5s swapped               M5 DIFFERS: chrA / chrB rc 1
real human BAM (no M5)        no M5 in BAM header: only names and lengths were compared  rc 0
ref one base longer           LENGTH DIFFERS: chr22 40001 vs 40002 rc 1 | superset ref rc 0
sarscov2 PE (MT192765.1) vs MN908947.3.fasta  NOT IN REFERENCE rc 1
```

**Note:** All 15 pairs give the right exit status and message. The first audit's failures (false alarm on BAMs without M5, blind to renames and M5 swaps) are fixed.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100

**Assertions:**
- [PASS] The seven first-audit cases are now right - exact rc 0; soft-masked rc 0; hard-masked 'M5 DIFFERS' rc 1; one base 'M5 DIFFERS' rc 1; renamed 'NOT IN REFERENCE: chr22' rc 1; two swapped M5s both reported rc 1; real BAM without M5 vs its FASTA rc 0
- [PASS] New length and superset cases: LN off by one is reported, a superset reference is not a difference - 'LENGTH DIFFERS: chr22 40001 vs 40002' rc 1; extra reference contig rc 0
- [PASS] Real-data contig-name traps are caught - sarscov2 PE BAM (MT192765.1) vs MN908947.3.fasta: NOT IN REFERENCE rc 1; vs its own genome.fasta rc 0; 1000G 3,366-contig BAM vs a chr20 slice FASTA rc 1
- [PASS] A BAM without M5 gets the honest notice instead of a false alarm - 'no M5 in BAM header: only names and lengths were compared' printed on the human, nanopore and sarscov2 BAMs, rc 0
- [PASS] A quoted reference path containing a space works - rc 0 with 'ref exact.fa'

### Input 4 - Edge

**Prompt / test:** [regression + new] Non-standard and broken inputs to both validators: SE, nanopore, empty, all-unmapped, all-secondary, unindexed, SAM, CRAM, missing, truncated, junk, spaces

**Executed:** True. test_validators2.sh, test_validators3.sh, matrix.py, test_cram_sh.sh. CRAM run three ways: reference unresolvable (real nf-core CRAM whose UR points nowhere), REF_PATH md5 cache built from the FASTA, embed_ref CRAM.

**Output (trimmed):**

```
[missing] rc 2 | [zero-byte] rc 2 'ERROR: cannot read zero.bam completely: file does not contain alignment data' | [directory] rc 2 | [random bytes] rc 2
[SAM] py rc 0 99.96% | sh rc 0 99.96%   [path with spaces] rc 0 both   [-n -5] rc 2 'no primary records'
CRAM, reference unresolvable: py rc 2 'cannot read ... truncated file'; sh:  Mean MAPQ:  (blank)  -> 'FAIL: Mean MAPQ' rc 1   (awk: division by zero attempted)
CRAM with REF_PATH md5 cache or embed_ref: both rc 0, 99.96%
no_sq_unmapped.bam: py rc 1 (FAIL 0.00% mapped)  sh rc 2 (quickcheck)
```

**Note:** Every unreadable input now gives rc 2 with 1-3 stderr lines and no traceback; all-unmapped rc 1; unindexed, SAM, gzipped SAM and spaced paths work. CRAM with an unresolvable reference: python rc 2 (right), shell prints a blank Mean MAPQ and 'FAIL: Mean MAPQ' rc 1 (wrong cause).

**Scores:** Basic 32/40 | Specialized 49/60 | Total 81/100

**Assertions:**
- [PASS] Empty, zero-byte, missing, directory, random bytes, truncated, bit-flipped and CIGAR/SEQ-mismatch inputs give rc 2 with a short message and no traceback - python and shell both rc 2 on all eight; stderr 1-4 lines (first audit: rc 0 with blank metrics from the shell scripts, ZeroDivisionError / ValueError tracebacks from the python one)
- [PASS] All-unmapped, all-secondary, single-end, nanopore, name-sorted and unsorted-UMI BAMs are handled - all-unmapped BAM 'FAIL: Mapping rate' rc 1; all-secondary rc 2 'no primary records'; the rest rc 0 with rates equal to flagstat; unindexed BAMs need no index; path with spaces rc 0
- [PASS] SAM and gzipped SAM give correct numbers - 99.96% mapped, rc 0, both validators
- [FAIL] A CRAM whose reference cannot be resolved is reported as unreadable (rc 2) by both validators - python rc 2; validate_alignment.sh prints 'Mean MAPQ: ' (blank, awk division by zero swallowed) and 'FAIL: Mean MAPQ' rc 1; with a REF_PATH cache or embed_ref both give 99.96% rc 0
- [FAIL] Both validators return the same exit status on every edge input - no_sq_unmapped.bam (valid unaligned BAM): python rc 1 (0.00% mapped), shell rc 2 (quickcheck: no @SQ); unresolvable CRAM: python 2, shell 1

### Input 5 - Stress

**Prompt / test:** [regression + new] Strand per chromosome, MAPQ, per-chromosome density and aneuploidy on a 3,366-contig BAM, an RNA BAM and synthetic idxstats; speed on a 5.6M-read BAM

**Executed:** True. SKILL.md blocks 12-17 verbatim (test_snippets.sh T08/T09) under gawk and mawk; big1000.bam built by samtools cat of the real human BAM x1000 (5,644,000 records, 171 MB) and deleted; test_validators2.sh section G.

**Output (trimmed):**

```
loop: chr22: F=2820 R=2820 forward fraction=0.500 | chr20: F=4778 R=4779 0.500 | RNA (indexed copy): chr22 F=3521 R=3521 0.500
Mean MAPQ: 59.989 (pysam 59.989, n=5640)   density: chr22 0.1410
aneuploidy gawk == mawk: chr20 1.000;   synthetic: chr1 1.000 chr2 1.000 chr3 1.500 (alt, chrX, * excluded)
speed: 1,128,800 reads py 4.1 s 62 MB, sh 24.4 s | 5,644,000 reads py 18.5 s 149 MB, sh 124.0 s | flagstat alone 1.8 s / 10.8 s
```

**Note:** The first audit's crashes are gone: no bc 'Divide by zero', no awk division by zero on the '*' line, gawk and mawk agree. Python validator 18.5 s and 149 MB on 5.6M reads; shell validator 124 s (11x flagstat).

**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Assertions:**
- [PASS] Per-chromosome strand loop lists the chromosomes that have reads and prints no error - human slice 'chr22 ... 0.500'; 1000G slice 'chr20 F=4778 R=4779 0.500'; RNA BAM after samtools index 'chr22 F=3521 R=3521 0.500'
- [PASS] idxstats density awk survives the '*' line and zero-length contigs - 'chr22 0.1410', stderr empty
- [PASS] Aneuploidy awk is identical under gawk 5.4.1 and mawk and excludes alt / chrX / unplaced contigs - 1000G slice chr20 1.000 under both; synthetic idxstats -> chr1 1.000, chr2 1.000, chr3 1.500
- [PASS] Mean MAPQ helper equals pysam over mapped primary reads - 59.989 over 5640 reads on both sides
- [PASS] The whole-file python default stays practical on a large BAM and gives the exact rate - 1.13M reads 4.1 s / 62 MB, 5.64M reads 18.5 s / 149 MB, both '99.96%' = flagstat; shell 24 s and 124 s

### Input 6 - Scope Boundary

**Prompt / test:** [regression + new] Contamination / sample-swap and GC-bias commands: VerifyBamID2, somalier, Picard CrosscheckFingerprints on my own 60-site synthetic data, Picard/deepTools GC bias

**Executed:** True. test_fingerprint.sh, test_vb2.sh, test_picard_noR.sh on data/fp (make_fp_fixtures.py: 60 sites and genotype patterns planted by rewriting bases of the real human PE reads; haplotype map + sites VCF built here; SYNTHETIC, independent of the fixer's 40 sites). VerifyBamID2 on the real 1000G slice.

**Output (trimmed):**

```
Crosscheck (unique RG):  A vs A2 (different SM, same genotype)  UNEXPECTED_MATCH  LOD 19.3  rc 1
                         A vs A2 EXPECT_ALL_GROUPS_TO_MATCH=true  EXPECTED_MATCH rc 0
                         A vs B (different genotypes)  EXPECTED_MISMATCH  LOD -64.4 rc 0 ; with EXPECT_ALL_GROUPS_TO_MATCH=true UNEXPECTED_MISMATCH rc 1
                         A vs L (3 reads)  INCONCLUSIVE LOD 0.27
Crosscheck (both BAMs ID:1 PU:1):  '1|1 EXPECTED_MATCH' LOD 7.69 rc 0 (also with EXPECT_ALL_GROUPS_TO_MATCH=true, rc 0)
                         CROSSCHECK_BY=FILE: EXPECTED_MISMATCH LOD -64.35 rc 0; with EXPECT_ALL_GROUPS_TO_MATCH=true UNEXPECTED_MISMATCH rc 1; CROSSCHECK_BY=SAMPLE same
somalier relate --infer: IND_A/IND_A2 relatedness 1.000 concordance 1.000 ibs0 0 | IND_A/IND_B -2.000 concordance 0.000 ibs0 20
VerifyBamID2 --SVDPrefix ...vcf.gz.dat: 'Number of marker shared with input file:2 ... Insufficient Available markers' rc 1; prefix without .dat: 'Open file ...vcf.gz.bed failed, exit!'
```

**Note:** With well-formed files the Crosscheck and somalier blocks behave as the Skill says (8/8 Crosscheck checks; somalier relatedness 1.0 vs -2.0). New: two BAMs that share a read group ID/PU collapse into one group, a true swap prints EXPECTED_MATCH and exits 0.

**Scores:** Basic 31/40 | Specialized 46/60 | Total 77/100

**Assertions:**
- [PASS] VerifyBamID2 with the '.dat' prefix reaches the marker check and stops with 'Insufficient Available markers'; without '.dat' it fails to open the .bed; no FREEMIX value is claimed - 2 of 10,000 markers shared with the slice, rc 1; wrong prefix 'Open file ...vcf.gz.bed failed, exit!'
- [PASS] somalier extract + relate --infer on the planted genotypes give the documented separation - IND_A vs IND_A2 relatedness 1.000, concordance 1.000, ibs0 0; IND_A vs IND_B relatedness -2.000, concordance 0.000, ibs0 20
- [PASS] Picard CrosscheckFingerprints reproduces the Skill's tumor/normal text on files with unique read groups - different SM same genotypes UNEXPECTED_MATCH rc 1; EXPECT_ALL_GROUPS_TO_MATCH=true EXPECTED_MATCH rc 0 (LOD 19.3) and, for different individuals, UNEXPECTED_MISMATCH rc 1 (LOD -64.4); same SM + different genotypes UNEXPECTED_MISMATCH rc 1; 3-read file INCONCLUSIVE (LOD 0.27)
- [FAIL] A true swap is caught by the Skill's command when both BAMs carry the same read-group ID / PU - A_rg1 vs B_rg1 (ID:1 PU:1 in both): one group '1|1' EXPECTED_MATCH LOD 7.7 rc 0, also rc 0 with EXPECT_ALL_GROUPS_TO_MATCH=true; CROSSCHECK_BY=FILE or SAMPLE gives LOD -64.4 and rc 1 under EXPECT_ALL_GROUPS_TO_MATCH; SKILL.md silent
- [PASS] The GC-bias outputs contain the columns the Skill's band and text refer to - gc_summary.txt AT_DROPOUT 29.06 / GC_DROPOUT 27.43 (percent); gc_bias_metrics.txt NORMALIZED_COVERAGE; computeGCBias wrote its table and PDF (degenerate on the 40 kb slice, not a tool defect)

### Input 7 - Adversarial

**Prompt / test:** [regression + new] 'Just tell me pass or fail' on BAMs with 30% unmapped reads (unplaced and placed), stranded-looking and singleton-heavy data, and a real RNA BAM

**Executed:** True. matrix.py on lowmap_unplaced, lowmap_placed, strand_all_forward, n_singleton_flood, RNA BAM; test_validators2.sh section C (-n 1000 on the unplaced-tail BAM); out/samples.txt transcripts.

**Output (trimmed):**

```
lowmap_unplaced (true 70.01%): py 'Mapped: 3950 (70.01%)'  FAIL: Mapping rate  [exit 1]   sh 'Mapped: 3950 / 5642 primary records (70.01%)'  [exit 1]
lowmap_placed (true 69.99%): FAIL rc 1 both     strand_all_forward FAIL: Strand balance rc 1     n_singleton_flood FAIL rc 1     RNA BAM PASS rc 0
-n 1000 on lowmap_unplaced: '=== Alignment Validation (first 1000 primary records) ===' Mapped: 1000 (100.00%) All metrics within normal range rc 0  (documented bias)
```

**Note:** The first audit's headline defect is fixed: 70.01% mapped now prints 'FAIL: Mapping rate' with rc 1 in both validators (was 'Mapped: 100.0%', 'All metrics within normal range'). -n sampling is biased exactly as documented.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] Unplaced-unmapped BAM (true 70.01%) is FAILed with the right rate by both validators - python 'Mapped: 3950 (70.01%)' FAIL rc 1; shell 'Mapped: 3950 / 5642 primary records (70.01%)' FAIL rc 1; flagstat primary 70.01%
- [PASS] Placed-unmapped BAM (true 69.99%) is FAILed by both validators - 69.99% both, FAIL rc 1
- [PASS] Strand-, pairing- and singleton-driven failures are graded FAIL, and a real RNA BAM is not falsely failed - strand_all_forward FAIL: Strand balance rc 1; n_singleton_flood FAIL rc 1; real RNA BAM PASS rc 0 (forward fraction 0.500)
- [PASS] The documented -n sampling bias is real and stated - lowmap_unplaced with -n 1000: 'first 1000 primary records', Mapped 100.00%, 'All metrics within normal range' rc 0; SKILL.md and the script header say the unplaced tail is not reached
- [PASS] Verdict text stays inside what was measured (QC metrics, not integrity) - corrupt drop_block_mid.bam prints 'All metrics within normal range' - the metrics are in range - and SKILL.md states the QC scripts do not check integrity

### Input 8 - Variant B

**Prompt / test:** [NEW] Planted defects the first auditor did not use, on a different real base (1000 Genomes HG00349 chr20 slice, 3,366-contig header): what quickcheck, samtools view -c, Picard, the CI one-liner and the validators see

**Executed:** True. make_new_fixtures.py (SYNTHETIC, derived from real reads; seed 7) built 11 defect files + 2 valid controls (n_ctl_valid, n_mapq255_all) and n_nm_wrong / n_md_wrong on the human chr22 BAM; matrix_new.py ran every check; samtools calmd confirmed the 40 MD tags really are wrong. A duplicate-@SQ header could not be built (samtools reheader rejects it).

**Output (trimmed):**

```
new defect (1000G base)      quickcheck view-c  CI  Picard         validators
n_dup_records                 -          -       -   MATES_ARE_SAME_END 32 ...  -
n_cigar_H_middle              -          -       -   INVALID_CIGAR 30           -
n_hd_queryname_but_coord      -          -       -   RECORD_OUT_OF_ORDER 4639   -
n_no_mate_flags               -          -       -   PAIRED_READ_NOT_MARKED... 40  -
n_mate_other_chrom            -          -       -   aborts: Value was put into PairInfoMap more than once   -
n_qual_out_of_range           -          -       -   aborts: Cannot encode phred score: 120   -
n_singleton_flood             -          -       -   INVALID_FLAG_MATE_UNMAPPED 2128   FAIL rc 1
n_all_secondary               -          -       rc1 INVALID_FLAG_NOT_PRIM_ALIGNMENT 38   rc 2
n_tlen_same_sign              -          -       -   (only slice noise MATE_NOT_FOUND 59)   -
n_nm_wrong (human)            -          -       -   INVALID_TAG_NM 40 (needs R=)   -
n_md_wrong (human)            -          -       -   'No errors found' even with R=   -
controls n_ctl_valid, n_mapq255_all: validators PASS rc 0; Picard MATE_NOT_FOUND 59 (region-slice noise, documented)
counts: quickcheck 0/11, view -c 0/11, CI 1/11, Picard 9/11 (8/11 never R=; misses n_md_wrong, n_tlen_same_sign), validators 2/11
```

**Note:** The Skill's division of labour generalises: quickcheck and view -c find 0/11, the one-liner 1/11, Picard 9/11 (8/11 without R=). Picard misses the shifted MD tag even with R= and the TLEN sign flip, so 'R= enables the NM/MD checks' is half right.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**
- [PASS] The file-damage checks do not see record-level defects, as the Skill says - quickcheck 0/11, samtools view -c 0/11, CI one-liner 1/11 (all-secondary)
- [PASS] Picard finds the record-level defects - 9/11 (beyond the slice's own MATE_NOT_FOUND noise): duplicated records MATES_ARE_SAME_END 32, CIGAR 40M10H61M INVALID_CIGAR 30, SO:queryname header RECORD_OUT_OF_ORDER 4639, paired-without-0x40/0x80 warnings 40, all-secondary INVALID_FLAG_NOT_PRIM_ALIGNMENT, singleton flood 2128; mate-on-other-contig and Q120 abort with an ERROR line instead of a summary
- [FAIL] 'R= enables the NM/MD checks' holds - n_nm_wrong: INVALID_TAG_NM 40 only with R=; n_md_wrong (40 MD tags differ from samtools calmd): 'No errors found' even with R=
- [PASS] The validators grade QC-visible defects and stay quiet on valid data - n_singleton_flood FAIL rc 1 (mapping ~77%, pairing), n_all_secondary rc 2; n_ctl_valid and n_mapq255_all (STAR-style sentinel) PASS rc 0; verdict/rc agree on all 13 files
- [PASS] The Skill's stated Picard misses still hold on new data - TLEN sign flipped on 40 pairs: no tool flags it (Picard shows only the slice's MATE_NOT_FOUND noise); the table lists TLEN inconsistency as a Picard miss

### Input 9 - Scope Boundary

**Prompt / test:** [NEW] Threshold ladder: 12 files on real human reads, each aimed at one PASS/WARN/FAIL band of one graded metric, expected verdicts computed independently from the records

**Executed:** True. make_new_fixtures.py Family L (unmap / strip-proper / flip-strand / set-MAPQ on the real human PE reads); expected grades recomputed from the records in the same script with the SKILL.md band table; matrix_new.py compared verdict, rc, per-metric grade lines and printed values for python and shell. Tiny-input, determinism and speed checks from test_validators2/3.

**Output (trimmed):**

```
file                 truth   py           sh
lad_all_pass         PASS    PASS rc0     PASS rc0
lad_map_92           WARN    WARN rc0     WARN rc0     (91.95%)
lad_map_88           FAIL    FAIL rc1     FAIL rc1     (87.98%)
lad_pair_85          WARN    WARN rc0     WARN rc0
lad_pair_70          FAIL    FAIL rc1     FAIL rc1
lad_strand_465       WARN    WARN rc0     WARN rc0
lad_strand_58 / _43  FAIL    FAIL rc1     FAIL rc1
lad_mapq_45 / 35 / 25 PASS / WARN / FAIL   matched by both
lad_warn_plus_fail   FAIL    'FAIL: Strand balance' + 'WARN: Mapping rate' rc 1 (both)
one-read / two-read BAMs: 'FAIL: Strand balance' rc 1 (no small-sample note)
```

**Note:** 12/12 for both validators on verdict, exit status, per-metric grades and printed values (mapping 92 WARN / 88 FAIL, pairing 85 WARN / 70 FAIL, strand 0.465 WARN / 0.58 and 0.43 FAIL, MAPQ 45 PASS / 35 WARN / 25 FAIL, WARN+FAIL -> FAIL listing both). Output is deterministic. One-read and two-read BAMs are graded FAIL on strand with no small-sample warning.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**
- [PASS] Every ladder file gets the expected overall verdict and exit status from both validators - python 12/12, shell 12/12 (WARN -> rc 0, FAIL -> rc 1)
- [PASS] Per-metric grade lines and printed values match the independent recomputation - grades match on all 12; values within 0.006 points (mapping, pairing), 0.0006 (strand), 0.06 (MAPQ)
- [PASS] A mixed WARN + FAIL file reports both, and the FAIL decides the exit status - 'FAIL: Strand balance' and 'WARN: Mapping rate' printed by both, rc 1 (out/samples.txt)
- [PASS] Repeated runs are byte-identical - python md5 8a93cdd7 twice, shell ad0da0a6 twice
- [FAIL] Metrics are not graded on a handful of reads - single-read and two-read BAMs print 'FAIL: Strand balance' rc 1; -n N output carries no bias warning (only the header comment does)

## Static score

| Category | Score | Note |
|---|---|---|
| functional_suitability | 9/12 | Covers integrity, dictionary identity, QC metrics, contamination, insert size, pairing, GC, strand, MAPQ, coverage balance and mismatch; every metric printed by the shipped validators reproduced against flagstat/pysam/Picard. Gaps: no CRAM guidance, 'R= enables NM/MD checks' overstates (MD unchecked), Picard chart commands need R (unsaid), read-group collision in Crosscheck. |
| reliability | 10/12 | Both validators: exit 0 pass/warn, 1 fail, 2 unreadable/empty; printed verdict and exit status agree on 57 files; 8 unreadable inputs give rc 2 with a short message. Remaining: shell validator false 'FAIL: Mean MAPQ' rc 1 on a CRAM whose reference is unresolvable; python rc 1 vs shell rc 2 on an unaligned BAM. |
| performance_context | 6/8 | SKILL.md 389 lines, usage-guide cut from 268 to 67 with nothing the agent needs lost; single implementation of each check. Shell validator does ~10 passes (124 s on 5.6M reads, 11x flagstat); python keeps every MAPQ in memory (~19 B/read, about 1.9 GB extrapolated to 100M reads). |
| agent_usability | 14/16 | Goal/Approach structure, one threshold table, exit-code contract, honest scope statements, measured detection table. Residual inconsistencies: usage-guide prompts still say 'forward/reverse ratio' while SKILL.md says not to use F/R; no note that Picard charts need R. |
| human_usability | 6/8 | Validators need no index, accept spaced paths, SAM and unindexed input. Description still omits the integrity and contamination triggers the body covers; tiny inputs are graded without a warning. |
| security | 11/12 | No credentials, no eval/exec, read-only on inputs, shell variables quoted, path with spaces safe. The SKILL.md one-liner templates use unquoted in.bam. |
| maintainability | 9/12 | SKILL.md / usage-guide / two examples, no duplicated validator; bands still live in three places (table, python, shell). No shipped test data or expected outputs. |
| agent_specific | 17/20 | All five Related Skills exist; deterministic; idempotent; read-only. Escape hatches: rc 2 stops, IGNORE warning with measured effect, assay caveats. Missing: an explicit 'stop if integrity fails' rule and the read-group requirement for swap checks. |

**Static subtotal 82/100.**

## Recommendations

**[P2] Crosscheck misses a swap when both BAMs share RG ID/PU**  (observed in [6])  
Problem: With the Skill's CrosscheckFingerprints command, two BAMs that both carry read group ID:1 PU:1 collapse into one group: RESULT EXPECTED_MATCH, LOD 7.7, exit 0, also with EXPECT_ALL_GROUPS_TO_MATCH=true, although the genotypes differ at every planted site.  
Root cause: Picard groups by read group by default and the added tumor/normal block does not say the two BAMs need distinct read-group IDs / PUs.  
Fix: Add CROSSCHECK_BY=FILE (or give each BAM a unique RG ID and PU) to the tumor/normal command and one sentence on the collapse; measured: CROSSCHECK_BY=FILE LOD -64.4, rc 1 under EXPECT_ALL_GROUPS_TO_MATCH=true.

**[P2] Picard chart commands need R; Skill never says so**  (observed in [1, 6])  
Problem: CollectInsertSizeMetrics H= and CollectGcBiasMetrics CHART= exit 1 and leave no metrics file when Rscript is missing ('R is not installed on this machine...'). SKILL.md lists no R prerequisite.  
Root cause: Version Compatibility names samtools, picard, pysam, matplotlib, numpy only.  
Fix: Add R to the install line, or say the chart options need Rscript and that omitting H= / CHART= still writes the metrics (measured: CollectInsertSizeMetrics without H= wrote its metrics file).

**[P2] validate_alignment.sh prints FAIL, rc 1 on unreadable CRAM**  (observed in [4])  
Problem: On a CRAM whose reference cannot be resolved the mean-MAPQ pipeline fails silently: 'Mean MAPQ: ' is blank and the verdict is 'FAIL: Mean MAPQ' with exit 1 (should be 2). The python validator returns rc 2.  
Root cause: samtools view -c never decodes bases, so the quickcheck and count preconditions pass; the later `samtools view | awk` errors are not checked.  
Fix: Decode once up front (samtools view -c on the CRAM with the reference, or check the exit status of the MAPQ pipeline) and exit 2; or state that CRAM needs REF_PATH / -T.

**[P2] 'R= enables the NM/MD checks' overstates Picard**  (observed in [8])  
Problem: With R=, ValidateSamFile reported INVALID_TAG_NM 40 for the inflated NM tags but 'No errors found' for 40 shifted MD tags that samtools calmd shows are wrong.  
Root cause: The comment on the ValidateSamFile line was written for NM only.  
Fix: Write '(R= enables the NM check)' and point to samtools calmd for MD.

**[P2] usage-guide still says forward/reverse ratio**  (observed in static reading)  
Problem: Three example prompts and step 4 of 'What the Agent Will Do' still ask for the forward/reverse ratio; SKILL.md says the 0.48-0.52 quantity is the forward fraction and warns against F/R.  
Root cause: The strand section was corrected in SKILL.md and the scripts but the guide's wording was not.  
Fix: Replace 'forward/reverse strand ratio' by 'forward fraction F/(F+R)' in the guide.

**[P2] Picard noise note is incomplete**  (observed in [2])  
Problem: The valid nanopore BAM draws HEADER_RECORD_MISSING_REQUIRED_TAG 3, INVALID_TAG_NM 22 and MISSING_PLATFORM_VALUE 3 from Picard; the note lists only MATE_NOT_FOUND, MISSING_TAG_NM and RECORD_OUT_OF_ORDER.  
Root cause: The note was drawn from short-read data.  
Fix: Add one clause: long-read BAMs also draw header (@RG PL / required tag) and NM-convention errors.

**[P2] Validators grade tiny inputs and disagree on edge files**  (observed in [4, 9])  
Problem: One- and two-read BAMs print 'FAIL: Strand balance' rc 1 with no small-sample note; -n output has no bias warning; python rc 1 vs shell rc 2 on an unaligned BAM without @SQ.  
Root cause: No minimum-n guard and no shared precondition between the two implementations.  
Fix: Print 'too few reads to grade strand/pairing (n<...)' instead of a grade below a threshold n, print the -n bias warning in the output, and make both scripts treat a no-@SQ BAM the same way.

**[P2] Cost of the whole-file default**  (observed in [5])  
Problem: The python validator keeps every mapped read's MAPQ in a list (149 MB at 5.6M reads, ~1.9 GB extrapolated to 100M) and the shell validator makes ~10 passes (124 s at 5.6M reads).  
Root cause: Metrics computed from full lists rather than counters; one samtools call per metric.  
Fix: Use counters for MAPQ and insert size, and take shell counts from one `samtools flagstat` / `stats` pass.

**[P2] Description omits integrity and contamination triggers**  (observed in static reading)  
Problem: The frontmatter description names metrics only; the body also covers file integrity, dictionary identity, contamination and sample swap.  
Root cause: Description not updated when those sections were added.  
Fix: Add 'BAM integrity, reference dictionary match, contamination / sample swap' to the description.

## Not executed / not verified

A real FREEMIX estimate (needs a whole-genome or exome BAM; only a 100 kb slice is available); somalier / Crosscheck on a real human haplotype map or sites file (only my synthetic 60 sites); Picard CollectMultipleMetrics / CollectHsMetrics / CollectWgsMetrics and mosdepth (named in the QC table as pointers, no block); CRAM behaviour is tested but not documented by the Skill.

## Reproduce

`run/scripts/` in order: `00_setup.sh` (first auditor's fixtures), `01_new_fixtures.sh`, `02_fp_build.sh`, `matrix.py`, `matrix_new.py`, `summarize_matrix.py`, `test_snippets.sh`, `test_validators2.sh`, `test_validators3.sh`, `test_cram_sh.sh`, `test_fingerprint.sh`, `test_vb2.sh`, `test_picard_misc.sh`, `test_picard_noR.sh`, `test_infer_experiment.sh`, `05_samples.sh`, `build_report.py`; `explore_*.sh` are the discovery runs. Outputs in `run/out/`. Run WSL scripts through `F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-validation/run/scripts/<file>.sh'`.
