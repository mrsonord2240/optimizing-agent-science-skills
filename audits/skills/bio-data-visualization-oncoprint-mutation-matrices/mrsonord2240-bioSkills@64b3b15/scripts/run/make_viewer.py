import json
SK = "bio-data-visualization-oncoprint-mutation-matrices"
OUT = r"F:\OpenScience\audits\%s" % SK
r = json.load(open(OUT + r"\eval_report_%s_result.json" % SK, encoding="utf-8"))
d = r["dynamic_score"]; f = r["final"]
L = []
L.append("# Eval Viewer - %s\n" % SK)
L.append("Generated: 2026-09-20 | Source: `%s` | Category: Data Analysis | Mode A | Complexity: Complex (7 inputs)\n" % r["meta"]["source"])
L.append("Method: every figure was rendered to SVG (svglite) and its rectangles, polygons and text labels were decoded and compared with counts computed independently from the raw MAF (pandas/scipy/base R). PNGs were opened with the Read tool and are non-blank. Data: real TCGA-LAML (maftools extdata, 193 samples) and SYNTHETIC cohorts with planted truth (`run/data`, generators `run/gen_synth_*.R`). Scripts are in `run/`, outputs in `run/out/`.\n")
L.append("## Summary Table\n")
L.append("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|")
for i in d["inputs"]:
    L.append("| %d | %s | %d | %d | %d | %d/%d PASS | %s |" % (i["index"], i["type"], i["basic"], i["specialized"], i["total"], i["assertions_passed"], i["assertions_total"], i["status_flag"]))
L.append("\n**Execution Average: %s / 100** | **Assertion Pass Rate: %d/%d** | Static: %d/100 | **Final: %d (%s), deployable: %s, veto: none**\n" % (d["execution_avg"], d["assertion_pass_rate"]["passed"], d["assertion_pass_rate"]["total"], r["static_score"]["subtotal"], f["score"], f["grade"], str(f["deployable"]).lower()))
L.append("Floors (Limited Release): static >= 70 met (71); execution avg >= 75 not met (74.9); assertion pass rate >= 80% not met (59%).\n")
L.append("## Skill Veto and Research Veto\nAll PASS (see JSON). M4 note: the comut block fails verbatim, but the Skill's own version section instructs the agent to introspect and adapt on AttributeError/TypeError, so it is recorded as P1 and not a veto.\n")
L.append("## Shipped-means-present (gate 8)\n`SKILL.md` points at no scripts/references; `examples/oncoprint_phd.R` and `usage-guide.md` exist; the six Related Skills all exist in staging. The example ran from a copy (`run/ex_run.R`) once `mat`, `clinical` and `cohort.maf` were supplied (the example leaves them as comments; `cohort.maf` does not exist).\n")
L.append("## SKILL.md code blocks\n| Block | Result |\n|---|---|\n| ComplexHeatmap `oncoPrint` | ran after defining `mat` and `clinical` (not defined by the Skill); output verified (Input 1, 5) |\n| maftools `read.maf` + `oncoplot` | ran only after adding `Tumor_Sample_Barcode` to clinical and giving numeric features a palette (Input 2) |\n| `somaticInteractions` | ran; returns a data.table (Input 6) |\n| comut Python block | FAILS verbatim: AttributeError (`comut.CoMut`), then ValueError (sample subset rule), then TypeError on pandas 3 (Input 4) |\n| examples/oncoprint_phd.R | ran with supplied objects; `oncoprint.pdf` 41 KB (Input 5) |\n")
L.append("## Detailed Outputs\n")
extra = {
1: "Code: `run/i1_complexheatmap_laml.R`, `helpers.R` (Skill `alter_fun` block verbatim). Key printed output:\n```\ndrawn gene order   : DNMT3A FLT3 NPM1 TET2 IDH2 TP53 IDH1 CEBPA RUNX1 NRAS WT1 PTPN11 KIT KRAS U2AF1 SMC3 PHF6 SMC1A STAG2 TTN\ninput (count desc) : FLT3 DNMT3A NPM1 IDH2 IDH1 TET2 RUNX1 NRAS TP53 CEBPA WT1 ...\nn columns drawn: 193  cohort N: 193\ncell mismatches (drawn vs matrix in drawn order): 0 of 3860\nMissense 225 / Splice 22 / Truncating 96 (matrix) == (drawing)\npct labels: 25% 27% 17% 9% 10% 8% 9% 7% ...  expected: identical\nsubtype strip mismatches: 0 of 192 (1 NA sample grey)\ndrawn order == descending alteration-EVENT count: TRUE ; == descending mutated SAMPLES: FALSE (DNMT3A FLT3 TET2 IDH2 TP53 IDH1 CEBPA RUNX1 NRAS out of order)\n```\nFigure: `run/out/i1.png` (opened: stacked cells, staircase, coloured tracks).",
2: "Code: `run/i2_maftools_oncoplot.R`, `i2c_verify_colours.R`. Key output:\n```\nnaive numeric-feature call: ERROR: numeric annotation color for NA must be a sequential color palette!\ndrawn genes: FLT3 DNMT3A NPM1 IDH2 IDH1 TET2 RUNX1 NRAS TP53 CEBPA ...  == independent sample counts 52 48 33 20 18 17 16 15 15 13 ...\ndrawn pct: 27% 25% 17% 10% 9% 9% 8% 8% 8% 7% ... == n/193\ngene rows whose drawn colour counts equal independent per-class/Multi_Hit counts: 19 of 20 (TTN row confounded by the annotation strip; own tiles match)\nread.maf with the Skill's clinical (no Tumor_Sample_Barcode): ERROR: Tumor_Sample_Barcode column not found\n```\nFigures: `run/out/i2.png`, `i2b.png` (partial annotationColor: only M1/M0 coloured, rest grey, legend lists two).",
3: "Code: `run/gen_synth_edge.R`, `i3_edge.R` (synthetic, planted). Key output:\n```\nmatrix from MAF+CNV equals planted truth: TRUE ; multi-class cells 2 ; S02 TP53 two Missense hits -> Missense\n[keepempty] columns 30 rows 6 order TP53 KRAS RB1 MYC PIK3CA EMPTYG ; cell mismatches 0 of 180 ; pct 27% 20% 10% 7% 7% 0%\n[dropempty] columns 13 ; cell mismatches 0 of 78 ; pct 27% 20% 10% 7% 7% 0%   (unchanged)\none-sample: ok ; all-empty: ERROR subscript out of bounds ; remove_empty_rows=TRUE drops EMPTYG only\nmaftools sample count: 16 (cohort 30) ; clinical rows 16 ; pct 50/38/19/12 ; removeNonMutated TRUE == FALSE\n```\nFigures: `run/out/i3_keepempty.png`, `i3_one.png`, `i3_maftools.png`.",
4: "Code: `run/i4_comut.py`. Key output:\n```\nimport comut; hasattr(comut,'CoMut') = False\nverbatim block (with import shim) ERROR: ValueError Unknown samples {...}\npandas 3.0.6: TypeError: Invalid value '[0.3 0.43 ...]' for dtype 'int64' (LossySetitemError)\ny tick order (bottom->top): FLT3 DNMT3A NPM1 ... CEBPA   (top gene at the bottom)\ncells checked 1930 | mismatches 0 | 2-class triangle cells 20\nTMB values above the Skill's 30: 1 of 192 ; normalised keys for 10,20,30 over (10,30): 0, 0.333, 0.667\n```\nFigure: `run/out/i4_comut.png` (opened: unsorted samples, overlapping x labels, no legend).",
5: "Code: `run/gen_synth_cohort.R`, `i5_stress.R`, `i5b_tmb.R`, `ex_run.R`. Key output:\n```\nMAF rows 24326 ; hypermutator TMBs 3000 2500 1800 ; median 21\n[A unaligned] annotation strip vs TRUE subtype: mismatches 391 of 600 (no warning)\n[B aligned]   mismatches 0 of 600 ; cells 0/7200\n[C split] Basal 180 | HER2 120 | Luminal 300 ; every column in the right panel ; pct labels cohort-wide (39% TP53)\nTMB bars 600: cor(height, log10(TMB+1)) = 1.0000 ; tallest/median 2.59 (linear 142.9)\nread.maf(clinicalData = Skill-shaped clinical): ERROR Tumor_Sample_Barcode column not found\nexample: pdf exists TRUE size 41029 ; class(si) data.table ; dim 190x12\n```\nFigure: `run/out/i5_C_split.png`.",
6: "Code: `run/i6_somatic_interactions.R`, `i6_verify_fisher.py`. Key output:\n```\n[LAML top20, N=193] pairs=190 | 2x2 count mismatches=0 | p mismatches=0 | max rel diff 2.6e-13\n[synthetic N=600]   pairs=45  | 0 | 0 | 3.6e-14\n[synthetic N=20]    pairs=28  | 0 | 0 | 3.2e-15\nTP53-MYC (planted co-occur) N=600 p=7.65e-46 OR=23.7 ; N=20 p=0.141\nBRAF-NRAS (planted mutex)   N=600 p=3.07e-06 OR=0 (0/166) ; N=20 p=1.0\nreturn class data.table 190x12: gene1,gene2,pValue,oddsRatio,00,01,11,10,pAdj,Event,pair,event_ratio\nClopper-Pearson max |R - scipy| 3e-16 ; BRAF/NRAS N=20 table 0/2/1/17 Haldane-Anscombe OR 2.33\n```\nFigure: `run/out/i6_synth.png` (opened; the significance legend overlaps one heat-map cell).",
7: "Code: `run/i7_adversarial.R`. Key output:\n```\nannotation values matched by ID: 0 of 193 ; oncoPrint: ok, warnings: none\nread.maf with non-matching clinical IDs: ok, warnings: none ; clinical rows kept 0\nunmapped 'Silent' cells: ERROR You should define graphic function for: Silent\nLAML classes not covered by the Skill classes: 5'Flank IGR Intron RNA Silent\nremove_empty_columns FALSE: 193 columns pct 25% 27% 17% 9% 10% 9% 8% 8% ; TRUE: 126 columns, same pct; altered-only would be 41% 38% 26% ...\n```"}
for i in d["inputs"]:
    L.append("### Input %d - %s: %s\n" % (i["index"], i["type"], i["label"]))
    L.append("**Executed:** %s. %s\n" % (str(i["executed"]).lower(), i["execution_note"]))
    L.append("**Result:** %s\n" % i["note"])
    L.append(extra[i["index"]] + "\n")
    L.append("**Scores:** Basic %d/40 | Specialized %d/60 | Total %d/100\n" % (i["basic"], i["specialized"], i["total"]))
    L.append("**Assertions:**")
    for a in i["assertions"]:
        L.append("- [%s] %s - %s" % (a["result"], a["text"], a["note"]))
    L.append("")
L.append("## Static scores\n")
for k, v in r["static_score"]["categories"].items():
    L.append("- %s: %d/%d - %s" % (k, v["score"], v["max"], v["note"]))
L.append("\nSubtotal %d/100. Final = %.1f + %.1f = %d.\n" % (r["static_score"]["subtotal"], f["static_weighted"], f["dynamic_weighted"], f["score"]))
L.append("## Recommendations\n")
for x in r["recommendations"]:
    L.append("**[%s] %s** (inputs %s)\n- Problem: %s\n- Root cause: %s\n- Fix: %s\n" % (x["priority"], x["title"], x["observed_in"], x["problem"], x["root_cause"], x["fix"]))
L.append("> Reviewer: check the failing assertions in Inputs 3, 4, 5 and 7 first; the recurring pattern is that the Skill states denominator and return-value behaviour it never ran, and leaves the matrix/annotation construction (where the silent errors live) as comments.\n")
open(OUT + r"\eval_viewer_%s.md" % SK, "w", encoding="utf-8").write("\n".join(L))
print("ok")
