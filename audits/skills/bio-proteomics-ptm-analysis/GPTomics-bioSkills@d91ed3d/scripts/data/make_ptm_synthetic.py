"""SYNTHETIC PTM test data for the bio-proteomics-ptm-analysis audit (2026-09-11). NOT REAL DATA.

Seeded and deterministic. Formats mimic MaxQuant 2.x txt/ output:
  phospho/  evidence_phospho.txt (enriched), evidence_global.txt + proteinGroups_global.txt (paired
            unenriched proteome), 'Phospho (STY)Sites.txt' (aggregated Intensity, Intensity___1/2/3 AND
            per-experiment Intensity C1, Intensity C1___1 ... as MaxQuant writes them), FASTA, annotations,
            truth_sites.csv
  glygly/   same layout for an anti-K-GG (diGly) experiment: evidence_glygly.txt, evidence_global.txt,
            proteinGroups_global.txt, 'GlyGly (K)Sites.txt', FASTA, annotations, truth_sites.csv

Design: 8 runs C1-C4 (Control) / T1-T4 (Treatment), one enriched run and one global run per sample.
Phospho truth classes (40 proteins, one primary site each):
  protein_driven : protein log2FC +/-1.5, occupancy 0     -> observed site change is ENTIRELY protein-driven
  site_regulated : protein 0, occupancy +/-1.5            -> true regulation (up sites carry S/T-P, down R-x-x-S/T)
  masked         : protein +1.2, occupancy -1.2           -> observed ~0, true occupancy change -1.2
  null           : 0 / 0
  4 null proteins also carry a doubly-phosphorylated form (multiplicity switch: ___1 down, ___2 up in T).
  ~20% of sites have ambiguous localization (class II/III).
GlyGly: 30 proteins; protein_driven (MG132-like stabilisation), site_regulated up, null; 4 rows carry the
  GG on the peptide C-terminal K (trypsin does not cleave after K-GG -> implausible, artifact-like).
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260911)
SAMPLES = ['C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4']
IS_T = {s: s.startswith('T') for s in SAMPLES}
AA = list('ACDEFGHIKLMNPQRSTVWY')
FREQ = np.array([7.0, 1.4, 5.4, 6.8, 3.9, 7.1, 2.3, 5.5, 5.8, 9.9, 2.4, 4.0, 4.7, 3.9, 5.5, 8.3, 5.3, 6.9, 1.2, 3.1])
FREQ = FREQ / FREQ.sum()
NAMES_WITH_QUOTE = "Cytosolic 5'-nucleotidase 3A"


def digest(seq):
    peps, start = [], 0
    for i, a in enumerate(seq):
        if a in 'KR' and (i + 1 == len(seq) or seq[i + 1] != 'P'):
            peps.append((start, seq[start:i + 1]))
            start = i + 1
    if start < len(seq):
        peps.append((start, seq[start:]))
    return peps


def window(seq, pos0, half=15):
    s = ''.join(seq[i] if 0 <= i < len(seq) else '_' for i in range(pos0 - half, pos0 + half + 1))
    return s


def make_proteins(n, prefix_num):
    prots = []
    for i in range(n):
        acc = f'P{prefix_num + i:05d}'  # matches the UniProt accession regex [OPQ][0-9][A-Z0-9]{3}[0-9]
        seq = ''.join(rng.choice(AA, size=int(rng.integers(320, 520)), p=FREQ))
        prots.append({'acc': acc, 'seq': 'M' + seq[1:], 'gene': f'PTMG{prefix_num % 1000 + i:03d}',
                      'name': NAMES_WITH_QUOTE if i == 3 else f'Synthetic protein {i}'})
    return prots


def pick_site(prot, residues, motif=None, need_second=False, cterm_k=False):
    """Choose a modifiable residue whose tryptic peptide is 7-30 aa; optionally plant a motif first."""
    for _ in range(4000):
        seq = list(prot['seq'])
        cand = [i for i, a in enumerate(seq) if a in residues and 20 < i < len(seq) - 20]
        pos = int(rng.choice(cand))
        if motif == 'P+1':
            seq[pos + 1] = 'P'
        elif motif == 'R-3':
            seq[pos - 3] = 'R'
            seq[pos - 2] = 'A'
            seq[pos - 1] = 'G'
        s = ''.join(seq)
        # a K carrying GG is NOT cleaved by trypsin: protect it during digestion (except the artifact rows)
        sd = s[:pos] + 'k' + s[pos + 1:] if (residues == 'K' and not cterm_k) else s
        for st, pep in [(a, b.upper()) for a, b in digest(sd)]:
            if st <= pos < st + len(pep):
                if not (7 <= len(pep) <= 30):
                    break
                k = pos - st
                if not cterm_k and k == len(pep) - 1:
                    break  # K-GG / S at the very C-terminus not wanted (except the planted artifact rows)
                if cterm_k and k != len(pep) - 1:
                    break
                others = [j for j, a in enumerate(pep) if a in residues and j != k and (j != len(pep) - 1)]
                if need_second and not others:
                    break
                prot['seq'] = s
                return {'pos0': pos, 'start0': st, 'pep': pep, 'k': k, 'others': others}
    raise RuntimeError('no site found')


def modseq(pep, idxs, tag):
    out = ''
    for j, a in enumerate(pep):
        out += a + (f'({tag})' if j in idxs else '')
    return '_' + out + '_'


def probs_string(pep, probs):
    out = ''
    for j, a in enumerate(pep):
        out += a + (f'({probs[j]:.3g})' if j in probs else '')
    return out


EVID_COLS = ['Sequence', 'Length', 'Modifications', 'Modified sequence', 'PROBCOL', 'Missed cleavages', 'Proteins',
             'Leading proteins', 'Leading razor protein', 'Gene names', 'Protein names', 'Type', 'Raw file',
             'Experiment', 'Charge', 'm/z', 'Retention time', 'PEP', 'Score', 'Delta score', 'Intensity', 'Reverse',
             'Potential contaminant', 'id', 'Protein group IDs']


def ev_row(prot, pep, mods, mseq, probs_str, raw, exp, inten, pg_id, rev='', con=''):
    return {'Sequence': pep, 'Length': len(pep), 'Modifications': mods, 'Modified sequence': mseq,
            'PROBCOL': probs_str, 'Missed cleavages': sum(a in 'KR' for a in pep[:-1]), 'Proteins': prot['acc'],
            'Leading proteins': prot['acc'], 'Leading razor protein': prot['acc'], 'Gene names': prot['gene'],
            'Protein names': prot['name'], 'Type': 'MULTI-MSMS', 'Raw file': raw, 'Experiment': exp, 'Charge': 2,
            'm/z': round(float(rng.uniform(400, 1200)), 4), 'Retention time': round(float(rng.uniform(10, 110)), 3),
            'PEP': float(10 ** rng.uniform(-9, -3)), 'Score': round(float(rng.uniform(60, 250)), 2),
            'Delta score': round(float(rng.uniform(20, 150)), 2), 'Intensity': round(float(inten), 1),
            'Reverse': rev, 'Potential contaminant': con, 'id': 0, 'Protein group IDs': pg_id}


def observed(logi):
    """Left-censored + MCAR dropout."""
    if rng.random() < 0.04:
        return None
    if logi < 21.0 and rng.random() < 0.6:
        return None
    return 2 ** logi


def build(kind):
    d = os.path.join(OUT, kind)
    os.makedirs(d, exist_ok=True)
    if kind == 'phospho':
        n, residues, tag, modname, probcol = 40, 'STY', 'Phospho (STY)', 'Phospho (STY)', 'Phospho (STY) Probabilities'
        classes = (['protein_driven'] * 8 + ['site_regulated'] * 8 + ['masked'] * 4 + ['null'] * 20)
        prots = make_proteins(n, 60000)
    else:
        n, residues, tag, modname, probcol = 30, 'K', 'GlyGly (K)', 'GlyGly (K)', 'GlyGly (K) Probabilities'
        classes = (['protein_driven'] * 6 + ['site_regulated'] * 8 + ['null'] * 12 + ['artifact_cterm_K'] * 4)
        prots = make_proteins(n, 70000)
    truth, sites_rows, ev_ptm, ev_glob = [], [], [], []
    run_off_ptm = {s: rng.normal(0, 0.15) for s in SAMPLES}
    run_off_glob = {s: rng.normal(0, 0.15) for s in SAMPLES}
    for i, (prot, cls) in enumerate(zip(prots, classes)):
        sign = 1 if i % 2 == 0 else -1
        prot_fc, occ_fc = 0.0, 0.0
        motif = None
        if cls == 'protein_driven':
            prot_fc = 1.5 * sign if kind == 'phospho' else 1.5
        elif cls == 'site_regulated':
            occ_fc = 1.5 * sign if kind == 'phospho' else 1.5
            if kind == 'phospho':
                motif = 'P+1' if sign > 0 else 'R-3'
        elif cls == 'masked':
            prot_fc, occ_fc = 1.2, -1.2
        multi = (kind == 'phospho' and cls == 'null' and i >= 36)
        site = pick_site(prot, 'ST' if motif else residues, motif=motif, need_second=multi,
                         cterm_k=(cls == 'artifact_cterm_K'))
        # localization confidence
        ambiguous = (rng.random() < 0.2) and len(site['others']) > 0 and cls in ('null', 'protein_driven')
        if ambiguous:
            lp = float(rng.uniform(0.35, 0.74))
        else:
            lp = float(rng.uniform(0.90, 1.0)) if site['others'] else 1.0
        base_prot = rng.normal(25.5, 1.3)
        base_site = base_prot - rng.uniform(2.0, 3.5)
        pep, k = site['pep'], site['k']
        pg_id = i
        # ---- global proteome peptides (unmodified)
        glob_peps = [(st, p) for st, p in digest(prot['seq']) if 7 <= len(p) <= 25][:6]
        for st, gp in glob_peps:
            pe = rng.normal(0, 0.8)
            for s in SAMPLES:
                li = base_prot + pe + prot_fc * IS_T[s] + run_off_glob[s] + rng.normal(0, 0.25)
                v = observed(li)
                if v is not None:
                    ev_glob.append(ev_row(prot, gp, 'Unmodified', '_' + gp + '_', '', 'Gl_' + s, s, v, pg_id))
        # ---- enriched run: singly form (+ doubly form for multiplicity proteins)
        p_other = 1 - lp
        probs = {k: lp}
        if site['others']:
            probs[site['others'][0]] = round(p_other, 3)
        site_int = {s: {1: 0.0, 2: 0.0} for s in SAMPLES}
        forms = [(1, [k], 0.0)]
        if multi:
            forms = [(1, [k], -1.5), (2, [k, site['others'][0]], +1.5)]
        for mult, idxs, switch in forms:
            mseq = modseq(pep, idxs, tag)
            mods = modname if mult == 1 else f'{mult} {modname}'
            pstr = probs_string(pep, probs if mult == 1 else {j: 1.0 for j in idxs})
            fbase = base_site - (1.0 if mult == 2 else 0.0)
            for s in SAMPLES:
                li = fbase + (prot_fc + occ_fc + switch) * IS_T[s] + run_off_ptm[s] + rng.normal(0, 0.25)
                v = observed(li)
                if v is not None:
                    ev_ptm.append(ev_row(prot, pep, mods, mseq, pstr, 'Ph_' + s, s, v, pg_id))
                    site_int[s][mult] += v
        # a few unmodified peptides co-enriched in the enriched run (typical 5-15 %)
        for st, gp in glob_peps[:1]:
            for s in SAMPLES:
                li = base_prot - 4 + prot_fc * IS_T[s] + run_off_ptm[s] + rng.normal(0, 0.25)
                v = observed(li)
                if v is not None:
                    ev_ptm.append(ev_row(prot, gp, 'Unmodified', '_' + gp + '_', '', 'Ph_' + s, s, v, pg_id))
        pos1 = site['pos0'] + 1
        aa = prot['seq'][site['pos0']]
        truth.append({'protein': prot['acc'], 'gene': prot['gene'], 'site': f"{prot['acc']}_{aa}{pos1}", 'class': cls,
                      'true_protein_log2fc': prot_fc, 'true_occupancy_log2fc': occ_fc,
                      'observed_expected_log2fc': prot_fc + occ_fc, 'loc_prob': round(lp, 3),
                      'multiplicity_switch': multi, 'motif': motif or ''})
        row = {'Proteins': prot['acc'], 'Positions within proteins': pos1, 'Leading proteins': prot['acc'],
               'Protein': prot['acc'], 'Protein names': prot['name'],
               'Gene names': '' if i == 5 else prot['gene'],  # one blank gene name (FASTA-dependent column)
               'Fasta headers': f"sp|{prot['acc']}|{prot['gene']}_HUMAN", 'Localization prob': round(lp, 4),
               'Score diff': round(float(rng.uniform(1, 60)), 2), 'PEP': float(10 ** rng.uniform(-8, -3)),
               'Score': round(float(rng.uniform(60, 250)), 2), 'Delta score': round(float(rng.uniform(20, 150)), 2),
               'Score for localization': round(float(rng.uniform(40, 200)), 2)}
        for s in SAMPLES:
            row[f'Localization prob {s}'] = round(lp, 4)
        row.update({f'Number of {modname}': '1;2' if multi else '1', 'Amino acid': aa,
                    'Sequence window': window(prot['seq'], site['pos0']),
                    'Modification window': 'X' * 31, 'Peptide window coverage': 'X' * 31,
                    probcol: probs_string(pep, probs), 'Position in peptide': k + 1, 'Charge': 2,
                    'Mass error [ppm]': round(float(rng.normal(0, 1)), 3)})
        tot = {m: sum(site_int[s][m] for s in SAMPLES) for m in (1, 2)}
        row['Intensity'] = round(tot[1] + tot[2], 1)
        row['Intensity___1'] = round(tot[1], 1)
        row['Intensity___2'] = round(tot[2], 1)
        row['Intensity___3'] = 0.0
        row['Ratio mod/base'] = np.nan
        for s in SAMPLES:
            row[f'Intensity {s}'] = round(site_int[s][1] + site_int[s][2], 1)
            row[f'Intensity {s}___1'] = round(site_int[s][1], 1)
            row[f'Intensity {s}___2'] = round(site_int[s][2], 1)
            row[f'Intensity {s}___3'] = 0.0
        for s in SAMPLES:
            row[f'Occupancy {s}'] = np.nan
        row.update({'Reverse': '', 'Potential contaminant': '', 'id': i, 'Protein group IDs': pg_id,
                    'Positions': pos1, 'Position': pos1})
        sites_rows.append(row)
    # decoy and contaminant rows in the Sites table and the PTM evidence
    for j, (rev, con, acc) in enumerate([('+', '', 'REV__P69999'), ('', '+', 'CON__P02769')]):
        r = dict(sites_rows[20])
        r.update({'Proteins': acc, 'Leading proteins': acc, 'Protein': acc, 'Gene names': '', 'Reverse': rev,
                  'Potential contaminant': con, 'id': n + j, 'Localization prob': 0.99})
        sites_rows.append(r)
    fasta = ''.join(f">sp|{p['acc']}|{p['gene']}_HUMAN {p['name']} OS=Homo sapiens OX=9606 GN={p['gene']}\n"
                    + '\n'.join(p['seq'][i:i + 60] for i in range(0, len(p['seq']), 60)) + '\n' for p in prots)
    with open(os.path.join(d, 'synthetic.fasta'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(fasta)
    evp = pd.DataFrame(ev_ptm)[EVID_COLS].rename(columns={'PROBCOL': probcol})
    evp['id'] = range(len(evp))
    evg = pd.DataFrame(ev_glob)[EVID_COLS].drop(columns=['PROBCOL'])
    evg['id'] = range(len(evg))
    ptm_name = 'evidence_phospho.txt' if kind == 'phospho' else 'evidence_glygly.txt'
    evp.to_csv(os.path.join(d, ptm_name), sep='\t', index=False)
    evg.to_csv(os.path.join(d, 'evidence_global.txt'), sep='\t', index=False)
    # proteinGroups for the global run
    pg = []
    for i, p in enumerate(prots):
        sub = evg[evg['Protein group IDs'] == i]
        r = {'Protein IDs': p['acc'], 'Majority protein IDs': p['acc'], 'Protein names': p['name'],
             'Gene names': p['gene'], 'Peptides': sub['Sequence'].nunique(),
             'Razor + unique peptides': sub['Sequence'].nunique(), 'Unique peptides': sub['Sequence'].nunique(),
             'Q-value': 0.0, 'Score': 100.0, 'Only identified by site': '', 'Reverse': '', 'Potential contaminant': ''}
        for s in SAMPLES:
            r[f'Intensity {s}'] = round(sub.loc[sub['Experiment'] == s, 'Intensity'].sum(), 1)
        for s in SAMPLES:
            r[f'LFQ intensity {s}'] = r[f'Intensity {s}']
        r['Intensity'] = round(sub['Intensity'].sum(), 1)
        r['id'] = i
        pg.append(r)
    pd.DataFrame(pg).to_csv(os.path.join(d, 'proteinGroups_global.txt'), sep='\t', index=False)
    sites_name = 'Phospho (STY)Sites.txt' if kind == 'phospho' else 'GlyGly (K)Sites.txt'
    pd.DataFrame(sites_rows).to_csv(os.path.join(d, sites_name), sep='\t', index=False)
    pd.DataFrame(truth).to_csv(os.path.join(d, 'truth_sites.csv'), index=False)
    cond = ['Control' if s.startswith('C') else 'Treatment' for s in SAMPLES]
    pd.DataFrame({'Raw.file': ['Ph_' + s for s in SAMPLES], 'Condition': cond, 'BioReplicate': SAMPLES,
                  'IsotopeLabelType': 'L'}).to_csv(os.path.join(d, 'annotation_ptm.csv'), index=False)
    pd.DataFrame({'Raw.file': ['Gl_' + s for s in SAMPLES], 'Condition': cond, 'BioReplicate': SAMPLES,
                  'IsotopeLabelType': 'L'}).to_csv(os.path.join(d, 'annotation_protein.csv'), index=False)
    print(kind, 'proteins', n, '| PTM evidence rows', len(evp), '| global evidence rows', len(evg),
          '| site rows', len(sites_rows))


if __name__ == '__main__':
    build('phospho')
    build('glygly')
