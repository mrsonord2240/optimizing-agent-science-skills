# Builds eval_report_..._result.json from the scores decided in this audit (numbers come from the logs in run/out).
import json
D = r"F:\OpenScience\audits\bio-data-visualization-distribution-plots" + "\\"
SK = "bio-data-visualization-distribution-plots"

def A(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = []
def add(i, typ, label, note, basic, spec, asserts, exe_note):
    inputs.append({"index": i, "type": typ, "label": label, "status": "COMPLETED", "status_flag": "\u2705", "note": note,
                   "basic": basic, "specialized": spec, "total": basic + spec,
                   "assertions_passed": sum(a["result"] == "PASS" for a in asserts), "assertions_total": len(asserts),
                   "assertions": asserts, "executed": True, "execution_note": exe_note})

add(1, "Canonical", "Every plain R block of SKILL.md verbatim (box+jitter, SJ violin, quasirandom+crossbar, gghalves raincloud, lvplot) on planted 2-group data, asserted against layer_data",
    "Synthetic Control n=25 unimodal vs Treated n=80 bimodal, equal means (4.99/4.97). Box/violin/quasirandom/letter-value blocks run on ggplot2 4.0.3 and every drawn median, quartile, point count, fill and colour maps to the right group (12/12 probes). The raincloud block, the Skill's headline, fails on ggplot2 4.0.3 (gghalves, archived on CRAN 2025-12-04: 'argument layout is missing') and renders only under ggplot2 3.5.2 (13/13 probes, 105 raw points, medians equal, opened PNG correct). A ggdist raincloud built from a package the Skill already lists renders on 4.0.3 with medians equal.",
    32, 45, [
    A("Every plain R block except the raincloud (boxplot+jitter, SJ violin, quasirandom+crossbar, letter-value) runs verbatim on ggplot2 4.0.3 and the drawn statistics equal the data", True, "12/12 probes: box medians 5.186/4.875 and quartiles equal quantile(); jitter and quasirandom draw 25+80 points with y equal to the data; crossbar y equals group medians; fills #0072B2/#D55E00 in group order; letter-value M row equals medians; quasirandom x identical on re-run"),
    A("The SJ violin shows Control unimodal and Treated bimodal, and trim=FALSE lets the KDE extend past the data range as the Skill says", True, "prominent modes 1/2 (independent density() check 1/2); Treated violin y 0.61..9.18 vs data 1.69..8.09; bw.SJ 0.618/0.363 vs nrd0 0.543/0.782"),
    A("The raincloud block renders on the current ggplot2 (4.0.3)", False, "ggsave error 'Problem while converting geom to grob ... argument \"layout\" is missing, with no default' from gghalves 0.1.4 (archived on CRAN); 1.5 KB blank PNG; the Skill states ggplot2 3.5+ and gghalves 0.1.4+"),
    A("The raincloud block renders under ggplot2 3.5.2 and draws the data it should", True, "105 raw points (25/80) with y equal to the data, box medians equal, opened PNG: violin, box and points per group in the right colours, Treated violin bimodal"),
    A("The bar-of-mean claim holds on planted data: equal bars, very different distributions", True, "means 4.990 vs 4.968; Treated has 0 of 80 points within 0.5 of its mean; the box median 4.875 sits in the empty gap between the modes at 3 and 7")],
    "Executed: run/i1_data.R, run/i1_blocks.R (TAG=gg4 via r.sh; TAG=gg35 via r-gg35.sh), run/i1b_ggdist.R. SYNTHETIC data (run/data/i1_synthetic_2group.csv, seed 20260920). lvplot fails under r-gg35.sh (built against 4.0.3, env artifact) and works under r.sh; gghalves the reverse.")

add(2, "Variant A", "Python blocks: ptitprince RainCloud (verbatim), seaborn boxenplot, and the header seaborn functions, on the same planted data",
    "The verbatim pt.RainCloud(x='group', y='value', orient='h', bw='scott', cut=0) and boxenplot blocks run on seaborn 0.13.2 / matplotlib 3.11.2 and draw n=25 and n=80 points with box medians 5.186/4.875 (opened PNG correct). Both raise deprecation warnings that will become errors. The Python bandwidth 'scott' (0.869) leaves the valley between the Treated modes at 35% of the lower peak versus 3% for the R Sheather-Jones bandwidth (0.363), although only 3 of 80 points lie between 4 and 6: the Python path does not deliver the honest bimodality the R path is sold on.",
    34, 48, [
    A("The Python raincloud block runs verbatim and draws every point with the right medians", True, "scatter collections of 25 and 80 points; box medians 5.186 and 4.875 present among the drawn Line2D; axis labels group/value; opened PNG correct"),
    A("The seaborn boxenplot block and the box/violin/swarm/strip functions named in the header run", True, "all 5 figures written; boxen for Treated shows the wide central box across the gap (as for lvplot)"),
    A("The Python blocks run without deprecation warnings on current seaborn and matplotlib", False, "seaborn 0.13.2 FutureWarning 'Passing palette without assigning hue' in boxenplot and inside ptitprince; matplotlib 3.11 MatplotlibDeprecationWarning vert (removed in 3.13) from ptitprince"),
    A("The Python raincloud's bandwidth keeps a planted bimodality as visible as the Skill's R recommendation (SJ)", False, "valley/lower-peak density ratio 0.346 for bw='scott' vs 0.028 for bw.SJ on the same 80 points (run/i2b_bw.py); ptitprince cannot take 'SJ'")],
    "Executed: run/i2_py.py, run/i2b_bw.py via py.sh. SYNTHETIC data from input 1.")

add(3, "Edge", "Zero-inflated single-cell-like clusters, ties, n=5/3/1, notch at n=8, the N-annotation snippet, NA rows, and the bandwidth claims (300-draw simulation)",
    "The Skill's central advice bw='SJ' turns the whole violin panel blank (exit 0, warning only) as soon as one cluster has tied values (all-zero cluster: 'sample is too sparse to find TD'), the case the usage guide names for single-cell violins; the default violin draws all four. Its stat_summary N-label snippet errors (missing y). The 'nrd (Scott) oversmooths less than Silverman' sentence is wrong (nrd is 1.178x nrd0). Simulation confirms SJ recovers bimodality at least as often as nrd0 in 12/12 cells (10 better, 0 worse), and the notch formula and warning reproduce. trim=FALSE draws density down to -1.63 for data whose minimum is 0.",
    26, 33, [
    A("geom_violin(trim=FALSE, bw='SJ') draws every cluster of zero-inflated single-cell-like data without error", False, "cluster C4 (all zeros) makes bw.SJ fail: 'sample is too sparse to find TD' -> 'Computation failed in stat_ydensity()' and the saved panel is empty (opened PNG); default violin draws all four. bw.SJ also fails on 90% ties, works at 60% zeros"),
    A("The Skill's stat_summary(geom='text', fun.data=function(x) data.frame(label=...)) N annotation draws n labels", False, "geom_text() requires the following missing aesthetics: y; the variant with y = max(x) gives n=12, n=20; the tick-label form 'Control (n=12)' works"),
    A("The bandwidth sentence 'nrd (Scott) oversmooths less than Silverman' is true", False, "bw.nrd 0.9323 vs bw.nrd0 0.7916 (ratio 1.1778); in 12 simulated cells nrd is at least as good as nrd0 in 1"),
    A("Sheather-Jones shows planted bimodality at least as often as the default nrd0", True, "300 draws x 12 (n, separation) cells: SJ better in 10, equal in 2, worse in 0; mean detection nrd0 0.458, nrd 0.340, SJ 0.510"),
    A("The notch guidance is accurate: warning at n<15 and notch = median +/- 1.58*IQR/sqrt(n)", True, "n=8 emits 'Notch went outside hinges'; drawn notch [1.765, 4.335] equals the formula; groups with fewer than two points are dropped with a warning at n=1")],
    "Executed: run/i3_edge.R, run/i3b_bw.R via r.sh (ggplot2 4.0.3). SYNTHETIC data (seeds set in the scripts).")

add(4, "Variant B", "REAL Bioconductor ALL microarray (128 samples): most B-vs-T probe (38319_at) per stage, split violin + box + N tick labels, plus a missing-cell edge",
    "Real unequal cells: B 19/36/23/12, T 1/15/10/2 across stages 1-4. Box medians equal the per-cell medians, fills map B=#56B4E9 and T=#D55E00, tick-label N equals the table. But the split-violin half is chosen by group-id parity: when a stage lacks one lineage every later stage swaps sides (B left at stage 1, right at stages 2-4), so the box, dodged to a fixed side, sits inside the wrong condition's half (opened PNG). The Skill's own rule (no violin below N=30) is not applied: T n=2 and n=1 cells still get a KDE violin or a silent drop.",
    28, 42, [
    A("Box medians equal the per-(stage, lineage) medians of the real data and all 8 boxes are drawn", True, "medians 4.54, 4.61, 4.71, 4.90, 8.58, 9.36, 9.64, 9.90 equal group medians of 38319_at; fills B=#56B4E9, T=#D55E00 by lineage"),
    A("N per group is stated correctly in the tick labels", True, "'Stage 1 (B n=19, T n=1)' ... 'Stage 4 (B n=12, T n=2)' equal table(); opened PNG"),
    A("The split violin keeps each condition on the same side at every stage, also when a cell is empty", False, "group ids 1,2,3,4,5,6 with odd = left: with stage-2 B removed, B is drawn right at stages 2-4 and T left, B left only at stage 1; boxes stay on the original sides (opened i4c_side_gg4.png, i4_split_missingB.png)"),
    A("Boxes and violins agree on which side belongs to which condition", False, "same rendering: box for B is dodged left while its half-violin is on the right at stages 2-4"),
    A("The Skill's N<30 rule is respected by its split-violin recipe", False, "cells n=1 (T stage 1, dropped with a warning) and n=2 (T stage 4, drawn as a KDE violin) are still plotted; recipe has no guard")],
    "Executed: run/i4_real_split.R, run/i4b_src.R, run/i4c_side.R (r.sh, ggplot2 4.0.3; i4c also r-gg35.sh). REAL data: Bioconductor ALL 1.48.0 (Chiaretti 2004), probe chosen by t-statistic; the missing-cell edge is a labelled subset.")

add(5, "Stress", "The shipped example examples/raincloud_phd.R: as shipped, with a data prelude, every plot rendered and checked, PDF export inspected",
    "The example is not standalone: df, df_small, df_med, df_large, df_paired are never created ('df' resolves to stats::df, error 'no applicable method for count applied to a function'). With a prelude it runs under ggplot2 3.5.2 (raincloud.pdf 88.9x69.85 mm, one embedded TrueType, no Type3) but under 4.0.3 it dies in its own ggsave and leaves a 1,031-byte blank PDF. The small-N panel labels every group n=80 while plotting 15 points, because N is counted on df, not df_small. Letter-value plot at N=2000 matches the medians and fourths; the split-violin medians match.",
    24, 34, [
    A("The shipped example runs as delivered", False, "'no applicable method for count applied to an object of class function' (df is stats::df); 5 objects undefined"),
    A("With a data prelude the example completes and exports the 89 x 70 mm PDF with embedded fonts", True, "ggplot2 3.5.2: raincloud.pdf 34,209 B, MediaBox 252x198 pt = 88.90 x 69.85 mm, 1 TrueType/FontFile2, 0 Type3"),
    A("On ggplot2 4.0.3 the example's export produces a usable raincloud.pdf", False, "ggsave error from gghalves; a 1,031-byte PDF with no fonts is left on disk (run/out/i5/raincloud_gg4_FAILED.pdf)"),
    A("N shown on the axis equals the number of points drawn", False, "p_small tick labels 'Ctrl (n=80)', 'Low (n=80)', 'High (n=80)' above 15 points per group (opened p_small.png); n_per_group is computed from df, plots use df_small; count(group) also counts NA rows"),
    A("The letter-value and split-violin panels match the data (N=2000 per group; 3 clusters x 2 conditions)", True, "LV M equals medians (2.79, 5.06, 3.84), F fourths within 0.4% of quantile(0.25/0.75), k=5 gives 5 levels; split-violin box medians equal per-cell medians")],
    "Executed: run/i5_example.R (r.sh then r-gg35.sh), run/i5_pdf.py, run/i5b_lv35.R, run/i5c_trim.R. SYNTHETIC prelude data (seed 11); the example itself unmodified from a copy in run/skill.")

n = len(inputs)
exe_avg = round(sum(i["total"] for i in inputs) / n, 1)
passed = sum(i["assertions_passed"] for i in inputs); total = sum(i["assertions_total"] for i in inputs)
static = {
 "functional_suitability": (8, 12, "Completeness 3, correctness 2, appropriateness 3. Sound decision table and the bars-of-means insight are verified, but the headline raincloud needs an archived package pinned to ggplot2 3.5, the N-label snippet errors, the nrd/Scott sentence is wrong, and ggdist is listed but never shown."),
 "reliability": (5, 12, "Fault tolerance 1, error reporting 2, recoverability 2. bw='SJ' blanks the whole panel on tied data with only a warning; the split violin swaps sides when a cell is missing; the example leaves a blank PDF on failure. The only guard is the generic 'introspect and adapt' note."),
 "performance_context": (6, 8, "267-line SKILL.md plus a short usage guide, no references layer needed; usage-guide Tips repeat SKILL.md content."),
 "agent_usability": (11, 16, "Learnability 3, consistency 2, feedback 3, error prevention 3. N thresholds disagree (table 200-1000 letter-value, rule >200, table >1000 KDE); R uses trim=FALSE with bw='SJ' while Python uses cut=0 with bw='scott'; 'drop the violin below N=30' contradicts the N=25 raincloud and the split-violin recipe. Failure-mode sections are good."),
 "human_usability": (7, 8, "Natural example prompts and a table-driven choice; input requirements (long format, column names) are implicit."),
 "security": (11, 12, "No credentials, shell, eval or network. Example writes raincloud.pdf into the cwd."),
 "maintainability": (7, 12, "Two prose files, no scripts; the shipped example is not runnable as delivered and has no data; no test data; usage-guide duplicates SKILL.md."),
 "agent_specific": (15, 20, "Precise trigger; related Skills all exist. Unseeded geom_jitter in the first recipe, example rewrites its output file, only a generic version escape hatch."),
}
cats = {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}
sub = sum(v[0] for v in static.values())
final = round(sub * 0.4 + exe_avg * 0.6, 1)
grade = "Production Ready" if final >= 85 else "Limited Release" if final >= 75 else "Beta Only" if final >= 60 else "Reject"
sym = {"Production Ready": "\u2b50", "Limited Release": "\u2705", "Beta Only": "\u26a0\ufe0f", "Reject": "\u274c"}[grade]

rep = {
 "meta": {"skill_name": SK,
  "description": "Plot per-group distributions of continuous data using boxplots, violins, beeswarms, quasirandom jitter, and raincloud plots with sample-size honesty (Weissgerber 2015), KDE-bandwidth awareness, and N-aware encoding choices.",
  "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Moderate", "n_inputs": n,
  "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/distribution-plots",
  "audit_type": "first audit (unmodified upstream GPTomics/bioSkills)",
  "executed": True,
  "execution_note": "Executed 5/5 inputs. R 4.4.3 via r.sh (ggplot2 4.0.3, ggbeeswarm 0.7.3, ggdist 3.3.3, lvplot 0.2.2, introdataviz) and r-gg35.sh (ggplot2 3.5.2 + gghalves 0.1.4, which fails on 4.0.3); Python via py.sh (seaborn 0.13.2, ptitprince 0.3.1, matplotlib 3.11.2, pandas 3.0.6). Every figure was checked by asserting on layer_data or artists against the input and the key PNGs were opened. Real data: Bioconductor ALL microarray; synthetic data labelled per input. Shipped example run from a copy in run/skill, no __pycache__ in the clone."},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "Citations (Weissgerber 2015 PLOS Biol 13:e1002128 with 703 papers, Allen 2019 Wellcome Open Res 4:63, Hofmann 2017 JCGS 26:469, McGill 1978, Sheather-Jones 1991) match the real papers; no fabricated statistic. The one factual error found is the nrd/Scott bandwidth sentence, recorded as P2."},
   "practice_boundaries": {"result": "PASS", "detail": "Plotting Skill for research data; no diagnostic, prescriptive or patient-level content."},
   "methodological_ground": {"result": "PASS", "detail": "No principled fallacy. Questionable advice recorded, not vetoed: trim=FALSE draws density beyond bounded data (down to -1.63 for expression with minimum 0) and the wrong nrd/Scott claim; the SJ-over-Silverman advice itself holds in a 3,600-draw simulation."},
   "code_usability": {"result": "PASS", "detail": "Every R and Python block parses and, with the right stack, runs: 4 of 5 R blocks and the Python blocks on ggplot2 4.0.3 / seaborn 0.13.2, the raincloud on ggplot2 3.5.2. Not vetoed because the Skill tells the agent to introspect and adapt and a working alternative exists (ggdist, run/i1b_ggdist.R), but the raincloud block fails on current ggplot2, the N-label snippet errors, and the shipped example is not standalone (P1)."}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": cats},
 "dynamic_score": {"execution_avg": exe_avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": total}, "inputs": inputs},
 "final": {"static_weighted": round(sub * 0.4, 1), "dynamic_weighted": round(exe_avg * 0.6, 1), "score": final, "max": 100, "grade": grade, "grade_symbol": sym,
           "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
 "key_strengths": [
  "The core message is right and verified on planted data: equal bars (4.990 vs 4.968) hide a bimodal group with 0 of 80 points near the mean; the decision table by N is sensible.",
  "Every drawn median, quartile, point count, fill and group order matched the input in all R blocks that render (12/12 probes on ggplot2 4.0.3, 13/13 on 3.5.2) and in the Python raincloud (25/80 points, medians 5.186/4.875).",
  "Sheather-Jones over the default bandwidth is supported by a 300-draw x 12-cell simulation (better in 10 cells, worse in 0); the notch formula and warning, quasirandom determinism and the tick-label N annotation all reproduce.",
  "The failure-mode sections and the cited literature are accurate and useful to an agent."],
 "recommendations": [
  {"priority": "P1", "title": "The headline R raincloud depends on gghalves, archived and broken on ggplot2 4.x",
   "observed_in": [1, 5], "problem": "geom_half_violin/geom_half_point fail on ggplot2 4.0.3 with 'argument \"layout\" is missing'; gghalves was archived on CRAN 2025-12-04; the example's own ggsave then leaves a 1,031-byte blank PDF. The Skill's version line says ggplot2 3.5+.",
   "root_cause": "The recipe was written against ggplot2 3.5 and the version note claims 3.5+ without a ceiling.",
   "fix": "State the ceiling (gghalves needs ggplot2 < 4.0) and give a ggdist raincloud that runs on 4.0.3 (stat_halfeye + geom_boxplot + jittered points; verified with medians equal, run/i1b_ggdist.R); make the example fail early with a clear message."},
  {"priority": "P1", "title": "bw = 'SJ' blanks the whole violin panel on tied or all-identical data",
   "observed_in": [3], "problem": "A single cluster with all-identical values (or 90% ties) makes stats::bw.SJ fail ('sample is too sparse to find TD'); ggplot2 only warns and draws an empty panel, exit 0. The usage guide recommends exactly this for single-cell violins.",
   "root_cause": "SJ is recommended unconditionally with no tie guard.",
   "fix": "Add a guard (n_distinct >= ~10 and tie fraction check, else bw = 'nrd0' with a stated reason) and a Common Errors row for 'Computation failed in stat_ydensity'."},
  {"priority": "P1", "title": "Split-violin recipe swaps sides when a cell is missing and does not enforce its own N rule",
   "observed_in": [4], "problem": "introdataviz::geom_split_violin picks the half by group-id parity, so an empty (cluster, condition) cell flips B/T for every later cluster while the dodged box stays put; n=1 and n=2 cells still get a KDE violin or a silent drop.",
   "root_cause": "The recipe assumes a complete cluster x condition grid.",
   "fix": "Complete the grid with tidyr::complete (or drop clusters without both conditions) before plotting, drop violins for n < 30, and say so in the recipe."},
  {"priority": "P1", "title": "The shipped example is not standalone and labels N from the wrong data frame",
   "observed_in": [5], "problem": "df, df_small, df_med, df_large and df_paired are never created (df falls through to stats::df); with data, the small-N panel labels every group n=80 above 15 points because n_per_group is computed on df; count(group) also counts NA rows.",
   "root_cause": "Example written as a fragment and N derived once from an unrelated frame.",
   "fix": "Build the five frames at the top (or read a shipped CSV), compute N per plot from the plotted frame with sum(!is.na(value)), and add a runnable data file."},
  {"priority": "P2", "title": "Wrong bandwidth sentence: nrd (Scott) is 1.178x nrd0, so it oversmooths more",
   "observed_in": [3], "problem": "The Silverman pitfall section says nrd oversmooths less than Silverman; bw.nrd/bw.nrd0 = 1.06/0.9 and nrd detected bimodality in 1 of 12 simulated cells where nrd0 was equal or better.",
   "root_cause": "Rule-of-thumb constants swapped.", "fix": "Say nrd0 (Silverman) < nrd (Scott) in bandwidth, SJ preferred; drop the sentence."},
  {"priority": "P2", "title": "stat_summary N-label snippet errors and tick-label N is not shown on raincloud/LV",
   "observed_in": [3, 5], "problem": "fun.data returns only label, so geom_text fails ('missing aesthetics: y'); the raincloud and letter-value recipes carry no N although the Skill says always annotate N.",
   "root_cause": "Snippet never run.", "fix": "Return data.frame(y = max(x), label = paste0('n=', sum(!is.na(x)))) with vjust, or use the tick-label form in every recipe."},
  {"priority": "P2", "title": "trim=FALSE with bounded data, and R/Python recipes disagree",
   "observed_in": [3, 5], "problem": "trim = FALSE draws density below 0 for expression (down to -1.63) and to -0.98 for a lognormal biomarker; Python uses cut=0. Python bw='scott' leaves the valley at 35% of the peak versus 3% for SJ.",
   "root_cause": "Blanket advice and no bounded-data caveat.", "fix": "Recommend trim = TRUE (or an explicit lower bound) for non-negative data and state the Python bandwidth limits (ptitprince has no SJ)."},
  {"priority": "P2", "title": "Inconsistent N thresholds and small-N guidance",
   "observed_in": [1, 4], "problem": "Table: letter-value 200-1000, KDE above 1000; operational rule: letter-value above 200; 'drop the violin below N=30' but the raincloud recipe is shown at N=25 and 30-200 is the raincloud band.",
   "root_cause": "Thresholds stated in three places.", "fix": "Keep one table and reference it."},
  {"priority": "P2", "title": "Deprecated seaborn/matplotlib usage and unseeded jitter",
   "observed_in": [1, 2], "problem": "boxenplot(palette=...) without hue warns and will be removed in seaborn 0.14; ptitprince triggers the matplotlib 3.13 vert removal; geom_jitter in the first recipe is unseeded so the figure changes each run while the Skill praises determinism.",
   "root_cause": "Older API forms.", "fix": "Pass hue with legend=False, note the ptitprince/matplotlib pin, and use position_jitter(seed=)."},
  {"priority": "P2", "title": "usage-guide.md repeats SKILL.md",
   "observed_in": [], "problem": "The Tips and What the Agent Will Do sections restate SKILL.md rules.", "root_cause": "Two files carry the same guidance.", "fix": "Reduce usage-guide.md to prompts and prerequisites."}]
}
assert len(inputs) == 5 and all(3 <= len(i["assertions"]) <= 5 for i in inputs)
json.dump(rep, open(D + "eval_report_%s_result.json" % SK, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("static", sub, "exe_avg", exe_avg, "final", final, grade, "assertions", passed, "/", total, "basic avg", sum(i["basic"] for i in inputs)/n, "spec avg", sum(i["specialized"] for i in inputs)/n)
