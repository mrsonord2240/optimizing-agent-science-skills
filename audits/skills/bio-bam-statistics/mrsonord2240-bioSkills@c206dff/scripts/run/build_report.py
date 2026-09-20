#!/usr/bin/env python3
"""Builds eval_report_bio-bam-statistics_result.json and checks it against the schema's Pre-Emit Checklist."""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(ROOT, 'eval_report_bio-bam-statistics_result.json')

def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="flagstat / idxstats / stats / coverage on the real human chr22-slice paired-end BAM (nf-core)",
      status="COMPLETED", note="All CLI numbers match an independent hand count; the Skill's pysam counting snippet and qc_report.py count the 2 secondary records as mapped/proper (100.0% vs flagstat 99.96%).",
      basic=34, specialized=50, executed=True,
      execution_note="Ran samtools 1.24 flagstat/idxstats/stats/coverage, pysam 0.24.1 snippets and the shipped examples/qc_report.py from a copy on public-data human/test.paired_end.sorted.bam; every number compared with truth.py (pysam flag hand count).",
      assertions=[
        A("samtools flagstat, stats and idxstats numbers equal an independent pysam hand count (15 checks: total, secondary, primary mapped, properly paired, unmapped ...)", True, "15/15 PASS in check_counts.py (5644 total, 5642 primary, 5640 primary mapped, 5638 proper, idxstats chr22 5642 + * 2)."),
        A("samtools stats error rate and samtools coverage meandepth equal hand values", True, "error rate 2.01493e-03 = NM 1352 / ~670,990 CIGAR bases; coverage meandepth 16.7743 = block-based truth 16.7743; covbases 1181."),
        A("The Skill's pysam 'Count Reads' snippet reproduces flagstat's mapped and properly-paired counts", False, "Snippet reports mapped 5642 (100.0%) and proper 5640 vs flagstat primary mapped 5640 (99.96%) and proper 5638: secondary records are counted."),
        A("Shipped examples/qc_report.py runs from a clean copy and prints a checked report", True, "Printed 5,644 total, 5,640 proper (99.9%), insert size mean 126 / median 123 vs stats 124.8 (99% trimmed) and 125.7 (-m 1.0)."),
        A("idxstats counts secondary alignments in the mapped column, as the Skill's table states", True, "idxstats chr22 mapped 5642 = 5640 primary mapped + 2 secondary; unmapped column 0, '*' line 2."),
      ]),
 dict(index=2, type="Variant A", label="Mean depth and breadth (>=10x/>=20x) on the real human BAM with every tool the Skill names",
      status="COMPLETED", note="samtools coverage, depth -a, mosdepth --by/--thresholds are exact; the Skill's headline 'mean depth' and '>=20x' one-liners and pysam mean_depth() are off by 34x; samtools coverage -b BED fails.",
      basic=27, specialized=35, executed=True,
      execution_note="Ran samtools depth/coverage, mosdepth (default, --fast-mode, --by, --thresholds, --quantize, CRAM), bedtools genomecov and all Skill pysam coverage snippets on the human BAM against a block-based truth (truth.py).",
      assertions=[
        A("samtools coverage meandepth and covbases equal the independent truth", True, "16.7743 and 1181 = truth; depth -a and bedtools genomecov identical."),
        A("The Quick Reference 'Mean depth' one-liner (samtools depth | awk sum/n) gives the true mean depth", False, "Prints 568.15 against true 16.77: without -a the denominator is the 1181 covered positions, not the 40001-bp contig. Skill's pysam mean_depth() gives 579.7 for the same reason."),
        A("The usage-guide '>=10x / >=20x' one-liner gives the true breadth", False, "Prints 82.3% / 79.3%; true breadth of the contig is 2.43% / 2.34% (same denominator error)."),
        A("mosdepth --by/--thresholds and the 'depth -s' overlap caveat reproduce the truth exactly", True, "thresholds 1181/942/801/776/644 and mean 132.94 = truth; depth -s halves mean 16.77 -> 8.86 = mate-overlap-once truth; mosdepth default 8.86."),
        A("'samtools coverage -b regions.bed input.bam' works for BED regions as documented", False, "In 1.24 -b is --bam-list: 'Cannot open file list \"exome.bed\"'. Regions need -r, or mosdepth --by / samtools depth -b."),
      ]),
 dict(index=3, type="Edge", label="SYNTHETIC PE BAM with planted secondary, supplementary, QC-fail, duplicate, unmapped, singleton and mate-on-other-chromosome records",
      status="COMPLETED", note="All samtools counts equal the planted truth; the Skill's cross-check identity fails as literally written when QC-failed reads exist, and the pysam/qc_report proper-pair percent (88.9%) disagrees with flagstat (92.0%).",
      basic=31, specialized=44, executed=True,
      execution_note="Built data/synth.bam (540 records, counts by construction) with make_synth.py; ran flagstat/stats/idxstats, the -F 2308 -q 30 fraction, the idxstats mito awk, pysam snippets and qc_report.py; compared with planted truth and hand counts.",
      assertions=[
        A("flagstat, stats and idxstats reproduce every planted category count", True, "15/15 count checks PASS (540 total, 20 QC-fail, 10 secondary, 10 supp, 40 dup, 505 primary mapped, 480 proper, 5 singletons, 20 mate-on-other-chr; idxstats mapped 525 / unmapped 15)."),
        A("The Skill's cross-check (flagstat_total - secondary - supplementary = stats raw total sequences) holds as written", False, "flagstat 'in total' is '520 + 20' (QC-passed + QC-failed): first column - sec - supp = 500 vs stats 520; holds only after adding the QC-fail column, which the Skill never mentions."),
        A("The Skill's pysam 'Count Reads' and qc_report.py properly-paired % equal flagstat's", False, "88.9% (480/540, denominator includes 10 secondary, 10 supplementary and QC-fail) vs flagstat 92.0% (460/500) / 92.3% on primary."),
        A("The 'samtools view -c -F 2308 -q 30' primary-mapped MAPQ>=30 fraction is correct", True, "485/505 = 96.0% = hand count (485 of 505 primary mapped)."),
        A("idxstats mito awk gives the value the Skill's documentation implies", True, "7.619% = 40/525; documented that idxstats counts secondary+supp, primary-only fraction would be 7.92%."),
      ]),
 dict(index=4, type="Variant B", label="Depth-cap trap: SYNTHETIC 9500x amplicon stack plus the real ARTIC nanopore amplicon BAM",
      status="COMPLETED", note="CLI tools and the Skill's mpileup -d 1000000 advice verified; the Skill's own pysam pileup recipes silently cap at 8000 (mean 850 vs 1000) and its cap warning omits pysam and bcftools.",
      basic=31, specialized=45, executed=True,
      execution_note="Built data/deep.bam (9500 reads at amp:101-200, 500 at 301-400); ran samtools depth (-d/-m), coverage (-d), mpileup (-d default/1000000), bcftools mpileup, mosdepth and pysam pileup; then repeated all depth tools on public-data sarscov2 ARTIC nanopore BAM (max depth 159).",
      assertions=[
        A("samtools depth, samtools coverage and mosdepth return the planted max 9500 and mean 1000", True, "depth max 9500; coverage meandepth 1000; mosdepth summary 1000.00, max 9500."),
        A("The Skill's advice holds: mpileup default caps at 8000, 'mpileup -d 1000000' fixes it, 'depth -d' is silently ignored", True, "mpileup max 8000 default / 9500 with -d 1000000; depth -d 100 and -m 100 still 9500."),
        A("The Skill's pysam pileup recipes reproduce the planted mean depth of 1000", False, "pileup default max_depth=8000: max 8000, coverage_stats mean 850 (-15%); mean_depth() prints 4250."),
        A("The Skill's cap warning covers every pileup engine it recommends", False, "No mention that pysam pileup (max_depth=8000) or bcftools mpileup (-d 250; DP=250 observed at 9500x) also truncate."),
        A("On real ARTIC nanopore data depth tools agree with the independent truth", True, "samtools depth -a, coverage, bedtools genomecov, mosdepth default all 68.84x / 29826 covered bases = truth; pysam and mosdepth --fast-mode read 69.97 because pileup.n counts deletion columns."),
      ]),
 dict(index=5, type="Stress", label="Batch summary of 8 BAMs (real PE, RNA, 1000G, ARTIC, SE, planted dups, synthetic) plus plot-bamstats and MultiQC",
      status="COMPLETED", note="The usage-guide loop matches hand counts on every real BAM including 1000G's 101 duplicates; it silently omits QC-failed reads and mixes secondary into Total/Mapped; plots and MultiQC work.",
      basic=33, specialized=48, executed=True,
      execution_note="Ran the usage-guide 'Process Multiple Files' loop verbatim over 8 BAM copies, compared summary.tsv with truth.py; ran plot-bamstats -p plots/ and MultiQC 1.35 on stats/flagstat/idxstats files.",
      assertions=[
        A("The batch loop's Total and Duplicates columns equal hand counts for all 8 BAMs", True, "8/8 rows match on QC-passed records, incl. 1000G 9601 total / 101 duplicates and RNA 8828 (1786 secondary)."),
        A("plot-bamstats -p plots/ creates the directory and the documented plots", True, "11 PNGs plus index.html written to a not-yet-existing plots/ (gnuplot warnings only)."),
        A("MultiQC ingests samtools stats, flagstat and idxstats output as the Skill says", True, "multiqc_sources.txt lists Samtools stats, flagstat and idxstats for the sample; report built."),
        A("The batch loop accounts for every record in the file", False, "Synthetic BAM: 20 QC-failed records dropped silently (Total 520 of 540); the 'Paired' column is properly-paired; Total/Mapped include secondary/supplementary."),
      ]),
 dict(index=6, type="Scope Boundary", label="Mate-pair insert size, adapter read-through via soft-clipping, off-target/enrichment and contamination checks",
      status="COMPLETED", note="Two Skill statements are wrong on samtools 1.24 (soft-clipped grep returns nothing; RF insert-size IS section is not empty); Picard fields exist; VerifyBamID2 could not produce a value on the 100 kb slice.",
      basic=28, specialized=34, executed=True,
      execution_note="Executed: samtools stats on synthetic RF BAMs (proper flag set/unset), the soft-clip grep on real and synthetic BAMs, Picard 3.5.0 CollectHsMetrics (synthetic bait/target interval), samtools dict, MultiQC, verifybamid2 (ran, 'No reads found in any of the regions'). Not executed: the assay threshold table (literature values, no matching data).",
      assertions=[
        A("Picard CollectHsMetrics prints PCT_OFF_BAIT, FOLD_80_BASE_PENALTY, AT_DROPOUT, GC_DROPOUT as named", True, "All four columns present (PCT_OFF_BAIT 0, AT/GC_DROPOUT 0, MEAN_TARGET_COVERAGE 124.74; FOLD_80_BASE_PENALTY '?' on the 2.8 kb bait)."),
        A("'samtools stats | grep \"bases soft-clipped\"' returns the value the Skill says to threshold at 5%", False, "No such SN line in 1.24: 0 matches on the real BAM (863 soft-clipped bases by CIGAR) and on the synthetic BAM (400 planted); silent empty output. Only 'bases trimmed' exists."),
        A("The Skill's claim that samtools stats leaves the IS section empty for RF mate-pair libraries", False, "Synthetic RF library (100 pairs, insert 2000): stats reports 'outward oriented pairs 100', IS average 2000.0 whether the proper flag is set or not; only the Skill's own proper-pair snippet yields nothing."),
        A("Contamination and enrichment questions are handed to Picard/VerifyBamID2/somalier without any individual-level diagnosis", True, "Skill only names the tools and thresholds; VerifyBamID2 ran on the slice and printed 'No reads found in any of the regions', so FREEMIX itself was not verified."),
        A("No clinical or diagnostic conclusion is drawn", True, "QC-only content; sex check is a raw X/Y read ratio with no interpretation."),
      ]),
 dict(index=7, type="Adversarial", label="Header-only, single-end and unindexed BAMs plus Ensembl-style MT contig naming through the Skill's recipes",
      status="PARTIAL", note="The Skill's pysam snippets and qc_report.py raise ZeroDivisionError on single-end / empty BAMs; the mito and X:Y awk one-liners print a silent 0 when the contig is absent.",
      basic=23, specialized=27, executed=True,
      execution_note="Built data/empty.bam, se.bam, noindex.bam and renamed chrM to MT; ran flagstat/idxstats/coverage/mosdepth, the Skill pysam snippets, qc_report.py and the awk one-liners on each; also the real nf-core single-end BAM.",
      assertions=[
        A("The Skill's Count Reads, flagstat-equivalent and insert-size snippets run on single-end and header-only BAMs", False, "ZeroDivisionError (paired == 0 / total == 0) on the real nf-core SE BAM and the empty BAM; qc_report.py also divides by total on the empty BAM."),
        A("The shipped qc_report.py handles a single-end BAM", True, "Guarded 'if stats[paired]': prints 50/55 mapped (90.9%), properly paired 0.0%."),
        A("The mito % and X:Y awk recipes flag a missing contig instead of printing 0", False, "'0% mitochondrial' for an MT-named contig holding 40 reads (and for a BAM with no chrM); 'X:Y = 0.00' with no chrX/chrY."),
        A("The Troubleshooting 'samtools index' fix resolves the unindexed-BAM failures", True, "pysam get_index_statistics ValueError and mosdepth 'must be indexed' are the failure modes; note idxstats itself falls back to a slow scan in 1.24 (rc 0), so 'requires an index' is stale."),
        A("No destructive or unsafe operation is recommended", True, "Read-only commands; no eval/exec/shell=True (grep scan)."),
      ]),
]

for it in inputs:
    it['total'] = it['basic'] + it['specialized']
    it['assertions_passed'] = sum(1 for a in it['assertions'] if a['result'] == 'PASS')
    it['assertions_total'] = len(it['assertions'])
    it['status_flag'] = '✅' if (it['status'] == 'COMPLETED' and it['total'] >= 75) else ('⚠️' if it['status'] == 'COMPLETED' else '❌')
    # key order as in the schema example
    order = ['index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'total',
             'assertions_passed', 'assertions_total', 'assertions', 'executed', 'execution_note']
    it_sorted = {k: it[k] for k in order}
    it.clear(); it.update(it_sorted)

cats = {
 "functional_suitability": (8, 12, "Completeness 3, Correctness 2, Appropriateness 3. Covers flagstat/idxstats/stats/depth/coverage/mosdepth/pysam, denominators and assay thresholds; but verified errors: samtools coverage -b BED, nonexistent 'bases soft-clipped', covered-position denominators in mean-depth/>=Nx recipes, pysam counts without primary filter, false RF insert-size claim, 'mapped and paired' = properly paired."),
 "reliability": (7, 12, "Fault tolerance 2, Error reporting 2, Recoverability 3. Snippets raise ZeroDivisionError on single-end/empty BAMs, awk recipes divide by zero or print a silent 0% (MT naming, no chrM); raw tracebacks, no guards; all recipes are read-only and re-runnable."),
 "performance_context": (6, 8, "Token cost 3, Execution efficiency 3. SKILL.md 427 lines with a tool-choice table up front, but the usage-guide repeats most CLI/pysam recipes and no references/ split exists."),
 "agent_usability": (11, 16, "Learnability 3, Consistency 2, Feedback 3, Error prevention 3. Clear tables and sample outputs; the 'what each tool counts' section is strong; pysam snippets disagree with each other (mean_depth vs coverage_stats vs region_coverage) and with the CLI denominators."),
 "human_usability": (5, 8, "Discoverability 3, Forgiveness 2. Description names the tools and use cases; usage-guide has natural example prompts; off-spec inputs (SE, empty, other contig names) give crashes or silent zeros."),
 "security": (11, 12, "Credentials 4, Input validation 3, Data safety 4. No eval/exec/network/credentials; batch loop quotes \"$bam\"; no path or BAM validation before use."),
 "maintainability": (8, 12, "Modularity 3, Modifiability 3, Testability 2. Two docs plus one example; recipes duplicated across SKILL.md and usage-guide.md; no test data or expected values shipped."),
 "agent_specific": (17, 20, "Trigger precision 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 3. Related-skill links all exist; MultiQC and plot-bamstats hand-offs verified; Picard/VerifyBamID2/somalier named for out-of-scope QC; no explicit stop/hand-off rule."),
}
static_sub = sum(v[0] for v in cats.values())
exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
sw, dw = round(static_sub * 0.4, 1), round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
passed = sum(i['assertions_passed'] for i in inputs); total_a = sum(i['assertions_total'] for i in inputs)

recs = [
 dict(priority="P1", title="Mean-depth and >=Nx recipes divide by covered positions", observed_in=[2],
      problem="'samtools depth | awk sum/n' (SKILL.md Quick Reference, usage-guide) returns 568.15x on a BAM whose true mean depth is 16.77x, the '>=10x/>=20x' one-liner returns 82.3%/79.3% for a true 2.43%/2.34%, and the pysam mean_depth() snippet returns 579.7.",
      root_cause="The recipes omit 'samtools depth -a' and divide by the number of covered positions / pileup columns instead of the region length.",
      fix="Use 'samtools depth -a' (or divide by end-start) in every mean-depth and >=Nx recipe, make mean_depth() divide by (end - start) like coverage_stats(), and point 'mean depth' at samtools coverage / mosdepth as the primary answer."),
 dict(priority="P1", title="pysam counting snippets count secondary/supplementary/QC-fail", observed_in=[1, 3],
      problem="'Count Reads', the usage-guide flagstat() and examples/qc_report.py count every record: mapped 5642 vs flagstat primary 5640 on the real BAM; on the planted BAM properly-paired is 88.9% vs flagstat 92.0%. The SE and empty cases raise ZeroDivisionError.",
      root_cause="Loops over all alignments with no is_secondary/is_supplementary/is_qcfail filter and unguarded divisions, contradicting the Skill's own 'what each tool counts' table.",
      fix="Skip secondary and supplementary records for read-level rates (count them separately), state the denominator in the printed labels, and guard every division (if paired / if total)."),
 dict(priority="P1", title="pysam pileup recipes silently cap depth at 8000 and drop orphans", observed_in=[4],
      problem="On a 9500x stack the pysam recipes report max 8000 and mean 850 (planted 1000), and pileup drops 20 non-proper paired reads (total depth 2000 vs samtools depth 3500); mean_depth() prints 4250.",
      root_cause="pysam pileup defaults (max_depth=8000, ignore_orphans=True, columns include deletions) are never mentioned although the Skill warns about the same cap for mpileup.",
      fix="Pass max_depth=1_000_000 (and ignore_orphans=False, stepper='nofilter' as needed) in every pileup snippet, add a note that pileup.n counts deletions, and extend the cap warning to pysam and bcftools mpileup (-d 250)."),
 dict(priority="P1", title="'samtools coverage -b regions.bed' is not a BED option", observed_in=[2],
      problem="In samtools 1.24 -b is --bam-list, so the documented 'Coverage from BED' command fails with 'Cannot open file list \"exome.bed\"'.",
      root_cause="Flag copied from 'samtools depth -b' where -b is a BED file.",
      fix="Delete the example or replace it with 'samtools coverage -r chr:start-end' per region, 'samtools depth -b bed', or 'mosdepth --by regions.bed'."),
 dict(priority="P1", title="Adapter-readthrough detector greps a stats field that does not exist", observed_in=[6],
      problem="'samtools stats | grep \"bases soft-clipped\"' prints nothing on samtools 1.24 (0 matches on a BAM with 863 soft-clipped bases, and on a synthetic BAM with 400), and the '>5%' threshold cannot apply to an absolute count.",
      root_cause="The SN line was assumed, not checked against the installed samtools.",
      fix="Compute the soft-clipped fraction from CIGARs (samtools view -F 2308 | awk on the CIGAR, or pysam cigartuples op 4 over primary reads) and state the denominator; keep the >5% rule for that fraction."),
 dict(priority="P1", title="'Insert Size Caveats' misstate what samtools stats reports", observed_in=[6],
      problem="The Skill says stats reports the IS section only for FR-oriented properly paired reads and leaves it empty for RF mate-pair libraries; on a synthetic RF library stats reports 100 outward-oriented pairs and IS average 2000.0 with the proper flag set or unset.",
      root_cause="Behaviour inferred from aligner flag conventions rather than from samtools stats output.",
      fix="State that stats reports IS for any pair with both mates mapped and gives inward/outward/other orientation counts; tell the agent to read those counts for mate-pair libraries, and only the pysam proper-pair snippet needs an orientation change."),
 dict(priority="P1", title="Recipes crash or print a silent 0 on SE, empty and differently named contigs", observed_in=[7],
      problem="ZeroDivisionError on single-end and header-only BAMs, awk division by zero on empty input, '0% mitochondrial' for an MT contig with 40 reads and for BAMs with no chrM, 'X:Y = 0.00' without chrX/chrY.",
      root_cause="Snippets assume paired human data with UCSC contig names and never check that the numerator contig exists.",
      fix="Match '^(chr)?(M|MT)$' and print a warning when no contig matches, guard divisions, and add a one-line 'check contig names with idxstats first' note."),
 dict(priority="P2", title="Cross-check identity and 'primary' table row ignore QC-failed and secondary", observed_in=[3],
      problem="flagstat 'in total' is 'QC-passed + QC-failed'; the identity as written gives 500 vs stats 520 on the planted BAM, and the table row 'primary = in total minus supp' omits secondary.",
      root_cause="The sample output shows '+ 0' columns and the text never explains them.",
      fix="Write the identity as total(pass+fail) - secondary - supplementary = stats raw total sequences, explain the two flagstat columns, and correct the table row to 'minus secondary and supplementary'."),
 dict(priority="P2", title="'reads mapped and paired' is described as properly paired", observed_in=[3],
      problem="Key summary fields list 'reads mapped and paired - Properly paired'; on the planted BAM stats shows 500 mapped-and-paired vs 480 properly paired.",
      root_cause="Two different SN lines conflated.",
      fix="Relabel it 'both mates mapped' and list 'reads properly paired' / 'percentage of properly paired reads' as the proper-pair fields."),
 dict(priority="P2", title="Mate-overlap defaults differ 2x across tools and are not tabulated", observed_in=[2],
      problem="Same BAM: samtools depth/coverage and mosdepth --fast-mode 16.77x, mosdepth default and depth -s 8.86x; the Quick Summary table presents them as interchangeable.",
      root_cause="Only 'depth -s' and mosdepth are discussed for overlap; samtools coverage (no overlap option) and mosdepth --fast-mode are not.",
      fix="Add one row per tool for default overlap handling and tell the agent to state which convention it reports."),
 dict(priority="P2", title="'Calculate Depth at Position' snippet prints whole read footprints", observed_in=[2],
      problem="pileup('chr22', 2999, 3000) without truncate=True printed 232 columns (2907-3138) for a 1-bp query; the requested position 1562x is correct.",
      root_cause="truncate=True is used in the later snippets but omitted here.",
      fix="Add truncate=True (and max_depth) to the single-position snippet."),
 dict(priority="P2", title="Batch loop drops QC-failed reads and mislabels columns", observed_in=[5],
      problem="The usage-guide loop takes only flagstat's first column: 20 QC-failed records vanish (Total 520 of 540), the 'Paired' column is properly-paired, and Total/Mapped include secondary/supplementary (RNA 1786).",
      root_cause="awk uses $1 only and column names are loose.",
      fix="Sum both flagstat columns or report QC-fail separately, rename the column 'ProperPair' and add a 'Primary' column."),
 dict(priority="P2", title="Stale or incomplete tool notes (idxstats, CRAM, plot-bamstats, mosdepth)", observed_in=[7],
      problem="idxstats no longer needs an index in 1.24 (slow-scan fallback, rc 0); 'samtools stats -r ref.fa' does not decode CRAM (needs --reference; fails with 'Failure while decoding file'); mosdepth CRAM needs a .crai; tooling pass found plot-bamstats needs perl-URI (not re-run here); 'depth -r chr1:1-10000000 # Single chromosome' is a 10 Mb region; the historic depth cap is attributed to mpileup only.",
      root_cause="Notes written from memory of older versions.",
      fix="Update each note to samtools 1.24 behaviour and add the CRAM/index and perl-URI prerequisites."),
 dict(priority="P2", title="Unverified claims and duplicated recipes", observed_in=[],
      problem="'mosdepth 3-10x faster than samtools depth', the assay-threshold table values and the historic depth-cap statement were not verifiable with the available data; SKILL.md and usage-guide.md carry parallel CLI and pysam recipes that already diverge.",
      root_cause="Literature/lore claims without a source and no single owner for each recipe.",
      fix="Cite or drop the speed claim and mark threshold values as literature ranges; keep each recipe in one file and link from the other."),
]

report = {
 "source": "mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/bam-statistics",
 "meta": {
   "skill_name": "bio-bam-statistics",
   "description": "Generate alignment statistics using samtools flagstat, stats, depth, coverage, and mosdepth. Use when assessing alignment quality, calculating coverage, or generating QC reports.",
   "evaluated_on": "2026-09-20",
   "evaluator_version": "skill-auditor@1.0",
   "category": "Data Analysis",
   "execution_mode": "D",
   "complexity": "Complex",
   "n_inputs": 7,
   "executed": "7/7 inputs executed (input 6 partly: VerifyBamID2 ran but returned no FREEMIX value; the assay-threshold table was not executable)",
   "tools": "samtools 1.24, pysam 0.24.1, mosdepth 0.3.14, bedtools 2.31.1, bcftools 1.24, Picard 3.5.0, MultiQC 1.35, plot-bamstats (WSL science, env alignment-files)"
 },
 "veto_gates": {
   "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
   "research_veto": {
     "applicable": True, "gate": "PASS",
     "scientific_integrity": {"result": "PASS", "detail": "No PMIDs, trial data or numbers are invented; every statistic the Skill prints was compared with an independent computation."},
     "practice_boundaries": {"result": "PASS", "detail": "QC statistics only; no diagnosis or prescription; the sex-check is a raw X/Y read ratio with no clinical interpretation; contamination/enrichment are handed to Picard/VerifyBamID2/somalier."},
     "methodological_ground": {"result": "PASS", "detail": "No principled fallacy in the recommended tools (samtools coverage, mosdepth, depth -a). The covered-position denominator in the awk mean-depth and >=Nx recipes (568x vs 16.8x, Input 2) is recorded as a P1 correctness defect: the same document offers correct alternatives, so it is not judged a veto-level fallacy."},
     "code_usability": {"result": "PASS", "detail": "Every snippet parses and runs on normal paired-end data and examples/qc_report.py ran 10/10. Recorded as P1 instead of veto: one wrong flag (samtools coverage -b), one nonexistent stats field, and ZeroDivisionError on single-end/empty input (Input 7)."}
   }
 },
 "static_score": {
   "subtotal": static_sub, "max": 100,
   "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}
 },
 "dynamic_score": {
   "execution_avg": exec_avg, "max": 100,
   "assertion_pass_rate": {"passed": passed, "total": total_a},
   "inputs": inputs
 },
 "final": {
   "static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
   "grade": "Beta Only", "grade_symbol": "⚠️", "deployable": False, "veto_override": False
 },
 "key_strengths": [
   "Every CLI number (flagstat, idxstats, stats, coverage, depth, mosdepth --by/--thresholds) matched an independent hand count on real and planted-truth BAMs (30/30 count checks on two files; 8/8 batch rows).",
   "Unusually careful pitfall content that verified on samtools 1.24: primary vs secondary/supplementary denominators, mpileup 8000 cap, 'depth -d' silently ignored, 'depth -s' halving overlapped depth (16.77x to 8.86x), mosdepth flag 1796/3844 semantics.",
   "Assay-specific QC framing and a 'what flagstat does not reveal' section that routes enrichment and contamination questions to Picard, VerifyBamID2 and somalier instead of over-reaching.",
   "Shipped example runs from a clean copy, output is deterministic, no security surface; plot-bamstats and MultiQC hand-offs work as documented."
 ],
 "recommendations": recs,
}

# ---------------- Pre-Emit Checklist
assert len(report['static_score']['categories']) == 8
assert report['static_score']['subtotal'] == sum(c['score'] for c in report['static_score']['categories'].values())
for k, c in report['static_score']['categories'].items():
    assert 0 <= c['score'] <= c['max'], k
assert sum(c['max'] for c in report['static_score']['categories'].values()) == 100
assert len(inputs) == report['meta']['n_inputs'] == 7
for it in inputs:
    assert 3 <= len(it['assertions']) <= 5
    assert it['assertions_passed'] == sum(a['result'] == 'PASS' for a in it['assertions'])
    assert it['basic'] + it['specialized'] == it['total']
    assert 0 <= it['basic'] <= 40 and 0 <= it['specialized'] <= 60
assert report['dynamic_score']['execution_avg'] == round(sum(i['total'] for i in inputs) / 7, 1)
assert 2 <= len(report['key_strengths']) <= 5
pr = [r['priority'] for r in recs]; assert pr == sorted(pr)
assert report['final']['score'] == int(round(sw + dw))
s = report['final']['score']
assert (s >= 85 and report['final']['grade'] == 'Production Ready') or (75 <= s < 85 and report['final']['grade'] == 'Limited Release') or (60 <= s < 75 and report['final']['grade'] == 'Beta Only') or (s < 60 and report['final']['grade'] == 'Reject')
json.dump(report, open(OUT, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
l1 = sum(i['basic'] for i in inputs) / 7; l2 = sum(i['specialized'] for i in inputs) / 7
print('static', static_sub, 'exec_avg', exec_avg, 'final', sw, dw, sw + dw, '->', score, report['final']['grade'])
print('L1 avg %.1f/40 (floor lim 28)  L2 avg %.1f/60 (floor lim 42)  assertions %d/%d = %.1f%%' % (l1, l2, passed, total_a, 100 * passed / total_a))
print('per-input totals', [i['total'] for i in inputs], [i['status_flag'] for i in inputs])
print('wrote', OUT)
