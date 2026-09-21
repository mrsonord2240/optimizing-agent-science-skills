import json, os
D = r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots"
SK = "bio-data-visualization-forest-funnel-plots"
def A(t, r, n): return {"text": t, "result": r, "note": n}
inputs = [
 dict(index=1, type="Canonical", label="Random-effects REML forest of 13 real BCG trials (log-OR, exp axis, PI)", status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="SKILL.md rma+forest block ran; pooled OR 0.4746 [0.3296, 0.6835], tau2 0.3378, I2 92.07%, Q 163.16 equal an independent numpy REML calculation; but the mlab bquote(paste(...)) summary label renders as the literal word 'paste' (class is 'call', not expression), so I2/tau2/Q never appear on the plot.",
  basic=30, specialized=44,
  executed=True, execution_note="in1_bcg_forest.R via r.sh; independent check in1_independent.py (numpy/scipy); fix probe in1b_mlab_probe.R. PNG opened with Read.",
  assertions=[
   A("Plotted per-study and pooled estimates equal an independent inverse-variance REML computation", "PASS", "REML mu -0.745178, se 0.186028, tau2 0.337772 identical to 6 decimals; FE OR 0.6465 also matches"),
   A("Reference line at OR = 1 (log 0) and exponentiated axis ticks 0.25-4", "PASS", "dotted line at 1; ticks 0.25/0.5/1/2/4; labels are ORs not logs"),
   A("Summary row reports I2, tau2 and Q-p as the Skill says the forest bottom must", "FAIL", "Summary label prints 'paste'; heterogeneity absent from the figure (as.expression() fixes it, verified)"),
   A("Prediction interval drawn and equals mu +/- 1.96*sqrt(tau2+se^2)", "PASS", "PI OR [0.1435, 1.5696] equals the hand value; drawn as dotted whisker"),
   A("Every CI is fully visible on the plot", "FAIL", "at= ticks double as alim, so 7 of 13 CIs and the PI are clipped with arrows at 0.25/4"),
  ]),
 dict(index=2, type="Variant A", label="Funnel, Egger, trim-and-fill and contour funnel on synthetic k=30 with planted publication bias plus a symmetric control", status="COMPLETED", status_flag="\u2705",
  note="Synthetic k=30 (seed 20260920, 15% of non-significant studies kept). Biased set: Egger t=2.929 p=0.0067, trim-and-fill k0=7, adjusted 0.353 vs 0.413; symmetric control p=0.48. All equal an independent numpy Egger/Duval-Tweedie/REML implementation. Funnel centre and pseudo-CI limits match hand values (-0.451, 1.277 at SE 0.441). refline=res$b triggers R 4.4 array-recycling warnings.",
  basic=34, specialized=51,
  executed=True, execution_note="in2_funnel_asym.R via r.sh; in2_egger_tf_independent.py and in2_check.py independent; also the shipped example forest_phd.R steps 1-7 (Egger p 0.00387, t -4.0137, k0 3, adjusted OR 1.44 all reproduced independently).",
  assertions=[
   A("Funnel points equal (yi, sei) and centre line is the pooled estimate", "PASS", "funnel() return equals data; centre 0.4128 = REML pooled; pseudo-95% edges at SE 0.441 read -0.46/1.28 vs expected -0.451/1.277"),
   A("Egger test detects the planted asymmetry and is quiet on the symmetric control", "PASS", "biased p=0.0067; symmetric p=0.482; both equal independent regression to 4 decimals"),
   A("Trim-and-fill k0 and adjusted estimate equal an independent Duval-Tweedie L0", "PASS", "k0=7 / 0.3531 biased and k0=1 / 0.2758 control; example k0=3 / 0.3674 (OR 1.44)"),
   A("Contour-enhanced funnel shows p<0.10/0.05/0.01 bands centred on 0", "PASS", "bands symmetric about 0, legend present; biased studies concentrate right of the bands"),
   A("Skill code runs without warnings", "FAIL", "refline = res$b (1x1 matrix) emits 4 'Recycling array of length 1' warnings in the contour calls; res$b[1] avoids it"),
  ]),
 dict(index=3, type="Edge", label="k=3 trials: REML vs HKSJ, Egger at k=3, k=2, I2 reporting", status="COMPLETED", status_flag="\u2705",
  note="Synthetic 3 trials (ORs 0.55/0.90/1.60). test='knha' CI on log scale [-1.430062, 1.211864] with df=2 equals a hand Hartung-Knapp calculation; REML z CI [-0.709, 0.491] is 2.4x narrower. Egger still runs at k=3 (t=22.4, df=1, p=0.028) with no warning, and I2=78.2% is printed although the Skill says not to report I2 below k=5.",
  basic=32, specialized=47,
  executed=True, execution_note="in3_smallk.R via r.sh; in3_check.py independent HKSJ. Forest PNG opened.",
  assertions=[
   A("HKSJ CI uses t with k-1 df and the q-adjusted SE, equal to a hand calculation", "PASS", "se 0.307011, CI [-1.430062, 1.211864], dfs 2 in both metafor and numpy"),
   A("Forest with test='knha' shows the pooled OR and diamond consistent with the model", "PASS", "0.90 [0.24, 3.36] matches exp of the HKSJ CI"),
   A("Skill's k<5 rule (do not report I2) is enforced or at least surfaced by the shipped patterns", "FAIL", "summary(res) and the example's cat() print I2=78.2% at k=3 without a guard"),
   A("Egger request at k<10 is refused or warned", "FAIL", "regtest returns t=22.37, p=0.028 silently; the k>=10 rule lives only in prose (the example wraps it in if(nrow>=10), the SKILL block does not)"),
   A("Claim that HKSJ is well-calibrated even at k=3 is supportable", "FAIL", "the k=3 HKSJ OR CI is [0.24, 3.36]; calibration at k<=3 is weak and IntHout 2014 does not claim it"),
  ]),
 dict(index=4, type="Variant B", label="ggforest Cox forest on real survival::lung (n=227) with an interaction request", status="PARTIAL", status_flag="\u26a0\ufe0f",
  note="ggforest block runs and every plotted HR and CI equals exp(coef)/exp(confint) (Female 0.58 [0.42, 0.81], ECOG2 2.47 [1.58, 3.86], log axis, reference line 1, ECOG3 N=1 unflagged). But this is a main-effects multivariable Cox display, not a subgroup forest; ggforest has no interaction argument and the Skill gives no code for subgroup-specific HRs plus an interaction p (stratified HRs 0.68/0.53/0.68 and LRT interaction p 0.893 had to be computed by hand). Example step 8 halts: object 'clinical_df' not found.",
  basic=28, specialized=38,
  executed=True, execution_note="in4_cox_forest.R via r.sh (survminer 0.5.2). The Skill block ran on lung with a treatment/stage stand-in; the example's step 8 as shipped errored.",
  assertions=[
   A("Plotted HRs and CIs equal exp(coef) and exp(confint) of the fitted model", "PASS", "5 terms identical to 3 decimals, p-values 0.001/0.246/0.04/<0.001/0.058 shown"),
   A("Figure is on a log axis with the reference line at HR = 1", "PASS", "ticks 0.5-50 on log spacing, dotted line at 1"),
   A("Output is a subgroup analysis with an interaction p-value as requested in the usage guide", "FAIL", "titled 'Subgroup HRs' but shows covariate HRs from one additive model; no interaction term, no per-subgroup treatment HR"),
   A("Sparse strata are flagged", "FAIL", "ECOG3 has N=1 and HR 7.06 (0.94-53.13) drawn with no warning; coxph on that stratum alone errors"),
   A("Shipped example step 8 runs as delivered", "FAIL", "Error: object 'clinical_df' not found; step 9 never reached"),
  ]),
 dict(index=5, type="Stress", label="MR forest of 28 real lipid SNPs (ldlc to CHD) with IVW, weighted-median, mode, Egger", status="COMPLETED", status_flag="\u26a0\ufe0f",
  note="Real MendelianRandomization::ldlc/chdlodds. mr_allmethods and mr_forest run; IVW 2.834 (se 0.5298 residual-scaled) and MR-Egger 3.253 / intercept -0.0115 equal an independent numpy IVW and weighted Egger. But snp_24's CI to ~380 sets the axis so all four method diamonds collapse near 3 and are indistinguishable; the Skill gives no snp_estimates=FALSE advice (which draws the comparison clearly) and the usage guide's 'annotate per-method p-values' is not supported by mr_forest.",
  basic=30, specialized=42,
  executed=True, execution_note="in5_mr_forest.R via r.sh (MendelianRandomization 0.10.0, ggplot2 4.0.3), in5_check.py independent. Both PNGs opened.",
  assertions=[
   A("IVW and MR-Egger estimates in the package output equal an independent computation", "PASS", "IVW 2.834214 se 0.529799; Egger slope 3.2529, intercept -0.0115, matching to 4 decimals"),
   A("Forest shows four method estimates that can be told apart", "FAIL", "with SNP rows shown, one outlier stretches x to 400; diamonds overlap; only snp_estimates=FALSE (not in the Skill) resolves them"),
   A("MR-Egger intercept reported alongside the main estimate as the example comment demands", "PASS", "printed by mr_allmethods and mr_egger: intercept -0.0115 (p 0.451)"),
   A("Per-method p-values annotated on the plot as the usage guide promises", "FAIL", "mr_forest has no p-value annotation; the Skill gives no code to add it"),
   A("No practice-boundary or causal over-claim in the guidance", "PASS", "Skill says triangulate methods, pleiotropy caveat, cites Bowden 2015"),
  ]),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"]); i["assertions_total"] = len(i["assertions"])
    assert 3 <= len(i["assertions"]) <= 5
avg = round(sum(i["total"] for i in inputs)/len(inputs), 1)
cats = {
 "functional_suitability": (7, 12, "Completeness 2: frontmatter promises forestplot, ggforestplot, netmeta, cumulative forests and subgroup-with-interaction forests but no code for any of them; Correctness 2: the shipped mlab prints 'paste', ggforest is sold as a subgroup forest, HKSJ is called well-calibrated at k=3, netmeta 'Bayesian or frequentist'; Appropriateness 3"),
 "reliability": (7, 12, "The failure modes are in prose only; the code blocks carry no k<5 / k<10 guard (Egger ran at k=3 with p=0.028) and the example dies at step 8 (clinical_df) so step 9 is never reached"),
 "performance_context": (6, 8, "272-line SKILL.md in one file with a usage guide that repeats its tips; no references to load lazily"),
 "agent_usability": (13, 16, "Very strong Error Prevention (7 failure-mode entries, reconciliation table, thresholds); Feedback Design loses a point because the promised I2/tau2/Q footer is not produced by the code"),
 "human_usability": (7, 8, "Natural trigger phrases (forest plot, funnel plot, Egger, MR forest); example prompts in the usage guide; graceful degradation for small k is described but not coded"),
 "security": (11, 12, "No credentials, network or user-string execution; plain plotting code writing into the working directory"),
 "maintainability": (8, 12, "SKILL.md plus usage guide plus one example; the example is not runnable past step 7 and prints no expected values, so testability is 2"),
 "agent_specific": (17, 20, "Trigger 3 (broad but on target), progressive disclosure 3 (no references dir, fine at 272 lines), composability 3 (Related Skills named), idempotency 4 (deterministic REML), escape hatches 4 (k<3 no pooling, k<5 no I2, k<10 no Egger)"),
}
sub = sum(v[0] for v in cats.values())
sw, dw = round(sub*0.4, 1), round(avg*0.6, 1); score = round(sw+dw)
rep = {
 "meta": {"skill_name": SK,
  "description": "Build forest plots (HR, OR, RR, beta-coefficient summaries with CIs) and funnel plots (meta-analysis publication-bias diagnostics) using forestplot, metafor, ggforest, and MendelianRandomization with proper axis-scaling, summary-diamond placement, subgroup nesting, and Egger / trim-and-fill asymmetry tests. Use when summarizing effects across subgroups, trials, or instruments - meta-analysis, Mendelian randomization, subgroup HRs.",
  "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Moderate", "n_inputs": 5,
  "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/forest-funnel-plots",
  "audit_type": "first audit",
  "executed": True,
  "execution_note": "Executed 5/5 inputs plus the shipped example forest_phd.R (steps 1-7 ran, step 8 halts on undefined clinical_df). R 4.4.3 via the env's r.sh: metafor 4.8.0, survminer 0.5.2, MendelianRandomization 0.10.0, ggplot2 4.0.3. Every plotted estimate was compared with an independent numpy/scipy computation (REML, Egger, Duval-Tweedie L0, HKSJ, IVW, MR-Egger) and every output PNG was opened. Data: real dat.bcg, survival::lung, MendelianRandomization ldlc/chdlodds; synthetic k=30 (biased and symmetric) and k=3 sets, labelled synthetic. Not exercised: forestplot, ggforestplot, netmeta, metafor::cumul (the Skill ships no code for them)."},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOIs, trial results or p-values; all figures were reproduced from real or labelled-synthetic inputs and the citations (Egger 1997, Sterne 2011, Higgins 2002, Peters 2008, Bowden 2015) are genuine"},
   "practice_boundaries": {"result": "PASS", "detail": "Research meta-analysis and MR summarisation; no individual diagnosis or treatment advice in any output"},
   "methodological_ground": {"result": "PASS", "detail": "No principled fallacy: REML, log-scale ratios, Egger k>=10, trim-and-fill as sensitivity and interaction-test warnings are all sound. Two overstatements (HKSJ 'well-calibrated at k=3'; ggforest as a 'subgroup' forest) are P1 findings, not inverted conclusions"},
   "code_usability": {"result": "PASS", "detail": "Every SKILL.md block ran and produced verified numbers. Example steps 8-9 reference undefined data (clinical_df, bx) and halt as shipped, recorded as a P1; the packages, syntax and call signatures are valid (steps run once data was supplied)"}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
  "inputs": [{k: i[k] for k in ["index","type","label","status","status_flag","note","basic","specialized","total","assertions_passed","assertions_total","assertions","executed","execution_note"]} for i in inputs]},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Limited Release", "grade_symbol": "\u2705", "deployable": True, "veto_override": False},
 "key_strengths": [
  "The statistics are right: REML pooled estimates, tau2, I2, Q, PI, Egger t/p, trim-and-fill k0/adjusted estimate, HKSJ CI, IVW and MR-Egger all matched independent numpy/scipy computations to 4-6 decimals",
  "Best-in-set failure-mode content: Egger k>=10, I2 uninterpretable below k=5, trim-and-fill as sensitivity, interaction-test warnings, log axis for ratios, each with trigger, mechanism, symptom and fix",
  "The contour-enhanced funnel, trim-and-fill and Egger examples work on planted-bias data and separate it from a symmetric control (p 0.0067 vs 0.48)",
  "Shipped-means-present holds: SKILL.md, usage-guide.md and the example exist and nothing points at a missing file"],
 "recommendations": [
  {"priority": "P1", "title": "mlab bquote(paste()) prints 'paste', hiding I2/tau2/Q", "observed_in": [1],
   "problem": "In both the SKILL.md forest block and examples/forest_phd.R the pooled-row label renders as the word 'paste' because bquote() returns a call, not an expression; the heterogeneity footer the Skill calls mandatory never appears.",
   "root_cause": "mlab needs an expression or character; the snippet was never rendered and checked.",
   "fix": "Wrap in as.expression(bquote(...)) (verified: prints 'RE Model (Q = 163.16, df = 12; I2 = 92.1%)') or use sprintf() to a character mlab; then add a rendered-output check."},
  {"priority": "P1", "title": "ggforest is not a subgroup forest and no interaction code is given", "observed_in": [4],
   "problem": "The decision tree and usage guide route 'Cox subgroup forest with interaction p-values' to ggforest, which draws covariate HRs from one additive coxph model and has no interaction argument; per-subgroup treatment HRs and the interaction LRT (p 0.893 here) had to be built by hand.",
   "root_cause": "ggforest was conflated with a stratified subgroup display; only prose mentions the interaction term.",
   "fix": "Rename that section 'multivariable Cox forest', and add a subgroup block: fit treatment*subgroup, extract stratum HRs with CIs, plot with metafor forest or forestplot, annotate the anova() interaction p. Warn that sparse strata (ECOG3 N=1) must be collapsed."},
  {"priority": "P1", "title": "Shipped example halts at step 8 and never runs step 9", "observed_in": [4, 5],
   "problem": "forest_phd.R stops with object 'clinical_df' not found; step 9 uses undefined bx/bxse/by/byse. Only steps 1-7 are runnable, so the example cannot serve as a test.",
   "root_cause": "Placeholder data objects are used without definitions or a synthetic fallback.",
   "fix": "Define small inline data for steps 8-9 (e.g. survival::lung and MendelianRandomization::ldlc/chdlodds) so the whole script runs, and print the expected values."},
  {"priority": "P1", "title": "Small-k rules live only in prose; HKSJ overstated at k=3", "observed_in": [3],
   "problem": "The code blocks print I2 at k=3 and run regtest() at k=3 (p=0.028) with no guard, despite the k<5 and k>=10 rules; the text says HKSJ is 'well-calibrated even at k=3' while the k=3 CI here spans OR 0.24-3.36.",
   "root_cause": "Guards are stated as advice, not encoded; the calibration claim goes beyond IntHout 2014.",
   "fix": "Wrap I2 and regtest in if (res$k >= 5) / if (res$k >= 10) with a message otherwise, and soften the HKSJ sentence to 'better calibrated than z-based CIs, still very wide at k<=3'."},
  {"priority": "P1", "title": "MR forest unreadable with outlier SNP; p-value annotation unsupported", "observed_in": [5],
   "problem": "mr_forest with default SNP rows lets one SNP (CI to 380) set the axis so the four method estimates overlap; the usage guide promises per-method p-value annotation that mr_forest cannot draw.",
   "root_cause": "No guidance on snp_estimates=FALSE or axis control, and the annotation claim was not tested.",
   "fix": "Show mr_forest(..., snp_estimates = FALSE) for the method comparison, note the outlier effect, and either add a ggplot annotation snippet for p-values or delete the promise."},
  {"priority": "P2", "title": "refline = res$b triggers array-recycling warnings", "observed_in": [2],
   "problem": "res$b is a 1x1 matrix; funnel() emits four deprecation warnings under R 4.4.", "root_cause": "Matrix passed where a scalar is expected.", "fix": "Use refline = res$b[1] or coef(res)."},
  {"priority": "P2", "title": "at= ticks clip most CIs on the BCG forest", "observed_in": [1],
   "problem": "at = log(c(0.25..4)) also sets the plotting range, so 7 of 13 CIs and the PI are cut with arrows.", "root_cause": "Tick set chosen without regard to data range.", "fix": "Say that at also sets alim, or add alim/xlim so all intervals are shown."},
  {"priority": "P2", "title": "Frontmatter promises tools with no code; netmeta described as Bayesian", "observed_in": [],
   "problem": "forestplot (with boxsize), ggforestplot, netmeta and metafor::cumul are named but no snippet exists; netmeta is frequentist yet the table says 'Bayesian or frequentist'.", "root_cause": "Description broader than the body.", "fix": "Add one short block per promised tool or trim the description; correct the netmeta row."},
  {"priority": "P2", "title": "usage-guide.md repeats SKILL.md tips; example data contradicts its own lesson", "observed_in": [2],
   "problem": "The Tips list is a near-copy of SKILL.md text; the example's synthetic data give I2 = 0% (so the prediction interval is invisible) and a significant Egger p = 0.0039, unremarked.", "root_cause": "Data were not designed to show the lessons.", "fix": "Remove the duplicate Tips, and choose example data with visible heterogeneity and a stated Egger outcome."}],
}
json.dump(rep, open(os.path.join(D, f"eval_report_{SK}_result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("static", sub, "avg", avg, "final", sw, dw, score, [i["total"] for i in inputs], rep["dynamic_score"]["assertion_pass_rate"])
