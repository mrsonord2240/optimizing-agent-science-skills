"""Builds eval_report_bio-phylo-divergence-dating_result.json from the scores decided in the audit.
Aggregates (averages, weighted scores, grade, floors) are computed here, not typed by hand."""
import json
import os

SKILL = "bio-phylo-divergence-dating"
SRC = "GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:phylogenetics/divergence-dating"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f"eval_report_{SKILL}_result.json")


def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}


static = {
    "functional_suitability": (9, 12, "Completeness 3: covers clock choice, calibration design, four engines, prior-only and "
        "temporal-signal checks; no BEAST2 tip-dating/FBD XML pattern and no root-to-tip or date-randomization code. "
        "Correctness 2: on PAML 4.10.10 the example ctl ('BDparas = 1 1 0.1') is rejected, bare 'usedata = 2' fails "
        "('file name empty'), the claim that '>'/'<' calibrations are silently ignored is false (bug existed only in "
        "4.9b-4.9d), and the Bio.Phylo prior-vs-posterior snippet does not compare node ages. Appropriateness 4."),
    "reliability": (8, 12, "Common Errors table and introspect-and-adapt rule help (fault tolerance 2, error reporting 3, "
        "recoverability 3), but one row is factually wrong ('>'/'<') and the two errors actually hit on PAML 4.10.10 "
        "(BDparas flag, in.BV filename) are absent."),
    "performance_context": (7, 8, "215-line SKILL.md plus 108-line usage guide, dense tables, no redundant steps; all content "
        "is loaded at once but it is compact."),
    "agent_usability": (13, 16, "Learnable (3) with excellent error prevention (4): fossil-as-minimum, effective prior, "
        "temporal signal, bare PL dates. Consistency 3: the shipped example writes RootAge = <1.0 while SKILL.md tells "
        "the agent to avoid '<' notation. Feedback design 3: 'specified vs effective vs posterior' and 'median + 95% HPD' "
        "are prescribed, but the code meant to produce them prints clade.confidence."),
    "human_usability": (6, 8, "Usage guide has natural prompts for every task type; the description is long and "
        "jargon-dense; off-spec requests are handled by routing to sibling Skills."),
    "security": (11, 12, "No credentials, no network, local tools only; shipped example writes into an OS temp dir "
        "without cleanup; no input sanity checks."),
    "maintainability": (8, 12, "Clear sections and one helper module (modularity 3, modifiability 3); testability 2: the "
        "example ships no data, never writes the calibrated tree file, its three ctl files share one output directory "
        "so mcmc.txt/FigTree.tre of the prior run are overwritten by the posterior run, and it was never run against "
        "PAML 4.10."),
    "agent_specific": (18, 20, "Precise trigger and routing to modern-tree-inference, bayesian-inference, tree-manipulation, "
        "tree-io and phylodynamics (all present); strong escape hatches (refuse to date without temporal signal, never "
        "a bare PL date). Progressive disclosure 3 (no references/), idempotency 3 (example uses seed = -1)."),
}

inputs = []


def add(index, type_, label, status, note, basic, spec, assertions, executed, exec_note):
    t = basic + spec
    flag = "✅" if (status == "COMPLETED" and t >= 75) else ("⚠️" if status == "COMPLETED" else "❌")
    inputs.append({"index": index, "type": type_, "label": label, "status": status, "status_flag": flag, "note": note,
                   "basic": basic, "specialized": spec, "total": t,
                   "assertions_passed": sum(a["result"] == "PASS" for a in assertions),
                   "assertions_total": len(assertions), "assertions": assertions, "executed": executed,
                   "execution_note": exec_note})


add(1, "Canonical", "MCMCTree fossil-calibrated dating, prior-only then approximate likelihood", "COMPLETED",
    "Prior (usedata=0), in.BV (usedata=3) ran; the Skill's bare 'usedata = 2' exits 1 on PAML 4.10.10, 'usedata = 2 in.BV' "
    "runs; all 7 true node ages inside the 95% HPD; effective prior on the L(0.15) node has mean 0.289, not the typed minimum",
    36, 48,
    [A("A prior-only (usedata = 0) run precedes the posterior run", True, "prior/ run, effective prior table produced"),
     A("The Skill's MCMCTree posterior step (usedata = 2) runs as written on PAML 4.10.10", False,
       "exit 1 'error: file name empty.'; pamlDOC p.48 documents 'usedata = 2 inBVfilename'"),
     A("Every true (simulated) node age lies inside the posterior 95% HPD", True, "7/7, e.g. AB 0.20 in [0.149, 0.300]"),
     A("Output reports specified vs effective prior vs posterior for each calibrated node", True,
       "AB: L(0.15) / 0.289 [0.134,0.572] / 0.222 [0.149,0.300]"),
     A("Fossil calibrations are encoded as soft minima or soft bounds, never points", True, "L(0.15,0.1,1,0.025), B() with 2.5% tails")],
    True, "mcmctree/baseml PAML 4.10.10 on SYNTHETIC 8-taxon 4 kb locus (runs/in1). Adapted: BDparas M flag and "
    "'usedata = 2 in.BV' after the as-written forms failed.")

add(2, "Variant A", "Temporal signal + LSD2 tip-dating on heterochronous virus data", "COMPLETED",
    "Root-to-tip slope 2.22e-3 (true 2e-3), R^2 0.987; LSD2 rate 1.94e-3 [1.54e-3, 2.28e-3], tMRCA 1996.79 [1994.74, 1998.40] "
    "(true 1996.98); date-randomization 20 reps max 7.3e-5, real CI outside -> signal passes",
    37, 53,
    [A("Both Skill IQ-TREE commands (ML tree; --date --date-ci 100) run as written", True, "exit 0 on IQ-TREE 2.4.0"),
     A("Root-to-tip regression reports slope, x-intercept, R^2 and residual outliers", True,
       "slope 2.22e-3, x-int 1997.98, R^2 0.987, 0 tips beyond 3 SD"),
     A("Date-randomization test is run and the real rate CI is compared with the randomized distribution", True,
       "20 shuffles; no overlap"),
     A("LSD2 rate and tMRCA confidence intervals contain the simulated truth", True, "rate 2e-3 and tMRCA 1996.98 bracketed"),
     A("Output states R^2 is exploratory (non-independent tips), not a formal test", True, "stated, per the Skill")],
    True, "IQ-TREE 2.4.0 + LSD2 on SYNTHETIC 30-tip serial-coalescent alignment (runs/in2). Root-to-tip and date "
    "randomization were implemented in Python (TempEst is GUI-only; the Skill gives no code for either).")

add(3, "Edge", "Virus samples spanning 0.4 yr: no temporal signal", "COMPLETED",
    "LSD2 still returns rate 4.2e-4 and tMRCA 1810 (CI to -1e9; truth 1976); root-to-tip R^2 0.094 with a spurious positive "
    "slope; real rate CI overlaps randomized 95% range [~0, 1.08e-3] -> output refuses to date",
    36, 50,
    [A("Output refuses to report a divergence date for this dataset", True, "no-signal verdict; recommends wider sampling span"),
     A("Date-randomization overlap is detected and used as the deciding test", True, "real CI [1e-10, 3.96e-3] overlaps"),
     A("R^2 < ~0.2 red flag and implausible x-intercept (2018.78) are reported", True, "both flagged"),
     A("The Skill's 'positive slope is mandatory' rule by itself rejects this dataset", False,
       "slope is positive (0.144, meaningless over 0.4 yr); only R^2 and the randomization test catch it")],
    True, "Same pipeline on SYNTHETIC no-signal set (runs/in3); verdict.py re-parses the LSD2 CI (negative bound broke "
    "the first regex - auditor script bug, not the Skill's).")

# Input 4 is filled from runs/in4 results (see IN4 block below)
IN4 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "in4", "in4_scores.json")))
add(4, "Variant B", IN4["label"], IN4["status"], IN4["note"], IN4["basic"], IN4["specialized"],
    [A(*a) for a in IN4["assertions"]], True, IN4["execution_note"])

add(5, "Stress", "Two loci, clock 2 vs 3, two chains; notation, RootAge and shipped example checks", "COMPLETED",
    "All 4 runs bracket 7/7 true ages, chains agree (max mean diff 0.0025); '>0.15'/'>0.35<0.55' read identically to "
    "L()/B(); RootAge = <1.0 works; shipped example ctl fails as written (BDparas), then needs a tree header and "
    "'usedata = 2 in.BV'",
    34, 47,
    [A("Two independent chains per clock model agree", True, "max |mean age difference| 0.0025 (clock 2), 0.0016 (clock 3)"),
     A("True node ages inside the 95% HPD under both clock models", True, "7/7 in all four runs"),
     A("The Skill's claim that '>'/'<' calibrations are silently ignored holds on PAML 4.10.10", False,
       "calibration block and effective priors identical to B()/L(); pamlHistory: bug only in 4.9b-4.9d"),
     A("Shipped examples/mcmctree_setup.py control files run as written", False,
       "all three exit 1 'BDparas: expect flag ... C ... M'"),
     A("Output reports effective prior vs posterior for every calibrated node", True, "table for 7 nodes")],
    True, "PAML 4.10.10, SYNTHETIC two-locus data (runs/in5). Strict-vs-relaxed was not settled by marginal likelihood "
    "(stepping-stone not run: time budget); reported as a limitation.")

add(6, "Scope Boundary", "Skyline Ne and Re requested from the tip-dated tree", "COMPLETED",
    "Routes Ne/Re to epidemiological-genomics/phylodynamics, hands over temporal-signal evidence, warns not to condition a "
    "skyline on the LSD2 point tree",
    37, 48,
    [A("Scope: no Ne or Re estimate is produced", True, "declined and routed"),
     A("Routes to the correct sibling Skill (epidemiological-genomics/phylodynamics, present in the repo)", True, "named"),
     A("States that LSD2 point dates are a cross-check and dating uncertainty must be integrated", True, "stated"),
     A("States the analysis concerns an outbreak population, not an individual", True, "research-only caveat given")],
    False, "Routing answer; nothing to execute (runs/in6/response.txt).")

add(7, "Adversarial", "PI demands a point fossil age and a bare TreePL date", "COMPLETED",
    "Point calibration B(0.399,0.401) pins (G,H) at 0.400 [0.399,0.401], excluding the true 0.45 and dragging EFGH to 0.694 "
    "and root to 0.922; soft minimum L(0.40) gives 0.491 [0.369,0.638]; TreePL prime/cv/bootstrap workflow written, "
    "not executed",
    37, 54,
    [A("Safety: output refuses to encode the fossil as a point age", True, "explains fossil = minimum"),
     A("Output demonstrates the too-young, falsely precise bias on data with known truth", True,
       "point HPD width 0.002 excludes truth; soft-min HPD contains it"),
     A("Output refuses a bare TreePL date and prescribes cross-validated smoothing plus bootstrap intervals", True,
       "prime -> cv/randomcv -> bootstrap trees"),
     A("TreePL configuration keys used exist in the treePL documentation", True, "prime, cv, randomcv, cvoutfile, mrca/min/max checked on the wiki")],
    True, "MCMCTree runs executed (runs/in7); TreePL NOT executed (no Windows build), keys checked against the treePL wiki.")

# ---- aggregates ----
sub = sum(v[0] for v in static.values())
tot = [i["total"] for i in inputs]
avg = round(sum(tot) / len(tot), 1)
P = sum(i["assertions_passed"] for i in inputs)
T = sum(i["assertions_total"] for i in inputs)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = round(sw + dw)
L1 = sum(i["basic"] for i in inputs) / len(inputs)
L2 = sum(i["specialized"] for i in inputs) / len(inputs)
tiers = ["Production Ready", "Limited Release", "Beta Only", "Reject"]
g = 0 if score >= 85 else 1 if score >= 75 else 2 if score >= 60 else 3
floors = {0: (80, 85, 32, 48, 0.9), 1: (70, 75, 28, 42, 0.8)}
missed = []
if g in floors:
    f = floors[g]
    for name, val, fl in (("static", sub, f[0]), ("execution", avg, f[1]), ("L1", L1, f[2]), ("L2", L2, f[3]),
                          ("assertions", P / T, f[4])):
        if val < fl:
            missed.append(f"{name} {val:.3g} < {fl}")
    if missed:
        g += 1
grade = tiers[g]
report = {
    "source": SRC,
    "meta": {"skill_name": SKILL,
             "description": "Estimate divergence times under molecular-clock models with BEAST2, MCMCTree/PAML, TreePL and "
                            "LSD2: calibration priors, effective-prior (sample-from-prior) checks, fossil minima and soft "
                            "bounds, tip-dating with temporal-signal tests, and clock-model choice.",
             "evaluated_on": "2026-09-15", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "A", "complexity": "Complex", "n_inputs": 7, "source": SRC,
             "executed": "6/7 inputs executed (PAML 4.10.10 mcmctree/baseml, IQ-TREE 2.4.0 + LSD2, BEAST 2.7.7 + "
                         "TreeAnnotator, Biopython 1.88, DendroPy 5.0.13); Input 6 is a routing answer",
             "execution_note": "All data SYNTHETIC (data/make_data.py): an 8-taxon time tree with known ages and lognormal "
                               "branch rates simulated with AliSim (two loci), a 30-tip heterochronous virus set with a "
                               "strict clock of 2e-3, and a 0.4-yr no-signal set. The shipped example and the Skill's "
                               "MCMCTree/BEAST/LSD2 commands and Python snippet were run as written first; TreePL and "
                               "TempEst were not executed (no Windows build / GUI only)."},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "Every number in the outputs comes from runs on synthetic data; "
                                     "citations in the Skill are real and correctly attributed; nothing fabricated."},
            "practice_boundaries": {"result": "PASS", "detail": "Evolutionary and outbreak-population dating only; nothing "
                                    "diagnoses, prescribes or triages an individual."},
            "methodological_ground": {"result": "PASS", "detail": "Fossil-as-minimum, effective-prior reporting, temporal-signal "
                                      "gating and refusal of bare PL dates were applied correctly; the Skill's misleading "
                                      "Bio.Phylo comparison snippet was replaced in the output, so no output carried the error."},
            "code_usability": {"result": "PASS", "detail": "All delivered code ran. Skill-supplied MCMCTree control lines "
                               "('BDparas = 1 1 0.1', bare 'usedata = 2') fail on PAML 4.10.10 with explicit messages and run after "
                               "the documented one-line fixes, as the Skill's adapt rule instructs; scored as P1 correctness "
                               "defects, not unrunnable code."}}},
    "static_score": {"subtotal": sub, "max": 100,
                     "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": P, "total": T}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade,
              "grade_symbol": {"Production Ready": "⭐", "Limited Release": "✅", "Beta Only": "⚠️", "Reject": "❌"}[grade],
              "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
    "key_strengths": [
        "Correct, current dating doctrine: fossils as minima with soft tails, specified vs effective prior vs posterior, "
        "and a tight HPD is not evidence the data informed a node",
        "Temporal-signal gate (root-to-tip plus date-randomization) correctly separated a signal dataset from a no-signal "
        "dataset on which LSD2 silently returned a date",
        "MCMCTree approximate-likelihood workflow, once its control lines are fixed, recovered all simulated node ages "
        "under independent and autocorrelated clocks with agreeing chains",
        "Clear routing to tree inference, Bayesian convergence, rooting, tree I/O and phylodynamics Skills, all present",
    ],
    "recommendations": IN4["recommendations_prefix"] + [
        {"priority": "P1", "title": "Fix MCMCTree control lines for PAML 4.10",
         "observed_in": [1, 5],
         "problem": "The example writes 'BDparas = 1 1 0.1' (rejected: 'expect flag ... C for conditional, M for multiplicative') "
                    "and SKILL.md/example use bare 'usedata = 2', which exits with 'file name empty.'",
         "root_cause": "Control-file syntax was written for PAML 4.9 and not re-tested on the 4.10 version the Skill claims.",
         "fix": "Write 'BDparas = 1 1 0.1 m' and 'usedata = 2 in.BV', and state that out.BV from usedata = 3 must be renamed/copied to in.BV."},
        {"priority": "P1", "title": "Remove the false '>'/'<' calibration claim",
         "observed_in": [5],
         "problem": "Common Errors says '>'/'<' calibrations are silently ignored; PAML 4.10.10 reads them identically to "
                    "L()/B() and the shipped example itself uses RootAge = <1.0.",
         "root_cause": "A 4.9b-4.9d parsing bug (pamlHistory) was generalised to all versions.",
         "fix": "Replace the row with: '>'/'<' bounds were mis-read only in PAML 4.9b-4.9d; prefer B()/L()/U() because they expose tail probabilities."},
        {"priority": "P2", "title": "Make examples/mcmctree_setup.py runnable end to end",
         "observed_in": [5],
         "problem": "It never writes the calibrated tree file (needed with an 'ntaxa ntree' header), puts all three runs in "
                    "one directory so mcmc.txt/FigTree.tre are overwritten, and uses seed = -1.",
         "root_cause": "The helper only prints configs and was never executed against data.",
         "fix": "Write the tree file with header, use one subdirectory and mcmcfile per run, copy out.BV to in.BV, set a fixed seed, and ship a tiny test alignment."},
        {"priority": "P2", "title": "Ship root-to-tip and date-randomization code",
         "observed_in": [2, 3],
         "problem": "Both temporal-signal tests are described but have no code (TempEst is GUI-only), and a positive slope "
                    "alone passed a no-signal dataset.",
         "root_cause": "The Skill defers to a GUI tool for its mandatory gate.",
         "fix": "Add a short Python/R root-to-tip regression with best-fitting root and an LSD2 date-shuffle loop; say a positive slope is necessary but not sufficient."},
        {"priority": "P2", "title": "Add a marginal-likelihood recipe for clock choice",
         "observed_in": [5],
         "problem": "The Skill says to decide strict vs relaxed by path sampling/stepping-stone but gives no command for "
                    "MCMCTree or BEAST2.",
         "root_cause": "Model comparison is delegated to bayesian-inference without an engine-specific pointer.",
         "fix": "Point to BEAST2 PathSampler/NS package and MCMCTree's mcmc3r stepping-stone workflow, or route explicitly."},
    ],
}
json.dump(report, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"static {sub} exec {avg} L1 {L1:.1f} L2 {L2:.1f} assertions {P}/{T} ({P/T:.1%}) final {sw}+{dw}={score} "
      f"grade {grade} floors missed {missed}")
