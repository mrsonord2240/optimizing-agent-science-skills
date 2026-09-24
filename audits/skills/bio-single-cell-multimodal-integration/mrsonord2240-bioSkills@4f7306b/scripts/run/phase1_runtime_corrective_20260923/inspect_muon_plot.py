import inspect
import muon as mu
import scanpy as sc

print(f"muon_plot_umap_present={hasattr(mu.pl, 'umap')}")
if hasattr(mu.pl, "umap"):
    print(f"muon_plot_umap_signature={inspect.signature(mu.pl.umap)}")
print(f"scanpy_plot_umap_signature={inspect.signature(sc.pl.umap)}")
