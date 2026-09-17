# Cross-reference — machine learning, survival and validation (2026-09-17)

Slice: 14 published Skills under `clinical-prediction-model-specialist` (all 14 assigned Skills belong to this specialist; none belong to `real-world-evidence-epidemiologist`). Cross-referenced against the `bioSkills/machine-learning`, `bioSkills/clinical-biostatistics`, and `bioSkills/workflows/biomarker-pipeline` folders.

No install-time conflicts exist (IDs differ). The findings below are about routing ambiguity and which Skill a future Specialist should bundle.

## Summary table

| Published Skill | bioSkills counterpart(s) | Verdict | Bundle | One-line reason |
|---|---|---|---|---|
| `lasso-logistics-analysis` | `bio-machine-learning-biomarker-discovery`, `bio-machine-learning-omics-classifiers` | partial | both (see below) | Published ships a runnable LASSO CLI with no held-out validation or stability check; bioSkill teaches the correct guard (elastic net over bare LASSO, stability selection, leakage-safe CV) but ships no turnkey tool. |
| `elastic-net-feature-selection` | `bio-machine-learning-biomarker-discovery`, `bio-workflows-biomarker-pipeline` | partial | both | Same method, same gap: bioSkill's own recommended default (elastic net) matches this published Skill's method, but adds stability scoring and leakage-safe CV the published Skill lacks. |
| `xgboost-analysis` | `bio-machine-learning-omics-classifiers` | partial | omics-classifiers for correctness, published for artifacts | bioSkill gives full working `XGBClassifier` code plus the exact failure modes (early-stopping API drift, calibration direction, no SMOTE); published gives a runnable R CLI with plots but no calibration or leakage guard. |
| `lightgbm-analysis` | `bio-machine-learning-omics-classifiers` | partial (thin) | published | bioSkill only namechecks LightGBM inside a combined "GBDT (XGBoost/LightGBM)" row — no LightGBM-specific code; published is the only concrete LightGBM tool. |
| `rf-model-importance-analysis` | `bio-machine-learning-omics-classifiers`, `bio-machine-learning-prediction-explanation` | partial | both | bioSkill flags that RF votes are bounded away from 0/1 (miscalibrated) and that OOB error after full-data selection is leakage — neither caveat appears in the published Skill, which reports `randomForest::importance` directly. |
| `svm-model-importance-analysis` | `bio-machine-learning-biomarker-discovery` | partial (thin) | published | bioSkill mentions SVM-RFE in one taxonomy row only ("needs a linear kernel"); published is the only Skill that actually runs SVM-RFE with a CV error curve and ranking plot. |
| `external-model-validation` | `bio-machine-learning-survival-analysis` | partial | published, gated by bioSkill's checklist | Published computes KM + basic time-dependent ROC on the external cohort but has no calibration or Uno's C(tau)/IBS — exactly the "C-index/ROC-only is the cardinal sin" failure mode the bioSkill names. |
| `roc-diagnostic-performance` | `bio-machine-learning-model-validation` | partial | published | bioSkill's AUC/discrimination guidance applies generically, but no bioSkill runs a marker-vs-marker diagnostic ROC comparison from expression data; `bio-clinical-biostatistics-logistic-regression` is a false-positive lexical match — its estimand is trial covariate adjustment, not diagnostic AUC. |
| `time-dependent-roc` | `bio-machine-learning-survival-analysis` | partial | published (already paired with `model-calibration-curve` in this slice) | bioSkill treats time-dependent AUC as one leg of a 3-part evaluation (AUC(t) + Uno's C + IBS); published's `time-dependent-roc` + `model-calibration-curve` together approximate two of the three legs already. |
| `model-calibration-curve` | `bio-machine-learning-survival-analysis` | partial | published | Published uses classic `rms::calibrate()` bootstrap groups (Harrell's own method); bioSkill recommends ICI/E50/E90 (Austin 2020) and explicitly bans Hosmer-Lemeshow — a modern-metric gap, not a wrong method. |
| `nomogram-construction` | none found | distinct / no counterpart | published | "nomogram" does not appear anywhere in the bioSkills corpus (grep confirmed zero hits). |
| `decision-curve-analysis` | `bio-machine-learning-model-validation` | partial | published | bioSkill states the identical net-benefit formula and cites the same Vickers-Elkin source, but only as a paragraph inside model-validation — no runnable DCA/clinical-impact-curve tool exists in bioSkills. |
| `km-survival-curve` | `bio-clinical-biostatistics-survival-analysis` | partial | published for the plot, bioSkill for the test choice | bioSkill covers 5 log-rank weighting variants and warns 1-KM is biased upward under competing risks; published always uses plain log-rank/Wald with no competing-risks warning. |
| `univariate-multivariable-cox-regression` | `bio-clinical-biostatistics-survival-analysis` | partial (consequential) | bioSkill gates, published executes | Published has **no proportional-hazards diagnostic anywhere in its workflow**; bioSkill's central teaching is "PH Almost Never Holds" and mandates `cox.zph`/Schoenfeld-residual checks before trusting any Cox HR. |

Counts: **partial = 13**, **distinct/no counterpart = 1**, **duplicate = 0**. No pair reached "duplicate" — every bioSkill counterpart differs from its published match either in modality (Python reference-and-guidance skill with code snippets vs. a tested, packaged R CLI with test data and `SKILL_*` error codes) or in the specific guardrail it adds/omits, so a user would not be simply choosing between two interchangeable tools.

---

## Duplicate / partial pairs — evidence

### `lasso-logistics-analysis` vs `bio-machine-learning-biomarker-discovery`

Published: fits `cv.glmnet` with `alpha = 1` on the full matrix and reports `lambda.min` coefficients directly — "Extract coefficients at `lambda.min`" — with no held-out performance number and no stability check anywhere in the workflow.

bioSkill: "L1 geometry keeps one vertex of a correlated group arbitrarily; the choice flips across resamples... Use elastic net (grouping effect) or report selection *frequencies*; never read membership as importance ordering," and separately: "Selecting the top-k features on the *whole* dataset before cross-validating the classifier produces near-zero apparent error even on pure noise (Ambroise-McLachlan 2002)."

Bundle: for a Specialist whose deliverable is a defensible signature (not just a coefficient plot), bundle `bio-machine-learning-biomarker-discovery` alongside the published tool and require its stability-selection step before the published Skill's `selected_features.txt` is trusted as final.

### `elastic-net-feature-selection` vs `bio-machine-learning-biomarker-discovery` / `bio-workflows-biomarker-pipeline`

Published: "Elastic net combines lasso (L1) and ridge (L2) penalties through alpha, enabling sparse feature selection while stabilizing correlated predictors" — single fit, `alpha_grid` CV-tuned once, no bootstrap stability score.

bioSkill (`bio-workflows-biomarker-pipeline`, Option B): "for i in range(n_bootstrap): ... stability_scores += (model.coef_[0] != 0).astype(int) ... selected_idx = stability_scores > 0.6" — the same elastic-net-family method wrapped in a 100+ resample stability check that the published Skill never performs.

Bundle: both are correct on method; bundle the bioSkill's pipeline for the stability index, keep published for the plots.

### `xgboost-analysis` / `lightgbm-analysis` / `rf-model-importance-analysis` / `svm-model-importance-analysis` vs `bio-machine-learning-omics-classifiers`

Published (`xgboost-analysis`): trains and reports `table/xgboost_feature_importance.csv` with no calibration check and no batch-shortcut check.

bioSkill: "XGBoost 2.x: early_stopping_rounds and eval_metric go in the CONSTRUCTOR, not fit()... scale_pos_weight is omitted on purpose: like resampling, it reweights the prior and distorts calibration," plus a full "Detecting Batch Shortcut Learning" section with a runnable `cross_val_score(pipe, X, batch_labels, ...)` check absent from any of the four published model-family Skills.

Bundle: see many-to-one section below — recommend the bioSkill trio for a Specialist that must defend its model choices; keep the individual published Skills only where a specific turnkey plot/table is the deliverable (e.g. `lightgbm-analysis`, where no bioSkill code exists at all).

### `external-model-validation` vs `bio-machine-learning-survival-analysis`

Published: computes `timeROC::timeROC` and a KM curve on the external cohort as the entire validation report — "Time-dependent ROC curve PDF" and "Kaplan-Meier survival curve with risk table" are the only performance outputs.

bioSkill: "The C-index is necessary but radically insufficient... Decision-grade evaluation is Uno's C(tau) + time-dependent AUC(t) + integrated Brier vs a Kaplan-Meier baseline + calibration curves, all on honestly held-out or external data." External validation with no calibration curve is precisely the pattern the bioSkill calls out as the "cardinal sin."

Bundle: keep published for its concrete artifact set, but flag that a Specialist relying on it alone is validating discrimination only, not calibration — pair with `model-calibration-curve` (already in this slice) to close part of the gap; full Uno's C/IBS still requires the bioSkill's Python stack.

### `model-calibration-curve` vs `bio-machine-learning-survival-analysis`

Published: "Run `rms::calibrate()` for each prediction horizon using bootstrap resampling" (Harrell's classical grouped-bootstrap calibration).

bioSkill: "summarize with ICI/E50/E90 (Austin 2020) -- never Hosmer-Lemeshow." rms::calibrate() is not Hosmer-Lemeshow and is a legitimate, still-current method (Harrell is cited in both), so this is a modern-metric enhancement gap rather than a wrong approach.

Bundle: published (it is the only runnable tool); the bioSkill's ICI reference is worth adding to the published Skill's `algorithm.md` rather than switching tools.

### `decision-curve-analysis` vs `bio-machine-learning-model-validation`

Published: `net_benefit` computed via `rmda::decision_curve()`, citing "Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models."

bioSkill: "net_benefit = TP/n - (FP/n)*(pt/(1-pt))... DCA requires good calibration to be valid and is the bridge from statistical performance to clinical usefulness — a model can have high AUC yet zero net benefit at every plausible threshold" (same Vickers-Elkin 2006 citation).

Bundle: published — it is the only runnable DCA tool in either corpus; the bioSkill statement is a one-paragraph concept explainer with no code.

### `km-survival-curve` vs `bio-clinical-biostatistics-survival-analysis`

Published: `--statistics_method logrank` or `wald` only; no mention of competing risks anywhere in the Skill.

bioSkill: "The KM estimator is biased upward in the presence of competing risks — it treats competing events as non-informative censoring and overestimates 1 - CIF" and offers five log-rank weighting variants (Wilcoxon, Tarone-Ware, Peto-Peto, Fleming-Harrington, MaxCombo) against the published Skill's one.

Bundle: published for the plot deliverable; a Specialist working in oncology (where competing risks are common) should route through the bioSkill's CIF/Aalen-Johansen guidance before accepting a KM curve as the answer.

### `univariate-multivariable-cox-regression` vs `bio-clinical-biostatistics-survival-analysis`

Published: the entire workflow is "Fit one Cox model per feature... Use all significant univariate features with `p < 0.05`... Export adjusted hazard ratios" — no proportional-hazards check is mentioned in the SKILL.md, the algorithm reference, or the output contract.

bioSkill: "In modern oncology... proportional hazards (PH) violations are the rule, not the exception... `cph.check_assumptions(df, p_value_threshold=0.05, show_plots=True)`... Critical interpretation rule: a global p > 0.05 does NOT mean PH holds." This is the single most consequential gap found in the slice: the published Skill's headline deliverable (a hazard-ratio forest plot) is exactly the artifact the bioSkill says is unsafe to trust without this diagnostic.

Bundle: bundle `bio-clinical-biostatistics-survival-analysis` as a mandatory gate in front of `univariate-multivariable-cox-regression` — run the published Skill for the HR table and forest plot, but require the bioSkill's `cox.zph`/Schoenfeld-residual check (or note the diagnostic is unavailable) before the HR is reported as valid. Separately, the published Skill's own "keep p<0.05 univariate features, fall back to all if fewer than 3" rule is a form of stepwise selection that `bio-clinical-biostatistics-logistic-regression`'s reviewer-pushback table explicitly names as inflating Type-I error — a second, smaller finding worth carrying into the same fix.

---

## The many-to-one collapse

Six published Skills — `lasso-logistics-analysis`, `elastic-net-feature-selection`, `xgboost-analysis`, `lightgbm-analysis`, `rf-model-importance-analysis`, `svm-model-importance-analysis` — each cover exactly one model family and ship as an independent, runnable R CLI. In bioSkills, the same six methods are distributed across two prose-and-code-pattern Skills:

- `bio-machine-learning-omics-classifiers` explicitly covers L1/elastic-net logistic, random forest, and XGBoost with runnable `sklearn`/`xgboost` code and a comparison table ("L1 logistic (lasso)... L2/elastic-net logistic... Random forest... GBDT (XGBoost/LightGBM)"). **LightGBM is named only inside a combined GBDT table row — no LightGBM-specific code exists.** Linear SVM is named as an algorithm choice ("High-dim linear separability (Statnikov 2008)") but SVM-RFE (the published Skill's actual method) is not implemented, only referenced in `bio-machine-learning-biomarker-discovery`'s taxonomy table as a one-line "Wrapper" entry with no code.
- `bio-machine-learning-biomarker-discovery` covers LASSO and elastic-net as "Minimal-Optimal" selection with full runnable code, plus Boruta (which none of the six published Skills implement).

So the collapse is real but **uneven**: XGBoost, RF, and the two linear-penalty methods (LASSO, elastic net) are substantively covered with working code in the bioSkill pair; LightGBM and SVM-RFE are only named, not implemented, in bioSkills — for those two, the published Skill is the only runnable option in either corpus.

The bioSkill pair adds four things absent from all six published Skills without exception: (1) leakage-safe selection inside a CV `Pipeline`, (2) a batch-shortcut-learning detection routine, (3) an explicit no-SMOTE-for-risk-models rule, and (4) calibration-direction guidance per model family. None of the six published Skills perform a train/test split with a reported held-out metric — each reports in-sample coefficients, importances, or a single train/test split with no CV-based generalization estimate beyond `xgboost`'s/`lightgbm`'s single internal validation split.

**Recommendation for a future Specialist:** bundle `bio-machine-learning-omics-classifiers` + `bio-machine-learning-biomarker-discovery` + `bio-machine-learning-model-validation` as the default reasoning layer (method choice, leakage, calibration, batch-shortcut checks), and keep the published per-family Skills only as the execution layer that produces the actual plots/tables the six published Skills are good at. For LightGBM and SVM-RFE specifically, the published Skill is not redundant — it is the only implementation.

---

## Audit scores

Of the eight bioSkills examined, only two have audit reports:

- `bio-machine-learning-model-validation`: `final.score` 93, `final.grade` "Limited Release"
- `bio-machine-learning-prediction-explanation`: `final.score` 89, `final.grade` "Limited Release"

`bio-machine-learning-omics-classifiers`, `bio-machine-learning-biomarker-discovery`, `bio-machine-learning-survival-analysis`, `bio-clinical-biostatistics-survival-analysis`, `bio-clinical-biostatistics-logistic-regression`, and `bio-workflows-biomarker-pipeline` have no audit report at `F:\OpenScience\audits\<skill-id>\`. The 14 published non-bio Skills have no audit reports at all — quality there was assessed only by reading the SKILL.md, not by a scored eval.

---

## Assigned Skills with no bioSkills counterpart

- `nomogram-construction` — "nomogram" does not appear anywhere in the bioSkills corpus (566-skill grep, zero hits). Nomograms are a clinical-communication artifact (graphical point-scoring device derived from a Cox model), not a modeling method bioSkills' machine-learning or clinical-biostatistics folders address at all.
