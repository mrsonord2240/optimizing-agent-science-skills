# Input 1 (Canonical) - Python part. Data: SYNTHETIC barcode20.fa (AliSim, known tree).
import sys
sys.path.insert(0, '..')
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor, DistanceMatrix
from phylo_util import rf_to_true, k2p

TRUE = '../../data/barcode20_true.nwk'
aln = AlignIO.read('../../data/barcode20.fa', 'fasta')

# Skill pattern, verbatim: identity-only p-distance
calc = DistanceCalculator('identity')
dm = calc.get_distance(aln)
tree_p = DistanceTreeConstructor().nj(dm)
print('Bio.Phylo identity (p-distance) NJ  RF to true = %d / %d' % rf_to_true(tree_p, TRUE))

# Skill's routing: Bio.Phylo has no K2P, so compute the corrected matrix yourself and pass it in
names = [r.id for r in aln]
lower = [[k2p(aln[i].seq, aln[j].seq) for j in range(i)] + [0.0] for i in range(len(aln))]
dm_k2p = DistanceMatrix(names, lower)
tree_k = DistanceTreeConstructor().nj(dm_k2p)
Phylo.write(tree_k, 'k2p_nj_python.nwk', 'newick')
print('K2P matrix passed into Bio.Phylo NJ  RF to true = %d / %d' % rf_to_true(tree_k, TRUE))
print('max p = %.4f  max K2P = %.4f' % (max(max(r) for r in dm.matrix), max(max(r) for r in lower)))
