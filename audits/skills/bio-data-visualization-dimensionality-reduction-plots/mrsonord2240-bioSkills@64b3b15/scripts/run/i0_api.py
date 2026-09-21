import inspect, importlib
for m in ['scanpy','umap','openTSNE','phate','sklearn','anndata','matplotlib','leidenalg','igraph','skmisc','numpy','pandas']:
    try:
        mod=importlib.import_module(m); print(m, getattr(mod,'__version__','?'))
    except Exception as e: print(m,'MISSING',e)
import openTSNE, umap, phate, scanpy as sc
print('openTSNE.TSNE sig:', inspect.signature(openTSNE.TSNE.__init__))
print('umap.UMAP has n_neighbors,min_dist,spread,init,random_state:', [p for p in ['n_neighbors','min_dist','spread','init','random_state','metric'] if p in inspect.signature(umap.UMAP.__init__).parameters])
print('PHATE sig:', inspect.signature(phate.PHATE.__init__))
print('sc.tl.umap:', inspect.signature(sc.tl.umap))
print('sc.tl.pca:', inspect.signature(sc.tl.pca))
print('sc.tl.leiden:', inspect.signature(sc.tl.leiden))
print('sc.pl.umap:', inspect.signature(sc.pl.umap))
print('sc.set_figure_params:', inspect.signature(sc.set_figure_params))
print('sc.pp.hvg:', inspect.signature(sc.pp.highly_variable_genes))
print('sc.pp.neighbors:', inspect.signature(sc.pp.neighbors))
