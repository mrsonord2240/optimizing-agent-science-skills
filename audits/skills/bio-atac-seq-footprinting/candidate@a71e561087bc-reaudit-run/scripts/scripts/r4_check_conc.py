"""Independent (pure python) recomputation of site_concordance.sh HINT numbers: bound/unbound overlap with HINT footprints within pk60 regions."""
import sys
def rd(p): return sorted({tuple(l.split("\t")[:3]) for l in open(p) if l.strip()})
def iv(rows): return [(c,int(s),int(e)) for c,s,e in rows]
pk=iv(rd("pk60.bed")); 
def inreg(x): return any(x[0]==c and x[1]<e and x[2]>s for c,s,e in pk)
b=[x for x in iv(rd("all_bound.bed")) if inreg(x)]; u=[x for x in iv(rd("all_unbound.bed")) if inreg(x)]
h=[x for x in iv(rd("out/sample.bed")) if inreg(x)]
ov=lambda a,B: any(a[0]==c and a[1]<e and a[2]>s for c,s,e in B)
ob=sum(ov(x,h) for x in b); ou=sum(ov(x,h) for x in u); oh=sum(ov(x,b) for x in h)
print(f"bound {ob}/{len(b)}  unbound {ou}/{len(u)}  hint-on-bound {oh}/{len(h)}")
assert (ob,len(b),ou,len(u),oh,len(h))==(58,143,0,31,54,358), "mismatch"
print("MATCH script output")
