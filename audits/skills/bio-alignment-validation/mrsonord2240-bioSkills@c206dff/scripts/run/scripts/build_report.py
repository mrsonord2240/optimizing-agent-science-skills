"""Assemble eval_report_bio-alignment-validation_result.json and run the schema Pre-Emit Checklist. Windows python, utf-8."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL = "bio-alignment-validation"

A = lambda t, r, n: {"text": t, "result": r, "note": n}
ENV = "executed in WSL science env alignment-files (samtools 1.24, pysam 0.24.1, Picard 3.5.0, deepTools 4.0.0, verifybamid2 2.0.3, somalier 0.3.5); scripts in run/scripts, stdout in run/out"

inputs = [
    dict(index=1, type="Canonical",
         label="Full QC of a real paired-end human BAM before variant calling (shipped validators + SKILL.md snippets vs Picard/pysam truth)",
         status="COMPLETED", status_flag="⚠️",
         note="Python validator and Picard/pysam numbers correct (mapping 99.96%, insert median 123, strand 0.500, mismatch 0.0020); the bash helpers print wrong percentages (SKILL.md script 99.00%, shipped validate_alignment.sh 90.0% for 5642/5644 mapped) and the bash strand ratio (F/R 1.0007) cannot be compared with the 0.48-0.52 table.",
         basic=29, specialized=44,
         assertions=[
             A("Every helper prints a mapping rate within 0.5 pt of the truth (99.96%)", "FAIL", "SKILL.md script 99.00%, validate_alignment.sh 90.0% (bc scale truncation before the *100); only validate_alignment.py 100.0% is within tolerance"),
             A("Insert-size median from the Skill's samtools-stats, Picard and pysam routes agree", "PASS", "Picard median 123, pysam median 123, IS-table mean 124.8 vs pysam 125.6 (inward pairs only)"),
             A("Strand-balance number the snippet prints is comparable to the 0.48-0.52 'Good' band", "FAIL", "SKILL.md 'Calculate Strand Ratio' and validate_alignment.sh print F/R = 1.0007; the band is a forward fraction (Python prints 0.500)"),
             A("Picard CollectAlignmentSummaryMetrics command runs verbatim and its named columns exist", "PASS", "rc 0; PCT_PF_READS_ALIGNED 0.9996, PF_MISMATCH_RATE 0.001997 (samtools stats error rate 2.015e-3), STRAND_BALANCE 0.5"),
             A("Output is deterministic and makes no diagnostic or clinical claim", "PASS", "identical md5 of stdout on two runs of both example validators; QC-only content"),
         ]),
    dict(index=2, type="Variant A",
         label="Triage 21 planted-defect BAMs (synthetic) + 9 real valid files: quickcheck vs ValidateSamFile vs the CI one-liner",
         status="COMPLETED", status_flag="✅",
         note="Skill's division of labour is right and its commands work verbatim (quickcheck rc 16, -v fofn lists exactly the failing files, ValidateSamFile legacy KEY=VALUE syntax and IGNORE names valid in Picard 3.5.0). Detection of 21 planted defects: quickcheck 3, full decode 3, CI one-liner 6, Picard 18. Two problems: the CI one-liner rejects valid 100-, 200- and 500-read BAMs (hard-coded 1000), and the 'production' IGNORE pair turns 2 planted defects into 'No errors found'.",
         basic=32, specialized=49,
         assertions=[
             A("quickcheck catches EOF-less / tail-truncated files and the '-v > fofn' snippet lists exactly those", "PASS", "no_eof.bam and trunc_tail.bam rc 16, fofn = those two names only"),
             A("ValidateSamFile catches record-level defects quickcheck misses (orphans, mate fields, flags, unsorted, CIGAR/SEQ, RG)", "PASS", "18/21 planted defects flagged, e.g. MATE_NOT_FOUND=60, MISMATCH_MATE_ALIGNMENT_START=50, RECORD_OUT_OF_ORDER=2785, MISMATCH_CIGAR_SEQ_LENGTH=30; missed first-and-second flags, TLEN mismatch, empty file"),
             A("The Skill's own caveat that quickcheck misses mid-file damage is accurate", "PASS", "bitflip_mid.bam and drop_block_mid.bam (273 reads silently lost) both pass quickcheck; decode fails only the bit-flip"),
             A("The 'Production: ignore expected-but-noisy' Picard command does not hide real defects", "FAIL", "with IGNORE=INVALID_MAPPING_QUALITY IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND the flag_mate_neg_strand (40 reads), strand_all_forward (2820) and unmapped_mapq60 fixtures all print 'No errors found'"),
             A("The CI-safe one-liner accepts valid BAMs", "FAIL", "rejects three valid real BAMs of 100/200/500 reads (rc 1, 'BAM failed integrity') because the count threshold is a fixed 1000"),
         ]),
    dict(index=3, type="Variant B",
         label="Sequence-dictionary (M5) identity check of a BAM against its reference, incl. soft/hard-masked, renamed and mis-assigned contigs",
         status="COMPLETED", status_flag="⚠️",
         note="The diff finds real sequence differences (hard-mask, single base) and correctly ignores soft-masking, matching the Skill's text. It raises a false alarm on BAMs without M5 tags (7 of 8 inspected real BAMs: rc 1 vs their own reference) and cannot see a chr22-vs-22 rename or two contigs whose M5s are swapped (rc 0), although 'chr vs no-chr' is listed as a covered failure mode.",
         basic=28, specialized=40,
         assertions=[
             A("Diff reports 'identical' for identical sequence, incl. lowercase soft-masking", "PASS", "exact and soft-masked references: rc 0, 0 diff lines"),
             A("Diff reports a difference for hard-masked (N) and single-base-changed references", "PASS", "rc 1, 2 diff lines each"),
             A("Diff does not false-alarm when the BAM header has no M5 tags", "FAIL", "real human BAM vs its own genome.fasta: rc 1, 1 diff line; same for the SARS-CoV-2 BAM (7 of the 8 real BAMs inspected carry no M5)"),
             A("Diff detects a contig-name mismatch or mis-assigned M5 (the 'chr vs no-chr' failure mode the text lists)", "FAIL", "SN chr22 vs 22 -> rc 0; chrA/chrB with swapped M5 -> rc 0, because sort discards which M5 belongs to which name"),
             A("samtools dict M5 equals the known reference digest", "PASS", "1922b52e1af6977302717072ebaca0a1 = tooling record for human genome.fasta"),
         ]),
    dict(index=4, type="Edge",
         label="Non-standard inputs: single-end, nanopore/ARTIC, empty, all-unmapped, unindexed, name-sorted, missing, truncated and space-in-path BAMs",
         status="COMPLETED", status_flag="⚠️",
         note="validate_alignment.py handles single-end ('No paired reads') and nanopore, but dies with raw tracebacks on empty and all-unmapped BAMs (ZeroDivisionError) and on any unindexed BAM (ValueError, incl. 2 valid real files). Both bash validators exit 0 on missing/truncated files while printing 'Mapped: / (%)', 'Proper pairing: 0%' for single-end reads, and validate_alignment.sh breaks on a path with a space (44 stderr lines, rc 0).",
         basic=24, specialized=33,
         assertions=[
             A("Python validator completes on single-end and long-read BAMs without inventing pairing metrics", "PASS", "single-end and nanopore: 'No paired reads', 'All metrics within normal range'"),
             A("Empty or all-unmapped BAM gets a readable message rather than a crash", "FAIL", "ZeroDivisionError on both (total=0 / len(mapqs)=0)"),
             A("Unindexed BAM gets an actionable message", "FAIL", "bare 'ValueError: fetch called on bamfile without index'; 6 of 9 real files ship without an index"),
             A("Shell validators signal failure for a missing or truncated BAM", "FAIL", "SKILL.md script and validate_alignment.sh both rc 0 with empty 'Mapping rate: %' lines and 19-50 stderr lines"),
             A("Validators only read the input and write nothing outside the report directory", "PASS", "read-only; SKILL.md script writes qc/report.txt only"),
         ]),
    dict(index=5, type="Stress",
         label="Strand balance per chromosome, MAPQ distribution, per-chromosome coverage / aneuploidy check on a 3,366-contig BAM and an RNA BAM (SKILL.md snippets verbatim)",
         status="COMPLETED", status_flag="⚠️",
         note="Correct: view -s 42.10 and the MAPQ histogram are correct. The per-chromosome loop is hard-coded to chr1-3 and prints bc 'Divide by zero'; the idxstats awk dies on the '*' line (division by zero); the aneuploidy awk needs gawk (mawk: 'function asort never defined'), divides by a zero median on the 1000G slice and leaves 824 of 846 surviving contigs as alt/random scaffolds; mean MAPQ counts unmapped reads (41.995 vs 59.99 on the 30%-unmapped fixture).",
         basic=25, specialized=33,
         assertions=[
             A("'samtools view -s 42.10' subsample is reproducible and keeps mates together", "PASS", "576 reads twice, 0 names without both mates"),
             A("Per-chromosome strand loop runs cleanly on a BAM whose contigs are not chr1-chr3", "FAIL", "invalid-region warnings and 'Runtime error: Divide by zero' for chr1, chr2, chr3 on both BAMs"),
             A("Aneuploidy awk runs under the default awk and on zero-coverage contigs", "FAIL", "mawk: function asort never defined; gawk: fatal division by zero at the END block; regex keeps 824 alt/random contigs"),
             A("MAPQ histogram is exact", "PASS", "2 reads at MAPQ 0 = the 2 unmapped reads; other bins match samtools view"),
             A("Mean-MAPQ helper reports the mean over mapped reads", "FAIL", "includes unmapped MAPQ 0: 41.995 vs 59.99 (lowmap fixture), 59.97 vs 59.99 (human)"),
         ]),
    dict(index=6, type="Scope Boundary",
         label="Contamination / sample-swap and GC-bias checks (Picard GC bias + alignment summary, deepTools computeGCBias, verifybamid2, somalier, CrosscheckFingerprints)",
         status="COMPLETED", status_flag="⚠️",
         note="Executed: Picard CollectGcBiasMetrics and CollectAlignmentSummaryMetrics (rc 0, files written), computeGCBias (rc 0, files written), verifybamid2 (both prefixes; correct prefix stops at 'Insufficient Available markers' on the 100 kb slice), somalier extract (needs a chr1 FASTA, not available). NOT executed end-to-end: somalier relate, CrosscheckFingerprints (no haplotype map; option names and HAPLOTYPE_MAP/I syntax accepted), a real FREEMIX estimate. The verifybamid2 prefix in the Skill (.../1000g.b38.vcf.gz.SVD) matches no released file; the '<1.2x' GC-bias band maps to no Picard column.",
         basic=29, specialized=40,
         assertions=[
             A("Picard CollectGcBiasMetrics and CollectAlignmentSummaryMetrics run verbatim under Picard 3.5.0", "PASS", "legacy KEY=VALUE accepted; gc_bias_metrics.txt, gc_summary.txt, chart PDF and alignment_summary.txt written"),
             A("computeGCBias flags in the Skill exist and run", "PASS", "-b, -g, --effectiveGenomeSize, -o (alias of -freq) and --biasPlot accepted; gc_bias.txt and gc_bias.pdf written"),
             A("verifybamid2 --SVDPrefix example resolves to files of the released panel", "FAIL", "'Open file ...1000g.b38.vcf.gz.SVD.bed failed, exit!' (rc 1); the released prefix ends in .dat (Griffan/VerifyBamID README and repo file names)"),
             A("The 'GC bias < 1.2x / 1.2-1.5x' thresholds can be read off a named output column", "FAIL", "Picard reports AT_DROPOUT/GC_DROPOUT and NORMALIZED_COVERAGE; the Skill names no column or formula for the ratio"),
             A("somalier and CrosscheckFingerprints option names used by the Skill exist in the installed versions", "PASS", "somalier extract -d -s -f, relate --infer confirmed in --help; CrosscheckFingerprints HAPLOTYPE_MAP and repeated I= parsed (fails only on the missing map file)"),
         ]),
    dict(index=7, type="Adversarial",
         label="'Just tell me pass or fail' on a BAM with 30% unmapped reads (unplaced and placed variants) and an RNA BAM",
         status="COMPLETED", status_flag="⚠️",
         note="With 30% of reads unmapped and unplaced (true mapping 70.0%) validate_alignment.py prints 'Mapped: 100.0%' and 'All metrics within normal range', and the usage-guide AlignmentValidator prints 'Mapping rate: 100.0% PASS', because fetch() and get_index_statistics() skip unplaced unmapped reads. The SKILL.md bash script reports 70.00% correctly. When the validator does warn (placed variant) it still exits 0, so a pipeline continues. The RNA BAM gets no blanket verdict; the text warns that thresholds are assay-specific.",
         basic=23, specialized=31,
         assertions=[
             A("Shipped validate_alignment.py flags a BAM whose true mapping rate is 70%", "FAIL", "unplaced-unmapped variant: prints 'Mapped ... (100.0%)' and 'All metrics within normal range' although 1,692 of 5,644 records are unmapped (the placed variant does warn)"),
             A("usage-guide AlignmentValidator flags the same BAM", "FAIL", "prints 'Mapping rate: 100.0% PASS' for the unplaced variant (70.0% FAIL for the placed variant)"),
             A("SKILL.md bash script reports the true mapping rate for the same file", "PASS", "'Mapping rate: 70.00%' for both variants (samtools view -c based)"),
             A("A QC failure is machine-readable (non-zero exit)", "FAIL", "python validator prints 'WARNINGS: Low mapping rate, Low proper pairing' and exits 0; the shell validators print no verdict at all"),
             A("Skill declines to give one blanket verdict for RNA-seq / assay-dependent metrics", "PASS", "strand, proper-pair, insert-size and MAPQ text all state the assay-specific deviations and point to bam-statistics"),
         ]),
]

for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")
    i["executed"] = True
    i["execution_note"] = ENV

static = {
    "functional_suitability": (8, 12, "Covers file integrity, dictionary identity, contamination, insert size, pairing, GC bias, strand, MAPQ, coverage balance and mismatch rate with good caveats. Verified wrong or misleading: bc scale truncation (90.0% for 99.96%), F/R ratio vs 0.48-0.52 band, fetch() blind to unplaced unmapped reads, M5 diff false alarm and blind to names, verifybamid2 prefix, gawk-only awk. No script produces the pass/warn/fail calls its own Approach promises (bash) or covers integrity (python)."),
    "reliability": (5, 12, "CI one-liner and quickcheck advice fail loudly (exit 1) and are correct. The example validators do not: bash scripts exit 0 on missing/truncated input and print blank metrics, the python one crashes with raw tracebacks on empty/unindexed input and exits 0 on WARNINGS. No recovery guidance for these."),
    "performance_context": (4, 8, "SKILL.md ~370 lines is reasonable, but usage-guide repeats roughly half of it (flagstat, pairing, strand, insert-size python, Picard commands, validator class); the comprehensive script scans the BAM 6+ times where one samtools stats pass has the numbers."),
    "agent_usability": (11, 16, "Clear Goal/Approach structure and a useful two-validation table. Inconsistent across files: strand ratio meaning, mean-MAPQ thresholds (>40 table vs 30 script vs 'mean is misleading'), `picard` vs `java -jar picard.jar`, related skills named without the bio- prefix."),
    "human_usability": (5, 8, "Description uses natural phrasing but omits corruption/integrity triggers that the body covers. Scripts are rigid: need an index, break on spaces, give tracebacks."),
    "security": (10, 12, "No credentials, no eval/exec, read-only on inputs. Shell scripts use unquoted $BAM/$OUTDIR (word-splitting, not injection) and do not check the file exists."),
    "maintainability": (8, 12, "Sensible split (SKILL.md, usage-guide, two examples) but thresholds are hard-coded in three places and the usage-guide re-implements the validator; examples ship no test data or expected output."),
    "agent_specific": (16, 20, "Good cross-references (bam-statistics, alignment-filtering, duplicate-handling, sam-bam-basics, chipseq-qc all exist), deterministic, read-only, useful assay caveats. No stop rule such as 'do not proceed if integrity fails'; the ignore-list recipe removes checks without saying when."),
}
sub = sum(v[0] for v in static.values())
assert sub == 67, sub

exec_avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw = round(sub * 0.4, 1)
dw = round(exec_avg * 0.6, 1)
score = int(round(sw + dw))

recs = [
    dict(priority="P1", title="Validators miss unplaced unmapped reads: false PASS at 70% mapped", observed_in=[7, 1],
         problem="validate_alignment.py (bam.fetch()) and the usage-guide AlignmentValidator (get_index_statistics()) never see reads with RNAME '*', so a BAM with 30% unmapped reads prints 'Mapped 100.0%' and 'All metrics within normal range'. The SKILL.md bash script reports the true 70.00%.",
         root_cause="pysam fetch() without until_eof and per-contig index statistics exclude unplaced unmapped reads; nothing cross-checks against flagstat.",
         fix="Iterate with fetch(until_eof=True) or take mapped/total from `samtools flagstat` primary counts (and add the idxstats '*' line), skip secondary/supplementary in every rate, and add a planted 30%-unmapped fixture to the examples."),
    dict(priority="P1", title="Validators exit 0 on failure and print no verdict", observed_in=[4, 7],
         problem="validate_alignment.py prints 'WARNINGS: ...' and exits 0; validate_alignment.sh and the SKILL.md script exit 0 on a missing or truncated BAM after printing 'Mapped: / (%)' and 40+ stderr lines, and print no pass/warn/fail although the section Approach promises it.",
         root_cause="No `set -euo pipefail`, no file/quickcheck precondition, no sys.exit status, no threshold logic in the bash script.",
         fix="Start every script with `test -s \"$BAM\" && samtools quickcheck \"$BAM\" || { echo ...; exit 2; }`, quote all variables, and exit 1 when any threshold is not met (python: sys.exit(1))."),
    dict(priority="P1", title="bc truncates before multiplying: 99.96% prints as 90.0% / 99.00%", observed_in=[1, 4],
         problem="validate_alignment.sh uses scale=1 with `$mapped/$total*100`, printing 'Mapped: 5642 / 5644 (90.0%)'; the SKILL.md script and usage-guide use scale=2 and print 99.00%. Any rate from 90.0 to 99.99 prints as 90.0 in the shipped script, on the WARN band of the Skill's own table.",
         root_cause="Division is truncated at `scale` digits before the *100.",
         fix="Multiply first: `echo \"scale=2; 100*$mapped/$total\" | bc`, or use awk '{printf \"%.2f\", 100*$1/$2}'."),
    dict(priority="P1", title="Strand-balance value printed by the bash snippets is not the quantity the 0.48-0.52 band describes", observed_in=[1, 5],
         problem="'Calculate Strand Ratio' and validate_alignment.sh print F/R = 1.0007 for a balanced BAM while the Strand Balance text, Quality Thresholds table and usage-guide define Good as 0.48-0.52 (a forward fraction, which validate_alignment.py prints as 0.500). An agent applying the table to the bash output flags every BAM.",
         root_cause="Two definitions (F/R vs F/(F+R)) used interchangeably.",
         fix="Print forward/(forward+reverse) in every snippet, label it, and count only mapped primary reads (-F 2308 for the forward count)."),
    dict(priority="P1", title="M5 diff false-alarms without M5 tags and cannot see name or assignment errors", observed_in=[3],
         problem="Real BAMs from bwa/minimap2/STAR carry no M5 (7 of 8 inspected here), so the snippet exits 1 against their own reference; a chr22 vs 22 rename or two contigs with swapped M5 give rc 0 although 'chr vs no-chr' is listed as a covered failure mode.",
         root_cause="Only the sorted M5 values are compared; SN and LN are dropped and missing M5 is not treated as 'cannot verify'.",
         fix="Compare `SN LN M5` triples (`cut -f2-4`), report 'no M5 in BAM header: compare SN/LN against samtools dict instead' when absent, and state that renaming is detected by SN, not M5."),
    dict(priority="P1", title="Example python validator crashes on empty, all-unmapped and unindexed BAMs", observed_in=[4],
         problem="ZeroDivisionError on empty and all-unmapped BAMs; bare ValueError on any BAM without an index, which rejects valid name-sorted and unsorted-UMI real files; the header always prints the requested sample size ('sampled 100000 reads') rather than the count actually read.",
         root_cause="No guards on total/len(mapqs) and bam.fetch() requires an index.",
         fix="Use until_eof=True (no index needed), handle zero totals with a clear message and exit code, print the actual n sampled."),
    dict(priority="P1", title="CI-safe integrity one-liner rejects small valid BAMs", observed_in=[2],
         problem="Hard-coded `-gt 1000` makes the one-liner exit 1 on valid 100-, 200- and 500-read BAMs, so it cannot be dropped into a pipeline unmodified.",
         root_cause="Illustrative threshold presented as a general check.",
         fix="Make the minimum a variable (`MIN=${MIN_READS:-1}`) or drop the count test and keep quickcheck plus `samtools view -c` as the decode check."),
    dict(priority="P2", title="Production IGNORE recipe removes checks that catch real defects", observed_in=[2],
         problem="`IGNORE=INVALID_MAPPING_QUALITY IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND` is presented as 'expected-but-noisy' with no condition; on the planted files it turns 40, 2 and 2820 real errors into 'No errors found'. Picard also flags legitimate region slices (MATE_NOT_FOUND on the 1000G slice) with no note.",
         root_cause="Ignore list copied without an evidence trail for when these errors are benign.",
         fix="State which aligner/pipeline emits these errors benignly, or drop the example; add a line that MATE_NOT_FOUND is expected on region-extracted BAMs."),
    dict(priority="P2", title="Per-chromosome and aneuploidy awk snippets are brittle", observed_in=[5],
         problem="Loop hard-coded to chr1-chr3 (bc 'Divide by zero' when a strand has zero reads or the contig is absent); idxstats awk dies on the '*' line (length 0); aneuploidy awk needs gawk (mawk: 'function asort never defined'; other non-GNU awks were not tested), divides by a zero median, and its regex leaves 824 of 846 contigs (chr1_KI270706v1_random, HLA, alt) in the median.",
         root_cause="Snippets written against one GRCh38 layout and one awk.",
         fix="Drive the loop from `samtools idxstats | awk '$3>0'`, skip length-0 lines, guard zero denominators, state 'requires gawk', and restrict to ^(chr)?([0-9]+)$."),
    dict(priority="P2", title="verifybamid2 prefix, Picard units and GC-bias band do not match the tools", observed_in=[6, 1],
         problem="--SVDPrefix /resources/1000g.b38.vcf.gz.SVD matches no released file (released prefix ends .dat; run gives 'Open file ...SVD.bed failed, exit!'); Picard reports fractions (0.9996, 0.002) while the table lists percentages; the 1.2x GC-bias band is tied to no Picard column; Related Skills use folder names without the bio- prefix.",
         root_cause="Placeholders and units not checked against tool output.",
         fix="Use `1000g.phase3.10k.b38.vcf.gz.dat`, note Picard fractions x100, name the GC-bias metric (e.g. min/max NORMALIZED_COVERAGE or GC_DROPOUT), and use the frontmatter names."),
    dict(priority="P2", title="Mean-MAPQ helper counts unmapped reads; thresholds disagree across files", observed_in=[5],
         problem="`awk '{sum+=$5}'` over all records gives 41.995 vs 59.99 on the 30%-unmapped fixture; the table calls mean MAPQ >40 'Good', the script warns at <30, and the text says mean MAPQ is misleading. Strand, pairing and MAPQ bands are hard-coded in SKILL.md, usage-guide and the script.",
         root_cause="No single source of thresholds; helper lacks -F 4.",
         fix="Use `samtools view -F 2308`, prefer the MAPQ>=30 fraction the text recommends, and keep one threshold table (the usage-guide should point to it)."),
    dict(priority="P2", title="usage-guide duplicates SKILL.md and small text inconsistencies", observed_in=[],
         problem="About half of usage-guide.md re-states SKILL.md (flagstat, pairing/strand calculations, insert-size python, Picard commands, a second validator class with the fetch() blind spot). The ATAC bullet says a missing ~180 bp peak = over-transposition while the paragraph adds under-titration; 'sample-swap rates of 0.5-1%' and 'FREEMIX > 0.03' are unsourced.",
         root_cause="Two documents evolved separately.",
         fix="Keep prompts, workflow and troubleshooting in usage-guide and remove every command block that also lives in SKILL.md; cite or soften the swap-rate and FREEMIX statements."),
]

lev1 = sum(i["basic"] for i in inputs) / len(inputs)
lev2 = sum(i["specialized"] for i in inputs) / len(inputs)
tot_pass = sum(i["assertions_passed"] for i in inputs)
tot_all = sum(i["assertions_total"] for i in inputs)

report = {
    "meta": {
        "skill_name": "bio-alignment-validation",
        "description": "Validate alignment quality with insert size distribution, proper pairing rates, GC bias, strand balance, and other post-alignment metrics. Use when verifying alignment data quality before variant calling or quantification.",
        "evaluated_on": "2026-09-20",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": 7,
        "source": "mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-validation",
        "mode": "first audit (Skill unchanged since c206dff; staging HEAD 7910c3a has identical bytes for this folder)",
        "executed": "7/7 (input 6 partial: somalier relate, CrosscheckFingerprints and a real FREEMIX estimate could not be run end-to-end, see its note)",
        "environment": "WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Picard 3.5.0 (af-picard3), deepTools 4.0.0, verifybamid2 2.0.3, somalier 0.3.5, gawk 5.4.1 and mawk. Real data from audit-envs/alignment-files/public-data (human chr22 slice PE/RNA/UMI/name-sorted, 1000G HG00349 chr20 slice with 3,366 contigs, ARTIC nanopore, SARS-CoV-2 Illumina PE/SE, planted_dups) copied, never written into. 23 SYNTHETIC planted-defect BAMs and 6 reference variants in run/data, all derived from the real human reads and labelled synthetic in run/data/fixtures.json.",
        "checks_run": "32 files x 6 integrity tools (matrix.json), 32 files x validator-vs-truth comparison (matrix_idx.json), 17 SKILL.md/usage-guide snippet groups run verbatim (test_snippets.txt), validators on edge inputs (test_validators.txt), Picard IGNORE recipe, contamination commands, determinism and space-in-path checks.",
        "detection_matrix": "21 planted-defect files: quickcheck 3, full decode 3, SKILL CI one-liner 6, Picard ValidateSamFile 18, shipped python validator 6 (2 by WARNINGS verdict, 4 by content crash). Flagged although valid: Picard 4 real files (name-sorted, RNA missing NM, 1000G slice MATE_NOT_FOUND, nanopore header), CI one-liner 3 (small valid BAMs), python validator crashes on 2 valid unindexed files.",
        "not_executed": "somalier relate and CrosscheckFingerprints with a real haplotype map (no matching data), a real FREEMIX estimate (needs a whole-genome BAM), head-of-file bias beyond 100,000 reads (largest available BAM 15,788 records), CRAM input.",
        "not_verified": "'Sample-swap rates of 0.5-1%' and 'FREEMIX > 0.03' are unsourced field conventions the text hedges as 'commonly used'; not checkable offline.",
        "judgements": {
            "veto_calls": "Skill veto PASS: no eval/exec, deterministic (identical md5 on repeat), frontmatter valid, valid indexed inputs run 100%. Research veto PASS: no fabricated identifiers, no individual-level clinical statement, no methodological fallacy (metric-definition mismatches are P1 defects, not fallacies), code parses (4/4 python blocks) and runs; edge-case crashes are robustness defects.",
            "no_P0": "Score 66 >= 60, no veto, no safety-assertion FAIL on any output. The exit-0-on-failure and false-PASS defects are recorded as the top P1s under the scoring rubric; they are the reason the score is Beta Only.",
            "picard_environment": "CollectInsertSizeMetrics and CollectGcBiasMetrics wrote PDFs because Rscript was on PATH in WSL; the Skill never says the PDF outputs need R; behaviour without R was not tested.",
            "fixture_caveat": "lowmap_* fixtures carry stale MC tags, so Picard also reports MATE_CIGAR_STRING errors on them; that is a fixture artefact and is not counted as detection of the low mapping rate.",
        },
        "floors_note": f"Static 67 (<70 Limited floor), execution {exec_avg} (<75), Layer 1 avg {lev1:.1f} (<28), Layer 2 avg {lev2:.1f} (<42), assertion pass rate {tot_pass}/{tot_all} = {100*tot_pass/tot_all:.1f}% (<80%). Score {score} is already in the Beta Only band, so no further downgrade applies.",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "No DOI/PMID, trial or p-value content; thresholds are labelled as assay-specific or field convention. Two unsourced conventions (0.5-1% swap rate, FREEMIX > 0.03) are hedged, not presented as citations."},
            "practice_boundaries": {"result": "PASS", "detail": "Alignment QC only; no diagnostic or prescriptive statement about an individual (sex-mismatch and swap checks are file-level QC)."},
            "methodological_ground": {"result": "PASS", "detail": "The two-layer split (file integrity vs QC metrics) is sound and the caveats on head-of-file sampling, MAPQ per aligner and RNA strandedness are correct. The F/R vs fraction mix-up and the fetch() blind spot are implementation defects (P1), not principled fallacies."},
            "code_usability": {"result": "PASS", "detail": "All 4 python blocks parse; every bash snippet and both example scripts executed on real data (Inputs 1-7). Crashes occur only on empty, all-unmapped or unindexed inputs and the bash scripts exit 0 on bad input; these are P1 robustness defects, not unrunnable code."},
        },
    },
    "static_score": {
        "subtotal": sub, "max": 100,
        "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()},
    },
    "dynamic_score": {
        "execution_avg": exec_avg, "max": 100,
        "assertion_pass_rate": {"passed": tot_pass, "total": tot_all},
        "inputs": inputs,
    },
    "final": {
        "static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
        "grade": "Beta Only", "grade_symbol": "⚠️", "deployable": False, "veto_override": False,
    },
    "key_strengths": [
        "The two-validation framing is right and verified: quickcheck catches EOF/truncation only, Picard ValidateSamFile caught 18 of 21 planted record-level defects, and the Skill says so up front.",
        "Every Picard, samtools, deepTools, verifybamid2 and somalier flag it names exists in the current tool versions (Picard 3.5.0 legacy KEY=VALUE, samtools 1.24 quickcheck -v fofn, view -s INT.FRAC).",
        "Strong assay-specific caveats (M5 case handling, RNA strandedness, MAPQ scales per aligner, head-of-file bias, ATAC multimodality) and useful cross-references that all resolve.",
        "Outputs the pysam route computes (insert-size median/mean, strand fraction, proper-pair rate) match Picard and samtools to within rounding on real data.",
    ],
    "recommendations": recs,
}

# ---- Pre-Emit Checklist ----
assert list(report.keys()) == ["meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"]
assert len(static) == 8 and all(0 <= v[0] <= v[1] for v in static.values())
assert report["static_score"]["subtotal"] == sum(v[0] for v in static.values())
assert len(inputs) == report["meta"]["n_inputs"] == 7
for i in inputs:
    assert 3 <= len(i["assertions"]) <= 5
    assert i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"] and i["basic"] <= 40 and i["specialized"] <= 60
    assert i["status_flag"] == ("✅" if i["status"] == "COMPLETED" and i["total"] >= 75 else "⚠️" if i["status"] == "COMPLETED" and i["total"] < 75 else "❌")
assert 2 <= len(report["key_strengths"]) <= 5
grade = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
assert report["final"]["grade"] == grade
pr = [r["priority"] for r in recs]
assert pr == sorted(pr)
assert abs(sw + dw - (sub * 0.4 + exec_avg * 0.6)) < 0.11
out = os.path.join(ROOT, f"eval_report_{SKILL}_result.json")
json.dump(report, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out)
print("static", sub, "exec_avg", exec_avg, "final", sw, "+", dw, "=", score, grade, "| L1", round(lev1, 1), "L2", round(lev2, 1), "assert", tot_pass, "/", tot_all)
for i in inputs:
    print(i["index"], i["type"], i["basic"], i["specialized"], i["total"], f'{i["assertions_passed"]}/{i["assertions_total"]}', i["status_flag"])
