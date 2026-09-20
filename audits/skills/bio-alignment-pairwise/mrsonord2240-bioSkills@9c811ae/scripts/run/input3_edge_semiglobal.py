# -*- coding: utf-8 -*-
"""Input 3 (Edge): the Skill's semiglobal snippets and its new 'Input Checks' section, every claim re-verified.
(a) semiglobal fragment-in-reference: the two snippets exactly as written (reference SYNTHETIC seed 11, fragment at [300,320]);
(b) global/local/semiglobal ordering; independent semiglobal DP for a mutated fragment;
(c) each 'Input Checks' bullet; (d) internal-stop expression on the 7 REAL RefSeq HBB CDS; (e) old query_* names still accepted with DeprecationWarning."""
import random, warnings
from common import *
from Bio.Seq import Seq
from ref_gotoh import semiglobal_score
random.seed(11)
rnd = lambda n: ''.join(random.choice('ACGT') for _ in range(n))
frag = 'GATTACAGATTACCAGGCTA'
reference = rnd(300) + frag + rnd(300); fragment = frag
# (a1) Skill snippet 1: end_gap_score = 0.0
a1 = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
a1.end_gap_score = 0.0
A = a1.align(reference, fragment)[0]
check("snippet1 end_gap_score=0: score 40.0, target span [[300,320]]", A.score == 40 and A.aligned[0].tolist() == [[300, 320]], (A.score, A.aligned[0].tolist()))
check("snippet1 is order-independent (align(fragment, reference) also 40)", a1.align(fragment, reference)[0].score == 40, a1.align(fragment, reference)[0].score)
# (a2) Skill snippet 2: new names, free end gaps on the query only, without warnings
with warnings.catch_warnings():
    warnings.simplefilter('error')
    a2 = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
    a2.open_left_deletion_score = a2.extend_left_deletion_score = 0
    a2.open_right_deletion_score = a2.extend_right_deletion_score = 0
    B = a2.align(reference, fragment)[0]
check("snippet2 (open/extend_left/right_deletion_score, warnings-as-errors): 40.0, [[300,320]]", B.score == 40 and B.aligned[0].tolist() == [[300, 320]], (B.score, B.aligned[0].tolist()))
sw = a2.align(fragment, reference)[0].score
check("snippet2 argument order matters: align(fragment, reference) scored -279 (the Skill's number)", sw == -279, sw)
# (a3) mutated fragment vs independent DP
fm = list(frag); fm[5] = 'T'; del fm[12]; fm = ''.join(fm)
S = lambda x, y: 2 if x == y else -1
g = semiglobal_score(reference, fm, S, 10, 0.5)
check("mutated fragment: end_gap_score=0 score == independent semiglobal DP", a1.score(reference, fm) == g, (a1.score(reference, fm), g))
# (b) ordering
gl = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
lo = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
print(f"global={gl.score(reference, fragment)} local={lo.score(reference, fragment)} semiglobal={a1.score(reference, fragment)}")
check("global < local == semiglobal (Skill's 'Common mistake' note)", gl.score(reference, fragment) < lo.score(reference, fragment) == a1.score(reference, fragment))
# (c) Input Checks bullets
B62 = substitution_matrices.load('BLOSUM62'); NUC = substitution_matrices.load('NUC.4.4')
pa = PairwiseAligner(mode='global', substitution_matrix=B62, open_gap_score=-11, extend_gap_score=-1)
na = PairwiseAligner(mode='global', substitution_matrix=NUC, open_gap_score=-10, extend_gap_score=-0.5)
mm = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
def raises(f, exc=ValueError):
    try: f(); return None
    except exc as e: return str(e)[:80]
    except Exception as e: return 'OTHER ' + type(e).__name__
r_lower = raises(lambda: pa.score('mkvlaa', 'MKVLAA')); r_nl = raises(lambda: pa.score('MKVL\n', 'MKVL')); r_J = raises(lambda: pa.score('MKJL', 'MKLL')); r_U = raises(lambda: pa.score('MKUL', 'MKCL'))
r_nucU = raises(lambda: na.score('ACGU', 'ACGT'))
print("ValueErrors:", r_lower, "|", r_nl, "|", r_J, "|", r_U, "|", r_nucU)
check("Skill: lowercase / trailing newline / J / U raise ValueError with a substitution matrix; NUC.4.4 also rejects U", all(x and not x.startswith('OTHER') for x in (r_lower, r_nl, r_J, r_U, r_nucU)))
check("Skill: match/mismatch aligner does NOT raise: 'acgt' vs 'ACGT' = four mismatches (-4); U vs T a mismatch", mm.score('acgt', 'ACGT') == -4 and mm.score('ACGU', 'ACGT') == 3 * 2 - 1, (mm.score('acgt', 'ACGT'), mm.score('ACGU', 'ACGT')))
r_empty = raises(lambda: pa.align('MKVL', ''))
print("empty ->", r_empty)
check("Skill: empty sequence raises ValueError: sequence has zero length", r_empty is not None and 'zero length' in r_empty, r_empty)
ok = []
for lab, f in [('star', lambda: pa.score('MKVL*', 'MKVLA')), ('XBZ', lambda: pa.score('MKXBZ', 'MKVLA'))]:
    try: ok.append((lab, f()))
    except Exception as e: ok.append((lab, 'ERR ' + str(e)[:60]))
print(ok)
check("Skill: '*', X/B/Z accepted silently", all(not isinstance(v, str) for _, v in ok), ok)
ra, rb = prot('P69905'), prot('P68871')
try: sr = pa.score(ra, rb); srok = sr == pa.score(ra.seq, rb.seq)
except Exception as e: sr, srok = str(e)[:60], False
check("Skill: a SeqRecord is accepted and scores identically to its .seq", srok, sr)
# strand
fwd = mm.score('T' * 20 + frag + 'G' * 20, frag)
rc = mm.score('T' * 20 + frag + 'G' * 20, str(Seq(frag).reverse_complement()))
print("strand: fwd (global, embedded) vs rc", fwd, rc)
lo2 = PairwiseAligner(mode='local', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
rng = random.Random(3)
diffs = []
for _ in range(50):
    s30 = ''.join(rng.choice('ACGT') for _ in range(30)); ctx = ''.join(rng.choice('ACGT') for _ in range(50)) + s30 + ''.join(rng.choice('ACGT') for _ in range(50))
    diffs.append((lo2.score(ctx, s30), lo2.score(ctx, str(Seq(s30).reverse_complement()))))
import statistics
print("50 random 30-mers, local 2/-1: forward always", set(d[0] for d in diffs), "| revcomp median", statistics.median(d[1] for d in diffs), "max", max(d[1] for d in diffs))
check("Skill: 30-nt exact match scores 60; reverse complement scores near zero (median <= 20, max < 60)", set(d[0] for d in diffs) == {60.0} and statistics.median(d[1] for d in diffs) <= 20 and max(d[1] for d in diffs) < 60, (statistics.median(d[1] for d in diffs), max(d[1] for d in diffs)))
# (d) internal-stop expression on real CDS
recs = list(SeqIO.parse(DATA + r'\hbb_cds_mammals.fasta', 'fasta'))
flag = ['NM_001314043.1' if r.id.split('_cds')[0].endswith('NM_001314043.1') else r.id[4:16] for r in recs if '*' in str(r.seq.translate()).rstrip('*')]
print("records flagged by the Skill's internal-stop expression:", flag, "of", len(recs))
check("Skill: expression flags NM_001314043.1 and none of the 6 clean CDS", flag == ['NM_001314043.1'], flag)
# (e) deprecated names
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always')
    d = PairwiseAligner(mode='global', match_score=2, mismatch_score=-1, open_gap_score=-10, extend_gap_score=-0.5)
    d.query_left_open_gap_score = 0; d.query_left_extend_gap_score = 0; d.query_right_open_gap_score = 0; d.query_right_extend_gap_score = 0
    sc = d.score(reference, fragment)
check("Skill: old query_left/right_* names still accepted on 1.88 with DeprecationWarning, same result (40)", sc == 40 and any(issubclass(w.category, DeprecationWarning) or 'renamed' in str(w.message) for w in W), (sc, [str(w.message)[:50] for w in W][:1]))
summary()
