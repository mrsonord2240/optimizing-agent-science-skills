#!/usr/bin/env python3
"""Build the delta report.json for bio-atac-seq-atac-peak-calling from the prior certified
report (candidate@b19054ded9df-reaudit-run). Only the dimensions and the assertion the delta
touches are re-scored; the final score is recomputed with the skill-auditor rubric
(final = 0.4 x static + 0.6 x execution average)."""
import json, sys

prior_path, out_path, real_note = sys.argv[1], sys.argv[2], sys.argv[3]
r = json.load(open(prior_path, encoding="utf-8"))
m = r["meta"]
m["evaluated_on"] = "2026-09-30"
m["description"] = ("Call accessible chromatin regions from ATAC-seq BAM files using MACS3, MACS2, Genrich, "
                    "or HMMRATAC. Use when identifying open chromatin from aligned ATAC-seq, choosing between "
                    "point-source vs HMM peak callers, applying ENCODE-style pseudoreplicate IDR, removing "
                    "blacklist regions, or re-centering peaks on summits for downstream differential analysis.")
assert m["category"] == "Data Analysis"

rv = r["veto_gates"]["research_veto"]
rv["scientific_integrity"]["detail"] = (
    "All reported counts and ratios recomputed independently; untested claims (30M-read HMMRATAC depth, whole "
    "genome, mm10) are labelled as untested or illustrative; the unexecuted ROSE snippet is gone and super-enhancer "
    "calling is correctly scoped to ChIP signal")

c = r["static_score"]["categories"]
c["functional_suitability"].update(score=12, note=(
    "Workflow, script and references agree; ratio rule, pseudoreplicates, install and caller commands verified; "
    "description now names summit re-centering, which the references describe, instead of 501 bp consensus peaks "
    "(ATACPC-015 resolved)"))
c["agent_specific"].update(score=16, note=(
    "Rich trigger description that now matches the Skill's scope; ENCODE differences disclosed; testing covers one "
    "chr1 slice of one cell line"))
c["maintainability"].update(score=10, note=(
    "License and provenance kept, tested versions stated accurately; unexecuted ROSE snippet replaced by a pointer "
    "(ATACPC-012 resolved), but the pointer names bio-chipseq-super-enhancers, which is not on this shelf; HOMER, "
    "chromap, whole-genome and mm10 unverified"))
r["static_score"]["subtotal"] = sum(x["score"] for x in c.values())

inp = {i["index"]: i for i in r["dynamic_score"]["inputs"]}
e = inp[4]
e["label"] = "Input guards, chrM guard on a synthetic BAM, idxstats chrM-removal recipe and its -f 2 orphan follow-up"
e["note"] = ("Eight guard cases exit 1 with named errors; chrM guard verified only on a planted 3-read fixture because "
             "source BAMs have no chrM reads; the documented -f 2 follow-up verified on aligner-flagged synthetic "
             "pairs and on real ENCODE GM12878 orphans")
e["assertions"][2]["note"] = ("Synthetic pair BAM: chr1 pairs kept, chrM reads removed, header kept; a chr1 read whose "
                              "mate maps to chrM stays as an orphan, as the usage guide now states")
e["assertions"].append({
    "text": "The documented `samtools view -b -f 2` follow-up removes chrM-mate orphans and keeps pairs intact",
    "result": "PASS",
    "note": real_note,
})
e["assertions_passed"], e["assertions_total"] = 4, 4
e["specialized"] = 52
e["total"] = e["basic"] + e["specialized"]

ins = r["dynamic_score"]["inputs"]
avg = round(sum(i["total"] for i in ins) / len(ins), 1)
r["dynamic_score"]["execution_avg"] = avg
r["dynamic_score"]["assertion_pass_rate"] = {
    "passed": sum(i["assertions_passed"] for i in ins), "total": sum(i["assertions_total"] for i in ins)}
for i in ins:
    assert i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["assertions_total"] == len(i["assertions"])
    assert i["total"] == i["basic"] + i["specialized"]

s = r["static_score"]["subtotal"]
f = r["final"]
f["static_weighted"] = round(0.4 * s, 1)
f["dynamic_weighted"] = round(0.6 * avg, 1)
f["score"] = round(0.4 * s + 0.6 * avg)
assert f["score"] >= 85 and f["grade"] == "Production Ready" and not f["veto_override"]

r["key_strengths"][3] = ("Genrich and hmmratac commands are tested and their reconciliation figures reproduce; the chrM "
                         "orphan-mate note and its -f 2 follow-up hold on real ENCODE data")
r["recommendations"] = [{
    "priority": "P2",
    "title": "Super-enhancer pointer targets a Skill not on this shelf",
    "observed_in": [],
    "problem": ("method-reference.md routes super-enhancer work to `bio-chipseq-super-enhancers`, which exists upstream "
                "(GPTomics chip-seq/super-enhancers) and covers every topic listed, but is not shipped on this shelf. "
                "Two unchanged lines (usage-guide Tips, method-reference broad-mode trigger) still list super-enhancers "
                "among --broad targets."),
    "root_cause": "Cross-reference written against the upstream collection.",
    "fix": ("Ship or name the upstream path of the super-enhancer Skill, or add one clause saying it is optional; "
            "optionally reword the two residual lines to 'super-enhancer overlap' only."),
}]
assert all(x["priority"] in ("P0", "P1", "P2") for x in r["recommendations"])

json.dump(r, open(out_path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
open(out_path, "a", encoding="utf-8", newline="\n").write("\n")
print(f"static={s} exec={avg} final={f['score']} ({f['static_weighted']}+{f['dynamic_weighted']}) grade={f['grade']} "
      f"assertions={r['dynamic_score']['assertion_pass_rate']} recs={[x['priority'] for x in r['recommendations']]}")
