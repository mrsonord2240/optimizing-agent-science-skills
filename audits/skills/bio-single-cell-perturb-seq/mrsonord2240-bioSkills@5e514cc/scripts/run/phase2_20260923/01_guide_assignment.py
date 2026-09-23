"""Phase 2 input 1: execute the documented mixture guide-assignment path."""
from pathlib import Path
import mudata as md
import pertpy as pt

data = Path(r"F:/OpenScience/audits/bio-single-cell-perturb-seq/run/data/papalexi_2021.h5mu")
mdata = md.read_h5mu(data, backed=None)
gdo = mdata.mod["gdo"][:500].copy()
gdo.X = gdo.X.tocsr()
gdo.layers["counts"] = gdo.X.copy()
ga = pt.pp.GuideAssignment()
try:
    ga.assign_mixture_model(gdo, assigned_guides_key="assigned_guide")
    assigned = gdo.obs["assigned_guide"]
    assert assigned.notna().all() and assigned.nunique() >= 2
    print(f"PASS mixture assignment: cells={gdo.n_obs}, guide labels={assigned.nunique()}")
except ImportError as exc:
    ga.assign_by_threshold(gdo, assignment_threshold=5, output_layer="assigned_guides")
    assert "assigned_guides" in gdo.layers and gdo.layers["assigned_guides"].sum() > 0
    print(f"PARTIAL documented fallback executed: {exc}; assigned entries={gdo.layers['assigned_guides'].sum()}")
