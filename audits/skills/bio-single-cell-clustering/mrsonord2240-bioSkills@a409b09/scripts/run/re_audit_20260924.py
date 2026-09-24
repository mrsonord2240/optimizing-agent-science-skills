"""Focused exact-commit re-audit for bio-single-cell-clustering."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import re

import anndata as ad
import numpy as np
import pandas as pd


COMMIT = "a409b098b3602b13d7c40610f1c6bc09057258ac"
SKILL = Path(r"F:\OpenScience\worktrees\bio-single-cell-clustering-fixpass\single-cell\clustering")


def load_helper():
    spec = spec_from_file_location("validate_partition", SKILL / "examples" / "validate_partition.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    print(f"source_commit={COMMIT}")

    # Regressions 1-5: all prior audit claims are retained or corrected in source.
    assert "flavor='igraph', n_iterations=2, directed=False" in text
    assert "max(elbow, ~30)" in text
    print("input1_reproducible_leiden_and_pc_rule=PASS")

    assert "leidenbase" in text and "install.packages('leidenbase')" in text
    assert "reticulate" in text
    print("input2_seurat5_leiden_dependency=PASS")

    assert "ARI({cluster_key}, {covariate})" in text
    assert "mean bootstrap Jaccard by cluster" in text
    assert "marker overlap alone cannot decide" in text
    print("input3_batch_split_stop_rule=PASS")

    assert "does not reproduce in an independent sample" in text
    assert "Do not use distinct markers or post-clustering p-values as a stop rule" in text
    print("input4_subclustering_stop_rule=PASS")

    assert "marker genes as ranking or annotation evidence only" in text
    assert "What to report from a sweep" in text
    print("input5_double_dipping_and_reporting=PASS")

    # New input 6: execute the helper's validation and Jaccard aggregation without
    # rerunning a graph algorithm; that algorithm is separately exercised in the
    # original Scanpy audit runs. The deterministic mock returns the selected labels.
    helper = load_helper()
    rng = np.random.default_rng(24)
    adata = ad.AnnData(np.zeros((40, 5)))
    adata.obsm['X_pca'] = rng.normal(size=(40, 5))
    adata.obs['candidate'] = pd.Categorical(['0'] * 20 + ['1'] * 20)
    adata.obs['batch'] = pd.Categorical(['b1'] * 20 + ['b2'] * 20)
    original_neighbors = helper.sc.pp.neighbors
    original_leiden = helper.sc.tl.leiden

    def fake_leiden(obj, **kwargs):
        obj.obs[kwargs['key_added']] = pd.Categorical(obj.obs['candidate'].astype(str))

    helper.sc.pp.neighbors = lambda *args, **kwargs: None
    helper.sc.tl.leiden = fake_leiden
    try:
        stability = helper.partition_checks(
            adata, 'candidate', covariates=('batch',), resolution=0.4,
            n_neighbors=8, n_pcs=5, n_bootstrap=2, seed=24)
    finally:
        helper.sc.pp.neighbors = original_neighbors
        helper.sc.tl.leiden = original_leiden
    assert len(stability) == 2 and float(stability.min()) == 1.0
    try:
        helper.partition_checks(adata, 'missing', n_bootstrap=1)
    except KeyError:
        pass
    else:
        raise AssertionError("missing labels did not raise KeyError")
    print(f"input6_helper_clusters={len(stability)} min_jaccard={stability.min():.3f} missing_key=PASS")

    # New input 7: all Python snippets compile and formal testing fails clearly
    # rather than falling back to invalid marker p-values when scSHC is unavailable.
    blocks = re.findall(r"```python\n(.*?)```", text, flags=re.S)
    for index, block in enumerate(blocks, start=1):
        compile(block, f"SKILL-python-block-{index}", "exec")
    assert "requireNamespace('scSHC', quietly = TRUE)" in text
    assert "scSHC::scSHC(expr_hvg)" in text
    print(f"input7_python_blocks_compiled={len(blocks)} scSHC_guard=PASS")


if __name__ == "__main__":
    main()
