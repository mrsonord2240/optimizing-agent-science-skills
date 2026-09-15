# Input 5 (Stress): the fixed Skill's rooted-replicate Python bootstrap VERBATIM (outgroup name filled in), on
# SYNTHETIC barcode20.fa (B=100) and big150.fa (B=20, the Skill warns it is slow), plus the skbio hand-off timing.
import random, sys, time
sys.path.insert(0, '..')
from phylo_util import rf_to_true
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

for name, B in (('barcode20', 100), ('big150', 20)):
    aln = AlignIO.read(f'../../data/{name}.fa', 'fasta')
    for r in aln:
        r.id = r.id.strip()
    calc = DistanceCalculator('identity')
    outgroup_taxon = aln[0].id
    t0 = time.time()
    # ---- Skill block ----
    import random
    from Bio.Phylo.Consensus import bootstrap_trees, majority_consensus

    random.seed(42)
    reps = []
    for rep in bootstrap_trees(aln, B, DistanceTreeConstructor(calc, 'nj')):
        rep.root_with_outgroup({'name': outgroup_taxon})   # fixed outgroup for every replicate
        reps.append(rep)
    consensus = majority_consensus(reps, cutoff=0.5)          # clade.confidence = % of replicates
    # ---- auditor checks ----
    conf = [c.confidence for c in consensus.get_nonterminals() if c.confidence is not None]
    print('%s B=%d %.0fs RF %d/%d | confidence max %.0f min %.0f | clades>=70%%: %d | internal %d' %
          (name, B, time.time() - t0, *rf_to_true(consensus, f'../../data/{name}_true.nwk'), max(conf), min(conf),
           sum(v >= 70 for v in conf), len(consensus.get_nonterminals())))
