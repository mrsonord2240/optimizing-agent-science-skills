"""Audit helpers (not part of the Skill): RF distance to the SYNTHETIC true tree, K2P distance."""
import io
import math

import dendropy
from dendropy.calculate import treecompare
from Bio import Phylo


def rf_to_true(tree_or_newick, true_path):
    """Unrooted Robinson-Foulds (symmetric difference) between a tree and the true tree file."""
    if not isinstance(tree_or_newick, str):
        buf = io.StringIO()
        Phylo.write(tree_or_newick, buf, "newick")
        tree_or_newick = buf.getvalue()
    tns = dendropy.TaxonNamespace()
    t_true = dendropy.Tree.get(path=true_path, schema="newick", taxon_namespace=tns, rooting="force-unrooted")
    t = dendropy.Tree.get(data=tree_or_newick, schema="newick", taxon_namespace=tns, rooting="force-unrooted",
                          suppress_internal_node_taxa=True)
    return treecompare.symmetric_difference(t_true, t), 2 * (len(t_true.leaf_nodes()) - 3)


PURINES = {"A", "G"}
PYRIMIDINES = {"C", "T"}


def k2p(s1, s2):
    """Kimura 2-parameter distance, ignoring sites with non-ACGT characters."""
    n = P = Q = 0
    for a, b in zip(str(s1).upper(), str(s2).upper()):
        if a in "ACGT" and b in "ACGT":
            n += 1
            if a != b:
                if {a, b} <= PURINES or {a, b} <= PYRIMIDINES:
                    P += 1
                else:
                    Q += 1
    P, Q = P / n, Q / n
    return -0.5 * math.log(1 - 2 * P - Q) - 0.25 * math.log(1 - 2 * Q)
