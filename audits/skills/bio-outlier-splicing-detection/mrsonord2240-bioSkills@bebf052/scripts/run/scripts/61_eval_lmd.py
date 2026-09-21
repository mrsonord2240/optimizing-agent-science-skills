# Evaluate LeafcutterMD output vs planted truth (SYNTHETIC). Usage: python 61_eval_lmd.py <lmd_dir> <synth_dir>
import sys, pandas as pd, numpy as np
d, synth = sys.argv[1], sys.argv[2]
cp = pd.read_csv(f"{d}/patient_outlier_clusterPvals.txt", sep="\t", index_col=0)
es = pd.read_csv(f"{d}/patient_outlier_effSize.txt", sep="\t", index_col=0)
pv = pd.read_csv(f"{d}/patient_outlier_pVals.txt", sep="\t", index_col=0)
truth = pd.read_csv(f"{synth}/planted_truth.tsv", sep="\t")
print("cluster p-value matrix:", cp.shape, "; intron p-value matrix:", pv.shape, "; effSize:", es.shape)
print("cluster index example:", cp.index[:3].tolist())
def bh(p):
    p = np.asarray(p, float); n = np.sum(~np.isnan(p)); o = np.argsort(np.where(np.isnan(p), 2, p)); r = np.empty_like(o); r[o] = np.arange(1, len(p)+1)
    q = np.minimum.accumulate((p[o] * n / np.arange(1, len(p)+1))[::-1])[::-1]; out = np.empty_like(q); out[o] = np.minimum(q, 1); out[np.isnan(p)] = np.nan; return out
flat = cp.stack(future_stack=True).dropna().reset_index(); flat.columns = ["cluster", "sample", "p"]
flat["q"] = bh(flat["p"].values)
# cluster ids carry no coordinates: map them from the intron-level rows chr:start:end:clu_N_strand
ix = pd.Series(pv.index).str.extract(r"^(?P<chrom>[^:]+):(?P<s>\d+):(?P<e>\d+):(?P<clu>.+)$"); ix["s"] = ix.s.astype(int); ix["e"] = ix.e.astype(int)
cmin = ix.groupby("clu").s.min(); cmax = ix.groupby("clu").e.max()
flat["start"] = flat.cluster.map(cmin); flat["end"] = flat.cluster.map(cmax)
print("clusters with coordinates:", int(flat.start.notna().sum()), "of", len(flat))
print("tested cluster-sample pairs:", len(flat), "; raw p<0.05:", int((flat.p < 0.05).sum()), "; BH q<0.05:", int((flat.q < 0.05).sum()))
planted_splice = truth[truth.type.isin(["exon_skipping","cryptic_donor","intron_retention","pseudoexon"])]
hit_pairs = set()
for _, t in planted_splice.iterrows():
    m = flat[(flat["sample"] == t["sample"]) & (flat.end >= t.gene_start) & (flat.start <= t.gene_end)]
    best = m.sort_values("p").head(1)
    if len(best):
        print(f"{t['sample']} {t.gene} {t.type:17s}: cluster {best.cluster.iloc[0]}  raw p={best.p.iloc[0]:.2e}  BH q={best.q.iloc[0]:.2e}  -> {'DETECTED' if best.q.iloc[0] < 0.05 else 'not detected at BH<0.05'}")
        hit_pairs.add((t["sample"], best.cluster.iloc[0]))
    else: print(f"{t['sample']} {t.gene} {t.type}: no cluster tested for that gene/sample")
truth_s = {(t["sample"], t.gene_start, t.gene_end) for _, t in truth.iterrows()}
def planted_gene(row): return any(row["sample"] == s and row.end >= a and row.start <= b for s, a, b in truth_s)
flat["planted"] = flat.apply(planted_gene, axis=1)
fp = flat[(~flat.planted) & (flat["sample"] != "S29")]
print("NON-planted, excl. S29: raw p<0.05:", int((fp.p < 0.05).sum()), f"(of {len(fp)}; {100*(fp.p<0.05).mean():.1f}%) ; BH q<0.05:", int((fp.q < 0.05).sum()))
print("NON-planted, excl. S29: raw p<0.001:", int((fp.p < 1e-3).sum()))
print("S29 tissue-mismatch: BH q<0.05:", int(((flat['sample']=='S29') & (flat.q < 0.05)).sum()))
