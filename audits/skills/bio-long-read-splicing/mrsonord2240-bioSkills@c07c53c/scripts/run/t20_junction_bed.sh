#!/bin/bash
# SKILL FLAIR failure-mode fix, the --junction_bed variant (6-column BED made with the SKILL's awk from a STAR SJ.out.tab): reads of the planted novel isoforms G057N/G058N kept by `flair correct`
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; cd $R/out/ex_hifi/out; export PYTHONDONTWRITEBYTECODE=1
awk 'BEGIN{OFS="\t"} $4>0 {print $1,$2-1,$3,"sj"NR,$7,($4==1?"+":"-")}' $D/SJ.out.tab > sr_junctions.bed
for V in "annotation only|" "junction_bed|--junction_bed sr_junctions.bed" "junction_tab|--junction_tab $D/SJ.out.tab"; do
  N=${V%%|*}; A=${V#*|}
  flair correct -q ctrl1.bed -f ../annotation.gtf $A -o jb_t -t 8 > jb.log 2>&1
  echo "$N: rc=$? corrected reads G057N: $(grep -c G057N jb_t_all_corrected.bed)/40  G058N: $(grep -c G058N jb_t_all_corrected.bed)/9  ; total corrected $(wc -l < jb_t_all_corrected.bed) inconsistent $(wc -l < jb_t_all_inconsistent.bed)"
done
