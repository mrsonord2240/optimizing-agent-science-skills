# Builds eval_report_bio-data-visualization-statistical-annotation_result.json (schema of report_json_schema.md)
import json, os
A = "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
SK = "bio-data-visualization-statistical-annotation"

cats = {
    "functional_suitability": (8, 12, "Completeness 3, correctness 2, appropriateness 3. The decision table, FWER arithmetic, pseudoreplication and paired/unpaired guidance are right and reproduce; but the headline ggpubr Holm pattern silently shows unadjusted p, statannotations holm/BH show raw stars, the default-test claim (t-test) is false, and Dunn/Tukey/LMM-on-figure have no code."),
    "reliability": (7, 12, "Fault tolerance 2, error reporting 2, recoverability 3. Paired tests pair by row order with no guard (shuffled rows: p 0.715 vs 0.0023, silent), the shipped paired section crashes on a missing y.position, and nothing checks that the adjusted family equals the intended one."),
    "performance_context": (6, 8, "About 270 lines, no references/ layer, and a 85-line usage-guide that repeats SKILL.md tips; small enough that the cost is modest."),
    "agent_usability": (11, 16, "Learnability 3, consistency 2, feedback design 3, error prevention 3. Failure-mode section is strong on pseudoreplication and selective reporting; internally inconsistent: Holm is the rule but the ggsignif recipe and example section 7 draw unadjusted stars, the table names Dunn but the example uses pairwise Wilcoxon, the caption calls rstatix r 'Cliff d'."),
    "human_usability": (7, 8, "Discoverability 4 (prompts are natural), forgiveness 3 (unmatched pairing and wrong family size are silently accepted)."),
    "security": (11, 12, "No credentials, eval or network; the example writes stat_annotated.pdf into the cwd."),
    "maintainability": (8, 12, "Modularity 3, modifiability 3, testability 2. No ground-truth check is shipped for p-values or stars, which is exactly what failed here."),
    "agent_specific": (17, 20, "Trigger precise, all four cross-referenced Skills exist, re-runs are idempotent, escape hatches (nested -> LMM, survival -> log-rank) are good; no references/ layer."),
}
subtotal = sum(v[0] for v in cats.values())

def A_(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="Three skewed groups, unequal n (12/15/9), Wilcoxon + Holm brackets: SKILL ggpubr, rstatix and statannotations blocks and the shipped example, p and stars vs scipy/base R",
  note="R exact p 0.1138 / 0.2188 / 0.00542, Holm 0.2277 / 0.2277 / 0.01627 (independent). rstatix and the example's brackets equal these and connect the right groups. The SKILL's ggpubr pattern and its statannotations holm block both print the Treatment-Vehicle bracket as ** (raw p) where the Holm-adjusted p is 0.0163 = *. In the example the Kruskal-Wallis label prints on top of the first bracket.",
  basic=29, specialized=39,
  assertions=[
   A_("rstatix pairwise_wilcox_test(holm) and the example's Holm p.adj equal independent p.adjust on the same Wilcoxon p", True, "0.2277 0.2277 0.01627 both ways; unadjusted p equal to 1e-8"),
   A_("Brackets connect the groups named in each comparison and the figure is non-blank", True, "Opened ex_plot1.png, skillblock3.png, py_skill_verbatim.png: Control-Treatment, Control-Vehicle, Treatment-Vehicle in the right positions"),
   A_("The SKILL's headline ggpubr block (stat_compare_means, comparisons, p.adjust.method='holm', label='p.signif') shows Holm-adjusted stars", False, "Shows raw-p stars (ns, ns, **); Holm gives ns, ns, *. ggpubr 1.0.0 prints 'displays unadjusted p-values' and p.adjust.method is not a formal argument"),
   A_("The SKILL's statannotations block (Mann-Whitney, holm, star) shows stars equal to the Holm-adjusted p", False, "Texts ns, **, ns; Holm p 0.0219 is *. Holm and BH are 'type 1' corrections that only append '(ns)' when significance is lost, the stars stay raw"),
   A_("All plots of the shipped example are legible (no overlapping annotation)", False, "'Kruskal-Wallis, p = 0.019' at label.y = 1.15*max overlaps the Control-Vehicle bracket in ex_plot1.png and skillblock3.png"),
  ], ex="Executed: run/r1_ggpubr.R, r1b_layers.R, r2_example.R, r3_verbatim.R, py1_statannot.py, py3_verbatim.py, truth.py."),
 dict(index=2, type="Variant A", label="Paired pre/post (n=14 subjects, planted +2.5 shift, large between-subject variance): paired Wilcoxon and t, unpaired contrast, ggpaired, statannotations",
  note="Paired Wilcoxon p 0.00232 (scipy, R, rstatix, statannotations Wilcoxon), paired t 0.00212; unpaired 0.51-0.63, so the Skill's 'unpaired n.s., paired significant' row reproduces. The shipped ggpaired + stat_pvalue_manual block errors (no y.position); add_xy_position fixes it and the drawn label is 0.00232. Pairing is by row order, so shuffled rows give p 0.715 in rstatix and statannotations with no message.",
  basic=30, specialized=42,
  assertions=[
   A_("Paired Wilcoxon and paired t p from rstatix (paired = TRUE) and statannotations (Wilcoxon, t-test_paired) equal the independent scipy/R values", True, "0.002319 and 0.002123 in all four"),
   A_("The 'unpaired n.s.; paired significant' reconciliation row reproduces on planted data", True, "unpaired MWU 0.505, Welch 0.632 vs paired 0.0023"),
   A_("The shipped paired block (ggpaired + stat_pvalue_manual(paired_test, label = 'p.adj')) runs", False, "Error: can't find the y.position variable 'y.position' in the data; a script run with Rscript halts there and never reaches the nested-LMM and ggsignif sections"),
   A_("The paired tests pair by subject id, not by row order", False, "Same 28 rows shuffled: rstatix p 0.7148, statannotations Wilcoxon 0.7148 vs 0.00232; the Skill only says 'verify pairing'"),
   A_("After adding add_xy_position the ggpaired figure has one connecting line per subject and the bracket label equals the paired p", True, "Opened r4_paired_fixed.png: 14 grey lines, label 0.00232"),
  ], ex="Executed: run/r4_targeted.R (section 3), py2_formats.py (paired), r2_example.R. SYNTHETIC data/paired.csv."),
 dict(index=3, type="Edge", label="Borderline family: raw p 0.042 / 0.00032 / 0.045 (planted so two pairs lose significance under Holm); ggpubr, statannotations, rstatix, geom_pwc",
  note="Independent: raw stars * *** *, Holm p 0.084 / 0.00096 / 0.084 = ns *** ns. The SKILL's stat_compare_means Holm pattern draws * *** * (unadjusted). statannotations holm draws '* (ns)' '* (ns)' '***' (raw star plus suffix), BH draws the raw stars with no suffix (BH p 0.0446 is still significant, so that one is right by decision), bonferroni draws ns ns ***. rstatix pairwise_wilcox_test and ggpubr geom_pwc(p.adjust.method='holm') draw ns *** ns. The central promise, adjusted brackets, holds only in the rstatix block and the shipped example's main plot.",
  basic=25, specialized=32,
  assertions=[
   A_("stat_compare_means(comparisons = ..., p.adjust.method = 'holm', label = 'p.signif') shows the Holm-adjusted stars", False, "Draws * *** * (raw); adjusted are ns *** ns. Two of three brackets claim significance the family-wise test does not support"),
   A_("p.adjust.method is an accepted argument of stat_compare_means", False, "formals(stat_compare_means) has no p.adjust.method (compare_means does); passed via ... it is ignored ('Ignoring unknown parameters' when no comparisons are given)"),
   A_("rstatix pairwise_wilcox_test p.adjust.method 'holm', 'bonferroni', 'BH' equal p.adjust computed independently", True, "four-group data (holm, bonferroni, BH) and border data (holm), all equal to 1e-8; 'fdr' == 'BH' verified"),
   A_("statannotations comparisons_correction='bonferroni' displays p x number of pairs", True, "0.13154 0.00096 0.13366 = raw x 3; text 'ns', '***', 'ns'"),
   A_("statannotations comparisons_correction='holm' (the SKILL's choice) displays the Holm-adjusted p or its stars", False, "Displays raw p and raw stars with a ' (ns)' suffix; only set_pvalues() with independently computed Holm p (verified: ns * ns) or 'bonferroni' shows adjusted values"),
  ], ex="Executed: run/gen_border.py (SYNTHETIC search for the planted family), r1_ggpubr.R, r1b_layers.R, r4_targeted.R, r6_more.R, r7_pwc.R, py2_formats.py, py4_fix_paths.py."),
 dict(index=4, type="Variant B", label="Four groups, unequal n (14/11/16/9), six comparisons, planted null (A-B) and two effects: Holm/Bonferroni/BH, Tukey and Dunn routes, family size",
  note="rstatix Holm/Bonferroni/BH equal p.adjust for all six comparisons and the brackets connect A-C and B-C (**) and the four ns pairs correctly. tukey_hsd equals TukeyHSD; rstatix dunn_test equals a manual tie-corrected Dunn. Two traps are not mentioned: passing a subset of pairs shrinks the corrected family (Bonferroni x2, not x6: 0.000456 vs 0.001368), and statannotations holm shows *** for A-C where Holm p (0.0014 R exact, 0.0031 scipy) is **.",
  basic=31, specialized=44,
  assertions=[
   A_("rstatix Holm, Bonferroni and BH p.adj equal independent p.adjust for all six comparisons and the ns/** stars follow", True, "holm 0.8931 0.001368 0.3216 0.001927 0.3216 0.3216; stars ns ** ns ** ns ns"),
   A_("Every bracket connects the two groups it is labelled with (xmin/xmax and the drawn segments)", True, "Six brackets, xmin/xmax pairs (1,2)(1,3)(1,4)(2,3)(2,4)(3,4) match group1/group2; r4_rstatix_holm4.png opened"),
   A_("The decision table's Tukey HSD and Dunn routes give correct p when run", True, "rstatix::tukey_hsd == TukeyHSD (0.000387, 0.000343 ...); rstatix::dunn_test z and p equal a manual Dunn to 4 digits"),
   A_("The SKILL states that the corrected family is the comparisons actually passed, not K(K-1)/2 of all groups", False, "pairwise_wilcox_test(comparisons = 2 pairs, bonferroni) gives raw x 2 (0.000456), statannotations likewise; the text says 'K(K-1)/2 unadjusted p-values' only"),
   A_("statannotations holm with text_format='star' shows the Holm-adjusted stars on the four-group data", False, "Draws *** *** for A-C and B-C (raw p 0.00052, 0.00087); Holm p is 0.0014-0.0043 (R exact 0.00137/0.00193, scipy 0.0031/0.0043), which is **"),
  ], ex="Executed: run/r4_targeted.R (sections 1, 1b), r6b.R, py2_formats.py. SYNTHETIC data/four_group.csv."),
 dict(index=5, type="Stress", label="Nested cells: 2 groups x 4 patients x 150 cells, big patient effect, planted NO group effect",
  note="Naive cell-level Wilcoxon p 1.29e-24 (ggpubr draws ****); the Skill's LMM and aggregation advice is right: emmeans holm on lmer gives p 0.3964, per-patient Welch 0.3975, per-patient Wilcoxon 0.486. The example's summary(lmer) prints estimate, SE and t but no p-value, and the Skill gives no route to put the correct p on the figure.",
  basic=32, specialized=46,
  assertions=[
   A_("Pseudoreplication is reproduced: the cell-level test is extreme where the patient-level test is null", True, "1.29e-24 vs 0.397 (patient means)"),
   A_("The example's lmer(value ~ group + (1 | subject_id)) runs and the emmeans holm contrast agrees with the per-patient test", True, "t.ratio 0.913, p 0.3964 (Kenward-Roger) vs Welch on four+four patient means 0.3975"),
   A_("summary(nested_lmm) as the example ends reports a p-value for the group effect", False, "Coefficients table has Estimate, Std. Error, t value only (lmerTest not loaded); the reader must add emmeans/lmerTest"),
   A_("The Skill gives a way to annotate the figure with the LMM or aggregated p", False, "Only prose ('LMM is correct'); no code drawing the corrected bracket, so the annotated figure defaults back to the naive test"),
  ], ex="Executed: run/r5_nested.R. SYNTHETIC data/nested.csv."),
 dict(index=6, type="Scope Boundary", label="Large N, tiny effect (5000 vs 5000, d = 0.097) and the notation the figure uses: exact p, star thresholds, ggsignif labels, effect-size caption",
  note="Wilcoxon p 9.6e-07, Cohen's d -0.097; ggpubr p.format prints 9.6e-07 (exact) and 'p < 2e-16' for p = 1e-107. The Skill's advice to report effect size is right, but the shipped caption 'Cliff d ranges 0.28-0.55' prints rstatix's r (0.31, 0.28, 0.55) while Cliff's delta is -0.367, 0.333, 0.674. The star table lists three levels; ggpubr and statannotations print **** for p <= 1e-4 (ggsignif stays at ***) and use p <= cut-off; ggsignif prints 'NS.' not the documented 'ns'.",
  basic=27, specialized=38,
  assertions=[
   A_("label = 'p.format' on p = 9.6e-07 prints that exact p", True, "'9.6e-07'; t-test variant '1.2e-06' equals Welch"),
   A_("The Skill's advice to report effect size gives a small effect for the large-N case", True, "rstatix::cohens_d = -0.0973, manual (mean diff / pooled SD) 0.097"),
   A_("The example's caption 'Cliff d ranges: min-max' is a Cliff's delta", False, "wilcox_effsize returns r = Z/sqrt(N): 0.310, 0.279, 0.554; manual Cliff's delta -0.367, 0.333, 0.674"),
   A_("The star table (* < 0.05, ** < 0.01, *** < 0.001) covers what the tools print", False, "ggpubr and statannotations add **** for p <= 1e-4 and treat p == 0.05, 0.01, 0.001 as the higher level (<=); ggsignif caps at ***"),
   A_("ggsignif map_signif_level = TRUE prints 'ns' for p >= 0.05 as the Skill says", False, "Layer annotation is 'NS.' (ex_plot2.png shows 'NS.')"),
  ], ex="Executed: run/r4_targeted.R (sections 2, 5). SYNTHETIC data/bigN.csv."),
 dict(index=7, type="Adversarial", label="'Use the ggpubr default test / a t-test' request: default-method claim, Python t-test naming, Shapiro-driven test choice on lognormal data",
  note="ggpubr 1.0.0 stat_compare_means() with no method uses Wilcoxon (two groups, 'Wilcoxon, p = 0.11') and Kruskal-Wallis (three groups, p = 0.019), not the t-test the Skill's headline insight, its ggpubr comment, the Failure Modes section and usage-guide Tip 1 all state; ANOVA would give 0.0426. statannotations 't-test_ind' is Student's (p 0.0425), not the Welch test the decision tree names (0.0293, 't-test_welch'). The Shapiro step the Skill prescribes flags the planted lognormal groups (Treatment p 0.0002) and leads to Wilcoxon, as intended.",
  basic=27, specialized=38,
  assertions=[
   A_("stat_compare_means() with no method argument runs a t-test (the Skill's stated default)", False, "Two groups: 'Wilcoxon, p = 0.11'; three groups: 'Kruskal-Wallis, p = 0.019'; compare_means default is also wilcox.test"),
   A_("statannotations 't-test_ind' is the Welch test named in the decision tree", False, "0.04246 = scipy ttest_ind(equal_var=True); Welch is 0.02932 and needs 't-test_welch'"),
   A_("statannotations 't-test_welch' and rstatix/ggpubr t.test equal scipy/R Welch", True, "0.02932 and 1.2e-06 both equal independent computations"),
   A_("The Skill's Shapiro-Wilk step flags the planted skewed groups and leads to the rank test", True, "Treatment p 0.00022, Vehicle 0.0155, Control 0.361; Wilcoxon selected in the example"),
   A_("statannotations Mann-Whitney p equals scipy mannwhitneyu (and the R/Python difference is documented)", True, "0.04385 = scipy auto; R exact gives 0.0422 for the same data, not mentioned"),
  ], ex="Executed: run/r1_ggpubr.R (default-method section), py2_formats.py (test names), r2_example.R (Shapiro). SYNTHETIC lognormal data."),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    i["assertions_total"] = len(i["assertions"])
    assert 3 <= i["assertions_total"] <= 5
    i["status"] = "COMPLETED"; i["status_flag"] = "\u2705" if i["total"] >= 75 else "\u26a0\ufe0f"
    i["executed"] = True; i["execution_note"] = i.pop("ex")
    i["type"] = i.pop("type")

exe = round(sum(i["total"] for i in inputs) / len(inputs), 1)
P = sum(i["assertions_passed"] for i in inputs); T = sum(i["assertions_total"] for i in inputs)
final = round(subtotal * 0.4 + exe * 0.6, 1)
grade = "Production Ready" if final >= 85 else "Limited Release" if final >= 75 else "Beta Only" if final >= 60 else "Reject"
sym = {"Production Ready": "\u2b50", "Limited Release": "\u2705", "Beta Only": "\u26a0\ufe0f", "Reject": "\u274c"}[grade]
print("static", subtotal, "exec", exe, "final", final, grade, "assertions", P, T)

recs = [
 dict(priority="P1", title="stat_compare_means(comparisons, p.adjust.method='holm') draws unadjusted p; the argument does not exist",
  observed_in=[1, 3], problem="The headline ggpubr block and the second overall-plus-pairwise block label brackets from raw per-pair tests. On the border data raw stars * *** * are drawn where Holm gives ns *** ns; on the canonical data Treatment-Vehicle shows ** (raw 0.0054) where Holm 0.0163 is *. formals(stat_compare_means) has no p.adjust.method and ggpubr 1.0.0 states that comparisons show unadjusted p. The shipped example's ggsignif section repeats it (three unadjusted wilcox pairs, 'NS.' labels) right after its own Holm step.",
  root_cause="The Skill assumes stat_compare_means forwards p.adjust.method to compare_means; it does only for the ref.group route (and then via ... it is ignored).",
  fix="Make the rstatix route the default (pairwise_wilcox_test(p.adjust.method='holm') |> add_xy_position() + stat_pvalue_manual(label='p.adj.signif')) or ggpubr's geom_pwc(method='wilcox_test', p.adjust.method='holm', label='p.adj.signif'), both verified against independent p.adjust; delete p.adjust.method from the stat_compare_means calls and say that comparisons= is unadjusted; for ggsignif pass the adjusted stars via annotations= (manual) rather than test=."),
 dict(priority="P1", title="statannotations holm and BH do not change the displayed p or stars",
  observed_in=[1, 3, 4], problem="With comparisons_correction='holm' the text is the raw-p star plus ' (ns)' when significance is lost; the SKILL's own block prints ** for a Holm p of 0.0219 (*), and on four groups *** for Holm p 0.0014-0.0043 (**). 'simple' and 'full' print raw p. Only 'bonferroni' rewrites p.",
  root_cause="statannotations treats Holm and BH as 'type 1' corrections that reinterpret significance; the Skill presents the option as if it produced adjusted p.",
  fix="Say so, and give the working route: compute adjusted p (scipy/statsmodels multipletests) and call annotator.set_pvalues(adjusted); annotator.annotate() (verified: ns * ns), or use 'bonferroni'."),
 dict(priority="P1", title="False claim that stat_compare_means defaults to a t-test",
  observed_in=[7], problem="'The Single Most Important Modern Insight', the '# explicit; default is t-test' comment, the first Failure Mode and usage-guide Tip 1 all say the default is a t-test. ggpubr 1.0.0 defaults to Wilcoxon (two groups) and Kruskal-Wallis (more groups).",
  root_cause="Confuses stat_compare_means with t.test; the failure mode 'Symptom: significant t, rank test n.s.' cannot arise from the default.",
  fix="Rewrite the section: the danger is choosing method='t.test' on skewed small-n data, or trusting a Wilcoxon default for paired or nested data without checking; keep the explicit-method advice."),
 dict(priority="P1", title="Shipped example: paired section crashes, Kruskal label overlaps, 'Cliff d' is r",
  observed_in=[1, 2, 6], problem="Section 5 fails with 'can't find the y.position variable' (stat_pvalue_manual without add_xy_position), so Rscript stops before the LMM and ggsignif sections. In section 4 the Kruskal-Wallis label at 1.15*max sits on the Control-Vehicle bracket, and the caption 'Cliff d ranges 0.28-0.55' prints wilcox_effsize's r (Cliff's delta is -0.37, 0.33, 0.67).",
  root_cause="The example was never run end to end, and wilcox_effsize is not Cliff's delta.",
  fix="Pipe paired_test into add_xy_position(x='time'); place the Kruskal label above the top bracket (max(stat_test$y.position) + step) ; caption 'effect size r' or compute Cliff's delta (effsize::cliff.delta or rstatix::wilcox_effsize renamed); source the example on a data file it ships."),
 dict(priority="P1", title="Paired tests pair by row order, silently",
  observed_in=[2], problem="rstatix pairwise_wilcox_test(paired = TRUE) and statannotations Wilcoxon / t-test_paired have no id argument; the same 28 rows shuffled give p 0.7148 instead of 0.00232 with no message, while ggpaired(id = ) draws the right subject lines, so the figure and the p disagree.",
  root_cause="Skill says 'Verify subjects are correctly matched' but ships no check.",
  fix="Add arrange(subject_id) (and an assert that both levels have identical id vectors) before any paired test, in the R and Python recipes."),
 dict(priority="P2", title="Test-name and label details differ from the tools",
  observed_in=[6, 7], problem="statannotations 't-test_ind' is Student's (0.0425 vs Welch 0.0293, 't-test_welch'); ggsignif prints 'NS.' not 'ns'; ggpubr and statannotations print **** for p <= 1e-4 and use <= at 0.05/0.01/0.001; ggpubr prints 'p < 2e-16', not '<2.22e-16'; R exact and scipy asymptotic Wilcoxon p differ (0.1138 vs 0.1128 at n = 12/15; 0.000228 vs 0.00052 in the tail at n = 14/16) so the R and Python figures of one analysis do not carry identical p.",
  root_cause="Version-specific behaviour was not checked against ggpubr 1.0.0 / statannotations 0.7.2 output.",
  fix="Fix the table: add the fourth star and the inclusive boundaries, document the ggsignif labels, name 't-test_welch', and note exact vs asymptotic Wilcoxon."),
 dict(priority="P2", title="Family size, nested annotation and posthoc code gaps",
  observed_in=[4, 5], problem="The corrected family is the comparisons passed (two pairs x2, not x6) and this is unstated; summary(lmer) shows no p-value and no code draws the LMM/aggregated p on the figure; Dunn is named in the decision table and usage-guide prompt but the example uses pairwise Wilcoxon after Kruskal-Wallis (rstatix::dunn_test works and was verified); the ggsignif block sets two fill colours for a three-group plot and errors on the Skill's own three-group df; Shapiro pre-testing is offered without noting its weakness.",
  root_cause="Decision table and code snippets were written separately.",
  fix="State the family-size rule; add a dunn_test/tukey_hsd + stat_pvalue_manual snippet and an emmeans-to-stat_pvalue_manual snippet for nested data; use lmerTest or emmeans for the p."),
]

report = {
 "meta": {
  "skill_name": SK,
  "description": "Add p-value brackets, significance asterisks, and effect-size annotations to distribution plots using ggpubr, ggsignif, and statannotations with correct test selection (parametric vs non-parametric vs paired), multiple-testing adjustment, and rendering of negative results. Use when a boxplot/violin/raincloud needs in-figure statistical comparisons between groups.",
  "evaluated_on": "2026-09-20",
  "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis",
  "execution_mode": "A",
  "complexity": "Complex",
  "n_inputs": len(inputs),
  "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/statistical-annotation",
  "audit_type": "first audit",
  "executed": True,
  "execution_note": "Executed 7/7 inputs. Windows R 4.4.3 (ggpubr 1.0.0, ggsignif 0.6.4, rstatix 1.1.0, lme4, emmeans, ggplot2 4.0.3) through r.sh and Python 3.12 (statannotations 0.7.2, seaborn 0.13.2, scipy 1.18.1, matplotlib 3.11.2) through py.sh. Every p-value and star on every figure was compared with an independent scipy or base-R computation (p, Holm/Bonferroni/BH, stars); layer data were read from ggplot_build and Annotator objects and the figures were opened. All data SYNTHETIC with planted effects, a planted null and unequal n. Skill files were extracted with git archive into run/skill; nothing was written into the staging repo. ggpubr 1.0.0 is newer than the 0.6+ the Skill names, so the p.adjust findings are verified on 1.0.0 only."
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated citation or number; references are real (Benjamini-Hochberg 1995, Holm 1979, Dunn 1964, Wasserstein-Lazar 2016). FWER 14/26/54% and Holm >= Bonferroni power verified numerically."},
   "practice_boundaries": {"result": "PASS", "detail": "Statistical annotation of research figures; no diagnostic or prescriptive content."},
   "methodological_ground": {"result": "PASS", "detail": "The stated methodology (test matched to data, Holm, LMM for nesting, effect size) is sound and every number reproduced. The tool recipes that claim to implement it do not always do so (headline ggpubr Holm pattern draws raw p, statannotations Holm stars are raw); recorded as P1 implementation defects with independent evidence, not as a principled fallacy, because the correct rstatix route sits in the same Skill."},
   "code_usability": {"result": "PASS", "detail": "All 4 R and 1 Python SKILL.md blocks parse and run (the ggsignif block needs a two-group df: its two-colour scale errors on the three-group data); the shipped example runs, except the paired section (missing y.position) which stops a Rscript run before its last two sections: recorded P1."},
  },
 },
 "static_score": {"subtotal": subtotal, "max": 100,
   "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": exe, "max": 100, "assertion_pass_rate": {"passed": P, "total": T},
   "inputs": [{k: i[k] for k in ["index","type","label","status","status_flag","note","basic","specialized","total","assertions_passed","assertions_total","assertions","executed","execution_note"]} for i in inputs]},
 "final": {"static_weighted": round(subtotal * 0.4, 1), "dynamic_weighted": round(exe * 0.6, 1), "score": final, "max": 100,
   "grade": grade, "grade_symbol": sym, "deployable": False, "veto_override": False},
 "key_strengths": [
  "The statistical guidance is right where it is prose: test-to-data table, FWER arithmetic, Holm over Bonferroni, pseudoreplication (naive p 1.3e-24 vs LMM 0.396 vs patient-level 0.397 on planted null), paired vs unpaired contrast (0.0023 vs 0.51).",
  "The rstatix route (pairwise_wilcox_test + add_xy_position + stat_pvalue_manual) matches independent Holm, Bonferroni and BH to 1e-8 with correct brackets on 3 and 4 groups; the shipped example's main plot is correct.",
  "The Failure Modes section names the real traps (unadjusted pairs, pseudoreplication, hidden n.s., p without effect size); Tukey and Dunn routes named in the table give correct p.",
 ],
 "recommendations": recs,
}
report["final"]["floors_note"] = None
del report["final"]["floors_note"]
json.dump(report, open(f"{A}/eval_report_{SK}_result.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
json.dump({"inputs": inputs, "subtotal": subtotal, "exe": exe, "final": final, "grade": grade, "P": P, "T": T, "recs": recs}, open(f"{A}/run/_viewer_data.json", "w", encoding="utf-8"), ensure_ascii=False)
L1 = sum(i["basic"] for i in inputs) / len(inputs); L2 = sum(i["specialized"] for i in inputs) / len(inputs)
print("L1 avg", round(L1, 1), "L2 avg", round(L2, 1), "assert rate", round(P / T, 2))
