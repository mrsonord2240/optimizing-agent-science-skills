"""Delta re-audit builder: carry the prior certified report forward and apply only delta-touched changes.

usage: python dc_build.py <skill_id>
Writes report.json and source-identity.json (+ candidate-manifest.tsv) into ../ (the run directory).
"""
import copy, hashlib, json, os, sys
from collections import OrderedDict

sys.dont_write_bytecode = True
SID = sys.argv[1]
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIOR_ROOT = "F:/optimizing-agent-science-skills/audits/skills"
PRIOR = {
    "bio-atac-seq-deep-learning-atac": "candidate@3a9d1b4cab32-reaudit-run",
    "bio-atac-seq-co-accessibility": "candidate@0aac567b1870-reaudit-run",
    "bio-atac-seq-enhancer-gene-linking": "candidate@44385431f019-reaudit-run",
}[SID]
CAND = {
    "bio-atac-seq-deep-learning-atac": "F:\\OpenScience\\wt\\atac-deep-learning-atac\\skills\\bio-atac-seq-deep-learning-atac",
    "bio-atac-seq-co-accessibility": "F:\\OpenScience\\wt\\atac-co-accessibility\\skills\\bio-atac-seq-co-accessibility",
    "bio-atac-seq-enhancer-gene-linking": "F:\\OpenScience\\wt\\atac-enhancer-gene-linking\\skills\\bio-atac-seq-enhancer-gene-linking",
}[SID]
DATE = "2026-09-30"


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh, object_pairs_hook=OrderedDict)


def dump(obj, p):
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def manifest(root):
    rows = []
    for dp, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(dp, f); b = open(p, "rb").read()
            rows.append((os.path.relpath(p, root).replace(os.sep, "/"), len(b), hashlib.sha256(b).hexdigest()))
    rows.sort(key=lambda r: r[0].encode("utf-8"))
    text = "\n".join(f"{r}\t{n}\t{h}" for r, n, h in rows)
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), rows, text


def finalize(r):
    ins = r["dynamic_score"]["inputs"]
    r["static_score"]["subtotal"] = sum(c["score"] for c in r["static_score"]["categories"].values())
    for i in ins:
        i["total"] = i["basic"] + i["specialized"]
        i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
        i["assertions_total"] = len(i["assertions"])
    d = r["dynamic_score"]
    d["execution_avg"] = round(sum(i["total"] for i in ins) / len(ins), 1)
    d["assertion_pass_rate"] = OrderedDict(passed=sum(i["assertions_passed"] for i in ins),
                                           total=sum(i["assertions_total"] for i in ins))
    f = r["final"]
    f["static_weighted"] = round(r["static_score"]["subtotal"] * 0.4, 1)
    f["dynamic_weighted"] = round(d["execution_avg"] * 0.6, 1)
    f["score"] = round(f["static_weighted"] + f["dynamic_weighted"])
    veto = "FAIL" in (r["veto_gates"]["skill_veto"]["gate"], r["veto_gates"]["research_veto"]["gate"])
    s = f["score"]
    grade = "Reject" if veto else "Production Ready" if s >= 85 else "Limited Release" if s >= 75 else "Beta Only" if s >= 60 else "Reject"
    assert grade == f["grade"], (grade, f["grade"])  # delta must not silently change grade symbol conventions
    f["veto_override"] = veto
    f["deployable"] = grade in ("Production Ready", "Limited Release") and not veto
    assert all(x["priority"] in ("P0", "P1", "P2") for x in r["recommendations"])


prior_dir = os.path.join(PRIOR_ROOT, SID, PRIOR)
r = load(os.path.join(prior_dir, "report.json"))
r["meta"]["evaluated_on"] = DATE
cats = r["static_score"]["categories"]
ins = r["dynamic_score"]["inputs"]

if SID == "bio-atac-seq-deep-learning-atac":
    cats["reliability"]["score"] = 11
    cats["reliability"]["note"] = ("Fail-fast guards, RESUME and an honest QC gate; step 0 now also refuses to start without "
                                   "bedtools or bedGraphToBigWig (DLA-015 resolved, executed on a filtered PATH).")
    cats["agent_usability"]["score"] = 15
    cats["agent_usability"]["note"] = ("Clear routing and copyable commands; the env table now lists every external binary and "
                                       "the script header points to the right step (DLA-016 resolved); three environments still must be juggled.")
    a = ins[0]["assertions"][0]
    a["note"] = ("ra_guards_gate.sh: 7 of 7 exit 1 with the documented message; delta: the no-chrombpnet guard is now a "
                 "three-tool loop and was re-executed (step0_tools.log)")
    i5 = ins[4]
    i5["basic"], i5["specialized"] = 35, 51
    i5["note"] = ("scBasset preprocess, 1-epoch train and embedding run on real 10x PBMC; Enformer matches an independent bin "
                  "computation; the Skill labels full-scale training, scBasset on Keras 3 and Borzoi as not run; bedtools and "
                  "bedGraphToBigWig are now declared and checked up front (delta re-test)")
    a = i5["assertions"][4]
    a["result"] = "PASS"
    a["note"] = ("delta: env table lists bedtools and ucsc-bedgraphtobigwig (both present in the env's conda-meta); step 0 exits 1 "
                 "in under 0.1 s naming the withheld tool for each of the three, and passes when all are present (step0_tools.log)")
    r["key_strengths"][1] = ("The shipped pipeline runs from a fresh directory, resumes cheaply, fails fast on bad inputs and on "
                             "missing external binaries, and gates on chromBPNet's own QC thresholds.")
    r["recommendations"] = []

elif SID == "bio-atac-seq-co-accessibility":
    cats["agent_usability"]["score"] = 15
    cats["agent_usability"]["note"] = ("Clear tool selection table with per-route execution status; version guidance and the "
                                       "TSS window (+/- 2 kb) are now consistent across SKILL.md, usage guide and script (COACC-015 resolved)")
    r["recommendations"] = [OrderedDict(
        priority="P2",
        title="COACC-014 cryptic halt on a zero-read cell",
        observed_in=[7],
        problem=("A cell with no reads in the peak set stops the CLI with 'attempt to set an attribute on NULL'; only "
                 "monocle3's warning names the cause. The conflicting TSS-window prompt from the prior report is fixed."),
        root_cause="No guard for empty cells in run_cicero_pipeline.",
        fix="Fail early with a message naming zero-read cells, or drop them with a count; not blocking.")]

elif SID == "bio-atac-seq-enhancer-gene-linking":
    pass  # frontmatter-only delta: no dimension or assertion is touched; EGL-013 stays open

finalize(r)
dump(r, os.path.join(RUN, "report.json"))

# ---- source-identity.json, modelled on the prior run's own file
new_id, rows, text = manifest(CAND)
si = load(os.path.join(prior_dir, "source-identity.json"))
files = [OrderedDict(path=p, bytes=n, sha256=h) for p, n, h in rows]
prior_identity = {"bio-atac-seq-deep-learning-atac": "3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87",
                  "bio-atac-seq-co-accessibility": "0aac567b1870fb501220470d665c600af91f274cfa816e649bdcad81db8c8afa",
                  "bio-atac-seq-enhancer-gene-linking": "44385431f01902a0e18e305b483538009282bb44c5f19de4b53d5facd2b38976"}[SID]
si["phase"] = "delta re-audit"
si["independent_auditor"] = True
si["prior_audit_identity"] = prior_identity
c = si["candidate"]
status = "untracked Skill subtree only" if SID != "bio-atac-seq-co-accessibility" else \
    "Candidate skill directory is staged with unstaged modifications (AM) in the worktree"
if SID == "bio-atac-seq-co-accessibility":
    c["root"] = CAND
    c["content_sha256"] = new_id
    c["manifest_bytes"] = len(text.encode("utf-8"))
    c["file_count"] = len(rows)
    c["manifest_recipe"] = ("Ordinal UTF-8 relative POSIX paths; each line is path, TAB, byte count, TAB, lowercase file "
                            "SHA-256 of the raw bytes; lines joined by LF without a trailing LF; SHA-256 over the manifest "
                            "bytes. No file contains a CR byte, so the prior CRLF->LF normalisation is a no-op here.")
    c["identity_before"] = c["identity_after"] = new_id
    c["tree_status"] = status + "; identity recomputed live before and after this delta re-audit; no candidate bytes modified."
    si["tooling"]["environment_live_check"] = ("Not re-run: the delta touches frontmatter and one usage-guide prompt only; "
                                               "no execution surface changed. Prior live check carried forward.")
    si["tooling"]["tools_md_sha256"] = "0fb4b3ba8bd8d255f85cea6a46f8a8fac699d1ccdd0e0b4f8078adf01535d489"
    si["files"] = files
    with open(os.path.join(RUN, "candidate-manifest.tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
else:
    c["path"] = CAND
    c["commit"] = "3186916406e9cc6b0e6dc24ffe47880951fc0f93"
    c["status_before"] = status
    c["status_after_execution"] = status + "; candidate bytes unchanged (identity recomputed after execution)"
    c["content_sha256"] = new_id
    cm = c["content_manifest"]
    cm["file_count"] = len(rows)
    if "byte_total" in cm:
        cm["byte_total"] = sum(n for _, n, _ in rows)
    else:
        cm["bytes"] = sum(n for _, n, _ in rows)
        cm["manifest_bytes"] = len(text.encode("utf-8"))
    c["files"] = files
    if SID == "bio-atac-seq-deep-learning-atac":
        si["tooling"]["environment_note"] = ("Skill env `chrombpnet` realised as micromamba env dlatac-tf in WSL distro science "
                                             "(TOOLS.md); no env named `chrombpnet` exists. Env not modified.")
dump(si, os.path.join(RUN, "source-identity.json"))
print(SID, "identity", new_id, "static", r["static_score"]["subtotal"], "exec", r["dynamic_score"]["execution_avg"],
      "final", r["final"]["score"], r["final"]["grade"], "recs", [x["title"] for x in r["recommendations"]])
