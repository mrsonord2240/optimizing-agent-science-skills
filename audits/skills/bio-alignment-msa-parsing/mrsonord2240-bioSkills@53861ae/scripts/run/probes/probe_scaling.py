"""Probe: run time of the SKILL.md helpers vs alignment length (normalize_alignment -> select_columns does ''.join(str(record.seq)[i] for i in keep),
i.e. str(record.seq) is re-materialised for every kept column). Compared with the pre-fix (first audit) helper, archived copy."""
import sys, os, time, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from collections import Counter
from common import *
import skillns
ns, _ = skillns.load()
rng = np.random.default_rng(0)
def make(n, L):
    return MultipleSeqAlignment([SeqRecord(Seq(''.join(rng.choice(list('ACGT-'), L, p=[.3, .3, .2, .1, .1]))), id=f's{i}') for i in range(n)])
def prefix_gaps_per_column(alignment):     # the pre-fix SKILL.md snippet (first audit report): count('-') per column, no normalisation
    return [alignment[:, i].count('-') for i in range(alignment.get_alignment_length())]
print(f"{'n x L':>14} {'normalize_alignment':>20} {'gaps_per_column (fixed)':>24} {'gaps_per_column (pre-fix)':>26} {'find_conserved':>16}")
for n, L in [(10, 5000), (10, 20000), (10, 50000), (10, 100000)]:
    a = make(n, L)
    t0 = time.time(); ns['normalize_alignment'](a); t1 = time.time() - t0
    t0 = time.time(); ns['gaps_per_column'](a); t2 = time.time() - t0
    t0 = time.time(); prefix_gaps_per_column(a); t3 = time.time() - t0
    t0 = time.time(); ns['find_conserved_positions'](a, 0.8); t4 = time.time() - t0
    print(f'{n:>5} x {L:<7} {t1:>19.2f}s {t2:>23.2f}s {t3:>25.2f}s {t4:>15.2f}s', flush=True)
