#!/bin/bash
# VerifyBamID2 with the Skill's prefix (with .dat) on the real 1000G chr20 slice: does it reach the marker check, and what does it say?
PD=/mnt/openscience/audit-envs/alignment-files/public-data; G=$PD/1000g; W=/mnt/openscience/audits/bio-alignment-validation/run/out/work_vb; rm -rf $W; mkdir -p $W
verifybamid2 --SVDPrefix $PD/resources/1000g.phase3.10k.b38.vcf.gz.dat --Reference $G/chr20_padded_1500000.fa --BamFile $G/HG00349.chr20_1400000-1500000.bam --Output $W/sample.contam > $W/vb_dat.log 2>&1; echo "rc=$?"
grep -a -E 'NOTICE|Insufficient|ERROR|FREEMIX|WARNING' $W/vb_dat.log | head -6 | cut -c1-200
ls $W
