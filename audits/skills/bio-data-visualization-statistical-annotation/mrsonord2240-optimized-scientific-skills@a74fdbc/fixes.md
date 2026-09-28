# 2026-09-27 - bio-data-visualization-statistical-annotation

Source fixed in `F:\OpenScience\wt\backlog-statistical-annotation` on branch `fix/backlog-statistical-annotation`. Audit fixtures under `F:\OpenScience\audits\bio-data-visualization-statistical-annotation\data` remained unchanged. Runtime: R 4.4.3 with ggpubr 1.0.0, ggsignif 0.6.4, rstatix 1.1.0, lme4 2.0.1, emmeans 2.0.3; Python 3.12 with statannotations 0.7.2, seaborn 0.13.2, scipy 1.18.1, statsmodels 0.15.0.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `stat_compare_means(comparisons, p.adjust.method='holm')` draws raw p | P1 | Made rstatix compute-adjust-position plus `stat_pvalue_manual()` the R default; explicitly marked the ggpubr pattern invalid; changed ggsignif to manual adjusted annotations | ran `annotate_pairwise.R` on `border.csv`: Holm 0.0843168, 0.000959824, 0.0843168 and labels `ns`, `***`, `ns`; repaired example ran end to end and its figure was opened | `stat_compare_means()` remains only for the omnibus label, positioned above the highest bracket |
| statannotations Holm/BH display raw p/stars | P1 | Added `scripts/annotate_pairwise.py`: compute raw Mann-Whitney p, adjust with `multipletests`, then call `set_pvalues(adjusted)` | ran on `border.csv`: adjusted 0.0876911, 0.000959824, 0.0876911; plot 1040x880, non-white fraction 0.116; visually opened via the repaired example's equivalent R output | Built-in Bonferroni is documented as the only named route here that rewrites p; Holm/BH type-1 behavior is explicit |
| False claim that ggpubr defaults to t-test | P1 | Corrected ggpubr 1.0.0 defaults to Wilcoxon (two groups) / Kruskal-Wallis (more groups); reframed advice around explicit design choice | ran package/version probe and the audit's prior default-method execution supports the corrected statement | Also named statannotations `t-test_welch`; `t-test_ind` is Student's |
| Shipped example crashes; omnibus label overlaps; r called Cliff d | P1 | Rebuilt the example around sourced scripts and shipped fixtures; added `add_xy_position`; put the omnibus label above all brackets; renamed `wilcox_effsize` output rank-biserial r; supplied adjusted ggsignif labels | ran once on all three audit fixtures and once on shipped fixtures; four figures each run, all >1 KB; opened pairwise, ggsignif, paired, and nested figures | Example now accepts three CSV paths plus output directory and is standalone with defaults |
| Paired tests silently pair by row order | P1 | R and Python paired scripts reject duplicate/incomplete IDs, require identical ID sets, pivot/sort by `subject_id`, then test and draw trajectories | R/Python regression suites passed; both reproduce p = 0.0023193359 on `paired.csv`; both reject a missing-subject fixture | Input contract is `subject_id,time,value` |
| Test names and labels differ from tools | P2 | Added inclusive four-star bins for ggpubr/statannotations, ggsignif `NS.`/three-star caveat, `p < 2e-16`, Welch name, and R-exact versus SciPy-asymptotic Wilcoxon note | ran installed-version probes; Python annotations printed the 0.7.2 five-bin legend; border data reproduced the expected R/Python p difference | No attempt to force cross-language equality; the Skill tells users to request the same algorithm when needed |
| Family size, nested annotation, post-hoc gaps | P2 | Stated that the supplied comparisons define the family; added runnable Dunn, Tukey HSD, and LMM+emmeans routes; removed Shapiro-only selection; fixed dynamic colors | ran Dunn on `four_group.csv` (six finite adjusted p; significant 0.00217020/0.00245187), Tukey HSD (0.000386848/0.000342783 significant), and LMM+emmeans on `nested.csv` (p = 0.396429); rendered outputs checked non-blank | Tukey mode explicitly uses Tukey's simultaneous adjustment, not Holm |

All 7/7 backlog findings are fixed. No finding is left unfixed.

## Deduplication and runnable-code moves

| deleted or moved passage | single home now |
|---|---|
| `usage-guide.md` prerequisite install blocks | `SKILL.md` -> Version Compatibility and Installation |
| `usage-guide.md` seven-step "What the Agent Will Do" procedure | `SKILL.md` -> Choose the Test, Adjust the Intended Comparison Family, and runnable workflow sections |
| `usage-guide.md` tip: false ggpubr t-test default | corrected once in `SKILL.md` -> Choose the Test from the Design |
| `usage-guide.md` tips: Holm, family adjustment, and >5-group omnibus | `SKILL.md` -> Adjust the Intended Comparison Family and decision table |
| `usage-guide.md` tips: paired matching and nested data | `SKILL.md` -> Paired Data and Nested Data |
| `usage-guide.md` tips: effect size, negative results, stars/numeric labels, ggsignif mapping, large-N p | `SKILL.md` -> Labels, Exact Values, and Effect Sizes plus Failure Modes |
| duplicated `SKILL.md` Common Errors table | removed; its corrections already live in the method-specific sections and Failure Modes |
| complete inline R adjusted-pairwise workflow | `scripts/annotate_pairwise.R` (parameterized for Wilcoxon, Dunn, and Tukey HSD) |
| complete inline Python statannotations workflow | `scripts/annotate_pairwise.py` (explicit adjusted values) |
| complete paired R workflow from the example | `scripts/annotate_paired.R`; example sources it |
| paired Python recipe required by the audit | `scripts/annotate_paired.py` |
| nested LMM prose/partial example | `scripts/annotate_nested.R`; example sources it |

`SKILL.md` is 153 lines, so the >300-line `references/` split rule does not apply. The usage guide now contains only a short chooser overview, prompts, input guidance, and related Skills.

## Validation evidence

- `run/fixer_parse_and_versions.R`: all five changed R/example/test files parsed; printed the installed package versions above.
- `run/fixer_compile_and_versions.py`: all three changed Python/test files passed `py_compile` with bytecode written only to the audit run directory; printed installed versions.
- `tests/regression.R` and `tests/regression.py`: both passed adjusted-value and incomplete-pair guards.
- `run/fixer_verify_outputs.py`: asserted exact R/Python Holm, paired, Dunn, Tukey, and nested p-values; asserted seven figures were at least 500x500 with non-white fraction >0.01.
- `run/fixer_structure.py`: frontmatter name unchanged, balanced fences, 153 lines, no stale default/Cliff/precision claims, and every referenced script/data path exists.
- Visual inspection: pairwise omnibus label is above the highest bracket; adjusted ggsignif labels are `ns/ns/*`; paired subject lines agree with the test; nested label is the emmeans contrast p rather than the naive cell-level p.

## 2026-09-27 - Round 2 follow-up

Source fixed in `F:\OpenScience\wt\backlog-statistical-annotation` on branch `fix/backlog-statistical-annotation`. Audit evidence and fixtures remained read-only.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Dense bracket families use fixed spacing and crowd the top of the plot | P2 | `annotate_pairwise.R` now derives `step.increase` from family size (0.18 for six comparisons), accepts a positive fifth-argument override, and reserves y-axis space above both the bracket stack and omnibus label; `SKILL.md` also recommends comparison facets or a compact-letter display when one-panel brackets remain too dense | R regression created a six-comparison family, asserted derived spacing exceeds the three-comparison spacing, checked the reserved y limits, and exercised a `0.2` override; the four-group audit fixture rendered all six separated rows at 1040x880 and was opened at original resolution | The full numerical family remains in the result table even when an alternate compact presentation is chosen |
| Default pairwise tables omit effect type and magnitude despite the documented result contract | P2 | R Wilcoxon/Dunn rows now persist signed rank-biserial r, Tukey rows persist signed Hedges' g, and Python Mann-Whitney rows persist signed rank-biserial r; both languages also write explicit test, adjustment, and family-size fields | Focused R regressions passed for Wilcoxon, Dunn, and Tukey; focused Python regression and `py_compile` passed; on `four_group.csv`, all six R/Python rank-biserial values agreed within 4e-16 and both CSV schemas contained `effect_type,effect_size` | Positive effects mean the first named group tends higher; the shipped example now captions the values already persisted by the reusable script |

Both 2/2 round-2 findings are fixed. No round-2 finding is left unfixed.
