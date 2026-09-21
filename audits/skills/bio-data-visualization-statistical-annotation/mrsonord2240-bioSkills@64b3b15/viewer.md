> **Audit record for `bio-data-visualization-statistical-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/statistical-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-statistical-annotation

Generated: 2026-09-20 | Auditor: first audit | Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/statistical-annotation` | Env: `F:\OpenScience\audit-envs\data-visualization` (R 4.4.3: ggpubr 1.0.0, ggsignif 0.6.4, rstatix 1.1.0, lme4, emmeans; Python 3.12: statannotations 0.7.2, seaborn 0.13.2, scipy 1.18.1)

Category 3 Data Analysis, Mode A, Complex -> 7 inputs. Every input executed. All data are SYNTHETIC (planted effects, a planted null, unequal n) in `data/`.

Static 75/100 | Execution avg 68.6/100 | **Final 71.2 Beta Only** | not deployable (grade below Limited Release; floors: exec avg < 75, L2 avg 39.9 < 42, assertion pass 50% < 80%) | no veto, no open P0.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 29 | 39 | 68 | 2/5 PASS | ⚠️ |
| 2 | Variant A | 30 | 42 | 72 | 3/5 PASS | ⚠️ |
| 3 | Edge | 25 | 32 | 57 | 2/5 PASS | ⚠️ |
| 4 | Variant B | 31 | 44 | 75 | 3/5 PASS | ✅ |
| 5 | Stress | 32 | 46 | 78 | 2/4 PASS | ✅ |
| 6 | Scope Boundary | 27 | 38 | 65 | 2/5 PASS | ⚠️ |
| 7 | Adversarial | 27 | 38 | 65 | 3/5 PASS | ⚠️ |

**Execution Average: 68.6 / 100**  
**Assertion Pass Rate: 17/34**

## Method

Every p-value and star on every figure was compared with an independent scipy / base-R computation of the same test (Mann-Whitney exact vs asymptotic, Welch vs Student, paired vs unpaired, Holm / Bonferroni / BH, the number of comparisons corrected, star cut-offs). For ggplot figures the drawn labels were read from `ggplot_build()` layer data (`annotation` / `label`, `x`/`xend`); for statannotations from `ax.texts` and `Annotation.data.pvalue`; PNGs were opened (all non-blank). Rscript through `r.sh`, Python through `py.sh`.

```
Scripts (all saved under run/):
  gen_data.py, gen_border.py   SYNTHETIC data with planted effects / a planted null / unequal n  -> data/*.csv
  truth.py                     independent scipy ground truth (Wilcoxon/Welch, Holm, Bonferroni, BH, paired, nested, big-N)
  r1_ggpubr.R, r1b_layers.R    SKILL ggpubr patterns; layer data read with ggplot_build
  r2_example.R                 shipped examples/statanno_phd.R, every top-level expression evaluated in order
  r3_verbatim.R                every ```r block of SKILL.md extracted and run verbatim
  r4_targeted.R, r5_nested.R, r6b.R, r7_pwc.R   rstatix route, formats/thresholds, paired, effect sizes, LMM, Dunn/Tukey, geom_pwc
  py1_statannot.py, py2_formats.py, py3_verbatim.py, py4_fix_paths.py   statannotations
  (r6_more.R stops at a bug in my own manual-Dunn code; r6b.R replaces it)
```

## Key evidence (trimmed output)

```
ggpubr 1.0.0  ggsignif 0.6.4  rstatix 1.1.0
### border data (planted: raw p 0.0422 / 0.00032 / 0.0446)
independent raw:  0.04216 0.0003199 0.04455    holm: 0.08432 0.0009598 0.08432   raw stars: * *** *   holm stars: ns *** ns
SKILL pattern  stat_compare_means(comparisons=..., p.adjust.method='holm', label='p.signif')  ->  * *** *      <- UNADJUSTED
ggpubr message: `stat_compare_means()` with `comparisons` displays *unadjusted* p-values (no correction for multiple comparisons).
formals(stat_compare_means) has p.adjust.method: FALSE   (compare_means: TRUE)
rstatix pairwise_wilcox_test(holm) -> p.adj 0.0843 0.00096 0.0843   ns *** ns       ggpubr geom_pwc(holm) -> ns *** ns   (both equal independent)

### default method (Skill: 't-test')
stat_compare_means() 2 groups -> "Wilcoxon, p = 0.11"   3 groups -> "Kruskal-Wallis, p = 0.019"   (Welch 0.0808, ANOVA 0.0426)

### statannotations 0.7.2, Mann-Whitney, border data
corr=None   star: ['*','*','***']
corr=holm   star: ['* (ns)','* (ns)','***']   Annotation.data.pvalue = raw 0.04385 0.04455 0.00032   simple/full print raw p
corr=BH     star: ['*','*','***']              (identical to no correction; BH p 0.0446 still <0.05)
corr=bonferroni star: ['ns','ns','***']        Annotation.data.pvalue = 0.13154 0.13366 0.00096 (= raw x 3)
three_group, SKILL block verbatim (holm, star): ['ns','**','ns']   Holm p for Treatment-Vehicle 0.0219 -> '*'
set_pvalues(holm p) -> ['ns','*','ns']      correction_format='replace' -> still ['ns','**','ns']
t-test_ind p 0.04246 = Student; t-test_welch 0.02932 = scipy Welch

### shipped example (statanno_phd.R), three_group
Holm p.adj 0.2277 0.2277 0.01627 -> ns ns *   equals independent      brackets: Control-Treatment, Control-Vehicle, Treatment-Vehicle
wilcox_effsize: 0.310 0.279 0.554 (r)     manual Cliff's delta: -0.367 0.333 0.674     caption says "Cliff d ranges: 0.28-0.55"
Kruskal label at 1.15*max sits on the Control-Vehicle bracket (ex_plot1.png)
section 5: ERROR at [ggpaired(df_paired, ...]: can't find the y.position variable 'y.position' in the data
section 7 (ggsignif): draws NS. NS. ** with three unadjusted pairs right after the Holm step

### paired (n=14): paired Wilcoxon 0.002319 / paired t 0.002123 / unpaired MWU 0.505 / Welch 0.632
rstatix and statannotations on the same rows shuffled: 0.7148  (pairing by row order)

### nested 2 x 4 x 150 cells (planted no group effect)
cell-level wilcox 1.29e-24 (ggpubr draws ****)   lmer+emmeans holm p 0.3964 (KR df=6)   patient means Welch 0.3975   summary(lmer): no p column

### four groups, rstatix holm/bonf/BH == p.adjust (1e-8); subset of 2 pairs, bonferroni: 0.000456 (x2) vs 0.001368 (x6)
tukey_hsd == TukeyHSD (0.000387, 0.000343);  rstatix::dunn_test z,p == manual tie-corrected Dunn
### big N: p 9.6e-07  d -0.097   ggpubr p.format '9.6e-07'; p.signif '****'; ggsignif '***'; p=1e-107 -> 'p < 2e-16'
```

Figures opened with the Read tool (all non-blank, brackets on the right groups): `figs/ex_plot1.png` (example, Holm brackets, overlapping Kruskal label), `figs/ex_plot2.png` (ggsignif, NS.), `figs/skillblock3.png`, `figs/py_skill_verbatim.png`, `figs/py_three_group_skill_star.png`, `figs/r4_rstatix_holm4.png`, `figs/r4_paired_fixed.png`, `figs/s1_border_p.signif.png`, `figs/r7_geom_pwc.png`.

## Detailed Outputs

### Input 1 - Canonical
**Prompt:** I have Control (n=12), Treatment (n=15) and Vehicle (n=9) expression values, right-skewed. Put Wilcoxon p-value brackets between all pairs on the boxplot with Holm adjustment, as asterisks.

**Test:** Three skewed groups, unequal n (12/15/9), Wilcoxon + Holm brackets: SKILL ggpubr, rstatix and statannotations blocks and the shipped example, p and stars vs scipy/base R

**Output / finding:** R exact p 0.1138 / 0.2188 / 0.00542, Holm 0.2277 / 0.2277 / 0.01627 (independent). rstatix and the example's brackets equal these and connect the right groups. The SKILL's ggpubr pattern and its statannotations holm block both print the Treatment-Vehicle bracket as ** (raw p) where the Holm-adjusted p is 0.0163 = *. In the example the Kruskal-Wallis label prints on top of the first bracket.

**Executed:** true. Executed: run/r1_ggpubr.R, r1b_layers.R, r2_example.R, r3_verbatim.R, py1_statannot.py, py3_verbatim.py, truth.py.

**Scores:** Basic: 29/40 | Specialized: 39/60 | Total: 68/100

**Assertions:**
- [PASS] rstatix pairwise_wilcox_test(holm) and the example's Holm p.adj equal independent p.adjust on the same Wilcoxon p - 0.2277 0.2277 0.01627 both ways; unadjusted p equal to 1e-8
- [PASS] Brackets connect the groups named in each comparison and the figure is non-blank - Opened ex_plot1.png, skillblock3.png, py_skill_verbatim.png: Control-Treatment, Control-Vehicle, Treatment-Vehicle in the right positions
- [FAIL] The SKILL's headline ggpubr block (stat_compare_means, comparisons, p.adjust.method='holm', label='p.signif') shows Holm-adjusted stars - Shows raw-p stars (ns, ns, **); Holm gives ns, ns, *. ggpubr 1.0.0 prints 'displays unadjusted p-values' and p.adjust.method is not a formal argument
- [FAIL] The SKILL's statannotations block (Mann-Whitney, holm, star) shows stars equal to the Holm-adjusted p - Texts ns, **, ns; Holm p 0.0219 is *. Holm and BH are 'type 1' corrections that only append '(ns)' when significance is lost, the stars stay raw
- [FAIL] All plots of the shipped example are legible (no overlapping annotation) - 'Kruskal-Wallis, p = 0.019' at label.y = 1.15*max overlaps the Control-Vehicle bracket in ex_plot1.png and skillblock3.png

### Input 2 - Variant A
**Prompt:** Pre/post measurements on 14 subjects (paired by subject_id). Add a paired Wilcoxon p-value to the figure and show the pairing.

**Test:** Paired pre/post (n=14 subjects, planted +2.5 shift, large between-subject variance): paired Wilcoxon and t, unpaired contrast, ggpaired, statannotations

**Output / finding:** Paired Wilcoxon p 0.00232 (scipy, R, rstatix, statannotations Wilcoxon), paired t 0.00212; unpaired 0.51-0.63, so the Skill's 'unpaired n.s., paired significant' row reproduces. The shipped ggpaired + stat_pvalue_manual block errors (no y.position); add_xy_position fixes it and the drawn label is 0.00232. Pairing is by row order, so shuffled rows give p 0.715 in rstatix and statannotations with no message.

**Executed:** true. Executed: run/r4_targeted.R (section 3), py2_formats.py (paired), r2_example.R. SYNTHETIC data/paired.csv.

**Scores:** Basic: 30/40 | Specialized: 42/60 | Total: 72/100

**Assertions:**
- [PASS] Paired Wilcoxon and paired t p from rstatix (paired = TRUE) and statannotations (Wilcoxon, t-test_paired) equal the independent scipy/R values - 0.002319 and 0.002123 in all four
- [PASS] The 'unpaired n.s.; paired significant' reconciliation row reproduces on planted data - unpaired MWU 0.505, Welch 0.632 vs paired 0.0023
- [FAIL] The shipped paired block (ggpaired + stat_pvalue_manual(paired_test, label = 'p.adj')) runs - Error: can't find the y.position variable 'y.position' in the data; a script run with Rscript halts there and never reaches the nested-LMM and ggsignif sections
- [FAIL] The paired tests pair by subject id, not by row order - Same 28 rows shuffled: rstatix p 0.7148, statannotations Wilcoxon 0.7148 vs 0.00232; the Skill only says 'verify pairing'
- [PASS] After adding add_xy_position the ggpaired figure has one connecting line per subject and the bracket label equals the paired p - Opened r4_paired_fixed.png: 14 grey lines, label 0.00232

### Input 3 - Edge
**Prompt:** Three groups, pairwise Mann-Whitney with Holm adjustment on the brackets. Two of my raw p-values are just under 0.05; make sure the figure shows what survives correction.

**Test:** Borderline family: raw p 0.042 / 0.00032 / 0.045 (planted so two pairs lose significance under Holm); ggpubr, statannotations, rstatix, geom_pwc

**Output / finding:** Independent: raw stars * *** *, Holm p 0.084 / 0.00096 / 0.084 = ns *** ns. The SKILL's stat_compare_means Holm pattern draws * *** * (unadjusted). statannotations holm draws '* (ns)' '* (ns)' '***' (raw star plus suffix), BH draws the raw stars with no suffix (BH p 0.0446 is still significant, so that one is right by decision), bonferroni draws ns ns ***. rstatix pairwise_wilcox_test and ggpubr geom_pwc(p.adjust.method='holm') draw ns *** ns. The central promise, adjusted brackets, holds only in the rstatix block and the shipped example's main plot.

**Executed:** true. Executed: run/gen_border.py (SYNTHETIC search for the planted family), r1_ggpubr.R, r1b_layers.R, r4_targeted.R, r6_more.R, r7_pwc.R, py2_formats.py, py4_fix_paths.py.

**Scores:** Basic: 25/40 | Specialized: 32/60 | Total: 57/100

**Assertions:**
- [FAIL] stat_compare_means(comparisons = ..., p.adjust.method = 'holm', label = 'p.signif') shows the Holm-adjusted stars - Draws * *** * (raw); adjusted are ns *** ns. Two of three brackets claim significance the family-wise test does not support
- [FAIL] p.adjust.method is an accepted argument of stat_compare_means - formals(stat_compare_means) has no p.adjust.method (compare_means does); passed via ... it is ignored ('Ignoring unknown parameters' when no comparisons are given)
- [PASS] rstatix pairwise_wilcox_test p.adjust.method 'holm', 'bonferroni', 'BH' equal p.adjust computed independently - four-group data (holm, bonferroni, BH) and border data (holm), all equal to 1e-8; 'fdr' == 'BH' verified
- [PASS] statannotations comparisons_correction='bonferroni' displays p x number of pairs - 0.13154 0.00096 0.13366 = raw x 3; text 'ns', '***', 'ns'
- [FAIL] statannotations comparisons_correction='holm' (the SKILL's choice) displays the Holm-adjusted p or its stars - Displays raw p and raw stars with a ' (ns)' suffix; only set_pvalues() with independently computed Holm p (verified: ns * ns) or 'bonferroni' shows adjusted values

### Input 4 - Variant B
**Prompt:** Four conditions (A-D), all six pairwise comparisons, Bonferroni or Holm or BH, brackets on the boxplot; also give me the Tukey and Dunn versions.

**Test:** Four groups, unequal n (14/11/16/9), six comparisons, planted null (A-B) and two effects: Holm/Bonferroni/BH, Tukey and Dunn routes, family size

**Output / finding:** rstatix Holm/Bonferroni/BH equal p.adjust for all six comparisons and the brackets connect A-C and B-C (**) and the four ns pairs correctly. tukey_hsd equals TukeyHSD; rstatix dunn_test equals a manual tie-corrected Dunn. Two traps are not mentioned: passing a subset of pairs shrinks the corrected family (Bonferroni x2, not x6: 0.000456 vs 0.001368), and statannotations holm shows *** for A-C where Holm p (0.0014 R exact, 0.0031 scipy) is **.

**Executed:** true. Executed: run/r4_targeted.R (sections 1, 1b), r6b.R, py2_formats.py. SYNTHETIC data/four_group.csv.

**Scores:** Basic: 31/40 | Specialized: 44/60 | Total: 75/100

**Assertions:**
- [PASS] rstatix Holm, Bonferroni and BH p.adj equal independent p.adjust for all six comparisons and the ns/** stars follow - holm 0.8931 0.001368 0.3216 0.001927 0.3216 0.3216; stars ns ** ns ** ns ns
- [PASS] Every bracket connects the two groups it is labelled with (xmin/xmax and the drawn segments) - Six brackets, xmin/xmax pairs (1,2)(1,3)(1,4)(2,3)(2,4)(3,4) match group1/group2; r4_rstatix_holm4.png opened
- [PASS] The decision table's Tukey HSD and Dunn routes give correct p when run - rstatix::tukey_hsd == TukeyHSD (0.000387, 0.000343 ...); rstatix::dunn_test z and p equal a manual Dunn to 4 digits
- [FAIL] The SKILL states that the corrected family is the comparisons actually passed, not K(K-1)/2 of all groups - pairwise_wilcox_test(comparisons = 2 pairs, bonferroni) gives raw x 2 (0.000456), statannotations likewise; the text says 'K(K-1)/2 unadjusted p-values' only
- [FAIL] statannotations holm with text_format='star' shows the Holm-adjusted stars on the four-group data - Draws *** *** for A-C and B-C (raw p 0.00052, 0.00087); Holm p is 0.0014-0.0043 (R exact 0.00137/0.00193, scipy 0.0031/0.0043), which is **

### Input 5 - Stress
**Prompt:** 8 patients (4 per group) with about 150 cells each. Annotate the violin plot of cell values with the group comparison, without pseudo-replicating.

**Test:** Nested cells: 2 groups x 4 patients x 150 cells, big patient effect, planted NO group effect

**Output / finding:** Naive cell-level Wilcoxon p 1.29e-24 (ggpubr draws ****); the Skill's LMM and aggregation advice is right: emmeans holm on lmer gives p 0.3964, per-patient Welch 0.3975, per-patient Wilcoxon 0.486. The example's summary(lmer) prints estimate, SE and t but no p-value, and the Skill gives no route to put the correct p on the figure.

**Executed:** true. Executed: run/r5_nested.R. SYNTHETIC data/nested.csv.

**Scores:** Basic: 32/40 | Specialized: 46/60 | Total: 78/100

**Assertions:**
- [PASS] Pseudoreplication is reproduced: the cell-level test is extreme where the patient-level test is null - 1.29e-24 vs 0.397 (patient means)
- [PASS] The example's lmer(value ~ group + (1 | subject_id)) runs and the emmeans holm contrast agrees with the per-patient test - t.ratio 0.913, p 0.3964 (Kenward-Roger) vs Welch on four+four patient means 0.3975
- [FAIL] summary(nested_lmm) as the example ends reports a p-value for the group effect - Coefficients table has Estimate, Std. Error, t value only (lmerTest not loaded); the reader must add emmeans/lmerTest
- [FAIL] The Skill gives a way to annotate the figure with the LMM or aggregated p - Only prose ('LMM is correct'); no code drawing the corrected bracket, so the annotated figure defaults back to the naive test

### Input 6 - Scope Boundary
**Prompt:** Two groups of 5000. Annotate with the exact p and stars, and report the effect size in the caption.

**Test:** Large N, tiny effect (5000 vs 5000, d = 0.097) and the notation the figure uses: exact p, star thresholds, ggsignif labels, effect-size caption

**Output / finding:** Wilcoxon p 9.6e-07, Cohen's d -0.097; ggpubr p.format prints 9.6e-07 (exact) and 'p < 2e-16' for p = 1e-107. The Skill's advice to report effect size is right, but the shipped caption 'Cliff d ranges 0.28-0.55' prints rstatix's r (0.31, 0.28, 0.55) while Cliff's delta is -0.367, 0.333, 0.674. The star table lists three levels; ggpubr and statannotations print **** for p <= 1e-4 (ggsignif stays at ***) and use p <= cut-off; ggsignif prints 'NS.' not the documented 'ns'.

**Executed:** true. Executed: run/r4_targeted.R (sections 2, 5). SYNTHETIC data/bigN.csv.

**Scores:** Basic: 27/40 | Specialized: 38/60 | Total: 65/100

**Assertions:**
- [PASS] label = 'p.format' on p = 9.6e-07 prints that exact p - '9.6e-07'; t-test variant '1.2e-06' equals Welch
- [PASS] The Skill's advice to report effect size gives a small effect for the large-N case - rstatix::cohens_d = -0.0973, manual (mean diff / pooled SD) 0.097
- [FAIL] The example's caption 'Cliff d ranges: min-max' is a Cliff's delta - wilcox_effsize returns r = Z/sqrt(N): 0.310, 0.279, 0.554; manual Cliff's delta -0.367, 0.333, 0.674
- [FAIL] The star table (* < 0.05, ** < 0.01, *** < 0.001) covers what the tools print - ggpubr and statannotations add **** for p <= 1e-4 and treat p == 0.05, 0.01, 0.001 as the higher level (<=); ggsignif caps at ***
- [FAIL] ggsignif map_signif_level = TRUE prints 'ns' for p >= 0.05 as the Skill says - Layer annotation is 'NS.' (ex_plot2.png shows 'NS.')

### Input 7 - Adversarial
**Prompt:** Just use the ggpubr default test, it is a t-test, right? And give me the Python t-test bracket too.

**Test:** 'Use the ggpubr default test / a t-test' request: default-method claim, Python t-test naming, Shapiro-driven test choice on lognormal data

**Output / finding:** ggpubr 1.0.0 stat_compare_means() with no method uses Wilcoxon (two groups, 'Wilcoxon, p = 0.11') and Kruskal-Wallis (three groups, p = 0.019), not the t-test the Skill's headline insight, its ggpubr comment, the Failure Modes section and usage-guide Tip 1 all state; ANOVA would give 0.0426. statannotations 't-test_ind' is Student's (p 0.0425), not the Welch test the decision tree names (0.0293, 't-test_welch'). The Shapiro step the Skill prescribes flags the planted lognormal groups (Treatment p 0.0002) and leads to Wilcoxon, as intended.

**Executed:** true. Executed: run/r1_ggpubr.R (default-method section), py2_formats.py (test names), r2_example.R (Shapiro). SYNTHETIC lognormal data.

**Scores:** Basic: 27/40 | Specialized: 38/60 | Total: 65/100

**Assertions:**
- [FAIL] stat_compare_means() with no method argument runs a t-test (the Skill's stated default) - Two groups: 'Wilcoxon, p = 0.11'; three groups: 'Kruskal-Wallis, p = 0.019'; compare_means default is also wilcox.test
- [FAIL] statannotations 't-test_ind' is the Welch test named in the decision tree - 0.04246 = scipy ttest_ind(equal_var=True); Welch is 0.02932 and needs 't-test_welch'
- [PASS] statannotations 't-test_welch' and rstatix/ggpubr t.test equal scipy/R Welch - 0.02932 and 1.2e-06 both equal independent computations
- [PASS] The Skill's Shapiro-Wilk step flags the planted skewed groups and leads to the rank test - Treatment p 0.00022, Vehicle 0.0155, Control 0.361; Wilcoxon selected in the example
- [PASS] statannotations Mann-Whitney p equals scipy mannwhitneyu (and the R/Python difference is documented) - 0.04385 = scipy auto; R exact gives 0.0422 for the same data, not mentioned

## Static evaluation (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Completeness 3, correctness 2, appropriateness 3. The decision table, FWER arithmetic, pseudoreplication and paired/unpaired guidance are right and reproduce; but the headline ggpubr Holm pattern silently shows unadjusted p, statannotations holm/BH show raw stars, the default-test claim (t-test) is false, and Dunn/Tukey/LMM-on-figure have no code. |
| reliability | 7/12 | Fault tolerance 2, error reporting 2, recoverability 3. Paired tests pair by row order with no guard (shuffled rows: p 0.715 vs 0.0023, silent), the shipped paired section crashes on a missing y.position, and nothing checks that the adjusted family equals the intended one. |
| performance_context | 6/8 | About 270 lines, no references/ layer, and a 85-line usage-guide that repeats SKILL.md tips; small enough that the cost is modest. |
| agent_usability | 11/16 | Learnability 3, consistency 2, feedback design 3, error prevention 3. Failure-mode section is strong on pseudoreplication and selective reporting; internally inconsistent: Holm is the rule but the ggsignif recipe and example section 7 draw unadjusted stars, the table names Dunn but the example uses pairwise Wilcoxon, the caption calls rstatix r 'Cliff d'. |
| human_usability | 7/8 | Discoverability 4 (prompts are natural), forgiveness 3 (unmatched pairing and wrong family size are silently accepted). |
| security | 11/12 | No credentials, eval or network; the example writes stat_annotated.pdf into the cwd. |
| maintainability | 8/12 | Modularity 3, modifiability 3, testability 2. No ground-truth check is shipped for p-values or stars, which is exactly what failed here. |
| agent_specific | 17/20 | Trigger precise, all four cross-referenced Skills exist, re-runs are idempotent, escape hatches (nested -> LMM, survival -> log-rank) are good; no references/ layer. |

**Static subtotal 75/100.** Skill veto T1-T4 PASS. Research veto M1-M4 PASS (M3 and M4 are close: see recommendations 1, 2 and 4).

## Shipped means present (gate 8)

`SKILL.md` and `usage-guide.md` point at no `references/`, `scripts/` or `assets/`; the only shipped file, `examples/statanno_phd.R`, exists. The four cross-referenced Skills (`data-visualization/distribution-plots`, `clinical-biostatistics/categorical-tests`, `clinical-biostatistics/effect-measures`, `experimental-design/multiple-testing`) exist at the staging commit. The example reads `df`, `df_paired`, `df_nested` from the session and ships no data.

## Research scope (gate 7)
Research figure annotation; nothing diagnoses, prescribes or triages an individual.

## Recommendations

**[P1] stat_compare_means(comparisons, p.adjust.method='holm') draws unadjusted p; the argument does not exist**  
Observed in: [1, 3]  
Problem: The headline ggpubr block and the second overall-plus-pairwise block label brackets from raw per-pair tests. On the border data raw stars * *** * are drawn where Holm gives ns *** ns; on the canonical data Treatment-Vehicle shows ** (raw 0.0054) where Holm 0.0163 is *. formals(stat_compare_means) has no p.adjust.method and ggpubr 1.0.0 states that comparisons show unadjusted p. The shipped example's ggsignif section repeats it (three unadjusted wilcox pairs, 'NS.' labels) right after its own Holm step.  
Root cause: The Skill assumes stat_compare_means forwards p.adjust.method to compare_means; it does only for the ref.group route (and then via ... it is ignored).  
Fix: Make the rstatix route the default (pairwise_wilcox_test(p.adjust.method='holm') |> add_xy_position() + stat_pvalue_manual(label='p.adj.signif')) or ggpubr's geom_pwc(method='wilcox_test', p.adjust.method='holm', label='p.adj.signif'), both verified against independent p.adjust; delete p.adjust.method from the stat_compare_means calls and say that comparisons= is unadjusted; for ggsignif pass the adjusted stars via annotations= (manual) rather than test=.

**[P1] statannotations holm and BH do not change the displayed p or stars**  
Observed in: [1, 3, 4]  
Problem: With comparisons_correction='holm' the text is the raw-p star plus ' (ns)' when significance is lost; the SKILL's own block prints ** for a Holm p of 0.0219 (*), and on four groups *** for Holm p 0.0014-0.0043 (**). 'simple' and 'full' print raw p. Only 'bonferroni' rewrites p.  
Root cause: statannotations treats Holm and BH as 'type 1' corrections that reinterpret significance; the Skill presents the option as if it produced adjusted p.  
Fix: Say so, and give the working route: compute adjusted p (scipy/statsmodels multipletests) and call annotator.set_pvalues(adjusted); annotator.annotate() (verified: ns * ns), or use 'bonferroni'.

**[P1] False claim that stat_compare_means defaults to a t-test**  
Observed in: [7]  
Problem: 'The Single Most Important Modern Insight', the '# explicit; default is t-test' comment, the first Failure Mode and usage-guide Tip 1 all say the default is a t-test. ggpubr 1.0.0 defaults to Wilcoxon (two groups) and Kruskal-Wallis (more groups).  
Root cause: Confuses stat_compare_means with t.test; the failure mode 'Symptom: significant t, rank test n.s.' cannot arise from the default.  
Fix: Rewrite the section: the danger is choosing method='t.test' on skewed small-n data, or trusting a Wilcoxon default for paired or nested data without checking; keep the explicit-method advice.

**[P1] Shipped example: paired section crashes, Kruskal label overlaps, 'Cliff d' is r**  
Observed in: [1, 2, 6]  
Problem: Section 5 fails with 'can't find the y.position variable' (stat_pvalue_manual without add_xy_position), so Rscript stops before the LMM and ggsignif sections. In section 4 the Kruskal-Wallis label at 1.15*max sits on the Control-Vehicle bracket, and the caption 'Cliff d ranges 0.28-0.55' prints wilcox_effsize's r (Cliff's delta is -0.37, 0.33, 0.67).  
Root cause: The example was never run end to end, and wilcox_effsize is not Cliff's delta.  
Fix: Pipe paired_test into add_xy_position(x='time'); place the Kruskal label above the top bracket (max(stat_test$y.position) + step) ; caption 'effect size r' or compute Cliff's delta (effsize::cliff.delta or rstatix::wilcox_effsize renamed); source the example on a data file it ships.

**[P1] Paired tests pair by row order, silently**  
Observed in: [2]  
Problem: rstatix pairwise_wilcox_test(paired = TRUE) and statannotations Wilcoxon / t-test_paired have no id argument; the same 28 rows shuffled give p 0.7148 instead of 0.00232 with no message, while ggpaired(id = ) draws the right subject lines, so the figure and the p disagree.  
Root cause: Skill says 'Verify subjects are correctly matched' but ships no check.  
Fix: Add arrange(subject_id) (and an assert that both levels have identical id vectors) before any paired test, in the R and Python recipes.

**[P2] Test-name and label details differ from the tools**  
Observed in: [6, 7]  
Problem: statannotations 't-test_ind' is Student's (0.0425 vs Welch 0.0293, 't-test_welch'); ggsignif prints 'NS.' not 'ns'; ggpubr and statannotations print **** for p <= 1e-4 and use <= at 0.05/0.01/0.001; ggpubr prints 'p < 2e-16', not '<2.22e-16'; R exact and scipy asymptotic Wilcoxon p differ (0.1138 vs 0.1128 at n = 12/15; 0.000228 vs 0.00052 in the tail at n = 14/16) so the R and Python figures of one analysis do not carry identical p.  
Root cause: Version-specific behaviour was not checked against ggpubr 1.0.0 / statannotations 0.7.2 output.  
Fix: Fix the table: add the fourth star and the inclusive boundaries, document the ggsignif labels, name 't-test_welch', and note exact vs asymptotic Wilcoxon.

**[P2] Family size, nested annotation and posthoc code gaps**  
Observed in: [4, 5]  
Problem: The corrected family is the comparisons passed (two pairs x2, not x6) and this is unstated; summary(lmer) shows no p-value and no code draws the LMM/aggregated p on the figure; Dunn is named in the decision table and usage-guide prompt but the example uses pairwise Wilcoxon after Kruskal-Wallis (rstatix::dunn_test works and was verified); the ggsignif block sets two fill colours for a three-group plot and errors on the Skill's own three-group df; Shapiro pre-testing is offered without noting its weakness.  
Root cause: Decision table and code snippets were written separately.  
Fix: State the family-size rule; add a dunn_test/tukey_hsd + stat_pvalue_manual snippet and an emmeans-to-stat_pvalue_manual snippet for nested data; use lmerTest or emmeans for the p.

## Final

Static 75 x 0.4 = 30.0; execution 68.6 x 0.6 = 41.2; **71.2 - Beta Only**; deployable false; veto_override false; open P0: none.
