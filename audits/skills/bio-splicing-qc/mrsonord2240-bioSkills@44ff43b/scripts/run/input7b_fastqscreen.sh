#!/bin/bash
# fastq_screen retry with minimap2 indexes (.mmi) built for the synthetic rRNA / genome
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
cd /mnt/openscience/audits/bio-splicing-qc/run/work/in7
gzip -kf rrna.fa; gzip -kf genome.fa; minimap2 -d rrna.mmi rrna.fa 2>&1 | tail -1
minimap2 -d genome.mmi genome.fa 2>&1 | tail -1
cat > fastq_screen_mm2.conf <<EOC
DATABASE	rRNA	/mnt/openscience/audits/bio-splicing-qc/run/work/in7/rrna
DATABASE	Genome	/mnt/openscience/audits/bio-splicing-qc/run/work/in7/genome
EOC
fastq_screen --force --conf fastq_screen_mm2.conf --aligner minimap2 --threads 4 sample_R1.fq.gz > fs_mm2b.log 2>&1; echo "rc=$?"
tr '\r' '\n' < fs_mm2b.log | tail -5
cat sample_R1_screen.txt
