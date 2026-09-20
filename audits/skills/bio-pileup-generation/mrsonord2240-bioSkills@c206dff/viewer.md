> **Audit record for `bio-pileup-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/pileup-generation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pileup-generation

Generated: 2026-09-20  |  Auditor: fresh Sonnet (audit stage, first audit)  |  Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/pileup-generation`

Env: WSL `science`, env `alignment-files` (samtools 1.24, bcftools 1.24, pysam 0.24.1). Skill folder copied to `run/skill/` and run from the copy; the external clone was never written (no `__pycache__` found).

## Result

**Final 71/100 — ⚠️ Beta Only — deployable: false — veto: none — executed 5/5 inputs.** Static 69/100 (x0.4 = 27.6); execution average 72.6/100 (x0.6 = 43.6). Layer 1 avg 29.4/40, Layer 2 avg 43.2/60, assertions 12/25. No open P0 (score 60-74 gives P1 items only). Floors for Limited Release (static >= 70, execution >= 75, L1 >= 28, L2 >= 42, assertions >= 80%) are not met: static 69, execution 72.6, assertions 48%.

**Skill Veto:** T1 stability PASS, T2 contract PASS (frontmatter name/description/license present), T3 determinism PASS, T4 security PASS (no eval/exec, no credentials).

**Classification:** Data Analysis (category 3), execution mode D (CLI + Python helper + shipped example). Complexity Moderate (2-3 task types: text pileup, bcftools calling, pysam counting; no references/ folder) -> N = 5 inputs.

## Static scores (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Completeness 3 (text pileup, region/BED, multi-BAM, filters, -d/BAQ/overlap traps, bcftools calling, pysam counting all present; default -Q 13, default excluded flags, indel counting and --output-QNAME/-s are absent), correctness 2 (CLI facts verified: -d 8000/250, -g removal, --max-BQ ont preset, -x aliases, cheat-sheet flags; but pysam n-as-depth, is_del before is_refskip, wrong 'WRONG'-pipe rationale, 'No sequences in common' text, exome -d 250 contradiction), appropriateness 3 |
| reliability | 7/12 | Fault tolerance 2 (3-row Common Errors table; example script has only an argc check), error reporting 2 (example dies with raw ValueError tracebacks on ':' contigs, ranges, no index, unknown contig; mismatched reference makes samtools exit 0 and the Skill quotes a different message), recoverability 3 (read-only tools, safe to re-run) |
| performance_context | 5/8 | SKILL.md 375 lines plus usage-guide.md 258 lines; allele counting, bcftools pipelines and pysam blocks are repeated in both (token cost 2); workflows themselves are linear (efficiency 3) |
| agent_usability | 10/16 | Learnability 3, consistency 2 (0-based function arguments vs 1-based 'chr1:1000000' prompts, n vs pileups for 'depth', format examples with depth 15 and 11 quality chars), feedback design 2 (no expected outputs or self-checks for pipelines), error prevention 3 (good traps: -d cap, BAQ, -A, -aa, overlap, removed -g/-u; but not default -Q, excluded flags, pysam defaults) |
| human_usability | 5/8 | Description matches how users ask (pileup for variant calling, allele frequency); forgiveness 2: strict region strings, no clarification of coordinate base |
| security | 11/12 | No credentials, no eval/exec, no shell built from user strings; example script does not validate its region argument (3) |
| maintainability | 8/12 | Modularity 3 (SKILL.md + usage-guide + one example), modifiability 3, testability 2 (one example, no expected outputs or tests; it is the only shipped code and it is fragile) |
| agent_specific | 15/20 | Trigger precision 3, progressive disclosure 2 (no references/ dir; usage-guide duplicates SKILL.md), composability 3 (Related Skills all exist), idempotency 4 (read-only), escape hatches 3 (points to Mutect2/DeepVariant/HaplotypeCaller/Sniffles for out-of-scope work) |

**Static subtotal: 69/100**

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 31 | 46 | 77 | 3/5 PASS | yes | ✅ |
| 2 | Variant A | 27 | 38 | 65 | 2/5 PASS | yes | ⚠️ |
| 3 | Edge | 30 | 45 | 75 | 2/5 PASS | yes | ✅ |
| 4 | Variant B | 30 | 44 | 74 | 3/5 PASS | yes | ⚠️ |
| 5 | Stress | 29 | 43 | 72 | 2/5 PASS | yes | ⚠️ |

**Execution Average: 72.6 / 100**  |  **Assertion Pass Rate: 12/25**

## Detailed inputs

### Input 1 — Canonical: Text pileup of real human BAM (region, -q/-Q, BED) cross-checked against samtools depth, pysam and bcftools

**Prompt:** Generate a text pileup for chr22:1952-4617 of my BAM (nf-core human test slice) with MAPQ>=20 and baseQ>=20, tell me what each column and symbol means, and check the depth against another tool.

**Executed:** true. run/in01_real_mpileup.py (WSL): SKILL commands `samtools mpileup -f ref -r/-l/-q/-Q`, 2 BAMs; 22/24 checks passed. The 2 failed checks are the pysam n-vs-depth claim and a bcftools-vs-samtools depth nuance.

**Code that ran:** `run/in01_real_mpileup.py` (all under `run/`; SKILL.md / usage-guide.md functions loaded verbatim, only file names and coordinates substituted).

**Output (trimmed, PASS/FAIL lines are the assertions the scores depend on):**

```text
--- log_in01.txt ---
[PASS] in1 basic mpileup with -r runs and prints rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files'
[PASS] in1 every row has exactly 6 columns (SKILL 'Output Format')  -- Counter({6: 1157})
[PASS] in1 col3 = reference base from FASTA, col2 is 1-based
[PASS] in1 col4 depth == number of read-slot symbols in col5 == number of quality chars in col6
[PASS] in1 default output contains depth-0 rows (reads present but all bases filtered by default -Q 13)  -- 3 zero-depth rows, e.g. ['chr22', '1952']; SKILL never mentions default -Q=13 nor these rows
MAPQ decoded from ^ chars: {60: 3182, 54: 1, 42: 1}
[PASS] in1 MAPQ values seen after '^' are a subset of MAPQs present in the BAM  -- bam={60: 5635, 58: 1, 44: 1, 54: 1, 40: 1, 42: 1} pileup={60: 3182, 54: 1, 42: 1}
[PASS] in1 mpileup -B -Q0 -q0 -x -A -a depth == samtools depth -a -J -Q0 at every position  -- positions=2666 diffs=[] maxdepth=2532
[PASS] in1 pysam pileup(min_base_quality=0, ignore_overlaps=False, ignore_orphans=False, max_depth=1e6) depth == mpileup all-off depth  -- diffs=[] n=0
mpileup default: rows=1157 sumdepth=353910; pysam default col.n sum=670718; len(col.pileups) sum=353982
[FAIL] in1 SKILL pysam `pileup_column.n` (default args) == samtools mpileup default depth column  -- 1087/1157 positions differ; sum mpileup=353910 vs col.n=670718 (n ignores overlap removal + min_base_quality)
[PASS] in1 len(col.pileups) with pysam defaults == samtools mpileup -B (no BAQ, -Q13, overlap removal) depth  -- 0 positions differ; sum mpileup -B=353982
[PASS] in1 len(col.pileups) with stepper='samtools', fastafile=ref (BAQ on) == samtools mpileup default depth  -- 0 positions differ; sum pysam=353910
MAPQ distribution in BAM: {60: 5637, 58: 1, 44: 1, 54: 1, 40: 1, 42: 1}
[PASS] in1 -q 20: mpileup depth == independent count of reads with MAPQ>=20  -- sum=670999 vs sum_all=670999 diffs=[]
[PASS] in1 -q 60: mpileup depth == independent count of reads with MAPQ>=60  -- sum=670681 vs sum_all=670999 diffs=[]
[PASS] in1 -Q 20: mpileup depth == independent count of bases with baseQ>=20  -- sum=661117 diffs=[]
[PASS] in1 -Q 30: mpileup depth == independent count of bases with baseQ>=30  -- sum=654118 diffs=[]
[PASS] in1 --ff 0 (no excluded flags) raises total depth vs default flags (duplicates/secondary are in this BAM)  -- sum ff0=671070 default-excl=670999; SKILL never lists the default excluded flags UNMAP,SECONDARY,QCFAIL,DUP
flag distribution: {99: 1402, 163: 1417, 147: 1402, 83: 1417, 387: 1, 371: 1, 97: 1, 145: 1}
[PASS] in1 -r chr22:3000-3000 gives exactly one row at 3000  -- [['chr22', '3000', 'A', '781']]
[PASS] in1 -r with thousands separators (chr22:3,000-3,005) accepted -> 6 rows  -- 6
[PASS] in1 SKILL-style far region on the renumbered slice returns 0 rows without error (trap)  -- rows=0 stderr='[mpileup] 1 samples in 1 input files'
[PASS] in1 wrong contig name '22' vs 'chr22' => error message (troubleshooting 'chromosome name match')  -- [E::mpileup] fail to parse region '22:3000-3005' with /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam
[PASS] in1 -l BED (0-based half-open) yields 1-based positions 3000-3003 and 3100-3101  -- [3000, 3001, 3002, 3003, 3100, 3101]
[PASS] in1 two BAMs => 9 columns (3 + 3*N), i.e. SKILL 'Text pileup format (6 columns per sample)' is imprecise  -- Counter({9: 3})
bcftools DP vs samtools depth: positions 1181 differ 5 [(2063, 795, 797, 2), (2943, 447, 449, 2), (3009, 1624, 1626, 2), (3252, 24, 26, 2), (3536, 2342, 2344, 2)]
[FAIL] in1 bcftools mpileup FORMAT/DP == samtools mpileup depth (filters off)  -- 5 of 1181 positions differ (bcftools excludes deleted-base reads)
[PASS] in1 bcftools mpileup FORMAT/DP == samtools mpileup depth minus '*' deletion slots  -- 0 differ
SUMMARY in1: 22/24 assertions passed
```

**Scores:** Basic 31/40 | Specialized 46/60 | Total 77/100 — CLI half verified exactly; pysam `pileup_column.n` (used as depth in every pysam example) differs from mpileup depth at 1087/1157 positions (sum 670718 vs 353910); default -Q 13, default excluded flags and depth-0 rows are not documented

**Assertions:**
- [PASS] mpileup -r output has 6 columns, col3 equals the FASTA base, and depth == read symbols == quality characters at every non-zero row — 1157 rows; base-column parsed by an independent decoder
- [PASS] -q / -Q behave as documented: mpileup depth equals an independent pysam count for -q 20/60 and -Q 20/30, and all-filters-off depth equals samtools depth -a -J and pysam at 2666 positions — 0 differing positions in every comparison; max depth 2532
- [FAIL] Skill states the defaults that change what the pileup shows (-Q 13, excluded flags UNMAP,SECONDARY,QCFAIL,DUP, zero-depth rows with '*') — None of the three is mentioned; 3 depth-0 rows appear at chr22:1952-1954 in the default output
- [FAIL] pysam `pileup_column.n` printed as depth equals the samtools mpileup depth column under default arguments — n ignores overlap removal and min_base_quality; len(column.pileups) matches mpileup -B exactly, n does not (1087/1157 positions differ)
- [PASS] Region, BED and multi-BAM syntax works as the Skill shows (0-based half-open BED -> 1-based rows; 9 columns for 2 BAMs) — BED 2999-3003 gave rows 3000-3003; the Skill's '6 columns per sample' is imprecise (3 + 3N)

### Input 2 — Variant A: pysam allele counts / frequency / find_variants / pileup_text on planted-truth synthetic BAM and real BAM

**Prompt:** Count the alleles and alt fraction at synA:100 (planted SNP) and at real chr22 positions with pysam, make a per-position pileup text, and list positions with >10% alternative alleles.

**Executed:** true. run/in02_pysam.py (WSL, pysam 0.24.1): SKILL.md and usage-guide.md functions loaded verbatim via ast; 16/29 checks passed. examples/allele_counts.py run from the copy.

**Code that ran:** `run/in02_pysam.py + run/snippets.py` (all under `run/`; SKILL.md / usage-guide.md functions loaded verbatim, only file names and coordinates substituted).

**Output (trimmed, PASS/FAIL lines are the assertions the scores depend on):**

```text
--- log_in02.txt ---
SKILL.md functions: ['allele_counts', 'allele_frequency', 'pileup_text'] | usage-guide functions: ['count_alleles', 'find_variants']
SKILL 'Basic Pileup' (no truncate) printed 50 columns, pos range 80 - 129
[FAIL] in2 SKILL 'Basic Pileup' snippet prints only columns inside the requested region 100-110  -- requested 10 columns, got 50 covering 80-129 (no truncate=True; reads overhang)
{('C', '40'): 10, ('T', '40'): 30} ['Position: 99', 'Depth: 40']
[PASS] in2 SKILL 'Access Reads at Position' at synA:100 lists 30 ref (T) and 10 alt (C) reads, all Q40  -- {('C', '40'): 10, ('T', '40'): 30}
[PASS] in2 'Access Reads' snippet's printed `Depth:` line equals reads listed  -- ['Depth: 40']
[FAIL] in2 SKILL 'Pileup with Quality Filtering' (min_base_quality=20): printed depth at synA:725 == bases that pass Q20 (4)  -- printed pos 724 -> n=10 (6 of 10 bases at this column are Q5 and are filtered; n ignores base-quality filter)
[PASS] in2 SKILL allele_counts(synA, 0-based 99) == planted {T:30, C:10}  -- {'C': 10, 'T': 30}
[FAIL] in2 SKILL allele_counts called with the 1-based coordinate the user gave (100) reports the SNP  -- returned {'T': 40} = base at 1-based 101 (function/docstring never states 0-based; usage-guide Tips does)
[PASS] in2 SKILL allele_frequency(synA, 99) == {T:0.75, C:0.25}  -- {'C': 0.25, 'T': 0.75}
[PASS] in2 SKILL allele_counts default (pysam min_base_quality=13) drops the six Q5 alt bases at synA:725 -> only 4 ref  -- {'C': 4}
[PASS] in2 allele_frequency(min_qual=0) at synA:725 includes the six Q5 alt bases (alt frac 0.6)  -- {'T': 0.6, 'C': 0.4}
[FAIL] in2 allele_counts at synA:200 (5 of 10 reads carry a +2 insertion) reports the insertion  -- {'A': 10} -> insertion invisible (`indel` attribute never read)
[PASS] in2 allele_counts at synA:251 == {DEL:4, ref:4}  -- {'DEL': 4, 'C': 4}
[FAIL] in2 allele_counts inside a spliced (N) region returns empty dict and does not crash  -- {'DEL': 3}
[PASS] in2 allele_counts at overlap site 930 (5 pairs, R1 ref / R2 alt): total = 5 (overlap removal on by default)  -- {'C': 2, 'T': 3} (mpileup default: '..ttt' -> 2 ref + 3 alt)
[PASS] in2 SKILL allele_counts at 930 == samtools mpileup -B parse (same overlap arbitration)  -- pysam {'C': 2, 'T': 3} mpileup {'C': 2, 'T': 3}
[PASS] in2 SKILL allele_counts == samtools mpileup -B parse at 106 real positions (incl. 11 indel sites)
pileup_text sample: ['synA', '220', 'T', '5', '.....'] | mpileup: ['synA', '100', 'T', '40', 'CCCCCC..............cccc,,,,,,,,,,,,,,,,']
[FAIL] in2 pileup_text emits the 6-column pileup format (chrom,pos,ref,depth,bases,quals)  -- Counter({5: 623})
[FAIL] in2 pileup_text depth column == number of symbols in its own bases column  -- 31 rows inconsistent, e.g. [(725, 10, 4), (921, 10, 5), (922, 10, 5)] (depth uses pileup_column.n)
[FAIL] in2 pileup_text depth == samtools mpileup depth at every position  -- 31 positions differ e.g. [(725, 10, 4), (921, 10, 5), (922, 10, 5)]
[FAIL] in2 pileup_text base column has the same symbol multiset as samtools mpileup at every covered position  -- 200 positions differ; first: [(326, {'*': 3}, {'>': 2, '<': 1}), (327, {'*': 3}, {'>': 2, '<': 1}), (328, {'*': 3}, {'>': 2, '<': 1})]
[FAIL] in2 pileup_text reports spliced (N) reads as '>'/'<' (SKILL: is_refskip branch) at synA:400  -- emitted '***'; mpileup '>><' (pysam sets is_del=True for ref-skips, so the is_del branch fires first and writes '*')
[FAIL] in2 pileup_text reproduces read-start/end markers (^,$) and indel text (+N/-N) that the Skill's own encoding table lists  -- 24 mpileup rows carry ^ $ + or -; pileup_text emits none, and no quality column
[FAIL] in2 pileup_text emits the base-quality column (column 6 in the Skill's format table)  -- columns=5
[PASS] in2 usage-guide count_alleles(min_qual=20) at synA:100 == {T:30,C:10}  -- {'C': 10, 'T': 30}
find_variants on syn: [{'chrom': 'synA', 'pos': 100, 'ref': 'T', 'alt': 'C', 'depth': 40, 'alt_count': 10, 'freq': 0.25}]
[PASS] in2 usage-guide find_variants recovers the planted SNP synA:100 T>C (depth 40, alt 10, freq 0.25)  -- {(100, 'T', 'C', 10)}
[PASS] in2 find_variants reports no false variants (only the planted SNP passes depth>=10, alt>=0.1, Q>=20)  -- {(100, 'T', 'C', 10)}
[FAIL] in2 find_variants can see the planted 2 bp insertion and 3 bp deletion (Skill claims 'SNP/indel detection')  -- min_depth=3 output positions [100, 930]: indels are never reported (only `alignment.query_sequence[qpos]`; `indel` field unused)
find_variants real chr22: 4 sites; mpileup-derived 4; only-in-skill []; only-in-mpileup []
[PASS] in2 find_variants on real human BAM == independent mpileup -B -Q20 parse (same alt sites and counts)  -- skill 4 vs mpileup 4
Position: synA:100
Total depth: 40
Allele counts:
  T: 30 (75.0%)
  C: 10 (25.0%)
 
[PASS] in2 examples/allele_counts.py synA:100 (from copy) prints T:30 (75.0%) and C:10 (25.0%)  -- Position: synA:100 | Total depth: 40 | Allele counts: |   T: 30 (75.0%) |   C: 10 (25.0%) | 
example on real chr22:3000: Position: chr22:3000 | Total depth: 781 | Allele counts: |   A: 781 (100.0%) |  | mpileup -B -q20 -Q20 col4: 781
[PASS] in2 examples/allele_counts.py total depth at real chr22:3000 == samtools mpileup -B -q20 -Q20 depth  -- example 781 vs mpileup 781
SUMMARY in2: 16/29 assertions passed
```

**Scores:** Basic 27/40 | Specialized 38/60 | Total 65/100 — allele_counts/allele_frequency/find_variants/example are right for SNPs (equal to mpileup at 106 real positions); pileup_text disagrees with its own depth in 31 rows, omits ^ $ indels and qualities; ref-skips are counted as DEL; indels invisible

**Assertions:**
- [PASS] allele_counts, allele_frequency, count_alleles and find_variants recover the planted SNP (T 30 / C 10, 25%) with no false variants, and allele_counts equals samtools mpileup -B at 106 real positions — find_variants on the real chr22 BAM equals an independent mpileup -B -Q20 parse (4 sites, same counts)
- [PASS] Shipped examples/allele_counts.py (run from a copy) prints T: 30 (75.0%), C: 10 (25.0%) and total depth 40; on real chr22:3000 total depth 781 equals mpileup -B -q20 -Q20 — runs from a clean copy; the 1-based -> 0-based conversion is correct
- [FAIL] pileup_text output is consistent with samtools mpileup (depth column == bases column, same symbols, ^/$/indel text, 6-column format) — 5 columns (no qualities); depth != symbol count in 31 rows (uses pileup_column.n); no ^ $ or +/-; 200 spliced positions differ
- [FAIL] Ref-skips (spliced reads) are treated as skips, not deletions — pysam sets is_del=True for N-skips, the Skill tests is_del first: allele_counts reports {'DEL': 3} at synA:400 and pileup_text writes '***' where mpileup shows '>><'; the is_refskip branch is dead code
- [FAIL] Module-level snippets print what they claim ('Basic Pileup' region columns; 'Pileup with Quality Filtering' depth) — 'Basic Pileup' (no truncate=True) prints 50 columns 80-129 for a 10-column request; with min_base_quality=20 the printed n=10 at synA:725 although only 4 bases pass

### Input 3 — Edge: Exact symbol decoding and silent defaults on planted synthetic BAM; shipped example on edge inputs

**Prompt:** Explain exactly how insertions, deletions, spliced reads, read starts/ends and soft clips appear in the pileup base column and which reads mpileup drops by default (flags, MAPQ, baseQ, overlaps, orphans, max depth); my amplicon library is 9000x deep. Then run the example script on unusual region strings.

**Executed:** true. run/in03_edge_symbols_defaults.py (35/35 checks passed) and run/in03b_example_script_edges.py (4/9 passed, raw ValueError tracebacks) on run/data (synthetic, truth in truth.json).

**Code that ran:** `run/in03_edge_symbols_defaults.py, run/in03b_example_script_edges.py` (all under `run/`; SKILL.md / usage-guide.md functions loaded verbatim, only file names and coordinates substituted).

**Output (trimmed, PASS/FAIL lines are the assertions the scores depend on):**

```text
--- log_in03.txt ---
[PASS] in3 SNP synA:100: '.' x14, ',' x16, alt forward 'C' x6, alt reverse 'c' x4, depth 40  -- {'C': 6, 'ref_fwd': 14, 'c': 4, 'ref_rev': 16}
[PASS] in3 '^Q' at read start: 40 read starts at synA:81, each '^]' (MAPQ 60 + 33 = ']')  -- ^ count 40, '^]' count 40
[PASS] in3 '$' at read end: 40 read ends at synA:130 (the '$' precedes the end position's next row, i.e. belongs to the last base)  -- .$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$.$,$,$,$,$,$,$,$,$,$,$
[PASS] in3 insertion after synA:200 appears on row 200 as '+2AC' x3 (fwd) and '+2ac' x2 (rev); depth 10 (insertion adds no depth)  -- {'ref_fwd': 8, '+AC': 3, 'ins': 5, 'ref_rev': 2, '+ac': 2} depth=10
[PASS] in3 with -B: deletion of synA:251-253 appears on row 250 as '-3CGT' x2 (fwd) and '-3cgt' x2 (rev), depth 8  -- {'ref_fwd': 6, '-CGT': 2, 'delmark': 4, 'ref_rev': 2, '-cgt': 2} depth=8
[PASS] in3 DEFAULT (BAQ on): the same deletion reads are dropped at 248-250 (baseQ after BAQ < 13): depth 4, no '-3CGT' marker -- the deletion is invisible in default text pileup  -- depth=4 marks=0 (SKILL says BAQ 'hurts indel detection sensitivity' but not that default mpileup text loses the indel)
[PASS] in3 deleted bases at synA:251-253 shown as '*' x4 with depth 8 (deleted reads stay in depth)  -- [('8', '**....**'), ('8', '**....**'), ('8', '**....**')]
[PASS] in3 --reverse-del marks reverse-strand deletions '#' (option not in the Skill)  -- **....##
[PASS] in3 splice N-gap: at synA:400 '>' x2 (fwd) and '<' x1 (rev), depth 3  -- {'>': 2, '<': 1} depth=3
[PASS] in3 soft-clip: the clipped 'TTTTT' never appear in rows 396-405 (no T/t/A/C/G letters; only '.' ',' '^]' and ref-skips)  -- {399: '>><', 401: '>><^].^].^].', 402: '>><...'}
[PASS] in3 default excluded flags: depth 10 at synA:825 (3 DUP, 2 SECONDARY, 1 QCFAIL, 2 UNMAP silently excluded)  -- 10
[PASS] in3 --ff 0 makes them visible: depth 16 (unmapped stay excluded)  -- 16
[PASS] in3 --ff DUP alone (named flag) -> depth 13 (10 + 2 secondary + 1 qcfail)  -- 13
[PASS] in3 -q 10 drops the 5 MAPQ-5 reads at synA:625 (depth 10 -> 5); '^&' shows MAPQ 5  -- 10->5
[PASS] in3 baseQ: default -Q 13 drops the six Q5 bases at synA:725 (depth 4); -Q 0 restores 10 (6 alt)  -- default=4 -Q0=10 -B=4 -B -Q0=10
[PASS] in3 overlap removal: depth 5 by default vs 10 with -x at synA:930  -- 5 vs 10
[PASS] in3 long option --disable-overlap-removal (samtools) accepted  -- 10
[PASS] in3 long option --ignore-overlaps-removal (samtools) accepted  -- 10
bcftools DP overlaps default / --ignore-overlaps: 67,0,44,73,53,116:5:2,3,0 118,0,118,133,133,242:10:5,5,0
[PASS] in3 bcftools mpileup --ignore-overlaps is the bcftools spelling (accepted) and changes DP 5 -> 10  -- 67,0,44,73,53,116:5:2,3,0 / 118,0,118,133,133,242:10:5,5,0
[PASS] in3 orphans (flag 65, paired not proper): depth 0 rows / no data by default, 4 with -A  -- default=None -A=4
rows per contig default / -a / -aa: {'synA': 623, 'synC': 50} {'synA': 1000, 'synC': 300} {'synA': 1000, 'synB': 500, 'synC': 300}
[PASS] in3 default mpileup omits uncovered positions (synA rows < 1000) and empty contigs  -- {'synA': 623, 'synC': 50}
[PASS] in3 -a: every position of contigs that have reads (synA 1000, synC 300), no rows for read-less synB  -- {'synA': 1000, 'synC': 300}
[PASS] in3 -aa additionally emits the read-less contig synB (500 rows, depth 0)  -- {'synA': 1000, 'synB': 500, 'synC': 300}
[PASS] in3 zero-depth row format: 'synB 1 <ref> 0 * *'  -- ['synB', '1', 'A', '0', '*', '*']
[PASS] in3 samtools mpileup default caps 9000 reads at 8000 (Skill: 'default -d 8000 silently truncates')  -- 8000
[PASS] in3 samtools mpileup -d 0 = no cap (Skill cheat-sheet uses -d 0): depth 9000  -- 9000
[PASS] in3 samtools mpileup -d 1000000 -> 9000  -- 9000
[PASS] in3 Skill cheat-sheet 'Capture / exome: -d 250' truncates 9000-deep amplicon-like data to 250 (contradicts its own 'Critical Trap')  -- depth 250
[PASS] in3 bcftools mpileup default -d 250 caps DP at 250 (Skill claim)  -- 250
[PASS] in3 bcftools mpileup -d 1000000 -> DP 9000 (Skill recommendation)  -- 9000
bcftools -d 0 gives DP = 9000 1 samples in 1 input files
[mpileup] Max depth set to maximum value (2147483647)
[PASS] in3 bcftools mpileup -d 0 (Skill uses `-d 0` only for samtools; check if it is 'no cap' here too)  -- DP=9000
[PASS] in3 SKILL pysam snippets (no max_depth) also truncate at 8000 silently: n=8000 with defaults, 9000 with max_depth=1e6  -- defaults n=8000, max_depth=1e6 n=9000
positions with different base-quality strings default vs -B (150-300): 22 [(171, ('DDDDDD', 'IIIIII')), (200, ('888III', 'IIIIII')), (201, ('IIIII', 'IIIIII')), (202, ('555III', 'IIIIII')), (203, ('888III', 'IIIIII')), (218, ('EEEIII', 'IIIIII'))]
[PASS] in3 BAQ (default with -f) alters base qualities near the planted indels at synA:200/250 versus -B  -- 22 positions differ, e.g. [(171, ('DDDDDD', 'IIIIII')), (200, ('888III', 'IIIIII')), (201, ('IIIII', 'IIIIII'))]
mpileup without -f rc, out, err: 0 synA	100	N	40	CCCCCCTTTTTTTTTTTTTTcccctttttttttttttttt	IIIIIIIIIIIIIIIIIIIIIIIII [mpileup] 1 samples in 1 input files
[PASS] in3 Common Errors row 'No FASTA reference | Missing -f' : samtools mpileup without -f actually succeeds (reference column N)  -- rc=0 out='synA\t100\tN\t40\tCCCCCCTTTTTTTTTTTTTTcccctttttttttttttttt\tIIIII'
bcftools mpileup without -f:  Error: mpileup requires the --fasta-ref option by default; use --no-reference to run without a fasta reference
[PASS] in3 bcftools mpileup without -f emits a specific error  -- Error: mpileup requires the --fasta-ref option by default; use --no-reference to run without a fasta reference
SUMMARY in3: 35/35 assertions passed
--- log_in03b.txt ---
colon contig -> 1  | ValueError: too many values to unpack (expected 2)
[FAIL] in3 example handles a contig name containing ':' (HLA-A*01:01:01:01:50)  -- rc=1 err=ValueError: too many values to unpack (expected 2)
[PASS] in3 example on contig 'plain' with no reads at :50 prints depth 0 without crashing  -- Position: plain:50 | Total depth: 0 | Allele counts:
no index -> 1 ValueError: no index available for pileup
[FAIL] in3 unindexed BAM gives a friendly message (not a raw traceback)  -- rc=1 last line: ValueError: no index available for pileup
range region -> 1 ValueError: invalid literal for int() with base 10: '100-110'
[FAIL] in3 region 'synA:100-110' (range, as in mpileup -r) is accepted or explained  -- rc=1 last line: ValueError: invalid literal for int() with base 10: '100-110'
[FAIL] in3 region with thousands separator 'synA:1,000' is accepted or explained  -- rc=1 last line: ValueError: invalid literal for int() with base 10: '1,000'
[FAIL] in3 unknown contig gives a friendly message  -- rc=1 last line: ValueError: invalid contig `nosuch`
pos 0 -> 1  ValueError: start out of range (-1)
[PASS] in3 position 0 (invalid 1-based) is rejected rather than silently reporting the wrong base  -- rc=1 out='' err=ValueError: start out of range (-1)
[PASS] in3 missing region argument prints the usage line and exits non-zero  -- Usage: allele_counts.py <input.bam> <region>
Example: allele_counts.py sample.ba
[PASS] in3 control: normal call from copy exits 0  -- Position: synA:100 | Total depth: 40 | Allele counts: |   T: 30 (75.0%) |   C: 10 (25.0%)
```

**Scores:** Basic 30/40 | Specialized 45/60 | Total 75/100 — Symbol table, -d 8000/250, -d 0, overlap, -A, -a/-aa all verified against planted truth; default BAQ drops the deletion evidence (depth 8 -> 4, no -3CGT marker) which the Skill only hints at; cheat-sheet -d 250 contradicts its own warning; example script fails with tracebacks on ':' contigs, ranges, commas, no index

**Assertions:**
- [PASS] Base-column symbol table matches planted truth: '.'/',' by strand, ACGT/acgt mismatches (6 C + 4 c), ^] at read start (MAPQ 60+33), $, +2AC/+2ac, -3CGT, '*', '>'/'<' for N-skips, soft clips absent — Decoded with an independent parser; notation '+NNN' in the Skill's table is loose (actual +2AC), '#' (--reverse-del) not mentioned
- [PASS] Depth-cap, overlap and orphan claims hold: samtools default 8000 (9000 reads -> 8000), -d 0 unlimited, bcftools default 250, -x/--disable-overlap-removal/--ignore-overlaps change depth 5 -> 10, -A restores orphans, -aa adds read-less contigs — all values reproduced exactly on deep.bam / syn.bam
- [FAIL] Cheat-sheet settings are consistent with the Skill's own 'Critical Trap' about silent depth truncation — 'Capture / exome: -q 20 -Q 20 -d 250' caps a 9000x amplicon-like column at 250; usage-guide 'Memory Issues' also suggests -d 500
- [FAIL] Skill documents the defaults that silently remove evidence (excluded flags DUP/SECONDARY/QCFAIL, -Q 13, BAQ hiding the planted deletion) — default text pileup shows depth 4 and no deletion marker at synA:250 versus 8 and '-3CGT' with -B; flags and -Q default not stated
- [FAIL] Shipped example handles realistic region strings without raw stack traces — 'HLA-A*01:01:01:01:50' -> ValueError too many values; 'synA:100-110', 'synA:1,000' -> int() ValueError; unindexed BAM and unknown contig -> raw ValueError

### Input 4 — Variant B: bcftools mpileup | call: single sample, BCF intermediate, two-sample joint, parallel by chromosome, and the 'WRONG' pipe

**Prompt:** Call variants from my BAM with the modern bcftools mpileup | bcftools call pipeline (single sample, BCF intermediate, joint calling of 2 samples, parallel per chromosome) and tell me if `samtools mpileup | bcftools call` is really wrong and why.

**Executed:** true. run/in04_bcftools_pipeline.py (WSL, bcftools 1.24): 17/19 checks passed on planted SNP/ins/del (syn.bam), 2-sample s1/s2, 11-contig multi.bam, real human chr22.

**Code that ran:** `run/in04_bcftools_pipeline.py` (all under `run/`; SKILL.md / usage-guide.md functions loaded verbatim, only file names and coordinates substituted).

**Output (trimmed, PASS/FAIL lines are the assertions the scores depend on):**

```text
--- log_in04.txt ---
stderr: Note: none of --samples-file, --ploidy or --ploidy-file given, assuming all sites are diploid
[mpileup] 1 samples in 1 input files
[mpileup] maximum number of reads per input file set to -d 1000000
[PASS] in4 SKILL 'Modern Germline Calling' pipeline runs and writes variants.vcf.gz + .tbi  -- rc=0
synA 100 T C 152.156 DP=40;AD=30,10;VDB=6.99472e-07;SGB=-0.670168;RPBZ=0;MQBZ=0;MQSBZ=0;BQBZ=0;SCBZ=0 GT:PL:DP:SP:AD ['0/1:186,0,255:40:1:30,10']
synA 200 AA AACA 201.37 INDEL;IDV=5;IMF=0.5;DP=10;AD=5,5;VDB=0.00187095;SGB=-0.590765;RPBZ=3;MQBZ=0;MQSB GT:PL:DP:SP:AD ['0/1:234,0,154:10:4:5,5']
synA 250 TCGT T 164.406 INDEL;IDV=4;IMF=0.5;DP=8;AD=4,4;VDB=0.0058656;SGB=-0.556411;RPBZ=0;MQBZ=0;MQSBZ= GT:PL:DP:SP:AD ['0/1:197,0,165:8:4:4,4']
synA 930 C T 34.2289 DP=10;AD=2,3;VDB=0.0221621;SGB=-0.511536;RPBZ=-2;MQBZ=0;MQSBZ=0;BQBZ=0;SCBZ=0;MQ GT:PL:DP:SP:AD ['0/1:67,0,44:5:10:2,3']
[PASS] in4 planted SNP synA:100 T>C is called with the Skill's flags  -- [{'chrom': 'synA', 'pos': 100, 'ref': 'T', 'alt': 'C', 'qual': 152.156, 'info': 'DP=40;AD=30,10;VDB=6.99472e-07;SGB=-0.670168;RPBZ=0;MQBZ=0;MQSBZ=0;BQBZ=0;SCBZ=0;MQ0F=0;AC=1;AN=2;DP4=14,16,6,4;MQ=60', 'fmt': 'GT:PL:DP:SP:AD', 'samples': ['0/1:186,0,255:40:1 ...
[PASS] in4 FORMAT/AD at the SNP == planted 30,10 and FORMAT/DP == 40  -- {'GT': '0/1', 'PL': '186,0,255', 'DP': '40', 'SP': '1', 'AD': '30,10'}
[PASS] in4 requested tags present: FORMAT/AD,DP,SP and INFO/AD  -- FORMAT=['GT', 'PL', 'DP', 'SP', 'AD'] INFO=DP=40;AD=30,10;VDB=6.99472e-07;SGB=-0.670168;RPBZ=0;MQBZ=0;M
[PASS] in4 planted 2 bp insertion after synA:200 is called  -- [(200, 'AA', 'AACA')]
[PASS] in4 planted 3 bp deletion synA:251-253 is called (default BAQ + -Q 20)  -- [(250, 'TCGT', 'T')]
[PASS] in4 no unexplained records beyond the planted SNP/ins/del (+ synA:930, the planted conflicting-overlap site, called 2 ref/3 alt)  -- extra []
[PASS] in4 usage-guide single-sample + `bcftools index` and BCF intermediate (`bcftools call -mv raw.bcf -o variants.vcf`) run  -- rc=0 maximum number of reads per input file set to -d 1000000
Note: none of --samples-file, --ploidy or --ploidy-file given, assuming all sites are diploid
BCF-intermediate records (no -q/-Q): [(100, 'T', 'C'), (200, 'AA', 'AACA'), (250, 'TCGT', 'T'), (930, 'C', 'T')]
[PASS] in4 BCF-intermediate route calls the planted SNP too  -- [100, 200, 250, 930]
[PASS] in4 multi-sample command (with --threads 4) runs  -- rc=0 -ploidy-file given, assuming all sites are diploid
[mpileup] 2 samples in 2 input files
[mpileup] maximum number of reads per input file set to -d 250
[PASS] in4 joint VCF sample names come from the @RG SM tags (s1, s2)  -- ['s1', 's2']
joint AD per sample: 100 17,3|8,12|
[PASS] in4 joint per-sample AD == planted (s1: 17,3  s2: 8,12)  -- 100 17,3|8,12|
WRONG pipe output: Note: none of --samples-file, --ploidy or --ploidy-file given, assuming all sites are diploid
Failed to read from standard input: unknown file type
pipestatus=0 255 0
[PASS] in4 the Skill's 'WRONG' pipe (samtools mpileup | bcftools call) fails  -- Note: none of --samples-file, --ploidy or --ploidy-file given, assuming all sites are diploid
Failed to read from standard input: unknown file type
pipestatus=0 255 0
[FAIL] in4 the failure is due to a double depth cap (the reason the Skill gives in its comment)  -- actual message: 'Failed to read from standard input: unknown file type' -> a text pileup is not VCF/BCF; bcftools call applies no depth cap, so the Skill's explanation is wrong
parallel loop stdout/err: concat_status=0 Concatenating chr3.vcf.gz	0.003165 seconds
Concatenating chr4.vcf.gz	0.003224 seconds
Concatenating chr5.vcf.gz	0.003116 seconds
Concatenating chr6.vcf.gz	0.003242 seconds
Concatenating chr7.vcf.gz	0.003302 seconds
Concatenating chr8.vcf.gz	0.003343 seconds
Concatenating chr9.vcf.gz	0.003139 seconds
all.vcf.gz contig order: ['chr1', 'chr10', 'chr11', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9']
[PASS] in4 each per-chromosome call has the planted SNP (11 records, pos 100)  -- ['chr1', 'chr10', 'chr11', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9']
[FAIL] in4 usage-guide `bcftools concat ... chr*.vcf.gz` (shell glob = lexicographic: chr1,chr10,chr11,chr2...) preserves header contig order  -- order ['chr1', 'chr10', 'chr11', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9']; ng chr6.vcf.gz	0.003242 seconds
Concatenating chr7.vcf.gz	0.003302 seconds
Concatenating chr8.vcf.gz	0.003343 seconds
Concatenating chr9.vcf.gz	0.003139 seconds
index of concat result: index_ok 
```

**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100 — Recommended pipelines reproduce truth exactly (AD 30,10; per-sample AD 17,3 / 8,12; ins and del called); the stated reason the samtools|bcftools pipe is 'WRONG' is false and the parallel-loop concat glob writes contigs out of header order with exit 0

**Assertions:**
- [PASS] 'Modern Germline Calling' pipeline (-d 1000000 -q 20 -Q 20 --annotate FORMAT/AD,DP,SP,INFO/AD | call -mv, index -t) calls the planted SNP with AD 30,10 / DP 40, the 2 bp insertion and the 3 bp deletion — synA:100 T>C AD=30,10 DP=40; synA:200 AA>AACA; synA:250 TCGT>T; plus synA:930 from the planted conflicting-overlap site
- [PASS] Multi-sample joint calling with --threads 4 gives per-sample AD matching planted truth and sample names from @RG SM — AD s1 17,3 and s2 8,12; usage-guide BCF-intermediate route and `bcftools index` also ran
- [FAIL] The reason given for the 'WRONG' pipe (samtools 8000 cap then bcftools 250 cap re-applied) is correct — bcftools call applies no depth cap; the pipe fails because a text pileup is not VCF/BCF: 'Failed to read from standard input: unknown file type'
- [FAIL] usage-guide parallel-by-chromosome loop (`bcftools concat ... chr*.vcf.gz`) yields a VCF in header contig order when extended past chr3 — 11 contigs: records chr1,chr10,chr11,chr2,...,chr9 while the header lists chr1..chr11; exit 0 and `bcftools index` still succeeds
- [PASS] Flags and tags named in the Skill exist in bcftools 1.24 (FORMAT/AD,DP,SP, INFO/AD, --max-BQ, ont preset value 30, --ignore-overlaps, --threads); samtools mpileup -g/-u are rejected — -X list shows `ont: -B -Q5 --max-BQ 30 -I`; samtools: 'invalid option -- g'

### Input 5 — Stress: Library-typed flag cheat-sheet on real ARTIC nanopore, spliced RNA-seq and 1000G germline BAMs; reference-mismatch handling

**Prompt:** Apply the library-typed flag cheat-sheet to my ARTIC SARS-CoV-2 nanopore amplicon BAM (consensus needs zero-coverage rows), an RNA-seq BAM and a 1000G germline BAM, and tell me what happens when the reference does not match the BAM.

**Executed:** true. run/in05_library_flags_real.py and in05b_misc_claims.py (WSL): 23/27 + 4/5 checks; real data only (ARTIC v5.3.2 BAM + MN908947.3, STAR RNA BAM, HG00349 chr20), BAM copies indexed in run/work and deleted afterwards.

**Code that ran:** `run/in05_library_flags_real.py, run/in05b_misc_claims.py` (all under `run/`; SKILL.md / usage-guide.md functions loaded verbatim, only file names and coordinates substituted).

**Output (trimmed, PASS/FAIL lines are the assertions the scores depend on):**

```text
--- log_in05.txt ---
[PASS] in5 cheat-sheet row 'Short-read germline WGS': `-q 20 -Q 20 -d 0` accepted, produces rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files\n[mpileup] Max depth set to maximum value (2'
[PASS] in5 cheat-sheet row 'Short-read tumor WGS': `-q 1 -Q 13 -d 0 -B` accepted, produces rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files\n[mpileup] Max depth set to maximum value (2'
[PASS] in5 cheat-sheet row 'Amplicon viral (ARTIC)': `-aa -A -d 600000 -B -Q 20` accepted, produces rows  -- rc=0 rows=2666 stderr='[mpileup] 1 samples in 1 input files'
[PASS] in5 cheat-sheet row 'Capture / exome': `-q 20 -Q 20 -d 250` accepted, produces rows  -- rc=0 rows=1145 stderr='[mpileup] 1 samples in 1 input files'
[PASS] in5 cheat-sheet row 'Long-read ONT R10.4+': `-q 30 -Q 0 -B -d 0` accepted, produces rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files\n[mpileup] Max depth set to maximum value (2'
[PASS] in5 cheat-sheet row 'PacBio HiFi': `-q 20 -Q 0 -B -d 0` accepted, produces rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files\n[mpileup] Max depth set to maximum value (2'
[PASS] in5 cheat-sheet row 'RNA-seq variants': `-q 20 -Q 20 -B -d 0` accepted, produces rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files\n[mpileup] Max depth set to maximum value (2'
[PASS] in5 cheat-sheet row 'Forensic / aDNA': `-q 0 -Q 0 -A -d 0 -B` accepted, produces rows  -- rc=0 rows=1181 stderr='[mpileup] 1 samples in 1 input files\n[mpileup] Max depth set to maximum value (2'
[PASS] in5 ONT row: `bcftools mpileup ... -q 30 -Q 0 -B -d 0 --max-BQ 30` accepted (bcftools has -d 0)  -- chr22	3000
[mpileup] 1 samples in 1 input files
[mpileup] Max depth set to maximum value (2147483647
ARTIC -aa rows=29903 in 0.1s
[PASS] in5 ARTIC row emits one line per genome position (29903 rows, MN908947.3)  -- 29903 rows
[PASS] in5 ARTIC depth column minus '*' slots == independent pysam count of aligned bases with baseQ>=20 at all 29903 positions (note: -Q also thins the '*' deletion slots)  -- 0 differ e.g. []
[PASS] in5 SKILL: '-aa is required for ARTIC' -- plain `-a` already emits the same 29903 rows for a single-contig BAM  -- -a rows=29903 vs -aa rows=29903 (77 zero-depth positions in both)
[PASS] in5 without -a/-aa the zero-depth positions are missing (consensus would skip them)  -- 29826 rows, expected 29826
MAPQ dist ARTIC: Counter({60: 4902, 37: 3, 20: 2, 33: 2, 26: 1, 34: 1, 40: 1, 56: 1, 53: 1, 38: 1, 39: 1})
[PASS] in5 ONT row `-q 30 -Q 0 -B -d 0` depth == independent count of MAPQ>=30 reads  -- 0 differ; positions with data=29826
RNA-seq mpileup: '>' slots=68805 '<' slots=369205 '*' slots=259 rows=36860
[PASS] in5 RNA-seq row: spliced reads appear as '>'/'<' in the base column (Skill table)  -- 68805 '>' and 369205 '<'
position with most ref-skips: 25548 mpileup '>'/'<'/'*': 3 45 0 | SKILL allele_counts: {'DEL': 54, 'G': 5}
[FAIL] in5 SKILL allele_counts at a real intron position does NOT report ref-skips as 'DEL' (mpileup: '*' = 0 real deletions here)  -- allele_counts DEL=54 vs mpileup real deletions '*'=0, '>'+'<'=48
1000G default germline row rows: 98421 [mpileup] 1 samples in 1 input files
[mpileup] Max depth set to maximum value (2
[PASS] in5 1000G germline row: rows produced and ref column == FASTA  -- 98421 rows
[PASS] in5 1000G: all-filters-off mpileup depth == independent pysam count at every position  -- 0 differ (windowed to reads overlapping region)
[PASS] in5 1000G: default flags silently drop the pre-flagged duplicates (Skill never says so): sum depth default-excl < --ff 0  -- sum depth 948889 vs 959299; 101 duplicate-flagged reads overlap the region
ARTIC BAM + MT192765.1 FASTA (contig missing from ref): 0 11 [mpileup] 1 samples in 1 input files
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_ad
[PASS] in5 wrong-reference case: message names the missing contig  -- rc=0 rows=11 err='[mpileup] 1 samples in 1 input files\n[E::faidx_adjust_position] The sequence "MN908947.3" was not found\n[E::faidx_adjust_position] The sequence "MN908'
[FAIL] in5 wrong-reference case: exits non-zero (an agent following the Skill's `> pileup.txt` would otherwise accept the output)  -- rc=0; still emitted 11 rows for the 10 bp region with reference base N: 'MN908947.3\t100\tN\t33\tCCCCCCCccccccccccc*c*cccccccCc*CC\t><<:;2=2/3262737'
[FAIL] in5 Skill troubleshooting text 'No sequences in common' is the message users will actually see  -- actual: '[E::faidx_adjust_position] The sequence "MN908947.3" was not found'
bcftools mpileup mismatched ref: 0 #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	/mnt/openscience/audits/bio-pileup-generation/run/work/in05/artic.bam
MN908947.3	100	.	N	C,<*>	0	.	DP=47;I16=0,0,14,33,0,0,763,14879,0,0,2820,169200,0,0,1 | [mpileup] 1 samples in 1 input files
[mpileup] maximum number of reads per input file set to -d 250
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_adjust
same without -r: 0 3 [mpileup] 1 samples in 1 input files
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
[E::faidx_adjust_position] The sequence "MN908947.3" was not found
--- log_in05b.txt ---
samtools mpileup default (BAQ) 0.23s vs -B 0.09s -> BAQ overhead 152%
[FAIL] in5 SKILL 'BAQ ... ~30% slower': measured overhead of default BAQ vs -B on 100 kb of 1000G is within 15-60%  -- 152% (0.23s vs 0.09s, best of 3)
[PASS] in5 -E / --redo-BAQ accepted  -- chr20	1400001	T	6	.,...,	><>>>>
chr20	1400002	C	6	.,...,	<B<<<0
[mpileup] 1 samp
[PASS] in5 --no-BAQ long form accepted  -- chr20	1400001	T	6	.,...,	B<BBBB
chr20	1400002	C	6	.,...,	<B<<<0
[mpileup] 1 samp
[PASS] in5 -B and -E together are rejected (Skill table lists both without saying they are exclusive)  -- Error: The -B option cannot be combined with -E
human deep slice: default 0.14s vs -B 0.05s -> 178% overhead
--output-QNAME -s columns: [8] ['chr20', '1400300', 'G', '6', ',,,.,,']
[PASS] in5 undocumented-in-Skill options work: `--output-QNAME` adds read-name column with one name per read, `-s` adds MAPQ column  -- cols=8
```

**Scores:** Basic 29/40 | Specialized 43/60 | Total 72/100 — All 8 cheat-sheet rows run and ARTIC/1000G outputs match independent counts; real RNA-seq reveals allele_counts reporting 54 'DEL' at an intron with zero deletions; reference mismatch exits 0 with 'N' bases; '-aa required' and '~30% slower' claims do not hold

**Assertions:**
- [PASS] Every cheat-sheet row (germline, tumor, ARTIC, exome, ONT, HiFi, RNA-seq, aDNA) and `bcftools mpileup ... --max-BQ 30` is accepted by samtools/bcftools 1.24 and produces rows — 8/8 samtools rows and the bcftools ONT variant ran
- [PASS] Real-data outputs match independent computations: ARTIC -aa gives 29903 rows with depth (minus '*') == pysam count at every position; 1000G all-filters-off depth == pysam count; RNA-seq shows '>'/'<' (68805/369205 slots) — 0 differing positions; 77 zero-depth ARTIC rows only with -a/-aa
- [FAIL] The Skill's pysam allele counter treats ref-skips in real spliced RNA-seq reads as skips — at chr22:25548 mpileup shows 3 '>' + 45 '<' and 0 '*', allele_counts returns {'DEL': 54, 'G': 5}
- [FAIL] Reference-mismatch guidance matches the tool: 'No sequences in common' / non-zero exit — actual: `[E::faidx_adjust_position] The sequence "MN908947.3" was not found`, exit status 0, 4.2 MB pileup of 'N' reference rows written by `> pileup.txt`
- [FAIL] Stated facts hold: '-aa is required for ARTIC' and 'BAQ ~30% slower' — -a already emits the same 29903 rows for a single-contig BAM (-aa only adds read-less contigs); BAQ default cost +152% (1000G) and +178% (human slice) vs -B

## Shipped-means-present (gate 8)

SKILL.md and usage-guide.md point at `examples/allele_counts.py` (present, ran from the copy) and Related Skills `alignment-filtering`, `reference-operations`, `bam-statistics`, `variant-calling/variant-calling`, `variant-calling/vcf-basics`, `variant-calling/joint-calling` — all exist in the staging clone. No missing primary file.

## Research veto

- **scientific_integrity:** PASS — No fabricated DOIs, trial results, p-values or sample sizes. The one unsourced number ('BAQ ~30% slower') was measured at +150-180% on the audit data, which is a wrong performance claim, not fabricated scientific evidence.
- **practice_boundaries:** PASS — No diagnostic or prescriptive content; the Skill steers somatic, ctDNA and germline WGS/WES production work to Mutect2 / DeepVariant / HaplotypeCaller instead of mpileup, which is the correct boundary.
- **methodological_ground:** PASS — No principled fallacy. The published rationale for the 'WRONG' samtools|bcftools pipe (double depth cap) is factually wrong (bcftools call rejects a text pileup as an unknown file type) and pysam column.n is reported as depth, but the recommended bcftools mpileup route reproduced planted truth exactly (AD 30,10; per-sample AD 17,3 / 8,12).
- **code_usability:** PASS — All Skill functions and the shipped example parse and ran (5/5 inputs executed, pysam 0.24.1). They are runnable but three helpers give silently wrong output (pileup_text depth column and missing markers, allele_counts labelling ref-skips as DEL, 'Basic Pileup' printing out-of-region columns); these are scored in Layer 2 and as P1 rather than as a veto because M4 covers unrunnable code.

## Recommendations

**[P1] pysam examples print pileup_column.n as depth** (observed in [1, 2])  
Problem: `pileup_column.n` ignores overlap removal and min_base_quality: on the real human BAM it differs from samtools mpileup depth at 1087 of 1157 positions (sum 670718 vs 353910), and pileup_text writes a depth column that disagrees with its own base column in 31 of 623 synthetic rows.  
Root cause: The pysam blocks were written as if n equalled the mpileup depth column and never compared with mpileup output.  
Fix: Report len(pileup_column.pileups) (or get_num_aligned()) as depth, and add a pysam-to-samtools parameter table: truncate=True, stepper='samtools' plus fastafile for BAQ, min_base_quality default 13, ignore_overlaps True, max_depth 8000, compute_baq.

**[P1] Ref-skips counted as deletions in every pysam helper** (observed in [2, 5])  
Problem: pysam sets is_del=True on N-skips, and every helper tests is_del first, so allele_counts reports 'DEL' for spliced reads ({'DEL': 3} at synA:400; {'DEL': 54, 'G': 5} at a real RNA-seq intron with 0 deletions) and pileup_text writes '*' instead of '>'/'<'; the is_refskip branch is dead code.  
Root cause: Branch order assumes is_del and is_refskip are exclusive.  
Fix: Test `pileup_read.is_refskip` before `is_del` in allele_counts, allele_frequency, pileup_text and both usage-guide functions.

**[P1] pileup_text is not a pileup: no ^ $ indels or qualities** (observed in [2])  
Problem: The 'Generate Pileup Text' helper emits 5 columns, no read-start/end markers, no +N/-N indel text, no quality column, and 200 of 623 synthetic positions differ from samtools mpileup (spliced positions).  
Root cause: Simplified re-implementation of mpileup presented under the same heading as the 6-column format.  
Fix: Either add the quality column, ^/$ and indel text using pileup_read.indel, or retitle it 'simplified base string' and point to samtools mpileup for the real format.

**[P1] Defaults that change the output are undocumented** (observed in [1, 3, 5])  
Problem: The Skill never gives samtools mpileup's default -Q 13 (bcftools: 1), the default excluded flags UNMAP,SECONDARY,QCFAIL,DUP (1000G BAM: 101 duplicate-flagged reads silently dropped), the depth-0 '*' rows, or that default BAQ removes bases beside a deletion (planted 3 bp deletion: depth 8 -> 4, no '-3CGT' marker unless -B).  
Root cause: Only -d, BAQ on/off and -A are treated as traps; the rest of the default filter set is left implicit.  
Fix: Add a 'What mpileup drops by default' table (flags, -q 0, -Q 13, orphans, overlap removal, -d 8000, BAQ) with the --ff/--rf, -Q, -x, -A, -B overrides.

**[P1] 'WRONG' pipe rationale false; parallel concat order broken** (observed in [4])  
Problem: samtools mpileup | bcftools call fails because a text pileup is not VCF/BCF ('unknown file type'), not from a double depth cap; and `bcftools concat chr*.vcf.gz` puts contigs in lexicographic order (chr1,chr10,chr11,chr2...), silently, with exit 0 and a valid index.  
Root cause: Rationale written from memory of the removed `mpileup -u` pipeline; loop shown with 3 contigs so the glob looks harmless.  
Fix: Reword the comment to 'samtools mpileup output is text and cannot feed bcftools call'; build the concat file list in header order (`bcftools view -h ref | ...` or `samtools idxstats | cut -f1`) and add `set -e`/wait status checks.

**[P1] Reference mismatch does not fail: exit 0 with N reference** (observed in [5])  
Problem: With a FASTA missing the BAM contig samtools mpileup prints `The sequence "MN908947.3" was not found`, still writes 4.2 MB of rows with reference base N and exits 0; the Skill's Common Errors and Troubleshooting rows quote different text ('No sequences in common', 'Reference mismatch').  
Root cause: Error text and behaviour not checked against samtools 1.24.  
Fix: Document the real message and exit status and add a `samtools view -H | grep @SQ` vs `.fai` contig-name check before running (mpileup without -f also succeeds with N, so 'No FASTA reference' is not an error).

**[P2] Cheat-sheet exome row contradicts the depth warning** (observed in [3])  
Problem: `-d 250` for capture/exome (and usage-guide `-d 500` for memory) silently caps depth at 250/500 (reproduced: 9000 reads -> 250) right after a 'Critical Trap' section warning about silent truncation.  
Root cause: Cheat-sheet rows copied from bcftools defaults.  
Fix: Use `-d 0` or a documented high cap for capture, or state the expected coverage at which the cap is safe.

**[P2] 'Basic Pileup' snippet prints out-of-region columns; 0/1-based ambiguity** (observed in [2])  
Problem: `bam.pileup('chr1', 1000000, 1001000)` without truncate=True prints 50 columns for a 10-column request; SKILL.md functions take 0-based pos while prompts say 'chr1:1000000' (calling allele_counts(..., 100) for 1-based 100 silently returns the neighbour base).  
Root cause: truncate=True and the coordinate convention appear only in some blocks and in usage-guide Tips.  
Fix: Add truncate=True to the first snippets and state '0-based pos; pass position-1' in the SKILL.md function docstrings.

**[P2] Shipped example fails with raw tracebacks on common inputs** (observed in [3])  
Problem: examples/allele_counts.py raises ValueError for contigs containing ':' (HLA-A*01:01:01:01, real UMI BAM contig), 'chr:100-110', 'chr:1,000', an unindexed BAM and an unknown contig.  
Root cause: region.split(':') without validation or try/except.  
Fix: Use rsplit(':', 1), strip commas, catch ValueError and print a one-line message naming the missing index or contig.

**[P2] Unverified or overstated statements** (observed in [5])  
Problem: 'BAQ ~30% slower' measured +152% / +178%; '-aa is required for ARTIC' is true only for multi-contig or read-less references (-a gives identical 29903 rows); '(computed from CIGAR if MD missing)' is not how mpileup BAQ works (reference-based HMM, no MD needed); format examples show depth 15 with 11 quality characters; '+NNN'/'-NNN' should read +2AC / -3CGT.  
Root cause: Numbers and notation not checked against tool output.  
Fix: Remove or source the numeric claim, say '-a is enough for a single contig; -aa adds read-less contigs', and correct the format examples.

**[P2] Indels invisible in pysam counters; prompts steer to removed -g** (observed in [2])  
Problem: allele_counts/find_variants never read pileup_read.indel, so the planted 2 bp insertion and 3 bp deletion are never reported although the Skill lists 'SNP/indel detection'; usage-guide example prompts 'Call variants using samtools mpileup and bcftools' and 'Generate BCF file' point at the removed mpileup -g route.  
Root cause: Helpers written for SNPs only; prompts predate the deprecation note.  
Fix: Add an indel branch (pileup_read.indel) or state SNP-only scope; reword the two prompts to bcftools mpileup.

**[P2] SKILL.md and usage-guide.md duplicate the same recipes** (observed in [])  
Problem: Allele counting, frequency, quality filtering, region/BED, bcftools pipelines and depth advice are written twice (375 + 258 lines) with small divergences (-d 250 vs 1000000 in multi-sample examples).  
Root cause: usage-guide restates SKILL.md.  
Fix: Keep the command reference in SKILL.md and reduce usage-guide.md to prompts and troubleshooting.

## Key strengths

- The bcftools pipeline guidance is correct and complete for small germline calling: planted SNP/ins/del recovered with exact AD (30,10), correct per-sample AD for two samples, valid annotate tags, --max-BQ 30 ont preset value and the removal of samtools mpileup -g/-u all verified on bcftools/samtools 1.24.
- Traps that matter are called out and were reproduced exactly: samtools -d 8000 vs bcftools -d 250 truncation, BAQ, -A for non-proper pairs, overlap removal (-x / --ignore-overlaps), -a/-aa zero-depth rows.
- Base-symbol table (. , ACGT acgt ^Q $ * > <) decodes correctly against planted truth, and all 8 library-typed flag rows are accepted by the installed tools and produced rows that match independent counts on real ARTIC, RNA-seq and 1000G BAMs.
- allele_counts / allele_frequency / find_variants and the shipped example give exact results for SNPs (equal to samtools mpileup -B at 106 real positions) and the example runs from a clean copy; every Related Skill path exists.

## Notes for the orchestrator

- Method traps honoured: outputs judged by asserted content, pysam vs samtools equivalence checked parameter by parameter (pysam `n`, overlap removal, BAQ via fastafile+stepper='samtools', min_base_quality default 13, max_depth 8000), every flag and default checked against the installed `--help`/behaviour.
- Two of my own first-draft checks were wrong and were corrected before scoring (deletion marker under default BAQ; BED region beyond the covered gap; `-Q` also thins the '*' deletion slots): the logs kept are the final runs.