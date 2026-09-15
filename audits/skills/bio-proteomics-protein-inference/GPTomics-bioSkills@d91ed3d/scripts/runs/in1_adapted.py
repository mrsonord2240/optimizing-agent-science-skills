# Input 1, step 2: Skill's block with the ONE change the error forces (PeptideIdentificationList), then the
# Skill's picked_group_fdr() verbatim, then checks against SYNTHETIC ground truth.
import sys
import pandas as pd
import pyopenms
from pyopenms import IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList

protein_ids = []
peptide_ids = PeptideIdentificationList()          # ADAPTATION: the Skill used a plain list -> Exception
IdXMLFile().load('peptides_1pct_fdr.idXML', protein_ids, peptide_ids)
print('loaded runs', len(protein_ids), 'PSMs', peptide_ids.size(), 'protein hits', len(protein_ids[0].getHits()))

inference = BasicProteinInferenceAlgorithm()
params = inference.getParameters()
params.setValue('annotate_indistinguishable_groups', 'true')
inference.setParameters(params)
inference.run(peptide_ids, protein_ids)

groups_raw = []
for prot_id in protein_ids:
    for group in prot_id.getIndistinguishableProteins():
        acc = [a.decode() if isinstance(a, bytes) else a for a in group.accessions]
        groups_raw.append((acc, group.probability))
print('indistinguishable groups:', len(groups_raw))
print('first 5 as the Skill prints them:')
for acc, p in groups_raw[:5]:
    print('  ', acc[0], p, acc)

# --- Skill's picked_group_fdr, VERBATIM from SKILL.md ---
def picked_group_fdr(groups, decoy_prefix='DECOY_'):
    # groups: list of dicts with 'accessions', 'score', 'is_decoy'
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

groups = [{'accessions': acc, 'score': p, 'is_decoy': all(a.startswith('DECOY_') for a in acc)} for acc, p in groups_raw]
passing = picked_group_fdr([dict(g) for g in groups])
print(f'\ntarget groups {sum(not g["is_decoy"] for g in groups)}, decoy groups {sum(g["is_decoy"] for g in groups)}')
print('groups passing 1% picked-group FDR (Skill function):', len(passing))

# ---------------- audit checks vs SYNTHETIC truth ----------------
truth = pd.read_csv('../data/truth_std.csv').set_index('accession')
def group_true(acc):  # a group is a true discovery if ANY member is truly present
    return any(truth.loc[a, 'present'] for a in acc)
fp = [g for g in passing if not group_true(g['accessions'])]
print(f'true FDP among passing groups: {len(fp)}/{len(passing)} = {len(fp)/max(1,len(passing)):.3%}')

# (a) isoform pairs: are X-1/X-2 grouped?
iso = [g for g in groups if any(a.endswith('-1') or a.endswith('-2') for a in g['accessions']) and not g['is_decoy']]
iso_pair = [g for g in iso if len(g['accessions']) == 2]
print(f'isoform-family groups: {len(iso)}; of which 2-member (X-1+X-2 indistinguishable): {len(iso_pair)}')
print('  example:', iso_pair[0]['accessions'] if iso_pair else None, 'leading (accessions[0]) =', iso_pair[0]['accessions'][0] if iso_pair else None)
# (b) subset fragments (truly absent, peptides subset of Y): are they dropped as parsimony would?
frag = truth[(truth.family_type == 'fragment') & truth.index.str.endswith('F') & truth.observed]
frag_groups = [g for g in groups if any(a in frag.index for a in g['accessions'])]
frag_pass = [g for g in passing if any(a in frag.index for a in g['accessions'])]
print(f'subsumable fragments observed: {len(frag)}; reported as their OWN group: {sum(len(g["accessions"])==1 for g in frag_groups)}; '
      f'fragment groups passing 1%: {len(frag_pass)}')
ex = frag_groups[0]
y = ex['accessions'][0][:-1]
print('  example fragment group', ex['accessions'], 'score', round(ex['score'], 6), '| its parent', y, 'score',
      [round(g['score'], 6) for g in groups if y in g['accessions']])
# (c) paralog B truly absent but sharing 3 peptides with present A
parB = truth[(truth.family_type == 'paralog') & truth.index.str.endswith('B') & ~truth.present & truth.observed]
parB_pass = [g for g in passing if any(a in parB.index for a in g['accessions'])]
print(f'absent paralog-B proteins observed via shared peptides: {len(parB)}; passing 1% as groups: {len(parB_pass)}')
# (d) what does group.probability hold? compare to protein hit scores
hs = {h.getAccession(): h.getScore() for h in protein_ids[0].getHits()}
print('protein score type:', protein_ids[0].getScoreType(), '| higher better:', protein_ids[0].isHigherScoreBetter())
print('group.probability equals max member protein score in', sum(abs(p - max(hs[a] for a in acc)) < 1e-12 for acc, p in groups_raw), 'of', len(groups_raw), 'groups')

# (e) built-in alternative: pyOpenMS FalseDiscoveryRate.applyPickedProteinFDR on groups
fdr = pyopenms.FalseDiscoveryRate()
pid = protein_ids[0]
fdr.applyPickedProteinFDR(pid, pyopenms.String('DECOY_'), True, True)  # needs String/bytes, not str
ig = pid.getIndistinguishableProteins()
q_ok = [g for g in ig if g.probability <= 0.01 and not all((a.decode() if isinstance(a,bytes) else a).startswith('DECOY_') for a in g.accessions)]
print('pyOpenMS applyPickedProteinFDR(groups_too=True): groups with q<=0.01:', len(q_ok), '| score type now:', pid.getScoreType())

qset = [[(a.decode() if isinstance(a, bytes) else a) for a in g.accessions] for g in q_ok]
print('  true FDP (built-in picked):', sum(not group_true(a) for a in qset), '/', len(qset))

# (f) greedy_group_resolution=true (razor-style resolution of shared peptides) -- closest Basic gets to parsimony
pr2 = []; pe2 = PeptideIdentificationList(); IdXMLFile().load('peptides_1pct_fdr.idXML', pr2, pe2)
inf2 = BasicProteinInferenceAlgorithm(); p2 = inf2.getParameters()
p2.setValue('annotate_indistinguishable_groups', 'true'); p2.setValue('greedy_group_resolution', 'true'); inf2.setParameters(p2)
inf2.run(pe2, pr2)
g2 = [{'accessions': [(a.decode() if isinstance(a, bytes) else a) for a in g.accessions], 'score': g.probability} for g in pr2[0].getIndistinguishableProteins()]
for g in g2: g['is_decoy'] = all(a.startswith('DECOY_') for a in g['accessions'])
pass2 = picked_group_fdr([dict(g) for g in g2])
print(f"greedy_group_resolution=true: groups {len(g2)}, passing {len(pass2)}, true FDP {sum(not group_true(g['accessions']) for g in pass2)}/{len(pass2)}, "
      f"fragment groups passing {sum(any(a in frag.index for a in g['accessions']) for g in pass2)}")
