# Input 5 (Stress) - Python half. Data: SYNTHETIC big150.fa (150 taxa, 1000 bp, known tree).
import sys
import time
sys.path.insert(0, '..')
import pandas as pd
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor, DistanceMatrix
from Bio.Phylo.Consensus import bootstrap_consensus, majority_consensus
from skbio import DistanceMatrix as SkDM
from skbio.tree import nj
from phylo_util import rf_to_true

TRUE = '../../data/big150_true.nwk'
B = int(sys.argv[1]) if len(sys.argv) > 1 else 100
aln = AlignIO.read('../../data/big150.fa', 'fasta')

t0 = time.time(); calc = DistanceCalculator('identity'); dm = calc.get_distance(aln); t_dm = time.time() - t0
t0 = time.time(); tree_p = DistanceTreeConstructor().nj(dm); t_nj = time.time() - t0
print('Bio.Phylo identity matrix %.1fs, NJ %.1fs, RF %d/%d' % (t_dm, t_nj, *rf_to_true(tree_p, TRUE)))

k = pd.read_csv('k80_big150.csv', index_col=0)
ids = list(k.index)
t0 = time.time(); sk = nj(SkDM(k.values, ids), neg_as_zero=True); t_sk = time.time() - t0
nwk = str(sk)
print('skbio nj(K80 from ape, neg_as_zero=True) %.2fs RF %d/%d' % (t_sk, *rf_to_true(nwk, TRUE)))
neg = nj(SkDM(k.values, ids), neg_as_zero=False)
print('skbio neg_as_zero=False negative branches:', sum(1 for n in neg.traverse() if n.length is not None and n.length < 0))
lower = [[float(k.values[i, j]) for j in range(i)] + [0.0] for i in range(len(ids))]
t0 = time.time(); tree_k = DistanceTreeConstructor().nj(DistanceMatrix(ids, lower)); t_bk = time.time() - t0
print('Bio.Phylo nj(K80 matrix from ape) %.1fs RF %d/%d' % (t_bk, *rf_to_true(tree_k, TRUE)))

# Skill's Python bootstrap line, as written (identity distance)
t0 = time.time()
cons = bootstrap_consensus(aln, B, DistanceTreeConstructor(calc, 'nj'), majority_consensus)
t_bs = time.time() - t0
Phylo.write(cons, 'bp_consensus_B%d.nwk' % B, 'newick')
conf = [c.confidence for c in cons.get_nonterminals() if c.confidence is not None]
print('bootstrap_consensus B=%d: %.0fs; internal nodes %d, with confidence %d; RF %d/%d' %
      (B, t_bs, len(cons.get_nonterminals()), len(conf), *rf_to_true(cons, TRUE)))
if conf:
    print('confidence range %.1f-%.1f' % (min(conf), max(conf)))
