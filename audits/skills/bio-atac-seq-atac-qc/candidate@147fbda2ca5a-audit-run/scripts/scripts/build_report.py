import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def A(t, ok, n):
    return {"text": t, "result": "PASS" if ok else "FAIL", "note": n}


raw = [
 dict(type="Canonical", label="ENCODE-style TSS enrichment on real GM12878 chr1 slice", status="COMPLETED", flag="⚠️",
      note="Score 11.38 vs independent deepTools 11.39; bigWig construction recipe is undocumented and moves the score 11.3-16.0",
      basic=32, spec=46, a=[
  A("Script emits parseable JSON with a TSS_enrichment float", True, "tss.json from the tooling run; JSON valid"),
  A("Score agrees with independent deepTools computeMatrix/plotProfile", True, "11.381 vs 11.391 (TOOLS.md)"),
  A("TSS profile is a single sharp peak with flat flanks", True, "tss_profile.png inspected in tooling pass"),
  A("Score is at or above the ENCODE hg38 ideal of 7 for a healthy GM12878 library", True, "11.3"),
  A("Skill documents how to build the bigWig input so the score is reproducible", False, "no recipe; extendReads 11.32, plain 14.92, 5-prime offset 15.98 (t_bw.log)")]),
 dict(type="Canonical", label="NRF/PBC on real unfiltered and ENCODE-filtered BAMs", status="COMPLETED", flag="⚠️",
      note="Values are single-end read-start metrics, not fragment NRF/PBC; contradict the documented dedup=1.0 invariant",
      basic=26, spec=30, a=[
  A("Script runs and returns JSON on a real BAM", True, "NRF 0.353 on unfiltered, exit 0"),
  A("Planted-truth synthetic BAM reproduces hand-computed counts", True, "total 250 distinct 160 (TOOLS.md)"),
  A("Unfiltered NRF/PBC1 agree with independent fragment-level computation", False, "0.353/0.632 vs 0.619/0.767 (MAPQ>=30: 0.779/0.799); run_all.log"),
  A("Deduplicated BAM gives NRF 1.0 as the Skill states", False, "script 0.573; independent fragment NRF 1.000"),
  A("MAPQ>=30 and chrM exclusion documented in the Skill are applied", False, "planted BAM: total 300 NRF 0.34 vs 100 and 1.0 (run2.log)")]),
 dict(type="Variant A", label="ATACseqQC R script on filtered slice with ENCODE IDR peaks", status="COMPLETED", flag="⚠️",
      note="Runs; TSSEscore 23.54 (2.1x ENCODE-style) matches the Skill claim; .bed.gz peaks fail; periodicity is counted not classified",
      basic=30, spec=45, a=[
  A("TSSEscore ratio to ENCODE-style score is within the documented 2-3x", True, "23.54 / 11.38 = 2.07"),
  A("Fragment-class counts and fractions are internally consistent", True, "NFR 28.4%, mono 14.7%, di 15.6%"),
  A("Fragment-size figure is legible and shows NFR/mono/di structure", True, "fragsize_replot.png inspected; shipped PDF is valid %PDF-1.4, 1 page, but was not rasterized directly"),
  A("FRiP is computed from a narrowPeak file", True, "0.671 with ENCFF917REN.narrowPeak"),
  A("Peaks file with a .bed.gz extension is accepted", False, "scan() expected an integer, got 22.06932 (out/rbed run)")]),
 dict(type="Variant B", label="aggregate_qc.py grading and MultiQC hand-off", status="COMPLETED", flag="⚠️",
      note="Grades match thresholds but the TSV is long-format per-metric, not per-sample MultiQC content",
      basic=27, spec=36, a=[
  A("PASS/WARN/FAIL grades match the Skill threshold table", True, "7 metrics hand-checked incl. inverted mt_fraction"),
  A("Null/NaN metrics graded NA without crashing", True, "TOOLS.md"),
  A("Output is a per-sample MultiQC-compatible table as documented", False, "MultiQC custom_content parsed 7 metric rows as 7 samples"),
  A("Non-numeric metric value handled with a clear error", False, "TypeError traceback on a string value"),
  A("library_complexity.py JSON output round-trips in strict JSON parsers", False, "PBC2 emitted as bare Infinity")]),
 dict(type="Variant B", label="deepTools/Picard/samtools/MultiQC CLI recipes", status="COMPLETED", flag="✅",
      note="All recipes ran; outputs consistent with the ENCODE slice", basic=34, spec=50, a=[
  A("multiBamSummary + plotCorrelation Spearman between replicates is high", True, "0.958; heatmap legible"),
  A("plotFingerprint metrics file has synthetic JS distance", True, "0.72 and 0.67"),
  A("Picard insert-size median is biologically plausible", True, "median 191, NFR mode 45"),
  A("MultiQC detects Picard, flagstat and fingerprint outputs", True, "multiqc_sources.txt"),
  A("--JSDsample claim consistent with installed deepTools 4.0.0", True, "plotFingerprint --help")]),
 dict(type="Variant B", label="preseq c_curve/lc_extrap recipes on paired-end ATAC BAM", status="PARTIAL", flag="❌",
      note="Documented commands omit -P; c_curve -s 1e6 returns header only on a library under 1M fragments",
      basic=27, spec=34, a=[
  A("lc_extrap returns finite monotone yield curve with ordered CI", True, "plateau about 1.2M distinct"),
  A("Skill-literal c_curve returns a curve on the test BAM", False, "header row only (t_pre.log)"),
  A("Documented commands are correct for paired-end BAM without extra flags", False, "-P merges mates: 500,001 distinct of 524,024 vs 305,029 without -P on the deduplicated BAM (t_pre3.log)"),
  A("Paired-end mode works on a coordinate-sorted BAM", True, "c_curve -B -P ran; name-sorted input fails")]),
 dict(type="Edge", label="Planted-truth silent-failure probes for TSS and complexity scripts", status="COMPLETED", flag="❌",
      note="Minus-strand gene intervals and absent chromosomes give wrong or zero scores with exit 0; chrM and MAPQ0 reads counted",
      basic=24, spec=28, a=[
  A("1 bp plus-strand TSS on planted bigWig returns the planted 21.0", True, "run2.log cases A, C, D, G"),
  A("Minus-strand gene interval (start,end) is scored at its true TSS", False, "1.0 vs 21.0 planted"),
  A("Chromosome absent from the bigWig raises an error rather than 0.0", False, "exit 0, TSS_enrichment 0.0 (also empty BED)"),
  A("Unindexed BAM fails with an explicit error", True, "ValueError: fetch called on bamfile without index"),
  A("chrM and MAPQ 0 reads are excluded from NRF/PBC", False, "planted BAM total 300, NRF 0.34")]),
]
inputs = []
for i, x in enumerate(raw, 1):
    a = x["a"]
    inputs.append({
        "index": i, "type": x["type"], "label": x["label"], "status": x["status"], "status_flag": x["flag"],
        "note": x["note"], "basic": x["basic"], "specialized": x["spec"], "total": x["basic"] + x["spec"],
        "assertions_passed": sum(t["result"] == "PASS" for t in a), "assertions_total": len(a), "assertions": a})

cats = {
 "functional_suitability": (8, 12, "Workflow covers the seven ENCODE metrics, but documented NRF/PBC filters, periodicity classification and per-sample MultiQC output are not delivered by the shipped scripts"),
 "reliability": (8, 12, "Some inputs fail loudly, but absent chromosomes, empty TSS BEDs and minus-strand gene intervals return 0.0 or wrong values with exit 0"),
 "performance_context": (7, 8, "SKILL.md is about 11 KB with routed references; thresholds and failure modes are deferred correctly"),
 "agent_usability": (12, 16, "Clear workflow and thresholds; bigWig construction, preseq -P and the TSS BED contract require inference"),
 "human_usability": (6, 8, "Usage guide has prompts and tips; no worked sample-level example or expected output layout"),
 "security": (11, 12, "No credentials, shell injection or destructive operations; scripts only read supplied paths"),
 "maintainability": (9, 12, "Small modular scripts with docstrings; no tests or fixtures shipped; Pearson vs Spearman contradiction in references"),
 "agent_specific": (15, 20, "Trigger description is precise and version-drift guidance present; several documented behaviors do not match the scripts"),
}
sub = sum(v[0] for v in cats.values())
avg = round(sum(x["total"] for x in inputs) / len(inputs), 1)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = int(round(sw + dw))

findings = [
 ("ATAC-QC-001", "P1", "library_complexity.py NRF/PBC are single-end read-start metrics, not ENCODE fragment metrics", [2],
  "On paired-end ATAC BAMs the script keys each mate by (chr, start, strand). Unfiltered rep1: 0.353/0.632/3.40 vs independent fragment NRF/PBC1/PBC2 0.619/0.767/4.87 (MAPQ>=30: 0.779/0.799/5.10); the ENCODE-filtered deduplicated BAM gives 0.573 instead of the 1.0 the Skill states. Grading against the 0.7 reject line would fail acceptable libraries.",
  "Skill defines NRF over reads/positions and the script never pairs mates.",
  "Compute on fragments (chr, fragment start, end) for paired-end input, keep a single-end mode, use 5-prime coordinates for reverse reads, and state definition and units in SKILL.md and method-reference.md.",
  "audit-run/out/run_all.log; audit-run/scripts/frag_nrf.py"),
 ("ATAC-QC-002", "P2", "library_complexity.py ignores documented MAPQ>=30, chrM exclusion and duplicate flags", [2, 7],
  "Docs say NRF/PBC run after MAPQ>=30 filtering; a planted BAM with 100 unique nuclear reads plus 100 chrM and 100 MAPQ0 duplicates returned total 300, NRF 0.34 instead of 100 and 1.0.",
  "Filtering is left to an undocumented pre-step and the script has no options.",
  "Add --min-mapq and contig-exclusion defaults matching the Skill, or state the required pre-filter command.",
  "audit-run/out/run2.log"),
 ("ATAC-QC-003", "P2", "aggregate_qc.py output is not per-sample or MultiQC-compatible and silently skips metrics", [4],
  "Long-format metric/value/flag TSV; MultiQC custom content parsed 7 metric rows as 7 samples. No sample column, no overall grade, missing metrics produce no row, string values raise TypeError.",
  "Docs describe a per-sample report card and _mqc.tsv that the script does not write.",
  "Emit a sample-wide _mqc.tsv with headers and an overall grade, report missing required metrics as NA, validate numeric types, or correct the documentation.",
  "audit-run/out/run2.log"),
 ("ATAC-QC-004", "P2", "encode_tss_enrichment.py returns wrong or zero scores with exit 0 on plausible input mistakes", [7],
  "Planted bigWig with true score 21.0: minus-strand gene interval (start,end) scored 1.0 because start is used as TSS; a chromosome absent from the bigWig and an empty BED both return 0.0 with success; strand is read from the last column so a name column after strand defaults to plus; used and skipped TSS counts are never reported.",
  "Input contract is only 'chrom start end ... strand' and skipped TSS are swallowed.",
  "Document that the BED must be 1 bp TSS with strand in column 6, read column 6, report used/skipped TSS counts, and exit nonzero when none are used.",
  "audit-run/out/run2.log"),
 ("ATAC-QC-005", "P2", "TSS bigWig recipe undocumented; score depends on it; pyTSSe equivalence unvalidated", [1],
  "Same BAM and TSS set gives 11.32 (bamCoverage --extendReads), 14.92 (plain), 15.98 (--Offset 1) and 11.48 (CPM, bin 10). Skill and usage guide call the script the ENCODE pyTSSe convention but give no bigWig command and no comparison to ENCODE-reported values.",
  "Signal-track construction is a hidden parameter of the metric.",
  "Add the exact bamCoverage command (bin size 1, chosen read representation), state the ENCODE reference method or soften the pyTSSe equivalence, and note that scores differ by recipe.",
  "audit-run/out/t_bw.log"),
 ("ATAC-QC-006", "P2", "preseq recipes omit -P for paired-end BAMs; c_curve step can give header-only output", [6],
  "On the deduplicated paired BAM c_curve without -P reports 305,029 distinct of 500,000 reads while -P reports 500,001 of 524,024. Without -P preseq counted 929,546 reads for 1.82M mates. c_curve -s 1e6 returns only the 0 0 row when depth is below the step; -P fails on name-sorted input.",
  "Commands were copied from single-end preseq usage.",
  "Use -B -P on a coordinate-sorted BAM for paired-end ATAC, state that deduplicated BAMs are unsuitable for lc_extrap, and set the step relative to depth.",
  "audit-run/out/t_pre.log; audit-run/out/t_pre3.log"),
 ("ATAC-QC-007", "P2", "atac_qc_metrics.R does not classify periodicity and labels all MAPQ>=30 pairs as nuclear reads", [3],
  "Workflow step 3 and the usage guide promise periodicity classification; the script only counts NFR/mono/di/tri. nuclear_reads_M counts pairs including chrM and duplicates yet is graded against the ENCODE nuclear-read threshold.",
  "Metric naming and documentation overstate what the script computes.",
  "Implement the documented pattern classification and chrM/duplicate exclusion, or rename the field and correct the docs.",
  "audit-run/out/run_all.log (R run in evidence/smoke_r.log)"),
 ("ATAC-QC-008", "P3", "atac_qc_metrics.R input contract: .bed.gz narrowPeak fails cryptically; hg38 hard-coded", [3],
  "ENCODE narrowPeak distributed as .bed.gz fails with scan() expected an integer, got 22.06932. TxDb hg38 is fixed with no genome argument or seqlevels check.",
  "rtracklayer infers format from the extension.",
  "Pass format='narrowPeak' to import or document supported extensions; expose the genome/TxDb as an argument.",
  "audit-run/out/rbed/"),
 ("ATAC-QC-009", "P3", "library_complexity.py emits non-standard JSON Infinity for PBC2", [4],
  "All-singleton BAM prints PBC2 Infinity, rejected by strict JSON parsers.",
  "json.dumps default allows non-finite floats.",
  "Emit null or a string when PBC2 is undefined.", "audit-run/out/run2.log"),
 ("ATAC-QC-010", "P3", "Reference inconsistencies and unverified threshold attribution", [],
  "method-reference.md says Pearson correlation on binned counts while the recipe and tips use Spearman; NRF/PBC 0.7-0.9 bands are attributed to Landt 2012 although the Skill says the PBC1/PBC2 split is a later refinement (not verified against ENCODE pages in this pass); the usage guide lists a Picard insert-size step with no command in the Skill; prerequisites omit preseq.",
  "Compiled from several sources without reconciliation.",
  "Reconcile to Spearman, verify each threshold against the current ENCODE ATAC standards and cite the exact source, add the Picard command and preseq install line.",
  "static review of SKILL.md and references/"),
]

report = {
 "meta": {"skill_name": "bio-atac-seq-atac-qc",
          "description": "ATAC-seq library quality control -- TSS enrichment, FRiP, fragment-size periodicity, library complexity (NRF/PBC1/PBC2), mitochondrial fraction, and ENCODE 4 thresholds.",
          "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
          "execution_mode": "B", "complexity": "Complex", "n_inputs": len(inputs)},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated citations or values observed; attribution of the 0.7-0.9 NRF/PBC bands to Landt 2012 is unverified and filed as P3 ATAC-QC-010"},
   "practice_boundaries": {"result": "PASS", "detail": "QC guidance for research data; no clinical claims"},
   "methodological_ground": {"result": "PASS", "detail": "NRF/PBC on single-end read starts is a serious method mismatch (ATAC-QC-001, P1) but implements the Skill's literal stated definition and is not a correlation/causation-class fallacy; escalated as P1 rather than veto"},
   "code_usability": {"result": "PASS", "detail": "All four scripts and the CLI recipes ran on numpy 2.5, pandas 3.0 and deepTools 4.0 without modification"}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100,
   "assertion_pass_rate": {"passed": sum(x["assertions_passed"] for x in inputs), "total": sum(x["assertions_total"] for x in inputs)},
   "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only",
           "grade_symbol": "⚠️", "deployable": False, "veto_override": False},
 "key_strengths": [
  "TSS enrichment script agrees with independent deepTools computation on real ENCODE data (11.38 vs 11.39)",
  "Threshold table, TSS-implementation comparison and failure-mode reference are substantive and mostly accurate",
  "CLI recipes (Picard, deepTools fingerprint/correlation, MultiQC) execute and produce plausible values",
  "Scripts are small, dependency-light and run unchanged on current numpy/pandas/deepTools majors"],
 "recommendations": [{"priority": ("P2" if p == "P3" else p), "title": (t if len(t) <= 60 else t[:57] + "..."), "observed_in": o, "problem": pr, "root_cause": rc, "fix": fx}
                     for (i, p, t, o, pr, rc, fx, e) in findings],
}
json.dump(report, open(os.path.join(R, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
json.dump([dict(id=i, severity=p, state="open", title=t, observed_in=o, problem=pr, root_cause=rc, fix=fx, evidence=e)
           for (i, p, t, o, pr, rc, fx, e) in findings],
          open(os.path.join(R, "findings.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(sub, avg, sw, dw, score, report["dynamic_score"]["assertion_pass_rate"], [x["total"] for x in inputs])
