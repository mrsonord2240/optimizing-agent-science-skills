# Input 5 (Stress): deep SYNTHETIC run (113k PSMs @1% PSM FDR, ~10k proteins). Naive vs picked group FDR, the
# two-peptide rule, "1% PSM = 1% protein", pairing diagnostics, and small-count behaviour -- all vs ground truth.
import numpy as np, pandas as pd, pyopenms
from pyopenms import IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList
D = lambda a: a.decode() if isinstance(a, bytes) else a

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

def naive_group_fdr(groups):  # same ranking and formula, no pick (the "reused PSM formula")
    s = sorted(groups, key=lambda g: g['score'], reverse=True)
    t = d = 0
    for g in s:
        d += g['is_decoy']; t += not g['is_decoy']; g['fdr'] = d / t if t else 1.0
    m = 1.0
    for g in reversed(s):
        m = min(m, g['fdr']); g['q'] = m
    return [g for g in s if not g['is_decoy'] and g['q'] <= 0.01]

def infer(greedy):
    pr = []; pe = PeptideIdentificationList(); IdXMLFile().load('../data/peptides_1pct_fdr_deep.idXML', pr, pe)
    inf = BasicProteinInferenceAlgorithm(); p = inf.getParameters()
    p.setValue('annotate_indistinguishable_groups', 'true'); p.setValue('greedy_group_resolution', 'true' if greedy else 'false')
    inf.setParameters(p); inf.run(pe, pr)
    prot_peps = {}
    for i in range(pe.size()):
        h = pe.at(i).getHits()[0]
        for ev in h.getPeptideEvidences():
            prot_peps.setdefault(ev.getProteinAccession(), set()).add(h.getSequence().toUnmodifiedString())
    gs = []
    for g in pr[0].getIndistinguishableProteins():
        acc = [D(a) for a in g.accessions]
        peps = set().union(*[prot_peps.get(a, set()) for a in acc])
        gs.append({'accessions': acc, 'score': g.probability, 'is_decoy': all(a.startswith('DECOY_') for a in acc), 'n_pep': len(peps)})
    return gs

truth = pd.read_csv('../data/truth_deep.csv').set_index('accession')
present = set(truth.index[truth.present])
gt = lambda acc: any(a in present for a in acc)
def fdp(lst): return sum(not gt(g['accessions']) for g in lst), len(lst)
def line(name, lst, est=None):
    f, n = fdp(lst)
    ntrue = n - f
    print(f'{name:58s} reported {n:5d} | true groups {ntrue:5d} | true FDP {f:4d}/{n} = {f/max(1,n):6.2%}' + (f' | estimated {est:.2%}' if est is not None else ''))

G = infer(greedy=False)
T = [g for g in G if not g['is_decoy']]; Dg = [g for g in G if g['is_decoy']]
print(f'groups: {len(G)} (target {len(T)}, decoy {len(Dg)}); truly-present target proteins observed: {len(present & set(a for g in T for a in g["accessions"]))}')
line('A. no protein-level FDR ("1% PSM FDR is enough")', T, len(Dg) / len(T))
line('B. naive group-level target-decoy, 1%', naive_group_fdr([dict(g) for g in G]))
line('C. Skill picked_group_fdr, 1%', picked_group_fdr([dict(g) for g in G]))
two = [g for g in G if g['n_pep'] >= 2]
T2 = [g for g in two if not g['is_decoy']]; D2 = [g for g in two if g['is_decoy']]
line('D. two-peptide rule only (no protein FDR)', T2, len(D2) / len(T2))
line('E. two-peptide rule + Skill picked FDR 1%', picked_group_fdr([dict(g) for g in two]))
lost = [g for g in picked_group_fdr([dict(g) for g in G]) if g['n_pep'] < 2 and gt(g['accessions'])]
print(f'   true single-peptide groups that pass picked 1% but the two-peptide rule deletes: {len(lost)}')
one_T = [g for g in T if g['n_pep'] == 1]; one_D = [g for g in Dg if g['n_pep'] == 1]
print(f'   one-hit groups: target {len(one_T)} (truly present {sum(gt(g["accessions"]) for g in one_T)}), decoy {len(one_D)}; '
      f'multi-peptide: target {len(T2)}, decoy {len(D2)}')
Gg = infer(greedy=True)
line('F. greedy_group_resolution=true + Skill picked FDR 1%', picked_group_fdr([dict(g) for g in Gg]))
line('F2. greedy groups + NAIVE (non-picked) group FDR 1%', naive_group_fdr([dict(g) for g in Gg]))
Gg2 = [g for g in Gg if g['n_pep'] >= 2]
Tg2 = [g for g in Gg2 if not g['is_decoy']]; Dgg2 = [g for g in Gg2 if g['is_decoy']]
line('G. greedy groups + two-peptide rule only (no protein FDR)', Tg2, len(Dgg2) / len(Tg2))
line('H. greedy groups + two-peptide rule + picked FDR 1%', picked_group_fdr([dict(g) for g in Gg2]))
lostg = [g for g in picked_group_fdr([dict(g) for g in Gg]) if g['n_pep'] < 2 and gt(g['accessions'])]
print(f'   (greedy) true single-peptide groups passing picked 1% that the two-peptide rule would delete: {len(lostg)}')

# pairing diagnostics for the frozenset pick (lead 3)
bases_t = {frozenset(g['accessions']) for g in T}
paired = [g for g in Dg if frozenset(a.replace('DECOY_', '') for a in g['accessions']) in bases_t]
print(f'\npairing: decoy groups {len(Dg)}; paired to a target group with the SAME membership: {len(paired)}; '
      f'unpaired (membership differs or no target): {len(Dg) - len(paired)}')
mism = [g for g in Dg if frozenset(a.replace('DECOY_', '') for a in g['accessions']) not in bases_t
        and any(frozenset([a.replace('DECOY_', '')]) <= b for b in bases_t for a in g['accessions'][:1])]
ex = [(g['accessions'], [sorted(b) for b in bases_t if g['accessions'][0].replace('DECOY_', '') in b][:1]) for g in Dg
      if frozenset(a.replace('DECOY_', '') for a in g['accessions']) not in bases_t
      and any(g['accessions'][0].replace('DECOY_', '') in b for b in bases_t)][:3]
print('   examples decoy group -> target group containing its first member:', ex)

# small-count behaviour (Skill decision tree: "0% FDR" from zero decoys is luck)
rng = np.random.default_rng(1)
for k in (10, 30):
    sub = list(rng.choice(np.array(G, dtype=object), size=k, replace=False))
    res = picked_group_fdr([dict(g) for g in sub])
    print(f'random subset of {k} groups: decoys in subset {sum(g["is_decoy"] for g in sub)}, passing at 1%: {len(res)} (no warning emitted)')
