#!/bin/bash
# Re-audit of bio-phylo-tree-manipulation at mrsonord2240/bioSkills@966f838. SYNTHETIC data (data/make_data.py).
set -u
source /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/env.sh
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
TM=/f/OpenScience/audits/bio-phylo-tree-manipulation; R=$TM/runs_v2; OLD=$TM/runs; D=$TM/data
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/tree-manipulation
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
MAD=$(find $T/mad $T/MADroot-master -name mad.py 2>/dev/null | head -1); FR=$(find $T/MinVar-Rooting-master -name FastRoot.py | head -1)
echo "mad.py: $MAD | FastRoot: $FR"
cp $OLD/rootsplit.py $R/
echo "######## IN1"; (cd $R/in1 && $PY in1.py; echo "exit $?")
echo "######## IN2 (regression)"; mkdir -p $R/in2 && cp $OLD/in2/in2_prune.py $R/in2/ && (cd $R/in2 && $PY in2_prune.py | grep -v "^ " | head -12)
echo "######## IN3"; cp $OLD/in3/edge16.treefile $R/in3/ && (cd $R/in3 && $PY in3.py; echo "exit $?")
echo "######## IN4 MAD + MinVar as written"
mkdir -p $R/in4 && cd $R/in4 && cp $OLD/in4/deep20.nwk $OLD/in4/in4_score.py .
$PY $MAD deep20.nwk > mad.out 2>&1; echo "mad exit $?"; grep -E "MAD|AI|CCV" mad.out | head -3
$PY $FR -i deep20.nwk -m MV -o rooted.nwk > fr.out 2>&1; echo "FastRoot exit $?"; tail -1 fr.out
$PY in4_score.py
echo "######## IN5 non-reversible root test (Skill command; iqtree2 on 2.x)"
mkdir -p $R/in5/nr && cd $R/in5/nr && cp $D/deep20_aln.fa aln.fa
t0=$(date +%s); iqtree2 -s aln.fa --model-joint 12.12 -B 1000 --root-test -zb 1000 -au -T 4 --seed 12345 --prefix rootnr > rootnr.stdout 2>&1; echo "iqtree exit $? ($(( $(date +%s) - t0 ))s)"
ls rootnr.* | head -20; head -8 rootnr.roottest.csv 2>/dev/null
cp $OLD/in5/roottest_map.py . && $PY roottest_map.py 2>&1 | head -12
grep -o "X1[^;]*" rootnr.rootstrap.nex 2>/dev/null | head -1 | cut -c1-200
cd $R/in5 && cp $OLD/in5/in5_pipeline.R . && pwsh -NoProfile -File /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/rrun.ps1 -Script $R/in5/in5_pipeline.R -WorkDir $R/in5 > in5_R.out 2>&1; echo "R exit $?"; tail -8 in5_R.out
echo "######## IN7 far outgroup (regression)"; mkdir -p $R/in7 && cd $R/in7 && cp $OLD/in7/in7_faroutgroup.py . && $PY in7_faroutgroup.py 2>&1 | tail -12
echo "######## IN8 NEW non-monophyletic outgroup"; cd $R && $PY in89.py in8 $MAD
echo "######## IN9 NEW MAD strip regex"; cd $R && $PY in89.py in9 $MAD
echo "######## EXAMPLES"
mkdir -p $R/examples && cd $R/examples
for s in collapse_support common_ancestor prune_taxa root_tree; do $PY -m py_compile $SK/examples/$s.py && echo "$s py_compile OK"; $PY $SK/examples/$s.py > $s.out 2>&1; echo "$s exit $?"; tail -4 $s.out; done
echo ALL DONE
