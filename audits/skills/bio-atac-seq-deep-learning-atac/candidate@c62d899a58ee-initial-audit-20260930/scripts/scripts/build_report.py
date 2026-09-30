"""Build report.json, findings.json, finding-ledger.md from the audit content below (English only)."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
CONTRIB = (R / "contribs_outcome.txt").read_text(encoding="utf-8").strip() if (R / "contribs_outcome.txt").exists() else "not completed"

findings = [
 dict(id="DLA-001", priority="P0", severity="critical", state="open", surface="SKILL step 4; references/method-reference.md In Silico Variant Effect Prediction",
  title="log2FC formula understates effects ~5x on log-count head",
  problem="`np.log2(y_alt.sum(-1)/y_ref.sum(-1))` is a ratio of LOG counts, not a count fold change. On a bpnet-lite model (planted-motif fixture, real hg38 backgrounds, 40 motif-breaking SNPs) it gave mean -0.46 versus true log2FC -2.27 (ratio 4.95x, spearman 0.91); with a raw (profile, counts) model output the documented line raises AttributeError. The |log2fc|>1 'strong effect' rule applied to this quantity would call every planted large effect weak.",
  evidence="evidence_log2fc.json; scripts/audit_log2fc_formula.py; run_log2fc.log", fix="State the head semantics (chromBPNet outputs profile logits + log counts). Compute (y_alt - y_ref)/ln2 on the log-count head (or log2 of exp-counts), or use variant-scorer's logfc; wrap tuple outputs with CountWrapper; add a numeric regression using a planted motif."),
 dict(id="DLA-002", priority="P0", severity="critical", state="open", surface="scripts/chrombpnet_pipeline.sh; SKILL step 2",
  title="Shipped pipeline not runnable as documented (no nonpeaks step)",
  problem="The script consumes NONPEAKS (default nonpeaks.bed) but nothing generates it; neither SKILL.md nor the script mentions `chrombpnet prep nonpeaks`. Run as shipped (only contig names adapted) it dies 34 s in with FileNotFoundError at bias-pipeline hyperparameter search and leaves empty out/model. `prep nonpeaks` also refuses to run if `<prefix>_auxiliary/` exists. Adapted with a generated negatives file, the bias and accessibility models train, but neither `bias pipeline` nor `pipeline` process exited within the caps because the post-training DeepSHAP interpret stage did not finish on CPU (see DLA-011). Research-veto M4.",
  evidence="run_script_missing_nonpeaks.log; runs/nonpeaks; evidence/skillscript_run.log; evidence/chrombpnet_step3.log", fix="Add a `chrombpnet prep nonpeaks -g -c -p -fl -o` step before step 2 (documented output `<prefix>_negatives.bed`), wire it to NONPEAKS, check inputs exist up front, and document the stage runtimes."),
 dict(id="DLA-003", priority="P1", severity="high", state="open", surface="SKILL step 4; method-reference; script step 4",
  title="variants.tsv format and pybedtools prerequisite wrong",
  problem="Documented `chrom, pos, ref, alt` (4 columns) fails in variant-scorer: `ValueError: File has 4 columns but chrombpnet schema expects 5 columns`. It needs 5 headerless columns (chr, pos, allele1, allele2, variant_id) and imports pybedtools (pip build fails; conda works). Output columns are `logfc`/`abs_logfc`, not 'log2FC magnitudes'. 5-column runs verified: logfc equals log2(allele2/allele1) to 1e-7 against counts on both the real ENCODE GM12878 model (200 real NA12878 SNPs) and the trained model.",
  evidence="evidence/smoke_variant_scorer.log; evidence/variant_on_trained.log; evidence/encode_model_variant_scores.tsv", fix="Document the 5-column schema with an example row, name the output columns, and list pybedtools (conda) as a prerequisite."),
 dict(id="DLA-004", priority="P1", severity="high", state="open", surface="SKILL step 4; tool-decision-tree; failure-modes",
  title="tangermeme route for chromBPNet models has no loader",
  problem="The SKILL/decision tree route variants through 'tangermeme on pre-trained chromBPNet' but `load_chrombpnet_model` is pseudocode and `tangermeme.io.adapter` does not exist (tangermeme 1.5.0 io exposes read_meme/read_vcf/extract_loci etc.). ENCODE and chrombpnet-trained models are Keras 2.8 .h5 (TF 2.8, CPU); tangermeme is PyTorch. Only bpnet-lite models or variant-scorer are executable.",
  evidence="scripts/probe_surfaces.sh; probe_surfaces.log; evidence/smoke_torch.log", fix="Route chromBPNet/ENCODE .h5 variant scoring to variant-scorer; keep tangermeme for torch models (bpnet-lite, bpnetlite.chrombpnet) with a working loader example; remove the 100x-speed claim or cite it."),
 dict(id="DLA-005", priority="P1", severity="high", state="open", surface="SKILL step 5; method-reference DeepLIFT + TF-MoDISco",
  title="chromBPNet-to-modisco route documented incorrectly",
  problem="The reference says `chrombpnet contribs_bw` writes hypothetical contributions to be converted 'via shap_to_modisco'; no such tool exists in chrombpnet 1.0.1. contribs_bw actually writes bigWigs plus an h5 (shap/projected_shap/raw) that `modisco motifs -i` reads directly. modisco input must be (N,4,L) npz of one-hot plus hypothetical attributions ((N,L,4) gives `Window (500) cannot be longer than the sequences`), `modisco report -m` needs `tomtom` on PATH (MEME suite) or `-l`. modisco motifs/report worked on bpnet-lite attributions (planted TGACTCA recovered, 91 seqlets, JASPAR2024 hits q=0.0026, CWM PNG clean); the working chromBPNet route is undocumented. Bounded contribs_bw check: " + CONTRIB,
  evidence="evidence/smoke_torch.log; evidence/modisco_consensus.txt; evidence/modisco_cwm_fwd.png; run_contribs_bw.log; probe_surfaces.log", fix="Document the actual chromBPNet route (interpret output or a working DeepSHAP-to-npz conversion), the (N,4,L) layout, the tomtom/MEME prerequisite and expected CPU runtime, and add an executed example."),
 dict(id="DLA-006", priority="P1", severity="high", state="open", surface="SKILL Version Compatibility; tool-decision-tree",
  title="Version claims (TF 2.13+) unsatisfiable for chromBPNet/scBasset",
  problem="chrombpnet 1.0.1 pins tensorflow 2.8.0/keras 2.8/numpy 1.23/python 3.8 (CPU only; libcudart 11 missing, sm_120 unsupported); scBasset training fails on Keras 3 (`ModelCheckpoint filepath must end in .weights.h5`) and needs TF<=2.15; modisco-lite is the PyPI name (chromBPNet env carries 2.0.7, Skill asks 2.2+). One 'tensorflow 2.13+' environment cannot satisfy the Skill.",
  evidence="TOOLS.md version table; evidence/smoke_scbasset.log; evidence/gpu_probe.log", fix="Document separate environments per tool (chromBPNet TF 2.8/py3.8 CPU; torch stack for bpnet-lite/tangermeme/modisco; scBasset TF<=2.15), correct the pins and the 'GPU required' claim for chromBPNet."),
 dict(id="DLA-007", priority="P1", severity="high", state="open", surface="SKILL step 3/6; tool-decision-tree; pred_bw echo",
  title="pred_bw regions need 10-column narrowPeak",
  problem="`chrombpnet pred_bw -r regions.bed` with a natural 3-column BED fails `ValueError: cannot convert float NaN to integer`; a 10-column narrowPeak (summit column) works and produced pred_bias.bw / pred_chrombpnet_nobias.bw (bias track sum 421.5 vs corrected 17,923.6 in regions, 60,959 non-zero bins). Same contract applies to contribs_bw.",
  evidence="evidence/pred_bw.log", fix="State the 10-column requirement and give a one-line way to derive it from peaks.narrowPeak."),
 dict(id="DLA-008", priority="P1", severity="high", state="open", surface="SKILL step 4; script echo; method-reference",
  title="Uncalibrated |log2FC|>1 threshold; tool null ignored",
  problem="The Skill declares |log2fc|>1 'strong effect' with no calibration. variant-scorer emits jsd and empirical p-values against a shuffled-sequence null (18 columns incl. logfc.pval, jsd.pval); only 2/200 real SNPs on the ENCODE GM12878 model exceeded |logfc|>1. No guidance on using the null, on effect-size versus significance, or on model quality gates.",
  evidence="evidence/encode_model_variant_scores.tsv; evidence/smoke_variant_scorer.log", fix="Recommend the shuffled-null p-values and jsd, describe how to pick thresholds, and label |log2FC|>1 as a heuristic."),
 dict(id="DLA-009", priority="P1", severity="high", state="open", surface="SKILL step 2; script; failure-modes",
  title="No model QC acceptance criteria after training",
  problem="No step checks bias-model or corrected-model quality. The run wrote bias_metrics.json, chrombpnet_metrics.json (test-peak counts pearson 0.474/spearman 0.461, median normalized JSD 0.18 for the 2-epoch bounded model), footprint PNGs and a max-bias-response file, and chromBPNet has a `qc` subcommand, but the Skill gives no thresholds, does not say the bias model must not learn TF motifs, and closes with a TOBIAS-based CTCF check unrelated to chromBPNet's own QC.",
  evidence="evidence/chrombpnet_step3_metrics.json; evidence/chrombpnet_bias_metrics.json; evidence/chrombpnet_help.log", fix="Add a QC gate (bias/corrected metrics, footprint and max bias response, `chrombpnet qc`) with pass/fail guidance before variant or motif use."),
 dict(id="DLA-010", priority="P1", severity="medium", state="open", surface="SKILL Enformer/Borzoi/scBasset guidance; tool-decision-tree; failure-modes",
  title="Enformer/Borzoi/scBasset advice unsupported or contradictory",
  problem="'Kipoi for Enformer' is false (kipoi ls shows no Enformer; Enformer works via enformer-pytorch/HF: real 196,608 bp hg38 -> (1,896,5313) finite). Borzoi is named with no install or command (not installed here). scBasset advice is self-contradictory: 'aggregate cells to clusters and train scBasset' versus 'per-cell projection layer'; scBasset learns a per-cell embedding and only ran on TF 2.15 CPU (3 epochs, 26,041 peaks x 4,609 PBMC cells, 609 s/epoch), preprocess crashes with fewer than ~20k peaks. No commands are shipped for any of these routes.",
  evidence="evidence/kipoi_probe.log; evidence/smoke_scbasset.log; evidence/smoke_torch.log", fix="Give a working Enformer command (enformer-pytorch) with input-length and track guidance, drop or qualify Borzoi, and rewrite the scBasset guidance around per-cell input with prerequisites and versions."),
 dict(id="DLA-011", priority="P2", severity="medium", state="open", surface="Skill compute claims; script header",
  title="CPU stage runtime undocumented; DeepSHAP stage never exited",
  problem="`chrombpnet bias pipeline` (two runs, 61-76 min) and `chrombpnet pipeline` (step 3, capped at 3,600 s, log ends 'Generating profile shap scores / Done 0 examples of 2165' at 60m01s) did not exit in the post-training DeepSHAP interpret stage on CPU under load; the interpret directories hold only args and a BED, no score file. Models, metrics and footprints were written first. The earlier TOOLS.md note that step 3 exited 0 is not supported by this log. Full-scale training and interpretation (A100/24 h) remain resource-infeasible here.",
  evidence="evidence/chrombpnet_step3.log; evidence/bias_step2_rerun.log; scripts (audit-envs) run_chrombpnet_step3.sh", fix="Document that interpretation is the slow tail, how to reduce/skip it, and per-stage runtimes; keep the 'exit not observed' limitation until rerun on suitable hardware."),
 dict(id="DLA-012", priority="P2", severity="low", state="open", surface="references/failure-modes.md",
  title="Stale or non-existent flags and terms",
  problem="`--num-filters` is `-fil/--filters`; `target_seqlet_fdr` and 'flank_size' are TF-MoDISco v1 terms not exposed by modisco-lite 2.x (`-f` seqlet flank; no FDR flag); 'DeepLIFT (RevealCancel rule)' conflicts with the stated rescale default; 'bias trained on naked-DNA control' conflicts with the pipeline, which trains the bias model on non-peak regions of the same data; 'verbose' re-run has no such flag.",
  evidence="evidence/chrombpnet_help.log; evidence/torch_help.log", fix="Replace each with the installed CLI's names and reconcile the bias-model statements."),
 dict(id="DLA-013", priority="P2", severity="low", state="open", surface="scripts/chrombpnet_pipeline.sh",
  title="Script hygiene: unquoted paths, placeholder scorer path",
  problem="Variables are unquoted (paths with spaces break); VARIANT_SCORER defaults to `/path/to/variant-scorer` with no existence check, so a placeholder failure would surface only after the long training; `-tcr/-vcr` are test/valid but the header says train/val/test order; step 4 says the `variants.tsv` contains ref/alt in four columns (see DLA-003).",
  evidence="scripts/chrombpnet_pipeline.sh; evidence/skillscript_run.log", fix="Quote variables, fail fast on missing inputs and scorer path, and fix the comment."),
 dict(id="DLA-014", priority="P3", severity="info", state="open", surface="method-reference; failure-modes",
  title="Unsupported comparative claims and thresholds",
  problem="'Strongest bias correction of the compared tools', '100x speedup', '<50M reads / <30k peaks' and the compute figures are uncited; bounded runs cannot confirm them.",
  evidence="static", fix="Cite or soften."),
]

def mk(idx, typ, label, status, note, basic, spec, asserts):
    p = sum(a[1] for a in asserts)
    return dict(index=idx, type=typ, label=label, status=status,
      status_flag=("✅" if basic + spec >= 75 else "⚠️") if status == "COMPLETED" else "❌", note=note,
      basic=basic, specialized=spec, total=basic + spec, assertions_passed=p, assertions_total=len(asserts),
      assertions=[dict(text=t, result="PASS" if ok else "FAIL", note=n) for t, ok, n in asserts])

inputs = [
 mk(1, "Canonical", "Shipped chromBPNet script on real-derived GM12878 fixture", "PARTIAL",
    "As shipped it fails 34 s in (no nonpeaks file); with a generated negatives file the models and metrics are produced but neither long stage exited within the CPU caps",
    20, 30, [
    ("Script runs as shipped with only path/contig substitution", False, "FileNotFoundError nonpeaks.bed; empty out/model"),
    ("Splits JSON matches documented chromosome assignment", True, "test chr1/3/6, valid chr8/20, 450 train contigs"),
    ("Bias and accessibility models trained with scientifically sane metrics", True, "bias.h5; nobias test-peak counts pearson 0.474, spearman 0.461 (2-epoch, 2,166 peaks)"),
    ("Both pipeline processes exit cleanly", False, "bias pipeline 61-76 min and pipeline 60 min capped in DeepSHAP interpret stage"),
    ("Documented outputs (bias.h5, chrombpnet_nobias.h5) exist", True, "present; footprint PNGs and bias response 0.001 inspected")]),
 mk(2, "Variant A", "Variant effect scoring: ENCODE GM12878 model + tangermeme formula", "PARTIAL",
    "variant-scorer works only with a 5-column list; documented tangermeme formula gives ~5x-understated effects and has no chromBPNet loader",
    25, 33, [
    ("Documented 4-column variants.tsv is accepted", False, "ValueError expects 5 columns"),
    ("5-column run gives finite logfc equal to log2(allele2/allele1)", True, "max deviation 1.1e-7; 200 real NA12878 SNPs; 2/200 abs logfc >1"),
    ("Pretrained ENCODE model separates real peaks from non-peaks", True, "mean logcounts 5.94 vs 3.30, AUC 0.970"),
    ("Documented tangermeme log2fc line returns the true count log2FC", False, "mean -0.46 vs true -2.27 on planted-motif fixture"),
    ("Documented chromBPNet-to-tangermeme route is executable", False, "load_chrombpnet_model is pseudocode; no adapter")]),
 mk(3, "Edge", "Bias-corrected prediction bigWigs with pred_bw", "COMPLETED",
    "Works only with 10-column narrowPeak regions; the natural 3-column BED fails with an unclear error",
    28, 38, [
    ("3-column regions.bed accepted", False, "ValueError cannot convert float NaN to integer"),
    ("10-column narrowPeak run writes both bigWigs", True, "pred_bias.bw and pred_chrombpnet_nobias.bw parsed with pyBigWig"),
    ("Bias track differs from corrected track as expected", True, "sum 421.5 vs 17,923.6; 60,959 non-zero bins")]),
 mk(4, "Variant B", "DeepLIFT + TF-MoDISco motif discovery", "COMPLETED",
    "modisco CLI recovers the planted motif from bpnet-lite attributions; chromBPNet contribs_bw h5 feeds `modisco motifs -i` but the documented shap_to_modisco conversion does not exist",
    26, 36, [
    ("modisco motifs (documented flags) runs and recovers planted TGACTCA", True, "pattern_0 consensus contains TGACTCA, 91 seqlets"),
    ("modisco report annotates against JASPAR2024", True, "MA0462.3/MA0835.3/MA1634.2 TGACTCA q=0.0026 with tomtom present; fails without tomtom"),
    ("Attributions concentrate on the planted motif; captum completeness holds", True, "0.235 vs 0.0005; delta 6e-8"),
    ("Documented contribs_bw then shap_to_modisco conversion is executable as written", False, "shap_to_modisco absent; undocumented h5 route ran (20 regions, exit 0)"),
    ("Documented npz layout works as-is", False, "(N,L,4) fails; (N,4,L) required")]),
 mk(5, "Stress", "Other advertised models: scBasset, Enformer, Kipoi, Borzoi", "PARTIAL",
    "scBasset ran only on TF 2.15 CPU (3 epochs); Enformer works via enformer-pytorch not Kipoi; Borzoi not run",
    18, 26, [
    ("scBasset preprocess/train/reload on real 10x PBMC on the documented tensorflow 2.13+", False, "Keras 3 ModelCheckpoint error; only TF 2.15 Keras 2 CPU env ran"),
    ("scBasset per-cell projection kernel finite after training", True, "(32,4609) finite, val_auc 0.53 after 3 epochs"),
    ("Enformer available through Kipoi as documented", False, "no Enformer in Kipoi listing"),
    ("Enformer forward on real hg38 gives valid tracks", True, "(1,896,5313) finite, non-negative, mean 1.352"),
    ("Borzoi route executed", False, "not installed; blocked/resource item")]),
]

cats = {
 "functional_suitability": (7, 12, "Core chromBPNet and modisco pieces work, but variant, motif and scBasset/Enformer/Borzoi routes are missing steps or wrong as written."),
 "reliability": (6, 12, "No input checks; missing nonpeaks and column-format failures surface as raw stack traces and the slow interpret stage is unmentioned."),
 "performance_context": (7, 8, "SKILL.md 88 lines with three focused references; compute figures uncited."),
 "agent_usability": (9, 16, "Tool-selection guidance is clear but several documented commands cannot be followed cold; inconsistent scBasset and bias-model statements."),
 "human_usability": (5, 8, "Good triggers and a when-not-to-use list; rigid undocumented input formats."),
 "security": (10, 12, "No secrets or destructive commands; unquoted variables and placeholder path unvalidated."),
 "maintainability": (8, 12, "Clean routing; only one runnable script and no tests or examples."),
 "agent_specific": (15, 20, "Strong progressive disclosure and routing; re-run of prep nonpeaks fails on existing outputs; escape hatches only partly stated."),
}
sub = sum(v[0] for v in cats.values())
ex = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * .4, 1), round(ex * .6, 1)
recs = []
for pr, ids in (("P0", ["DLA-001", "DLA-002"]), ("P1", ["DLA-003", "DLA-004", "DLA-005", "DLA-006", "DLA-007", "DLA-008", "DLA-009", "DLA-010"]), ("P2", ["DLA-011", "DLA-012", "DLA-013", "DLA-014"])):
    for i in ids:
        f = next(x for x in findings if x["id"] == i)
        obs = {"DLA-001": [2], "DLA-002": [1], "DLA-003": [2], "DLA-004": [2], "DLA-005": [4], "DLA-006": [5], "DLA-007": [3], "DLA-008": [2], "DLA-009": [1], "DLA-010": [5], "DLA-011": [1]}.get(i, [])
        recs.append(dict(priority=pr, title=(f["id"] + " " + f["title"])[:60], observed_in=obs, problem=f["problem"].split(". ")[0][:300] + ".",
                         root_cause="Reference examples were written from tool documentation without executing them against installed versions.", fix=f["fix"]))
report = dict(
 meta=dict(skill_name="bio-atac-seq-deep-learning-atac",
  description="Sequence-based deep learning for ATAC-seq using chromBPNet, BPNet, scBasset, or Enformer: Tn5 bias correction, per-base accessibility profiles, in silico variant effects, and DeepLIFT/TF-MoDISco motif discovery.",
  evaluated_on="2026-09-30", evaluator_version="skill-auditor@1.0", category="Data Analysis", execution_mode="D", complexity="Moderate", n_inputs=5),
 veto_gates=dict(
  skill_veto=dict(gate="PASS", stability="PASS", contract="PASS", determinism="PASS", security="PASS"),
  research_veto=dict(applicable=True, gate="FAIL",
   scientific_integrity=dict(result="PASS", detail="No fabricated citations or results; uncited speed/compute claims are scored under maintainability."),
   practice_boundaries=dict(result="PASS", detail="Research analysis scope; no diagnostic or therapeutic conclusions."),
   methodological_ground=dict(result="FAIL", detail="Input 2: documented log2FC on the log-count head understates effects about 5x (mean -0.46 vs true -2.27), so the |log2fc|>1 rule would call strong effects weak (DLA-001)."),
   code_usability=dict(result="FAIL", detail="Input 1: shipped pipeline script fails at once because the required nonpeaks file is never generated; documented variants.tsv and pred_bw region formats also fail (DLA-002, DLA-003, DLA-007)."))),
 static_score=dict(subtotal=sub, max=100, categories={k: dict(score=v[0], max=v[1], note=v[2]) for k, v in cats.items()}),
 dynamic_score=dict(execution_avg=ex, max=100, assertion_pass_rate=dict(passed=sum(i["assertions_passed"] for i in inputs), total=sum(i["assertions_total"] for i in inputs)), inputs=inputs),
 final=dict(static_weighted=sw, dynamic_weighted=dw, score=round(sw + dw), max=100, grade="Reject", grade_symbol="❌", deployable=False, veto_override=True),
 key_strengths=[
  "Clear tool-selection guidance and when-not-to-use boundaries that keep classical ATAC steps out of scope.",
  "Correct current-CLI details in places (chrombpnet prep splits flags, snp_score removed, variant-scorer companion repo).",
  "Concise SKILL.md with routed references and a shipped end-to-end script skeleton.",
  "Core tooling verified live: pretrained ENCODE model separates real peaks (AUC 0.970); variant-scorer logfc exact; modisco recovers a planted motif."],
 recommendations=recs)
(R / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
(R / "findings.json").write_text(json.dumps(dict(candidate_content_sha256="c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943", findings=findings), indent=2, ensure_ascii=False), encoding="utf-8")
rows = ["# Ordered finding ledger", "", "Audit identity: candidate content SHA-256 `c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943` (6 files).", "",
        "| Order | ID | Priority | State | Surface | Required disposition |", "|---:|---|---|---|---|---|"]
for n, f in enumerate(findings, 1):
    rows.append(f"| {n} | {f['id']} | {f['priority']} | {f['state']} | {f['surface']} | {f['title']}: {f['fix']} |")
(R / "finding-ledger.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
print(sub, ex, report["final"])
