> **Audit record for `bio-data-visualization-statistical-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@a74fdbc](https://github.com/mrsonord2240/optimized-scientific-skills/tree/a74fdbc6b6001691903e5051ce36f3fba93bb966/skills/bio-data-visualization-statistical-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-data-visualization-statistical-annotation

Generated: 2026-09-27  
Auditor: independent re-auditor (`meta.auditor_independent=true`)  
Source: `mrsonord2240/optimized-scientific-skills@a74fdbc6b6001691903e5051ce36f3fba93bb966:skills/bio-data-visualization-statistical-annotation`  
Environment: `F:\OpenScience\audit-envs\data-visualization` — R 4.4.3 with ggpubr 1.0.0, ggsignif 0.6.4, rstatix 1.1.0, lme4 2.0.1, emmeans 2.0.3; Python 3.12 with statannotations 0.7.2, seaborn 0.13.2, scipy 1.18.1, statsmodels 0.15.0.

Category 3 Data Analysis, Mode D Hybrid, Complex. This round-two re-audit executed all nine archived prior-audit inputs and two genuinely new follow-up inputs, for 11/11 executed. Every data file is synthetic. The provider worktree was clean at the dispatched commit, and the copied Skill under `run/skill-copy/` was byte-checked against every provider source file before testing.

Static 93/100 | Execution average 95.7/100 | Weighted score 94.6, schema score **95/100** | **⭐ Production Ready** | deployable true | no veto | open P0: 0, P1: 0, P2: 0.

All Production Ready floors pass: static 93 ≥ 80; execution 95.7 ≥ 85; Layer 1 average 38.5/40 ≥ 32; Layer 2 average 57.3/60 ≥ 48; assertions 55/55 = 100% ≥ 90%.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Variant B | 38 | 57 | 95 | 5/5 | ✅ |
| 5 | Stress | 38 | 57 | 95 | 5/5 | ✅ |
| 6 | Scope Boundary | 37 | 55 | 92 | 5/5 | ✅ |
| 7 | Adversarial | 39 | 57 | 96 | 5/5 | ✅ |
| 8 | Variant B — new | 39 | 58 | 97 | 5/5 | ✅ |
| 9 | Adversarial — new | 38 | 56 | 94 | 5/5 | ✅ |
| 10 | Edge — new round 2 | 39 | 59 | 98 | 5/5 | ✅ |
| 11 | Variant B — new round 2 | 39 | 59 | 98 | 5/5 | ✅ |

**Execution Average: 95.7 / 100**  
**Assertion Pass Rate: 55 / 55 (100%)**

## Method and Execution Evidence

The nine prior prompts were copied exactly from the archived viewer. Inputs 10 and 11 were written independently after reading the follow-up fixed Skill: a dense six-comparison family requiring automatic and explicit spacing plus honest alternate-display guidance, and a cross-language result-contract check requiring persisted effect type, magnitude, and direction. The re-audit did not reuse the fixer's output as evidence.

The complete command sequence is in `run/run_all.sh`. It generates the new fixtures, runs the copied Skill's R and Python modules, executes the shipped example, independently verifies all tables and pixels, and builds visual contact sheets. Important evidence:

- `run/audit_r.R` — R regressions for inputs 1–11; Holm/Bonferroni/BH checked against `p.adjust`, Tukey against `TukeyHSD`, dense layout coordinates asserted, and every pairwise effect contract parsed.
- `run/audit_python.py` — Python regressions, shuffle-invariant pairing, explicit adjusted values, Welch checked against SciPy, and six signed rank-biserial effects independently reconstructed from Mann-Whitney U.
- `run/output/r_metrics.txt` and `run/output/python_metrics.json` — exact numerical results.
- `run/evidence_manifest.json` — provider commit, byte hashes, image dimensions, nonwhite fractions, and SHA-256 hashes.
- `figs/regression_plots_contact.png` and `figs/new_and_example_plots_contact.png` — visual-inspection sheets. Key plots were also opened individually at original resolution.

The shared Windows R runtime consistently exits with status 139 during process teardown after printing the explicit completion marker. This was not treated as evidence by itself. Each R result counted as executed only because both the audit and shipped regression scripts reached their PASS markers, wrote every expected table/figure, and those artifacts were independently parsed, hashed, and pixel-checked. Python generation, execution, shipped regression, and verification returned status 0.

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** I have Control (n=12), Treatment (n=15) and Vehicle (n=9) expression values, right-skewed. Put Wilcoxon p-value brackets between all pairs on the boxplot with Holm adjustment, as asterisks.

**Output:** The R route returned raw p = 0.1138250, 0.2188480, 0.0054241 and Holm p = 0.2276500, 0.2276500, 0.0162722, giving `ns`, `ns`, `*`. These equal `stats::p.adjust` on the same exact Wilcoxon values. Python's asymptotic Mann-Whitney route returned raw p = 0.1127761, 0.2136207, 0.0072904 and explicit Holm p = 0.2255523, 0.2255523, 0.0218711, equal to statsmodels. The difference is the documented exact-versus-asymptotic algorithm choice, not a correction error. The shipped example completed and placed the omnibus `p = 0.019` above the pairwise stack without overlap.

**Executed:** true — `run/audit_r.R`, `run/audit_python.py`, and `run/skill-copy/examples/statanno_phd.R`.  
**Figures:** `run/output/r_three_group_holm.png`, `run/output/py_three_group_holm.png`, `run/output/example/pairwise-adjusted.png`.  
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100.

Assertions: all 5 PASS — R adjustment equality; Python adjustment equality; correct bracket endpoints; non-overlapping omnibus label; no unsupported or clinical claim.

### Input 2 — Variant A

**Prompt:** Pre/post measurements on 14 subjects (paired by subject_id). Add a paired Wilcoxon p-value to the figure and show the pairing.

**Output:** Both R and Python returned p = 0.0023193359375. A deterministic row shuffle produced the identical p-value and identical figure within each language because both scripts pivot/sort by `subject_id`. Removing one record produced the expected rejection, `time levels do not contain identical complete subject IDs`, rather than a row-order test.

**Executed:** true — original, shuffled, and incomplete fixtures in both languages.  
**Figures:** `run/output/r_paired.png`, `run/output/r_paired_shuffled.png`, `run/output/py_paired.png`, `run/output/py_paired_shuffled.png`, `run/output/example/paired-adjusted.png`.  
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100.

Assertions: all 5 PASS — shuffle invariance; incomplete-pair rejection; subject trajectories; correct displayed p; research boundary.

### Input 3 — Edge

**Prompt:** Three groups, pairwise Mann-Whitney with Holm adjustment on the brackets. Two of my raw p-values are just under 0.05; make sure the figure shows what survives correction.

**Output:** R raw values 0.0421584, 0.00031994, 0.0445526 became 0.0843168, 0.00095982, 0.0843168 under Holm. Python raw values 0.0438455, 0.00031994, 0.0445526 became 0.0876911, 0.00095982, 0.0876911. Both figures show `ns`, `***`, `ns`, so only G1–G3 survives and the two negative comparisons remain visible.

**Executed:** true — both fixed pairwise scripts plus independent R/Python correction calculations.  
**Figures:** `run/output/r_border_holm.png`, `run/output/py_border_holm.png`.  
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100.

Assertions: all 5 PASS — three raw positives versus one adjusted positive; R adjusted labels; Python explicit adjusted labels; negative-result retention; no fabricated statistic.

### Input 4 — Variant B

**Prompt:** Four conditions (A-D), all six pairwise comparisons, Bonferroni or Holm or BH, brackets on the boxplot; also give me the Tukey and Dunn versions.

**Output:** The full family contains six rows in every route. R Holm, Bonferroni, and BH equal `p.adjust`; Python BH equals statsmodels. Dunn-Holm returned significant adjusted p = 0.0021702 and 0.0024519 for the planted effects. Tukey HSD returned 0.00038685 and 0.00034278 for the same effects and all six values matched independent `TukeyHSD` within 1e-8. All brackets were present on distinct vertical rows with expanded y limits.

**Executed:** true — five R routes and one Python BH route.  
**Figures:** `run/output/r_four_holm.png`, `r_four_bonferroni.png`, `r_four_bh.png`, `r_four_dunn.png`, `r_four_tukey.png`, and `py_four_group_bh.png`.  
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100.

Assertions: all 5 PASS — full six-test family; correction equality; Tukey equality; finite Dunn family; all positive and negative comparisons retained.

### Input 5 — Stress

**Prompt:** 8 patients (4 per group) with about 150 cells each. Annotate the violin plot of cell values with the group comparison, without pseudo-replicating.

**Output:** The fixed route validates one group per subject, fits `value ~ group + (1 | subject_id)`, computes the emmeans contrast, and displays Holm-adjusted p = 0.396429. The plot therefore shows the patient-aware null contrast, not the extreme naive cell-level result.

**Executed:** true — `annotate_nested.R` on synthetic `nested.csv`, direct and shipped-example variants.  
**Figures:** `run/output/r_nested.png`, `run/output/example/nested-lmm.png`.  
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100.

Assertions: all 5 PASS — subject clustering; model-based label; membership validation; visible correct bracket; no individual diagnosis.

### Input 6 — Scope Boundary

**Prompt:** Two groups of 5000. Annotate with the exact p and stars, and report the effect size in the caption.

**Output:** The generated R route following the Skill displays `p = 9.615e-07 (****)` and captions `Cohen's d = 0.097`. The exact table stores p = 9.615462389e-07 and d = 0.0973108. This keeps the extremely small p-value separate from the tiny magnitude. The 1040×880 figure is dense but the bracket and caption remain readable.

**Executed:** true — synthetic `bigN.csv`, independent Wilcoxon/effect calculation, saved table, pixel and visual checks.  
**Figure:** `run/output/r_bigN_exact_effect.png`.  
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100.

Assertions: all 5 PASS — displayed p equality; four-star threshold; magnitude present; no overstatement; nonblank readable figure.

### Input 7 — Adversarial

**Prompt:** Just use the ggpubr default test, it is a t-test, right? And give me the Python t-test bracket too.

**Output:** The Skill correctly rejects the premise. Installed ggpubr rendered `Wilcoxon, p = 0.11` for two groups and `Kruskal-Wallis, p = 0.019` for three. The Python Welch route is explicitly named `t-test_welch`; it is not statannotations' Student test `t-test_ind`.

**Executed:** true — built and inspected both default ggpubr plots, extracted their labels, and checked statannotations' Welch result against SciPy.  
**Figures:** `run/output/r_default_two.png`, `run/output/r_default_three.png`.  
**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100.

Assertions: all 5 PASS — Wilcoxon default; Kruskal-Wallis default; correct Welch test name; false premise corrected; no unsupported conclusion.

### Input 8 — Variant B, New

**Prompt:** These two independent groups are approximately normal but have visibly unequal variances and unequal n. Add a Welch bracket in Python, show the exact p-value, and report a small-sample corrected standardized effect size.

**Output:** On the deterministic 22-versus-31 fixture, statannotations' `t-test_welch` returned p = 0.008363188800053285, identical to SciPy `ttest_ind(equal_var=False)` to 1e-12. Student's p was 0.019064584660832905, proving the workflow did not silently use the equal-variance test. The figure caption and result table report Hedges' g = 0.665.

**Executed:** true — new fixture generated by `run/generate_new_data.py`; route executed by `run/audit_python.py`.  
**Figure:** `run/output/py_welch_unequal_variance.png`.  
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100.

Assertions: all 5 PASS — displayed Welch equality; Student test excluded; exact p present; effect magnitude present; synthetic/research scope respected.

### Input 9 — Adversarial, New

**Prompt:** My nested cell dataset accidentally assigns the same `subject_id` to both Control and Treatment. Do not fit or annotate anything if that violates the design; tell me exactly what is wrong.

**Output:** `annotate_nested.R` stopped before model fitting with `each subject_id must belong to exactly one group`. It wrote no plot or partial statistical result. A valid nested fixture reran successfully in the same audit, proving recovery by data correction.

**Executed:** true — new malformed fixture generated by `run/generate_new_data.py`; rejection asserted in `run/audit_r.R`.  
**Figure:** none by design; `must_not_exist_nested.png` was asserted absent.  
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100.

Assertions: all 5 PASS — rejected before modeling; no misleading plot; precise contract error; clean retry path; no fabricated statistic.

### Input 10 — Edge, New Round 2

**Prompt:** I need every one of the six Holm-adjusted comparisons across four groups, but the bracket pyramid must remain readable. Use automatic spacing, show me how a 0.20 override behaves, keep the complete numerical results, and tell me what an alternate compact display would omit.

**Output:** The automatic route returned bracket spacing 0.18, larger than the three-comparison route's 0.12. The explicit route honored 0.20 exactly. In both cases the omnibus position exceeded every bracket position and the plot upper limit exceeded the omnibus position. Both 1040×880 figures showed six distinct rows without clipping. The Skill requires retaining the full result table if a compact-letter or faceted view is used and explicitly warns that a compact display does not show exact per-pair p-values or effects.

**Executed:** true — automatic and explicit-spacing calls in `run/audit_r.R`, layout-coordinate assertions, table parsing, documentation contract check, pixel checks, and original-resolution inspection.  
**Figures:** `run/output/r_four_holm.png`, `run/output/r_four_custom_spacing.png`.  
**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100.

Assertions: all 5 PASS — spacing grows with family size; explicit override honored; upper range reserved; complete table retained with alternate-display limitations; figures readable and unclipped.

### Input 11 — Variant B, New Round 2

**Prompt:** Run the same four-group Holm family in R and Python. Persist `effect_type` and signed `effect_size` for every pair, verify the first-group-positive direction agrees across languages, and also prove the R Tukey route labels its magnitude as Hedges' g rather than a rank effect.

**Output:** Both CSVs contain six ordered rows with `effect_type=rank_biserial_r` and finite signed values. Python values independently equaled `2U/(n1*n2)-1` to 1e-15. R and Python pair order and values agreed within 1e-12: 0.038961, -0.75, -0.428571, -0.772727, -0.474747, and 0.402778. R Dunn rows used rank-biserial r and R Tukey rows used `hedges_g`, matching the documented contract.

**Executed:** true — dedicated Python Holm output, R Holm/Dunn/Tukey outputs, independent SciPy reconstruction, cross-language CSV join, and schema assertions.  
**Figures:** `run/output/py_four_group_effect_contract.png`, `run/output/r_four_holm.png`.  
**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100.

Assertions: all 5 PASS — fields persisted; effect types match methods; values finite and bounded; Python independently reconstructed; R/Python sign direction agrees.

## Visual Inspection

All 25 produced PNGs were parsed and checked for minimum dimensions and nonwhite content. I opened contact sheets for the entire set and original-resolution versions of the key border-Holm, Dunn, nested, big-N, Welch, shipped pairwise, shipped paired, shipped nested, automatic dense-family, and explicit-spacing figures.

Observed results:

- Pairwise endpoints and significance labels agree with their result tables.
- The repaired omnibus label is above the pairwise stack rather than overlapping it.
- Paired subject trajectories visibly connect the same subject across time and are stable after row shuffling.
- The nested figure displays the model-based p = 0.396 rather than a cell-level result.
- The new Welch figure visibly identifies `t-test_welch` and includes exact p and Hedges' g.
- Six-comparison R figures have distinct bracket rows, and both automatic 0.18 and explicit 0.20 spacing remain inside the expanded canvas.
- The cross-language effect-contract figure is visually consistent with the numerical pair family and saved CSV.

## Static Evaluation — 25 Criteria

| Category | Score | Note |
|---|---:|---|
| Functional suitability | 12/12 | Correct runnable pairwise, paired, nested, parametric and non-parametric routes; reusable pairwise tables persist the documented test, correction-family and signed effect contract. |
| Reliability | 9/12 | Major input-integrity guards are clear and reruns deterministic; errors are not structured and singular/degenerate model recovery is not comprehensive. |
| Performance/context | 8/8 | Concise 153-line SKILL.md with logic moved into focused scripts. |
| Agent usability | 16/16 | Test choice, corrections, output files, library traps, family-size-aware spacing, explicit override, and compact alternate-display limitations are explicit. |
| Human usability | 7/8 | Natural triggers and short chooser; a few unsupported data types can still surface package-level errors. |
| Security | 11/12 | No secrets, network, raw-code execution or destructive actions; no explicit output-path scope policy. |
| Maintainability | 12/12 | Focused modules and shipped R/Python regressions. |
| Agent-specific | 18/20 | Strong trigger, progressive disclosure, idempotency and method escape hatches; result schemas differ by language and human handoff guidance is minimal. |

**Static subtotal: 93/100.**

## Veto Gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Operational Stability | PASS | Every requested output completed and was independently verified; no infinite loop, random numerical failure, or unresolved dependency conflict. |
| T2 Structural Consistency | PASS | Required frontmatter is present; shipped files resolve; output tables are consistent within each workflow. |
| T3 Determinism | PASS | Fixed fixtures, explicit comparisons, deterministic corrections, and shuffle-invariant paired results. |
| T4 System Security | PASS | No `eval`/`exec`, command injection, credentials, network calls, or destructive operations. |
| M1 Scientific Integrity | PASS | All numerical claims traced to saved synthetic fixtures and independent calculations. |
| M2 Practice Boundaries | PASS | No diagnosis, prescription, or individual clinical inference. |
| M3 Methodological Ground | PASS | Correct design-aware tests, declared family correction, paired-ID validation, and subject-level nested model. |
| M4 Code Usability | PASS | All eleven inputs produced checked outputs or the intended checked rejection; no syntax error, missing core dependency, or logical loop. |

## Open Recommendations

None. The two prior P2 findings are closed by executed round-two evidence: dense-family spacing and alternate-display guidance pass Input 10, and persisted cross-language effect metadata passes Input 11. Open P0: 0; P1: 0; P2: 0.

## Final

Static 93 × 0.4 = 37.2; execution 95.7 × 0.6 = 57.4; weighted score 94.6, schema score **95/100**. **⭐ Production Ready**, deployable true, veto override false. Open P0: none; P1: none; P2: none.
