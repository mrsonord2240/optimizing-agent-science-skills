#!/usr/bin/env bash
set -euo pipefail

env=/home/sci/micromamba/envs/phylo-phase2
root=/mnt/openscience/wt/phylogenetics-tree-visualization/phylogenetics/tree-visualization/examples
out=/mnt/openscience/audits/bio-phylo-tree-visualization/run/python_examples.out
"$env/bin/python" "$root/ascii_tree.py" >"$out" 2>&1
"$env/bin/python" "$root/basic_tree_plot.py" >>"$out" 2>&1
"$env/bin/python" "$root/labeled_tree.py" >>"$out" 2>&1
printf 'exit=0\n' >>"$out"
