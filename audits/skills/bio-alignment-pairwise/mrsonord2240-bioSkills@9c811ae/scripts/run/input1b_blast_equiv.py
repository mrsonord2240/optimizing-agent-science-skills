"""Skill claim (2026-09-19 fix): BLASTP 11/1 == Biopython open -12 / extend -1; -11/-1 == EMBOSS 11/1. Ground truth = blastp raw score 285 (logs/input1_emboss_blast.txt), EMBOSS water 288."""
from common import *
a, b = prot('P69905'), prot('P68871')
B62 = substitution_matrices.load('BLOSUM62')
res = {}
for o in (-11, -12):
    al = PairwiseAligner(mode='local', substitution_matrix=B62, open_gap_score=o, extend_gap_score=-1)
    A = al.align(a.seq, b.seq)[0]
    res[o] = A
    print(f"local open={o} ext=-1: score={A.score} aligned={A.aligned.tolist()}")
check("Skill now says -11/-1 is EMBOSS 11/1 (not BLASTP): local -11/-1 != BLASTP raw 285", res[-11].score != 285, res[-11].score)
check("Skill: BLASTP defaults (11/1) are open_gap_score=-12/extend -1 -> raw score 285 (blastp -comp_based_stats 0 measured in input1_emboss_blast.sh)", res[-12].score == 285, res[-12].score)
# BLAST HSP coords (1-based inclusive): q 3-141, s 4-146
q0, q1 = res[-12].aligned[0][0][0], res[-12].aligned[0][-1][1]
s0, s1 = res[-12].aligned[1][0][0], res[-12].aligned[1][-1][1]
check("local -12/-1 coordinates match BLAST HSP (q 3..141, s 4..146, 1-based)", (q0+1, q1, s0+1, s1) == (3, 141, 4, 146), (q0+1, q1, s0+1, s1))
# EMBOSS water 11/1 = 288 == Biopython -11/-1
check("Biopython local -11/-1 == EMBOSS water 11/1 (288)", res[-11].score == 288, res[-11].score)
summary()
