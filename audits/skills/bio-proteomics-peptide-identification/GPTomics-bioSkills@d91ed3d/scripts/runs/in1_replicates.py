# AUDIT: is the Input-1 FDP (13 false of 311) systematic or sampling noise? Re-generate the SYNTHETIC data with
# 8 other seeds and rerun the adapted Skill pipeline (user settings: 0.02 Da fragment, 2 missed cleavages).
import csv
import os
import subprocess
import sys
from pyopenms import (FalseDiscoveryRate, FASTAFile, IDFilter, PeptideIdentificationList, PeptideIndexing,
                      SimpleSearchEngineAlgorithm)

PY = sys.executable
BASE = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/'
tot_acc = tot_false = tot_dec = 0
for seed in [11, 22, 33, 44, 55, 66, 77, 88]:
    out = BASE + f'rep{seed}/'
    os.makedirs(out, exist_ok=True)
    subprocess.run([PY, BASE + 'make_synthetic_ms2.py'], env={**os.environ, 'SYN_SEED': str(seed), 'SYN_OUT': out},
                   check=True, capture_output=True)
    se = SimpleSearchEngineAlgorithm()
    sp = se.getParameters()
    sp.setValue('fragment:mass_tolerance', 0.02); sp.setValue('fragment:mass_tolerance_unit', 'Da')
    sp.setValue('peptide:missed_cleavages', 2); se.setParameters(sp)
    prot, pep = [], PeptideIdentificationList()
    se.search(out + 'sample.mzML', out + 'target_decoy.fasta', prot, pep)
    n_dec = sum(1 for p in pep for h in p.getHits() if h.getMetaValue('target_decoy') == 'decoy')
    fasta = []
    FASTAFile().load(out + 'target_decoy.fasta', fasta)
    ix = PeptideIndexing(); pr = ix.getParameters()
    pr.setValue('decoy_string', 'DECOY_'); pr.setValue('decoy_string_position', 'prefix'); ix.setParameters(pr)
    ix.run(fasta, prot, pep)
    FalseDiscoveryRate().apply(pep)
    IDFilter().filterHitsByScore(pep, 0.01)
    IDFilter().removeDecoyHits(pep)
    truth = {int(r['scan']): r for r in csv.DictReader(open(out + 'truth.csv', encoding='utf-8'))}
    acc = fal = 0
    for p in pep:
        if not p.getHits():
            continue
        t = truth[int(str(p.getMetaValue('spectrum_reference')).split('scan=')[-1])]
        acc += 1
        seq = p.getHits()[0].getSequence().toUnmodifiedString().replace('I', 'L')
        fal += not (t['kind'] == 'true' and seq == t['peptide'].replace('I', 'L'))
    tot_acc += acc; tot_false += fal; tot_dec += n_dec
    print(f'REP seed={seed}: decoy hits (all) {n_dec}, accepted {acc}, false {fal}, FDP {fal / acc:.4f}')
print(f'REP pooled over 8 seeds: accepted {tot_acc}, false {tot_false}, pooled FDP {tot_false / tot_acc:.4f}')
