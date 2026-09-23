"""Build input files. REAL: derived from public-data (Pfam PF00042 seed, UniProt globins, RefSeq HBB CDS) and the Pfam
Ras seed PF00071 downloaded from the EBI InterPro public API (data/PF00071_seed.sto.gz, see data/SOURCES.txt).
SYNTHETIC: every file named syn_* (built in the in*.py scripts)."""
import os, gzip
from Bio import AlignIO, SeqIO
from common import *
# 1. Pfam globin seed -> FASTA (Biopython conversion) and ungapped FASTA for MUSCLE (raw text parse)
aln = AlignIO.read(PFAM_STO, 'stockholm')
AlignIO.write(aln, os.path.join(DATA, 'pfam_PF00042_seed.fasta'), 'fasta')
raw = {}
for line in open(PFAM_STO, encoding='utf-8'):
    if line.startswith('#') or line.startswith('//') or not line.strip(): continue
    n, s = line.split(); raw[n] = s
with open(os.path.join(DATA, 'pfam73_ungapped.fa'), 'w', newline='\n') as f:
    for n, s in raw.items():
        f.write('>' + n.replace('/', '_') + '\n' + ''.join(c for c in s if c.isalpha()) + '\n')
# 2. Ras seed: gunzip
sto = gzip.open(os.path.join(DATA, 'PF00071_seed.sto.gz'), 'rt', encoding='utf-8').read()
open(os.path.join(DATA, 'PF00071_seed.sto'), 'w', encoding='utf-8', newline='\n').write(sto)
# 3. clean HBB CDS (drop the record with an internal stop, TOOLS.md trap 23)
recs = [r for r in SeqIO.parse(HBB_CDS, 'fasta') if 'NM_001314043' not in r.id]
SeqIO.write(recs, os.path.join(DATA, 'hbb6_cds.fa'), 'fasta')
print('pfam raw seqs', len(raw), '| clean HBB CDS', len(recs), [len(r.seq) for r in recs])
open(os.path.join(DATA, 'SOURCES.txt'), 'w', newline='\n').write(
    'REAL: PF00042_seed.sto, globins_uniprot.fasta, hbb_cds_mammals.fasta, 1MBN.pdb from F:/OpenScience/audit-envs/alignment/public-data (see its README).\n'
    'REAL: PF00071_seed.sto.gz (Pfam Ras seed) downloaded 2026-09-20 from https://www.ebi.ac.uk/interpro/api/entry/pfam/PF00071/?annotation=alignment:seed (public, no auth; Pfam data is CC0).\n'
    'SYNTHETIC: every syn_* file, created by the in*.py scripts.\n')
