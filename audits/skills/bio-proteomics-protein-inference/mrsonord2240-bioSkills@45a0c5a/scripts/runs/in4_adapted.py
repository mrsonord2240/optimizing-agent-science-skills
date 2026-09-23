# Input 4 step 2: the two adaptations the errors force (class name, list type), then group FDR on the posteriors.
import time
import pandas as pd
import pyopenms
from pyopenms import IdXMLFile, PeptideIdentificationList

algo_cls = getattr(pyopenms, 'BayesianProteinInferenceAlgorithm')   # ADAPTATION 1 (EpifanyAlgorithm absent)
protein_ids = []
peptide_ids = PeptideIdentificationList()                            # ADAPTATION 2
IdXMLFile().load('peptides_with_pep.idXML', protein_ids, peptide_ids)
algo = algo_cls()
t0 = time.time()
algo.inferPosteriorProbabilities(protein_ids, peptide_ids, False)   # Skill's call, unchanged
print(f'EPIFANY ran in {time.time()-t0:.1f}s; protein score type: {protein_ids[0].getScoreType()}')
D = lambda a: a.decode() if isinstance(a, bytes) else a
ig = protein_ids[0].getIndistinguishableProteins()
print('indistinguishable groups annotated:', len(ig))
for g in list(ig)[:3]:
    print('  as Skill prints:', g.accessions[0], g.probability)

def picked_group_fdr(groups, decoy_prefix='DECOY_'):   # SKILL.md verbatim
    by_base = {}
    for g in groups:
        base = frozenset(a.replace(decoy_prefix, '') for a in g['accessions'])
        if base not in by_base or g['score'] > by_base[base]['score']:
            by_base[base] = g
    picked = sorted(by_base.values(), key=lambda g: g['score'], reverse=True)
    targets = decoys = 0
    for g in picked:
        if g['is_decoy']:
            decoys += 1
        else:
            targets += 1
        g['fdr'] = decoys / targets if targets else 1.0
    running_min = 1.0
    for g in reversed(picked):
        running_min = min(running_min, g['fdr'])
        g['qvalue'] = running_min
    return [g for g in picked if not g['is_decoy'] and g['qvalue'] <= 0.01]

truth = pd.read_csv('../data/truth_std.csv').set_index('accession')
gt = lambda acc: any(truth.loc[a, 'present'] for a in acc)
groups = [{'accessions': [D(a) for a in g.accessions], 'score': g.probability} for g in ig]
for g in groups: g['is_decoy'] = all(a.startswith('DECOY_') for a in g['accessions'])
passing = picked_group_fdr([dict(g) for g in groups])
fp = [g for g in passing if not gt(g['accessions'])]
print(f'groups {len(groups)} (decoy {sum(g["is_decoy"] for g in groups)}); passing 1% picked-group FDR: {len(passing)}; true FDP {len(fp)}/{len(passing)} = {len(fp)/len(passing):.2%}')
frag = truth[(truth.family_type == 'fragment') & truth.index.str.endswith('F') & truth.observed].index
parB = truth[(truth.family_type == 'paralog') & ~truth.present & truth.observed].index
print('  fragment groups passing:', sum(any(a in frag for a in g['accessions']) for g in passing),
      '| absent paralog groups passing:', sum(any(a in parB for a in g['accessions']) for g in passing))
# posterior of subsumable fragments vs their parents
hs = {h.getAccession(): h.getScore() for h in protein_ids[0].getHits()}
fr = [a for a in frag if a in hs][:5]
print('  fragment posteriors:', [(a, round(hs[a], 3), a[:-1], round(hs.get(a[:-1], float('nan')), 3)) for a in fr])
# EPIFANY's own group posteriors -> expected FDR (sum of 1-p), a model-based alternative
ts = sorted([g for g in groups if not g['is_decoy']], key=lambda g: -g['score'])
cum = 0; n_model = 0
for i, g in enumerate(ts, 1):
    cum += 1 - g['score']
    if cum / i <= 0.01: n_model = i
fp_m = sum(not gt(g['accessions']) for g in ts[:n_model])
print(f'model-based (posterior) group FDR 1%: {n_model} groups; true FDP {fp_m}/{n_model} = {fp_m/max(1,n_model):.2%}')
# The idXML the Skill says EPIFANY needs: PSM PEPs present? score type
print('PSM score type in input:', peptide_ids[0].getScoreType() if peptide_ids.size() else None)
