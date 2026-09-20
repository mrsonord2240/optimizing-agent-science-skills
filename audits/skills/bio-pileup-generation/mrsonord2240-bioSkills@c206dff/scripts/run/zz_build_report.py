#!/usr/bin/env python3
"""Builds eval_report_bio-pileup-generation_result.json and eval_viewer_bio-pileup-generation.md from the scores decided in the audit and
the logs produced by in0*.py (this script only assembles and validates; the numbers come from the logged runs)."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
SKILL = "bio-pileup-generation"

def rd(name, n=None, width=300):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return ""
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    lines = [l[:width] + (" ..." if len(l) > width else "") for l in lines]
    return "\n".join(lines[:n] if n else lines)

meta = {
    "skill_name": SKILL,
    "description": "Generate pileup data for variant calling using samtools mpileup and pysam. Use when preparing data for variant calling, analyzing per-position read data, or calculating allele frequencies.",
    "evaluated_on": "2026-09-20",
    "evaluator_version": "skill-auditor@1.0",
    "category": "Data Analysis",
    "execution_mode": "D",
    "complexity": "Moderate",
    "n_inputs": 5,
    "source": "mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/pileup-generation",
    "executed": "5/5 inputs executed",
    "execution_note": "WSL science env alignment-files (TOOLS.md): samtools 1.24, bcftools 1.24, pysam 0.24.1. The Skill's python functions were loaded verbatim from the copied SKILL.md/usage-guide.md (run/snippets.py) and the shipped examples/allele_counts.py was run from the copy in run/skill. Real data: nf-core human chr22 slice (DNA and STAR RNA-seq), ARTIC v5.3.2 nanopore BAM + MN908947.3, 1000G HG00349 chr20 slice, plus labelled synthetic planted-truth BAMs in run/data. Skill commit c206dff (folder unchanged since; staging HEAD 85a3e4d). Nothing written into the external clone (no __pycache__ found).",
}

veto_gates = {
    "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
    "research_veto": {
        "applicable": True,
        "gate": "PASS",
        "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOIs, trial results, p-values or sample sizes. The one unsourced number ('BAQ ~30% slower') was measured at +150-180% on the audit data, which is a wrong performance claim, not fabricated scientific evidence."},
        "practice_boundaries": {"result": "PASS", "detail": "No diagnostic or prescriptive content; the Skill steers somatic, ctDNA and germline WGS/WES production work to Mutect2 / DeepVariant / HaplotypeCaller instead of mpileup, which is the correct boundary."},
        "methodological_ground": {"result": "PASS", "detail": "No principled fallacy. The published rationale for the 'WRONG' samtools|bcftools pipe (double depth cap) is factually wrong (bcftools call rejects a text pileup as an unknown file type) and pysam column.n is reported as depth, but the recommended bcftools mpileup route reproduced planted truth exactly (AD 30,10; per-sample AD 17,3 / 8,12)."},
        "code_usability": {"result": "PASS", "detail": "All Skill functions and the shipped example parse and ran (5/5 inputs executed, pysam 0.24.1). They are runnable but three helpers give silently wrong output (pileup_text depth column and missing markers, allele_counts labelling ref-skips as DEL, 'Basic Pileup' printing out-of-region columns); these are scored in Layer 2 and as P1 rather than as a veto because M4 covers unrunnable code."},
    },
}

static = {
    "functional_suitability": (8, 12, "Completeness 3 (text pileup, region/BED, multi-BAM, filters, -d/BAQ/overlap traps, bcftools calling, pysam counting all present; default -Q 13, default excluded flags, indel counting and --output-QNAME/-s are absent), correctness 2 (CLI facts verified: -d 8000/250, -g removal, --max-BQ ont preset, -x aliases, cheat-sheet flags; but pysam n-as-depth, is_del before is_refskip, wrong 'WRONG'-pipe rationale, 'No sequences in common' text, exome -d 250 contradiction), appropriateness 3"),
    "reliability": (7, 12, "Fault tolerance 2 (3-row Common Errors table; example script has only an argc check), error reporting 2 (example dies with raw ValueError tracebacks on ':' contigs, ranges, no index, unknown contig; mismatched reference makes samtools exit 0 and the Skill quotes a different message), recoverability 3 (read-only tools, safe to re-run)"),
    "performance_context": (5, 8, "SKILL.md 375 lines plus usage-guide.md 258 lines; allele counting, bcftools pipelines and pysam blocks are repeated in both (token cost 2); workflows themselves are linear (efficiency 3)"),
    "agent_usability": (10, 16, "Learnability 3, consistency 2 (0-based function arguments vs 1-based 'chr1:1000000' prompts, n vs pileups for 'depth', format examples with depth 15 and 11 quality chars), feedback design 2 (no expected outputs or self-checks for pipelines), error prevention 3 (good traps: -d cap, BAQ, -A, -aa, overlap, removed -g/-u; but not default -Q, excluded flags, pysam defaults)"),
    "human_usability": (5, 8, "Description matches how users ask (pileup for variant calling, allele frequency); forgiveness 2: strict region strings, no clarification of coordinate base"),
    "security": (11, 12, "No credentials, no eval/exec, no shell built from user strings; example script does not validate its region argument (3)"),
    "maintainability": (8, 12, "Modularity 3 (SKILL.md + usage-guide + one example), modifiability 3, testability 2 (one example, no expected outputs or tests; it is the only shipped code and it is fragile)"),
    "agent_specific": (15, 20, "Trigger precision 3, progressive disclosure 2 (no references/ dir; usage-guide duplicates SKILL.md), composability 3 (Related Skills all exist), idempotency 4 (read-only), escape hatches 3 (points to Mutect2/DeepVariant/HaplotypeCaller/Sniffles for out-of-scope work)"),
}

def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
    {
        "index": 1, "type": "Canonical",
        "label": "Text pileup of real human BAM (region, -q/-Q, BED) cross-checked against samtools depth, pysam and bcftools",
        "prompt": "Generate a text pileup for chr22:1952-4617 of my BAM (nf-core human test slice) with MAPQ>=20 and baseQ>=20, tell me what each column and symbol means, and check the depth against another tool.",
        "executed": True,
        "execution_note": "run/in01_real_mpileup.py (WSL): SKILL commands `samtools mpileup -f ref -r/-l/-q/-Q`, 2 BAMs; 22/24 checks passed. The 2 failed checks are the pysam n-vs-depth claim and a bcftools-vs-samtools depth nuance.",
        "status": "COMPLETED", "status_flag": "✅",
        "note": "CLI half verified exactly; pysam `pileup_column.n` (used as depth in every pysam example) differs from mpileup depth at 1087/1157 positions (sum 670718 vs 353910); default -Q 13, default excluded flags and depth-0 rows are not documented",
        "basic": 31, "specialized": 46, "total": 77,
        "assertions": [
            A("mpileup -r output has 6 columns, col3 equals the FASTA base, and depth == read symbols == quality characters at every non-zero row", True, "1157 rows; base-column parsed by an independent decoder"),
            A("-q / -Q behave as documented: mpileup depth equals an independent pysam count for -q 20/60 and -Q 20/30, and all-filters-off depth equals samtools depth -a -J and pysam at 2666 positions", True, "0 differing positions in every comparison; max depth 2532"),
            A("Skill states the defaults that change what the pileup shows (-Q 13, excluded flags UNMAP,SECONDARY,QCFAIL,DUP, zero-depth rows with '*')", False, "None of the three is mentioned; 3 depth-0 rows appear at chr22:1952-1954 in the default output"),
            A("pysam `pileup_column.n` printed as depth equals the samtools mpileup depth column under default arguments", False, "n ignores overlap removal and min_base_quality; len(column.pileups) matches mpileup -B exactly, n does not (1087/1157 positions differ)"),
            A("Region, BED and multi-BAM syntax works as the Skill shows (0-based half-open BED -> 1-based rows; 9 columns for 2 BAMs)", True, "BED 2999-3003 gave rows 3000-3003; the Skill's '6 columns per sample' is imprecise (3 + 3N)"),
        ],
    },
    {
        "index": 2, "type": "Variant A",
        "label": "pysam allele counts / frequency / find_variants / pileup_text on planted-truth synthetic BAM and real BAM",
        "prompt": "Count the alleles and alt fraction at synA:100 (planted SNP) and at real chr22 positions with pysam, make a per-position pileup text, and list positions with >10% alternative alleles.",
        "executed": True,
        "execution_note": "run/in02_pysam.py (WSL, pysam 0.24.1): SKILL.md and usage-guide.md functions loaded verbatim via ast; 16/29 checks passed. examples/allele_counts.py run from the copy.",
        "status": "COMPLETED", "status_flag": "⚠️",
        "note": "allele_counts/allele_frequency/find_variants/example are right for SNPs (equal to mpileup at 106 real positions); pileup_text disagrees with its own depth in 31 rows, omits ^ $ indels and qualities; ref-skips are counted as DEL; indels invisible",
        "basic": 27, "specialized": 38, "total": 65,
        "assertions": [
            A("allele_counts, allele_frequency, count_alleles and find_variants recover the planted SNP (T 30 / C 10, 25%) with no false variants, and allele_counts equals samtools mpileup -B at 106 real positions", True, "find_variants on the real chr22 BAM equals an independent mpileup -B -Q20 parse (4 sites, same counts)"),
            A("Shipped examples/allele_counts.py (run from a copy) prints T: 30 (75.0%), C: 10 (25.0%) and total depth 40; on real chr22:3000 total depth 781 equals mpileup -B -q20 -Q20", True, "runs from a clean copy; the 1-based -> 0-based conversion is correct"),
            A("pileup_text output is consistent with samtools mpileup (depth column == bases column, same symbols, ^/$/indel text, 6-column format)", False, "5 columns (no qualities); depth != symbol count in 31 rows (uses pileup_column.n); no ^ $ or +/-; 200 spliced positions differ"),
            A("Ref-skips (spliced reads) are treated as skips, not deletions", False, "pysam sets is_del=True for N-skips, the Skill tests is_del first: allele_counts reports {'DEL': 3} at synA:400 and pileup_text writes '***' where mpileup shows '>><'; the is_refskip branch is dead code"),
            A("Module-level snippets print what they claim ('Basic Pileup' region columns; 'Pileup with Quality Filtering' depth)", False, "'Basic Pileup' (no truncate=True) prints 50 columns 80-129 for a 10-column request; with min_base_quality=20 the printed n=10 at synA:725 although only 4 bases pass"),
        ],
    },
    {
        "index": 3, "type": "Edge",
        "label": "Exact symbol decoding and silent defaults on planted synthetic BAM; shipped example on edge inputs",
        "prompt": "Explain exactly how insertions, deletions, spliced reads, read starts/ends and soft clips appear in the pileup base column and which reads mpileup drops by default (flags, MAPQ, baseQ, overlaps, orphans, max depth); my amplicon library is 9000x deep. Then run the example script on unusual region strings.",
        "executed": True,
        "execution_note": "run/in03_edge_symbols_defaults.py (35/35 checks passed) and run/in03b_example_script_edges.py (4/9 passed, raw ValueError tracebacks) on run/data (synthetic, truth in truth.json).",
        "status": "COMPLETED", "status_flag": "✅",
        "note": "Symbol table, -d 8000/250, -d 0, overlap, -A, -a/-aa all verified against planted truth; default BAQ drops the deletion evidence (depth 8 -> 4, no -3CGT marker) which the Skill only hints at; cheat-sheet -d 250 contradicts its own warning; example script fails with tracebacks on ':' contigs, ranges, commas, no index",
        "basic": 30, "specialized": 45, "total": 75,
        "assertions": [
            A("Base-column symbol table matches planted truth: '.'/',' by strand, ACGT/acgt mismatches (6 C + 4 c), ^] at read start (MAPQ 60+33), $, +2AC/+2ac, -3CGT, '*', '>'/'<' for N-skips, soft clips absent", True, "Decoded with an independent parser; notation '+NNN' in the Skill's table is loose (actual +2AC), '#' (--reverse-del) not mentioned"),
            A("Depth-cap, overlap and orphan claims hold: samtools default 8000 (9000 reads -> 8000), -d 0 unlimited, bcftools default 250, -x/--disable-overlap-removal/--ignore-overlaps change depth 5 -> 10, -A restores orphans, -aa adds read-less contigs", True, "all values reproduced exactly on deep.bam / syn.bam"),
            A("Cheat-sheet settings are consistent with the Skill's own 'Critical Trap' about silent depth truncation", False, "'Capture / exome: -q 20 -Q 20 -d 250' caps a 9000x amplicon-like column at 250; usage-guide 'Memory Issues' also suggests -d 500"),
            A("Skill documents the defaults that silently remove evidence (excluded flags DUP/SECONDARY/QCFAIL, -Q 13, BAQ hiding the planted deletion)", False, "default text pileup shows depth 4 and no deletion marker at synA:250 versus 8 and '-3CGT' with -B; flags and -Q default not stated"),
            A("Shipped example handles realistic region strings without raw stack traces", False, "'HLA-A*01:01:01:01:50' -> ValueError too many values; 'synA:100-110', 'synA:1,000' -> int() ValueError; unindexed BAM and unknown contig -> raw ValueError"),
        ],
    },
    {
        "index": 4, "type": "Variant B",
        "label": "bcftools mpileup | call: single sample, BCF intermediate, two-sample joint, parallel by chromosome, and the 'WRONG' pipe",
        "prompt": "Call variants from my BAM with the modern bcftools mpileup | bcftools call pipeline (single sample, BCF intermediate, joint calling of 2 samples, parallel per chromosome) and tell me if `samtools mpileup | bcftools call` is really wrong and why.",
        "executed": True,
        "execution_note": "run/in04_bcftools_pipeline.py (WSL, bcftools 1.24): 17/19 checks passed on planted SNP/ins/del (syn.bam), 2-sample s1/s2, 11-contig multi.bam, real human chr22.",
        "status": "COMPLETED", "status_flag": "⚠️",
        "note": "Recommended pipelines reproduce truth exactly (AD 30,10; per-sample AD 17,3 / 8,12; ins and del called); the stated reason the samtools|bcftools pipe is 'WRONG' is false and the parallel-loop concat glob writes contigs out of header order with exit 0",
        "basic": 30, "specialized": 44, "total": 74,
        "assertions": [
            A("'Modern Germline Calling' pipeline (-d 1000000 -q 20 -Q 20 --annotate FORMAT/AD,DP,SP,INFO/AD | call -mv, index -t) calls the planted SNP with AD 30,10 / DP 40, the 2 bp insertion and the 3 bp deletion", True, "synA:100 T>C AD=30,10 DP=40; synA:200 AA>AACA; synA:250 TCGT>T; plus synA:930 from the planted conflicting-overlap site"),
            A("Multi-sample joint calling with --threads 4 gives per-sample AD matching planted truth and sample names from @RG SM", True, "AD s1 17,3 and s2 8,12; usage-guide BCF-intermediate route and `bcftools index` also ran"),
            A("The reason given for the 'WRONG' pipe (samtools 8000 cap then bcftools 250 cap re-applied) is correct", False, "bcftools call applies no depth cap; the pipe fails because a text pileup is not VCF/BCF: 'Failed to read from standard input: unknown file type'"),
            A("usage-guide parallel-by-chromosome loop (`bcftools concat ... chr*.vcf.gz`) yields a VCF in header contig order when extended past chr3", False, "11 contigs: records chr1,chr10,chr11,chr2,...,chr9 while the header lists chr1..chr11; exit 0 and `bcftools index` still succeeds"),
            A("Flags and tags named in the Skill exist in bcftools 1.24 (FORMAT/AD,DP,SP, INFO/AD, --max-BQ, ont preset value 30, --ignore-overlaps, --threads); samtools mpileup -g/-u are rejected", True, "-X list shows `ont: -B -Q5 --max-BQ 30 -I`; samtools: 'invalid option -- g'"),
        ],
    },
    {
        "index": 5, "type": "Stress",
        "label": "Library-typed flag cheat-sheet on real ARTIC nanopore, spliced RNA-seq and 1000G germline BAMs; reference-mismatch handling",
        "prompt": "Apply the library-typed flag cheat-sheet to my ARTIC SARS-CoV-2 nanopore amplicon BAM (consensus needs zero-coverage rows), an RNA-seq BAM and a 1000G germline BAM, and tell me what happens when the reference does not match the BAM.",
        "executed": True,
        "execution_note": "run/in05_library_flags_real.py and in05b_misc_claims.py (WSL): 23/27 + 4/5 checks; real data only (ARTIC v5.3.2 BAM + MN908947.3, STAR RNA BAM, HG00349 chr20), BAM copies indexed in run/work and deleted afterwards.",
        "status": "COMPLETED", "status_flag": "⚠️",
        "note": "All 8 cheat-sheet rows run and ARTIC/1000G outputs match independent counts; real RNA-seq reveals allele_counts reporting 54 'DEL' at an intron with zero deletions; reference mismatch exits 0 with 'N' bases; '-aa required' and '~30% slower' claims do not hold",
        "basic": 29, "specialized": 43, "total": 72,
        "assertions": [
            A("Every cheat-sheet row (germline, tumor, ARTIC, exome, ONT, HiFi, RNA-seq, aDNA) and `bcftools mpileup ... --max-BQ 30` is accepted by samtools/bcftools 1.24 and produces rows", True, "8/8 samtools rows and the bcftools ONT variant ran"),
            A("Real-data outputs match independent computations: ARTIC -aa gives 29903 rows with depth (minus '*') == pysam count at every position; 1000G all-filters-off depth == pysam count; RNA-seq shows '>'/'<' (68805/369205 slots)", True, "0 differing positions; 77 zero-depth ARTIC rows only with -a/-aa"),
            A("The Skill's pysam allele counter treats ref-skips in real spliced RNA-seq reads as skips", False, "at chr22:25548 mpileup shows 3 '>' + 45 '<' and 0 '*', allele_counts returns {'DEL': 54, 'G': 5}"),
            A("Reference-mismatch guidance matches the tool: 'No sequences in common' / non-zero exit", False, "actual: `[E::faidx_adjust_position] The sequence \"MN908947.3\" was not found`, exit status 0, 4.2 MB pileup of 'N' reference rows written by `> pileup.txt`"),
            A("Stated facts hold: '-aa is required for ARTIC' and 'BAQ ~30% slower'", False, "-a already emits the same 29903 rows for a single-contig BAM (-aa only adds read-less contigs); BAQ default cost +152% (1000G) and +178% (human slice) vs -B"),
        ],
    },
]

recs = [
    {"priority": "P1", "title": "pysam examples print pileup_column.n as depth", "observed_in": [1, 2],
     "problem": "`pileup_column.n` ignores overlap removal and min_base_quality: on the real human BAM it differs from samtools mpileup depth at 1087 of 1157 positions (sum 670718 vs 353910), and pileup_text writes a depth column that disagrees with its own base column in 31 of 623 synthetic rows.",
     "root_cause": "The pysam blocks were written as if n equalled the mpileup depth column and never compared with mpileup output.",
     "fix": "Report len(pileup_column.pileups) (or get_num_aligned()) as depth, and add a pysam-to-samtools parameter table: truncate=True, stepper='samtools' plus fastafile for BAQ, min_base_quality default 13, ignore_overlaps True, max_depth 8000, compute_baq."},
    {"priority": "P1", "title": "Ref-skips counted as deletions in every pysam helper", "observed_in": [2, 5],
     "problem": "pysam sets is_del=True on N-skips, and every helper tests is_del first, so allele_counts reports 'DEL' for spliced reads ({'DEL': 3} at synA:400; {'DEL': 54, 'G': 5} at a real RNA-seq intron with 0 deletions) and pileup_text writes '*' instead of '>'/'<'; the is_refskip branch is dead code.",
     "root_cause": "Branch order assumes is_del and is_refskip are exclusive.",
     "fix": "Test `pileup_read.is_refskip` before `is_del` in allele_counts, allele_frequency, pileup_text and both usage-guide functions."},
    {"priority": "P1", "title": "pileup_text is not a pileup: no ^ $ indels or qualities", "observed_in": [2],
     "problem": "The 'Generate Pileup Text' helper emits 5 columns, no read-start/end markers, no +N/-N indel text, no quality column, and 200 of 623 synthetic positions differ from samtools mpileup (spliced positions).",
     "root_cause": "Simplified re-implementation of mpileup presented under the same heading as the 6-column format.",
     "fix": "Either add the quality column, ^/$ and indel text using pileup_read.indel, or retitle it 'simplified base string' and point to samtools mpileup for the real format."},
    {"priority": "P1", "title": "Defaults that change the output are undocumented", "observed_in": [1, 3, 5],
     "problem": "The Skill never gives samtools mpileup's default -Q 13 (bcftools: 1), the default excluded flags UNMAP,SECONDARY,QCFAIL,DUP (1000G BAM: 101 duplicate-flagged reads silently dropped), the depth-0 '*' rows, or that default BAQ removes bases beside a deletion (planted 3 bp deletion: depth 8 -> 4, no '-3CGT' marker unless -B).",
     "root_cause": "Only -d, BAQ on/off and -A are treated as traps; the rest of the default filter set is left implicit.",
     "fix": "Add a 'What mpileup drops by default' table (flags, -q 0, -Q 13, orphans, overlap removal, -d 8000, BAQ) with the --ff/--rf, -Q, -x, -A, -B overrides."},
    {"priority": "P1", "title": "'WRONG' pipe rationale false; parallel concat order broken", "observed_in": [4],
     "problem": "samtools mpileup | bcftools call fails because a text pileup is not VCF/BCF ('unknown file type'), not from a double depth cap; and `bcftools concat chr*.vcf.gz` puts contigs in lexicographic order (chr1,chr10,chr11,chr2...), silently, with exit 0 and a valid index.",
     "root_cause": "Rationale written from memory of the removed `mpileup -u` pipeline; loop shown with 3 contigs so the glob looks harmless.",
     "fix": "Reword the comment to 'samtools mpileup output is text and cannot feed bcftools call'; build the concat file list in header order (`bcftools view -h ref | ...` or `samtools idxstats | cut -f1`) and add `set -e`/wait status checks."},
    {"priority": "P1", "title": "Reference mismatch does not fail: exit 0 with N reference", "observed_in": [5],
     "problem": "With a FASTA missing the BAM contig samtools mpileup prints `The sequence \"MN908947.3\" was not found`, still writes 4.2 MB of rows with reference base N and exits 0; the Skill's Common Errors and Troubleshooting rows quote different text ('No sequences in common', 'Reference mismatch').",
     "root_cause": "Error text and behaviour not checked against samtools 1.24.",
     "fix": "Document the real message and exit status and add a `samtools view -H | grep @SQ` vs `.fai` contig-name check before running (mpileup without -f also succeeds with N, so 'No FASTA reference' is not an error)."},
    {"priority": "P2", "title": "Cheat-sheet exome row contradicts the depth warning", "observed_in": [3],
     "problem": "`-d 250` for capture/exome (and usage-guide `-d 500` for memory) silently caps depth at 250/500 (reproduced: 9000 reads -> 250) right after a 'Critical Trap' section warning about silent truncation.",
     "root_cause": "Cheat-sheet rows copied from bcftools defaults.", "fix": "Use `-d 0` or a documented high cap for capture, or state the expected coverage at which the cap is safe."},
    {"priority": "P2", "title": "'Basic Pileup' snippet prints out-of-region columns; 0/1-based ambiguity", "observed_in": [2],
     "problem": "`bam.pileup('chr1', 1000000, 1001000)` without truncate=True prints 50 columns for a 10-column request; SKILL.md functions take 0-based pos while prompts say 'chr1:1000000' (calling allele_counts(..., 100) for 1-based 100 silently returns the neighbour base).",
     "root_cause": "truncate=True and the coordinate convention appear only in some blocks and in usage-guide Tips.", "fix": "Add truncate=True to the first snippets and state '0-based pos; pass position-1' in the SKILL.md function docstrings."},
    {"priority": "P2", "title": "Shipped example fails with raw tracebacks on common inputs", "observed_in": [3],
     "problem": "examples/allele_counts.py raises ValueError for contigs containing ':' (HLA-A*01:01:01:01, real UMI BAM contig), 'chr:100-110', 'chr:1,000', an unindexed BAM and an unknown contig.",
     "root_cause": "region.split(':') without validation or try/except.", "fix": "Use rsplit(':', 1), strip commas, catch ValueError and print a one-line message naming the missing index or contig."},
    {"priority": "P2", "title": "Unverified or overstated statements", "observed_in": [5],
     "problem": "'BAQ ~30% slower' measured +152% / +178%; '-aa is required for ARTIC' is true only for multi-contig or read-less references (-a gives identical 29903 rows); '(computed from CIGAR if MD missing)' is not how mpileup BAQ works (reference-based HMM, no MD needed); format examples show depth 15 with 11 quality characters; '+NNN'/'-NNN' should read +2AC / -3CGT.",
     "root_cause": "Numbers and notation not checked against tool output.", "fix": "Remove or source the numeric claim, say '-a is enough for a single contig; -aa adds read-less contigs', and correct the format examples."},
    {"priority": "P2", "title": "Indels invisible in pysam counters; prompts steer to removed -g", "observed_in": [2],
     "problem": "allele_counts/find_variants never read pileup_read.indel, so the planted 2 bp insertion and 3 bp deletion are never reported although the Skill lists 'SNP/indel detection'; usage-guide example prompts 'Call variants using samtools mpileup and bcftools' and 'Generate BCF file' point at the removed mpileup -g route.",
     "root_cause": "Helpers written for SNPs only; prompts predate the deprecation note.", "fix": "Add an indel branch (pileup_read.indel) or state SNP-only scope; reword the two prompts to bcftools mpileup."},
    {"priority": "P2", "title": "SKILL.md and usage-guide.md duplicate the same recipes", "observed_in": [],
     "problem": "Allele counting, frequency, quality filtering, region/BED, bcftools pipelines and depth advice are written twice (375 + 258 lines) with small divergences (-d 250 vs 1000000 in multi-sample examples).",
     "root_cause": "usage-guide restates SKILL.md.", "fix": "Keep the command reference in SKILL.md and reduce usage-guide.md to prompts and troubleshooting."},
]

key_strengths = [
    "The bcftools pipeline guidance is correct and complete for small germline calling: planted SNP/ins/del recovered with exact AD (30,10), correct per-sample AD for two samples, valid annotate tags, --max-BQ 30 ont preset value and the removal of samtools mpileup -g/-u all verified on bcftools/samtools 1.24.",
    "Traps that matter are called out and were reproduced exactly: samtools -d 8000 vs bcftools -d 250 truncation, BAQ, -A for non-proper pairs, overlap removal (-x / --ignore-overlaps), -a/-aa zero-depth rows.",
    "Base-symbol table (. , ACGT acgt ^Q $ * > <) decodes correctly against planted truth, and all 8 library-typed flag rows are accepted by the installed tools and produced rows that match independent counts on real ARTIC, RNA-seq and 1000G BAMs.",
    "allele_counts / allele_frequency / find_variants and the shipped example give exact results for SNPs (equal to samtools mpileup -B at 106 real positions) and the example runs from a clean copy; every Related Skill path exists.",
]

# ---- numbers
static_sub = sum(v[0] for v in static.values())
tot = [i["basic"] + i["specialized"] for i in inputs]
for i, t in zip(inputs, tot):
    i["total"] = t
    assert t == i["total"]
    i["assertions_passed"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")
    i["assertions_total"] = len(i["assertions"])
    assert 3 <= i["assertions_total"] <= 5
avg = round(sum(tot) / len(tot), 1)
sw = round(static_sub * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(sw + dw)
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75 else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌")
passed = sum(i["assertions_passed"] for i in inputs)
totala = sum(i["assertions_total"] for i in inputs)

rep = {
    "meta": meta,
    "veto_gates": veto_gates,
    "static_score": {"subtotal": static_sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
    "dynamic_score": {
        "execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": totala},
        "inputs": [{k: i[k] for k in ("index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions", "executed", "execution_note")} for i in inputs],
    },
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym,
              "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
    "key_strengths": key_strengths,
    "recommendations": recs,
    "source": meta["source"],
}
assert static_sub == sum(c["score"] for c in rep["static_score"]["categories"].values())
assert all(0 <= c["score"] <= c["max"] for c in rep["static_score"]["categories"].values())
assert [r["priority"] for r in recs] == sorted(r["priority"] for r in recs)
assert 2 <= len(key_strengths) <= 5 and len(rep["static_score"]["categories"]) == 8 and len(inputs) == meta["n_inputs"]
json.dump(rep, open(os.path.join(OUT, f"eval_report_{SKILL}_result.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("static", static_sub, "avg", avg, "sw", sw, "dw", dw, "score", score, grade, "assertions", passed, "/", totala)

# ---- floors
l1 = round(sum(i["basic"] for i in inputs) / 5, 1); l2 = round(sum(i["specialized"] for i in inputs) / 5, 1)
print("L1 avg", l1, "L2 avg", l2)

# ---- viewer
V = []
w = V.append
w(f"# Eval Viewer — {SKILL}\n")
w("Generated: 2026-09-20  |  Auditor: fresh Sonnet (audit stage, first audit)  |  Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/pileup-generation`\n")
w("Env: WSL `science`, env `alignment-files` (samtools 1.24, bcftools 1.24, pysam 0.24.1). Skill folder copied to `run/skill/` and run from the copy; the external clone was never written (no `__pycache__` found).\n")
w("## Result\n")
w(f"**Final {score}/100 — {sym} {grade} — deployable: false — veto: none — executed 5/5 inputs.** Static {static_sub}/100 (x0.4 = {sw}); execution average {avg}/100 (x0.6 = {dw}). Layer 1 avg {l1}/40, Layer 2 avg {l2}/60, assertions {passed}/{totala}. No open P0 (score 60-74 gives P1 items only). Floors for Limited Release (static >= 70, execution >= 75, L1 >= 28, L2 >= 42, assertions >= 80%) are not met: static {static_sub}, execution {avg}, assertions {round(100*passed/totala)}%.\n")
w("**Skill Veto:** T1 stability PASS, T2 contract PASS (frontmatter name/description/license present), T3 determinism PASS, T4 security PASS (no eval/exec, no credentials).\n")
w("**Classification:** Data Analysis (category 3), execution mode D (CLI + Python helper + shipped example). Complexity Moderate (2-3 task types: text pileup, bcftools calling, pysam counting; no references/ folder) -> N = 5 inputs.\n")
w("## Static scores (25 criteria)\n")
w("| Category | Score | Note |\n|---|---|---|")
for k, v in static.items():
    w(f"| {k} | {v[0]}/{v[1]} | {v[2]} |")
w(f"\n**Static subtotal: {static_sub}/100**\n")
w("## Summary table\n")
w("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |\n|---|---|---|---|---|---|---|---|")
for i in inputs:
    w(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | yes | {i['status_flag']} |")
w(f"\n**Execution Average: {avg} / 100**  |  **Assertion Pass Rate: {passed}/{totala}**\n")
w("## Detailed inputs\n")
logs = {1: ["log_in01.txt"], 2: ["log_in02.txt"], 3: ["log_in03.txt", "log_in03b.txt"], 4: ["log_in04.txt"], 5: ["log_in05.txt", "log_in05b.txt"]}
scripts = {1: "run/in01_real_mpileup.py", 2: "run/in02_pysam.py + run/snippets.py", 3: "run/in03_edge_symbols_defaults.py, run/in03b_example_script_edges.py", 4: "run/in04_bcftools_pipeline.py", 5: "run/in05_library_flags_real.py, run/in05b_misc_claims.py"}
for i in inputs:
    w(f"### Input {i['index']} — {i['type']}: {i['label']}\n")
    w(f"**Prompt:** {i['prompt']}\n")
    w(f"**Executed:** true. {i['execution_note']}\n")
    w(f"**Code that ran:** `{scripts[i['index']]}` (all under `run/`; SKILL.md / usage-guide.md functions loaded verbatim, only file names and coordinates substituted).\n")
    w("**Output (trimmed, PASS/FAIL lines are the assertions the scores depend on):**\n")
    w("```text")
    for lg in logs[i["index"]]:
        txt = rd(lg, 45, 330)
        w(f"--- {lg} ---")
        w(txt)
    w("```\n")
    w(f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100 — {i['note']}\n")
    w("**Assertions:**")
    for a in i["assertions"]:
        w(f"- [{a['result']}] {a['text']} — {a['note']}")
    w("")
w("## Shipped-means-present (gate 8)\n")
w("SKILL.md and usage-guide.md point at `examples/allele_counts.py` (present, ran from the copy) and Related Skills `alignment-filtering`, `reference-operations`, `bam-statistics`, `variant-calling/variant-calling`, `variant-calling/vcf-basics`, `variant-calling/joint-calling` — all exist in the staging clone. No missing primary file.\n")
w("## Research veto\n")
for k, v in veto_gates["research_veto"].items():
    if isinstance(v, dict):
        w(f"- **{k}:** {v['result']} — {v['detail']}")
w("\n## Recommendations\n")
for r in recs:
    w(f"**[{r['priority']}] {r['title']}** (observed in {r['observed_in']})  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
w("## Key strengths\n")
for s in key_strengths:
    w(f"- {s}")
w("\n## Notes for the orchestrator\n")
w("- Method traps honoured: outputs judged by asserted content, pysam vs samtools equivalence checked parameter by parameter (pysam `n`, overlap removal, BAQ via fastafile+stepper='samtools', min_base_quality default 13, max_depth 8000), every flag and default checked against the installed `--help`/behaviour.")
w("- Two of my own first-draft checks were wrong and were corrected before scoring (deletion marker under default BAQ; BED region beyond the covered gap; `-Q` also thins the '*' deletion slots): the logs kept are the final runs.")
open(os.path.join(OUT, f"eval_viewer_{SKILL}.md"), "w", encoding="utf-8").write("\n".join(V))
print("viewer written", os.path.getsize(os.path.join(OUT, f"eval_viewer_{SKILL}.md")))
