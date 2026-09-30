"""Builds report.json, source-identity.json and validates the report against skill-auditor report_json_schema.md rules."""
import hashlib, json, os, subprocess, sys
RUN = r"F:\OpenScience\audits\bio-atac-seq-single-cell-atac\reaudit-run"
CAND = r"F:\OpenScience\wt\atac-single-cell-atac\skills\bio-atac-seq-single-cell-atac"
AUD = r"F:\OpenScience\audits\bio-atac-seq-single-cell-atac"

def A(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}
def inp(i, typ, label, status, note, b, s, asserts):
    t = b + s
    flag = "✅" if status == "COMPLETED" and t >= 75 else ("⚠️" if status == "COMPLETED" else "❌")
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note,
            "basic": b, "specialized": s, "total": t,
            "assertions_passed": sum(a["result"] == "PASS" for a in asserts), "assertions_total": len(asserts), "assertions": asserts}

inputs = [
 inp(1, "Canonical", "Shipped signac_workflow.R on its documented 3 arguments, 10x PBMC 5k scATAC (chr1 slice)", "COMPLETED",
     "Exit 0 at documented QC (TSS 4, 1000 fragments): 40 of 1,472 cells survive on the slice, one cluster; all expected outputs written", 33, 49, [
   A("Script exits 0 on h5 + fragments + singlecell.csv with no extra arguments", True, "EXIT 0; previously failed with annotation genome mismatch (SCATAC-001)"),
   A("Output object has ATAC and ACT assays, LSI, UMAP and finite values", True, "ACT 2027 x 40 finite, UMAP 40 x 2 finite, annotation converted to UCSC/hg38 in-script (seqlevels chrX/chr20/chr1, genome hg38)"),
   A("Every retained cell satisfies the SKILL.md filter rule", True, "passed_filters 15.6k-38.0k, TSS 4.2-7.39, nucleosome 0.42-0.85, FRiP 65-88%, blacklist <= 0.005, mito <= 0.040"),
   A("LSI component 1 tracks depth as the script states", True, "cor(LSI1, log10 depth) = -0.95 (sign arbitrary, wording says so)"),
 ]),
 inp(2, "Variant A", "Same script with relaxed QC (args 4-5 = 1 1000) plus missing-metadata-column guard", "COMPLETED",
     "788 cells, 2 clusters (758/30), figures rendered and read; guard stops with a named missing column", 35, 52, [
   A("Relaxed run (slice-driven) completes and filters within the stated rule", True, "788 cells; FRiP 23-88%, nucleosome 0.36-1.99, TSS >= 1.02, blacklist <= 0.01, mito <= 0.043"),
   A("QC violin, depth and UMAP PDFs render legibly", True, "Rendered to PNG and read: five violins labelled, UMAP with legend and cluster labels; a 30-cell cluster is separated"),
   A("Depth correlation of LSI1 is strong; UMAP and ACT finite", True, "cor -0.96; ACT 2027 x 788 finite; UMAP 788 x 2 finite"),
   A("Missing singlecell.csv column fails loudly before processing", True, "Column peak_region_fragments renamed: stop('metadata file lacks columns: peak_region_fragments'), exit 1, no outputs"),
 ]),
 inp(3, "Variant A", "Multiome WNN block extracted verbatim from ecosystem-workflows.md, 10x PBMC 3k Multiome (full genome, counts only)", "COMPLETED",
     "Runs with only Signac and Seurat attached; 2,557 cells, 12 WNN clusters, finite WNN UMAP", 36, 54, [
   A("Block runs as written with only library(Signac), library(Seurat) attached", True, "%>% absent beforehand (FALSE); block supplies library(magrittr); no error"),
   A("Joint clusters are biologically coherent", True, "12 clusters 702/340/.../30; CD3E high in clusters 1-5, CD14 in 0, MS4A1 in 7 and 9 (2.1-2.4), NKG7 in 5 and 8 (2.8-3.4)"),
   A("LSI1 tracks depth and modality weights are inspectable", True, "LSI1-3 vs depth -0.96/-0.14/-0.11; RNA/ATAC weight medians 0.475/0.525"),
   A("WNN UMAP dimensionality and finiteness", True, "wnn.umap 2557 x 2 finite"),
 ]),
 inp(4, "Variant B", "SnapATAC2 2.10.0 block extracted verbatim from ecosystem-workflows.md, PBMC 5k slice", "COMPLETED",
     "Block runs without edits other than path and slice-driven filter (400/0.3): 697 cells, 6 leiden clusters, gene matrix 697 x 60,606", 35, 51, [
   A("Corrected block has no sample_id line and includes snap.pp.knn", True, "Checked in the live block before execution"),
   A("import_fragments exists, import_data and read_10x do not, as the Skill states", True, "hasattr checks: import_data False, import_fragments True, read_10x False (2.10.0)"),
   A("spectral -> knn -> umap -> leiden -> macs3(n_jobs=1) -> gene matrix completes", True, "obsp distances present; leiden 203/172/159/84/50/29; uns macs3 present; UMAP 697 x 2 finite; spectral 697 x 18"),
   A("Outputs are scientifically plausible", True, "TSSE 0.3-2.93 (filter 0.3); gene matrix 697 x 60,606 (whole-genome gene set, chr1 slice signal)"),
 ]),
 inp(5, "Variant B", "ArchR block with new stopifnot(length(ArrowFiles) > 0) guard, PBMC 5k slice", "COMPLETED",
     "Documented thresholds stop at the guard; relaxed (minTSS 1, minFrags 500) gives rep1.arrow with 403 cells; downstream steps unchanged, prior identity-matched evidence reused", 34, 50, [
   A("Documented thresholds on shallow data fail loudly at the guard", True, "STOPPED with: length(ArrowFiles) > 0 is not TRUE"),
   A("Relaxed thresholds pass the guard and yield an Arrow file with cells", True, "rep1.arrow 178 MB, 403 cell names in Metadata/CellNames"),
   A("Downstream pipeline behavior is unchanged from the audited identity", True, "Step text unchanged (TileMatrix, addIterativeLSI, addClusters, addReproduciblePeakSet with macs3); initial audit executed it (403 cells, 5 clusters, 7,788 peaks); not rerun here"),
 ]),
 inp(6, "Variant B", "AMULET v1.1 fragment route as documented, in the documented numpy<1.24 env, PBMC 5k slice", "COMPLETED",
     "Documented command exits 0: 1,823,956 reads, 5,335 cells, 55 multiplets (1.03%); BAM route not executed and labelled untested", 34, 50, [
   A("Documented fragment command runs in the documented environment", True, "numpy 1.23.5; EXIT 0; 14 s"),
   A("Output files exist and are consistent", True, "MultipletSummary: 5335 cells, 426 merged regions, 55 multiplets; MultipletBarcodes_01 55 lines; Probabilities 5336 lines (header + cells) with p and q values"),
   A("Skill does not claim the BAM route was executed", True, "ecosystem-workflows.md: 'UNTESTED here, no CB-tagged BAM was available'; SKILL.md version note lists Cell Ranger as not run"),
   A("Depth-conditional guidance is consistent with the demo data", True, "Median 10,701 passed fragments per called cell, 69.9% under 15K (recomputed from singlecell.csv), so ArchR/scDblFinder preference below 25K is supported"),
 ]),
 inp(7, "Variant B", "PEAKVI scArches block from specialized-topics.md with peak-set alignment lines, PBMC 5k slice (GPU)", "COMPLETED",
     "Aligned query 0 var_names warnings, latent 368 x 6 finite, query-to-reference distance 0.031 vs ref-ref 0.030; shuffled unaligned query warns and is 0.129", 35, 51, [
   A("Alignment lines are present and executable", True, "Block executed from the live markdown with epochs bounded 200 -> 30"),
   A("Aligned query maps into the reference latent space", True, "median query->ref NN 0.031 vs ref-ref 0.030"),
   A("Unaligned control demonstrates why the precondition matters", True, "shuffled peaks: var_names warning and distance 0.129 (4x)"),
   A("Latent representation is finite with expected shape", True, "368 x 6 finite; obsm['X_emb'] set"),
 ]),
 inp(8, "Variant A", "Cell-cycle LSI S-phase regression block extracted verbatim from specialized-topics.md, 10x PBMC 3k Multiome", "COMPLETED",
     "Max |cor(LSI2:30, S.Score)| 0.264 -> 0, LSI1 untouched, embedding 2557 x 50 finite, UMAP runs on the new reduction", 36, 53, [
   A("Block runs as written on a Multiome object with S.Score", True, "CellCycleScoring from paired RNA, then block executed verbatim; no error"),
   A("S-phase association removed from LSI dims 2-30", True, "0.264 -> 0 (max abs correlation)"),
   A("Depth component is left unchanged", True, "LSI1 identical; embedding 2557 x 50 finite"),
   A("Downstream UMAP on the regressed reduction works", True, "umap 2557 x 2 finite; reductions include lsi_sreg"),
 ]),
]
n = len(inputs)
avg = round(sum(i["total"] for i in inputs) / n, 1)
passed = sum(i["assertions_passed"] for i in inputs); tot = sum(i["assertions_total"] for i in inputs)
cats = {
 "functional_suitability": (11, 12, "Broad ecosystem coverage and routing; every runnable surface now executes; Cell Ranger ATAC 2.x/ARC metadata and the AMULET BAM route are not exercised (stated as untested)"),
 "reliability": (10, 12, "Loud guards for missing metadata columns, empty ArrowFiles, zero cells passing QC and leidenbase; peak-set alignment is an assertion, not a hard stop for same-count mismatches upstream"),
 "performance_context": (7, 8, "SKILL.md about 10 KB with one-level routed references; dense but sectioned tables"),
 "agent_usability": (14, 16, "One filter rule defined once and implemented; AMULET env and commands present; depth-conditional doublet choice; relaxed-threshold guidance for shallow data is one sentence"),
 "human_usability": (7, 8, "Good trigger description, example requests and error lookup table; recovery advice brief"),
 "security": (11, 12, "No credentials or destructive operations; script writes to CWD with a default prefix; upstream downloads not checksummed"),
 "maintainability": (10, 12, "Versions verified current; license and provenance preserved; one shipped sentence narrates audit history and the SnapATAC2 'removed in 2.9' boundary is unverified"),
 "agent_specific": (16, 20, "Trigger-rich description; dims 2:30 and cell-cycle claims reproduce; a few rule-of-thumb numbers are labelled as such; Cell Ranger claims untested"),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = int(round(sw + dw))
report = {
 "meta": {"skill_name": "bio-atac-seq-single-cell-atac",
   "description": "Process and analyze single-cell ATAC-seq data with Signac, ArchR, SnapATAC2, or Cell Ranger ATAC. Use when handling 10X scATAC or 10X Multiome (paired RNA+ATAC) data, performing per-cell QC, choosing between ArchR/Signac/SnapATAC2 ecosystems, building per-cluster consensus peaksets, integrating with paired scRNA-seq, doublet detection (AMULET vs ArchR vs scDblFinder), or running pseudobulk differential accessibility per cluster.",
   "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex", "n_inputs": n},
 "veto_gates": {
   "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
   "research_veto": {"applicable": True, "gate": "PASS",
     "scientific_integrity": {"result": "PASS", "detail": "Checked figures reproduce: 7.2% of called cells under 1000 fragments, median 10,701 fragments and 69.9% under 15K, LSI1-depth correlation, S-phase correlation 0.264 to 0, peak-set alignment distances; uncited rules of thumb are labelled as such"},
     "practice_boundaries": {"result": "PASS", "detail": "Research-only genomics Skill with no clinical conclusions"},
     "methodological_ground": {"result": "PASS", "detail": "dims 2:30, LSI-embedding cell-cycle regression and depth-conditional doublet-tool choice are sound and reproduced; relaxed thresholds for shallow data are disclosed in the filter rule"},
     "code_usability": {"result": "PASS", "detail": "signac_workflow.R runs end to end on its documented three arguments and stops with a named message when metadata columns are missing; SnapATAC2, ArchR guard, WNN, AMULET fragment, PEAKVI and cell-cycle blocks all executed from the live markdown"}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": passed, "total": tot}, "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100,
   "grade": "Production Ready" if score >= 85 else "Limited Release", "grade_symbol": "⭐" if score >= 85 else "✅",
   "deployable": True, "veto_override": False},
 "key_strengths": [
   "The primary shipped script now runs end to end on its documented three arguments and fails loudly on missing metadata or empty QC results",
   "Every corrected Python and R snippet executes from the live markdown on real public PBMC data (SnapATAC2 2.10.0, ArchR guard, WNN, AMULET fragment route, PEAKVI, cell-cycle LSI regression)",
   "One QC filter rule is defined once and implemented by the script; shallow-data relaxation and untested Cell Ranger/BAM routes are stated plainly",
   "Numerical claims check out against the real singlecell.csv and Multiome data; licensing and provenance preserved"],
 "recommendations": [
   {"priority": "P2", "title": "Cell Ranger ATAC 2.x / ARC metadata untested", "observed_in": [1, 2],
    "problem": "signac_workflow.R was verified only against Cell Ranger ATAC 1.0.1 singlecell.csv columns; cellranger-arc per_barcode_metrics.csv uses different names and only the missing-column stop was exercised.",
    "root_cause": "10x registration is required to obtain Cell Ranger output (carried from SCATAC-015).",
    "fix": "After-action: with 10x access run cellranger-atac/-arc count on a demo dataset and point the script at outs/; adjust column mapping if needed. The Skill already states the test scope."},
   {"priority": "P2", "title": "AMULET BAM route not executed", "observed_in": [6],
    "problem": "Only the fragment route ran; the BAM/jar route with --forcesorted has no public CB-tagged BAM to exercise.",
    "root_cause": "No CB-tagged BAM staged; the Skill labels it UNTESTED.",
    "fix": "After-action: run AMULET.sh on a CB-tagged BAM when one is available. No Skill change required."},
   {"priority": "P2", "title": "Shipped text narrates audit history", "observed_in": [],
    "problem": "specialized-topics.md says 'the audit saw ScaleData error on the full peak set'; the claim was not re-run in this re-audit and the phrase is process narrative in an operational Skill.",
    "root_cause": "Fix text kept the audit finding as a parenthetical.",
    "fix": "Reword to a neutral, testable statement (for example 'ScaleData can error on the full peak set') or drop the parenthetical."},
   {"priority": "P2", "title": "SnapATAC2 import_data removal version unverified", "observed_in": [4],
    "problem": "SKILL.md says import_data was 'renamed/removed in 2.9'; 2.8.0 still has both names and 2.10.0 has only import_fragments, but 2.9 was not inspectable.",
    "root_cause": "Boundary inferred from two endpoints.",
    "fix": "State 'absent in 2.10.0' or verify the 2.9 wheel and cite it."}]}

# ---- schema validation (report_json_schema.md pre-emit checklist) ----
errs = []
def chk(c, m):
    if not c: errs.append(m)
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
chk(len(inputs) == report["meta"]["n_inputs"], "n_inputs")
for i in inputs:
    chk(3 <= len(i["assertions"]) <= 5, f"assertion count input {i['index']}")
    chk(i["basic"] + i["specialized"] == i["total"], "total")
    chk(0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60, "ranges")
    chk(i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]), "passed count")
    chk(i["assertions_total"] == len(i["assertions"]), "assert total")
chk(len(cats) == 8 and all(0 <= v[0] <= v[1] for v in cats.values()), "cats")
chk(report["static_score"]["subtotal"] == sum(c["score"] for c in report["static_score"]["categories"].values()), "subtotal")
chk(abs(avg - round(sum(i["total"] for i in inputs) / n, 1)) < 1e-9, "avg")
chk(report["final"]["static_weighted"] == round(sub * 0.4, 1) and report["final"]["dynamic_weighted"] == round(avg * 0.6, 1), "weights")
chk(report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]), "score")
pr = [r["priority"] for r in report["recommendations"]]
chk(all(p in ("P0", "P1", "P2") for p in pr) and pr == sorted(pr), "priorities")
chk(2 <= len(report["key_strengths"]) <= 5, "strengths")
chk(all(len(r["title"]) <= 60 for r in report["recommendations"]), "title length")
if errs: sys.exit("SCHEMA FAIL: " + "; ".join(errs))
json.dump(report, open(os.path.join(RUN, "report.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
l1 = sum(i["basic"] for i in inputs) / n; l2 = sum(i["specialized"] for i in inputs) / n
print("schema OK; static", sub, "exec avg", avg, "L1", l1, "L2", l2, "assert", passed, tot, "score", score, report["final"]["grade"])

# ---- source-identity.json ----
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
files = []
for r, d, f in os.walk(CAND):
    for nme in f:
        p = os.path.join(r, nme); rel = os.path.relpath(p, CAND).replace("\\", "/"); b = open(p, "rb").read().replace(b"\r\n", b"\n")
        blob = subprocess.run(["git", "hash-object", "--stdin"], input=b, capture_output=True).stdout.decode().strip()
        files.append({"path": rel, "git_blob": blob, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
files.sort(key=lambda x: x["path"].encode())
manifest = "\n".join("%s\t%d\t%s" % (x["path"], x["bytes"], x["sha256"]) for x in files).encode()
ident = hashlib.sha256(manifest).hexdigest()
assert ident == "4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286", ident
logs = os.path.join(AUD, "evidence", "logs")
fp = hashlib.sha256("\n".join(sha(os.path.join(logs, x)) for x in ["conda-list-r.json", "conda-list-py.json", "conda-list-amulet.json", "R-packages.csv", "pip-py.txt"]).encode()).hexdigest()
init = json.load(open(os.path.join(AUD, "initial-audit-20260930", "source-identity.json"), encoding="utf-8"))
out = {"phase": "final re-audit", "independent_auditor": True, "origin": init["origin"],
  "candidate": {"branch": "fix/atac-single-cell-atac", "commit": init["candidate"]["commit"], "identity": "sha256-manifest-v1", "manifest_sha256": ident,
    "file_count": len(files), "byte_total": sum(x["bytes"] for x in files),
    "path": CAND, "status_before": "untracked skills/bio-atac-seq-single-cell-atac/ (fixed, uncommitted)",
    "status_after_execution": "unchanged (manifest recomputed after execution; no __pycache__)", "manifest_recipe": init["candidate"]["manifest_recipe"]},
  "files": files,
  "tooling": {"tools_md_sha256": sha(os.path.join(AUD, "TOOLS.md")), "environment_fingerprint_sha256": fp,
    "environment_fingerprint_recipe": init["tooling"]["environment_fingerprint_recipe"], "rubric_zip_sha256": sha(r"F:\optimizing-agent-science-skills\skill-auditor.zip")},
  "supersedes_audit_identity": "da2da9c8bbafb674486ac581373867852f7b577f77626b19e63cc8dcecf55d08",
  "candidate_cache_artifacts_after_execution": []}
json.dump(out, open(os.path.join(RUN, "source-identity.json"), "w", encoding="utf-8"), indent=2)
print("identity", ident, len(files), "files", out["candidate"]["byte_total"], "bytes; env fp", fp)
