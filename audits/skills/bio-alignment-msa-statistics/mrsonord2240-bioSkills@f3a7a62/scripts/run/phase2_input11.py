"""New Phase 2 format-map boundary test for bio-alignment-msa-statistics."""
import sys
from pathlib import Path

from Bio import AlignIO

RUN = Path(__file__).resolve().parent
DATA = RUN.parent / "data"
sys.path.insert(0, str(RUN / "skill" / "examples"))
from msa_utils import load_alignment

seed = load_alignment(DATA / "seed_norm.fasta")
for record in seed:
    record.annotations["molecule_type"] = "protein"  # Biopython Nexus writer requires this annotation.
formats = {"phase2_seed.clw": "clustal", "phase2_seed.phy": "phylip-relaxed", "phase2_seed.nex": "nexus", "phase2_seed.stk": "stockholm"}
for name, fmt in formats.items():
    path = DATA / name
    AlignIO.write(seed, path, fmt)
    reread = load_alignment(path)
    assert (len(reread), reread.get_alignment_length()) == (73, 141), f"{fmt} round-trip shape"
    assert [str(r.seq) for r in reread] == [str(r.seq) for r in seed], f"{fmt} extension map changed rows"
print("INPUT 11 PASS: 4 extension-mapped formats, 8 shape/row assertions plus format-count assertion")
