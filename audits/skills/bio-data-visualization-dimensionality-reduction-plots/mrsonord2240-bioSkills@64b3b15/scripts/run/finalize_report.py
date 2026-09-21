import json, os
AUD = r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots"
SK = "bio-data-visualization-dimensionality-reduction-plots"
A = lambda t, r, n: {"text": t, "result": r, "note": n}
KEYS = ("index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total",
        "assertions_passed", "assertions_total", "assertions", "executed", "execution_note")
inputs = [
 dict(index=1, type="Canonical", label="Bulk PCA (sklearn) on synthetic 3-condition x 2-batch counts, variance-labelled axes", status="COMPLETED",
   note="Executed run/i1_pca_python.py. SKILL.md Python PCA block verbatim; axis-label percentages compared with an independent numpy SVD; colours compared with cmap(norm(codes)).",
   basic=32, specialized=46, assertions=[
   A("PC1/PC2 axis-label percentages equal an independent SVD computation", "PASS", "Labels 32.0% / 10.3% equal SVD 32.0% / 10.3%; sklearn used the randomized solver here (max ratio diff 0.0007) but the 1-dp labels were unchanged; scores are centred (mean ~0), not scaled. run/i1b_pca_determinism.py: the same block run twice without random_state gives different scores (max abs diff 15.3, sign/rotation of late PCs) and ratios differing by 1.6e-4; svd_solver='full' or random_state=42 is identical."),
   A("Colour-by-group mapping is correct", "PASS", "Scatter facecolors equal viridis(norm(condition code)) for all 60 points (figs/i1_pca_skillblock.png opened: three separated bands, PC2 = condition, R2 0.99)."),
   A("The block works on a condition column as a researcher has it (string labels) and identifies groups", "FAIL", "c=labels with string labels raises ValueError; block has no category-to-colour step and no legend."),
   A("The stated fix for library-size-driven PC1 ('vst() or log + scale') removes the library-size axis", "FAIL", "On raw counts PC1 corr with library size +0.96; after log2+scale still +0.99 (PC1 explains 34%). Only size-factor (CPM) normalisation first drops it to +0.19 and lets batch (PC1, R2 0.97) and condition (PC2/PC3, R2 0.98) appear."),
   A("The warning that unnormalised PCA is dominated by library size is accurate", "PASS", "Raw-count PC1 tracks the planted library factor (r = 0.96).")]),
 dict(index=2, type="Variant A", label="PCAtools biplot/scree/loadings on REAL airway vst data (R route)", status="COMPLETED",
   note="Executed run/i2_pcatools_airway.R via r.sh (PCAtools 2.18.0, DESeq2 1.46.0, ggplot2 4.0.3). SKILL.md R block run with airway's dex/cell in place of condition/batch.",
   basic=33, specialized=49, assertions=[
   A("p$variance used in the title is percent and equals an independent prcomp for PC1-8", "PASS", "41.94 / 21.97 / 16.20 identical to prcomp on t(assay(vsd)); all.equal tolerance 1e-6; PC1 scores correlate +1 with prcomp (no sign flip)."),
   A("biplot colby/shape mapping is correct on real data", "PASS", "figs/i2_biplot.png opened: trt (coral) right, untrt (teal) left on PC1; PC1 R2 for dex 0.95, PC2 R2 for cell 0.98; 4 cell-line shapes present."),
   A("screeplot(components = 1:10) and plotloadings(components = 1, rangeRetain = 0.05) run verbatim", "PASS", "Both returned figures; loadings panel opened (top positive ENSG00000101347/ENSG00000211445, non-blank). Only warnings are PCAtools' ggplot2 size deprecations. With airway's 8 samples the fixed components = 1:10 draws an empty 'NA' slot (figs/i2_scree.png): the Skill hard-codes 10 components."),
   A("The Skill supports the promised 'show loadings as arrows on PC1 vs PC2' request", "FAIL", "usage-guide prompt promises it but no code or argument (showLoadings, ntopLoadings) is given; it works (biplot(showLoadings=TRUE)) only if the agent knows the API."),
   A("Warning that PCA on unnormalised counts is dominated by a few high-count genes is accurate", "PASS", "Raw airway counts: PC1 51.1% of variance, top 10 genes carry 65% of PC1 squared loading.")]),
 dict(index=3, type="Variant B", label="scanpy PCA -> neighbors -> UMAP -> Leiden -> save on synthetic 4-cluster counts + real pbmc68k_reduced", status="COMPLETED",
   note="Executed run/i3_scanpy_umap.py (scanpy 1.12.4, umap-learn 0.5.12). Leiden as written fails on this stack; completed with flavor='igraph'.",
   basic=31, specialized=44, assertions=[
   A("The scanpy save-path trap is described accurately", "PASS", "save='_clusters.pdf' -> figures/umap_clusters.pdf; save='myplot.pdf' -> figures/umapmyplot.pdf; nothing in cwd; dpi_save default 150 in the installed signature."),
   A("UMAP is reproducible under the stated seed (scanpy random_state=42, umap-learn random_state=42)", "PASS", "Two runs bit-identical for each; seed 7 differs; umap-learn without random_state differs between runs; umap-learn prints the n_jobs-overridden-to-1 warning (not mentioned in the Skill)."),
   A("Claim 'without setting seed, results vary' holds for the scanpy route", "FAIL", "sc.tl.umap default random_state=0: two runs without random_state are identical. True only for umap-learn/uwot/openTSNE."),
   A("sc.tl.leiden(adata, resolution=0.5, random_state=42) runs as written", "FAIL", "ModuleNotFoundError: leidenalg (scanpy 1.12 default flavor); usage-guide pip line lists neither leidenalg nor igraph. With flavor='igraph', n_iterations=2, directed=False it recovers the 4 planted clusters (ARI 1.000)."),
   A("Colour-by-group mapping and cluster structure are right", "PASS", "UMAP point colours equal the cluster_true palette for all 600 cells; kNN purity vs planted labels 1.0; real pbmc68k_reduced UMAP (figs/i3_pbmc.png) shows dendritic/monocyte/B/T groups, non-blank.")]),
 dict(index=4, type="Edge", label="t-SNE (openTSNE Kobak-Berens block, Rtsne, uwot), seeds and small-n perplexity on a 6-cluster hierarchy", status="COMPLETED",
   note="Executed run/i4_tsne.py, i4b_rtsne_uwot.R, i4c_seedarg.R (openTSNE 1.0.4, Rtsne 0.17, uwot 0.2.4). All three blocks run verbatim.",
   basic=31, specialized=43, assertions=[
   A("The openTSNE Kobak-Berens block runs and is reproducible under random_state=42, n_jobs=-1", "PASS", "Two fits bit-identical (n_jobs=-1 and n_jobs=1); 1500x2 TSNEEmbedding; parameter names n_iter, initialization, learning_rate, perplexity, random_state all exist in 1.0.4."),
   A("PCA init + lr n/12 recovers more global structure than a random-init lr=200 run", "PASS", "Spearman of cluster-centroid distances vs high-dim over 4 seeds: 0.61/0.66/0.52/0.63 vs 0.39/0.30/0.13/0.59."),
   A("Claim 'learning_rate = n/12, not the default 200' (and 'init=pca, NOT random') matches the tool the block uses", "FAIL", "openTSNE default is learning_rate='auto' (= n/12 = 125 here) and initialization='pca'; results with explicit KB settings equal the defaults (0.68/0.66/0.51/0.67). The 'default 200 / random init' story is Rtsne/older sklearn."),
   A("'Set seed=42 (R uwot/Rtsne)' gives reproducible R embeddings", "FAIL", "uwot::umap(seed=42) works (identical twice), but Rtsne(seed=42) is silently absorbed by `...`: two calls differ (identical: FALSE). Only set.seed() works, as the Skill's own code block does."),
   A("Small-n perplexity rule (perplexity > n/3 fails) is accurate", "PASS", "n=60: Rtsne perplexity 30 errors 'perplexity is too large'; 19 and 5 run. openTSNE instead warns 'Perplexity 30 is too high. Using perplexity 19.67' (clamps, no failure).")]),
 dict(index=5, type="Stress", label="PHATE block on planted continuous and branching (Y) trajectories vs UMAP/PCA", status="COMPLETED",
   note="Executed run/i5_phate.py and i5b_branching.py (phate 2.0.0). Block verbatim with knn=10, decay=40, t='auto', random_state=42.",
   basic=34, specialized=50, assertions=[
   A("PHATE block runs and is reproducible under random_state=42", "PASS", "800x2 embedding, optimal t=8, two runs bit-identical (max diff 0)."),
   A("Colour by pseudotime is mapped correctly and the embedding orders the trajectory", "PASS", "Scatter colours equal viridis(pseudotime); |Spearman| of pseudotime with the embedding's principal axis 0.97 (UMAP 0.98, PCA 0.88); figs/i5_phate.png opened, non-blank."),
   A("PHATE is at least as faithful as UMAP for continuous/branching structure (Skill claim)", "PASS", "Branching data, mean |dpseudotime| among 10-NN: PHATE 0.100, UMAP 0.124 / 0.130 (high-dim 0.159); unbranched: 0.051 vs 0.058. Not contradicted; margin is modest."),
   A("Stated hyperparameters (knn, decay, t) are valid and robust", "PASS", "knn=3/10/40 all recover order (rho 0.96-0.97); SGD-MDS non-convergence warnings are not mentioned in the Skill.")]),
 dict(index=6, type="Scope Boundary", label="Shipped examples/embedding_phd.py end to end on a 1200-cell, 3000-gene h5ad", status="PARTIAL",
   note="Executed from a copy in run/ex (input processed.h5ad synthetic; the example points at a file that is not shipped). Fails as shipped on missing scikit-misc; ran after installing scikit-misc 0.5.2 + leidenalg 0.12.0 with pip --target into run/pylib (no shared env changed).",
   basic=28, specialized=37, assertions=[
   A("The example runs as shipped on a valid h5ad", "FAIL", "ModuleNotFoundError: skmisc at highly_variable_genes(flavor='seurat_v3'); later leiden needs leidenalg; usage-guide pip line lists neither; the example's processed.h5ad is not shipped. n_top_genes=2000 also needs >=2000 genes."),
   A("With dependencies present, PCA axis labels equal an independent computation and outputs are non-blank", "PASS", "variance_ratio 1.10%/1.05% equals SVD of the HVG-scaled matrix; pca.pdf, tsne.pdf, figures/umap_clusters.pdf rendered by Ghostscript and opened: clusters visible, ARI 1.000 vs 5 planted clusters."),
   A("The HVG step is methodologically sound", "FAIL", "seurat_v3 is run after normalize_total+log1p; scanpy warns it 'expects raw count data'. Marker recovery 288/300 vs 295/300 on raw counts; 251 of 2000 HVGs differ."),
   A("Every figure and the caption template the example builds is usable", "FAIL", "Scree and PHATE figures are created but never saved (2 savefig for 4 figures); the caption is a plain string, so it prints literal 'N={n}' (AST: Constant, not JoinedStr); the 2-level condition uses cmap='tab10' on codes -> blue/cyan, no legend."),
   A("The example encodes the traps the Skill lists (seed, PCA init, figdir, variance labels)", "PASS", "random_state=42 everywhere, initialization='pca', figdir set (file landed in figures/), PC axes carry variance percentages; UMAP and t-SNE cluster colours are identical across panels.")]),
 dict(index=7, type="Adversarial", label="'UMAP shows A closer to B than C, so they are lineage-related; and UMAP hides batch': the Skill's claims against measurement", status="COMPLETED",
   note="Executed run/i3b_batch_hierarchy.py and i7_local_preservation.py (synthetic planted hierarchy + batch; real pbmc68k_reduced).",
   basic=34, specialized=49, assertions=[
   A("Guidance not to read inter-cluster UMAP distance as biology, and to check in high-dim space, is correct", "PASS", "Three planted equidistant clusters (PCA centroid distances 13.5/13.9/13.3) come out as 0.58-1.0 (normalised) UMAP distances across 5 seeds; on real pbmc the between-seed rank correlation of centroid distances is 0.87-0.98 but only 0.22-0.33 against high-dim."),
   A("'Local neighborhoods are preserved by construction' is accurate", "FAIL", "Mean fraction of high-dim 15-NN kept in 2-D: real pbmc68k_reduced 0.39-0.41 (UMAP), synthetic 1500 cells UMAP 0.14, t-SNE 0.23. Chari-Pachter's actual point (local structure is distorted too) is stated more weakly than measured."),
   A("Batch diagnosis rule ('PC1/PC2 separate batches; UMAP can hide it') holds", "FAIL", "Planted batch sits on PC4 (R2 0.83) while PC1/PC2 are cell type (R2 0.98): a PC1-vs-PC2 view misses it. Within cell type, same-batch kNN fraction is 0.80-0.83 in PCA but 0.94-0.96 in UMAP: UMAP exposed the batch more, not less."),
   A("Output stays in research scope and asks for limits in the caption", "PASS", "No individual-level clinical use; caption template requires hyperparameters and the embedding limit.")]),
]
for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    i["status_flag"] = "❌" if i["status"] in ("PARTIAL", "ERROR") else ("✅" if i["total"] >= 75 else "⚠️")
    i["executed"] = True
    i["execution_note"] = i["note"]
inputs = [{k: i[k] for k in KEYS} for i in inputs]
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
cats = {
 "functional_suitability": (9, 12, "Covers PCA/t-SNE/UMAP/PHATE, hyperparameters, seeds, failure modes, method-choice tables. Gaps: no Python loadings/biplot/legend code despite the promised loadings-arrow request; several inaccurate statements (Rtsne seed=, openTSNE default lr, log+scale fix, 'preserved by construction', PC1=5% heuristic)."),
 "reliability": (8, 12, "Per-method failure modes and a Common Errors table document seed, perplexity, scaling and save-path traps (verified); no guidance on missing optional dependencies (skmisc, leidenalg) or on openTSNE clamping perplexity; recovery is idempotent under seeds."),
 "performance_context": (5, 8, "327-line single SKILL.md carrying dense tables plus a 93-line usage-guide that repeats its tips; no references/ split; example is 84 lines."),
 "agent_usability": (11, 16, "Clear decision tree and 'report all hyperparameters' rule; inconsistencies: 'Perplexity too low' heading vs 'too high' body, 'seed=' vs set.seed, blocks that assume undefined X/labels/pseudotime."),
 "human_usability": (6, 8, "Quick-start prompts, tips and reviewer-pushback table; forgiveness limited: shipped example fails on a missing dependency and a placeholder file with no note."),
 "security": (11, 12, "No credentials or network; reads a local h5ad only; no eval/exec."),
 "maintainability": (7, 12, "One example, no scripts or tests; example depends on an unshipped processed.h5ad and undeclared scikit-misc/leidenalg; version-compatibility block and 'introspect the API' escape hatch are good."),
 "agent_specific": (14, 20, "Good trigger description (63 words, names methods and use cases) and correct Related Skills (all six exist at the commit); all guidance in one file (no progressive disclosure); seeds give idempotency."),
}
subtotal = sum(v[0] for v in cats.values())
sw = round(subtotal * 0.4, 1)
dw = round(avg * 0.6, 1)
score = int(round(sw + dw))
tp = sum(i["assertions_passed"] for i in inputs)
tt = sum(i["assertions_total"] for i in inputs)
l1 = sum(i["basic"] for i in inputs) / len(inputs)
l2 = sum(i["specialized"] for i in inputs) / len(inputs)
print("static", subtotal, "exec", avg, "score", score, sw, dw, "assert", tp, tt, round(100 * tp / tt, 1), "L1", round(l1, 1), "L2", round(l2, 1))
recs = [
 dict(priority="P1", title="Rtsne seed=42 advice is silently ignored", observed_in=[4],
      problem="Failure-mode 'Fix' says set seed=42 for R uwot/Rtsne. Rtsne(seed=42) is absorbed by `...` with no error and two runs differ; only set.seed() (used in the Skill's code block) reproduces. Same wording is in usage-guide Tips.",
      root_cause="One sentence generalises uwot's seed argument to Rtsne.",
      fix="Say: uwot seed=42 or set.seed(42); Rtsne set.seed(42) before the call (Rtsne has no seed argument)."),
 dict(priority="P1", title="'PCA is deterministic' but the sklearn block is not", observed_in=[1],
      problem="SKILL.md calls PCA deterministic and says random_state matters only for t-SNE/UMAP. PCA(n_components=10) on a wide matrix (>500 features) auto-selects the randomized solver; two identical runs gave different scores (max abs diff 15.3) and variance ratios differing by ~1e-4. svd_solver='full' or random_state=42 is reproducible.",
      root_cause="Determinism asserted from the algorithm, not from sklearn's default solver.",
      fix="Add random_state=42 (or svd_solver='full') to the PCA block and drop 'deterministic' unless a seed/solver is fixed."),
 dict(priority="P1", title="Shipped example is not runnable as shipped", observed_in=[3, 6],
      problem="embedding_phd.py stops at highly_variable_genes(flavor='seurat_v3') with 'No module named skmisc'; sc.tl.leiden as written needs leidenalg (or flavor='igraph', n_iterations=2, directed=False in scanpy 1.12); processed.h5ad is not shipped; the usage-guide pip line lists none of scikit-misc, leidenalg, igraph.",
      root_cause="Prerequisites list only the headline packages; example written against placeholder data.",
      fix="Add scikit-misc and leidenalg (or igraph flavor) to Prerequisites, state the input h5ad requirements (raw counts, obs['condition'], >=2000 genes), and use leiden flavor='igraph'."),
 dict(priority="P1", title="Example runs seurat_v3 HVG on log-normalised data", observed_in=[6],
      problem="scanpy warns flavor='seurat_v3' 'expects raw count data'; on the audit data it captured 288/300 planted marker genes vs 295/300 on raw counts and changed 251 of 2000 HVGs.",
      root_cause="HVG call placed after normalize_total/log1p.",
      fix="Run seurat_v3 on raw counts (layer or before normalisation), or use flavor='seurat' after log1p."),
 dict(priority="P1", title="Batch/library-size guidance is inaccurate or incomplete", observed_in=[1, 7],
      problem="'log + scale' is offered as the fix for library-size-driven PC1 but leaves the library-size PC at r = 0.99 (only size-factor normalisation removes it); batch diagnosis is framed as PC1 vs PC2 though the planted batch lived on PC4; 'UMAP can hide batch' was contradicted (UMAP separated it more than PCA).",
      root_cause="Rules of thumb stated as facts without a test.",
      fix="Normalise for library size before log+scale; screen PC1-PC5 (or the top PCs by R2 with batch) for batch; soften the UMAP claim to 'UMAP does not quantify batch; use PCA R2 or kNN batch mixing'."),
 dict(priority="P1", title="Example drops figures and prints a literal caption", observed_in=[6],
      problem="Scree and PHATE figures are built but never saved (2 savefig for 4 figures); caption is a plain string so 'N={n}' prints literally; condition coloured with cmap='tab10' over category codes (blue/cyan for two groups) with no legend.",
      root_cause="Example written as snippets rather than a runnable script.",
      fix="Save all four figures, make caption an f-string, use a categorical palette with a legend."),
 dict(priority="P2", title="openTSNE default statements are wrong for openTSNE", observed_in=[4],
      problem="'learning_rate = n/12, not the default 200' and 'init=pca, NOT random' are already openTSNE 1.0.4 defaults (learning_rate='auto', initialization='pca'); explicit KB settings gave the same result as defaults.",
      root_cause="Kobak-Berens' comparison was against other implementations' defaults.",
      fix="Say these are the openTSNE defaults and only need setting explicitly for Rtsne/sklearn."),
 dict(priority="P2", title="'Local neighborhoods preserved by construction' overstates", observed_in=[7],
      problem="Measured 15-NN retention in 2-D was 0.39-0.41 on real pbmc68k_reduced (UMAP) and 0.14-0.23 on synthetic data.",
      root_cause="Simplified summary of Chari & Pachter.",
      fix="Reword to 'local neighborhoods are only partly preserved (typically well under half of the 15 nearest neighbours)' and give a retention check."),
 dict(priority="P2", title="PC1=5%/PC2=4% 'may be noise' heuristic contradicted", observed_in=[6],
      problem="In the example run PC1 is 1.1% and PC2 1.05% yet the five planted clusters are perfect (ARI 1.0); low variance % is normal for sparse scRNA-seq.",
      root_cause="Bulk-RNA-seq intuition applied to single cell.",
      fix="Limit the heuristic to bulk data or replace with a permutation/elbow check."),
 dict(priority="P2", title="Perplexity failure-mode heading contradicts its body", observed_in=[4],
      problem="Heading 'Perplexity too low for the data' but trigger/mechanism/Common Errors describe perplexity too high; openTSNE clamps with a warning ('Using perplexity 19.67'), Rtsne errors.",
      root_cause="Copy-editing slip.",
      fix="Rename to 'too high for n' and mention both behaviours."),
 dict(priority="P2", title="No Python loadings/biplot/legend code; scanpy seed and save notes", observed_in=[2, 3],
      problem="Loadings-arrow request has no code (PCAtools showLoadings=TRUE, sklearn components_); PCA block has no legend/category mapping; 'without seed results vary' is false for scanpy (random_state=0 default); sc.pl.umap(save=) is deprecated in scanpy 1.12; sklearn's randomized solver on wide matrices moves the variance percentages by up to 0.07 points.",
      root_cause="Blocks are minimal sketches.",
      fix="Add a loadings/biplot snippet and legend, scope the seed claim to umap-learn/uwot/openTSNE, use fig.savefig after show=False."),
 dict(priority="P2", title="usage-guide repeats SKILL.md", observed_in=[],
      problem="Tips section restates SKILL.md failure modes almost line for line.",
      root_cause="Two overlapping documents.",
      fix="Keep the tips in one place and point to it."),
]
report = {
 "meta": {"skill_name": SK,
   "description": "Produce and interpret PCA, t-SNE, UMAP, and PHATE plots for high-dimensional omics data with rigor about which method preserves what (variance, local structure, manifold, transitions), hyperparameter sensitivity, and the limits of 2D embeddings; covers PCA biplot/scree/loadings, t-SNE PCA initialization, UMAP n_neighbors/min_dist, and the Chari-Pachter 2023 critique.",
   "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Complex", "n_inputs": 7,
   "source": "mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/dimensionality-reduction-plots",
   "audit_type": "first audit (unmodified upstream GPTomics/bioSkills)", "executed": True,
   "execution_note": "Executed 7/7 inputs on the data-visualization env (Windows py.sh: scanpy 1.12.4, umap-learn 0.5.12, openTSNE 1.0.4, phate 2.0.0, scikit-learn 1.9.1; r.sh: R 4.4.3, PCAtools 2.18.0, Rtsne 0.17, uwot 0.2.4, ggplot2 4.0.3; WSL Ghostscript to render the example PDFs). Data: synthetic planted clusters/batch/trajectories (run/common.py, seeded) and real airway (Bioconductor) and scanpy pbmc68k_reduced. scikit-misc 0.5.2 and leidenalg 0.12.0 installed with pip --target into run/pylib only (no shared env changed, no install.lock needed). Run order: i0, i1, i1b, i2, i3, i3b, i4, i4b, i4c, i5, i5b, mk_h5ad, ex/embedding_phd.py, i6, i6b, i6c, render_pdf.sh, i7. PNGs under figs/ were opened with the Read tool."},
 "veto_gates": {
   "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
   "research_veto": {"applicable": True, "gate": "PASS",
     "scientific_integrity": {"result": "PASS", "detail": "No fabricated citations or values; the cited papers (Chari & Pachter 2023 PLOS CB e1011288, Kobak & Berens 2019 Nat Commun 10:5416, Becht 2019, Moon 2019, McInnes 2018) match their real bibliographic data."},
     "practice_boundaries": {"result": "PASS", "detail": "Research visualisation only; no individual diagnosis or treatment content."},
     "methodological_ground": {"result": "PASS", "detail": "Core method guidance is sound (seeds, PCA init, refuse to over-read distances, validate in high-dim space). Inaccuracies (log+scale fix, 'preserved by construction', batch-on-PC1/2 rule, seurat_v3 on logged data) are recorded as P1/P2 but do not invert a conclusion."},
     "code_usability": {"result": "PASS", "detail": "Every SKILL.md block executed (7/7 inputs). Leiden as written and the shipped example need packages the pip line omits (leidenalg, scikit-misc) and a data file that is not shipped; the errors are explicit and the fix is one pip install, so recorded as P1, not as unrunnable code."}}},
 "static_score": {"subtotal": subtotal, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": tp, "total": tt}, "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": "Beta Only", "grade_symbol": "⚠️", "deployable": False, "veto_override": False},
 "final_note": "Numeric score 75 (74.8) is Limited Release, but the assertion pass rate is 21/33 = 63.6%, below the 80% floor for Limited Release (scoring_rubric section 5), so the grade drops one tier to Beta Only; deployable is false under the schema rule. Other floors met: static 71 >= 70, execution 77.3 >= 75, Layer 1 avg 31.9 >= 28, Layer 2 avg 45.4 >= 42. No veto fired, no open P0.",
 "key_strengths": [
  "Method-choice content is sound and consistent with what was measured: PCA-init t-SNE beat random init on global structure, UMAP/PHATE/t-SNE reproduce bit-for-bit under the stated seeds, and the guidance not to read inter-cluster UMAP distance as biology is confirmed.",
  "Variance-explained axis labels are correct in both routes: sklearn and PCAtools percentages equal independent SVD/prcomp (p$variance is percent) and colour-by-group mappings are exact.",
  "The scanpy save-path trap, dpi_save default, small-n Rtsne perplexity rule and parameter names for umap-learn, openTSNE, phate, uwot, PCAtools all check out on the installed versions.",
  "Every cited paper is real and correctly referenced; all six Related Skills paths exist at the commit, so shipped-means-present passes."],
 "recommendations": recs}
assert all(len(i["assertions"]) in (3, 4, 5) for i in inputs) and 2 <= len(report["key_strengths"]) <= 5
assert subtotal == sum(v["score"] for v in report["static_score"]["categories"].values())
json.dump(report, open(os.path.join(AUD, "eval_report_%s_result.json" % SK), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written")
