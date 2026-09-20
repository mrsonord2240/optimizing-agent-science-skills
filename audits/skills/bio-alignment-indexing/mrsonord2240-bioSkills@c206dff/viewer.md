> **Audit record for `bio-alignment-indexing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/alignment-indexing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-indexing

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-indexing` (SKILL.md 312 lines, usage-guide.md 190 lines, examples/fetch_regions.py 37 lines)
Category: Data Analysis | Mode: D (instructions + one shipped script) | Complexity: Moderate -> N=5
Environment: WSL `science` env `alignment-files` (samtools 1.24 / htslib 1.24, pysam 0.24.1, bedtools 2.31.1, GATK 4.6.2.0 / htsjdk 4.2.0). Real data from `audit-envs/alignment-files/public-data`; synthetic data in `run/data` (labelled). All scripts are in `run/scripts/`, logs in `run/out/`, `run/run_all.sh` reruns everything (verified from a clean state).

## Verdict

| | |
|---|---|
| Skill veto (T1-T4) | PASS |
| Static | 75 / 100 |
| Execution avg | 75.0 / 100 (5/5 inputs executed) |
| Raw final | 75 (Limited Release band) |
| Floor check | Layer 1 avg 31.0 (>=28 ok), Layer 2 avg 44.0 (>=42 ok), static 75 (>=70 ok), exec 75.0 (>=75 ok), **assertion pass rate 15/25 = 60% (<80%) fails** |
| **Final grade** | **Beta Only, score 75, deployable = false** (downgraded one tier by the assertion floor) |
| Research veto (M1-M4) | PASS |
| Open P0 | none |
| P1 | 4 (stale-CSI trap, CRAM gaps, large-genome section wrong, `-L` is not index access) |

## Skill Veto

- T1 Stability PASS: every documented command and snippet ran; the example ran on every documented region form.
- T2 Contract PASS: frontmatter has name, description, tool_type, primary_tool, license.
- T3 Determinism PASS: re-running `samtools index` gives byte-identical .bai/.csi; pysam.index gives the same bytes as samtools.
- T4 Security PASS: no eval/exec, no credentials, region parsed with int(), static shell.

Shipped-means-present: `examples/fetch_regions.py` exists; every Related Skill path exists (`alignment-files/{sam-bam-basics,alignment-sorting,alignment-filtering,bam-statistics}`, `sequence-io/read-sequences`). No missing primary file.

## Static score (25 criteria) = 75

| Category | Score | Note |
|---|---|---|
| Functional suitability | 8/12 | Completeness 3, correctness 2, appropriateness 3 |
| Reliability | 8/12 | Fault tolerance 3, error reporting 2, recoverability 3 |
| Performance/context | 6/8 | Token cost 3, efficiency 3 (SKILL.md and usage-guide.md duplicate each other) |
| Agent usability | 12/16 | 3/3/3/3 |
| Human usability | 5/8 | Discoverability 3, forgiveness 2 |
| Security | 11/12 | 4/3/4 |
| Maintainability | 8/12 | 3/3/2 |
| Agent-specific | 17/20 | 3/3/4/4/3 |

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: real 1000G BAM, BAI+CSI, regions, idxstats | 36 | 55 | 91 | 4/5 | PASS |
| 2 | Variant A: CRAM + FASTA index | 28 | 38 | 66 | 2/5 | PARTIAL |
| 3 | Edge: unsorted, missing index, colon contigs, odd regions | 30 | 42 | 72 | 3/5 | WARN |
| 4 | Variant B: wheat-scale contigs, CSI vs BAI, `-m` | 31 | 43 | 74 | 3/5 | WARN |
| 5 | Stress: stale/dual indices, `-L` vs `-M`, idxstats semantics | 30 | 42 | 72 | 3/5 | WARN |

**Execution average: 75.0 / 100. Assertion pass rate: 15/25.**

All five were executed (5/5). Not executed: the usage-guide prompt "Check X/Y ratio for sex determination" (no code shipped and the real 1000G slice only has chr20).

---

## Input 1 - Canonical (executed: yes)

**Prompt:** "I have a coordinate-sorted BAM from 1000 Genomes (HG00349, chr20 slice). Index it, pull the reads in chr20:1,440,001-1,440,500, count reads in a few windows, and sanity-check the counts with idxstats. Also make a CSI version."

**Code run** (`run/scripts/t1_canonical.py`, `t1b_snippets.py`): SKILL commands verbatim (`samtools index`, `-c`, `-@ 4`, `in.bam out.bai`, `pysam.index`, `pysam.index('-c', ...)`, `samtools view ... region`, `bam.fetch/count`, `get_index_statistics`, the idxstats awk one-liners, `is_indexed`, `examples/fetch_regions.py` from a copy). Ground truth: index-free full scan with `fetch(until_eof=True)` for 53 regions, and `bedtools bamtobed` for one window.

**Printed (excerpt):**
```
[PASS] 53 regions: full-scan truth == samtools view -c (BAI) == (CSI) == pysam fetch == pysam count == pysam CSI :: mismatches=[]
[PASS] bedtools full-scan count == samtools view -F 4 -c region :: bedtools=1209 samtools=1209
[PASS] fetch_regions.py Total == samtools view -c :: tot=['Total reads in chr20:1440001-1440500: 127'] expected=127
[PASS] pysam BAI bytes == samtools BAI bytes ; pysam CSI bytes == samtools CSI bytes ; re-run idempotent
[PASS] idxstats total (mapped+unmapped) == records in a full scan :: 9563+38 vs 9601
[PASS] SKILL cross-check: idxstats unmapped sum == view -c -f 4 -F 2304 :: 38 vs 38
[FAIL] is_indexed True for alt.bam with alt.bai (SKILL lists input.bai as a valid location) :: returned False
[PASS] 'Get Reads Covering Position' snippet == samtools depth -J -G 0 :: 1568 vs 1568
[FAIL] usage-guide mito awk on an 'MT'-named contig (true 33.33%) :: printed 'MT: 0.00%'
```
Also: `samtools index in.bam out.bai` works, but samtools then cannot find `out.bai` for region queries (rc 1, "Could not retrieve index file") - expected, and not warned about in the Skill. Overlapping multi-region arguments without `-M` return duplicates (219 vs 162 union).

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91
**Assertions (4/5):**
- [PASS] BAI/CSI created; every region count equals the index-free ground truth - 53 regions x 6 methods, 0 mismatches
- [PASS] fetch_regions.py equals samtools view (names, positions, strand)
- [PASS] idxstats totals and unmapped cross-check hold
- [FAIL] is_indexed() recognises every index location the SKILL lists - misses input.bai
- [PASS] in scope, read-only on inputs

## Input 2 - Variant A: CRAM and FASTA index (executed: yes)

**Prompt:** "Index my CRAM, get the reads in chr22:1952-4700 and the per-contig counts, and index the reference FASTA so I can pull chr22:1000-2000."

**Code run** (`t2_cram_faidx.py`, `t2b_cram_probe.py`): `samtools index x.cram`; region counts with and without `-T`; `pysam.AlignmentFile(cram,'rb')` (the SKILL pattern) with and without `reference_filename`; `get_index_statistics()` on CRAM vs `samtools idxstats`; `is_indexed`/`fetch_regions.py` on a CRAM; `samtools faidx` and `pysam.FastaFile` vs a plain-Python FASTA parse.

**Printed (excerpt):**
```
[PASS] CRAM region count with -T == BAM region count (5642) :: cram=5642 bam=5642
[PASS] 6 sub-regions: CRAM(.crai) counts == BAM(.bai) counts :: []
[FAIL] pysam.AlignmentFile(cram,'rb').count without reference_filename :: OSError: truncated file
[FAIL] pysam get_index_statistics(CRAM) == samtools idxstats (5642) :: pysam=[('chr22', 0, 0)] samtools=['chr22 40001 5642 0', '* 0 0 2']
[FAIL] SKILL is_indexed(s.cram) with a real .crai present :: returned False
[FAIL] fetch_regions.py on CRAM :: prints 'Indexing ...' on every call, then OSError: truncated file
[PASS] samtools faidx chr22:1000-2000 == seq[999:2000] (1001 bp) ; FastaFile.fetch(999,2000) identical
[PASS] SKILL.md FastaFile.fetch('chr22',1000,2000) is 1000 bp, NOT faidx chr22:1000-2000 (1001 bp)
```
`samtools view -c` on the CRAM without `-T` returns 5642 (counting needs no reference) while `samtools view` (records) prints none and logs "Failed to populate reference". The CRAM's `UR:` header points at an absent path here; that is ordinary for shared CRAMs and the Skill never mentions the reference requirement.

**Scores:** Basic 28/40 | Specialized 38/60 | Total 66
**Assertions (2/5):** PASS CRAM index and counts (with -T); FAIL pysam pattern retrieves without guidance; FAIL pysam idxstats on CRAM (silent 0); PASS faidx/FastaFile vs independent parse; FAIL shipped helpers on CRAM.

## Input 3 - Edge (executed: yes)

**Prompt:** "This UMI BAM won't index. Fix it, then pull the reads for chr22:1,952-4,700 and for HLA-A*01:01:01:01:1-1500. Also tell me what error I should expect if the index is missing or I ask for chromosome 22 without the 'chr'."

**Code run** (`t3_edge.py`): unsorted real UMI BAM (no @HD) -> `samtools index`, `pysam.index`; sort -> index -> idxstats; a BAM whose header lies `SO:coordinate`; synthetic `hla_contig.bam`; `fetch_regions.py` on six region spellings; missing-index and wrong-name behaviour of samtools and pysam; header-only BAM; the mito awk on an empty BAM.

**Printed (excerpt):**
```
[E::hts_idx_push] Unsorted positions on sequence #1: 3477 followed by 3470
samtools index: failed to create index for "work/t3/umi.bam"          <- no .bai written
[FAIL] stderr contains SKILL table text 'file is not sorted'
[FAIL] stderr contains usage-guide text 'file is not coordinate sorted'
[PASS] idxstats (mapped+unmapped) of sorted+indexed UMI BAM == 15788 records in the unsorted input
[PASS] samtools view -c 'HLA-A*01:01:01:01' == 3 ; brace syntax {HLA-A*01:01:01:01}:1-1500 == 2
[FAIL] shipped fetch_regions.py on a contig name containing ':' :: ValueError: too many values to unpack (expected 2)
[FAIL] example on 'chr22:1,952-4,700' (samtools: 5642) :: ValueError: invalid literal for int() with base 10: '1,952'
[FAIL] example on 'chr22' (samtools: 5642) :: ValueError: not enough values to unpack
samtools view -c 22:1-4000 -> rc 0, n=0, "specifies an invalid region or unknown reference. Continue anyway."   (Skill's 'chromosome not found' does not exist)
pysam count('22',...) -> ValueError: invalid contig `22`
missing index: "Random alignment retrieval only works for indexed SAM.gz, BAM or CRAM files" and "Could not retrieve index file" (both match the Skill, case-insensitive)
idxstats without index: warns "reverting to slow method" and still answers (Skill does not mention the fallback)
```
The header-based sort check (`grep ^@HD` -> "Should show SO:coordinate") prints nothing on this real unsorted BAM (no @HD) and passes a lying header; the index attempt itself is what reliably detects unsorted input.

**Scores:** Basic 30/40 | Specialized 42/60 | Total 72
**Assertions (3/5):** PASS unsorted -> sort -> index remedy; FAIL error strings match installed tools; PASS missing-index/wrong-contig behaviour; FAIL example accepts region forms samtools accepts; PASS scope, header-only BAM handled.

## Input 4 - Variant B: large genomes (executed: yes)

**Prompt:** "My wheat alignments have chr3B at 830 Mbp and samtools index fails. Which index do I need, and how do I set it up for a genome this size?" (Synthetic BAMs, reads at known positions.)

**Code run** (`t4_large_genome.py`): `samtools index` (BAI) on 594 Mbp / 830 Mbp contigs; `samtools index -c`; `samtools index -c -m 18`; the CSI header parsed directly (min_shift, depth); 6 chr3B region queries vs a hand-computed truth; 2.0 Gbp contig; 3 Gbp contig in SAM -> BAM.

**Printed (excerpt):**
```
[E::hts_idx_check_range] Region 540000000..540000100 cannot be stored in a bai index. Try using a csi index
samtools index: failed to create index ... Numerical result out of range           <- loud, no .bai written
default -c CSI: min_shift=14 depth=6 -> covers 2^32 = 4,294,967,296 bp per contig  <- works, counts == truth
-c -m 18 CSI: min_shift=18 depth=4 -> 2^30                                        <- SKILL says 2^(18+15)=2^33
2.0 Gbp contig: -c and -c -m 18 both find reads at 1.9e9 and 7e8
[E::bam_write1] Positional data is too large for BAM format                       <- 3 Gbp contig, read at 2.5e9
[PASS] default -c CSI: 6 chr3B queries == hand-computed truth (samtools + pysam)
[PASS] -c -m 18 works, counts == truth ; idxstats on CSI: chr1A 4, chr3B 5
```

**Scores:** Basic 31/40 | Specialized 43/60 | Total 74
**Assertions (3/5):** PASS CSI correct on >537 Mbp; FAIL "BAI silently truncates" (it fails loudly); FAIL large-genome guidance (default CSI depth, `-m 18` = 2^33, multi-Gbp in BAM); PASS pysam CSI; PASS idxstats on CSI.

## Input 5 - Stress (executed: yes)

**Prompt:** "I replaced a BAM in place and some CSI-indexed files too; make sure the indices are fresh, tell me which index wins when both exist, fetch a BED of regions quickly, batch-index a folder, and check idxstats counts (secondary/supplementary/orphans)."

**Code run** (`t5_stress.py`): stale-index scenario (BAM replaced by a half-size BAM, index not rebuilt); the SKILL's `-nt` snippet verbatim on BAI-only and CSI-only BAMs; correct-CSI/wrong-BAI and correct-BAI/wrong-CSI fixtures read by samtools, pysam and GATK PrintReads (htsjdk); the usage-guide batch loop verbatim; `-L` vs `-M -L` vs `--region-file` on a damaged-tail 1.2 M-read BAM plus timing; `-@ 0/4/8` timing; synthetic `semantics.bam` (hand-known flags); real ARTIC nanopore BAM.

**Printed (excerpt):**
```
stale .bai: [W::hts_idx_load3] The index file is older than the data file ... [E::bgzf_read_block] Invalid BGZF header ... region retrieval failed
stale .bai: idxstats silently reports OLD totals: 9563 vs true 4806
SKILL -nt snippet on stale BAI -> 'Index older than BAM; re-indexing' -> count 1095 == truth
SKILL -nt snippet on a CSI-only BAM -> false alarm, creates redundant .bai (files: csionly.bam .bai .csi)
TRAP: CSI-indexed BAM replaced, SKILL snippet run -> t.bam.bai fresh + t.bam.csi stale; region count = error (truth 1095)
precedence: correct .csi + wrong .bai -> samtools 1095, pysam 1095 (truth), GATK 0 records ("invalid uncompressedLength")
            correct .bai + wrong .csi -> samtools/pysam error, GATK 1095            <- SKILL note verified both ways
damaged-tail BAM: region arg rc0 1791 | -L bed rc1 (CRC32 mismatch) | -M -L rc0 1791 | --region-file rc0 1791 | full scan rc1
intact 1.2 M reads: -L 1.57 s vs -M -L 0.02 s (both 1791 == truth)
index time: -@0 1.61 s, -@4 1.54 s, -@8 1.58 s (43 MB BAM); BAI bytes identical
semantics.bam idxstats: chrA 10000 7 1 | * 0 0 2 ; cross-check 3 == 3 ; 'view -c -F 2304 chrA' = 5 vs -F 2308 = 4
ARTIC nanopore BAM: idxstats mapped 4916 == primary 4916 (0 supp/sec)
```

**Scores:** Basic 30/40 | Specialized 42/60 | Total 72
**Assertions (3/5):** PASS staleness snippet fixes a stale BAI; PASS precedence note (htslib .csi first, htsjdk .bai first); FAIL snippet/batch loop safe for CSI; FAIL `-L bed` uses the index; PASS idxstats semantics and cross-check.

---

## Layer averages and floors

Layer 1 avg 31.0/40 (>=28), Layer 2 avg 44.0/60 (>=42), static 75 (>=70), execution 75.0 (>=75), assertion pass 60% (**<80%, floor missed -> one tier down**).

## Research Veto (Data Analysis)

- M1 PASS: no fabricated identifiers or statistics; every count reproduced.
- M2 PASS: indexing utility; "X/Y ratio for sex determination" is a QC use with no diagnostic output (and no code).
- M3 PASS: no methodological fallacy (the large-genome mis-statements are accuracy defects, recorded as P1).
- M4 PASS: all snippets and the example run from a copy; failures are documented behaviour gaps, not syntax/import errors.

## Recommendations

**P1**
1. Staleness snippet and batch loop break for CSI-indexed BAMs (input 5): `-nt x.bam.bai` is true when no .bai exists; after re-indexing the stale .csi still wins. Test whichever index exists and delete the other kind.
2. CRAM: no reference guidance (`-T`, `reference_filename`, `REF_PATH`); pysam `get_index_statistics()` is silently 0 on CRAM (use `samtools idxstats`); helpers ignore `.crai` (input 2).
3. Large-genome section wrong in four places (input 4): BAI fails loudly, default `-c` already reaches 2^32, `-m 18` gives 2^30 not 2^33, contigs above 2^31-1 cannot be stored in BAM.
4. `-L regions.bed` shown as index access but scans the file; use `-M -L` / `--region-file` (input 5: 1.57 s vs 0.02 s; fails on a damaged tail).

**P2**
5. Common Errors strings do not match samtools 1.24 / pysam 0.24.1 output ("file is not sorted", "file is not coordinate sorted", "chromosome not found"); samtools returns rc 0 with 0 reads on an unknown contig.
6. `fetch_regions.py` rejects thousands separators, bare contigs, open-ended regions and contig names containing `:` (HLA-A*01:01:01:01) with raw tracebacks; pass the string to `fetch(region=...)`.
7. `is_indexed()` misses `input.bai` and `.crai`; sibling `.bam.bai` gives a false True for a CRAM.
8. usage-guide mito awk hard-codes `/^chrM/` (silent 0.00% on `MT`), divides by zero on an empty BAM; "X/Y ratio" prompt has no code.
9. "primary only" recipe `-F 2304 file chr` counts placed unmapped reads (use `-F 2308`); SKILL.md `FastaFile.fetch('chr1',1000,2000)` is not faidx `chr1:1000-2000`; `-@` speedup claim unsupported on a 43 MB BAM; SKILL.md and usage-guide.md duplicate each other.

## Key strengths
- Core commands correct and reproduce ground truth from three independent methods; byte-identical re-indexing.
- The .csi-vs-.bai precedence note is correct and verified for htslib and htsjdk.
- idxstats caveats and the unmapped cross-check hold on hand-built flags.
- Real pitfalls called out (contig naming, sort-before-index, stale index, BAI limit); all referenced files exist.

## Housekeeping
- No `__pycache__` or .pyc anywhere under `F:\OpenScience\external\mrsonord2240__bioSkills` or the audit folder (checked with `find`). The clone's `git status` is clean.
- `run/skill/` is a copy of the Skill; nothing was run from, or written to, the clone.
- `run/work/` and the two large synthetic files (`big.bam`, `big.positions.txt`) were deleted after the verified clean rerun to save space; `run/run_all.sh` regenerates them (seeded).
- `run/scripts/build_report.py` builds the JSON from the scored data and asserts the schema's pre-emit checklist.
