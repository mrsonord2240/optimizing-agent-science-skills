> **Audit record for `bio-atac-seq-nucleosome-positioning`**
> - Audited working candidate `ce9a8a0618678bc71ab7afa41b98c37beab513e9b0c599d5a83197d31b879cd7`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/nucleosome-positioning), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-nucleosome-positioning`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/nucleosome-positioning) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent. Initial diagnostic audit only; not a certification.
> - Data: ENCODE GM12878 and K562 ATAC chr1:1-30Mb filtered BAMs (ENCSR095QNB, ENCFF415FEC/ENCFF646NWY), GENCODE v29 chr1 protein-coding TSS, and a planted-shift BAM pair derived from GM12878 (truth: +40 bp in chr1:10-12 Mb). Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-nucleosome-positioning

Candidate: `sha256-manifest-v1 ce9a8a0618678bc71ab7afa41b98c37beab513e9b0c599d5a83197d31b879cd7` (7 files), branch `fix/atac-nucleosome-positioning` @ 3186916, re-verified live before and after; no Skill edits.
Category: 3 - Data Analysis - Mode D - Complex, N = 5.
Environment: WSL `science`; lane envs `bio-atac-seq-nucleosome-positioning` (py3.12, pysam 0.24.1, samtools 1.24, bedtools 2.31.1), `-r` (R 4.4.3, ATACseqQC 1.30.0, ChIPpeakAnno 3.40.0), `-nucleoatac37` (py3.7); shared read-only `atac-nucleo` (NucleoATAC 0.3.4, py2.7.15) and `atac-danpos` (danpos3 3.2.4). Fingerprint `0972fade...f866`.
Code: `scripts/a1_py_checks.py`, `a2_r_script.sh` (+ `a2_patched_nucleosome_analysis.R`, `a2_check_bams.sh`), `a3_nucleoatac.sh` (+ `a3_check.py`), `a4_danpos.sh` (+ `a4_make_planted_shift.py`, `a4_check.py`), `a5_pip_install.sh`, root-cause probes `na_debug.py`, `na_cov_probe*.py`, plus tooling-phase scripts `tooling_*`. Output: `logs/`, `out/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (V-plot at TSS) | yes | 30 | 34 | 64 | 3/5 | warn |
| 2 | Variant A (NRL estimate) | failed | 14 | 12 | 26 | 1/3 | fail |
| 3 | Variant B (ATACseqQC R pipeline) | partial | 20 | 22 | 42 | 2/5 | fail |
| 4 | Variant B (NucleoATAC run) | partial | 26 | 26 | 52 | 3/5 | fail |
| 5 | Variant B (DANPOS3 differential, planted shift) | yes | 32 | 44 | 76 | 3/5 | pass |

**Execution Average: 52.0 / 100** - **Assertion Pass Rate: 12/23 (52.2 %)**
**Static: 65/100** - **Final: 57 (Reject)**. Research veto M4 (code usability) FAIL: two of three shipped scripts are not runnable as documented on real data. Deployable: no.

Surface classifications: `vplot.py` (executed, defects), `estimate_nrl.py` (failed), `nucleosome_analysis.R` (failed verbatim; executed with two API fixes in a scratch copy), NucleoATAC run (executed, calling step empty), documented NucleoATAC pip install (failed), DANPOS3 differential and ATAC-tuned recipes (executed), H2A.Z snippet (executed in tooling phase), scPrinter and single-cell route (static-only, no command), Fiber-seq/NanoNOMe (prose, not applicable).

## Input 1 - Canonical: vplot.py at 300 chr1 TSS (GM12878 rep1)

Tooling-phase run (identical bytes) and audit checks (`logs/tooling_smoke_py.log`, `logs/a1_py_checks.log`): grid (600,2000) and total 116,428 equal an independent recount; NFR fragments are 6.80-fold enriched at the TSS centre. Independent checks against true fragment centres:

- 50.0 percent of read1 are reverse; for mono read1 only 50.1 percent have the script's centre equal to the true centre, median error 112 bp for the rest (NUCPOS-004).
- 151 of 300 TSS are minus strand and the script ignores strand. Mono downstream/upstream is 0.48 (plus) and 2.21 (minus) in genome coordinates; strand-unaware pooling reads 1.21, strand-aware 0.46 (NUCPOS-005). See `out/a1_vplot_compare.png`.
- The Skill's go/no-go gate ("V or W recoverable, flat band stop") is read from this plot.

Findings: NUCPOS-004, -005, -014. **Scores:** 30/40 + 34/60 = **64**. Assertions 3/5.

## Input 2 - Variant A: estimate_nrl.py

`estimate_nrl()` and the CLI raise `IndexError` on GM12878 rep1 and on the planted BAM. Root cause: `find_peaks(distance=50)` is 250 bp in 5 bp bins, so only the 42.5 bp NFR peak survives; with `distance=10` the peaks are 42.5, 107.5, 177.5 bp and 177.5 matches the independent mono mode (178 bp) (`logs/a1_py_checks.log`).

Findings: NUCPOS-001. **Scores:** 14/40 + 12/60 = **26**. Assertions 1/3.

## Input 3 - Variant B: nucleosome_analysis.R (ATACseqQC 1.30.0)

Verbatim: counts printed (NFR 28.4, mono 14.7, di 15.6 percent), fragSizeDist PDF written, then `invalid class "GAlignmentsList"` at the shift step (rc 1). Scratch copy with `readBamFile(asMates=TRUE)` and `library(ChIPpeakAnno)` completes (rc 0): heatmap PDF, NFR and mono BAMs, summary CSV (`logs/a2_r_script.log`). Checks on outputs: the NFR BAM has 65,070 of 348,372 records with MAPQ < 30 although counts use MAPQ >= 30 (NUCPOS-008); the heatmap page is uniform zero-coverage colour on the chr1 slice with alt-contig out-of-bound warnings (NUCPOS-009), so readability was not confirmed.

Findings: NUCPOS-002, -003, -008, -009. **Scores:** 20/40 + 22/60 = **42**. Assertions 2/5.

## Input 4 - Variant B: NucleoATAC at TSS-flank regions

`bedtools slop -l 200 -r 1000` on 382 TSS gives 209 merged regions (1.2-3.2 kb); `nucleoatac run` on rep1+rep2 exits 0 (`logs/a3_nucleoatac.log`). Occupancy is well formed (130,082 bp, mean 0.39, values 0-1), 47 NFRs sit a median 83 bp from a TSS, 386 occupancy peaks. `nucpos.bed.gz` is empty. Diagnosis (bounded effort, resolved): wrapping `findAllNucs` shows 26 of 26 candidates that pass coverage and LR filters get z = NaN; `calculateCov` returns exact + garbage (identical inputs give 106.48, 106.95, 107.43 vs exact 0.476) because the Cython source leaves `value` uninitialised; NaN fails `z >= min_z` at any threshold. The documented py3.7 `pip install nucleoatac` fails with "Python version must be 2.7!" (`logs/a5_pip_install.log`).

Findings: NUCPOS-006, -007. **Scores:** 26/40 + 26/60 = **52**. Assertions 3/5.

## Input 5 - Variant B: DANPOS3 differential (planted +40 bp shift)

`danpos dpos trt.bam:ctl.bam --paired 1 --smooth_width 80` (rc 0, 34 s) on GM12878 chr1:10-14 Mb with all pairs in 10-12 Mb shifted +40 bp. `treat2control_dis` median 40 bp (shifted) and 0 bp (unshifted). Skill rule with `point_diff_FDR` < 0.05 and shift >= 30: 90.4 percent of planted positions, 0 false calls; with `smt_diff_FDR` 0 percent (`logs/a4_danpos.log`). The tooling phase also ran the ATAC-tuned recipe (spacing >= 140 bp for 100 percent, `-jd 145` honoured). The executable is `danpos`, not `python danpos.py`.

Findings: NUCPOS-010, -011. **Scores:** 32/40 + 44/60 = **76**. Assertions 3/5.

## Static and general findings

NUCPOS-012 (uncited or inconsistent claims: H2A.Z 10 bp, yeast +1, maintenance date, snippet import), NUCPOS-013 (unresolved "deferred to tooling / unverified" language, version floors), NUCPOS-015 (scPrinter route without a command). Layer 1 average 24.4/40, Layer 2 average 27.6/60. Restricted-access items: none.

## Finding ledger (open)

P0: NUCPOS-001, NUCPOS-002, NUCPOS-003. P1: NUCPOS-004, NUCPOS-005, NUCPOS-006, NUCPOS-007. P2: NUCPOS-008, NUCPOS-009, NUCPOS-010, NUCPOS-011, NUCPOS-012, NUCPOS-013. P3: NUCPOS-014, NUCPOS-015. Full text in `findings.json`.
