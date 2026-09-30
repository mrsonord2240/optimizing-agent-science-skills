#!/bin/bash
# A1b: independent assertions on the A1 outputs (tooling-authored checkers, reused; reads bindetect_results.txt and corrected bigwigs directly).
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
cd $W/a1
python $A/scripts/check_bindetect.py out/bindetect/bindetect_results.txt | tail -n 8
python $A/scripts/check_ctcf_profile.py out $A/out/a1_ctcf_profile.png
# what the script's summary step actually sorts on, vs its comment "ranked by absolute change"
echo "--- rank of the script's printed order vs |change| order (top 13 rows printed by the script)"
awk -F'\t' 'NR==1 {for(i=1;i<=NF;i++) col[$i]=i; next} {print $(col["output_prefix"]), $(col["cond1_cond2_change"]), $(col["cond1_cond2_pvalue"])}' out/bindetect/bindetect_results.txt | sort -k3,3g | head -20 | awk '{print NR, $1, $2}' > byp.txt
awk -F'\t' 'NR==1 {for(i=1;i<=NF;i++) col[$i]=i; next} {c=$(col["cond1_cond2_change"]); if(c<0)c=-c; print $(col["output_prefix"]), c}' out/bindetect/bindetect_results.txt | sort -k2,2gr | head -20 | awk '{print NR, $1, $2}' > byabs.txt
echo "by p-value (script):"; head -6 byp.txt; echo "by |change|:"; head -6 byabs.txt
