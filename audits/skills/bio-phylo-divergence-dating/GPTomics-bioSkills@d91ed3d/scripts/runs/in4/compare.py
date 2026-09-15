"""Corrected effective-prior vs posterior comparison for the BEAST2 runs (SYNTHETIC data).
1. Trace log: MRCA heights logged by the MRCAPriors -> median and 95% HPD per calibrated node.
2. MCC trees: TreeAnnotator writes height_median / height_95%_HPD inside [&...] comments; Bio.Phylo keeps
   them only as raw clade.comment strings, so they are parsed with a regex and matched by tip set,
   not by zip() order."""
import glob
import re

import numpy as np
from Bio import Phylo

TRUE = {"AB": 20.0, "GH": 45.0, "ABCDEFGH": 100.0, "CD": 35.0, "ABCD": 60.0, "EF": 15.0, "EFGH": 80.0}


def hpd(x, mass=0.95):
    x = np.sort(x)
    n = int(np.floor(mass * len(x)))
    w = x[n:] - x[: len(x) - n]
    i = int(np.argmin(w))
    return x[i], x[i + n]


def trace(prefix):
    f = sorted(glob.glob(f"{prefix}*.log"))[0]
    rows = [l.rstrip("\n").split("\t") for l in open(f) if not l.startswith("#")]
    hdr, vals = rows[0], np.array(rows[1:], dtype=float)
    vals = vals[len(vals) // 10:]  # 10% burn-in
    out = {}
    for col in hdr:
        if col.startswith("mrca.age(") or col in ("tree.height", "clockRate"):
            v = vals[:, hdr.index(col)]
            lo, hi = hpd(v)
            ess_proxy = len(v)
            out[col] = (float(np.median(v)), float(lo), float(hi))
    return f, out


print("== trace logs (10% burn-in) ==")
tp = trace("prioronly")
tw = trace("withdata")
print("files:", tp[0], tw[0])
for k in tw[1]:
    a, b = tp[1].get(k), tw[1][k]
    print(f"{k:22s} eff.prior median {a[0]:9.4f} [{a[1]:.4f}, {a[2]:.4f}]   posterior median {b[0]:9.4f} [{b[1]:.4f}, {b[2]:.4f}]")


def mcc(path):
    t = Phylo.read(path, "nexus")
    res = {}
    for c in t.get_nonterminals():
        tips = "".join(sorted(x.name for x in c.get_terminals()))
        com = c.comment or ""
        med = re.search(r"height_median=([\d.Ee+-]+)", com)
        h = re.search(r"height_95%_HPD=\{([\d.Ee+-]+),([\d.Ee+-]+)\}", com)
        res[tips] = (float(med.group(1)) if med else None, (float(h.group(1)), float(h.group(2))) if h else None,
                     c.confidence)
    return t, res


print("\n== MCC trees, parsed by tip set ==")
tp_, rp = mcc("prioronly.mcc.tree")
tw_, rw = mcc("withdata.mcc.tree")
print("prior-only MCC order:", [k for k in rp], "\nwith-data MCC order:", [k for k in rw])
for tips in TRUE:
    a = rp.get(tips)
    b = rw.get(tips)
    fa = f"{a[0]:.2f} [{a[1][0]:.2f}, {a[1][1]:.2f}]" if a and a[0] else "clade absent from prior MCC"
    fb = f"{b[0]:.2f} [{b[1][0]:.2f}, {b[1][1]:.2f}]" if b and b[0] else "clade absent from posterior MCC"
    inside = b and b[1] and b[1][0] <= TRUE[tips] <= b[1][1]
    print(f"{tips:9s} true {TRUE[tips]:6.1f}  eff.prior {fa:28s} posterior {fb:28s} bracket={'YES' if inside else 'NO'}")
print("\nzip(get_nonterminals()) pairs tip sets:",
      [("".join(sorted(x.name for x in p.get_terminals())), "".join(sorted(x.name for x in q.get_terminals())))
       for p, q in zip(tp_.get_nonterminals(), tw_.get_nonterminals())])
