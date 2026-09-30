export MAMBA_ROOT_PREFIX=/home/sci/micromamba
source /mnt/openscience/audit-envs/bio-atac-seq-nucleosome-positioning/wsl_env.sh
W=/mnt/openscience/audit-envs/bio-atac-seq-nucleosome-positioning/work/nucleoatac/run1
D=/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/initial-audit-20260930
rm -f $D/logs/na_debug.log
cd $W; mkdir -p dbg; cd dbg
/home/sci/micromamba/envs/atac-nucleo/bin/python $D/scripts/na_debug.py nuc --bed ../r3.bed --bam ../merged.bam --fasta $ATACDATA/reference/hg38.chr1.fa --out d1 --vmat ../out.VMat --occ_track ../out.occ.bedgraph.gz --cores 1 2>&1 | tail -5
cat $D/logs/na_debug.log
