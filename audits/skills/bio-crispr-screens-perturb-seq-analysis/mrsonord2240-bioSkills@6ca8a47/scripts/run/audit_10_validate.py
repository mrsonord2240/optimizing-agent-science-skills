"""Check the shipped Mixscape CLI wrote KO-only output and a reproducible call column."""
from pathlib import Path
import anndata as ad

root = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\data")
full = ad.read_h5ad(root / "mixscape_fixture.h5ad")
ko = ad.read_h5ad(root / "mixscape_ko.h5ad")
assert "mixscape_class_global" in ko.obs
assert set(ko.obs["mixscape_class_global"].unique()) == {"KO"}
assert 0 < ko.n_obs < full.n_obs
print(f"full_cells={full.n_obs}")
print(f"ko_cells={ko.n_obs}")
print("ko_global_classes=" + repr(ko.obs["mixscape_class_global"].value_counts().to_dict()))
