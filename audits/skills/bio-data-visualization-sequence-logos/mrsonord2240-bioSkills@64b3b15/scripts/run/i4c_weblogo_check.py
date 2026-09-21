# Input 4 (analysis half): parse WebLogo logodata written in WSL and compare with independent IC / ggseqlogo / Logomaker
import os, re, numpy as np
from common import *
WL = os.path.join(OUT, "wl")
LN2 = np.log(2)
def parse(fn):
    rows = []
    hdr = None
    for l in open(os.path.join(WL, fn), encoding="utf-8"):
        if l.startswith("#\t") and "Entropy" in l:
            hdr = l[1:].split()
        elif l[0].isdigit():
            rows.append(l.split())
    cols = hdr
    letters = [c for c in cols if c not in ("Entropy", "Low", "High", "Weight")]
    counts = np.array([[float(r[1 + i]) for i in range(len(letters))] for r in rows])
    ent = np.array([float(r[1 + len(letters)]) for r in rows])   # nats
    return letters, counts, ent / LN2                          # bits
res = []
def ok(name, cond, note=""):
    res.append(bool(cond)); print(f"ASSERT {name:<84s} {'PASS' if cond else 'FAIL'} {note}")

A = list("ACGT")
for n in (5, 20, 200, 2000):
    tag = f"n{n}"
    l, c, wl_def = parse(f"{tag}.equi.logodata")
    _, _, wl_w0 = parse(f"{tag}.equi.w0.logodata")
    uni = ic_uniform(c); sch = ic_uniform(c, small=True)
    ok(f"n={n} weblogo --weight 0 --composition equiprobable == independent IC (no correction)", np.allclose(wl_w0, uni, atol=1e-3), f"max|d|={np.abs(wl_w0-uni).max():.4f}")
    ok(f"n={n} weblogo DEFAULT == Schneider e_n-corrected IC (as ggseqlogo)", np.allclose(wl_def, np.maximum(sch, 0), atol=1e-2), f"max|d|={np.abs(wl_def-np.maximum(sch,0)).max():.3f}")
    print(f"   n={n:<5d} weblogo default {np.round(wl_def,3)}\n            weblogo weight0 {np.round(wl_w0,3)}\n            Schneider/ggseq {np.round(np.maximum(sch,0),3)}")

# background handling. WebLogo uses the composition only as the Dirichlet prior (weight*composition): it acts under the default weight,
# and is silently ignored with --weight 0 (heights == uniform-background IC).
_, c200, _ = parse("n200.equi.w0.logodata")
hb = [0.29546, 0.20454, 0.20454, 0.29546]
_, _, wl_h = parse("n200.human.logodata"); _, _, wl_h0 = parse("n200.human.w0.logodata")
ok("weblogo --composition 'H. sapiens' (default weight) ~= relative entropy vs human bg (n=200, tol 0.12)", np.abs(wl_h-ic_bg(c200, hb)).max() < 0.12, f"max|d|={np.abs(wl_h-ic_bg(c200,hb)).max():.3f}")
_, cg, gd = parse("gc500.dict.logodata"); _, _, ge = parse("gc500.equi.logodata")
ind = ic_bg(cg, [.18,.32,.32,.18])
ok("weblogo explicit GC-rich composition dict (default weight) ~= relative entropy (n=500, tol 0.06)", np.abs(gd-ind).max() < 0.06, f"pos1/2/9 wl={np.round(gd[[0,1,8]],3)} ind={np.round(ind[[0,1,8]],3)}")
ok("weblogo composition changes heights vs equiprobable (works, unlike ggseqlogo bg_freq)", not np.allclose(gd, ge, atol=0.05), f"pos9 A: equi {ge[8]:.3f} vs GC-rich {gd[8]:.3f}")
ok("weblogo: composition with --weight 0 is silently ignored (heights == uniform IC)", np.allclose(wl_h0, ic_uniform(c200), atol=1e-3), "footnote: SKILL never combines them")

# protein
lp, cp, p_eq = parse("prot200.equi.w0.logodata"); _, _, p_auto = parse("prot200.auto.w0.logodata")
K = len(lp)
ok("protein equiprobable weight0 == independent log2(20)-H", np.allclose(p_eq, ic_uniform(cp), atol=1e-3), f"pos8 {p_eq[7]:.3f}")
print("   protein 'auto' composition (typical proteome bg) pos8 IC:", round(float(p_auto[7]), 3), "vs equiprobable", round(float(p_eq[7]), 3), " -> auto is NOT uniform for proteins")
ok("weblogo dominant protein letter at pos 8 is S", lp[int(np.argmax(cp[7]))] == "S")

# RNA
lr, cr, r_ic = parse("rna200.logodata"); ld, cd, d_ic = parse("n200.equi.logodata")
print("RNA logodata letters:", lr, "| RNA fed with --sequence-type dna (U not in alphabet):", open(os.path.join(WL,'rna_as_dna.logodata'),encoding='utf-8').read().split('#\t')[-1][:60].strip().replace('\n',' '))
ok("RNA IC == DNA IC of same data (default weight)", np.allclose(r_ic, d_ic, atol=1e-6))
lad, cad, ic_ad = parse("rna_as_dna.logodata")
print("   RNA fed as dna: letters counted", lad, "counts pos1", cad[0], "(U silently dropped -> heights on partial data)")
ok("RNA fed to --sequence-type dna does not silently drop U", cad[3].sum() == 200, f"position 4 counted {int(cad[3].sum())} of 200 sequences; IC {ic_ad[3]:.3f} vs {r_ic[3]:.3f} bits with rna alphabet")

print("\nsummary: %d/%d PASS" % (sum(res), len(res)))
