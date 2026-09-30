#!/bin/bash
# Clean-install NucleoATAC following usage-guide.md verbatim (env name np-reaudit-nucleoatac), then run without and with the documented patch.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PYTHONDONTWRITEBYTECODE=1
MM=/home/sci/.local/bin/micromamba; N=np-reaudit-nucleoatac; E=/home/sci/micromamba/envs/$N
export HOME=/mnt/openscience/audit-envs/bio-atac-seq-nucleosome-positioning/work/na27_home
BASE=/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/reaudit-run
DATA=/mnt/openscience/audit-envs/atac-seq/public-data
TOOLS=/home/sci/micromamba/envs/bio-atac-seq-nucleosome-positioning/bin
( exec 9>/mnt/openscience/runtime/locks/micromamba-mutate.lock; flock 9
  $MM env remove -y -n $N >/dev/null 2>&1
  # --- usage-guide prerequisites, verbatim except env name
  $MM create -n $N -c conda-forge -c bioconda --override-channels python=2.7 nucleoatac "cython<3" > $BASE/logs/na_create.log 2>&1; echo "create rc=$?" )
$MM list -n $N | grep -E " (python|nucleoatac|cython|numpy|scipy|pysam) "
$MM list -n $N --explicit --md5 > $BASE/env-np-reaudit-nucleoatac.explicit.txt
W=$BASE/out/na; rm -rf $W; mkdir -p $W; cd $W
$TOOLS/samtools merge -f -@4 merged.bam $DATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam $DATA/encode/GM12878_rep2_filtered.chr1_1-30000000.bam && $TOOLS/samtools index merged.bam
# Skill step 5 verbatim: bedtools slop -l 200 -r 1000 on protein-coding TSS
awk '$2>10000000 && $2<20000000' $DATA/annotation/gencode_v29_protein_coding_tss.chr1.bed | cut -f1-3 > tss.bed
$TOOLS/bedtools slop -i tss.bed -g $DATA/reference/hg38.chr1.chrom.sizes -l 200 -r 1000 | sort -k1,1 -k2,2n | $TOOLS/bedtools merge -i - > regions.bed
echo regions $(wc -l < regions.bed) minlen $(awk '{print $3-$2}' regions.bed | sort -n | head -1)
run() { ( time $MM run -n $N nucleoatac run --bed regions.bed --bam merged.bam --fasta $DATA/reference/hg38.chr1.fa --out $1 --cores 8 ) > $1.log 2>&1; echo "$1 rc=$?"; for f in $1.nucpos.bed.gz $1.nucpos.redundant.bed.gz $1.occ.bedgraph.gz $1.nfrpos.bed.gz; do echo "$f $(zcat $f | wc -l)"; done; }
echo "== as installed"; run ctrl
# --- usage-guide patch lines verbatim (name adapted)
P=$($MM run -n $N python -c "import nucleoatac,os;print(os.path.dirname(nucleoatac.__file__))")
grep -n "cdef DTYPE_t value" $P/multinomial_cov.pyx
sed -i 's/cdef DTYPE_t value$/cdef DTYPE_t value = 0/' $P/multinomial_cov.pyx
(cd $P && CFLAGS="-I$($MM run -n $N python -c 'import numpy;print(numpy.get_include())')"     $MM run -n $N cythonize -i multinomial_cov.pyx > $W/cythonize.log 2>&1; echo cythonize rc=$?)
grep -n "cdef DTYPE_t value" $P/multinomial_cov.pyx
echo "== patched"; run patched
zcat patched.nucpos.bed.gz | head -3
