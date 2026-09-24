# Builds ../eval_report_bio-isoform-switching_result.json (schema: skill-auditor/references/report_json_schema.md) and checks the pre-emit list.
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "eval_report_bio-isoform-switching_result.json")

def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = []
def add(index, typ, label, status, note, basic, spec, assertions, executed=True, exec_note="", new=False, regression_of=None):
    total = basic + spec
    p = sum(1 for a in assertions if a["result"] == "PASS")
    flag = "✅" if status == "COMPLETED" and total >= 75 else ("⚠️" if status == "COMPLETED" else "❌")
    d = {"index": index, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note, "basic": basic, "specialized": spec,
         "total": total, "assertions_passed": p, "assertions_total": len(assertions), "assertions": assertions,
         "executed": executed, "execution_note": exec_note, "new_input": new}
    if regression_of: d["regression_of"] = regression_of
    inputs.append(d)

add(1, "Canonical", "SKILL workflow block verbatim on synthetic 3v3 (DEXSeq) and 6v6 (satuRn), shuffled SRR IDs, plus null comparison and sample-ID error messages", "COMPLETED",
    "3v3 DEXSeq 20/20 planted, direction and dIF within 0.1 of truth 20/20, 2/260 null FP; 6v6 satuRn 20/20, 0/260 null FP; ID errors now name the samples (5/5 cases)",
    37, 52, [
    A("ISAR dIF equals an independent hand computation from quant.sf TPM", True, "max abs diff 7.32e-05 over 871 isoforms (3v3) and 5.54e-05 over 875 (6v6)"),
    A("All 20 planted switches recovered with correct direction and dIF within 0.1 of truth on both branches", True, "3v3 DEXSeq 20/20; 6v6 satuRn 20/20 (branch chosen by the block's own max(table(condition)) > 5 test); direction 20/20, magnitude 20/20"),
    A("Gene-level-only (DGE) decoys and sub-threshold shifts are not called; null-gene FP <= 5%", True, "dge_only 0/5, small(0.06) 0/10; null FP 2/260 (DEXSeq) and 0/260 (satuRn); control-v-control 1 gene of 300"),
    A("Round-2 fix: the block's sample-ID check names the offending IDs", True, "run/93c: missing row -> 'only in quant: <ID>'; extra row -> 'only in metadata: SRR_EXTRA'; case mismatch names both spellings; duplicate metadata row -> 'duplicated sample_id in metadata'; correct metadata runs to completion"),
    A("Design joined by name is correct when SRR-style IDs and metadata rows are shuffled", True, "20/20 where the pre-fix positional vector gave 0/20 on such IDs")],
    exec_note="run/10_input1_canonical.R, 93c_id_error_message.R; blocks/r_01.R executed verbatim via source(); planted truth in run/data/synth (SYNTHETIC).", regression_of="pre-fix input 1")

add(2, "Variant A", "Manual DRIMSeq-DEXSeq-stageR block verbatim on synthetic 6v6 (and 3v3), shuffled IDs", "COMPLETED",
    "Block runs as written; DEXSeq gene q<0.05 27 genes = 20/20 planted + 1 null + 5 dte-like + 1 small (the composition the Skill states); stageR 20/20; DRIMSeq Jaccard 0.93; 3v3 25 genes, 20/20",
    36, 51, [
    A("The Skill's block runs verbatim and its masking warning is real", True, "block finished; unqualified samples(d) after library(DEXSeq) fails with 'unable to find an inherited method ... dmDSdata'"),
    A("DEXSeq gene level recovers the planted switches with few false calls", True, "27 genes: planted 20/20, null 1/260, dge_only 0, small(0.06) 1, dte-like(0.15) 5 (the Skill states exactly this composition)"),
    A("stageR confirmation names the truly switching transcript", True, "B (poison) or C (skip) confirmed in 20/20 planted genes"),
    A("An independent implementation (DRIMSeq dmPrecision/dmFit/dmTest) reaches the same gene set", True, "27 genes, 20/20 planted, Jaccard 0.93 with DEXSeq"),
    A("Null split and 3v3 behave", True, "ctrl 1-3 v 4-6: 2 gene calls; 3v3 through the block: 25 genes, 20/20 planted")],
    exec_note="run/20_input2_manual_dtu.R, blocks/r_04.R executed verbatim; the preamble the block's comments ask for (meta, files, tx2gene) is mine.", regression_of="pre-fix input 2")

add(3, "Edge", "Real chrX 2 GBR v 2 YRI: SKILL block, shipped example (demo, real, mixed labels), Null-check table, permutation block, seed sensitivity", "COMPLETED",
    "Block 26 isoforms / 20 genes; Null-check table and permutation block reproduce exactly (20/11/15 raw, 0/0/0 default; manual 13/0/4, DRIMSeq 11/4/3, confirmed 12/0/4; permuted 15 11); but sva makes the n=2 mixed-split result seed-dependent (11 genes for 5 of 6 seeds, 0 for seed 5) and the example on that split gave 0",
    34, 47, [
    A("Skill block on real chrX 2v2 reproduces the stated result", True, "26 isoforms in 20 genes; RPL10 ENST00000406022 dIF -0.3291 q 4.63e-18; route table raw 26/20, lengthScaledTPM 28/22, scaledTPM 0/0, dtuScaledTPM 0/0"),
    A("Round-2 Null-check table reproduces cell for cell with the Skill's own blocks", True, "run/96: ISAR raw 20/11/15; manual DEXSeq 13/0/4; DRIMSeq 11/4/3; both 7/0/1; ISAR calls DEXSeq-confirmed 12/0/4; raw-route genes shared with mixed splits 1/20 and 1/20; default route 0/0/0 (run/71)"),
    A("The permutation block runs verbatim as written and gives the stated numbers", True, "observed 20; permuted 15 and 11; exactly 2 alternative splits; 238 s"),
    A("Shipped example runs end to end from a clean copy and warns at n<3", True, "demo: 35 isoforms in 14 genes, 14/14 planted, 8/8 NMD = poison genes, DEMO OK twice; real chrX: 26/20, annotated ORFs, PDF, n<3 warning with the Null-check pointer; missing sample stops naming ERR204916"),
    A("Small-n calls are reproducible run to run", False, "mixed1 split, workflow block verbatim, set.seed 1-6: 11 genes for seeds 1,2,3,4,6 but 0 genes for seed 5 (importRdata's sva step added sv1); the example on the same split (35c) printed 0 while the Skill's table says 11. True split 20 for every seed tried; planted 3v3 22 genes for 6/6 seeds. The Skill mentions sv1 but not that it is random or that it flips the count")],
    exec_note="run/30_input3_real_chrX.R, 35_example_runs.sh, 71_real_label_permutation.R, 72_efflen_factor.R, 96_null_table_real_chrX.R, 99c_sva_seed_determinism.R, 99d_sva_seed_3v3.R; public-data rnasplice chrX (real).", regression_of="pre-fix input 3")

add(4, "Variant B", "Consequence block verbatim (ORFs, sequences, CPC2, hmmscan + converter, Pfam) on synthetic and real chrX", "COMPLETED",
    "Synthetic: NMD 10/10 (8/10 with removeNoncodinORFs=TRUE), Domain loss 10/10, converter rows column-identical; real chrX PTC flag v Ensembl NMD biotype sens 0.96 spec 1.00, corrected post-analyzeORF specificity 0.95 confirmed. SignalP/IUPred2A/NetSurfP-2/DeepTMHMM not run",
    34, 49, [
    A("NMD_status flags the planted poison isoform B as NMD-sensitive and up in 10/10 poison genes; TRUE drops some", True, "10/10 with removeNoncodinORFs=FALSE, 0 calls outside poison genes; 8/10 with TRUE (2 poison B isoforms CPC2 noncoding) as the Skill states"),
    A("domains_identified calls 'Domain loss' A-down/C-up in 10/10 skip genes and stays quiet elsewhere", True, "10/10; 0 outside; PF00240 20 rows / 10 genes never in an isoform C; 0 intron-retention calls (none planted)"),
    A("examples/hmmscan_to_pfamscan.py produces a file analyzePFAM accepts, with columns correct", True, "60 rows converted and imported on the synthetic set; 264 real-chrX rows accepted (clan CL... column); error paths (no args, missing file, plain clans file) exit non-zero with a message"),
    A("Round-2 corrected figures reproduce", True, "annotated ORFs sens 0.96 (48/50) spec 1.00 (1023/1028); after analyzeORF('longest') 0.64 (32/50) / 0.95 (974/1028); orf_origin Annotation -> Predicted 1738; length-factor ranges 0.023-18.1 (Length) and 0.019-575.8 (EffectiveLength)"),
    A("Licence-gated annotators are labelled honestly", True, "SignalP, IUPred2A, NetSurfP-2, DeepTMHMM marked 'not run' / 'read from source'; missing-file errors for SignalP and IUPred2A reproduce with the quoted text; the annotators themselves were not executed here either (no licence)")],
    exec_note="run/40a-40d, 41, 63, 65, 72; CPC2 (as-cpc2) and hmmscan --cut_ga vs Pfam-A (as-annot) in WSL. NOT executed: SignalP, IUPred2A, NetSurfP-2, DeepTMHMM (licence/cloud; labelled in the Skill).", regression_of="pre-fix input 4")

add(5, "Stress", "Batch-confounded synthetic set and adversarial inputs through the block (regression of pre-fix inputs 5 and 7)", "COMPLETED",
    "Batch column removes artefacts (11/30 -> 0/30, planted 20/20); confounded/constant/1v1/suffix errors match the Skill's table; the ID check now names the sample",
    35, 50, [
    A("Ignoring batch produces artefact calls and the block's optional batch line removes them", True, "artefact genes called 11/30 -> 0/30; planted 20/20 both; 5 other null-gene calls appear with the batch column"),
    A("Covariate and replicate errors match the Skill's Common Errors rows", True, "'not full rank'; 'Contain constant information'; 'A statistical test cannot be performed without replicates' all reproduced verbatim"),
    A("Version-suffixed IDs fail as documented and the stated remedy works", True, "Jaccard < 0.925 error; ignoreAfterPeriod = TRUE in both calls imported 875 isoform rows"),
    A("A metadata/quantification mismatch gives an actionable message (round-2 fix)", True, "'sample IDs differ between quantification and metadata. only in quant: SRR7478007 only in metadata:'"),
    A("Remaining Common Errors rows (SignalP/IUPred2A missing file, both dmFilter messages, swish without Gibbs) reproduce", True, "all messages triggered; the dmFilter message now carries the 'min_samps_gene_expr >= 0 &&' clause")],
    exec_note="run/50_input5_stress_adversarial.R, 65_common_errors_rest.R; batch set rebuilt from the regression synthetic data (SYNTHETIC).", regression_of="pre-fix inputs 5 and 7")

add(6, "Scope Boundary", "fishpond/swish block verbatim (real Gibbs 2v2, synthetic 6v6), tximeta path, count-only long-read style import", "COMPLETED",
    "swish numbers reproduce exactly (391 tested, 6 q<0.05, top ENST00000380861 log2FC -1.45, meanInfRV filter keeps 231); synthetic 33/35 TP (all log2FC>0), FP 29/848; tximeta hedge accurate",
    34, 49, [
    A("Skill's swish block runs verbatim and its stated real-data numbers reproduce", True, "391 tested, 6 at q<0.05, top ENST00000380861 log2FC -1.45; block adds meanInfRV column"),
    A("infRV filter example and swish factor requirement work as documented", True, "y[mcols(y)$meanInfRV < 1, ] keeps 231 of 391; character condition -> 'is.factor(condition) is not TRUE'"),
    A("swish recovers planted DTE-up transcripts in the right direction with low FP (synthetic 6v6)", True, "33/35 called, 33/33 log2FC>0, FP 29/848 (3.4%)"),
    A("The Skill's hedge on the tximeta rowData path is accurate", True, "run/61: makeLinkedTxome succeeded, tximeta returned an SE with 0 rowData columns and \"couldn't find matching transcriptome\"; rowData(se)$gene_id not runnable here, as the Skill says (run/60's 6B check is a recorder that always passes; run/61 is the evidence)"),
    A("Count-only importRdata (the Skill's long-read route) recovers the planted switches", True, "20/20, 2 null FP; no long-read/single-cell argument in importRdata 2.6.0")],
    exec_note="run/60_input6_swish.R, 61_tximeta_warning.R; synthetic 'inferential replicates' are Poisson resamples (SYNTHETIC); the tximeta rowData(se)$gene_id lines were NOT executed on real tximeta output.", regression_of="pre-fix input 6")

add(7, "Adversarial", "Claims about ISAR versions and the count route: newer-release source, auto-selection, citation, route mechanism on my own sets", "COMPLETED",
    "Count-route numbers and cause tests reproduce; citation verified; but 'does not choose the test for you' is wrong for isoformSwitchAnalysisPart1 (2.6.0, run with trace) and 'no newer release was available' is wrong (2.8/2.10/2.12 sources exist; 2.12.0 replaces analyzeNetSurfP2 by analyzeNetSurfP3)",
    32, 46, [
    A("Manual-pipeline route numbers on real chrX and the emulation/cause tests reproduce", True, "DEXSeq 13/13/2, DRIMSeq 11/11/7 (raw/lengthScaledTPM/scaledTPM), overlap 7; raw x median(len)/len -> 0 switches; clean simulations (5v5, 4v7, lengths 0.5-5.4 kb) recover 20/20 on every route, so 'a clean simulation will not reveal the problem' holds"),
    A("Citation Han et al. 2026 NAR Genom Bioinform 8(3):lqag098 is real and correctly described", True, "web search + PMC page (PMC13504270): 'IsoformSwitchAnalyzeR v2: analysis of functional isoform changes in long-read and single-cell sequencing data', Han, Gilis, Iriondo Delgado, Clement, Vitting-Seerup, DOI 10.1093/nargab/lqag098; bioRxiv 10.64898/2025.12.08.693027 appears in the results; text 'uses DEXSeq for smaller studies and satuRn for larger studies ... and single-cell data' (page summarised by the fetch tool, wording paraphrased)"),
    A("'2.6.0 does not choose the test for you' is true", False, "isoformSwitchAnalysisPart1() in 2.6.0 contains the rule (any condition > 5 replicates -> isoformSwitchTestSatuRn, else DEXSeq); traced run: 3v3 called isoformSwitchTestDEXSeq, 6v6 called isoformSwitchTestSatuRn (run/99b). Only the two test wrappers themselves merely warn. The rule equals the Skill's manual rule"),
    A("'no newer release was available to check' is true", False, "Bioconductor 3.21/3.22/3.23 carry 2.8.0/2.10.0/2.12.0 as public source tarballs (run/98): same wrappers and warnings, same Part1 rule, calculateCountsFromAbundance still defaults TRUE; 2.12.0 exports analyzeNetSurfP3 instead of analyzeNetSurfP2 (the Skill's NetSurfP-2 rows do not apply to the current release); 2.12.0 needs Seqinfo and could not be installed in this R 4.4/Bioc 3.20 env (run/97), so it was read, not run"),
    A("Covariate paragraph (detectUnwantedEffects, sva, corrected IF/dIF) matches the package", True, "importRdata formals default detectUnwantedEffects = TRUE; 'Added 1 batch/covariates' message and sv1 in designMatrix seen in run/99c and 35c; hand dIF matches ISAR to 7e-5 without a covariate")],
    exec_note="run/70_input7_new_count_route.R, 72_efflen_factor.R, 62_isar_news.R, 64_isar_source_dump.R, 97_install_isar212.R, 98_isar_newer_source.sh, 99b_isar_part1_autoselect.R; web lookups for the citation; data/new1, data/new2 SYNTHETIC (seeds 8801, 8802).", regression_of="pre-fix input 7 (count route) and round-2 targets")

add(8, "Stress", "4v7 unbalanced design with batch column, shuffled IDs; SKILL block and shipped example in real-data mode (first re-audit's new input, now regression)", "COMPLETED",
    "satuRn branch 20/20, 0/195 null FP; example (real-data mode) 20/20 planted, 0 others, NMD-sensitive up in 10/10 poison genes; null 3v4 split 4/250 genes",
    36, 52, [
    A("SKILL block (satuRn branch, 4v7, shuffled IDs and metadata rows) recovers the planted switches with correct direction and size", True, "20/20; dIF within 0.1 of truth 20/20; null FP 0/195; design joined by name correct"),
    A("The block's own batch line works and forcing DEXSeq gives the same picture", True, "with batch: planted 20/20; DEXSeq forced 20/20"),
    A("A null split stays within a normal false-positive rate", True, "3 v 4 split of the 7 treatment samples with batch column: 4 of 250 genes (1.6%)"),
    A("Shipped example in real-data mode recovers the planted set on a design it was not tuned on", True, "20/20 planted, 0 non-planted, batch kept as covariate; ORFs predicted; NMD 'NMD sensitive' up in 10/10 poison genes; PDF > 5 kB"),
    A("Shipped example demo is deterministic and self-checking", True, "run in three separate sessions: identical '35 in 14 genes', 14/14 planted, 8/8 NMD, DEMO OK")],
    exec_note="run/04_gen_new.R (seed 8801, SYNTHETIC), 80_input8_new_unbalanced.R, 81_input8_example.sh, 82_eval_example_new.R, 35a_demo*.log.", regression_of="first re-audit input 8")

add(9, "Stress", "NEW: individual-level heterogeneity null at n = 2, 3, 4, 6 per group, then the Skill's permutation block on planted + heterogeneous data", "COMPLETED",
    "Pure-null set (20% of genes with per-sample isoform shifts): false calls per 250 genes 5/4/5 (n=2), 1/1/4 (n=3), 0/1/2 (n=4), 0/0/0 (n=6, satuRn); permutation block: 3v3 observed 22 v permuted max 6, 6v6 observed 20 v permuted all 0; planted 20/20 in both",
    36, 51, [
    A("False-positive calls under subject-level heterogeneity fall with replicate number, as the guidance (>=3, ideally >=5) assumes", True, "9A, 3 random label draws per n: n=2 4-5 genes (all het genes), n=3 1-4, n=4 0-2, n=6 satuRn 0 of 250; n=3 is not clean, which is why the Skill's permutation check matters"),
    A("The Skill's permutation block runs verbatim on a new data set and separates signal from shuffled labels", True, "3v3 (DEXSeq): observed 22 genes, permuted 0 0 1 4 1 0 0 0 6 (9 splits, 271 s); 6v6 (satuRn): observed 20, permuted 0 x10 (31 s)"),
    A("Workflow block recovers the planted switches despite the heterogeneity", True, "3v3: planted 20/20, het-null called 1/46, other null 1; 6v6: planted 20/20, 0 false calls"),
    A("The permutation block behaves on an unbalanced design", True, "3v5 (run/92b): observed 21, permuted 0 0 2 0 0 0 0 0 0 0; 10 distinct splits, group sizes kept, overlap with the true group always 1 (= k*k/n rounded); 284 s"),
    A("Stated run time and split-count remarks are accurate", True, "about 30 s per call x (splits + 1) here (271-284 s at 9-10 splits; the Skill says 20-40 s per call); 2 splits on 2v2, 9 on 3v3 as stated")],
    exec_note="run/05_gen_het.R + 90_gen_het_data.sh (seeds 9101-9103, SYNTHETIC), 91_input9_het_null.R, 92b_perm_block_unbalanced.R; blocks r_01 and r_02 verbatim.", new=True)

add(10, "Edge", "NEW: unbalanced 3 v 5 design with non-syntactic sample IDs (1-ctrl, trt.1-b): workflow block, manual DTU block, shipped example", "COMPLETED",
    "Workflow block 20/20 planted (1 other gene) and shipped example 20/20 planted, NMD 10/10; the manual DTU block FAILS with 'undefined columns selected' because DRIMSeq rewrites the IDs; passing IDs through make.names() makes it run (20/20 planted)",
    32, 45, [
    A("Workflow block (DEXSeq branch, 3v5, odd IDs) recovers the planted switches with correct direction", True, "21 genes called: planted 20/20, 1 other; dIF > 0 for the switching isoform in 20/20; IDs kept verbatim in the switchAnalyzeRlist"),
    A("Shipped example in real-data mode handles the odd IDs and unbalanced design", True, "40 isoforms in 21 genes, planted 20/20, 1 non-planted, NMD_status up in poison genes >= 9/10, PDF written (114 s)"),
    A("Manual DTU block runs on the same samples", False, "error 'undefined columns selected': DRIMSeq::counts(d) columns are make.names()-ed (X1.ctrl, trt.1.b) and DRIMSeq::samples(d)$sample_id becomes 1..8, so cnt[, samples$sample_id] fails (run/94); the Skill does not warn about this"),
    A("A one-line workaround works and the rest of the block is sound", True, "with sample IDs passed through make.names() (run/95): block verbatim gene q<0.05 23 genes, planted 20/20, 3 other, stageR result table 614 rows"),
    A("Confirm snippet and stageR outputs are reachable on this design without a workaround", False, "the block fails first; stageR returns its table only after the make.names() workaround")],
    exec_note="run/05_gen_het.R odd 3v5 (seed 9104, SYNTHETIC), 92_input10_odd_ids_unbalanced.R, 93_input10_example.sh, 93b_eval_example_odd.R, 94_odd_id_probe.R, 95_odd_id_workaround.R.", new=True)

n = len(inputs)
exec_avg = round(sum(i["total"] for i in inputs) / n, 1)
cats = {
    "functional_suitability": (10, 12, "Covers DTU/DTE/DGE framing, ISAR workflow, permutation null check, manual DRIMSeq/DEXSeq/stageR, swish, NMD and consequence annotation; the round-2 numbers (null table, 0.95 specificity, length ranges, dmFilter message) all reproduce and the citation is real. Deductions: 'does not choose the test for you' is wrong for isoformSwitchAnalysisPart1, 'no newer release was available' is wrong, and the manual block fails on non-syntactic sample IDs."),
    "reliability": (11, 12, "Common Errors rows all re-triggered and matching; the block's ID check now names the samples (5/5 cases); hard stops for replicates, zero switches, missing annotators. Gaps: manual block gives an opaque 'undefined columns selected' on IDs such as 1-ctrl; sva can flip an n=2 result between runs (11 genes -> 0) with no seed guidance."),
    "performance_context": (4, 8, "550 lines / 43.7 KB (~11k tokens) in one SKILL.md with no references/ (491 lines at the first re-audit); the Null check section alone is ~50 lines. Workflow is linear and the example and converter carry the heavy logic, but everything loads at once."),
    "agent_usability": (14, 16, "DGE/DTE/DTU table, ordered consequence steps, numbers and error texts to expect, a runnable permutation block and an explicit recommended route; the count-route and Null check sections are dense and need a careful read."),
    "human_usability": (7, 8, "Natural trigger language; the honest 'exploratory at n = 2' message is now surfaced in the example's warning and points to the check; strict validation is by design."),
    "security": (11, 12, "No credentials, no eval/exec, local R/Python only; example validates metadata and replicate counts; converter validates its input."),
    "maintainability": (10, 12, "SKILL + usage-guide + runnable example with self-assertions + converter; every fenced block extracts and runs verbatim; the many embedded run numbers (tables, 'checked' paragraphs) will drift and no script regenerates them."),
    "agent_specific": (16, 20, "Precise trigger; example and converter are true scripts; stop conditions present; no references/ split at 550 lines; version-behaviour statements (auto-selection, newest release, NetSurfP-2 vs 3) are stale or incomplete for the current Bioconductor release."),
}
static = sum(v[0] for v in cats.values())
sw, dw = round(static * 0.4, 1), round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
grade = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
sym = {"Production Ready": "⭐", "Limited Release": "✅", "Beta Only": "⚠️", "Reject": "❌"}[grade]
assert_pass = sum(i["assertions_passed"] for i in inputs); assert_tot = sum(i["assertions_total"] for i in inputs)

report = {
    "meta": {
        "skill_name": "bio-isoform-switching",
        "description": "Analyzes differential transcript usage (DTU) and isoform switches with functional consequence prediction (NMD via 50nt rule, ORF disruption, protein domain loss/gain, coding-potential shifts; signal peptide and IDR changes when licensed annotators are available). Tools include IsoformSwitchAnalyzeR (DEXSeq up to 5 replicates per condition, satuRn above), the manual DRIMSeq -> DEXSeq/satuRn -> stageR DTU pipeline, and fishpond/swish for inferential-uncertainty-aware DTE.",
        "source": "mrsonord2240/bioSkills@48e3cbc5c3b116ae021618313014e046b688618d:alternative-splicing/isoform-switching",
        "evaluated_on": "2026-09-20",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": n,
        "re_audit": True,
        "re_audit_round": 2,
        "pre_fix_score": 82, "pre_fix_grade": "Limited Release",
        "original_audit_score": 66, "original_audit_grade": "Beta Only",
        "new_inputs": [9, 10],
        "tool_versions": {"R": "4.4.3", "Bioconductor": "3.20", "IsoformSwitchAnalyzeR": "2.6.0 (installed); 2.10.0 and 2.12.0 source read only", "DRIMSeq": "1.34.0", "DEXSeq": "1.52.0", "satuRn": "1.14.0", "stageR": "1.28.0", "fishpond": "2.12.0", "tximport": "1.34.0", "tximeta": "1.24.0", "Salmon quants": "2.7.0", "CPC2": "standalone (python 2.7, as-cpc2)", "HMMER": "3.4 + Pfam-A 2026-09"},
        "not_executed": ["SignalP (licence)", "IUPred2A (licence)", "NetSurfP-2/3 (registration)", "DeepTMHMM (cloud)", "tximeta rowData(se)$gene_id path on real tximeta output (linkedTxome does not match the Salmon 2.7.0 index; the Skill says so)", "IsoformSwitchAnalyzeR 2.8.0-2.12.0 (source read; 2.12.0 needs Seqinfo, not installable in R 4.4 / Bioc 3.20)"],
        "data": "SYNTHETIC planted-truth sets generated by the auditors in run/data (synth seed 20260920; new1 8801 4v7; new2 8802 5v5; het_null/het_3v3/het_6v6 seeds 9101-9103 with per-sample isoform heterogeneity; odd_3v5 seed 9104 with non-syntactic IDs) plus real nf-core rnasplice chrX GBR v YRI 2 v 2 (Salmon quants, Gibbs samples, GTF/FASTA) from audit-envs public-data."
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "Every number quoted in the Skill that I re-derived reproduced (route table 26/28/0/0; Null-check table 20/11/15, 13/0/4, 11/4/3, 12/0/4; permuted 15 and 11; 0.96/1.00 and 0.64/0.95 NMD flag; length ranges; swish 391/6). The Han et al. 2026 citation (NAR Genom Bioinform 8(3):lqag098, DOI 10.1093/nargab/lqag098) exists and is described correctly. Two version statements are inaccurate but not fabricated (P2)."},
            "practice_boundaries": {"result": "PASS", "detail": "Research analysis only; no diagnosis or treatment advice; the SCN1A ASO is stated as 'in clinical development, phase not verified'."},
            "methodological_ground": {"result": "PASS", "detail": "The round-2 Null check now states plainly that raw-count calls are not validated at n = 2, are exploratory, and should be checked with a label permutation; my heterogeneity null (n=2..6) and permutation-block runs support the guidance to use >= 3 (ideally >= 5) replicates plus the check."},
            "code_usability": {"result": "PASS", "detail": "All fenced R blocks, the example (demo and real mode) and the converter executed from copies with checked output. One block (manual DTU) fails on non-syntactic sample IDs (P2, one-line workaround verified); licence-gated annotator calls were not run and are labelled so."}
        }
    },
    "static_score": {"subtotal": static, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": exec_avg, "max": 100, "assertion_pass_rate": {"passed": assert_pass, "total": assert_tot}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
    "key_strengths": [
        "The round-2 Null check is honest and reproducible: the chrX table matches cell for cell (20/11/15 raw, 0 default, manual 13/0/4, confirmed 12/0/4), the permutation block runs verbatim and separates signal from shuffled labels on four different data sets (chrX, 3v3, 6v6, unbalanced 3v5)",
        "Core detection has not regressed: 20/20 planted switches with correct direction and size on 3v3, 4v7, 5v5, 6v6 and 3v5 designs, through the block and the shipped example",
        "Shipped example is a real regression test: demo self-asserts (14/14 planted, 8/8 NMD) and reproduces across sessions; real-data mode works on chrX and on designs it was not tuned on, including unbalanced and odd-named samples",
        "Sample-ID handling is now actionable: names the IDs in five mismatch cases; design is joined by name; the Han et al. 2026 citation and the corrected figures (0.95 specificity, length ranges, dmFilter message) verify",
        "Hedging on unrun material is accurate: licence-gated annotators, tximeta rowData and satuRn-on-real-data are labelled as not run"],
    "recommendations": [
        {"priority": "P2", "title": "Manual DTU block fails on non-syntactic sample IDs", "observed_in": [10],
         "problem": "With sample dirs such as 1-ctrl or trt.1-b the manual block stops with 'undefined columns selected': DRIMSeq make.names()-es the count columns (X1.ctrl) and replaces samples(d)$sample_id by 1..n. The workflow block and the example handle the same IDs.",
         "root_cause": "The block indexes DRIMSeq::counts(d) by the original IDs.",
         "fix": "Add a line before dmDSdata: meta$sample_id <- make.names(meta$sample_id); names(files) <- meta$sample_id (verified: block then runs, planted 20/20), or note the requirement next to the block."},
        {"priority": "P2", "title": "ISAR version statements stale or wrong", "observed_in": [7],
         "problem": "The Skill says 2.6.0 'does not choose the test for you' and that no newer release was available to check. isoformSwitchAnalysisPart1() in 2.6.0 (and 2.10.0/2.12.0) does choose (any condition > 5 replicates -> satuRn, else DEXSeq; traced run), only the two test wrappers merely warn. 2.8.0/2.10.0/2.12.0 (Bioc 3.21-3.23) exist and 2.12.0 renames analyzeNetSurfP2 to analyzeNetSurfP3.",
         "root_cause": "Only the test wrappers and the installed Bioc 3.20 release were inspected.",
         "fix": "Say the one-call wrapper isoformSwitchAnalysisPart1 applies the same >5 rule, the wrappers only warn, the rule is unchanged through 2.12.0, and that on Bioc >= 3.23 the NetSurfP importer is analyzeNetSurfP3."},
        {"priority": "P2", "title": "Surrogate-variable step makes n=2 results seed-dependent", "observed_in": [3],
         "problem": "importRdata(detectUnwantedEffects = TRUE) runs sva, which is random: on the real chrX mixed split the workflow block called 11 genes for seeds 1-4 and 6 but 0 for seed 5 (sv1 added), and the shipped example printed 0 on that split while the Null-check table lists 11. The Skill notes sv1 appeared once but not that it is random or that it flips the answer. True split (20) and 3v3 data (22, 0) were stable across seeds.",
         "root_cause": "No set.seed() in the workflow block or example; the Null-check text treats one draw as the result.",
         "fix": "Put set.seed(1) at the top of the workflow block and the example, and say a small-n list can change with the seed when sva adds a surrogate variable (check colnames(aSwitchList$designMatrix))."},
        {"priority": "P2", "title": "SKILL.md is 550 lines in one file", "observed_in": [],
         "problem": "About 11k tokens load at once (was 491 lines); the count-route table, Null check with its block, the consequence details and Common Errors are all in the main file.",
         "root_cause": "No references/ layer; round 2 added content instead of moving it.",
         "fix": "Move Count route + Null check and the Common Errors table into references/ with a one-line pointer each in SKILL.md."},
        {"priority": "P2", "title": "Licence-gated annotators still unrun", "observed_in": [4],
         "problem": "signal_peptide_identified, IDR_identified/IDR_type and isoform_topology were not exercised (SignalP, IUPred2A, NetSurfP, DeepTMHMM); the Skill labels them 'not run' or 'read from source'.",
         "root_cause": "Licence or cloud gating.", "fix": "Keep the flags; add a smoke test when a licence is available."}
    ]
}

# ---- pre-emit checklist
assert len(report["static_score"]["categories"]) == 8
assert report["static_score"]["subtotal"] == sum(c["score"] for c in report["static_score"]["categories"].values())
for k, c in report["static_score"]["categories"].items(): assert 0 <= c["score"] <= c["max"], k
assert len(inputs) == report["meta"]["n_inputs"]
for i in inputs:
    assert 3 <= len(i["assertions"]) <= 5 and i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]) and i["basic"] + i["specialized"] == i["total"]
    assert 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60
assert 2 <= len(report["key_strengths"]) <= 5
order = {"P0": 0, "P1": 1, "P2": 2}; pr = [order[r["priority"]] for r in report["recommendations"]]; assert pr == sorted(pr)
assert report["final"]["grade_symbol"] == sym
with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh: json.dump(report, fh, indent=2, ensure_ascii=False)
print("static", static, "exec_avg", exec_avg, "weighted", sw, dw, "score", score, grade, "| assertions", assert_pass, "/", assert_tot)
print("layer1 avg", round(sum(i["basic"] for i in inputs) / n, 1), "layer2 avg", round(sum(i["specialized"] for i in inputs) / n, 1))
print("inputs:", [(i["index"], i["total"]) for i in inputs])
