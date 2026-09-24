"""Exact-source contract checks for 3473a8f48eccab6c73436a627c3e8568f3736eef."""
from pathlib import Path
import json

root = Path(r"F:\OpenScience\wt\data-visualization-forest-funnel-plots\data-visualization\forest-funnel-plots")
skill = (root / "SKILL.md").read_text(encoding="utf-8")
example = (root / "examples" / "forest_phd.R").read_text(encoding="utf-8")
checks = {
    "frontmatter_targeted": "small-study safeguards" in skill,
    "no_bquote_paste_footer": "mlab = bquote" not in skill,
    "all_study_plot_limits": "study_lb <- studies$log_or" in skill and "study_ub <- studies$log_or" in skill,
    "plot_limits_include_prediction_interval": "alim = limits" in skill and "pred$pi.lb" in skill,
    "scalar_funnel_reference": "refline = as.numeric(coef(res)[1])" in skill,
    "small_k_guard": "if (nrow(studies) < 3)" in skill and "test = if (nrow(studies) < 5) \"knha\"" in skill,
    "egger_guard": "if (res$k >= 10)" in skill and "Egger test withheld" in skill,
    "cox_roles_separated": "Adjusted covariate hazard ratios" in skill and "treatment * subgroup" in skill,
    "sparse_subgroups_guarded": "counts < 20" in skill and "fewer than 5 events" in skill,
    "mr_outlier_safe": "snp_estimates = FALSE" in skill,
    "netmeta_corrected": "frequentist network-meta-analysis" in skill,
    "runnable_example_defines_clinical_data": "clinical_df <- data.frame(" in example,
    "runnable_example_uses_nonshadowing_mr_name": "mr_dat <- mr_input" in example,
}
result = {"commit": "3473a8f48eccab6c73436a627c3e8568f3736eef", "passed": sum(checks.values()),
          "total": len(checks), "checks": checks}
print(json.dumps(result, indent=2))
if result["passed"] != result["total"]:
    raise SystemExit("source contract check failed")
