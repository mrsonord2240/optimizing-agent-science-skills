"""AUDITOR CHECK (not Skill output): score an estimated MSA against the simulated TRUE alignment.

SP  = fraction of truly homologous residue pairs recovered (sum-of-pairs recall)
TC  = fraction of true columns (with >=2 residues) reproduced exactly
PID = mean pairwise identity (PID2: identical / aligned residue pairs) of the TRUE alignment
usage: python aln_accuracy.py TRUE_ALN EST_ALN [--upper]
"""
import itertools
import sys

from Bio import SeqIO


def residue_columns(path):
    recs = {r.id: str(r.seq).upper() for r in SeqIO.parse(path, "fasta")}
    cols = {}
    for sid, s in recs.items():
        k = 0
        for j, c in enumerate(s):
            if c not in "-.":
                cols[(sid, k)] = j
                k += 1
    return recs, cols


def pairs_by_column(recs, cols):
    bycol = {}
    for (sid, k), j in cols.items():
        bycol.setdefault(j, []).append((sid, k))
    return bycol


def main():
    true_recs, true_cols = residue_columns(sys.argv[1])
    est_recs, est_cols = residue_columns(sys.argv[2])
    common = set(true_recs) & set(est_recs)
    tb = pairs_by_column(true_recs, true_cols)
    eb = pairs_by_column(est_recs, est_cols)
    true_pairs = set()
    true_colsets = []
    for j, members in tb.items():
        members = [m for m in members if m[0] in common]
        if len(members) >= 2:
            true_colsets.append(frozenset(members))
        for a, b in itertools.combinations(sorted(members), 2):
            true_pairs.add((a, b))
    est_pairs = set()
    est_colsets = set()
    for j, members in eb.items():
        members = [m for m in members if m[0] in common]
        if len(members) >= 2:
            est_colsets.add(frozenset(members))
        for a, b in itertools.combinations(sorted(members), 2):
            est_pairs.add((a, b))
    sp = len(true_pairs & est_pairs) / len(true_pairs)
    tc = sum(1 for c in true_colsets if c in est_colsets) / len(true_colsets)
    # mean PID2 on the true alignment
    ids = sorted(common)
    pids = []
    for a, b in itertools.combinations(ids, 2):
        s1, s2 = true_recs[a], true_recs[b]
        m = sum(x == y and x not in "-." for x, y in zip(s1, s2))
        d = sum(x not in "-." and y not in "-." for x, y in zip(s1, s2))
        pids.append(m / d if d else 0)
    print(f"sequences scored: {len(common)}; true columns (>=2 residues): {len(true_colsets)}")
    print(f"SP (pair recall) = {sp:.3f}   TC (exact columns) = {tc:.3f}   mean true PID2 = {sum(pids)/len(pids):.3f}")


if __name__ == "__main__":
    main()
