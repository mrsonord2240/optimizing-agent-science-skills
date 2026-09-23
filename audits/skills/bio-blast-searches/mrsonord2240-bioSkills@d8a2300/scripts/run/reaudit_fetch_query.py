"""Fetch a real ~95nt window of human ACTB mRNA (NM_001101) live via Entrez, to use as an
independent megablast test query (distinct gene from HBB, which both the original auditor and
the fixer used). Avoids hand-transcribed sequence errors.
"""
import time
from Bio import Entrez, SeqIO

Entrez.email = 'reaudit-tooling@optimizing-agent-science-skills.local'
Entrez.tool = 'bio-blast-searches-reaudit'

handle = Entrez.efetch(db='nucleotide', id='NM_001101.5', rettype='fasta', retmode='text')
record = SeqIO.read(handle, 'fasta')
handle.close()

# Take a 95nt coding-region window (offset chosen to land inside the CDS, away from UTR)
window = record.seq[300:395]
print(f'Fetched {record.id}, length {len(record.seq)}')
print(f'Window (300:395), {len(window)} nt:')
print(str(window))

with open('reaudit_actb_query.fasta', 'w', encoding='utf-8') as f:
    f.write(f'>ACTB_partial_{record.id}\n{window}\n')
