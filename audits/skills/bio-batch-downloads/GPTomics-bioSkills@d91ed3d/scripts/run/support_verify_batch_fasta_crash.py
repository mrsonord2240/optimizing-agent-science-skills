"""Independent second-method verification of the batch_fasta.py 0-count crash already
flagged in TOOLS.md (not taking that note on faith -- rerunning it myself here)."""
from Bio import Entrez, SeqIO
import time
from pathlib import Path

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34
OUT_DIR = Path(__file__).parent
OUT_PATH = OUT_DIR / 'insulin_mrna.fasta'
if OUT_PATH.exists():
    OUT_PATH.unlink()


def history_server_download(db, term, out_path, batch_size=500):
    '''Verbatim copy of examples/batch_fasta.py's history_server_download.'''
    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
    s = Entrez.read(h); h.close()
    webenv, query_key, total = s['WebEnv'], s['QueryKey'], int(s['Count'])
    print(f'  history-server: {total} records')

    if total == 0:
        return 0

    t0 = time.time()
    with open(out_path, 'w') as out:
        for start in range(0, total, batch_size):
            h = Entrez.efetch(db=db, rettype='fasta', retmode='text',
                              retstart=start, retmax=batch_size,
                              webenv=webenv, query_key=query_key)
            out.write(h.read()); h.close()
            time.sleep(DELAY)
    elapsed = time.time() - t0
    return elapsed


print('=== History-server download (small query) === (exact shipped query)')
elapsed = history_server_download(
    'nucleotide',
    'Homo sapiens[ORGN] AND insulin[Gene Name] AND srcdb_refseq[PROP] AND biomol_mrna[PROP]',
    str(OUT_PATH),
)
print(f'  elapsed: {elapsed}')

print('\n=== Verify integrity === (exact shipped, unguarded code)')
try:
    records = list(SeqIO.parse(str(OUT_PATH), 'fasta'))
    print(f'  {len(records)} records in file')
except FileNotFoundError as e:
    print(f'CRASH CONFIRMED (independently re-run): {type(e).__name__}: {e}')
