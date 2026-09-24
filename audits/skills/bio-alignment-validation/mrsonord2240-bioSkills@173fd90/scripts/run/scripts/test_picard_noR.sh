#!/bin/bash
# The Skill's Picard chart commands (H=, CHART=) with no Rscript on PATH: exit status, files, message. Judge by files, not rc.
RUN=/mnt/openscience/audits/bio-alignment-validation/run; PD=/mnt/openscience/audit-envs/alignment-files/public-data
W=$RUN/out/work_nor; rm -rf $W; mkdir -p $W; cd $W
H=$PD/human/test.paired_end.sorted.bam; REF=$PD/human/genome.fasta
NOR=$(echo "$PATH" | tr ':' '\n' | while read p; do [ -x "$p/Rscript" ] || echo "$p"; done | paste -sd:)
echo "Rscript on stripped PATH: '$(env PATH="$NOR" which Rscript 2>&1 | head -1)'"
for i in 1 2; do
  rm -f im.txt ih.pdf; env PATH="$NOR" picard CollectInsertSizeMetrics I=$H O=im.txt H=ih.pdf > i$i.log 2>&1; rc=$?
  echo "InsertSize run$i (as in SKILL.md, H=): rc=$rc metrics=$([ -s im.txt ] && echo yes || echo NO) pdf=$([ -s ih.pdf ] && echo yes || echo NO) msg: $(grep -a -E 'R is not installed|Rscript|R script' i$i.log | head -2 | cut -c1-140 | tr '\n' '|')"
done
rm -f gm.txt gs.txt gc.pdf; env PATH="$NOR" picard CollectGcBiasMetrics I=$H O=gm.txt CHART=gc.pdf S=gs.txt R=$REF > g.log 2>&1; rc=$?
echo "GcBias (as in SKILL.md, CHART=): rc=$rc metrics=$([ -s gm.txt ] && echo yes || echo NO) summary=$([ -s gs.txt ] && echo yes || echo NO) msg: $(grep -a -E 'R is not installed|Rscript|R script' g.log | head -2 | cut -c1-140 | tr '\n' '|')"
echo "--- same commands with R on PATH:"
rm -f im.txt ih.pdf; picard CollectInsertSizeMetrics I=$H O=im.txt H=ih.pdf > ok.log 2>&1; echo "InsertSize: rc=$? metrics=$([ -s im.txt ] && echo yes || echo NO) pdf=$([ -s ih.pdf ] && echo yes || echo NO)"
echo "--- workaround check: no-R with the chart option dropped (Picard needs H=): CollectInsertSizeMetrics O= only"
rm -f im2.txt; env PATH="$NOR" picard CollectInsertSizeMetrics I=$H O=im2.txt > w.log 2>&1; echo "rc=$? metrics=$([ -s im2.txt ] && echo yes || echo NO) msg: $(grep -a -E 'Exception|ERROR|required' w.log | head -2 | cut -c1-150 | tr '\n' '|')"
