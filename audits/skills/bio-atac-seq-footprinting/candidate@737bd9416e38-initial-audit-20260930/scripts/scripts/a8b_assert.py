"""A8b: assertions on the A8 footprint h5ad (separate process: scPrinter holds an HDF5 lock while the compute process is alive)."""
import glob, numpy as np, pandas as pd, anndata
from scipy.stats import mannwhitneyu
W="/mnt/openscience/audit-envs/bio-atac-seq-footprinting/audit-20260930"
A="/mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930"
R=pd.read_csv(f"{A}/out/a8_scprinter_regions.tsv",sep="	")
f=glob.glob(f"{W}/a8/*supp*/*ctcf*")[0]; ad=anndata.read_h5ad(f)
lab=dict(zip(R.chrom+":"+R.start.astype(str)+"-"+R.end.astype(str),R.cls))
keys=list(ad.obsm.keys()); M=np.stack([np.asarray(ad.obsm[k])[0] for k in keys]); cls=np.array([lab[k] for k in keys])
print("array",M.shape,"finite",np.isfinite(M).all(),{c:int((cls==c).sum()) for c in set(cls)})
modes=list(range(2,101)); b=cls=="bound"; ok=True
for m in (10,20,30,50):
    i=modes.index(m); c=M[:,i,90:110].mean(1); p=mannwhitneyu(c[b],c[~b],alternative="greater").pvalue
    print(f"mode{m}: centre bound={c[b].mean():.3f} unbound={c[~b].mean():.3f} p(bound>unbound)={p:.1e}")
# positional check: at mode 20 the score should peak near the motif centre (+/-25 bp) for bound sites
i=modes.index(20); prof=M[b][:,i].mean(0); pk=int(np.argmax(prof))-100
print("mode20 bound-site profile argmax offset from centre (bp):",pk)
