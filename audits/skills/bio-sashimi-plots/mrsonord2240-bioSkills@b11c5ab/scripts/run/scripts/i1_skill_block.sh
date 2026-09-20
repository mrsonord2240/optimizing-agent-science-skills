# Input 1a: SKILL.md 'ggsashimi for Publication Overlays' block run literally (only names/region substituted) in the ggplot2 3.4.4 env
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
cd $RUN/data/planted
for FMT in pdf svg png; do
  sed -e "s/ctrl1.bam/G1_rep1.bam/;s/ctrl2.bam/G1_rep2.bam/;s/ctrl3.bam/G1_rep3.bam/;s/trt1.bam/G2_rep1.bam/;s/trt2.bam/G2_rep2.bam/;s/trt3.bam/G2_rep3.bam/" \
      -e "s#chr17:43094000-43125000#chrP:1-1200#;s#BRCA1_sashimi#../../out/i1_skill#g;s#gencode_v45.gtf#planted.gtf#;s#pdf#$FMT#g" $RUN/blocks/02_*.py > $RUN/out/i1_block_$FMT.py
  micromamba run -n as-core python $RUN/out/i1_block_$FMT.py > $RUN/out/i1_block_$FMT.log 2>&1; echo "[$FMT] rc=$?  $(ls -l $RUN/out/i1_skill.$FMT | awk '{print $5}') bytes"
  grep -aiE "error|warn|Traceback" $RUN/out/i1_block_$FMT.log | head -5
done
echo "--- independent truth vs SVG labels (block uses -M default 1 via ggsashimi; -A mean_j)"
micromamba run -n as-core python $RUN/scripts/jtruth.py chrP:1-1200 sashimi_groups.tsv --M 1 --agg mean_j --svg $RUN/out/i1_skill.svg
