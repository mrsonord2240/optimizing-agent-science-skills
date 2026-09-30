"""A8: scPrinter 1.2.0 classic multi-scale footprinting (bulk GM12878 fragments, chr1) at TOBIAS-A1-bound vs unbound CTCF sites.
Reuses tooling-pass artifacts (chr1 Tn5 bias.h5 predicted on GPU, frags.tsv.gz built from the same BAM); redoes import_fragments, get_footprint_score
and assertions here, with bound/unbound labels taken from THIS audit's A1 BINDetect beds. Skill has no scPrinter code, so the API calls follow the scPrinter docs."""
import os, sys, time, glob
S="/mnt/openscience/audit-envs/bio-atac-seq-footprinting/scprinter"   # tooling-pass cache (bias.h5, frags, models)
W="/mnt/openscience/audit-envs/bio-atac-seq-footprinting/audit-20260930"
A="/mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930"
os.environ["SCPRINTER_DATA"]=S
import numpy as np, pandas as pd, torch, anndata
import scprinter as scp
from scipy.stats import mannwhitneyu
PD="/mnt/openscience/audit-envs/atac-seq/public-data"
B=f"{W}/a1/out/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_"
print("scprinter", scp.__version__, "cuda", torch.cuda.is_available())
os.makedirs(f"{W}/a8",exist_ok=True); sav=f"{W}/a8/a8.h5ad"
for f in glob.glob(f"{W}/a8/*"):
    if os.path.isfile(f): os.remove(f)
genome=scp.genome.Genome(name="hg38chr1", fa_file=f"{PD}/reference/hg38.chr1.fa", gff_file=f"{S}/gencode.v29.chr1.gtf", bias_file=f"{S}/bias.h5", blacklist_file=f"{S}/hg38-blacklist.v2.bed")
printer=scp.pp.import_fragments(path_to_frags=[f"{S}/frags.tsv.gz"], barcodes=[None], savename=sav, genome=genome, min_num_fragments=1000, min_tsse=0, sorted_by_barcode=False, low_memory=False)
print(printer)
def load(n):
    d=pd.read_csv(B+f"cond1_{n}.bed",sep="\t",header=None); d=d[(d[0]=="chr1")&(d[1]>2000)&(d[2]<29990000)]
    return d.sample(200,random_state=1)
R=pd.concat([pd.DataFrame({"chrom":"chr1","start":((d[1]+d[2])//2).astype(int)-100,"end":((d[1]+d[2])//2).astype(int)+100,"cls":n}) for n in ("bound","unbound") for d in [load(n)]],ignore_index=True)
R.to_csv(f"{A}/out/a8_scprinter_regions.tsv",sep="\t",index=False)
printer.load_disp_model()
t=time.time()
scp.tl.get_footprint_score(printer,[list(printer.obs_names)],["GM12878"],R[["chrom","start","end"]],region_width=200,modes=np.arange(2,101),footprintRadius=None,flankRadius=None,n_jobs=4,save_key="ctcf",backed=True,overwrite=True)
print("footprint seconds", time.time()-t)
