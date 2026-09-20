> **Audit record for `bio-sam-bam-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@35712f5](https://github.com/mrsonord2240/bioSkills/tree/35712f5f1c1177aec6e6f1fab165b8c49a832aab/alignment-files/sam-bam-basics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sam-bam-basics (RE-AUDIT of the fixed Skill)
Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@35712f5f1c1177aec6e6f1fab165b8c49a832aab:alignment-files/sam-bam-basics` (worktree `wt/af-sambam`, read-only; the Skill was copied to `run/skill/` and run from there, md5 identical to the worktree)

**Pre-fix 77 (Beta Only, not deployable) -> 85 (Production Ready), deployable, no veto, no open P0/P1.** Static 72 -> 82; execution average 80.4 -> 87.1; assertion pass 19/25 (76%) -> 36/39 (92.3%); 303 asserted checks ran, 302 passed, 1 failed (a Skill statement, see below).

## Summary table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Checks | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 35 | 54 | 89 | 5/5 PASS | 40/40 | ✅ |
| 2 | Variant A | yes | 35 | 54 | 89 | 5/5 PASS | 40/40 | ✅ |
| 3 | Edge | yes | 35 | 53 | 88 | 5/5 PASS | 48/48 | ✅ |
| 4 | Variant B | yes | 35 | 54 | 89 | 5/5 PASS | 36/36 | ✅ |
| 5 | Stress | yes | 34 | 51 | 85 | 4/5 PASS | 39/39 | ✅ |
| 6 | Stress | yes | 36 | 55 | 91 | 4/4 PASS | 23/23 | ✅ |
| 7 | Edge | yes | 33 | 50 | 83 | 4/5 PASS | 53/54 | ✅ |
| 8 | Adversarial | yes | 33 | 50 | 83 | 4/5 PASS | 23/23 | ✅ |

**Execution Average: 87.1 / 100** (Layer 1 avg 34.5/40, Layer 2 avg 52.6/60) | **Assertion Pass Rate: 36/39** | Static 82/100 | Final = 32.8 + 52.3 = **85** ⭐ Production Ready

Inputs 1-5 are the pre-fix inputs re-run as REGRESSION tests (scripts under `run/regress/`, pointed at the fixed copy; assertions that used to encode a defect were rewritten to assert the fixed behaviour). Inputs 6-8 are NEW (`run/new/`).

## Regression: the five assertions that failed before

| Pre-fix FAIL (input) | Now |
|---|---|
| 1: no safe degrade on unindexed BAM / wrong contig / multi-region duplicates | PASS: view_bam.py 5642/2 on an unindexed copy; multi-region section with -M, -M -L, --region-file, fetch_regions (Input 6: 140/140 sets equal truth) |
| 2: helper ignores reference for CRAM input, rejects .BAM, destroys its input | PASS: CRAM->BAM/SAM with 3rd arg identical to original; h5.BAM works; same path, ./path and symlink all rc 1 with the input intact |
| 3: view_bam.py crashes on empty unindexed BAM, prints None:-1 for unmapped | PASS: Mapped 0/Unmapped 0; rows `ctgA:49 + unmapped`, `* + unmapped` |
| 4: "view -c proves reference reachable"; "different reference silently corrupts" | PASS: text says view -c cannot; `view -o /dev/null && echo ok` fails with the reference gone (rc 1, no ok) and prints ok when reachable; wrong reference = MD5 mismatch rc 1, silent only with ignore_md5=1 |
| 5: four wrong failure-mode claims (markdup silent, MD needed, =/X, Bowtie2 42 rare) | PASS: markdup rc 1 + message; mpileup identical with/without MD/NM and on =/X vs M; mapDamage tables identical with MD/NM stripped; Bowtie2 42 = 97.4%, --local 44 = 94.7% |

## Fix-log claims re-verified by my own runs

| Fix-log item | My evidence |
|---|---|
| CRAM check `view -o /dev/null f.cram && echo ok` | Input 4 and 8: with the reference gone no "ok" and rc 1 ("Unable to fetch reference"); with -T, UR, REF_PATH (M5-named file), REF_CACHE, the Skill's own recipe run verbatim, or embed_ref=1: "ok" and md5 of columns 1-11 identical to the source. `view -c`, flagstat, idxstats, quickcheck pass with the reference gone (200 / 200+0 / 197 3 / rc 0); `samtools stats` and pysam iteration fail. Nuance (not a defect): a CRAM whose only records are unplaced unmapped reads decodes with no reference, so "ok" there proves decodability only. |
| view_bam.py rewrite | Input 7 matrix: SAM, sorted BAM, unsorted BAM, unindexed BAM, unmapped-only BAM (indexed/not), empty SAM/BAM, CRAM with reference / reference gone / 3rd argument: Mapped/Unmapped equals `view -c -F 4` / `-f 4` every time; missing file, text file and truncated BAM exit 1 with readable errors. Leftover: non-numeric limit traceback, cram_index_load noise on unindexed CRAM. |
| convert_formats.sh | Inputs 2, 7: SAM/BAM/CRAM legs correct; CRAM input takes the reference; .BAM ok; input==output guard (path, ./path, symlink) works. Leftover: header-only partial output when samtools fails after opening it (checked in `run/debug/d3.sh`). |
| multi-region recipes | Input 6: counts vs full-scan truth for overlapping, adjacent, nested, gap-9bp/100bp, identical, chained, reversed, single-base and far-apart sets, plus 60 + 80 random sets: -M, -M -L, --region-file, fetch_regions all equal truth; default `view r1 r2` = sum of per-region counts (duplicates). BED 0-based half-open confirmed for -L and --region-file. |
| corrected failure-mode table | Input 5: markdup (rc 1, message), MD not needed (mpileup md5 identical; mapDamage 2.2.2 tables identical), =/X identical pileup, Bowtie2 42/44 shares, wrong CRAM reference (MD5 mismatch). |
| removed claims | dedup_check: "production pipelines reject", Picard/bcftools-need-M, featureCounts-without-NH, consensus-tools-without-MD, "silently corrupts", "MD required by mpileup BAQ", "view -c proves", "Bowtie2 42 rare" all absent (9/9). |
| usage-guide dedup | dedup_check: 33/33 facts, 12/12 prompts, pointers resolve. Nothing the agent needs was lost. |

## Honesty of the unrunnable rows

DRAGEN (`--mapq-max`, default 60), Cell Ranger/STARsolo (MAPQ 255, CB:Z/UB:Z), featureCounts/RSEM as NH/HI consumers, and pbmm2 could not be run here. The fixed SKILL.md states them exactly as before with **no marker**; the honesty is only in the fix log ("Unfixed"). Recorded as P2 (label or cite). Adjacent rows I could run held: STAR MAPQ set and HI base, minimap2 ms/cs, bwa MC, fgbio RX, HISAT2 MAPQ, mapDamage.

## Findings the fix left or introduced (all P2)

- **[P2] CRAM round trip is not lossless: =/X become M, NM/MD get added** (inputs [7, 8]): SKILL.md says a CRAM round trip "keeps every field and tag but not the tag order". On a hand SAM the =/X CIGAR of one read became 9M, and on real minimap2 --eqx output 5000 of 5000 reads lost their =/X ops; on a minimap2 BAM without MD, decoding with the reference added MD:Z to all 5000 reads (unmapped-read MAPQ also becomes 0). Fix: Replace with: a CRAM round trip preserves reads and quality but rewrites =/X to M, regenerates NM/MD when the reference is available and reorders tags; use BAM if the exact CIGAR ops matter.
- **[P2] Unverifiable table rows presented as fact** (inputs [5]): DRAGEN "--mapq-max (default 60)", Cell Ranger/STARsolo "inherits STAR / 255" and CB/UB, featureCounts/RSEM as consumers of NH/HI, and the pbmm2 row are stated without any marker, although the fix log says none could be run. Fix: Append "(not verified here)" to those rows, or cite the vendor documentation for each, or drop the DRAGEN flag name.
- **[P2] Residual robustness gaps in the shipped examples** (inputs [7]): view_bam.py with a non-numeric limit dies with a raw ValueError traceback (the int() sits outside the try); on an unindexed CRAM pysam prints several [E::cram_index_load] lines on stderr although the run succeeds; convert_formats.sh leaves a header-only output file behind when samtools fails after opening it (rc 1, file present). Fix: Move int(sys.argv[2]) into the try and print a usage error; delete OUTPUT in an EXIT trap when the run fails; mention that the cram_index_load lines are harmless.
- **[P2] Small text inaccuracies and gaps** (inputs [1, 5, 6, 8]): Mode table says pysam "wc" needs reference_filename= but it writes an embedded-reference CRAM with warnings when omitted; the @PG example uses IDs bwa-mem and samtools.1 where real files have bwa and samtools; the multi-region section does not say -M needs an index; the "mapping quality distribution" command prints distinct values, not counts. Fix: Reword the wc row ("should be given"), use real @PG IDs, add "(needs an index)" to the -M line, and add `| uniq -c` to the MAPQ command.

## Static score (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Completeness 4 / Correctness 3 / Appropriateness 3. Every promised use case now has a working recipe (multi-region added); 302 of 303 asserted checks hold. Correctness loses a point for the over-general CRAM round-trip sentence and unverified aligner/assay rows; SKILL.md carries MAPQ, tag and provenance tables beyond "basics". |
| reliability | 9/12 | Fault tolerance 3 / Error reporting 3 / Recoverability 3. view_bam.py handles no index, empty, unmapped-only, SAM, CRAM (with/without reference) and exits 1 with readable messages; convert_formats.sh guards input==output and missing CRAM reference. Left: raw ValueError on a non-numeric limit, header-only partial output left behind when samtools fails, pysam's "truncated file" wording for a missing CRAM reference. |
| performance_context | 6/8 | Token cost 3 / Efficiency 3. usage-guide duplication removed (210 -> 53 lines), one copy of each fact; SKILL.md grew to 431 lines with no references/ layering. |
| agent_usability | 14/16 | Learnability 4 / Consistency 3 / Feedback design 3 / Error prevention 4. Coordinates, MAPQ portability, CRAM reference, multi-region duplicates and secondary-vs-supplementary footguns are explicit with checked commands; example @PG IDs differ from real ones, and a few rows carry no verification marker. |
| human_usability | 6/8 | Discoverability 3 / Forgiveness 3. Natural trigger wording; helper accepts any-case extensions and points at the CRAM reference; non-numeric limit still crashes. |
| security | 11/12 | Credential 4 / Input validation 3 / Data safety 4. No secrets, no eval, variables quoted; the input==output guard closes the data-loss path found in the first audit; input existence is left to samtools. |
| maintainability | 9/12 | Modularity 3 / Modifiability 3 / Testability 3. Facts live once; examples print checkable output; no shipped test data or expected outputs, and version-pinned claims (htslib 1.22 default) need re-verification when tools move. |
| agent_specific | 17/20 | Trigger precision 3 / Progressive disclosure 3 / Composability 4 / Idempotency 4 / Escape hatches 3. Related Skills all exist; conversions deterministic and refuse to overwrite their input; no explicit when-not-to-use. |
| **Subtotal** | **82/100** | pre-fix 72 |

Skill Veto: T1 stability PASS (302/303 checks, no crash), T2 contract PASS (name + description; helpers print labelled output), T3 determinism PASS (seeded data; the final suite ran twice with identical pass counts, 302/303), T4 security PASS (no eval, variables quoted, input==output guard). Research Veto (Data Analysis): M1-M4 PASS.

## Detailed outputs

### Input 1 — Canonical: Regression: inspect the real human PE BAM (header, FLAG decode, coordinates, counts, regions, view_bam.py, Rsamtools, usage-guide dedup)
**Executed:** yes. executed: 5644-record nf-core BAM read by samtools 1.24 + pysam 0.24.1 + Rsamtools 2.22.0 (r.sh); every SKILL.md/usage-guide snippet and shipped example ran from the run/skill copy.
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 | checks 40/40
**Note:** All 40 asserted checks pass (regress in1/in1b, dedup_check, misc_claims) + Rsamtools scanBam run; pre-fix defects (view_bam crash without an index, unlabelled 0-based rows, multi-region duplicates, unparseable SAM example) are gone.
**Assertions:**
- [PASS] FLAG decoding (samtools flags, 12-row table, 99/147 text, pysam is_* properties) equals an independent SAM-spec decoder; coordinate rules (POS = reference_start+1, view chr:a-b == fetch(a-1,b), faidx 1-based) hold on real reads — in1 + in1b + dedup_check + misc_claims: 40/40 pass (flagstat primary 5642 == view -c -F 2304; NM filter 5516 == pysam scan; r/rb/rc x SAM/BAM/CRAM all read 5644)
- [PASS] Shipped examples/view_bam.py works on the canonical indexed BAM and on an UNINDEXED copy, with a labelled 0-based coordinate column — indexed: Mapped 5642 Unmapped 2 (from index); unindexed: same numbers (from scan); header row "name chrom:start(0-based) strand cigar"
- [PASS] Instructions degrade safely on multi-region, wrong contig and missing index and say so — view r1 r2 = 7356 rows vs 5426 truth as documented; wrong contig warning text and exit 0 as documented; missing index message as documented
- [PASS] usage-guide dedup (210 -> 53 lines) lost nothing the agent needs — 33/33 facts of the old guide still present in SKILL.md/usage-guide.md, 12/12 advertised prompts have a command or section, 9/9 claims the fix log calls removed are absent, both usage-guide pointers resolve; only "Phred-scaled", "PL:ILLUMINA", "context manager" wording dropped (judged immaterial)
- [PASS] SAM example block and the R bullet work as written — SKILL.md SAM block extracted verbatim parses with samtools view -b and reads back as read1 chr1:100 8M; Rsamtools scanBam: 5644 records, pos 1952, flag 99, 130M13S

<details><summary>Asserted checks that ran for input 1 (from run/out/results.jsonl; 40 checks + notes)</summary>

- [PASS] view -H prints @HD/@SQ/@RG/@PG :: @HD	VN:1.6	SO:coordinate
- [PASS] view -H adds its own @PG (chain grows by one when viewing a header) :: the header printed by samtools view has an extra @PG for the view command itself; the Skill says nothing (use --no-PG)
- [PASS] --no-PG removes that extra @PG line :: 1 @PG lines
- [PASS] samtools view -c == pysam iteration count == 5644 (smoke value) :: 5644 vs 5644
- [NOTE] distinct flags among first 400 reads :: [83, 99, 147, 163]
- [PASS] samtools flags <n> agrees with independent spec decoder for every flag seen :: [83, 99, 147, 163]
- [PASS] Skill flag 99 text ("PAIRED,PROPER_PAIR,MREVERSE,READ1") equals spec decode :: PAIRED,PROPER_PAIR,MREVERSE,READ1
- [PASS] Skill flag 147 text ("PAIRED,PROPER_PAIR,REVERSE,READ2") equals spec decode :: PAIRED,PROPER_PAIR,REVERSE,READ2
- [PASS] flag 99 read: is_read1, is_proper_pair, mate_is_reverse, not is_reverse, reference_start<next_reference_start or equal :: testN:1 tlen=157
- [PASS] flag 147 read: is_read2, reverse; TLEN is negative (spec: rightmost segment negative) :: testN:5 tlen=-135
- [PASS] Skill 12-row FLAG table: each bit maps 1:1 to the pysam property named for it :: built AlignedSegment per bit
- [PASS] SAM POS (col 4) = pysam reference_start + 1 (0-based) :: 1952 vs 1951
- [PASS] CIGAR/MAPQ/flag agree between samtools text and pysam :: 130M13S 60 99
- [NOTE] Skill snippet prints read.query_qualities :: array('B', [13, 34, 34, 34, 34, 34, 34, 31, 13, 34, 34, 34, 34, 34, 31
- [PASS] Quick Reference equivalence: samtools chr:2000-3000 == fetch(chr,1999,3000) :: 2732 vs 2732
- [NOTE] fetch(chr,2000,3000) vs samtools chr:2000-3000 on this region (counts can coincide when no read ends on the boundary) :: samtools 2732, fetch(2000,3000)=2732
- [PASS] boundary read (last base at 1-based E) is in samtools chr22:E-E+1 but missing from fetch(E,E+1) when copying coordinates verbatim :: E=2094: samtools 512, fetch(E,E+1)=493, fetch(E-1,E)=512
- [NOTE] wrong contig name (22 vs chr22) samtools :: 0 / rc=0 / [main_samview] region "22:2000-3000" specifies an invalid region or unknown reference. Continue anyway.
- [NOTE] wrong contig, stdout mode :: 0 / pipe-rc=0 / [main_samview] region "22:2000-3000" specifies an invalid region or unknown reference. Continue anyway.
- [PASS] pysam fetch with wrong contig name raises ValueError :: ValueError: invalid contig `22`
- [NOTE] samtools region query on unindexed BAM: rc / message :: rc=1 stdout='' stderr="[E::idx_find_and_load] Could not retrieve index file for '/mnt/openscience/audits/bio-sam-bam-basics/run/data/noidx.b
- [PASS] usage-guide says region on missing index errors with "Could not retrieve index file" :: [E::idx_find_and_load] Could not retrieve index file for '/mnt/openscience/audits/bio-sam-bam-basics/run/data/noidx.bam' samtools view: Rand
- [PASS] pysam fetch without index raises ValueError :: ValueError: fetch called on bamfile without index
- [PASS] view_bam.py prints References: 1 / Mapped: 5642 / Unmapped: 2 (pysam index stats) :: ['References: 1', 'Mapped: 5642  Unmapped: 2  (from index)', '']
- [PASS] view_bam.py prints reference_start 0-based (SAM 1952 -> 1951) AND the header row now says so (chrom:start(0-based)) :: testN:1	chr22:1951	+	130M13S
- [NOTE] view_bam.py on an UNINDEXED BAM :: References: 1 / Mapped: 5642  Unmapped: 2  (from scan) /  / name	chrom:start(0-based)	strand	cigar / testN:1	chr22:1951	+	130M13S / testN:4	
- [PASS] view_bam.py works on unindexed BAM (bam.mapped needs an index) :: References: 1 Mapped: 5642  Unmapped: 2  (from scan)  name	chrom:start(0-based)	strand	cigar testN:1	chr22:1951	+	130M13S testN:4	chr22:1958
- [NOTE] view_bam.py on a CRAM (opens with mode rb) ::  [E::cram_decode_slice] Unable to fetch reference chr22:1952-4617 / [E::cram_next_slice] Failure to decode slice / Error reading /mnt/opensc
- [PASS] SKILL.md SAM example, extracted verbatim, parses with `samtools view -b` and reads back as read1 chr1:100 8M ACGTACGT :: rc=0 read1	0	chr1	100	60	8M	*	0	0	ACGTACGT	FFFFFFFF	NM:i:0 
- [NOTE] multi-region call, overlapping regions: duplicated records / count default / count with -M / true union :: (1930, 7356, 5426, 5426)
- [PASS] Skill multi-region section: default `view bam r1 r2` prints overlapping records twice (7356 rows vs 5426 distinct, as documented); -M gives the union :: default 7356 (dup records 1930), -M 5426, union 5426
- [PASS] pysam: summing fetch() over two overlapping regions double-counts reads (naive multi-region loop is wrong) :: naive 7356 vs union 5426
- [PASS] -L BED (0-based) with the same two regions equals the union count :: 5426 vs 5426
- [PASS] samtools faidx chr22:1-5 returns the FIRST 5 bases (1-based, closed) as the Skill states :: ACTCA vs ACTCA
- [PASS] 1-based samtools chr22:1952-1952 == 0-based fetch(1951,1952) (single base at POS 1952) :: 1 == 1, != 1
- [PASS] archived pre-fix usage-guide is the 210-line one (so the comparison is against the right file) :: (210, 53)
- [PASS] usage-guide dedup: 33 facts the OLD guide carried are each still present in the fixed SKILL.md/usage-guide.md :: 33/33 present
- [NOTE] old-guide wording that did NOT survive (judged for loss) :: ['Phred-scaled', 'PL:ILLUMINA', 'context manager']
- [PASS] every SKILL.md section named by the fixed usage-guide exists ("Version Compatibility", "Related Skills") :: (['Version Compatibility', 'Related Skills'], ['Version Compatibility', 'Related Skills'])
- [PASS] every example prompt the guide advertises has a command/section in SKILL.md :: 12/12
- [NOTE] prompt "mapping quality distribution": SKILL.md gives `sort -un | head` = distinct MAPQ values, not counts (agent must add uniq -c) :: informational
- [PASS] claims listed as removed/corrected in the fix log are absent from the fixed SKILL.md/usage-guide.md :: 9/9 gone
- [PASS] piping without -h into a BAM writer fails (no header); with -h it works and keeps records :: no -h: 'rc=1\n[E::sam_parse1] no SQ lines present in the header\nsamtools view: error reading file "-"'; with -h: ['rc=0', '195']
- [PASS] `view -c` 5644 records incl. secondary; `view -c -F 2304` 5642 == flagstat "primary" (Skill: "primary alignments only") :: (5644, 5642, 5642)
- [PASS] -@ 2 accepted and count unchanged :: 5644
- [PASS] `samtools view input.bam chr22` (whole contig) count == idxstats mapped+unmapped-placed of that contig :: (5642, ['chr22', '40001', '5642', '0'])
- [PASS] Skill tag row: `samtools view -e '[NM]<=2'` filters by edit distance (count equals a pysam scan) :: ('5516', 5516)
- [NOTE] pysam read modes x formats :: {'sam/r': (5644, False, False), 'sam/rb': (5644, False, False), 'sam/rc': (5644, False, False), 'bam/r': (5644, True, False), 'bam/rb': (564
- [PASS] Skill: reading detects SAM/BAM/CRAM, so 'r', 'rb' and 'rc' each read any of them (9 combinations, 5644 records each; is_bam/is_cram tell which) :: {('sam', 'r'): (5644, False, False), ('sam', 'rb'): (5644, False, False), ('sam', 'rc'): (5644, False, False), ('bam', 'r'): (5644, True, Fa
- [NOTE] bam.mapped/bam.unmapped by format :: {'sam': 'AttributeError: AlignmentFile.mapped only available in bam files', 'bam': (5642, 2), 'cram': (0, 0), 'bam_noidx': 'ValueError: mapp
- [PASS] Skill: `bam.mapped`/`bam.unmapped` come from the index: correct (5642, 2) for indexed BAM; unavailable ('0 or an error') for SAM, unindexed BAM and CRAM :: {'sam': 'AttributeError: AlignmentFile.mapped only available in bam files', 'bam': (5642, 2), 'cram': (0, 0), 'bam_noidx': 'ValueError: mapp
- [PASS] Skill quick-reference: `bam.count(until_eof=True)` counts an unindexed BAM (5644) :: 5644
- [NOTE] pysam 'wc' WITHOUT reference_filename :: no exception; wrote 66621 bytes
- [PASS] Skill: CRAM moves NM/MD to the end: same tag set, different order on the real BAM->CRAM (record 1) :: ('NM:i:1\tMD:Z:2T127\tMC:Z:48S95M\tAS:i:127\tXS:i:0\tRG:Z:1', 'MC:Z:48S95M\tAS:i:127\tXS:i:0\tMD:Z:2T127\tNM:i:1\tRG:Z:1')
- [NOTE] real @PG lines of the test BAM (IDs are what the tools wrote) :: ID:bwa	PN:bwa	VN:0.7.17-r1188 / ID:samtools	PN:samtools	PP:bwa

</details>

### Input 2 — Variant A: Regression: BAM<->SAM<->CRAM conversions with samtools, pysam and convert_formats.sh
**Executed:** yes. executed: real BAM/CRAM (CRAM UR path dead, REF_PATH empty, so only the 3rd argument can resolve it); 5644 records compared as SAM text with sorted tags.
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 | checks 40/40
**Note:** All 40 checks pass; the helper now passes the reference for CRAM input, accepts .BAM, refuses input==output (same path, ./path, symlink) and exits non-zero without a usable reference.
**Assertions:**
- [PASS] Every documented conversion (BAM->SAM->BAM->CRAM->BAM, pipe form) round-trips 5644 records with identical fields and tag sets — md5 of tag-sorted SAM text identical for o.bam, o.cram, o2.bam, pipe.bam; only tag ORDER differs after CRAM (5644 of 5644 tag sets identical, 2 orders identical), as SKILL.md says
- [PASS] pysam conversions (w, wb, wc + reference_filename) preserve all records and the mode table is right — p.sam/p.bam/p.cram identical to original; 'r' reads a BAM; 'rc' with reference reads CRAM
- [PASS] convert_formats.sh performs SAM->BAM, BAM->SAM, BAM->CRAM(+ref) and CRAM->BAM/SAM(+ref) correctly, including on the original nf-core CRAM whose header UR is dead — h3.bam/h3.sam identical to the original 5644 records; without the reference: rc 1, no silent success
- [PASS] Helper guards: uppercase .BAM works; input==output (same path, ./path, symlink) exits 1 and leaves the input at 5644 records; missing input and missing CRAM reference exit non-zero — rc=1, rc2=1, rc3=1 with 5644 records intact each time; h5.BAM identical to the original
- [PASS] Format statements hold: SAM > BAM > CRAM in size; header preserved; CRAM without -T warns and embeds — sizes ordered; @SQ M5/UR added at CRAM write; -C without -T exit 0 with embed_ref=2 warning

<details><summary>Asserted checks that ran for input 2 (from run/out/results.jsonl; 40 checks + notes)</summary>

- [PASS] baseline BAM has 5644 records :: 5644
- [PASS] BAM->SAM  samtools view -h -o output.sam input.bam: exit 0 and non-empty output :: rc=0 
- [PASS] SAM->BAM  samtools view -b -o output.bam input.sam: exit 0 and non-empty output :: rc=0 
- [PASS] BAM->CRAM samtools view -C -T reference.fa -o output.cram input.bam: exit 0 and non-empty output :: rc=0 
- [PASS] CRAM->BAM samtools view -b -T reference.fa -o output.bam input.cram: exit 0 and non-empty output :: rc=0 
- [PASS] Pipe      samtools view -b input.sam > output.bam: exit 0 and non-empty output :: rc=0 
- [PASS] round-trip o.bam: 5644 records with byte-identical SAM text (all fields + tags) vs original :: n=5644 md5 match=True
- [PASS] round-trip o.cram: 5644 records with byte-identical SAM text (all fields + tags) vs original :: n=5644 md5 match=True
- [PASS] round-trip o2.bam: 5644 records with byte-identical SAM text (all fields + tags) vs original :: n=5644 md5 match=True
- [PASS] round-trip pipe.bam: 5644 records with byte-identical SAM text (all fields + tags) vs original :: n=5644 md5 match=True
- [PASS] SAM step keeps all records identical :: 5644
- [PASS] CRAM round trip preserves every field, but NOT the raw text: optional-tag ORDER changes (NM/MD move to the end) :: raw md5 differs while sorted-tag md5 is identical; Skill calls nothing lossless-by-text, so informational
- [PASS] Format table: SAM > BAM > CRAM in size (CRAM "smaller than BAM", SAM larger) :: {'o.sam': 1881176, 'o.bam': 176101, 'o.cram': 66597}
- [PASS] @HD/@SQ/@RG survive BAM->SAM->BAM->CRAM->BAM (M5/UR tags may be added by CRAM) :: ['@HD\tVN:1.6\tSO:coordinate', '@SQ\tSN:chr22\tLN:40001', '@RG\tID:1\tPU:1\tSM:testN\tLB:testN\tPL:illumina'] vs ['@HD\tVN:1.6\tSO:coordinat
- [NOTE] CRAM header @SQ (M5/UR added at CRAM write) :: @SQ	SN:chr22	LN:40001	M5:1922b52e1af6977302717072ebaca0a1	UR:/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta
- [NOTE] samtools view -o x.bam (no -b): first bytes :: 1f8b0804
- [NOTE] samtools view -o x.cram (no -C): first bytes :: 4352414d
- [NOTE] samtools view -T ref -o x.cram (no -C): magic :: CRAM
- [NOTE] samtools view CRAM with unresolvable reference (no -T, REF_PATH empty), stdout lines :: 0 :: [E::fai_build3_core] Failed to open the file /sfs/7/workspace/ws/iizha01-dsl2_testdata_human-0/test-datasets/data/genomics/homo_sapiens
- [PASS] CRAM->BAM without -T and no REF_PATH fails loudly (non-zero rc) :: rc=1 [E::fai_build3_core] Failed to open the file /sfs/7/workspace/ws/iizha01-dsl2_testdata_human-0/test-datasets/data/genomics/homo_sapiens
- [NOTE] samtools view -C without -T (BAM->CRAM) and no REF_PATH :: rc=0 -rw-r--r-- 1 sci sci 66809 Sep 20 08:47 /mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/noref.cram / [W::cram_get_ref] Failed 
- [NOTE] unaligned headerless SAM -> BAM (Skill recipe) :: rc=0 
- [PASS] aligned SAM lacking @SQ -> BAM recipe fails (needs -t ref.fai); message :: rc=1 [E::sam_parse1] no SQ lines present in the header samtools view: error reading file "/mnt/openscience/audits/bio-sam-bam-basics/run/dat
- [PASS] the -t ref.fai workaround (not in the Skill) produces a 1-record BAM :: rc=0 1 
- [PASS] pysam-written p.sam: 5644 records identical to original SAM text :: n=5644
- [PASS] pysam-written p.bam: 5644 records identical to original SAM text :: n=5644
- [PASS] pysam-written p.cram: 5644 records identical to original SAM text :: n=5644
- [PASS] mode 'r' on a BAM (usage-guide says 'r' = Read SAM) :: pysam auto-detected, read 5644 records
- [NOTE] mode 'rb' on a SAM file :: read 5644 records (autodetect)
- [PASS] mode 'rc' + reference_filename reads CRAM (5644) :: 5644
- [NOTE] pysam 'rc' on CRAM with no reference at all :: OSError: truncated file
- [PASS] Skill snippet bam.header["SQ"] works on pysam 0.24 -> "chr22: 40001 bp" :: ['chr22: 40001 bp']
- [PASS] convert_formats.sh BAM->SAM ::  rc=0 out='Converted /mnt/openscience/audit-envs/alignment-files/public-data/human/test.pai' err=''
- [PASS] convert_formats.sh SAM->BAM ::  rc=0 out='Converted /mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/h.sam -> /mnt' err=''
- [PASS] convert_formats.sh BAM->CRAM with reference ::  rc=0 out='Converted /mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/h.bam -> /mnt' err=''
- [PASS] convert_formats.sh BAM->CRAM without reference arg -> clean error ::  rc=1 out='Error: CRAM conversion requires reference.fa' err=''
- [PASS] helper output h.bam identical to original records :: 5644
- [PASS] helper output h.cram identical to original records :: 5644
- [PASS] convert_formats.sh CRAM->BAM with reference arg (usage says [reference.fa]); input is the ORIGINAL nf-core CRAM whose UR is dead ::  rc=0 out='Converted /mnt/openscience/audit-envs/alignment-files/public-data/human/test.pai' err=''
- [PASS] convert_formats.sh CRAM->SAM with reference arg ::  rc=0 out='Converted /mnt/openscience/audit-envs/alignment-files/public-data/human/test.pai' err=''
- [PASS] helper CRAM-input output h3.bam identical to original 5644 records (fields + tags) :: n=5644
- [PASS] helper CRAM-input output h3.sam identical to original 5644 records (fields + tags) :: n=5644
- [PASS] helper CRAM->BAM WITHOUT reference (unresolvable) fails with non-zero rc, not exit 0 :: rc=1 /mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/h4.bam [E::fai_build3_core] Failed to open the file /sfs/7/workspace/ws/iizha0
- [PASS] convert_formats.sh uppercase extension .BAM now accepted ::  rc=0 out='Converted /mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/h.bam -> /mnt' err=''
- [PASS] uppercase .BAM output is a real BAM with the original records :: 5644
- [PASS] convert_formats.sh unknown extension -> error ::  rc=1 out='Unknown output format: txt' err=''
- [PASS] convert_formats.sh no args -> usage ::  rc=1 out='Usage: convert_formats.sh <input> <output> [reference.fa]\nExamples:\n  convert_fo' err=''
- [NOTE] helper with missing input: rc and leftover output file :: rc=1 ls: cannot access '/mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/x.bam': No such file or directory / [E::hts_open_format] Fa
- [PASS] helper with missing input exits non-zero :: rc=1 ls: cannot access '/mnt/openscience/audits/bio-sam-bam-basics/run/data/conv/x.bam': No such file or directory
- [PASS] helper refuses input == output (same path, ./ path, symlink): rc 1 each and the input keeps 5644 records :: Error: input and output are the same file; refusing to overwrite the input / rc=1 / 5644 / Error: input and output are the same file; refusi

</details>

### Input 3 — Edge: Regression: synthetic edge SAM (unmapped-with-position, secondary/supplementary, hard/soft clips, N, MAPQ 255/0, 66,000-op CIGAR, empty BAM)
**Executed:** yes. executed: synthetic (seeded) 15-record BAM built with samtools sort/index; independent CIGAR model from the SAM spec.
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100 | checks 48/48
**Note:** All 48 checks pass; view_bam.py now labels unmapped rows (placed: ctgA:49 ... unmapped; unplaced: * ... unmapped) and handles an empty unindexed BAM.
**Assertions:**
- [PASS] CIGAR semantics stated by the Skill (N not covered, S kept in SEQ, H absent, M overloaded, =/X, P) match an independent spec model and pysam — r2_spliced: 50 covered positions vs span 1050; hard clip query_length 30 vs infer_read_length 50; P consumes neither
- [PASS] Secondary vs supplementary arithmetic and flag bits hold — -F 256 = 14, -F 2304 = 13, -F 2048 = 14 on the 15-record BAM
- [PASS] Unmapped-with-position, "*" SEQ/QUAL, MAPQ 255/0, mate fields, TLEN sign, 66,000-op CIGAR and empty BAM behave as the Skill says — placed unmapped returned by region query; "* *" printed; TLEN +90/-90; pysam sees 66000 ops; empty BAM 0 records
- [PASS] Shipped view_bam.py copes with the edge inputs — empty unindexed and indexed BAM: Mapped 0 Unmapped 0; synthetic BAM: unmapped rows labelled, no None:-1; SAM input reads
- [PASS] Skill alone answers the prompt (bases consumed per op, TLEN sign, unplaced vs placed unmapped) — consumption table + TLEN sentence present and correct

<details><summary>Asserted checks that ran for input 3 (from run/out/results.jsonl; 48 checks + notes)</summary>

- [PASS] synthetic SAM -> sorted+indexed BAM; 15 records :: 15 
- [PASS] usage-guide CIGAR 50M2I30M: spec query=82, ref=80; pysam reference_length agrees :: 82,80 pysam ref_len=80
- [PASS] usage-guide CIGAR 10M2I30M5D20M: spec query=62, ref=65; pysam reference_length agrees :: 62,65 pysam ref_len=65
- [PASS] until_eof fetch returns all 15 records incl. the unplaced unmapped read :: 15
- [PASS] r1_clips_indels: pysam lengths/attributes match spec CIGAR model :: cigar=5S20M2I10M3D15M4S ref_len=48 (spec 48) qlen=56 (spec 56) infer_read_length=56 (spec incl H 56)
- [PASS] pair1: pysam lengths/attributes match spec CIGAR model :: cigar=50M ref_len=50 (spec 50) qlen=50 (spec 50) infer_read_length=50 (spec incl H 50)
- [PASS] pair1/2: pysam lengths/attributes match spec CIGAR model :: cigar=50M ref_len=50 (spec 50) qlen=50 (spec 50) infer_read_length=50 (spec incl H 50)
- [PASS] r6_secondary_noseq: pysam lengths/attributes match spec CIGAR model :: cigar=20M ref_len=20 (spec 20) qlen=0 (spec 20) infer_read_length=20 (spec incl H 20)
- [PASS] r8_mapq255: pysam lengths/attributes match spec CIGAR model :: cigar=25M ref_len=25 (spec 25) qlen=25 (spec 25) infer_read_length=25 (spec incl H 25)
- [PASS] r9_mapq0_multi: pysam lengths/attributes match spec CIGAR model :: cigar=25M ref_len=25 (spec 25) qlen=25 (spec 25) infer_read_length=25 (spec incl H 25)
- [PASS] r7_supplementary: pysam lengths/attributes match spec CIGAR model :: cigar=20M30H ref_len=20 (spec 20) qlen=20 (spec 20) infer_read_length=50 (spec incl H 50)
- [PASS] r2_spliced: pysam lengths/attributes match spec CIGAR model :: cigar=30M1000N20M ref_len=1050 (spec 1050) qlen=50 (spec 50) infer_read_length=50 (spec incl H 50)
- [PASS] r12_eqx: pysam lengths/attributes match spec CIGAR model :: cigar=10=1X9= ref_len=20 (spec 20) qlen=20 (spec 20) infer_read_length=20 (spec incl H 20)
- [PASS] r13_padding: pysam lengths/attributes match spec CIGAR model :: cigar=5M2P5M ref_len=10 (spec 10) qlen=10 (spec 10) infer_read_length=10 (spec incl H 10)
- [PASS] r15_dup_qcfail: pysam lengths/attributes match spec CIGAR model :: cigar=30M ref_len=30 (spec 30) qlen=30 (spec 30) infer_read_length=30 (spec incl H 30)
- [PASS] r3_hardclip: pysam lengths/attributes match spec CIGAR model :: cigar=10H30M10H ref_len=30 (spec 30) qlen=30 (spec 30) infer_read_length=50 (spec incl H 50)
- [PASS] r14_bigcigar: pysam lengths/attributes match spec CIGAR model :: cigar=1M1I1M1I1M1I1M1I1M1I1M1I ref_len=33000 (spec 33000) qlen=66000 (spec 66000) infer_read_length=66000 (spec incl H 66000)
- [PASS] N (intron) is NOT counted as covered: get_reference_positions has 50 entries though reference_end-start=1050 (Skill claim) :: 50 positions, span 1050
- [PASS] N jump visible in positions: 128 -> 1129 (0-based; POS 100 -> 0-based 99, 30M ends at 128) :: 128, 1129
- [PASS] hard clip: bases absent from SEQ (query_length 30) but infer_read_length 50 (Skill: "sequence not in SEQ") :: 30/50
- [PASS] soft clip bases stay in SEQ (query_length 56) while query_alignment_length 47 :: 56/47
- [PASS] reference_end for 5S20M2I10M3D15M4S at POS 10 is 57 (0-based excl); 1-based last base 57 :: (9, 57)
- [PASS] unmapped-but-placed read: is_unmapped, reference_name ctg1, reference_start 49 (POS 50 - 1), cigar None, reference_end None :: ('ctg1', 49, None, None)
- [PASS] region query returns the placed unmapped read (both samtools and pysam) :: ['r1_clips_indels', 'pair1', 'r4_unmapped_placed'] / ['r1_clips_indels', 'pair1', 'r4_unmapped_placed']
- [NOTE] -F 4 count, -f 4 count, idxstats :: 13 / 2 / ctg1	300	7	1 / ctg2	2000	5	0 / ctg3	40000	1	0 / *	0	0	1 / 
- [NOTE] view_bam.py-style stats: bam.mapped / bam.unmapped (idxstats-derived) :: 13 / 2; iteration count 15
- [PASS] bam.mapped counts records not flagged unmapped (13) and bam.unmapped 2 (placed + unplaced) :: (13, 2)
- [PASS] unplaced unmapped: reference_name None, reference_id -1, reference_start -1 :: (None, -1, -1)
- [PASS] secondary record with SEQ/QUAL "*": query_sequence None, query_qualities None (Skill snippet prints "None"), is_secondary :: (None, None)
- [PASS] samtools view prints "* *" for absent SEQ/QUAL :: * *
- [PASS] supplementary flag 2048: is_supplementary and not is_secondary; SA tag readable :: ctg2,100,+,30S20M,60,0;
- [PASS] Skill: -F 256 removes secondary only (14), -F 2304 removes both (13), -F 2048 removes supplementary (14) :: ['14', '13', '14']
- [NOTE] flags 2304/2048/1536 :: 0x900	2304	SECONDARY,SUPPLEMENTARY / 0x800	2048	SUPPLEMENTARY / 0x600	1536	QCFAIL,DUP / 
- [PASS] samtools flags matches spec for every synthetic flag (0,4,99,147,256,512+1024,2048) :: [0, 4, 99, 147, 256, 1536, 2048]
- [NOTE] view -q 30 keeps :: r1_clips_indels 60;pair1 60;pair1 60;r8_mapq255 255;r7_supplementary 30;r2_spliced 60;r12_eqx 60;r13_padding 60;r15_dup_qcfail 60;r3_hardcli
- [NOTE] -q 255 / -q 1 / -q 0 counts :: ['1', '11', '15']
- [PASS] MAPQ 255 read: mapping_quality 255; a -q 255 filter keeps exactly it :: ['1', '11', '15']
- [PASS] MAPQ 0 multimapper: mapping_quality 0 :: 0
- [PASS] pair: TLEN +90 on leftmost, -90 on rightmost; PNEXT cross-referenced; RNEXT "=" :: (90, -90, 59, 19)
- [PASS] Skill flag 99 = READ1 fwd, mate reverse; 147 = READ2 reverse: pysam is_reverse/mate_is_reverse consistent :: ok
- [PASS] TLEN equals rightmost end - leftmost start + 1 computed from CIGAR :: (109, 19)
- [PASS] =/X CIGAR 10=1X9= : cigartuples ops 7,8,7 (pysam codes) and reference_length 20 :: [(7, 10), (8, 1), (7, 9)]
- [PASS] P consumes neither: 5M2P5M -> ref len 10, query len 10 :: (10, 10)
- [PASS] 66000-op CIGAR read through sort->BAM: pysam sees 66000 ops (htslib expands the CG tag), ref_len 33000, query_len 66000 :: (66000, 33000, 66000)
- [NOTE] samtools view CIGAR text of 66000 ops (first 20 chars, then length) :: 1M1I1M1I1M1I1M1I1M1I / 132001 / 
- [PASS] region query on the 66000-op read works (reference span 1..33000) :: 1
- [PASS] flag 1536 -> is_duplicate and is_qcfail true (bits 0x400 and 0x200) :: 1536
- [PASS] SA:Z tag string structure "rname,pos,strand,CIGAR,mapQ,NM;" (Skill calls it "Comma-list of supplementary coords") :: ctg2,100,+,30S20M,60,0;
- [NOTE] samtools calmd -e on =/X read (does calmd rebuild MD/NM from = / X ops?) :: 10=1X9=	NM:i:1	MD:Z:10T9
- [PASS] calmd (no -e) rebuilds MD/NM for =/X read: NM:i:1 and MD 10 + mismatch + 9 :: 10=1X9=	NM:i:1	MD:Z:10T9
- [PASS] empty BAM: view -c 0, header 2 lines (+PG) , no records :: ['0', '4', '0']
- [PASS] empty BAM: pysam iteration yields 0 reads without error :: ok
- [PASS] view_bam.py on an empty, unindexed BAM works :: References: 1 Mapped: 0  Unmapped: 0  (from scan)  name	chrom:start(0-based)	strand	cigar rc=0 
- [PASS] view_bam.py on an empty, indexed BAM prints References: 1 / Mapped: 0 / Unmapped: 0 :: References: 1 / Mapped: 0  Unmapped: 0  (from index) /  / name	chrom:start(0-based)	strand	cigar / rc=0 / 
- [NOTE] view_bam.py rows for unmapped/hard-clip records :: r4_unmapped_placed	ctg1:49	+	unmapped // r6_secondary_noseq	ctg1:119	+	20M // r5_unmapped_unplaced	*	+	unmapped
- [PASS] view_bam.py labels unmapped records: placed one shows ctg1:49 ... unmapped, unplaced one shows * ... unmapped; no None:-1 :: ['r4_unmapped_placed\tctg1:49\t+\tunmapped', 'r5_unmapped_unplaced\t*\t+\tunmapped']
- [NOTE] view_bam.py given a SAM (opens with rb) :: References: 3 / Mapped: 13  Unmapped: 2  (from scan) /  / name	chrom:start(0-based)	strand	cigar / r1_clips_indels	ctg1:9	+	5S20M2I10M3D15M4

</details>

### Input 4 — Variant B: Regression: CRAM offline (resolution order, REF_CACHE recipe, proving a CRAM readable, archive lossless)
**Executed:** yes. executed: real human CRAM plus CRAMs written here; 1.22+ network default checked with a bogus proxy and by inspecting libhts.
**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 | checks 36/36
**Note:** All 36 checks pass; the corrected CRAM section now matches samtools 1.24: view -c does not decode, view -o /dev/null does, wrong reference is refused with MD5 mismatch.
**Assertions:**
- [PASS] Resolution order -T > REF_CACHE > REF_PATH > @SQ UR and the seq_cache_populate.pl layout hold — poisoned-cache/poisoned-path/-T/UR experiments each behave in the stated order
- [PASS] The recommended check `samtools view -o /dev/null f.cram && echo ok` fails (no "ok", rc 1) with the reference unreachable and prints ok when it is reachable; view -c / flagstat / idxstats / quickcheck pass without the reference — view -c 5644 rc 0, quickcheck rc 0, view -o /dev/null rc 1 "Unable to fetch reference"; stats fails; mid-file corruption: quickcheck rc 0 but full decode rc 1
- [PASS] A different reference is refused, not silently accepted; silent only with ignore_md5=1 — MD5 checksum reference mismatch rc 1; ignore_md5=1 rc 0 with different SEQ column
- [PASS] htslib >= 1.22 does no network lookup by default; archive preset is lossless and smallest — no ebi/ena/proxy activity; libhts holds no ebi.ac.uk/ena/cram string; archive records identical to source, smallest profile
- [PASS] view_bam.py on CRAM: indexed CRAM gives 5642/2, unreachable reference gives exit 1 with the reference hint, 3rd argument resolves it — Mapped 5642 Unmapped 2 (scan); "Error reading ...: truncated file (CRAM needs its reference: pass reference.fa as the 3rd argument)"; with 3rd arg rc 0

<details><summary>Asserted checks that ran for input 4 (from run/out/results.jsonl; 36 checks + notes)</summary>

- [PASS] @SQ has M5 (md5 of reference) and UR (path of the FASTA) written by samtools :: @SQ	SN:chr22	LN:40001	M5:1922b52e1af6977302717072ebaca0a1	UR:/mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa
- [PASS] with UR reachable: full decode of b.cram = 5644 records, rc 0 (no -T/REF_PATH/REF_CACHE: fallback #4 UR works) :: (0, 5644)
- [PASS] reference unreachable: full decode FAILS loudly (rc != 0, no records) :: (1, 0, '/mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa: No such file or directory\n[E::refs_')
- [NOTE] reference unreachable: samtools view -c b.cram :: 5644 rc=0
- [PASS] SKILL.md: "`samtools view -c file.cram` forces full decode; proves reference reachable" -> FALSE in 1.24: -c returns the count, rc 0, with NO reference :: 5644 rc=0
- [PASS] a working reachability proof: `samtools view -o /dev/null file.cram` gives rc != 0 when reference is unreachable :: rc=1/mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa: No such file or
- [PASS] Skill recipe verbatim `samtools view -o /dev/null file.cram && echo ok`: prints NO "ok" and stays non-zero when the reference is unreachable :: rc=1 /mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa: No such file or directory [E::refs_
- [PASS] Skill: flagstat / idxstats print counts on a CRAM with no reachable reference (never decode bases) :: 5644 + 0 in total (QC-passed reads + QC-failed reads) / chr22	40001	5642	0 / rc=0
- [PASS] Skill: `samtools stats` decodes bases, so it fails (non-zero) with the reference unreachable :: rc=254/mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa: No such file or
- [PASS] quickcheck -v passes (rc 0) even though the reference is unreachable ("header + EOF only") :: rc=0
- [PASS] seq_cache_populate.pl ships with samtools 1.24 and writes files named by M5 in %2s/%2s/%s layout :: ['/mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/cache/19/22/b52e1af6977302717072ebaca0a1']
- [PASS] Skill recipe REF_CACHE=<root>/%2s/%2s/%s + REF_PATH=$REF_CACHE: full decode offline = 5644 records rc 0 :: (0, 5644, '')
- [PASS] REF_PATH alone: full decode offline = 5644 records rc 0 :: (0, 5644, '')
- [PASS] REF_CACHE alone: full decode offline = 5644 records rc 0 :: (0, 5644, '')
- [NOTE] poisoned REF_CACHE + good REF_PATH :: (1, 0, '[E::cram_decode_slice] MD5 checksum reference mismatch at chr22:1952-4617\n[E::cram_decode_slice] CRAM  : 0b707159b93f476')
- [NOTE] good REF_CACHE + poisoned REF_PATH :: (0, 5644, '')
- [PASS] REF_CACHE is consulted BEFORE REF_PATH (Skill order #2 before #3): poisoned cache breaks decode; poisoned path + good cache decodes :: cache-first-poison rc=1; path-poison rc=0 n=5644
- [PASS] -T ref.fa (#1) beats a poisoned REF_CACHE/REF_PATH :: (0, 5644, '')
- [PASS] UR (#4) is last: with UR target poisoned, decode fails alone but REF_PATH (good) rescues it :: UR only rc=1; +REF_PATH rc=0 n=5644
- [NOTE] no reference, bogus proxy, full decode: output :: /mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa: No such file or directory / [E::refs_load_fai] Failed to open reference fil
- [PASS] no network lookup by default (>=1.22): no ebi/ena/curl/proxy mention when reference unresolvable :: /mnt/openscience/audits/bio-sam-bam-basics/run/data/cram/ref.fa: No such file or directory [E::refs_load_fai] Failed to open reference file 
- [PASS] libhts 1.24 binary holds no built-in ebi.ac.uk/ena/cram default (independent confirmation of the 1.22 removal claim) :: 0
- [NOTE] REF_PATH set explicitly to the ENA URL + bogus proxy: the server IS tried :: exit=124 (124 = still retrying the server when killed after 25 s)
- [PASS] Skill recipe prints "ok" and rc 0 once the reference is reachable again (UR path restored) :: ok rc=0
- [PASS] `--output-fmt-option archive` is accepted syntax :: rc=0
- [PASS] archive CRAM is lossless: 5644 records identical after tag canonicalisation (Skill: "does not alter bases or qualities") :: 5644 records, identical=True
- [PASS] archive is the smallest profile ("maximum-compression preset") :: {'fast': 78600, 'normal': 66569, 'small': 65051, 'archive': 64152}
- [NOTE] CRAM option names available (embed_ref / no_ref etc. -- Skill mentions none) :: --output-fmt-option no_ref -o out.cram in.bam / 	samtools view --output-fmt cram,seqs_per_slice=5000,no_ref \
- [PASS] embed_ref (undocumented in Skill) yields a self-contained CRAM: decodes with NO reference reachable :: rc=0
- [PASS] (i) CRAM (true ref) read with a 1-base-different reference: hard error (rc!=0, MD5 mismatch), not silent corruption :: rc=1 n=0 err='[E::cram_decode_slice] MD5 checksum reference mismatch at chr22:1952-4617\n[E::cram_decode_slice] CRAM  : 0b707'
- [PASS] (ii) BAM converted against the WRONG reference, read back with the right one: hard error, not silent :: rc=1 n=0 identical=False
- [PASS] (iii) read back with the same wrong reference: faithful (records identical) :: identical=True
- [NOTE] with --input-fmt-option ignore_md5=1 the mismatch IS silent: records identical to original? :: rc=0 n=5644 identical=False
- [PASS] silent corruption is possible only when the M5 check is switched off (ignore_md5=1): reads differ from the original :: n=5644 identical=False
- [PASS] quickcheck detects a truncated CRAM (missing EOF) with non-zero rc :: run/data/cram/trunc.cram rc=16
- [PASS] mid-file corruption: quickcheck rc 0 (header+EOF only) but a FULL decode fails :: qc rc0; full decode rc=1 n=0
- [PASS] mid-file corruption is also NOT caught by `samtools view -c` (only a full decode is) :: view -c => '5644\nrc=0' 
- [NOTE] BAM->CRAM WITHOUT -T, no reference env (help says "-C requires -T") :: rc=0 err='[W::cram_get_ref] Failed to populate reference "chr22"\n[W::cram_get_ref] See https://www.htslib.org/doc/reference_seqs.html for f
- [PASS] SKILL.md "CRAM requires a reference FASTA with -T": samtools 1.24 nonetheless exits 0 and writes a CRAM (with warnings) -> silent non-portable file :: rc=0
- [NOTE] noT.cram @SQ (no M5/UR) :: ['@SQ\tSN:chr22\tLN:40001']
- [PASS] that CRAM written without -T is readable with no reference at all (embedded/no_ref) :: (0, 5644, '')
- [PASS] pysam 'rc' + reference_filename + .crai: fetch chr22:2000-3000 gives 2732 (same as BAM) :: 2732
- [NOTE] view_bam.py on an INDEXED CRAM (mode "rb") :: References: 1 / Mapped: 5642  Unmapped: 2  (from scan) /  / name	chrom:start(0-based)	strand	cigar / testN:1	chr22:1951	+	130M13S / testN:4	
- [PASS] view_bam.py works on an indexed CRAM (prints Mapped: 5642) :: References: 1 / Mapped: 5642  Unmapped: 2  (from scan) /  / name	chrom:start(0-based)	strand	cigar / testN:1	chr22:1951	+	130M13S / testN:4	
- [PASS] view_bam.py on CRAM with unreachable reference: exit 1 with a readable error naming the reference option, no Traceback :: s.html for further suggestions [E::cram_decode_slice] Unable to fetch reference chr22:1952-4617 [E::cram_next_slice] Failure to decode slice
- [PASS] view_bam.py <cram> 2 <reference.fa> works with the UR target gone (3rd arg resolves it): Mapped 5642 Unmapped 2, rc 0 :: References: 1 Mapped: 5642  Unmapped: 2  (from scan)  name	chrom:start(0-based)	strand	cigar testN:1	chr22:1951	+	130M13S testN:4	chr22:1958

</details>

### Input 5 — Stress: Regression: six aligners on a synthetic repeat genome (MAPQ scale, -q, tags, @PG chain, fixmate/markdup, failure-mode table)
**Executed:** yes. executed: bwa 0.7.19, bwa-mem2, minimap2 (+--eqx, --cs, splice), bowtie2 (end-to-end and --local), hisat2, STAR on a seeded synthetic genome; fgbio 4.1.1 AnnotateBamWithUmis; mapDamage 2.2.2; bcftools 1.24. DRAGEN, Cell Ranger, featureCounts, RSEM, pbmm2 NOT run.
**Scores:** Basic 34/40 | Specialized 51/60 | Total 85/100 | checks 39/39
**Note:** All 39 checks pass (in5, in5c mapDamage, tags_check). Table rows for DRAGEN, Cell Ranger/STARsolo, featureCounts/RSEM and pbmm2 could not be run and are stated as fact without a marker.
**Assertions:**
- [PASS] MAPQ table rows hold: bwa/bwa-mem2/minimap2 0-60 max 60, HISAT2 {0,1,60}, Bowtie2 max 42 (97.4% of records) and max 44 with --local (94.7%), STAR {0,1,3,255} with -q 30 == -q 255 — histograms in out/in5.txt; Bowtie2 -q 60 keeps 0
- [PASS] Tag/provenance rows hold: NM/MD from bwa, MC from bwa mem, ms in minimap2 unrelated to fixmate, cs with --cs, RX from fgbio AnnotateBamWithUmis, HI 1-based, @PG names the aligner — tags_check 6/6 and in5 tag checks pass
- [PASS] The corrected failure-mode table is true: markdup refuses (rc 1, "no ms score tag. Please run samtools fixmate"), MD/NM not needed by bcftools mpileup or mapDamage, =/X gives identical mpileup — mpileup body md5 identical with/without MD/NM and on eqx vs M; mapDamage misincorporation/dnacomp/lgdistribution bodies identical with MD/NM stripped
- [PASS] @PG chain links through PP and the head -1 command names the aligner — six-line chain linear; example IDs in SKILL.md (bwa-mem, samtools.1) are illustrative, real IDs are bwa / samtools
- [FAIL] Rows that could not be run (DRAGEN --mapq-max, Cell Ranger/STARsolo MAPQ 255 and CB/UB, featureCounts/RSEM tag consumers, pbmm2) are marked as unverified in the Skill — stated as fact with no marker; the fix log admits they are unverifiable

<details><summary>Asserted checks that ran for input 5 (from run/out/results.jsonl; 39 checks + notes)</summary>

- [PASS] bwa BAM has 5000 primary records (2500 pairs) :: 5000
- [NOTE] MAPQ histogram bwa :: {0: 26, 1: 2, 4: 2, 7: 4, 10: 6, 34: 2, 37: 2, 40: 366, 42: 4, 43: 1, 45: 3, 46: 1, 50: 2, 52: 1, 53: 1, 55: 4, 58: 2, 60: 4571}
- [NOTE] MAPQ histogram bwamem2 :: {0: 29, 1: 2, 4: 2, 7: 4, 10: 6, 34: 2, 37: 2, 40: 366, 42: 4, 43: 1, 45: 3, 46: 1, 50: 2, 52: 1, 53: 1, 55: 4, 58: 2, 60: 4568}
- [NOTE] MAPQ histogram mm2 :: {0: 26, 1: 8, 2: 3, 3: 1, 5: 1, 6: 1, 10: 1, 13: 1, 16: 1, 20: 1, 21: 4, 22: 1, 26: 2, 27: 1, 28: 1, 30: 1, 32: 2, 34: 1, 37: 1, 38: 1, 40: 
- [NOTE] MAPQ histogram bt2 :: {1: 26, 6: 10, 12: 2, 17: 8, 18: 4, 21: 20, 25: 2, 30: 4, 31: 6, 32: 14, 34: 8, 35: 4, 36: 2, 40: 20, 42: 4870}
- [NOTE] MAPQ histogram hs2 :: {0: 47, 1: 1807, 60: 4452}
- [NOTE] MAPQ histogram star :: {0: 882, 1: 658, 3: 372, 255: 4444}
- [PASS] bwa: MAPQ scale 0-60 with 60 the maximum and present :: max 60 n60=4571
- [PASS] bwamem2: MAPQ scale 0-60 with 60 the maximum and present :: max 60 n60=4568
- [PASS] mm2: MAPQ scale 0-60 with 60 the maximum and present :: max 60 n60=4833
- [PASS] HISAT2: 0-60 scale, unique = 60 (values seen are within {0,1,60}) :: [0, 1, 60]
- [PASS] Bowtie2: 0-42, nothing above 42 :: max 42
- [PASS] Bowtie2 42 is the top and most common MAPQ, as the fixed Skill says (majority of records) :: MAPQ 42 = 97.4% of records; Skill text says 97% in its run: True
- [NOTE] MAPQ histogram bowtie2 --local :: {1: 26, 11: 40, 14: 32, 17: 16, 18: 20, 21: 24, 25: 2, 31: 30, 32: 28, 33: 18, 34: 28, 35: 2, 44: 4734}
- [PASS] Bowtie2 --local: MAPQ up to 44 (Skill "0-44 with --local", 44 the top and common); nothing above 44 :: max 44; 44 = 94.7%
- [PASS] Bowtie2 "-q 60 drops everything" :: [0, 4930, 4928]
- [NOTE] bowtie2 -q 23 / -q 30 retained :: [4930, 4928]
- [PASS] STAR MAPQ set is exactly {0,1,3,255} :: [0, 1, 3, 255]
- [NOTE] STAR (MAPQ, NH) pairs :: {(0, 5): 390, (0, 6): 492, (1, 3): 426, (1, 4): 232, (255, 1): 4444, (3, 2): 372}
- [PASS] STAR MAPQ = f(NH): 1 locus->255, 2->3, 3-4->1, >=5->0 (STARmanual; Skill lists 0,1,3,255) :: {(0, 5): 390, (0, 6): 492, (1, 3): 426, (1, 4): 232, (255, 1): 4444, (3, 2): 372}
- [PASS] STAR: "-q 30 accidentally keeps unique only too" and -q 255 keeps unique only (same counts); -q 60 keeps unique too :: [4444, 4444, 4444] vs n255=4444
- [PASS] bwa-family BAMs never emit 255 (so 255 there could only mean "unavailable" per SAM spec) :: ok
- [PASS] STAR HI:i is 1-based by default and 0-based with --outSAMattrIHstart 0 :: default:    4990 HI:i:1     546 HI:i:2     360 HI:i:3     218 HI:i:4     160 HI:i:5      82 HI:i:6  / ihstart0:    4990 HI:i:0     546 HI:i:
- [NOTE] tags bwa :: {'AS': 5000, 'MC': 5000, 'MD': 5000, 'MQ': 5000, 'NM': 5000, 'RG': 5000, 'XA': 468, 'XS': 5000}
- [NOTE] tags bwamem2 :: {'AS': 5000, 'MC': 5000, 'MD': 5000, 'NM': 5000, 'XA': 471, 'XS': 5000}
- [NOTE] tags mm2 :: {'AS': 5000, 'NM': 5000, 'cm': 5000, 'de': 5000, 'ms': 5000, 'nn': 5000, 'rl': 5000, 's1': 5000, 's2': 5000, 'tp': 5000}
- [NOTE] tags bt2 :: {'AS': 5000, 'MD': 5000, 'NM': 5000, 'XG': 5000, 'XM': 5000, 'XN': 5000, 'XO': 5000, 'XS': 475, 'YS': 5000, 'YT': 5000}
- [NOTE] tags hs2 :: {'AS': 6303, 'MD': 6303, 'NH': 6303, 'NM': 6303, 'XG': 6303, 'XM': 6303, 'XN': 6303, 'XO': 6303, 'XS': 22, 'YS': 6296, 'YT': 6306, 'ZS': 130
- [NOTE] tags star :: {'AS': 6356, 'HI': 6356, 'MD': 6356, 'NH': 6356, 'NM': 6356, 'nM': 6356}
- [PASS] NM:i and MD:Z emitted by bwa (Skill: "NM/MD | bwa") :: ['AS', 'MC', 'MD', 'MQ', 'NM', 'RG', 'XA', 'XS']
- [PASS] minimap2 -ax sr emits NM but no MD by default (so MD needs calmd or --MD) :: ['AS', 'NM', 'cm', 'de', 'ms', 'nn', 'rl', 's1', 's2', 'tp']
- [PASS] STAR emits NH and HI; HISAT2 emits NH (Skill table) :: (['AS', 'HI', 'MD', 'NH', 'NM', 'nM'], ['AS', 'MD', 'NH', 'NM', 'XG', 'XM', 'XN', 'XO', 'XS', 'YS', 'YT', 'ZS'])
- [PASS] bwa mem -R sets RG:Z on every record and an @RG header line :: RG on 5000 records
- [NOTE] hisat2 @PG count / XS:A records on unspliced DNA reads :: ['3', '22']
- [PASS] '@PG | head -1' names the aligner for bwa :: @PG	ID:bwa	PN:bwa	VN:0.7.19-r1273	CL:bwa mem -t 4 -R @RG\tID:rgA\tSM:synS\tPL:ILLUMINA g.f
- [PASS] '@PG | head -1' names the aligner for bwamem2 :: @PG	ID:bwa-mem2	PN:bwa-mem2	VN:2.2.1	CL:bwa-mem2 mem -t 4 g.fa r1.fq r2.fq
- [PASS] '@PG | head -1' names the aligner for mm2 :: @PG	ID:minimap2	PN:minimap2	VN:2.31-r1302	CL:minimap2 -t 4 -ax sr g.fa r1.fq r2.fq
- [PASS] '@PG | head -1' names the aligner for bt2 :: @PG	ID:bowtie2	PN:bowtie2	VN:2.5.5	CL:"/home/sci/micromamba/envs/alignment-files/bin/bowti
- [PASS] '@PG | head -1' names the aligner for hs2 :: @PG	ID:hisat2	PN:hisat2	VN:2.2.3	CL:"/home/sci/micromamba/envs/alignment-files/bin/hisat2-
- [PASS] '@PG | head -1' names the aligner for star :: @PG	ID:STAR	PN:STAR	VN:2.7.11b	CL:/home/sci/micromamba/envs/alignment-files/bin/STAR-avx2 
- [NOTE] chain.bam @PG (ID, PP) :: [('bwa', None), ('samtools', 'bwa'), ('samtools.1', 'samtools'), ('samtools.2', 'samtools.1'), ('samtools.3', 'samtools.2'), ('samtools.4', 
- [PASS] @PG chain links through PP (bwa -> samtools -> samtools.1 -> ...), linear, first has no PP :: [('bwa', None), ('samtools', 'bwa'), ('samtools.1', 'samtools'), ('samtools.2', 'samtools.1'), ('samtools.3', 'samtools.2'), ('samtools.4', 
- [PASS] Skill example IDs are illustrative: real first samtools ID is "samtools" (no ".1"), and bwa ID is "bwa" not "bwa-mem" :: ['bwa', 'samtools', 'samtools.1', 'samtools.2', 'samtools.3', 'samtools.4']
- [PASS] samtools fixmate -m adds ms:i and MC:Z (lowercase "ms", as Skill says) :: {'MC': 5000, 'ms': 5000}
- [NOTE] markdup flagged reads on random-position synthetic reads :: 6
- [PASS] markdup on a BAM without ms/MC fails LOUDLY (rc!=0, message says to run fixmate) -- Skill says "silently wrong (markdup marking nothing)" :: samtools markdup: error, no ms score tag. Please run samtools fixmate on file first.  samtools markdup: error, no ms sco
- [NOTE] markdup with ms present but MC removed :: samtools markdup: error, no MC tag. Please run samtools fixmate on file first. /  / rc=1
- [NOTE] markdup with MC present but ms removed :: samtools markdup: error, no ms score tag. Please run samtools fixmate on file first. /  / rc=1
- [PASS] bcftools mpileup output identical with and without MD/NM tags (Skill: "MD:Z required by ... bcftools mpileup BAQ" is not true for mpileup) :: md5 with=d82f012d without=d82f012d; variant records -/-
- [NOTE] mpileup on M-CIGAR minimap2 vs --eqx (=/X) BAM: md5, #variants :: (['464c34cc3a7807865cedbca3eb7861a6', '-', '0'], ['464c34cc3a7807865cedbca3eb7861a6', '-', '0'])
- [PASS] minimap2 --eqx BAM really carries =/X ops (and default does not) :: ['5000', '0']
- [PASS] bcftools mpileup tolerates =/X CIGARs: pileup identical to the M-CIGAR alignment (Skill: "bcftools / Picard often need M") :: 464c34cc vs 464c34cc
- [PASS] pysam read.get_tag('NM') returns int; missing tag raises KeyError (Skill points at get_tag) :: [('NM', 0), ('MD', '100'), ('MC', '100M')]
- [PASS] Skill tag-inspection command `samtools view f | head -1 | tr '\t' '\n'` lists one field per line :: NM:i:0 MD:Z:100 MC:Z:100M MQ:i:60 AS:i:100 XS:i:0 RG:Z:rgA 
- [NOTE] real RNA BAM tags/PG ::    8828 AS /    8828 HI /    8828 NH /    8828 RG /    8828 nM / @PG	ID:STAR	PN:STAR	VN:2.7.10a	CL:STAR   --runThreadN 2   --genomeDir star 
- [NOTE] real RNA BAM spliced reads (CIGAR with N) :: SRR5665260.1.9691545 163 chr22 2714 255 48S41M295N61M = 4489 1924 / 805 / 
- [PASS] Skill row "MC:Z | samtools fixmate -m (bwa mem also writes it)": bwa mem output carries MC:Z without any fixmate :: ['AS', 'MC', 'MD', 'MQ', 'NM', 'RG', 'XA', 'XS']
- [PASS] Skill row "minimap2's own ms:i is an unrelated DP score": minimap2 -ax sr writes ms but no MC (so ms there is not fixmate's mate score) :: ['AS', 'NM', 'cm', 'de', 'ms', 'nn', 'rl', 's1', 's2', 'tp']
- [PASS] Skill row "cs:Z | minimap2 --cs": present with --cs :: ['AS', 'NM', 'cm', 'cs', 'de', 'ms', 'nn', 'rl', 's1', 's2', 'tp']
- [PASS] cs:Z absent without --cs (minimap2 default) :: ['AS', 'NM', 'cm', 'de', 'ms', 'nn', 'rl', 's1', 's2', 'tp']
- [NOTE] minimap2 -ax splice tags on unspliced DNA reads (ts:A only appears for spliced alignments) :: ['AS', 'NM', 'cm', 'de', 'ms', 'nn', 'rl', 's1', 's2', 'tp']
- [PASS] Skill row "MD:Z ... samtools calmd regenerates it": calmd adds MD:Z to minimap2 BAM (which has none) :: NM:i:0	ms:i:200	AS:i:200	nn:i:0	tp:A:P	cm:i:14	s1:i:173	s2:i:0	de:f:0	rl:i:0	MD:
- [PASS] Skill row "RX:Z | fgbio AnnotateBamWithUmis": every record of the output BAM carries RX:Z :: [2026/09/20 08:48:32 / FgBioMain / Info] AnnotateBamWithUmis completed. Elapsed time: 0.04 minutes. / XA:Z:syn1,+12262,100M,0;syn1,+7262,100

</details>

### Input 6 — Stress: NEW: multi-region recipes (-M, -M -L, --region-file, pysam fetch_regions) vs a full-scan truth: overlapping, adjacent, nested, gap, identical, chained, multi-contig, 60 + 80 random sets
**Executed:** yes. executed: real 5644-record BAM (10 named sets + 60 random) and the 15-record synthetic multi-contig BAM (80 random sets) with samtools 1.24 and pysam 0.24.1.
**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100 | checks 23/23
**Note:** All 23 checks pass. Truth = parse of `samtools view` (no region) with an independent overlap model; fetch_regions() extracted verbatim from SKILL.md.
**Assertions:**
- [PASS] -M, -M -L bed, --region-file and fetch_regions() each return exactly the full-scan truth (each record once) on 10 named region sets — overlap 5426, adjacent 5550, nested 5550, gap-9bp 802, gap-100bp 802, identical-twice 2732, chained 1170, reverse-order 5058, single-base 539, far-apart 539; default query rows = per-region sum (7356, 7112, 7480, 950, ...)
- [PASS] The same on 60 random multi-region sets (real BAM) and 80 random multi-contig sets (synthetic BAM incl. placed-unmapped, secondary, supplementary, 66,000-op CIGAR) — 140/140 sets equal truth for all four recipes; default duplicates in 19 of 60 real-BAM sets; fetch_regions never repeated a record
- [PASS] Skill numbers reproduce (default 7356, -M/-M -L/--region-file 5426) and the BED convention (0-based half-open) holds for both -L and --region-file — single-base BEDs at 4 positions select exactly the 1-based base
- [PASS] Error paths behave as documented or fail loudly: -M on an unindexed BAM exits 1 naming the index; an unknown contig in a multi-region call warns with exit 0; fetch_regions with a wrong contig raises ValueError — the Skill does not itself say -M needs an index (noted, P2)

<details><summary>Asserted checks that ran for input 6 (from run/out/results.jsonl; 23 checks + notes)</summary>

- [PASS] SKILL.md fetch_regions code block extracted and compiled :: 
- [PASS] full-scan model parsed all 5644 records (5642 placed + 2 unplaced) :: 5644
- [NOTE] set "overlap (Skill example)": truth 5426; default rows 7356 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "overlap (Skill example)": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (5426); default query = sum over regions (7356) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "adjacent, touching": truth 5550; default rows 7112 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "adjacent, touching": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (5550); default query = sum over regions (7112) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "nested": truth 5550; default rows 7480 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "nested": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (5550); default query = sum over regions (7480) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "gap of 9 bp": truth 802; default rows 950 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "gap of 9 bp": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (802); default query = sum over regions (950) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "gap of 100 bp": truth 802; default rows 802 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "gap of 100 bp": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (802); default query = sum over regions (802) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "identical twice": truth 2732; default rows 5464 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "identical twice": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (2732); default query = sum over regions (5464) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "three chained": truth 1170; default rows 1170 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "three chained": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (1170); default query = sum over regions (1170) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "reverse order given": truth 5058; default rows 5058 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "reverse order given": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (5058); default query = sum over regions (5058) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "single base each": truth 539; default rows 540 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "single base each": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (539); default query = sum over regions (540) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [NOTE] set "disjoint far apart": truth 539; default rows 539 :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] region set "disjoint far apart": -M, -M -L bed, --region-file and fetch_regions() all equal the full-scan truth (539); default query = sum over regions (539) :: {'default_eq_per_region_sum': 1, 'default_rc0': 1, 'M': 1, 'M_L': 1, 'region_file': 1, 'L_only': 1, 'fetch_regions_eq_truth': 1, 'fetch_regi
- [PASS] Skill numbers reproduced: default 7356, -M 5426, -M -L 5426, --region-file 5426 (truth 5426) :: ['7356', '5426', '5426', '5426']
- [PASS] BED given as 0-based half-open (start-1, end) selects exactly the 1-based base p for -M -L (Skill comment) :: [('-M -L', 1952, 1, 1, 1), ('--region-file', 1952, 1, 1, 1), ('-M -L', 1959, 2, 2, 2), ('--region-file', 1959, 2, 2, 2)]
- [PASS] --region-file BED uses the same 0-based half-open convention (Skill lists it beside -M -L; convention not stated for it) :: [('-M -L', 1963, 8, 8, 9), ('--region-file', 1963, 8, 8, 9), ('-M -L', 2500, 0, 0, 0), ('--region-file', 2500, 0, 0, 0)]
- [NOTE] 60 random sets on the real BAM: tally :: {'default_eq_per_region_sum': 60, 'default_rc0': 60, 'M': 60, 'M_L': 60, 'region_file': 60, 'L_only': 60, 'fetch_regions_eq_truth': 60, 'fet
- [PASS] 60 random multi-region sets (real BAM): -M, -M -L, --region-file, fetch_regions == truth in all 60; fetch_regions never repeats a record; default over-counts in some sets (meaningful test) :: {'default_eq_per_region_sum': 60, 'default_rc0': 60, 'M': 60, 'M_L': 60, 'region_file': 60, 'L_only': 60, 'fetch_regions_eq_truth': 60, 'fet
- [PASS] -L bed WITHOUT -M is also correct (full scan filter): informational agreement with truth :: 60
- [PASS] synthetic BAM: 15 records loaded, 1 unplaced :: 15
- [NOTE] 80 random multi-contig sets on synthetic BAM: tally :: {'default_eq_per_region_sum': 80, 'default_rc0': 80, 'M': 80, 'M_L': 80, 'region_file': 80, 'L_only': 80, 'fetch_regions_eq_truth': 80, 'fet
- [PASS] 80 random multi-contig sets (synthetic BAM incl. placed-unmapped, secondary, supplementary, 66k-op CIGAR): -M, --region-file, -M -L, fetch_regions == truth; default = per-region sum :: {'default_eq_per_region_sum': 80, 'default_rc0': 80, 'M': 80, 'M_L': 80, 'region_file': 80, 'L_only': 80, 'fetch_regions_eq_truth': 80, 'fet
- [NOTE] -M on an UNINDEXED BAM :: rc=1 / [E::idx_find_and_load] Could not retrieve index file for '/mnt/openscience/audits/bio-sam-bam-basics/run/data/in6/noidx.bam' / samtoo
- [PASS] -M on an unindexed BAM fails loudly (non-zero rc, message names the index) and prints no records :: rc=1 [E::idx_find_and_load] Could not retrieve index file for '/mnt/openscience/audits/bio-sam-bam-basics/run/data/in6/noidx.bam' samtools v
- [PASS] unknown contig mixed in a multi-region call: warning on stderr, still exit 0, records of the good region present :: [main_samview] region "22:1-50" specifies an invalid region or unknown reference. Continue anyway.
- [NOTE] -M with an unknown contig mixed in :: XS:i:0	RG:Z:1 / rc=0 / [W::hts_itr_regions] Region '22' specifies an unknown reference name. Continue anyway
- [PASS] fetch_regions with a wrong contig name raises ValueError (no silent empty result) :: invalid contig `22`
- [PASS] fetch_regions on an empty region list yields nothing :: ok

</details>

### Input 7 — Edge: NEW: 32-record HAND-WRITTEN SAM with planted truth (every FLAG bit, CIGAR ops M/I/D/N/S/H/=/X/P, placed/unplaced unmapped, secondary/supplementary, "*" SEQ, three pair kinds) + view_bam.py matrix + convert_formats.sh
**Executed:** yes. executed: expectations written by hand from the SAM spec before running; SAM, sorted BAM, unsorted BAM, unindexed BAM, unmapped-only BAM (indexed and not), empty SAM/BAM, CRAM with and without its reference, missing file, text file, truncated BAM.
**Scores:** Basic 33/40 | Specialized 50/60 | Total 83/100 | checks 53/54
**Note:** 53 of 54 checks pass; the failing check is a Skill statement: "a round trip keeps every field and tag but not the tag order" is false for CRAM (=/X CIGAR rewritten to M; NM/MD added). view_bam.py raw traceback on a non-numeric limit.
**Assertions:**
- [PASS] FLAG decoding and counts equal hand truth: 12 single bits, 1536/73/133/65/129, and 12 filters (-f/-F/-q, -F 2304 = 28 of 32) — samtools flags and view -c match all hand counts; Skill FLAG table hex==decimal and meanings match the spec
- [PASS] CIGAR consumption table, span/SEQ formulas, N not covered, soft vs hard clip, TLEN (+71/-71, 0 for mate-unmapped and cross-contig), "*" SEQ and SA:Z shape are correct — all 9 ops match htslib; 17 hand-written (SEQ length, span) pairs match; TLEN as planted
- [PASS] view_bam.py: correct counts and exit codes on SAM, sorted/unsorted/unindexed BAM, unmapped-only BAM, empty SAM/BAM, CRAM with the reference reachable / unreachable / 3rd argument; readable errors on missing, text and truncated files — 28/4 mapped/unmapped agrees with -F 4 / -f 4 on every file; unmapped-only 0/4; empty 0/0; CRAM without reference exit 1 with hint; all errors readable
- [PASS] convert_formats.sh SAM->BAM->CRAM(+ref)->SAM/BAM on the hand SAM: rc 0, 32 records; no-reference CRAM output and input==output refused — SAM->BAM byte-identical records; BAM->CRAM->SAM/BAM agree with each other; rc 1 with messages for the two guarded cases
- [FAIL] SKILL.md: "a round trip keeps every field and tag but not the tag order" (CRAM) — CRAM leg turned 4=1X4= into 9M and added MD:Z/NM:i to 16 of 30 realistic records (reference available); MAPQ of an unmapped read 10->0

<details><summary>Asserted checks that ran for input 7 (from run/out/results.jsonl; 54 checks + notes)</summary>

- [PASS] hand-written SAM has 32 records (hand count) by `samtools view -c` :: 32
- [PASS] Skill FLAG table: 12 rows, hex == decimal on every row, decimals are 1..2048 doubling :: [('1', '1'), ('2', '2'), ('4', '4')]
- [PASS] Skill FLAG table meaning column matches the SAM spec for all 12 bits (hand keyword per bit) :: [('1', 'Paired'), ('2', 'Proper pair'), ('4', 'Unmapped'), ('8', 'Mate unmapped'), ('16', 'Reverse strand'), ('32', 'Mate reverse strand'), 
- [PASS] `samtools flags <bit>` == spec name for all 12 single bits (hand names) :: ok
- [PASS] samtools flags 1536/73/133/65/129 decode as the hand truth :: 0x600	1536	QCFAIL,DUP / 0x49	73	PAIRED,MUNMAP,READ1 / 0x85	133	PAIRED,UNMAP,READ2 / 0x41	65	PAIRED,READ1 / 0x81	129	PAIRED,READ2
- [PASS] Skill: mnemonics -> number (147), hex input works, and the Skill's 99/147 strings verbatim :: 0x93	147	PAIRED,PROPER_PAIR,REVERSE,READ2 / 0x93	147	PAIRED,PROPER_PAIR,REVERSE,READ2 / 0x63	99	PAIRED,PROPER_PAIR,MREVERSE,READ1
- [PASS] view -c with -f/-F/-q equals hand-counted truth for 12 filters (incl. Skill's `-F 2304` and plain `-c`) :: {'': 32, '-f 4': 4, '-F 4': 28, '-F 256': 30, '-F 2048': 30, '-F 2304': 28, '-f 1024': 2, '-f 512': 2, '-f 64': 4, '-f 128': 4, '-f 1': 7, '
- [PASS] Skill: `samtools view -c input.bam` counts secondary/supplementary too (32), `-F 2304` primary only (28) - on the SAM file :: (32, 28)
- [PASS] pysam reads all 32 records, keys unique :: 32
- [PASS] SEQ length and reference span of every CIGAR record equal the hand truth (pysam reference_length; SEQ excludes H) - Skill formulas :: 17 records
- [PASS] Skill formulas ("span = sum M/D/N/=/X"; "SEQ length = sum M/I/S/=/X, H excluded") reproduce every hand-written expectation :: ok
- [PASS] Skill consumption table parsed: all 9 ops present :: {'M': (True, True), '=': (True, True), 'X': (True, True), 'I': (True, False), 'S': (True, False), 'D': (False, True), 'N': (False, True), 'H
- [PASS] each op consumption claim (query yes/no, reference yes/no) equals htslib/pysam behaviour for all 9 ops :: all 9 match
- [PASS] N (skipped region) not covered: r_N `4M20N4M` at POS 5 covers 8 reference positions (5-8 and 29-32), reference_end spans 28; get_reference_positions has 8 :: (8, [4, 5, 6, 7, 28, 29, 30, 31])
- [PASS] soft clip stays in SEQ (r_S query_length 11, aligned 6), hard clip does not (r_H query_length 6, inferred 10) :: (11, 6, 10)
- [PASS] TLEN: + on leftmost mate (99, POS 10), - on rightmost (147, POS 61), |TLEN| = 80-10+1 = 71; 0 when mate unmapped (m1) and when mates are on different contigs (x1) :: (71, -71)
- [PASS] unmapped mate placed at its mate's position: m1/133 has reference ctgA, start 99, no CIGAR; samtools view shows POS 100 :: ('ctgA', 99)
- [PASS] "*" SEQ (secondary record): query_sequence None, samtools prints "* *" :: None
- [PASS] SA:Z tag on the supplementary record has the Skill's documented shape rname,pos,strand,CIGAR,mapQ,NM; :: ctgB,10,+,10S5M,60,0;
- [PASS] pysam is_* property for each of the 12 single-bit records is True (only that bit set) :: no failures logged above
- [PASS] CRAMs built: hand.cram has 32 records, unmapped_only.cram 4 (truth -f 4) :: ['32', '4']
- [PASS] view_bam.py hand.sam: rc 0, "Mapped/Unmapped" = (28, 4) = samtools -F4/-f4 truth (28/4), from scan :: rc=0 stats=(28, 4, 'scan') err=
- [PASS] view_bam.py hand.bam: rc 0, "Mapped/Unmapped" = (28, 4) = samtools -F4/-f4 truth (28/4), from index :: rc=0 stats=(28, 4, 'index') err=
- [PASS] view_bam.py hand_noidx.bam: rc 0, "Mapped/Unmapped" = (28, 4) = samtools -F4/-f4 truth (28/4), from scan :: rc=0 stats=(28, 4, 'scan') err=
- [PASS] view_bam.py unsorted.bam: rc 0, "Mapped/Unmapped" = (28, 4) = samtools -F4/-f4 truth (28/4), from scan :: rc=0 stats=(28, 4, 'scan') err=
- [PASS] view_bam.py unmapped_only.bam: rc 0, "Mapped/Unmapped" = (0, 4) = samtools -F4/-f4 truth (0/4), from index :: rc=0 stats=(0, 4, 'index') err=
- [PASS] view_bam.py unmapped_only_noidx.bam: rc 0, "Mapped/Unmapped" = (0, 4) = samtools -F4/-f4 truth (0/4), from scan :: rc=0 stats=(0, 4, 'scan') err=
- [PASS] view_bam.py empty.bam: rc 0, "Mapped/Unmapped" = (0, 0) = samtools -F4/-f4 truth (0/0), from index :: rc=0 stats=(0, 0, 'index') err=
- [PASS] view_bam.py empty_noidx.bam: rc 0, "Mapped/Unmapped" = (0, 0) = samtools -F4/-f4 truth (0/0), from scan :: rc=0 stats=(0, 0, 'scan') err=
- [PASS] view_bam.py empty.sam: rc 0, "Mapped/Unmapped" = (0, 0) = samtools -F4/-f4 truth (0/0), from scan :: rc=0 stats=(0, 0, 'scan') err=
- [PASS] view_bam.py hand.cram, UR target reachable (ref.fa beside it): 28/4 from scan, rc 0 :: rc=0 (28, 4, 'scan') 
- [PASS] view_bam.py hand.cram, reference unreachable: exit 1, readable "Error reading ..." + CRAM hint, no Traceback, no fake statistics line :: rc=1 out='References: 2\n' err=rror reading /mnt/openscience/audits/bio-sam-bam-basics/run/data/in7/hand.cram: truncated file (CRAM needs it
- [PASS] view_bam.py hand.cram <limit> <reference.fa> resolves via the 3rd arg even though UR is dead: 28/4, rc 0 :: rc=0 (28, 4, 'scan') 
- [PASS] unmapped-only CRAM whose reads are PLACED (ctgA:50/100/150) still needs the reference: view_bam.py exits 1 with the CRAM hint when it is gone :: rc=1 None basics/run/data/in7/unmapped_only.cram: truncated file (CRAM needs its reference: pass reference.fa as the 3rd argument)
- [PASS] Skill full-decode check `view -o /dev/null f.cram && echo ok` also fails on that placed-unmapped CRAM while the reference is gone (consistent with the Skill text) :: rc=1
- [PASS] CRAM holding only the UNPLACED unmapped read decodes with no reference at all ("ok" printed): the Skill check proves decodability, so for such a file it cannot prove the reference is reachable :: ok 1 rc=0
- [PASS] view_bam.py header row labels the coordinate: "name  chrom:start(0-based)  strand  cigar" :: name	chrom:start(0-based)	strand	cigar
- [PASS] view_bam.py rows: r_M shows ctgA:4 (POS 5 - 1) + 10M; r_H shows 2H6M2H; p1 reverse mate shows "-"; hard/soft clips and N printed verbatim :: [['r_M', 'ctgA:4', '+', '10M'], ['p1', 'ctgA:9', '+', '20M'], ['p1', 'ctgA:60', '-', '20M']]
- [PASS] view_bam.py unmapped rows: placed one shows ctgA:49 ... unmapped, unplaced shows * ... unmapped (never None:-1) :: {'u_placed': ['u_placed', 'ctgA:49', '+', 'unmapped'], 'u_unplaced': ['u_unplaced', '*', '+', 'unmapped']}
- [PASS] limit 0: prints the header row and no records, rc 0 :: References: 2 Mapped: 28  Unmapped: 4  (from scan)  name	chrom:start(0-based)	strand	cigar
- [PASS] limit larger than the file prints all 32 records :: 36
- [PASS] missing file: exit 1, "Error reading" message, no Traceback :: rc=1 [E::hts_open_format] Failed to open file "/mnt/openscience/audits/bio-sam-bam-basics/run/data/in7/does_not_exist.bam" : 
- [PASS] non-alignment text file: nonzero exit and a readable error (no bare Traceback) :: rc=1 out='' err=Error reading /mnt/openscience/audits/bio-sam-bam-basics/run/data/in7/notbam.txt: file does not contain alignment data
- [PASS] truncated BAM: nonzero exit with a readable error, no Traceback :: rc=1 out='' err=Error reading /mnt/openscience/audits/bio-sam-bam-basics/run/data/in7/trunc.bam: no BGZF EOF marker; file may be truncated
- [NOTE] non-numeric limit argument :: rc=1 err=) > 2 else 10             ^^^^^^^^^^^^^^^^ ValueError: invalid literal for int() with base 10: 'abc'
- [PASS] no arguments: usage line, exit 1 :: Usage: view_bam.py <input.sam/bam/cram> [limit] [reference.fa]
- [PASS] convert_formats.sh SAM -> BAM keeps all 32 records byte-identical (fields + tags) :: (0, 32)
- [PASS] convert_formats.sh BAM -> CRAM(+ref) -> SAM and -> BAM: rc 0, 32 records, SAM and BAM outputs agree with each other :: (0, 0, 0, 32, 32)
- [NOTE] records changed by BAM->CRAM->SAM (fb_* excluded) :: {'r_M/0': ['tags+MD,NM tags-'], 'r_I/0': ['tags+MD,NM tags-'], 'r_D/0': ['tags+MD,NM tags-'], 'r_N/0': ['tags+MD,NM tags-'], 'r_S/0': ['tags
- [PASS] CRAM leg rewrites the `=`/`X` CIGAR of r_EQX (4=1X4= -> 9M) and nothing else in columns 1-11 of the realistic records :: {('r_EQX', '0'): ['fields:col6 4=1X4=->9M', 'tags+MD,NM tags-']}
- [PASS] CRAM decode adds MD:Z and NM:i to mapped records that had neither (reference available): MD/NM appear on the mapped, non-clipped-only records :: 16
- [FAIL] SKILL.md line "a round trip keeps every field and tag but not the tag order" holds for this file (CRAM changed a CIGAR and added tags) :: 16 of 30 realistic records differ: [(('r_M', '0'), ['tags+MD,NM tags-']), (('r_I', '0'), ['tags+MD,NM tags-'])]
- [PASS] fb_4 (unmapped, MAPQ 10) and nonsense flag 0x20-without-0x1 are normalised by CRAM: MAPQ 10->0 and flag 32->33 (informational, planted-nonsense records) :: ('0', [('fb_32', '33')])
- [PASS] convert_formats.sh CRAM -> BAM with no reference arg and the UR target gone: non-zero rc (no silent success) :: rc=1 /mnt/openscience/audits/bio-sam-bam-basics/run/data/in7/ref.fa: No such file or directory [E::refs_l
- [PASS] convert_formats.sh SAM -> CRAM without the reference argument: rc 1 and message says a reference is required :: Error: CRAM conversion requires reference.fa rc=1
- [PASS] convert_formats.sh input == output refuses (rc 1) and the SAM keeps 32 records :: Error: input and output are the same file; refusing to overwrite the input rc=1

</details>

### Input 8 — Adversarial: NEW: CRAM reference states on a second real dataset (nf-core SARS-CoV-2): -T, UR, gone, REF_PATH/REF_CACHE, the Skill recipe verbatim, wrong/missing-contig reference, ignore_md5, embed_ref, -C without -T; =/X and MD through CRAM on real minimap2 --eqx output
**Executed:** yes. executed: every state decoded with the Skill's own check and independently by md5 of columns 1-11 against the source BAM; HOME redirected so no ~/.cache/hts-ref could rescue a decode; pysam read attempt with the reference gone.
**Scores:** Basic 33/40 | Specialized 50/60 | Total 83/100 | checks 23/23
**Note:** 23 of 23 checks pass, but two of them confirm that the Skill's CRAM round-trip sentence is inaccurate on real aligner output (=/X lost, MD added).
**Assertions:**
- [PASS] For every reference state the Skill's check `view -o /dev/null f.cram && echo ok` gives the right verdict and an independent decode agrees — -T ok; UR ok; gone -> no "ok", rc 1 "Unable to fetch reference"; REF_PATH (M5-named) ok; REF_CACHE ok; embed_ref=1 ok with nothing reachable; wrong reference and lacking-contig reference fail (MD5 mismatch)
- [PASS] The HPC recipe in SKILL.md runs verbatim: cache created under $HOME/cram_cache, quickcheck silent, full-decode check prints ok — one cache file created; ok, rc 0
- [PASS] view -c / flagstat / idxstats / quickcheck succeed with the reference gone while stats and pysam iteration fail loudly; ignore_md5=1 makes the wrong-reference decode silent — view -c 200, flagstat 200+0, idxstats 197/3, qc rc 0; stats non-zero; pysam OSError; ignore_md5 rc 0 with different SEQ column
- [PASS] -C without -T and no reachable reference exits 0 with the embed_ref=2 warning and the CRAM decodes with no reference — as SKILL.md states
- [FAIL] SKILL.md: "a round trip keeps every field and tag but not the tag order" holds for real aligner output — minimap2 --eqx BAM: 5000/5000 reads lose their =/X ops to M in the CRAM; minimap2 default BAM: MD:Z appears on 5000 reads that had none

<details><summary>Asserted checks that ran for input 8 (from run/out/results.jsonl; 23 checks + notes)</summary>

- [PASS] source BAM: 200 records on MT192765.1 :: 200
- [PASS] CRAM header @SQ carries M5 and UR (points at d1/ref.fa) :: @SQ	SN:MT192765.1	LN:29829	M5:c95f3e5592d0ad9974e41e7f0ea14eb0	UR:/mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/d1/ref.fa
- [PASS] A: -T d1/ref.fa: Skill check `view -o /dev/null f.cram && echo ok` prints ok=True (expected True); independent decode identical to source (rc 0, 200 rows) :: 'ok\nrc=0' 
- [PASS] B: no -T, no env, UR path reachable (fallback 4): Skill check `view -o /dev/null f.cram && echo ok` prints ok=True (expected True); independent decode identical to source (rc 0, 200 rows) :: 'ok\nrc=0' 
- [PASS] C: reference gone (UR dead, no env): Skill check `view -o /dev/null f.cram && echo ok` prints ok=False (expected False); independent decode fails (rc 1, 0 rows) :: 'rc=1' [E::fai_build3_core] Failed to open the file /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/d1/ref.fa : No such
- [PASS] C: with the reference gone, `view -c` (200), flagstat (200 + 0), idxstats (MT192765.1 29829 197 3: 197 mapped + 3 placed-unmapped) all succeed and quickcheck rc 0: none of them can prove reachability (Skill claim) :: 200 / 200 + 0 in total (QC-passed reads + QC-failed reads) / MT192765.1	29829	197	3 / qc=0
- [PASS] C: `samtools stats` (decodes bases) fails non-zero with the reference gone (Skill: "or stats") :: rc=254[E::fai_build3_core] Failed to open the file /mnt/openscience/audits/bio-sam-bam
- [NOTE] C: samtools depth on the unreachable CRAM :: 12853 rc=0
- [PASS] D: REF_PATH=<dir>/%s holding a file named by the M5: Skill check `view -o /dev/null f.cram && echo ok` prints ok=True (expected True); independent decode identical to source (rc 0, 200 rows) :: 'ok\nrc=0' 
- [NOTE] D2: REF_PATH=<dir> without %s (informational) :: ok / rc=0
- [PASS] G: REF_PATH pointing at a dir with the FASTA under its normal name (Skill: elements are matched by the @SQ M5 name): Skill check `view -o /dev/null f.cram && echo ok` prints ok=False (expected False); independent decode fails (rc  :: 'rc=1' [E::fai_build3_core] Failed to open the file /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/d1/ref.fa : No such
- [PASS] seq_cache_populate.pl writes cache/<M5[0:2]>/<M5[2:4]>/<M5[4:]> :: ww.htslib.org/workflow/cram#the-ref_path-and-ref_cache for further information. cache/c9/5f/3e5592d0ad9974e41e7f0ea14eb0
- [PASS] E: REF_CACHE=<root>/%2s/%2s/%s: Skill check `view -o /dev/null f.cram && echo ok` prints ok=True (expected True); independent decode identical to source (rc 0, 200 rows) :: 'ok\nrc=0' 
- [PASS] F: the Skill's HPC recipe run verbatim (mkdir, seq_cache_populate.pl, exports, quickcheck, full-decode check): quickcheck silent, then prints "ok", rc 0 :: Reading /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/d1.gone/ref.fa ... / /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8
- [PASS] F: the recipe created the cache under $HOME/cram_cache :: o-sam-bam-basics/run/data/in8/home/cram_cache/c9/5f/3e5592d0ad9974e41e7f0ea14eb0
- [PASS] H: -T points at a 1-base-different reference: refused, MD5 mismatch: Skill check `view -o /dev/null f.cram && echo ok` prints ok=False (expected False); independent decode fails (rc 1, 0 rows) :: 'rc=1' [E::cram_decode_slice] MD5 checksum reference mismatch at MT192765.1:121-29602 [E::cram_decode_slice] CRAM  : b9d9a16fd8
- [PASS] I: -T points at a FASTA that lacks MT192765.1: fails: Skill check `view -o /dev/null f.cram && echo ok` prints ok=False (expected False); independent decode fails (rc 1, 0 rows) :: 'rc=1' [W::cram_get_ref] Reference file given, but ref 'MT192765.1' not present [E::fai_build3_core] Failed to open the file /m
- [PASS] H2: with ignore_md5=1 the wrong reference decodes (rc 0, 200 rows) but the SEQ column differs from the source: silent corruption only when the check is disabled (Skill) :: rc=0 n=200 seq-identical=False
- [PASS] J: embed_ref=1 CRAM with no reference reachable anywhere: Skill check `view -o /dev/null f.cram && echo ok` prints ok=True (expected True); independent decode identical to source (rc 0, 200 rows) :: 'ok\nrc=0' 
- [PASS] K: `samtools view -C` with no -T and no reachable reference exits 0, warns "Enabling embed_ref=2", writes a CRAM (Skill text) :: rc=0 1 [W::cram_get_ref] Failed to populate reference "MT192765.1" [W::cram_get_ref] See https://www.htslib.org/doc/reference_seqs.html for 
- [PASS] K2: that noT.cram decodes with no reference at all: Skill check `view -o /dev/null f.cram && echo ok` prints ok=True (expected True); independent decode identical to source (rc 0, 200 rows) :: 'ok\nrc=0' 
- [PASS] pysam iterating a CRAM whose reference is gone raises OSError/ValueError (does not return partial data silently) :: OSError: truncated file
- [PASS] pysam 'rc' + reference_filename decodes all 200 reads with the UR path dead :: 200
- [NOTE] minimap2 eqx: reads with =/X ops before -> after CRAM round trip; reads with MD:Z before -> after :: ('5000', '0', '0', '5000')
- [NOTE] minimap2 mm2: reads with =/X ops before -> after CRAM round trip; reads with MD:Z before -> after :: ('0', '0', '0', '5000')
- [PASS] REAL minimap2 --eqx BAM: =/X CIGAR ops are rewritten to M by the CRAM round trip (before >0, after 0): Skill text says a round trip keeps every field :: (5000, 0)
- [PASS] REAL minimap2 BAM (NM, no MD): the CRAM round trip ADDS MD:Z to every mapped read (0 -> >0) :: (0, 5000)

</details>

## What was run (all in `run/`)

- `run_all.sh` (WSL: regression + new inputs) and `run_rsamtools.sh` (Windows R via `r.sh`); `build_report.py` writes this file and the JSON from `out/results.jsonl`.
- `regress/`: pre-fix scripts re-pointed at `run/skill` (`in1`, `in1b`, `in1_rsamtools.R`, `in2`, `in2_diff.sh`, `in3`, `in4`, `in4b`, `in5`, `in5.sh`, `make_reads.py`, `make_synth.py`, `00_probe.sh`, `chk.py`), with assertions rewritten where they had encoded a defect.
- `new/`: `in6.py` (multi-region), `in7.py` (hand-written SAM + view_bam matrix + helper), `in8.py` (CRAM reference states), `dedup_check.py`, `misc_claims.py`, `tags_check.py`, `in5c_mapdamage.sh`. `debug/`: three diagnostic scripts that explained the CRAM round-trip diffs and the helper's leftover output.
- `out/`: raw outputs; `data/`: only the small synthetic inputs (bulky BAM/CRAM intermediates deleted, rebuilt by `run_all.sh`).
- Deviations from the pre-fix scripts worth knowing: the F: drive is case-insensitive, so `h.bam -> h.BAM` hit the helper's own input==output guard (correct); the test writes `h5.BAM` instead. An early in7 expectation ("unmapped-only CRAM needs no reference") was wrong (placed unmapped reads do need it) and was corrected before scoring; the 1-base-different reference must sit inside a covered position for the ignore_md5 test to show a difference.
