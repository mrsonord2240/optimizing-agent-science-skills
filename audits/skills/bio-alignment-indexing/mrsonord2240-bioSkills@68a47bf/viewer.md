> **Audit record for `bio-alignment-indexing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@68a47bf](https://github.com/mrsonord2240/bioSkills/tree/68a47bf30aae303543db67ce46ecc8b068b06f78/alignment-files/alignment-indexing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-indexing (RE-AUDIT of the fixed Skill)
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@68a47bf30aae303543db67ce46ecc8b068b06f78:alignment-files/alignment-indexing` (read from worktree `wt/af-index`, copied to `run/skill/`; md5 of the three files identical to the worktree)
Pre-fix report (archived `_pre-fix-20260920`): 75, Beta Only, not deployable. Fix log read for orientation only; nothing in it is used as evidence.
Environment: WSL `science` env `alignment-files`: samtools/htslib 1.24, pysam 0.24.1, bedtools 2.31.1, GATK 4.6.2.0. Category Data Analysis, Mode D. Every script is in `run/scripts/`, every stdout in `run/out/`. Rerun: `wsl_run.sh 'bash /mnt/openscience/audits/bio-alignment-indexing/run/run_all.sh r1_canonical r2_cram_faidx r3_edge r4_large_genome r5_stress n6_region_parser n7_ensure_index_edges n7b_sibling_index_probe'`.

**Result: final 85 -> Limited Release (assertion-rate floor 27/35 = 77.1% drops it one tier from Production Ready); deployable; no veto; 0 P0, 0 P1, 6 P2. Executed 7/7. 174 of 183 scripted checks pass; the 9 FAILs are the new findings.**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 37 | 56 | 93 | 5/5 | ✅ |
| 2 | Variant A: CRAM (regression) | 35 | 52 | 87 | 4/5 | ✅ |
| 3 | Edge (regression) | 34 | 50 | 84 | 4/5 | ✅ |
| 4 | Variant B: large genome (regression) | 34 | 50 | 84 | 3/5 | ✅ |
| 5 | Stress (regression) | 37 | 55 | 92 | 5/5 | ✅ |
| 6 | Scope Boundary: region parser (NEW) | 30 | 44 | 74 | 2/5 | ⚠️ |
| 7 | Adversarial: ensure_index edges (NEW) | 33 | 48 | 81 | 4/5 | ✅ |

**Execution average: 85.0 / 100** (pre-fix 5-input average 75). **Static: 84 / 100** (pre-fix 75). Final = 84 x 0.4 + 85.0 x 0.6 = 33.6 + 51.0 = 84.6 -> 85.
**Assertion pass rate: 27/35.** Floors: static 84 (>= 80 ok), execution 85.0 (>= 85 ok), Layer 1 avg 34.3 (>= 32 ok), Layer 2 avg 50.7 (>= 48 ok), assertions 77.1% (< 90%, and also < the Limited floor of 80%; one-tier downgrade applied as the rubric says "exactly one"; a double application would give Beta Only).

Inputs 1-5 are the first audit's inputs re-run against the fixed text. Snippets are **extracted from the shipped SKILL.md** by `common.py` (`block_containing`), not retyped, so a wrong snippet in the file fails the test. Inputs 6-7 are new and aim at the fixer's own code.

## Regression: what the first audit found, now

| First-audit finding | Result on the fixed Skill (own run) |
|---|---|
| P1 stale .csi beats fresh .bai after the `-nt .bai` snippet | Closed. `ensure_index` on stale-CSI BAM: count 1095 == full scan, files `['t.bam','t.bam.csi']`; fresh .bai + stale .csi repaired; Python twin same (r5) |
| P1 batch loop redundant .bai on CSI files | Closed. Loop kept BAI as BAI and CSI as CSI, built the missing one, errored on the unsorted BAM and continued (r5) |
| P1 CRAM: no reference, pysam idxstats 0 | Closed. `-T` 5642 == BAM 5642; no reference -> 0 records + `Failed to populate reference`, `view -c` 5642; pysam `OSError: truncated file`; `get_index_statistics()` 0; `pysam.idxstats` 5642 (r2) |
| P1 large-genome section wrong x4 | Closed. BAI exit 1 + no .bai; `-c` min_shift 14 depth 6 on 830 Mbp; `-m 18` depth 4 = 2^30; 2.0 Gbp depth 6 / 5; queries == hand truth (r4). Residual: see finding 4 |
| P1 `-L bed` shown as index access | Closed. `--region-file` == `-M -L` == region args == 1791 on a damaged-tail BAM; plain `-L` rc 1; 1.52 s vs 0.02 s on 1.2 M reads (r5) |
| P2 Common Errors strings | Closed. 27/27 checks in r3 include each verbatim string |
| P2 fetch_regions.py region forms, CRAM | Mostly closed (2,604/2,605 strings equal); see findings 1-2 |
| P2 `is_indexed()` | Replaced by `ensure_indexed`; alt `x.bai`, `.crai` handled (r1, r2, n7) |
| P2 mito awk, `-F 2304`, FASTA off-by-one, threads claim | Closed: chrM 50.00%, MT 33.33%, empty BAM silent; `-F 2308` == 4; `fetch(999,2000)` == faidx; `-@` 0/4/8 = 1.62/1.57/1.82 s |

## Judgements requested

- **Pine / axolotl contig sizes (fixer could not verify).** Not correct as left. Sugar pine longest scaffold is 23,976,851 bp after rescaffolding (4,064,336 bp originally; G3 2017 Table 2, PMC5427496) and loblolly v2.0 scaffold N50 is about 107 kb (PMC5437942), so BAI is enough for those assemblies and the "Pine, fir, ... -> CSI" row misleads. "up to 2^31-1 bp" is a limit, not a size. Axolotl: assembly split into 28 p/q arms "for technical reasons", scaffold N50 1.2 Gb (PNAS 2021, PMC8053990), so arms over 537 Mbp are plausible and CSI is right, but I could not obtain the largest arm length. Also, `r4_large_genome.py` shows the sentence "a contig above 2^31-1 bp cannot be stored in BAM at all" is an overstatement: a BAM with an `LN:3000000000` header and reads at 1000 and 2,000,000,000 writes, CSI-indexes (min_shift 14, depth 6) and returns both reads; only a read positioned above 2^31-1 fails (`Positional data is too large for BAM format`).
- **Dropped X/Y ratio prompt.** Acceptable: it had no code and no verification and would need PAR handling.
- **usage-guide.md dedup.** Nothing the agent needs was lost. Every deleted command, table row and troubleshooting entry exists in SKILL.md, corrected. Trivia dropped: `get_reference_length` example, a per-chromosome percent-share pysam snippet, the "8 threads" prompt.

## New findings (inputs 6 and 7)

1. **`fetch_regions.py` tracebacks on `chr22:0-N` and end<start.** `samtools view -c chr22:0-4000` = 5550; the example: `ValueError: start out of range (-1)` (raw pysam traceback). `chr22:5000-4000`: `ValueError: invalid coordinates: start (4999) > stop (4000)`. The fix log claims bad coordinates exit with a message; only malformed text and unknown contigs do.
2. **Contig names containing a comma are rejected** (`ctg,1` -> `unknown contig 'ctg1'`; 260 of 2,605 strings on the synthetic BAM). samtools returns 30. Cause: `region.replace(',', '')` runs on the whole string.
3. **Bash `ensure_index` deletes a sibling's index with alternate-style names.** `sample.bam` + `sample.cram` indexed as `sample.bai` / `sample.crai`: `ensure_index sample.cram` removed `sample.bai`; `ensure_index sample.bam` removed `sample.crai`. Standard `.bam.bai` / `.cram.crai` names are safe. The Python twin does not cross formats.
4. **Genome table / 2^31-1 wording** (above). 5. **`REF_PATH` named without its format**: a directory holding `genome.fasta` gives 0 records; only flat MD5-named files or a `%2s/%2s/%s` pattern give 2 (`refpath_probe.sh`).
6. Limits worth one line: freshness is mtime-only (truncated fresh .bai and an old-mtime restore pass as fresh); batch loop in a directory with no BAMs runs `samtools index '*.bam'`; a stale CSI built with `-m 12` is rebuilt at default.

## Detailed Outputs

### Input 1 - Canonical (regression) - `scripts/r1_canonical.py`, 42/42
**Prompt:** "Index this HG00349 chr20 slice BAM (and the human chr22 slice) as BAI and CSI, pull regions, and check idxstats against a full scan."
**Ran:** every command of the fixed SKILL on REAL 1000G + nf-core human BAMs. 53 regions (50 random + whole-slice + edges) by six methods.
```
[PASS] 53 regions: full-scan truth == samtools view -c (BAI) == (CSI) == pysam fetch == pysam count == pysam CSI :: mismatches=[]
[PASS] fetch_regions.py Total == samtools view -c :: tot=['Total reads in chr20:1440001-1440500: 127'] expected=127
[PASS] SKILL 'samtools view -X input.bam output.bai region' works and == standard count
[PASS] SKILL mito awk on 'MT' contig (true 33.33%) / 'chrM' (true 50.00%) / empty BAM prints nothing
```
**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100
**Assertions:** 5/5 PASS (see JSON).

### Input 2 - CRAM (regression) - `scripts/r2_cram_faidx.py`, 22/22, `scripts/refpath_probe.sh`
**Prompt:** "Index my CRAM, pull chr22:1952-4700, get idxstats, and index the reference FASTA."
```
[PASS] SKILL `samtools view -T ref.fa in.cram region` returns records == BAM count 5642
[PASS] without a reachable reference `samtools view` prints no records and says 'Failed to populate reference'
[PASS] pysam without reference raises OSError 'truncated file'; get_index_statistics() gives 0 mapped; pysam.idxstats gives chr22 40001 5642 0
[PASS] SKILL FastaFile snippet fetch(999,2000) == faidx chr22:1000-2000 (fixed off-by-one)
refpath_probe:  REF_PATH=<dir with genome.fasta> : 0 | flat MD5-named dir : 2 | nested dir bare : 0 | '<dir>/%2s/%2s/%s' : 2 | -T : 2
```
**Scores:** Basic 35 | Specialized 52 | Total 87. **Assertions:** 4/5 (FAIL: "set REF_PATH" advice not actionable as written).

### Input 3 - Edge (regression) - `scripts/r3_edge.py`, 27/27
Unsorted real UMI BAM (`Unsorted positions on sequence #1: 3477 followed by 3470`, `failed to create index`, no index), sort->index keeps 15788 records, lying `@HD` refused, wrong contig (`22:1-4000` -> exit 0, 0 reads, `specifies an invalid region or unknown reference. Continue anyway.`), pysam `ValueError: invalid contig`, missing index strings verbatim, empty BAM `chr22 40001 0 0`.
Informational (feeds input 6): `[0-based start] chr22:0-100 -> samtools 0 | example rc=1 ValueError: start out of range (-1)`; `[end before start] chr22:5000-4000 -> example rc=1 ValueError: invalid coordinates`.
**Scores:** Basic 34 | Specialized 50 | Total 84. **Assertions:** 4/5 (FAIL: example exits cleanly on every malformed region).

### Input 4 - Large genome (regression) - `scripts/r4_large_genome.py`, 15/15
```
[PASS] BAI on >2^29 contig fails loudly: exit 1, no .bai;  message 'cannot be stored in a bai index. Try using a csi index'
[PASS] default -c: min_shift 14, depth 6 (2^32) on 830 Mbp;  -m 18 -> depth 4 (2^30);  2.0 Gbp: depth 6 / 5
[PASS] read positioned beyond 2^31-1 -> 'Positional data is too large for BAM format'
[PASS] LN=3,000,000,000 header + reads at 1000 and 2,000,000,000 -> writes, index -c ok (14,6), both reads found  <- contradicts 'cannot be stored in BAM at all'
```
**Scores:** Basic 34 | Specialized 50 | Total 84. **Assertions:** 3/5 (FAIL: "cannot be stored in BAM at all"; FAIL: pine row supported by real sizes).

### Input 5 - Stress (regression) - `scripts/r5_stress.py`, 29/29
```
[PASS] FORMER TRAP: after ensure_index on a stale-CSI BAM the region count == truth and only a fresh .csi remains :: count='1095' truth=1095 files=['t.bam','t.bam.csi']
[PASS] fresh .bai + stale .csi: before ensure_index the count is wrong/erroring; after it == truth
[PASS] SKILL batch loop: ... unsorted BAM errors but loop continues :: ['a_ok.bam','a_ok.bam.bai','b_csi.bam','b_csi.bam.csi','c_none.bam','c_none.bam.bai','d_unsorted.bam']
[INFO] corrupt-tail BAM: region arg 1791 | -L rc=1 | -M -L 1791 | --region-file 1791 | full scan rc=1
[INFO] intact 1.2M-read BAM: -L 1.52s n=1791; -M -L 0.02s n=1791
[INFO] -@0 1.62s  -@4 1.57s  -@8 1.82s
[PASS] GATK/htsjdk prefers .bai: wrong .bai -> Invalid GZIP header, correct .bai + wrong .csi -> 1095 == truth
```
**Scores:** Basic 37 | Specialized 55 | Total 92. **Assertions:** 5/5.

### Input 6 - NEW, region parser - `scripts/n6_region_parser.py`, 9/16
**Prompt:** "Fetch these regions with the shipped example and make sure they match samtools" over human chr22, 1000G chr20 (3,366-contig header incl. HLA-*:* names), ARTIC MN908947.3, RNA BAM, and a synthetic BAM with contigs `a:1-5`, `ctg,1`, `12:34`, `x-y`, `HLA-A*01:01:01:01`.
2,605 region strings (six read-edge +-1 positions per contig, random, whole-contig, past-end; forms `c:s-e`, commas, `c:s-`, `c:s`, `{c}:s-e`, bare). Compared: shipped `parse_region` + `fetch` vs `samtools view -c` vs full scan.
```
[INFO] total region strings compared: 2605
[FAIL] count == samtools == truth on every accepted region :: 1 mismatch: ('weird','ctg,1','bare contig', truth 30, samtools 30, example REJECT unknown contig '')
[FAIL] no accepted-by-samtools region rejected :: 260 rejected (all ctg,1...) e.g. 'ctg,1:2760-2859' -> unknown contig 'ctg1'
[INFO] [human] 'chr22:0-100' samtools=0 | example CRASH ValueError: start out of range (-1)
[INFO] samtools chr22:0-4000 -> 5550; example -> CRASH
[INFO] [human] 'chr22:5000-4000' samtools=0 (warn) | example CRASH ValueError: invalid coordinates: start (4999) > stop (4000)
[PASS] contigs 'a:1-5' (30, and 18 with :1-2500), '12:34:100-4000' (26), 'x-y:1-5000', 'HLA-A*01:01:01:01:1-1500' (14): example == samtools
[PASS] chr22:1952-1952 == 1, chr22:1951-1951 == 0, chr22:-2000 == 539, chr22:1952-99999999 == 5642: example == samtools
```
**Scores:** Basic 30 | Specialized 44 | Total 74. **Assertions:** 2/5.

### Input 7 - NEW, ensure_index edge cases - `scripts/n7_ensure_index_edges.py` 29/29, `scripts/n7b_sibling_index_probe.py` 1/3
Held (both helpers where applicable): equal mtimes fresh; 1.1 s newer stale; `.bai`+`.csi` fresh/fresh, stale/stale, stale `.bai` + fresh `.csi`; alt `x.bai` fresh (kept) and stale (deleted, rebuilt); `.crai` alt fresh/stale; spaces/parentheses/brackets; symlinked BAM; `set -euo pipefail`; `-@ 4`; unsorted replacement fails loudly and leaves no index.
```
[INFO] CSI (min_shift, depth) before (12, 6), after stale-rebuild (14, 5)
[INFO] truncated fresh .bai (27960->9320 bytes) after ensure_index: count=rc=1 [E::hts_idx_load3] Could not load local index file
[INFO] batch loop in a directory with no BAMs: rc=1 err='[E::hts_open_format] Failed to open file "*.bam"'
[PASS] standard names (sample.bam.bai + sample.cram.crai): re-indexing a stale CRAM leaves the BAM's index alone
[INFO] alt names, stale CRAM: files after = ['sample.bam', 'sample.cram', 'sample.cram.crai']     <- sample.bai deleted
[FAIL] alternate names: refreshing the CRAM index does not delete sample.bai (the BAM's index)
[INFO] alt names, stale BAM: files after = ['sample.bam', 'sample.bam.bai', 'sample.cram']         <- sample.crai deleted
[FAIL] alternate names: refreshing the BAM index does not delete sample.crai (the CRAM's index)
```
**Scores:** Basic 33 | Specialized 48 | Total 81. **Assertions:** 4/5.

## Research Veto (Data Analysis)
M1 PASS (no fabricated values; every number reproduced) | M2 PASS (utility; X/Y prompt removed) | M3 PASS (first-audit fallacies corrected and re-verified) | M4 PASS (all shipped code ran; the example's uncaught ValueErrors are robustness defects). Skill Veto T1-T4 PASS (determinism: BAI bytes identical across `samtools`, `pysam`, `-@ 8`).

## Recommendations
All P2 (no P0, no P1): (1) fetch_regions.py 0-based start / end<start traceback; (2) comma contig names; (3) bash `ensure_index` sibling-index deletion, make candidates format-specific; (4) pine row and "cannot be stored in BAM at all"; (5) REF_PATH format; (6) nullglob, mtime-only note, `-m` pass-through. Full text in the JSON.

## Record hygiene
`run/` holds scripts, `skill/` (copy of the audited commit), tiny synthetic BAMs in `data/` (all synthetic, built by `make_synth.py`), `out/` stdout and JSON per script. The 1.2 M-read `big.bam` and `work/` were deleted after the run (rebuilt by `run_all.sh`). No symlinks, no `__pycache__`. Nothing written to `external/`, the worktree, or `public-data/`.
