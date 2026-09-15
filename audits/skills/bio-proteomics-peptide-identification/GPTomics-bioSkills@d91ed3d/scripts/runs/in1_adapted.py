# Input 1 - minimal adaptation of the Skill's pyOpenMS blocks for pyopenms 3.5.0:
#   peptide_ids = []  ->  peptide_ids = PeptideIdentificationList()
# Everything else is the Skill's code. Instrumentation (prints, truth check) is marked AUDIT.
import os
import csv
os.chdir('F:/OpenScience/audits/bio-proteomics-peptide-identification/runs')
D = '../data/'

from pyopenms import SimpleSearchEngineAlgorithm, IdXMLFile, PeptideIdentificationList  # ADAPTED import

protein_ids = []
peptide_ids = PeptideIdentificationList()        # ADAPTED (Skill: peptide_ids = [])
search = SimpleSearchEngineAlgorithm()
import sys  # AUDIT: 'user' = apply the user's stated settings (the Skill shows no parameter code for the search)
if len(sys.argv) > 1 and sys.argv[1] == 'user':
    sp = search.getParameters()
    sp.setValue('fragment:mass_tolerance', 0.02)
    sp.setValue('fragment:mass_tolerance_unit', 'Da')
    sp.setValue('peptide:missed_cleavages', 2)
    search.setParameters(sp)
print('SSE params:', {k.decode(): search.getParameters().getValue(k) for k in [b'precursor:mass_tolerance', b'fragment:mass_tolerance', b'fragment:mass_tolerance_unit', b'peptide:missed_cleavages']})
search.search(D + 'sample.mzML', D + 'target_decoy.fasta', protein_ids, peptide_ids)
IdXMLFile().store('search_results.idXML', protein_ids, peptide_ids)


def summary(tag, pids):  # AUDIT
    n_hits = sum(len(p.getHits()) for p in pids)
    td = {}
    for p in pids:
        for h in p.getHits():
            v = h.getMetaValue('target_decoy') if h.metaValueExists('target_decoy') else '<unset>'
            td[v] = td.get(v, 0) + 1
    st = pids[0].getScoreType() if len(pids) else None
    hsb = pids[0].isHigherScoreBetter() if len(pids) else None
    print(f'[{tag}] pep_ids={len(pids)} hits={n_hits} target_decoy={td} score_type={st} higher_better={hsb}')


summary('after search', peptide_ids)  # AUDIT

from pyopenms import PeptideIndexing, FalseDiscoveryRate, IDFilter, FASTAFile

fasta = []
FASTAFile().load(D + 'target_decoy.fasta', fasta)
indexer = PeptideIndexing()
params = indexer.getParameters()
params.setValue('decoy_string', 'DECOY_')
params.setValue('decoy_string_position', 'prefix')
indexer.setParameters(params)
rc = indexer.run(fasta, protein_ids, peptide_ids)
print('PeptideIndexing return code', rc)  # AUDIT
summary('after indexing', peptide_ids)  # AUDIT

FalseDiscoveryRate().apply(peptide_ids)
summary('after FDR', peptide_ids)  # AUDIT
IdXMLFile().store('after_fdr_all.idXML', protein_ids, peptide_ids)  # AUDIT: keep the unfiltered q-values
IDFilter().filterHitsByScore(peptide_ids, 0.01)
summary('after filterHitsByScore(0.01)', peptide_ids)  # AUDIT
IDFilter().removeDecoyHits(peptide_ids)
summary('after removeDecoyHits', peptide_ids)  # AUDIT
IdXMLFile().store('psms_1pct.idXML', protein_ids, peptide_ids)  # AUDIT: the deliverable

# AUDIT: compare with ground truth
truth = {int(r['scan']): r for r in csv.DictReader(open(D + 'truth.csv', encoding='utf-8'))}
tp = fp_noise = fp_wrong = 0
qs = []
for p in peptide_ids:
    if not p.getHits():
        continue
    scan = int(str(p.getMetaValue('spectrum_reference')).split('scan=')[-1])
    h = p.getHits()[0]
    qs.append(h.getScore())
    seq = h.getSequence().toUnmodifiedString()
    t = truth[scan]
    if t['kind'] == 'noise':
        fp_noise += 1
    elif seq.replace('I', 'L') == t['peptide'].replace('I', 'L'):
        tp += 1
    else:
        fp_wrong += 1
n = tp + fp_noise + fp_wrong
print(f'accepted target PSMs={n}  correct={tp}  false(noise spectra)={fp_noise}  false(wrong peptide)={fp_wrong}  '
      f'true FDP={(fp_noise + fp_wrong) / max(n, 1):.4f}  max q={max(qs) if qs else None}')
print('true spectra in file = 300; sensitivity =', round(tp / 300, 3))
