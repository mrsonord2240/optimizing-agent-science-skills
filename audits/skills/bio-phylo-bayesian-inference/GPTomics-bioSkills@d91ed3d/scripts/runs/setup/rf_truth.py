"""RF distance (unrooted, unweighted) between a MrBayes .con.tre (or newick) and a SYNTHETIC true tree; lists true splits missing from the estimate."""
import sys, dendropy
from dendropy.calculate import treecompare
est_path, truth_path = sys.argv[1], sys.argv[2]
tns = dendropy.TaxonNamespace()
truth = dendropy.Tree.get(path=truth_path, schema="newick", taxon_namespace=tns, rooting="force-unrooted")
schema = "nexus" if est_path.endswith(".tre") else "newick"
est = dendropy.TreeList.get(path=est_path, schema=schema, taxon_namespace=tns, rooting="force-unrooted")[0]
truth.encode_bipartitions(); est.encode_bipartitions()
print("RF =", treecompare.symmetric_difference(truth, est))
tb = {b.split_bitmask for b in truth.bipartition_encoding if not b.is_trivial()}
eb = {b.split_bitmask for b in est.bipartition_encoding if not b.is_trivial()}
print("true splits missing from estimate:", len(tb - eb), "| estimated splits not in truth:", len(eb - tb))
