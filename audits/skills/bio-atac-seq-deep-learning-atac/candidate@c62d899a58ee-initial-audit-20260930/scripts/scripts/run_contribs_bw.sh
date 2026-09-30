# Skill step "motif discovery: chrombpnet contribs_bw ... convert to numpy via shap_to_modisco".
# Bounded: 20 real-derived peak regions, trained chrombpnet_nobias.h5 from the tooling run. timeout 1500.
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH
P=$ME/public-cache/pseudo; S=$ME/run/skillscript; R=/mnt/openscience/audits/bio-atac-seq-deep-learning-atac/initial-audit-20260930/runs/contribs; rm -rf $R; mkdir -p $R; cd $R
export TMPDIR=$R/tmp; mkdir -p $TMPDIR
head -20 $P/pseudo.narrowPeak > regions20.bed
( time timeout 1500 chrombpnet contribs_bw -m $S/out/model/models/chrombpnet_nobias.h5 -r regions20.bed -g $P/pseudo.fa -c $P/pseudo.chrom.sizes -op $R/contrib -pc counts ) 2>&1 | grep -v -E "it/s\]|^[0-9]+it \[|Warning:" | tail -25
echo "exit=${PIPESTATUS[0]}"; ls -la $R
python - <<'P'
import glob
try:
    import pyBigWig
    for f in glob.glob('contrib*.bw'):
        b=pyBigWig.open(f); print(f,b.chroms()); 
        import numpy as np
        tot=0;nz=0
        for c,l in b.chroms().items():
            v=np.nan_to_num(np.array(b.values(c,0,l),dtype=float)); tot+=v.size; nz+=int((v!=0).sum())
        print('nonzero bins',nz,'of',tot)
except Exception as e: print('ERR',e)
P
