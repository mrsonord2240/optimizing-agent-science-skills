"""Builds eval_report_bio-isoform-switching_result.json (schema: skill-auditor/references/report_json_schema.md) and the viewer .md.
All numbers below are copied from the logs in run/*.log (10_input1.log ... 70_input7.log, 35a*.log, 36*.log, 40*.log)."""
import json, io, os
OUT = r"F:\OpenScience\audits\bio-isoform-switching"
SRC = "mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/isoform-switching"

def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="Planted isoform switches, 3 v 3 Salmon quants, IsoformSwitchAnalyzeR workflow as written (SYNTHETIC)",
  status="COMPLETED", status_flag="\u2705", executed=True,
  execution_note="Ran run/10_input1_isar_3v3.R from the SKILL.md code (importIsoformExpression -> importRdata -> preFilter -> isoformSwitchTestSatuRn; plus isoformSwitchTestDEXSeq, the test the Skill's own >5-replicate rule selects). 300 genes x 3 isoforms, 20 planted switches (10 poison-exon, 10 exon-skip), 10 sub-threshold (dIF 0.06), 5 gene-level-only decoys, 5 dIF 0.15. Truth in run/data/synth/truth_genes.tsv. Re-run gave identical output.",
  note="20/20 planted switches recovered by both tests, direction correct 20/20, dIF within 0.1 of truth 20/20; ISAR dIF == hand-computed mean-of-sample-IF dIF (max diff 7.3e-05); DGE-only decoys 0 called; null split (ctrl 1-3 v 4-6) 1 isoform call (DEXSeq) / 0 (satuRn). ISAR warns that satuRn is not advised with few replicates, which contradicts the Skill's own example.",
  basic=32, specialized=47,
  assertions=[
   A("ISAR dIF equals an independent hand computation from quant.sf TPM", True, "max abs diff 7.32e-05 over 871 isoforms (ISAR IF = mean of per-sample fractions)"),
   A("All 20 planted switches recovered with the right isoform direction and dIF within 0.1 of truth", True, "20/20 for satuRn and DEXSeq"),
   A("Gene-level-only (DGE) decoys are not called as DTU", True, "0/5 called; DEXSeq 2 null-gene FP of 260 (0.8%)"),
   A("Null comparison (control v control) stays quiet", True, "DEXSeq 1 isoform call in 300 tested genes, satuRn 0; re-run identical"),
   A("The satuRn call in the workflow agrees with the Skill's own rule (satuRn only when a condition has >5 replicates)", False, "3 v 3 example calls isoformSwitchTestSatuRn; ISAR 2.6.0 warns 'few replicates... use isoformSwitchTestDEXSeq()'"),
  ]),
 dict(index=2, type="Variant A", label="Manual DRIMSeq -> DEXSeq -> stageR DTU pipeline, 6 v 6 (SYNTHETIC)",
  status="COMPLETED", status_flag="\u26a0\ufe0f", executed=True,
  execution_note="Ran run/20_input2_manual_dtu.R. As written the code stops at samples(d) (Biobase::samples masks DRIMSeq::samples once library(DEXSeq) is attached; run/21_samples_mask.R shows this with the Skill's exact library() order). Ran after replacing samples(d) by DRIMSeq::samples(d). tximeta(coldata) replaced by tximport (synthetic data has no Salmon index).",
  note="As-written code fails; patched: gene-level q<0.05 recovers 20/20 planted, 1/260 null-gene FP, stageR names the truly switching transcript (B or C) in 20/20, DRIMSeq dmTest agrees (Jaccard 0.89), null split gives 2 gene calls, dtuScaledTPM and raw counts give the same 20/20.",
  basic=28, specialized=43,
  assertions=[
   A("Pipeline code runs as written from the Skill", False, "'unable to find an inherited method for function samples for signature dmDSdata' (Biobase masks DRIMSeq); fix is DRIMSeq::samples(d)"),
   A("After the one-token fix, all 20 planted switches are called at gene-level q<0.05 with <=5% null-gene FP", True, "20/20; 1/260 null FP; DGE decoys 0"),
   A("stageR confirmation names the transcript that truly switches", True, "B (poison) or C (skip) confirmed in 20/20 planted genes"),
   A("An independent implementation (DRIMSeq dmTest) reaches the same gene set", True, "27 v 26 genes, Jaccard 0.89, both 20/20 planted"),
   A("Null split (control 1-3 v 4-6) stays quiet through stageR", True, "2 gene-level calls in 291 genes"),
  ]),
 dict(index=3, type="Edge", label="Real chrX GBR v YRI 2 v 2 Salmon quants + the shipped example script",
  status="PARTIAL", status_flag="\u274c", executed=True,
  execution_note="Ran run/30_input3_real_chrX.R, 35a_shipped_example_prep.R, 35a3-35a6 (real nf-core rnasplice chrX, GRCh37 Ensembl GTF, 4 samples). The shipped examples/isoform_switch_analysis.R was run from the copy in run/skill/examples.",
  note="Skill's 6-sample hard-coded vector errors loudly on 4 samples; its dmFilter values (min_samps_gene_expr=6) fail on n=4. Adapted runs: DEXSeq 19 / DRIMSeq 12 / ISAR 20 genes (DEXSeq v DRIMSeq overlap 6/12; ISAR v DEXSeq Jaccard 0.77); top switch RPL10 dIF -0.329 v hand -0.336. The Skill's default importIsoformExpression route (scaledTPM counts) gives 0 significant switches (RPL10 q=1) while raw NumReads / lengthScaledTPM give 26 isoforms in 20-22 genes. The shipped example stops at run_switch_analysis ('No genes were considered switching') and prints only a banner when run as shipped.",
  basic=23, specialized=28,
  assertions=[
   A("Skill's hard-coded 6-sample values work on a 2 v 2 study without editing", False, "design vector: loud data.frame error (good); dmFilter(min_samps_gene_expr=6) on 4 samples: 'min_samps_gene_expr <= ncol(x@counts) is not TRUE', no guidance"),
   A("ISAR dIF for the top real switch matches a hand computation from quant.sf", True, "RPL10 ENST00000406022: ISAR -0.3291 v hand -0.3356 (isoforms removed by preFilter change the denominator)"),
   A("Independent implementations agree on the main real signal", True, "DEXSeq 19, DRIMSeq 12, overlap 6; ISAR v manual DEXSeq overlap 17/20"),
   A("The Skill's default count route detects the clearest real switch (RPL10, counts in the thousands)", False, "importIsoformExpression defaults -> 0 significant, RPL10 q=1; calculateCountsFromAbundance=FALSE or tximport raw -> 26 isoforms, RPL10 q=4.6e-18; cause not isolated (35a3-35a6)"),
   A("Shipped example runs end to end on real data", False, "banner only as shipped; functions: run_switch_analysis stops (0 switches); extract_sequences fails without CDS lines and without an existing output dir; analyze_consequences needs analyzeAlternativeSplicing and SignalP"),
  ]),
 dict(index=4, type="Variant B", label="Functional consequences: planted poison-exon (NMD) and ubiquitin-domain-loss switches; real chrX ORF/NMD check",
  status="PARTIAL", status_flag="\u274c", executed=True,
  execution_note="Ran run/40a_input4_prep.R, 40b_annot.sh + 40b2_hmmscan.sh (CPC2 in as-cpc2, HMMER hmmscan --cut_ga vs Pfam-A in as-annot), 40c_domtbl_to_pfamscan.py (own bridge), 40d, 36a-36d on real chrX. NOT executed: SignalP, IUPred2A, DeepTMHMM (licence-gated; analyzeSignalP/analyzeIUPred2A only tested for their missing-file errors). The consequence steps on synthetic data needed the ORF step reordered (see assertions).",
  note="Domain loss 10/10 with correct direction and quiet elsewhere; ES-only splicing classes right; PTC flag == planted poison isoform for all 72 isoforms (distance == |P|+|E3| for all 10, both strands). With the Skill's CPC2 removeNoncodinORFs=TRUE, 2/10 poison isoforms lose their NMD call (10/10 without CPC2). Skill order extractSequence->analyzeORF fails on a CDS-less GTF; hmmscan --domtblout is not accepted by analyzePFAM (needs pfam_scan-style rows with a CL clan); the full 8-consequence list errors when SignalP/IUPred are not imported. Real chrX: annotated-ORF PTC v Ensembl NMD biotype sens 0.96 / spec 1.00, but the Skill's analyzeORF(longest) overwrites annotated ORFs (sens 0.64 / spec 0.89).",
  basic=25, specialized=38,
  assertions=[
   A("The documented order (extractSequence before analyzeORF) works", False, "fails on GTF without CDS ('Please run addORFfromGTF()... to detect ORFs'); works only when the GTF carries CDS lines"),
   A("analyzePFAM accepts the output of the tool the Skill names (hmmscan against Pfam-A)", False, "raw --domtblout: 'more columns than column names'; needs pfam_scan-style table with a CL clan column (Pfam-A.clans.tsv bridge used); Skill silent"),
   A("With the Skill's settings all 10 planted poison isoforms are flagged NMD-sensitive and up-regulated", False, "8/10 with CPC2 removeNoncodinORFs=TRUE (2 poison ORFs discarded as noncoding); 10/10 without CPC2"),
   A("Domain-loss consequence flags the skipped-exon isoform with the right direction and stays quiet elsewhere", True, "10/10 'Domain loss' (C up, A down); 0 domain calls outside the 10 planted genes"),
   A("Predicted NMD status agrees with an independent reference on real annotation", True, "annotated-ORF PTC v Ensembl nonsense_mediated_decay biotype: sens 0.96 (48/50), spec 1.00 (1023/1028)"),
  ]),
 dict(index=5, type="Stress", label="Batch-confounded design and sample-order hazard (SYNTHETIC)",
  status="COMPLETED", status_flag="\u26a0\ufe0f", executed=True,
  execution_note="Ran run/50_input5_batch_order.R. synthB = synth with b2 batch shifting A->C by 40% in 30 null genes, batch imbalanced with condition (ctrl 5 b1/1 b2, trt 1 b1/5 b2). The Skill shows a condition-only designMatrix and a positional condition vector.",
  note="Condition-only design (the Skill's): 19/30 batch-artefact genes called. A batch column in ISAR's designMatrix (not mentioned by the Skill): artefacts 19 -> 0 and planted 20/20 kept, but 4 other null genes called. Perfect confounding gives a clear 'not full rank' error. Skill's positional condition vector with SRR-style IDs that do not sort by condition: 0/20 planted recovered (silent), 20/20 when joined by sample ID.",
  basic=23, specialized=35,
  assertions=[
   A("The Skill's positional design vector is correct for arbitrary sample IDs", False, "samples sorted alphabetically by importIsoformExpression; half the labels wrong -> 0/20 planted recovered, no warning"),
   A("The Skill tells the agent how to handle batch/covariates", False, "no mention; ISAR accepts extra designMatrix columns"),
   A("Adding a batch column removes the batch artefacts without losing planted switches", True, "artefact genes called 19/30 -> 0/30; planted 20/20 (4 other null FP)"),
   A("Perfect confounding is caught explicitly", True, "'The supplied design matrix will result in a model matrix that is not full rank'"),
  ]),
 dict(index=6, type="Scope Boundary", label="Inferential-uncertainty (fishpond/swish) branch and long-read style count-only import",
  status="COMPLETED", status_flag="\u26a0\ufe0f", executed=True,
  execution_note="Ran run/60_input6_swish.R: real Salmon Gibbs (20 reps) chrX 2 v 2; SYNTHETIC 6 v 6 with planted DTE truth and Poisson-resampled 'inferential replicates'; count-only importRdata. tximeta -> linkedTxome match FAILED in this env (Salmon 2.7 index metadata, 'Unknown or uninitialised column sha256'), so rowData(se)$gene_id/tx_id lines were not executed on real tximeta output; that line was tested on a SIMULATED CharacterList rowData.",
  note="swish 6 v 6 synthetic: 33/35 planted up transcripts called, all log2FC>0, 29 FP of 848 (3.4%). Real 2 v 2: 6 transcripts q<0.05 (24 permutations available; coarse p). Skill's swish(y, x='condition') errors unless colData condition is a factor. Skill's data.frame(gene_id = rowData(se)$gene_id, ...) breaks when gene_id is a CharacterList (simulated). Count-only importRdata (long-read style) recovers 20/20. installed ISAR 2.6.0 has no long-read/single-cell mode argument; the Skill's v2 claims (2.11+) cannot be verified here.",
  basic=28, specialized=41,
  assertions=[
   A("The Skill's tximeta-based first lines give a transcript table usable by dmDSdata", False, "not executable on real tximeta output here; SIMULATED CharacterList gene_id -> data.frame gives gene_id.group/.group_name/.value columns"),
   A("swish(y, x='condition') runs as written", False, "'is.factor(condition) is not TRUE' with a default data.frame coldata; Skill leaves coldata undefined"),
   A("swish recovers planted DTE-up transcripts in the right direction", True, "33/35, all log2FC>0"),
   A("swish false-positive rate <=5% on non-DTE transcripts", True, "29/848 = 3.4%"),
   A("Count-only importRdata (the Skill's long-read route) recovers the planted switches", True, "20/20, 2 null FP"),
  ]),
 dict(index=7, type="Adversarial", label="Unreplicated 1 v 1, mismatched/versioned annotation, and the Skill's Common Errors table",
  status="COMPLETED", status_flag="\u26a0\ufe0f", executed=True,
  execution_note="Ran run/70_input7_adversarial.R on SYNTHETIC quants: 1 v 1 design; Ensembl-style '.1' version suffix on quant IDs against an unversioned GTF; real chrX GTF against synthetic quants; then each Common Errors row triggered and the real message recorded.",
  note="1 v 1 stops with ISAR's own error (no test cannot be performed without replicates); the Skill never mentions minimum replicates. '.1'-suffixed IDs fail with a Jaccard-0 annotation error; the Skill's remedy (rebuild the Salmon index) is wrong for the common version-suffix cause (importRdata ignoreAfterPeriod). Common Errors messages are paraphrases: real texts differ, and 'analyzeSwitchConsequences: not enough switching genes' actually surfaces at isoformSwitchTestDEXSeq as 'No genes were considered switching with the used cutoff values' (hard stop with reduceToSwitchingGenes=TRUE).",
  basic=29, specialized=40,
  assertions=[
   A("An unreplicated 1 v 1 request is refused rather than reported as significant switches", True, "ISAR: 'A statistical test cannot be performed without replicates'; not from the Skill text"),
   A("A wholly wrong annotation is rejected with a clear error", True, "Jaccard similarity < 0.925, 0 overlap, message names the mismatch"),
   A("The Skill's remedy for annotation mismatch fixes the common Ensembl version-suffix case", False, "quant IDs 'X.1' v GTF 'X' -> error; fix is ignoreAfterPeriod, not rebuilding the index"),
   A("Error strings in the Common Errors table match what the tools print", False, "dmFilter: '!No genes left after filtering!'; analyzeIUPred2A: 'file(s) ... does not exist'; swish: 'there are no inferential replicates in the assays'; consequences: 'No genes were considered switching...'"),
  ]),
]
for i in inputs:
    i["assertions_passed"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")
    i["assertions_total"] = len(i["assertions"])
    i["total"] = i["basic"] + i["specialized"]
    assert 3 <= i["assertions_total"] <= 5
n = len(inputs); avg = round(sum(i["total"] for i in inputs) / n, 1)
cats = {
 "functional_suitability": (8, 12, "Covers ISAR v2 workflow, manual DRIMSeq/DEXSeq/stageR, swish, NMD/AS-NMD interpretation. Core detection verified against planted truth. Deductions: documented snippets that fail as written (samples(d), extractSequence order, full consequence list), wrong 'silently drops' and dmFilter-default claims, unverifiable v2 auto-selection."),
 "reliability": (7, 12, "Common Errors table exists but its messages are paraphrases and two remedies are wrong (version suffix, no-switch stop); example has file.exists guards that defer the crash; no n>=3 / replicate check."),
 "performance_context": (5, 8, "440-line SKILL.md with no references/ directory and a usage-guide that repeats it; linear workflow otherwise."),
 "agent_usability": (10, 16, "Clear DGE/DTE/DTU table and decision tree (learnability). Inconsistent: satuRn in a 3v3 example v its own >5-replicate rule; analyzeORF ordering differs between snippets. Few checkpoints for verifying imports or counts."),
 "human_usability": (5, 8, "Technical but keyword-rich description; sample-order and batch mistakes are not forgiven or flagged."),
 "security": (11, 12, "No credentials, no eval/exec, local R only; design vector and sample IDs are not validated."),
 "maintainability": (8, 12, "SKILL + usage guide + example, cross-links resolve (all related skills exist). Example is a commented stub with hard-coded file names; no test data or expected output."),
 "agent_specific": (13, 20, "Trigger description precise. Progressive disclosure weak (no references). Escape hatches thin: no replicate minimum, no note that SignalP/IUPred2A/DeepTMHMM are licence-gated, no note that CPC2 filtering can drop PTC isoforms."),
}
sub = sum(v[0] for v in cats.values())
static_w = round(sub * 0.4, 1); dyn_w = round(avg * 0.6, 1); score = round(static_w + dyn_w)
assert sub == 67 and avg == 65.7 and score == 66
recs = [
 dict(priority="P1", title="Manual DTU pipeline stops at samples(d) after library(DEXSeq)", observed_in=[2],
  problem="Biobase::samples masks DRIMSeq::samples, so model.matrix(~ condition, data = samples(d)) and sampleData = samples(d) fail with 'unable to find an inherited method' (verified with the Skill's exact library order, DRIMSeq 1.34.0, DEXSeq 1.52.0).",
  root_cause="Snippet was never run with all four packages attached; the design_full line is also unused.", fix="Write DRIMSeq::samples(d) in both places (or drop the unused design_full line) and state the masking."),
 dict(priority="P1", title="Default count route silently changes DTU results; shipped example stops on real data", observed_in=[3],
  problem="importIsoformExpression defaults (scaledTPM counts) followed by isoformSwitchTestDEXSeq found 0 switches on real chrX 2v2 (RPL10 dIF -0.33, q=1) while raw NumReads or lengthScaledTPM found 26 isoforms in 20-22 genes; run_switch_analysis in the example then stops with 'No genes were considered switching'. The Skill never discusses count v abundance scaling.",
  root_cause="Count derivation (calculateCountsFromAbundance / countsFromAbundance) and reduceToSwitchingGenes=TRUE hard stop are undocumented; example was never run on data.",
  fix="Add a short section: which count route the tests use, compare calculateCountsFromAbundance=TRUE/FALSE on the user's data, and wrap the test in a check that reports zero switches instead of erroring; run the example on the shipped test data."),
 dict(priority="P1", title="Shipped example is a banner plus functions that do not run in the order given", observed_in=[3, 4],
  problem="Run as shipped it prints one line. Calling its functions: extract_sequences fails on GTF without CDS (ORFs not yet predicted) and when the output directory does not exist; analyze_consequences fails because intron_retention needs analyzeAlternativeSplicing() (SKILL.md calls it, the example does not) and signal_peptide_identified needs SignalP; annotation.gtf/transcripts.fa are hard-coded.",
  root_cause="Example was written from the API names, not executed end to end.", fix="Make the example runnable on a bundled toy dataset: analyzeORF before extractSequence when the GTF has no CDS, dir.create the output, add analyzeAlternativeSplicing, and build the consequence list only from annotators that were imported."),
 dict(priority="P1", title="Consequence workflow order and annotator formats are wrong or missing", observed_in=[4],
  problem="SKILL.md runs extractSequence before analyzeORF (fails without CDS); says analyzeSwitchConsequences 'silently drops' consequence types with no annotation, but it errors ('the result of the SignalP analysis must be available'); names hmmscan for Pfam but analyzePFAM needs pfam_scan-style rows containing a CL clan (raw --domtblout fails); calls analyzeORF(longest) unconditionally, which overwrote annotated ORFs on real chrX (PTC v Ensembl NMD biotype sens 0.96 -> 0.64, spec 1.00 -> 0.89); CPC2 removeNoncodinORFs=TRUE removed 2/10 planted poison isoforms from the NMD call.",
  root_cause="External-annotator interfaces and ISAR ORF logic were paraphrased rather than exercised.", fix="Give the exact order (addAnnotatedORFs/ analyzeORF first when needed), the pfam_scan or web-server format analyzePFAM expects, the real failure text for missing annotators, and a warning that CPC2 filtering can drop PTC-bearing isoforms; use annotated ORFs when the GTF has CDS."),
 dict(priority="P1", title="Design construction is positional and ignores replicates and batch", observed_in=[1, 5, 7],
  problem="The design vector is hard-coded positionally against colnames(counts)[-1] (alphabetical): with SRR-style IDs it mislabels half the samples and recovered 0/20 planted switches with no warning. The Skill gives no minimum-replicate guidance (1v1 only stops through ISAR's own error) and does not mention that ISAR accepts a batch column (batch-confounded data: 19/30 artefact genes called without it, 0 with it). The 3v3 example uses satuRn although the Skill's own rule and ISAR's warning say DEXSeq for <=5 replicates.",
  root_cause="Example design matrix is illustrative but presented as the recipe.", fix="Build the design by joining sample metadata on sampleID, add a batch/covariate line, state n>=3 per condition and choose DEXSeq for <=5 replicates in the example call."),
 dict(priority="P2", title="dmFilter 'default too strict' claim is wrong; thresholds hard-coded for 6 samples", observed_in=[3],
  problem="DRIMSeq 1.34.0 dmFilter defaults are all 0 (no filtering); the quoted 3/10 values are the Skill's own example. min_samps_gene_expr=6 errors on n=4 with a cryptic message.", root_cause="Example values described as defaults.", fix="Say these are suggested values, scale min_samps_* to group sizes."),
 dict(priority="P2", title="Common Errors table is paraphrased and partly misdirected", observed_in=[7],
  problem="Real messages: 'The annotation and quantification ... seems to be different (Jaccard similarity < 0.925)', '!No genes left after filtering!', 'No genes were considered switching with the used cutoff values' (at the test step), 'there are no inferential replicates in the assays'. Version-suffixed IDs need ignoreAfterPeriod, not a new Salmon index.", root_cause="Messages written from memory.", fix="Quote the real text and the right argument."),
 dict(priority="P2", title="ISAR v2 claims (auto-select satuRn, long-read/single-cell mode, 2.11+) not verifiable", observed_in=[1, 6],
  problem="Installed ISAR 2.6.0 (Bioc 3.20) has no auto-selection wrapper and no long-read/single-cell argument; the bioRxiv paper (Han et al 2025, 10.64898/2025.12.08.693027) exists but the version pin 2.11+ does not correspond to an installable Bioconductor release here.", root_cause="Claims taken from the preprint abstract.", fix="Name the exact version/branch, or describe the explicit isoformSwitchTestSatuRn/DEXSeq choice."),
 dict(priority="P2", title="swish/tximeta snippets are incomplete", observed_in=[6],
  problem="coldata is undefined and its condition column must be a factor for swish; rowData(se)$gene_id from tximeta is a CharacterList so the txdf data.frame() line misbehaves (simulated); infRV filtering is described but no code; tximeta needs a linkedTxome matching the Salmon index.", root_cause="Snippets not executed against tximeta output.", fix="Show coldata construction with factor(), unlist the gene_id, and add computeInfRV()."),
 dict(priority="P2", title="Small factual points and licence gating", observed_in=[],
  problem="STMN2 cryptic exon is a premature-polyadenylation truncation, not PTC-NMD like UNC13A; the '~22% escape NMD' figure is not verified; SignalP, IUPred2A and DeepTMHMM are licence/cloud-gated and not flagged; SKILL.md is 440 lines with no references/ and a repeating usage-guide.",
  root_cause="Prose summarised from reviews.", fix="Correct the STMN2 mechanism, cite the figure or drop it, flag the gated tools, move detail into references/ and dedupe the usage guide."),
]
report = {
 "meta": {"skill_name": "bio-isoform-switching",
  "description": "Analyzes differential transcript usage (DTU) and isoform switches with functional consequence prediction (NMD via the 50 nt rule, ORF disruption, domain loss/gain, signal peptide, IDR, coding potential) using IsoformSwitchAnalyzeR, the manual DRIMSeq -> DEXSeq/satuRn -> stageR pipeline, and fishpond/swish.",
  "source": SRC, "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Complex", "n_inputs": n,
  "tool_versions": {"R": "4.4.3", "Bioconductor": "3.20", "IsoformSwitchAnalyzeR": "2.6.0", "DRIMSeq": "1.34.0", "DEXSeq": "1.52.0", "satuRn": "1.14.0", "stageR": "1.28.0", "fishpond": "2.12.0", "tximport": "1.34.0", "tximeta": "1.24.0", "CPC2": "standalone (python 2.7)", "HMMER": "3.4 + Pfam-A 2026-09"},
  "not_executed": ["SignalP (licence)", "IUPred2A (licence)", "DeepTMHMM (cloud/licence)", "tximeta rowData(se)$gene_id path on real tximeta output (linkedTxome did not match the Salmon 2.7 index; simulated)", "ISAR v2 long-read / single-cell modes (not in installed 2.6.0)"],
  "data": "Synthetic planted switches in run/data/synth (labelled synthetic) plus real nf-core rnasplice chrX GBR v YRI 2 v 2 (public-data)."},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOIs, PMIDs or results; ISAR v2 preprint DOI and satuRn F1000Research 10:374 verified via Crossref/bioRxiv API. Unverified '~22% NMD escape' figure and the STMN2-as-NMD example are P2 accuracy notes, not fabrication."},
   "practice_boundaries": {"result": "PASS", "detail": "Research-level analysis only; no diagnostic or prescriptive statements. ASO/STK-001 mention is descriptive."},
   "methodological_ground": {"result": "PASS", "detail": "DTU vs DTE vs DGE framing, stageR two-stage control and NMD direction caveats are sound (DGE decoys not called, DTE detected by swish). Positional design vector, missing batch/replicate guidance and count-route sensitivity are P1 defects but no principled fallacy."},
   "code_usability": {"result": "PASS", "detail": "All API arguments exist in installed versions and every core call ran; failures (samples(d) masking, extractSequence order, missing-annotator consequence list, raw domtblout, swish factor) are one-line or ordering fixes recorded as P1. No syntax errors or infinite loops."}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100,
  "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
  "inputs": inputs},
 "final": {"static_weighted": static_w, "dynamic_weighted": dyn_w, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "\u26a0\ufe0f", "deployable": False, "veto_override": False},
 "key_strengths": [
  "Core DTU detection is accurate: on planted truth IsoformSwitchAnalyzeR, DEXSeq/DRIMSeq/stageR recover 20/20 switches with correct isoform, direction and dIF (dIF matches a hand computation to 7e-5) while gene-level DGE decoys and null splits stay quiet.",
  "The DGE v DTE v DTU framing and tool-selection tables are correct and were demonstrated (DGE-only genes not called by DTU tools, called by swish).",
  "NMD/PTC logic is right: PTC flag equals the planted poison isoform for all 72 isoforms and, on real chrX annotation, matches Ensembl NMD biotype (sens 0.96, spec 1.00); domain-loss consequences recovered 10/10 with correct direction.",
  "Every function and argument named in SKILL.md exists in the installed packages; cited literature checks out where verified."],
 "recommendations": recs}
assert [r["priority"] for r in recs] == sorted(r["priority"] for r in recs)
with io.open(os.path.join(OUT, "eval_report_bio-isoform-switching_result.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
# ---------- viewer ----------
L = []
L.append("# Eval Viewer - bio-isoform-switching\n\nGenerated: 2026-09-20 | source: `%s` | Category 3 Data Analysis | Mode A | Complex, N=7\n" % SRC)
L.append("Scripts and logs: `run/` (every script named below). Synthetic data: `run/data/synth` (SYNTHETIC, seeded, planted truth in `truth_genes.tsv`). Real data: nf-core rnasplice chrX GBR v YRI 2 v 2 from `audit-envs/alternative-splicing/public-data`. Not executed: SignalP, IUPred2A, DeepTMHMM (licence-gated).\n")
L.append("## Summary Table\n\n| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|---|")
for i in inputs:
    L.append("| %d | %s | %s | %d | %d | %d | %d/%d PASS | %s %s |" % (i["index"], i["type"], "yes", i["basic"], i["specialized"], i["total"], i["assertions_passed"], i["assertions_total"], i["status_flag"], i["status"]))
L.append("\n**Execution Average: %.1f / 100** | **Assertion Pass Rate: %d/%d** | Static 67 x 0.4 = %.1f | Dynamic %.1f x 0.6 = %.1f | **FINAL 66 - Beta Only (not deployable; no veto, no P0)**\n" % (avg, sum(i["assertions_passed"] for i in inputs), sum(i["assertions_total"] for i in inputs), static_w, avg, dyn_w))
L.append("Floors: Static 67 (<70), Layer 1 avg 26.9 (<28), Layer 2 avg 38.9 (<42), assertions 58% (<80%): grade capped at Beta Only by score in any case.\n")
L.append("## Step 1 - Skill Veto\nT1 PASS (all failures deterministic, one-line/ordering fixes; no random crash, loop or unresolvable dependency) | T2 PASS (frontmatter name, description, tool_type, primary_tool, license present) | T3 PASS (re-ran Input 1: identical PASS/FAIL, counts and minimum q; swish seeded) | T4 PASS (no eval/exec, no credentials).\n")
L.append("## Step 2 - Static (67/100)\n\n| Category | Score | Note |\n|---|---|---|")
for k, v in cats.items(): L.append("| %s | %d/%d | %s |" % (k, v[0], v[1], v[2]))
L.append("\n## Version and claim verification (installed: ISAR 2.6.0, DRIMSeq 1.34.0, DEXSeq 1.52.0, satuRn 1.14.0, stageR 1.28.0, fishpond 2.12.0, tximeta 1.24.0)\n")
L.append("- `run/00_versions.log`: every function/argument used in SKILL.md and the example exists (importIsoformExpression, importRdata, preFilter incl. IFcutoff/keepIsoformInAllConditions, isoformSwitchTestSatuRn/DEXSeq, extractSequence, analyzeORF/CPC2/PFAM/SignalP/IUPred2A, analyzeAlternativeSplicing, analyzeSwitchConsequences, extractTopSwitches, switchPlot, extractConsequenceSummary/Enrichment, extractSplicingSummary, extractSwitchSummary). `addIsofomIdAsColumn`, `isoformExonAnnoation` spellings are the package's own.\n- No installed function auto-selects satuRn/DEXSeq; ISAR warns satuRn is not advised with few replicates. No long-read/single-cell argument in importRdata (2.6.0).\n- `01_docs.log`: DRIMSeq dmFilter defaults are all 0 (the Skill's 'default too strict' is wrong). ISAR analyzePFAM needs pfam_scan / web-server rows with a CL clan column.\n- Citations: ISAR v2 bioRxiv 10.64898/2025.12.08.693027 (Han et al 2025) and satuRn F1000Research 10:374 confirmed via bioRxiv/Crossref APIs.\n- Shipped-means-present: SKILL.md, usage-guide.md, examples/isoform_switch_analysis.R exist; all Related Skills paths exist. No missing primary file.\n")
L.append("## Detailed Outputs\n")
detail = {
1: ("Import Salmon, pre-filter, test switches; find the 20 planted switches (3 v 3).", "run/10_input1_isar_3v3.R, helpers.R, 11_dif_check.R; logs 10_input1.log, 10_input1_rerun.log",
 "```\n[PASS] ISAR dIF == hand-computed mean-of-sample-IF dIF | max abs diff 7.32e-05 over 871 isoforms\ntested genes 300 | planted switches recovered 20/20 | null-gene false positives 2 (of 260) GENE175,GENE206 (DEXSeq) / 0 (satuRn)\ndge_only called 0 | small_switch (dIF~0.06) called 0 | dte_like (true dIF 0.15) called 3\n[PASS] direction correct 20/20 ; dIF within 0.1 of planted truth 20/20\n[PASS] NULL comparison DEXSeq: 1 isoform call in 300 tested genes; satuRn 0\nWarning: isoformSwitchTestSatuRn: You seem to have few replicates. We therefore recommend isoformSwitchTestDEXSeq()\n```"),
2: ("Manual DRIMSeq -> DEXSeq -> stageR on 6 v 6.", "run/20_input2_manual_dtu.R, 21_samples_mask.R; logs 20_input2.log",
 "```\nsamples(d) unqualified: ERROR: unable to find an inherited method for function 'samples' for signature 'object = \"dmDSdata\"'   (find('samples') -> Biobase, DRIMSeq)\n--- after DRIMSeq::samples(d) ---\ngene-level q<0.05: 26 genes | planted 20/20 | null-gene FP 1 | dge_only 0 | small(0.06) 0 | dte_like(0.15) 5\n[PASS] stageR confirms B/C transcript in 20/20 | DRIMSeq dmTest 27 genes, Jaccard 0.89\nnull split: 2 gene-level calls, 3 stageR-confirmed transcripts, 2 naive-BH transcripts\ndtuScaledTPM: 27 genes, planted 20/20\n```"),
3: ("Real chrX 2 v 2 plus the shipped example.", "run/30_input3_real_chrX.R, 35a_shipped_example_prep.R, 35a2-35a6, 31_dmfilter_defaults.R; logs 30_input3.log, 35a*.log",
 "```\nSkill design vector on 4 files: ERROR arguments imply differing number of rows: 4, 6 (loud)\ndmFilter(min_samps_gene_expr=6) on n=4: ERROR min_samps_gene_expr <= ncol(x@counts) is not TRUE\nDEXSeq 19 | DRIMSeq 12 | ISAR 20 genes ; DEXSeq v DRIMSeq overlap 6 ; ISAR v DEXSeq Jaccard 0.77\ntop switch RPL10 ENST00000406022: ISAR dIF -0.3291 vs hand -0.3356\nSkill path (importIsoformExpression defaults):   q<0.05 & |dIF|>0.1 isoforms 0, RPL10 q 1\ncalculateCountsFromAbundance=FALSE / tximport raw: isoforms 26, genes 20, RPL10 q 4.6e-18\ntximport lengthScaledTPM: 28 isoforms / 22 genes ; scaledTPM, dtuScaledTPM through ISAR: 0\nplain DEXSeq on scaledTPM counts: 2 genes, RPL10 q=0 (ISAR wrapper gives q=1; cause not isolated)\nshipped example as shipped: banner only. run_switch_analysis: ERROR No genes were considered switching\n```"),
4: ("Functional consequences (planted NMD + domain loss; real chrX).", "run/40a_input4_prep.R, 40a3_ptc_independent.R, 40b_annot.sh, 40b2_hmmscan.sh, 40b3_clans.sh (unused), 40c_domtbl_to_pfamscan.py, 40d_input4_consequences.R, 36a-36d",
 "```\nSkill order extractSequence -> analyzeORF: ERROR Please run the 'addORFfromGTF()' ... to detect ORFs\nPTC flag == planted poison isoform for 72/72 ; distance(ISAR) == |P|+|E3| for 10/10 (6 plus, 4 minus strand)\nhmmscan --cut_ga vs Pfam-A: ubiquitin PF00240 E~1e-32 in A and B isoforms of all 10 skip genes, never in C\nanalyzePFAM(raw --domtblout): ERROR more columns than column names ; after pfam_scan-style bridge with clan: 60 domains imported\nfull 8-consequence list w/o SignalP: ERROR To test differences in signal peptides, the result of the SignalP analysis must be available\nNMD (CPC2 removeNoncodinORFs=TRUE): 8/10 poison genes ; without CPC2: 10/10 ; domain loss 10/10 ; ES-only splicing 24 ES, 0 IR/A3/A5\nreal chrX: annotated-ORF PTC v Ensembl NMD biotype sens 0.96 (48/50) spec 1.00 ; after analyzeORF(longest): sens 0.64 spec 0.89, all orf_origin -> Predicted\nreal end-to-end consequence table 110 rows (IR, coding potential, ORF, NMD, domains)\n```"),
5: ("Batch-confounded synthetic design and sample-order hazard.", "run/50_input5_batch_order.R; log 50_input5.log",
 "```\nno batch column:  planted 20/20 | batch-artefact genes called 19/30 | other null FP 0 | total 45\nbatch column:     planted 20/20 | batch-artefact genes called  0/30 | other null FP 4 | total 28\nbatch == condition: ERROR The supplied design matrix will result in a model matrix that is not full rank\npositional vector (Skill pattern), SRR IDs: planted recovered 0/20 ; joined by sample ID: 20/20\n```"),
6: ("swish / tximeta / count-only import.", "run/60_input6_swish.R; log 60_input6.log",
 "```\ntximeta linkedTxome: 'couldn't find matching transcriptome' (Salmon 2.7 index metadata), rowData empty -> gene_id lines not executed\nSIMULATED CharacterList gene_id: data.frame() gives gene_id.group, gene_id.group_name, gene_id.value columns\nswish(y, x='condition'): ERROR is.factor(condition) is not TRUE (default data.frame coldata)\nreal 2v2 swish: 391 tested, 6 q<0.05 ; 24 permutations available\nsynthetic 6v6: 33/35 planted DTE-up called (all log2FC>0), FP 29/848\ncount-only importRdata: planted 20/20, null FP 2\n```"),
7: ("Unreplicated, mismatched annotation, Common Errors.", "run/70_input7_adversarial.R; log 70_input7.log",
 "```\n1v1: ERROR A statistical test cannot be performed without replicates.\n'.1'-versioned quant IDs v unversioned GTF: ERROR ... Jaccard similarity < 0.925 ... Only 0 overlap\nreal GTF v synthetic quants: same error, 900 quantified v 6001 annotated\nanalyzeIUPred2A(missing): ERROR (At least on of) the file(s) ... does not exist ; analyzeSignalP(missing): ERROR The file(s) ... does not exist\nscaleInfReps/swish(no infReps): ERROR there are no inferential replicates in the assays of 'y'\ndmFilter impossible thresholds: ERROR !No genes left after filtering!\nisoformSwitchTestDEXSeq(reduceToSwitchingGenes=TRUE, no switches): ERROR No genes were considered switching with the used cutoff values\n```"),
}
for i in inputs:
    d = detail[i["index"]]
    L.append("### Input %d - %s\n**Prompt (realistic request):** %s\n\n**Executed:** true - %s\n\n**Code:** %s\n\n**Output (trimmed):**\n%s\n\n**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100\n\n**Assertions:**" % (i["index"], i["type"], d[0], i["execution_note"], d[1], d[2], i["basic"], i["specialized"], i["total"]))
    for a in i["assertions"]: L.append("- [%s] %s - %s" % (a["result"], a["text"], a["note"]))
    L.append("")
L.append("## Research Veto (Category 3)\nM1 PASS | M2 PASS | M3 PASS | M4 PASS (details in the JSON). No safety or scope assertion failed.\n")
L.append("## Recommendations\n")
for r in recs: L.append("- **[%s] %s** (inputs %s): %s Fix: %s" % (r["priority"], r["title"], r["observed_in"], r["problem"], r["fix"]))
L.append("\n## Clean-up checks\nNothing written inside `F:\\OpenScience\\external\\`; `find <clone> -name __pycache__` returned nothing. Copied Skill under `run/skill`. No symlinks in `run/`. Large intermediates (.rds, real GTF/FASTA copies) deleted.\n")
with io.open(os.path.join(OUT, "eval_viewer_bio-isoform-switching.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(L))
print("ok", score, avg, sub)
