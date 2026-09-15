"""Auditor tree utilities (2026-09-15), used on SYNTHETIC data only.

  rf TRUE EST [EST ...]           unrooted RF distance (and normalised) of each estimate vs truth
  freq GENETREES SPECIES          frequency of the most common unrooted gene-tree topologies vs the species tree
  contract IN OUT THRESH          collapse internal branches whose support label < THRESH (stand-in for the Skill's
                                  `nw_ed ... 'i & b<=N' o`; Newick Utilities has no Windows build). Handles IQ-TREE
                                  labels 'UFBoot' or 'SH-aLRT/UFBoot' (last value used).
  splits TREE                     list non-trivial splits with their labels
"""
import collections
import sys

import dendropy


def load_many(path, tns):
    return dendropy.TreeList.get(path=path, schema="newick", taxon_namespace=tns, preserve_underscores=True,
                                 rooting="force-unrooted")


def load_one(path, tns):
    return dendropy.Tree.get(path=path, schema="newick", taxon_namespace=tns, preserve_underscores=True,
                             rooting="force-unrooted")


def split_set(tree):
    tree.encode_bipartitions()
    full = tree.taxon_namespace.all_taxa_bitmask()
    leaves = frozenset(t.label for t in (lf.taxon for lf in tree.leaf_node_iter()))
    out = set()
    for nd in tree.postorder_internal_node_iter():
        if nd is tree.seed_node:
            continue
        side = frozenset(lf.taxon.label for lf in nd.leaf_iter())
        other = leaves - side
        if len(side) > 1 and len(other) > 1:
            out.add(min(side, other, key=lambda s: sorted(s)))
    return out


def rf(true_path, est_paths):
    tns = dendropy.TaxonNamespace()
    t = load_one(true_path, tns)
    ts = split_set(t)
    for p in est_paths:
        e = load_one(p, tns)
        es = split_set(e)
        d = len(ts ^ es)
        print(f"{p}\tRF={d}\tmax={len(ts) + len(es)}\tmissing_true_splits={[''.join(sorted(x)) for x in ts - es]}")


def freq(gt_path, sp_path, top=5):
    tns = dendropy.TaxonNamespace()
    sp = split_set(load_one(sp_path, tns))
    cnt = collections.Counter(frozenset(split_set(g)) for g in load_many(gt_path, tns))
    n = sum(cnt.values())
    print(f"{n} gene trees; species-tree topology frequency {cnt[frozenset(sp)] / n:.3f}")
    for k, c in cnt.most_common(top):
        tag = "SPECIES" if k == frozenset(sp) else "other"
        print(f"  {c / n:.3f} {tag} {sorted('|'.join([''.join(sorted(s))]) for s in k)}")


def contract(inp, out, thresh):
    tns = dendropy.TaxonNamespace()
    trees = dendropy.TreeList.get(path=inp, schema="newick", taxon_namespace=tns, preserve_underscores=True)
    n_col = 0
    for tr in trees:
        for nd in list(tr.postorder_internal_node_iter()):
            if nd is tr.seed_node or nd.label is None:
                continue
            try:
                sup = float(str(nd.label).split("/")[-1])
            except ValueError:
                continue
            if sup < thresh:
                nd.edge.collapse()
                n_col += 1
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        for tr in trees:
            fh.write(tr.as_string(schema="newick", suppress_rooting=True).strip().replace("'", "") + "\n")
    print(f"collapsed {n_col} internal branches with support < {thresh} across {len(trees)} trees -> {out}")


def splits(path):
    tns = dendropy.TaxonNamespace()
    t = dendropy.Tree.get(path=path, schema="newick", taxon_namespace=tns, preserve_underscores=True)
    leaves = frozenset(lf.taxon.label for lf in t.leaf_node_iter())
    for nd in t.postorder_internal_node_iter():
        if nd is t.seed_node:
            continue
        side = frozenset(lf.taxon.label for lf in nd.leaf_iter())
        if 1 < len(side) < len(leaves) - 1:
            print(f"{','.join(sorted(side))}\tlabel={nd.label}\tlen={nd.edge.length}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "rf":
        rf(sys.argv[2], sys.argv[3:])
    elif cmd == "freq":
        freq(sys.argv[2], sys.argv[3])
    elif cmd == "contract":
        contract(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    elif cmd == "splits":
        splits(sys.argv[2])
