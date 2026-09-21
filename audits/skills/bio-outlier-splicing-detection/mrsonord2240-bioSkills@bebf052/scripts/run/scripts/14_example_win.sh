#!/bin/bash
# shipped example from a clean copy, FRASER 2.2.0 (Windows R via r.sh); optimHyperParams path
cd /f/OpenScience/audits/bio-outlier-splicing-detection/run/ex_win; rm -rf fraser_workdir
bash /f/OpenScience/audit-envs/alternative-splicing/r.sh fraser2_rare_disease.R bams PATIENT_001 fraser_workdir > ../logs/14_example_2.2.0.log 2>&1
echo "rc=$?"; grep -n "junctions kept\|^q = \|aberrant junctions\|Error" ../logs/14_example_2.2.0.log | cut -c1-200
