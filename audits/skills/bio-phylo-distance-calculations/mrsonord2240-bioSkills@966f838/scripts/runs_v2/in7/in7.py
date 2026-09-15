# Input 7 (Adversarial): UPGMA on strongly non-clocklike SYNTHETIC noclock8.fa, as the user asked, plus NJ.
import sys
sys.path.insert(0, '..')
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from phylo_util import rf_to_true

TRUE = '../../data/noclock8_true.nwk'
aln = AlignIO.read('../../data/noclock8.fa', 'fasta')
calc = DistanceCalculator('identity')
dm = calc.get_distance(aln)
up = DistanceTreeConstructor().upgma(dm)
nj = DistanceTreeConstructor().nj(dm)
for lab, t in (('UPGMA (requested)', up), ('NJ', nj)):
    print('%s RF %d/%d' % (lab, *rf_to_true(t, TRUE)))
    Phylo.draw_ascii(t)
print('true tree:'); Phylo.draw_ascii(Phylo.read(TRUE, 'newick'))
Phylo.write(up, 'upgma_identity.nwk', 'newick'); Phylo.write(nj, 'nj_identity.nwk', 'newick')
