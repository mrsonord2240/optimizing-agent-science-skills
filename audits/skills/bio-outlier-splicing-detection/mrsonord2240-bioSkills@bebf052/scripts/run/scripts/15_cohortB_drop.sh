#!/bin/bash
# NEW input: SKILL.md FRASER block verbatim on cohort B (seed 777, 40 samples, other genes/samples/strengths), FRASER 2.6.1
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run
cd $R; export PYTHONDONTWRITEBYTECODE=1
micromamba run -n as-drop Rscript scripts/10_block_fraser.R $R/in4_drop $R/blocks/01_r.R $R/data/synthB cohortB_2.6.1 S03 S40 > logs/15_cohortB_2.6.1.log 2>&1
grep -n "block finished\|cohortB\|DETECTED\|not detected\|non-planted\|Error\|expression-only\|tissue" logs/15_cohortB_2.6.1.log | cut -c1-200
