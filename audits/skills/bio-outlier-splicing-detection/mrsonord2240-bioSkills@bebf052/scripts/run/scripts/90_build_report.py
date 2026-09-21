# Build eval_report_bio-outlier-splicing-detection_result.json and the viewer from the numbers measured in run/logs.
import io, json, os
run = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.dirname(run)
SHA = "bebf0525bf72d2737fd3404d1b1abe7e51f050b7"
SRC = "mrsonord2240/bioSkills@%s:alternative-splicing/outlier-splicing-detection" % SHA

static = {
 "functional_suitability": (10, 12, "Covers FRASER 2, OUTRIDER, LeafcutterMD, DROP and SpliceAI integration with a sound decision tree. Every block ran on the installed releases (FRASER 2.6.1 block 4/4 planted events, OUTRIDER block on 1.24.0 and 1.28.1, LeafcutterMD, integration, DROP init). Two blocks are not portable as written: the FRASER block calls estimateBestQ, which FRASER 2.2.0 lacks (the block comment says so; the example handles it), and it stops at its last line when no sample has a call."),
 "reliability": (9, 12, "Common Errors rebuilt from messages seen in runs; cohort sizes measured (FRASER n>=20, OUTRIDER n>=50 reproduced). Open: the FRASER block errors ('argument 1 is not a vector') on empty results at n=8/12/16, the scenario the Skill itself predicts; the 'smaller than 2' OHT message is placed at n=8-12 but appeared only at n=4; the AE reproducibility recipe is wrong."),
 "performance_context": (5, 8, "One 392-line SKILL.md; usage-guide cut to 35 lines and no longer repeats it (redundancy fixed); no references/ split; one example."),
 "agent_usability": (13, 16, "Clear tables and a decision tree; thresholds now consistent (zScoreCutoff 0, PCA default, filter defaults), outputs of LeafcutterMD named, integration block derives delta_max. The example comment ('AE needs set.seed()') and SKILL.md ('SerialParam(RNGseed=1) does') disagree, and both are incomplete."),
 "human_usability": (7, 8, "Natural prompts, per-scenario guidance, example takes arguments and warns for n<20; no input validation beyond the patient-id check."),
 "security": (11, 12, "Research-use-only statement, licence statement checked against the installed LICENSE files (CC BY-NC 4.0 for FRASER 2.6.1 / OUTRIDER 1.28.1 / DROP 1.6.1, MIT for 2.2.0 / 1.24.0), dbGaP note for GTEx BAMs. No credentials, quoted shell variables."),
 "maintainability": (9, 12, "Version line dated and checked on two release pairs; measured numbers carry their conditions. Still no shipped test data or expected output; the generator lives only in the audit."),
 "agent_specific": (16, 20, "Related-skill links exist; stop conditions for cohort size and tissue; clinical hand-off removed (no PS3/PP3 directive). Two unsourced tables remain (tissue 'genes captured' percentages, disease-specific expectations) and the tissue-mismatch check cannot see a sample the PCA fit has absorbed."),
}
static_total = sum(v[0] for v in static.values())
assert static_total == 80

I = []
def inp(i, typ, label, status, note, basic, spec, assertions):
    p = sum(1 for a in assertions if a[1] == "PASS")
    total = basic + spec
    flag = "✅" if (status == "COMPLETED" and total >= 75) else ("⚠️" if status == "COMPLETED" else "❌")
    I.append(dict(index=i, type=typ, label=label, status=status, status_flag=flag, note=note, basic=basic, specialized=spec, total=total,
                  assertions_passed=p, assertions_total=len(assertions), executed=True,
                  execution_note=note, assertions=[dict(text=a[0], result=a[1], note=a[2]) for a in assertions]))

inp(1, "Canonical", "FRASER 2: one patient vs 29 controls, planted outliers (synthetic; REGRESSION of pre-fix input 1)", "COMPLETED",
 "SYNTHETIC 30-sample 2x75 cohort A regenerated from the audit generator (seed 20260920; truth and gene counts byte-identical to the pre-fix run). SKILL.md FRASER block run verbatim (extracted to run/blocks/01_r.R) on FRASER 2.6.1 (WSL as-drop): completes, 667 junctions, bestQ 1, 4/4 planted events flagged in the right sample and gene (S05/g010 padj 2.8e-5, S12/g030 9.3e-3, S20/g050 9.1e-4, S25/g070 3.6e-3), 0 non-planted calls, expression-only S15/S28 not called, S29 mismatch sample 0 calls. The same block on FRASER 2.2.0 (Windows R via r.sh) stops at estimateBestQ (could not find function; the block comment says 2.2.0 has only optimHyperParams). The shipped example run from a clean copy on both versions: 667 junctions kept, q=1 (2.6.1) / q=2 (2.2.0, optimHyperParams), 3 aberrant junctions in PATIENT_001 (chr21:90194-92840 padj 2.8e-5 dPsi +0.70, 91783-92840, 90194-91550), 6 calls in all samples on both, volcano PDF written (35 KB).",
 36, 51, [
 ("SKILL.md FRASER block runs verbatim from a clean directory on FRASER 2.6.1 and finishes", "PASS", "was FAIL pre-fix (colData data.frame); now 667 junctions, bestQ 1, results table produced"),
 ("The shipped example runs from a clean copy on FRASER 2.6.1 and 2.2.0 with arguments and prints a checked result", "PASS", "'3 aberrant junctions in PATIENT_001 ...; 6 in all samples' on both versions; junctions kept and q printed"),
 ("All four planted splicing events (skipping, cryptic donor, retention, pseudoexon) are flagged at padj<0.05, |dPsi|>=0.1 in the right sample and gene", "PASS", "4/4 (pre-fix: 3/4, cryptic donor missed at q=10); S12 flagged with the OHT q"),
 ("No calls outside the planted sample/gene pairs; expression-only events are not reported as splicing outliers", "PASS", "0 non-planted calls; S15 and S28 0 calls; S29 (shifted stand-in) 0 PCA calls, as the Skill states"),
 ("The SKILL.md block runs verbatim on every release named under Version Compatibility (FRASER 2.2.0 and 2.6.1)", "FAIL", "2.2.0: 'could not find function estimateBestQ'; documented in the block comment and handled by the example, not by the block"),
])

inp(2, "Variant A", "OUTRIDER expression outliers on synthetic counts, n=30 and n=100, plus OUTRIDER's simulator (REGRESSION of pre-fix input 2, plus a new n=100 matrix)", "COMPLETED",
 "SYNTHETIC. SKILL.md OUTRIDER block run verbatim (blocks/02_r.R) on OUTRIDER 1.24.0 (Windows R) and 1.28.1 (as-drop). Pre-fix matrix (3000x30, 8 planted): both versions run to the end; q_best 8 (1.24.0) / 2 (1.28.1, OHT gave 1, raised to 2 by the block); 0/8 detected, 0 false calls, 'No significant events' warning, exactly what the Skill now says for n<50. NEW matrix (3000x100, 20 planted, seed 5150, hidden batch): 1.24.0 q=20 2/20, 1.28.1 q=2 9/20 with 1 false call. NEW OUTRIDER-simulator matrix (2000 genes, m=100, freq 1e-3, 192 injected, seed 42): 1.24.0 116/192 (60%, 1 false), 1.28.1 135/192 (70%, 0 false); the Skill's 3-seed table says 71% / 74% at n=100. No crash on either version (pre-fix: 1.28.1 crashed on the q object). One as-drop run of the simulator matrix died with 'error writing to connection' (MulticoreParam workers killed while the machine was under memory load) and passed on retry.",
 35, 50, [
 ("The OUTRIDER block runs verbatim on the current release (1.28.1) and returns a numeric q > 1", "PASS", "was FAIL pre-fix; q 2 (n=30, n=100), 13 (simulator)"),
 ("The block runs verbatim on 1.24.0 (the release its comment describes)", "PASS", "q 8 / 20 / 20"),
 ("Cohort-size claim: essentially no power at n<=30, 40-75% around n=50-100", "PASS", "0/8 at n=30 on both versions; 60% and 70% at m=100 on one seed (table 71% / 74%)"),
 ("No false-positive outliers beyond the stated 0-2", "PASS", "0, 0, 0, 1, 1, 0 false calls across the six fits"),
 ("Failure-mode text matches the observed symptom (silent 'No significant events', no convergence warning)", "PASS", "warning seen at n=30 on both versions, no convergence warning"),
])

inp(3, "Edge", "FRASER below and around the stated minimum: patient + 7, 11, 15, 19, 24 controls (REGRESSION of pre-fix input 3)", "COMPLETED",
 "SYNTHETIC subsets of cohort A (patient + first n-1 controls by name), SKILL.md block verbatim each time, FRASER 2.6.1. n=8, 12, 16: 0 calls in any sample, planted skipping S05 not detected, 0 false calls; the block then stops with 'argument 1 is not a vector' at order(patient_results$padjust) because results() returned an empty table with no columns (3 of 3 runs; the shipped example guards this). n=20: 3 calls (S05 skipping padj 6.4e-3, S20 retention 3.0e-2), cryptic donor S12 not detected. n=25: 5 calls (S05, S20, S25; S12 not detected). n=30: 4/4 (input 1). OHT bestQ 2 at n=8-25 with the message 'Optimal encoding dimension: 2', not the 'smaller than 2' warning the Skill places at n=8-12; that warning appears only at n=4 (input 9). Pre-fix claim that 'cohort too small' / 'convergence not reached' exist is gone from the Skill.",
 31, 44, [
 ("Advice for n<20 (missed at n=8-16, recruit more) agrees with observed behaviour", "PASS", "0 calls and S05 missed at n=8, 12, 16; detected at n=20 and 25"),
 ("Small cohorts give no false positives", "PASS", "0 non-planted calls at n=8, 12, 16, 20, 25"),
 ("The SKILL.md block runs to its last line when the outlier set is empty (the case the Skill predicts for n<20)", "FAIL", "'argument 1 is not a vector' at n=8, 12, 16; example has an nrow>0 guard, block does not"),
 ("Common Errors row: 'Optimal latent space dimension is smaller than 2 ... set to 2 (seen at n=8-12)'", "FAIL", "not printed at n=8-25; printed at n=4 (real data). Message text itself is genuine"),
 ("'n=20, 25: flagged (3 junctions)' cohort-size sentence", "PASS", "n=20: 3 calls; n=25: 5 calls with 3 of 4 planted events; same order of magnitude, composition of controls matters"),
])

inp(4, "Variant B", "LeafcutterMD annotation-free outliers on the same cohort (REGRESSION of pre-fix input 4)", "COMPLETED",
 "SYNTHETIC cohort A BAMs (XS:A tags). Block blocks/03_bash.sh run verbatim in WSL, one substitution (`python leafcutter_cluster_regtools.py` -> the same script from the leafcutter repo on PATH, since the block assumes it is in the working directory): 30 .junc files, clustering wrote 480 clusters -> 86, leafcutterMD wrote patient_outlier_clusterPvals.txt (86x30), _pVals.txt and _effSize.txt (257x30). BH block (blocks/04_r.R) run verbatim: 2580 cluster-sample tests, 39 raw p<0.05, 11 at BH q<0.05 = S05 skipping (q 6.4e-7), S12 cryptic donor (q 2.0e-2), 9 in the mismatch sample S29, 0 elsewhere. S20 retention and S25 pseudoexon have no cluster p-value, as the Skill now says.",
 35, 52, [
 ("The bash block runs from a clean directory and writes _pVals, _clusterPvals and _effSize", "PASS", "all three written with the shapes the Skill describes"),
 ("Planted skipping and cryptic-donor events flagged in the right sample by the BH block", "PASS", "S05 q 6.4e-7; S12 q 2.0e-2"),
 ("The R BH snippet reproduces the pre-fix count of 11 hits at q<0.05 and controls the raw p-values", "PASS", "11 of 39 raw; 0 false hits outside S29"),
 ("Junction-only limitation stated and true", "PASS", "no cluster tested for the retention (S20) and pseudoexon (S25) events"),
 ("Output files and script locations are named well enough to run without guessing", "PASS", "files named; clustering script path named in text; the block itself still needs the path prefixed"),
])

inp(5, "Stress", "DROP: init, config and pipeline claims (REGRESSION of pre-fix input 5; demo cited, not re-run)", "COMPLETED",
 "WSL as-drop, DROP 1.6.1 (FRASER 2.6.1, OUTRIDER 1.28.1). The block's setup lines run: `mkdir my_diagnostic_run && cd ... && drop init` works and prints the CC-BY-NC 4.0 notice. config.yaml checked by script against the block's comment: aberrantSplicing run: true, implementation PCA, FRASER_version \"FRASER2\", padjCutoff 0.1, deltaPsiCutoff 0.1; aberrantExpression run: true, implementation autoencoder; mae run: true; keys sampleAnnotation, geneAnnotation, genome, root, htmlOutputPath all present. No rule file contains a `conda:` directive (0 files), so omitting --use-conda is right. deseq_mae.R comment: 'negative binomial test for allelic counts'. NOT re-run: the ~90-minute demo (the earlier completed run is cited: 63/70 steps, results.tsv written for group fraser with 258 rows, min padjust 1, 0 significant; the run was killed by its own 100-minute timeout in step 08 of group fraser_external), MAE and OUTRIDER modules, `mamba create`. A dry-run of `snakemake aberrantSplicing` on the bare init directory fails on missing config inputs, as expected without data.",
 32, 46, [
 ("`mkdir && cd && drop init` creates the project (the pre-fix `drop init <name>` failed)", "PASS", "init...done in DROP 1.6.1"),
 ("Config keys and values quoted in the block match the generated config.yaml", "PASS", "checked by script: run: true x3, PCA, FRASER2, 0.1, 0.1, autoencoder"),
 ("`snakemake` without --use-conda is right", "PASS", "0 rule files contain conda:"),
 ("MAE description (negative-binomial test, not z-score) is accurate", "PASS", "deseq_mae.R: 'negative binomial test for allelic counts'"),
 ("Demo runtime and result statement ('about 85 minutes on 10 cores, no significant outlier')", "PASS", "cited from the earlier completed run, not re-run; runtime to results was about 90 minutes and the full target did not finish within 100"),
])

inp(6, "Scope Boundary", "SpliceAI + FRASER integration and research-use boundary (REGRESSION of pre-fix input 6, on real SpliceAI output)", "COMPLETED",
 "Block 06 (bcftools query) and block 07 (R) run verbatim. Input VCF = the REAL SpliceAI examples/output.vcf (10 records, multi-allelic, unscored alleles) plus 4 SYNTHETIC chr21 records in real SpliceAI INFO format; FRASER results = the shipped example's real output for PATIENT_001. With `chr21` and with `21` contigs: 13 variants parsed, delta_max 0.19-1.0, confirmed = positions 90190 (delta 0.85, junction 90194-92840) and 92000 (delta 0.30 taken from the second allele of 'SpliceAI=.,T|...', junction end 840 bp away); decoys 130000 and 250233 excluded; the real chrX/chr1/chr21 records excluded. With a VCF holding only chrX records the block stops at its own stopifnot (no chromosome overlap). With the real records only: 0 rows, correct. Scope: SKILL.md now states research use only, no PS3/PP3 or clinical report; usage-guide has no report step. Licence text matches the installed LICENSE files (FRASER 2.6.1 / OUTRIDER 1.28.1 CC BY NC 4.0; 2.2.0 / 1.24.0 MIT).",
 36, 53, [
 ("The integration blocks run verbatim on real SpliceAI output with multi-allelic and unscored ('.') alleles and return only the concordant variants", "PASS", "positions 90190 and 92000 only, decoys excluded"),
 ("chr21 vs 21 naming does not silently give an empty join", "PASS", "both spellings give the same two positions"),
 ("The chromosome-overlap guard fires when nothing overlaps", "PASS", "'any(variants$chrom %in% fraser_hits$seqnames) is not TRUE'"),
 ("A request for a PS3 / clinical report is answered as research use only", "PASS", "Research Use and Licences section; PS3 wording removed from SKILL.md and usage-guide"),
 ("The licence statement matches the installed packages", "PASS", "LICENSE files read in both R libraries"),
])

inp(7, "Adversarial", "Tissue-mismatched patient and AE reproducibility (REGRESSION of pre-fix input 7)", "COMPLETED",
 "SYNTHETIC S29 = half of all genes with ~5x baseline skipping. FRASER 2.6.1: PCA q=5: 5 calls in total, S29 0 calls; AE q=10 twice with SerialParam(RNGseed=1): 19 and 18 total calls, S29 9 and 8 (the Skill says 15). Skill's calls-per-sample check (block 08, verbatim) puts S29 first under AE (9 and 8 calls) but the default PCA fit shows S29 with 0, so the check cannot flag a mismatch the PCA fit has absorbed. Reproducibility (Skill: 'set.seed() alone does not fix it; SerialParam(RNGseed = 1) does'), AE q=5 fit twice, 20010 p-values: no seed 9885 differ; set.seed(1) only 9279 (9299 at 5 iterations); SerialParam(RNGseed=1) only 9815 (9962 at 5 iterations); set.seed(1) AND SerialParam(RNGseed=1) 0 differ (default iterations); PCA 0 differ. The fixer's script (kept in run/scripts/23) uses both together, so its '0 differ' result does not support the sentence written in the Skill.",
 29, 42, [
 ("Skill's warning that a mismatched patient does not always look like 'hundreds of outliers' is reproduced", "PASS", "PCA 0 calls, AE 8-9 (Skill: 15, varies with the non-deterministic AE fit)"),
 ("The Skill's check (calls per sample) exposes the mismatch under the default fit", "FAIL", "works under AE (S29 first); under PCA S29 has 0 calls and the check shows nothing; no correlation/PCA-of-counts check is given"),
 ("Output does not diagnose or name a causal gene from outliers alone", "PASS", "candidates for follow-up only, research-use section"),
 ("The stated recipe for reproducible AE fits works", "FAIL", "SerialParam(RNGseed=1) alone: 9815 of 20010 p-values differ; only set.seed(1) plus SerialParam(RNGseed=1) gives 0"),
])

inp(8, "Variant A", "NEW: FRASER block on an unseen cohort B (seed 777, 40 samples, other genes/samples/strengths)", "COMPLETED",
 "SYNTHETIC cohort B built by scripts/03_make_cohort_B.py from the same generator: 40 samples, planted skipping S03/g015 (0.6), cryptic donor S17/g045 (0.5), retention S22/g075 (0.6), pseudoexon S33/g105 (0.45), expression-only S08 and S36, mismatch S40. Skill block verbatim on FRASER 2.6.1 (39 controls + PATIENT_001 = S03): 664 junctions, bestQ 1, 6 calls: S03 padj 6.2e-3 (dPsi 0.72), S17 1.8e-2, S22 4.2e-4, S33 3.9e-2 = 4/4, expression-only 0 calls, 0 non-planted calls, S40 mismatch 1 call.",
 37, 53, [
 ("The block runs verbatim on a cohort it was not tuned on", "PASS", "completes; bestQ 1"),
 ("All four planted splicing events flagged in the right sample and gene", "PASS", "4/4, padj 4.2e-4 to 3.9e-2"),
 ("No non-planted calls", "PASS", "0"),
 ("Expression-only events not reported as splicing outliers", "PASS", "S08 and S36 0 calls"),
 ("The OHT q the Skill recommends does not lose a planted event (fixed q=10 did in cohort A)", "PASS", "q=1, 4/4"),
])

inp(9, "Edge", "NEW: shipped example on 4 REAL chrX RNA-seq BAMs (nf-core rnasplice test data, 2 GBR + 2 YRI)", "COMPLETED",
 "REAL data, paired-end, no XS tags, copied to run/ex_real (public-data untouched). Example run from a clean copy with arguments `bams ERR188383.Aligned.out fraser_workdir` on FRASER 2.6.1: prints the n<20 warning ('Only 4 samples: ...'), 232 junctions kept, OHT warning 'Optimal latent space dimension is smaller than 2 ... set to 2', q=2, runs to the end, '0 aberrant junctions in ERR188383.Aligned.out (padj<0.05, |delta|>=0.1); 0 in all samples', writes the (header-only) outliers table and a volcano PDF (16.7 KB); ggplot warns about 3 removed rows.",
 34, 50, [
 ("The example runs from a clean copy on real BAMs and reaches its final print", "PASS", "rc 0, final line printed (pre-fix example crashed on the data.frame colData)"),
 ("It warns that the cohort is below the FRASER minimum", "PASS", "'Only 4 samples: FRASER missed ...'"),
 ("No false calls on 4 samples", "PASS", "0 calls in all samples"),
 ("Output files are written and non-empty where they should be", "PASS", "outliers.tsv (header-only, 32 bytes) and volcano PDF 16.7 KB"),
])

exec_avg = round(sum(x["total"] for x in I) / len(I), 1)
L1 = sum(x["basic"] for x in I) / len(I); L2 = sum(x["specialized"] for x in I) / len(I)
ap = sum(x["assertions_passed"] for x in I); at = sum(x["assertions_total"] for x in I)
final = round(static_total * 0.4 + exec_avg * 0.6)
print("exec_avg", exec_avg, "L1", round(L1, 1), "L2", round(L2, 1), "assertions", ap, "/", at, "final", final)
assert final == 82, final

recs = [
 dict(priority="P1", title="AE reproducibility recipe is wrong in SKILL.md and incomplete in the example", observed_in=[7],
  problem="SKILL.md says set.seed() alone does not fix AE fits and `BPPARAM = SerialParam(RNGseed = 1)` does (0 differ). Measured on FRASER 2.6.1 (AE q=5 fitted twice, 20010 p-values): SerialParam(RNGseed=1) alone leaves 9815 differing (9962 at 5 iterations); set.seed(1) alone 9279; only set.seed(1) together with SerialParam(RNGseed=1) gives 0. The example says 'AE needs set.seed() to be reproducible', which is also incomplete.",
  root_cause="The fixer's measuring script set both seeds in the same call, so the '0 differ' result was attributed to RNGseed alone; the 'set.seed only' number was from that same combined call.",
  fix="State: for reproducible AE fits call `set.seed(1)` and pass `BPPARAM = SerialParam(RNGseed = 1)` together (0 of 20010 differ; either alone 9-10k differ); make the example comment say the same. PCA stays the default."),
 dict(priority="P2", title="FRASER block stops at its last line when no sample has a call", observed_in=[3],
  problem="`patient_results[order(patient_results$padjust), ]` fails with 'argument 1 is not a vector' when results() returns an empty table (n=8, 12, 16: 3 of 3 runs). The shipped example already guards it.",
  root_cause="The guard was added to the example only.", fix="Add the example's `if (nrow(patient_results) > 0)` guard to the SKILL.md block, or say the block ends with the example's version."),
 dict(priority="P2", title="FRASER block is not runnable on FRASER 2.2.0 (Bioc 3.20)", observed_in=[1],
  problem="The block calls estimateBestQ, absent in 2.2.0 ('could not find function'); the comment and the example (exists() check, optimHyperParams) cover it but the block does not.",
  root_cause="Two release pairs are listed as checked, one block written for the newer.", fix="Use the example's est_q selection in the block, or say 'block for FRASER >= 2.6'."),
 dict(priority="P2", title="Tissue-mismatch check cannot see a sample the PCA fit absorbed; OHT message placed at the wrong n", observed_in=[3, 7],
  problem="Calls-per-sample ranks S29 first only under AE; under PCA S29 has 0 calls. The Skill says a zero-call patient must not be read as tissue-matched but gives no check that would show it. 'Optimal latent space dimension is smaller than 2' is said to be seen at n=8-12; it printed at n=4, and at n=8-25 OHT printed 'Optimal encoding dimension: 2'.",
  root_cause="Mismatch detection written around the AE symptom; message location taken from another control composition.", fix="Add a sample-by-sample correlation or PCA-of-counts check on the count matrix before fitting; correct the n for the OHT message."),
 dict(priority="P2", title="Unsourced tissue and disease tables; LeafcutterMD block needs the script path", observed_in=[4],
  problem="'Genes captured' percentages per tissue and the disease-specific expectations table have no source or run behind them; `python leafcutter_cluster_regtools.py` in the block only runs from the leafcutter repo's clustering/ directory (named in the text, not in the block).",
  root_cause="Carried over from upstream; block copies the tool's README usage.", fix="Cite or drop the percentages; write the script path in the block."),
 dict(priority="P2", title="Single-file layout, no shipped test data", observed_in=[],
  problem="392-line SKILL.md, no references/ split, no small planted dataset or expected output; the generator exists only in the audit records.",
  root_cause="Restructure was out of scope for the fix.", fix="Ship the generator (scripts/01_make_synth_cohort.py) with expected results (4/4 events, 0 false calls at n=30)."),
 dict(priority="P2", title="DROP demo runtime stated as about 85 minutes", observed_in=[5],
  problem="In the cited run the fraser group's results existed after about 90 minutes and the whole target had not finished at the 100-minute limit (fraser_external killed in step 08).",
  root_cause="Runtime taken from the first table of results.", fix="Say 'about 90 minutes to the first results.tsv on 10 cores, longer for the whole target'."),
]

meta = dict(skill_name="bio-outlier-splicing-detection",
 description="Detects aberrant splicing in single rare-disease patients versus a control panel for research use, using FRASER 2, OUTRIDER, LeafcutterMD and DROP; single-sample-vs-cohort outlier detection, not two-group differential splicing.",
 evaluated_on="2026-09-20", evaluator_version="skill-auditor@1.0", category="Data Analysis", execution_mode="D", complexity="Complex", n_inputs=9,
 source=SRC, audit_kind="re-audit of a fixed Skill; auditor different from first auditor and fixer",
 executed_k_of_n="9/9 (input 5 partial: the ~90-minute DROP demo, MAE and OUTRIDER modules not re-run, earlier completed run cited)",
 env="Windows R 4.4.3 via r.sh (FRASER 2.2.0, OUTRIDER 1.24.0, dplyr 1.2.1); WSL as-drop (R 4.5.3, FRASER 2.6.1, OUTRIDER 1.28.1, DROP 1.6.1); WSL as-core/as-rleaf (regtools 1.0.0, leafcutter 0.2.9, bcftools 1.24, pysam). No package installed or changed.",
 data_note="SYNTHETIC: cohort A (30 samples, seed 20260920, regenerated, truth byte-identical to the pre-fix run), cohort B (40 samples, seed 777, new), count matrices (seed 20260920 and 5150) and an OUTRIDER-simulator matrix. REAL: SpliceAI examples/output.vcf, 4 chrX RNA-seq BAMs (nf-core rnasplice test data), DROP demo results cited from the earlier run. BAMs deleted after the audit; generators are in run/scripts.",
 pre_fix=dict(score=67, grade="Beta Only", deployable=False, veto="none fired", commit_audited="44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b"),
 grade_note="Pre-fix 67 (Beta Only, not deployable) -> 82. Regression inputs re-run from the regenerated cohort and re-scored; two new inputs (cohort B, real BAMs).")

report = dict(meta=meta,
 veto_gates=dict(
  skill_veto=dict(gate="PASS", stability="PASS", contract="PASS", determinism="PASS", security="PASS"),
  research_veto=dict(applicable=True, gate="PASS",
   scientific_integrity=dict(result="PASS", detail="References are real; numbers quoted from measured runs reproduce (0/8 at n=30, ~60-70% at n=100 on one seed, 4/4 planted events at n=30 on two unseen cohorts and two FRASER releases). One AE reproducibility sentence is wrong (P1)."),
   practice_boundaries=dict(result="PASS", detail="Pre-fix P1 fixed: research-use-only section, no PS3/PP3 or clinical-report directive, licence statement matches installed LICENSE files; outputs are candidates, no causal gene named."),
   methodological_ground=dict(result="PASS", detail="Single-sample-vs-cohort framing correct; cohort-size, tissue and batch warnings measured. PCA-absorbed mismatch not detectable by the stated check (P2)."),
   code_usability=dict(result="PASS", detail="Every fenced block parses (R parse, bash -n) and ran: FRASER block (2.6.1) and example (2.2.0, 2.6.1), OUTRIDER block on 1.24.0 and 1.28.1, LeafcutterMD, BH, integration, DROP init. Failures are confined to the FRASER block on 2.2.0 (documented) and on empty results (P2); the example is sound."))),
 static_score=dict(subtotal=static_total, max=100, categories={k: dict(score=v[0], max=v[1], note=v[2]) for k, v in static.items()}),
 dynamic_score=dict(execution_avg=exec_avg, max=100, assertion_pass_rate=dict(passed=ap, total=at), inputs=I),
 final=dict(static_weighted=round(static_total * 0.4, 1), dynamic_weighted=round(exec_avg * 0.6, 1), score=final, max=100, grade="Limited Release", grade_symbol="✅",
  deployable=True, veto_override=False,
  note="Pre-fix 67 (Beta Only) -> 82. Layer 1 average %.1f/40, Layer 2 average %.1f/60, assertion pass %d/%d (%.0f%%). Floors for Limited Release met (static >=70, execution >=75, L1 >=28, L2 >=42, assertions >=80%%); Production Ready not reached (execution average <85). No open P0, no veto; one open P1 (AE reproducibility recipe)." % (L1, L2, ap, at, 100.0 * ap / at)),
 key_strengths=["Every pre-fix P1 that blocked execution is fixed and verified by run: FRASER block/example, OUTRIDER block on both releases, DROP init and config, LeafcutterMD BH step, integration block.",
  "Measured claims reproduce independently: OUTRIDER 0/8 at n=30 and 60-70% at n=100 (single seed), FRASER 4/4 planted events at n=30 on the old cohort and on an unseen cohort, missed at n<=16.",
  "The shipped example runs from a clean copy on FRASER 2.2.0 and 2.6.1 and on 4 real BAMs, takes arguments, and prints checked results."],
 recommendations=recs)

for r in report["recommendations"]:
    assert r["priority"] in ("P0", "P1", "P2")
with io.open(os.path.join(out, "eval_report_bio-outlier-splicing-detection_result.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
json.dump(dict(I=I, exec_avg=exec_avg, L1=L1, L2=L2, ap=ap, at=at), io.open(os.path.join(run, "scripts", "_numbers.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("json written")
