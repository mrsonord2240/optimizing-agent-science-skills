#!/bin/bash
# Re-audit of bio-phylo-divergence-dating at mrsonord2240/bioSkills@966f838. PAML 4.10.10, IQ-TREE 2.4.0 (LSD2), Biopython.
set -u
source /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/env.sh
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
DD=/f/OpenScience/audits/bio-phylo-divergence-dating; R=$DD/runs_v2; OLD=$DD/runs
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/divergence-dating
mkdir -p $R/common && cp $OLD/common/mct.py $OLD/common/tipdate.py $R/common/
cd $R
echo "######## IN1 canonical MCMCTree prior -> bv -> post (Skill control lines: BDparas m, usedata = 2 in.BV, header)"
mkdir -p in1 && cp $OLD/in1/run_in1.py in1/ && $PY in1/run_in1.py
echo "######## IN2 virus temporal signal + LSD2 (regression)"; $PY common/tipdate.py virus in2 20 | tail -6
echo "######## IN3 no-signal (regression)"; $PY common/tipdate.py nosig in3 20 | tail -3; (cd in3 && cp $OLD/in3/verdict.py . && $PY verdict.py)
echo "######## IN4 Skill's fixed MCC snippet, verbatim, on the pre-fix BEAST MCC trees"
mkdir -p in4 && cp $OLD/in4/prioronly.mcc.tree $OLD/in4/withdata.mcc.tree in4/ && (cd in4 && $PY ../in4_snippet.py; echo "exit $?")
echo "-- reference (pre-fix compare.py output)"; grep -E "^(AB|GH|ABCDEFGH) " $OLD/in4/compare_out.txt
echo "######## IN5 shipped helper, pipeline mode, 1 locus"; $PY example_runs.py in5
echo "-- claims: >/< vs B/L/U on 4.10.10"; $PY claims_and_isp.py claims
echo "######## IN7 adversarial point vs soft minimum (regression)"; mkdir -p in7 && cp $OLD/in7/run_in7.py in7/ && $PY in7/run_in7.py | tail -9
echo "######## IN8 NEW helper with a 2-locus alignment (ndata = 2)"; $PY example_runs.py in8
echo "######## IN9 NEW infinite-sites plot"; $PY claims_and_isp.py isp
echo "######## EXAMPLE demo mode + py_compile"
$PY -m py_compile $SK/examples/mcmctree_setup.py && echo "py_compile OK"; $PY $SK/examples/mcmctree_setup.py; echo "demo exit $?"
echo ALL DONE
