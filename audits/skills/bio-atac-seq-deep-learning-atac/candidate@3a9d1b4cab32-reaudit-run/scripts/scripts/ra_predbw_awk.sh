# Re-audit: documented 3-col BED -> 10-col narrowPeak one-liner, then pred_bw (models from ra_pipe_run1 output)
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH
P=$ME/public-cache/pseudo; O=$ME/run/reaudit/pipe; W=$ME/run/reaudit/predbw; rm -rf $W; mkdir -p $W; export TMPDIR=$W
awk -F'\t' '$1=="chrP1"{print $1"\t"$2"\t"$3}' $P/pseudo.narrowPeak | head -40 > $W/r3.bed; head -3 $W/r3.bed >> $W/r3.bed   # 3 duplicate rows appended, unsorted
echo "-- raw 3-col + dup rows (expect failure)"
chrombpnet pred_bw -cmb $O/model/models/chrombpnet_nobias.h5 -bm $O/bias/models/bias.h5 -cm $O/model/models/chrombpnet.h5 -r $W/r3.bed -g $P/pseudo.fa -c $P/pseudo.chrom.sizes -op $W/raw 2>&1 | grep -E "Error" | tail -2
echo "-- documented one-liner"
sort -k1,1 -k2,2n -u $W/r3.bed | awk -v OFS='\t' '{print $1,$2,$3,".",0,".",0,0,0,int(($3-$2)/2)}' > $W/r10.bed; wc -l $W/r10.bed; head -2 $W/r10.bed
chrombpnet pred_bw -cmb $O/model/models/chrombpnet_nobias.h5 -bm $O/bias/models/bias.h5 -cm $O/model/models/chrombpnet.h5 -r $W/r10.bed -g $P/pseudo.fa -c $P/pseudo.chrom.sizes -op $W/ok 2>&1 | grep -E "Error|Traceback" | tail -3; ls $W
py_torch - <<PY
import pyBigWig, numpy as np
for n in ["ok_chrombpnet_nobias.bw","ok_bias.bw","ok_chrombpnet.bw"]:
    b=pyBigWig.open("$W/"+n); tot=0; nz=0
    for l in open("$W/r10.bed"):
        c,s,e=l.split()[:3]; v=np.nan_to_num(np.array(b.values(c,int(s),int(e)))); tot+=v.sum(); nz+=int((v!=0).sum())
    print(n,"sum in regions",round(float(tot),1),"nonzero bins",nz, "chroms",list(b.chroms())[:2])
PY
