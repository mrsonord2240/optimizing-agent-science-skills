# Input 2a: SKILL.md blocks 02 (defines groups/TSV/palette) + 03 (batch) run literally in sequence, planted 3v3 and real chrX (contig X, rMATS says chrX)
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
PUB=$AS/public-data
for SET in planted real; do
  W=$RUN/out/i2a_$SET; rm -rf $W; mkdir -p $W; cd $W
  for FMT in pdf svg; do
    mkdir -p $FMT; cd $FMT
    if [ $SET = planted ]; then
      cp $PUB/planted/*.bam $PUB/planted/*.bai $PUB/planted/planted.gtf .
      sed -e "s/ctrl1.bam/G1_rep1.bam/;s/ctrl2.bam/G1_rep2.bam/;s/ctrl3.bam/G1_rep3.bam/;s/trt1.bam/G2_rep1.bam/;s/trt2.bam/G2_rep2.bam/;s/trt3.bam/G2_rep3.bam/;s#chr17:43094000-43125000#chrP:1-1200#;s#BRCA1_sashimi#blk02#g;s#gencode_v45.gtf#planted.gtf#" $RUN/blocks/02_*.py > b02.py
      RM=$RUN/data/rmats_planted/SE.MATS.JC.txt; GTF=planted.gtf
    else
      # block 02 hard-codes 6 samples; real chrX has 4 BAMs, so the DataFrame is replaced by the 4-sample equivalent (same columns, same TSV/palette writes)
      cat > b02.py <<PY
import subprocess
import pandas as pd
from pathlib import Path
groups = pd.DataFrame({
    'sample_id': ['gbr1', 'gbr2', 'yri1', 'yri2'],
    'bam': ['$PUB/rnasplice/bam/ERR188383.Aligned.out.bam', '$PUB/rnasplice/bam/ERR188428.Aligned.out.bam', '$PUB/rnasplice/bam/ERR188454.Aligned.out.bam', '$PUB/rnasplice/bam/ERR204916.Aligned.out.bam'],
    'group': ['GBR', 'GBR', 'YRI', 'YRI']})
groups.to_csv('sashimi_groups.tsv', sep='\t', index=False, header=False)
Path('palette.txt').write_text('#1f77b4\n#ff7f0e\n')
PY
      RM=$RUN/data/rmats_real/SE.MATS.JC.txt; GTF=$PUB/rnasplice/reference/genes_chrX.gtf
    fi
    [ $SET = planted ] && micromamba run -n as-core python b02.py > b02.log 2>&1 || micromamba run -n as-core python b02.py > b02.log 2>&1
    sed -e "s#rmats_output/SE.MATS.JC.txt#$RM#;s#annotation.gtf#$GTF#;s#pdf#$FMT#g;s#sashimi_plots#plots#g" $RUN/blocks/03_*.py > b03.py
    # groups comes from block 02's namespace in the real Skill flow: prepend block 02 (the real chrX one) so `groups` exists
    cat b02.py b03.py > b0203.py
    micromamba run -n as-core python b0203.py > b03.log 2>&1; echo "[$SET $FMT] rc=$?"; grep -aE "Traceback|Error|assert" b03.log | head -3
    ls -l plots 2>/dev/null | awk 'NR>1{print $5, $9}'
    cd ..
  done
done
