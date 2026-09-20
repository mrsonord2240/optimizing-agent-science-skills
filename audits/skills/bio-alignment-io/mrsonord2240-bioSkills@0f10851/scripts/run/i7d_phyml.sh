#!/bin/bash
# PhyML 100-char-name claim on two builds; saves each tree under its own name
D=/mnt/openscience/audits/bio-alignment-io/run/data/tools; cd $D
for tag in new old; do
  E=aln-treetools; [ $tag = old ] && E=aln-phyml-old
  rm -f pf12_longnames.phy_phyml_tree.txt
  timeout 240 micromamba run -n $E phyml -i pf12_longnames.phy -d aa -m LG -o n -b 0 --quiet </dev/null > ph_${tag}.out 2>&1
  micromamba run -n $E phyml --version </dev/null 2>&1 | grep -a "PhyML version"
  cp pf12_longnames.phy_phyml_tree.txt phyml_${tag}_tree.txt
done
