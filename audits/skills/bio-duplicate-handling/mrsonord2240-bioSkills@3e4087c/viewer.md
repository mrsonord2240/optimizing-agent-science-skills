> **Audit record for `bio-duplicate-handling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3e4087c](https://github.com/mrsonord2240/bioSkills/tree/3e4087ce9b3d9c4d89df6765e6dd4c4d8c063dc9/alignment-files/duplicate-handling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-duplicate-handling (re-audit of a fixed Skill)
Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@3e4087ce9b3d9c4d89df6765e6dd4c4d8c063dc9:alignment-files/duplicate-handling`  |  pre-fix score 77 (Limited Release) -> **87 (Production Ready ⭐)**

Category: Data Analysis | Mode: B | Complexity: Complex -> 8 inputs (6 pre-fix inputs re-run as regression, 2 new). Fixer log read but not used as evidence; every number below is from `run/in*.log`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 37 | 56 | 93 | 5/5 PASS | yes | ✅ |
| 2 | Variant A (regression) | 34 | 51 | 85 | 4/5 PASS | yes | ✅ |
| 3 | Edge (regression) | 37 | 56 | 93 | 5/5 PASS | yes | ✅ |
| 4 | Variant B (regression) | 36 | 54 | 90 | 5/5 PASS | yes | ✅ |
| 5 | Stress (regression) | 34 | 50 | 84 | 4/5 PASS | yes | ✅ |
| 6 | Scope Boundary (regression) | 35 | 53 | 88 | 4/4 PASS | yes | ✅ |
| 7 | Variant B (NEW) | 36 | 55 | 91 | 5/5 PASS | yes | ✅ |
| 8 | Adversarial (NEW) | 36 | 55 | 91 | 4/5 PASS | yes | ✅ |

**Execution Average: 89.4 / 100**  |  **Assertion Pass Rate: 36/39 (92.3%)**  |  Layer 1 avg 35.6/40, Layer 2 avg 53.8/60

**Static 83/100 (x0.4 = 33.2) + Execution 89.4 (x0.6 = 53.6) = 87 -> ⭐ Production Ready. Deployable: yes. Vetoes: none. Open P0: 0. Open P1: 0. P2: 5.**
Floors for Production Ready: static >= 80 (83), execution >= 85 (89.4), L1 >= 32 (35.6), L2 >= 48 (53.8), assertions >= 90% (92.3%): all met.

## Pre-fix defects re-tested

| Pre-fix finding | Pre-fix result | Now (input) |
|---|---|---|
| Duplex consensus after adjacency grouping (P1) | StringIndexOutOfBoundsException | Two branches; paired -> duplex 4042 reads on the real BAM, 50/50 on planted truth (5, 8) |
| umi_tools example: no sort/index, no --paired (P1) | fetch error / 2805 records | Block verbatim: 5688-5689 records, guard exits 1 on missing CB/UB (5) |
| Optimized pipeline fails from clean dir, exit 0 (P1) | 501-byte empty marked.bam, exit 0 | exit 0 valid; exit 1 without mkdir; missing/truncated input exit 1 (2) |
| Shipped example: no pipefail/-d/gate, stats in cwd (P1/P2) | failed only by accident | exit 0/1/2/3 verified, stats beside output, no partial file (4) |
| Common Errors strings / silent-under-mark pitfall (P2) | 3 wrong strings, wrong pitfall | 8/8 match tool output; pitfall corrected (3) |
| -c and @RG for Picard (P2) | absent; NPE on aligner output | -c 111/101/101 reproduced; bwa-mem2 -R + Picard exit 0 (3, 4) |
| usage-guide duplicates/contradicts SKILL.md (P2) | -d and rate contradictions | 60-line index; nothing an agent needs was lost (all deleted content found in SKILL.md, see below); rate 29.35 in both (1) |
| Workflow does not gate on assay (P2) | table only | Step 0 in SKILL.md and usage-guide; example refuses (4, 6) |
| Missing runnable blocks for named tools | not executed | biobambam2, sambamba, pbmarkdup, mapDamage --rescale, Picard UmiAware all run against planted truth (7, 8) |

**Judged leftovers.** macs3 pointer: valid (macs3 3.0.4: `--keep-dup auto` exists, and a marked and an unmarked BAM give identical results, so the mark-not-remove advice is harmless). ATAC Tn5 +4/-5: a one-line pointer to a downstream step, no code, not testable here, acceptable. '~30% faster' / biobambam2 'Fastest': unmeasured, and my 800k-read timing contradicts the first (P2).

**usage-guide dedup check.** Old sections compared with the fixed SKILL.md: workflow diagram -> 'Duplicate Marking Workflow'; step-by-step and pipeline -> same section and the optimized block; mark vs remove, -s/-f, optical -d -> 'samtools markdup' / 'Optical Distance'; rate one-liner -> 'Percentage Duplicates'; pysam mark/rate/remove -> 'pysam Python Alternative' (all three run verbatim, input 1); troubleshooting -> verbatim Common Errors; tips -> decision table, Lossy Operations, samblaster. The `-@ 8 fixes memory` tip was unsupported and is gone. The only lost item is the `mark_duplicates(threads=)` wrapper with try/finally temp cleanup, which SKILL.md replaces with the inline five-line version. Nothing the agent needs is missing.

**What the fix broke:** nothing found. Cosmetic: the SKILL.md `set -euo pipefail` line will terminate a persistent interactive shell on a later failure if an agent pastes the block into one rather than running it as a script; the umi_tools block holds two alternative commands whose combined exit status hides the scRNA guard failure when run as one script.

## Static score (83/100)

- **functional_suitability** 11/12: Completeness 4 (every tool the tables name now has a run block: biobambam2, sambamba, pbmarkdup, mapDamage --rescale, Picard UmiAware, umi_tools, fgbio single-strand and duplex), correctness 3 (all blocks reproduced; unmeasured '~30% faster' and biobambam2 'Fastest' claims, and my 800k-read timing contradicts the first), appropriateness 4.
- **reliability** 10/12: Fault tolerance 3 (pipefail + mkdir + record-count check in the block; example exits 1/2/3 and leaves no half-written output: verified for missing, truncated, empty, unwritable, unknown-assay inputs), error reporting 4 (8 of 8 Common Errors messages match tool output), recoverability 3 (the SKILL.md block still leaves a partial marked.bam; the text says to delete it).
- **performance_context** 5/8: Token cost 3 (SKILL.md 421 lines but usage-guide cut to 60 and duplicates removed), execution efficiency 2 (the 'Optimized' pipeline measured 6.4 s vs 4.6 s for the plain 5-step chain on an 800k-read BAM at 4 threads; the ~30% faster claim is unsupported).
- **agent_usability** 14/16: Learnability 3, consistency 4 (usage-guide contradictions gone, one copy of each fact), feedback design 3 (example prints stats + warnings; SKILL.md blocks assert counts), error prevention 4 (Step 0 assay gate, -c, @RG, tmpdir, --paired, MQ prerequisite all stated).
- **human_usability** 6/8: Discoverability 3 (frontmatter description still omits the assay/UMI caveats), forgiveness 3 (name-sorts first, accepts any-order input; ASSAY must be declared by the user).
- **security** 11/12: No credentials, no eval; variables quoted; example uses mktemp -d + trap and writes output by temp-then-mv; silently overwrites an existing output path.
- **maintainability** 10/12: Modularity 4 (usage-guide is now an index into SKILL.md), modifiability 3 (large single SKILL.md), testability 3 (verifiable counts, one runnable example, no shipped test data).
- **agent_specific** 16/20: Trigger 3, progressive disclosure 3 (421 lines, no references/), composability 4 (Related Skills exist), idempotency 3 (example overwrites; umi_tools output varies by 1 record run to run without --random-seed), escape hatches 3 (assay gate refuses eight assay names; a mis-declared RNA-seq BAM under ASSAY=wgs passes with no warning at 38% flagged).

## Detailed Outputs

### Input 1 — Canonical: Workflow steps, stats, -r, pysam blocks vs planted truth and 4 independent tools
**Prompt:** I have paired-end Illumina alignments (coordinate sorted). Mark the PCR duplicates with the standard fixmate/markdup workflow, index the result, tell me how many reads were flagged and the duplicate rate. Then do the same in Python with pysam and filter the duplicates out.

**Executed:** true. Scripts: `in01_canonical.sh`; logs: `in01.log`.

**What ran and what it printed:**

```
planted_dups.bam: flagged 100 of 500, flagstat '100 + 0 duplicates', pct block 20.00, -s stats DUPLICATE TOTAL 100, -r -> 400 records (=500-100). Picard READ_PAIR_DUPLICATES 50, flagged 100; sambamba 100; samblaster 100.
test.paired_end.sorted.bam: flagged 1656 of 5644, pct block 29.35 (primary-only, same as pysam rate 29.35%), -r -> 3988, Picard/sambamba/samblaster 1656, samtools vs Picard flagged (name,flag) set difference 0 lines. pysam full pipeline flagged 100/1656 and wrote marked.bam.bai; pysam filter 400/3988 = samtools -F 1024; pysam.markdup without ms raises SamtoolsError 'no ms score tag'.
```
**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100 | SKILL.md 'Duplicate Marking Workflow', 'Percentage Duplicates', '-s', '-r' and all three pysam blocks extracted verbatim and run: planted 100/100, real human BAM 1656; Picard, sambamba, samblaster agree

**Assertions:**
- [PASS] SKILL.md workflow steps 1-5 (extracted verbatim) flag exactly the planted 100 reads and index the output — view -c -f 1024 = 100; flagstat '100 + 0 duplicates'; marked.bam.bai written; -s stats DUPLICATE TOTAL 100
- [PASS] Independent tools agree: Picard 50 pairs (=100 reads), sambamba 100, samblaster 100; on the real BAM samtools and Picard flag the identical (name,flag) set — 1656 for all four on the human BAM; set difference 0. On planted, ties are broken differently but counts are equal
- [PASS] -r returns total minus flagged; -c/-F counting blocks agree — 500->400 and 5644->3988; 1656 dup / 3988 non-dup
- [PASS] 'Percentage Duplicates' block agrees with the pysam rate (same primary-only denominator) — 29.35 vs pysam 29.35%; 20.00 on planted; the usage-guide/SKILL.md denominator contradiction is gone
- [PASS] Every pysam block runs verbatim and matches samtools; tool errors surface as exceptions — flagged 100/1656, filter 400/3988, SamtoolsError text includes the samtools message

### Input 2 — Variant A: Rewritten 'Pipeline Version (Optimized)' from a clean dir: valid exit 0, failure exit non-zero; optical vs Picard; speed claim
**Prompt:** This is a NovaSeq 6000 WGS run. Give me the fast piped duplicate-marking command with 4 threads, optical duplicates at the right distance, per-read-group handling and a stats file, then tell me how many duplicates are optical vs PCR.

**Executed:** true. Scripts: `in02_pipeline_optical.sh; in09_timing_claim.sh`; logs: `in02.log; in09.log`.

**What ran and what it printed:**

```
Block extracted verbatim (set -euo pipefail; mkdir -p tmpdir; collate|fixmate|sort|markdup; index; count test). Clean dir: planted exit=0 500/500 records, flagged 100, index present, stats EXAMINED 500 / DUPLICATE TOTAL 100 (ALL + 1 READ GROUP block); human exit=0 5644/5644, 1656.
Without the mkdir line: exit=1, 'samtools collate: Cannot open intermediate file "tmpdir/collate.0000.bam"' (was exit 0 pre-fix). Without pipefail AND mkdir the closing count test still returns exit 1 (the record-count check is a second guard). Missing input exit 1; truncated BAM exit 1 ('EOF marker is absent').
Optical (SYNTHETIC, truth 4 dup pairs): samtools optical pairs 0/1/2 at -d 0/100/2500 = Picard optical pairs 0/1/2; dt:Z:SQ/LB tags only when -d is set (4 SQ + 4 LB at 2500); the SKILL.md grep block prints the same counts.
Timing (in09, 800k reads, 4 threads, 3 reps): optimized 6.29/6.56/6.47 s vs 5-step 4.59/4.64/4.67 s, both flag 120610.
```
**Scores:** Basic 34/40 | Specialized 51/60 | Total 85/100 | Pre-fix P1 fixed: block from a clean dir now exits 0 with 100/1656, and without its mkdir line exits 1; failure modes exit non-zero. Only the unmeasured '~30% faster' claim fails (measured slower)

**Assertions:**
- [PASS] The verbatim optimized pipeline runs from a clean working directory and flags the truth counts — exit 0; 100 planted, 1656 human; 500/500 and 5644/5644 records; index written
- [PASS] Every failure mode of the block exits non-zero (missing tmpdir, missing input, truncated input) — exit 1 in all three; pre-fix defect (exit 0 with an empty 501-byte marked.bam) is gone
- [PASS] Optical claims hold: -d 0 emits no dt tag, -d emits dt:Z:SQ/LB, counts match Picard — samtools optical pairs 0/1/2 vs Picard 0/1/2 at -d 0/100/2500 on synthetic truth
- [PASS] -f stats file and --use-read-groups are accepted and do not change the flagged count — flags in 1.24 help; 100 flagged; stats file has ALL + READ GROUP blocks
- [FAIL] The claim 'This is ~30% faster than sort -n | fixmate | sort | markdup' holds — Not reproduced: optimized 6.4 s vs 5-step 4.6 s on 800k reads (equal flagged counts). Scale caveat (30x WGS is ~1e9 reads) but the claim is unmeasured and contradicted here

### Input 3 — Edge: Verbatim Common Errors table (8 rows), Critical pitfall, fixmate -r, -c on a pre-marked BAM
**Prompt:** samtools markdup errors out or marks nothing on my BAM and I'm not sure of the sort order I used. What is wrong, how do I fix it, and can I drop secondary/unmapped reads with fixmate on the way? My BAM was already marked once.

**Executed:** true. Scripts: `in03_errors_edge.sh; in03b_sort_T.sh; 03_strip_tags.py`; logs: `in03.log; in03b.log`.

**What ran and what it printed:**

```
Table messages extracted from SKILL.md by regex and grep -F'd against real stderr: row1 fixmate on coord-sorted 'Coordinate sorted, require grouped/sorted by queryname' MATCH (exit 1, 28-byte partial output left); row2 markdup after fixmate without -m 'no ms score tag' MATCH; row3 MC stripped via pysam 'no MC tag' MATCH; row4 markdup on name-sorted 'queryname sorted, must be sorted by coordinate' MATCH; row5 collate 'Cannot open intermediate file "tmpdir/collate.0000.bam"' MATCH; sort -m 1M -T nodir/sort fails 'failed to create "nodir/sort.0000.bam"' (the table's sort -T claim holds when sort spills); row8 Picard on RG-less BAM: 'java.lang.NullPointerException: Cannot invoke "...SAMReadGroupRecord.getReadGroupId()"' MATCH; samtools addreplacerg then Picard: exit 0, 1656 flagged.
Critical pitfall (ms stripped): exit 1 with error, not silent (text now says so). fixmate -r -m: 5644 -> 5640, 0 secondary/unmapped left.
-c: 1000G slice pre-flagged 101; re-mark without -c 111, with -c 101, Picard 101.
```
**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100 | Pre-fix P2 fixed: 8 of 8 table messages match tool output (6 triggered here, fgbio MQ and umi_tools index in input 5); pitfall text now accurate; -c claim reproduced

**Assertions:**
- [PASS] All eight Common Errors messages match the tools' real output — 8/8: six triggered here on real data; fgbio 'Mate mapping quality (MQ) tag not present' and umi_tools 'fetch called on bamfile without index' reproduced in input 5
- [PASS] The Critical pitfall (lost ms/MC tags) is accurate: samtools 1.24 stops with an error, not a silent under-mark — ms and MC stripped: exit 1 + message, 0 flagged
- [PASS] Stated prerequisites and fixes are correct (name-sort before fixmate, -m, coordinate-sort before markdup, mkdir for tmpdir, @RG for Picard) — each violation reproduced and each stated fix verified (addreplacerg -> Picard 1656)
- [PASS] The -c paragraph is accurate (111 without -c vs 101 with -c and Picard on the pre-marked 1000G slice) — 111 / 101 / 101 reproduced exactly
- [PASS] fixmate -r -m removes secondary/unmapped as documented and 'a partial output file is left behind' is true — 5644->5640, 0 left; row1 leaves a 28-byte out file, row2 an output with 0 flagged

### Input 4 — Variant B: Rewritten shipped example: valid runs exit 0, failures non-zero, assay gate; aligner block with -R; Picard on its output
**Prompt:** Use the shipped markdup_pipeline.sh on my BAM, refuse it if it's the wrong assay, and also show me how to mark duplicates inline during alignment with bwa-mem2 and samblaster.

**Executed:** true. Scripts: `in04_example_gate_aligner.sh`; logs: `in04.log`.

**What ran and what it printed:**

```
Run from the copy: bash -n OK. ASSAY=wgs: planted exit 0, flagged 100, records 500/500, out.bam.bai and out.markdup_stats.txt written beside the output (no stray markdup_stats.txt in cwd); human exit 0, 1656, 5644/5644. OPTICAL_DIST=100 with 1 thread exit 0.
Failures: missing input exit 1, no out.bam; truncated exit 1, no out.bam; empty BAM exit 3 (record-count check), no out.bam; unwritable dir exit 1; nonexistent output dir exit 1; all leave no half-written output.
Gate: ASSAY unset exit 2; rnaseq, scrna, umi, amplicon, longread, 16s, its, bogus all exit 2, no output. SYNTHETIC amplicon BAM under ASSAY=wgs: exit 0, 1980/2000 flagged, WARNING over 50% printed. Real RNA-seq BAM under ASSAY=wgs: exit 0, 2570/8828 flagged (29%), no warning (below threshold). ARTIC nanopore under pacbio-amplicon: exit 0, 3886/4916.
Aligner block extracted verbatim (bwa-mem2 mem -R ... | samblaster | samtools sort) on 100 real + 20 SYNTHETIC clone pairs: exit 0, @RG present, 240 records, flagged 40, 40 of 40 are clones; Picard on that output exit 0, flagged 40, library lib1.
```
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100 | Pre-fix P1/P2 fixed: pipefail, temp-then-mv, stats beside output, record-count check, -d, assay gate all verified by exit codes and files; -R block gives @RG and Picard runs. Only design limit: a mis-declared RNA-seq BAM passes silently

**Assertions:**
- [PASS] Shipped example run from a copy flags the truth counts, indexes, and writes stats beside the output — 100 / 1656; index and <out>.markdup_stats.txt present; no cwd litter
- [PASS] Every failing run exits non-zero and leaves no half-written output — missing 1, truncated 1, empty 3, unwritable 1, missing dir 1; out.bam absent in all
- [PASS] Assay gate refuses: unset and eight refused or unknown assay values exit 2 without writing — exit 2 x9, no output file
- [PASS] Wrong-assay heuristic warns on an amplicon BAM declared as wgs — 1980/2000 flagged, WARNING printed, exit 0
- [PASS] bwa-mem2 -R | samblaster block flags exactly the planted clones and Picard then runs on its output — 40 of 40 flagged reads are clones; Picard exit 0 (pre-fix NullPointerException gone)

### Input 5 — Stress: UMI paired-end capture BAM: umi_tools block + guard, fgbio single-strand and duplex blocks, table rows
**Prompt:** My paired-end capture BAM has duplex UMIs in the RX tag. Deduplicate it with the UMIs and call consensus reads, duplex if possible. Also I have a 10x BAM.

**Executed:** true. Scripts: `in05_umi.sh; in05b_umi_determinism.sh`; logs: `in05.log; in05b.log`.

**What ran and what it printed:**

```
Real nf-core UMI BAM (15788 records, RX only, no CB). umi_tools on the unsorted BAM: 'ValueError: fetch called on bamfile without index'; sorted+indexed, no --paired: 2805; --paired: 5689 (the Skill quotes both).
umi_tools block extracted verbatim (scRNA form + bulk form): pre-check grep -c 'CB:Z:' prints 0; scRNA part alone exits 1 and dedup.bam has 0 records (guard works); bulk part yields dedup.bam 5688 records. Six repeat runs: 5689 5689 5688 5689 5688 5688; three with --random-seed=1: 5689 x3.
fgbio block extracted verbatim, bash -e: exit 0. mated 15788, grouped (adjacency) 15766 with 2823 MI groups, consensus 5646; grouped_duplex 15766 of 15766 records carry MI /A|/B, duplex 4042. Consensus and duplex reads: 0 mapped, all unmapped (as stated). SetMateInformation route = fixmate -m route (15766 records, 2823 MI groups). adjacency-grouped -> CallDuplexConsensusReads: StringIndexOutOfBoundsException (as the comment says). GroupReadsByUmi on queryname input without mate info: 'Mate mapping quality (MQ) tag not present on read 921195' (table row matches). --method=unique keeps 5926 vs directional 5689; samtools markdup --barcode-tag RX flags 9879 vs 11783 without.
```
**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 | Pre-fix P1s fixed: duplex branch (--strategy=paired) and umi_tools --paired/sort/index verified on the real UMI BAM; empty-output guard returns 1. Quoted 5689 varies +-1 run to run (no --random-seed)

**Assertions:**
- [PASS] umi_tools sorted+indexed requirement and --paired figures (2805 without vs 5689 with) reproduce — 'fetch called on bamfile without index' on unsorted; 2805 and 5689 on the sorted BAM
- [PASS] The empty-output guard on the scRNA form returns non-zero when CB/UB are absent — grep -c prints 0; test returns 1; dedup.bam 0 records
- [PASS] fgbio single-strand and duplex branches run verbatim; consensus reads are unmapped; MI /A /B on every duplex-grouped read — 5646 consensus, 4042 duplex, 15766/15766 with /A|/B, 0 mapped
- [PASS] SetMateInformation alternative equals the fixmate -m route, and adjacency -> duplex crashes as the comment says — 15766/2823 both routes; StringIndexOutOfBoundsException reproduced
- [FAIL] The quoted umi_tools record counts (5689 / 2805) are reproducible run to run as written — unseeded umi_tools gave 5688 in 3 of 6 runs; Skill does not mention --random-seed (seeded: 5689 x3)

### Input 6 — Scope Boundary: Assay decisions: multi-library, same-library 2 RG, amplicon panel, real RNA-seq; Step 0 gate
**Prompt:** I have a bulk RNA-seq BAM, an amplicon-panel BAM and a pooled 2-library WGS BAM. Remove the duplicates from all three.

**Executed:** true. Scripts: `in06_assay_scope.sh; 00_make_synth.py; 00b_make_synth2.py`; logs: `in06.log`.

**What ran and what it printed:**

```
SYNTHETIC multilib (2 libraries, truth 0 dups): default samtools 60 flagged, --use-read-groups 0 (SKILL.md block verbatim: 0), Picard 0. SYNTHETIC same-library 2 RG (truth 60 = 30 pairs): default 60, --use-read-groups 0, Picard 60 (RG-ID vs LB claim confirmed). SYNTHETIC amplicon (10 amplicons x 100 pairs): 1980 of 2000 flagged, -r leaves 20. Real ARTIC amplicon nanopore: 3981/4916 flagged. Real RNA-seq PE BAM: 2570/8828 flagged (Picard 2570); top 500 bp bin 6489 primary reads, 2443 flagged (38%).
Text check: SKILL.md line 112 starts the workflow Approach with 'Step 0: confirm the assay ... stop and hand off if it says NO'; usage-guide 'What the Agent Will Do' item 0 says the same.
```
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100 | Decision table and multi-library claims re-verified by output; the workflow text now has a Step 0 assay gate (pre-fix P2) which the example enforces

**Assertions:**
- [PASS] Multi-library over-marking prediction and the --use-read-groups fix are correct (SKILL.md block run verbatim) — 60 -> 0 flagged, Picard 0
- [PASS] '--use-read-groups keys on RG ID, Picard on LB' is accurate — same-library 2-RG BAM: 0 / 60 / Picard 60
- [PASS] 'Amplicon panel: markdup erases the dataset' is accurate — 1980 of 2000 flagged; -r leaves 20 records
- [PASS] The workflow now gates on assay (Step 0) in SKILL.md, usage-guide and the example — text present in both docs; example refuses eight assay values (input 4)

### Input 7 — Variant B: NEW: soft-clip/SE/reverse planted truth vs every tool block; pbmarkdup, mapDamage --rescale, Picard UmiAware blocks
**Prompt:** Mark duplicates in this mixed paired/single-end BAM with soft clips, tell me if samtools, Picard, biobambam2 and sambamba agree; also I have a PacBio HiFi amplicon BAM (pbmarkdup), an ancient-DNA BAM (mapDamage rescale) and a UMI BAM (Picard UmiAware).

**Executed:** true. Scripts: `in07_extra_tools.sh; in07b_pbmarkdup.sh; 10_make_planted2.py; mk_hifi.py; mk_damage.py; md_check.py`; logs: `in07.log; in07b.log`.

**What ran and what it printed:**

```
planted2.bam (SYNTHETIC, auditor's own: 20x3 identical pairs, 15 pairs with a 5S left clip, 15 off-by-one non-dups, 10x3 SE forward, 10x2 SE reverse with 6S at the 3' end, 100 unique pairs; truth 140 flagged reads). SKILL.md workflow 140; optimized pipeline block exit 0, 140; shipped example exit 0, 140; Picard 140; biobambam2 block 140; sambamba block 140; samblaster 140. Per family (A 80, B 30, E 30 = E1 20 + E2 10, C 0, F 0) identical for all four tools. (name,read1/2) sets identical for samtools, Picard, biobambam2 (0 differences); sambamba picks the other member of each tie (56 differences, same counts).
biobambam2 block: metrics use Picard column names except no SECONDARY_OR_SUPPLEMENTARY_RDS column.
pbmarkdup block verbatim on SYNTHETIC HiFi-style unaligned BAM (60 reads, 12 planted exact duplicates): exit 0, 60 records, 12 flagged 0x400; --rmdup 48 records; --dup-file 48 main + 12 in the dup file; FASTQ --rmdup 48 reads; summary '48 (80.0%) unique / 12 (20.0%) duplicate'.
mapDamage block verbatim (2.2.2, 3m09s, 'Successful run') on a SYNTHETIC damaged SE BAM (6000 reads, C>T at 5' p=0.35*0.6^i): mapdamage_out/marked.rescaled.bam written, 6000/6000 records; C->T at 5' pos1 (n=452) mean Q 40 -> 0 while unchanged C (n=836) stays 40 and mid-read matches stay 40; 5pCtoT_freq pos 2 = 0.2035 (planted 0.21).
Picard UmiAware block verbatim on the real UMI BAM (fixmate + coordinate sort): exit 0, 10127 flagged (samtools --barcode-tag RX 9879, plain markdup 11783).
```
**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100 | All five fixer-added blocks run verbatim and match planted truth (140/140 on planted2 for samtools workflow, pipeline block, example, Picard, biobambam2, sambamba, samblaster; pbmarkdup 12/60; mapDamage quality drop; UmiAware exit 0)

**Assertions:**
- [PASS] Every tool block (workflow, pipeline block, example, Picard, biobambam2, sambamba, samblaster) flags the planted 140 reads, soft-clip, reverse-SE and near-miss cases handled correctly — 140 each; per-family 80/30/30/0/0 identical across tools
- [PASS] The biobambam2 and sambamba blocks run verbatim on coordinate-sorted input without fixmate — both exit 0, 140 flagged
- [PASS] pbmarkdup block flags the planted duplicates in an unaligned HiFi BAM and --rmdup/--dup-file behave as the comment says — 12 flagged of 60; --rmdup 48; --dup-file 48+12
- [PASS] mapDamage --rescale block writes marked.rescaled.bam and lowers the quality of damage-consistent bases only — Q 40 -> 0 for C->T at 5' pos 1 (n=452); unchanged bases 40; 6000/6000 records
- [PASS] Picard UmiAwareMarkDuplicatesWithMateCigar block runs verbatim and is between plain markdup and exact-UMI counts — exit 0; 10127 flagged vs 11783 plain and 9879 exact-UMI

### Input 8 — Adversarial: NEW: planted duplex-UMI library (truth 80/110/50) through umi_tools, fgbio, Picard UmiAware, samtools --barcode-tag; gap hunt
**Prompt:** My capture library has duplex UMIs in RX and some molecules share coordinates. Deduplicate with the UMIs, call consensus, duplex if possible. And what if my RX only holds one UMI?

**Executed:** true. Scripts: `in08_planted_umi.sh; 20_make_planted_umi.py; in11_gap_hunt.sh`; logs: `in08.log; in11.log`.

**What ran and what it printed:**

```
SYNTHETIC planted duplex-UMI BAM (210 pairs = 420 reads: 30 duplex molecules x (3 top-strand incl. one 1-base UMI error + 2 bottom-strand) + 10 shared coordinates x 2 distinct molecules x 3 copies; UMIs 8-mers >= 3 apart). Truth: 80 strand-aware families, 110 exact-UMI families, 50 duplex molecules.
Coordinate-only: samtools markdup and Picard flag 340 reads (keep 40 pairs), truth 80: wrong tool for a UMI library, as the Skill's table says. samtools --barcode-tag RX keeps 110 pairs (exact-UMI truth 110). umi_tools bulk block verbatim: directional 80 pairs, --method=unique 110 pairs.
fgbio block verbatim: adjacency 80 MI groups, consensus 80 pairs; paired strategy 80 groups incl. /A/B = 50 base groups, duplex 50 pairs; 30 of 30 duplex molecules have /A and /B each containing one physical strand; consensus/duplex reads all unmapped. Picard UmiAware block verbatim: flagged 260 reads, keeps 80 pairs; UMI_METRICS INFERRED_UNIQUE_UMIS 80, OBSERVED 110.
Gap hunt (in11): fgbio --strategy=paired on a single-UMI RX: 'Paired strategy used but umi did not contain 2 segments delimited by a '-'' (clear, undocumented). RG-less BAM: SKILL.md pipeline block exit 0 flagged 100, example exit 0 flagged 100. -d 2500 on non-Illumina names: 24 stderr lines (10 'cannot decipher', 7 distinct names), dt tags still emitted, no optical detection (same 1656 flagged). All flags named in the Skill exist in samtools 1.24 markdup help. macs3 3.0.4 (throwaway venv): --keep-dup auto|all|<int> valid; a duplicate-marked and an unmarked BAM give identical results (899 tags at auto, 747 at 1): macs3 ignores 0x400, so the ChIP pointer 'mark, do not remove, use macs3 --keep-dup auto' is valid and harmless.
```
**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100 | Every UMI-aware path equals planted truth (80 strand-aware families, 110 exact-UMI, 50 duplex molecules). Only gap: --strategy=paired needs RX 'A-B' and the Skill does not say so (tool error is clear)

**Assertions:**
- [PASS] umi_tools bulk block gives the strand-aware truth (directional 80 pairs) and unique gives exact-UMI truth (110) — 80 / 110
- [PASS] fgbio adjacency and paired branches give truth: 80 groups -> 80 consensus pairs; 50 duplex molecules -> 50 duplex pairs; strand purity of /A and /B — 80/80, 50/50, 30 of 30 molecules
- [PASS] Picard UmiAware block keeps the 80 true UMI families and samtools --barcode-tag RX matches exact-UMI truth (110) — keeps 80; barcode-tag keeps 110
- [PASS] The Skill warns that coordinate-only markdup is wrong for a UMI library, and the numbers back it (keeps 40 pairs vs 80) — decision table + intro; samtools and Picard both flag 340 reads
- [FAIL] The Skill states the input requirement of --strategy=paired (RX must be 'A-B') — not stated; a single-UMI RX fails with a clear IllegalArgumentException, so the cost is one retry

## Research Veto
Scientific integrity PASS | Practice boundaries PASS | Methodological ground PASS | Code usability PASS (every block extracted verbatim and run; see inputs 1-8).

## Recommendations

**[P2] Unmeasured speed claims; the optimized pipeline measured slower** (inputs [2])
- Problem: '~30% faster than sort -n | fixmate | sort | markdup on typical 30x WGS' is still asserted and biobambam2 is labelled 'Fastest'. On an 800k-read BAM at 4 threads the collate/-u pipeline took 6.4 s vs 4.6 s for the plain chain (3 reps, equal flagged counts). 30x WGS scale was not tested.
- Root cause: Speed claims were carried over from prose and never benchmarked.
- Fix: Delete the percentage and the 'Fastest' label, or state the measured setup (reads, threads, disk) next to the number.

**[P2] umi_tools counts vary by 1 without --random-seed** (inputs [5])
- Problem: The Skill quotes '5689 vs 2805 records'; unseeded umi_tools dedup returned 5688 in 3 of 6 runs on the same input (5689 in all three seeded runs).
- Root cause: umi_tools picks among tied reads randomly; the bulk block has no seed.
- Fix: Add --random-seed=1 to the umi_tools blocks and say the figure is approximate without it.

**[P2] --strategy=paired input requirement not stated** (inputs [8])
- Problem: The ctDNA row and the duplex branch send the agent to GroupReadsByUmi --strategy=paired, which needs RX as 'A-B'. A single-UMI RX fails with IllegalArgumentException (clear message, one retry).
- Root cause: Duplex branch documents the MI /A /B output but not the RX format it requires.
- Fix: One sentence: 'paired needs RX as UMI1-UMI2 (as in this BAM); single-UMI libraries use adjacency + CallMolecularConsensusReads'.

**[P2] Assay gate relies on the user's declared ASSAY** (inputs [4, 6])
- Problem: The example refuses eight assay names and warns above 50% flagged, but a real RNA-seq BAM declared ASSAY=wgs exits 0 with 2570/8828 flagged and no warning (38% at the top locus).
- Root cause: The gate checks a label, not the BAM; the 50% heuristic catches amplicon panels only.
- Fix: Optionally refuse when @PG names a splice-aware aligner (STAR, HISAT2) or when many CIGARs contain N, and print the flagged percentage even below 50%.

**[P2] Frontmatter description omits the assay and UMI caveats** (inputs static)
- Problem: The description still says 'Use when preparing alignments for variant calling' with no hint that RNA-seq, amplicon, scRNA and UMI libraries need a different tool.
- Root cause: Description untouched by the fix.
- Fix: Append one clause: 'Not for RNA-seq, amplicon or UMI libraries (see the decision table)'.

## Run record
Environment and data notes: `run/README_run.md`. All scripts and logs are in `run/`; `run/skill_copy` is the Skill at 3e4087c (diff-identical to the worktree), `run/blocks.py` extracts the Skill's own fenced blocks so blocks are run verbatim.
