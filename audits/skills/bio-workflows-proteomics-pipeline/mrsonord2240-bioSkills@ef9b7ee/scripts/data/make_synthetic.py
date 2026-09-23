"""SYNTHETIC proteomics test data for the mass-spec-proteomics-analyst audit (2026-09-11).

NOT REAL DATA. Seeded, deterministic. Formats mimic MaxQuant 2.x txt/ tables, a DIA-NN 1.9
report.parquet, two TMT plexes, a MaxQuant Phospho (STY)Sites.txt and its evidence tables.

Ground truth (truth_proteins.csv):
  8 runs C1-C4 (Control) / T1-T4 (Treatment); batches B1 = C1,C2,T1,T2 and B2 = C3,C4,T3,T4 (balanced).
  1500 target protein groups: 60 up, 60 down (|log2FC| 1.0-2.2), 12 on/off (absent in every T run), rest null.
  B2 carries a protein-specific batch shift (mean +0.30 log2).
  Missingness: left-censored (logistic detection curve around log2 ~21.5) + 2% MCAR.
  Bookkeeping rows: 25 REV__ decoys, 20 CON__ contaminants, 15 'Only identified by site'.
  proteinGroups_failed.txt: T4 loaded ~3x low (raw Intensity -1.58 log2, more dropout); MaxLFQ has
  re-normalised its LFQ column (residual -0.2) as MaxQuant would.
Usage: python make_synthetic.py   (writes next to this file)
"""
import os
import numpy as np
import pandas as pd

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260911)

SAMPLES = ['C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4']
COND = {s: 'Control' if s[0] == 'C' else 'Treatment' for s in SAMPLES}
BATCH = {'C1': 'B1', 'C2': 'B1', 'T1': 'B1', 'T2': 'B1', 'C3': 'B2', 'C4': 'B2', 'T3': 'B2', 'T4': 'B2'}
N = 1500
AA = 'ACDEFGHIKLMNPQRSTVWY'


def accession(i):
    letters = 'OPQ'
    return f'{letters[i % 3]}{(10000 + i * 7) % 99999:05d}'


def rand_peptide(k):
    body = ''.join(rng.choice(list('ACDEFGHILMNPQSTVWY'), size=k - 1))
    return body + rng.choice(['K', 'R'])


# ---------------------------------------------------------------- truth
acc = [accession(i) for i in range(N)]
genes = [f'GENE{i:04d}' for i in range(N)]
base = rng.normal(24.0, 2.2, N)
effect = np.zeros(N)
effect[0:60] = rng.uniform(1.0, 2.2, 60)
effect[60:120] = -rng.uniform(1.0, 2.2, 60)
onoff = np.zeros(N, bool)
onoff[120:132] = True
klass = np.array(['null'] * N, dtype=object)
klass[0:60] = 'up'
klass[60:120] = 'down'
klass[120:132] = 'on_off'
perm = rng.permutation(N)  # shuffle so truth is not positional
acc = [acc[i] for i in perm]
genes = [genes[i] for i in perm]
base, effect, onoff, klass = base[perm], effect[perm], onoff[perm], klass[perm]
batch_shift = rng.normal(0.30, 0.20, N)
pd.DataFrame({'protein': acc, 'gene': genes, 'class': klass, 'true_log2fc': effect,
              'base_log2': base.round(3)}).to_csv(os.path.join(OUT, 'truth_proteins.csv'), index=False)
pd.DataFrame({'sample': SAMPLES, 'condition': [COND[s] for s in SAMPLES],
              'replicate': [int(s[1]) for s in SAMPLES], 'batch': [BATCH[s] for s in SAMPLES]}
             ).to_csv(os.path.join(OUT, 'sample_annotation.csv'), index=False)


def true_log2(i, s):
    v = base[i] + (effect[i] if COND[s] == 'Treatment' else 0.0)
    if BATCH[s] == 'B2':
        v += batch_shift[i]
    return v


def detect(x, thr, rng_):
    p_detect = 1 / (1 + np.exp(-(x - thr) / 0.5))
    return (rng_.random(x.shape) < p_detect) & (rng_.random(x.shape) > 0.02)


LOAD = dict(zip(SAMPLES, [0.10, -0.20, 0.15, 0.00, -0.10, 0.20, -0.15, 0.05]))


def protein_matrix(failed_t4=False):
    lfq = np.zeros((N, 8))
    raw = np.zeros((N, 8))
    for j, s in enumerate(SAMPLES):
        x = np.array([true_log2(i, s) for i in range(N)]) + rng.normal(0, 0.35, N)
        load = LOAD[s] + (-1.585 if (failed_t4 and s == 'T4') else 0.0)
        thr = 21.5 + rng.normal(0, 0.2)
        seen = detect(x + load, thr, rng)
        if COND[s] == 'Treatment':
            seen &= ~onoff
        lfq_seen = seen & (rng.random(N) > 0.03)  # MaxLFQ needs ratio counts: a few extra LFQ gaps
        resid = -0.2 if (failed_t4 and s == 'T4') else 0.0
        lfq[:, j] = np.where(lfq_seen, 2 ** (x + resid + rng.normal(0, 0.05, N)), 0)
        raw[:, j] = np.where(seen, 2 ** (x + load + 1.0), 0)
    return lfq, raw


def bookkeeping_rows(kind, n):
    rows = []
    for k in range(n):
        lv = rng.normal(27.5 if kind == 'CON' else 20.5, 1.0)
        vals = {s: (2 ** (lv + rng.normal(0, 0.4)) if rng.random() > (0.1 if kind == 'CON' else 0.45) else 0.0)
                for s in SAMPLES}
        if kind == 'REV':
            pid, gene, pname = f'REV__{accession(5000 + k)}', '', ''
        elif kind == 'CON':
            pid = ['CON__P02769', 'CON__P04264', 'CON__P35908', 'CON__P13645', 'CON__P00761'][k % 5]
            pid = pid if k < 5 else f'{pid}-{k}'
            gene, pname = ['ALB', 'KRT1', 'KRT2', 'KRT10', ''][k % 5], ['Serum albumin', 'Keratin, type II cytoskeletal 1', 'Keratin, type II cytoskeletal 2 epidermal', 'Keratin, type I cytoskeletal 10', 'Trypsin'][k % 5]
        else:
            pid, gene, pname = accession(7000 + k), f'SITE{k:02d}', 'Uncharacterized protein'
        rows.append((pid, gene, pname, vals))
    return rows


APOS = ["Cytosolic 5'-nucleotidase 3A", "5'-3' exoribonuclease 2", "ATP-dependent 3'-5' DNA helicase",
        "Poly(A) RNA polymerase, mitochondrial", "tRNA (guanine(37)-N1)-methyltransferase"]


def write_protein_groups(path, failed_t4=False):
    lfq, raw = protein_matrix(failed_t4)
    recs = []
    for i in range(N):
        pid = acc[i]
        if rng.random() < 0.15:
            pid = f'{acc[i]};{acc[i]}-2;{accession(9000 + i)}'
        gene = genes[i] if rng.random() > 0.03 else ''
        if gene and rng.random() < 0.05:
            gene = f'{gene};{gene}L'
        pname = APOS[i % 5] if i % 97 == 0 else f'Protein {genes[i].title()}'
        npep = int(max(1, rng.poisson(max(1, (base[i] - 19) * 2.2))))
        rec = {'Protein IDs': pid, 'Majority protein IDs': pid.split(';')[0] if ';' in pid and rng.random() < 0.5 else pid,
               'Protein names': pname, 'Gene names': gene, 'Peptides': npep,
               'Razor + unique peptides': npep, 'Unique peptides': max(1, npep - int(';' in pid)),
               'Sequence coverage [%]': round(min(95, npep * 3.1), 1), 'Mol. weight [kDa]': round(rng.uniform(10, 250), 3),
               'Q-value': 0.0, 'Score': round(min(323.31, npep * 12.4), 3),
               'Only identified by site': '', 'Reverse': '', 'Potential contaminant': ''}
        ntheo = int(rng.integers(8, 80))
        for j, s in enumerate(SAMPLES):
            rec[f'Intensity {s}'] = raw[i, j]
        for j, s in enumerate(SAMPLES):
            rec[f'iBAQ {s}'] = raw[i, j] / ntheo
        for j, s in enumerate(SAMPLES):
            rec[f'LFQ intensity {s}'] = lfq[i, j]
        for j, s in enumerate(SAMPLES):
            rec[f'MS/MS count {s}'] = int(rng.poisson(npep * 1.5)) if raw[i, j] > 0 else 0
        recs.append(rec)
    for kind, n in (('REV', 25), ('CON', 20), ('SITE', 15)):
        for pid, gene, pname, vals in bookkeeping_rows(kind, n):
            rec = {'Protein IDs': pid, 'Majority protein IDs': pid, 'Protein names': pname, 'Gene names': gene,
                   'Peptides': 1 if kind != 'CON' else 12, 'Razor + unique peptides': 1 if kind != 'CON' else 12,
                   'Unique peptides': 1 if kind != 'CON' else 10, 'Sequence coverage [%]': 4.0,
                   'Mol. weight [kDa]': 55.0, 'Q-value': 0.004 if kind == 'REV' else 0.0, 'Score': 5.1,
                   'Only identified by site': '+' if kind == 'SITE' else '',
                   'Reverse': '+' if kind == 'REV' else '',
                   'Potential contaminant': '+' if kind == 'CON' else ''}
            for s in SAMPLES:
                rec[f'Intensity {s}'] = vals[s] * 2
            for s in SAMPLES:
                rec[f'iBAQ {s}'] = vals[s] / 20
            for s in SAMPLES:
                rec[f'LFQ intensity {s}'] = vals[s]
            for s in SAMPLES:
                rec[f'MS/MS count {s}'] = 1 if vals[s] > 0 else 0
            recs.append(rec)
    df = pd.DataFrame(recs)
    df['Intensity'] = df[[f'Intensity {s}' for s in SAMPLES]].sum(axis=1)
    df['id'] = np.arange(len(df))
    df = df.sample(frac=1.0, random_state=7).reset_index(drop=True)
    df['id'] = np.arange(len(df))
    df.to_csv(path, sep='\t', index=False)
    return df


pg = write_protein_groups(os.path.join(OUT, 'proteinGroups.txt'))
write_protein_groups(os.path.join(OUT, 'proteinGroups_failed.txt'), failed_t4=True)

# ---------------------------------------------------------------- evidence.txt (peptide level, 300 proteins)
sub_idx = list(np.where(klass != 'null')[0][:90]) + list(np.where(klass == 'null')[0][:210])
acc_to_id = {}
for _, r in pg.iterrows():
    acc_to_id[r['Protein IDs'].split(';')[0]] = int(r['id'])
ev = []
evid = 0
for i in sub_idx:
    pid_row = pg[pg['Protein IDs'].str.split(';').str[0] == acc[i]].iloc[0]
    npep = int(rng.integers(2, 9))
    for p in range(npep):
        seq = rand_peptide(int(rng.integers(7, 20)))
        pep_eff = rng.normal(0, 1.2)
        charge = int(rng.choice([2, 3], p=[0.7, 0.3]))
        for s in SAMPLES:
            x = true_log2(i, s) + pep_eff + LOAD[s] + rng.normal(0, 0.25)
            if COND[s] == 'Treatment' and onoff[i]:
                continue
            if not detect(np.array([x]), 21.0, rng)[0]:
                continue
            ev.append({'Sequence': seq, 'Length': len(seq), 'Modifications': 'Unmodified',
                       'Modified sequence': f'_{seq}_', 'Missed cleavages': 0,
                       'Proteins': pid_row['Protein IDs'], 'Leading proteins': acc[i], 'Leading razor protein': acc[i],
                       'Gene names': pid_row['Gene names'], 'Protein names': pid_row['Protein names'],
                       'Type': 'MULTI-MSMS', 'Raw file': s, 'Experiment': s, 'Charge': charge,
                       'm/z': round(rng.uniform(400, 1200), 4), 'Retention time': round(rng.uniform(10, 110), 3),
                       'PEP': round(10 ** rng.uniform(-8, -2), 10), 'Score': round(rng.uniform(40, 250), 2),
                       'Intensity': round(2 ** x, 1), 'Reverse': '', 'Potential contaminant': '',
                       'id': evid, 'Protein group IDs': int(pid_row['id'])})
            evid += 1
evidence = pd.DataFrame(ev)
evidence.to_csv(os.path.join(OUT, 'evidence.txt'), sep='\t', index=False)
pg_sub = pg[pg['id'].isin(evidence['Protein group IDs'].unique())]
pg_sub.to_csv(os.path.join(OUT, 'proteinGroups_evidence_subset.txt'), sep='\t', index=False)
pd.DataFrame({'Raw.file': SAMPLES, 'Condition': [COND[s] for s in SAMPLES],
              'BioReplicate': SAMPLES, 'IsotopeLabelType': 'L'}).to_csv(os.path.join(OUT, 'annotation_msstats.csv'), index=False)

# ---------------------------------------------------------------- DIA-NN 1.9-style report.parquet
dia_idx = list(range(0, 900))
rows = []
for i in dia_idx:
    npr = int(rng.integers(2, 6))
    precs = [(rand_peptide(int(rng.integers(7, 22))), int(rng.choice([2, 3]))) for _ in range(npr)]
    for s in SAMPLES:
        x = true_log2(i, s) + LOAD[s] + rng.normal(0, 0.2)
        if COND[s] == 'Treatment' and onoff[i]:
            continue
        if not detect(np.array([x]), 20.5, rng)[0]:
            continue
        pgq = 10 ** rng.uniform(-5, -2.3)
        maxlfq = 0.0 if rng.random() < 0.01 else round(2 ** (x - LOAD[s]), 1)
        for seq, z in precs:
            rows.append({'Run': f'{s}_DIA', 'Protein.Group': acc[i], 'Protein.Ids': acc[i], 'Protein.Names': f'{genes[i]}_HUMAN',
                         'Genes': genes[i], 'Precursor.Id': f'{seq}{z}', 'Modified.Sequence': seq, 'Stripped.Sequence': seq,
                         'Precursor.Charge': z, 'Q.Value': 10 ** rng.uniform(-5, -1.6), 'PEP': 10 ** rng.uniform(-6, -1),
                         'Global.Q.Value': 10 ** rng.uniform(-5, -2.2), 'PG.Q.Value': pgq, 'Global.PG.Q.Value': 10 ** rng.uniform(-5, -2.3),
                         'Lib.Q.Value': 10 ** rng.uniform(-5, -2.2), 'Lib.PG.Q.Value': 10 ** rng.uniform(-5, -2.3),
                         'Precursor.Quantity': round(2 ** (x + rng.normal(-1, 0.8)), 1),
                         'Precursor.Normalised': round(2 ** (x - LOAD[s] + rng.normal(-1, 0.8)), 1),
                         'PG.Quantity': round(2 ** (x + 0.5), 1), 'PG.MaxLFQ': maxlfq, 'RT': round(rng.uniform(5, 60), 3)})
# 60 low-confidence groups: pass run-level PG.Q.Value in 1-3 runs but FAIL experiment-wide Global.PG.Q.Value
for k in range(60):
    seq = rand_peptide(11)
    for s in rng.choice(SAMPLES, size=int(rng.integers(1, 4)), replace=False):
        rows.append({'Run': f'{s}_DIA', 'Protein.Group': f'LOWCONF{k:02d}', 'Protein.Ids': f'LOWCONF{k:02d}', 'Protein.Names': '',
                     'Genes': '', 'Precursor.Id': f'{seq}2', 'Modified.Sequence': seq, 'Stripped.Sequence': seq, 'Precursor.Charge': 2,
                     'Q.Value': 0.008, 'PEP': 0.2, 'Global.Q.Value': 0.03, 'PG.Q.Value': 0.009, 'Global.PG.Q.Value': 0.04,
                     'Lib.Q.Value': 0.03, 'Lib.PG.Q.Value': 0.04, 'Precursor.Quantity': 2 ** 19, 'Precursor.Normalised': 2 ** 19,
                     'PG.Quantity': 2 ** 19.5, 'PG.MaxLFQ': 2 ** 19.2, 'RT': 30.0})
report = pd.DataFrame(rows)
report.to_parquet(os.path.join(OUT, 'report.parquet'), index=False)

# ---------------------------------------------------------------- TMT: two 10-plex runs, pooled reference in channel 131
tmt_prot = [acc[i] for i in range(600)]
chans = ['126', '127N', '127C', '128N', '128C', '129N', '129C', '130N', '130C', '131']
design_tmt = []
for plex, members in (('A', ['C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4', 'C5', 'T5']),
                      ('B', ['C6', 'C7', 'C8', 'C9', 'T6', 'T7', 'T8', 'T9', 'C10', 'T10'])):
    plex_eff = rng.normal(0, 0.8, 600) + (1.0 if plex == 'B' else 0.0)  # elution-sampling offset, not biology
    mat = {}
    for c, m in zip(chans, members):
        if c == '131':
            continue
        is_t = m.startswith('T')
        x = np.array([base[i] + (effect[i] * 0.6 if is_t else 0) for i in range(600)])  # MS2 ratio compression ~0.6
        x = x + plex_eff + rng.normal(0, 0.25, 600) + rng.normal(0, 0.15)
        mat[c] = 2 ** x
        design_tmt.append({'plex': plex, 'channel': c, 'sample': f'{plex}_{m}', 'condition': 'Treatment' if is_t else 'Control'})
    ref = np.mean(np.vstack([np.log2(v) for v in mat.values()]), axis=0)
    mat['131'] = 2 ** (ref + rng.normal(0, 0.1, 600))
    design_tmt.append({'plex': plex, 'channel': '131', 'sample': f'{plex}_REF', 'condition': 'Reference'})
    df = pd.DataFrame(mat, index=tmt_prot)[chans]
    df.index.name = 'protein'
    df.round(1).to_csv(os.path.join(OUT, f'tmt_plex{plex}.csv'))
pd.DataFrame(design_tmt).to_csv(os.path.join(OUT, 'tmt_design.csv'), index=False)

print('wrote', sorted(os.listdir(OUT)))
print('proteinGroups rows', len(pg), '| evidence rows', len(evidence), '| DIA report rows', len(report))
