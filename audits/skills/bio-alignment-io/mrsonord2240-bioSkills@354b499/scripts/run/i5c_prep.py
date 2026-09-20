"""Input 5c step 1 (REAL data): take the 6 clean HBB CDS (drop record 7 with internal stop) -> data/hbb6.fa with the ORIGINAL NCBI headers."""
import pathlib
from Bio import SeqIO
here = pathlib.Path(__file__).parent
recs = list(SeqIO.parse(r'F:\OpenScience\audit-envs\alignment\public-data\msa\hbb_cds_mammals.fasta', 'fasta'))[:6]
assert len(recs) == 6 and all(len(r.seq) % 3 == 0 for r in recs), [len(r.seq) for r in recs]
SeqIO.write(recs, here/'data'/'hbb6.fa', 'fasta'); print('wrote', [r.id for r in recs], [len(r.seq) for r in recs])
