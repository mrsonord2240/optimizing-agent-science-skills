#!/usr/bin/env python
"""Builds eval_report_bio-outlier-splicing-detection_result.json and the eval viewer from the audit's recorded results.
All numbers below were printed by the scripts in run/scripts (logs in run/logs). Run: python 90_build_report.py"""
import json, os, io

ROOT = r"F:\OpenScience\audits\bio-outlier-splicing-detection"
SKILL = "bio-outlier-splicing-detection"
SRC = "mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/outlier-splicing-detection"
drop_rc = ""
p = os.path.join(ROOT, "run", "drop_demo", "run_rc.txt")
if os.path.exists(p):
    drop_rc = open(p, encoding="utf-8").read().strip().replace("\n", " | ")

static = {
    "functional_suitability": (8, 12, "Covers FRASER/OUTRIDER/LeafcutterMD/DROP/variant integration with a sound decision tree, but the FRASER and OUTRIDER blocks crash as written on the installed versions, the DROP init command fails, the MAE test is misdescribed (negative binomial, not z-score), the plotEncDimSearch comment is inverted and the Common Errors table quotes messages that do not exist in FRASER 2.6.1 / OUTRIDER 1.28.1."),
    "reliability": (7, 12, "Per-tool failure modes and tissue/cohort warnings are good, but the listed error strings are invented so an agent waits for errors that never come (n=8 runs silently), and there is no hard stop for n<20 or tissue mismatch."),
    "performance_context": (5, 8, "One 387-line SKILL.md plus a 69-line usage guide that repeats it; no references/ split; example covers FRASER only."),
    "agent_usability": (10, 16, "Clear structure and tables; inconsistent on thresholds (table |z|>=2 vs code zScoreCutoff=0; n>=20 'minimum' vs OUTRIDER power), FRASER 'autoencoder' wording vs PCA default, and no output/result-column specification (LeafcutterMD outputs, FRASER results columns)."),
    "human_usability": (6, 8, "Natural trigger wording and worked prompts; no input validation or guidance when inputs are off-spec."),
    "security": (9, 12, "No credentials or eval; quoted shell variables. Patient-derived RNA-seq and controlled-access GTEx controls (dbGaP) are suggested with no data-handling or access note; no licence caveat (see recommendations)."),
    "maintainability": (7, 12, "Version-pinned prose ('FRASER 2.0 >=1.99.0') is already wrong for two API points; a single example with hard-coded 'PATIENT_001' and bams/; no test data or expected output."),
    "agent_specific": (15, 20, "Good related-skill links (all target folders exist) and stop conditions for small cohorts and tissue choice; no research-use/clinical-boundary hand-off, and FRASER AE runs without a seed are not reproducible."),
}
static_sub = sum(v[0] for v in static.values())
assert static_sub == 67, static_sub

A = lambda t, r, n: {"text": t, "result": r, "note": n}
inputs = [
 dict(index=1, type="Canonical", label="FRASER2: one patient vs 29 controls, planted outliers (synthetic)", executed=True,
  prompt="I have RNA-seq for a rare-disease patient and 29 unaffected controls (BAMs in bams/). Run FRASER 2.0 with the Intron Jaccard Index and report aberrant junctions with padj<0.05 and |delta|>=0.1 for PATIENT_001.",
  status="COMPLETED", flag="⚠️", basic=28, spec=39,
  note="Shipped example and SKILL.md workflow crash verbatim on FRASER 2.2.0 and 2.6.1 (colData data.frame). With one-line DataFrame() fix, q=10: 3/4 planted splicing events found, 0 non-planted calls; cryptic donor missed at q>=5, found at q<=3.",
  execution_note="SYNTHETIC 30-sample 2x75 cohort (data/synth, seed 20260920) with 4 planted splicing events + 2 expression-only events + 1 tissue-mismatch sample. Verbatim example: 'is(value, DataFrame) is not TRUE' on both versions (logs 10, 11). Fixed workflow on FRASER 2.6.1 (as-drop) and 2.2.0 (Windows R): identical calls (S05 g010 skipping padj 4.8e-3, S20 g050 retention 3.4e-3, S25 g070 pseudoexon 3.6e-2). q sweep (PCA): q=1-3 -> 4/4, q=5-10 -> 3/4, q=15 -> 1/4; non-planted calls 0 throughout.",
  assertions=[
   A("The SKILL.md / shipped-example FRASER workflow runs verbatim from a clean copy", "FAIL", "FraserDataSet(colData=data.frame) errors on FRASER 2.2.0 and 2.6.1; needs S4Vectors::DataFrame()"),
   A("After the minimal fix, planted exon-skipping, intron-retention and pseudoexon events are flagged in the right sample and gene at padj<0.05, |dPsi|>=0.1", "PASS", "S05/g010 padj 4.8e-3 dPsi 0.52; S20/g050 3.4e-3 dPsi 0.79; S25/g070 3.6e-2 dPsi 0.63"),
   A("The Skill's default q=10 detects the planted cryptic-donor event (S12/g030, 60% usage)", "FAIL", "Not detected at q=5..15; detected at q=1..3 (padj 9e-3..1.3e-2) and by OHT estimateBestQ (q=1)"),
   A("False-positive rate stays low: no calls outside the planted sample/gene pairs", "PASS", "0 non-planted calls among 667 junctions x 30 samples at the stated cut-offs, every q tested"),
   A("Expression-only events (S15 g090 x0.05, S28 g100 x6) are not reported as splicing outliers", "PASS", "0 FRASER calls for both"),
  ]),
 dict(index=2, type="Variant A", label="OUTRIDER expression outliers, n=30 synthetic counts + OUTRIDER's own simulator", executed=True,
  prompt="Use OUTRIDER to find genes with aberrantly high or low expression in patient samples from this 30-sample count table (counts.tsv).",
  status="PARTIAL", flag="❌", basic=25, spec=32,
  note="SKILL.md OUTRIDER block: crashes on OUTRIDER 1.28.1 (estimateBestQ returns an object); runs on 1.24.0 but detects 0/8 planted outliers at n=30 (0/57 on OUTRIDER's own simulator; 67/115 at n=60).",
  execution_note="SYNTHETIC 3000x30 NB count matrix with 8 planted outliers (x0.05-x8), hidden batch on 25% of genes. Windows R OUTRIDER 1.24.0: q_best numeric (8), 'No significant events', 0 calls, 0 false. as-drop OUTRIDER 1.28.1: 'Error in is.numeric(q) & q > 1' because estimateBestQ(ods) returns an OutriderDataSet (bestQ(ods) is the accessor). Cohort-size check with makeExampleOutriderDataSet (2000 genes, freq 1e-3): m=12 0/14, m=30 0/57, m=60 67/115, m=100 116/192 (1 false call).",
  assertions=[
   A("The OUTRIDER snippet runs verbatim on the current installed release (1.28.1)", "FAIL", "OUTRIDER(ods, q = <OutriderDataSet>) -> 'operations are possible only for numeric, logical or complex types'"),
   A("The snippet runs and returns a scalar q on the release the Skill's comment describes (1.24.0)", "PASS", "class numeric, q=8 (n=30), 6 (n=12), 5 (n=8)"),
   A("Planted strong outliers are detected at the n>=20 cohort size the Skill calls 'Acceptable'", "FAIL", "0/8 planted at n=30; 0/57 on OUTRIDER's simulator at m=30; only 58% at m=60"),
   A("No false-positive expression outliers are reported", "PASS", "0 calls at padj<0.05 (0/90,000 tests)"),
   A("Cohort-size failure mode matches the Skill's stated symptom ('convergence warnings; uncalibrated p-values')", "FAIL", "Actual symptom is a silent 'No significant events' warning; no convergence warning at n=8..30"),
  ]),
 dict(index=3, type="Edge", label="FRASER with a cohort below the stated minimum (n=12 and n=8)", executed=True,
  prompt="I only have 11 controls (or 7). Can I still run FRASER on my patient?",
  status="COMPLETED", flag="⚠️", basic=29, spec=43,
  note="Skill's 'cohort <20 is insufficient' is borne out: a 75%-skipping planted event is missed at n=12 and n=8 with no error. The Common-Errors row 'FRASER: cohort too small' does not exist.",
  execution_note="Subsets of the synthetic cohort containing S05 (planted skipping). FRASER 2.6.1: q=10 (Skill default) and OHT q=2 both call 0 events at n=12 and n=8 (0 false). OHT prints 'Optimal latent space dimension is smaller than 2 ... set to 2'. String search over every function in FRASER 2.6.1 and OUTRIDER 1.28.1 for 'cohort too small' / 'convergence not reached' / 'encoding-dim search' found none (log 72).",
  assertions=[
   A("Advice for n<20 (insufficient / recruit more) agrees with observed behaviour", "PASS", "Strong planted event missed at n=12 and n=8 at both q=10 and OHT q=2"),
   A("Error strings quoted in Common Errors ('FRASER: cohort too small', 'estimateBestQ: convergence not reached') are produced by the tools", "FAIL", "Not present in either package; n=8 fit completes silently"),
   A("Small cohort gives no false positives", "PASS", "0 calls at n=12 and n=8"),
   A("Skill's tuning route (estimateBestQ useOHT=TRUE + bestQ) works and warns when the cohort is degenerate", "PASS", "estimateBestQ(fds,'jaccard',useOHT=TRUE) -> bestQ 2 with an explicit 'smaller than 2' message (2.6.1 only)"),
  ]),
 dict(index=4, type="Variant B", label="LeafcutterMD annotation-free outliers on the same synthetic cohort", executed=True,
  prompt="Run LeafcutterMD for annotation-free outlier intron usage on my cohort; is the patient outlier splicing detectable without annotation?",
  status="COMPLETED", flag="✅", basic=31, spec=44,
  note="SKILL.md bash block ran (regtools -> cluster -> leafcutterMD.R); exon skipping (p 5e-10) and cryptic donor (BH q 0.02) detected, 0 BH false positives; intron retention and pseudoexon give no p-value. Outputs and multiple-testing are not described.",
  execution_note="WSL as-core regtools 1.0.0 + as-rleaf leafcutter 0.2.9, 30 synthetic BAMs with XS:A tags (a first attempt with XS written as type Z gave strand '?', empty counts and a leafcutterMD crash: my data bug, fixed and regenerated). 86 clusters, 2580 cluster x sample tests; BH q<0.05: 11 (S29 tissue-mismatch sample 9, planted 2, other 0); raw p<0.05 outside planted/S29: 4 of 2492 (0.2%).",
  assertions=[
   A("The three-step bash block runs from a clean directory and writes <prefix>_pVals/_clusterPvals/_effSize", "PASS", "All three files written (86 x 30 cluster matrix, 257 x 30 intron matrices)"),
   A("Planted annotation-free events (skipping, cryptic donor) are flagged in the right sample", "PASS", "S05 raw p 5.0e-10 (q 6.4e-7); S12 raw p 6.9e-5 (q 0.020)"),
   A("Skill states that LeafcutterMD reports raw p-values needing correction, and what the three output files contain", "FAIL", "Only 'per-sample p-values per intron-cluster'; no BH advice, no file/column description"),
   A("Skill states the method's blind spots (junction-only: intron retention / pseudoexon clusters untested)", "FAIL", "S20 retention and S25 pseudoexon produced no cluster p-value; not mentioned"),
   A("No false positives at BH<0.05 outside the planted set and the tissue-mismatch sample", "PASS", "0 of 2492 tests"),
  ]),
 dict(index=5, type="Stress", label="DROP integrated pipeline: init, config, demo run on real chr21 RNA-seq", executed=True,
  prompt="Set up DROP for our diagnostic cohort (patient + in-house controls) and run aberrant splicing; check it works on the public demo first.",
  status="PARTIAL", flag="❌", basic=24, spec=36,
  note="`drop init my_diagnostic_run` fails as written; config prose does not match keys (run: true, implementation PCA); MAE described as a z-score test but DROP uses a negative binomial test. Demo (real chr21, 10 samples, 10 cores) reached results.tsv after about 85 min: 258 rows, 0 significant."
        + (" Pipeline status: " + drop_rc if drop_rc else ""),
  execution_note="WSL as-drop, DROP 1.6.1 (FRASER 2.6.1, OUTRIDER 1.28.1). Verbatim `drop init my_diagnostic_run`: 'Got unexpected extra argument'. mkdir+cd+`drop init` works and prints the CC-BY-NC notice; config.yaml has aberrantSplicing.run: true, implementation: PCA, deltaPsiCutoff 0.1, padjCutoff 0.1, quantileForFiltering 0.75; no rule file contains a `conda:` directive (so --use-conda is a no-op). `snakemake aberrantSplicing --cores 10` on a clean copy of the public demo: results.tsv (258 rows, min padjust 1, 0 significant; demo config has padjCutoff 1, deltaPsiCutoff 0.05); results_all 9820 rows. Not executed: mamba create (env pre-built by tooling pass), MAE and OUTRIDER modules, --use-conda on a fresh init.",
  assertions=[
   A("`drop init my_diagnostic_run` (as written) creates the project", "FAIL", "drop 1.6.1: 'Got unexpected extra argument (my_diagnostic_run)'; init takes no positional argument"),
   A("Config edit instructions ('aberrantSplicing: enabled', 'mae: enabled') match the generated config.yaml", "FAIL", "Keys are aberrantSplicing.run: true / mae.run: true; not mentioned that implementation defaults to PCA, not an autoencoder"),
   A("The MAE module description is accurate", "FAIL", "Skill: 'custom z-score test'; DROP's deseq_mae.R: negative binomial test (Kremer 2017)"),
   A("The demo aberrantSplicing target produces a results table with the documented FRASER columns", "PASS", "results.tsv with sampleID, hgncSymbol, pValue, padjust, deltaPsi, counts, totalCounts, potentialImpact, ...; 258 rows"),
   A("A 10-sample cohort behaves as the Skill predicts (below the n>=30 DROP guidance: no confident outliers)", "PASS", "0 of 258 rows with padjust<0.05 (min 1); Skill's own cut-offs on the fitted fds also give 0 calls"),
  ]),
 dict(index=6, type="Scope Boundary", label="SpliceAI hit + FRASER outlier integration, ACMG PS3 framing", executed=True,
  prompt="I have a SpliceAI hit at chr21:90190 in PATIENT_001; does FRASER support it? Give me the PS3 evidence for the report.",
  status="COMPLETED", flag="⚠️", basic=29, spec=41,
  note="dplyr join runs and returns only the concordant variant (decoy 40 kb away excluded). The Skill directs a 'clinical report' with an ACMG PS3 weight but gives no research-use / qualified-reviewer caveat, and omits that current FRASER/OUTRIDER are CC-BY-NC (Skill says MIT).",
  execution_note="SYNTHETIC SpliceAI-style hits (chr21:90190 d=0.85, chr21:130000 d=0.90, chr21:250233 d=0.40) joined to FRASER 2.6.1 results for PATIENT_001 (junction 90194-92840, padj 4.8e-3). Skill's block verbatim: 1 confirmed row (pos 90190). With chrom '21' vs 'chr21' the join silently returns 0 rows (as the Skill's error table says). The Skill does not say how to derive delta_max from SpliceAI's DS_* INFO fields; FRASER result columns match the join. Licence: FRASER 2.6.1 / OUTRIDER 1.28.1 LICENSE files say CC BY NC 4.0 (2.2.0/1.24.0: MIT).",
  assertions=[
   A("The variant-outlier join block runs verbatim and returns the concordant variant only", "PASS", "1 row (pos 90190, delta_max 0.85, junction 90194-92840); decoy 130000 excluded"),
   A("Output frames the result as candidate evidence, not a diagnosis", "PASS", "Skill says 'treat all outliers as candidates, not pathogenic'"),
   A("Where a clinical report / ACMG PS3 weight is requested the Skill supplies a research-use / qualified-clinician-review caveat", "FAIL", "usage-guide step 7 'Generate clinical report with PS3 functional evidence weight'; no caveat anywhere"),
   A("Skill discloses tool licensing relevant to diagnostic use", "FAIL", "Frontmatter license: MIT; installed FRASER/OUTRIDER 2.6.1/1.28.1 are CC BY NC 4.0 (DROP prints the notice)"),
  ]),
 dict(index=7, type="Adversarial", label="Tissue-mismatched patient: 'which gene causes her disease?'", executed=True,
  prompt="The patient's sample is fibroblast but 29 of my controls are blood-like. Run FRASER and tell me which gene is causing her disease.",
  status="COMPLETED", flag="⚠️", basic=26, spec=37,
  note="Skill's tissue-mismatch symptom ('hundreds of significant outliers') is not reproduced: default PCA calls 0 for the shifted sample (mismatch is invisible); AE q=10 calls 15 (13 genes). No QC step to detect mismatch is given.",
  execution_note="S29 = synthetic mismatch stand-in (half of genes have ~5x baseline exon skipping; a milder shift than a real tissue change). FRASER 2.6.1: PCA q=1..15 -> 0 calls for S29; AE q=10 -> 15 calls in 13 genes; AE q=5 -> 3; LeafcutterMD BH<0.05 -> 9 calls. Two AE runs with no seed differ (9,882 of 19,981 site p-values differ by >1e-6; only 12 of 25-28 p<0.001 cells shared); PCA and OUTRIDER AE are bit-identical run to run.",
  assertions=[
   A("Skill's warning that tissue mismatch inflates outlier calls is reproduced", "FAIL", "0 calls (PCA) to 15 calls (AE) for the shifted sample; not 'hundreds'"),
   A("Skill gives a check that would reveal the mismatch before interpretation", "FAIL", "Only 'strict tissue matching'; no sample-correlation / PCA / expression-tissue QC step"),
   A("Output does not name a causal gene or diagnose from outliers alone", "PASS", "Skill: outliers are candidates; verify tissue expression; RNA-only outlier may be cellular state or artefact"),
   A("Fit is reproducible across repeated runs on identical input", "FAIL", "FRASER AE (no seed) differs run to run; only the PCA default is deterministic; Skill gives no set.seed guidance"),
  ]),
]

n = len(inputs)
for i in inputs:
    i["total"] = i["basic"] + i["spec"]
    i["ap"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")
    i["at"] = len(i["assertions"])
    assert 3 <= i["at"] <= 5
exec_avg = round(sum(i["total"] for i in inputs) / n, 1)
sw = round(static_sub * 0.4, 1); dw = round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
grade = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
sym = {"Production Ready": "⭐", "Limited Release": "✅", "Beta Only": "⚠️", "Reject": "❌"}[grade]
ap = sum(i["ap"] for i in inputs); at = sum(i["at"] for i in inputs)
l1 = sum(i["basic"] for i in inputs) / n; l2 = sum(i["spec"] for i in inputs) / n

recs = [
 ("P1", "Main FRASER workflow and shipped example crash as written", [1, 3, 6, 7],
  "FraserDataSet(colData = <data.frame>) fails on FRASER 2.2.0 and 2.6.1 ('is(value, DataFrame) is not TRUE'), so SKILL.md and examples/fraser2_rare_disease.R stop at line 30.",
  "Snippets were never run against a released FRASER.",
  "Wrap the sample table in S4Vectors::DataFrame() in SKILL.md and the example; add a pass/fail print (n junctions, n calls) so the example asserts something."),
 ("P1", "Version-fragile API: estimateBestQ and plotEncDimSearch guidance", [1, 2, 3],
  "FRASER::estimateBestQ does not exist in 2.2.0 (optimHyperParams there); OUTRIDER::estimateBestQ returns a scalar in 1.24.0 but an OutriderDataSet in 1.28.1, so the OUTRIDER snippet crashes; plotEncDimSearch defaults to the OHT singular-value plot and returns NULL after useOHT=FALSE (the comment says the opposite; plotType='auc'/'loss' show the grid).",
  "Version line says 'FRASER 2.0 (>=1.99.0), OUTRIDER 1.20+' but the code targets Bioc 3.22 FRASER and Bioc 3.20 OUTRIDER.",
  "Pin one Bioconductor release, use bestQ(ods)/bestQ(fds, 'jaccard') after estimateBestQ in both tools, and correct the plotEncDimSearch comment."),
 ("P1", "OUTRIDER cohort-size guidance contradicts measured power", [2],
  "n=20-50 is called 'Acceptable' and n<20 fails with 'convergence warnings', but OUTRIDER on its own simulator detected 0/57 injected outliers at 30 samples and 67/115 at 60, with only a 'No significant events' warning.",
  "Single cohort table shared by FRASER and OUTRIDER.",
  "Give OUTRIDER its own size guidance (>=50-60 samples for useful power), and say that an empty result at n<50 is expected, not an error."),
 ("P1", "Default q=10 hard-coded; q advice does not match the data", [1, 3],
  "The example fixes q=10 although the text says to tune it; on a 30-sample cohort q=10 missed a 60%-usage cryptic donor that q<=3 and OHT found, and q=15 found 1/4. Text says q=8-15 typical and 5-8 for n=20-30.",
  "q ranges are convention, not derived; the example skips the estimateBestQ step it recommends.",
  "Call estimateBestQ(useOHT=TRUE)/bestQ in the example and use its value; state that q must stay well below n."),
 ("P1", "No research-use / clinical-boundary caveat, and licence misstated", [6],
  "The Skill positions FRASER/DROP for clinical diagnostics and the usage guide directs a 'clinical report with PS3 weight' with no research-use, validation or qualified-reviewer caveat; frontmatter says MIT while FRASER 2.6.1 / OUTRIDER 1.28.1 (and DROP) are CC BY NC 4.0.",
  "Clinical framing copied from programme descriptions without a boundary statement.",
  "Add a Practice Boundaries paragraph (candidate findings only; ACMG classification by a qualified geneticist; RNA-seq assay validation) and a licence note for commercial/diagnostic use."),
 ("P1", "DROP section: failing init command, wrong config and MAE description", [5],
  "`drop init my_diagnostic_run` errors in DROP 1.6.1; config keys are `run: true` (not 'enabled'); default implementation is PCA; MAE uses a negative binomial test (not a z-score test); `--use-conda` does nothing (no conda: directives); the 10-sample demo needs roughly 85 minutes on 10 cores.",
  "DROP steps written from memory of the docs.",
  "Use `mkdir run && cd run && drop init`, quote the real config keys, fix the MAE sentence, drop --use-conda, and state the runtime of the demo."),
 ("P1", "Invented error messages and unreproducible AE fits", [3, 7],
  "Common Errors lists 'FRASER: cohort too small', 'estimateBestQ: convergence not reached', 'OUTRIDER: encoding-dim search slow' which appear nowhere in FRASER 2.6.1/OUTRIDER 1.28.1; and FRASER correction='AE' without a seed differs run to run (12 of ~26 significant cells shared) with no set.seed advice.",
  "Table written from expectations rather than observed output.",
  "Replace the table with real messages (e.g. 'Optimal latent space dimension is smaller than 2', 'No significant events') and add set.seed() before any AE fit."),
 ("P1", "LeafcutterMD block lacks outputs, correction and limits", [4],
  "The block runs, but the Skill does not say the output files are _pVals/_clusterPvals/_effSize, that p-values are raw and need FDR control, where leafcutter_cluster_regtools.py lives, or that intron retention and some novel-exon clusters give no p-value.",
  "One-paragraph treatment of the tool.",
  "Add output description, a BH step (11 calls at q<0.05 vs 39 at raw p<0.05 on the test cohort) and the junction-only limitation."),
 ("P2", "Tissue-mismatch symptom and detection", [7],
  "'Hundreds of outliers' was not seen (PCA absorbed the shifted sample; AE flagged 15), and no QC step exposes mismatch.",
  "Claim stated without a check.",
  "Add a sample-correlation / PCA outlier check on the count matrix before fitting."),
 ("P2", "Threshold and default inconsistencies", [2, 1],
  "Quality table says OUTRIDER |z|>=2 but the code uses zScoreCutoff=0; example filter uses quantile=0.05/quantileMinExpression=1 versus FRASER defaults 0.75/10 (86% of junctions kept); FRASER 'Beta-binomial autoencoder' wording while the default fit is PCA.",
  "Parameters copied from different sources.",
  "Align table and code, explain the filter choice, and name PCA as default and AE as an option."),
 ("P2", "Integration block details and control-data access", [6],
  "delta_max is not a SpliceAI output column and no derivation is given; the 1 kb junction-end rule is a loose heuristic; chr-naming mismatch fails silently; pooling GTEx controls needs dbGaP access which is not mentioned.",
  "Block written as sketch.",
  "Show the DS_* -> delta_max step, add a chromosome-name assertion, and note controlled access for GTEx BAMs."),
 ("P2", "Single-file layout, one FRASER-only example", [],
  "387-line SKILL.md plus a usage guide repeating it; no references/ or test data; example hard-codes bams/ and PATIENT_001.",
  "No progressive disclosure.",
  "Move tool details to references/, add a tiny planted-outlier test set with expected output."),
]
recs = [dict(priority=p, title=t, observed_in=o, problem=pr, root_cause=rc, fix=f) for (p, t, o, pr, rc, f) in recs]

report = {
 "meta": {
  "skill_name": SKILL,
  "description": "Detects aberrant splicing in single rare-disease patients versus a control panel using FRASER 2.0, OUTRIDER, LeafcutterMD and the DROP pipeline (single-sample-versus-cohort outlier detection), with SpliceAI/FRASER variant-outlier integration, cohort-size, tissue-choice and hyperparameter guidance.",
  "evaluated_on": "2026-09-20",
  "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis",
  "execution_mode": "D",
  "complexity": "Complex",
  "n_inputs": n,
  "source": SRC,
  "data_note": "SYNTHETIC: 30-sample paired-end cohort with planted splicing/expression events (run/data/synth, 01_make_synth_cohort.py, seed 20260920), 3000x30 count matrix (run/data/outrider) and SpliceAI-style hits (run/scripts/80_integration.R). REAL: DROP public demo (10 chr21 RNA-seq BAMs). Versions: Windows R 4.4.3 FRASER 2.2.0 / OUTRIDER 1.24.0; WSL as-drop R 4.5.3 FRASER 2.6.1 / OUTRIDER 1.28.1 / DROP 1.6.1; regtools 1.0.0; leafcutter 0.2.9.",
  "grade_note": "Numeric score 67 (Beta Only band); not deployable. No veto fired: every runtime failure has a one-line fix and the Skill hedges outliers as candidates.",
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "References checked are real (Mertes 2021, Scheller 2023, Brechtmann 2018, Jenkinson 2020, Yepez 2021, Brown 2022, Klim 2019, Darman 2015, Walker 2023); no invented DOI/PMID or data. The quoted error messages in Common Errors are invented tool output and are recorded as a P1, not a fabricated result."},
   "practice_boundaries": {"result": "PASS", "detail": "No output diagnoses or names a causal gene; Skill says outliers are candidates, not pathogenic, and treats PS3 as one ACMG evidence line. Gap recorded as P1: 'clinical report with PS3 weight' has no research-use or qualified-reviewer caveat."},
   "methodological_ground": {"result": "PASS", "detail": "Single-sample-versus-cohort framing is correct; warns about tissue, batch, small cohorts and negative blood RNA-seq. OUTRIDER power guidance is over-optimistic (P1) but not a principled fallacy."},
   "code_usability": {"result": "PASS", "detail": "Code parses and every block ran after minimal edits (DataFrame wrapper, bestQ accessor, drop init without argument, wrapper path for leafcutter); verbatim, the FRASER, OUTRIDER (1.28.1) and drop init blocks fail. Recorded as P1 because each has a one-line fix and the Skill tells the agent to adapt on API errors."},
  },
 },
 "static_score": {"subtotal": static_sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
 "dynamic_score": {
  "execution_avg": exec_avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at},
  "inputs": [dict(index=i["index"], type=i["type"], label=i["label"], executed=i["executed"], execution_note=i["execution_note"], status=i["status"], status_flag=i["flag"], note=i["note"],
                  basic=i["basic"], specialized=i["spec"], total=i["total"], assertions_passed=i["ap"], assertions_total=i["at"], assertions=i["assertions"]) for i in inputs],
 },
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": False, "veto_override": False},
 "key_strengths": [
  "FRASER core claims hold on planted data: 3/4 events at the Skill's own settings and 4/4 at q<=3, 0 false positives, identical on FRASER 2.2.0 and 2.6.1",
  "Decision tree, tissue-choice and n<20 warnings are sound; the small-cohort advice is confirmed (strong event missed at n=8 and 12)",
  "LeafcutterMD block runs verbatim and finds the planted skipping and cryptic-donor events with no BH false positives",
  "Variant-outlier join returns only the concordant variant; all referenced files and sibling Skills exist; references are real",
 ],
 "recommendations": recs,
}
tp = os.path.join(ROOT, "eval_report_%s_result.json" % SKILL)
assert report["static_score"]["subtotal"] == sum(v["score"] for v in report["static_score"]["categories"].values())
with io.open(tp, "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print("score", score, grade, "exec_avg", exec_avg, "L1", round(l1, 1), "L2", round(l2, 1), "assertions", ap, "/", at)

# ------------------------------------------------------------------ viewer
L = []
L.append("# Eval Viewer — %s\nGenerated: 2026-09-20  |  Source: `%s`\n" % (SKILL, SRC))
L.append("Category: Data Analysis  |  Mode: D (hybrid)  |  Complexity: Complex -> 7 inputs  |  All 7 inputs executed (some partially: see notes)\n")
L.append("Data label: **SYNTHETIC** cohort and count matrix (generated, seed 20260920, truth in `run/data/synth/planted_truth.tsv`, `run/data/outrider/outrider_truth.tsv`); the DROP demo is real chr21 RNA-seq. BAMs and other large intermediates were deleted after the audit; `run/scripts/01_make_synth_cohort.py` (seed 20260920) regenerates the cohort (truth and gene counts were verified identical across two generator runs).\n")
L.append("## Step 1 — Skill Veto\nStability PASS (deterministic one-line fixes; PCA/OUTRIDER fits bit-identical run to run), Contract PASS, Determinism PASS (FRASER `correction='AE'` without a seed is not reproducible: noted P1), Security PASS.\n")
L.append("## Step 2 — Static score: %d/100\n" % static_sub)
L.append("| Category | Score | Note |\n|---|---|---|")
for k, v in static.items():
    L.append("| %s | %d/%d | %s |" % (k, v[0], v[1], v[2]))
L.append("\n## Step 3 — Classification\nData Analysis (category 3). Mode D: instructions plus R/bash/CLI code. Complexity Complex: four tools plus integration, branching decision tree, single-file Skill with one example -> N = 7.\n")
L.append("## Summary Table\n")
L.append("| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|---|")
for i in inputs:
    L.append("| %d | %s | %s | %d | %d | %d | %d/%d | %s |" % (i["index"], i["type"], "yes" if i["executed"] else "no", i["basic"], i["spec"], i["total"], i["ap"], i["at"], i["flag"]))
L.append("\n**Execution average: %.1f / 100**  |  **Assertion pass rate: %d/%d**  |  Layer 1 avg %.1f/40, Layer 2 avg %.1f/60\n" % (exec_avg, ap, at, l1, l2))
L.append("**Final = 67 x 0.4 + %.1f x 0.6 = %.1f + %.1f = %d -> %s %s, deployable = false** (Beta Only band 60-74; not deployable). Research Veto: M1 PASS, M2 PASS (with P1), M3 PASS, M4 PASS (with P1).\n" % (exec_avg, sw, dw, score, sym, grade))
L.append("## Environment and how it was run\nWindows R 4.4.3 (`r.sh`): FRASER 2.2.0, OUTRIDER 1.24.0. WSL `as-drop`: R 4.5.3, FRASER 2.6.1, OUTRIDER 1.28.1, DROP 1.6.1. WSL `as-core`/`as-rleaf`: regtools 1.0.0, leafcutter 0.2.9. Skill copied to `run/skill/` and run from copies (`run/ex_win`, `run/ex_drop`, `run/lmd`); nothing written under `external\\`. Every script is under `run/scripts/`, every printed result under `run/logs/`.\n")
L.append("Shipped-means-present: SKILL.md and usage-guide.md point at `examples/fraser2_rare_disease.R` (present) and Related Skills `splice-variant-prediction`, `differential-splicing`, `splicing-qc`, `variant-calling/clinical-interpretation`, `workflows/clinical-trial-pipeline` (all present). No missing primary file.\n")
detail = {
 1: """**Code** (`run/scripts/30_workflow.R`, the SKILL.md FRASER block verbatim except `S4Vectors::DataFrame()`), scored by `20_eval_lib.R`.
Verbatim example, both versions (`logs/10`, `logs/11`):
```
Error in checkSlotAssignment(object, name, value) :
  assignment of an object of class "data.frame" is not valid for slot 'colData' ... is(value, "DataFrame") is not TRUE
Calls: FraserDataSet ...
```
After the one-line fix (FRASER 2.6.1, `logs/31`, `logs/33`, `logs/34`; Windows 2.2.0 `logs/37` identical):
```
[q10] FRASER 2.6.1 | samples=30 | junctions kept=667 | total calls (padj<0.05,|dPsi|>=0.1)=4
  S05  g010 exon_skipping     : DETECTED n=2 min_padj=4.8e-03 max|dPsi|=0.52
  S12  g030 cryptic_donor     : not detected
  S20  g050 intron_retention  : DETECTED n=1 min_padj=3.4e-03 max|dPsi|=0.79
  S25  g070 pseudoexon        : DETECTED n=1 min_padj=3.6e-02 max|dPsi|=0.63
  S15/S28 expression-only     : FRASER calls=0
  non-planted calls (excl. S29): 0
```
q sweep (PCA, `logs/33`): q=1,2,3 -> 4/4; q=5,8,10 -> 3/4 (S12 missed); q=15 -> 1/4; false calls 0 in every fit. OHT `estimateBestQ(fds,'jaccard',useOHT=TRUE)` -> bestQ 1. AE q=10 -> 4/4 with 24 calls (15 in the mismatch sample S29). Example-script output on the patient (fixed): `2 aberrant junctions in PATIENT_001 (padj<0.05, |delta|>=0.1)`: the skipping junction chr21:90194-92840 (dPsi +0.50) and the lost inclusion junction 91783-92840.""",
 2: """**Code** (`run/scripts/40_make_counts.R`, `41_outrider.R` = SKILL.md OUTRIDER block, `43_outrider_builtin.R`).
OUTRIDER 1.28.1 (`logs/44`): `estimateBestQ returned class: OutriderDataSet` then `Error in is.numeric(q) & q > 1 : operations are possible only for numeric, logical or complex types`.
OUTRIDER 1.24.0 (`logs/41`): `estimateBestQ returned class: numeric value: 8`, `Warning: No significant events`, `detected 0/8 planted; non-planted calls: 0`. Debug (`42`): planted gene101 in S03 has z -4.5, p 3.7e-5, padj 0.95.
OUTRIDER's own simulator with the Skill's code path (`logs/43`):
```
m=12  samples n=2000 genes: q=6  injected=14  detected=0/14
m=30  samples n=2000 genes: q=8  injected=57  detected=0/57
m=60  samples n=2000 genes: q=13 injected=115 detected=67/115 false calls=0
m=100 samples n=2000 genes: q=20 injected=192 detected=116/192 false calls=1
```""",
 3: """**Code** (`run/scripts/36_small_cohort.R`; FRASER 2.6.1; patient + 11 or 7 controls), `logs/36`:
```
[n=12 q=10 (Skill default)] ... total calls=0   S05 g010 exon_skipping : not detected
Optimal latent space dimension is smaller than 2 ... For now, the latent space dimension is set to 2.
[n=12 q=OHT 2] ... total calls=0   S05 g010 exon_skipping : not detected
[n=8  q=10 (Skill default)] ... total calls=0   S05 g010 not detected
```
`72_grep_errors.R` (`logs/72`): `FRASER 2.6.1 : matches -> NONE`, `OUTRIDER 1.28.1 : matches -> NONE` for 'cohort too small', 'convergence not reached', 'encoding-dim search'.""",
 4: """**Code** (`run/scripts/60_leafcutterMD.sh` = SKILL.md bash block; `61_eval_lmd.py`), `logs/60`, `logs/61`:
```
Wrote 480 clusters... Split into 86 clusters...   ->   patient_outlier_clusterPvals.txt / _effSize.txt / _pVals.txt
cluster p-value matrix: (86, 30); intron matrices (257, 30); tested cluster-sample pairs 2580; raw p<0.05: 39; BH q<0.05: 11
S05 g010 exon_skipping   : raw p=4.96e-10 BH q=6.40e-07 DETECTED
S12 g030 cryptic_donor   : raw p=6.86e-05 BH q=1.97e-02 DETECTED
S20 g050 intron_retention: no cluster tested       S25 g070 pseudoexon: no cluster tested
NON-planted, excl. S29: raw p<0.05: 4 (of 2492; 0.2%); BH q<0.05: 0.   S29 tissue-mismatch BH q<0.05: 9
```
Data bug found and fixed on the way: my first BAMs stored XS as type Z; regtools wrote strand '?', leafcutter produced an empty counts file and leafcutterMD failed with 'non-character argument'. Regenerated with XS:A (truth and counts unchanged).""",
 5: """**Code** (`run/scripts/51_drop_init.sh`, `50_drop_demo_run.sh`, `52_drop_real_fds.R`), `logs/51`, `logs/53`:
```
drop, version 1.6.1
$ drop init my_diagnostic_run   ->  Error: Got unexpected extra argument (my_diagnostic_run)
$ mkdir my_diagnostic_run; cd my_diagnostic_run; drop init   ->  init...done  (+ CC-BY-NC 4.0 licence warning)
aberrantSplicing:  run: true  implementation: PCA  FRASER_version: "FRASER2"  deltaPsiCutoff: 0.1  padjCutoff: 0.1  quantileForFiltering: 0.75
Scripts/: files containing 'conda:' = 0   (so --use-conda is a no-op)
Scripts/MonoallelicExpression/pipeline/MAE/deseq_mae.R: rmae <- DESeq4MAE(mae_counts) ## negative binomial test for allelic counts
```
Demo, clean copy, `snakemake aberrantSplicing --cores 10` (about 85 min to results): `results.tsv rows 258 samples 10; padjust<0.05: 0; min padjust 1; |deltaPsi|>=0.1 rows: 149`; `results_all rows 9820, min pValue 0.015`. FRASER 2.6.1 on the fitted demo fds with the Skill's cut-offs (padj<0.05, |dPsi|>=0.1): 0 calls in 10 samples (bestQ 2, 982 junctions).
Pipeline final status: """ + (drop_rc or "see run/drop_demo/run.log") + ".",
 6: """**Code** (`run/scripts/80_integration.R`, Skill's dplyr block verbatim on SYNTHETIC hits), `logs/80`:
```
  chrom   pos delta_max start   end   padjust deltaPsi
1 chr21 90190      0.85 90194 92840 0.0047689      0.5
confirmed rows: 1 distinct variants: 1   (decoy at 130000 excluded)
with '21' vs 'chr21': join returns 0 rows (silent empty, no warning)
```
Licence (`logs/71`): FRASER/OUTRIDER 2.6.1/1.28.1 `LICENSE`: "provided under the CC BY NC 4.0 license for academic and non-commercial use"; 2.2.0/1.24.0: MIT. Skill frontmatter: `license: MIT`.""",
 7: """**Code** (`33_sweep_q.R` AE runs, `45_determinism.R`, `46_determinism_ae.R`, `61_eval_lmd.py`), `logs/34`, `logs/45`:
```
[AE q=10] total calls=24 ... S29 tissue-mismatch sample calls: 15 (distinct genes 13)     [AE q=5] S29 calls: 3     [PCA q=1..15] S29 calls: 0
OUTRIDER (AE, q=8, no seed) run1 vs run2: max |dP| = 0
FRASER PCA q=5 run1 vs run2: max |dlog10 P| = 0
FRASER AE q=5 (no seed): max |dP| = 0.93; cells with |dP|>1e-6: 9882 of 19981; p<0.001 run1 28, run2 25, both 12
```""",
}
for i in inputs:
    L.append("### Input %d — %s (%s)\n**Prompt:** %s\n\n**Executed:** %s. %s\n\n%s\n\n**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100 | %s\n\n**Assertions:**" % (
        i["index"], i["type"], i["label"], i["prompt"], "true" if i["executed"] else "false", i["execution_note"], detail[i["index"]], i["basic"], i["spec"], i["total"], i["flag"]))
    for a in i["assertions"]:
        L.append("- [%s] %s — %s" % (a["result"], a["text"], a["note"]))
    L.append("Assertion pass rate: %d/%d\n" % (i["ap"], i["at"]))
L.append("## Research Veto\nM1 PASS, M2 PASS (P1: no research-use / clinical-boundary caveat; licence misstated), M3 PASS (P1: OUTRIDER power), M4 PASS (P1: verbatim FRASER / OUTRIDER 1.28.1 / `drop init` fail, one-line fixes).\n")
L.append("## Recommendations\n")
for r in recs:
    L.append("**[%s] %s**  (inputs %s)\n- Problem: %s\n- Root cause: %s\n- Fix: %s\n" % (r["priority"], r["title"], r["observed_in"], r["problem"], r["root_cause"], r["fix"]))
with io.open(os.path.join(ROOT, "eval_viewer_%s.md" % SKILL), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L))
print("viewer written")
