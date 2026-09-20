#!/bin/bash
RUN=/mnt/openscience/audits/bio-alignment-validation/run
W=$RUN/out/work3; mkdir -p $W; cd $W
B=$RUN/data/idx/real_human_PE.bam
cp $RUN/snip/usage-guide_06_bash.txt ug6.sh
sed -i "s#input.bam#$B#" ug6.sh
bash ug6.sh > ug6.log 2>&1; echo "rc=$? (verbatim usage-guide 'Comprehensive Stats', no mkdir of stats_plots/)"; head -3 ug6.log | cut -c1-160
mkdir -p stats_plots; bash ug6.sh > ug6b.log 2>&1; echo "rc(after mkdir)=$?"; ls stats_plots | head -4; ls stats_plots | wc -l
