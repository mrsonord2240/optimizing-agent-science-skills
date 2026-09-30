#!/bin/bash
# A2: minimal patched COPY of run_abc.sh (adds --accessibility_feature DHS --hic_gamma/--hic_scale from ABC config avg-hic values). Skill bytes untouched.
source /mnt/openscience/audits/bio-atac-seq-enhancer-gene-linking/initial-audit-20260930/scripts/common.sh
mkdir -p $RUN/outputs; python - <<'P'
import os
s=open(os.environ['SKILL']+'/scripts/run_abc.sh',encoding='utf-8',newline='').read()
BS=chr(92); key='--hic_type avg '+BS+chr(10); assert s.count(key)==1
open(os.environ['RUN']+'/outputs/run_abc_patched.sh','w',encoding='utf-8',newline='').write(s.replace(key,key+'    --accessibility_feature DHS --hic_gamma 1.024238616787792 --hic_scale 5.9594510043736655 '+BS+chr(10)))
P
diff <(cat $SKILL/scripts/run_abc.sh) $RUN/outputs/run_abc_patched.sh
stage_inputs $RUN/outputs/a2_patched; date -Is
bash $RUN/outputs/run_abc_patched.sh atac.bam h3k27ac.bam $EG/work/avg dummy.fa chr22.sizes $E/RefSeqCurated.170308.bed.CollapsedGeneBounds.chr22.hg38.bed $R K562 abc_out
echo "patched run_abc.sh rc=$?"
