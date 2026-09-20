"""Shared helpers for the audit scripts. Verbatim copies of SKILL.md functions live in skill_md_funcs.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = r'F:\OpenScience\audit-envs\alignment\public-data\msa'
PFAM_STO = os.path.join(PUB, 'PF00042_seed.sto')
PFAM_FA = os.path.join(HERE, 'data', 'pfam_PF00042_seed_from_real.fasta')  # REAL data, converted from .sto by mkdata.py
SKILL_EX = os.path.join(HERE, 'skill', 'examples')
_results = []
def check(name, cond, detail=''):
    """Record and print an explicit assertion. Never raises so the whole script reports."""
    _results.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ''))
    return bool(cond)
def summary():
    p = sum(1 for _, c, _ in _results if c)
    print(f"\nASSERTIONS: {p}/{len(_results)} passed")
    for n, c, d in _results:
        if not c: print('  FAILED:', n, d)
