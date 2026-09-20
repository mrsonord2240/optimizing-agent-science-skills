#!/bin/bash
RUN=/mnt/openscience/audits/bio-alignment-validation/run
I=$RUN/data/idx; S=$RUN/skill/examples; W=$RUN/out/work5; rm -rf $W; mkdir -p "$W/my dir"; cd $W
echo "--- determinism: 2 runs each, hash of stdout"
for t in py sh; do
  if [ $t = py ]; then c="python $S/validate_alignment.py"; else c="bash $S/validate_alignment.sh"; fi
  h1=$($c $I/real_human_PE.bam 2>&1 | md5sum | cut -c1-12); h2=$($c $I/real_human_PE.bam 2>&1 | md5sum | cut -c1-12); echo "  $t: $h1 $h2 $([ $h1 = $h2 ] && echo IDENTICAL || echo DIFFER)"
done
echo "--- path with a space (validate_alignment.sh is unquoted)"
cp $I/real_human_PE.bam "$W/my dir/my sample.bam"; cp $I/real_human_PE.bam.bai "$W/my dir/my sample.bam.bai"
bash $S/validate_alignment.sh "$W/my dir/my sample.bam" > sp.out 2> sp.err; echo "  sh rc=$?  stderr lines=$(grep -c . sp.err) first: $(head -1 sp.err | cut -c1-120)"
python $S/validate_alignment.py "$W/my dir/my sample.bam" > sp2.out 2>&1; echo "  py rc=$? verdict: $(grep -E 'All metrics|WARN' sp2.out)"
echo "--- py validator sample_size default 100000: head-of-file bias (1000g slice fine); note only"
echo "--- first-N-reads on coordinate-sorted BAM: fraction of reads sampled on RNA BAM with -n 1000 vs all"
python $S/validate_alignment.py -n 1000 $I/real_human_RNA.bam | grep -E 'sampled|Mapped|Strand|Ratio' | head -4
