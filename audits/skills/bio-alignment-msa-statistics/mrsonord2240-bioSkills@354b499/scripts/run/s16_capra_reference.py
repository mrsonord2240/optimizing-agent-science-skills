"""Capra & Singh 2007 JSD: compare the Skill's examples/capra_singh_jsd.py against a PYTHON-3 PORT of the authors' own
score_conservation.py (downloaded 2026-09-20 from https://compbio.cs.princeton.edu/conservation/score_conservation.py, saved as
data/score_conservation.py; Python 2, so the four functions js_divergence / weighted_freq_count_pseudocount /
weighted_gap_penalty / window_score / calculate_sequence_weights are re-typed here, logic unchanged).
Claims tested (SKILL.md / example header): (1) the Robinson background 'gives effectively-equivalent column ranking' to the
BLOSUM62 background of the original; (2) the Skill's implementation reproduces the reference algorithm.  REAL data: Pfam seed."""
import os, sys, math, json
import numpy as np
from scipy.stats import spearmanr
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import ref
from Bio import AlignIO
import capra_singh_jsd as CS

AA = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', '-']
IDX = {a: i for i, a in enumerate(AA)}
BLOSUM_BG = [0.078, 0.051, 0.041, 0.052, 0.024, 0.034, 0.059, 0.083, 0.025, 0.062, 0.092, 0.056, 0.024, 0.044, 0.043, 0.059, 0.055, 0.014, 0.034, 0.072]
PC = .0000001

def wfc(col, w, pc):                       # weighted_freq_count_pseudocount (original)
    fc = len(AA) * [pc]
    for k, a in enumerate(AA):
        for j in range(len(col)):
            if col[j] == a: fc[k] += w[j]
    return [x / (sum(w) + len(AA) * pc) for x in fc]
def gap_pen(col, w):                        # weighted_gap_penalty (original)
    return 1 - sum(w[i] for i in range(len(col)) if col[i] == '-') / sum(w)
def jsd_orig(col, bg, w):                   # js_divergence (original), gap_penalty=1
    fc = wfc(col, w, PC)[:-1]; s = sum(fc); fc = [x / s for x in fc]
    r = [.5 * f + .5 * b for f, b in zip(fc, bg)]
    d = 0.
    for i in range(len(fc)):
        if r[i] != 0.0:
            if fc[i] == 0.0: d += bg[i] * math.log(bg[i] / r[i], 2)
            elif bg[i] == 0.0: d += fc[i] * math.log(fc[i] / r[i], 2)
            else: d += fc[i] * math.log(fc[i] / r[i], 2) + bg[i] * math.log(bg[i] / r[i], 2)
    return d / 2 * gap_pen(col, w)
def win_orig(scores, wl):                   # window_score (original): edges unchanged, lam weights the column itself
    out = scores[:]
    for i in range(wl, len(scores) - wl):
        if scores[i] < 0: continue
        s = 0.; n = 0
        for j in range(i - wl, i + wl + 1):
            if i != j and scores[j] >= 0: n += 1; s += scores[j]
        if n > 0: out[i] = .5 * (s / n) + .5 * scores[i]
    return out
def henikoff(msa):                          # calculate_sequence_weights (original)
    w = [0.] * len(msa)
    for i in range(len(msa[0])):
        fc = [0] * len(AA)
        for r in msa:
            if r[i] != '-': fc[IDX[r[i]]] += 1
        ntypes = sum(1 for x in fc if x > 0)
        for j, r in enumerate(msa):
            d = fc[IDX[r[i]]] * ntypes
            if d > 0: w[j] += 1. / d
    return [x / len(msa[0]) for x in w]

aln = AlignIO.read(os.path.join(HERE, 'data', 'seed_norm.fasta'), 'fasta')
# original crashes (KeyError) on B/Z: replace with gaps for the reference run only (27 of 10,293 residues)
rows = [''.join('-' if c in 'BZ' else c for c in str(r.seq)) for r in aln]
N, L = len(rows), len(rows[0]); cols = [[r[i] for r in rows] for i in range(L)]
unit = [1.] * N; hw = henikoff(rows)
rob = [CS.ROBINSON_BACKGROUND[a] for a in AA[:-1]]; rob = [x / sum(rob) for x in rob]

sk = np.array(CS.capra_singh_score(aln))                                              # Skill: Robinson bg, unweighted, edge-smoothed
o_unit_rob_raw = np.array([jsd_orig(c, rob, unit) for c in cols])                      # original formula, Skill's background, unit weights
sk_raw = []                                                                            # Skill raw (unsmoothed) via its own js_divergence
from collections import Counter
for i in range(L):
    full = ''.join(cols[i]); colng = full.replace('-', '')
    if not colng: sk_raw.append(0.0); continue
    cnt = Counter(colng); tot = len(colng)
    sk_raw.append(CS.js_divergence({k: v / tot for k, v in cnt.items()}, CS.ROBINSON_BACKGROUND) * (1 - full.count('-') / N))
sk_raw = np.array(sk_raw)
print('(1) Skill raw JSD vs original formula (same bg, unit weights): max |diff| = %.4f, Spearman = %.4f' % (np.abs(sk_raw - o_unit_rob_raw).max(), spearmanr(sk_raw, o_unit_rob_raw)[0]))
orig_default = np.array(win_orig([jsd_orig(c, BLOSUM_BG, hw) for c in cols], 3))       # authors' default: BLOSUM62 bg, Henikoff weights, window 3
orig_noW = np.array(win_orig([jsd_orig(c, BLOSUM_BG, unit) for c in cols], 3))          # authors' algorithm without weights
rho_def = spearmanr(sk, orig_default)[0]; rho_nw = spearmanr(sk, orig_noW)[0]
top = lambda x, k: set(np.argsort(-x)[:k].tolist())
print('(2) Skill (Robinson bg, unweighted) vs authors\' BLOSUM62 bg + Henikoff weights: Spearman %.4f ; top-10 overlap %d/10 ; top-30 overlap %d/30' % (rho_def, len(top(sk, 10) & top(orig_default, 10)), len(top(sk, 30) & top(orig_default, 30))))
print('(3) Skill vs authors\' algorithm, BLOSUM62 bg, NO weights (isolates background choice): Spearman %.4f ; top-10 %d/10 ; top-30 %d/30' % (rho_nw, len(top(sk, 10) & top(orig_noW, 10)), len(top(sk, 30) & top(orig_noW, 30))))
w_only = spearmanr(orig_default, orig_noW)[0]
print('(4) effect of Henikoff weighting alone (authors\' algorithm): Spearman %.4f ; top-10 %d/10' % (w_only, len(top(orig_default, 10) & top(orig_noW, 10))))
gf = np.array([c.count('-') / N for c in cols])
print('(5) gappy columns: authors\' full script masks columns above a gap cutoff (their web tool default 30%%); Skill keeps and down-weights. Columns with >=30%% gaps: %d ; of them in Skill top-30: %d' % ((gf >= .3).sum(), sum(1 for k in top(sk, 30) if gf[k] >= .3)))
ok = rho_nw > 0.95
json.dump(dict(raw_maxdiff=float(np.abs(sk_raw - o_unit_rob_raw).max()), rho_default=float(rho_def), rho_noweights=float(rho_nw), rho_weights_only=float(w_only),
               top10_default=len(top(sk, 10) & top(orig_default, 10)), top30_default=len(top(sk, 30) & top(orig_default, 30))), open(os.path.join(HERE, 'results_capra.json'), 'w'), indent=1)
print('CHECK Skill formula reproduces the authors\' JSD (raw max diff < 0.01):', 'PASS' if np.abs(sk_raw - o_unit_rob_raw).max() < 0.01 else 'FAIL')
