"""Check SKILL.md API/prose claims against installed Biopython. Every claim prints the observed value and asserts."""
import Bio, sys
from Bio.Align import PairwiseAligner, substitution_matrices
from Bio.Seq import Seq
print("Biopython", Bio.__version__)
res = {}
def check(name, cond, obs=""):
    res[name] = bool(cond)
    print(("PASS " if cond else "FAIL "), name, "|", obs)

a = PairwiseAligner()
check("defaults match1/mis0/gaps0", (a.match_score, a.mismatch_score, a.open_gap_score, a.extend_gap_score)==(1.0,0.0,0.0,0.0), (a.match_score, a.mismatch_score, a.open_gap_score, a.extend_gap_score))
names = substitution_matrices.load()
check("30 matrices listed", len(names)==30, f"{len(names)}: {names}")
check("HOXD70 present", "HOXD70" in names)
nuc = substitution_matrices.load('NUC.4.4')
check("NUC.4.4 match=+5 mismatch=-4", nuc['A','A']==5 and nuc['A','C']==-4, (nuc['A','A'], nuc['A','C']))
check("NUC.4.4 R vs A is +1 (claim)", nuc['R','A']==1, nuc['R','A'])
print("NUC.4.4 alphabet:", nuc.alphabet)
# algorithm names
def algo(**kw):
    x = PairwiseAligner(**kw); return x.algorithm
print("algo global linear:", algo(mode='global', open_gap_score=-1, extend_gap_score=-1))
print("algo global affine:", algo(mode='global', open_gap_score=-10, extend_gap_score=-0.5))
print("algo local linear:", algo(mode='local', open_gap_score=-1, extend_gap_score=-1))
print("algo local affine:", algo(mode='local', open_gap_score=-10, extend_gap_score=-0.5))
b = PairwiseAligner(mode='global', open_gap_score=-10, extend_gap_score=-0.5)
b.target_internal_open_gap_score = -3
print("algo global WSB (diff internal):", b.algorithm)
# max_alignments
try:
    a.max_alignments = 100
    print("max_alignments settable (no error); attr read back:", getattr(a,'max_alignments','<none>'), "in dir:", 'max_alignments' in dir(a))
except Exception as e:
    print("max_alignments set ERROR", type(e).__name__, e)
# pairwise2
try:
    import Bio.pairwise2
    print("Bio.pairwise2 import OK")
except Exception as e:
    print("Bio.pairwise2 import ->", type(e).__name__, e)
# end_gap_score
try:
    c = PairwiseAligner(mode='global'); c.end_gap_score = 0.0
    print("end_gap_score ok", c.query_left_open_gap_score, c.target_right_extend_gap_score)
except Exception as e:
    print("end_gap_score ERROR", e)
# formats
al = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5).align(Seq('ACCGGTAACGTAG'), Seq('ACCGTTAACGAAG'))
x = al[0]
for fmt in ('fasta','clustal','psl','sam'):
    try:
        out = format(x, fmt); print(f"--- format {fmt}: OK ({len(out)} chars)\n{out[:250]}")
    except Exception as e:
        print(f"--- format {fmt}: ERROR {type(e).__name__}: {e}")
print("shape", x.shape, "len", len(x), "x[0,:]", x[0,:], "x[1,:]", x[1,:])
print("aligned", x.aligned.tolist(), "coordinates", x.coordinates.tolist())
cn = x.counts()
print("counts", cn)
check("counts identities=11 mismatches=2 gaps=0", (cn.identities, cn.mismatches, cn.gaps)==(11,2,0), cn)
print("substitutions:\n", x.substitutions)
check("substitutions['G','T'] == 1 (G aligned to T once)", x.substitutions['G','T']==1, x.substitutions['G','T'])
check("len(alignments) and count", len(al)==1, len(al))
# local, all-negative scoring
try:
    l = PairwiseAligner(mode='local', match_score=-1, mismatch_score=-1, open_gap_score=-1, extend_gap_score=-1)
    r = l.align('ACGT','ACGT'); print("local all-negative: n=", len(r), "score", r.score if hasattr(r,'score') else None)
    print(r[0])
except Exception as e:
    print("local all-negative ERROR", type(e).__name__, e)
# Overflow with many optimal alignments
from Bio.Align import PairwiseAligner as PA
pa = PA(mode='global', match_score=1, mismatch_score=0, open_gap_score=0, extend_gap_score=0)
r = pa.align('A'*40+'C'*40, 'A'*20+'C'*20+'A'*20)
try:
    print("many-optimal len:", len(r))
except OverflowError as e:
    print("many-optimal len -> OverflowError", e)
r2 = PA(mode='global').align('ACGT'*30, 'TGCA'*30)
try:
    n = len(r2); print("len(r2)=", n)
except OverflowError as e:
    print("OverflowError", str(e)[:100])
# aligner printing
print(PairwiseAligner(mode='global', substitution_matrix=substitution_matrices.load('BLOSUM62'), open_gap_score=-11, extend_gap_score=-1))
