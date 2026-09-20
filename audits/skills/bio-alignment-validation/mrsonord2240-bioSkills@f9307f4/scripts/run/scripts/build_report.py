"""Builds eval_report_bio-alignment-validation_result.json and eval_viewer_bio-alignment-validation.md (re-audit of the fixed Skill)
from the scores and assertions written below.  Every number quoted in a note was printed by a script in run/scripts (see run/out).
Run (Windows python, utf-8):  python build_report.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = "bio-alignment-validation"
SRC = "mrsonord2240/bioSkills@f9307f4029f87c79892a5d2832dee4b903038056:alignment-files/alignment-validation"

P, F = "PASS", "FAIL"


def A(text, result, note):
    return {"text": text, "result": result, "note": note}


inputs = [
    dict(index=1, type="Canonical", label="[regression] Full QC of a real PE human BAM before variant calling: shipped validators + every SKILL.md metric block vs flagstat / pysam / Picard",
         executed=True,
         execution_note="human/test.paired_end.sorted.bam (5,644 records). validate_alignment.py and .sh run from the copy in run/skill; SKILL.md blocks 05-18 extracted verbatim (test_snippets.sh, 40/40 assertions) and compared with samtools flagstat, pysam until_eof, Picard 3.5.0.",
         note="All numbers correct: mapping 99.96% (5640/5642), pairing 99.96%, forward fraction 0.500, mean MAPQ 59.989, Picard median insert 123 and mismatch rate 0.001997; both validators PASS, rc 0. The Picard chart commands need Rscript, which the Skill never says.",
         basic=35, specialized=53,
         assertions=[
             A("Mapping and proper-pairing rates printed by both validators equal flagstat and pysam (99.96% / 99.96%, no bc truncation)", P, "flagstat primary mapped 5640/5642; pysam mapped paired 5638/5640; py and sh print 99.96 (first audit: 90.0 / 99.00)"),
             A("Strand is printed as forward fraction F/(F+R) and equals pysam; mean MAPQ equals pysam", P, "0.500 with F=2820 R=2820 on both sides; MAPQ 59.989 over 5640 reads on both sides"),
             A("Both validators print 'All metrics within normal range' and exit 0 on the valid control, and agree with each other", P, "identical verdict and rc 0 (transcript in out/samples.txt)"),
             A("Picard insert-size median and alignment-summary fractions match the independent values", P, "median 123 = pysam 123; PCT_PF_READS_ALIGNED 0.999646 = 99.96%; PF_MISMATCH_RATE 0.001997"),
             A("Every Picard command shown runs as written in a fresh environment", F, "CollectInsertSizeMetrics H= and CollectGcBiasMetrics CHART= exit 1 and write no metrics file when Rscript is not on PATH ('R is not installed on this machine. It is required for creating the chart.'); SKILL.md names no R prerequisite"),
         ]),
    dict(index=2, type="Variant A", label="[regression] Triage 21 planted-defect BAMs + 2 controls + 9 real BAMs: quickcheck vs samtools view -c vs Picard vs the CI one-liner (and the validators)",
         executed=True,
         execution_note="First auditor's generator (make_fixtures.py, seed 42) re-run to rebuild the 23 SYNTHETIC files from real reads; matrix.py ran six checks on 32 files; summarize_matrix.py counted.",
         note="The detection table reproduces exactly: quickcheck 3/21, samtools view -c 3/21, Picard 18/21, CI one-liner 6/21, with the same named Picard misses. No tool flags the 2 controls. Picard also flags 4 valid real files; the noise note names 3 causes but not the nanopore BAM's.",
         basic=37, specialized=54,
         assertions=[
             A("The detection table in SKILL.md reproduces on the 21 planted files", P, "quickcheck 3 (no_eof, trunc_tail, no_sq), view -c 3 (trunc, bitflip, CIGAR/SEQ), Picard 18 (misses flag_first_and_second, tlen_mismatch, empty_records), CI one-liner 6"),
             A("No integrity check flags either valid synthetic control, and the CI one-liner passes small valid BAMs", P, "ctl_valid and single_end_like: 0 flags in all six checks; one-liner rc 0 on 100/200/500/5,642-read valid BAMs (first audit: rc 1 on the small ones)"),
             A("For every file the validators' printed verdict agrees with their exit status (0 pass/warn, 1 fail, 2 unreadable)", P, "32/32 files, 0 disagreements for python and shell; rc 2 on no_eof, trunc_tail, bitflip, CIGAR mismatch, empty"),
             A("The 'Picard noise on valid files' note covers every valid real file Picard flags", F, "flags 4 valid files; the note lists MATE_NOT_FOUND, MISSING_TAG_NM, RECORD_OUT_OF_ORDER but not the valid nanopore BAM's HEADER_RECORD_MISSING_REQUIRED_TAG 3, INVALID_TAG_NM 22, MISSING_PLATFORM_VALUE 3"),
             A("The validators do not present themselves as integrity checks", P, "they print PASS on drop_block_mid, orphans, flag_first_and_second; SKILL.md's table and text say QC scripts do not see these and route them to quickcheck / Picard / md5sum"),
         ]),
    dict(index=3, type="Variant B", label="[regression + new] Sequence-dictionary (SN / LN / M5) identity check of a BAM against its reference, incl. renamed, swapped, masked and real-data contig-name traps",
         executed=True,
         execution_note="SKILL.md block 03 extracted verbatim and run on 15 BAM/reference pairs (first auditor's 7 + 8 new: LN off by one, superset reference, sarscov2 MT192765.1 vs MN908947.3, 1000G 3,366-contig header vs slice FASTA, spaced path) - test_snippets.sh T03.",
         note="All 15 pairs give the right exit status and message. The first audit's failures (false alarm on BAMs without M5, blind to renames and M5 swaps) are fixed.",
         basic=38, specialized=55,
         assertions=[
             A("The seven first-audit cases are now right", P, "exact rc 0; soft-masked rc 0; hard-masked 'M5 DIFFERS' rc 1; one base 'M5 DIFFERS' rc 1; renamed 'NOT IN REFERENCE: chr22' rc 1; two swapped M5s both reported rc 1; real BAM without M5 vs its FASTA rc 0"),
             A("New length and superset cases: LN off by one is reported, a superset reference is not a difference", P, "'LENGTH DIFFERS: chr22 40001 vs 40002' rc 1; extra reference contig rc 0"),
             A("Real-data contig-name traps are caught", P, "sarscov2 PE BAM (MT192765.1) vs MN908947.3.fasta: NOT IN REFERENCE rc 1; vs its own genome.fasta rc 0; 1000G 3,366-contig BAM vs a chr20 slice FASTA rc 1"),
             A("A BAM without M5 gets the honest notice instead of a false alarm", P, "'no M5 in BAM header: only names and lengths were compared' printed on the human, nanopore and sarscov2 BAMs, rc 0"),
             A("A quoted reference path containing a space works", P, "rc 0 with 'ref exact.fa'"),
         ]),
    dict(index=4, type="Edge", label="[regression + new] Non-standard and broken inputs to both validators: SE, nanopore, empty, all-unmapped, all-secondary, unindexed, SAM, CRAM, missing, truncated, junk, spaces",
         executed=True,
         execution_note="test_validators2.sh, test_validators3.sh, matrix.py, test_cram_sh.sh. CRAM run three ways: reference unresolvable (real nf-core CRAM whose UR points nowhere), REF_PATH md5 cache built from the FASTA, embed_ref CRAM.",
         note="Every unreadable input now gives rc 2 with 1-3 stderr lines and no traceback; all-unmapped rc 1; unindexed, SAM, gzipped SAM and spaced paths work. CRAM with an unresolvable reference: python rc 2 (right), shell prints a blank Mean MAPQ and 'FAIL: Mean MAPQ' rc 1 (wrong cause).",
         basic=32, specialized=49,
         assertions=[
             A("Empty, zero-byte, missing, directory, random bytes, truncated, bit-flipped and CIGAR/SEQ-mismatch inputs give rc 2 with a short message and no traceback", P, "python and shell both rc 2 on all eight; stderr 1-4 lines (first audit: rc 0 with blank metrics from the shell scripts, ZeroDivisionError / ValueError tracebacks from the python one)"),
             A("All-unmapped, all-secondary, single-end, nanopore, name-sorted and unsorted-UMI BAMs are handled", P, "all-unmapped BAM 'FAIL: Mapping rate' rc 1; all-secondary rc 2 'no primary records'; the rest rc 0 with rates equal to flagstat; unindexed BAMs need no index; path with spaces rc 0"),
             A("SAM and gzipped SAM give correct numbers", P, "99.96% mapped, rc 0, both validators"),
             A("A CRAM whose reference cannot be resolved is reported as unreadable (rc 2) by both validators", F, "python rc 2; validate_alignment.sh prints 'Mean MAPQ: ' (blank, awk division by zero swallowed) and 'FAIL: Mean MAPQ' rc 1; with a REF_PATH cache or embed_ref both give 99.96% rc 0"),
             A("Both validators return the same exit status on every edge input", F, "no_sq_unmapped.bam (valid unaligned BAM): python rc 1 (0.00% mapped), shell rc 2 (quickcheck: no @SQ); unresolvable CRAM: python 2, shell 1"),
         ]),
    dict(index=5, type="Stress", label="[regression + new] Strand per chromosome, MAPQ, per-chromosome density and aneuploidy on a 3,366-contig BAM, an RNA BAM and synthetic idxstats; speed on a 5.6M-read BAM",
         executed=True,
         execution_note="SKILL.md blocks 12-17 verbatim (test_snippets.sh T08/T09) under gawk and mawk; big1000.bam built by samtools cat of the real human BAM x1000 (5,644,000 records, 171 MB) and deleted; test_validators2.sh section G.",
         note="The first audit's crashes are gone: no bc 'Divide by zero', no awk division by zero on the '*' line, gawk and mawk agree. Python validator 18.5 s and 149 MB on 5.6M reads; shell validator 124 s (11x flagstat).",
         basic=36, specialized=54,
         assertions=[
             A("Per-chromosome strand loop lists the chromosomes that have reads and prints no error", P, "human slice 'chr22 ... 0.500'; 1000G slice 'chr20 F=4778 R=4779 0.500'; RNA BAM after samtools index 'chr22 F=3521 R=3521 0.500'"),
             A("idxstats density awk survives the '*' line and zero-length contigs", P, "'chr22 0.1410', stderr empty"),
             A("Aneuploidy awk is identical under gawk 5.4.1 and mawk and excludes alt / chrX / unplaced contigs", P, "1000G slice chr20 1.000 under both; synthetic idxstats -> chr1 1.000, chr2 1.000, chr3 1.500"),
             A("Mean MAPQ helper equals pysam over mapped primary reads", P, "59.989 over 5640 reads on both sides"),
             A("The whole-file python default stays practical on a large BAM and gives the exact rate", P, "1.13M reads 4.1 s / 62 MB, 5.64M reads 18.5 s / 149 MB, both '99.96%' = flagstat; shell 24 s and 124 s"),
         ]),
    dict(index=6, type="Scope Boundary", label="[regression + new] Contamination / sample-swap and GC-bias commands: VerifyBamID2, somalier, Picard CrosscheckFingerprints on my own 60-site synthetic data, Picard/deepTools GC bias",
         executed=True,
         execution_note="test_fingerprint.sh, test_vb2.sh, test_picard_noR.sh on data/fp (make_fp_fixtures.py: 60 sites and genotype patterns planted by rewriting bases of the real human PE reads; haplotype map + sites VCF built here; SYNTHETIC, independent of the fixer's 40 sites). VerifyBamID2 on the real 1000G slice.",
         note="With well-formed files the Crosscheck and somalier blocks behave as the Skill says (8/8 Crosscheck checks; somalier relatedness 1.0 vs -2.0). New: two BAMs that share a read group ID/PU collapse into one group, a true swap prints EXPECTED_MATCH and exits 0.",
         basic=31, specialized=46,
         assertions=[
             A("VerifyBamID2 with the '.dat' prefix reaches the marker check and stops with 'Insufficient Available markers'; without '.dat' it fails to open the .bed; no FREEMIX value is claimed", P, "2 of 10,000 markers shared with the slice, rc 1; wrong prefix 'Open file ...vcf.gz.bed failed, exit!'"),
             A("somalier extract + relate --infer on the planted genotypes give the documented separation", P, "IND_A vs IND_A2 relatedness 1.000, concordance 1.000, ibs0 0; IND_A vs IND_B relatedness -2.000, concordance 0.000, ibs0 20"),
             A("Picard CrosscheckFingerprints reproduces the Skill's tumor/normal text on files with unique read groups", P, "different SM same genotypes UNEXPECTED_MATCH rc 1; EXPECT_ALL_GROUPS_TO_MATCH=true EXPECTED_MATCH rc 0 (LOD 19.3) and, for different individuals, UNEXPECTED_MISMATCH rc 1 (LOD -64.4); same SM + different genotypes UNEXPECTED_MISMATCH rc 1; 3-read file INCONCLUSIVE (LOD 0.27)"),
             A("A true swap is caught by the Skill's command when both BAMs carry the same read-group ID / PU", F, "A_rg1 vs B_rg1 (ID:1 PU:1 in both): one group '1|1' EXPECTED_MATCH LOD 7.7 rc 0, also rc 0 with EXPECT_ALL_GROUPS_TO_MATCH=true; CROSSCHECK_BY=FILE or SAMPLE gives LOD -64.4 and rc 1 under EXPECT_ALL_GROUPS_TO_MATCH; SKILL.md silent"),
             A("The GC-bias outputs contain the columns the Skill's band and text refer to", P, "gc_summary.txt AT_DROPOUT 29.06 / GC_DROPOUT 27.43 (percent); gc_bias_metrics.txt NORMALIZED_COVERAGE; computeGCBias wrote its table and PDF (degenerate on the 40 kb slice, not a tool defect)"),
         ]),
    dict(index=7, type="Adversarial", label="[regression + new] 'Just tell me pass or fail' on BAMs with 30% unmapped reads (unplaced and placed), stranded-looking and singleton-heavy data, and a real RNA BAM",
         executed=True,
         execution_note="matrix.py on lowmap_unplaced, lowmap_placed, strand_all_forward, n_singleton_flood, RNA BAM; test_validators2.sh section C (-n 1000 on the unplaced-tail BAM); out/samples.txt transcripts.",
         note="The first audit's headline defect is fixed: 70.01% mapped now prints 'FAIL: Mapping rate' with rc 1 in both validators (was 'Mapped: 100.0%', 'All metrics within normal range'). -n sampling is biased exactly as documented.",
         basic=37, specialized=55,
         assertions=[
             A("Unplaced-unmapped BAM (true 70.01%) is FAILed with the right rate by both validators", P, "python 'Mapped: 3950 (70.01%)' FAIL rc 1; shell 'Mapped: 3950 / 5642 primary records (70.01%)' FAIL rc 1; flagstat primary 70.01%"),
             A("Placed-unmapped BAM (true 69.99%) is FAILed by both validators", P, "69.99% both, FAIL rc 1"),
             A("Strand-, pairing- and singleton-driven failures are graded FAIL, and a real RNA BAM is not falsely failed", P, "strand_all_forward FAIL: Strand balance rc 1; n_singleton_flood FAIL rc 1; real RNA BAM PASS rc 0 (forward fraction 0.500)"),
             A("The documented -n sampling bias is real and stated", P, "lowmap_unplaced with -n 1000: 'first 1000 primary records', Mapped 100.00%, 'All metrics within normal range' rc 0; SKILL.md and the script header say the unplaced tail is not reached"),
             A("Verdict text stays inside what was measured (QC metrics, not integrity)", P, "corrupt drop_block_mid.bam prints 'All metrics within normal range' - the metrics are in range - and SKILL.md states the QC scripts do not check integrity"),
         ]),
    dict(index=8, type="Variant B", label="[NEW] Planted defects the first auditor did not use, on a different real base (1000 Genomes HG00349 chr20 slice, 3,366-contig header): what quickcheck, samtools view -c, Picard, the CI one-liner and the validators see",
         executed=True,
         execution_note="make_new_fixtures.py (SYNTHETIC, derived from real reads; seed 7) built 11 defect files + 2 valid controls (n_ctl_valid, n_mapq255_all) and n_nm_wrong / n_md_wrong on the human chr22 BAM; matrix_new.py ran every check; samtools calmd confirmed the 40 MD tags really are wrong. A duplicate-@SQ header could not be built (samtools reheader rejects it).",
         note="The Skill's division of labour generalises: quickcheck and view -c find 0/11, the one-liner 1/11, Picard 9/11 (8/11 without R=). Picard misses the shifted MD tag even with R= and the TLEN sign flip, so 'R= enables the NM/MD checks' is half right.",
         basic=34, specialized=50,
         assertions=[
             A("The file-damage checks do not see record-level defects, as the Skill says", P, "quickcheck 0/11, samtools view -c 0/11, CI one-liner 1/11 (all-secondary)"),
             A("Picard finds the record-level defects", P, "9/11 (beyond the slice's own MATE_NOT_FOUND noise): duplicated records MATES_ARE_SAME_END 32, CIGAR 40M10H61M INVALID_CIGAR 30, SO:queryname header RECORD_OUT_OF_ORDER 4639, paired-without-0x40/0x80 warnings 40, all-secondary INVALID_FLAG_NOT_PRIM_ALIGNMENT, singleton flood 2128; mate-on-other-contig and Q120 abort with an ERROR line instead of a summary"),
             A("'R= enables the NM/MD checks' holds", F, "n_nm_wrong: INVALID_TAG_NM 40 only with R=; n_md_wrong (40 MD tags differ from samtools calmd): 'No errors found' even with R="),
             A("The validators grade QC-visible defects and stay quiet on valid data", P, "n_singleton_flood FAIL rc 1 (mapping ~77%, pairing), n_all_secondary rc 2; n_ctl_valid and n_mapq255_all (STAR-style sentinel) PASS rc 0; verdict/rc agree on all 13 files"),
             A("The Skill's stated Picard misses still hold on new data", P, "TLEN sign flipped on 40 pairs: no tool flags it (Picard shows only the slice's MATE_NOT_FOUND noise); the table lists TLEN inconsistency as a Picard miss"),
         ]),
    dict(index=9, type="Scope Boundary", label="[NEW] Threshold ladder: 12 files on real human reads, each aimed at one PASS/WARN/FAIL band of one graded metric, expected verdicts computed independently from the records",
         executed=True,
         execution_note="make_new_fixtures.py Family L (unmap / strip-proper / flip-strand / set-MAPQ on the real human PE reads); expected grades recomputed from the records in the same script with the SKILL.md band table; matrix_new.py compared verdict, rc, per-metric grade lines and printed values for python and shell. Tiny-input, determinism and speed checks from test_validators2/3.",
         note="12/12 for both validators on verdict, exit status, per-metric grades and printed values (mapping 92 WARN / 88 FAIL, pairing 85 WARN / 70 FAIL, strand 0.465 WARN / 0.58 and 0.43 FAIL, MAPQ 45 PASS / 35 WARN / 25 FAIL, WARN+FAIL -> FAIL listing both). Output is deterministic. One-read and two-read BAMs are graded FAIL on strand with no small-sample warning.",
         basic=37, specialized=54,
         assertions=[
             A("Every ladder file gets the expected overall verdict and exit status from both validators", P, "python 12/12, shell 12/12 (WARN -> rc 0, FAIL -> rc 1)"),
             A("Per-metric grade lines and printed values match the independent recomputation", P, "grades match on all 12; values within 0.006 points (mapping, pairing), 0.0006 (strand), 0.06 (MAPQ)"),
             A("A mixed WARN + FAIL file reports both, and the FAIL decides the exit status", P, "'FAIL: Strand balance' and 'WARN: Mapping rate' printed by both, rc 1 (out/samples.txt)"),
             A("Repeated runs are byte-identical", P, "python md5 8a93cdd7 twice, shell ad0da0a6 twice"),
             A("Metrics are not graded on a handful of reads", F, "single-read and two-read BAMs print 'FAIL: Strand balance' rc 1; -n N output carries no bias warning (only the header comment does)"),
         ]),
]

static = {
    "functional_suitability": (9, "Covers integrity, dictionary identity, QC metrics, contamination, insert size, pairing, GC, strand, MAPQ, coverage balance and mismatch; every metric printed by the shipped validators reproduced against flagstat/pysam/Picard. Gaps: no CRAM guidance, 'R= enables NM/MD checks' overstates (MD unchecked), Picard chart commands need R (unsaid), read-group collision in Crosscheck."),
    "reliability": (10, "Both validators: exit 0 pass/warn, 1 fail, 2 unreadable/empty; printed verdict and exit status agree on 57 files; 8 unreadable inputs give rc 2 with a short message. Remaining: shell validator false 'FAIL: Mean MAPQ' rc 1 on a CRAM whose reference is unresolvable; python rc 1 vs shell rc 2 on an unaligned BAM."),
    "performance_context": (6, "SKILL.md 389 lines, usage-guide cut from 268 to 67 with nothing the agent needs lost; single implementation of each check. Shell validator does ~10 passes (124 s on 5.6M reads, 11x flagstat); python keeps every MAPQ in memory (~19 B/read, about 1.9 GB extrapolated to 100M reads)."),
    "agent_usability": (14, "Goal/Approach structure, one threshold table, exit-code contract, honest scope statements, measured detection table. Residual inconsistencies: usage-guide prompts still say 'forward/reverse ratio' while SKILL.md says not to use F/R; no note that Picard charts need R."),
    "human_usability": (6, "Validators need no index, accept spaced paths, SAM and unindexed input. Description still omits the integrity and contamination triggers the body covers; tiny inputs are graded without a warning."),
    "security": (11, "No credentials, no eval/exec, read-only on inputs, shell variables quoted, path with spaces safe. The SKILL.md one-liner templates use unquoted in.bam."),
    "maintainability": (9, "SKILL.md / usage-guide / two examples, no duplicated validator; bands still live in three places (table, python, shell). No shipped test data or expected outputs."),
    "agent_specific": (17, "All five Related Skills exist; deterministic; idempotent; read-only. Escape hatches: rc 2 stops, IGNORE warning with measured effect, assay caveats. Missing: an explicit 'stop if integrity fails' rule and the read-group requirement for swap checks."),
}

recs = [
    dict(priority="P2", title="Crosscheck misses a swap when both BAMs share RG ID/PU", observed_in=[6],
         problem="With the Skill's CrosscheckFingerprints command, two BAMs that both carry read group ID:1 PU:1 collapse into one group: RESULT EXPECTED_MATCH, LOD 7.7, exit 0, also with EXPECT_ALL_GROUPS_TO_MATCH=true, although the genotypes differ at every planted site.",
         root_cause="Picard groups by read group by default and the added tumor/normal block does not say the two BAMs need distinct read-group IDs / PUs.",
         fix="Add CROSSCHECK_BY=FILE (or give each BAM a unique RG ID and PU) to the tumor/normal command and one sentence on the collapse; measured: CROSSCHECK_BY=FILE LOD -64.4, rc 1 under EXPECT_ALL_GROUPS_TO_MATCH=true."),
    dict(priority="P2", title="Picard chart commands need R; Skill never says so", observed_in=[1, 6],
         problem="CollectInsertSizeMetrics H= and CollectGcBiasMetrics CHART= exit 1 and leave no metrics file when Rscript is missing ('R is not installed on this machine...'). SKILL.md lists no R prerequisite.",
         root_cause="Version Compatibility names samtools, picard, pysam, matplotlib, numpy only.",
         fix="Add R to the install line, or say the chart options need Rscript and that omitting H= / CHART= still writes the metrics (measured: CollectInsertSizeMetrics without H= wrote its metrics file)."),
    dict(priority="P2", title="validate_alignment.sh prints FAIL, rc 1 on unreadable CRAM", observed_in=[4],
         problem="On a CRAM whose reference cannot be resolved the mean-MAPQ pipeline fails silently: 'Mean MAPQ: ' is blank and the verdict is 'FAIL: Mean MAPQ' with exit 1 (should be 2). The python validator returns rc 2.",
         root_cause="samtools view -c never decodes bases, so the quickcheck and count preconditions pass; the later `samtools view | awk` errors are not checked.",
         fix="Decode once up front (samtools view -c on the CRAM with the reference, or check the exit status of the MAPQ pipeline) and exit 2; or state that CRAM needs REF_PATH / -T."),
    dict(priority="P2", title="'R= enables the NM/MD checks' overstates Picard", observed_in=[8],
         problem="With R=, ValidateSamFile reported INVALID_TAG_NM 40 for the inflated NM tags but 'No errors found' for 40 shifted MD tags that samtools calmd shows are wrong.",
         root_cause="The comment on the ValidateSamFile line was written for NM only.",
         fix="Write '(R= enables the NM check)' and point to samtools calmd for MD."),
    dict(priority="P2", title="usage-guide still says forward/reverse ratio", observed_in=[],
         problem="Three example prompts and step 4 of 'What the Agent Will Do' still ask for the forward/reverse ratio; SKILL.md says the 0.48-0.52 quantity is the forward fraction and warns against F/R.",
         root_cause="The strand section was corrected in SKILL.md and the scripts but the guide's wording was not.",
         fix="Replace 'forward/reverse strand ratio' by 'forward fraction F/(F+R)' in the guide."),
    dict(priority="P2", title="Picard noise note is incomplete", observed_in=[2],
         problem="The valid nanopore BAM draws HEADER_RECORD_MISSING_REQUIRED_TAG 3, INVALID_TAG_NM 22 and MISSING_PLATFORM_VALUE 3 from Picard; the note lists only MATE_NOT_FOUND, MISSING_TAG_NM and RECORD_OUT_OF_ORDER.",
         root_cause="The note was drawn from short-read data.",
         fix="Add one clause: long-read BAMs also draw header (@RG PL / required tag) and NM-convention errors."),
    dict(priority="P2", title="Validators grade tiny inputs and disagree on edge files", observed_in=[4, 9],
         problem="One- and two-read BAMs print 'FAIL: Strand balance' rc 1 with no small-sample note; -n output has no bias warning; python rc 1 vs shell rc 2 on an unaligned BAM without @SQ.",
         root_cause="No minimum-n guard and no shared precondition between the two implementations.",
         fix="Print 'too few reads to grade strand/pairing (n<...)' instead of a grade below a threshold n, print the -n bias warning in the output, and make both scripts treat a no-@SQ BAM the same way."),
    dict(priority="P2", title="Cost of the whole-file default", observed_in=[5],
         problem="The python validator keeps every mapped read's MAPQ in a list (149 MB at 5.6M reads, ~1.9 GB extrapolated to 100M) and the shell validator makes ~10 passes (124 s at 5.6M reads).",
         root_cause="Metrics computed from full lists rather than counters; one samtools call per metric.",
         fix="Use counters for MAPQ and insert size, and take shell counts from one `samtools flagstat` / `stats` pass."),
    dict(priority="P2", title="Description omits integrity and contamination triggers", observed_in=[],
         problem="The frontmatter description names metrics only; the body also covers file integrity, dictionary identity, contamination and sample swap.",
         root_cause="Description not updated when those sections were added.",
         fix="Add 'BAM integrity, reference dictionary match, contamination / sample swap' to the description."),
]

key_strengths = [
    "Both example validators now keep the contract they state: 0 pass/warn, 1 fail, 2 unreadable/empty; printed verdict and exit status agree on 57 test files, and 12/12 ladder files match an independent recomputation of every band.",
    "The first audit's headline defect is fixed and stays fixed under new data: 70% mapped with unplaced reads now FAILs with the exact flagstat rate (was 100.0%, 'All metrics within normal range').",
    "The measured detection table is honest: quickcheck 3/21, samtools view -c 3/21, Picard 18/21, CI one-liner 6/21 all reproduced, and the same picture (quickcheck 0, view -c 0, Picard 9 of 11, one-liner 1) holds on 11 new defects on a different real BAM (Picard 9/11, quickcheck and view -c 0/11, one-liner 1/11).",
    "Every SKILL.md block that can run here ran and matched an independent method (40/40 assertions); dictionary check catches renames, swapped M5s and real contig-name traps and says when M5 is absent.",
    "usage-guide cut from 268 to 67 lines with no agent-relevant loss; the deleted peddy / ATACseqQC mentions are gone.",
]

# ---------------------------------------------------------------- arithmetic
for it in inputs:
    it["total"] = it["basic"] + it["specialized"]
    n_p = sum(1 for a in it["assertions"] if a["result"] == P)
    it["assertions_passed"], it["assertions_total"] = n_p, len(it["assertions"])
    assert 3 <= len(it["assertions"]) <= 5
    it["status"] = "COMPLETED"
    it["status_flag"] = "\u2705" if it["total"] >= 75 else "\u26a0\ufe0f"
n = len(inputs)
exec_avg = round(sum(i["total"] for i in inputs) / n, 1)
static_sub = sum(v[0] for v in static.values())
assert static_sub == 82, static_sub
static_w = round(static_sub * 0.4, 1)
dyn_w = round(exec_avg * 0.6, 1)
score = int(round(static_w + dyn_w))
passed = sum(i["assertions_passed"] for i in inputs)
total_as = sum(i["assertions_total"] for i in inputs)
l1 = round(sum(i["basic"] for i in inputs) / n, 1)
l2 = round(sum(i["specialized"] for i in inputs) / n, 1)
rate = round(100 * passed / total_as, 1)
band = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
grade = band
if band == "Production Ready" and rate < 90:
    grade = "Limited Release"
symbols = {"Production Ready": "\u2b50", "Limited Release": "\u2705", "Beta Only": "\u26a0\ufe0f", "Reject": "\u274c"}
print(f"static {static_sub} exec {exec_avg} static_w {static_w} dyn_w {dyn_w} score {score} band {band} grade {grade} assertions {passed}/{total_as} = {rate}% L1 {l1} L2 {l2}")

floors_note = (f"Weighted score {static_w + dyn_w:.1f} rounds to {score} ({band} band). Floors for Production Ready: static {static_sub} >= 80 met; execution {exec_avg} >= 85 met; "
               f"Layer 1 avg {l1} >= 32 met; Layer 2 avg {l2} >= 48 met; assertion pass rate {passed}/{total_as} = {rate}% is below the 90% floor, so the grade is downgraded exactly one tier to {grade} "
               f"(scoring_rubric section 5); {rate}% is above the Limited Release floor of 80%. No veto fired; no P0 or P1 open.")

meta = {
    "skill_name": SKILL,
    "description": "Validate alignment quality with insert size distribution, proper pairing rates, GC bias, strand balance, and other post-alignment metrics. Use when verifying alignment data quality before variant calling or quantification.",
    "evaluated_on": "2026-09-20",
    "evaluator_version": "skill-auditor@1.0",
    "category": "Data Analysis",
    "execution_mode": "D",
    "complexity": "Complex",
    "n_inputs": n,
    "source": SRC,
    "audit_type": "re-audit of a fixed Skill (third agent: not the first auditor, not the fixer)",
    "pre_fix_score": 66,
    "pre_fix_grade": "Beta Only",
    "pre_fix_static": 67,
    "pre_fix_execution_avg": 65.7,
    "executed": f"{n}/{n}",
    "inputs_note": "Inputs 1-7 are the first audit's seven inputs re-run as regression tests (its 21 planted-defect BAMs regenerated with its own make_fixtures.py, seed 42), each widened with checks the first audit never made; inputs 8 and 9 are new (11 planted defects on a different real base, and a 12-file threshold ladder with independently computed expected verdicts). n_inputs is 9 as in the two earlier re-audits (the schema's 1-8 hint is not enforced).",
    "environment": "WSL science env alignment-files via wsl_run.sh: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14, numpy 2.5.3, Picard 3.5.0 (af-picard3), VerifyBamID2 2.0.3, somalier 0.3.5, deepTools 4.0.0, RSeQC 5.0.4, gawk 5.4.1 + mawk 1.3.4. Real data from audit-envs/alignment-files/public-data (read, never written): human chr22-slice PE / name-sorted / RNA / UMI / CRAM, 1000G HG00349 chr20 slice with 3,366 contigs, ARTIC nanopore, SARS-CoV-2 Illumina PE/SE, planted_dups. Skill copied from worktree af-valid @ f9307f4 into run/skill (byte-identical, diff -r); nothing written to the worktree or external clones; 0 __pycache__.",
    "checks_run": "matrix.py: 32 files x 6 checks; matrix_new.py: 13 new planted files x 5 checks + 12 ladder files x 2 validators; test_snippets.sh: every runnable SKILL.md block (40 assertions, 40 pass); test_validators2/3.sh: odd inputs, CRAM x3, -n bias, speed on 1.1M and 5.6M reads, determinism; test_fingerprint.sh: 8 Crosscheck cases + 4 RG-collision cases, somalier extract x4 + relate, VerifyBamID2 x2; test_picard_misc.sh / test_picard_noR.sh: IGNORE recipe, noise on valid files, R dependency; test_infer_experiment.sh; static: ast.parse and bash -n on the examples.",
    "regression_result": "All 7 first-audit P1 defects and the P2s the fixer addressed are fixed by my runs: validators exit 0/1/2 with a verdict (was exit 0 always, no verdict); 70% mapped -> FAIL 70.01% (was 100.0%); 99.96% prints 99.96% (was 90.0% / 99.00%); strand printed as forward fraction 0.500 (was F/R 1.0007); M5 snippet: no false alarm, catches renames and swaps; python validator no traceback on empty / all-unmapped / unindexed; CI one-liner passes small valid BAMs.",
    "fix_claims_checked": "Reproduced: detection table 3/3/18/6; IGNORE recipe hides 40 / 2 / 2820 errors; VerifyBamID2 '.dat' prefix and 'Insufficient Available markers'; CrosscheckFingerprints and somalier relate on planted data (my own 60 sites, not the fixer's 40); mapping-rate arithmetic 99.96; peddy and ATACseqQC deleted (grep: 0 hits); plot-bamstats now lives in bio-bam-statistics (exists); all Related Skills exist; usage-guide dedup lost nothing the agent needs (six troubleshooting symptoms condensed into 'When a Metric Fails'). Not reproduced (no data): a real FREEMIX value.",
    "not_executed": "A real FREEMIX estimate (needs a whole-genome or exome BAM; only a 100 kb slice is available); somalier / Crosscheck on a real human haplotype map or sites file (only my synthetic 60 sites); Picard CollectMultipleMetrics / CollectHsMetrics / CollectWgsMetrics and mosdepth (named in the QC table as pointers, no block); CRAM behaviour is tested but not documented by the Skill.",
    "judgements": {
        "veto_calls": "Skill veto PASS: no eval/exec; output byte-identical on repeat; frontmatter valid; every valid input runs; unreadable inputs end in rc 2 with a message. Research veto PASS: no fabricated identifiers or values (every quantitative claim tested reproduced; FREEMIX 0.03 is hedged as 'commonly used'); no diagnostic or prescriptive content; no methodological fallacy (the Crosscheck read-group collapse is a tool trap left unsaid, a P2, not a fallacy); all code parses and the blocks run.",
        "grade_call": "No P0 or P1. Nine P2s. Numeric band Production Ready (85), downgraded one tier by the assertion floor (see floors_note).",
        "fixture_caveats": "All planted defects, genotype patterns and thresholds-ladder files are SYNTHETIC and derived from real reads; labels in run/data/fixtures.json, run/data/new/fixtures_new.json, ladder_truth.json. My assertion in test_snippets.sh first mis-stated quickcheck's exit status (16, not 1) and mis-parsed Picard's summary file; fixed and re-run, 40/40 pass.",
    },
    "floors_note": floors_note,
}

report = {
    "meta": meta,
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated identifiers, values or results; the detection table, thresholds, LOD and relatedness values, timings and error strings quoted in the Skill were reproduced by my own runs. The FREEMIX 0.03 threshold is hedged as commonly used."},
            "practice_boundaries": {"result": "PASS", "detail": "Alignment QC utility; no diagnostic or prescriptive content about a person. Contamination and swap commands report sample-level statistics with thresholds labelled as conventions."},
            "methodological_ground": {"result": "PASS", "detail": "Metric definitions now match their bands (forward fraction, primary-record denominators, mean over mapped reads); assay caveats stated; -n bias stated. The read-group collapse in the Crosscheck block is an unstated tool limitation (P2), not a principled fallacy."},
            "code_usability": {"result": "PASS", "detail": "validate_alignment.py and .sh run from a copy on 57 files with correct output; both parse (ast.parse, bash -n); every runnable SKILL.md block ran (40/40 assertions). Picard chart options need Rscript (P2)."},
        },
    },
    "static_score": {"subtotal": static_sub, "max": 100,
                     "categories": {k: {"score": v[0], "max": m, "note": v[1]} for (k, v), m in zip(static.items(), (12, 12, 8, 16, 8, 12, 12, 20))}},
    "dynamic_score": {"execution_avg": exec_avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total_as}, "inputs": inputs},
    "final": {"static_weighted": static_w, "dynamic_weighted": dyn_w, "score": score, "max": 100, "grade": grade, "grade_symbol": symbols[grade],
              "deployable": True, "veto_override": False},
    "key_strengths": key_strengths,
    "recommendations": recs,
}
# schema checks
assert [c for c in report["static_score"]["categories"]] == ["functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"]
for k, c in report["static_score"]["categories"].items():
    assert 0 <= c["score"] <= c["max"], k
assert len(inputs) == n == meta["n_inputs"]
assert 2 <= len(key_strengths) <= 5
assert [r["priority"] for r in recs] == sorted(r["priority"] for r in recs)
for r in recs:
    assert len(r["title"]) <= 60, r["title"]
(ROOT / f"eval_report_{SKILL}_result.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

# ---------------------------------------------------------------- viewer
L = []
w = L.append
w(f"# Eval Viewer - {SKILL} (re-audit of the fixed Skill)")
w("Generated: 2026-09-20  |  Source: `" + SRC + "`  |  Category: Data Analysis  |  Mode: D  |  Complexity: Complex  |  N = 9\n")
w(f"**Pre-fix 66 (Beta Only, not deployable)  ->  now {score} ({grade}), deployable, no veto, no open P0/P1, 9 P2.**  Executed 9/9.\n")
w("## Summary table\n")
w("| # | Type | Input | Basic /40 | Spec /60 | Total /100 | Assertions | Status |")
w("|---|---|---|---|---|---|---|---|")
for it in inputs:
    w(f"| {it['index']} | {it['type']} | {it['label'][:110]} | {it['basic']} | {it['specialized']} | {it['total']} | {it['assertions_passed']}/{it['assertions_total']} | {it['status_flag']} |")
w(f"\n**Execution average {exec_avg} / 100 (first audit 65.7).  Static {static_sub} / 100 (first audit 67).  Assertion pass rate {passed}/{total_as} = {rate}% (first audit 18/35).**")
w(f"Final = {static_sub} x 0.4 + {exec_avg} x 0.6 = {static_w} + {dyn_w} = {static_w + dyn_w:.1f} -> {score}.  {floors_note}\n")
w("## Vetoes\n")
w("Skill veto PASS (stability, contract, determinism, security). Research veto PASS (integrity, practice boundaries, methodology, code usability). Details in the JSON.\n")
w("## What the fix did, by my runs (not by the fix log)\n")
w("| First-audit defect | Now |")
w("|---|---|")
w("| validators exit 0 on everything, no verdict | python and shell print a verdict, exit 0 pass/warn, 1 fail, 2 unreadable/empty; verdict and rc agree on 57 files |")
w("| 70% mapped (unplaced) prints 100.0%, 'All metrics within normal range' | 70.01% `FAIL: Mapping rate`, rc 1 in both; equals flagstat primary |")
w("| bc truncation: 99.96% printed as 90.0% / 99.00% | 99.96% in both scripts and in the pairing snippet |")
w("| strand printed as F/R 1.0007 against a 0.48-0.52 band | forward fraction 0.500 everywhere |")
w("| M5 diff false alarm without M5, blind to renames and swaps | 15/15 cases right, prints a notice when M5 is absent |")
w("| python validator crashes on empty / all-unmapped / unindexed | rc 2 / rc 1 / runs; no traceback |")
w("| CI one-liner rejects small valid BAMs | rc 0 on 100..5,642-read valid BAMs |")
w("| detection claim unmeasured | table 3 / 3 / 18 / 6 of 21 reproduced exactly; same picture on 11 new defects |\n")
w("## Findings the fix left or introduced (all P2)\n")
for r in recs:
    w(f"- **{r['title']}** - {r['problem']} Fix: {r['fix']}")
w("")
w("## Detailed outputs\n")
detail = {
    1: "```\nvalidate_alignment.py  human/test.paired_end.sorted.bam\n  Mapped: 5640 (99.96%)   Properly paired: 5638 (99.96% of mapped paired reads)\n  Median 123 / Mean 126 / Std 32   Forward fraction F/(F+R): 0.500   Mean MAPQ: 60.0\n  Mapping rate: PASS  Proper pairing: PASS  Strand balance: PASS  Mean MAPQ: PASS   All metrics within normal range   [exit 0]\nvalidate_alignment.sh: Mapped: 5640 / 5642 primary records (99.96%)  ... same grades  [exit 0]\nPicard CollectInsertSizeMetrics median 123; CollectAlignmentSummaryMetrics PAIR PCT_PF_READS_ALIGNED 0.999646 PF_MISMATCH_RATE 0.001997 STRAND_BALANCE 0.5\nno Rscript on PATH: CollectInsertSizeMetrics H=  -> rc 1, no metrics file: 'R is not installed on this machine. It is required for creating the chart.'\n```",
    2: "```\n                       caught /21   flags on 2 controls   flags on 9 real valid files\nquickcheck             3            0                     0\nsamtools view -c       3            0                     0\nPicard ValidateSamFile 18           0                     4 (name-sorted, RNA, 1000G slice, nanopore)\nCI one-liner           6            0                     0\nvalidators (rc != 0)   9            0                     0\nPicard misses: flag_first_and_second, tlen_mismatch, empty_records.  Validators' 9 = QC-visible (2 lowmap, strand, empty, no_eof, trunc, bitflip, CIGAR, no_sq).\n```",
    3: "```\nBAM(M5) vs ref_exact          rc 0            | vs ref_softmask   rc 0\nvs ref_hardmask               M5 DIFFERS rc 1 | vs ref_onebase    M5 DIFFERS rc 1\nvs ref_renamed (22)           NOT IN REFERENCE: chr22 rc 1\ntwo M5s swapped               M5 DIFFERS: chrA / chrB rc 1\nreal human BAM (no M5)        no M5 in BAM header: only names and lengths were compared  rc 0\nref one base longer           LENGTH DIFFERS: chr22 40001 vs 40002 rc 1 | superset ref rc 0\nsarscov2 PE (MT192765.1) vs MN908947.3.fasta  NOT IN REFERENCE rc 1\n```",
    4: "```\n[missing] rc 2 | [zero-byte] rc 2 'ERROR: cannot read zero.bam completely: file does not contain alignment data' | [directory] rc 2 | [random bytes] rc 2\n[SAM] py rc 0 99.96% | sh rc 0 99.96%   [path with spaces] rc 0 both   [-n -5] rc 2 'no primary records'\nCRAM, reference unresolvable: py rc 2 'cannot read ... truncated file'; sh:  Mean MAPQ:  (blank)  -> 'FAIL: Mean MAPQ' rc 1   (awk: division by zero attempted)\nCRAM with REF_PATH md5 cache or embed_ref: both rc 0, 99.96%\nno_sq_unmapped.bam: py rc 1 (FAIL 0.00% mapped)  sh rc 2 (quickcheck)\n```",
    5: "```\nloop: chr22: F=2820 R=2820 forward fraction=0.500 | chr20: F=4778 R=4779 0.500 | RNA (indexed copy): chr22 F=3521 R=3521 0.500\nMean MAPQ: 59.989 (pysam 59.989, n=5640)   density: chr22 0.1410\naneuploidy gawk == mawk: chr20 1.000;   synthetic: chr1 1.000 chr2 1.000 chr3 1.500 (alt, chrX, * excluded)\nspeed: 1,128,800 reads py 4.1 s 62 MB, sh 24.4 s | 5,644,000 reads py 18.5 s 149 MB, sh 124.0 s | flagstat alone 1.8 s / 10.8 s\n```",
    6: "```\nCrosscheck (unique RG):  A vs A2 (different SM, same genotype)  UNEXPECTED_MATCH  LOD 19.3  rc 1\n                         A vs A2 EXPECT_ALL_GROUPS_TO_MATCH=true  EXPECTED_MATCH rc 0\n                         A vs B (different genotypes)  EXPECTED_MISMATCH  LOD -64.4 rc 0 ; with EXPECT_ALL_GROUPS_TO_MATCH=true UNEXPECTED_MISMATCH rc 1\n                         A vs L (3 reads)  INCONCLUSIVE LOD 0.27\nCrosscheck (both BAMs ID:1 PU:1):  '1|1 EXPECTED_MATCH' LOD 7.69 rc 0 (also with EXPECT_ALL_GROUPS_TO_MATCH=true, rc 0)\n                         CROSSCHECK_BY=FILE: EXPECTED_MISMATCH LOD -64.35 rc 0; with EXPECT_ALL_GROUPS_TO_MATCH=true UNEXPECTED_MISMATCH rc 1; CROSSCHECK_BY=SAMPLE same\nsomalier relate --infer: IND_A/IND_A2 relatedness 1.000 concordance 1.000 ibs0 0 | IND_A/IND_B -2.000 concordance 0.000 ibs0 20\nVerifyBamID2 --SVDPrefix ...vcf.gz.dat: 'Number of marker shared with input file:2 ... Insufficient Available markers' rc 1; prefix without .dat: 'Open file ...vcf.gz.bed failed, exit!'\n```",
    7: "```\nlowmap_unplaced (true 70.01%): py 'Mapped: 3950 (70.01%)'  FAIL: Mapping rate  [exit 1]   sh 'Mapped: 3950 / 5642 primary records (70.01%)'  [exit 1]\nlowmap_placed (true 69.99%): FAIL rc 1 both     strand_all_forward FAIL: Strand balance rc 1     n_singleton_flood FAIL rc 1     RNA BAM PASS rc 0\n-n 1000 on lowmap_unplaced: '=== Alignment Validation (first 1000 primary records) ===' Mapped: 1000 (100.00%) All metrics within normal range rc 0  (documented bias)\n```",
    8: "```\nnew defect (1000G base)      quickcheck view-c  CI  Picard         validators\nn_dup_records                 -          -       -   MATES_ARE_SAME_END 32 ...  -\nn_cigar_H_middle              -          -       -   INVALID_CIGAR 30           -\nn_hd_queryname_but_coord      -          -       -   RECORD_OUT_OF_ORDER 4639   -\nn_no_mate_flags               -          -       -   PAIRED_READ_NOT_MARKED... 40  -\nn_mate_other_chrom            -          -       -   aborts: Value was put into PairInfoMap more than once   -\nn_qual_out_of_range           -          -       -   aborts: Cannot encode phred score: 120   -\nn_singleton_flood             -          -       -   INVALID_FLAG_MATE_UNMAPPED 2128   FAIL rc 1\nn_all_secondary               -          -       rc1 INVALID_FLAG_NOT_PRIM_ALIGNMENT 38   rc 2\nn_tlen_same_sign              -          -       -   (only slice noise MATE_NOT_FOUND 59)   -\nn_nm_wrong (human)            -          -       -   INVALID_TAG_NM 40 (needs R=)   -\nn_md_wrong (human)            -          -       -   'No errors found' even with R=   -\ncontrols n_ctl_valid, n_mapq255_all: validators PASS rc 0; Picard MATE_NOT_FOUND 59 (region-slice noise, documented)\ncounts: quickcheck 0/11, view -c 0/11, CI 1/11, Picard 9/11 (8/11 never R=; misses n_md_wrong, n_tlen_same_sign), validators 2/11\n```",
    9: "```\nfile                 truth   py           sh\nlad_all_pass         PASS    PASS rc0     PASS rc0\nlad_map_92           WARN    WARN rc0     WARN rc0     (91.95%)\nlad_map_88           FAIL    FAIL rc1     FAIL rc1     (87.98%)\nlad_pair_85          WARN    WARN rc0     WARN rc0\nlad_pair_70          FAIL    FAIL rc1     FAIL rc1\nlad_strand_465       WARN    WARN rc0     WARN rc0\nlad_strand_58 / _43  FAIL    FAIL rc1     FAIL rc1\nlad_mapq_45 / 35 / 25 PASS / WARN / FAIL   matched by both\nlad_warn_plus_fail   FAIL    'FAIL: Strand balance' + 'WARN: Mapping rate' rc 1 (both)\none-read / two-read BAMs: 'FAIL: Strand balance' rc 1 (no small-sample note)\n```",
}
for it in inputs:
    w(f"### Input {it['index']} - {it['type']}\n")
    w(f"**Prompt / test:** {it['label']}\n")
    w(f"**Executed:** {it['executed']}. {it['execution_note']}\n")
    w("**Output (trimmed):**\n")
    w(detail[it["index"]] + "\n")
    w(f"**Note:** {it['note']}\n")
    w(f"**Scores:** Basic {it['basic']}/40 | Specialized {it['specialized']}/60 | Total {it['total']}/100\n")
    w("**Assertions:**")
    for a in it["assertions"]:
        w(f"- [{a['result']}] {a['text']} - {a['note']}")
    w("")
w("## Static score\n")
w("| Category | Score | Note |")
w("|---|---|---|")
for k, c in report["static_score"]["categories"].items():
    w(f"| {k} | {c['score']}/{c['max']} | {c['note']} |")
w(f"\n**Static subtotal {static_sub}/100.**\n")
w("## Recommendations\n")
for r in recs:
    w(f"**[{r['priority']}] {r['title']}**  (observed in {r['observed_in'] or 'static reading'})  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
w("## Not executed / not verified\n")
w(meta["not_executed"] + "\n")
w("## Reproduce\n")
w("`run/scripts/` in order: `00_setup.sh` (first auditor's fixtures), `01_new_fixtures.sh`, `02_fp_build.sh`, `matrix.py`, `matrix_new.py`, `summarize_matrix.py`, `test_snippets.sh`, `test_validators2.sh`, `test_validators3.sh`, `test_cram_sh.sh`, `test_fingerprint.sh`, `test_vb2.sh`, `test_picard_misc.sh`, `test_picard_noR.sh`, `test_infer_experiment.sh`, `05_samples.sh`, `build_report.py`; `explore_*.sh` are the discovery runs. Outputs in `run/out/`. Run WSL scripts through `F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-validation/run/scripts/<file>.sh'`.\n")
(ROOT / f"eval_viewer_{SKILL}.md").write_text("\n".join(L), encoding="utf-8")
print("written")
