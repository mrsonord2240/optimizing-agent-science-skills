#!/bin/bash
# INPUT 6 add-on (NEW, SYNTHETIC): end-to-end VerifyBamID2 with the Skill's block 034 command (real 10k SVD panel, synthetic chr20 reference+BAM)
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; P=/mnt/openscience/audit-envs/alignment-files/public-data/resources
python $R/t10_make_vb2_data.py
cd vb2
timeout 300 verifybamid2 --SVDPrefix $P/1000g.phase3.10k.b38.vcf.gz.dat --Reference chr20.fa --BamFile vb2.bam --Output sample_vb 2>&1 | tail -8
ls sample_vb* 2>&1; cat sample_vb.selfSM 2>&1 | head -3
