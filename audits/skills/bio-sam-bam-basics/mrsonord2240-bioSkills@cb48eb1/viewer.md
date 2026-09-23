> **Audit record for `bio-sam-bam-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cb48eb1](https://github.com/mrsonord2240/bioSkills/tree/cb48eb16bf63f75098c865da4e8f7bf3191af733/alignment-files/sam-bam-basics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sam-bam-basics

Generated: 2026-09-23

**Source:** `mrsonord2240/bioSkills@cb48eb16bf63f75098c865da4e8f7bf3191af733:alignment-files/sam-bam-basics`

**Final pass note:** final pass: fixed and audited under one brief, see CHECKPOINT.md

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical — Replay: inspect real human paired-end BAM | 37 | 55 | 92 | 4/4 | ✅ |
| 2 | Variant A — Replay: conversion and CRAM/BAM compatibility | 37 | 55 | 92 | 4/4 | ✅ |
| 3 | Edge — Replay: SAM fields, CIGAR, flags and boundaries | 37 | 54 | 91 | 4/4 | ✅ |
| 4 | Variant B — Replay: CRAM reference-resolution states | 37 | 55 | 92 | 4/4 | ✅ |
| 5 | Stress — Replay: aligner MAPQ, tags and provenance | 35 | 54 | 89 | 4/4 | ✅ |
| 6 | Stress — Replay: multi-region de-duplication | 38 | 56 | 94 | 4/4 | ✅ |
| 7 | Edge — Replay: view_bam.py input matrix | 37 | 55 | 92 | 4/4 | ✅ |
| 8 | Adversarial — Replay: lossless versus lossy CRAM expectations | 37 | 56 | 93 | 4/4 | ✅ |
| 9 | Variant B — Fresh: NH:i featureCounts multimapper handling | 38 | 57 | 95 | 4/4 | ✅ |
| 10 | Adversarial — Fresh: unordered and malformed BED for fetch_regions | 34 | 50 | 84 | 3/4 | ✅ |

**Execution Average:** 91.4/100  
**Assertion Pass Rate:** 39/40

## Veto Gates

- Skill Veto T1–T4: PASS.
- Research Veto M1–M4: PASS.

## Detailed Outputs

### Input 1 — Replay: inspect real human paired-end BAM

**Executed:** yes. Executed: samtools 1.24, pysam 0.24.1 and Rsamtools 2.22.0; current source copy in run/skill.

**Result:** Replayed samtools/pysam/Rsamtools inspection, flags, coordinates, count and shipped view helper on the 5,644-record human BAM.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] Canonical BAM counts, FLAG decoding and coordinate conversions agree with independent checks — All recorded assertions for input 1 passed.
- [PASS] view_bam.py works for indexed and unindexed BAM and labels 0-based coordinates — Replay output reports identical mapped/unmapped counts by index and scan.
- [PASS] The shipped SAM example parses with samtools — Regression check passed.
- [PASS] Usage guide pointers resolve to the compact current Skill layout — Source files present and referenced.

### Input 2 — Replay: conversion and CRAM/BAM compatibility

**Executed:** yes. Executed: current convert_formats.sh with SAM, BAM and CRAM fixtures.

**Result:** Replayed format conversions, input/output protection and reference-dependent CRAM reads.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] SAM/BAM/CRAM conversions preserve expected record counts — Regression assertions passed.
- [PASS] CRAM input requires and uses the supplied reference — Decode checks passed.
- [PASS] Input equals output is refused without destroying the input — Regression assertion passed.
- [PASS] Uppercase output extension is accepted — Regression assertion passed.

### Input 3 — Replay: SAM fields, CIGAR, flags and boundaries

**Executed:** yes. Executed: seeded 15-record synthetic fixture and reference model.

**Result:** Replayed seeded synthetic SAM/BAM checks against independent SAM-spec calculations.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100

**Assertions:**
- [PASS] CIGAR query/reference consumption matches the independent model — Regression assertions passed.
- [PASS] Primary and supplementary/secondary FLAG behavior is correct — Regression assertions passed.
- [PASS] 0-based pysam and 1-based samtools region boundaries are distinguished — Regression assertions passed.
- [PASS] Malformed/missing file cases are rejected by view_bam.py — Regression assertions passed.

### Input 4 — Replay: CRAM reference-resolution states

**Executed:** yes. Executed: samtools full-decode and independent column comparison.

**Result:** Replayed reachable, absent, REF_PATH, REF_CACHE, wrong-reference and embedded-reference CRAM states on a second real dataset.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] Full decode, rather than count or quickcheck, detects an unreachable CRAM reference — Recorded reference-state checks passed.
- [PASS] REF_PATH and REF_CACHE recipes decode the CRAM offline — Recorded checks passed.
- [PASS] Wrong reference is refused unless MD5 checking is explicitly disabled — Recorded checks passed.
- [PASS] Embedded-reference CRAM decodes without a reachable external reference — Recorded checks passed.

### Input 5 — Replay: aligner MAPQ, tags and provenance

**Executed:** yes. Executed: real and seeded aligner data. DRAGEN and Cell Ranger remain explicitly unexecuted because they are licensed/registration-gated.

**Result:** Replayed BWA, minimap2, Bowtie2, HISAT2 and STAR behavior, optional tags, markdup prerequisites, and CRAM CIGAR/tag changes.

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] Runnable aligner MAPQ scales and STAR sentinel behavior match the table — Recorded checks passed.
- [PASS] Runnable tag and @PG provenance claims match produced BAMs — Recorded checks passed.
- [PASS] markdup fails loudly when required fixmate tags are absent — Recorded check passed.
- [PASS] CRAM round trip changes =/X and MD/tag representation as documented — Recorded checks passed.

### Input 6 — Replay: multi-region de-duplication

**Executed:** yes. Executed: samtools -M/-L/--region-file and current shipped fetch_regions.py.

**Result:** Replayed 60 random real-BAM region sets plus synthetic cases against a full-scan truth after adapting the regression harness to the moved scripts/fetch_regions.py.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:**
- [PASS] Multi-region samtools commands equal full-scan truth — All 60 random sets passed.
- [PASS] fetch_regions returns each matching record exactly once — All 60 random sets passed.
- [PASS] Default separate region queries can duplicate overlapping reads — Observed in 19 meaningful random sets.
- [PASS] The moved helper imports from scripts/ — Current source module imported and ran.

### Input 7 — Replay: view_bam.py input matrix

**Executed:** yes. Executed: current examples/view_bam.py against the fixture matrix.

**Result:** Replayed SAM, indexed/unindexed BAM, CRAM with/without reference, empty input, missing file, truncated input and nonnumeric limit behavior.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] Counts are correct for indexed and scan-only formats — Recorded matrix checks passed.
- [PASS] CRAM reference omission produces a friendly actionable error — Recorded matrix check passed.
- [PASS] Nonnumeric limit produces usage and exit 1 — Recorded matrix check passed.
- [PASS] Missing and malformed inputs exit nonzero without an uncaught traceback — Recorded matrix checks passed.

### Input 8 — Replay: lossless versus lossy CRAM expectations

**Executed:** yes. Executed: current reference file recipe plus real SARS-CoV-2 and minimap2 fixtures.

**Result:** Replayed CRAM-read states and minimap2 eqx/MD transformations after adapting the regression harness to the moved cram-reference.md.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:**
- [PASS] The documented cache recipe runs verbatim after substituting fixture paths — Recorded check passed.
- [PASS] The recommended full-decode command proves reference reachability — Recorded check passed.
- [PASS] CRAM round trip is accurately disclosed as non-byte-lossless — Recorded checks passed.
- [PASS] Current reference-file split is exercised rather than treated as a missing section — Harness was updated only for the post-split location.

### Input 9 — Fresh: NH:i featureCounts multimapper handling

**Executed:** yes. Executed: subread featureCounts 2.0.6 in af-subread; output saved in out/fresh_9_featurecounts_tags.txt.

**Result:** Built a three-alignment synthetic BAM: one NH=1 record and two NH=2 loci; featureCounts default, -M and -M --fraction produced the documented counts.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] Default featureCounts excludes NH>1 alignments — geneA=1, geneB=0 and Unassigned_MultiMapping=2.
- [PASS] featureCounts -M counts all three alignment records — geneA=2, geneB=1.
- [PASS] featureCounts -M --fraction applies 1/NH weights — geneA=1.5, geneB=0.5.
- [PASS] The fresh fixture and scripts are retained in run/ — fresh/fresh_9_featurecounts_tags.sh and data/fresh9 are present.

### Input 10 — Fresh: unordered and malformed BED for fetch_regions

**Executed:** yes. Executed: current scripts/fetch_regions.py; output saved in out/fresh_10_fetch_regions.txt.

**Result:** Unordered overlapping BED exactly matched samtools -M -L (5,426 records, no duplicates). A two-column BED exits 1 but exposes a raw IndexError traceback.

**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100

**Assertions:**
- [PASS] Unordered overlapping BED exactly matches samtools -M -L — 5,426 records, byte-for-byte SAM-line match.
- [PASS] Helper does not duplicate records for overlapping intervals — 5,426 unique records.
- [PASS] Malformed BED is rejected nonzero — The process exits 1.
- [FAIL] Malformed BED receives a concise actionable error rather than a raw traceback — A two-column BED raises uncaught IndexError in read_bed().

## Evidence and Harness Notes

- Prior input replay: `300/300` relevant asserted runnable checks passed; informational notes were not scored.
- Three archived harness predicates intentionally fail only because their old expectations are no longer true: pysam/MAPQ material moved to references, and the former false CRAM-losslessness sentence was corrected. They are not source failures and are retained in raw output for traceability.
- The Phase-1 source split moved helper/reference content; the archived regression harness was adapted only to load the documented current `scripts/` and `references/` locations, then rerun.
- Fresh scripts: `fresh/fresh_9_featurecounts_tags.sh`, `fresh/fresh_10_fetch_regions.py`, and `fresh/run_fresh.sh`.
- The previous report and raw run remain preserved at `F:/OpenScience/audits/_pre-fix-20260923/bio-sam-bam-basics/`.

## Final

**Static:** 90/100 | **Dynamic:** 91.4/100 | **Final:** 91/100 — ⭐ Production Ready | **Deployable:** true

## Recommendations

- [P2] Validate malformed BED rows in `scripts/fetch_regions.py`; current behavior exposes raw `IndexError`.
- [P2] Preserve explicit evidence labels for DRAGEN and Cell Ranger until a licensed instance or real BAM is available.
