"""Numeric claim check: SKILL.md / capra_singh_jsd.py say the Robinson-background, unweighted example gives 'effectively
equivalent column ranking' to the authors' script (Spearman 0.98, top-10 overlap 9/10). Re-tested against a Python-3 port of the
authors' own score_conservation.py (data/score_conservation.py, downloaded from compbio.cs.princeton.edu in the first audit;
the four functions are re-typed below, logic unchanged) on the real Pfam PF00042 seed, with the FIXED example.
Run from run/:  PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python b10_capra_authors.py"""
import os, sys, math, json
from collections import Counter
import numpy as np
from scipy.stats import spearmanr
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'skill', 'examples'))
import msa_utils, capra_singh_jsd as CS

AA = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V', '-']
IDX = {a: i for i, a in enumerate(AA)}
BLOSUM_BG = [0.078, 0.051, 0.041, 0.052, 0.024, 0.034, 0.059, 0.083, 0.025, 0.062, 0.092, 0.056, 0.024, 0.044, 0.043, 0.059, 0.055, 0.014, 0.034, 0.072]
PC = .0000001
def wfc(col, w, pc):
    fc = len(AA) * [pc]
    for k, a in enumerate(AA):
        for j in range(len(col)):
            if col[j] == a: fc[k] += w[j]
    return [x / (sum(w) + len(AA) * pc) for x in fc]
def gap_pen(col, w):
    return 1 - sum(w[i] for i in range(len(col)) if col[i] == '-') / sum(w)
def jsd_orig(col, bg, w):
    fc = wfc(col, w, PC)[:-1]; s = sum(fc); fc = [x / s for x in fc]
    r = [.5 * f + .5 * b for f, b in zip(fc, bg)]
    d = 0.
    for i in range(len(fc)):
        if r[i] != 0.0:
            if fc[i] == 0.0: d += bg[i] * math.log(bg[i] / r[i], 2)
            elif bg[i] == 0.0: d += fc[i] * math.log(fc[i] / r[i], 2)
            else: d += fc[i] * math.log(fc[i] / r[i], 2) + bg[i] * math.log(bg[i] / r[i], 2)
    return d / 2 * gap_pen(col, w)
def win_orig(scores, wl):
    out = scores[:]
    for i in range(wl, len(scores) - wl):
        if scores[i] < 0: continue
        s = 0.; n = 0
        for j in range(i - wl, i + wl + 1):
            if i != j and scores[j] >= 0: n += 1; s += scores[j]
        if n > 0: out[i] = .5 * (s / n) + .5 * scores[i]
    return out
def henikoff(msa):
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

aln = msa_utils.load_alignment(os.path.join(HERE, 'data', 'seed_dot.fasta'))       # dotted file, normalised by the Skill's own loader
rows = [''.join('-' if c in 'BZ' else c for c in str(r.seq)) for r in aln]          # original crashes on B/Z: replaced by gaps for the reference only
N, L = len(rows), len(rows[0]); cols = [[r[i] for r in rows] for i in range(L)]
unit = [1.] * N; hw = henikoff(rows)
rob = [CS.ROBINSON_BACKGROUND[a] for a in AA[:-1]]; rob = [x / sum(rob) for x in rob]
sk = np.array(CS.capra_singh_score(aln))
o_unit_rob_raw = np.array([jsd_orig(c, rob, unit) for c in cols])
sk_raw = []
for i in range(L):
    full = ''.join(str(aln[k].seq[i]) for k in range(N)); colng = ''.join(c for c in full if c in CS.ROBINSON_BACKGROUND)
    if not colng: sk_raw.append(0.0); continue
    cnt = Counter(colng); tot = len(colng)
    sk_raw.append(CS.js_divergence({k: v / tot for k, v in cnt.items()}, CS.ROBINSON_BACKGROUND) * (1 - full.count('-') / N))
sk_raw = np.array(sk_raw)
d_raw_all = np.abs(sk_raw - o_unit_rob_raw).max()
bz = np.array([any(str(aln[k].seq[i]) in 'BZ' for k in range(N)) for i in range(L)])      # columns where the reference turned B/Z into gaps
d_raw = np.abs(sk_raw - o_unit_rob_raw)[~bz].max()
print('    columns with B/Z (reference counts them as gaps in the gap penalty, Skill drops the letters and keeps them in the gap-penalty denominator): %d ; max |diff| on them %.4f, elsewhere %.1e' % (bz.sum(), np.abs(sk_raw - o_unit_rob_raw)[bz].max(), d_raw))
print('(1) Skill raw JSD vs original formula (same bg, unit weights): max |diff| = %.4f, Spearman = %.4f' % (d_raw, spearmanr(sk_raw, o_unit_rob_raw)[0]))
orig_default = np.array(win_orig([jsd_orig(c, BLOSUM_BG, hw) for c in cols], 3))
orig_noW = np.array(win_orig([jsd_orig(c, BLOSUM_BG, unit) for c in cols], 3))
rho_def = spearmanr(sk, orig_default)[0]; rho_nw = spearmanr(sk, orig_noW)[0]
top = lambda x, k: set(np.argsort(-x)[:k].tolist())
t10 = len(top(sk, 10) & top(orig_default, 10)); t30 = len(top(sk, 30) & top(orig_default, 30))
print("(2) Skill (Robinson bg, unweighted) vs authors' BLOSUM62 bg + Henikoff weights: Spearman %.4f ; top-10 overlap %d/10 ; top-30 overlap %d/30" % (rho_def, t10, t30))
print("(3) Skill vs authors' algorithm, BLOSUM62 bg, NO weights: Spearman %.4f ; top-10 %d/10" % (rho_nw, len(top(sk, 10) & top(orig_noW, 10))))
print('CHECK Skill raw JSD reproduces the authors formula on columns without B/Z (max diff < 1e-3):', 'PASS' if d_raw < 1e-3 else 'FAIL', f'{d_raw:.2e}')
print('CHECK SKILL.md claim Spearman 0.98 (>= 0.97) and top-10 overlap 9/10 (>= 8):', 'PASS' if rho_def >= 0.97 and t10 >= 8 else 'FAIL', f'{rho_def:.4f}, {t10}/10')
json.dump(dict(raw_maxdiff=float(d_raw), rho_default=float(rho_def), rho_noweights=float(rho_nw), top10=t10, top30=t30), open(os.path.join(HERE, 'results_b10.json'), 'w'), indent=1)
