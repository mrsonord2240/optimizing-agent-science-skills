source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/planted
asenv as-core python $RUN/scripts/junction_truth.py chrP 1 1200 G1_rep1.bam G1_rep2.bam G1_rep3.bam G2_rep1.bam G2_rep2.bam G2_rep3.bam
