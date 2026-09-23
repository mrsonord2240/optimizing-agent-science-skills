"""Input 4 (Variant B): homology significance. Uses the Skill's own examples/empirical_pvalue.py (copy) on REAL pairs:
related (HBA vs HBB), distant (MYG_HUMAN vs HBB), unrelated (PKA kinase 1ATP vs HBB). Ground truth: BLASTP raw/bit score (Karlin-Altschul
lambda=0.267 K=0.041 for BLOSUM62 11/1), seed determinism, Gumbel fit of the shuffled null."""
import math, sys, numpy as np
from common import *
import empirical_pvalue_copy as ep
from scipy import stats
B62 = substitution_matrices.load('BLOSUM62')
STR = r'F:\OpenScience\audit-envs\alignment\public-data\structures'
kin = next(r for r in SeqIO.parse(STR + r'\1ATP.pdb', 'pdb-seqres'))
print("1ATP chain:", kin.id, len(kin.seq))
pairs = {'HBA vs HBB (related)': (prot('P69905').seq, prot('P68871').seq),
         'MYG_HUMAN vs HBB (distant)': (prot('P02144').seq, prot('P68871').seq),
         'PKA(1ATP) vs HBB (unrelated)': (kin.seq, prot('P68871').seq)}
loc = PairwiseAligner(mode='local', substitution_matrix=B62, open_gap_score=-12, extend_gap_score=-1)   # BLAST-equivalent (see input1b)
loc11 = PairwiseAligner(mode='local', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1)  # skill's own protein config
glo = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1)
out = {}
for name, (s1, s2) in pairs.items():
    a = glo.align(s1, s2)[0]; c = a.counts(); pid2 = 100 * c.identities / (c.identities + c.mismatches)
    obs, p, null = ep.empirical_pvalue(str(s1), str(s2), loc11, n_shuffles=1000, seed=42)
    obs2, p2, null2 = ep.empirical_pvalue(str(s1), str(s2), loc11, n_shuffles=1000, seed=42)
    bits = (0.267 * obs - math.log(0.041)) / math.log(2)
    print(f"{name}: global pid2={pid2:.1f}%  local raw={obs}  bits(K-A)={bits:.1f}  empirical p={p:.4f}  null mean={np.mean(null):.1f} max={max(null)}")
    check(f"  seed=42 deterministic (p and null identical on rerun)", p == p2 and null == null2)
    out[name] = (obs, p, null, bits)
o, p, null, bits = out['HBA vs HBB (related)']
check("related pair: empirical p at floor 1/1001", abs(p - 1/1001) < 1e-9, p)
check("HBA/HBB Karlin-Altschul bit score ~114 (BLASTP reported 114 for raw 285)", abs((0.267*285 - math.log(0.041))/math.log(2) - 114.4) < 0.5)
o, p, null, bits = out['PKA(1ATP) vs HBB (unrelated)']
check("unrelated pair: empirical p > 0.01 (not significant)", p > 0.01, p)
# Gumbel fit of the null -> lambda vs NCBI 0.267 (gapped 11/1)
nn = np.array(out['HBA vs HBB (related)'][2], float)
loc_, scale = stats.gumbel_r.fit(nn); lam = 1/scale
print(f"Gumbel fit of shuffled null (HBA vs shuffled HBB-side): lambda={lam:.3f} (NCBI gapped BLOSUM62 11/1: 0.267)")
check("empirical null lambda within 25% of NCBI 0.267", abs(lam - 0.267)/0.267 < 0.25, lam)
# the skill's default example
obs, pv, _ = ep.empirical_pvalue('MKTIIALSYIFCLVFA', 'MKAIIVCSCLLVFFA', PairwiseAligner(mode='local', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1), n_shuffles=1000)
print("skill's demo: observed", obs, "p", round(pv, 4))
# mono-shuffle only shuffles seq1: verify composition preserved and other sequence untouched
import random
random.seed(1); sh = ep.shuffle_seq('MKTIIALSYIFCLVFA')
check("shuffle preserves composition", sorted(sh) == sorted('MKTIIALSYIFCLVFA'))
try:
    ep.shuffle_seq('ACGT', preserve='di')
except NotImplementedError as e:
    print("preserve='di' ->", e)
summary()
