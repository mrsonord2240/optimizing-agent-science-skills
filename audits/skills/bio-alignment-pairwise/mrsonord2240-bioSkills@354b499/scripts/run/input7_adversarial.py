"""Input 7 (Adversarial/ambiguous): user asks (i) 'just use pairwise2', (ii) 'set aligner.max_alignments as the skill says' on a repetitive
sequence, (iii) 'report percent identity so it matches EMBOSS 43.6%', (iv) IUPAC-ambiguous DNA with NUC.4.4, (v) 'is score 292 significant?'.
Everything checked against independent values (EMBOSS needle 43.6%, hand-summed matrix scores)."""
import itertools, warnings
from common import *
from Bio.Seq import Seq
a, b = prot('P69905').seq, prot('P68871').seq
B62 = substitution_matrices.load('BLOSUM62')
# (i) pairwise2 still importable? does it agree?
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always')
    from Bio import pairwise2
    r = pairwise2.align.globalds(str(a), str(b), B62, -10, -0.5, one_alignment_only=True)
print("pairwise2 deprecation warning emitted:", any('deprecated' in str(w.message) for w in W), "| score", r[0].score)
al = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-10, extend_gap_score=-0.5)
check("pairwise2.globalds(-10,-0.5) == PairwiseAligner(-10,-0.5): 292.5", r[0].score == al.score(a, b) == 292.5, r[0].score)
# (ii) max_alignments per skill
al2 = PairwiseAligner(mode='global', match_score=1, mismatch_score=0, open_gap_score=0, extend_gap_score=0)
try:
    al2.max_alignments = 100; ok = True
except Exception as e:
    ok = False; print("aligner.max_alignments = 100 ->", type(e).__name__, e)
check("SKILL.md/usage-guide 'aligner.max_alignments = 100' works on 1.88", ok)
rep = al2.align('A'*40 + 'C'*40, 'A'*20 + 'C'*20 + 'A'*20)
try:
    n = len(rep); print("n alignments", n)
except OverflowError as e:
    print("SKILL first snippet `len(alignments)` -> OverflowError:", e)
    ok2 = False
else: ok2 = True
check("skill's `print(len(alignments))` snippet survives repetitive input", ok2)
got = [x.score for x in itertools.islice(rep, 5)]
check("lazy iteration (skill's enumerate/break loop, or islice) still works after OverflowError", len(got) == 5, got)
# (iii) PID definitions on the real alignment (open -10, ext -0.5 -> EMBOSS needle 65/149 = 43.6%)
A = al.align(a, b)[0]; c = A.counts(); s0, s1 = A[0, :], A[1, :]
L = len(s0); pid1 = 100 * c.identities / L; pid2 = 100 * c.identities / (c.identities + c.mismatches)
pid3 = 100 * c.identities / min(len(a), len(b)); pid4 = 100 * c.identities / ((len(a) + len(b)) / 2)
print(f"PID1={pid1:.1f} PID2={pid2:.1f} PID3={pid3:.1f} PID4={pid4:.1f}  (Skill's counts() recipe gives PID2)")
check("PID1 == EMBOSS needle identity 43.6%; PID3/PID4 match Biostrings pid() (45.8/45.0)", round(pid1, 1) == 43.6 and round(pid3, 1) == 45.8 and round(pid4, 1) == 45.0, (round(pid1, 1), round(pid3, 1), round(pid4, 1)))
check("PID2 is the highest of the four (skill table claim)", pid2 == max(pid1, pid2, pid3, pid4))
check("Skill's recipe (identities/(identities+mismatches)) != EMBOSS-reported 43.6% (needs the caveat the skill gives)", round(pid2, 1) != 43.6, round(pid2, 1))
# (iv) NUC.4.4 IUPAC
nuc = substitution_matrices.load('NUC.4.4')
nl = PairwiseAligner(mode='global', substitution_matrix=nuc, open_gap_score=-10, extend_gap_score=-0.5)
q, t = 'ACGTRYNACGT', 'ACGTAGCACGT'
hand = sum(nuc[x, y] for x, y in zip(q, t))
check("NUC.4.4 IUPAC alignment score == hand sum of matrix cells", nl.score(t, q) == hand, (nl.score(t, q), hand))
print("cells R/A", nuc['R', 'A'], "Y/G", nuc['Y', 'G'], "N/C", nuc['N', 'C'], "R/G", nuc['R', 'G'], "-> ambiguity-aware scoring is partial (+1) / negative as skill says")
# (v) is 292.5 significant? -> answer requires null model. Already done in input4. Score alone from a gap-free unrelated pair:
kin = next(SeqIO.parse(r'F:\OpenScience\audit-envs\alignment\public-data\structures\1ATP.pdb', 'pdb-seqres')).seq
print("unrelated PKA vs HBB global score (10/0.5):", al.score(kin, b), " vs related HBA/HBB:", al.score(a, b), "(raw score alone is length-dependent; skill says use bit/E)")
summary()
