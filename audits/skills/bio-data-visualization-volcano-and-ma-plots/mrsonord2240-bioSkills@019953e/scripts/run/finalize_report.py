# Builds eval_report_..._result.json and validates the schema arithmetic. Run: py.sh finalize_report.py
import json, pathlib
A = pathlib.Path(r"F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots")
SID = "bio-data-visualization-volcano-and-ma-plots"


def a(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}


def inp(i, typ, label, note, basic, spec, asr, exec_note, status="COMPLETED"):
    tot = basic + spec
    p = sum(x["result"] == "PASS" for x in asr)
    flag = "\u2705" if (status == "COMPLETED" and tot >= 75) else "\u26a0\ufe0f"
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note, "basic": basic,
            "specialized": spec, "total": tot, "assertions_passed": p, "assertions_total": len(asr), "assertions": asr,
            "executed": True, "execution_note": exec_note}


inputs = [
    inp(1, "Canonical", "ggplot2 + ggrepel volcano (SKILL block 02, verbatim) on real airway dex vs untrt, apeglm-shrunken",
        "33,469 genes, 450 Up / 365 Down; counts, x/y values, vlines and labels match the table. Labels are the right biology (ZBTB16, DUSP1, KLF15, PER1, SPARCL1, VCAM1). But the drawn hline is on the raw-p axis: 1,684 genes that are not FDR-significant (1,596 with padj>=0.05, 88 with NA padj) sit above it, because padj<0.05 really starts at -log10 p = 1.95.",
        33, 48,
        [a("Plotted Up/Down/NS counts equal an independent recompute from the DESeq2 table (450/365/32,654) and the point count equals the non-NA-pvalue rows (33,469)", True, "ggplot_build layer data vs res"),
         a("x is the shrunken LFC and y is -log10(pvalue): x range and max y equal the table's range and -log10(min p)", True, "asserted on layer data"),
         a("Default top-10 labels are biologically sensible and free of housekeeping genes", True, "SAMHD1 ZBTB16 DUSP1 SPARCL1 VCAM1 KLF15 CACNB2 PER1 MAOA GPX3 (mapped from Ensembl); no GAPDH/ACTB/B2M"),
         a("User-supplied symbols (DUSP1, KLF15, PER1, TSC22D3, FKBP5, TP53) are all labelled after mapping rownames to symbols", True, "PNG opened; TP53 labelled although |LFC|=0.40"),
         a("The dashed horizontal threshold line separates colored (padj-significant) from grey points, as the Skill's own 'raw p threshold line on adjusted axis' rule requires", False, "hline at 1.301 (raw p 0.05); 1,684 not-FDR-significant genes (1,596 padj>=0.05 + 88 NA) lie above it, the largest at y=1.95; the padj<0.05 boundary is 1.95 (i1b_line_recount.R)")],
        "Executed: run/i0_prep_airway.R (DESeq2 1.46.0 fit + apeglm/ashr/normal), run/i1_ggplot_volcano.R; two PNGs opened with Read. Ensembl-to-symbol mapping with org.Hs.eg.db added by the auditor (the Skill is silent on IDs)."),
    inp(2, "Variant A", "EnhancedVolcano block (SKILL block 03, verbatim) plus the Skill's EnhancedVolcano and shrinkage-method claims",
        "Block runs and draws; NA padj rows are dropped exactly as stated (14,905 of 22,392 drawn); y = padj puts the line at 1.301 on the padj axis. Two documented claims do not reproduce: 'selectLab is filtered by pCutoff/FCcutoff' (GAPDH padj 0.43 and TP53 |LFC| 0.40 are labelled; EnhancedVolcano 1.24 source has no such filter) and 'ashr also returns svalue' (not without svalue=TRUE, which then drops pvalue/padj).",
        31, 47,
        [a("Block 03 runs verbatim, returns a ggplot, draws non-blank, and draws exactly the non-NA-padj rows (14,905) as the Skill says NA padj is dropped", True, "layer 1 has 22,392 rows, 14,905 non-NA y; PNG opened"),
         a("Threshold lines sit at -log10(0.05) = 1.301 on the padj axis with y = 'padj', and no colored point lies below it", True, "min y colored: 1.30 (p-value class), 1.39 (both)"),
         a("Requested selectLab genes (TP53, MYC, BRCA1) are labelled", True, "all three drawn; PNG opened"),
         a("Gotcha 1 / failure mode / Common Errors claim reproduces: a selectLab gene failing pCutoff/FCcutoff is silently unlabelled", False, "GAPDH (padj 0.43, LFC -0.14), ACTB and TP53 (|LFC| 0.40) all labelled in layer data and in the PNG; source uses which(lab %in% selectLab) only. What really vanishes is an NA-padj gene (no y)"),
         a("Code comment 'ashr also returns svalue column' holds for the shown call lfcShrink(..., type = 'ashr')", False, "columns are baseMean,log2FoldChange,lfcSE,pvalue,padj; svalue appears only with svalue=TRUE, which removes pvalue/padj")],
        "Executed: run/i2_enhancedvolcano.R, i2b_ev_followup.R, i2c_selectlab_matrix.R, i2d_ashr_svalue.R; three PNGs opened. EnhancedVolcano 1.24.0 with ggplot2 4.0.3 (size/linewidth deprecation warnings come from the package)."),
    inp(3, "Variant B", "MA plots: DESeq2 plotMA (block 04) and the Python ma_plot (block 05), raw MLE vs shrunken fan diagnostic",
        "Both blocks run verbatim. plotMA draws the 5 |LFC|>5 genes as edge triangles (not dropped); the Python function draws 3,993 significant + 29,476 grey = 33,469 points with x = log10 baseMean and y = the table LFC. The fan diagnostic reproduces (baseMean<5: max |LFC| 5.19 raw vs 2.91 apeglm). Hard-coded '(shrunken)' y label would mislabel a raw table; the '5 MB+ PDF' claim does not hold (0.50 MB for 33k points).",
        35, 53,
        [a("plotMA(res_apeglm, alpha = 0.05, ylim = c(-5, 5)) renders and keeps out-of-range genes as edge markers", True, "PNG opened: 5 open triangles at y = 5, matches 5 genes with |LFC|>5"),
         a("ma_plot draws every gene once: significant layer = padj<0.05 count and the two layers total the table", True, "3,993 + 29,476 = 33,469"),
         a("Plotted x equals log10(baseMean) and y equals the shrunken log2FoldChange of the input table", True, "sorted-value equality, np.isclose"),
         a("The fan diagnostic reproduces: low-count extreme LFC in the raw MLE is removed by shrinkage while well-estimated genes are untouched", True, "baseMean<5 max|LFC| 5.19 -> 2.91; baseMean>=1000 median |LFC| 0.1815 -> 0.1655; side-by-side PNG opened"),
         a("'Vector scatter of >5000 points creates 5MB+ PDFs' holds", False, "measured 498 KB unrasterized vs 33 KB rasterized for 33,469 points in matplotlib 3.11")],
        "Executed: run/i3a_ma_R.R, run/i3b_ma_python.py (pandas 3.0.6, numpy 2.5.3, matplotlib 3.11.2); PNGs and PDFs measured and opened."),
    inp(4, "Stress", "Shipped examples/volcano_phd.R run verbatim (Ensembl and symbol rownames) plus synthetic extreme p (1e-200 and exactly 0)",
        "The example runs end to end and writes volcano.pdf and ma_plot.pdf (TrueType embedded, no Type 3). With the shipped y_cap = 50 applied unconditionally, 49 significant genes (the top hits, 135 max) fall outside the panel and 9 of 13 labels collapse into an unreadable overprint at the top edge (PDF opened). The usage-guide claim that capped points stay visible at the edge is false for coord_cartesian. The same hline/padj mismatch (line 1.30, boundary 1.91-1.95) is admitted in the example's own comment.",
        29, 43,
        [a("volcano_phd.R runs verbatim to completion given a dds with coef condition_treated_vs_control, writing both PDFs", True, "1.07 MB / 1.10 MB (Ensembl), 0.77 MB / 0.78 MB (symbols); no error"),
         a("cairo_pdf output embeds TrueType fonts (journal requirement stated in the Skill) with no Type 3 fonts", True, "/TrueType 3 and 2, /Type3 0 in every PDF"),
         a("Extreme p (1e-200 and an underflowed p = 0 on a synthetic 20,000-gene table) does not crash volcano_plot(); the Inf point is drawn at the top edge and labelled", True, "SYNTHETIC data seed 20260920; g955 (p=0) drawn at the edge; PNG opened"),
         a("With the shipped cap (coord_cartesian ylim 0-50) the significant top hits and their labels remain visible and readable", False, "49 Up/Down genes above the cap; 9 of 13 labels overprinted at the panel edge; the 'render at the edge' claim is false")],
        "Executed: run/i4_shipped_example.R (sys.source of the shipped file), i4b_pdf_check.py, i4c_extreme_synth.R (SYNTHETIC), i4d_repel_default.R; PDFs and PNGs opened. ggrepel default max.overlaps did not raise a warning for 60 labels on real or synthetic data, so that claim was not reproduced (not scored)."),
    inp(5, "Scope Boundary", "Non-DESeq2 inputs: limma microarray table (real ALL, BCR/ABL vs NEG) and a Python volcano the Skill advertises but does not ship",
        "volcano_plot() fails on a limma topTable as delivered (object 'padj' not found inside case_when); after renaming columns the counts match the table (31 Up / 2 Down) and ABL1 probes rank on top. limma logFC equals the plain group-mean difference to 2e-15, so the Skill's 'limma already shrinks / the original shrunken-LFC method' is wrong, and the function's fixed '(shrunken)' axis label would mislabel it. EnhancedVolcano accepts limma columns. The Python volcano written from the Skill's rules works (450/365, right top genes) but the Skill supplies no code for it.",
        28, 42,
        [a("volcano_plot() from SKILL.md runs on a limma topTable as the Skill's 'plot logFC vs adj.P.Val directly' implies", False, "case_when error, object 'padj' not found; no column-mapping guidance"),
         a("After renaming logFC/P.Value/adj.P.Val the plot's Up/Down counts equal the table", True, "31/2 both; PNG opened, 1636_g_at 1635_at 1674_at (ABL1) labelled"),
         a("EnhancedVolcano(x='logFC', y='adj.P.Val') draws all probes from a limma table", True, "12,625 points; PNG opened"),
         a("A Python volcano built from the Skill's stated rules (matplotlib + adjustText 1.4.0, padj classes, combined-rank labels, raster) is correct", True, "450 Up / 365 Down, same top genes as the R path; PNG opened"),
         a("The claim that limma logFC is already an empirical-Bayes shrunken estimate holds", False, "max |logFC - group-mean difference| = 2.2e-15; eBayes moderates the variance, not the LFC")],
        "Executed: run/i5_limma_scope.R, run/i5b_prep_symbols.R + i5b_python_volcano.py (adjustText 1.4.0). sanbomics.tools.volcano (named in the Skill) is not installed and was not run."),
]
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
P = sum(i["assertions_passed"] for i in inputs)
T = sum(i["assertions_total"] for i in inputs)
cats = {
    "functional_suitability": (8, 12, "Completeness 3, correctness 2, appropriateness 3. Covers ggplot2, EnhancedVolcano and MA well, but gives no Python volcano code, no non-DESeq2 column mapping and no ID-to-symbol step. Several stated behaviours do not reproduce: EnhancedVolcano selectLab filtering (5 places), ashr svalue, limma logFC 'shrunken', the coord_cartesian 'edge' claim, the 5 MB PDF claim."),
    "reliability": (8, 12, "Common Errors table is broad and most rows reproduce (NA padj dropped, apeglm coef). The reference function dies with a cryptic case_when error on any table not named padj/log2FoldChange/pvalue, and the y cap silently hides the top hits."),
    "performance_context": (5, 8, "325 lines / ~3,000 words in one SKILL.md with a 91-line usage-guide.md that repeats the same eleven tips and prompts; no references/ layer."),
    "agent_usability": (12, 16, "Goal/Approach blocks, a decision tree and version stamps help. Consistency suffers: the Skill's own rule (threshold line on the axis quantity) is broken by its function and example, and the example colours by padj while plotting raw p."),
    "human_usability": (6, 8, "Natural example prompts and a reviewer-pushback table; several pushback answers rest on claims that fail."),
    "security": (11, 12, "No credentials, network, eval or shell. The example writes volcano.pdf/ma_plot.pdf into the cwd and overwrites silently."),
    "maintainability": (8, 12, "Version-stamped and self-contained, but the example is not runnable without a user-supplied dds whose coef name is assumed, and hardcodes labels (TP53, MYC, BRCA1) that need symbol rownames."),
    "agent_specific": (16, 20, "Precise trigger description; related Skills all exist. Dangling [[api_gotchas]] link, no progressive disclosure, no escape hatch for non-DESeq2 column names."),
}
static = sum(v[0] for v in cats.values())
sw = round(static * 0.4, 1)
dw = round(avg * 0.6, 1)
score = round(static * 0.4 + avg * 0.6)
l1 = sum(i["basic"] for i in inputs) / 5
l2 = sum(i["specialized"] for i in inputs) / 5
floors = {"static>=70": static >= 70, "exec>=75": avg >= 75, "L1>=28": l1 >= 28, "L2>=42": l2 >= 42, "assertions>=80%": P / T >= 0.8}
print("static", static, "avg", avg, "score", score, "L1", l1, "L2", l2, "assertions", P, T, round(100 * P / T, 1), floors)
assert not floors["assertions>=80%"] and all(v for k, v in floors.items() if k != "assertions>=80%")
rec = [
    {"priority": "P1", "title": "Threshold line drawn on the wrong axis quantity", "observed_in": [1, 4, 5],
     "problem": "volcano_plot() and examples/volcano_phd.R plot -log10(pvalue), colour by padj, and draw the hline at -log10(fdr). On airway 1,684 genes that are not FDR-significant (padj>=0.05 or NA) sit above the line and the padj<0.05 boundary is really at 1.95. This is the Skill's own 'Raw p threshold line drawn on adjusted axis' failure mode.",
     "root_cause": "The function was written for y = raw p while the significance class and the line assume padj; the example's comment calls it 'approximate' instead of fixing it.",
     "fix": "Plot y = -log10(padj) (as the EnhancedVolcano block does) or draw the hline at -log10(max pvalue with padj<fdr); label the axis to match; state that the LFC on x is shrunken while p/padj come from the unshrunken Wald test."},
    {"priority": "P1", "title": "Shipped y-cap hides the top hits and mangles their labels", "observed_in": [4],
     "problem": "y_cap = 50 is applied unconditionally in the example. On airway 49 significant genes (max 135) leave the panel and 9 of 13 labels overprint at the top edge; coord_cartesian does not 'render at the edge' as SKILL.md and the usage-guide prompt state.",
     "root_cause": "coord_cartesian clips the view; the guidance treats it as a squish, and labels are chosen before the cap.",
     "fix": "Apply the cap only when max(-log10 p) exceeds it; use pmin(y, cap) with a distinct (triangle) shape for capped points, or exclude off-panel genes from the labels; correct the 'keeps points at the edge' wording."},
    {"priority": "P1", "title": "Not usable on the non-DESeq2 tables it claims; limma called 'shrunken'", "observed_in": [5],
     "problem": "The description and decision tree cover limma/MSstats/ChIP/ATAC, but volcano_plot() fails on logFC/P.Value/adj.P.Val columns (cryptic case_when error), no column mapping is shown, the axis label is hard-coded '(shrunken)', and limma is described as 'the original shrunken-LFC method' though its logFC equals the plain mean difference to 2e-15.",
     "root_cause": "The function hard-codes DESeq2 column names and the shrinkage claim confuses variance moderation with LFC shrinkage.",
     "fix": "Add x/y/padj/baseMean column arguments (defaults DESeq2), set the x label from an argument, and rewrite the limma rows: eBayes moderates variances, not the LFC, so the plotted LFC is unshrunken."},
    {"priority": "P2", "title": "EnhancedVolcano 'selectLab filtered by thresholds' does not reproduce", "observed_in": [2],
     "problem": "Stated in the Gotcha, failure-mode, Common Errors, usage-guide tip and the example comment. In EnhancedVolcano 1.24.0 GAPDH (padj 0.43) and TP53 (|LFC| 0.40) are labelled; the only genes that vanish have NA padj (no y).",
     "root_cause": "Claim not checked against the installed source (selectLab is matched by lab %in% selectLab only).",
     "fix": "Replace it with: selectLab genes with NA padj (or absent from lab) are not drawn; drop the 'build labels manually' workaround and the 'pre-shrink so genes pass' advice."},
    {"priority": "P2", "title": "ashr svalue comment wrong; svalue=TRUE removes pvalue/padj", "observed_in": [2],
     "problem": "'# ashr also returns svalue column' is false for the shown call; svalue needs svalue=TRUE, which replaces pvalue/padj so volcano_plot() then breaks. (s<0.005 gives 3,921 genes vs 3,993 for padj<0.05, so the stated equivalence itself holds.)",
     "root_cause": "The svalue argument and its side effect are not mentioned.",
     "fix": "Show lfcShrink(..., type = 'ashr', svalue = TRUE), note the replaced columns, and let the volcano function take the significance column as an argument."},
    {"priority": "P2", "title": "Python volcano advertised but not shipped", "observed_in": [5],
     "problem": "The description and overview name matplotlib + adjustText (and sanbomics.tools.volcano) for volcanos but only ma_plot() has code; the sanbomics package is not installed and unverified.",
     "root_cause": "Python section stops at the MA function.",
     "fix": "Add a short Python volcano (padj classes, combined-rank labels, rasterized scatter, adjust_text) mirroring the R function, or drop the claim; verify or remove the sanbomics mention."},
    {"priority": "P2", "title": "Ensembl IDs, unrunnable example and dangling link", "observed_in": [1, 4],
     "problem": "DESeq2 output usually has Ensembl rownames, so the example's TP53/MYC/BRCA1 labels match nothing (silently); the example needs an undefined dds with coef 'condition_treated_vs_control'; SKILL.md links [[api_gotchas]], which does not exist.",
     "root_cause": "No ID-to-symbol step, no example data and an unresolved wiki link.",
     "fix": "Add a mapIds/rownames step and a minimal dds constructor to the example, warn when labels are absent from the table, and remove or supply api_gotchas."},
    {"priority": "P2", "title": "Smaller accuracy and consistency items", "observed_in": [2, 3, 4],
     "problem": "(a) '5MB+ PDF' for vector scatter: 0.50 MB measured. (b) EnhancedVolcano y axis reads '-Log10 P' while plotting padj and the Skill does not set ylab. (c) ma_plot() hard-codes '(shrunken)'. (d) SKILL.md cites Dudoit 2002 as 'JASA' but the reference list says Stat Sin. (e) 'horizontal stripe = batch confound' and 'asymmetry = normalization failure' MA heuristics are stated without support. (f) The example's MA colours by 'significance != NS' (padj and |LFC|) while the SKILL's plotMA colours by padj only.",
     "root_cause": "Statements were not tested.",
     "fix": "Correct or soften each (measured PDF size, ylab = expression(-log[10]~adj.~p), label argument, citation, hedge heuristics, one colouring rule)."},
    {"priority": "P2", "title": "SKILL.md and usage-guide.md duplicate the same tips", "observed_in": [],
     "problem": "The eleven usage-guide tips and the Quick Start prompts restate SKILL.md failure modes almost word for word (~880 words), and all of it loads with a 325-line SKILL.md.",
     "root_cause": "No split between method and quick start.",
     "fix": "Keep the tips once (SKILL.md) and make usage-guide.md a short prompt list, or move failure modes to references/."},
]
report = {
    "meta": {"skill_name": SID,
             "description": "Build volcano and MA plots from differential-expression / association results with LFC shrinkage, FDR-adjusted thresholds, sensible label placement, and axis-truncation conventions. Covers EnhancedVolcano, ggplot2, matplotlib, and the apeglm/ashr/normal shrinkage decision.",
             "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A",
             "complexity": "Moderate", "n_inputs": 5,
             "source": "mrsonord2240/bioSkills@019953e9ca90f6f6f69e3f5a9cd19a5c1b9dc6be:data-visualization/volcano-and-ma-plots",
             "audit_type": "first audit (unmodified upstream GPTomics/bioSkills content)",
             "executed": True,
             "execution_note": "Executed 5/5 inputs on the data-visualization env: R 4.4.3 (DESeq2 1.46.0, EnhancedVolcano 1.24.0, ggplot2 4.0.3, ggrepel 0.9.8, limma, ALL, apeglm 1.28.0, ashr 2.2.63) and Python 3.12 (pandas 3.0.6, matplotlib 3.11.2, adjustText 1.4.0). All 5 SKILL.md code blocks and the shipped example were parsed and run (block 01's calls were run as equivalent statements in i0_prep_airway.R). Real data: Bioconductor airway (dex vs untreated) and ALL; the extreme-p table is SYNTHETIC (seed 20260920). Every output PNG/PDF was opened or measured."},
    "veto_gates": {"skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
                   "research_veto": {"applicable": True, "gate": "PASS",
                                     "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOI, statistic or result; the citations checked (Zhu 2019, Stephens 2017, Bourgon 2010, Wong 2011) are real. Several tool-behaviour statements are wrong (selectLab filtering, ashr svalue, limma 'shrunken', 5 MB PDF) but they are recorded as accuracy defects, not invented evidence."},
                                     "practice_boundaries": {"result": "PASS", "detail": "Visualization Skill; no diagnostic or prescriptive content."},
                                     "methodological_ground": {"result": "PASS", "detail": "No conclusion-inverting fallacy. The raw-p axis with padj colouring and the limma 'shrunken' claim are recorded as P1 defects: the plot can mislead but the classification by padj and |LFC| is computed correctly."},
                                     "code_usability": {"result": "PASS", "detail": "All 4 R blocks, the Python block and shipped volcano_phd.R example parse and ran; outputs opened. volcano_plot() does not run on non-DESeq2 column names and the example needs a user dds (P1/P2)."}}},
    "static_score": {"subtotal": static, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": P, "total": T}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "\u26a0\ufe0f",
              "deployable": False, "veto_override": False,
              "grade_note": f"Numeric {round(static * 0.4 + avg * 0.6, 1)} is Limited Release, but the assertion pass rate {P}/{T} = {round(100 * P / T, 1)}% is under the 80% Limited Release floor (scoring_rubric section 5), so the grade drops one tier to Beta Only. Static {static} >= 70, execution {avg} >= 75, L1 avg {l1:.1f} >= 28 and L2 avg {l2:.1f} >= 42 all pass. No veto fired and no P0 is open; deployable is false only because of the grade."},
    "key_strengths": [
        "Numerically sound core: every plotted count, x/y value, threshold line and label set checked against the DESeq2 and limma tables was right, and the MA/shrinkage fan diagnostic reproduced (baseMean<5 max |LFC| 5.19 raw to 2.91 apeglm).",
        "Shrinkage guidance is correct on the installed stack: lfcShrink default is apeglm, apeglm needs coef, ashr accepts contrast, s<0.005 tracks padj<0.05 (3,921 vs 3,993), NA padj rows are dropped by EnhancedVolcano as stated.",
        "Combined-rank labelling surfaces the real dex biology on airway (ZBTB16, DUSP1, KLF15, PER1, SPARCL1) and never a housekeeping gene; cairo_pdf output embeds TrueType and no Type 3 fonts.",
        "Extreme values do not crash the function: p = 1e-200 and an underflowed p = 0 draw (Inf lands on the panel edge)."],
    "recommendations": rec}
(A / f"eval_report_{SID}_result.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
print("written; recs", [r["priority"] for r in rec])
