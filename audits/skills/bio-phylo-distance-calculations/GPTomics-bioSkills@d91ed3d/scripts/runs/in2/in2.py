# Input 2 - the user's "quick Biopython NJ tree", reproduced with the Skill's Python pattern. SYNTHETIC deep12.fa.
import sys
sys.path.insert(0, '..')
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from phylo_util import rf_to_true

aln = AlignIO.read('../../data/deep12.fa', 'fasta')
calc = DistanceCalculator('identity')
tree = DistanceTreeConstructor().nj(calc.get_distance(aln))
print('Bio.Phylo identity NJ RF to true = %d / %d' % rf_to_true(tree, '../../data/deep12_true.nwk'))
