# Input 3: Logomaker route -- SKILL.md blocks verbatim + independent IC / background / pseudocount / alphabet assertions
import os, sys, warnings, io
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import logomaker
from common import *

print("logomaker", logomaker.__version__, "pandas", pd.__version__, "numpy", np.__version__, "matplotlib", matplotlib.__version__)
res = []
def ok(name, cond, note=""):
    res.append((name, bool(cond)))
    print(f"ASSERT {name:<78s} {'PASS' if cond else 'FAIL'} {note}")

A = list("ACGT")
def counts_df(seqs, alpha=A):
    return pd.DataFrame(count_matrix(seqs, alpha), columns=alpha)

# ---------- SKILL block: counts -> information (verbatim) ----------
counts = pd.DataFrame({'A': [10, 0, 5, 8], 'C': [0, 8, 5, 1], 'G': [0, 2, 0, 0], 'T': [0, 0, 0, 1]})
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    ic_df = logomaker.transform_matrix(counts, from_type='counts', to_type='information', background=[0.25] * 4)
    fig, ax = plt.subplots(figsize=(6, 2))
    logo = logomaker.Logo(ic_df, color_scheme='classic', shade_below=0.5, fade_below=0.5, font_name='Arial Rounded MT Bold')
    logo.style_xticks(rotation=0)
    logo.ax.set_ylabel('Bits')
    fig.savefig(os.path.join(OUT, "py_block_information_fig_as_written_BLANK.png"), dpi=120, bbox_inches="tight")
    logo.fig.savefig(os.path.join(OUT, "py_block_information.png"), dpi=120, bbox_inches="tight")
print("SKILL block: logo.fig is the pre-made fig?", logo.fig is fig, "| open figures:", len(plt.get_fignums()), "(a blank plt.subplots figure plus the real logo)")
print("warnings in SKILL information block:", sorted(set(str(x.message)[:120] for x in w)))
# independent: P=(N+1)/(n+4) (pseudocount 1 is transform_matrix's default), IC = sum p log2(p/q)
def ind_info(counts, bg, pseudo=1.0):
    C = counts.values.astype(float); P = (C + pseudo) / (C.sum(1, keepdims=True) + counts.shape[1] * pseudo)
    return P * (P * np.log2(P / np.asarray(bg))).sum(1, keepdims=True)
ok("information df column-sum == independent IC with pseudocount=1 default", np.allclose(ic_df.sum(axis=1).values, ind_info(counts, [.25]*4).sum(axis=1)), f"lm={np.round(ic_df.sum(axis=1).values,3)} ind={np.round(ind_info(counts,[.25]*4).sum(axis=1),3)}")
plain = ic_uniform(counts.values)
ok("information df row-sum == plain IC (log2 4 - H) with NO pseudocount", np.allclose(ic_df.sum(axis=1).values, plain), f"plain IC={np.round(plain,3)}  (pos1 has 10 A: plain 2.0 vs lm {ic_df.sum(axis=1).values[0]:.3f})")
ok("letter heights sum to the row IC by construction", np.allclose(ic_df.values.sum(axis=1), ind_info(counts,[.25]*4).sum(axis=1)))
ok("SKILL block draws the logo on the fig it created (ax=ax passed)", logo.fig is fig, "Logo(ic_df, ...) has no ax=ax so figsize=(6,2) is ignored and plt.subplots leaves an empty axes")
ok("dominant letter per row correct (A,C,A,A)", list(ic_df.idxmax(axis=1)) == ["A","C","A","A"], str(list(ic_df.idxmax(axis=1))))
ok("all-conserved row reads 2 bits (SKILL: 'fully conserved = 2 bits')", abs(ic_df.sum(axis=1).values[0]-2) < 0.01, f"got {ic_df.sum(axis=1).values[0]:.3f}")

# ---------- SKILL block: weight matrix ----------
genome_composition = [0.29, 0.21, 0.21, 0.29]   # SKILL leaves genome_composition undefined
weight_df = logomaker.transform_matrix(counts, from_type='counts', to_type='weight', background=genome_composition)
fig, ax = plt.subplots(figsize=(6, 2))
logo = logomaker.Logo(weight_df, color_scheme='classic', flip_below=True)
logo.fig.savefig(os.path.join(OUT, "py_block_weight.png"), dpi=120, bbox_inches="tight")
Pc = (counts.values + 1) / (counts.values.sum(1, keepdims=True) + 4)
ok("weight = log2(P/Q) with pseudocount 1 and the genome background", np.allclose(weight_df.values, np.log2(Pc / np.array(genome_composition))))
ok("weight df has negative entries (depletion) and flip_below draws them below 0", (weight_df.values < 0).any())

# ---------- planted data at n = 5, 20, 200, 2000 ----------
planted = ["A","C",None,None,"T","G",None,"A","C",None]
for n in (5, 20, 200, 2000):
    seqs = open(os.path.join(DATA, f"dna_n{n}.txt"), encoding="utf-8").read().split()
    cdf = counts_df(seqs)
    info = logomaker.transform_matrix(cdf, from_type='counts', to_type='information', background=[0.25]*4, pseudocount=0)
    row = info.sum(axis=1).values
    uni = ic_uniform(cdf.values); corr = ic_uniform(cdf.values, small=True)
    ok(f"n={n} pseudocount=0: row IC == independent uncorrected IC", np.allclose(row, uni, atol=1e-9))
    same_as_corr = np.allclose(row, np.maximum(corr,0), atol=1e-9)
    ok(f"n={n} Logomaker applies Schneider small-sample correction (SKILL/README implies)", same_as_corr, f"max |lm - corrected| = {np.abs(row-np.maximum(corr,0)).max():.3f}")
    ic1 = logomaker.transform_matrix(cdf, from_type='counts', to_type='information', background=[0.25]*4).sum(axis=1).values
    print(f"   n={n:<5d} IC lm(pseudo=1) {np.round(ic1,3)}\n            IC lm(pseudo=0) {np.round(row,3)}\n            IC Schneider    {np.round(corr,3)}")
    dom = list(info.idxmax(axis=1))
    am = [A[i] for i in cdf.values.argmax(1)]
    ok(f"n={n} dominant letter == sample argmax", dom == am, "".join(dom))
    if n >= 20:
        ok(f"n={n} dominant letter == planted at 1,2,5,6,8,9", all(dom[i]==planted[i] for i in (0,1,4,5,7,8)))
    fig, ax = plt.subplots(figsize=(6, 2)); logomaker.Logo(info, color_scheme='classic', ax=ax); ax.set_ylabel("Bits"); ax.set_ylim(0,2.1)
    fig.savefig(os.path.join(OUT, f"py_dna_n{n}.png"), dpi=120, bbox_inches="tight"); plt.close(fig)

# ---------- background: uniform vs GC-rich vs human, incl. claimed direction of the bias ----------
gc_bg = [0.18, 0.32, 0.32, 0.18]; hu_bg = [0.29, 0.21, 0.21, 0.29]
s500 = open(os.path.join(DATA, "dna_gcrich_n500.txt"), encoding="utf-8").read().split(); cg = counts_df(s500)
i_uni = logomaker.transform_matrix(cg, from_type='counts', to_type='information', background=[.25]*4, pseudocount=0).sum(axis=1).values
i_gc  = logomaker.transform_matrix(cg, from_type='counts', to_type='information', background=gc_bg, pseudocount=0).sum(axis=1).values
ok("bg=GC-rich IC == independent relative entropy sum p log2(p/q)", np.allclose(i_gc, ic_bg(cg.values, gc_bg)), f"{np.round(i_gc,3)}")
ok("background argument changes heights (works, unlike ggseqlogo bg_freq)", not np.allclose(i_uni, i_gc))
print("GC-rich data (bg .18/.32/.32/.18): planted G@pos1 C@pos2 A@pos9, other columns ~ bg")
print("   uniform IC :", np.round(i_uni, 3)); print("   GC-bg IC   :", np.round(i_gc, 3))
# SKILL claim: 'a motif preferring GC in a genome where GC is rare OVERestimates information under uniform bg;
#              an A-rich motif in an AT-rich genome UNDERestimates'.  Test with GC-poor (human-like) genome.
g_at = counts_df(["G"]*100); a_at = counts_df(["A"]*100)
for name, c, bg in (("fully-G column, human bg (G=0.21)", g_at, hu_bg), ("fully-A column, human bg (A=0.29)", a_at, hu_bg)):
    u = ic_uniform(c.values)[0]; b = ic_bg(c.values, bg)[0]
    print(f"   {name}: uniform IC {u:.3f} vs bg-corrected {b:.3f}  -> uniform {'OVER' if u > b else 'UNDER'}estimates")
u_g = ic_uniform(g_at.values)[0]; b_g = ic_bg(g_at.values, hu_bg)[0]
ok("SKILL claim: GC-preferring motif in GC-poor genome -> uniform bg OVERestimates", u_g > b_g, f"uniform {u_g:.3f} < corrected {b_g:.3f}: uniform UNDERestimates (claim reversed)")
u_a = ic_uniform(a_at.values)[0]; b_a = ic_bg(a_at.values, hu_bg)[0]
ok("SKILL claim: A-rich motif in AT-rich genome -> uniform bg UNDERestimates", u_a < b_a, f"uniform {u_a:.3f} > corrected {b_a:.3f}: uniform OVERestimates (claim reversed)")

# ---------- SKILL claim: 'transpose... logomaker expects positions as rows' ----------
try:
    logomaker.Logo(counts.T); print("transposed df (letters as rows): built a Logo with", counts.T.shape, "-> ", "no error")
except Exception as e:
    print("transposed df:", type(e).__name__, str(e)[:200])
tf = counts.T; fig, ax = plt.subplots(figsize=(4,2));
try:
    logomaker.Logo(tf, ax=ax); ok("transposed matrix (letters as rows) raises an error (SKILL 'verify shape')", False, "silently draws a 4-position logo of 'characters' A,C,G,T,...; no error")
except Exception as e:
    ok("transposed matrix raises an error", True, str(e)[:80])
plt.close('all')

# ---------- RNA / protein / custom alphabet ----------
rna = open(os.path.join(DATA, "rna_n200.txt"), encoding="utf-8").read().split()
cr = counts_df(rna, list("ACGU")); ir = logomaker.transform_matrix(cr, from_type='counts', to_type='information', background=[.25]*4, pseudocount=0)
fig, ax = plt.subplots(figsize=(6,2)); logomaker.Logo(ir, color_scheme='classic', ax=ax); fig.savefig(os.path.join(OUT,"py_rna.png"), dpi=120, bbox_inches="tight"); plt.close(fig)
ok("RNA U column: 'classic' colour scheme paints U (no box, no error)", True)
ok("RNA IC == DNA IC of same data", np.allclose(ir.sum(axis=1).values, logomaker.transform_matrix(counts_df(open(os.path.join(DATA,'dna_n200.txt')).read().split()), from_type='counts', to_type='information', background=[.25]*4, pseudocount=0).sum(axis=1).values))
AA = list("ACDEFGHIKLMNPQRSTVWY")
prot = open(os.path.join(DATA, "prot_n200.txt"), encoding="utf-8").read().split(); cp = counts_df(prot, AA)
bgp = [1/20]*20
ip = logomaker.transform_matrix(cp, from_type='counts', to_type='information', background=bgp, pseudocount=0)
ok("protein IC == independent (K=20)", np.allclose(ip.sum(axis=1).values, ic_uniform(cp.values)), f"pos8 {ip.sum(axis=1).values[7]:.3f} (max log2 20 = 4.322)")
ok("protein dominant letter at position 8 is S", ip.idxmax(axis=1).iloc[7] == "S")
fig, ax = plt.subplots(figsize=(8,2.5)); logomaker.Logo(ip, color_scheme='NajafabadiEtAl2017', ax=ax); fig.savefig(os.path.join(OUT,"py_protein_Najafabadi.png"), dpi=120, bbox_inches="tight"); plt.close(fig)
fig, ax = plt.subplots(figsize=(8,2.5)); logomaker.Logo(ip, color_scheme='chemistry', ax=ax); fig.savefig(os.path.join(OUT,"py_protein_chemistry.png"), dpi=120, bbox_inches="tight"); plt.close(fig)
# protein with default nucleotide scheme 'classic'
try:
    fig, ax = plt.subplots(figsize=(8,2.5)); logomaker.Logo(ip, color_scheme='classic', ax=ax); print("protein df + color_scheme='classic': built")
except Exception as e: print("protein + classic:", type(e).__name__, str(e)[:150])
plt.close('all')
# SKILL claims 'Logomaker (matrix_type='counts')' in the decision table
try:
    logomaker.Logo(counts, matrix_type='counts'); print("Logo(matrix_type=...): accepted")
except Exception as e: print("Logo(matrix_type='counts') ->", type(e).__name__, str(e)[:120])
# CRISPR sgRNA probability route (decision table: 'probability, logomaker custom alphabet')
p_df = logomaker.transform_matrix(cp, from_type='counts', to_type='probability', pseudocount=0)
fig, ax = plt.subplots(figsize=(8,2.5)); logomaker.Logo(p_df, ax=ax); fig.savefig(os.path.join(OUT,"py_protein_probability.png"), dpi=120, bbox_inches="tight"); plt.close(fig)
ok("probability logo: every row sums to 1", np.allclose(p_df.sum(axis=1).values, 1))

# ---------- JASPAR TP53 ----------
import json
pfm = json.load(open(r"F:\OpenScience\audit-envs\data-visualization\public-data\sequence-logos\MA0106.3_TP53.json", encoding="utf-8"))["pfm"]
jc = pd.DataFrame({k: pfm[k] for k in "ACGT"}); ji = logomaker.transform_matrix(jc, from_type='counts', to_type='information', background=[.25]*4)
fig, ax = plt.subplots(figsize=(8,2)); logomaker.Logo(ji, color_scheme='classic', ax=ax); ax.set_ylabel("Bits"); fig.savefig(os.path.join(OUT,"py_jaspar_TP53.png"), dpi=120, bbox_inches="tight"); plt.close(fig)
ok("JASPAR TP53 (17,412 sites): IC ~= 2-H within pseudocount effect (<0.01)", np.allclose(ji.sum(axis=1).values, ic_uniform(jc.values), atol=0.01), f"max diff {np.abs(ji.sum(axis=1).values-ic_uniform(jc.values)).max():.4f}; consensus {''.join(ji.idxmax(axis=1))}")
ok("JASPAR consensus == argmax counts", ''.join(ji.idxmax(axis=1)) == ''.join(jc.idxmax(axis=1)))

print("\nsummary: %d/%d PASS" % (sum(1 for _, c in res if c), len(res)))
