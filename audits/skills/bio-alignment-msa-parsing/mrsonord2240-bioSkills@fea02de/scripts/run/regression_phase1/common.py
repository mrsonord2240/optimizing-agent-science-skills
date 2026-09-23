"""Shared helpers for the re-audit scripts (bio-alignment-msa-parsing @ 53861ae).

Every check is an explicit assertion on CONTENT; results are printed as [PASS]/[FAIL] and never raise.
Skill code under test is either exec'd straight out of SKILL.md (skillns.py, no transcription) or run
from the COPY of the Skill in run/skill/ (never from the worktree or external/).
"""
import os, sys, warnings

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
SKILL = os.path.join(HERE, 'skill')
EX = os.path.join(SKILL, 'examples')
PUB = r'F:\OpenScience\audit-envs\alignment\public-data'
PFAM_STO = os.path.join(PUB, 'msa', 'PF00042_seed.sto')          # REAL: Pfam PF00042 seed, 73 x 141
GLOBINS_FA = os.path.join(PUB, 'msa', 'globins_uniprot.fasta')     # REAL: 8 UniProt globins
HBB_CDS = os.path.join(PUB, 'msa', 'hbb_cds_mammals.fasta')        # REAL: RefSeq HBB CDS
PDB_1MBN = os.path.join(PUB, 'structures', '1MBN.pdb')             # REAL

os.makedirs(DATA, exist_ok=True)
if EX not in sys.path:
    sys.path.insert(0, EX)

_results = []


def check(name, cond, detail=''):
    _results.append((name, bool(cond), detail))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ''))
    return bool(cond)


def summary():
    p = sum(1 for _, c, _ in _results if c)
    print(f"\nASSERTIONS: {p}/{len(_results)} passed")
    for n, c, d in _results:
        if not c:
            print('  FAILED:', n, d)
    return p, len(_results)
