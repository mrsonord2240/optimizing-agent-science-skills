"""Prior Edge regression: symbols succeed and Ensembl IDs hard-fail with zero overlap."""
from pathlib import Path

import pandas as pd
import scanpy as sc
import celltypist

DATA = Path(r"F:\OpenScience\audits\_partial-20260911\bio-workflows-scrnaseq-pipeline\data\synthetic_pbmc_8samples")
MODEL = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl")
a = sc.read_h5ad(DATA / "all_samples_filtered.h5ad")
truth = pd.read_csv(DATA / "truth_cells.csv").set_index("cell_id").loc[a.obs_names]
a = a[(~truth["true_doublet"].astype(bool) & ~truth["true_low_quality"].astype(bool)).values][:2000].copy()
model = celltypist.models.Model.load(model=MODEL.resolve().as_posix())
for label, ensembl in (("symbols", False), ("ensembl", True)):
    q = a.copy()
    if ensembl:
        q.var_names = q.var["gene_ids"].astype(str).values
        q.var_names_make_unique()
    sc.pp.normalize_total(q, target_sum=1e4); sc.pp.log1p(q)
    matched = len(set(model.classifier.features) & set(q.var_names))
    try:
        result = celltypist.annotate(q, model=model, majority_voting=False)
    except ValueError as exc:
        print(f"{label}: matched={matched}/{len(model.classifier.features)} error={exc}")
        assert ensembl and matched == 0 and "No features overlap" in str(exc)
    else:
        print(f"{label}: matched={matched}/{len(model.classifier.features)} labels={result.predicted_labels.iloc[:,0].nunique()}")
        assert not ensembl and matched > 1000
print("gene identifier regression PASS")
