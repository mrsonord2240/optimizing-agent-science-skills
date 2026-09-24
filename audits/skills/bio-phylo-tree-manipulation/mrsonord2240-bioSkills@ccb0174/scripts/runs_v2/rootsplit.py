"""Auditor helper: report the root bipartition of a rooted Bio.Phylo tree and score it against a true split."""
from Bio import Phylo


def root_split(tree):
    kids = tree.root.clades
    if len(kids) == 2:
        return frozenset(t.name for t in kids[0].get_terminals()), 'branch'
    return None, f'node with {len(kids)} children'


def score(tree, true_side):
    """true_side: set of leaf names on one side of the true root."""
    allnames = {t.name for t in tree.get_terminals()}
    true_side = frozenset(true_side) & allnames
    other = frozenset(allnames - true_side)
    s, kind = root_split(tree)
    if s is None:
        return False, kind
    ok = s in (true_side, other)
    small = min(s, frozenset(allnames - s), key=len)
    return ok, 'root branch separates ' + ','.join(sorted(small))
