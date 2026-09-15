"""Shared MCMCTree helpers for the audit (writes ctl, runs mcmctree, parses node-age tables).
All inputs are SYNTHETIC (data/make_data.py)."""
import os
import re
import shutil
import subprocess

BIN = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin"
ENV = dict(os.environ, PATH=BIN + os.pathsep + os.environ.get("PATH", ""))

CTL = """seed = {seed}
seqfile = {seqfile}
treefile = {treefile}
mcmcfile = mcmc.txt
outfile = out.txt

ndata = {ndata}
seqtype = 0
usedata = {usedata}
clock = {clock}
RootAge = {rootage}

model = 4
alpha = 0.5
ncatG = 5
cleandata = 0

BDparas = 1 1 0.1 m
kappa_gamma = 6 2
alpha_gamma = 1 1
rgene_gamma = {rgene}
sigma2_gamma = 1 10 1

print = 1
burnin = {burnin}
sampfreq = {sampfreq}
nsample = {nsample}
"""


def write_ctl(d, **kw):
    p = dict(seed=1234, ndata=1, clock=2, rootage="'<1.2'", rgene="2 8 1", burnin=20000, sampfreq=20,
             nsample=10000)
    p.update(kw)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "mcmctree.ctl"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(CTL.format(**p))


def run(d, ctl="mcmctree.ctl", timeout=1800):
    r = subprocess.run([os.path.join(BIN, "mcmctree.exe"), ctl], cwd=d, env=ENV, capture_output=True, text=True, timeout=timeout,
                       input="\n")
    with open(os.path.join(d, "stdout.txt"), "w", encoding="utf-8") as fh:
        fh.write(r.stdout + "\n--stderr--\n" + r.stderr)
    return r.returncode, r.stdout


def parse_times(d):
    """Return {node: (mean, lo, hi)} for t_n* rows of 'Posterior mean (95% Equal-tail CI) (95% HPD CI)'."""
    txt = open(os.path.join(d, "out.txt"), encoding="utf-8", errors="replace").read()
    rows = {}
    for m in re.finditer(r"^(t_n\d+)\s+([\d.]+)\s+\(\s*([\d.]+),\s*([\d.]+)\)\s+\(\s*([\d.]+),\s*([\d.]+)\)", txt,
                         re.M):
        rows[m.group(1)] = tuple(float(x) for x in m.group(2, 5, 6))  # mean, HPD lo, HPD hi
    return rows


def node_map(d):
    """Map t_nN -> sorted tip set, from the 'Species tree for FigTree' / numbered tree in out.txt."""
    txt = open(os.path.join(d, "out.txt"), encoding="utf-8", errors="replace").read()
    m = re.search(r"Species tree with node labels for FigTree\s*\n\s*(\(.*?;)", txt, re.S)
    if not m:
        m = re.search(r"\n\s*(\(\(.*?\)\s*\d+\s*;)", txt, re.S)
    s = m.group(1)
    # tokens: '(' ')' names (e.g. 1_A) node numbers after ')'
    stack, res, i = [], {}, 0
    toks = re.findall(r"\(|\)\s*\d*|[^(),;\s]+", s)
    for t in toks:
        if t == "(":
            stack.append(set())
        elif t.startswith(")"):
            members = stack.pop()
            num = t[1:].strip()
            if num:
                res["t_n" + num] = members
            if stack:
                stack[-1] |= members
        else:
            name = t.split("_", 1)[1] if "_" in t else t
            if stack:
                stack[-1].add(name)
    return {k: "".join(sorted(v)) for k, v in res.items()}


def copy(src, dst):
    shutil.copy(src, dst)
