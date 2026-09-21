#!/bin/bash
# runs the three example variants written by 10_example_run.py, each in its own out/ex dir so PDFs/HTML land there
cd /f/OpenScience/audits/bio-data-visualization-lollipop-protein-maps/run/out/ex || exit 1
for v in V1_verbatim V2_no_proteinID V3_clean_no_proteinID; do
  mkdir -p $v; cp $v.R $v/; (cd $v && /f/OpenScience/audit-envs/data-visualization/r.sh $v.R > ../$v.log 2>&1)
  echo "===== $v"; grep -n "rror\|Warning\|WARNING\|halted" $v.log | head -8; ls $v
done
