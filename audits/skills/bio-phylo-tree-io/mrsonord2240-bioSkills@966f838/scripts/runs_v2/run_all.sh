#!/bin/bash
# Re-audit of bio-phylo-tree-io at mrsonord2240/bioSkills@966f838. SYNTHETIC data (data/make_data.py).
set -u
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
export PYTHONIOENCODING=utf-8
TI=/f/OpenScience/audits/bio-phylo-tree-io; R=$TI/runs_v2; OLD=$TI/runs
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/tree-io
rr() { pwsh -NoProfile -File /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/rrun.ps1 -Script "$1" -WorkDir "$2"; echo "Rscript $(basename $1) exit $?"; }
echo "######## IN1"; (cd $R/in1 && $PY in1.py; echo "exit $?")
mkdir -p $R/in1r && cp $OLD/in1/extract_mcc.R $R/in1r/ && rr $R/in1r/extract_mcc.R $R/in1r 2>&1 | grep -E "columns|identical|posterior|exit" | head -6
echo "######## IN2"; (cd $R/in2 && $PY in2.py | tail -9; echo "exit ${PIPESTATUS[0]}")
echo "######## IN3 (regression scripts; Skill now carries the encoding and quoted-name guidance)"
mkdir -p $R/in3 && cp $OLD/in3/odd_names.py $OLD/in3/odd_names.R $R/in3/ && (cd $R/in3 && $PY odd_names.py 2>&1 | grep -E "join|raised|round trip|tips:" | head -10)
rr $R/in3/odd_names.R $R/in3 2>&1 | tail -4
echo "######## IN4 (regression + Common Errors rows)"
mkdir -p $R/in4 && cp $OLD/in4/posterior_set.py $OLD/in4/empty.nwk $R/in4/ && (cd $R/in4 && $PY posterior_set.py 2>&1 | head -14)
echo "######## IN5 (regression)"; mkdir -p $R/in5 && cp $OLD/in5/format_matrix.py $R/in5/ && (cd $R/in5 && $PY format_matrix.py 2>&1 | grep -E "->|cdao|NeXML|tips" | head -12)
echo "######## IN6 (regression)"; mkdir -p $R/in6 && cp $OLD/in6/merge_runs.py $R/in6/ && (cd $R/in6 && $PY merge_runs.py 2>&1 | tail -6)
echo "######## IN7 (regression)"; mkdir -p $R/in7 && cp $OLD/in7/collab_labels.py $R/in7/ && (cd $R/in7 && $PY collab_labels.py 2>&1 | tail -6)
echo "######## IN8 NEW strict Newick readers"; rr $R/in8/in8.R $R/in8
echo "######## IN9 NEW encoding claim"; (cd $R/in9 && $PY in9.py; echo "exit $?")
echo "######## EXAMPLES"; mkdir -p $R/examples && cd $R/examples
for s in convert_formats parse_multiple_trees read_newick; do $PY -m py_compile $SK/examples/$s.py && echo "$s py_compile OK"; $PY $SK/examples/$s.py > $s.out 2>&1; echo "$s exit $?"; tail -3 $s.out; done
echo ALL DONE
