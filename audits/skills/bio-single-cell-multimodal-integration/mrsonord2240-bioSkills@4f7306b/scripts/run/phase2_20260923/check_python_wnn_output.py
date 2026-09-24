"""Assert the copied shipped CITE-seq example produced all required Muon WNN artifacts."""
from pathlib import Path

import mudata as md

path = Path("cite_seq_analyzed.h5mu")
if not path.exists():
    raise SystemExit("Missing cite_seq_analyzed.h5mu")
mdata = md.read_h5mu(path)
for modality in ("rna", "prot"):
    if "neighbors" not in mdata.mod[modality].uns:
        raise SystemExit(f"Missing modality-local neighbors for {modality}")
    if "connectivities" not in mdata.mod[modality].obsp:
        raise SystemExit(f"Missing modality-local connectivity graph for {modality}")
if "wnn_connectivities" not in mdata.obsp:
    raise SystemExit("Missing Muon WNN connectivity graph")
if "wnn_clusters" not in mdata.obs:
    raise SystemExit("Missing WNN clusters")
print(
    "PYTHON_WNN_OUTPUT",
    f"n_obs={mdata.n_obs}",
    f"modalities={','.join(mdata.mod)}",
    f"wnn_nnz={mdata.obsp['wnn_connectivities'].nnz}",
    f"clusters={mdata.obs['wnn_clusters'].nunique()}",
)
