"""Shared helpers (runs inside WSL `science`, env alignment-files). Written for the 2026-09-20 re-audit of bio-reference-operations."""
import hashlib, os, subprocess, sys
W = '/mnt/openscience/audits/bio-reference-operations/run'
RESULTS = []

def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (' -- ' + str(detail)[:400] if detail != '' else ''))
    RESULTS.append((bool(ok), name)); return ok

def sh(cmd, cwd=None, env=None, timeout=600):
    e = dict(os.environ); e.update(env or {})
    p = subprocess.run(['bash', '-c', cmd], cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def parse_fasta(path):
    d = {}; name = None
    for ln in open(path).read().splitlines():
        if ln.startswith('>'): name = ln[1:].split()[0]; d[name] = []
        elif name: d[name].append(ln)
    return {k: ''.join(v) for k, v in d.items()}

def fa_records(text):
    out = []
    for ln in text.splitlines():
        if ln.startswith('>'): out.append([ln[1:], []])
        elif ln.strip(): out[-1][1].append(ln)
    return [(h, ''.join(s)) for h, s in out]

def md5(s): return hashlib.md5(s.encode()).hexdigest()
COMP = str.maketrans('ACGTNacgtn', 'TGCANtgcan')
def revcomp(s): return s.translate(COMP)[::-1]

def summary():
    ok = sum(1 for r in RESULTS if r[0])
    print('\nSUMMARY: %d/%d checks passed; FAILS=%s' % (ok, len(RESULTS), [n for k, n in RESULTS if not k]))
