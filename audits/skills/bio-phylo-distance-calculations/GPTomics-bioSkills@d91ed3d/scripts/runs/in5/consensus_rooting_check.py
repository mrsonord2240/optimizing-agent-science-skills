# Input 5 follow-up: does Bio.Phylo majority_consensus split support between a split and its complement
# because each NJ replicate is rooted arbitrarily? Same replicates, consensus with vs without a common outgroup root.
# Data: SYNTHETIC barcode20.fa and big150.fa.
import random
import sys
sys.path.insert(0, '..')
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Phylo.Consensus import bootstrap_trees, majority_consensus
from phylo_util import rf_to_true

for name, B in (('barcode20', 100), ('big150', 20)):
    random.seed(20260915)
    aln = AlignIO.read(f'../../data/{name}.fa', 'fasta')
    trees = list(bootstrap_trees(aln, B, DistanceTreeConstructor(DistanceCalculator('identity'), 'nj')))
    raw = majority_consensus(trees)
    out = aln[0].id
    for t in trees:
        t.root_with_outgroup(out)
    rooted = majority_consensus(trees)
    for lab, c in (('as Skill (unrooted NJ replicates)', raw), (f'replicates rooted on {out}', rooted)):
        conf = [x.confidence for x in c.get_nonterminals() if x.confidence is not None]
        print('%s B=%d %-36s RF %d/%d  confidence max %.0f  clades>=70%%: %d' %
              (name, B, lab, *rf_to_true(c, f'../../data/{name}_true.nwk'), max(conf), sum(v >= 70 for v in conf)))
