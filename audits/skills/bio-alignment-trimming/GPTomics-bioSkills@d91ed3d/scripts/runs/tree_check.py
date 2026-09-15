"""AUDITOR CHECK (not Skill output): unrooted Robinson-Foulds distance of estimated trees to the TRUE tree.

usage: python tree_check.py TRUE.nwk EST1.treefile [EST2.treefile ...]
"""
import sys

import dendropy
from dendropy.calculate import treecompare


def main():
    tns = dendropy.TaxonNamespace()
    true = dendropy.Tree.get(path=sys.argv[1], schema="newick", taxon_namespace=tns, preserve_underscores=True)
    true.is_rooted = False
    true.encode_bipartitions()
    n_int = len(true.internal_edges(exclude_seed_edge=True))
    for p in sys.argv[2:]:
        est = dendropy.Tree.get(path=p, schema="newick", taxon_namespace=tns, preserve_underscores=True)
        est.is_rooted = False
        est.encode_bipartitions()
        rf = treecompare.symmetric_difference(true, est)
        print(f"{p}: RF = {rf} (max {2 * (len(tns) - 3)}), nRF = {rf / (2 * (len(tns) - 3)):.3f}")


if __name__ == "__main__":
    main()
