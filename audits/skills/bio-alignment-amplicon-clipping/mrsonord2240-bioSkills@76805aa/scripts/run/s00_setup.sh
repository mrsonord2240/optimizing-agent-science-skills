# Regenerate the SYNTHETIC data (deterministic seed) used by the pre-fix audit, for regression.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
cd $R
python make_synth.py
python s3a_strand_cases_make.py
ls -la data
md5sum data/synth.fa data/synth_primers.bed
md5sum /mnt/openscience/audits/_pre-fix-20260920/bio-alignment-amplicon-clipping/run/data/synth.fa /mnt/openscience/audits/_pre-fix-20260920/bio-alignment-amplicon-clipping/run/data/synth_primers.bed
samtools view data/synth_pe.bam | md5sum; samtools view /mnt/openscience/audits/_pre-fix-20260920/bio-alignment-amplicon-clipping/run/data/synth_pe.bam | md5sum
