#!/bin/bash
# Re-audit of bio-phylo-distance-calculations at mrsonord2240/bioSkills@966f838. SYNTHETIC data (data/make_data.py).
set -u
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
export PYTHONIOENCODING=utf-8
DC=/f/OpenScience/audits/bio-phylo-distance-calculations; R=$DC/runs_v2; OLD=$DC/runs
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/distance-calculations
rr() { pwsh -NoProfile -File /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/rrun.ps1 -Script "$1" -WorkDir "$2"; echo "Rscript $(basename $1) exit $?"; }
cp $OLD/phylo_util.py $R/
echo "######## IN1"; rr $R/in1/in1.R $R/in1; (cd $R/in1 && $PY in1.py; echo "py exit $?")
echo "######## IN2"; rr $R/in2/in2.R $R/in2
echo "######## IN3"; rr $R/in3/in3.R $R/in3
echo "######## IN4"; rr $R/in4/in4.R $R/in4
echo "######## IN5"; (cd $R/in5 && $PY in5.py; echo "py exit $?")
echo "######## IN6 (regression, unchanged Skill lines)"; mkdir -p $R/in6 && cp $OLD/in6/in6.R $R/in6/ && rr $R/in6/in6.R $R/in6
echo "######## IN7 (regression, unchanged Skill lines)"; mkdir -p $R/in7 && cp $OLD/in7/in7.R $OLD/in7/in7.py $R/in7/ && rr $R/in7/in7.R $R/in7; (cd $R/in7 && $PY in7.py | grep RF)
echo "######## IN8 NEW gapped identity"; (cd $R/in8 && $PY in8.py; echo "py exit $?"); rr $R/in8/in8.R $R/in8
echo "######## IN9 NEW estimate alpha"; rr $R/in9/in9.R $R/in9
echo "######## EXAMPLES as shipped"
mkdir -p $R/examples && cd $R/examples
for s in build_nj_tree bootstrap_consensus pairwise_tree_distances; do $PY -m py_compile $SK/examples/$s.py && echo "$s py_compile OK"; $PY $SK/examples/$s.py > $s.out 2>&1; echo "$s exit $?"; done
tail -8 bootstrap_consensus.out
rr $SK/examples/model_corrected_tree.R $R/examples > model_corrected_tree.out 2>&1; tail -4 model_corrected_tree.out
echo ALL DONE
