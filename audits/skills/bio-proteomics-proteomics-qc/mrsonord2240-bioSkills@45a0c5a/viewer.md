> **Audit record for `bio-proteomics-proteomics-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@45a0c5a](https://github.com/mrsonord2240/bioSkills/tree/45a0c5a65b7346d47a7b72b6d0a6eb60ea590317/proteomics/proteomics-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-proteomics-qc
Generated: 2026-09-15 (pass-5 confirmation audit of the FIXED Skill)

Source: `mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:proteomics/proteomics-qc`
(fix commit `95a8460`). **Supersedes the pass-3 report that scored 85.**
Category: Data Analysis · Execution mode: A · Complexity: Complex → N = 8
(7 required; 8 run so the whole pass-3 set survives as regression alongside the two new inputs).
Scripts and captured output: `pass5/`. All six SKILL.md python blocks are extracted programmatically
from the fork path and exec'd unchanged by `pass5/skill.py` — nothing is retyped.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical — MaxQuant LFQ QC + PTXQC with/without Pandoc | 37 | 55 | **92** | 5/5 | yes | ✅ |
| 2 | Variant A — real DIA-NN, 3 runs, no replicates (**the P1 driver**) | 36 | 53 | **89** | 4/5 | yes | ✅ |
| 3 | Variant B — failed loading hidden by MaxLFQ | 37 | 55 | **92** | 4/4 | yes | ✅ |
| 4 | Variant C — TMT channel balance across two plexes | 34 | 51 | **85** | 3/4 | yes | ✅ |
| 5 | Stress — batch fully confounded with condition | 36 | 53 | **89** | 4/4 | yes | ✅ |
| 6 | Edge — suspected sample swap (C2 ↔ T3) | 33 | 50 | **83** | 3/4 | yes | ⚠️ |
| 7 | Reproducibility (**NEW**) — PCA determinism | 38 | 55 | **93** | 5/5 | yes | ✅ |
| 8 | Scope boundary (**NEW**) — partially degenerate 2/1/1 design | 34 | 53 | **87** | 4/5 | yes | ⚠️ |

**Execution Average: 88.8 / 100** · **Assertion Pass Rate: 32/36** · **Executed: 8/8**

**Static: 87/100** (was 83) · **Final = 87 × 0.4 + 88.8 × 0.6 = 88.1** → ⭐ Production Ready,
deployable, **clears the 85 core floor** (was exactly at it). No veto, no P0.

---

## What the fixers claimed, and what I found

| Claim | Verdict | Evidence |
|---|---|---|
| PCA now seeded — six unseeded fits gave six p-values, seeded gives one | **Reproduced exactly** | Wide 20×600 matrix, pre-fix line: PC3 p = 0.56520 / 0.69045 / 0.69205 / 0.69796 / 0.72069 / 0.89537. Fixed function: 1 distinct stdout in 6 calls |
| `replicate_correlation` / `median_cv_linear` raise at n = 1 | **Reproduced** | Both raise `ValueError` naming the group sizes, on the real 3-run DIA-NN report |
| `raw_sample_qc` warns and falls back | **Reproduced** | Warning printed, `baseline` column switched to `ALL`, design limitation stated |
| `f_oneway` prints NOT TESTABLE | **Reproduced** | `PC1 ~ batch: NOT TESTABLE, level sizes [3] … this is not evidence of no batch effect` |
| `createReport()` always produced the PDF; Pandoc adds HTML **only** with `RSTUDIO_PANDOC` set | **Reproduced, both legs run** | Leg A: `pandoc_available() FALSE`, call completes 0.23 min, writes PDF + mzQC + YAML + heatmap, **no** HTML. Leg B: `TRUE`, same call adds a 1,367 kB HTML |
| Confounded design: mean \|log2FC\| 1.55 → 0.00 | **Reproduced** | 1.546 → 0.000 over 104 labelled true-DA proteins |

**New this pass:** the caveats are `print()`-only and never reach the returned objects (Input 8) — filed **P1**.

---

## Detailed Outputs

### Input 1 — Canonical: MaxQuant LFQ QC + the PTXQC row, both Pandoc configurations

```
python blocks: 6      functions: strip_contaminant_rows, raw_sample_qc, contaminant_fraction,
  replicate_correlation, median_cv_linear, geometric_cv_from_log, missingness_profile,
  completeness_filter, pca_batch_check, tmt_channel_balance        <- all exec unchanged

strip_contaminant_rows: 1560 -> 1500 ;  contaminant % of raw Intensity 4.19 - 6.52
replicate r (log2 LFQ): min 0.956 max 0.966
median_cv_linear: Control 24.27% | Treatment 23.57%
pca_batch_check: PC1 ~ batch p=0.0000, PC2 p=0.9597, PC3 p=0.9398

--- A: verbatim, no environment change ---
rmarkdown::pandoc_available(): FALSE     Sys.which("pandoc"): (empty)
  "The 'Pandoc' converter is not installed on your system ... Pandoc is required for HTML reports."
elapsed min 0.23
files: report_v1.1.5_qcA.mzQC  .pdf  .yaml  _filename_sort.txt  _heatmap.txt
HTML exists: FALSE      PDF exists: TRUE          <- the call COMPLETED

--- B: same call, RSTUDIO_PANDOC = pandoc-3.11 ---
pandoc_available(): TRUE | version: 3.11
HTML exists: TRUE | 1367.4 kB      PDF exists: TRUE | 59.2 kB      mzQC: TRUE   heatmap 8 x 13
```

The corrected table row — *"PDF (+ mzQC + YAML; HTML only when Pandoc is reachable)"* — is exactly the
observed file set in both configurations. **92/100**, 5/5.

### Input 2 — Variant A, real DIA-NN, one run per condition (the input that produced the pass-3 P1)

```
REAL DIA-NN report: (4851, 73) | runs: ['A','B','C']

[raw_sample_qc]
WARNING: single-sample group(s) ['A','B','C']: the within-group loading rule cannot fire there, so
those samples are compared to the ALL-sample median instead. A loading difference that tracks
condition is NOT detectable in a design with no replicates.
     n_quantified  total_signal  missing_pct  baseline  fold_total_vs_group  ids_vs_group  flag
A            1607   320818336.0        0.741       ALL                0.901         1.000  False
B            1613   401046592.0        0.371       ALL                1.127         1.004  False
C            1597   355990048.0        1.359       ALL                1.000         0.994  False

[stop conditions with one replicate per condition]
  replicate_correlation -> ValueError: needs >=2 samples in a group; sizes are {'A':1,'B':1,'C':1}.
       With one run per condition there is no replicate reproducibility to measure -- do not report
       "no outliers found".
  median_cv_linear      -> ValueError: CV is undefined with no replicates -- report "not
       measurable", not NaN.
  pca_batch_check       -> PC1 ~ batch: NOT TESTABLE, level sizes [3] (need >=2 levels with >=2
       samples each) -- this is not evidence of no batch effect
```

Every one of the pass-3 silent failures is now loud and correctly worded. Residual: the Level-1
metrics the description advertises still have no code — `RT vs Predicted.RT r = 0.9996–0.9999` and
`median FWHM 0.047–0.050 min` in this output were computed by the auditor, not by the Skill.
**89/100**, 4/5.

### Input 3 — Variant B, failed loading hidden by MaxLFQ
```
proteinGroups_failed.txt | LFQ intensity: flagged []
proteinGroups_failed.txt | Intensity:     flagged ['T4']   fold_total 0.409  ids 0.814
T4 raw log2 median fold vs group: 0.623      after median normalisation all medians: [0.0]
```
The Skill's "apply the rule to TOTAL raw signal and ID count, not the boxplot median" is the
load-bearing instruction, and it still is. **92/100**, 4/4.

### Input 4 — Variant C, TMT channel balance
```
flagged: []            plex B / plex A median channel total: 2.08   (correctly not chased)
positive control (A 128C x0.3) flagged: [['A','128C']] | fold 0.403
PCA raw log2 reporters, batch=plex: PC1 ~ plex p=0.0000
```
**85/100**, 3/4 — the reporter-ion path still has no stated reporting template for the QC decision.

### Input 5 — Stress, batch fully confounded with condition
```
crosstab batch x condition:   day1: Control 4, Treatment 0 ;  day2: Control 0, Treatment 4
before: mean |log2FC| on 104 true DA proteins = 1.546
after batch removal:                            0.000
```
SKILL.md now says *"on a fully confounded synthetic set the mean |log2FC| of 104 truly-changed
proteins went from 1.55 to 0.00 after batch removal. Report the design as non-identifiable and stop;
do not correct, and do not test."* That is the measurement, to the digit. **89/100**, 4/4.

### Input 6 — Edge, sample swap (unchanged gap)
```
raw_sample_qc flags: []                       within-group r: all pairs 0.927 - 0.964
  C2 (Control):   mean centred r own -0.510  other +0.141   <-- better with other group
  T3 (Treatment): mean centred r own -0.508  other +0.132   <-- better with other group
```
The decision tree names the right diagnostic; the Skill ships no code for it, so the auditor wrote the
own-vs-other comparison. **83/100**, 3/4.

### Input 7 — NEW: PCA determinism
**Prompt:** *"Our QC PCA printed one batch p-value yesterday and a different one today on the same
file. Is our data unstable, or is your code?"*

```
(a) FIXED pca_batch_check, 6 identical calls   -> distinct stdout across 6 runs: 1
(b) PRE-FIX PCA(n_components=n_pc), 738x8      -> distinct PC3 p-values: 1   (already stable at this shape)
(c) wide 20 x 600, the shape SKILL.md cites:
    unseeded distinct PC3 p-values: 6  | 0.69796 0.69205 0.69045 0.56520 0.89537 0.72069
    SEEDED (fixed SKILL.md) distinct stdout: 1
```

The defect was real, the fix removes it, and the new Version Compatibility note scopes it correctly to
wide matrices — which also means the fix changes no previously reported small-n result (seeded and
unseeded agree to 6 dp on the 8-sample matrix). **93/100**, 5/5.

### Input 8 — NEW: partially degenerate design (2/1/1), the case the fixer did not test
**Prompt:** *"We have four runs: two controls, one treated, one treated+drug. Run your full QC and
tell me what you can and cannot conclude."*

```
design: {'Control': 2, 'Treated': 1, 'Treated_drug': 1}

raw_sample_qc      WARNING: single-sample group(s) ['Treated','Treated_drug'] ... -> baseline ALL
                   C1/C2 keep the real Control baseline (1.088 / 0.912)
replicate_corr     does NOT raise (one group has 2) ; returns Control C1-C2 r = 0.962314
                   WARNING: no within-group pairs for ['Treated','Treated_drug']; UNCHECKED here
median_cv_linear   Control 16.16% ; Treated NaN ; Treated_drug NaN
                   WARNING: group 'Treated' has 1 sample(s); its CV is NaN (undefined), not low.
pca_batch_check    PC1/PC2/PC3 ~ batch: NOT TESTABLE, level sizes [2, 1, 1]
```

The guards get the untested middle case right: compute what is computable, mark the rest.
**New finding:** every caveat above is a `print()`. The **returned** frame from `median_cv_linear`
still carries a bare `NaN` and `replicate_correlation` simply omits the unchecked groups — an agent
reading the return value (the intended consumer) sees exactly the "NaN reads as clean" ambiguity the
fix set out to remove, one layer down. Filed **P1**. **87/100**, 4/5.

---

## Veto gates

| Gate | Result | Note |
|---|---|---|
| Stability / Contract / Determinism / Security | PASS | Determinism now positively verified (Input 7), not just assumed. |
| M1 Scientific Integrity | PASS | Both quantitative claims added by the fix reproduced independently. |
| M2 Practice Boundaries | PASS | Run/sample-level QC only; no individual-level claim anywhere. |
| M3 Methodological Baseline | PASS | The pass-3 threat (empty/NaN tables reading as "clean") is fixed and verified on real data and on an untested design shape. |
| M4 Code Usability | PASS | 6/6 python blocks exec unchanged, 10/10 functions called; both R legs completed. |

## Recommendations

- **P1 — degenerate-design caveats are `print()`-only and never reach the returned objects.**
  Add a `status` column to `median_cv_linear`, return the unchecked groups from
  `replicate_correlation`, and return the per-PC test status from `pca_batch_check`.
- **P2 — Levels 1–2 and DIA matrix construction are still prose only** (no code or threshold for
  RT/iRT fit or FWHM, though the DIA-NN columns are already loaded).
- **P2 — sample-swap detection is named in the decision tree but has no code.**
- **P2 — no QC report or exclusion-decision template.**
- **P2 — `examples/qc_analysis.py` still states no expected output**, so it cannot self-regress even
  now that it is seeded.
