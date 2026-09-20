import warnings; warnings.simplefilter('ignore')
import Bio
from Bio.Align import PairwiseAligner, substitution_matrices
print(Bio.__version__)
print(PairwiseAligner())
a = PairwiseAligner(mode='global', substitution_matrix=substitution_matrices.load('BLOSUM62'))
print("BLOSUM62 + DEFAULT gaps: open", a.open_gap_score, "extend", a.extend_gap_score)
x = a.align("HEAGAWGHEE","PAWHEAE")
print(x[0], x.score)
# WSB
b = PairwiseAligner(mode='global'); b.gap_score = lambda i,l: -1-0.5*l**0.5 if False else -2.0 if l>0 else 0
print("algo with callable gap fn:", b.algorithm)
b2 = PairwiseAligner(mode='global', match_score=1, mismatch_score=0)
b2.gap_score = lambda pos, length: -length*0.5
print("callable linear:", b2.algorithm)
