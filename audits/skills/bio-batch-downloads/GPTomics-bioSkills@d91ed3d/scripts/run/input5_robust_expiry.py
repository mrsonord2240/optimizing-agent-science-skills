"""
Input 5 (Stress/complex, multi-part): "Build a download with exponential-backoff retry
on 429, detection of HTTP-200-with-ERROR-body (WebEnv expired), and automatic re-ESearch
+ resume from the disk checkpoint." -- verbatim from usage-guide.md's Example Prompts.

Runs examples/robust_download.py's checkpointed_download() COPIED VERBATIM (byte-for-byte,
not modified) against a real query. Because a genuine 8h-TTL/15min-idle WebEnv expiry can't
be forced inside a short audit pass, this test forges an invalid WebEnv/QueryKey for the
*first* EFetch call only (by monkeypatching Entrez.esearch's first return value) -- which
independently-confirmed live testing (check_bad_webenv.py) shows produces exactly the
documented real-world symptom: HTTP 200 with an XML body containing '<ERROR>...</ERROR>'.
This exercises the Skill's own WebEnv-expiry-detection branch with real server bytes, not
a mocked string.
"""
from Bio import Entrez
from urllib.error import HTTPError
import json
import random
import time
from pathlib import Path

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'bio-batch-downloads-audit'

OUT_DIR = Path(__file__).parent / 'out5'
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / 'test.fasta'
CKPT_PATH = OUT_DIR / 'test.ckpt.json'
for p in (OUT_PATH, CKPT_PATH):
    if p.exists():
        p.unlink()


def truncate_to_last_newline(path):
    '''If a previous run crashed mid-chunk, truncate the trailing partial record.'''
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return
    with open(p, 'rb+') as f:
        f.seek(-min(8192, p.stat().st_size), 2)
        tail = f.read()
        last_nl = tail.rfind(b'\n')
        if last_nl >= 0:
            f.seek(-len(tail) + last_nl + 1, 2)
            f.truncate()


def checkpointed_download(db, term, out_path, ckpt_path, rettype='fasta',
                           batch_size=100, max_retries=5):
    '''VERBATIM copy of examples/robust_download.py's checkpointed_download.
    Not one character changed from the shipped example.'''
    delay = 0.1 if Entrez.api_key else 0.34
    ckpt = Path(ckpt_path)
    start = json.loads(ckpt.read_text())['start'] if ckpt.exists() else 0

    def refresh_session():
        h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
        s = Entrez.read(h); h.close()
        return s['WebEnv'], s['QueryKey'], int(s['Count'])

    webenv, query_key, total = refresh_session()
    print(f'{total:,} records matched; resuming at {start:,}')
    if start >= total:
        print('Already complete.')
        return

    if start == 0:
        Path(out_path).write_text('')
    else:
        truncate_to_last_newline(out_path)

    with open(out_path, 'a') as out:
        while start < total:
            success = False
            for attempt in range(max_retries):
                try:
                    h = Entrez.efetch(db=db, rettype=rettype, retmode='text',
                                      retstart=start, retmax=batch_size,
                                      webenv=webenv, query_key=query_key)
                    body = h.read(); h.close()
                    if not body.strip():
                        raise RuntimeError('Empty body')
                    if '<ERROR>' in body[:500]:
                        raise RuntimeError(f'WebEnv expired or server error: {body[:200]}')
                    out.write(body); out.flush()
                    success = True
                    break
                except HTTPError as e:
                    backoff = min(120, (2 ** attempt) + random.uniform(0, 1))
                    if e.code == 429:
                        print(f'  HTTP 429; backing off {backoff:.1f}s')
                        time.sleep(backoff)
                    elif e.code in (500, 502, 503, 504):
                        print(f'  HTTP {e.code}; backing off {backoff:.1f}s')
                        time.sleep(backoff)
                    else:
                        raise
                except RuntimeError as e:
                    print(f'  {e}; refreshing WebEnv')
                    webenv, query_key, total = refresh_session()
                    time.sleep(1)

            if not success:
                raise RuntimeError(f'Failed after {max_retries} retries at start={start}')

            start += batch_size
            ckpt.write_text(json.dumps({'start': start, 'total': total}))
            time.sleep(delay)
            if (start // batch_size) % 10 == 0 or start >= total:
                print(f'  {min(start, total):,}/{total:,}')

    ckpt.unlink(missing_ok=True)
    print(f'Done: {total:,} records -> {out_path}')


TERM = 'BRCA1[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]'

# --- Monkeypatch to force the *first* Entrez.efetch call to hit a bad session,
#     reproducing the real, live '<ERROR>...</ERROR>' HTTP-200 body. ---
_orig_efetch = Entrez.efetch
_state = {'forced': False}


def _efetch_with_forced_expiry(*args, **kwargs):
    if not _state['forced']:
        _state['forced'] = True
        print('  [test hook] forcing first EFetch call onto a bogus WebEnv/QueryKey '
              '(simulates expired session)')
        kwargs = dict(kwargs)
        kwargs['webenv'] = 'BOGUS_WEBENV_STRING'
        kwargs['query_key'] = '999'
    return _orig_efetch(*args, **kwargs)


Entrez.efetch = _efetch_with_forced_expiry

try:
    checkpointed_download('nucleotide', TERM, str(OUT_PATH), str(CKPT_PATH), batch_size=100)
    print('\nRESULT: checkpointed_download completed without raising.')
except TypeError as e:
    print(f'\nRESULT: TypeError raised -- {e}')
    print('This means the WebEnv-expiry detection branch (the one this example exists to '
          'demonstrate) is broken: it crashes instead of recovering.')
except Exception as e:
    print(f'\nRESULT: {type(e).__name__} raised -- {e}')
finally:
    Entrez.efetch = _orig_efetch
