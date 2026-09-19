"""New input (not in the fixer's brief): verify the P0 guard in batch_fasta.py actually
prevents the crash on a genuine zero-hit query, rather than merely avoiding the crash
because the replacement query (INS[GENE]) happens to return >0 hits. Uses
history_server_download() imported directly from the fixed, copied batch_fasta.py, called
with a query engineered to return Count=0 today, then walks through the same
elapsed==0-guarded block the module runs at import time.
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))
# Import the function without re-running batch_fasta.py's own module-level driver code
import importlib.util
spec = importlib.util.spec_from_file_location("batch_fasta_module", "batch_fasta.py")
# We can't use spec/exec directly since the file has top-level driver code that runs on import.
# Instead, read history_server_download() out of the source and exec it in an isolated namespace.
src_lines = open("batch_fasta.py", encoding="utf-8").read().split("def datasets_cli_genome")[0]
ns = {}
exec(src_lines, ns)
history_server_download = ns['history_server_download']

from Bio import Entrez
Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'

OUT = 'input2_zero.fasta'
if os.path.exists(OUT):
    os.remove(OUT)

# Deliberately nonsense gene symbol combo -> genuine Count=0 live (not a crafted local mock)
term = 'ZZZNOTAREALGENE9999[GENE] AND Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]'
elapsed = history_server_download('nucleotide', term, OUT)
print(f'elapsed sentinel: {elapsed!r}')

# Reproduce the exact guarded block from batch_fasta.py's module-level code
crashed = False
err = None
try:
    if elapsed == 0:
        print('  No records found -- nothing to verify')
    else:
        from Bio import SeqIO
        records = list(SeqIO.parse(OUT, 'fasta'))
        print(f'  {len(records)} records in file')
except Exception as e:
    crashed = True
    err = f'{type(e).__name__}: {e}'

print(f'crashed: {crashed}')
if err:
    print(f'error: {err}')
print(f'output file created: {os.path.exists(OUT)}')

result = {'query_count_was_zero': elapsed == 0, 'crashed': crashed, 'error': err}
with open('input2_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
