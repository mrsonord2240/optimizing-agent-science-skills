"""pwalign gapOpening=11/ext=1 global (=282 in input7_R_biostrings.R) must equal Biopython global open -12/ext -1 (the Skill's conversion rule)."""
from common import *
a, b = prot('P69905').seq, prot('P68871').seq
B62 = substitution_matrices.load('BLOSUM62')
s = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-12, extend_gap_score=-1).score(a, b)
check("Biopython global -12/-1 == pwalign global gapOpening 11/ext 1 (282)", s == 282, s)
summary()
