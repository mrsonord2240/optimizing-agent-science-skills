"""Prepare audit-owned clean FASTA inputs for the Phase 2 ModelTest-NG regression."""
import sys
from pathlib import Path

from Bio import AlignIO

RUN = Path(__file__).resolve().parent
DATA = RUN.parent / "data"
sys.path.insert(0, str(RUN / "skill" / "examples"))
from msa_utils import load_alignment

AlignIO.write(load_alignment(DATA / "hbb6_mafft_upper.fa"), DATA / "modeltest_nt.fasta", "fasta")
AlignIO.write(load_alignment(DATA / "globins_mafft_default.fa"), DATA / "modeltest_aa.fasta", "fasta")
assert (DATA / "modeltest_nt.fasta").exists() and (DATA / "modeltest_aa.fasta").exists()
print("prepared modeltest_nt.fasta (6 HBB CDS rows) and modeltest_aa.fasta (8 aligned globin rows)")
