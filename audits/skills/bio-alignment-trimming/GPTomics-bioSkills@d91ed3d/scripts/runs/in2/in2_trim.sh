# Input 2 (Variant A) -- SYNTHETIC 12-taxon x 20-locus DNA supermatrix (AliSim + MAFFT L-INS-i), partition file supplied.
# Skill: concatenated supermatrix -> ClipKIT kpic-smart-gap (or BMGE -h 0.5); PHYLIP output; sensitivity check.
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
cd "$(dirname "$0")"
cp ../../data/dna_super/supermatrix.fasta supermatrix.fasta; cp ../../data/dna_super/supermatrix.nex supermatrix.nex
echo "== Skill command 1 (as written): kpic-smart-gap on the concatenated matrix"
clipkit supermatrix.fasta -m kpic-smart-gap -o super_kpic.fasta > c1.out 2>&1; echo "exit $?"; grep -E "Original length|kept|trimmed:" c1.out
echo "== Skill command 3 (as written): --output-format phylip"
clipkit supermatrix.fasta -m kpic-smart-gap --output-format phylip -o super_kpic.phy > c3.out 2>&1; echo "exit $?"; tail -4 c3.out
echo "== adapted: -of phylip"
clipkit supermatrix.fasta -m kpic-smart-gap -of phylip -o super_kpic.phy > c3b.out 2>&1; echo "exit $?"; head -1 super_kpic.phy
echo "== Skill BMGE DNA command (as written) with BMGE 1.12"
java -jar $T/BMGE112.jar -i supermatrix.fasta -t DNA -of super_bmge112.fasta -m DNAPAM100:2 -h 0.5 > b112.out 2>&1; echo "exit $?"; grep -a -E "before|after" b112.out | tr '\r' '\n' | grep -E "before|after" | tail -2
echo "== Skill BMGE DNA command (as written) with BMGE 2.0"
java -jar $T/BMGE200.jar -i supermatrix.fasta -t DNA -of super_bmge200.fasta -m DNAPAM100:2 -h 0.5 > b200.out 2>&1; echo "exit $?"; head -3 b200.out; ls super_bmge200.fasta 2>&1
echo "== BMGE 2.0 adapted to its own flags (-t NT -e 0.5 -g 0.2 to match 1.12 gap default)"
java -jar $T/BMGE200.jar -i supermatrix.fasta -t NT -of super_bmge200e.fasta -m DNAPAM100:2 -e 0.5 -g 0.2 > b200e.out 2>&1; echo "exit $?"; tail -3 b200e.out
echo "== Partition file vs trimmed concatenation: IQ-TREE with original charsets on kpic-trimmed matrix"
iqtree2 -s super_kpic.fasta -p supermatrix.nex -m GTR+G4 -T 4 --seed 1 --prefix naive_part -redo -quiet > naive_part.out 2>&1; echo "exit $?"; grep -i -E "error|too large" naive_part.out naive_part.log 2>/dev/null | head -3
echo "== adapted: per-locus kpic-smart-gap, re-concatenate, rebuild charsets"
PYTHONIOENCODING=utf-8 python in2_perlocus.py
echo "== trees (edge-linked partitions, ModelFinder per partition)"
iqtree2 -s supermatrix.fasta        -p supermatrix.nex          -m MFP -B 1000 -T 4 --seed 1 --prefix untrimmed -redo -quiet; echo "untrimmed exit $?"
iqtree2 -s super_perlocus_kpic.fasta -p super_perlocus_kpic.nex -m MFP -B 1000 -T 4 --seed 1 --prefix kpic      -redo -quiet; echo "kpic exit $?"
iqtree2 -s super_bmge112.fasta      -m MFP -B 1000 -T 4 --seed 1 --prefix bmge -redo -quiet; echo "bmge (unpartitioned; BMGE drops locus boundaries) exit $?"
python ../tree_check.py ../../data/dna12_true.nwk untrimmed.treefile kpic.treefile bmge.treefile
