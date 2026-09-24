#!/bin/bash
# Re-runs the whole audit of bio-data-visualization-distribution-plots (Git Bash). Run from this directory.
# Skill copy: run/skill/ was made with: git -C F:/OpenScience/external/mrsonord2240__bioSkills archive 64b3b150c9b989c102f7ee69e0bb07c16842d894 data-visualization/distribution-plots | tar -x -C run/skill
E=F:/OpenScience/audit-envs/data-visualization
mkdir -p data out
$E/r.sh v0_versions.R;   $E/r-gg35.sh v0_versions.R
$E/r.sh i1_data.R
TAG=gg4  $E/r.sh      i1_blocks.R > out/i1_gg4.log 2>&1
TAG=gg35 $E/r-gg35.sh i1_blocks.R > out/i1_gg35.log 2>&1
$E/r.sh i1b_ggdist.R
$E/py.sh i2_py.py > out/i2_py.log 2>&1;  $E/py.sh i2b_bw.py > out/i2b_bw.log 2>&1
$E/r.sh i3_edge.R > out/i3_gg4.log 2>&1; $E/r.sh i3b_bw.R > out/i3b.log 2>&1
$E/r.sh i4_real_split.R > out/i4.log 2>&1
TAG=gg4 $E/r.sh i4c_side.R;  TAG=gg35 $E/r-gg35.sh i4c_side.R
# input 5: run the ggplot2 4.0.3 pass first and keep its blank PDF, then the 3.5.2 pass (writes the real PDF)
$E/r.sh i5_example.R > out/i5_gg4.log 2>&1; cp out/i5/raincloud.pdf out/i5/raincloud_gg4_FAILED.pdf
$E/r-gg35.sh i5_example.R > out/i5_gg35.log 2>&1
$E/py.sh i5_pdf.py > out/i5_pdf.log 2>&1
$E/r-gg35.sh i5b_lv35.R; $E/r.sh i5b_lv35.R; $E/r-gg35.sh i5c_trim.R
$E/py.sh build_report.py
