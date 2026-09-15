# Input 1 (Canonical), Python half: the fixed Skill's Python block VERBATIM (path names only), SYNTHETIC barcode20.fa.
import sys
sys.path.insert(0, '..')
from phylo_util import rf_to_true
TRUE = '../../data/barcode20_true.nwk'

from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

aln = AlignIO.read('../../data/barcode20.fa', 'fasta')
calc = DistanceCalculator('identity')        # identity-only: this is a p-distance, NOT a JC/K80 correction
dm = calc.get_distance(aln)                   # multiple/back/parallel hits are NOT corrected here
tree = DistanceTreeConstructor().nj(dm)       # NJ algorithm is correct; the DISTANCES are the limitation

# Model-corrected matrix from R -- write.csv(as.matrix(dist.dna(aln, model = 'K80')), 'k80.csv') -- passed in:
import pandas as pd
from Bio.Phylo.TreeConstruction import DistanceMatrix
df = pd.read_csv('k80.csv', index_col=0)
names = list(df.index)
lower = [[float(df.iat[i, j]) for j in range(i + 1)] for i in range(len(names))]   # lower triangle incl. diagonal
tree_k80 = DistanceTreeConstructor().nj(DistanceMatrix(names, lower))
# scikit-bio: skbio.tree.nj(skbio.DistanceMatrix(df.values, names))
import skbio
sk = skbio.tree.nj(skbio.DistanceMatrix(df.values, names))

print('identity NJ RF %d/%d' % rf_to_true(tree, TRUE))
print('K80 hand-off Bio.Phylo NJ RF %d/%d' % rf_to_true(tree_k80, TRUE))
print('K80 hand-off skbio NJ RF %d/%d' % rf_to_true(str(sk), TRUE))
print('names match alignment ids:', sorted(names) == sorted(r.id.strip() for r in aln), '| first names', names[:3])
