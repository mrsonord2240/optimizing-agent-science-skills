#!/bin/bash
RUN=/mnt/openscience/audits/bio-alignment-validation/run
W=$RUN/out/work4; rm -rf $W; mkdir -p $W; cd $W
B=$RUN/data/idx/real_human_PE.bam
samtools stats $B > stats.txt
plot-bamstats -p stats_plots/ stats.txt > pb.log 2>&1; echo "rc=$?  dir exists: $([ -d stats_plots ] && echo yes || echo no); files: $(ls stats_plots 2>/dev/null | wc -l)"; grep -iE 'error|No such|cannot' pb.log | head -2 | cut -c1-150
