# ecosystem-workflows.md SnapATAC2 block on real 10x PBMC 5k chr1 slice (fragments.tsv.gz).
# Steps that fail as documented are printed as DOC-AS-WRITTEN ... FAILED, then a minimal workaround is applied.
import os, time, numpy as np
import snapatac2 as snap
SCA = os.environ["SCA"]; D = os.environ["ATACDATA"]
os.makedirs(f"{SCA}/work/snap", exist_ok=True); os.chdir(f"{SCA}/work/snap")
FR = f"{D}/scatac/outs/fragments.tsv.gz"
print("snapatac2", snap.__version__, "| import_data:", hasattr(snap.pp, "import_data"),
      "import_fragments:", hasattr(snap.pp, "import_fragments"), "read_10x:", hasattr(snap, "read_10x"))

_n = [0]
def load():
    _n[0] += 1
    d = snap.pp.import_fragments(fragment_file=FR, chrom_sizes=snap.genome.hg38, file=f"out{_n[0]}.h5ad",
                                 sorted_by_barcode=False, min_num_fragments=200)
    snap.metrics.tsse(d, gene_anno=snap.genome.hg38); snap.metrics.frag_size_distr(d)
    return d

t = time.time(); data = load(); print("imported", data.n_obs, "barcodes", round(time.time() - t), "s")
try:
    data.obs["sample_id"] = "rep1"
except Exception as e:
    print("DOC-AS-WRITTEN data.obs['sample_id']='rep1' FAILED:", e)
    data.obs["sample_id"] = ["rep1"] * data.n_obs
o = data.obs[:]; print(o.select(["n_fragment", "tsse"]).describe())
snap.pp.filter_cells(data, min_counts=1000, min_tsse=4)
print("after DOCUMENTED filter (min_counts=1000,min_tsse=4):", data.n_obs, "(chr1 slice is ~3% of genome; ~0 expected)")
if data.n_obs == 0:
    data.close(); data = load()
    snap.pp.filter_cells(data, min_counts=400, min_tsse=0.3)
print("after relaxed filter (400, 0.3):", data.n_obs)
snap.pp.add_tile_matrix(data, bin_size=500)
snap.pp.select_features(data, n_features=250000)
snap.tl.spectral(data); snap.tl.umap(data)
try:
    snap.tl.leiden(data)
except Exception as e:
    print("DOC-AS-WRITTEN leiden without snap.pp.knn FAILED:", e)
    snap.pp.knn(data); snap.tl.leiden(data)
o = data.obs[:]
print("clusters", o["leiden"].value_counts().sort("count", descending=True).to_dicts()[:12])
print("obsm", list(data.obsm.keys()))
try:
    import logging; logging.basicConfig(level=logging.INFO)
    r = snap.tl.macs3(data, groupby="leiden", n_jobs=1); print("macs3 ok; uns keys", list(data.uns.keys()))
except Exception as e:
    import traceback; traceback.print_exc(); print("macs3 FAILED", type(e).__name__, str(e)[:400])
try:
    gm = snap.pp.make_gene_matrix(data, gene_anno=snap.genome.hg38)
    print("gene matrix", gm.shape, "nnz", gm.X.nnz)
    tot = np.asarray(gm.X.sum(0)).ravel()
    print("top10 genes", [gm.var_names[i] for i in np.argsort(-tot)[:10]])
except Exception as e:
    print("make_gene_matrix FAILED", type(e).__name__, str(e)[:400])
data.close()
