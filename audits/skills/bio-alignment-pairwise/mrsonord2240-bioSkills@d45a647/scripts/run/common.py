import warnings; warnings.simplefilter('ignore')
from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices
DATA = r'F:\OpenScience\audit-envs\alignment\public-data\msa'
def prot(acc):
    for r in SeqIO.parse(DATA + r'\globins_uniprot.fasta', 'fasta'):
        if acc in r.id: return r
    raise KeyError(acc)
_fail = []
def check(name, cond, obs=""):
    print(("PASS  " if cond else "FAIL  ") + name + " | " + str(obs))
    if not cond: _fail.append(name)
    return bool(cond)
def summary():
    print("\nASSERTIONS FAILED:", _fail if _fail else "none")
