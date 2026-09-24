import inspect
import muon as mu
import scanpy as sc

print(f"muon_umap_present={hasattr(mu.tl, 'umap')}")
if hasattr(mu.tl, "umap"):
    print(f"muon_umap_signature={inspect.signature(mu.tl.umap)}")
print(f"scanpy_umap_signature={inspect.signature(sc.tl.umap)}")
