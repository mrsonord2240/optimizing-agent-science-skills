# Input 6 - Bio.Phylo score-matrix distance for contrast (SYNTHETIC prot15.fa).
import sys
sys.path.insert(0, '..')
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from phylo_util import rf_to_true

aln = AlignIO.read('../../data/prot15.fa', 'fasta')
for model in ('identity', 'blosum62'):
    t = DistanceTreeConstructor().nj(DistanceCalculator(model).get_distance(aln))
    print('Bio.Phylo %-8s NJ RF %d/%d' % (model, *rf_to_true(t, '../../data/prot15_true.nwk')))
