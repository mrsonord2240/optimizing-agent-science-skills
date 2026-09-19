#!/bin/bash
# Re-audit of bio-phylo-tree-visualization at mrsonord2240/bioSkills@966f838. SYNTHETIC data (data/make_data.py).
set -u
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
export PYTHONIOENCODING=utf-8
TV=/f/OpenScience/audits/bio-phylo-tree-visualization; R=$TV/runs_v2; OLD=$TV/runs
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/tree-visualization
rr() { pwsh -NoProfile -File /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/rrun.ps1 -Script "$1" -WorkDir "$2"; echo "Rscript $(basename $1) exit $?"; }
cd $R
for p in in1 in2 in3; do echo "######## ${p^^}"; $PY in123.py $p; echo "exit $?"; done
echo "-- in1 reroot shift (regression check_reroot.py)"; cp $OLD/in1/check_reroot.py in1/ && (cd in1 && $PY check_reroot.py | tail -2)
$PY $OLD/raster.py in1/supported_tree.svg in2/colored_tree.pdf 2>&1 | tail -2
echo "######## IN4 HPD bars (regression hpd_center.R)"; mkdir -p in4 && cp $OLD/in4/hpd_center.R in4/ && rr $R/in4/hpd_center.R $R/in4 2>&1 | grep -E "center =|max"
echo "######## IN5 Fig 2 (regression fig2.R)"; mkdir -p in5 && cp $OLD/in5/fig2.R in5/ && rr $R/in5/fig2.R $R/in5 2>&1 | tail -6
echo "######## IN6 unrooted (regression)"; mkdir -p in6 && cp $OLD/in6/unrooted.R $OLD/in6/unrooted_ape.R in6/ && rr $R/in6/unrooted.R $R/in6 2>&1 | tail -3; rr $R/in6/unrooted_ape.R $R/in6 2>&1 | tail -3
echo "######## IN7 PP honest (regression)"; mkdir -p in7 && cp $OLD/in7/honest_pp.R in7/ && rr $R/in7/honest_pp.R $R/in7 2>&1 | tail -6
echo "######## IN8 NEW version block"; rr $R/in8/in8.R $R/in8
echo "######## IN9 NEW ape edgelabel"; rr $R/in9/in9.R $R/in9
echo "######## EXAMPLES"; mkdir -p examples && cd examples
for s in ascii_tree basic_tree_plot labeled_tree; do $PY -m py_compile $SK/examples/$s.py && echo "$s py_compile OK"; $PY $SK/examples/$s.py > $s.out 2>&1; echo "$s exit $?"; tail -3 $s.out; done
echo ALL DONE
