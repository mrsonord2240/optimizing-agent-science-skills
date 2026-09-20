#!/bin/bash
# INPUT 5 (NEW, stress / end-to-end): MAFFT alignments of REAL data with REAL ids (no renaming):
#  - 6 clean RefSeq HBB CDS (the 7th record, NM_001314043.1, has an internal stop and is excluded)
#  - 8 real UniProt globins (sp|P02185|MYG_PHYMC ...)
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
D=/mnt/openscience/audits/bio-alignment-io/run/data/e2e; mkdir -p $D; cd $D
P=/mnt/openscience/audit-envs/alignment/public-data/msa
python - <<'PY'
from Bio import SeqIO
recs = list(SeqIO.parse('/mnt/openscience/audit-envs/alignment/public-data/msa/hbb_cds_mammals.fasta', 'fasta'))[:6]
import re
for r in recs:
    r.id = re.match(r'(lcl\|[NX]M_\d+\.\d+)', r.id).group(1); r.description = ''   # 'lcl|NM_000518.5' (accession only: <= 30 chars, the Clustal name limit)
SeqIO.write(recs, 'hbb6.fa', 'fasta')
PY
mafft --quiet --auto hbb6.fa > hbb6_aln.fa </dev/null; echo "hbb6_aln records: $(grep -c '>' hbb6_aln.fa)"
mafft --quiet --auto $P/globins_uniprot.fasta > globins8_aln.fa </dev/null; echo "globins8_aln records: $(grep -c '>' globins8_aln.fa)"
