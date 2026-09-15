> **Audit record for `bio-vcf-manipulation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/variant-calling/vcf-manipulation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-manipulation
Generated: 2026-09-11 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:variant-calling/vcf-manipulation`
Category: Data Analysis · Mode A · Complexity: Moderate → N = 5 (merge, concat, isec, subset, header/sort; 3 files).

Environment: bcftools 1.24 (MSYS2 native Windows); bcftools 1.21 (bioconda, micromamba env in WSL `agents`, /tmp) for
Input 3 and the `-R` cross-check. `tr -d '\r'` in scripts only strips the CR the Windows build writes on stdout.

**All data are SYNTHETIC** (`data/make_data.py`, seed 20260911).

## Step 1 — Skill Veto
T1–T4 PASS.

## Step 2 — Static score: 88/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | reheader advised for chr-naming (wrong tool); stale `-R` warning; wrong concat sample-order fix |
| Reliability | 10/12 | Error messages in the table match reality |
| Performance & context | 7/8 | 128-line SKILL.md |
| Agent usability | 15/16 | Excellent by-what-differs table |
| Human usability | 7/8 | |
| Security | 11/12 | |
| Maintainability | 10/12 | Example runs |
| Agent-specific | 18/20 | Good routing |

Shipped-means-present: usage-guide.md, `examples/compare_vcfs.sh` exist. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 2 | Variant A | 37 | 53 | 90 | 3/4 | yes | ✅ |
| 3 | Edge | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 4 | Variant B | 36 | 52 | 88 | 3/4 | yes | ✅ |
| 5 | Stress | 33 | 46 | 79 | 3/4 | yes | ✅ |

**Execution Average: 88.0 / 100** · **Assertion Pass Rate: 17/20 (85 %)** · Layer 1 avg 36.2 · Layer 2 avg 51.8

Research Veto: M1–M4 PASS. **Final: 88 × 0.4 + 88.0 × 0.6 = 35.2 + 52.8 = 88.** Assertion-rate floor for Production
Ready (≥ 90 %) not met → **✅ Limited Release**.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have single-sample VCFs for four samples from our per-sample pipeline. Merge them into a cohort VCF; my
colleague says add -0 so we don't get missing genotypes."
**Code (runs/in1/run.sh):** single-sample files = each sample's non-ref sites from the joint call (`view -s -c 1`);
`bcftools merge -l files.txt` and `merge -0`; compare with the joint call of the same samples.
**Printed:**
```
sites per single-sample file: 197 121 124 84
truth4:    sites=305 missing_GT=62  hom_ref=632
merged:    sites=305 missing_GT=694 hom_ref=0
merged_m0: sites=305 missing_GT=0   hom_ref=694
merged:    concordant 588/1220, ./. placeholders 632
merged_m0: concordant 1158/1220, 0/0 fabricated where truth is ./. 62
sites with different AF (joint vs default ./.): 274  inflated: 274
```
Interpretation: both fills are guesses — `./.` inflates AF, `-0` invents hom-ref where SYN_S6 had no reads; build the
cohort by joint-genotyping gVCFs (joint-calling).
**Scores:** 38 + 55 = **93** · **Assertions 4/4.**

### Input 2 — Variant A
**Prompt:** "Stitch my per-chromosome files into one genome VCF; they're big, can I use --naive? Also combine two
overlapping calling windows."
**Printed (runs/in2/out.txt):**
```
concat == original records: 1cbd1513 vs 1cbd1513
--naive: headers compatible, records=361 ; with reordered samples: "Cannot concatenate, different samples"
plain concat with reordered samples: "Different sample names ... Perhaps bcftools merge"   (so 'drop --naive' is not a fix)
overlap windows: no -a -> 194 records (exit 0, 22 duplicates) ; -a -d exact -> 172 (truth 172)
```
**Scores:** 37 + 53 = **90** · **Assertions 3/4.**

### Input 3 — Edge
**Prompt:** "Compare calls from three callers: what is supported by at least two, what is in all three, and what is
unique to caller A?"
**Printed (runs/in3/out.txt, Linux 1.21):**
```
raw  -n+2: 9   | norm -n+2: 11 | norm -n=3: 8
-C (A only): chr1 1420 GA G  | -n~100: chr1 1420 GA G
compare_vcfs.sh: VCF1 only 4, VCF2 only 1, Shared 8, Overlap with VCF1 66.6%
```
**Scores:** 37 + 53 = **90** · **Assertions 4/4.**

### Input 4 — Variant B
**Prompt:** "Extract the four case samples into their own VCF for a burden test; make sure the INFO counts are right.
I'll restrict to my target BED, which has overlapping intervals."
**Printed:**
```
sub_default:  AC wrong 0,   AN wrong 0,   AF wrong 277
sub_noupdate: AC wrong 233, AN wrong 361, AF wrong 277
sub_filltags: AC wrong 0,   AN wrong 0,   AF wrong 0
-R overlap.bed: 80 (distinct 80) ; -T: 80 ; Linux 1.21 identical
```
**Scores:** 36 + 52 = **88** · **Assertions 3/4** (FAIL: `-R` duplication warning not reproducible).

### Input 5 — Stress
**Prompt:** "Merge batch1 and batch2. Batch2 came from another centre (1/2 instead of chr1/chr2, and a sample label that
clashes). A third file is unsorted. Get me one clean cohort."
**Printed (runs/in5/out.txt):**
```
naive merge: Error: Duplicate sample names (SYN_S1), use --force-samples to proceed anyway.
after reheader -f ref.fa.fai: header contigs 2, body CHROMs still 1, 2 ; merge exit 0 -> 722 rows (chr1 172, 1 172, chr2 189, 2 189)
annotate --rename-chrs: merged 361 sites x 8 samples; equals joint: a2805164 vs a2805164
unsorted: index: failed to create index ; bcftools sort -T ./tmp -m 100M -> sorted+indexed records: 361
```
Interpretation: the Skill's instruction to fix chr1-vs-1 with reheader produced a silently doubled cohort; the record
rename needs `bcftools annotate --rename-chrs` (covered only in variant-annotation's usage guide).
**Scores:** 33 + 46 = **79** · **Assertions 3/4.**

## Recommendations
- **[P1]** Replace "fix contig naming with reheader" with `bcftools annotate --rename-chrs` (Input 5).
- **[P2]** Fix the concat sample-order advice (Input 2).
- **[P2]** Qualify or drop the `-R` duplicate-record warning (Input 4).
