# Builds eval_viewer_bio-data-visualization-statistical-annotation.md from run/_viewer_data.json
import json
A = "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
SK = "bio-data-visualization-statistical-annotation"
d = json.load(open(f"{A}/run/_viewer_data.json", encoding="utf-8"))
inputs = d["inputs"]

prompts = {
 1: "I have Control (n=12), Treatment (n=15) and Vehicle (n=9) expression values, right-skewed. Put Wilcoxon p-value brackets between all pairs on the boxplot with Holm adjustment, as asterisks.",
 2: "Pre/post measurements on 14 subjects (paired by subject_id). Add a paired Wilcoxon p-value to the figure and show the pairing.",
 3: "Three groups, pairwise Mann-Whitney with Holm adjustment on the brackets. Two of my raw p-values are just under 0.05; make sure the figure shows what survives correction.",
 4: "Four conditions (A-D), all six pairwise comparisons, Bonferroni or Holm or BH, brackets on the boxplot; also give me the Tukey and Dunn versions.",
 5: "8 patients (4 per group) with about 150 cells each. Annotate the violin plot of cell values with the group comparison, without pseudo-replicating.",
 6: "Two groups of 5000. Annotate with the exact p and stars, and report the effect size in the caption.",
 7: "Just use the ggpubr default test, it is a t-test, right? And give me the Python t-test bracket too.",
}
ex_code = """Scripts (all saved under run/):
  gen_data.py, gen_border.py   SYNTHETIC data with planted effects / a planted null / unequal n  -> data/*.csv
  truth.py                     independent scipy ground truth (Wilcoxon/Welch, Holm, Bonferroni, BH, paired, nested, big-N)
  r1_ggpubr.R, r1b_layers.R    SKILL ggpubr patterns; layer data read with ggplot_build
  r2_example.R                 shipped examples/statanno_phd.R, every top-level expression evaluated in order
  r3_verbatim.R                every ```r block of SKILL.md extracted and run verbatim
  r4_targeted.R, r5_nested.R, r6b.R, r7_pwc.R   rstatix route, formats/thresholds, paired, effect sizes, LMM, Dunn/Tukey, geom_pwc
  py1_statannot.py, py2_formats.py, py3_verbatim.py, py4_fix_paths.py   statannotations
  (r6_more.R stops at a bug in my own manual-Dunn code; r6b.R replaces it)
"""

out = []
o = out.append
o(f"# Eval Viewer - {SK}\n")
o("Generated: 2026-09-20 | Auditor: first audit | Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/statistical-annotation` | Env: `F:\\OpenScience\\audit-envs\\data-visualization` (R 4.4.3: ggpubr 1.0.0, ggsignif 0.6.4, rstatix 1.1.0, lme4, emmeans; Python 3.12: statannotations 0.7.2, seaborn 0.13.2, scipy 1.18.1)\n")
o("Category 3 Data Analysis, Mode A, Complex -> 7 inputs. Every input executed. All data are SYNTHETIC (planted effects, a planted null, unequal n) in `data/`.\n")
o(f"Static {d['subtotal']}/100 | Execution avg {d['exe']}/100 | **Final {d['final']} {d['grade']}** | not deployable (grade below Limited Release; floors: exec avg < 75, L2 avg 39.9 < 42, assertion pass 50% < 80%) | no veto, no open P0.\n")
o("## Summary Table\n")
o("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|")
for i in inputs:
    o(f"| {i['index']} | {i['type']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['status_flag']} |")
o(f"\n**Execution Average: {d['exe']} / 100**  \n**Assertion Pass Rate: {d['P']}/{d['T']}**\n")
o("## Method\n")
o("Every p-value and star on every figure was compared with an independent scipy / base-R computation of the same test (Mann-Whitney exact vs asymptotic, Welch vs Student, paired vs unpaired, Holm / Bonferroni / BH, the number of comparisons corrected, star cut-offs). For ggplot figures the drawn labels were read from `ggplot_build()` layer data (`annotation` / `label`, `x`/`xend`); for statannotations from `ax.texts` and `Annotation.data.pvalue`; PNGs were opened (all non-blank). Rscript through `r.sh`, Python through `py.sh`.\n")
o("```\n" + ex_code + "```\n")

o("## Key evidence (trimmed output)\n")
o("""```
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
""")
o("Figures opened with the Read tool (all non-blank, brackets on the right groups): `figs/ex_plot1.png` (example, Holm brackets, overlapping Kruskal label), `figs/ex_plot2.png` (ggsignif, NS.), `figs/skillblock3.png`, `figs/py_skill_verbatim.png`, `figs/py_three_group_skill_star.png`, `figs/r4_rstatix_holm4.png`, `figs/r4_paired_fixed.png`, `figs/s1_border_p.signif.png`, `figs/r7_geom_pwc.png`.\n")

o("## Detailed Outputs\n")
for i in inputs:
    o(f"### Input {i['index']} - {i['type']}")
    o(f"**Prompt:** {prompts[i['index']]}\n")
    o(f"**Test:** {i['label']}\n")
    o(f"**Output / finding:** {i['note']}\n")
    o(f"**Executed:** true. {i['execution_note']}\n")
    o(f"**Scores:** Basic: {i['basic']}/40 | Specialized: {i['specialized']}/60 | Total: {i['total']}/100\n")
    o("**Assertions:**")
    for a in i["assertions"]:
        o(f"- [{a['result']}] {a['text']} - {a['note']}")
    o("")

o("## Static evaluation (25 criteria)\n")
rep = json.load(open(f"{A}/eval_report_{SK}_result.json", encoding="utf-8"))
o("| Category | Score | Note |\n|---|---|---|")
for k, v in rep["static_score"]["categories"].items():
    o(f"| {k} | {v['score']}/{v['max']} | {v['note']} |")
o(f"\n**Static subtotal {d['subtotal']}/100.** Skill veto T1-T4 PASS. Research veto M1-M4 PASS (M3 and M4 are close: see recommendations 1, 2 and 4).\n")
o("## Shipped means present (gate 8)\n")
o("`SKILL.md` and `usage-guide.md` point at no `references/`, `scripts/` or `assets/`; the only shipped file, `examples/statanno_phd.R`, exists. The four cross-referenced Skills (`data-visualization/distribution-plots`, `clinical-biostatistics/categorical-tests`, `clinical-biostatistics/effect-measures`, `experimental-design/multiple-testing`) exist at the staging commit. The example reads `df`, `df_paired`, `df_nested` from the session and ships no data.\n")
o("## Research scope (gate 7)\nResearch figure annotation; nothing diagnoses, prescribes or triages an individual.\n")
o("## Recommendations\n")
for r in d["recs"]:
    o(f"**[{r['priority']}] {r['title']}**  \nObserved in: {r['observed_in']}  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
o(f"## Final\n\nStatic {d['subtotal']} x 0.4 = {round(d['subtotal']*0.4,1)}; execution {d['exe']} x 0.6 = {round(d['exe']*0.6,1)}; **{d['final']} - {d['grade']}**; deployable false; veto_override false; open P0: none.\n")
open(f"{A}/eval_viewer_{SK}.md", "w", encoding="utf-8").write("\n".join(out))
print("written")
