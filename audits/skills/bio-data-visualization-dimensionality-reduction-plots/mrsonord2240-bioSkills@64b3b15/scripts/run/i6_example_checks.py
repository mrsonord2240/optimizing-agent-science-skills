"""Input 6: assertions on the shipped example embedding_phd.py (run copy in run/ex). Re-executes the example's computations to check numbers."""
import numpy as np, scanpy as sc, os, sys, warnings, importlib.util
warnings.filterwarnings('ignore')
sys.path.insert(0, r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\pylib')
os.chdir(r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\ex')
adata = sc.read_h5ad('processed.h5ad')
markers = set(f'g{j}' for j in range(0, 300))   # planted: 5 clusters x 60 marker genes = g0..g299
raw = adata.copy()
# --- (a) HVG on RAW counts (correct use of seurat_v3) vs on log-normalised (the example's order)
a1 = raw.copy(); sc.pp.highly_variable_genes(a1, n_top_genes=2000, flavor='seurat_v3')
a2 = raw.copy(); sc.pp.normalize_total(a2, target_sum=1e4); sc.pp.log1p(a2)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); sc.pp.highly_variable_genes(a2, n_top_genes=2000, flavor='seurat_v3')
    print('warning in example order:', sorted({str(x.message)[:90] for x in w}))
h1 = set(a1.var_names[a1.var.highly_variable]); h2 = set(a2.var_names[a2.var.highly_variable])
print('HVG overlap raw-vs-logged: %d / 2000; planted markers captured  raw: %d/300  log-normalised (example order): %d/300' % (len(h1&h2), len(h1&markers), len(h2&markers)))
# --- (b) PCA variance-ratio labels equal independent computation
a = raw.copy(); sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3'); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=50, random_state=42)
var = a.uns['pca']['variance_ratio']
Xh = a[:, a.var.highly_variable].X; Xh = np.asarray(Xh); Xc = Xh - Xh.mean(0)
s = np.linalg.svd(Xc, compute_uv=False); tv = s**2/np.sum(s**2)
print('scanpy variance_ratio[:3] = %s | independent SVD on HVG-subset = %s' % (np.round(var[:3]*100,2), np.round(tv[:3]*100,2)))
print('PC labels equal to 1 dp:', all(round(var[i]*100,1)==round(tv[i]*100,1) for i in range(2)))
print('use_highly_variable in effect (n genes used by PCA):', int(a.var.highly_variable.sum()), '; a.varm PCs shape', a.varm['PCs'].shape, '; nonzero loading rows', int((np.abs(a.varm['PCs']).sum(1)>0).sum()))
# --- (c) example's t-SNE learning rate arg & final files
for f in ('pca.pdf','tsne.pdf','figures/umap_clusters.pdf'): print(f, os.path.getsize(f), 'bytes')
# --- (d) caption template
src = open('embedding_phd.py', encoding='utf-8').read()
ns = {}; exec("n=1200\ncaption = ('UMAP of N={n} cells.')", ns); print("caption template without f-prefix -> literal:", ns['caption'])
import ast; t = ast.parse(src)
for node in ast.walk(t):
    if isinstance(node, ast.Assign) and getattr(node.targets[0],'id','')=='caption': print('caption node is', type(node.value).__name__, '(JoinedStr=f-string)')
print('savefig calls in example:', src.count('savefig('), ' | scatter/plot figures created:', src.count('plt.subplots('))
