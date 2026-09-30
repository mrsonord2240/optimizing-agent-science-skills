import json
ident = json.load(open('logs/identity_after.json', encoding='utf-8'))


def A(t, r, n):
    return {"text": t, "result": r, "note": n}


def I(i, ty, label, note, b, s, asr, st="COMPLETED"):
    p = sum(1 for a in asr if a['result'] == 'PASS')
    return {"index": i, "type": ty, "label": label, "status": st,
            "status_flag": "\u2705" if b + s >= 75 else "\u26a0\ufe0f", "note": note,
            "basic": b, "specialized": s, "total": b + s,
            "assertions_passed": p, "assertions_total": len(asr), "assertions": asr}


inputs = [
    I(1, "Canonical", "Shipped signac_workflow.R on 10x ATAC 1.0.1 PBMC 5k (chr1 fragments), documented args and relaxed 1 1000",
      "exit 0; 40/1472 cells at documented QC and 788/1472 relaxed, identical to prior baseline", 35, 53, [
          A("Script exits 0 and writes rds, QC, UMAP and depth PDFs", "PASS", "both runs exit 0; scatac_signac.rds present"),
          A("Kept cells satisfy the documented filter rule", "PASS", "default: passed_filters 15.6k-38k, TSS 4.2-7.4, nucleosome 0.42-0.85, FRiP 65-88%, mito<=0.040, blacklist<=0.005"),
          A("LSI component 1 tracks depth and dims 2:30 are used", "PASS", "LSI1-depth r -0.95/-0.96; UMAP 40x2 and 788x2 finite"),
          A("Rendered QC violins are legible and consistent with values", "PASS", "relaxed QC png inspected; blacklist outliers to 0.18 visible")]),
    I(2, "Variant A", "Shipped script auto-detecting Cell Ranger ARC 2.0.0 per_barcode_metrics.csv, PBMC 3k Multiome, whole-genome fragments",
      "exit 0 in 14m; 2392/2687 cells, 8 clusters; ARC blacklist ratio is peak-level and cannot reach the 0.05 cut (max 0.004)", 34, 51, [
          A("ARC metadata auto-detected and mapped without patching the script", "PASS", "log 'Metadata mode: cellranger-arc'; passed_filters == atac_fragments for all kept cells"),
          A("Kept cells are called cells inside the documented thresholds", "PASS", "is_cell==1 for 100%; passed_filters 1012-69101, TSS 4.02-11.2, nucleosome<=2.61, FRiP 17.9-81%, mito max 0.0499"),
          A("Embedding, clusters, gene activity and figures are valid and readable", "PASS", "LSI1-depth r -0.96; 8 clusters 594..117; ACT 19607x2392; UMAP finite; umap and qc png inspected"),
          A("ARC-substituted blacklist QC is documented with its sensitivity", "FAIL", "blacklist ratio max 0.00405 (57/128741 peaks overlap the list) versus up to 0.18 from the official ATAC column, so the filter is effectively inert; the Skill states the substitution but not that")]),
    I(3, "Variant A", "Shipped script on 10x ATAC 2.1.0 10k PBMC v2 (chr1 fragments slice), documented args and relaxed",
      "exit 0; 7008/10246 at documented args, 9884/10246 relaxed; 12 and 16 clusters", 35, 52, [
          A("ATAC 2.x singlecell.csv path runs at the documented three arguments", "PASS", "exit 0, 7008 cells; passed_filters 2090-79531, TSS>=4, nucleosome<=3.78"),
          A("Relaxed arguments 4-5 honored", "PASS", "9884 cells with 1 1000; TSS min 1.0"),
          A("Depth component skipped and outputs finite", "PASS", "LSI1-depth r +0.89; UMAP finite; ACT 2027 x cells; annotation genome hg38"),
          A("UMAP renders with separable clusters", "PASS", "12-cluster UMAP png inspected")]),
    I(4, "Variant B", "AMULET BAM route on ARC per the new flag table (ARC chr1 1-30 Mb CB-tagged BAM slice)",
      "exit 0; 2711 cells, 481 merged regions, 21 multiplets (0.77%)", 35, 52, [
          A("Documented flags --forcesorted --bcidx 0 --cellidx 0 --iscellidx 3 run to completion", "PASS", "jar + AMULET.py exit 0"),
          A("Cell count equals the ARC is_cell total", "PASS", "2711 of 2711"),
          A("Output family present and self-consistent", "PASS", "MultipletBarcodes_01 has 21 lines = summary 21; probabilities 2711 rows + header"),
          A("Multiplet rate plausible for shallow chr1 slice", "PASS", "0.77%; recall caveat stated in Skill")]),
    I(5, "Variant B", "AMULET fragment route: ARC (derived barcode,is__cell_barcode csv, whole-genome fragments) and ATAC 2.1.0 (chr1 slice, defaults)",
      "ARC 2711 cells/66 multiplets (2.43%); ATAC 2.1.0 10246 cells/146 multiplets (1.42%)", 35, 52, [
          A("Derived two-column csv recipe from the Skill text works on ARC", "PASS", "exit 0 after deriving csv from barcode and is_cell"),
          A("ATAC 2.1.0 fragments run at defaults", "PASS", "exit 0, 10246 cells"),
          A("Cell counts match the source metadata", "PASS", "2711 and 10246"),
          A("Multiplet files present and rates plausible", "PASS", "66 and 146 multiplets, outputs present")]),
    I(6, "Edge", "AMULET misuse controls for the table: ARC BAM with ATAC default indices; fragment route fed the raw ARC csv",
      "both fail loudly (exit 1): IndexError / missing Overlaps.txt; no silent success", 34, 52, [
          A("Wrong-index BAM run does not report success", "PASS", "IndexError in AMULET.py line 201, exit 1, matches the Skill's warning"),
          A("Raw ARC csv on fragment route does not report success", "PASS", "FileNotFoundError Overlaps.txt, exit 1"),
          A("Skill table prevents both failure modes", "PASS", "table rows specify indices and the derived csv")]),
    I(7, "Variant A", "Regression: Multiome WNN block verbatim plus cell-cycle LSI regression on 10x ARC PBMC 3k",
      "exit 0; WNN 2557 cells, weights 0.475/0.525; S-phase cor 0.264 to 0, ARI 0.843", 36, 54, [
          A("WNN block runs with only Signac and Seurat attached", "PASS", "magrittr loaded by the block; pca, lsi, wnn.umap built"),
          A("Modality weights and embedding valid", "PASS", "RNA/ATAC weight medians 0.475/0.525; wnn.umap 2557x2 finite"),
          A("Cell-cycle regression removes the S-phase association", "PASS", "max abs cor(LSI, S.Score) 0.264 to 0; UMAP cor 0.173 to 0.107"),
          A("Marker means fit cell types", "PASS", "CD3E/CD14/MS4A1/NKG7 enriched in distinct clusters")]),
    I(8, "Variant B", "Regression: SnapATAC2 2.10.0 block, ArchR empty-ArrowFiles guard, PEAKVI scArches alignment on PBMC 5k chr1 slice",
      "exit 0; SnapATAC2 697 cells/6 clusters; ArchR guard stops then passes relaxed; PEAKVI aligned 0.034 vs unaligned 0.099", 35, 52, [
          A("SnapATAC2 documented block runs (relaxed filter)", "PASS", "697 cells, 6 leiden clusters, obsp distances present, gene_mat 697x60606"),
          A("ArchR guard fails loudly at documented thresholds and passes relaxed", "PASS", "'length(ArrowFiles) > 0 is not TRUE' then rep1.arrow"),
          A("PEAKVI alignment lines change the mapping as claimed", "PASS", "median query-to-reference distance 0.099 unaligned, 0.034 aligned, ref-ref 0.033"),
          A("No audit narration or unrun Cell Ranger claims in the shipped text", "PASS", "SKILL.md states Cell Ranger ATAC/ARC were not run and outputs were read from public datasets")]),
]
avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
tp = sum(i['assertions_passed'] for i in inputs)
tt = sum(i['assertions_total'] for i in inputs)
cats = {
    "functional_suitability": (11, 12, "Covers ATAC 1.x/2.x and ARC inputs, three ecosystems, WNN and both AMULET routes; ARC blacklist QC is effectively non-filtering and not flagged as such"),
    "reliability": (11, 12, "Loud guards for missing metadata columns, barcode mismatch, zero passing cells, empty ArrowFiles; AMULET misuse fails with exit 1; peak-set alignment is an assertion"),
    "performance_context": (7, 8, "SKILL.md 123 lines with one-level routed references and tables"),
    "agent_usability": (15, 16, "Single filter rule, per-input AMULET flag table with derived csv recipe, depth-conditional doublet choice, relaxed-threshold guidance"),
    "human_usability": (7, 8, "Clear triggers, example requests and error table; recovery advice brief"),
    "security": (11, 12, "No credentials or destructive actions; writes to the working directory only; upstream downloads not checksummed"),
    "maintainability": (11, 12, "Audit narration removed, versions verified, provenance and MIT notice preserved; FractionCountsInRegion is soft-deprecated in Signac 1.17"),
    "agent_specific": (17, 20, "Trigger-rich description; dims 2:30 and cell-cycle claims reproduce; Cell Ranger not claimed as run; rule-of-thumb numbers labelled"),
}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1)
dw = round(avg * 0.6, 1)
sc = round(sw + dw)
rep = {
    "meta": {"skill_name": "bio-atac-seq-single-cell-atac",
             "description": "Process and analyze single-cell ATAC-seq data with Signac, ArchR, SnapATAC2, or Cell Ranger ATAC. Use when handling 10X scATAC or 10X Multiome (paired RNA+ATAC) data, performing per-cell QC, choosing between ArchR/Signac/SnapATAC2 ecosystems, building per-cluster consensus peaksets, integrating with paired scRNA-seq, doublet detection (AMULET vs ArchR vs scDblFinder), or running pseudobulk differential accessibility per cluster.",
             "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis",
             "execution_mode": "D", "complexity": "Complex", "n_inputs": 8},
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {"applicable": True, "gate": "PASS",
                          "scientific_integrity": {"result": "PASS", "detail": "Cell Ranger is stated as not run; ARC metric substitutions are disclosed as substitutions; reported numbers reproduced"},
                          "practice_boundaries": {"result": "PASS", "detail": "Public 10x data; no clinical or identifiable-person claims"},
                          "methodological_ground": {"result": "PASS", "detail": "LSI depth component skipped, depth-conditional doublet tool choice, ARC barcode mapping verified against matrix, BAM CB tag and fragments"},
                          "code_usability": {"result": "PASS", "detail": "signac_workflow.R ran on ARC 2.0.0, ATAC 2.1.0 and ATAC 1.0.1; AMULET routes ran as documented"}}},
    "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": tp, "total": tt}, "inputs": inputs},
    "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": sc, "max": 100, "grade": "Production Ready",
              "grade_symbol": "\u2b50", "deployable": True, "veto_override": False},
    "key_strengths": [
        "The shipped script runs end to end on ARC 2.0.0, ATAC 2.1.0 and ATAC 1.0.1 metadata and stops clearly on missing columns or barcode mismatch",
        "AMULET flag table per input type reproduces on real ARC and ATAC 2.1.0 data; misuse fails loudly",
        "Cell Ranger is honestly stated as not run, with outputs read from public 10x datasets",
        "Regression blocks (WNN, cell-cycle LSI, SnapATAC2, ArchR guard, PEAKVI alignment) reproduce as documented"],
    "recommendations": [{"priority": "P2", "title": "ARC blacklist ratio is inert; state that", "observed_in": [2, 3],
                         "problem": "On ARC the blacklist ratio comes from the peak matrix and peaked at 0.004 (57 of 128741 peaks overlap the list), so the 0.05 cut never removes a cell, while the official ATAC 1.0.1 column reaches 0.18; ATAC 2.1.0 singlecell.csv has a zero blacklist column. The Skill states the substitution but not its insensitivity.",
                         "root_cause": "The ARC substitution is peak-level, not fragment-level, and is documented only as a method.",
                         "fix": "Add one sentence to SKILL.md that on ARC and ATAC 2.x the blacklist ratio is an approximation that rarely reaches 0.05, so blacklist QC is effectively off unless computed from fragments."}],
}
json.dump(rep, open('report.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(sub, avg, sw, dw, sc, tp, tt)
c = ident
json.dump({"phase": "final re-audit", "independent_auditor": True,
           "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a", "path": "atac-seq/single-cell-atac", "subtree": "ef5b1305663382e0228349bd42d9768afc19dcb8"},
           "candidate": {"path": "F:\\OpenScience\\wt\\atac-single-cell-atac\\skills\\bio-atac-seq-single-cell-atac", "identity": "sha256-manifest-v1",
                         "manifest_sha256": c['manifest_sha256'], "file_count": c['file_count'], "byte_total": c['byte_total'],
                         "branch": "fix/atac-single-cell-atac", "base_commit": "3186916406e9cc6b0e6dc24ffe47880951fc0f93",
                         "status": "untracked, uncommitted; identity verified live before and after execution; no __pycache__",
                         "manifest_recipe": "relative POSIX path, byte count, lowercase SHA-256; tab-separated; LF joins; ordinal UTF-8 byte ordering; no trailing LF"},
           "files": c['files'], "supersedes_audit_identity": "4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286",
           "tooling": {"tools_md_sha256": "6089874dc93fb48cf2ade31eeb940fc620096ee4e76f936278a3b99318ae9c08",
                       "rubric_zip_sha256": "e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de",
                       "envs": ["bio-atac-seq-single-cell-atac-r", "bio-atac-seq-single-cell-atac-py", "bio-atac-seq-single-cell-atac-amulet"]}},
          open('source-identity.json', 'w', encoding='utf-8'), indent=2)
