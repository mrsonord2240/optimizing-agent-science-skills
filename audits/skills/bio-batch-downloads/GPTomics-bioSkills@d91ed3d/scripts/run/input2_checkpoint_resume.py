"""
Input 2 (Variant A): "Download all RefSeq mRNAs for Homo sapiens/BRCA1 to a single FASTA.
Use the history server. Checkpoint progress to ckpt.json so if my SSH session drops we
resume from where we left off, not from zero."

Runs SKILL.md's own 'Production batch fetch (history server + retry + checkpoint)' code
pattern (checkpointed_batch_download), verbatim, against a real query. Deliberately
interrupts the process after 2 chunks (simulating a crashed SSH session) and re-invokes
the *same* function a second time to verify it resumes from the checkpoint rather than
re-downloading from zero, and that the final file has the exact expected record count.
"""
import json
import time
from pathlib import Path
from urllib.error import HTTPError
from Bio import Entrez, SeqIO

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'bio-batch-downloads-audit'

OUT_DIR = Path(__file__).parent / 'out2'
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / 'brca1_mrna.fasta'
CKPT_PATH = OUT_DIR / 'brca1_mrna.ckpt.json'
for p in (OUT_PATH, CKPT_PATH):
    if p.exists():
        p.unlink()


class SimulatedCrash(Exception):
    pass


def checkpointed_batch_download(db, term, out_path, ckpt_path, rettype='fasta',
                                 retmode='text', batch_size=100, max_retries=3,
                                 crash_after_chunks=None):
    """Verbatim port of SKILL.md's checkpointed_batch_download, with one added
    optional test hook (crash_after_chunks) to simulate a mid-job process kill."""
    delay = 0.1 if Entrez.api_key else 0.34
    ckpt = Path(ckpt_path)
    start = json.loads(ckpt.read_text())['start'] if ckpt.exists() else 0

    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
    s = Entrez.read(h)
    h.close()
    webenv, query_key, total = s['WebEnv'], s['QueryKey'], int(s['Count'])
    print(f'{total:,} records matched; resuming at {start:,}')

    mode = 'a' if start else 'w'
    chunks_done = 0
    with open(out_path, mode) as out:
        while start < total:
            for attempt in range(max_retries):
                try:
                    h = Entrez.efetch(db=db, rettype=rettype, retmode=retmode,
                                       retstart=start, retmax=batch_size,
                                       webenv=webenv, query_key=query_key)
                    body = h.read()
                    h.close()
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
                    s = Entrez.read(h)
                    h.close()
                    webenv, query_key = s['WebEnv'], s['QueryKey']

            start += batch_size
            ckpt.write_text(json.dumps({'start': start, 'total': total}))
            chunks_done += 1
            time.sleep(delay)
            print(f'  {min(start, total):,}/{total:,}')

            if crash_after_chunks is not None and chunks_done >= crash_after_chunks:
                raise SimulatedCrash(
                    f'Simulated SSH-drop after {chunks_done} chunks (checkpoint at start={start})')
    ckpt.unlink(missing_ok=True)


TERM = 'BRCA1[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]'

# Get expected total independently, up front.
h = Entrez.esearch(db='nucleotide', term=TERM, retmax=0)
s = Entrez.read(h)
h.close()
expected_total = int(s['Count'])
print(f'Independent ESearch check: Count={expected_total}')

print('\n=== Phase 1: run until simulated crash after 2 chunks ===')
try:
    checkpointed_batch_download('nucleotide', TERM, str(OUT_PATH), str(CKPT_PATH),
                                 batch_size=100, crash_after_chunks=2)
    print('UNEXPECTED: phase 1 completed without crashing (dataset smaller than 2 chunks?)')
except SimulatedCrash as e:
    print(f'Simulated crash raised as expected: {e}')

ckpt_state_after_crash = json.loads(CKPT_PATH.read_text())
print(f'Checkpoint after crash: {ckpt_state_after_crash}')
size_after_crash = OUT_PATH.stat().st_size
records_after_crash = sum(1 for _ in SeqIO.parse(str(OUT_PATH), 'fasta'))
print(f'File after crash: {size_after_crash} bytes, {records_after_crash} parseable FASTA records')

print('\n=== Phase 2: resume (same call, no crash hook) ===')
checkpointed_batch_download('nucleotide', TERM, str(OUT_PATH), str(CKPT_PATH), batch_size=100)

assert not CKPT_PATH.exists(), 'Checkpoint file should be deleted on successful completion'
observed = sum(1 for _ in SeqIO.parse(str(OUT_PATH), 'fasta'))
print(f'\nFinal FASTA record count: {observed}, expected (ESearch Count): {expected_total}')
assert observed == expected_total, f'MISMATCH: expected {expected_total}, got {observed}'
print('PASS: resume-from-checkpoint after simulated crash produced the full, correct record set exactly once each.')
