# Re-audit 2026-09-15, Input 5 (Stress, regression). Deep SYNTHETIC idXML (113k PSMs). Skill default path
# (Basic + greedy + applyPickedProteinFDR) vs no protein FDR vs classic non-picked count vs two-peptide rule,
# and the Skill's revised picked_group_fdr sketch (verbatim) incl. its prefix/min-decoy guards on small subsets.
import numpy as np, pandas as pd
from pyopenms import (IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList, FalseDiscoveryRate, String)

def picked_group_fdr(groups, decoy_prefix, min_decoys=10):   # SKILL.md verbatim (fork 575ab94)
    # groups: list of dicts with 'accessions' (str), 'score' (higher = better), 'is_decoy'
    n_decoy = sum(g['is_decoy'] for g in groups)
    if n_decoy == 0 or not any(a.startswith(decoy_prefix) for g in groups for a in g['accessions']):
        raise ValueError(f'no decoy groups with prefix {decoy_prefix!r}; keep decoys upstream or fix the prefix')
    if n_decoy < min_decoys:
        print(f'WARNING: only {n_decoy} decoy groups; the protein FDR estimate is not meaningful')
    by_base = {}
    for g in groups:
        base = frozenset(a.replace(decoy_prefix, '') for a in g['accessions'])
        # keep only the higher-scoring of the target/decoy pair (the 'pick')
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
    for g in reversed(picked):  # monotone q-values from the bottom up
        running_min = min(running_min, g['fdr'])
        g['qvalue'] = running_min
    return [g for g in picked if not g['is_decoy'] and g['qvalue'] <= 0.01]

def naive(groups):
    s = sorted(groups, key=lambda g: -g['score']); t = d = 0
    for g in s:
        d += g['is_decoy']; t += not g['is_decoy']; g['fdr'] = d / max(t, 1)
    m = 1.0
    for g in reversed(s):
        m = min(m, g['fdr']); g['q'] = m
    return [g for g in s if not g['is_decoy'] and g['q'] <= 0.01]

truth = pd.read_csv('../data/truth_deep.csv').set_index('accession')
present = set(truth.index[truth.present])
gt = lambda acc: any(a in present for a in acc)

def load_infer(greedy):
    pr = []; pe = PeptideIdentificationList(); IdXMLFile().load('../data/peptides_1pct_fdr_deep.idXML', pr, pe)
    inf = BasicProteinInferenceAlgorithm(); p = inf.getParameters()
    p.setValue('annotate_indistinguishable_groups', 'true'); p.setValue('greedy_group_resolution', 'true' if greedy else 'false')
    inf.setParameters(p); inf.run(pe, pr)
    pp = {}
    for i in range(pe.size()):
        h = pe.at(i).getHits()[0]
        for ev in h.getPeptideEvidences():
            pp.setdefault(ev.getProteinAccession(), set()).add(h.getSequence().toUnmodifiedString())
    return pr, pe, pp

def line(name, lst, est=None):
    f = sum(not gt(g['accessions']) for g in lst); n = len(lst)
    print(f'{name:55s} {n:5d} | true FDP {f:4d}/{n} = {f/max(1,n):6.2%}' + (f' | estimated {est:.2%}' if est is not None else ''))

pr, pe, pp = load_infer(True)
groups = []
for g in pr[0].getIndistinguishableProteins():
    acc = [a.decode() for a in g.accessions]
    groups.append({'accessions': acc, 'score': g.probability, 'is_decoy': all(a.startswith('DECOY_') for a in acc),
                   'n_pep': len(set().union(*[pp.get(a, set()) for a in acc]))})
T = [g for g in groups if not g['is_decoy']]; D = [g for g in groups if g['is_decoy']]
print(f'resolved groups: {len(groups)} (target {len(T)}, decoy {len(D)})')
line('A. no protein-level FDR', T, len(D) / len(T))
line('B. classic non-picked group count 1%', naive([dict(g) for g in groups]))
line('C. Skill picked_group_fdr sketch 1% (DECOY_)', picked_group_fdr([dict(g) for g in groups], 'DECOY_'))
FalseDiscoveryRate().applyPickedProteinFDR(pr[0], String('DECOY_'), True, True)
Sk = [{'accessions': [a.decode() for a in g.accessions]} for g in pr[0].getIndistinguishableProteins()
      if g.probability <= 0.01 and not all(a.decode().startswith('DECOY_') for a in g.accessions)]
line('D. Skill SKILL.md block (built-in applyPickedProteinFDR) 1%', Sk)
two = [g for g in groups if g['n_pep'] >= 2]
line('E. two-peptide rule + picked 1%', picked_group_fdr([dict(g) for g in two], 'DECOY_'))
lost = [g for g in picked_group_fdr([dict(g) for g in groups], 'DECOY_') if g['n_pep'] < 2 and gt(g['accessions'])]
print('   true single-peptide groups passing picked 1% that the two-peptide rule deletes:', len(lost))

prU, _, _ = load_infer(False)
gU = [{'accessions': [a.decode() for a in g.accessions], 'score': g.probability} for g in prU[0].getIndistinguishableProteins()]
for g in gU: g['is_decoy'] = all(a.startswith('DECOY_') for a in g['accessions'])
line('F. UNresolved groups (greedy off) + picked 1%', picked_group_fdr([dict(g) for g in gU], 'DECOY_'))

bases_t = {frozenset(g['accessions']) for g in T}
unp = sum(frozenset(a.replace('DECOY_', '') for a in g['accessions']) not in bases_t for g in D)
print(f'pairing on resolved groups: decoy groups {len(D)}, unpaired by exact set {unp}')

rng = np.random.default_rng(1)
for k in (10, 30):
    sub = list(rng.choice(np.array(groups, dtype=object), size=k, replace=False))
    try:
        res = picked_group_fdr([dict(g) for g in sub], 'DECOY_')
        print(f'subset {k}: decoys {sum(g["is_decoy"] for g in sub)}, passing {len(res)}')
    except ValueError as e:
        print(f'subset {k}: ValueError: {e}')
try:
    picked_group_fdr([dict(g) for g in groups], 'REV__')
except ValueError as e:
    print('wrong prefix REV__ on DECOY_ data -> ValueError:', e)
