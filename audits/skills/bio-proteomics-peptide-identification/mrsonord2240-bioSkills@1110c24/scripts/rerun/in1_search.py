# Re-audit 2026-09-15, Input 1 (Canonical, regression). SKILL.md "Database Search with pyOpenMS" and "Annotate
# Target/Decoy and Estimate FDR" blocks VERBATIM, except the two file names ('sample.mzML',
# 'human_target_decoy.fasta') point at the SYNTHETIC files. Truth check per replicate afterwards.
import csv, sys, os

def run_skill(mzml, fasta_path):
    BLOCK1 = f'''
from pyopenms import SimpleSearchEngineAlgorithm, IdXMLFile, PeptideIdentificationList

protein_ids = []
peptide_ids = PeptideIdentificationList()   # pyOpenMS 3.5+: a plain [] raises TypeError
search = SimpleSearchEngineAlgorithm()
p = search.getParameters()
p.setValue('precursor:mass_tolerance', 10.0)
p.setValue('precursor:mass_tolerance_unit', 'ppm')
p.setValue('fragment:mass_tolerance', 0.02)         # HCD Orbitrap; default is 10 ppm
p.setValue('fragment:mass_tolerance_unit', 'Da')
p.setValue('peptide:missed_cleavages', 2)           # default is 1
p.setValue('modifications:fixed', [b'Carbamidomethyl (C)'])
p.setValue('modifications:variable', [b'Oxidation (M)'])
search.setParameters(p)
# spectra are scored against in-silico fragment ions of every candidate peptide
search.search({mzml!r}, {fasta_path!r}, protein_ids, peptide_ids)

# protein_ids FIRST in load/store -- the OpenMS argument order is fixed
IdXMLFile().store('search_results.idXML', protein_ids, peptide_ids)
'''
    BLOCK2 = f'''
from pyopenms import PeptideIndexing, FalseDiscoveryRate, IDFilter, FASTAFile

fasta = []
FASTAFile().load({fasta_path!r}, fasta)
indexer = PeptideIndexing()
params = indexer.getParameters()
params.setValue('decoy_string', 'DECOY_')      # must match the decoy prefix in the FASTA
params.setValue('decoy_string_position', 'prefix')
indexer.setParameters(params)
indexer.run(fasta, protein_ids, peptide_ids)   # sets target/decoy flags on every hit

FalseDiscoveryRate().apply(peptide_ids)         # concatenated competition -> per-PSM q-value as the new score
IDFilter().filterHitsByScore(peptide_ids, 0.01) # 0.01 = 1% FDR, the community list-level standard
IDFilter().removeDecoyHits(peptide_ids)
'''
    ns = {}
    exec(compile(BLOCK1, 'block1', 'exec'), ns)
    n_search = ns['peptide_ids'].size()
    exec(compile(BLOCK2, 'block2', 'exec'), ns)
    return ns, n_search

def score(ns, truth_path):
    truth = {int(r['scan']): r for r in csv.DictReader(open(truth_path, encoding='utf-8'))}
    tp = fp = 0; qs = []
    pe = ns['peptide_ids']
    for i in range(pe.size()):
        p = pe.at(i)
        if not p.getHits():
            continue
        scan = int(str(p.getMetaValue('spectrum_reference')).split('scan=')[-1])
        h = p.getHits()[0]; qs.append(h.getScore())
        t = truth[scan]
        ok = t['kind'] != 'noise' and h.getSequence().toUnmodifiedString().replace('I', 'L') == t['peptide'].replace('I', 'L')
        tp += ok; fp += not ok
    return tp, fp, max(qs) if qs else None

D = '../data/'
ns, n = run_skill(D + 'sample.mzML', D + 'target_decoy.fasta')
pr = ns['peptide_ids']
print('params read back:', {k: ns['search'].getParameters().getValue(k) for k in
      ['precursor:mass_tolerance', 'fragment:mass_tolerance', 'fragment:mass_tolerance_unit', 'peptide:missed_cleavages', 'modifications:fixed', 'modifications:variable']})
tp, fp, qmax = score(ns, D + 'truth.csv')
print(f'main: PSMs after search {n}; accepted {tp+fp}; correct {tp}; false {fp}; true FDP {fp/max(1,tp+fp):.4f}; max q {qmax}; score type {ns["peptide_ids"].at(0).getScoreType()}')

TP = FP = 0
for rep in ['rep11', 'rep22', 'rep33', 'rep44', 'rep55', 'rep66', 'rep77', 'rep88']:
    nsr, _ = run_skill(D + rep + '/sample.mzML', D + rep + '/target_decoy.fasta')
    a, b, _ = score(nsr, D + rep + '/truth.csv')
    TP += a; FP += b
    print(f'{rep}: accepted {a+b} false {b} FDP {b/max(1,a+b):.4f}')
print(f'pooled replicates: accepted {TP+FP}, false {FP}, FDP {FP/max(1,TP+FP):.4f}')

# Common Errors claim check: FalseDiscoveryRate on hits without target_decoy meta value
from pyopenms import IdXMLFile, PeptideIdentificationList, FalseDiscoveryRate
pr2 = []; pe2 = PeptideIdentificationList(); IdXMLFile().load('search_results.idXML', pr2, pe2)
stripped = PeptideIdentificationList()
for i in range(pe2.size()):
    p = pe2.at(i); hs = p.getHits()
    for h in hs:
        if h.metaValueExists('target_decoy'):
            h.removeMetaValue('target_decoy')
    p.setHits(hs); stripped.push_back(p)
try:
    FalseDiscoveryRate().apply(stripped)
    print('FDR on unannotated hits: no exception')
except Exception as e:
    print('FDR on unannotated hits ->', type(e).__name__, str(e)[:120])
try:
    from pyopenms import SimpleSearchEngineAlgorithm
    SimpleSearchEngineAlgorithm().search(D + 'sample.mzML', D + 'target_decoy.fasta', [], [])
except Exception as e:
    print('plain [] for peptide ids ->', type(e).__name__, str(e)[:120])
