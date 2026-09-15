# Input 1 (Canonical) -- SYNTHETIC 15-taxon single protein gene (AliSim + MAFFT L-INS-i), commands as the Skill directs.
# Skill: single-gene tree input -> ClipKIT smart-gap; --log for reproducibility; aggressiveness cap; trimmed vs untrimmed trees.
set -u
export PATH=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts:$PATH
cd "$(dirname "$0")"
cp ../../data/prot15_linsi.fasta input.fasta
clipkit --version
clipkit input.fasta -m smart-gap --log -o trimmed.fasta; echo "clipkit exit $?"
ls trimmed.fasta* input.fasta* 2>/dev/null
iqtree2 -s input.fasta   -m MFP -B 1000 -T 4 --seed 1 --prefix untrimmed -redo -quiet; echo "iqtree untrimmed exit $?"
iqtree2 -s trimmed.fasta -m MFP -B 1000 -T 4 --seed 1 --prefix smartgap  -redo -quiet; echo "iqtree trimmed exit $?"
