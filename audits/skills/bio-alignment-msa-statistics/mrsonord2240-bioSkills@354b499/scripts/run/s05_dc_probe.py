"""Why does Bio.Phylo DistanceCalculator('identity') differ from Skill PID2? Probe on seed_norm."""
import sys, os, inspect
sys.path.insert(0, 'skill/examples'); sys.path.insert(0, '.')
import ref
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
aln = AlignIO.read('data/seed_norm.fasta', 'fasta')
dc = DistanceCalculator('identity'); D = dc.get_distance(aln)
rows = ref.norm_rows([str(r.seq) for r in aln])
worst = None
for a in range(len(aln)):
    for b in range(a):
        r = ref.pid_ref(rows[a], rows[b])
        diff = abs(r['PID2'] - (1 - D[a, b]))
        if worst is None or diff > worst[0]: worst = (diff, a, b, r, D[a, b])
print('worst', worst[:3], 'PID2(ref)=%.4f 1-D=%.4f' % (worst[3]['PID2'], 1 - worst[4]))
print(inspect.getsource(DistanceCalculator._pairwise))
