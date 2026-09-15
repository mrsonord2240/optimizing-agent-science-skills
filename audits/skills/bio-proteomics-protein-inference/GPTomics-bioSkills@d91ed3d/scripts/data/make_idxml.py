"""SYNTHETIC peptide-identification data for the bio-proteomics-protein-inference audit (2026-09-11).

NOT REAL DATA. Seeded and deterministic. Writes idXML files that look like a Comet/Percolator search filtered
at 1% PSM FDR (decoy PSMs that pass the threshold are KEPT so protein-level target-decoy is possible), with
PSM main score = Posterior Error Probability (lower is better), plus a ground-truth CSV per protein.

Proteome design (per 'family'):
  single     one protein, 6-30 unique peptides
  isoform    X-1 / X-2 share all peptides except ONE low-detectability isoform-specific peptide each;
             only X-1 is truly present, so in the observed data X-1/X-2 are usually INDISTINGUISHABLE
  paralog    A / B, each with unique peptides plus 3 shared peptides; A present, B present 50% of the time
  fragment   Y plus a fragment F whose peptides are a strict SUBSET of Y (F has no unique peptide);
             only Y is truly present (F is SUBSUMABLE)
Decoys: DECOY_<acc>, every peptide reversed except the C-terminal K/R, so shared-peptide topology is mirrored.
Spectra: true PSMs from present proteins (score ~ N(3.2, 1)); random PSMs whose top hit is a random
target-or-decoy peptide (score ~ N(0, 1)). PEP is computed from the known generating densities.

Usage: python make_idxml.py   (writes next to this file)
"""
import os
import numpy as np
import pandas as pd
import pyopenms as oms

OUT = os.path.dirname(os.path.abspath(__file__))
AA = list('ACDEFGHILMNPQSTVWY')


def make_dataset(tag, n_families, present_frac, n_random, mean_psm, seed):
    rng = np.random.default_rng(seed)
    seen = set()

    def pep(k=None):
        while True:
            k = k or int(rng.integers(7, 20))
            s = ''.join(rng.choice(AA, size=k - 1)) + rng.choice(['K', 'R'])
            if s not in seen:
                seen.add(s)
                return s

    prot_peps, truth = {}, []
    det = {}  # peptide detectability weight
    for f in range(n_families):
        kind = rng.choice(['single', 'isoform', 'paralog', 'fragment'], p=[0.70, 0.12, 0.10, 0.08])
        fam_present = rng.random() < present_frac
        base = f'P{f:05d}'
        if kind == 'single':
            ps = [pep() for _ in range(int(rng.integers(6, 31)))]
            prot_peps[base] = ps
            truth.append((base, kind, f, fam_present))
        elif kind == 'isoform':
            core = [pep() for _ in range(int(rng.integers(6, 25)))]
            s1, s2 = pep(), pep()
            prot_peps[base + '-1'] = core + [s1]
            prot_peps[base + '-2'] = core + [s2]
            det[s1] = det[s2] = 0.05  # isoform-specific peptides are rarely observed
            truth += [(base + '-1', kind, f, fam_present), (base + '-2', kind, f, False)]
        elif kind == 'paralog':
            shared = [pep() for _ in range(3)]
            a, b = base + 'A', base + 'B'
            prot_peps[a] = [pep() for _ in range(int(rng.integers(3, 15)))] + shared
            prot_peps[b] = [pep() for _ in range(int(rng.integers(3, 15)))] + shared
            truth += [(a, kind, f, fam_present), (b, kind, f, fam_present and rng.random() < 0.5)]
        else:
            full = [pep() for _ in range(int(rng.integers(10, 30)))]
            y, fr = base, base + 'F'
            prot_peps[y] = full
            prot_peps[fr] = list(rng.choice(full, size=int(rng.integers(2, 5)), replace=False))
            truth += [(y, kind, f, fam_present), (fr, kind, f, False)]
    for ps in prot_peps.values():
        for p in ps:
            det.setdefault(p, float(rng.lognormal(0, 1)))

    def rev(p):
        return p[-2::-1] + p[-1]

    decoy_peps = {'DECOY_' + a: [rev(p) for p in ps] for a, ps in prot_peps.items()}
    for ps in decoy_peps.values():
        for p in ps:
            det.setdefault(p, 1.0)
    all_prot = {**prot_peps, **decoy_peps}
    pep2prot = {}
    for a, ps in all_prot.items():
        for p in ps:
            pep2prot.setdefault(p, set()).add(a)

    truth_df = pd.DataFrame(truth, columns=['accession', 'family_type', 'family', 'present'])
    present = truth_df.loc[truth_df.present, 'accession'].tolist()

    # true PSMs
    rows = []
    for a in present:
        n = int(rng.poisson(rng.lognormal(np.log(mean_psm), 1.1)))
        ps = prot_peps[a]
        w = np.array([det[p] for p in ps])
        for p in rng.choice(ps, size=n, p=w / w.sum()):
            rows.append((p, rng.normal(3.2, 1.0), 'true'))
    n_true = len(rows)
    tpool = [p for ps in prot_peps.values() for p in ps]
    dpool = [p for ps in decoy_peps.values() for p in ps]
    for _ in range(n_random):
        p = tpool[rng.integers(len(tpool))] if rng.random() < 0.5 else dpool[rng.integers(len(dpool))]
        rows.append((p, rng.normal(0.0, 1.0), 'random'))
    psm = pd.DataFrame(rows, columns=['peptide', 'score', 'origin'])
    psm['is_decoy'] = psm.peptide.map(lambda p: all(a.startswith('DECOY_') for a in pep2prot[p]))
    # PSM-level target-decoy competition q-values
    psm = psm.sort_values('score', ascending=False).reset_index(drop=True)
    d = psm.is_decoy.cumsum()
    t = (~psm.is_decoy).cumsum()
    fdr = (d / t.clip(lower=1)).values
    psm['q'] = np.minimum.accumulate(fdr[::-1])[::-1]
    pi0 = n_random / len(psm)
    f0 = np.exp(-0.5 * psm.score ** 2)
    f1 = np.exp(-0.5 * (psm.score - 3.2) ** 2)
    psm['pep'] = pi0 * f0 / (pi0 * f0 + (1 - pi0) * f1)
    kept = psm[psm.q <= 0.01].copy()

    # write idXML
    run_id = 'SyntheticSearch_' + tag
    prot_id = oms.ProteinIdentification()
    prot_id.setIdentifier(run_id)
    prot_id.setSearchEngine('SyntheticSearch')
    prot_id.setScoreType('')
    used = sorted({a for p in kept.peptide for a in pep2prot[p]})
    hits = []
    for a in used:
        h = oms.ProteinHit()
        h.setAccession(a)
        h.setMetaValue('target_decoy', 'decoy' if a.startswith('DECOY_') else 'target')
        hits.append(h)
    prot_id.setHits(hits)
    peps = oms.PeptideIdentificationList()
    for i, r in enumerate(kept.itertuples()):
        pid = oms.PeptideIdentification()
        pid.setIdentifier(run_id)
        pid.setScoreType('Posterior Error Probability')
        pid.setHigherScoreBetter(False)
        pid.setRT(float(i))
        pid.setMZ(500.0 + (i % 1000) / 10)
        ph = oms.PeptideHit()
        ph.setSequence(oms.AASequence.fromString(r.peptide))
        ph.setScore(float(r.pep))
        ph.setCharge(2)
        ph.setMetaValue('target_decoy', 'decoy' if r.is_decoy else ('target+decoy' if any(a.startswith('DECOY_') for a in pep2prot[r.peptide]) else 'target'))
        evs = []
        for a in sorted(pep2prot[r.peptide]):
            ev = oms.PeptideEvidence()
            ev.setProteinAccession(a)
            evs.append(ev)
        ph.setPeptideEvidences(evs)
        pid.setHits([ph])
        peps.push_back(pid)
    oms.IdXMLFile().store(os.path.join(OUT, f'peptides_1pct_fdr_{tag}.idXML'), [prot_id], peps)

    truth_df = pd.concat([truth_df, pd.DataFrame({'accession': list(decoy_peps), 'family_type': 'decoy',
                                                  'family': -1, 'present': False})])
    truth_df['observed'] = truth_df.accession.isin(used)
    truth_df.to_csv(os.path.join(OUT, f'truth_{tag}.csv'), index=False)
    kept.to_csv(os.path.join(OUT, f'psms_1pct_{tag}.csv'), index=False)
    print(f'[{tag}] families={n_families} target proteins={len(prot_peps)} present={len(present)} '
          f'PSMs total={len(psm)} (true={n_true}) kept@1%={len(kept)} decoyPSMs kept={int(kept.is_decoy.sum())} '
          f'random-target PSMs kept={int(((kept.origin == "random") & ~kept.is_decoy).sum())} '
          f'proteins in idXML={len(used)}')


if __name__ == '__main__':
    make_dataset('std', n_families=1500, present_frac=0.40, n_random=12000, mean_psm=6, seed=20260911)
    make_dataset('deep', n_families=12000, present_frac=0.55, n_random=120000, mean_psm=10, seed=20260912)
