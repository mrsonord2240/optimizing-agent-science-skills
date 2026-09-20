"""Independent pure-Python affine-gap DP (Gotoh), written by the auditor as ground truth.
Convention (same as EMBOSS and Biopython): a gap of length k costs open + (k-1)*extend (both given as positive penalties).
mode: 'global' | 'local' | 'semiglobal' (free end gaps on BOTH sequences).
Returns the optimal score only (no traceback needed for score ground truth).
"""
NEG = -10**9
def load_matrix(name='BLOSUM62'):
    from Bio.Align import substitution_matrices
    m = substitution_matrices.load(name)
    return {(a, b): float(m[a, b]) for a in m.alphabet for b in m.alphabet}

def gotoh_score(x, y, sub, open_pen, ext_pen, mode='global', free_end_x=False, free_end_y=False, end_open=None, end_ext=None):
    """x rows, y cols. sub: function (a,b)->score or dict. Gap penalties positive.
    free_end_*: end gaps free in x / y (gap in the other) -- used for semiglobal/fragment."""
    n, m = len(x), len(y)
    S = sub if callable(sub) else (lambda a, b: sub[(a, b)])
    M = [[NEG]*(m+1) for _ in range(n+1)]   # ends in match/mismatch
    X = [[NEG]*(m+1) for _ in range(n+1)]   # ends in gap in y (x residue vs gap)   [vertical]
    Y = [[NEG]*(m+1) for _ in range(n+1)]   # ends in gap in x                        [horizontal]
    M[0][0] = 0
    for i in range(1, n+1):
        X[i][0] = 0 if (free_end_x or mode=='local') else -(open_pen + (i-1)*ext_pen)
    for j in range(1, m+1):
        Y[0][j] = 0 if (free_end_y or mode=='local') else -(open_pen + (j-1)*ext_pen)
    best = 0 if mode == 'local' else NEG
    for i in range(1, n+1):
        for j in range(1, m+1):
            s = S(x[i-1], y[j-1])
            prev = max(M[i-1][j-1], X[i-1][j-1], Y[i-1][j-1])
            if mode == 'local': prev = max(prev, 0)
            M[i][j] = prev + s
            # X: consume x[i-1] against gap. Gap in interior unless j==m and free_end_y (gap at end of y)? handled below
            ox = open_pen; ex = ext_pen
            if j == m and free_end_x is False and False: pass
            X[i][j] = max(M[i-1][j] - ox, Y[i-1][j] - ox, X[i-1][j] - ex)
            Y[i][j] = max(M[i][j-1] - open_pen, X[i][j-1] - open_pen, Y[i][j-1] - ext_pen)
            if mode == 'local':
                best = max(best, M[i][j])
    if mode == 'local':
        return best
    # global / semiglobal
    if mode == 'global':
        return max(M[n][m], X[n][m], Y[n][m])
    raise ValueError(mode)

def semiglobal_score(x, y, sub, open_pen, ext_pen):
    """Free end gaps on both sequences: max over last row / last col of M,X,Y with free leading gaps."""
    n, m = len(x), len(y)
    S = sub if callable(sub) else (lambda a, b: sub[(a, b)])
    M = [[NEG]*(m+1) for _ in range(n+1)]
    X = [[NEG]*(m+1) for _ in range(n+1)]
    Y = [[NEG]*(m+1) for _ in range(n+1)]
    M[0][0] = 0
    for i in range(1, n+1): M[i][0] = 0   # free leading gap in y: start anywhere in x
    for j in range(1, m+1): M[0][j] = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            M[i][j] = max(M[i-1][j-1], X[i-1][j-1], Y[i-1][j-1], 0 if (i==1 or j==1) else NEG) + S(x[i-1], y[j-1])
            X[i][j] = max(M[i-1][j] - open_pen, Y[i-1][j] - open_pen, X[i-1][j] - ext_pen)
            Y[i][j] = max(M[i][j-1] - open_pen, X[i][j-1] - open_pen, Y[i][j-1] - ext_pen)
    cands = [max(M[n][j], X[n][j], Y[n][j]) for j in range(m+1)] + [max(M[i][m], X[i][m], Y[i][m]) for i in range(n+1)]
    return max(cands)

if __name__ == '__main__':
    # self-test on a hand-computed case
    B = load_matrix()
    # HEAGAWGHEE / PAWHEAE, BLOSUM50 known example score for local = 23 (Durbin), here check BLOSUM62 hand case:
    # AAAA vs AA with open 11 ext 1: global best = 2 matches(4+4) - gap of length 2 (11+1) = -4 ; with BLOSUM62 A/A=4
    assert gotoh_score('AAAA','AA',B,11,1,'global') == 8-12, gotoh_score('AAAA','AA',B,11,1,'global')
    assert gotoh_score('AAAA','AA',B,11,1,'local') == 8
    print("ref_gotoh self-test ok")
