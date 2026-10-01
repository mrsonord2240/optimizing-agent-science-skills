"""Build delta-cat-20260930 report.json and source-identity.json from the prior certified re-audit.

Usage: python build_delta.py <skill_id>
Copies the prior report.json structure exactly, then updates only the scores, notes, assertions and
recommendations the delta touches; writes source-identity.json modelled on the prior run's.
Final = 0.4 x static + 0.6 x execution average (skill-auditor@1.0), same gates and floors.
"""
import copy
import glob
import json
import os
import sys

SID = sys.argv[1]
PRIOR_DIR = glob.glob(f"F:/optimizing-agent-science-skills/audits/skills/{SID}/candidate@*-reaudit-run")[0]
RUN = f"F:/OpenScience/audits/{SID}/delta-cat-20260930"
WT = {"bio-atac-seq-differential-accessibility": "atac-differential-accessibility",
      "bio-atac-seq-motif-deviation": "atac-motif-deviation",
      "bio-atac-seq-nucleosome-positioning": "atac-nucleosome-positioning"}[SID]
CAND = f"F:\\OpenScience\\wt\\{WT}\\skills\\{SID}"
EXPECTED = {"bio-atac-seq-differential-accessibility": "678737f8a1672087f240de16908c4b4362ff650a6e0df8ecea6cc21e4a1a0184",
            "bio-atac-seq-motif-deviation": "9e4cce81ace8ed64e685173ec67852c56f25adc2b015da0c395456e54ee30e07",
            "bio-atac-seq-nucleosome-positioning": "c8ef5320a0fa4a07ef8c801303862c0e6334c584103b267eeb2bda6c5303fa3d"}[SID]

prior = json.load(open(f"{PRIOR_DIR}/report.json", encoding="utf-8"))
psrc = json.load(open(f"{PRIOR_DIR}/source-identity.json", encoding="utf-8"))
ident = json.load(open(f"{RUN}/logs/identity.json", encoding="utf-8"))
assert ident["candidate_identity"] == EXPECTED, "identity mismatch"
rep = copy.deepcopy(prior)
rep["meta"]["evaluated_on"] = "2026-09-30"
cats = rep["static_score"]["categories"]
inputs = {i["index"]: i for i in rep["dynamic_score"]["inputs"]}


def assertion(idx, n):
    return inputs[idx]["assertions"][n]


def rec(title_prefix):
    return next(r for r in rep["recommendations"] if r["title"].startswith(title_prefix))


# ---------------------------------------------------------------- per-skill delta
if SID == "bio-atac-seq-differential-accessibility":
    cats["agent_usability"].update(score=15, note=(
        "Clear workflow and CLI header; SKILL.md step 5 now states the --sva limits, but "
        "method-reference still says --sva runs inside DiffBind"))
    cats["maintainability"].update(score=11, note=(
        "Versions stated and satisfied, license and provenance preserved; default-vs-SVA threshold "
        "semantics now documented in SKILL.md"))
    cats["agent_specific"].update(score=17, note=(
        "Precise description; body matches the shipped script and SKILL.md now documents SVA-mode "
        "limits; Outputs line still lists the heatmap without the SVA qualifier"))
    a = assertion(2, 3)
    a["note"] = ("Runtime unchanged (script bytes identical to the certified run): no blacklist step, hard "
                 "|LFC|>=1 filter instead of the lfcThreshold test, no heatmap. Now documented in SKILL.md "
                 "step 5 (delta-cat), but the assertion is behavioural and still fails")
    rep["veto_gates"]["research_veto"]["methodological_ground"]["detail"] = (
        "Surrogate variables verified to enter the DESeq2 design and change results; documented design "
        "restriction verified; SVA-mode limits now documented in SKILL.md and checked against the code; "
        "residual runtime and reference inconsistencies are P2")
    rep["key_strengths"].append(
        "SKILL.md now states the --sva mode's direct DESeq2 fit, ignored flags, skipped blacklist/heatmap, "
        "hard post-filter and small-n cap; each statement checked against the script and prior evidence")
    r1 = rec("SVA mode skips blacklist")
    r1["title"] = "SVA mode skips blacklist filter with no runtime warning"
    r1["problem"] = ("--sva fits DESeq2 on dba.count output and never runs the DiffBind blacklist step that the "
                     "default path applies in dba.analyze; SKILL.md step 5 now says so, but the run prints no "
                     "warning and genome-wide input could report blacklisted regions (0 of 2260 intervals on "
                     "the audit slice).")
    r1["fix"] = "Call dba.blacklist with the genome-matched blacklist before the SVA fit, or warn at runtime."
    r2 = rec("SVA-mode limits documented only")
    r2["title"] = "method-reference contradicts SKILL.md on where --sva runs"
    r2["problem"] = ("SKILL.md step 5 now says --sva fits DESeq2 directly, but references/method-reference.md "
                     "line 149 still says the script does this 'inside DiffBind'; --method is still ignored "
                     "silently at runtime (--design prints a message).")
    r2["root_cause"] = "The delta edited SKILL.md only; the reference sentence and runtime warning were not updated."
    r2["fix"] = ("Change method-reference line 149 to 'fits DESeq2 directly on the DiffBind counts' and warn "
                 "when --method is passed with --sva.")
    rep["recommendations"].remove(rec("Effect-size threshold semantics"))
    r4 = rec("Non-human TxDb untested")
    r4["title"] = "Non-human TxDb untested"
    r4["observed_in"] = [7]
    r4["problem"] = ("--txdb=<package> was executed only for none because no non-human TxDb was installed; "
                     "the SVA small-n caution is now in SKILL.md step 5.")
    r4["root_cause"] = "Only hg38 annotation packages were installed in the audit environment."
    r4["fix"] = "Validate one non-model-organism TxDb package when available."

elif SID == "bio-atac-seq-motif-deviation":
    cats["functional_suitability"].update(score=12, note=(
        "Bulk, Signac and ArchR routes execute and reproduce known biology; the z-score magnitude claim "
        "now matches the measured run"))
    cats["maintainability"].update(score=11, note=(
        "License and provenance preserved; tested stack stated; Bioc 3.23 not run"))
    a = assertion(1, 4)
    a["result"] = "PASS"
    a["note"] = ("SKILL.md now says the top motifs 'reached |z| of about 7 per sample'; certified runs bulk_A "
                 "and bulk_B (script byte-identical to the candidate) give per-sample max |z| 6.61-7.24, "
                 "0 values above 9; 742-motif count unchanged")
    i1 = inputs[1]
    i1["assertions_passed"] = 5
    i1["specialized"] = 54
    i1["total"] = i1["basic"] + i1["specialized"]
    i1["note"] = "Exit 0 twice, CSVs byte-identical; biology correct; SKILL.md numbers match the run"
    rep["veto_gates"]["research_veto"]["scientific_integrity"]["detail"] = (
        "No fabricated values; unexecuted paths and heuristics are labelled; the wrong z-score number "
        "(MOTDEV-013) is corrected to |z| about 7 and re-verified against the certified run outputs")
    rep["recommendations"].remove(rec("Correct the 'top motifs exceeded 9'"))

elif SID == "bio-atac-seq-nucleosome-positioning":
    cats["reliability"]["note"] = (
        "Failure guards present and exercised; NRL plateau ambiguity remains; export/summary count "
        "mismatch now has a script comment, but the comment misstates the cause")
    a = assertion(3, 5)
    a["note"] = ("Runtime unchanged. NFR BAM 141,651 pairs vs nfr_count 130,774; mono 64,579 vs 67,604. "
                 "Exports equal fixed right-closed windows (0,100] and (180,247] on 9 bp-shorter Tn5-shifted "
                 "fragments exactly; the new comment calls them model-based, which they are not without a "
                 "conservation argument (NUCPOS-017)")
    r = rec("R exports and summary CSV")
    r["problem"] = ("Exported NFR/mono BAM pair counts differ from nfr_count/mono_count (141,651 vs 130,774; "
                    "64,579 vs 67,604). The new script comment attributes this to 'splitGAlignmentsByCut's "
                    "model-based classes', but the script passes no conservation score, so ATACseqQC 1.30.0 "
                    "returns a plain cut(abs(isize)) split; recounting the input with widths minus 9 bp "
                    "reproduces both export counts exactly.")
    r["root_cause"] = ("Counts use unshifted widths with closed windows; exports use Tn5-shifted isize "
                       "(9 bp shorter) with right-closed cut() breaks. The random-forest path runs only when "
                       "conservation is supplied.")
    r["fix"] = ("Reword the comment: exports are split by the same size windows after the Tn5 shift "
                "(fragments 9 bp shorter, right-closed breaks); or compute the summary from the exported "
                "classes. (NUCPOS-017)")

# ---------------------------------------------------------------- recompute totals and grade
st = sum(c["score"] for c in cats.values())
rep["static_score"]["subtotal"] = st
ins = rep["dynamic_score"]["inputs"]
ex = round(sum(i["total"] for i in ins) / len(ins), 1)
rep["dynamic_score"]["execution_avg"] = ex
passed = sum(i["assertions_passed"] for i in ins)
total = sum(i["assertions_total"] for i in ins)
rep["dynamic_score"]["assertion_pass_rate"] = {"passed": passed, "total": total}
sw, dw = round(0.4 * st, 1), round(0.6 * ex, 1)
score = round(0.4 * st + 0.6 * ex)
grade, sym = (("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75
              else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌"))
l1 = sum(i["basic"] for i in ins) / len(ins)
l2 = sum(i["specialized"] for i in ins) / len(ins)
floors = {"static>=80": st >= 80, "exec>=85": ex >= 85, "L1>=32": l1 >= 32, "L2>=48": l2 >= 48,
          "assert>=90%": passed / total >= 0.9}
assert all(floors.values()), floors
assert all(r["priority"] in ("P0", "P1", "P2") for r in rep["recommendations"])
rep["final"].update(static_weighted=sw, dynamic_weighted=dw, score=score, grade=grade, grade_symbol=sym,
                    deployable=True, veto_override=False)


def keys(o):
    if isinstance(o, dict):
        return {k: keys(v) for k, v in o.items()}
    if isinstance(o, list):
        return [keys(o[0])] if o else []
    return type(o).__name__


assert keys(rep["meta"]) == keys(prior["meta"]) and set(rep) == set(prior)
assert keys(rep["static_score"]) == keys(prior["static_score"])
assert keys(rep["dynamic_score"]) == keys(prior["dynamic_score"])
assert keys(rep["final"]) == keys(prior["final"])
json.dump(rep, open(f"{RUN}/report.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
print(f"{SID}: static {st} exec {ex} L1 {l1:.1f} L2 {l2:.1f} assertions {passed}/{total} "
      f"final {score} ({sw}+{dw}) {grade}; floors {floors}; recs {[r['title'] for r in rep['recommendations']]}")

# ---------------------------------------------------------------- source-identity.json
src = copy.deepcopy(psrc)
files = ident["candidate_files"]
nbytes = sum(f["bytes"] for f in files)
c = src["candidate"]
c["path"] = CAND
if "content_sha256" in c:  # differential-accessibility layout
    c["content_sha256"] = EXPECTED
    c["content_manifest"]["file_count"] = len(files)
    c["content_manifest"]["bytes"] = nbytes
    c["files"] = [{"path": f["path"], "bytes": f["bytes"], "sha256": f["sha256"]} for f in files]
    c["status"] = "untracked Skill subtree only; unmodified by delta re-audit (identity re-verified after)"
    src["prior_audit"] = {"path": PRIOR_DIR.replace("/", "\\") + "\\report.json",
                          "content_sha256": psrc["candidate"]["content_sha256"], "score": prior["final"]["score"]}
    src["tooling"]["note"] = "Environment not re-executed in this delta; fingerprints carried from the certified run"
else:
    c["manifest_sha256"] = EXPECTED
    c["file_count"] = len(files)
    c["byte_total"] = nbytes
    c["status_after_execution"] = "unchanged (manifest recomputed after the delta checks; no __pycache__)"
    blobs = {}
    if any("git_blob" in f for f in src["files"]):
        import subprocess
        for f in files:
            blobs[f["path"]] = subprocess.check_output(
                ["git", "hash-object", os.path.join(CAND, f["path"])], text=True).strip()
    src["files"] = [dict({"path": f["path"]}, **({"git_blob": blobs[f["path"]]} if blobs else {}),
                         sha256=f["sha256"], bytes=f["bytes"]) for f in files]
    src["prior_audit"] = {"path": PRIOR_DIR, "identity": psrc["candidate"]["manifest_sha256"],
                          "score": prior["final"]["score"]}
src["phase"] = "delta re-audit (delta-cat-20260930: category/author frontmatter and documented fixes)"
src["delta"] = {"shelf": f"F:/optimized-scientific-skills/skills/{SID}", "shelf_commit": "ea3b976",
                "shelf_identity": ident["shelf_identity"], "changed": ident["changed"],
                "added": ident["added"], "removed": ident["removed"]}
json.dump(src, open(f"{RUN}/source-identity.json", "w", encoding="utf-8", newline="\n"), indent=2,
          ensure_ascii=False)
print("source-identity written")
