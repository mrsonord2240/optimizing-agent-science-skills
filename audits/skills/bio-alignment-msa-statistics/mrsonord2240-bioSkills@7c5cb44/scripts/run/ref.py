"""Independent ground-truth implementations (written by the auditor, NOT from the Skill).
Second implementations: numpy / scipy / Bio.Phylo / definitional PID (Raghava & Barton 2006; pwalign::pid semantics)."""
import math
import itertools
import numpy as np
from scipy.stats import entropy as sp_entropy
from scipy.spatial.distance import jensenshannon

GAPCH = set('-.~')
AA20 = 'ARNDCQEGHILKMFPSTWYV'
# Robinson & Robinson 1991 as used by NCBI BLAST (blast_stat.c, 'Robinson_prob'), percent -> fraction
ROB_TRUE = dict(A=.07805, R=.05129, N=.04487, D=.05364, C=.01925, Q=.04264, E=.06295, G=.07377, H=.02199,
                I=.05142, L=.09019, K=.05744, M=.02243, F=.03856, P=.05203, S=.07120, T=.05841, W=.01330,
                Y=.03216, V=.06441)


def norm_rows(rows):
    """upper-case, all gap glyphs -> '-'"""
    return [''.join('-' if c in GAPCH else c.upper() for c in r) for r in rows]


def pid_ref(a, b):
    """Return dict PID1 (Doolittle: aligned + INTERNAL gap positions; terminal overhang excluded),
    PID2, PID3, PID4, plus n_id. a,b already normalised."""
    ra = [i for i, c in enumerate(a) if c != '-']
    rb = [i for i, c in enumerate(b) if c != '-']
    a0, a1, b0, b1 = ra[0], ra[-1], rb[0], rb[-1]
    ident = aligned = internal = 0
    for i, (x, y) in enumerate(zip(a, b)):
        if x != '-' and y != '-':
            aligned += 1
            ident += (x == y)
        elif x == '-' and y != '-':          # gap in a: internal iff a has residues on both sides
            internal += (a0 < i < a1)
        elif y == '-' and x != '-':
            internal += (b0 < i < b1)
    la, lb = len(ra), len(rb)
    return dict(n_id=ident, aligned=aligned, PID1=ident / (aligned + internal), PID2=ident / aligned,
                PID3=ident / min(la, lb), PID4=ident / ((la + lb) / 2))


def col_arrays(rows):
    return np.array([list(r) for r in rows])


def conservation_ref(col, ignore_gaps=True):
    c = [x for x in col if x != '-'] if ignore_gaps else list(col)
    if not c:
        return 0.0
    vals, cnt = np.unique(c, return_counts=True)
    return cnt.max() / cnt.sum()


def entropy_ref(col):
    c = [x for x in col if x != '-']
    if not c:
        return 0.0
    _, cnt = np.unique(c, return_counts=True)
    return float(sp_entropy(cnt, base=2))


def ic_ref(col, bg):
    """KL(p || bg) in bits over the 20/4 background alphabet; residues outside the background are dropped
    and the column renormalised (the defensible treatment), returns (ic, n_dropped)."""
    c = [x for x in col if x != '-']
    inn = [x for x in c if x in bg]
    if not inn:
        return 0.0, len(c)
    vals, cnt = np.unique(inn, return_counts=True)
    p = cnt / cnt.sum()
    q = np.array([bg[v] for v in vals])
    return float(np.sum(p * np.log2(p / q))), len(c) - len(inn)


def jsd_ref(col, bg, keys=AA20):
    """JSD (bits) between column distribution over `keys` (gaps/other dropped) and bg; scipy returns sqrt(JSD)."""
    c = [x for x in col if x in keys]
    if not c:
        return 0.0
    p = np.array([c.count(k) for k in keys], float)
    p /= p.sum()
    q = np.array([bg[k] for k in keys], float)
    q /= q.sum()
    return float(jensenshannon(p, q, base=2) ** 2)


def sp_ref(rows, matrix):
    """BLOSUM sum-of-pairs, gap-containing pairs contribute 0; matrix is Bio Array; upper-case alphabet."""
    total = 0.0
    n_skipped = 0
    for col in zip(*rows):
        for x, y in itertools.combinations(col, 2):
            if x == '-' or y == '-':
                continue
            try:
                total += matrix[x, y]
            except Exception:
                n_skipped += 1
    return total, n_skipped


def sp_simple_ref(rows, match=1, mismatch=-1, gap=-2, gapgap=0):
    """Textbook simple SP: gap/residue pair = gap; gap/gap pair scored `gapgap` (0 by convention)."""
    tot = 0
    for col in zip(*rows):
        for x, y in itertools.combinations(col, 2):
            if x == '-' and y == '-':
                tot += gapgap
            elif x == '-' or y == '-':
                tot += gap
            elif x == y:
                tot += match
            else:
                tot += mismatch
    return tot


def kimura_ref(a, b):
    both = [(x, y) for x, y in zip(a, b) if x != '-' and y != '-']
    if not both:
        return float('nan')
    p = 1 - sum(x == y for x, y in both) / len(both)
    v = 1 - p - 0.2 * p * p
    return -math.log(v) if v > 0 else float('inf')


def pssm_ref(rows, bg, pc=1.0):
    """log2((c_r + pc*bg_r)/(n+pc)/bg_r), n = number of residues in `bg` alphabet (upper-cased input)."""
    out = []
    for col in zip(*rows):
        c = [x for x in col if x != '-']
        n = len(c)
        d = {}
        for r in bg:
            d[r] = math.log2(((c.count(r) + pc * bg[r]) / (n + pc)) / bg[r])
        out.append(d)
    return out
