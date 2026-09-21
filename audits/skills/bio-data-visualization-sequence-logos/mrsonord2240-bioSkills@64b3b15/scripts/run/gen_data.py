# synthetic, seeded. Planted DNA motif (10 pos), RNA version, protein 15-mer, GC-biased background set.
import numpy as np, os
from common import *
rng = np.random.default_rng(20260920)
A = list("ACGT")
# position probabilities (A,C,G,T)
P = np.array([
 [1.00,0,0,0],          # 1 fully A
 [0.02,0.94,0.02,0.02], # 2 C
 [0.25,0.25,0.25,0.25], # 3 uniform
 [0,0,0.5,0.5],         # 4 G/T half
 [0.05,0.05,0.05,0.85], # 5 T
 [0.1,0.1,0.7,0.1],     # 6 G
 [0.25,0.25,0.25,0.25], # 7 uniform
 [0.7,0.1,0.1,0.1],     # 8 A
 [0,1.0,0,0],           # 9 fully C
 [0.4,0.1,0.4,0.1],     # 10 A/G
])
def draw(n, P, alpha):
    return ["".join(rng.choice(alpha, p=P[i]) for i in range(len(P))) for _ in range(n)]
for n in (5, 20, 200, 2000):
    s = draw(n, P, A)
    open(f"{DATA}/dna_n{n}.fa","w").write("".join(f">s{i}\n{x}\n" for i,x in enumerate(s)))
    open(f"{DATA}/dna_n{n}.txt","w").write("\n".join(s)+"\n")
    open(f"{DATA}/rna_n{n}.txt","w").write("\n".join(x.replace("T","U") for x in s)+"\n")
# GC-biased set: draw uniformly-random background at GC-rich composition (0.18,0.32,0.32,0.18) then plant the motif at pos 1,2,9 only
bg = np.array([0.18,0.32,0.32,0.18])
Pg = np.tile(bg,(10,1)); Pg[0]=[0,0,1,0]; Pg[1]=[0,1,0,0]; Pg[8]=[1,0,0,0]
s = draw(500, Pg, A)
open(f"{DATA}/dna_gcrich_n500.txt","w").write("\n".join(s)+"\n")
# protein 15-mer: S at 8, K/R at 5, hydrophobic-ish at 9
AA = list("ACDEFGHIKLMNPQRSTVWY")
Pp = np.tile(np.ones(20)/20,(15,1))
Pp[7] = np.array([1.0 if a=="S" else 0 for a in AA])
def dist(d):
    v=np.array([d.get(a,0.0) for a in AA]); return v/v.sum()
Pp[4]=dist({"K":0.25,"R":0.25,**{a:0.5/18 for a in AA if a not in "KR"}})
Pp[8]=dist({"L":.25,"I":.25,"V":.25,"M":.25})
for n in (200,):
    s = draw(n, Pp, AA)
    open(f"{DATA}/prot_n{n}.txt","w").write("\n".join(s)+"\n")
print("ok", os.listdir(DATA))
