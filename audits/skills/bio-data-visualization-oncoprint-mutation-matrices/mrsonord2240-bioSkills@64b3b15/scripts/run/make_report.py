import json
SK = "bio-data-visualization-oncoprint-mutation-matrices"
OUT = r"F:\OpenScience\audits\%s" % SK

def A(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}
def I(index, typ, label, note, basic, spec, assertions, status="COMPLETED", executed=True, exec_note=""):
    total = basic + spec
    p = sum(1 for a in assertions if a["result"] == "PASS")
    flag = "\u2705" if status == "COMPLETED" and total >= 75 else ("\u26a0\ufe0f" if status == "COMPLETED" else "\u274c")
    return {"index": index, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note, "basic": basic, "specialized": spec,
            "total": total, "assertions_passed": p, "assertions_total": len(assertions), "assertions": assertions, "executed": executed, "execution_note": exec_note}

inputs = [
 I(1, "Canonical", "ComplexHeatmap oncoPrint of the top 20 genes of real TCGA-LAML (193 samples), FAB + vital-status tracks",
   "Skill block run with data adapted; drawn cells decoded from SVG equal the matrix (0/3860 mismatches), colours, 193 columns, 192/192 annotation strips correct; but row order is by alteration events, not by the mutated-sample percentages printed beside it.",
   32, 48, [
    A("Every drawn cell (colour rectangles decoded from the SVG, in drawn row/column order) equals an independent gene x sample matrix built from the MAF", True, "0 of 3860 cells differ; class totals Missense 225 / Truncating 96 / Splice 22 identical in matrix and drawing; 20 multi-class cells drawn stacked"),
    A("Variant-class to colour mapping is right (Missense #56B4E9, Truncating #000000, Splice #CC79A7)", True, "Decoded rect fills map back to the expected class for every cell"),
    A("All 193 cohort samples are drawn (remove_empty_columns = FALSE) and % labels equal independent n/193", True, "193 columns; labels 25% 27% 17% ... 3% equal round(n/193*100) for all 20 rows"),
    A("Annotation track colours map to the right samples", True, "FAB strip 0 mismatches over 192 coloured columns; the one sample with NA FAB (TCGA-AB-2941) is grey"),
    A("Gene order follows descending mutated-sample frequency as the decision table says ('Gene frequency (default)')", False, "DNMT3A (48 samples, 25%) is drawn above FLT3 (52, 27%); 9 of 20 rows are out of sample-frequency order. oncoPrint ranks by summed alteration types (drawn order == descending event count, verified)")],
   exec_note="Executed. run/i1_complexheatmap_laml.R, i1b_memosort.R; ComplexHeatmap 2.22.0; figure opened (non-blank, out/i1.png)."),
 I(2, "Variant A", "maftools::oncoplot(top=20) with clinical features and sortByAnnotation on TCGA-LAML",
   "Gene order, percentages and per-class colours match an independent count (20/20 gene rows); the Skill's call as written fails (clinicalData needs Tumor_Sample_Barcode, numeric feature needs a palette) and its partial annotationColor greys out the other groups.",
   30, 46, [
    A("Gene order equals descending count of mutated samples from the raw MAF", True, "FLT3 DNMT3A NPM1 IDH2 IDH1 TET2 ... TTN identical; gene percentages 27% 25% 17% ... equal independent n/193"),
    A("Drawn colour counts per gene equal independent per-class and Multi_Hit counts", True, "20/20 rows (19 exact, TTN row only confounded by the annotation strip below it; its own tiles match); 30 multi-hit gene-sample pairs shown as black Multi_Hit"),
    A("Non-mutated samples kept (removeNonMutated = FALSE) so the denominator is the cohort", True, "Title 'Altered in 159 (82.38%) of 193 samples'; 193 columns"),
    A("The maftools example call runs as written in SKILL.md", False, "clinicalData must contain a Tumor_Sample_Barcode column (the Skill's clinical does not); a numeric feature without a palette raises 'numeric annotation color for NA must be a sequential color palette'; annotationColor with 2 of 3 subtypes silently draws the rest grey and unlabeled")],
   exec_note="Executed. run/i2_maftools_oncoplot.R, i2c_verify_colours.R; maftools 2.22.0; figures opened (out/i2.png, i2b.png)."),
 I(3, "Edge", "Synthetic 30-sample cohort: multi-class cell, two hits of the same class, CNV+SNV cell, empty gene, zero-mutation samples, one sample, all-empty",
   "ComplexHeatmap stacking and collapsing are exact and the cohort denominator holds; maftools silently drops the 14 samples without a mutation (denominator 16, not 30) even with removeNonMutated = FALSE and clinicalData for all 30.",
   30, 46, [
    A("Stacked cells (Missense;Truncating, Amp;Missense) and a double same-class hit are drawn as planted", True, "0 of 180 cells differ from the planted truth; S02 TP53 two Missense hits collapses to one Missense rectangle"),
    A("Empty gene row is kept at 0% and zero-mutation samples are kept with cohort denominator 30", True, "EMPTYG row present at 0%; 30 columns; TP53 27% = 8/30; remove_empty_rows = TRUE drops only EMPTYG"),
    A("Single-sample matrix draws correctly", True, "1 column; TP53 stack Missense+Truncating, KRAS Missense, MYC Amp; PIK3CA/RB1/EMPTYG 0%"),
    A("maftools with removeNonMutated = FALSE preserves the cohort N (30) when clinicalData lists all 30 samples", False, "maftools reports 16 samples; getClinicalData has 16 rows; percentages 50/38/19/12 are of 16. Samples absent from the MAF cannot be restored"),
    A("Percent labels differ between remove_empty_columns TRUE and FALSE, as the Reconciliation table says", False, "ComplexHeatmap labels identical (27% 20% 10% 7% 7% 0%) with 13 or 30 columns; maftools identical too; the documented denominator effect does not exist")],
   exec_note="Executed. run/gen_synth_edge.R, i3_edge.R (SYNTHETIC data with planted truth). An all-empty matrix errors with 'subscript out of bounds' (ComplexHeatmap, unhelpful message)."),
 I(4, "Variant B", "comut.py co-mutation plot from TCGA-LAML long-format data (Skill Python block)",
   "The Skill block does not run verbatim: comut.CoMut is not exposed by 'import comut'; after adapting, the first dataset must hold every sample; pandas 3 breaks add_continuous_data. With fixes cells match (0/1930) but the top gene is drawn at the bottom and samples are unsorted.",
   24, 34, [
    A("The Skill's comut code block runs as written", False, "AttributeError: module 'comut' has no attribute 'CoMut' (comut 0.0.3; correct is from comut import comut); with that fixed, ValueError 'Unknown samples' because clinical/TMB samples are not in the mutation frame (zero-mutation samples); pandas 3.0.6: TypeError LossySetitemError in add_continuous_data (pandas 2.3.3 only warns)"),
    A("After adaptation every cell equals an independent groupby (single class = colour, two classes = two triangles)", True, "0 of 1930 cells mismatched; 20 two-class triangle cells; no 3+ class cells in this data"),
    A("Annotation track maps to the right samples", True, "Subtype 0 mismatches for annotated samples; sample without annotation left white"),
    A("Top-frequency gene is drawn at the top and samples ordered by burden as the description promises", False, "category_order=top_genes puts FLT3 at the bottom (y tick order bottom-to-top); samples are in first-seen/list order, unsorted, no staircase"),
    A("TMB colour scale is valid for the data", False, "value_range=(0,30) hard-coded; max TMB 34 saturates; comut normalises as (x-min)/max, so any range with min>0 is mis-scaled (10,20,30 over (10,30) -> 0, .33, .67)")],
   exec_note="Executed in main venv (pandas 3.0.6) and venv-pd2 (pandas 2.3.3): run/i4_comut.py, outputs out/i4_pd3.log, i4_pd2.log. Verbatim block failed in both (with the import shim)."),
 I(5, "Stress", "Synthetic 600-sample cohort (subtypes, 3 hypermutators to 3000 mutations, multi-hit TP53): shipped example script + column_split + log10 TMB",
   "Shipped example runs once mat/clinical are defined; log10 TMB bars are exact (r = 1.0, tallest/median 2.6 vs 143 linear) and split panels are right; clinical order not matching mat columns silently mislabels 391/600 samples and the Skill never warns.",
   33, 47, [
    A("examples/oncoprint_phd.R runs from a clean copy once mat, clinical and cohort.maf exist", True, "oncoprint.pdf 41 KB written; somaticInteractions returns 190 pairs; script leaves mat, clinical and cohort.maf undefined (comments only)"),
    A("TMB bar height is proportional to log10(true TMB + 1) per column and hypermutators do not dominate", True, "600 bars; cor(height, log10(TMB+1)) = 1.0000; tallest/median = 2.59 (log expectation 2.59; linear would be 143)"),
    A("column_split by subtype puts each sample in the panel of its true subtype", True, "Basal 180 / HER2 120 / Luminal 300; every column matches; annotation 0/600 mismatches; cells 0/7200 mismatches"),
    A("Annotation tracks map to the right samples even when the clinical table is in MAF order and the matrix columns are sorted", False, "391 of 600 subtype strips wrong, no error or warning: HeatmapAnnotation is positional and the Skill never says to reorder clinical by colnames(mat)"),
    A("Per-panel gene frequency right bar as the usage guide promises for split layouts", False, "One cohort-wide right bar and cohort-wide % (39% TP53), no per-panel frequencies"),
    A("The Skill's step 6 read.maf(clinicalData = clinical) works with the clinical data frame defined in the Skill", False, "Error: Tumor_Sample_Barcode column not found in provided clinical data (works after adding it)")],
   exec_note="Executed. run/gen_synth_cohort.R, i5_stress.R, i5b_tmb.R, ex_run.R (SYNTHETIC cohort, seed 7); figures opened (out/i5_C_split.png)."),
 I(6, "Scope Boundary", "Mutual exclusivity / co-occurrence: somaticInteractions on LAML, on a planted N=600 cohort and on an N=20 subset, plus small-cohort CI recipe",
   "All 263 pairwise Fisher results equal an independent scipy computation; planted pairs are recovered at N=600 and correctly non-significant at N=20; the documented return value is wrong.",
   34, 50, [
    A("somaticInteractions p-values and 2x2 counts equal an independent two-sided Fisher computed from the raw MAF", True, "LAML 190/190 pairs (N=193), synthetic N=600 45/45, N=20 28/28; max relative p difference 2.6e-13; direction agrees for all p<0.05"),
    A("Planted co-occurrence (TP53-MYC) and mutual exclusivity (BRAF-NRAS) are detected at N=600", True, "TP53-MYC p=7.6e-46 OR=23.7 Co_Occurence; BRAF-NRAS p=3.1e-06 OR=0, 0 of 166 co-mutated"),
    A("At N=20 the same pairs are not significant, supporting the Skill's small-cohort warning", True, "TP53-MYC p=0.141 (adj 0.75); BRAF-NRAS p=1.0; KRAS-EGFR p=1.0"),
    A("Clopper-Pearson intervals from binom.test agree with an independent exact method", True, "max |R - scipy exact| 3e-16 over 8 genes"),
    A("somaticInteractions returns 'a matrix of -log10(p) with sign by direction' as the Skill states", False, "Returns a 12-column data.table (gene1, gene2, pValue, oddsRatio, 00/01/11/10, pAdj, Event, pair, event_ratio); the signed -log10 matrix exists only in the plot")],
   exec_note="Executed. run/i6_somatic_interactions.R, i6_verify_fisher.py. Haldane-Anscombe OR for BRAF/NRAS (0/2/1/17) is 2.33 (>1) although zero co-occurrences were observed: the recommended correction reverses the apparent direction at these counts (P2)."),
 I(7, "Adversarial", "MAF barcodes differ from clinical barcodes; MAF classes outside the six Skill classes; request to drop non-mutated samples so frequencies look higher",
   "Unmapped alteration strings fail loudly, but ID mismatch produces an all-NA annotation with no warning in both tools, the Skill gives no Variant_Classification mapping, and its claim that dropping empty columns changes the percentages is false.",
   28, 42, [
    A("An alteration string with no alter_fun/col entry fails loudly", True, "'You should define graphic function for: Silent' (and for a case mismatch 'missense')"),
    A("A clinical/MAF sample-ID mismatch is reported", False, "oncoPrint draws an all-grey annotation with no warning; read.maf(clinicalData = non-matching IDs) returns 0 clinical rows with no warning"),
    A("The Skill maps MAF Variant_Classification values to its alteration classes", False, "SKILL.md/usage guide only say 'map per-row Variant_Classification to alteration class'; 5 of the 12 LAML classes (Silent, Intron, RNA, IGR, 5'Flank) plus In_Frame_* and Nonstop have no stated rule"),
    A("Dropping empty columns changes the percentage denominator as the Skill states, so the request would inflate frequencies", False, "remove_empty_columns TRUE: 126 columns but labels unchanged (25% 27% 17% ...); an altered-only denominator would give 41% 38% 26%; the Skill's denominator warning describes behaviour that does not occur")],
   exec_note="Executed. run/i7_adversarial.R on TCGA-LAML. No scope or safety problem arises; the Skill correctly advises keeping all samples.")
]

exe = round(sum(i["total"] for i in inputs) / len(inputs), 1)
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)
static = {"functional_suitability": (9, 12, "Completeness 3, correctness 2, appropriateness 4. Central pieces are only comments (MAF to matrix pivot, Variant_Classification map, CNV merge, TMB definition). Several stated behaviours are wrong: % labels change with remove_empty_columns, somaticInteractions returns a signed matrix, default gene order is by frequency, comut example imports."),
          "reliability": (7, 12, "Fault tolerance 2, error reporting 3, recoverability 2. Silent failure modes an agent will hit: clinical order not aligned to matrix columns (391/600 wrong strips), ID mismatch gives all-NA annotation, maftools drops samples absent from the MAF; no guard or check is described. The Common Errors table is useful but misses these."),
          "performance_context": (6, 8, "SKILL.md about 240 lines with no references layer; usage-guide adds a second copy of several tips; example repeats the alter_fun block verbatim."),
          "agent_usability": (10, 16, "Learnability 3, consistency 2, feedback 3, error prevention 2. Clear Goal/Approach and decision table, but usage-guide prompt colours/heights (green Missense, quarter-height Truncating) contradict SKILL.md (#56B4E9, 0.33), and the 'sort by gene 1' failure mode contradicts its own fix line."),
          "human_usability": (5, 8, "Discoverability 3, forgiveness 2. Example prompts are natural; numeric errors from maftools/comut surface with no Skill-side hint."),
          "security": (11, 12, "No credentials, network, eval or shell. Example writes oncoprint.pdf and reads cohort.maf in cwd."),
          "maintainability": (8, 12, "Version-stamped and cited (Cerami 2012, Canisius 2016, Gu 2016, Mayakonda 2018 are correct references), but the example cannot run without objects the reader must invent and nothing is testable as shipped; comut instructions drifted from the package API."),
          "agent_specific": (15, 20, "Trigger precise; all six related Skills exist; safe re-runs; escape hatch for AttributeError present in the version block; no references/ layer and no MAF loader helper.")}
sub = sum(v[0] for v in static.values())
sw = round(sub * 0.4, 1); dw = round(exe * 0.6, 1); score = round(sw + dw)
report = {
 "meta": {"skill_name": SK,
  "description": "Build OncoPrint and co-mutation matrix plots from somatic-variant cohorts using ComplexHeatmap, maftools, and comut.py with alteration-type stacking, sample ordering by mutational burden, mutual-exclusivity overlays, and clinical annotation tracks.",
  "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Complex", "n_inputs": 7,
  "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/oncoprint-mutation-matrices",
  "audit_type": "first audit (staging copy, unmodified upstream GPTomics/bioSkills)",
  "executed": True,
  "execution_note": "Executed 7/7 inputs. R 4.4.3 via r.sh (ComplexHeatmap 2.22.0, maftools 2.22.0, circlize 0.4.18, svglite for content extraction), Python 3.12 (main venv pandas 3.0.6 and venv-pd2 pandas 2.3.3; comut 0.0.3, scipy). Figures were verified by decoding drawn rectangles/labels from SVG output and compared with independent counts (pandas/scipy/base R); PNGs opened with the Read tool. SKILL.md code blocks: ComplexHeatmap, maftools and somaticInteractions blocks ran after supplying the undefined objects; the comut block fails verbatim. Shipped example oncoprint_phd.R ran from a copy. Data: real TCGA-LAML (maftools extdata) plus SYNTHETIC cohorts with planted truth (run/data). No __pycache__ written in the staging clone."},
 "veto_gates": {"skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated statistics or references; the four citations and numbers checked are correct. Documentation claims that do not match tool behaviour are recorded as P1 defects, not fabrication."},
   "practice_boundaries": {"result": "PASS", "detail": "Research visualisation of cohort mutation data; no diagnostic or prescriptive content."},
   "methodological_ground": {"result": "PASS", "detail": "The small-cohort warnings, Fisher/DISCOVER caveat and log-TMB advice are sound and were confirmed (N=20 pairs non-significant; log TMB bars tame 143x hypermutators). The Haldane-Anscombe suggestion inverts the apparent direction for a zero co-occurrence cell (P2), not a principled fallacy."},
   "code_usability": {"result": "PASS", "detail": "ComplexHeatmap, maftools and somaticInteractions blocks and the shipped example run once the data objects the Skill leaves undefined are supplied. The comut block does not run verbatim (wrong import path, first-dataset sample precondition, pandas 3 TypeError) but the version section tells the agent to introspect and adapt on AttributeError/TypeError; recorded as P1, not a veto."}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": m, "note": v[2]} for (k, v), m in zip(static.items(), [12, 12, 8, 16, 8, 12, 12, 20])}},
 "dynamic_score": {"execution_avg": exe, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at}, "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "\u26a0\ufe0f", "deployable": False, "veto_override": False},
 "key_strengths": [
  "Core rendering claims hold: ComplexHeatmap stacking, class colours and cohort denominator matched an independent matrix cell for cell (0/3860 and 0/7200 mismatches); maftools gene order, percentages and colours matched raw-MAF counts.",
  "Statistics advice is sound: somaticInteractions equals an independent Fisher on 263 pairs, planted co-occurrence and mutual exclusivity are recovered at N=600 and correctly not significant at N=20.",
  "log10 TMB recipe is exact (bar heights correlate 1.000 with log10(TMB+1)) and tames a 143x hypermutator spread.",
  "Correct citations, all related Skills exist, no security surface."],
 "recommendations": [
  {"priority": "P1", "title": "comut block cannot run as written", "observed_in": [4],
   "problem": "import comut then comut.CoMut() raises AttributeError (class lives in comut.comut); later datasets must have samples inside the first dataset's set, so zero-mutation and unannotated samples raise ValueError; add_continuous_data raises TypeError on pandas 3; category_order draws the top gene at the bottom; no sample sorting; TMB range (0,30) saturates.",
   "root_cause": "Python equivalent was written from memory of the API and never executed.",
   "fix": "Use from comut import comut, set toy_comut.samples to the full cohort first, reverse category_order, pre-sort samples by burden, note pandas<3, derive value_range from the data."},
  {"priority": "P1", "title": "Denominator claims contradict tool behaviour", "observed_in": [3, 7],
   "problem": "The Skill says percentages differ with remove_empty_columns and that removeNonMutated = FALSE preserves cohort N. ComplexHeatmap % is always over the input matrix; maftools drops samples that are absent from the MAF (16 of 30) regardless of the flag and of clinicalData.",
   "root_cause": "Behaviour asserted without running it.",
   "fix": "State the true denominators, and tell the agent to build the matrix from the explicit cohort sample list (or add zero-mutation samples to the MAF/clinical merge) before plotting."},
  {"priority": "P1", "title": "Matrix and annotation construction left as comments", "observed_in": [1, 5, 7],
   "problem": "mat, clinical and the Variant_Classification-to-class map are undefined; clinical rows not ordered like colnames(mat) silently mislabel samples (391/600 wrong), non-matching IDs give an all-NA track with no warning, and the maftools example needs a Tumor_Sample_Barcode column.",
   "root_cause": "The hardest correctness step is the one the Skill does not show.",
   "fix": "Ship a short verified MAF-to-matrix function with the class map, and require clinical <- clinical[match(colnames(mat), clinical$Tumor_Sample_Barcode), ] plus a stopifnot on NA matches."},
  {"priority": "P1", "title": "Row order is not sample frequency; somaticInteractions return misdescribed", "observed_in": [1, 6],
   "problem": "oncoPrint ranks genes by alteration events, so a gene with fewer mutated samples can sit above one with more (DNMT3A 25% above FLT3 27%). somaticInteractions returns a data.table, not a signed -log10 matrix.",
   "root_cause": "Both descriptions were written from the plot appearance.",
   "fix": "Say the default order counts alteration types and pass row_order = order(-rowSums(mat != '')) when sample frequency is wanted; document the data.table columns (pValue, oddsRatio, Event, pAdj)."},
  {"priority": "P2", "title": "usage-guide and SKILL.md disagree; smaller gaps", "observed_in": [3, 5, 6],
   "problem": "Usage-guide prompt gives green Missense and quarter-height Truncating versus SKILL.md; the 'sort by gene 1' failure mode contradicts its own fix; per-panel right bar and 'rasterize the cell layer' / 'side annotation' have no code and are not what oncoPrint does; Haldane-Anscombe OR flips to >1 for a 0-cell mutex pair; an all-empty matrix errors with 'subscript out of bounds'; maftools Multi_Hit black clashes with the Skill's black Truncating; partial annotationColor greys unlisted groups.",
   "root_cause": "Two documents maintained separately.",
   "fix": "Align the two files, delete or implement the unsupported claims, and add one line per gotcha."}]
}
json.dump(report, open(OUT + r"\eval_report_%s_result.json" % SK, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("static", sub, "exec", exe, "final", score, "assertions", ap, "/", at)
