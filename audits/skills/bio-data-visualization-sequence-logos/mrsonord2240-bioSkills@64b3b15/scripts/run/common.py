import numpy as np, os
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data"); OUT = os.path.join(HERE, "out")
def ic_uniform(counts, K=None, small=False):
    """independent IC per column; counts: (L, K) array. Schneider 1986 e_n correction if small."""
    counts = np.asarray(counts, float); n = counts.sum(1)
    p = counts / n[:, None]; K = counts.shape[1]
    with np.errstate(divide="ignore", invalid="ignore"):
        H = -np.nansum(np.where(p > 0, p * np.log2(p), 0), axis=1)
    ic = np.log2(K) - H
    if small: ic = ic - (K - 1) / (2 * np.log(2) * n)
    return ic
def ic_bg(counts, bg):
    counts = np.asarray(counts, float); p = counts / counts.sum(1, keepdims=True)
    bg = np.asarray(bg, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.nansum(np.where(p > 0, p * np.log2(p / bg), 0), axis=1)
def count_matrix(seqs, alphabet):
    L = len(seqs[0]); M = np.zeros((L, len(alphabet)))
    for s in seqs:
        for i, c in enumerate(s): M[i, alphabet.index(c)] += 1
    return M
