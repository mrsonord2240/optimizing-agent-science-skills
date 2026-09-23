> **Audit record for `bio-bam-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bc26317](https://github.com/mrsonord2240/bioSkills/tree/bc263173612a0d88214a3c2292d4a9c67f6feb04/alignment-files/bam-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-bam-statistics

Generated: 2026-09-23

## Evaluation context

- Source: `mrsonord2240/bioSkills@bc263173612a0d88214a3c2292d4a9c67f6feb04:alignment-files/bam-statistics`
- Category / mode / complexity: Data Analysis / D / Complex (7 inputs)
- Final-pass exception: `auditor_independent: false`; final pass: fixed and audited under one brief, see CHECKPOINT.md.
- Prior evidence archived unchanged: `F:/OpenScience/audits/_pre-fix-20260922/bio-bam-statistics/`.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical | 38/40 | 57/60 | 95/100 | 4/4 PASS | ✅ |
| 2 | Variant A | 37/40 | 57/60 | 94/100 | 4/4 PASS | ✅ |
| 3 | Edge | 37/40 | 57/60 | 94/100 | 4/4 PASS | ✅ |
| 4 | Variant B | 38/40 | 57/60 | 95/100 | 4/4 PASS | ✅ |
| 5 | Stress | 37/40 | 55/60 | 92/100 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 35/40 | 52/60 | 87/100 | 4/4 PASS | ✅ |
| 7 | Adversarial | 37/40 | 56/60 | 93/100 | 4/4 PASS | ✅ |

**Execution average:** 92.9/100  
**Assertion pass rate:** 28/28 (100%)  
**Static:** 90/100  
**Final:** 92/100 — ⭐ Production Ready — deployable: true  
**Vetoes:** Skill PASS; Research PASS.

## What ran

- Regression scripts: `t0_stability_determinism.sh`, `t1_canonical.sh`, `t2_planted.sh`, `t3_edge.sh`, `t4_depth_cap.sh`, `t5_batch_plots.sh`, and `t6_scope.sh`.
- Fresh scripts: `phase2_fresh_deletion.sh`, `phase2_fresh_source_check.py`, and `phase2_fresh_adversarial.py`.
- Representative checked output: 10/10 deterministic qc_report runs with one distinct output; `BATCH_FAILS 0`; `REGION_TRUTH_MISMATCHES 0`; `SOFTCLIP_MISMATCHES 0`; 11 plot PNGs; MultiQC HTML 2,272,085 bytes; fresh deletion and adversarial assertions all PASS.

## Detailed outputs

### Input 1 — Canonical

**Prompt class:** Human PE BAM and 1000G BAM: flagstat, idxstats, stats, coverage and batch summary

**Execution:** Regression t1_canonical.sh: human and 1000G summaries agree with flagstat/hand-count helpers; chr22-only mitochondrial and sex recipes correctly stop with explicit messages.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] Flagstat-derived counts agree with the saved record-flag helper. — Canonical output includes the expected human and 1000G primary/mapped/proper-pair values.
- [PASS] idxstats missing-contig recipes reject absent chrM and chrX/chrY. — Both cases exited 1 with a message instead of printing a false zero.
- [PASS] The batch summary labels total records and primary fields distinctly. — The 1000G row reports 9601 records, 9595 primary, 9557 primary mapped, and 101 primary duplicates.
- [PASS] Output stays within alignment-QC scope. — Only BAM/CRAM statistical interpretation and tool outputs were produced.

### Input 2 — Variant A

**Prompt class:** Coverage denominators on planted read-less contigs and target regions

**Execution:** Regression t2_planted.sh: region_depth_stats, samtools depth -aa, coverage, and synthetic truth agree across covered and read-less contigs.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:**
- [PASS] Region helper equals independent block-based truth. — t2 reports REGION_TRUTH_MISMATCHES 0 over the tested regions.
- [PASS] Depth -aa retains BED bases on a read-less contig. — 3110 rows versus 2810 with -a alone; chrC contributes 300 rows only with -aa.
- [PASS] Coverage region mean is correct. — chrA:1001-2000 reports mean depth 30, the planted truth.
- [PASS] Empty and boundary behavior is explicit. — The documented zero-denominator and missing-contig paths report errors rather than invent a value.

### Input 3 — Edge

**Prompt class:** Flag categories, empty data, QC-fail data, and insert-size boundaries

**Execution:** Regression t3_edge.sh: Count Reads and qc_report.py agree with flagstat and planted records; CIGAR soft-clip checks also pass under awk and mawk.

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100

**Assertions:**
- [PASS] QC report and Count Reads match flagstat on planted categories. — The saved checker reports zero mismatches for the exercised edge inputs.
- [PASS] Unaligned and all-QC-fail inputs avoid tracebacks and divide-by-zero. — The documented messages and zero-report paths were observed.
- [PASS] Soft-clip output equals an independent CIGAR walk. — t6 records SOFTCLIP_MISMATCHES 0 across real and synthetic inputs.
- [PASS] Insert-size behavior is bounded and disclosed. — The report uses MAX_INSERT and caveat text rather than presenting an unbounded value.

### Input 4 — Variant B

**Prompt class:** Depth caps, mate overlap, and a fresh 20-base deletion test

**Execution:** Regression t4_depth_cap.sh reproduces caps and ARTIC depth truth. Fresh phase2_fresh_deletion.sh independently asserts the clause added in Phase 1.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**
- [PASS] Depth-cap defaults reproduce on the 9500x synthetic stack. — The helper reports mean 1000.0 and max 9500 with the documented raised-cap behavior.
- [PASS] ARTIC depth recipe equals independent block-based truth. — Both report mean 68.8373x and matching threshold/breadth values.
- [PASS] New bcftools deletion claim is exact. — Across del:541-560, samtools mpileup depth is 20 at 20 sites while bcftools INFO/DP and FORMAT/DP are zero at all 20 sites.
- [PASS] Overlap and CIGAR caveats are methodologically explicit. — The skill distinguishes mate overlap conventions and internal CIGAR behavior by tool.

### Input 5 — Stress

**Prompt class:** Fifteen-sample table, plot-bamstats, MultiQC and CRAM/statistics paths

**Execution:** Regression t5_batch_plots.sh: all 15 batch rows pass hand-count validation; plot-bamstats creates 11 PNGs and MultiQC writes a 2.27 MB report.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100

**Assertions:**
- [PASS] All batch rows equal hand-count truth. — t5 records BATCH_FAILS 0 for 15 real and synthetic BAMs.
- [PASS] Report-generation tools produce usable artifacts. — 11 plot PNGs and multiqc_out/multiqc_report.html were created; the report was 2,272,085 bytes.
- [PASS] CRAM reference requirement is exercised rather than assumed. — samtools stats succeeds with --reference and emits controlled reference-loading diagnostics without it.
- [PASS] Command outputs were inspected, not accepted solely on exit status. — Counts, report files, and MultiQC module text were all asserted.

### Input 6 — Scope Boundary

**Prompt class:** Picard targeted-QC and identity/contamination hand-offs

**Execution:** Regression t6_scope.sh: Picard succeeds; VerifyBamID2 and somalier correctly demonstrate the documented dataset limitation rather than fabricating FREEMIX or identity results.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100

**Assertions:**
- [PASS] Picard target metrics run and are plausible. — BedToIntervalList and CollectHsMetrics produced PCT_OFF_BAIT 0 and MEAN_TARGET_COVERAGE 131.05814.
- [PASS] Unavailable end-to-end identity analyses are not represented as completed. — VerifyBamID2 reported no reads in panel regions and somalier failed on absent chr1, matching the documented limitation.
- [PASS] Assay thresholds are explicitly labelled orientation-only. — The table says it is unsourced and not checked on this machine, avoiding false runtime validation.
- [PASS] No diagnosis or treatment recommendation is made. — The skill limits itself to QC metrics and hand-offs.

### Input 7 — Adversarial

**Prompt class:** Fresh qc_report.py error-boundary matrix plus exact-source/fence verification

**Execution:** Fresh phase2_fresh_adversarial.py passes real BAM, uBAM, all-QC-fail, missing file, CRAM without reference, and CRAM with reference. phase2_fresh_source_check.py verifies the copied exact source and 31 fences.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:**
- [PASS] The shipped report handles six adversarial/compatibility cases without a traceback. — All six phase2_fresh_adversarial.py assertions pass with expected rc and message or count.
- [PASS] CRAM missing-reference and provided-reference paths are distinguishable. — No-reference returns rc 1 with a hint; supplied-reference returns rc 0 and primary 5,642.
- [PASS] The evaluated source is the dispatched source. — phase2_fresh_source_check.py byte-compares SKILL.md to the staged worktree.
- [PASS] All bundled runnable fences parse. — 31 total fences are present; 28 bash/python fences pass bash -n or ast.parse; linked references and qc_report.py exist.

## Recommendations

- [P2] Cite the assay thresholds and FREEMIX cut-offs.
- [P2] Add a reproducible whole-genome identity/contamination fixture.
