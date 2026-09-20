"""SKILL.md claim: '.get((c1, c2), 0) on an Array silently always returns 0'. Probe Biopython 1.88."""
from Bio.Align import substitution_matrices
BL = substitution_matrices.load('BLOSUM62')
print('BL.get((A,A),0) =', BL.get(('A', 'A'), 0), '| BL[A,A] =', BL['A', 'A'], '| BL.get(("A","A")) =', BL.get(('A','A')))
print('BL.get((W,W),0) =', BL.get(('W', 'W'), 0), '| BL[W,W] =', BL['W', 'W'])
print(type(BL).__mro__[:3])
assert BL.get(('A', 'A'), 0) == 4 and BL['A', 'A'] == 4
print('REFUTED: in Biopython 1.88 Array.get((c1,c2),0) returns the correct score (4.0), not 0; the SKILL.md claim is inaccurate for 1.88')
