#!/bin/bash
# Delta re-audit static checks for DLA-016 and the env-table row (read-only).
S=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac
echo "--- numbered workflow steps in SKILL.md:"; grep -nE '^[0-9]+\. |^#+ .*[Ss]tep' "$S/SKILL.md"
echo "--- script header step pointer:"; sed -n 4p "$S/scripts/chrombpnet_pipeline.sh"
echo "--- other 'step N' pointers in the Skill tree:"; grep -rnoE 'SKILL\.md step [0-9]+' "$S"
echo "--- conda packages providing the tools in dlatac-tf (conda-meta):"
ls /home/sci/micromamba/envs/dlatac-tf/conda-meta | grep -iE '^(bedtools|ucsc-bedgraphtobigwig)-'
echo "--- versions:"; /home/sci/micromamba/envs/dlatac-tf/bin/bedtools --version
/home/sci/micromamba/envs/dlatac-tf/bin/bedGraphToBigWig 2>&1 | head -2
echo "--- chromBPNet call sites that need them:"
P=$(ls -d /home/sci/micromamba/envs/dlatac-tf/lib/python3.8/site-packages/chrombpnet)
grep -rnE 'bedtools|bedGraphToBigWig' "$P" --include=*.py | cut -c1-200 | head
