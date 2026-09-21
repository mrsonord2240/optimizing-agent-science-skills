> **Audit record for `bio-data-visualization-forest-funnel-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/forest-funnel-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-forest-funnel-plots
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/forest-funnel-plots` (unmodified upstream, extracted with `git archive` into `run/skill/`).
Category: Data Analysis | Mode: A | Complexity: Moderate -> 5 inputs | Executed 5/5 (plus the shipped example).
Environment: `F:\OpenScience\audit-envs\data-visualization\` (`r.sh`, `py.sh`): R 4.4.3, metafor 4.8.0, survminer 0.5.2, MendelianRandomization 0.10.0, ggplot2 4.0.3.
Method: every plotted number was compared with an independent numpy/scipy computation (no metafor) and every PNG in `figs/` was opened.

## Verdict

Static 76/100, execution average 75.2/100, **final 76, Limited Release, deployable, no P0, no veto.**
Step 1 veto PASS (T1-T4). Research veto PASS (M1-M4). Shipped-means-present PASS (SKILL.md, usage-guide.md, examples/forest_phd.R; no `references/`).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: BCG forest (real) | 30 | 44 | 74 | 3/5 | warn |
| 2 | Variant A: funnel/Egger/trim-fill (synthetic k=30) | 34 | 51 | 85 | 4/5 | ok |
| 3 | Edge: k=3 HKSJ (synthetic) | 32 | 47 | 79 | 2/5 | ok |
| 4 | Variant B: Cox forest (lung, real) | 28 | 38 | 66 | 2/5 | partial |
| 5 | Stress: MR forest (ldlc/CHD, real) | 30 | 42 | 72 | 3/5 | warn |

**Execution Average: 75.2 / 100. Assertion pass rate: 14/25. Static 76 x 0.4 = 30.4; dynamic 75.2 x 0.6 = 45.1; final 76.**

## Static (25 criteria)
Functional 7/12, Reliability 7/12, Performance 6/8, Agent usability 13/16, Human usability 7/8, Security 11/12, Maintainability 8/12, Agent-specific 17/20 = 76. Notes are in the JSON.

## Input 1 - Canonical: random-effects forest of 13 real BCG trials
**Prompt:** "Meta-analyse these 13 BCG trials (2x2 counts) with REML random effects, forest plot with a log-scale OR axis, prediction interval, and heterogeneity on the plot."
**Data:** `metafor::dat.bcg` (real, Colditz 1994) -> `data/bcg_logor.csv` (`escalc(measure="OR")`).
**Code:** the SKILL.md `rma` + `forest` block verbatim (`run/in1_bcg_forest.R`), figure `figs/in1_forest_skillmd.png`.
**Output (trimmed):**
```
Random-Effects Model (k = 13; tau^2 estimator: REML)
tau^2 0.3378 (SE 0.1784)  I^2 92.07%  Q(df=12)=163.1649 p<.0001
estimate -0.7452  se 0.1860  ci -1.1098 .. -0.3806
FIT: OR=0.4746 [0.3296, 0.6835]   PRED: OR PI [0.1435, 1.5696]   weights sum 100
```
**Independent check (`run/in1_independent.py`, numpy/scipy):** REML mu -0.745178, se 0.186028, tau2 0.337772, Q 163.1649, FE OR 0.6465 [0.5951, 0.7024]. Identical. (My PI with t_{k-2} differs from metafor's default z-based PI, which equals mu +/- 1.96 sqrt(tau2+se^2) = [0.1435, 1.5696]; the plot uses the latter.)
**What the figure shows (opened):** 13 squares scaled by weight, reference line at 1, ticks 0.25/0.5/1/2/4, right column "0.39 [0.12, 1.26]" etc., pooled diamond 0.47 [0.33, 0.68], PI whisker. **Defects:** (1) the summary row is labelled the literal word `paste`: `bquote(paste(...))` is a `call`, not an expression (`class()` printed `call`), so Q, I2 and tau2 never reach the figure; `run/in1b_mlab_probe.R` shows `as.expression(bquote(...))` prints "RE Model (Q = 163.16, df = 12; I2 = 92.1%)" (`figs/in1_mlab_fixes.png`); (2) `at=` also sets the plotting range, so 7 of 13 CIs and the PI are clipped with arrows.
**Scores:** Basic 30/40 | Specialized 44/60 | Total 74/100
**Assertions:**
- [PASS] Plotted estimates equal independent REML - identical to 6 decimals
- [PASS] Reference line at OR=1, exp axis - yes
- [FAIL] Summary row reports I2, tau2, Q-p - prints "paste"
- [PASS] PI drawn and equal to hand value - yes
- [FAIL] Every CI visible - clipped by `at=`

## Input 2 - Variant A: funnel, Egger, trim-and-fill, contour (synthetic, planted bias)
**Prompt:** "Publication-bias check for 30 studies: funnel plot, Egger test, trim-and-fill as sensitivity, and a contour-enhanced funnel."
**Data (synthetic, seed 20260920):** `data/synthetic_biased_k30.csv` (true log-OR 0.25, tau 0.2, SE 0.08-0.45, only 15% of non-significant studies kept) and `data/synthetic_symmetric_k30.csv` (control, no selection).
**Code:** SKILL.md funnel, `regtest`, `trimfill`, and contour blocks (`run/in2_funnel_asym.R`); independent `run/in2_egger_tf_independent.py`, `run/in2_check.py`.
**Output vs independent:**
```
biased    REML b=0.412806  Egger t=2.9293 df=28 p=0.0067   TF k0=7 adj b=0.3531
symmetric REML b=0.265098  Egger t=-0.7120 df=28 p=0.4824  TF k0=1 adj b=0.2758
numpy:    biased 0.412804 / t=2.9293 p=0.00669 / k0=7 adj 0.3531 ; symmetric 0.265098 / t=-0.7120 p=0.48236 / k0=1 adj 0.2758
```
`funnel()` returned coordinates equal (yi, sei). Funnel centre 0.413; expected pseudo-95% limits at SE 0.441 are [-0.451, 1.277]; the opened image (`figs/in2_biased_funnel.png`) shows them at about -0.46 and 1.28. Contour funnel (`in2_biased_contour.png`): bands symmetric about 0, legend correct, the planted studies pile up right of the bands. Trim-and-fill funnel (`in2_biased_funnel_tf.png`): 7 open circles on the left, centre moved to 0.353.
**Shipped example `forest_phd.R` steps 1-7** (run from a copy, `run/example_run/`): I2=0.0%, Egger t=-4.0137 df=8 p=0.00387, limit estimate 1.3064, trim-and-fill k0=3 adjusted OR 1.44, interaction p 0.406. numpy reproduces Egger (t -4.0137, p 0.00387, b0 1.3064) and trim-and-fill (k0 3, 0.3674, OR 1.444). Its forest also prints "paste" as the summary label (`figs/ex_forest.png`).
**Defect:** `refline = res$b` (a 1x1 matrix) prints four "Recycling array of length 1" warnings from R 4.4.
**Scores:** Basic 34/40 | Specialized 51/60 | Total 85/100
**Assertions:**
- [PASS] Funnel points and centre - equal
- [PASS] Egger detects planted bias, quiet on control - p 0.0067 vs 0.482, both equal numpy
- [PASS] Trim-and-fill k0 and adjusted estimate equal independent - yes
- [PASS] Contour funnel bands correct - yes
- [FAIL] Runs without warnings - refline matrix warnings

## Input 3 - Edge: k=3 trials, HKSJ
**Prompt:** "Only three trials are available. Pool them and show a forest plot; tell me what to report."
**Data (synthetic):** ORs 0.55 / 0.90 / 1.60, SE 0.20 / 0.25 / 0.30 (`data/synthetic_k3.csv`).
**Code:** SKILL.md `rma(... method='REML')` and the HKSJ block verbatim (`run/in3_smallk.R`); independent `run/in3_check.py`.
**Output:**
```
REML  z:  b=-0.1091 ci=[-0.7093, 0.4911]        tau2=0.2187  I2=78.21%  Q(2)=9.07 p=0.0107
HKSJ:     b=-0.1091 se=0.307011 ci=[-1.430062, 1.211864] df=2   (numpy: se 0.307011, same CI)
FE OR 0.803 [0.612, 1.054] ; RE 0.897 [0.492, 1.634] ; HKSJ 0.897 [0.239, 3.360]
regtest at k=3: t=22.3746, df=1, p=0.0284   (no warning)
```
Forest (`figs/in3_forest_k3.png`): three studies, diamond 0.90 [0.24, 3.36], correct.
**Findings:** the tool and the Skill's own patterns print I2 (78.2%) and run Egger at k=3 with no guard although the Skill says not to report I2 below k=5 and to require k>=10 for Egger; "HKSJ well-calibrated even at k=3" is overstated (OR CI 0.24-3.36).
**Scores:** Basic 32/40 | Specialized 47/60 | Total 79/100
**Assertions:**
- [PASS] HKSJ CI equals hand calculation
- [PASS] Forest consistent with model
- [FAIL] k<5 I2 rule surfaced by the code
- [FAIL] Egger at k<10 refused or warned
- [FAIL] HKSJ calibration claim supportable at k=3

## Input 4 - Variant B: Cox forest with ggforest, interaction request
**Prompt:** "Subgroup forest of the treatment HR across stage subgroups from a Cox fit, with the interaction p-value."
**Data (real):** `survival::lung`, complete cases n=227, 164 events; sex as the "treatment" stand-in, ph.ecog as "stage".
**Code:** SKILL.md `coxph` + `ggforest(... cpositions, fontsize, refLabel, noDigits)` block (`run/in4_cox_forest.R`).
**Output:** model HRs Female 0.579 (0.417-0.806), age 1.011 (0.993-1.029), ECOG1 1.507 (1.019-2.228), ECOG2 2.468 (1.578-3.859), ECOG3 7.061 (0.938-53.129). The opened figure (`figs/in4_ggforest.png`) shows exactly these, log axis, reference line 1.
**What was needed but not supplied:** a subgroup forest. By hand: stratum HRs for Female vs Male ECOG0 0.677 (0.309-1.482), ECOG1 0.531 (0.333-0.848), ECOG2 0.683 (0.342-1.364); interaction LRT p 0.893. `ggforest` has arguments `model, data, main, cpositions, fontsize, refLabel, noDigits` and no interaction option. ECOG3 (N=1) is drawn with no warning. The example's step 8 halts: `Error: object 'clinical_df' not found`.
**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100
**Assertions:**
- [PASS] Plotted HRs equal exp(coef)/exp(confint)
- [PASS] Log axis, reference at 1
- [FAIL] Subgroup analysis with interaction p
- [FAIL] Sparse strata flagged
- [FAIL] Shipped example step 8 runs

## Input 5 - Stress: MR forest (real lipid SNPs)
**Prompt:** "MR forest of LDL-C on CHD with IVW, weighted median, mode-based and MR-Egger; report the Egger intercept."
**Data (real):** `MendelianRandomization::ldlc, ldlcse, chdlodds, chdloddsse`, 28 SNPs (`data/mr_ldlc_chd.csv`).
**Code:** the example's step 9 (`run/in5_mr_forest.R`); independent `run/in5_check.py`.
**Output:** IVW 2.834 se 0.530 (numpy IVW 2.834214, residual-scaled se 0.529799); MR-Egger 3.253 se 0.770, intercept -0.0115 p 0.451 (numpy 3.2529, -0.0115); weighted median 2.683. `mr_forest` returns a ggplot. The figure (`figs/in5_mr_forest.png`) is drawn but one SNP (CI to ~380) sets the axis so the four method diamonds are indistinguishable; `snp_estimates = FALSE` (`figs/in5_mr_forest_nosnp.png`) separates them clearly. The usage guide's "annotate per-method p-values" is not something `mr_forest` does. Re-calling `mr_input()` after `mr_input <- mr_input(...)` still works (R skips non-functions), so the shadowing is harmless.
**Scores:** Basic 30/40 | Specialized 42/60 | Total 72/100
**Assertions:**
- [PASS] IVW and MR-Egger equal independent
- [FAIL] Four methods distinguishable in the forest
- [PASS] Egger intercept reported
- [FAIL] Per-method p-values annotated
- [PASS] No over-claim in guidance

## Recommendations
P1: `mlab` prints "paste" (inputs 1, example); ggforest is not a subgroup forest and no interaction code (4); example halts at step 8 (4, 5); small-k guards only in prose and HKSJ overstated (3); MR forest unreadable with an outlier SNP and promised p-value annotation missing (5).
P2: `refline = res$b` warnings; `at=` clips CIs; frontmatter names forestplot/ggforestplot/netmeta/cumul with no code and calls netmeta Bayesian; usage-guide duplicates SKILL.md tips and the example data give I2=0 with a significant Egger p that is not discussed.
Full text in the JSON.

## Files
`run/`: `in1_bcg_forest.R`, `in1_independent.py`, `in1b_mlab_probe.R`, `in2_funnel_asym.R`, `in2_egger_tf_independent.py`, `in2_check.py`, `in3_smallk.R`, `in3_check.py`, `in4_cox_forest.R`, `in5_mr_forest.R`, `in5_check.py`, `build_report.py`, `example_run/` (shipped example and PNG variant), `skill/` (extracted Skill). `figs/` holds every PNG opened. `data/` holds the real-data exports and the labelled-synthetic sets.
