"""SYNTHETIC probe (auditor check, 2026-09-15): find species trees whose most frequent UNROOTED gene-tree
topology differs from the species tree (anomaly zone), by simulating gene trees under the MSC with DendroPy.
usage: python az_probe.py NREPS
"""
import collections
import random
import sys

import dendropy
from dendropy.simulate import treesim

CANDIDATES = {
    "cat5_0.05": "(((((A:1,B:1):0.05,C:1.05):0.05,D:1.1):0.05,E:1.15):3.0,O:4.15);",
    "cat4_0.03": "((((A:1,B:1):0.03,C:1.03):0.03,D:1.06):3.0,O:4.06);",
    "cat5_0.02": "(((((A:1,B:1):0.02,C:1.02):0.02,D:1.04):0.02,E:1.06):3.0,O:4.06);",
}


def unrooted_key(tree):
    tree.encode_bipartitions(suppress_unifurcations=True, is_bipartitions_mutable=True)
    labels = sorted(t.label for t in tree.taxon_namespace)
    splits = []
    for bp in tree.bipartition_encoding:
        side = [t.label for t in bp.leafset_taxa(tree.taxon_namespace)]
        if 1 < len(side) < len(labels) - 1:
            a = frozenset(side)
            b = frozenset(labels) - a
            splits.append(min(a, b, key=lambda s: sorted(s)))
    return frozenset(splits)


def main(n):
    rng = random.Random(1)
    for name, nwk in CANDIDATES.items():
        sp = dendropy.Tree.get(data=nwk, schema="newick")
        gtns = dendropy.TaxonNamespace([t.label for t in sp.taxon_namespace])
        tmap = dendropy.TaxonNamespaceMapping(domain_taxon_namespace=gtns, range_taxon_namespace=sp.taxon_namespace,
                                              mapping_fn=lambda gt: sp.taxon_namespace.get_taxon(label=gt.label))
        sp_copy = dendropy.Tree.get(data=nwk, schema="newick", taxon_namespace=gtns)
        sp_key = unrooted_key(sp_copy)
        cnt = collections.Counter()
        for _ in range(n):
            gt = treesim.contained_coalescent_tree(containing_tree=sp, gene_to_containing_taxon_map=tmap,
                                                   default_pop_size=1.0, rng=rng)
            gt.is_rooted = False
            cnt[unrooted_key(gt)] += 1
        top = cnt.most_common(3)
        print(name, "species-tree freq %.3f" % (cnt[sp_key] / n))
        for k, c in top:
            print("   %.3f %s %s" % (c / n, "SPECIES" if k == sp_key else "anomalous",
                                    sorted("".join(sorted(s)) for s in k)))


if __name__ == "__main__":
    main(int(sys.argv[1]))
