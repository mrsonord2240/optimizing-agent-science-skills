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

add(1, "Canonical", "SKILL workflow block verbatim on synthetic 3v3 (DEXSeq) and 6v6 (satuRn), shuffled SRR IDs, plus null comparison", "COMPLETED",
    "3v3 DEXSeq 20/20 planted, direction and dIF within 0.1 of truth 20/20, 2/260 null FP; 6v6 satuRn 20/20, 0/260 null FP; null comparison 1 gene of 300",
    36, 52, [
    A("ISAR dIF equals an independent hand computation from quant.sf TPM", True, "max abs diff 7.32e-05 over 871 isoforms (3v3) and 5.54e-05 over 875 (6v6)"),
    A("All 20 planted switches recovered with correct direction and dIF within 0.1 of truth on both branches", True, "3v3 DEXSeq 20/20; 6v6 satuRn 20/20 (branch chosen by the block's own max(table(condition)) > 5 test); direction 20/20, magnitude 20/20"),
    A("Gene-level-only (DGE) decoys and sub-threshold shifts are not called; null-gene FP <= 5%", True, "dge_only 0/5, small(0.06) 0/10; null FP 2/260 (DEXSeq) and 0/260 (satuRn)"),
    A("Design joined by sample name is correct when SRR-style IDs and metadata rows are shuffled", True, "20/20 where the pre-fix positional vector gave 0/20 on such IDs"),
    A("Control-v-control null comparison stays quiet through the block", True, "1 gene of 300 tested (min isoform q 0.0034)")],
    exec_note="run/10_input1_canonical.R, blocks/r_01.R executed verbatim via source(); planted truth in run/data/synth (SYNTHETIC).", regression_of="pre-fix input 1")

add(2, "Variant A", "Manual DRIMSeq-DEXSeq-stageR block verbatim on synthetic 6v6 (and 3v3), shuffled IDs", "COMPLETED",
    "Block runs as written (samples(d) failure gone); DEXSeq gene q<0.05 27 genes = 20/20 planted + 1 null + 5 dte-like + 1 small (the composition the Skill states); stageR 20/20; DRIMSeq Jaccard 0.93",
    35, 50, [
    A("The Skill's block runs verbatim and its masking warning is real", True, "block finished (700 stageR rows); unqualified samples(d) after library(DEXSeq) fails with 'unable to find an inherited method ... dmDSdata'; find('samples') = Biobase, DRIMSeq"),
    A("DEXSeq gene level recovers the planted switches with few false calls", True, "27 genes: planted 20/20, null 1/260, dge_only 0, small(0.06) 1, dte-like(0.15) 5 (the Skill states exactly this composition)"),
    A("stageR confirmation names the truly switching transcript", True, "B (poison) or C (skip) confirmed in 20/20 planted genes"),
    A("An independent implementation (DRIMSeq dmPrecision/dmFit/dmTest) reaches the same gene set", True, "27 genes, 20/20 planted, Jaccard 0.93 with DEXSeq"),
    A("Null split and 3v3 behave", True, "ctrl 1-3 v 4-6: 2 gene calls (3 stageR-confirmed transcripts); 3v3 through the block: 25 genes, 20/20 planted")],
    exec_note="run/20_input2_manual_dtu.R, blocks/r_03.R executed verbatim; the preamble the block's comments ask for (meta, files, tx2gene) is mine.", regression_of="pre-fix input 2")

add(3, "Edge", "Real chrX 2 GBR v 2 YRI: SKILL block, shipped example (demo + real mode), count-route table and cause tests", "COMPLETED",
    "Block: 26 isoforms / 20 genes, RPL10 dIF -0.3291 q 4.6e-18; route table and cause tests reproduce; example runs end to end. Raw-route calls at n=2 are not validated: mixed-population splits call 11 and 15 genes",
    32, 46, [
    A("Skill block on real chrX 2v2 reproduces the stated result and dIF", True, "26 isoforms in 20 genes; RPL10 ENST00000406022 dIF -0.3291 vs hand computation -0.3356 (isoforms removed by preFilter change the denominator)"),
    A("The count-route table and the hedged cause statement reproduce", True, "raw 26/20, lengthScaledTPM 28/22, scaledTPM 0/0, dtuScaledTPM 0/0, ISAR default 0/0 (RPL10 q 1); raw x median(len)/len -> 0, same factors permuted -> 34, sqrt factor -> 17, gene totals restored -> 0: 'consistent with, not proven' is the right hedge"),
    A("Shipped example runs end to end from a copy on the demo data and on real chrX", True, "demo: 35 isoforms in 14 genes, 14/14 planted, 8/8 NMD = poison genes, DEMO OK twice; real chrX (metadata rows shuffled): 26/20, annotated ORFs 1281, consequences, RPL10 PDF; missing sample stops naming ERR204916"),
    A("Example fails safe on a metadata mismatch", True, "'sample IDs differ ... only in quant: ERR204916'"),
    A("Skill's n=2 and count-route guidance matches behaviour on label-permuted real data", False, "raw route on the two mixed-population 2v2 splits called 11 and 15 genes (true split 20); the Skill calls n=2 'underpowered' and presents raw counts as the route that works, without this null")],
    exec_note="run/30_input3_real_chrX.R, 35_example_runs.sh, 71_real_label_permutation.R, 72_efflen_factor.R; public-data rnasplice chrX (real).", regression_of="pre-fix input 3")

add(4, "Variant B", "Consequence block verbatim (ORFs, sequences, CPC2, hmmscan + converter, Pfam) on synthetic and real chrX", "COMPLETED",
    "Synthetic: NMD 10/10 (8/10 with removeNoncodinORFs=TRUE), Domain loss 10/10, converter rows column-identical; real chrX PTC flag v Ensembl NMD biotype sens 0.96 spec 1.00. SignalP/IUPred2A/DeepTMHMM not run",
    33, 49, [
    A("NMD_status flags the planted poison isoform B as NMD-sensitive and up in 10/10 poison genes; TRUE drops some", True, "10/10 with removeNoncodinORFs=FALSE, 0 calls outside poison genes; 8/10 with TRUE (2 poison B isoforms CPC2 noncoding) as the Skill states"),
    A("domains_identified calls 'Domain loss' A-down/C-up in 10/10 skip genes and stays quiet elsewhere", True, "10/10; 0 calls outside; PF00240 in 20 rows / 10 genes, never in an isoform C; intron_retention 0 calls (none planted)"),
    A("examples/hmmscan_to_pfamscan.py produces a file analyzePFAM accepts, with columns correct", True, "60/60 rows column-identical to an independent parse of the domtblout; raw domtblout rejected ('more columns than column names'); 264 real-chrX rows accepted; error paths (no args, missing file, non-domtblout, plain clans file) behave"),
    A("Documented consequence order and quoted error text hold", True, "extractSequence before ORFs on a no-CDS GTF: \"Please run the 'addORFfromGTF()' ...\"; missing SignalP: 'the result of the SignalP analysis must be advailable'; analyzeCPC2 without removeNoncodinORFs stops"),
    A("Real chrX NMD/ORF statements reproduce", True, "annotated-ORF PTC flag v Ensembl nonsense_mediated_decay biotype sens 0.96 (48/50) spec 1.00 (1023/1028); after analyzeORF('longest') over annotated ORFs sens 0.64 (32/50) spec 0.95 (Skill says 0.89): direction and sensitivity confirmed")],
    exec_note="run/40a-40d, 41, 63; CPC2 (as-cpc2) and hmmscan --cut_ga vs Pfam-A (as-annot) in WSL. NOT executed: SignalP, IUPred2A, NetSurfP-2, DeepTMHMM (licence/cloud; the Skill marks them 'not run').", regression_of="pre-fix input 4")

add(5, "Stress", "Batch-confounded synthetic set and adversarial inputs through the block (regression of pre-fix inputs 5 and 7)", "COMPLETED",
    "Batch column removes artefacts (11/30 -> 0/30, planted 20/20); confounded/constant/1v1/suffix/no-switch errors match the Skill's table; the block's own metadata check gives an opaque message",
    32, 47, [
    A("Ignoring batch produces artefact calls and the block's optional batch line removes them", True, "artefact genes called 11/30 -> 0/30; planted 20/20 both; 5 other null-gene calls appear with the batch column (0 without)"),
    A("Covariate and replicate errors match the Skill's Common Errors rows", True, "'not full rank' (batch == condition); 'Contain constant information' (constant batch); 'A statistical test cannot be performed without replicates' (1v1); 'No genes were considered switching' (default reduceToSwitchingGenes)"),
    A("Version-suffixed IDs fail as documented and the stated remedy works", True, "Jaccard < 0.925 error; ignoreAfterPeriod = TRUE in both calls imported 875 isoform rows"),
    A("A metadata/quantification mismatch in the Skill block gives an actionable message", False, "message is 'setequal(ids, meta$sample_id) is not TRUE' with no sample named; the shipped example's message names the IDs")],
    exec_note="run/50_input5_stress_adversarial.R; batch set rebuilt from the regression synthetic data (SYNTHETIC).", regression_of="pre-fix inputs 5 and 7")

add(6, "Scope Boundary", "fishpond/swish block verbatim (real Gibbs 2v2, synthetic 6v6), tximeta path, count-only long-read style import", "COMPLETED",
    "swish numbers reproduce exactly (391 tested, 6 q<0.05, top ENST00000380861 log2FC -1.45, median meanInfRV 0.69); synthetic 33/35 TP (all log2FC>0), FP 29/848; tximeta hedge accurate",
    34, 49, [
    A("Skill's swish block runs verbatim and its stated real-data numbers reproduce", True, "391 tested, 6 at q<0.05, top ENST00000380861 log2FC -1.45, median meanInfRV 0.69; block adds meanInfRV column"),
    A("infRV filter example and swish factor requirement work as documented", True, "y[mcols(y)$meanInfRV < 1, ] keeps 231 of 391; character condition -> 'is.factor(condition) is not TRUE'"),
    A("swish recovers planted DTE-up transcripts in the right direction with low FP (synthetic 6v6)", True, "33/35 called, 33/33 log2FC>0, FP 29/848 (3.4%)"),
    A("The Skill's hedge on the tximeta rowData path is accurate", True, "makeLinkedTxome succeeded; tximeta returned an SE with 0 rowData columns and the message 'couldn't find matching transcriptome' (warning 'Unknown or uninitialised column: sha256'); rowData(se)$gene_id not runnable here, as the Skill says"),
    A("Count-only importRdata (the Skill's long-read route) recovers the planted switches", True, "20/20, 2 null FP; importRdata has no long-read/single-cell argument, as the Skill states")],
    exec_note="run/60_input6_swish.R, 61_tximeta_warning.R; the synthetic 'inferential replicates' are Poisson resamples (SYNTHETIC); the tximeta rowData(se)$gene_id lines were NOT executed on real tximeta output.", regression_of="pre-fix input 6")

add(7, "Adversarial", "NEW: count-route mechanism on my own simulated set (isoforms 0.5-5.4 kb), satuRn across routes, real chrX label permutation, ISAR source and NEWS", "COMPLETED",
    "Every route recovers 20/20 on my synthetic sets, so simulation does not expose the problem; real chrX: satuRn 0 on either route; raw-route calls persist under label permutation (11 and 15 genes) while the default route gives 0 in every split",
    31, 45, [
    A("The Skill's manual-pipeline route numbers on real chrX reproduce", True, "DEXSeq 13 / 13 / 2 genes and DRIMSeq 11 / 11 / 7 for raw / lengthScaledTPM / scaledTPM; DEXSeq-DRIMSeq overlap 7 with raw counts"),
    A("The Skill's remark that a clean simulation will not reveal the count-route problem holds on data I generated", True, "5v5 DEXSeq and 4v7 satuRn, isoform lengths 0.5-5.4 kb (length factor 0.35-3.5): default, lengthScaledTPM, scaledTPM, dtuScaledTPM and emulated factors all 20/20 with 0/195 null FP"),
    A("The Skill's 'satuRn not compared across routes on real data' is an honest gap; what happens", True, "ISAR satuRn wrapper on real chrX 2v2: 0 switches with raw (RPL10 q 0.40) and with default counts (q 0.11)"),
    A("Version statements are consistent with the installed package", True, "2.6.0 exports only isoformSwitchTestDEXSeq/isoformSwitchTestSatuRn (each warns on replicate count); no long-read/single-cell argument in importRdata; NEWS shows importRdata now corrects IF for covariates (detectUnwantedEffects = TRUE)"),
    A("Raw-count route is presented with the right level of caution for n=2 real data", False, "label-permuted 2v2 splits: raw route 11 and 15 genes (true split 20, 1/20 shared), default route 0 genes in all three splits (min q = 1); the Skill's 'default lost every call, so use raw' has no null behind it")],
    exec_note="run/70_input7_new_count_route.R, 71_real_label_permutation.R, 62_isar_news.R, 64_isar_source_dump.R; data/new1 and data/new2 are SYNTHETIC (seeds 8801, 8802); real chrX from public-data.", new=True)

add(8, "Stress", "NEW: 4v7 unbalanced design with batch column, shuffled IDs, new genes and effect sizes; SKILL block and shipped example in real-data mode", "COMPLETED",
    "satuRn branch 20/20, 0/195 null FP; example (real-data mode) 38 isoforms in 20 genes = 20/20 planted, 0 others, NMD-sensitive up in 10/10 poison genes; null 3v4 split 4/250 genes",
    36, 52, [
    A("SKILL block (satuRn branch, 4v7, shuffled IDs and metadata rows) recovers the planted switches with correct direction and size", True, "20/20; dIF within 0.1 of truth 20/20; null FP 0/195; dge_only 0, small(0.04) 0; design joined by name correct"),
    A("The block's own batch line works and forcing DEXSeq gives the same picture", True, "with batch: 20/20 (19/20 within 0.1 of truth: covariate adjusts dIF, as the Skill warns); DEXSeq forced: 20/20. My batch effect (0.15 dIF diluted by imbalance) produced no artefacts without adjustment, so this did not test batch removal"),
    A("A null split stays within a normal false-positive rate", True, "3 v 4 split of the 7 treatment samples with batch column: 4 of 250 genes (1.6%)"),
    A("Shipped example in real-data mode recovers the planted set on a design it was not tuned on", True, "38 isoforms in 20 genes: 20/20 planted, 0 non-planted, batch column kept as covariate; ORFs predicted (no CDS in GTF); NMD_status 'NMD sensitive' up in 10/10 poison genes; PDF > 5 kB"),
    A("Shipped example demo is deterministic and self-checking", True, "run twice: identical '35 in 14 genes', 14/14 planted, 8/8 NMD genes, DEMO OK; ~65 s")],
    exec_note="run/04_gen_new.R (seed 8801, SYNTHETIC), 80_input8_new_unbalanced.R, 81_input8_example.sh, 82_eval_example_new.R, 35a_demo_rerun.log.", new=True)

n = len(inputs)
exec_avg = round(sum(i["total"] for i in inputs) / n, 1)
cats = {
    "functional_suitability": (10, 12, "Covers DTU/DTE/DGE framing, ISAR workflow, manual DRIMSeq/DEXSeq/stageR, swish, NMD and consequence annotation; every numeric claim checked reproduced except two small figures (post-analyzeORF specificity 0.89 v 0.95 measured; factor max 205 v 576). Attributes 'auto-selecting wrapper' to the 2025 preprint, whose abstract does not say so. Licence-gated annotators flagged unrun."),
    "reliability": (10, 12, "Common Errors table holds 14 real messages, all 14 re-triggered here and matching (one dmFilter message quoted without its first clause); hard stops and ID checks in block and example. The block's metadata check message names nothing; n=2 false-positive behaviour not warned."),
    "performance_context": (5, 8, "491 lines / 37 KB in one SKILL.md with no references/; workflow itself is linear and the example/converter carry the heavy logic."),
    "agent_usability": (14, 16, "Clear DGE/DTE/DTU table, ordered consequence steps, checkpoints with numbers to expect, error text to expect; the count-route section needs a re-read."),
    "human_usability": (6, 8, "Natural trigger language; strict validation is by design; the one weak point is the opaque stopifnot message in the block."),
    "security": (11, 12, "No credentials, no eval/exec, local R/Python only; example validates metadata and replicate counts; converter validates its input."),
    "maintainability": (10, 12, "SKILL + usage-guide + runnable example with self-assertions + converter; blocks extract cleanly and run verbatim; sections mix provenance ('audit:') into instructions."),
    "agent_specific": (16, 20, "Precise trigger; example and converter are true scripts; stop conditions (replicates, zero switches, missing annotators) present; no references/ split at 491 lines; n=2 caution missing."),
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
        "description": "Analyzes differential transcript usage (DTU) and isoform switches with functional consequence prediction (NMD via the 50 nt rule, ORF disruption, domain loss/gain, coding-potential shifts; signal peptide and IDR changes when licensed annotators are available) using IsoformSwitchAnalyzeR, the manual DRIMSeq-DEXSeq/satuRn-stageR pipeline and fishpond/swish.",
        "source": "mrsonord2240/bioSkills@306e225a1d72aaa5b70504efc068cce0b4743416:alternative-splicing/isoform-switching",
        "evaluated_on": "2026-09-20",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": n,
        "re_audit": True,
        "pre_fix_score": 66, "pre_fix_grade": "Beta Only",
        "new_inputs": [7, 8],
        "tool_versions": {"R": "4.4.3", "Bioconductor": "3.20", "IsoformSwitchAnalyzeR": "2.6.0", "DRIMSeq": "1.34.0", "DEXSeq": "1.52.0", "satuRn": "1.14.0", "stageR": "1.28.0", "fishpond": "2.12.0", "tximport": "1.34.0", "tximeta": "1.24.0", "Salmon quants": "2.7.0", "CPC2": "standalone (python 2.7, as-cpc2)", "HMMER": "3.4 + Pfam-A 2026-09"},
        "not_executed": ["SignalP (licence)", "IUPred2A (licence)", "NetSurfP-2 (registration)", "DeepTMHMM (cloud)", "tximeta rowData(se)$gene_id path on real tximeta output (linkedTxome does not match the Salmon 2.7.0 index; the Skill says so)", "IsoformSwitchAnalyzeR releases newer than 2.6.0 (not installable in Bioc 3.20)"],
        "data": "SYNTHETIC planted-truth sets in run/data (synth seed 20260920, new1 seed 8801 4v7, new2 seed 8802 5v5) plus real nf-core rnasplice chrX GBR v YRI 2 v 2 (Salmon quants, Gibbs samples, BAM-derived GTF/FASTA) from audit-envs public-data."
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "Numbers quoted in the Skill (26/20, 28/22, 0/0 route table; 13/13/2 and 11/11/7; 391/6; 0.96/1.00 NMD flag; 8/10 v 10/10) reproduced; two small figures differ (specificity 0.95 v 0.89, factor max 576 v 205 by effective length). Citations checked against Crossref/bioRxiv where possible; the preprint attribution is unverifiable from its abstract (P2)."},
            "practice_boundaries": {"result": "PASS", "detail": "Research analysis only; no diagnosis or treatment advice; the SCN1A ASO is stated as 'in clinical development, phase not verified'."},
            "methodological_ground": {"result": "PASS", "detail": "No principled error: DTU separated from DGE/DTE, stageR two-stage, compositional null, replicate/covariate handling stated; n=2 caution is under-stated (P1) but not a fallacy."},
            "code_usability": {"result": "PASS", "detail": "All Skill blocks, the example (demo and real mode) and the converter executed from copies with checked output; every R block ran verbatim. Only licence-gated annotator calls were not run and are labelled so."}
        }
    },
    "static_score": {"subtotal": static, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": exec_avg, "max": 100, "assertion_pass_rate": {"passed": assert_pass, "total": assert_tot}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
    "key_strengths": [
        "Every documented R block runs verbatim and every number the Skill quotes that I re-derived reproduced (route table 26/28/0/0, manual pipeline 13/13/2 and 11/11/7, swish 391/6, NMD flag sens 0.96), on synthetic sets with planted truth and on real chrX",
        "Name-keyed design fixes the pre-fix silent-mislabel hazard: 20/20 with shuffled SRR IDs and shuffled metadata rows on 3v3, 6v6 and my own 4v7 set (positional vector gave 0/20)",
        "Shipped example is now a real regression test: demo self-asserts (14/14 planted, 8/8 NMD) and reproduced twice; real-data mode recovered 20/20 planted on a design it was not tuned on",
        "hmmscan_to_pfamscan.py is column-exact against the domtblout (60/60 rows) and accepted by analyzePFAM on synthetic and real chrX",
        "Hedging is mostly honest: cause of the count-route gap stated 'consistent with, not proven' (my ordered-vs-permuted and dose-response tests agree), tximeta rowData failure and licence-gated tools labelled not run"],
    "recommendations": [
        {"priority": "P1", "title": "Raw-count route and n=2 presented without a null", "observed_in": [3, 7],
         "problem": "On real chrX 2v2, the two mixed-population label splits called 11 and 15 genes with the raw route (true split 20; 1 of 20 shared), while the default route gave 0 in every split. The Skill says the default 'lost every call' so raw is used, and calls n=2 only 'underpowered'.",
         "root_cause": "The 26-v-0 comparison has no permutation baseline, so it cannot say which route is right, and n=2 individual-level variation is not mentioned.",
         "fix": "Add the label-permutation result to the Count route section, say n=2 calls are exploratory and can be anti-conservative, and recommend a label-shuffle sanity run and >=3 replicates before trusting either route."},
        {"priority": "P2", "title": "Block's sample-ID check is opaque", "observed_in": [5],
         "problem": "A metadata row missing from the quantification stops with 'setequal(ids, meta$sample_id) is not TRUE' and names no sample; the shipped example names them.",
         "root_cause": "The SKILL.md block uses bare stopifnot() while the example carries the informative check.", "fix": "Reuse the example's stop() message (only in quant / only in metadata) in the block."},
        {"priority": "P2", "title": "Preprint attribution and covariate mechanism", "observed_in": [7, 8],
         "problem": "The Skill says the 2025 preprint 'describes an auto-selecting DTU wrapper and long-read/single-cell modes'; the bioRxiv abstract says only that the standard workflow suits long-read and single-cell data. The covariate-adjusted dIF is 'not traced', but installed NEWS and formals show importRdata(detectUnwantedEffects = TRUE) and covariate correction of IF.",
         "root_cause": "Claims about a source and a package mechanism were written without checking either.", "fix": "Cite the abstract's actual wording, and replace 'not traced in the source' with the NEWS statement and the detectUnwantedEffects argument."},
        {"priority": "P2", "title": "Small numeric mismatches and provenance text inside the Skill", "observed_in": [3, 4],
         "problem": "Specificity after analyzeORF('longest') is 0.95 here (Skill 0.89); the factor range 0.019-205 is 0.019-576 with EffectiveLength (0.023-18 with Length); the dmFilter message is quoted without its 'min_samps_gene_expr >= 0 &&' clause; the Skill quotes 'the audit' inside instructions.",
         "root_cause": "Numbers copied from one run and provenance left in the prose.", "fix": "Correct or drop the figures, name which length was used, and move 'audit' wording out of SKILL.md."},
        {"priority": "P2", "title": "SKILL.md is 491 lines in one file", "observed_in": [],
         "problem": "The Skill loads about 9-10k tokens whole; the count-route table, consequence order and Common Errors could load on demand.",
         "root_cause": "No references/ layer; the fix chose deduplication over a split.", "fix": "Move Count route, Functional Consequence Annotation details and Common Errors into references/ and keep a pointer in SKILL.md."},
        {"priority": "P2", "title": "Licence-gated annotators still unrun", "observed_in": [4],
         "problem": "signal_peptide_identified, IDR_identified/IDR_type and isoform_topology were not exercised (SignalP, IUPred2A, NetSurfP-2, DeepTMHMM); the Skill labels them 'not run' or 'read from source'.",
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
