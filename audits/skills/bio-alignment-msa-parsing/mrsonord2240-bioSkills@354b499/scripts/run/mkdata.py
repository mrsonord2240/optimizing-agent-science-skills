"""Build inputs. REAL: Pfam seed -> FASTA (converted, not altered). SYNTHETIC: everything named syn_*."""
import os
from Bio import AlignIO
from common import PFAM_STO, HERE
D = os.path.join(HERE, 'data')
aln = AlignIO.read(PFAM_STO, 'stockholm')
AlignIO.write(aln, os.path.join(D, 'pfam_PF00042_seed_from_real.fasta'), 'fasta')
# SYNTHETIC small protein MSA with hand-known properties (5 seqs x 12 cols)
syn = """>species_A synthetic
MKV-LLAAGTWH
>species_B synthetic
MKVALLAAGTWH
>species_C synthetic
MKI-LLSAGTWQ
>species_D synthetic
MRV-LLAAG--H
>species_E synthetic (exact duplicate of A)
MKV-LLAAGTWH
"""
open(os.path.join(D, 'syn_small.fasta'), 'w', newline='\n').write(syn)
print(os.listdir(D))
