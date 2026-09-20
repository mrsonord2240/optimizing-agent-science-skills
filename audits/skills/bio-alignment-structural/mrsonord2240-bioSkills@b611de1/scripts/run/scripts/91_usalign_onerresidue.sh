#!/bin/bash
# SKILL.md claim: "US-align can segfault on a one-residue input". Run inside WSL (cwd = run/), env alignment.
cd "$(dirname "$0")/.." || exit 1
for args in "" "-outfmt 2" "-mol prot -outfmt 2" "-mm 1 -ter 0"; do
  USalign data/synthetic/one_residue.pdb data/real_pdb/1MBN.pdb $args > /tmp/us_one.txt 2>&1; echo "one_residue as structure_1, args=[$args] rc=$?  output lines=$(wc -l < /tmp/us_one.txt)"
  USalign data/real_pdb/1MBN.pdb data/synthetic/one_residue.pdb $args > /tmp/us_one.txt 2>&1; echo "one_residue as structure_2, args=[$args] rc=$?  output lines=$(wc -l < /tmp/us_one.txt)"
done
echo "--- foldseek databases names containing 'multimer' (SKILL/usage-guide mention AFDB-Multimer / PDB100-Multimer):"
foldseek databases 2>&1 | grep -i -c multimer
echo "--- names containing PDB100:"
foldseek databases 2>&1 | grep -i -c pdb100
