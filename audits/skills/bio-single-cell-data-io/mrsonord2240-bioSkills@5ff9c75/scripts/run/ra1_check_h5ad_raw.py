import h5py

PATH = "F:/OpenScience/audits/bio-single-cell-data-io/data/ra1_rich.h5ad"
with h5py.File(PATH, "r") as f:
    print("Top-level keys:", list(f.keys()))
    assert "raw" in f, "raw group missing from file entirely"
    raw = f["raw"]
    print("raw/ keys:", list(raw.keys()))
    idx = raw["var"]["_index"]
    idx_len = idx.shape if hasattr(idx, "shape") else len(list(idx.keys()))
    print("raw/var/_index:", idx_len)
    print("raw X attrs shape:", dict(raw["X"].attrs).get("shape"))
print("CONFIRMED: /raw group genuinely present in the h5ad file, independent of scanpy.")
