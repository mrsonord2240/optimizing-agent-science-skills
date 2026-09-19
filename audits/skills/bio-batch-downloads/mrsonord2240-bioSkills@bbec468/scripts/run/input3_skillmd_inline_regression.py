"""Brief requirement #4: independently verify SKILL.md's inline checkpointed_batch_download
has the decode guard (fixer claims lines 139-140, untouched). Extracted the function
verbatim from the worktree's SKILL.md (see inline_function_extract.py output) and confirmed
by inspection that 'if isinstance(body, bytes): body = body.decode(...)' is present right
after 'body = h.read(); h.close()'. This script goes further: runs the function live with
the same forged-WebEnv technique as input1, against the SKILL.md copy (not the examples
copy), to confirm it recovers in practice, not just by reading the text.
"""
import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'


def checkpointed_batch_download(db, term, out_path, ckpt_path, rettype='fasta',
                                 retmode='text', batch_size=500, max_retries=3):
    '''Verbatim copy of SKILL.md's inline function (lines ~127-175 in the worktree).'''
    delay = 0.1 if Entrez.api_key else 0.34
    ckpt = Path(ckpt_path)
    start = json.loads(ckpt.read_text())['start'] if ckpt.exists() else 0

    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
    s = Entrez.read(h); h.close()
    webenv, query_key, total = s['WebEnv'], s['QueryKey'], int(s['Count'])
    print(f'{total:,} records matched; resuming at {start:,}')

    mode = 'a' if start else 'w'
    with open(out_path, mode) as out:
        while start < total:
            for attempt in range(max_retries):
                try:
                    h = Entrez.efetch(db=db, rettype=rettype, retmode=retmode,
                                      retstart=start, retmax=batch_size,
                                      webenv=webenv, query_key=query_key)
                    body = h.read(); h.close()
                    if isinstance(body, bytes):
                        body = body.decode('utf-8', errors='replace')
                    if '<ERROR>' in body[:500]:
                        raise RuntimeError(f'Server error in body: {body[:200]}')
                    out.write(body)
                    break
                except HTTPError as e:
                    if e.code == 429:
                        wait = 10 * (attempt + 1)
                        print(f'  Rate-limited; sleeping {wait}s')
                        time.sleep(wait)
                    elif attempt == max_retries - 1:
                        raise
                    else:
                        time.sleep(5 * (attempt + 1))
                except RuntimeError as e:
                    print(f'  {e}; refreshing WebEnv')
                    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
                    s = Entrez.read(h); h.close()
                    webenv, query_key = s['WebEnv'], s['QueryKey']

            start += batch_size
            ckpt.write_text(json.dumps({'start': start, 'total': total}))
            time.sleep(delay)
            print(f'  {min(start, total):,}/{total:,}')
    ckpt.unlink(missing_ok=True)


OUT = 'input3_tp53.fasta'
CKPT = 'input3_tp53.ckpt.json'
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
        kwargs['query_key'] = '888888'
        print(f"  [test] forging call #{_state['calls']}: query_key -> 888888")
    return _real_efetch(*args, **kwargs)

Entrez.efetch = forging_efetch

crashed = False
err = None
try:
    checkpointed_batch_download(
        db='nucleotide',
        term='TP53[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]',
        out_path=OUT,
        ckpt_path=CKPT,
        batch_size=10,
    )
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

result = {'crashed': crashed, 'error': err, 'records': n if not crashed else None}
Path('input3_result.json').write_text(json.dumps(result, indent=2))
