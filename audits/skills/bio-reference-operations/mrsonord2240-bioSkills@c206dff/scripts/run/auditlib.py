"""Shared helpers for the bio-reference-operations audit (runs inside WSL `science`, env alignment-files)."""
import hashlib, os, subprocess, sys

W = '/mnt/openscience/audits/bio-reference-operations/run'
FAILS = []
RESULTS = []


def check(name, ok, detail=''):
    line = ('PASS ' if ok else 'FAIL ') + name + (' -- ' + str(detail)[:300] if detail != '' else '')
    print(line)
    RESULTS.append((bool(ok), name))
    if not ok:
        FAILS.append(name)
    return ok


def sh(cmd, cwd=None, env=None, timeout=300):
    """run a shell command, return (rc, stdout, stderr)"""
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(['bash', '-c', cmd], cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def parse_fasta(path):
    """Independent FASTA parser -> dict name -> sequence (case preserved), first token of header."""
    d = {}
    name = None
    for ln in open(path).read().splitlines():
        if ln.startswith('>'):
            name = ln[1:].split()[0]
            d[name] = []
        elif name:
            d[name].append(ln)
    return {k: ''.join(v) for k, v in d.items()}


COMP = str.maketrans('ACGTNacgtn', 'TGCANtgcan')


def revcomp(s):
    return s.translate(COMP)[::-1]


def fa_records(text):
    """parse FASTA text -> list of (header, seq)"""
    out = []
    h = None
    for ln in text.splitlines():
        if ln.startswith('>'):
            h = ln[1:]
            out.append([h, []])
        elif ln.strip():
            out[-1][1].append(ln)
    return [(h, ''.join(s)) for h, s in out]


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def summary():
    ok = sum(1 for r in RESULTS if r[0])
    print('\nSUMMARY: %d/%d checks passed; FAILS=%s' % (ok, len(RESULTS), FAILS))
