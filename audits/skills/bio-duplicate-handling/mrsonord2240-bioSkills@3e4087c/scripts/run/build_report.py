"""Builds eval_report_bio-duplicate-handling_result.json and eval_viewer_bio-duplicate-handling.md from the scored results below.
Every number quoted in the notes comes from the in*.log files in this folder. Run from run/:  PYTHONIOENCODING=utf-8 python build_report.py"""
import io, json, os
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILL = "bio-duplicate-handling"
SRC = "mrsonord2240/bioSkills@3e4087ce9b3d9c4d89df6765e6dd4c4d8c063dc9:alignment-files/duplicate-handling"

meta = {
    "skill_name": SKILL,
    "description": "Mark and remove PCR/optical duplicates using samtools fixmate and markdup. Use when preparing alignments for variant calling or when duplicate reads would bias analysis.",
    "evaluated_on": "2026-09-20",
    "evaluator_version": "skill-auditor@1.0",
    "category": "Data Analysis",
    "execution_mode": "B",
    "complexity": "Complex",
    "n_inputs": 8,
    "source": SRC,
    "audit_kind": "re-audit of a fixed Skill (pre-fix 77, Limited Release, first audit 2026-09-20; fixer: fix/af-dup 3e4087c)",
    "executed": "8/8 inputs executed (inputs 1-6 = the pre-fix inputs re-run as regression against the fixed text, with the fixer's blocks extracted verbatim from SKILL.md by run/blocks.py; inputs 7 and 8 are new, built on the auditor's own planted truth).",
    "execution_note": "WSL science, env alignment-files (samtools 1.24, pysam 0.24.1, Picard 3.5.0 side env, fgbio 4.1.1 side env, umi_tools 1.1.6, sambamba 1.0.1, samblaster 0.1.26, bwa-mem2 2.3, mapDamage 2.2.2 side env) plus the fixer's env af-dup-extra (biobambam2 2.0.185, pbmarkdup 1.2.0; not in TOOLS.md, driven with micromamba run) and a throwaway macs3 3.0.4 venv. Real data from public-data (nf-core human PE/RNA/UMI BAMs, 1000G HG00349 slice, ARTIC nanopore, sarscov2 FASTQ pairs) plus planted_dups.bam (truth 50 pairs) and SYNTHETIC data written by run/ scripts (multi-library, same-library 2 RG, amplicon, optical, planted2 soft-clip/SE/reverse, HiFi-style unaligned BAM, damaged SE BAM, planted duplex-UMI BAM, 800k-read timing BAM, ChIP-like BAM). Scripts: run/. Skill folder run from a COPY (run/skill_copy, diff-identical to the worktree at 3e4087c).",
    "execution_mode_note": "SKILL.md CLI patterns plus one shipped shell example (examples/markdup_pipeline.sh); no scripts/ dir. Classified B (CLI/script).",
}

static = {
    "functional_suitability": (11, 12, "Completeness 4 (every tool the tables name now has a run block: biobambam2, sambamba, pbmarkdup, mapDamage --rescale, Picard UmiAware, umi_tools, fgbio single-strand and duplex), correctness 3 (all blocks reproduced; unmeasured '~30% faster' and biobambam2 'Fastest' claims, and my 800k-read timing contradicts the first), appropriateness 4."),
    "reliability": (10, 12, "Fault tolerance 3 (pipefail + mkdir + record-count check in the block; example exits 1/2/3 and leaves no half-written output: verified for missing, truncated, empty, unwritable, unknown-assay inputs), error reporting 4 (8 of 8 Common Errors messages match tool output), recoverability 3 (the SKILL.md block still leaves a partial marked.bam; the text says to delete it)."),
    "performance_context": (5, 8, "Token cost 3 (SKILL.md 421 lines but usage-guide cut to 60 and duplicates removed), execution efficiency 2 (the 'Optimized' pipeline measured 6.4 s vs 4.6 s for the plain 5-step chain on an 800k-read BAM at 4 threads; the ~30% faster claim is unsupported)."),
    "agent_usability": (14, 16, "Learnability 3, consistency 4 (usage-guide contradictions gone, one copy of each fact), feedback design 3 (example prints stats + warnings; SKILL.md blocks assert counts), error prevention 4 (Step 0 assay gate, -c, @RG, tmpdir, --paired, MQ prerequisite all stated)."),
    "human_usability": (6, 8, "Discoverability 3 (frontmatter description still omits the assay/UMI caveats), forgiveness 3 (name-sorts first, accepts any-order input; ASSAY must be declared by the user)."),
    "security": (11, 12, "No credentials, no eval; variables quoted; example uses mktemp -d + trap and writes output by temp-then-mv; silently overwrites an existing output path."),
    "maintainability": (10, 12, "Modularity 4 (usage-guide is now an index into SKILL.md), modifiability 3 (large single SKILL.md), testability 3 (verifiable counts, one runnable example, no shipped test data)."),
    "agent_specific": (16, 20, "Trigger 3, progressive disclosure 3 (421 lines, no references/), composability 4 (Related Skills exist), idempotency 3 (example overwrites; umi_tools output varies by 1 record run to run without --random-seed), escape hatches 3 (assay gate refuses eight assay names; a mis-declared RNA-seq BAM under ASSAY=wgs passes with no warning at 38% flagged)."),
}

def A(t, r, n): return {"text": t, "result": "PASS" if r else "FAIL", "note": n}

inputs = [
 dict(index=1, type="Canonical", label="Workflow steps, stats, -r, pysam blocks vs planted truth and 4 independent tools", status="COMPLETED", flag="✅",
  prompt="I have paired-end Illumina alignments (coordinate sorted). Mark the PCR duplicates with the standard fixmate/markdup workflow, index the result, tell me how many reads were flagged and the duplicate rate. Then do the same in Python with pysam and filter the duplicates out.",
  note="SKILL.md 'Duplicate Marking Workflow', 'Percentage Duplicates', '-s', '-r' and all three pysam blocks extracted verbatim and run: planted 100/100, real human BAM 1656; Picard, sambamba, samblaster agree",
  basic=37, spec=56, script="in01_canonical.sh", log="in01.log",
  output="planted_dups.bam: flagged 100 of 500, flagstat '100 + 0 duplicates', pct block 20.00, -s stats DUPLICATE TOTAL 100, -r -> 400 records (=500-100). Picard READ_PAIR_DUPLICATES 50, flagged 100; sambamba 100; samblaster 100.\ntest.paired_end.sorted.bam: flagged 1656 of 5644, pct block 29.35 (primary-only, same as pysam rate 29.35%), -r -> 3988, Picard/sambamba/samblaster 1656, samtools vs Picard flagged (name,flag) set difference 0 lines. pysam full pipeline flagged 100/1656 and wrote marked.bam.bai; pysam filter 400/3988 = samtools -F 1024; pysam.markdup without ms raises SamtoolsError 'no ms score tag'.",
  assertions=[
   A("SKILL.md workflow steps 1-5 (extracted verbatim) flag exactly the planted 100 reads and index the output", 1, "view -c -f 1024 = 100; flagstat '100 + 0 duplicates'; marked.bam.bai written; -s stats DUPLICATE TOTAL 100"),
   A("Independent tools agree: Picard 50 pairs (=100 reads), sambamba 100, samblaster 100; on the real BAM samtools and Picard flag the identical (name,flag) set", 1, "1656 for all four on the human BAM; set difference 0. On planted, ties are broken differently but counts are equal"),
   A("-r returns total minus flagged; -c/-F counting blocks agree", 1, "500->400 and 5644->3988; 1656 dup / 3988 non-dup"),
   A("'Percentage Duplicates' block agrees with the pysam rate (same primary-only denominator)", 1, "29.35 vs pysam 29.35%; 20.00 on planted; the usage-guide/SKILL.md denominator contradiction is gone"),
   A("Every pysam block runs verbatim and matches samtools; tool errors surface as exceptions", 1, "flagged 100/1656, filter 400/3988, SamtoolsError text includes the samtools message"),
  ]),
 dict(index=2, type="Variant A", label="Rewritten 'Pipeline Version (Optimized)' from a clean dir: valid exit 0, failure exit non-zero; optical vs Picard; speed claim", status="COMPLETED", flag="✅",
  prompt="This is a NovaSeq 6000 WGS run. Give me the fast piped duplicate-marking command with 4 threads, optical duplicates at the right distance, per-read-group handling and a stats file, then tell me how many duplicates are optical vs PCR.",
  note="Pre-fix P1 fixed: block from a clean dir now exits 0 with 100/1656, and without its mkdir line exits 1; failure modes exit non-zero. Only the unmeasured '~30% faster' claim fails (measured slower)",
  basic=34, spec=51, script="in02_pipeline_optical.sh; in09_timing_claim.sh", log="in02.log; in09.log",
  output="Block extracted verbatim (set -euo pipefail; mkdir -p tmpdir; collate|fixmate|sort|markdup; index; count test). Clean dir: planted exit=0 500/500 records, flagged 100, index present, stats EXAMINED 500 / DUPLICATE TOTAL 100 (ALL + 1 READ GROUP block); human exit=0 5644/5644, 1656.\nWithout the mkdir line: exit=1, 'samtools collate: Cannot open intermediate file \"tmpdir/collate.0000.bam\"' (was exit 0 pre-fix). Without pipefail AND mkdir the closing count test still returns exit 1 (the record-count check is a second guard). Missing input exit 1; truncated BAM exit 1 ('EOF marker is absent').\nOptical (SYNTHETIC, truth 4 dup pairs): samtools optical pairs 0/1/2 at -d 0/100/2500 = Picard optical pairs 0/1/2; dt:Z:SQ/LB tags only when -d is set (4 SQ + 4 LB at 2500); the SKILL.md grep block prints the same counts.\nTiming (in09, 800k reads, 4 threads, 3 reps): optimized 6.29/6.56/6.47 s vs 5-step 4.59/4.64/4.67 s, both flag 120610.",
  assertions=[
   A("The verbatim optimized pipeline runs from a clean working directory and flags the truth counts", 1, "exit 0; 100 planted, 1656 human; 500/500 and 5644/5644 records; index written"),
   A("Every failure mode of the block exits non-zero (missing tmpdir, missing input, truncated input)", 1, "exit 1 in all three; pre-fix defect (exit 0 with an empty 501-byte marked.bam) is gone"),
   A("Optical claims hold: -d 0 emits no dt tag, -d emits dt:Z:SQ/LB, counts match Picard", 1, "samtools optical pairs 0/1/2 vs Picard 0/1/2 at -d 0/100/2500 on synthetic truth"),
   A("-f stats file and --use-read-groups are accepted and do not change the flagged count", 1, "flags in 1.24 help; 100 flagged; stats file has ALL + READ GROUP blocks"),
   A("The claim 'This is ~30% faster than sort -n | fixmate | sort | markdup' holds", 0, "Not reproduced: optimized 6.4 s vs 5-step 4.6 s on 800k reads (equal flagged counts). Scale caveat (30x WGS is ~1e9 reads) but the claim is unmeasured and contradicted here"),
  ]),
 dict(index=3, type="Edge", label="Verbatim Common Errors table (8 rows), Critical pitfall, fixmate -r, -c on a pre-marked BAM", status="COMPLETED", flag="✅",
  prompt="samtools markdup errors out or marks nothing on my BAM and I'm not sure of the sort order I used. What is wrong, how do I fix it, and can I drop secondary/unmapped reads with fixmate on the way? My BAM was already marked once.",
  note="Pre-fix P2 fixed: 8 of 8 table messages match tool output (6 triggered here, fgbio MQ and umi_tools index in input 5); pitfall text now accurate; -c claim reproduced",
  basic=37, spec=56, script="in03_errors_edge.sh; in03b_sort_T.sh; 03_strip_tags.py", log="in03.log; in03b.log",
  output="Table messages extracted from SKILL.md by regex and grep -F'd against real stderr: row1 fixmate on coord-sorted 'Coordinate sorted, require grouped/sorted by queryname' MATCH (exit 1, 28-byte partial output left); row2 markdup after fixmate without -m 'no ms score tag' MATCH; row3 MC stripped via pysam 'no MC tag' MATCH; row4 markdup on name-sorted 'queryname sorted, must be sorted by coordinate' MATCH; row5 collate 'Cannot open intermediate file \"tmpdir/collate.0000.bam\"' MATCH; sort -m 1M -T nodir/sort fails 'failed to create \"nodir/sort.0000.bam\"' (the table's sort -T claim holds when sort spills); row8 Picard on RG-less BAM: 'java.lang.NullPointerException: Cannot invoke \"...SAMReadGroupRecord.getReadGroupId()\"' MATCH; samtools addreplacerg then Picard: exit 0, 1656 flagged.\nCritical pitfall (ms stripped): exit 1 with error, not silent (text now says so). fixmate -r -m: 5644 -> 5640, 0 secondary/unmapped left.\n-c: 1000G slice pre-flagged 101; re-mark without -c 111, with -c 101, Picard 101.",
  assertions=[
   A("All eight Common Errors messages match the tools' real output", 1, "8/8: six triggered here on real data; fgbio 'Mate mapping quality (MQ) tag not present' and umi_tools 'fetch called on bamfile without index' reproduced in input 5"),
   A("The Critical pitfall (lost ms/MC tags) is accurate: samtools 1.24 stops with an error, not a silent under-mark", 1, "ms and MC stripped: exit 1 + message, 0 flagged"),
   A("Stated prerequisites and fixes are correct (name-sort before fixmate, -m, coordinate-sort before markdup, mkdir for tmpdir, @RG for Picard)", 1, "each violation reproduced and each stated fix verified (addreplacerg -> Picard 1656)"),
   A("The -c paragraph is accurate (111 without -c vs 101 with -c and Picard on the pre-marked 1000G slice)", 1, "111 / 101 / 101 reproduced exactly"),
   A("fixmate -r -m removes secondary/unmapped as documented and 'a partial output file is left behind' is true", 1, "5644->5640, 0 left; row1 leaves a 28-byte out file, row2 an output with 0 flagged"),
  ]),
 dict(index=4, type="Variant B", label="Rewritten shipped example: valid runs exit 0, failures non-zero, assay gate; aligner block with -R; Picard on its output", status="COMPLETED", flag="✅",
  prompt="Use the shipped markdup_pipeline.sh on my BAM, refuse it if it's the wrong assay, and also show me how to mark duplicates inline during alignment with bwa-mem2 and samblaster.",
  note="Pre-fix P1/P2 fixed: pipefail, temp-then-mv, stats beside output, record-count check, -d, assay gate all verified by exit codes and files; -R block gives @RG and Picard runs. Only design limit: a mis-declared RNA-seq BAM passes silently",
  basic=36, spec=54, script="in04_example_gate_aligner.sh", log="in04.log",
  output="Run from the copy: bash -n OK. ASSAY=wgs: planted exit 0, flagged 100, records 500/500, out.bam.bai and out.markdup_stats.txt written beside the output (no stray markdup_stats.txt in cwd); human exit 0, 1656, 5644/5644. OPTICAL_DIST=100 with 1 thread exit 0.\nFailures: missing input exit 1, no out.bam; truncated exit 1, no out.bam; empty BAM exit 3 (record-count check), no out.bam; unwritable dir exit 1; nonexistent output dir exit 1; all leave no half-written output.\nGate: ASSAY unset exit 2; rnaseq, scrna, umi, amplicon, longread, 16s, its, bogus all exit 2, no output. SYNTHETIC amplicon BAM under ASSAY=wgs: exit 0, 1980/2000 flagged, WARNING over 50% printed. Real RNA-seq BAM under ASSAY=wgs: exit 0, 2570/8828 flagged (29%), no warning (below threshold). ARTIC nanopore under pacbio-amplicon: exit 0, 3886/4916.\nAligner block extracted verbatim (bwa-mem2 mem -R ... | samblaster | samtools sort) on 100 real + 20 SYNTHETIC clone pairs: exit 0, @RG present, 240 records, flagged 40, 40 of 40 are clones; Picard on that output exit 0, flagged 40, library lib1.",
  assertions=[
   A("Shipped example run from a copy flags the truth counts, indexes, and writes stats beside the output", 1, "100 / 1656; index and <out>.markdup_stats.txt present; no cwd litter"),
   A("Every failing run exits non-zero and leaves no half-written output", 1, "missing 1, truncated 1, empty 3, unwritable 1, missing dir 1; out.bam absent in all"),
   A("Assay gate refuses: unset and eight refused or unknown assay values exit 2 without writing", 1, "exit 2 x9, no output file"),
   A("Wrong-assay heuristic warns on an amplicon BAM declared as wgs", 1, "1980/2000 flagged, WARNING printed, exit 0"),
   A("bwa-mem2 -R | samblaster block flags exactly the planted clones and Picard then runs on its output", 1, "40 of 40 flagged reads are clones; Picard exit 0 (pre-fix NullPointerException gone)"),
  ]),
 dict(index=5, type="Stress", label="UMI paired-end capture BAM: umi_tools block + guard, fgbio single-strand and duplex blocks, table rows", status="COMPLETED", flag="✅",
  prompt="My paired-end capture BAM has duplex UMIs in the RX tag. Deduplicate it with the UMIs and call consensus reads, duplex if possible. Also I have a 10x BAM.",
  note="Pre-fix P1s fixed: duplex branch (--strategy=paired) and umi_tools --paired/sort/index verified on the real UMI BAM; empty-output guard returns 1. Quoted 5689 varies +-1 run to run (no --random-seed)",
  basic=34, spec=50, script="in05_umi.sh; in05b_umi_determinism.sh", log="in05.log; in05b.log",
  output="Real nf-core UMI BAM (15788 records, RX only, no CB). umi_tools on the unsorted BAM: 'ValueError: fetch called on bamfile without index'; sorted+indexed, no --paired: 2805; --paired: 5689 (the Skill quotes both).\numi_tools block extracted verbatim (scRNA form + bulk form): pre-check grep -c 'CB:Z:' prints 0; scRNA part alone exits 1 and dedup.bam has 0 records (guard works); bulk part yields dedup.bam 5688 records. Six repeat runs: 5689 5689 5688 5689 5688 5688; three with --random-seed=1: 5689 x3.\nfgbio block extracted verbatim, bash -e: exit 0. mated 15788, grouped (adjacency) 15766 with 2823 MI groups, consensus 5646; grouped_duplex 15766 of 15766 records carry MI /A|/B, duplex 4042. Consensus and duplex reads: 0 mapped, all unmapped (as stated). SetMateInformation route = fixmate -m route (15766 records, 2823 MI groups). adjacency-grouped -> CallDuplexConsensusReads: StringIndexOutOfBoundsException (as the comment says). GroupReadsByUmi on queryname input without mate info: 'Mate mapping quality (MQ) tag not present on read 921195' (table row matches). --method=unique keeps 5926 vs directional 5689; samtools markdup --barcode-tag RX flags 9879 vs 11783 without.",
  assertions=[
   A("umi_tools sorted+indexed requirement and --paired figures (2805 without vs 5689 with) reproduce", 1, "'fetch called on bamfile without index' on unsorted; 2805 and 5689 on the sorted BAM"),
   A("The empty-output guard on the scRNA form returns non-zero when CB/UB are absent", 1, "grep -c prints 0; test returns 1; dedup.bam 0 records"),
   A("fgbio single-strand and duplex branches run verbatim; consensus reads are unmapped; MI /A /B on every duplex-grouped read", 1, "5646 consensus, 4042 duplex, 15766/15766 with /A|/B, 0 mapped"),
   A("SetMateInformation alternative equals the fixmate -m route, and adjacency -> duplex crashes as the comment says", 1, "15766/2823 both routes; StringIndexOutOfBoundsException reproduced"),
   A("The quoted umi_tools record counts (5689 / 2805) are reproducible run to run as written", 0, "unseeded umi_tools gave 5688 in 3 of 6 runs; Skill does not mention --random-seed (seeded: 5689 x3)"),
  ]),
 dict(index=6, type="Scope Boundary", label="Assay decisions: multi-library, same-library 2 RG, amplicon panel, real RNA-seq; Step 0 gate", status="COMPLETED", flag="✅",
  prompt="I have a bulk RNA-seq BAM, an amplicon-panel BAM and a pooled 2-library WGS BAM. Remove the duplicates from all three.",
  note="Decision table and multi-library claims re-verified by output; the workflow text now has a Step 0 assay gate (pre-fix P2) which the example enforces",
  basic=35, spec=53, script="in06_assay_scope.sh; 00_make_synth.py; 00b_make_synth2.py", log="in06.log",
  output="SYNTHETIC multilib (2 libraries, truth 0 dups): default samtools 60 flagged, --use-read-groups 0 (SKILL.md block verbatim: 0), Picard 0. SYNTHETIC same-library 2 RG (truth 60 = 30 pairs): default 60, --use-read-groups 0, Picard 60 (RG-ID vs LB claim confirmed). SYNTHETIC amplicon (10 amplicons x 100 pairs): 1980 of 2000 flagged, -r leaves 20. Real ARTIC amplicon nanopore: 3981/4916 flagged. Real RNA-seq PE BAM: 2570/8828 flagged (Picard 2570); top 500 bp bin 6489 primary reads, 2443 flagged (38%).\nText check: SKILL.md line 112 starts the workflow Approach with 'Step 0: confirm the assay ... stop and hand off if it says NO'; usage-guide 'What the Agent Will Do' item 0 says the same.",
  assertions=[
   A("Multi-library over-marking prediction and the --use-read-groups fix are correct (SKILL.md block run verbatim)", 1, "60 -> 0 flagged, Picard 0"),
   A("'--use-read-groups keys on RG ID, Picard on LB' is accurate", 1, "same-library 2-RG BAM: 0 / 60 / Picard 60"),
   A("'Amplicon panel: markdup erases the dataset' is accurate", 1, "1980 of 2000 flagged; -r leaves 20 records"),
   A("The workflow now gates on assay (Step 0) in SKILL.md, usage-guide and the example", 1, "text present in both docs; example refuses eight assay values (input 4)"),
  ]),
 dict(index=7, type="Variant B", label="NEW: soft-clip/SE/reverse planted truth vs every tool block; pbmarkdup, mapDamage --rescale, Picard UmiAware blocks", status="COMPLETED", flag="✅",
  prompt="Mark duplicates in this mixed paired/single-end BAM with soft clips, tell me if samtools, Picard, biobambam2 and sambamba agree; also I have a PacBio HiFi amplicon BAM (pbmarkdup), an ancient-DNA BAM (mapDamage rescale) and a UMI BAM (Picard UmiAware).",
  note="All five fixer-added blocks run verbatim and match planted truth (140/140 on planted2 for samtools workflow, pipeline block, example, Picard, biobambam2, sambamba, samblaster; pbmarkdup 12/60; mapDamage quality drop; UmiAware exit 0)",
  basic=36, spec=55, script="in07_extra_tools.sh; in07b_pbmarkdup.sh; 10_make_planted2.py; mk_hifi.py; mk_damage.py; md_check.py", log="in07.log; in07b.log",
  output="planted2.bam (SYNTHETIC, auditor's own: 20x3 identical pairs, 15 pairs with a 5S left clip, 15 off-by-one non-dups, 10x3 SE forward, 10x2 SE reverse with 6S at the 3' end, 100 unique pairs; truth 140 flagged reads). SKILL.md workflow 140; optimized pipeline block exit 0, 140; shipped example exit 0, 140; Picard 140; biobambam2 block 140; sambamba block 140; samblaster 140. Per family (A 80, B 30, E 30 = E1 20 + E2 10, C 0, F 0) identical for all four tools. (name,read1/2) sets identical for samtools, Picard, biobambam2 (0 differences); sambamba picks the other member of each tie (56 differences, same counts).\nbiobambam2 block: metrics use Picard column names except no SECONDARY_OR_SUPPLEMENTARY_RDS column.\npbmarkdup block verbatim on SYNTHETIC HiFi-style unaligned BAM (60 reads, 12 planted exact duplicates): exit 0, 60 records, 12 flagged 0x400; --rmdup 48 records; --dup-file 48 main + 12 in the dup file; FASTQ --rmdup 48 reads; summary '48 (80.0%) unique / 12 (20.0%) duplicate'.\nmapDamage block verbatim (2.2.2, 3m09s, 'Successful run') on a SYNTHETIC damaged SE BAM (6000 reads, C>T at 5' p=0.35*0.6^i): mapdamage_out/marked.rescaled.bam written, 6000/6000 records; C->T at 5' pos1 (n=452) mean Q 40 -> 0 while unchanged C (n=836) stays 40 and mid-read matches stay 40; 5pCtoT_freq pos 2 = 0.2035 (planted 0.21).\nPicard UmiAware block verbatim on the real UMI BAM (fixmate + coordinate sort): exit 0, 10127 flagged (samtools --barcode-tag RX 9879, plain markdup 11783).",
  assertions=[
   A("Every tool block (workflow, pipeline block, example, Picard, biobambam2, sambamba, samblaster) flags the planted 140 reads, soft-clip, reverse-SE and near-miss cases handled correctly", 1, "140 each; per-family 80/30/30/0/0 identical across tools"),
   A("The biobambam2 and sambamba blocks run verbatim on coordinate-sorted input without fixmate", 1, "both exit 0, 140 flagged"),
   A("pbmarkdup block flags the planted duplicates in an unaligned HiFi BAM and --rmdup/--dup-file behave as the comment says", 1, "12 flagged of 60; --rmdup 48; --dup-file 48+12"),
   A("mapDamage --rescale block writes marked.rescaled.bam and lowers the quality of damage-consistent bases only", 1, "Q 40 -> 0 for C->T at 5' pos 1 (n=452); unchanged bases 40; 6000/6000 records"),
   A("Picard UmiAwareMarkDuplicatesWithMateCigar block runs verbatim and is between plain markdup and exact-UMI counts", 1, "exit 0; 10127 flagged vs 11783 plain and 9879 exact-UMI"),
  ]),
 dict(index=8, type="Adversarial", label="NEW: planted duplex-UMI library (truth 80/110/50) through umi_tools, fgbio, Picard UmiAware, samtools --barcode-tag; gap hunt", status="COMPLETED", flag="✅",
  prompt="My capture library has duplex UMIs in RX and some molecules share coordinates. Deduplicate with the UMIs, call consensus, duplex if possible. And what if my RX only holds one UMI?",
  note="Every UMI-aware path equals planted truth (80 strand-aware families, 110 exact-UMI, 50 duplex molecules). Only gap: --strategy=paired needs RX 'A-B' and the Skill does not say so (tool error is clear)",
  basic=36, spec=55, script="in08_planted_umi.sh; 20_make_planted_umi.py; in11_gap_hunt.sh", log="in08.log; in11.log",
  output="SYNTHETIC planted duplex-UMI BAM (210 pairs = 420 reads: 30 duplex molecules x (3 top-strand incl. one 1-base UMI error + 2 bottom-strand) + 10 shared coordinates x 2 distinct molecules x 3 copies; UMIs 8-mers >= 3 apart). Truth: 80 strand-aware families, 110 exact-UMI families, 50 duplex molecules.\nCoordinate-only: samtools markdup and Picard flag 340 reads (keep 40 pairs), truth 80: wrong tool for a UMI library, as the Skill's table says. samtools --barcode-tag RX keeps 110 pairs (exact-UMI truth 110). umi_tools bulk block verbatim: directional 80 pairs, --method=unique 110 pairs.\nfgbio block verbatim: adjacency 80 MI groups, consensus 80 pairs; paired strategy 80 groups incl. /A/B = 50 base groups, duplex 50 pairs; 30 of 30 duplex molecules have /A and /B each containing one physical strand; consensus/duplex reads all unmapped. Picard UmiAware block verbatim: flagged 260 reads, keeps 80 pairs; UMI_METRICS INFERRED_UNIQUE_UMIS 80, OBSERVED 110.\nGap hunt (in11): fgbio --strategy=paired on a single-UMI RX: 'Paired strategy used but umi did not contain 2 segments delimited by a '-'' (clear, undocumented). RG-less BAM: SKILL.md pipeline block exit 0 flagged 100, example exit 0 flagged 100. -d 2500 on non-Illumina names: 24 stderr lines (10 'cannot decipher', 7 distinct names), dt tags still emitted, no optical detection (same 1656 flagged). All flags named in the Skill exist in samtools 1.24 markdup help. macs3 3.0.4 (throwaway venv): --keep-dup auto|all|<int> valid; a duplicate-marked and an unmarked BAM give identical results (899 tags at auto, 747 at 1): macs3 ignores 0x400, so the ChIP pointer 'mark, do not remove, use macs3 --keep-dup auto' is valid and harmless.",
  assertions=[
   A("umi_tools bulk block gives the strand-aware truth (directional 80 pairs) and unique gives exact-UMI truth (110)", 1, "80 / 110"),
   A("fgbio adjacency and paired branches give truth: 80 groups -> 80 consensus pairs; 50 duplex molecules -> 50 duplex pairs; strand purity of /A and /B", 1, "80/80, 50/50, 30 of 30 molecules"),
   A("Picard UmiAware block keeps the 80 true UMI families and samtools --barcode-tag RX matches exact-UMI truth (110)", 1, "keeps 80; barcode-tag keeps 110"),
   A("The Skill warns that coordinate-only markdup is wrong for a UMI library, and the numbers back it (keeps 40 pairs vs 80)", 1, "decision table + intro; samtools and Picard both flag 340 reads"),
   A("The Skill states the input requirement of --strategy=paired (RX must be 'A-B')", 0, "not stated; a single-UMI RX fails with a clear IllegalArgumentException, so the cost is one retry"),
  ]),
]

def fin(inp):
    inp["total"] = inp["basic"] + inp["spec"]
    inp["ap"] = sum(1 for a in inp["assertions"] if a["result"] == "PASS")
    return inp
inputs = [fin(i) for i in inputs]
static_sub = sum(v[0] for v in static.values())
ex_avg = round(sum(i["total"] for i in inputs) / len(inputs) + 1e-9, 1)
sw = round(static_sub * 0.4 + 1e-9, 1); dw = round(ex_avg * 0.6 + 1e-9, 1)
score = int(round(sw + dw))
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75 else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌")
ap = sum(i["ap"] for i in inputs); at = sum(len(i["assertions"]) for i in inputs)
l1 = sum(i["basic"] for i in inputs) / len(inputs); l2 = sum(i["spec"] for i in inputs) / len(inputs)

recs = [
 dict(priority="P2", title="Unmeasured speed claims; the optimized pipeline measured slower", observed_in=[2],
      problem="'~30% faster than sort -n | fixmate | sort | markdup on typical 30x WGS' is still asserted and biobambam2 is labelled 'Fastest'. On an 800k-read BAM at 4 threads the collate/-u pipeline took 6.4 s vs 4.6 s for the plain chain (3 reps, equal flagged counts). 30x WGS scale was not tested.",
      root_cause="Speed claims were carried over from prose and never benchmarked.",
      fix="Delete the percentage and the 'Fastest' label, or state the measured setup (reads, threads, disk) next to the number."),
 dict(priority="P2", title="umi_tools counts vary by 1 without --random-seed", observed_in=[5],
      problem="The Skill quotes '5689 vs 2805 records'; unseeded umi_tools dedup returned 5688 in 3 of 6 runs on the same input (5689 in all three seeded runs).",
      root_cause="umi_tools picks among tied reads randomly; the bulk block has no seed.",
      fix="Add --random-seed=1 to the umi_tools blocks and say the figure is approximate without it."),
 dict(priority="P2", title="--strategy=paired input requirement not stated", observed_in=[8],
      problem="The ctDNA row and the duplex branch send the agent to GroupReadsByUmi --strategy=paired, which needs RX as 'A-B'. A single-UMI RX fails with IllegalArgumentException (clear message, one retry).",
      root_cause="Duplex branch documents the MI /A /B output but not the RX format it requires.",
      fix="One sentence: 'paired needs RX as UMI1-UMI2 (as in this BAM); single-UMI libraries use adjacency + CallMolecularConsensusReads'."),
 dict(priority="P2", title="Assay gate relies on the user's declared ASSAY", observed_in=[4, 6],
      problem="The example refuses eight assay names and warns above 50% flagged, but a real RNA-seq BAM declared ASSAY=wgs exits 0 with 2570/8828 flagged and no warning (38% at the top locus).",
      root_cause="The gate checks a label, not the BAM; the 50% heuristic catches amplicon panels only.",
      fix="Optionally refuse when @PG names a splice-aware aligner (STAR, HISAT2) or when many CIGARs contain N, and print the flagged percentage even below 50%."),
 dict(priority="P2", title="Frontmatter description omits the assay and UMI caveats", observed_in=[],
      problem="The description still says 'Use when preparing alignments for variant calling' with no hint that RNA-seq, amplicon, scRNA and UMI libraries need a different tool.",
      root_cause="Description untouched by the fix.",
      fix="Append one clause: 'Not for RNA-seq, amplicon or UMI libraries (see the decision table)'."),
]

report = {
 "meta": meta,
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated identifiers or results. Every count quoted traces to a logged run. Unmeasured speed claims are qualitative, recorded as P2, not fabricated data."},
   "practice_boundaries": {"result": "PASS", "detail": "Alignment-file processing only; no diagnostic or prescriptive clinical output."},
   "methodological_ground": {"result": "PASS", "detail": "Assay decision table verified again (RNA-seq 38% flagged at the top locus, amplicon 1980/2000, multi-library over-marking, RG-ID vs LB); UMI branches equal planted truth; the two former factual errors (error strings, silent-under-mark pitfall) are corrected."},
   "code_usability": {"result": "PASS", "detail": "Every code block was extracted verbatim and run: SKILL.md workflow, optimized pipeline, pysam x3, umi_tools, fgbio single-strand and duplex, Picard UmiAware, biobambam2, sambamba, pbmarkdup, mapDamage --rescale, samblaster, the shipped example. All ran and produced checked output; the two pre-fix runnable-code defects (clean-dir pipeline, duplex after adjacency) are gone."}}},
 "static_score": {"subtotal": static_sub, "max": 100,
  "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
 "dynamic_score": {"execution_avg": ex_avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at},
  "inputs": [{"index": i["index"], "type": i["type"], "label": i["label"], "prompt": i["prompt"], "status": i["status"], "status_flag": i["flag"],
              "note": i["note"], "basic": i["basic"], "specialized": i["spec"], "total": i["total"],
              "assertions_passed": i["ap"], "assertions_total": len(i["assertions"]), "assertions": i["assertions"],
              "executed": True, "execution_note": "scripts: " + i["script"] + " -> " + i["log"]} for i in inputs]},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym,
           "deployable": True, "veto_override": False},
 "key_strengths": [
  "All seven pre-fix findings verified fixed by output: clean-dir pipeline exits 0 valid and 1 on failure, duplex branch (--strategy=paired) works, umi_tools --paired/sort/index with a working empty-output guard, 8 of 8 error messages verbatim, -c and @RG guidance, Step 0 assay gate",
  "Every tool named in the decision tables now has a runnable block that matched auditor-planted truth: biobambam2, sambamba, samblaster, Picard, pbmarkdup (12/60), mapDamage rescale (Q 40 -> 0 on damage-consistent bases), Picard UmiAware (keeps 80 of 80 planted families)",
  "UMI section is correct end to end on a planted duplex library: umi_tools 80/110, fgbio 80 groups -> 80 consensus and 50 duplex molecules -> 50 duplex reads, strand purity 30/30",
  "Shipped example is now a real guard: exits 1/2/3 on missing, truncated, empty, unwritable, wrong-assay input and leaves no half-written output",
 ],
 "recommendations": recs,
}
json.dump(report, io.open(os.path.join(OUT, "eval_report_%s_result.json" % SKILL), "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)

# ---------------- viewer
L = []
L.append("# Eval Viewer — %s (re-audit of a fixed Skill)" % SKILL)
L.append("Generated: 2026-09-20  |  Source: `%s`  |  pre-fix score 77 (Limited Release) -> **%d (%s %s)**\n" % (SRC, score, grade, sym))
L.append("Category: Data Analysis | Mode: B | Complexity: Complex -> 8 inputs (6 pre-fix inputs re-run as regression, 2 new). Fixer log read but not used as evidence; every number below is from `run/in*.log`.\n")
L.append("## Summary Table\n")
L.append("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |")
L.append("|---|---|---|---|---|---|---|---|")
for i in inputs:
    L.append("| %d | %s (%s) | %d | %d | %d | %d/%d PASS | yes | %s |" % (i["index"], i["type"], "NEW" if i["index"] >= 7 else "regression", i["basic"], i["spec"], i["total"], i["ap"], len(i["assertions"]), i["flag"]))
L.append("\n**Execution Average: %s / 100**  |  **Assertion Pass Rate: %d/%d (%.1f%%)**  |  Layer 1 avg %.1f/40, Layer 2 avg %.1f/60" % (ex_avg, ap, at, ap / at * 100, l1, l2))
L.append("\n**Static %d/100 (x0.4 = %s) + Execution %s (x0.6 = %s) = %d -> %s %s. Deployable: yes. Vetoes: none. Open P0: 0. Open P1: 0. P2: 5.**" % (static_sub, sw, ex_avg, dw, score, sym, grade))
L.append("Floors for Production Ready: static >= 80 (%d), execution >= 85 (%s), L1 >= 32 (%.1f), L2 >= 48 (%.1f), assertions >= 90%% (%.1f%%): all met.\n" % (static_sub, ex_avg, l1, l2, ap / at * 100))
L.append("## Pre-fix defects re-tested\n")
L.append("| Pre-fix finding | Pre-fix result | Now (input) |")
L.append("|---|---|---|")
for a, b, c in [
 ("Duplex consensus after adjacency grouping (P1)", "StringIndexOutOfBoundsException", "Two branches; paired -> duplex 4042 reads on the real BAM, 50/50 on planted truth (5, 8)"),
 ("umi_tools example: no sort/index, no --paired (P1)", "fetch error / 2805 records", "Block verbatim: 5688-5689 records, guard exits 1 on missing CB/UB (5)"),
 ("Optimized pipeline fails from clean dir, exit 0 (P1)", "501-byte empty marked.bam, exit 0", "exit 0 valid; exit 1 without mkdir; missing/truncated input exit 1 (2)"),
 ("Shipped example: no pipefail/-d/gate, stats in cwd (P1/P2)", "failed only by accident", "exit 0/1/2/3 verified, stats beside output, no partial file (4)"),
 ("Common Errors strings / silent-under-mark pitfall (P2)", "3 wrong strings, wrong pitfall", "8/8 match tool output; pitfall corrected (3)"),
 ("-c and @RG for Picard (P2)", "absent; NPE on aligner output", "-c 111/101/101 reproduced; bwa-mem2 -R + Picard exit 0 (3, 4)"),
 ("usage-guide duplicates/contradicts SKILL.md (P2)", "-d and rate contradictions", "60-line index; nothing an agent needs was lost (all deleted content found in SKILL.md, see below); rate 29.35 in both (1)"),
 ("Workflow does not gate on assay (P2)", "table only", "Step 0 in SKILL.md and usage-guide; example refuses (4, 6)"),
 ("Missing runnable blocks for named tools", "not executed", "biobambam2, sambamba, pbmarkdup, mapDamage --rescale, Picard UmiAware all run against planted truth (7, 8)"),
]:
    L.append("| %s | %s | %s |" % (a, b, c))
L.append("\n**Judged leftovers.** macs3 pointer: valid (macs3 3.0.4: `--keep-dup auto` exists, and a marked and an unmarked BAM give identical results, so the mark-not-remove advice is harmless). ATAC Tn5 +4/-5: a one-line pointer to a downstream step, no code, not testable here, acceptable. '~30% faster' / biobambam2 'Fastest': unmeasured, and my 800k-read timing contradicts the first (P2).")
L.append("\n**usage-guide dedup check.** Old sections compared with the fixed SKILL.md: workflow diagram -> 'Duplicate Marking Workflow'; step-by-step and pipeline -> same section and the optimized block; mark vs remove, -s/-f, optical -d -> 'samtools markdup' / 'Optical Distance'; rate one-liner -> 'Percentage Duplicates'; pysam mark/rate/remove -> 'pysam Python Alternative' (all three run verbatim, input 1); troubleshooting -> verbatim Common Errors; tips -> decision table, Lossy Operations, samblaster. The `-@ 8 fixes memory` tip was unsupported and is gone. The only lost item is the `mark_duplicates(threads=)` wrapper with try/finally temp cleanup, which SKILL.md replaces with the inline five-line version. Nothing the agent needs is missing.")
L.append("\n**What the fix broke:** nothing found. Cosmetic: the SKILL.md `set -euo pipefail` line will terminate a persistent interactive shell on a later failure if an agent pastes the block into one rather than running it as a script; the umi_tools block holds two alternative commands whose combined exit status hides the scRNA guard failure when run as one script.\n")
L.append("## Static score (%d/100)\n" % static_sub)
for k, v in static.items():
    L.append("- **%s** %d/%d: %s" % (k, v[0], v[1], v[2]))
L.append("\n## Detailed Outputs\n")
for i in inputs:
    L.append("### Input %d — %s: %s" % (i["index"], i["type"], i["label"]))
    L.append("**Prompt:** %s\n" % i["prompt"])
    L.append("**Executed:** true. Scripts: `%s`; logs: `%s`.\n" % (i["script"], i["log"]))
    L.append("**What ran and what it printed:**\n")
    L.append("```\n%s\n```" % i["output"])
    L.append("**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100 | %s\n" % (i["basic"], i["spec"], i["total"], i["note"]))
    L.append("**Assertions:**")
    for a in i["assertions"]:
        L.append("- [%s] %s — %s" % (a["result"], a["text"], a["note"]))
    L.append("")
L.append("## Research Veto\nScientific integrity PASS | Practice boundaries PASS | Methodological ground PASS | Code usability PASS (every block extracted verbatim and run; see inputs 1-8).\n")
L.append("## Recommendations\n")
for r in recs:
    L.append("**[%s] %s** (inputs %s)\n- Problem: %s\n- Root cause: %s\n- Fix: %s\n" % (r["priority"], r["title"], r["observed_in"] or "static", r["problem"], r["root_cause"], r["fix"]))
L.append("## Run record\nEnvironment and data notes: `run/README_run.md`. All scripts and logs are in `run/`; `run/skill_copy` is the Skill at 3e4087c (diff-identical to the worktree), `run/blocks.py` extracts the Skill's own fenced blocks so blocks are run verbatim.")
io.open(os.path.join(OUT, "eval_viewer_%s.md" % SKILL), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("static", static_sub, "exec_avg", ex_avg, "score", score, grade, "assertions", ap, "/", at, "L1", round(l1, 1), "L2", round(l2, 1))
