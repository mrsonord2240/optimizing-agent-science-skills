#!/bin/bash
# INPUT 7 part 3: RAxML-NG '*' on a 5-taxon DNA alignment (previous DNA probe had 3 taxa and was rejected for count); old PhyML tree name lengths
D=/mnt/openscience/audits/bio-alignment-io/run/data/tools; cd $D
printf ' 5 12\nA1  ACGTACGTACGT\nA2  ACGTACGTACGA\nA3  ACGTTCGTACGT\nA4  ACGAACGTTCGT\nA5  ACG*ACGTACGT\n' > dna_star.phy
for v in 1 2; do R="micromamba run -n aln-raxml1"; [ $v = 2 ] && R="micromamba run -n aln-treetools"
  $R raxml-ng --check --msa dna_star.phy --model GTR+G --prefix rxd$v </dev/null > rxd$v.out 2>&1; echo "v$v DNA star exit=$?"; grep -aE "ERROR|exception|successfully|nvalid" rxd$v.out | head -3
done
python3 -c "
import re
tr=open('pf12_longnames.phy_phyml_tree.txt').read()
names=re.findall(r'[(,]([^(),:]+):',tr); print('old-phyml (3.3.20220408) tree taxon-name lengths:', sorted(set(len(n) for n in names)), 'n=', len(names))
"
