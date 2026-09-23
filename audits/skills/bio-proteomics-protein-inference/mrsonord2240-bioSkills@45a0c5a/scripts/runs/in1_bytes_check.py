# Input 1, step 3: feed pyOpenMS groups straight into the Skill's picked_group_fdr (no decoding), as the Skill's
# two blocks imply; and check the order of group.accessions.
from pyopenms import *
pr=[]; pe=PeptideIdentificationList(); IdXMLFile().load('peptides_1pct_fdr.idXML', pr, pe)
BasicProteinInferenceAlgorithm().run(pe, pr)
ig = pr[0].getIndistinguishableProteins()
print('all groups have accessions sorted alphabetically:', all(list(g.accessions) == sorted(g.accessions) for g in ig))
groups = [{'accessions': list(g.accessions), 'score': g.probability,
           'is_decoy': all(a.startswith(b'DECOY_') for a in g.accessions)} for g in ig]
def picked_group_fdr(groups, decoy_prefix='DECOY_'):
    by_base = {}
    for g in groups:
        base = frozenset(a.replace(decoy_prefix, '') for a in g['accessions'])
        if base not in by_base or g['score'] > by_base[base]['score']:
            by_base[base] = g
    return by_base
try:
    picked_group_fdr(groups)
except Exception as e:
    print('Skill picked_group_fdr on raw pyOpenMS accessions ->', type(e).__name__ + ':', e)
