> **Audit record for `bio-pileup-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@ad9b5a4](https://github.com/mrsonord2240/bioSkills/tree/ad9b5a4ec484bcfc7d12e38a03a31d2a60cf6429/alignment-files/pileup-generation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pileup-generation (RE-AUDIT)

Generated: 2026-09-20 | Re-auditor: fresh Sonnet (different from first auditor and fixer) | Source: `mrsonord2240/bioSkills@ad9b5a4ec484bcfc7d12e38a03a31d2a60cf6429:alignment-files/pileup-generation`

Env: WSL `science`, env `alignment-files` (samtools 1.24, bcftools 1.24, pysam 0.24.1). The Skill folder was copied from worktree `wt\af-pileup` (commit ad9b5a4) to `run/skill/` (md5 identical to the worktree files) and run from the copy; the worktree was not written.

## Result

**Pre-fix 71 (Beta Only, not deployable) -> now 84/100, ✅ Limited Release, deployable: true, veto: none, executed 7/7 inputs, scripted checks 223/230, assertions 29/35.** Static 81/100 (x0.4 = 32.4); execution average 86.1/100 (x0.6 = 51.7); Layer 1 avg 34.3/40, Layer 2 avg 51.9/60. No open P0. One open P1, five P2. Floors for Limited Release met (static >= 70, exec >= 75, L1 >= 28, L2 >= 42, assertions 29/35 = 83% >= 80%); the Production Ready floor for assertions (90%) is not met and the score is 84.

Skill Veto: T1 PASS, T2 PASS, T3 PASS (all outputs deterministic on repeat), T4 PASS. Research Veto (Data Analysis): M1-M4 PASS.

**Classification:** Data Analysis (3), mode D, Moderate. N = 7: inputs 1-5 are the archived pre-fix inputs re-run as regression tests; inputs 6-7 are new and use planted truth and data the fixer never saw.

## What broke or was left (only my runs count as evidence)

- **[P1] False claim: pysam stepper='all' + fastafile applies no BAQ** (inputs [1, 7]): SKILL.md says the default stepper='all' does not apply BAQ even with a fastafile. In pysam 0.24.1 it does: depth equals samtools mpileup default (BAQ on) at all 1157 real positions, differs from -B at 40, and is 4 vs 8 at the planted deletion; only compute_baq=False restores -B.
- **[P2] Options table equates bcftools --nu with samtools --rf** (inputs [7]): Row '--rf FLAGS (bcftools --nu): keep only reads with any of these flags set' is wrong for bcftools: --nu skips reads with ANY bit unset, i.e. needs ALL bits. Mask 65 keeps 6 reads in samtools --rf and 2 in bcftools --nu.
- **[P2] pileup_text drops a second indel marker next to another indel** (inputs [6]): For a read whose CIGAR has an insertion directly before a deletion (10M2I2D10M) or a deletion before an insertion, samtools prints '+2ca-2at' and pileup_text prints '+2ca'. Equal on 4,486 clean-CIGAR fuzz rows x 13 option sets and 432,147 real rows; ~5% of exotic-CIGAR fuzz rows differ, all indel-marker only.
- **[P2] find_variants reports N artifacts** (inputs [6]): On the planted N sites it returns nA:800 ref N > A (9/9) and nA:790 G>N (1/7) as variants (min_base_quality default 20 keeps the Q40 N read).
- **[P2] Dedup dropped read-name/strand access; example not referenced** (inputs [2, 7]): The old 'Access Individual Reads' variant printed alignment.query_name and strand; SKILL.md keeps only base+quality, so 'which reads carry the alt allele' has no snippet. examples/allele_counts.py is mentioned nowhere in SKILL.md or the guide.
- **[P2] Soft-masked FASTA prints lower-case reference bases** (inputs [6]): With a soft-masked reference (UCSC-style hg38.fa) samtools mpileup column 3 is lower-case ('g'); the Output Format table says only 'Reference base'. pileup_text reproduces it, allele helpers upper-case.

I found no regression of anything that worked before the fix: the five re-run pre-fix inputs (t01-t05) pass 145 of 146 scripted checks; the one failure is the P1 above.

## Static scores (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 9/12 | Completeness 3: text pileup, region/BED, multi-BAM, filters, defaults table, BAQ, bcftools calling/joint/parallel, pysam helpers all present and verified; indel allele counting deliberately out of scope (stated). Correctness 3: every checked command, default and message reproduced, but three statements are wrong (stepper='all'+fastafile BAQ, --nu == --rf, pileup_text on adjacent I/D). Appropriateness 3: a 40-line Python pileup_text re-implements a tool that is one shell command. |
| reliability | 10/12 | Fault tolerance 3 and error reporting 3: Common Errors quote real messages and the exit-0-with-N trap plus a contig pre-check; the shipped example rejects 9 hostile inputs with one 'Error:' line (a missing file also prints an htslib line first); the parallel block stops on failure. Recoverability 4: read-only, idempotent, safe to re-run. |
| performance_context | 6/8 | Token cost 3: SKILL.md grew to 446 lines (was 375) but the guide fell from 258 to 46 lines and the duplicated recipes are gone; no references/ split. Execution efficiency 3: linear workflows, one long helper (pileup_text). |
| agent_usability | 14/16 | Learnability 3, consistency 4 (0/1-based rule and 'depth = len(pileups)' stated and used everywhere), feedback design 3 (formats, message texts and example rows given; no expected-output self-check for the pipelines), error prevention 4 (max depth, BAQ, -Q 13, default flags, ref mismatch exit 0, max_depth=0, concat order, memory hog all called out and verified). |
| human_usability | 6/8 | Discoverability 3: description unchanged and terse (no mention of text pileup/depth/BAQ). Forgiveness 3: example accepts commas and colon contigs and rejects ranges/typos with a one-line message. |
| security | 11/12 | No credentials, no eval/exec, no shell built from user strings in the example; helpers take paths only. Input validation 3: shell blocks assume trusted file names. |
| maintainability | 9/12 | Modularity 3 (one SKILL.md holds everything, guide is thin), modifiability 3, testability 3 (real example rows and message texts to check against; still one example and no test script). |
| agent_specific | 16/20 | Trigger precision 3, progressive disclosure 3 (446 lines, under 500, no references/), composability 3 (Related Skills all exist), idempotency 4, escape hatches 3 (tool table sends somatic/WGS production/long-read work elsewhere). |

**Static subtotal: 81/100** (pre-fix 69)

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Checks | Executed | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 54 | 89 | 4/5 | 27/28 | yes | ✅ |
| 2 | Variant A | 35 | 53 | 88 | 4/5 | 28/28 | yes | ✅ |
| 3 | Edge | 36 | 54 | 90 | 5/5 | 41/41 | yes | ✅ |
| 4 | Variant B | 35 | 54 | 89 | 5/5 | 21/21 | yes | ✅ |
| 5 | Stress | 35 | 53 | 88 | 5/5 | 28/28 | yes | ✅ |
| 6 | Variant B | 33 | 49 | 82 | 3/5 | 54/56 | yes | ✅ |
| 7 | Stress | 31 | 46 | 77 | 3/5 | 24/28 | yes | ✅ |

**Execution Average: 86.1 / 100** | **Assertion Pass Rate: 29/35**

## Detailed inputs

### Input 1 — Canonical: Text pileup of the real human chr22 BAM (region/BED/-q/-Q), columns and symbols, depth cross-checked (REGRESSION of pre-fix input 1)

**Prompt:** Generate a text pileup for chr22:1952-4617 of my BAM (nf-core human test slice) with MAPQ>=20 and baseQ>=20, tell me what each column and symbol means, and check the depth against another tool.

**Executed:** true. executed; 27/28 checks pass (t01). One Skill claim is false: stepper='all' + fastafile DOES apply BAQ.

**Code that ran:** `run/t01_regress_real_mpileup.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
[PASS] in1 basic mpileup with -r runs and prints rows  -- rc=0 rows=1157 stderr='[mpileup] 1 samples in 1 input files'
[PASS] in1 Output Format: 6 columns for one BAM  -- Counter({6: 1157})
[PASS] in1 col3 = FASTA base (upper-case here), col2 1-based
[PASS] in1 Output Format table: col4 depth == number of read symbols in col5 == number of chars in col6
[PASS] in1 Output Format: the Skill's example 'chr22 1952 T 0 * *' is real: exact row present, col5 and col6 both '*'  -- 3 depth-0 rows, first [['chr22', '1952', 'T', '0', '*', '*'], ['chr22', '1953', 'T', '0', '*', '*']]
[PASS] in1 SKILL.md text contains the depth-0 explanation and the exact example row
[PASS] in1 '^Q' MAPQ+33: decoded MAPQs are a subset of the BAM's MAPQs; MAPQ 60 -> '^]'  -- {60: 3182, 54: 1, 42: 1}
[PASS] in1 mpileup -B -Q0 -q0 -x -A -a depth == samtools depth -a -J at every position (independent tool)  -- positions=2666 diffs=[] max=2532
[PASS] in1 pysam defaults == samtools mpileup -B, position by position (len(pileups)); Skill: 'pysam defaults equal -B'  -- 0 of 1157 differ; sum 353982 vs 353982
[PASS] in1 stepper='samtools' + fastafile == samtools mpileup default (BAQ), position by position  -- 0 of 1157 differ; sum 353910 vs 353910
[PASS] in1 Skill claim reproduced: pileup_column.n differs from the default mpileup depth at 1087 of 1157 positions on this BAM  -- n differs at 1087 of 1157 (vs -B: 1084)
[FAIL] in1 Skill claim: stepper='all' + fastafile does NOT apply BAQ (== mpileup -B, != default)   -- vs -B 40 differ; vs default 0 differ
[PASS] in1 -q 20: depth == independent count of reads with MAPQ>=20  -- sum 670999
[PASS] in1 -q 60: depth == independent count of reads with MAPQ>=60  -- sum 670681
[PASS] in1 -Q 13: depth == independent count of bases with baseQ>=13  -- sum 670651
[PASS] in1 -Q 20: depth == independent count of bases with baseQ>=20  -- sum 661117
[PASS] in1 -Q 30: depth == independent count of bases with baseQ>=30  -- sum 654118
[PASS] in1 Options table: samtools default -Q is 13 (explicit -Q 13 output identical to default)
[PASS] in1 Options table: -Q 0 changes the output (default silently drops low-quality bases)  -- 670718 vs 353910
[PASS] in1 Options table: default --ff is UNMAP,SECONDARY,QCFAIL,DUP (explicit named list == default; --ff 0 adds reads)  -- --ff 0 sum 671070 vs default 670999; named==default True
flag distribution: {99: 1402, 163: 1417, 147: 1402, 83: 1417, 387: 1, 371: 1, 97: 1, 145: 1}
[PASS] in1 -r single position -> exactly one row at 3000
[PASS] in1 -r accepts thousands separators
[PASS] in1 SKILL-style far region on the renumbered slice: 0 rows, no error (env trap)
[PASS] in1 Common Errors: '[E::mpileup] fail to parse region '22:3000-3005'' is the real message for a contig mismatch  -- [E::mpileup] fail to parse region '22:3000-3005' with /mnt/openscience/audit-envs/alignment-files/public-data/human/test
[PASS] in1 -l BED (0-based half-open) -> 1-based positions 3000-3003, 3100-3101
[PASS] in1 Output Format: '3 shared columns, then 3 per input BAM' -> 9 columns for two BAMs
[PASS] in1 bcftools mpileup FORMAT/DP == samtools depth minus '*' deletion slots at every position (second tool)  -- 1181 positions
[PASS] in1 Output Format example rows equal real 1000G output  -- ['chr20\t1400300\tG\t6\t,,,.,,\tBBB<BB', 'chr20\t1400301\tC\t6\t,,,.,,\tBB<BBB']
symbols present in this real BAM's pileup: {'*': 4, '.': 180037, 'T': 18, ',': 173595, 'C': 20, 'G': 90, 'g': 24, 'c': 44, 'a': 21, '$': 3234, 'A': 29, 't': 29}
SUMMARY in1: 27/28 assertions passed
```

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] Output Format table and the quoted example row 'chr22 1952 T 0 * *' are true: 6 columns, depth == symbols == qualities, depth-0 rows exist — 1157 rows; 3 depth-0 rows incl. the exact quoted row
- [PASS] pysam len(pileups) == samtools mpileup depth at every position: pysam defaults == -B, stepper='samtools'+fastafile == default; n differs at 1087 of 1157 — 0 of 1157 differ in both comparisons; 1087 reproduced
- [PASS] -q/-Q/-Q 13 default/--ff default UNMAP,SECONDARY,QCFAIL,DUP behave as documented against independent pysam-record counts and samtools depth — -q 20/60 and -Q 13/20/30 equal at every position; named --ff list == default
- [PASS] Region, BED, multi-BAM (9 columns), '[E::mpileup] fail to parse region' message, 1000G example rows and bcftools DP (minus '*') are as documented — 1000G rows identical to the Skill's example
- [FAIL] Skill statement 'stepper=all + fastafile does not apply BAQ' is true — false in pysam 0.24.1: depth equals mpileup default (BAQ) at all 1157 positions and differs from -B at 40

### Input 2 — Variant A: pysam allele counts / frequency / find_variants / pileup_text on planted synthetic BAM and real BAM, shipped example (REGRESSION of pre-fix input 2)

**Prompt:** Count the alleles and alt fraction at synA:100 (planted SNP) and at real chr22 positions with pysam, make a per-position pileup text, and list positions with >10% alternative alleles.

**Executed:** true. executed; 28/28 checks pass (t02); every pre-fix pysam defect here is gone.

**Code that ran:** `run/t02_regress_pysam_helpers.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
[PASS] in2 usage-guide.md no longer carries code that duplicates SKILL.md (0 python blocks) and SKILL.md has no stale count_alleles/min_qual API
[PASS] in2 Basic Pileup snippet (truncate=True): exactly the 10 requested columns 101..110 (1-based printed) with mpileup -B depths  -- [(101, 40), (102, 40), (103, 40)]
[PASS] in2 Access Reads snippet at synA:100 lists 30 ref and 10 alt reads, all Q40, 'Depth: 40'  -- {('C', '40'): 10, ('T', '40'): 30}
[PASS] in2 Access Reads snippet in the spliced region synA:400: 3 'Reference skip', no 'Deletion' (Skill: is_refskip first)  -- Position: 399|Depth: 3|  Reference skip|  Reference skip|  Reference skip|
[PASS] in2 Access Reads snippet at the real deletion synA:251: 4 'Deletion' + 4 bases (deletion still reported)  -- Position: 250|Depth: 8|  Deletion|  Deletion|  C (Q40)|  C (Q40)|  C (Q40)|  C (Q40)|  Deletion|  Deletion|
[PASS] in2 Quality Filtering snippet prints the real depth: synA:725 -> 4 (6 Q5 bases filtered) and every printed depth == mpileup -B -q20 -Q20  -- 725 -> 4
[PASS] in2 allele_counts(synA, 99) == planted {T:30, C:10}  -- {'C': 10, 'T': 30}
[PASS] in2 allele_frequency == {T:0.75, C:0.25}  -- {'C': 0.25, 'T': 0.75}
[PASS] in2 docstring + call examples state 0-based / 1-based (pos - 1 pattern)
[PASS] in2 allele_counts default drops six Q5 alt bases at synA:725 (only 4 ref); min_base_quality=0 keeps them (alt 6)  -- ({'C': 4}, {'T': 6, 'C': 4})
[PASS] in2 SNV-only scope: allele_counts at the insertion site synA:200 -> {'A': 10}; docstring states insertions are not counted  -- {'A': 10}
[PASS] in2 allele_counts at the deleted base synA:251 == {DEL:4, ref:4}  -- {'DEL': 4, 'C': 4}
[PASS] in2 allele_counts inside a spliced region synA:400 == {} (ref skips not counted, was {'DEL': 3} before the fix)
[PASS] in2 allele_counts at the overlap site 930 (5 pairs, R1 ref/R2 alt) == mpileup -B parse  -- ({'C': 2, 'T': 3}, {'ref_fwd': 2, 't': 3})
[PASS] in2 allele_counts == parse of samtools mpileup -B at 110 real chr22 positions (incl. indel sites)
[PASS] in2 find_variants recovers only the planted SNP synA:100 T>C depth 40 alt 10 freq 0.25  -- [{'chrom': 'synA', 'pos': 100, 'ref': 'T', 'alt': 'C', 'depth': 40, 'alt_count': 10, 'freq': 0.25}]
[PASS] in2 find_variants is SNV-only as stated: nothing at the planted indels (200, 250) and none inside the splice (326-525)  -- [100, 930]
[PASS] in2 find_variants on real chr22 == independent mpileup -B -Q20 parse (same alt sites and counts)  -- skill 4 vs mpileup 4: [(1982, 'A', 'G', 24), (3266, 'T', 'C', 12), (3406, 'T', 'G', 3)]
[PASS] in2 pileup_text default (BAQ) == samtools mpileup, row-for-row on synA (623 rows, splice/indel/overlap/flag events)  -- 623 rows; diffs []
[PASS] in2 pileup_text compute_baq=False == samtools mpileup -B, row-for-row  -- 623 rows; diffs []
[PASS] in2 pileup_text hand counts: '+2AC' x3 and '+2ac' x2 at synA:200 (depth 10)  -- ({'+2AC': 3, '+2ac': 2}, '10')
[PASS] in2 pileup_text -B hand counts: '-3CGT' x2 and '-3cgt' x2 at synA:250 (depth 8); default BAQ hides them (depth 4, no marker) as the Skill says  -- ({'-3CGT': 2, '-3cgt': 2}, '8', ['4', '....'])
[PASS] in2 pileup_text spliced site synA:400: '>><' (was '***'); depth 3  -- >><
[PASS] in2 pileup_text emits '^]' (MAPQ 60) and '$' markers and a quality column; zero-depth row format  -- ('^].^].^].^].', '.$.$.$.$')
[PASS] in2 pileup_text(-q 20 -Q 20 -x -A equivalents) == samtools mpileup on synA
[PASS] in2 examples/allele_counts.py synA:100 -> T 30 (75.0%) / C 10 (25.0%), depth 40, rc 0  -- Position: synA:100|Total depth: 40|Allele counts:|  T: 30 (75.0%)|  C: 10 (25.0%)|
[PASS] in2 examples/allele_counts.py real chr22:3000 total depth == samtools mpileup -B -q20 -Q20 (781)  -- Position: chr22:3000|Total depth: 781|Allele counts:|  A: 781 (100.0%)|
[PASS] in2 examples/allele_counts.py at the spliced synA:400: depth 0 (skips not counted)  -- Position: synA:400|Total depth: 0|Allele counts:|
SUMMARY in2: 28/28 assertions passed
```

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**
- [PASS] allele_counts / allele_frequency / find_variants recover the planted SNP (T30/C10, 25%), report ref-skips as nothing (was DEL 3) and equal a mpileup -B parse at 110 real positions — find_variants on real chr22 == independent parse (4 sites)
- [PASS] Module snippets print what they claim: 'Basic Pileup' only the 10 requested columns, refskip vs deletion, quality-filtered depth 4 at synA:725 — all equal mpileup -B -q20 -Q20
- [PASS] pileup_text == samtools mpileup row-for-row (623 rows, default and -B and -q20 -Q20 -x -A) and hand counts +2AC x3 / +2ac x2, -3CGT x2 / -3cgt x2, '>><' — was 5 columns, 31 wrong depths, no markers pre-fix
- [PASS] examples/allele_counts.py: synA:100 -> T 30 / C 10; real chr22:3000 depth 781 == mpileup — runs from the copy
- [FAIL] usage-guide dedup lost nothing an agent needs — the read-name + strand print variant (query_name / is_reverse) was dropped; examples/allele_counts.py is not referenced from SKILL.md or the guide

### Input 3 — Edge: Exact symbol decoding, every silent default, max depth and the shipped example on hostile input (REGRESSION of pre-fix input 3)

**Prompt:** Explain exactly how insertions, deletions, spliced reads, read starts/ends and soft clips appear in the pileup base column and which reads mpileup drops by default (flags, MAPQ, baseQ, overlaps, orphans, max depth); my amplicon library is 9000x deep. Then run the example script on unusual region strings.

**Executed:** true. executed; 41/41 checks pass (t03).

**Code that ran:** `run/t03_regress_edge_defaults.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
[PASS] in3 SNP synA:100: '.' x14, ',' x16, 'C' x6, 'c' x4, depth 40  -- {'C': 6, 'ref_fwd': 14, 'c': 4, 'ref_rev': 16}
[PASS] in3 '^]' x40 at read start (MAPQ 60 + 33 = ']')
[PASS] in3 '$' x40 at read end
[PASS] in3 insertion row 200: '+2AC' x3, '+2ac' x2, depth 10 (Skill symbol table)  -- {'ref_fwd': 8, '+AC': 3, 'ins': 5, 'ref_rev': 2, '+ac': 2}
[PASS] in3 -B deletion row 250: '-3CGT' x2, '-3cgt' x2, depth 8  -- {'ref_fwd': 6, '-CGT': 2, 'delmark': 4, 'ref_rev': 2, '-cgt': 2}
[PASS] in3 Skill claim (BAQ section): default text pileup hides the deletion: depth 8 -> 4, no '-3CGT' marker  -- ['4', '....']
[PASS] in3 deleted bases synA:251-253 are '*' x4 with depth 8
[PASS] in3 '#' for reverse-strand deletions with --reverse-del (Skill symbol table)  -- **....##
[PASS] in3 splice N-gap synA:400: '>' x2, '<' x1, depth 3
[PASS] in3 soft-clipped TTTTT never appear in rows 396-405
[PASS] in3 default flags: depth 10 at synA:825 (DUP/SECONDARY/QCFAIL/UNMAP dropped); --ff 0 -> 16; --ff DUP -> 13  -- ('10', '16', '13')
[PASS] in3 -q 10 drops 5 MAPQ-5 reads at synA:625 (10 -> 5)
[PASS] in3 Options table -Q 13 default: synA:725 depth 4 default, 10 with -Q 0
[PASS] in3 overlap removal: depth 5 default vs 10 with -x / --disable-overlap-removal / --ignore-overlaps-removal
[PASS] in3 bcftools spelling --ignore-overlaps works: DP 10 vs 5 default  -- 67,0,44,73,53,116:5:2,3,0 / 118,0,118,133,133,242:10:5,5,0
[PASS] in3 orphans (flag 65): dropped by default, 4 with -A (Skill table)
[PASS] in3 bcftools default --ns = UNMAP,SECONDARY,QCFAIL,DUP: DP 10 default vs 16 with --ns 0 (Skill table: '--ff (bcftools --ns)')  -- 0,30,191:10:10,0 / 0,48,210:16:16,0
[PASS] in3 bcftools default min-BQ is 1 (Q5 bases kept: DP 10 default, 10 at -Q 5, 4 at -Q 6); samtools default 13 drops them  -- 3,0,118,15,136,128:10:4,6,0 3,0,118,15,136,128:10:4,6,0 0,12,146:4:4,0
help text extract (samtools mpileup): ['-d, --max-depth INT     max per-file depth; avoids excessive memory usage [8000]', '-q, --min-MQ INT        skip alignments with mapQ smaller than INT [0]', '-Q, --min-BQ INT        skip bases with baseQ/BAQ smaller than INT [13]', '--ff, --excl-flags STR|INT'
help text extract (bcftools mpileup): []
[PASS] in3 Options table: -a = every position of contigs that have reads (synA 1000, synC 300; no synB); -aa also the read-less contig synB (500 rows)  -- ({'synA': 623, 'synC': 50}, {'synA': 1000, 'synC': 300}, {'synA': 1000, 'synB': 500, 'synC': 300})
[PASS] in3 zero-depth row: 'synB 1 <ref> 0 * *'
[PASS] in3 samtools: default caps 9000 reads at 8000; -d 0 and -d 1000000 give 9000; -d 250 gives 250  -- {'': 8000, '-d 8000': 8000, '-d 0': 9000, '-d 1000000': 9000, '-d 250': 250}
[PASS] in3 bcftools: default 250; -d 0, -d 1000000, -d 100000 give 9000 (Skill cheat sheet 'Capture / exome: -d 0' now safe)  -- {'': 250, '-d 250': 250, '-d 0': 9000, '-d 1000000': 9000, '-d 100000': 9000}
[PASS] in3 Skill claim: pysam max_depth default 8000 and max_depth=0 is NOT unlimited (still 8000); max_depth=1000000 -> 9000  -- {'default': (8000, 8000), 'max_depth=0': (8000, 8000), 'max_depth=8000': (8000, 8000), 'max_depth=1000000': (9000, 9000), 'max_depth=250': (250, 250)}
[PASS] in3 cheat sheet rows on the 9000x BAM never cap (depth 9000 for every row that sets -d 0 / -d 600000)  -- {'germline `-q 20 -Q 20 -d 0`': 9000, 'exome `-q 20 -Q 20 -d 0`': 9000, 'tumor `-q 1 -Q 13 -d 0 -B`': 9000, 'ARTIC `-aa -A -d 600000 -B -Q 20`': 9000, 'ONT `-q 30 -Q 0 -B -d 0`': 9000}
[PASS] in3 BAQ default changes qualities near the planted indels vs -B
[PASS] in3 Common Errors: samtools mpileup without -f succeeds with reference column N  -- synA	100	N	40	CCCCCCTTTTTTTTTTTTTTcccctt
[PASS] in3 Common Errors: bcftools mpileup without -f refuses: 'requires the --fasta-ref option'  -- Error: mpileup requires the --fasta-ref option by default; use --no-reference to run without a fasta reference
[PASS] in3 BAQ table: -B and -E cannot be combined (Skill) -> samtools refuses  -- Error: The -B option cannot be combined with -E
[PASS] in3 Deprecation section: samtools mpileup -g no longer exists (removed in 1.15)  -- mpileup: invalid option -- 'g'
[PASS] in3 example, range synA:100-110: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err="Error: expected <contig>:<1-based position>, got 'synA:100-110' (ranges are not supported)"
[PASS] in3 example, missing colon: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err="Error: expected <contig>:<1-based position>, got 'synA100' (ranges are not supported)"
[PASS] in3 example, position 0: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err="Error: expected <contig>:<1-based position>, got 'synA:0' (ranges are not supported)"
[PASS] in3 example, unknown contig: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err=" contig 'nosuch' is not in the BAM header (see: samtools view -H /mnt/openscience/audits/bio-pileup-generation/run/data/syn.bam | grep ^@SQ)"
[PASS] in3 example, unindexed BAM: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err='up-generation/run/work/t03/noidx.bam has no index (run: samtools index /mnt/openscience/audits/bio-pileup-generation/run/work/t03/noidx.bam)'
[PASS] in3 example, garbage file: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err='Error: cannot read /mnt/openscience/audits/bio-pileup-generation/run/work/t03/garbage.bam: file does not contain alignment data'
[PASS] in3 example, nonexistent file: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err="m: [Errno 2] Could not open alignment file: No such file or directory: '/mnt/openscience/audits/bio-pileup-generation/run/work/t03/nope.bam'"
[PASS] in3 example, letters as position: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err="Error: expected <contig>:<1-based position>, got 'synA:abc' (ranges are not supported)"
[PASS] in3 example, empty position: rc 1, last stderr line is 'Error: ...' naming the problem, no traceback  -- rc=1 err="Error: expected <contig>:<1-based position>, got 'synA:' (ranges are not supported)"
[PASS] in3 example: thousands separator synA:1,000 accepted (position 1000; real depth from mpileup)  -- Position: synA:1000|Total depth: 0|Allele counts:
[PASS] in3 example: position beyond contig end does not print a traceback  -- rc=0 out='Position: synA:5000\nTotal depth: 0\nAllele counts:' err=''
[PASS] in3 example: missing region -> usage line, rc 1
SUMMARY in3: 41/41 assertions passed
```

**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Assertions:**
- [PASS] Symbol table (^], $, +2AC/+2ac, -3CGT/-3cgt, *, #, >/<, soft clips absent) matches planted truth; default BAQ hides the deletion (depth 8 -> 4) — hand-derived counts
- [PASS] Defaults table verified by behaviour: -Q 13 (4 vs 10), --ff default (10 vs 16), overlap 5 vs 10 with -x and both long forms, orphans 0 vs 4 with -A, bcftools --ns/-Q 1/-d 250, -a vs -aa — and help text for -Q/-d/-q/--ff
- [PASS] Max depth: samtools 8000 cap, -d 0 unlimited, bcftools 250 vs -d 0/100000/1000000 = 9000, pysam default 8000 and max_depth=0 NOT unlimited; all 8 cheat-sheet rows run without capping — 9000x BAM
- [PASS] Common Errors/BAQ statements: no -f -> N (rc 0), bcftools refuses, -B with -E rejected, samtools mpileup -g removed — real messages
- [PASS] Shipped example on 9 hostile inputs (range, no colon, pos 0, unknown contig, unindexed, garbage/nonexistent file, letters, empty) exits 1 with a last line 'Error: ...' and no traceback; commas and pos beyond contig end handled — was raw ValueError tracebacks

### Input 4 — Variant B: bcftools mpileup | call: germline, BCF intermediate, multi-sample -d 100000, parallel-by-contig, the 'WRONG' pipe (REGRESSION of pre-fix input 4)

**Prompt:** Call variants from my BAM with the modern bcftools mpileup | bcftools call pipeline (single sample, BCF intermediate, joint calling of 2 samples, parallel per chromosome) and tell me if `samtools mpileup | bcftools call` is really wrong and why.

**Executed:** true. executed; 21/21 checks pass (t04); bash blocks extracted verbatim from SKILL.md.

**Code that ran:** `run/t04_regress_bcftools.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
[PASS] in4 Modern Germline Calling block runs (verbatim) and writes variants.vcf.gz + .tbi  -- rc=0 ites are diploid
[PASS] in4 planted SNP synA:100 T>C called with FORMAT/AD 30,10 and FORMAT/DP 40 (planted truth), INFO/AD present  -- {'GT': '0/1', 'PL': '186,0,255', 'DP': '40', 'SP': '1', 'AD': '30,10'}
[PASS] in4 planted 2 bp insertion (AA>AACA at 200) and 3 bp deletion (TCGT>T at 250) are called (default BAQ + -Q 20)  -- [(100, 'T', 'C'), (200, 'AA', 'AACA'), (250, 'TCGT', 'T'), (930, 'C', 'T')]
[PASS] in4 no unexplained records (only SNP 100, ins 200, del 250, overlap-conflict site 930)  -- [100, 200, 250, 930]
[PASS] in4 BCF Intermediate block runs; raw.bcf non-empty; calling from it gives the planted SNP/ins/del  -- rc=0 calls=[100, 200, 250, 930]
[PASS] in4 Multi-Sample block (-d 100000, --threads 4) runs; samples s1,s2 from @RG SM; per-sample AD == planted (17,3 | 8,12)  -- rc=0 samples=['s1', 's2'] AD=100 17,3|8,12|
[PASS] in4 no 'Potential memory hog' warning with the Skill's -d 100000 and 2 samples  -- Note: none of --samples-file, --ploidy or --ploidy-file given, assuming all sites are diploid
[PASS] in4 Skill claim reproduced: -d 1000000 with 2 samples makes bcftools 1.24 warn 'Potential memory hog'  -- [mpileup] maximum number of reads per input file set to -d 1000000
[PASS] in4 control: -d 1000000 with ONE sample gives no memory warning (Skill's single-sample blocks use -d 1000000)  -- [mpileup] maximum number of reads per input file set to -d 1000000
[PASS] in4 Maximum Depth block text: the WRONG comment now says text pileup is not VCF/BCF and quotes the real error; no 'double cap' rationale remains  -- ['# "Failed to read from standard input: unknown file type"', 'samtools mpileup -f ref.fa in.bam | bcftools call -mv', '']
[PASS] in4 Skill's stated error text is what bcftools 1.24 prints for the WRONG pipe and the exit status is non-zero (255)  -- te: none of --samples-file, --ploidy or --ploidy-file given, assuming all sites are diploid
[PASS] in4 without pipefail the pipeline's exit status is that of bcftools call: 255 (agents should not treat the pipe as success)  -- rc=255
[PASS] in4 RIGHT pipe (bcftools mpileup -d 1000000 | call) returns 4 records  -- 4
[PASS] in4 Parallel-by-Contig block (verbatim): all.vcf.gz has 11 records in HEADER contig order chr1..chr11 (glob order would be chr1,chr10,chr11,chr2...)  -- rc=0 records=['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11']
[PASS] in4 Parallel block builds the index and every record is the planted pos-100 SNP  -- ['all.vcf.gz', 'all.vcf.gz.csi', 'blk.sh', 'chr1.vcf.gz', 'chr10.vcf.gz', 'chr11.vcf.gz', 'chr2.vcf.gz', 'chr3.vcf.gz']
[PASS] in4 Parallel block with a missing reference: non-zero exit and no all.vcf.gz (failure not swallowed)  -- rc=124 files=['blk.sh', 'contigs.txt']
[PASS] in4 Parallel block with one bad contig: xargs exits non-zero and concat is skipped (no all.vcf.gz)  -- rc=124 files=['blk.sh', 'chr1.vcf.gz', 'chr2.vcf.gz', 'contigs.txt', 'contigs_bad.txt']
[PASS] in4 Parallel block on the 3-contig synthetic BAM (one contig without reads) still completes and finds the planted SNP  -- rc=0 ['synA', '100', 'synA', '200', 'synA', '250', 'synA', '930'] 002246 seconds
[PASS] in4 annotate tags named in the Skill (FORMAT/AD,DP,SP, INFO/AD) exist in bcftools 1.24  -- Annotations added by default are in this list prefixed with "*". To suppress their output, run with
[PASS] in4 `--max-BQ 30` is the `ont` preset value (Skill's ONT cheat-sheet note)  -- '\nont\n    -B -Q5 --max-BQ 30 -I\n\nont-sup,'
[PASS] in4 real chr22 slice: every strong (>=30% alt, >=10 reads) site of the independent mpileup parse is called by the Skill's germline recipe  -- missing []
SUMMARY in4: 21/21 assertions passed
```

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] Germline, BCF-intermediate and multi-sample blocks reproduce planted truth: SNP 100 AD 30,10 DP 40, AA>AACA, TCGT>T, per-sample AD 17,3 | 8,12 — verbatim blocks
- [PASS] Multi-sample -d 100000 example is safe and the note is true: no memory warning at 2 samples/-d 100000, warning at -d 1000000 x 2 samples and at 11 files x 100000; none for one sample — bcftools 1.24 prints 'Potential memory hog'
- [PASS] The 'WRONG' pipe explanation is now correct: text pileup is not VCF/BCF, real error text 'Failed to read from standard input: unknown file type', exit 255 — no 'double cap' rationale left
- [PASS] Parallel-by-Contig block: header contig order chr1..chr11 (not glob order), index built, missing reference / bad contig -> non-zero and no all.vcf.gz — was chr1,chr10,chr11,chr2,... with exit 0
- [PASS] Real chr22 slice: every strong (>=30% alt, >=10 reads) site of an independent mpileup parse is called; --max-BQ 30 is the ont preset value — sites 3266, 3413

### Input 5 — Stress: Library cheat sheet on real ARTIC, spliced RNA-seq and 1000G BAMs; reference mismatch and index errors (REGRESSION of pre-fix input 5)

**Prompt:** Apply the library-typed flag cheat-sheet to my ARTIC SARS-CoV-2 nanopore amplicon BAM (consensus needs zero-coverage rows), an RNA-seq BAM and a 1000G germline BAM, and tell me what happens when the reference does not match the BAM.

**Executed:** true. executed; 28/28 checks pass (t05); real data only.

**Code that ran:** `run/t05_regress_library_real.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
cheat-sheet rows read from SKILL.md: [('Short-read germline WGS (BWA)', '-q 20 -Q 20 -d 0'), ('Short-read tumor WGS', '-q 1 -Q 13 -d 0 -B'), ('Amplicon viral (ARTIC)', '-aa -A -d 600000 -B -Q 20'), ('Capture / exome', '-q 20 -Q 20 -d 0'), ('Long-read ONT R10.4+', '-q 30 -Q 0 -B -d 0'), ('PacBio HiFi
[PASS] in5 cheat sheet has the 8 library rows and no row caps depth at 250 (`-d 250` absent)  -- [('Short-read germline WGS (BWA)', '-q 20 -Q 20 -d 0'), ('Short-read tumor WGS', '-q 1 -Q 13 -d 0 -B'), ('Amplicon viral (ARTIC)', '-aa -A -d 600000 -B -Q 20'), ('Capture / exome', '-q 20 -Q 20 -d 0'), (
[PASS] in5 cheat-sheet row 'Short-read germline WGS (BWA)': `-q 20 -Q 20 -d 0` accepted, produces rows  -- rc=0 rows=1157
[PASS] in5 cheat-sheet row 'Short-read tumor WGS': `-q 1 -Q 13 -d 0 -B` accepted, produces rows  -- rc=0 rows=1157
[PASS] in5 cheat-sheet row 'Amplicon viral (ARTIC)': `-aa -A -d 600000 -B -Q 20` accepted, produces rows  -- rc=0 rows=2666
[PASS] in5 cheat-sheet row 'Capture / exome': `-q 20 -Q 20 -d 0` accepted, produces rows  -- rc=0 rows=1157
[PASS] in5 cheat-sheet row 'Long-read ONT R10.4+': `-q 30 -Q 0 -B -d 0` accepted, produces rows  -- rc=0 rows=1157
[PASS] in5 cheat-sheet row 'PacBio HiFi': `-q 20 -Q 0 -B -d 0` accepted, produces rows  -- rc=0 rows=1157
[PASS] in5 cheat-sheet row 'RNA-seq variants': `-q 20 -Q 20 -B -d 0` accepted, produces rows  -- rc=0 rows=1157
[PASS] in5 cheat-sheet row 'Forensic / aDNA': `-q 0 -Q 0 -A -d 0 -B` accepted, produces rows  -- rc=0 rows=1181
[PASS] in5 ONT row for bcftools (`-q 30 -Q 0 -B -d 0 --max-BQ 30`) is accepted  -- chr22	3000
[PASS] in5 ARTIC row: 29903 rows (one per genome position), MN908947.3  -- 29903 rows in 0.1s
[PASS] in5 ARTIC depth (minus '*' slots) == independent pysam count of aligned bases with baseQ>=20 at all 29903 positions  -- 0 differ []
[PASS] in5 Options table: `-a` = `-aa` for a single-contig reference (29903 rows either way); without -a/-aa the zero-depth positions vanish  -- -a 29903, none 29826, zero-depth 77
[PASS] in5 ONT row `-q 30 -Q 0 -B -d 0` depth == independent count of MAPQ>=30 reads at every position  -- positions with data 29826
[PASS] in5 RNA-seq row: '>' / '<' present (Skill table)
40 positions with the most ref-skips: allele_counts vs mpileup -B parse; mismatches: []
[PASS] in5 allele_counts at the 40 real intron positions with most ref-skips == mpileup -B -q20 -Q20 parse; 'DEL' equals real '*' only (was DEL=54 at chr22:25548 pre-fix)
top ref-skip position 25548 3 45 | allele_counts {'G': 5}
[PASS] in5 DEL counts summed over 1/20 of all RNA-seq positions: allele_counts == mpileup '*' total  -- 0 vs 0
[PASS] in5 1000G germline row: rows and ref column == FASTA  -- 98421 rows
[PASS] in5 1000G: all-filters-off depth == independent pysam count at every position
[PASS] in5 Options table: default --ff drops pre-flagged duplicates (Skill: 'Pre-flagged duplicates vanish from depth'): sum depth --ff 0 > default  -- 948889 -> 959299
[PASS] in5 Common Errors row 1: reference lacks the contig -> '[E::faidx_adjust_position] The sequence "MN908947.3" was not found', EXIT STATUS 0, rows with reference N  -- rc=0 rows=11 err='[mpileup] 1 samples in 1 input files\n[E::faidx_adjust_position] The sequence "MN908947.3" was not fo'
[PASS] in5 Skill's contig pre-check (`samtools view -H | grep '^@SQ'` vs `cut -f1 ref.fa.fai`) detects the mismatch: BAM contig MN908947.3 missing from reference  -- MN908947.3
[PASS] in5 Common Errors row 2: samtools mpileup without -f -> reference column N, rc 0; bcftools refuses
[PASS] in5 Common Errors row 4: '[E::idx_find_and_load] Could not retrieve index file for' on an unindexed BAM with -r  -- [E::idx_find_and_load] Could not retrieve index file for '/mnt/openscience/audits/bio-pileup-generation/run/work/t05/noidx.bam'
[PASS] in5 pysam pileup on unindexed BAM raises (Skill: BAM must be indexed for bam.pileup())  -- line 1342, in pysam.libcalignmentfile.AlignmentFile.pileup
[PASS] in5 Common Errors 'Empty output | Region has no reads': the check `samtools view in.bam region | head` returns nothing and mpileup prints nothing
[PASS] in5 Version Compatibility: 'The reference must be indexed' — samtools builds a missing .fai itself (advice, not a hard requirement); statement stays true for pysam.FastaFile
[PASS] in5 three BAMs -> 3 + 3*3 = 12 columns
SUMMARY in5: 28/28 assertions passed
```

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**
- [PASS] All 8 cheat-sheet rows (read from the SKILL.md table) run; no row uses -d 250; bcftools ONT variant accepted — exome row now -d 0
- [PASS] ARTIC: 29903 rows, depth (minus '*') == pysam count at every position, -a == -aa for one contig, 77 zero-depth rows vanish without -a — 0 differ
- [PASS] RNA-seq: allele_counts at the 40 positions with most ref-skips == mpileup parse; chr22:25548 gives {'G': 5} (was DEL 54) — no false DEL
- [PASS] 1000G: all-filters-off depth == pysam count; default --ff drops the 101 pre-flagged duplicates (sum 948889 vs 959299) — 
- [PASS] Reference mismatch and index errors match the fixed Common Errors table: '[E::faidx_adjust_position] ... not found' with exit 0 and N rows, contig pre-check works, no -f, '[E::idx_find_and_load] Could not retrieve index file', empty region — real message texts

### Input 6 — Variant B: NEW: re-auditor's planted-truth BAM (11 event types, soft-masked/N reference, colon contig) + 1,862-read randomized differential test of pileup_text

**Prompt:** Here is a BAM with a reverse-strand deletion, two insertions in one read, MAPQ 19/20/21 and 255 reads, base qualities 12/13/14/93, overlapping mates that disagree, N in the reference and in reads, a soft-masked reference, duplicate/supplementary/orphan flags, clips, a deletion before a ref-skip and a contig named HLA-A*01:01:01:01: give me the pileup rows, allele counts and variants.

**Executed:** true. executed; 54/56 checks pass (t06). Two real defects found: pileup_text drops the 2nd marker of adjacent I/D, find_variants reports N artifacts.

**Code that ran:** `run/01_make_new_data.py, 02_make_fuzz.py, t06_new_planted_and_fuzz.py, x_probe_exotic_other.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
[PASS] in6 E1 -B: row 110 depth 10 with '-2CC' x3 (fwd) and '-2cc' x3 (rev)  -- ['10', '.-2CC.-2CC.-2CC..,-2cc,-2cc,-2cc,,'] {'ref_fwd': 5, '-CC': 3, 'delmark': 6, 'ref_rev': 5, '-cc': 3}
[PASS] in6 E1 -B: row 111 depth 10 with '*' x6 (deleted bases stay in depth)  -- ['10', '***..***,,']
[PASS] in6 E1 --reverse-del: 3 '*' (fwd) + 3 '#' (rev); Skill's symbol table says '#' with --reverse-del on the reverse strand  -- ***..###,,
[PASS] in6 E2 -B row 420: depth 10, '+3ACG' x2, '+3acg' x2, '+1T' x2 (insertion adds no depth)  -- 10 {'ref_fwd': 8, '+ACG': 2, 'ins': 6, '+T': 2, 'ref_rev': 2, '+acg': 2}
[PASS] in6 E2 -B row 425: second insertion '+2GG' x2  -- ...+2GG.+2GG....,,
[PASS] in6 E3 -q boundary: depth 14 (all), 12 (-q19), 9 (-q20), 6 (-q21), 3 (-q22): 20 kept at -q 20, dropped at -q 21  -- {0: 14, 19: 12, 20: 9, 21: 6, 22: 3}
[PASS] in6 E3 '^' MAPQ char: MAPQ 255 and 100 are capped to '~' (3 x '^~' incl. MAPQ 93+); MAPQ 0 = '^!'  -- Counter({'4': 3, '5': 3, '6': 3, '~': 3, '!': 2})
[PASS] in6 E4 -Q boundary with -B: Q12 dropped at -Q13, Q13 kept: depth 15 (-Q0), 15 (-Q12), 12 (-Q13), 9 (-Q14), 6 (-Q15 keeps the Q93 x2 + 4 ref)  -- {0: 15, 12: 15, 13: 12, 14: 9, 15: 6}
[PASS] in6 E4 default -Q 13: Skill says 'Min base quality default 13': omitting -Q equals -Q 13 (depth 12 with -B), Q93 prints '~'  -- 12 quals=...///~~IIII
[PASS] in6 E5 overlap: depth 6 default (12 pairs' bases -> 6 counted once), 12 with -x; 3 alt 'A' remain  -- default 6 A...aa | -x 12
[PASS] in6 E6 reference N: col3 'N', read bases print as mismatches 'AAAAAAaaa' (depth 9)  -- ['N', '9', 'AAAAAAaaa']
[PASS] in6 E6 read-base N: default -Q 13 drops the two Q2 'N' bases (depth 7), -Q 0 keeps them (depth 9); Q40 N stays as 'N'  -- ['7', '...N,,,'] vs ['9', '...NNN,,,']
[PASS] in6 E7 soft-masked (lowercase) reference: mpileup col3 is printed lowercase 'g' (as in the FASTA)  -- ['g', '8', 'AA..a,,,']
[PASS] in6 E8 flags: default 10 (supplementary 2048 and proper-flag reads kept, DUP/orphans dropped), -A 14, --ff 0 12, both 16  -- {'default': 10, 'A': 14, 'ff0': 12, 'ff0_A': 16}
[PASS] in6 E9 soft/hard clips never appear: depth 6, only '.' and ',' at 1320; at read starts (1301/1301) no clipped letters  -- ['6', '...,,,']
[PASS] in6 E10 at 1420: 3 '>' (fwd reads inside the 50 bp N skip) + 3 ',' (rev reads M10) = depth 6  -- >>>,,,
[PASS] in6 E10 deletion 1411-1412: depth 6 with '*' x6 (fwd 10M2D5M50N10M and rev 10M2I2D10M)  -- ******
E10 row 1410 (fwd -2 deletion, rev +2 insertion then D): ['6', '.-2AT.-2AT.-2AT,+2ca-2at,+2ca-2at,+2ca-2at']
[PASS] in6 E11 colon-named contig 'HLA-A*01:01:01:01': `samtools mpileup -r 'HLA-A*01:01:01:01:120-120'` works (last colon splits the region) and the brace form gives the same row  -- plain=['HLA-A*01:01:01:01', '120', 'G', '10', 'AA...aa,,,'] brace depth=10
[PASS] in6 C allele_counts on colon-named contig (pysam takes the name verbatim): {G:6, A:4}  -- {'A': 4, 'G': 6}
[PASS] in6 C allele_counts at the soft-masked site nA:920 == {G:5, A:3} (case-insensitive counting)  -- {'A': 3, 'G': 5}
[PASS] in6 C allele_counts min_base_quality boundary matches -Q: 12 keeps Q12 (T? alt 11 + ref 4), 13 drops Q12 (alt 8 + ref 4), 14 drops Q13  -- ({'C': 11, 'T': 4}, {'C': 8, 'T': 4}, {'C': 5, 'T': 4})
[PASS] in6 C allele_counts(min_mapping_quality=20) at nA:510 counts 9 reads (MAPQ 20 kept, 19 dropped)  -- {'G': 9}
[PASS] in6 C find_variants on the soft-masked block reports exactly the planted nA:920 G>A 3/8 (ref reported upper-case)  -- [{'chrom': 'nA', 'pos': 920, 'ref': 'G', 'alt': 'A', 'depth': 8, 'alt_count': 3, 'freq': 0.375}]
  with min_base_quality=0 (overlap removal defeated: Skill table warns '-Q 0 with default overlap detection has subtle behavior'): [(730, 9, 12), (790, 3, 9), (800, 9, 9)]
find_variants E5 window: [(730, 'G', 'A', 3, 6), (790, 'G', 'N', 1, 7), (800, 'N', 'A', 9, 9)]
[PASS] in6 C find_variants E5 overlap site nA:730: alt 3 of depth 6 (overlap removal, same as mpileup)  -- [(730, 3, 6), (790, 1, 7), (800, 9, 9)]
[FAIL] in6 C find_variants reports only real SNVs: no site where the reference is N (nA:800-805) and no read-base 'N' allele (nA:790) is called a variant  -- artifacts reported: [(790, 'G', 'N', 1, 7), (800, 'N', 'A', 9, 9)] (planted truth: only nA:730 G>A)
[PASS] in6 C SNV-only scope: find_variants reports nothing at the planted insertions nA:420/425 (docstring says indels are not reported)
[PASS] in6 C examples/allele_counts.py on the colon contig: G 6 (60%) / A 4 (40%), depth 10, rc 0  -- Position: HLA-A*01:01:01:01:120 | Total depth: 10 | Allele counts: |   G: 6 (60.0%) |   A: 4 (40.0%) | 
[PASS] in6 C examples/allele_counts.py with thousands separator nA:1,420: ref-skip reads not counted (3 fwd '>' skipped): depth 3 (rev reads)  -- Position: nA:1420 | Total depth: 3 | Allele counts: |   G: 3 (100.0%) | 
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup 'default': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-B': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-q 20 -Q 20': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-Q 0': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-x': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-A': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '--ff 0': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '--rf 16': row-for-row  -- rows=4480 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-E': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-C 50': row-for-row  -- rows=4476 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-d 15': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-B -Q0 -q0 -x -A --ff 0': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B fuzz-clean pileup_text == samtools mpileup '-q 1 -Q 13 -B -x': row-for-row  -- rows=4486 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup 'default': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-B': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-q 20 -Q 20': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-Q 0': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-x': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-A': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '--ff 0': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '--rf 16': row-for-row  -- rows=365 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-E': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-C 50': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-d 15': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-B -Q0 -q0 -x -A --ff 0': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[PASS] in6 B planted new.bam (minus row nA:1410) pileup_text == samtools mpileup '-q 1 -Q 13 -B -x': row-for-row  -- rows=593 differ=0 only-mpileup=0 only-pysam=0
[FAIL] in6 B edge: read with an insertion DIRECTLY followed by a deletion (10M2I2D10M): pileup_text prints the same row as samtools mpileup  -- mpileup '.-2AT.-2AT.-2AT,+2ca-2at,+2ca-2at,+2ca-2at' vs pileup_text '.-2AT.-2AT.-2AT,+2ca,+2ca,+2ca'
  [info] fuzz-exotic default: rows=4470 differ=244 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['21', ',<<,<...,,..,*+1a,.,,.,.', ':1/W.I3I>LCGL.>.78=VB'], ['21', ',<<,<...,,..,*,.,,.,.', ':1/W.I3I>LCGL.>.78=VB'])] | classes={'indel marker only (samtools prints an indel marker after a
  [info] fuzz-exotic -B: rows=4470 differ=257 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['21', ',<<,<...,,..,*+1a,.,,.,.', ':1/W.I3I>LCGL.>.78=VF'], ['21', ',<<,<...,,..,*,.,,.,.', ':1/W.I3I>LCGL.>.78=VF'])] | classes={'indel marker only (samtools prints an indel marker after a * / 
  [info] fuzz-exotic -q 20 -Q 20: rows=4470 differ=137 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 108), ['16', '<,+2gt-2ag,.,a..,....,..', '=BMB<5DWd9\\CPE;F'], ['16', '<,+2gt,.,a..,....,..', '=BMB<5DWd9\\CPE;F'])] | classes={'indel marker only (samtools prints an indel marker after a * /
  [info] fuzz-exotic -Q 0: rows=4470 differ=299 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['31', ',.<.<,<....,,...,,*+1a,,.,..,.,.,.', ':!1!/W.I3I#>L-CG!L.>-!!!.7-8=VB'], ['31', ',.<.<,<....,,...,,*,,.,..,.,.,.', ':!1!/W.I3I#>L-CG!L.>-!!!.7-8=VB'])] | classes={'indel marker only (sa
  [info] fuzz-exotic -x: rows=4470 differ=262 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['27', ',.<.<,<...,,..,,*+1a,.,..,,.,.', ':?1:/9..3I>3CG<..>73?.78=@0'], ['27', ',.<.<,<...,,..,,*,.,..,,.,.', ':?1:/9..3I>3CG<..>73?.78=@0'])] | classes={'indel marker only (samtools prints an i
  [info] fuzz-exotic -A: rows=4470 differ=251 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['24', ',<<>>,.<...,,..,*+1a,.,,.,.', ':1/?AWB.I3I>LCGL.>.78=VB'], ['24', ',<<>>,.<...,,..,*,.,,.,.', ':1/?AWB.I3I>LCGL.>.78=VB'])] | classes={'indel marker only (samtools prints an indel marker 
  [info] fuzz-exotic --ff 0: rows=4470 differ=257 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 36), ['11', ',,*+1T,,,...,^],', 'FGIDIAB947d'], ['11', ',,*,,,...,^],', 'FGIDIAB947d'])] | classes={'indel marker only (samtools prints an indel marker after a * / next to another indel; pileup_te
  [info] fuzz-exotic --rf 16: rows=4470 differ=129 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['15', ',<<,<,,,,*+1a,,,,,', ':1/9.>3<..>378@'], ['15', ',<<,<,,,,*,,,,,', ':1/9.>3<..>378@'])] | classes={'indel marker only (samtools prints an indel marker after a * / next to another ind
  [info] fuzz-exotic -E: rows=4470 differ=244 only-mpileup=0 only-pysam=0 first=[('differ', ('fz1', 69), ['21', ',<<,<...,,..,*+1a,.,,.,.', ':1/W.I3I>LCGL.>.78=VB'], ['21', ',<<,<...,,..,*,.,,.,.', ':1/W.I3I>LCGL.>.78=VB'])] | classes={'indel marker only (samtools prints an indel marker after a * / 
... (trimmed; full log in run/log_t06.txt)
[FAIL] in6 C find_variants reports only real SNVs: no site where the reference is N (nA:800-805) and no read-base 'N' allele (nA:790) is called a variant  -- artifacts reported: [(790, 'G', 'N', 1, 7), (800, 'N', 'A', 9, 9)] (planted truth: only nA:730 G>A)
[FAIL] in6 B edge: read with an insertion DIRECTLY followed by a deletion (10M2I2D10M): pileup_text prints the same row as samtools mpileup  -- mpileup '.-2AT.-2AT.-2AT,+2ca-2at,+2ca-2at,+2ca-2at' vs pileup_text '.-2AT.-2AT.-2AT,+2ca,+2ca,+2ca'
```

**Scores:** Basic 33/40 | Specialized 49/60 | Total 82/100

**Assertions:**
- [PASS] Planted events match hand truth: -2CC/-2cc, +3ACG/+1T/+2GG, -q 20 boundary (9 of 14), -Q 13 boundary (12 of 15), '^~' cap, overlap 6 vs 12, N ref/read, lower-case reference col3, flags 10/14/12/16, clips, refskip; colon contig works in samtools and pysam — all E1-E11 checks pass
- [PASS] pileup_text == samtools mpileup row-for-row on 1,862 random reads (mixed-case reference with N, S/H/I/D/N CIGARs, MAPQ 0-255, Q2-93, overlapping mates, odd flags): 13 option combinations x 4,486 rows — 0 differing rows; also equal on the planted BAM apart from one row
- [FAIL] pileup_text prints the same row as mpileup where an insertion is directly followed by a deletion (10M2I2D10M) — mpileup '+2ca-2at', pileup_text '+2ca'; ~5% of rows differ in exotic-CIGAR fuzz, all indel-marker-only
- [FAIL] find_variants reports only real SNVs on the planted data — also reports nA:790 G>N (1/7) and the reference-N site nA:800 N>A (9/9)
- [PASS] allele_counts, find_variants and examples/allele_counts.py give exact truth on the colon-named contig and the soft-masked block (G6/A4, G5/A3, 3/8 alt, 3 of 6 at the overlap site) — min_base_quality boundary equals -Q

### Input 7 — Stress: NEW: pysam-vs-samtools parameter table re-tested on 4 real + 2 synthetic BAMs, 432,147 real pileup_text rows, stepper/BAQ/flag/BQ-tag probes, usage-guide token diff

**Prompt:** I want to replace samtools mpileup with pysam. For every option in the Skill's table, show that pysam gives identical depth and rows on my real DNA, RNA-seq, 1000G and ARTIC BAMs, and check the claims about steppers, flag filters and BAQ.

**Executed:** true. executed; 24/28 checks pass (t07). Two documented claims are false (stepper='all'+fastafile; bcftools --nu == samtools --rf).

**Code that ran:** `run/t07_new_real_matrix.py` (Skill code loaded verbatim from `run/skill/`).

**Output (trimmed; PASS/FAIL lines are the scripted checks the scores depend on):**

```text
[PASS] in7 A depth, human chr22 DNA: 12 Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position  -- 12/12 rows equal
[PASS] in7 A depth, human chr22 RNA-seq (spliced): 12 Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position  -- 12/12 rows equal
[PASS] in7 A depth, 1000G chr20: 12 Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position  -- 12/12 rows equal
[PASS] in7 A depth, ARTIC nanopore: 12 Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position  -- 12/12 rows equal
[PASS] in7 A depth, synthetic syn.bam: 12 Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position  -- 12/12 rows equal
[PASS] in7 A depth, synthetic new.bam: 12 Skill-table rows, pysam len(pileups) == samtools mpileup depth at every position  -- 12/12 rows equal
[PASS] in7 B pileup_text == samtools mpileup 'default', human chr22 DNA: row-for-row  -- rows=1157 differ=0 (1.2s)
[PASS] in7 B pileup_text == samtools mpileup '-B', human chr22 DNA: row-for-row  -- rows=1157 differ=0 (1.0s)
[PASS] in7 B pileup_text == samtools mpileup 'default', human chr22 RNA-seq (spliced): row-for-row  -- rows=36865 differ=0 (3.8s)
[PASS] in7 B pileup_text == samtools mpileup '-B', human chr22 RNA-seq (spliced): row-for-row  -- rows=36865 differ=0 (3.4s)
[PASS] in7 B pileup_text == samtools mpileup 'default', 1000G chr20: row-for-row  -- rows=98421 differ=0 (3.1s)
[PASS] in7 B pileup_text == samtools mpileup '-B', 1000G chr20: row-for-row  -- rows=98421 differ=0 (2.5s)
[PASS] in7 B pileup_text == samtools mpileup 'default', ARTIC nanopore: row-for-row  -- rows=29826 differ=0 (6.8s)
[PASS] in7 B pileup_text == samtools mpileup '-B', ARTIC nanopore: row-for-row  -- rows=29826 differ=0 (5.4s)
[PASS] in7 B pileup_text == samtools mpileup '-q 20 -Q 20 -x -A', human chr22 DNA: row-for-row  -- rows=1181 differ=0 (1.9s)
[PASS] in7 B pileup_text == samtools mpileup '--ff 0 -Q 0', 1000G chr20: row-for-row  -- rows=98428 differ=0 (3.3s)
total rows compared row-for-row on real data: 432147
depth at synA:250 (deletion reads: BAQ hides them, mpileup default 4 vs -B 8 ):
    stepper='all' (default), no fastafile -> 8
    stepper='all' + fastafile -> 4
    stepper='samtools', no fastafile -> 8
    stepper='samtools' + fastafile -> 4
    stepper='samtools' + fastafile + compute_baq=False -> 8
    stepper='all' + fastafile + compute_baq=False -> 8
    stepper='all' + fastafile + redo_baq=True -> 4
[PASS] in7 pysam stepper='samtools' + fastafile applies BAQ (== mpileup default 4) and compute_baq=False restores -B (8)  -- {"stepper='all' (default), no fastafile": 8, "stepper='all' + fastafile": 4, "stepper='samtools', no fastafile": 8, "stepper='samtools' + fastafile": 4, "stepper='samtools' + 
[FAIL] in7 SKILL claim 'stepper='all' + fastafile does not apply BAQ': depth at synA:250 with stepper='all' + fastafile equals the no-BAQ depth 8  -- stepper='all'+fastafile gives 4 (mpileup -B 8, default 4)
[PASS] in7 SKILL claim 'pysam defaults equal `-B`': stepper='all' with no fastafile equals -B  -- 8
mpileup: {'-B': 10, '-B --ff 0': 12, '-B --ff 0 -A': 16, '-B -A': 14} | pysam: {'default': 10, 'flag_filter=0': 12, 'flag_filter=0, ignore_orphans=False': 16, "stepper='nofilter'": 16}
[PASS] in7 Skill table: `--ff 0` == flag_filter=0 (12); `--ff 0 -A` == flag_filter=0 + ignore_orphans=False (16); default 10  -- ({'-B': 10, '-B --ff 0': 12, '-B --ff 0 -A': 16, '-B -A': 14}, {'default': 10, 'flag_filter=0': 12, 'flag_filter=0, ignore_orphans=False': 16, "stepper='nofilter'": 16})
[PASS] in7 Skill claim: stepper='nofilter' also drops the orphan filter so it is NOT `--ff 0` (nofilter == 16 == --ff 0 -A, != 12)  -- {'default': 10, 'flag_filter=0': 12, 'flag_filter=0, ignore_orphans=False': 16, "stepper='nofilter'": 16}
positions where samtools --rf N and pysam flag_require=N disagree (fz_clean, fz1): {16: 0, 17: 0, 3: 0, 2049: 0}
[PASS] in7 Skill table: `--rf FLAGS` == flag_require=INT holds for single-bit masks (16) AND multi-bit masks (17, 3, 2049)  -- {16: 0, 17: 0, 3: 0, 2049: 0}
nA:1120 with mask 65: samtools --rf 65 -A depth 6 | bcftools --nu 65 DP 0,6,73:2:2,0
[FAIL] in7 Options table: `--rf FLAGS` (bcftools `--nu`) 'Keep only reads with any of these flags set' — same reads kept by both tools for a multi-bit mask (65 = PAIRED+READ1)  -- samtools --rf 65 keeps 6 reads (any bit set); bcftools --nu 65 keeps 2 (skips reads with ANY bit unset = requires ALL bi
BQ-tag test: samtools default 35 -E 40 -B 40 | pysam samtools+fasta 35 redo_baq 40
[PASS] in7 BAQ table: an existing BQ tag is reused by default (5 reads with BQ='h' lose their bases: depth 35), `-E` recomputes and ignores it (40), `-B` ignores it (40)  -- (35, 40, 40)
[PASS] in7 pysam table: stepper='samtools' + fastafile reuses the BQ tag like the default (35); redo_baq=True == -E (40)  -- (35, 40)
tokens in the OLD usage-guide code blocks that no longer occur anywhere in the new SKILL.md + usage-guide.md: ['.query_name', 'count_alleles', 'min_qual']
[FAIL] in7 Dedup: every flag / function / tag used by the old usage-guide code still occurs in SKILL.md or the new guide (only the replaced count_alleles/min_qual left)  -- ['.query_name']
old prompts removed/reworded: ['Call variants using samtools mpileup and bcftools', 'Generate BCF file for efficient variant calling'] | new prompts not in old: ['Call variants using bcftools mpileup and bcftools call', 'Generate a BCF file so I can re-run variant calling without repeating the pileu
[PASS] in7 Dedup: the guide keeps its 9 example prompts (2 reworded to bcftools mpileup), Quick Start and 'What the Agent Will Do'  -- (9, 9)
[FAIL] in7 Dedup: the old 'Access Individual Reads' variant printed read name + strand; new SKILL.md keeps base+qual only (read name / strand not shown)  -- query_name in SKILL.md: False
SUMMARY in7: 24/28 assertions passed
```

**Scores:** Basic 31/40 | Specialized 46/60 | Total 77/100

**Assertions:**
- [PASS] 12 Skill-table rows: pysam len(pileups) == samtools mpileup depth at every position on human DNA, RNA-seq, 1000G, ARTIC, syn.bam and new.bam (max_depth passed explicitly) — 72/72 row x BAM comparisons equal
- [PASS] pileup_text == samtools mpileup row-for-row on 432,147 real rows (default, -B, -q20 -Q20 -x -A, --ff 0 -Q 0) — 0 differing rows
- [PASS] nofilter vs --ff 0 (16 vs 12), flag_filter=0 == --ff 0, flag_require == --rf (16/17/3/2049), existing BQ tag reused by default (35) and ignored by -E/-B (40) / redo_baq — all as documented
- [FAIL] 'stepper=all + fastafile does not apply BAQ' (pysam table and text) — BAQ IS applied: depth 4 at synA:250 (== mpileup default), 8 only with compute_baq=False
- [FAIL] Table row '--rf FLAGS (bcftools --nu)': both keep the same reads — mask 65: samtools --rf keeps 6 reads (any bit), bcftools --nu keeps 2 (all bits required)

## Notes on method

- Independent second methods: `samtools depth -a -J`, pysam record walks (`get_aligned_pairs`), a separate decoder of the mpileup base column, `bcftools mpileup` DP, hand-derived counts from the generator designs (`01_make_new_data.py`, `00_make_data.py`), and tool help text.
- `x_probe_exotic_other.py` shows the only 4 exotic-fuzz rows that were not caught by the automatic 'indel-marker-only' classification: all are indel markers adjacent to a ref-skip.
- Env traps honoured: no bare Rscript, WSL only via `.sh`/`bash -lc`, public-data never written (BAMs copied to `run/work`, deleted afterwards), no symlinks, no `__pycache__`.
- Data generated for this audit lives in `run/data/` (all synthetic: `00_make_data.py` regression data re-used unchanged from the pre-fix audit; `01_make_new_data.py` and `02_make_fuzz.py` are new).
