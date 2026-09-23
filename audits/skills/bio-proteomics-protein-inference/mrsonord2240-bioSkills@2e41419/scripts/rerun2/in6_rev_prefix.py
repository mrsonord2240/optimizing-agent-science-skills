# Re-audit 2026-09-15, Input 6 (NEW, Edge). "FragPipe-built database: decoys are 'rev_'." SYNTHETIC std idXML with
# DECOY_ renamed to rev_ (accessions in protein hits and peptide evidences). The Skill says the prefix is tool-specific
# and must be passed explicitly, so the agent changes String('DECOY_') -> String('rev_') and the startswith check.
# Also records what the SKILL.md block does if the agent forgets (DECOY_ left in).
import pandas as pd
from pyopenms import (IdXMLFile, BasicProteinInferenceAlgorithm, PeptideIdentificationList, FalseDiscoveryRate, String)

# text substitution of the accession prefix (pe.at(i) returns copies, so in-memory edits do not persist)
txt = open('peptides_1pct_fdr.idXML', encoding='utf-8').read()
print('DECOY_ occurrences replaced:', txt.count('DECOY_'))
open('rev_prefix.idXML', 'w', encoding='utf-8').write(txt.replace('DECOY_', 'rev_'))

truth = pd.read_csv('../data/truth_std.csv').set_index('accession')
present = set(truth.index[truth.present])

def skill_block(path, prefix):
    protein_ids = []
    peptide_ids = PeptideIdentificationList()
    IdXMLFile().load(path, protein_ids, peptide_ids)
    inference = BasicProteinInferenceAlgorithm()
    params = inference.getParameters()
    params.setValue('annotate_indistinguishable_groups', 'true')
    params.setValue('greedy_group_resolution', 'true')
    inference.setParameters(params)
    inference.run(peptide_ids, protein_ids)
    FalseDiscoveryRate().applyPickedProteinFDR(protein_ids[0], String(prefix), True, True)
    out = []
    for group in protein_ids[0].getIndistinguishableProteins():
        accs = [a.decode() for a in group.accessions]
        if all(a.startswith(prefix) for a in accs) or group.probability > 0.01:
            continue
        out.append(accs)
    return out

for prefix in ('rev_', 'DECOY_'):
    try:
        res = skill_block('rev_prefix.idXML', prefix)
        dec_as_target = sum(all(a.startswith('rev_') for a in acc) for acc in res)
        fp = sum(not any(a.replace('rev_', 'DECOY_') in present or a in present for a in acc) for acc in res)
        print(f"prefix {prefix!r}: passing {len(res)}, rev_ decoy groups reported as targets {dec_as_target}, true FDP {fp}/{len(res)} = {fp/max(1,len(res)):.2%}")
    except Exception as e:
        print(f'prefix {prefix!r}: {type(e).__name__}: {e}')
