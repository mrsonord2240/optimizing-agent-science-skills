#!/bin/bash
# A5b: overlap of HINT / Wellington footprints with TOBIAS (A1 run) bound vs unbound CTCF/all-motif sites inside the 60 peaks.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
H=$W/a5; B=$W/a1/out/bindetect; cd $H
cat $B/*/beds/*_cond1_bound.bed   | cut -f1-3 | sort -u | bedtools intersect -u -a - -b pk60.bed > bound.bed
cat $B/*/beds/*_cond1_unbound.bed | cut -f1-3 | sort -u | bedtools intersect -u -a - -b pk60.bed > unbound.bed
cut -f1-3 hint_out/t.bed > hint.bed; cut -f1-3 wl_default/*FDR*.bed > wl.bed; cut -f1-3 wl_A/*FDR*.bed > wlA.bed
for t in hint wl wlA; do for s in bound unbound; do
  n=$(wc -l < $s.bed); o=$(bedtools intersect -u -a $s.bed -b $t.bed | wc -l)
  awk -v t=$t -v s=$s -v n=$n -v o=$o 'BEGIN{printf "%s footprints x TOBIAS %s sites: %d/%d = %.3f\n",t,s,o,n,(n?o/n:0)}'; done
  # reverse direction: fraction of the tool's own footprints that contain/overlap a TOBIAS-bound site
  nt=$(wc -l < $t.bed); ot=$(bedtools intersect -u -a $t.bed -b bound.bed | wc -l)
  awk -v t=$t -v n=$nt -v o=$ot 'BEGIN{printf "%s: %d/%d = %.3f of its footprints overlap a TOBIAS-bound site\n",t,o,n,(n?o/n:0)}'
done
