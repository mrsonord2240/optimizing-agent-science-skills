"""Build report.json and source-identity.json for the final re-audit (run once, after all executed evidence exists)."""
import hashlib
import json
import os
from pathlib import Path

RUN = Path(__file__).resolve().parent.parent
SK = Path(r"F:\OpenScience\wt\atac-deep-learning-atac\skills\bio-atac-seq-deep-learning-atac")
EXPECTED = "3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87"

files = []
for r, _, fs in os.walk(SK):
    for f in fs:
        p = Path(r) / f
        b = p.read_bytes()
        files.append({"path": p.relative_to(SK).as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
files.sort(key=lambda x: x["path"])
manifest = "\n".join("%s\t%d\t%s" % (x["path"], x["bytes"], x["sha256"]) for x in files)
ident = hashlib.sha256(manifest.encode()).hexdigest()
assert ident == EXPECTED, ident
assert not [x for x in files if "__pycache__" in x["path"]]

OK, NO = "\u2705", "\u26a0\ufe0f"


def mk(idx, typ, label, status, note, basic, spec, asserts):
    p = sum(1 for a in asserts if a[1])
    flag = (OK if basic + spec >= 75 else NO) if status == "COMPLETED" else "\u274c"
    return dict(index=idx, type=typ, label=label, status=status, status_flag=flag, note=note,
                basic=basic, specialized=spec, total=basic + spec, assertions_passed=p, assertions_total=len(asserts),
                assertions=[dict(text=t, result="PASS" if ok else "FAIL", note=n) for t, ok, n in asserts])


inputs = [
    mk(1, "Canonical", "Shipped chromBPNet pipeline, fresh OUTDIR, then RESUME tail and guards", "COMPLETED",
       "Fresh end-to-end run (prep splits, prep nonpeaks, bias train, train, pred_bw, footprints, QC gate, variant scoring) exited 0 in about 43 min on the real-derived GM12878 fixture at 1 epoch (2700 s cap not reached); the 1-epoch model correctly fails the QC gate",
       36, 52, [
           ("Seven fail-fast guards (missing BAM, 3-col peaks, 4-col variants, placeholder scorer, stale nonpeaks, no chrombpnet, trained OUTDIR) exit 1 in seconds before training", True, "ra_guards_gate.sh: 7 of 7 exit 1 with the documented message"),
           ("Fresh run creates nonpeaks_negatives.bed, bias.h5, chrombpnet.h5, chrombpnet_nobias.h5, pred_bw metrics and footprints and exits 0", True, "pipe_run1.log exit=0; all artifacts present"),
           ("QC gate reports the unconverged 1-epoch model as FAIL instead of passing it", True, "bias 0.494 PASS, corrected pearsonr -0.496 FAIL, Tn5 response corrected_0.001 PASS; ALLOW_FAILED_QC continued as documented"),
           ("Variant table has 18 columns, finite logfc equal to log2(allele2/allele1), null p-values present", True, "30 rows, max deviation 7e-8, abs_logfc.pval 0.05-0.99"),
           ("RESUME=1 on the finished OUTDIR skips every training step and re-runs gate plus variant scoring", True, "22 s wall, exit 0, variant table regenerated")]),
    mk(2, "Variant A", "Variant-effect log2FC correctness (P0) with three independent methods", "COMPLETED",
       "Raw Keras recomputation, shipped score_variants_torch.py and variant-scorer forward-only agree on 200 real NA12878 SNPs; the planted-truth fixture confirms the old formula is 5.5x too small",
       38, 55, [
           ("Formula (alt - ref)/ln2 on the log-count head equals log2(exp(alt)/exp(ref)) computed independently in raw Keras", True, "max diff 2.7e-7 on 200 SNPs"),
           ("score_variants_torch.py agrees with the independent Keras values", True, "corr 0.9999997, max abs diff 1.1e-3"),
           ("Keras values agree with variant-scorer --forward_only logfc and its allele counts", True, "corr 1.0, max diff 2.6e-7"),
           ("Planted-motif fixture: fixed formula near planted truth -2.44, old formula about 5x too small", True, "fixed -2.20 (within 20 percent), old -0.446, ratio 5.47"),
           ("Documented calling numbers reproduce (2 of 200 exceed abs logfc 1 in default mode; Pearson 0.96 forward-only versus default)", True, "2/200 and r 0.960 from the scorer default output; 3/200 forward-only")]),
    mk(3, "Edge", "pred_bw regions contract and Enformer reference guard", "COMPLETED",
       "A 3-column BED with duplicate rows fails as documented; the documented sort/awk one-liner yields a working 10-column file and three bigWigs; Enformer skips a wrong-REF row",
       36, 52, [
           ("Raw 3-column BED with duplicates fails with the documented NaN error", True, "ValueError: cannot convert float NaN to integer"),
           ("Documented one-liner produces 17 sorted unique 10-column rows and pred_bw succeeds", True, "ok_bias.bw, ok_chrombpnet.bw, ok_chrombpnet_nobias.bw written"),
           ("bigWigs hold signal in the requested regions and bias differs from corrected", True, "9,858 non-zero bins each; sums bias 73.0, nobias 489.3, corrected 576.7"),
           ("enformer_variant_effect.py skips a variant whose REF does not match the genome", True, "scored 1 of 2")]),
    mk(4, "Variant B", "Attributions, TF-MoDISco and report (lite and tomtom) on the real ENCODE GM12878 model", "COMPLETED",
       "attributions_to_modisco_npz.py output feeds modisco motifs and both report modes; 10 patterns map to expected regulators. The chrombpnet contribs_bw route was not re-run by this auditor (reused from the delta and fix runs)",
       36, 52, [
           ("ohe.npz and attr.npz have shape (400,4,1000), finite, one-hot valid", True, "nonzero fraction 0.99999; centre attribution 3.7x flank"),
           ("modisco motifs finds patterns from 400 real peaks", True, "10 positive patterns, 119 down to 21 seqlets"),
           ("modisco report -t and -l annotate patterns with expected GM12878 regulators", True, "CTCF (q 1e-14), ELK4/ETS, NFY, IRF/STAT, NRF1, REL/RELA, SP/KLF"),
           ("Report without tomtom on PATH fails as documented and -l is the alternative", True, "tomtom executable could not be called; -l ran")]),
    mk(5, "Stress", "scBasset documented commands, Enformer tracks, restricted-item honesty, external prerequisites", "COMPLETED",
       "scBasset preprocess, 1-epoch train and embedding run on real 10x PBMC; Enformer matches an independent bin computation; the Skill labels full-scale training, scBasset on Keras 3 and Borzoi as not run; bedtools and bedGraphToBigWig prerequisites are not declared",
       34, 50, [
           ("scBasset preprocess, 1-epoch train and embedding on TF 2.15 CPU", True, "184 steps in 760 s, best_model.h5, embedding (32,4609) finite"),
           ("Enformer 40 SNPs, 2 tracks: finite and equal to an independent recomputation at the variant bin", True, "ranges -0.42..0.19; 0.006142679 both ways"),
           ("Skill never claims full-scale chromBPNet training, Borzoi or scBasset on Keras 3 as executed", True, "each is labelled untested or failing in SKILL.md and method-reference"),
           ("Skill states scBasset short runs are mechanics only", True, "3-epoch val AUC 0.53 stated; 1-epoch val AUC 0.49 observed"),
           ("External binaries chromBPNet shells out to (bedtools, bedGraphToBigWig) are declared or checked up front", False, "absent from the env table and step 0 (DLA-015); confirmed in chrombpnet source, not by a failing run")]),
]

MAXES = {"functional_suitability": 12, "reliability": 12, "performance_context": 8, "agent_usability": 16,
         "human_usability": 8, "security": 12, "maintainability": 12, "agent_specific": 20}
cats = {
    "functional_suitability": (11, "Every documented route now runs; both P0 defects are repaired and reproduced independently."),
    "reliability": (10, "Fail-fast guards, RESUME and an honest QC gate; bedtools and bedGraphToBigWig are not checked up front (DLA-015)."),
    "performance_context": (7, "SKILL.md stays compact with three focused references; runtimes are recorded with their fixture."),
    "agent_usability": (14, "Clear routing and copyable commands; three environments must be juggled and one stale step pointer remains (DLA-016)."),
    "human_usability": (7, "Good triggers and boundaries; long reference tables."),
    "security": (11, "No secrets or destructive actions; paths are quoted and the scorer path is validated."),
    "maintainability": (10, "Pinned versions and shipped scripts; no shipped regression fixture for the log2FC rule."),
    "agent_specific": (17, "Progressive disclosure, explicit gates and labelled limitations; restricted items stay unclaimed."),
}
sub = sum(v[0] for v in cats.values())
ex = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * .4, 1), round(ex * .6, 1)
score = round(sw + dw)
P = sum(i["assertions_passed"] for i in inputs)
T = sum(i["assertions_total"] for i in inputs)

recs = [
    dict(priority="P2", title="DLA-015 bedtools and bedGraphToBigWig undeclared", observed_in=[5],
         problem="chromBPNet 1.0.1 shells out to bedtools (prep nonpeaks) and bedGraphToBigWig (reads_to_bigwig in bias train and train), but the SKILL env table and the script's step 0 check only chrombpnet.",
         root_cause="The env table listed Python packages only; the external binaries were present in the audit environment.",
         fix="Add bedtools and UCSC bedGraphToBigWig (conda: bedtools, ucsc-bedgraphtobigwig) to the chrombpnet row of the env table and to the step 0 command -v checks."),
    dict(priority="P2", title="DLA-016 pipeline header points to the wrong SKILL step", observed_in=[],
         problem="scripts/chrombpnet_pipeline.sh line 3 says to run interpretation separately per SKILL.md step 5, but step 5 is variant effects; motif interpretation is step 6.",
         root_cause="Step numbers shifted when the workflow was rewritten.",
         fix="Change the header comment to SKILL.md step 6."),
]
report = dict(
    meta=dict(skill_name="bio-atac-seq-deep-learning-atac",
              description="Sequence-based deep learning for ATAC-seq using chromBPNet, BPNet, scBasset, or Enformer: Tn5 bias correction, per-base accessibility profiles, in silico variant effects, and DeepLIFT/TF-MoDISco motif discovery.",
              evaluated_on="2026-09-30", evaluator_version="skill-auditor@1.0", category="Data Analysis", execution_mode="D", complexity="Moderate", n_inputs=5),
    veto_gates=dict(
        skill_veto=dict(gate="PASS", stability="PASS", contract="PASS", determinism="PASS", security="PASS"),
        research_veto=dict(applicable=True, gate="PASS",
                           scientific_integrity=dict(result="PASS", detail="Uncited rules of thumb are labelled; measured numbers in the text match the re-run evidence; limits are stated."),
                           practice_boundaries=dict(result="PASS", detail="Research analysis scope; no clinical claims."),
                           methodological_ground=dict(result="PASS", detail="The log2FC on the log-count head was reproduced by three independent methods (Keras, PyTorch, variant-scorer) and a planted-truth fixture."),
                           code_usability=dict(result="PASS", detail="The shipped pipeline ran end to end from a fresh directory, RESUME works, and the four new scripts ran on real public inputs."))),
    static_score=dict(subtotal=sub, max=100, categories={k: dict(score=v[0], max=MAXES[k], note=v[1]) for k, v in cats.items()}),
    dynamic_score=dict(execution_avg=ex, max=100, assertion_pass_rate=dict(passed=P, total=T), inputs=inputs),
    final=dict(static_weighted=sw, dynamic_weighted=dw, score=score, max=100, grade="Production Ready", grade_symbol=OK, deployable=True, veto_override=False),
    key_strengths=[
        "The variant-effect formula is now correct and backed by a planted-truth regression plus three independent numerical agreements.",
        "The shipped pipeline runs from a fresh directory, resumes cheaply, fails fast on bad inputs and gates on chromBPNet's own QC thresholds.",
        "Every route (variant-scorer, PyTorch, MoDISco, Enformer, scBasset) has an executed command, and untested items are labelled as such.",
        "Data formats and CLI errors that broke the original Skill are documented with exact messages."],
    recommendations=recs)
assert score >= 85
(RUN / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

tools = hashlib.sha256(Path(r"F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\TOOLS.md").read_bytes()).hexdigest()
zipsha = hashlib.sha256(Path(r"F:\optimizing-agent-science-skills\skill-auditor.zip").read_bytes()).hexdigest()
si = {"phase": "final re-audit", "independent_auditor": True,
      "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/deep-learning-atac"},
      "candidate": {"branch": "fix/atac-deep-learning-atac", "commit": "3186916", "path": str(SK),
                    "status_before": "untracked subtree only", "status_after_execution": "untracked subtree only (bytes unchanged, verified)",
                    "content_sha256": ident,
                    "content_manifest": {"file_count": len(files), "byte_total": sum(x["bytes"] for x in files),
                                         "scheme": "sha256-manifest-v1 (sorted path, bytes, sha256 lines joined by LF)"},
                    "files": files},
      "prior_audit_identity": "c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943",
      "tooling": {"tools_md_sha256": tools, "environment_fingerprint_sha256": "06fc27986ce7b28c4e102689c57fa41596fc3d2716402daaa8309f93bf9cfa29", "rubric_zip_sha256": zipsha}}
(RUN / "source-identity.json").write_text(json.dumps(si, indent=2), encoding="utf-8")
print(sub, ex, sw, dw, score, P, T, ident)
