import json, pathlib, hashlib
H = pathlib.Path(__file__).resolve().parent.parent
M = json.load(open(H / 'out' / 'manifest.json'))
W = lambda name, obj: open(H / name, 'w', encoding='utf-8', newline='\n').write(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

# ---------------------------------------------------------------- source identity
blob = {"LICENSE": "bcccf5e00d6fb375e1a12f8552ccaa05e377ca17", "SKILL.md": "141d7362847750aac24fd45ad2f2dd9c8bf55a0a",
        "references/ecosystem-workflows.md": "4e8d5f971a688171d30ada01278a28721f6e0776",
        "references/specialized-topics.md": "2658dc74c535fa1192bd4ac4742e164844882ba6",
        "references/usage-guide.md": "6b1720a8bdec46fdd7da3f13b6d8cd5e9772dd3b",
        "scripts/signac_workflow.R": "85635bee0786d6e73f24831f1b92d00a1ab31152"}
fp = ["e63d107d5564bee29c53fb4febd883fa6a63e492c90355857463606ab1b896f2", "40698d35f4f7d1cbfff800e191267393e1c65203ca1ff4a517b20024444baf11",
      "1f8b3faecfce87f8546c1e02814c88c1dcf92675ba5c8e4f1443e0d73d49ef85", "6dde8477b912e7e6d574889f5312082a059a4ad54279d1baacd60251b3833f6c",
      "5f2805955e046e50bd4114ebc23de72a0d9282a149d8faa1dc5f95e415661a8e"]
src = {
    "origin": {"repository": "GPTomics/bioSkills", "commit": "d91ed3d563019e649dc854c56ccd62551359488a",
               "path": "atac-seq/single-cell-atac", "subtree": "ef5b1305663382e0228349bd42d9768afc19dcb8",
               "checkout": "F:\\optimizing-agent-science-skills\\external\\GPTomics__bioSkills", "status": "clean"},
    "candidate": {"branch": "fix/atac-single-cell-atac", "commit": "3186916406e9cc6b0e6dc24ffe47880951fc0f93",
                  "identity": "sha256-manifest-v1", "manifest_sha256": M["manifest_sha256"],
                  "path": "F:\\OpenScience\\wt\\atac-single-cell-atac\\skills\\bio-atac-seq-single-cell-atac",
                  "status_before": "untracked skills/bio-atac-seq-single-cell-atac/ (normalization output); no working-tree edits",
                  "status_after_execution": "unchanged (manifest re-verified after execution; no __pycache__)",
                  "manifest_recipe": "relative POSIX path, byte count, lowercase SHA-256; tab-separated; LF joins; ordinal UTF-8 byte ordering; no trailing LF"},
    "files": [{"path": f["path"], "git_blob": blob[f["path"]], "sha256": f["sha256"], "bytes": f["bytes"]} for f in M["files"]],
    "tooling": {"tools_md_sha256": "a3c94d911150ef72f5a9f3a1012667dfed0b3164bb181003e9e48687aa5ff986",
                "environment_fingerprint_sha256": hashlib.sha256("\n".join(fp).encode()).hexdigest(),
                "environment_fingerprint_recipe": "sha256 of the LF-joined sha256 values of evidence/logs conda-list-r.json, conda-list-py.json, conda-list-amulet.json, R-packages.csv, pip-py.txt",
                "rubric_zip_sha256": "e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de"},
    "candidate_cache_artifacts_after_execution": []}
W('source-identity.json', src)

# ---------------------------------------------------------------- findings
F = []
def f(id, sev, title, obs, problem, cause, fix, ev):
    F.append({"id": id, "severity": sev, "state": "open", "title": title, "observed_in": obs, "problem": problem, "root_cause": cause, "fix": fix, "evidence": ev})

f("SCATAC-001", "P0", "signac_workflow.R fails: annotation genome mismatch", [1],
  "Running the shipped script exactly as the Skill documents (Rscript scripts/signac_workflow.R h5 fragments singlecell.csv, hg38, EnsDb.Hsapiens.v86) aborts in CreateSeuratObject with 'Annotation genome does not match genome of the object' after about 3 minutes; no QC, PDF or RDS output is written. Reproduced in the tooling phase and again in this audit (Signac 1.17.1, Seurat 5.5.1, EnsDb.Hsapiens.v86 2.99.0). The script is byte-identical to the origin example, so the defect is inherited. With annotation converted to UCSC style and genome set to hg38 the same script completes (input 2).",
  "GetGRangesFromEnsDb() returns Ensembl-style seqlevels (1, 2, X) with no genome, while the object is hg38/UCSC (chr1).",
  "After GetGRangesFromEnsDb(), add seqlevelsStyle(ann) <- 'UCSC' and genome(ann) <- 'hg38' (as done in the patched copy), pass ann to CreateChromatinAssay, and note that the same conversion applies to the CallPeaks/WNN snippets that build assays. Rerun the script end to end on the PBMC 5k slice.",
  "out/signac_asis.log; out/signac_patched.log (diff of patched copy printed by run_audit.sh signac_patched); scripts/patch_signac.py")
f("SCATAC-002", "P1", "SnapATAC2 block: obs['sample_id'] assignment raises", [4],
  "ecosystem-workflows.md step 1 runs data.obs['sample_id'] = 'rep1' straight after import_fragments; on SnapATAC2 2.10.0 it raises RuntimeError 'lengths don't match: unable to add a column of length 0 to a DataFrame of height 2973'. The whole documented block stops at its second line.",
  "Scalar assignment to a backed AnnData obs frame is no longer supported in 2.x (obs is a Polars-backed element).",
  "Replace with a list assignment (data.obs['sample_id'] = ['rep1'] * data.n_obs) or drop the line (the Skill never uses it) and rerun the block.",
  "out/snap.log (DOC-AS-WRITTEN line)")
f("SCATAC-003", "P1", "SnapATAC2 block: leiden needs snap.pp.knn first", [4],
  "snap.tl.spectral -> umap -> leiden as documented fails with RuntimeError 'No such key: distances' because tl.leiden reads adata.obsp['distances'], which only snap.pp.knn creates. After adding snap.pp.knn(data) the block gives 6 clusters on 697 cells.",
  "Step list omits the kNN-graph step required by 2.10 tl.leiden.",
  "Insert snap.pp.knn(data) between snap.tl.spectral and snap.tl.leiden (and before umap if the graph is reused); update the usage-guide example request and the goal-routing table ('spectral -> UMAP -> leiden').",
  "out/snap.log (DOC-AS-WRITTEN leiden line, clusters 203/172/159/84/50/29)")
f("SCATAC-004", "P1", "QC thresholds conflict across SKILL.md, script and usage guide", [2, 4, 5],
  "SKILL.md table passes 3000-50000 fragments per cell (caution 1000-3000), TSS >= 4, and lists mitochondrial fraction and doublet score; the script filters peak_region_fragments 1000-20000 (a different metric), TSS > 4, never computes a mitochondrial fraction and runs no doublet step although the agent sequence requires both; the agent sequence and error table say re-filter at fragments >= 1000 AND TSS >= 4 (so 1000-3000 is both 'caution' and 'keep'). On the real Cell Ranger ATAC 1.0.1 PBMC 5k singlecell.csv (5,335 called cells): 384 (7.2%) have passed_filters < 1000, 330 fall in 1000-3000, 4,545 in 3000-50000, 41 exceed 80000; the script's peak-fragment window (1000-20000) alone keeps 4,288. An agent cannot tell which cell set is intended.",
  "Thresholds were merged from several sources without reconciling the metric (total vs peak-region fragments) or the pass/caution boundary.",
  "State one QC rule set in one place (metric, lower and upper bound, treatment of caution band), make the script implement it or say explicitly which rows it does not implement (mito, doublets), and align usage-guide examples. Keep the cell-calling note (supported: 7.2% of called cells < 1000).",
  "out/qccsv.log; scripts/singlecell_csv_qc.py; SKILL.md QC table vs scripts/signac_workflow.R lines 41-47")
f("SCATAC-005", "P2", "AMULET: no invocation, undocumented numpy<1.24 pin", [7],
  "The Skill names AMULET as the primary doublet tool but gives no command; usage-guide.md lists only 'numpy/pandas/scipy/statsmodels + Java 8+'. AMULET v1.1 AMULET.py/FragmentFileOverlapCounter.py use np.object, which raises AttributeError on numpy >= 1.24 (verified with numpy 2.5.3). With numpy 1.23.5 the fragment route (AMULET.sh --forcesorted fragments singlecell.csv chrlist repeatfilter outdir scriptdir) ran on the PBMC 5k slice: 5,335 barcodes, 426 merged regions, 55 multiplets (1.03%). The BAM/jar route (snATACOverlapCounter.jar) was not executed (no CB-tagged BAM staged).",
  "Skill defers to upstream without an executable recipe; upstream code is unmaintained against modern numpy.",
  "Add the AMULET.sh command (fragment and BAM forms), the repeat-filter file source, chromosome list, and the numpy<1.24 requirement (separate env). Label the BAM route as untested until a CB-tagged BAM is exercised.",
  "out/amulet.log; out/amulet_MultipletSummary.txt; out/amulet_numpy_probe.log")
f("SCATAC-006", "P2", "Multiome WNN snippet fails without magrittr", [3],
  "The WNN block chains NormalizeData(obj) %>% FindVariableFeatures() ... %>% and RunTFIDF(obj) %>% FindTopFeatures(...) but exists('%>%') is FALSE after library(Signac); library(Seurat), so the snippet stops with 'could not find function \"%>%\"'. With library(magrittr) it ran on the 3k Multiome (2,557 cells, 12 WNN clusters).",
  "Snippet assumes dplyr/magrittr attached.",
  "Add library(magrittr) (or rewrite with native |> / intermediate assignments) and list the libraries at the top of the block.",
  "out/probe.log ('%>% availability'); out/wnn.log")
f("SCATAC-007", "P2", "Cell-cycle 'ScaleData regress S.score' fix cannot work", [2],
  "specialized-topics.md tells the agent to regress the S-phase score before LSI with ScaleData(obj, vars.to.regress='S.score'). On Signac 1.17.1 / Seurat 5.5.1 ScaleData on the ChromatinAssay errors (features in 'scale.data' must be in the same order as in 'data'), with or without vars.to.regress; and RunSVD.Assay reads layer='data' (not scale.data), so even a working regression would not change the LSI. The '5-10% global accessibility' effect size and the chromatin S-phase signature are uncited.",
  "R/Seurat RNA idiom transplanted to a TF-IDF/SVD workflow.",
  "Replace with a method that acts on the LSI input (e.g. regress the covariate from the LSI embedding, or include it as a covariate in pseudobulk DA) and test it; cite the effect size or remove it.",
  "out/probe.log (ScaleData section); scripts/probe_static_claims.R (covariate is synthetic, labelled)")
f("SCATAC-008", "P2", "'AMULET primary' default conflicts with typical depth", [7],
  "The doublet section says run AMULET as the primary check and keep intersections of two tools as high confidence, while stating AMULET recall drops below about 15-16K read pairs per cell. In the real PBMC 5k Cell Ranger metadata the median called cell has 10.7K passed fragments and 69.9% of called cells are below 15K. The AMULET paper (Genome Biol 22:252, PMC8408950) reports recall about 0.85-0.90 near 25K valid read pairs and states ArchR outperformed AMULET at lower depth; the '15-16K' figure was not found in the paper text. Requiring two-tool agreement further lowers sensitivity at low depth.",
  "Tool ranking is stated independent of the depth condition the Skill itself lists.",
  "Make the primary tool depth-conditional (measure median valid read pairs per cell first; AMULET above ~25K, synthetic-doublet methods below), source the 15-16K threshold or replace it with the paper's figure, and describe two-tool intersection as a precision choice, not the default.",
  "out/qccsv.log; PMC8408950 (Thibodeau 2021)")
f("SCATAC-009", "P3", "DepthCor '~ -1' comment is sign-dependent; UMAP artifact is modest", [2, 3],
  "Script and docs say LSI component 1 'should correlate ~ -1 with depth'. Observed: +0.88 (Signac slice, 458 cells), -0.96 (Multiome, 2,557 cells); SVD sign is arbitrary. The 'dims 1:30 gives a density gradient' claim is supported in direction only: max |cor(UMAP, log depth)| 0.098 (1:30) vs 0.045 (2:30) on the Multiome data.",
  "Sign and magnitude quoted as if fixed.",
  "Say 'strongly correlated (|r| near 1, either sign)' and describe the UMAP effect as depth-associated structure rather than always a visible gradient.",
  "out/signac_depth_cor.png; out/wnn.log; out/signac_patched.log")
f("SCATAC-010", "P3", "ArchR createArrowFiles returns nothing quietly at documented thresholds", [5],
  "On shallow data (chr1 slice) createArrowFiles(minTSS=4, minFrags=1000) logs 'has encountered an error, checking if any ArrowFiles completed' and returns an empty vector without an R error; the next line (addDoubletScores) would fail obscurely. Relaxed thresholds (minTSS=1, minFrags=500) gave 403 cells. Slice-driven, but the Skill has no guard.",
  "No check that ArrowFiles is non-empty.",
  "Add 'stopifnot(length(ArrowFiles) > 0)' (or an explicit message) after createArrowFiles and advise lowering thresholds and inspecting the ArchR log if no cells pass.",
  "out/archr.log")
f("SCATAC-011", "P3", "snap.tl.macs3 default parallelism fails in a plain script", [4],
  "snap.tl.macs3(data, groupby='leiden') with default n_jobs launches spawn workers that re-import the __main__ script; in this audit the workers raised 'An attempt has been made to start a new process before the current process has finished its bootstrapping phase' (Exporting fragments/Calling peaks repeated per worker) and an earlier run with the backed file open r+ died with an HDF5 lock error ('Some worker process has died unexpectedly'). n_jobs=1 works (6 clusters, peaks called).",
  "Documented call is not wrapped in an if __name__ == '__main__' guard and does not mention n_jobs.",
  "Wrap script use in a main guard or set n_jobs=1 for scripts, and note the backed-file locking limitation on network/drvfs mounts (HDF5_USE_FILE_LOCKING=FALSE).",
  "out/snap_macs3_nolock.log; out/snap_macs3_default_lock_error.log; out/snap.log (n_jobs=1 run)")
f("SCATAC-012", "P3", "PEAKVI reference mapping omits the peak-set alignment requirement", [8],
  "specialized-topics.md shows PEAKVI.load_query_data(adata_query, reference_path) with no statement that query peaks must equal the reference peak set. Tested: a query with 60% of the peaks is rejected (ValueError, var count mismatch); a query with the same number of features but different names is accepted with only a 'var_names ... does not match' warning. The mapping itself ran (368 query cells, 6-d finite latent, median query->reference distance 0.034 vs 0.033), but that test is a random split of one dataset and does not test cross-study transfer.",
  "Reference-mapping recipe copied without its preconditions.",
  "State that query peaks must be re-quantified on the reference peak set (same names and order), and treat the var_names warning as an error.",
  "out/peakvi.log; out/peakvi_mm.log")
f("SCATAC-013", "P3", "Install guidance incomplete for the documented code", [1, 3, 5, 6],
  "usage-guide.md installs Signac, Seurat, ArchR and snapatac2 but not leidenbase (Seurat lists it under Suggests; FindClusters(algorithm=4), used by the script, needs it), magrittr, or MACS3 (needed by CallPeaks, ArchR pathToMacs2 and snap.tl.macs3); CallPeaks/ArchR examples use a '/path/macs3' placeholder that must point to a macs3 executable (worked with macs3 3.0.4 for both).",
  "Prerequisites list not derived from the code paths.",
  "Add leidenbase, magrittr and macs3 (with how to locate the executable) to the prerequisites and state the AMULET env requirement.",
  "out/probe.log (leidenbase Suggests); out/callpeaks.log; out/archr.log")
f("SCATAC-014", "P3", "Uncited or unverified quantitative and biological claims", [6],
  "MACS3 'needs roughly >= 1M reads per pseudobulk / >= 200 cells' is uncited (a 67-cell cluster of the slice went through CallPeaks without error); S-phase '5-10% accessibility' and XCI-escapee wording are uncited ('biallelically accessible in female but not male cells' is imprecise: males carry Y gametologs DDX3Y and UTY, verified present in EnsDb v86 at chrY:12.9-13.5 Mb); AMULET 15-16K threshold see SCATAC-008. Verified correct: XIST hg38 coordinates chrX:73820651-73852753 (EnsDb v86); 'no UMIs' and lenient cell calling (SCATAC-004).",
  "Numbers inherited from the source without provenance.",
  "Cite or soften each figure; reword the XCI-escapee sentence; keep the verified XIST coordinates.",
  "out/callpeaks.log; out/probe.log (XIST/UTY/DDX3Y coordinates)")
f("SCATAC-015", "P3", "singlecell.csv columns untested for cellranger-atac 2.x and cellranger-arc", [1],
  "The script and usage guide read outs/singlecell.csv (passed_filters, peak_region_fragments, blacklist_region_fragments), verified only on a Cell Ranger ATAC 1.0.1 file. The Skill claims Cell Ranger ATAC 2.1+ and Multiome inputs; cellranger-arc emits per_barcode_metrics.csv (different columns, per the tooling notes; the 10x page could not be fetched in this audit). Static-only; Cell Ranger requires 10x registration (restricted).",
  "Column assumptions from one legacy pipeline version.",
  "After 10x access is available, run cellranger-atac 2.x / cellranger-arc on the demo FASTQs and adapt the metadata reader (or document both column sets).",
  "TOOLS.md (blockers); scripts/signac_workflow.R lines 22, 42-43")

# ---------------------------------------------------------------- report
def inp(i, typ, label, status, note, basic, spec, asr):
    flag = "✅" if status == "COMPLETED" and basic + spec >= 75 else ("⚠️" if status == "COMPLETED" else "❌")
    return {"index": i, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note, "basic": basic, "specialized": spec,
            "total": basic + spec, "assertions_passed": sum(a[1] for a in asr), "assertions_total": len(asr),
            "assertions": [{"text": a[0], "result": "PASS" if a[1] else "FAIL", "note": a[2]} for a in asr]}

I = [
 inp(1, "Canonical", "signac_workflow.R as shipped on 10x PBMC 5k scATAC (chr1 slice)", "ERROR",
     "Aborts with annotation genome mismatch; no outputs (SCATAC-001)", 14, 26, [
     ("Script exits 0 on the documented 3-argument invocation", False, "Execution halted at CreateSeuratObject/SetAssayData"),
     ("Script writes the QC PDF, depth-correlation PDF, UMAP PDF and scatac_signac.rds", False, "No output files written"),
     ("Failure is loud and specific rather than silently wrong", True, "Error names the annotation/object genome mismatch"),
     ("Documented hg38 + EnsDb.Hsapiens.v86 assumption works without annotation conversion", False, "Ensembl-style seqlevels without genome; reproduced in tooling and audit runs")]),
 inp(2, "Variant A", "Same script, 2-line-patched copy (UCSC style, genome hg38), relaxed TSS > 1; plus QC-table and cell-cycle probes", "COMPLETED",
     "Runs after patch; documented TSS > 4 keeps 13 cells on the slice (relaxed keeps 458/1472); one cluster; ScaleData probe fails", 30, 42, [
     ("Patched script completes and writes ATAC + ACT assays, UMAP, LSI, gene activity", True, "458 cells, ACT 2027 x 458, UMAP 458x2, chr1 features; QC violin/UMAP PNGs rendered and read"),
     ("Per-cell QC values in plausible ranges", True, "TSS 1.0-6.4, nucleosome signal 0.36-1.99, FRiP 23-88% (whole-genome Cell Ranger counts over a slice)"),
     ("Cell Ranger cell calling is lenient as the Skill states", True, "Real singlecell.csv: 384/5335 called cells (7.2%) < 1000 fragments"),
     ("LSI component 1 correlates about -1 with depth", False, "+0.88 on this run (sign arbitrary; SCATAC-009)"),
     ("Documented ScaleData(vars.to.regress) cell-cycle correction runs on the ATAC assay", False, "Errors on ChromatinAssay in Signac 1.17.1 / Seurat 5.5.1 (SCATAC-007)")]),
 inp(3, "Variant A", "Multiome WNN block on 10x PBMC 3k granulocyte-sorted Multiome (full genome, counts only)", "COMPLETED",
     "Runs with magrittr attached; 2,557 cells, 12 WNN clusters, weights RNA 0.475 / ATAC 0.525 median", 33, 48, [
     ("WNN block runs as written after loading Signac and Seurat only", False, "%>% not found (SCATAC-006); works with library(magrittr)"),
     ("Joint clusters are biologically sensible", True, "12 clusters; means of CD3E/CD14/MS4A1/NKG7/GNLY/CST3 separate T, monocyte, B, NK; ARI(wnn,RNA)=0.822, ARI(wnn,ATAC 2:30)=0.858"),
     ("LSI1 tracks depth as claimed", True, "cor -0.96 (LSI2/3 -0.14/-0.11)"),
     ("dims 2:30 lowers depth association of the ATAC UMAP versus 1:30", True, "max |cor(UMAP,depth)| 0.045 vs 0.098 (modest)"),
     ("Per-modality weights can be inspected as advised", True, "RNA/ATAC weights per cell present; IQR 0.41-0.52 / 0.48-0.59")]),
 inp(4, "Variant B", "SnapATAC2 block (import_fragments -> tsse -> tile matrix -> spectral -> leiden -> macs3 -> gene matrix), PBMC 5k slice", "PARTIAL",
     "Two documented steps fail on 2.10.0; runs after fixes with relaxed filter (697 cells, 6 clusters)", 24, 38, [
     ("pp.import_fragments exists and pp.import_data does not on 2.10.0, as the Skill states", True, "hasattr checks and 2,973 barcodes imported"),
     ("data.obs['sample_id'] = 'rep1' works as documented", False, "RuntimeError lengths don't match (SCATAC-002)"),
     ("spectral -> umap -> leiden works as documented", False, "No such key: distances; needs snap.pp.knn (SCATAC-003)"),
     ("After fixes the pipeline yields clusters, peaks and a gene matrix", True, "6 leiden clusters, macs3 (n_jobs=1) ok, gene matrix 697 x 60606 (documented filter keeps 0 cells on the slice; relaxed 400/0.3 used)"),
     ("Documented snap.tl.macs3 default parallelism works in a plain script", False, "Bootstrapping RuntimeError in spawn workers / HDF5 lock death (SCATAC-011)")]),
 inp(5, "Variant B", "ArchR block (Arrow files -> doublets -> IterativeLSI -> clusters -> UMAP -> group coverages -> reproducible peaks -> PeakMatrix), PBMC 5k slice", "COMPLETED",
     "Exit 0 in 37 min under load; documented thresholds return no ArrowFile on the slice, relaxed (minTSS=1, minFrags=500) gives 403 cells", 32, 46, [
     ("Arrow file, TileMatrix and GeneScoreMatrix are built and doublets filtered", True, "403 cells, 402 after filterDoublets; GeneScoreMatrix 24919 x 402"),
     ("Clustering and UMAP produce interpretable output", True, "5 clusters (25/53/119/118/87); UMAP PNG rendered and read; clusters overlap in embedding at this depth"),
     ("addReproduciblePeakSet accepts macs3 via pathToMacs2 and yields a peak set", True, "7,788 peaks, chr1 only, median width 501; PeakMatrix 7788 x 402"),
     ("Matrices share the same cells and expected dimensions", True, "PeakMatrix and GeneScoreMatrix both 402 cells"),
     ("Documented thresholds give either cells or a clear error", False, "Empty return with log line only on shallow data (SCATAC-010; slice-driven)")]),
 inp(6, "Variant B", "Signac CallPeaks per cluster (MACS3) and scDblFinder doublets (amulet() and synthetic ATAC mode), PBMC 5k slice", "COMPLETED",
     "Runs with magrittr and explicit macs3 path; 3 clusters (847/558/67) -> 7,959 peaks; scDblFinder 103/1472 doublets", 32, 46, [
     ("CallPeaks returns a valid GRanges with peak_called_in per cluster", True, "7,959 peaks, width median 150, chr1 only, cluster labels present"),
     ("Tn5 recipe (format BED, shift -75, extsize 150) is honoured", True, "median width 150"),
     ("scDblFinder ATAC mode (aggregateFeatures, nfeatures 25, normFeatures) classifies cells", True, "1369 singlet / 103 doublet, threshold ~0.76; score-depth cor 0.81 on this shallow slice"),
     ("scDblFinder::amulet() yields per-cell q-values from the fragments file", True, "834 cells, 47 with q < 0.05")]),
 inp(7, "Variant B", "AMULET v1.1 fragment route on PBMC 5k slice (chr1)", "COMPLETED",
     "Runs only in a numpy<1.24 env; no command in the Skill; BAM/jar route not executed", 27, 36, [
     ("AMULET runs on modern numpy", False, "np.object AttributeError on numpy 2.5.3; ran with numpy 1.23.5 (SCATAC-005)"),
     ("Output files parse and are consistent", True, "5,335 cells, 426 merged regions, 55 multiplets (1.03%) in MultipletSummary.txt"),
     ("Skill documents the invocation and the numpy pin", False, "Neither present in SKILL.md or usage-guide.md"),
     ("AMULET-primary advice matches the depth of the demo data", False, "Median 10.7K fragments per called cell, 69.9% under 15K (SCATAC-008)")]),
 inp(8, "Variant B", "PEAKVI scArches mapping (GPU) on PBMC 5k slice peak matrix, plus peak-set mismatch probes", "COMPLETED",
     "Mapping runs (30 epochs, RTX 5070 Ti); first attempt hit a transient CUDA-busy error, rerun ok; test is a same-dataset split", 32, 45, [
     ("load_query_data + train + get_latent_representation run as documented", True, "368 x 6 finite latent (epochs 30, bounded from 200)"),
     ("Query cells fall inside the reference latent space", True, "median query->ref NN distance 0.034 vs ref-ref 0.033"),
     ("Query with a different peak count is rejected", True, "ValueError var count mismatch"),
     ("Skill states the peak-set alignment precondition", False, "Absent; same-count/different-name query only warns (SCATAC-012)")]),
]
ne = round(sum(i["total"] for i in I) / len(I), 1)
passed = sum(i["assertions_passed"] for i in I); tot = sum(i["assertions_total"] for i in I)
cats = {
 "functional_suitability": (8, "Broad ecosystem coverage and routing; primary script fails as shipped, SnapATAC2 block fails twice, cell-cycle fix ineffective"),
 "reliability": (7, "Script has no annotation/input guard; ArchR returns empty quietly; scDblFinder/AMULET/macs3 edge behaviour undocumented"),
 "performance_context": (7, "SKILL.md about 10 KB with one-level routed references; QC and doublet tables are dense but sectioned"),
 "agent_usability": (11, "Clear ecosystem decision table and failure modes; QC rule set contradictory across files; AMULET without a command"),
 "human_usability": (7, "Good trigger description and example requests; error recovery advice limited"),
 "security": (11, "No credentials or destructive operations; script writes to CWD with a default prefix; upstream downloads unchecksummed"),
 "maintainability": (9, "License and provenance preserved, versions verified current; unpinned, no numpy/AMULET env note"),
 "agent_specific": (15, "Trigger-rich description; scientific rationale for dims 2:30 verified; several uncited numbers and overstated defaults"),
}
mx = {"functional_suitability": 12, "reliability": 12, "performance_context": 8, "agent_usability": 16, "human_usability": 8, "security": 12, "maintainability": 12, "agent_specific": 20}
sub = sum(v[0] for v in cats.values())
sw = round(sub * 0.4, 1); dw = round(ne * 0.6, 1)
R = {
 "meta": {"skill_name": "bio-atac-seq-single-cell-atac",
          "description": "Process and analyze single-cell ATAC-seq data with Signac, ArchR, SnapATAC2, or Cell Ranger ATAC. Use when handling 10X scATAC or 10X Multiome (paired RNA+ATAC) data, performing per-cell QC, choosing between ArchR/Signac/SnapATAC2 ecosystems, building per-cluster consensus peaksets, integrating with paired scRNA-seq, doublet detection (AMULET vs ArchR vs scDblFinder), or running pseudobulk differential accessibility per cluster.",
          "evaluated_on": "2026-09-30", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex", "n_inputs": len(I)},
 "veto_gates": {
   "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
   "research_veto": {"applicable": True, "gate": "FAIL",
     "scientific_integrity": {"result": "PASS", "detail": "No fabricated values; checked figures (XIST coordinates, LSI1-depth correlation, cell-calling leniency) are traceable; uncited numbers noted in SCATAC-008 and SCATAC-014"},
     "practice_boundaries": {"result": "PASS", "detail": "Research-only genomics Skill with no clinical conclusions"},
     "methodological_ground": {"result": "PASS", "detail": "dims 2:30 rationale confirmed on real data; the ScaleData cell-cycle remedy and AMULET-primary default are flawed (SCATAC-007, SCATAC-008) but are guidance errors, not a principled fallacy in a produced result"},
     "code_usability": {"result": "FAIL", "detail": "The primary shipped script scripts/signac_workflow.R does not run on its documented input (annotation genome mismatch, SCATAC-001); reproduced in two independent runs; one-line class of fix, but the script is not runnable as shipped"}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": mx[k], "note": v[1]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": ne, "max": 100, "assertion_pass_rate": {"passed": passed, "total": tot}, "inputs": I},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": round(sw + dw), "max": 100, "grade": "Reject", "grade_symbol": "❌", "deployable": False, "veto_override": True},
 "key_strengths": [
   "Strong ecosystem-choice guidance and failure-mode table; the LSI dims 2:30 rationale reproduces on real Multiome data",
   "Most workflows execute end to end on real public PBMC data once documented gaps are patched: WNN, ArchR, Signac CallPeaks, scDblFinder, AMULET fragment route, PEAKVI mapping",
   "Version claims are current (Signac 1.17.1, Seurat 5.5.1, ArchR 1.0.3, SnapATAC2 2.10.0 with import_fragments); XIST coordinates verified; cell-calling leniency confirmed on real singlecell.csv",
   "Clean progressive disclosure with one-level routed references; MIT license and provenance preserved"],
 "recommendations": [
   {"priority": "P0", "title": "Shipped signac_workflow.R fails on annotation genome", "observed_in": [1],
    "problem": "The primary script aborts with 'Annotation genome does not match genome of the object' on its documented input and writes nothing.",
    "root_cause": "EnsDb annotation is Ensembl-style with no genome while the object is hg38/UCSC.",
    "fix": "Convert annotation with seqlevelsStyle(ann) <- 'UCSC' and genome(ann) <- 'hg38' before CreateChromatinAssay and rerun end to end (SCATAC-001)."},
   {"priority": "P1", "title": "SnapATAC2 block errors twice on 2.10.0", "observed_in": [4],
    "problem": "data.obs['sample_id']='rep1' raises and tl.leiden fails with 'No such key: distances'; default macs3 parallelism fails in plain scripts.",
    "root_cause": "Block was not executed against the current SnapATAC2 API.",
    "fix": "Use a list assignment or drop the line, add snap.pp.knn before leiden, and use n_jobs=1 or a main guard for macs3 (SCATAC-002, SCATAC-003, SCATAC-011)."},
   {"priority": "P1", "title": "Contradictory QC thresholds across files", "observed_in": [2, 4, 5],
    "problem": "SKILL.md table, script and usage guide use different metrics and bands; the script omits mito and doublet steps the workflow requires.",
    "root_cause": "Thresholds merged from sources without one canonical rule set.",
    "fix": "Define one rule set, implement or explicitly exclude each row in the script, and align examples (SCATAC-004)."},
   {"priority": "P2", "title": "AMULET route: no command, numpy pin, depth default", "observed_in": [7],
    "problem": "No AMULET command or numpy<1.24 requirement is given, and AMULET is ranked primary although most cells in the demo data are below its recall depth.",
    "root_cause": "Defers to upstream and states ranking without the depth condition.",
    "fix": "Add the AMULET.sh recipe and env pin, make tool choice depth-conditional, and source the depth threshold (SCATAC-005, SCATAC-008)."},
   {"priority": "P2", "title": "Cell-cycle regression and WNN snippets not executable", "observed_in": [2, 3],
    "problem": "ScaleData on the ChromatinAssay errors and would not affect RunSVD; the WNN block needs magrittr.",
    "root_cause": "RNA idioms and implicit package attachments were carried over untested.",
    "fix": "Replace the regression method with one that acts on LSI and test it; attach magrittr or avoid pipes (SCATAC-006, SCATAC-007)."},
   {"priority": "P2", "title": "Prerequisites, guards and uncited claims", "observed_in": [5, 6, 8],
    "problem": "Install list misses leidenbase/magrittr/macs3, ArchR and PEAKVI lack input guards, several quantitative claims are uncited, and singlecell.csv columns are unverified beyond Cell Ranger ATAC 1.0.1.",
    "root_cause": "Prerequisites and claims were not derived from executed code paths.",
    "fix": "Complete the prerequisites, add the ArrowFiles and peak-set checks, cite or soften numbers, and test cellranger-arc metadata when 10x access exists (SCATAC-009, SCATAC-010, SCATAC-012, SCATAC-013, SCATAC-014, SCATAC-015)."}]}
W('report.json', R)
W('findings.json', F)
print("static", sub, "exec_avg", ne, "assertions", passed, tot, "score", R["final"]["score"])
