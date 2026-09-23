#!/bin/bash
# generate all SYNTHETIC data (regression: make_synth.py from pre-fix audit; new: make_depth.py, make_edge.py)
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work
python $R/make_synth.py > $R/out/make_synth.txt 2>&1; tail -5 $R/out/make_synth.txt
python $R/make_depth.py > $R/out/make_depth.txt 2>&1; head -c 600 $R/out/make_depth.txt
python $R/make_edge.py > $R/out/make_edge.txt 2>&1; tail -c 400 $R/out/make_edge.txt
ls $R/data $R/data/edge
