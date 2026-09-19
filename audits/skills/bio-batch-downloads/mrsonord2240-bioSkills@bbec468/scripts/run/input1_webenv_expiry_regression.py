"""Regression test: robust_download.py's checkpointed_download() forced onto a real
expired/invalid WebEnv-QueryKey response. Reproduces the original audit's Input 5 exactly,
against the fixer's unmodified-except-for-the-fix copy of examples/robust_download.py.

Method: monkeypatch Bio.Entrez.efetch so the FIRST call is redirected onto a forged
query_key (guaranteed invalid), producing NCBI's real "HTTP 200 with <ERROR> body"
response. Every subsequent call (including the one issued by refresh_session()'s own
recovery path) uses the real, valid session. If the decode guard is present, the code
should detect the <ERROR> body, print a "refreshing WebEnv" message, and complete the
download with the correct total record count. If the guard is missing, this crashes with
TypeError: a bytes-like object is required, not 'str'.
"""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
import robust_download as rd  # the fixed, copied example
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

OUT = 'input1_brca1.fasta'
CKPT = 'input1_brca1.ckpt.json'
for p in (OUT, CKPT):
    if os.path.exists(p):
        os.remove(p)

_real_efetch = Entrez.efetch
_state = {'calls': 0, 'forged': False}

def forging_efetch(*args, **kwargs):
    _state['calls'] += 1
    if _state['calls'] == 1 and not _state['forged']:
        _state['forged'] = True
        kwargs = dict(kwargs)
        kwargs['query_key'] = '999999'  # guaranteed-invalid key against the real webenv
        print(f"  [test] forging call #{_state['calls']}: query_key -> 999999 (webenv left real/valid)")
    return _real_efetch(*args, **kwargs)

Entrez.efetch = forging_efetch

try:
    rd.checkpointed_download(
        db='nucleotide',
        term='BRCA1[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]',
        out_path=OUT,
        ckpt_path=CKPT,
        batch_size=200,
    )
    crashed = False
    err = None
except Exception as e:
    crashed = True
    err = f'{type(e).__name__}: {e}'
finally:
    Entrez.efetch = _real_efetch

print()
print(f'crashed: {crashed}')
if err:
    print(f'error: {err}')
if not crashed:
    from Bio import SeqIO
    n = sum(1 for _ in SeqIO.parse(OUT, 'fasta'))
    print(f'records in {OUT}: {n}')
    print(f'ckpt file still present: {os.path.exists(CKPT)}')
    result = {'crashed': False, 'records': n, 'forged_calls': _state['calls']}
else:
    result = {'crashed': True, 'error': err, 'forged_calls': _state['calls']}
Path('input1_result.json').write_text(json.dumps(result, indent=2))
