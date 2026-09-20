#!/bin/bash
# NEW input 8: the SKILL's skera block on MY synthetic 6-fold Kinnex array (mk_kinnex3.py), then lima / isoseq refine on the S-reads with Iso-Seq primers.
R=/mnt/openscience/audits/bio-long-read-splicing/run; O=$R/out/kinnex3; rm -rf $O; mkdir -p $O; cd $O; export PYTHONDONTWRITEBYTECODE=1
cp $R/mk_kinnex3.py $R/chk_kinnex3.py .
asenv as-lr python mk_kinnex3.py
cp adapters7.fasta mas16_primers.fasta; cp kinnex3.bam raw_kinnex.bam
echo "### SKILL block: skera split raw_kinnex.bam mas16_primers.fasta segmented.bam"
sed -n '/^skera split/,/^    segmented.bam/p' $R/out/blocks/single-cell-long-read-for-splicing_1.sh
PATH=/home/sci/micromamba/envs/as-pb/bin:$PATH bash $R/out/blocks/single-cell-long-read-for-splicing_1.sh 2>&1 | grep -v "^ *$" | tail -5; echo "block rc=${PIPESTATUS[0]}"
ls segmented*
asenv as-lr python chk_kinnex3.py segmented.bam
echo "### lima (--isoseq) on the S-reads, timeout 150 s"
timeout 150 micromamba run -n as-pb lima segmented.bam primers.fasta fl.bam --isoseq --peek-guess -j 6 2>&1 | tail -12; echo "lima rc=${PIPESTATUS[0]}"; ls fl* 2>/dev/null
if [ -f fl.IsoSeq_5p--IsoSeq_3p.bam ]; then
  timeout 150 micromamba run -n as-pb isoseq refine fl.IsoSeq_5p--IsoSeq_3p.bam primers.fasta flnc.bam --require-polya -j 6 2>&1 | tail -6; echo "refine rc=${PIPESTATUS[0]}"; ls flnc* 2>/dev/null
fi
