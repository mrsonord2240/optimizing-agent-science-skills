import json
desc = "Call accessible chromatin regions from ATAC-seq BAM files using MACS3, MACS2, Genrich, or HMMRATAC. Use when identifying open chromatin from aligned ATAC-seq, choosing between point-source vs HMM peak callers, applying ENCODE-style pseudoreplicate IDR, removing blacklist regions, or fixing 501bp consensus peaks for downstream differential analysis."


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


def inp(i, typ, label, status, flag, note, b, s, asr):
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note,
            "basic": b, "specialized": s, "total": b + s,
            "assertions_passed": sum(a["result"] == "PASS" for a in asr), "assertions_total": len(asr),
            "assertions": asr}


inputs = [
    inp(1, "Canonical", "ENCODE-style script on GM12878 rep1/rep2 chr1:1-30Mb (passing library, MACS3, bigWig)", "COMPLETED", "✅",
        "Nt=1197 N1=1143 N2=1249 Np=1036, rescue 1.155, self 1.093, PASS; 1,188 blacklist-free conservative peaks; matches the disjoint reference from the initial audit", 37, 55, [
            A("Script exits 0 and writes per-replicate, pooled, six pseudoreplicate, four IDR, plot, conservative and bigWig outputs", "PASS",
              "All present; rep1 4,803, rep2 4,366, pooled 4,310 peaks; four IDR PNGs (true_reps plot inspected, legible)"),
            A("Reported Nt, N1, N2, Np equal an independent recount of IDR rows with score >= 540 and the verdict follows the ENCODE rule", "PASS",
              "Recount 1197/1143/1249/1036 identical; every row score >= 540; rescue 1.155 and self 1.093 both <= 2 give PASS"),
            A("Pseudoreplicate halves are disjoint and keep pairs together (rep1 re-split)", "PASS",
              "524,024 read names, 0 shared, union equals all; every name appears twice in each half where present"),
            A("Conservative set is 10-column narrowPeak, has no blacklist overlap and agrees with ENCODE IDR peaks", "PASS",
              "1,188 rows, 0 overlaps with the v2 blacklist, 1,059 overlap ENCODE ENCFF346CZA; 2,194 of 2,566 slice ENCODE peaks recovered"),
            A("pooled.bw is a valid bigWig whose signal matches the pooled bedGraph", "PASS",
              "Header readback: version 4, basesCovered 29,998,866, max 7,458.77, mean 5.0, identical to the bedGraph")]),
    inp(2, "Variant A", "Genuinely failing library (rep2 = 6% subsample), ratio-logic unit cases, MACS=macs2 mode", "COMPLETED", "✅",
        "Failing library gives Nt=495 N1=1143 N2=233 Np=1680, rescue 3.394, self 4.906, FAIL; MACS2 mode byte-identical to MACS3; first attempt hit a transient drvfs read error under 3 concurrent runs", 36, 54, [
            A("A poorly reproducible library is reported FAIL with both ratios above 2", "PASS",
              "Recount of IDR rows 495/1143/233/1680 matches the script; rescue 3.394, self 4.906, verdict FAIL"),
            A("The ratio/verdict block returns PASS, BORDERLINE (either ratio), FAIL, inf handling and the exactly-2.0 boundary correctly", "PASS",
              "7 synthetic IDR-file cases, block extracted from the shipped script; all verdicts as expected"),
            A("MACS=macs2 (with the env shim) reproduces the MACS3 result", "PASS",
              "idr/true_reps.idr, reproducibility.txt and conservative.narrowPeak byte-identical; rep1 4,803 peaks in both"),
            A("The failing-library run completes on its first attempt", "FAIL",
              "samtools merge reported a truncated intermediate BAM (BGZF read error at ~4 MiB) while 3 pipelines ran concurrently on drvfs; identical rerun completed. Not reproduced in 4 other runs; treated as an environment I/O flake")]),
    inp(3, "Variant B", "Documented Genrich joint and macs3 hmmratac commands on GM12878", "COMPLETED", "✅",
        "Genrich 14,498 peaks with blacklist, 14,328 without; hmmratac 2,064 regions with model and cutoff files", 34, 53, [
            A("The usage-guide name-sorted Genrich joint command runs and yields peaks", "PASS", "rc 0, 14,498 peaks with -E blacklist"),
            A("Coordinate-sorted input aborts as the Skill states", "PASS", "Error: SAM/BAM file not sorted by queryname"),
            A("The hmmratac command runs and writes the documented outputs", "PASS",
              "rc 0; _accessible_regions.narrowPeak (2,064 regions, mean width 300 bp), _model.json, _cutoff_analysis.tsv"),
            A("The reconciliation-table Genrich count is reproducible", "PASS",
              "14,328 peaks at -q 0.05 without -E reproduces the quoted figure; the blacklist run gives 14,498")]),
    inp(4, "Edge", "Input guards, chrM guard on a synthetic BAM, idxstats chrM-removal recipe", "COMPLETED", "✅",
        "Eight guard cases exit 1 with named errors; chrM guard verified only on a planted 3-read fixture because source BAMs have no chrM reads", 35, 51, [
            A("Missing genome size, missing argument, missing/unindexed/unsorted BAM, missing blacklist, missing tool and bad chrom.sizes each exit 1 with a specific message", "PASS",
              "8 of 8 rc=1, no output directory created for the argument errors"),
            A("A BAM with chrM reads is refused", "PASS",
              "Synthetic BAM (3 planted chrM reads, real chrM header): 'has 3 reads on the mitochondrial contig', rc 1"),
            A("The documented idxstats contig-selection recipe removes chrM reads and keeps header and other reads", "PASS",
              "Synthetic pair BAM: chr1 pairs kept, chrM reads removed, header kept; a chr1 read whose mate maps to chrM stays as an orphan (see ATACPC-016)")]),
    inp(5, "Variant B", "Corrected two-environment install recipe and NFR-only recipe", "COMPLETED", "✅",
        "Both create lines solve; the old bioconda-only line still fails; fresh-environment execution reused from the identity-matched delta pass", 34, 51, [
            A("Both documented micromamba create lines solve", "PASS",
              "Dry-run rc 0 each: macs3 3.0.4, Genrich 0.6.2, samtools 1.24, bedtools 2.31.1, bedGraphToBigWig 482; idr 2.0.4.2 with numpy 1.23.5. Delta pass ran real fresh installs and the script in them (reused, same bytes)"),
            A("The superseded bioconda-only line fails to solve, confirming the correction was needed", "PASS",
              "dry-run rc 1: macs3 requires hmmlearn conflict"),
            A("The NFR-only recipe runs and calls peaks", "PASS",
              "322,156 short-fragment reads; 10,951 peaks, identical to the initial audit")]),
]
avg = round(sum(i["total"] for i in inputs) / 5, 1)
sub = 11 + 10 + 7 + 14 + 7 + 11 + 10 + 15
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
rep = {
    "meta": {"skill_name": "bio-atac-seq-atac-peak-calling", "description": desc, "evaluated_on": "2026-09-30",
             "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D",
             "complexity": "Moderate", "n_inputs": 5},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True, "gate": "PASS",
            "scientific_integrity": {"result": "PASS", "detail": "All reported counts and ratios recomputed independently; untested claims (30M-read HMMRATAC depth, ROSE, whole genome, mm10) are labelled as untested or illustrative"},
            "practice_boundaries": {"result": "PASS", "detail": "Research-only genomics Skill, no clinical conclusions"},
            "methodological_ground": {"result": "PASS", "detail": "Disjoint pseudoreplicates and the ENCODE rescue and self-consistency rule now match encode_task_reproducibility.py; genuine passing and failing libraries give the correct verdicts"},
            "code_usability": {"result": "PASS", "detail": "Script ran to completion in three modes (MACS3 pass, MACS2 pass, MACS3 failing library) and its guards refuse bad inputs"}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {
        "functional_suitability": {"score": 11, "max": 12, "note": "Workflow, script and references agree; ratio rule, pseudoreplicates, install and caller commands verified; description still names 501 bp consensus peaks the Skill does not build"},
        "reliability": {"score": 10, "max": 12, "note": "Input, index, sort, chrM, tool and argument guards work; no handling shown for degenerate libraries where IDR itself aborts; one transient I/O failure under load"},
        "performance_context": {"score": 7, "max": 8, "note": "SKILL.md is short with routed references; method-reference.md is 20 KB but sectioned"},
        "agent_usability": {"score": 14, "max": 16, "note": "Clear workflow, tested Genrich and hmmratac commands, verdict printed to reproducibility.txt; needs two environments and a wrapper or IDR variable"},
        "human_usability": {"score": 7, "max": 8, "note": "Consistent single-sample and IDR guidance, decision tables and prompts; long reference file"},
        "security": {"score": 11, "max": 12, "note": "Expansions quoted, no credentials or destructive operations; blacklist download has no checksum"},
        "maintainability": {"score": 10, "max": 12, "note": "License and provenance kept, tested versions stated accurately; ROSE, HOMER, chromap, whole-genome and mm10 unverified"},
        "agent_specific": {"score": 15, "max": 20, "note": "Rich trigger description, ENCODE differences disclosed; description overreaches on consensus peaks and testing covers one chr1 slice of one cell line"}}},
    "dynamic_score": {"execution_avg": avg, "max": 100,
                      "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs),
                                              "total": sum(i["assertions_total"] for i in inputs)},
                      "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": round(sw + dw), "max": 100,
              "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False},
    "key_strengths": [
        "Pseudoreplicate and Nt/Nself logic now reproduces the ENCODE definitions: disjoint halves (0 shared reads), Nt/N1/N2/Np at one IDR threshold, and correct PASS and FAIL verdicts on a real passing and a genuinely failing library",
        "The corrected two-environment install solves and the superseded one-line install demonstrably does not; MACS2 and MACS3 modes give byte-identical outputs",
        "Input guards fail fast with named errors, and outputs (conservative narrowPeak, pooled bigWig, IDR plots) were inspected and cross-checked against ENCODE peaks and the bedGraph",
        "Genrich and hmmratac commands are now tested and their reconciliation figures reproduce"],
    "recommendations": [
        {"priority": "P2", "title": "Trim description claim of 501bp consensus peaks (ATACPC-015)", "observed_in": [],
         "problem": "The description advertises fixing 501bp consensus peaks but the Skill only mentions the Corces re-centering convention and routes to consensus-peakset.",
         "root_cause": "Trigger text inherited from upstream.",
         "fix": "Reword to point to atac-seq/consensus-peakset for fixed-width peaks, or state that only re-centering is described."},
        {"priority": "P2", "title": "ROSE snippet remains unexecuted (ATACPC-012)", "observed_in": [],
         "problem": "The ROSE_main.py and GFF conversion are labelled illustrative but were never run because ROSE is not installed.",
         "root_cause": "Optional, outside the primary workflow.",
         "fix": "Keep the illustrative label, or execute it in a ROSE environment before dropping the label."},
        {"priority": "P2", "title": "State orphan-mate behaviour of the chrM recipe (ATACPC-016)", "observed_in": [4],
         "problem": "The idxstats contig-selection recipe keeps a chr1 read whose mate maps to chrM, leaving a paired-flag orphan that the chrM guard cannot see.",
         "root_cause": "Selection is by the read's own contig only.",
         "fix": "Add one sentence, or filter by RNEXT as well, when using BAMPE or hmmratac downstream."}]}
json.dump(rep, open('report.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(avg, sub, sw, dw, rep["final"]["score"], rep["dynamic_score"]["assertion_pass_rate"],
      sum(i["basic"] for i in inputs) / 5, sum(i["specialized"] for i in inputs) / 5)
