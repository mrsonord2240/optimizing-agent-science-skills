"""Shared helpers for the bio-alignment-io re-audit (fixed commit 0f10851). Every script runs with cwd = run/."""
import pathlib, re, ast, sys
HERE = pathlib.Path(__file__).parent
SKILL = HERE / 'skill'
DATA = HERE / 'data'
PUB = pathlib.Path(r'F:\OpenScience\audit-envs\alignment\public-data')
PFAM = PUB / 'msa' / 'PF00042_seed.sto'
RESULTS = []

def ok(cond, msg):
    RESULTS.append(bool(cond))
    print(('PASS ' if cond else 'FAIL ') + msg)
    return cond

def summary():
    print(f'ASSERTIONS: {sum(RESULTS)}/{len(RESULTS)} passed')

def py_blocks():
    """Return list of (heading, code) for every ```python block in SKILL.md (verbatim)."""
    txt = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    out, head, i = [], '', 0
    lines = txt.splitlines()
    while i < len(lines):
        l = lines[i]
        if l.startswith('#'):
            head = l.lstrip('# ').strip()
        if l.strip() == '```python':
            j = i + 1; buf = []
            while lines[j].strip() != '```':
                buf.append(lines[j]); j += 1
            out.append((head, '\n'.join(buf)))
            i = j
        i += 1
    return out

def block(heading_substr, nth=0):
    hits = [c for h, c in py_blocks() if heading_substr.lower() in h.lower()]
    return hits[nth]
