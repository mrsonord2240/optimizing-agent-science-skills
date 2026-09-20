#!/usr/bin/env python3
"""Builds eval_report_bio-sashimi-plots_result.json from the audit findings and runs the schema pre-emit checklist."""
import json, sys

A = lambda t, ok, n: {"text": t, "result": "PASS" if ok else "FAIL", "note": n}

inputs = [
 dict(index=1, type="Canonical", label="ggsashimi Control vs Treatment overlay on planted 3v3 exon-skipping BAMs (SKILL.md block)",
  status="COMPLETED", flag="\u26a0\ufe0f", executed=True,
  exec_note="SKILL.md block run verbatim (pdf 18,738 B, plus svg/png of the same call). Labels 41/11/39 and 11/39/10 checked against pysam counts; z-order, colours and panel alignment inspected on the rendered PNG.",
  note="Junction labels correct (round mean of raw counts); coverage drawn gray (no -C), 'Edit colors in groups TSV' does nothing; -M 10 drops the 9- and 8-read replicate before averaging (label 11 vs true mean 10.33); gene model panel not aligned with coverage under ggplot2 4.0.3",
  basic=34, spec=47,
  assertions=[
   A("Every plotted arc label equals the rounded mean of the independent pysam per-sample junction counts (201-501, 201-901, 601-901)", True, "Control 41/11/39 = mean(40,44,38)/(10,10,12)/(40,36,42); Treatment 39 exact"),
   A("With the Skill's -M 10, aggregate labels equal the true group mean of all replicates", False, "Treatment 201-501 shows 11 (mean of the 10 and 12 that pass -M) vs true 10.33; 601-901 shows 10 vs 9.67; per-sample filter is applied before -A mean_j and the Skill does not say so"),
   A("Skill's command yields the documented Control=blue / Treatment=orange colour convention", False, "All coverage and arcs are gray; colours need -C 3 plus -P palette (default palette red/green); the TSV group column alone does not colour"),
   A("Output is a non-empty vector PDF with the requested gene model track drawn from the GTF", True, "PDF 18,738 B; T_inc (3 exons) and T_skip (2 exons) drawn with strand arrows"),
   A("Coverage panels and gene-model panel share one x scale", False, "Junction ends do not line up with exon boundaries in the rendered figure, with or without --shrink (ggsashimi 1.1.5 with ggplot2 4.0.3; upstream reference figure is aligned); x-axis tick labels are clipped"),
  ]),
 dict(index=2, type="Variant A", label="Batch sashimi for significant rMATS SE hits (SKILL.md batch block and examples/plot_sashimi.py)",
  status="PARTIAL", flag="\u274c", executed=True,
  exec_note="Real chrX rMATS SE output (5 significant events) with the 4 real BAMs; SKILL.md block, examples/plot_sashimi.py batch_plot_rmats_events and plot_specific_event all run from a copy; planted rMATS output also tried; then a manual chrX->X region for the PDZD11 event.",
  note="Both batch recipes fail on Ensembl-style data (rMATS writes chrX, BAM contig is X): SKILL.md block raises CalledProcessError on the first event, the example prints 'Failed to plot' 5 times and produces 0 files; negative region start on the planted event; plot_specific_event exits 1 (-A without -O)",
  basic=24, spec=31,
  assertions=[
   A("SKILL.md batch block produces one PDF per significant event on real rMATS output", False, "0 of 5: ggsashimi 'invalid contig chrX'; the block has no try/except so the script dies at event 1"),
   A("examples/plot_sashimi.py batch_plot_rmats_events produces the plots or fails loudly", False, "Function returns normally, os.listdir shows [] after 5 printed failures; a pipeline would see exit 0 and no figures"),
   A("examples/plot_sashimi.py plot_specific_event runs as written", False, "aggregate='mean' passes -A without -O: 'ERROR: Cannot apply aggregate function if overlay is not selected', CalledProcessError"),
   A("With the contig name corrected by hand, the drawn skipping-junction label equals the independent count", True, "PDZD11 GBR label 6 for reads 7 and 6 (mean 6.5, R round half-even); pysam 69509205-69509710 = 7,6; rMATS SJC 7,6"),
   A("Region arithmetic is safe for events near a contig start", False, "planted event upstreamES=100 gives region chrP:-400-1500 and ggsashimi exits 1; no clamp to 1"),
  ]),
 dict(index=3, type="Edge", label="Minimum-junction threshold semantics, defaults, missing BAMs, bad contig, empty region",
  status="COMPLETED", flag="\u26a0\ufe0f", executed=True,
  exec_note="Nine ggsashimi calls on planted BAMs (scripts/i3_edge.sh); svg labels parsed; output in out/i3_edge.txt.",
  note="-M is per-sample and inclusive (>=); default is 1 not 10 (Skill troubleshooting says default 10); typo BAM path silently skipped (rc 0); bad contig and -A without -O exit 1 with a message; empty region draws an empty figure with rc 0",
  basic=24, spec=34,
  assertions=[
   A("Skill's statement that the default -M is 10 ('Default -M 10 too strict') is true", False, "Default run on G2_rep3 prints junctions with 9, 38 and 11 reads; --help says default=1"),
   A("-M 10 keeps a junction supported by exactly 10 reads and -M 11 drops it", True, "G1_rep1 labels 40 10 40 at -M 10 and 40 40 at -M 11 (v >= min_coverage)"),
   A("A wrong BAM path in the group TSV is reported", False, "'typo' sample silently skipped, plot of the remaining sample drawn, rc 0, no warning"),
   A("A wrong contig name gives a clear error", True, "rc 1, 'ValueError: invalid contig `1`' (traceback, not a friendly message)"),
   A("A region with no reads is reported as such", False, "rc 0 and an empty figure; no 'no reads' message reached the log"),
  ]),
 dict(index=4, type="Variant B", label="rmats2sashimiplot on rMATS SE output with group colours (SKILL.md block)",
  status="PARTIAL", flag="\u274c", executed=True,
  exec_note="rmats2sashimiplot 4.0.0: the Skill command verbatim, then five corrected variants, planted and real chrX; PDFs rendered with pymupdf (installed with pip --target outside every shared env, removed afterwards) and their text and image inspected.",
  note="Verbatim command exits 2 ('unrecognized arguments: -t SE'); with --event-type the documented --color pair plus no valid .gf group file gives exit 0 and an empty Sashimi_plot; a missing --group-info file also exits 0 with a traceback and no figure; with a correct .gf file the plot is correct",
  basic=26, spec=36,
  assertions=[
   A("The Skill's rmats2sashimiplot command runs as written", False, "rc 2: '-t SE' does not exist in 4.0.0 (--event-type); group_def.txt is never defined in the Skill and its .gf format is not documented"),
   A("A failed rmats2sashimiplot run is visible from the exit code or an output file", False, "Two colours with per-replicate plots: 'Must provide sample label and color for each entry', rc 0, empty Sashimi_plot; missing group file: FileNotFoundError, rc 0, mv fails, no PDF"),
   A("With a valid grouping.gf the plotted counts equal the independent pysam counts", True, "Group means 41/11/39 and 10/39/10, IncLevel 0.79 / 0.20; per-replicate run gives 40/10/40, 44/10/36, 38/12/42, 10/40/10, 12/40/8, 9/38/11 exactly"),
   A("Real chrX/X contig naming works without manual intervention", True, "rMATS chrX event plotted against BAM contig X with or without --remove-event-chr-prefix; GBR skip 6, YRI 3/2/1, IncLevel 0.00 / 0.27 = rMATS 0.274"),
   A("The 'rmats2sashimiplot expects 1-based coordinates ... plot region shifted by 1 nt' failure mode is reproducible", False, "Exon boundaries 101/200/501/600/901/1000 plot aligned; the rMATS *_0base columns are handled; claim is unsupported"),
  ]),
 dict(index=5, type="Stress", label="Real 10-BAM ENCODE locus, three groups, strandedness options (ggsashimi)",
  status="COMPLETED", flag="\u2705", executed=True,
  exec_note="ggsashimi's own real data (12 sample rows incl. 3 groups): -j junction BED and svg with the Skill flags compared with pysam (scripts/i5_check.py); repo example 2 re-rendered and compared with the upstream figure; -s SENSE/ANTISENSE on planted reads and MATE1/MATE2_SENSE on real paired-end chrX compared with an independent pysam strand counter.",
  note="Per-sample junction BED equals pysam exactly (36 sample-junction pairs) and all 9 aggregate labels equal the independent means; strand routing correct; with -s the output splits into <prefix>_+.<fmt> and <prefix>_-.<fmt> (undocumented); MATE1_SENSE on single-end reads crashes",
  basic=34, spec=51,
  assertions=[
   A("ggsashimi per-sample junction counts and 1-based coordinates match pysam at -M 10", True, "i5_check.py: True for 12 samples / 36 junction records"),
   A("Aggregate -O 3 -A mean_j labels equal the independent group means", True, "126/207/169, 265/115/186, 258/35/201 all present and identical to the upstream reference figure"),
   A("-s MATE2_SENSE / MATE1_SENSE route reads to the strand a dUTP library implies", True, "Real chrX PE reads: 3 on '+' and 3 on '-' for either mode, identical to the independent strand counter"),
   A("The Skill tells the reader that -s writes two files (plus and minus)", False, "Output is i5s_SENSE_+.svg and i5s_SENSE_-.svg; the Skill and plot_sashimi.py print '{prefix}.pdf' and never expose -s"),
   A("Every strandedness value named for single-end data works", False, "-s MATE1_SENSE on unpaired reads: TypeError NoneType ^ bool; SENSE/ANTISENSE work"),
  ]),
 dict(index=6, type="Scope Boundary", label="pyGenomeTracks multi-track figure with regtools junction arcs (Skill ini + awk BEDPE conversion)",
  status="COMPLETED", flag="\u26a0\ufe0f", executed=True,
  exec_note="regtools 1.0.0 junctions extract -> Skill awk verbatim -> BEDPE; Skill ini verbatim with bigwigs I built (bedtools genomecov -split -bga + pyBigWig; the Skill never says how to make bigwigs); pyGenomeTracks 3.9 PDF and PNG rendered and inspected; BAM track attempted.",
  note="BEDPE anchors exactly at 0-based intron start/end (200/499, 199/899, 600/899) and arcs land on the drawn exon edges; ini runs verbatim; a BAM track is not supported ('can not identify file type') though the Skill text says 'BAM'; the two coverage tracks get different y ranges",
  basic=32, spec=46,
  assertions=[
   A("Skill awk turns regtools BED12 into BEDPE whose anchors equal the independent intron boundaries", True, "regtools chrP 175-525 -> BEDPE 200-201 / 499-500 score 40; all three junctions match pysam introns 201-500, 201-900, 601-900 (1-based)"),
   A("Skill ini renders 3 links and 2 coverage tracks over the gene model without edit", True, "log: '3 were links plotted'; PDF 20,270 B; arcs start/end at exon edges in the PNG"),
   A("A BAM can be given as a track as the Skill text ('genes, BAM, BigWig, BED') suggests", False, "InputError: can not identify file type for the .bam"),
   A("Control and Treatment coverage tracks are drawn on a common y scale", False, "67.72 vs 56.17 upper bounds; the ini sets no min/max although the Skill insists on identical y scales elsewhere"),
   A("The Skill tells the reader how to produce the bigwig and how coverage of spliced reads must be split", False, "No recipe; my first bigwig (genomecov without -split) filled introns with coverage until corrected"),
  ]),
 dict(index=7, type="Adversarial", label="Validate a leafcutter cluster and a MAJIQ LSV, plus a tool-agnostic Jutils view (leafviz, VOILA, Jutils)",
  status="PARTIAL", flag="\u274c", executed=True,
  exec_note="Jutils 0.x from the GitHub clone (convert-results, heatmap, sashimi, venn-diagram), leafviz scripts from the leafcutter clone (prepare_results.R --help and run, requireNamespace), bioconda search for the install lines. MAJIQ/VOILA is licence-gated and was not executed; its flags were checked only against the public VOILA view documentation.",
  note="Jutils sashimi is correct (per-replicate labels 40,44,38 / 10,10,12 / 40,36,42 exact) but convert-results names the output rmats_JC_results.tsv (Skill: rmats.tsv) and venn-diagram --tsv-file-list wants a file of paths (Skill: comma list, exit 1); library(leafviz)/run_leafviz() do not exist; conda install of ggsashimi and jutils finds no package; 'voila view ... -o' has no -o in the documented option list",
  basic=24, spec=30,
  assertions=[
   A("Skill's Jutils sashimi call (tsv + meta + gtf + coordinate + bam-list) draws the correct counts", True, "labels 40,44,38 / 10,10,12 / 40,36,42 and 10,12,9 / 40,40,38 / 10,8,11 equal the pysam counts"),
   A("Skill's Jutils venn-diagram command runs as written", False, "FileNotFoundError: 'jutils_out/...,jutils_out/leafcutter.tsv'; --tsv-file-list takes a file listing TSV paths; also jutils_out/rmats.tsv is not a file name convert-results writes"),
   A("Skill's leafviz launch code exists", False, "requireNamespace('leafviz') FALSE; no run_leafviz() in leafcutter; the tool is Rscript leafviz/run_leafviz.R <file>.RData; prepare_results.R -o leafviz would not create leafviz.RData"),
   A("The installation lines in usage-guide.md work", False, "micromamba search: 'No entries matching ggsashimi', none for jutils; rmats2sashimiplot 4.0.0 and pygenometracks 3.9 do exist, so the single conda install line fails atomically"),
   A("The Skill points to a tool for the MAJIQ LSV that could be run and checked", False, "MAJIQ V3/VOILA not installable here (academic download); 'voila view -o <dir>' contradicts the documented option list (view is a server, no -o); not executed"),
  ]),
]

for i in inputs:
    i["total"] = i["basic"] + i["spec"]
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    i["assertions_total"] = len(i["assertions"])

static = {
 "functional_suitability": (8, 12, "Covers six tools and a decision tree, but several stated recipes are wrong as written: rmats2sashimiplot -t SE, run_leafviz(), comma venn list, wrong Jutils file name, default -M 10, colours via TSV, mean_j 'sample-wise normalization'; no bigwig or .gf group-file recipe"),
 "reliability": (6, 12, "Batch code has no contig-name mapping, no clamp for negative region starts, no empty-result check, and hides failures behind print(); ggsashimi silently skips missing BAMs; rmats2sashimiplot exits 0 with no figure; Common Errors table is a real help"),
 "performance_context": (6, 8, "393-line SKILL.md plus short usage guide; no references/ split, tool sections could be conditional"),
 "agent_usability": (9, 16, "Goal/Approach headings and a decision tree are easy to follow; inconsistent flag styles and wrong facts would mislead an agent; no instruction to verify a figure against a junction count"),
 "human_usability": (6, 8, "Description names every tool and use case in natural language; wrong commands leave little room to recover"),
 "security": (10, 12, "subprocess with list arguments, no secrets; gene symbols go into output file names unsanitised"),
 "maintainability": (8, 12, "One example module and a usage guide; no test data, no version pins beyond 'ggsashimi 1.1+ / ggplot2 3.5+' although 4.x changes the layout"),
 "agent_specific": (14, 20, "Good trigger text and Related Skills; tool matrix helps choice; escape hatches for licence-gated tools present; nothing tells the agent when a run silently produced nothing"),
}
sub = sum(v[0] for v in static.values())
exec_avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * 0.4, 1), round(exec_avg * 0.6, 1)
score = int(round(sw + dw))

rec = [
 dict(priority="P0", title="rmats2sashimiplot block does not run and fails silently", observed_in=[4],
  problem="'-t SE' is rejected by rmats2sashimiplot 4.0.0 (rc 2). After using --event-type, the documented 2-colour --color without a valid .gf file or a missing --group-info file both exit 0 and leave Sashimi_plot empty. group_def.txt is never defined.",
  root_cause="Command copied from an older CLI, no group-file format, no output check.",
  fix="Use --event-type SE; show a grouping.gf ('Control: 1-3' / 'Treatment: 4-6', 1-based over --b1 then --b2), require one colour per group (or per replicate), and add 'ls Sashimi_plot/*.pdf' as a required check because the tool exits 0 on failure."),
 dict(priority="P0", title="leafviz, Jutils venn and install lines use commands that do not exist", observed_in=[7],
  problem="library(leafviz)/run_leafviz() do not exist (leafviz is a script directory); venn-diagram --tsv-file-list needs a file of paths, not a comma list; convert-results writes rmats_JC_results.tsv, not rmats.tsv; conda install ggsashimi/jutils finds nothing; 'voila view -o' has no -o in the documented options (VOILA view is a server).",
  root_cause="APIs written from memory and never run; unmaintained-tool packaging assumed.",
  fix="Replace with 'Rscript leafviz/run_leafviz.R leafviz.RData' after 'prepare_results.R -o leafviz.RData ...' (annotation_codes is a path prefix); give a tsv_list.txt example (path<TAB>label); use the real output names; install ggsashimi and Jutils from their GitHub clones (R with ggplot2, data.table, gridExtra, pysam); state that VOILA view serves a browser and give the V3 command from its own docs."),
 dict(priority="P1", title="Batch recipes break on Ensembl-style contigs and near contig starts, and fail silently", observed_in=[2],
  problem="rMATS writes chrX while the BAM contig is X; the SKILL.md block dies at event 1 and examples/plot_sashimi.py prints 5 failures and writes no file. upstreamES-500 can be < 1 (chrP:-400-1500). plot_specific_event passes -A without -O and always fails.",
  root_cause="No contig-name reconciliation, no clamp, no result check, options mixed without testing.",
  fix="Map the contig against the BAM header (pysam) or strip 'chr' when absent, use max(1, start), raise if no file is produced, and make plot_specific_event pass -O 3 (or drop aggregate)."),
 dict(priority="P1", title="Wrong statements about ggsashimi defaults, colours and aggregation", observed_in=[1, 3],
  problem="Default -M is 1, not 10. 'Edit colors in groups TSV' does not colour anything: -C <col> and -P palette are needed, and the default palette is not blue/orange. mean_j is a plain mean of raw counts, not 'sample-wise normalization'. -M is applied per sample before averaging, so a label can be biased upward (11 vs 10.33 in the planted data). With -s the output splits into _+ and _- files.",
  root_cause="Prose written without running the tool.",
  fix="Correct these lines; add -C 3 -P palette.txt to the Publication Overlays example; add one sentence that -M filters each sample before -A."),
 dict(priority="P1", title="Version line hides a layout regression with ggplot2 4.x", observed_in=[1, 2, 5, 7],
  problem="With ggsashimi 1.1.5 and ggplot2 4.0.3 the gene model is not aligned with the coverage panels and x tick labels are clipped, while the upstream reference figure is correct. Arc labels are unaffected.",
  root_cause="'ggplot2 3.5+' has no upper bound and no visual check.",
  fix="Pin ggplot2 <4 for ggsashimi 1.1.5 (or note the check), and tell the agent to look at the figure for exon/arc alignment before reporting it."),
 dict(priority="P1", title="Failure modes that exit 0 are not called out", observed_in=[3, 4],
  problem="ggsashimi silently drops BAM paths that do not exist; empty regions produce an empty figure; rmats2sashimiplot exits 0 on errors.",
  root_cause="Common Errors table lists messages that are not what the tools print.",
  fix="Add a post-run check to every recipe: files exist, sample count in the TSV equals samples drawn, at least one junction label present; correct the Common Errors table ('invalid contig', 'No available bam files')."),
 dict(priority="P1", title="pyGenomeTracks section promises a BAM track and gives no bigwig recipe", observed_in=[6],
  problem="pyGenomeTracks 3.9 cannot draw a BAM; the ini needs bigwigs the Skill never shows how to make (bedtools genomecov must use -split -bga or introns fill with coverage); tracks have unlinked y scales.",
  root_cause="Generic track description not exercised.",
  fix="Add 'bamCoverage' or 'genomecov -split -bga' + bedGraphToBigWig, drop 'BAM' from the sentence, add min_value/max_value on both coverage tracks."),
 dict(priority="P2", title="Unsupported coordinate-convention failure mode and minor items", observed_in=[4, 5],
  problem="The rmats2sashimiplot 1-nt shift claim could not be reproduced; MATE1_SENSE on single-end reads crashes; R round() halves to even (6.5 shown as 6); geneSymbol enters file names unsanitised.",
  root_cause="Unverified troubleshooting content.",
  fix="Delete or evidence the shift claim, list MATE*_SENSE as paired-end only, sanitise safe_name, mention integer rounding of aggregate labels."),
]

report = {
 "source": "mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/sashimi-plots",
 "meta": {
  "skill_name": "bio-sashimi-plots",
  "description": "Creates sashimi-style plots showing RNA-seq read coverage and splice junction counts using ggsashimi, rmats2sashimiplot, MAJIQ-VOILA, leafviz, Jutils or pyGenomeTracks; tool choice depends on the upstream differential-splicing output and the publication vs interactive use case.",
  "evaluated_on": "2026-09-20",
  "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis",
  "execution_mode": "D",
  "complexity": "Complex",
  "n_inputs": 7,
  "executed_k_of_n": "7/7 (input 7: MAJIQ/VOILA part not executed, licence-gated)",
  "env": "F:/OpenScience/audit-envs/alternative-splicing (ggsashimi 1.1.5 clone, rmats2sashimiplot 4.0.0, pyGenomeTracks 3.9, Jutils clone, regtools 1.0.0, pysam 0.24.1; ggplot2 4.0.3)",
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "FAIL",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated identifiers or numbers; every label I generated was checked against pysam counts. Unsupported claims (rmats2sashimiplot 1-nt shift, mean_j normalization) are factual errors, not fabricated data."},
   "practice_boundaries": {"result": "PASS", "detail": "Visualisation only; no diagnostic or prescriptive content."},
   "methodological_ground": {"result": "PASS", "detail": "Strand handling, -M semantics and group aggregation verified correct in the tool; the per-sample -M before -A bias is tool behaviour left undocumented (P1), not a methodological fallacy."},
   "code_usability": {"result": "FAIL", "detail": "Inputs 4 and 7: the Skill's rmats2sashimiplot command (-t SE), leafviz launch (run_leafviz), Jutils venn-diagram comma list and conda install line are unrunnable as written; input 2: both batch recipes fail on real Ensembl-style data and plot_specific_event always exits 1. The primary ggsashimi block, Jutils sashimi and the pyGenomeTracks/awk recipe run and are correct. Fixing the P0 items clears this gate."},
  },
 },
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
 "dynamic_score": {
  "execution_avg": exec_avg, "max": 100,
  "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
  "inputs": [dict(index=i["index"], type=i["type"], label=i["label"], status=i["status"], status_flag=i["flag"],
                  note=i["note"], executed=i["executed"], execution_note=i["exec_note"], basic=i["basic"], specialized=i["spec"],
                  total=i["total"], assertions_passed=i["assertions_passed"], assertions_total=i["assertions_total"],
                  assertions=i["assertions"]) for i in inputs],
 },
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
           "grade": "Reject", "grade_symbol": "\u274c", "deployable": False, "veto_override": True,
           "note": f"Numeric score {score} would be Beta Only; grade forced to Reject by the Research Veto M4 (code usability)."},
 "key_strengths": [
  "ggsashimi core path is right: per-sample junction BED equals pysam exactly on 12 real ENCODE samples and the 9 aggregate labels equal the upstream reference figure; strand routing (-s MATE*_SENSE) and -M >= semantics verified",
  "Tool-selection matrix and decision tree by goal are accurate and useful; rmats2sashimiplot with a proper .gf group file, Jutils sashimi and pyGenomeTracks links reproduce the planted counts (41/11/39, 40/44/38) exactly",
  "The regtools BED12 -> BEDPE awk conversion is correct (anchors land on the intron boundaries) and the ini renders as written",
  "Failure-mode sections on strandedness, --shrink, --fix-y-scale and flank size are the right topics for a splicing figure",
 ],
 "recommendations": rec,
}

# pre-emit checklist
d = report
assert len(d["static_score"]["categories"]) == 8
assert d["static_score"]["subtotal"] == sum(c["score"] for c in d["static_score"]["categories"].values())
assert len(d["dynamic_score"]["inputs"]) == d["meta"]["n_inputs"] == 7
for i in d["dynamic_score"]["inputs"]:
    assert 3 <= len(i["assertions"]) <= 5, i["index"]
    assert i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"]
assert d["dynamic_score"]["execution_avg"] == round(sum(i["total"] for i in d["dynamic_score"]["inputs"]) / 7, 1)
assert 2 <= len(d["key_strengths"]) <= 5
assert [r["priority"] for r in rec] == sorted(r["priority"] for r in rec)
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print("static", sub, "exec_avg", exec_avg, "score", score, "assertions", d["dynamic_score"]["assertion_pass_rate"])
print("L1 avg", round(sum(i["basic"] for i in inputs) / 7, 1), "L2 avg", round(sum(i["spec"] for i in inputs) / 7, 1))
